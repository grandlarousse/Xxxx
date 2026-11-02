import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
pd.set_option('display.width',250)
T=raw('TCELL.IS'); X=raw('XU100.IS'); K=raw('TKC'); F=raw('TRY=X')
for d0 in ['2021-12-15','2022-09-08','2023-02-13','2018-08-10','2019-04-26']:
    s=pd.Timestamp(d0); e=s+pd.Timedelta(days=9)
    t=T.loc[s:e,['o','h','l','c','v']]; x=X.loc[s:e,['o','h','l','c']].add_prefix('xu_')
    k=K.loc[s:e,['c']].add_prefix('tkc_'); f=F.loc[s:e,['o','c']].add_prefix('fx_')
    print(pd.concat([t,x,k,f],axis=1).round(3).to_string()); print()
