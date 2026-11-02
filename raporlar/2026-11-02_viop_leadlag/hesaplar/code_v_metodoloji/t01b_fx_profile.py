# T01b: FX günlük kapanışın saat profili (bar sonu = h1 bar başlangıcı+1s). Getiri bazında da test: günlük r(t) ile saatlik pencere getirisi korelasyonu
import pandas as pd, numpy as np
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
for s in ['TRY=X','EURTRY=X','EURUSD=X','JPY=X']:
    d=pd.read_parquet(f'{B}/daily/{s}.parquet'); h=pd.read_parquet(f'{B}/h1/{s}.parquet').sort_index()
    hc=pd.Series(h['c'].values,index=h.index+pd.Timedelta(hours=1))
    dd=d[d.index>=h.index[0]+pd.Timedelta(days=3)].iloc[:-2]
    L=pd.DatetimeIndex(dd['ldate'].values).tz_localize('UTC')
    rd=np.log(dd['c']).diff().values  # günlük getiri ldate t-1 -> t
    out=[]
    for off in [-24,-12,-6,-3,-1,0,1,3,6,9,12,15,18,21,23,24,25,30,36,48]:
        tgt=L+pd.Timedelta(hours=off); pos=hc.index.searchsorted(tgt,side='right')-1
        px=hc.values[np.clip(pos,0,None)]; age=(tgt-hc.index[np.clip(pos,0,None)]).total_seconds()/3600; px=np.where(age<=3,px,np.nan)
        rh=np.diff(np.log(px),prepend=np.nan)
        ok=np.isfinite(rd)&np.isfinite(rh)
        out.append((off, np.nanmedian(np.abs(np.log(dd['c'].values/px)))*1e4, np.corrcoef(rd[ok],rh[ok])[0,1], ok.sum()))
    print(s); print(pd.DataFrame(out,columns=['ofset_saat','seviye_medyan_bp','getiri_corr','n']).to_string(index=False))
