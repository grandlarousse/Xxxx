"""C1, C2: Çin/HK orijinal endeks vs ABD ETF vekili sadakati + BIST tarafı. C6: TIO=F ay içi oynaklık çöküşü."""
import json, os, numpy as np, pandas as pd
from vcore import *

def sina_idx(code):
    d = pd.read_parquet(f"{S}/data_cin/sina_idx/{code}.parquet")
    s = pd.Series(d["c"].astype(float).values, index=pd.to_datetime(d["ldate"].astype(str)))
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s[s > 0]

def local(sym):
    return px(sym, "adj")

def weekly(p):
    return np.log(p.resample("W-FRI").last().dropna()).diff().dropna()

def fid(o, a, start="2014-01-01"):
    P = pd.concat([o.rename("o"), a.rename("a")], axis=1, join="inner").dropna()
    P = P[P.index >= start]
    R = np.log(P).diff().dropna()
    res = {"n_d": len(R), "start": str(P.index[0].date())}
    res["sync"] = R.o.corr(R.a)
    res["alt_t_orig_t+1"] = R.a.corr(R.o.shift(-1))
    res["orig_t_alt_t+1"] = R.o.corr(R.a.shift(-1))
    P2 = P.iloc[::2]; R2 = np.log(P2).diff().dropna(); res["2g"] = R2.o.corr(R2.a)
    W = np.log(P.resample("W-FRI").last().dropna()).diff().dropna()
    res["n_w"] = len(W); res["haft"] = W.o.corr(W.a)
    for w, (x, y) in WIN.items():
        ww = W.loc[x:y]; res[f"haft_{w}"] = ww.o.corr(ww.a) if len(ww) > 20 else np.nan
    yr = W.groupby(W.index.year).apply(lambda g: g.o.corr(g.a) if len(g) > 20 else np.nan)
    res["yil_min"] = yr.min(); res["yil_min_yil"] = int(yr.idxmin()); res["yil>=0.80"] = f"{int((yr >= 0.8).sum())}/{int(yr.notna().sum())}"
    # haftalık beta (alt ~ orig)
    res["beta_w"] = np.cov(W.a, W.o)[0, 1] / W.o.var()
    # bağımsız haftalandırma (inner join yok): her seri kendi son kapanışı
    Wo, Wa = weekly(o[o.index >= start]), weekly(a[a.index >= start])
    J = pd.concat([Wo, Wa], axis=1, join="inner").dropna(); res["haft_noinner"] = J.iloc[:, 0].corr(J.iloc[:, 1])
    return res, yr

out = []
log = open(f"{OUT}/v1_cin.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n"); log.flush()

# ---- veri kontrolü: Sina SSE vs Yahoo 000001.SS
ss_s = sina_idx("sh000001"); ss_y = local("000001.SS")
J = pd.concat([ss_s, ss_y], axis=1, join="inner").dropna(); RJ = np.log(J).diff().dropna()
P("Sina sh000001 vs Yahoo 000001.SS günlük r:", round(RJ.iloc[:, 0].corr(RJ.iloc[:, 1]), 5), "n", len(RJ),
  "| seviye medyan oran", round((J.iloc[:, 0] / J.iloc[:, 1]).median(), 5), "| |fark|>%0,5 gün oranı", round(((RJ.iloc[:, 0] - RJ.iloc[:, 1]).abs() > 0.005).mean(), 4))
y300 = raw("000300.SS"); P("Yahoo 000300.SS satır sayısı:", len(y300), "(tek satır -> Sina gerekli)")

ORIG = {"CSI300(sina)": sina_idx("sh000300"), "SSE(sina)": ss_s, "SSE(yahoo)": ss_y, "SZSE(sina)": sina_idx("sz399001"),
        "HSI": local("^HSI"), "HSCEI": local("^HSCE")}
PAIRS = {"CSI300(sina)": ["ASHR", "KBA", "CNYA"], "SSE(sina)": ["ASHR", "CNYA", "KBA"], "SSE(yahoo)": ["ASHR", "CNYA", "KBA"],
         "SZSE(sina)": ["CNXT", "ASHR"], "HSI": ["FXI", "MCHI", "EWH"], "HSCEI": ["FXI", "MCHI", "EWH"]}
yrs = {}
for o, alts in PAIRS.items():
    for a in alts:
        r, yr = fid(ORIG[o], local(a)); r.update(orig=o, alt=a); out.append(r); yrs[(o, a)] = yr
        P(f"{o:14s} {a:5s} start {r['start']} n_d {r['n_d']} sync {r['sync']:.3f} alt->o(t+1) {r['alt_t_orig_t+1']:.3f} 2g {r['2g']:.3f} "
          f"haft {r['haft']:.3f} (IS {r['haft_IS']:.3f} OOS {r['haft_OOS']:.3f} 3y {r['haft_3y']:.3f} 1y {r['haft_1y']:.3f}) noinner {r['haft_noinner']:.3f} "
          f"yıl-min {r['yil_min']:.2f}({r['yil_min_yil']}) yıl>=0,80 {r['yil>=0.80']} beta_w {r['beta_w']:.2f}")
