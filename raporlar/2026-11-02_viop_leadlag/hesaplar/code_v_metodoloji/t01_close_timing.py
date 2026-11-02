# T01: Günlük kapanışın hangi UTC saatine karşılık geldiğini saatlik veriyle bağımsız ölç (ll.py kullanılmaz)
import pandas as pd, numpy as np, sys
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
syms=sys.argv[1:] or ['TRY=X','EURUSD=X','EURTRY=X','ES=F','BZ=F','GC=F','^VIX','TUR','^GDAXI','^N225','BTC-USD','XU100.IS','THYAO.IS','HG=F','NG=F','^TNX','ZN=F','DX-Y.NYB']
for s in syms:
    try:
        d=pd.read_parquet(f'{B}/daily/{s}.parquet'); h=pd.read_parquet(f'{B}/h1/{s}.parquet')
    except Exception as e: print(s,'yok',e); continue
    h=h.sort_index(); end=h.index+pd.Timedelta(hours=1)  # bar sonu
    hc=pd.Series(h['c'].values,index=end)
    dd=d[d.index>=h.index[0]+pd.Timedelta(days=2)].iloc[:-1]
    res={}
    for off in range(-30,49):  # ldate 00:00 UTC'ye göre saat ofseti (bar sonu)
        tgt=pd.DatetimeIndex(dd['ldate'].values).tz_localize('UTC')+pd.Timedelta(hours=off)
        pos=hc.index.searchsorted(tgt,side='right')-1
        ok=pos>=0
        px=np.where(ok,hc.values[np.clip(pos,0,None)],np.nan)
        age=(tgt-hc.index[np.clip(pos,0,None)]).total_seconds()/3600
        px[age>1.01]=np.nan
        dev=np.abs(np.log(dd['c'].values/px))
        res[off]=(np.nanmedian(dev)*1e4, np.mean(dev<1e-4), np.isfinite(dev).sum())
    r=pd.DataFrame(res,index=['med_bp','exact_frac','n']).T
    best=r['med_bp'].idxmin()
    print(f"{s:10s} en iyi ofset (ldate 00:00 UTC + saat) = {best:+d}h  medyan sapma={r.loc[best,'med_bp']:.1f}bp tam_eşleşme={r.loc[best,'exact_frac']:.2f} n={int(r.loc[best,'n'])} | BIST kapanışı(+15h) sapma={r.loc[15,'med_bp'] if 15 in r.index else np.nan:.1f}bp")
