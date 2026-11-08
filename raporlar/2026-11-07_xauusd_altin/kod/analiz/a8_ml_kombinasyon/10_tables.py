"""Rapor tabloları (markdown) üret: tablolar.md"""
from common import *
R = pd.read_csv(f"{OUT}/eval_all.csv")
def md(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else str(v) for v in r.values) + " |")
    return "\n".join(lines)
out = []
for V, per in [("V1", ["VAL", "OOS", "ALL"]), ("V2", ["VAL", "OOS", "ALL"]), ("V3", ["EARLY"])]:
    for pn in per:
        q = R[(R.V == V) & (R.period == pn)][["model", "h", "r2_hm", "r2_0", "cw_t_hm", "cw_t_0", "ic", "ic_t", "hit", "hit_base_long", "tim_sharpe", "tim_sharpe_dm", "tim_long_sharpe", "tim_short_sharpe", "tim_sharpe_10bps", "raw_sharpe", "tim_bh_sharpe", "tim_turnover"]].copy()
        q["r2_hm"] = (q.r2_hm * 100).round(2); q["r2_0"] = (q.r2_0 * 100).round(2)
        out.append(f"\n#### {V} — {pn} (R² yüzde)\n\n" + md(q.round(3)))
pm = pd.read_csv(f"{OUT}/permimp_groups.csv").pivot_table(index="group", columns=["model", "h"], values="d_mse_1e6").round(2)
pm.columns = [f"{a}_h{b}" for a, b in pm.columns]
out.append("\n#### Permütasyon önemi (grup, OOS MSE artışı ×1e6; negatif = grup OOS'ta zarar veriyor)\n\n" + md(pm.reset_index()))
pb = pd.read_csv(f"{OUT}/permimp_base.csv"); pb["oos_r2_hm"] *= 100; pb["oos_r2_0"] *= 100
out.append("\n#### Statik model (2017-03..2021-12 eğitim → 2022+ test) temel OOS performansı (R² yüzde)\n\n" + md(pb.round(3)))
rb = pd.read_csv(f"{OUT}/robust.csv"); rb = rb[rb.check.str.startswith("bagimsiz")].groupby(["V", "model", "h"])[["r2_hm", "r2_0", "ic"]].mean().reset_index()
rb["r2_hm"] *= 100; rb["r2_0"] *= 100
out.append("\n#### Örtüşmesiz (her h günde bir) alt örneklemler, h ofsetleri ortalaması (R² yüzde)\n\n" + md(rb.round(3)))
open(f"{OUT}/tablolar.md", "w").write("# a8 ek tablolar (otomatik üretildi: 10_tables.py)\n" + "\n".join(out))
print("ok")

# kompakt VAL/OOS/ALL tabloları (compact_tables.md)
def md2(df):
    cols = list(df.columns); L = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        L.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else (f"{v:.2f}" if isinstance(v, float) else str(v)) for v in r.values) + " |")
    return "\n".join(L)
outc = []
for V in ["V1", "V2"]:
    q = R[(R.V == V) & (R.period.isin(["VAL", "OOS", "ALL"]))].copy()
    q["r2hm%"] = q.r2_hm * 100; q["r2_0%"] = q.r2_0 * 100
    p = q.pivot_table(index=["model", "h"], columns="period", values=["r2hm%", "r2_0%", "cw_t_hm", "ic_t", "tim_sharpe", "tim_sharpe_dm", "tim_long_sharpe", "tim_short_sharpe", "tim_sharpe_10bps"]).round(2)
    p.columns = [f"{a}_{b}" for a, b in p.columns]
    p = p[["r2hm%_VAL", "r2hm%_OOS", "r2_0%_OOS", "cw_t_hm_VAL", "cw_t_hm_OOS", "ic_t_VAL", "ic_t_OOS", "ic_t_ALL", "tim_sharpe_VAL", "tim_sharpe_OOS", "tim_sharpe_dm_OOS", "tim_long_sharpe_OOS", "tim_short_sharpe_OOS", "tim_sharpe_10bps_OOS"]].reset_index()
    outc.append(f"\n### {V}\n\n" + md2(p))
open(f"{OUT}/compact_tables.md", "w").write("# Kompakt tablolar (10_tables.py): R² yüzde, Sharpe net 5 bps (10bps ayrı), zamanlama pozisyonu\n" + "\n".join(outc))
print("compact ok")
