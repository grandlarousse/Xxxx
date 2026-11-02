"""Uzun örneklem vekili (2017-2026): ex_t = Δlog(F_uzl/C) aynı sözleşme (vadesi t'den sonra olan en yakın).
(a) h1 döneminde ex = a + b*CA + e ayrıştırması: ertesi getiriyi CA mı, e (müzayede-dışı, 18:05-18:15 bilgisi/SSF gürültüsü) mi taşıyor?
(b) Alt dönemler 2017, 2018-20, 2021-23, 2024-26; kesit arındırılmış ertesi gap ve gün-içi."""
import numpy as np, pandas as pd, vlib as v
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
TG="AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()
alias={'TRALT':['TRALT','KOZAL'],'TRMET':['TRMET','KOZAA']}
p=pd.read_parquet(D+'/viop_panel.parquet',columns=['date','root','segment','expiry','settle','trades','value_tl'])
p=p[(p.segment=='SSF')&(p.expiry>p.date)&p.settle.notna()]
rows=[]
for s in TG:
    d=pd.read_parquet(f'{D}/daily/{s}.IS.parquet'); d.index=pd.DatetimeIndex(d['ldate']); d=d[~d.index.duplicated(keep='last')]
    st=(d['v'].fillna(0)==0)&(d['h']==d['l']); d.loc[st,['o','h','l','c']]=np.nan
    d=d[d.index>='2017-01-01']
    q=p[p.root.isin(alias.get(s,[s]))]
    # her gün vadesi > t olan en yakın sözleşme
    fr=q.sort_values(['date','expiry']).groupby('date').first()[['expiry','settle','trades']]
    piv=q.pivot_table(index='date',columns='expiry',values='settle',aggfunc='last')
    X=pd.DataFrame(index=d.index); X['O']=d['o']; X['C']=d['c']
    X=X.join(fr,how='left')
    # aynı sözleşmenin bir önceki günkü uzlaşması
    dates=X.index; prev=pd.Series(dates[:-1].insert(0,pd.NaT),index=dates)
    Fp=[]
    for t,e in zip(dates,X['expiry']):
        pt=prev[t]
        Fp.append(piv.at[pt,e] if (pd.notna(e) and pd.notna(pt) and pt in piv.index and e in piv.columns) else np.nan)
    X['F_prev']=Fp; X['C_prev']=X['C'].shift(1)
    X['ex']=np.log(X['settle']/X['C'])-np.log(X['F_prev']/X['C_prev'])
    X['cc']=np.log(X['C']/X['C_prev'])
    X['gap1']=np.log(X['O'].shift(-1)/X['C']); X['intra1']=np.log(X['C'].shift(-1)/X['O'].shift(-1))
    lim=np.where(X.index<'2020-03-13',0.205,0.105)
    for c in ['cc','gap1','intra1']: X.loc[X[c].abs()>lim,c]=np.nan
    X.loc[X['ex'].abs()>0.05,'ex']=np.nan
    X['sym']=s; rows.append(X.reset_index().rename(columns={'ldate':'date','index':'date'}))
P=pd.concat(rows); P=P.rename(columns={P.columns[0]:'date'})
for c in ['ex','cc','gap1','intra1']: P[c+'_x']=P[c]-P.groupby('date')[c].transform('mean')
P.to_parquet(v.RES+'/w7_ssfpanel.parquet')
print('ex mevcut:',P.ex.notna().sum(),'gün',P[P.ex.notna()].date.nunique(), P.date.min())
def reg(d,y,xs):
    d=d[[y,'date']+xs].dropna(); b,se=v.ols_cl(d[y],d[xs],d['date']); return b,se,len(d)
print('\n== Alt dönemler: gap1_x ~ ex_x + cc_x (kesit arındırılmış) ==')
P['yr']=P.date.dt.year
for lab,m in [('2017',P.yr==2017),('2018-20',P.yr.between(2018,2020)),('2021-23',P.yr.between(2021,2023)),('2024-26',P.yr>=2024),('IS 2017-20',P.yr<=2020),('OOS 2021-26',P.yr>=2021)]:
    for y in ['gap1_x','intra1_x']:
        b,se,n=reg(P[m],y,['ex_x','cc_x']); print(f'{lab:12s} {y:9s} b_ex {b[1]:+.3f} (t {b[1]/se[1]:+.1f})  n={n}',end=' | ')
    print()
print('yıllar (gap1_x):',' '.join(f'{yr}:{reg(P[P.yr==yr],"gap1_x",["ex_x","cc_x"])[0][1]:+.3f}' for yr in range(2017,2027)))
# (a) h1 dönemi ayrıştırması
A=pd.read_parquet(v.RES+'/panel.parquet'); A=A[A.sym!='XU030']
M=A.merge(P[['date','sym','ex','ex_x','trades']],on=['date','sym'],how='inner')
M=M[M.CA.notna()&M.ex.notna()].copy()
b,se,n=reg(M,'ex',['CA']); print('\nh1 yaz: ex ~ CA: %.3f (t %.1f) n=%d'%(b[1],b[1]/se[1],n))
M['e']=M['ex']-(b[0]+b[1]*M['CA'])
M['yx']=M['y']-A.groupby('date')['y'].transform('mean').reindex(M.index).values if False else M['y']
M['yx']=M['y']-M.groupby('date')['y'].transform('mean'); M['gx']=M['gap1']-M.groupby('date')['gap1'].transform('mean')
for y in ['gap1','y','gx','yx']:
    for xs in [['ex'],['CA'],['CA','e']]:
        b,se,n=reg(M,y,xs); print(f'  {y:4s} ~ {"+".join(xs):5s}: '+'  '.join(f'{x} {b[i+1]:+.3f} (t {b[i+1]/se[i+1]:+.1f})' for i,x in enumerate(xs)))
# e'nin varyans payı
print('var(b*CA)/var(ex) = %.2f'%(np.var(M.ex-M.e)/np.var(M.ex)))
