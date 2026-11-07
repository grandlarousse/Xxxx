"""Ortak kütüphane: veri yükleme, temizlik, sinyal değerlendirme (1-3 gün, maliyetli), istatistikler.

ZAMANLAMA SÖZLEŞMESİ (tüm betikler buna uyar):
  * Gün t'nin sinyali yalnızca t kapanışına (16:00 ET) kadar bilinen veriyle hesaplanır.
  * Giriş modları:
      'C0' : t kapanışında gir (kapanıştan hemen önce, TR saatiyle kışın ~23:45, yazın ~22:45).
             Sinyal t kapanış fiyatını kullanıyorsa bu hafif iyimserdir (son dakikalar).
      'O1' : t+1 açılışında gir (TR 17:30 kış / 16:30 yaz).  Çıkış t+h kapanışı.
      'C1' : t+1 kapanışında gir (bir gün gecikmeli, en muhafazakâr).  Çıkış t+1+h kapanışı.
  * Çıkış: girişten itibaren h işlem günü sonraki kapanış (h=1,2,3). 'C0' için t+h, 'O1' için t+h
    (yani O1'de h=1 tutuş = t+1 açılış -> t+1 kapanış, gün içi), 'C1' için t+1+h.
  * Çakışmayan işlemler: pozisyondayken gelen sinyal yok sayılır.
  * Getiriler toplam getiri (temettü dahil) düzeltmeli fiyatlardan.
  * Cboe VIX kapanışı 16:15 ET'dir (15 dk sonra) -> VIX bazlı sinyallerde C0 hafif iyimser; O1/C1 temiz.
  * Coinbase günlük mum 00:00 UTC'de kapanır (ABD kapanışından 3-4 saat SONRA) -> günlük BTC getirisi
    t kapanışında BİLİNMEZ. Saatlik veriden 16:00 ET anındaki BTC fiyatını kullanın: btc_at_us_close().

MALİYET: Midas ABD işlemlerinde işlem başına 1,5 USD (alış + satış = 3 USD).
  pozisyon 2.500 USD -> 12 bp gidiş-dönüş komisyon. Üzerine tahmini makas (spread_bp) eklenir.
  cost_bp(sym) = 2*1.5/POS*1e4 + spread_bp(sym).
"""
import os, json, math
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
POS_USD = 2500.0
COMM_USD = 1.5
IS_END = pd.Timestamp("2021-12-31")   # IS: 2016-11..2021 ; OOS: 2022..2026-11

_cache = {}

def meta():
    return json.load(open(os.path.join(DATA, "meta", "etf_meta.json")))

def available():
    d = os.path.join(DATA, "etf")
    return sorted(f[:-8] for f in os.listdir(d) if f.endswith(".parquet"))

def load(sym, clean=True):
    """Toplam getiri düzeltmeli OHLC: o,h,l,c (düzeltilmiş), raw_c, v, dv (dolar hacim)."""
    key = (sym, clean)
    if key in _cache: return _cache[key].copy()
    df = pd.read_parquet(os.path.join(DATA, "etf", sym + ".parquet"))
    df = df[df["c"] > 0].copy()
    f = df["adjc"] / df["c"]
    out = pd.DataFrame(index=df.index)
    o = df["o"].where(df["o"] > 0)
    h = df["h"].where(df["h"] > 0)
    l = df["l"].where(df["l"] > 0)
    if clean:
        # eksik/bozuk açılış -> önceki kapanış; h/l tutarlılığı
        o = o.fillna(df["c"].shift(1)).fillna(df["c"])
        h = pd.concat([h.fillna(df["c"]), o, df["c"]], axis=1).max(axis=1)
        l = pd.concat([l.fillna(df["c"]), o, df["c"]], axis=1).min(axis=1)
    out["o"] = o * f; out["h"] = h * f; out["l"] = l * f; out["c"] = df["adjc"]
    out["raw_c"] = df["c"]; out["v"] = df["v"]; out["dv"] = df["c"] * df["v"]; out["div"] = df["div"]
    _cache[key] = out
    return out.copy()

def closes(syms, field="c"):
    return pd.DataFrame({s: load(s)[field] for s in syms})

def vol_index(name):
    df = pd.read_parquet(os.path.join(DATA, "vol", name + ".parquet"))
    return df["close"]

_TSY = {"DGS2": ("nominal", "2 Yr"), "DGS10": ("nominal", "10 Yr"), "DGS30": ("nominal", "30 Yr"), "DGS3MO": ("nominal", "3 Mo"),
        "DFII10": ("real", "10 YR"), "DFII5": ("real", "5 YR")}

