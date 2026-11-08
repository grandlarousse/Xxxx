"""e2_etf_leadlag — ortak yardımcılar (Midas/ABD ETF cephesi, lead-lag).
Zaman kuralları (DATA_README.md + DATA_README_ETF.md):
  Giriş = gün t ABD kapanışı 16:00 ET (yaz 20:00 / kış 21:00 UTC); çıkış = t+h kapanışı (h NYSE günü).
  Karar anı (cutoff) = gün t 15:00 ET (cut_utc; yaz 19:00 / kış 20:00 UTC).
  c_<T>   : enstrümanın kendi yerel günü t kapanışı -> ABD ETF'lerinde GİRİŞ fiyatı, sinyalde YASAK (yalnız shift(1)).
  y_<T>   : cutoff'tan önce kapanmış son değer (ABD: t-1 kapanışı; Avrupa/Asya: t kapanışı). y_<T>_avail UTC.
  xau_cut : spot XAUUSD gün t 15:00 ET (Dukascopy BID, saatlik). xau_close (16:00 ET) YASAK (yalnız t-1).
  dk_*_cut: Dukascopy çapraz varlıklar gün t 15:00 ET.
  viop_*  : gün t VİOP uzlaşması (~15:05-15:15 UTC) < cutoff.
  shfe_AU0_c, xau_p07, dk_USDCNH_p07 : gün t 07:00 UTC.
  ust_*   : t-1 (D 22:00 UTC). cot_gold_* : Salı pozisyonu, Cuma 21:00 UTC (Cuma cutoff'undan SONRA -> Pazartesi'den itibaren).
IS = 2008..2017, OOS = 2018..2026-11 (lib_altin.IS_END ayarlanır). Ayrıca 2022+ alt dönem.
"""
import sys, os, json, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
import lib_altin
lib_altin.IS_END = pd.Timestamp("2017-12-31")
from lib_altin import fwd, ic, split_stats, nw_ols, backtest, register, placebo_lead, bh_fdr  # noqa
IS_END = lib_altin.IS_END
OUT = f"{S}/out/e2_etf_leadlag"
AGENT = "e2_etf_leadlag"
P = f"{S}/panel"
os.makedirs(OUT, exist_ok=True)

TARGETS = ["GLD", "GDX", "GDXJ", "SLV"]
INVERSE = {"GLD": "GLL", "GDX": "DUST", "GDXJ": "JDST", "SLV": "ZSL"}
COST = {"base": 10.0, "stress": 20.0}          # GLD/IAU/GLDM/GDX/GDXJ/SLV gidiş-dönüş bps
COST_LEV = {"base": 20.0, "stress": 40.0}      # kaldıraçlı / ters ETF
HS = (1, 3, 5)
EXTREMES = {"2008_GFC": ("2008-09-01", "2008-12-31"), "2013_Nisan": ("2013-04-01", "2013-06-30"),
            "2020_Mart": ("2020-02-20", "2020-04-30"), "2026_OcakSubat": ("2026-01-01", "2026-02-28")}


def load():
    d = pd.read_parquet(f"{P}/panel_etf.parquet"); d.index = pd.to_datetime(d.index)
    return d


def ret_of(d, t):
    """Gün t log getirisi (t-1 kapanış -> t kapanış), c_ sütunundan. GİRİŞ/HEDEF içindir."""
    c = d[f"c_{t}"].astype(float)
    r = np.log(c).diff()
    r[c.isna() | c.shift(1).isna()] = np.nan
    return r


def known_ret(d, t):
    """Gün t'de BİLİNEN son günlük getiri: ABD varlıkları için (t-2 -> t-1 kapanış) = ret_of(t).shift(1)."""
    return ret_of(d, t).shift(1)


def roll_beta(y, x, win=120, minp=60):
    """y ~ x yuvarlanan beta, yalnız geçmiş (t'ye kadar dahil; çağıran zaten bilinen seriler veriyor). Çok değişkenli için roll_beta2."""
    cov = y.rolling(win, min_periods=minp).cov(x); var = x.rolling(win, min_periods=minp).var()
    return cov / var


def roll_beta2(y, X, win=250, minp=120):
    """Çok değişkenli yuvarlanan OLS betaları (sabitli) — numpy ile, yalnız geçmiş pencere [i-win+1, i]."""
    Xv = X.values; yv = y.values; n, k = Xv.shape
    B = np.full((n, k), np.nan)
    for i in range(n):
        lo = max(0, i - win + 1)
        xx = Xv[lo:i + 1]; yy = yv[lo:i + 1]
        m = np.isfinite(yy) & np.all(np.isfinite(xx), axis=1)
        if m.sum() < minp: continue
        A = np.column_stack([np.ones(m.sum()), xx[m]])
        try:
            b = np.linalg.lstsq(A, yy[m], rcond=None)[0]; B[i] = b[1:]
        except Exception:
            pass
    return pd.DataFrame(B, index=X.index, columns=X.columns)


