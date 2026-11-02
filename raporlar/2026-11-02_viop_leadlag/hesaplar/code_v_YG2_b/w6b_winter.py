"""Kış vekili, piyasa-nötr: hisseye özgü LH_id = LH - LH_XU030 -> yx (kesit arındırılmış C->07:30), gün FE."""
import numpy as np, pandas as pd, vlib as v
A=pd.read_parquet(v.RES+'/panel.parquet'); XU=A[A.sym=='XU030'].set_index('date')
S=A[A.sym!='XU030'].copy(); S['yx']=S['y']-S.groupby('date')['y'].transform('mean')
S['LH_id']=S['LH']-S['date'].map(XU['LH']); S['CA_id']=S['CA']-S['date'].map(XU['CA'])
S['win']=np.where(S.summer,'yaz','kış')
S['sea']=np.where(S.date.dt.month>=10, S.date.dt.year.astype(str)+'/'+(S.date.dt.year+1).astype(str), (S.date.dt.year-1).astype(str)+'/'+S.date.dt.year.astype(str))
for w in ['yaz','kış']:
    d=S[(S.win==w)][['yx','LH_id','DAY','date','sym']].dropna(); Z=v.demean2(d,['yx','LH_id','DAY'])
    b,se=v.ols_cl(Z['yx'],Z[['LH_id','DAY']],d['date'])
    print(w,'yx ~ LH_id (2yönlü FE): b %.3f (t %.1f), n_gün %d'%(b[1],b[1]/se[1],d.date.nunique()))
    for thr in [25,50]:
        dd,x=v.port(S[S.win==w],'LH_id','yx',thr/1e4); print('   portföy |LH_id|>%d excess:'%thr, v.summ(dd,x))
print('kış sezonları (excess, |LH|>25):')
for sea,g in S[S.win=='kış'].groupby('sea'):
    dd,x=v.port(g,'LH','yx',0.0025); print('  ',sea,v.summ(dd,x))
# yaz: LH bileşenleri
d=S[S.win=='yaz'][['yx','CA_id','DAY','date','sym']].dropna(); Z=v.demean2(d,['yx','CA_id','DAY']); b,se=v.ols_cl(Z['yx'],Z[['CA_id','DAY']],d['date'])
print('yaz yx ~ CA_id FE: b %.3f (t %.1f)'%(b[1],b[1]/se[1]))
