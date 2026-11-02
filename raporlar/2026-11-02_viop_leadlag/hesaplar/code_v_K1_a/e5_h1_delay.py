"""(b)+(c) Zamanlama: h1 (2023-12+). intra = r_a [açılış->07:30 UTC (10:30 TSİ)] + r_b [07:30->kapanış].
Geri dönüş ilk 30 dk sürekli işlemde mi (açılış seansı fiyat baskısı/gürültü) yoksa gün boyu mu?
Gecikmeli giriş fade: sinyal (i) gap (açılış vs önceki kapanış; 07:00 UTC'de bilinir) (ii) gap2 = gap + r_a (giriş anına kadarki toplam gece+ilk saat)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
R4 = pd.read_csv(OUT + "/res_e4_all47.csv").set_index("sym")
rows = []; pool = []
for s in VIOP:
    d = decomp(s, start="2023-11-01"); H = h1(s)
    p1 = H[H.hm == 630].set_index("day")["c"].rename("p1")   # 07:30 UTC'de biten ilk saatlik bar kapanışı
    p2 = H[H.hm == 730].set_index("day")["c"].rename("p2")   # 08:30 UTC
    p3 = H[H.hm == 1130].set_index("day")["c"].rename("p3")  # 12:30 UTC
    x = d.join(p1, how="inner").join(p2, how="left").join(p3, how="left").dropna(subset=["gap", "intra", "p1"])
    x = x[x.index >= "2023-12-01"]
    # tutarlılık: saatlik fiyatlar günlük [l,h] aralığında olmalı (HEKTS 09/2024 saatlik veride bedelsiz düzeltmesi yok)
    for pc_ in ["p1", "p2", "p3"]:
        bad = (x[pc_] > x.h * 1.0005) | (x[pc_] < x.l * 0.9995); x.loc[bad, pc_] = np.nan
    x = x.dropna(subset=["p1"])
    x["ra"] = np.log(x.p1 / x.o); x["rb"] = np.log(x.c / x.p1)
    x["ra2"] = np.log(x.p2 / x.o); x["rb2"] = np.log(x.c / x.p2); x["rb3"] = np.log(x.c / x.p3)
    x["gap2"] = x.gap + x.ra; x["gap3"] = x.gap + x.ra2
    x["sym"] = s; pool.append(x)
    r = dict(sym=s, n=len(x))
    for col in ["intra", "ra", "rb", "rb2"]:
        b, t, n = nw_ols(x[col].values, np.column_stack([np.ones(len(x)), x.gap.values])); r[f"b_{col}"] = b[1]; r[f"t_{col}"] = t[1]
    b, t, n = nw_ols(x.rb.values, np.column_stack([np.ones(len(x)), x.gap2.values])); r["b_rb_on_gap2"] = b[1]; r["t_rb_on_gap2"] = t[1]
    def fade(sig, tgt, thr=0.01, cost=10):
        y = x[sig.abs() > thr]; p = -np.sign(sig[sig.abs() > thr]) * tgt[sig.abs() > thr] - cost / 1e4
        m, t, n = nw_mean_t(p.values); return 1e4 * m, t, n
    for lab, sig, tgt in [("open", x.gap, x.intra), ("e0730_gap", x.gap, x.rb), ("e0730_gap2", x.gap2, x.rb), ("e0830_gap", x.gap, x.rb2), ("e0830_gap3", x.gap3, x.rb2), ("e1230_gap", x.gap, x.rb3)]:
        m, t, n = fade(sig, tgt); r[f"{lab}_bps"] = m; r[f"{lab}_t"] = t; r[f"{lab}_n"] = n
    rows.append(r)
R = pd.DataFrame(rows).set_index("sym"); R["liq_grp"] = R4.liq_grp
R.to_csv(OUT + "/res_e5_h1_delay.csv")
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 60)
print(R.loc[["CIMSA", "OYAKC"]].round(2).T.to_string())
cols = ["liq_grp", "n", "b_intra", "t_intra", "b_ra", "t_ra", "b_rb", "t_rb", "open_bps", "open_t", "e0730_gap_bps", "e0730_gap_t", "e0730_gap2_bps", "e0830_gap_bps", "e1230_gap_bps", "open_n"]
print(R[cols].sort_values("open_t", ascending=False).round(2).to_string())
print(R.groupby("liq_grp")[["b_intra", "b_ra", "b_rb", "t_ra", "t_rb", "open_bps", "e0730_gap_bps", "e0730_gap2_bps", "e0830_gap_bps", "e1230_gap_bps"]].median().round(3))
print("medyan oran: ilk 30 dk'nın geri dönüşteki payı (b_ra/b_intra):", (R.b_ra / R.b_intra).median().round(2))
# havuz
P = pd.concat(pool); P["liq"] = P.sym.map(R.liq_grp)
print("\nHAVUZ (eşit ağırlıklı günlük portföy, 2023-12+, |sinyal|>%1, net 10 bps)")
for lg in ["düşük", "orta", "yüksek", "hepsi"]:
    Q = P if lg == "hepsi" else P[P.liq == lg]
    b, t, n = nw_ols(Q.intra.values, np.column_stack([np.ones(len(Q)), Q.gap.values])); bi = (b[1], t[1])
    b, t, n = nw_ols(Q.ra.values, np.column_stack([np.ones(len(Q)), Q.gap.values])); ba = (b[1], t[1])
    b, t, n = nw_ols(Q.rb.values, np.column_stack([np.ones(len(Q)), Q.gap.values])); bb = (b[1], t[1])
    out = [f"{lg:7s} regresyon eğimi gap->intra {bi[0]:+.3f} (t{bi[1]:+.1f}) | ->r_a(ilk30dk) {ba[0]:+.3f} (t{ba[1]:+.1f}) | ->r_b(10:30-kapanış) {bb[0]:+.3f} (t{bb[1]:+.1f})"]
    for lab, sc, tc in [("açılış", "gap", "intra"), ("10:30 gap", "gap", "rb"), ("10:30 gap2", "gap2", "rb"), ("11:30 gap", "gap", "rb2"), ("15:30 gap", "gap", "rb3")]:
        y = Q[Q[sc].abs() > 0.01]; pn = (-np.sign(y[sc]) * y[tc] - 0.0010).groupby(level=0).mean()
        m, t, n = nw_mean_t(pn.values); out.append(f"   {lab:11s}: {1e4*m:+6.1f} bps (t{t:+.2f}) gün {n} işlem {len(y)}")
    print("\n".join(out))
