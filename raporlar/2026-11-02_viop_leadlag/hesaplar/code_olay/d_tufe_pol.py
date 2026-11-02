"""TÜFE (10:00 TSİ, açılışla eşzamanlı) ve siyasi şoklar."""
from olib import *
cc, gp, it = comp('cc'), comp('gap'), comp('intra'); f15 = fwd_cc(cc, 1, 5)
# ---------- TÜFE
tu = pd.DatetimeIndex(EV[EV.type == 'TUFE'].react_date)
ar_i = abs_ratio(tu, 'intra'); ar_g = abs_ratio(tu, 'gap')
print('TÜFE |intra| oranı XU100', round(ar_i['XU100'],2), 'XBANK', round(ar_i['XBANK'],2), '| |gap| XU100', round(ar_g['XU100'],2))
# banka - XU100 aşırı |gün-içi|
ex = (it['XBANK'] - it['XU100']).abs(); m = it.index.isin(tu)
print('|XBANK-XU100| intra TÜFE/diğer', round(ex[m].mean()/ex[~m].mean(),2))
pd.DataFrame({'abs_intra_ratio': ar_i, 'abs_gap_ratio': ar_g}).to_csv('res_tufe_absratio.csv')
print('TÜFE |intra| en yüksek oran:', ar_i.tail(6).round(2).to_dict(), 'en düşük:', ar_i.head(3).round(2).to_dict())
# saatlik: ilk bar (06:30 UTC barı; açılış ~06:55-07:00 UTC, TÜFE 07:00 UTC) -> sonrası
rows = []
for sym in ['XBANK.IS', 'XU030.IS']:
    h = ll.intraday(sym); dclose = ll.daily(sym, 'c', on_bist_cal=False)
    for d, g in h.groupby(h.index.tz_convert(None).normalize()):
        t = g.index.strftime('%H:%M')
        if '06:30' not in t or '07:30' not in t or d not in dclose.index: continue
        o = g['o'][t == '06:30'].iloc[0]; c1 = g['c'][t == '06:30'].iloc[0]
        rows.append(dict(sym=sym, date=d, tufe=d in tu, first=np.log(c1/o), rest=np.log(dclose[d]/c1)))
H = pd.DataFrame(rows)
for sym in ['XBANK.IS', 'XU030.IS']:
    for lab in [True, False]:
        S = H[(H.sym == sym) & (H.tufe == lab)].dropna()
        v = np.sign(S['first']) * S['rest']
        print(sym, 'TÜFE' if lab else 'diğer', 'n', len(S), '|ilk bar| bps', round(1e4*S['first'].abs().mean(),1), 'corr(ilk,kalan)', round(S[['first','rest']].corr().iloc[0,1],3), 'devam bps', round(1e4*v.mean(),1), 't', round(tstat(v)[0],2))
H.to_csv('res_tufe_h1.csv', index=False)
# ---------- Siyasi şoklar
pol = EV[EV.type == 'POLITICAL'].copy()
rows = []
for _, e in pol.iterrows():
    d = e.react_date
    if d not in cc.index: continue
    r = dict(date=e.date.date(), react=d.date(), sub=e['sub'], dir=e.dir, note=e.note)
    for c in ['XU100', 'XBANK']:
        r[f'{c}_gap'] = gp.at[d, c]; r[f'{c}_intra'] = it.at[d, c]; r[f'{c}_cc'] = cc.at[d, c]; r[f'{c}_f1_5'] = f15.at[d, c]
    rows.append(r)
P = pd.DataFrame(rows); P.to_csv('res_political_events.csv', index=False)
print(P[['react','sub','dir','XU100_gap','XU100_intra','XU100_cc','XU100_f1_5','XBANK_cc']].round(3).to_string(index=False))
neg = P[P.dir == -1]
for c in ['XU100_gap','XU100_intra','XU100_f1_5','XBANK_cc','XBANK_f1_5']:
    t, n = tstat(neg[c]); print('negatif şoklar', c, round(1e4*neg[c].mean(),1), 'bps t', round(t,2), 'n', n)
# kesit: negatif şoklarda hisse aşırı cc (react günü) -> 'siyasi şok betası'
nd = [pd.Timestamp(x) for x in neg.react]
xs = xsec(nd, None, 'cc'); xs.to_csv('res_political_xsec_neg.csv')
# ayrıca beta: hisse cc ~ XU100 cc yalnız şok günlerinde
b = {}
for s in VIOP:
    dd = pd.concat([cc.loc[nd, "XU100"], cc.loc[nd, s]], axis=1).dropna()
    b[s] = np.polyfit(dd.iloc[:, 0], dd.iloc[:, 1], 1)[0] if len(dd) > 5 else np.nan
xs['shock_beta'] = pd.Series(b); xs.to_csv('res_political_xsec_neg.csv')
print('negatif şokta en kötü (aşırı bps):', xs.head(6)['mean_bps'].round(0).to_dict()); print('en dayanıklı:', xs.tail(6)['mean_bps'].round(0).to_dict())
print('şok betası en yüksek:', xs['shock_beta'].sort_values().tail(5).round(2).to_dict(), 'en düşük:', xs['shock_beta'].sort_values().head(5).round(2).to_dict())
