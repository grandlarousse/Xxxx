import sys; sys.path.insert(0,"/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b")
from vb import *
q=pd.read_parquet(RES+'/06_q.parquet'); Y=q.intra1_raw
q['U0']=q.D_fx0-q.gap1_raw
for nm,sig,thr in [('D_fx0 |>50|',q.D_fx0,0.005),('U_fx0 |>50|',q.U0,0.005),('U |>50|',q.U,0.005),('D |>50|',q.D,0.005),('D |>0|',q.D,0)]:
    o=[]
    for lab,s,e in [('IS','2014','2020-12-31'),('OOS','2021','2026-12-31'),('2021-22','2021','2022-12-31'),('2023','2023','2023-12-31'),('2024+','2024','2026-12-31')]:
        r,_=bt(sig,Y,thr,8,s,e); o.append(f'{lab} {r["mean"]:+.1f}(t {r["t"]:+.2f},Sh {r["sh"]:+.2f},n {r["n"]})')
    print(f'{nm:13s}',' | '.join(o))
# Maliyet duyarlılığı: U|>50 ve D|>50 tüm dönem / OOS
for c in [4,8,12,15,20]:
    a,_=bt(q.U,Y,0.005,c,'2021'); b,_=bt(q.D,Y,0.005,c,'2021'); a2,_=bt(q.U,Y,0.005,c,'2014','2020-12-31'); b2,_=bt(q.D,Y,0.005,c,'2014','2020-12-31')
    print(f'maliyet {c:>2}: U50 OOS {a["mean"]:+.1f} Sh {a["sh"]:+.2f} IS {a2["mean"]:+.1f} | D50 OOS {b["mean"]:+.1f} Sh {b["sh"]:+.2f} IS {b2["mean"]:+.1f}')
# OOS PnL payı 2021-22
r,p=bt(q.U,Y,0.005,8,'2021'); print('U50 OOS toplam bps',round(p.sum()),' 2021-22 payı %',round(100*p.loc[:'2022-12-31'].sum()/p.sum()))
r,p=bt(q.D,Y,0.005,8,'2021'); print('D50 OOS toplam bps',round(p.sum()),' 2021-22 payı %',round(100*p.loc[:'2022-12-31'].sum()/p.sum()))
