"""v_A4_a bağımsız çekirdek (ll.py / h.py IMPORT EDİLMEZ). Ham parquet -> kendi hizalama/temizlik.
Tanımlar r1_havacilik kaynak kodundan (a3_multi.signals, a5b_attrib) okunup yeniden yazıldı:
  EU_AIR = LHA.DE AF.PA IAG.L RYA.IR EZJ.L WIZZ.L JET2.L ; US_AIR = DAL UAL AAL LUV ALK JBLU
  sepet = üyelerin log getiri ortalaması (>=2 üye), sıfır getiri (tatil ffill) -> NaN
  artık = sepet - beta_roll * endeks (STOXX / SPX), beta: 250g kayan cov/var (min 120), shift(1)
  z = (x - mean250)/std250, ikisi de shift(1) (min 60); clip ±3 ; AIR = zEU + zUS ; |AIR|>1 -> sign
  sinyal t-1 -> BIST gün-içi t (log c/o). Maliyet işlem başına gidiş-dönüş.
"""
import numpy as np, pandas as pd, os, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUTD = S + "/out/code_v_A4_a/res"
os.makedirs(OUTD, exist_ok=True)
EU_AIR = ["LHA.DE", "AF.PA", "IAG.L", "RYA.IR", "EZJ.L", "WIZZ.L", "JET2.L"]
US_AIR = ["DAL", "UAL", "AAL", "LUV", "ALK", "JBLU"]
UP, DN = np.log(1.105), np.log(0.895)
SPLIT = pd.Timestamp("2021-01-01")

_raw = {}
def raw(sym, kind="daily"):
    k = (sym, kind)
    if k not in _raw:
        _raw[k] = pd.read_parquet(f"{S}/data/{kind}/{sym}.parquet")
    return _raw[k]

def bist_calendar():
    d = raw("XU100.IS")
    d = d[d.v.fillna(0) > 0]
    return pd.DatetimeIndex(sorted(set(d.ldate)))

CAL = None
def cal():
    global CAL
    if CAL is None: CAL = bist_calendar()
    return CAL

def bist_day(sym):
    """Hisse günlük ayrıştırma (kendi). index=ldate. cc(adj), intra=log(c/o), gap=cc-intra. Simetrik ±%10,5 temizlik."""
    d = raw(sym).copy(); d.index = pd.DatetimeIndex(d.ldate); d = d[~d.index.duplicated(keep="last")]
    if (d.v.fillna(0) > 0).mean() > 0.5: d = d[d.v.fillna(0) > 0]
    cc = np.log(d.adj).diff()
    intra = np.log(d.c / d.o)
    bad_o = (d.o <= 0) | d.o.isna() | ((d.h == d.l) & (d.o == d.c.shift(1)))
    intra[bad_o] = np.nan
    gap = cc - intra
    df = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra, "o": d.o, "c": d.c, "v": d.v})
    bad = (df.cc > UP) | (df.cc < DN)
    df.loc[bad, ["cc", "gap", "intra"]] = np.nan
    df.loc[df.index < "2014-01-01", ["gap", "intra"]] = np.nan
    badg = (df.gap > UP) | (df.gap < DN)
    df.loc[badg, ["gap", "intra"]] = np.nan
    return df

def drv_ret_cal(sym, field="adj"):
    """Varyant A (kaynakla aynı mantık, kendi kodu): BIST günü t fiyatı = ldate<=t olan son kapanış; log fark; 12-sigma sıçrama temizliği; 0 -> NaN."""
    d = raw(sym); s = pd.Series(d[field].values, index=pd.DatetimeIndex(d.ldate)).astype(float)
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0]
    if sym.endswith("=X"):
        s = s.shift(-1).dropna()  # FX 00:00 UTC kayması
    c = cal(); c = c[c >= s.index[0]]
    p = s.reindex(s.index.union(c)).ffill().reindex(c)
    r = np.log(p).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1)
    r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r.where(r != 0)

