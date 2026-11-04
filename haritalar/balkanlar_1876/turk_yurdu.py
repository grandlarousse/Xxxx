#!/usr/bin/env python3
"""RUMELİ TÜRK YURTLARI 1876 — Türklerin bariz çoğunlukta olduğu kuşaklar (sade tasarım).

Kurallar:
  * 5 grup: Türk · Balkan Müslümanları · Bulgar · Rum · diğer Hristiyan
  * Türk yurdu: köylerinin en az %40'ı Türk olan alanlar (kırmızı dolgu + çizgi + sınır).
    Diğer alanlar yerel çoğunluğun rengini (soluk) alır; boşluklar çevrenin rengiyle dolar.
  * 1 nokta = 100 kişi; noktalar temsilîdir.
Veri: data_cal/clusters_calibrated.json + seri/hristiyan_ayrimi.json (Hristiyan payının bölünmesi)
İçerik: seri/yurt_<anahtar>.json
Kullanım: python3 turk_yurdu.py [rodoplar drama deliorman dobruca makedonya]
"""
import argparse
import json
import math
import os

import numpy as np
import shapely
import geopandas as gpd
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, distance_transform_edt

import engine as E
import poster as P
import seri as S
import topluluk as T
from poster import Canvas, hx, bs, bod, bar, fmt_int, fmt_pct, rasterize_pil, log, W, H

HERE = os.path.dirname(os.path.abspath(__file__))
# topluluklar (sıra lejant sırasıdır) — ortak tanım: topluluk.py
CATS5, NAMES5, COL5, TINT5, NG = T.CATS, T.NAMES, T.COL, T.TINT, T.NG
INK = "#0A0E14"
IV, IV2, MUTE, BRASS = hx("#F1E9D8"), hx("#DED6C6"), hx("#97A1B3"), hx("#B89B5E")
TURK_RULE = T.TURK_RULE   # Türk yurdu eşiği
MAP_TOP, MAP_BOT = 470, 2250
TOTAL = 5
SERIES = "RUMELİ TÜRK YURTLARI 1876"

YURTLAR = {
    "rodoplar": dict(n=1, center=(25.62, 41.52), width=210, title="Doğu Rodoplar"),
    "drama": dict(n=2, center=(24.42, 41.08), width=170, title="Drama, Kavala ve Sarışaban"),
    "deliorman": dict(n=3, center=(26.82, 43.43), width=230, title="Deliorman ve Gerlovo"),
    "dobruca": dict(n=4, center=(28.32, 44.27), width=230, title="Dobruca"),
    "makedonya": dict(n=5, center=(22.30, 41.17), width=250, title="Makedonya Türkleri"),
}


def hf(h):
    return np.array(hx(h)[:3], np.float32) / 255


# ------------------------------------------------------------------ veri
def load_clusters5():
    return T.split_named(S.load_cal())


def yurt_labels(F, x, y, k, area, sigma_km=2.6, step=2):
    return T.yurt_labels(F, x, y, k, area, sigma_km=sigma_km, step=step, rule=TURK_RULE)


def fill_image(lab, spacing=13, lw=2.4):
    Y, X = np.mgrid[0:H, 0:W]
    v = (X - Y) % spacing
    hatch = np.clip(lw / 2 + 0.5 - np.abs(v - spacing / 2), 0, 1).astype(np.float32)
    lay = np.zeros((H, W, 4), np.float32)
    for g in range(NG):
        m = lab == g
        if not m.any():
            continue
        lay[m, :3] = np.array(hx(COL5[g])[:3], np.float32)
        lay[m, 3] = (0.50 + 0.30 * hatch[m]) if g == 0 else 0.26
    # Türk yurdu sınırı
    tm = (lab == 0)
    d_in = distance_transform_edt(tm)
    d_out = distance_transform_edt(~tm & (lab >= 0))
    edge = np.clip(2.0 - np.where(tm, d_in, d_out), 0, 1) * (lab >= 0)
    lay[..., :3] = lay[..., :3] * (1 - edge[..., None]) + np.array([255, 110, 125], np.float32) * edge[..., None]
    lay[..., 3] = np.maximum(lay[..., 3], edge * 0.95)
    return Image.fromarray(np.clip(lay * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA")


def draw_dots(img, x, y, k, inside):
    S_ = 3
    r = 1.55 * S_
    lay = Image.new("RGBA", (W * S_, H * S_), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    order = np.random.default_rng(1876).permutation(x.size)
    for i in order:
        g = int(k[i])
        a = 235 if inside[i] else 70
        xa, ya = x[i] * S_, y[i] * S_
        d.ellipse((xa - r, ya - r, xa + r, ya + r), fill=hx(TINT5[g])[:3] + (a,))
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))


# ------------------------------------------------------------------ çizim (ortak sade motor: sade.py)
def render(key, out_dir, ppd=100):
    import sade
    cfg_p = os.path.join(S.SERI, f"yurt_{key}.json")
    cfg = S.sanitize(json.load(open(cfg_p, encoding="utf-8"))) if os.path.exists(cfg_p) else {}
    Y_ = YURTLAR[key]
    cfg.setdefault("title", Y_["title"])
    cfg.setdefault("subtitle", "1876: Türklerin bariz çoğunlukta olduğu topraklar")
    cfg["cities"] = [c for c in (cfg.get("cities") or []) if int(c.get("tier", 3)) <= 2]
    spec = dict(n=Y_["n"], total=TOTAL, series=SERIES, center=Y_["center"], width=Y_["width"], ppd=ppd, focus=None)
    rec = cfg.get("record") or {}

    def cols(st):
        out = [(sade.km2_txt(st["km2_turk"]), "Türk yurdu", "kırmızı taralı alan · harita modeli"),
               (fmt_pct(st["turk_in_yurt"]), "Türk", f"Türk yurdunda yaşayanlar arasında · Müslüman toplam {fmt_pct(st['muslim_in_yurt'])}")]
        if rec:
            out.append((rec.get("big", ""), rec.get("line1", ""), rec.get("src", "")))
        return out

    os.makedirs(out_dir, exist_ok=True)
    return sade.render_simple(spec, cfg, os.path.join(out_dir, f"{Y_['n']:02d}_{key}"), cols)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--out", default=os.path.join(HERE, "cikti", "turk_yurtlari"))
    a = ap.parse_args()
    for key in (a.keys or list(YURTLAR)):
        render(key, a.out)


if __name__ == "__main__":
    main()
