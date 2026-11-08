"""kripto ailesi: ortak yardımcılar (kod/lib.py ve kod/strategies.py DEĞİŞTİRİLMEDEN genişletme).

ZAMANLAMA (lib.py sözleşmesiyle aynı):
  * Sinyal t kapanışına (16:00 ET) kadar bilinen veriyle. Coinbase GÜNLÜK mum 00:00 UTC'de kapanır
    (ABD kış saatinde 19:00 ET, yaz saatinde 20:00 ET) -> ETF kapanışında (16:00 ET) t günü mumu BİLİNMEZ.
  * İki BTC dayanak serisi kurulur (ikisi de NYSE işlem günlerine örneklenir, Pazartesi = hafta sonu dahil):
      BTC_D  : 2016-11..2026-11, NYSE günü t'nin "kapanışı" = UTC t günü mumunun kapanışı (00:00 UTC t+1,
               yani 16:00 ET'den 3-4 saat SONRA). Sinyal ve giriş AYNI zaman damgasında (C0) -> kendi içinde
               ileri bakışsız; ama ETF'ye aktarılırken zaman kayması vardır. Yalnız C0 ve C1 (bir sonraki proxy
               kapanışında gir) raporlanır; O1 anlamsız (24 saat piyasa, açılış yok).
               h/l: önceki NYSE gününden sonraki tüm takvim günlerinin mumlarının max/min'i.
      BTC_ET : 2023-05..2026-11, saatlik veriden 16:00 ET fiyatı (lib.btc_at_us_close). o = 09:30 ET tahmini
               (09:00 ET mumunun açılış ve kapanış ortalaması), h/l = önceki 16:00 ET'den bu yana saatlik max/min.
               ETF ile birebir zaman uyumlu; O1 = 09:30 ET'de gir.
  * Maliyet: BTC serilerinde işlem aracı IBIT kabul edilir -> cost = lib.cost_bp(IBIT) (2.500$ pozisyonda).
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, KOD)
import numpy as np, pandas as pd
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_kripto")
os.makedirs(OUT, exist_ok=True)

FAM = ["IBIT", "FBTC", "GBTC", "BITB", "ARKB", "BITO", "ETHA", "ETHE", "BITX", "BITI", "ETHU", "SBIT", "BITU", "BLOK", "MSTU", "CONL"]
GROUPS = {
    "BTC_spot": ["IBIT", "FBTC", "GBTC", "BITB", "ARKB"],
    "BTC_vadeli": ["BITO"],
    "BTC_2x": ["BITX", "BITU"],
    "BTC_ters_1x": ["BITI"],
    "BTC_ters_2x": ["SBIT"],
    "ETH_spot": ["ETHA", "ETHE"],
    "ETH_2x": ["ETHU"],
    "blokzincir_hisse": ["BLOK"],
    "MSTR_2x": ["MSTU"],
    "COIN_2x": ["CONL"],
}
SYM2GRP = {s: g for g, ss in GROUPS.items() for s in ss}
# Uzun yönlü (dayanağa long) grup temsilcileri. Dayanak bazında bağımsızlık: BTC (IBIT/BITO/BITX aynı dayanak!),
# ETH (ETHA/ETHU), hisse (BLOK, MSTU, CONL). Ters ürünler ayrı değerlendirilir.
REPS_LONG = ["IBIT", "BITO", "BITX", "ETHA", "ETHU", "BLOK", "MSTU", "CONL"]
REPS_INV = ["BITI", "SBIT"]
UNDERLYING = {"IBIT": "BTC", "FBTC": "BTC", "GBTC": "BTC", "BITB": "BTC", "ARKB": "BTC", "BITO": "BTC", "BITX": "BTC",
              "BITU": "BTC", "BITI": "-BTC", "SBIT": "-BTC", "ETHA": "ETH", "ETHE": "ETH", "ETHU": "ETH",
              "BLOK": "hisse", "MSTU": "MSTR", "CONL": "COIN"}

_c = {}

def nyse_days():
    if "nyse" not in _c:
        _c["nyse"] = lib.load("SPY").index
    return _c["nyse"]

def cost_ibit(pos=lib.POS_USD):
    return lib.cost_bp(lib.load("IBIT"), pos)

def spread_bp(sym):
    return lib.spread_bp_tier(lib.load(sym))

def cost_at(sym_or_spread, pos):
    sp = sym_or_spread if isinstance(sym_or_spread, (int, float)) else spread_bp(sym_or_spread)
    return 2 * lib.COMM_USD / pos * 1e4 + sp

def crypto_daily_proxy(pair="BTC-USD"):
    """BTC_D: NYSE günlerine örneklenmiş günlük UTC mum serisi (bkz. modül açıklaması)."""
    key = ("D", pair)
    if key in _c: return _c[key].copy()
    d = pd.read_parquet(os.path.join(ROOT, "data", "crypto", pair + ".parquet"))
    d.index = pd.to_datetime(d.index).normalize()
    days = nyse_days()
    days = days[days <= d.index[-1]]
    # her takvim gününü >= ilk NYSE gününe ata
    pos = np.searchsorted(days.values, d.index.values, side="left")
    ok = pos < len(days)
    d = d[ok].copy(); d["grp"] = days.values[pos[ok]]
    d = d[d.index > days[0] - pd.Timedelta(days=1)]
    g = d.groupby("grp")
    out = pd.DataFrame({"o": g["o"].first(), "h": g["h"].max(), "l": g["l"].min(), "c": g["c"].last(),
                        "ncal": g.size()})
    out = out[out.index >= days[0]]
    # NYSE günü t'nin grubu t tarihli mumla bitmeli (t mumu 00:00 UTC t+1'de kapanır); değilse at
    out = out[out.index.isin(d.index)]
    out.index.name = "date"
    _c[key] = out
    return out.copy()

def crypto_et_proxy(pair="BTC-USD"):
    """BTC_ET: saatlik veriden 16:00 ET kapanış; o = 09:30 ET tahmini; h/l önceki 16:00'dan beri."""
    key = ("ET", pair)
    if key in _c: return _c[key].copy()
    h = pd.read_parquet(os.path.join(ROOT, "data", "crypto", pair + "_h1.parquet"))
    hh = h.copy(); hh.index = h.index.tz_convert("America/New_York")
    c16 = lib.btc_at_us_close(pair)
    days = nyse_days()
    days = days[(days >= c16.index[0] + pd.Timedelta(days=3)) & (days <= c16.index[-1])]
    # 09:30 tahmini
    m9 = hh[hh.index.hour == 9]
    o930 = (m9["o"] + m9["c"]) / 2
    o930.index = o930.index.tz_localize(None).normalize()
    o930 = o930[~o930.index.duplicated(keep="last")]
    # h/l: önceki NYSE günü 16:00 ET'den t 16:00 ET'ye kadar saatlik mumlar (başlangıç saati 16:00 prev .. 15:00 t)
    loc = hh.index.tz_localize(None)
    # her saatlik mumu (başlangıç zamanı s) 16:00'dan sonra başlıyorsa ertesi takvim gününe kaydır, sonra >= NYSE gününe ata
    eff = (loc - pd.Timedelta(hours=16)).normalize() + pd.Timedelta(days=1)
    pos = np.searchsorted(days.values, eff.values, side="left")
    ok = pos < len(days)
    tmp = pd.DataFrame({"h": hh["h"].values[ok], "l": hh["l"].values[ok]}, index=days.values[pos[ok]])
    g = tmp.groupby(level=0)
    out = pd.DataFrame(index=days)
    out["c"] = c16.reindex(days)
    out["o"] = o930.reindex(days)
    out["h"] = g["h"].max().reindex(days)
    out["l"] = g["l"].min().reindex(days)
    out = out.dropna(subset=["c"])
    out["o"] = out["o"].fillna(out["c"].shift(1))
    out["h"] = out[["h", "o", "c"]].max(axis=1); out["l"] = out[["l", "o", "c"]].min(axis=1)
    out = out.iloc[1:]
    out.index.name = "date"
    _c[key] = out
    return out.copy()

