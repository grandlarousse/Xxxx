"""Ek kontroller: 06:30 bar c'si (P07:30) bozuk mu (=O)? Ay bazında eğim; vade sonu/toplu müzayede günleri hariç."""
import numpy as np, pandas as pd, vlib as v
A=pd.read_parquet(v.RES+'/panel.parquet'); S=A[A.sym!='XU030'].copy()
S['yx']=S['y']-S.groupby('date')['y'].transform('mean'); S['yr']=S.date.dt.year; S['mo']=S.date.dt.month
S['eqO']=np.isclose(S.P0730,S.O); 
print('P07:30==O payı (yaz/kış, yıl):'); print(S[S.P0730.notna()].groupby(['summer','yr'])['eqO'].mean().round(3).unstack())
W=S[S.CA.notna()].copy()
print('\nAy bazında: ort |CA| bps, eğim (y~CA), portföy excess')
for mo,g in W.groupby('mo'):
    d=g[['y','CA','date']].dropna(); b,se=v.ols_cl(d['y'],d[['CA']],d['date']); s=v.summ(v.port(g,'CA','yx',0.0025)[0])
    print(mo,'|CA| %.1f  b %.2f (t %.1f)  port_x %.1f (t %.1f)  gün %d'%(1e4*g.CA.abs().mean(),b[1],b[1]/se[1],s['bps'],s['t'],d.date.nunique()))
cal=pd.Series(sorted(A.date.unique())); eom=set(cal.groupby([cal.dt.year,cal.dt.month]).max().values)
W['eom']=W.date.isin(eom)
mabs=W.groupby('date')['CA'].apply(lambda x:x.abs().mean()); big=set(mabs[mabs>mabs.quantile(.95)].index)
for lab,m in [('vade sonu hariç',~W.eom),('toplu müzayede (üst %5 gün) hariç',~W.date.isin(big)),('ikisi de hariç',~W.eom&~W.date.isin(big)),('Nisan hariç',W.mo!=4)]:
    print(lab,'ham',v.summ(*v.port(W[m],'CA','y',0.0025)),' excess',v.summ(v.port(W[m],'CA','yx',0.0025)[0]))
