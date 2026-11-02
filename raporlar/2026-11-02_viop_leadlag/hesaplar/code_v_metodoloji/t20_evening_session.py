# T20: XU030 spot açılış gap'inin hangi gece penceresindeki ES=F hareketiyle açıklandığı (2024-06+, h1). Pencereler (UTC):
# W1 15:00-16:00 (BIST kapandı, akşam seansı henüz yok), W2 16:00-20:00 (VİOP akşam seansı: yalnız endeks vadelileri), W3 20:00-06:30 (seans yok; kışın ABD'nin son saati + Asya), W4 06:30-06:55 (VİOP gündüz açılışı -> spot açılış müzayedesi)
import warnings; warnings.filterwarnings("ignore")
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, pandas as pd, numpy as np
import statsmodels.api as sm
h=vm.raw('ES=F','h1').sort_index(); hc=pd.Series(h['c'].values,index=h.index+pd.Timedelta(hours=1))
def at(ts):
    pos=hc.index.searchsorted(ts,side='right')-1; px=hc.values[np.clip(pos,0,None)]; age=(ts-hc.index[np.clip(pos,0,None)]).total_seconds()/3600
    return np.where((pos>=0)&(age<=3),px,np.nan)
g=vm.decomp('XU030.IS',start='2024-06-15'); c=vm.cal(); c=c[c>='2024-06-15']
prev=pd.Series(c,index=c).shift(1).dropna()
t=pd.DatetimeIndex(prev.index).tz_localize('UTC'); p=pd.DatetimeIndex(prev.values).tz_localize('UTC')
P15=at(p+pd.Timedelta(hours=15)); P16=at(p+pd.Timedelta(hours=16)); P20=at(p+pd.Timedelta(hours=20)); P0630=at(t+pd.Timedelta(hours=6,minutes=30)); P07=at(t+pd.Timedelta(hours=7))
W=pd.DataFrame({'W1':np.log(P16/P15),'W2':np.log(P20/P16),'W3':np.log(P0630/P20),'W4':np.log(P07/P0630)},index=prev.index)
D=pd.concat([g['gap'],g['intra'],W],axis=1).dropna()
# ABD yaz saati: ABD kapanışı 20:00 UTC (W2 içinde) vs kış 21:00 UTC (W3 içinde)
us_summer=D.index.to_series().apply(lambda d: pd.Timestamp(d).tz_localize('America/New_York').utcoffset().total_seconds()==-4*3600)
for lab,m in [('TÜMÜ',slice(None)),('ABD yaz saati',us_summer.values),('ABD kış saati',~us_summer.values)]:
    X=D[m] if not isinstance(m,slice) else D
    mod=sm.OLS(X['gap'],sm.add_constant(X[['W1','W2','W3']])).fit(cov_type='HC1')
    tot=mod.rsquared
    r2_12=sm.OLS(X['gap'],sm.add_constant(X[['W1','W2']])).fit().rsquared
    var=X[['W1','W2','W3']].var(); share=(var/var.sum())
    print(f"{lab:14s} n={len(X)} R²(W1+W2+W3)={tot:.3f}  R²(yalnız W1+W2: akşam seansında bilinir)={r2_12:.3f} -> akşam seansının görebildiği pay={r2_12/tot:.0%} | β: W1 {mod.params['W1']:.2f} W2 {mod.params['W2']:.2f} W3 {mod.params['W3']:.2f} | ES varyans payı W1/W2/W3 = {share['W1']:.0%}/{share['W2']:.0%}/{share['W3']:.0%}")
    mi=sm.OLS(X['intra'],sm.add_constant(X[['W1','W2','W3']])).fit(cov_type='HC1')
    print(f"{'':14s} gün-içi ~ W: t = W1 {mi.tvalues['W1']:+.2f} W2 {mi.tvalues['W2']:+.2f} W3 {mi.tvalues['W3']:+.2f} (işlenebilir kalıntı yoksa ≈0)")
