"""TR1 Kore lag1 -> XU030 gün-içi; TR2 USD bazlı XU100 EEM Dimson betası rejimleri; TR3 'küresel sürücüsü olmayan 20 hisse' taraması.
Ek: G1 uzun örneklem (günlük ES/^GSPC_{t-1} -> gap, 2014+)."""
import os, numpy as np, pandas as pd
from vcore import *
log = open(f"{OUT}/v4_tarama.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n"); log.flush()
c = cal()
x30 = decomp("XU030.IS"); x100 = decomp("XU100.IS")
ks = ret("^KS11", "c"); nk = ret("^N225", "c"); tw = ret("^TWII", "c") if os.path.exists(f"{D}/daily/^TWII.parquet") else None
es = ret("ES=F", "c"); spx = ret("^GSPC", "c"); eem = ret("EEM"); usd = ret("TRY=X", "c")
y = x30["intra"]
RUN_TR12 = os.environ.get("TR12", "1") == "1"
P("TR1: XU030 gün-içi_t ~ ^KS11 (BIST takvimi; KS11 kapanışı ~06:30 UTC, BIST açılışı 07:00 UTC)")
P("  Tanım: KS11_t = Kore seansı t (BIST t açılışından ÖNCE biter, lag0 zaten işlenebilir); KS11_{t-1} = Kore seansı t-1 (BIST t-1 seansından da önce).")
for lab, x in [("KS11_t (lag0)", ks), ("KS11_{t-1} (lag1)", ks.shift(1)), ("KS11_{t-2}", ks.shift(2)), ("N225_{t-1}", nk.shift(1)), ("N225_t", nk)] + ([("TWII_{t-1}", tw.shift(1)), ("TWII_t", tw)] if tw is not None else []) + [("ES_{t-1}", es.shift(1)), ("XU030 intra_{t-1}", x30["intra"].shift(1)), ("XU030 gap_t", x30["gap"])]:
    rows, yr, same, tot = full_report(y, x)
    P(f"  {lab:20s} {fmt(rows, yr, same, tot)}")
P("  yıllar KS11_{t-1}: " + ", ".join(f"{k}:{v:+.3f}" for k, v in by_year(y, ks.shift(1)).items()))
# kontroller
ctrl1 = pd.concat([x30["intra"].shift(1).rename("i1"), x30["gap"].shift(1).rename("g1"), x30["cc"].shift(1).rename("c1"), x30["gap"].rename("g0"),
                   ks.rename("k0"), es.shift(1).rename("e1"), es.shift(2).rename("e2")], axis=1)
ctrl2 = pd.concat([ctrl1, eem.shift(1).rename("eem1"), usd.shift(1).rename("usd1"), x100["cc"].shift(1).rename("xu1"), nk.shift(1).rename("n1")], axis=1)
for lab, ct in [("| XU030 kendi gecikmeleri + gap_t + KS11_t + ES_{t-1,t-2}", ctrl1), ("| + EEM_{t-1}, USDTRY_{t-1}, XU100_{t-1}, N225_{t-1}", ctrl2)]:
    rows, yr, same, tot = full_report(y, ks.shift(1), ct)
    P(f"  KS11_{{t-1}} {lab}: {fmt(rows, yr, same, tot)}")
# KS11_{t-1} ile XU030'un t-1 parçaları: Kore t-1, BIST t-1 gün-içi ile örtüşmez ama gap_{t-1}'e girer
P("  corr(KS11_{t-1}, XU030 gap_{t-1}) =", round(pd.concat([ks.shift(1), x30["gap"].shift(1)], axis=1).loc["2014":].corr().iloc[0, 1], 3),
  "; corr(KS11_{t-1}, XU030 intra_{t-1}) =", round(pd.concat([ks.shift(1), x30["intra"].shift(1)], axis=1).loc["2014":].corr().iloc[0, 1], 3))
# backtest
def bt(sig, tgt, cost, mode="sign", z=1.0):
    df = pd.concat([sig.rename("s"), tgt.rename("r")], axis=1).dropna()
    if mode == "z":
        sd = df.s.rolling(250, min_periods=120).std().shift(1)
        zz = df.s / sd
        pos = np.sign(zz).where(zz.abs() > z, 0)
    else:
        pos = np.sign(df.s)
    pnl = pos * df.r - (pos != 0) * cost / 1e4
    out = {}
    for w, (a, b) in [("IS", WIN["IS"]), ("OOS", WIN["OOS"])]:
        p = pnl.loc[a:b]; tr = p[pos.loc[a:b] != 0]
        out[w] = dict(n=len(tr), bps=tr.mean() * 1e4, t=tr.mean() / (tr.std() / np.sqrt(len(tr))) if len(tr) > 2 else np.nan,
                      sharpe=p.mean() / p.std() * np.sqrt(252) if p.std() > 0 else np.nan)
    return out
