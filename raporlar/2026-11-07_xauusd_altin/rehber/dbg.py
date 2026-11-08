import sys, math, datetime as dt, numpy as np, pandas as pd
S_="/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S_}/out/sentez"); import sinyal_altin as SA
K=SA.PanelKaynak(f"{S_}/panel", log=lambda *a: None)
t=dt.date(2026,11,9); kar=SA.etf_karar(t); g=K.veri_gunleri_etf(t); gg=g[:g.index(t)]
kk={x:K.kapanis(x,kar) for x in ("GLD","GDX","GDXJ","SPY")}
R=pd.DataFrame({x:SA._getiri(kk[x],gg) for x in kk}, index=gg); n=len(R)
Y=R.GDX.values; X=R[["GLD","SPY"]].values
for i in range(n-10,n):
    b=SA._beta2(Y,X,i,250,60); e=Y[i]-b[0]*X[i,0]-b[1]*X[i,1]
    print(gg[i], R.iloc[i].round(4).to_dict(), b.round(3), round(e*100,3))
e=SA.madenci_artik(R,"GDX",range(n-40,n)); print((e.iloc[-3:]*100).round(3).tolist(), e.iloc[-3:].sum()*100, e.iloc[-10:].sum()*100)
print(R.iloc[-3:].sum()*100)
