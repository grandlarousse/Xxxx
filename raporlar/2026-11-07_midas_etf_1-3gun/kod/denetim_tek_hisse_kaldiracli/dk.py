"""Denetim (tek_hisse_kaldiracli) — bağımsız yardımcılar. lib.trades / lib.evaluate / thk KULLANILMAZ.
Fiyat: hisse için data/stock/<SYM>.parquet (ya da denetim veri/ dizini) doğrudan okunur; gerçek ETF için yalnız lib.load (fiyat).
Göstergeler: Wilder RSI (TradingView ta.rsi gibi RMA, ilk değer SMA tohumlu), SMA (rolling mean).
Sentetik 2x: r = 2*r_hisse - sürükleme; sürükleme = (gider %1,05 + (L-1)*(3 aylık faiz + %0,5))/252 + ek (gerçek ETF'ten
bağımsız kalibre, d2'de ölçülür). Açılış: önceki sentetik kapanış * (1 + 2*gece getirisi - sürükleme).
Zamanlama: sinyal t kapanışıyla; C0 giriş t kapanışı, O1 giriş t+1 açılışı, C1 giriş t+1 kapanışı.
Çıkış: çıkış koşulu (hisse kapanış > SMA5) j kapanışında görülür ve j kapanışında çıkılır (C0'da j>=t+1; O1'de j>=t+1; C1'de j>=t+2),
en geç t+hmax (C1'de t+1+hmax). Aynı hissede pozisyondayken yeni sinyal yok sayılır; yeni sinyal çıkış günü ya da sonrası olabilir."""
import os, sys, math
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE); ROOT = os.path.dirname(KOD)
sys.path.insert(0, KOD)
import lib  # yalnız lib.load (ETF fiyatı) ve lib.fred (faiz verisi) kullanılır

OUT = os.path.join(ROOT, "sonuclar", "aile_tek_hisse_kaldiracli", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
STK = ["NVDA", "TSLA", "AAPL", "AMZN", "META", "MSFT", "GOOGL"]
ETF = {"NVDA": "NVDL", "TSLA": "TSLL", "AAPL": "AAPU", "AMZN": "AMZU", "META": "METU", "MSFT": "MSFU", "GOOGL": "GGLL",
       "MSTR": "MSTU", "COIN": "CONL"}
SWITCH = {"NVDL": "2024-02-01", "TSLL": "2024-04-10", "AAPU": "2024-04-10", "AMZU": "2024-04-15", "METU": "2024-06-06",
          "MSFU": "2024-04-10", "GGLL": "2024-04-10", "NVDU": "2024-04-15", "MSTU": "2024-09-19", "CONL": "2024-02-01"}

_tar = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")

def spread(etf):
    return float(_tar.loc[etf, "spread_bp"]) if etf in _tar.index else 4.0

def cost(etf, pos=2500.0):
    return 2 * 1.5 / pos * 1e4 + spread(etf)

def load_stock(sym):
    p = os.path.join(ROOT, "data", "stock", sym + ".parquet")
    if not os.path.exists(p): p = os.path.join(HERE, "veri", sym + ".parquet")
    d = pd.read_parquet(p)
    d = d[d["c"] > 0].copy()
    d["o"] = d["o"].where(d["o"] > 0).fillna(d["c"].shift(1)).fillna(d["c"])
    return d[["o", "h", "l", "c", "v"]]

def rsi_wilder(c, n=2):
    c = np.asarray(c, float); out = np.full(len(c), np.nan)
    d = np.diff(c, prepend=np.nan); up = np.where(d > 0, d, 0.0); dn = np.where(d < 0, -d, 0.0)
    if len(c) <= n: return out
    au = up[1:n + 1].mean(); ad = dn[1:n + 1].mean()
    out[n] = 100.0 if ad == 0 else 100 - 100 / (1 + au / ad)
    for i in range(n + 1, len(c)):
        au = (au * (n - 1) + up[i]) / n; ad = (ad * (n - 1) + dn[i]) / n
        out[i] = 100.0 if ad == 0 else 100 - 100 / (1 + au / ad)
    return out

def sma(c, n):
    return pd.Series(c).rolling(n).mean().values

_rf = None
def rf_daily(idx):
    global _rf
    if _rf is None:
        s = lib.fred("DGS3MO"); _rf = (s / 100.0).dropna()
    return _rf.reindex(idx, method="ffill").fillna(0.02).values / 252.0

def synth(sd, L=2.0, fee=0.0105, sp=0.005, extra_bp=0.0):
    c = sd["c"].values; o = sd["o"].values
    rf = rf_daily(sd.index)
    drag = fee / 252 + (L - 1) * (rf + sp / 252) + extra_bp / 1e4
    r = np.zeros(len(c)); r[1:] = L * (c[1:] / c[:-1] - 1) - drag[1:]
    P = 100 * np.cumprod(1 + r)
    Po = np.empty(len(c)); Po[0] = 100.0
    Po[1:] = P[:-1] * (1 + L * (o[1:] / c[:-1] - 1) - drag[1:])
    return pd.DataFrame({"o": np.maximum(Po, 1e-6), "c": P}, index=sd.index)

def signal(sd, thr=10, trend=200, use_trend=True, rsi_n=2):
    c = sd["c"].values
    r = rsi_wilder(c, rsi_n)
    s = r < thr
    if use_trend:
        m = sma(c, trend); s = s & (c > m)
    s[:max(trend, 20)] = False
    return np.nan_to_num(s, nan=0).astype(bool)

def exit_cond(sd, n=5):
    c = sd["c"].values; return np.nan_to_num(c > sma(c, n), nan=0).astype(bool)

def sim(sig, exc, Pc, Po, mode="C0", hmax=3, exit_next_open=False):
    """Bağımsız işlem simülasyonu. Dönüş: liste (i_sig, i_entry, i_exit, gross). exit_next_open: koşul j kapanışında görülür,
    j+1 açılışında çıkılır (muhafazakâr çıkış)."""
    n = len(sig); out = []; i = 0
    while i < n:
        if not sig[i]:
            i += 1; continue
        if mode == "C0": e = i; first = i + 1; last = i + hmax
        elif mode == "O1": e = i + 1; first = i + 1; last = i + hmax
        elif mode == "C1": e = i + 1; first = i + 2; last = i + 1 + hmax
        else: raise ValueError(mode)
        if last + (1 if exit_next_open else 0) >= n: break
        ep = Po[e] if mode == "O1" else Pc[e]
        x = last
        if exc is not None:
            for j in range(first, last + 1):
                if exc[j]: x = j; break
        if exit_next_open:
            g = Po[x + 1] / ep - 1; xi = x + 1
        else:
            g = Pc[x] / ep - 1; xi = x
        out.append((i, e, xi, g))
        i = max(xi, i + 1)
    return out

def run(stocks, mode="C0", thr=10, trend=200, use_trend=True, exit_n=5, hmax=3, exit_rule=True, pos=2500.0,
        data="synth", extra=None, etf_map=None, since=None, exit_next_open=False, L=2.0, cost_override=None):
    rows = []
    for st in stocks:
        sd = load_stock(st)
        e = (etf_map or ETF).get(st, None)
        if data == "synth":
            px = synth(sd, L=L, extra_bp=(extra or {}).get(st, 2.0))
            sdx = sd
        else:
            px = lib.load(e)[["o", "c"]]
            sdx = sd.reindex(px.index)
            if sdx["c"].isna().any():
                # hisse verisinde olmayan ETF günü (olmamalı)
                print("UYARI tarih uyumsuzluğu", st, e, int(sdx["c"].isna().sum()))
        sig_full = pd.Series(signal(sd, thr, trend, use_trend), index=sd.index)
        exc_full = pd.Series(exit_cond(sd, exit_n), index=sd.index)
        sig = sig_full.reindex(px.index).fillna(False).values.astype(bool)
        exc = exc_full.reindex(px.index).fillna(False).values.astype(bool) if exit_rule else None
        if since is not None:
            sig = sig & (px.index >= pd.Timestamp(since.get(e, "1900-01-01")))
        c_bp = cost_override if cost_override is not None else (cost(e, pos) if e else 2 * 1.5 / pos * 1e4 + 4.0)
        tr = sim(sig, exc, px["c"].values, px["o"].values, mode, hmax, exit_next_open)
        idx = px.index
        for (i, en, x, g) in tr:
            rows.append((st, e, idx[i], idx[en], idx[min(x, len(idx) - 1)], x - en + (1 if mode == "O1" else 0), g, g - c_bp / 1e4, c_bp))
    return pd.DataFrame(rows, columns=["stock", "etf", "sig_date", "entry_date", "exit_date", "days", "gross", "net", "cost_bp"])

def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))