def stock(sym):
    """data/stock/<SYM> bölünme düzeltmeli (temettüsüz) o/h/l/c."""
    d = pd.read_parquet(os.path.join(ROOT, "data", "stock", sym + ".parquet")).copy()
    d = d[d["c"] > 0]
    r = d["c"] / d["c"].shift(1)
    f = pd.Series(1.0, index=d.index)
    for dt in d.index[(r < 0.55).fillna(False)]:
        prev = d["c"].shift(1)[dt]
        ratio = prev / d.at[dt, "o"]
        k = round(ratio)
        if k >= 2 and abs(ratio / k - 1) < 0.15:
            f[d.index < dt] /= k
    for col in ("o", "h", "l", "c"):
        d[col] = d[col] * f
    d["raw_c"] = d["c"]; d["dv"] = d["c"] * d["v"]
    return d

# ---------------- değerlendirme yardımcıları ----------------
def full_eval(df, sig, h, mode, spread, exit_sig=None, label=""):
    """lib.evaluate + 1.000/2.500/10.000$ maliyet duyarlılığı + p."""
    cost = cost_at(spread, lib.POS_USD)
    s, tr = lib.evaluate(df, sig, h, mode, cost, exit_sig=exit_sig, label=label)
    if s.get("n", 0) > 0:
        g = tr["gross"].values * 1e4
        for pos in (1000, 2500, 10000):
            s[f"net_{pos}"] = float(g.mean() - cost_at(spread, pos))
        s["p"] = lib.t_to_p(s.get("t", np.nan), s["n"])
        s["t_gross"] = float(g.mean() / (g.std(ddof=1) / math.sqrt(len(g)))) if len(g) > 2 else np.nan
        # ilk/ikinci yarı (kısa geçmişli seriler için IS/OOS yerine)
        half = len(tr) // 2
        s["h1_net_bp"] = float(tr["net"].values[:half].mean() * 1e4) if half > 1 else np.nan
        s["h2_net_bp"] = float(tr["net"].values[half:].mean() * 1e4) if half > 1 else np.nan
    return s, tr

def overnight_trades(df, sig, cost):
    """t kapanışında al, t+1 açılışında sat (C->O)."""
    sig = sig.reindex(df.index).fillna(False).astype(bool)
    c = df["c"]; o = df["o"].shift(-1)
    g = (o / c - 1)[sig].dropna()
    tr = pd.DataFrame({"sig_date": g.index, "entry_date": g.index, "exit_date": g.index, "gross": g.values,
                       "net": g.values - cost / 1e4, "days": 1})
    return tr

def summarize(tr, label="", cost=None, spread=None):
    s = lib.stats(tr, None, label=label)
    if s.get("n", 0) > 1:
        s["p"] = lib.t_to_p(s["t"], s["n"])
        if spread is not None:
            g = tr["gross"].values * 1e4
            for pos in (1000, 2500, 10000):
                s[f"net_{pos}"] = float(g.mean() - cost_at(spread, pos))
    return s

def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))

def nw_t(y, X, lags=1):
    n, k = X.shape
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

def is_dst(dates):
    """ABD yaz saati mi (ET) — TR saati dönüşümü için."""
    idx = pd.DatetimeIndex(dates)
    loc = (idx + pd.Timedelta(hours=12)).tz_localize("America/New_York", ambiguous=True, nonexistent="shift_forward")
    return np.array([bool(x.dst()) for x in loc])
