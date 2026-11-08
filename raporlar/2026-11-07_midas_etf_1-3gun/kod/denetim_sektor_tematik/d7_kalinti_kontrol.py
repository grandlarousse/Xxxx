"""Denetim: ajanın reddettiği 'SPY'a göre aşırı satılan sektörü al' (beta60 kalıntı z1<-2, C0 h1) kuralının işareti.
11 SPDR havuzu; beta ve kalıntı oynaklığı yalnız t'ye kadar (t dahil) veriyle. python3 -I kod/denetim_sektor_tematik/d7_kalinti_kontrol.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *
SP = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
spy = np.log(D("SPY")["c"]).diff()
allt = []
for s in SP:
    df = D(s); r = np.log(df["c"]).diff(); m = spy.reindex(r.index)
    b = (r.rolling(60).cov(m) / m.rolling(60).var()).shift(1)        # beta t-1'e kadar
    e = r - b * m; z = e / e.rolling(60).std().shift(1)
    sig = (z < -2); sig.iloc[:200] = False
    tr = sim(df, sig, 1, "C0", cost(s)); tr["sym"] = s
    # SPY'a göre hedge'li brüt
    sc = D("SPY")["c"]; tr["spy"] = (sc.reindex(tr.exit_date).values / sc.reindex(tr.entry_date).values - 1)
    tr["b"] = b.reindex(tr.sig_date).values; tr["hedged"] = tr["gross"] - tr["b"] * tr["spy"]
    allt.append(tr)
A = pd.concat(allt)
wk = A.groupby(A.sig_date.dt.to_period("W-FRI"))[["net", "hedged"]].mean()
print(f"11 SPDR kalıntı z1<-2 -> al C0 h1: n={len(A)} net={A.net.mean()*1e4:.1f} bp, hedge'li brüt={A.hedged.mean()*1e4:.1f} bp; "
      f"hafta-ortalaması t: net {tt(wk.net.values):.2f}, hedge'li {tt(wk.hedged.values):.2f}")
