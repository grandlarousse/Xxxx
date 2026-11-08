"""E3-1 mekanizma saldırısı (tanı, işlem dışı): kaldıraçlı ETF dengelemesi gün t'nin TAM getirisiyle orantılı.
Eğer mekanizma bu ise tam gün altın hareketi (16->16) ve madencinin kendi r_t'si m_t'den güçlü olmalı. Rank (Spearman) at yarışı."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
from common import *
import statsmodels.api as sm
d=load_etf()
m=np.log(d.xau_cut/d.xau_close.shift(1)); mfull=np.log(d.xau_close/d.xau_close.shift(1)); lasth=np.log(d.xau_close/d.xau_cut)
for tgt,lev in [("GDXJ",["JNUG","JDST"]),("GDX",["NUGT","DUST"])]:
    r=lr(d[f"c_{tgt}"]); y=r.shift(-1)
    print("=====",tgt)
    for nm,s in [("m_t (15ET)",m),("mfull (16->16, tanı)",mfull),("lasthour t (tanı)",lasth),("r_t own (tanı)",r)]:
        for per in [("2009","2026"),("2018","2026")]:
            q=ic(s[per[0]:per[1]],y[per[0]:per[1]],5); print(f"  {nm} {per}: IC {q['ic']:.3f} t {q['t']:.2f}")
    # rank at yarışı
    dd=pd.concat([m.rename("m"),r.rename("r"),mfull.rename("mf"),y.rename("y")],axis=1).dropna().rank()
    dd=(dd-dd.mean())/dd.std()
    for cols in [["m","r"],["mf","r"],["m","mf"]]:
        o=sm.OLS(dd.y,sm.add_constant(dd[cols])).fit(cov_type="HAC",cov_kwds={"maxlags":5})
        print("  rank reg y ~",cols,o.params[cols].round(3).to_dict(),o.tvalues[cols].round(2).to_dict())
    # kaldıraçlı ETF dolar hacmi (t-1, proxy AUM aktivitesi) yüksek/düşük dönemlerde IC
    vv=sum(d[f"y_{l}_vol"].fillna(0)*d[f"y_{l}"].fillna(0) for l in lev)
    vrel=(vv/vv.rolling(250,min_periods=100).median()).where(vv>0)
    zz=pd.concat([m.rename("m"),y.rename("y"),vrel.rename("v")],axis=1).dropna()
    zz["hi"]=zz.v>zz.v.rolling(500,min_periods=100).median().shift(1)
    for k,g in zz.groupby("hi"):
        q=ic(g.m,g.y,5); print("  LETF $hacim göreli yüksek" if k else "  LETF $hacim göreli düşük",f"IC {q['ic']:.3f} t {q['t']:.2f} n {q['n']}")
