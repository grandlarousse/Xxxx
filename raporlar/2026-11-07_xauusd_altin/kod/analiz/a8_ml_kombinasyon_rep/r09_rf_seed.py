"""Adım 9: A8-6 (V2 RF h3) tohum (random_state) duyarlılığı ve yıl yıl ayrıştırma.
Kaynaklar: analist preds_V2 (random_state=0), kendi mypreds_V2 (1), mypreds_V2_rf_s7_h3 (7). Ayrıca 3 tohum ortalaması."""
import numpy as np, pandas as pd
from rep_stats import ic_test, bt_full, bt, nw_t_mean
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
v = pd.read_parquet(f"{OUT}/base_viop.parquet")
def load(f):
    P = pd.read_parquet(f); P["date"] = pd.to_datetime(P.date); return P[(P.model == "rf") & (P.h == 3)].set_index("date").sort_index()
src = {"analist_s0": f"{S}/out/a8_ml_kombinasyon/preds_V2.parquet", "ben_s1": f"{OUT}/mypreds_V2.parquet", "ben_s7": f"{OUT}/mypreds_V2_rf_s7_h3.parquet"}
Q = {k: load(f) for k, f in src.items()}
Q["ort_3tohum"] = Q["ben_s1"].copy(); Q["ort_3tohum"]["yhat"] = sum(q.yhat.reindex(Q["ben_s1"].index) for q in Q.values() if q is not Q["ort_3tohum"]) / 3
y = v.fwd3
for k, q in Q.items():
    tim = q.yhat - q.ybar_w; pos = np.sign(tim)
    out = {}
    for pn, (a, b) in {"VAL": ("2020", "2021"), "OOS": ("2022", "2026"), "OOS_ex2026": ("2022", "2025")}.items():
        d = pd.concat([y.rename("y"), q.yhat.rename("f"), q.ybar.rename("b")], axis=1).loc[a:b].dropna()
        r2 = 1 - ((d.y - d.f) ** 2).sum() / ((d.y - d.b) ** 2).sum()
        cw = (d.y - d.b) ** 2 - ((d.y - d.f) ** 2 - (d.b - d.f) ** 2)
        it = ic_test(tim.loc[a:b], y.loc[a:b], 5)
        B = bt_full(pos.loc[a:b], v.ret.loc[a:b], 3)
        out[pn] = dict(r2_hm=round(r2 * 100, 3), cw_t=round(nw_t_mean(cw, 5), 2), ic=round(it["ic"], 3), ic_t=round(it["t"], 2), sh=B["sh"], sh_dm=B["sh_dm"], bh=B["bh"], long=B["long"], short=B["short"])
    z = bt(pos.loc["2020":], v.ret.loc["2020":], 3)["pnl"]
    out["yil_sharpe"] = z.groupby(z.index.year).apply(lambda g: round(float(g.mean() / g.std() * np.sqrt(252)), 2)).to_dict()
    print("=====", k)
    for kk, vv in out.items(): print("  ", kk, vv)
print("tohumlar arası OOS pozisyon uyumu:", {f"{a}-{b}": round(float((np.sign(Q[a].yhat - Q[a].ybar_w) == np.sign(Q[b].yhat - Q[b].ybar_w)).loc["2022":].mean()), 3)
                                         for a, b in (("analist_s0", "ben_s1"), ("analist_s0", "ben_s7"), ("ben_s1", "ben_s7"))})
