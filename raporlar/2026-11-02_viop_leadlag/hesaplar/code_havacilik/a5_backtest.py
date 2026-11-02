"""A5: Backtestler (look-ahead yok: sinyal = BIST açılışından (07:00 UTC) ÖNCE bilinen t-1 bilgisi; hedef = BIST gün-içi getiri (açılış->kapanış) t).
IS 2014(2015)-2020 / OOS 2021-2026. Maliyet 8 ve 15 bps gidiş-dönüş. Çıktı: res/a5_bt.csv, res/a5_years.csv, res/a5_summary.txt"""
from h import *
from h import _nwcorr
import json

SG = pd.read_parquet(RES + "/signals.parquet")  # a3_multi.py üretir

def zs(x, w=250):
    mu = x.rolling(w, min_periods=60).mean().shift(1); sd = x.rolling(w, min_periods=60).std().shift(1)
    return (x - mu) / sd

def run(name, sig, tgt, stock, mode="sign", thr=0.0, costs=(8, 15), note=""):
    out = []
    for c in costs:
        r, pnl = ll.backtest(sig, tgt, cost_bps=c, mode=mode, thr=thr)
        for per in ["IS", "OOS", "ALL"]:
            d = r[per]
            out.append({"bt": name, "stock": stock, "cost": c, "period": per, "mode": mode, "thr": thr, **{k: d.get(k, np.nan) for k in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]}, "note": note})
        if c == costs[0]:
            yrs = r["by_year_bps"]
    return out, yrs

