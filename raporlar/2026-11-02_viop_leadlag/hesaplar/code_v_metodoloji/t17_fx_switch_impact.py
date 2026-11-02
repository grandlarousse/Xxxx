# T17: FX zaman damgası geçiş tarihi ve FX_FIX'in 2005-2010 look-ahead etkisi (TRY lag-1 -> BIST)
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, pandas as pd, numpy as np
def raw_r(sym):
    d=vm.raw(sym); x=pd.Series(d['adj'].values,index=pd.DatetimeIndex(d['ldate'].values)); x=x[~x.index.duplicated(keep='last')]; return np.log(x[x>0]).diff()
a=raw_r('EURUSD=X'); b=raw_r('FXE')
df=pd.concat([a.rename('fx'),b.rename('e'),b.shift(1).rename('em1')],axis=1).dropna()
df=df[(df.index>='2010-01-01')&(df.index<='2011-06-30')]
r0=df.fx.rolling(30).corr(df.e); r1=df.fx.rolling(30).corr(df.em1)
sw=(r1>r0)
first=sw[sw.rolling(20).mean()>0.9].index.min()
print('Geçiş: 30 günlük kayan corr ile "önceki gün ETF" baskın olmaya başladığı ilk tarih (20 gün kalıcı):',first.date() if pd.notna(first) else None)
print(pd.DataFrame({'ayni_gun':r0,'etf_dun':r1}).resample('ME').last().round(2).loc['2010-03':'2011-03'].T.to_string())
# Etki: FX_FIX'li TRY lag-1 -> XBANK/XU100 cc, yıllara göre
c=vm.cal()
tr=np.log(vm.on_cal(vm.px('TRY=X',fx_fix=True),c)).diff()
trr=np.log(vm.on_cal(vm.px('TRY=X',fx_fix=False),c)).diff()
for st in ['XU100.IS','XBANK.IS']:
    y=vm.ret(st,c=c)
    D=pd.concat([y.rename('y'),tr.shift(1).rename('fix_l1'),tr.rename('fix_l0'),trr.rename('raw_l0'),trr.shift(1).rename('raw_l1')],axis=1).dropna()
    out=D.groupby(D.index.year).apply(lambda g: pd.Series({k:g.y.corr(g[k]) for k in ['fix_l1','fix_l0','raw_l0','raw_l1']}))
    print(f'--- {st}: corr(BIST cc_t, TRY ...) yıllara göre (fix=FX_FIX kaydırmalı)'); print(out.loc[2005:2014].round(3).to_string())
    for lo,hi in [('2005','2010-12-31'),('2011','2026')]:
        g=D.loc[lo:hi]; print(f'  {lo}-{hi[:4]}: fix_l1={g.y.corr(g.fix_l1):+.3f} fix_l0={g.y.corr(g.fix_l0):+.3f}')
    g=D.loc['2005':]; h=D.loc['2011':]
    print(f'  TAM 2005+: fix_l1={g.y.corr(g.fix_l1):+.3f} | yalnız 2011+: {h.y.corr(h.fix_l1):+.3f}  (look-ahead katkısı)')
