"""b1: YURTICI + VIOP_T ailelerinin backtesti (PLAN.md v2). python3 -I b1_yurtici.py"""
import os, sys, time, numpy as np, pandas as pd
from scipy.optimize import nnls
from scipy import stats as st
V = "/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri/panel/"
R0 = "/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/"
EK = R0 + "ek/"
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:5.0f}s]", *a, flush=True)

fr = pd.read_parquet(V + "fut_ret.parquet"); cal = pd.DatetimeIndex(fr.index).normalize(); N = len(cal)
fr.index = cal
def W(n): d = pd.read_parquet(V + n); d.index = cal; return d
FL, FT, FV, FC, FS = W("fut_limit.parquet"), W("fut_trades.parquet"), W("fut_value_tl.parquet"), W("fut_code.parquet"), W("fut_settle.parquet")
sp = pd.concat([pd.read_parquet(V + "spot_gunluk.parquet"), pd.read_parquet(V + "ek_b1_spot_AKGRT.parquet")])
sp["date"] = pd.to_datetime(sp["date"]).dt.normalize()
def pv(col): return sp.pivot_table(index="date", columns="sym", values=col, aggfunc="last").reindex(cal)
ADJ, CC, VV, HH, LL = pv("adj"), pv("c"), pv("v"), pv("h"), pv("l")
spl = pd.read_csv(V + "bolunme_gunleri.csv"); spl["date"] = pd.to_datetime(spl["date"]).dt.normalize()
SPLD = {}
for s_, g in spl.groupby("sym"): SPLD[s_] = set(g["date"])
sh = pd.concat([pd.read_parquet(V + "saatlik.parquet"), pd.read_parquet(V + "ek_b1_saatlik_SI.parquet")])
sh["d"] = sh["ts_utc"].dt.tz_convert("UTC").dt.tz_localize(None).dt.normalize()
sh["hm"] = sh["ts_utc"].dt.hour * 60 + sh["ts_utc"].dt.minute
UND = [c for c in fr.columns if c not in ("XU030", "XLBNK", "USDTRY", "XAUUSD", "XAGUSD", "XAUTRY")]
IDX = ("XU030.IS", "XBANK.IS", "XU100.IS")
YR = cal.year.values
MARJ_D = pd.Timestamp("2020-03-13")

# ---------------- spot getirileri
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
    _S[sym] = (r, exd, sym in IDX); return _S[sym]

def katir(sym):
    """KATI_1730 getirisi: ln(17:30 bilinen fiyat / onceki gun HAM kapanis)"""
    g = sh[sh["sym"] == sym]
    if len(g) == 0: return None
    pc = g.pivot_table(index="d", columns="hm", values="c", aggfunc="last").reindex(cal)
    for k in (750, 810, 870):
        if k not in pc.columns: pc[k] = np.nan
    p = pc[810].where(pc[870].notna(), pc[750])
    r = np.log(p / CC[sym].shift(1)) if sym in CC.columns else None
    s = srets(sym)
    if s is not None: r[s[1]] = np.nan
    if sym in IDX: r[r.abs() > 0.5] = np.nan
    else:
        m = pd.Series(np.where(cal < MARJ_D, 0.20, 0.10), index=cal); r[(r.abs() > np.log(1 + m + 0.005))] = np.nan
    return r
def katifut(sym):  # emtia 14:00 UTC (13:00 baslangic) / onceki BIST gunu
    g = sh[sh["sym"] == sym]
    if len(g) == 0: return None
    pc = g.pivot_table(index="d", columns="hm", values="c", aggfunc="last").reindex(cal)
    if 780 not in pc.columns: return None
    r = np.log(pc[780] / pc[780].shift(1)); r[r.abs() > 0.2] = np.nan; return r

def rolsd(x, w=120, mp=60): return x.rolling(w, min_periods=mp).std().shift(1)
_E = {}
def eres(sym):
    """dict r, e (artik), sig, sigr (ham sigma), eK, rK"""
    if sym in _E: return _E[sym]
    s = srets(sym)
    if s is None: _E[sym] = None; return None
    r, _, isidx = s; rm = srets("XU030.IS")[0]
    if sym == "XU030.IS": beta = None
    else: beta = r.rolling(250, min_periods=120).cov(rm) / rm.rolling(250, min_periods=120).var(); beta = beta.shift(1)
    e = r.copy() if beta is None else r - beta * rm
    d = {"r": r, "e": e, "sig": rolsd(e), "sigr": rolsd(r)}
    rK = katir(sym)
    if rK is not None:
        rmK = katir("XU030.IS")
        d["rK"] = rK; d["eK"] = rK.copy() if beta is None else rK - beta * rmK
    _E[sym] = d; return d

