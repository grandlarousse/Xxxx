# T15: VİOP bülten 'open' 23.09.2022 öncesi = ilk sürekli işlem (zamanı bilinmiyor; spot açılışından SONRA olabilir) -> 'vadeli açılış -> spot gap' R² şişer mi?
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, pandas as pd, numpy as np
v=pd.read_parquet(f'{vm.B}/viop_panel.parquet'); v=v[(v.segment=='SSF')&(v.open>0)&(v.prev_settle>0)]
v=v.sort_values('value_tl').groupby(['und','date']).tail(1)  # günün en likit kontratı
v['gF']=np.log(v.open/v.prev_settle)
rows=[]
for u,g in v.groupby('und'):
    try: dd=vm.decomp(u+'.IS',start='2017-01-01')
    except Exception: continue
    g=g.set_index('date'); j=pd.concat([g[['gF','trades','value_tl']],dd['gap'],dd['intra']],axis=1).dropna()
    j=j[(j.gF.abs()<0.1)]
    j['post']=j.index>=pd.Timestamp('2022-09-23'); j['und']=u
    rows.append(j)
A=pd.concat(rows)
A['liq']=A.groupby(A.index.year)['trades'].transform(lambda x: pd.qcut(x.rank(method='first'),3,labels=['düşük','orta','yüksek']))
print('Dönem x likidite: corr(gF, spot gap) ve corr(gF, spot gün-içi)')
for (p,l),g in A.groupby(['post','liq']):
    print(f"{'2022-09-23 sonrası (09:30 seansı)' if p else '2022-09 öncesi (ilk sürekli işlem)':36s} likidite={l:6s} n={len(g):6d} corr(gF,gap)={g.gF.corr(g.gap):.3f} corr(gF,intra)={g.gF.corr(g.intra):+.3f}")
