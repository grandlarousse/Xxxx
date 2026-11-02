"""v_hakem bağımsız kütüphanesi (ll.py IMPORT EDİLMEZ). Ham parquet'ten hizalama/temizlik.
ZAMANLAMA (UTC): BIST sürekli işlem 07:00–15:00 (+15:00–15:10 kapanış seansı); açılış seansı 06:40–07:00.
 - 'post' kova (ABD, Kanada, Latin Amerika, Avrupa ana borsaları): yerel tarih d seansı BIST d kapanışından SONRA biter
   -> bilgi BIST'in d'den SONRAKİ ilk işlem gününe (t > d) atanır. (ABD 20/21, Avrupa 15:30/16:30)
 - 'pre' kova (Tokyo, Seul, Taipei, Sidney, NZ): yerel tarih d seansı 05:00–06:30 UTC'de, BIST d açılışından ÖNCE biter
   -> bilgi d'ye eşit/sonraki ilk BIST gününe (t >= d) atanır.
 - 'sync' kova (HK, Çin, Hindistan, Körfez, JSE, Atina, Tel Aviv, Kahire, Moskova, GD Asya): BIST seansı içinde kapanır -> kullanılmaz.
 - Pencere toplamı: BIST günü t'ye atanan tüm emsal seanslarının log getirileri toplanır (tatil birikimi doğru ele alınır).
 - '=X' FX serileri kullanılmıyor (gerekirse 1 gün kaydırma: c(ldate t) = t günü 00:00 UTC).
TEMİZLİK: BIST hissesi fiyat bazında +%10,5 üstü / -%10,5 altı günlük getiri -> NaN (cc, gap, intra). Açılış: o<=0 veya (h==l ve o==önceki c) -> NaN.
 Kurumsal işlem günü (adj/c oranı değişimi) -> gap NaN (intra = ln(c/o) aynı gün içinde olduğundan etkilenmez). 2014 öncesi gap/intra NaN.
 Yabancı emsal: hacimsiz satırlar atılır; |r| > 12 x önceki 250 seans std veya |r|>0,5 -> NaN.
"""
import os, numpy as np, pandas as pd
from scipy import stats

SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DD = os.path.join(SCR, "data", "daily")
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "res")
START, END = pd.Timestamp("2014-01-01"), pd.Timestamp("2026-10-30")
IS_END, OOS_START = pd.Timestamp("2020-12-31"), pd.Timestamp("2021-01-01")
LUP, LDN = np.log(1.105), np.log(0.895)

PRE_SUF = (".T", ".KS", ".KQ", ".TW", ".AX", ".NZ")
SYNC_SUF = (".HK", ".SS", ".SZ", ".NS", ".BO", ".SR", ".QA", ".AE", ".JO", ".AT", ".TA", ".CA", ".ME", ".BK", ".JK", ".KL", ".SI", ".IS")
EU_SUF = (".DE", ".PA", ".L", ".MI", ".MC", ".AS", ".BR", ".SW", ".ST", ".OL", ".HE", ".CO", ".WA", ".BD", ".VI", ".PR", ".LS", ".IR")
REGION_IDX = {".T": "^N225", ".KS": "^KS11", ".KQ": "^KS11", ".TW": "^TWII", ".AX": "^AXJO", ".TO": "^GSPTSE", ".MX": "^MXX", ".SA": "^BVSP"}

def suffix(sym):
    i = sym.rfind(".")
    return sym[i:] if i > 0 else ""

IDX_BUCKET = {"^N225": "pre", "^KS11": "pre", "^KQ11": "pre", "^TWII": "pre", "^AXJO": "pre", "^NZ50": "pre",
              "^HSI": "sync", "^HSCE": "sync", "000001.SS": "sync", "399001.SZ": "sync", "^NSEI": "sync", "^BSESN": "sync", "^STI": "sync", "^JKSE": "sync", "^KLSE": "sync"}
def bucket(sym):
    # DÜZELTME (v_hakem, 02.11): son eki olmayan Asya endeksleri önceden 'post' sayılıyordu (h1_build etkilenmedi: endeks emsalin kovasıyla hizalanıyor)
    if sym in IDX_BUCKET: return IDX_BUCKET[sym]
    s = suffix(sym)
    if s in PRE_SUF: return "pre"
    if s in SYNC_SUF: return "sync"
    return "post"

def region_index(sym):
    s = suffix(sym)
    if s in REGION_IDX: return REGION_IDX[s]
    if s in EU_SUF: return "^STOXX"
    return "^GSPC"

