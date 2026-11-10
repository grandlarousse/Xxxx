"""b3: F6 kesif taramasi (PLAN.md v2, 5. bolum). python3 -I b3_kesif.py [NREP]"""
import os, sys, time, warnings, numpy as np, pandas as pd
from scipy import stats as st
warnings.filterwarnings("ignore")
V = "/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/"
R0 = "/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/"
EK = R0 + "ek/"
T0 = time.time()
NREP = int(sys.argv[1]) if len(sys.argv) > 1 else 200
def log(*a): print(f"[{time.time()-T0:5.0f}s]", *a, flush=True)

fr = pd.read_parquet(V + "fut_ret.parquet"); cal = pd.DatetimeIndex(fr.index).normalize(); N = len(cal); fr.index = cal
def W(n): d = pd.read_parquet(V + n); d.index = cal; return d
FL, FT, FV, FC = W("fut_limit.parquet"), W("fut_trades.parquet"), W("fut_value_tl.parquet"), W("fut_code.parquet")
sp = pd.read_parquet(V + "spot_gunluk.parquet"); sp["date"] = pd.to_datetime(sp["date"]).dt.normalize()
def pv(col): return sp.pivot_table(index="date", columns="sym", values=col, aggfunc="last").reindex(cal)
ADJ, CC, VV, HH, LL = pv("adj"), pv("c"), pv("v"), pv("h"), pv("l")
spl = pd.read_csv(V + "bolunme_gunleri.csv"); spl["date"] = pd.to_datetime(spl["date"]).dt.normalize()
SPLD = {s_: set(g["date"]) for s_, g in spl.groupby("sym")}
sh = pd.read_parquet(V + "saatlik.parquet")
sh["d"] = sh["ts_utc"].dt.tz_convert("UTC").dt.tz_localize(None).dt.normalize()
sh["hm"] = sh["ts_utc"].dt.hour * 60 + sh["ts_utc"].dt.minute
UND = [c for c in fr.columns if c not in ("XU030", "XLBNK", "USDTRY", "XAUUSD", "XAGUSD", "XAUTRY")]
IDX = ("XU030.IS", "XBANK.IS", "XU100.IS")
RAWL = ("XU030.IS", "XBANK.IS")
YR = cal.year.values
MARJ_D = pd.Timestamp("2020-03-13")
PM = {"IS": (cal >= "2017-03-01") & (cal <= "2022-12-31"), "OOS": cal >= "2023-01-01", "TAM": np.ones(N, bool),
      "SON2Y": cal >= "2024-11-10", "Y2526": cal >= "2025-01-01", "KWIN": cal >= "2023-11-09"}
iE = int(np.argmax(cal >= "2023-01-01"))
YEARS = {"IS": 5.83, "OOS": 3.92, "TAM": 9.7, "SON2Y": 2.0}

_S = {}
def srets(sym):
    if sym in _S: return _S[sym]
    if sym not in ADJ.columns or ADJ[sym].notna().sum() < 300: _S[sym] = None; return None
    a = ADJ[sym]; r = np.log(a / a.shift(1))
    if sym in IDX: r[r.abs() > 0.5] = np.nan
    else:
        m = pd.Series(np.where(cal < MARJ_D, 0.20, 0.10), index=cal)
        r[(r > np.log(1 + m + 0.005)) | (r < np.log(1 - m - 0.005))] = np.nan
    for d in SPLD.get(sym, ()):
        if d in r.index: r[d] = np.nan
    stale = (VV[sym] == 0) & (HH[sym] == LL[sym]); r[stale] = np.nan
    craw = np.log(CC[sym] / CC[sym].shift(1))
    exd = ((craw - np.log(a / a.shift(1))).abs() > 0.005) | pd.Series([d in SPLD.get(sym, ()) for d in cal], index=cal)
    _S[sym] = (r, exd); return _S[sym]