for mode in ["sign", "z"]:
    for cost in [0, 4, 8, 15]:
        o = bt(ks.shift(1).loc["2014":], y, cost, mode)
        P(f"  BT KS11_{{t-1}} -> XU030 gün-içi, {mode}, {cost} bps: IS {o['IS']['bps']:+.1f} bps (t {o['IS']['t']:.2f}, Sh {o['IS']['sharpe']:.2f}, n {o['IS']['n']}) | OOS {o['OOS']['bps']:+.1f} bps (t {o['OOS']['t']:.2f}, Sh {o['OOS']['sharpe']:.2f}, n {o['OOS']['n']})")
# Kore lag0 (işlenebilir) aynı backtest
for cost in [0, 8]:
    o = bt(ks.loc["2014":], y, cost, "z")
    P(f"  BT KS11_t (lag0, Kore t kapanışı) -> XU030 gün-içi z, {cost} bps: IS {o['IS']['bps']:+.1f} (t {o['IS']['t']:.2f}) | OOS {o['OOS']['bps']:+.1f} (t {o['OOS']['t']:.2f})")

# ---------------- TR2 ----------------
P("\nTR2: USD bazlı XU100 ~ EEM Dimson betası (lag0+lag1), dönemler")
xu = ret("XU100.IS", "c"); xusd = (xu - usd).rename("y")
REG = [("2014-2017", "2014-01-01", "2017-12-31"), ("2018", "2018-01-01", "2018-12-31"), ("2019-2020", "2019-01-01", "2020-12-31"), ("2021", "2021-01-01", "2021-12-31"),
       ("2022-May2023", "2022-01-01", "2023-05-31"), ("Haz2023-Mar2025", "2023-06-01", "2025-03-18"), ("Mar-Ara2025", "2025-03-19", "2025-12-31"),
       ("2026 Oca-Ağu", "2026-01-01", "2026-08-31"), ("Eyl-Eki 2026", "2026-09-01", "2026-10-31"), ("tam 2014-2026", "2014-01-01", "2026-12-31")] + \
      [(str(yy), f"{yy}-01-01", f"{yy}-12-31") for yy in range(2014, 2027)]
W = pd.DataFrame({"y": xusd, "x0": eem, "x1": eem.shift(1), "xm1": eem.shift(-1), "ytl": xu})
# haftalık (asenkronluğu azaltır)
def wk(s): return np.log(s.resample("W-FRI").last()).diff()
Wk = pd.DataFrame({"y": wk(px("XU100.IS", "c")) - wk(px("TRY=X", "c")), "x": wk(px("EEM", "adj"))}).dropna()
rows = []
for lab, a, b in REG:
    d = W.loc[a:b].dropna()
    X = np.column_stack([np.ones(len(d)), d.x0, d.x1]); bb = np.linalg.lstsq(X, d.y, rcond=None)[0]; e = d.y - X @ bb
    XtXi = np.linalg.inv(X.T @ X); V = XtXi @ (X.T * e.values ** 2) @ X @ XtXi; wv = np.array([0, 1, 1]); se = np.sqrt(wv @ V @ wv)
    X3 = np.column_stack([np.ones(len(d)), d.x0, d.x1, d.xm1]); b3 = np.linalg.lstsq(X3, d.y, rcond=None)[0]
    dw = Wk.loc[a:b]; bw = np.cov(dw.y, dw.x)[0, 1] / dw.x.var() if len(dw) > 5 else np.nan
    rows.append(dict(donem=lab, n=len(d), dimson=bb[1] + bb[2], se=se, b0=bb[1], b1=bb[2], dimson3=b3[1:].sum(), corr0=d.y.corr(d.x0), beta_haftalik=bw, n_w=len(dw)))
