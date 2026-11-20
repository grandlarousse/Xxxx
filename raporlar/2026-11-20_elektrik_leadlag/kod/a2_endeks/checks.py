"""checks.py — aday kurallar için ek denetimler (yalnız IS): yer değiştirme sıfır dağılımı, aile içi en-büyük istatistik,
sinyal örtüşmesi, keşif amaçlı (ızgara dışı) satırlar. Kullanım: python3 -I checks.py <panel_is> <çıktı klasörü>"""
import os, sys, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a2lib
from a2lib import elib
import statsmodels.api as sm
warnings.filterwarnings('ignore')
PANEL, OUT = sys.argv[1], sys.argv[2]
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.IS_END
C = a2lib.context(P); sc = C['sc']
pd.set_option('display.width', 250)

# 1) yer değiştirme (dairesel kaydırma) — adaylar
cands = [('XELKT', 1.0, 'all', 3), ('XELKT', 1.0, 'lag', 3), ('KOMSU', 1.5, 'all', 2), ('SPEC', 2.0, 'all', 3),
         ('XU100', 1.0, 'all', 3), ('KOMSU', 2.0, 'AKSEN', 1), ('KOMSU', 1.5, 'ENJSA', 2)]
print('== yer değiştirme testi (n=500, tek yönlü)')
for inp, thr, hed, h in cands:
    s = a2lib.make_sig(C, inp, thr, hed)
    real, pv, null = elib.shift_null(s, P, h=h, n=500)
    print(f'{inp} z>={thr} {hed} h{h}: gerçek {real:.1f} bps, p={pv:.4f}, sıfır ort {np.nanmean(null):.1f} std {np.nanstd(null):.1f}')

# 2) aile içi en-büyük istatistik: T2a + T2b, pozitif eşik (long, AL yönü) 7 girdi × 3 eşik × 3 h × 2 hedef = 126 kural; aynı kaydırmalar
print('== aile içi en-büyük standart istatistik (T2a+T2b pozitif eşik; 126 kural, 200 ortak kaydırma)')
Z = {}
for inp in a2lib.INPUTS:
    for thr in [1.0, 1.5, 2.0]:
        for hed in ['all', 'lag']:
            s = a2lib.make_sig(C, inp, thr, hed)
            for h in [1, 2, 3]:
                real, pv, null = elib.shift_null(s, P, h=h, n=200, seed=1)
                mu, sd = np.nanmean(null), np.nanstd(null)
                Z[(inp, thr, hed, h)] = ((real - mu) / sd, (null - mu) / sd)
zr = pd.Series({k: v[0] for k, v in Z.items()}).sort_values(ascending=False)
mx = np.nanmax(np.vstack([v[1] for v in Z.values()]), axis=0)
print(zr.head(8).round(2).to_string())
print('sıfır altında max-z dağılımı: medyan %.2f, %%90 %.2f, %%95 %.2f' % (np.median(mx), np.quantile(mx, .9), np.quantile(mx, .95)))
for k in zr.index[:5]:
    print(k, 'aile düzeltmeli p = %.3f' % ((np.sum(mx >= zr[k]) + 1) / (len(mx) + 1)))

# 3) sinyal günlerinin örtüşmesi ve ayrıştırma (keşif)
def days(inp, thr):
    return a2lib.make_sig(C, inp, thr, 'all').any(axis=1)
dx, dk, ds, dm = days('XELKT', 1.0), days('KOMSU', 1.5), days('SPEC', 2.0), days('XU100', 1.0)
print('== örtüşme: KOMSU>=1.5 günlerinin XELKT>=1 payı %.2f | SPEC>=2: %.2f | XU100>=1: %.2f | XELKT>=1 günlerinin XU100>=1 payı %.2f'
      % ((dk & dx).sum() / dk.sum(), (ds & dx).sum() / ds.sum(), (dm & dx).sum() / dm.sum(), (dx & dm).sum() / dx.sum()))
rows = []
def ev(sig, ad, h, side='long', arac='spot'):
    r = elib.evaluate(sig, P, h=h, side=side, name=ad, family='A2', measure='own', instrument=arac, extra={'blok': 'KESIF'})
    s2 = sig.copy()
    if arac == 'viop':
        for c in s2.columns:
            s2.loc[s2.index < pd.Timestamp(elib.VIOP_START[c]), c] = False
    r.update(a2lib.halves(s2, P, h, side)); rows.append(r)
