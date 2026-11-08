"""s02: Bütün ailelerin iddiaları tek tabloda: analist güveni, REP ve ADV hükmü, SON güven (muhafazakâr birleşim = ikisinden düşüğü).
Ayakta kalanların etki ve Sharpe değerleri hakemin kendi yeniden hesabından (basit getiri, s03) ayrı sütunlara da yazılır.
Çıktı: sinyal_tablosu.csv"""
import pandas as pd, numpy as np
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/sentez"
RANK = {"YOK": 0, "DUSUK": 1, "ORTA": 2, "YUKSEK": 3}
C = ["id", "aile", "cephe", "kural", "bilgi_zamani", "h", "etki_bps_islem", "etki_yillik", "t_IS", "t_OOS", "oos_sharpe_net", "oos_bh_sharpe", "yilda_islem",
     "analist", "rep", "adv", "ana_zayiflik", "islenebilirlik", "hakem_kod"]
R = [
# ---------------- VİOP: a1
("A1-LOWMOM-h1", "a1", "VIOP", "P=spot XAUUSD 15:00 UTC; x=ln(P_t/P_t-5); rv20=son 20 günlük ΔlnP std; q=rv20'nin 2010'dan beri genişleyen yüzdeliği (bugün dahil). q<1/3 (≈yıllık %11,7) ise t uzlaşmasında sign(x) yönünde 1 birim aç, t+1 uzlaşmasında kapat (aynı yön sürerse netleştir); q≥1/3 ise nakit.",
 "t 15:00 UTC (Dukascopy 14:00 barı kapanışı)", 1, "8,1 bps/aktif gün (OOS 14,9)", "net %7,2/yıl (1x, tam); alfa %7,1 (t 2,9), OOS %7,6 (t 2,6)", 2.38, 2.68, "1,36 (dm 1,31)", "0,53", 21.5,
 "ORTA", "ORTA", "DUSUK", "Izgara tepesi (280 komşunun 99. yüzdeliği; medyan ≈0,4); 2017-19'da etki yok; en iyi 20 gün PnL'in %66-75'i; 2026'da hiç tetiklenmedi.", "Uygulanabilir (VİOP, 5 bps, yılda ~22 gidiş-dönüş; TR yarım günleri hariç); 2026 rejiminde pasif.", "V_LOWMOM_h1"),
("A1-LOWMOM-h5", "a1", "VIOP", "A1-LOWMOM-h1 ile aynı sinyal; t uzlaşmasında aç, t+5'te kapat; her gün sermayenin 1/5'i (kademeli).",
 "t 15:00 UTC", 5, "29,0 bps/aktif gün, 5 günlük (OOS 67,9)", "net %5,4/yıl (1x, tam)", 0.64, 3.64, "1,69 (dm 1,63)", "0,53", 11.2,
 "ORTA", "ORTA", "DUSUK", "h1'in tutuş varyantı, bağımsız değil; IS IC t 0,64; 2017-19 negatif; OOS yalnız 278 aktif güne dayanıyor.", "Uygulanabilir; 2026'da pasif.", "V_LOWMOM_h5"),
("A1-VOLREG5-h5", "a1", "VIOP", "q<1/3: sign(ln P_t/P_t-5); q>2/3: −sign(...); aksi 0; h=5 kademeli.", "t 15:00 UTC", 5, "—", "—", 2.78, 2.24, "1,03 (dm 1,02)", "0,53", 21.5,
 "DUSUK", "DUSUK", "DUSUK", "LOWMOM dışı kısmı (çalkantıda dönüş) 2010-16'da ve 2022-23'te negatif; k=10'da çöküyor.", "Kullanılabilir içeriği LOWMOM ile aynı; 2026'da yalnız çürük bacak aktif olurdu.", ""),
("A1-TAILMOM-BB-h1", "a1", "VIOP", "Bollinger z(20,2)>2 uzun, <−2 kısa, 1 gün.", "t 15:00 UTC", 1, "—", "—", 1.64, 0.75, "0,40 (dm 0,34)", "0,53", 13.6,
 "DUSUK", "DUSUK", "YOK", "BB dönüş kuralının aynası; hiçbir dönemde t>2 değil; eşiğe duyarlı.", "Tek başına işlem sinyali değil.", ""),
("A1-REV-NEG", "a1", "VIOP", "Kısa vadeli dönüş kuralları (BB±2 ters, 2σ ters, RSI2, Connors, 3+ gün seri ters, −sign(r1)).", "t 15:00 UTC", 1, "—", "drift çık. Sharpe −0,4..−0,67", -2.15, -1.14, "−0,57", "0,53", 13.6,
 "YOK", "YOK", "YOK", "Negatif bulgu: dönüş kuralları üç dönemde de zarar; kayıp kısmen maliyetten.", "KULLANMA (ortalama düşürme/dip alma işe yaramıyor).", ""),
("A1-TREND-MA50", "a1", "VIOP", "P15>SMA50 uzun, değilse kısa, 1 gün.", "t 15:00 UTC", 1, "—", "—", -0.72, 1.82, "0,96 (dm 0,83)", "0,53", 17,
 "DUSUK", "DUSUK", "YOK", "OOS kârı 2022-26 boğa drift'i; yıl ortalaması çıkarınca Sharpe 0,03; IS negatif.", "Trend filtresi yön kenarı vermiyor.", ""),
# ---------------- a2
("a2_c1_S2_gece", "a2", "VIOP", "VİOP akşam seansı kapanışında (23:00 TSİ) uzun, ertesi sabah normal seans açılışında (09:30 TSİ) kapat.", "t-1 20:00 → t 00:00 UTC takvim etkisi", 0, "~3 bps/gün brüt", "—", 3.6, 4.57, "0,28 (gerçek çıkış saatiyle ≈0)", "—", 252,
 "ORTA", "ORTA", "DUSUK", "Brüt kenar ≈ maliyet (5 bps); gerçekçi akşam maliyetiyle negatif; drift'in tahakkuk zamanı, lead-lag değil.", "İŞLENEMEZ: kapanıştan kapanışa değil.", ""),
("a2_c2_baz_donus", "a2", "VIOP", "eb_t-1 (uzlaşma−spot−taşıma) üst tercil: VİOP kısa+spot uzun (alt tercil tersi), h=5; hedef VİOP−spot.", "t-1 15:10 UTC", 5, "—", "—", -1.9, -3.08, "0,39 (fonlama sonrası ≈0)", "—", 36,
 "ORTA", "ORTA", "DUSUK", "İstatistik gerçek ama ekonomik değer yok: OOS kârı taşıma drift'i; düşük hacimli günlerde güçlü (bayat uzlaşma).", "İŞLENEMEZ: göreli (spot bacak gerekir).", ""),
("a2_c3_kis_fiks", "a2", "VIOP", "Kış (GMT) günlerinde 14→15 UTC işareti yönünde, h=1.", "t 15:00 UTC", 1, "—", "—", 1.63, 2.08, "1,02", "0,53", 100,
 "DUSUK", "DUSUK", "YOK", "30 saat×mevsim testinin en iyisi; erken dönemde yok; IS Sharpe 0,13; yaz fiks saati 0.", "—", ""),
("a2_c4_C_pre_h3", "a2", "VIOP", "sign(ln p15/p00), 3 gün.", "t 15:00 UTC", 3, "—", "—", 1.1, 2.11, "0,30", "0,53", 83,
 "DUSUK", "YOK", "YOK", "Yalnız h=3'te tepe; 2010-16'da IC 0; kâr 2025-26'dan.", "—", ""),
("a2_c5_NY_sabahi", "a2", "VIOP", "|ln p15/p12|>IS q90 ise işaret yönünde 5 gün.", "t 15:00 UTC", 5, "—", "—", 0.33, 2.33, "0,77", "0,53", 31,
 "DUSUK", "DUSUK", "YOK", "IS'te hiçbir eşikte yok; erken dönemde ters; 2022-23'e yaslanıyor.", "—", ""),
# ---------------- a3
("A3_QEND_h3", "a3", "VIOP", "Mar/Haz/Eyl/Ara'nın sondan 2. VİOP işlem günü uzlaşmasında UZUN, 3 VİOP günü sonra (yeni çeyreğin 2. günü) kapat; diğer günler nakit.", "Takvim (önceden bilinir)", 3, "+76,7 bps/olay (diğer günler +8,3; fark +68,5)", "net %1,0/yıl (maruziyet %1,6); alfa t 2,75", 2.13, 2.26, "0,99 (dm 0,87)", "0,53", 4,
 "ORTA", "ORTA", "DUSUK", "39 olay; sağlam kısım yıl dönümü; Mar/Haz/Eyl 2010-16'da yok (t 0,61); 2017-19 ve 2022-23 ≈0; BH q 0,06.", "Uygulanabilir, çok düşük devir; tek başına küçük katkı.", "V_QEND_h3"),
("A3_NFP_MOM_h1", "a3", "VIOP", "NFP günü (VİOP açık, yarım gün değil) x=sign(ln p15/p12); uzlaşmada x yönünde gir, ertesi VİOP günü çık.", "t 15:00 UTC (NFP 12:30/13:30 UTC)", 1, "+18 bps/olay (IS +5,7, OOS +31)", "—", 0.55, 3.46, "0,90", "0,53", 11.4,
 "ORTA", "DUSUK", "DUSUK", "IS'te yok (t 0,47); 2010-21 boyunca sıfır/ters; en iyi 5 olay çıkınca etki kayboluyor; CPI'da ters işaret.", "Uygulanabilir ama yalnız OOS'ta bulunmuş; izleme listesi.", ""),
("A3_NFP_MOM_h3", "a3", "VIOP", "A3_NFP_MOM_h1 ile aynı, 3 gün tut.", "t 15:00 UTC", 3, "+35 bps/olay", "—", 0.99, 2.64, "1,07", "0,53", 11.4,
 "ORTA", "DUSUK", "DUSUK", "h1 ile aynı sinyal; fazladan iki gün t 1,53; OOS 2024-26'ya dayanıyor.", "Bağımsız değil.", ""),
("A3_OG_EXPIRY_DAY", "a3", "VIOP", "COMEX OG vade gününden önceki uzlaşmada KISA, vade günü uzlaşmasında çık.", "Takvim", 1, "−23,8 bps/olay", "—", -0.95, -3.11, "1,03", "0,53", 12,
 "DUSUK", "DUSUK", "YOK", "17 yıllık spotta etki 0 (t −0,35); tek günlük sivri tepe; 2024-26 birkaç düşüş günü.", "—", ""),
("A3_BAYRAM_POST", "a3", "VIOP", "Bayram sonrası ilk VİOP günü KISA, 5 gün.", "Takvim", 5, "−78 bps/olay (düzeltilmiş)", "—", -2.1, -2.08, "0,43", "0,53", 2.2,
 "DUSUK", "DUSUK", "YOK", "Kod hatası (sahte olay); 20 olay; erken dönemde ters; mekanizma yok.", "—", ""),
("A3_JANUARY", "a3", "VIOP", "Ocak'ta her gün uzun.", "Takvim", 1, "+15 bps/gün fark", "—", 0.72, 2.0, "0,84", "0,51", 1,
 "DUSUK", "DUSUK", "YOK", "12 ay testinden biri; Ocak 2026 ve 2017 çıkınca t 0,94.", "—", ""),
# ---------------- a4
("A4-C1_GDXJ_artik_h3", "a4", "VIOP", "e=r_GDXJ−β60·r_GLD (Yahoo adjclose, t-2→t-1 ABD kapanışı, VİOP satırlarında fark; β önceki 60 gün); z=e/std(e, önceki 120 gün). z>0,43 UZUN, z<−0,43 KISA; 3 gün kademeli.", "t-1 16:00 ET ABD kapanışı (cutoff'tan 18-19 saat önce)", 3, "12,1 bps/aktif gün, 3 günlük (OOS 16,9)", "net %3,9/yıl (1x, tam); alfa %4,7 (t 1,8), OOS %7,6 (t 1,7)", 2.53, 2.63, "0,72 (dm 0,76)", "0,53", 34,
 "ORTA", "DUSUK", "DUSUK", "Kanıt sıra IC'sinde; kural P&L t tam 1,64/IS 0,53; IS gücü 2017'den; 2025-26 IC t 0,86; 2010-16 spotta yok; ABD takvimiyle kurunca OOS 0,52.", "Uygulanabilir; ETF tarafındaki E2-C2j ile aynı öngörücü (sıra korelasyonu 0,87).", "V_GDXJRES_h3"),
("A4-C1b_madenci_kompozit_h3", "a4", "VIOP", "GDX, GDXJ, RING ve 7'li sepet artık z ortalamasının işareti, 3 gün.", "t-1 ABD kapanışı", 3, "—", "—", 2.27, 2.43, "0,38", "0,53", 237,
 "ORTA", "DUSUK", "DUSUK", "OOS backtest t 0,83; kısa bacak her iki dönemde zarar; kompozit tek madenciden zayıf.", "A4-C1'in varyantı.", ""),
("A4-C2_egri_d5_h1", "a4", "VIOP", "pos=clip(z(Δ5(10y−2y))/2,−1,1), 1 gün.", "t-1 22:00 UTC", 1, "—", "—", 1.87, 2.58, "0,65", "0,53", 243,
 "DUSUK", "DUSUK", "YOK", "Getiri 2020 ve 2025-26'dan; 2013-16'da anlamlı ters (t −2,09).", "—", ""),
("A4-C3_dxy_sapma_h1", "a4", "VIOP", "−clip(z(β250·r_DXY − r_XAU, t-1 20:00→t 15:00)/2), 1 gün.", "t 15:00 UTC", 1, "—", "—", -2.17, -1.65, "0,27", "0,53", 205,
 "DUSUK", "YOK", "YOK", "OOS t −1,65; 10 bps'de negatif.", "—", ""),
("A4-D1_dolar_emilim", "a4", "VIOP", "TANI: dolar t-1 kapanışında yükseldiyse altın [t-1 20:00→t 15:00] penceresinde yükselir.", "t-1 22:00 UTC", 0, "—", "—", 1.61, 2.23, "—", "—", 0,
 "DUSUK", "DUSUK", "YOK", "Etki giriş öncesi pencerede; doğrusal t 1,1.", "İŞLENEMEZ (pencere VİOP girişinden önce kapanıyor).", ""),
("A4-C4_reel_dolar_artik", "a4", "VIOP", "log xau ~ real10 + log DXY artık z, 1 gün.", "t 15:00 / t-1", 1, "—", "—", 1.62, 1.7, "0,36 (dm 0,06)", "0,53", 218,
 "YOK", "YOK", "YOK", "Drift ve momentum vekili.", "—", ""),
# ---------------- a5
("a5_C1_makrogunu_artik_h3", "a5", "VIOP", "|b'x12/σ|>1,096 (büyük ABD makro hareketi) günlerinde 12→15 UTC altın artığının işareti yönünde, 3 gün.", "t 15:00 UTC", 3, "—", "—", 2.1, 1.93, "0,60", "0,53", 37,
 "ORTA", "DUSUK", "DUSUK", "Spesifikasyona duyarlı (W120/W250'de zayıf); P&L t 1,3; OOS kazanç uzun bacakta; 2019-07 öncesinde yok.", "Uygulanabilir ama OOS t<2.", ""),
("a5_C4_londra_ny_artik_h1", "a5", "VIOP", "|e07|>1 ise 07→15 UTC artık işareti yönünde, 1 gün.", "t 15:00 UTC", 1, "—", "—", 2.66, 1.38, "0,88", "0,53", 55,
 "DUSUK", "DUSUK", "DUSUK", "Tamamen eşik seçimine bağlı (sign kuralı OOS 0,04); erken vekilde sıfır.", "—", ""),
("a5_B1_altin_gumus_5g", "a5", "VIOP", "−sign(5 günlük altın−gümüş göreli getiri), 1 gün.", "t 15:00 UTC", 1, "—", "—", -0.68, -2.82, "1,12", "0,53", 99,
 "DUSUK", "DUSUK", "DUSUK", "Post-hoc; IS'te yok; Pearson t −0,56; 2022 sonrası rejim.", "—", ""),
("a5_yetisme_YOK", "a5", "VIOP", "Makroya eksik tepki → yetişme.", "t 15:00 UTC", 1, "—", "—", -2.21, -0.98, "−0,64", "—", 0, "YOK", "YOK", "YOK", "Negatif bulgu: yetişme yok, işaret ters (sürme).", "—", ""),
("a5_15to15_artik_YOK", "a5", "VIOP", "15→15 yuvarlanan-beta artığı dönüşü (11 model).", "t 15:00 UTC", 1, "—", "—", 2.49, -0.41, "−0,81", "—", 257, "YOK", "YOK", "YOK", "Negatif bulgu: 297 testte |t|>2 oranı %2.", "—", ""),
("a5_oran_zskor_YOK", "a5", "VIOP", "Altın/gümüş, altın/platin oran z-skoru dönüşü.", "t 15:00 UTC / t-1", 5, "—", "—", 2.11, -0.17, "—", "—", 0, "YOK", "YOK", "YOK", "IS ve OOS işaretleri ters.", "—", ""),
# ---------------- a6
("a6_cn_gold_res_comp_h5", "a6", "VIOP", "Çin altın hisseleri (600547.SS, 1818.HK, 2899.HK) spot altın ve yerel endeks artıkları ortalamasının işareti, 5 gün kademeli.", "t 07:00/08:10 UTC", 5, "—", "—", 0.37, 3.4, "1,41 (REP 1,26)", "0,51", 121,
 "ORTA", "DUSUK", "DUSUK", "OOS dahil tam örneklemle seçildi; IS 2017-21 ve 2010-16'da t≈0; kanıt 2024-26'da.", "Uygulanabilir ama yalnız OOS'ta bulunmuş; izleme listesi.", ""),
("a6_res600547_h5", "a6", "VIOP", "Shandong Gold artığı işareti, 5 gün.", "t 07:00 UTC", 5, "—", "—", 0.86, 3.08, "1,02", "0,51", 119, "ORTA", "DUSUK", "DUSUK", "Ana iddiayla aynı kanıt; 2022-23 negatif.", "Varyant.", ""),
("a6_hsi_h3", "a6", "VIOP", "sign(r_HSI,t), 3 gün.", "t 08:10 UTC", 3, "—", "—", 2.37, 2.11, "0,24", "0,51", 132, "DUSUK", "YOK", "YOK", "Spot altın kontrolüyle kayboluyor (OOS t 0,56).", "—", ""),
("a6_viop_oi5_x_trend_h5", "a6", "VIOP", "−sign(OI 5g % × sign(r5)), 5 gün.", "t-1 bülten", 5, "—", "—", -3.61, -0.62, "0,38", "0,51", 72, "DUSUK", "YOK", "YOK", "Etki tamamen IS'te.", "—", ""),
("a6_gpr_z250_h5", "a6", "VIOP", "−sign(GPR z250), 5 gün.", "D+1 23:00 varsayımı", 5, "—", "—", -1.86, -1.63, "0,70", "0,51", 87, "DUSUK", "DUSUK", "YOK", "Yayın gecikmesine karşı istikrarsız; gerçek zamanlı veri değil.", "—", ""),
("a6_cn_res_sum5_h1", "a6", "VIOP", "Çin artık bileşiğinin 5 günlük toplamının işareti, 1 gün.", "t 07:00/08:10 UTC", 1, "—", "—", 0.9, 3.64, "0,97", "0,51", 50, "DUSUK", "DUSUK", "DUSUK", "Post-hoc varyant; aynı veri.", "Varyant.", ""),
# ---------------- a7
("a7_C1_usdtry_carry", "a7", "VIOP-USDTRY", "F_USDTRY'de pos=sign(20g ort ΔlnUSDTRY − 1,4×baz/dte), 1 gün (hedef USDTRY, ALTIN DEĞİL).", "t-1 15:00/15:10", 1, "—", "—", 3.21, 2.48, "1,19 (dm 0,88)", "hep kısa +0,55", 20.5,
 "ORTA", "ORTA", "DUSUK", "Fiilen 20g kur momentumu; PnL birkaç epizotta; 2024-26'da zamanlama katkısı negatif, kâr carry'den.", "Cephe dışı (altın değil).", ""),
("a7_C2_fx_drift", "a7", "VIOP-USDTRY", "Yönetilen kurda USDTRY h günlük beklenen değişim = h × 20g ortalama.", "t 15:00", 5, "—", "—", np.nan, 2.71, "—", "—", 0, "ORTA", "DUSUK", "DUSUK", "Sabit uzun dönem drift eşdeğer; h5 sonucu 2026'ya dayanıyor.", "Tahmin, işlem kuralı değil.", ""),
("a7_C3_gram_prim_donus", "a7", "VIOP-gram", "z(gram primi, t-1)>1 gram kısa + ons ve USDTRY uzun (tersi), 3 gün, 3 bacak 15 bps.", "t-1 15:10", 3, "—", "—", -2.93, -5.79, "−0,77", "—", 75, "DUSUK", "DUSUK", "DUSUK", "İstatistik çok güçlü (t −6,1) ama 3 bacak maliyetiyle net zarar.", "İŞLENEMEZ (net zarar); yalnız araç seçiminde bilgi.", ""),
("a7_C4_xau_after_usdtry", "a7", "VIOP", "−sign(VİOP USDTRY getirisi t-1), 3 gün.", "t-1 15:10", 3, "—", "—", -1.56, -1.45, "0,21 (dm −0,01)", "0,53", 104, "DUSUK", "DUSUK", "YOK", "Tek tepe; drift'ten.", "—", ""),
("a7_C5_TR_sok", "a7", "VIOP", "TL şoku ya da XU030<−%5 gününde ons kısa, 3 gün.", "t 15:00 / t-1", 3, "−48 bps/olay", "—", -2.29, -1.48, "0,45", "0,53", 11.8, "DUSUK", "DUSUK", "YOK", "Kümeleme sonrası anlamsız; ~30 bağımsız epizot.", "—", ""),
("a7_C6_xautry_oi", "a7", "VIOP", "sign(ΔlnOI XAUTRYM, t-1), 3 gün.", "t-1 bülten", 3, "—", "—", 0.38, 2.62, "0,28", "0,53", 109, "DUSUK", "DUSUK", "YOK", "IS'te sıfır; roll sıçramaları.", "—", ""),
# ---------------- a8
("A8-1_ML", "a8", "VIOP", "103 öznitelikli ridge/lasso/EN/HGB/RF/topluluk, aylık yeniden eğitim.", "≤ t 15:00 UTC", 1, "—", "—", 1.08, 1.17, "−0,91", "0,53", 0, "YOK", "YOK", "YOK", "Negatif bulgu: 0/27 pozitif OOS R².", "—", ""),
("A8-2_nom2_d5", "a8", "VIOP", "−sign(Δ5 ABD 2y getirisi), 1 gün.", "t-1 22:00 UTC", 1, "—", "—", -0.26, -2.48, "0,66", "0,53", 57, "DUSUK", "DUSUK", "DUSUK", "OOS 2026'dan; IS'te yok; 309 testten seçildi.", "—", ""),
("A8-3_seg_last1h_h5", "a8", "VIOP", "pos=sign(ln(p15/p14)) (spot 14:00→15:00 UTC); t uzlaşmasında gir, 5 gün kademeli; TR yarım günleri hariç.", "t 15:00 UTC", 5, "10,3 bps/aktif gün, 5 günlük (OOS 13,7)", "net %3,9/yıl (1x, tam); alfa %3,6 (t 1,5), OOS %5,1 (t 1,25)", 1.32, 2.05, "0,63 (dm 0,57)", "0,53", 25,
 "DUSUK", "DUSUK", "DUSUK", "2010-16'da h1-h3'te yok; 2024 Sharpe −2,31; kazanç 2026'ya yığılı; kısa bacak her dönemde zarar; 309 testten seçildi.", "Uygulanabilir; Pazartesi 14-15 UTC verisi gerekir.", "V_LAST1H_h5"),
("A8-4_2s10s_d5", "a8", "VIOP", "sign(Δ5(10y−2y)), 1 gün.", "t-1 22:00 UTC", 1, "—", "—", 1.5, 2.53, "0,85", "0,53", 58, "DUSUK", "YOK", "YOK", "Bilgi −Δ2y bacağından; 2025-26'ya yığılı; erken dönemde ters.", "—", ""),
("A8-5_C1_combo", "a8", "VIOP", "6 a priori z-skorunun eşit ağırlıklı ortalamasının işareti, 1 gün.", "≤ t 15:00", 1, "—", "—", -0.65, 1.85, "0,90", "0,53", 36, "DUSUK", "DUSUK", "YOK", "Yıl içi IC 7/9 yılda negatif; değer yavaş trendden.", "—", ""),
("A8-6_RF_V2_h3", "a8", "VIOP", "Spot panelde eğitilen RF tahmininin işareti, 3 gün.", "≤ t 15:00", 3, "—", "—", -0.92, 2.11, "0,80", "0,53", 24, "DUSUK", "YOK", "YOK", "Tohuma duyarlı; VAL'de ters; şans düzeyinde.", "—", ""),
# ---------------- ETF: e1
("E1-C1_madenci_takvim_sepeti", "e1", "ETF", "Ayın ilk işlem günü ∪ NYSE tatil öncesi son gün: bir önceki kapanışta GDXJ al, olay günü kapanışında sat.", "Takvim", 1, "+59,3 bps/olay (diğer −4,3)", "—", 2.62, 3.41, "1,08 (10 bps)", "—", 18.6,
 "ORTA", "ORTA", "DUSUK", "144 testten sonradan kurulan sepet; ayın ilk günü yarısı aynı gün GLD kontrolüyle kayboluyor; 1983-2007'de t 0,99.", "Sağlam kısmı E1-C2 (tatil öncesi).", ""),
("E1-C2_GDX_tatil_oncesi", "e1", "ETF", "NYSE tatilinden önceki son işlem gününden bir önceki kapanışta GDX al, tatil öncesi gün kapanışında sat (yalnız uzun).", "Takvim (önceden bilinir)", 1, "+47,3 bps/olay (diğer −0,2)", "net %3,6/yıl (1x nominal, tam); B&H'ye göre alfa %3,3 (t 2,3), OOS %4,3 (t 2,1)", 1.71, 2.45, "0,75 (10 bps; dm 0,65)", "0,61", 9.3,
 "ORTA", "ORTA", "ORTA", "IS t 1,71<2; global q 0,52; aynı gün GLD+SPY kontrolüyle 20 bps (t 2,0); ortalamanın 2/3'ü en iyi 10 günden; 1983-2007 madenci sepetinde 35 bps (t 2,16) kısmi teyit.", "Midas'ta uygulanabilir (yılda ~9 işlem); açılış/kapanış emri gerekir.", "E_GDXTATIL_h1"),
("E1-C3_GDX_5gun_dusus", "e1", "ETF", "≥5 gün üst üste düşüş sonrası GDX al, 1 gün.", "t-1 kapanış", 1, "+76,6 bps/olay", "—", 2.07, 2.98, "0,78", "—", 3.4, "ORTA", "DUSUK", "YOK", "1.046 testin beklenen maksimumu; eşik 4/6'da çöküyor; GDXJ'de yok.", "—", ""),
("E1-C4_GLD_Ocak", "e1", "ETF", "Aralık son günü GLD al, Ocak son günü sat.", "Takvim", 1, "+17 bps/gün", "—", 2.22, 1.19, "0,59", "0,81", 1, "ORTA", "DUSUK", "YOK", "48 testin en iyisi; 2001-07'de yok.", "—", ""),
("E1-C5_GLD_BollZ_alt", "e1", "ETF", "z(20,2)_t-1<−2 ise GLD al, 5 gün.", "t-1 kapanış", 5, "+63,9 bps/olay", "—", 0.9, 2.52, "0,70", "—", 2.2, "DUSUK", "DUSUK", "YOK", "Parametreye duyarlı; IS'te yok.", "—", ""),
("E1-C6_GLD_gece", "e1", "ETF", "Her gün kapanışta al, açılışta sat.", "—", 1, "—", "—", 1.08, 3.37, "−0,79", "—", 252, "DUSUK", "DUSUK", "YOK", "Başabaş maliyet 4-7 bps; kısmen mekanik.", "İŞLENEMEZ (kapanıştan kapanışa değil, maliyet).", ""),
# ---------------- e2
("E2-C2j_GDXJ_artik_h3", "e2", "ETF", "e=r_GDXJ−b_GLD·r_GLD−b_SPY·r_SPY (250 günlük yuvarlanan OLS, beta_t-1; getiriler t-2→t-1 kapanış); x=e_t-1 > IS (2008-17) %70 kantili (≈+0,67%) ise GDXJ'yi t kapanışında al, 3 gün kademeli; aksi nakit.", "t-1 16:00 ET kapanışı (~23 saat önce)", 3, "48,5 bps/aktif gün, 3 günlük (OOS 53,1)", "net %13,1/yıl (1x, tam; beta dahil); alfa %9,2 (t 3,3), OOS %6,8 (t 1,95)", 1.9, 3.04, "0,64 log / 0,81 basit", "0,31 log / 0,54 basit", 16.9,
 "YUKSEK", "ORTA", "ORTA", "IS t 1,90; geniş ızgarada dürüst IS seçimi OOS'u ≈0'a indiriyor; Bonferroni'de elenir; 2025-26 IC 0,03 (t 0,6); 2026 YTD ≈0.", "Midas'ta uygulanabilir (yalnız uzun); JDST'li ters sürüm KULLANMA.", "E_C2J_h3"),
("E2-C2_GDX_artik_h3", "e2", "ETF", "GDX'in GLD+SPY'ye göre 3 günlük artık toplamı (t-1'de biter) > IS %70 kantili ise GDX uzun 3 gün; aksi nakit.", "t-1 16:00 ET", 3, "38,1 bps/aktif gün, 3 günlük (OOS 44,3)", "net %10,5/yıl (1x, tam; beta dahil); alfa %6,8 (t 2,2), OOS %5,3 (t 1,3)", 2.24, 2.34, "0,58 log / 0,71 basit", "0,41 log / 0,60 basit", 17.5,
 "ORTA", "ORTA", "ORTA", "2022+ B&H'yi geçmiyor (0,57'ye 0,58); 20 bps'de marjinal; C2j ile aynı fenomen.", "Midas'ta uygulanabilir; C2j ile birlikte tek fenomen say.", "E_C2_h3"),
("E2-C1_madenci_oncu_GLD_h5", "e2", "ETF", "GDX'in GLD+SPY'ye göre 10 günlük artık toplamı > IS %80 kantili ise GLD uzun 5 gün kademeli; aksi nakit. Kaplama: GLD tut, yalnız < %20 kantilde nakit.", "t-1 16:00 ET", 5, "58,4 bps/aktif gün, 5 günlük (OOS 55,3)", "net %5,4/yıl (1x, tam; beta dahil); alfa %3,5 (t 2,8), OOS %2,2 (t 1,3)", 3.46, 1.94, "0,73 log / 0,78 basit", "0,72 log / 0,81 basit", 5.6,
 "ORTA", "ORTA", "ORTA", "OOS t<2; yalnız uzun B&H'yi geçmiyor; 2018-24 IC≈0; kaplamanın üstünlüğü 2026 Oca-Şub çöküşüne dayanıyor.", "Midas'ta uygulanabilir; en pratik kullanım GLD tutan için kaplama/risk filtresi.", "E_C1_h5"),
("E2-C5_asya_madenci_GLD", "e2", "ETF", "Asya altın madencileri artığı (gün t HK/SS kapanışı) > IS %70 ise GLD uzun 3 gün.", "t 08:10 UTC", 3, "—", "—", 2.08, 2.48, "0,84", "0,72", 35, "ORTA", "ORTA", "DUSUK", "2018-21 IC 0; 20 bps'de B&H altında; takvim hizasına duyarlı.", "Teyit sinyali olabilir.", ""),
("E2-C4_platin5_GDX", "e2", "ETF", "Platin vadelisi 5 günlük değişimi < IS %20 ise GDX uzun 3 gün.", "t-1 NYMEX kapanışı", 3, "—", "—", -1.99, -3.87, "0,69", "0,41", 23, "DUSUK", "DUSUK", "DUSUK", "IS verisi kirli (PL=F 2008-09 sıçramaları); temiz PPLT ile IS t −0,7; mekanizma yok.", "—", ""),
("E2-C3_altin_gunici_GDX", "e2", "ETF", "Altın [t-1 16:00→t 15:00 ET] < IS %30 ise GDX uzun 1 gün, > %70 kısa.", "t 15:00 ET", 1, "—", "—", -3.25, -2.05, "0,37 (yalnız uzun)", "0,41", 105, "DUSUK", "DUSUK", "DUSUK", "Maliyet sonrası ≈0; 2013-17'de yoğun; E3-2 ile aynı.", "—", ""),
# ---------------- e3
("E3-1_altin_gunici_GDXJ_donus", "e3", "ETF", "m_t=ln(spot altın 15:00 ET_t / spot 16:00 ET_t-1). m_t<0 ise GDXJ'yi t kapanışında al, t+1 kapanışında sat (koşul sürerse koru); aksi nakit. ABD yarım günleri hariç.", "t 15:00 ET (19:00/20:00 UTC)", 1, "18,0 bps/aktif gün (OOS 20,8)", "net %19,9/yıl (1x, tam; beta dahil); alfa %13,4 (t 2,5), OOS %10,6 (t 1,4)", -4.8, -2.77, "0,72 (10 bps) / 0,51 (20 bps)", "0,54", 66,
 "YUKSEK", "YUKSEK", "ORTA", "Maliyet sonrası B&H'ye göre alfa OOS anlamsız (10 bps t 1,41; 20 bps t 0,54); etki 2013-17'de yoğun; GDX'te 2008 −%48,7 (kriz kuyruğu); doğrusal etki zayıf.", "Midas'ta uygulanabilir ama yılda ~66 gidiş-dönüş; 1,5 USD/emir küçük hesapta pahalı.", "E_M_GDXJ_h1"),
("E3-2_altin_gunici_GDX", "e3", "ETF", "E3-1 kuralı GDX'te.", "t 15:00 ET", 1, "—", "—", -3.48, -1.87, "0,61", "0,61", 65, "ORTA", "ORTA", "DUSUK", "OOS t −1,87; B&H'ye eşit; 2008'de ters.", "E3-1'in uzantısı.", ""),
("E3-3_PHYS_GLD_iskonto", "e3", "ETF", "z=[ln(PHYS/GLD)_t-1 − 60g medyan]/250g std. z<−1,5 iken altın alınacaksa PHYS'i seç (GLD yerine).", "t-1 16:00 ET", 5, "z<−2: PHYS 5 günde +19-21 bps iyi", "—", -4.31, -4.87, "geçiş stratejisi IR −0,29", "—", 7,
 "ORTA", "ORTA", "ORTA", "Ekonomik büyüklük küçük; PHYS fiyat adımı 3-9 bps; Midas'ta PHYS doğrulanmadı.", "Yönlü sinyal değil; yalnız araç seçimi.", ""),
("E3-4_CEF_artik", "e3", "ETF", "CEF−(β_g·GLD+β_s·SLV) artık z (t-1) < −2 iken CEF'i tercih et.", "t-1 16:00 ET", 5, "z<−2: 5 günde +32/+59 bps", "—", -5.15, -4.41, "geçiş IR 0,07", "—", 2, "ORTA", "ORTA", "ORTA", "Asimetrik ve kararsız; geçiş kuralı OOS'ta başarısız.", "Yalnız araç seçimi.", ""),
("E3-5_GLDTR_prim", "e3", "BIST-BYF", "GLDTR primi üst %20 iken BYF yerine VİOP/ETF seç.", "t ≤14:30 UTC", 1, "−18 bps (h1)", "—", np.nan, -3.85, "—", "—", 0, "DUSUK", "DUSUK", "DUSUK", "Veri kusuru (kış barları eksik); 3 yıl; IS yok.", "Cephe dışı.", ""),
("E3-6_GLD_akis", "e3", "ETF", "GLD/GLDM pay akışları → getiri.", "t-1/t-2", 1, "—", "—", 0.47, -1.3, "0,21", "0,81", 0, "YOK", "YOK", "YOK", "Akış fiyatı takip ediyor.", "—", ""),
]
T = pd.DataFrame(R, columns=C)
def son(r):
    a, b = r.rep, r.adv
    s = min([a, b], key=lambda z: RANK[z])
    return s
