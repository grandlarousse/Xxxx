# T02: FX_FIX shift(-1) eksik FX barlarında look-ahead üretir mi? BIST günü t için lag-1 FX getirisinin BİTİŞ anı > BIST t açılışı (06:40 UTC açılış seansı) ise look-ahead.
import pandas as pd, numpy as np
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
x=pd.read_parquet(f'{B}/daily/XU100.IS.parquet'); x=x[x['v'].fillna(0)>0]
cal=pd.DatetimeIndex(x['ldate'].values).unique().sort_values()
cal=cal[cal>=pd.Timestamp('2005-01-01')]
rows=[]
for s in ['TRY=X','EURTRY=X','EURUSD=X','GBPTRY=X','JPY=X','CNY=X','ZAR=X','RUB=X','DX-Y.NYB']:
    d=pd.read_parquet(f'{B}/daily/{s}.parquet'); L=pd.DatetimeIndex(d['ldate'].values)
    L=L[~L.duplicated(keep='last')]; L=L[d['c'].values[~pd.DatetimeIndex(d['ldate'].values).duplicated(keep='last')]>0] if False else L
    dow=pd.Series(L.dayofweek).value_counts().sort_index().to_dict()
    # shift(-1) sonrası ldate t'nin değeri = sonraki barın (t') 00:00 UTC fiyatı
    nxt=pd.Series(L[1:].append(pd.DatetimeIndex([pd.NaT])), index=L)
    if s.endswith('=X'):
        end_time=nxt  # gerçek fiyat anı (yaklaşık 00:00 UTC t')
    else:
        end_time=pd.Series(L+pd.Timedelta(hours=21),index=L)
    # BIST takviminde: BIST günü t için sürücü fiyatı = ldate<=t olan son bar -> zaman = end_time(o bar)
    lastbar=pd.Series(L,index=L).reindex(L.union(cal)).ffill().reindex(cal)
    et=end_time.reindex(lastbar.values).values
    et=pd.DatetimeIndex(et)
    # lag-1 sinyal (BIST t için): BIST t-1'deki fiyat anı; look-ahead eğer > BIST t açılış (t 06:40 UTC)
    prev_et=pd.Series(et,index=cal).shift(1)
    open_t=pd.Series(cal+pd.Timedelta(hours=6,minutes=40),index=cal)
    close_t=pd.Series(cal+pd.Timedelta(hours=15),index=cal)
    la_open=(prev_et>open_t)
    la_close=(prev_et>close_t)
    # lag-0 'senkron' getirisinin bitişi BIST t kapanışından ne kadar sonra?
    lag0_after=(pd.Series(et,index=cal)-close_t).dt.total_seconds()/3600
    gaps=(nxt-pd.Series(L,index=L)).dt.days
    wk_missing=((gaps>1)&~((pd.Series(L,index=L).dt.dayofweek==4)&(gaps==3))).sum()
    rows.append(dict(sym=s,n=len(L),gun_dagilimi=dow,hafta_ici_eksik_bar=int(wk_missing),
        lag1_lookahead_acilis=int(la_open.sum()),lag1_lookahead_kapanis=int(la_close.sum()),
        frac_la_open=round(la_open.mean()*100,2), lag0_bitis_bist_kapanisindan_sonra_medyan_saat=float(lag0_after.median())))
    if s=='TRY=X':
        print('TRY=X lag-1 look-ahead günleri (ilk 25):', [str(t.date()) for t in la_open[la_open].index[:25]])
print(pd.DataFrame(rows).to_string(index=False))
