import sys
sys.argv=['x']
"""Adv3: C1/C2 aykırı değer ve dağılım sağlamlığı, GLD/SPY aynı gün kontrolü, uygulama zamanı (15:30 ET girişi, saatlik veri),
yıllık P&L, en iyi N olay çıkarılınca; C3 parametre komşuluğu; C4 Ocak (GC=F 2001-07, ay sıralaması); C5 Bollinger duyarlılığı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_adv")
from adv_common import *
from scipy import stats
pd.set_option("display.width", 250)
M = cal_masks(idx); first, pre = M["first"], M["pre"]; basket = first | pre
R = {t: np.log(d[f"c_{t}"]).diff() for t in ["GDX", "GDXJ", "GLD", "SPY", "NUGT", "JNUG", "SLV"]}

print("\n=== C4 Ocak: ay sıralaması GLD (2008-26) ve GC=F 2001-07 bağımsız ===")
for nm, r in [("GLD", np.log(yahoo("GLD").adjclose).diff()), ("GC=F", np.log(yahoo("GC_F").adjclose).diff())]:
    for a, b in [("2001-01-01", "2007-12-31"), ("2008-01-01", "2026-12-31")]:
        q = r.loc[a:b].dropna()
        if q.empty or (q.index.month == 1).sum() == 0: continue
        mm = q.groupby(q.index.month).mean() * 1e4
        tj = ev(pd.Series(q.index.month == 1, index=q.index), q)
        print(nm, a[:4], b[:4], "Ocak ort", round(mm[1], 1), "sıra", int(mm.rank(ascending=False)[1]), "/12", "t", tj["t"], "| ay ort bps:", mm.round(1).to_dict())
gc = np.log(yahoo("GC_F").adjclose).diff()
jy = gc[gc.index.month == 1].groupby(gc[gc.index.month == 1].index.year).sum() * 100
print("GC=F Ocak yıllık %:", jy.round(1).to_dict())

print("\n=== C5 Bollinger duyarlılığı GLD (z_{t-1}<thr, t kapanışında giriş, h gün) ===")
c = d.c_GLD; r = R["GLD"]
res = {}
for w in [10, 20, 50]:
    z = (c - c.rolling(w).mean()) / c.rolling(w).std()
    for thr in [-1.5, -2.0, -2.5]:
        sig = (z.shift(1) < thr).astype(float)
        for h in [1, 3, 5, 10]:
            y = sum(r.shift(-j) for j in range(1, h + 1))
            dd = pd.concat([y.rename("y"), sig.rename("x")], axis=1).dropna()
            _, tf, _ = nwt(dd.y, dd.x, max(h, 5)); _, ti, _ = nwt(dd.y[:IS_END], dd.x[:IS_END], max(h, 5)); _, to, _ = nwt(dd.y[IS_END:], dd.x[IS_END:], max(h, 5))
            res[(w, thr, h)] = f"{tf:.2f}/{ti:.2f}/{to:.2f}"
print(pd.Series(res).unstack(level=2).to_string())
# IAU ve GC=F 2005-07 aynı kural
for nm, cc in [("GC=F", yahoo("GC_F").adjclose), ("GLD_2005_07", yahoo("GLD").adjclose)]:
    rr = np.log(cc).diff(); z = (cc - cc.rolling(20).mean()) / cc.rolling(20).std()
    sig = (z.shift(1) < -2).astype(float); y = sum(rr.shift(-j) for j in range(1, 6))
    for a, b in [("2001-01-01", "2007-12-31"), ("2008-01-01", "2026-12-31")]:
        dd = pd.concat([y.rename("y"), sig.rename("x")], axis=1).dropna().loc[a:b]
        bb, tt, n = nwt(dd.y, dd.x, 5); print(nm, a[:4], b[:4], "BollZ<-2 h5: t", round(tt, 2), "olay", int(dd.x.sum()), "fark bps", round(bb * 1e4, 1))