def katir(sym):
    g = sh[sh["sym"] == sym]
    if len(g) == 0 or sym not in CC.columns: return None
    pc = g.pivot_table(index="d", columns="hm", values="c", aggfunc="last").reindex(cal)
    for k in (750, 810, 870):
        if k not in pc.columns: pc[k] = np.nan
    p = pc[810].where(pc[870].notna(), pc[750])
    r = np.log(p / CC[sym].shift(1)); s = srets(sym)
    if s is not None: r[s[1]] = np.nan
    if sym in IDX: r[r.abs() > 0.5] = np.nan
    else:
        m = pd.Series(np.where(cal < MARJ_D, 0.20, 0.10), index=cal); r[(r.abs() > np.log(1 + m + 0.005))] = np.nan
    return r
def rolsd(x, w=120, mp=60): return x.rolling(w, min_periods=mp).std().shift(1)
_E = {}
def eres(sym):
    if sym in _E: return _E[sym]
    s = srets(sym)
    if s is None: _E[sym] = None; return None
    r = s[0]; rm = srets("XU030.IS")[0]
    beta = None if sym in RAWL else (r.rolling(250, min_periods=120).cov(rm) / rm.rolling(250, min_periods=120).var()).shift(1)
    e = r.copy() if beta is None else r - beta * rm
    d = {"r": r, "e": e, "sig": rolsd(e), "beta": beta}
    _E[sym] = d; return d
_K = {}
def ezk(sym):
    """KATI_1730 z (sigma ana tanimla ayni)"""
    if sym in _K: return _K[sym]
    E = eres(sym); rK = katir(sym)
    if E is None or rK is None: _K[sym] = None; return None
    if E["beta"] is None: eK = rK
    else:
        rmK = katir("XU030.IS"); eK = rK - E["beta"] * rmK
    _K[sym] = (eK / E["sig"]).values; return _K[sym]

LIK = pd.read_csv("/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv").set_index("und")["rt_cost_retail_bps"]
_T = {}
def tgt(h):
    if h in _T: return _T[h]
    f = fr[h].copy(); E = eres(h + ".IS")
    if E is None: _T[h] = None; return None
    z = (E["e"] / E["sig"]).values
    db = f - E["r"]; zb = (db / rolsd(db)).abs().values
    ok = ((FT[h] >= 20) & (FV[h] >= 1e6) & (FL[h] != 1)).values
    fa = f.values
    cs = np.concatenate([[0], np.nancumsum(fa)]); nn = np.concatenate([[0], np.cumsum(np.isnan(fa))])
    codes = FC[h].values; chg = np.zeros(N, bool); chg[1:] = codes[1:] != codes[:-1]
    cc = np.concatenate([[0], np.cumsum(chg)])
    A, ROLL = {}, {}
    for hh in (1, 2, 3):
        a = np.full(N, np.nan); rl = np.zeros(N, bool)
        for i in range(N - hh):
            if ok[i] and ok[i + hh] and nn[i + hh + 1] - nn[i + 1] == 0:
                a[i] = (cs[i + hh + 1] - cs[i + 1]) * 1e4; rl[i] = (cc[i + hh + 1] - cc[i + 1]) > 0
        A[hh] = a; ROLL[hh] = rl
    drift = pd.Series(fa, index=cal).groupby(YR).mean()
    dr = np.array([drift.get(y, 0.0) for y in YR]) * 1e4
    rt = float(LIK.get(h, 22)) if not pd.isna(LIK.get(h, np.nan)) else 22.0
    _T[h] = dict(z=z, zb=zb, A=A, ROLL=ROLL, dr=dr, retail=rt, cost=(8, 15), rf=fa); return _T[h]

def chain(m, d, A, s, h=2):
    idx = np.nonzero(m)[0]; idx = idx[idx + s < N]; idx = idx[~np.isnan(A[idx + s])]
    out = []; last = -1
    for i in idx.tolist():
        e = i + s
        if e < last: continue
        out.append(i); last = e + h
    ii = np.array(out, int); return ii, d[ii]
def tstat(x):
    n = len(x)
    if n < 2: return np.nan
    sd = np.std(x, ddof=1); return np.mean(x) / (sd / np.sqrt(n)) if sd > 0 else np.nan
