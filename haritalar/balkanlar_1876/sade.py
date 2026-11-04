#!/usr/bin/env python3
"""RUMELİ 1876 — sade harita tasarımı (Türk yurdu haritalarıyla aynı görsel dil).

Kurallar (bütün haritalarda aynı):
  * Topluluklar adıyla: Türk, Pomak, Arnavut, Boşnak, Torbeş, Çerkes, Müslüman Roman; Bulgar, Rum, Sırp, Hırvat …
  * Alan (boşluk kalmaz): köylerin en az %40'ı Türk ise Türk yurdu (kırmızı tarama + parlak sınır);
    en az %40'ı Müslüman ise en kalabalık Müslüman topluluğun rengi; diğer yerler yerel çoğunluk.
    Boşluklar çevresindeki karar verilmiş alanın rengini alır.
  * 1876'da Osmanlı idaresi dışındaki devletler (Sırbistan, Karadağ, Yunanistan, Avusturya) soluk tonla.
  * Noktalar küçük ve temsilîdir.

Kullanım: python3 sade.py [genel tuna edirne makedonya arnavut bosna]
Çıktı: cikti/seri/NN_<anahtar>.png ve _ig.jpg (1080x1350)
"""
import argparse
import json
import os

import numpy as np
import shapely
import geopandas as gpd
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, distance_transform_edt
from scipy.spatial import cKDTree

import engine as E
import poster as P
import seri as S
import topluluk as T
from poster import Canvas, hx, bs, bod, bar, fmt_int, fmt_pct, rasterize_pil, log, W, H

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#0A0E14"
IV, IV2, MUTE, BRASS = hx("#F1E9D8"), hx("#DED6C6"), hx("#97A1B3"), hx("#B89B5E")
MAP_TOP, MAP_BOT = 470, 2250
NG = T.NG

SERIES = "RUMELİ 1876"
TOTAL = 8
POSTS = {
    "genel": dict(n=1, center=(22.55, 42.1), width=1150, ppd=250, sigma_km=8.0, smooth_km=4.0, focus=None),
    "tuna": dict(n=2, center=(25.95, 43.3), **{k: S.REGIONS["tuna"][k] for k in ("width", "focus")}),
    "edirne": dict(n=3, **{k: S.REGIONS["edirne"][k] for k in ("center", "width", "focus")}),
    "makedonya": dict(n=4, **{k: S.REGIONS["makedonya"][k] for k in ("center", "width", "focus")}),
    "arnavut": dict(n=5, **{k: S.REGIONS["arnavut"][k] for k in ("center", "width", "focus")}),
    "bosna": dict(n=6, **{k: S.REGIONS["bosna"][k] for k in ("center", "width", "focus")}),
}
FOREIGN_A3 = ("ROU", "HUN", "SVN", "HRV", "SRB", "MNE", "AUT")


def hf(h):
    return np.array(hx(h)[:3], np.float32) / 255


def rule_text(ppd):
    return (f"Kırmızı taralı alan: Türk yurdu (köylerin en az %{int(T.TURK_RULE * 100)}’ı Türk) · köylerin en az "
            f"%{int(T.MUSLIM_RULE * 100)}’ı Müslümansa en kalabalık Müslüman topluluğun rengi · diğer yerler yerel çoğunluk · "
            f"1 nokta = {ppd} kişi")


# ------------------------------------------------------------------ katmanlar
def fill_alpha(g):
    """Alan opaklığı: Türk taralı; Müslüman topluluklar ve diğer Hristiyan daha belirgin (gri görünmesin)."""
    if g == 0:
        return 0.50
    if g < T.NMUS or g == T.IDX["hdiger"]:
        return 0.42
    return 0.27


def swatch_rgb(g, bg="#1A212C"):
    """Lejant kutusu: alanın haritada göründüğü renk (koyu rölyef üstünde)."""
    a = fill_alpha(g)
    c = np.array(hx(T.COL[g])[:3], float) * a + np.array(hx(bg)[:3], float) * (1 - a)
    return tuple(int(v) for v in c)


