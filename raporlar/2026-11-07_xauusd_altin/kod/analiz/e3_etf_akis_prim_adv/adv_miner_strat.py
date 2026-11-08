"""E3-1/E3-2 strateji saldırısı: B&H'ye göre alfa, maliyet ızgarası, alt dönem Sharpe, bootstrap (rastgele %47 maruziyet), eşik duyarlılığı,
15:30 ET giriş/çıkışlı uygulama (Yahoo saatlik, son ~2 yıl) ve yarım günler."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
from common import *
import statsmodels.api as sm
d=load_etf()
m=np.log(d.xau_cut/d.xau_close.shift(1))
zm=m/m.rolling(60,min_periods=40).std().shift(1)
rng=np.random.default_rng(0)
for tgt in ["GDXJ","GDX","JNUG","NUGT"]:
    r=lr(d[f"c_{tgt}"]).dropna(); R=np.expm1(r)
    pos=(m<0).astype(float).where(m.notna(),0.0)
    print("=====",tgt)
    for c in (0,10,20,30,40):
        net,wl,_=bt(pos,r,1,c)
        L=wl.shift(1).reindex(net.index)
        out=[]
        for a,b in [("2008","2012"),("2013","2017"),("2018","2021"),("2022","2026"),("2018","2026")]:
            nn=net[a:b]; bb=R[a:b]; ll=L[a:b]
            if len(nn)<100: out.append((a,b,None)); continue
            # alfa: net ~ a + beta*R (HAC)
            o=sm.OLS(nn,sm.add_constant(bb.reindex(nn.index))).fit(cov_type="HAC",cov_kwds={"maxlags":5})
            sh=nn.mean()/nn.std()*np.sqrt(252); shb=bb.mean()/bb.std()*np.sqrt(252)
            out.append((a,b,round(sh,2),round(shb,2),round(o.params.iloc[0]*252*100,1),round(o.tvalues.iloc[0],2)))
        print(f" cost {c}: (dönem, Sharpe, B&H Sharpe, alfa %/yıl, alfa t):",out)
    # uzun gün − nakit gün fark t (maliyetsiz), OOS
    L=pos.shift(1).reindex(R.index)  # pozisyon t-1 sinyali ile t getirisi
    for a,b in [("2009","2017"),("2018","2026"),("2022","2026")]:
        Ra=R[a:b]; La=L[a:b]
        dlt=Ra[La==1].mean()-Ra[La==0].mean()
        se=np.sqrt(Ra[La==1].var()/(La==1).sum()+Ra[La==0].var()/(La==0).sum())
        print(f"  {a}-{b}: uzun gün ort {Ra[La==1].mean()*1e4:.1f} bps, nakit gün {Ra[La==0].mean()*1e4:.1f} bps, fark t {dlt/se:.2f}")
    # eşik duyarlılığı (yalnız uzun, 10 bps), OOS
    rowz=[]
    for thr in (-1.0,-0.5,-0.25,0.0,0.25,0.5):
        p_=(zm<thr).astype(float).where(zm.notna(),0.0)
        for h in (1,3,5):
            net,wl,_=bt(p_,r,h,10.0 if tgt in("GDXJ","GDX") else 20.0); s=segs(net)
            rowz.append((thr,h,s["is"]["sharpe"],s["oos"]["sharpe"],s["22"]["sharpe"],round(wl.mean(),2)))
    print("  eşik/h ızgarası (thr,h,IS,OOS,22+,maruziyet):",rowz)
# Bootstrap: OOS'ta rastgele %47 maruziyetli 1-gün tutuşlu yalnız-uzun (aynı devir) Sharpe dağılımı vs gerçek
r=lr(d.c_GDXJ).dropna(); R=np.expm1(r); pos=(m<0).astype(float).where(m.notna(),0.0)
net,wl,_=bt(pos,r,1,10.0); real=net["2018":].mean()/net["2018":].std()*np.sqrt(252)
p0=pos.reindex(r.index).fillna(0).values; sims=[]
blk=pos["2018":].reindex(r["2018":].index).fillna(0).values
for i in range(2000):
    perm=rng.permutation(blk)
    pp=pd.Series(perm,index=r["2018":].index)
    nn,_,_=bt(pp,r["2018":],1,10.0); sims.append(nn.mean()/nn.std()*np.sqrt(252))
sims=np.array(sims); print("GDXJ OOS gerçek Sharpe",round(real,2),"permütasyon ort",round(sims.mean(),2),"p(>=gerçek)",round((sims>=real).mean(),4))
