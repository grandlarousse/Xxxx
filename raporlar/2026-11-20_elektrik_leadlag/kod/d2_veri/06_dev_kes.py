"""panel_dev: viop_daily, viop_front, snap, h1/ ve h1_isy/ dosyalarının CUT (2025-06-30, dahil) tarihinde kesilmiş kopyası.
m5 ve m5_isy yalnız panel_full'da kalır. viop_front'taki ileri getiriler (ret_settle_f1..f3) kesim sonrasına taşıyorsa NaN yapılır.
Sonda denetim: panel_dev altındaki her parquet'te CUT sonrası satır sayısı = 0 olmalı.  Kullanım: python3 -I 06_dev_kes.py"""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import FULL, DEV, CUT
cut = pd.Timestamp(CUT); cut_end = cut + pd.Timedelta(days=1)
for name in ("viop_daily", "viop_front", "snap"):
    x = pd.read_parquet(f"{FULL}/{name}.parquet"); x = x[x["date"] <= cut].copy()
    if name == "viop_front":
        days = np.sort(x["date"].unique())   # ileri getiri t+h > CUT ise gizle
        for h in (1, 2, 3):
            x.loc[x["date"] > days[-1 - h], f"ret_settle_f{h}"] = np.nan
    x.reset_index(drop=True).to_parquet(f"{DEV}/{name}.parquet", index=False)
for sub in ("h1", "h1_isy"):
    os.makedirs(f"{DEV}/{sub}", exist_ok=True)
    for f in glob.glob(f"{DEV}/{sub}/*.parquet"): os.remove(f)
    for f in sorted(glob.glob(f"{FULL}/{sub}/*.parquet")):
        x = pd.read_parquet(f); x = x[x["ts_tr"] < cut_end]
        if len(x): x.reset_index(drop=True).to_parquet(f"{DEV}/{sub}/{os.path.basename(f)}", index=False)
bad = 0; n = 0
mine = [f"{DEV}/{n}.parquet" for n in ("viop_daily", "viop_front", "snap")] + sorted(glob.glob(f"{DEV}/h1/*.parquet")) + sorted(glob.glob(f"{DEV}/h1_isy/*.parquet"))
for f in mine:   # yalnız D2'nin dosyaları denetlenir (D1'in dosyaları D1'in sorumluluğunda)
    x = pd.read_parquet(f); n += 1
    for c in x.columns:
        if str(x[c].dtype).startswith("datetime") and c != "vade":
            k = int((x[c] >= cut_end + (pd.Timedelta(hours=-3) if c == "ts_utc" else pd.Timedelta(0))).sum())
            if k: bad += k; print("KESIM IHLALI", f, c, k)
    if os.path.basename(f) in ("viop_daily.parquet", "viop_front.parquet", "snap.parquet"): print(os.path.basename(f), len(x), x["date"].max().date())
print("panel_dev D2 parquet", n, "| kesim sonrasi satir", bad, "| m5 klasoru var mi:", os.path.exists(f"{DEV}/m5") or os.path.exists(f"{DEV}/m5_isy"))