# ---------------- hedef
def hedef_info(h):
    if h in UND: return dict(sym=h + ".IS", mode="resid", proxy=False, cost=(8, 15))
    if h == "XU030": return dict(sym="XU030.IS", mode="raw", proxy=False, cost=(3, 3))
    if h == "XLBNK": return dict(sym="XBANK.IS", mode="resid", proxy=False, cost=(3, 3))
    return dict(sym=None, mode="fut", proxy=True, cost=(3, 3))
LIK = pd.read_csv("/home/user/Xxxx/raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv").set_index("und")["rt_cost_retail_bps"]
def retail(h):
    if h in UND: return float(LIK.get(h, 22)) if not pd.isna(LIK.get(h, np.nan)) else 22.0
    return 6.0 if h in ("XU030", "XLBNK") else 8.0

_T = {}
def tgt(h):
    if h in _T: return _T[h]
    hi = hedef_info(h); f = fr[h].copy()
    if h in ("XU030", "XLBNK"): f[f.abs() > 0.5] = np.nan
    if hi["sym"] and eres(hi["sym"]) is not None:
        E = eres(hi["sym"]); z = E["e"] / E["sig"]; zr = E["r"] / E["sigr"]; zK = None
        if "eK" in E: zK = E["eK"] / E["sig"]
        db = f - E["r"]; zb = (db / rolsd(db)).abs()
    elif hi["sym"] is None:
        z = f / rolsd(f); zr = z; zK = None; zb = None
    else: _T[h] = None; return None
    if hi["mode"] == "raw" and hi["sym"] == "XU030.IS": z = zr
    ok = (FT[h] >= 20) & (FV[h] >= 1e6) & (FL[h] != 1)
    fa = f.values; okv = ok.values
    cs = np.concatenate([[0], np.nancumsum(fa)]); nn = np.concatenate([[0], np.cumsum(np.isnan(fa))])
    codes = FC[h].values; chg = np.zeros(N, bool); chg[1:] = codes[1:] != codes[:-1]
    cc = np.concatenate([[0], np.cumsum(chg)])
    A, ROLL = {}, {}
    for hh in (1, 2, 3):
        a = np.full(N, np.nan); rl = np.zeros(N, bool)
        for i in range(N - hh):
            if okv[i] and okv[i + hh] and nn[i + hh + 1] - nn[i + 1] == 0:
                a[i] = (cs[i + hh + 1] - cs[i + 1]) * 1e4; rl[i] = (cc[i + hh + 1] - cc[i + 1]) > 0
        A[hh] = a; ROLL[hh] = rl
    drift = pd.Series(fa, index=cal).groupby(YR).mean()
    dr = np.array([drift.get(y, 0.0) for y in YR]) * 1e4
    o = dict(hi=hi, f=f, z=z.values, zr=zr.values, zK=None if zK is None else zK.values, zb=None if zb is None else zb.values, A=A, ROLL=ROLL, dr=dr,
             retail=retail(h), cost=hi["cost"], rf=f.values)
    _T[h] = o; return o

# ---------------- oncu
def ncomp_weights(tsym, comps):
    y = srets(tsym)[0].values; X = np.column_stack([srets(c)[0].values for c in comps]); k = len(comps)
    Wt = np.full((N, k), np.nan)
    for t in range(120, N):
        a = max(0, t - 250); yy = y[a:t]; XX = X[a:t]
        m = ~np.isnan(yy)
        if m.sum() < 100: continue
        XX = np.nan_to_num(XX[m]); yy = yy[m]
        good = (~np.isnan(X[a:t][m])).sum(0) >= 100
        w = np.zeros(k)
        if good.sum() == 0: continue
        wg, _ = nnls(XX[:, good], yy); w[good] = wg
        w = w / w.sum() if w.sum() > 0 else good / good.sum()
        Wt[t] = w
    return Wt
