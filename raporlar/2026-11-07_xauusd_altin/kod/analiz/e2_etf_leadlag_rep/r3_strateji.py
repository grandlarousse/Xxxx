"""r3: IS izgarasindan secim (yalniz <=2017 ideal net Sharpe), sonra secilen konfigurasyon icin
ideal / ideal-demeaned / yalniz uzun / yalniz-uzun demeaned / uzun + ters ETF / ters ETF bacagi / B&H;
donemler tam, IS, OOS, 2022+; maliyet temel (10 / ters 20 bps) ve stres (20 / 40 bps).
Iki hesap: (A) tum ornek uzerinde backtest, sonra donem dilimi (pozisyon donem sinirindan tasinir);
(B) analistin yaptigi gibi getiriyi doneme kirpip yeniden backtest (sinirda pozisyon sifirlanir)."""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag_rep")
from rep_lib import *
Z = pd.read_pickle(f"{OUT}/r1_signals.pkl"); SIG, R, LP, W, cal = Z["SIG"], Z["R"], Z["LP"], Z["W"], Z["cal"]
INV = {"GLD": "GLL", "GDX": "DUST", "GDXJ": "JDST"}
CST = {"base": (10.0, 20.0), "stress": (20.0, 40.0)}
PER = {"full": (None, None), "is": (None, "2017-12-31"), "oos": ("2018-01-01", None), "2022+": ("2022-01-01", None)}
early = pd.DatetimeIndex(pd.read_csv(f"{OUT}/early_close_days.csv").iloc[:, 0])

def msk(idx, a, b):
    m = pd.Series(True, index=idx)
    if a: m &= idx >= pd.Timestamp(a)
    if b: m &= idx <= pd.Timestamp(b)
    return m.values

def run(pos, und, h, ck, per, mode="A"):
    c, cl = CST[ck]; a, b = PER[per]
    r = R[und].copy(); inv = INV[und]; ri = R[inv].copy()
    if mode == "B":
        keep = msk(r.index, a, b) & r.notna().values
        r = r[keep]; ri = ri.reindex(r.index); p = pos.reindex(r.index).fillna(0)
    else:
        p = pos.reindex(r.index).fillna(0); valid = r.notna().values; r = r.fillna(0)
    m = msk(r.index, a, b)
    if mode == "A": m = m & valid
    rd = r - r[m].mean()                                   # donem ortalamasi cikarilmis
    o = {}
    o["ideal"] = bt(p, r, h, c)[0]; o["ideal_dm"] = bt(p, rd, h, c)[0]
    pl = p.clip(lower=0)
    o["long"], effL, turnL = bt(pl, r, h, c); o["long_dm"] = bt(pl, rd, h, c)[0]
    ps = (-p).clip(lower=0)
    w = W[inv].reindex(r.index)
    okinv = ri.notna() & w.notna()
    psi = (ps * w).where(okinv, 0.0).fillna(0)
    o["short_inv"] = bt(psi, ri.fillna(0), h, cl)[0]
    o["short_ideal"] = bt(-ps, r, h, c)[0]
    o["long_inv"] = o["long"] + o["short_inv"]
    o["bh"] = r.copy()
    _, eff, turn = bt(p, r, h, c)
    res = {k: sharpe(v[m]) for k, v in o.items()}
    res.update(ann_long=float(o["long"][m].mean() * 252), ann_long_inv=float(o["long_inv"][m].mean() * 252), ann_bh=float(o["bh"][m].mean() * 252),
               expo_long=float(effL[m].abs().mean()), trades_yr_ideal=float(turn[m].sum() / m.sum() * 252 / 2), trades_yr_long=float(turnL[m].sum() / m.sum() * 252 / 2))
    return res, o, m