def stats(ii, dd, T, s, pm, h=2, full=True):
    sel = pm[ii]; ii = ii[sel]; dd = dd[sel]; n = len(ii)
    if n == 0: return dict(n=0)
    e = ii + s; g = dd * T["A"][h][e]; rl = T["ROLL"][h][e]
    o = dict(n=n, brut=g.mean(), t=tstat(g))
    if not full: return o
    dr = g - dd * h * T["dr"][ii]; c8, c15 = T["cost"]
    gs = np.sort(g)[::-1]; g10 = gs[10:] if n > 10 else np.array([])
    yy = YR[ii] - 2017; sm = np.bincount(yy, g, 10); ct = np.bincount(yy, minlength=10); u = ct > 0
    o.update(net8=np.mean(g - c8 * (1 + rl)), net15=np.mean(g - c15 * (1 + rl)), net_bireysel=np.mean(g - T["retail"] * (1 + rl)),
             isabet=(g > 0).mean(), medyan=np.median(g), brut_ilk10haric=g10.mean() if len(g10) else np.nan,
             t_ilk10haric=tstat(g10) if len(g10) > 1 else np.nan, poz_yil=int(((sm[u] / ct[u]) > 0).sum()), yil_say=int(u.sum()),
             brut_suruklenme_duz=dr.mean(), uzun_pay=(dd > 0).mean())
    return o

# ---------------- evren
TG = {}
for h in UND:
    T = tgt(h)
    if T is not None: TG[h] = T
leaders = []
for c in ADJ.columns:
    if not c.endswith(".IS") or c == "XU100.IS": continue
    E = eres(c)
    if E is None: continue
    z = (E["e"] / E["sig"]).values
    if np.isfinite(z[PM["IS"]]).sum() >= 750: leaders.append(c)
LZ = np.column_stack([(eres(c)["e"] / eres(c)["sig"]).values for c in leaders])
L = len(leaders)
def excl(h, c):
    if c == h + ".IS": return True
    if h == "KRDMD" and c in ("KRDMA.IS", "KRDMB.IS"): return True
    if h == "EREGL" and c == "ISDMR.IS": return True
    return False
EXC = {h: np.array([excl(h, c) for c in leaders]) for h in TG}
NP = sum(int((~EXC[h]).sum()) for h in TG)
log(f"hedef {len(TG)}, oncu {L}, taranan cift {NP}")

# ---------------- gercek tarama (orrtusmesiz)
rows = []; SEL = []; REAL = {}
def rowdict(aile_h, c, rho, sig, per, st_, giris="E0"):
    d = dict(aile="F6_KESIF", hedef=aile_h, oncu=c, isaret=rho, zamanlama="YURTICI", agirlik="-", sinyal=sig, giris=giris, tutma=2, donem=per)
    d.update(st_)
    if st_.get("n", 0) > 0 and per in YEARS: d["yillik_n"] = st_["n"] / YEARS[per]
    return d
fields = ["n", "brut", "net8", "net15", "net_bireysel", "t", "isabet", "medyan", "brut_ilk10haric", "t_ilk10haric", "poz_yil", "yil_say", "brut_suruklenme_duz", "uzun_pay"]
for h, T in TG.items():
    zT = T["z"]; A2 = T["A"][2]; okT = ~np.isnan(zT)
    for j, c in enumerate(leaders):
        if EXC[h][j]: continue
        zL = LZ[:, j]; d = np.sign(zL)
        m = (np.abs(zL) >= 1) & okT & (d * zT <= 0.25)
        if m.sum() < 5: continue
        ii, dd = chain(m, d, A2, 0)
        if len(ii) == 0: continue
        for yon, sg in (("ILERI", 1), ("TERS", -1)):
            sin = "S_KUL" if sg == 1 else "S_KUL_TERSYON"
            res = {}
            for per in ("IS", "OOS"):
                s_ = stats(ii, dd * sg, T, 0, PM[per]); res[per] = s_
                if s_["n"] > 0: rows.append(rowdict(h, c, sg, sin, per, {k: s_.get(k) for k in fields}))
            si = res["IS"]
            if si["n"] >= 40 and si["t"] >= 3: SEL.append((h, c, yon, sg, ii, dd))
            REAL[(h, c, yon)] = (res["IS"], res["OOS"])
