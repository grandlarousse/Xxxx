# T11: h1 bar zaman damgası/bitiş varsayımını m5 ile doğrula; ABD nakit enstrümanlarının 15:00 UTC snap kapsamı (yaz/kış)
import warnings; warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
B='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
for s in ['THYAO.IS','XU030.IS','GARAN.IS','ES=F','TUR','BZ=F']:
    h=pd.read_parquet(f'{B}/h1/{s}.parquet').sort_index(); m=pd.read_parquet(f'{B}/m5/{s}.parquet').sort_index()
    m=m[m.index>=h.index.max()-pd.Timedelta(days=55)]
    mc=pd.Series(m['c'].values,index=m.index+pd.Timedelta(minutes=5))  # m5 bar sonu
    hh=h[h.index>=m.index[0]]
    res={}
    for assume in [0,30,60]:
        tgt=hh.index+pd.Timedelta(minutes=assume)
        pos=mc.index.searchsorted(tgt,side='right')-1; px=mc.values[np.clip(pos,0,None)]
        res[assume]=np.mean(np.abs(np.log(hh['c'].values/px))<1e-5)
    # h1 bar sonu için en iyi eşleşme süresi
    print(f"{s:9s} h1 c == m5 fiyatı (bar başlangıcı + X dk) oranı: X=0:{res[0]:.2f} X=30:{res[30]:.2f} X=60:{res[60]:.2f} | h1 dakika damgaları: {sorted(set(hh.index.minute))} saatler: {sorted(set(hh.index.hour))}")
# ABD nakit: 15:00 UTC'ye kadar kapanmış bar var mı (aylara göre)
for s in ['TUR','SPY','JETS','TKC','EEM']:
    try: h=pd.read_parquet(f'{B}/h1/{s}.parquet').sort_index()
    except Exception: continue
    end=h.index+pd.Timedelta(hours=1)
    days=pd.DatetimeIndex(h.index.normalize().unique())
    ok=[]
    for d in days:
        e=end[(end>d)&(end<=d+pd.Timedelta(hours=15))]
        ok.append(len(e)>0)
    ok=pd.Series(ok,index=days)
    print(s,'15:00 UTC snap mevcut oranı aylara göre:',ok.groupby(ok.index.month).mean().round(2).to_dict())
