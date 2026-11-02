"""Bayat sinyal plasebosunun ayrıştırılması + permütasyon null'ları + ortak faktör."""
import numpy as np, pandas as pd, vlib as v
rng=np.random.default_rng(7)
A=pd.read_parquet(v.RES+'/panel.parquet')
XU=A[A.sym=='XU030'].set_index('date'); S=A[A.sym!='XU030'].sort_values(['sym','date']).copy()
S['CA_n']=S.groupby('sym')['CA'].shift(-1); S['CA_l1']=S.groupby('sym')['CA'].shift(1)
S['y_l1']=S.groupby('sym')['y'].shift(1)
# CA otokorelasyonu
d=S[['CA','CA_n','date']].dropna(); b,se=v.ols_cl(d['CA_n'],d[['CA']],d['date']); print('CA_{t+1} ~ CA_t: b %.3f (t %.1f), corr %.3f'%(b[1],b[1]/se[1],d[['CA','CA_n']].corr().iloc[0,1]))
Z=v.demean2(d.assign(sym=S.loc[d.index,'sym']),['CA','CA_n']); print('  hisse+gün FE sonrası corr %.3f'%Z.corr().iloc[0,1])
print('Hisse ortalama CA (bps) dağılımı:', (S.groupby('sym')['CA'].mean()*1e4).describe().round(1).to_dict())
# y_n2 ~ CA_t + CA_{t+1}
d=S[['y_n2','CA','CA_n','date','sym']].dropna()
for xs in [['CA'],['CA','CA_n']]:
    b,se=v.ols_cl(d['y_n2'],d[xs],d['date']); Z=v.demean2(d,['y_n2']+xs); b2,se2=v.ols_cl(Z['y_n2'],Z[xs],d['date'])
    print('y_n2 ~',xs,' ham:',[f'{b[i+1]:+.3f}(t{b[i+1]/se[i+1]:+.1f})' for i in range(len(xs))],' FE:',[f'{b2[i+1]:+.3f}(t{b2[i+1]/se2[i+1]:+.1f})' for i in range(len(xs))])
# baz y ~ CA_t + CA_{t-1}
d=S[['y','CA','CA_l1','date','sym']].dropna()
b,se=v.ols_cl(d['y'],d[['CA','CA_l1']],d['date']); print('y ~ CA_t + CA_{t-1}:',f'{b[1]:+.3f}(t{b[1]/se[1]:+.1f}) {b[2]:+.3f}(t{b[2]/se[2]:+.1f})')
# bayat sinyal portföyü, CA_t ile aynı yönde olmayan alt küme
W=S[S.CA_l1.notna()&S.CA.notna()]
for lab,m in [('CA_t ve CA_{t-1} aynı işaret',np.sign(W.CA)==np.sign(W.CA_l1)),('ters işaret',np.sign(W.CA)!=np.sign(W.CA_l1)),('|CA_t|<5bps',W.CA.abs()<5e-4)]:
    dd,x=v.port(W[m],'CA_l1','y',0.0025); print('bayat sinyal portföyü,',lab,v.summ(dd,x))
# hisse sabit etkili (dışarıda bırakılmış) portföy: y - hissenin (o gün hariç) ortalama y'si
S['y_dm']=S['y']-(S.groupby('sym')['y'].transform('sum')-S['y'])/(S.groupby('sym')['y'].transform('count')-1)
W=S[S.CA.notna()]
print('hisse-ortalama arındırılmış y ile portföy |CA|>25:',v.summ(*v.port(W,'CA','y_dm',0.0025)))
# genişleyen (yalnız geçmiş) hisse ortalaması
S['mu_past']=S.groupby('sym')['y'].transform(lambda x:x.shift(1).expanding(20).mean())
S['y_dmp']=S['y']-S['mu_past']; W=S[S.CA.notna()]
print('geçmiş hisse ortalaması arındırılmış:',v.summ(*v.port(W,'CA','y_dmp',0.0025)))
# Uzun/kısa bacaklar ve net yön
dd,x=v.port(W,'CA','y',0.0025)
print('işlem payı uzun (CA<0): %.2f'%(x.CA<0).mean(), ' gün başı net uzun oran medyan', x.groupby('date').apply(lambda g:(-np.sign(g.CA)).mean()).median())
for side in ['long','short']:
    for ex in [False,True]:
        print(side,'excess' if ex else 'ham',v.summ(*v.port(W,'CA','y',0.0025,excess=ex,side=side)))
# ortak faktör: günlük P&L ~ XU030 C->07:30
pnl=dd; xu=XU['y'].reindex(pnl.index); csm=S.groupby('date')['y'].mean().reindex(pnl.index)
for nm,f in [('XU030 y',xu),('kesit ort. y',csm)]:
    m=pd.concat([pnl,f],axis=1).dropna(); b,se=v.ols_cl(m.iloc[:,0],m.iloc[:,[1]],np.arange(len(m))//5)
    print(f'P&L ~ {nm}: alfa {1e4*b[0]:.1f} bps (t {b[0]/se[0]:.1f}), beta {b[1]:+.3f} (t {b[1]/se[1]:.1f})')
# PERMÜTASYON null'ları (|CA|>25, ham ve excess)
W=S[S.CA.notna()].copy()
obs={ex:v.summ(*v.port(W,'CA','y',0.0025,excess=ex))['bps'] for ex in [False,True]}
mu=W.groupby('date')['y'].transform('mean'); W['yx']=W['y']-mu
def pstat(ca,yy,dates):
    m=np.abs(ca)>0.0025; m&=~np.isnan(yy)&~np.isnan(ca)
    p=pd.Series(-np.sign(ca[m])*yy[m]).groupby(dates[m]).mean(); return 1e4*p.mean()
dates=W['date'].values; ca=W['CA'].values
res={'time':[], 'xsec':[]}
gi=W.groupby('sym').indices; di=W.groupby('date').indices
for k in range(500):
    c1=ca.copy()
    for s,ix in gi.items(): c1[ix]=ca[rng.permutation(ix)]   # hisse içinde tarih karıştırma
    res['time'].append((pstat(c1,W['y'].values,dates),pstat(c1,W['yx'].values,dates)))
    c2=ca.copy()
    for dt,ix in di.items(): c2[ix]=ca[rng.permutation(ix)]  # gün içinde hisse karıştırma (rastgele çift)
    res['xsec'].append((pstat(c2,W['y'].values,dates),pstat(c2,W['yx'].values,dates)))
for k,vv in res.items():
    a=np.array(vv)
    for j,ex in enumerate([False,True]):
        print(f'perm {k:5s} {"excess" if ex else "ham   "}: null ort {a[:,j].mean():+.1f}, %95 {np.percentile(a[:,j],95):+.1f}, %99 {np.percentile(a[:,j],99):+.1f}, max {a[:,j].max():+.1f}; gözlenen {obs[ex]:+.1f}; p={(a[:,j]>=obs[ex]).mean():.3f}')
