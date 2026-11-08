"""Hakem: strateji düzeyi — maliyet taraması, alt dönemler, dairesel kaydırma null'u, parametre duyarlılığı, giriş zamanlaması, uç dönem hariç."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag")
from e2_common import *
import e2_common
ADV = f"{S}/out/e2_etf_leadlag_adv"
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); SIGA = pd.read_pickle(f"{OUT}/s7_signals.pkl"); FEAT3 = pd.read_pickle(f"{OUT}/s3_signals.pkl")
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1))
C = {"C2j": (SIG1[("GDXJ~GLD+SPY", 1)], +1, "GDXJ", 3, 0.7), "C2": (SIG1[("GDX~GLD+SPY", 3)], +1, "GDX", 3, 0.7),
     "C1": (SIG1[("GDX~GLD+SPY", 10)], +1, "GLD", 5, 0.8), "C5": (SIGA[1], +1, "GLD", 3, 0.7),
     "C4": (FEAT3[("PLATIN", "d5")], -1, "GDX", 3, 0.8), "C3": (gi, -1, "GDX", 1, 0.7)}
P4 = [("2008-01-01", "2012-12-31"), ("2013-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31"), ("2022-01-01", "2026-12-31")]
def lo_bt(pos, r, h, c, dm=False):
    return backtest(pos.clip(lower=0), r, h, c, demean=dm)
print("=== 1) maliyet taramasi (OOS 2018+, yalniz uzun / ideal) ===")
for cn, (x, sg, T, h, q) in C.items():
    pos = pos_from_signal(x, sg, q); r = R[T][R[T].index >= "2018-01-01"].dropna()
    s = []
    for c in (0, 10, 20, 30, 40, 60):
        a = lo_bt(pos, r, h, c); b = backtest(pos, r, h, c)
        s.append(f"{c}bp L{a['sharpe']:.2f}/I{b['sharpe']:.2f}")
    a0 = lo_bt(pos, r, h, 0); turn = a0["turnover_per_yr"]
    be = a0["ann_ret"] / (turn / 2 / 1e4) if turn > 0 else np.nan   # ann_ret = turn*c/2/1e4 -> c
    bh = backtest(pd.Series(1.0, index=r.index), r, 1, 0)
    # maliyet sonrası B&H'yi geçme eşiği: (ann_long - c*turn/2e4)/vol_long = SR_bh
    sr_bh = bh["sharpe"]; c_be_bh = (a0["ann_ret"] - sr_bh * a0["ann_vol"]) / (turn / 2 / 1e4)
    print(f"{cn}: {' | '.join(s)} | turnover/yr {turn:.1f} | breakeven c(sifir getiri) {be:.0f}bp | B&H Sharpe'ini gecme esigi {c_be_bh:.0f}bp | B&H {sr_bh:.2f}")

print("\n=== 2) alt donemler: yalniz uzun / long_dm / ideal / B&H (10bp) ===")
for cn, (x, sg, T, h, q) in C.items():
    pos = pos_from_signal(x, sg, q); s = []
    for a_, b_ in P4:
        r = R[T][(R[T].index >= a_) & (R[T].index <= b_)].dropna()
        if len(r) < 100: s.append(f"{a_[:4]}: -"); continue
        L = lo_bt(pos, r, h, 10); Ld = lo_bt(pos, r, h, 10, True); I = backtest(pos, r, h, 10); B = backtest(pd.Series(1.0, index=r.index), r, 1, 0)
        s.append(f"{a_[:4]}-{b_[2:4]}: L{L['sharpe']:+.2f} Ldm{Ld['sharpe']:+.2f} I{I['sharpe']:+.2f} BH{B['sharpe']:+.2f}")
    print(cn, " | ".join(s))

print("\n=== 3) dairesel kaydirma null'u (OOS 2018+, 10bp): sinyali 120..len-120 gün kaydir, pozisyon yeniden ===")
rng = np.random.default_rng(7)
for cn, (x, sg, T, h, q) in C.items():
    r = R[T][R[T].index >= "2018-01-01"].dropna()
    pos = pos_from_signal(x, sg, q).reindex(r.index).fillna(0)
    act_L = lo_bt(pos, r, h, 10)["sharpe"]; act_Ld = lo_bt(pos, r, h, 10, True)["sharpe"]; act_I = backtest(pos, r, h, 10)["sharpe"]
    n = len(pos); nullL = []; nullLd = []; nullI = []
    for sh in rng.integers(120, n - 120, 400):
        pp = pd.Series(np.roll(pos.values, sh), index=pos.index)
        nullL.append(lo_bt(pp, r, h, 10)["sharpe"]); nullLd.append(lo_bt(pp, r, h, 10, True)["sharpe"]); nullI.append(backtest(pp, r, h, 10)["sharpe"])
    nullL = np.array(nullL); nullLd = np.array(nullLd); nullI = np.array(nullI)
    print(f"{cn}: L {act_L:.2f} (null med {np.median(nullL):.2f}, 95% {np.quantile(nullL,.95):.2f}, p={np.mean(nullL>=act_L):.3f}) | Ldm {act_Ld:.2f} (null 95% {np.quantile(nullLd,.95):.2f}, p={np.mean(nullLd>=act_Ld):.3f}) | I {act_I:.2f} (null 95% {np.quantile(nullI,.95):.2f}, p={np.mean(nullI>=act_I):.3f})")

print("\n=== 4) uc donem haric / winsor (OOS 2018+, 10bp) ===")
for cn, (x, sg, T, h, q) in C.items():
    pos = pos_from_signal(x, sg, q); r = R[T][R[T].index >= "2018-01-01"].dropna()
    ex = ~(((r.index >= "2020-02-20") & (r.index <= "2020-04-30")) | ((r.index >= "2026-01-01") & (r.index <= "2026-02-28")))
    rw = r.clip(r.quantile(0.01), r.quantile(0.99))
    a = lo_bt(pos, r, h, 10); b = lo_bt(pos, r[ex], h, 10); c = lo_bt(pos, rw, h, 10); c2 = lo_bt(pos, rw, h, 10, True)
    bb = backtest(pd.Series(1.0, index=r[ex].index), r[ex], 1, 0)
    # en iyi 10 gün çıkarılınca
    pn = a["pnl"]; top = pn.nlargest(10).index; pn2 = pn.drop(top)
    print(f"{cn}: L {a['sharpe']:.2f} | uc-haric L {b['sharpe']:.2f} (BH {bb['sharpe']:.2f}) | winsor1% L {c['sharpe']:.2f} Ldm {c2['sharpe']:.2f} | en iyi 10 gun cikinca L {pn2.mean()/pn2.std()*np.sqrt(252):.2f}")
