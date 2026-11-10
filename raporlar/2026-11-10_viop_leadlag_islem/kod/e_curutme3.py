"""e_: USDTRY sinyal gunlerinde XU030 ve hedef-beta*XU030 (piyasa etkisi mi?). python3 -I e_curutme3.py"""
import math, numpy as np, pandas as pd
V = "/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/"
EK = "/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/"
def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x); return x.mean() / (x.std(ddof=1) / math.sqrt(n))
def d(x): x = np.asarray(x, float); x = x[np.isfinite(x)]; return f"n={len(x)} ort={x.mean():.1f} t={tt(x):.2f}"
fr = pd.read_parquet(V + "fut_ret.parquet"); cal = pd.DatetimeIndex(fr.index).normalize(); fr.index = cal; N = len(cal); pos = {t: i for i, t in enumerate(cal)}
x3 = fr["XU030"].where(fr["XU030"].abs() < 0.5)
t = pd.read_csv(EK + "islemler_b1.csv", sep=";", parse_dates=["giris_tarihi"])
for cift, sg in (("FROTO<-VIOP:USDTRY", "S_KUL"), ("ENKAI<-VIOP:USDTRY", "S_ONCU")):
    h = cift.split("<-")[0]; x = t[(t.cift == cift) & (t.sinyal == sg)]
    ei = np.array([pos[pd.Timestamp(v)] for v in x.giris_tarihi]); y = x.yon.values
    b = (fr[h].rolling(250, min_periods=120).cov(x3) / x3.rolling(250, min_periods=120).var()).shift(1).values
    xu = x3.values; f = fr[h].values
    xu2 = 1e4 * y * (xu[np.minimum(ei + 1, N - 1)] + xu[np.minimum(ei + 2, N - 1)]) ; hg = x.brut_bps.values - b[ei] * xu2
    print(cift, sg, "hedef", d(x.brut_bps), "| XU030 ayni pencere", d(xu2), "| beta-hedge'li", d(hg), "| beta ort", np.nanmean(b[ei]).round(2))
    s2 = x.giris_tarihi.values >= np.datetime64("2024-11-10"); print("   SON2Y hedge'li", d(hg[s2]))