T["son_guven"] = T.apply(son, axis=1)
T["gerekce"] = "min(REP, ADV)"
# ayakta kalan seçimi: ORTA+ (ETF) ya da VİOP'ta DÜŞÜK'lerin en iyileri (kural: IS ve OOS aynı işaret, |t_IS|≥1,3, |t_OOS|≥2, işlenebilir, varyant değil)
best_dusuk = {"A1-LOWMOM-h1", "A1-LOWMOM-h5", "A3_QEND_h3", "A4-C1_GDXJ_artik_h3", "A8-3_seg_last1h_h5"}
T["ayakta"] = np.where(T.id.isin(best_dusuk), "EVET (DÜŞÜK'lerin en iyisi)", np.where((T.son_guven.isin(["ORTA", "YUKSEK"])) & ~T.id.isin(["E3-3_PHYS_GLD_iskonto", "E3-4_CEF_artik"]), "EVET (ORTA)",
                       np.where(T.id.isin(["E3-3_PHYS_GLD_iskonto", "E3-4_CEF_artik"]), "araç seçimi kuralı (ORTA)", "HAYIR")))
T.loc[T.id == "A1-LOWMOM-h5", "ayakta"] = "EVET (LOWMOM'un 5 günlük tutuş varyantı)"
# hakem yeniden hesap sütunları
D = pd.read_csv(f"{OUT}/dogrulama.csv"); D = D[D.getiri == "basit"]
EV = pd.read_csv(f"{OUT}/islem_basi.csv").set_index("sinyal")
for col, per, f in [("hakem_tam_sharpe", "tam", "sharpe"), ("hakem_IS_sharpe", "IS", "sharpe"), ("hakem_OOS_sharpe", "OOS", "sharpe"), ("hakem_OOS_sharpe_stres", "OOS", "sharpe_stres"),
                    ("hakem_OOS_dm", "OOS", "sharpe_dm"), ("hakem_OOS_BH", "OOS", "bh_sharpe"), ("hakem_2022p_sharpe", "2022+", "sharpe"), ("hakem_2022p_BH", "2022+", "bh_sharpe"),
                    ("hakem_tam_yillik_pct", "tam", "ann_pct"), ("hakem_2026_sharpe", "2026", "sharpe")]:
    m = D[D.donem == per].set_index("sinyal")[f]
    T[col] = T.hakem_kod.map(m)
