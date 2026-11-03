"""Harita motoru: projeksiyon çerçevesi, yükselti/rölyef, nüfus noktaları.

render2.py tarafından kullanılır. Bütün mesafeler metre, piksel koordinatları
(0,0) sol-üst köşe olacak şekilde.
"""
import json
import math
import os
import urllib.request

import numpy as np
import shapely
from scipy.ndimage import gaussian_filter, map_coordinates, distance_transform_edt
from pyproj import Transformer
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
CRS = "+proj=lcc +lat_1=40 +lat_2=44 +lat_0=42.4 +lon_0=22.6 +datum=WGS84 +units=m +no_defs"
TO_XY = Transformer.from_crs("EPSG:4326", CRS, always_xy=True)
TO_LL = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)


class Frame:
    """Haritanın projeksiyon penceresi ve piksel ızgarası."""

    def __init__(self, width_px, height_px, width_km, center_lonlat=(22.6, 42.4), shift_km=(0, 0)):
        self.W, self.H = int(width_px), int(height_px)
        cx, cy = TO_XY.transform(*center_lonlat)
        cx += shift_km[0] * 1000
        cy += shift_km[1] * 1000
        self.mpp = width_km * 1000 / self.W  # metre / piksel
        self.x0 = cx - self.W / 2 * self.mpp
        self.y1 = cy + self.H / 2 * self.mpp
        self.x1 = self.x0 + self.W * self.mpp
        self.y0 = self.y1 - self.H * self.mpp

    def xy_to_px(self, x, y):
        return (np.asarray(x) - self.x0) / self.mpp, (self.y1 - np.asarray(y)) / self.mpp

    def ll_to_px(self, lon, lat):
        x, y = TO_XY.transform(lon, lat)
        return self.xy_to_px(x, y)

    def px_grid(self, step=1.0):
        """Piksel merkezlerinin projeksiyon koordinatları (H/step, W/step)."""
        xs = self.x0 + (np.arange(0, self.W, step) + step / 2) * self.mpp
        ys = self.y1 - (np.arange(0, self.H, step) + step / 2) * self.mpp
        return np.meshgrid(xs, ys)


# ------------------------------------------------------------------ yükselti
DEM_Z = 8


