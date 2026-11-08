"""Denetim (uluslararasi): bağımsız işlem simülatörü. lib.trades / lib.evaluate / ortak.pooled KULLANILMAZ.
Fiyat için yalnız lib.load (temizlenmiş, toplam getiri düzeltmeli o/h/l/c) kullanılır.
Maliyet: tarama.csv'deki spread_bp (makas) + 2 x 1,5 USD komisyon / pozisyon.
Zamanlama: sinyal t kapanışında bilinir.
  C0: giriş c[t], çıkış c[t+h]
  O1: giriş o[t+1], çıkış c[t+h]   (h=1 gün içi)
  C1: giriş c[t+1], çıkış c[t+1+h]
Çakışma: pozisyondayken gelen sinyal yok sayılır; çıkış günü gelen sinyal (C0) yeni işlem açar (yeniden giriş, ek maliyet)
  -> hold=True ile 'pozisyonu koru' (uzat, ek maliyet yok) varyantı da hesaplanır."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
ROOT = os.path.dirname(KOD)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

OUT = os.path.join(ROOT, "sonuclar", "aile_uluslararasi", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
_D = {}
def L(s):
    if s not in _D: _D[s] = lib.load(s)
    return _D[s]

_T = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")
def spread(s): return float(_T.loc[s, "spread_bp"])
def cost(s, pos=2500.0): return 2 * 1.5 / pos * 1e4 + spread(s)

def sim(s, sig, h=1, mode="C0", pos=2500.0, extra_bp=0.0, hold=False):
    """sig: bool Seri (t kapanışında bilinir). Dönüş: DataFrame sig_date, entry, exit, gross, net, sym."""
    df = L(s)
    sg = sig.reindex(df.index).fillna(False).astype(bool).to_numpy()
    o = df["o"].to_numpy(); c = df["c"].to_numpy(); ix = df.index; n = len(df)
    cb = cost(s, pos) + extra_bp
    rows = []
    t = 0
    busy_until = -1          # pozisyonun çıkış indeksine kadar (dahil değil: çıkış günü yeni sinyal serbest)
    while t < n:
        if not sg[t] or t < busy_until:
            t += 1; continue
        if mode == "C0": e, ep, x = t, c[t], t + h
        elif mode == "O1":
            if t + 1 >= n: break
            e, ep, x = t + 1, o[t + 1], t + h
        elif mode == "C1":
            if t + 1 >= n: break
            e, ep, x = t + 1, c[t + 1], t + 1 + h
        else: raise ValueError(mode)
        if x >= n: break
        if hold and mode == "C0":
            # pozisyonu koru: çıkış günü yeniden sinyal varsa çıkışı h gün uzat
            while x < n and sg[x] and x + h < n:
                x = x + h
        g = c[x] / ep - 1.0
        rows.append((ix[t], ix[e], ix[x], g, g - cb / 1e4, s))
        busy_until = x
        t = t + 1 if x <= t else x   # çıkış günü (C0) yeni sinyale açık
    return pd.DataFrame(rows, columns=["sig_date", "entry", "exit", "gross", "net", "sym"])

def nw_t(x, lags):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    if n < 5: return np.nan
    e = x - x.mean(); s = e @ e / n
    for l in range(1, lags + 1):
        s += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / math.sqrt(s / n) if s > 0 else np.nan

def simple_t(x):
    x = np.asarray(x, float); n = len(x)
    if n < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(n))

def summarize(tr, h=1, by_date=True):
    """Gün-kümeli özet (sepet): aynı sinyal günündeki işlemlerin eşit ağırlıklı ortalaması = 1 gözlem."""
    if tr is None or len(tr) == 0: return {"n_trades": 0, "n_dates": 0}
    if by_date:
        d = tr.groupby("sig_date").agg(gross=("gross", "mean"), net=("net", "mean")).sort_index()
    else:
        d = tr.set_index("sig_date")[["gross", "net"]].sort_index()
    x = d["net"].to_numpy()
    r = {"n_trades": len(tr), "n_dates": len(d), "gross_bp": d["gross"].mean() * 1e4, "net_bp": x.mean() * 1e4,
         "t_simple": simple_t(x), "t_nw": nw_t(x, max(1, h)), "win": float((x > 0).mean())}
    w = x[x > 0].sum(); lo = -x[x < 0].sum(); r["pf"] = w / lo if lo > 0 else np.inf
    eq = np.cumprod(1 + x); r["maxdd"] = float((eq / np.maximum.accumulate(eq) - 1).min())
    r["worst_bp"] = float(tr["net"].min() * 1e4); r["worst_date_bp"] = float(x.min() * 1e4)
    for nm, part in (("is", d[d.index <= IS_END]), ("oos", d[d.index > IS_END])):
        y = part["net"].to_numpy()
        r[nm + "_n"] = len(y); r[nm + "_net_bp"] = y.mean() * 1e4 if len(y) else np.nan
        r[nm + "_t"] = nw_t(y, max(1, h)) if len(y) >= 5 else np.nan
    yrs = d.groupby(d.index.year)["net"].sum()
    r["years_pos"] = float((yrs > 0).mean()); r["n_years"] = len(yrs)
    return r

def basket(syms, sigfn, h=1, mode="C0", pos=2500.0, extra_bp=0.0, hold=False):
    out = [sim(s, sigfn(s), h, mode, pos, extra_bp, hold) for s in syms]
    out = [o for o in out if len(o)]
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["sig_date", "entry", "exit", "gross", "net", "sym"])

def bh(p, q=0.10):
    p = np.asarray(p, float); m = np.isfinite(p).sum(); o = np.argsort(np.where(np.isfinite(p), p, 9))
    k = 0
    for i, j in enumerate(o[:m], 1):
        if p[j] <= q * i / m: k = i
    res = np.zeros(len(p), bool); res[o[:k]] = True
    return res
