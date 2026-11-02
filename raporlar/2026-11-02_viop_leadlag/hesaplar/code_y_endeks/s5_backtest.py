"""GÖREV 5: Backtestler (look-ahead yok; maliyet 8 ve 15 bps gidiş-dönüş; IS <2021, OOS >=2021; yön IS'te seçilir).
BT1  Sektör 'yakalama': sinyal = sektör(ex-hisse)_{t-1} - hisse_{t-1}  -> hisse gün-içi_t (açılış->kapanış). Tek hisse + kesitsel L/S (üst 5 / alt 5).
BT1b Sektör momentumu: sektör(ex)_{t-1} - XU100_{t-1} -> hisse gün-içi_t.
BT2  XU030 son saat (17:00->18:00 TSİ, İş h1) -> (a) XU030 ertesi gap (kapanış müzayedesinden gir, açılışta çık), (b) ertesi cc, (c) ertesi gün-içi;
     ayrıca 47 hisse için aynı sinyal -> hisse gap_{t+1}. Kapanış müzayedesi hareketi (18:00->18:10) -> ertesi gün-içi.
BT3  Büyük->küçük: XU030_{t-1} -> en illikit VİOP üçte biri gün-içi_t ve illikit beşli (Q1) portföy gün-içi_t.
"""
from ye_common import *
COSTS = [0, 8, 15]
def bt(sig, tgt, mode="z", thr=1.0, sign=1, cost=8):
    res, pnl = ll.backtest(sign * sig, tgt, cost_bps=cost, mode=mode, thr=thr, split=str(SPLIT.date()))
    return res, pnl
def row(name, stock, res, cost, sign, extra=None):
    r = {"bt": name, "stock": stock, "cost": cost, "sign": sign}
    for k in ["IS", "OOS", "ALL"]:
        for f in ["n", "mean_bps", "t", "hit", "sharpe"]: r[f"{k}_{f}"] = res[k].get(f, np.nan)
    r["by_year"] = str(res.get("by_year_bps"));
    if extra: r.update(extra)
    return r
rows = []
m = idx_ret("XU100")
# ---------- BT1 / BT1b ----------
S1 = pd.read_csv(RES + "/sync_best.csv").set_index("stock")
sigC = {}; sigM = {}; tgtI = {}
for s in VIOP:
    sec = S1.loc[s, "own_sector"]; rs = stk_ret(s); d = stk_dec(s)
    ex = ex_ret(sec, s, idx_ret(sec), rs)
    sigC[s] = (ex - rs).shift(1); sigM[s] = (ex - m).shift(1); tgtI[s] = d["intra"]
    for nm, sg in [("BT1_catchup", sigC[s]), ("BT1b_secmom", sigM[s])]:
        sg = sg[sg.index >= START]
        r0, _ = bt(sg, tgtI[s], cost=0); sgn = 1 if r0["IS"].get("mean_bps", 0) >= 0 else -1  # yön IS'te
        for c in COSTS:
            res, _ = bt(sg, tgtI[s], sign=sgn, cost=c); rows.append(row(nm, s, res, c, sgn, {"sector": sec}))
SC = pd.DataFrame(sigC); TI = pd.DataFrame(tgtI); SM = pd.DataFrame(sigM)
SC = SC[SC.index >= START]; TI = TI.reindex(SC.index); SM = SM.reindex(SC.index)
def cs_ls(sig, tgt, k=5, cost=8, sign=1):
    """kesitsel: sinyal en yüksek k hisse long, en düşük k short (eşit ağırlık, piyasa-nötr). Her bacak gidiş-dönüş cost."""
    rk = (sign * sig).rank(axis=1); n = rk.notna().sum(axis=1)
    lo = rk.le(k) & tgt.notna(); hi = rk.gt(n.values[:, None] - k) & tgt.notna()
    pnl = (tgt.where(hi).mean(axis=1) - tgt.where(lo).mean(axis=1)) - 2 * cost / 1e4
    return pnl[(n >= 20)].dropna()
def pnl_stats(p):
    out = {}
    for k, msk in [("IS", p.index < SPLIT), ("OOS", p.index >= SPLIT), ("ALL", p.index == p.index)]:
        x = p[msk]
        if len(x) < 30: continue
        mu, t, n = ll.nw_t(x); out[k] = {"n": n, "mean_bps": 1e4 * mu, "t": t, "hit": (x > 0).mean(), "sharpe": x.mean() / x.std() * np.sqrt(252)}
    out["by_year_bps"] = (1e4 * p.groupby(p.index.year).mean()).round(1).to_dict(); return out
for nm, sg in [("BT1_catchup_CS_LS5", SC), ("BT1b_secmom_CS_LS5", SM)]:
    p0 = cs_ls(sg, TI, cost=0); sgn = 1 if p0[p0.index < SPLIT].mean() >= 0 else -1
    for c in COSTS:
        rows.append(row(nm, "47 hisse L/S", pnl_stats(cs_ls(sg, TI, cost=c / 2, sign=sgn)), c, sgn))  # cost/2 per leg => toplam round-trip 'c' per bacak çifti
