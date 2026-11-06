"""Izgara özetleri: aile medyanları, dönem bazında (2012-18 / 2019-23 / 2024-26), EW-tüm-kümeler kıyası,
ileri yürüyüş (2012-18'de seç -> 2019-26'da ölç), maliyet/gecikme duyarlılığı, seçilen kuralın yıllık tablosu."""
import os, sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
D = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)
def yukle(suf=""):
    A = pd.read_parquet(f"{D}/seriler{suf}.parquet")
    p = f"{D}/seriler_ek{suf}.parquet"
    if os.path.exists(p):
        B = pd.read_parquet(p); A = A.join(B[[c for c in B if c not in A]])
    return A
A = yukle()
usd = pd.read_csv(f"{D}/d/USDTRY.csv", parse_dates=["ldate"]).set_index("ldate")["px"]
usd = usd[~usd.index.duplicated(keep="last")].reindex(A.index).ffill()
rf = A["rf"]; ew = A["EW_tum_kumeler"]; xu = A["XU100"]
kur = [c for c in A if (c.startswith("O:") or c.startswith("R:")) and not c.endswith(":inv")]
def cagr(r): r = r.dropna(); return (1 + r).prod() ** (252 / len(r)) - 1
def mdd(r): n = (1 + r).cumprod(); return (n / n.cummax() - 1).min()
DON = {"2012-26": ("2012-01-02", None), "2012-18": ("2012-01-02", "2018-12-31"), "2019-23": ("2019-01-01", "2023-12-31"),
       "2024-26": ("2024-01-01", None)}
rows = []
for c in kur + ["EW_tum_kumeler", "XU100", "rf"]:
    r = A[c]; d = dict(kural=c)
    for k, (a, b) in DON.items():
        x = r.loc[a:b]; d[f"cagr_{k}"] = cagr(x); d[f"dd_{k}"] = mdd(x)
        d[f"a_ew_{k}"] = (1 + cagr(x)) / (1 + cagr(ew.loc[a:b])) - 1
        d[f"a_rf_{k}"] = (1 + cagr(x)) / (1 + cagr(rf.loc[a:b])) - 1
        u = usd.loc[x.index]; d[f"usd_{k}"] = ((1 + x).prod() / (u.iloc[-1] / u.iloc[0])) ** (252 / len(x)) - 1
    y = r.loc["2012":].groupby(r.loc["2012":].index.year).apply(lambda z: (1 + z).prod() - 1)
    ye = ew.loc["2012":].groupby(ew.loc["2012":].index.year).apply(lambda z: (1 + z).prod() - 1)
    yr = rf.loc["2012":].groupby(rf.loc["2012":].index.year).apply(lambda z: (1 + z).prod() - 1)
    d["yil_ew_yenen"] = (y > ye).mean(); d["yil_rf_yenen"] = (y > yr).mean()
    ex = (r - rf).loc["2012":]; d["sharpe"] = ex.mean() / ex.std() * np.sqrt(252)
    ex1 = (r - rf).loc["2012":"2018"]; d["sharpe_12_18"] = ex1.mean() / ex1.std() * np.sqrt(252)
    if c + ":inv" in A: d["maruz"] = A[c + ":inv"].loc["2012":].mean()
    rows.append(d)
T = pd.DataFrame(rows).set_index("kural")
def aile(k):
    if k.startswith("O:"):
        p = k[2:].split("|"); return "olay:" + p[0]
    if k.startswith("R:"):
        p = k[2:].split("|"); return "rot:" + p[0]
    return k