def fill_image(lab, weak=None, spacing=13, lw=2.4):
    """Türk yurdu: kırmızı + tarama + parlak sınır. Diğer topluluklar: düz soluk ton.
    weak: (H,W) float çarpan (ör. Osmanlı dışı 0.45, odak dışı 0.6)."""
    Y, X = np.mgrid[0:H, 0:W]
    v = (X - Y) % spacing
    hatch = np.clip(lw / 2 + 0.5 - np.abs(v - spacing / 2), 0, 1).astype(np.float32)
    lay = np.zeros((H, W, 4), np.float32)
    for g in range(NG):
        m = lab == g
        if not m.any():
            continue
        lay[m, :3] = np.array(hx(T.COL[g])[:3], np.float32)
        lay[m, 3] = (fill_alpha(0) + 0.30 * hatch[m]) if g == 0 else fill_alpha(g)
    tm = lab == 0
    if tm.any():
        d_in = distance_transform_edt(tm)
        d_out = distance_transform_edt(~tm)   # yalnız Türk yurdunun gerçek sınırı (kıyılar değil)
        edge = np.clip(2.0 - np.where(tm, d_in, d_out), 0, 1) * (lab >= 0)
        lay[..., :3] = lay[..., :3] * (1 - edge[..., None]) + np.array([255, 110, 125], np.float32) * edge[..., None]
        lay[..., 3] = np.maximum(lay[..., 3], edge * 0.95)
    if weak is not None:
        lay[..., 3] *= weak
    return Image.fromarray(np.clip(lay * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA")


def draw_dots(img, x, y, k, alpha, r=1.55):
    S_ = 3
    rr = r * S_
    lay = Image.new("RGBA", (W * S_, H * S_), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    order = np.random.default_rng(1876).permutation(x.size)
    for i in order:
        g = int(k[i])
        xa, ya = x[i] * S_, y[i] * S_
        d.ellipse((xa - rr, ya - rr, xa + rr, ya + rr), fill=hx(T.TINT[g])[:3] + (int(alpha[i]),))
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))


def _lw(f, row):
    return sum(46 + f.getlength(T.NAMES[g]) + 30 for g in row) - 30


def legend_two_rows(groups, maxw=1980):
    return _lw(bar(25, "SemiBold"), groups) > maxw


def legend(d, groups, y0, maxw=1980):
    """Tek satır; sığmazsa Müslüman ve Hristiyan iki satır. Son satırın y'sini döndürür."""
    width = _lw

    f1 = bar(30, "SemiBold")
    while width(f1, groups) > maxw and f1.size > 25:
        f1 = bar(f1.size - 1, "SemiBold")
    rows = [groups] if width(f1, groups) <= maxw else [[g for g in groups if g < T.NMUS], [g for g in groups if g >= T.NMUS]]
    if len(rows) > 1:
        f1 = bar(30, "SemiBold")
    yb = y0 - (12 if len(rows) > 1 else 0)
    step_ = 40 if len(rows) > 1 else 44
    for row in rows:
        x0 = W / 2 - width(f1, row) / 2
        for g in row:
            if g == 0:
                d.rectangle((x0, yb - 26, x0 + 32, yb - 2), fill=swatch_rgb(0))
                for o in range(-24, 33, 8):          # haritadaki gibi '\' tarama, kutuya kırpılmış
                    t0, t1 = max(1, -o), min(23, 31 - o)
                    if t0 < t1:
                        d.line((x0 + o + t0, yb - 26 + t0, x0 + o + t1, yb - 26 + t1), fill=(255, 179, 188), width=2)
                d.rectangle((x0, yb - 26, x0 + 32, yb - 2), outline=hx("#FF6E7D"), width=2)
            else:
                d.rectangle((x0, yb - 26, x0 + 32, yb - 2), fill=swatch_rgb(g))
                d.ellipse((x0 + 11, yb - 19, x0 + 21, yb - 9), fill=hx(T.TINT[g]))
            d.text((x0 + 44, yb), T.NAMES[g], font=f1, fill=hx(T.TINT[g]), anchor="ls")
            x0 += 46 + f1.getlength(T.NAMES[g]) + 30
        yb += step_
    return yb - step_


# ------------------------------------------------------------------ çizim
def render_simple(spec, cfg, stem, cols_fn, extra_labels=None):
    """spec: center, width, ppd, n, total, series, focus (None = tüm Osmanlı), sigma_km, smooth_km.
    cfg: title, subtitle, cities, story_labels, line, sources_line.
    cols_fn(st) -> [(büyük, satır1, satır2), ...] (alt şerit; en çok 3)."""
    ppd = spec.get("ppd", 100)
    mpp = spec["width"] * 1000 / W
    shift = (0, -(H / 2 - (MAP_TOP + MAP_BOT) / 2) * mpp / 1000)
    F = E.Frame(W, H, spec["width"], center_lonlat=spec["center"], shift_km=shift)
    elev = E.dem_on_frame(F, z=9 if spec["width"] <= 700 else 8)
    countries, land, region, by = P.build_masks(F)
    landm = rasterize_pil(land, F, 1.0)
    regm = rasterize_pil(region, F, 1.0)
    regm2 = rasterize_pil(region, F, 2.0)
    elev2 = elev[::2, ::2][:regm2.shape[0], :regm2.shape[1]]
    F0, ott0, non0 = S.master_masks()
    ott1 = S.sample_master(F, ott0, F0) & regm
    non1 = S.sample_master(F, non0, F0)

    cl_all = T.split_named(S.load_cal(), quiet=True)
    cx, cy = F.ll_to_px([c["lon"] for c in cl_all], [c["lat"] for c in cl_all])
    cx, cy = np.asarray(cx), np.asarray(cy)
    rpx = np.array([c["radius_km"] for c in cl_all]) * 1000 / F.mpp
    near = (cx > -2 * rpx - 60) & (cx < W + 2 * rpx + 60) & (cy > -2 * rpx - 60) & (cy < H + 2 * rpx + 60)
    cl = [c for c, n in zip(cl_all, near) if n]   # İstanbul haritada görünür, hesaplara katılmaz
    x, y, k, ci = E.make_dots(cl, F, regm2, elev2, people_per_dot=ppd, seed=1876, return_cluster=True, cats=T.CATS,
                              village_sigma_km=0.6 if ppd <= 100 else 0.9)
    xi, yi = np.clip(x.astype(int), 0, W - 1), np.clip(y.astype(int), 0, H - 1)
    ott_d = ott1[yi, xi]
    focus = spec.get("focus")
    foc_c = np.array([True if focus is None else S.in_focus(c, focus) for c in cl])
    foc_d = foc_c[ci]
    inside = ott_d & foc_d
    ist_c = np.array([c.get("vilayet") in T.NO_STATS for c in cl])
    inside_st = inside & ~ist_c[ci]          # istatistik: İstanbul hariç
    log(f"[{stem}] {x.size} nokta ({inside.sum()} odakta)")

    # odak alanı (piksel): en yakın kümenin odak bayrağı
    if focus is None:
        focus_px = np.ones((H, W), bool)
    else:
        ccx, ccy = F.ll_to_px([c["lon"] for c in cl], [c["lat"] for c in cl])
        tree = cKDTree(np.c_[np.asarray(ccx), np.asarray(ccy)])
        gy_, gx_ = np.mgrid[0:H:4, 0:W:4]
        _, nn = tree.query(np.c_[gx_.ravel(), gy_.ravel()])
        focus_px = np.repeat(np.repeat(foc_c[nn].reshape(gy_.shape), 4, 0), 4, 1)[:H, :W]

    # ---- altlık: sade, koyu rölyef
    hs, slope, flat = E.multi_hillshade(elev, F.mpp)
    shade = gaussian_filter(np.clip(hs / flat, 0, 1.6) / 1.6, 0.6)
    d_sea = distance_transform_edt(~landm) * F.mpp / 1000
    coast = np.exp(-d_sea / 8.0)[..., None]
    img = hf("#06090E") * (1 - coast) + hf("#0C1420") * coast
    lo, hi = hf("#0E131B"), hf("#232B37")
    img = np.where(landm[..., None], lo + (hi - lo) * shade[..., None] ** 1.2, img)
    base = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8)).convert("RGBA")

    # ---- alan: bütün veri alanı dolar (Osmanlı dışı soluk, odak dışı yarı soluk)
    area = regm & landm
    dexp = T.expected_field(F, cl, regm2, elev2, ppd)
    lab = T.yurt_labels(F, x, y, k, area, sigma_km=spec.get("sigma_km", max(2.6, spec["width"] / 100)),
                        smooth_km=spec.get("smooth_km", 1.6 if spec["width"] <= 300 else 2.4), dexp=dexp)
    weak = np.ones((H, W), np.float32)
    ff = gaussian_filter(focus_px.astype(np.float32), 4)
    weak[ott1] = 0.62 + 0.38 * ff[ott1]
    weak[~ott1] = 0.6
    base.alpha_composite(fill_image(lab, weak=weak))
    fade = np.ones((H, 1), np.float32)
    base.alpha_composite(P.draw_rivers(F, regm, fade, under=False))
    alpha = np.where(inside, 235, np.where(ott_d, 120, 70))
    draw_dots(base, x, y, k, alpha, r=1.55 if ppd <= 100 else 1.45)
    outside = shapely.union_all([by[a3] for a3 in FOREIGN_A3 if a3 in by])
    to_g = lambda geom: gpd.GeoSeries([geom], crs="EPSG:4326").to_crs(E.CRS).iloc[0]
    foreign = rasterize_pil(to_g(outside), F, 1.0) & ~regm
    foreign |= (regm & ~ott1 & non1)
    foreign = P.binary_opening(foreign, iterations=2) & landm & ~ott1
    if foreign.any():
        fl, _ = P.frontier_layer(ott1, foreign)
        base.alpha_composite(fl)

    # ---- istatistik (odak + Osmanlı; İstanbul ve Ege adaları hariç)
    px_km2 = (F.mpp / 1000) ** 2
    nost_c = np.array([c.get("vilayet") in T.NO_STATS for c in cl])
    if nost_c.any():
        ccx2, ccy2 = F.ll_to_px([c["lon"] for c in cl], [c["lat"] for c in cl])
        tree2 = cKDTree(np.c_[np.asarray(ccx2), np.asarray(ccy2)])
        gy2, gx2 = np.mgrid[0:H:4, 0:W:4]
        _, nn2 = tree2.query(np.c_[gx2.ravel(), gy2.ravel()])
        nost_px = np.repeat(np.repeat(nost_c[nn2].reshape(gy2.shape), 4, 0), 4, 1)[:H, :W]
    else:
        nost_px = np.zeros((H, W), bool)
    zone = ott1 & focus_px & ~nost_px & (lab >= 0)
    km2 = {g: float(((lab == g) & zone).sum() * px_km2) for g in range(NG)}
    tm = (lab == 0) & zone
    in_t = tm[yi, xi] & inside_st
    cnt_t = np.bincount(k[in_t], minlength=NG).astype(float)
    tp = 100 * cnt_t / max(1, cnt_t.sum())
    allc = np.bincount(k[inside_st], minlength=NG).astype(float)
    allp = 100 * allc / max(1, allc.sum())
    st = dict(km2_turk=km2[0], km2_muslim=sum(km2[g] for g in range(T.NMUS)), km2_all=float(zone.sum() * px_km2),
              turk_in_yurt=float(tp[0]), muslim_in_yurt=float(tp[:T.NMUS].sum()),
              shares=dict(zip(T.NAMES, allp.tolist())), muslim=float(allp[:T.NMUS].sum()),
              people=float(allc.sum() * ppd), people_yurt=float(cnt_t.sum() * ppd),
              km2_by=dict(zip(T.NAMES, [km2[g] for g in range(NG)])))
    # lejant: görünen bantta (başlık ve alt şerit hariç) nokta payı ya da görünür alanı yeterli olan topluluklar
    vis_d = inside & (y > MAP_TOP) & (y < MAP_BOT)
    visp = 100 * np.bincount(k[vis_d], minlength=NG) / max(1, vis_d.sum())
    vlab = lab[MAP_TOP:MAP_BOT]
    vis_km2 = np.bincount(vlab[vlab >= 0].ravel(), minlength=NG) * px_km2
    vis_min = min(0.003 * max(1.0, vis_km2.sum()), 200.0)
    present = [g for g in range(NG) if g == 0 or visp[g] >= spec.get("legend_min", 0.6) or vis_km2[g] >= vis_min]
    log(f"[{stem}] Türk yurdu ≈{km2[0]:,.0f} km² (içinde Türk %{tp[0]:.1f}, Müslüman %{tp[:T.NMUS].sum():.1f}) · "
        f"Müslüman topluluk alanı ≈{st['km2_muslim']:,.0f} km² / {st['km2_all']:,.0f} km²")
    log(f"[{stem}] topluluklar: " + ", ".join(f"{T.NAMES[g]} %{allp[g]:.1f}" for g in present))

    # ---- başlık arkası ve alt şerit koyulaştır
    yy = np.arange(H, dtype=np.float32)[:, None]
    top_ = MAP_TOP + (36 if legend_two_rows(present) else 0)
    a_top = np.clip((top_ + 30 - yy) / 110, 0, 1) * 0.94
    a_bot = np.clip((yy - (MAP_BOT - 30)) / 90, 0, 1) * 0.94
    ov = np.zeros((H, W, 4), np.uint8)
    ov[..., :3] = hx(INK)[:3]
    ov[..., 3] = (np.repeat(np.maximum(a_top, a_bot), W, 1) * 255).astype(np.uint8)
    base.alpha_composite(Image.fromarray(ov, "RGBA"))
    cv = Canvas(base)
    cv.occupy((0, 0, W, MAP_TOP - 4))
    cv.occupy((0, MAP_BOT - 4, W, H))
    d = cv.d

    # ---- başlık, lejant, kural
    t = P.tr_upper(cfg.get("title") or "")
    ts = 156
    while bs(ts).getlength(t) > 1900:
        ts -= 2
    d.text((W / 2, 238), t, font=bs(ts), fill=IV, anchor="ms")
    sub = cfg.get("subtitle") or ""
    ss = 46
    while bod(ss, 600, 11).getlength(sub) > 1900:
        ss -= 2
    d.text((W / 2, 316), sub, font=bod(ss, 600, 11), fill=IV2, anchor="ms")
    y_last = legend(d, present, 384)
    rt = rule_text(ppd)
    fr = bar(23, "Medium")
    while fr.getlength(rt) > 1980 and fr.size > 17:
        fr = bar(fr.size - 1, "Medium")
    yr = y_last + 46
    d.text((W / 2, yr), rt, font=fr, fill=MUTE, anchor="ms")
    cv.occupy((0, MAP_TOP - 10, W, yr + 12))

    # ---- etiketler
    S.MAP_TOP, S.MAP_BOT = MAP_TOP, MAP_BOT
    tints = {i: hx(c) for i, c in enumerate(T.TINT)}
    cities = cfg.get("cities") or []
    S.place_city_list(cv, F, [c for c in cities if int(c.get("tier", 3)) == 1], dimmed=("Belgrad", "Çetine", "Bükreş"))
    if extra_labels:
        extra_labels(cv, F)
    S.place_story(cv, F, cfg.get("story_labels") or [], tints=tints)
    S.place_city_list(cv, F, [c for c in cities if int(c.get("tier", 3)) == 2], dimmed=("Belgrad", "Çetine", "Bükreş"))

    # ---- alt şerit: üç rakam + bir cümle
    d = cv.d
    d.line((80, MAP_BOT + 6, W - 80, MAP_BOT + 6), fill=BRASS[:3] + (150,), width=1)
    cols = cols_fn(st)[:3]
    cw = (W - 160) / max(1, len(cols))
    for i, (big, l1, l2) in enumerate(cols):
        x_ = 80 + i * cw
        if i:
            d.line((x_ - 20, MAP_BOT + 40, x_ - 20, MAP_BOT + 230), fill=BRASS[:3] + (80,), width=1)
        fb = bs(104)
        while fb.getlength(big) > cw - 40 and fb.size > 60:
            fb = bs(fb.size - 4)
        d.text((x_, MAP_BOT + 128), big, font=fb, fill=hx("#FF8592") if i == 0 else IV, anchor="ls")
        f1 = bar(32, "SemiBold")
        while f1.getlength(l1) > cw - 40 and f1.size > 24:
            f1 = bar(f1.size - 1, "SemiBold")
        d.text((x_, MAP_BOT + 172), l1, font=f1, fill=IV, anchor="ls")
        for j, ln in enumerate(S.wrap(l2, bar(21, "Medium"), cw - 40)[:2]):
            d.text((x_, MAP_BOT + 204 + j * 26), ln, font=bar(21, "Medium"), fill=MUTE, anchor="ls")
    nar = cfg.get("line") or ""
    if nar:
        fz = 30
        while bod(fz, 600, 11).getlength(nar) > W - 200 and fz > 26:
            fz -= 1
        nl = S.wrap(nar, bod(fz, 600, 11), W - 200)[:2]
        y_n = MAP_BOT + (300 if len(nl) == 1 else 288)
        for j, ln in enumerate(nl):
            d.text((W / 2, y_n + j * (fz + 8)), ln, font=bod(fz, 600, 11), fill=IV2, anchor="ms")
    src = cfg.get("sources_line") or "Kaynak: Osmanlı salname ve tahrir kayıtları; harita modeli"
    meth = ("Yöntem: Osmanlı kayıtlarına dayalı bölge kümeleri; nokta yerleri ve alan sınırları temsilîdir · erkek sayımları ×2 · "
            "topluluk ayrımı: Osmanlı millet kayıtları ve dönem etnografyası · Tatar ve Nogaylar Türk sayıldı · "
            + T.HDIGER_NOTE + " · Yahudiler gösterilmedi")
    for fs in (18, 17, 16, 15, 14):
        fsrc = bar(fs, "Medium")
        lines = S.wrap(src, fsrc, 1980) + S.wrap(meth, fsrc, 1980)
        if len(lines) <= 3:
            break
    lines = lines[:3]
    for j, ln in enumerate(lines):
        d.text((W / 2, 2610 + j * (fs + 4)), ln, font=fsrc, fill=MUTE, anchor="ms")
    d.rectangle((26, 26, W - 26, H - 26), outline=BRASS[:3] + (170,), width=2)
    P.series_tag(cv, f"{spec['n']}/{spec['total']}", prefix=spec["series"])

    out = cv.img.convert("RGB")
    out.save(stem + ".png", optimize=True)
    out.resize((1080, 1350), Image.LANCZOS).save(stem + "_ig.jpg", quality=95, subsampling=0)
    json.dump(st, open(stem + "_stats.json", "w"), ensure_ascii=False, indent=1)
    log(f"-> {stem}.png")
    return st


