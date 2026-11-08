"""Çin altın hisseleri artığı, HSI getirisi — ham Yahoo dosyalarından, kendi takvimleriyle.
Kapanış anı (UTC): SSE (600547.SS, 000001.SS) 15:00 CST = 07:00 UTC; HKEX (1818.HK, 2899.HK, ^HSI) 16:00 HKT + 10 dk kapanış müzayedesi = 08:10 UTC.
Yahoo 'date' = yerel işlem günü, ts_utc = bar açılışı (01:30 UTC). DST yok (Çin/HK).
"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
from numpy.lib.stride_tricks import sliding_window_view

CLOSE_UTC = {"600547.SS": (7, 0), "000001.SS": (7, 0), "1818.HK": (8, 10), "2899.HK": (8, 10), "_HSI": (8, 10)}
GOLD_SNAP = {"600547.SS": (7, 0), "1818.HK": (8, 0), "2899.HK": (8, 0)}   # saatlik veride 08:10 yerine 08:00 (bar kapanışı)
STK = {"600547.SS": "000001.SS", "1818.HK": "_HSI", "2899.HK": "_HSI"}

def yh(tk):
    y = pd.read_parquet(f"{P}/yahoo/{tk}.parquet"); y.index = pd.to_datetime(y.index).normalize()
    y = y[~y.index.duplicated(keep="last")].sort_index()
    y = y[y.adjclose.notna() & (y.adjclose > 0)]
    # Yahoo bazen hacimsiz tekrar satırı koyar: kapanış önceki günle aynı ve hacim 0 -> işlem yok say
    return y

def daily_ret(tk):
    y = yh(tk); r = np.log(y.adjclose).diff()
    return r, y

def rolling_resid(y, X, win=250, minn=150):
    """y_d - Xb_{d-1}: b, d-1'e kadarki son 'win' gözlemden OLS (yalnız geçmiş)."""
    n = len(y); k = X.shape[1]; res = np.full(n, np.nan)
    for i in range(n):
        lo = max(0, i - win)
        if i - lo < minn: continue
        Xi = X[lo:i]; yi = y[lo:i]
        b = np.linalg.lstsq(Xi, yi, rcond=None)[0]
        res[i] = y[i] - X[i] @ b
    return res

def stock_resid(tk, win=250, use_mkt=True, minn=None):
    minn = minn or int(win * 0.6)
    r, y = daily_ret(tk); rm, _ = daily_ret(STK[tk])
    hh, mm = GOLD_SNAP[tk]
    t_close = y.index + pd.Timedelta(hours=hh, minutes=mm)
    g = pd.Series(gold_at(t_close), index=y.index)
    rg = np.log(g / g.shift(1))                     # önceki hisse kapanışı -> bu kapanış (aynı pencere)
    d = pd.concat([r.rename("y"), rg.rename("g"), rm.reindex(y.index).rename("m")], axis=1)
    cols = ["g", "m"] if use_mkt else ["g"]
    dd = d.dropna(subset=["y"] + cols)
    X = np.column_stack([np.ones(len(dd))] + [dd[c].values for c in cols])
    e = rolling_resid(dd.y.values, X, win, minn)
    return pd.Series(e, index=dd.index), d

def to_viop(s, days):
    """Hisse günü d -> VİOP günü t=d (kapanış 07:00/08:10 UTC < 15:00 UTC). Hisse t'de işlem görmediyse NaN."""
    return s.reindex(days)

if __name__ == "__main__":
    T = viop_target(); days = T.index
    # --- 1) Ham zaman damgası kontrolü
    for tk in CLOSE_UTC:
        y = yh(tk)
        ts = pd.to_datetime(y.ts_utc).dt.tz_convert("UTC")
        loc_date = ts.dt.tz_convert("Asia/Shanghai" if tk.endswith("SS") else "Asia/Hong_Kong").dt.normalize().dt.tz_localize(None)
        print(tk, "ts_utc saatleri:", ts.dt.strftime("%H:%M").value_counts().head(3).to_dict(), "| yerel tarih=index:", float((loc_date.values == y.index.values).mean()))
    # --- 2) tarih hizası: hisse getirisi ile altın pencere getirisi korelasyonu, kaydırmalı
    rows = []
    for tk in GOLD_SNAP:
        r, y = daily_ret(tk); hh, mm = GOLD_SNAP[tk]
        G = pd.Series(gold_at(y.index + pd.Timedelta(hours=hh, minutes=mm)), index=y.index); rg = np.log(G / G.shift(1))
        for k in (-2, -1, 0, 1, 2):
            rows.append(dict(tk=tk, gold_shift=k, corr=round(r.corr(rg.shift(k)), 3)))
    al = pd.DataFrame(rows).pivot(index="tk", columns="gold_shift", values="corr"); print("hisse r_d vs altın penceresi (shift k: k>0 = altının ESKİ penceresi)\n", al)
    al.to_csv(f"{OUT}/r1_alignment.csv")
    # altın 07->15 UTC aynı gün (hisse kapanışı SONRASI) ile korelasyon: hisse kapanışı geç mi damgalanmış?
    for tk in GOLD_SNAP:
        r, y = daily_ret(tk)
        a = pd.Series(gold_at(y.index + pd.Timedelta(hours=8, minutes=0)), index=y.index); b = pd.Series(gold_at(y.index + pd.Timedelta(hours=15)), index=y.index)
        c0 = pd.Series(gold_at(y.index + pd.Timedelta(hours=GOLD_SNAP[tk][0])), index=y.index)
        print(tk, "corr(r_hisse, altın kapanış->15:00 aynı gün)=", round(r.corr(np.log(b / c0)), 3))

    F = pd.DataFrame(index=days)
    for tk in STK:
        e, d = stock_resid(tk)
        F[f"res_{tk}"] = to_viop(e, days)
        F[f"r_{tk}"] = to_viop(d.y, days)
    rH, _ = daily_ret("_HSI"); F["r_HSI"] = to_viop(rH, days)
    R3 = F[[f"res_{tk}" for tk in STK]]
    F["comp"] = R3.mean(axis=1).where(R3.notna().sum(axis=1) >= 2)
    F["comp_sum5"] = F["comp"].rolling(5, min_periods=3).sum()
    F.to_parquet(f"{OUT}/r1_features_viop.parquet")
    print(F.describe().T[["count", "mean", "std"]])
