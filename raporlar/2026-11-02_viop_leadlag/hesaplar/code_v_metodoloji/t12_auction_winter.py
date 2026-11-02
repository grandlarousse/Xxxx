# T12: ry_akis c2_auction 'auc=log(C/snap15:00)' kışın 14:30 fiyatını kullanır -> son 30 dk sürekli işlem + müzayede karışır. Bağımsız yeniden hesap.
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
from universe import VIOP
import pandas as pd, numpy as np
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
rows=[]
for s in VIOP:
    h=pd.read_parquet(f'{B}/h1/{s}.IS.parquet').sort_index(); h=h[h.index.hour*60+h.index.minute<=14*60+30]
    end=h.index+pd.Timedelta(hours=1); end=end.where(~((h.index.hour==14)&(h.index.minute==30)),h.index+pd.Timedelta(minutes=30))
    last=pd.DataFrame({'c':h['c'].values,'end':end,'ld':pd.DatetimeIndex(h['ldate'].values)}).groupby('ld').tail(1).set_index('ld')
    d=pd.read_parquet(f'{B}/daily/{s}.IS.parquet'); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]
    cc=np.log(d['adj']).diff(); intra=np.log(d['c']/d['o']); gap=cc-intra
    j=pd.DataFrame({'C':d['c'],'P':last['c'],'endh':last['end'].dt.hour*60+last['end'].dt.minute,'gap1':gap.shift(-1),'cc1':cc.shift(-1)}).dropna(subset=['C','P'])
    j['auc']=np.log(j.C/j.P); j=j[j.auc.abs()<0.05]; j['stock']=s
    j['summer']=j.endh==15*60
    j['me']=j.index.to_series().groupby(j.index.to_period('M')).transform('max')==j.index.to_series()
    rows.append(j)
A=pd.concat(rows)
for lab,g in [('yaz (gerçek müzayede)',A[A.summer]),('kış (14:30->C: son30dk+müzayede)',A[~A.summer])]:
    b=np.polyfit(g.auc,g.cc1.fillna(0),1)[0]; bg=np.polyfit(g.auc,g.gap1.fillna(0),1)[0]
    print(f"{lab:35s} n={len(g):6d} |auc| ort={1e4*g.auc.abs().mean():5.1f} bps  ertesi cc eğimi={b:+.3f} ertesi gap eğimi={bg:+.3f}")
for lab,g in [('vade sonu',A[A.me]),('diğer',A[~A.me])]:
    print(f"{lab:10s} n={len(g)} kış payı={(~g.summer).mean():.2f} |auc| tümü={1e4*g.auc.abs().mean():.1f}  yaz={1e4*g[g.summer].auc.abs().mean():.1f}  kış={1e4*g[~g.summer].auc.abs().mean():.1f} | eğim cc1 tümü={np.polyfit(g.auc,g.cc1.fillna(0),1)[0]:+.3f} yaz={np.polyfit(g[g.summer].auc,g[g.summer].cc1.fillna(0),1)[0]:+.3f} kış={np.polyfit(g[~g.summer].auc,g[~g.summer].cc1.fillna(0),1)[0]:+.3f}")
