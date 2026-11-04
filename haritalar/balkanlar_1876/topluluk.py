#!/usr/bin/env python3
"""Topluluk kategorileri (adıyla): Türk, Pomak, Arnavut, Boşnak, Torbeş, Çerkes, Müslüman Roman;
Bulgar, Rum, Sırp, Hırvat, diğer Hristiyan.

Kalibre edilmiş kümeler üç ana pay taşır (turk / muslim_other / christian). Bu modül
  * Müslüman payını  seri/muslim_ayrimi.json     (pomak … roman, diger)
  * Hristiyan payını seri/hristiyan_ayrimi.json  (bulgar, rum, diger)  ve
                     seri/hristiyan_ayrimi_bati.json (bulgar, rum, sirp, hirvat, diger; batı vilâyetleri, öncelikli)
satırlarına göre böler. Satırı olmayan kümeler grup notu ve vilâyete göre tahminle atanır.
Ayrıca ortak alan kuralı (Türk yurdu: yerel Türk payı >= %40; Müslüman payı >= %40 ise en kalabalık
Müslüman topluluk; aksi hâlde yerel çoğunluk) ve alan dolgusu buradadır.
"""
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, distance_transform_edt, label as nd_label

HERE = os.path.dirname(os.path.abspath(__file__))
SERI = os.path.join(HERE, "seri")

CATS = ("turk", "pomak", "arnavut", "bosnak", "torbes", "cerkes", "roman", "mdiger",
        "bulgar", "rum", "sirp", "hirvat", "hdiger")
NAMES = ["Türk", "Pomak", "Arnavut", "Boşnak", "Torbeş", "Çerkes", "Müslüman Roman", "Valaad ve Müslüman Ulah",
         "Bulgar", "Rum", "Sırp", "Hırvat", "Diğer Hristiyan"]
# gri kullanılmaz (gri = boş alan gibi okunur): diğer Müslüman zeytin, diğer Hristiyan kahverengi
COL = ["#E23B4E", "#F0B43C", "#8FC740", "#2FAE7A", "#C7D64B", "#E58A3A", "#D46FC3", "#8E9A5B",
       "#3F7FE0", "#33C1C6", "#9A6CEB", "#5DB3EE", "#B08860"]
TINT = ["#FF7A88", "#FFD27A", "#B9E77A", "#6FD8A8", "#E4EE8A", "#FFB57A", "#F0A6E2", "#C9D296",
        "#86B1FF", "#8FE6E9", "#C4AEFF", "#A9DBFB", "#E0C29C"]
NG = len(CATS)
NMUS = 8                      # ilk 8 kategori Müslüman
IDX = {c: i for i, c in enumerate(CATS)}
K3 = np.array([0] + [1] * (NMUS - 1) + [2] * (NG - NMUS), np.int8)   # adlı → (Türk, diğer Müslüman, Hristiyan)
TURK_RULE = 0.40
MKEYS = ("pomak", "arnavut", "bosnak", "torbes", "cerkes", "roman")
HKEYS = ("bulgar", "rum", "sirp", "hirvat")
# 'diğer Hristiyan' kapsamı (dipnot için)
HDIGER_NOTE = "Diğer Hristiyan: Ulah, Ortodoks ve Katolik Arnavut, Romen, Ermeni, Gagavuz, Lipovan"


def log(*a):
    try:
        from poster import log as _l
        _l(*a)
    except Exception:
        print(*a)


def _index(path):
    out = {}
    if os.path.exists(path):
        for r in json.load(open(path, encoding="utf-8")):
            out[(r["name"], round(r["lat"], 2), round(r["lon"], 2))] = r
    return out


def _guess_muslim(c):
    g = (c.get("groups") or "").lower()
    for key, words in (("pomak", ("pomak",)), ("arnavut", ("alban", "arnavut")), ("bosnak", ("bosniak", "boşnak")),
                       ("torbes", ("torbe",)), ("cerkes", ("circass", "çerkes")), ("roman", ("roma", "kıpti", "gypsy"))):
        if any(w in g for w in words):
            return key
    vil = c.get("vilayet")
    return {"Bosna": "bosnak", "Hersek": "bosnak", "İşkodra": "arnavut", "Yanya": "arnavut", "Prizren": "arnavut",
            "Sırbistan": "bosnak", "Karadağ": "arnavut", "Avusturya-Macaristan": "bosnak"}.get(vil, "pomak")


