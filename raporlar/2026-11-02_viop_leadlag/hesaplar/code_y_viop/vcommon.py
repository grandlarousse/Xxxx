"""Ortak yardımcılar (viop ajanı). ll.py'yi değiştirmez; sadece import eder."""
import sys, os, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, S + "/code"); import ll
OUT = S + "/out"; CODE = OUT + "/code_y_viop"; RES = CODE + "/results"; os.makedirs(RES, exist_ok=True)
STOCKS = ll.VIOP if hasattr(ll, "VIOP") else []
IDX = ["XU030", "XLBNK", "X10XB", "XSD25"]
FXM = ["USDTRY", "XAUTRY"]
ALL = STOCKS + IDX + FXM
TV = {**{s: f"BIST:{s}1!" for s in STOCKS}, "XU030": "BIST:XU030D1!", "XLBNK": "BIST:XLBNKD1!", "X10XB": "BIST:X10XBD1!",
      "XSD25": "BIST:XSD25D1!", "USDTRY": "BIST:USDTRY1!", "XAUTRY": "BIST:XAUTRY1!"}
SPOT = {**{s: s + ".IS" for s in STOCKS}, "XU030": "XU030.IS", "XLBNK": "XLBNK.IS", "X10XB": "X10XB.IS", "XSD25": "XSD25.IS",
        "USDTRY": "TRY=X", "XAUTRY": None}

def tick(und, px, date):
    """Minimum fiyat adımı (Borsa İstanbul, 02.12.2024 sonrası bantlı; öncesi pay 0,01, endeks 0,25 (2020-07 sonrası),
    USDTRY 0,0001, gram altın 0,01). Kaynak: Halk Yatırım genelgesi 29.11.2024 (BIST duyurusuna atıf)."""
    new = pd.Timestamp(date) >= pd.Timestamp("2024-12-02")
    if und in IDX: return 1.0 if new else 0.25
    if und == "USDTRY": return 0.001 if new else 0.0001
    if und == "XAUTRY": return 0.10 if new else 0.01
    if not new: return 0.01
    return 0.01 if px < 100 else 0.05 if px < 500 else 0.1 if px < 1000 else 0.25 if px < 2500 else 0.5

def load_panel():
    F = pd.read_parquet(S + "/data/viop_panel.parquet")
    for c in ["code", "und", "root"]: F[c] = F[c].astype(str)
    return F

def spot_daily(und):
    sym = SPOT.get(und)
    if sym is None: return None
    d = ll.raw(sym).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    return d

def nw(y, x=None, lags=5):
    return ll.nw_t(y, x, lags)

def spot_decomp(und):
    """Spot cc/gap/intra: hisselerde ll.decomp; endekslerde tam takvimli Yahoo serisinden (bülten günlerine değil)."""
    sym = SPOT.get(und)
    if sym is None: return None
    if und in STOCKS: return ll.decomp(sym)
    d = spot_daily(und)
    d = d[d["c"] > 0]
    cc = np.log(d["adj"]).diff(); intra = np.log(d["c"] / d["o"]); gap = cc - intra
    out = pd.DataFrame({"cc": cc, "gap": gap, "intra": intra})
    out.loc[out["cc"].abs() > 0.15, :] = np.nan
    out.loc[out.index < pd.Timestamp("2014-01-01"), ["gap", "intra"]] = np.nan
    return out

def fama_macbeth(P, sig, y, ctrls=(), min_n=10, periods=(("ALL", "2000", "2100"), ("IS", "2000", "2022-12-31"), ("OOS", "2023-01-01", "2100")), return_series=False):
    """Her gün kesit OLS: (y - kesit ort.) ~ z(sig) + z(ctrls). Eğim (bps / 1 kesit sd) zaman serisi NW t. (vektörize)"""
    cols = [sig] + [c for c in ctrls if c != sig]
    d = P[["date", "und", y] + cols].replace([np.inf, -np.inf], np.nan).dropna().sort_values("date")
    out = []
    if d.empty: return (out, None) if return_series else out
    g = d.groupby("date")
    cnt = g[y].transform("count")
    d = d[cnt >= max(min_n, len(cols) + 3)]
    g = d.groupby("date")
    for c in cols:  # kesit sıra-normalizasyonu (uç değerlere dayanıklı): (pct_rank - 0.5) * sqrt(12) ~ birim varyans
        d[c] = (g[c].rank(pct=True) - 0.5) * np.sqrt(12)
    d["yd"] = d[y] - g[y].transform("mean")
    d = d.dropna()
    dates = d["date"].values; X = d[cols].values; Y = d["yd"].values
    idx = np.flatnonzero(np.r_[True, dates[1:] != dates[:-1], True])
    sl = []
    for i in range(len(idx) - 1):
        a, b = idx[i], idx[i + 1]
        Xi = np.column_stack([np.ones(b - a), X[a:b]])
        try: sl.append((dates[a], np.linalg.lstsq(Xi, Y[a:b], rcond=None)[0][1]))
        except Exception: pass
    sl = pd.Series([v for _, v in sl], index=pd.DatetimeIndex([k for k, _ in sl]))
    for per, a, b in periods:
        ss = sl[(sl.index >= a) & (sl.index <= b)]
        if len(ss) < 60: continue
        mu, t, n = ll.nw_t(ss, None, 5)
        out.append(dict(sig=sig, tgt=y, per=per, bps_per_sd=1e4 * mu, t=t, n_days=n, n_und=d["und"].nunique(), ctrls="+".join(ctrls)))
    return (out, sl) if return_series else out