# ------------------------------------------------------------------ seri postları
def km2_txt(v):
    return f"≈ {fmt_int(round(v, -2))} km²"


def cols_region(cfg):
    def fn(st):
        if st["km2_turk"] >= 1500:
            v = st["turk_in_yurt"]
            c0 = (km2_txt(st["km2_turk"]), "Türk yurdu", f"kırmızı taralı alan · içinde yaşayanların {fmt_pct(v)}{P_suffix(v)} Türk")
        else:
            c0 = (km2_txt(st["km2_muslim"]), "Müslüman toprak", f"Türk, Arnavut, Boşnak… renkli alanlar · harita modeli")
        cos = cfg.get("callouts") or []
        out = [c0]
        for c in cos[:2]:
            out.append((c.get("big", ""), c.get("line1", ""), " · ".join(v for v in (c.get("line2"), c.get("src")) if v)))
        return out
    return fn


def P_suffix(v):
    """%74,1 → ’i ; ondalığın son rakamına göre iyelik eki."""
    s = f"{v:.1f}".replace(".", ",")
    last = int(s[-1])
    return "’" + {0: "ı", 1: "i", 2: "si", 3: "ü", 4: "ü", 5: "i", 6: "sı", 7: "si", 8: "i", 9: "u"}[last]


def genel_cfg():
    p = os.path.join(S.SERI, "icerik_genel.json")
    cfg = S.sanitize(json.load(open(p, encoding="utf-8"))) if os.path.exists(p) else {}
    if not cfg.get("cities"):
        key2 = {"Silistre", "Hezargrad", "Kırkkilise", "Tekfurdağı", "Şumnu", "Varna", "Tulça", "Kırcaali", "Drama",
                "Serez", "Yanya", "İşkodra", "Prizren", "Mostar", "Banaluka", "Yenipazar", "Niş", "Vidin", "Tırnova", "Burgaz"}
        cities = [dict(name=n, modern=m or "", lon=lo, lat=la, tier=1) for (n, m, lo, la) in P.T1]
        cities += [dict(name=n, modern="", lon=lo, lat=la, tier=2) for (n, m, lo, la) in P.T2 + P.T3 if n in key2]
        cfg["cities"] = cities
    return cfg


