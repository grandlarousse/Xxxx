"""BT6 (saatlik, İş h1 2017–2026): lider endeks saatlik barı (|z|>1, z geçmiş 500 bar) -> takipçi endeksin SONRAKİ 3 bar (gün içinde) getirisi.
Yön IS'te (2017–2020) seçilir; OOS 2021–2026. Maliyet 4 (endeks vadelisi gerçekçi), 8, 15 bps gidiş-dönüş.
UYARI: spot endeks işlenemez; VİOP'ta XU030D, XLBNKD, X10XBD var (XUSIN/XKMYA vadelisi YOK). Vadeli, spotu genellikle önceler -> spot üzerindeki sonuç iyimser üst sınırdır."""
import sys; sys.argv = ["x", "isy", "h1"]
import s4_intraday as S4
from ye_common import *
H = 3
def run(lead, fol, thr=1.0):
    a = S4.bar_ret(S4.px(lead)); b = S4.bar_ret(S4.px(fol))
    df = pd.concat([a["r"].rename("x"), b["r"].rename("y"), a["date"]], axis=1, join="inner").dropna(subset=["x"])
    mu = df["x"].rolling(500, min_periods=200).mean().shift(1); sd = df["x"].rolling(500, min_periods=200).std().shift(1); z = (df["x"] - mu) / sd
    fwd = pd.Series(0.0, index=df.index); cnt = pd.Series(0, index=df.index)
    for k in range(1, H + 1):
        yk = df["y"].shift(-k); same = df["date"].shift(-k) == df["date"]
        fwd = fwd + yk.where(same, 0).fillna(0); cnt = cnt + (same & yk.notna()).astype(int)
    sig = np.sign(z).where(z.abs() > thr, 0)
    g = (sig * fwd)[(sig != 0) & (cnt > 0)]
    isg = g[g.index < SPLIT]; sgn = 1 if isg.mean() >= 0 else -1; g = sgn * g
    out = []
    for c in [0, 4, 8, 15]:
        p = g - c / 1e4
        r = {"lead": lead, "follower": fol, "cost": c, "sign": sgn}
        for k, msk in [("IS", p.index < SPLIT), ("OOS", p.index >= SPLIT)]:
            q = p[msk]; r[f"{k}_n"] = len(q); r[f"{k}_mean_bps"] = 1e4 * q.mean(); r[f"{k}_t"] = q.mean() / q.std() * np.sqrt(len(q)) if len(q) > 10 else np.nan
        r["by_year"] = str((1e4 * p.groupby(p.index.year).mean()).round(1).to_dict()); out.append(r)
    return out
rows = []
for a, b in [("XBANK", "XUSIN"), ("XLBNK", "X10XB"), ("XBANK", "XU030"), ("XU030", "XU030"), ("XBANK", "XKMYA"), ("XUSIN", "XBANK"), ("XU030", "XTUMY")]:
    rows += run(a, b)
R = pd.DataFrame(rows); R.to_csv(RES + "/bt_h1_idx.csv", index=False)
pd.set_option("display.width", 250); print(R.drop(columns="by_year").round(2).to_string())
print(R[(R.cost == 4)][["lead", "follower", "by_year"]].to_string())

# BT6b: rölatif (spread) sinyal: (takipçi - lider) son bar -> takipçi sonraki 3 bar ve spread (takipçi - lider) sonraki 3 bar
def run_spread(lead, fol, thr=1.0):
    a = S4.bar_ret(S4.px(lead)); b = S4.bar_ret(S4.px(fol))
    df = pd.concat([a["r"].rename("x"), b["r"].rename("y"), a["date"]], axis=1, join="inner").dropna(subset=["x", "y"])
    s = df["y"] - df["x"]; mu = s.rolling(500, min_periods=200).mean().shift(1); sd = s.rolling(500, min_periods=200).std().shift(1); z = (s - mu) / sd
    out = []
    for tn, tgt in [("follower", df["y"]), ("spread", df["y"] - df["x"])]:
        fwd = sum(tgt.shift(-k).where(df["date"].shift(-k) == df["date"], 0).fillna(0) for k in range(1, H + 1))
        sig = np.sign(z).where(z.abs() > thr, 0); g = (sig * fwd)[sig != 0]
        sgn = 1 if g[g.index < SPLIT].mean() >= 0 else -1; g = sgn * g
        for c in [0, 4, 8]:
            cc = c * (2 if tn == "spread" else 1); p = g - cc / 1e4
            r = {"lead": lead, "follower": fol, "target": tn, "cost_per_leg": c, "sign": sgn}
            for k, msk in [("IS", p.index < SPLIT), ("OOS", p.index >= SPLIT)]:
                q = p[msk]; r[f"{k}_n"] = len(q); r[f"{k}_mean_bps"] = 1e4 * q.mean(); r[f"{k}_t"] = q.mean() / q.std() * np.sqrt(len(q)) if len(q) > 10 else np.nan
            out.append(r)
    return out
rs = []
for a, b in [("XBANK", "XUSIN"), ("XLBNK", "X10XB")]:
    rs += run_spread(a, b)
RS = pd.DataFrame(rs); RS.to_csv(RES + "/bt_h1_spread.csv", index=False); print(RS.round(2).to_string())
