#!/usr/bin/env python3
"""RUMELİ 1876 serisi — bölge yakın planları (2–6/8).

Ana posterle aynı görsel dil: gece rölyefi, ışık noktaları (1 nokta = 100 kişi),
1876 Osmanlı sınırı, sancak çubukları, kayıt kutuları, kısa anlatı, konum haritası.
İçerik (etiketler, şehirler, kutular, anlatı) seri/icerik_<anahtar>.json dosyasından okunur.

Kullanım: python3 seri.py tuna edirne ...   (boşsa hepsi)
"""
import argparse
import json
import math
import os
import re

import numpy as np
import shapely
import geopandas as gpd
from PIL import Image, ImageDraw, ImageFilter

import engine as E
import render as R
import poster as P
from poster import (Canvas, hx, COL, TINT, IV, IV2, MUTE, BRASS, BRASS_L, bs, bod, bar,
                    fmt_int, fmt_pct, largest_remainder, rasterize_pil, star8, log, W, H)

HERE = os.path.dirname(os.path.abspath(__file__))
SERI = os.path.join(HERE, "seri")
NONOTT = {"Sırbistan", "Karadağ", "Avusturya-Macaristan", "Yunanistan"}
MAP_TOP, MAP_BOT = 470, 2060
STRIP = (44, 2070, 2116, 2656)
TOTAL = 8

REGIONS = {
    "tuna": dict(n=2, center=(25.9, 43.75), width=640, name="Tuna Vilâyeti: Deliorman ve Dobruca", float=(90, 520, 1000, 1000),
                 focus=[("Tuna", None)]),
    "edirne": dict(n=3, center=(26.3, 41.55), width=520, name="Edirne Vilâyeti: Trakya ve Rodoplar", float=(90, 1640, 1000, 2040),
                   focus=[("Edirne", None), ("İstanbul", None), ("Selanik", ["Drama"])]),
    "makedonya": dict(n=4, center=(22.5, 40.85), width=480, name="Makedonya ve Teselya", float=(1440, 1660, 2080, 2040), loc=(1790, 1330, 2070, 1520),
                      focus=[("Selanik", None), ("Manastır", ["Manastır", "Serfice", "Görice"]),
                             ("Prizren", ["Üsküp"]), ("Yanya", ["Tırhala"])]),
    "arnavut": dict(n=5, center=(20.4, 41.15), width=560, name="Arnavutluk, Kosova ve Epir", float=(80, 1240, 700, 2030),
                    focus=[("İşkodra", None), ("Yanya", ["Yanya", "Ergiri", "Berat", "Preveze"]),
                           ("Prizren", ["Prizren", "Dibra", "Debre"]),
                           ("Manastır", ["Prizren", "Elbasan", "Görice"])]),
    "bosna": dict(n=6, center=(18.4, 43.9), width=470, name="Bosna-Hersek ve Yenipazar", float=(1520, 560, 2070, 1330),
                  focus=[("Bosna", None), ("Hersek", None)]),
}


_MASTER = None


def master_masks():
    """1876 Osmanlı alanı ve yabancı devlet alanı — 250 m'lik ana ızgarada bir kez hesaplanır."""
    global _MASTER
    if _MASTER is not None:
        return _MASTER
    F0 = E.Frame(4840, 3800, 1210, center_lonlat=(22.6, 42.25), shift_km=(30, 0))
    cache = os.path.join(E.CACHE, "ott_master_v1.npz")
    if os.path.exists(cache):
        z = np.load(cache)
        _MASTER = (F0, z["ott"], z["non"])
        return _MASTER
    countries, land, region, by = P.build_masks(F0)
    ott, lines, non = P.ottoman_mask(F0, region, by, load_cal(), 1.0)
    np.savez_compressed(cache, ott=ott, non=non)
    _MASTER = (F0, ott, non)
    return _MASTER


def sample_master(F, m0, F0):
    X, Y = F.px_grid(1.0)
    j = np.clip(((X - F0.x0) / F0.mpp).astype(int), 0, m0.shape[1] - 1)
    i = np.clip(((F0.y1 - Y) / F0.mpp).astype(int), 0, m0.shape[0] - 1)
    inside = (X >= F0.x0) & (X <= F0.x1) & (Y >= F0.y0) & (Y <= F0.y1)
    return m0[i, j] & inside


GLYPH_FIX = {"→": "›", "↔": "–", "←": "‹", "'": "’"}


def sanitize(x):
    """Yazı tiplerinde olmayan karakterleri değiştir (kutu/tofu çıkmasın)."""
    if isinstance(x, str):
        for a_, b_ in GLYPH_FIX.items():
            x = x.replace(a_, b_)
        return x
    if isinstance(x, list):
        return [sanitize(v) for v in x]
    if isinstance(x, dict):
        return {k: sanitize(v) for k, v in x.items()}
    return x


