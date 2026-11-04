import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lb, common as C
V = pd.read_pickle('V_sa.pkl')
a, b = pd.Timestamp('2021-01-01'), pd.Timestamp('2026-12-31')
rng = np.random.default_rng(20261103)
res = {}
for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    T, d = C.run(V, exit_=ex); T = T[~T.bad & (T.d0 >= a)]
    act = T.net.mean(); H = T.hold.values; nshort = (T.sgn < 0).mean(); n = len(T)
    idx = V.index; ok = np.where((idx >= a) & (idx < idx[-1] - pd.Timedelta(days=1)))[0]
    FA0, dFA, FB0, dFB, rA, rB, be = V.F0A.values, V.dFA.values, V.F0B.values, V.dFB.values, V.rollA.values, V.rollB.values, V.beta.values
    means = []
    for it in range(2000):
        i0 = rng.choice(ok, n); h = rng.choice(H, n); s = np.where(rng.random(n) < nshort, -1, 1)
        tr = [(int(x), int(min(x + y, len(idx) - 1)), int(z)) for x, y, z in zip(i0, h, s)]
        Tp, _ = lb.eval_trades(tr, idx, FA0, dFA, FB0, dFB, rA, rB, be)
        means.append(Tp.net.mean())
    means = np.array(means)
    # zaman kaydirma plasebosu
    sh = []
    for k in list(range(-750, -19, 10)) + list(range(20, 751, 10)):
        X = V.copy(); X['z'] = V.z.shift(k)
        Tk, dk = C.run(X, exit_=ex); Tk = Tk[~Tk.bad & (Tk.d0 >= a)]
        sh.append(Tk.net.mean())
    sh = np.array(sh)
    print(f'== {nm}: gercek ort net {act:.1f} (n={n})')
    print(f'   rastgele giris (2000): ort {means.mean():.1f}, sd {means.std():.1f}, %95 {np.percentile(means,95):.1f}, %99 {np.percentile(means,99):.1f}, p(>=gercek)={np.mean(means>=act):.4f}')
    print(f'   z zaman kaydirma ({len(sh)} kaydirma): ort {sh.mean():.1f}, sd {sh.std():.1f}, maks {sh.max():.1f}, p(>=gercek)={np.mean(sh>=act):.3f}')
    res[nm] = (act, means, sh)
# ---- maliyet
print('== (8) maliyet (VIOP 2021-26), bacak basina gidis-donus bps')
L = pd.read_csv(lb.S + '/out/y_viop_likidite.csv').set_index('und')
for col in ['rt_cost_floor_bps', 'rt_cost_small_bps', 'rt_cost_cons_bps', 'rt_cost_1m_bps', 'rt_cost_retail_bps']:
    print(f'   {col}: SAHOL {L.at["SAHOL", col]:.1f} AKBNK {L.at["AKBNK", col]:.1f}')
cases = [('8+tik (kaynak)', 8, 8, True), ('kucuk emir', L.at['SAHOL', 'rt_cost_small_bps'], L.at['AKBNK', 'rt_cost_small_bps'], False),
         ('muhafazakar', L.at['SAHOL', 'rt_cost_cons_bps'], L.at['AKBNK', 'rt_cost_cons_bps'], False),
         ('1 mn TL', L.at['SAHOL', 'rt_cost_1m_bps'], L.at['AKBNK', 'rt_cost_1m_bps'], False),
         ('15+tik', 15, 15, True),
         ('bireysel onbinde10+BSMV', L.at['SAHOL', 'rt_cost_retail_bps'], L.at['AKBNK', 'rt_cost_retail_bps'], False), ('30+tik', 30, 30, True)]
for nm, ex in [('A', 1.5), ('C', 1.0), ('B', 0.5)]:
    for lab, ca, cb, tk in cases:
        T, d = C.run(V, exit_=ex, cA=ca, cB=cb, tick=tk); T = T[~T.bad]
        print(f'   {nm} {lab:24s}', C.line(T, d, '2021-01-01', '2026-12-31'))
    T, d = C.run(V, exit_=ex, cA=0, cB=0, tick=False); T = T[~T.bad & (T.d0 >= a)]
    g = T.gross.mean(); k = (1 + T.beta.mean()) * (1 + T.nroll.mean())
    print(f'   {nm} brut {g:.1f} bps; basabas bacak basi RT maliyet ~ {g / k:.1f} bps')
print('== tam sayi kontrat (kucuk emir maliyeti), VIOP 2021-26')
ca, cb = L.at['SAHOL', 'rt_cost_small_bps'], L.at['AKBNK', 'rt_cost_small_bps']
for nm, ex in [('A', 1.5), ('B', 0.5)]:
    for nS in [1, 2, 3, 5, 13, 39]:
        T, d = C.run(V, exit_=ex, cA=ca, cB=cb, tick=False, ratio='int', nS=nS); T = T[~T.bad]
        TT = T[T.d0 >= a]
        print(f'   {nm} N_SAHOL={nS:2d}: ort w={TT.w.mean():.2f} (sd {TT.w.std():.2f})', C.line(T, d, '2021-01-01', '2026-12-31'))
    T, d = C.run(V, exit_=ex, cA=ca, cB=cb, tick=False, ratio='eq'); T = T[~T.bad]
    print(f'   {nm} esit TL           ', C.line(T, d, '2021-01-01', '2026-12-31'))
