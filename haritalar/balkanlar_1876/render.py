#!/usr/bin/env python3
"""Balkanlar'da Türkler, Müslümanlar ve Hristiyanlar (1876) haritası.

Kullanım:
    python3 render.py                      # isimsiz
    python3 render.py --imza "© Ad Soyad"  # alt-başlık hapında imza

Veri: data/*.json  (her bölge için küme listesi: lat, lon, radius_km,
turk / muslim_other / christian yüzdeleri, density)
Altlık: Natural Earth 10m (otomatik indirilir, cache/ klasörüne).
"""
import argparse
import glob
import json
import math
import os
import urllib.request
import zipfile

import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from scipy.ndimage import gaussian_filter, zoom
from scipy.special import ndtr
from pyproj import Transformer

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
FONTS = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- görünüm
W_PX, H_PX = 2600, 2000                     # çıktı boyutu
CRS = "+proj=lcc +lat_1=40 +lat_2=44 +lat_0=42.55 +lon_0=22.6 +datum=WGS84 +units=m +no_defs"
FRAME_W_KM = 1200.0
FRAME_H_KM = FRAME_W_KM * H_PX / W_PX
CENTER_SHIFT_KM = (28.0, 0.0)

SEA = "#fbfbfb"
LAND = "#bfbfbf"
BORDER = "#f4f4f4"

CATS = ["turk", "muslim_other", "christian"]
COLORS = {                                   # Türk / diğer Müslüman / Hristiyan
    "turk": (214, 12, 22),
    "muslim_other": (16, 122, 58),
    "christian": (52, 40, 200),
}

GRID_KM = 1.0
SEED = 1876

TO_XY = Transformer.from_crs("EPSG:4326", CRS, always_xy=True)


def frame():
    cx, cy = CENTER_SHIFT_KM
    return (
        (cx - FRAME_W_KM / 2) * 1000,
        (cx + FRAME_W_KM / 2) * 1000,
        (cy - FRAME_H_KM / 2) * 1000,
        (cy + FRAME_H_KM / 2) * 1000,
    )


def lonlat_to_px(lon, lat):
    x, y = TO_XY.transform(lon, lat)
    x0, x1, y0, y1 = frame()
    return (x - x0) / (x1 - x0) * W_PX, (y1 - y) / (y1 - y0) * H_PX


# ---------------------------------------------------------------- altlık
NE = {
    "countries": "cultural/ne_10m_admin_0_countries",
    "borders": "cultural/ne_10m_admin_0_boundary_lines_land",
    "lakes": "physical/ne_10m_lakes",
}


def ne_layer(key):
    name = NE[key].split("/")[1]
    shp = os.path.join(CACHE, name + ".shp")
    if not os.path.exists(shp):
        os.makedirs(CACHE, exist_ok=True)
        z = os.path.join(CACHE, name + ".zip")
        urllib.request.urlretrieve(f"https://naciscdn.org/naturalearth/10m/{NE[key]}.zip", z)
        with zipfile.ZipFile(z) as f:
            f.extractall(CACHE)
    g = gpd.read_file(shp, bbox=(10, 34, 36, 50))
    return g


def lonlat_poly(pts):
    return Polygon(pts)