log("tarama bitti; satir", len(rows), "secilen", len(SEL))
npairs_scanned = len({(k[0], k[1]) for k in REAL})
def cnt(yon, f): return sum(1 for k, (a, b) in REAL.items() if k[2] == yon and f(a, b))
real_no = {}
for yon in ("ILERI", "TERS"):
    nsel = cnt(yon, lambda a, b: a["n"] >= 40 and a["t"] >= 3)
    ns = cnt(yon, lambda a, b: a["n"] >= 40 and a["t"] >= 3 and b["n"] >= 2 and b["t"] >= 2)
    ns20 = cnt(yon, lambda a, b: a["n"] >= 40 and a["t"] >= 3 and b["n"] >= 20 and b["t"] >= 2)
    real_no[yon] = (nsel, ns, ns20)
log("gercek (orrtusmesiz) secilen/ayakta/ayakta20:", real_no)

# ---------------- kaydirma (orrtusmeye izin; ayni bicimde gercek)
MABS = (np.abs(np.nan_to_num(LZ, nan=0.0)) >= 1)
SGN = np.sign(np.nan_to_num(LZ, nan=0.0))
PREP = {}
for h, T in TG.items():
    A = T["A"][2]; zT = T["z"]; vm = ~np.isnan(A) & ~np.isnan(zT)
    PREP[h] = (np.nan_to_num(A, nan=0.0), np.nan_to_num(zT, nan=0.0), vm, ~EXC[h])
AR = np.arange(N)
def tt(s1, s2, n):
    mu = s1 / np.maximum(n, 1); var = (s2 - n * mu ** 2) / np.maximum(n - 1, 1)
    with np.errstate(all="ignore"): t = np.where((n >= 2) & (var > 0), mu / np.sqrt(var / np.maximum(n, 1)), np.nan)
    return t
def scan(shift):
    idx = (AR - shift) % N; Ma = MABS[idx]; Sg = SGN[idx]
    res = np.zeros(6, int)
    for h in TG:
        A, zq, vm, allow = PREP[h]; A2 = A * A
        M = Ma & (Sg * zq[:, None] <= 0.25) & vm[:, None]
        Mf = M.astype(np.float64); Ms = Mf * Sg
        out = {}
        for nm, sl in (("IS", slice(0, iE)), ("OOS", slice(iE, N))):
            n = Mf[sl].sum(0); s1 = Ms[sl].T @ A[sl]; s2 = Mf[sl].T @ A2[sl]
            out[nm] = (n, tt(s1, s2, n))
        nI, tI = out["IS"]; nO, tO = out["OOS"]
        for k, sg in ((0, 1), (3, -1)):
            tIs = sg * tI; tOs = sg * tO
            sel = allow & (nI >= 40) & (tIs >= 3)
            sv = sel & (nO >= 2) & (tOs >= 2); sv20 = sv & (nO >= 20)
            res[k] += sel.sum(); res[k + 1] += sv.sum(); res[k + 2] += sv20.sum()
    return res
SH = np.random.RandomState(20261110).randint(250, N - 250, size=500)
real_ov = scan(0)
log("gercek (orrtusmeli) [selF,survF,surv20F,selR,survR,surv20R]:", real_ov.tolist())
null = []; tl = time.time()
for r in range(NREP):
    null.append(scan(int(SH[r])))
    if r == 4:
        per = (time.time() - tl) / 5; log(f"tekrar basina {per:.1f}s")
        if per * NREP > 840 and NREP > 100: NREP = 100; log("tekrar 100'e indirildi")
    if r + 1 >= NREP: break
null = np.array(null)
ks = pd.DataFrame(null, columns=["sec_ileri", "ayakta_ileri", "ayakta20_ileri", "sec_ters", "ayakta_ters", "ayakta20_ters"])
ks.insert(0, "tekrar", range(1, len(ks) + 1)); ks.loc[len(ks)] = [0] + real_ov.tolist()  # tekrar 0 = gercek (orrtusmeli)
ks.to_csv(EK + "kesif_sans_b3.csv", sep=";", index=False)
nullsum = {c: (float(np.median(ks[c][:-1])), float(np.percentile(ks[c][:-1], 95))) for c in ks.columns[1:]}
log("sans medyan/%95:", nullsum, "tekrar", len(null))

