"""Backtestler (look-ahead yok; yön IS 2014-2020'den seçilir, OOS 2021-2026 raporlanır). Maliyet 8/10/15 bps gidiş-dönüş.
BT1  TUR_{t-1} (günlük, ABD kapanışı) -> banka intra_t (açılıştan kapanışa)       [ABD seansı sinyali]
BT1h TUR_post (saatlik 15:30->ABD kapanışı, 2023-12+) -> intra_t
BT2  BBVA ADR_{t-1} ve BBVA.MC_{t-1} -> GARAN intra_t                              [BBVA sinyali]
BT3  gap_t (açılışta biliniyor) -> intra_t  (gap fade/continuation), |z|>1 filtresi, + TRY-vol rejim filtresi
BT3x Banka-özgü fazla gap (gap_b - beta*gap_XU100) -> fazla intra (pair: banka vs XU030 vadeli; maliyet x2)
BT4  ^MOVE_{t-1} -> XBANK intra_t (zayıf aday stres testi)
BT5  ES gece (15:00->06:00) -> intra (saatlik)
"""
import bk, ll, numpy as np, pandas as pd, json
SP = bk.SPLIT
res = []
def run(name, stock, signal, target, mode="sign", thr=0.0, costs=(0, 8, 10, 15), note="", force_dir=None):
    df = pd.concat([signal.rename("s"), target.rename("y")], axis=1).dropna()
    isd = df[(df.index >= bk.IS0) & (df.index < SP)]
    if force_dir is not None: d = force_dir
    elif len(isd) > 100: d = np.sign(isd["s"].corr(isd["y"])) or 1.0
    else:
        h = df[df.index < "2025-05-01"]; d = np.sign(h["s"].corr(h["y"])) or 1.0  # saatlik: ilk yarı "IS"
    for c in costs:
        r, pnl = ll.backtest(d * df["s"], df["y"], cost_bps=c, mode=mode, thr=thr)
        o = {"bt": name, "stock": stock, "dir": d, "cost": c, "note": note}
        for k in ["IS", "OOS", "ALL"]:
            for kk in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]:
                o[f"{k}_{kk}"] = r[k].get(kk, np.nan)
        o["by_year"] = json.dumps(r["by_year_bps"]); res.append(o)
# --- BT1
for s in bk.ALL:
    run("BT1_TURlag1_intra", s, bk.R("TUR").shift(1), bk.dec(s, "intra"))
# --- BT1h
H = pd.read_parquet(bk.RES + "/hourly_signals.parquet")
for s in ["XBANK", "GARAN", "AKBNK", "YKBNK", "ISCTR", "HALKB", "VAKBN"]:
    run("BT1h_TURpost_intra", s, H["TUR_post"], bk.dec(s, "intra"), note="2023-12+; yön ilk yarıdan")
    run("BT5h_ESovn_intra", s, H["ES_ovn"], bk.dec(s, "intra"), note="2023-12+; yön ilk yarıdan")
# --- BT2
run("BT2_BBVAadr_lag1_GARANintra", "GARAN", bk.R("BBVA").shift(1), bk.dec("GARAN", "intra"))
run("BT2_BBVAmc_lag1_GARANintra", "GARAN", bk.R("BBVA.MC").shift(1), bk.dec("GARAN", "intra"))
run("BT2h_BBVApost_GARANintra", "GARAN", H["BBVA_post"], bk.dec("GARAN", "intra"), note="2023-12+")
# --- BT3 gap fade
trv = bk.R("TRY=X").rolling(20).std().shift(1)  # t-1'e kadar bilinen (FX düzeltilmiş: TRY_{t-1} 00:00 t'de biliniyor)
trv_med = trv.rolling(500, min_periods=250).median()
hi = (trv > 1.5 * trv_med)
for s in bk.ALL:
    g = bk.dec(s, "gap"); it = bk.dec(s, "intra")
    run("BT3_gap_intra_all", s, g, it)
    run("BT3_gap_intra_z1", s, g, it, mode="z", thr=1.0)
    run("BT3_gap_intra_z1_TRYvolHI", s, g.where(hi.reindex(g.index).fillna(False).astype(bool)), it, mode="z", thr=1.0, note="sadece TRY 20g vol > 1.5x 2y medyan")
    run("BT3_gap_intra_z1_TRYvolLO", s, g.where(~(hi.reindex(g.index).fillna(True).astype(bool))), it, mode="z", thr=1.0, note="TRY vol normal")
xg = bk.dec("XU100", "gap"); xi = bk.dec("XU100", "intra")
for s in bk.BANKS + ["XBANK"]:
    g = bk.dec(s, "gap"); it = bk.dec(s, "intra")
    # beta: geçmiş 250g kayan (look-ahead yok)
    df = pd.concat([g.rename("g"), xg.rename("xg"), it.rename("i"), xi.rename("xi")], axis=1)
    bg = (df.g.rolling(250, min_periods=120).cov(df.xg) / df.xg.rolling(250, min_periods=120).var()).shift(1)
    bi = (df.i.rolling(250, min_periods=120).cov(df.xi) / df.xi.rolling(250, min_periods=120).var()).shift(1)
    exg = df.g - bg * df.xg; exi = df.i - bi * df.xi
    run("BT3x_exgap_exintra_z1", s, exg, exi, mode="z", thr=1.0, costs=(0, 16, 20, 30), note="pair (banka - beta*XU030 vadeli): maliyet 2 bacak")
# --- BT4
run("BT4_MOVElag1_intra", "XBANK", bk.R("^MOVE").shift(1), bk.dec("XBANK", "intra"))
run("BT4_MOVElag1_intra_z1", "XBANK", bk.R("^MOVE").shift(1), bk.dec("XBANK", "intra"), mode="z", thr=1.0)
B = pd.DataFrame(res); B.to_csv(bk.RES + "/backtests.csv", index=False)
pd.set_option("display.width", 220)
c = ["bt", "stock", "dir", "IS_n", "IS_mean_bps", "IS_t", "IS_sharpe", "OOS_n", "OOS_mean_bps", "OOS_t", "OOS_sharpe", "OOS_hit"]
print(B[B.cost == 10][c].round(2).to_string(index=False))
