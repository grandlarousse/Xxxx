"""Denetim (kripto) — bağımsız yardımcılar. lib.trades / lib.evaluate / lib.stats KULLANILMAZ.
Fiyat için yalnız lib.load (ETF), ham parquet (kripto günlük/saatlik) kullanılır.
Zamanlama: sinyal t kapanışında bilinir; C0 = t kapanışı, O1 = t+1 açılışı, C1 = t+1 kapanışı;
çıkış girişten h işlem günü sonraki kapanış (O1'de h=1 = aynı gün kapanışı)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
ROOT = os.path.dirname(KOD)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib  # yalnız lib.load ve sabitler

OUT = os.path.join(ROOT, "sonuclar", "aile_kripto", "denetim")
os.makedirs(OUT, exist_ok=True)
IS_END = pd.Timestamp("2021-12-31")
COMM = 1.5

def comm_bp(pos):
    return 2 * COMM / pos * 1e4

def tarama_spread(sym):
    t = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv"))
    r = t[t.sym == sym]
    return float(r.spread_bp.iloc[0]) if len(r) else np.nan

def nyse_days():
    return lib.load("SPY").index

# ------------------------------------------------------------------ kripto serileri (kendi kurulumum)
def btc_daily_on_nyse(pair="BTC-USD"):
    """NYSE günü t -> UTC t tarihli günlük mumun kapanışı (00:00 UTC t+1). Pazartesi = Pazar mumu kapanışı.
    Bu seri ETF kapanışından 3-4 saat SONRA kapanır: kendi içinde (sinyal ve giriş aynı damgada) ileri bakışsız."""
    d = pd.read_parquet(os.path.join(ROOT, "data", "crypto", pair + ".parquet"))
    d.index = pd.to_datetime(d.index).normalize()
    days = nyse_days()
    c = d["c"].reindex(days)
    out = pd.DataFrame({"c": c}).dropna()
    out["o"] = out["c"].shift(1)  # O1 bu seride anlamsız; yer tutucu
    return out.iloc[1:]

def btc_hourly_et(pair="BTC-USD"):
    h = pd.read_parquet(os.path.join(ROOT, "data", "crypto", pair + "_h1.parquet"))
    h = h.copy(); h.index = h.index.tz_convert("America/New_York")
    return h

def btc_session(pair="BTC-USD"):
    """Kendi kurulumum: NYSE günü için 09:30 ET (09:00 mumunun açılışı ile kapanışının ortası yerine:
    09:00-10:00 mumunun AÇILIŞI = 09:00 ET ve KAPANIŞI = 10:00 ET; 09:30 ~ ortalama) ve 16:00 ET fiyatı
    (15:00 başlangıçlı mumun kapanışı)."""
    h = btc_hourly_et(pair)
    loc = h.index.tz_localize(None)
    day = loc.normalize(); hr = loc.hour
    c16 = pd.Series(h["c"].values[hr == 15], index=day[hr == 15])
    c16 = c16[~c16.index.duplicated(keep="last")]
    o9 = pd.Series(((h["o"] + h["c"]) / 2).values[hr == 9], index=day[hr == 9])
    o9 = o9[~o9.index.duplicated(keep="last")]
    o10 = pd.Series(h["o"].values[hr == 10], index=day[hr == 10])  # 10:00 ET fiyatı (alternatif açılış)
    o10 = o10[~o10.index.duplicated(keep="last")]
    days = nyse_days()
    df = pd.DataFrame({"c": c16.reindex(days), "o": o9.reindex(days), "o10": o10.reindex(days)}).dropna(subset=["c"])
    df = df[df.index >= pd.Timestamp("2023-05-30")]
    return df

# ------------------------------------------------------------------ simülasyon
def sim(df, sig, h=1, mode="C0", cost_bp=0.0):
    """Kendi çakışmasız işlem döngüm. sig: bool Seri (t kapanışında bilinir). Döner: DataFrame."""
    sig = sig.reindex(df.index).fillna(False).astype(bool).values
    o = df["o"].values; c = df["c"].values; idx = df.index; n = len(df)
    rows = []; busy_until = -1
    for i in range(n):
        if not sig[i]: continue
        if i < busy_until: continue          # sinyal günü son çıkıştan önce olamaz (çıkış günü sinyali geçerli)
        if mode == "C0":
            e = i; ep = c[i]; x = i + h
        elif mode == "O1":
            e = i + 1; x = i + h
            if e >= n: break
            ep = o[e]
        elif mode == "C1":
            e = i + 1; x = i + 1 + h
            if e >= n: break
            ep = c[e]
        if x >= n: break
        g = c[x] / ep - 1
        rows.append((idx[i], idx[e], idx[x], g, g - cost_bp / 1e4))
        busy_until = x
    return pd.DataFrame(rows, columns=["sig_date", "entry_date", "exit_date", "gross", "net"])

def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3: return np.nan
    s = x.std(ddof=1)
    return x.mean() / (s / math.sqrt(len(x))) if s > 0 else np.nan

def pval(t, n):
    from scipy import stats as st
    if not np.isfinite(t) or n < 3: return np.nan
    return float(2 * st.t.sf(abs(t), n - 1))

def summ(tr, label=""):
    if len(tr) == 0: return {"label": label, "n": 0}
    g = tr.gross.values; ne = tr.net.values
    eq = np.cumprod(1 + ne); dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    w = ne[ne > 0].sum(); l = -ne[ne < 0].sum()
    yrs = tr.groupby(tr.sig_date.dt.year).net.sum()
    isx = tr[tr.sig_date <= IS_END]; oos = tr[tr.sig_date > IS_END]
    srt = np.sort(ne)[::-1]
    r = {"label": label, "n": len(tr), "brut_bp": g.mean() * 1e4, "net_bp": ne.mean() * 1e4, "t": tt(ne), "t_brut": tt(g),
         "kazanma": float((ne > 0).mean()), "pf": float(w / l) if l > 0 else np.inf, "maxdd": dd, "en_kotu_bp": ne.min() * 1e4,
         "medyan_bp": float(np.median(ne) * 1e4),
         "is_n": len(isx), "is_net_bp": isx.net.mean() * 1e4 if len(isx) else np.nan, "is_t": tt(isx.net) if len(isx) > 2 else np.nan,
         "oos_n": len(oos), "oos_net_bp": oos.net.mean() * 1e4 if len(oos) else np.nan, "oos_t": tt(oos.net) if len(oos) > 2 else np.nan,
         "yil_pozitif": float((yrs > 0).mean()), "n_yil": len(yrs),
         "en_iyi5_haric_net_bp": srt[5:].mean() * 1e4 if len(srt) > 6 else np.nan, "en_iyi5_haric_t": tt(srt[5:]) if len(srt) > 8 else np.nan}
    r["p"] = pval(r["t"], r["n"]); r["p_brut"] = pval(r["t_brut"], r["n"])
    return r

def yearly(tr):
    return (tr.groupby(tr.sig_date.dt.year).net.agg(["mean", "count"]) * [1e4, 1]).round(1)

def perm_random_entry(ret_pool, n, observed, reps=5000, seed=7):
    """ret_pool: aynı tutuş yapısındaki tüm olası işlem getirileri (her gün bir). n adet rastgele (yerine koymadan) gün
    seçilir; ortalama >= gözlenen olma oranı (tek yönlü p)."""
    rng = np.random.default_rng(seed)
    pool = np.asarray(ret_pool, float); pool = pool[np.isfinite(pool)]
    m = np.empty(reps)
    for k in range(reps):
        m[k] = pool[rng.choice(len(pool), size=n, replace=False)].mean()
    return float((m >= observed).mean()), float(m.mean()), float(np.percentile(m, 95))

def bh(p, q=0.10):
    p = np.asarray(p, float); ok = np.isfinite(p); m = ok.sum()
    order = np.argsort(np.where(ok, p, 9)); thr = 0
    for k, ix in enumerate(order[:m], 1):
        if p[ix] <= q * k / m: thr = k
    out = np.zeros(len(p), bool); out[order[:thr]] = True
    return out
