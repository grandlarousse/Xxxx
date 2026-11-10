"""r3b: ana ajanin bildirdigi rakamlara (84 islem, +0,91, Sharpe 0,90, alfa 5,0 t 2,26; h3 +0,26/+0,10; h5 +0,48/+0,14) hangi esik uyuyor?"""
import json
from rep_lib import *
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet"); r = D.ret; bh = np.exp(r) - 1
print("esik%  n_sin | h3_sin h3_tum t3 | h5_sin h5_tum t5 | t5(18-26) || H3: islem ort% kazanan enkotu Sharpe alfa t | 22bps Sharpe t || H5: islem ort% kaz Sharpe alfa t")
for th in [2.20, 2.25, 2.307, 2.35, 2.40, 2.437, 2.45, 2.50, 2.541, 2.60, 2.70, 2.80, 3.0]:
    sig = (D.x > th / 100).astype(float)
    e3 = event_stats(r, sig, 3); e5 = event_stats(r, sig, 5); e5o = event_stats(r, sig, 5, "2018-01-01", None)
    T, net, pos = run_trades(r, sig, 3, 5); Tc = T[T.closed]; al = alpha_vs_bh(net, bh)
    T2, net2, _ = run_trades(r, sig, 3, 22); al2 = alpha_vs_bh(net2, bh)
    T5, net5, _ = run_trades(r, sig, 5, 5); T5c = T5[T5.closed]; al5 = alpha_vs_bh(net5, bh)
    print(f"{th:5.3f} {int(sig.sum()):4d} | {e3['mean_sig']:.3f} {e3['mean_all']:.3f} {e3['t_nw']:.2f} | {e5['mean_sig']:.3f} {e5['mean_all']:.3f} {e5['t_nw']:.2f} | {e5o['t_nw']:.2f} || "
          f"{len(Tc)} {Tc.net.mean()*100:.2f} g{Tc.gross.mean()*100:.2f} {(Tc.net>0).mean()*100:.0f} {Tc.net.min()*100:.1f} {sharpe(net):.2f} {al['alpha_ann']:.1f} {al['t']:.2f} | {sharpe(net2):.2f} {al2['t']:.2f} || "
          f"{len(T5c)} {T5c.net.mean()*100:.2f} g{T5c.gross.mean()*100:.2f} {(T5c.gross>0).mean()*100:.0f} {sharpe(net5):.2f} {al5['alpha_ann']:.1f} {al5['t']:.2f}")
# basit getiri ile olay ortalamasi (log yerine)
sig = (D.x > 0.02307).astype(float)
for h in (3, 5):
    f = np.exp(fwd_sum(r, h)) - 1
    print(f"basit getiri h{h}: sinyal {f[sig>0].mean()*100:.3f} tum {f.mean()*100:.3f} | 2026-11 haric log: sinyal {fwd_sum(r,h)[sig>0][:'2026-10-31'].mean()*100:.3f}")
