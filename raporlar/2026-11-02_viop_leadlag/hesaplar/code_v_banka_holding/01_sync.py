# -*- coding: utf-8 -*-
"""Senkron iddialarin bagimsiz yeniden uretimi: B4, B5, B7, H1, H2, H3 (+ ortak faktor testleri, plasebolar)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vb

OUT = os.path.dirname(os.path.abspath(__file__)) + '/res'
os.makedirs(OUT, exist_ok=True)

_s = {}
def get(name):
    """Seri olusturucu. '_L1' soneki = 1 gun gecikme. Ozel sepetler asagida."""
    if name in _s: return _s[name]
    if name.endswith('_L1'):
        s = get(name[:-3]).shift(1)
    elif name == 'BANKS_exAKBNK':
        s = pd.concat([get(k) for k in ['GARAN.IS', 'YKBNK.IS', 'ISCTR.IS', 'HALKB.IS', 'VAKBN.IS']], axis=1).mean(axis=1, skipna=False)
    elif name == 'BANKS_exYKBNK':
        s = pd.concat([get(k) for k in ['GARAN.IS', 'AKBNK.IS', 'ISCTR.IS', 'HALKB.IS', 'VAKBN.IS']], axis=1).mean(axis=1, skipna=False)
    elif name.startswith('XU100ex:'):
        # XU100ex:SYM1,SYM2:w  -> (XU100 - w*sum)/(1-k*w)
        _, syms, w = name.split(':'); w = float(w); syms = syms.split(',')
        s = (get('XU100.IS') - w * sum(get(k) for k in syms)) / (1 - w * len(syms))
    elif name == 'XBANK_rel':
        s = get('XBANK.IS') - get('XU100.IS')
    else:
        s = vb.ret(name)
    _s[name] = s
    return s

def Z(names):
    if not names: return None
    return pd.concat([get(n).rename(n) for n in names], axis=1)

rows = []
def run(cid, y, x, ctrls, note='', periods=vb.PERIODS, do_year=True):
    yy, xx = get(y), get(x)
    for cname, cl in ctrls.items():
        zz = Z(cl)
        sm = vb.summarize(yy, xx, zz, periods)
        rec = dict(claim=cid, y=y, x=x, ctrl=cname, ctrl_list='+'.join(cl) if cl else '-', note=note)
        for p, d in sm.items():
            rec[f'{p}_n'] = d['n']; rec[f'{p}_corr'] = d['corr']; rec[f'{p}_pc'] = d['pc']; rec[f'{p}_t'] = d['t']; rec[f'{p}_beta'] = d['beta']
        if do_year:
            yr = vb.yearly(yy, xx, zz, 2010, 2026)
            ref_c = sm['full2010']['corr']; ref_p = sm['full2010']['pc']
            fc, ny = vb.same_sign_frac(yr, 'corr', ref_c)
            fp, _ = vb.same_sign_frac(yr, 'pc', ref_p)
            rec['yrs'] = ny; rec['yrs_same_corr'] = fc; rec['yrs_same_pc'] = fp
            if len(yr):
                rec['yr_pc'] = ' '.join(f"{int(a)}:{b:+.2f}" for a, b in zip(yr['year'], yr['pc']))
                rec['yr_corr'] = ' '.join(f"{int(a)}:{b:+.2f}" for a, b in zip(yr['year'], yr['corr']))
        rows.append(rec)
        f = sm
        print(f"{cid:4s} {y:>14s} ~ {x:<10s} | {cname:<10s} full10 c={f['full2010']['corr']:+.3f} pc={f['full2010']['pc']:+.3f} t={f['full2010']['t']:+.1f} n={f['full2010']['n']} | IS pc={f['IS14_20']['pc']:+.3f} | OOS pc={f['OOS21_26']['pc']:+.3f} | 3y pc={f['last3y']['pc']:+.3f} | 1y c={f['last1y']['corr']:+.3f} pc={f['last1y']['pc']:+.3f} t={f['last1y']['t']:+.1f}" + (f" | yrs={rec['yrs']} same_c={rec['yrs_same_corr']:.2f} same_pc={rec['yrs_same_pc']:.2f}" if do_year and rec['yrs'] else ''), flush=True)

X = ['XU100.IS']
BANKS = ['XBANK.IS', 'AKBNK.IS', 'GARAN.IS', 'YKBNK.IS', 'ISCTR.IS', 'HALKB.IS', 'VAKBN.IS', 'TSKB.IS']

# ---------------- B4: USDTRY -> banka ozgu negatif ----------------
print('\n=== B4 USDTRY ===')
for b in BANKS:
    run('B4', b, 'TRY=X', {
        'XU100': X,
        'X+EEM': X + ['EEM'],
        'X+EEM+ES': X + ['EEM', 'ES=F'],
        'X+EEM+ES+L1': X + ['EEM', 'ES=F', 'EEM_L1', 'ES=F_L1', 'XU100.IS_L1'],
    })
# yorum karsilastirmasi: sanayi/hizmet endeksleri ayni testte (banka-disi taraf pozitif mi?)
for s in ['XUSIN.IS', 'XU030.IS']:
    run('B4ctx', s, 'TRY=X', {'XU100': X, 'X+EEM': X + ['EEM']})
run('B4rel', 'XBANK_rel', 'TRY=X', {'none': [], 'EEM': ['EEM']})

# ---------------- B5: 2026 rejim kaymasi ----------------
print('\n=== B5 2026 ===')
P5 = {'y2021_24': ('2021-01-01', '2024-12-31'), 'y2025': ('2025-01-01', '2025-12-31'),
      'w2511_2610': ('2025-11-01', '2026-10-30'), 'h1_2511_2604': ('2025-11-01', '2026-04-30'),
      'h2_2605_2610': ('2026-05-01', '2026-10-30'), 'full2010': ('2010-01-01', '2026-12-31')}
b5rows = []
for b in ['XBANK.IS', 'AKBNK.IS', 'GARAN.IS', 'YKBNK.IS', 'ISCTR.IS', 'HALKB.IS', 'VAKBN.IS']:
    for d in ['BZ=F', 'SAN.MC', 'EMB', 'BBVA.MC']:
        for cname, cl in {'XU100': X, 'X+TRY+EEM': X + ['TRY=X', 'EEM'], 'X+TRY+EEM+ES': X + ['TRY=X', 'EEM', 'ES=F']}.items():
            sm = vb.summarize(get(b), get(d), Z(cl), P5)
            rec = dict(claim='B5', y=b, x=d, ctrl=cname)
            for p, v in sm.items():
                rec[f'{p}_n'] = v['n']; rec[f'{p}_pc'] = v['pc']; rec[f'{p}_t'] = v['t']; rec[f'{p}_corr'] = v['corr']
            b5rows.append(rec)
            if b == 'XBANK.IS' or cname == 'XU100':
                print(f"B5 {b:9s}~{d:8s} {cname:13s} 21-24 pc={sm['y2021_24']['pc']:+.3f} | 2025 pc={sm['y2025']['pc']:+.3f} | 2511-2610 c={sm['w2511_2610']['corr']:+.3f} pc={sm['w2511_2610']['pc']:+.3f} t={sm['w2511_2610']['t']:+.1f} n={sm['w2511_2610']['n']} | H1 pc={sm['h1_2511_2604']['pc']:+.3f} H2 pc={sm['h2_2605_2610']['pc']:+.3f}", flush=True)
pd.DataFrame(b5rows).to_csv(f'{OUT}/b5_windows.csv', index=False)

# B5 saglamlik: XBANK, pencere 2025-11..2026-10
a, bnd = '2025-11-01', '2026-10-30'
y = vb.per(get('XBANK.IS'), a, bnd)
print('\nB5 saglamlik (XBANK, 2025-11..2026-10, ctrl XU100):')
for d in ['BZ=F', 'SAN.MC', 'EMB', 'BBVA.MC']:
    x = vb.per(get(d), a, bnd); z = vb.per(Z(X), a, bnd)
    base = vb.pc(y, x, z)
    # en buyuk 10 |x| gunu cikar
    idx = x.abs().sort_values(ascending=False).index[:10]
    m = ~x.index.isin(idx)
    drop10 = vb.pc(y[m], x[m], z[m])
    # winsor %1
    def w(s): lo, hi = s.quantile([.01, .99]); return s.clip(lo, hi)
    wz = vb.pc(w(y), w(x), z.apply(w))
    # lag0+lag1 (eszamansiz kapanis)
    x01 = (get(d) + get(d).shift(1)); x01 = vb.per(x01, a, bnd)
    l01 = vb.pc(y, x01, z)
    xl1 = vb.per(get(d).shift(1), a, bnd)
    l1 = vb.pc(y, xl1, z)
    print(f"  {d:8s} base pc={base['pc']:+.3f} t={base['t']:+.1f} | drop top10 pc={drop10['pc']:+.3f} | winsor pc={wz['pc']:+.3f} | lag1 pc={l1['pc']:+.3f} | lag0+1 pc={l01['pc']:+.3f}")
# dort surucu tek regresyonda
df = pd.concat([y.rename('y')] + [vb.per(get(d), a, bnd).rename(d) for d in ['BZ=F', 'SAN.MC', 'EMB', 'BBVA.MC', 'XU100.IS', 'TRY=X', 'EEM']], axis=1).dropna()
b_, se_, e_ = vb.ols(df['y'].values, df.drop(columns='y').values)
print('  ortak regresyon (XBANK ~ BZ+SAN+EMB+BBVA+XU100+TRY+EEM):', ' '.join(f"{c}: b={bb:+.3f} t={bb/ss:+.1f}" for c, bb, ss in zip(df.columns[1:], b_, se_)), 'n=', len(df))
print('  surucu korelasyon matrisi (XU100 artiklari):')
R = df[['BZ=F', 'SAN.MC', 'EMB', 'BBVA.MC']]
Zx = np.column_stack([np.ones(len(df)), df['XU100.IS'].values])
Rres = R - Zx @ np.linalg.lstsq(Zx, R.values, rcond=None)[0]
print(Rres.corr().round(2).to_string())

# ---------------- B7: BBVA <-> GARAN ----------------
print('\n=== B7 BBVA-GARAN ===')
for d in ['BBVA.MC', 'BBVA']:
    run('B7', 'GARAN.IS', d, {
        'XU100': X, 'X+TRY+EEM': X + ['TRY=X', 'EEM'], 'X+TRY+EEM+XBANKex': X + ['TRY=X', 'EEM', 'BANKS_exAKBNK'],
    })
# GARAN'in XBANK disi bankalarla kiyas (BBVA ozel bag var mi? yerine plasebo: SAN.MC)
run('B7plc', 'GARAN.IS', 'SAN.MC', {'XU100': X})
run('B7plc', 'AKBNK.IS', 'BBVA.MC', {'XU100': X})
# ters yon: BBVA.MC ~ GARAN | SAN.MC (Avrupa bankasi faktoru)
run('B7rev', 'BBVA.MC', 'GARAN.IS', {'SAN': ['SAN.MC'], 'SAN+XU100': ['SAN.MC', 'XU100.IS'], 'SAN+EUFN+XU100': ['SAN.MC', 'EUFN', 'XU100.IS']})
run('B7rev', 'BBVA.MC', 'AKBNK.IS', {'SAN+XU100': ['SAN.MC', 'XU100.IS']})

# ---------------- H1: SAHOL-AKBNK ----------------
print('\n=== H1 SAHOL-AKBNK ===')
run('H1', 'SAHOL.IS', 'AKBNK.IS', {
    'XU100': X,
    'X+TRY+EEM': X + ['TRY=X', 'EEM'],
    'X+TRY+EEM+BNKex': X + ['TRY=X', 'EEM', 'BANKS_exAKBNK'],
    'X+TRY+EEM+XBANK': X + ['TRY=X', 'EEM', 'XBANK.IS'],
    'XU100ex5%': ['XU100ex:SAHOL.IS,AKBNK.IS:0.05'],
    'XU100ex8%': ['XU100ex:SAHOL.IS,AKBNK.IS:0.08'],
    'XU030': ['XU030.IS'],
})
for bk in ['GARAN.IS', 'YKBNK.IS', 'ISCTR.IS', 'HALKB.IS', 'VAKBN.IS', 'XBANK.IS']:
    run('H1plc', 'SAHOL.IS', bk, {'XU100': X, 'X+TRY+EEM+BNKex': X + ['TRY=X', 'EEM', 'BANKS_exAKBNK']} if bk not in ('XBANK.IS',) else {'XU100': X})
run('H1plc', 'KCHOL.IS', 'AKBNK.IS', {'XU100': X, 'X+TRY+EEM+BNKex': X + ['TRY=X', 'EEM', 'BANKS_exAKBNK']})

# ---------------- H2: KCHOL - istirakler ----------------
print('\n=== H2 KCHOL ===')
for sub in ['ARCLK.IS', 'FROTO.IS', 'YKBNK.IS', 'TOASO.IS', 'TUPRS.IS']:
    sect = ['BANKS_exYKBNK'] if sub == 'YKBNK.IS' else ['XUSIN.IS']
    run('H2', 'KCHOL.IS', sub, {
        'XU100': X,
        'X+TRY+EEM': X + ['TRY=X', 'EEM'],
        'X+TRY+EEM+SECT': X + ['TRY=X', 'EEM'] + sect,
        'X+TRY+EEM+SAHOL': X + ['TRY=X', 'EEM', 'SAHOL.IS'],
        'XU100ex5%': [f'XU100ex:KCHOL.IS,{sub}:0.05'],
        'XU030': ['XU030.IS'],
    })

# ---------------- H3: ENKAI - USDTRY ----------------
print('\n=== H3 ENKAI-USDTRY ===')
run('H3', 'ENKAI.IS', 'TRY=X', {
    'XU100': X, 'X+EEM': X + ['EEM'], 'X+EEM+ES': X + ['EEM', 'ES=F'],
    'X+EEM+ES+L1': X + ['EEM', 'ES=F', 'EEM_L1', 'ES=F_L1', 'XU100.IS_L1'],
    'X+EEM+XUSIN': X + ['EEM', 'XUSIN.IS'],
})
run('H3', 'ENKAI.IS', 'EURTRY=X', {'XU100': X})
pd.DataFrame(rows).to_csv(f'{OUT}/sync_results.csv', index=False)
print('kaydedildi', f'{OUT}/sync_results.csv')