def fred(series):
    """FRED serisi; yoksa ABD Hazinesi yedeği (DGS2, DGS10, DGS30, DGS3MO, DFII10, DFII5)."""
    p = os.path.join(DATA, "fred", series + ".parquet")
    if os.path.exists(p):
        return pd.read_parquet(p)["value"]
    if series in _TSY:
        fn, col = _TSY[series]
        q = os.path.join(DATA, "treasury", fn + ".parquet")
        if os.path.exists(q):
            df = pd.read_parquet(q)
            cols = {c.upper(): c for c in df.columns}
            c = cols.get(col.upper())
            if c: return pd.to_numeric(df[c], errors="coerce")
    if series == "T10YIE":
        a, b = fred("DGS10"), fred("DFII10")
        if a is not None and b is not None: return (a - b).dropna()
    if series == "T10Y2Y":
        a, b = fred("DGS10"), fred("DGS2")
        if a is not None and b is not None: return (a - b).dropna()
    return None

def btc_at_us_close(pair="BTC-USD"):
    """16:00 America/New_York anındaki (o saatin açılışı ~ 15:00-16:00 mumu kapanışı) kripto fiyatı, ET tarihine göre."""
    p = os.path.join(DATA, "crypto", pair + "_h1.parquet")
    h = pd.read_parquet(p)
    et = h.index.tz_convert("America/New_York")
    hh = h.copy(); hh.index = et
    # 15:00 başlangıçlı mumun kapanışı = 16:00 ET fiyatı
    m = hh[hh.index.hour == 15]["c"]
    m.index = m.index.tz_localize(None).normalize()
    return m[~m.index.duplicated(keep="last")]

# ---------------- göstergeler ----------------
def rsi(c, n=2):
    d = c.diff(); up = d.clip(lower=0); dn = (-d).clip(lower=0)
    au = up.ewm(alpha=1 / n, adjust=False).mean(); ad = dn.ewm(alpha=1 / n, adjust=False).mean()
    rs = au / ad.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(100)

def ibs(df):
    rng = (df["h"] - df["l"]).replace(0, np.nan)
    return ((df["c"] - df["l"]) / rng).clip(0, 1)

def sma(x, n): return x.rolling(n).mean()