def basket(comps, key, Wt=None, sigkey="e"):
    cols = np.column_stack([eres(c)[key].values for c in comps]); av = ~np.isnan(cols)
    if Wt is None: w = np.ones_like(cols) / len(comps)
    else: w = np.nan_to_num(Wt)
    ww = w * av; den = ww.sum(1)
    out = np.where((av.sum(1) >= len(comps) / 2) & (den > 0), np.nansum(np.nan_to_num(cols) * ww, 1) / np.where(den > 0, den, 1), np.nan)
    return out
def zof(x): x = pd.Series(x, index=cal); return x.values, rolsd(x).values

def leader_z(spec, rho, Wt, mode_raw=False):
    """returns zL, zLK, zLraw (hepsi dizi)"""
    if spec.startswith("VIOP:"):
        u = spec[5:]; r = fr[u].copy()
        if u in ("XU030", "XLBNK"): r[r.abs() > 0.5] = np.nan
        if u == "USDTRY": r = r - r.rolling(20, min_periods=15).mean().shift(1)
        z = (r / rolsd(r)).values
        kmap = {"XAUUSD": "GC=F", "XAGUSD": "SI=F"}
        zK = None
        if u in kmap: rk = katifut(kmap[u])
        elif u == "XU030": rk = katir("XU030.IS")
        elif u == "XLBNK": rk = katir("XBANK.IS")
        else: rk = None
        if rk is not None: zK = (rk / rolsd(r)).values
        return z, zK, z
    comps = spec.split("+")
    if any(eres(c) is None for c in comps): return None
    raw = mode_raw
    if len(comps) == 1:
        E = eres(comps[0]); e = E["r"] if raw else E["e"]; sg = E["sigr"] if raw else E["sig"]
        zK = None
        if "eK" in E: zK = ((E["rK"] if raw else E["eK"]) / sg).values
        zr = (E["r"] / E["sigr"]).values
        return (e / sg).values, zK, zr
    key = "r" if raw else "e"
    e = basket(comps, key, Wt); z = zof(e); zL = e / z[1]
    zK = None
    if all("eK" in eres(c) for c in comps):
        eK = basket(comps, "rK" if raw else "eK", Wt); zK = eK / z[1]
    er = basket(comps, "r", Wt); zr = er / zof(er)[1]
    return zL, zK, zr

# ---------------- cift listesi
cs_ = pd.read_csv(EK + "ciftler_onkayit.csv", sep=";")
FAM = ("F1_GRUP", "F1_KONTROL", "F2_SEKTOR", "F4_MAKRO", "F5_VIOP", "F5_OZDESLIK")
cs_ = cs_[cs_["aile"].isin(FAM) & cs_["zaman"].isin(["YURTICI", "VIOP_T"])].reset_index(drop=True)
pairs, atlanan = [], []
for _, r in cs_.iterrows():
    comps = r["oncu"].split("+")
    base = dict(aile=r["aile"], hedef=r["hedef"], oncu=r["oncu"], rho=int(r["isaret"]), zaman=r["zaman"])
    if r["aile"] == "F1_GRUP" and len(comps) >= 3:
        pairs.append(dict(base, agirlik="REG")); pairs.append(dict(base, agirlik="ESIT"))
    else: pairs.append(dict(base, agirlik="TEK" if len(comps) == 1 else "ESIT"))
for h in UND:
    pairs.append(dict(aile="PIYASA", hedef=h, oncu="XU030.IS", rho=1, zaman="YURTICI", agirlik="TEK"))
pairs.append(dict(aile="F5_OZDESLIK", hedef="XAUTRY", oncu="OZDESLIK_s", rho=1, zaman="VIOP_T", agirlik="TEK"))
log("cift:", len(pairs))

# ---------------- motor
PER = {"TAM": (pd.Timestamp("2017-03-01"), pd.Timestamp("2026-12-31"), 9.68), "IS": (pd.Timestamp("2017-01-01"), pd.Timestamp("2021-12-31"), 5.0),
       "OOS": (pd.Timestamp("2022-01-01"), pd.Timestamp("2026-12-31"), 4.86), "SON2Y": (pd.Timestamp("2024-11-10"), pd.Timestamp("2026-12-31"), 2.0),
       "2020+": (pd.Timestamp("2020-01-01"), pd.Timestamp("2026-12-31"), 6.86)}
