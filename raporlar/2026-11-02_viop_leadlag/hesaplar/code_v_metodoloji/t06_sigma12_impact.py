# T06: 12-sigma filtresinin TL kuru/petrol/VIX bağlantılı korelasyonlara etkisi (filtreli vs filtresiz; filtresiz=yalnızca ertesi gün geri dönen veri hatalarını sil)
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, numpy as np, pandas as pd
c=vm.cal()
R=pd.read_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji/sigma12_removed.csv',parse_dates=['date'])
def drv(s,mode):
    r=np.log(vm.on_cal(vm.px(s),c)).diff()
    if mode=='f12':
        sd=r.rolling(250,min_periods=60).std().shift(1); r[(r.abs()>12*sd)&sd.notna()]=np.nan
    elif mode=='err':
        bad=R[(R.sym==s)&(R.reverts)].date; r[r.index.isin(bad)]=np.nan
    return r
pairs=[('XBANK.IS','TRY=X'),('XU100.IS','TRY=X'),('GARAN.IS','TRY=X'),('AKBNK.IS','TRY=X'),('FROTO.IS','TRY=X'),('THYAO.IS','TRY=X'),('TUPRS.IS','TRY=X'),('EREGL.IS','TRY=X'),('XBANK.IS','EURTRY=X'),('TUPRS.IS','BZ=F'),('THYAO.IS','BZ=F'),('PETKM.IS','BZ=F'),('XU100.IS','^VIX'),('ERGL','x')]
rows=[]
for st,d in pairs:
    if d=='x': continue
    g=vm.decomp(st,start='2005-01-01'); y=vm.ret(st,c=c)
    out={'pair':f'{st}~{d}'}
    for mode in ['f12','err']:
        r=drv(d,mode)
        df=pd.concat([y.rename('y'),r.rename('x'),r.shift(1).rename('x1'),g['gap'],g['intra']],axis=1)
        out[f'sync_{mode}']=df['y'].corr(df['x'])
        sub=df[df.index>=pd.Timestamp('2014-01-01')]
        out[f'gapL1_{mode}']=sub['gap'].corr(sub['x1']); out[f'intraL1_{mode}']=sub['intra'].corr(sub['x1']); out[f'ccL1_{mode}']=df['y'].corr(df['x1'])
        b,t,n=vm.nwt(df['y'],df['x']); out[f'beta_{mode}']=b
    rows.append(out)
T=pd.DataFrame(rows).set_index('pair').round(3)
print(T[['sync_f12','sync_err','beta_f12','beta_err','ccL1_f12','ccL1_err','gapL1_f12','gapL1_err','intraL1_f12','intraL1_err']].to_string())
T.to_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji/t06_out.csv')
