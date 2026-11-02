"""v6: CIMSA / OYAKC (ve ALARK) derin inceleme + plasebo.
- Yıllar, gap-up/gap-down, Şubat–Mart 2023 deprem dönemi hariç, en iyi 5 / 10 işlem çıkarılınca, medyan işlem, isabet oranı.
- Plasebo: dünün gap'i ile bugünün gün-içini fade (aynı gün mekanizması yoksa ~0 olmalı); işaret-karıştırma null (1000 permütasyon, OOS ortalaması).
- Hisseye özgü (idio) versiyon CIMSA/OYAKC.
Çıktı: res/v6_cimsa.csv"""
import numpy as np, pandas as pd, vc
rng = np.random.default_rng(7)
D = {s: vc.decomp(s) for s in ["CIMSA", "OYAKC", "ALARK", "XU030"]}
gm = D["XU030"]["gap"]; im = D["XU030"]["intra"]
rows = []
for s in ["CIMSA", "OYAKC", "ALARK"]:
    d = D[s].dropna(subset=["gap", "intra"]).copy()
    d["pos"] = (-np.sign(d.gap)).where(d.gap.abs() > 0.01, 0.0)
    d["r"] = d.pos * d.intra
    t = d[d.pos != 0]
    def st(lab, x):
        m, tt, n = vc.nw_mean(x.values, 5)
        rows.append(dict(stock=s, spec=lab, n=n, bps=1e4 * m, t=tt, med_bps=1e4 * x.median() if n else np.nan, hit=float((x > 0).mean()) if n else np.nan))
    for pn, m in [("IS14-20", t.index < vc.SPLIT), ("IS16-20", (t.index >= "2016-01-01") & (t.index < vc.SPLIT)), ("OOS21-26", t.index >= vc.SPLIT)]:
        x = t.r[m]; st(pn, x)
        st(pn + " gap-UP short", t.r[m & (t.gap > 0)]); st(pn + " gap-DOWN long", t.r[m & (t.gap < 0)])
        if pn == "OOS21-26":
            xx = x[~((x.index >= "2023-02-06") & (x.index <= "2023-03-31"))]; st(pn + " deprem (06.02–31.03.2023) hariç", xx)
            st(pn + " en iyi 5 işlem hariç", x.drop(x.nlargest(5).index)); st(pn + " en iyi 10 işlem hariç", x.drop(x.nlargest(10).index))
            st(pn + " koşulsuz ort. intra (tüm günler, long)", D[s].intra[(D[s].index >= vc.SPLIT)].dropna())
            # işaret karıştırma null
            sig = t.pos[m].values; y = t.intra[m].values; obs = (sig * y).mean()
            null = np.array([(rng.permutation(sig) * y).mean() for _ in range(2000)])
            rows.append(dict(stock=s, spec="OOS işaret-permütasyon p (tek yönlü)", n=len(y), bps=1e4 * obs, t=np.nan, med_bps=1e4 * np.median(null), hit=float((null >= obs).mean())))
            # plasebo: dünün gap'i
            dd = D[s].copy(); dd["g1"] = dd.gap.shift(1); dd = dd[(dd.index >= vc.SPLIT)].dropna(subset=["g1", "intra"])
            p1 = (-np.sign(dd.g1)).where(dd.g1.abs() > 0.01, 0.0); st("PLASEBO OOS: gap_{t-1} fade -> intra_t", (p1 * dd.intra)[p1 != 0])
            p1b = p1.where(dd.gap.abs() <= 0.01, 0.0); st("PLASEBO OOS: gap_{t-1} fade, bugün |gap|<=1%", (p1b * dd.intra)[p1b != 0])
            st("corr(gap_t, gap_{t-1}) OOS x1e4", pd.Series([1e4 * dd[["gap", "g1"]].corr().iloc[0, 1]]))
            # idio hedge'li
            di = D[s].join(pd.DataFrame({"gm": gm, "im": im}), how="left").dropna(subset=["gap", "intra", "gm", "im"])
            di = di[di.index >= vc.SPLIT]; idio = di.gap - di.gm
            pi = (-np.sign(idio)).where(idio.abs() > 0.01, 0.0); st("OOS idio>1% hedge'li", (pi * (di.intra - di.im))[pi != 0])
    for y, g in t.groupby(t.index.year):
        m, tt, n = vc.nw_mean(g.r.values, 3); rows.append(dict(stock=s, spec=f"yıl {y}", n=n if n else len(g), bps=1e4 * g.r.mean(), t=tt, med_bps=1e4 * g.r.median(), hit=float((g.r > 0).mean())))
R = pd.DataFrame(rows); R.to_csv(vc.RES + "/v6_cimsa.csv", index=False)
pd.set_option("display.width", 200); pd.set_option("display.max_rows", 300)
print(R.round(2).to_string())
