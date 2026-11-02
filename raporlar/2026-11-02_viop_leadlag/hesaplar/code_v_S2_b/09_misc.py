"""09: yıllık kırılım, açılış verisi kalitesi, kayan b, kapanış seansı gürültüsü kanalı, ES kontrolü (saatlik)."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
q=pd.read_parquet(RES+'/06_q.parquet'); Y=q.intra1_raw
print('== Yıllık net bps/işlem (8 bps): U|>50 | D|>50 | D|>0   ve  b_D (ham hedef)')
pos={'U':0,'D50':0,'D0':0}
for y in range(2014,2027):
    s,e=str(y),f'{y}-12-31'
    a,_=bt(q.U,Y,0.005,8,s,e); b,_=bt(q.D,Y,0.005,8,s,e); c,_=bt(q.D,Y,0,8,s,e)
    pos['U']+=a['mean']>0; pos['D50']+=b['mean']>0; pos['D0']+=c['mean']>0
    print(f'  {y}: U {a["mean"]:+6.1f} (n {a["n"]}) | D50 {b["mean"]:+6.1f} (n {b["n"]}) | D0 {c["mean"]:+6.1f}')
print('  pozitif yıl:',pos)
# kayan 500g b
z=q[['D','intra1_raw']].dropna(); bs=[]
for i in range(500,len(z),20):
    w=z.iloc[i-500:i]; bs.append((w.index[-1],np.polyfit(w.D,w.intra1_raw,1)[0]))
B=pd.Series(dict(bs)); print(f'== Kayan 500g b: pozitif oranı {(B>0).mean():.2f}, min {B.min():+.3f}, medyan {B.median():+.3f}, max {B.max():+.3f}')
# açılış verisi kalitesi
T=raw('TCELL.IS'); T=T[T.v>0]
T['o_eq_pc']=(abs(np.log(T.o/T.c.shift(1)))<1e-6); T['o_out']=(T.o>T.h*1.0001)|(T.o<T.l*0.9999); T['o_eq_c']=abs(np.log(T.o/T.c))<1e-6
print('== TCELL açılış kalitesi (yıllık): o==önceki c | o [l,h] dışı | o==c')
print(T.loc['2012':].groupby(T.loc['2012':].index.year)[['o_eq_pc','o_out','o_eq_c']].mean().round(3).to_string())
# kapanış seansı kanalı (2023-12+): TCELL 15:00 sürekli (14:30 barı kapanışı) vs kapanış seansı
h=pd.read_parquet(H1+'/TCELL.IS.parquet'); h.index=pd.DatetimeIndex(h.index).tz_convert('UTC'); h['hm']=h.index.strftime('%H:%M'); h['ld']=pd.DatetimeIndex(h.ldate)
last_cont=h[h.hm!='15:00'].groupby('ld').c.last()   # son sürekli bar kapanışı (yaz/kış)
x=q.loc['2023-12':].copy(); x['pc']=last_cont.reindex(x.index)
x['auc']=np.log(x.tcc/x.pc)          # kapanış seansı sapması
x['Dcont']=x.D+x.auc                  # D'nin sürekli fiyatla versiyonu: D = ... - ln c ; Dcont = ... - ln pc
for xs in [['D'],['Dcont'],['Dcont','auc'],['D','auc']]:
    m,n=ols(x.intra1_raw,x[xs]); print(f'  2023-12+ intra1 ~ {xs}: '+'  '.join(f'{c} {m.params[c]:+.3f}({m.tvalues[c]:+.2f})' for c in xs)+f' n {n}')
# ES kontrolü: TKC kapanış saatine eşlenmiş ES post-close
def h1(sym):
    H=pd.read_parquet(f'{H1}/{sym}.parquet'); H.index=pd.DatetimeIndex(H.index).tz_convert('UTC'); H['hm']=H.index.strftime('%H:%M'); H['ld']=pd.DatetimeIndex(H.ldate); return H
K=h1('TKC'); E=h1('ES=F'); N=h1('NQ=F')
kc_time=K[K.v==0].groupby('ld').apply(lambda g:g.index.max())  # kapanış damgası (20:00/21:00)
k1530=K[K.hm=='15:30'].set_index('ld').o
Kd=raw('TKC'); tk_post=np.log(Kd.c/k1530)
ep=pd.Series(E.c.values,index=E.index+pd.Timedelta(hours=1)); ep=ep[~ep.index.duplicated()]
np_=pd.Series(N.c.values,index=N.index+pd.Timedelta(hours=1)); np_=np_[~np_.index.duplicated()]
rows={}
for d,tc in kc_time.items():
    t0=pd.Timestamp(d.date()).tz_localize('UTC')+pd.Timedelta(hours=15,minutes=30)
    a=ep.asof(t0); b=ep.asof(tc); a2=np_.asof(t0); b2=np_.asof(tc)
    rows[d]=(np.log(b/a) if a and b else np.nan, np.log(b2/a2) if a2 and b2 else np.nan)
EP=pd.DataFrame(rows,index=['es_post','nq_post']).T
z=pd.read_parquet(RES+'/07_intraday.parquet')[['r_7c','g_7','D']].join(tk_post.rename('tk_post')).join(EP)
z.loc[z.tk_post.abs()>0.15,'tk_post']=np.nan
for xs in [['tk_post'],['tk_post','es_post'],['tk_post','nq_post'],['tk_post','es_post','D']]:
    m,n=ols(z.r_7c,z[xs]); print(f'  saatlik r_7c ~ {xs}: '+'  '.join(f'{c} {m.params[c]:+.3f}({m.tvalues[c]:+.2f})' for c in xs)+f' n {n}')
print('  corr(tk_post, es_post)=',round(z[['tk_post','es_post']].corr().iloc[0,1],3))
