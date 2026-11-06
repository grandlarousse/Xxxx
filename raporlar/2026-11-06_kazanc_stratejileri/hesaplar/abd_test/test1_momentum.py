"""TEST 1: Momentum.
 a) UMD (French Mom, uzun-kisa, sifir maliyetli) + RF  -> teminatli uzun-kisa getiri
 b) Volatilite yonetimli UMD (Barroso & Santa-Clara 2015): w_t = hedef_vol / gerceklesen vol (onceki 126 gunluk gunluk Mom), tavan 2x
 c) Sadece-uzun momentum: French 10 Prior(12-2) portfoyu, en ust desil (VW)  -> MTUM/benzeri vekili
 d) Endustri momentumu (sektor ETF rotasyonu vekili): 49 ve 12 endustri VW aylik; son K ay getirisine gore ilk N, esit agirlik,
    aylik yeniden dengeleme; maliyet = tek yon devir * 10 bp. Izgara: K in {3,6,9,12}, atlama {0,1}, N in {3,5,10}.
 e) Endustri momentumu + piyasa 10-ay SMA filtresi (pozisyon disi T-bill)
Tum getiriler aylik, USD, toplam getiri (CRSP). Sinyal t ay sonu, getiri t+1 ay.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from ortak import french_monthly, french_daily, stats, md_table, fmt_pct, OUT

ff, _ = french_monthly("F-F_Research_Data_Factors.csv")
rf = ff["RF"]; mkt = ff["Mkt-RF"] + ff["RF"]
umd, _ = french_monthly("F-F_Momentum_Factor.csv"); umd = umd.iloc[:, 0]
umd_d, _ = french_daily("F-F_Momentum_Factor_daily.csv"); umd_d = umd_d.iloc[:, 0]
dec, t = french_monthly("10_Portfolios_Prior_12_2.csv", 0)
assert "Value" in t
top = dec.iloc[:, -1]
top2 = dec.iloc[:, -2:].mean(axis=1)  # ust %20 vekili (desil 9-10 ortalamasi)

# ---- vol-managed UMD
rv = umd_d.rolling(126).std() * np.sqrt(252)
rv_me = rv.groupby([rv.index.year, rv.index.month]).last()
rv_me.index = pd.to_datetime([f"{y}-{m:02d}-01" for y, m in rv_me.index]) + pd.offsets.MonthEnd(0)
w = (0.12 / rv_me).clip(upper=2.0).shift(1)        # t-1 ay sonundaki vol ile t ayi agirligi
umd_vm = (w.reindex(umd.index) * umd)
# karsilastirilabilir: ayni ortalama volde sabit kaldirac (tam ornek esitleme -> ex-post, sadece bilgi icin)

# ---- endustri momentumu
def ind_mom(R, K, skip, N, cost=0.001, filt=None):
    R = R.copy()
    valid = R.notna()
    lr = np.log1p(R)
    past = lr.shift(skip).rolling(K, min_periods=K).sum()
    rets, turns, idx = [], [], []
    prev_w = None
    dates = R.index
    for i in range(len(dates) - 1):
        d, dn = dates[i], dates[i + 1]
        p = past.loc[d].dropna()
        p = p[valid.loc[dn].reindex(p.index).fillna(False)]
        if len(p) < N * 2:
            continue
        sel = p.nlargest(N).index
        wv = pd.Series(1.0 / N, index=sel)
        inmkt = True if filt is None else bool(filt.get(d, 1.0))
        if not inmkt:
            wv = wv * 0
        r = (wv * R.loc[dn, sel]).sum() + (1 - wv.sum()) * rf.get(dn, 0)
        if prev_w is None:
            to = wv.abs().sum()
        else:
            # kayan agirliklar ihmal; hedefler arasi fark
            allk = wv.index.union(prev_w.index)
            to = (wv.reindex(allk).fillna(0) - prev_w.reindex(allk).fillna(0)).abs().sum() / 2 + abs(wv.sum() - prev_w.sum()) / 2
        r -= to * cost
        rets.append(r); turns.append(to); idx.append(dn)
        prev_w = wv
    return pd.Series(rets, index=idx), pd.Series(turns, index=idx)

I49, t49 = french_monthly("49_Industry_Portfolios.csv", 0); assert "Value Weighted" in t49
I12, t12 = french_monthly("12_Industry_Portfolios.csv", 0); assert "Value Weighted" in t12
ew49 = I49.mean(axis=1)
ew12 = I12.mean(axis=1)

# piyasa 10-ay SMA filtresi (TR endeksiyle)
mi = (1 + mkt).cumprod()
filt = (mi > mi.rolling(10).mean()).astype(float).to_dict()

PER = [("1927-2026 (tam)", "1927-07-31", "2026-12-31"), ("1950-2026", "1950-01-01", "2026-12-31"),
       ("2000-2026", "2000-01-01", "2026-12-31"),
       ("2010-2026", "2010-01-01", "2026-12-31"), ("2020-2026", "2020-01-01", "2026-12-31")]

series = {
    "Piyasa (CRSP VW TR)": mkt,
    "UMD+RF (uzun-kisa, teminatli)": umd + rf,
    "VolYon. UMD+RF (hedef %12)": umd_vm + rf,
    "Mom ust desil VW (sadece uzun)": top,
    "Mom ust %20 VW (sadece uzun)": top2,
}
grid = []
for (nm, R), K, skip, N in itertools.product([("49", I49), ("12", I12)], (3, 6, 9, 12), (0, 1), (3, 5, 10)):
    if nm == "12" and N == 10:
        continue
    r, to = ind_mom(R, K, skip, N)
    for lab, a, b in PER:
        s = stats(r.loc[a:b], rf.loc[a:b])
        if s:
            grid.append(dict(Evren=nm, K=K, skip=skip, TopN=N, Donem=lab, Devir_ay=to.loc[a:b].mean(), **s))
    if (K, skip, N) in [(6, 0, 5), (12, 1, 5)] and nm == "49":
        series[f"Endustri49 mom K={K} skip={skip} top{N}"] = r
    if (K, skip, N) in [(6, 0, 3), (12, 1, 3)] and nm == "12":
        series[f"Endustri12 mom K={K} skip={skip} top{N}"] = r
r_f, _ = ind_mom(I49, 6, 0, 5, filt=filt)
series["Endustri49 K=6 top5 + piyasa 10aySMA"] = r_f
r_f12, _ = ind_mom(I49, 12, 1, 5, filt=filt)
series["Endustri49 K=12 skip1 top5 + piyasa 10aySMA"] = r_f12
series["EW 49 endustri (benchmark)"] = ew49
series["EW 12 endustri (benchmark)"] = ew12

rows = []
for lab, a, b in PER:
    for nm, r in series.items():
        s = stats(r.loc[a:b], rf.loc[a:b])
        if s:
            rows.append(dict(Donem=lab, Strateji=nm, **s))
T = pd.DataFrame(rows)
G = pd.DataFrame(grid)
T.to_csv(os.path.join(OUT, "t1_ozet.csv"), index=False); G.to_csv(os.path.join(OUT, "t1_izgara.csv"), index=False)

# Momentum crash istatistikleri
crash = umd.nsmallest(8)
vm_crash = umd_vm.reindex(crash.index)
md = ["\n#### Momentum: ozet (aylik, USD, toplam getiri; endustri stratejileri 10 bp/devir maliyetli)\n",
      md_table(T[["Donem", "Strateji", "CAGR", "Vol", "Sharpe", "MaxDD", "EnKotuYil", "EnKotuYilT", "ExcessCAGR"]])]
agg = G.groupby(["Evren", "Donem"]).agg(CAGR_med=("CAGR", "median"), CAGR_min=("CAGR", "min"), CAGR_max=("CAGR", "max"),
                                        Sharpe_med=("Sharpe", "median"), MaxDD_med=("MaxDD", "median"),
                                        Devir_med=("Devir_ay", "median"), n=("CAGR", "size")).reset_index()
for c in ["CAGR_med", "CAGR_min", "CAGR_max", "MaxDD_med", "Devir_med"]:
    agg[c] = agg[c].map(fmt_pct)
agg["Sharpe_med"] = agg["Sharpe_med"].map(lambda x: f"{x:.2f}")
md += ["\n#### Endustri momentum izgarasi (K 3/6/9/12 x skip 0/1 x N): medyan [min,max]\n", md_table(agg, pct_cols=())]
# benchmark ile fark: medyan izgara CAGR - EW endustri CAGR
bm = T[T.Strateji.str.startswith("EW")].set_index(["Strateji", "Donem"])["CAGR"]
mk = T[T.Strateji.str.startswith("Piyasa")].set_index("Donem")["CAGR"]
diff = []
for (ev, dn), g in G.groupby(["Evren", "Donem"]):
    b = bm.get((f"EW {ev} endustri (benchmark)", dn), np.nan)
    diff.append(dict(Evren=ev, Donem=dn, Medyan_CAGR=g.CAGR.median(), EW_bench=b, Piyasa=mk.get(dn, np.nan),
                     Fark_EW=g.CAGR.median() - b, Fark_Piyasa=g.CAGR.median() - mk.get(dn, np.nan),
                     Pay_pozitif_vs_piyasa=(g.CAGR > mk.get(dn, np.nan)).mean()))
D = pd.DataFrame(diff)
for c in ["Medyan_CAGR", "EW_bench", "Piyasa", "Fark_EW", "Fark_Piyasa", "Pay_pozitif_vs_piyasa"]:
    D[c] = D[c].map(fmt_pct)
md += ["\n#### Endustri momentum: izgara medyani benchmark'a gore\n", md_table(D, pct_cols=())]
cr = pd.DataFrame({"Ay": crash.index.strftime("%Y-%m"), "UMD": crash.values, "VolYon_UMD": vm_crash.values})
cr["UMD"] = cr["UMD"].map(fmt_pct); cr["VolYon_UMD"] = cr["VolYon_UMD"].map(fmt_pct)
md += ["\n#### En kotu 8 UMD ayi (momentum crash) ve vol-yonetimli karsiligi\n", md_table(cr, pct_cols=())]
# UMD on yillik ortalama
dec_ = (umd.groupby((umd.index.year // 10) * 10).agg(lambda x: (1 + x).prod() ** (12 / len(x)) - 1))
dvm = (umd_vm.dropna().groupby((umd_vm.dropna().index.year // 10) * 10).agg(lambda x: (1 + x).prod() ** (12 / len(x)) - 1))
dd = pd.DataFrame({"On yil": dec_.index, "UMD yillik": dec_.values, "VolYon UMD yillik": dvm.reindex(dec_.index).values})
dd["UMD yillik"] = dd["UMD yillik"].map(fmt_pct); dd["VolYon UMD yillik"] = dd["VolYon UMD yillik"].map(fmt_pct)
md += ["\n#### UMD on yillara gore (yillik bilesik, RF haric prim)\n", md_table(dd, pct_cols=())]
open(os.path.join(OUT, "t1_tablolar.md"), "w").write("\n".join(md))
print("\n".join(md))