def data_region(countries):
    """1876 haritasının veri alanı: Tuna–Sava hattının güneyindeki Balkan
    yarımadası + Dobruca + Doğu Trakya (İstanbul dahil)."""
    by = {r["ADM0_A3"]: r.geometry for _, r in countries.iterrows()}
    parts = []
    for a3 in ["BGR", "MKD", "ALB", "MNE", "BIH", "KOS"]:
        parts.append(by[a3])
    # Sırbistan: Voyvodina (Sava–Tuna kuzeyi) hariç
    vojvodina_cut = lonlat_poly([
        (18.8, 46.5), (18.8, 44.86), (19.35, 44.90), (19.70, 44.77), (20.20, 44.67),
        (20.45, 44.83), (20.65, 44.84), (20.93, 44.68), (21.35, 44.77), (21.65, 44.70),
        (23.0, 44.70), (23.0, 46.5)])
    parts.append(by["SRB"].difference(vojvodina_cut))
    # Hırvatistan: Sava/Kupa güneyi (Dalmaçya, Lika, Askerî Sınır)
    croatia_south = lonlat_poly([
        (13.0, 42.0), (13.0, 45.35), (15.2, 45.45), (15.6, 45.50), (16.37, 45.48),
        (17.0, 45.25), (18.0, 45.13), (18.85, 44.86), (19.5, 44.85), (19.5, 42.0)])
    parts.append(by["HRV"].intersection(croatia_south))
    # Romanya: yalnız Kuzey Dobruca
    dobruja = lonlat_poly([
        (27.27, 44.12), (27.70, 44.20), (28.02, 44.33), (27.95, 44.68), (27.97, 45.15),
        (28.10, 45.42), (28.45, 45.30), (28.75, 45.26), (29.10, 45.30), (29.9, 45.40),
        (29.9, 43.6), (27.27, 43.6)])
    fr = os.path.join(HERE, "data", "frontier_1876.json")
    if os.path.exists(fr):
        # 1876 Dobruca sınırı: Tuna kolları (Kiepert 1870) boyunca
        for ln in json.load(open(fr, encoding="utf-8"))["lines"]:
            if "Dobruca" in ln["name"]:
                co = [tuple(c) for c in ln["coords"]]
                if co[0][0] > co[-1][0]:
                    co = co[::-1]
                dobruja = shapely.make_valid(Polygon(co + [(30.2, 45.3), (30.2, 43.6), (co[0][0], 43.6)]))
    parts.append(by["ROU"].intersection(dobruja))
    # Yunanistan: ekranda kalan kısım (Girit hariç)
    parts.append(by["GRC"].intersection(box(19, 37.6, 27, 42)))
    # Türkiye: yalnız Avrupa yakası (Trakya) + Gökçeada/Bozcaada
    tur = by["TUR"]
    geoms = list(tur.geoms) if isinstance(tur, MultiPolygon) else [tur]
    for g in geoms:
        c = g.representative_point()
        if (c.x < 29.1 and c.y > 40.5 and g.area > 0.5) or c.x < 26.2:  # Trakya + Gökçeada/Bozcaada
            parts.append(g)
    reg = unary_union([shapely.make_valid(p) for p in parts])
    return gpd.GeoSeries([reg], crs="EPSG:4326").to_crs(CRS).iloc[0]


def geom_to_path(geom):
    verts, codes = [], []
    polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
    for p in polys:
        if p.is_empty or p.geom_type != "Polygon":
            continue
        for ring in [p.exterior, *p.interiors]:
            xy = np.asarray(ring.coords)
            verts.extend(xy.tolist())
            codes.extend([Path.MOVETO] + [Path.LINETO] * (len(xy) - 2) + [Path.CLOSEPOLY])
    return Path(verts, codes)


# ---------------------------------------------------------------- veri
def load_clusters(paths=None):
    paths = paths or sorted(glob.glob(os.path.join(HERE, "data", "*.json")))
    cl = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        for c in d["clusters"]:
            s = np.array([max(0.0, float(c[k])) for k in CATS])
            if s.sum() <= 0:
                continue
            c = dict(c)
            c["shares"] = s / s.sum()
            c["src"] = os.path.basename(p)
            cl.append(c)
    return cl


def smooth_noise(rng, shape, sigma):
    n = gaussian_filter(rng.standard_normal(shape).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-9)