PMASK = {k: ((cal >= a) & (cal <= b)) for k, (a, b, _) in PER.items()}
def select(idx, dirs, T, h, s):
    A = T["A"][h]; out = []; last = -1
    for i, d in zip(idx, dirs):
        e = i + s
        if e >= N or e < last: continue
        if np.isnan(A[e]): continue
        out.append((i, d)); last = e + h
    return out
def tstat(x):
    n = len(x)
    if n < 2: return np.nan
    sd = np.std(x, ddof=1); return np.mean(x) / (sd / np.sqrt(n)) if sd > 0 else np.nan
def stat_rows(tr, T, h, s, pm):
    """tr: liste (i,d). pm: periyot maskesi. -> dict"""
    sel = [(i, d) for i, d in tr if pm[i]]
    n = len(sel)
    if n == 0: return dict(n=0)
    ii = np.array([i for i, _ in sel]); dd = np.array([d for _, d in sel], float)
    A = T["A"][h]; g = dd * A[ii + s]; rl = T["ROLL"][h][ii + s]
    dr = g - dd * h * T["dr"][ii]
    c8, c15 = T["cost"]; cr = T["retail"]
    net = lambda c: np.mean(g - c * (1 + rl))
    gs = np.sort(g)[::-1]; g10 = gs[10:] if n > 10 else np.array([])
    yy = pd.Series(g).groupby(YR[ii]).mean()
    return dict(n=n, brut=g.mean(), net8=net(c8), net15=net(c15), net_bireysel=net(cr), t=tstat(g), isabet=(g > 0).mean(), medyan=np.median(g),
                brut_ilk10haric=g10.mean() if len(g10) else np.nan, t_ilk10haric=tstat(g10) if len(g10) > 1 else np.nan,
                poz_yil=int((yy > 0).sum()), yil_say=len(yy), brut_suruklenme_duz=dr.mean(), uzun_pay=(dd > 0).mean(), roll_sayi=int(rl.sum()))
def sigs(zL, zT, rho, zr_L, zr_T, zb):
    d = rho * np.sign(zL); aL = np.abs(zL) >= 1; dz = d * zT
    ok = ~np.isnan(zL) & ~np.isnan(zT)
    kul = aL & ok & (dz <= 0.25)
    S = {"S_KUL": (kul, d), "S_KUL_YATAY": (kul & (dz >= -0.5), d), "S_KUL_TERS": (aL & ok & (dz < -0.5), d),
         "S_ONCU": (aL & ~np.isnan(zL), d), "S_IKISI": (aL & ok & (dz > 0.25), d)}
    if zb is not None: S["S_KUL_BAZSIZ"] = (kul & ~np.isnan(zb) & (zb < 1), d)
    dh = rho * np.sign(zr_L); okh = ~np.isnan(zr_L) & ~np.isnan(zr_T)
    S["S_HAM"] = (okh & (np.abs(zr_L) >= 1) & (dh * zr_T <= 0.25), dh)
    return S
rng_sh = np.random.RandomState(20261110)
SHIFTS = rng_sh.randint(250, N - 250, size=500)
def pkaydir(zL, zT, rho, T, s, kind):
    A = T["A"][2]; As = np.full(N, np.nan); As[:N - s] = A[s:]
    val = ~np.isnan(As); Af = np.where(val, As, 0.0)
    def stat(Z):
        d = rho * np.sign(Z); m = (np.abs(Z) >= 1) & val
        if kind == "S_KUL": m = m & (d * zT <= 0.25) & ~np.isnan(zT)
        c = m.sum(-1); return np.where(c > 0, (m * d * Af).sum(-1) / np.maximum(c, 1), np.nan), c
    z0 = np.nan_to_num(zL, nan=0.0); Z = np.nan_to_num(zL, nan=0.0)
    real, c0 = stat(z0[None, :])
    if c0[0] == 0: return np.nan
    idx = (np.arange(N)[None, :] - SHIFTS[:, None]) % N
    sm, _ = stat(z0[idx])
    sm = sm[~np.isnan(sm)]
    return float((sm >= real[0]).mean()) if len(sm) else np.nan

