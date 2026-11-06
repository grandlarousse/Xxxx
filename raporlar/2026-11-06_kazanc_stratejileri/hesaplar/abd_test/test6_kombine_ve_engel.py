"""TEST 6 (ek): (a) TL carry'nin USD getirisi = kullanicinin firsat maliyeti (engel orani)
              (b) Onceden belirlenmis 2 kombinasyon: endustri momentumu (49 VW, top5) + gunluk kaldirac (1x/2x) + piyasa 200-DMA filtresi
              (c) Sadece-uzun 'kazanc olayi' bacaklari: CZ ust portfoy - piyasa (AnnouncementReturn, EarningsStreak, REV6 ...)
(a) Veri: FRED IRSTCI01TRM156N (TR gecelik/interbank, %, aylik), CCUSMA02TRM618N (USD/TRY aylik ortalama). Brut, stopaj oncesi.
(b) Secim aylik getirilerle (t ay sonu), elde tutma gunluk getirilerle t+1 ay; kaldirac maliyeti T-bill+1%, ER 0.9%; 10bp/devir.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from ortak import french_monthly, french_daily, fred, stats, md_table, fmt_pct, OUT, CZ

md = []
# ---------------- (a) TL carry USD
i_tl = fred("IRSTCI01TRM156N").dropna() / 100
fx = fred("CCUSMA02TRM618N").dropna()
df = pd.concat([i_tl.rename("i"), fx.rename("fx")], axis=1).dropna()
df["usd_ret"] = (1 + df.i.shift(1) / 12) * (df.fx.shift(1) / df.fx) - 1
df["tl_ret"] = df.i.shift(1) / 12
df["fxr"] = df.fx / df.fx.shift(1)
rows = []
for lab, a, b in [("2010-2026", "2010-01-01", "2026-12-31"), ("2015-2026", "2015-01-01", "2026-12-31"),
                  ("2020-2026", "2020-01-01", "2026-12-31"), ("2023-07..2026-08 (ortodoks donus)", "2023-07-01", "2026-12-31"),
                  ("2024-2026", "2024-01-01", "2026-12-31"), ("Son 12 ay", df.index[-12], df.index[-1])]:
    x = df.loc[a:b, "usd_ret"].dropna()
    yrs = len(x) / 12
    rows.append(dict(Donem=lab, Ay=len(x), USD_CAGR=(1 + x).prod() ** (1 / yrs) - 1,
                     TL_faiz_ort=df.loc[a:b, "i"].mean(), USDTRY_degisim_yillik=df.loc[x.index, "fxr"].prod() ** (1 / yrs) - 1,
                     TL_bilesik_yillik=(1 + df.loc[x.index, "tl_ret"]).prod() ** (1 / yrs) - 1,
                     MaxDD=((1 + x).cumprod() / (1 + x).cumprod().cummax() - 1).min()))
A = pd.DataFrame(rows)
for c in ["USD_CAGR", "TL_faiz_ort", "TL_bilesik_yillik", "USDTRY_degisim_yillik", "MaxDD"]:
    A[c] = A[c].map(fmt_pct)
md += ["\n#### (a) TL para piyasasi carry'sinin USD getirisi (brut, stopaj/vergi oncesi; aylik ortalama kur ile yaklasik)\n", md_table(A, pct_cols=())]

# ---------------- (b) kombinasyon
ffd, _ = french_daily("F-F_Research_Data_Factors_daily.csv")
mkt_d = ffd["Mkt-RF"] + ffd["RF"]; rf_d = ffd["RF"]
Im, _ = french_monthly("49_Industry_Portfolios.csv", 0)
Id, t = french_daily("49_Industry_Portfolios_Daily.csv", 0); assert "Value" in t
mi = (1 + mkt_d).cumprod()
trend = (mi > mi.rolling(200).mean()).astype(float)
trend[mi.rolling(200).mean().isna()] = np.nan
pos_tr = trend.shift(1)  # t kapanis -> t+1


def comb(K, skip, N, L, use_trend, spread=0.01, ER=0.009, cost=0.001):
    lr = np.log1p(Im)
    past = lr.shift(skip).rolling(K, min_periods=K).sum()
    # gunluk agirlik: ay m sonunda secilen, ay m+1 gunlerine uygulanir
    sel = {}
    for d in past.index:
        p = past.loc[d].dropna()
        if len(p) >= 2 * N:
            sel[d] = list(p.nlargest(N).index)
    mon = Id.index.to_period("M")
    out = pd.Series(np.nan, index=Id.index)
    prev = None
    rets = []
    for per in mon.unique():
        me = (per - 1).to_timestamp(how="end").normalize() + pd.offsets.MonthEnd(0)
        me = pd.Timestamp(me.date())
        if me not in sel:
            continue
        days = Id.index[mon == per]
        names = sel[me]
        r_ind = Id.loc[days, names].mean(axis=1)   # gunluk esit agirlik (gunluk rebalans yaklasimi)
        rfx = rf_d.reindex(days).fillna(0)
        lev = L * r_ind - (L - 1) * (rfx + spread / 252) - (ER / 252 if L > 1 else 0.0)
        if use_trend:
            ptr = pos_tr.reindex(days).fillna(0)
            r = ptr * lev + (1 - ptr) * rfx
            sw = ptr.diff().abs().fillna(0); sw.iloc[0] = 0
            r = r - sw * cost
        else:
            r = lev
        to = 1.0 if prev is None else len(set(names) - set(prev)) / N
        r.iloc[0] -= to * cost * (L if L > 1 else 1)
        prev = names
        rets.append(r)
    return pd.concat(rets)


series = {}
for K, skip in [(6, 0), (12, 1)]:
    for L in (1, 2):
        for tr in (False, True):
            series[f"Ind49 K={K} s={skip} top5 L={L}{' +200DMA' if tr else ''}"] = comb(K, skip, 5, L, tr)
# referans: piyasa 2x + 200DMA (gunluk), ayni maliyetler
lev2 = 2 * mkt_d - (rf_d + 0.01 / 252) - 0.009 / 252
ptr = pos_tr.fillna(0)
ref = ptr * lev2 + (1 - ptr) * rf_d - ptr.diff().abs().fillna(0) * 0.001
series["Piyasa 2x +200DMA (referans)"] = ref
series["Piyasa 1x BH"] = mkt_d
PER = [("1927-2026", "1927-07-01", "2026-12-31"), ("1950-2026", "1950-01-01", "2026-12-31"), ("2000-2026", "2000-01-01", "2026-12-31"),
       ("2010-2026", "2010-01-01", "2026-12-31"), ("2020-2026", "2020-01-01", "2026-12-31")]
rows = []
for lab, a, b in PER:
    for nm, r in series.items():
        s = stats(r.loc[a:b], rf_d.loc[a:b], ppy=252)
        if s:
            rows.append(dict(Donem=lab, Strateji=nm, **s))
B = pd.DataFrame(rows)
B.to_csv(os.path.join(OUT, "t6_kombine.csv"), index=False)
md += ["\n#### (b) Endustri momentumu x gunluk kaldirac x 200-DMA (onceden secilmis 8 varyant + referans)\n",
       md_table(B[["Donem", "Strateji", "CAGR", "Vol", "Sharpe", "MaxDD", "EnKotuYil", "EnKotuYilT", "ExcessCAGR"]])]

# ---------------- (c) sadece-uzun kazanc olayi bacaklari
P = pd.read_parquet(os.path.join(CZ, "PredictorPortsFull.parquet"))
L20 = pd.read_parquet(os.path.join(CZ, "PredictorAltPorts_LiqScreen_ME_gt_NYSE20pct.parquet"))
ffm, _ = french_monthly("F-F_Research_Data_Factors.csv")
mkt_m = (ffm["Mkt-RF"] + ffm["RF"]) * 100
mkt_m.index = mkt_m.index.to_period("M")
rows = []
for s in ["AnnouncementReturn", "EarningsStreak", "REV6", "EarningsSurprise", "RevenueSurprise", "AnalystRevision", "Mom12m", "Mom6m", "IndMom"]:
    for lab, src in [("OP", P), ("ME>NYSE20p", L20)]:
        x = src[src.signalname == s].pivot_table(index="date", columns="port", values="ret")
        top = [c for c in x.columns if c != "LS"][-1]
        lt = x[top]; lt.index = pd.to_datetime(lt.index).to_period("M")
        ex = (lt - mkt_m.reindex(lt.index)).dropna()
        allp = x[[c for c in x.columns if c != "LS"]].mean(axis=1); allp.index = lt.index
        ex2 = (lt - allp).dropna()
        for plab, a in [("1990-2009", 1990), ("2010-2025", 2010), ("2020-2025", 2020)]:
            b = 2009 if a == 1990 else 2025
            e = ex[(ex.index.year >= a) & (ex.index.year <= b)]
            if len(e) < 24:
                continue
            e2 = ex2[(ex2.index.year >= a) & (ex2.index.year <= b)]
            rows.append(dict(Sinyal=s, Versiyon=lab, Donem=plab, Ust_port=top, Ort_fazla_ay=e.mean(), Yillik=12 * e.mean(),
                             t=e.mean() / e.std() * np.sqrt(len(e)), Ust_eksi_portort_yillik=12 * e2.mean(),
                             t2=e2.mean() / e2.std() * np.sqrt(len(e2))))
C = pd.DataFrame(rows)
C["Ort_fazla_ay"] = C["Ort_fazla_ay"].map(lambda v: f"{v:.2f}%")
C["Yillik"] = C["Yillik"].map(lambda v: f"{v:.1f}%")
C["t"] = C["t"].map(lambda v: f"{v:.2f}")
C["Ust_eksi_portort_yillik"] = C["Ust_eksi_portort_yillik"].map(lambda v: f"{v:.1f}%")
C["t2"] = C["t2"].map(lambda v: f"{v:.2f}")
md += ["\n#### (c) Sadece-uzun ust portfoy - CRSP VW piyasa (aylik fazla getiri, maliyet oncesi); ayrica ust portfoy - ayni sinyalin tum portfoylerinin ortalamasi (boyut etkisini ayiklar)\n", md_table(C, pct_cols=(), num_cols=())]
open(os.path.join(OUT, "t6_tablolar.md"), "w").write("\n".join(md))
print("\n".join(md))