def ethnic_raster(clusters, region_geom):
    """Her ızgara hücresine bir kategori atar (0 boş, 1..3)."""
    x0, x1, y0, y1 = frame()
    nx = int(round((x1 - x0) / (GRID_KM * 1000)))
    ny = int(round((y1 - y0) / (GRID_KM * 1000)))
    xs = x0 + (np.arange(nx) + 0.5) * GRID_KM * 1000
    ys = y0 + (np.arange(ny) + 0.5) * GRID_KM * 1000
    X, Y = np.meshgrid(xs, ys)  # (ny, nx), satır 0 = güney
    rng = np.random.default_rng(SEED)

    # organik sınırlar için alan bükme (domain warp)
    warp_x = (smooth_noise(rng, (ny, nx), 14) * 5.5 + smooth_noise(rng, (ny, nx), 3.5) * 1.8) * 1000
    warp_y = (smooth_noise(rng, (ny, nx), 14) * 5.5 + smooth_noise(rng, (ny, nx), 3.5) * 1.8) * 1000
    WX, WY = X + warp_x, Y + warp_y

    cx, cy = TO_XY.transform([c["lon"] for c in clusters], [c["lat"] for c in clusters])
    cx, cy = np.asarray(cx, np.float32), np.asarray(cy, np.float32)
    r = np.array([max(3.0, float(c["radius_km"])) for c in clusters], np.float32) * 1000
    logr = np.log(r / 1000.0)
    shares = np.stack([c["shares"] for c in clusters]).astype(np.float32)
    dens_thr = {"high": 2.9, "normal": 2.35, "low": 1.2}
    thr = np.array([dens_thr.get(c.get("density", "normal"), 2.0) for c in clusters], np.float32)

    cov_lim = 1.80 + 0.28 * smooth_noise(rng, (ny, nx), 2.0)

    owner = np.full(ny * nx, -1, np.int32)
    flatX, flatY = WX.ravel().astype(np.float32), WY.ravel().astype(np.float32)
    flatL = cov_lim.ravel()
    CH = 40000
    for s in range(0, flatX.size, CH):
        dx = flatX[s:s + CH, None] - cx[None, :]
        dy = flatY[s:s + CH, None] - cy[None, :]
        q = np.sqrt(dx * dx + dy * dy) / r[None, :]
        score = q + 0.5 * logr[None, :]
        score[q >= flatL[s:s + CH, None]] = np.inf
        best = np.argmin(score, axis=1)
        ok = np.isfinite(score[np.arange(best.size), best])
        owner[s:s + CH][ok] = best[ok]
    owner = owner.reshape(ny, nx)

    # kategori seçimi: mekânsal olarak ilişkili Gumbel gürültüsü ile
    # (her hücrede P(kategori) = o bölgenin nüfus payı; komşu hücreler ortak lekeler oluşturur)
    gum = []
    for _ in CATS:
        n = smooth_noise(rng, (ny, nx), 4.5) * 0.88 + smooth_noise(rng, (ny, nx), 1.4) * 0.47
        n = n / n.std()
        u = np.clip(ndtr(n), 1e-6, 1 - 1e-6)
        gum.append(-np.log(-np.log(u)))
    gum = np.stack(gum, -1)
    valid = owner >= 0
    S = np.where(valid[..., None], shares[np.clip(owner, 0, None)], 1.0)
    with np.errstate(divide="ignore"):
        logit = np.log(S) + gum
    cat = np.argmax(logit, -1) + 1
    cat[~valid] = 0

    # boşluklar (seyrek yerleşim, dağlar)
    holes = smooth_noise(rng, (ny, nx), 2.8)
    T = np.where(valid, thr[np.clip(owner, 0, None)], 0)
    cat[(holes > T) & valid] = 0
    return cat, owner


def upsample_labels(cat):
    """1 km ızgarayı çıktı çözünürlüğüne yumuşak kenarlarla büyütür."""
    ny, nx = cat.shape
    zy, zx = H_PX / ny, W_PX / nx
    layers = []
    for k in range(4):
        m = (cat == k).astype(np.float32)
        m = gaussian_filter(m, 0.55)
        m = zoom(m, (zy, zx), order=1)[:H_PX, :W_PX]
        m = gaussian_filter(m, 0.8)
        layers.append(m)
    L = np.argmax(np.stack(layers, -1), -1)
    return L[::-1]  # satır 0 = kuzey


def colorize(L, rng):
    img = np.zeros(L.shape + (4,), np.float32)
    tex = smooth_noise(rng, L.shape, 6) * 0.035
    for k, c in enumerate(CATS, start=1):
        m = L == k
        col = np.array(COLORS[c], np.float32) / 255
        img[m, :3] = np.clip(col[None, :] * (1 + tex[m, None]), 0, 1)
        img[m, 3] = 1
    return img


