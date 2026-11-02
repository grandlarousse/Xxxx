"""Reel / nominal / USD bazlı getiri karşılaştırması ve 'dolar hissesi' (kur geçişkenliği) ayrımı.
- Yıllık ortalama log getiri: TL, USD (TL − USDTRY), reel (TL − aylık TÜFE).
- Haftalık (Cuma-Cuma) ve aylık kur geçişkenliği: r_TL = a + b·r_USDTRY ; USD bazlı beta = b − 1. XU100'e göre göreli: (r_i − r_XU100) ~ r_USDTRY.
- Kriz pencereleri: 2018-08, 2021-Q4, 2025-03.
Çıktı: res/usd_real.csv, res/usd_crisis.csv"""
import numpy as np, pandas as pd
import mlib as M, ll
GROUP = {  # iş modeli sınıfı (kaynak: şirket faaliyetleri; ihracat payı 2026/06: BRSAN %89, THYAO %88, FROTO %82)
 "ENKAI": "E", "TUPRS": "E", "THYAO": "E", "PGSUS": "E", "FROTO": "E", "TOASO": "E", "BRSAN": "E", "EREGL": "E", "KRDMD": "E", "TRALT": "E", "TRMET": "E",
 "ARCLK": "E", "VESTL": "E", "SISE": "E", "CIMSA": "E", "ASTOR": "E", "TAVHL": "E", "TKFEN": "E", "AEFES": "E", "ASELS": "E", "PETKM": "E", "SASA": "E",
 "AKBNK": "B", "GARAN": "B", "YKBNK": "B", "ISCTR": "B", "HALKB": "B", "VAKBN": "B", "TSKB": "B",
 "BIMAS": "D", "MGROS": "D", "SOKM": "D", "ULKER": "D", "TCELL": "D", "TTKOM": "D", "EKGYO": "D", "ENJSA": "D", "AKSEN": "D", "ODAS": "D", "OYAKC": "D",
 "DOAS": "I", "HEKTS": "I", "GUBRF": "I",
 "KCHOL": "H", "SAHOL": "H", "ALARK": "H", "DOHOL": "H"}
GDESC = {"E": "ihracatçı / döviz gelirli", "B": "banka", "D": "yurt içi TL gelirli", "I": "ithalatçı / döviz maliyetli", "H": "holding"}
cpi = M.cpi_monthly()
cal = ll.bist_cal(); cal = cal[cal >= "2014-01-01"]
fx = ll.ret("TRY=X").reindex(cal)
per = cal.to_period("M"); ndays = pd.Series(per).value_counts()
infl = pd.Series(np.log(1 + cpi["mom"].reindex(per).values / 100) / ndays.reindex(per).values, index=cal)
def weekly(r): return r.groupby(pd.Grouper(freq="W-FRI")).sum(min_count=1)
def monthly(r): return r.groupby(pd.Grouper(freq="ME")).sum(min_count=1)
def quarterly(r): return r.groupby(pd.Grouper(freq="QE")).sum(min_count=1)
xu = ll.ret("XU100").reindex(cal)
rows = []
for s in M.STOCKS + ["XU100", "XBANK", "XUSIN"]:
    r = M.cc(s).reindex(cal)
    ok = r.notna() & fx.notna()
    o = {"stock": s, "group": GROUP.get(s, "IDX"), "n": int(ok.sum())}
    for lab, a, b in [("full", "2014-01-01", "2026-12-31"), ("is", "2014-01-01", "2020-12-31"), ("oos", "2021-01-01", "2026-12-31"), ("3y", "2023-10-30", "2026-12-31")]:
        m = ok & (cal >= a) & (cal <= b)
        o[f"ann_tl_{lab}"] = 252 * r[m].mean() * 100; o[f"ann_usd_{lab}"] = 252 * (r - fx)[m].mean() * 100; o[f"ann_real_{lab}"] = 252 * (r - infl)[m].mean() * 100
    for lab, f in [("w", weekly), ("m", monthly), ("q", quarterly)]:
        R = f(r); F = f(fx); X = f(xu)
        for per_, a, b in [("full", "2014", "2026"), ("is", "2014", "2020"), ("oos", "2021", "2026")]:
            sl = slice(a, b)
            q = M.ols(R[sl], pd.DataFrame({"fx": F[sl]}), lags=4 if lab == "w" else 2, min_n=20)
            if q: o[f"pt_{lab}_{per_}"], o[f"pt_{lab}_{per_}_t"] = q[0]["fx"], q[1]["fx"]
            if s != "XU100":
                q = M.ols((R - X)[sl], pd.DataFrame({"fx": F[sl]}), lags=4 if lab == "w" else 2, min_n=20)
                if q: o[f"rel_{lab}_{per_}"], o[f"rel_{lab}_{per_}_t"] = q[0]["fx"], q[1]["fx"]
                # USD bazlı beta: hisse USD getirisi ~ USDTRY + XU100 USD getirisi
                q = M.ols((R - F)[sl], pd.DataFrame({"fx": F[sl], "mu": (X - F)[sl]}), lags=4 if lab == "w" else 2, min_n=20)
                if q: o[f"usdb_{lab}_{per_}"], o[f"usdb_{lab}_{per_}_t"] = q[0]["fx"], q[1]["fx"]
    rows.append(o)
