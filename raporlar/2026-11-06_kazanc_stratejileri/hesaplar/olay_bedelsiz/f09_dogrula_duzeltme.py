"""Duzeltme dogrulamasi: her bedelsiz hak gunu icin (a) ham kapanis sicramasi, (b) Is Yatirim duzeltilmis getirisi, (c) bizim temiz getiri,
(d) gozlenen carpan (q sicramasi) ile teorik 1+oran (bedelli kismi varsa teorik rüçhan ayari haric) karsilastirmasi.
Ayrica Is Yatirim HisseTekil duzeltilmis kapanisi ile ChartData kapanisi (gorevde belirtilen kaynak) ornek hisselerde karsilastirilir."""
import numpy as np, pandas as pd
import f10_panel as P
CACHE = P.CACHE
ev = pd.read_pickle(f"{CACHE}/olaylar_bedelsiz.pkl")
rows = []
for kod, g in ev.groupby("kod"):
    d = P.hisse(kod)
    if d is None: continue
    for _, e in g.iterrows():
        j = d.index.searchsorted(e.hak)
        if j >= len(d) or j < 1: continue
        t = d.index[j]
        if (t - e.hak).days > 5: continue
        ham = d.c.iloc[j] / d.c.iloc[j - 1] - 1; isy = d.adj.iloc[j] / d.adj.iloc[j - 1] - 1
        rows.append(dict(kod=kod, hak=e.hak, gun=t, oran=e.oran, bedelli=e.bedelli_oran, ham=ham, isy_adj=isy, temiz=d.r.iloc[j],
                         carpan=d.adjf.iloc[j], teorik=1 + e.oran / 100))
R = pd.DataFrame(rows)
saf = R[(R.bedelli.fillna(0) == 0)]
R["carpan_sapma"] = R.carpan / R.teorik - 1
print("olay", len(R), "| saf bedelsiz", len(saf))
print("ham hak gunu getirisi medyan %.1f%%, temiz getiri medyan %.2f%%, |temiz|>%%20 olan: %d" % (100 * R.ham.median(), 100 * R.temiz.median(), (R.temiz.abs() > .2).sum()))
s = R.loc[saf.index, "carpan_sapma"]
print("saf bedelsizde gozlenen/teorik carpan: |sapma|<%%1: %.1f%%, <%%3: %.1f%%" % (100 * (s.abs() < .01).mean(), 100 * (s.abs() < .03).mean()))
print(R.loc[saf.index].assign(a=s.abs()).sort_values("a").tail(8)[["kod", "hak", "oran", "ham", "isy_adj", "temiz", "carpan", "teorik"]].round(4).to_string())
ornek = R[R.kod.isin(["SASA", "KORDS", "ADEL", "TUKAS", "PETKM", "ACSEL"])][["kod", "hak", "oran", "ham", "isy_adj", "temiz", "carpan", "teorik"]]
print(ornek.round(4).to_string())
R.to_csv(f"{CACHE}/dogrulama_duzeltme.csv", index=False)
# HisseTekil duzeltilmis vs ChartData
for k in ["THYAO", "SASA", "KORDS"]:
    try:
        t = pd.read_parquet(f"{CACHE}/px_tekil/{k}.parquet"); c = pd.read_parquet(f"{CACHE}/px_chart/{k}.parquet")
        j = t.join(c, how="inner"); ra = np.log(j.adj).diff(); rc = np.log(j.px).diff()
        print(k, "gun", len(j), "medyan |fark| %.4f%%" % (100 * (j.adj / j.px - 1).abs().median()), "getiri korelasyonu %.5f" % ra.corr(rc))
    except Exception as ex: print(k, ex)
