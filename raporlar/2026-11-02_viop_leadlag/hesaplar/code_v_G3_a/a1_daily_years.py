"""A1: Yahoo günlük ham veriden XU030/XU100/XU050 ve 47 hisse gece (gap) / gün-içi (intra) yıllık kırılım.
Ayrıca 'açılışta sat, kapanışta kapat' (=-intra) brüt/net, IS 2014-2020 / OOS 2021-2026."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
R = S + "/out/code_v_G3_a/res"
pd.set_option("display.width", 250)
rows = []
for sym in ["XU030.IS", "XU100.IS", "XU050.IS", "XBANK.IS", "XUSIN.IS"]:
    x = decomp(sym)
    print(sym, "n", x["intra"].notna().sum(), "badopen/NaN gün", x["intra"].isna().sum())
    for y, g in x.groupby(x.index.year):
        rows.append(dict(sym=sym, year=y, n=g.intra.notna().sum(), gap=1e4*g.gap.mean(), intra=1e4*g.intra.mean(), cc=1e4*g.cc_p.mean(),
                         t_intra=tstat(g.intra), sd_intra=1e4*g.intra.std(), gap_eq0=(g.gap.abs() < 1e-9).mean()))
Y = pd.DataFrame(rows)
for sym, g in Y.groupby("sym"):
    print("\n==", sym); print(g.set_index("year")[["n", "gap", "intra", "cc", "t_intra", "sd_intra", "gap_eq0"]].round(2).T.to_string())
    print("gap>0 yıl:", (g.gap > 0).sum(), "/", len(g), " intra<0 yıl:", (g.intra < 0).sum(), "/", len(g))
Y.to_csv(R + "/a1_years_idx.csv", index=False)

# Tam dönem + IS/OOS + maliyet
def summ(x, label):
    out = []
    for nm, sl in [("2014-2026", slice("2014", "2026")), ("IS 2014-2020", slice("2014", "2020")), ("OOS 2021-2026", slice("2021", "2026")),
                   ("2023-12..2026-10 (h1 dönemi)", slice("2023-12-01", "2026-10-31")), ("IS<2025-07", slice("2023-12-01", "2025-06-30")), ("OOS>=2025-07", slice("2025-07-01", "2026-10-31"))]:
        s = -x["intra"].loc[sl].dropna()
        out.append(dict(sym=label, per=nm, n=len(s), gross_bps=1e4*s.mean(), t=tstat(s), t_nw=nw_t(s), net2=1e4*s.mean()-2, net4=1e4*s.mean()-4, net8=1e4*s.mean()-8,
                        sharpe_net4=(s.mean()-4e-4)/s.std()*np.sqrt(250), hit=(s > 0).mean(), gap_bps=1e4*x["gap"].loc[sl].mean()))
    return out
rr = []
for sym in ["XU030.IS", "XU100.IS", "XU050.IS"]:
    rr += summ(decomp(sym), sym)
T = pd.DataFrame(rr); print("\n", T.round(3).to_string()); T.to_csv(R + "/a1_bt_idx.csv", index=False)

# 47 hisse
rows = []; P = {}
for s in STOCKS:
    try:
        x = decomp(s + ".IS")
    except Exception as e:
        print("yok", s, e); continue
    P[s] = x
    for y, g in x.groupby(x.index.year):
        rows.append(dict(stock=s, year=y, n=g.intra.notna().sum(), gap=1e4*g.gap.mean(), gap_tr=1e4*g.gap_tr.mean(), intra=1e4*g.intra.mean()))
H = pd.DataFrame(rows); H.to_csv(R + "/a1_years_stocks.csv", index=False)
H2 = H[H.n >= 100]
print("\n47 hisse yıl bazında medyan (n>=100 gün):")
print(H2.groupby("year")[["gap", "gap_tr", "intra"]].median().round(1).T.to_string())
print("intra<0 olan hisse oranı:", H2.assign(neg=H2.intra < 0).groupby("year")["neg"].mean().round(2).to_dict())
print("gap>0 olan hisse oranı:", H2.assign(p=H2.gap > 0).groupby("year")["p"].mean().round(2).to_dict())
# hisse bazında tam dönem
rows = []
for s, x in P.items():
    for nm, sl in [("full", slice("2014", "2026")), ("IS", slice("2014", "2020")), ("OOS", slice("2021", "2026"))]:
        z = x.loc[sl]
        rows.append(dict(stock=s, per=nm, n=z.intra.notna().sum(), gap=1e4*z.gap.mean(), gap_tr=1e4*z.gap_tr.mean(), intra=1e4*z.intra.mean(), t_intra=tstat(z.intra)))
Q = pd.DataFrame(rows); Q.to_csv(R + "/a1_stocks_full.csv", index=False)
for nm, g in Q.groupby("per"):
    print(nm, "gap>0:", (g.gap > 0).sum(), "intra<0:", (g.intra < 0).sum(), "intra t<-2:", (g.t_intra < -2).sum(), "/", len(g),
          " medyan gap", round(g.gap.median(), 1), "medyan intra", round(g.intra.median(), 1))
# eşit ağırlıklı sepet: 47 hissede her gün aç-sat
ew = pd.DataFrame({s: -x["intra"] for s, x in P.items()}).mean(axis=1)
for nm, sl in [("full", slice("2014", "2026")), ("IS", slice("2014", "2020")), ("OOS", slice("2021", "2026")), ("2024-26", slice("2024", "2026"))]:
    s = ew.loc[sl].dropna(); print("EW sepet aç-sat", nm, "n", len(s), "brüt", round(1e4*s.mean(), 1), "t", round(tstat(s), 2), "NW t", round(nw_t(s), 2))
pd.to_pickle(P, R + "/a1_P.pkl")
