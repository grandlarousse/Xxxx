"""05: Plasebo/çürütme: bayat sinyal, kendi geri dönüş, diğer 46 VİOP hissesi, dairesel kaydırma, rastgele işaret, aykırı değer etkisi."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
df=pd.read_parquet(RES+'/02_daily.parquet')
# Hedef varyantı: (a) benim temizlik (|intra|>10.5% NaN)  (b) ham hedef (yalnız cc/gap temizliği) -> iddia ile aynı
T=raw('TCELL.IS'); T=T[T.v>0].reindex(bistcal()); 
intra_raw=np.log(T.c/T.o); ccr=T.adj/T.adj.shift(1)-1
okc=(ccr.abs()<=0.105)|ccr.isna()
gapr=np.log(T.o*(T.adj/T.c)/T.adj.shift(1)); okg=((np.exp(gapr)-1).abs()<=0.105)|gapr.isna()
df['intra1_raw']=intra_raw.where(okc&okg).shift(-1)
q=df.loc['2014':]; q=q[q.D.abs()<0.15].copy()
q['Dlag']=q.D.shift(1)
PER=[('ALL','2014','2026-12-31'),('IS','2014','2020-12-31'),('OOS','2021','2026-12-31')]
def line(y,xs,z0=q):
    out=[]
    for lab,s,e in PER:
        z=z0.loc[s:e]; m,n=ols(z[y],z[xs]); out.append(f'{lab} {m.params[xs[0]]:+.3f}(t {m.tvalues[xs[0]]:+.2f}, n {n})')
    return ' | '.join(out)
print('Ham hedef (iddia ile aynı temizlik): intra1_raw ~ D+gap1 :',line('intra1_raw',['D','gap1']))
print('Ham hedef: intra1_raw ~ D :',line('intra1_raw',['D']))
print('Benim hedef: intra1 ~ D :',line('intra1',['D']))
print('Bayat sinyal: intra1 ~ D_{t-1} :',line('intra1',['Dlag']))
print('Bayat sinyal ham: intra1_raw ~ D_{t-1} :',line('intra1_raw',['Dlag']))
print('İkisi birlikte: intra1 ~ D + D_{t-1} :',line('intra1',['D','Dlag']))
# kendi geri dönüş
for x in ['cc','gap','intra']:
    print(f'Kendi: intra1 ~ {x}_t :',line('intra1',[x]))
print('D | kendi cc,gap: intra1 ~ D + gap + intra :',line('intra1',['D','gap','intra']))
# Huber robust
import statsmodels.api as sm
for lab,s,e in PER:
    z=q.loc[s:e,['intra1_raw','D']].dropna(); r=sm.RLM(z.intra1_raw,sm.add_constant(z.D),M=sm.robust.norms.HuberT()).fit()
    print(f'Huber RLM {lab}: b {r.params.D:+.3f} t {r.tvalues.D:+.2f}')
# Etkili gözlemleri at (|D*intra| en büyük k gün)
for k in [0,5,10,20,40]:
    z=q[['intra1_raw','D']].dropna(); infl=(z.D*z.intra1_raw).abs().sort_values(ascending=False); zz=z.drop(infl.index[:k])
    r=[]
    for lab,s,e in PER:
        w=zz.loc[s:e]; m,n=ols(w.intra1_raw,w[['D']]); r.append(f'{lab} {m.params.D:+.3f}({m.tvalues.D:+.2f})')
    print(f'En etkili {k} gün hariç:',' | '.join(r), ' atılan ilk 5:', [d.strftime('%Y-%m-%d') for d in infl.index[:min(k,5)]])
# KKM penceresi ve 2018 Ağustos hariç
mask=~(((q.index>='2021-11-15')&(q.index<='2022-01-31'))|((q.index>='2018-08-01')&(q.index<='2018-09-30')))
print('KKM(15.11.21-31.01.22)+Ağu-Eyl 2018 hariç: intra1_raw ~ D :',line('intra1_raw',['D'],q[mask]))
# --- Diğer VİOP hisseleri plasebosu: D_t -> hisse intra_{t+1} (ham ve XU100-arındırılmış)
rows=[]
for s in VIOP:
    try: B=bist(s)
    except Exception as ex: continue
    y=B.intra.shift(-1).reindex(q.index)
    zz=pd.concat([y.rename('y'),q.D,q.xu_intra1],axis=1).dropna()
    if len(zz)<500: continue
    be=np.polyfit(zz.xu_intra1,zz.y,1)[0]; zz['res']=zz.y-be*zz.xu_intra1
    m,n=ols(zz.y,zz[['D']]); m2,_=ols(zz.res,zz[['D']])
    o=zz.loc['2021':]; i=zz.loc[:'2020']
    m3=ols(o.y,o[['D']])[0] if len(o)>200 else None; m4=ols(i.y,i[['D']])[0] if len(i)>200 else None
    rows.append((s,n,round(m.params.D,3),round(m.tvalues.D,2),round(m2.tvalues.D,2),round(m4.tvalues.D,2) if m4 is not None else np.nan,round(m3.tvalues.D,2) if m3 is not None else np.nan))
P=pd.DataFrame(rows,columns=['hisse','n','b','t','t_res','t_IS','t_OOS']).sort_values('t',ascending=False)
P.to_csv(RES+'/05_placebo_stocks.csv',index=False)
print('Diğer hisseler (D -> hisse intra_{t+1}):'); print(P.to_string(index=False))
print('|t|>2 sayısı (TCELL hariç):',int((P[P.hisse!='TCELL'].t.abs()>2).sum()),'/',len(P)-1,'  t_res |t|>2:',int((P[P.hisse!='TCELL'].t_res.abs()>2).sum()))
print('TCELL sırası (t):',list(P.hisse).index('TCELL')+1,' t_res sırası:',list(P.sort_values('t_res',ascending=False).hisse).index('TCELL')+1)
