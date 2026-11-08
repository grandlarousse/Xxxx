"""s04: (3) örtüşme: pozisyon ve PnL korelasyonları, fenomen testleri, etkin bağımsız sinyal sayısı;
(4) önceden tanımlı eşit ağırlıklı birleşim (VİOP ve ETF ayrı), tam/IS/OOS/2022+/2026 ve 'yarıya indir' beklentisi;
(5b) oynaklık rejimine göre sinyal başarımı. P&L basit getiriyle (sabit nominal)."""
import json, numpy as np, pandas as pd
from sl import *
OUT = f"{S}/out/sentez"
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
VR = pd.read_parquet(f"{OUT}/sinyal_viop_ham.parquet"); ER = pd.read_parquet(f"{OUT}/sinyal_etf_ham.parquet")
VP = pd.read_parquet(f"{OUT}/poz_viop.parquet"); EP = pd.read_parquet(f"{OUT}/poz_etf.parquet")
res = {}
VSIG = {"V_LOWMOM_h1": 1, "V_QEND_h3": 3, "V_GDXJRES_h3": 3, "V_LAST1H_h5": 5}
ESIG = {"E_GDXTATIL_h1": ("GDX", 1), "E_C2J_h3": ("GDXJ", 3), "E_C2_h3": ("GDX", 3), "E_C1_h5": ("GLD", 5), "E_M_GDXJ_h1": ("GDXJ", 1)}
rE = {t: ret_of(t) for t in ["GDX", "GDXJ", "GLD"]}

# ---------- net PnL (basit getiri, temel maliyet)
VN = pd.DataFrame({k: bt_eff(eff_of(VR[k], h), RV.dropna(), 5.0)[0] for k, h in VSIG.items()})
EN = pd.DataFrame({k: bt_eff(eff_of(ER[k], h), rE[u].dropna(), 10.0)[0] for k, (u, h) in ESIG.items()})

def neff(C):
    lam = np.linalg.eigvalsh(C.values); lam = lam[lam > 0]
    return round(float(lam.sum() ** 2 / (lam ** 2).sum()), 2)

print("=== (3) Pozisyon korelasyonu (ham sinyal, tüm günler) VİOP"); C1 = VR[list(VSIG)].corr().round(2); print(C1)
print("=== Etkin (kademeli) pozisyon korelasyonu VİOP"); C1e = VP[list(VSIG)].corr().round(2); print(C1e)
print("=== Net PnL korelasyonu VİOP"); C2 = VN.corr().round(2); print(C2, "\nN_eff (PnL):", neff(VN.corr()))
print("=== Pozisyon korelasyonu ETF"); C3 = ER[list(ESIG)].corr().round(2); print(C3)
print("=== Etkin pozisyon korelasyonu ETF"); C3e = EP[list(ESIG)].corr().round(2); print(C3e)
print("=== Net PnL korelasyonu ETF"); C4 = EN.dropna(how="all").fillna(0).corr().round(2); print(C4, "\nN_eff (PnL):", neff(EN.dropna(how="all").fillna(0).corr()))
res["corr"] = dict(viop_poz=C1.to_dict(), viop_effpoz=C1e.to_dict(), viop_pnl=C2.to_dict(), etf_poz=C3.to_dict(), etf_effpoz=C3e.to_dict(), etf_pnl=C4.to_dict(),
                   neff_viop=neff(VN.corr()), neff_etf=neff(EN.dropna(how="all").fillna(0).corr()))
C1.to_csv(f"{OUT}/korelasyon_viop_poz.csv"); C2.to_csv(f"{OUT}/korelasyon_viop_pnl.csv"); C3.to_csv(f"{OUT}/korelasyon_etf_poz.csv"); C4.to_csv(f"{OUT}/korelasyon_etf_pnl.csv")

