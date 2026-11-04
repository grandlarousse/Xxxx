#!/usr/bin/env python3
"""RUMELİ 1876 serisi — bilgi grafikleri: 7/8 Bulgaristan 1875 il il, 8/8 Rakamlarla Rumeli 1876.

Metinler seri/icerik_bulgaristan.json ve seri/icerik_rakamlar.json içindeki 'texts'
sözlüğünden (varsa) okunur; yoksa aşağıdaki varsayılanlar kullanılır.
Kullanım: python3 seri_info.py [bulgaristan] [rakamlar]
"""
import argparse
import json
import os

import numpy as np
import shapely
from PIL import Image, ImageDraw, ImageFilter

import engine as E
import calibrate as C
import poster as P
from poster import (Canvas, hx, COL, TINT, IV, IV2, MUTE, BRASS, BRASS_L, bs, bod, bar,
                    fmt_int, fmt_pct, largest_remainder, star8, log, W, H, RECORDS)
import seri as S
import topluluk as TP

HERE = os.path.dirname(os.path.abspath(__file__))
TOTAL = 8

OTT_NAMES = {
    "Kardzhali": "Kırcaali", "Dobrich": "Hacıoğlu Pazarcığı", "Razgrad": "Hezargrad", "Targovishte": "Eski Cuma",
    "Shumen": "Şumnu", "Smolyan": "Paşmaklı", "Haskovo": "Hasköy", "Ruse": "Rusçuk", "Varna": "Varna",
    "Silistra": "Silistre", "Plovdiv": "Filibe", "Stara Zagora": "Eski Zağra", "Sliven": "İslimye",
    "Yambol": "Yanbolu", "Burgas": "Burgaz", "Pazardzhik": "Tatar Pazarcığı", "Montana": "Kutlofça",
    "Vratsa": "İvraca", "Lovech": "Lofça", "Kyustendil": "Köstendil", "Blagoevgrad": "Yukarı Cuma",
    "Grad Sofiya": "Sofya (şehir)", "Sofia": "Sofya (il)", "Pernik": "Pernik", "Vidin": "Vidin",
    "Pleven": "Plevne", "Gabrovo": "Gabrova", "Veliko Tarnovo": "Tırnova",
}


def texts_for(key, defaults):
    p = os.path.join(S.SERI, f"icerik_{key}.json")
    t = dict(defaults)
    if os.path.exists(p):
        cfg = json.load(open(p, encoding="utf-8"))
        for k, v in (cfg.get("texts") or {}).items():
            if isinstance(v, str) and v.strip():
                t[k] = S.sanitize(v)
    return t


def tr_poss(n):
    """Sayıya 3. tekil iyelik eki: 44’ü, 52’si, 40’ı, 60’ı ..."""
    n = int(n)
    last = {0: None, 1: "i", 2: "si", 3: "ü", 4: "ü", 5: "i", 6: "sı", 7: "si", 8: "i", 9: "u"}
    tens = {10: "u", 20: "si", 30: "u", 40: "ı", 50: "si", 60: "ı", 70: "i", 80: "i", 90: "ı", 0: "ü"}
    if n % 10:
        suf = last[n % 10]
    elif n % 100:
        suf = tens[n % 100]
    else:
        suf = "ü"
    return f"{n}’{suf}"


def header(cv, n, kicker, title, subtitle):
    import re
    kicker = re.sub(r"RUMELİ 1876\s*·\s*\d+/\d+\s*·?\s*", "", kicker).strip(" ·") or "Osmanlı kayıtlarına göre · 93 Harbi arifesi"
    d = cv.d
    d.line((140, 74, W / 2 - 30, 74), fill=BRASS, width=2)
    d.line((W / 2 + 30, 74, W - 140, 74), fill=BRASS, width=2)
    d.line((140, 80, W / 2 - 36, 80), fill=BRASS[:3] + (115,), width=1)
    d.line((W / 2 + 30, 80, W - 140, 80), fill=BRASS[:3] + (115,), width=1)
    cv.tracked((W / 2, 146), P.tr_upper(kicker), bar(30, "SemiBold"), 8, BRASS, anchor="c")
    t = P.tr_upper(title)
    ts = 170
    while bs(ts).getlength(t) > 1900:
        ts -= 2
    cv.halo((W / 2, 300), t, bs(ts), IV, anchor="ms", rad=8, strength=0.6)
    ss = 52
    while bod(ss, 600, 11).getlength(subtitle) > 1900:
        ss -= 2
    cv.halo((W / 2, 376), subtitle, bod(ss, 600, 11), IV2, anchor="ms", rad=6, strength=0.6)