k15 = a2lib.make_sig(C, 'KOMSU', 1.5, 'all'); x1 = a2lib.make_sig(C, 'XELKT', 1.0, 'all'); m1 = a2lib.make_sig(C, 'XU100', 1.0, 'all')
ev(k15 & ~x1, 'KESIF|KOMSU z>=1.5 & XELKT z<1|all|h2', 2)
ev(k15 & x1, 'KESIF|KOMSU z>=1.5 & XELKT z>=1|all|h2', 2)
ev(x1 & ~k15, 'KESIF|XELKT z>=1 & KOMSU z<1.5|all|h3', 3)
ev(x1 & ~m1, 'KESIF|XELKT z>=1 & XU100 z<1|all|h3', 3)
ev(m1 & ~x1, 'KESIF|XU100 z>=1 & XELKT z<1|all|h3', 3)
# 4) keşif: sektör sert düştü, VİOP'lu hisse düşmedi (geciken) → vadeli SAT
for inp in ['XELKT', 'EWx']:
    for thr in [-1.0, -1.5, -2.0]:
        s = a2lib.make_sig(C, inp, thr, 'lag')[elib.VIOP]
        for h in [1, 2]:
            ev(s, f'KESIF|{inp} z<={thr:g}|lag∩VIOP3|h{h}|short|viop', h, 'short', 'viop')
            ev(s, f'KESIF|{inp} z<={thr:g}|lag∩VIOP3|h{h}|short|spot-tam-gecmis(bilgi)', h, 'short', 'spot')
d = elib.to_csv(rows, os.path.join(OUT, 'kesif_raw.csv'))
K = ['sinyal_tanimi', 'n_gun_IS', 'n_islem_IS', 'ort_fazla_IS_bps', 't_IS', 'net_temel_bps_IS', 'y1_bps', 'y1_n', 'y2_bps', 'top10_haric_bps', 'giris_kapanis1_bps', 'en_yogun_pay', 'yillar_bps']
print(d[K].round(1).to_string(index=False))

# 5) gecikenler akranlarını geçiyor mu? (sec ölçüsü, bilgi) ve XU030'un XU100 kontrolsüz havuz katsayısı
sr = pd.read_csv(os.path.join(OUT, 'scan_raw.csv'))
x = sr[(sr.blok == 'T2b') & (sr.esik_z > 0)]
print('== T2b (gecikenler, yukarı) sec ölçüsü: ort %.1f bps; pozitif pay %.2f; t>2: %d, t<-2: %d (n=%d)' % (
    x.dol_sec_IS_bps.mean(), (x.dol_sec_IS_bps > 0).mean(), (x.dol_sec_IS_t > 2).sum(), (x.dol_sec_IS_t < -2).sum(), len(x)))
x = sr[(sr.blok == 'T2b') & (sr.esik_z < 0)]
print('== T2b (gecikenler, aşağı) sec ölçüsü: ort %.1f bps; pozitif pay %.2f; t>2: %d, t<-2: %d (n=%d)' % (
    x.dol_sec_IS_bps.mean(), (x.dol_sec_IS_bps > 0).mean(), (x.dol_sec_IS_t > 2).sum(), (x.dol_sec_IS_t < -2).sum(), len(x)))
R = P['ret_cc'][sc]
reg = []
for h in [1, 2, 3]:
    f, fl, _ = elib.fwd_exec(P, h, 'long', sc)
    for inp in ['XU030', 'XU100']:
        parts = []
        for c in sc:
            parts.append(pd.DataFrame({'y': f[c], 'g': C['raw'][inp][c], 'r': R[c], 't': np.arange(len(R))})[fl[c]].dropna())
        dd = pd.concat(parts).sort_values('t')
        m = sm.OLS(dd['y'], sm.add_constant(dd[['g', 'r']])).fit(cov_type='hac-groupsum', cov_kwds={'time': dd['t'].values, 'maxlags': h})
        reg.append({'test': 'T1_havuz_XU100kontrolsuz', 'girdi': inp, 'h': h, 'katsayi': m.params['g'], 't': m.tvalues['g'], 'n': len(dd)})
        for lab, mk in [('liq10', C['liq_rank'] <= 10), ('sig', C['liq_rank'] > 10)]:
            parts = [pd.DataFrame({'y': f[c], 'g': C['raw'][inp][c], 'r': R[c], 't': np.arange(len(R))})[fl[c] & mk[c]].dropna() for c in sc]
            dd = pd.concat(parts).sort_values('t')
            m = sm.OLS(dd['y'], sm.add_constant(dd[['g', 'r']])).fit(cov_type='hac-groupsum', cov_kwds={'time': dd['t'].values, 'maxlags': h})
            reg.append({'test': 'T1_havuz_XU100kontrolsuz_' + lab, 'girdi': inp, 'h': h, 'katsayi': m.params['g'], 't': m.tvalues['g'], 'n': len(dd)})
rg = pd.DataFrame(reg); rg.to_csv(os.path.join(OUT, 'regresyon_ek.csv'), index=False)
print(rg.round(3).to_string(index=False))
