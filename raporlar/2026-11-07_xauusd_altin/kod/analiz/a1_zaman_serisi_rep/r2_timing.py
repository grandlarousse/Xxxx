#!/usr/bin/env python3
"""Adım 2: Uzlaşma anının (τ) ham verilerle doğrulanması — yıl yıl.
Mantık: v_ret_t = ln(settle_t/settle_{t-1}) ≈ spot(τ_t) − spot(τ_{t-1}). Gün t'nin saatlik spot getirisi [a,b] aralığı τ_t'den ÖNCE ise
v_ret_t katsayısı ≈1 ve v_ret_{t+1} katsayısı ≈0; SONRA ise tersi. 14→15 UTC barının v_ret_{t+1} katsayısı > 0 çıkarsa uzlaşma 15:00'ten önce
demektir (=15:00 spot sinyali ileriye bakar). Ayrıca dakikalık örnek günlerde uzlaşmaya en yakın dakika-VWAP penceresi.
Yarım gün (arife) tespiti: settle_t, gün t 09-10 UTC spotuna 15:00 spotundan belirgin şekilde daha yakınsa.
"""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a1_zaman_serisi_rep"
B = pd.read_parquet(f"{OUT}/base.parquet"); HR = pd.read_parquet(f"{OUT}/spot_hours.parquet")
lh = np.log(HR)
seg = pd.DataFrame({f"{a}-{a+1}": lh[a + 1] - lh[a] for a in range(10, 19)})  # gün t saatlik getiriler
seg.columns = [f"r{c}" for c in seg.columns]
D = B[["v_ret"]].join(seg, how="inner")
D["v_next"] = B.v_ret.shift(-1).reindex(D.index)
import statsmodels.api as sm
rows = []
for y, g in D.groupby(D.index.year):
    g = g.dropna()
    if len(g) < 60: continue
    for tgt in ["v_ret", "v_next"]:
        m = sm.OLS(g[tgt], sm.add_constant(g[seg.columns])).fit()
        rows.append(dict(year=y, target=tgt, n=len(g), **{c: round(m.params[c], 2) for c in seg.columns}))
T = pd.DataFrame(rows); T.to_csv(f"{OUT}/timing_regression.csv", index=False)
print("Katsayılar (gün t saatlik spot getirisi → v_ret_t / v_ret_{t+1}). r14-15 = 14:00→15:00 UTC.")
print(T.to_string(index=False))

# dakikalık örnek günler: settle'a en yakın 10 dk pencere (bazı yok etmek için ertesi günün farkı yerine gün içi: settle - VWAP(pencere) ile
# 'baz' = settle/close_spot oranının gün içindeki tutarlılığı ölçülemez; bunun yerine iki ardışık örnek günde değil, her gün için
# (settle_t / spot_window) − medyan(settle/spot_15:10) sapmasının MAD'i).
M = pd.read_parquet(f"{S}/panel/duka_min_XAUUSD.parquet"); M.index = pd.DatetimeIndex(M.index)
M["d"] = M.index.normalize()
res = []
for (d, g) in M.groupby("d"):
    if d not in B.index or not np.isfinite(B.at[d, "settle"]): continue
    g = g.set_index(g.index + pd.Timedelta(minutes=1))  # fiyat anı = bar başlangıcı + 1 dk
    for hhmm in ["09:00", "09:30", "10:00", "14:00", "14:30", "14:45", "14:50", "15:00", "15:10", "15:15", "15:30", "16:00", "17:00"]:
        t = d + pd.Timedelta(hours=int(hhmm[:2]), minutes=int(hhmm[3:]))
        w = g.c[(g.index > t - pd.Timedelta(minutes=5)) & (g.index <= t + pd.Timedelta(minutes=5))]
        if len(w) >= 3:
            res.append(dict(d=d, year=d.year, at=hhmm, lb=np.log(B.at[d, "settle"] / w.mean())))
R = pd.DataFrame(res)
# baz yavaş değişir; günler arası değil, her gün için baz ~ carry. Kontrat bazını gidermek için: aynı gün farklı saatler arası kıyas,
# günün medyan bazından sapma değil; doğrudan |lb − medyan_yıl(lb@15:10)| ölç.
piv = R.pivot_table(index=["d", "year"], columns="at", values="lb")
ref = piv["15:10"].groupby(level="year").transform("median")
mad = (piv.sub(ref, axis=0)).abs().groupby(level="year").median() * 1e4
print("\nDakikalık örnek günlerde |ln(settle/spot±5dk) − yıl medyanı(15:10)| medyanı (bps), yıl yıl:")
print(mad.round(1).to_string())

# yarım gün / erken uzlaşma tespiti (saatlik): settle_t 'baz' sapması
lb = pd.DataFrame({hh: np.log(B.settle) - lh[hh].reindex(B.index) for hh in [10, 11, 12, 13, 14, 15, 16]})
base = lb[15].rolling(21, center=True, min_periods=5).median()
dev = lb.sub(base, axis=0).abs() * 1e4
early = dev[[10, 11, 12]].min(axis=1) + 5 < dev[[15, 16]].min(axis=1)
E = dev[early].round(1); E["code"] = B.code
print("\nErken uzlaşma şüphesi (10-12 UTC spotu 15-16 UTC'den ≥5 bps daha yakın):", int(early.sum()), "gün")
print(E.to_string())
pd.Series(early[early].index).to_csv(f"{OUT}/early_settle_days.csv", index=False)
