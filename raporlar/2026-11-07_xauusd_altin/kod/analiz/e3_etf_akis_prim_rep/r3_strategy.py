"""E3-1/E3-2 strateji: m_t<0 -> madenci ETF'yi t kapanışında al, t+1 kapanışında sat (yalnız uzun; ters ETF'li)."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
sig = pd.read_parquet(f"{OUT}/sig_m.parquet"); days = sig.index
EXT = {"2008": ("2008-01-01", "2008-12-31"), "2013-04": ("2013-04-01", "2013-04-30"), "2020-03": ("2020-03-01", "2020-03-31"), "2026-01/02": ("2026-01-01", "2026-02-28")}
def simple_ret(t):
    c = yh(t).reindex(days); return np.expm1(np.log(c).diff())
# ters ETF gerçekleşen kaldıracını 2019-2020 civarında ölç (kaldıraç değişim tarihi)
for inv, und in [("JDST", "GDXJ"), ("DUST", "GDX")]:
    ri = np.log(yh(inv).reindex(days)).diff(); ru = np.log(yh(und).reindex(days)).diff()
    for a, b in [("2019-07-01", "2020-02-28"), ("2020-03-01", "2020-03-31"), ("2020-04-01", "2020-06-30"), ("2020-07-01", "2021-06-30")]:
        dd = pd.concat([ri[a:b], ru[a:b]], axis=1).dropna()
        print(inv, a, b, "beta", round(np.polyfit(dd.iloc[:, 1], dd.iloc[:, 0], 1)[0], 2), "n", len(dd))
def Lser(idx, inv):
    return pd.Series(np.where(idx < pd.Timestamp("2020-04-01"), 3.0, 2.0), index=idx) if inv in ("DUST", "JDST") else pd.Series(2.0, index=idx)
out = []
def evaluate(tgt, inv, pred="m", thr=0.0, h=1, costs=((10, 20), (20, 40), (40, 80)), label=""):
    R = simple_ret(tgt); x = sig[pred]
    pos_long = ((x < -thr) & x.notna()).astype(float)
    pos_inv = pos_long - ((x > thr) & x.notna()).astype(float)
    Ri = simple_ret(inv) if inv else None
    first_inv = Ri.first_valid_index() if inv else None
    Rv = R.dropna()
    bh = seg_sh(Rv)
    for cl, ci in costs:
        net, wl, _ = run_bt(pos_long, Rv, h, cl)
        # demeaned: (a) tam örneklem ortalaması, (b) her segmentin kendi ortalaması
        dmA, _, _ = run_bt(pos_long, Rv - Rv.mean(), h, cl)
        Roos = Rv.copy(); Roos[Roos.index > IS_END] -= Rv[Rv.index > IS_END].mean(); Roos[Roos.index <= IS_END] -= Rv[Rv.index <= IS_END].mean()
        dmB, _, _ = run_bt(pos_long, Roos, h, cl)
        sh = seg_sh(net); shA = seg_sh(dmA); shB = seg_sh(dmB)
        entries = ((wl > 0) & (wl.shift(1).fillna(0) == 0)).sum() / len(wl) * 252
        ex = {k: round(net[a:b].sum() * 100, 2) if len(net[a:b]) else np.nan for k, (a, b) in EXT.items()}
        msk = pd.Series(True, index=net.index)
        for a, b in EXT.values(): msk[a:b] = False
        yr = net.groupby(net.index.year).sum()
        row = dict(target=tgt, label=label, pred=pred, thr=thr, h=h, mode="long_only", cost=f"{cl}", sh_full=sh["full"], sh_IS=sh["IS"], sh_OOS=sh["OOS"], sh_22=sh["s22"],
                   dmA_OOS=shA["OOS"], dmB_OOS=shB["OOS"], dmA_IS=shA["IS"], bh_IS=bh["IS"], bh_OOS=bh["OOS"], expo=round(wl.mean(), 3), entries_yr=round(entries, 1),
                   ann_OOS=round(net[net.index > IS_END].mean() * 252 * 100, 2), t_OOS=round(net[net.index > IS_END].mean() / net[net.index > IS_END].std() * np.sqrt((net.index > IS_END).sum()), 2),
                   sh_full_exext=sharpe(net[msk]), sh_OOS_exext=sharpe(net[msk & (net.index > IS_END)]), yrs_pos=f"{int((yr > 0).sum())}/{len(yr)}", **{f"x_{k}": v for k, v in ex.items()})
        out.append(row)
        if inv is None: continue
        Rr = Rv[Rv.index >= first_inv]
        neti, wli, wsi = run_bt(pos_inv, Rr, h, cl, inv=dict(R=Ri, L=Lser(Rr.index, inv), cost=ci))
        Rdm = Rr - Rr.mean(); Ridm = Ri - Ri[Ri.index >= first_inv].mean()
        dmi, _, _ = run_bt(pos_inv, Rdm, h, cl, inv=dict(R=Ridm, L=Lser(Rr.index, inv), cost=ci))
        legS, _, _ = run_bt(pos_inv.clip(upper=0), Rr, h, 0, inv=dict(R=Ri, L=Lser(Rr.index, inv), cost=0))
        legL, _, _ = run_bt(pos_long, Rr, h, 0)
        sh = seg_sh(neti); shd = seg_sh(dmi)
        ex = {k: round(neti[a:b].sum() * 100, 2) if len(neti[a:b]) else np.nan for k, (a, b) in EXT.items()}
        msk = pd.Series(True, index=neti.index)
        for a, b in EXT.values(): msk[a:b] = False
        yr = neti.groupby(neti.index.year).sum()
        out.append(dict(target=tgt, label=label, pred=pred, thr=thr, h=h, mode=f"inverse_{inv}", cost=f"{cl}/{ci}", sh_full=sh["full"], sh_IS=sh["IS"], sh_OOS=sh["OOS"], sh_22=sh["s22"],
                        dmA_OOS=shd["OOS"], dmA_IS=shd["IS"], bh_IS=seg_sh(Rr)["IS"], bh_OOS=seg_sh(Rr)["OOS"], legL_OOS=seg_sh(legL)["OOS"], legS_OOS=seg_sh(legS)["OOS"],
                        legS_ann_OOS=round(legS[legS.index > IS_END].mean() * 252 * 100, 2),
                        sh_full_exext=sharpe(neti[msk]), yrs_pos=f"{int((yr > 0).sum())}/{len(yr)}", **{f"x_{k}": v for k, v in ex.items()}))
evaluate("GDXJ", "JDST", label="E3-1 ana")
evaluate("GDX", "DUST", label="E3-2 ana")
evaluate("GDXJ", None, pred="m14", costs=((10, 20),), label="m14")
evaluate("GDX", None, pred="m14", costs=((10, 20),), label="m14")
evaluate("GDX", None, pred="zm", thr=1.5, costs=((10, 20),), label="GDX IS seçimi thr1.5")
# IS seçim ızgarası (GDXJ, yalnız uzun, demeaned IS Sharpe): eşik ve h
grid = []
for tgt in ["GDXJ", "GDX"]:
    R = simple_ret(tgt).dropna()
    for thr in (0.0, 1.0, 1.5, 2.0):
        for h in (1, 3, 5):
            x = sig.zm if thr > 0 else sig.m
            pos = ((x < -thr) & x.notna()).astype(float)
            dm, _, _ = run_bt(pos, R - R.mean(), h, 10)
            nt, _, _ = run_bt(pos, R, h, 10)
            grid.append(dict(target=tgt, thr=thr, h=h, dmA_IS=seg_sh(dm)["IS"], dmA_OOS=seg_sh(dm)["OOS"], sh_IS=seg_sh(nt)["IS"], sh_OOS=seg_sh(nt)["OOS"]))
g = pd.DataFrame(grid); print(g.to_string())
o = pd.DataFrame(out); o.to_csv(f"{OUT}/r3_strategy.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
print(o.T.to_string())
# başabaş maliyet OOS
for tgt in ["GDXJ", "GDX"]:
    R = simple_ret(tgt).dropna(); pos = ((sig.m < 0) & sig.m.notna()).astype(float)
    n0, wl, _ = run_bt(pos, R, 1, 0)
    turn = wl.diff().abs().reindex(n0.index)
    oo = n0.index > IS_END
    print(tgt, "OOS başabaş gidiş-dönüş bps:", round(n0[oo].mean() / turn.shift(1)[oo].mean() * 2e4, 1))
