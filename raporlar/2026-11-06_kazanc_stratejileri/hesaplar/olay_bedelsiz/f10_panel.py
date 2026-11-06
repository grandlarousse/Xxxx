"""Fiyat paneli: temiz duzeltilmis getiri, tavan/taban kilidi, piyasa degeri, XU100.
Duzeltilmis getiri: r_t = (c_t/c_{t-1}) * (q_{t-1}/q_t) - 1 ; q = c/adj (Is Yatirim duzeltme carpani). q parcali sabit; 4 ondalik
yuvarlama gurultusunu atmak icin her parca icinde MEDYAN q kullanilir. Parca sinirlari: |dlog q|>%0.8 ve kalici (sonraki 5 gun
medyani ile onceki 5 gun medyani farki >%0.8) olan gunler. Boylece bedelsiz/bolunme/bedelli/temettu gunu sicramalari temizlenir.
Kilit: duzeltilmis getiri >= +%9 ve kapanis == gun ici en yuksek  -> tavan kilidi (kapanista alim dolmaz varsayimi);
       duzeltilmis getiri <= -%9 ve kapanis == gun ici en dusuk  -> taban kilidi (kapanista satis dolmaz varsayimi)."""
import os, numpy as np, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz"
def xu100():
    x = pd.read_parquet(f"{CACHE}/px_chart/XU100.parquet").px
    return x[x.index <= "2026-11-05"]
_ISY = None
def isy_olaylar():
    global _ISY
    if _ISY is None:
        _ISY = pd.read_csv(f"{CACHE}/isy_sermaye_all.csv", parse_dates=["tarih"])
    return _ISY
def hisse(kod):
    p = f"{CACHE}/px_tekil/{kod}.parquet"
    if not os.path.exists(p): return None
    d = pd.read_parquet(p)
    if len(d) < 30: return None
    d = d[(d.c > 0) & (d.adj > 0)].copy()
    lq = np.log(d.c / d.adj)
    dl = lq.diff()
    fwd = lq[::-1].rolling(5, min_periods=1).median()[::-1]            # t..t+4
    bwd = lq.shift(1).rolling(5, min_periods=1).median()               # t-5..t-1
    thr = np.maximum(0.008, 6 * 0.00005 / d.adj)                       # 4 ondalik yuvarlama gurultusu
    jump = (fwd - bwd).abs()
    brk = (dl.abs() > thr) & (jump > thr)
    # Is Yatirim listesindeki olay gunleri: [-1,+2] islem gunu icinde en buyuk |dlog q| gunu (>%0.3 ve kalici) sinir sayilir
    ev = isy_olaylar(); ev = ev[ev.HISSE_KODU == kod].tarih.dropna()
    idx = d.index
    for t in ev:
        j = idx.searchsorted(t)
        lo, hi = max(1, j - 1), min(len(idx), j + 3)
        if lo >= hi: continue
        w = dl.iloc[lo:hi].abs()
        if len(w) and w.max() > 0.003:
            k = w.idxmax()
            if jump.loc[k] > 0.003: brk.loc[k] = True
    seg = brk.cumsum()
    lqm = lq.groupby(seg).transform("median")
    d["r"] = np.exp(np.log(d.c / d.c.shift(1)) - (lqm - lqm.shift(1))) - 1
    d["adjf"] = np.exp(-(lqm - lqm.shift(1)))                          # ex-gun carpani (1 = olay yok)
    d["brk"] = brk
    eps = 1e-9
    d["tavan"] = (d.r >= 0.09) & (d.c >= d.hi - eps)
    d["taban"] = (d.r <= -0.09) & (d.c <= d.lo + eps)
    d["pd"] = d.pd.astype(float)
    return d
