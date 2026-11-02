"""(a)+(d) 47 hisse: corr(gap,intra) ve |gap|>%1 fade (10 bps) IS 2014-20 / IS' 2016-20 / OOS 2021+; likidite grupları; BH-FDR.
Ayrıca piyasa (XU100) gap'i ile hisseye özgü gap ayrıştırması: intra_i ~ gap_i^idio + gap_XU100 (NW)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
from scipy import stats as st
X = decomp("XU100")
rows = []; pool = []
for s in VIOP:
    d = decomp(s)
    d = d.join(X[["gap", "intra"]].add_prefix("x_"), how="left")
    d = d.dropna(subset=["gap", "intra"])
    r = dict(sym=s, first=d.index.min().date(), n=len(d))
    for lab, msk in [("all", d.index >= "2014"), ("IS", d.index < SPLIT), ("IS16", (d.index >= "2016") & (d.index < SPLIT)), ("OOS", d.index >= SPLIT)]:
        x = d[msk]
        if len(x) < 100: continue
        r[f"corr_{lab}"] = x.gap.corr(x.intra)
        b, t, n = nw_ols(x.intra.values, np.column_stack([np.ones(len(x)), x.gap.values]))
        r[f"t_reg_{lab}"] = t[1]
        y = x[x.gap.abs() > 0.01]
        p = -np.sign(y.gap) * y.intra - 0.0010
        m, tt, nn = nw_mean_t(p.values)
        r[f"fade_{lab}_bps"] = 1e4 * m; r[f"fade_{lab}_t"] = tt; r[f"fade_{lab}_n"] = nn
    # hisseye özgü gap: gap_i - beta*gap_XU (beta OOS dışı: tüm dönem, sadece ayrıştırma amaçlı)
    z = d.dropna(subset=["x_gap"]); z = z[z.index >= "2016"]
    bet = np.cov(z.gap, z.x_gap)[0, 1] / z.x_gap.var()
    idio = z.gap - bet * z.x_gap
    b, t, n = nw_ols(z.intra.values, np.column_stack([np.ones(len(z)), idio.values, z.x_gap.values]))
    r.update(beta_gap=bet, b_idio=b[1], t_idio=t[1], b_mkt=b[2], t_mkt=t[2])
    yrs = d[d.index >= "2016"]; yy = yrs[yrs.gap.abs() > 0.01]; pp = -np.sign(yy.gap) * yy.intra - 0.0010
    yr = pp.groupby(pp.index.year).mean(); r["yrs_pos16"] = int((yr > 0).sum()); r["n_yrs16"] = len(yr)
    r["tlv_med_2021"] = float(d.loc[d.index >= SPLIT, "tlv"].median() / 1e6)  # milyon TL
    r["tlv_med_2025"] = float(d.loc[d.index >= "2025", "tlv"].median() / 1e6)
    rows.append(r)
    q = d[["gap", "intra", "x_gap", "tlv"]].copy(); q["sym"] = s; pool.append(q)
R = pd.DataFrame(rows)
R["liq_grp"] = pd.qcut(R.tlv_med_2025.rank(method="first"), 3, labels=["düşük", "orta", "yüksek"])
R["p_oos"] = 2 * (1 - st.norm.cdf(R.fade_OOS_t.abs())); R["fdr_oos"] = bh(R.p_oos.values)
R["p_reg_oos"] = 2 * (1 - st.norm.cdf(R.t_reg_OOS.abs())); R["fdr_reg_oos"] = bh(R.p_reg_oos.values)
R.to_csv(OUT + "/res_e4_all47.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 50)
cols = ["sym", "liq_grp", "tlv_med_2025", "corr_IS", "corr_OOS", "t_reg_OOS", "fade_IS_bps", "fade_IS_t", "fade_IS16_bps", "fade_OOS_bps", "fade_OOS_t", "fade_OOS_n", "fdr_oos", "yrs_pos16", "n_yrs16", "t_idio", "t_mkt"]
print(R[cols].sort_values("fade_OOS_t", ascending=False).round(2).to_string(index=False))
print("\nÖzet: corr_OOS aralığı", R.corr_OOS.min().round(3), R.corr_OOS.max().round(3), "medyan", R.corr_OOS.median().round(3), "; negatif:", (R.corr_OOS < 0).sum(), "/", len(R))
print("fade OOS net10 >0:", (R.fade_OOS_bps > 0).sum(), "; t>2:", (R.fade_OOS_t > 2).sum(), "; FDR:", R.fdr_oos.sum(), "; IS&OOS ikisi de >0:", ((R.fade_IS_bps > 0) & (R.fade_OOS_bps > 0)).sum())
print(R.groupby("liq_grp")[["tlv_med_2025", "corr_IS", "corr_OOS", "fade_IS_bps", "fade_IS16_bps", "fade_OOS_bps", "t_idio", "t_mkt"]].median().round(2))
# Havuz (eşit ağırlıklı günlük portföy): her gün |gap|>%1 olan hisselerde fade, gün ortalaması
P = pd.concat(pool); P = P[P.index >= "2014"]
P["liq"] = P.sym.map(R.set_index("sym").liq_grp)
for lab, msk in [("IS", P.index < SPLIT), ("IS16", (P.index >= "2016") & (P.index < SPLIT)), ("OOS", P.index >= SPLIT)]:
    for lg in ["düşük", "orta", "yüksek", "hepsi"]:
        x = P[msk & (P.gap.abs() > 0.01)]
        if lg != "hepsi": x = x[x.liq == lg]
        pn = (-np.sign(x.gap) * x.intra - 0.0010).groupby(level=0).mean()
        m, t, n = nw_mean_t(pn.values)
        print(f"havuz {lab:5s} {lg:7s}: günlük portföy net10 {1e4*m:+6.1f} bps (t {t:+.2f}) gün {n}  işlem {len(x)}")
