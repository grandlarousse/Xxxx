"""v_YG2_a ortak: panel yükleme, değişken türetme, istatistik (bağımsız; ll.py kullanılmaz)."""
import numpy as np, pandas as pd, os
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
RES = SCR + "/out/code_v_YG2_a/res"
LIM = 0.105  # h1 dönemi (2023-11+) fiyat marjı ±%10 -> kurumsal işlem eşiği ±%10,5


def tick_spot(p):
    """BIST pay piyasası fiyat adımı tablosu (yaklaşık)."""
    p = np.asarray(p, float)
    return np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)


def lg(a, b):
    x = np.log(a / b)
    x[np.abs(np.exp(x) - 1) > LIM] = np.nan
    return x


def load():
    P = pd.read_parquet(RES + "/panel.parquet").sort_values(["stock", "date"]).reset_index(drop=True)
    g = P.groupby("stock", sort=False)
    nx = lambda col, k=1: g[col].shift(-k)
    P["CA"] = lg(P["C"], P["P1500"])
    P.loc[~P["summer"] | P["half"], "CA"] = np.nan
    P["L30"] = lg(P["P1500"], P["P1430"]); P.loc[~P["summer"] | P["half"], "L30"] = np.nan
    P["DAY"] = lg(P["P1430"], P["O"]); P.loc[P["half"], "DAY"] = np.nan
    P["LH"] = lg(P["C"], P["P1430"]); P.loc[P["half"], "LH"] = np.nan
    P["CC"] = lg(P["C"], g["C"].shift(1))
    P["GAP"] = lg(P["O"], g["C"].shift(1))
    # ertesi gün parçaları (hepsi C_t'ye göre, ±%10,5 filtresi)
    O1, C1, P7, P8, P14 = nx("O"), nx("C"), nx("P0730"), nx("P0830"), nx("P1430")
    VW1 = (nx("fb_h") + nx("fb_l") + nx("P0730")) / 3.0  # ilk barın (06:30-07:30) tipik fiyatı; açılış müzayedesi dahil
    P["y_gap"] = lg(O1, P["C"])
    P["y_c730"] = lg(P7, P["C"])
    P["y_o730"] = P["y_c730"] - P["y_gap"]
    P["y_c830"] = lg(P8, P["C"])
    P["y_c1430"] = lg(P14, P["C"])
    P["y_cc"] = lg(C1, P["C"])
    P["y_730c"] = P["y_cc"] - P["y_c730"]
    P["y_cvw"] = lg(VW1, P["C"])
    P["y_cc2"] = lg(nx("C", 2), C1)  # t+2 günü (kalıcılık)
    P["next_half"] = nx("half").astype(float)
    P["next_summer"] = nx("summer").astype(float)
    P["year"] = P["date"].dt.year
    return P


def liquidity(P):
    """spot ciro (C*V) medyanı, h1 dönemi; hacmi eksik günler (SASA) hariç."""
    x = P[P["V"] > 0].assign(to=lambda d: d["C"] * d["V"])
    to = x.groupby("stock")["to"].median() / 1e6
    return to.sort_values(ascending=False)


def ssf_liq():
    v = pd.read_parquet(SCR + "/data/viop_panel.parquet", columns=["date", "root", "segment", "value_tl"])
    v = v[(v.segment == "SSF") & (v.date >= "2023-12-01")]
    s = v.groupby(["root", "date"])["value_tl"].sum().groupby("root").median() / 1e6
    return s


def ols_cl(y, X, groups):
    """OLS + küme-dayanıklı (gün kümelenmiş) SE. X sabitsiz verilir, sabit eklenir."""
    X = np.column_stack([np.ones(len(y)), X])
    iXX = np.linalg.pinv(X.T @ X)
    b = iXX @ X.T @ y; u = y - X @ b
    gi = pd.factorize(groups)[0]; G = gi.max() + 1
    S = np.zeros((G, X.shape[1])); np.add.at(S, gi, X * u[:, None])
    V = iXX @ (S.T @ S) @ iXX * G / (G - 1) * (len(y) - 1) / (len(y) - X.shape[1])
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    return b, se, len(y), G


def nw_t(x, L=5):
    x = np.asarray(pd.Series(x).dropna(), float); n = len(x)
    if n < 10: return np.nan, np.nan, n
    m = x.mean(); e = x - m
    s = e @ e / n
    for k in range(1, L + 1):
        w = 1 - k / (L + 1); s += 2 * w * (e[k:] @ e[:-k]) / n
    return m, m / np.sqrt(s / n), n


def port(P, sig_col, y_col, thr, mask=None, cost=None):
    """pos = -sign(sig) |sig|>thr; gün içi eşit ağırlık ortalama; dönüş: günlük seri (bps), işlem sayısı."""
    d = P if mask is None else P[mask]
    d = d[[sig_col, y_col, "date"] + (["cost"] if cost is not None else [])].dropna(subset=[sig_col, y_col])
    d = d[d[sig_col].abs() > thr]
    pnl = -np.sign(d[sig_col]) * d[y_col] * 1e4
    if cost is not None: pnl = pnl - d["cost"]
    daily = pnl.groupby(d["date"]).mean()
    return daily, len(d), pnl
