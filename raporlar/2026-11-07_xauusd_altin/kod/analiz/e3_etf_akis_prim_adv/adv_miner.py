"""E3-1 / E3-2 saldırısı: m_t (altın 16:00 ET t-1 -> 15:00 ET t) -> GDXJ/GDX ertesi gün.
Kontroller: yeniden üretim, alt dönemler, örtüşmesiz OLS, parametre duyarlılığı (kesim saati, çapa, eşik),
B&H'ye göre alfa, gece/gün-içi ayrışımı, kendi-dönüş kontrolü, yüksek maliyet, 15:00 ET girişli uygulama (saatlik, son 2 yıl)."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
from common import *
import statsmodels.api as sm
d=load_etf()
m=np.log(d.xau_cut/d.xau_close.shift(1))
x=pd.read_parquet(f"{P}/duka/XAUUSD.parquet")["c"]; x.index=(x.index+pd.Timedelta(hours=1)).tz_convert("America/New_York")
def xat(hh):
    s=x[(x.index.hour==hh)&(x.index.minute==0)]; s.index=pd.to_datetime(s.index.date); return s[~s.index.duplicated()].reindex(d.index)
X={hh:xat(hh) for hh in (10,11,12,13,14,15,16)}
print("check xau_cut==X15:", np.nanmax(np.abs(np.log(X[15]/d.xau_cut))))
def rep(nm,x_,y_,h=1):
    q=ic(x_,y_,max(h,5)); return f"{nm}: IC {q['ic']:.3f} t {q['t']:.2f} n {q['n']}"
for tgt in ["GDXJ","GDX"]:
    r=lr(d[f"c_{tgt}"]); y1=fwd(r,1)
    print("=====",tgt)
    print(rep("full m15",m,y1))
    # alt dönemler
    for a,b in [("2008","2012"),("2013","2017"),("2018","2021"),("2022","2026")]:
        print(" ",a,b,rep("",m[a:b],y1[a:b]))
    # Pearson vs Spearman, düz OLS (h=1 örtüşmesiz)
    dd=pd.concat([m.rename("m"),y1.rename("y")],axis=1).dropna()
    o=sm.OLS(dd.y,sm.add_constant(dd.m)).fit(); oh=sm.OLS(dd.y,sm.add_constant(dd.m)).fit(cov_type="HC1")
    print("  OLS beta",round(o.params.m,3),"t",round(o.tvalues.m,2),"HC t",round(oh.tvalues.m,2),"Pearson",round(dd.m.corr(dd.y),3))
    # winsorize m ve y (uç gözlemler)
    q1,q99=dd.m.quantile([.01,.99]); yq1,yq99=dd.y.quantile([.01,.99])
    dw=dd.assign(m=dd.m.clip(q1,q99),y=dd.y.clip(yq1,yq99))
    ow=sm.OLS(dw.y,sm.add_constant(dw.m)).fit(cov_type="HC1"); print("  winsor 1/99 OLS t",round(ow.tvalues.m,2))
    # parametre duyarlılığı: kesim saati
    for hh in (10,11,12,13,14,15):
        mm=np.log(X[hh]/d.xau_close.shift(1)); print("  cut",hh,rep("",mm,y1),"| OOS",rep("",mm["2018":],y1["2018":]))
    # çapa: t-1 15:00 ET (kesimden kesime) ve t-1 16:00
    mc=np.log(d.xau_cut/d.xau_cut.shift(1)); print("  anchor cut->cut",rep("",mc,y1),"| OOS",rep("",mc["2018":],y1["2018":]))
    # son saat (t-1 15->16) bileşeni ayrı
    lh=np.log(d.xau_close/d.xau_cut).shift(1); print("  t-1 last hour gold",rep("",lh,y1))
    # kendi dönüşü: r_t (kapanış, ulaşılamaz) kontrol
    X2=pd.concat([m.rename("m"),r.rename("r_t"),y1.rename("y")],axis=1).dropna()
    o2=sm.OLS(X2.y,sm.add_constant(X2[["m","r_t"]])).fit(cov_type="HC1"); print("  y~m+r_t (tanı):",o2.params.round(3).to_dict(),o2.tvalues.round(2).to_dict())
    o3=sm.OLS(X2.y,sm.add_constant(X2[["r_t"]])).fit(cov_type="HC1"); print("  y~r_t:",o3.params.round(3).to_dict(),o3.tvalues.round(2).to_dict())
    # gece/gün-içi ayrışımı (ham open/close; adj faktörü ile)
    g=pd.read_parquet(f"{P}/yahoo/{tgt}.parquet"); g.index=pd.to_datetime(g.index); g=g.reindex(d.index)
    fac=g.adjclose/g.close; on=np.log(g.open*fac/(g.adjclose.shift(1))); idy=np.log(g.close/g.open)
    for nm,yy in [("overnight t+1",on.shift(-1)),("intraday t+1",idy.shift(-1))]:
        print("  ",nm,rep("",m,yy),"| OOS",rep("",m["2018":],yy["2018":]))
