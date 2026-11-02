"""(1) Açılış ayrışması sinyalinin ayrıştırılması: holding intra_t ~ NAVgap_t + holding_gap_t (kendi gap dönüşü mü, yakalama mı?)
(2) Saatlik (h1, 2023-11+) ve 5 dakikalık (m5, son ~60g) holding <-> iştirak sepeti lead-lag.
Çıktı: res_intraday.csv"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hc, ll, numpy as np, pandas as pd
import statsmodels.api as sm

SUBS = {'KCHOL': {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04},
        'SAHOL': {'AKBNK': .45, 'ENJSA': .10, 'CIMSA': .03}}
NAV = pd.read_parquet(os.path.join(hc.CODE, 'nav_series.parquet'))
rows = []
M = ll.decomp('XU100')
for h in ['KCHOL', 'SAHOL']:
    H = ll.decomp(h)
    ng = NAV[(f'{h}_fixed', 'gap')]
    df = pd.concat([H['intra'].rename('y'), ng.rename('navgap'), H['gap'].rename('hgap'), M['gap'].rename('mgap')], axis=1).dropna()
    for lab, d in [('ALL', df), ('IS', df[df.index < hc.SPLIT]), ('OOS', df[df.index >= hc.SPLIT])]:
        for spec in [['navgap', 'hgap'], ['navgap', 'hgap', 'mgap']]:
            m = sm.OLS(d['y'], sm.add_constant(d[spec])).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
            o = {'holding': h, 'test': 'intra~' + '+'.join(spec), 'sample': lab, 'n': len(d)}
            for c in spec: o[f'b_{c}'] = m.params[c]; o[f't_{c}'] = m.tvalues[c]
            rows.append(o)
    # iştiraklerin kendi gap dönüşü (karşılaştırma): sub intra ~ sub gap
    for s in list(SUBS[h]) + [h, 'XU100']:
        D = ll.decomp(s); b, t, n = ll.nw_t(D['intra'], D['gap'])
        rows.append({'holding': h, 'test': f'{s}: intra~own gap', 'sample': 'ALL', 'n': n, 'b_hgap': b, 't_hgap': t})

def hourly(sym, kind='h1'):
    d = ll.raw(ll.T(sym), kind).copy()
    d = d[d['c'] > 0]
    d['day'] = d.index.tz_convert(None).normalize()
    r = np.log(d['c']).groupby(d['day']).diff()  # gün içi bar getirileri (açılış barı hariç: ilk barın getirisi NaN)
    return r

for kind, lags in [('h1', [1, 2]), ('m5', [1, 2, 3, 6])]:
    for h, subs in SUBS.items():
        try:
            R = pd.DataFrame({s: hourly(s, kind) for s in [h] + list(subs) + ['XU100']})
        except Exception as e:
            print('skip', kind, h, e); continue
        w = pd.Series(subs); R['NAV'] = (R[list(subs)].fillna(0) * w).sum(axis=1) / w.sum()
        R = R.dropna(subset=[h, 'NAV'])
        day = R.index.tz_convert(None).normalize()
        for L in lags:
            sh = R.groupby(day).shift(L)  # aynı gün içinde gecikme
            for tgt, sig in [(h, 'NAV'), ('NAV', h)] + [(h, s) for s in subs]:
                y = R[tgt]; x = sh[sig]; c_own = sh[tgt]; c_m = sh['XU100']
                pc, t, n = hc.pcorr_t(y, x, [c_own, c_m])
                c, t0, _ = hc.corr_t(y, x)
                rows.append({'holding': h, 'test': f'{kind} {sig}_(h-{L}) -> {tgt}_h', 'sample': f'{R.index.min().date()}..{R.index.max().date()}', 'n': n, 'corr': c, 't_corr': t0, 'pcorr_ctrl_own_mkt': pc, 't_pc': t})
out = pd.DataFrame(rows); out.to_csv(os.path.join(hc.CODE, 'res_intraday.csv'), index=False)
pd.set_option('display.width', 250)
print(out.round(3).to_string())