# ---------------------------------------------------------------- çizim
def render_base(clusters, out_png, debug=False):
    countries = ne_layer("countries")
    borders = ne_layer("borders")
    lakes = ne_layer("lakes")
    region = data_region(countries)
    x0, x1, y0, y1 = frame()

    view = gpd.GeoSeries([box(x0, y0, x1, y1)], crs=CRS).to_crs("EPSG:4326").total_bounds
    clipbox = box(view[0] - 1, view[1] - 1, view[2] + 1, view[3] + 1)
    cp = countries.clip(clipbox).to_crs(CRS)
    bp = borders.clip(clipbox).to_crs(CRS)
    lk = lakes.clip(clipbox).to_crs(CRS)
    lk = lk[lk.geometry.area > 15e6]

    cat, owner = ethnic_raster(clusters, region)
    L = upsample_labels(cat)
    rng = np.random.default_rng(SEED + 1)
    rgba = colorize(L, rng)

    fig = plt.figure(figsize=(W_PX / 100, H_PX / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis("off")
    fig.patch.set_facecolor(SEA)
    ax.set_facecolor(SEA)
    cp.plot(ax=ax, color=LAND, linewidth=0)
    im = ax.imshow(rgba, extent=(x0, x1, y0, y1), origin="upper", interpolation="nearest", zorder=3)
    land_region = shapely.make_valid(region)
    patch = PathPatch(geom_to_path(land_region), transform=ax.transData, facecolor="none", edgecolor="none")
    ax.add_patch(patch)
    im.set_clip_path(patch)
    lk.plot(ax=ax, color=SEA, linewidth=0, zorder=4)
    bp.plot(ax=ax, color=BORDER, linewidth=1.5, zorder=5)
    if debug:
        cx, cy = TO_XY.transform([c["lon"] for c in clusters], [c["lat"] for c in clusters])
        ax.scatter(cx, cy, s=6, c="k", zorder=9)
        for c, a, b in zip(clusters, cx, cy):
            ax.add_patch(plt.Circle((a, b), c["radius_km"] * 1000, fill=False, lw=0.4, color="k", zorder=9))
    fig.savefig(out_png, dpi=100, facecolor=SEA)
    plt.close(fig)
    return cat, owner


# ---------------------------------------------------------------- yazılar (PIL)
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Kanit-{name}.ttf"), size)


def tracked_width(text, fnt, track):
    return sum(fnt.getlength(ch) for ch in text) + track * (len(text) - 1)


def draw_tracked(img, xy, text, fnt, track, fill, anchor="mm", stroke=0, stroke_fill=None,
                 angle=0.0, shadow=None):
    """Harf aralıklı metin (isteğe bağlı döndürme, kontur, gölge)."""
    w = tracked_width(text, fnt, track)
    asc, desc = fnt.getmetrics()
    pad = 12 + stroke * 2 + (shadow[2] * 3 if shadow else 0)
    tw, th = int(w + 2 * pad), int(asc + desc + 2 * pad)
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = pad
    for ch in text:
        d.text((x, pad), ch, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += fnt.getlength(ch) + track
    if shadow:
        sx, sy, blur, col = shadow
        a = layer.split()[3].filter(ImageFilter.GaussianBlur(blur))
        sh = Image.new("RGBA", layer.size, col)
        sh.putalpha(a.point(lambda v: int(v * col[3] / 255)))
        base = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        base.alpha_composite(sh, (int(sx), int(sy)) if sx >= 0 and sy >= 0 else (0, 0))
        base.alpha_composite(layer)
        layer = base
    if angle:
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    cx, cy = xy
    if anchor == "mm":
        pos = (int(cx - layer.width / 2), int(cy - layer.height / 2))
    elif anchor == "lm":
        pos = (int(cx - pad), int(cy - layer.height / 2))
    else:
        pos = (int(cx), int(cy))
    img.alpha_composite(layer, pos)
    return w


def crescent(img, cx, cy, R, col):
    s = 4
    m = Image.new("L", (int(R * 2 * s) + 8, int(R * 2 * s) + 8), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((4, 4, 4 + 2 * R * s, 4 + 2 * R * s), fill=255)
    off = 0.52 * R * s
    r2 = 0.80 * R * s
    ccx, ccy = 4 + R * s + off, 4 + R * s
    d.ellipse((ccx - r2, ccy - r2, ccx + r2, ccy + r2), fill=0)
    # yıldız
    sx, sy, sr = 4 + R * s + 1.02 * R * s, 4 + R * s, 0.36 * R * s
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5 + math.pi
        rr = sr if i % 2 == 0 else sr * 0.40
        pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
    w = int(R * 2 * s + 8 + sr * 2)
    m2 = Image.new("L", (w + int(R * s), m.height), 0)
    m2.paste(m, (0, 0))
    d2 = ImageDraw.Draw(m2)
    pts = [(p[0], p[1]) for p in pts]
    # yıldızı hilalin açık tarafına döndür
    rot = []
    for (px, py) in pts:
        ang = math.radians(-18)
        dx, dy = px - sx, py - sy
        rot.append((sx + dx * math.cos(ang) - dy * math.sin(ang), sy + dx * math.sin(ang) + dy * math.cos(ang)))
    d2.polygon(rot, fill=255)
    m2 = m2.resize((m2.width // s, m2.height // s), Image.LANCZOS)
    layer = Image.new("RGBA", m2.size, col)
    layer.putalpha(m2.point(lambda v: int(v * col[3] / 255)))
    img.alpha_composite(layer, (int(cx - R), int(cy - R)))


def rounded_box(img, xyxy, radius, fill, outline, width):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(xyxy, radius=radius, fill=fill, outline=outline, width=width)


CITY_STYLE = {
    1: dict(size=40, stroke=3),
    2: dict(size=33, stroke=3),
    3: dict(size=28, stroke=2),
}

CITIES = [
    # (ad, lon, lat, rank, dx, dy)  dx/dy: piksel kaydırma
    ("İstanbul", 28.97, 41.02, 1, -1, -26),
    ("Edirne", 26.56, 41.68, 1, 0, 0),
    ("Selanik", 22.94, 40.64, 1, 0, -12),
    ("Manastır", 21.34, 41.03, 1, 0, 0),
    ("Yanya", 20.85, 39.67, 1, 0, 0),
    ("İşkodra", 19.51, 42.07, 1, 0, 0),
    ("Saraybosna", 18.41, 43.86, 1, 0, 0),
    ("Prizren", 20.74, 42.21, 2, 0, 0),
    ("Priştine", 21.16, 42.66, 2, 0, 0),
    ("Üsküp", 21.43, 42.00, 1, 0, 0),
    ("Rusçuk", 25.97, 43.85, 1, 0, 0),
    ("Filibe", 24.75, 42.15, 1, 0, 0),
    ("Sofya", 23.32, 42.70, 1, 0, 0),
    ("Niş", 21.90, 43.32, 2, 0, 0),
    ("Belgrad", 20.46, 44.82, 2, 0, -22),
    ("Varna", 27.91, 43.21, 2, 0, 0),
    ("Şumnu", 26.93, 43.27, 2, 0, 0),
    ("Tulça", 28.80, 45.18, 2, 0, 0),
    ("Köstence", 28.63, 44.17, 3, 0, 0),
    ("Silistre", 27.26, 44.12, 3, 0, 0),
    ("Vidin", 22.88, 43.99, 2, 0, 0),
    ("Tırnova", 25.63, 43.08, 2, 0, 0),
    ("Lofça", 24.72, 43.14, 3, 0, 0),
    ("Mostar", 17.81, 43.34, 2, 0, 0),
    ("Banaluka", 17.19, 44.77, 2, 0, 0),
    ("Yenipazar", 20.51, 43.14, 2, 0, 0),
    ("Kırcaali", 25.37, 41.65, 2, 0, 0),
    ("Gümülcine", 25.40, 41.12, 2, 0, 0),
    ("Drama", 24.15, 41.15, 3, 0, 0),
    ("Serez", 23.55, 41.09, 3, 0, 0),
    ("Tekirdağ", 27.51, 40.98, 2, 0, 0),
    ("Kırklareli", 27.22, 41.73, 3, 0, 0),
    ("Burgaz", 27.47, 42.50, 3, 0, 0),
    ("Eski Zağra", 25.63, 42.43, 3, 0, 0),
    ("Ohri", 20.80, 41.12, 3, 0, 0),
    ("Elbasan", 20.08, 41.11, 3, 0, 0),
    ("Berat", 19.95, 40.70, 3, 0, 0),
    ("Görice", 20.78, 40.62, 3, 0, 0),
    ("Yenişehir", 22.42, 39.64, 2, 0, 0),
    ("Tuzla", 18.67, 44.54, 3, 0, 0),
    ("Hezargrad", 26.52, 43.53, 3, 0, 0),
    ("Dedeağaç", 25.87, 40.85, 3, 0, 0),
]

COUNTRY_LABELS = [
    # (metin, lon, lat, açı, renk)
    ("ROMANYA", 25.2, 44.55, 0, "dark"),
    ("SIRBİSTAN", 21.05, 43.95, 0, "light"),
    ("BULGARİSTAN", 25.3, 42.92, 0, "light"),
    ("BOSNA-HERSEK", 17.75, 44.12, 0, "light"),
    ("KARADAĞ", 19.25, 42.86, 0, "light"),
    ("KOSOVA", 20.95, 42.45, 0, "light"),
    ("ARNAVUTLUK", 19.95, 40.95, 78, "light"),
    ("MAKEDONYA", 21.75, 41.55, 0, "light"),
    ("YUNANİSTAN", 21.85, 39.95, 0, "light"),
]
SEA_LABELS = [
    ("ADRİYATİK", 17.35, 41.95, 82),
    ("KARADENİZ", 29.55, 43.2, 90),
    ("EGE DENİZİ", 24.6, 39.75, 0),
    ("ANADOLU", 28.55, 39.75, 0),
]
MOUNTAIN_LABELS = [
    ("RODOP DAĞLARI", 24.55, 41.62, -16),
    ("BALKAN DAĞLARI", 25.3, 42.72, 0),
]


def overlay(base_png, out_png, imza=None, note=True):
    img = Image.open(base_png).convert("RGBA")
    W, H = img.size

    # ülke ve deniz adları
    for t, lon, lat, ang, tone in COUNTRY_LABELS:
        x, y = lonlat_to_px(lon, lat)
        if tone == "dark":
            draw_tracked(img, (x, y), t, font("Italic", 26), 15, (95, 95, 95, 255), angle=ang)
        else:
            draw_tracked(img, (x, y), t, font("MediumItalic", 25), 14, (255, 255, 255, 215),
                         stroke=1, stroke_fill=(40, 40, 40, 140), angle=ang)
    for t, lon, lat, ang in SEA_LABELS:
        x, y = lonlat_to_px(lon, lat)
        draw_tracked(img, (x, y), t, font("Italic", 25), 16, (120, 120, 120, 255), angle=ang)
    for t, lon, lat, ang in MOUNTAIN_LABELS:
        x, y = lonlat_to_px(lon, lat)
        draw_tracked(img, (x, y), t, font("MediumItalic", 19), 7, (255, 255, 255, 235),
                     stroke=2, stroke_fill=(30, 30, 30, 170), angle=ang)

    # şehirler
    for name, lon, lat, rank, dx, dy in CITIES:
        x, y = lonlat_to_px(lon, lat)
        st = CITY_STYLE[rank]
        d = ImageDraw.Draw(img)
        r = 5 if rank == 1 else 4
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 255), outline=(25, 25, 25, 255), width=2)
        fnt = font("BoldItalic", st["size"])
        if dx == -1:  # etiketi noktanın soluna yaz
            tw = tracked_width(name, fnt, 0.5)
            lx = x - r - 6 - tw
        else:
            lx = x + r + 6 + dx
        draw_tracked(img, (lx, y - 3 + dy), name, fnt, 0.5,
                     (255, 255, 255, 255), anchor="lm", stroke=st["stroke"], stroke_fill=(25, 25, 25, 230),
                     shadow=(2, 3, 3, (0, 0, 0, 120)))

    # başlık kutusu
    m = 34
    bx0, by0, bx1, by1 = m, 26, W - m, 136
    rounded_box(img, (bx0 + 4, by0 + 6, bx1 + 4, by1 + 6), 55, (0, 0, 0, 40), None, 0)
    rounded_box(img, (bx0, by0, bx1, by1), 55, (238, 238, 238, 240), (35, 35, 35, 255), 3)
    title = "Balkanlar’da Türkler, Müslümanlar ve Hristiyanlar"
    fs = 64
    while tracked_width(title, font("BoldItalic", fs), fs * 0.16) > (bx1 - bx0) - 120:
        fs -= 2
    draw_tracked(img, ((bx0 + bx1) / 2, (by0 + by1) / 2 - 4), title, font("BoldItalic", fs), fs * 0.16,
                 (15, 15, 15, 255))

    # alt-başlık hapları
    sub = imza if imza else "93 Harbi Öncesi Nüfus Dağılımı"
    sfnt = font("Italic", 40)
    sw = tracked_width(sub, sfnt, 6)
    sx0 = W / 2 - sw / 2 - 40
    sx1 = W / 2 + sw / 2 + 40
    rounded_box(img, (sx0, 156, sx1, 226), 35, (238, 238, 238, 240), (35, 35, 35, 255), 3)
    draw_tracked(img, (W / 2, 189), sub, sfnt, 6, (20, 20, 20, 255))
    yfnt = font("BoldItalic", 44)
    yt = "1876"
    yw = tracked_width(yt, yfnt, 10)
    yx1 = W - m - 6
    yx0 = yx1 - yw - 80
    rounded_box(img, (yx0, 156, yx1, 226), 35, (238, 238, 238, 240), (35, 35, 35, 255), 3)
    draw_tracked(img, ((yx0 + yx1) / 2, 189), yt, yfnt, 10, (15, 15, 15, 255))

    crescent(img, 104, 192, 44, (120, 120, 120, 220))

    # lejant
    items = [
        ("Türkler", "turk", "(Tatarlar dahil)"),
        ("Diğer Müslümanlar", "muslim_other", "(Pomak, Arnavut, Boşnak, Çerkez…)"),
        ("Hristiyanlar", "christian", "(Bulgar, Rum, Sırp, Ulah, Hırvat…)"),
    ]
    lw, lh = 1500, 132
    lx0 = W / 2 - lw / 2
    ly1 = H - 34
    ly0 = ly1 - lh
    rounded_box(img, (lx0 + 4, ly0 + 6, lx0 + lw + 4, ly1 + 6), 8, (0, 0, 0, 40), None, 0)
    rounded_box(img, (lx0, ly0, lx0 + lw, ly1), 8, (250, 250, 250, 245), (60, 60, 60, 255), 3)
    colw = (lw - 60) / 3
    d = ImageDraw.Draw(img)
    for i, (lab, key, small) in enumerate(items):
        cx = lx0 + 30 + colw * i + colw / 2
        draw_tracked(img, (cx, ly0 + 36), lab, font("MediumItalic", 38), 1.5, (20, 20, 20, 255))
        draw_tracked(img, (cx, ly0 + 74), small, font("Italic", 23), 1, (80, 80, 80, 255))
        c = COLORS[key]
        d.rectangle((lx0 + 30 + colw * i + 6, ly1 - 30, lx0 + 30 + colw * (i + 1) - 6, ly1 - 16), fill=c + (255,))

    if note:
        lines = ["Yaklaşık dağılım (nüfus payı).", "Kaynak: Osmanlı salnameleri,",
                 "C. Sax 1878 etnografya haritası,", "K. Karpat, Ottoman Population."]
        nx_ = lx0 + lw + 40
        for i, t in enumerate(lines):
            draw_tracked(img, (nx_, ly0 + 22 + i * 30), t, font("Italic", 23), 0.5, (55, 55, 55, 255),
                         anchor="lm")

    img.convert("RGB").save(out_png, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imza", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "balkanlar_1876.png"))
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--data", nargs="*")
    a = ap.parse_args()
    clusters = load_clusters(a.data)
    print(len(clusters), "küme")
    base = a.out.replace(".png", "_base.png")
    cat, owner = render_base(clusters, base, debug=a.debug)
    n = (cat > 0).sum()
    for k, c in enumerate(CATS, 1):
        print(f"  {c}: %{100 * (cat == k).sum() / max(n, 1):.1f} alan")
    overlay(base, a.out, imza=a.imza)
    os.remove(base)
    print("->", a.out)


if __name__ == "__main__":
    main()
