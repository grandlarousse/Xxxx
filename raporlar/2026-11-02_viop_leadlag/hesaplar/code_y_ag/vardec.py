"""1) Varyans ayrıştırması: günlük getiri varyansı = küresel + TR makro + BIST piyasa + sektör/küme + hisseye özgü.
Shapley (genel dominans) R² — düzeltilmiş R² değer fonksiyonu ile; ayrıca 'tek başına' (üst sınır), 'özgün' (alt sınır) ve
sabit sıralı (küresel -> TR -> piyasa -> sektör) ayrıştırma. Faktör-blok düzeyinde (12 blok) Shapley de hesaplanır.
Çalıştır: nice -n 10 python3 vardec.py
"""
import itertools, math, numpy as np, pandas as pd
from common import *

def r2_engine(y, X):
    """Merkezlenmiş Gram matrisi; alt küme R² hesaplayıcı döndürür."""
    y = y - y.mean(); X = X - X.mean(0)
    XtX = X.T @ X; Xty = X.T @ y; yty = float(y @ y); n = len(y)
    def r2(idx, adj=True):
        if len(idx) == 0: return 0.0
        idx = np.asarray(idx)
        A = XtX[np.ix_(idx, idx)]; b = Xty[idx]
        try: beta = np.linalg.solve(A, b)
        except np.linalg.LinAlgError: beta = np.linalg.lstsq(A, b, rcond=None)[0]
        R2 = float(beta @ b) / yty
        if not adj: return R2
        k = len(idx); return 1 - (1 - R2) * (n - 1) / (n - k - 1)
    return r2, n

def shapley(blocks, r2):
    """blocks: dict ad -> sütun indeksleri. Dönüş: shapley, alone, unique, R2_full."""
    names = list(blocks); m = len(names); cache = {}
    def v(S):
        key = frozenset(S)
        if key not in cache:
            idx = sorted(itertools.chain.from_iterable(blocks[x] for x in S)); cache[key] = r2(idx)
        return cache[key]
    full = v(names); sh = {}
    for g in names:
        others = [x for x in names if x != g]; tot = 0.0
        for k in range(m):
            w = math.factorial(k) * math.factorial(m - k - 1) / math.factorial(m)
            for S in itertools.combinations(others, k):
                tot += w * (v(list(S) + [g]) - v(S))
        sh[g] = tot
    alone = {g: v([g]) for g in names}; unique = {g: full - v([x for x in names if x != g]) for g in names}
    return sh, alone, unique, full, v

def build(stock, spec="base"):
    F = factors(); y = stock_rets()[stock]
    gl = GLOBAL; cols = {}
    if spec == "compact":
        G = ["ES=F", "ES=F_l1", "EEM", "EEM_l1", "^STOXX50E"]
    elif spec == "g_lag0":
        G = list(gl)
    else:
        G = [c for g in gl for c in (g, g + "_l1")]
    TRc = ["TRY=X", "TRY=X_l1"] + ([] if spec == "tr_fx_only" else ["TUR_l1"])
    D = F[G + TRc].copy()
    D["MKT"] = ew_market_ex(stock) if spec == "mkt_ew" else F["XU100"]
    D["SEC"] = peer_factor(stock)
    D["y"] = y
    return D, G, TRc

