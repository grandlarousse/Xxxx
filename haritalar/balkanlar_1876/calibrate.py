#!/usr/bin/env python3
"""Bulgaristan il (oblast) bazında 1875 Bulgar oranı hedefleriyle karşılaştırma.

Hedef: kullanıcının verdiği 1875 '% Bulgar' haritası. Karşılaştırma,
haritada çizilen noktalar (veya küme nüfusları) üzerinden yapılır:
Hristiyan payı ≈ Bulgar payı + (Rum, Gagavuz, Ulah vb. küçük pay).
"""
import os
import sys
import glob

import numpy as np
import geopandas as gpd
import shapely

import engine as E

TARGET_BG = {
    "Vidin": 73, "Montana": 75, "Vratsa": 76, "Pleven": 58, "Lovech": 76, "Gabrovo": 93,
    "Veliko Tarnovo": 60, "Ruse": 38, "Razgrad": 37, "Silistra": 27, "Dobrich": 25,
    "Targovishte": 40, "Shumen": 43, "Varna": 25, "Burgas": 54, "Sliven": 64, "Yambol": 60,
    "Stara Zagora": 75, "Plovdiv": 64, "Pazardzhik": 71, "Smolyan": 38, "Kardzhali": 3,
    "Haskovo": 42, "Grad Sofiya": 42, "Sofia": 86, "Pernik": 90, "Kyustendil": 88,
    "Blagoevgrad": 55,
}
TOTAL_BG = 55.8


def oblasts():
    p = os.path.join(E.CACHE, "ne_10m_admin_1_states_provinces.shp")
    g = gpd.read_file(p, where="adm0_a3='BGR'").to_crs(E.CRS)
    return {r["name"]: r.geometry for _, r in g.iterrows()}


def compare_dots(frame, x, y, k, verbose=True):
    """Noktalardan il bazında Türk/diğer Müslüman/Hristiyan payları."""
    X = frame.x0 + x * frame.mpp
    Y = frame.y1 - y * frame.mpp
    obl = oblasts()
    rows, tot = [], np.zeros(3)
    for name, geom in obl.items():
        inside = shapely.contains_xy(geom, X, Y)
        cnt = np.bincount(k[inside], minlength=3).astype(float)
        tot += cnt
        if cnt.sum() == 0:
            continue
        sh = 100 * cnt / cnt.sum()
        rows.append((name, TARGET_BG[name], sh[2], sh[0], sh[1], int(cnt.sum())))
    if verbose:
        print(f"{'il':16s} hedef%Bulgar  harita%Hrist  Türk  dMüs   nokta  fark")
        for name, tg, ch, tu, mo, n in sorted(rows, key=lambda r: r[2] - r[1]):
            flag = "  <-- " if (ch - tg) > 12 or (ch - tg) < -3 else ""
            print(f"{name:16s} {tg:10.0f} {ch:13.1f} {tu:6.1f} {mo:5.1f} {n:7d} {ch - tg:+5.1f}{flag}")
        s = 100 * tot / tot.sum()
        print(f"{'BULGARİSTAN':16s} {TOTAL_BG:10.1f} {s[2]:13.1f} {s[0]:6.1f} {s[1]:5.1f} {int(tot.sum()):7d} {s[2] - TOTAL_BG:+5.1f}")
    return rows


# Bulgar dışı Hristiyanlar (Rum, Gagavuz, Ulah, Ermeni...) için hedefe eklenen pay;
# Sofya şehrinde Yahudiler paydan çıkarıldığı için Hristiyan payı daha yüksek çıkar.
ALLOW = {"Varna": 6, "Burgas": 6, "Plovdiv": 4, "Dobrich": 4, "Vidin": 6, "Grad Sofiya": 8,
         "Silistra": 3, "Ruse": 4, "Montana": 3, "Blagoevgrad": 3, "Stara Zagora": 2,
         "Pazardzhik": 2, "Haskovo": 2, "Yambol": 2, "Sliven": 2, "Shumen": 2}


def _logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


def footprint_matrix(clusters, frame, land_mask, elev, grid_step=2.0, kernel_cut=1.7):
    """F[i, o]: küme i nüfusunun o iline düşen payı (beklenen değer)."""
    obl = oblasts()
    names = list(obl)
    ids = np.full(land_mask.shape, -1, np.int16)
    for oi, n in enumerate(names):
        ids[E.rasterize(obl[n], frame, grid_step)[:ids.shape[0], :ids.shape[1]]] = oi
    suit = E.suitability(frame, land_mask, elev, grid_step)
    Fm = np.zeros((len(clusters), len(names)))
    for i, c in enumerate(clusters):
        fp = E.footprint(c, frame, suit, land_mask, grid_step, kernel_cut)
        if fp is None:
            continue
        II, JJ, w = fp
        o = ids[II, JJ]
        m = o >= 0
        if m.any():
            Fm[i] = np.bincount(o[m], weights=w[m], minlength=len(names))
    return names, Fm


def auto_calibrate(clusters, frame, land_mask, elev, iters=60, eta=0.6, tol=1.0, verbose=True):
    """Bulgaristan'daki kümelerin Hristiyan payını il hedeflerine yaklaştırır.

    Kümelerin il bazındaki beklenen nüfus dağılımı (F) bir kez hesaplanır;
    sonra her ilin hatası, o ile nüfus düşüren kümelere düşen pay oranında
    logit uzayında dağıtılır. Türk / diğer Müslüman oranı her kümede korunur.
    """
    names, Fm = footprint_matrix(clusters, frame, land_mask, elev)
    target = np.array([TARGET_BG[n] + ALLOW.get(n, 1) for n in names], float) / 100
    P = np.array([E.cluster_population(c) for c in clusters])
    ch = np.array([c["christian"] for c in clusters], float) / 100
    mus = np.array([c["turk"] + c["muslim_other"] for c in clusters], float)
    W = P[:, None] * Fm                      # kişi
    tot = W.sum(0)
    active = W.sum(1) > 0
    lg = _logit(ch)
    for it in range(iters):
        cur = 1 / (1 + np.exp(-lg))
        comp = (W * cur[:, None]).sum(0) / np.maximum(tot, 1)
        err = comp - target
        err[tot < 1000] = 0
        if verbose and (it % 10 == 0 or it == iters - 1):
            print(f"  kalibrasyon turu {it}: en büyük sapma {100 * np.abs(err).max():.1f} puan")
        if np.abs(err).max() * 100 < tol:
            break
        share_in = np.divide(W, W.sum(1, keepdims=True), out=np.zeros_like(W), where=W.sum(1, keepdims=True) > 0)
        adj = (share_in * (_logit(target) - _logit(np.clip(comp, 0.005, 0.995)))[None, :]).sum(1)
        lg = np.where(active, lg + eta * adj, lg)
    new = 1 / (1 + np.exp(-lg))
    changed = 0
    for i, c in enumerate(clusters):
        if not active[i] or abs(new[i] - ch[i]) < 1e-4:
            continue
        changed += 1
        nc = 100 * float(new[i])
        if mus[i] > 0:
            f = (100 - nc) / mus[i]
            c["turk"] *= f
            c["muslim_other"] *= f
        else:
            c["turk"] = 100 - nc
        c["christian"] = nc
        s = np.array([c[kk] for kk in E.CATS])
        c["shares"] = s / s.sum()
    if verbose:
        print(f"  {changed} küme ayarlandı")
    return clusters
