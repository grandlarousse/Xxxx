"""Denetim (volatilite) - bağımsız işlem simülatörü. lib.trades / lib.evaluate / lib.rsi KULLANILMAZ.
Fiyat için yalnız lib.load kullanılır. Maliyet tarama.csv'deki spread_bp + Midas komisyonundan bağımsız hesaplanır.

Zamanlama:
  C0 : t kapanışında gir, t+h kapanışında çık.
  O1 : t+1 açılışında gir, t+h kapanışında çık (h=1 gün içi).
  C1 : t+1 kapanışında gir, t+1+h kapanışında çık.
  Çakışma yok: pozisyon kapanana kadar gelen sinyal atlanır; çıkış gününün sinyali (C0) yeni işlem açabilir.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib  # yalnız lib.load ve ROOT için

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_volatilite", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
_tar = None

def spread(sym):
    global _tar
    if _tar is None:
        _tar = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")
    return float(_tar.loc[sym, "spread_bp"])

def cost(sym, pos=2500.0):
    return 2 * 1.5 / pos * 1e4 + spread(sym)

def wilder_rsi(c, n=2):
    """Wilder RSI: ilk n değişimin basit ortalamasıyla tohumlanan RMA (TradingView ta.rsi ile aynı tanım)."""
    d = np.diff(c.values, prepend=np.nan)
    up = np.where(d > 0, d, 0.0); dn = np.where(d < 0, -d, 0.0)
    up[0] = np.nan; dn[0] = np.nan
    au = np.full(len(c), np.nan); ad = np.full(len(c), np.nan)
    if len(c) > n:
        au[n] = np.mean(up[1:n + 1]); ad[n] = np.mean(dn[1:n + 1])
        for i in range(n + 1, len(c)):
            au[i] = (au[i - 1] * (n - 1) + up[i]) / n
            ad[i] = (ad[i - 1] * (n - 1) + dn[i]) / n
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = au / ad
        r = 100 - 100 / (1 + rs)
    r = np.where((ad == 0) & np.isfinite(au), 100.0, r)
    return pd.Series(r, index=c.index)

def sma(c, n):
    return c.rolling(n, min_periods=n).mean()

def sim(df, sig, h=2, mode="C0", cost_bp=0.0):
    """Kendi döngüm. sig: bool Seri (df.index). Dönüş DataFrame: sig, giris, cikis, ep, xp, gross, net."""
    s = sig.reindex(df.index).fillna(False).values.astype(bool)
    o = df["o"].values; c = df["c"].values; ix = df.index; n = len(df)
    rows = []; busy_until = -1
    for i in range(n):
        if not s[i]:
            continue
        if mode == "C0":
            ei, ep, xi = i, c[i], i + h
            if i < busy_until: continue
        elif mode == "O1":
            ei, xi = i + 1, i + h
            if i < busy_until: continue      # önceki pozisyon xi kapanışında kapanır; aynı gün sinyali ertesi açılışa girer
            if ei >= n: break
            ep = o[ei]
        elif mode == "C1":
            ei, xi = i + 1, i + 1 + h
            if ei <= busy_until: continue     # giriş günü önceki çıkıştan sonra olmalı... (çıkış kapanışında girişe izin: ei==busy_until hariç tutulur)
            if ei >= n: break
            ep = c[ei]
        if xi >= n: break
        xp = c[xi]; g = xp / ep - 1
        rows.append((ix[i], ix[ei], ix[xi], ep, xp, g, g - cost_bp / 1e4))
        busy_until = xi
    return pd.DataFrame(rows, columns=["sig", "giris", "cikis", "ep", "xp", "gross", "net"])

def tstat(x):
    x = np.asarray(x, float); n = len(x)
    if n < 3: return np.nan
    sd = x.std(ddof=1)
    return x.mean() / (sd / math.sqrt(n)) if sd > 0 else np.nan

def summ(tr, tag=""):
    if len(tr) == 0: return {"tag": tag, "n": 0}
    g = tr.gross.values; ne = tr.net.values
    eq = np.cumprod(1 + ne); dd = (eq / np.maximum.accumulate(eq) - 1).min()
    w = ne[ne > 0].sum(); l = -ne[ne < 0].sum()
    isx = tr[tr.sig <= IS_END]; oo = tr[tr.sig > IS_END]
    yr = tr.groupby(tr.sig.dt.year).net.sum()
    from scipy import stats as st
    t = tstat(ne)
    return {"tag": tag, "n": len(tr), "brut_bp": g.mean() * 1e4, "net_bp": ne.mean() * 1e4, "t": t,
            "p": float(2 * st.t.sf(abs(t), len(ne) - 1)) if np.isfinite(t) else np.nan,
            "win": float((ne > 0).mean()), "pf": float(w / l) if l > 0 else np.inf, "maxdd": float(dd),
            "en_kotu_bp": ne.min() * 1e4, "en_iyi_bp": ne.max() * 1e4,
            "is_n": len(isx), "is_net_bp": isx.net.mean() * 1e4 if len(isx) else np.nan, "is_t": tstat(isx.net),
            "oos_n": len(oo), "oos_net_bp": oo.net.mean() * 1e4 if len(oo) else np.nan, "oos_t": tstat(oo.net),
            "yil_pozitif": float((yr > 0).mean()), "n_yil": len(yr)}
