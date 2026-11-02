"""FOMC olay çalışması: karar 18/19 UTC (BIST kapanışı sonrası) -> BIST d+1 gap vs gün-içi vs t+2..5 sürüklenme."""
from olib import *
import json
ev = EV[(EV.type == 'FOMC') & (EV['sub'] == 'scheduled')]
D0 = pd.DatetimeIndex(ev['date']); R = pd.DatetimeIndex(ev['react_date'])
es = ll.ret('ES=F'); tnx = ll.daily('^TNX').diff()  # yüzde puan değişim
cc, gp, it = comp('cc'), comp('gap'), comp('intra')
res = {}
# sinyal: ES getirisi FOMC günü (US kapanışı, BIST kapanışından sonrasını içerir) -> BIST'in ertesi günü
sig = es.reindex(cc.index)  # BIST takvimi
s_lag = sig.shift(1)        # d+1 satırında d'nin ES getirisi
isF = cc.index.isin(R)
out = []
for tgt_name, T in [('gap', gp), ('intra', it), ('cc', cc), ('f2_5', fwd_cc(cc, 1, 4))]:
    for c in ['XU100', 'XBANK', 'XU030']:
        y = T[c]
        for lab, m in [('FOMC', isF), ('other', ~isF)]:
            df = pd.concat([y[m], s_lag[m]], axis=1).dropna()
            if len(df) < 20: continue
            b, t, n = ll.nw_t(df.iloc[:, 0], df.iloc[:, 1])
            out.append(dict(target=tgt_name, idx=c, sample=lab, corr=df.corr().iloc[0, 1], beta=b, t=t, n=n))
reg = pd.DataFrame(out); reg.to_csv('res_fomc_reg.csv', index=False)
print(reg[reg.idx == 'XU100'].round(3).to_string(index=False))
# |gap| oranı FOMC sonrası
ar = abs_ratio(R, 'gap'); ar_i = abs_ratio(R, 'intra')
print('|gap| oranı XU100', round(ar['XU100'], 2), 'XBANK', round(ar['XBANK'], 2), ' |intra| XU100', round(ar_i['XU100'], 2))
# Hisse bazında: FOMC sonrası gap'in ES'e betası (FOMC günleri) - normal günler
rows = []
for s in VIOP:
    for lab, m in [('F', isF), ('O', ~isF)]:
        df = pd.concat([gp[s][m], s_lag[m]], axis=1).dropna()
        b = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)[0] if len(df) > 20 else np.nan
        rows.append((s, lab, b, df.corr().iloc[0, 1] if len(df) > 20 else np.nan, len(df)))
xb = pd.DataFrame(rows, columns=['stock', 's', 'beta', 'corr', 'n']).pivot(index='stock', columns='s', values=['beta', 'corr'])
xb.columns = [f'{a}_{b}' for a, b in xb.columns]; xb['abs_gap_ratio'] = ar.reindex(xb.index); xb['abs_intra_ratio'] = ar_i.reindex(xb.index)
xb.sort_values('beta_F').to_csv('res_fomc_xsec.csv'); print(xb.sort_values('abs_gap_ratio').round(2).iloc[[0,1,2,-3,-2,-1]].to_string())
# Backtest: FOMC sonrası gün-içi -> sign(ES_d) ile XU030 gün-içi (açılışta gir, kapanışta çık) [işlenebilir]
for c in ['XU030', 'XBANK']:
    for cost in [8, 15]:
        sgn = s_lag.where(isF)  # sadece FOMC sonrası
        r_, _ = ll.backtest(sgn, it[c], cost_bps=cost, split='2021-01-01')
        res[f'bt_intra_{c}_{cost}'] = {k: {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()} if isinstance(v, dict) else v for k, v in r_.items()}
    # ters (reversal) yönü de raporlanır: sharpe işareti tersse reversal
# Ek: TNX (10y getiri değişimi, yp) FOMC günü -> BIST d+1
t_lag = tnx.reindex(cc.index).shift(1)
for c in ['XU100', 'XBANK']:
    for tgt_name, T in [('gap', gp), ('intra', it), ('f2_5', fwd_cc(cc, 1, 4))]:
        df = pd.concat([T[c][isF], t_lag[isF], s_lag[isF]], axis=1).dropna(); df.columns = ['y', 'tnx', 'es']
        import statsmodels.api as sm
        m = sm.OLS(df.y, sm.add_constant(df[['tnx', 'es']])).fit(cov_type='HC1')
        res[f'tnx_{c}_{tgt_name}'] = dict(b_tnx=round(m.params['tnx'], 4), t_tnx=round(m.tvalues['tnx'], 2), b_es=round(m.params['es'], 3), t_es=round(m.tvalues['es'], 2), n=int(m.nobs))
json.dump(res, open('res_fomc_bt.json', 'w'), indent=1, default=str)
for k, v in res.items():
    if k.startswith('bt'): print(k, {s: (v[s].get('mean_bps'), v[s].get('t'), v[s].get('sharpe'), v[s].get('n')) for s in ['IS', 'OOS', 'ALL']})
    else: print(k, v)
