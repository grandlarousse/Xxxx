"""Endeks bileşen ağırlıklarının (yaklaşık) tahmini: NNLS ile endeks basit getirisi = Σ w_i r_i (+ kalıntı).
Aday evren: veri setindeki ~176 BIST hissesi. Pencere: çeyrek başından ÖNCEKİ 250 işlem günü (look-ahead yok) -> o çeyreğe uygulanır.
Amaç: 'mekanik içerme' ayrıştırması: endeks_ex_hisse = (r_I - w r_s) / (1 - w).
Çıktı: results/weights.parquet (index=çeyrek başı, MultiIndex sütun (endeks, hisse)), results/weights_fit.csv (R², Σw)."""
import numpy as np, pandas as pd
from scipy.optimize import nnls
from ye_common import *

cat = pd.read_csv(SCR + "/data/catalog.csv"); B = cat[cat.group.isin(["VIOP", "BIST_other"])].sym
STK = [s for s in B if not s.startswith("X")]
R = pd.concat({s.replace(".IS", ""): stk_ret(s) for s in STK}, axis=1)
R = R[(R.index >= "2012-06-01")]
Rs = np.exp(R) - 1
TARGET = [k for k in IDX_DESC if os.path.exists(f"{ISY}/d/{k}.parquet")]
qs = pd.date_range("2014-01-01", "2026-10-01", freq="QS")
W = {}; fit = []
for I in TARGET:
    ri = np.exp(idx_ret(I)) - 1
    for q in qs:
        win = Rs[Rs.index < q].tail(250)
        y = ri.reindex(win.index)
        if y.notna().sum() < 200: continue
        okc = win.notna().sum() >= 200
        X = win.loc[:, okc]
        m = y.notna()
        Xv = X[m].fillna(0.0).values; yv = y[m].values
        w, _ = nnls(Xv, yv, maxiter=3000)
        e = yv - Xv @ w; r2 = 1 - e.var() / yv.var()
        ws = pd.Series(w, index=X.columns); ws = ws[ws > 1e-4]
        for s, v in ws.items(): W[(I, s, q)] = v
        fit.append((I, q, r2, ws.sum(), len(ws), ws.sort_values().index[-1], ws.max()))
    print(I, "ok", flush=True)
w = pd.Series(W); w.index.names = ["idx", "stk", "q"]
w = w.unstack(["idx", "stk"]).sort_index()
w.to_parquet(RES + "/weights.parquet")
f = pd.DataFrame(fit, columns=["idx", "q", "r2", "sumw", "n_pos", "top", "top_w"]); f.to_csv(RES + "/weights_fit.csv", index=False)
print(f.groupby("idx")[["r2", "sumw", "n_pos", "top_w"]].median().round(3))
last = w.iloc[-1]
for I in ["XU030", "XBANK", "XHOLD", "XUSIN"]:
    print(I, last[I].dropna().sort_values(ascending=False).head(8).round(3).to_dict())
