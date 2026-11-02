"""10:30 girişli (işlenebilir) fade'in 47 hissede BH-FDR'si + ilk 30 dk'nın yönüne göre koşullu kırılım."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
from scipy import stats as st
E5 = pd.read_csv(OUT + "/res_e5_h1_delay.csv").set_index("sym")
for col in ["open_t", "e0730_gap_t", "e0830_gap_t"]:
    p = 2 * (1 - st.norm.cdf(E5[col].abs().values)); rej = bh(p)
    print(f"{col}: t>2 olan {int((E5[col]>2).sum())}/47, BH-FDR geçen {int(rej.sum())} ({list(E5.index[rej])}), en yüksek {E5[col].idxmax()} t={E5[col].max():.2f} p={p.min():.4f} (BH eşiği rank1 {0.05/47:.4f})")
print("10:30 girişte net>0 hisse sayısı:", int((E5.e0730_gap_bps > 0).sum()), "/47 ; medyan", round(E5.e0730_gap_bps.median(), 1), "bps")
# koşullu: ilk 30 dk gap yönünde devam mı (cont) yoksa geri dönüş mü (rev)
pool = []
R4 = pd.read_csv(OUT + "/res_e4_all47.csv").set_index("sym")
for s in VIOP:
    d = decomp(s, start="2023-11-01"); H = h1(s); p1 = H[H.hm == 630].set_index("day")["c"].rename("p1")
    x = d.join(p1, how="inner").dropna(subset=["gap", "intra", "p1"]); x = x[(x.index >= "2023-12-01") & (x.p1 <= x.h * 1.0005) & (x.p1 >= x.l * 0.9995)]
    x = x[x.gap.abs() > 0.01].copy(); x["ra"] = np.log(x.p1 / x.o); x["rb"] = np.log(x.c / x.p1); x["sym"] = s; x["liq"] = R4.loc[s, "liq_grp"]; pool.append(x)
P = pd.concat(pool); P["state"] = np.where(np.sign(P.ra) == np.sign(P.gap), "ilk30dk_devam", "ilk30dk_geri_dönüş")
P["pn"] = -np.sign(P.gap) * P.rb - 0.001
for grp, Q in [("CIMSA", P[P.sym == "CIMSA"]), ("OYAKC", P[P.sym == "OYAKC"]), ("düşük likidite", P[P.liq == "düşük"]), ("hepsi", P)]:
    for stt in ["ilk30dk_devam", "ilk30dk_geri_dönüş"]:
        q = Q[Q.state == stt].pn.groupby(level=0).mean(); m, t, n = nw_mean_t(q.values)
        print(f"  {grp:15s} {stt:20s}: 10:30 giriş net10 {1e4*m:+6.1f} bps (t{t:+.2f}) n {n}")
