"""k_dis ortak kütüphane — kapanıştan kapanışa (VİOP uzlaşma t -> t+h) dış sürücü testleri.
ZAMAN: karar BIST kapanışında (15:00-15:15 UTC). Sinyal yalnız 15:00 UTC'ye kadar bilinen bilgiyle kurulur.
 - Saatlik sürücü fiyatı: snap(sym,'15:00') = 15:00 UTC'de BİLİNEN son fiyat (bitmiş barın kapanışı ya da başlamış barın açılışı).
 - Günlük: Asya kapanışı t (BIST'ten önce) kullanılabilir; Avrupa/ABD günlük kapanışı t KULLANILAMAZ -> t-1 (shift(1)).
 - Hedef: VİOP ön vade uzlaşma getirisi (aynı kontrat ln(settle/prev_settle)), t+1..t+h toplamı.
"""
import os, sys, re, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, S + "/code")
import ll
from universe import VIOP
RES = S + "/out/code_k_dis/res"
os.makedirs(RES, exist_ok=True)
STOCKS = list(VIOP)
REGIME = pd.Timestamp("2020-03-13")

def lim_series(idx):
    pre = np.asarray(idx < REGIME)
    return pd.Series(np.where(pre, np.log(1.205), np.log(1.105)), index=idx)

# ---------------- VİOP ön vade ----------------
_PANEL = None
def panel():
    global _PANEL
    if _PANEL is None:
        _PANEL = pd.read_parquet(S + "/data/viop_panel.parquet",
                                 columns=["date", "code", "und", "expiry", "settle", "prev_settle", "value_tl", "trades", "oi", "vwap"])
        _PANEL["und"] = _PANEL["und"].astype(str); _PANEL["code"] = _PANEL["code"].astype(str)
    return _PANEL

def viop_front(und, min_bd=2):
    """Her gün: vadesine >= min_bd iş günü kalan en yakın vade. ret = ln(settle/prev_settle) aynı kontrat."""
    p = panel(); x = p[(p["und"] == und) & p["code"].str.match(r"^F_[A-Z]+[0-9]*\d{4}$")].copy()
    x["mini"] = x["code"].str.match(r"^F_[A-Z]+M\d{4}$") & ~x["code"].str.match(r"^F_XAUTRYM")
    x = x[(x["settle"] > 0) & (x["prev_settle"] > 0)]
    x["bd"] = np.busday_count(x["date"].values.astype("datetime64[D]"), x["expiry"].values.astype("datetime64[D]"))
    x = x[x["bd"] >= min_bd].sort_values(["date", "expiry", "mini"])
    f = x.groupby("date").head(1).set_index("date")
    r = np.log(f["settle"] / f["prev_settle"])
    out = pd.DataFrame({"ret": r, "settle": f["settle"], "code": f["code"], "value_tl": f["value_tl"], "trades": f["trades"], "oi": f["oi"]})
    out.index = pd.DatetimeIndex(out.index)
    return out

_FUT = None
def fut_panel():
    """DataFrame (tarih x und) VİOP ön vade log getirileri, temizlenmiş. 47 hisse + XU030 + USDTRY + XAUUSD + XAUTRY."""
    global _FUT
    if _FUT is not None: return _FUT
    fp = RES + "/_fut_ret.parquet"
    if os.path.exists(fp):
        _FUT = pd.read_parquet(fp); return _FUT
    cols = {}
    for u in STOCKS + ["XU030", "XLBNK", "USDTRY", "XAUUSD", "XAUTRY"]:
        f = viop_front(u)
        r = f["ret"].copy()
        # işlem yoksa (trades==0) uzlaşma teorik olabilir: işaretle ama tut (getiri uzlaşmadan); likidite ayrı raporlanır
        if u in STOCKS:
            lim = lim_series(r.index); r[(r.abs() > lim)] = np.nan
            try:
                sp = ll.ret(u).reindex(r.index)
                bad = (r - sp).abs() > 0.06  # kurumsal işlem / düzeltme farkı
                r[bad & sp.notna()] = np.nan
            except Exception as e:
                print("spot yok", u, e)
        else:
            sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 10 * sd) & sd.notna()] = np.nan
        cols[u] = r
    _FUT = pd.DataFrame(cols).sort_index()
    _FUT.to_parquet(fp)
    return _FUT

_SPOT = None
def spot_panel():
    global _SPOT
    if _SPOT is not None: return _SPOT
    fp = RES + "/_spot_ret.parquet"
    if os.path.exists(fp):
        _SPOT = pd.read_parquet(fp); return _SPOT
    cols = {u: ll.ret(u) for u in STOCKS + ["XU030", "XU100"]}
    _SPOT = pd.DataFrame(cols).sort_index(); _SPOT = _SPOT[_SPOT.index >= "2012-01-01"]
    _SPOT.to_parquet(fp); return _SPOT

