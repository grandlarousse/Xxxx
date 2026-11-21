"""Her sembol için özet istatistik (haritacı ajanlar ve rapor tabloları için). Çıktı: ek/ozet_istatistik.csv"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

m = o.meta()
c = o.panel("adjclose"); raw = o.panel("close"); v = o.panel("volume"); op = o.panel("ao")
r = c.pct_change(fill_method=None)
spy, qqq = r["SPY"], r["QQQ"]
son = c.index[-1]
ytd_bas = c.index[c.index <= "2025-12-31"][-1]
sat = []
for s in c.columns:
    x = c[s].dropna()
    if len(x) < 120 or x.index[-1] < pd.Timestamp("2026-11-01"):
        continue
    rs = r[s].dropna()
    def g(n):
        return (x.iloc[-1] / x.iloc[-1 - n] - 1) * 100 if len(x) > n else np.nan
    ytd = (x.iloc[-1] / x[:ytd_bas].iloc[-1] - 1) * 100 if (x.index <= ytd_bas).any() else np.nan
    r250 = rs.iloc[-250:]
    b_spy = r250.cov(spy.reindex(r250.index)) / spy.reindex(r250.index).var()
    b_qqq = r250.cov(qqq.reindex(r250.index)) / qqq.reindex(r250.index).var()
    dv = (raw[s] * v[s]).dropna().iloc[-20:].mean() / 1e6
    gece = (op[s] / c[s].shift(1) - 1).dropna().iloc[-750:]
    gunici = (c[s] / op[s] - 1).dropna().iloc[-750:]
    x1y = x.iloc[-252:]
    sat.append(dict(
        sembol=s, ad=m.loc[s, "ad"], tur=m.loc[s, "tur"], gruplar=m.loc[s, "gruplar"], ilk=m.loc[s, "ilk"],
        fiyat=round(float(raw[s].dropna().iloc[-1]), 2),
        g5=round(g(5), 1), g21=round(g(21), 1), g63=round(g(63), 1), ytd=round(ytd, 1), g252=round(g(252), 1), g756=round(g(756), 1),
        oyn60_yillik=round(float(rs.iloc[-60:].std() * np.sqrt(252) * 100), 1),
        sigma1g=round(float(rs.iloc[-250:].std() * 100), 2),
        sigma3g=round(float((x.pct_change(3).iloc[-250:]).std() * 100), 2),
        beta_spy=round(float(b_spy), 2), beta_qqq=round(float(b_qqq), 2),
        corr_spy=round(float(r250.corr(spy.reindex(r250.index))), 2),
        hacim20_mn_usd=round(float(dv), 1) if dv == dv else np.nan,
        zirveden_1y=round(float((x.iloc[-1] / x1y.max() - 1) * 100), 1),
        maxdd_1y=round(float((x1y / x1y.cummax() - 1).min() * 100), 1),
        gece_bps_gun_3y=round(float(gece.mean() * 1e4), 1), gunici_bps_gun_3y=round(float(gunici.mean() * 1e4), 1),
    ))
df = pd.DataFrame(sat)
df.to_csv(os.path.join(o.KOK, "ek", "ozet_istatistik.csv"), index=False)
print(len(df), "sembol; son gun", son.date())
print(df[df.gruplar.str.contains("sektor_etf", na=False)][["sembol","g21","g63","ytd","g252","oyn60_yillik","beta_spy","hacim20_mn_usd","gece_bps_gun_3y","gunici_bps_gun_3y"]].to_string(index=False))
