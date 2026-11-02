"""Elektrik: PTF (EPİAŞ) ve Avrupa gaz/karbon -> AKSEN/ENJSA/ODAS. Günlük (zamanlama: PTF(t+1) t günü ~11:00 UTC ilan), haftalık, aylık.
Ayrıca PTF'nin TTF/Brent/kömür ile ilişkisi (Türkiye fiyatı Avrupa gazını takip ediyor mu?)."""
import pandas as pd, numpy as np, statsmodels.api as sm, elib
from elib import R, DEC, ll
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)
ptf = elib.ptf_daily()
lp = np.log(ptf[["tl", "usd", "eur"]].clip(lower=1))
cal = ll.bist_cal()
# günlük haber: L_t = (t-5..t+1) 7g ort (t günü seansında bilinir)
m7 = lp.rolling(7).mean().shift(-1)
L = m7.reindex(m7.index.union(cal)).ffill().reindex(cal); L = L[L.index <= "2026-09-25"]
news = L.diff()
# alternatif: yarının PTF'si / bugünün - geçen haftanın aynı günü farkı (D1D7)
d1 = (lp.shift(-1) - lp).sub(lp.shift(-1).shift(7) - lp.shift(7))
d1 = d1.reindex(cal)
rows = []
for s in ["AKSEN", "ENJSA", "ODAS", "ZOREN", "TUPRS"]:
    dd = DEC(s) if s != "ZOREN" else pd.DataFrame({"cc": R("ZOREN")})
    for nm, sig in [("news_tl", news.tl), ("news_usd", news.usd), ("d1d7_tl", d1.tl)]:
        for tg in ["cc", "gap", "intra"]:
            if tg not in dd: continue
            for k, lab in [(0, "aynı gün (haber seans içinde)"), (1, "ertesi gün")]:
                st = elib.lead_stats(dd[tg], sig.shift(k), start="2014-01-01")
                rows.append({"stock": s, "sig": nm, "target": tg, "lag": k, "c_all": st["all"][0], "t_all": st["all"][1], "t_is": st["is"][1], "t_oos": st["oos"][1], "c_oos": st["oos"][0], "n": st["all"][2]})
G = pd.DataFrame(rows); G.to_csv(elib.RES + "/ptf_daily_tests.csv", index=False)
P("== Günlük PTF haberi testleri (t değerleri)"); P(G[G.sig != "d1d7_tl"].pivot_table(index=["stock", "sig"], columns=["target", "lag"], values="t_all").round(1).to_string())
# haftalık / aylık: USD bazlı hisse vs PTF ort (USD) değişimi
def agg(rule):
    pm = ptf[["usd", "tl"]].resample(rule).mean()
    px = pd.concat({s: ll.daily(s) for s in ["AKSEN", "ENJSA", "ODAS", "ZOREN", "XU100", "TRY=X"]}, axis=1)
    pxm = px.resample(rule).last()
    usdret = np.log(pxm.drop(columns="TRY=X").div(pxm["TRY=X"], axis=0)).diff()
    ttf = np.log(ll.daily("TTF=F").resample(rule).mean()).diff()
    bz = np.log(ll.daily("BZ=F").resample(rule).mean()).diff()
    mtf = np.log(ll.daily("MTF=F").resample(rule).mean()).diff()
    eur = np.log(ptf.eur.resample(rule).mean()).diff()
    return pd.concat([usdret, np.log(pm.usd).diff().rename("ptf_usd"), np.log(pm.tl).diff().rename("ptf_tl"), eur.rename("ptf_eur"), ttf.rename("ttf"), bz.rename("bz"), mtf.rename("mtf")], axis=1).dropna(subset=["ptf_usd"])
for rule, lab in [("ME", "aylık"), ("QE", "çeyreklik")]:
    A = agg(rule); A = A[A.index >= "2014-01-01"]
    P(f"== {lab}: corr(hisse USD getirisi, ortalama PTF USD değişimi) | kısmi (XU100 USD)")
    for s in ["AKSEN", "ENJSA", "ODAS", "ZOREN"]:
        a = A[[s, "ptf_usd", "XU100"]].dropna()
        for per, x in [("tam", a), ("IS", a[a.index < "2021"]), ("OOS", a[a.index >= "2021"])]:
            if len(x) < 8: continue
            P(f"  {s} {per}: c={x[s].corr(x.ptf_usd):.2f} pc={ll.partial_corr(x[s], x.ptf_usd, [x.XU100])[0]:.2f} n={len(x)}")
    a = A[["ptf_eur", "ttf", "bz", "mtf"]].dropna()
    P(f"  PTF(EUR) ~ TTF corr={a.ptf_eur.corr(a.ttf):.2f}, ~Brent {a.ptf_eur.corr(a.bz):.2f}, ~kömür {a.ptf_eur.corr(a.mtf):.2f} (n={len(a)}); OOS TTF: {a[a.index>='2021'].ptf_eur.corr(a[a.index>='2021'].ttf):.2f}")
# Avrupa gaz şoku rejimi 2021-09..2022-12: AKSEN/ODAS vs TTF haftalık
w = pd.concat([elib.wk(R(s) - R("TRY=X")).rename(s) for s in ["AKSEN", "ODAS", "ENJSA"]] + [elib.wk(R("TTF=F")).rename("ttf"), elib.wk(R("XU100") - R("TRY=X")).rename("xu")], axis=1).dropna()
for per, x in [("2021H2-2022 gaz krizi", w[(w.index >= "2021-07") & (w.index < "2023")]), ("diğer", w[(w.index < "2021-07") | (w.index >= "2023")])]:
    P(f"== haftalık USD, {per}: " + ", ".join(f"{s}: c={x[s].corr(x.ttf):.2f} pc={ll.partial_corr(x[s], x.ttf, [x.xu])[0]:.2f}" for s in ["AKSEN", "ODAS", "ENJSA"]) + f" n={len(x)}")
open(elib.RES + "/05_power.txt", "w").write("\n".join(out))
