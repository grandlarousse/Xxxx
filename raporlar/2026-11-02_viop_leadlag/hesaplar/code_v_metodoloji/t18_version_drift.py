# T18: ll v3 (tüm dönem ±%10,5, hacim=0 günleri at) vs v4 (2020-03-13 öncesi ±%20,5, bayat = v=0 & h==l) farkı
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji'); sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import vm, pandas as pd, numpy as np
from universe import VIOP
cnt=[]; vz=[]
for s in VIOP:
    d=vm.raw(s+'.IS').copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]
    r=np.log(d['adj']).diff()
    a=r.abs(); m=(a>np.log(1.105))&(a<np.log(1.205))
    cnt.append(pd.Series(m.groupby(m.index.year).sum(),name=s))
    vzero=(d['v'].fillna(0)<=0); stale=vzero&(d['h']==d['l'])
    vz.append(dict(sym=s,v0_pct_2024p=round(vzero[d.index>='2024-01-01'].mean()*100,1),stale_pct_2024p=round(stale[d.index>='2024-01-01'].mean()*100,1)))
C=pd.concat(cnt,axis=1).fillna(0)
print('47 hissede |r| %10,5–%20,5 gün sayısı (yıllara göre):', C.sum(axis=1).astype(int).to_dict())
V=pd.DataFrame(vz); print('2024+ hacim=0 günü oranı yüksek olanlar (v3 bu günleri siliyordu):'); print(V.sort_values('v0_pct_2024p',ascending=False).head(8).to_string(index=False))
# Örnek etki: XU100 kontrollü bir senkron korelasyon ve bir gap-fade sonucunun v3 vs v4 kuralına göre değişimi (2014-2019 IS)
def clean(r,rule):
    if rule=='v3': return r.where(~((r>np.log(1.105))|(r<np.log(0.895))))
    pre=r.index<pd.Timestamp('2020-03-13'); up=np.where(pre,np.log(1.205),np.log(1.105)); dn=np.where(pre,np.log(0.795),np.log(0.895))
    return r.where(~((r>up)|(r<dn)))
res=[]
for s in ['CIMSA','OYAKC','HEKTS','DOHOL','SASA','ASELS','KRDMD','THYAO']:
    d=vm.raw(s+'.IS').copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]; d=d[d.index>='2014-01-01']
    cc=np.log(d['adj']).diff(); intra=np.log(d['c']/d['o']); gap=cc-intra
    for rule in ['v3','v4']:
        ok=clean(cc,rule).notna()&clean(gap,rule).notna()
        g=gap[ok]; i=intra[ok]; sig=g.abs()>0.01
        pnl=(-np.sign(g)*i)[sig]
        IS=pnl[pnl.index<'2021-01-01']
        res.append(dict(sym=s,rule=rule,n_gun=int(ok.sum()),fade_IS_bps=round(1e4*IS.mean(),1),fade_IS_n=len(IS)))
R=pd.DataFrame(res).pivot(index='sym',columns='rule',values=['n_gun','fade_IS_bps','fade_IS_n']); print(R.to_string())
