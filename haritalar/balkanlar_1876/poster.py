#!/usr/bin/env python3
"""RUMELİ’NİN SON IŞIKLARI · 1876 — Balkanlar’da Türkler, diğer Müslümanlar ve Hristiyanlar.

Gece uydu görüntüsü estetiğinde nokta yoğunluğu haritası (1 nokta = 250 kişi).
Veri: data/*.json (Osmanlı salname/sayım öncelikli bölge kümeleri),
Bulgaristan il hedefleri (calibrate.TARGET_BG), 1876 sınırı (data/frontier_1876.json).

Kullanım:  python3 poster.py [--imza "..."] [--out cikti/rumeli_1876]
"""
import argparse
import glob
import json
import math
import os
import time

import numpy as np
import shapely
import geopandas as gpd
from shapely.geometry import box, Point
from scipy.ndimage import gaussian_filter, distance_transform_edt, label as nd_label, binary_dilation, binary_opening
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import engine as E
import render as R
import calibrate as C

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")
W, H = 2160, 2700
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


# ------------------------------------------------------------------ renkler
def hx(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def hf(h):
    return np.array(hx(h)[:3], np.float32) / 255


INK = "#04070D"
COL = {0: "#E83A55", 1: "#FFC83D", 2: "#4A90F0"}          # Türk / Diğer Müslüman / Hristiyan
TINT = {0: hx("#FF6B7F"), 1: hx("#FFD166"), 2: hx("#7FB2FF")}
IV, IV2, MUTE = hx("#F1E9D8"), hx("#DED6C6"), hx("#96A0B2")
BRASS, BRASS_L, BRASS_D = hx("#B89B5E"), hx("#D9BE84"), hx("#7E6538")
FRONT = hx("#EDE3CC")
GROUP_NAMES = ["Türk", "Diğer Müslüman", "Hristiyan"]

# ------------------------------------------------------------------ kayıtlar
RECORDS = {
    "TUNA_1875": dict(males=1120954, muslim=461602, muslim_pct=41.2, bulgar_pct=54.0,
                      islam_pct=36.2, cerkes_kibti_pct=4.9, diger_pct=4.8,
                      src="Tuna Vilâyeti 1292/1875 tahriri (A. Koyuncu, Turkish Studies 9/4, 2014)"),
    "EDIRNE_1293": dict(muslim_pct=38.2, src="Devlet Salnamesi 1293, Edirne vilâyeti (Ubicini & Pavet de Courteille 1876)"),
    "BOSNA_1287": dict(bosna_pct=51.0, hersek_pct=49.0, src="Bosna 1287/1870 salnamesi (Z. Gölen, Belleten 65, 2001)"),
    "BG1875": dict(src="swenstone0 derlemesi (bugünkü il sınırlarına göre)", src_short="swenstone0 derlemesi"),
    "MCCARTHY": dict(muslims=1501883, dead=261937, emigrated=515000,
                     src="J. McCarthy tahmini (aktaran A. Koyuncu, Avrasya Etüdleri 44, 2013)"),
}
if not RECORDS["BG1875"]["src"]:
    raise SystemExit("BG1875 kaynağı boş olamaz")


# ------------------------------------------------------------------ yazı tipleri
_fc = {}


def bs(size, wght=800):
    k = ("bs", size, wght)
    if k not in _fc:
        f = ImageFont.truetype(f"{FD}/BigShouldersDisplay[wght].ttf", int(size))
        f.set_variation_by_axes([wght])
        _fc[k] = f
    return _fc[k]


def bod(size, wght=500, opsz=28):
    k = ("bod", size, wght, opsz)
    if k not in _fc:
        f = ImageFont.truetype(f"{FD}/BodoniModa[opsz,wght].ttf", int(size))
        vals = []
        for a in f.get_variation_axes():
            n = a["name"] if isinstance(a["name"], str) else a["name"].decode()
            vals.append({"Optical size": opsz, "Weight": wght}.get(n, a["default"]))
        f.set_variation_by_axes(vals)
        _fc[k] = f
    return _fc[k]


def bar(size, w="Medium"):
    k = ("bar", size, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(f"{FD}/BarlowSemiCondensed-{w}.ttf", int(size))
    return _fc[k]


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def fmt_int(n):
    return f"{int(round(n)):,}".replace(",", ".")


def fmt_pct(v, nd=1):
    s = f"{v:.{nd}f}".replace(".", ",")
    return "%" + s


# ------------------------------------------------------------------ tuval yardımcıları
class Canvas:
    def __init__(self, img):
        self.img = img
        self.obst = []  # dolu dikdörtgenler (x0,y0,x1,y1)

    @property
    def d(self):
        return ImageDraw.Draw(self.img)

    def free(self, rect, pad=4):
        x0, y0, x1, y1 = rect
        if x0 < 50 or y0 < 50 or x1 > W - 50 or y1 > H - 50:
            return False
        for a in self.obst:
            if not (x1 + pad < a[0] or x0 - pad > a[2] or y1 + pad < a[1] or y0 - pad > a[3]):
                return False
        return True

    def clear(self, rect, pad=0):
        """Yalnız engellere bakar (kenar sınırı yok)."""
        x0, y0, x1, y1 = rect
        for a in self.obst:
            if not (x1 + pad < a[0] or x0 - pad > a[2] or y1 + pad < a[1] or y0 - pad > a[3]):
                return False
        return True

    def occupy(self, rect):
        self.obst.append(tuple(rect))

    def tracked_w(self, text, fnt, track):
        return sum(fnt.getlength(c) for c in text) + track * max(0, len(text) - 1)

    def tracked(self, xy, text, fnt, track, fill, anchor="l", layer=None):
        """Harf aralıklı metin; xy taban çizgisi noktası."""
        w = self.tracked_w(text, fnt, track)
        x0, y0 = xy
        if anchor == "c":
            x0 -= w / 2
        elif anchor == "r":
            x0 -= w
        tgt = layer if layer is not None else self.img
        dd = ImageDraw.Draw(tgt)
        for ch in text:
            dd.text((x0, y0), ch, font=fnt, fill=fill, anchor="ls")
            x0 += fnt.getlength(ch) + track
        return w

    def halo(self, xy, text, fnt, fill, anchor="ls", rad=4, strength=0.85, track=0):
        """Yumuşak (bulanık) hale + metin; kontur değil."""
        if track:
            w = self.tracked_w(text, fnt, track)
            bb = (xy[0] - (w / 2 if anchor[0] == "m" else 0), xy[1] - fnt.size, xy[0] + w, xy[1] + fnt.size * 0.3)
        else:
            bb = ImageDraw.Draw(self.img).textbbox(xy, text, font=fnt, anchor=anchor)
        pad = rad * 4 + 4
        x0, y0 = int(bb[0] - pad), int(bb[1] - pad)
        x1, y1 = int(bb[2] + pad), int(bb[3] + pad)
        lay = Image.new("L", (x1 - x0, y1 - y0), 0)
        ld = ImageDraw.Draw(lay)
        if track:
            xx = xy[0] - x0 - (self.tracked_w(text, fnt, track) / 2 if anchor[0] == "m" else 0)
            for ch in text:
                ld.text((xx, xy[1] - y0), ch, font=fnt, fill=255, anchor="ls", stroke_width=rad, stroke_fill=255)
                xx += fnt.getlength(ch) + track
        else:
            ld.text((xy[0] - x0, xy[1] - y0), text, font=fnt, fill=255, anchor=anchor, stroke_width=rad, stroke_fill=255)
        lay = lay.filter(ImageFilter.GaussianBlur(rad * 0.9))
        lay = lay.point(lambda v: int(min(255, v * strength * 1.25)))
        dark = Image.new("RGBA", lay.size, (3, 5, 10, 255))
        self.img.paste(dark, (x0, y0), lay)
        if track:
            self.tracked((xy[0], xy[1]), text, fnt, track, fill, anchor="c" if anchor[0] == "m" else "l")
        else:
            ImageDraw.Draw(self.img).text(xy, text, font=fnt, fill=fill, anchor=anchor)
        return bb

    def panel(self, rect, alpha=0.80):
        x0, y0, x1, y1 = rect
        ov = Image.new("RGBA", (int(x1 - x0), int(y1 - y0)), (4, 6, 10, int(255 * alpha)))
        self.img.alpha_composite(ov, (int(x0), int(y0)))
        d = self.d
        d.line((x0, y0, x1, y0), fill=BRASS, width=2)
        d.rectangle((x0, y0 - 3, x0 + 8, y0 + 5), fill=BRASS)
        self.occupy(rect)


def star8(d, cx, cy, R, col, w=1, fill=None):
    for a0 in (0, 45):
        pts = [(cx + R * math.cos(math.radians(a0 + 90 * i)), cy + R * math.sin(math.radians(a0 + 90 * i))) for i in range(4)]
        d.polygon(pts, outline=col, width=w, fill=fill)


# ------------------------------------------------------------------ geometri
def rasterize_pil(geom, F, step=1.0):
    """Shapely (Multi)Polygon -> bool maske (PIL ile hızlı)."""
    w, h = int(math.ceil(F.W / step)), int(math.ceil(F.H / step))
    S = 2
    im = Image.new("L", (w * S, h * S), 0)
    d = ImageDraw.Draw(im)
    polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    for p in polys:
        if p.is_empty or p.geom_type != "Polygon":
            continue
        xs, ys = F.xy_to_px(*np.asarray(p.exterior.coords).T[:2])
        d.polygon(list(zip(xs / step * S, ys / step * S)), fill=255)
        for ring in p.interiors:
            xs, ys = F.xy_to_px(*np.asarray(ring.coords).T[:2])
            d.polygon(list(zip(xs / step * S, ys / step * S)), fill=0)
    im = im.resize((w, h), Image.BILINEAR)
    return np.asarray(im) > 127


def build_masks(F):
    countries = R.ne_layer("countries")
    land = shapely.make_valid(gpd.GeoSeries([shapely.union_all(countries.geometry.values)], crs="EPSG:4326")
                              .clip((8, 30, 38, 52)).to_crs(E.CRS).iloc[0])
    region = shapely.make_valid(R.data_region(countries))
    by = {r["ADM0_A3"]: r.geometry for _, r in countries.iterrows()}
    return countries, land, region, by


def ottoman_mask(F, region, by, clusters, step=2.0):
    """1876 Osmanlı idaresindeki alan (data_region içinde) — bool maske (step çözünürlüğünde)."""
    reg = rasterize_pil(region, F, step)
    fr_path = os.path.join(HERE, "data", "frontier_1876.json")
    to_g = lambda geom: gpd.GeoSeries([geom], crs="EPSG:4326").to_crs(E.CRS).iloc[0]
    hrv = rasterize_pil(to_g(by["HRV"]), F, step)
    # kıyı rasterizasyon farklarını kapat (Bosna'ya taşmadan)
    bih = rasterize_pil(to_g(by["BIH"]), F, step)
    hrv = binary_dilation(hrv, iterations=2) & ~bih
    grc = by["GRC"]
    gparts = list(grc.geoms) if hasattr(grc, "geoms") else [grc]
    gr_isl = [g for g in gparts if g.representative_point().y < 39.3 and g.representative_point().x < 25.0
              and g.area < 2.0]
    gr_isl += [g for g in gparts if g.representative_point().x < 20.4 and g.representative_point().y < 39.95]
    isl = rasterize_pil(to_g(shapely.union_all(gr_isl)), F, step) if gr_isl else np.zeros_like(reg)
    non = hrv | isl
    lines = []
    if os.path.exists(fr_path):
        fr = json.load(open(fr_path, encoding="utf-8"))
        h, w = reg.shape
        bar_im = Image.new("L", (w, h), 0)
        bd = ImageDraw.Draw(bar_im)
        for ln in fr["lines"]:
            co = np.asarray(ln["coords"], float)
            if len(co) < 2:
                continue
            xs, ys = F.ll_to_px(co[:, 0], co[:, 1])
            xs, ys = np.asarray(xs) / step, np.asarray(ys) / step
            # uçları ~8 km uzat (kıyıya/bölge kenarına değmeyen boşlukları kapat)
            ext = 8000 / (F.mpp * step)
            def _tip(i0, i1):
                vx, vy = xs[i0] - xs[i1], ys[i0] - ys[i1]
                L = math.hypot(vx, vy) or 1
                return xs[i0] + vx / L * ext, ys[i0] + vy / L * ext
            k_ = min(4, len(xs) - 1)
            p0, p1 = _tip(0, k_), _tip(-1, -1 - k_)
            pts = [p0] + list(zip(xs, ys)) + [p1]
            bd.line(pts, fill=255, width=3)
            lines.append(ln)
        barrier = np.asarray(bar_im) > 0
        lab, n = nd_label(reg & ~barrier)
        # Sırbistan: kendi sınır çizgisi + Sava/Tuna (bölge kenarı) ile kapalı bileşen
        bad = set()
        for lo, la in ((20.92, 44.01), (20.46, 44.75), (21.9, 43.9), (19.9, 44.27)):
            px, py = F.ll_to_px(lo, la)
            i, j = int(py / step), int(px / step)
            if lab[i, j] > 0:
                bad.add(lab[i, j])
        serb = np.isin(lab, list(bad))
        if serb.mean() > 0.2 * reg.mean():
            log("  uyarı: Sırbistan bileşeni sızdırıyor")
            serb[:] = False
        serb |= barrier & binary_dilation(serb, iterations=3) & reg
        polys = []
        byname = {ln["name"]: np.asarray(ln["coords"], float) for ln in fr["lines"]}
        mne = next((v for k_, v in byname.items() if "Karadağ" in k_), None)
        if mne is not None:
            close = [(18.93, 42.25), (18.84, 42.33), (18.78, 42.40), (18.70, 42.45), (18.60, 42.52)]
            ring = list(map(tuple, mne)) + close
            pg = shapely.make_valid(shapely.Polygon(ring))
            polys.append(pg)
        grc = next((v for k_, v in byname.items() if "Yunanistan" in k_), None)
        if grc is not None:
            w_ = [(19.0, 38.80), (20.70, 38.88), (20.80, 38.93), (21.05, 38.99)]
            e_ = [(23.25, 39.10), (24.75, 39.10), (24.75, 37.0), (19.0, 37.0)]
            ring = w_ + list(map(tuple, grc)) + e_
            polys.append(shapely.make_valid(shapely.Polygon(ring)))
        extra = np.zeros_like(reg)
        if polys:
            extra = rasterize_pil(to_g(shapely.union_all(polys)), F, step)
        # Boka Kotorska (Avusturya): bugünkü Karadağ kıyısının Karadağ prensliği dışında kalan batı ucu
        boka = shapely.Polygon([(18.43, 42.40), (18.58, 42.52), (18.70, 42.45), (18.78, 42.40), (18.84, 42.33),
                                (18.93, 42.25), (19.02, 42.17), (18.95, 42.10), (18.40, 42.35)])
        extra |= rasterize_pil(to_g(boka), F, step)
        nonseed = serb | extra
        non |= nonseed
        ott = reg & ~non
        frac_out = (reg & ~ott).mean() / max(reg.mean(), 1e-9)
        log(f"1876 sınırı: {len(lines)} çizgi, Osmanlı dışı oran {frac_out:.2f}")
        # mantık testi: Sırbistan çekirdeği Osmanlı dışı, Niş/Sofya Osmanlı içi olmalı
        ok = True
        for lo, la, want in ((20.92, 44.01, False), (21.9, 43.32, True), (23.32, 42.7, True), (22.42, 39.64, True), (22.43, 38.9, False)):
            px, py = F.ll_to_px(lo, la)
            v = ott[int(py / step), int(px / step)]
            if bool(v) != want:
                ok = False
                log(f"  uyarı: ({lo},{la}) beklenen {'içeride' if want else 'dışarıda'}")
        if ok:
            return ott, lines, non
        log("  sınır çizgisi tutarsız -> küme tabanlı yedek kullanılıyor")
    # yedek: kümelerin devlet etiketine göre en yakın-küme (Voronoi) bölmesi
    NON = {"Sırbistan", "Karadağ", "Avusturya-Macaristan", "Yunanistan"}
    xs, ys = F.ll_to_px([c["lon"] for c in clusters], [c["lat"] for c in clusters])
    tree = cKDTree(np.c_[np.asarray(xs) / step, np.asarray(ys) / step])
    ii, jj = np.nonzero(reg)
    _, idx = tree.query(np.c_[jj + 0.5, ii + 0.5])
    isnon = np.array([c.get("vilayet") in NON for c in clusters])
    m = np.zeros(reg.shape, np.float32)
    m[ii, jj] = isnon[idx]
    m = gaussian_filter(m, 3.0) > 0.5
    ott = reg & ~(m | non)
    return ott, [], (m | non) & reg


# ------------------------------------------------------------------ veri
def load_data():
    paths = sorted(p for p in glob.glob(os.path.join(HERE, "data", "*.json")) if "frontier" not in p)
    return R.load_clusters(paths)


def group_people(cl):
    P = np.array([E.cluster_population(c) for c in cl])
    S = np.array([[c[k] for k in E.CATS] for c in cl], float)
    S = S / S.sum(1, keepdims=True)
    return P[:, None] * S  # kişi (n, 3)


def largest_remainder(vals, total=100.0, nd=1):
    vals = np.asarray(vals, float)
    scale = 10 ** nd
    raw = vals / vals.sum() * total * scale
    fl = np.floor(raw)
    rem = int(round(total * scale - fl.sum()))
    order = np.argsort(-(raw - fl))
    fl[order[:rem]] += 1
    return fl / scale


REC_YEAR = {"Tuna (Niş hariç)": "1875", "Edirne": "1876", "Bosna": "1870", "Hersek": "1870"}


def stats(cl, in_ott):
    """Vilayet satırları (model, kişi; İstanbul hariç; 1876 sınırı içi)."""
    G = group_people(cl)
    vil = np.array([c.get("vilayet", "") for c in cl])
    san = np.array([(c.get("sancak") or "") for c in cl])
    base = in_ott & (vil != "İstanbul")

    def row(mask):
        g = G[mask].sum(0)
        return g, largest_remainder(g)

    rows = []
    rows.append(("TÜM RUMELİ", *row(base), None))
    kos = base & ((vil == "Prizren") | ((vil == "Manastır") & np.char.startswith(san.astype(str), "Prizren")))
    defs = [
        ("Tuna (Niş hariç)", base & (vil == "Tuna") & ~np.char.startswith(san.astype(str), "Niş"), RECORDS["TUNA_1875"]["muslim_pct"]),
        ("Edirne", base & (vil == "Edirne"), RECORDS["EDIRNE_1293"]["muslim_pct"]),
        ("Bosna", base & (vil == "Bosna"), RECORDS["BOSNA_1287"]["bosna_pct"]),
        ("Hersek", base & (vil == "Hersek"), RECORDS["BOSNA_1287"]["hersek_pct"]),
        ("Selanik", base & (vil == "Selanik"), None),
        ("Manastır (diğer)", base & (vil == "Manastır") & ~kos, None),
        ("Prizren–Üsküp", kos, None),
        ("Yanya", base & (vil == "Yanya"), None),
        ("İşkodra", base & (vil == "İşkodra"), None),
    ]
    sub = []
    for name, m, rec in defs:
        if m.sum() == 0:
            continue
        g, p = row(m)
        sub.append((name, g, p, rec))
    sub.sort(key=lambda r: -(r[2][0] + r[2][1]))
    return rows + sub


# ------------------------------------------------------------------ çizim: altlık
def base_image(F, elev, landm, regm, ottm):
    hs, slope, flat = E.multi_hillshade(elev, F.mpp)
    shade = gaussian_filter(np.clip(hs / flat, 0, 1.6) / 1.6, 0.5)
    d_sea = distance_transform_edt(~landm) * F.mpp / 1000
    coast = np.exp(-d_sea / 16.0)[..., None]
    img = hf(INK) * (1 - coast) + hf("#0C1624") * coast
    lo, hi = hf("#080B11"), hf("#181E29")
    img = np.where(landm[..., None], lo + (hi - lo) * shade[..., None] ** 1.2, img)
    lo, hi = hf("#0E141E"), hf("#27303F")
    img = np.where(ottm[..., None], lo + (hi - lo) * shade[..., None] ** 1.1, img)
    # Osmanlı dışı veri alanı (Sırbistan vb.) arada bir ton
    mid = regm & ~ottm
    lo, hi = hf("#0B1018"), hf("#1E2532")
    img = np.where(mid[..., None], lo + (hi - lo) * shade[..., None] ** 1.15, img)
    return img


def vfade():
    yy = np.arange(H, dtype=np.float32)[:, None]
    return (np.clip((yy - 140) / 480, 0, 1) * np.clip((2320 - yy) / 360, 0, 1)) ** 0.8


def draw_rivers(F, regm, fade, under=True):
    riv = []
    for f in ("ne_10m_rivers_lake_centerlines.shp", "ne_10m_rivers_europe.shp"):
        p = os.path.join(R.CACHE, f)
        if os.path.exists(p):
            riv.append(gpd.read_file(p, bbox=(13, 36, 32, 48)).to_crs(E.CRS))
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    MAJ = {"Sava", "Morava", "Vardar", "Axios", "Evros", "Maritsa", "Meriç", "Strymnas", "Strymónas", "Struma",
           "Drina", "Iskar", "Haliacmon", "Tundzha", "Bosna", "Vrbas", "Neretva", "Drin", "Ergene", "Mesta", "Nestos",
           "Yantra", "Timok", "Ibar", "Južna Morava", "Zapadna Morava", "Velika Morava", "Una", "Osam", "Vit",
           "Strimonas", "Aoos", "Pineios", "Kamchiya"}
    for g in riv:
        for _, r in g.iterrows():
            nm = str(r.get("name") or "")
            if nm in ("Danube", "Bratul Chillia", "Bratul Sfântu Gheorghe", "Bratul Sulina", "Borcea") or r["scalerank"] <= 2:
                w = 4.0 if under else 2.6
            elif nm in MAJ or r["scalerank"] <= 8:
                w = 2.2 if under else 1.4
            else:
                w = 1.2 if under else 0.9
            col = hx("#2B4560") if under else hx("#05080D", int(255 * 0.85))
            gs = r.geometry.geoms if hasattr(r.geometry, "geoms") else [r.geometry]
            for gg in gs:
                xs, ys = F.xy_to_px(*np.asarray(gg.coords).T[:2])
                d.line(list(zip(xs * S, ys * S)), fill=col, width=max(1, int(round(w * S))), joint="curve")
    lay = lay.resize((W, H), Image.LANCZOS)
    a = np.asarray(lay, np.float32).copy()
    if under:
        m = np.where(regm, 1.0, 0.25) * np.clip(fade[:, 0], 0, 1)[:, None] ** 1.5
    else:
        m = regm.astype(np.float32) * np.clip(fade[:, 0], 0, 1)[:, None] ** 1.5
    a[..., 3] *= m
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def dotted_borders(F, fade):
    b = R.ne_layer("borders").to_crs(E.CRS)
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = hx("#8C98AC", int(255 * 0.35))
    for g in b.geometry:
        gs = g.geoms if hasattr(g, "geoms") else [g]
        for gg in gs:
            L = gg.length / F.mpp
            n = int(L / 7)
            for t in np.linspace(0, 1, max(n, 2)):
                p = gg.interpolate(t, normalized=True)
                x, y = F.xy_to_px(p.x, p.y)
                d.ellipse((x * S - 1.5, y * S - 1.5, x * S + 1.5, y * S + 1.5), fill=col)
    lay = lay.resize((W, H), Image.LANCZOS)
    a = np.asarray(lay, np.float32).copy()
    a[..., 3] *= np.clip(fade[:, 0], 0, 1)[:, None]
    return Image.fromarray(a.astype(np.uint8), "RGBA")


# ------------------------------------------------------------------ çizim: noktalar
def render_dots(img_f, x, y, k, inside, seed=1876):
    """Çekirdek noktalar + eşit kazançlı bloom. img_f: (H,W,3) float [0,1]."""
    S = 3
    r = 1.6 * S
    rng = np.random.default_rng(seed)
    order = rng.permutation(x.size)
    core = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    dc = ImageDraw.Draw(core)
    masks = [Image.new("L", (W * S, H * S), 0) for _ in range(3)]
    dms = [ImageDraw.Draw(m) for m in masks]
    cols = {g: np.array(hx(COL[g])[:3], float) for g in range(3)}
    des = {}
    for g in range(3):
        c = cols[g]
        lum = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        des[g] = tuple(int(v) for v in (c * 0.6 + lum * 0.4))
    for i in order:
        yy = y[i]
        fy = 1.0 if yy <= 1960 else max(0.0, min(1.0, (2320 - yy) / 360))
        if fy <= 0:
            continue
        g = int(k[i])
        xa, ya = x[i] * S, yy * S
        bb = (xa - r, ya - r, xa + r, ya + r)
        if inside[i]:
            dc.ellipse(bb, fill=tuple(int(v) for v in cols[g]) + (int(255 * 0.96 * fy),))
            dms[g].ellipse(bb, fill=int(255 * fy))
        else:
            dc.ellipse(bb, fill=des[g] + (int(255 * 0.30 * fy),))
    lin = img_f ** 2.2
    for g in range(3):
        m = np.asarray(masks[g].resize((W, H), Image.LANCZOS), np.float32) / 255
        b = 0.9 * gaussian_filter(m, 2.2) + 0.55 * gaussian_filter(m, 7) + 0.30 * gaussian_filter(m, 22)
        lin = lin + 1.3 * 0.85 * b[..., None] * (hf(COL[g]) ** 2.2)[None, None, :]
    out = (1 - np.exp(-1.15 * lin)) ** (1 / 2.2)
    res = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8)).convert("RGBA")
    res.alpha_composite(core.resize((W, H), Image.LANCZOS))
    return res


