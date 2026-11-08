"""Denetim (abd_endeks): BAĞIMSIZ işlem simülatörü. lib.trades / lib.evaluate / ae.full_eval KULLANILMAZ.
Fiyat için yalnız lib.load (temizlenmiş toplam getiri düzeltmeli OHLC) ve ham parquet (çapraz kontrol) okunur.
Zamanlama: sinyal t kapanışında (yalnız <=t verisi). C0: giriş c[t], çıkış c[t+h]; O1: giriş o[t+1], çıkış c[t+h];
C1: giriş c[t+1], çıkış c[t+1+h]. Çakışma yok: yeni işlem ancak önceki çıkış gününün kapanışında ya da sonrasında
oluşan sinyalle (C0'da çıkış günü sinyali aynı kapanışta yeniden giriş) açılır.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_abd_endeks", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
WARM = 200

def raw(sym):
    return pd.read_parquet(os.path.join(ROOT, "data", "etf", sym + ".parquet"))

def cost_bp(sym, pos):
    """Midas: 2 x 1,5 USD + makas kademesi (tarama.csv spread_bp)."""
    t = TAR.loc[sym, "spread_bp"]
    return 2 * 1.5 / pos * 1e4 + t

TAR = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")

def my_ibs(d):
    rng = (d["h"] - d["l"]).values
    out = np.full(len(d), np.nan)
    ok = rng > 0
    out[ok] = (d["c"].values[ok] - d["l"].values[ok]) / rng[ok]
    return np.clip(out, 0, 1)

def sim(d, sig, h, mode, exit_sig=None, warm=WARM):
    """sig: numpy bool (len(d)), t kapanışında bilinir. Döner: liste (i_sig, i_entry, i_exit, gross)."""
    o = d["o"].values; c = d["c"].values; n = len(c)
    sig = np.asarray(sig, bool).copy(); sig[:warm] = False
    ex = None if exit_sig is None else np.asarray(exit_sig, bool)
    res = []; i = 0
    while i < n:
        if not sig[i]:
            i += 1; continue
        if mode == "C0":
            e, ep, last, fx = i, c[i], i + h, i + 1
        elif mode == "O1":
            e = i + 1
            if e >= n: break
            ep, last, fx = o[e], i + h, e
        elif mode == "C1":
            e = i + 1
            if e >= n: break
            ep, last, fx = c[e], i + 1 + h, e + 1
        elif mode == "C2":   # ek sağlamlık: t+2 kapanışında gir
            e = i + 2
            if e >= n: break
            ep, last, fx = c[e], i + 2 + h, e + 1
        if last >= n: break
        x = last
        if ex is not None:
            for j in range(fx, last + 1):
                if ex[j]: x = j; break
        res.append((i, e, x, c[x] / ep - 1))
        i = max(x, i + 1)
    return res

def tstat(x):
    x = np.asarray(x, float); n = len(x)
    if n < 3: return np.nan
    s = x.std(ddof=1)
    return x.mean() / (s / math.sqrt(n)) if s > 0 else np.nan

def summarize(d, tr, cost):
    if not tr: return {"n": 0}
    idx = d.index
    sd = pd.DatetimeIndex([idx[a] for a, _, _, _ in tr])
    g = np.array([r[3] for r in tr]); ne = g - cost / 1e4
    wins = ne[ne > 0].sum(); loss = -ne[ne < 0].sum()
    eq = np.cumprod(1 + ne); dd = (eq / np.maximum.accumulate(eq) - 1).min()
    isx = sd <= IS_END
    yrs = pd.Series(ne, index=sd).groupby(sd.year).sum()
    return {"n": len(g), "brut_bp": g.mean() * 1e4, "net_bp": ne.mean() * 1e4, "win": (ne > 0).mean(),
            "pf": wins / loss if loss > 0 else np.inf, "t": tstat(ne),
            "is_n": int(isx.sum()), "is_net_bp": ne[isx].mean() * 1e4 if isx.any() else np.nan, "is_t": tstat(ne[isx]),
            "oos_n": int((~isx).sum()), "oos_net_bp": ne[~isx].mean() * 1e4 if (~isx).any() else np.nan, "oos_t": tstat(ne[~isx]),
            "yil_poz": float((yrs > 0).mean()), "maxdd": dd, "en_kotu_bp": ne.min() * 1e4}

def trades_df(d, tr, cost):
    idx = d.index
    return pd.DataFrame({"sig": [idx[a] for a, _, _, _ in tr], "giris": [idx[b] for _, b, _, _ in tr],
                         "cikis": [idx[x] for _, _, x, _ in tr], "brut_bp": [g * 1e4 for *_, g in tr],
                         "net_bp": [g * 1e4 - cost for *_, g in tr]})

def s1_signal(d, thr=0.10, down=True):
    ib = my_ibs(d); c = d["c"].values
    dn = np.r_[False, c[1:] < c[:-1]]
    s = np.nan_to_num(ib, nan=1.0) < thr
    return (s & dn) if down else s

def s3_signal(d, k=3):
    c = d["c"].values; dn = np.r_[False, c[1:] < c[:-1]]
    s = dn.copy()
    for j in range(1, k):
        s = s & np.r_[[False] * j, dn[:-j]]
    return s

def up_close(d):
    c = d["c"].values
    return np.r_[False, c[1:] > c[:-1]]
