"""h6: (1) 2017'deki büyük IC (0,226) VİOP'a özgü mü? spot ile kıyas, VİOP hacmi; (2) panel-diff ile ABD-günü sinyali arasındaki farkın kaynağı (TR tatil sonrası çok-günlük farklar)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
d = load_viop(); sp = load_spot(); idx = d.index
x = miner_resid(d, "y_GDXJ"); xs = miner_resid(sp, "y_GDXJ")
# VİOP hedefi yerine aynı günlerde spot 15:00→15:00 hedef (xau_p15)
g = np.log(d.xau_p15); s3 = g.shift(-3) - g
for yr in range(2017, 2027):
    m = idx.year == yr; ms = sp.index.year == yr
    a = ic(x[m], d.fwd3[m], 5); b = ic(x[m], s3[m], 5); c = ic(xs[ms], sp.sfwd3[ms], 5)
    print(yr, f"VİOP fwd3 ic={a['ic']:.3f} t={a['t']:.2f} | aynı gün spot p15 hedef ic={b['ic']:.3f} t={b['t']:.2f} | spot panel ic={c['ic']:.3f} | VİOP med hacim={d.v_volume[m].median():.0f}")
for nm, m in (("IS", idx <= IS_END), ("OOS", idx > IS_END), ("full", idx == idx)):
    b = ic(x[m], s3[m], 5); print("VİOP günleri, spot p15 hedef", nm, round(b["ic"], 3), round(b["t"], 2))
# VİOP-spot hedef farkı ile sinyal
dif = d.fwd3 - s3
print("fark (VİOP fwd3 − spot p15 3g) ile sinyal IC:", {k: round(v, 3) for k, v in split_stats(x, dif, 3).items() if k != "by_year"})
# (2) panel diff çok günlük mü? y_GDXJ_avail farkı
av = pd.to_datetime(d.y_GDXJ_avail)
gap = (av - av.shift(1)).dt.days
print("y_GDXJ_avail ardışık fark (gün) dağılımı:", gap.value_counts().sort_index().to_dict())
multi = gap >= 4  # hafta sonu 3 gün normal; ≥4 = arada ABD işlem günü atlanmış (TR tatili) ya da uzun ABD tatili
print("çok-günlük fark gün sayısı:", int(multi.sum()), " bu günlerde |z| ort:", round(x[multi].abs().mean(), 2), " diğer:", round(x[~multi].abs().mean(), 2))
for nm, m in (("IS", idx <= IS_END), ("OOS", idx > IS_END), ("full", idx == idx)):
    a = ic(x[m & ~multi], d.fwd3[m & ~multi], 5); print("çok-günlük farklar hariç", nm, round(a["ic"], 3), round(a["t"], 2))
