"""s4: Gün-içi giriş/çıkış saat ızgarası (spot XU030, İş Yatırım saatlik 2017+ ızgarası 10..18 + kapanış),
plasebo pencereleri, IS/OOS, uç değer; ayrıca vadeli için 'küçük gap günleri' testi (bayat ACILIS etkisi yok sayılabilecek günler)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc, statsmodels.api as sm
pd.set_option("display.width", 250)
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
s = pd.read_parquet(f"{bc.RES}/s2_XU030.parquet")
s = s[s.first_h == 11.0]  # 2017+ ızgarası (10:00 açılış, ilk saatlik 11:00)
s["p10"] = s.o; s["pC"] = s.c
pts = ["p10"] + [f"p{h}" for h in range(11, 19)] + ["pC"]
lab = {p: (p[1:] if p != "pC" else "K") for p in pts}
P(f"gün sayısı (2017+ ızgara) {len(s)}")
for nm, a, b in [("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026"), ("2017-2026", "2017", "2026")]:
    x = s.loc[a:b]
    P(f"\n== {nm}: KISA pozisyon brüt bps/gün (satır=giriş saati, sütun=çıkış), parantezde t")
    hdr = "giriş\\çıkış " + " ".join(f"{lab[q]:>11s}" for q in pts[1:])
    P(hdr)
    for i, pa in enumerate(pts[:-1]):
        row = []
        for pb in pts[1:]:
            j = pts.index(pb)
            if j <= i: row.append(" " * 11); continue
            r = -np.log(x[pb] / x[pa]); st = bc.st(r)
            row.append(f"{st['mean']:5.1f}({st['t']:4.1f})")
        P(f"{lab[pa]:>10s}  " + " ".join(row))
# 11:00 girişinin istikrarı
r11 = -np.log(s.pC / s.p11)
r12 = -np.log(s.pC / s.p12)
r14 = -np.log(s.pC / s.p14)
P("\n11:00->kapanış kısa (spot proxy), yıllık:", {y: round(v * 1e4, 1) for y, v in r11.groupby(r11.index.year).mean().items()})
P("12:00->kapanış kısa, yıllık:", {y: round(v * 1e4, 1) for y, v in r12.groupby(r12.index.year).mean().items()})
P("14:00->kapanış kısa, yıllık:", {y: round(v * 1e4, 1) for y, v in r14.groupby(r14.index.year).mean().items()})
for nm, a, b in [("IS 2017-2020", "2017", "2020"), ("OOS 2021-2026", "2021", "2026"), ("2021-2022", "2021", "2022")]:
    P(f"11->K {nm}: {bc.fmt(bc.st(r11.loc[a:b]))}")
lo, hi, p0 = bc.block_boot(r11, "Y"); P(f"11->K yıl-blok bootstrap GA [{lo:.1f},{hi:.1f}] P<=0 {p0:.3f}")
ss = r11.dropna(); srt = ss.sort_values(ascending=False)
for k in [10, 20, 50]:
    P(f"11->K en iyi {k} gün çıkarılınca {bc.fmt(bc.st(ss.drop(srt.index[:k])))}; simetrik kırpma {bc.fmt(bc.st(ss.drop(srt.index[:k]).drop(srt.index[-k:])))}")
P(f"11->K winsor %2.5: {bc.fmt(bc.st(ss.clip(ss.quantile(.025), ss.quantile(.975))))}")
P("11->K haftanın günü:", {k: round(v * 1e4, 1) for k, v in ss.groupby(ss.index.dayofweek).mean().items()})
# Plasebo: rastgele saatlik pencere (aynı uzunlukta, 7 saat) yok; bunun yerine 'gece' penceresi ile karşılaştır ve günlük işaret permütasyonu
rng = np.random.default_rng(7)
perm = []
v = ss.values
for _ in range(5000):
    sg = rng.choice([-1, 1], size=len(v)); perm.append((v * sg).mean())
P(f"işaret-permütasyon p (ortalama >= gözlenen): {(np.array(perm) >= v.mean()).mean():.4f}")
# Vadeli: küçük gap günleri (bayat ACILIS'in önemsiz olduğu günler)
J = pd.read_parquet(f"{bc.RES}/s3_join.parquet")
J = J[J.f_gapc.abs() < bc.LIM]
for thr in [0.0015, 0.0025, 0.005]:
    for nm, a, b in [("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026")]:
        g = J.loc[a:b]; g = g[g.gap.abs() < thr]
        P(f"|s_gap|<{thr*100:.2f}% {nm}: n={len(g)} vadeli aç-sat {bc.st(-g.f_intra)['mean']:.1f} (t {bc.st(-g.f_intra)['t']:.1f}) | spot aç-sat {bc.st(-g.intra)['mean']:.1f} (t {bc.st(-g.intra)['t']:.1f})"
          f" | spot 11->K {bc.st(-g.s_11c)['mean']:.1f} | d_intra {bc.st(g.d_intra)['mean']:.1f} (t {bc.st(g.d_intra)['t']:.1f})")
# regresyon sabiti: f_intra = a + b1 s_gap + b2 s_o11 + b3 s_11c  (a = bayatlık düzeltmesi sonrası vadeli-spot gün-içi farkı)
for nm, a, b in [("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026")]:
    g = J.loc[a:b].dropna(subset=["gap", "s_o11", "s_11c", "f_intra"])
    r = sm.OLS(g.f_intra.values, sm.add_constant(g[["gap", "s_o11", "s_11c"]].values)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    P(f"{nm}: f_intra = {r.params[0]*1e4:.2f} bps (t {r.tvalues[0]:.2f}) + {r.params[1]:.2f} s_gap + {r.params[2]:.2f} s_o11 + {r.params[3]:.2f} s_11c")
open(f"{bc.RES}/s4_grid.log", "w").write("\n".join(L))
