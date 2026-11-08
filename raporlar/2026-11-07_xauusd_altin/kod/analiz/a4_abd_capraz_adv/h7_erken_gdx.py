"""h7: ek erken dönem: GDX (2006+) ve GDXJ (2009-11+) beta-artığı → altın spot 15:00→15:00 UTC 3 gün, 2008–2009 (spot paneli öncesi) ve
spot panelinde GDX ile 2010–2016. Hedef Dukascopy XAUUSD saatlik (fiyat anı = bar başı + 1 saat)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
h = hourly("XAUUSD").copy(); i = pd.to_datetime(h.index).tz_convert("UTC").tz_localize(None); px = pd.Series(h["c"].values, index=i + pd.Timedelta(hours=1))
p15 = px[(px.index.hour == 15) & (px.index.minute == 0)]; p15.index = p15.index.normalize(); p15 = p15[~p15.index.duplicated()]
p15 = p15[p15.index.dayofweek < 5]
print("2008-2009 15:00 doluluk:", p15["2008"].notna().sum(), p15["2009"].notna().sum())
def raw(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); y.index = pd.to_datetime(y.index); return y["adjclose"]
gl = raw("GLD")
for m in ("GDX", "GDXJ"):
    us = pd.concat([raw(m).rename("m"), gl.rename("g")], axis=1).dropna()
    rm = np.log(us.m).diff(); rg = np.log(us.g).diff(); z = zscale(rm - beta(rm, rg, 60, 40) * rg)
    days = p15.index
    D = pd.Series(us.index, index=us.index).reindex(days - pd.Timedelta(days=1), method="ffill"); D.index = days
    x = pd.Series(z.reindex(D.values).values, index=days).where(~D.duplicated().values, 0.0)
    lp = np.log(p15); y3 = lp.shift(-3) - lp
    for nm, a, b in (("2007-09", "2007-01-01", "2009-12-31"), ("2010-12", "2010-01-01", "2012-12-31"), ("2013-16", "2013-01-01", "2016-12-31"), ("2010-16", "2010-01-01", "2016-12-31"), ("2017-26", "2017-03-01", "2026-12-31")):
        mm = (days >= a) & (days <= b)
        s = ic(x[mm], y3[mm], 5)
        print(m, nm, "n", s["n"], "ic", round(s["ic"], 3) if s["ic"] == s["ic"] else None, "t", round(s["t"], 2) if s["t"] == s["t"] else None)
