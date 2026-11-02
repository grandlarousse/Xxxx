"""Backtestler (look-ahead yok): sinyal BIST açılışından (07:00 UTC) ÖNCE bilinir; hedef = gün-içi (açılış->kapanış) getiri.
IS 2014-2020 / OOS 2021-2026. Maliyet 8 ve 15 bps gidiş-dönüş (hedge'li stratejide 2 bacak -> 2x).
Sinyal tanımları ÖNCEDEN sabitlendi (sepet bileşimi tarama sonucuna göre değil, sektör tanımıyla)."""
import pandas as pd, numpy as np, elib
from elib import R, DEC, ll
xud = DEC("XU100")
tu = DEC("TUPRS"); pk = DEC("PETKM"); ej = DEC("ENJSA"); od = DEC("ODAS"); ak = DEC("AKSEN")
cr = elib.crack_ret()
basket = lambda syms: pd.concat([R(s) for s in syms], axis=1).mean(axis=1)
US_REF = basket(["VLO", "MPC", "PSX", "PBF"])
EU_REF = basket(["PKN.WA", "MOL.BD", "MOH.AT", "ELPE.AT", "NESTE.HE", "GALP.LS", "REP.MC", "OMV.VI"])
ASIA_PC = basket(["1301.TW", "1303.TW", "1326.TW", "011170.KS", "051910.KS"])  # BIST açılışından önce kapanır -> lag0 kullanılabilir
bz = R("BZ=F")
ptf = elib.ptf_daily(); lp = np.log(ptf.tl.clip(lower=1)); m7 = lp.rolling(7).mean().shift(-1)
cal = ll.bist_cal(); L = m7.reindex(m7.index.union(cal)).ffill().reindex(cal); L = L[L.index <= "2026-09-25"]; ptf_news = L.diff()

# Brent şok: geçmiş 250g std ile z (look-ahead yok)
zbz = (bz - bz.rolling(250, min_periods=60).mean().shift(1)) / bz.rolling(250, min_periods=60).std().shift(1)
shock = zbz.shift(1).abs() > 2

S = {
 "BT1_USREF_lag1->TUPRS_intra": (US_REF.shift(1), tu.intra, 1),
 "BT1h_USREF_lag1->TUPRS-XU100_intra": (US_REF.shift(1), tu.intra - xud.intra, 2),
 "BT1z_USREF_lag1(|z|>1)->TUPRS-XU100_intra": (US_REF.shift(1), tu.intra - xud.intra, 2),
 "BT1e_EUREF_lag1->TUPRS-XU100_intra": (EU_REF.shift(1), tu.intra - xud.intra, 2),
 "BT1x_XLE_lag1->TUPRS-XU100_intra": (R("XLE").shift(1), tu.intra - xud.intra, 2),
 "BT2_HOxBZ_lag1->TUPRS_intra": (cr.hoxbz.shift(1), tu.intra, 1),
 "BT2b_dC321_lag1->TUPRS_intra": (cr.d_c321.shift(1), tu.intra, 1),
 "BT2c_dHOcrack_lag1->TUPRS-XU100_intra": (cr.d_ho_crack.shift(1), tu.intra - xud.intra, 2),
 "BT3_BZ_lag1->TUPRS_intra(tüm günler)": (bz.shift(1), tu.intra, 1),
 "BT3a_BZşok(|z|>2)_lag1->TUPRS_intra(devam)": (bz.shift(1).where(shock, 0), tu.intra, 1),
 "BT3b_BZşok->TUPRS_gap_ters(fade)": ((-tu.gap).where(shock, 0), tu.intra, 1),
 "BT3c_fade_gap_tüm_günler(kontrol)": (-tu.gap, tu.intra, 1),
 "BT4_AsyaPetkim_lag0->PETKM_intra": (ASIA_PC, pk.intra, 1),
 "BT4h_AsyaPetkim_lag0->PETKM-XU100_intra": (ASIA_PC, pk.intra - xud.intra, 2),
 "BT5_PTFhaber(t-1)->ENJSA_intra": (ptf_news.shift(1), ej.intra, 1),
 "BT5b_PTFhaber(t-1)->AKSEN_intra": (ptf_news.shift(1), ak.intra, 1),
 "BT6_GC_lag1->ODAS_intra": (R("GC=F").shift(1), od.intra, 1),
}
rows = []; years = {}
for k, (sig, tgt, legs) in S.items():
    sig = sig[sig.index >= "2014-01-01"]
    for c in (8, 15):
        kw = dict(mode="z", thr=1.0) if "|z|>1" in k else dict(mode="sign", thr=0.0)
        res, pnl = ll.backtest(sig, tgt, cost_bps=c * legs, **kw)
        for per in ["IS", "OOS", "ALL"]:
            r = res[per]; rows.append({"strateji": k, "maliyet_bps": c * legs, "dönem": per, **{kk: r.get(kk) for kk in ["n", "mean_bps", "t", "hit", "sharpe", "ann_ret_pct", "maxdd_pct"]}})
        if c == 8: years[k] = res["by_year_bps"]
    # brüt (0 maliyet)
    res0, _ = ll.backtest(sig, tgt, cost_bps=0, **(dict(mode="z", thr=1.0) if "|z|>1" in k else dict(mode="sign", thr=0.0)))
    for per in ["IS", "OOS"]: rows.append({"strateji": k, "maliyet_bps": 0, "dönem": per, **{kk: res0[per].get(kk) for kk in ["n", "mean_bps", "t", "hit", "sharpe"]}})
B = pd.DataFrame(rows); B.to_csv(elib.RES + "/backtests.csv", index=False)
Y = pd.DataFrame(years).T; Y.to_csv(elib.RES + "/backtests_by_year_bps_cost8.csv")
pv = B[B.maliyet_bps.isin([0]) | (B.maliyet_bps == B.groupby("strateji").maliyet_bps.transform(lambda x: sorted(set(x))[1] if len(set(x)) > 1 else x.iloc[0]))]
show = B[B.dönem.isin(["IS", "OOS"])].pivot_table(index="strateji", columns=["maliyet_bps", "dönem"], values="sharpe", aggfunc="first").round(2)
print("Sharpe (maliyet_bps, dönem):"); print(show.to_string())
show2 = B[B.dönem.isin(["IS", "OOS"]) & (B.maliyet_bps == 0)].pivot_table(index="strateji", columns="dönem", values=["mean_bps", "t", "n"], aggfunc="first").round(1)
print("Brüt bps/işlem, t:"); print(show2.to_string())
print("Yıllık (8bps/bacak, bps/işlem) seçili:"); print(Y.loc[["BT1h_USREF_lag1->TUPRS-XU100_intra", "BT1e_EUREF_lag1->TUPRS-XU100_intra", "BT3b_BZşok->TUPRS_gap_ters(fade)"]].round(0).to_string())
