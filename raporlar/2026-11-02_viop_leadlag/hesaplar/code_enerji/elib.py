"""ENERJİ ajanı yardımcı kütüphanesi (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
Zamanlama: ll.py konvansiyonu. Sürücü r_d(t) = (t_önceki BIST günü, t] aralığındaki son kapanışlar arası getiri.
"""
import sys, os, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ll
OUT = SCR + "/out/code_enerji"
RES = OUT + "/res"
os.makedirs(RES, exist_ok=True)

_P = None; _D = None
def panel():
    global _P
    if _P is None: _P = pd.read_parquet(SCR + "/data/panel_ret_bistcal.parquet")
    return _P
def dpanel():
    global _D
    if _D is None: _D = pd.read_parquet(SCR + "/data/panel_decomp_bist.parquet")
    return _D

def R(sym):
    """BIST takviminde log getiri (panelden; yoksa ll.ret)."""
    P = panel(); s = ll.T(sym)
    if s in P: return P[s].copy()
    return ll.ret(s)

def DEC(stock):
    D = dpanel(); s = stock.replace(".IS", "")
    if s in D.columns.get_level_values(0): return D[s].copy()
    return ll.decomp(stock)

# ---------------- türetilmiş sürücüler -----------------
def px(sym): return ll.daily(sym)  # BIST takvimine ffill'li fiyat

def cracks():
    """$/bbl crack seviyeleri (BIST takviminde, son bilinen kapanış). HO/RB $/gal *42."""
    bz = px("BZ=F"); ho = px("HO=F") * 42; rb = px("RB=F") * 42; cl = px("CL=F")
    df = pd.concat([bz.rename("BZ"), ho.rename("HO"), rb.rename("RB"), cl.rename("CL")], axis=1).dropna()
    df["ho_crack"] = df.HO - df.BZ
    df["rb_crack"] = df.RB - df.BZ
    df["c321"] = (2 * df.RB + df.HO - 3 * df.BZ) / 3
    return df

def crack_ret():
    """Crack 'getirileri': (a) Δcrack / Brent_{t-1} (marjın ham petrole oranı değişimi), (b) log oran farkı r_HO - r_BZ.
    Vadeli roll sıçramalarına karşı %0,5/%99,5 winsorize."""
    df = cracks(); out = pd.DataFrame(index=df.index)
    for c in ["ho_crack", "rb_crack", "c321"]:
        out["d_" + c] = df[c].diff() / df.BZ.shift(1)
    out["hoxbz"] = np.log(df.HO).diff() - np.log(df.BZ).diff()
    out["rbxbz"] = np.log(df.RB).diff() - np.log(df.BZ).diff()
    out[(df.BZ.diff() == 0) & (df.HO.diff() == 0)] = np.nan  # her iki seri de bayat (tatil ffill)
    for c in out:
        lo, hi = out[c].quantile([0.005, 0.995]); out[c] = out[c].clip(lo, hi)
    return out

def ptf_daily():
    p = OUT + "/ptf_daily.parquet"
    return pd.read_parquet(p) if os.path.exists(p) else None

# ---------------- istatistik -----------------
def _c(a, b):
    df = pd.concat([a, b], axis=1).dropna()
    return (df.iloc[:, 0].corr(df.iloc[:, 1]), len(df)) if len(df) > 30 else (np.nan, len(df))

def wk(r):
    """Haftalık (Cuma) log getiri toplamı; eşzamansız kapanış etkisini büyük ölçüde giderir."""
    x = r.dropna(); return x.resample("W-FRI").sum(min_count=2)

