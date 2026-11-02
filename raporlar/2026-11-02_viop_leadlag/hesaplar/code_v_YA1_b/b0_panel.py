# v_YA1_b: bagimsiz panel (ll.py ve onceki kodlar IMPORT EDILMEZ)
import pandas as pd, numpy as np, os, json
D='/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data'
OUT=os.path.dirname(os.path.abspath(__file__))
VIOP47="AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()

def load(sym):
    d=pd.read_parquet(f'{D}/daily/{sym}.parquet')
    d=d.copy(); d['date']=pd.to_datetime(d['ldate']).dt.normalize()
    d=d.drop_duplicates('date',keep='last').set_index('date').sort_index()
    return d[['o','h','l','c','adj','v']]

def main():
    cat=pd.read_csv(f'{D}/catalog.csv')
    eq=cat[cat.group.isin(['VIOP','BIST_other'])&(cat.type=='EQUITY')].sym.tolist()
    # takvim: XU100 islem gunleri
    xu=load('XU100.IS'); xu=xu[xu.c>0]
    cal=xu.index
    rows=[]
    for s in eq:
        d=load(s)
        d=d[(d.c>0)]
        stale=(d.v.fillna(0)==0)&(d.h==d.l)
        d=d[~stale]
        d=d[d.index.isin(cal)]
        if len(d)<50: continue
        d['sym']=s.replace('.IS','')
        # onceki satir gercekten onceki BIST gunu mu?
        pos=pd.Series(np.searchsorted(cal,d.index),index=d.index)
        d['consec']=(pos.diff()==1)
        d['f']=d.adj/d.c
        d['c1']=d.c.shift(1); d['f1']=d.f.shift(1)
        d['base']=d.c1*d.f1/d.f          # temettu duzeltmeli baz (teorik ex)
        d['R']=d.c/d.base; d['Rh']=d.h/d.base; d['Rl']=d.l/d.base; d['Ro']=d.o/d.base
        d['dy']=1-d.f1/d.f                # temettu verimi (ex gunu >0)
        bad_o=(d.o<d.l*0.9995)|(d.o>d.h*1.0005)|(d.o<=0)
        d.loc[bad_o,'o']=np.nan
        d.loc[d.index<'2014-01-01','o']=np.nan   # Yahoo acilisi 2014 oncesi bozuk
        rows.append(d.reset_index())
    P=pd.concat(rows,ignore_index=True)
    P['viop47']=P.sym.isin(VIOP47)
    # rejim
    P['reg']=np.where(P.date>=pd.Timestamp('2020-03-13'),'P10',np.where((P.date>=pd.Timestamp('2015-12-01'))&(P.date<=pd.Timestamp('2020-03-10')),'P20','OLD'))
    lim=np.where(P.reg=='P10',0.10,np.where(P.reg=='P20',0.20,np.nan))
    P['lim']=lim
    # kurumsal islem esigi rejime bagli
    thr=np.where(P.reg=='P10',0.105,0.205)
    P['ca']=(np.abs(P.R-1)>thr)|(~P.consec)
    P.to_parquet(f'{OUT}/_panel.parquet')
    xu=xu.copy(); xu.to_parquet(f'{OUT}/_xu100.parquet')
    print(P.shape, P.sym.nunique(), P.date.min(), P.date.max())
    print(P.groupby('reg').size())
if __name__=='__main__': main()
