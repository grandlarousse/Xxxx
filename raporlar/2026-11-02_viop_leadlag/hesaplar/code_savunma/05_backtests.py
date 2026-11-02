"""05: Backtestler (look-ahead yok; IS 2014-2020 / OOS 2021-2026; maliyet 8 ve 15 bps gidiş-dönüş).
BT1  TKC parite sapması D_{t-1} (TKC ABD kapanışı t-1, kur ~00:00 UTC t) -> TCELL gün-içi_t (açılışta gir, kapanışta çık).
BT1u açılışta kalan sapma U = D_{t-1} - gap_t -> TCELL gün-içi_t (açılış fiyatı bilindikten sonra gir).  Kontrol: saf gap-fade.
BT1h saatlik (2023-12+): TKC post-close (15:30->kapanış) -> TCELL ilk saatten sonra (07:30 UTC -> kapanış).
BT2a EU_DEF_{t-1} -> ASELS gün-içi_t;  BT2b KR_DEF_t (06:30 UTC kapanır) -> ASELS gün-içi_t;  BT2c EU savunma post-close (saatlik) -> ASELS gün-içi_{t+1}.
BT3  EU_DEF anormal şok günü (|z|>2, STOXX'a göre) -> ASELS ertesi gün gün-içi, yön = sign(z).  BT3b olay listesi (rearm/war/peace) -> ASELS ertesi gün gün-içi.
"""
from sv import *
import statsmodels.api as sm, json
out = []
def run(name, sig, tgt, mode="sign", thr=0.0, note=""):
    for c in (8.0, 15.0):
        r, pnl = ll.backtest(sig, tgt, cost_bps=c, mode=mode, thr=thr)
        row = {"bt": name, "cost": c, "mode": mode, "thr": thr, "note": note}
        for k in ("IS", "OOS", "ALL"):
            for f in ("n", "mean_bps", "t", "hit", "sharpe", "maxdd_pct"): row[f"{k}_{f}"] = r[k].get(f, np.nan)
        row["by_year"] = json.dumps(r["by_year_bps"]); out.append(row)
    return r