# ---------------- secilenler icin ek sinamalar
SHA = SH
IDXM = (AR[None, :] - SHA[:, None]) % N
def pkay(zL, zT, A):
    val = ~np.isnan(A); Af = np.where(val, A, 0.0); zq = np.nan_to_num(zT, nan=9.0)
    def stat(Z):
        d = np.sign(Z); m = (np.abs(Z) >= 1) & val & (d * zq <= 0.25); c = m.sum(-1)
        return np.where(c > 0, (m * d * Af).sum(-1) / np.maximum(c, 1), np.nan)
    z0 = np.nan_to_num(zL, nan=0.0); real = stat(z0[None, :])[0]; sm = stat(z0[IDXM]); sm = sm[~np.isnan(sm)]
    if np.isnan(real) or len(sm) == 0: return np.nan, np.nan
    return float((sm >= real).mean()), float((sm <= real).mean())  # ileri, ters
KS = {}
def kstat(h):
    T = TG[h]; zT = T["z"]; z = zT
    m = (z <= -1); m2 = z >= 1; d = np.where(z <= -1, 1.0, -1.0)
    ii, dd = chain(m | m2, d, T["A"][2], 0); return ii, dd
SEC_ROWS = []
KCACHE = {}
for h, c, yon, sg, ii, dd in SEL:
    T = TG[h]; j = leaders.index(c); zL = LZ[:, j]; zT = T["z"]; A2 = T["A"][2]; d = np.sign(zL)
    sigN = "S_KUL" if sg == 1 else "S_KUL_TERSYON"
    r = dict(hedef=h, oncu=c, yon=yon, isaret=sg)
    sI, sO = REAL[(h, c, yon)]
    sT = stats(ii, dd * sg, T, 0, PM["TAM"]); sS = stats(ii, dd * sg, T, 0, PM["SON2Y"]); s26 = stats(ii, dd * sg, T, 0, PM["Y2526"], full=False)
    for per, s_ in (("TAM", sT), ("SON2Y", sS), ("Y2526", s26)):
        if per != "Y2526" and s_["n"] > 0: rows.append(rowdict(h, c, sg, sigN, per, {k: s_.get(k) for k in fields}))
    sOF = stats(ii, dd * sg, T, 0, PM["OOS"])
    r.update(IS_n=sI["n"], IS_brut=sI["brut"], IS_t=sI["t"], OOS_n=sO["n"], OOS_brut=sO.get("brut"), OOS_t=sO.get("t"),
             oos_ayakta=int(sO["n"] >= 2 and sO["t"] >= 2), TAM_n=sT["n"], TAM_brut=sT["brut"], TAM_t=sT["t"],
             p_birincil=float(2 * st.t.sf(abs(sT["t"]), sT["n"] - 1)), q_fdr="",
             net_bir_TAM=sT["net_bireysel"], net_bir_SON2Y=sS.get("net_bireysel", np.nan), OOS_suruklenme=sOF.get("brut_suruklenme_duz", np.nan),
             TAM_ilk10haric=sT["brut_ilk10haric"], brut_2025_26=s26.get("brut", np.nan), brut_2025_26_n=s26["n"])
    # E2
    m = (np.abs(zL) >= 1) & ~np.isnan(zT) & (d * zT <= 0.25)
    i2, d2 = chain(m, d, A2, 1)
    e2T = stats(i2, d2 * sg, T, 1, PM["TAM"], full=False); e2O = stats(i2, d2 * sg, T, 1, PM["OOS"], full=False)
    r.update(E2_TAM_brut=e2T.get("brut", np.nan), E2_OOS_brut=e2O.get("brut", np.nan), E2_OOS_t=e2O.get("t", np.nan), E2_OOS_n=e2O["n"])
    # S_ONCU
    io, do = chain(np.abs(zL) >= 1, d, A2, 0)
    oT = stats(io, do * sg, T, 0, PM["TAM"], full=False); oO = stats(io, do * sg, T, 0, PM["OOS"], full=False)
    r.update(ONCU_TAM_brut=oT.get("brut", np.nan), ONCU_OOS_brut=oO.get("brut", np.nan), ONCU_OOS_t=oO.get("t", np.nan))
    # S_KENDI (hedef bazinda; yon gozetmez)
    if h not in KCACHE:
        ik, dk = kstat(h); KCACHE[h] = (stats(ik, dk, T, 0, PM["OOS"], full=False), stats(ik, dk, T, 0, PM["TAM"], full=False))
    r.update(KENDI_OOS_brut=KCACHE[h][0].get("brut", np.nan), KENDI_OOS_n=KCACHE[h][0]["n"], KENDI_TAM_brut=KCACHE[h][1].get("brut", np.nan))
    # BAZSIZ
    mb = m & ~np.isnan(T["zb"]) & (T["zb"] < 1)
    ib, db_ = chain(mb, d, A2, 0)
    bO = stats(ib, db_ * sg, T, 0, PM["OOS"], full=False); bT = stats(ib, db_ * sg, T, 0, PM["TAM"], full=False)
    r.update(BAZSIZ_OOS_brut=bO.get("brut", np.nan), BAZSIZ_OOS_n=bO["n"], BAZSIZ_TAM_brut=bT.get("brut", np.nan))
    # KATI_1730
    zLK = ezk(c); zTK = ezk(h + ".IS")
    if zLK is not None and zTK is not None:
        dK = np.sign(zLK); mK = (np.abs(zLK) >= 1) & ~np.isnan(zTK) & (dK * zTK <= 0.25) & PM["KWIN"]
        ik, dk = chain(mK, dK, A2, 0); kk = stats(ik, dk * sg, T, 0, PM["KWIN"], full=False)
        e0w = stats(ii, dd * sg, T, 0, PM["KWIN"], full=False)
        r.update(KATI_n=kk["n"], KATI_brut=kk.get("brut", np.nan), KATI_t=kk.get("t", np.nan), E0_KWIN_n=e0w["n"], E0_KWIN_brut=e0w.get("brut", np.nan))
    else: r.update(KATI_n=0, KATI_brut=np.nan, KATI_t=np.nan, E0_KWIN_n=0, E0_KWIN_brut=np.nan)
    pf, pt = pkay(zL, zT, A2); r["p_kaydir"] = pf if sg == 1 else pt
    # kriterler (FDR haric)
    f = {}
    f["n>=40"] = sT["n"] >= 40
    f["TAM_t>=2.5"] = sT["t"] >= 2.5
    f["net_bireysel>0 (TAM,SON2Y)"] = sT["net_bireysel"] > 0 and (sS["n"] > 0 and sS["net_bireysel"] > 0)
    f["OOS brut>0,t>=1.5"] = sO["n"] >= 2 and sO["brut"] > 0 and sO["t"] >= 1.5
    f["OOS suruklenme>0"] = r["OOS_suruklenme"] > 0
    f["E2>0,>=E0/3"] = (r["E2_TAM_brut"] > 0) and r["E2_TAM_brut"] >= sT["brut"] / 3
    f["ilk10 haric>0"] = sT["brut_ilk10haric"] > 0
    f["p_kaydir<=0.05"] = (not np.isnan(r["p_kaydir"])) and r["p_kaydir"] <= 0.05
    f["KATI>0,>=E0/2"] = (r["KATI_n"] > 0) and r["KATI_brut"] > 0 and r["KATI_brut"] >= 0.5 * r["E0_KWIN_brut"]
    kal = [k for k, v in f.items() if not bool(v)]
    r["n_kalan_olcut"] = len(kal)
    if len(kal) == 0: kr = "ADAY" if r["KATI_n"] >= 30 else "IZLE"
    elif len(kal) <= 2 and sT["t"] >= 2.0: kr = "IZLE"
    else: kr = "ELENDI"
    r["karar"] = kr; r["neden"] = "; ".join(kal) + ("; KATI n<30" if r["KATI_n"] < 30 else "") + " (FDR ana ajanda)"
    SEC_ROWS.append(r)
