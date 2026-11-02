"""Adım 7 (ek): Gün-içi saatlik lead-lag (60 dk, 2023-11..2026-10). lider r_{h-1} -> hedef r_h (aynı gün; gece hariç),
kontroller: hedef r_{h-1}, XU100 r_{h-1}. Liderler: h1'de verisi olan tüm BIST hisseleri (~93). BH-FDR; iki yarı (H1: <2025-05, H2: >=2025-05).
Bar: BIST barları :30'da başlar (06:30..13:30, 14:30 kısmen); 15:00 kapanış barı neredeyse hiç yok -> kapanış seansı dahil değil.
Çıktı: res/hourly.txt, res/hourly_long.parquet
"""
import sys, os, glob, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata, hreg
sys.path.insert(0, hdata.SCR + "/code"); import ll
H = hdata.SCR + "/data/h1"
syms = sorted(os.path.basename(f)[:-11] for f in glob.glob(H + "/*.IS.parquet"))
stocks = [s for s in syms if not (s.startswith("X") and s not in ("XU100",))]
stocks = [s for s in stocks if s != "XU100"]
def bars(s):
    d = pd.read_parquet(f"{H}/{s}.IS.parquet")
    d = d[~d.index.duplicated(keep="last")]
    d = d[(d.index.minute == 30)]  # 15:00 kapanış barını at (çok seyrek)
    day = d.index.tz_convert(None).normalize()
    c = d["c"]; o = d["o"]
    prev = c.groupby(day).shift(1)
    r = np.log(c / prev)
    first = prev.isna()
    r[first] = np.log(c[first] / o[first])  # ilk bar: açılıştan (gece gap hariç)
    r[(c <= 0) | (r.abs() > 0.08)] = np.nan
    return r, day
R = {}; DAY = None
for s in stocks + ["XU100"]:
    r, day = bars(s); R[s] = r
P = pd.DataFrame(R).sort_index()
P = P[P.index >= pd.Timestamp("2023-12-01", tz="UTC")]
day = pd.Series(P.index.tz_convert(None).normalize(), index=P.index)
same = (day == day.shift(1)).values
L1 = P.shift(1); L1[~same] = np.nan
TG = [t for t in hdata.VIOP if t in P]
LD = [s for s in stocks if s in P]
half = P.index < pd.Timestamp("2025-05-01", tz="UTC")
rows = []
for j in TG:
    C = np.column_stack([L1[j].values, L1["XU100"].values])
    for pn, pm in [("FULL", np.ones(len(P), bool)), ("H1", half), ("H2", ~half)]:
        y = np.where(pm, P[j].values, np.nan)
        r = hreg.nw_batch(y, L1[LD].values, C, min_n=500)
        rows.append(pd.DataFrame({"target": j, "leader": LD, "period": pn, "b": r["b"], "t": r["t"], "pc": r["pc"], "n": r["n"]}))
X = pd.concat(rows); X = X[X.target != X.leader]
W = X.pivot_table(index=["target", "leader"], columns="period", values=["b", "t", "pc"]).reset_index()
W.columns = ["_".join([a for a in c if a]) for c in W.columns]
W["p"] = 2 * stats.norm.sf(W.t_FULL.abs()); W["bh"] = ll.fdr(W.p.values, 0.05)[0]
W.to_parquet(os.path.join(hdata.RES, "hourly_long.parquet"))
out = [f"Saatlik tarama: {len(TG)} hedef x {len(LD)} lider = {W.t_FULL.notna().sum()} test; bar sayısı {len(P)}; gün {day.nunique()}",
       f"p<0,05: {(W.p<0.05).sum()} (beklenen ~{0.05*W.t_FULL.notna().sum():.0f}); |t|>3: {(W.t_FULL.abs()>3).sum()}; BH05: {W.bh.sum()} (pozitif {(W.bh & (W.t_FULL>0)).sum()})",
       f"BH keşiflerinde iki yarı aynı işaret: {100*(np.sign(W.loc[W.bh,'t_H1'])==np.sign(W.loc[W.bh,'t_H2'])).mean():.0f}%; H2'de |t|>2 & aynı işaret: {100*((np.sign(W.loc[W.bh,'t_H1'])==np.sign(W.loc[W.bh,'t_H2']))&(W.loc[W.bh,'t_H2'].abs()>2)).mean():.0f}%"]
