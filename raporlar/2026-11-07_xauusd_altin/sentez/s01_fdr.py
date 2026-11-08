"""s01: Global kayıttan (7.446 test) işlenemez testleri ayıkla, kalan 'işlenebilir öngörü' testlerine
hedef alanı bazında (VİOP / ETF) BH-FDR ve Bonferroni uygula.

Ayıklama kuralı (öncelik sırasıyla; bir test ilk eşleşen sınıfa düşer):
  X1 KAPANIS  : bilgi zamanı karar anından sonra ya da girişle eş zamanlı (not 'KAPANIŞTA HESAPLANAN',
                'CUTOFF SONRASI', 'SONRASINDA HESAPLANAN', 'sinyal t 15:10 K', 'K;' ; aile viop_pos_sameday;
                a1 '_vt' backtest sürümleri = gün t VİOP uzlaşması).
  X2 MEKANIK  : hedef ile öngörücü aynı fiyat gürültüsünü paylaşıyor (not 'MEKANİK'; e3 b_prem_diag; e1 e_prem).
  X3 TANI     : tanı/kontrol/betimsel; işlem kuralı değil (emilim pencereleri, kısmi regresyonlar, kontrol,
                oynaklık oranı, ters yön, aşınma, bacak ortalamaları, ayrıştırma, 'tanı' notlu satırlar).
  X4 KAPKAP_DEGIL : hedef kapanıştan kapanışa değil (akşam/gece/gün içi bacak, son saat, hafta sonu boşluğu).
  X5 GORELI_CEPHE : hedef göreli/spread (açığa satış gerekir) ya da altın yönü dışı / cephe dışı
                (USDTRY, gram primi RV, VİOP−spot baz, madenci ileri artığı, PHYS/CEF spread, GLD−spot, BIST BYF).
  X6 KOPYA    : birebir kopya (r4_turkiye_altin = a7 testleri; e2 s6_strateji = c_/a_ testlerinin tekrarı).
Kalan = 'işlenebilir öngörü (geniş)'. Bunun içinden ayrıca
  R1 SAGLAMLIK : sağlamlık/komşuluk/alternatif hedef/IS-seçilmiş tekrar/bacak varyantları
  R2 ERKEN     : 2010–2016 (ya da 2008 öncesi) bağımsız erken dönem tekrarları
çıkarılınca 'birincil' küme kalır. FDR iki küme için ayrı ayrı, her biri VİOP ve ETF alanında ayrı yapılır.
"""
import re, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = f"{S}/out/sentez"
d = pd.read_csv(f"{S}/out/main/global_registry_fdr.csv")
d["note"] = d["note"].fillna("")
d["test_id"] = d["test_id"].astype(str)


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.clip(q, 0, 1)


X3_FAM = {"s1_emilim", "s3_emilim", "s5_tani", "s1_kismi", "s4_kismi", "s6_sirakismi", "a_kismi", "a_kismi_rank",
          "K_control", "kontrol", "oynaklik", "A_own", "A_own_spot", "B_spread_diag", "c_cef_diag", "d_letf_diag",
          "d_letf_lasthour", "e_bist_byf_diag", "a_reverse", "d_drag", "d_volregime", "b2_decomp", "b_mean",
          "b_segmean", "b_segexcess"}
X4_FAM = {"b_altentry", "f_viop_native", "b_weekend"}
R1_FAM = {"robust_lowmom", "robust_volreg", "g_is_selected", "s4_saglam", "s4_bt", "R_robust", "X_extra",
          "asia_robust", "asia_rule", "cot_robust", "cot_rule", "gpr_robust", "gpr_rule", "shfe_robust", "shfe_rule",
          "viop_pos_robust", "viop_pos_rule", "f_claims", "a8_robust", "a8_c1_components", "f_final", "a2_leg",
          "b2_leg", "g_main", "A_resid_spot", "A_fitted_spot", "B_ratio_spot", "C_intraday_spot",
          "a8_univariate_longspot", "c_cef_switch"}
R2_FAM = {"a_mom_early", "b_trend_early", "c_rev_early", "d_vol_early", "e_micro_early", "g_intraday_early",
          "bt_early", "bt2_early", "a_early", "g_early", "s5_erken", "s4_erken", "s7_bt", "asia_early",
          "cot_early", "gpr_early", "shfe_early", "a8_ml_V3", "a8_univariate_early"}


