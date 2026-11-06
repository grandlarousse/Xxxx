"""Olay calismasi motoru: genis matrisler (getiri, kilit, piyasa degeri, hacim), t0 eslemesi, CAR/BHAR, kumelenmis t, islem simulasyonu,
takvim-zamani portfoyu. Getiri kaynagi: f10_panel (Is Yatirim duzeltilmis, temettu dahil toplam getiri). Piyasa: XU100 (ChartData)."""
import os, glob, numpy as np, pandas as pd
import f10_panel as P
CACHE = P.CACHE
MAT = f"{CACHE}/matris.pkl"
def matrisler(force=False):
    if os.path.exists(MAT) and not force: return pd.read_pickle(MAT)
    xu = P.xu100(); th = pd.read_parquet(f"{CACHE}/px_tekil/THYAO.parquet").index
    cal = xu.index.intersection(th); cal = cal[cal <= "2026-11-05"]
    rm = xu.reindex(cal).pct_change()
    R, TAV, TAB, PD, VOL, TRD, C = {}, {}, {}, {}, {}, {}, {}
    ks = set(os.path.basename(f)[:-8] for f in glob.glob(f"{CACHE}/px_tekil/*.parquet"))
    ks |= set(os.path.basename(f)[:-8] for f in glob.glob(f"{CACHE}/px_chart/*.parquet")) - {"XU100", "XUTUM", "XYUZO", "XU030"}
    for k in sorted(ks):
        d = P.hisse(k)
        if d is None: continue
        d = d[d.index.isin(cal)]
        if len(d) < 20: continue
        R[k] = d.r; TAV[k] = d.tavan; TAB[k] = d.taban; PD[k] = d.pd; VOL[k] = d.hacim_tl.astype(float); C[k] = d.c
        TRD[k] = pd.Series(True, index=d.index)
    M = {"cal": cal, "rm": rm}
    for nm, D in [("R", R), ("TAV", TAV), ("TAB", TAB), ("PD", PD), ("VOL", VOL), ("TRD", TRD), ("C", C)]:
        X = pd.DataFrame(D).reindex(cal)
        if nm == "R": X = X.fillna(0.0)                     # islem gormeyen gun getirisi 0 (bosluk getirisi acilis gunune yazilir)
        elif nm in ("TAV", "TAB", "TRD"): X = X.fillna(False).astype(bool)
        elif nm == "PD": X = X.ffill(limit=20)
        M[nm] = X
    # ilk islem gunu oncesini NaN yap (halka arz oncesi 0 getiri sayilmasin)
    first = M["TRD"].idxmax(); last = M["TRD"][::-1].idxmax()
    Rv = M["R"].values.copy(); ix = M["R"].index
    for c, k in enumerate(M["R"].columns):
        Rv[ix <= first[k], c] = np.nan; Rv[ix > last[k], c] = np.nan   # halka arz oncesi / kottan cikis sonrasi yok
    M["R"] = pd.DataFrame(Rv, index=ix, columns=M["R"].columns)
    M["PDR"] = M["PD"].rank(axis=1, pct=True)            # gunluk kesitsel piyasa degeri yuzdeligi
    pd.to_pickle(M, MAT); return M
def t0_idx(cal, ts, cutoff_hour=18):
    """Yayim zamani ts (TSI) -> ilk kapanisi bilgiden SONRA olan islem gunu indeksi. 18:00 oncesi yayim: ayni gun (kapanis seansinda alim mumkun)."""
    if pd.isna(ts): return None
    ts = pd.Timestamp(ts); d = ts.normalize()
    j = cal.searchsorted(d)
    if j < len(cal) and cal[j] == d and ts.hour < cutoff_hour: return j
    j = cal.searchsorted(d + pd.Timedelta(days=1))
    return j if j < len(cal) else None
def day_idx(cal, d):
    if pd.isna(d): return None
    j = cal.searchsorted(pd.Timestamp(d).normalize())
    return j if j < len(cal) else None
def beta(M, k, end_idx, n=200, gap=20):
    a, b = end_idx - gap - n, end_idx - gap
    if a < 1: a = 1
    y = M["R"][k].iloc[a:b]; x = M["rm"].iloc[a:b]
    ok = y.notna() & x.notna() & M["TRD"][k].iloc[a:b]
    if ok.sum() < 80: return 0.0, 1.0, int(ok.sum())
    X = np.vstack([np.ones(ok.sum()), x[ok].values]).T
    al, be = np.linalg.lstsq(X, y[ok].values, rcond=None)[0]
    return float(al), float(be), int(ok.sum())
