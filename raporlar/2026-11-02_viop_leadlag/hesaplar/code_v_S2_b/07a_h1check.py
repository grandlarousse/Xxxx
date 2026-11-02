import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
h=pd.read_parquet(H1+'/TCELL.IS.parquet'); h.index=pd.DatetimeIndex(h.index).tz_convert('UTC')
m=pd.read_parquet(M5+'/TCELL.IS.parquet'); m.index=pd.DatetimeIndex(m.index).tz_convert('UTC')
d=raw('TCELL.IS')
h['hm']=h.index.strftime('%H:%M'); print(h.hm.value_counts().sort_index())
b630=h[h.hm=='06:30']; print('06:30 bar v=0 oranı:',(b630.v==0).mean().round(3))
# 06:30 bar o == günlük o?
b=b630.set_index(pd.DatetimeIndex(b630.ldate)); j=b[['o','c','v']].join(d[['o','c']],rsuffix='_d')
print('06:30 bar o == günlük o oranı:',(abs(np.log(j.o/j.o_d))<1e-4).mean().round(3))
# m5 ile: 06:30 h1 bar close vs m5 07:25 bar close (son 60 gün)
m['hm']=m.index.strftime('%H:%M'); m['ld']=pd.DatetimeIndex(m.ldate)
c725=m[m.hm=='07:25'].set_index('ld').c; o730=m[m.hm=='07:30'].set_index('ld').o; o655=m[m.hm=='06:55'].set_index('ld').o
jj=pd.concat([b.c.rename('h1_0630c'),c725.rename('m5_0725c'),o730.rename('m5_0730o'),o655.rename('m5_0655o'),d.o.rename('daily_o')],axis=1).dropna()
print('n',len(jj),' |h1 06:30 c - m5 07:25 c| medyan bps',(1e4*abs(np.log(jj.h1_0630c/jj.m5_0725c))).median().round(2),' max',(1e4*abs(np.log(jj.h1_0630c/jj.m5_0725c))).max().round(1))
print(' |m5 06:55 o - günlük o| medyan bps',(1e4*abs(np.log(jj.m5_0655o/jj.daily_o))).median().round(2))
# 06:30 bar v=0 günlerinde close nedir?
z=j[j.v==0]; print('v=0 günleri: c==o oranı',(abs(np.log(z.c/z.o))<1e-4).mean().round(3), ' n',len(z))
print(b630[b630.v==0].tail(5))
print(m[(m.ld=='2026-10-30')&(m.hm<'07:40')][['o','h','l','c','v']])
