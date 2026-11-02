"""s3: VİOP F_XU030 — zamanlama denetimi (bağımsız), spot saatlik segmentlerle hizalama, baz değişimi, VWAP testi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc, statsmodels.api as sm
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)

V = bc.viop_parse()
for rule in ["next", "vol"]:
    f = bc.fut_series(V, "D_XU030D", rule)
    f.to_parquet(f"{bc.RES}/s3_fxu030_{rule}.parquet")
f = pd.read_parquet(f"{bc.RES}/s3_fxu030_next.parquet")
fv = pd.read_parquet(f"{bc.RES}/s3_fxu030_vol.parquet")
P("ön vade (next) ile en hacimli aynı sözleşme payı:", round((f.code == fv.reindex(f.index).code).mean(), 4))
s = pd.read_parquet(f"{bc.RES}/s2_XU030.parquet")  # spot + isy saatlik
s["s_o11"] = np.log(s.p11 / s.o) if "p11" in s else np.nan
s["s_11c"] = np.log(s.c / s.p11)
tw = s[[f"p{h}" for h in range(11, 19) if f"p{h}" in s]].copy()
s["twap"] = np.exp(np.log(pd.concat([s.o, tw], axis=1)).mean(axis=1))  # 10:00..18:00 saatlik zaman ağırlıklı (geometrik)
s["s_tw2c"] = np.log(s.c / s.twap); s["s_o2tw"] = np.log(s.twap / s.o)
J = f.join(s, how="inner")
J = J[J.f_intra.abs() < bc.LIM]
J["d_intra"] = J.f_intra - J.intra
J["b_open"] = np.log(J.open / J.o); J["b_close"] = np.log(J.close / J.c)
P(f"ortak gün: {len(J)}  {J.index.min().date()}..{J.index.max().date()}")

# 1) zamanlama: ACILIS sabah mı?
P("\n[1] Zamanlama korelasyonları (yıl): corr(f_gapc, s_gap), corr(f_gapc, s_o11), corr(f_intra, s_intra), corr(f_intra, s_11c), "
  "regresyon f_intra ~ s_o11 + s_11c (+ s_gap)")
for y, g in J.groupby(J.index.year):
    g = g.dropna(subset=["f_gapc", "gap", "s_o11", "s_11c", "f_intra"])
    X = sm.add_constant(g[["gap", "s_o11", "s_11c"]].values)
    r = sm.OLS(g.f_intra.values, X).fit()
    P(f"{y}: n={len(g)} c(fgap,sgap)={g.f_gapc.corr(g.gap):.2f} c(fgap,s_o11)={g.f_gapc.corr(g.s_o11):.2f} c(fint,sint)={g.f_intra.corr(g.intra):.2f} "
      f"c(fint,s11c)={g.f_intra.corr(g.s_11c):.2f} | b_gap={r.params[1]:.2f} b_o11={r.params[2]:.2f} b_11c={r.params[3]:.2f} R2={r.rsquared:.2f}")

# 2) yıllık tablo: vadeli gün-içi, spot segmentleri, baz
P("\n[2] Yıllık (bps/gün): f_intra, spot intra, s_o11 (10->11), s_11c (11->kapanış), d_intra=f-s, f_intra - s_11c (= vadeli 09:30->11:00 + baz değ.), b_open, b_close")
rows = []
for y, g in J.groupby(J.index.year):
    r = dict(year=y, n=len(g))
    for c in ["f_intra", "intra", "s_o11", "s_11c", "d_intra", "f_gap", "gap"]:
        r[c] = g[c].mean() * 1e4
    r["f_minus_s11c"] = (g.f_intra - g.s_11c).mean() * 1e4
    r["t_f_minus_s11c"] = bc.st(g.f_intra - g.s_11c)["t"]
    r["b_open"] = g.b_open.median() * 1e4; r["b_close"] = g.b_close.median() * 1e4
    rows.append(r)
T = pd.DataFrame(rows).set_index("year"); P(T.round(1).to_string()); T.to_csv(f"{bc.RES}/s3_years.csv")

# 3) VWAP testi: vadeli VWAP->KAPANIS vs spot TWAP->kapanış (aynı yönde mi? vadeli gün içinde spot gibi düşüyor mu?)
P("\n[3] VWAP: f_vw2c = ln(KAPANIS/VWAP), s_tw2c = ln(kapanış/TWAP10-18). corr ve ortalamalar (bps)")
for y, g in J.groupby(J.index.year):
    g = g.dropna(subset=["f_vw2c", "s_tw2c"])
    P(f"{y}: n={len(g)} f_vw2c {g.f_vw2c.mean()*1e4:6.1f} (t {bc.st(g.f_vw2c)['t']:.1f})  s_tw2c {g.s_tw2c.mean()*1e4:6.1f} (t {bc.st(g.s_tw2c)['t']:.1f})  "
      f"corr {g.f_vw2c.corr(g.s_tw2c):.2f} | f_o2vw {g.f_o2vw.mean()*1e4:6.1f} s_o2tw {g.s_o2tw.mean()*1e4:6.1f} corr {g.f_o2vw.corr(g.s_o2tw):.2f}")
for nm, a, b in [("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026"), ("2017-2026", "2017", "2026")]:
    g = J.loc[a:b]
    P(f"{nm}: -f_vw2c (VWAP'ta sat, kapanışta al) {bc.fmt(bc.st(-g.f_vw2c))} | -s_tw2c {bc.fmt(bc.st(-g.s_tw2c))}")
# akşam seansı VWAP'a giriyor mu? VWAP, gün içi [low,high] içinde mi ve spot TWAP'a göre baz sapması 2020-01-17 öncesi/sonrası
J["b_vw"] = np.log(J.vwap / J.twap) - (J.b_open + J.b_close) / 2
for nm, a, b in [("pre-AS 2017-03..2020-01-16", "2017-03-06", "2020-01-16"), ("post-AS 2020-01-17..2022", "2020-01-17", "2022-12-31"), ("2023-2026", "2023", "2026")]:
    g = J.loc[a:b]
    P(f"{nm}: VWAP baz sapması medyan {g.b_vw.median()*1e4:.1f} bps, sd {g.b_vw.std()*1e4:.1f}; corr(f_o2vw,s_o2tw) {g.f_o2vw.corr(g.s_o2tw):.2f}")

# 4) d_intra'nın kaynağı: spot gap ile ilişkisi ve 'vadeli 09:30 açılışı gap'in ne kadarını görmüş'
P("\n[4] f_gapc / s_gap oranı (regresyon eğimi, yıl) -> vadeli 09:30 açılışının spot 10:00 açılışındaki gece bilgisinin ne kadarını içerdiği")
for y, g in J.groupby(J.index.year):
    g = g.dropna(subset=["f_gapc", "gap"])
    r = sm.OLS(g.f_gapc.values, sm.add_constant(g.gap.values)).fit()
    P(f"{y}: eğim {r.params[1]:.2f}  sabit {r.params[0]*1e4:.1f} bps | d_intra ~ s_gap eğim {sm.OLS(g.d_intra.values, sm.add_constant(g.gap.values)).fit().params[1]:.2f}")

# 5) Vadeli aç-sat ve 'sentetik 11:00 girişi' (varsayım: 11:00 sonrası vadeli spotu izler)
P("\n[5] Stratejiler (bps/gün brüt): A vadeli aç-sat = -f_intra; B spot 11:00->kapanış kısa = -s_11c (vadeli için baz değişimi ~0 varsayımı); C -f_vw2c")
for nm, a, b in [("2017-03..2020", "2017-03-06", "2020"), ("2021-2022", "2021", "2022"), ("2023-2026", "2023", "2026"), ("2017-2026", "2017", "2026"), ("2021-2026", "2021", "2026")]:
    g = J.loc[a:b]
    P(f"{nm:14s} A {bc.fmt(bc.st(-g.f_intra), ('n','mean','t','med'))} | B {bc.fmt(bc.st(-g.s_11c), ('mean','t','med'))} | C {bc.fmt(bc.st(-g.f_vw2c), ('mean','t'))}")
J.to_parquet(f"{bc.RES}/s3_join.parquet")
open(f"{bc.RES}/s3_viop.log", "w").write("\n".join(L))
