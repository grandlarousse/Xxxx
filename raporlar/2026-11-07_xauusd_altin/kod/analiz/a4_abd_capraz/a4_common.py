"""a4_abd_capraz ortak yardımcılar: öngörücü üretimi, olay (büyük hareket) testleri, kısmi regresyon, saatlik pencere fiyatları.
Bilgi zamanı kuralları:
  y_<T>          : Yahoo son bilinen kapanış; zaman damgası y_<T>_avail (UTC). Panel kurucusu as-of hizaladı; avail < t 15:00 UTC kontrolü check_avail().
  ust_*          : ABD Hazinesi par getirisi, gün D değeri D 22:00 UTC → gün t'de son değer t-1 (ya da daha eski).
  xau_p15        : spot XAUUSD gün t 15:00 UTC (cutoff anı; dahil).
  dk_<SYM>_p15   : Dukascopy gün t 15:00 UTC.
  duka saatlik   : index = bar başlangıcı; fiyat anı = index + 1 saat → px_at(sym, H) = H:00 UTC fiyatı = (H-1):00 başlayan barın kapanışı.
"""
import sys, os, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *  # noqa
OUT = f"{S}/out/a4_abd_capraz"
AGENT = "a4_abd_capraz"
os.makedirs(OUT, exist_ok=True)

# ---- öngörücü evreni (görev metni) ----
PRICE_TICKERS = {
    # dolar
    "y_DX_Y_NYB": "dolar", "y_UUP": "dolar",
    # hisse / risk
    "y__GSPC": "hisse", "y_ES_F": "hisse", "y__NDX": "hisse", "y_HYG": "kredi", "y_EEM": "gelisen", "y_FXI": "gelisen", "y_TUR": "gelisen",
    # oynaklık (log değişim)
    "y__VIX": "oynaklik", "y__GVZ": "oynaklik", "y__MOVE": "oynaklik",
    # emtia
    "y_BZ_F": "petrol", "y_CL_F": "petrol", "y_HG_F": "bakir", "y_SI_F": "metal", "y_PL_F": "metal", "y_PA_F": "metal",
    # madenciler (y_GOLD hariç: Yahoo 'GOLD' 2025'te Barrick'ten başka şirkete geçti; Barrick tarihi y_B'de)
    "y_GDX": "madenci", "y_GDXJ": "madenci", "y_NEM": "madenci", "y_AEM": "madenci", "y_B": "madenci", "y_FNV": "madenci",
    "y_WPM": "madenci", "y_KGC": "madenci", "y_RGLD": "madenci", "y_SIL": "madenci", "y_RING": "madenci",
    # altın ETF ve tahvil
    "y_GLD": "altin_etf", "y_TLT": "tahvil", "y_TIP": "tahvil",
    # kripto
    "y_BTC_USD": "kripto",
    # referans: altının kendi ABD kapanışı (öz-gecikme kıyası)
    "y_GC_F": "oz_altin",
}
RATE_SERIES = {"ust_nom10": "faiz", "ust_real10": "faiz", "ust_be10": "faiz", "ust_nom2": "faiz", "curve_10_2": "faiz", "y__TNX": "faiz"}


def check_avail(d, col, cutoff_hour=15):
    """y_<T>_avail'in gün t 15:00 UTC'den önce olduğunu doğrula. Döndür: ihlal sayısı, medyan gecikme (saat)."""
    a = pd.to_datetime(d[col + "_avail"])
    cut = d.index + pd.Timedelta(hours=cutoff_hour)
    viol = int((a >= cut).sum())
    lag_h = ((cut - a).dt.total_seconds() / 3600).median()
    return viol, float(lag_h)


def zscale(r, win=120, minp=60):
    """Geçmiş-yalnız oynaklıkla ölçek: r_t / std(r_{t-win..t-1})."""
    sd = r.rolling(win, min_periods=minp).std().shift(1)
    return r / sd


def build_changes(d):
    """Her öngörücü için 1 ve 5 günlük değişim (fiyat: log; faiz: seviye farkı, yüzde puanı)."""
    out = {}
    for c in PRICE_TICKERS:
        if c not in d: continue
        lx = np.log(d[c].where(d[c] > 0))
        out[(c, 1)] = lx.diff(); out[(c, 5)] = lx.diff(5)
    dd = d.copy(); dd["curve_10_2"] = dd["ust_nom10"] - dd["ust_nom2"]
    for c in RATE_SERIES:
        x = dd[c]
        out[(c, 1)] = x.diff(); out[(c, 5)] = x.diff(5)
    return out


def gold_controls(d):
    """Altının kendi geçmiş getirileri (kısmi regresyon kontrolü): 15:00→15:00 UTC spot 1 ve 5 gün (gün t 15:00'te bilinir)."""
    lp = np.log(d["xau_p15"])
    return pd.DataFrame({"g1": lp.diff(), "g5": lp.diff(5)}, index=d.index)


