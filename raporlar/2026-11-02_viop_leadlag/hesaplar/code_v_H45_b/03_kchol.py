"""03: (a) KCHOL açılış NAV ayrışması — çürütme testleri.
A sinyal bileşenleri (NAV kısmı mı, kendi-gap kısmı mı?)
B sektör-eşleşmeli plasebo sepetler (Koç dışı, aynı sektör, aynı ağırlık)
C sektör/piyasa gap kontrolleri + gecikme kontrolleri + eşzamanlı piyasa gün-içi (ayrıştırma)
D iki taraflı yakınsama: sig -> NAV gün-içi
E uç değer / doğrusal olmama / küçük-gap günleri / alt dönem
F VİOP KCHOL vadelisi: VWAP girişli (gerçekçi, yavaş giriş) hedef ln(uzlaşma/VWAP), 2017+
G h1 (2023-11+) ve m5 (son 60 gün) giriş zamanı
"""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *
import importlib.util
spec = importlib.util.spec_from_file_location('r01', OUT + '/01_repro.py'); r01 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r01)
spec = importlib.util.spec_from_file_location('f02', OUT + '/02_futaudit.py'); f02 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f02)
W, basket_gap = r01.W, r01.basket_gap
rng = np.random.default_rng(45)

K = bist('KCHOL')
nav = basket_gap(W)
navi = basket_gap(W, col='intra')
navcc = basket_gap(W, col='cc')
sig = nav - K['gap']
X30 = bist('XU030'); XS = bist('XUSIN'); XB = bist('XBANK'); X100 = bist('XU100')
rows = []
def rec(name, y, x, **kw):
    s = ct3(y, x); print(f'{name:58s} {s}'); a = ct(y, x, T0); o = ct(y, x, SPLIT)
    rows.append({'test': name, 'corr': a[0], 't': a[1], 'n': a[2], 'oos_corr': o[0], 'oos_t': o[1], **kw})

print('=== A. sinyal bileşenleri ===')
rec('sig -> Kintra', K['intra'], sig)
rec('NAVgap alone -> Kintra', K['intra'], nav)
rec('-Kgap alone -> Kintra', K['intra'], -K['gap'])
rec('(NAVgap - X30gap) -> Kintra', K['intra'], nav - X30['gap'])
rec('(X30gap - Kgap) -> Kintra [genel piyasa-göreli gap]', K['intra'], X30['gap'] - K['gap'])
rec('sig_{t-1} -> Kintra_t (zaman plasebosu)', K['intra'], sig.shift(1))
rec('sig_t -> Kgap_{t+1}', K['gap'].shift(-1), sig)
rec('sig_t -> Kintra_{t+1}', K['intra'].shift(-1), sig)

print('\n=== C. kontroller (NW t) ===')
specs = {
    'nav+kgap': {'nav': nav, 'kgap': K['gap']},
    '+x30gap': {'nav': nav, 'kgap': K['gap'], 'x30': X30['gap']},
    '+xusin+xbank gap': {'nav': nav, 'kgap': K['gap'], 'x30': X30['gap'], 'xs': XS['gap'], 'xb': XB['gap']},
    '+lags (Kcc-1, NAVcc-1, X100cc-1)': {'nav': nav, 'kgap': K['gap'], 'x30': X30['gap'], 'xs': XS['gap'], 'xb': XB['gap'],
                                          'kcc1': K['cc'].shift(1), 'navcc1': navcc.shift(1), 'x100cc1': X100['cc'].shift(1)},
    '+X30intra (eşzamanlı, ayrıştırma)': {'nav': nav, 'kgap': K['gap'], 'x30': X30['gap'], 'x30i': X30['intra']},
}
for nm, Xd in specs.items():
    for lab, a, b in [('ALL', T0, None), ('IS', T0, SPLIT), ('OOS', SPLIT, None)]:
        r = reg(K['intra'], Xd, a, b)
        print(f'  {nm:38s} {lab:3s} n {r["n"]} ' + ' '.join(f'{k} {r["b"][k]:+.3f}({r["t"][k]:+.1f})' for k in Xd))
