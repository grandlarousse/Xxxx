"""Gün gün ayrıştırma, close0 girişli plasebo, vadeli açılış girişi (akşam seansı öncesi)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_V1_a')
from v1 import *
rat = EV[EV.kind == 'rating'].copy()
xu = DLY['XU100.IS']; o, c = xu['o'].values, xu['c'].values
print('=== gün gün işaretli getiri (XU100, brüt bps): k=0 gün-içi (açılış->kapanış), k>=1 kapanış->kapanış (gap+gün-içi) ===')
rows = []
for _, e in rat.iterrows():
    i = int(e.react_i); s = -e.dir
    r = {'react': e.react.date(), 'gap0_notrade': s * np.log(o[i] / c[i - 1]), 'k0_intra': s * np.log(c[i] / o[i])}
    for k in range(1, 6):
        r[f'k{k}_gap'] = s * np.log(o[i + k] / c[i + k - 1]); r[f'k{k}_intra'] = s * np.log(c[i + k] / o[i + k])
        r[f'k{k}'] = s * np.log(c[i + k] / c[i + k - 1])
    rows.append(r)
T = pd.DataFrame(rows).set_index('react')
for col in ['gap0_notrade', 'k0_intra', 'k1', 'k1_gap', 'k1_intra', 'k2', 'k2_gap', 'k2_intra', 'k3', 'k4', 'k5']:
    t, n = tstat(T[col]); print(f'{col:13s} ort {1e4*T[col].mean():7.1f}  med {1e4*T[col].median():7.1f}  t {t:5.2f}  isabet {(T[col]>0).mean():.2f}')
print((1e4 * T[['gap0_notrade', 'k0_intra', 'k1', 'k2', 'k3']]).round(0).to_string())
# her gün için plasebo: tüm günler ortalaması (yön etiketi işaretiyle) -> karşılaştırma
print('\n=== close0 girişli (açılış fiyatına bağımsız) plasebo, ±3..52 hafta ===')
for sym in ['XU100.IS', 'XBANK.IS']:
    act = np.mean([-e.dir * trade(sym, int(e.react_i), 'close0', 2) for _, e in rat.iterrows()])
    pl = []
    for w in list(range(-52, -2)) + list(range(3, 53)):
        v = []
        for _, e in rat.iterrows():
            p = CAL.searchsorted(e.react + pd.Timedelta(weeks=w))
            if 6 <= p < len(CAL) - 2: v.append(-e.dir * trade(sym, p, 'close0', 2))
        pl.append(np.mean(v))
    pl = np.array(pl); print(f'{sym}: gerçek {1e4*act:.0f} brüt | plasebo ort {1e4*pl.mean():.0f} sd {1e4*pl.std():.0f} | p={np.mean(pl>=act):.3f}')
# vadeli açılış girişi (akşam seansı öncesi olaylar: react < 2024-12-01) - bülten açılış fiyatı 09:30 TSİ
F = pd.read_csv(OUT + '/res_viop_futures.csv', parse_dates=['react'])
X = F[(F.root == 'XU030') & (F.react < '2024-12-01')].copy()
X['fut_open_t2'] = -X['dir'] * np.log(X['s2'] / X['o0'])
print('\nF_XU030 açılış(09:30)->t+2 uzlaşma, 4 bps, akşam seansı öncesi olaylar:', summarize(X.fut_open_t2, 4))
print('F_XU030 t0 uzlaşma ->t+2 uzlaşma, aynı olaylar:', summarize(X.fut_settle_t0_t2, 4))
print('F_XU030 IS(<2021) / OOS:', summarize(F[(F.root=='XU030')&(F.react<'2021')].fut_settle_t0_t2, 4), summarize(F[(F.root=='XU030')&(F.react>='2021')].fut_settle_t0_t2, 4))
