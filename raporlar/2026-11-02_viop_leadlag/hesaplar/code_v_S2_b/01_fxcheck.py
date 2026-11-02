"""v_S2_b 01: Yahoo TRY=X günlük barının gerçek zaman damgası (bağımsız; ll.py kullanılmadı).
Günlük bar (ldate L) 'c' değerini saatlik TRY=X barlarının KAPANIŞ (c) değerleriyle karşılaştır: L-1 ve L günlerinin her UTC saati."""
import pandas as pd, numpy as np
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
d=pd.read_parquet(D+'/daily/TRY=X.parquet'); d=d.set_index(pd.DatetimeIndex(d.ldate)); d=d[~d.index.duplicated(keep='last')]
h=pd.read_parquet(D+'/h1/TRY=X.parquet'); h.index=pd.DatetimeIndex(h.index).tz_convert('UTC')
# bar başlangıcı -> bar sonu fiyatı = c ; bar sonu zamanı = start+1h
hc=pd.Series(h.c.values, index=h.index+pd.Timedelta(hours=1)).astype(float)
ho=pd.Series(h.o.values, index=h.index).astype(float)  # bar başlangıcındaki fiyat
hh=pd.concat([hc,ho]).groupby(level=0).last().sort_index()   # fiyat @ zaman
rows=[]
for L,r in d[d.index>='2024-01-20'].iterrows():
    for off in range(-30,16):  # saat: L 00:00 UTC'ye göre
        t=pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=off)
        if t in hh.index:
            rows.append((L,off,1e4*abs(np.log(r.c/hh[t]))))
R=pd.DataFrame(rows,columns=['L','off','absbps'])
g=R.groupby('off').absbps.agg(['median','mean','count'])
print('Günlük c (ldate L) ile saatlik fiyat @ L 00:00 UTC + off saat arasındaki |fark| (bps):')
print(g.round(2).to_string())
# open de kontrol
rows=[]
for L,r in d[d.index>='2024-01-20'].iterrows():
    for off in range(-30,16):
        t=pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=off)
        if t in hh.index: rows.append((L,off,1e4*abs(np.log(r.o/hh[t]))))
R2=pd.DataFrame(rows,columns=['L','off','absbps']); print('Günlük o için:'); print(R2.groupby('off').absbps.median().round(2).to_string())
