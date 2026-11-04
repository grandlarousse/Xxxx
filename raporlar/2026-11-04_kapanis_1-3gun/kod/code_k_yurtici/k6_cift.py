"""(f) Çift/küme göreli dönüş, 1–3 gün, VİOP uzlaşmasından giriş/çıkış; (h) Koza grubu (TRALT/TRMET/TRENJ) kapanıştan kapanışa.
Spread günlük getirisi u_t = r_A − β·r_B (β: spot 250g OLS, t−1'e kadar, [0,3;2] kırpılmış).
Sinyaller (t kapanışında bilinir):
  Z20/Z60: kümülatif spread'in L günlük z-skoru; |z|>1,5 / 2,0
  REV1/REV3: son k günün spread getirisi / (σ60·√k); |z|>1,5 / 2,0
İşlem: −sign(z) spread, tutma h ∈ {1,2,3,5}, E0 = uzlaşma_t, E2 = uzlaşma_{t+1}. Getiri sermaye başına: (A − β·B)/(1+β) (iki bacak toplam 1 birim);
maliyet bacak başına gidiş-dönüş c -> net = brüt − c. Spot kıyası aynı kurallarla (2014+).
Sinyaller VİOP testinde VİOP uzlaşma getirilerinden, spot testinde spot getirilerinden hesaplanır.
"""
from klib import *
C = ctx(); vcal = C['vcal']; scal = C['scal']
r_s = C['r']
r_f = C['F']['f0_1'].shift(1)  # t-1 uzlaşma -> t uzlaşma (t-1'de seçilen sözleşme)
PAIRS = [('AKBNK', 'GARAN'), ('YKBNK', 'ISCTR'), ('VAKBN', 'HALKB'), ('THYAO', 'PGSUS'), ('EREGL', 'KRDMD'), ('FROTO', 'TOASO'), ('TRALT', 'TRMET'),
         ('MGROS', 'SOKM'), ('TCELL', 'TTKOM'), ('CIMSA', 'OYAKC'), ('KCHOL', 'SAHOL'), ('TUPRS', 'PETKM')]
# ASELS için ortak: IS döneminde (2014–2020) XU100 kontrollü kısmi korelasyonu en yüksek VİOP47 hissesi (sonuca bakmadan seçim)
m = r_s['XU100']; IS = r_s.index <= S_IS_END
res = {}
for u in VIOP47:
    if u == 'ASELS': continue
    d = pd.concat([r_s['ASELS'], r_s[u], m], axis=1).dropna(); d = d[d.index <= S_IS_END]
    if len(d) < 500: continue
    ea = d.iloc[:, 0] - np.polyfit(d.iloc[:, 2], d.iloc[:, 0], 1)[0] * d.iloc[:, 2]; eb = d.iloc[:, 1] - np.polyfit(d.iloc[:, 2], d.iloc[:, 1], 1)[0] * d.iloc[:, 2]
    res[u] = np.corrcoef(ea, eb)[0, 1]
best = max(res, key=res.get); print('ASELS ortak (IS kısmi korelasyon):', best, round(res[best], 3), '| ilk 3:', sorted(res.items(), key=lambda x: -x[1])[:3])
PAIRS.append(('ASELS', best))
SIGS = [('Z20', 20, 1.5), ('Z20', 20, 2.0), ('Z60', 60, 1.5), ('Z60', 60, 2.0), ('REV1', 1, 1.5), ('REV1', 1, 2.0), ('REV3', 3, 1.5), ('REV3', 3, 2.0)]
def beta_pair(a, b):
    bb = (r_s[a].rolling(250, min_periods=120).cov(r_s[b]) / r_s[b].rolling(250, min_periods=120).var()).shift(1)
    return bb.clip(0.3, 2.0)
def signal(u, kind, L):
    if kind.startswith('Z'):
        Sx = u.fillna(0).cumsum().where(u.notna())
        mu = Sx.rolling(L, min_periods=int(L * 0.8)).mean(); sd = Sx.rolling(L, min_periods=int(L * 0.8)).std()
        return (Sx - mu) / sd
    sd = u.rolling(60, min_periods=40).std()
    return u.rolling(L, min_periods=L).sum() / (sd * np.sqrt(L))
POOL = {}
out = []
for a, b in PAIRS:
    beta = beta_pair(a, b)
    for inst in ['VIOP', 'SPOT']:
        if inst == 'VIOP':
            ra, rb = r_f[a], r_f[b]; cal = vcal; ise = V_IS_END
            FA = {h: C['F'][f'f0_{h}'][a] for h in H}; FB = {h: C['F'][f'f0_{h}'][b] for h in H}
        else:
            ra, rb = r_s[a], r_s[b]; cal = scal; ise = S_IS_END
            FA = {h: C['SF'][h][a] for h in H}; FB = {h: C['SF'][h][b] for h in H}
        bt = beta.reindex(ra.index).ffill()
        u = (ra - bt * rb)
        for kind, L, thr in SIGS:
            z = signal(u, kind, L)
            on = z.abs() > thr
            dates = z.index[on.fillna(False)]
            for h in H:
                for entry in (['E0', 'E2'] if inst == 'VIOP' else ['E0']):
                    sh = 1 if entry == 'E2' else 0
                    ed = shift_date(dates, sh, cal)
                    ok = ~pd.isna(ed)
                    sd_ = -np.sign(z.loc[dates[ok]].values)
                    ee = ed[ok]
                    fa = FA[h].reindex(ee).values; fb = FB[h].reindex(ee).values; bb = bt.reindex(dates[ok]).values
                    ret = sd_ * (fa - bb * fb) / (1 + bb)
                    tr = pd.DataFrame({'date': ee, 'ret': ret}).dropna()
                    st = trade_stats(tr, 'ret', h=h, is_end=ise)
                    newe = int((on & ~on.shift(1, fill_value=False)).sum())
                    yrs = max((tr.date.max() - tr.date.min()).days / 365.25, 0.5) if len(tr) else 1
                    st['new_entries_per_yr'] = round(newe / yrs, 1)
                    name = f'{a}-{b} {kind}>{thr}'
                    reg('f_cift', name, inst, entry, h, st, dict(pair=f'{a}-{b}', sig=kind, thr=thr))
                    if len(tr): POOL.setdefault((inst, entry, kind, thr, h), []).append(tr.assign(pair=f'{a}-{b}'))
                    if h in (1, 3) and entry == 'E0': out.append(f'{name:24s} {inst:4s} {entry} h{h} yeni giriş/yıl {st["new_entries_per_yr"]:5.1f} {fmt(st)}')
for o in out: print(o)
print('\n=== HAVUZ (tüm çiftler, eşit ağırlık işlem) ===')
for (inst, entry, kind, thr, h), L in POOL.items():
    tr = pd.concat(L)
    st = trade_stats(tr, 'ret', h=h, is_end=V_IS_END if inst == 'VIOP' else S_IS_END)
    reg('f_cift', f'HAVUZ {kind}>{thr}', inst, entry, h, st, dict(pair='HAVUZ', sig=kind, thr=thr))
    print(f'HAVUZ {kind}>{thr} {inst} {entry} h{h} {fmt(st)}')
D = save_registry('f_cift'); print('test sayısı', len(D))
