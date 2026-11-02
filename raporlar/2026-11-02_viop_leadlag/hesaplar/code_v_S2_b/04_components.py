"""04: D'nin bileşenleri ve FX zaman damgası (ileriye bakma) testi, yıllara göre."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
df=pd.read_parquet(RES+'/02_daily.parquet')
df['r_tk']=np.log(df.tk).diff(); df['r_fx']=np.log(df.fx1).diff(); df['r_fx0']=np.log(df.fx0).diff()
df['r_tc']=np.log(df.tc).diff()
df['dP']=df.r_tk+df.r_fx-df.r_tc; df['Lag']=df.D-df.dP
df['r_fx_next']=df.r_fx.shift(-1)   # bar t+2 - bar t+1 : t+1 seansını İÇERİR (doğru konvansiyonda)
q=df.loc['2014':]; q=q[q.D.abs()<0.15]
PER=[('ALL','2014','2026-12-31'),('IS','2014','2020-12-31'),('OOS','2021','2026-12-31'),('2024+','2024','2026-12-31')]
for y,xs in [('intra1',['r_tk','r_fx','r_tc','Lag']),('gap1',['r_tk','r_fx','r_tc','Lag']),('intra1',['dP','Lag']),('res',None)]:
    if y=='res': continue
    print(f'== {y} ~ {xs}')
    for lab,s,e in PER:
        z=q.loc[s:e]; m,n=ols(z[y],z[xs]); print(f'  {lab}: '+'  '.join(f'{x} {m.params[x]:+.3f}({m.tvalues[x]:+.2f})' for x in xs)+f' n {n}')
# FX zaman damgası: r_fx (bar t+1 - bar t) ve r_fx_next (bar t+2 - bar t+1) ile t+1 gün-içi korelasyonu (XU100 ve TCELL), yıllara göre
print('== Yıllara göre corr: [r_fx(t) ~ XU intra(t+1)]  [r_fx_next ~ XU intra(t+1)]  [r_fx ~ XU gap(t+1)]  [r_fx ~ TCELL intra1]  [r_fx_next ~ TCELL intra1]')
for yr in range(2011,2027):
    z=df.loc[str(yr)]
    c=lambda a,b: z[[a,b]].dropna().corr().iloc[0,1]
    print(f'  {yr}: {c("r_fx","xu_intra1"):+.3f}  {c("r_fx_next","xu_intra1"):+.3f}  {c("r_fx","xu_gap1"):+.3f}  {c("r_fx","intra1"):+.3f}  {c("r_fx_next","intra1"):+.3f}')
q.to_parquet(RES+'/04_q.parquet')
