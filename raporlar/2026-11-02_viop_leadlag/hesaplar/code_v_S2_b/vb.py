"""v_S2_b yardımcıları — ll.py KULLANILMAZ. Ham parquet'ten kendi hizalama/temizlik."""
import pandas as pd, numpy as np, statsmodels.api as sm, warnings
warnings.filterwarnings('ignore')
SCR='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
DD=SCR+'/data/daily'; H1=SCR+'/data/h1'; M5=SCR+'/data/m5'
RES=SCR+'/out/code_v_S2_b/res'
VIOP="AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()

def raw(sym):
    d=pd.read_parquet(f'{DD}/{sym}.parquet'); d=d.set_index(pd.DatetimeIndex(d.ldate)).drop(columns='ldate')
    d=d[~d.index.duplicated(keep='last')].sort_index(); d.index.name='date'
    return d.astype(float)

_cal=None
def bistcal():
    global _cal
    if _cal is None:
        a=raw('XU100.IS'); b=raw('TCELL.IS')
        idx=a.index.union(b.index); _cal=idx[idx>='2005-01-01']
    return _cal

def bist(sym):
    """BIST hissesi: cc (adj), gap (temettü düzeltmeli), intra (ham o->c). ±%10,5 fiyat bazlı simetrik temizlik."""
    d=raw(sym if sym.endswith('.IS') else sym+'.IS'); d=d[(d.c>0)&(d.o>0)]
    if 'v' in d and not sym.startswith('XU'):
        d=d[d.v>0]
    d=d.reindex(bistcal())
    pc=d.c.shift(1); pa=d.adj.shift(1)
    cc=np.log(d.adj/pa)
    f=d.adj/d.c   # temettü faktörü
    gap=np.log(d.o*f/pa); intra=np.log(d.c/d.o)
    rawcc=d.c/pc-1
    bad=(rawcc>0.105)|(rawcc<-0.105)|((d.adj/pa-1)>0.105)|((d.adj/pa-1)<-0.105)
    badg=(np.exp(gap)-1>0.105)|(np.exp(gap)-1<-0.105)
    out=pd.DataFrame({'o':d.o,'c':d.c,'adj':d.adj,'v':d.v,'cc':cc,'gap':gap,'intra':intra})
    out.loc[bad|badg,['cc','gap','intra']]=np.nan
    out.loc[out.intra.abs()>0.105,['cc','gap','intra']]=np.nan
    return out

def fx_for_bist(sym='TRY=X', k=1):
    """BIST günü t için kur: ldate = t'den sonraki k'ıncı iş günü olan Yahoo barı (k=1 -> ≈00-06 UTC t+1; k=0 -> ≈00-06 UTC t, BIST t kapanışından ÖNCE)."""
    d=raw(sym); s=d.c[d.c>0]
    cal=bistcal()
    out={}
    sidx=s.index
    for t in cal:
        tgt=t+pd.offsets.BDay(k) if k>0 else t
        # tam ldate yoksa sonraki ilk bar (ama tgt'den sonra en fazla 3 gün)
        p=sidx.searchsorted(tgt)
        if p<len(sidx) and (sidx[p]-tgt).days<=3: out[t]=s.iloc[p]
    return pd.Series(out)

def ols(y,X,lags=5):
    z=pd.concat([y.rename('y')]+[X[c].rename(c) for c in X.columns] if isinstance(X,pd.DataFrame) else [y.rename('y'),X.rename('x')],axis=1).dropna()
    m=sm.OLS(z.y,sm.add_constant(z.drop(columns='y'))).fit(cov_type='HAC',cov_kwds={'maxlags':lags})
    return m,len(z)

def bt(sig,tgt,thr=0.0,cost=8.0,start=None,end=None):
    """sign(sig) pozisyon, |sig|>thr; net bps/işlem."""
    z=pd.concat([sig.rename('s'),tgt.rename('y')],axis=1).dropna()
    if start: z=z[z.index>=start]
    if end: z=z[z.index<=end]
    z=z[z.s.abs()>thr]
    p=np.sign(z.s)*z.y*1e4-cost
    if len(p)<5: return dict(n=len(p),mean=np.nan,t=np.nan,sh=np.nan,hit=np.nan),p
    nd=len(pd.concat([sig,tgt],axis=1).dropna().loc[start or '1900':end or '2100'])
    # yıllık Sharpe: günlük pnl serisi (işlem olmayan gün 0)
    daily=p.reindex(pd.concat([sig,tgt],axis=1).dropna().loc[start or '1900':end or '2100'].index).fillna(0)
    sh=daily.mean()/daily.std()*np.sqrt(252) if daily.std()>0 else np.nan
    return dict(n=len(p),mean=p.mean(),t=p.mean()/p.std()*np.sqrt(len(p)),sh=sh,hit=(p>0).mean()),p