R2 = pd.DataFrame(rows); R2.round(3).to_csv(f"{OUT}/tr2_beta.csv", index=False)
P(R2.round(2).to_string(index=False))
# 2024+ eşzamanlı USDTRY (15:00 UTC h1) ile USD bazlı XU100
su = snap("TRY=X", ["15:00"])["15:00"].reindex(c)
xu_usd_sync = (xu - np.log(su).diff()).rename("y")
for lab, a, b in [("2024", "2024-01-01", "2024-12-31"), ("2025", "2025-01-01", "2025-12-31"), ("2026", "2026-01-01", "2026-12-31"), ("Mar-Ara2025", "2025-03-19", "2025-12-31"), ("2026 Oca-Ağu", "2026-01-01", "2026-08-31")]:
    d = pd.DataFrame({"y": xu_usd_sync, "x0": eem, "x1": eem.shift(1)}).loc[a:b].dropna()
    bb = np.linalg.lstsq(np.column_stack([np.ones(len(d)), d.x0, d.x1]), d.y, rcond=None)[0]
    P(f"  eşzamanlı USDTRY(15:00) ile Dimson β {lab}: {bb[1]+bb[2]:.2f} (n {len(d)})")

# ---------------- TR3 ----------------
P("\nTR3: 20 hisse için XU100+USDTRY kontrollü küresel tarama (tüm BIST-dışı sürücüler, lag0; ayrıca lag1)")
L20 = "AKSEN ALARK DOHOL EKGYO ENKAI HALKB HEKTS ISCTR ODAS SASA SISE TCELL TKFEN TTKOM ULKER VAKBN VESTL TSKB BIMAS SOKM".split()
cat = pd.read_csv(f"{D}/catalog.csv")
MIRROR = {"TUR", "TKC", "AKBTY", "TKGBY", "YKBNY", "TYIDY", "TRY=X", "EURTRY=X", "GBPTRY=X", "TRYUSD=X"}
drv = [s for s in cat.sym if not s.endswith(".IS") and os.path.exists(f"{D}/daily/{s}.parquet")]
C0 = pd.DataFrame({"xu": xu, "usd": usd}).loc["2014-01-01":"2026-10-30"]
idx = C0.index
def rsd(s, cols=C0):
    df = pd.concat([s.rename("v"), cols], axis=1).loc[idx]
    m = df.notna().all(axis=1)
    out = pd.Series(np.nan, index=idx)
    if m.sum() < 500: return out
    A = np.column_stack([np.ones(m.sum()), df.loc[m, cols.columns].values]); b = np.linalg.lstsq(A, df.loc[m, "v"].values, rcond=None)[0]
    out[m] = df.loc[m, "v"].values - A @ b
    return out
DR = {}; meta = {}
for s in drv:
    try:
        r = ret(s, "adj")
    except Exception:
        continue
    r = r.loc[idx]
    if r.notna().sum() < 1000: continue
    zf = (r == 0).mean()
    if zf > 0.3: continue
    DR[s] = rsd(r); DR[s + "|L1"] = rsd(r.shift(1)); meta[s] = zf
DRm = pd.DataFrame(DR)
P(f"  sürücü sayısı {len(meta)} (n>=1000, sıfır oranı<=0,3), test = 20 × {len(meta)} × 2 lag")
ST = pd.DataFrame({s: rsd(ret(s + ".IS")) for s in L20})
def pcor(A, B):
    """A: T×k, B: T×m, NaN çift-tam."""
    a = A.values; b = B.values; ma = np.isfinite(a); mb = np.isfinite(b)
    a0 = np.where(ma, a, 0); b0 = np.where(mb, b, 0)
    n = ma.T.astype(float) @ mb.astype(float)
    sa = a0.T @ mb; sb = ma.T.astype(float) @ b0
    saa = (a0 ** 2).T @ mb; sbb = ma.T.astype(float) @ (b0 ** 2); sab = a0.T @ b0
    cov = sab - sa * sb / n; va = saa - sa ** 2 / n; vb = sbb - sb ** 2 / n
    return pd.DataFrame(cov / np.sqrt(va * vb), index=A.columns, columns=B.columns), pd.DataFrame(n, index=A.columns, columns=B.columns)
