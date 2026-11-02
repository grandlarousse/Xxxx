import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
# (1) o==c (sahte açılış) günlerini at
q=pd.read_parquet(RES+'/06_q.parquet'); T=raw('TCELL.IS')
oeqc=(abs(np.log(T.o/T.c))<1e-6).astype(float).reindex(bistcal()).shift(-1).reindex(q.index).fillna(0).astype(bool)
print('o==c (t+1) gün sayısı yıl:',q[oeqc].groupby(q[oeqc].index.year).size().to_dict())
w=q[~oeqc]
for lab,s,e in [('ALL','2014','2026-12-31'),('IS','2014','2020-12-31'),('OOS','2021','2026-12-31')]:
    z=w.loc[s:e]; m,n=ols(z.intra1_raw,z[['D']]); m2,_=ols(z.intra1_raw,z[['D','gap1_raw']])
    r,_=bt(z.U,z.intra1_raw,0.005,8); r2,_=bt(z.D,z.intra1_raw,0.005,8)
    print(f'  o==c hariç {lab}: b_D {m.params.D:+.3f}(t {m.tvalues.D:+.2f}) | D+gap {m2.params.D:+.3f}(t {m2.tvalues.D:+.2f}) n {n} | BT U50 {r["mean"]:+.1f} Sh {r["sh"]:+.2f} | D50 {r2["mean"]:+.1f} Sh {r2["sh"]:+.2f}')
# (2) ES/NQ kontrolü: TKC kapanış saati = 16:00 New York -> UTC
def h1(sym):
    H=pd.read_parquet(f'{H1}/{sym}.parquet'); H.index=pd.DatetimeIndex(H.index).tz_convert('UTC'); H['hm']=H.index.strftime('%H:%M'); H['ld']=pd.DatetimeIndex(H.ldate); return H
K=h1('TKC'); E=h1('ES=F'); N=h1('NQ=F')
k1530=K[K.hm=='15:30'].set_index('ld').o; Kd=raw('TKC'); tk_post=np.log(Kd.c/k1530)
def px(H):
    a=pd.concat([pd.Series(H.o.values,index=H.index),pd.Series(H.c.values,index=H.index+pd.Timedelta(hours=1))]); return a[~a.index.duplicated(keep='last')].sort_index()
ep=px(E); npx=px(N)
rows={}
for d in k1530.index:
    tc=pd.Timestamp(d.date().isoformat()+' 16:00',tz='America/New_York').tz_convert('UTC')
    t0=pd.Timestamp(d.date().isoformat()+' 15:30',tz='UTC')
    rows[d]=(np.log(ep.asof(tc)/ep.asof(t0)),np.log(npx.asof(tc)/npx.asof(t0)))
EP=pd.DataFrame(rows,index=['es_post','nq_post']).T
z=pd.read_parquet(RES+'/07_intraday.parquet')[['r_7c','g_7','D']].join(tk_post.rename('tk_post')).join(EP)
z.loc[z.tk_post.abs()>0.15,'tk_post']=np.nan
print('corr(tk_post,es_post)',round(z[['tk_post','es_post']].corr().iloc[0,1],3),' n',z[['tk_post','es_post']].dropna().shape[0])
for xs in [['tk_post'],['tk_post','es_post'],['tk_post','nq_post'],['es_post'],['tk_post','es_post','D']]:
    m,n=ols(z.r_7c,z[xs]); print(f'  r_7c ~ {xs}: '+'  '.join(f'{c} {m.params[c]:+.3f}({m.tvalues[c]:+.2f})' for c in xs)+f' n {n}')
# idiyosinkratik tk_post: tk_post - beta*es_post
zz=z.dropna(subset=['tk_post','es_post']); be=np.polyfit(zz.es_post,zz.tk_post,1)[0]; z['tk_idio']=z.tk_post-be*z.es_post
m,n=ols(z.r_7c,z[['tk_idio']]); print(f'  r_7c ~ tk_idio (beta_es {be:.2f}): {m.params.tk_idio:+.3f}({m.tvalues.tk_idio:+.2f}) n {n}')
for thr in [0,0.005]:
    r,_=bt(z.tk_idio,z.r_7c,thr,8); print(f'  BT tk_idio |>{thr*1e4:.0f}|: n {r["n"]} {r["mean"]:+.1f} Sh {r["sh"]:+.2f}')
