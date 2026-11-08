import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); SIGA = pd.read_pickle(f"{OUT}/s7_signals.pkl")
# 1) en iyi 10 gün çıkarma: strateji vs B&H vs maruziyet-eşleşmeli null
x = SIG1[("GDXJ~GLD+SPY", 1)]; r = R["GDXJ"][R["GDXJ"].index >= "2018-01-01"].dropna()
pos = pos_from_signal(x, 1, 0.7).clip(lower=0)
a = backtest(pos, r, 3, 10)["pnl"]; b = r.copy()
def drop_top(p, k=10): q = p.drop(p.nlargest(k).index); return q.mean() / q.std() * np.sqrt(252)
print("[top10] C2j L", round(drop_top(a), 2), "B&H", round(drop_top(b), 2), "| top20:", round(drop_top(a, 20), 2), round(drop_top(b, 20), 2))
# 2) hafta günü
y = fwd(R["GDXJ"], 3); z = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
print("[hafta gunu IC]", z.groupby(z.index.dayofweek).apply(lambda g: (round(g.x.corr(g.y, method='spearman'), 3), len(g))).to_dict())
# 3) C1 kaplama 2018-2024 ve yıllık fark
x1 = SIG1[("GDX~GLD+SPY", 10)]; p = pos_from_signal(x1, 1, 0.8); ov = pd.Series(1.0, index=p.index); ov[p < 0] = 0.0
for a_, b_ in [("2018-01-01", "2024-12-31"), ("2025-01-01", "2026-12-31")]:
    rr = R["GLD"][(R["GLD"].index >= a_) & (R["GLD"].index <= b_)].dropna()
    o = backtest(ov.reindex(rr.index).fillna(1), rr, 5, 10); bh = backtest(pd.Series(1.0, index=rr.index), rr, 1, 0)
    print(f"[C1 kaplama] {a_[:4]}-{b_[:4]}: {o['sharpe']:.2f} vs B&H {bh['sharpe']:.2f}")
o = backtest(ov.reindex(R["GLD"].dropna().index).fillna(1), R["GLD"].dropna(), 5, 10)["pnl"]; bb = R["GLD"].dropna()
print("[C1 kaplama yillik fark %]", ((o.groupby(o.index.year).sum() - bb.groupby(bb.index.year).sum()) * 100).round(1).to_dict())
# 4) C2j: IS'te tüm ızgara (k1,2,3,5 x h1-5 x q) IS-en iyi seçilseydi OOS ne olurdu
X2 = pd.concat([R["GLD"], R["SPY"]], axis=1); X2.columns = ["GLD", "SPY"]
for und in ["GDXJ", "GDX"]:
    e = SIG1[(f"{und}~GLD+SPY", 1)].shift(-1)  # e_t
    rI = R[und][R[und].index <= "2017-12-31"].dropna(); rO = R[und][R[und].index >= "2018-01-01"].dropna()
    best = None; res = []
    for k in (1, 2, 3, 5, 10):
        xx = e.rolling(k, min_periods=k).sum().shift(1)
        for h in (1, 2, 3, 4, 5):
            for q in (0.6, 0.7, 0.8, 0.9):
                ps = pos_from_signal(xx, 1, q); si = backtest(ps, rI, h, 10)["sharpe"]
                so = backtest(ps.clip(lower=0), rO, h, 10)["sharpe"]; sod = backtest(ps.clip(lower=0), rO, h, 10, demean=True)["sharpe"]; soi = backtest(ps, rO, h, 10)["sharpe"]
                res.append((si, k, h, q, so, sod, soi))
    res = pd.DataFrame(res, columns=["is", "k", "h", "q", "oos_L", "oos_Ldm", "oos_I"]).sort_values("is", ascending=False)
    print(f"[genis izgara {und}] IS-en iyi 5:\n", res.head(5).round(2).to_string(index=False))
    print(f"   tüm {len(res)} konf. OOS L medyan {res.oos_L.median():.2f}, Ldm medyan {res.oos_Ldm.median():.2f}, I medyan {res.oos_I.median():.2f}; IS-üst %20 OOS L medyan {res.head(len(res)//5).oos_L.median():.2f}")
# 5) C3 alt dönem IC
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1)); yy = fwd(R["GDX"], 1)
print("[C3 alt donem]", {f"{a_[:4]}": (round(sub_ic(-gi, yy, 1, a_, b_)['ic'], 3), round(sub_ic(-gi, yy, 1, a_, b_)['t'], 2)) for a_, b_ in [("2008-01-01", "2012-12-31"), ("2013-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]})
# 6) C5 alt dönem IC
y5 = fwd(R["GLD"], 3)
print("[C5 alt donem]", {f"{a_[:4]}": (round(sub_ic(SIGA[1], y5, 3, a_, b_)['ic'], 3), round(sub_ic(SIGA[1], y5, 3, a_, b_)['t'], 2)) for a_, b_ in [("2008-01-01", "2012-12-31"), ("2013-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]})
# 7) C4 2011 sonrası (PL=F veri hataları 2008-10 dışlanınca)
pl = np.log(d["y_PL_F"].astype(float)).diff(5); yg = fwd(R["GDX"], 3)
m = pl.index >= "2011-01-01"; st = split_stats(pl[m], yg[m], 3); print(f"[C4 2011+] ic {st['ic']:+.3f} t {st['t']:+.2f} is(2011-17) {st['t_is']:+.2f} oos {st['t_oos']:+.2f}")
