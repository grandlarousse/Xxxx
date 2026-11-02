"""s3b: VİOP 'ACILIS FIYATI' 2017–2022'de gece bilgisini içeriyor mu? (bayat vadeli açılışı vs spot açılış aşırılığı)
H_u (vadeli ACILIS bayat): s_o11 ~ s_gap eğimi ≈ 0; corr(f_gapc, ABD) < corr(s_gap, ABD); vadeli ACILIS büyük gap günlerinde gün dibi/tepesi.
H_e (spot açılışı aşırı tepki): s_o11 ~ s_gap eğimi belirgin negatif; corr(f_gapc, ABD) >= corr(s_gap, ABD)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc, statsmodels.api as sm
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
J = pd.read_parquet(f"{bc.RES}/s3_join.parquet")
J = J[J.f_gapc.abs() < bc.LIM]
_y = bc.yahoo("XU030.IS"); J["s_h"] = _y.h.reindex(J.index); J["s_l"] = _y.l.reindex(J.index)
# ABD: S&P 500 T-1 (ABD tarihi < BIST T) kapanıştan kapanışa ve ES gece (BIST kapanışı 15:00 UTC -> 06:00 UTC) mümkünse h1'den
spx = bc.yahoo("^GSPC").c
r_spx = np.log(spx / spx.shift(1))
# BIST günü T için: T'den önceki son ABD işlem günü
us_days = r_spx.index
idx = us_days.searchsorted(J.index, side="left") - 1
J["spx_prev"] = r_spx.values[np.clip(idx, 0, None)]
J.loc[idx < 0, "spx_prev"] = np.nan
P("Yıl | eğim(s_o11~s_gap) t | corr(s_gap,SPX_{T-1}) corr(f_gapc,SPX_{T-1}) corr(f_gap(uzl),SPX) | sd s_gap / sd f_gapc | ACILIS==gün dibi/tepesi payı |s_gap|>1% günlerde (vadeli; spot)")
for y, g in J.groupby(J.index.year):
    g = g.dropna(subset=["gap", "s_o11", "f_gapc", "spx_prev"])
    r = sm.OLS(g.s_o11.values, sm.add_constant(g.gap.values)).fit()
    big = g[g.gap.abs() > 0.01]
    ext_f = ((big.open <= big.low * (1 + 1e-9)) | (big.open >= big.high * (1 - 1e-9))).mean()
    ext_s = ((big.o <= big.s_l * (1 + 1e-7)) | (big.o >= big.s_h * (1 - 1e-7))).mean()
    P(f"{y}: {r.params[1]:+.2f} ({r.tvalues[1]:+.1f}) | {g.gap.corr(g.spx_prev):.2f} {g.f_gapc.corr(g.spx_prev):.2f} {g.f_gap.corr(g.spx_prev):.2f} | "
      f"{g.gap.std()*1e4:.0f}/{g.f_gapc.std()*1e4:.0f} | n_big={len(big)} vadeli {ext_f:.2f} spot {ext_s:.2f}")
# ABD regresyonu: hangi açılış ABD bilgisini daha çok taşıyor
P("\nβ(SPX_{T-1}) : s_gap, f_gapc, f_intra, s_intra (yıl)")
for y, g in J.groupby(J.index.year):
    g = g.dropna(subset=["gap", "f_gapc", "spx_prev"])
    b = {}
    for c in ["gap", "f_gapc", "f_intra", "intra", "s_o11", "s_11c"]:
        rr = sm.OLS(g[c].values, sm.add_constant(g.spx_prev.values)).fit(); b[c] = f"{rr.params[1]:+.2f}({rr.tvalues[1]:+.1f})"
    P(f"{y}: " + " ".join(f"{k}={v}" for k, v in b.items()))
# Açılış seansı fiyatı alanı (2022 sonu+) ile ACILIS ilişkisi
J["has_os"] = J.os_px.notna()
P("\nAçılış seansı fiyatı dolu gün payı (yıl):", J.has_os.groupby(J.index.year).mean().round(2).to_dict())
P("ACILIS == açılış seansı fiyatı (dolu günlerde):", ((J.open == J.os_px)[J.has_os]).groupby(J.index[J.has_os].year).mean().round(2).to_dict())
P("Açılış seansı işlem sayısı medyan (yıl):", J.os_ntr.groupby(J.index.year).median().to_dict())
P("Açılış seansı hacmi medyan (mn TL):", (J.os_val.groupby(J.index.year).median() / 1e6).round(1).to_dict())
P("Günlük toplam hacim medyan (mn TL):", (J.val.groupby(J.index.year).median() / 1e6).round(0).to_dict())
P("Günlük işlem sayısı medyan:", J.ntr.groupby(J.index.year).median().to_dict())
# Geçiş noktası: açılış seansı başlangıcı etrafında ACILIS'in gece bilgisini içermesi (çeyreklik eğim f_gapc~s_gap)
P("\nÇeyreklik eğim f_gapc ~ s_gap (vadeli açılışın spot gap'ini ne kadar içerdiği):")
q = []
for p, g in J.groupby(J.index.to_period("Q")):
    g = g.dropna(subset=["gap", "f_gapc"])
    if len(g) < 30: continue
    r = sm.OLS(g.f_gapc.values, sm.add_constant(g.gap.values)).fit(); q.append(f"{p}:{r.params[1]:.2f}")
P(" ".join(q))
open(f"{bc.RES}/s3b_acilis.log", "w").write("\n".join(L))