# hedef: KCHOL intra - beta*X30 intra (beta kayan 250g, look-ahead yok)
cv = K['intra'].rolling(250, min_periods=100).cov(X30['intra']).shift(1)
vv = X30['intra'].rolling(250, min_periods=100).var().shift(1)
beta = cv / vv
kh = K['intra'] - beta * X30['intra']
rec('sig -> Kintra - beta*X30intra (hedge\'li)', kh, sig)
rec('sig -> NAVintra (iştirakler ters yönde yakınsıyor mu?)', navi, sig)
rec('sig -> Kintra - NAVintra (çift)', K['intra'] - navi, sig)

print('\n=== B. sektör-eşleşmeli plasebo sepetler ===')
PEERS = {'TUPRS': ['PETKM', 'AKSEN', 'ENJSA', 'ZOREN', 'AYDEM', 'ODAS'], 'YKBNK': ['GARAN', 'AKBNK', 'ISCTR', 'VAKBN', 'HALKB', 'TSKB'],
         'FROTO': ['DOAS', 'KARSN', 'TMSN', 'ASUZU', 'BRISA'], 'ARCLK': ['VESTL', 'VESBE'], 'TOASO': ['DOAS', 'KARSN', 'ASUZU'],
         'AYGAZ': ['AKSEN', 'ENJSA', 'ODAS', 'ZOREN'], 'TTRAK': ['TMSN', 'KARSN', 'ASUZU'], 'OTKAR': ['ASELS', 'KARSN', 'ASUZU']}
allp = sorted({p for v in PEERS.values() for p in v})
G = pd.concat({p: bist(p)['gap'] for p in allp}, axis=1)
res = []
for it in range(400):
    w = {}
    for k, wt in W.items():
        p = rng.choice(PEERS[k]); w[p] = w.get(p, 0) + wt
    wv = pd.Series(w); g = G[list(w)]
    num = (g.fillna(0) * wv).sum(1); den = (g.notna() * wv).sum(1)
    b = (num / den).where(den >= 0.7)
    s = b - K['gap']
    a = ct(K['intra'], s, T0); o = ct(K['intra'], s, SPLIT)
    r = reg(K['intra'], {'b': b, 'kgap': K['gap'], 'x30': X30['gap']}, T0)
    res.append((a[1], o[1], r['t']['b'], r['b']['b']))
res = pd.DataFrame(res, columns=['t_sig', 't_oos', 't_b_ctrl', 'b_ctrl'])
r_real = reg(K['intra'], {'b': nav, 'kgap': K['gap'], 'x30': X30['gap']}, T0)
real = (ct(K['intra'], sig, T0)[1], ct(K['intra'], sig, SPLIT)[1], r_real['t']['b'], r_real['b']['b'])
print(res.describe(percentiles=[.5, .9, .95, .99]).round(2).to_string())
print('gerçek:', np.round(real, 2), ' yüzdelik:', [round(100 * (res.iloc[:, i] < real[i]).mean(), 1) for i in range(4)])
res.to_csv(OUT + '/res_sector_placebo.csv', index=False)
# saf sektör sepeti (eşit ağırlıklı her sektörün tüm akranları)
for nm, lst in [('bankalar (Koç dışı)', PEERS['YKBNK']), ('otomotiv akranları', ['DOAS', 'KARSN', 'TMSN', 'ASUZU']),
                ('enerji akranları', ['PETKM', 'AKSEN', 'ENJSA', 'ZOREN'])]:
    b = G[lst].mean(1)
    r = reg(K['intra'], {'b': b, 'kgap': K['gap'], 'x30': X30['gap']}, T0)
    print(f'  {nm:22s}: b {r["b"]["b"]:+.3f} t {r["t"]["b"]:+.2f} | with NAV: ', end='')
    r2 = reg(K['intra'], {'nav': nav, 'b': b, 'kgap': K['gap'], 'x30': X30['gap']}, T0)
    print(f'NAV {r2["b"]["nav"]:+.3f}({r2["t"]["nav"]:+.1f}) peer {r2["b"]["b"]:+.3f}({r2["t"]["b"]:+.1f})')
