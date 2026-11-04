"""Sağlamlık: öne çıkan adaylar.
 A) Emsal: REF_US->TUPRS, MINERS_AU->EREGL/KRDMD, GOLD_V->TRALT/TRMET, DEF_EU->ASELS
    - 47 hisse içinde hedefin sırası (tP, h=2 hedged), birini-dışarıda-bırak üyeler, ek gecikme (bir gün daha eski P), kriz dışı, eşik.
 B) VİOP USDTRY k günlük kümülatif -> THYAO / ihracatçı sepeti (raw ve hedged), kriz dışı, yıllar, işlemler.
"""
import numpy as np, pandas as pd, klib as K, ll
import a_peers as A
F = K.fut_panel(); Sp = K.spot_panel()
CRISIS = [("2018-08-01", "2018-09-30"), ("2020-02-24", "2020-04-30"), ("2021-11-15", "2022-01-31"), ("2023-05-15", "2023-06-30"),
          ("2025-03-19", "2025-04-30"), ("2026-09-01", "2026-10-31")]
def crisis_mask(idx):
    m = pd.Series(False, index=idx)
    for a, b in CRISIS: m |= (idx >= a) & (idx <= b)
    return m
_SU = {}
def setup(mode):
    if mode in _SU: return _SU[mode]
    if mode in ("H", "DF"):
        R = F; mk = F["XU030"]; start = "2023-12-05" if mode == "H" else "2017-03-06"; split = "2025-05-01" if mode == "H" else "2022-01-01"
    else:
        R = Sp; mk = Sp["XU100"]; start = "2014-01-01"; split = "2021-01-01"
    w = 120 if mode == "H" else 250; mp = 40 if mode == "H" else 60
    betaS = K.roll_beta(R[K.STOCKS], mk, 250, 60)
    resid = R[K.STOCKS] - betaS.mul(mk, axis=0)
    _SU[mode] = (R, mk, start, split, w, mp, betaS, resid)
    return _SU[mode]
def evalP(P0, s, mode, h=2, tg="hedged", lagged=False, extra_mask=None, thr=1.0):
    R, mk, start, split, w, mp, betaS, resid = setup(mode)
    P0 = P0.reindex(R.index); Pz = K.sdscale(P0, w, mp)
    Ds = K.sdscale(resid, w, mp)
    y = K.fwd(R[s], h) if tg == "raw" else K.fwd(R[s], h) - betaS[s] * K.fwd(mk, h)
    y = y[y.index >= start]
    if extra_mask is not None: y = y[~extra_mask.reindex(y.index).fillna(False)]
    X2 = pd.concat([Pz.rename("P"), Ds[s].rename("Ds")] + ([Ds[s].shift(1).rename("Ds1")] if lagged else []), axis=1)
    r2 = K.reg(y, X2, h + 1); r1 = K.reg(y, Pz, h + 1)
    tr = K.trades_nonoverlap(Pz, y, h, thr); st = K.trade_stats(tr, 8 + (3 if tg == "hedged" else 0), split) if len(tr) >= 5 else {}
    return dict(tP=r2["t"], bP=r2["b"] * 1e4, tP_uni=r1["t"], n_tr=st.get("n"), net8=st.get("net"), t8=st.get("t_net"),
                IS=st.get("IS_net"), IS_t=st.get("IS_t"), OOS=st.get("OOS_net"), OOS_t=st.get("OOS_t"), yrs=st.get("yrs_pos"), by_year=st.get("by_year"))
rows = []
CANDS = [("REF_US", ["TUPRS"], ["DF", "DS", "H"]), ("MINERS_AU", ["EREGL", "KRDMD"], ["DF", "DS", "H"]),
         ("GOLD_V", ["TRALT", "TRMET"], ["DF"]), ("GOLD", ["TRALT", "TRMET"], ["H"]), ("DEF_EU", ["ASELS"], ["DF", "DS", "H"])]