def frontier_layer(ott1, nonott_land1):
    """Çift çizgi (cetvel): ott ile Osmanlı-dışı kara arasındaki sınır."""
    dA = distance_transform_edt(~ott1)          # Osmanlı alanına uzaklık
    dB = distance_transform_edt(~nonott_land1)  # Osmanlı dışı karaya uzaklık
    # sınıra uzaklık (yaklaşık): iki tarafta da bant
    dist = np.where(ott1, dB, np.where(nonott_land1, dA, 99.0))
    outer = np.clip(2.2 + 0.5 - dist, 0, 1)
    inner = np.clip(0.7 + 0.5 - dist, 0, 1)
    glow = gaussian_filter(outer, 4) * 0.25
    lay = np.zeros((H, W, 4), np.float32)
    iv = np.array(FRONT[:3], np.float32)
    a_out = np.clip(outer * 0.9 + glow, 0, 1)
    lay[..., :3] = iv
    lay[..., 3] = a_out
    # çekirdek koyu çizgi
    core = inner
    lay[..., :3] = lay[..., :3] * (1 - core[..., None]) + np.array([5, 8, 13], np.float32) * core[..., None]
    lay[..., 3] = np.maximum(lay[..., 3], core)
    return Image.fromarray(np.clip(lay * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA"), dist


# ------------------------------------------------------------------ süsler
def frame_ornament(cv):
    d = cv.d
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle((0, 0, W, 44), fill=hx("#05080D"))
    bd.rectangle((0, H - 44, W, H), fill=hx("#05080D"))
    bd.rectangle((0, 0, 44, H), fill=hx("#05080D"))
    bd.rectangle((W - 44, 0, W, H), fill=hx("#05080D"))
    cv.img.alpha_composite(band)
    d = cv.d
    d.rectangle((20, 20, W - 20, H - 20), outline=BRASS[:3] + (230,), width=2)
    d.rectangle((42, 42, W - 42, H - 42), outline=BRASS[:3] + (150,), width=1)
    # zencerek bandı (inset 31)
    for (xa, ya, xb, yb) in ((127, 31, W - 127, 31), (127, H - 31, W - 127, H - 31), (31, 127, 31, H - 127), (W - 31, 127, W - 31, H - 127)):
        L = math.hypot(xb - xa, yb - ya)
        n = int(L / 24)
        for i in range(n + 1):
            t = i / n
            x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
            if i % 2 == 0:
                star8(d, x, y, 6.4, BRASS[:3] + (140,), 1)
            else:
                d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=BRASS[:3] + (160,))
    # köşebent
    for (cx, cy) in ((31, 31), (W - 31, 31), (31, H - 31), (W - 31, H - 31)):
        Rr = 84
        S = 3
        size = int(2 * Rr * 1.2)
        lay = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        o = size * S / 2

        def ring(rs):
            return [(o + rs * S * (1 + 0.07 * math.cos(10 * th)) * math.cos(th),
                     o + rs * S * (1 + 0.07 * math.cos(10 * th)) * math.sin(th)) for th in np.linspace(0, 2 * math.pi, 400)]
        ld.polygon(ring(Rr), fill=hx("#05080D"), outline=BRASS[:3] + (190,), width=int(1.5 * S))
        mask = Image.new("L", lay.size, 0)
        ImageDraw.Draw(mask).polygon(ring(Rr * 0.72), fill=255)
        lat = Image.new("RGBA", lay.size, hx("#05080D"))
        latd = ImageDraw.Draw(lat)
        for gx in np.arange(0, size * S, 18 * S):
            for gy in np.arange(0, size * S, 18 * S):
                star8(latd, gx, gy, 4 * S, BRASS[:3] + (72,), S)
        lay.paste(lat, (0, 0), mask)
        ld.polygon(ring(Rr * 0.72), outline=BRASS[:3] + (115,), width=S)
        star8(ld, o, o, 9 * S, BRASS_L, S)
        lay = lay.resize((size, size), Image.LANCZOS)
        cv.img.alpha_composite(lay, (int(cx - size / 2), int(cy - size / 2)))


def compass_rose(cv, cx, cy, R, rot_deg):
    S = 3
    size = int(R * 3.2)
    lay = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    o = size * S / 2
    rot = math.radians(rot_deg)

    def kite(ang, length, half, light, dark):
        a = ang + rot
        tip = (o + length * S * math.sin(a), o - length * S * math.cos(a))
        l = (o + half * S * math.sin(a - math.pi / 2), o - half * S * math.cos(a - math.pi / 2))
        r_ = (o + half * S * math.sin(a + math.pi / 2), o - half * S * math.cos(a + math.pi / 2))
        d.polygon([(o, o), l, tip], fill=light)
        d.polygon([(o, o), r_, tip], fill=dark)

    for i in range(8):
        kite(math.radians(22.5 + 45 * i), 0.6 * R, 0.11 * R, BRASS_L[:3] + (200,), BRASS_D[:3] + (220,))
    for i in range(8):
        kite(math.radians(45 * i), R if i % 2 == 0 else 0.82 * R, 0.15 * R, BRASS_L, BRASS_D)
    for rr in (0.30, 0.34):
        d.ellipse((o - rr * R * S, o - rr * R * S, o + rr * R * S, o + rr * R * S), outline=BRASS_L, width=S)
    star8(d, o, o, 0.12 * R * S, BRASS_L, S, fill=hx("#05080D"))
    lay = lay.resize((size, size), Image.LANCZOS)
    cv.img.alpha_composite(lay, (int(cx - size / 2), int(cy - size / 2)))
    names = ["Yıldız", "Poyraz", "Gündoğusu", "Keşişleme", "Kıble", "Lodos", "Günbatısı", "Karayel"]
    for i, n in enumerate(names):
        a = math.radians(45 * i) + rot
        sa, ca = math.sin(a), math.cos(a)
        rr = 1.12 * R
        x, y = cx + rr * sa, cy - rr * ca + 6
        anc = "l" if sa > 0.35 else "r" if sa < -0.35 else "c"
        if anc == "c":
            y += -8 if ca > 0 else 10
        cv.tracked((x, y), n, bar(16, "SemiBold"), 2, BRASS, anchor=anc)
    cv.occupy((cx - 1.45 * R, cy - 1.45 * R, cx + 1.45 * R, cy + 1.45 * R))


def lat_ticks(cv, F):
    d = cv.d
    for xe, side in ((44, "l"), (W - 44, "r")):
        ys = np.arange(600, 2150)
        lon_, lat_ = E.TO_LL.transform(F.x0 + xe * F.mpp + 0 * ys, F.y1 - ys * F.mpp)
        for yv, l0, l1 in zip(ys[1:], lat_[:-1], lat_[1:]):
            if math.floor(l0 * 2) != math.floor(l1 * 2):
                whole = math.floor(l0) != math.floor(l1)
                ln = 14 if whole else 7
                xa = xe if side == "l" else xe - ln
                if not cv.clear((xa - 4, yv - 12, xa + ln + 4, yv + 12)):
                    continue
                d.line((xa, yv, xa + ln, yv), fill=BRASS[:3] + (180,), width=2 if whole else 1)
                lr = (xe + 18, yv - 12, xe + 70, yv + 12) if side == "l" else (xe - 70, yv - 12, xe - 18, yv + 12)
                if whole and cv.clear(lr):
                    lab = f"{int(math.floor(l0))}°K"
                    d.text((xe + 22 if side == "l" else xe - 22, yv), lab, font=bar(17, "Medium"), fill=MUTE,
                           anchor="lm" if side == "l" else "rm")


# ------------------------------------------------------------------ yer adları
T1 = [("İstanbul", None, 28.97, 41.01), ("Edirne", None, 26.56, 41.68), ("Filibe", "Plovdiv", 24.75, 42.15),
      ("Sofya", "Sofia", 23.32, 42.70), ("Rusçuk", "Ruse", 25.97, 43.85), ("Selanik", "Thessaloniki", 22.94, 40.64),
      ("Manastır", "Bitola", 21.34, 41.03), ("Üsküp", "Skopje", 21.43, 42.00), ("Saraybosna", "Sarajevo", 18.41, 43.86),
      ("Yanya", "Ioannina", 20.85, 39.67), ("İşkodra", "Shkodër", 19.51, 42.07)]
T2 = [("Varna", None, 27.91, 43.21), ("Vidin", None, 22.88, 43.99), ("Tırnova", "V. Tarnovo", 25.63, 43.08),
      ("Tulça", "Tulcea", 28.80, 45.18), ("Şumnu", "Shumen", 26.93, 43.27), ("Niş", "Niš", 21.90, 43.32),
      ("Priştine", "Prishtinë", 21.16, 42.66), ("Prizren", None, 20.74, 42.21), ("Yenipazar", "Novi Pazar", 20.51, 43.14),
      ("Mostar", None, 17.81, 43.34), ("Banaluka", "Banja Luka", 17.19, 44.77), ("İslimye", "Sliven", 26.32, 42.68),
      ("Eski Zağra", "Stara Zagora", 25.63, 42.43), ("Gümülcine", "Komotini", 25.40, 41.12), ("Serez", "Serres", 23.55, 41.09),
      ("Kavala", None, 24.41, 40.94), ("Yenişehir", "Larisa", 22.42, 39.64), ("Görice", "Korçë", 20.78, 40.62),
      ("Elbasan", None, 20.08, 41.11), ("Kırcaali", "Kardzhali", 25.37, 41.65), ("Tekfurdağı", "Tekirdağ", 27.51, 40.98),
      ("Kırkkilise", "Kırklareli", 27.22, 41.73), ("Silistre", "Silistra", 27.26, 44.12), ("Plevne", "Pleven", 24.62, 43.42),
      ("Hezargrad", "Razgrad", 26.52, 43.53), ("Belgrad", None, 20.46, 44.82)]
T3 = [("Bihke", "Bihać", 15.87, 44.82), ("Çatalca", None, 28.46, 41.14), ("Lom", None, 23.23, 43.82),
      ("Köstence", None, 28.63, 44.17), ("Burgaz", None, 27.47, 42.50), ("Hasköy", None, 25.55, 41.93),
      ("Dedeağaç", None, 25.87, 40.85), ("Drama", None, 24.15, 41.15), ("Ohri", None, 20.80, 41.12),
      ("Berat", None, 19.95, 40.70), ("Tırhala", None, 21.77, 39.55), ("Kesriye", None, 21.27, 40.52),
      ("İştip", None, 22.20, 41.75), ("Kalkandelen", None, 20.97, 42.01), ("İpek", None, 20.29, 42.66),
      ("Yakova", None, 20.43, 42.38), ("Tuzla", None, 18.67, 44.54), ("İzvornik", None, 19.10, 44.41),
      ("Travnik", None, 17.67, 44.23), ("Lofça", None, 24.72, 43.14), ("Köstendil", None, 22.69, 42.28),
      ("Tatar Pazarcığı", None, 24.33, 42.19), ("Babadağ", None, 28.70, 44.90), ("Hacıoğlu Pazarcığı", None, 27.83, 43.57),
      ("Çetine", None, 18.92, 42.39), ("Podgoriçe", None, 19.26, 42.44), ("Avlonya", None, 19.49, 40.47),
      ("Draç", None, 19.45, 41.32), ("Gelibolu", None, 26.67, 40.41), ("Karaferye", None, 22.20, 40.52)]
DIMMED = {"Belgrad", "Çetine"}

STORY = [("DELİORMAN", 0, 26.72, 43.93), ("DOBRUCA", 0, 28.70, 44.50),
         ("DOĞU RODOPLAR", 0, 25.75, 41.40), ("KONYAR TÜRKLERİ", 0, 21.70, 40.30),
         ("POMAKLAR", 1, 24.3, 41.68), ("ARNAVUTLAR", 1, 20.34, 41.56), ("BOŞNAKLAR", 1, 18.05, 44.42)]
STORY_SUB = {"DOBRUCA": "Tatar ve Nogaylar", "KONYAR TÜRKLERİ": "Kayalar · Sarıgöl · Kozana"}
STATES = [("SIRBİSTAN PRENSLİĞİ", 21.0, 44.25), ("KARADAĞ PRENSLİĞİ", 19.0, 42.58),
          ("YUNANİSTAN KRALLIĞI", 22.2, 38.72), ("AVUSTURYA-MACARİSTAN", 17.0, 45.55)]
GHOST = [("TUNA", 25.0, 43.35), ("EDİRNE", 26.0, 42.0), ("SELANİK", 23.4, 40.95), ("MANASTIR", 21.4, 41.25),
         ("YANYA", 20.9, 39.4), ("İŞKODRA", 19.85, 41.75), ("BOSNA", 18.0, 44.25), ("HERSEK", 18.0, 43.2)]


def place_cities(cv, F, ottm1, tiers=None):
    d = cv.d
    tiers = tiers or [(T1, 1), (T2, 2), (T3, 3)]
    for lst, tier in tiers:
        for name, modern, lon, lat in lst:
            x, y = F.ll_to_px(lon, lat)
            x, y = float(x), float(y)
            if not (60 < x < W - 60 and 560 < y < 2150):
                continue
            dim = name in DIMMED
            fnt = bar(38, "SemiBold") if tier == 1 else bar(30, "SemiBold") if tier == 2 else bar(23, "Medium")
            col = IV if tier == 1 else hx("#E1DACA") if tier == 2 else hx("#C9C2B4")
            if dim:
                col = col[:3] + (150,)
            mod_f = bar(18 if tier == 1 else 16, "Medium") if (modern and tier <= 2) else None
            tw = fnt.getlength(name)
            th = fnt.size * 0.78
            mw = mod_f.getlength(modern) if mod_f else 0
            bw = max(tw, mw)
            bh = th + (mod_f.size + 2 if mod_f else 0)
            r = 7 if tier == 1 else 5 if tier == 2 else 3
            cands = [(x + r + 8, y + th / 2 - 2, "E"), (x - r - 8 - bw, y + th / 2 - 2, "W"),
                     (x + r + 4, y - r - 4, "NE"), (x - r - 4 - bw, y + r + th + 4, "SW"),
                     (x - bw / 2, y - r - 6 - (bh - th), "N"), (x - bw / 2, y + r + th + 4, "S"),
                     (x + r + 4, y + r + th + 4, "SE"), (x - r - 4 - bw, y - r - 4, "NW")]
            placed = False
            for lx, ly, tag in cands:
                rect = (lx, ly - th, lx + bw, ly - th + bh)
                if cv.free(rect, pad=3) and cv.free((x - r - 2, y - r - 2, x + r + 2, y + r + 2), pad=0):
                    placed = True
                    break
            if not placed:
                continue
            # sembol: elmas / kare (daire değil — veri noktasıyla karışmasın)
            if tier == 1:
                d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=IV, outline=hx("#05080D"), width=2)
            else:
                d.rectangle((x - r / 2 - 1, y - r / 2 - 1, x + r / 2 + 1, y + r / 2 + 1), fill=col, outline=hx("#05080D"))
            cv.halo((lx, ly), name, fnt, col, anchor="ls", rad=4)
            if mod_f:
                cv.halo((lx, ly + mod_f.size + 1), modern, mod_f, MUTE[:3] + ((150,) if dim else (255,)), anchor="ls", rad=3)
            cv.occupy(rect)
            cv.occupy((x - r - 2, y - r - 2, x + r + 2, y + r + 2))