def pooled(A, col="net"):
    """Tarih kümelemeli (aynı sinyal günündeki işlemlerin ortalaması tek gözlem)."""
    if len(A) < 3: return dict(n=len(A), n_tarih=len(A), bp=np.nan, t=np.nan)
    g = A.groupby("sig_date")[col].mean()
    return dict(n=len(A), n_tarih=len(g), bp=g.mean() * 1e4, t=tstat(g.values))

def summary(A, label=""):
    if len(A) == 0: return dict(label=label, n=0)
    P = pooled(A); G = pooled(A, "gross")
    ISa = A[A.sig_date <= IS_END]; OOSa = A[A.sig_date > IS_END]
    pi = pooled(ISa) if len(ISa) > 2 else dict(bp=np.nan, t=np.nan, n=len(ISa))
    po = pooled(OOSa) if len(OOSa) > 2 else dict(bp=np.nan, t=np.nan, n=len(OOSa))
    g = A.groupby("sig_date")["net"].mean().sort_index()
    yrs = g.groupby(g.index.year).sum()
    yrs_tr = A.groupby(A.sig_date.dt.year)["net"].sum()
    w = A.net[A.net > 0].sum(); l = -A.net[A.net < 0].sum()
    return dict(label=label, n=len(A), n_tarih=P["n_tarih"], brut_bp=G["bp"], net_bp=P["bp"], t=P["t"],
                net_islem_bp=A.net.mean() * 1e4, t_islem=tstat(A.net.values),
                is_n=pi["n"], is_bp=pi["bp"], is_t=pi["t"], oos_n=po["n"], oos_bp=po["bp"], oos_t=po["t"],
                win=float((A.net > 0).mean()), pf=float(w / l) if l > 0 else np.nan,
                yil_poz_tarih=float((yrs > 0).mean()), yil_poz_islem=float((yrs_tr > 0).mean()), n_yil=len(yrs),
                en_kotu_bp=A.net.min() * 1e4, en_iyi_bp=A.net.max() * 1e4)

def nw_t(x, lags=5):
    x = np.asarray(x, float); x = x[np.isfinite(x)]; n = len(x)
    m = x.mean(); e = x - m
    v = (e @ e) / n
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1); v += 2 * w * (e[k:] @ e[:-k]) / n
    return m / math.sqrt(v / n)
