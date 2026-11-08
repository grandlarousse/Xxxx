"""Denetim (enerji_tarim): bağımsız işlem simülatörü ve istatistikler.
lib.trades / lib.evaluate / ortak.full KULLANILMAZ. Fiyat için yalnız lib.load (toplam getiri düzeltmeli o/c) okunur.

Zamanlama (lib.py sözleşmesiyle aynı tanım, ayrı kod):
  C0: giriş t kapanışı, çıkış t+h kapanışı
  O1: giriş t+1 açılışı, çıkış t+h kapanışı (h=1 -> gün içi)
  C1: giriş t+1 kapanışı, çıkış t+1+h kapanışı
Çakışma: pozisyon açıkken (çıkış gününden önce) gelen sinyal yok sayılır; çıkış günü gelen sinyal yeni işlem açabilir.
Maliyet: 2*1,5 USD / pozisyon + tarama.csv makası (bp), işlem başına bir kez düşülür.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_enerji_tarim", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
_tar = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")


def spread(sym):
    return float(_tar.loc[sym, "spread_bp"])


def cost(sym, pos=2500.0):
    return 2 * 1.5 / pos * 1e4 + spread(sym)


def sim(df, sig, h, mode):
    """sig: df.index ile aynı uzunlukta bool dizi (t kapanışında bilinen). Brüt getirili işlem listesi döndürür."""
    s = np.asarray(pd.Series(sig, index=df.index).reindex(df.index).fillna(False).astype(bool))
    o = df["o"].to_numpy(); c = df["c"].to_numpy(); idx = df.index; n = len(df)
    rows = []; free_from = 0
    for i in range(n):
        if not s[i] or i < free_from:
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
        if x >= n:
            break
        rows.append((idx[i], idx[e], idx[x], c[x] / ep - 1.0))
        free_from = x
    return pd.DataFrame(rows, columns=["sig", "giris", "cikis", "brut"])


def st(tr, cost_bp, label=""):
    if len(tr) < 2:
        return {"label": label, "n": len(tr)}
    g = tr["brut"].to_numpy(); ne = g - cost_bp / 1e4; n = len(ne)
    sd = ne.std(ddof=1)
    eq = np.cumprod(1 + ne); dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    r = {"label": label, "n": n, "brut_bp": g.mean() * 1e4, "net_bp": ne.mean() * 1e4,
         "t": ne.mean() / (sd / math.sqrt(n)), "t_brut": g.mean() / (g.std(ddof=1) / math.sqrt(n)),
         "kazanma": float((ne > 0).mean()),
         "pf": float(ne[ne > 0].sum() / -ne[ne < 0].sum()) if (ne < 0).any() else np.inf,
         "maxdd": dd, "en_kotu_bp": ne.min() * 1e4, "en_iyi_bp": ne.max() * 1e4, "maliyet_bp": cost_bp}
    for nm, m in (("is", tr["sig"] <= IS_END), ("oos", tr["sig"] > IS_END)):
        x = ne[m.to_numpy()]
        r[nm + "_n"] = len(x)
        r[nm + "_net_bp"] = x.mean() * 1e4 if len(x) else np.nan
        r[nm + "_t"] = x.mean() / (x.std(ddof=1) / math.sqrt(len(x))) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan
    yrs = pd.Series(ne, index=tr["sig"].dt.year.to_numpy()).groupby(level=0).sum()
    r["yil_poz"] = float((yrs > 0).mean()); r["yil_n"] = len(yrs)
    return r


def t_of(x):
    x = np.asarray(x, float)
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x))) if len(x) > 2 else np.nan


def yearly(tr, cost_bp):
    ne = tr["brut"] - cost_bp / 1e4
    g = pd.DataFrame({"y": tr["sig"].dt.year, "net": ne})
    return g.groupby("y")["net"].agg(n="size", ort_bp=lambda v: v.mean() * 1e4, toplam_bp=lambda v: v.sum() * 1e4)


def bh(p, q=0.10):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); thr = 0
    for k, ix in enumerate(o, 1):
        if p[ix] <= q * k / m: thr = k
    out = np.zeros(m, bool); out[o[:thr]] = True
    return out
