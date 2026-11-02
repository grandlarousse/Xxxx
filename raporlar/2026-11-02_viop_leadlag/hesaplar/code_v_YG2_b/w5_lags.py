"""CA_t'nin sonraki 3 günün parçalarına etkisi (dağıtılmış gecikme): gece+sabah tekrar tekrar mı dönüyor?"""
import numpy as np, pandas as pd, vlib as v
A=pd.read_parquet(v.RES+'/panel.parquet'); S=A[A.sym!='XU030'].sort_values(['sym','date']).copy()
S['ov']=np.log(S['P0730_n']/S['C'])  # C_t -> 07:30_{t+1}
S['dy']=np.log(S['C_n']/S['P0730_n'])  # 07:30_{t+1} -> C_{t+1}
for c in ['ov','dy']: S.loc[S[c].abs()>0.105,c]=np.nan
rows=[]
for k in range(0,4):  # parçalar t+k
    S[f'ov{k}']=S.groupby('sym')['ov'].shift(-k); S[f'dy{k}']=S.groupby('sym')['dy'].shift(-k)
for k in range(0,4):
    for p in ['ov','dy']:
        d=S[['CA',f'{p}{k}','date','sym']].dropna(); Z=v.demean2(d,['CA',f'{p}{k}'])
        b,se=v.ols_cl(Z[f'{p}{k}'],Z[['CA']],d['date']); b0,se0=v.ols_cl(d[f'{p}{k}'],d[['CA']],d['date'])
        rows.append(dict(piece=('gece+sabah C->07:30' if p=='ov' else 'gün 07:30->C'),day=f't+{k+1}' if p=='ov' else f't+{k+1}',b_ham=round(b0[1],3),t_ham=round(b0[1]/se0[1],1),b_fe=round(b[1],3),t_fe=round(b[1]/se[1],1),n=len(d)))
R=pd.DataFrame(rows); print(R.to_string()); R.to_csv(v.RES+'/w5_lags.csv',index=False)
# Toplam kümülatif: C_t -> C_{t+3}
S['c3']=np.log(S.groupby('sym')['C'].shift(-3)/S['C']); S.loc[S.c3.abs()>0.2,'c3']=np.nan
d=S[['CA','c3','date','sym']].dropna(); b,se=v.ols_cl(d['c3'],d[['CA']],d['date']); print('C_t->C_{t+3} ~ CA: %.3f (t %.1f)'%(b[1],b[1]/se[1]))
# Aynı yapı plasebo: L60 (sürekli işlem 13:30-14:30) için gece+sabah t+2
S['L60_']=S['L60']
for k in [0,1]:
    d=S[['L60_',f'ov{k}','date']].dropna(); b,se=v.ols_cl(d[f'ov{k}'],d[['L60_']],d['date']); print(f'L60 -> ov t+{k+1}: %.3f (t %.1f)'%(b[1],b[1]/se[1]))
# ertesi gün CA'sı ile ilişki: CA_t -> L30_{t+1}, DAY_{t+1}, CA_{t+1}
for c in ['CA','L30','DAY']:
    S[c+'_n']=S.groupby('sym')[c].shift(-1); d=S[['CA',c+'_n','date']].dropna(); b,se=v.ols_cl(d[c+'_n'],d[['CA']],d['date']); print(f'{c}_(t+1) ~ CA_t: %.3f (t %.1f)'%(b[1],b[1]/se[1]))