F = pd.DataFrame(out); F.to_csv(f"{OUT}/c1c2_fidelity.csv", index=False)
pd.DataFrame(yrs).to_csv(f"{OUT}/c1c2_fidelity_by_year.csv")

# ---- BIST tarafı: XU100 / XU030 haftalık korelasyon: orijinal vs vekil, EEM + USDTRY kontrollü
P("\nBIST tarafı (haftalık, Cuma-Cuma; XU100 TL ve USD bazlı; kısmi = EEM+USDTRY kontrollü)")
xu = px("XU100.IS", "c"); usd = px("TRY=X", "c"); eem = px("EEM", "adj"); es = px("ES=F", "c")
def wk(s): return np.log(s.resample("W-FRI").last()).diff()
W = pd.DataFrame({"XU100": wk(xu), "USDTRY": wk(usd), "EEM": wk(eem), "ES": wk(es)})
W["XU100usd"] = W.XU100 - W.USDTRY
rows = []
for nm, s in list(ORIG.items()) + [(a, local(a)) for a in ["ASHR", "KBA", "CNYA", "FXI", "MCHI", "EWH", "CNXT"]]:
    w = wk(s).rename("d")
    for tgt in ["XU100", "XU100usd"]:
        for lab, ctrl in [("sync", None), ("pc_EEM_USD", W[["EEM", "USDTRY"]] if tgt == "XU100" else W[["EEM"]]), ("pc_EEM_ES_USD", W[["EEM", "ES", "USDTRY"]] if tgt == "XU100" else W[["EEM", "ES"]])]:
            for win in ["tam", "IS", "OOS"]:
                rr = pc(W[tgt], w, ctrl, WIN[win]); rows.append(dict(seri=nm, hedef=tgt, tip=lab, pencere=win, r=rr["r"], t=rr["t"], n=rr["n"]))
B = pd.DataFrame(rows); B.to_csv(f"{OUT}/c1c2_bist_weekly.csv", index=False)
pv = B[B.pencere == "tam"].pivot_table(index="seri", columns=["hedef", "tip"], values="r").round(3)
P(pv.to_string())
# günlük: XU100 cc_t ile ASHR_{t-1}, ASHR_t; CSI300_t (Çin kapanışı 07:00 UTC -> BIST t seansından önce)
P("\nGünlük XU100: sync / lag1 (sürücü t-1) — CSI300 Çin kapanışı 07:00 UTC, ASHR 20/21 UTC")
xr = ret("XU100.IS", "c")
for nm, s in [("CSI300(sina)", ORIG["CSI300(sina)"]), ("ASHR", local("ASHR")), ("HSI", ORIG["HSI"]), ("FXI", local("FXI")), ("EWH", local("EWH"))]:
    d = np.log(on_cal(s)).diff()
    a = pc(xr, d, None, WIN["tam"]); b = pc(xr, d.shift(1), None, WIN["tam"])
    P(f"  {nm:13s} sync r {a['r']:+.3f} (n {a['n']}) | sürücü t-1 r {b['r']:+.3f}")

# ===================== C6 TIO =====================
P("\nC6: TIO=F (COMEX ön ay, aylık ortalama fiyatlı) vs DCE demir cevheri (Sina tekil kontratlardan kendi roll serim)")
def sina_contracts(root):
    files = sorted(f for f in os.listdir(f"{S}/data_cin/sina") if f.startswith(root) and f[len(root):-5].isdigit() and len(f[len(root):-5]) == 4)
    L = []
    for f in files:
        js = json.load(open(f"{S}/data_cin/sina/{f}"))
        if not js: continue
        df = pd.DataFrame(js); df["k"] = f[:-5]
        L.append(df)
    A = pd.concat(L); A["d"] = pd.to_datetime(A["d"])
    for c in ["o", "h", "l", "c", "v", "p", "s"]:
        A[c] = pd.to_numeric(A[c], errors="coerce")
    return A