def drv_ret_open(sym, field="adj"):
    """Varyant B (zaman damgası temelli): BIST günü t için bilgi = takvim tarihi < t olan son kapanış (AB/ABD kapanışları t-1 akşamı, BIST açılışından önce).
    sinyal_B(t) = log P(son kapanış < t) - log P(son kapanış < t_önceki BIST günü). Doğrudan t'de KULLANILIR (shift gerekmez)."""
    d = raw(sym); s = pd.Series(d[field].values, index=pd.DatetimeIndex(d.ldate)).astype(float)
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0]
    c = cal(); c = c[c > s.index[0]]
    pos = s.index.searchsorted(c, side="left") - 1  # ldate < t
    p = pd.Series(s.values[pos], index=c)
    r = np.log(p).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1)
    r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r.where(r != 0)

def basket(syms, fn=drv_ret_cal, min_n=2):
    X = pd.concat([fn(s).rename(s) for s in syms], axis=1)
    return X.mean(axis=1, skipna=True).where(X.notna().sum(1) >= min_n), X

def rresid(y, x, w=250, mp=120):
    df = pd.concat([y.rename("y"), x.rename("x")], axis=1)
    b = (df.y.rolling(w, min_periods=mp).cov(df.x) / df.x.rolling(w, min_periods=mp).var()).shift(1)
    return df.y - b * df.x

def zs(x, w=250, mp=60):
    mu = x.rolling(w, min_periods=mp).mean().shift(1); sd = x.rolling(w, min_periods=mp).std().shift(1)
    return (x - mu) / sd

def nw_mean_t(x, lags=5):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x)
    if n < 20: return np.nan
    e = x - x.mean(); g0 = (e @ e) / n; v = g0
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); v += 2 * w * (e[L:] @ e[:-L]) / n
    return x.mean() / np.sqrt(v / n)

def bt(sig, y, cost=8.0, thr=1.0, split=SPLIT, start=None, end=None):
    """sig: t'de pozisyondan ÖNCE bilinen değer (hizalı). pos = sign(sig) if |sig|>thr. pnl = pos*y - cost*|pos|."""
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    pos = np.sign(df.s).where(df.s.abs() > thr, 0.0)
    pnl = pos * df.y - cost / 1e4 * pos.abs()
    out = {}
    for per, m in [("IS", df.index < split), ("OOS", df.index >= split), ("ALL", np.ones(len(df), bool))]:
        p = pnl[m]; ps = pos[m]; a = ps != 0; n = int(a.sum())
        if n < 20: out[per] = {"n": n}; continue
        pa = p[a]
        ann = pa.mean() * 252 * a.mean(); vol = p.std() * np.sqrt(252)
        out[per] = {"n": n, "bps": 1e4 * pa.mean(), "t_nw": nw_mean_t(pa.values), "t_iid": pa.mean() / pa.std() * np.sqrt(n),
                    "hit": float((pa > 0).mean()), "SR": ann / vol if vol > 0 else np.nan,
                    "gross_bps": 1e4 * (pa.mean() + cost / 1e4), "t_gross": nw_mean_t((pa + cost / 1e4).values),
                    "nlong": int((ps > 0).sum()), "nshort": int((ps < 0).sum())}
    yr = pnl[pos != 0]
    out["years"] = (1e4 * yr.groupby(yr.index.year).mean()).round(1).to_dict()
    out["years_n"] = yr.groupby(yr.index.year).size().to_dict()
    return out, pnl, pos

def build_signals(fn=drv_ret_cal, w_beta=250, eu=EU_AIR, us=US_AIR, idx_eu="^STOXX", idx_us="^GSPC"):
    EU, _ = basket(eu, fn); US, _ = basket(us, fn)
    sx = fn(idx_eu); sp = fn(idx_us)
    out = pd.DataFrame({"EU": EU, "US": US, "SX": sx, "SP": sp})
    out["EU_X"] = rresid(EU, sx, w_beta); out["US_X"] = rresid(US, sp, w_beta)
    out["TUR"] = fn("TUR")
    out["zEU"] = zs(out.EU_X).clip(-3, 3); out["zUS"] = zs(out.US_X).clip(-3, 3); out["zTUR"] = zs(out.TUR).clip(-3, 3)
    out["AIR"] = out.zEU + out.zUS
    out["COMBO"] = out.zEU + out.zUS - out.zTUR
    out["AIR_raw"] = zs(EU).clip(-3, 3) + zs(US).clip(-3, 3)
    return out