ALL_OTT = [("Tuna", None), ("Edirne", None), ("İstanbul", None), ("Selanik", None), ("Manastır", None),
           ("Prizren", None), ("Yanya", None), ("İşkodra", None), ("Bosna", None), ("Hersek", None)]
TURK = dict(series="RUMELİ TÜRKLERİ 1876", total=4)
REGIONS.update({
    "t_rodoplar": dict(n=1, center=(25.35, 41.45), width=300, name="Doğu Rodoplar ve Batı Trakya", focus=ALL_OTT,
                       float=(1440, 1640, 2080, 2040), **TURK),
    "t_deliorman": dict(n=2, center=(27.4, 44.0), width=380, name="Deliorman ve Dobruca", focus=ALL_OTT,
                        float=(90, 520, 980, 960), **TURK),
    "t_makedonya": dict(n=3, center=(22.9, 41.1), width=380, name="Makedonya Türkleri", focus=ALL_OTT,
                        float=(1440, 1620, 2080, 2040), **TURK),
    "t_trakya": dict(n=4, center=(27.3, 41.35), width=330, name="Edirne ve Doğu Trakya", focus=ALL_OTT,
                     float=(90, 1660, 1000, 2040), **TURK),
})


def areal_fill(F, x, y, k, area, sigma_km=6.0, step=2):
    """Boş alanları çevredeki yerleşimlerin çoğunluk grubuyla doldurur (etnografya haritası yöntemi).

    Dönüş: (H, W) int8 etiket (-1 = doldurulmaz), her grup için alan payı.
    Kural her grup için aynıdır: etrafı Türk köyleriyle çevrili boşluk Türk, Bulgar köyleriyle çevrili boşluk
    Hristiyan rengi alır.
    """
    from scipy.ndimage import gaussian_filter as gf, distance_transform_edt as edt
    h, w = H // step, W // step
    cnt = np.zeros((3, h, w), np.float32)
    xi = np.clip((x / step).astype(int), 0, w - 1)
    yi = np.clip((y / step).astype(int), 0, h - 1)
    for g in range(3):
        m = k == g
        np.add.at(cnt[g], (yi[m], xi[m]), 1.0)
    sig = sigma_km * 1000 / (F.mpp * step)
    D = np.stack([gf(cnt[g], sig) for g in range(3)])
    tot = D.sum(0)
    decided = tot > (0.6 / (2 * np.pi * sig * sig))
    lab = np.argmax(D, 0).astype(np.int8)
    if (~decided).any() and decided.any():
        _, (ii, jj) = edt(~decided, return_indices=True)
        lab = lab[ii, jj]
    # çoğunluk süzgeci: küçük adacıkları yumuşat
    oh = np.stack([gf((lab == g).astype(np.float32), 2.0e3 / (F.mpp * step) + 1.0) for g in range(3)])
    lab = np.argmax(oh, 0).astype(np.int8)
    full = np.repeat(np.repeat(lab, step, 0), step, 1)[:H, :W]
    out = np.where(area, full, -1).astype(np.int8)
    tot_px = max(1, (out >= 0).sum())
    shares = [100.0 * (out == g).sum() / tot_px for g in range(3)]
    return out, shares