# H1-seçim -> H2 replikasyon
w1 = W.dropna(subset=["t_H1", "t_H2"]).copy(); w1["a"] = w1.t_H1.abs(); top = w1.nlargest(200, "a")
out.append(f"H1 top-200 -> H2 aynı işaret & p<0,05: {100*((np.sign(top.t_H1)==np.sign(top.t_H2))&(top.t_H2.abs()>1.96)).mean():.1f}% (null ≈ %2,5)")
# lider skorları
g = W[W.bh].groupby("leader").agg(n=("bh", "size"), pos=("t_FULL", lambda s: int((s > 0).sum())))
out.append("Saatlik lider sayımları (BH keşif, + sayısı):\n" + g.sort_values("n", ascending=False).head(20).to_string())
gt = W[W.bh].groupby("target").size().sort_values(ascending=False)
out.append("Saatlik takipçi sayımları:\n" + gt.head(20).to_string())
W["a"] = W.t_FULL.abs()
out.append("En güçlü 30:\n" + W.sort_values("a", ascending=False)[["target", "leader", "b_FULL", "t_FULL", "pc_FULL", "t_H1", "t_H2"]].head(30).round(3).to_string(index=False))
# ekonomik çiftler saatlik
EP = [("THYAO", "PGSUS"), ("PGSUS", "THYAO"), ("THYAO", "TAVHL"), ("TAVHL", "THYAO"), ("THYAO", "CLEBI"), ("TUPRS", "PETKM"), ("EREGL", "KRDMD"), ("KRDMD", "EREGL"),
      ("EREGL", "ISDMR"), ("AKBNK", "GARAN"), ("GARAN", "AKBNK"), ("AKBNK", "YKBNK"), ("YKBNK", "AKBNK"), ("ISCTR", "YKBNK"), ("GARAN", "YKBNK"), ("HALKB", "VAKBN"), ("VAKBN", "HALKB"),
      ("FROTO", "TOASO"), ("TOASO", "FROTO"), ("ASTOR", "EUPWR"), ("EUPWR", "ASTOR"), ("BIMAS", "MGROS"), ("MGROS", "SOKM"), ("GUBRF", "HEKTS"), ("CIMSA", "OYAKC"), ("OYAKC", "CIMSA"),
      ("TCELL", "TTKOM"), ("TTKOM", "TCELL"), ("KCHOL", "SAHOL"), ("SAHOL", "KCHOL"), ("TRALT", "TRMET"), ("TRMET", "TRALT"), ("TRENJ", "TRMET"), ("TRENJ", "TRALT"), ("AKBNK", "SAHOL")]
er = []
for a, b in EP:
    x = W[(W.leader == a) & (W.target == b)]
    if len(x): er.append(x[["leader", "target", "b_FULL", "t_FULL", "pc_FULL", "t_H1", "t_H2", "bh"]])
ER = pd.concat(er); ER.to_csv(os.path.join(hdata.RES, "hourly_pairs.csv"), index=False)
out.append("Ekonomik çiftler (saatlik, lider r_{h-1} -> hedef r_h):\n" + ER.round(3).to_string(index=False))
# basit backtest: en güçlü 5 (H1 seçimli) çift, sign(lider_{h-1}) -> hedef_h, maliyet 8 bps
bt = []
for _, rr in top.head(5).iterrows():
    s = np.sign(rr.t_H1) * L1[rr.leader]; y = P[rr.target]
    d = pd.concat([s, y], axis=1).dropna(); d = d[d.index >= pd.Timestamp("2025-05-01", tz="UTC")]
    pnl = np.sign(d.iloc[:, 0]) * d.iloc[:, 1]
    bt.append(f"{rr.leader}->{rr.target}: H2 brüt ort {1e4*pnl.mean():.2f} bps/bar (n={len(pnl)}), 8 bps maliyetle {1e4*(pnl.mean()-8e-4):.1f}")
out.append("H1-seçimli en iyi 5 saatlik çift, H2 brüt getiri:\n" + "\n".join(bt))
txt = "\n".join(out); open(os.path.join(hdata.RES, "hourly.txt"), "w").write(txt); print(txt)
