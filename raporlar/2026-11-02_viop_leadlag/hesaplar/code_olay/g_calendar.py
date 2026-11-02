"""Kısa: VİOP vade sonu (ayın son iş günü) / MSCI (Şub-May-Ağu-Kas son iş günü) kapanış seansı, bayram kapanışları, Perşembe 14:30 TSİ (yabancı akış verisi) barı."""
from olib import *
cc, gp, it = comp('cc'), comp('gap'), comp('intra'); cal = cc.index
# kapanış seansı getirisi = günlük kapanış / 14:30 barının kapanışı (15:00 UTC, sürekli işlem sonu)
out = {}
for sym in ['XU030.IS', 'XBANK.IS']:
    p15 = ll.snap_daily(sym, '15:00'); dc = ll.daily(sym, 'c', on_bist_cal=False)
    auc = np.log(dc / p15.reindex(dc.index)).dropna()
    me = pd.Series(auc.index, index=auc.index).groupby([auc.index.year, auc.index.month]).transform('max') == auc.index
    msci = me & auc.index.month.isin([2, 5, 8, 11])
    out[sym] = dict(abs_auc_monthend=1e4*auc[me].abs().mean(), abs_auc_msci=1e4*auc[msci].abs().mean(), abs_auc_other=1e4*auc[~me].abs().mean(), n_me=int(me.sum()), mean_auc_me=1e4*auc[me].mean(), t_me=tstat(auc[me])[0])
print(pd.DataFrame(out).round(2).to_string())
# bayram/uzun kapanış: ardışık BIST günleri arasında >=4 takvim günü (normal hafta sonu 3)
gaps = pd.Series(cal[1:] - cal[:-1], index=cal[1:]).dt.days
long_ = gaps[gaps >= 4].index; es = ll.daily('ES=F', on_bist_cal=False)
rows = []
for d in long_:
    prev = cal[cal < d][-1]
    try: esr = np.log(es[es.index < d].iloc[-1] / es[es.index <= prev].iloc[-1])
    except IndexError: continue
    rows.append(dict(react=d, days=gaps[d], es_closure=esr, gap=gp.at[d, 'XU100'], intra=it.at[d, 'XU100'], pre=cc.at[prev, 'XU100'], f1_3=fwd_cc(cc, 1, 3).at[d, 'XU100']))
B = pd.DataFrame(rows).dropna(); B.to_csv('res_bayram.csv', index=False)
print('uzun kapanış n', len(B), 'corr(ES kapanış süresince, XU100 gap)', round(B[['es_closure','gap']].corr().iloc[0,1],2), 'corr(ES, intra)', round(B[['es_closure','intra']].corr().iloc[0,1],2),
      'ort gap bps', round(1e4*B.gap.mean(),1), 't', round(tstat(B.gap)[0],2), '| kapanış öncesi gün bps', round(1e4*B.pre.mean(),1), 't', round(tstat(B.pre)[0],2), '| t+1..3', round(1e4*B.f1_3.mean(),1), round(tstat(B.f1_3)[0],2))
# normal günlerde gap baz
print('normal gün ort gap bps', round(1e4*gp['XU100'][~gp.index.isin(long_)].mean(),1))
# Perşembe 11:30 UTC barı (TCMB haftalık menkul kıymet 14:30 TSİ) |getiri| Perşembe vs diğer günler
h = ll.intraday('XBANK.IS'); b = h[h.index.strftime('%H:%M') == '11:30']; r = np.log(b['c'] / b['o'])
thu = r.index.dayofweek == 3
print('XBANK 11:30 barı |r| bps Perşembe', round(1e4*r[thu].abs().mean(),1), 'diğer', round(1e4*r[~thu].abs().mean(),1), 'n', int(thu.sum()))
