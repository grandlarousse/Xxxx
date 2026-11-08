import json,sys,warnings,pandas as pd,numpy as np
warnings.filterwarnings('ignore')
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.tsa.api import VAR
D=sys.argv[1]
def y(f,adj=True,monthly=True):
    j=json.load(open(f"{D}/{f}"))['chart']['result'][0]
    ts=pd.to_datetime(j['timestamp'],unit='s'); q=j['indicators']
    v=q['adjclose'][0]['adjclose'] if adj and 'adjclose' in q else q['quote'][0]['close']
    s=pd.Series(v,index=ts,dtype=float).dropna()
    if monthly: s.index=s.index.to_period('M'); s=s.groupby(level=0).last()
    return s
print("== Returns (adj, local ccy): YTD, 1Y, 2025, vol3y")
for k in ['ITA','XAR','EUAD','GSPC','URTH','JETS','GE','RTX','LMT','BA','AIR.PA','SAF.PA','RHM.DE','BA.L']:
    s=y(f"y_{k}.json"); r=s.pct_change()
    g=lambda p: s[:pd.Period(p,'M')].iloc[-1]
    print(f"{k:7s} YTD {(s.iloc[-1]/g('2025-12')-1)*100:6.1f} 1Y {(s.iloc[-1]/g('2025-10')-1)*100:6.1f} 2025 {(g('2025-12')/g('2024-12')-1)*100:6.1f} 3M {(s.iloc[-1]/g('2026-07')-1)*100:6.1f} vol3y {r[-36:].std()*np.sqrt(12)*100:5.1f}")
ita=y("y_ITA.json"); print("ITA 3y ann", round(((ita.iloc[-1]/ita[pd.Period('2023-10','M')])**(1/3)-1)*100,1), "5y ann", round(((ita.iloc[-1]/ita[pd.Period('2021-10','M')])**(1/5)-1)*100,1), "1M", round((ita.iloc[-1]/ita[pd.Period('2026-10','M')]-1)*100,1) if False else '')
# weekly 2026 path
d={k:y(f"d_{k}.json",adj=False,monthly=False) for k in ['ITA','EUAD','GSPC','JETS']}
df=pd.DataFrame(d); df.index=df.index.normalize(); df=df.groupby(level=0).last().dropna()
# split-adjust ITA daily close (3:1 split) using adjclose instead
jd=json.load(open(f"{D}/d_ITA.json"))['chart']['result'][0]; 
ad=pd.Series(jd['indicators']['adjclose'][0]['adjclose'],index=pd.to_datetime(jd['timestamp'],unit='s').normalize()).groupby(level=0).last(); df['ITA']=ad
df=df.dropna(); df=df/df.iloc[0]*100
w=df.resample('W-FRI').last().round(1); w.index=w.index.strftime('%Y-%m-%d'); w.to_csv(f"{D}/weekly2026.csv")
print("weekly rows",len(w), "first", df.index[0].date(), "last", df.index[-1].date()); print(df.iloc[-1].round(1).to_dict())
for k in df: print(k,"peak",df[k].idxmax().date(),round(df[k].max(),1),"min after peak",round(df[k][df[k].idxmax():].min(),1))
# ===== DXY vs aircraft backlog
dxy=y("y_DXY_long.json",adj=False)
def fred(s):
    f=pd.read_csv(f"{D}/f_{s}.csv"); f.columns=['d','v']; f['v']=pd.to_numeric(f.v,errors='coerce'); f.index=pd.to_datetime(f.d).dt.to_period('M'); return f.v.groupby(level=0).last()