ROWS, TR, POOL, META = [], {}, {}, {}
def run_set(pid, p, T, name, zL, zT, rho, S, giris_list, sigset, mainperiods=True):
    for sg in sigset:
        if sg not in S: continue
        mask, d = S[sg]; idx = np.where(mask)[0]; dirs = d[idx]
        for gi in giris_list:
            s = 1 if gi == "E2" else 0
            for h in (1, 2, 3):
                tr = select(idx, dirs, T, h, s)
                TR[(pid, sg, gi, h)] = tr
                for pn, pm in PMASK.items():
                    if gi == "KATI" and pn == "IS": continue
                    r = stat_rows(tr, T, h, s, pm)
                    if r["n"] == 0: continue
                    r.update(aile=p["aile"], hedef=p["hedef"], oncu=p["oncu"], isaret=p["rho"], zamanlama=p["zaman"], agirlik=p["agirlik"], sinyal=sg, giris=gi, tutma=h, donem=pn,
                             yillik_n=r["n"] / PER[pn][2])
                    ROWS.append(r)
                # havuz (E0 / ana giris) icin gunluk toplama
                if gi in ("E0", "E2") and sg in ("S_KUL", "S_ONCU", "S_IKISI", "S_KUL_YATAY", "S_KUL_TERS") and name == "main":
                    pass
log("kuruluyor")
Wcache = {}
t_f = {}
for pid, p in enumerate(pairs):
    T = tgt(p["hedef"])
    if T is None: atlanan.append((pid, p["hedef"], "hedef spot yok")); continue
    ro = None
    spec = p["oncu"]
    Wt = None
    if p["agirlik"] == "REG":
        comps = spec.split("+")
        if any(eres(c) is None for c in comps) or srets(p["hedef"] + ".IS") is None: atlanan.append((pid, spec, "bilesen veri yok")); continue
        key = (p["hedef"], spec)
        if key not in Wcache: Wcache[key] = ncomp_weights(p["hedef"] + ".IS", comps)
        Wt = Wcache[key]
    if p["aile"] == "PIYASA":
        zl = leader_z("XU030.IS", 1, None, mode_raw=True); zT = T["zr"]; zTK = None
        zL, zLK, zLr = zl
        E = eres(p["hedef"] + ".IS"); zTK = (E["rK"] / E["sigr"]).values if "rK" in E else None
        zT_use = T["zr"]; zr_T = T["zr"]
    elif spec == "OZDESLIK_s":
        ss = np.log(FS["XAUTRY"]) - np.log(FS["XAUUSD"] * FS["USDTRY"] / 31.1035)
        xx = ss - ss.rolling(20, min_periods=15).mean().shift(1); zz = (xx / rolsd(xx)).values
        zL = -zz; zLK = None; zLr = zL; zT_use = T["z"]; zTK = None; zr_T = T["zr"]
    else:
        zl = leader_z(spec, p["rho"], Wt)
        if zl is None: atlanan.append((pid, spec, "oncu veri yok")); continue
        zL, zLK, _ = zl; zLr = leader_z(spec, p["rho"], Wt, mode_raw=True)[2]
        zT_use = T["z"]; zTK = T["zK"]; zr_T = T["zr"]
    p["vekilsiz"] = int(T["hi"]["proxy"] or p["oncu"].startswith("VIOP:") and T["hi"]["proxy"])
    usd = spec == "VIOP:USDTRY"
    gl = ["E2"] if False else ["E0", "E2"]
    S = sigs(zL, zT_use, p["rho"], zLr, zr_T, T["zb"])
    kendi_mask = (np.abs(T["z"] if p["aile"] != "PIYASA" else T["zr"]) >= 1) & ~np.isnan(T["z"] if p["aile"] != "PIYASA" else T["zr"])
    zk = T["z"] if p["aile"] != "PIYASA" else T["zr"]
    S["S_KENDI"] = (kendi_mask, -np.sign(zk))
    run_set(pid, p, T, "main", zL, zT_use, p["rho"], S, gl, list(S.keys()))
    if zLK is not None and zTK is not None and not usd:
        SK = sigs(zLK, zTK, p["rho"], zLr, zr_T, None)
        run_set(pid, p, T, "kati", zLK, zTK, p["rho"], {k: v for k, v in SK.items() if k in ("S_KUL", "S_ONCU")}, ["KATI"], ["S_KUL", "S_ONCU"])
        META[pid] = dict(zLK=zLK, zTK=zTK)
    # p_kaydir ve sapma
    s_ana = 1 if usd else 0
    META.setdefault(pid, {})
    META[pid].update(pk_kul=pkaydir(zL, zT_use, p["rho"], T, s_ana, "S_KUL"), pk_oncu=pkaydir(zL, zT_use, p["rho"], T, s_ana, "S_ONCU"), zL=zL, zT=zT_use, S=S)
    # havuz
    for sg in ("S_KUL", "S_ONCU", "S_IKISI", "S_KUL_YATAY", "S_KUL_TERS"):
        if sg not in S: continue
        gi = "E2" if usd else "E0"; sft = 1 if usd else 0
        for h in (1, 2, 3):
            tr = TR[(pid, sg, gi, h)]
            key = (p["aile"], sg, h)
            if key not in POOL: POOL[key] = [np.zeros(N), np.zeros(N)]
            f = T["rf"]
            for i, d in tr:
                e = i + sft
                POOL[key][0][e + 1:e + h + 1] += d * f[e + 1:e + h + 1] * 1e4
                POOL[key][1][e + 1:e + h + 1] += 1
    if pid % 20 == 0: log("cift", pid, p["aile"], p["hedef"], p["oncu"][:30])