OZ = pd.DataFrame(SEC_ROWS)
OZ.to_csv(EK + "ozet_b3.csv", sep=";", index=False)
log("ozet yazildi", len(OZ))

# ---------------- havuz: IS'te secilenlerin OOS takvim zamani portfoyu
def pool(sel, per="OOS", sub=None):
    sm = np.zeros(N); ct = np.zeros(N)
    for h, c, yon, sg, ii, dd in sel:
        if sub is not None and (h, c, yon) not in sub: continue
        T = TG[h]; rf = np.nan_to_num(T["rf"], nan=0.0) * 1e4
        for i, d_ in zip(ii.tolist(), dd.tolist()):
            if not PM[per][i]: continue
            for k in (1, 2):
                if i + k < N: sm[i + k] += sg * d_ * rf[i + k]; ct[i + k] += 1
    msk = ct > 0; x = sm[msk] / ct[msk]
    if len(x) < 10: return dict(gun=len(x))
    mu = x.mean(); u = x - mu; Lg = 3; v = (u @ u) / len(x)
    for l in range(1, Lg + 1): v += 2 * (1 - l / (Lg + 1)) * (u[l:] @ u[:-l]) / len(x)
    return dict(gun=len(x), ort_gunluk_bps=mu, t_NW=mu / np.sqrt(v / len(x)), ort_esz_islem=ct[msk].mean())