for bk, targets, modes in CANDS:
    for mode in modes:
        sig = pd.read_pickle(K.RES + f"/a_sig_{mode}.pkl"); P0 = sig[bk]
        lagged = (mode != "H") and (bk not in A.ASIA) and bk != "GOLD_V"
        R, mk, start, split, w, mp, betaS, resid = setup(mode)
        # 47 hisse sırası
        ts = {s: evalP(P0, s, mode, 2, "hedged", lagged)["tP"] for s in K.STOCKS}
        rk = pd.Series(ts).rank(ascending=False)
        for s in targets:
            for h in (1, 2, 3):
                for tg in ("raw", "hedged"):
                    base = evalP(P0, s, mode, h, tg, lagged)
                    rows.append(dict(cand=bk, stock=s, mode=mode, h=h, tgt=tg, test="temel", rank47=rk[s] if (h == 2 and tg == "hedged") else np.nan, **base))
            # kriz dışı, ek gecikme, eşik
            cm = crisis_mask(R.index)
            rows.append(dict(cand=bk, stock=s, mode=mode, h=2, tgt="hedged", test="kriz_dışı", **evalP(P0, s, mode, 2, "hedged", lagged, cm)))
            rows.append(dict(cand=bk, stock=s, mode=mode, h=2, tgt="hedged", test="+1 gün eski P", **evalP(P0.shift(1), s, mode, 2, "hedged", lagged)))
            for thr in (0.5, 1.5, 2.0):
                rows.append(dict(cand=bk, stock=s, mode=mode, h=2, tgt="hedged", test=f"eşik {thr}", **evalP(P0, s, mode, 2, "hedged", lagged, None, thr)))
            # birini dışarıda bırak
            if bk in A.B and len(A.B[bk]) > 1:
                for m_out in A.B[bk]:
                    keep = {k: v for k, v in A.B[bk].items() if k != m_out}
                    old = A.B[bk]; A.B[bk] = keep
                    try: Pm = A.peer_signal(bk, mode)
                    finally: A.B[bk] = old
                    rows.append(dict(cand=bk, stock=s, mode=mode, h=2, tgt="hedged", test=f"-{m_out}", **evalP(Pm, s, mode, 2, "hedged", lagged)))
        print(bk, mode, "ok", flush=True)
O = pd.DataFrame(rows); O.to_csv(K.RES + "/r_robust_peers.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 90)
print(O.drop(columns=["by_year"]).round(2).to_string())

# ---------------- B) VİOP USDTRY -> ihracatçılar ----------------
EXP = ["THYAO", "FROTO", "TOASO", "VESTL", "ARCLK", "EREGL", "SISE", "AEFES", "PGSUS", "TAVHL"]
usd = F["USDTRY"]; R = F[K.STOCKS + ["XU030"]]; mk = F["XU030"]
betaS = K.roll_beta(R[K.STOCKS], mk, 250, 60)
rows = []
for k in (3, 5):
    z = K.sdscale(K.cum(usd, k, 0), 250, 60)
    cm = crisis_mask(R.index)
    for s in EXP + ["XU030", "BASKET"]:
        for h in (2, 3):
            for tg in ("raw", "hedged"):
                if s == "BASKET":
                    yy = pd.concat([(K.fwd(R[x], h) - (betaS[x] * K.fwd(mk, h) if tg == "hedged" else 0)) for x in EXP], axis=1).mean(axis=1)
                elif s == "XU030":
                    if tg == "hedged": continue
                    yy = K.fwd(R[s], h)
                else:
                    yy = K.fwd(R[s], h) - (betaS[s] * K.fwd(mk, h) if tg == "hedged" else 0)
                yy = yy[yy.index >= "2017-03-06"]
                for lab, msk in (("tümü", None), ("kriz_dışı", cm)):
                    y = yy if msk is None else yy[~msk.reindex(yy.index).fillna(False)]
                    r = K.reg(y, z, h + 1); ri = K.reg(y[y.index < "2022-01-01"], z, h + 1); ro = K.reg(y[y.index >= "2022-01-01"], z, h + 1)
                    tr = K.trades_nonoverlap(z, y, h, 1.0); st = K.trade_stats(tr, 8 + (3 if tg == "hedged" else 0), "2022-01-01")
                    up = tr[tr["dir"] > 0]["gross"].mean() * 1e4 if len(tr) else np.nan; dn = tr[tr["dir"] < 0]["gross"].mean() * 1e4 if len(tr) else np.nan
                    rows.append(dict(k=k, stock=s, h=h, tgt=tg, sample=lab, t=r["t"], b=r["b"] * 1e4, t_IS=ri["t"], t_OOS=ro["t"], n_tr=st.get("n"), per_yr=st.get("per_yr"),
                                     net8=st.get("net"), t8=st.get("t_net"), IS=st.get("IS_net"), OOS=st.get("OOS_net"), yrs=st.get("yrs_pos"),
                                     n_long=int((tr["dir"] > 0).sum()) if len(tr) else 0, gross_long=up, gross_short=dn, by_year=st.get("by_year")))
U = pd.DataFrame(rows); U.to_csv(K.RES + "/r_robust_usd.csv", index=False)
print(U.drop(columns=["by_year"]).round(2).to_string())
print(U[(U.stock.isin(["THYAO", "BASKET"])) & (U["sample"] == "tümü") & (U.h == 3)][["k", "stock", "tgt", "by_year"]].to_string())
