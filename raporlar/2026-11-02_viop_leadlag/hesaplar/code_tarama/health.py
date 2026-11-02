"""ZAMANLAMA SAĞLIK KONTROLÜ: her sürücü için corr(XU100_t, d_{t+1}) (lag -1), lag0, lag1 ve 47 hisse medyanı.
Bayrak: |lag-1| > |lag0| (sürücü 'gelecekte' daha iyi korele -> zaman etiketi kayması şüphesi). Asya/during kovalarında
kısmen beklenir (Asya t+1 seansı BIST t seansıyla çakışır), ABD/AB/FX kovalarında ALARM.
Çıktı: cache/health_timing.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
P, DP = load_panels(); dm = pd.read_parquet(CACHE + "/driver_meta.parquet")
M = pd.read_parquet(OUT + "/tarama_matrix.parquet"); V = M[~M.is_index_row]
xu = P["XU100.IS"]; X = P[dm.index]
from tlib import mcorr
out = pd.DataFrame(index=dm.index)
for k in [-1, 0, 1]:
    c, n, t, _ = mcorr(xu.values[:, None], X.shift(k).values); out[f"xu_lag{k}"] = c[0]; out[f"t_xu_lag{k}"] = t[0]
g = V.groupby("driver")
out["med_abs_sync"] = g["sync_full"].apply(lambda s: s.abs().median()); out["med_abs_rev"] = g["rev_full"].apply(lambda s: s.abs().median())
out["bucket"] = dm["bucket"]; out["group"] = dm["group"]; out["sparse"] = dm["sparse"]
out["flag_xu"] = (out["xu_lag-1"].abs() > out["xu_lag0"].abs()) & (out["t_xu_lag-1"].abs() > 2)
out["flag_med"] = out["med_abs_rev"] > out["med_abs_sync"]
out["ALARM"] = (out["flag_xu"] | out["flag_med"]) & out["bucket"].isin(["us", "eu"]) & ~out["sparse"]
out.round(4).to_csv(CACHE + "/health_timing.csv")
print("bayrak (tüm):", int((out.flag_xu | out.flag_med).sum()), "| ALARM (us/eu, seyrek değil):", int(out.ALARM.sum()))
print(out[out.ALARM][["bucket", "group", "xu_lag-1", "xu_lag0", "xu_lag1", "med_abs_sync", "med_abs_rev"]].round(3).head(30).to_string())
print(out[(out.flag_xu | out.flag_med) & ~out.ALARM].groupby("bucket").size().to_string())