U = pd.DataFrame(rows); U.to_csv(M.RES + "/usd_real.csv", index=False)
# kriz pencereleri: hisse TL getirisi / USDTRY değişimi (geçişkenlik)
W = {"2018-08 kur krizi": ("2018-07-31", "2018-08-13"), "2018 Mayıs-Ağustos": ("2018-04-30", "2018-08-31"), "2021-Q4 faiz indirimi": ("2021-09-22", "2021-12-17"),
     "2021-12 KKM dönüşü": ("2021-12-17", "2021-12-24"), "2023-06 ortodoks dönüş": ("2023-05-26", "2023-07-31"), "2025-03 İmamoğlu": ("2025-03-18", "2025-03-21")}
px = {s: ll.daily(s if s in ("XU100", "XBANK", "XUSIN") else s) for s in M.STOCKS + ["XU100", "XBANK", "XUSIN"]}
fxp = ll.daily("TRY=X"); rows = []
for w, (a, b) in W.items():
    f = np.log(fxp.asof(pd.Timestamp(b)) / fxp.asof(pd.Timestamp(a)))
    for s, p in px.items():
        try: rs = np.log(p.asof(pd.Timestamp(b)) / p.asof(pd.Timestamp(a)))
        except Exception: rs = np.nan
        rows.append({"window": w, "a": a, "b": b, "stock": s, "group": GROUP.get(s, "IDX"), "r_tl": rs, "r_fx": f, "r_usd": rs - f, "passthrough": rs / f if abs(f) > 0.01 else np.nan})
C = pd.DataFrame(rows); C.to_csv(M.RES + "/usd_crisis.csv", index=False)
pd.set_option("display.width", 250)
print(U[["stock", "group", "ann_tl_full", "ann_usd_full", "ann_real_full", "pt_w_full", "pt_w_is", "pt_w_oos", "pt_m_full", "rel_w_full", "rel_w_full_t", "usdb_w_full", "usdb_w_full_t", "usdb_m_full"]].sort_values("pt_m_full").round(2).to_string(index=False))
print(U.groupby("group")[["pt_w_full", "pt_m_full", "pt_q_full", "rel_w_full", "rel_m_full", "rel_q_full", "usdb_w_full", "usdb_m_full", "usdb_q_full", "pt_w_is", "pt_w_oos", "ann_tl_full", "ann_usd_full", "ann_real_full"]].mean().round(2).to_string())
print(U[["stock","group","pt_q_full","pt_q_full_t","rel_q_full","rel_q_full_t","usdb_q_full","usdb_q_full_t","pt_q_is","pt_q_oos"]].sort_values("rel_q_full").round(2).to_string(index=False))
print(C.pivot_table(index="stock", columns="window", values="passthrough").round(2).to_string())