def atr(df, n=14):
    pc = df["c"].shift(1)
    tr = pd.concat([df["h"] - df["l"], (df["h"] - pc).abs(), (df["l"] - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()

def zret(c, k=1, n=60):
    """k günlük getirinin, son n günlük k-günlük oynaklığa göre z skoru (t'ye kadar bilgi)."""
    r = np.log(c).diff(k)
    sd = np.log(c).diff().rolling(n).std() * math.sqrt(k)
    return r / sd

def spread_bp_est(df, n=252):
    """Abdi-Ranaldo (2017) kapanış-orta fiyat makas tahmini, son n gün medyanı, bp. Kaba bir tahmindir."""
    eta = np.log((df["h"] + df["l"]) / 2)
    c = np.log(df["c"])
    s2 = 4 * (c - eta) * (c - eta.shift(-1))
    s = np.sqrt(s2.clip(lower=0)).tail(n)
    return float(np.nanmean(s) * 1e4) if len(s) else np.nan

def spread_bp_tier(df, n=252):
    """Likidite kademesine göre tahmini tam makas (bp) ve 1 sentlik fiyat adımı tabanı.
    Medyan günlük dolar hacim (son n gün): >1 mlr: 1bp, >200 mn: 2bp, >50 mn: 4bp, >10 mn: 8bp, >2 mn: 15bp, aksi 35bp.
    Taban: 0.01 USD / son fiyat (ör. 10 USD'lik ETF'de en az 10 bp)."""
    t = df.tail(n)
    dv = float(np.nanmedian(t["dv"])) if len(t) else 0.0
    px = float(t["raw_c"].iloc[-1]) if len(t) else np.nan
    tier = 1 if dv > 1e9 else 2 if dv > 2e8 else 4 if dv > 5e7 else 8 if dv > 1e7 else 15 if dv > 2e6 else 35
    tick = 1e4 * 0.01 / px if px and px > 0 else 10
    return max(tier, tick)

def cost_bp(df, pos_usd=POS_USD):
    """Gidiş-dönüş maliyet (bp): Midas komisyonu (2 x 1.5 USD) + tahmini tam makas."""
    return 2 * COMM_USD / pos_usd * 1e4 + spread_bp_tier(df)

# ---------------- değerlendirme ----------------
def trades(df, sig, h=1, mode="C0", exit_sig=None, cost=0.0):
    """sig: t kapanışında bilinen bool Seri (df.index ile hizalı). Çakışmayan işlemler.
    exit_sig: (opsiyonel) t kapanışında True ise erken çık (en fazla h gün).
    Dönüş: DataFrame [sig_date, entry_date, exit_date, gross, net, days]."""
    sig = sig.reindex(df.index).fillna(False).astype(bool).values
    ex = None if exit_sig is None else exit_sig.reindex(df.index).fillna(False).astype(bool).values
    o = df["o"].values; c = df["c"].values; idx = df.index
    n = len(df); out = []; i = 0
    while i < n:
        if not sig[i]:
            i += 1; continue
        if mode == "C0":
            e = i; ep = c[i]; last = i + h; first_exit = e + 1
        elif mode == "O1":
            e = i + 1; last = i + h; first_exit = e
            if e >= n: break
            ep = o[e]
        elif mode == "C1":
            e = i + 1; last = i + 1 + h; first_exit = e + 1
            if e >= n: break
            ep = c[e]
        else:
            raise ValueError(mode)
        if last >= n: break
        x = last
        if ex is not None:
            for j in range(first_exit, last + 1):
                if ex[j]:
                    x = j; break
        g = c[x] / ep - 1
        days = (x - e + 1) if mode == "O1" else (x - e)
        out.append((idx[i], idx[e], idx[x], g, g - cost / 1e4, days))
        # bir sonraki uygun sinyal: çıkış kapanışında (C0) ya da sonrasında
        i = max(x, i + 1)
    return pd.DataFrame(out, columns=["sig_date", "entry_date", "exit_date", "gross", "net", "days"])

def uncond(df, h=1, mode="C0"):
    """Aynı tutuş yapısının koşulsuz ortalaması (her gün sinyal var gibi, örtüşen)."""
    c = df["c"]; o = df["o"]
    if mode == "C0": r = c.shift(-h) / c - 1
    elif mode == "O1": r = c.shift(-h) / o.shift(-1) - 1
    else: r = c.shift(-(1 + h)) / c.shift(-1) - 1
    return r

def stats(tr, df=None, h=1, mode="C0", label=""):
    if tr is None or len(tr) == 0:
        return {"label": label, "n": 0}
    g = tr["gross"].values; ne = tr["net"].values
    n = len(g)
    m = ne.mean(); sd = ne.std(ddof=1) if n > 1 else np.nan
    t = m / (sd / math.sqrt(n)) if n > 1 and sd > 0 else np.nan
    wins = ne[ne > 0].sum(); loss = -ne[ne < 0].sum()
    eq = np.cumprod(1 + ne); dd = (eq / np.maximum.accumulate(eq) - 1).min()
    res = {"label": label, "n": n, "mean_gross_bp": g.mean() * 1e4, "mean_net_bp": m * 1e4,
           "median_net_bp": float(np.median(ne) * 1e4), "win": float((ne > 0).mean()),
           "pf": float(wins / loss) if loss > 0 else np.inf, "t": t, "maxdd": float(dd),
           "worst_bp": float(ne.min() * 1e4), "days_in_mkt": int(tr["days"].sum())}
    if df is not None:
        u = uncond(df, h, mode).dropna()
        u = u[(u.index >= tr["sig_date"].min())]
        res["uncond_bp"] = float(u.mean() * 1e4)
        res["edge_bp"] = res["mean_gross_bp"] - res["uncond_bp"]
        res["t_edge"] = (g.mean() - u.mean()) / (g.std(ddof=1) / math.sqrt(n)) if n > 1 and g.std(ddof=1) > 0 else np.nan
    isx = tr[tr["sig_date"] <= IS_END]; oos = tr[tr["sig_date"] > IS_END]
    for nm, part in (("is", isx), ("oos", oos)):
        if len(part) > 1:
            x = part["net"].values
            res[f"{nm}_n"] = len(x); res[f"{nm}_net_bp"] = x.mean() * 1e4
            res[f"{nm}_t"] = x.mean() / (x.std(ddof=1) / math.sqrt(len(x))) if x.std(ddof=1) > 0 else np.nan
        else:
            res[f"{nm}_n"] = len(part); res[f"{nm}_net_bp"] = np.nan; res[f"{nm}_t"] = np.nan
    yrs = tr.groupby(tr["sig_date"].dt.year)["net"].sum()
    res["years_pos_frac"] = float((yrs > 0).mean()) if len(yrs) else np.nan
    res["n_years"] = int(len(yrs))
    return res

def evaluate(df, sig, h=1, mode="C0", cost=None, exit_sig=None, label=""):
    if cost is None: cost = cost_bp(df)
    tr = trades(df, sig, h, mode, exit_sig, cost)
    s = stats(tr, df, h, mode, label); s["cost_bp"] = cost; s["h"] = h; s["mode"] = mode
    return s, tr

def bh_fdr(pvals, q=0.10):
    """Benjamini-Hochberg: geçen maskeyi döndürür."""
    p = np.asarray(pvals, float); m = np.isfinite(p).sum()
    order = np.argsort(np.where(np.isfinite(p), p, 9)); passed = np.zeros(len(p), bool)
    thr = 0
    for k, ix in enumerate(order[:m], 1):
        if p[ix] <= q * k / m: thr = k
    passed[order[:thr]] = True
    return passed

def t_to_p(t, n):
    from scipy import stats as st
    if not np.isfinite(t) or n < 3: return np.nan
    return float(2 * st.t.sf(abs(t), n - 1))
