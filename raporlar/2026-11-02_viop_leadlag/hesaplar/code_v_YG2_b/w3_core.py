import numpy as np, pandas as pd, vlib as v
A=pd.read_parquet(v.RES+'/panel.parquet')
XU=A[A.sym=='XU030'].set_index('date'); S=A[(A.sym!='XU030')].copy()
S=S.sort_values(['sym','date']); S['CA_l1']=S.groupby('sym')['CA'].shift(1)   # bir önceki yaz-gününün CA'sı (bayat sinyal)
S['xu_y']=S['date'].map(XU['y']); S['xu_CA']=S['date'].map(XU['CA'])
S['CA_id']=S['CA']-S['xu_CA']
W=S[S['CA'].notna()].copy()
print('gözlem',len(W),'gün',W.date.nunique())
out=[]
# 1) havuz regresyonları
print('\n== Havuz regresyonu (gün kümelenmiş) ==')
for y in ['gap1','r1_1','y','rest1','cc1','p15_y','y0830','y_n2']:
    d=W[[y,'CA','L30','DAY','date','sym']].dropna()
    b,se=v.ols_cl(d[y],d[['CA','L30','DAY']],d['date'])
    Z=v.demean2(d,[y,'CA','L30','DAY']); b2,se2=v.ols_cl(Z[y],Z[['CA','L30','DAY']],d['date'])
    print(f'{y:7s} n={len(d)} CA {b[1]:+.3f} (t {b[1]/se[1]:+.1f})  L30 {b[2]:+.3f} ({b[2]/se[2]:+.1f})  DAY {b[3]:+.3f} ({b[3]/se[3]:+.1f}) | 2yönlü SE: CA {b2[1]:+.3f} ({b2[1]/se2[1]:+.1f}) L30 {b2[2]:+.3f} ({b2[2]/se2[2]:+.1f})')
    out.append(dict(test='pooled',y=y,b_CA=b[1],t_CA=b[1]/se[1],b_CA_fe=b2[1],t_CA_fe=b2[1]/se2[1],b_L30=b[2],t_L30=b[2]/se[2]))
# 2) standartlaştırılmış karşılaştırma: müzayede vs sürekli işlemdeki son hareketler (her hareket kendi referansından sonrasını tahmin ediyor mu?)
print('\n== Sahte müzayede plasebosu: hareket -> referans noktasından ertesi 07:30 (1σ başına bps) ==')
S['p1430_y']=np.log(S['P0730_n']/S['P1430'])
for sig,y,lab in [('CA','y','CA -> C..07:30'),('L30','p15_y','L30 (14:30-15:00) -> P15:00..07:30'),('L60','p1430_y','L60 (13:30-14:30) -> P14:30..07:30')]:
    d=S[S['CA'].notna()][[sig,y,'date']].dropna(); sd=d[sig].std()
    b,se=v.ols_cl(d[y],d[[sig]]/sd,d['date'])
    print(f'{lab:38s} sd={1e4*sd:5.1f}bps  b/1σ={1e4*b[1]:+.2f} bps (t {b[1]/se[1]:+.1f})  ham b={b[1]/sd:+.3f}')
# 3) portföy ızgarası (veri madenciliği yüzeyi)
print('\n== Portföy ızgarası (ham, bps/gün, t) ==')
grid=[]
for thr in [0,10,25,50,75,100]:
    row={}
    for y in ['gap1','y','y0830','y0930','y1430','cc1']:
        for ex in [False,True]:
            dd,d=v.port(W,'CA',y,thr/1e4,excess=ex); s=v.summ(dd,d)
            grid.append(dict(thr=thr,y=y,excess=ex,**s))
G=pd.DataFrame(grid)
for ex in [False,True]:
    print('excess' if ex else 'ham'); print(G[G.excess==ex].pivot(index='thr',columns='y',values='bps').round(1).to_string()); print(G[G.excess==ex].pivot(index='thr',columns='y',values='t').round(1).to_string())
G.to_csv(v.RES+'/w3_grid.csv',index=False)
# 4) plasebolar
print('\n== Plasebolar (|sinyal|>25 bps, ham ve excess) ==')
for lab,sig,y in [('baz CA_t -> C_t..07:30_{t+1}','CA','y'),('bayat CA_{t-1} -> C_t..07:30_{t+1}','CA_l1','y'),('CA_t -> C_{t+1}..07:30_{t+2}','CA','y_n2'),('CA_t -> P15:00..07:30 (C atlanmış)','CA','p15_y')]:
    for ex in [False,True]:
        dd,d=v.port(S[S['CA'].notna()|S['CA_l1'].notna()],sig,y,0.0025,excess=ex); print(f'{lab:40s} {"excess" if ex else "ham   "}', v.summ(dd,d))