if __name__ == "__main__":
    rows = []; years = []
    tv = {st: D(st) for st in STOCKS}
    # gün-içi hedef; sinyal t-1 bilgisi
    combo = (zs(SG["EUAIR_X"]).clip(-3, 3) + zs(SG["USAIR_X"]).clip(-3, 3) - zs(SG["TUR"]).clip(-3, 3))
    bz = SG["BZ"]; zbz = zs(bz)
    fx = R("TRY=X").where(R("TRY=X") != 0)
    tests = []
    for st in STOCKS:
        y = tv[st]["intra"]
        tests += [
            ("B1a_USAIR_X->intra", SG["USAIR_X"].shift(1), y, st, "z", 1.0, "ABD havayolu sepeti (SPX'e göre artık) z>1"),
            ("B1b_JETS_raw->intra", SG["JETS"].shift(1), y, st, "z", 1.0, "JETS ham z>1"),
            ("B1c_EUAIR_X->intra", SG["EUAIR_X"].shift(1), y, st, "z", 1.0, "Avrupa havayolu sepeti (STOXX'a göre artık) z>1"),
            ("B1d_COMBO->intra", combo.shift(1), y, st, "sign", 1.0, "z(EUAIR_X)+z(USAIR_X)-z(TUR) |.|>1"),
            ("B1e_COMBO_all->intra", combo.shift(1), y, st, "sign", 0.0, "COMBO her gün"),
            ("B2a_BrentShock->intra", (-np.sign(zbz) * (zbz.abs() > 2)).shift(1), y, st, "sign", 0.5, "Brent |z|>2 ise ters yön, gün-içi"),
            ("B2b_BrentShock->5d", (-np.sign(zbz) * (zbz.abs() > 2)).shift(1), y + sum(tv[st]["cc"].shift(-k) for k in range(1, 5)), st, "sign", 0.5, "Brent |z|>2 ters yön, açılıştan t+4 kapanışa (5g, üst üste binen; maliyet tek)"),
            ("B3_USDTRY->intra", fx.shift(1), y, st, "z", 1.0, "USDTRY (FX düzeltmeli) z>1 -> aynı yön"),
            ("B1f_COMBO_noBrentShock", (combo * (zbz.abs() <= 2)).shift(1), y, st, "sign", 1.0, "COMBO, Brent şok günleri hariç"),
        ]
    # B4 yurt içi: THYAO_cc(t-1) -> PGSUS intra
    tests.append(("B4_THYAO->PGSUS_intra", tv["THYAO"]["cc"].shift(1), tv["PGSUS"]["intra"], "PGSUS", "z", 1.0, "THYAO cc z>1 -> PGSUS gün-içi"))
    tests.append(("B4b_PGSUS->TAVHL_intra", tv["PGSUS"]["cc"].shift(1), tv["TAVHL"]["intra"], "TAVHL", "z", 1.0, "PGSUS cc z>1 -> TAVHL gün-içi"))
    # B6 hisseye özgü: COMBO -> (hisse intra - beta*XU030 intra) (VİOP pay vadelisi + XU030 vadelisi hedge; maliyet 2x)
    xi = D("XU030")["intra"]
    for st in STOCKS:
        y = tv[st]["intra"]; df = pd.concat([y, xi], axis=1).dropna()
        b = df.iloc[:, 0].rolling(250, min_periods=120).cov(df.iloc[:, 1]) / df.iloc[:, 1].rolling(250, min_periods=120).var()
        hed = (y - b.shift(1).reindex(y.index) * xi)
        tests.append(("B6_COMBO->hedged_intra", combo.shift(1), hed, st, "sign", 1.0, "XU030 hedge'li gün-içi (maliyet 16/24 bps)"))
    for (nm, s, y, st, mode, thr, note) in tests:
        costs = (16, 24) if nm.startswith("B6") else (8, 15)
        o, yrs = run(nm, s, y, st, mode, thr, costs, note)
        rows += o; years.append({"bt": nm, "stock": st, **{str(k): v for k, v in yrs.items()}})
    # B5 saatlik: gece Brent hareketi (15:00->07:00 UTC) -> gün-içi (2024-06+)
    HP = pd.read_parquet(RES + "/a4_panel.parquet")
    for st in STOCKS:
        nbz = HP[(st, "BZ=F", "N")]; y = HP[(st, "_", "intra")]
        for thr in [0.0, 0.01]:
            r, pnl = ll.backtest(-nbz, y, cost_bps=8, mode="sign", thr=thr, split="2026-01-01")
            for per in ["IS", "OOS", "ALL"]:
                d = r[per]; rows.append({"bt": f"B5_nightBrent->intra_thr{thr}", "stock": st, "cost": 8, "period": per.replace("IS", "2024-25").replace("OOS", "2026"), "mode": "sign", "thr": thr, **{k: d.get(k, np.nan) for k in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]}, "note": "gece Brent ters yön; kısa örneklem"})
        # gece ABD havayolu (JETS 15:00->21:00) -> intra
        nj = HP[(st, "JETS", "N")]
        r, pnl = ll.backtest(nj, y, cost_bps=8, mode="sign", thr=0.005, split="2026-01-01")
        for per in ["IS", "OOS", "ALL"]:
            d = r[per]; rows.append({"bt": "B5b_nightJETS->intra_thr0.005", "stock": st, "cost": 8, "period": per.replace("IS", "2024-25").replace("OOS", "2026"), "mode": "sign", "thr": 0.005, **{k: d.get(k, np.nan) for k in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]}, "note": "BIST kapanışı sonrası JETS hareketi"})
    BT = pd.DataFrame(rows); BT.to_csv(RES + "/a5_bt.csv", index=False)
    YR = pd.DataFrame(years); YR.to_csv(RES + "/a5_years.csv", index=False)
    s = BT[(BT.cost.isin([8, 16])) | BT.bt.str.startswith("B5")].pivot_table(index=["bt", "stock"], columns="period", values=["mean_bps", "t", "sharpe", "n"]).round(2)
    s2 = BT[BT.cost.isin([15, 24])].pivot_table(index=["bt", "stock"], columns="period", values=["mean_bps", "sharpe"]).round(2)
    open(RES + "/a5_summary.txt", "w").write("MALİYET 8 (B6:16) bps\n" + s.to_string() + "\n\nMALİYET 15 (B6:24) bps\n" + s2.to_string() + "\n\nYILLAR (bps/işlem, düşük maliyet)\n" + YR.round(1).to_string())
    print("ok")
