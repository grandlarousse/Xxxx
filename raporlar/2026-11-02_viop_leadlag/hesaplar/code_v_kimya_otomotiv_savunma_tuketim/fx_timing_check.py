"""Bağımsız FX zaman damgası kontrolü: Yahoo '=X' günlük kapanışı (ldate t) hangi UTC anına denk geliyor?
h1 bar zaman damgası = bar başlangıcı; bar sonu = +60 dk. Günlük c(t) ile şu anlardaki saatlik fiyat karşılaştırılır:
 A: 00:00 UTC t (bar 23:00 t-1 kapanışı), B: 15:00 UTC t, C: 00:00 UTC t+1 (bar 23:00 t kapanışı)."""
import pandas as pd, numpy as np, sys
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
for s in ['EURUSD=X','TRY=X','EURTRY=X','JPY=X','KRW=X']:
    try:
        d=pd.read_parquet(f'{D}/daily/{s}.parquet'); h=pd.read_parquet(f'{D}/h1/{s}.parquet')
    except Exception as e:
        print(s,'yok',e); continue
    dc=pd.Series(d['c'].values,index=pd.DatetimeIndex(d['ldate'].values)); dc=dc[~dc.index.duplicated(keep='last')]
    hc=pd.Series(h['c'].values,index=h.index+pd.Timedelta(minutes=60)).sort_index()  # bar sonu
    hc.index=hc.index.tz_convert(None)
    def at(ts):
        pos=hc.index.searchsorted(ts,side='right')-1
        v=np.where(pos>=0,hc.values[np.clip(pos,0,None)],np.nan)
        age=(ts.values-hc.index.values[np.clip(pos,0,None)])
        v[age>np.timedelta64(3,'h')]=np.nan
        return pd.Series(v,index=ts)
    days=dc.index[(dc.index>='2024-02-01')&(dc.index<='2026-10-29')]
    out={}
    for lab,off in [('A_00UTC_t',0),('B_15UTC_t',15),('C_00UTC_t+1',24),('D_21UTC_t',21)]:
        ts=pd.DatetimeIndex(days+pd.Timedelta(hours=off))
        p=at(ts).values
        diff=np.abs(np.log(dc.reindex(days).values/p))*1e4
        out[lab]=np.nanmedian(diff)
    # günlük getiri korelasyonu: daily r(t) vs saatlik r (A->A) vs (C->C)
    r_d=np.log(dc.reindex(days)).diff()
    rA=np.log(at(pd.DatetimeIndex(days)).values); rA=pd.Series(rA,index=days).diff()
    rC=np.log(at(pd.DatetimeIndex(days+pd.Timedelta(hours=24))).values); rC=pd.Series(rC,index=days).diff()
    print(f"{s}: medyan |log fark| bps: "+", ".join(f"{k}={v:.1f}" for k,v in out.items())+
          f" | corr(r_daily, r[00UTC t-1->00UTC t])={r_d.corr(rA):.3f}, corr(r_daily, r[00UTC t->00UTC t+1])={r_d.corr(rC):.3f}")