def classify(r):
    a, f, tid, n = r.agent, r.family, r.test_id, r.note
    # X6 kopya
    if a == "r4_turkiye_altin": return "X6_KOPYA"
    if f == "s6_strateji": return "X6_KOPYA"
    # X1 kapanışta / cutoff sonrası
    if re.search(r"KAPANI[SŞ]TA|CUTOFF SONRASI|SONRASINDA HESAPLANAN|sinyal t 15:10 K|^K;|^K t 15:10", n): return "X1_KAPANIS"
    if f == "viop_pos_sameday": return "X1_KAPANIS"
    if a == "a1_zaman_serisi" and re.search(r"_vt($|\|)", tid): return "X1_KAPANIS"
    # X2 mekanik
    if "MEKANİK" in n or f in {"b_prem_diag", "e_prem"}: return "X2_MEKANIK"
    # X3 tanı
    if f in X3_FAM: return "X3_TANI"
    if n.startswith("tanı") or "tani;" in n or n.startswith("tani") or "(tanı)" in n: return "X3_TANI"
    if f == "d_fix" and "ortalama saatlik" in n: return "X3_TANI"
    if f == "a_madenci_artik" and "ayrıştırma" in n: return "X3_TANI"
    if f == "e_robust" and tid.startswith("diag_"): return "X3_TANI"
    # X4 kapanıştan kapanışa değil
    if f in X4_FAM: return "X4_KAPKAP_DEGIL"
    if f == "d_letf_intraday": return "X4_KAPKAP_DEGIL"
    if f == "d_fix" and "gün içi" in n: return "X4_KAPKAP_DEGIL"
    if f == "e_weekend" and (tid in {"e_gap_to_monday_day", "e_friaft_to_gap"}): return "X4_KAPKAP_DEGIL"
    # X5 göreli hedef / altın dışı / cephe dışı
    if f == "c_basis" and "_rel_" in tid: return "X5_GORELI_CEPHE"
    if f == "b_trgold": return "X5_GORELI_CEPHE"
    if f == "e_robust" and tid.startswith("usdtry_component"): return "X5_GORELI_CEPHE"
    if f == "a_madenci_artik" and "ileri_artik" in tid: return "X5_GORELI_CEPHE"
    if f in {"c_cef", "c_cef_intraday"} and "spread" in tid: return "X5_GORELI_CEPHE"
    if f in {"b_prem", "b_prem_intraday"} and "relGLDspot" in tid: return "X5_GORELI_CEPHE"
    if f == "d2_miners_rel": return "X5_GORELI_CEPHE"
    if f == "e_bist_byf": return "X5_GORELI_CEPHE"
    # --- işlenebilir; birincil mi?
    if f in R1_FAM: return "R1_SAGLAMLIK"
    if f == "e_robust": return "R2_ERKEN" if tid.startswith("early::") else "R1_SAGLAMLIK"
    if f == "a_madenci_artik" and ("duyarlılığı" in n or n == "robust" or "_uc_haric" in tid): return "R1_SAGLAMLIK"
    if f == "e_cot" and n == "robust": return "R1_SAGLAMLIK"
    if f == "a_flow_gld" and "IAU" in n: return "R1_SAGLAMLIK"
    if a == "a3_takvim_olay" and re.search(r"ex2026|exDec|QDECOMP|nonQ|_perday|bigIS", tid): return "R1_SAGLAMLIK"
    if f in R2_FAM: return "R2_ERKEN"
    if a == "a3_takvim_olay" and re.search(r"spot_?early", tid): return "R2_ERKEN"
    if f == "e_weekend" and "2010-2016" in n: return "R2_ERKEN"
    if f == "B_early" and not tid.endswith("_viop"): return "R2_ERKEN"
    return "BIRINCIL"


d["sinif"] = d.apply(classify, axis=1)
# hedef alanı
d["alan"] = np.where(d.agent.str.startswith("e"), "ETF", "VIOP")
d.loc[(d.agent == "e3_etf_akis_prim") & (d.family == "a_flow_viop"), "alan"] = "VIOP"

ex = d.sinif.str.startswith("X")
d["islenebilir"] = ~ex
d["birincil"] = d.sinif == "BIRINCIL"

rows = []; passed = []
for kume, m in [("islenebilir_genis", d.islenebilir), ("birincil", d.birincil)]:
    for alan in ["VIOP", "ETF"]:
        g = d[m & (d.alan == alan)].copy()
        g["q_bh"] = bh(g.p.values); g["p_bonf"] = np.minimum(g.p * len(g), 1)
        d.loc[g.index, f"q_{kume}"] = g.q_bh; d.loc[g.index, f"bonf_{kume}"] = g.p_bonf
        tcrit = float(pd.Series([0]).pipe(lambda _: __import__("scipy.stats", fromlist=["norm"]).norm.isf(0.025 / len(g))))
        rows.append(dict(kume=kume, alan=alan, n_test=len(g), p_lt_005=int((g.p < 0.05).sum()), beklenen_p005=round(0.05 * len(g), 1),
                         abs_t_ge3=int((g.t.abs() >= 3).sum()), q_lt_005=int((g.q_bh < 0.05).sum()), q_lt_010=int((g.q_bh < 0.10).sum()),
                         bonf_lt_005=int((g.p_bonf < 0.05).sum()), bonf_esik_t=round(tcrit, 2), min_q=round(g.q_bh.min(), 4)))
        top = g[(g.q_bh < 0.10) | (g.p_bonf < 0.05)].sort_values("p")
        for _, r in top.iterrows():
            passed.append(dict(kume=kume, alan=alan, agent=r.agent, family=r.family, test_id=r.test_id, h=r.h, t=round(r.t, 2), t_is=r.t_is, t_oos=r.t_oos,
                               p=r.p, q_bh=round(r.q_bh, 4), p_bonf=round(r.p_bonf, 4), note=r.note[:90]))

summ = pd.DataFrame(rows)
cls = d.groupby(["sinif", "alan"]).size().unstack(fill_value=0)
cls["toplam"] = cls.sum(axis=1)
d.to_csv(f"{OUT}/fdr_siniflandirma.csv", index=False)
summ.to_csv(f"{OUT}/fdr_ozet.csv", index=False)
P = pd.DataFrame(passed); P.to_csv(f"{OUT}/fdr_gecenler.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70); pd.set_option("display.max_rows", 300)
print(cls.to_string()); print()
print(summ.to_string()); print()
print(P.to_string())
# eski global q'ya göre geçen ve yeni kümede elenenler
old = d[d.q_global < 0.05]
print("\nEski global q<0,05:", len(old), "| sınıf dağılımı:"); print(old.sinif.value_counts().to_string())
