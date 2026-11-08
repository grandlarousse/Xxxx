"""E3-1 uygulanabilirlik: Midas'ta MOC yok. Sinyal 14:00/15:00 ET, giriş 15:30 ET (saatlik bar 14:30 kapanışı) ve çıkış ertesi gün 15:30 ET;
aynı günlerde 16:00->16:00 ile karşılaştır. 5 dk (60 gün): 15:50 girişli. Ayrıca son 30 dk'nın m_t'ye koşullu ortalaması (kayma)."""
import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e3_etf_akis_prim")
from common import *
d=load_etf()
m=np.log(d.xau_cut/d.xau_close.shift(1))
x=pd.read_parquet(f"{P}/duka/XAUUSD.parquet")["c"]; x.index=(x.index+pd.Timedelta(hours=1)).tz_convert("America/New_York")
x14=x[(x.index.hour==14)&(x.index.minute==0)]; x14.index=pd.to_datetime(x14.index.date); x14=x14[~x14.index.duplicated()].reindex(d.index)
m14=np.log(x14/d.xau_close.shift(1))
for t in ["GDXJ","GDX"]:
    g=pd.read_parquet(f"{P}/yahoo_h/{t}.parquet"); g.index=g.index.tz_convert("America/New_York")
    g=g[(g.index.hour*100+g.index.minute>=930)&(g.index.hour*100+g.index.minute<1600)]
    def barclose(hhmm):
        s=g[(g.index.hour*100+g.index.minute)==hhmm]["close"]; s.index=pd.to_datetime(s.index.date); return s[~s.index.duplicated()].reindex(d.index)
    p1530=barclose(1430); p1600=barclose(1530)
    yl=pd.read_parquet(f"{P}/yahoo/{t}.parquet"); yl.index=pd.to_datetime(yl.index); cl=yl["close"].reindex(d.index)
    ok=p1530.notna()&cl.notna()
    r1530=np.log(p1530/p1530.shift(1)); r16=np.log(cl/cl.shift(1))
    last30=np.log(cl/p1530)
    for nm,sig in [("m15",m),("m14",m14)]:
        L=(sig<0).astype(float).where(sig.notna())
        out={}
        for lab,rr in [("15:30->15:30",r1530.shift(-1)),("16:00->16:00",r16.shift(-1))]:
            dd=pd.concat([L.rename("L"),rr.rename("y")],axis=1)[ok].dropna()
            a=dd.y[dd.L==1]; b=dd.y[dd.L==0]
            out[lab]=(round(a.mean()*1e4,1),round(b.mean()*1e4,1),round((a.mean()-b.mean())/np.sqrt(a.var()/len(a)+b.var()/len(b)),2),len(dd))
            q=ic(sig[ok],rr[ok],5); out[lab+"_IC"]=(round(q["ic"],3),round(q["t"],2))
        dd=pd.concat([L.rename("L"),last30.rename("y")],axis=1)[ok].dropna()
        out["son30dk(15:30->16:00) uzun gün/nakit gün bps"]=(round(dd.y[dd.L==1].mean()*1e4,1),round(dd.y[dd.L==0].mean()*1e4,1))
        print(t,nm,out)
# 5 dk: 15:50 giriş
for t in ["GDXJ","GDX"]:
    g=pd.read_parquet(f"{P}/yahoo_5m/{t}.parquet"); g.index=g.index.tz_convert("America/New_York")
    s=g[(g.index.hour==15)&(g.index.minute==45)]["close"]; s.index=pd.to_datetime(s.index.date); p1550=s[~s.index.duplicated()].reindex(d.index)
    yl=pd.read_parquet(f"{P}/yahoo/{t}.parquet"); yl.index=pd.to_datetime(yl.index); cl=yl["close"].reindex(d.index)
    L=(m<0).astype(float).where(m.notna())
    dd=pd.concat([L.rename("L"),np.log(cl/p1550).rename("y")],axis=1).dropna()
    print(t,"5dk son 10 dk (15:50->16:00) uzun/nakit bps:",round(dd.y[dd.L==1].mean()*1e4,1),round(dd.y[dd.L==0].mean()*1e4,1),"n",len(dd))