# ---------- BT2: XU030 son saat ----------
h = pd.read_parquet(f"{ISY}/h1/XU030.parquet")["px"]; h = h[h.index >= "2017-01-01"]
dt_ = (h.index + pd.Timedelta(hours=3)).normalize()
H = pd.DataFrame({"px": h.values, "d": dt_, "hr": h.index.hour}, index=h.index)
p13 = H[H.hr == 13].set_index("d")["px"]; p14 = H[H.hr == 14].set_index("d")["px"]; p15 = H[H.hr == 15].set_index("d")["px"]; p12 = H[H.hr == 12].set_index("d")["px"]
last1 = np.log(p14 / p13); last2 = np.log(p14 / p12); auc = np.log(p15 / p14)
# XU030 gap/gün-içi: Yahoo açılış + İş kapanış
y = ll.raw("XU030.IS"); y.index = pd.DatetimeIndex(y["ldate"]); y = y[~y.index.duplicated(keep="last")]
cc30 = idx_ret("XU030"); o = y["o"].reindex(cc30.index); c_ = idx_px("XU030")
intra30 = np.log(c_ / o); bad = (o <= 0) | (np.abs(np.log(o / c_.shift(1))) < 1e-7); intra30[bad] = np.nan; gap30 = cc30 - intra30
sigs = {"last1h": last1, "last2h": last2, "auction": auc}
for sn, sg in sigs.items():
    for tn, tg in [("XU030_gap_t+1", gap30.shift(-1)), ("XU030_cc_t+1", cc30.shift(-1)), ("XU030_intra_t+1", intra30.shift(-1))]:
        if sn == "auction" and tn != "XU030_intra_t+1": continue  # müzayede hareketi 18:10'da biliniyor -> pay vadelisi kapalı; sadece ertesi gün-içi işlenebilir
        sg2 = sg.reindex(tg.index)
        r0, _ = bt(sg2, tg, cost=0); sgn = 1 if r0["IS"].get("mean_bps", 0) >= 0 else -1
        b_, t_, n_, _ = ols_nw(tg.reindex(sg2.index).values, sg2.values)
        for c in COSTS:
            res, _ = bt(sg2, tg, sign=sgn, cost=c); rows.append(row(f"BT2_{sn}->{tn}", "XU030", res, c, sgn, {"beta": b_[1], "beta_t": t_[1]}))
# hisseler: XU030 son saat -> hisse gap_{t+1} (kapanıştan gir)
for s in VIOP:
    d = stk_dec(s); tg = d["gap"].shift(-1); sg2 = last1.reindex(tg.index)
    r0, _ = bt(sg2, tg, cost=0); sgn = 1 if r0["IS"].get("mean_bps", 0) >= 0 else -1
    for c in COSTS:
        res, _ = bt(sg2, tg, sign=sgn, cost=c); rows.append(row("BT2_last1h->stock_gap_t+1", s, res, c, sgn))
# ---------- BT3: büyük -> küçük ----------
liq = pd.read_csv(RES + "/viop_liquidity.csv", index_col=0)["log_turnover_2021"].sort_values()
ill = list(liq.index[:16]); liqs = list(liq.index[-16:])
x30 = idx_ret("XU030").shift(1)
for grpn, names in [("illikit16", ill), ("likit16", liqs)]:
    T_ = pd.DataFrame({s: stk_dec(s)["intra"] for s in names}); T_ = T_[T_.index >= START]
    port = T_.mean(axis=1)
    r0, _ = bt(x30.reindex(port.index), port, cost=0); sgn = 1 if r0["IS"].get("mean_bps", 0) >= 0 else -1
    for c in COSTS:
        res, _ = bt(x30.reindex(port.index), port, sign=sgn, cost=c); rows.append(row(f"BT3_XU030_t-1->{grpn}_intra", grpn, res, c, sgn))
    for s in names:
        tg = stk_dec(s)["intra"]
        r0, _ = bt(x30.reindex(tg.index), tg, cost=0); sgn = 1 if r0["IS"].get("mean_bps", 0) >= 0 else -1
        for c in COSTS:
            res, _ = bt(x30.reindex(tg.index), tg, sign=sgn, cost=c); rows.append(row(f"BT3_XU030_t-1->stock_intra", s, res, c, sgn, {"group": grpn}))
P = pd.read_parquet(RES + "/liq_portfolios.parquet"); P.columns = [f"{a}_{b}" for a, b in P.columns]
for tn in ["intra_1", "cc_1"]:
    tg = P[tn]; r0, _ = bt(x30.reindex(tg.index), tg, cost=0); sgn = 1 if r0["IS"].get("mean_bps", 0) >= 0 else -1
    for c in COSTS:
        res, _ = bt(x30.reindex(tg.index), tg, sign=sgn, cost=c); rows.append(row(f"BT3_XU030_t-1->Q1_{tn}", "Q1 (en illikit beşli, ~25 hisse; VİOP'ta işlenemez)", res, c, sgn))
R_ = pd.DataFrame(rows); R_.to_csv(RES + "/backtests.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)
agg = R_[R_.stock.isin(["XU030", "47 hisse L/S", "illikit16", "likit16"]) | R_.stock.str.startswith("Q1")]
print(agg[["bt", "stock", "cost", "sign", "IS_n", "IS_mean_bps", "IS_t", "OOS_n", "OOS_mean_bps", "OOS_t", "OOS_sharpe", "OOS_hit"]].round(2).to_string())
per = R_[~R_.index.isin(agg.index)]
print(per.groupby(["bt", "cost"]).agg(n=("stock", "size"), med_IS=("IS_mean_bps", "median"), med_OOS=("OOS_mean_bps", "median"), frac_OOS_pos=("OOS_mean_bps", lambda x: (x > 0).mean()),
                                       n_OOS_t2=("OOS_t", lambda x: (x > 2).sum()), med_OOS_sharpe=("OOS_sharpe", "median")).round(2).to_string())
