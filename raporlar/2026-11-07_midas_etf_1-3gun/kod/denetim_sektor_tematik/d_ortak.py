"""Denetim (sektor_tematik): bağımsız işlem simülatörü ve istatistikler.
lib.trades / lib.evaluate KULLANILMAZ. Fiyatlar lib.load'dan (toplam getiri düzeltmeli o/h/l/c) alınır.
IBS ayrıca ham (düzeltilmemiş) parquet'ten de hesaplanıp karşılaştırılır."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_sektor_tematik", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
COMM = 1.5

_D = {}


def D(sym):
    if sym not in _D:
        _D[sym] = lib.load(sym)
    return _D[sym]


def raw(sym):
    df = pd.read_parquet(os.path.join(lib.DATA, "etf", sym + ".parquet"))
    return df[df["c"] > 0]


def my_ibs(df):
    """IBS = (C-L)/(H-L); H==L ise NaN (sinyal yok)."""
    rng = df["h"] - df["l"]
    x = (df["c"] - df["l"]) / rng.where(rng > 0)
    return x.clip(0, 1)


def spread_tier(sym):
    """tarama.csv'deki ile aynı mantık bağımsız yazıldı: son 252 gün medyan $ hacim kademesi + 1 sent tabanı."""
    df = D(sym).tail(252)
    dv = float(np.nanmedian(df["dv"]))
    px = float(df["raw_c"].iloc[-1])
    tier = 1 if dv > 1e9 else 2 if dv > 2e8 else 4 if dv > 5e7 else 8 if dv > 1e7 else 15 if dv > 2e6 else 35
    return max(tier, 1e4 * 0.01 / px)


def cost(sym, pos=2500.0):
    return 2 * COMM / pos * 1e4 + spread_tier(sym)


def sim(df, sig, h=1, mode="C0", cost_bp=0.0):
    """Kendi simülatörüm. sig: t kapanışında bilinen bool. Çakışmasız: pozisyon kapanana kadar gelen sinyal yok.
    C0: giriş c[t], çıkış c[t+h].  O1: giriş o[t+1], çıkış c[t+h] (h=1 -> gün içi).  C1: giriş c[t+1], çıkış c[t+1+h].
    Çıkış günü gelen sinyal yeni işlem açabilir (lib ile aynı sayım; tam maliyet tekrar düşülür)."""
    s = sig.reindex(df.index).fillna(False).astype(bool).values
    c = df["c"].values; o = df["o"].values; idx = df.index; n = len(df)
    rows = []; free_from = 0
    for i in range(n):
        if i < free_from or not s[i]:
            continue
        if mode == "C0":
            e, ep, x = i, c[i], i + h
        elif mode == "O1":
            e = i + 1
            if e >= n: break
            ep, x = o[e], i + h
        elif mode == "C1":
            e = i + 1
            if e >= n: break
            ep, x = c[e], i + 1 + h
        else:
            raise ValueError(mode)
        if x >= n: break
        g = c[x] / ep - 1.0
        rows.append((idx[i], idx[e], idx[x], g, g - cost_bp / 1e4))
        free_from = x
    return pd.DataFrame(rows, columns=["sig_date", "entry_date", "exit_date", "gross", "net"])


def sim_hold(df, sig, cost_bp=0.0):
    """Ajanın pratik kuralı: sinyal günü kapanışta al; her kapanışta sinyal sürüyorsa tut, sürmüyorsa sat.
    Pozisyon başına tek maliyet."""
    s = sig.reindex(df.index).fillna(False).astype(bool).values
    c = df["c"].values; idx = df.index; n = len(df)
    rows = []; i = 0
    while i < n:
        if not s[i]:
            i += 1; continue
        j = i + 1
        while j < n and s[j]:
            j += 1
        if j >= n: break
        g = c[j] / c[i] - 1.0
        rows.append((idx[i], idx[i], idx[j], g, g - cost_bp / 1e4, j - i))
        i = j  # j'de sinyal yok; j+1'den devam
    return pd.DataFrame(rows, columns=["sig_date", "entry_date", "exit_date", "gross", "net", "days"])


def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))


def st(tr, label=""):
    r = {"label": label, "n": len(tr)}
    if len(tr) < 3: return r
    g = tr["gross"].values; ne = tr["net"].values
    r["brut_bp"] = g.mean() * 1e4; r["net_bp"] = ne.mean() * 1e4; r["t"] = tt(ne)
    r["kazanma"] = float((ne > 0).mean())
    lo = -ne[ne < 0].sum(); r["pf"] = float(ne[ne > 0].sum() / lo) if lo > 0 else np.inf
    eq = np.cumprod(1 + ne); r["maxdd"] = float((eq / np.maximum.accumulate(eq) - 1).min())
    r["en_kotu_bp"] = float(ne.min() * 1e4); r["en_iyi_bp"] = float(ne.max() * 1e4)
    d = pd.to_datetime(tr["sig_date"])
    for nm, m in (("is", d <= IS_END), ("oos", d > IS_END)):
        x = ne[m.values]
        r[nm + "_n"] = len(x); r[nm + "_net_bp"] = x.mean() * 1e4 if len(x) else np.nan; r[nm + "_t"] = tt(x)
    y = tr.groupby(d.dt.year)["net"].sum()
    r["yil_poz"] = float((y > 0).mean()); r["n_yil"] = len(y)
    return r


def p_from_t(t, n):
    from scipy import stats as S
    if not np.isfinite(t): return np.nan
    return float(2 * S.t.sf(abs(t), max(n - 1, 1)))


def bh(p, q=0.10):
    p = np.asarray(p, float); ok = np.isfinite(p); m = ok.sum()
    order = np.argsort(np.where(ok, p, 9.0)); k_ok = 0
    for k, ix in enumerate(order[:m], 1):
        if p[ix] <= q * k / m: k_ok = k
    out = np.zeros(len(p), bool); out[order[:k_ok]] = True
    return out


def nw_t(y, X, lags=5):
    """OLS + Newey-West (Bartlett) t'leri. X sabit içermeli."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    ok = np.isfinite(y) & np.isfinite(X).all(1); y = y[ok]; X = X[ok]
    n, k = X.shape
    XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; u = y - X @ b
    Xu = X * u[:, None]; S = Xu.T @ Xu
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = Xu[L:].T @ Xu[:-L]; S += w * (G + G.T)
    V = XtX @ S @ XtX
    return b, b / np.sqrt(np.diag(V)), n