T["hakem_gidis_donus_yil"] = T.hakem_kod.map(EV.gidis_donus_yil)
T["hakem_maruziyet"] = T.hakem_kod.map(EV.maruziyet)
T = T[["id", "aile", "cephe", "ayakta", "son_guven", "analist", "rep", "adv", "gerekce", "kural", "bilgi_zamani", "h", "etki_bps_islem", "etki_yillik", "t_IS", "t_OOS",
       "oos_sharpe_net", "oos_bh_sharpe", "yilda_islem", "ana_zayiflik", "islenebilirlik", "hakem_kod", "hakem_tam_sharpe", "hakem_IS_sharpe", "hakem_OOS_sharpe", "hakem_OOS_sharpe_stres",
       "hakem_OOS_dm", "hakem_OOS_BH", "hakem_2022p_sharpe", "hakem_2022p_BH", "hakem_2026_sharpe", "hakem_tam_yillik_pct", "hakem_gidis_donus_yil", "hakem_maruziyet"]]
T.to_csv(f"{OUT}/sinyal_tablosu.csv", index=False)
print(T.groupby(["cephe", "son_guven"]).size().unstack(fill_value=0))
print(T[T.ayakta != "HAYIR"][["id", "son_guven", "ayakta", "hakem_OOS_sharpe", "hakem_OOS_BH", "hakem_2026_sharpe"]].to_string())
print(len(T))