# Holding plasebosu: aynı kurgu SAHOL ve diğer holdingler için piyasa (XU030) 'NAV' yerine
for h in ['SAHOL', 'ALARK', 'DOHOL']:
    H = bist(h)
    rec(f'{h}: (X30gap - own gap) -> intra', H['intra'], X30['gap'] - H['gap'])
SW = {'AKBNK': .45, 'ENJSA': .10, 'CIMSA': .03, 'BRISA': .03}
S = bist('SAHOL'); snav = basket_gap(SW)
rec('SAHOL NAV ayrışması -> SAHOL intra (iddia: ~0)', S['intra'], snav - S['gap'])

print('\n=== E. uç değer / doğrusal olmama / alt dönem ===')
df = pd.concat([K['intra'].rename('y'), sig.rename('s'), K['gap'].rename('kg'), nav.rename('nav')], axis=1).dropna()
df = df[df.index >= T0]
print('Spearman ALL %.3f IS %.3f OOS %.3f' % (df.y.corr(df.s, 'spearman'), df[df.index < SPLIT].y.corr(df[df.index < SPLIT].s, 'spearman'),
      df[df.index >= SPLIT].y.corr(df[df.index >= SPLIT].s, 'spearman')))
for q in (0.99, 0.95, 0.90):
    thr = df.s.abs().quantile(q)
    d2 = df[df.s.abs() <= thr]
    print(f'  |sig| <= q{int(q*100)} ({1e4*thr:.0f} bps): corr {d2.y.corr(d2.s):+.3f} t {ct(d2.y, d2.s)[1]:+.2f} n {len(d2)}')
df['bin'] = pd.qcut(df.s, 10, labels=False)
print('  sig desil -> ort. Kintra (bps):', (1e4 * df.groupby('bin').y.mean()).round(1).tolist())
print('  sig desil ort sig (bps):       ', (1e4 * df.groupby('bin').s.mean()).round(1).tolist())
small = df[df.kg.abs() < 0.005]
print(f'  |Kgap|<%0,5 günleri: corr(sig, y) {small.y.corr(small.s):+.3f} t {ct(small.y, small.s)[1]:+.2f} n {len(small)}; '
      f'NAVgap alone {small.y.corr(small.nav):+.3f}')
zero = df[df.kg.abs() < 1e-9]
print(f'  Kgap==0 günleri n {len(zero)}: corr(nav, y) {zero.y.corr(zero.nav):+.3f}')
# 2 yıllık bloklar
for a in range(2014, 2027, 2):
    d2 = df[(df.index.year >= a) & (df.index.year < a + 2)]
    print(f'  {a}-{a+1}: corr {d2.y.corr(d2.s):+.3f} t {ct(d2.y, d2.s)[1]:+.2f} n {len(d2)}')
# yıl jackknife (her yılı çıkar)
jk = {y: ct(df[df.index.year != y].y, df[df.index.year != y].s)[1] for y in sorted(df.index.year.unique())}
print('  jackknife t (yıl çıkarılınca):', {k: round(v, 2) for k, v in jk.items()})

print('\n=== F. VİOP KCHOL vadelisi (gerçek enstrüman) ===')
F = f02.front('KCHOL')
F['vw_s'] = np.log(F.Fs / F.Fvw)   # VWAP girişi -> uzlaşma
F['vw_c'] = np.log(F.Fc / F.Fvw)   # VWAP girişi -> son işlem
F['o_c'] = np.log(F.Fc / F.Fo)     # vadeli açılışı (06:30, SİNYALDEN ÖNCE: ileriye bakmalı kıyas)
F['o_s'] = np.log(F.Fs / F.Fo)
j = F.join(pd.concat([sig.rename('sig'), K['intra'].rename('spot_intra')], axis=1), how='inner')
for per, a, b in [('2017+', '2017', '2099'), ('2020+ (likit)', '2020', '2099'), ('2023-11+', '2023-11-30', '2099'), ('2024-11-19+', '2024-11-19', '2099')]:
    jj = j[(j.index >= a) & (j.index < b)].dropna(subset=['sig'])
    out = [f'{per:14s} n {len(jj)}']
    for c in ['spot_intra', 'o_c', 'vw_s', 'vw_c']:
        cc = ct(jj[c], jj['sig'])
        out.append(f'{c} {cc[0]:+.3f}({cc[1]:+.1f})')
    print('  ' + ' | '.join(out))
