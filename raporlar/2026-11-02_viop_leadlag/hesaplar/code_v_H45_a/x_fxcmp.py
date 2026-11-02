"""Kontrol: benim USDTRY_{t-1} hizam vs iddianın (ll tarzı: FX_FIX shift(-1)+ffill+12σ temizlik, shift(1)) hizası."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
E=V.decomp('ENKAI'); cal=V.bist_cal()
fx=V.raw('TRY=X')['c'].astype(float); fx=fx[fx>0]
s=fx.shift(-1).dropna(); s=s.reindex(s.index.union(cal)).ffill().reindex(cal)
r=np.log(s).diff(); sd=r.rolling(250,min_periods=60).std().shift(1); bad=(r.abs()>12*sd)&sd.notna()
print('12σ ile silinen günler (2014+):', r[bad].loc['2014':].round(3).to_dict())
rc=r.copy(); rc[bad]=np.nan
mine=V.fx_prev('TRY=X')
d=pd.concat([mine.rename('mine'),rc.shift(1).rename('claim'),r.shift(1).rename('claim_noclean')],axis=1).loc['2014':]
print('farklı gün sayısı (mine vs claim_noclean):', int((abs(d.mine-d.claim_noclean)>1e-9).sum()))
print(d[(abs(d.mine-d.claim_noclean)>1e-9)].head(8))
for nm in ['mine','claim','claim_noclean']:
    print(f'{nm:14s}', [(round(a,3),round(b,2)) for a,b,_ in [V.corr_t(E['intra'],d[nm]),V.corr_t(E['intra'],d[nm],V.IS0,V.SPLIT),V.corr_t(E['intra'],d[nm],V.SPLIT)]])
