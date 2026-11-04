"""17:55 / 17:40 fiyatıyla sinyal: bağımsız Monte Carlo (bag + d2_bt simülatörü; m5 verisi kurucunun indirdiği dosya)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/kod')
import bag, d2_bt as BT
M5 = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl_rehber_koza/m5/'
SIG, D = bag.signal(upto='2026-11-03')
def px_at(sym, start):
    m = pd.read_parquet(M5 + sym + '.IS.parquet'); t = m.index.tz_convert('Europe/Istanbul')
    k = t.strftime('%H:%M') == start; s = m.c[k]; s.index = pd.DatetimeIndex(t[k].date); return s
base, _ = BT.simulate(SIG); ob = BT.stats(base)
print(f"taban P0L: brüt {ob['gross']:+.1f} net15t {ob['net15t']:+.1f}")
rng = np.random.default_rng(11)
for lab, st in [('17:55 (5dk bar 17:50–17:55 kapanışı)', '17:50'), ('17:40 (TV 15 dk gecikmeli, 17:55 görünümü)', '17:35')]:
    P = pd.DataFrame({s: px_at(s, st) for s in ['TRMET', 'TRALT', 'TRENJ']}).dropna()
    P = P[P.index <= '2026-11-03']
    C = pd.DataFrame({s: D[s].c for s in ['TRMET', 'TRALT', 'TRENJ']}).reindex(P.index)
    eps = np.log(C / P)
    eu = eps.TRMET - SIG.b_g.reindex(P.index) * (eps.TRALT + eps.TRENJ) / 2
    q = (eu / SIG.sd60.reindex(P.index)).dropna()
    z2 = SIG.z3.copy(); z2.loc[q.index] = SIG.z3.loc[q.index] - q / np.sqrt(3)
    w = q.index; a0 = np.sign(SIG.z3.reindex(w)) * (SIG.z3.reindex(w).abs() > 1.5); a1 = np.sign(z2.reindex(w)) * (z2.reindex(w).abs() > 1.5)
    print(f"{lab}: pencere {w[0].date()}–{w[-1].date()} gün {len(w)}, sd(q) {q.std():.3f}, corr(z3) {np.corrcoef(SIG.z3.reindex(w), z2.reindex(w))[0,1]:.3f}, sinyal uyumu {(a0 == a1).mean():.3f}, kapanış sinyal {int((a0!=0).sum())} saat sinyal {int((a1!=0).sum())}")
    res = []
    for rep in range(150):
        s2 = SIG.copy(); s2['z3'] = SIG.z3 - rng.choice(q.values, len(SIG)) / np.sqrt(3)
        T, _ = BT.simulate(s2); o = BT.stats(T); res.append((o['n'], o['gross'], o['net15t'], o['t']))
    r = np.array(res)
    print(f"   MC 150: n {r[:,0].mean():.0f} brüt {r[:,1].mean():+.1f} (%5–95 {np.percentile(r[:,1],5):+.1f}…{np.percentile(r[:,1],95):+.1f}) net15t {r[:,2].mean():+.1f} t {r[:,3].mean():.2f} | fark {r[:,1].mean()-ob['gross']:+.1f} bps")
