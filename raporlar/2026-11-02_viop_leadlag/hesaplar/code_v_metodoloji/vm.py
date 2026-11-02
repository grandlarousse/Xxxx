import warnings; warnings.filterwarnings("ignore")
"""v_metodoloji bağımsız yükleyici (ll.py İMPORT EDİLMEZ). Ham parquet'ten hizalama/temizlik."""
import os, numpy as np, pandas as pd
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
_c={}
def raw(sym,kind='daily'):
    k=(sym,kind)
    if k not in _c: _c[k]=pd.read_parquet(f'{B}/{kind}/{sym.replace("/","_")}.parquet')
    return _c[k]
def cal(stock_union=True):
    """BIST takvimi: XU100 barları + (Yahoo'da XU100'ün eksik olduğu ama ≥20 VİOP hissesinin işlem gördüğü günler)."""
    x=raw('XU100.IS'); c=pd.DatetimeIndex(x.loc[x['v'].fillna(0)>0,'ldate'].values).unique()
    return c.sort_values()
def px(sym,field='adj',fx_fix=True):
    d=raw(sym); s=pd.Series(d[field].values,index=pd.DatetimeIndex(d['ldate'].values)).astype(float)
    s=s[~s.index.duplicated(keep='last')].dropna(); s=s[s>0]
    if fx_fix and sym.endswith('=X'): s=s.shift(-1).dropna()
    return s
def on_cal(s,c=None):
    c=cal() if c is None else c; c=c[c>=s.index[0]]
    return s.reindex(s.index.union(c)).ffill().reindex(c)
def clean_bist(r):
    pre=r.index<pd.Timestamp('2020-03-13')
    up=np.where(pre,np.log(1.205),np.log(1.105)); dn=np.where(pre,np.log(0.795),np.log(0.895))
    r=r.copy(); r[(r>up)|(r<dn)]=np.nan; return r
def ret(sym,field='adj',fx_fix=True,sig12=False,c=None):
    s=on_cal(px(sym,field,fx_fix),c); r=np.log(s).diff()
    if sym.endswith('.IS'): r=clean_bist(r)
    elif sig12:
        sd=r.rolling(250,min_periods=60).std().shift(1); r[(r.abs()>12*sd)&sd.notna()]=np.nan
    return r
def decomp(sym,start='2014-01-01'):
    d=raw(sym).copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]
    d=d[(d['c']>0)&(d['o']>0)]
    cc=np.log(d['adj']).diff(); intra=np.log(d['c']/d['o']); gap=cc-intra
    out=pd.DataFrame({'cc':cc,'gap':gap,'intra':intra})
    pre=out.index<pd.Timestamp('2020-03-13')
    bad=(out['cc']>np.where(pre,np.log(1.205),np.log(1.105)))|(out['cc']<np.where(pre,np.log(0.795),np.log(0.895)))
    out[bad]=np.nan
    out.loc[(out['gap'].abs()>np.log(1.105)),['gap','intra']]=np.nan
    return out[out.index>=pd.Timestamp(start)]
def nwt(y,x,L=5):
    import statsmodels.api as sm
    df=pd.concat([pd.Series(y).rename('y'),pd.Series(x).rename('x')],axis=1).dropna()
    if len(df)<30: return np.nan,np.nan,len(df)
    m=sm.OLS(df['y'].values,sm.add_constant(df['x'].values)).fit(cov_type='HAC',cov_kwds={'maxlags':L})
    return m.params[1],m.tvalues[1],len(df)
