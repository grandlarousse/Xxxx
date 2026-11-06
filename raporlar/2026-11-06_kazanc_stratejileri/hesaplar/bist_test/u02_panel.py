"""Hisse panelini kurar: temiz getiri, temiz fiyat endeksi, likidite (60g medyan TL hacim) ve gunluk likidite sirasi.
Cikti: scratchpad/data/bist_test/panel_*.parquet + temizlik raporu."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
P = load_stocks(min_days=120)
r, traded, info = clean_returns(P)
first = P["adj"].apply(lambda s: s.first_valid_index())
px = (1 + r.fillna(0)).cumprod().where(P["adj"].ffill().notna())
vol = P["vol_tl"].where(traded, 0.0)
liq = vol.rolling(60, min_periods=40).median()
# son 20 gunde en az 15 gun islem gormus olmali
active = traded.astype(float).rolling(20, min_periods=20).sum() >= 15
hist = P["adj"].notna().cumsum()
liq = liq.where(active & (hist >= 260))
rank = liq.rank(axis=1, ascending=False)
px.to_parquet(f"{DD}/panel_px.parquet"); r.to_parquet(f"{DD}/panel_r.parquet")
rank.to_parquet(f"{DD}/panel_liqrank.parquet"); liq.to_parquet(f"{DD}/panel_liq.parquet")
traded.to_parquet(f"{DD}/panel_traded.parquet")
yr = pd.Series({y: int((first.dt.year == y).sum()) for y in range(2009, 2027)})
info.update({"hisse_sayisi": int(P["adj"].shape[1]), "ilk_tarih_yila_gore": yr.to_dict(),
             "uygun_evren_ort_hisse_sayisi_yila_gore": rank.notna().sum(axis=1).groupby(rank.index.year).mean().round(0).to_dict()})
json.dump(info, open(f"{OUTD}/u02_temizlik.json", "w"), indent=1, default=str)
print(json.dumps(info, indent=0, default=str))