def backdrop(F=None):
    """Koyu zemin + hafif rölyef (bilgi sayfaları için)."""
    F = F or E.Frame(W, H, 1210, center_lonlat=(22.6, 42.4), shift_km=(30, -40))
    elev = E.dem_on_frame(F)
    countries, land, region, by = P.build_masks(F)
    landm = P.rasterize_pil(land, F, 1.0)
    regm = P.rasterize_pil(region, F, 1.0)
    base = P.base_image(F, elev, landm, regm, regm) * 0.55
    return Image.fromarray(np.clip(base * 255, 0, 255).astype(np.uint8)).convert("RGBA"), F


def finish(cv, n, srcs, out_dir, stem):
    P.frame_ornament(cv)
    P.series_tag(cv, f"{n}/{TOTAL}")
    d = cv.d
    for i, t in enumerate(srcs):
        fs = 16
        while bar(fs, "Medium").getlength(t) > 1900 and fs > 11:
            fs -= 1
        d.text((W / 2, 2606 + i * 20), t, font=bar(fs, "Medium"), fill=MUTE, anchor="ms")
    out = cv.img.convert("RGB")
    arr = np.asarray(out, np.int16) + np.random.default_rng(7).integers(-1, 2, (H, W, 1))
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    p = os.path.join(out_dir, stem)
    out.save(p + ".png", optimize=True)
    out.resize((1080, 1350), Image.LANCZOS).save(p + "_ig.jpg", quality=95, subsampling=0)
    log("->", p + ".png")