def car(M, k, j0, a, b, al=0.0, be=1.0, model="m"):
    """CAR = sum AR[j0+a .. j0+b]. model 'm': r - rm ; 'mm': r - (al + be*rm). Veri yoksa NaN."""
    lo, hi = j0 + a, j0 + b
    if lo < 1 or hi >= len(M["cal"]): return np.nan
    r = M["R"][k].iloc[lo:hi + 1]; m = M["rm"].iloc[lo:hi + 1]
    if r.isna().any(): return np.nan
    if model == "m": return float((r - m).sum())
    return float((r - al - be * m).sum())
def bhar(M, k, j_in, j_out):
    """j_in kapanisinda al, j_out kapanisinda sat: ham getiri, XU100 getirisi."""
    if j_in is None or j_out is None or j_out <= j_in or j_out >= len(M["cal"]): return np.nan, np.nan
    r = M["R"][k].iloc[j_in + 1:j_out + 1]; m = M["rm"].iloc[j_in + 1:j_out + 1]
    if r.isna().any(): return np.nan, np.nan
    return float(np.prod(1 + r) - 1), float(np.prod(1 + m) - 1)
def dolabilir_giris(M, k, j, maxgec=10):
    """Tavan kilitli kapanista alim dolmaz: ilk kilitsiz kapanisa kaydir. (giris_idx, gecikme)"""
    for g in range(maxgec + 1):
        jj = j + g
        if jj >= len(M["cal"]): return None, None
        if M["TRD"][k].iloc[jj] and not M["TAV"][k].iloc[jj]: return jj, g
    return None, None
def dolabilir_cikis(M, k, j, maxgec=10):
    for g in range(maxgec + 1):
        jj = j + g
        if jj >= len(M["cal"]): return None, None
        if M["TRD"][k].iloc[jj] and not M["TAB"][k].iloc[jj]: return jj, g
    return None, None
def ozet(x, grp=None):
    """Ortalama, medyan, t (tarihe gore kumelenmis, CR1), isabet, p5/p95, N, kume sayisi."""
    x = pd.Series(x, dtype=float); ok = x.notna(); x = x[ok]
    n = len(x)
    if n < 3: return dict(N=n, ort=np.nan, med=np.nan, t=np.nan, isabet=np.nan, p5=np.nan, p95=np.nan, G=np.nan)
    m = x.mean(); e = x - m
    if grp is None: g = pd.Series(np.arange(n), index=x.index)
    else: g = pd.Series(grp)[ok.values] if not isinstance(grp, pd.Series) else grp[ok]
    g = pd.Series(np.asarray(g), index=x.index)
    S = e.groupby(g).sum(); G = len(S)
    v = (S ** 2).sum() / n ** 2 * (G / (G - 1) if G > 1 else 1)
    t = m / np.sqrt(v) if v > 0 else np.nan
    return dict(N=n, ort=m, med=x.median(), t=t, isabet=(x > 0).mean(), p5=x.quantile(.05), p95=x.quantile(.95), G=G)
def takvim_portfoy(M, trades, maliyet=0.0025):
    """trades: list of (k, j_in, j_out). Gunluk esit agirlikli portfoy (acik pozisyonlar), XU100 fazlasi.
    Net: her giriste maliyet/n_acik dusulur (tek seferlik gidis-donus)."""
    cal = M["cal"]; T = len(cal)
    num = np.zeros(T); cnt = np.zeros(T); ent = np.zeros(T)
    for k, a, b in trades:
        if a is None or b is None or b <= a: continue
        r = M["R"][k].iloc[a + 1:b + 1].values
        if np.isnan(r).any(): continue
        num[a + 1:b + 1] += r; cnt[a + 1:b + 1] += 1; ent[a + 1] += 1
    act = cnt > 0
    pr = np.where(act, num / np.maximum(cnt, 1), np.nan); rm = M["rm"].values
    ex = pr - rm; exn = ex - np.where(act, maliyet * ent / np.maximum(cnt, 1), 0)
    s = pd.Series(ex[act], index=cal[act]); sn = pd.Series(exn[act], index=cal[act])
    def nw_t(z, L=5):
        z = z.dropna().values; n = len(z)
        if n < 30: return np.nan
        m = z.mean(); e = z - m; v = (e @ e) / n
        for l in range(1, L + 1): v += 2 * (1 - l / (L + 1)) * (e[l:] @ e[:-l]) / n
        return m / np.sqrt(v / n)
    return dict(gun=int(act.sum()), ort_poz=float(cnt[act].mean()) if act.any() else np.nan,
                gunluk_fazla=float(s.mean()) if len(s) else np.nan, t_nw=nw_t(s),
                gunluk_fazla_net=float(sn.mean()) if len(sn) else np.nan, t_nw_net=nw_t(sn),
                yillik_fazla_net=float(sn.mean() * 252) if len(sn) else np.nan)
