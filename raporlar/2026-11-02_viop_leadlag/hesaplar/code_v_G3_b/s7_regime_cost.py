"""s7: Rejim (vadeli bazından ima edilen TL taşıma oranı) ve maliyet/likidite gerçekçiliği.
- ima edilen yıllık taşıma r = ln(F_uzl/S_kapanış) * 365 / takvim günü (ön vade, vade>=5 gün)
- aylık: spot 11->K kısa getirisi vs r ; spot aç-sat vs r ; ilk saat (10->11) vs r
- tik büyüklüğü (bps), açılış seansı hacmi, net getiri senaryoları (11->K vadeli proxy ve 2023+ açılış seansı girişli vadeli)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc, statsmodels.api as sm
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
J = pd.read_parquet(f"{bc.RES}/s3_join.parquet")
J = J[J.f_gapc.abs() < bc.LIM]
dte = (J.exp - J.index).dt.days
J["carry"] = np.where(dte >= 5, np.log(J.settle / J.c) * 365 / dte, np.nan)
# 2020-07 endeks bölünmesi: Yahoo XU030 ölçeği vs vadeli ölçeği farkını oran medyanıyla düzelt (yıl içi sabit)
ratio = np.log(J.settle / J.c)
J["carry"] = np.where(dte >= 5, (ratio - ratio.rolling(1).median().where(ratio.abs() < 0.5, np.nan).pipe(lambda x: 0)) * 365 / dte, np.nan)
# ölçek: 2020-07-27 öncesi vadeli fiyat = endeks/1000, Yahoo = endeks/100 -> ln(10) ekle
pre = J.index < "2020-07-27"
J.loc[pre, "carry"] = (np.log(J.settle[pre] * 10 / J.c[pre]) * 365 / dte[pre]).where(dte[pre] >= 5)
J.loc[J.carry.abs() > 1.5, "carry"] = np.nan
P("Yıllık medyan ima edilen taşıma (yıllık, %):", (J.carry.groupby(J.index.year).median() * 100).round(1).to_dict())
J["r11"] = -J.s_11c; J["aqs"] = -J.intra; J["o11"] = -J.s_o11; J["fa"] = -J.f_intra
M = J[["r11", "aqs", "o11", "fa", "carry"]].groupby(J.index.to_period("M")).mean().dropna()
for c in ["r11", "aqs", "o11", "fa"]:
    r = sm.OLS(M[c].values * 1e4, sm.add_constant(M.carry.values * 100)).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    P(f"aylık {c} (bps/gün) = {r.params[0]:.2f} + {r.params[1]:.3f} × taşıma(%)  t={r.tvalues[1]:.2f}  n_ay={len(M)}")
# taşıma terciline göre
J["cq"] = pd.qcut(J.carry, 3, labels=["düşük", "orta", "yüksek"])
for q, g in J.groupby("cq", observed=True):
    P(f"taşıma {q} (medyan %{g.carry.median()*100:.0f}): 11->K kısa {bc.st(g.r11)['mean']:.1f} (t {bc.st(g.r11)['t']:.1f}) | aç-sat spot {bc.st(g.aqs)['mean']:.1f} (t {bc.st(g.aqs)['t']:.1f}) | ilk saat kısa {bc.st(g.o11)['mean']:.1f} | vadeli aç-sat {bc.st(g.fa)['mean']:.1f}")
# reel faiz yaklaşık: 2021-2022 negatif reel faiz dönemi
# tik büyüklüğü: gün içi fiyatların ondalık ızgarası (KAPANIS, ACILIS, low, high) -> min pozitif fark
def tick(g):
    v = np.unique(np.round(np.concatenate([g.open.values, g.close.values, g.low.values, g.high.values, g.settle.values]), 6))
    d = np.diff(np.sort(v)); d = d[d > 1e-9]
    return np.round(d.min(), 4) if len(d) else np.nan
V = bc.viop_parse(); x = V[V.und == "D_XU030D"]
tk = x.groupby(x.date.dt.year).apply(tick)
px = J.close.groupby(J.index.year).median()
P("XU030 vadeli asgari fiyat adımı (gözlenen) ve bps karşılığı:", {y: (tk[y], round(tk[y] / px[y] * 1e4, 2)) for y in tk.index if y in px.index})
# net senaryolar
P("\nNet (bps/gün) — maliyet = gidiş-dönüş toplam (komisyon + spread/kayma):")
for nm, ser, a, b in [("spot-proxy 11->K (vadeli 11:00 kısa) 2017-2026", J.r11, "2017", "2026"), ("  aynı, 2021-2026", J.r11, "2021", "2026"),
                      ("  aynı, 2023-2026", J.r11, "2023", "2026"), ("vadeli aç-sat (açılış seansı) 2023-2026", J.fa, "2023", "2026"),
                      ("vadeli aç-sat 2023-01..2026-10 (açılış seansı tam yıl)", J.fa, "2023-01-01", "2026-12-31")]:
    s = ser.loc[a:b].dropna(); m = s.mean() * 1e4; sd = s.std() * 1e4
    P(f"{nm}: brüt {m:.1f} (t {bc.st(s)['t']:.1f}) | " + " | ".join(f"{c} bps→ {m-c:.1f} (SR {((m-c)/sd)*np.sqrt(250):.2f})" for c in [2, 4, 8]))
open(f"{bc.RES}/s7_regime_cost.log", "w").write("\n".join(L))
