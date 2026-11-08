"""Ek kontroller: QEND penceresinde vade (LBMA PM nihai uzlaşma) bulaşması; al-tut OOS Sharpe farkı; NFP 2010-2026 spot birleşik."""
import numpy as np, pandas as pd
from rlib import *
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; O = f"{S}/out/a3_takvim_olay_rep"
B = pd.read_parquet(f"{O}/base.parquet"); V = B.index; r = B.ret
L = pd.read_parquet(f"{S}/panel/viop_long.parquet"); x = L[(L.root == "XAUUSD") & L.code.str.startswith("F_XAUUSD")]
exp = x.groupby("code").expiry.first().pipe(pd.to_datetime)
g = pd.Series(np.arange(len(V)), index=V).groupby([V.year, V.month]); tde = (g.transform("size") - g.cumcount() - 1).values
ev = np.where(np.isin(V.month, [3, 6, 9, 12]) & (tde == 1))[0]
bad = []
for i in ev:
    for k in range(1, 4):
        if i + k < len(V):
            c = B.code.iloc[i + k]
            if exp[c] == V[i + k]: bad.append((V[i].date(), V[i + k].date(), c))
print("QEND pencerelerinde aktif kontratın vade günü getirisi:", bad)
dte = [(exp[B.code.iloc[i]] - V[i]).days for i in ev]; print("QEND olay günü aktif kontrat vadeye kalan gün min/medyan:", min(dte), np.median(dte))
oos = V > IS_END; ro = r[oos]
print("al-tut OOS Sharpe tüm günler %.3f, ilk OOS günü hariç %.3f" % (ro.mean() / ro.std() * np.sqrt(252), ro.iloc[1:].mean() / ro.iloc[1:].std() * np.sqrt(252)))
# NFP spot 2010-2026 birleşik ve 2010-2021 birleşik
SP = pd.read_parquet(f"{O}/spot_daily.parquet"); NFP = pd.to_datetime(pd.read_csv(f"{O}/cal_nfp.csv").date)
evs = [d for d in NFP if d in set(SP.index)]
xs = pd.Series(np.nan, index=SP.index); xs.loc[evs] = np.log(SP.p15 / SP.p12).reindex(evs).values
for lo, hi in [("2010-01-01", "2026-12-31"), ("2010-01-01", "2021-12-31")]:
    m = (SP.index >= lo) & (SP.index <= hi)
    for h in (1, 3):
        o = cond_test(xs[m], SP[f"sfwd{h}"][m], h); print(f"spot NFP {lo[:4]}-{hi[:4]} h{h}:", fmt(o, ["n_full", "ic_full", "tIC_full", "sgn_mean_full", "t_sgnreg_full"]))
# QEND olay başına net getiri dağılımı ve en iyi/kötü
D = pd.Series(0.0, index=V); D.iloc[ev] = 1
e = B.fwd3.iloc[ev] * 1e4
print("QEND olay fwd3: pozitif %d/%d, ort %.1f, medyan %.1f, std %.1f" % ((e > 0).sum(), len(e), e.mean(), e.median(), e.std()))
# NFP: IS'te yön seçimi ne kadar sağlam? IS işaret ortalamasının bootstrap olasılığı > 0
pnl_is = None

# ---- birleşik spot 2010-2026: OG, Ocak, Bayram ----
SPI = SP.index
OG = pd.read_csv(f"{O}/cal_og.csv", parse_dates=["og"])
p = np.searchsorted(SPI.values, OG.og[(OG.og >= SPI[0]) & (OG.og <= SPI[-1])].values); p = p[(p > 0) & (p < len(SPI))]
Dog = pd.Series(0.0, index=SPI); Dog.iloc[np.unique(p - 1)] = 1
print("spot OG 2010-2026:", fmt(dummy_test(Dog, SP.sfwd1, 1), ["n_ev", "diff_full", "t_full", "yrs_same"]))
nms = pd.Series(np.r_[SPI.month[1:], [0]], index=SPI)
print("spot Ocak 2010-2026:", fmt(dummy_test((nms == 1).astype(float), SP.sfwd1, 1), ["n_ev", "diff_full", "t_full", "yrs_same"]))
k = SPI < "2026-01-01"; print("spot Ocak 2010-2025:", fmt(dummy_test((nms == 1).astype(float)[k], SP.sfwd1[k], 1), ["n_ev", "diff_full", "t_full", "yrs_same"]))
BY = pd.read_csv(f"{O}/cal_bayram.csv", parse_dates=["start"])
ends = BY.start + pd.to_timedelta(BY.ndays, unit="D"); ps = [SPI[SPI >= e][0] for e in ends if SPI[0] <= e <= SPI[-1]]
Db = pd.Series(0.0, index=SPI); Db.loc[ps] = 1
print("spot Bayram sonrası 2010-2026:", fmt(dummy_test(Db, SP.sfwd5, 5), ["n_ev", "diff_full", "t_full", "yrs_same"]))
# NFP OOS içinde en kârlı 5 olay hariç
B2 = B; NFPv = [d for d in NFP if d in set(V)]
half = set(pd.to_datetime(pd.read_csv(f"{O}/cal_halfdays.csv").date))
xv = pd.Series(np.nan, index=V); ok = [d for d in NFPv if d not in half]; xv.loc[ok] = np.log(B.p15 / B.p12).reindex(ok).values
for h in (1, 3):
    pnl = (np.sign(xv) * B[f"fwd{h}"]).dropna() * 1e4; po = pnl[pnl.index > IS_END]
    tb = po.drop(po.sort_values().index[-5:]); print(f"NFP h{h} OOS: n={len(po)} ort {po.mean():.1f} t {mean_t(po, 0):.2f}; en kârlı 5 hariç ort {tb.mean():.1f} t {mean_t(tb, 0):.2f}")