def partial_t(y, x, ctrl, h, msk=None):
    """y ~ x + kontroller, NW lag=max(h,5). x'in t'si (z ölçekli x ve y ile)."""
    X = pd.concat([x.rename("x"), ctrl], axis=1)
    if msk is not None:
        X = X[msk]; y = y[msk]
    dd = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(dd) < 100: return np.nan
    z = (dd - dd.mean()) / dd.std()
    r = nw_ols(z["y"], z[["x"] + list(ctrl.columns)], lags=max(h, 5))
    return r["t"]


def partial_stats(x, y, ctrl, h):
    t_full = partial_t(y, x, ctrl, h)
    t_is = partial_t(y, x, ctrl, h, msk=(x.index <= IS_END))
    t_oos = partial_t(y, x, ctrl, h, msk=(x.index > IS_END))
    n = int(pd.concat([x, y, ctrl], axis=1).dropna().shape[0])
    return dict(ic=np.nan, t=t_full, t_is=t_is, t_oos=t_oos, n=n)


def event_stats(dummy, y, h):
    """Olay kuklası (0/1) sonrası y'nin olay dışı günlere göre farkı; NW t. Döndür register uyumlu dict (ic = ortalama fark, bps)."""
    def one(m):
        dd = pd.concat([dummy[m].rename("x"), y[m].rename("y")], axis=1).dropna()
        if dd.x.sum() < 8 or len(dd) < 100: return np.nan, np.nan, int(dd.x.sum()) if len(dd) else 0
        r = nw_ols(dd.y, dd.x, lags=max(h, 5))
        return r["b"] * 1e4, r["t"], int(dd.x.sum())
    allm = pd.Series(True, index=y.index)
    b, t, ne = one(allm)
    b_is, t_is, ne_is = one(y.index <= IS_END)
    b_oos, t_oos, ne_oos = one(y.index > IS_END)
    dd = pd.concat([dummy.rename("x"), y.rename("y")], axis=1).dropna()
    yr = dd.groupby(dd.index.year).apply(lambda g: (g.y[g.x == 1].mean() - g.y[g.x == 0].mean()) if g.x.sum() >= 3 else np.nan)
    sgn = np.sign(b)
    return dict(ic=b, t=t, n=ne, t_is=t_is, t_oos=t_oos, ic_oos=b_oos, ic_is=b_is, n_is=ne_is, n_oos=ne_oos,
                yrs_same_sign=int((np.sign(yr) == sgn).sum()), yrs=int(yr.notna().sum()), by_year=yr.mul(1e4).round(1).to_dict())


# ---- Dukascopy saatlik fiyatlar ----
_HCACHE = {}

def px_at(sym, hour):
    """Gün D'nin hour:00 UTC fiyatı (Series, index = takvim günü). Bar başlangıcı hour-1 olan barın kapanışı."""
    if sym not in _HCACHE:
        h = hourly(sym).copy()
        idx = pd.to_datetime(h.index)
        if idx.tz is not None: idx = idx.tz_convert("UTC").tz_localize(None)
        h.index = idx + pd.Timedelta(hours=1)  # fiyat anı
        _HCACHE[sym] = h["c"]
    c = _HCACHE[sym]
    sel = c[c.index.hour == hour]
    # tam saat damgası olmalı
    sel = sel[sel.index.minute == 0]
    s = pd.Series(sel.values, index=sel.index.normalize())
    return s[~s.index.duplicated(keep="last")]


def yearly_sign_table(x, y, method="spearman"):
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    return dd.groupby(dd.index.year).apply(lambda g: g.x.corr(g.y, method=method) if len(g) > 20 else np.nan)


def legs_bt(pos, ret, h, cost=COST_BPS):
    """Uzun / kısa bacak ve toplam: tam, IS, OOS net Sharpe + demeaned."""
    res = {}
    for nm, p in [("ls", pos), ("long", pos.clip(lower=0)), ("short", pos.clip(upper=0))]:
        res[nm] = bt_summary(p, ret, h, cost)
    return res


def reg_reset(prefix):
    """Betik yeniden çalıştırılınca kayıt yinelenmesin: bu betiğin (test_id öneki) eski satırlarını sil."""
    import lib_altin
    f = f"{lib_altin.REG_DIR}/{AGENT}.csv"
    if os.path.exists(f):
        r = pd.read_csv(f)
        r = r[~r.test_id.astype(str).str.startswith(prefix)]
        if len(r): r.to_csv(f, index=False)
        else: os.remove(f)


def reg(family, test_id, predictor, h, stats, note=""):
    st = {k: (float(v) if isinstance(v, (np.floating, float, int, np.integer)) and v is not None else v) for k, v in stats.items() if k != "by_year"}
    return register(AGENT, family, test_id, predictor, h, st, note)
