"""Hakem: adil uç gün testi — piyasanın en büyük |v_ret| günlerini (pozisyondan bağımsız) örneklemden çıkar; B&H ile kıyasla.
Ayrıca Pearson (doğrusal) IC t ve winsorize edilmiş hedefle IC."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
from lib_altin import load_viop, load_spot, ic, backtest, fwd
d = load_viop(); s = load_spot(); ret = d.v_ret
asof = lambda x: x.reindex(x.index.union(d.index)).ffill(limit=2).reindex(d.index)
sig = {"-nom2_d5 h1": (asof(-s.ust_nom2.diff(5)), 1), "+curve_d5 h1": (asof((s.ust_nom10 - s.ust_nom2).diff(5)), 1),
       "+seg_last1h h5": (asof(np.log(s.xau_p15 / s.xau_p14)), 5)}
P2 = pd.read_parquet("/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon/preds_V2.parquet"); P2["date"] = pd.to_datetime(P2["date"])
q = P2[(P2.model == "rf") & (P2.h == 3)].set_index("date"); sig["V2 rf h3"] = ((q.yhat - q.ybar_w).reindex(d.index), 3)
P1 = pd.read_parquet("/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon/preds_V1.parquet"); P1["date"] = pd.to_datetime(P1["date"])
sig["C1 wf h1"] = (P1[(P1.model == "c1_apriori_score") & (P1.h == 1)].set_index("date").yhat.reindex(d.index), 1)
r = ret.loc["2022":].dropna()
for k in (0, 10, 20, 40):
    big = r.abs().sort_values(ascending=False).index[:k]
    rr = r.drop(big)
    bh = backtest(pd.Series(1.0, index=rr.index), rr, 1, 0)["sharpe"]
    out = {nm: round(backtest(np.sign(x).reindex(rr.index).fillna(0), rr, h)["sharpe"], 2) for nm, (x, h) in sig.items()}
    print(f"OOS, en büyük {k} |v_ret| günü çıkarıldı: B&H {bh:.2f}", out)
for nm, (x, h) in sig.items():
    y = fwd(ret, h); yw = y.clip(y.quantile(0.01), y.quantile(0.99))
    print(nm, "Spearman t", round(ic(x.loc["2017-03":], y.loc["2017-03":], max(h, 5))["t"], 2), "Pearson t", round(ic(x.loc["2017-03":], y.loc["2017-03":], max(h, 5), method="pearson")["t"], 2),
          "Pearson winsor t", round(ic(x.loc["2017-03":], yw.loc["2017-03":], max(h, 5), method="pearson")["t"], 2),
          "| OOS Spearman", round(ic(x.loc["2022":], y.loc["2022":], max(h, 5))["t"], 2), "Pearson", round(ic(x.loc["2022":], y.loc["2022":], max(h, 5), method="pearson")["t"], 2))
