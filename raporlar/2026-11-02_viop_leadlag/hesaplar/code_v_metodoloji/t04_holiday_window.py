import warnings; warnings.filterwarnings("ignore")
# T04: Tatil sonrası 'lag-1' penceresi hatasının etkisi. Doğru gece-bilgisi penceresi: ABD kapanışları d, prev<=d<=t-1 (takvim)
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_metodoloji')
import vm, numpy as np, pandas as pd
c=vm.cal(); c=c[c>=pd.Timestamp('2014-01-01')]
for drv in ['ES=F','^GSPC','TUR','EEM','BZ=F','^VIX']:
    p=vm.px(drv)
    # kütüphane tarzı
    pc=vm.on_cal(p,c); lib=np.log(pc).diff().shift(1)
    # doğru: P(son kapanış tarihi <= t-1 takvim) - P(son kapanış <= prev-1 takvim)
    def at(dates):
        idx=p.index.searchsorted(dates,side='right')-1
        return pd.Series(np.where(idx>=0,p.values[np.clip(idx,0,None)],np.nan),index=c)
    prev=pd.Series(c,index=c).shift(1)
    a=at(c-pd.Timedelta(days=1)); b=at(pd.DatetimeIndex(prev.values)-pd.Timedelta(days=1))
    cor=np.log(a/b.values); cor[prev.isna().values]=np.nan  # ilk gün NaT düzeltmesi
    aff=(lib.round(10)!=cor.round(10))&lib.notna()&cor.notna()
    for tgt in ['XU100.IS','XU030.IS','THYAO.IS','GARAN.IS']:
        g=vm.decomp(tgt)
        r=[]
        for nm,sig in [('lib',lib),('dogru',cor)]:
            df=pd.concat([g['gap'],g['intra'],g['cc'],sig.rename('s')],axis=1).dropna()
            r.append((nm,df['gap'].corr(df['s']),df['intra'].corr(df['s']),df['cc'].corr(df['s']),len(df)))
        # etkilenen günlerde
        df=pd.concat([g['gap'],lib.rename('lib'),cor.rename('cor')],axis=1).dropna(); df=df[aff.reindex(df.index).fillna(False)]
        print(f"{drv:6s}->{tgt:9s} gap-corr lib={r[0][1]:.3f} doğru={r[1][1]:.3f} | intra lib={r[0][2]:+.3f} doğru={r[1][2]:+.3f} | cc lib={r[0][3]:.3f} doğru={r[1][3]:.3f} | etkilenen gün n={len(df)}: gap~lib={df['gap'].corr(df['lib']):.2f} gap~doğru={df['gap'].corr(df['cor']):.2f}")