uo,vs,ip,brd=fred('ANAPUO'),fred('ANAPVS'),fred('IPG3364S'),fred('DTWEXBGS')
X=pd.DataFrame({'dxy':dxy,'uo':uo,'vs':vs,'ip':ip,'broad':brd}).loc['1992-01':]
X['bm']=X.uo/X.vs
print("\nM3 coverage", uo.dropna().index[0], uo.dropna().index[-1], "| DXY", dxy.index[0], dxy.index[-1])
print("BM last", round(X.bm.dropna().iloc[-1],1), "BM 2019-01", round(X.bm['2019-01'],1), "BM max", round(X.bm.max(),1), X.bm.idxmax(), "BM mean 1992-2018", round(X.bm[:'2018-12'].mean(),1))
print("BM by year-end:", X.bm.groupby(X.index.year).last().round(1).to_dict())
Z=X.dropna(subset=['dxy','uo','vs']).copy()
Z['ld']=np.log(Z.dxy).diff(); Z['dbm']=Z.bm.diff(); Z['lvs']=np.log(Z.vs).diff(); Z['lip']=np.log(Z.ip).diff()
Z['ld12']=np.log(Z.dxy).diff(12)*100; Z['dbm12']=Z.bm.diff(12); Z['lvs12']=np.log(Z.vs).diff(12)*100; Z['lip12']=np.log(Z.ip).diff(12)*100
print("\nADF p: dxy lvl %.3f, bm lvl %.3f, ld %.4f, dbm %.4f, lvs %.4f"%(adfuller(np.log(Z.dxy))[1],adfuller(Z.bm)[1],adfuller(Z.ld.dropna())[1],adfuller(Z.dbm.dropna())[1],adfuller(Z.lvs.dropna())[1]))
def cor(a,b,sub=None):
    T=Z if sub is None else Z.loc[sub[0]:sub[1]]; t=T[[a,b]].dropna(); r=t[a].corr(t[b]); n=len(t)
    se=1/np.sqrt(n); return round(r,3), n
for sub in [None,('1992-01','2019-12'),('2020-01','2026-12')]:
    print("\nSUB",sub)
    print(" level corr log dxy vs bm:", cor('dxy','bm',sub))
    print(" yoy: d12logDXY vs d12BM", cor('ld12','dbm12',sub), " vs ship yoy", cor('ld12','lvs12',sub), " vs IP yoy", cor('ld12','lip12',sub))
    print(" mom: dlogDXY vs dBM", cor('ld','dbm',sub), " vs dlog ship", cor('ld','lvs',sub))
# cross-corr yoy: DXY leads by k months
cc={k: round(Z.ld12.shift(k).corr(Z.dbm12),3) for k in range(-12,25,6)}; print("\ncross-corr DXY(t-k) vs dBM12(t):",cc)
cc2={k: round(Z.ld12.shift(k).corr(Z.lvs12),3) for k in range(-12,25,6)}; print("cross-corr DXY(t-k) vs ship yoy(t):",cc2)
# Granger
def gr(y_,x_,sub=None,maxlag=12):
    T=Z if sub is None else Z.loc[sub[0]:sub[1]]; t=T[[y_,x_]].dropna()
    sel=VAR(t).select_order(maxlags=maxlag); lag=max(1,sel.aic)
    res=grangercausalitytests(t,[lag])[lag][0]['ssr_ftest']
    return dict(lag=lag,F=round(res[0],2),p=round(res[1],3),n=len(t))
for sub in [None,('1992-01','2019-12'),('2020-01','2026-12')]:
    print("\nGranger",sub)
    print(" DXY -> dBM :",gr('dbm','ld',sub)); print(" dBM -> DXY :",gr('ld','dbm',sub))
    print(" DXY -> ship:",gr('lvs','ld',sub)); print(" ship -> DXY:",gr('ld','lvs',sub))
    print(" DXY -> IP  :",gr('lip','ld',sub))
# broad dollar robustness
Z2=X.dropna(subset=['broad','uo','vs']).copy(); Z2['lb']=np.log(Z2.broad).diff(); Z2['dbm']=Z2.bm.diff()
t=Z2[['dbm','lb']].dropna(); lag=max(1,VAR(t).select_order(12).aic); print("\nBroad USD -> dBM (2006+):", lag, round(grangercausalitytests(t,[lag])[lag][0]['ssr_ftest'][1],3), "yoy corr", round((np.log(Z2.broad).diff(12)).corr(Z2.bm.diff(12)),3))
# rolling 60m corr of yoy
rc=Z.ld12.rolling(60).corr(Z.dbm12).dropna(); print("rolling60 corr range", round(rc.min(),2), rc.idxmin(), round(rc.max(),2), rc.idxmax(), "share>0", round((rc>0).mean(),2))
# export monthly chart data (quarter-end to keep rows small)
E=Z[['dxy','bm']].dropna(); E=E[E.index.month.isin([3,6,9,12]) | (E.index==E.index[-1])].round(1); E.index=E.index.strftime('%Y-%m'); E.to_csv(f"{D}/dxy_bm_q.csv"); print("export rows",len(E), E.tail(3).to_dict())
