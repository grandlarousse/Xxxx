"""Sahte-OOS (excess), yıllık regresyon eğimleri, SSF uzlaşma->uzlaşma kontrolü, spot maliyet ve kapasite."""
import numpy as np, pandas as pd, vlib as v
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
A=pd.read_parquet(v.RES+'/panel.parquet'); XU=A[A.sym=='XU030'].set_index('date')
S=A[A.sym!='XU030'].sort_values(['sym','date']).copy()
for y in ['gap1','y','y0830','y0930','y1430','cc1']: S[y+'x']=S[y]-S.groupby('date')[y].transform('mean')
S['liq']=S.groupby('sym')['TL'].transform(lambda z:z.shift(1).rolling(60,min_periods=20).median()); S['liqr']=S.groupby('date')['liq'].rank(pct=True)
W=S[S.CA.notna()].copy(); W['yr']=W.date.dt.year
print('== Yıllık eğim (y ~ CA, ham ve 2yönlü FE) ==')
for yr,g in W.groupby('yr'):
    d=g[['y','CA','date','sym']].dropna(); b,se=v.ols_cl(d['y'],d[['CA']],d['date']); Z=v.demean2(d,['y','CA']); b2,se2=v.ols_cl(Z['y'],Z[['CA']],d['date'])
    print(yr,'ham %.3f (t %.1f)  FE %.3f (t %.1f)  gün %d'%(b[1],b[1]/se[1],b2[1],b2[1]/se2[1],d.date.nunique()))
print('\n== Sahte-OOS, excess getirilerle: 2024 yazında seç -> 2025-26 ==')
IS=W[W.yr==2024]; OOS=W[W.yr>=2025]; sc=[]
for thr in [0,10,25,50,75,100]:
    for y in ['gap1x','yx','y0830x','y0930x','y1430x','cc1x']:
        s=v.summ(v.port(IS,'CA',y,thr/1e4)[0]); so=v.summ(v.port(OOS,'CA',y,thr/1e4)[0]); sc.append((s['t'],thr,y,s['bps'],so['bps'],so['t']))
sc.sort(reverse=True)
for r in sc[:5]: print('  IS t %.1f thr %d %s IS %.1f -> OOS %.1f (t %.1f)'%r)
print('  tüm 36 hücrede OOS>0 oranı %.2f, OOS t>2 oranı %.2f'%(np.mean([r[4]>0 for r in sc]),np.mean([r[5]>2 for r in sc])))
# SSF: uzlaşmadan uzlaşmaya (aynı sözleşme)
P=pd.read_parquet(v.RES+'/w7_ssfpanel.parquet')[['date','sym','settle','expiry','ex']]
p=pd.read_parquet(D+'/viop_panel.parquet',columns=['date','root','segment','expiry','settle'])
p=p[p.segment=='SSF'].drop_duplicates(['root','expiry','date'],keep='last'); pdict={(a,b,c):x for a,b,c,x in zip(p.root,p.expiry,p.date,p.settle)}
P=P.merge(W[['date','sym','CA','y','liqr']],on=['date','sym'],how='inner')
# ertesi gün aynı sözleşme uzlaşması
cal=sorted(A.date.unique()); nx=dict(zip(cal[:-1],cal[1:]))
def fnext(r):
    return pdict.get((r.sym, r.expiry, nx.get(r.date)), np.nan)
P['F_n']=[fnext(r) for r in P.itertuples()]
P['fr']=np.log(P['F_n'].astype(float)/P['settle'].astype(float)); P.loc[P.fr.abs()>0.105,'fr']=np.nan
d=P[['fr','CA','date']].dropna(); b,se=v.ols_cl(d['fr'],d[['CA']],d['date'])
print('\nSSF uzlaşma_t -> uzlaşma_{t+1} ~ CA: %.3f (t %.1f) n=%d'%(b[1],b[1]/se[1],len(d)))
print('  SSF dönüş portföyü (|CA|>25, -sign(CA), uzlaşmadan uzlaşmaya):',v.summ(*v.port(P,'CA','fr',0.0025)))
# Spot maliyet modeli: komisyon+ücret 2 bps/taraf, giriş C (spread yok), çıkış 07:30 piyasa emri: h*tik
def tick(p_):
    p_=np.asarray(p_,float); return np.select([p_<20,p_<50,p_<100,p_<250,p_<500,p_<1000,p_<2500],[0.01,0.02,0.05,0.10,0.25,0.50,1.00],2.50)
W['tickb']=1e4*tick(W['C'])/W['C']
print('\n== Spot net (bps/gün, NW t) — maliyet = 4 bps komisyon (2 taraf) + h×tik (çıkışta yarım/tam spread) [+ kısa bacak ödünç 2 bps] ==')
for thr in [25,50,100]:
    for univ,m in [('tümü',W.CA.notna()),('liq alt 2/3',W.liqr<=2/3),('liq üst 1/3',W.liqr>2/3)]:
        out=[]
        for h in [0.5,1.0]:
            for yv in ['y','yx']:
                X=W[m&(W.CA.abs()>thr/1e4)][['date','CA',yv,'tickb']].dropna()
                c=4+h*X.tickb+np.where(X.CA>0,2,0)
                pn=(-np.sign(X.CA)*X[yv]*1e4-c).groupby(X.date).mean(); s=v.summ(pn/1e4)
                out.append(f'h={h} {yv:2s}: {s["bps"]:+.1f} (t {s["t"]:.1f})')
        print(f'|CA|>{thr:3d} {univ:12s} n_işlem/gün {((W[m].CA.abs()>thr/1e4).groupby(W[m].date).sum()).mean():.1f} | ort tik {W[m&(W.CA.abs()>thr/1e4)].tickb.mean():.1f} bps | '+' | '.join(out))
# Kapasite: m5 son 60 gün, (günlük hacim - sürekli işlem hacmi) = açılış+kapanış müzayedesi+kapanış fiyatından işlemler (üst sınır)
rows=[]
for s in W.sym.unique():
    m=pd.read_parquet(f'{D}/m5/{s}.IS.parquet'); m=m[~m.index.duplicated(keep='last')]
    hm=m.index.hour*100+m.index.minute; m=m[(hm>=700)&(hm<=1455)]
    day=pd.DatetimeIndex(m.index.tz_convert(None).normalize()); cv=m['v'].groupby(day).sum()
    d=pd.read_parquet(f'{D}/daily/{s}.IS.parquet'); d.index=pd.DatetimeIndex(d['ldate']); d=d[~d.index.duplicated(keep='last')].reindex(cv.index)
    aux=(d['v']-cv).clip(lower=0)*d['c']; tot=d['v']*d['c']
    rows.append(dict(sym=s,aux_mnTL=aux.median()/1e6,share=(aux/tot).median(),tot_mnTL=tot.median()/1e6))
K=pd.DataFrame(rows).sort_values('tot_mnTL'); K.to_csv(v.RES+'/w8_capacity.csv',index=False)
print('\nMüzayede+KFİ hacmi (üst sınır, m5 60 gün, medyan): tüm hisseler medyan %.1f mn TL/gün, pay %.3f'%(K.aux_mnTL.median(),K.share.median()))
print(K.head(16).round(3).to_string())
