"""TCMB PPK: karar 11:00 UTC (14:00 TSİ, seans İÇİ). Günlük: karar günü gün-içi; saatlik (2023-11+): 10:30->12:30 UTC tepki, 12:30->kapanış devam."""
from olib import *
ev = EV[EV.type == 'PPK'].copy()
cc, gp, it = comp('cc'), comp('gap'), comp('intra'); f15 = fwd_cc(cc, 1, 5)
ev = ev[ev.react_date >= '2014-01-02']
rows = []
for _, e in ev.iterrows():
    d = e.react_date
    if d not in cc.index: continue
    r = dict(date=d.date(), sub=e['sub'], dir=e.dir, surp=e.get('sub2', np.nan))
    for c in ['XU100', 'XBANK']:
        r[f'{c}_gap'] = gp.at[d, c]; r[f'{c}_intra'] = it.at[d, c]; r[f'{c}_cc'] = cc.at[d, c]; r[f'{c}_f1_5'] = f15.at[d, c]
    rows.append(r)
T = pd.DataFrame(rows); T.to_csv('res_ppk_events.csv', index=False)
bi = it['XBANK'].mean(); ui = it['XU100'].mean()
print('baz gün-içi ort bps XBANK', round(1e4*bi,1), 'XU100', round(1e4*ui,1))
for g, m in [('hike', T['sub'].isin(['hike','extra_hawk'])), ('cut', T['sub']=='cut'), ('hold', T['sub']=='hold'), ('surp_hawk', T.surp==1), ('surp_dove', T.surp==-1), ('surp_inline', T.surp==0)]:
    S = T[m]
    print(f'{g:12s} n={len(S):3d}', ' '.join(f"{c}={1e4*S[c].mean():7.1f}(t{tstat(S[c])[0]:5.2f})" for c in ['XBANK_intra','XU100_intra','XBANK_f1_5','XU100_f1_5']))
# Sürpriz yönlü işaretli: banka gün-içi * surp
S = T[T.surp.isin([1, -1])]; v = S.XBANK_intra * S.surp; print('XBANK intra * sürpriz', round(1e4*v.mean(),1), 'bps t', round(tstat(v)[0],2), 'n', len(v), 'hit', round((v>0).mean(),2))
v = S.XBANK_f1_5 * S.surp; print('XBANK t+1..5 * sürpriz', round(1e4*v.mean(),1), 'bps t', round(tstat(v)[0],2))
# kesit: sürpriz günlerinde (işaretli) hisse aşırı gün-içi
sign = dict(zip(pd.to_datetime(S.date), S.surp))
xs = xsec(list(sign.keys()), sign, 'intra'); xs.to_csv('res_ppk_surprise_xsec.csv')
print('en negatif/pozitif şahin-sürpriz aşırı gün-içi:', xs.round(0).head(4).index.tolist(), xs.round(0).tail(6)[['mean_bps']].T.to_dict('records'))
# ---- saatlik (2023-11+)
def h1c(sym):
    h = ll.intraday(sym); return h['c']
rows = []
for sym in ['XBANK.IS', 'XU100.IS', 'XU030.IS']:
    c = h1c(sym); idx = c.index
    for _, e in ev[ev.react_date >= '2023-11-30'].iterrows():
        d = e.react_date; day = c[idx.normalize().tz_convert(None) == d]
        if len(day) < 6: continue
        t = day.index.strftime('%H:%M')
        try:
            p_pre = day[t == '09:30'].iloc[0]; p_r = day[t == '11:30'].iloc[0]  # 09:30 barı 10:30'da kapanır; 11:30 barı 12:30'da kapanır
        except IndexError: continue
        dclose = ll.daily(sym, 'c', on_bist_cal=False).get(d, np.nan)
        op = day.iloc[0]
        rows.append(dict(sym=sym, date=d.date(), sub=e['sub'], surp=e.get('sub2', np.nan), pre=np.log(p_pre/ll.intraday(sym)['o'][day.index[0]]), react=np.log(p_r/p_pre), post=np.log(dclose/p_r)))
H = pd.DataFrame(rows); H.to_csv('res_ppk_h1.csv', index=False)
for sym in ['XBANK.IS', 'XU030.IS']:
    S = H[H.sym == sym].dropna(subset=['react', 'post'])
    cr = S[['react', 'post']].corr().iloc[0, 1]
    v = np.sign(S.react) * S.post
    print(sym, 'n', len(S), 'corr(tepki, sonrası)', round(cr, 2), 'devam stratejisi bps', round(1e4*v.mean(),1), 't', round(tstat(v)[0],2), '| sürpriz*tepki', round(1e4*(S.react*S.surp)[S.surp!=0].mean(),1), 'n', int((S.surp.abs()==1).sum()))
