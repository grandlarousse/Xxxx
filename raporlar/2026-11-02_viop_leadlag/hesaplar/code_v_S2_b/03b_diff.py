import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
me=pd.read_parquet(RES+'/02_daily.parquet').loc['2014':]
a=pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a/res/02_daily.parquet').loc['2014':]
j=me[['D','intra1','gap1']].join(a[['D','intra1','gap1']],rsuffix='_a',how='outer')
print('D corr',j[['D','D_a']].corr().iloc[0,1],' intra1 corr',j[['intra1','intra1_a']].corr().iloc[0,1])
print('n D',j.D.notna().sum(),j.D_a.notna().sum(),' n intra1',j.intra1.notna().sum(),j.intra1_a.notna().sum())
x=j[(j.intra1-j.intra1_a).abs()>1e-6].dropna(subset=['intra1','intra1_a']); print('intra1 farklı gün',len(x)); print(x.head(10))
y=j[j.intra1.isna()&j.intra1_a.notna()]; print('bende NaN onda değil:',len(y)); print(y.assign(ai=1e4*y.intra1_a).sort_values('ai').head(8)); print(y.assign(ai=1e4*y.intra1_a).sort_values('ai').tail(8))
y2=j[j.intra1.notna()&j.intra1_a.isna()]; print('onda NaN bende değil:',len(y2)); print(y2.head())
dd=j[(j.D-j.D_a).abs()>1e-4].dropna(subset=['D','D_a']); print('D farklı gün',len(dd)); print(dd.head(10))
# farklı gün kümesiyle regresyon
for lab,s,e in [('ALL','2014','2026-12-31'),('IS','2014','2020-12-31'),('OOS','2021','2026-12-31')]:
    z=j.loc[s:e]
    m,n=ols(z.intra1_a,z[['D_a','gap1_a']]); m2,n2=ols(z.intra1,z[['D_a','gap1']]); m3,n3=ols(z.intra1_a,z[['D','gap1_a']])
    print(lab,'onların veri:',round(m.params.D_a,3),round(m.tvalues.D_a,2),n,' | benim hedef+onların D:',round(m2.params.D_a,3),round(m2.tvalues.D_a,2),n2,' | onların hedef+benim D:',round(m3.params.D,3),round(m3.tvalues.D,2),n3)
