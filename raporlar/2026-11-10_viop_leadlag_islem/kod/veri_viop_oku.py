"""Bulten dosyalarini tek DataFrame'e cevirir. python3 -I veri_viop_oku.py <VERI_DIR>  -> panel/viop_gunluk.parquet"""
import sys, glob, io, os
import pandas as pd, numpy as np
V = sys.argv[1]
M = {"TARIH": "date", "SOZLESME KODU": "code", "SOZLESME ADI": "name", "PAZAR SEGMENTI": "seg", "DAYANAK VARLIK": "und_raw", "VADE TARIHI": "expiry",
     "UZLASMA FIYATI": "settle", "ONCEKI UZLASMA FIYATI": "prev_settle", "ACILIS FIYATI": "open", "EN YUKSEK FIYAT": "high", "EN DUSUK FIYAT": "low",
     "KAPANIS FIYATI": "close", "AGIRLIKLI ORTALAMA FIYAT": "vwap", "ISLEM HACMI": "value_tl", "ISLEM MIKTARI": "volume", "ISLEM SAYISI": "trades", "ACIK POZISYON": "oi"}
def num(s):
    s = s.astype(str).str.strip()
    return pd.to_numeric(s.str.replace(",", ".", regex=False), errors="coerce")
parts = []
for f in sorted(glob.glob(f"{V}/raw/viop/viop_*.csv")):
    d = pd.read_csv(f, sep=";", encoding="cp1254", skiprows=[1], dtype=str)
    d.columns = [c.strip() for c in d.columns]
    d = d[[c for c in M if c in d.columns]].rename(columns=M)
    d = d[d["code"].astype(str).str.startswith("F_")]
    parts.append(d)
x = pd.concat(parts, ignore_index=True)
x["date"] = pd.to_datetime(x["date"]); x["expiry"] = pd.to_datetime(x["expiry"])
for c in ["settle", "prev_settle", "open", "high", "low", "close", "vwap", "value_tl", "volume", "trades", "oi"]:
    x[c] = num(x[c])
u = x["und_raw"].str.strip()
u = u.str.replace(r"\.E$", "", regex=True).replace({"D_XU030D": "XU030", "D_XLBNKD": "XLBNK"}).str.replace(r"^D_", "", regex=True)
x["und"] = u
x = x.sort_values(["date", "code"]).reset_index(drop=True)
os.makedirs(f"{V}/panel", exist_ok=True)
x.to_parquet(f"{V}/panel/viop_gunluk.parquet")
print(len(x), x["date"].min(), x["date"].max(), x["date"].nunique())
