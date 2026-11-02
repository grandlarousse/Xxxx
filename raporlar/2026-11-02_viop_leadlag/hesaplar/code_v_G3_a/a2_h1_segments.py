"""A2: Saatlik (h1, 2023-12..2026-10) ile gün-içi negatif kaymanın NEREDE oluştuğu + alternatif giriş/çıkış.
Bar zamanı = bar başlangıcı (UTC). BIST h1: 06:30 (=06:55 açılış müzayedesi + 07:00-07:30), 07:30..13:30, yazın 14:30 (14:30-15:00), 15:00 kapanış barı nadiren.
Segmentler: open(günlük o) -> 07:30 ; 07:30 -> 08:30 ; ... ; son sürekli fiyat (yaz 15:00, kış 14:30) ; -> günlük kapanış (kapanış müzayedesi [+kışın son 30 dk]).
Strateji varyantları (hep 'sat, sonra kapat'): A open->close ; B 07:30->close ; C 08:30->close ; D open->son sürekli ; E 07:30->son sürekli ; F son sürekli->close (kapanış müzayedesi)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)

def build(sym):
    d = decomp(sym, start="2023-11-01")
    h = h1(sym)
    h = h[h.hm != "15:00"]
    piv = h.pivot_table(index="ldate", columns="hm", values="c", aggfunc="last")
    o1 = h[h.hm == "06:30"].set_index("ldate")["o"]
    last_hm = h.groupby("ldate")["hm"].max()
    lastc = h.sort_index().groupby("ldate")["c"].last()
    X = pd.DataFrame(index=piv.index)
    X["o"] = d["o"].reindex(X.index); X["c"] = d["c"].reindex(X.index); X["cp"] = d["c"].shift(1).reindex(X.index)
    X["intra_ok"] = d["intra"].reindex(X.index).notna()
    X["h1o"] = o1.reindex(X.index)
    for k in piv.columns: X["c" + k] = piv[k]
    X["lastc"] = lastc; X["last_hm"] = last_hm
    X = X[X.intra_ok & X.index.isin(d.index)]
    # tam gün: 13:30 barı olmalı (yarım günleri çıkar)
    X = X[X["c13:30"].notna()]
    return X

def segs(X):
    L = np.log
    out = pd.DataFrame(index=X.index)
    out["gap"] = L(X.o / X.cp)
    out["o_0730"] = L(X["c06:30"] / X.o)
    prev = "c06:30"
    for k in ["07:30", "08:30", "09:30", "10:30", "11:30", "12:30", "13:30"]:
        out[f"s{k}"] = L(X["c" + k] / X[prev]); prev = "c" + k
    out["s14:30"] = L(X["c14:30"] / X["c13:30"])  # yazın; kışın NaN
    out["last_close"] = L(X.c / X.lastc)
    out["intra"] = L(X.c / X.o)
    out["summer"] = X["c14:30"].notna()
    out["A"] = -L(X.c / X.o); out["B"] = -L(X.c / X["c06:30"]); out["C"] = -L(X.c / X["c07:30"])
    out["D"] = -L(X.lastc / X.o); out["E"] = -L(X.lastc / X["c06:30"]); out["F"] = -L(X.c / X.lastc)
    return out

res = {}
for sym in ["XU030.IS", "XU100.IS", "XBANK.IS"] + [s + ".IS" for s in STOCKS]:
    try:
        X = build(sym); res[sym] = (X, segs(X))
    except Exception as e:
        print("hata", sym, e)
pd.to_pickle(res, R + "/a2_res.pkl")
# Açılış kontrolü
print("== Açılış kontrolü: günlük o vs h1 06:30 o (eşit oran), h1 o vs önceki kapanış (eşit oran)")
rows = []
for sym, (X, Z) in res.items():
    rows.append(dict(sym=sym, n=len(X), o_eq_h1o=(np.abs(X.o / X.h1o - 1) < 1e-4).mean(), h1o_eq_cp=(np.abs(X.h1o / X.cp - 1) < 1e-4).mean(),
                     o_eq_cp=(np.abs(X.o / X.cp - 1) < 1e-6).mean()))
A = pd.DataFrame(rows); print(A.head(5).round(3).to_string()); print("47 hisse medyan:", A.iloc[3:][["o_eq_h1o", "h1o_eq_cp", "o_eq_cp"]].median().round(3).to_dict())
# Segment ortalamaları
cols = ["gap", "o_0730", "s07:30", "s08:30", "s09:30", "s10:30", "s11:30", "s12:30", "s13:30", "s14:30", "last_close", "intra"]
def tab(Z, sl=None):
    z = Z if sl is None else Z.loc[sl]
    return pd.DataFrame({"bps": 1e4 * z[cols].mean(), "t": z[cols].apply(tstat), "n": z[cols].notna().sum()})
for sym in ["XU030.IS", "XU100.IS"]:
    print("\n==", sym, "segment ortalamaları (bps/gün)"); print(tab(res[sym][1]).round(2).T.to_string())
    Z = res[sym][1]
    print("  yaz:", tab(Z[Z.summer]).round(2).loc[["last_close", "intra"]].T.to_string())
    print("  kış:", tab(Z[~Z.summer]).round(2).loc[["last_close", "intra"]].T.to_string())
# EW 47
EW = pd.concat({s: res[s + ".IS"][1][cols] for s in STOCKS if s + ".IS" in res}, axis=1)
ew = EW.T.groupby(level=1).mean().T
print("\n== 47 hisse EW segment ortalamaları"); print(pd.DataFrame({"bps": 1e4 * ew.mean(), "t": ew.apply(tstat)}).round(2).T.to_string())
# Hisse bazında segment medyanları
med = pd.DataFrame({s: 1e4 * res[s + ".IS"][1][cols].mean() for s in STOCKS if s + ".IS" in res}).T
print("hisse medyanları:"); print(med.median().round(2).to_string())
print("o_0730<0 hisse oranı", (med.o_0730 < 0).mean().round(2), " last_close<0 oranı", (med.last_close < 0).mean().round(2))
# Strateji varyantları
print("\n== Strateji varyantları (sat-kapat), brüt bps/gün, t; IS<2025-07 / OOS>=2025-07")
rows = []
for sym in ["XU030.IS", "XU100.IS", "XBANK.IS"]:
    Z = res[sym][1]
    for v in "ABCDEF":
        for nm, sl in [("all", slice(None)), ("IS", slice(None, "2025-06-30")), ("OOS", slice("2025-07-01", None))]:
            s = Z[v].loc[sl].dropna()
            rows.append(dict(sym=sym, var=v, per=nm, n=len(s), bps=1e4 * s.mean(), t=tstat(s)))
ewv = pd.concat({s: res[s + ".IS"][1][list("ABCDEF")] for s in STOCKS if s + ".IS" in res}, axis=1).T.groupby(level=1).mean().T
for v in "ABCDEF":
    for nm, sl in [("all", slice(None)), ("IS", slice(None, "2025-06-30")), ("OOS", slice("2025-07-01", None))]:
        s = ewv[v].loc[sl].dropna(); rows.append(dict(sym="EW47", var=v, per=nm, n=len(s), bps=1e4 * s.mean(), t=tstat(s)))
V = pd.DataFrame(rows); print(V.pivot_table(index=["sym", "var"], columns="per", values=["bps", "t"]).round(2).to_string())
V.to_csv(R + "/a2_variants.csv", index=False)