def summary(stock, drv, name=None, start="2010-01-01", usd=False, lag_asia0=False):
    """Bir hisse-sürücü çifti için standart metrikler. drv: getiri serisi (BIST takvimi).
    lag_asia0=True: sürücü BIST açılışından önce kapanıyor (Kore/Japonya/Tayvan) -> lag0 da 'öncü' sayılır."""
    a = R(stock) if not usd else (R(stock) - R("TRY=X"))
    a = a[a.index >= start]; b = drv[drv.index >= start]
    m = R("XU100"); dd = DEC(stock); last = a.dropna().index.max()
    o = {"stock": stock.replace(".IS", ""), "driver_yahoo": name or getattr(drv, "name", "?")}
    o["corr_full"], o["n"] = _c(a, b)
    o["corr_3y"], _ = _c(a[a.index >= last - pd.DateOffset(years=3)], b)
    o["corr_1y"], _ = _c(a[a.index >= last - pd.DateOffset(years=1)], b)
    o["pcorr_xu100"], _ = ll.partial_corr(a, b, [m])
    # lag1 sürücünün kısmi etkisi (lag0 da kontrol) ~ eşzamansızlık düzeltmeli toplam: corr0+corr1
    c1, _ = _c(a, b.shift(1)); o["corr_lag1"] = c1
    o["corr_w"], o["n_w"] = _c(wk(a), wk(b))
    o["pcorr_w_xu100"], _ = ll.partial_corr(wk(a), wk(b), [wk(m)])
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    bb, tt, _ = ll.nw_t(df.a, df.b); o["beta"] = bb; o["t_sync"] = tt
    # gap / intra lag1 (ve Asya için lag0)
    for col in ["gap", "intra"]:
        for k in ([0, 1] if lag_asia0 else [1]):
            x = pd.concat([dd[col], b.shift(k).rename("b")], axis=1).dropna()
            x = x[x.index >= "2014-01-01"]
            if len(x) > 60:
                z = lambda s: (s - s.mean()) / s.std()
                be, t, n = ll.nw_t(z(x[col]), z(x["b"]))
                o[f"{col}_lag{k}_corr"] = be; o[f"{col}_lag{k}_t"] = t
    # ters yön: hisse_{t-1} -> sürücü_t
    cr, _ = _c(b, a.shift(1)); o["reverse_corr"] = cr
    # stabilite: yıllık senkron korelasyon işaret tutarlılığı, IS/OOS
    yc = ll.by_year_corr(a, b)
    s0 = np.sign(o["corr_full"]); o["yr_same_sign"] = float((np.sign(yc.dropna()) == s0).mean()) if len(yc.dropna()) else np.nan
    o["n_years"] = int(yc.notna().sum())
    o["is_corr"], _ = _c(a[(a.index >= "2014-01-01") & (a.index < "2021-01-01")], b)
    o["oos_corr"], _ = _c(a[a.index >= "2021-01-01"], b)
    o["pc_is"], _ = ll.partial_corr(a[(a.index >= "2014-01-01") & (a.index < "2021-01-01")], b, [m])
    o["pc_oos"], _ = ll.partial_corr(a[a.index >= "2021-01-01"], b, [m])
    return o

def lead_stats(target, sig, start="2014-01-01", split="2021-01-01"):
    """corr(target_t, sig_t) (sig zaten hizalanmış!) tam/IS/OOS + NW t."""
    x = pd.concat([target.rename("y"), sig.rename("s")], axis=1).dropna(); x = x[x.index >= start]
    z = lambda s: (s - s.mean()) / s.std()
    out = {}
    for lab, xx in [("all", x), ("is", x[x.index < split]), ("oos", x[x.index >= split])]:
        if len(xx) < 40: out[lab] = (np.nan, np.nan, len(xx)); continue
        b, t, n = ll.nw_t(z(xx.y), z(xx.s)); out[lab] = (b, t, n)
    return out

def bt_report(sig, tgt, costs=(8, 15), **kw):
    rows = []
    for c in costs:
        res, pnl = ll.backtest(sig, tgt, cost_bps=c, **kw)
        for k in ["IS", "OOS", "ALL"]:
            r = res[k]; rows.append({"cost": c, "per": k, **{kk: r.get(kk) for kk in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]}})
        by = res["by_year_bps"]
    return pd.DataFrame(rows), by