# ------------------------------------------------------------------ ana akış
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imza", default="")
    ap.add_argument("--out", default=os.path.join(HERE, "cikti", "rumeli_1876"))
    ap.add_argument("--ppd", type=int, default=250, help="nokta başına kişi")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)

    F = E.Frame(W, H, 1210, center_lonlat=(22.6, 42.4), shift_km=(30, -40))
    elev = E.dem_on_frame(F)
    countries, land, region, by = build_masks(F)
    landm = rasterize_pil(land, F, 1.0)
    regm = rasterize_pil(region, F, 1.0)
    regm2 = rasterize_pil(region, F, 2.0)
    elev2 = elev[::2, ::2][:regm2.shape[0], :regm2.shape[1]]
    log("maskeler")

    cl = load_data()
    log(f"{len(cl)} küme, {sum(E.cluster_population(c) for c in cl):,.0f} kişi")
    cl = C.auto_calibrate(cl, F, regm2, elev2)
    os.makedirs(os.path.join(HERE, "data_cal"), exist_ok=True)
    json.dump([{k: v for k, v in c.items() if k != "shares"} for c in cl],
              open(os.path.join(HERE, "data_cal", "clusters_calibrated.json"), "w", encoding="utf-8"), ensure_ascii=False)

    ott2, flines, non2 = ottoman_mask(F, region, by, cl, 2.0)
    ott1 = np.repeat(np.repeat(ott2, 2, 0), 2, 1)[:H, :W] & regm
    log("1876 maskesi")

    x, y, k = E.make_dots(cl, F, regm2, elev2, people_per_dot=a.ppd, seed=1876)
    xi, yi = np.clip(x.astype(int), 0, W - 1), np.clip(y.astype(int), 0, H - 1)
    inside = ott1[yi, xi]
    log(f"{x.size} nokta ({inside.sum()} Osmanlı içi)")
    C.compare_dots(F, x, y, k)

    # kümelerin 1876 içi bayrağı
    cxs, cys = F.ll_to_px([c["lon"] for c in cl], [c["lat"] for c in cl])
    cxi = np.clip(np.asarray(cxs).astype(int), 0, W - 1)
    cyi = np.clip(np.asarray(cys).astype(int), 0, H - 1)
    in_ott = np.array([c.get("vilayet") not in ("Sırbistan", "Karadağ", "Avusturya-Macaristan", "Yunanistan") for c in cl])
    ROWS = stats(cl, in_ott)
    for n, g, p, rec in ROWS:
        log(f"  {n:18s} {fmt_int(g.sum()):>11s}  T {p[0]:5.1f}  M {p[1]:5.1f}  H {p[2]:5.1f}  Müs {p[0] + p[1]:5.1f}" + (f"  kayıt {rec}" if rec else ""))

    # ---- altlık
    fade = vfade()
    basef = base_image(F, elev, landm, regm, ott1)
    basef = basef * (0.22 + 0.78 * fade[..., None])
    base = Image.fromarray(np.clip(basef * 255, 0, 255).astype(np.uint8)).convert("RGBA")
    cvb = Canvas(base)
    # hayalet vilayet adları (noktaların altında)
    base.alpha_composite(draw_rivers(F, regm, fade, under=True))
    base.alpha_composite(dotted_borders(F, fade))
    log("altlık")

    img = render_dots(np.asarray(base.convert("RGB"), np.float32) / 255, x, y, k, inside)
    log("noktalar")
    img.alpha_composite(draw_rivers(F, regm, fade, under=False))
    # Osmanlı dışı kara: yalnız 1876'nın yabancı devletleri (Anadolu ve Osmanlı adaları değil)
    to_g = lambda geom: gpd.GeoSeries([geom], crs="EPSG:4326").to_crs(E.CRS).iloc[0]
    outside = shapely.union_all([by[a3] for a3 in ("ROU", "HUN", "SVN", "HRV", "SRB", "MNE", "AUT") if a3 in by])
    foreign = rasterize_pil(to_g(outside), F, 1.0) & ~regm
    non1 = np.repeat(np.repeat(non2, 2, 0), 2, 1)[:H, :W]
    foreign |= (regm & ~ott1 & non1)
    foreign = binary_opening(foreign, iterations=2) & landm & ~ott1
    fl, fdist = frontier_layer(ott1, foreign)
    fa = np.asarray(fl, np.float32).copy()
    fa[..., 3] *= np.clip(fade[:, 0], 0, 1)[:, None] ** 1.2
    img.alpha_composite(Image.fromarray(fa.astype(np.uint8), "RGBA"))
    log("sınır")

    cv = Canvas(img)
    d = cv.d

    # ---- engeller (paneller vb.) önce kaydedilir
    KAYIT = (1060, 612, 1736, 926)
    LENS_C, LENS_R = (1958, 1262), 112
    NASIL = (60, 1690, 520, 2150)
    SONRA = (1704, 1652, 2104, 2084)
    STRIP = (44, 2160, 2116, 2656)
    ROSE = (330, 1520, 80)
    for r_ in (KAYIT, NASIL, SONRA, STRIP, (0, 0, W, 560), (ROSE[0] - 1.5 * ROSE[2], ROSE[1] - 1.5 * ROSE[2], ROSE[0] + 1.5 * ROSE[2], ROSE[1] + 1.5 * ROSE[2])):
        cv.occupy(r_)
    cv.occupy((LENS_C[0] - LENS_R - 12, LENS_C[1] - LENS_R - 40, LENS_C[0] + LENS_R + 12, LENS_C[1] + LENS_R + 60))

    # ---- büyüteç (aynı noktalar)
    src_c = F.ll_to_px(26.72, 43.74)
    src_c = (float(src_c[0]), float(src_c[1]))
    Z, sr = 3.0, LENS_R / 3.0
    S3 = 3
    crop = img.crop((int(src_c[0] - sr), int(src_c[1] - sr), int(src_c[0] + sr), int(src_c[1] + sr)))
    lens = Image.fromarray(np.clip(basef * 255, 0, 255).astype(np.uint8)).crop(
        (int(src_c[0] - sr), int(src_c[1] - sr), int(src_c[0] + sr), int(src_c[1] + sr))).resize(
        (2 * LENS_R * S3, 2 * LENS_R * S3), Image.BICUBIC).convert("RGBA")
    ld = ImageDraw.Draw(lens)
    sel = np.hypot(x - src_c[0], y - src_c[1]) < sr + 3
    glow_l = Image.new("RGBA", lens.size, (0, 0, 0, 0))
    gld = ImageDraw.Draw(glow_l)
    rr = 3.6 * S3
    for i in np.nonzero(sel)[0]:
        px_ = ((x[i] - src_c[0]) * Z + LENS_R) * S3
        py_ = ((y[i] - src_c[1]) * Z + LENS_R) * S3
        c_ = hx(COL[int(k[i])])
        gld.ellipse((px_ - rr * 2.2, py_ - rr * 2.2, px_ + rr * 2.2, py_ + rr * 2.2), fill=c_[:3] + (70,))
        ld.ellipse((px_ - rr, py_ - rr, px_ + rr, py_ + rr), fill=c_)
    glow_l = glow_l.filter(ImageFilter.GaussianBlur(2 * S3))
    lens2 = Image.alpha_composite(lens, glow_l)
    lens2.alpha_composite(Image.fromarray(np.asarray(lens)[..., :4]).convert("RGBA"), (0, 0)) if False else None
    ImageDraw.Draw(lens2)
    for i in np.nonzero(sel)[0]:
        px_ = ((x[i] - src_c[0]) * Z + LENS_R) * S3
        py_ = ((y[i] - src_c[1]) * Z + LENS_R) * S3
        ImageDraw.Draw(lens2).ellipse((px_ - rr, py_ - rr, px_ + rr, py_ + rr), fill=hx(COL[int(k[i])]))
    lens2 = lens2.resize((2 * LENS_R, 2 * LENS_R), Image.LANCZOS)
    mk = Image.new("L", (2 * LENS_R * 4, 2 * LENS_R * 4), 0)
    ImageDraw.Draw(mk).ellipse((0, 0, 2 * LENS_R * 4 - 1, 2 * LENS_R * 4 - 1), fill=255)
    mk = mk.resize((2 * LENS_R, 2 * LENS_R), Image.LANCZOS)
    # bağlantı çizgisi
    vx, vy = LENS_C[0] - src_c[0], LENS_C[1] - src_c[1]
    L = math.hypot(vx, vy)
    ux, uy = vx / L, vy / L
    d = cv.d
    d.line((src_c[0] + ux * (sr + 2), src_c[1] + uy * (sr + 2), LENS_C[0] - ux * (LENS_R + 3), LENS_C[1] - uy * (LENS_R + 3)),
           fill=IV[:3] + (128,), width=2)
    d.ellipse((src_c[0] - sr, src_c[1] - sr, src_c[0] + sr, src_c[1] + sr), outline=IV[:3] + (205,), width=2)
    cv.img.paste(lens2, (LENS_C[0] - LENS_R, LENS_C[1] - LENS_R), mk)
    d = cv.d
    d.ellipse((LENS_C[0] - LENS_R - 1, LENS_C[1] - LENS_R - 1, LENS_C[0] + LENS_R + 1, LENS_C[1] + LENS_R + 1), outline=IV, width=3)
    d.ellipse((LENS_C[0] - LENS_R - 9, LENS_C[1] - LENS_R - 9, LENS_C[0] + LENS_R + 9, LENS_C[1] + LENS_R + 9), outline=BRASS, width=1)
    cv.tracked((LENS_C[0], LENS_C[1] + LENS_R + 34), "BÜYÜTEÇ ×3", bar(22, "SemiBold"), 3, IV, anchor="c")
    cv.tracked((LENS_C[0], LENS_C[1] + LENS_R + 60), "DELİORMAN", bar(22, "SemiBold"), 3, TINT[0], anchor="c")
    cv.occupy((src_c[0] - sr - 4, src_c[1] - sr - 4, src_c[0] + sr + 4, src_c[1] + sr + 4))

    # ---- etiketler: önce T1 ve kilit T2 şehirler, sonra hikâye, devletler, denizler, diğer şehirler
    KEY2 = {"Silistre", "Hezargrad", "Kırkkilise", "Tekfurdağı", "Şumnu", "Varna"}
    place_cities(cv, F, ott1, [(T1, 1), ([c_ for c_ in T2 if c_[0] in KEY2], 2)])
    # Selanik notu (Ege'de) — yer ayır
    nx_, ny_ = F.ll_to_px(23.27, 39.82)
    nx_, ny_ = float(nx_), float(ny_)
    SELNOTE = (nx_ - 4, ny_ - 32, nx_ + 262, ny_ + 14)
    cv.occupy(SELNOTE)
    for t, g, lo, la in STORY:
        px, py = F.ll_to_px(lo, la)
        px, py = float(px), float(py)
        fnt = bar(30, "SemiBold")
        w = cv.tracked_w(t, fnt, 3)
        rect = (px - w / 2, py - 28, px + w / 2, py + 6)
        done = False
        for dy in (0, -36, 36, -72, 72, -108, 108):
            for dxx in ((0, 70, 120, 170, -70) if t == "DELİORMAN" else (0, -60, 60, -120, 120)):
                rr_ = (rect[0] + dxx, rect[1] + dy, rect[2] + dxx, rect[3] + dy)
                sub_ = STORY_SUB.get(t)
                rr2 = (rr_[0], rr_[1], rr_[2], rr_[3] + (24 if sub_ else 0))
                if cv.free(rr2, 2):
                    cv.halo((px + dxx, py + dy), t, fnt, TINT[g], anchor="ms", rad=5, track=3)
                    if sub_:
                        cv.halo((px + dxx, py + dy + 24), sub_, bar(19, "SemiBold"), TINT[g], anchor="ms", rad=4, track=2)
                    cv.occupy(rr2)
                    done = True
                    break
            if done:
                break
        if not done:
            log("  hikâye etiketi yerleşmedi:", t)
    for t, lo, la in STATES:
        px, py = F.ll_to_px(lo, la)
        fnt = bar(24, "SemiBold")
        w = cv.tracked_w(t, fnt, 7)
        rect = (float(px) - w / 2, float(py) - 22, float(px) + w / 2, float(py) + 6)
        cv.halo((float(px), float(py)), t, fnt, hx("#A0A8B8", 160), anchor="ms", rad=4, track=7)
        if t.startswith("SIRBİSTAN"):
            cv.halo((float(px), float(py) + 24), "Osmanlı’ya bağlı özerk prenslik", bar(16, "Medium"), hx("#A0A8B8", 150), anchor="ms", rad=3)
            rect = (rect[0], rect[1], rect[2], rect[3] + 24)
        cv.occupy(rect)
    cv.tracked((965, 730), "ROMANYA", bar(24, "SemiBold"), 7, hx("#A0A8B8", 160), anchor="c")
    cv.tracked((965, 760), "PRENSLİĞİ", bar(24, "SemiBold"), 7, hx("#A0A8B8", 160), anchor="c")
    ImageDraw.Draw(cv.img).text((965, 786), "Osmanlı’ya bağlı özerk prenslik", font=bar(16, "Medium"), fill=hx("#A0A8B8", 150), anchor="ms")
    cv.occupy((820, 700, 1110, 796))
    adl = Image.new("RGBA", (640, 70), (0, 0, 0, 0))
    Canvas(adl).tracked((320, 48), "ADRİYATİK DENİZİ", bod(26, 600, 11), 10, hx("#5D7391"), anchor="c")
    adl = adl.rotate(-36, expand=True, resample=Image.BICUBIC)
    apx, apy = F.ll_to_px(17.6, 42.35)
    cv.img.alpha_composite(adl, (int(apx) - adl.width // 2, int(apy) - adl.height // 2))
    for t, lo, la, sz in (("ADALAR DENİZİ", 24.9, 39.45, 30), ("MARMARA", 28.15, 40.62, 22)):
        px, py = F.ll_to_px(lo, la)
        cv.tracked((float(px), float(py)), t, bod(sz, 500), 12 if sz > 22 else 6, hx("#5D7391"), anchor="c")
        w = cv.tracked_w(t, bod(sz, 500), 12)
        cv.occupy((float(px) - w / 2, float(py) - sz, float(px) + w / 2, float(py) + 6))
    # KARADENİZ dikey
    kl = Image.new("RGBA", (500, 60), (0, 0, 0, 0))
    Canvas(kl).tracked((250, 44), "KARADENİZ", bod(30, 500), 14, hx("#5D7391"), anchor="c")
    kl = kl.rotate(90, expand=True, resample=Image.BICUBIC)
    cv.img.alpha_composite(kl, (2066 - kl.width // 2, 950 - kl.height // 2))
    cv.occupy((2036, 700, 2096, 1200))
    # TUNA nehir adı
    px, py = F.ll_to_px(24.2, 43.78)
    cv.halo((float(px), float(py)), "TUNA", bod(30, 500), hx("#6E8DB0", 220), anchor="ms", rad=3, track=14)
    # sınır etiketleri
    band = (fdist < 1.2) & landm
    for lo, la in ((20.75, 43.36), (21.7, 39.05)):
        hx_, hy_ = F.ll_to_px(lo, la)
        hx_, hy_ = float(hx_), float(hy_)
        yy_, xx_ = np.nonzero(band[int(hy_) - 90:int(hy_) + 90, int(hx_) - 90:int(hx_) + 90])
        if len(xx_) < 30:
            continue
        pts_ = np.c_[xx_ + int(hx_) - 90, yy_ + int(hy_) - 90].astype(float)
        dd = np.hypot(pts_[:, 0] - hx_, pts_[:, 1] - hy_)
        c0 = pts_[np.argmin(dd)]
        near = pts_[np.hypot(pts_[:, 0] - c0[0], pts_[:, 1] - c0[1]) < 80]
        mu = near.mean(0)
        u, sv, vt = np.linalg.svd(near - mu)
        dx_, dy_ = vt[0]
        if dx_ < 0:
            dx_, dy_ = -dx_, -dy_
        ang = -math.degrees(math.atan2(dy_, dx_))
        nx_, ny_ = -dy_, dx_
        # Osmanlı dışı tarafa kaydır
        tx_, ty_ = int(mu[0] + nx_ * 20), int(mu[1] + ny_ * 20)
        if 0 <= ty_ < H and 0 <= tx_ < W and ott1[ty_, tx_]:
            nx_, ny_ = -nx_, -ny_
        cxl, cyl = mu[0] + nx_ * 20, mu[1] + ny_ * 20
        tl = Image.new("RGBA", (420, 50), (0, 0, 0, 0))
        Canvas(tl).tracked((210, 34), "1876 OSMANLI SINIRI", bar(18, "SemiBold"), 5, FRONT[:3] + (190,), anchor="c")
        tl = tl.rotate(ang, expand=True, resample=Image.BICUBIC)
        cv.img.alpha_composite(tl, (int(cxl) - tl.width // 2, int(cyl) - tl.height // 2))
        cv.occupy((cxl - 110, cyl - 30, cxl + 110, cyl + 30))
    place_cities(cv, F, ott1, [([c_ for c_ in T2 if c_[0] not in KEY2], 2), (T3, 3)])
    # İstanbul notu
    px, py = F.ll_to_px(28.97, 41.01)
    cv.halo((float(px) - 10, float(py) + 32), "(Dersaadet · hesaplara katılmadı)", bar(16, "Medium"), MUTE, anchor="rs", rad=3)
    log("etiketler")

    # ---- başlık bloğu
    d = cv.d
    d.line((140, 74, W / 2 - 30, 74), fill=BRASS, width=2)
    d.line((W / 2 + 30, 74, W - 140, 74), fill=BRASS, width=2)
    d.line((140, 80, W / 2 - 36, 80), fill=BRASS[:3] + (115,), width=1)
    d.line((W / 2 + 36, 80, W - 140, 80), fill=BRASS[:3] + (115,), width=1)
    star8(d, W / 2, 77, 16, BRASS, 2)
    cv.tracked((W / 2, 140), "OSMANLI KAYITLARI VE DÖNEM HARİTALARINA GÖRE · 93 HARBİ ARİFESİ", bar(32, "SemiBold"), 10, BRASS, anchor="c")
    tsize = 184
    while bs(tsize).getlength("RUMELİ’NİN SON IŞIKLARI") > 1880:
        tsize -= 2
    cv.halo((W / 2, 318), "RUMELİ’NİN SON IŞIKLARI", bs(tsize), IV, anchor="ms", rad=8, strength=0.6)
    cv.halo((W / 2, 416), "1876’da Balkanlar’da kim, nerede yaşıyordu?", bod(64, 600, 11), IV2, anchor="ms", rad=6, strength=0.6)
    # lejant satırı
    items = [(0, "Türk"), (1, "Diğer Müslüman"), (2, "Hristiyan")]
    f1, f2 = bar(38, "SemiBold"), bar(32, "Medium")
    unit = "1 nokta = 250 kişi (≈ 50 hane)"
    tot = sum(70 + f1.getlength(t) + 44 for _, t in items) + 30 + f2.getlength(unit)
    xx = W / 2 - tot / 2
    yb = 506
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for g, t in items:
        for j, (ox, oy) in enumerate(((0, 0), (14, -6), (26, 2), (12, 9), (36, -3))):
            cx_, cy_ = xx + 8 + ox, yb - 13 + oy
            gd.ellipse((cx_ - 9, cy_ - 9, cx_ + 9, cy_ + 9), fill=hx(COL[g], 120))
            d.ellipse((cx_ - 5, cy_ - 5, cx_ + 5, cy_ + 5), fill=hx(COL[g]))
        xx += 62
        d.text((xx, yb), t, font=f1, fill=TINT[g], anchor="ls")
        xx += f1.getlength(t) + 44
    d.ellipse((xx - 22, yb - 15, xx - 18, yb - 11), fill=BRASS)
    d.text((xx, yb), unit, font=f2, fill=MUTE, anchor="ls")
    cv.img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(4)))
    d = cv.d

    # ---- KAYIT bloğu
    cv.obst.remove(KAYIT)
    cv.panel(KAYIT)
    d = cv.d
    cv.tracked((1080, 652), "BUGÜNKÜ BULGARİSTAN", bar(24, "SemiBold"), 4, BRASS)
    cv.tracked((1080, 680), "TOPRAKLARINDA, 1875", bar(24, "SemiBold"), 4, BRASS)
    d.text((1074, 812), fmt_pct(C.TOTAL_BG), font=bs(136), fill=IV, anchor="ls")
    d.text((1080, 852), "Bulgar. Her 100 kişiden", font=bar(30, "SemiBold"), fill=IV, anchor="ls")
    nb = 100 - round(C.TOTAL_BG)
    d.text((1080, 888), f"{nb}’ü Bulgar değildi.", font=bar(30, "SemiBold"), fill=IV, anchor="ls")
    d.text((1080, 914), f"il verisi: {RECORDS['BG1875']['src_short']} · ayrıntı aşağıda", font=bar(16, "Medium"), fill=MUTE, anchor="ls")
    d.line((1420, 640, 1420, 900), fill=BRASS[:3] + (100,), width=1)
    cv.tracked((1436, 650), "OSMANLI KAYDI", bar(20, "SemiBold"), 3, BRASS)
    cv.tracked((1436, 676), "TUNA VİLÂYETİ · 1292/1875", bar(20, "SemiBold"), 3, IV)
    t_ = f"Tahrir-i Cedid · {fmt_int(RECORDS['TUNA_1875']['males'])} erkek (1 kare = 1.000) · Niş hariç"
    fz_ = 15
    while bar(fz_, "Medium").getlength(t_) > 1730 - 1436 and fz_ > 11:
        fz_ -= 1
    d.text((1436, 698), t_, font=bar(fz_, "Medium"), fill=MUTE, anchor="ls")
    cats = [(406, hx(COL[0]), False), (55, hx(COL[1]), False), (606, hx(COL[2]), False), (54, hx("#8A93A3"), True)]
    seq = []
    for n_, c_, hol in cats:
        seq += [(c_, hol)] * n_
    ox, oy = 1433, 712
    for i, (c_, hol) in enumerate(seq):
        col_, row_ = i // 19, i % 19
        x0, y0 = ox + col_ * 5, oy + row_ * 5
        if hol:
            d.rectangle((x0, y0, x0 + 3, y0 + 3), outline=c_, width=1)
        else:
            d.rectangle((x0, y0, x0 + 3, y0 + 3), fill=c_)
    # ilk 461 karenin (Müslüman) basamaklı çerçevesi
    fullc, rem = divmod(461, 19)
    x_e = ox + fullc * 5
    pts = [(ox - 2, oy - 2), (x_e + 4 + 1, oy - 2), (x_e + 4 + 1, oy + rem * 5 - 1),
           (x_e - 1, oy + rem * 5 - 1), (x_e - 1, oy + 19 * 5 + 1), (ox - 2, oy + 19 * 5 + 1), (ox - 2, oy - 2)]
    d.line(pts, fill=IV, width=2)
    d.text((1436, 860), fmt_pct(RECORDS["TUNA_1875"]["muslim_pct"]), font=bs(48), fill=IV, anchor="ls")
    d.text((1436, 884), "Müslüman", font=bar(20, "SemiBold"), fill=IV, anchor="ls")
    d.text((1590, 860), fmt_pct(RECORDS["TUNA_1875"]["bulgar_pct"]), font=bs(48), fill=TINT[2], anchor="ls")
    d.text((1590, 884), "Bulgar milleti", font=bar(20, "SemiBold"), fill=IV, anchor="ls")
    kx = 1436
    for c_, lab_, hol in ((hx(COL[0]), "İslam %36,2", False), (hx(COL[1]), "Çerkes, Kıpti %4,9", False),
                          (hx("#8A93A3"), "diğer %4,8", True)):
        if hol:
            d.rectangle((kx, 902, kx + 8, 910), outline=c_, width=1)
        else:
            d.rectangle((kx, 902, kx + 8, 910), fill=c_)
        d.text((kx + 12, 912), lab_, font=bar(15, "Medium"), fill=MUTE, anchor="ls")
        kx += 12 + bar(15, "Medium").getlength(lab_) + 9


    # ---- NASIL OKUNUR
    cv.obst.remove(NASIL)
    cv.panel(NASIL)
    d = cv.d
    x0, y0 = NASIL[0] + 22, NASIL[1]
    cv.tracked((x0, y0 + 40), "NASIL OKUNUR?", bar(24, "SemiBold"), 4, BRASS)
    subs = ["Tatar ve Nogaylar dâhil", "Pomak, Arnavut, Boşnak, Çerkes, Müslüman Roman", "Bulgar, Rum, Sırp, Ulah, Ermeni, Gagavuz…"]
    for i in range(3):
        yb = y0 + 92 + i * 56
        for (qx, qy) in ((0, 0), (12, 0), (6, -8), (0, -16), (12, -16)):
            d.ellipse((x0 + qx, yb - 14 + qy, x0 + qx + 7, yb - 7 + qy), fill=hx(COL[i]))
        d.text((x0 + 36, yb - 4), GROUP_NAMES[i], font=bar(30, "SemiBold"), fill=TINT[i], anchor="ls")
        d.text((x0 + 36, yb + 18), subs[i], font=bar(18, "Medium"), fill=MUTE, anchor="ls")
    yk = y0 + 268
    d.ellipse((x0 + 4, yk - 10, x0 + 10, yk - 4), fill=IV)
    d.text((x0 + 36, yk), "= 250 kişi", font=bar(19, "Medium"), fill=IV2, anchor="ls")
    for (qx, qy) in ((150, -2), (158, -6), (156, 2), (164, -1)):
        d.ellipse((x0 + qx, yk - 10 + qy, x0 + qx + 6, yk - 4 + qy), fill=IV)
    d.text((x0 + 178, yk), "≈ 1.000 kişilik bir köy", font=bar(19, "Medium"), fill=IV2, anchor="ls")
    yk += 30
    d.line((x0, yk - 8, x0 + 26, yk - 8), fill=FRONT, width=5)
    d.line((x0, yk - 8, x0 + 26, yk - 8), fill=hx("#05080D"), width=1)
    d.text((x0 + 36, yk), "1876 Osmanlı sınırı (yaklaşık)", font=bar(18, "Medium"), fill=IV2, anchor="ls")
    yk += 26
    for qx in range(0, 28, 7):
        d.ellipse((x0 + qx, yk - 9, x0 + qx + 3, yk - 6), fill=hx("#8C98AC", 160))
    d.text((x0 + 36, yk), "bugünkü sınırlar", font=bar(18, "Medium"), fill=IV2, anchor="ls")
    yk += 26
    for qx, g in ((0, 0), (9, 2), (18, 1)):
        d.ellipse((x0 + qx, yk - 11, x0 + qx + 6, yk - 5), fill=hx(COL[g], 85))
    d.text((x0 + 36, yk), "soluk: 1876’da doğrudan Osmanlı idaresi dışı", font=bar(18, "Medium"), fill=IV2, anchor="ls")
    yk += 26
    d.polygon([(x0 + 10, yk - 15), (x0 + 16, yk - 9), (x0 + 10, yk - 3), (x0 + 4, yk - 9)], fill=IV)
    d.text((x0 + 36, yk), "vilâyet merkezi / büyük şehir", font=bar(18, "Medium"), fill=IV2, anchor="ls")
    d.rectangle((x0 + 262, yk - 12, x0 + 268, yk - 6), fill=hx("#E1DACA"))
    d.text((x0 + 278, yk), "şehir, kasaba", font=bar(18, "Medium"), fill=IV2, anchor="ls")
    # ölçek
    yk += 30
    px100 = 100000 / F.mpp
    d.line((x0, yk, x0 + px100, yk), fill=BRASS, width=2)
    for t_, frac in (("0", 0), ("50", 0.5), ("100 km", 1)):
        xx_ = x0 + px100 * frac
        d.line((xx_, yk - 6, xx_, yk + 6), fill=BRASS, width=2)
        d.text((xx_, yk + 22), t_, font=bar(16, "Medium"), fill=MUTE, anchor="ms")
    d.text((x0, NASIL[3] - 10), "Noktaların yeri temsilîdir; oranlar kayıtlara ve tahminlere dayanır.", font=bar(16, "Regular"), fill=MUTE, anchor="ls")

    # ---- SONRA
    cv.obst.remove(SONRA)
    cv.panel(SONRA)
    d = cv.d
    sx = SONRA[0] + 18
    cv.tracked((sx, 1690), "SONRA: 93 HARBİ, 1877–78", bar(24, "SemiBold"), 4, BRASS)
    M = RECORDS["MCCARTHY"]
    d.text((sx, 1782), fmt_int(M["muslims"]), font=bs(80), fill=IV, anchor="ls")
    t_ = "Müslüman (1877) · Tuna vilâyeti + sonraki Şarkî Rumeli"
    fz_ = 20
    while bar(fz_, "Medium").getlength(t_) > SONRA[2] - sx - 10:
        fz_ -= 1
    d.text((sx, 1810), t_, font=bar(fz_, "Medium"), fill=IV2, anchor="ls")
    d.text((sx, 1882), fmt_int(M["dead"]), font=bs(56), fill=IV, anchor="ls")
    d.text((sx, 1908), "hayatını kaybetti", font=bar(20, "SemiBold"), fill=IV2, anchor="ls")
    d.text((sx + 194, 1882), fmt_int(M["emigrated"]), font=bs(56), fill=IV, anchor="ls")
    d.text((sx + 194, 1908), "göç etti", font=bar(20, "SemiBold"), fill=IV2, anchor="ls")
    d.text((sx, 1946), "J. McCarthy tahmini; aktaran A. Koyuncu,", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    d.text((sx, 1968), "Avrasya Etüdleri 44 (2013). Rakamlar tartışmalıdır.", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    fz = 26
    while bod(fz, 600, 9).getlength("hemen önceki Rumeli’yi gösteriyor.") > SONRA[2] - sx - 14:
        fz -= 1
    d.text((sx, 2024), "Bu harita, o büyük göçten", font=bod(fz, 600, 9), fill=IV, anchor="ls")
    d.text((sx, 2056), "hemen önceki Rumeli’yi gösteriyor.", font=bod(fz, 600, 9), fill=IV, anchor="ls")

    # ---- gül, enlem çentikleri
    rot = math.degrees(math.atan2(*(lambda p, q: (q[0] - p[0], -(q[1] - p[1])))(
        tuple(map(float, F.ll_to_px(18.62, 41.06))), tuple(map(float, F.ll_to_px(18.62, 41.56))))))
    compass_rose(cv, ROSE[0], ROSE[1], ROSE[2], rot)
    lat_ticks(cv, F)

    # ---- alt şerit
    st = Image.new("RGBA", (STRIP[2] - STRIP[0], STRIP[3] - STRIP[1]), (4, 6, 10, int(255 * 0.82)))
    cv.img.alpha_composite(st, (STRIP[0], STRIP[1]))
    d = cv.d
    d.line((STRIP[0], STRIP[1], STRIP[2], STRIP[1]), fill=BRASS, width=2)
    star8(d, 1080, STRIP[1], 10, BRASS, 2, fill=hx("#05080D"))
    # P-left: vilayet çubukları
    cv.tracked((80, 2206), "VİLÂYET VE SANCAKLARA GÖRE · 1876", bar(24, "SemiBold"), 4, BRASS)
    d.text((80, 2232), "çubuk: harita modeli (kişi) ·     Osmanlı kaydı · Yahudiler hariç · İstanbul hariç", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    dx_ = 80 + bar(17, "Medium").getlength("çubuk: harita modeli (kişi) · ") + 4
    d.polygon([(dx_ + 6, 2218), (dx_ + 12, 2224), (dx_ + 6, 2230), (dx_, 2224)], fill=IV)
    bx0, bw = 256, 580
    y_ = 2256
    d.line((bx0 + bw / 2, y_ - 8, bx0 + bw / 2, y_ + 34 * min(len(ROWS), 10) - 8), fill=BRASS[:3] + (90,), width=1)
    d.text((bx0 + bw / 2 + 4, y_ - 3), "%50", font=bar(14, "Medium"), fill=BRASS, anchor="ls")
    cv.tracked((bx0 + bw + 14, y_ - 10), "MÜSLÜMAN", bar(14, "SemiBold"), 2, BRASS)
    cv.tracked((bx0 + bw + 112, y_ - 10), "KAYIT", bar(14, "SemiBold"), 2, BRASS)
    for i, (n, g, p, rec) in enumerate(ROWS[:10]):
        hb = 26 if i == 0 else 22
        yy = y_ + i * 34
        d.text((80, yy + hb - 3), n, font=bar(24 if i else 26, "SemiBold"), fill=BRASS if i == 0 else IV, anchor="ls")
        xs_ = bx0
        pint = largest_remainder(g, nd=0)
        for gi in range(3):
            wseg = bw * p[gi] / 100
            if wseg > 0.5:
                d.rectangle((xs_, yy, xs_ + max(0, wseg - 2), yy + hb), fill=hx(COL[gi]))
                if wseg >= 44:
                    d.text((xs_ + wseg / 2 - 1, yy + hb - 5), f"{pint[gi]:.0f}", font=bar(16, "SemiBold"), fill=hx("#05080D"), anchor="ms")
            xs_ += wseg
        if i == 0:
            d.rectangle((bx0 - 1, yy - 1, bx0 + bw + 1, yy + hb + 1), outline=BRASS, width=1)
        mus = p[0] + p[1]
        d.text((bx0 + bw + 14, yy + hb - 2), fmt_pct(mus), font=bs(32), fill=IV, anchor="ls")
        if rec:
            xr = bx0 + bw * rec / 100
            d.rectangle((xr - 2, yy - 4, xr + 2, yy + hb + 4), fill=IV)
            d.polygon([(xr, yy - 14), (xr + 5, yy - 9), (xr, yy - 4), (xr - 5, yy - 9)], fill=IV)
            d.text((bx0 + bw + 112, yy + hb - 2), f"{REC_YEAR.get(n, '')} {fmt_pct(rec)}", font=bar(20, "SemiBold"), fill=IV2, anchor="ls")
    d.line((1085, 2190, 1085, 2590), fill=BRASS[:3] + (100,), width=1)
    star8(d, 1085, 2390, 9, BRASS, 1, fill=hx("#05080D"))
    # P-right: Bulgaristan 1875 il haritası
    cv.tracked((1110, 2206), "BUGÜNKÜ BULGARİSTAN, 1875 · İL İL BULGAR ORANI", bar(24, "SemiBold"), 4, BRASS)
    d.text((1110, 2232), f"Kaynak: {RECORDS['BG1875']['src_short']} · sayı: ildeki Bulgarların payı (%)", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    obl = C.oblasts()
    allb = shapely.union_all(list(obl.values()))
    mx0, my0, mx1, my1 = 1110, 2250, 1680, 2590
    gx0, gy0, gx1, gy1 = allb.bounds
    sc = min((mx1 - mx0) / (gx1 - gx0), (my1 - my0) / (gy1 - gy0))
    offx = mx0 + ((mx1 - mx0) - (gx1 - gx0) * sc) / 2
    offy = my0 + ((my1 - my0) - (gy1 - gy0) * sc) / 2
    tp = lambda xy: [(offx + (a_ - gx0) * sc, offy + (gy1 - b_) * sc) for a_, b_ in xy]
    TG = C.TARGET_BG
    S2 = 2
    mm = Image.new("RGBA", (W * S2, H * S2), (0, 0, 0, 0))
    md = ImageDraw.Draw(mm)
    tp2 = lambda xy: [(u * S2, v * S2) for u, v in tp(xy)]
    for nm, g in obl.items():
        t = TG[nm] / 100
        colm = tuple(int(v) for v in (np.array([14, 20, 32]) * (1 - t) + np.array(hx(COL[2])[:3]) * t)) + (255,)
        for pp in (g.geoms if hasattr(g, "geoms") else [g]):
            md.polygon(tp2(pp.exterior.coords), fill=colm, outline=(5, 8, 13, 255), width=3)
    for nm, g in obl.items():
        if TG[nm] < 50:
            for pp in (g.geoms if hasattr(g, "geoms") else [g]):
                inner = pp.buffer(-1.6 / sc)
                for q in (inner.geoms if hasattr(inner, "geoms") else [inner]):
                    if not q.is_empty:
                        md.line(tp2(q.exterior.coords), fill=BRASS, width=3)
    cv.img.alpha_composite(mm.resize((W, H), Image.LANCZOS))
    for nm, g in obl.items():
        c_ = g.representative_point()
        if nm == "Grad Sofiya":
            (px_, py_), = tp([(c_.x, c_.y)])
            cv.halo((px_, py_ + 7), f"{TG[nm]}", bs(18, 800), IV, anchor="ms", rad=2)
            continue
        (px_, py_), = tp([(c_.x, c_.y)])
        v = TG[nm]
        cv.halo((px_, py_ + 9), f"{v}", bs(28, 800) if v < 50 else bs(22, 600), IV if v < 50 else IV[:3] + (190,), anchor="ms", rad=3)
    nlow = sum(1 for v in TG.values() if v < 50)
    tx = 1710
    d = cv.d
    d.text((tx, 2330), f"{nlow} / 28 il", font=bs(72), fill=IV, anchor="ls")
    d.text((tx, 2362), "Bulgarlar nüfusun yarısından azdı.", font=bar(24, "SemiBold"), fill=IV, anchor="ls")
    d.text((tx, 2400), f"Bulgaristan toplamı: {fmt_pct(C.TOTAL_BG)} Bulgar", font=bar(22, "SemiBold"), fill=IV2, anchor="ls")
    OTT = {"Kardzhali": "Kırcaali", "Dobrich": "Hacıoğlu Pazarcığı", "Razgrad": "Hezargrad", "Targovishte": "Eski Cuma",
           "Shumen": "Şumnu", "Smolyan": "Paşmaklı", "Haskovo": "Hasköy", "Ruse": "Rusçuk", "Varna": "Varna",
           "Silistra": "Silistre", "Grad Sofiya": "Sofya (şehir)"}
    low = sorted(TG.items(), key=lambda t: t[1])[:4]
    s1 = " · ".join(f"{OTT.get(n, n)} %{v}" for n, v in low[:2])
    s2 = " · ".join(f"{OTT.get(n, n)} %{v}" for n, v in low[2:])
    d.text((tx, 2440), "En düşük: " + s1, font=bar(19, "Medium"), fill=IV2, anchor="ls")
    d.text((tx, 2466), s2, font=bar(19, "Medium"), fill=IV2, anchor="ls")
    for i in range(300):
        t = i / 299
        cc = tuple(int(v) for v in (np.array([14, 20, 32]) * (1 - t) + np.array(hx(COL[2])[:3]) * t))
        d.line((tx + i, 2486, tx + i, 2496), fill=cc)
    d.text((tx, 2514), "%0", font=bar(15, "Medium"), fill=MUTE, anchor="ls")
    d.text((tx + 300, 2514), "%100 Bulgar", font=bar(15, "Medium"), fill=MUTE, anchor="rs")
    d.rectangle((tx, 2528, tx + 22, 2542), outline=BRASS, width=2)
    d.text((tx + 30, 2542), "altın çerçeve: Bulgarlar < %50", font=bar(16, "Medium"), fill=MUTE, anchor="ls")
    # harita modeli: aynı sınırlarda Hristiyan payı
    rows_b = C.compare_dots(F, x, y, k, verbose=False)
    ch_tot = sum(r_[2] * r_[5] for r_ in rows_b) / max(1, sum(r_[5] for r_ in rows_b))
    d.text((tx, 2566), f"Harita modeli aynı sınırlarda: {fmt_pct(ch_tot)} Hristiyan", font=bar(15, "Medium"), fill=MUTE, anchor="ls")
    d.text((tx, 2586), "(Bulgar + Rum, Ulah, Gagavuz vb.)", font=bar(15, "Medium"), fill=MUTE, anchor="ls")

    # ---- Selanik notu
    px, py = F.ll_to_px(23.27, 39.82)
    sx_, sy_ = F.ll_to_px(22.94, 40.64)
    d.line((float(sx_) + 4, float(sy_) + 10, float(px) + 20, float(py) - 30), fill=IV[:3] + (128,), width=1)
    cv.halo((float(px), float(py) - 14), "Selanik’te en kalabalık topluluk", bar(17, "Medium"), IV2, anchor="ls", rad=3)
    cv.halo((float(px), float(py) + 8), "Yahudilerdi; harita üç grubu gösterir.", bar(17, "Medium"), IV2, anchor="ls", rad=3)

    # ---- çerçeve
    frame_ornament(cv)
    d = cv.d
    # ---- dipnot
    srcs = " · ".join([RECORDS["TUNA_1875"]["src"], RECORDS["EDIRNE_1293"]["src"], RECORDS["BOSNA_1287"]["src"]])
    f17 = bar(17, "Medium")
    l1 = "Kaynaklar: " + srcs
    l2 = (RECORDS["MCCARTHY"]["src"] + " · Bulgaristan il oranları: " + RECORDS["BG1875"]["src"] +
          " · A. H. Layard raporu 1877 (M. Köse 2019) · 1881/82 Osmanlı sayımı (K. Karpat) · M. Kokolakis 2003 · "
          "yerleşim: C. Sax 1878, V. Kănčov 1900 · sınır: H. Kiepert 1870 · Natural Earth, AWS Terrain")
    l3 = (f"Yöntem: {len(cl)} bölge kümesi; Osmanlı kayıtları esas, Bulgaristan’da il oranlarına göre ayarlandı · kayıt eksiği "
          "bilinen yerlerde Müslüman payı için kaynakların üst değeri alındı (ör. McCarthy düzeltmesi) · nokta yerleri temsilîdir · "
          "erkek sayımları ×2 · Yahudiler gösterilmedi · Tatar/Nogay = Türk · ‘İslam milleti’ Türk–Pomak ayrımı yapmaz")
    for i, t in enumerate((l1, l2, l3)):
        fs = 16
        while bar(fs, "Medium").getlength(t) > 1900 and fs > 11:
            fs -= 1
        d.text((W / 2, 2606 + i * 19), t, font=bar(fs, "Medium"), fill=MUTE, anchor="ms")
    if a.imza:
        d.text((W - 170, 2600), a.imza, font=bar(22, "SemiBold"), fill=IV[:3] + (155,), anchor="rs")

    out = cv.img.convert("RGB")
    # ±1/255 titreşim (bantlaşmayı önler)
    arr = np.asarray(out, np.int16) + np.random.default_rng(7).integers(-1, 2, (H, W, 1))
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    out.save(a.out + ".png", optimize=True)
    out.resize((1080, 1350), Image.LANCZOS).save(a.out + "_ig_1080x1350.jpg", quality=95, subsampling=0)
    log("bitti ->", a.out + ".png")


if __name__ == "__main__":
    main()