HV = []
for yon in ("ILERI", "TERS"):
    ss = [s for s in SEL if s[2] == yon]
    HV.append(dict(kume="IS_secilenler_" + yon, **pool(ss)))
    sub = set((r["hedef"], r["oncu"], r["yon"]) for r in SEC_ROWS if r["oos_ayakta"] and r["yon"] == yon)
    HV.append(dict(kume="OOS_ayakta_" + yon, **pool(ss, sub=sub)))
pd.DataFrame(HV).to_csv(EK + "havuz_b3.csv", sep=";", index=False)

# ---------------- sinama: sahte onculer ve kalibrasyon
def pooled(sets):
    g = np.concatenate(sets) if sets else np.array([]); return len(g), g.mean(), tstat(g)
fk, rn = [], []; rg = np.random.RandomState(7)
for h, T in TG.items():
    zT = T["z"]; A2 = T["A"][2]
    zF = pd.Series(zT).shift(-1).values  # hedefin ertesi gun z'si
    for zz, bag in ((zF, fk), (rg.randn(N), rn)):
        d = np.sign(zz); m = (np.abs(zz) >= 1) & ~np.isnan(zT) & (d * zT <= 0.25)
        ii, dd = chain(m, d, A2, 0)
        if len(ii): bag.append(dd * A2[ii])
log("sahte(ertesi gun z):", pooled(fk), " gurultu:", pooled(rn))
T = TG["SAHOL"]; j = leaders.index("AKBNK.IS"); zL = LZ[:, j]; d = np.sign(zL)
m = (np.abs(zL) >= 1) & ~np.isnan(T["z"]) & (d * T["z"] <= 0.25); ii, dd = chain(m, d, T["A"][2], 0)
log("KALIBRASYON SAHOL<-AKBNK.IS:", stats(ii, dd, T, 0, PM["TAM"], full=False))

# ---------------- sonuc yaz
pd.DataFrame(rows).reindex(columns=["aile", "hedef", "oncu", "isaret", "zamanlama", "agirlik", "sinyal", "giris", "tutma", "donem", "n", "yillik_n"] + fields[1:]).to_csv(EK + "sonuc_b3.csv", sep=";", index=False)
if len(OZ):
    log("karar:", OZ.groupby(["yon", "karar"]).size().to_dict())
    log("oos_ayakta:", OZ.groupby("yon").oos_ayakta.sum().to_dict())
    for yon in ("ILERI", "TERS"):
        o = OZ[(OZ.yon == yon) & (OZ.oos_ayakta == 1)]
        log(yon, "ayakta hedef:", o.hedef.value_counts().head(8).to_dict(), "oncu:", o.oncu.value_counts().head(8).to_dict())
log("bitti")