log("tarama bitti, satir", len(ROWS))
sonuc = pd.DataFrame(ROWS)
cols = "aile;hedef;oncu;isaret;zamanlama;agirlik;sinyal;giris;tutma;donem;n;yillik_n;brut;net8;net15;net_bireysel;t;isabet;medyan;brut_ilk10haric;t_ilk10haric;poz_yil;yil_say;brut_suruklenme_duz;uzun_pay".split(";")
sonuc = sonuc[cols + ["roll_sayi"]]
sonuc.to_csv(EK + "sonuc_b1.csv", sep=";", index=False, float_format="%.4f")

# ---------------- ozet ve karar
def getrow(p, sg, gi, h, per):
    m = sonuc[(sonuc.aile == p["aile"]) & (sonuc.hedef == p["hedef"]) & (sonuc.oncu == p["oncu"]) & (sonuc.agirlik == p["agirlik"]) & (sonuc.sinyal == sg) & (sonuc.giris == gi) & (sonuc.tutma == h) & (sonuc.donem == per)]
    return m.iloc[0] if len(m) else None
oz = []
for pid, p in enumerate(pairs):
    if pid not in META or "pk_kul" not in META[pid]: continue
    sub = sonuc[(sonuc.aile == p["aile"]) & (sonuc.hedef == p["hedef"]) & (sonuc.oncu == p["oncu"]) & (sonuc.agirlik == p["agirlik"])]
    for sg, pk in (("S_KUL", META[pid]["pk_kul"]), ("S_ONCU", META[pid]["pk_oncu"])):
        usd = p["oncu"] == "VIOP:USDTRY"; ga = "E2" if usd else "E0"
        g = lambda gi, per, h=2, sg=sg: getrow(p, sg, gi, h, per)
        tam, oos, s2, e2, e0 = g(ga, "TAM"), g(ga, "OOS"), g(ga, "SON2Y"), g("E2", "TAM"), g("E0", "TAM")
        kt = g("KATI", "TAM")
        rowd = dict(aile=p["aile"], hedef=p["hedef"], oncu=p["oncu"], isaret=p["rho"], zaman=p["zaman"], agirlik=p["agirlik"], sinyal=sg, giris_ana=ga, vekilsiz=T_v if (T_v := int(hedef_info(p["hedef"])["proxy"])) else 0)
        if tam is None: rowd.update(n=0, karar="ELENDİ", neden="işlem yok"); oz.append(rowd); continue
        Tg = tgt(p["hedef"])
        n = int(tam["n"]); t = tam["t"]
        pb = 2 * (1 - st.t.cdf(abs(t), n - 1)) if n > 2 and not np.isnan(t) else np.nan
        # KATI ayni donem E0
        kn = int(kt["n"]) if kt is not None else 0
        kbrut = kt["brut"] if kt is not None else np.nan
        e0same = np.nan
        if kt is not None:
            trs = TR[(pid, sg, ga, 2)]; k0 = pd.Timestamp("2023-11-09")
            s_ = 1 if usd else 0
            gg = np.array([d * Tg["A"][2][i + s_] for i, d in trs if cal[i] >= k0])
            e0same = gg.mean() if len(gg) else np.nan
        crit = {}
        crit["n>=40"] = n >= 40; crit["t>=2.5"] = (not np.isnan(t)) and t >= 2.5
        crit["net_bir_TAM_SON2Y>0"] = tam["net_bireysel"] > 0 and (s2 is not None and s2["net_bireysel"] > 0)
        crit["OOS_brut>0_t>=1.5"] = oos is not None and oos["brut"] > 0 and oos["t"] >= 1.5
        crit["OOS_suruk>0"] = oos is not None and oos["brut_suruklenme_duz"] > 0
        if usd: crit["E2_kriteri"] = True
        else: crit["E2>0_ve>=E0/3"] = e2 is not None and e2["brut"] > 0 and e2["brut"] >= tam["brut"] / 3
        crit["ilk10_haric>0"] = not np.isnan(tam["brut_ilk10haric"]) and tam["brut_ilk10haric"] > 0
        pkv = pk; crit["p_kaydir<=0.05"] = (not np.isnan(pkv)) and pkv <= 0.05
        kati_cap = False
        if not usd:
            crit["KATI"] = kt is not None and kbrut > 0 and (not np.isnan(e0same)) and kbrut >= e0same / 2
            if kn < 30: kati_cap = True
        fails = [k for k, v in crit.items() if not v]
        if not fails: karar = "İZLE" if kati_cap else "ADAY"
        elif len(fails) <= 2 and t >= 2.0: karar = "İZLE"
        else: karar = "ELENDİ"
        neden = "; ".join(fails) + ("; KATI n<30 (en çok İZLE)" if kati_cap else "") + "; FDR ana ajanda"
        rowd.update(n=n, brut_tam=tam["brut"], t_tam=t, p_birincil=pb, net_bireysel_tam=tam["net_bireysel"], net_bireysel_son2y=s2["net_bireysel"] if s2 is not None else np.nan,
                    oos_brut=oos["brut"] if oos is not None else np.nan, oos_t=oos["t"] if oos is not None else np.nan, oos_suruk=oos["brut_suruklenme_duz"] if oos is not None else np.nan,
                    e0_brut=e0["brut"] if e0 is not None else np.nan, e2_brut=e2["brut"] if e2 is not None else np.nan, ilk10_haric=tam["brut_ilk10haric"],
                    p_kaydir=pkv, kati_n=kn, kati_brut=kbrut, kati_e0_ayni_donem=e0same, q_fdr="", karar=karar, neden=neden)
        for k, v in crit.items(): rowd["g_" + k] = int(v)
        oz.append(rowd)
