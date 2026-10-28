import pandas as pd, numpy as np
exec(open('load.py').read())
c=x100['c']; f=fx['c'].reindex(c.index).ffill()
usd=c/f
# --- (a) >=20% drop from 30-trading-day rolling max close
rm=c.rolling(30,min_periods=10).max()
dd=c/rm-1
ev=[]; last=None
for d,v in dd.items():
    if v<=-0.20 and (last is None or (c.index.get_loc(d)-c.index.get_loc(last))>63):
        ev.append(d); last=d
def fwd(series,d,n):
    i=series.index.get_loc(d)
    if i+n>=len(series): return np.nan
    return series.iloc[i+n]/series.iloc[i]-1
def mae(series,d,n):
    i=series.index.get_loc(d)
    w=series.iloc[i+1:i+n+1]
    if len(w)<n: return np.nan
    return w.min()/series.iloc[i]-1
rows=[]
for d in ev:
    pk=c.loc[:d].iloc[-30:].idxmax()
    rows.append(dict(event=d.date(),peak=pk.date(),dd=round(dd[d]*100,1),
      r21=round(fwd(c,d,21)*100,1),r42=round(fwd(c,d,42)*100,1),r63=round(fwd(c,d,63)*100,1),
      mae63=round(mae(c,d,63)*100,1),
      usd63=round(fwd(usd.dropna(),d,63)*100,1) if d>=pd.Timestamp('2005-01-10') else np.nan))
A=pd.DataFrame(rows); print("(a) XU100 >=20% düşüş, 30 işlem günü içinde (63g cooldown)"); print(A.to_string())
print(A[['r21','r42','r63','mae63','usd63']].describe().loc[['count','mean','50%','min','max']].round(1))
print('pozitif oran r21,r63:',(A.r21>0).mean().round(2),(A.r63>0).mean().round(2))
# unconditional
for n in (21,63):
    u=(c.shift(-n)/c-1).dropna()
    print(f'koşulsuz {n}g: ort {u.mean()*100:.1f}% medyan {u.median()*100:.1f}% poz {(u>0).mean():.2f}')
    u2=u.loc['2005':]; print(f'  2005+ : ort {u2.mean()*100:.1f}% medyan {u2.median()*100:.1f}%')
# --- (b) 6+ consecutive weekly declines
w=c.resample('W-FRI').last().dropna()
wr=w.pct_change()
cnt=0; evb=[]
for d,v in wr.items():
    cnt = cnt+1 if v<0 else 0
    if cnt==6: evb.append(d)
print("\n(b) 6 hafta üst üste haftalık düşüş (6. hafta kapanışı)")
rows=[]
for d in evb:
    dd_=c.loc[:d].index[-1]
    i=w.index.get_loc(d); tot=w.iloc[i]/w.iloc[i-6]-1
    rows.append(dict(week=d.date(),cum6w=round(tot*100,1),r21=round(fwd(c,dd_,21)*100,1),r63=round(fwd(c,dd_,63)*100,1),mae63=round(mae(c,dd_,63)*100,1)))
print(pd.DataFrame(rows).to_string())
# 5+ weeks
cnt=0; ev5=[]
for d,v in wr.items():
    cnt = cnt+1 if v<0 else 0
    if cnt==5: ev5.append(d)
rows=[]
for d in ev5:
    dd_=c.loc[:d].index[-1]; i=w.index.get_loc(d); tot=w.iloc[i]/w.iloc[i-5]-1
    rows.append(dict(week=d.date(),cum5w=round(tot*100,1),r21=round(fwd(c,dd_,21)*100,1),r63=round(fwd(c,dd_,63)*100,1),mae63=round(mae(c,dd_,63)*100,1)))
B=pd.DataFrame(rows); print("\n(b2) 5+ hafta üst üste düşüş"); print(B.to_string()); print(B[['r21','r63','mae63']].describe().loc[['count','mean','50%']].round(1))