def _guess_christian(c):
    """Satırı olmayan küme: grup notu, yoksa vilâyet."""
    g = (c.get("groups") or "").lower()
    out = {k: 0.0 for k in HKEYS + ("diger",)}
    hits = [k for k, ws in (("sirp", ("serb", "sırp", "montenegr", "karadağ")), ("hirvat", ("croat", "hırvat", "catholic", "katolik")),
                            ("rum", ("greek", "rum ", "rum,", "yunan")), ("bulgar", ("bulgar",)))
            if any(w in g for w in ws)]
    if hits:
        for k in hits:
            out[k] = 1.0 / len(hits)
        return out
    vil = c.get("vilayet")
    if vil in ("Bosna", "Hersek"):
        out["sirp"], out["hirvat"] = 0.75, 0.25
    elif vil in ("Sırbistan", "Karadağ", "Prizren"):
        out["sirp"] = 1.0
    elif vil == "Avusturya-Macaristan":
        out["hirvat"], out["sirp"] = 0.7, 0.3
    elif vil in ("Yanya", "Yunanistan"):
        out["rum"] = 1.0
    elif vil == "İşkodra":
        out["diger"] = 1.0
    else:
        out["bulgar"] = 1.0
    return out


def _serb_part(text):
    """Eski ayrımın 'diger' notunda Sırp payı (0–1)."""
    t = (text or "").lower()
    if "serb" not in t and "sırp" not in t:
        return 0.0
    others = any(w in t for w in ("alban", "vlach", "aromanian", "catholic", "romanian", "tsintsar", "armenian"))
    if not others:
        return 1.0
    few = any(w in t for w in ("a few", "few ", "merchants"))
    if t.startswith("serb"):
        return 0.85 if few else 0.65
    return 0.4


def split_named(cl, quiet=False):
    """Kümelere adlı topluluk paylarını (yüzde) ekler; turk/muslim_other/christian toplamları korunur."""
    hs = _index(os.path.join(SERI, "hristiyan_ayrimi.json"))
    hb = _index(os.path.join(SERI, "hristiyan_ayrimi_bati.json"))
    ms = _index(os.path.join(SERI, "muslim_ayrimi.json"))
    mh = mm = 0
    for c in cl:
        k_ = (c["name"], round(c["lat"], 2), round(c["lon"], 2))
        ch, mo = max(0.0, float(c["christian"])), max(0.0, float(c["muslim_other"]))
        for kk in CATS[1:]:
            c[kk] = 0.0
        # Hristiyan
        r = hb.get(k_)
        if r and sum(float(r.get(kk, 0)) for kk in HKEYS + ("diger",)) > 0:
            t = sum(float(r.get(kk, 0)) for kk in HKEYS + ("diger",))
            for kk in HKEYS:
                c[kk] = ch * float(r.get(kk, 0)) / t
            c["hdiger"] = ch * float(r.get("diger", 0)) / t
        else:
            r = hs.get(k_)
            if r and (r["bulgar"] + r["rum"] + r["diger"]) > 0:
                t = r["bulgar"] + r["rum"] + r["diger"]
                sp = _serb_part(r.get("diger_groups"))
                c["bulgar"], c["rum"] = ch * r["bulgar"] / t, ch * r["rum"] / t
                c["sirp"] = ch * r["diger"] / t * sp
                c["hdiger"] = ch * r["diger"] / t * (1 - sp)
            else:
                mh += ch > 0
                gs = _guess_christian(c)
                for kk in HKEYS:
                    c[kk] = ch * gs[kk]
                c["hdiger"] = ch * gs["diger"]
        # Müslüman (Türk dışı)
        r = ms.get(k_)
        if r and sum(r[kk] for kk in MKEYS + ("diger",)) > 0:
            t = sum(r[kk] for kk in MKEYS + ("diger",))
            for kk in MKEYS:
                c[kk] = mo * r[kk] / t
            c["mdiger"] = mo * r["diger"] / t
        else:
            mm += mo > 0
            c[_guess_muslim(c)] = mo
    if (mh or mm) and not quiet:
        log(f"  ayrımı eksik küme: Hristiyan {mh}, Müslüman {mm} (tahminle atandı)")
    return cl


def people(cl):
    """(n, NG) kişi."""
    from engine import cluster_population
    P = np.array([float(c.get("population") or cluster_population(c)) for c in cl])
    S = np.array([[max(0.0, float(c.get(k, 0))) for k in CATS] for c in cl])
    S = S / np.maximum(S.sum(1, keepdims=True), 1e-12)
    return P[:, None] * S


def present(k, inside=None, min_pct=0.6):
    """Çerçevede görünen kategoriler (lejant), sıra = CATS."""
    kk = k if inside is None else k[inside]
    cnt = np.bincount(kk, minlength=NG).astype(float)
    p = 100 * cnt / max(1, cnt.sum())
    return [g for g in range(NG) if p[g] >= min_pct or g == 0], p


# ------------------------------------------------------------------ Türk yurdu kuralı ve dolgu
MUSLIM_RULE = 0.40


