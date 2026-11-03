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