# ------------------------------------------------------------------ 7/8 Bulgaristan
def post_bulgaristan(out_dir):
    T = texts_for("bulgaristan", dict(
        kicker="Bugünkü il sınırlarıyla · 93 Harbi arifesi",
        title="Bulgaristan 1875: il il",
        subtitle="Bugünkü Bulgaristan topraklarında Bulgarların payı",
        footnote="Rakam: ildeki Bulgarların nüfusa oranı (%). Bulgar olmayanlar: Türk, Pomak, Tatar, Çerkes, Roman, Rum, Gagavuz, Ulah, Ermeni, Yahudi.",
    ))
    img = Image.new("RGBA", (W, H), hx("#04070D"))
    # hafif rölyef zemin: Bulgaristan çerçevesi
    obl = C.oblasts()
    allb = shapely.union_all(list(obl.values()))
    gx0, gy0, gx1, gy1 = allb.bounds
    box = (110, 500, 2050, 1700)
    sc = min((box[2] - box[0]) / (gx1 - gx0), (box[3] - box[1]) / (gy1 - gy0))
    offx = box[0] + ((box[2] - box[0]) - (gx1 - gx0) * sc) / 2
    offy = box[1] + ((box[3] - box[1]) - (gy1 - gy0) * sc) / 2
    # bu ölçekte bir Frame kur (rölyef için)
    mpp = 1 / sc
    cxm, cym = (gx0 + gx1) / 2, (gy0 + gy1) / 2
    lon_c, lat_c = E.TO_LL.transform(cxm, cym)
    cpx = offx + (cxm - gx0) * sc
    cpy = offy + (gy1 - cym) * sc
    F = E.Frame(W, H, W * mpp / 1000, center_lonlat=(lon_c, lat_c), shift_km=((W / 2 - cpx) * mpp / 1000, -(H / 2 - cpy) * mpp / 1000))
    elev = E.dem_on_frame(F, z=9)
    hs, slope, flat = E.multi_hillshade(elev, F.mpp)
    shade = np.clip(hs / flat, 0, 1.6) / 1.6
    countries, land, region, by = P.build_masks(F)
    landm = P.rasterize_pil(land, F, 1.0)
    base = np.where(landm[..., None], (np.array([8, 11, 17]) + np.array([16, 20, 28]) * shade[..., None] ** 1.2), np.array([4, 7, 13]))
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    TG = C.TARGET_BG
    S2 = 2
    lay = Image.new("RGBA", (W * S2, H * S2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    tp = lambda xy: [((offx + (a - gx0) * sc) * S2, (offy + (gy1 - b) * sc) * S2) for a, b in xy]
    lo_c, hi_c = np.array([20, 30, 52]), np.array(hx(TP.COL[8])[:3])
    for nm, g in obl.items():
        t = TG[nm] / 100
        col = tuple(int(v) for v in (lo_c * (1 - t) + hi_c * t)) + (215,)
        for pp in (g.geoms if hasattr(g, "geoms") else [g]):
            ld.polygon(tp(pp.exterior.coords), fill=col, outline=(5, 8, 13, 255), width=4)
    for nm, g in obl.items():
        if TG[nm] < 50:
            for pp in (g.geoms if hasattr(g, "geoms") else [g]):
                inner = pp.buffer(-2.5 / sc)
                for q in (inner.geoms if hasattr(inner, "geoms") else [inner]):
                    if not q.is_empty:
                        ld.line(tp(q.exterior.coords), fill=BRASS_L, width=5)
    lay = lay.resize((W, H), Image.LANCZOS)
    # rölyefi göstermek için choropleth'i hillshade ile çarp
    la = np.asarray(lay, np.float32) / 255
    sh = (0.70 + 0.45 * shade)[..., None]
    rgb = np.clip(la[..., :3] * sh, 0, 1)
    out = np.asarray(img, np.float32) / 255
    out[..., :3] = out[..., :3] * (1 - la[..., 3:4]) + rgb * la[..., 3:4]
    img = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8), "RGBA")
    cv = Canvas(img)
    header(cv, 7, T["kicker"], T["title"], T["subtitle"])
    # il adları + değerler
    for nm, g in obl.items():
        c = g.representative_point()
        (px, py), = [(offx + (c.x - gx0) * sc, offy + (gy1 - c.y) * sc)]
        v = TG[nm]
        on = T.get("name_" + nm, OTT_NAMES.get(nm, nm))
        if nm == "Grad Sofiya":
            cv.halo((px, py + 12), f"{v}", bs(34), IV, anchor="ms", rad=3)
            cv.d.line((px + 10, py - 18, px + 70, py - 70), fill=IV[:3] + (170,), width=2)
            cv.halo((px + 74, py - 74), on, bar(22, "SemiBold"), IV2, anchor="ls", rad=3)
            continue
        cv.halo((px, py + 18), f"{v}", bs(64 if v < 50 else 50, 800 if v < 50 else 700), IV if v < 50 else IV[:3] + (220,), anchor="ms", rad=4)
        f_ = bar(24 if len(on) < 14 else 21, "SemiBold")
        cv.halo((px, py - (48 if v < 50 else 36)), on, f_, IV2, anchor="ms", rad=3)
        mod = T.get("modern_" + nm, "")
        if mod and mod != on:
            cv.halo((px, py + (46 if v < 50 else 40)), mod, bar(19, "Medium"), MUTE, anchor="ms", rad=2)
    d = cv.d
    # Karadeniz / komşular
    for t_, lo, la_ in (("KARADENİZ", 28.6, 42.75), ("ROMANYA", 25.5, 44.35),
                        ("YUNANİSTAN", 24.2, 41.15), ("TÜRKİYE", 27.2, 41.6)):
        x_, y_ = E.TO_XY.transform(lo, la_)
        cv.tracked((offx + (x_ - gx0) * sc, offy + (gy1 - y_) * sc), t_, bar(22, "SemiBold"), 8, hx("#5D7391"), anchor="c")
    # lejant rampası
    lx, ly = 1580, 1760
    for i in range(420):
        t = i / 419
        cc = tuple(int(v) for v in (lo_c * (1 - t) + hi_c * t))
        d.line((lx + i, ly, lx + i, ly + 14), fill=cc)
    d.text((lx, ly + 36), "%0", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    d.text((lx + 420, ly + 36), "%100 Bulgar", font=bar(17, "Medium"), fill=MUTE, anchor="rs")
    d.rectangle((lx, ly + 52, lx + 26, ly + 68), outline=BRASS_L, width=3)
    d.text((lx + 36, ly + 68), "Bulgarların yarıdan az olduğu iller", font=bar(18, "Medium"), fill=IV2, anchor="ls")
    nt = T.get("map_sub", "")
    if nt:
        d.text((120, ly + 14), nt, font=bar(21, "Medium"), fill=IV2, anchor="ls")
    sn = "*" + T.get("sofya_note", "")
    for j, ln in enumerate(S.wrap(sn, bar(20, "Medium"), 1400)[:2]):
        d.text((120, ly + 42 + j * 25), ln, font=bar(20, "Medium"), fill=MUTE, anchor="ls")
    # ---- alt bölüm: sıralı liste + karşılaştırma
    y0 = 1840
    st = Image.new("RGBA", (2116 - 44, 2580 - y0), (4, 6, 10, int(255 * 0.86)))
    cv.img.alpha_composite(st, (44, y0))
    d = cv.d
    d.line((44, y0, 2116, y0), fill=BRASS, width=2)
    star8(d, W / 2, y0, 10, BRASS, 2, fill=hx("#05080D"))
    cv.tracked((80, y0 + 48), T.get("panel_head_rank", "SIRALAMA · EN AZDAN EN ÇOĞA"), bar(22, "SemiBold"), 4, BRASS)
    ro = [n.strip() for n in (T.get("rank_order") or "").split(",") if n.strip() in TG]
    items = [(n, TG[n]) for n in ro] if len(ro) == len(TG) else sorted(TG.items(), key=lambda t: (t[1], OTT_NAMES.get(t[0], t[0])))
    colx = [80, 560]
    for i, (nm, v) in enumerate(items):
        cx_ = colx[i // 14]
        yy = y0 + 84 + (i % 14) * 46
        on = T.get("name_" + nm, OTT_NAMES.get(nm, nm))
        if i == 11 and items[10][1] < 50 <= v:
            d.line((cx_, yy - 2, cx_ + 470, yy - 2), fill=BRASS, width=2)
            d.text((cx_ + 474, yy + 4), "%50", font=bar(16, "SemiBold"), fill=BRASS, anchor="ls")
        d.text((cx_, yy + 22), f"{i + 1:>2}.", font=bar(19, "Medium"), fill=MUTE, anchor="ls")
        d.text((cx_ + 36, yy + 22), on, font=bar(21, "SemiBold"), fill=IV, anchor="ls")
        bx0, bw = cx_ + 230, 170
        d.rectangle((bx0, yy + 6, bx0 + bw, yy + 24), fill=(20, 26, 38))
        d.rectangle((bx0, yy + 6, bx0 + bw * v / 100, yy + 24), fill=hx(TP.COL[8]))
        d.line((bx0 + bw / 2, yy + 3, bx0 + bw / 2, yy + 27), fill=BRASS[:3] + (160,), width=1)
        d.text((bx0 + bw + 10, yy + 23), f"%{v}", font=bs(26), fill=IV if v < 50 else IV2, anchor="ls")
    # karşılaştırma kutusu
    d.line((1060, y0 + 30, 1060, 2560), fill=BRASS[:3] + (90,), width=1)
    x0 = 1100
    cv.tracked((x0, y0 + 48), T.get("panel_head_compare", "KARŞILAŞTIRMA"), bar(22, "SemiBold"), 4, BRASS)
    nlow = sum(1 for v in TG.values() if v < 50)
    hero = f"{nlow}* / 28"
    d.text((x0, y0 + 160), hero, font=bs(110), fill=IV, anchor="ls")
    hx_ = x0 + bs(110).getlength(hero) + 22
    d.text((hx_, y0 + 116), "ilde Bulgarlar", font=bar(28, "SemiBold"), fill=IV, anchor="ls")
    d.text((hx_, y0 + 150), "nüfusun yarısından azdı", font=bar(28, "SemiBold"), fill=IV, anchor="ls")
    yy = y0 + 214
    for ln in S.wrap(T.get("highlight_model", ""), bar(22, "SemiBold"), 950)[:2]:
        d.text((x0, yy), ln, font=bar(22, "SemiBold"), fill=hx(TP.TINT[0]), anchor="ls")
        yy += 28
    rows = [
        (T.get("compare_1_value", fmt_pct(C.TOTAL_BG)), T.get("compare_1_label", "Bulgar"), T.get("compare_1_sub", "")),
        (T.get("compare_2_value", "%54,0"), T.get("compare_2_label", "Bulgar milleti"), T.get("compare_2_sub", "")),
        (T.get("compare_3_value", "%40,5"), T.get("compare_3_label", "Müslüman"), T.get("compare_3_sub", "")),
    ]
    yy += 8
    for big, l1, l2 in rows:
        d.text((x0, yy + 56), big, font=bs(62), fill=IV, anchor="ls")
        d.text((x0 + 200, yy + 26), l1, font=bar(23, "SemiBold"), fill=IV, anchor="ls")
        for j, ln in enumerate(S.wrap(l2, bar(19, "Medium"), 760)[:2]):
            d.text((x0 + 200, yy + 51 + j * 22), ln, font=bar(19, "Medium"), fill=MUTE, anchor="ls")
        yy += 84
    for ln in S.wrap(T.get("compare_note", ""), bar(18, "Medium"), 960)[:2]:
        d.text((x0, yy + 4), ln, font=bar(18, "Medium"), fill=MUTE, anchor="ls")
        yy += 22
    yy += 14
    d.line((x0, yy, 2080, yy), fill=BRASS[:3] + (70,), width=1)
    cv.tracked((x0, yy + 34), T.get("panel_head_check", "OSMANLI KAYDIYLA SAĞLAMA"), bar(20, "SemiBold"), 4, BRASS)
    d.text((x0, yy + 58), T.get("check_sub", ""), font=bar(18, "Medium"), fill=MUTE, anchor="ls")
    yy += 70
    rows_c = []
    for i in range(1, 6):
        t_ = T.get(f"check_row_{i}")
        if t_:
            left, _, right = t_.replace("›", "→").partition("→")
            rows_c.append((left.strip(), right.strip()))
    lw_ = max([bar(20, "SemiBold").getlength(l) for l, _ in rows_c] + [100])
    for left, right in rows_c:
        d.text((x0, yy + 22), left, font=bar(20, "SemiBold"), fill=IV2, anchor="ls")
        ay = yy + 15
        ax = x0 + lw_ + 20
        d.line((ax, ay, ax + 30, ay), fill=BRASS, width=2)
        d.polygon([(ax + 30, ay - 6), (ax + 40, ay), (ax + 30, ay + 6)], fill=BRASS)
        d.text((ax + 52, yy + 22), right, font=bar(20, "SemiBold"), fill=IV, anchor="ls")
        yy += 27
    for ln in S.wrap(T.get("check_note", ""), bar(18, "Medium"), 960)[:2]:
        d.text((x0, yy + 22), ln, font=bar(18, "Medium"), fill=MUTE, anchor="ls")
        yy += 22
    srcs = [T.get("footnote_short") or f"Kaynak: il oranları {RECORDS['BG1875']['src']} · Osmanlı kaydı: {RECORDS['TUNA_1875']['src']}",
            "il oranları: swenstone0 (çevrimiçi derleme, 1875 verileri bugünkü il sınırlarına göre) · harita: Natural Earth · rölyef: AWS Terrain · Osmanlıca il adları yaklaşık karşılıklardır"]
    finish(cv, 7, srcs, out_dir, "07_bulgaristan")


# ------------------------------------------------------------------ 8/8 Rakamlar
def post_rakamlar(out_dir):
    T = texts_for("rakamlar", dict(
        kicker="Osmanlı kayıtları ve harita modeli",
        title="Rakamlarla Rumeli 1876",
        subtitle="93 Harbi’nden hemen önce Balkanlar’ın nüfusu",
    ))
    base, F = backdrop()
    cv = Canvas(base)
    # arka plana soluk nokta haritası (ana posterden)
    mp = os.path.join(HERE, "cikti", "rumeli_1876.png")
    if os.path.exists(mp):
        m = Image.open(mp).convert("RGBA").filter(ImageFilter.GaussianBlur(3))
        a = np.asarray(m, np.float32).copy()
        a[..., 3] = 255 * 0.16
        a[:560, :, 3] = 0
        a[2100:, :, 3] = 0
        for (x0_, y0_, x1_, y1_) in ((1040, 590, 1760, 950), (40, 1680, 540, 2160), (1690, 1630, 2120, 2100),
                                     (1820, 1120, 2120, 1460)):
            a[y0_:y1_, x0_:x1_, 3] = 0
        cv.img.alpha_composite(Image.fromarray(a.astype(np.uint8), "RGBA"))
    header(cv, 8, T["kicker"], T["title"], T["subtitle"])
    d = cv.d
    cl = TP.split_named(S.load_cal(), quiet=True)
    vil = np.array([c.get("vilayet", "") for c in cl])
    ok = np.array([v not in S.NONOTT and v != "İstanbul" for v in vil])
    G = TP.people(cl)
    g = G[ok].sum(0)
    p = largest_remainder(g)
    # ---- kahraman satırı
    y0 = 470
    ov = Image.new("RGBA", (2000, 520), (4, 6, 10, 215))
    cv.img.alpha_composite(ov, (80, y0))
    d = cv.d
    d.line((80, y0, 2080, y0), fill=BRASS, width=2)
    cv.tracked((110, y0 + 48), "OSMANLI RUMELİ’Sİ · 1876 · İSTANBUL HARİÇ", bar(24, "SemiBold"), 4, BRASS)
    d.text((104, y0 + 200), fmt_int(g.sum()), font=bs(150), fill=IV, anchor="ls")
    d.text((110, y0 + 240), "kişi (harita modeli; Osmanlı salname ve sayımlarından)", font=bar(24, "Medium"), fill=IV2, anchor="ls")
    mus = p[:TP.NMUS].sum()
    d.text((1180, y0 + 200), fmt_pct(mus), font=bs(150), fill=IV, anchor="ls")
    d.text((1186, y0 + 240), f"Müslüman: her 100 kişiden {tr_poss(round(mus))}", font=bar(26, "SemiBold"), fill=IV, anchor="ls")
    fy = y0 + 92
    for key in ("fact_1", "fact_2", "fact_3"):
        t_ = T.get(key, "")
        for ln in S.wrap(t_, bar(22, "SemiBold"), 520)[:2]:
            d.text((1560, fy), ln, font=bar(22, "SemiBold"), fill=hx(TP.TINT[0]) if key == "fact_1" else IV2, anchor="ls")
            fy += 27
        fy += 10
    # yığılmış çubuk (adlı topluluklar)
    bx0, bw, by = 110, 1940, y0 + 290
    xs = bx0
    pint = largest_remainder(g, nd=0)
    for gi in range(TP.NG):
        w_ = bw * p[gi] / 100
        if w_ <= 0.5:
            continue
        d.rectangle((xs, by, xs + max(0, w_ - 3), by + 66), fill=hx(TP.COL[gi]))
        lab_ = f"{TP.NAMES[gi]} {fmt_pct(p[gi])}"
        if bar(28, "SemiBold").getlength(lab_) < w_ - 26:
            d.text((xs + 14, by + 46), lab_, font=bar(28, "SemiBold"), fill=hx("#05080D"), anchor="ls")
        elif w_ > 40:
            d.text((xs + w_ / 2 - 1, by + 44), f"{pint[gi]:.0f}", font=bar(22, "SemiBold"), fill=hx("#05080D"), anchor="ms")
        xs += w_
    # alt satırlar: Müslüman | Hristiyan toplulukları (yüzde ve kişi)
    for ri, (head, rng) in enumerate((("MÜSLÜMAN", range(TP.NMUS)), ("HRİSTİYAN", range(TP.NMUS, TP.NG)))):
        yy = by + 112 + ri * 40
        tot_ = p[list(rng)].sum()
        cv.tracked((110, yy), f"{head} {fmt_pct(tot_)}", bar(20, "SemiBold"), 3, BRASS)
        items = []
        for gi in rng:
            if p[gi] < 0.3:      # çok küçük paylar (ör. diğer Müslüman %0,2) yalnız toplamda
                continue
            mn = g[gi] / 1e6
            items.append((gi, f"{TP.NAMES[gi]} {fmt_pct(p[gi])}",
                          f" · {('%.2f' % mn).replace('.', ',')} mn" if mn >= 0.1 else f" · {fmt_int(round(g[gi], -3))}"))
        fs, gap = 22, 28
        while True:
            f_, f2_ = bar(fs, "SemiBold"), bar(fs - 4, "Medium")
            need = sum(22 + f_.getlength(a_) + f2_.getlength(b_) + gap for _, a_, b_ in items) - gap
            if need <= 2050 - 390 or fs <= 16:
                break
            fs -= 1
            gap = max(16, gap - 2)
        xx = 390
        for gi, t_, t2 in items:
            d.rectangle((xx, yy - 17, xx + 14, yy - 3), fill=hx(TP.COL[gi]))
            d.text((xx + 22, yy), t_, font=f_, fill=hx(TP.TINT[gi]), anchor="ls")
            d.text((xx + 22 + f_.getlength(t_), yy), t2, font=f2_, fill=MUTE, anchor="ls")
            xx += 22 + f_.getlength(t_) + f2_.getlength(t2) + gap
    d.text((110, y0 + 498), "Türk: Tatar ve Nogaylar dâhil · " + TP.HDIGER_NOTE + " · Yahudiler gösterilmedi",
           font=bar(18, "Medium"), fill=MUTE, anchor="ls")
    # ---- vilayet tablosu
    y1 = 1040
    ov = Image.new("RGBA", (1180, 760), (4, 6, 10, 215))
    cv.img.alpha_composite(ov, (80, y1))
    d = cv.d
    d.line((80, y1, 1260, y1), fill=BRASS, width=2)
    cv.tracked((110, y1 + 46), "VİLÂYET VE SANCAKLARA GÖRE", bar(24, "SemiBold"), 4, BRASS)
    in_ott = ok
    ROWS = P.stats(cl, np.array([v not in S.NONOTT for v in vil]))
    ROWS = [(n_, g_, p_, (34.9 if n_ == "Yanya" else r_)) for (n_, g_, p_, r_) in ROWS]
    P.REC_YEAR["Yanya"] = "1871"
    bx0, bw = 380, 560
    yy0 = y1 + 100
    for i, (n_, gg, pp, rec) in enumerate(ROWS[:10]):
        yy = yy0 + i * 64
        d.text((110, yy + 30), n_, font=bar(28 if i else 30, "SemiBold"), fill=BRASS if i == 0 else IV, anchor="ls")
        d.text((110, yy + 52), fmt_int(gg.sum()) + " kişi", font=bar(16, "Medium"), fill=MUTE, anchor="ls")
        xs = bx0
        pint = largest_remainder(gg, nd=0)
        for gi in range(TP.NG):
            w_ = bw * pp[gi] / 100
            if w_ > 0.5:
                d.rectangle((xs, yy + 4, xs + max(0, w_ - 2), yy + 38), fill=hx(TP.COL[gi]))
                if w_ > 44:
                    d.text((xs + w_ / 2, yy + 30), f"{pint[gi]:.0f}", font=bar(18, "SemiBold"), fill=hx("#05080D"), anchor="ms")
            xs += w_
        d.text((bx0 + bw + 16, yy + 36), fmt_pct(pp[:TP.NMUS].sum()), font=bs(40), fill=IV, anchor="ls")
        if rec:
            xr = bx0 + bw * rec / 100
            d.rectangle((xr - 2, yy, xr + 2, yy + 42), fill=IV)
            d.polygon([(xr, yy - 10), (xr + 5, yy - 5), (xr, yy), (xr - 5, yy - 5)], fill=IV)
            d.text((bx0 + bw + 130, yy + 34), f"{P.REC_YEAR.get(n_, '')} %{str(rec).replace('.', ',')}", font=bar(20, "SemiBold"), fill=IV2, anchor="ls")
    d.text((110, y1 + 742), "çubuk: harita modeli · ◆ çizgi: Osmanlı kaydı (Müslüman %) · büyük rakam: modelde Müslüman payı",
           font=bar(16, "Medium"), fill=MUTE, anchor="ls")
    # ---- Tuna kaydı (waffle)
    x2 = 1300
    ov = Image.new("RGBA", (780, 760), (4, 6, 10, 215))
    cv.img.alpha_composite(ov, (x2, y1))
    d = cv.d
    d.line((x2, y1, x2 + 780, y1), fill=BRASS, width=2)
    cv.tracked((x2 + 30, y1 + 46), "OSMANLI KAYDI · TUNA VİLÂYETİ 1875", bar(24, "SemiBold"), 4, BRASS)
    d.text((x2 + 30, y1 + 78), f"Tahrir-i Cedid · {fmt_int(RECORDS['TUNA_1875']['males'])} erkek · 1 kare = 1.000 erkek", font=bar(18, "Medium"), fill=MUTE, anchor="ls")
    cats = [(406, hx(TP.COL[0]), False), (55, hx(TP.COL[5]), False), (606, hx(TP.COL[8]), False), (54, hx("#8A93A3"), True)]
    seq = []
    for n_, c_, hol in cats:
        seq += [(c_, hol)] * n_
    ox, oy, pitch = x2 + 30, y1 + 104, 12
    for i, (c_, hol) in enumerate(seq):
        col_, row_ = i // 19, i % 19
        xq, yq = ox + col_ * pitch, oy + row_ * pitch
        if hol:
            d.rectangle((xq, yq, xq + 9, yq + 9), outline=c_, width=1)
        else:
            d.rectangle((xq, yq, xq + 9, yq + 9), fill=c_)
    yk = oy + 19 * pitch + 60
    d.text((x2 + 30, yk), fmt_pct(RECORDS["TUNA_1875"]["muslim_pct"]), font=bs(80), fill=IV, anchor="ls")
    d.text((x2 + 30, yk + 34), "Müslüman", font=bar(24, "SemiBold"), fill=IV, anchor="ls")
    d.text((x2 + 300, yk), fmt_pct(RECORDS["TUNA_1875"]["bulgar_pct"]), font=bs(80), fill=hx(TP.TINT[8]), anchor="ls")
    d.text((x2 + 300, yk + 34), "Bulgar milleti", font=bar(24, "SemiBold"), fill=IV, anchor="ls")
    kx, ky = x2 + 30, yk + 80
    for c_, lab_, hol in ((hx(TP.COL[0]), "İslam milleti %36,2", False), (hx(TP.COL[5]), "Çerkes, Kıpti %4,9", False), (hx("#8A93A3"), "diğer %4,8", True)):
        if hol:
            d.rectangle((kx, ky - 14, kx + 12, ky - 2), outline=c_, width=1)
        else:
            d.rectangle((kx, ky - 14, kx + 12, ky - 2), fill=c_)
        d.text((kx + 18, ky), lab_, font=bar(19, "Medium"), fill=IV2, anchor="ls")
        kx += 18 + bar(19, "Medium").getlength(lab_) + 22
    d.text((x2 + 30, ky + 34), "Kaynak: A. Koyuncu, Turkish Studies 9/4 (2014)", font=bar(17, "Medium"), fill=MUTE, anchor="ls")
    # ---- 93 Harbi + Berlin
    y3 = 1840
    ov = Image.new("RGBA", (2000, 720), (4, 6, 10, 228))
    cv.img.alpha_composite(ov, (80, y3))
    d = cv.d
    d.line((80, y3, 2080, y3), fill=BRASS, width=2)
    M = RECORDS["MCCARTHY"]
    cv.tracked((110, y3 + 48), T.get("after_head", "SONRA: 93 HARBİ, 1877–78"), bar(24, "SemiBold"), 4, BRASS)
    cols = [(fmt_int(M["muslims"]), "Müslüman (1877)", "Tuna + sonraki Şarkî Rumeli"),
            (fmt_int(M["dead"]), "hayatını kaybetti", "%17,4"),
            (fmt_int(M["emigrated"]), "göç etti", "%34,3")]
    for i, (big, l1, l2) in enumerate(cols):
        x_ = 110 + i * 360
        d.text((x_, y3 + 170), big, font=bs(92), fill=IV, anchor="ls")
        d.text((x_ + 2, y3 + 206), l1, font=bar(26, "SemiBold"), fill=IV, anchor="ls")
        d.text((x_ + 2, y3 + 236), l2, font=bar(20, "Medium"), fill=IV2, anchor="ls")
    yy = y3 + 316
    line = T.get("after_line", "Her 100 Müslümandan 17’si öldü, 34’ü yurdunu bırakmak zorunda kaldı.")
    for ln in S.wrap(line, bod(40, 600, 11), 1020)[:2]:
        d.text((110, yy), ln, font=bod(40, 600, 11), fill=IV, anchor="ls")
        yy += 50
    yy += 6
    for key in ("after_alt", "after_src"):
        for ln in S.wrap(T.get(key, ""), bar(18, "Medium"), 1020)[:3]:
            d.text((110, yy), ln, font=bar(18, "Medium"), fill=MUTE if key == "after_src" else IV2, anchor="ls")
            yy += 23
        yy += 6
    d.line((1180, y3 + 30, 1180, y3 + 690), fill=BRASS[:3] + (90,), width=1)
    bx = 1210
    cv.tracked((bx, y3 + 48), T.get("berlin_head", "BERLİN 1878: KOPAN TOPRAKLAR"), bar(22, "SemiBold"), 4, BRASS)
    d.text((bx, y3 + 160), T.get("berlin_big", "≈2 milyon"), font=bs(104), fill=IV, anchor="ls")
    yy = y3 + 200
    for ln in S.wrap(T.get("berlin_big_label", ""), bar(21, "SemiBold"), 850)[:4]:
        d.text((bx, yy), ln, font=bar(21, "SemiBold"), fill=IV, anchor="ls")
        yy += 27
    yy += 10
    for i in range(1, 9):
        t_ = T.get(f"berlin_item_{i}", "")
        if not t_:
            continue
        lines_ = S.wrap(t_, bar(17, "Medium"), 830)[:2]
        d.rectangle((bx, yy - 11, bx + 6, yy - 5), fill=BRASS)
        for ln in lines_:
            d.text((bx + 16, yy), ln, font=bar(17, "Medium"), fill=IV2, anchor="ls")
            yy += 21
        yy += 4
        if yy > y3 + 690:
            break
    srcs = ["Kaynaklar: " + " · ".join([RECORDS["TUNA_1875"]["src"], RECORDS["EDIRNE_1293"]["src"], RECORDS["BOSNA_1287"]["src"], RECORDS["MCCARTHY"]["src"]]),
            "Model: Osmanlı salname/sayım verilerine dayalı 702 bölge kümesi (ana poster ile aynı) · İstanbul ve 1876’da Osmanlı idaresi dışındaki devletler hariç"]
    finish(cv, 8, srcs, out_dir, "08_rakamlar")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keys", nargs="*")
    ap.add_argument("--out", default=os.path.join(HERE, "cikti", "seri"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    keys = a.keys or ["bulgaristan", "rakamlar"]
    if "bulgaristan" in keys:
        post_bulgaristan(a.out)
    if "rakamlar" in keys:
        post_rakamlar(a.out)


if __name__ == "__main__":
    main()