def zpast(x, win=250, minp=60):
    """Geçmiş-yalnız z-skoru: (x_t - mean_{t-win..t-1}) / std_{t-win..t-1}."""
    m = x.shift(1).rolling(win, min_periods=minp).mean(); s = x.shift(1).rolling(win, min_periods=minp).std()
    return (x - m) / s


def sub_ic(x, y, h, start=None, end=None, method="spearman"):
    xx = x.copy(); yy = y.copy()
    if start is not None: xx = xx[xx.index >= start]; yy = yy[yy.index >= start]
    if end is not None: xx = xx[xx.index <= end]; yy = yy[yy.index <= end]
    return ic(xx, yy, max(h, 5), method)


def test(family, test_id, x, target_ret, h, predictor, note="", reg=True, method="spearman"):
    """split_stats + 2022+ alt dönem + kayıt. Döndür: dict."""
    y = fwd(target_ret, h)
    st = split_stats(x, y, h, method)
    s22 = sub_ic(x, y, h, start="2022-01-01", method=method)
    st["ic_22"] = s22["ic"]; st["t_22"] = s22["t"]; st["n_22"] = s22["n"]
    if reg:
        register(AGENT, family, test_id, predictor, h, st, note)
    st.update(family=family, test_id=test_id, predictor=predictor, h=h)
    return st


def realized_lev(d, inv, und, h, start=None, end=None):
    """h günlük (örtüşmeyen) log getirilerde ters/kaldıraçlı ETF'nin dayanak ETF'ye regresyon betası."""
    ci = np.log(d[f"c_{inv}"]); cu = np.log(d[f"c_{und}"])
    if start: ci = ci[ci.index >= start]; cu = cu[cu.index >= start]
    if end: ci = ci[ci.index <= end]; cu = cu[cu.index <= end]
    ri = (ci.shift(-h) - ci).iloc[::h]; ru = (cu.shift(-h) - cu).iloc[::h]
    m = ri.notna() & ru.notna()
    if m.sum() < 30: return np.nan, np.nan, int(m.sum())
    b = np.polyfit(ru[m], ri[m], 1)[0]
    # basit getiri bazında ölçülen ortalama 'aşınma': ters ETF getirisi - L * dayanak getirisi (yıllık)
    return float(b), float(np.corrcoef(ru[m], ri[m])[0, 1]), int(m.sum())


def inv_weight(d, inv, und, win=60):
    """Ters ETF ağırlığı = 1/|beta| (geçmiş 60 günlük günlük getiri betası, yalnız t ve öncesi bilinen). -1x eşdeğeri maruziyet."""
    ri = ret_of(d, inv); ru = ret_of(d, und)
    b = roll_beta(ri, ru, win, 40).shift(1)   # t-1'e kadar bilinen
    w = (1.0 / b.abs()).clip(0.2, 1.0)
    return w


def strat(d, pos, und, h, cost_key="base", start=None, end=None):
    """Üç sürüm: (i) ideal ±1 dayanak (açığa satış varsayımsal), (ii) yalnız uzun (değilse nakit), (iii) uzun dayanak + kısa yön ters ETF (≈-1x).
    Ayrıca demeaned (drift çıkarılmış) ideal ve yalnız-uzun Sharpe. pos: gün t kapanışında alınan hedef pozisyon ∈[-1,1]."""
    r = ret_of(d, und); inv = INVERSE[und]; ri = ret_of(d, inv)
    msk = pd.Series(True, index=r.index)
    if start: msk &= r.index >= pd.Timestamp(start)
    if end: msk &= r.index <= pd.Timestamp(end)
    r = r[msk].dropna()
    pos = pos.reindex(r.index).fillna(0).clip(-1, 1)
    c = COST[cost_key]; cl = COST_LEV[cost_key]
    o = {}
    a = backtest(pos, r, h, c); o["ideal"] = a
    o["ideal_dm"] = backtest(pos, r, h, c, demean=True)
    pl = pos.clip(lower=0)
    o["long"] = backtest(pl, r, h, c); o["long_dm"] = backtest(pl, r, h, c, demean=True)
    ps = (-pos).clip(lower=0)
    o["short_ideal"] = backtest(-ps, r, h, c)
    # ters ETF bacağı
    w = inv_weight(d, inv, und).reindex(r.index)
    rinv = ri.reindex(r.index)
    ok = rinv.notna()
    psi = (ps * w).where(ok, 0.0).fillna(0)
    bi = backtest(psi, rinv.fillna(0), h, cl)
    o["short_inv"] = bi
    if bi is not None and o["long"] is not None:
        pnl = o["long"]["pnl"].add(bi["pnl"], fill_value=0)
        o["long_inv"] = dict(pnl=pnl, sharpe=float(pnl.mean() / pnl.std() * np.sqrt(252)) if pnl.std() > 0 else np.nan,
                             ann_ret=float(pnl.mean() * 252), ann_vol=float(pnl.std() * np.sqrt(252)))
    else:
        o["long_inv"] = None
    bh = backtest(pd.Series(1.0, index=r.index), r, 1, 0)
    o["bh"] = bh
    return o


