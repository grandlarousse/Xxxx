"""W3-C çürütme taraması: A5_gecikme1_viop3_h3 (XU030 z ≥ 1 ve XELKT z < 0,5 → AKSEN/ENJSA/ODAS AL, 3 gün).

Kullanım: python3 -I tara.py <panel_dev> <cikti.csv> [<oos1_sonuc.csv>]
Her CSV satırı elib.evaluate() / evaluate_viop() çıktısıdır; ek istatistikler 'ek_' önekli sütunlardadır.
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
sys.path.insert(0, HERE)
import elib  # noqa: E402
import rules as R  # noqa: E402

DATA, OUT = sys.argv[1], sys.argv[2]
OOS_CSV = sys.argv[3] if len(sys.argv) > 3 else None
P = elib.load(DATA)
idx = P['ret_cc'].index
IS_END, O1, O2 = elib.IS_END, elib.OOS1_START, elib.OOS1_END
V3 = R.VIOP3
rows = []


def per_mask(i, per):
    return (i <= IS_END) if per == 'IS' else ((i >= O1) & (i <= O2))


def dayser(sig, h, PP=None, measure='own', min_n=1):
    PP = PP or P
    cols = [c for c in sig.columns if c in PP['ret_cc'].columns]
    M, fl = elib.excess_measures(PP, h, 'long', cols)
    p, n, X = elib.day_series(sig[cols].reindex(PP['ret_cc'].index).fillna(False).astype(bool), M[measure], fl, min_n)
    return p.dropna()


def ev(name, sig, h=3, soru='', min_n=1, PP=None, **kw):
    PP = PP or P
    ex = {'soru': soru}
    p = dayser(sig, h, PP, min_n=min_n)
    for per in ['IS', 'OOS1']:
        q = p[per_mask(p.index, per)]
        ex[f'ek_sd_gun_{per}_bps'] = 1e4 * q.std() if len(q) > 2 else np.nan
        ex[f'ek_top3_haric_{per}_bps'] = 1e4 * q.sort_values().iloc[:-3].mean() if len(q) > 6 else np.nan
        ex[f'ek_medyan_{per}_bps'] = 1e4 * q.median() if len(q) else np.nan
    ex.update(kw)
    row = elib.evaluate(sig, PP, h=h, side='long', measure='own', name=name, family='W3C', min_n=min_n, extra=ex)
    rows.append(row)
    return row


def augment(P):
    """Sözde sütunlu panel kopyası (kütüphane değişmez): XU030 (endeks), XU030F (yakın vade vadeli, uzlaşma),
    <hisse>_H = hisse − β(XU030; 250 gün, 1 gün gecikmeli)·XU030 (endeks vadelisiyle korunmuş üçlü)."""
    Q = dict(P)
    Q['_cache'] = {}
    rx = P['idx_ret']['XU030'].reindex(idx)
    Rc = P['ret_cc'].copy()
    new = {'XU030': rx, 'XU030F': elib.viop_returns(P, 'settle')['XU030']}
    beta = elib.beta_lagged(P['ret_cc'][V3], rx)
    for c in V3:
        new[c + '_H'] = P['ret_cc'][c] - beta[c] * rx
    for k, v in new.items():
        Rc[k] = v
    Q['ret_cc'] = Rc
    for nme in ['lim_up', 'lim_dn', 'fill_long', 'fill_short', 'tradable', 'close_raw', 'ret_co']:
        X = P[nme].copy()
        for k in new:
            src = k[:-2] if k.endswith('_H') else None
            if nme in ('lim_up', 'lim_dn'):
                X[k] = P[nme][src] if src else False
            elif nme in ('fill_long', 'fill_short', 'tradable'):
                X[k] = P[nme][src] if src else Rc[k].notna()
            elif nme == 'close_raw':
                X[k] = P[nme][src] if src else np.nan
            else:
                X[k] = np.nan
        Q[nme] = X
    op = P['idx_open']['XU030'].reindex(idx)
    Q['ret_co']['XU030'] = op / P['idx']['XU030'].reindex(idx).shift(1) - 1
    return Q, beta


def welch(a, b):
    if len(a) < 3 or len(b) < 3:
        return np.nan, np.nan
    d = a.mean() - b.mean()
    return 1e4 * d, d / np.sqrt(a.var() / len(a) + b.var() / len(b))


P2, BETA = augment(P)
zx, ze = R.index_z(P)
S = {'a_kosulsuz': R.lag_signal(P, 1.0, mode='none'),
     'b_sektor_da_guclu': R.lag_signal(P, 1.0, 0.5, mode='ge'),
     'c_ozgun_gecikme': R.lag_signal(P, 1.0, 0.5, mode='lt')}

print('=== S0: ölçünün taban kayması (her gün AL; own ölçüsünün dönem ortalaması) ===')
ALL = pd.Series(True, index=idx)
for h in (1, 2, 3):
    ev(f'S0_hergun_viop3_h{h}', R.spread(P, ALL, 'viop3')[0], h, 'S0')
ev('S0_hergun_sepet_h3', R.spread(P, ALL, 'sepet')[0], 3, 'S0', min_n=5)
ev('S0_hergun_BIG5_h3', R.spread(P, ALL, elib.BIG)[0], 3, 'S0')
ev('S0_hergun_XU030endeks_h3', R.spread(P2, ALL, 'XU030')[0], 3, 'S0', PP=P2)
ev('S0_hergun_XU030vadeli_h3', R.spread(P2, ALL, 'XU030F')[0], 3, 'S0', PP=P2)
ev('S0_hergun_viop3_XU030korumali_h3', R.spread(P2, ALL, [c + '_H' for c in V3])[0], 3, 'S0', PP=P2)
sdd = P['idx_ret'][['XU030', 'XELKT']].reindex(idx).rolling(60, min_periods=40).std().shift(1)
for per in ['IS', 'OOS1']:
    m = per_mask(idx, per)
    print(f'  {per}: medyan 60 günlük std XU030 %{100 * sdd.XU030[m].median():.2f}, XELKT %{100 * sdd.XELKT[m].median():.2f}; '
          f'(c) günlerinde medyan XU030 getirisi %{100 * P["idx_ret"]["XU030"].reindex(idx)[m & S["c_ozgun_gecikme"]].median():.2f}, '
          f'XELKT %{100 * P["idx_ret"]["XELKT"].reindex(idx)[m & S["c_ozgun_gecikme"]].median():.2f}, '
          f'üçlü ort. %{100 * P["ret_cc"][V3][m & S["c_ozgun_gecikme"]].mean(axis=1).median():.2f}')

print('=== S1: gecikme mi, piyasa momentumu mu? (üçlü, h3, own) ===')
for k, s in S.items():
    ev(f'S1_{k}_viop3_h3', R.spread(P, s, 'viop3')[0], 3, 'S1')
    ev(f'S1_{k}_XU030endeks_h3', R.spread(P2, s, 'XU030')[0], 3, 'S1', PP=P2)
    ev(f'S1_{k}_XU030vadeli_h3', R.spread(P2, s, 'XU030F')[0], 3, 'S1', PP=P2)
    ev(f'S1_{k}_viop3_XU030korumali_h3', R.spread(P2, s, [c + '_H' for c in V3])[0], 3, 'S1', PP=P2)
    for hh in (1, 2):
        ev(f'S1_{k}_XU030endeks_h{hh}', R.spread(P2, s, 'XU030')[0], hh, 'S1', PP=P2)
pb = dayser(R.spread(P, S['b_sektor_da_guclu'], 'viop3')[0], 3)
pc = dayser(R.spread(P, S['c_ozgun_gecikme'], 'viop3')[0], 3)
pa = dayser(R.spread(P, S['a_kosulsuz'], 'viop3')[0], 3)
for per in ['IS', 'OOS1']:
    d, t = welch(pc[per_mask(pc.index, per)], pb[per_mask(pb.index, per)])
    print(f'  fark (c) − (b) {per}: {d:.0f} bps, Welch t = {t:.2f}')
    q = pa[per_mask(pa.index, per)]
    zz = ze.reindex(q.index)
    ok = zz.notna()
    b1 = np.polyfit(zz[ok], q[ok], 1)[0]
    print(f'  zX≥1 günlerinde f3_own ~ zXELKT eğimi {per}: {1e4 * b1:.0f} bps / 1 z; korelasyon {np.corrcoef(zz[ok], q[ok])[0, 1]:.3f}; n {ok.sum()}')
print('  β(XU030) ortalaması sinyal günlerinde:', BETA[S['c_ozgun_gecikme'].values].mean().round(2).to_dict())

print('=== S2: hangi hisse, sektörün geri kalanı ===')
for k in ['a_kosulsuz', 'c_ozgun_gecikme', 'b_sektor_da_guclu']:
    for hedef in V3 + ['likit10', 'likit10_ex3', 'sepet', 'sepet_ex3', elib.BIG]:
        sig, mn = R.spread(P, S[k], hedef)
        hn = hedef if isinstance(hedef, str) else 'BIG5'
        ev(f'S2_{k}_{hn}_h3', sig, 3, 'S2', min_n=mn)

print('=== S3: parametre komşuluğu (üçlü) ===')
for win in (60, 40, 120):
    for thx in (0.75, 1.0, 1.25, 1.5, 2.0):
        for the, mode in ((0.0, 'lt'), (0.5, 'lt'), (1.0, 'lt'), (None, 'none'), (0.5, 'ge')):
            for h in ((1, 2, 3, 5) if win == 60 else (3,)):
                s = R.lag_signal(P, thx, the if the is not None else 0, win, mode)
                tag = {'lt': f'E_lt{the}', 'ge': f'E_ge{the}', 'none': 'kosulsuz'}[mode]
                ev(f'S3_w{win}_X_ge{thx}_{tag}_viop3_h{h}', R.spread(P, s, 'viop3')[0], h, 'S3',
                   ek_win=win, ek_thx=thx, ek_the=the, ek_mode=mode)

print('=== S4: kaydırma p-değeri, kümelenme ===')
SH = {}
for k, s in S.items():
    sg = R.spread(P, s, 'viop3')[0]
    for per, kw in (('IS', dict(end=IS_END)), ('OOS1', dict(start=O1, end=O2))):
        real, pv, null = elib.shift_null(sg, P, h=3, n=1000, seed=7, **kw)
        SH[(k, per)] = (real, pv, np.nanmean(null), np.nanpercentile(null, 95))
        print(f'  kaydırma {k} {per}: gerçek {real:.0f} bps, p = {pv:.3f}, sıfır ort {np.nanmean(null):.0f}, %95 {np.nanpercentile(null, 95):.0f}')
for r_ in rows:
    for k in S:
        if r_['sinyal_tanimi'] == f'S1_{k}_viop3_h3':
            r_['ek_kaydirma_p_IS'], r_['ek_kaydirma_p_OOS1'] = SH[(k, 'IS')][1], SH[(k, 'OOS1')][1]
sc_ = S['c_ozgun_gecikme']
pos = np.where(sc_.values)[0]
gaps = np.diff(pos)
for per in ['IS', 'OOS1']:
    m = per_mask(idx, per)
    pp = np.where(sc_.values & m)[0]
    g = np.diff(pp)
    cl5 = 1 + int((g > 5).sum()) if len(pp) else 0
    q = pc[per_mask(pc.index, per)]
    mon = q.groupby(q.index.to_period('M')).size()
    print(f'  (c) {per}: sinyal günü {len(pp)}, dolabilir gün {len(q)}, ardışık (aralık=1) çift {int((g == 1).sum())}, aralık ≤3 {int((g <= 3).sum())}, '
          f'>5 gün aralıklı küme {cl5}, en yoğun ay {mon.idxmax()} ({mon.max()} gün), ≥2 gün olan ay {int((mon >= 2).sum())}/{len(mon)}')
q = pc[per_mask(pc.index, 'OOS1')]
print('  (c) OOS1 gün gün (bps, own f3):')
print('   ' + '; '.join(f'{d.date()}:{1e4 * v:.0f}' for d, v in q.items()))
print('  (c) OOS1 yıllara göre:', (1e4 * q.groupby(q.index.year).mean()).round(0).to_dict(), q.groupby(q.index.year).size().to_dict())
qi = pc[per_mask(pc.index, 'IS')]
print('  (c) IS yıllara göre:', (1e4 * qi.groupby(qi.index.year).mean()).round(0).to_dict())
print('  (c) IS yıl gün sayısı:', qi.groupby(qi.index.year).size().to_dict())

print('=== S5: giriş gecikmesi, 17:00 sinyali ===')
for k in ['a_kosulsuz', 'c_ozgun_gecikme']:
    sg = R.spread(P, S[k], 'viop3')[0]
    ev(f'S5_{k}_viop3_giris_t+1kapanis_h3', sg.shift(1, fill_value=False), 3, 'S5')
    ev(f'S5_{k}_viop3_giris_t+1kapanis_h2', sg.shift(1, fill_value=False), 2, 'S5')


def hourly17(P):
    out = {}
    for s in ['XELKT', 'XU030']:
        d = pd.read_parquet(os.path.join(P['dir'], 'h1_isy', s + '.parquet'))[['ts_tr', 'c']].copy()
        d['ts_tr'] = pd.to_datetime(d['ts_tr'])
        d = d.sort_values('ts_tr')
        d['date'] = d['ts_tr'].dt.normalize()
        d['hr'] = d['ts_tr'].dt.hour
        v17 = d[d.hr <= 16].groupby('date').c.last()      # 17:00'de bilinen değer (16:00 damgalı bar)
        v18 = d[d.hr <= 17].groupby('date').c.last()      # ~18:00 (kapanış seansı öncesi son değer) — üst sınır
        has17 = d[d.hr == 16].groupby('date').c.size()
        cl = d[d.hr == 18].groupby('date').c.last()
        W = pd.DataFrame({'k17': v17 / cl, 'k18': v18 / cl})
        ok = (has17.reindex(W.index).fillna(0) > 0) & cl.reindex(W.index).notna()
        out[s] = W[ok].reindex(idx)
    return out


H = hourly17(P)
r = P['idx_ret'][['XELKT', 'XU030']].reindex(idx)
sd = r.rolling(60, min_periods=40).std().shift(1)
valid = H['XELKT']['k17'].notna() & H['XU030']['k17'].notna()
Sc = S['c_ozgun_gecikme'] & valid
Sa = S['a_kosulsuz'] & valid
for tag in ['k17', 'k18']:
    zx17 = ((1 + r['XU030']) * H['XU030'][tag] - 1) / sd['XU030']
    ze17 = ((1 + r['XELKT']) * H['XELKT'][tag] - 1) / sd['XELKT']
    S17 = ((zx17 >= 1) & (ze17 < 0.5)).fillna(False) & valid
    A17 = (zx17 >= 1).fillna(False) & valid
    lab = '1700' if tag == 'k17' else '1800on'
    for per in ['IS', 'OOS1']:
        m = per_mask(idx, per)
        for nm, s17, sk in (('gecikme', S17, Sc), ('kosulsuz', A17, Sa)):
            hit, n17, nk = int((s17 & sk & m).sum()), int((s17 & m).sum()), int((sk & m).sum())
            print(f'  {lab} {nm} {per} (2017+): kapanış sinyali {nk}, {lab} sinyali {n17}, ortak {hit} → yakalama %{100 * hit / max(nk, 1):.0f}, yanlış %{100 * (n17 - hit) / max(n17, 1):.0f}')
    ev(f'S5_gecikme_sinyal{lab}_viop3_h3', R.spread(P, S17, 'viop3')[0], 3, 'S5')
    ev(f'S5_gecikme_sinyal{lab}_isabet_viop3_h3', R.spread(P, S17 & Sc, 'viop3')[0], 3, 'S5')
    ev(f'S5_gecikme_sinyal{lab}_yanlis_viop3_h3', R.spread(P, S17 & ~Sc, 'viop3')[0], 3, 'S5')
    ev(f'S5_gecikme_sinyal{lab}_kacan_viop3_h3', R.spread(P, Sc & ~S17, 'viop3')[0], 3, 'S5')
    ev(f'S5_kosulsuz_sinyal{lab}_viop3_h3', R.spread(P, A17, 'viop3')[0], 3, 'S5')
    ev(f'S5_kosulsuz_sinyal{lab}_yanlis_viop3_h3', R.spread(P, A17 & ~Sa, 'viop3')[0], 3, 'S5')
ev('S5_gecikme_kapanis_sinyali_2017+_viop3_h3', R.spread(P, Sc, 'viop3')[0], 3, 'S5')
ev('S5_kosulsuz_kapanis_sinyali_2017+_viop3_h3', R.spread(P, Sa, 'viop3')[0], 3, 'S5')

print('=== S6: vadeli ile uygulama ===')
for k in ['a_kosulsuz', 'c_ozgun_gecikme']:
    for h in (1, 2, 3):
        rule = {'ad': f'S6_{k}_viop3_h{h}', 'sig': R.spread(P, S[k], 'viop3')[0], 'h': h, 'yon': 'long', 'olcu': 'own',
                'arac': 'viop', 'birincil': False, 'aciklama': ''}
        for rw in elib.eval_rule(rule, P, family='W3C'):
            rw['soru'] = 'S6'
            rows.append(rw)

df = pd.DataFrame(rows)


def etiket(x):
    ad, soru = x['sinyal_tanimi'], x['soru']
    sozde = any(k in ad for k in ('XU030endeks', 'XU030vadeli', 'korumali'))
    if ad == 'S1_c_ozgun_gecikme_viop3_h3':
        return 'ozgun', 'A5_gecikme1_viop3_h3 ile aynı kural; yeniden dondurulmadı (kasaya A5 adıyla ayrıca giriyor)'
    if soru == 'S0':
        return 'bilgi', 'her gün AL: own ölçüsünün dönem içi taban değeri (OOS-1de eksi: 2022 rallisi gecikmeli ortalamayı şişiriyor)' + \
            ('; sözde sütun, maliyet sütunları anlamsız' if sozde else '')
    if sozde:
        return 'bilgi', 'sözde sütun (endeks / endeks vadelisi / XU030 β korumalı üçlü): alınıp satılan araç değil, maliyet ve net sütunları anlamsız'
    if soru == 'S1':
        return 'karsilastirma', ('koşulsuz sürüm = (b) + (c); (b) yarısı etkisiz, yani özgünün seyreltilmişi: dondurulmadı' if '_a_' in ad
                                 else 'sektör geride değilken etki yok (t ≤ 1)')
    if soru == 'S2':
        return 'elendi', 'hedef değişikliği özgün üçlüden belirgin biçimde sağlam değil; dondurulmadı'
    if soru == 'S3':
        return 'komsuluk', 'parametre komşusu; seçim için kullanılmadı (OOS-1e bakarak eşik seçmek gözetleme olur)'
    if soru == 'S5':
        return 'bilgi', 'giriş gecikmesi / 17:00 ve ~18:00 değerleriyle kurulan sinyal (2017+); keşif'
    if soru == 'S6':
        return 'bilgi', 'vadeli uygulaması (kontrat listelenince başlar: ENJSA 2018-12, ODAS 2021-04, AKSEN 2022-11); viop_vadeli satırı ikisinin kötüsü'
    return 'tarama', ''


et = df.apply(etiket, axis=1)
df['secim'] = [e[0] for e in et]
df['not'] = [e[1] for e in et]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False)

pd.set_option('display.width', 260); pd.set_option('display.max_rows', 400); pd.set_option('display.max_columns', 40)
show = ['sinyal_tanimi', 'arac', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS', 'n_bagimsiz_OOS1', 'ort_fazla_OOS1_bps', 't_OOS1',
        'net_temel_bps_IS', 'net_temel_bps_OOS1', 'dol_mkt_IS_bps', 'dol_mkt_OOS1_bps', 'top10_haric_bps', 'yil_pozitif_orani',
        'ek_top3_haric_OOS1_bps', 'ek_medyan_OOS1_bps', 'giris_acilis1_bps', 'giris_kapanis1_bps', 'gece_payi']
T = df[show].copy()
T.columns = ['ad', 'arac', 'nIS', 'IS', 'tIS', 'nO', 'OOS', 'tO', 'netIS', 'netO', 'mktIS', 'mktO', 'top10', 'yil+', 'top3O', 'medO', 'acl1', 'kap1', 'gece']
from math import erf, sqrt  # noqa: E402


def guc(etki, sd, n, zcrit):
    """Tek yönlü testte güç: P(Z > zcrit − etki/(sd/√n))."""
    return 1 - 0.5 * (1 + erf((zcrit - etki / (sd / sqrt(max(n, 1)))) / sqrt(2)))


print('--- S6 ham getiri (spot, kontrat döneminde) | vadeli ham (uzlaşma)')
v_ = df[df.soru == 'S6']
print(v_[['sinyal_tanimi', 'arac', 'dol_raw_IS_bps', 'dol_raw_OOS1_bps', 'settle_ham_IS_bps', 'settle_ham_OOS1_bps', 'maliyet_temel_bps',
          'settle_maliyet_temel_bps', 'net_muhafazakar_bps_IS', 'net_muhafazakar_bps_OOS1']].round(1).to_string(index=False))
for s_ in ['S0', 'S1', 'S2', 'S5', 'S6']:
    print(f'--- {s_}')
    print(T[df.soru == s_].round(2).to_string(index=False))
print('--- S3 (win 60): OOS/IS bps (t) ızgara')
g = df[df.soru == 'S3'].copy()
g['hucre'] = g.apply(lambda x: f"{x.ort_fazla_IS_bps:.0f}({x.t_IS:.1f})/{x.ort_fazla_OOS1_bps:.0f}({x.t_OOS1:.1f}) n{x.n_bagimsiz_IS:.0f}/{x.n_bagimsiz_OOS1:.0f}", axis=1)
g['kos'] = g.ek_mode + g.ek_the.fillna(-1).astype(str)
for win in (60, 40, 120):
    for h in ((1, 2, 3, 5) if win == 60 else (3,)):
        print(f'win {win}, h {h}:  IS bps(t)/OOS1 bps(t) nIS/nOOS')
        print(g[(g.ek_win == win) & (g.h == h)].pivot(index='ek_thx', columns='kos', values='hucre').to_string())
print('--- S6 ayrıntı')
v = df[(df.soru == 'S6') & (df.arac == 'viop_vadeli')]
print(v[['sinyal_tanimi', 'settle_n_bagimsiz_IS', 'settle_fazla_IS_bps', 'settle_t_IS', 'last_fazla_IS_bps', 'settle_n_bagimsiz_OOS1', 'settle_fazla_OOS1_bps',
         'settle_t_OOS1', 'last_fazla_OOS1_bps', 'last_t_OOS1', 'settle_ham_OOS1_bps', 'settle_net_temel_OOS1_bps', 'last_net_temel_OOS1_bps', 'settle_maliyet_temel_bps',
         'settle_yillar_bps']].round(1).to_string(index=False))

print('=== S7: güç ===')
c = df[df.sinyal_tanimi == 'S1_c_ozgun_gecikme_viop3_h3'].iloc[0]
a = df[df.sinyal_tanimi == 'S1_a_kosulsuz_viop3_h3'].iloc[0]
nd = {'IS': int(per_mask(idx, 'IS').sum()), 'OOS1': int(per_mask(idx, 'OOS1').sum())}
for nm, rw in (('c_ozgun', c), ('a_kosulsuz', a)):
    for per in ['IS', 'OOS1']:
        rate = rw[f'n_bagimsiz_{per}'] / nd[per]
        n_k = rate * 350
        sdv = rw[f'ek_sd_gun_{per}_bps']
        print(f'  {nm} {per}: gün {nd[per]}, bağımsız olay {rw[f"n_bagimsiz_{per}"]}, sinyal günü {rw[f"n_gun_{per}"]}, oran %{100 * rate:.1f} → kasada ~{n_k:.0f} olay; '
              f'gün-portföyü sd {sdv:.0f} bps; MDE(%80; α=0,05) {2.486 * sdv / np.sqrt(max(n_k, 1)):.0f} bps; MDE(Holm-10 en kötü α=0,005) {3.418 * sdv / np.sqrt(max(n_k, 1)):.0f} bps')
        for etki in (rw['ort_fazla_IS_bps'], rw['ort_fazla_OOS1_bps']):
            print(f'      gerçek etki {etki:.0f} bps ise kasada güç: α=0,05 → %{100 * guc(etki, sdv, n_k, 1.645):.0f}; α=0,005 → %{100 * guc(etki, sdv, n_k, 2.576):.0f}')
if OOS_CSV and os.path.exists(OOS_CSV):
    o = pd.read_csv(OOS_CSV)
    o = o[o.karar_satiri == True] if 'karar_satiri' in o.columns else o  # noqa: E712
    lo = o[(o.yon == 'long')]
    print('  OOS-1 karar satırları (AL):', len(lo), '; IS>0:', int((lo.ort_fazla_IS_bps > 0).sum()), '; OOS1 t ort', round(lo.t_OOS1.mean(), 2), 'sd', round(lo.t_OOS1.std(), 2),
          'en büyük', round(lo.t_OOS1.max(), 2), '; ikinci', round(lo.t_OOS1.nlargest(2).iloc[-1], 2))
    print('  p=0,015 için 41 denemede en az bir:', round(1 - (1 - 0.015) ** 41, 3))
    ex = o[o.sinyal_tanimi.isin(['A6_V1_dbaz_uzl_z1_yuk_spotAL_h3', 'A3_big_z10_small_h3', 'A1_FL_th2.0_h1'])]
    print(ex[['sinyal_tanimi', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS', 'n_bagimsiz_OOS1', 'ort_fazla_OOS1_bps', 't_OOS1', 'net_temel_bps_IS', 'net_temel_bps_OOS1',
              'dol_mkt_OOS1_bps', 'dol_sec_OOS1_bps', 'dol_sec_OOS1_t', 'top10_haric_bps', 'yil_pozitif_orani', 'giris_kapanis1_bps', 'en_yogun_hisse', 'en_yogun_pay', 'yillar_bps']].round(2).to_string(index=False))
