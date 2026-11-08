"""3) Seçim düzeltmeli test: genel kütüphanenin 31 sinyali x {C0,O1,C1} x h{1,2,3} = 279 hücrede en yüksek net-t'nin
dairesel kaydırma (tüm sinyaller aynı kaydırma; sinyal kümelenmesi korunur) altındaki dağılımı. Ayrıca 19 temsilcinin
'hepsinde net>0' bulgusunun aynı null altındaki olasılığı. Hızlı çakışmasız simülasyon (yalnız sinyal günleri üzerinde)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
import strategies as S
rng = np.random.default_rng(7)

def fast(c, o, idx, h, mode, n):
    out = []; nxt = 0
    for i in idx:
        if i < nxt: continue
        if mode == 0: e, ep, x = i, c[i], i + h
        elif mode == 1:
            e = i + 1; x = i + h
            if e >= n: break
            ep = o[e]
        else:
            e = i + 1; x = i + 1 + h
            if e >= n: break
            ep = c[e]
        if x >= n: break
        out.append(c[x] / ep - 1); nxt = max(x, i + 1)
    return np.array(out)

def tnet(g, cost):
    if len(g) < 40: return np.nan
    x = g - cost / 1e4; s = x.std(ddof=1)
    return x.mean() / (s / math.sqrt(len(x))) if s > 0 else np.nan

ctx = {k: lib.vol_index(k) for k in ("VIX", "VIX3M")}
def sig_matrix(d):
    M = {}
    for k, f in S.LIB.items():
        s = f(d, ctx).reindex(d.index).fillna(False).astype(bool).values.copy(); s[:dt.WARM] = False
        M[k] = s
    return M

def maxt(d, M, shift, cost):
    c = d["c"].values; o = d["o"].values; n = len(c); best = -9; arg = None
    for k, s in M.items():
        z = np.roll(s, shift) if shift else s
        if shift: z = z.copy(); z[:dt.WARM] = False
        idx = np.flatnonzero(z)
        for m in (0, 1, 2):
            for h in (1, 2, 3):
                t = tnet(fast(c, o, idx, h, m, n), cost)
                if np.isfinite(t) and t > best: best, arg = t, (k, "C0 O1 C1".split()[m], h)
    return best, arg

NREP = int(os.environ.get("NREP", "400"))
res = []
for sym in ("SPY", "QQQ"):
    d = lib.load(sym); M = sig_matrix(d); cost = dt.cost_bp(sym, 2500)
    obs, arg = maxt(d, M, 0, cost)
    t_s1 = {m: tnet(fast(d["c"].values, d["o"].values, np.flatnonzero(M["MR_ibs_lt01_dusus"]), 3, mi, len(d)), cost) for mi, m in enumerate(("C0", "O1", "C1"))}
    n = len(d); null = []
    for r in range(NREP):
        null.append(maxt(d, M, int(rng.integers(250, n - 250)), cost)[0])
    null = np.array(null)
    rec = {"sym": sym, "gozlenen_max_t": round(obs, 2), "max_hucre": str(arg), "S1_t_C0_C1": f"{t_s1['C0']:.2f}/{t_s1['C1']:.2f}",
           "null_max_t_medyan": round(np.median(null), 2), "null_max_t_95": round(np.quantile(null, 0.95), 2),
           "p_max_gozlenen": round((np.sum(null >= obs) + 1) / (NREP + 1), 4),
           "p_S1_C1_secim_duzeltmeli": round((np.sum(null >= t_s1["C1"]) + 1) / (NREP + 1), 4),
           "p_S1_C0_secim_duzeltmeli": round((np.sum(null >= t_s1["C0"]) + 1) / (NREP + 1), 4)}
    print(rec); res.append(rec)
pd.DataFrame(res).to_csv(os.path.join(dt.OUT, "secim_duzeltmeli_maxt.csv"), index=False)

# 19 temsilci: 'hepsinde net>0' (C1 h3, MR_ibs_lt01_dusus) dairesel kaydırma null'ı
REPS = ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY", "IWF", "IWD", "SCHD", "SPLV", "SPHB", "MTUM", "QUAL", "VLUE", "IWO", "IWN", "COWZ", "JEPI", "QYLD"]
DD = {s: lib.load(s) for s in REPS}
base = pd.bdate_range("2016-01-01", "2026-12-31")
SG = {s: dt.s1_signal(DD[s]) for s in REPS}
COST = {s: dt.cost_bp(s, 2500) for s in REPS}
def fam(shift):
    nets = []
    for s in REPS:
        d = DD[s]; z = np.roll(SG[s], shift) if shift else SG[s].copy(); z[:dt.WARM] = False
        g = fast(d["c"].values, d["o"].values, np.flatnonzero(z), 3, 2, len(d))
        nets.append(g.mean() * 1e4 - COST[s] if len(g) else np.nan)
    return np.array(nets)
obs = fam(0)
nmin = min(len(DD[s]) for s in REPS)
nul = np.array([fam(int(rng.integers(250, nmin - 250))) for _ in range(1000)])
print(f"19 temsilci C1 h3: gözlenen pozitif sayısı {np.sum(obs > 0)}/19, ort net {np.nanmean(obs):.1f}; "
      f"null: 19/19 olasılığı {(np.sum(nul > 0, axis=1) == 19).mean():.3f}, >=18 olasılığı {(np.sum(nul > 0, axis=1) >= 18).mean():.3f}, "
      f"ort net null medyan {np.median(np.nanmean(nul, axis=1)):.1f}, p(ort)={(np.sum(np.nanmean(nul, axis=1) >= np.nanmean(obs)) + 1) / 1001:.4f}")