def genel_states(cv, F):
    for t, lo, la in P.STATES:
        px, py = F.ll_to_px(lo, la)
        px, py = float(px), float(py)
        if not (60 < px < W - 60 and MAP_TOP + 40 < py < MAP_BOT - 40):
            continue
        fnt = bar(24, "SemiBold")
        w = cv.tracked_w(t, fnt, 6)
        cv.halo((px, py), t, fnt, hx("#A0A8B8", 170), anchor="ms", rad=4, track=6)
        cv.occupy((px - w / 2, py - 24, px + w / 2, py + 6))
    px, py = F.ll_to_px(25.3, 44.45)
    cv.tracked((float(px), float(py)), "ROMANYA PRENSLİĞİ", bar(24, "SemiBold"), 6, hx("#A0A8B8", 170), anchor="c")
    w = cv.tracked_w("ROMANYA PRENSLİĞİ", bar(24, "SemiBold"), 6)
    cv.occupy((float(px) - w / 2, float(py) - 20, float(px) + w / 2, float(py) + 20))


def render_post(key, out_dir):
    sp = dict(POSTS[key])
    sp.setdefault("ppd", 100)
    sp["total"], sp["series"] = TOTAL, SERIES
    stem = os.path.join(out_dir, f"{sp['n']:02d}_{key}")
    if key == "genel":
        cfg = genel_cfg()
        sp["legend_min"] = 0.3

        # başlık rakamları küme toplamlarından (Rakamlar postu ile aynı): İstanbul ve Osmanlı dışı devletler hariç
        cl_ = T.split_named(S.load_cal(), quiet=True)
        ok_ = [c.get("vilayet") not in S.NONOTT and c.get("vilayet") not in T.NO_STATS for c in cl_]
        g_ = T.people([c for c, o in zip(cl_, ok_) if o]).sum(0)
        p_ = T.largest_remainder(g_)

        def cols(st):
            return [(km2_txt(st["km2_turk"]), "Türk yurdu", "kırmızı taralı alan · Osmanlı Rumeli’si, 1876 · harita modeli"),
                    (fmt_pct(p_[:T.NMUS].sum()), "Müslüman",
                     f"İstanbul hariç Osmanlı Rumeli’si · {fmt_int(round(g_.sum(), -3))} kişi · Türk {fmt_pct(p_[0])}"),
                    (fmt_pct(55.8), "Bulgar, bugünkü Bulgaristan 1875", "her 100 kişiden 44’ü Bulgar değildi · il oranları: swenstone0 derlemesi")]
        return render_simple(sp, cfg, stem, cols, extra_labels=genel_states)
    p = os.path.join(S.SERI, f"icerik_{key}.json")
    cfg = S.sanitize(json.load(open(p, encoding="utf-8")))
    return render_simple(sp, cfg, stem, cols_region(cfg))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--out", default=os.path.join(HERE, "cikti", "seri"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for key in (a.keys or list(POSTS)):
        render_post(key, a.out)


if __name__ == "__main__":
    main()
