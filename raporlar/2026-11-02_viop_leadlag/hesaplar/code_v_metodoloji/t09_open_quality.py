# T09: Yahoo günlük açılış (o) ile saatlik ilk bar (06:30 UTC) açılışı uyumu; o==önceki c günlerinde açılış gerçekten değişmemiş mi?
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji'); sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code')
import vm, numpy as np, pandas as pd
from universe import VIOP
rows=[]
for s in VIOP+['XU030','XU100','XBANK']:
    try: h=vm.raw(s+'.IS','h1')
    except Exception: continue
    h=h.sort_index(); f=h[(h.index.hour==6)&(h.index.minute==30)]
    fo=pd.Series(f['o'].values,index=pd.DatetimeIndex(f['ldate'].values)); fo=fo[~fo.index.duplicated()]
    d=vm.raw(s+'.IS').copy(); d.index=pd.DatetimeIndex(d['ldate'].values); d=d[~d.index.duplicated(keep='last')]
    d['pc']=d['c'].shift(1); d=d[d.index>=fo.index[0]]
    j=pd.concat([d[['o','c','pc','h','l']],fo.rename('h1o')],axis=1).dropna()
    eq=j['o']==j['pc']
    dev=np.abs(np.log(j['o']/j['h1o']))
    # gerçek açılış hareketi (h1 açılışı) o==pc günlerinde ne kadar?
    true_gap_on_eq=np.abs(np.log(j.loc[eq,'h1o']/j.loc[eq,'pc']))
    rows.append(dict(sym=s,n=len(j),o_eq_pc_pct=round(eq.mean()*100,1),o_vs_h1o_exact_pct=round((dev<1e-6).mean()*100,1),o_vs_h1o_med_bp=round(dev.median()*1e4,1),
                     eqdays_h1o_eq_pc_pct=round((true_gap_on_eq<1e-6).mean()*100,1) if eq.sum() else np.nan,
                     eqdays_true_absgap_med_bp=round(true_gap_on_eq.median()*1e4,1) if eq.sum() else np.nan,
                     h1o_eq_pc_pct=round((np.abs(np.log(j['h1o']/j['pc']))<1e-6).mean()*100,1)))
T=pd.DataFrame(rows); print(T.to_string(index=False))
print('ÖZET: o==pc günlerinde saatlik ilk bar açılışı da ==pc olan oran (medyan):',T.eqdays_h1o_eq_pc_pct.median(), '| Günlük o ile h1 açılışı birebir aynı (medyan %):',T.o_vs_h1o_exact_pct.median())
