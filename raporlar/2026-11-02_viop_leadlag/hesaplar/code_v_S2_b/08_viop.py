"""08: VİOP F_TCELL (gerçek işlem aracı) bülten verisi: likidite ve D_t -> F_TCELL t+1 açılış->kapanış/uzlaşma getirisi."""
import sys, glob, os; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
rows=[]
for f in sorted(glob.glob(SCR+'/data/viop/viop_*.csv')):
    try:
        with open(f,encoding='windows-1254',errors='replace') as fh:
            lines=fh.read().splitlines()
    except Exception: continue
    if len(lines)<3: continue
    hdr=lines[0].split(';')
    for ln in lines[2:]:
        if ';F_TCELL' not in ln: continue
        p=ln.split(';'); rows.append(dict(zip([h.strip() for h in hdr],p)))
V=pd.DataFrame(rows)
num=['UZLASMA FIYATI','ONCEKI UZLASMA FIYATI','ACILIS FIYATI','EN DUSUK FIYAT','EN YUKSEK FIYAT','KAPANIS FIYATI','AGIRLIKLI ORTALAMA FIYAT','ISLEM HACMI','ISLEM SAYISI','ACIK POZISYON','ACILIS SEANSI FIYATI','ACILIS SEANSI ISLEM HACMI','ACILIS SEANSI ISLEM SAYISI']
for c in num:
    if c in V: V[c]=pd.to_numeric(V[c].str.replace(',','.'),errors='coerce')
V['date']=pd.to_datetime(V.TARIH); V=V[V['SOZLESME KODU'].str.match(r'^F_TCELL\d{4}$')]
V=V.sort_values(['date','ISLEM HACMI']).groupby('date').tail(1).set_index('date')   # en likit kontrat
V.to_parquet(RES+'/08_ftcell.parquet')
y=V.groupby(V.index.year).agg(gun=('ISLEM HACMI','size'),med_hacim_mnTL=('ISLEM HACMI',lambda s:s.median()/1e6),med_islem=('ISLEM SAYISI','median'),
  sifir_hacim_gun=('ISLEM HACMI',lambda s:(s==0).mean()), acilis_seansi_med_islem=('ACILIS SEANSI ISLEM SAYISI','median'))
print('F_TCELL en likit kontrat, yıllık:'); print(y.round(2).to_string())
q=pd.read_parquet(RES+'/06_q.parquet')
T=raw('TCELL.IS')
F=V[(V['ISLEM HACMI']>0)&(V['ACILIS FIYATI']>0)].copy()
F['f_oc']=np.log(F['KAPANIS FIYATI']/F['ACILIS FIYATI']); F['f_os']=np.log(F['UZLASMA FIYATI']/F['ACILIS FIYATI'])
F=F.join(T[['o','c']])
F['spot_oc']=np.log(F.c/F.o); F['fo_vs_so']=1e4*np.log(F['ACILIS FIYATI']/F.o)
F.loc[F.f_oc.abs()>0.105,['f_oc','f_os']]=np.nan
print('corr(F o->c, spot o->c):',round(F[['f_oc','spot_oc']].corr().iloc[0,1],3),' n',F.f_oc.notna().sum())
print('Vadeli açılış / spot açılış farkı (bps, baz dahil) medyan:',round(F.fo_vs_so.median(),1),' IQR',F.fo_vs_so.quantile([.25,.75]).round(1).tolist())
# D_t -> F_TCELL t+1: BIST takviminde t+1 eşle
cal=bistcal(); nxt=pd.Series(cal[1:],index=cal[:-1])
z=pd.DataFrame({'D':q.D}); z['t1']=nxt.reindex(z.index)
for c in ['f_oc','f_os','spot_oc']: z[c]=F[c].reindex(z.t1).values
z=z.dropna(subset=['D','f_oc'])
for lab,s,e in [('ALL','2017','2026-12-31'),('2017-20','2017','2020-12-31'),('2022-26','2022','2026-12-31'),('2023-12+','2023-12','2026-12-31')]:
    w=z.loc[s:e]
    if len(w)<100: continue
    m,n=ols(w.f_oc,w[['D']]); m2,_=ols(w.spot_oc,w[['D']]); m3,_=ols(w.f_os,w[['D']])
    r,p=bt(w.D,w.f_oc,0,8); r5,p5=bt(w.D,w.f_oc,0.005,8)
    print(f'{lab}: F o->c ~ D {m.params.D:+.3f}(t {m.tvalues.D:+.2f}) | F o->uzlaşma {m3.params.D:+.3f}(t {m3.tvalues.D:+.2f}) | spot o->c aynı günler {m2.params.D:+.3f}(t {m2.tvalues.D:+.2f}) n {n}')
    top=p5.sort_values(ascending=False)
    print(f'     BT F_TCELL açılış->kapanış, 8 bps: |D|>0 {r["mean"]:+.1f} bps Sh {r["sh"]:+.2f} (n {r["n"]}); |D|>50 {r5["mean"]:+.1f} bps Sh {r5["sh"]:+.2f} (n {r5["n"]}); en iyi 10 hariç {top.iloc[10:].mean():+.1f}')
