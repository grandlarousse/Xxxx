"""(a) devam: yalnız emsal artığı P (t kapanışında bilinen) ile işlem kuralı, örtüşmeyen işlemler, maliyet, IS/OOS, yıllar.
Kural: |Pz|>thr -> yön(Pz) hisse VİOP vadelisi (raw) ya da hisse - beta x F_XU030 (hedged), settle t -> settle t+h.
Maliyet: 8 / 15 bps gidiş-dönüş + hisse bazlı (y_viop_likidite rt_cost_small); hedged'e +3 bps (XU030 bacağı).
Havuz: hedef çiftlerin tüm işlemleri, giriş tarihine göre kümelenmiş t. Plasebo: hedef olmayan çiftler.
"""
import numpy as np, pandas as pd, klib as K
from a_peers import TARGET, B, ASIA
cost_small, cost_1m = K.cost_table()
F = K.fut_panel(); Sp = K.spot_panel()
rows = []; trades_all = []
for mode in ["H", "DF", "DS"]:
    sig = pd.read_pickle(K.RES + f"/a_sig_{mode}.pkl")
    if mode in ("H", "DF"):
        R = F; mk = F["XU030"]; start = "2023-12-05" if mode == "H" else "2017-03-06"; split = "2025-05-01" if mode == "H" else "2022-01-01"
    else:
        R = Sp; mk = Sp["XU100"]; start = "2014-01-01"; split = "2021-01-01"
    w = 120 if mode == "H" else 250; mp = 40 if mode == "H" else 60
    betaS = K.roll_beta(R[K.STOCKS], mk, 250, 60)
    pairs = [(bk, s) for bk in sig for s in K.STOCKS]
    for bk, s in pairs:
        tp = s in TARGET.get(bk, [])
        P = sig[bk].reindex(R.index); Pz = K.sdscale(P, w, mp)
        Pz = Pz[Pz.index >= start]
        for h in (1, 2, 3):
            for tg in ("raw", "hedged"):
                y = K.fwd(R[s], h) if tg == "raw" else K.fwd(R[s], h) - betaS[s] * K.fwd(mk, h)
                y = y[y.index >= start]
                if not tp and tg == "raw":  # plasebo için yalnız hedged + raw ikisini de tut ama ayrıntısız
                    pass
                for thr in ([0.5, 1.0, 1.5] if tp else [1.0]):
                    tr = K.trades_nonoverlap(Pz, y, h, thr)
                    if len(tr) < 5: continue
                    extra = 3 if tg == "hedged" else 0
                    yrs = (y.dropna().index[-1] - y.dropna().index[0]).days / 365.25
                    st8 = K.trade_stats(tr, 8 + extra, split, yrs); st15 = K.trade_stats(tr, 15 + extra, split, yrs)
                    cs = cost_small.get(s, 10) + extra; stc = K.trade_stats(tr, cs, split, yrs)
                    rows.append(dict(mode=mode, basket=bk, stock=s, target_pair=tp, h=h, tgt=tg, thr=thr, n=st8["n"], per_yr=st8["per_yr"],
                                     gross=st8["gross"], net8=st8["net"], t8=st8["t_net"], net15=st15["net"], t15=st15["t_net"],
                                     cost_stock=cs, net_c=stc["net"], t_c=stc["t_net"], hit8=st8["hit"],
                                     IS_n=st8["IS_n"], IS_net8=st8["IS_net"], IS_t8=st8["IS_t"], OOS_n=st8["OOS_n"], OOS_net8=st8["OOS_net"], OOS_t8=st8["OOS_t"],
                                     yrs_pos=st8["yrs_pos"], by_year=st8["by_year"]))
                    if thr == 1.0:
                        tt = tr.copy(); tt["mode"] = mode; tt["basket"] = bk; tt["stock"] = s; tt["h"] = h; tt["tgt"] = tg; tt["tp"] = tp
                        trades_all.append(tt.reset_index())
    print(mode, "bitti", flush=True)
O = pd.DataFrame(rows); O.to_csv(K.RES + "/a2_trades_summary.csv", index=False)
T = pd.concat(trades_all, ignore_index=True); T.to_parquet(K.RES + "/a2_trades_all.parquet")
# havuz
out = []
for (mode, h, tg, tp), g in T.groupby(["mode", "h", "tgt", "tp"]):
    g = g.copy(); g["net8"] = g["gross"] * 1e4 - 8 - (3 if tg == "hedged" else 0)
    d = g.groupby("date")["net8"].mean()
    split = {"H": "2025-05-01", "DF": "2022-01-01", "DS": "2021-01-01"}[mode]
    def tt(x): return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 5 else np.nan
    out.append(dict(mode=mode, h=h, tgt=tg, target=tp, n_tr=len(g), n_dates=len(d), net8=g["net8"].mean(), t_clu=tt(d),
                    IS=d[d.index < split].mean(), IS_t=tt(d[d.index < split]), OOS=d[d.index >= split].mean(), OOS_t=tt(d[d.index >= split])))
Pp = pd.DataFrame(out); Pp.to_csv(K.RES + "/a2_pooled.csv", index=False)
pd.set_option("display.width", 250); print(Pp.round(2).to_string())
