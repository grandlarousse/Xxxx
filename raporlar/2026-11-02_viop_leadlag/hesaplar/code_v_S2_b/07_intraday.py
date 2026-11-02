"""07: 2023-12+ saatlik: giriş zamanı gerçekçiliği + saatlik alt iddia (tk_post) bağımsız üretim ve çürütme."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
def h1(sym):
    h=pd.read_parquet(f'{H1}/{sym}.parquet'); h.index=pd.DatetimeIndex(h.index).tz_convert('UTC'); h['hm']=h.index.strftime('%H:%M'); h['ld']=pd.DatetimeIndex(h.ldate); return h
def snaps(sym):
    h=h1(sym); g=lambda hm,f: h[h.hm==hm].set_index('ld')[f]
    return pd.DataFrame({'p0730':g('06:30','c'),'p0830':g('07:30','c'),'p1230':g('11:30','c')})
q=pd.read_parquet(RES+'/06_q.parquet')
cal=bistcal()
S=snaps('TCELL.IS').reindex(cal)
T=raw('TCELL.IS').reindex(cal)
x=pd.DataFrame(index=cal)
x['o1']=T.o.shift(-1); x['c1']=T.c.shift(-1); x['c0']=T.c
x['p0730_1']=S.p0730.shift(-1); x['p0830_1']=S.p0830.shift(-1)
x['r_oc']=np.log(x.c1/x.o1); x['r_7c']=np.log(x.c1/x.p0730_1); x['r_8c']=np.log(x.c1/x.p0830_1); x['r_o7']=np.log(x.p0730_1/x.o1)
x['g_o']=np.log(x.o1/x.c0); x['g_7']=np.log(x.p0730_1/x.c0); x['g_8']=np.log(x.p0830_1/x.c0)
x=x.join(q[['D','gap1_raw','intra1_raw']])
x=x.loc['2023-12-01':].dropna(subset=['D','r_oc','r_7c'])
for c in ['r_oc','r_7c','r_8c','r_o7']: x.loc[x[c].abs()>0.105,c]=np.nan
x['U_o']=x.D-x.g_o; x['U_7']=x.D-x.g_7; x['U_8']=x.D-x.g_8
print('n gün',len(x), x.index.min().date(), x.index.max().date())
for y,xs in [('r_oc',['D']),('r_7c',['D']),('r_8c',['D']),('r_o7',['D']),('r_7c',['D','g_7']),('r_7c',['U_7']),('r_8c',['U_8'])]:
    m,n=ols(x[y],x[xs]); print(f'  {y} ~ {xs}: '+'  '.join(f'{c} {m.params[c]:+.3f}({m.tvalues[c]:+.2f})' for c in xs)+f' n {n}')
print('== Giriş zamanı x sinyal, 8 bps (aynı günler):')
for nm,sig,y in [('D, açılış (MOO)',x.D,x.r_oc),('U_open, açılış',x.U_o,x.r_oc),('D, 07:30',x.D,x.r_7c),('U_open, 07:30',x.U_o,x.r_7c),('U_0730, 07:30',x.U_7,x.r_7c),('D, 08:30',x.D,x.r_8c),('U_0830, 08:30',x.U_8,x.r_8c)]:
    for thr in [0,0.005]:
        r,_=bt(sig,y,thr,8); print(f'  {nm:18s} |s|>{thr*1e4:.0f}: n {r["n"]} {r["mean"]:+.1f} bps t {r["t"]:+.2f} Sh {r["sh"]:+.2f}')
# ---- saatlik alt iddia: tk_post
K=h1('TKC'); Kd=raw('TKC')
k1530=K[K.hm=='15:30'].set_index('ld').o
tk_post=np.log(Kd.c/k1530).rename('tk_post')
E=h1('ES=F'); 
# ES: 15:30 UTC fiyatı ve 20:00/21:00 (TKC kapanış saatine yakın) -> bar o @15:00 ve 15:30 ; ES kapanış ~ 20:00/21:00 bar
def snapat(H,hm,f='o'): return H[H.hm==hm].set_index('ld')[f]
es1530=snapat(E,'15:00','c'); es20=snapat(E,'20:00','o'); es19=snapat(E,'19:00','c')
es_post=np.log(es19/es1530).rename('es_post')  # 16:00->20:00 UTC (her iki mevsimde ABD seansı içinde)
try:
    U_=h1('TUR'); tur_post=np.log(raw('TUR').c/U_[U_.hm=='15:30'].set_index('ld').o).rename('tur_post')
except Exception as ex: tur_post=pd.Series(dtype=float,name='tur_post'); print('TUR h1 yok',ex)
z=x.join(tk_post.reindex(x.index)).join(es_post.reindex(x.index)).join(tur_post.reindex(x.index))
z.loc[z.tk_post.abs()>0.15,'tk_post']=np.nan
print('== Saatlik alt iddia: TCELL 07:30->kapanış(t+1) ~ tk_post_t')
for xs in [['tk_post'],['tk_post','es_post'],['tk_post','tur_post'],['tk_post','D'],['tk_post','g_7'],['tk_post','es_post','g_7']]:
    m,n=ols(z.r_7c,z[xs]); print(f'  {xs}: '+'  '.join(f'{c} {m.params[c]:+.3f}({m.tvalues[c]:+.2f})' for c in xs)+f' n {n}')
for lab,s,e in [('2023-12..2024','2023-12','2024-12-31'),('2025','2025','2025-12-31'),('2026','2026','2026-12-31')]:
    w=z.loc[s:e]; m,n=ols(w.r_7c,w[['tk_post']]); print(f'  {lab}: b {m.params.tk_post:+.3f} t {m.tvalues.tk_post:+.2f} n {n}')
# gap tk_post'u fiyatlıyor mu
m,n=ols(z.g_o,z[['tk_post']]); print(f'  gap(open) ~ tk_post: {m.params.tk_post:+.3f} ({m.tvalues.tk_post:+.2f})')
m,n=ols(z.g_7,z[['tk_post']]); print(f'  gap(07:30) ~ tk_post: {m.params.tk_post:+.3f} ({m.tvalues.tk_post:+.2f})')
for thr in [0,0.005]:
    r,_=bt(z.tk_post,z.r_7c,thr,8); r2,_=bt(z.tk_post,z.r_7c,thr,15); print(f'  BT tk_post |>{thr*1e4:.0f}| -> 07:30 giriş: n {r["n"]} {r["mean"]:+.1f} bps Sh {r["sh"]:+.2f} | 15bps {r2["mean"]:+.1f} Sh {r2["sh"]:+.2f}')
# plasebo: diğer hedefler 07:30->kapanış
for sym in ['XU100.IS','XU030.IS','TTKOM.IS']:
    try:
        S2=snaps(sym).reindex(cal); T2=raw(sym).reindex(cal)
        y=np.log(T2.c.shift(-1)/S2.p0730.shift(-1)).reindex(z.index); y[y.abs()>0.105]=np.nan
        m,n=ols(y,z[['tk_post']]); m2,_=ols(y,z[['D']]); print(f'  plasebo {sym} 07:30->kapanış ~ tk_post: {m.params.tk_post:+.3f} ({m.tvalues.tk_post:+.2f}); ~ D: {m2.params.D:+.3f} ({m2.tvalues.D:+.2f}) n {n}')
    except Exception as ex: print(sym,ex)
z.to_parquet(RES+'/07_intraday.parquet')