def run_one(D, G, TRc, start, end, block_level=False):
    d = D[(D.index >= start) & (D.index <= end)].dropna()
    if len(d) < 40 or d["SEC"].std() == 0: return None
    cols = G + TRc + ["MKT", "SEC"]; X = d[cols].values.astype(float); y = d["y"].values.astype(float)
    r2, n = r2_engine(y, X); ix = {c: i for i, c in enumerate(cols)}
    groups = {"global": [ix[c] for c in G], "trmakro": [ix[c] for c in TRc], "piyasa": [ix["MKT"]], "sektor": [ix["SEC"]]}
    sh, alone, uniq, full, v = shapley(groups, r2)
    out = {"n": n, "r2_full_adj": full, "r2_full_raw": r2(list(range(len(cols))), adj=False), "idio": 1 - full}
    for g in groups:
        out[f"sh_{g}"] = sh[g]; out[f"alone_{g}"] = alone[g]; out[f"uniq_{g}"] = uniq[g]
    # sabit sıralı: küresel -> TR -> piyasa -> sektör
    seq = ["global", "trmakro", "piyasa", "sektor"]; prev = 0.0
    for i, g in enumerate(seq):
        cur = v(seq[:i + 1]); out[f"hier_{g}"] = cur - prev; prev = cur
    # yerli-önce sıralı: sektör -> piyasa -> TR -> küresel (küreselin 'saf' alt sınırı)
    seq2 = ["sektor", "piyasa", "trmakro", "global"]; prev = 0.0
    for i, g in enumerate(seq2):
        cur = v(seq2[:i + 1]); out[f"hier2_{g}"] = cur - prev; prev = cur
    out["global_frac_of_sys"] = sh["global"] / full if full > 0 else np.nan
    out["vol_ann_pct"] = float(d["y"].std() * np.sqrt(252) * 100)
    if block_level:
        bl = {}
        for g in GLOBAL:
            bl[g] = [ix[c] for c in (g, g + "_l1") if c in ix]
        bl["TRY=X"] = [ix["TRY=X"], ix["TRY=X_l1"]]
        if "TUR_l1" in ix: bl["TUR_l1"] = [ix["TUR_l1"]]
        bl["XU100"] = [ix["MKT"]]; bl["SEKTOR"] = [ix["SEC"]]
        shb, _, _, _, _ = shapley(bl, r2)
        for k, val in shb.items(): out[f"blk_{k}"] = val
    return out

def xu100_level():
    F = factors(); rows = []
    G = [c for g in GLOBAL for c in (g, g + "_l1")]; TRc = ["TRY=X", "TRY=X_l1", "TUR_l1"]
    for pn, (a, b) in list(PERIODS.items()) + [("fonkrizi", ("2026-09-01", "2026-10-30")), ("2026oca-agu", ("2026-01-01", "2026-08-31"))]:
        d = F[G + TRc + ["XU100"]]; d = d[(d.index >= a) & (d.index <= b)].dropna()
        if pn in ("fonkrizi",): Gc = ["ES=F", "ES=F_l1", "EEM", "EEM_l1", "^STOXX50E"]
        else: Gc = G
        X = d[Gc + TRc].values; y = d["XU100"].values; r2, n = r2_engine(y, X)
        ix = {c: i for i, c in enumerate(Gc + TRc)}
        sh, alone, uniq, full, v = shapley({"global": [ix[c] for c in Gc], "trmakro": [ix[c] for c in TRc]}, r2)
        rows.append({"stock": "XU100", "period": pn, "spec": "base" if pn != "fonkrizi" else "compact", "n": n, "r2_full_adj": full,
                     "sh_global": sh["global"], "sh_trmakro": sh["trmakro"], "alone_global": alone["global"], "alone_trmakro": alone["trmakro"],
                     "uniq_global": uniq["global"], "uniq_trmakro": uniq["trmakro"], "idio": 1 - full})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    import time; t0 = time.time(); rows = []
    for s in STOCKS:
        for spec in ["base", "mkt_ew", "tr_fx_only", "g_lag0"]:
            D, G, TRc = build(s, spec)
            for pn, (a, b) in PERIODS.items():
                o = run_one(D, G, TRc, a, b, block_level=(spec == "base"))
                if o: rows.append({"stock": s, "sector": SECT[s], "period": pn, "spec": spec, **o})
        D, G, TRc = build(s, "compact")
        for pn, (a, b) in [("fonkrizi", ("2026-09-01", "2026-10-30")), ("2026oca-agu", ("2026-01-01", "2026-08-31")), ("son1y", PERIODS["son1y"]), ("tam", PERIODS["tam"])]:
            o = run_one(D, G, TRc, a, b)
            if o: rows.append({"stock": s, "sector": SECT[s], "period": pn, "spec": "compact", **o})
        print(s, round(time.time() - t0, 1), flush=True)
    V = pd.DataFrame(rows)
    V = pd.concat([V, xu100_level()], ignore_index=True)
    V.to_csv(os.path.join(CACHE, "vardec_all.csv"), index=False)
    print(V.shape, time.time() - t0)