Rf, Nf = pcor(ST, DRm)
Ris, _ = pcor(ST.loc[:"2020"], DRm.loc[:"2020"]); Roos, _ = pcor(ST.loc["2021":], DRm.loc["2021":])
from scipy import stats
T_ = Rf * np.sqrt((Nf - 4) / (1 - Rf ** 2)); Pv = pd.DataFrame(2 * stats.t.sf(np.abs(T_.values), Nf.values - 4), index=Rf.index, columns=Rf.columns)
nonmir = [cc_ for cc_ in DRm.columns if cc_.split("|")[0] not in MIRROR]
pv = Pv[nonmir].values.ravel(); ok = bh(pv, 0.05).reshape(Pv[nonmir].shape)
OK = pd.DataFrame(ok, index=ST.columns, columns=nonmir)
rows = []
for s in L20:
    r = Rf.loc[s, nonmir]; top = r.abs().sort_values(ascending=False).index[:5]
    rep = [(d, round(r[d], 3), round(Ris.loc[s, d], 3), round(Roos.loc[s, d], 3), bool(OK.loc[s, d])) for d in top]
    nfdr = int(OK.loc[s].sum()); nfdr_rep = int(sum(OK.loc[s, d] and np.sign(Ris.loc[s, d]) == np.sign(Roos.loc[s, d]) and abs(Roos.loc[s, d]) > 0.04 and abs(Ris.loc[s, d]) > 0.04 for d in nonmir))
    rows.append(dict(stock=s, max_abs_pc=r.abs().max(), top1=top[0], top1_pc=r[top[0]], n_fdr=nfdr, n_fdr_replike=nfdr_rep, n_abs_gt_008=int((r.abs() > 0.08).sum()),
                     top5=str(rep)))
T3 = pd.DataFrame(rows).set_index("stock"); T3.to_csv(f"{OUT}/tr3_scan.csv")
P(T3[["max_abs_pc", "top1", "top1_pc", "n_fdr", "n_fdr_replike", "n_abs_gt_008"]].round(3).to_string())
P("  toplam FDR geçen (20 hisse):", int(OK.values.sum()), "/", OK.size)
for s in L20:
    P(f"  {s} ilk5: {T3.loc[s, 'top5']}")
# TR3 çelişki kontrolleri
P("\nTR3 çelişki kontrolleri (XU100 kontrollü; USDTRY kontrol DEĞİL, sürücü)")
for s in L20:
    yy = ret(s + ".IS")
    a = pc(yy, usd, xu.to_frame(), WIN["tam"]); i_ = pc(yy, usd, xu.to_frame(), WIN["IS"]); o_ = pc(yy, usd, xu.to_frame(), WIN["OOS"])
    P(f"  {s:6s} USDTRY|XU100 tam {a['r']:+.3f} (t {a['t']:.1f}) IS {i_['r']:+.3f} OOS {o_['r']:+.3f}")
tkc = ret("TKC"); tc = ret("TCELL.IS"); dtc = decomp("TCELL.IS")
for lab, x, yv, ct in [("TCELL cc ~ TKC_t | XU100+USD", tkc, tc, pd.concat([xu, usd], axis=1)), ("TCELL cc ~ TKC_t | XU100+USD+EEM+ES", tkc, tc, pd.concat([xu, usd, eem, es], axis=1)),
                       ("TCELL gap ~ TKC_{t-1} | XU100 gap", tkc.shift(1), dtc["gap"], x100[["gap"]]), ("TCELL gap ~ TKC_{t-1} | XU100 gap + TUR_{t-1}", tkc.shift(1), dtc["gap"], pd.concat([x100["gap"], ret("TUR").shift(1).rename("tur")], axis=1)),
                       ("TCELL intra ~ TKC_{t-1} | XU100 intra", tkc.shift(1), dtc["intra"], x100[["intra"]])]:
    rows_, yr, same, tot = full_report(yv, x, ct)
    P(f"  {lab:42s} {fmt(rows_, yr, same, tot)}")
en = ret("ENKAI.IS")
for lab, ct in [("ENKAI ~ USDTRY | XU100", xu.to_frame()), ("ENKAI ~ USDTRY | XU100+EEM", pd.concat([xu, eem], axis=1))]:
    rows_, yr, same, tot = full_report(en, usd, ct); P(f"  {lab:42s} {fmt(rows_, yr, same, tot)}")
# USD bazlı 'dış sürücü' kontrolü: ENKAI'nin EUR/USD'si
eurusd = ret("EURUSD=X", "c")
rows_, yr, same, tot = full_report(en, eurusd, pd.concat([xu, usd], axis=1)); P(f"  {'ENKAI ~ EURUSD | XU100+USD':42s} {fmt(rows_, yr, same, tot)}")

# ---------------- G1 uzun örneklem (günlük) ----------------
P("\nG1 uzun örneklem: XU030 gap_t ~ ES_{t-1} / ^GSPC_{t-1} (günlük kapanış; BIST t-1 seansıyla örtüşme var -> seyreltilmiş)")
for lab, x in [("ES_{t-1}", es.shift(1)), ("^GSPC_{t-1}", spx.shift(1)), ("TUR_{t-1}", ret("TUR").shift(1))]:
    rows_, yr, same, tot = full_report(x30["gap"], x)
    P(f"  {lab:12s} {fmt(rows_, yr, same, tot)}")
log.close()
