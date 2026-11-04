"""XU030 vadelisi kapanış bazı sıçraması (Δb) sağlamlık: (c) müzayede ve (e) baz bulgularının endeks düzeyindeki ortak adayı.
Sinyal: db_c_t = ln(F_kapanış/S_kapanış)_t − (aynı)_{t−1}; F_kapanış = XU030 vadelisi son işlem (18:15, spot kapanışından 5 dk sonra),
S_kapanış = XU030 spot kapanışı (18:10). z = db_c / std_L(db_c) (t−1'e kadar). Yön: −sign(z) (vadeli spot'a göre ucuz kaldıysa al).
Giriş E1 = vadeli kapanış_t (sinyal tam biliniyor), çıkış uzlaşma_{t+h}. Maliyet endeks vadelisi 3 bps (8 bps kötümser)."""
from klib import *
C = ctx(); vcal = C['vcal']
B = pd.read_parquet(S + '/out/code_y_viop/results/basis_panel.parquet'); B['date'] = pd.to_datetime(B['date'])
X = B[B.und == 'XU030'].set_index('date').sort_index()
same = X['L_code'].shift(1) == X['L_code']  # DÜZELTME: sözleşme değişiminde Δb tanımsız
X['db_c'] = X['b_L_close'].diff().where(same); X['db'] = X['b_L'].diff().where(same)
X.loc[(X.L_dte <= 1) | (X.L_trades < 5), ['db_c', 'db']] = np.nan
X.loc[X['L_dte'].shift(1) <= 1, ['db_c', 'db']] = np.nan  # vade geçişinde sözleşme değişimi
CF = pd.read_parquet(S + '/out/code_y_akis/_cal_flags.parquet'); CF.index = pd.to_datetime(CF.index)
half = CF.index[CF.pre_rel.astype(bool)]
out = []
F1 = {h: C['F'][f'f1_{h}']['XU030'] for h in H}; F0 = {h: C['F'][f'f0_{h}']['XU030'] for h in H}
def run(name, z, thr, h, entry='E1', side_filter=None, excl_half=False, label=''):
    on = z.abs() > thr; d = z.index[on.fillna(False)]
    if excl_half: d = d.difference(half)
    sd_ = -np.sign(z.loc[d])
    if side_filter == 'long': d = d[sd_ > 0]; sd_ = sd_[sd_ > 0]
    if side_filter == 'short': d = d[sd_ < 0]; sd_ = sd_[sd_ < 0]
    f = (F1 if entry == 'E1' else F0)[h].reindex(d).values
    if entry == 'E2':
        d2 = shift_date(d, 1, vcal); f = F0[h].reindex(d2).values; d = d2
    tr = pd.DataFrame({'date': d, 'ret': sd_.values * f}).dropna()
    st = trade_stats(tr, 'ret', h=h, costs=[3, 8])
    reg('e2_xu030', f'XU030 Δb sağlamlık {name}', 'XU030F', entry, h, st, dict(thr=thr))
    out.append(f'{name:38s} |z|>{thr:<4} {entry} h{h} {fmt(st)}')
for L in [60, 120, 250]:
    z = X['db_c'] / X['db_c'].rolling(L, min_periods=L // 2).std().shift(1)
    for thr in [0.75, 1.0, 1.25, 1.5]:
        for h in [1, 2, 3]:
            run(f'db_c z{L}', z, thr, h)
# taşıma (faiz·τ) düzeltmeli Δ: d(b_close − b*) — faiz şoklarının mekanik baz değişimini ayıklar
X['dac'] = (X['b_L_close'] - X['b_star']).diff().where(same)
X.loc[(X.L_dte <= 1) | (X.L_trades < 5) | (X['L_dte'].shift(1) <= 1), 'dac'] = np.nan
za = X['dac'] / X['dac'].rolling(120, min_periods=60).std().shift(1)
for thr in [0.75, 1.0, 1.5]:
    for h in [1, 2]:
        run('d(b_close−b*) z120 taşıma düzeltmeli', za, thr, h)
print('Δb_c ile d(b−b*) korelasyonu:', round(X[['db_c', 'dac']].corr().iloc[0, 1], 3), '| d(b−b*) std bps:', round(1e4 * X['dac'].std(), 1))
z = X['db_c'] / X['db_c'].rolling(120, min_periods=60).std().shift(1)
for h in [1, 2, 3]:
    run('db_c z120 yalnız AL', z, 1.0, h, side_filter='long'); run('db_c z120 yalnız SAT', z, 1.0, h, side_filter='short')
    run('db_c z120 arife hariç', z, 1.0, h, excl_half=True)
    run('db_c z120 E2 (plasebo: 1 gün geç)', z, 1.0, h, entry='E2')
# sürekli: f1_1 ~ −db_c eğimi
d = pd.concat([X['db_c'].rename('x'), F1[1].rename('y')], axis=1).dropna()
b = np.polyfit(d.x, d.y, 1)[0]; c = d.x.corr(d.y)
print(f'Sürekli: vadeli(kapanış_t→uzlaşma_t+1) ~ Δb_c eğim {b:.3f} (−1 = tam kapanma), corr {c:.3f}, n {len(d)}')
for y0, y1 in [(2017, 2019), (2020, 2022), (2023, 2026)]:
    s = d[(d.index.year >= y0) & (d.index.year <= y1)]; print(f'  {y0}-{y1}: eğim {np.polyfit(s.x, s.y, 1)[0]:.3f} corr {s.x.corr(s.y):.3f} n {len(s)}')
# müzayede (CA_x, 2023-11+) ile ilişki
A = pd.read_parquet(S + '/out/code_v_YG2_b/res/panel.parquet'); A['date'] = pd.to_datetime(A['date'])
ca = A[A.sym == 'XU030'].set_index('date')['CA']
j = pd.concat([ca, X['db_c']], axis=1).dropna(); print('CA_x ile Δb_c korelasyonu (yaz günleri, 2023-11+):', round(j.corr().iloc[0, 1], 3), 'n', len(j))
for o in out: print(o)
D = save_registry('e2_xu030'); print('test sayısı', len(D))
