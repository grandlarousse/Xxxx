"""Adım 6: VİOP pay vadelisi likiditesi (işlenebilirlik). Ortak dizindeki BIST VİOP günlük bültenlerinden (data/viop/, başka ajan indiriyor;
yeniden indirme yok) 47 dayanak için son 12 ayın günlük toplam işlem hacmi (TL), işlem sayısı, açık pozisyon; spot TL hacmiyle oran.
Çıktı: res/viop_liq.csv
"""
import sys, os, glob, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
files = sorted(glob.glob(hdata.SCR + "/data/viop/viop_*.csv"))
files = [f for f in files if os.path.basename(f)[5:13] >= "20251101"]
rows = []
for f in files:
    try:
        d = pd.read_csv(f, sep=";", encoding="windows-1254", skiprows=[1], dtype=str)
    except Exception as e:
        continue
    d.columns = [c.strip() for c in d.columns]
    d = d[d["PAZAR SEGMENTI"].str.strip() == "SSF"] if "PAZAR SEGMENTI" in d else d
    d = d[d["SOZLESME KODU"].str.startswith("F_")]
    d["und"] = d["DAYANAK VARLIK"].str.replace(".E", "", regex=False).str.strip()
    for c in ["ISLEM HACMI", "ISLEM SAYISI", "ACIK POZISYON", "UZLASMA FIYATI"]:
        d[c] = pd.to_numeric(d[c].str.replace(",", "."), errors="coerce")
    g = d.groupby("und").agg(vol=("ISLEM HACMI", "sum"), trades=("ISLEM SAYISI", "sum"))
    d["oi_tl"] = d["ACIK POZISYON"] * d["UZLASMA FIYATI"] * 100  # sözleşme büyüklüğü genelde 100 pay
    g["oi_tl"] = d.groupby("und")["oi_tl"].sum()
    g["date"] = os.path.basename(f)[5:13]
    rows.append(g.reset_index())
if rows:
    A = pd.concat(rows)
    S = A.groupby("und").agg(days=("date", "nunique"), vol_med_mnTL=("vol", lambda x: x.median() / 1e6), trades_med=("trades", "median"), oi_med_mnTL=("oi_tl", lambda x: x.median() / 1e6))
    liq = hdata.load()["liq"]
    tov = hdata.load()["tov"]; spot = tov[tov.index >= pd.Timestamp("2025-11-01")].median() / 1e6
    S["spot_tov_med_mnTL"] = spot.reindex(S.index)
    S["fut_to_spot"] = S.vol_med_mnTL / S.spot_tov_med_mnTL
    S = S[S.index.isin(hdata.VIOP)].sort_values("vol_med_mnTL", ascending=False)
    S.to_csv(os.path.join(hdata.RES, "viop_liq.csv"))
    print(f"bülten günü: {A.date.nunique()} ({A.date.min()}..{A.date.max()})"); print(S.round(2).to_string())
