"""5 dk 'endeks önde' etkisinin fiyat adımı (tick) ayrıklığıyla ilişkisi. BIST pay fiyat adımları (TL): <20:0,01; 20-50:0,02; 50-100:0,05; 100-250:0,10;
250-500:0,25; 500-1000:0,50; 1000-2500:1,00; >=2500:2,50 (Borsa İstanbul pay piyasası fiyat adımı tablosu; '?': 2026 itibarıyla doğrulanmalı)."""
import sys
from ye_common import *
tag = sys.argv[1] if len(sys.argv) > 1 else "yh_m5"
def tick(p):
    for lim, t in [(20, .01), (50, .02), (100, .05), (250, .10), (500, .25), (1000, .5), (2500, 1.0)]:
        if p < lim: return t
    return 2.5
R = pd.read_csv(RES + f"/intraday_{tag}.csv"); L = pd.read_csv(RES + "/viop_liquidity.csv", index_col=0)
rows = []
for s in VIOP:
    p = (f"{SCR}/data/m5/{s}.IS.parquet" if tag.startswith("yh") else f"{ISY}/m5/{s}.parquet")
    if not os.path.exists(p): continue
    d = pd.read_parquet(p); c = d["c"] if "c" in d else d["px"]
    if tag.startswith("isy"): c = c[c.index >= "2026-01-01"]
    rr = np.log(c).diff(); raw_px = ll.raw(s + ".IS")["c"].iloc[-60:].median()
    rows.append({"stock": s, "zero_bar_frac": (rr == 0).mean(), "rel_tick_bps": 1e4 * tick(raw_px) / raw_px})
T = pd.DataFrame(rows).set_index("stock")
f = R[(R.per == "full") & (R["var"] == "ex") & (R.dir == "idx->stk")]
out = []
for I, g in f.groupby("idx"):
    g = g.set_index("stock").join(T).join(L)
    out.append({"idx": I, "spearman(lag_share,zero_bar)": g.lag_share.corr(g.zero_bar_frac, method="spearman"), "spearman(lag_share,rel_tick)": g.lag_share.corr(g.rel_tick_bps, method="spearman"),
                "spearman(lag_share,log_turnover)": g.lag_share.corr(g.log_turnover_2021, method="spearman"), "spearman(b0,zero_bar)": g.b0.corr(g.zero_bar_frac, method="spearman")})
O = pd.DataFrame(out); print(O.round(3).to_string()); O.to_csv(RES + f"/tick_{tag}.csv", index=False); T.to_csv(RES + f"/tickinfo_{tag}.csv")
print(T.sort_values("zero_bar_frac").round(3).T.to_string())
