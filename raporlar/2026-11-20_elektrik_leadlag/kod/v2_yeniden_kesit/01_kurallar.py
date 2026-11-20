"""V2: T2, K1, K2'nin ham veriden bagimsiz yeniden uretimi + ek sorular (a), (b), (c).
Kullanim: python3 -I 01_kurallar.py <RAW_D1> <EK_DIR> <WORK_DIR>"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

RAW, EK, WORK = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(WORK, exist_ok=True)
P = L.build(RAW)
pd.to_pickle(P, os.path.join(WORK, 'v2_panel.pkl'))
print('panel:', P['ret'].shape, P['ret'].index.min().date(), P['ret'].index.max().date(),
      '| tavan kap.', int(P['lu'].sum().sum()), 'taban kap.', int(P['ld'].sum().sum()), 'tradable hisse-gun', int(P['tr'].sum().sum()))

fill = P['fill']
f_sh = L.fwd(P, 1, shift=True, cap=5)          # ortak sozlesme: en cok +5 gun kaydirma
f_inf = L.fwd(P, 1, shift=True, cap=None)      # yontem metni: ilk kilitsiz kapanis (sinirsiz)
f_no = L.fwd(P, 1, shift=False)                # kaydirma yok
E = {
    'ortak': L.sec_excess(f_sh, fill),
    'kaydirma_sinirsiz': L.sec_excess(f_inf, fill),
    'kaydirma_yok': L.sec_excess(f_no, fill),
    'kiyas_tabansiz': L.sec_excess(f_sh, fill & ~P['ld']),
    'kiyas_medyan': L.sec_excess(f_sh, fill, kind='median'),
    'kaydirma_yok_kiyas_tabansiz': L.sec_excess(f_no, fill & ~P['ld']),
    'kiyas_bayraksiz': L.sec_excess(f_sh, fill & ~((P['tu'] & ~P['lu']) | (P['td'] & ~P['ld']) | P['ld'])),   # T2'nin kendi suzgeci
}
sig = {'T2': L.rule_T2(P), 'K1': L.rule_K1(P), 'K2': L.rule_K2(P)}
sig['K2_tabansiz'] = sig['K2'] & ~P['ld']
pd.to_pickle({k: v for k, v in sig.items()}, os.path.join(WORK, 'v2_sig.pkl'))

rows = []
for rn, s in sig.items():
    sf = s & fill
    for vn, Ex in E.items():
        for pn, (a, b) in L.PERIODS.items():
            st = L.stats(Ex, sf, a, b)
            rows.append(dict(kural=rn, surum=vn, donem=pn, **st))
res = pd.DataFrame(rows)
res.to_csv(os.path.join(WORK, 'v2_tum_surumler.csv'), index=False)

# ---------------------------------------------------------------- ana ajanin rakamlari
ADLAR = {'T2': ('w3b_damitma', 'W3B_sade_sakin_guclu_h1'), 'K1': ('a3_kesit', 'A3_rel1_alt5_h1_RED'),
         'K2': ('w3a_kacinma', 'W3A_sektorden_5puan_geride_KACIN_h1')}
kasa = pd.read_csv(os.path.join(EK, 'kasa_sonuc.csv'))
tum = pd.read_csv(os.path.join(EK, 'tum_oos_sonuc.csv'))
o1 = pd.read_csv(os.path.join(EK, 'oos1_sonuc_donem_notr.csv'))


def pick(df, ajan, ad):
    r = df[(df['aile'] == ajan) & (df['sinyal_tanimi'] == ad)]
    return r.iloc[0] if len(r) else None


def ana(rn, donem):
    ajan, ad = ADLAR[rn]
    src = [(kasa, {'IS': 'IS', 'OOS1': 'OOS1', 'KASA': 'KASA'}, 'kasa_sonuc.csv'),
           (tum, {'IS': 'IS', 'HAVUZ2023': 'OOS'}, 'tum_oos_sonuc.csv'),
           (o1, {'IS': 'IS', 'OOS1': 'OOS1'}, 'oos1_sonuc_donem_notr.csv')]
    for df, mp, nm in src:
        r = pick(df, ajan, ad)
        if r is not None and donem in mp:
            k = mp[donem]
            return dict(ana_kaynak=nm, ana_n_gun=r[f'n_gun_{k}'], ana_n_islem=r[f'n_islem_{k}'], ana_ort_bps=r[f'ort_fazla_{k}_bps'],
                        ana_t=r[f't_{k}'], ana_isabet=r[f'isabet_{k}'], ana_ort_islem_bps=r[f'basabas_{k}_bps'])
    return dict(ana_kaynak='yok', ana_n_gun=np.nan, ana_n_islem=np.nan, ana_ort_bps=np.nan, ana_t=np.nan, ana_isabet=np.nan,
                ana_ort_islem_bps=np.nan)


out = []
for rn in ('T2', 'K1', 'K2'):
    for pn in L.PERIODS:
        v = res[(res.kural == rn) & (res.surum == 'ortak') & (res.donem == pn)].iloc[0].to_dict()
        a = ana(rn, pn)
        d = dict(kural=rn, ad=ADLAR[rn][1], donem=pn, v2_n_gun=v['n_gun'], v2_n_islem=v['n_islem'], v2_ort_bps=round(v['ort_bps'], 2),
                 v2_t=round(v['t'], 2), v2_medyan_gun_bps=round(v['medyan_gun_bps'], 2), v2_medyan_islem_bps=round(v['medyan_islem_bps'], 2),
                 v2_isabet_islem=round(v['isabet_islem'], 4), v2_isabet_gun=round(v['isabet_gun'], 4), **a)
        d['fark_bps'] = round(d['v2_ort_bps'] - d['ana_ort_bps'], 2) if d['ana_ort_bps'] == d['ana_ort_bps'] else np.nan
        d['fark_n_islem'] = d['v2_n_islem'] - d['ana_n_islem'] if d['ana_n_islem'] == d['ana_n_islem'] else np.nan
        d['isaret_ayni'] = (np.sign(d['v2_ort_bps']) == np.sign(d['ana_ort_bps'])) if d['ana_ort_bps'] == d['ana_ort_bps'] else ''
        for vn in ('kaydirma_sinirsiz', 'kaydirma_yok', 'kiyas_tabansiz', 'kiyas_bayraksiz', 'kiyas_medyan', 'kaydirma_yok_kiyas_tabansiz'):
            w = res[(res.kural == rn) & (res.surum == vn) & (res.donem == pn)].iloc[0]
            d[f'{vn}_bps'] = round(w['ort_bps'], 2)
            d[f'{vn}_t'] = round(w['t'], 2)
        w = res[(res.kural == rn + '_tabansiz') & (res.surum == 'ortak') & (res.donem == pn)] if rn == 'K2' else []
        d['sinyal_tabansiz_bps'] = round(w.iloc[0]['ort_bps'], 2) if len(w) else np.nan
        d['sinyal_tabansiz_t'] = round(w.iloc[0]['t'], 2) if len(w) else np.nan
        d['sinyal_tabansiz_n_islem'] = w.iloc[0]['n_islem'] if len(w) else np.nan
        out.append(d)
out = pd.DataFrame(out)
out.to_csv(os.path.join(EK, 'v2_yeniden_kesit.csv'), index=False)
pd.set_option('display.width', 250)
print(out[['kural', 'donem', 'v2_n_gun', 'ana_n_gun', 'v2_n_islem', 'ana_n_islem', 'v2_ort_bps', 'ana_ort_bps', 'fark_bps', 'v2_t', 'ana_t',
           'v2_medyan_islem_bps', 'v2_isabet_islem', 'ana_isabet']].to_string(index=False))
print(out[['kural', 'donem', 'kaydirma_sinirsiz_bps', 'kaydirma_sinirsiz_t', 'kaydirma_yok_bps', 'kaydirma_yok_t', 'kiyas_tabansiz_bps',
           'kiyas_tabansiz_t', 'kiyas_bayraksiz_bps', 'kiyas_bayraksiz_t', 'kaydirma_yok_kiyas_tabansiz_bps', 'kiyas_medyan_bps', 'kiyas_medyan_t', 'sinyal_tabansiz_bps', 'sinyal_tabansiz_t', 'sinyal_tabansiz_n_islem']].to_string(index=False))

# ---------------------------------------------------------------- (c) T2: secilen ve secilmeyen dolabilir hisselerin HAM ertesi gun getirisi
print('\n(c) T2 ham ertesi gun getirisi (gunluk EW ortalama -> gunler arasi ortalama, bps); yalniz sinyal olan gunler')
s = sig['T2'] & fill
crow = []
for fn, f in (('kaydirmali(+5)', f_sh), ('kaydirmasiz', f_no)):
    for pn in ('OOS1', 'KASA', 'IS'):
        a, b = L.PERIODS[pn]
        sel = f.where(s).mean(axis=1)
        oth = f.where(fill & ~s).mean(axis=1)
        allf = f.where(fill).mean(axis=1)
        m = sel.notna() & oth.notna()
        if a is not None:
            m &= sel.index >= a
        if b is not None:
            m &= sel.index <= b
        d = (sel - oth)[m]
        per = allf[(allf.index >= (a or allf.index[0])) & (allf.index <= (b or allf.index[-1]))].dropna()
        crow.append(dict(getiri=fn, donem=pn, n_gun=int(m.sum()), secilen_ham_bps=round(1e4 * sel[m].mean(), 1),
                         secilmeyen_ham_bps=round(1e4 * oth[m].mean(), 1), fark_bps=round(1e4 * d.mean(), 1),
                         fark_t=round(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))), 2),
                         secilen_medyan_gun_bps=round(1e4 * sel[m].median(), 1), secilmeyen_medyan_gun_bps=round(1e4 * oth[m].median(), 1),
                         donem_tum_dolabilir_ham_bps=round(1e4 * per.mean(), 1)))
crow = pd.DataFrame(crow)
crow.to_csv(os.path.join(EK, 'v2_yeniden_kesit_T2_ham.csv'), index=False)
print(crow.to_string(index=False))

# ---------------------------------------------------------------- kiyasta kilit: kasada art arda taban serileri
ld = P['ld']
run = ld.astype(int)
for c in ld.columns:
    v = ld[c].values
    r = np.zeros(len(v), int)
    for i in range(len(v)):
        r[i] = (r[i - 1] + 1 if i else 1) if v[i] else 0
    run[c] = r
mx = run[run.index >= L.KASA_START].max().sort_values(ascending=False).head(6)
print('\nkasada en uzun art arda taban kapanisi (gun):', mx.to_dict())
k = (f_sh.index >= L.KASA_START)
print('kasa: kiyas sepetinde tabanda kapanan (dolabilir) hisse-gun:', int((fill & ld)[k].sum().sum()),
      '| toplam dolabilir hisse-gun:', int(fill[k].sum().sum()))
bm = f_sh.where(fill).mean(axis=1)
bm2 = f_sh.where(fill & ~ld).mean(axis=1)
bm3 = f_no.where(fill).mean(axis=1)
bmed = f_sh.where(fill).median(axis=1)
for pn in ('IS', 'OOS1', 'KASA'):
    a, b = L.PERIODS[pn]
    m = (bm.index >= (a or bm.index[0])) & (bm.index <= (b or bm.index[-1]))
    print(f'{pn}: kiyas sepeti f1 ort (bps): ortak {1e4 * bm[m].mean():.1f} | tabansiz {1e4 * bm2[m].mean():.1f} | kaydirmasiz {1e4 * bm3[m].mean():.1f}'
          f' | medyan {1e4 * bmed[m].mean():.1f}')
