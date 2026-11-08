"""Denetim (metal_madenci) — bağımsız işlem simülasyonu.
lib.trades / lib.evaluate / mm.full KULLANILMAZ. Yalnız fiyat için lib.load çağrılır.

Zamanlama (sözleşmeyle aynı, ama ayrı yazıldı):
  sinyal i günü kapanışında bilinir.
  C0: giriş c[i], çıkış c[i+h]
  O1: giriş o[i+1], çıkış c[i+h]   (h=1 -> gün içi)
  C1: giriş c[i+1], çıkış c[i+1+h]
  Çakışma yok: pozisyon açıkken (giriş günü .. çıkış gününden önceki gün) gelen sinyal atlanır;
  çıkış günündeki sinyal yeniden giriş sayılır (lib ile aynı kural; ayrıca 'katı' varyant da var).
Maliyet: 2*1,5$/poz + makas kademesi (son 252 gün medyan dolar hacmi) — ya da tarihsel (o günkü
  geçmiş 252 gün) kademe ile 'dinamik' maliyet.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
if KOD not in sys.path:
    sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = os.path.dirname(KOD)
OUTD = os.path.join(ROOT, "sonuclar", "aile_metal_madenci", "denetim")
os.makedirs(OUTD, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")

_cache = {}
def px(sym, drop=()):
    k = (sym, tuple(drop))
    if k not in _cache:
        d = lib.load(sym)
        for x in drop:
            d = d.drop(pd.Timestamp(x), errors="ignore")
        _cache[k] = d
    return _cache[k].copy()

def tier_bp(dv_med, price):
    t = 1 if dv_med > 1e9 else 2 if dv_med > 2e8 else 4 if dv_med > 5e7 else 8 if dv_med > 1e7 else 15 if dv_med > 2e6 else 35
    tick = 1e4 * 0.01 / price if price and price > 0 else 10
    return max(t, tick)

def cost_static(df, pos=2500.0):
    t = df.tail(252)
    return 2 * 1.5 / pos * 1e4 + tier_bp(float(np.nanmedian(t["dv"])), float(t["raw_c"].iloc[-1]))

def cost_dynamic(df, pos=2500.0):
    """Her gün için o güne kadarki 252 günlük medyan dolar hacim ve o günkü ham fiyatla makas (ileriye bakmaz)."""
    dvm = df["dv"].rolling(252, min_periods=60).median().bfill()
    out = np.array([tier_bp(a, b) for a, b in zip(dvm.values, df["raw_c"].values)])
    return pd.Series(2 * 1.5 / pos * 1e4 + out, index=df.index)

def sim(df, sig, h=3, mode="C0", cost=14.0, strict=False):
    """cost: skaler bp ya da tarih indeksli Seri (giriş gününün değeri kullanılır)."""
    s = sig.reindex(df.index).fillna(False).astype(bool).values
    o = df["o"].values; c = df["c"].values; idx = df.index; n = len(df)
    cs = cost.reindex(df.index).values if isinstance(cost, pd.Series) else None
    rows = []; busy_until = -1   # son çıkış indeksi
    for i in range(n):
        if not s[i]:
            continue
        if strict:
            if i <= busy_until: continue
        else:
            if i < busy_until: continue
        if mode == "C0":
            e, ep, x = i, c[i], i + h
        elif mode == "O1":
            e, x = i + 1, i + h
            if e >= n: break
            ep = o[e]
        elif mode == "C1":
            e, x = i + 1, i + 1 + h
            if e >= n: break
            ep = c[e]
        if x >= n: break
        g = c[x] / ep - 1
        cb = cs[e] if cs is not None else cost
        rows.append((idx[i], idx[e], idx[x], ep, c[x], g, g - cb / 1e4))
        busy_until = x
    return pd.DataFrame(rows, columns=["sig", "entry", "exit", "ep", "xp", "gross", "net"])

def tstat(x):
    x = np.asarray(x, float); n = len(x)
    if n < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(n))

def summ(tr, label=""):
    if len(tr) == 0: return {"label": label, "n": 0}
    g = tr["gross"].values; ne = tr["net"].values
    w = ne[ne > 0].sum(); l = -ne[ne < 0].sum()
    eq = np.cumprod(1 + ne); dd = (eq / np.maximum.accumulate(eq) - 1).min()
    isx = tr[tr["sig"] <= IS_END]["net"].values; oos = tr[tr["sig"] > IS_END]["net"].values
    yrs = tr.groupby(tr["sig"].dt.year)["net"].sum()
    return {"label": label, "n": len(ne), "gross_bp": g.mean() * 1e4, "net_bp": ne.mean() * 1e4, "t": tstat(ne),
            "win": (ne > 0).mean(), "pf": w / l if l > 0 else np.inf, "maxdd": dd, "worst_bp": ne.min() * 1e4,
            "is_n": len(isx), "is_net_bp": isx.mean() * 1e4 if len(isx) else np.nan, "is_t": tstat(isx),
            "oos_n": len(oos), "oos_net_bp": oos.mean() * 1e4 if len(oos) else np.nan, "oos_t": tstat(oos),
            "yil_poz": float((yrs > 0).mean()), "n_yil": len(yrs)}

def fwd(df, h, mode):
    c = df["c"]; o = df["o"]
    if mode == "C0": return c.shift(-h) / c - 1
    if mode == "O1": return c.shift(-h) / o.shift(-1) - 1
    return c.shift(-(1 + h)) / c.shift(-1) - 1

def perm_test(df, tr, h, mode, reps=5000, seed=7, by_year=False, start=None):
    """Rastgele giriş permütasyonu: aynı sayıda rastgele gün (aynı h, aynı mod), brüt ortalama.
    by_year=True: her yılda sinyal sayısı kadar gün çekilir (boğa yılı yoğunlaşmasını kontrol eder).
    Tek yönlü p = P(rastgele ort >= gerçek ort)."""
    rng = np.random.default_rng(seed)
    f = fwd(df, h, mode).dropna()
    if start is not None: f = f[f.index >= start]
    actual = tr["gross"].mean()
    vals = f.values; yrs = f.index.year
    if not by_year:
        k = len(tr)
        sims = np.array([vals[rng.choice(len(vals), k, replace=False)].mean() for _ in range(reps)])
    else:
        cnt = tr.groupby(tr["sig"].dt.year).size()
        pools = {y: vals[yrs == y] for y in cnt.index}
        sims = np.empty(reps)
        for r in range(reps):
            tot = 0.0; m = 0
            for y, k in cnt.items():
                p = pools[y]; k2 = min(k, len(p))
                tot += p[rng.choice(len(p), k2, replace=False)].sum(); m += k2
            sims[r] = tot / m
    return float(actual * 1e4), float(sims.mean() * 1e4), float((sims >= actual).mean())

def nw_t_reg(y, X, lags):
    """OLS + Newey-West standart hata; X sabit içermeli. Dönüş: beta, t."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    m = np.isfinite(y) & np.isfinite(X).all(axis=1); y = y[m]; X = X[m]
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b
    Xe = X * e[:, None]; S = Xe.T @ Xe / n
    for l in range(1, lags + 1):
        G = Xe[l:].T @ Xe[:-l] / n; S += (1 - l / (lags + 1)) * (G + G.T)
    V = n * XtXi @ S @ XtXi
    return b, b / np.sqrt(np.diag(V)), n