T["aile"] = [aile(k) for k in T.index]
T["surum"] = ["lider" if "lider" in k else ("sepet" if "sepet" in k else "-") for k in T.index]
T["filtre"] = [("f1" in k or "mkt1" in k) for k in T.index]
T.to_csv(os.path.join(OUT, "ozet_tum_kurallar.csv"), float_format="%.4f")
cols = ["cagr_2012-26", "a_ew_2012-26", "a_rf_2012-26", "dd_2012-26", "sharpe", "cagr_2012-18", "a_ew_2012-18", "cagr_2019-23",
        "a_ew_2019-23", "cagr_2024-26", "a_rf_2024-26", "a_ew_2024-26", "usd_2012-26", "usd_2024-26", "yil_ew_yenen", "yil_rf_yenen"]
print("=== KIYAS ===\n", T.loc[["EW_tum_kumeler", "XU100", "rf"], cols].round(3).to_string())
M1 = T[T.aile.str.contains(":")].groupby(["aile", "surum"])[cols].median()
M1["n"] = T[T.aile.str.contains(":")].groupby(["aile", "surum"]).size()
print("\n=== AİLE x SÜRÜM MEDYANLARI ===\n", M1.round(3).to_string())
M1.to_csv(os.path.join(OUT, "ozet_aile_medyan.csv"), float_format="%.4f")
M2 = T[T.aile.str.contains(":")].groupby(["aile", "filtre"])[cols].median()
print("\n=== AİLE x XU100>200GHO FİLTRE MEDYANLARI ===\n", M2[["cagr_2012-26", "a_ew_2012-26", "dd_2012-26", "cagr_2024-26", "a_ew_2024-26"]].round(3).to_string())
# ileri yürüyüş: 2012-18 Sharpe ile seç
K = T[T.aile.str.contains(":")].copy()
rho = spearmanr(K["sharpe_12_18"], K["cagr_2019-23"]).correlation
rho2 = spearmanr(K["cagr_2012-18"], K["cagr_2024-26"]).correlation
top = K.sort_values("sharpe_12_18", ascending=False).head(10)
print(f"\n=== İLERİ YÜRÜYÜŞ === Spearman(2012-18 Sharpe, 2019-23 CAGR)={rho:.2f}; Spearman(2012-18 CAGR, 2024-26 CAGR)={rho2:.2f}")
print("2012-18'in en iyi 10'u (Sharpe):\n", top[["cagr_2012-18", "sharpe_12_18", "cagr_2019-23", "a_ew_2019-23", "cagr_2024-26", "a_ew_2024-26"]].round(3).to_string())
print("tüm kuralların medyanı 2019-23 CAGR=%.3f a_ew=%.3f ; 2024-26 CAGR=%.3f a_ew=%.3f" % (
    K["cagr_2019-23"].median(), K["a_ew_2019-23"].median(), K["cagr_2024-26"].median(), K["a_ew_2024-26"].median()))
print("top10 medyanı 2019-23 CAGR=%.3f a_ew=%.3f ; 2024-26 CAGR=%.3f a_ew=%.3f" % (
    top["cagr_2019-23"].median(), top["a_ew_2019-23"].median(), top["cagr_2024-26"].median(), top["a_ew_2024-26"].median()))
print("EW'yi 2012-26'da yenen kural payı: %.2f ; 2012-18: %.2f ; 2019-23: %.2f ; 2024-26: %.2f" % tuple(
    (K[f"a_ew_{p}"] > 0).mean() for p in DON))
# duyarlılık
for suf, ad in [("_c50", "maliyet %0.50/yön"), ("_L0", "gecikme 0 (sinyal günü kapanışı)")]:
    try:
        B = yukle(suf)
    except Exception as e:
        print(ad, "yok", e); continue
    kk = [c for c in kur if c in B]
    d = pd.DataFrame({"base": [cagr(A[c].loc["2012":]) for c in kk], "alt": [cagr(B[c].loc["2012":]) for c in kk]}, index=kk)
    d["aile"] = [aile(k) for k in kk]
    print(f"\n=== DUYARLILIK: {ad} (CAGR 2012-26 medyan) ===\n", d.groupby("aile")[["base", "alt"]].median().round(3).T.to_string())