def region_name(sym):
    s = suffix(sym)
    if s in (".T",): return "JP"
    if s in (".KS", ".KQ"): return "KR"
    if s == ".TW": return "TW"
    if s == ".AX": return "AU"
    if s in EU_SUF: return "EU"
    return "AM"  # ABD + Kanada + Latin Amerika

_C = {}
def raw(sym):
    if sym in _C: return _C[sym]
    p = os.path.join(DD, sym.replace("/", "_") + ".parquet")
    if not os.path.exists(p): _C[sym] = None; return None
    d = pd.read_parquet(p)
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"]).dt.normalize()); d = d[~d.index.duplicated(keep="last")].sort_index()
    if "v" in d and d["v"].fillna(0).gt(0).mean() > 0.5: d = d[d["v"].fillna(0) > 0]
    d = d[(d["adj"] > 0) & (d["c"] > 0)]
    _C[sym] = d
    return d

_CAL = None
def bist_cal():
    global _CAL
    if _CAL is None:
        d = raw("XU100.IS"); _CAL = d.index[(d.index >= pd.Timestamp("2013-01-01")) & (d.index <= END)]
    return _CAL

def bist_decomp(code):
    """BIST hisse/endeks: cc (adj), gap (ham o/önceki c), intra (ham c/o). BIST takvimine reindex."""
    sym = code if code.endswith(".IS") else code + ".IS"
    d = raw(sym)
    if d is None: return None
    cal = bist_cal(); d = d[d.index.isin(cal)]
    cc = np.log(d["adj"]).diff(); intra = np.log(d["c"] / d["o"]); gap = np.log(d["o"] / d["c"].shift(1))
    ca = np.abs(np.log(d["adj"] / d["c"]).diff()) > 1e-4
    gap[ca] = np.nan
    bad_open = (d["o"] <= 0) | d["o"].isna() | ((d["h"] == d["l"]) & (d["o"] == d["c"].shift(1)))
    intra[bad_open] = np.nan; gap[bad_open] = np.nan
    badcc = (cc > LUP) | (cc < LDN)
    cc[badcc] = np.nan; intra[badcc] = np.nan; gap[badcc] = np.nan
    badg = (gap > LUP) | (gap < LDN); gap[badg] = np.nan; intra[badg] = np.nan
    bi = (intra > LUP) | (intra < LDN); intra[bi] = np.nan
    pre = d.index < START; intra[pre] = np.nan; gap[pre] = np.nan
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra}).reindex(cal)
    return out

def foreign_ret(sym):
    d = raw(sym)
    if d is None or len(d) < 300: return None
    r = np.log(d["adj"]).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1)
    r[((r.abs() > 12 * sd) & sd.notna()) | (r.abs() > 0.5)] = np.nan
    return r.dropna()

def to_bist_window(r, bkt):
    """Yerel seans getirilerini BIST günü penceresine topla."""
    cal = bist_cal()
    side = "right" if bkt == "post" else "left"
    pos = cal.searchsorted(r.index.values, side=side)
    ok = pos < len(cal)
    tgt = cal[pos[ok]]
    s = pd.Series(r.values[ok], index=tgt)
    w = s.groupby(level=0).sum(min_count=1)
    return w.reindex(cal)

def roll_beta(y, x, w=250, minp=120):
    """y, x: DataFrame/Series aynı index; geçmiş pencere beta (t günü için t-1'e kadar)."""
    cov = y.rolling(w, min_periods=minp).cov(x); var = x.rolling(w, min_periods=minp).var()
    return (cov / var).shift(1)

def zscore(x, w=250, minp=60, clip=4.0):
    mu = x.rolling(w, min_periods=minp).mean().shift(1); sd = x.rolling(w, min_periods=minp).std().shift(1)
    return ((x - mu) / sd).clip(-clip, clip)

# ---------------- istatistik ----------------
def nw_se_mean(u, L=5):
    u = np.asarray(u, float); u = u[~np.isnan(u)]; n = len(u)
    if n < 30: return np.nan, n
    e = u - u.mean(); g0 = e @ e / n; s = g0
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); s += 2 * w * (e[l:] @ e[:-l]) / n
    return np.sqrt(max(s, 0) / n), n

def ols_nw(y, x, L=5):
    """tek regresör + sabit; dönüş b, t_NW, n, corr."""
    m = ~(np.isnan(y) | np.isnan(x)); y = y[m]; x = x[m]; n = len(y)
    if n < 100: return np.nan, np.nan, n, np.nan
    xd = x - x.mean(); yd = y - y.mean(); sxx = xd @ xd
    b = (xd @ yd) / sxx; e = yd - b * xd
    h = xd * e; g = h @ h
    for l in range(1, L + 1):
        g += 2 * (1 - l / (L + 1)) * (h[l:] @ h[:-l])
    se = np.sqrt(g) / sxx
    c = (xd @ yd) / np.sqrt(sxx * (yd @ yd))
    return b, b / se, n, c