def fwd(R, h):
    """t+1..t+h toplam (eksik gün varsa NaN)."""
    out = 0
    for i in range(1, h + 1):
        out = out + R.shift(-i)
    return out

def cum(R, k, lag=0):
    """t-lag-k+1 .. t-lag toplam."""
    out = 0
    for i in range(lag, lag + k):
        out = out + R.shift(i)
    return out

def roll_beta(y, x, w=250, minp=60):
    """y,x: Series ya da DataFrame (aynı şekil ya da x Series). Geçmiş pencere, shift(1) -> look-ahead yok."""
    if isinstance(y, pd.DataFrame) and isinstance(x, pd.Series):
        x = pd.DataFrame({c: x for c in y.columns}, index=y.index)
    m = y.notna() & x.notna()
    yy = y.where(m); xx = x.where(m)
    mxy = (yy * xx).rolling(w, min_periods=minp).mean(); mx = xx.rolling(w, min_periods=minp).mean(); my = yy.rolling(w, min_periods=minp).mean()
    mxx = (xx * xx).rolling(w, min_periods=minp).mean()
    b = (mxy - mx * my) / (mxx - mx * mx)
    return b.shift(1)

def zroll(x, w=250, minp=60):
    """Geçmiş pencereyle z (bugünkü değer dahil değil -> shift(1) istatistikleri)."""
    mu = x.rolling(w, min_periods=minp).mean().shift(1); sd = x.rolling(w, min_periods=minp).std().shift(1)
    return (x - mu) / sd

def sdscale(x, w=250, minp=60):
    """Ortalama çıkarmadan geçmiş std ile ölçekle (getiri sinyalleri için)."""
    sd = x.rolling(w, min_periods=minp).std().shift(1)
    return x / sd

# ---------------- saatlik anlık fiyat ----------------
_SN = {}
def snap(sym, hhmm="15:00", max_age_days=4):
    """UTC günü t için hhmm UTC anında BİLİNEN son fiyat: (bar_başı, open) ve (bar_sonu, close) olayları içinde son olan.
    60 dk bar varsayımı (Yahoo 60m). Index: tarih (UTC günü)."""
    key = (sym, hhmm)
    if key in _SN: return _SN[key]
    d = ll.raw(sym, "h1"); d = d[~d.index.duplicated(keep="last")].sort_index()
    ev_t = np.concatenate([d.index.values, (d.index + pd.Timedelta(minutes=60)).values])
    ev_v = np.concatenate([d["o"].values, d["c"].values])
    ev_k = np.concatenate([np.zeros(len(d)), np.ones(len(d))])  # aynı anda açılış ve kapanış: kapanış önce gelsin diye sırala
    o = np.lexsort((ev_k, ev_t)); ev_t = ev_t[o]; ev_v = ev_v[o]
    ok = np.isfinite(ev_v) & (ev_v > 0); ev_t = ev_t[ok]; ev_v = ev_v[ok]
    h, m = map(int, hhmm.split(":"))
    days = pd.DatetimeIndex(pd.DatetimeIndex(d.index.tz_convert(None)).normalize().unique()).sort_values()
    days = pd.date_range(days[0], days[-1], freq="D")
    tg = (days + pd.Timedelta(hours=h, minutes=m)).tz_localize("UTC").values
    pos = np.searchsorted(ev_t, tg, side="right") - 1
    v = np.where(pos >= 0, ev_v[np.clip(pos, 0, None)], np.nan)
    age = (tg - ev_t[np.clip(pos, 0, None)]) / np.timedelta64(1, "D")
    v[(pos < 0) | (age > max_age_days)] = np.nan
    s = pd.Series(v, index=days)
    _SN[key] = s
    return s

_CAL = None
def cal():
    global _CAL
    if _CAL is None:
        f = fut_panel(); c = ll.bist_cal(); _CAL = c
    return _CAL

def r_snap(sym, hhmm="15:00"):
    """BIST takviminde (t-1 hhmm, t hhmm] log getirisi."""
    s = snap(sym, hhmm); c = cal(); c = c[(c >= s.dropna().index[0]) & (c <= s.dropna().index[-1])]
    px = s.reindex(c)
    r = np.log(px).diff()
    sd = r.rolling(120, min_periods=30).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r

# ---------------- istatistik ----------------
def nw_ols(y, X, lags):
    """y (n,), X (n,k) sabit dahil değil -> sabit eklenir. Dönüş: b (k+1), t (k+1), n."""
    n = len(y)
    Xc = np.column_stack([np.ones(n), X])
    XtX = Xc.T @ Xc
    try: iXX = np.linalg.inv(XtX)
    except np.linalg.LinAlgError: return None
    b = iXX @ (Xc.T @ y); e = y - Xc @ b
    u = Xc * e[:, None]
    Sm = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; Sm += w * (G + G.T)
    V = iXX @ Sm @ iXX
    se = np.sqrt(np.clip(np.diag(V), 1e-30, None))
    return b, b / se, n

