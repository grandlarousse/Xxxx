import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
cal=bistcal()
T=bist('TCELL'); K=raw('TKC')
fx1=fx_for_bist('TRY=X',1); fx0=fx_for_bist('TRY=X',0); fx2=fx_for_bist('TRY=X',2)
df=pd.DataFrame(index=cal)
df['tk']=K.adj.reindex(cal); df['tkc']=K.c.reindex(cal)   # NYSE kapalıysa NaN (ffill yok)
df['tc']=T.adj; df['tcc']=T.c
df['fx1']=fx1.reindex(cal); df['fx0']=fx0.reindex(cal); df['fx2']=fx2.reindex(cal)
for k in ['fx1','fx0','fx2']:
    P=np.log(df.tk*df[k]/(2.5*df.tc)); df['P_'+k]=P
    df['D_'+k]=P-P.shift(1).rolling(20,min_periods=10).mean()
df['Praw']=np.log(df.tkc*df.fx1/(2.5*df.tcc))
df['Draw']=df.Praw-df.Praw.shift(1).rolling(20,min_periods=10).mean()
df['D']=df.D_fx1
for c in ['cc','gap','intra']:
    df[c]=T[c]; df[c+'1']=T[c].shift(-1)
df['o1']=T.o.shift(-1); df['c1']=T.c.shift(-1)
X=bist('XU100'); df['xu_intra1']=X.intra.shift(-1); df['xu_gap1']=X.gap.shift(-1); df['xu_cc']=X.cc; df['xu_intra']=X.intra
X3=bist('XU030'); df['x30_intra1']=X3.intra.shift(-1)
df['tk_r']=np.log(df.tk).diff(); df['fx_r']=np.log(df.fx1).diff()
df.to_parquet(RES+'/02_daily.parquet')
print(df.loc['2014':].describe().T[['count','mean','std']].round(4).to_string())
print('yıllık medyan prim % (Praw):',(100*df.Praw.groupby(df.index.year).median()).round(2).to_dict())
