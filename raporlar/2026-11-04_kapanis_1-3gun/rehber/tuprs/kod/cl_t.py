"""rehber_tuprs — araştırma kütüphanesi cl.py'nin (out/code_k_dis-suruculer_curut/cl.py) birebir kopyası;
yalnız veri yolları değişti: Yahoo günlük -> rehber/tuprs/veri/daily (yoksa ortak data/daily),
VİOP paneli = ortak panel (2017-03..2026-10-30) + 02-03.11.2026 bültenleri (dl_k_sahol_a/viop_new.parquet, salt okunur).
LAST_BIST: tamamlanmış son BIST günü (gün-içi kısmi Yahoo barı atılır)."""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
R = S + "/out/rehber/tuprs"
OUT = R + "/sonuc"
os.makedirs(OUT, exist_ok=True)
REGIME = pd.Timestamp("2020-03-13")
LAST_BIST = pd.Timestamp("2026-11-03")
NEW_VIOP = S + "/dl_k_sahol_a/viop_new.parquet"
USE_NEW = True

def dly(sym):
    p = f"{R}/veri/daily/{sym}.parquet"
    if not os.path.exists(p): p = f"{S}/data/daily/{sym}.parquet"
    d = pd.read_parquet(p)
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"])).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    if sym.endswith(".IS"): d = d[d.index <= LAST_BIST]
    return d

def lret(sym, field="adj", bist=False):
    d = dly(sym)
    if bist:
        stale = (d["v"].fillna(0) <= 0) & (d["h"] == d["l"])
        d = d[~stale]
    px = d[field].where(d[field] > 0)
    return np.log(px).diff()

_P = None
def panel():
    global _P
    if _P is None:
        cols = ["date", "code", "und", "expiry", "settle", "prev_settle", "close", "vwap", "value_tl", "trades", "oi"]
        p = pd.read_parquet(S + "/data/viop_panel.parquet", columns=cols)
        if USE_NEW and os.path.exists(NEW_VIOP):
            q = pd.read_parquet(NEW_VIOP, columns=cols)
            q = q[q["date"] > p["date"].max()]
            for c in ("code", "und"): p[c] = p[c].astype(str); q[c] = q[c].astype(str)
            p = pd.concat([p, q], ignore_index=True)
        p["code"] = p["code"].astype(str); p["und"] = p["und"].astype(str)
        p["date"] = pd.DatetimeIndex(p["date"]).normalize(); p["expiry"] = pd.DatetimeIndex(p["expiry"]).normalize()
        _P = p
    return _P

_CAL = None
def cal():
    global _CAL
    if _CAL is None:
        p = panel(); _CAL = pd.DatetimeIndex(sorted(p.loc[p["und"] == "XU030", "date"].unique()))
    return _CAL

_FR = {}
def contracts(und):
    """Standart pay/endeks vadeli kontratları (N1/mini hariç), td_left ile."""
    p = panel(); x = p[(p["und"] == und) & p["code"].str.match(r"^F_[A-Z0-9]+\d{4}$") & ~p["code"].str.contains(r"N\d$")].copy()
    x = x[~x["code"].str.match(r"^F_[A-Z]+M\d{4}$")]
    c = cal(); pos = pd.Series(np.arange(len(c)), index=c)
    epos = np.searchsorted(c.values, x["expiry"].values, side="right") - 1
    x["td_left"] = epos - pos.reindex(x["date"]).values
    beyond = x["expiry"].values > c.values[-1]
    x.loc[beyond, "td_left"] = x.loc[beyond, "td_left"] + np.busday_count(np.datetime64(c[-1].date()), x.loc[beyond, "expiry"].values.astype("datetime64[D]"))
    return x

def front(und, min_td=3):
    key = (und, min_td)
    if key in _FR: return _FR[key]
    x = contracts(und)
    x = x[(x["settle"] > 0) & (x["prev_settle"] > 0)]
    x = x[x["td_left"] >= min_td].sort_values(["date", "expiry"])
    f = x.groupby("date").head(1).set_index("date")
    out = pd.DataFrame({"ret": np.log(f["settle"] / f["prev_settle"]), "settle": f["settle"], "code": f["code"],
                        "value_tl": f["value_tl"], "trades": f["trades"], "oi": f["oi"], "td_left": f["td_left"]})
    out["roll"] = out["code"] != out["code"].shift(1)
    out.iloc[0, out.columns.get_loc("roll")] = False
    _FR[key] = out
    return out

def fut_ret(und, spot_sym=None, min_td=3):
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
    c = cal() if c is None else c
    r = r_local.dropna(); d = r.index.values
    k = np.searchsorted(c.values, d, side="right") if mode == "after" else np.searchsorted(c.values, d, side="left")
    ok = k < len(c)
    s = pd.Series(r.values[ok], index=c[k[ok]])
    return s.groupby(level=0).sum().reindex(c)

def roll_beta(y, x, w=250, minp=100):
    m = y.notna() & x.notna(); yy = y.where(m); xx = x.where(m)
    cov = (yy * xx).rolling(w, min_periods=minp).mean() - yy.rolling(w, min_periods=minp).mean() * xx.rolling(w, min_periods=minp).mean()
    var = (xx * xx).rolling(w, min_periods=minp).mean() - xx.rolling(w, min_periods=minp).mean() ** 2
    return (cov / var).shift(1)

def zscale(x, w=250, minp=100):
    sd = x.rolling(w, min_periods=minp).std().shift(1)
    return x / sd

def fwd(r, h):
    out = pd.Series(0.0, index=r.index)
    for i in range(1, h + 1): out = out + r.shift(-i)
    return out

def trades(z, y, h, thr=1.0, roll_flag=None):
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

MEM = ["VLO", "MPC", "PSX", "PBF"]
def signal_z():
    """Araştırma kuralı (c1_ref.py) birebir: P = ort(VLO,MPC,PSX,PBF artıkları), en az 3 üye; z = to_bist(P,'after') / std250 (önceki)."""
    rm = lret("^GSPC", "adj")
    RS = []
    for m in MEM:
        r = lret(m, "adj"); b = roll_beta(r, rm.reindex(r.index), 250, 100); RS.append((r - b * rm.reindex(r.index)).rename(m))
    df = pd.concat(RS, axis=1)
    P = df.mean(axis=1).where(df.notna().sum(axis=1) >= 3)
    Pb = to_bist(P, "after")
    return zscale(Pb, 250, 100), Pb, P, df
