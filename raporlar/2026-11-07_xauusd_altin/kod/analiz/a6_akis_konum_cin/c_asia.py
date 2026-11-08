"""(c) Asya (gün t'de kapanmış) -> VİOP fwd{h}.
Bilgi zamanları (UTC, gün t): Nikkei ^N225 06:30 (Kasım 2024 öncesi 06:00), KOSPI ^KS11 06:30, ASX ^AXJO ~05:10/06:10, Şanghay 000001.SS ve 600547.SS 07:00,
Hong Kong ^HSI, 1818.HK, 2899.HK 08:10. Hepsi 15:00 UTC cutoff'tan önce (panel y_*_avail ile doğrulanır).
Getiri = gün t'de bilinen son kapanışın bir önceki günün bilinen kapanışına log farkı; kapanış değişmediyse (Asya tatili) NaN.
Çin altın hisseleri için artık getiri: r_hisse − b1·r_altın(aynı pencere) − b2·r_yerel_endeks, 250g kayan OLS (yalnız geçmiş veri).
Spot altının Asya seansı getirisi log(xau_p07/xau_p00) de bu aileye eklendi (00:00-07:00 UTC, gün t).
"""
from common import *
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

def ret_known(P, tk):
    y = P[f"y_{tk}"]; a = pd.to_datetime(P[f"y_{tk}_avail"])
    r = np.log(y).diff()
    r[a == a.shift(1)] = np.nan                      # yeni kapanış yok
    return r

def check_avail(P, tk):
    a = pd.to_datetime(P[f"y_{tk}_avail"]); cut = P.index + pd.Timedelta(hours=15)
    a = a.dt.tz_localize(None) if getattr(a.dt, "tz", None) is not None else a
    lag_h = (cut - a) / pd.Timedelta(hours=1)
    return dict(tk=tk, min_lag_h=float(lag_h.min()), med_lag_h=float(lag_h.median()), same_day=float((a.dt.normalize() == P.index).mean()))

_XH = None
def gold_at(times):
    """Spot XAUUSD (Dukascopy saatlik bar kapanışı) verilen UTC anlarında (<= an olan son bar kapanışı, en fazla 3 saat bayat)."""
    global _XH
    if _XH is None:
        h = hourly("XAUUSD"); s_ = h["c"].copy(); s_.index = pd.DatetimeIndex(h.index).tz_convert("UTC").tz_localize(None) + pd.Timedelta(hours=1)
        pv = D["xau_p07"].dropna(); pv.index = pv.index + pd.Timedelta(hours=7)        # Ekim-Kasım 2026 yaması
        _XH = pd.concat([s_, pv[~pv.index.isin(s_.index)]]).sort_index()
    t = pd.DatetimeIndex(times)
    ok = ~t.isna()
    out = np.full(len(t), np.nan)
    idx = _XH.index.searchsorted(t[ok], side="right") - 1
    v = _XH.values[np.clip(idx, 0, None)]; ts = _XH.index[np.clip(idx, 0, None)]
    stale = (t[ok] - ts) / pd.Timedelta(hours=1)
    out[ok] = np.where((idx >= 0) & (stale <= 3), v, np.nan)
    return pd.Series(out, index=times.index if hasattr(times, "index") else None)

def gold_window_ret(P, tk):
    """Hisse getirisinin kapsadığı pencereyle (önceki bilinen kapanış anı -> bu kapanış anı) aynı pencerede spot altın getirisi."""
    a = pd.to_datetime(P[f"y_{tk}_avail"])
    a = a.dt.tz_localize(None) if getattr(a.dt, "tz", None) is not None else a
    a = a.dt.floor("h")                                  # 08:10 -> 08:00
    g1 = gold_at(a); g0 = gold_at(a.shift(1))
    r = np.log(g1.values / g0.values)
    r = pd.Series(r, index=P.index); r[a == a.shift(1)] = np.nan
    return r

IDX = ["_N225", "_HSI", "000001_SS", "_KS11", "_AXJO"]
STK = {"600547_SS": ("000001_SS", 7), "1818_HK": ("_HSI", 8), "2899_HK": ("_HSI", 8)}

def build(P):
    F = pd.DataFrame(index=P.index)
    for tk in IDX:
        F[f"r{tk}"] = ret_known(P, tk)
    zs = pd.concat([F[f"r{tk}"] / F[f"r{tk}"].rolling(250, min_periods=120).std().shift(1) for tk in IDX], axis=1)
    F["asia_comp"] = zs.mean(axis=1, skipna=True).where(zs.notna().sum(axis=1) >= 3)
    for tk, (mk, hh) in STK.items():
        rs = ret_known(P, tk); rm = ret_known(P, mk)
        g = gold_window_ret(P, tk)
        F[f"r{tk}"] = rs
        dd = pd.concat([rs.rename("y"), g.rename("g"), rm.rename("m")], axis=1)
        ok = dd.notna().all(axis=1)
        m = RollingOLS(dd.y[ok], sm.add_constant(dd[["g", "m"]][ok]), window=250, min_nobs=150).fit()
        b = m.params.shift(1)                          # yalnız t-1'e kadar tahmin edilen beta
        res = dd.y[ok] - b["const"] - b["g"] * dd.g[ok] - b["m"] * dd.m[ok]
        F[f"res{tk}"] = res.reindex(P.index)
    F["cn_gold_res_comp"] = F[[f"res{tk}" for tk in STK]].mean(axis=1, skipna=True).where(F[[f"res{tk}" for tk in STK]].notna().sum(axis=1) >= 2)
    F["xau_asia_sess"] = np.log(P["xau_p07"] / P["xau_p00"])
    return F

av = pd.DataFrame([check_avail(D, tk) for tk in IDX + list(STK)]); print(av.round(2).to_string(index=False)); av.to_csv(f"{OUT}/c_avail_check.csv", index=False)
X = build(D)
DESC = {"r_N225": "Nikkei günlük getiri (t, 06:30 UTC)", "r_HSI": "Hang Seng getiri (t, 08:10 UTC)", "r000001_SS": "Şanghay Bileşik getiri (t, 07:00 UTC)",
        "r_KS11": "KOSPI getiri (t)", "r_AXJO": "ASX200 getiri (t)", "asia_comp": "Asya endeks bileşik (vol-ölçekli ort.)",
        "r600547_SS": "Shandong Gold 600547.SS ham getiri", "r1818_HK": "Zhaojin 1818.HK ham getiri", "r2899_HK": "Zijin 2899.HK ham getiri",
        "res600547_SS": "600547.SS artık getiri (altın+endeks betası çıkarılmış)", "res1818_HK": "1818.HK artık getiri", "res2899_HK": "2899.HK artık getiri",
        "cn_gold_res_comp": "Çin altın hisseleri artık bileşik", "xau_asia_sess": "Spot altın Asya seansı getirisi 00→07 UTC (t)"}
rows = []
for k, d in DESC.items():
    rows += T(X[k], "asia", f"asia_{k}", d, note="Asya kapanışı gün t < 09:00 UTC")
df = save(rows, "c_asia_ic"); show(df)

Xs = build(SP)
rows3 = []
for k, d in DESC.items():
    rows3 += T_early(Xs[k], "asia", f"asia_{k}", d)
df3 = save(rows3, "c_asia_early"); show(df3, ("test_id", "h", "n", "ic", "t", "yrs_same"))
X.to_csv(f"{OUT}/c_asia_features.csv")
