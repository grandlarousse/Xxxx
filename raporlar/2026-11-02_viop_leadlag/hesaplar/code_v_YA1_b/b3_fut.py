# VIOP pay vadelisi bulteniyle dolum gercekciligi (bagimsiz)
import pandas as pd, numpy as np
from blib import *
V=pd.read_parquet(f'{D}/viop_panel.parquet')
V=V[V.segment=='SSF'][['date','und','expiry','settle','prev_settle','open','high','low','close','vwap','value_tl','trades','os_price']].copy()
V['und']=V.und.astype(str)
F=pd.read_parquet(f'{OUT}/_full.parquet')
F=F[F.viop47&(F.date>='2017-03-01')].copy()

def front(dates_col, min_exp_col=None):
    """her (sym, trade_date) icin vadesi trade_date'ten (veya min_exp_col'dan) SONRA olan en yakin kontrat"""
    q=F[['sym',dates_col]+([min_exp_col] if min_exp_col else [])].dropna().drop_duplicates()
    q=q.rename(columns={'sym':'und',dates_col:'date'})
    m=q.merge(V,on=['und','date'],how='inner')
    lim=m[min_exp_col] if min_exp_col else m.date
    m=m[m.expiry>lim]
    m=m.sort_values('expiry').drop_duplicates(['und','date'],keep='first')
    return m

# t+1 bilgisi (TC/TU sonrasi gun-ici)
m1=front('date_1')
m1=m1.rename(columns={c:'f1_'+c for c in ['expiry','settle','prev_settle','open','high','low','close','vwap','value_tl','trades','os_price']})
m1=m1.rename(columns={'und':'sym','date':'date_1'})
E=F.merge(m1,on=['sym','date_1'],how='left')
# t gunu vadeli (kilit)
m0=front('date').rename(columns={'und':'sym'})
m0=m0[['sym','date','settle','prev_settle','close','high','low','open','expiry']].rename(columns={'settle':'f0_settle','prev_settle':'f0_prev','close':'f0_close','high':'f0_high','low':'f0_low','open':'f0_open','expiry':'f0_exp'})
E=E.merge(m0,on=['sym','date'],how='left')
E['f_open_rel']=E.f1_open/E.f1_prev_settle-1
E['spot_open_rel']=E.gap1
E['open_diff']=E.f_open_rel-E.spot_open_rel
E['sf_oc']=1-E.f1_close/E.f1_open
E['sf_vc']=1-E.f1_close/E.f1_vwap
E['sf_os']=1-E.f1_settle/E.f1_open
E['ss']=-E.intra1
E['tk']=0.01/E.px
ok=(E.f1_open>0)&(E.f1_close>0)&(E.f1_trades>0)&E.ok1
base=E[ok&E.date.ge('2020-03-13')&~(E.TC|E.TCs|E.TU_src|E.BC)&(np.abs(E.R-1)<0.03)]
print('BAZ (normal gunler, |R-1|<3%): vadeli acilis rel - spot acilis rel medyan bps',round(base.open_diff.median()*1e4,1),'ort',round(base.open_diff.mean()*1e4,1),'n',len(base))
print('BAZ kosulsuz vadeli open->close short brut',round(base.sf_oc.mean()*1e4,1),' spot ayni gunler',round(base.ss.mean()*1e4,1))
res=[]
for nm,msk in [('TC',E.TC),('TCs',E.TCs),('TU_s',E.TU_s),('TU_src',E.TU_src)]:
    s=E[msk&ok&E.date.ge('2020-03-13')].copy()
    # t gununde vadeli kilitli mi
    s['f0_lock']=s.f0_close>=s.f0_prev*1.0995-0.011
    print(f'\n=== {nm} (P10, VIOP47, vadeli t+1 islem gormus) n={len(s)} | t gunu vadeli tavanda kapanis orani {s.f0_lock.mean():.3f} | t+1 vadeli acilis limitte {(s.f1_open>=s.f1_prev_settle*1.0995-0.011).mean():.3f}')
    print('  open_diff (vadeli acilis rel - spot acilis rel) medyan bps',round(s.open_diff.median()*1e4,1),'ort',round(s.open_diff.mean()*1e4,1),' -> baza gore fazla medyan',round((s.open_diff.median()-base.open_diff.median())*1e4,1))
    print('  t+1 vadeli islem sayisi medyan',s.f1_trades.median(),' islem tutari medyan mn TL',round(s.f1_value_tl.median()/1e6,1),' %10 dilim',round(s.f1_value_tl.quantile(.1)/1e6,1))
    for lab,col,cost in [('spot acilis->kapanis (ayni olaylar) @15+tik','ss',1),('vadeli open->close brut','sf_oc',0),('vadeli open->close @15+tik','sf_oc',1),
                         ('vadeli open->settle @15+tik','sf_os',1),('vadeli VWAP->close brut','sf_vc',0),('vadeli VWAP->close @15+tik','sf_vc',1)]:
        x=s[col]-(15e-4+s.tk if cost else 0)
        r=summ(s.assign(net=x),'net');
        sub={}
        for a,b in [('2020-03-13','2020-12-31'),('2021-01-01','2023-12-31'),('2024-01-01','2026-12-31')]:
            q=s[(s.date>=a)&(s.date<=b)]; xx=q[col]-(15e-4+q.tk if cost else 0); mm,tt,nn=cl_t(xx,q.date_1); sub[a[:4]+'-'+b[2:4]]=f'{mm*1e4:.0f} (t {tt:.1f}, n {nn})'
        print(f'  {lab:45s} trade {r["trade_bps"]:7.1f} (t {r["trade_t"]:5.2f}) day {r["day_bps"]:7.1f} (t {r["day_t"]:5.2f}) med {r["med_bps"]:6.1f} n {r["n"]} | {sub}')
    # acilis seansi var mi (2022-09+)
    q=s[s.date>='2022-09-01']
    print('  2022-09+ vadeli acilis seansi fiyati olan olay orani',round(q.f1_os_price.notna().mean(),3))
E.to_parquet(f'{OUT}/_ev_fut.parquet')
