# T16: Yahoo '=X' günlük kapanış zamanlaması yıllara göre değişiyor mu? Referans: ABD'de 20/21 UTC kapanan FXE (EURUSD), FXY (JPY), UUP (DXY).
# ham FX r(t) (kaydırmasız) ile ETF r(t-1), r(t) korelasyonu. Kapanış t günü 00:00 UTC ise r_raw(t) ≈ ETF(t-1) ile eşleşir (FX_FIX doğru). Gün sonu ise ETF(t) ile (FX_FIX look-ahead yaratır).
import warnings; warnings.filterwarnings("ignore")
import pandas as pd, numpy as np, os
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/daily'
def s(sym):
    d=pd.read_parquet(f'{B}/{sym}.parquet'); x=pd.Series(d['adj'].values,index=pd.DatetimeIndex(d['ldate'].values)); x=x[~x.index.duplicated(keep='last')]; return np.log(x[x>0]).diff()
pairs=[('EURUSD=X','FXE',1),('JPY=X','FXY',-1),('EURUSD=X','UUP',-1),('TRY=X','TUR',-1)]
for fx,etf,sg in pairs:
    if not os.path.exists(f'{B}/{etf}.parquet'): print(etf,'yok'); continue
    a=s(fx); b=s(etf)
    df=pd.concat([a.rename('fx'),b.rename('e'),b.shift(1).rename('e_m1'),b.shift(-1).rename('e_p1')],axis=1).dropna()
    out=df.groupby(df.index.year).apply(lambda g: pd.Series({'c_ayni_gun':sg*g.fx.corr(g.e),'c_etf_dun':sg*g.fx.corr(g.e_m1),'n':len(g)}))
    out['karar']=np.where(out.c_etf_dun>out.c_ayni_gun,'00:00 UTC (FX_FIX doğru)','gün sonu (FX_FIX look-ahead!)')
    print(f'--- {fx} vs {etf}'); print(out.round(3).to_string())
