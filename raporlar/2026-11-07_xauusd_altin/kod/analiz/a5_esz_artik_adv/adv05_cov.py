from adv_lib import *
sp=load_spot(); days=sp.index
for k in ["DXY","TBOND","SPX","EURUSD","USDJPY","XAG"]:
    a=hsnap(SYM[k],12,days); b=hsnap(SYM[k],15,days); r=np.log(b/a)
    yr=r.groupby(r.index.year).apply(lambda s: f"{s.notna().sum()}/{(s.fillna(0)!=0).sum()}")
    print(k, yr.to_dict())
