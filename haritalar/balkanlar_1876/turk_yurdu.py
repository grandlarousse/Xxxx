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


# ------------------------------------------------------------------ çizim
def render(key, out_dir, ppd=100):
    cfg_p = os.path.join(S.SERI, f"yurt_{key}.json")
    cfg = S.sanitize(json.load(open(cfg_p, encoding="utf-8"))) if os.path.exists(cfg_p) else {}
    Y_ = YURTLAR[key]
    mpp = Y_["width"] * 1000 / W
    shift = (0, -(H / 2 - (MAP_TOP + MAP_BOT) / 2) * mpp / 1000)
    F = E.Frame(W, H, Y_["width"], center_lonlat=Y_["center"], shift_km=shift)
    elev = E.dem_on_frame(F, z=9)
    countries, land, region, by = P.build_masks(F)
    landm = rasterize_pil(land, F, 1.0)
    regm = rasterize_pil(region, F, 1.0)
    regm2 = rasterize_pil(region, F, 2.0)
    elev2 = elev[::2, ::2][:regm2.shape[0], :regm2.shape[1]]
    F0, ott0, non0 = S.master_masks()
    ott1 = S.sample_master(F, ott0, F0) & regm
    non1 = S.sample_master(F, non0, F0)

    cl_all = load_clusters5()
    cx, cy = F.ll_to_px([c["lon"] for c in cl_all], [c["lat"] for c in cl_all])
    cx, cy = np.asarray(cx), np.asarray(cy)
    rpx = np.array([c["radius_km"] for c in cl_all]) * 1000 / F.mpp
    near = (cx > -2 * rpx - 60) & (cx < W + 2 * rpx + 60) & (cy > -2 * rpx - 60) & (cy < H + 2 * rpx + 60)
    cl = [c for c, n in zip(cl_all, near) if n and c.get("vilayet") != "İstanbul"]
    x, y, k, ci = E.make_dots(cl, F, regm2, elev2, people_per_dot=ppd, seed=1876, return_cluster=True, cats=CATS5,
                              village_sigma_km=0.6)
    xi, yi = np.clip(x.astype(int), 0, W - 1), np.clip(y.astype(int), 0, H - 1)
    inside = ott1[yi, xi]
    log(f"[{key}] {x.size} nokta")

    # ---- altlık: sade, koyu rölyef
    hs, slope, flat = E.multi_hillshade(elev, F.mpp)
    shade = gaussian_filter(np.clip(hs / flat, 0, 1.6) / 1.6, 0.6)
    d_sea = distance_transform_edt(~landm) * F.mpp / 1000
    coast = np.exp(-d_sea / 8.0)[..., None]
    img = hf("#06090E") * (1 - coast) + hf("#0C1420") * coast
    lo, hi = hf("#0E131B"), hf("#232B37")
    img = np.where(landm[..., None], lo + (hi - lo) * shade[..., None] ** 1.2, img)
    base = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8)).convert("RGBA")

    lab = yurt_labels(F, x, y, k, ott1 & landm)
    base.alpha_composite(fill_image(lab))
    # nehirler (ince, koyu)
    fade = np.ones((H, 1), np.float32)
    base.alpha_composite(P.draw_rivers(F, regm, fade, under=False))
    draw_dots(base, x, y, k, inside)
    # 1876 sınırı (varsa)
    outside = shapely.union_all([by[a3] for a3 in ("ROU", "HUN", "SVN", "HRV", "SRB", "MNE", "AUT") if a3 in by])
    to_g = lambda geom: gpd.GeoSeries([geom], crs="EPSG:4326").to_crs(E.CRS).iloc[0]
    foreign = rasterize_pil(to_g(outside), F, 1.0) & ~regm
    foreign |= (regm & ~ott1 & non1)
    foreign = P.binary_opening(foreign, iterations=2) & landm & ~ott1
    if foreign.any():
        fl, _ = P.frontier_layer(ott1, foreign)
        base.alpha_composite(fl)

    # ---- istatistik (Türk yurdu)
    tm = lab == 0
    km2 = tm.sum() * (F.mpp / 1000) ** 2
    in_t = tm[yi, xi] & inside
    cnt = np.bincount(k[in_t], minlength=NG).astype(float)
    tp = 100 * cnt / max(1, cnt.sum())
    mus_t = tp[:T.NMUS].sum()
    allp = np.bincount(k[inside], minlength=NG).astype(float)
    allp = 100 * allp / max(1, allp.sum())
    present = [g for g in range(NG) if allp[g] >= 0.6 or g == 0]
    log(f"[{key}] Türk yurdu ≈{km2:,.0f} km² · içinde Türk %{tp[0]:.1f} Müslüman %{mus_t:.1f} · nüfus {cnt.sum() * ppd:,.0f}")
    log(f"[{key}] çerçevedeki topluluklar: " + ", ".join(f"{NAMES5[g]} %{allp[g]:.1f}" for g in present))

    # ---- başlık arkası ve alt şerit koyulaştır
    yy = np.arange(H, dtype=np.float32)[:, None]
    a_top = np.clip((MAP_TOP + 30 - yy) / 110, 0, 1) * 0.94
    a_bot = np.clip((yy - (MAP_BOT - 30)) / 90, 0, 1) * 0.94
    ov = np.zeros((H, W, 4), np.uint8)
    ov[..., :3] = hx(INK)[:3]
    ov[..., 3] = (np.repeat(np.maximum(a_top, a_bot), W, 1) * 255).astype(np.uint8)
    base.alpha_composite(Image.fromarray(ov, "RGBA"))
    cv = Canvas(base)
    cv.occupy((0, 0, W, MAP_TOP - 4))
    cv.occupy((0, MAP_BOT - 4, W, H))
    d = cv.d

    # ---- başlık
    t = P.tr_upper(cfg.get("title") or Y_["title"])
    ts = 156
    while bs(ts).getlength(t) > 1900:
        ts -= 2
    d.text((W / 2, 238), t, font=bs(ts), fill=IV, anchor="ms")
    sub = cfg.get("subtitle") or "1876: Türklerin bariz çoğunlukta olduğu topraklar"
    ss = 46
    while bod(ss, 600, 11).getlength(sub) > 1900:
        ss -= 2
    d.text((W / 2, 316), sub, font=bod(ss, 600, 11), fill=IV2, anchor="ms")
    # lejant (5 grup) — tek satır, sade
    f1 = bar(30, "SemiBold")
    items = [(g, NAMES5[g]) for g in present]
    while sum(46 + f1.getlength(n) + 30 for _, n in items) - 30 > 1980 and f1.size > 22:
        f1 = bar(f1.size - 1, "SemiBold")
    tot = sum(46 + f1.getlength(n) + 30 for _, n in items) - 30
    x0 = W / 2 - tot / 2
    yb = 392
    for g, n in items:
        if g == 0:
            d.rectangle((x0, yb - 26, x0 + 32, yb - 2), fill=hx(COL5[0], 210), outline=hx("#FF6E7D"), width=2)
            for o in range(-30, 40, 9):
                d.line((x0 + o, yb - 2, x0 + o + 24, yb - 26), fill=hx("#FFB3BC", 150), width=2)
            d.rectangle((x0 - 2, yb - 28, x0 + 34, yb), outline=hx(INK), width=2)
            d.rectangle((x0, yb - 26, x0 + 32, yb - 2), outline=hx("#FF6E7D"), width=2)
        else:
            d.rectangle((x0, yb - 26, x0 + 32, yb - 2), fill=hx(COL5[g], 120))
            d.ellipse((x0 + 11, yb - 19, x0 + 21, yb - 9), fill=hx(TINT5[g]))
        d.text((x0 + 44, yb), n, font=f1, fill=hx(TINT5[g]), anchor="ls")
        x0 += 46 + f1.getlength(n) + 30
    rule = f"Kırmızı taralı alan = Türk yurdu: köylerinin en az %{int(TURK_RULE * 100)}’ı Türk · diğer alanlar yerel çoğunluk · 1 nokta = {ppd} kişi"
    d.text((W / 2, 440), rule, font=bar(24, "Medium"), fill=MUTE, anchor="ms")

    # ---- etiketler (az ve öz)
    S.MAP_TOP, S.MAP_BOT = MAP_TOP, MAP_BOT
    cities = [c for c in (cfg.get("cities") or []) if int(c.get("tier", 3)) <= 2]
    S.place_city_list(cv, F, [c for c in cities if int(c.get("tier", 3)) == 1])
    # hikâye etiketleri topluluk rengini alır ("cat": "torbes" vb.; yoksa "group" = CATS5 sırası)
    tint0 = S.TINT
    S.TINT = {i: hx(TINT5[i]) for i in range(NG)}
    labs = [dict(lb, group=CATS5.index(lb["cat"])) if lb.get("cat") in CATS5 else lb
            for lb in (cfg.get("story_labels") or [])]
    S.place_story(cv, F, labs)
    S.TINT = tint0
    S.place_city_list(cv, F, [c for c in cities if int(c.get("tier", 3)) == 2])

    # ---- alt şerit: üç rakam + bir cümle
    d = cv.d
    d.line((80, MAP_BOT + 6, W - 80, MAP_BOT + 6), fill=BRASS[:3] + (150,), width=1)
    cols = [
        (f"≈ {fmt_int(round(km2, -2))} km²", "Türk yurdu", "kırmızı taralı alan · harita modeli"),
        (fmt_pct(tp[0]), "Türk", f"Türk yurdunda yaşayanlar arasında · Müslüman toplam {fmt_pct(mus_t)}"),
    ]
    rec = cfg.get("record") or {}
    if rec:
        cols.append((rec.get("big", ""), rec.get("line1", ""), rec.get("src", "")))
    cw = (W - 160) / len(cols)
    for i, (big, l1, l2) in enumerate(cols):
        x_ = 80 + i * cw
        if i:
            d.line((x_ - 20, MAP_BOT + 40, x_ - 20, MAP_BOT + 230), fill=BRASS[:3] + (80,), width=1)
        d.text((x_, MAP_BOT + 128), big, font=bs(104), fill=hx("#FF8592") if i < 2 else IV, anchor="ls")
        d.text((x_, MAP_BOT + 172), l1, font=bar(32, "SemiBold"), fill=IV, anchor="ls")
        for j, ln in enumerate(S.wrap(l2, bar(21, "Medium"), cw - 40)[:2]):
            d.text((x_, MAP_BOT + 204 + j * 26), ln, font=bar(21, "Medium"), fill=MUTE, anchor="ls")
    nar = cfg.get("line") or ""
    if nar:
        for j, ln in enumerate(S.wrap(nar, bod(30, 600, 11), W - 200)[:2]):
            d.text((W / 2, MAP_BOT + 300 + j * 40), ln, font=bod(30, 600, 11), fill=IV2, anchor="ms")
    src = cfg.get("sources_line") or "Kaynak: Osmanlı salname ve tahrir kayıtları; harita modeli"
    meth = ("Yöntem: Osmanlı kayıtlarına dayalı bölge kümeleri; nokta yerleri ve alan sınırları temsilîdir · "
            "topluluk ayrımı (Pomak, Çerkes, Rum, Bulgar…): Osmanlı millet kayıtları ve dönem etnografyası · Tatar ve Nogaylar Türk sayıldı · Yahudiler gösterilmedi")
    lines = S.wrap(src, bar(18, "Medium"), 1960) + S.wrap(meth, bar(18, "Medium"), 1960)
    for j, ln in enumerate(lines[:3]):
        d.text((W / 2, H - 92 + j * 22), ln, font=bar(18, "Medium"), fill=MUTE, anchor="ms")
    # çerçeve: ince çizgi + seri etiketi
    d.rectangle((26, 26, W - 26, H - 26), outline=BRASS[:3] + (170,), width=2)
    P.series_tag(cv, f"{Y_['n']}/{TOTAL}", prefix=SERIES)

    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.join(out_dir, f"{Y_['n']:02d}_{key}")
    out = cv.img.convert("RGB")
    out.save(stem + ".png", optimize=True)
    out.resize((1080, 1350), Image.LANCZOS).save(stem + "_ig.jpg", quality=95, subsampling=0)
    json.dump(dict(km2=km2, turk=tp[0], muslim=mus_t, shares=dict(zip(NAMES5, tp.tolist())),
                   frame_shares=dict(zip(NAMES5, allp.tolist())), people=float(cnt.sum() * ppd)),
              open(stem + "_stats.json", "w"), ensure_ascii=False)
    log(f"[{key}] -> {stem}.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--out", default=os.path.join(HERE, "cikti", "turk_yurtlari"))
    a = ap.parse_args()
    for key in (a.keys or list(YURTLAR)):
        render(key, a.out)


if __name__ == "__main__":
    main()