def reg(y, x, lags, minn=60):
    """y Series, x Series ya da DataFrame. Dönüş dict: b,t (ilk regresör), n."""
    if isinstance(x, pd.Series): x = x.to_frame("x")
    df = pd.concat([y.rename("_y"), x], axis=1).dropna()
    if len(df) < minn: return dict(b=np.nan, t=np.nan, n=len(df))
    o = nw_ols(df["_y"].values, df.drop(columns="_y").values, lags)
    if o is None: return dict(b=np.nan, t=np.nan, n=len(df))
    b, t, n = o
    out = dict(b=b[1], t=t[1], n=n)
    for j in range(2, len(b)): out[f"b{j}"] = b[j]; out[f"t{j}"] = t[j]
    return out

def mean_nw(x, lags):
    x = np.asarray(pd.Series(x).dropna(), float); n = len(x)
    if n < 15: return np.nan, np.nan, n
    m = x.mean(); e = x - m; s = (e * e).sum()
    for l in range(1, lags + 1): s += 2 * (1 - l / (lags + 1)) * (e[l:] * e[:-l]).sum()
    se = np.sqrt(s) / n
    return m, m / se if se > 0 else np.nan, n

def t2p(t):
    from scipy import stats
    return 2 * (1 - stats.norm.cdf(np.abs(t)))

def bh(p, q=0.05):
    p = np.asarray(p, float); ok = np.isfinite(p); rej = np.zeros(len(p), bool); padj = np.full(len(p), np.nan)
    if ok.sum():
        from statsmodels.stats.multitest import multipletests
        r, pa, _, _ = multipletests(p[ok], alpha=q, method="fdr_bh"); rej[ok] = r; padj[ok] = pa
    return rej, padj

def trades_nonoverlap(sig, y_h, h, thr=1.0):
    """sig: z (t'de bilinen); y_h: t->t+h getirisi. Pozisyonda değilken |z|>thr ise gir, h gün tut, sonra yeniden bak.
    Dönüş: DataFrame(date, dir, gross)."""
    df = pd.concat([sig.rename("z"), y_h.rename("y")], axis=1).dropna()
    z = df["z"].values; y = df["y"].values; idx = df.index
    # takvim indeksini kullanarak h iş günü ilerle (df boşlukları için tarih bazlı pozisyon)
    allidx = y_h.index; posmap = pd.Series(np.arange(len(allidx)), index=allidx)
    pos = posmap.reindex(idx).values
    rows = []; next_free = -1
    for i in range(len(z)):
        if pos[i] < next_free: continue
        if abs(z[i]) > thr:
            d = np.sign(z[i]); rows.append((idx[i], d, d * y[i])); next_free = pos[i] + h
    return pd.DataFrame(rows, columns=["date", "dir", "gross"]).set_index("date") if rows else pd.DataFrame(columns=["dir", "gross"])

def trade_stats(tr, cost_bps, split, years_total=None):
    if len(tr) < 5: return dict(n=len(tr))
    g = tr["gross"].values * 1e4; net = g - cost_bps
    from scipy import stats
    t = net.mean() / (net.std(ddof=1) / np.sqrt(len(net))) if net.std() > 0 else np.nan
    sp = pd.Timestamp(split); isd = tr.index < sp
    yrs = (tr.index[-1] - tr.index[0]).days / 365.25 if years_total is None else years_total
    o = dict(n=len(tr), per_yr=len(tr) / max(yrs, 0.5), gross=g.mean(), net=net.mean(), t_net=t, hit=(net > 0).mean(),
             IS_net=(net[isd].mean() if isd.sum() >= 5 else np.nan), IS_n=int(isd.sum()),
             OOS_net=(net[~isd].mean() if (~isd).sum() >= 5 else np.nan), OOS_n=int((~isd).sum()))
    for lab, msk in (("IS", isd), ("OOS", ~isd)):
        x = net[msk]; o[lab + "_t"] = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) >= 5 and x.std() > 0 else np.nan
    by = pd.Series(net, index=tr.index).groupby(tr.index.year).mean().round(0)
    o["by_year"] = ";".join(f"{k}:{int(v)}" for k, v in by.items())
    o["yrs_pos"] = f"{int((by > 0).sum())}/{len(by)}"
    return o

def cost_table():
    l = pd.read_csv(S + "/out/y_viop_likidite.csv").set_index("und")
    return l["rt_cost_small_bps"].to_dict(), l["rt_cost_1m_bps"].to_dict()
