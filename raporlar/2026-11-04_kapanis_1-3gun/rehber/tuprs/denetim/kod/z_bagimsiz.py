"""DENETİM (rehber_tuprs_denetim) — TUPRS <- ABD rafineri sepeti z'sinin BAĞIMSIZ hesabı.
sinyal_tuprs.py, cl.py, cl_t.py import EDİLMEZ. Açık döngülerle (rolling yok) yeniden yazıldı.
Veri: denetim/veri/daily (Yahoo, 04.11.2026'da yeniden indirildi), BIST takvimi = VİOP panelindeki XU030 günleri
 + 02–03.11.2026 bültenleri + hedef seans(lar).
Çıktı: denetim/sonuc/z_bagimsiz.csv (BIST günü, kullanılan ABD günleri, P, sd, z, sinyal)."""
import os, sys, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/out/rehber/tuprs/denetim"
os.makedirs(D + "/sonuc", exist_ok=True)
MEM = ["VLO", "MPC", "PSX", "PBF"]

def adj(sym):
    d = pd.read_parquet(f"{D}/veri/daily/{sym}.parquet")
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"])).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d["adj"].astype(float)

def bist_cal(extra=()):
    p = pd.read_parquet(S + "/data/viop_panel.parquet", columns=["date", "und"])
    c = set(pd.DatetimeIndex(p.loc[p["und"].astype(str) == "XU030", "date"]).normalize())
    q = pd.read_parquet(S + "/dl_k_sahol_a/viop_new.parquet", columns=["date", "und"])
    c |= set(pd.DatetimeIndex(q.loc[q["und"].astype(str) == "XU030", "date"]).normalize())
    c |= set(pd.DatetimeIndex(list(extra)))
    return pd.DatetimeIndex(sorted(c))

def beta_loop(y, x, w=250, minn=100):
    """b[j] = cov/var of (y,x) over rows j-w .. j-1 (o gün HARİÇ), iki taraf da dolu, en az minn çift."""
    n = len(y); b = np.full(n, np.nan)
    for j in range(n):
        a = max(0, j - w); yy = y[a:j]; xx = x[a:j]
        m = np.isfinite(yy) & np.isfinite(xx)
        if m.sum() < minn: continue
        xm = xx[m] - xx[m].mean(); ym = yy[m] - yy[m].mean()
        v = (xm * xm).sum()
        if v > 0: b[j] = (xm * ym).sum() / v
    return b

def us_basket(last_us=None):
    spx = adj("^GSPC")
    if last_us is not None: spx = spx[spx.index <= last_us]
    us = spx.index
    rm = np.log(spx).diff().values
    res = {}
    for m in MEM:
        a = adj(m); a = a.where(a > 0)
        r_own = np.log(a).diff()                       # hissenin kendi takviminde getiri
        r = r_own.reindex(us).values
        b = beta_loop(r, rm)
        res[m] = r - b * rm
        res["b_" + m] = b; res["r_" + m] = r
    R = pd.DataFrame(res, index=us)
    E = R[MEM]
    cnt = np.isfinite(E.values).sum(1)
    P = np.where(cnt >= 3, np.nanmean(np.where(np.isfinite(E.values), E.values, np.nan), axis=1), np.nan)
    R["P"] = P; R["rm"] = rm
    return R

def map_after(R, cal):
    """BIST günü cal[k]: cal[k-1] <= ABD günü < cal[k] olan ve P'si dolu ABD günlerinin toplamı. k=0 için boş."""
    us = R.index.values; P = R["P"].values
    out = np.full(len(cal), np.nan); used = [""] * len(cal)
    for k in range(1, len(cal)):
        lo, hi = cal[k - 1], cal[k]
        sel = (us >= lo.to_datetime64()) & (us < hi.to_datetime64())
        v = P[sel]; days = R.index[sel]
        used[k] = ",".join(f"{d:%m-%d}" for d in days)
        v = v[np.isfinite(v)]
        if len(v): out[k] = v.sum()
    return out, used

def zloop(pb, w=250, minn=100):
    n = len(pb); sd = np.full(n, np.nan)
    for k in range(n):
        x = pb[max(0, k - w):k]; x = x[np.isfinite(x)]
        if len(x) >= minn: sd[k] = x.std(ddof=1)
    return pb / sd, sd

def build(extra=(pd.Timestamp("2026-11-04"),), last_us=None):
    cal = bist_cal(extra)
    R = us_basket(last_us)
    pb, used = map_after(R, cal)
    z, sd = zloop(pb)
    Z = pd.DataFrame({"abd_gunleri": used, "P": pb, "sd": sd, "z": z}, index=cal)
    Z["sinyal"] = np.where(np.isfinite(Z["z"]) & (Z["z"].abs() > 1), np.sign(Z["z"]), 0).astype(int)
    return Z, R

if __name__ == "__main__":
    Z, R = build()
    Z.to_csv(D + "/sonuc/z_bagimsiz.csv")
    print(Z.tail(12).to_string())
    print("son ABD günleri ve betalar:"); print(R[[c for c in R.columns if c.startswith("b_")] + ["P"]].tail(4).round(4).to_string())