def _tile_xy(lon, lat, z=DEM_Z):
    r = math.radians(lat)
    return (int((lon + 180) / 360 * 2 ** z),
            int((1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** z))


def dem_mosaic(bounds=(14.0, 36.6, 32.3, 48.0)):
    """AWS 'terrarium' yükselti karolarından mozaik (cache'lenir)."""
    d = os.path.join(CACHE, "dem")
    os.makedirs(d, exist_ok=True)
    npy, meta = os.path.join(d, "mosaic.npy"), os.path.join(d, "mosaic.json")
    if os.path.exists(npy):
        return np.load(npy), json.load(open(meta))
    x0, y0 = _tile_xy(bounds[0], bounds[3])
    x1, y1 = _tile_xy(bounds[2], bounds[1])
    M = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            p = os.path.join(d, f"{DEM_Z}_{x}_{y}.png")
            if not os.path.exists(p):
                urllib.request.urlretrieve(
                    f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{DEM_Z}/{x}/{y}.png", p)
            a = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
            M[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = \
                a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
    m = dict(x0=x0, y0=y0, z=DEM_Z)
    np.save(npy, M)
    json.dump(m, open(meta, "w"))
    return M, m


def dem_on_frame(frame, step=1.0):
    """Çerçevenin her pikseline yükselti (m), bilineer örnekleme."""
    M, m = dem_mosaic()
    X, Y = frame.px_grid(step)
    lon, lat = TO_LL.transform(X, Y)
    n = 2 ** m["z"]
    tx = (lon + 180) / 360 * n
    lr = np.radians(lat)
    ty = (1 - np.log(np.tan(lr) + 1 / np.cos(lr)) / np.pi) / 2 * n
    col = (tx - m["x0"]) * 256 - 0.5
    row = (ty - m["y0"]) * 256 - 0.5
    return map_coordinates(M, [row, col], order=1, mode="nearest").astype(np.float32)


def hillshade(elev, mpp, azimuth=315, altitude=40, z_factor=1.6):
    gy, gx = np.gradient(elev * z_factor, mpp)
    slope = np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    az, alt = math.radians(azimuth), math.radians(altitude)
    hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return np.clip(hs, 0, 1), slope


def multi_hillshade(elev, mpp):
    """Çok yönlü yumuşak rölyef (NW ağırlıklı)."""
    e = gaussian_filter(elev, 0.6)
    acc = 0
    for az, w in ((315, 0.55), (270, 0.2), (0, 0.15), (225, 0.10)):
        h, slope = hillshade(e, mpp, az, 42)
        acc = acc + w * h
    flat = math.sin(math.radians(42))
    return acc, slope, flat


# ------------------------------------------------------------------ geometri rasterı
def rasterize(geom, frame, step=1.0):
    X, Y = frame.px_grid(step)
    return shapely.contains_xy(geom, X.ravel(), Y.ravel()).reshape(X.shape)


# ------------------------------------------------------------------ nüfus noktaları
CATS = ("turk", "muslim_other", "christian")
DENS_KM2 = {"high": 55.0, "normal": 34.0, "low": 16.0}


def smooth_noise(rng, shape, sigma):
    n = gaussian_filter(rng.standard_normal(shape).astype(np.float32), sigma, mode="wrap")
    return (n - n.mean()) / (n.std() + 1e-9)


def cluster_population(c):
    p = c.get("population")
    if p:
        return float(p)
    r = float(c["radius_km"])
    return DENS_KM2.get(c.get("density", "normal"), 34.0) * math.pi * r * r * 0.85


def make_dots(clusters, frame, land_mask, elev, people_per_dot=250, seed=1876,
              grid_step=2.0, village_size=(2, 9), village_sigma_km=0.9):
    """Nokta yoğunluğu: her küme kendi nüfusunu kendi alanına dağıtır.

    Dönüş: x_px, y_px, kat (0 Türk, 1 diğer Müslüman, 2 Hristiyan)
    """
    rng = np.random.default_rng(seed)
    gH, gW = land_mask.shape  # land_mask zaten grid_step çözünürlüğünde
    cell_m = frame.mpp * grid_step
    # yerleşime elverişlilik: deniz 0, yüksek ve dik yerler az
    gy, gx = np.gradient(gaussian_filter(elev, 1.0), cell_m)
    slope = np.hypot(gx, gy)
    suit = 1.0 / (1.0 + (np.maximum(elev, 0) / 1500.0) ** 4)
    suit *= 1.0 / (1.0 + (slope / 0.30) ** 2)
    suit *= (elev < 2300)
    suit = suit * land_mask
    suit = gaussian_filter(suit.astype(np.float32), 0.6) * land_mask
    # her grup için mekânsal lekelenme alanı (köyler gruplaşır)
    patch = [np.exp(1.15 * (0.8 * smooth_noise(rng, (gH, gW), 7) + 0.6 * smooth_noise(rng, (gH, gW), 2.2)))
             for _ in CATS]
    xs, ys, ks = [], [], []
    for c in clusters:
        P = cluster_population(c)
        sh = np.array([max(0.0, float(c[k])) for k in CATS])
        if sh.sum() <= 0 or P <= 0:
            continue
        sh = sh / sh.sum()
        px, py = frame.ll_to_px(c["lon"], c["lat"])
        gxc, gyc = px / grid_step, py / grid_step
        r_cells = float(c["radius_km"]) * 1000 / cell_m
        R = int(math.ceil(1.7 * r_cells)) + 1
        i0, i1 = max(0, int(gyc) - R), min(gH, int(gyc) + R + 1)
        j0, j1 = max(0, int(gxc) - R), min(gW, int(gxc) + R + 1)
        if i1 <= i0 or j1 <= j0:
            continue
        II, JJ = np.mgrid[i0:i1, j0:j1]
        d = np.hypot(II + 0.5 - gyc, JJ + 0.5 - gxc) / max(r_cells, 0.5)
        kern = np.exp(-0.5 * (d / 0.78) ** 2) * (d < 1.7)
        base = kern * suit[i0:i1, j0:j1]
        if base.sum() <= 0:
            # kıyıda/kara dışında kalan küme: en yakın kara hücresine
            base = kern * land_mask[i0:i1, j0:j1]
            if base.sum() <= 0:
                continue
        for k in range(3):
            n_dots = P * sh[k] / people_per_dot
            n = int(n_dots) + (rng.random() < (n_dots - int(n_dots)))
            if n <= 0:
                continue
            w = (base * patch[k][i0:i1, j0:j1]).ravel()
            w = w / w.sum()
            # köyler: birkaç nokta bir arada
            nv = max(1, int(round(n / rng.uniform(*village_size))))
            cells = rng.choice(w.size, size=nv, p=w)
            vy = II.ravel()[cells] + rng.random(nv)
            vx = JJ.ravel()[cells] + rng.random(nv)
            owner = rng.integers(0, nv, size=n)
            sig = village_sigma_km * 1000 / cell_m
            dy = vy[owner] + rng.normal(0, sig, n)
            dx = vx[owner] + rng.normal(0, sig, n)
            xs.append(dx * grid_step)
            ys.append(dy * grid_step)
            ks.append(np.full(n, k, np.int8))
    x = np.concatenate(xs)
    y = np.concatenate(ys)
    k = np.concatenate(ks)
    # denize düşenleri en yakın karaya it
    gi = np.clip((y / grid_step).astype(int), 0, gH - 1)
    gj = np.clip((x / grid_step).astype(int), 0, gW - 1)
    wet = ~land_mask[gi, gj]
    if wet.any():
        _, (ni, nj) = distance_transform_edt(~land_mask, return_indices=True)
        x[wet] = (nj[gi[wet], gj[wet]] + rng.random(wet.sum())) * grid_step
        y[wet] = (ni[gi[wet], gj[wet]] + rng.random(wet.sum())) * grid_step
    order = rng.permutation(x.size)
    return x[order], y[order], k[order]