def fill_layer(lab, fade, dim=None, spacing=11, lw=2.6):
    """Taralı alan katmanı (RGBA): grup renginde çapraz çizgiler + hafif ton."""
    Y, X = np.mgrid[0:H, 0:W]
    v = (X + Y) % spacing
    hatch = np.clip(lw / 2 + 0.5 - np.abs(v - spacing / 2), 0, 1).astype(np.float32)
    lay = np.zeros((H, W, 4), np.float32)
    for g in range(3):
        m = lab == g
        if not m.any():
            continue
        col = np.array(hx(COL[g])[:3], np.float32)
        lay[m, :3] = col
        lay[m, 3] = 0.20 + 0.55 * hatch[m]
    # grup sınırlarında ince koyu çizgi
    edge = np.zeros((H, W), bool)
    edge[:, 1:] |= (lab[:, 1:] != lab[:, :-1]) & (lab[:, 1:] >= 0) & (lab[:, :-1] >= 0)
    edge[1:, :] |= (lab[1:, :] != lab[:-1, :]) & (lab[1:, :] >= 0) & (lab[:-1, :] >= 0)
    lay[edge, :3] = (8, 10, 16)
    lay[edge, 3] = 0.55
    a = lay[..., 3] * np.clip(fade[:, 0], 0, 1)[:, None]
    if dim is not None:
        a = np.where(dim, a * 0.4, a)
    lay[..., 3] = a
    return Image.fromarray(np.clip(lay * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA")


def in_focus(c, focus):
    for vil, sans in focus:
        if c.get("vilayet") == vil and (sans is None or (c.get("sancak") or "") in sans):
            return True
    return False


def load_cal():
    cl = json.load(open(os.path.join(HERE, "data_cal", "clusters_calibrated.json"), encoding="utf-8"))
    for c in cl:
        s = np.array([max(0.0, float(c[k])) for k in E.CATS])
        c["shares"] = s / s.sum()
    return cl


def wrap(text, fnt, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def place_city_list(cv, F, cities, dimmed=()):
    d = cv.d
    order = sorted(cities, key=lambda c: c.get("tier", 3))
    for c in order:
        name, modern, lon, lat, tier = c["name"], c.get("modern") or None, c["lon"], c["lat"], int(c.get("tier", 3))
        x, y = F.ll_to_px(lon, lat)
        x, y = float(x), float(y)
        if not (70 < x < W - 70 and MAP_TOP + 10 < y < MAP_BOT - 10):
            continue
        dim = name in dimmed
        fnt = bar(40, "SemiBold") if tier == 1 else bar(31, "SemiBold") if tier == 2 else bar(24, "Medium")
        col = IV if tier == 1 else hx("#E1DACA") if tier == 2 else hx("#C9C2B4")
        if dim:
            col = col[:3] + (150,)
        mod_f = bar(22 if tier == 1 else 20, "Medium") if (modern and modern != name and tier <= 2) else None
        tw = fnt.getlength(name)
        th = fnt.size * 0.78
        mw = mod_f.getlength(modern) if mod_f else 0
        bw = max(tw, mw)
        bh = th + (mod_f.size + 2 if mod_f else 0)
        r = 8 if tier == 1 else 5 if tier == 2 else 3
        cands = [(x + r + 8, y + th / 2 - 2), (x - r - 8 - bw, y + th / 2 - 2), (x + r + 4, y - r - 4),
                 (x - r - 4 - bw, y + r + th + 4), (x - bw / 2, y - r - 6 - (bh - th)), (x - bw / 2, y + r + th + 4),
                 (x + r + 4, y + r + th + 4), (x - r - 4 - bw, y - r - 4)]
        if c.get("side") == "left":
            cands = [cands[1], cands[3], cands[7], cands[0]] + cands[2:]
        placed = None
        for lx, ly in cands:
            rect = (lx, ly - th, lx + bw, ly - th + bh)
            if cv.free(rect, pad=3) and cv.free((x - r - 2, y - r - 2, x + r + 2, y + r + 2), pad=0):
                placed = (lx, ly, rect)
                break
        if not placed:
            continue
        lx, ly, rect = placed
        if tier == 1:
            d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=IV, outline=hx("#05080D"), width=2)
        else:
            d.rectangle((x - r / 2 - 1, y - r / 2 - 1, x + r / 2 + 1, y + r / 2 + 1), fill=col, outline=hx("#05080D"))
        cv.halo((lx, ly), name, fnt, col, anchor="ls", rad=4)
        if mod_f:
            cv.halo((lx, ly + mod_f.size + 1), modern, mod_f, MUTE, anchor="ls", rad=3)
        cv.occupy(rect)
        cv.occupy((x - r - 2, y - r - 2, x + r + 2, y + r + 2))


def place_story(cv, F, labels):
    for lb in labels:
        t, sub, g = lb["text"], lb.get("sub") or "", int(lb.get("group", 3))
        px, py = F.ll_to_px(lb["lon"], lb["lat"])
        px, py = float(px), float(py)
        fnt = bar(32, "SemiBold")
        col = TINT[g] if g in TINT else hx("#B9C3D6")
        w = max(cv.tracked_w(t, fnt, 4), cv.tracked_w(sub, bar(20, "SemiBold"), 2) if sub else 0) + 10
        done = False
        for dy in (0, -36, 36, -72, 72, -108, 108):
            for dxx in (0, -60, 60, -120, 120):
                rect = (px + dxx - w / 2, py + dy - 30, px + dxx + w / 2, py + dy + 6 + (26 if sub else 0))
                if MAP_TOP < rect[1] and rect[3] < MAP_BOT and cv.free(rect, 2):
                    cv.halo((px + dxx, py + dy), t, fnt, col, anchor="ms", rad=5, track=4)
                    if sub:
                        cv.halo((px + dxx, py + dy + 26), sub, bar(20, "SemiBold"), col, anchor="ms", rad=4, track=2)
                    cv.occupy(rect)
                    done = True
                    break
            if done:
                break
        if not done:
            log("  etiket yerleşmedi:", t)


def locator(cv, box, F):
    """Küçük Balkan konum haritası; çerçevenin kapsadığı alan altın dikdörtgen."""
    x0, y0, x1, y1 = box
    countries = R.ne_layer("countries")
    G = countries.clip((14.5, 37.5, 30.5, 46.6)).to_crs(E.CRS)
    region = shapely.make_valid(R.data_region(countries))
    gx0, gy0, gx1, gy1 = E.TO_XY.transform(14.8, 37.8)[0], E.TO_XY.transform(14.8, 37.8)[1], \
        E.TO_XY.transform(30.0, 46.3)[0], E.TO_XY.transform(30.0, 46.3)[1]
    bx0, by0, bx1, by1 = region.bounds
    bx0, by0, bx1, by1 = bx0 - 30000, by0 - 30000, bx1 + 30000, by1 + 30000
    sc = min((x1 - x0) / (bx1 - bx0), (y1 - y0) / (by1 - by0))
    ox = x0 + ((x1 - x0) - (bx1 - bx0) * sc) / 2
    oy = y0 + ((y1 - y0) - (by1 - by0) * sc) / 2
    tp = lambda xs, ys: list(zip(ox + (np.asarray(xs) - bx0) * sc, oy + (by1 - np.asarray(ys)) * sc))
    S = 3
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)

    def poly(geom, fill):
        for p in (geom.geoms if hasattr(geom, "geoms") else [geom]):
            if p.geom_type != "Polygon" or p.area < 2e8:
                continue
            pts = [(u * S, v * S) for u, v in tp(*np.asarray(p.exterior.coords).T[:2])]
            ld.polygon(pts, fill=fill)

    for g in G.geometry:
        poly(g, (28, 34, 46, 255))
    poly(region, (52, 64, 86, 255))
    fx = [F.x0, F.x1, F.x1, F.x0, F.x0]
    fy = [F.y1 - MAP_BOT * F.mpp, F.y1 - MAP_BOT * F.mpp, F.y1 - MAP_TOP * F.mpp, F.y1 - MAP_TOP * F.mpp, F.y1 - MAP_BOT * F.mpp]
    ld.line([(u * S, v * S) for u, v in tp(fx, fy)], fill=BRASS_L, width=3 * S)
    lay = lay.resize((W, H), Image.LANCZOS)
    cv.img.alpha_composite(lay)


def callout_box(cv, x, y, w, c):
    d = cv.d
    big = c["big"]
    fb = bs(108)
    while fb.getlength(big) > w and fb.size > 40:
        fb = bs(fb.size - 2)
    d.text((x, y + 96), big, font=fb, fill=IV, anchor="ls")
    yy = y + 140
    f1, f2, f3 = bar(29, "SemiBold"), bar(24, "Medium"), bar(19, "Medium")
    for ln in wrap(c.get("line1", ""), f1, w)[:3]:
        d.text((x, yy), ln, font=f1, fill=IV, anchor="ls")
        yy += 35
    yy += 2
    for ln in wrap(c.get("line2", ""), f2, w)[:4]:
        d.text((x, yy), ln, font=f2, fill=IV2, anchor="ls")
        yy += 30
    yy += 10
    for ln in wrap(c.get("src", ""), f3, w)[:4]:
        d.text((x, yy), ln, font=f3, fill=MUTE, anchor="ls")
        yy += 24


def render_region(key, cfg, out_dir, ppd=100):
    reg = REGIONS[key]
    mpp = reg["width"] * 1000 / W
    shift = (0, -(H / 2 - (MAP_TOP + MAP_BOT) / 2) * mpp / 1000)
    F = E.Frame(W, H, reg["width"], center_lonlat=reg["center"], shift_km=shift)
    elev = E.dem_on_frame(F, z=9)
    countries, land, region, by = P.build_masks(F)
    landm = rasterize_pil(land, F, 1.0)
    regm = rasterize_pil(region, F, 1.0)
    regm2 = rasterize_pil(region, F, 2.0)
    elev2 = elev[::2, ::2][:regm2.shape[0], :regm2.shape[1]]
    cl_all = load_cal()
    F0, ott0, non0 = master_masks()
    ott1 = sample_master(F, ott0, F0) & regm
    non1 = sample_master(F, non0, F0)
    log(f"[{key}] maskeler")

    # yalnız çerçeveye yakın kümeler
    cx, cy = F.ll_to_px([c["lon"] for c in cl_all], [c["lat"] for c in cl_all])
    cx, cy = np.asarray(cx), np.asarray(cy)
    rpx = np.array([c["radius_km"] for c in cl_all]) * 1000 / F.mpp
    near = (cx > -2 * rpx - 50) & (cx < W + 2 * rpx + 50) & (cy > -2 * rpx - 50) & (cy < H + 2 * rpx + 50)
    cl = [c for c, n in zip(cl_all, near) if n]
    x, y, k, ci = E.make_dots(cl, F, regm2, elev2, people_per_dot=ppd, seed=1876, return_cluster=True)
    foc = np.array([in_focus(c, reg["focus"]) for c in cl])
    xi, yi = np.clip(x.astype(int), 0, W - 1), np.clip(y.astype(int), 0, H - 1)
    inside = ott1[yi, xi] & foc[ci]
    log(f"[{key}] {x.size} nokta ({inside.sum()} odakta)")

    fade = P.vfade(top0=150, topw=420, bot1=2160, botw=260)
    basef = P.base_image(F, elev, landm, regm, ott1) * (0.22 + 0.78 * fade[..., None])
    base = Image.fromarray(np.clip(basef * 255, 0, 255).astype(np.uint8)).convert("RGBA")
    base.alpha_composite(P.draw_rivers(F, regm, fade, under=True))
    fill_shares, fill_km2 = None, [0, 0, 0]
    if reg.get("fill", True):
        focus_area = np.zeros((H, W), bool)
        fpx = np.zeros(len(cl), bool)
        # odak alanı: odak kümelerin en yakın olduğu Osmanlı karası
        from scipy.spatial import cKDTree
        ccx, ccy = F.ll_to_px([c["lon"] for c in cl], [c["lat"] for c in cl])
        tree = cKDTree(np.c_[np.asarray(ccx), np.asarray(ccy)])
        gy_, gx_ = np.mgrid[0:H:4, 0:W:4]
        _, nn = tree.query(np.c_[gx_.ravel(), gy_.ravel()])
        fz_ = foc[nn].reshape(gy_.shape)
        focus_area = np.repeat(np.repeat(fz_, 4, 0), 4, 1)[:H, :W] & ott1
        lab, _ = areal_fill(F, x, y, k, ott1 & landm)
        fl_ = (lab >= 0) & focus_area
        fill_shares = [100.0 * ((lab == g) & fl_).sum() / max(1, fl_.sum()) for g in range(3)]
        fill_km2 = [((lab == g) & fl_).sum() * (F.mpp / 1000) ** 2 for g in range(3)]
        base.alpha_composite(fill_layer(lab, fade, dim=~focus_area))
        log(f"[{key}] alan payları (odak): Türk %{fill_shares[0]:.1f} · d.Müs %{fill_shares[1]:.1f} · Hr %{fill_shares[2]:.1f}")
    base.alpha_composite(P.dotted_borders(F, fade))
    img = P.render_dots(np.asarray(base.convert("RGB"), np.float32) / 255, x, y, k, inside,
                        radius=1.9, fade_y0=1990, fade_y1=2110, alpha_out=0.30)
    img.alpha_composite(P.draw_rivers(F, regm, fade, under=False))
    outside = shapely.union_all([by[a3] for a3 in ("ROU", "HUN", "SVN", "HRV", "SRB", "MNE", "AUT") if a3 in by])
    to_g = lambda geom: gpd.GeoSeries([geom], crs="EPSG:4326").to_crs(E.CRS).iloc[0]
    foreign = rasterize_pil(to_g(outside), F, 1.0) & ~regm
    foreign |= (regm & ~ott1 & non1)
    foreign = P.binary_opening(foreign, iterations=2) & landm & ~ott1
    fl, fdist = P.frontier_layer(ott1, foreign)
    fa = np.asarray(fl, np.float32).copy()
    fa[..., 3] *= np.clip(fade[:, 0], 0, 1)[:, None] ** 1.2
    img.alpha_composite(Image.fromarray(fa.astype(np.uint8), "RGBA"))
    log(f"[{key}] harita")

    # başlık arkası: haritayı yukarıda koyulaştır (başlık ve lejant okunur kalsın)
    yy_ = np.arange(H, dtype=np.float32)[:, None]
    shade_a = np.clip((MAP_TOP + 40 - yy_) / 150, 0, 1) * 0.93
    ov = np.zeros((H, W, 4), np.uint8)
    ov[..., :3] = (4, 7, 13)
    ov[..., 3] = (np.repeat(shade_a, W, 1) * 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(ov, "RGBA"))
    cv = Canvas(img)
    cv.occupy((0, 0, W, MAP_TOP - 6))
    cv.occupy(STRIP)
    cv.occupy((0, MAP_BOT - 6, W, H))
    FL = reg["float"]
    cv.occupy(FL)

    # ---- başlık
    d = cv.d
    d.line((140, 74, W / 2 - 30, 74), fill=BRASS, width=2)
    d.line((W / 2 + 30, 74, W - 140, 74), fill=BRASS, width=2)
    d.line((140, 80, W / 2 - 36, 80), fill=BRASS[:3] + (115,), width=1)
    d.line((W / 2 + 30, 80, W - 140, 80), fill=BRASS[:3] + (115,), width=1)
    kicker = cfg.get("kicker") or "OSMANLI KAYITLARINA GÖRE · 93 HARBİ ARİFESİ"
    kicker = re.sub(r"RUMELİ (TÜRKLERİ )?1876\s*·\s*\d+/\d+\s*·?\s*", "", kicker).strip(" ·") or "OSMANLI KAYITLARINA GÖRE · 93 HARBİ ARİFESİ"
    cv.tracked((W / 2, 146), P.tr_upper(kicker), bar(30, "SemiBold"), 8, BRASS, anchor="c")
    title = P.tr_upper(cfg.get("title") or reg["name"])
    ts = 170
    while bs(ts).getlength(title) > 1900:
        ts -= 2
    cv.halo((W / 2, 300), title, bs(ts), IV, anchor="ms", rad=8, strength=0.6)
    sub = cfg.get("subtitle") or "1876’da kim, nerede yaşıyordu?"
    ss = 52
    while bod(ss, 600, 11).getlength(sub) > 1900:
        ss -= 2
    cv.halo((W / 2, 376), sub, bod(ss, 600, 11), IV2, anchor="ms", rad=6, strength=0.6)
    items = [(0, "Türk"), (1, "Balkan Müslümanları"), (2, "Hristiyan")]
    f1, f2 = bar(34, "SemiBold"), bar(28, "Medium")
    unit = f"1 nokta = {ppd} kişi (≈ {ppd // 5} hane)" + ("  ·  taralı alan: çevredeki köylerin çoğunluğu" if reg.get("fill", True) else " · soluk: bölge dışı ya da 1876’da Osmanlı idaresi dışında")
    tot = sum(62 + f1.getlength(t) + 40 for _, t in items) + 26 + f2.getlength(unit)
    xx = W / 2 - tot / 2
    yb = 446
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for g, t in items:
        for (ox, oy) in ((0, 0), (14, -6), (26, 2), (12, 9), (36, -3)):
            cx_, cy_ = xx + 8 + ox, yb - 12 + oy
            gd.ellipse((cx_ - 9, cy_ - 9, cx_ + 9, cy_ + 9), fill=hx(COL[g], 120))
            d.ellipse((cx_ - 5, cy_ - 5, cx_ + 5, cy_ + 5), fill=hx(COL[g]))
        xx += 58
        d.text((xx, yb), t, font=f1, fill=TINT[g], anchor="ls")
        xx += f1.getlength(t) + 40
    d.ellipse((xx - 20, yb - 14, xx - 16, yb - 10), fill=BRASS)
    d.text((xx, yb), unit, font=f2, fill=MUTE, anchor="ls")
    cv.img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(4)))

    # ---- etiketler
    cities = cfg.get("cities") or []
    t12 = [c for c in cities if int(c.get("tier", 3)) <= 2]
    place_city_list(cv, F, t12, dimmed=("Belgrad", "Çetine", "Bükreş"))
    place_story(cv, F, cfg.get("story_labels") or [])
    place_city_list(cv, F, [c for c in cities if int(c.get("tier", 3)) > 2], dimmed=("Belgrad", "Çetine"))

    # ---- alt şerit
    st = Image.new("RGBA", (STRIP[2] - STRIP[0], STRIP[3] - STRIP[1]), (4, 6, 10, int(255 * 0.86)))
    cv.img.alpha_composite(st, (STRIP[0], STRIP[1]))
    d = cv.d
    d.line((STRIP[0], STRIP[1], STRIP[2], STRIP[1]), fill=BRASS, width=2)
    star8(d, W / 2, STRIP[1], 10, BRASS, 2, fill=hx("#05080D"))
    # sancak çubukları — çubuk: harita modeli; büyük rakam: Osmanlı kaydı varsa kayıt, yoksa model
    bars = cfg.get("bars") or []
    cv.tracked((80, 2118), cfg.get("bars_head") or "SANCAKLARA GÖRE · 1876", bar(24, "SemiBold"), 4, BRASS)
    fl_ = bar(18, "Medium")
    t1_ = "çubuk: harita modeli ·"
    d.text((80, 2146), t1_, font=fl_, fill=MUTE, anchor="ls")
    dx_ = 80 + fl_.getlength(t1_) + 10
    d.polygon([(dx_ + 6, 2131), (dx_ + 12, 2137), (dx_ + 6, 2143), (dx_, 2137)], fill=IV)
    d.text((dx_ + 18, 2146), "Osmanlı kaydı · büyük rakam: Müslüman %", font=fl_, fill=MUTE, anchor="ls")
    bx0, bw = 290, 460
    y_ = 2178
    pitch = 52
    rows = []
    for b in bars:
        m = np.array([c.get("vilayet") == b["vilayet"] and ((c.get("sancak") or "") in b["sancak"]) for c in cl_all])
        if not m.any():
            log("  çubuk boş:", b["label"])
            continue
        G = np.array([[c["population"] * c[kk] / 100 for kk in E.CATS] for c in np.array(cl_all, dtype=object)[m]]).sum(0)
        rows.append((b, G))
    rows = rows[:8]
    if rows:
        d.line((bx0 + bw / 2, y_ - 6, bx0 + bw / 2, y_ + pitch * (len(rows) - 1) + 34), fill=BRASS[:3] + (90,), width=1)
        d.text((bx0 + bw / 2 + 4, y_ + pitch * (len(rows) - 1) + 50), "%50", font=bar(16, "Medium"), fill=BRASS, anchor="ls")
    for i, (b, G) in enumerate(rows):
        yy = y_ + i * pitch
        hb = 30
        nm = b["label"]
        fn = bar(25, "SemiBold")
        while fn.getlength(nm) > bx0 - 92 and fn.size > 18:
            fn = bar(fn.size - 1, "SemiBold")
        d.text((80, yy + hb - 5), nm, font=fn, fill=IV, anchor="ls")
        p = largest_remainder(G)
        pint = largest_remainder(G, nd=0)
        xs_ = bx0
        for gi in range(3):
            wseg = bw * p[gi] / 100
            if wseg > 0.5:
                d.rectangle((xs_, yy, xs_ + max(0, wseg - 2), yy + hb), fill=hx(COL[gi]))
                if wseg >= 40:
                    d.text((xs_ + wseg / 2 - 1, yy + hb - 6), f"{pint[gi]:.0f}", font=bar(20, "SemiBold"), fill=hx("#05080D"), anchor="ms")
            xs_ += wseg
        rec = float(b.get("record_muslim_pct") or 0)
        lab = re.sub(r"(?i)kayıt\s*", "", (b.get("record_label") or "")).strip()
        xn = bx0 + bw + 14
        if rec > 0:
            xr = bx0 + bw * rec / 100
            d.rectangle((xr - 2, yy - 4, xr + 2, yy + hb + 4), fill=IV)
            d.polygon([(xr, yy - 14), (xr + 5, yy - 9), (xr, yy - 4), (xr - 5, yy - 9)], fill=IV)
            d.text((xn, yy + hb - 1), fmt_pct(rec), font=bs(36), fill=IV, anchor="ls")
            d.text((xn + 108, yy + 13), f"kayıt {lab}".strip(), font=bar(17, "SemiBold"), fill=IV2, anchor="ls")
            d.text((xn + 108, yy + 33), f"model {fmt_pct(p[0] + p[1])}", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
        else:
            d.text((xn, yy + hb - 1), fmt_pct(p[0] + p[1]), font=bs(36), fill=IV, anchor="ls")
            d.text((xn + 108, yy + 13), "harita modeli", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
        d.text((xn + 108, yy + 33 + (0 if rec <= 0 else 0)), "" if rec > 0 else f"{fmt_int(G.sum())} kişi", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    # kutular: üç sütun
    d.line((1022, 2100, 1022, 2590), fill=BRASS[:3] + (90,), width=1)
    cos = (cfg.get("callouts") or [])[:3]
    colw = (2086 - 1052) / 3
    for i, c in enumerate(cos):
        x_ = 1052 + i * colw
        if i:
            d.line((x_ - 16, 2120, x_ - 16, 2570), fill=BRASS[:3] + (60,), width=1)
        callout_box(cv, x_, 2110, colw - 34, c)
    # yüzen anlatı paneli (haritanın boş alanında)
    x0f, y0f, x1f, y1f = FL
    ov = Image.new("RGBA", (int(x1f - x0f), int(y1f - y0f)), (4, 6, 10, int(255 * 0.80)))
    cv.img.alpha_composite(ov, (int(x0f), int(y0f)))
    d = cv.d
    d.line((x0f, y0f, x1f, y0f), fill=BRASS, width=2)
    d.rectangle((x0f, y0f - 3, x0f + 8, y0f + 5), fill=BRASS)
    nar = cfg.get("narrative") or []
    pw, ph = x1f - x0f, y1f - y0f
    sep_loc = reg.get("loc")
    wide = pw >= 800 and not sep_loc
    loc_w = 300 if wide else min(300, pw - 48)
    loc_h = 190 if wide else 150

    def fit(text_w, avail_h):
        fz = 38
        while True:
            fnar = bod(fz, 600, 11)
            lh = int(fz * 1.32)
            lines = []
            for sent in nar:
                lines += wrap(sent, fnar, text_w)
                lines.append("")
            need = sum(lh if ln else 10 for ln in lines[:-1]) + int(fz * 0.3)
            if need <= avail_h or fz <= 20:
                return fz, fnar, lh, lines, need
            fz -= 1

    stat_h = 70 if (reg.get("fill", True) and reg.get("series")) else 0
    ph = ph - stat_h
    if wide:
        fz, fnar, lh, lines, need = fit(pw - 48 - loc_w - 30, ph - 104)
        show_loc = True
    elif sep_loc:
        fz, fnar, lh, lines, need = fit(pw - 48, ph - 104)
        show_loc = True
    else:
        fz, fnar, lh, lines, need = fit(pw - 48, ph - 84 - loc_h - 70)
        show_loc = need <= ph - 84 - loc_h - 70
        if not show_loc:
            fz, fnar, lh, lines, need = fit(pw - 48, ph - 104)
    cv.tracked((x0f + 24, y0f + 42), "1876’DA BU TOPRAKLAR", bar(20, "SemiBold"), 4, BRASS)
    yy = y0f + 84
    for ln in lines:
        if ln:
            d.text((x0f + 24, yy), ln, font=fnar, fill=IV2, anchor="ls")
            yy += lh
        else:
            yy += 10
    if fill_shares is not None and reg.get("series"):
        yy += 6
        d.line((x0f + 24, yy - 18, x0f + 24 + 120, yy - 18), fill=BRASS[:3] + (120,), width=1)
        st_ = f"≈ {fmt_int(round(fill_km2[0], -2))} km² Türk çoğunluklu toprak"
        d.text((x0f + 24, yy + 12), st_, font=bar(28, "SemiBold"), fill=TINT[0], anchor="ls")
        d.text((x0f + 24, yy + 40), "bu haritadaki kırmızı taralı alan · harita modeli", font=bar(18, "Medium"), fill=MUTE, anchor="ls")
        yy += 50
    if show_loc:
        if sep_loc:
            lb = sep_loc
            ov2 = Image.new("RGBA", (int(lb[2] - lb[0] + 20), int(lb[3] - lb[1] + 50)), (4, 6, 10, 200))
            cv.img.alpha_composite(ov2, (int(lb[0] - 10), int(lb[1] - 10)))
        elif wide:
            lb = (x1f - 24 - loc_w, y0f + 70, x1f - 24, y0f + 70 + loc_h)
        else:
            lb = (x0f + 24, y1f - 24 - loc_h, x0f + 24 + loc_w, y1f - 24)
        locator(cv, lb, F)
        d = cv.d
        cy_ = lb[3] + 24 if (wide or sep_loc) else lb[1] - 12
        d.text((lb[0], cy_), "KONUM · altın çerçeve: bu haritanın alanı", font=bar(17, "Medium"), fill=MUTE, anchor="ls")

    P.lat_ticks(cv, F)
    P.frame_ornament(cv)
    P.series_tag(cv, f"{reg['n']}/{reg.get('total', TOTAL)}", prefix=reg.get("series", "RUMELİ 1876"))
    d = cv.d
    src = cfg.get("sources_line") or ""
    l2 = ("Yöntem: Osmanlı salname/sayım verilerine dayalı bölge kümeleri (ana poster ile aynı veri) · nokta yerleri temsilîdir · "
          "erkek sayımları ×2 · Yahudiler gösterilmedi · Tatar/Nogay = Türk")
    flines = []
    for t in (src, l2):
        if t:
            flines += wrap(t, bar(17, "Medium"), 1940)
    flines = flines[:3]
    y_f = 2645 - 20 * (len(flines) - 1)
    for i, t in enumerate(flines):
        d.text((W / 2, y_f + i * 20), t, font=bar(17, "Medium"), fill=MUTE, anchor="ms")

    out = cv.img.convert("RGB")
    arr = np.asarray(out, np.int16) + np.random.default_rng(7).integers(-1, 2, (H, W, 1))
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    stem = os.path.join(out_dir, f"{reg['n']:02d}_{key}")
    out.save(stem + ".png", optimize=True)
    out.resize((1080, 1350), Image.LANCZOS).save(stem + "_ig.jpg", quality=95, subsampling=0)
    log(f"[{key}] -> {stem}.png")


def default_cfg(key):
    reg = REGIONS[key]
    cities = [dict(name=n, modern=m or "", lon=lo, lat=la, tier=t) for lst, t in ((P.T1, 1), (P.T2, 2), (P.T3, 3))
              for (n, m, lo, la) in lst]
    cl = load_cal()
    bars = []
    seen = []
    for c in cl:
        if in_focus(c, reg["focus"]):
            k_ = (c["vilayet"], c.get("sancak") or "")
            if k_ not in seen:
                seen.append(k_)
    for vil, san in seen[:8]:
        bars.append(dict(label=san, vilayet=vil, sancak=[san], record_muslim_pct=0, record_label=""))
    return dict(title=reg["name"], cities=cities, bars=bars, story_labels=[], callouts=[], narrative=[])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--out", default=os.path.join(HERE, "cikti", "seri"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for key in (a.keys or list(REGIONS)):
        p = os.path.join(SERI, f"icerik_{key}.json")
        cfg = sanitize(json.load(open(p, encoding="utf-8"))) if os.path.exists(p) else default_cfg(key)
        render_region(key, cfg, a.out)


if __name__ == "__main__":
    main()