CANDS = {
    "E2-C1": dict(und="GLD", sign=+1, grid=[(("GDXres", k, 60), h, q) for k in (5, 10) for h in (3, 5) for q in (0.7, 0.8)], claimed=(("GDXres", 10, 60), 5, 0.8)),
    "E2-C2": dict(und="GDX", sign=+1, grid=[(("GDXres", k, 60), h, q) for k in (1, 3) for h in (1, 3) for q in (0.7, 0.8)], claimed=(("GDXres", 3, 60), 3, 0.7)),
    "E2-C2j": dict(und="GDXJ", sign=+1, grid=[(("GDXJres", k, 60), h, q) for k in (1, 3) for h in (1, 3) for q in (0.7, 0.8)], claimed=(("GDXJres", 1, 60), 3, 0.7)),
    "E2-C3": dict(und="GDX", sign=-1, grid=[("gi", 1, q) for q in (0.7, 0.8, 0.9)], claimed=("gi", 1, 0.7)),
    "E2-C4": dict(und="GDX", sign=-1, grid=[("PL_d5", h, q) for h in (3, 5) for q in (0.7, 0.8)], claimed=("PL_d5", 3, 0.8)),
    "E2-C5": dict(und="GLD", sign=+1, grid=[(f"asia{k}", h, q) for k in (1, 5) for h in (3, 5) for q in (0.7, 0.8)], claimed=("asia1", 3, 0.7)),
}
rows = []; sel = {}; grids = []; YR = {}
for cid, cd in CANDS.items():
    best = None
    for key, h, q in cd["grid"]:
        p, _, _ = positions(SIG[key], cd["sign"], q)
        for mode in ("A", "B"):
            rs, _, _ = run(p, cd["und"], h, "base", "is", mode)
            ro, _, _ = run(p, cd["und"], h, "base", "oos", mode)
            grids.append(dict(id=cid, key=str(key), h=h, q=q, mode=mode, is_ideal=round(rs["ideal"], 3), is_long=round(rs["long"], 3), oos_ideal=round(ro["ideal"], 3), oos_long=round(ro["long"], 3)))
            if mode == "B" and (best is None or rs["ideal"] > best[0]): best = (rs["ideal"], key, h, q)
    sel[cid] = dict(chosen=str(best[1:]), claimed=str(cd["claimed"]), same=(best[1:] == cd["claimed"]))
    key, h, q = cd["claimed"]
    p, hi, lo = positions(SIG[key], cd["sign"], q)
    sel[cid].update(thr_hi=float(hi), thr_lo=float(lo))
    for mode in ("A", "B"):
        for ck in ("base", "stress"):
            for per in PER:
                rs, o, m = run(p, cd["und"], h, ck, per, mode)
                rows.append(dict(id=cid, mode=mode, cost=ck, period=per, **{k: round(v, 3) for k, v in rs.items()}))
                if mode == "A" and ck == "base" and per == "full":
                    YR[cid] = pd.DataFrame({k: o[k].groupby(o[k].index.year).sum() for k in ("ideal", "long", "long_inv", "bh")}) * 100
T = pd.DataFrame(rows); T.to_csv(f"{OUT}/r3_strateji.csv", index=False)
G = pd.DataFrame(grids); G.to_csv(f"{OUT}/r3_izgara.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 30)
cols = ["id", "mode", "cost", "period", "ideal", "ideal_dm", "long", "long_dm", "long_inv", "short_inv", "short_ideal", "bh", "expo_long", "trades_yr_ideal", "trades_yr_long"]
print(T[(T.period.isin(["oos", "2022+", "is"]))][cols].to_string())
print(json.dumps(sel, indent=1))
gm = G[G["mode"] == "B"].groupby("id")[["is_ideal", "oos_ideal"]].median(); print("izgara medyanlari (B):"); print(gm.round(2))
for k, v in YR.items():
    print(k); print(v.round(1).T.to_string())
    v.to_csv(f"{OUT}/r3_yillik_{k}.csv")

# ---------- C1 kaplama: GLD tut, x < IS %20 kantili iken nakit (h=5 kademeli, 10 bps) ----------
p, hi, lo = positions(SIG[("GDXres", 10, 60)], +1, 0.8)
ov = pd.Series(1.0, index=p.index); ov[p < 0] = 0.0
kap = []
for per, (a, b) in PER.items():
    for mode in ("A", "B"):
        r = R["GLD"]
        if mode == "B":
            k_ = msk(r.index, a, b) & r.notna().values; rr = r[k_]
            pn = bt(ov.reindex(rr.index), rr, 5, 10.0)[0]; bh = rr; m = np.ones(len(rr), bool); eff = bt(ov.reindex(rr.index), rr, 5, 10.0)[1]
        else:
            rr = r.fillna(0); pn, eff, _ = bt(ov, rr, 5, 10.0); bh = rr; m = msk(rr.index, a, b)
        kap.append(dict(period=per, mode=mode, sh_overlay=round(sharpe(pn[m]), 3), sh_bh=round(sharpe(bh[m]), 3), ann_ov=round(pn[m].mean() * 252 * 100, 2), ann_bh=round(bh[m].mean() * 252 * 100, 2),
                        mdd_ov=round(maxdd(pn[m]) * 100, 1), mdd_bh=round(maxdd(bh[m]) * 100, 1), expo=round(eff[m].mean(), 3)))
K = pd.DataFrame(kap); K.to_csv(f"{OUT}/r3_c1_kaplama.csv", index=False); print(K.to_string())

# ---------- C3: yarim gun (13:00 ET kapanis) gunleri haric ----------
gi = SIG["gi"].copy(); gi_x = gi.copy(); gi_x[gi_x.index.isin(early)] = np.nan
y1 = fwd_ret(LP["GDX"], 1)
s_all = stats_block(gi, y1, 1); s_x = stats_block(gi_x, y1, 1)
print("C3 tum:", {k: round(s_all[k], 3) for k in ("ic", "t", "t_is", "t_oos")}, " yarim gunler haric:", {k: round(s_x[k], 3) for k in ("ic", "t", "t_is", "t_oos")})
json.dump(dict(selection=sel, c3_early_close=dict(all={k: s_all[k] for k in ("ic", "t", "t_is", "t_oos")}, excl={k: s_x[k] for k in ("ic", "t", "t_is", "t_oos")})), open(f"{OUT}/r3_secim.json", "w"), indent=1, default=str)
