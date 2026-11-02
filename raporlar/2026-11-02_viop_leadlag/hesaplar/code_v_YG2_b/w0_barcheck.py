"""Kış h1 bar hizalaması kontrolü: kışın son bar gerçekten 13:30-14:30 mu, yoksa etiket kayması ile 14:00-15:00 mı?
Test: günlük h/l ile h1 bar h/l kapsama oranı, bar başına hacim payı ve |log(C/son bar c)| mevsime göre."""
import pandas as pd, numpy as np, sys
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
syms=['THYAO','GARAN','AKBNK','EREGL','BIMAS','ASELS','KCHOL','TUPRS','SISE','FROTO','PGSUS','TCELL']
rows=[]
for s in syms:
    h=pd.read_parquet(f'{D}/h1/{s}.IS.parquet'); h=h[~h.index.duplicated(keep='last')]
    d=pd.read_parquet(f'{D}/daily/{s}.IS.parquet'); d.index=pd.DatetimeIndex(d['ldate']); d=d[~d.index.duplicated(keep='last')]
    day=pd.DatetimeIndex(h.index.tz_convert(None).normalize()); hm=h.index.hour*100+h.index.minute
    h=h.assign(day=day,hm=hm)
    h=h[h.hm<1500]
    g=h.groupby('day')
    summ=g['hm'].apply(lambda x:(x==1430).any()); nb=g.size()
    full=nb>=8
    last=g.apply(lambda x:x.sort_values('hm').iloc[-1]['c'])
    hh=g['h'].max(); lw=g['l'].min(); vs=g['v'].sum()
    dd=d.reindex(hh.index)
    X=pd.DataFrame({'summer':summ,'full':full,'cov_h':np.isclose(hh,dd['h'],rtol=1e-6),'cov_l':np.isclose(lw,dd['l'],rtol=1e-6),
       'hmiss':hh<dd['h']-1e-9,'lmiss':lw>dd['l']+1e-9,'absCL':np.abs(np.log(dd['c']/last))*1e4,'vr':vs/dd['v'],
       'c_eq_h':np.isclose(dd['c'],dd['h']),'c_eq_l':np.isclose(dd['c'],dd['l'])})
    X=X[X.full]
    # aşırı: gün yüksek/düşüğü h1'de yoksa ve kapanış o uç değilse -> eksik sürekli işlem parçası
    X['miss_not_close']=(X.hmiss&~X.c_eq_h)|(X.lmiss&~X.c_eq_l)
    X['sym']=s; rows.append(X)
A=pd.concat(rows)
print(A.groupby('summer')[['cov_h','cov_l','miss_not_close','absCL','vr']].mean().round(3))
# last-bar label and per-bar volume share in winter vs summer
s='THYAO'
h=pd.read_parquet(f'{D}/h1/{s}.IS.parquet'); day=pd.DatetimeIndex(h.index.tz_convert(None).normalize()); hm=h.index.hour*100+h.index.minute
h=h.assign(day=day,hm=hm); sm=h.groupby('day')['hm'].transform(lambda x:(x==1430).any())
h=h[h.hm<1500]
h['vsh']=h['v']/h.groupby('day')['v'].transform('sum')
h['rng']=np.log(h['h']/h['l'])*1e4
print(h.groupby([sm.reindex(h.index).values,'hm'])[['vsh','rng']].mean().round(3).unstack(0))
