"""r3c: ana ajanin bildirdigi H=3 rakamlarina uyan varyant arayisi (sabit cikarilmis artik, ince esik taramasi)."""
from rep_lib import *
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet"); r = D.ret; bh = np.exp(r) - 1
def line(lab, x, th):
    sig = (x > th).astype(float)
    e3 = event_stats(r, sig, 3); e5 = event_stats(r, sig, 5)
    T, net, pos = run_trades(r, sig, 3, 5); Tc = T[T.closed]; al = alpha_vs_bh(net, bh)
    T2, net2, _ = run_trades(r, sig, 3, 22); al2 = alpha_vs_bh(net2, bh)
    print(f"{lab:28s} th {th*100:.3f} n {int(sig.sum()):4d} | h3 {e3['mean_sig']:.3f}/{e3['mean_all']:.3f} t {e3['t_nw']:.2f} | h5 {e5['mean_sig']:.3f}/{e5['mean_all']:.3f} t {e5['t_nw']:.2f} || {len(Tc)}(+{int((~T.closed).sum())}) net {Tc.net.mean()*100:.2f} brut {Tc.gross.mean()*100:.2f} kaz {(Tc.gross>0).mean()*100:.0f} enkotu {Tc.gross.min()*100:.1f} Sh {sharpe(net):.2f} alfa {al['alpha_ann']:.1f} t {al['t']:.2f} | 22: Sh {sharpe(net2):.2f} t {al2['t']:.2f}")
for th in np.arange(2.30, 2.96, 0.05):
    line("temel", D.x, th / 100)
R = us_returns("adjclose")
e, _ = rolling_resid(R, 250, 250, sub_const=True); X = e.rolling(10, min_periods=10).sum(); x, _ = map_last_us_before(D.index, X)
for lab, th in [("sabit cikarilmis 2008-17", float(X["2008-01-01":"2017-12-31"].quantile(.8))), ("sabit cikarilmis <=2017", float(X[:"2017-12-31"].dropna().quantile(.8)))]:
    line(lab, x, th)
# H=3 islem sayisi: acik islem dahil / haric ve sure sinirlamasi