ozet = pd.DataFrame(oz); ozet.to_csv(EK + "ozet_b1.csv", sep=";", index=False, float_format="%.4f")
log("ozet", ozet.groupby(["aile", "sinyal", "karar"]).size().to_string())

# ---------------- havuz
def nw(x, L):
    x = x - x.mean(); n = len(x); v = (x @ x) / n
    for l in range(1, L + 1): v += 2 * (1 - l / (L + 1)) * (x[l:] @ x[:-l]) / n
    return x.mean() if False else np.sqrt(v / n)
hv = []
def series(key):
    a, c = POOL[key]; m = c > 0; return pd.Series(np.where(m, a / np.where(m, c, 1), np.nan), index=cal)
def hrow(name, sg, h, s):
    s = s.dropna()
    if len(s) < 30: return
    se = nw(s.values, h + 1); hv.append(dict(aile=name, sinyal=sg, tutma=h, n_gun=len(s), brut_gunluk_bps=s.mean(), t_nw=s.mean() / se if se > 0 else np.nan, yillik_bps=s.mean() * 252))
fams = sorted({k[0] for k in POOL})
for f in fams:
    for sg in ("S_KUL", "S_ONCU", "S_IKISI", "S_KUL_YATAY", "S_KUL_TERS"):
        for h in (1, 2, 3):
            if (f, sg, h) in POOL: hrow(f, sg, h, series((f, sg, h)))
    for h in (1, 2, 3):
        for a, b in (("S_KUL", "S_IKISI"), ("S_KUL_YATAY", "S_KUL_TERS")):
            if (f, a, h) in POOL and (f, b, h) in POOL:
                sa, sb = series((f, a, h)), series((f, b, h)); dif = (sa - sb).dropna(); hrow(f, a + "-" + b, h, dif)
