"""v_YG2_b — bağımsız panel (ll.py KULLANILMAZ).
Gün-hisse paneli: O,C (günlük, ldate), P0730..P1430 (h1 06:30..13:30 bar c), P1500 (h1 14:30 bar c; yalnız 'yaz' günleri).
Temizlik: bayat gün (v==0 & h==l) -> NaN; yarım gün (XU030 h1 bar sayısı<=6) -> CA NaN; her getiri parçası |r|>10,5% -> NaN (h1 dönemi tamamen 2020-03-13 sonrası).
Çıktı: res/panel.parquet (uzun format)."""
import pandas as pd, numpy as np, os
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
RES=os.path.dirname(os.path.abspath(__file__))+'/res'
TG="AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()
def h1raw(s):
    h=pd.read_parquet(f'{D}/h1/{s}.IS.parquet'); h=h[~h.index.duplicated(keep='last')].sort_index()
    h['day']=pd.DatetimeIndex(h.index.tz_convert(None).normalize()); h['hm']=h.index.hour*100+h.index.minute
    return h
X=h1raw('XU030'); cal=pd.Series(X.groupby('day').size())
summer=X.groupby('day')['hm'].apply(lambda x:(x==1430).any())
half=cal<=6
days=cal.index
nxt=pd.Series(days[1:].append(pd.DatetimeIndex([pd.NaT])),index=days)
LAB={630:'P0730',730:'P0830',830:'P0930',930:'P1030',1030:'P1130',1130:'P1230',1230:'P1330',1330:'P1430',1430:'P1500'}
out=[]
for s in TG+['XU030']:
    h=h1raw(s)
    piv=h.pivot_table(index='day',columns='hm',values='c',aggfunc='last').reindex(days)
    vb=h.pivot_table(index='day',columns='hm',values='v',aggfunc='last').reindex(days)
    d=pd.read_parquet(f'{D}/daily/{s}.IS.parquet'); d.index=pd.DatetimeIndex(d['ldate']); d=d[~d.index.duplicated(keep='last')]
    stale=(d['v'].fillna(0)==0)&(d['h']==d['l'])
    if s=='XU030': stale=d['h']==d['l']
    d.loc[stale,['o','h','l','c']]=np.nan
    d=d.reindex(days)
    P=pd.DataFrame(index=days); P['O']=d['o']; P['C']=d['c']; P['H']=d['h']; P['L']=d['l']; P['V']=d['v']
    for k,v in LAB.items(): P[v]=piv[k] if k in piv.columns else np.nan
    P.loc[~summer.values,'P1500']=np.nan
    P.loc[half.values,['P1500']]=np.nan
    P['TL']=P['V']*P['C']
    P['summer']=summer.values; P['half']=half.values
    # ertesi gün değerleri
    N=P.reindex(nxt.values); N.index=days
    for c in ['O','C','P0730','P0830','P0930','P1430','P1500','H','L']: P[c+'_n']=N[c].values
    N2=P.reindex(nxt.reindex(nxt.values).values); N2.index=days
    P['P0730_n2']=N2['P0730'].values; P['C_n2']=N2['C'].values; P['O_n2']=N2['O'].values
    P['sym']=s; out.append(P)
A=pd.concat(out); A.index.name='date'; A=A.reset_index()
lg=lambda a,b: np.log(A[a]/A[b])
A['CA']=lg('C','P1500'); A['L30']=lg('P1500','P1430'); A['LH']=lg('C','P1430'); A['DAY']=lg('P1430','O')
A['L60']=lg('P1430','P1330')
A['gap1']=lg('O_n','C'); A['r1_1']=lg('P0730_n','O_n'); A['y']=lg('P0730_n','C'); A['rest1']=lg('C_n','P0730_n')
A['cc1']=lg('C_n','C'); A['y0830']=lg('P0830_n','C'); A['y0930']=lg('P0930_n','C'); A['y1430']=lg('P1430_n','C')
A['p15_y']=lg('P0730_n','P1500')  # müzayede öncesi fiyattan ertesi 07:30'a
A['y_n2']=np.log(A['P0730_n2']/A['C_n'])  # ertesi günden sonraki C->07:30 (gecikmeli sonuç plasebosu)
for c in ['CA','L30','LH','DAY','L60','gap1','r1_1','y','rest1','cc1','y0830','y0930','y1430','p15_y','y_n2']:
    A.loc[A[c].abs()>0.105,c]=np.nan
A.loc[A['half'],['CA','L30','LH','DAY','L60']]=np.nan
A.to_parquet(RES+'/panel.parquet')
print(A.shape, A.date.min(), A.date.max(), A['CA'].notna().sum(), A.loc[A.sym!='XU030','CA'].groupby(A.date).count().gt(0).sum())