# ---------- fenomen testleri
F = {}
# (a) LOWMOM ile trend: aktif günlerde sign(5g) ile MA50 konumunun uyumu; trendi kontrol edince LOWMOM PnL'i kalıyor mu
pma = to_viop(sig_trend_pma50()).fillna(0)
tsm5 = to_viop(np.sign(np.log(SP.s_p15).diff(5))).fillna(0)
act = VR.V_LOWMOM_h1 != 0
F["lowmom_aktif_gun_payi"] = round(float(act.mean()), 3)
F["lowmom_vs_tsmom5_aktif_gunde_ayni_isaret"] = round(float((VR.V_LOWMOM_h1[act] == tsm5[act]).mean()), 3)
F["lowmom_vs_pma50_aktif_gunde_ayni_isaret"] = round(float((VR.V_LOWMOM_h1[act] == pma[act]).mean()), 3)
F["corr_lowmom_pma50_tumgun"] = round(float(VR.V_LOWMOM_h1.corr(pma)), 3)
# trend kuralı (PMA50, h1) ve koşulsuz TSMOM5 PnL'i; LOWMOM PnL'inin bunlara regresyonu (alfa t)
pnl_pma = bt_eff(eff_of(pma, 1), RV.dropna(), 5.0)[0]; pnl_ts5 = bt_eff(eff_of(tsm5, 1), RV.dropna(), 5.0)[0]
import statsmodels.api as sm
def alpha_t(y, X):
    d = pd.concat([y, X], axis=1).dropna(); m = sm.OLS(d.iloc[:, 0], sm.add_constant(d.iloc[:, 1:])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return dict(alfa_yillik_pct=round(m.params.iloc[0] * 252 * 100, 2), alfa_t=round(m.tvalues.iloc[0], 2), beta={k: round(v, 2) for k, v in m.params.iloc[1:].items()}, r2=round(m.rsquared, 3))
F["lowmom_pnl_vs_pma50_tsmom5"] = alpha_t(VN.V_LOWMOM_h1, pd.concat([pnl_pma.rename("PMA50"), pnl_ts5.rename("TSMOM5")], axis=1))
F["lowmom_pnl_corr_pma50"] = round(float(VN.V_LOWMOM_h1.corr(pnl_pma)), 3); F["lowmom_pnl_corr_tsmom5"] = round(float(VN.V_LOWMOM_h1.corr(pnl_ts5)), 3)
# (b) VİOP madenci artığı (A4-C1) ile ETF madenci artığı (E2-C2j) aynı öngörücü mü? (aynı ABD kapanışı t-1)
pg, zg = sig_gdxj_res_viop(); p2j, x2j, _, _ = sig_e2("GDXJ", 1, 0.7)
j = pd.concat([zg.rename("viop_z"), x2j.rename("etf_x")], axis=1).dropna()
F["A4C1_vs_E2C2j_ongorucu_spearman"] = round(float(j.viop_z.corr(j.etf_x, method="spearman")), 3)
# (c) madenci artığı ile altının gece/gün içi hareketi: artık (ABD kapanışı t-1) → altın [t-1 20:00 UTC → t 15:00 UTC] (VİOP girişinden ÖNCE)
gold_pre = np.log(V.xau_p15 / V.xau_p20_prev)
j2 = pd.concat([zg.rename("z"), gold_pre.rename("pre"), RV.shift(-1).rename("fwd1"), (RV.shift(-1) + RV.shift(-2) + RV.shift(-3)).rename("fwd3")], axis=1).dropna()
F["A4C1_z_vs_altin_giris_oncesi_spearman"] = round(float(j2.z.corr(j2.pre, method="spearman")), 3)
F["A4C1_z_vs_fwd3_spearman"] = round(float(j2.z.corr(j2.fwd3, method="spearman")), 3)
# kısmi: fwd3 ~ z + pre (sıra)
rk = j2.rank(); m = sm.OLS(rk.fwd3, sm.add_constant(rk[["z", "pre"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
F["A4C1_fwd3_kismi_t_z_kontrol_pre"] = round(float(m.tvalues["z"]), 2)
# ETF tarafı: GDXJ artığı (t-1) → altının t-1 16:00 ET → t 15:00 ET hareketi (m_t)
pm, mm = sig_m()
j3 = pd.concat([x2j.rename("x"), mm.rename("m")], axis=1).dropna()
F["E2C2j_x_vs_m_t_spearman"] = round(float(j3.x.corr(j3.m, method="spearman")), 3)
F["corr_poz_E_M_vs_C2J"] = round(float(ER.E_M_GDXJ_h1.corr(ER.E_C2J_h3)), 3)
# (d) E3-1 (altın 15:00 ET'ye kadar → GDXJ ters) ile LAST1H (altın 14→15 UTC → VİOP momentum): aynı bilgi mi?
lx = np.log(V.xau_p15 / V.xau_p14)
j4 = pd.concat([lx.rename("last1h"), mm.rename("m")], axis=1).dropna()
F["last1h_vs_m_t_spearman_ayni_tarih"] = round(float(j4.last1h.corr(j4.m, method="spearman")), 3)
# (e) madenci artığı → GLD (E2-C1) ile → GDXJ (E2-C2j): ETF pozisyon korelasyonu yukarıda; ayrıca VİOP GDXJRES ile E_C1 (k10) öngörücü
p1, x1, _, _ = sig_e2("GDX", 10, 0.8)
j5 = pd.concat([zg.rename("viop_z"), x1.rename("x10")], axis=1).dropna()
F["A4C1_vs_E2C1_ongorucu_spearman"] = round(float(j5.viop_z.corr(j5.x10, method="spearman")), 3)
# (f) tatil öncesi ve çeyrek sonu çakışması
F["qend_ve_gdx_tatil_ayni_hafta"] = int(sum(1 for d0 in VR.index[VR.V_QEND_h3 > 0] if (ER.E_GDXTATIL_h1[(ER.index >= d0 - pd.Timedelta(days=3)) & (ER.index <= d0 + pd.Timedelta(days=3))] > 0).any()))
res["fenomen"] = F
print(json.dumps(F, indent=1, ensure_ascii=False))

# ---------- (4) eşit ağırlıklı birleşim (ÖNCEDEN tanımlı ağırlık; sinyaller sonradan seçilmiştir)
def comb_viop(cost=5.0):
    eff = sum(eff_of(VR[k], h) for k, h in VSIG.items()) / len(VSIG)
    return eff
def comb_etf(cost=10.0, start=None, end=None):
    pnl = 0; effs = {}
    for u, ks in [("GDX", ["E_GDXTATIL_h1", "E_C2_h3"]), ("GDXJ", ["E_C2J_h3", "E_M_GDXJ_h1"]), ("GLD", ["E_C1_h5"])]:
        eff = sum(eff_of(ER[k], ESIG[k][1]) for k in ks) / len(ESIG)
        rr = cut(rE[u].dropna(), start, end)
        n, _ = bt_eff(eff, rr, cost); effs[u] = eff
        pnl = n if isinstance(pnl, int) else pnl.add(n, fill_value=0)
    return pnl, effs

rows = []
for nm, a, b in periods("VIOP"):
    rr = cut(RV.dropna(), a, b); eff = comb_viop()
    for ck, c in [("temel", 5.0), ("stres", 10.0)]:
        n, t = bt_eff(eff.reindex(rr.index).fillna(0), rr, c); dm, _ = bt_eff(eff.reindex(rr.index).fillna(0), rr, c, demean=True)
        bh, _ = bt_eff(pd.Series(1.0, index=rr.index), rr, 0)
        s = per_stats(n, t)
        rows.append(dict(cephe="VIOP", donem=nm, maliyet=ck, sharpe=s["sharpe"], yillik_pct=s["ann_pct"], vol_pct=s["vol_pct"], t=s["t"], sharpe_dm=per_stats(dm)["sharpe"],
                         bh_sharpe=per_stats(bh)["sharpe"], bh_yillik_pct=per_stats(bh)["ann_pct"], maruziyet=round(float(eff.reindex(rr.index).abs().mean()), 3), devir_yil=s["turn_yr"],
                         maxDD_pct=round(float((n.cumsum() - n.cumsum().cummax()).min() * 100), 1)))
for nm, a, b in periods("ETF"):
    for ck, c in [("temel", 10.0), ("stres", 20.0)]:
        n, effs = comb_etf(c, a, b)
        # B&H kıyası: eşit ağırlıklı GDX/GDXJ/GLD sepeti (1/3)
        bhs = sum(np.expm1(cut(rE[u].dropna(), a, b)) for u in ["GDX", "GDXJ", "GLD"]) / 3
        bhs = bhs.dropna()
        expo = sum(effs[u].reindex(n.index).abs() for u in effs)
        # maruziyet eşleşmeli alfa: strateji ~ a + b*sepet
        al = alpha_t(n, bhs.rename("sepet"))
        s = per_stats(n)
        rows.append(dict(cephe="ETF", donem=nm, maliyet=ck, sharpe=s["sharpe"], yillik_pct=s["ann_pct"], vol_pct=s["vol_pct"], t=s["t"], sharpe_dm=np.nan,
                         bh_sharpe=per_stats(bhs)["sharpe"], bh_yillik_pct=per_stats(bhs)["ann_pct"], maruziyet=round(float(expo.mean()), 3), devir_yil=np.nan,
                         maxDD_pct=round(float((n.cumsum() - n.cumsum().cummax()).min() * 100), 1), alfa_yillik_pct=al["alfa_yillik_pct"], alfa_t=al["alfa_t"], beta_sepet=al["beta"]["sepet"]))
CB = pd.DataFrame(rows)
CB["beklenen_yariya_sharpe"] = (CB.sharpe / 2).round(2); CB["beklenen_yariya_yillik_pct"] = (CB.yillik_pct / 2).round(2)
CB.to_csv(f"{OUT}/birlesim.csv", index=False); print(CB.to_string())
# birleşimin yıllık getirileri
effv = comb_viop(); nv, _ = bt_eff(effv, RV.dropna(), 5.0)
ne, _ = comb_etf(10.0)
YR = pd.DataFrame({"VIOP_birlesim_%": nv.groupby(nv.index.year).sum() * 100, "VIOP_BH_%": np.expm1(RV.dropna()).groupby(RV.dropna().index.year).sum() * 100,
                   "ETF_birlesim_%": ne.groupby(ne.index.year).sum() * 100}).round(1)
YR.to_csv(f"{OUT}/birlesim_yillik.csv"); print(YR.to_string())

# ---------- tek tek sinyallerin ETF alfa testi (maruziyet eşleşmeli) ve OOS/2022+
AL = []
for k, (u, h) in ESIG.items():
    for nm, a, b in periods("ETF"):
        rr = cut(rE[u].dropna(), a, b); n, _ = bt_eff(eff_of(ER[k], h).reindex(rr.index).fillna(0), rr, 10.0)
        al = alpha_t(n, np.expm1(rr).rename("bh")); AL.append(dict(sinyal=k, donem=nm, **{kk: vv for kk, vv in al.items() if kk != "beta"}, beta=al["beta"]["bh"]))
for k, h in VSIG.items():
    for nm, a, b in periods("VIOP"):
        rr = cut(RV.dropna(), a, b); n, _ = bt_eff(eff_of(VR[k], h).reindex(rr.index).fillna(0), rr, 5.0)
        al = alpha_t(n, np.expm1(rr).rename("bh")); AL.append(dict(sinyal=k, donem=nm, **{kk: vv for kk, vv in al.items() if kk != "beta"}, beta=al["beta"]["bh"]))
AL = pd.DataFrame(AL); AL.to_csv(f"{OUT}/alfa_bh.csv", index=False); print(AL.to_string())

# ---------- (5b) oynaklık rejimi: karar günü rv20 (yıllık, spot 15:00 UTC) dilimlerine göre sinyal PnL'i
_, qv, rvA = sig_lowmom()
rv_v = to_viop(rvA); rv_e = rvA.reindex(E.index, method="ffill")
bins = [0, 0.12, 0.18, 0.25, 9]; lab = ["<%12", "%12-18", "%18-25", ">%25"]
RG = []
for k, h in VSIG.items():
    n = VN[k]; rg = pd.cut(rv_v.shift(1).reindex(n.index), bins, labels=lab)
    for L_ in lab:
        x = n[rg == L_]
        RG.append(dict(sinyal=k, rejim=L_, gun=len(x), sharpe=per_stats(x)["sharpe"] if len(x) > 60 else np.nan, yillik_pct=round(x.mean() * 252 * 100, 2) if len(x) else np.nan,
                       aktif_pay=round(float((eff_of(VR[k], h).shift(1).reindex(x.index) != 0).mean()), 2) if len(x) else np.nan))
for k, (u, h) in ESIG.items():
    n = EN[k].dropna(); rg = pd.cut(rv_e.shift(1).reindex(n.index), bins, labels=lab)
    for L_ in lab:
        x = n[rg == L_]
        RG.append(dict(sinyal=k, rejim=L_, gun=len(x), sharpe=per_stats(x)["sharpe"] if len(x) > 60 else np.nan, yillik_pct=round(x.mean() * 252 * 100, 2) if len(x) else np.nan,
                       aktif_pay=round(float((eff_of(ER[k], h).shift(1).reindex(x.index) != 0).mean()), 2) if len(x) else np.nan))
RG = pd.DataFrame(RG); RG.to_csv(f"{OUT}/rejim.csv", index=False); print(RG.pivot(index="sinyal", columns="rejim", values="sharpe").to_string())
print(RG.pivot(index="sinyal", columns="rejim", values="gun").to_string())
# 2026 gerçekleşen oynaklık
r26 = RV[RV.index >= "2026-01-01"]; g26 = rE["GLD"][rE["GLD"].index >= "2026-01-01"]
res["vol2026"] = dict(viop_ann=round(float(r26.std() * np.sqrt(252)), 3), gld_ann=round(float(g26.std() * np.sqrt(252)), 3), gdxj_ann=round(float(rE["GDXJ"][rE["GDXJ"].index >= "2026-01-01"].std() * np.sqrt(252)), 3),
                      rv20_spot_son=round(float(rvA.iloc[-1]), 3), rv20_spot_2026_min=round(float(rvA[rvA.index >= "2026-01-01"].min()), 3),
                      lowmom_q_son=round(float(qv.iloc[-1]), 3), viop_ann_2017_2026=round(float(RV.std() * np.sqrt(252)), 3))
print(res["vol2026"])
json.dump(res, open(f"{OUT}/s04_sonuc.json", "w"), indent=1, ensure_ascii=False, default=str)
