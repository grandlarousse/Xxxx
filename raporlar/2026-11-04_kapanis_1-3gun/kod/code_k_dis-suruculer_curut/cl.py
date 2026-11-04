"""k_dis-suruculer_curut — BAĞIMSIZ yeniden hesap kütüphanesi (tarayıcının klib/ll koduna dokunmaz).
Zaman: BIST kapanışı 15:00-15:10 UTC; VİOP uzlaşması ~15:05-15:15 UTC. Giriş/çıkış = VİOP ön vade uzlaşması.
Roll kuralı (tarayıcıdan farklı): vadeye >= 3 BIST işlem günü kalan en yakın standart kontrat (N1/mini hariç).
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUT = S + "/out/code_k_dis-suruculer_curut/res"
os.makedirs(OUT, exist_ok=True)
REGIME = pd.Timestamp("2020-03-13")

def dly(sym):
    d = pd.read_parquet(f"{S}/data/daily/{sym}.parquet")
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"])).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d

def lret(sym, field="adj", bist=False):
    d = dly(sym)
    if bist:
        stale = (d["v"].fillna(0) <= 0) & (d["h"] == d["l"])
        d = d[~stale]
    px = d[field].where(d[field] > 0)
    r = np.log(px).diff()
    return r

_P = None
def panel():
    global _P
    if _P is None:
        p = pd.read_parquet(S + "/data/viop_panel.parquet",
                            columns=["date", "code", "und", "expiry", "settle", "prev_settle", "close", "vwap", "value_tl", "trades", "oi"])
        p["code"] = p["code"].astype(str); p["und"] = p["und"].astype(str)
        p["date"] = pd.DatetimeIndex(p["date"]).normalize(); p["expiry"] = pd.DatetimeIndex(p["expiry"]).normalize()
        _P = p
    return _P

_CAL = None
def cal():
    """BIST/VİOP işlem günleri = panelde XU030 uzlaşması olan günler."""
    global _CAL
    if _CAL is None:
        p = panel(); _CAL = pd.DatetimeIndex(sorted(p.loc[p["und"] == "XU030", "date"].unique()))
    return _CAL

_FR = {}
def front(und, min_td=3):
    """Ön vade: vadeye >= min_td işlem günü kalan en yakın standart kontrat. ret = ln(settle/prev_settle) (aynı kontrat).
    Ayrıca roll günü bayrağı (kontrat değişti) ve likidite."""
    key = (und, min_td)
    if key in _FR: return _FR[key]
    p = panel(); x = p[(p["und"] == und) & p["code"].str.match(r"^F_[A-Z0-9]+\d{4}$") & ~p["code"].str.contains(r"N\d$")].copy()
    x = x[~x["code"].str.match(r"^F_[A-Z]+M\d{4}$")]
    x = x[(x["settle"] > 0) & (x["prev_settle"] > 0)]
    c = cal(); pos = pd.Series(np.arange(len(c)), index=c)
    # işlem günü sayısı: expiry'den önceki/eşit son işlem günü pozisyonu - bugünkü pozisyon
    epos = np.searchsorted(c.values, x["expiry"].values, side="right") - 1
    x["td_left"] = epos - pos.reindex(x["date"]).values
    beyond = x["expiry"].values > c.values[-1]
    x.loc[beyond, "td_left"] = x.loc[beyond, "td_left"] + np.busday_count(np.datetime64(c[-1].date()), x.loc[beyond, "expiry"].values.astype("datetime64[D]"))
    x = x[x["td_left"] >= min_td].sort_values(["date", "expiry"])
    f = x.groupby("date").head(1).set_index("date")
    out = pd.DataFrame({"ret": np.log(f["settle"] / f["prev_settle"]), "settle": f["settle"], "code": f["code"],
                        "value_tl": f["value_tl"], "trades": f["trades"], "oi": f["oi"], "td_left": f["td_left"]})
    out["roll"] = out["code"] != out["code"].shift(1)
    out.iloc[0, out.columns.get_loc("roll")] = False
    _FR[key] = out
    return out

def fut_ret(und, spot_sym=None, min_td=3):
    """Temizlenmiş VİOP ön vade getirisi (BIST takvimi). Hisse: limit bandı dışı ve spot(adj) ile > %8 ayrışma -> NaN."""
    f = front(und, min_td); r = f["ret"].reindex(cal())
    if spot_sym is not None:
        lim = np.where(r.index < REGIME, np.log(1.22), np.log(1.115))
        r[r.abs() > lim] = np.nan
        sp = lret(spot_sym, bist=True).reindex(r.index)
        r[((r - sp).abs() > 0.08) & sp.notna()] = np.nan
    else:
        sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 10 * sd) & sd.notna()] = np.nan
    return r

def to_bist(r_local, mode, c=None):
    """Yabancı günlük (yerel tarih) getiriyi BIST günü t'ye eşle.
    mode='after': piyasa BIST kapanışından SONRA kapanır (ABD/Avrupa/COMEX) -> t'de yalnız tarih < t olan günler bilinir:
                  t'ye atanır: tarih d, t_prev <= d < t (t_prev = önceki BIST günü).
    mode='before': piyasa BIST kapanışından ÖNCE kapanır (ASX/TSE) -> t_prev < d <= t."""
    c = cal() if c is None else c
    r = r_local.dropna()
    d = r.index.values
    if mode == "after":
        k = np.searchsorted(c.values, d, side="right")      # d < c[k]  -> ilk BIST günü > d
    else:
        k = np.searchsorted(c.values, d, side="left")       # d <= c[k]
    ok = k < len(c)
    s = pd.Series(r.values[ok], index=c[k[ok]])
    out = s.groupby(level=0).sum().reindex(c)
    # ilgili gün yoksa (yabancı tatil) 0 değil NaN bırak
    return out

def roll_beta(y, x, w=250, minp=100):
    m = y.notna() & x.notna(); yy = y.where(m); xx = x.where(m)
    cov = (yy * xx).rolling(w, min_periods=minp).mean() - yy.rolling(w, min_periods=minp).mean() * xx.rolling(w, min_periods=minp).mean()
    var = (xx * xx).rolling(w, min_periods=minp).mean() - xx.rolling(w, min_periods=minp).mean() ** 2
    return (cov / var).shift(1)

def zscale(x, w=250, minp=100, demean=False):
    sd = x.rolling(w, min_periods=minp).std().shift(1)
    if demean:
        mu = x.rolling(w, min_periods=minp).mean().shift(1); return (x - mu) / sd
    return x / sd

def fwd(r, h):
    a = np.full(len(r), np.nan); v = r.values
    out = pd.Series(0.0, index=r.index)
    for i in range(1, h + 1): out = out + r.shift(-i)
    return out

def trades(z, y, h, thr=1.0, roll_flag=None):
    """Örtüşmeyen işlemler. z_t (t'de bilinen), y_t = t uzlaşmasından t+h uzlaşmasına getiri. Takvim = y.index.
    Dönüş DataFrame(date, dir, gross, rolls)."""
    zz = z.reindex(y.index).values; yy = y.values; n = len(yy)
    rf = roll_flag.reindex(y.index).fillna(False).values if roll_flag is not None else np.zeros(n, bool)
    rows = []; i = 0
    while i < n:
        if np.isfinite(zz[i]) and np.isfinite(yy[i]) and abs(zz[i]) > thr:
            d = np.sign(zz[i]); nr = int(rf[i + 1:i + h + 1].sum()) if i + 1 < n else 0
            rows.append((y.index[i], d, d * yy[i], nr)); i += h
        else:
            i += 1
    return pd.DataFrame(rows, columns=["date", "dir", "gross", "rolls"]).set_index("date")

def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 5 or x.std(ddof=1) == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def summ(tr, cost, roll_cost=0.0, split="2022-01-01"):
    if len(tr) < 5: return dict(n=len(tr))
    g = tr["gross"].values * 1e4; net = g - cost - roll_cost * tr["rolls"].values
    idx = tr.index; isd = idx < pd.Timestamp(split)
    yrs = max((idx[-1] - idx[0]).days / 365.25, 0.5)
    return dict(n=len(tr), per_yr=len(tr) / yrs, gross=g.mean(), net=net.mean(), t=tstat(net), hit=(net > 0).mean(),
                long_frac=(tr["dir"] > 0).mean(), IS=net[isd].mean() if isd.sum() >= 5 else np.nan, IS_t=tstat(net[isd]), IS_n=int(isd.sum()),
                OOS=net[~isd].mean() if (~isd).sum() >= 5 else np.nan, OOS_t=tstat(net[~isd]), OOS_n=int((~isd).sum()))

def periods(tr, cost, per=None):
    per = per or [("2017-19", "2017-01-01", "2019-12-31"), ("2020-21", "2020-01-01", "2021-12-31"), ("2022-23", "2022-01-01", "2023-12-31"),
                  ("2024-26", "2024-01-01", "2026-12-31"), ("fon_krizi", "2026-09-01", "2026-10-31")]
    out = {}
    net = tr["gross"] * 1e4 - cost
    for lab, a, b in per:
        x = net[(net.index >= a) & (net.index <= b)]
        out[lab] = (round(x.mean(), 1) if len(x) else np.nan, round(tstat(x), 2) if len(x) >= 5 else np.nan, len(x))
    return out

def drop_top(tr, cost, k=10):
    net = (tr["gross"] * 1e4 - cost).sort_values()
    x = net.iloc[:-k] if len(net) > k else net.iloc[:0]
    return x.mean(), tstat(x)

def by_year(tr, cost):
    net = tr["gross"] * 1e4 - cost
    return net.groupby(net.index.year).mean().round(0).astype(int).to_dict()

def circ_null(z, y_dict, grid, nsim=500, seed=7, minshift=250):
    """Veri madenciliği düzeltmeli null: sinyali takvimde dairesel kaydır (otokorelasyon + işaret dağılımı korunur),
    ızgaradaki (h, thr, bacak) varyantların en yüksek t'sini al. Dönüş: max-t dağılımı ve her varyant için tek p."""
    rng = np.random.default_rng(seed); zv = z.reindex(y_dict[next(iter(y_dict))].index)
    n = len(zv); mx = []; per = {g: [] for g in grid}
    for _ in range(nsim):
        k = int(rng.integers(minshift, n - minshift))
        zs = pd.Series(np.roll(zv.values, k), index=zv.index)
        best = -np.inf
        for g in grid:
            h, thr, leg, cost = g
            tr = trades(zs, y_dict[(h, leg)], h, thr)
            t = tstat(tr["gross"].values * 1e4 - cost) if len(tr) >= 5 else np.nan
            per[g].append(t)
            if np.isfinite(t): best = max(best, t)
        mx.append(best)
    return np.array(mx), {g: np.array(v) for g, v in per.items()}

def nw_reg(y, X, lags):
    df = pd.concat([y.rename("_y")] + [X[c].rename(c) for c in X.columns], axis=1).dropna()
    n = len(df)
    if n < 60: return None
    Xc = np.column_stack([np.ones(n), df.drop(columns="_y").values]); yy = df["_y"].values
    iXX = np.linalg.pinv(Xc.T @ Xc); b = iXX @ Xc.T @ yy; e = yy - Xc @ b; u = Xc * e[:, None]; Sm = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; Sm += w * (G + G.T)
    se = np.sqrt(np.diag(iXX @ Sm @ iXX))
    return pd.DataFrame({"b": b, "t": b / se}, index=["const"] + list(X.columns)), n

def liq(und):
    f = front(und)
    g = f.groupby(f.index.year).agg(med_value_mn=("value_tl", lambda v: np.nanmedian(v) / 1e6), med_trades=("trades", "median"),
                                    zero_trade_frac=("trades", lambda v: float((v.fillna(0) <= 0).mean())))
    return g.round(2)

def costs():
    l = pd.read_csv(S + "/out/y_viop_likidite.csv").set_index("und")
    return l
