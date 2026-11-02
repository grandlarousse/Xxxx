"""s5: 47 hisse — ortak faktör (piyasa artığı), etkin bağımsız test sayısı, SSF ACILIS bayatlığı, SSF küçük-gap testi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc, statsmodels.api as sm
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
m = bc.decomp("XU030.IS", start="2014-01-01")
G, I = {}, {}
for s in bc.STOCKS:
    d = bc.decomp(s + ".IS", start="2014-01-01")
    G[s] = d.gap_tr; I[s] = d.intra
G = pd.DataFrame(G); I = pd.DataFrame(I)
rows = []
for s in bc.STOCKS:
    x = pd.concat([I[s], m.intra], axis=1, keys=["i", "m"]).dropna()
    for nm, a, b in [("2014-2026", "2014", "2026"), ("2014-2020", "2014", "2020"), ("2021-2026", "2021", "2026")]:
        xx = x.loc[a:b]
        if len(xx) < 200: continue
        beta = np.cov(xx.i, xx.m)[0, 1] / xx.m.var()
        e = xx.i - beta * xx.m
        r = dict(stock=s, per=nm, n=len(xx), intra=xx.i.mean() * 1e4, t_intra=bc.st(xx.i)["t"], beta=beta, resid=e.mean() * 1e4, t_resid=bc.st(e)["t"])
        rows.append(r)
R = pd.DataFrame(rows); R.to_csv(f"{bc.RES}/s5_resid.csv", index=False)
for nm, g in R.groupby("per"):
    P(f"{nm}: hisse {len(g)} | ham gün-içi<0 {int((g.intra<0).sum())}, t<-2 {int((g.t_intra<-2).sum())}, medyan {g.intra.median():.1f} | "
      f"PİYASA ARTIĞI (intra - β·XU030 intra) <0 {int((g.resid<0).sum())}, t<-2 {int((g.t_resid<-2).sum())}, t>+2 {int((g.t_resid>2).sum())}, medyan {g.resid.median():.1f} bps, medyan β {g.beta.median():.2f}")
# etkin bağımsız test sayısı
C = I.loc["2014":].corr().values; n = C.shape[0]
rho = (C.sum() - n) / (n * (n - 1))
P(f"47 hisse gün-içi ortalama ikili korelasyon {rho:.2f} -> etkin bağımsız sayı N/(1+(N-1)ρ) = {n/(1+(n-1)*rho):.1f}")
ew = I.loc["2014":].mean(axis=1)
P(f"EW47 aç-sat 2014-2026 {bc.fmt(bc.st(-ew))}; 2021-2026 {bc.fmt(bc.st(-ew.loc['2021':]))}")
ewr = (I.loc["2014":].sub(m.intra.reindex(I.loc['2014':].index), axis=0)).mean(axis=1)
P(f"EW47 - XU030 gün-içi farkı (eşit ağırlık küçük hisse eğilimi): {bc.fmt(bc.st(ewr))}")

# SSF: bayat ACILIS testi, hisse bazında
V = bc.viop_parse()
ss = []
for s in bc.STOCKS:
    und = f"{s}.E"
    if (V.und == und).sum() < 100: continue
    f = bc.fut_series(V, und, "next")
    f = f[(f.f_intra.abs() < bc.LIM) & (f.f_gapc.abs() < bc.LIM) & (f.ntr >= 20)]
    j = f.join(pd.DataFrame({"g": G[s], "i": I[s]}), how="inner").dropna(subset=["g", "i", "f_gapc", "f_intra"])
    for nm, a, b in [("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026")]:
        jj = j.loc[a:b]
        if len(jj) < 100: continue
        sl = sm.OLS(jj.f_gapc.values, sm.add_constant(jj.g.values)).fit().params[1]
        small = jj[jj.g.abs() < 0.0025]
        ext = ((jj.open <= jj.low) | (jj.open >= jj.high))[jj.g.abs() > 0.02].mean()
        ss.append(dict(stock=s, per=nm, n=len(jj), slope=sl, f_aqs=-jj.f_intra.mean() * 1e4, s_aqs=-jj.i.mean() * 1e4,
                       n_small=len(small), f_small=-small.f_intra.mean() * 1e4, s_small=-small.i.mean() * 1e4, ext_big=ext,
                       ntr=jj.ntr.median()))
SS = pd.DataFrame(ss); SS.to_csv(f"{bc.RES}/s5_ssf.csv", index=False)
for nm, g in SS.groupby("per"):
    P(f"SSF {nm}: hisse {len(g)} | medyan eğim f_gapc~s_gap {g.slope.median():.2f} | ACILIS gün dibi/tepesi (|gap|>2%) medyan {g.ext_big.median():.2f} | "
      f"aç-sat medyan vadeli {g.f_aqs.median():.1f} / spot {g.s_aqs.median():.1f} | KÜÇÜK GAP (|g|<0,25%) medyan vadeli {g.f_small.median():.1f} / spot {g.s_small.median():.1f} | medyan işlem sayısı {g.ntr.median():.0f}")
open(f"{bc.RES}/s5_stocks.log", "w").write("\n".join(L))
