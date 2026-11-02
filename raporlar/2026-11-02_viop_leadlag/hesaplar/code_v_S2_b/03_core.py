import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
df=pd.read_parquet(RES+'/02_daily.parquet'); df=df.loc['2014':]
PER=[('ALL','2014','2026-12-31'),('IS','2014','2020-12-31'),('OOS','2021','2026-12-31')]
def reg(y,xs,d=df,filt='D'):
    rows=[]
    for lab,s,e in PER:
        z=d.loc[s:e]; z=z[z[filt].abs()<0.15]
        m,n=ols(z[y],z[xs])
        rows.append(f"{lab}: "+"  ".join(f"{x} {m.params[x]:+.3f} (t {m.tvalues[x]:.2f})" for x in xs)+f"  n {n}")
    return rows
print('== İddia replikasyonu: intra_{t+1} ~ D_t + gap_{t+1}'); [print(' ',r) for r in reg('intra1',['D','gap1'])]
print('== Mekanik-temiz: intra_{t+1} ~ D_t (gap kontrolü YOK)'); [print(' ',r) for r in reg('intra1',['D'])]
print('== gap_{t+1} ~ D_t'); [print(' ',r) for r in reg('gap1',['D'])]
print('== cc_{t+1} ~ D_t (açılış gürültüsünden bağımsız toplam)'); [print(' ',r) for r in reg('cc1',['D'])]
print('== intra_{t+1} ~ gap_{t+1} (kendi gap fade / açılış gürültüsü)'); [print(' ',r) for r in reg('intra1',['gap1'])]
print('== D tanım varyantları, intra1 ~ D (gap yok) ve D+gap')
for Dv in ['D_fx0','D_fx1','D_fx2','Draw']:
    for xs in ([Dv],[Dv,'gap1']):
        print(' ',Dv,xs, reg('intra1',xs,filt=Dv))
# Mekanik yanlılık hesaplaması: b_D(gap'li) = b_D(gapsız) + b_gap * a ; a = gap1~D katsayısı
z=df[df.D.abs()<0.15]
m1,_=ols(z.intra1,z[['D','gap1']]); m0,_=ols(z.intra1,z[['D']]); ma,_=ols(z.gap1,z[['D']])
print('Ayrıştırma (ALL): b_D|gap =',round(m1.params.D,3),' b_D(tek) =',round(m0.params.D,3),' b_gap =',round(m1.params.gap1,3),' a(gap~D) =',round(ma.params.D,3),
      ' => b_D|gap - b_D = -b_gap*a =',round(-m1.params.gap1*ma.params.D,3))
# kontrol: intra1 ~ D + gap1 + kendi lag + XU100 gap1 + XU100 intra lag
print('== kontrollü: intra1 ~ D + gap1 + xu_gap1 + intra + cc + xu_cc'); [print(' ',r) for r in reg('intra1',['D','gap1','xu_gap1','intra','cc','xu_cc'])]
print('== kontrollü (gap yok): intra1 ~ D + xu_gap1 + intra + cc + xu_cc'); [print(' ',r) for r in reg('intra1',['D','xu_gap1','intra','cc','xu_cc'])]
# hisseye özgü hedef: intra1 - beta*xu_intra1 (beta IS'ten değil tüm dönem; ayrıca rolling)
zz=df[['intra1','xu_intra1']].dropna(); beta=np.polyfit(zz.xu_intra1,zz.intra1,1)[0]
df['res1']=df.intra1-beta*df.xu_intra1
print('beta(TCELL intra ~ XU100 intra)=',round(beta,3))
print('== hisseye özgü: res1 ~ D'); [print(' ',r) for r in reg('res1',['D'])]
print('== hisseye özgü: res1 ~ D + gap1 + xu_gap1'); [print(' ',r) for r in reg('res1',['D','gap1','xu_gap1'])]
# yıllık b_D (gap yok) ve (gap var)
print('== Yıllara göre b_D (t): tek D | D+gap1')
for y in range(2014,2027):
    z=df.loc[str(y)]; z=z[z.D.abs()<0.15]
    a,_=ols(z.intra1,z[['D']]); b,_=ols(z.intra1,z[['D','gap1']])
    print(f'  {y}: {a.params.D:+.3f} ({a.tvalues.D:+.2f}) | {b.params.D:+.3f} ({b.tvalues.D:+.2f})  sdD {1e4*z.D.std():.0f}bps')