def summ(o):
    def g(k, f="sharpe"):
        v = o.get(k); return None if v is None else round(float(v[f]), 3)
    return dict(sh_ideal=g("ideal"), sh_ideal_dm=g("ideal_dm"), sh_long=g("long"), sh_long_dm=g("long_dm"),
                sh_long_inv=g("long_inv"), sh_short_ideal=g("short_ideal"), sh_short_inv=g("short_inv"), sh_bh=g("bh"),
                ann_long=g("long", "ann_ret"), ann_long_inv=g("long_inv", "ann_ret"), ann_ideal=g("ideal", "ann_ret"), ann_bh=g("bh", "ann_ret"),
                expo_long=None if o.get("long") is None else round(o["long"]["exposure"], 3),
                turn_ideal=None if o.get("ideal") is None else round(o["ideal"]["turnover_per_yr"], 1))


def full_report(d, pos, und, h, label):
    """Tam/IS/OOS/2022+ ve maliyet temel+stres; yıllık getiriler; uç dönem getirileri."""
    rows = []
    for ck in ("base", "stress"):
        for nm, s, e in [("full", None, None), ("is", None, "2017-12-31"), ("oos", "2018-01-01", None), ("2022+", "2022-01-01", None)]:
            o = strat(d, pos, und, h, ck, s, e)
            if o["ideal"] is None: continue
            rr = summ(o); rr.update(label=label, und=und, h=h, cost=ck, period=nm); rows.append(rr)
    o = strat(d, pos, und, h, "base")
    yr = {}
    for k in ("ideal", "long", "long_inv", "bh"):
        if o.get(k) is None: continue
        p = o[k]["pnl"]; yr[k] = p.groupby(p.index.year).sum()
    yr = pd.DataFrame(yr)
    ext = {}
    for en, (a, b) in EXTREMES.items():
        e = {}
        for k in ("ideal", "long", "long_inv", "bh"):
            if o.get(k) is None: continue
            p = o[k]["pnl"]; p = p[(p.index >= a) & (p.index <= b)]
            e[k] = round(float(p.sum()) * 100, 2) if len(p) else np.nan
        ext[en] = e
    return pd.DataFrame(rows), yr, ext


def label_conf(st, mech=True, oos_sh_long=None, oos_sh_any=None, oos_bh=None, oos_long_dm=None):
    """Görev kuralı + drift koruması: YUKSEK için yalnız-uzun OOS net Sharpe>0,3 VE (yalnız-uzun OOS Sharpe > B&H OOS Sharpe ya da demeaned yalnız-uzun>0,2) VE ideal net OOS Sharpe>0,3."""
    t = st.get("t"); ti = st.get("t_is"); to = st.get("t_oos")
    ok_same = (np.sign(ti) == np.sign(t)) and (np.sign(to) == np.sign(t)) if all(np.isfinite([t, ti, to])) else False
    yrs = st.get("yrs") or 0; ys = st.get("yrs_same_sign") or 0
    drift_ok = (oos_bh is None or (oos_sh_long or 0) > oos_bh or (oos_long_dm or 0) > 0.2) and (oos_sh_any is None or oos_sh_any > 0.3)
    if mech and abs(t) >= 3 and ok_same and abs(to) >= 2 and yrs and ys / yrs >= 0.7 and (oos_sh_long or 0) > 0.3 and drift_ok:
        return "YUKSEK"
    if mech and abs(t) >= 2 and np.isfinite(to) and np.sign(to) == np.sign(t):
        return "ORTA"
    if abs(t) >= 1.5 or (np.isfinite(to) and abs(to) >= 1.5):
        return "DUSUK"
    return "YOK"


def pos_from_signal(x, sign, q=0.8, is_end="2017-12-31", mode="tail"):
    """IS kantilleriyle eşik: x > q-kantil -> +sign, x < (1-q)-kantil -> -sign, arada 0 (yalnız IS dağılımı)."""
    xi = x[x.index <= pd.Timestamp(is_end)].dropna()
    if len(xi) < 100:
        xi = x.dropna().iloc[:max(250, int(len(x.dropna()) * 0.3))]
    hi = xi.quantile(q); lo = xi.quantile(1 - q)
    p = pd.Series(0.0, index=x.index)
    p[x > hi] = sign; p[x < lo] = -sign
    p[x.isna()] = 0.0
    return p
