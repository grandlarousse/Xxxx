"""01b: Getiri bazlı zaman damgası tespiti: r_daily(L) = ln(c_L/c_{L-1}) ile saatlik pencere getirisi ln(p(L+off)/p(Lprev+off)) korelasyonu.
Ayrıca 'snapshot' ile BIST seansı içindeki kur hareketinin (07:00->15:00 UTC, L günü) r_daily(L) ile korelasyonu: c_L seans içini içeriyorsa pozitif olur."""
import pandas as pd, numpy as np
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
d=pd.read_parquet(D+'/daily/TRY=X.parquet'); d=d.set_index(pd.DatetimeIndex(d.ldate)); d=d[~d.index.duplicated(keep='last')]
h=pd.read_parquet(D+'/h1/TRY=X.parquet'); h.index=pd.DatetimeIndex(h.index).tz_convert('UTC')
hc=pd.Series(h.c.values, index=h.index+pd.Timedelta(hours=1)).astype(float)
ho=pd.Series(h.o.values, index=h.index).astype(float)
hh=pd.concat([hc,ho]).groupby(level=0).last().sort_index()
full=pd.date_range(hh.index.min().floor('h'),hh.index.max(),freq='h'); hp=hh.reindex(full).ffill()
d=d[d.index>='2024-01-20']; c=np.log(d.c.astype(float)); rd=c.diff()
Ls=d.index
out=[]
for off in range(-12,16):
    t=[pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=off) for L in Ls]
    p=np.log(hp.reindex(t).values); p=pd.Series(p,index=Ls); rh=p.diff()
    z=pd.concat([rd,rh],axis=1).dropna(); z=z[(z.iloc[:,0].abs()<0.05)&(z.iloc[:,1].abs()<0.05)]
    out.append((off, round(z.corr().iloc[0,1],3), round(1e4*(z.iloc[:,0]-z.iloc[:,1]).std(),2), len(z)))
print('off(saat, L 00:00 UTC\'ye göre)  corr(r_daily, r_hourly-snap)  sd(fark) bps  n'); 
for o in out: print(o)
# seans içi kur hareketi: L günü 07:00->15:00 UTC
t7=[pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=7) for L in Ls]; t15=[pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=15) for L in Ls]
ses=pd.Series(np.log(hp.reindex(t15).values)-np.log(hp.reindex(t7).values),index=Ls)
t0=[pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=-1) for L in Ls]; t6=[pd.Timestamp(L).tz_localize('UTC')+pd.Timedelta(hours=6) for L in Ls]
pre=pd.Series(np.log(hp.reindex(t6).values)-np.log(hp.reindex(t0).values),index=Ls)
# r_daily(L) -> c_L - c_{L-1}. c_L icinde L seansi var mi? corr(rd(L), ses(L)); c_{L+1} - c_L icinde L seansı var mı? corr(rd(L+1), ses(L))
z=pd.concat([rd.rename('rd'),rd.shift(-1).rename('rd_next'),ses.rename('ses'),pre.rename('pre')],axis=1).dropna()
print('corr(r_daily(L), kur L 07->15 UTC) =',round(z.rd.corr(z.ses),3),' corr(r_daily(L+1), kur L 07->15) =',round(z.rd_next.corr(z.ses),3))
print('corr(r_daily(L), kur L-1 23:00->L 06:00) =',round(z.rd.corr(z.pre),3))
# OLS: rd(L+1) ~ ses(L) beta: 1 ise L+1 barı L seansını tam içeriyor
b=np.polyfit(z.ses,z.rd_next,1)[0]; b0=np.polyfit(z.ses,z.rd,1)[0]; print('beta rd(L+1)~ses(L)',round(b,3),' beta rd(L)~ses(L)',round(b0,3))