def corr_hc(y, x):
    """tarama ajanının tanımı: pairwise corr + HC0 (H0 altında) t."""
    m = ~(np.isnan(y) | np.isnan(x)); y = y[m]; x = x[m]; n = len(y)
    if n < 250: return np.nan, np.nan, n
    xd = x - x.mean(); yd = y - y.mean()
    c = (xd @ yd) / np.sqrt((xd @ xd) * (yd @ yd)); t = (xd @ yd) / np.sqrt(((xd ** 2) * (yd ** 2)).sum())
    return c, t, n

def pooled_dk(Y, Xs, L=5, fe=True):
    """Havuzlanmış panel OLS. Y: T x N DataFrame; Xs: liste T x N DataFrame (regresörler). Hisse sabit etkisi (fe) opsiyonel.
    SE: Driscoll–Kraay (tarih bazında skor toplamı, NW L gecikme) + tarih-kümelenmiş. Dönüş dict."""
    Yv = Y.values.astype(float); Xv = [X.reindex_like(Y).values.astype(float) for X in Xs]
    m = ~np.isnan(Yv)
    for X in Xv: m &= ~np.isnan(X)
    if fe:
        def dm(A):
            A = np.where(m, A, np.nan); mu = np.nanmean(A, 0); return np.where(m, A - mu, 0.0)
        Yd = dm(Yv); Xd = [dm(X) for X in Xv]
    else:
        Yd = np.where(m, Yv, 0.0); Xd = [np.where(m, X, 0.0) for X in Xv]
    k = len(Xd)
    XX = np.array([[np.sum(Xd[i] * Xd[j]) for j in range(k)] for i in range(k)])
    XY = np.array([np.sum(Xd[i] * Yd) for i in range(k)])
    b = np.linalg.solve(XX, XY)
    E = Yd - sum(b[i] * Xd[i] for i in range(k)); E = np.where(m, E, 0.0)
    H = np.column_stack([np.sum(Xd[i] * E, 1) for i in range(k)])  # T x k tarih skoru
    S = H.T @ H
    for l in range(1, L + 1):
        G = H[l:].T @ H[:-l]; S += (1 - l / (L + 1)) * (G + G.T)
    Sc = H.T @ H
    iXX = np.linalg.inv(XX)
    V = iXX @ S @ iXX; Vc = iXX @ Sc @ iXX
    return {"b": b, "t_dk": b / np.sqrt(np.diag(V)), "t_cl": b / np.sqrt(np.diag(Vc)), "nobs": int(m.sum()), "ndays": int(m.any(1).sum())}

def bh(p):
    p = np.asarray(p, float); ok = ~np.isnan(p); adj = np.full(len(p), np.nan)
    ps = p[ok]; mm = len(ps)
    if mm == 0: return adj
    o = np.argsort(ps); r = np.empty(mm); r[o] = np.arange(1, mm + 1)
    a = ps * mm / r; a_s = np.minimum.accumulate(a[o][::-1])[::-1]; aa = np.empty(mm); aa[o] = np.minimum(a_s, 1)
    adj[ok] = aa; return adj

def p2(t): return 2 * stats.norm.sf(np.abs(t))

def period_mask(idx, per):
    if per == "IS": return (idx >= START) & (idx <= IS_END)
    if per == "OOS": return (idx >= OOS_START) & (idx <= END)
    return (idx >= START) & (idx <= END)

def bt_stats(pnl, active, per_idx_mask=None):
    """pnl: günlük seri (pozisyon günlerinde dolu), active: pozisyon var mı. Dönüş: n, ort bps, NW-t, isabet, Sharpe (yıllık; tüm günler)."""
    p = pnl.copy(); a = active.copy()
    if per_idx_mask is not None: p = p[per_idx_mask]; a = a[per_idx_mask]
    pa = p[a]
    n = int(a.sum())
    if n < 20: return {"n": n}
    se, _ = nw_se_mean(pa.values)
    full = p.where(a, 0.0)
    vol = full.std() * np.sqrt(252)
    return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": pa.mean() / se if se > 0 else np.nan, "hit": float((pa > 0).mean()),
            "sharpe": (full.mean() * 252) / vol if vol > 0 else np.nan}
