import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code'); from lib_altin import bh_fdr
import pandas as pd, numpy as np
pd.set_option('display.width',250); pd.set_option('display.max_columns',40)
R=pd.read_csv('eval_all.csv')
print("== summary counts")
for V in ['V1','V2']:
  for pn in ['VAL','OOS','ALL']:
    q=R[(R.V==V)&(R.period==pn)]
    i=q.r2_hm.idxmax(); j=q.cw_t_hm.idxmax()
    print(V,pn,'r2>0',(q.r2_hm>0).sum(),'max',round(q.r2_hm.max()*100,2),q.loc[i,'model'],q.loc[i,'h'],'cw>1.645',(q.cw_t_hm>1.645).sum(),'maxcw',round(q.cw_t_hm.max(),2),q.loc[j,'model'],q.loc[j,'h'],'sh>0',(q.tim_sharpe>0).sum(),'dm>0.3',(q.tim_sharpe_dm>0.3).sum(),'r2_0>0',(q.r2_0>0).sum(),'bh',q.tim_bh_sharpe.iloc[0])
q=R[R.V=='V3']; print('V3 r2>0',(q.r2_hm>0).sum(),'range',round(q.r2_hm.min()*100,2),round(q.r2_hm.max()*100,2),'maxcw',round(q.cw_t_hm.max(),2),q.loc[q.cw_t_hm.idxmax(),['model','h','r2_hm']].tolist(), 'c1 sh', q[q.model=='c1_apriori'].tim_sharpe.round(2).tolist(), 'bh', q.tim_bh_sharpe.iloc[0])
print("== selected rows")
sel=[('V1','ridge',1),('V1','ridge',3),('V1','hgb',5),('V1','rf',3),('V1','ens_ml',1),('V1','c1_apriori',1),('V2','hgb',1),('V2','rf',3),('V2','ridge',5),('V2','ens_ml',1),('V2','rf',1)]
rows=[]
for V,m,h in sel:
  a=R[(R.V==V)&(R.model==m)&(R.h==h)].set_index('period')
  rows.append(dict(V=V,m=m,h=h,r2val=a.loc['VAL','r2_hm']*100,r2oos=a.loc['OOS','r2_hm']*100,r20oos=a.loc['OOS','r2_0']*100,cwoos=a.loc['OOS','cw_t_hm'],ictval=a.loc['VAL','ic_t'],ictoos=a.loc['OOS','ic_t'],ictall=a.loc['ALL','ic_t'],shval=a.loc['VAL','tim_sharpe'],shoos=a.loc['OOS','tim_sharpe'],dmoos=a.loc['OOS','tim_sharpe_dm'],L=a.loc['OOS','tim_long_sharpe'],S=a.loc['OOS','tim_short_sharpe'],sh10=a.loc['OOS','tim_sharpe_10bps'],shall=a.loc['ALL','tim_sharpe'],turn=a.loc['OOS','tim_turnover'],raw=a.loc['OOS','raw_sharpe'],rawdm=a.loc['OOS','raw_sharpe_dm']))
print(pd.DataFrame(rows).round(2).to_string(index=False))
print("== selection"); print(pd.read_csv('selection_val_to_oos.csv').round(4).to_string(index=False))
c=R[(R.V=='V1')&(R.model=='c1_apriori')][['h','period','ic_t','tim_sharpe','tim_sharpe_dm','tim_long_sharpe','tim_short_sharpe','tim_sharpe_10bps','tim_turnover']]; print(c.round(3).to_string(index=False))
Y=pd.read_csv('eval_yearly.csv'); print(Y[(Y.V=='V2')&(Y.model.isin(['rf']))].round(2).dropna(axis=1,how='all').to_string(index=False)); print(Y[(Y.V=='V1')&(Y.model.isin(['c1_apriori']))].round(2).dropna(axis=1,how='all').to_string(index=False))
print("== diag")
for V in ['V1','V2','V3']:
  g=pd.read_csv(f'diag_{V}.csv'); print(V, g.groupby('h').agg(lasso0=('lasso_nnz',lambda x:(x==0).mean()), ridge_med=('ridge_alpha','median'), nfeat=('n_feat','max')).round(2).to_dict())
print("== permimp"); pb=pd.read_csv('permimp_base.csv'); print(pb.groupby('model').oos_r2_hm.agg(['min','max']).mul(100).round(2))
g=pd.read_csv('permimp_groups.csv'); print(g.pivot_table(index='group',columns=['model','h'],values='d_mse_1e6').round(2).to_string())
fi=pd.read_csv('permimp_features.csv')
for (h,m),q in fi.groupby(['h','model']): print(h,m,q.sort_values('d_mse_1e6',ascending=False).head(5)[['feature','d_mse_1e6']].round(3).values.tolist())
print("== robust"); rb=pd.read_csv('robust.csv')
def gr(V,m,h,ch,col): return round(float(rb[(rb.V==V)&(rb.model==m)&(rb.h==h)&(rb.check==ch)][col].iloc[0]),4)
for (V,m,h) in [('V1','ridge',3),('V2','rf',1),('V1','c1_apriori',1),('V1','c1_apriori',3),('V2','rf',3)]:
  print(V,m,h,{ch:(gr(V,m,h,ch,'r2_hm'),gr(V,m,h,ch,'tim_sharpe_all'),gr(V,m,h,ch,'tim_sharpe_oos')) for ch in ['base','uc_haric','roll_haric','cot_gecikme_haric']})
b=rb[rb.check.str.startswith('bagimsiz')].groupby(['V','model','h'])[['r2_hm','ic']].mean(); print(b.loc[[('V1','ridge',3),('V2','rf',3),('V2','ridge',3)]].round(4))
print("== placebo"); print(pd.read_csv('placebo_preds.csv').round(3).to_string(index=False))
print("== registry")
r=pd.read_csv('/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/registry/a8_ml_kombinasyon.csv'); print(len(r), r.family.value_counts().to_dict(), 'dup', r.test_id.duplicated().sum())
r['a']=r.t.abs(); m=r.p.notna(); r.loc[m,'q']=bh_fdr(r.p[m].values); print('n_t',r.t.notna().sum(),'|t|>=2',(r.a>=2).sum(),'|t|>=3',(r.a>=3).sum(),'minq',round(r.q.min(),3))
print(r[r.a>=2].groupby('family').size())
