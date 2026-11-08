"""Görev 2 (havuz): genel kütüphanenin 31 sinyali × mod × h, 37 küme temsilcisinde havuzlanmış;
hafta-kümeli t (kesitsel bağımlılığa karşı), SPY beta-hedge'li getiri, BH-FDR (q=0.10, bu tablodaki testler).
Çıktı: sonuclar/aile_sektor_tematik/havuz_genel.csv"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *
import strategies as S

t0 = time.time()
ctx = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
gen = pd.read_csv(os.path.join(ROOT, "sonuclar", "genel_tum.csv"))
spy = gen[gen.sym == "SPY"].set_index(["sig", "mode", "h", "exit"])
rows = []
sigs = {}
for s in REPS:
    df = D(s)
    for name, fn in S.LIB.items():
        sigs[(s, name)] = fn(df, ctx).reindex(df.index).fillna(False).astype(bool)
for name in S.LIB:
    for mode in ("C0", "O1", "C1"):
        cfgs = [(h, "sabit") for h in (1, 2, 3)] + ([(3, "kural_max3")] if name in S.EXITS else [])
        for h, ex in cfgs:
            trs = []
            for s in REPS:
                es = S.EXITS[name](D(s)) if ex == "kural_max3" else None
                trs.append(run_sym(s, sigs[(s, name)], h, mode, exit_sig=es))
            tr = pd.concat(trs, ignore_index=True)
            r = summarize(tr, name)
            r.update({"sig": name, "mode": mode, "h": h, "exit": ex})
            k = (name, mode, h, ex)
            r["spy_net_bp"] = spy.loc[k, "mean_net_bp"] if k in spy.index else np.nan
            r["spy_t"] = spy.loc[k, "t"] if k in spy.index else np.nan
            rows.append(r)
res = pd.DataFrame(rows)
res["fdr10"] = lib.bh_fdr(res["p_cl"].values, 0.10)
res.to_csv(os.path.join(OUT, "havuz_genel.csv"), index=False)
print("test sayısı (havuz):", len(res), "FDR geçen:", int(res.fdr10.sum()), "süre", round(time.time() - t0), "sn")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 100)
cols = ["sig", "mode", "h", "exit", "n", "n_weeks", "mean_gross_bp", "mean_net_bp", "t_cl", "t_cl_ay", "t_wk_eq", "is_net_bp", "oos_net_bp", "is_t_cl", "oos_t_cl",
        "years_pos_frac", "pos_cl_frac", "mean_hedged_bp", "t_hedged_cl", "spy_net_bp", "spy_t", "fdr10"]
print(res.sort_values("t_cl", ascending=False)[cols].head(35).round(2).to_string())
print("\nFDR geçen ve net>0, IS>0, OOS>0:")
q = res[res.fdr10 & (res.mean_net_bp > 0) & (res.is_net_bp > 0) & (res.oos_net_bp > 0)]
print(q[cols].round(2).to_string())
