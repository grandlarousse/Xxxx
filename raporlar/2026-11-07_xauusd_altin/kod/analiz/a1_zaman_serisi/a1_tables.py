#!/usr/bin/env python3
"""a1_zaman_serisi — rapor tablolarını (markdown) CSV çıktılarından üretir → tables.md"""
import pandas as pd, numpy as np, json
D = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi"
def md(df, fl=2):
    df = df.copy()
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(((str(int(v)) if float(v).is_integer() and abs(v) > 3 else f"{v:.{fl}f}") if isinstance(v, (float, np.floating)) and np.isfinite(v) else ("" if isinstance(v, float) else str(v))) for v in r.values) + " |")
    return "\n".join(out)
R = pd.read_csv(f"{D}/ic_results.csv")
T = []
g = R.groupby(["fam", "src"]).apply(lambda x: pd.Series(dict(test=len(x), t2=int((x.t.abs() >= 2).sum()),
        is_oos_t2=int(((x.t_is.abs() >= 2) & (x.t_oos.abs() >= 2) & (np.sign(x.t_is) == np.sign(x.t_oos))).sum()), maks_t=x.t.abs().max()))).reset_index()
T.append("### T1. IC testleri aile × kaynak özeti (h=1,3,5 birlikte)\n" + md(g))
a = R[(R.src == "spot") & (R.fam == "a_mom")].copy()
p = a.pivot_table(index="feat", columns="h", values=["t", "t_is", "t_oos", "t_e"]); p.columns = [f"{x}_h{h}" for x, h in p.columns]
order = [f"ret{k}" for k in [1, 2, 3, 5, 10, 20, 60, 120, 250]] + [f"vsr{k}" for k in [1, 2, 3, 5, 10, 20, 60, 120, 250]]
p = p.reindex(order).reset_index()
T.append("### T2. (a) Geçmiş getiri → fwd: NW t (spot 15:00 UTC sinyal, VİOP hedef); t_e = erken spot 2010-2016\n" + md(p[["feat"] + [c for c in p.columns if c.startswith("t_h") or c.startswith("t_e_h")]]))
b = R[(R.src == "spot") & (R.fam.isin(["b_trend", "c_rev", "d_vol", "g_intraday", "e_micro"]))].copy()
p = b.pivot_table(index=["fam", "feat"], columns="h", values=["t", "t_is", "t_oos", "t_e"]); p.columns = [f"{x}_h{h}" for x, h in p.columns]
p = p.reset_index()
T.append("### T3. (b)(c)(d)(g) spot sinyaller: NW t tam / IS / OOS / erken\n" + md(p[["fam", "feat", "t_h1", "t_is_h1", "t_oos_h1", "t_e_h1", "t_h5", "t_is_h5", "t_oos_h5", "t_e_h5"]]))
m = R[R.src.isin(["mt", "mt1", "gvz"])].copy()
p = m.pivot_table(index=["feat", "src"], columns="h", values=["t", "t_is", "t_oos"]); p.columns = [f"{x}_h{h}" for x, h in p.columns]
T.append("### T4. (d) GVZ ve (e)(f) VİOP mikro yapı: mt = gün t (cutoff SONRASI), mt1 = gün t-1 (temiz)\n" + md(p.reset_index()))
B = pd.read_csv(f"{D}/bt_results.csv")
T.append("### T5. Klasik kurallar backtest (spot 15:00 sinyal → VİOP uzlaşma, 5 bps, kademeli). shdm = drift çıkarılmış Sharpe; early = spot 2010-2016\n" +
         md(B[["strat", "h", "sh_full", "shdm_full", "shdm_is", "shdm_oos", "sh_oos", "shdm_oos_10", "long_shdm_oos", "short_shdm_oos", "expo", "turn", "t_dm_full", "yrs_pos_dm", "early_shdm"]]))
B2 = pd.read_csv(f"{D}/bt2_results.csv")
T.append("### T6. Kuyruk momentumu ve oynaklık rejimi backtestleri\n" + md(B2[["strat", "h", "sh_full", "shdm_full", "shdm_is", "shdm_oos", "sh_oos", "shdm_oos10", "strict5dm_oos",
         "long_shdm_oos", "short_shdm_oos", "expo", "turn", "t_dm_full", "t_dm_is", "t_dm_oos", "yrs_pos", "e_shdm", "e_t"]]))
T.append("### T7. IS seçimi (spot kaynak, |t_IS| en büyük) ve tek seferlik OOS\n" + md(pd.read_csv(f"{D}/is_secim.csv")))
T.append("### T8. IS seçimi (backtest, IS demeaned Sharpe en büyük)\n" + md(pd.read_csv(f"{D}/is_secim2.csv")))
L = pd.read_csv(f"{D}/lowmom_robust.csv")
T.append("### T9. LOWMOM (sakin piyasa momentumu) sağlamlık\n" + md(L.drop(columns="by_year")))
T.append("### T10. LOWMOM yıllık demeaned Sharpe (VİOP)\n" + md(L[L.sig == "LOWMOM_k5(base)"][["h", "by_year"]]))
T.append("### T11. LOWMOM spot yıllık demeaned Sharpe 2011-2025 (spot hedef)\n" + md(pd.read_csv(f"{D}/lowmom_spot_by_year.csv")))
T.append("### T12. VOLREG komşuluk duyarlılığı\n" + md(pd.read_csv(f"{D}/volreg_sensitivity.csv")))
T.append("### T13. VOLREG bacaklar × dönem (spot hedef)\n" + md(pd.read_csv(f"{D}/volreg_spot_periods.csv").drop(columns="yr")))
T.append("### T14. Rejim payları (yıl içi gün oranı)\n" + md(pd.read_csv(f"{D}/volreg_regime_share.csv").set_index("date").T.reset_index()))
T.append("### T15. Sağlamlık (IC)\n" + md(pd.read_csv(f"{D}/robust_ic.csv")))
T.append("### T16. Sağlamlık (backtest, demeaned Sharpe, t)\n" + md(pd.read_csv(f"{D}/robust_bt.csv")))
T.append("### T17. Placebo (s<0 = gelecek bilgisi, s>0 = daha eski bilgi), Spearman IC\n" + md(pd.concat([pd.read_csv(f"{D}/placebo.csv"), pd.read_csv(f"{D}/placebo_lowmom.csv")]), 3))
T.append("### T18. Gün içi segment / konum: spot hedefle dönem kıyası\n" + md(pd.read_csv(f"{D}/seg_spot_target.csv")))
open(f"{D}/tables.md", "w").write("\n\n".join(T))
print("ok")
