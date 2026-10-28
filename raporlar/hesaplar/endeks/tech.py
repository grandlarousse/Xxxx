import pandas as pd, numpy as np
exec(open('load.py').read())
def rsi(s,n=14):
    d=s.diff(); up=d.clip(lower=0); dn=-d.clip(upper=0)
    au=up.ewm(alpha=1/n,adjust=False).mean(); ad=dn.ewm(alpha=1/n,adjust=False).mean()
    return 100-100/(1+au/ad)
for name,df in [('XU030',x30),('XU100',x100)]:
    c=df['c']; h=df['h']; l=df['l']
    print('==',name,'son',c.index[-1].date(),round(c.iloc[-1],1))
    for n in (20,50,100,200):
        ma=c.rolling(n).mean().iloc[-1]; print(f' SMA{n}: {ma:,.0f} ({(c.iloc[-1]/ma-1)*100:+.1f}%)')
    e20=c.ewm(span=20,adjust=False).mean().iloc[-1]; print(f' EMA20: {e20:,.0f}')
    print(' RSI14 günlük:', round(rsi(c).iloc[-1],1), ' min son 30g:', round(rsi(c).iloc[-30:].min(),1), rsi(c).iloc[-30:].idxmin().date())
    w=c.resample('W-FRI').last(); print(' RSI14 haftalık:', round(rsi(w).iloc[-1],1))
    lr=np.log(c).diff()
    print(f' realize vol 20g yıllık: {lr.iloc[-20:].std()*np.sqrt(252)*100:.1f}%  60g: {lr.iloc[-60:].std()*np.sqrt(252)*100:.1f}%  1y: {lr.iloc[-252:].std()*np.sqrt(252)*100:.1f}%')
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    print(f' ATR14: {tr.rolling(14).mean().iloc[-1]:,.0f}')
    y=c.loc['2025-10-28':]; print(f' 52h aralık: {y.min():,.0f} ({y.idxmin().date()}) - {y.max():,.0f} ({y.idxmax().date()})')
    print(f' yılbaşı (2025 son kapanış): {c.loc[:"2025-12-31"].iloc[-1]:,.0f}')
    lo=c.loc['2025-01-01':'2025-12-31']; print(f' 2025 min: {lo.min():,.0f} {lo.idxmin().date()}, 2025 max {lo.max():,.0f} {lo.idxmax().date()}')
    print(' gün içi dip son 10g:', round(l.iloc[-10:].min(),0), l.iloc[-10:].idxmin().date())
    # fib from 2025 min to 2026 max
    a=lo.min(); b=c.loc['2026'].max()
    for r in (0.382,0.5,0.618): print(f'  fib {r}: {b-(b-a)*r:,.0f}')
# USD based
c=x100['c']; f=fx['c'].reindex(c.index).ffill(); u=(c/f).dropna()
print('USD bazlı XU100 son:',round(u.iloc[-1],1),' 14 Eyl:',round(u.loc['2026-09-14'],1),' 9 Eyl:',round(u.loc['2026-09-09'],1), ' düşüş', round((u.iloc[-1]/u.loc['2026-09-09']-1)*100,1))
print('USDTRY 9 Eyl', round(f.loc['2026-09-09'],3), 'son', round(f.iloc[-1],3))
u2=u.loc['2005':]
print('USD bazlı 2005+ yüzdelik:', round((u2<u.iloc[-1]).mean()*100,1))
print('USD bazlı 2018+ yüzdelik:', round((u.loc['2018':]<u.iloc[-1]).mean()*100,1),' 2023-06+:',round((u.loc['2023-06':]<u.iloc[-1]).mean()*100,1))
for per in ['2013-05','2018-08','2020-03','2021-12','2023-06','2024-07','2025-04','2025-12','2026-09']:
    s=u.loc[per]; print(f'  {per}: min {s.min():.0f} max {s.max():.0f}')
print('son 2 yılın en düşüğü:', round(u.loc['2024-10-28':].min(),1), u.loc['2024-10-28':].idxmin().date())
print('2023-06 sonrası en düşük:', round(u.loc['2023-07':].min(),1), u.loc['2023-07':].idxmin().date())
# XU030/XU100 ratio
r=(x30['c']/x100['c']).dropna(); print('XU030/XU100 oran son', round(r.iloc[-1],3),' 9 Eyl', round(r.loc['2026-09-09'],3))
