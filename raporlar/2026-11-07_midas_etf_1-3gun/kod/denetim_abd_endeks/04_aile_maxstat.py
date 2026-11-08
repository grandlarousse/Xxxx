"""4) Aile düzeyinde seçim düzeltmeli test: 31 sinyal x 9 hücre için 19 temsilcinin ortalama net-t'si (aile tutarlılığı
istatistiği); gözlenen en yüksek değerin, tüm ETF'lere aynı dairesel kaydırma uygulanan null altındaki p'si."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
import strategies as S


rng = np.random.default_rng(11)
REPS = ["SPY", "QQQ", "IWM", "DIA", "RSP", "MDY", "IWF", "IWD", "SCHD", "SPLV", "SPHB", "MTUM", "QUAL", "VLUE", "IWO", "IWN", "COWZ", "JEPI", "QYLD"]
ctx = {k: lib.vol_index(k) for k in ("VIX", "VIX3M")}

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
    if len(g) < 25: return np.nan
    x = g - cost / 1e4; s = x.std(ddof=1)
    return x.mean() / (s / math.sqrt(len(x))) if s > 0 else np.nan

DD = {s: lib.load(s) for s in REPS}
COST = {s: dt.cost_bp(s, 2500) for s in REPS}
# Ortak takvim (SPY) üzerinde hizala ki aynı kaydırma aynı tarihlere karşılık gelsin
cal = DD["SPY"].index
for s in REPS: DD[s] = DD[s].reindex(cal).ffill()
SIG = {}
for s in REPS:
    d = DD[s]; M = {}
    for k, f in S.LIB.items():
        z = f(d, ctx).reindex(cal).fillna(False).astype(bool).values.copy(); z[:dt.WARM] = False
        # ETF'nin verisi başlamadan önceki günler (ffill ile doldurulanlar) sinyalsiz
        z &= lib.load(s).reindex(cal)["c"].notna().values
        M[k] = z
    SIG[s] = M
CO = {s: (DD[s]["c"].values, DD[s]["o"].values) for s in REPS}
n = len(cal)
def stat(shift):
    best = -9; arg = None; tab = {}
    for k in S.LIB:
        for m in (0, 1, 2):
            for h in (1, 2, 3):
                ts = []
                for s in REPS:
                    z = SIG[s][k]
                    if shift: z = np.roll(z, shift).copy(); z[:dt.WARM] = False
                    c, o = CO[s]
                    ts.append(tnet(fast(c, o, np.flatnonzero(z), h, m, n), COST[s]))
                v = np.nanmean(ts); tab[(k, m, h)] = v
                if np.isfinite(v) and v > best: best, arg = v, (k, "C0 O1 C1".split()[m], h)
    return best, arg, tab
obs, arg, tab = stat(0)
s1 = {m: tab[("MR_ibs_lt01_dusus", mi, 3)] for mi, m in enumerate(("C0", "O1", "C1"))}
top = sorted(tab.items(), key=lambda kv: -kv[1])[:8]
print("gözlenen en yüksek 8 hücre (19 temsilcinin ort. t'si):", [(k, round(v, 2)) for k, v in top])
NREP = int(os.environ.get("NREP", "300"))
null = np.array([stat(int(rng.integers(250, n - 250)))[0] for _ in range(NREP)])
rec = {"gozlenen_max_ort_t": round(obs, 3), "hucre": str(arg), "S1_ort_t_C0_O1_C1": {k: round(v, 2) for k, v in s1.items()},
       "null_medyan": round(np.median(null), 3), "null_95": round(np.quantile(null, 0.95), 3),
       "p_max": round((np.sum(null >= obs) + 1) / (NREP + 1), 4),
       "p_S1_C0": round((np.sum(null >= s1["C0"]) + 1) / (NREP + 1), 4), "p_S1_O1": round((np.sum(null >= s1["O1"]) + 1) / (NREP + 1), 4)}
print(rec)
pd.DataFrame([rec]).to_csv(os.path.join(dt.OUT, "aile_maxstat.csv"), index=False)