main_f = [f for f in fams if f in ("F1_GRUP", "F2_SEKTOR", "F4_MAKRO", "F5_VIOP")]
for sg in ("S_KUL", "S_ONCU", "S_IKISI", "S_KUL_YATAY", "S_KUL_TERS"):
    for h in (1, 2, 3):
        a = sum(POOL[(f, sg, h)][0] for f in main_f if (f, sg, h) in POOL); c = sum(POOL[(f, sg, h)][1] for f in main_f if (f, sg, h) in POOL)
        POOL[("TOPLAM", sg, h)] = [a, c]; hrow("TOPLAM(F1,F2,F4,F5)", sg, h, series(("TOPLAM", sg, h)))
for h in (1, 2, 3):
    for a_, b_ in (("S_KUL", "S_IKISI"), ("S_KUL_YATAY", "S_KUL_TERS")):
        dif = (series(("TOPLAM", a_, h)) - series(("TOPLAM", b_, h))).dropna(); hrow("TOPLAM(F1,F2,F4,F5)", a_ + "-" + b_, h, dif)
pd.DataFrame(hv).to_csv(EK + "havuz_b1.csv", sep=";", index=False, float_format="%.4f")
log("havuz", len(hv))

# ---------------- islemler (ADAY / IZLE)
il = []
for _, r in ozet[ozet.karar.isin(["ADAY", "İZLE"])].iterrows():
    pid = [i for i, p in enumerate(pairs) if p["aile"] == r.aile and p["hedef"] == r.hedef and p["oncu"] == r.oncu and p["agirlik"] == r.agirlik][0]
    T = tgt(r.hedef); s = 1 if r.giris_ana == "E2" else 0
    for i, d in TR[(pid, r.sinyal, r.giris_ana, 2)]:
        e = i + s
        il.append(dict(cift=f"{r.hedef}<-{r.oncu}", sinyal=r.sinyal, giris_tarihi=cal[e].date(), yon=int(d), z_L=META[pid]["zL"][i], z_T=META[pid]["zT"][i], cikis_tarihi=cal[min(e + 2, N - 1)].date(), brut_bps=d * T["A"][2][e], roll=int(T["ROLL"][2][e])))
pd.DataFrame(il).to_csv(EK + "islemler_b1.csv", sep=";", index=False, float_format="%.4f")

# ---------------- kalibrasyon ve sahte oncu sinamasi
cal_row = sonuc[(sonuc.hedef == "SAHOL") & (sonuc.oncu == "AKBNK.IS") & (sonuc.aile == "F1_GRUP") & (sonuc.sinyal == "S_KUL") & (sonuc.giris == "E0") & (sonuc.tutma == 2) & (sonuc.donem == "TAM")]
log("KALIBRASYON SAHOL<-AKBNK.IS:", cal_row[["n", "brut", "t"]].to_dict("records"))
rs = np.random.RandomState(7)
def fake(kind, nrep):
    res = []
    for h in sorted({p["hedef"] for p in pairs if p["aile"] in ("F2_SEKTOR", "F1_GRUP") and hedef_info(p["hedef"])["sym"] and p["hedef"] in UND}):
        T = tgt(h)
        if T is None: continue
        for k in range(nrep):
            if kind == "ertesi": zL = np.concatenate([T["z"][1:], [np.nan]])
            else: zL = rs.randn(N)
            S = sigs(zL, T["z"], 1, zL, T["zr"], None); m, d = S["S_KUL"]; idx = np.where(m)[0]
            tr = select(idx, d[idx], T, 2, 0)
            res += [x * T["A"][2][i] for i, x in tr]
            if kind == "ertesi": break
    res = np.array(res); return len(res), res.mean(), tstat(res)
log("SAHTE ertesi-gun oncu (n, ort bps, t):", fake("ertesi", 1))
log("SAHTE gurultu oncu (n, ort bps, t; 20 tekrar havuz):", fake("gurultu", 20))
for sd in (11,12,13):
    rs = np.random.RandomState(sd); log("SAHTE gurultu tek tekrar seed", sd, fake("gurultu", 1))
log("atlanan:", atlanan)