# ---- BT1
T = pd.read_parquet(RES + "/02_tkc_daily.parquet")
dT = ll.decomp("TCELL"); D = T["D"].where(T["D"].abs() < 0.15)
sigD = D.shift(1).reindex(dT.index)
run("BT1 D->TCELL intra", sigD, dT["intra"])
run("BT1 D->TCELL intra |D|>50bps", sigD, dT["intra"], thr=0.005)
run("BT1 D->TCELL intra |D|>100bps", sigD, dT["intra"], thr=0.01)
U = sigD - dT["gap"]
run("BT1u U=D-gap->TCELL intra", U, dT["intra"])
run("BT1u U |U|>50bps", U, dT["intra"], thr=0.005)
run("KONTROL gap-fade (-gap)->TCELL intra", -dT["gap"], dT["intra"])
run("KONTROL gap-fade |gap|>50bps", -dT["gap"], dT["intra"], thr=0.005)
z = pd.concat([dT["intra"].rename("y"), sigD.rename("D"), dT["gap"].rename("g")], axis=1).dropna(); z = z[z.index >= "2014"]
for lab, s, e in [("ALL", "2014", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027")]:
    q = z[(z.index >= s) & (z.index < e)]; mm = sm.OLS(q.y, sm.add_constant(q[["D", "g"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(f"TCELL intra ~ D_(t-1) + gap_t [{lab}]: b_D {mm.params['D']:.3f} (t {mm.tvalues['D']:.2f})  b_gap {mm.params['g']:.3f} (t {mm.tvalues['g']:.2f}) n {len(q)}")
# TTKOM için aynı sinyal (yayılma)
dK = ll.decomp("TTKOM"); run("BT1 D->TTKOM intra", sigD.reindex(dK.index), dK["intra"])
# ---- BT1h saatlik
H = pd.read_parquet(RES + "/02b_h1.parquet")
run("BT1h tk_post->TCELL rest(07:30->kapanış)", H["tk_post"], H["TCELL_rest1"], note="2023-12+ (yalnız OOS)")
run("BT1h tk_post->TCELL intra", H["tk_post"], H["TCELL_intra1"], note="2023-12+")
run("BT1h tk_post |>50bps|->TCELL rest", H["tk_post"], H["TCELL_rest1"], thr=0.005, note="2023-12+")
# ---- BT2
dA = ll.decomp("ASELS")
eu = drv("EU_DEF"); kr = drv("KR_DEF")
run("BT2a EU_DEF(t-1)->ASELS intra", eu.shift(1).reindex(dA.index), dA["intra"])
run("BT2a EU_DEF(t-1) z>1->ASELS intra", eu.shift(1).reindex(dA.index), dA["intra"], mode="z", thr=1.0)
run("BT2b KR_DEF(t)->ASELS intra", kr.reindex(dA.index), dA["intra"])
run("BT2b KR_DEF(t) z>1->ASELS intra", kr.reindex(dA.index), dA["intra"], mode="z", thr=1.0)
eu_syms = ["RHM.DE", "BA.L", "LDO.MI", "SAAB-B.ST"]
post = pd.concat([np.log(ll.snap_daily(s, "16:40") / ll.snap_daily(s, "15:00")).rename(s) for s in eu_syms], axis=1).mean(axis=1)
post = post.reindex(ll.bist_cal()); post = post.where(post.abs() < 0.1)
run("BT2c EU_DEF post-close(t-1)->ASELS intra", post.shift(1).reindex(dA.index), dA["intra"], note="2023-12+")
# ---- BT3 şok günleri
F = pd.read_parquet(RES + "/03F_shock.parquet")
zs = F["z"].reindex(dA.index)
run("BT3 EU_DEF şok |z|>2 (t-1)->ASELS intra", zs.shift(1), dA["intra"], thr=2.0)
run("BT3 EU_DEF şok |z|>2 (t-1)->ASELS cc", zs.shift(1), dA["cc"], thr=2.0, note="kapanışta gir (BIST kapanışı EU kapanışından önce! -> sinyal t-1 EU kapanışı, giriş t-1 kapanışında DEĞİL t açılışında olmalı; cc yalnız referans, işlenemez)")
ev = pd.read_csv(CODE + "/events.csv", parse_dates=["bist_day0"])
sgn = pd.Series(0.0, index=dA.index)
for _, r in ev.iterrows():
    if r.type in ("war", "rearm", "peace"):
        p = dA.index.searchsorted(r.bist_day0)
        if p + 1 < len(dA.index): sgn.iloc[p + 1] = 1.0 if r.type in ("war", "rearm") else -1.0
q = pd.concat([sgn.rename("s"), dA["intra"].rename("y")], axis=1).dropna(); q = q[q.s != 0]
print("BT3b olay+1 gün-içi (yön tipe göre): n", len(q), "ort bps", round(1e4 * (q.s * q.y).mean(), 1), "isabet", round(((q.s * q.y) > 0).mean(), 2))
# ---- LISN.SW sürprizi mekanizma testi (TCELL intra_l1 FDR geçen tek sürücü)
li = R("LISN.SW")
for lab, s, e in [("IS", "2014", "2021"), ("OOS", "2021", "2027")]:
    c, t, n = tstat_corr(dT["intra"], li.shift(1), s, e); print(f"LISN.SW(t-1)->TCELL intra {lab}: corr {c:.3f} t {t:.2f} n {n}; sıfır getiri oranı {(li==0).mean():.2f}")
z = pd.concat([dT["intra"].rename("y"), li.shift(1).rename("li"), R("^SSMI").shift(1).rename("smi"), R("ES=F").shift(1).rename("es")], axis=1).dropna()
mm = sm.OLS(z.y, sm.add_constant(z[["li", "smi", "es"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5}); print("  LISN | SMI,ES kontrol: t", round(mm.tvalues["li"], 2))
O = pd.DataFrame(out); O.to_csv(RES + "/05_backtests.csv", index=False)
cols = ["bt", "cost", "IS_n", "IS_mean_bps", "IS_t", "IS_sharpe", "OOS_n", "OOS_mean_bps", "OOS_t", "OOS_hit", "OOS_sharpe"]
print(O[O.cost == 8.0][cols].round(2).to_string(index=False))
print("15 bps OOS sharpe:", O[O.cost == 15.0].set_index("bt")["OOS_sharpe"].round(2).to_dict())
print("BT1u yıllık (8bps):", O[(O.bt == "BT1u U=D-gap->TCELL intra") & (O.cost == 8.0)].by_year.values[0])
print("BT1 yıllık (8bps):", O[(O.bt == "BT1 D->TCELL intra") & (O.cost == 8.0)].by_year.values[0])
