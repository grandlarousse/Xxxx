"""E3-3/E3-4 saldırısı: PHYS/GLD ve CEF artık sapması. Durağan (stale) fiyat günleri, sinyali 1-3 gün eskitme (bounce kontrolü),
örtüşmesiz h=5 OLS, alt dönemler, eşik/k duyarlılığı, 'araç seçimi' kazancının gerçekçi spread sonrası büyüklüğü."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
from common import *
import statsmodels.api as sm
d=load_etf()
rP=lr(d.c_PHYS); rG=lr(d.c_GLD); rC=lr(d.c_CEF); rS=lr(d.c_SLV); rPS=lr(d.c_PSLV)
# stale kontrol
st=(rP==0)&(rG.abs()>0.01); print("PHYS sıfır getiri & |GLD|>1% gün sayısı:",int(st.sum()), [str(i.date()) for i in st[st].index[:10]])
st2=(rC==0)&(rG.abs()>0.01); print("CEF sıfır getiri & |GLD|>1%:",int(st2.sum()))
def rolling_beta_resid(y, X, win=250):
    dd=pd.concat([y.rename("y"),X],axis=1).dropna(); out=pd.Series(np.nan,index=dd.index)
    Y=dd.y.values; XX=np.column_stack([np.ones(len(dd)),dd.iloc[:,1:].values])
    for i in range(win,len(dd)):
        b=np.linalg.lstsq(XX[i-win:i],Y[i-win:i],rcond=None)[0]; out.iloc[i]=Y[i]-XX[i,1:]@b[1:]
    return out
eC=rolling_beta_resid(rC,pd.concat([rG.rename("g"),rS.rename("s")],axis=1)).reindex(d.index)
pairs={"PHYS-GLD":(np.log(d.c_PHYS/d.c_GLD),rP-rG),"PSLV-SLV":(np.log(d.c_PSLV/d.c_SLV),rPS-rS),"CEF-mix":(eC.fillna(0).cumsum().where(eC.notna()),eC)}
for nm,(lvl,sp) in pairs.items():
    print("=====",nm)
    for k in (20,60,120):
        dev=lvl-lvl.rolling(k,min_periods=k//2).median(); z=dev/dev.rolling(250,min_periods=120).std()
        for lag in (1,2,3,5):
            y5=fwd(sp,5); q=ic(z.shift(lag),y5,5)
            # örtüşmesiz (her 5. gün) düz OLS
            dd=pd.concat([z.shift(lag).rename("z"),y5.rename("y")],axis=1).dropna().iloc[::5]
            o=sm.OLS(dd.y,sm.add_constant(dd.z)).fit(cov_type="HC1")
            print(f"  k{k} lag{lag} h5: IC {q['ic']:.3f} t {q['t']:.2f} | örtüşmesiz OLS t {o.tvalues.z:.2f} b(bps/z) {o.params.z*1e4:.1f} n {len(dd)}")
    dev=lvl-lvl.rolling(60,min_periods=30).median(); z=(dev/dev.rolling(250,min_periods=120).std()).shift(1); y5=fwd(sp,5)
    for a,b in [("2008","2012"),("2013","2017"),("2018","2021"),("2022","2026")]:
        q=ic(z[a:b],y5[a:b],5)
        g=pd.concat([z[a:b].rename("z"),y5[a:b].rename("y")],axis=1).dropna()
        lo=g.y[g.z<-1.5].mean()*1e4; hi=g.y[g.z>1.5].mean()*1e4
        print(f"  {a}-{b} k60 h5: IC {q['ic']:.3f} t {q['t']:.2f} n {q['n']} | z<-1.5: {lo:.1f} bps (n {(g.z<-1.5).sum()}), z>1.5: {hi:.1f} bps")
# Roll spread tahmini (PHYS, GLD tekil): 2*sqrt(-cov(r_t,r_t-1)) — kapanış fiyat gürültüsü üst sınırı
for t in ["PHYS","GLD","CEF","PSLV","GDXJ"]:
    r=lr(d[f"c_{t}"])
    for a,b in [("2010","2017"),("2018","2026")]:
        rr=r[a:b].dropna(); cv=rr.cov(rr.shift(1))
        print(t,a,b,"Roll spread bps:", round(2*np.sqrt(-cv)*1e4,1) if cv<0 else "cov>0")
# PHYS tick: medyan fiyat
for a,b in [("2010","2017"),("2018","2026")]:
    y=pd.read_parquet(f"{P}/yahoo/PHYS.parquet"); y.index=pd.to_datetime(y.index); p=y.close[a:b].median()
    print("PHYS medyan fiyat",a,b,round(p,2),"1 cent =",round(0.01/p*1e4,1),"bps")