A = sina_contracts("I")
A = A[A.c > 0]
piv_c = A.pivot_table(index="d", columns="k", values="c"); piv_p = A.pivot_table(index="d", columns="k", values="p")
# baskın kontrat: ÖNCEKİ günün en yüksek açık pozisyonu, yalnız ileri vadeye geçiş
_pp = piv_p.shift(1); _ok = _pp.notna().any(axis=1)
dom = pd.Series(np.nan, index=piv_p.index, dtype=object); dom[_ok] = _pp[_ok].idxmax(axis=1)
cur = None; rets = []; keys = []
for d in piv_c.index:
    k = dom.get(d)
    if pd.isna(k): rets.append(np.nan); keys.append(cur); continue
    if cur is None or k > cur: cur = k
    # getiri: aynı kontratta t-1 -> t
    i = piv_c.index.get_loc(d)
    if i == 0: rets.append(np.nan); keys.append(cur); continue
    prev = piv_c.iloc[i - 1][cur]; now = piv_c.iloc[i][cur]
    rets.append(np.log(now / prev) if prev > 0 and now > 0 else np.nan); keys.append(cur)
dce = pd.Series(rets, index=piv_c.index).dropna()
P(f"DCE I roll serisi: {dce.index[0].date()}..{dce.index[-1].date()} n {len(dce)}; kontrat sayısı {piv_c.shape[1]}")
tio = np.log(px("TIO=F", "c")).diff()
fmg = np.log(px("FMG.AX", "c")).diff() if os.path.exists(f"{D}/daily/FMG.AX.parquet") else None
R = pd.concat([tio.rename("tio"), dce.rename("dce")] + ([fmg.rename("fmg")] if fmg is not None else []), axis=1, join="inner").dropna()
R = R[R.index >= "2019-01-01"]
# TIO bayat (0 getiri) oranı
P(f"TIO=F sıfır getiri oranı (2019+): {(tio['2019':] == 0).mean():.3f}")
R["dom"] = R.index.day
# ayın işlem günü sırası ve ay sonundan geriye sayım (TIO kendi takvimi)
tdays = tio["2019":].dropna().index
pos = pd.Series(np.arange(len(tdays)), index=tdays)
m = tdays.to_period("M")
first = pd.Series(tdays, index=tdays).groupby(m).transform("min"); last_ = pd.Series(tdays, index=tdays).groupby(m).transform("max")
k_from_start = pd.Series(tdays, index=tdays).groupby(m).cumcount() + 1
k_to_end = pd.Series(tdays, index=tdays).groupby(m).cumcount(ascending=False)
R["k_start"] = k_from_start.reindex(R.index); R["k_end"] = k_to_end.reindex(R.index)
bins = pd.cut(R.dom, [0, 7, 14, 21, 31], labels=["1-7", "8-14", "15-21", "22-31"])
T = R.groupby(bins, observed=True).apply(lambda g: pd.Series({"n": len(g), "tio_abs%": 100 * g.tio.abs().mean(), "dce_abs%": 100 * g.dce.abs().mean(),
     "corr_tio_dce": g.tio.corr(g.dce), "corr_tio_dce(t+1)": np.nan, "corr_fmg_dce": g.fmg.corr(g.dce) if "fmg" in g else np.nan}))
P(T.round(3).to_string())
# ay sonundan geriye sayım
T2 = R.groupby(pd.cut(R.k_end, [-1, 0, 2, 5, 10, 30], labels=["son gün", "son 2-3", "son 4-6", "son 7-11", "12+ önce"]), observed=True).apply(
    lambda g: pd.Series({"n": len(g), "tio_abs%": 100 * g.tio.abs().mean(), "dce_abs%": 100 * g.dce.abs().mean(), "corr": g.tio.corr(g.dce)}))
P(T2.round(3).to_string())
# ilk gün sıçraması (roll): ayın 1. işlem günü
T3 = R.groupby(R.k_start.clip(upper=4)).apply(lambda g: pd.Series({"n": len(g), "tio_abs%": 100 * g.tio.abs().mean(), "corr": g.tio.corr(g.dce)}))
P("Ayın k. işlem günü (4=4+):\n" + T3.round(3).to_string())
# TIO 1. gün getirisi DCE'nin önceki ay getirisiyle ilişkili mi? (roll = yeni ay kontratına geçiş)
# haftalık
Wt = pd.concat([px("TIO=F", "c").rename("tio")], axis=1)
P("Not: TIO=F haftalık ve aylık TIO/DCE korelasyonu (ay sonu etkisini aşmak için):")
dce_p = np.exp(dce.cumsum())
J = pd.concat([px("TIO=F", "c").rename("tio"), dce_p.rename("dce")], axis=1, join="inner").dropna()["2019":]
Wj = np.log(J.resample("W-FRI").last()).diff().dropna(); Mj = np.log(J.resample("ME").last()).diff().dropna()
P(f"  haftalık r {Wj.tio.corr(Wj.dce):.3f} (n {len(Wj)}), aylık r {Mj.tio.corr(Mj.dce):.3f} (n {len(Mj)})")
T.to_csv(f"{OUT}/c6_tio_dom.csv"); T2.to_csv(f"{OUT}/c6_tio_kend.csv")
log.close()