def yurt_labels(F, x, y, k, area, sigma_km=2.6, step=2, rule=TURK_RULE, smooth_km=1.6, muslim_rule=MUSLIM_RULE):
    """Alan kuralı (boşluk bırakmaz):
      1) yerel Türk payı >= rule            → Türk yurdu (0)
      2) yerel Müslüman payı >= muslim_rule → en kalabalık Müslüman topluluk (Türk olabilir)
      3) aksi hâlde                          → yerel çoğunluk
    Boşluklar en yakın karar verilmiş alanla dolar; içinde yerleşim olmayan kara parçaları boş kalır."""
    Hh, Ww = area.shape
    h, w = Hh // step, Ww // step
    cnt = np.zeros((NG, h, w), np.float32)
    xi = np.clip((x / step).astype(int), 0, w - 1)
    yi = np.clip((y / step).astype(int), 0, h - 1)
    for g in range(NG):
        m = k == g
        if m.any():
            np.add.at(cnt[g], (yi[m], xi[m]), 1.0)
    sig = sigma_km * 1000 / (F.mpp * step)
    D = np.stack([gaussian_filter(cnt[g], sig) for g in range(NG)])
    tot = D.sum(0)
    decided = tot > (0.5 / (2 * np.pi * sig * sig))
    tshare = D[0] / np.maximum(tot, 1e-12)
    mshare = D[:NMUS].sum(0) / np.maximum(tot, 1e-12)
    lab = np.argmax(D, 0).astype(np.int8)
    if muslim_rule is not None:
        lab = np.where(mshare >= muslim_rule, np.argmax(D[:NMUS], 0), lab).astype(np.int8)
    lab = np.where(tshare >= rule, 0, lab).astype(np.int8)
    if (~decided).any() and decided.any():
        _, (ii, jj) = distance_transform_edt(~decided, return_indices=True)
        lab = lab[ii, jj]
    oh = np.stack([gaussian_filter((lab == g).astype(np.float32), smooth_km * 1e3 / (F.mpp * step) + 1.0) for g in range(NG)])
    lab = np.argmax(oh, 0).astype(np.int8)
    # içinde hiç yerleşim olmayan kara parçaları (ör. veri dışı adalar) boyanmaz
    area2 = area[::step, ::step][:h, :w]
    comp, n = nd_label(area2)
    has = np.zeros(n + 1, bool)
    has[np.unique(comp[yi, xi])] = True
    has[0] = False
    lab = np.where(has[comp], lab, -1).astype(np.int8)
    full = np.repeat(np.repeat(lab, step, 0), step, 1)[:Hh, :Ww]
    return np.where(area, full, -1).astype(np.int8)


def _hx(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def fill_layer(lab, fade=None, dim=None, spacing=11, lw=2.4, a_turk=(0.30, 0.45), a_other=(0.12, 0.22), edge_turk=True):
    """Taralı alan katmanı: Türk yurdu güçlü tarama + parlak sınır; diğer topluluklar soluk tarama."""
    Hh, Ww = lab.shape
    Y, X = np.mgrid[0:Hh, 0:Ww]
    v = (X + Y) % spacing
    hatch = np.clip(lw / 2 + 0.5 - np.abs(v - spacing / 2), 0, 1).astype(np.float32)
    lay = np.zeros((Hh, Ww, 4), np.float32)
    for g in range(NG):
        m = lab == g
        if not m.any():
            continue
        lay[m, :3] = _hx(COL[g])
        a0, a1 = a_turk if g == 0 else a_other
        lay[m, 3] = a0 + a1 * hatch[m]
    # topluluk sınırlarında ince koyu çizgi
    edge = np.zeros((Hh, Ww), bool)
    edge[:, 1:] |= (lab[:, 1:] != lab[:, :-1]) & (lab[:, 1:] >= 0) & (lab[:, :-1] >= 0)
    edge[1:, :] |= (lab[1:, :] != lab[:-1, :]) & (lab[1:, :] >= 0) & (lab[:-1, :] >= 0)
    lay[edge, :3] = (8, 10, 16)
    lay[edge, 3] = 0.45
    if edge_turk:
        tm = lab == 0
        if tm.any():
            d_in = distance_transform_edt(tm)
            d_out = distance_transform_edt(~tm & (lab >= 0))
            e = np.clip(1.8 - np.where(tm, d_in, d_out), 0, 1) * (lab >= 0)
            lay[..., :3] = lay[..., :3] * (1 - e[..., None]) + np.array([255, 110, 125], np.float32) * e[..., None]
            lay[..., 3] = np.maximum(lay[..., 3], e * 0.85)
    a = lay[..., 3]
    if fade is not None:
        a = a * np.clip(fade[:, 0], 0, 1)[:, None]
    if dim is not None:
        a = np.where(dim, a * 0.4, a)
    lay[..., 3] = a
    return Image.fromarray(np.clip(lay * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA")


def largest_remainder(vals, total=100.0, nd=1):
    vals = np.asarray(vals, float)
    if vals.sum() <= 0:
        return np.zeros_like(vals)
    scale = 10 ** nd
    raw = vals / vals.sum() * total * scale
    fl = np.floor(raw)
    rem = int(round(total * scale - fl.sum()))
    order = np.argsort(-(raw - fl))
    fl[order[:rem]] += 1
    return fl / scale
