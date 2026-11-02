# T03: bist_cal() (XU100 hacim>0) ile 47 hissenin fiilen işlem gördüğü günlerin karşılaştırması + BIST tatili sonrası hizalama hatası sıklığı
import pandas as pd, numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
from universe import VIOP   # sadece sembol listesi (ll değil)
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
x=pd.read_parquet(f'{B}/daily/XU100.IS.parquet')
calall=pd.DatetimeIndex(x['ldate'].values)
cal=pd.DatetimeIndex(x.loc[x['v'].fillna(0)>0,'ldate'].values).unique().sort_values()
print('XU100 bar sayısı',len(calall),' hacim>0',len(cal),' hacim=0 atılan', len(calall)-len(cal))
dropped=calall.difference(cal)
cnt=pd.Series(0,index=calall.union(pd.DatetimeIndex([])))
for s in VIOP:
    d=pd.read_parquet(f'{B}/daily/{s}.IS.parquet'); L=pd.DatetimeIndex(d.loc[(d['v'].fillna(0)>0)&(d['h']!=d['l']),'ldate'].values)
    cnt=cnt.add(pd.Series(1,index=L.unique()),fill_value=0)
cnt=cnt.sort_index()
print('XU100 hacim=0 olup atılan günlerde kaç VİOP hissesi işlem görmüş (yıl, gün, hisse sayısı):')
dd=cnt.reindex(dropped).fillna(0)
print(dd[dd>=20].groupby(dd[dd>=20].index.year).size().to_dict(), ' toplam(>=20 hisse işlem):', int((dd>=20).sum()))
print(' örnek:', [ (str(i.date()),int(v)) for i,v in dd[dd>=20].head(15).items()])
extra=cnt[(cnt>=20)].index.difference(calall)
print('Hisselerin işlem gördüğü ama XU100 barı olmayan gün:', len(extra), [str(i.date()) for i in extra[:10]])
inc=cal[(cnt.reindex(cal).fillna(0)<5)&(cal>=pd.Timestamp('2008-01-01'))]
print('Takvimde olup <5 VİOP hissesinin işlem gördüğü gün (2008+):', len(inc), [str(i.date()) for i in inc[:15]])
# Tatil sonrası hizalama: BIST hafta içi tatili (önceki BIST günü ile t arasında ABD'nin işlem gördüğü bir hafta içi günü var)
es=pd.read_parquet(f'{B}/daily/ES=F.parquet'); usd=pd.DatetimeIndex(es['ldate'].values).unique()
c2=cal[cal>=pd.Timestamp('2010-01-01')]
prev=pd.Series(c2,index=c2).shift(1)
skipped=[]
for t,p in prev.dropna().items():
    between=usd[(usd>p)&(usd<t)]
    skipped.append(len(between))
sk=pd.Series(skipped,index=c2[1:])
print('2010+ BIST günleri:',len(sk),' önceki BIST günüyle arasında ABD işlem günü olan (lag0 ön-bilgi içerir):',int((sk>0).sum()), f'({(sk>0).mean()*100:.1f}%)', ' bunlardan >=2 ABD günü:',int((sk>=2).sum()))
# bunun bir sonraki günü de (lag1 penceresi tatil hareketini tekrar içerir)
nxt=(sk>0).shift(1).fillna(False)
print(' tatil sonrası 2. gün (lag1 penceresi zaten fiyatlanmış tatil hareketini içerir):', int(nxt.sum()))
print(' yıllık ortalama etkilenen gün:', round(((sk>0)|nxt).groupby(sk.index.year).sum().mean(),1))
sk.to_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji/us_days_between_bist.csv')