# backtest: z>0.5 sig, 8/15 bps, VWAP girişi (vadeli) vs spot müzayede girişi
z = zsig(sig)
pos = np.sign(z).where(z.abs() > 0.5, 0)
for lab, tgt in [('spot müzayede->c (iddia, erişilemez)', K['intra']), ('vadeli VWAP->uzlaşma', F['vw_s'].reindex(K.index)),
                 ('vadeli VWAP->son işlem', F['vw_c'].reindex(K.index))]:
    for cost in (0, 8):
        r, _ = bt(pos, tgt, cost, start=pd.Timestamp('2020-01-01'))
        print(f'  BT 2020+ {lab:36s} {cost:2d}bps: ' + ' | '.join(f"{k} n {r[k][0]} {r[k][1]:+.1f}bps t {r[k][2]:+.2f}" for k in ('IS', 'OOS', 'ALL')))

print('\n=== G. h1 (2023-11+) ve m5 giriş zamanı ===')
h = load('KCHOL.IS', 'h1').copy(); h['d'] = pd.DatetimeIndex(h['ldate'].values)
first = h[h.index.hour == 6]  # 06:30 barı (müzayede + 07:00-07:30)
c0730 = first.set_index('d')['c']
h['tp'] = h['c']
rest = h[h.index.hour >= 7]
vw = (rest['c'] * rest['v']).groupby(rest['d']).sum() / rest['v'].groupby(rest['d']).sum()
hj = pd.DataFrame({'c0730': c0730, 'vw': vw}).join(K[['o', 'c', 'intra']], how='inner').join(sig.rename('sig'))
hj['o_0730'] = np.log(hj.c0730 / hj.o); hj['r0730_c'] = np.log(hj.c / hj.c0730); hj['vw_c'] = np.log(hj.c / hj.vw)
for c in ['intra', 'o_0730', 'r0730_c', 'vw_c']:
    cc = ct(hj[c], hj['sig']); print(f'  h1 {c:8s}: corr {cc[0]:+.3f} t {cc[1]:+.2f} n {cc[2]}')
m = load('KCHOL.IS', 'm5').copy(); m['d'] = pd.DatetimeIndex(m['ldate'].values)
def at(hh, mm, col):
    x = m[(m.index.hour == hh) & (m.index.minute == mm)]
    return x.set_index('d')[col]
mj = pd.DataFrame({'auc': at(6, 55, 'o'), 'o700': at(7, 0, 'o'), 'c700': at(7, 0, 'c'), 'c710': at(7, 10, 'c'), 'c725': at(7, 25, 'c')}).join(K[['o', 'c']], how='inner').join(sig.rename('sig'))
print('  m5: müzayede(06:55 o) == Yahoo günlük o oranı: %.2f' % np.isclose(mj.auc, mj.o).mean(), ' 07:00 açılışı == o: %.2f' % np.isclose(mj.o700, mj.o).mean())
for nm, e in [('o (müzayede)', 'o'), ('07:00 ilk işlem', 'o700'), ('07:05', 'c700'), ('07:15', 'c710'), ('07:30', 'c725')]:
    y = np.log(mj.c / mj[e]); cc = ct(y, mj.sig, L=2)
    print(f'  m5 giriş {nm:16s}: corr {cc[0]:+.3f} t {cc[1]:+.2f} n {cc[2]}; ort |getiri| {1e4*y.abs().mean():.0f} bps')
pd.DataFrame(rows).to_csv(OUT + '/res_kchol.csv', index=False)
