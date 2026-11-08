"""6) Ek kontroller: C3 GDX sinyal günlerinde GDXJ/NUGT getirisi; sepetin altın ve EEM'e göre artığı; örnek öncesi SPY kontrollü sepet; tatil türü 2008 hariç."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
pd.set_option("display.width", 250)
R = {t: logret(t) for t in ["GDX", "GDXJ", "GLD", "SPY", "EEM", "NUGT", "COPX", "SIL", "RING"]}
def streak(r):
    s = np.sign(r).fillna(0).values; o = np.zeros(len(s))
    for i in range(len(s)):
        if s[i] == 0: o[i] = 0
        elif i > 0 and np.sign(o[i - 1]) == s[i]: o[i] = o[i - 1] + s[i]
        else: o[i] = s[i]
    return pd.Series(o, index=r.index)
k = streak(R["GDX"]); pos = (k.shift(1) <= -5).astype(float)
print("C3: GDX>=5 düşüş sinyal günlerinde (t kapanışı -> t+1) diğer ETF'ler:")
for t in ["GDX", "GDXJ", "NUGT", "GLD", "SPY", "RING", "SIL"]:
    y = R[t].shift(-1); q = pd.concat([y.rename("y"), pos.rename("x")], axis=1).dropna()
    b, tv = nw_ols(q.y.values, q.x.values, 5)
    print(f"  {t}: n_sig={int(q.x.sum())} ort={q.y[q.x==1].mean()*1e4:.1f} bps t={tv[1]:.2f}")
# GDXJ kendi serisi ile GDX serisi sinyal örtüşmesi
kj = streak(R["GDXJ"]); pj = (kj.shift(1) <= -5).astype(float)
both = pd.concat([pos, pj], axis=1).dropna(); print("  GDX ve GDXJ sinyal günü örtüşmesi:", int((both.iloc[:, 0] * both.iloc[:, 1]).sum()), "/", int(both.iloc[:, 0].sum()), int(both.iloc[:, 1].sum()))
# GDX sinyal yıl dağılımı ve en büyük katkılar
y = R["GDX"].shift(-1); ev = y[pos == 1].dropna()
print("  GDX sinyal getirisi yıl dağılımı (n, toplam %):", ev.groupby(ev.index.year).agg(['count', 'sum']).assign(sum=lambda d: (d['sum'] * 100).round(1)).T.to_dict())
print("  en büyük 5 katkı:", (ev.sort_values(ascending=False).head(5) * 100).round(2).to_dict())
print("  en büyük 5 hariç ortalama bps:", round(ev.sort_values(ascending=False).iloc[5:].mean() * 1e4, 1), " medyan bps:", round(ev.median() * 1e4, 1), " isabet:", round((ev > 0).mean(), 3))

# Sepet: GDXJ artığı (aynı gün GLD, SPY, EEM kontrolü)
ix = pd.Series(SESS, index=SESS); ym = ix.dt.to_period("M"); FIRST = ym != ym.shift(1)
H = regular_holidays(); nxt = ix.shift(-1)
PRE = pd.Series([((H.index > d) & (H.index < n)).any() if pd.notna(n) else False for d, n in zip(SESS, nxt)], index=SESS)
BAS = (FIRST | PRE).astype(float)
print("\nSepet dummy, aynı gün kontrollerle (NW5):")
for t in ["GDXJ", "GDX"]:
    for ctrl in [[], ["SPY"], ["GLD"], ["SPY", "GLD"], ["SPY", "GLD", "EEM"]]:
        d = pd.concat([R[t].rename("y")] + [R[c].rename(c) for c in ctrl] + [BAS.rename("b")], axis=1).dropna()
        for lab, dd in [("tam", d), ("OOS", d[d.index >= OOS_START])]:
            b, tv = nw_ols(dd.y.values, dd[ctrl + ["b"]].values, 5)
            print(f"  {t} ctrl={ctrl} {lab}: sepet {b[-1]*1e4:.1f} bps t={tv[-1]:.2f}")
print("\nSepet günlerinde diğer varlıklar (ortalama bps, t):")
for t in ["GLD", "SPY", "EEM", "COPX"]:
    d = pd.concat([R[t].rename("y"), BAS.rename("b")], axis=1).dropna(); b, tv = nw_ols(d.y.values, d.b.values, 5)
    print(f"  {t}: olay {d.y[d.b==1].mean()*1e4:.1f} diğer {d.y[d.b==0].mean()*1e4:.1f} t={tv[1]:.2f}")

# tatil türü, 2008 hariç (analistin isim tablosu 2009+)
PN = pd.Series("", index=SESS)
for d, n in zip(SESS, nxt):
    if pd.notna(n):
        hh = H.index[(H.index > d) & (H.index < n)]
        if len(hh): PN[d] = H.loc[hh[0], "name"]
tt = pd.DataFrame({"tatil": PN[PRE], "GDX": R["GDX"][PRE] * 1e4, "GDXJ": R["GDXJ"][PRE] * 1e4})
tt = tt[tt.index.year >= 2009]
print("\nTatil türü 2009+:"); print(tt.groupby("tatil").mean().round(1).sort_values("GDX", ascending=False).to_string())
