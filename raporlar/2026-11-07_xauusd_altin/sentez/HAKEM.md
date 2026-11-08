# HAKEM: altın 1/3/5 günlük sinyaller için metodoloji denetimi ve son karar

Tarih 2026-11-08. Veri 2026-11-06 Cuma kapanışına kadar. İki cephe var:
- **VİOP F_XAUUSD.** Giriş gün t uzlaşması, karar 15:00 UTC.
- **Midas ABD ETF'leri.** Giriş 16:00 ET kapanışı, karar 15:00 ET. Açığa satış yok.

Bütün sayılar `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/sentez/` altındaki betiklerle yeniden üretilebilir (s01–s07, ortak kütüphane `sl.py`).

---

## 0. Kısa hüküm

1. **VİOP'ta tek başına güvenilir bir öngörücü bulunamadı.**
   - İşlenebilir 2.621 birincil test var. Hiçbiri BH q<0,10'u geçmiyor; en küçük q 0,29. Bonferroni'yi geçen de yok.
   - p<0,05 olan test sayısı 184, şansla beklenen 131. Hafif bir fazlalık var ama tek tek seçilebilecek düzeyde değil.
   - Son güvende VİOP'ta ORTA kalan iddia yok: 18 DÜŞÜK, 26 YOK.
2. **ETF'te istatistiksel öngörülebilirlik var, maliyet sonrası kâr kanıtı zayıf.**
   - 2.130 birincil testin 18'i q<0,05'i, 5'i Bonferroni'yi geçiyor. Hepsi üç fenomene düşüyor:
     - (i) Altının 15:00 ET'ye kadarki hareketi madenci ETF'lerinde ertesi gün ters yönde sürüyor. Bonferroni'yi geçen tek aile bu.
     - (ii) Metallerin 1–5 günlük hareketi GDX'te ters yönde sürüyor.
     - (iii) Madenci artığı GLD'yi öngörüyor.
   - Ama (i)'nin yalnız uzun kuralında B&H'ye göre OOS alfası 10 bps maliyette t 1,4. Yani istatistik gerçek, net kâr kanıtı zayıf.
3. **Ayakta kalanlar.**
   - VİOP: ORTA kalan olmadığı için DÜŞÜK'lerin en iyi 4'ü alındı: LOWMOM, çeyrek sonu, GDXJ artığı, son saat.
   - ETF: 5 yönlü ORTA (tatil öncesi GDX, C2j, C2, C1, E3-1) ve 2 araç seçimi kuralı (PHYS/GLD, CEF).
   - İki cephe birlikte düşünüldüğünde gerçekten bağımsız fenomen sayısı yaklaşık 5.
4. **Eşit ağırlıklı birleşim.** Sinyaller sonradan seçildiği için bu sonuçlar bir üst sınırdır.

   | Cephe | Tam net Sharpe | OOS | 2022+ | Kıyas | Not |
   |---|---|---|---|---|---|
   | VİOP | 1,33 | 1,59 | 1,59 | VİOP B&H 0,57 | Ortalama mutlak pozisyon 0,19; yıllık %4,2 (1x nominal) |
   | ETF | 0,86 | 1,02 | 1,09 | GDX/GDXJ/GLD sepeti 0,34 / 0,64 / 0,79 | |

   Yarıya indirilmiş gerçekçi beklenti:
   - VİOP: Sharpe ≈ 0,7, yılda %2 (1x).
   - ETF: Sharpe ≈ 0,4–0,5, sepete göre alfa yılda ≈ %3.
5. **Pazartesi 2026-11-09.**
   - VİOP:
     - LOWMOM pasif: rv20 %21, eşik %11,7.
     - Çeyrek sonu pasif; bir sonraki giriş 30 Aralık.
     - GDXJ artığının yeni dilimi UZUN.
     - Son saat sinyali koşullu, Pazartesi 14→15 UTC hareketine bakar.
     - Birleşik VİOP pozisyonu fiilen düz: +0,03 ya da −0,07 birim.
   - ETF:
     - C2j, C2 ve C1 UZUN (madenciler geçen hafta altını çok geçti).
     - E3-1 koşullu: Pazartesi 15:00 ET'de spot altın 4.065,68 USD'nin altındaysa GDXJ alınır.
     - Tatil öncesi kuralı pasif; bir sonraki giriş 24 Kasım kapanışı.
6. **Risk.**
   - 2026 rejiminde F_XAUUSD için 1 günlük VaR99 %5,0, 5 günlük %11,8.
   - Nominal/özsermaye 3 olursa 5 günlük VaR99 kaybı özsermayenin %35'i olur. Öneri: nominal ≤ 2× özsermaye.
   - Dip alma (2σ dönüş) kuralları üç dönemde de zarar ettiriyor. 1 günlük kısa stop maliyetsiz, ama alfa kaynağı değil.

---

## 1. Test ayıklama ve çoklu test düzeltmesi

### 1.1 Ayıklama kuralı

Bir test, aşağıdaki sınıflardan ilk eşleştiğine atanır. Kod: `s01_fdr.py`.

| Sınıf | Tanım | Örnek |
|---|---|---|
| X1 kapanışta / cutoff sonrası | Bilgi zamanı karar anından sonra ya da giriş fiyatıyla eş zamanlı. Kayıtta "KAPANIŞTA HESAPLANAN", "CUTOFF SONRASI", "K t 15:10" notu taşıyanlar, `viop_pos_sameday`, a1'in `_vt` (gün t VİOP) backtest sürümleri. | v_ret_t'nin işareti, gün t OI |
| X2 mekanik | Hedef ile öngörücü aynı fiyat gürültüsünü paylaşıyor. | eb_t → VİOP−spot (t −25); GLD primi_t → GLD−spot (t −26) |
| X3 tanı / kontrol / betimsel | İşlem kuralı değil. | Emilim pencereleri, kısmi regresyonlar, kontrol testleri, oynaklık oranları, ters yön (akış ← fiyat), aşınma ölçümleri, segment ortalamaları, ayrıştırmalar, "tanı" notlu satırlar |
| X4 kapanıştan kapanışa değil | Hedef bir seans bacağı. | Akşam→sabah, gece/gün içi bacak, son saat, hafta sonu boşluğu |
| X5 göreli / cephe dışı | Hedef bir spread (açığa satış gerekir) ya da altın yönü değil. | VİOP−spot baz, USDTRY, gram primi RV, madenci ileri artığı, PHYS/CEF spread, GLD−spot, BIST BYF |
| X6 birebir kopya | Aynı testin tekrar kaydı. | `r4_turkiye_altin` (a7'nin aynısı), e2 `s6_strateji` (c_/a_ testlerinin tekrarı) |
| R1 sağlamlık / varyant | İşlenebilir ama birincil değil: komşuluk, alternatif hedef (spot), IS-seçilmiş tekrar, bacak ayrıştırması, kural sürümü. | `robust_*`, `*_spot`, `f_final`, `a2_leg` |
| R2 erken dönem | İşlenebilir ama birincil değil: 2010–2016 (2008 öncesi dahil) bağımsız tekrar. | `*_early`, V3 |

Kalan küme = **işlenebilir öngörü (geniş)**. Bunun içinden R1 ve R2 çıkarılınca **birincil** küme kalır. BH-FDR ve Bonferroni her kümede VİOP ve ETF alanı için ayrı uygulandı. a6'nın e3'teki `a_flow_viop` testleri VİOP alanına sayıldı.

### 1.2 Sonuç

| Sınıf | VIOP | ETF | toplam |
|---|---|---|---|
| Birincil işlenebilir öngörü | 2.621 | 2.130 | 4.751 |
| R1 sağlamlık/varyant (işlenebilir, birincil değil) | 895 | 185 | 1.080 |
| R2 erken dönem tekrarı (işlenebilir, birincil değil) | 614 | 0 | 614 |
| X1 kapanışta/cutoff sonrası | 269 | 0 | 269 |
| X2 mekanik | 3 | 8 | 11 |
| X3 tanı/kontrol/betimsel | 409 | 146 | 555 |
| X4 kapanıştan kapanışa değil | 11 | 12 | 23 |
| X5 göreli/spread ya da cephe dışı | 37 | 80 | 117 |
| X6 birebir kopya | 18 | 8 | 26 |

| Küme | Alan | Test | p<0,05 | Şansla beklenen | mutlak t≥3 | BH q<0,05 | BH q<0,10 | Bonferroni<0,05 | Bonf. t eşiği | En küçük q |
|---|---|---|---|---|---|---|---|---|---|---|
| işlenebilir (geniş) | VIOP | 4.130 | 389 | 206,5 | 59 | 0 | 0 | 0 | 4,38 | 0,1702 |
| işlenebilir (geniş) | ETF | 2.315 | 281 | 115,8 | 66 | 37 | 66 | 6 | 4,25 | 0,0001 |
| birincil | VIOP | 2.621 | 184 | 131,1 | 20 | 0 | 0 | 0 | 4,28 | 0,2932 |
| birincil | ETF | 2.130 | 255 | 106,5 | 52 | 18 | 44 | 5 | 4,23 | 0,0000 |

**Okuma.**
- **VİOP.** Gözlenen p<0,05 sayısı beklenenin yaklaşık 1,4 katı (184/131). Bu bir miktar gerçek sinyal olduğunu düşündürüyor. Ama en iyi testin q'su 0,29. Hangi testin gerçek olduğu çoklu test düzeltmesiyle ayırt edilemiyor. Sağlamlık ve erken dönem varyantları eklendiğinde de değişmiyor (geniş kümede en küçük q 0,17).
- **ETF.** p<0,05 sayısı beklenenin 2,4 katı (255/106). 18 test q<0,05'te, 5 test Bonferroni'de geçiyor.
- Eski global kayıtta q<0,05 olan 158 testin yalnız 38'i birincil. Kalanlar şöyle dağılıyor:
  - 46 tanı
  - 31 göreli/cephe dışı
  - 24 sağlamlık
  - 7 kopya
  - 6 mekanik
  - 6 kapanış/erken/kapanıştan kapanışa olmayan
  Global q'yu bu testler aşağı çekiyordu.

### 1.3 ETF'te birincil q<0,05'i geçen 18 test

| Aile | Test | h | t | t IS | t OOS | q (BH, alan içi) | Bonferroni p | Fenomen |
|---|---|---|---|---|---|---|---|---|
| e3_etf_akis_prim | d2_zm14_GDXJ_h1 | 1 | -5,59 | -4,89 | -3,08 | 0,0000 | 0,0000 | altın gün içi hareketi → madenci ertesi gün ters |
| e3_etf_akis_prim | d_zm_GDXJ_h1 | 1 | -5,30 | -4,80 | -2,77 | 0,0001 | 0,0002 | altın gün içi hareketi → madenci ertesi gün ters |
| e3_etf_akis_prim | d_zm_GDXJ_h5 | 5 | -4,49 | -3,13 | -3,27 | 0,0041 | 0,0150 | altın gün içi hareketi → madenci ertesi gün ters |
| e3_etf_akis_prim | d2_zm14_GDXJ_h5 | 5 | -4,47 | -3,31 | -3,07 | 0,0041 | 0,0163 | altın gün içi hareketi → madenci ertesi gün ters |
| e3_etf_akis_prim | d2_zm14_GDX_h1 | 1 | -4,32 | -3,78 | -2,30 | 0,0065 | 0,0327 | altın gün içi hareketi → madenci ertesi gün ters |
| e2_etf_leadlag | c_PLATIN_d5_GDX_h3 | 3 | -4,18 | -1,99 | -3,87 | 0,0106 | 0,0633 | metal 1-5 g hareketi → GDX ters |
| e2_etf_leadlag | c_PLATIN_d5_GDX_h5 | 5 | -4,12 | -2,19 | -3,66 | 0,0117 | 0,0817 | metal 1-5 g hareketi → GDX ters |
| e3_etf_akis_prim | d2_zm_JNUG_h1 | 1 | -4,01 | -4,18 | -1,72 | 0,0161 | 0,1287 | altın gün içi hareketi → madenci ertesi gün ters |
| e2_etf_leadlag | a1_GDX~GLD+SPY_k10_GLD_h5 | 5 | 3,93 | 3,46 | 1,94 | 0,0188 | 0,1816 | madenci artığı → GLD |
| e3_etf_akis_prim | d2_zm_JNUG_h5 | 5 | -3,92 | -2,65 | -2,79 | 0,0188 | 0,1883 | altın gün içi hareketi → madenci ertesi gün ters |
| e2_etf_leadlag | b1_xau_intraday_GDX_h1 | 1 | -3,84 | -3,41 | -1,86 | 0,0237 | 0,2663 | altın gün içi hareketi → madenci ertesi gün ters |
| e3_etf_akis_prim | d_zm_GDX_h1 | 1 | -3,82 | -3,48 | -1,87 | 0,0237 | 0,2839 | altın gün içi hareketi → madenci ertesi gün ters |
| e3_etf_akis_prim | d2_zB_abd_sabah_GDXJ_h1 | 1 | -3,79 | -3,11 | -2,20 | 0,0248 | 0,3222 | altın gün içi hareketi → madenci ertesi gün ters |
| e2_etf_leadlag | a1_GDX~GLD+SPY_k10_GLD_h3 | 3 | 3,76 | 3,24 | 2,00 | 0,0257 | 0,3591 | madenci artığı → GLD |
| e3_etf_akis_prim | d2_zA_asya_avrupa_GDX_h5 | 5 | -3,65 | -1,72 | -3,34 | 0,0367 | 0,5505 | altın gün içi hareketi → madenci ertesi gün ters |
| e2_etf_leadlag | c_JP_GOLD_ETF_1328_d5_GDX_h5 | 5 | -3,57 | -2,29 | -2,84 | 0,0449 | 0,7649 | metal 1-5 g hareketi → GDX ters |
| e2_etf_leadlag | c_PLATIN_d5_GDX_h1 | 1 | -3,56 | -2,08 | -2,99 | 0,0449 | 0,7961 | metal 1-5 g hareketi → GDX ters |
| e2_etf_leadlag | c_PLATIN_d1_GDX_h5 | 5 | -3,55 | -2,06 | -2,97 | 0,0449 | 0,8086 | metal 1-5 g hareketi → GDX ters |

Ayakta kalan sinyallerin kendi testlerinin birincil alan içi q değerleri:

| Cephe | Sinyal | q | Not |
|---|---|---|---|
| ETF | E3-1 (m_t → GDXJ h1) | 0,0001 | Bonferroni p 0,0002 |
| ETF | E2-C1 (GDX k10 → GLD h5) | 0,019 | |
| ETF | E2-C2j (GDXJ k1 → GDXJ h3) | 0,056 | |
| ETF | E2-C2 (GDX k3 → GDX h3) | 0,069 | |
| ETF | E1-C2 (tatil öncesi GDX) | 0,126 | |
| VİOP | A4-C1 (GDXJ artığı) | 0,29 | |
| VİOP | LOWMOM | 0,33 | |
| VİOP | Çeyrek sonu | 0,33 | |
| VİOP | Son saat | 0,50 | |

---

## 2. İddia tablosu (65 iddia, 11 aile)

**SON güven kuralı.** SON güven = min(REP, ADV). Analist etiketi yalnız bilgi amaçlı gösterildi. Hiçbir iddiada bu birleşimi yukarı çekmedim. Gerekçe: yukarı çekmeyi haklı kılacak bağımsız bir kanıt yok. Erken dönem ya da başka cephede tekrar, birkaç iddiada (LOWMOM, A4-C1/E2-C2j) zaten REP ve ADV tarafından tartılmıştı.

**"Ayakta" kuralı.** Kural önceden yazıldı, sonra uygulandı.
- **ETF:** SON güven ORTA ve yönlü sinyal.
- **VİOP:** ORTA yok. Bu yüzden DÜŞÜK'lerin en iyileri alındı. Koşullar:
  - IS ve OOS'ta aynı işaret.
  - |t_IS| ≥ 1,3 ve |t_OOS| ≥ 2.
  - Kapanıştan kapanışa işlenebilir.
  - Başka bir iddianın varyantı değil.

  Bu koşulları LOWMOM-h1, çeyrek sonu, A4-C1 ve son saat (A8-3) geçiyor.

  Kalan yakınlar ve neden elendikleri:
  - A4-C1b (madenci kompozit) ve A1-VOLREG5: t eşiklerini geçiyor ama varyant. VOLREG'in LOWMOM dışındaki bacağı çürük.
  - a7_C1 (USDTRY carry): t eşiklerini geçiyor ama hedefi altın değil, F_USDTRY.
  - a5_C1: OOS t 1,93.
  - NFP momentumu: IS t 0,55.
  - Çin madenci artığı: IS t 0,37.
  - a5_B1 ve A8-2: IS'te işaret yok.
- E3-3 ve E3-4 ORTA, ama yönlü sinyal değil. Yalnız araç seçimi (GLD yerine PHYS/CEF) kuralı olarak ayrı tutuldu.

**Etki sütunları.** Ayakta kalanlarda etki ve Sharpe değerleri hakemin kendi yeniden hesabından alındı (`hakem_*` sütunları, basit getiri). Ayrıntı §2.3'te.

### 2.1 Ayakta kalanlar: kesin kural ve sayılar

| İddia | Cephe | SON güven | Kural | Bilgi zamanı | h | Etki (işlem başı, brüt) | Etki (yıllık, net) | t IS | t OOS | OOS net Sharpe (analist) | OOS B&H (analist) | Hakem OOS Sharpe | Hakem OOS stres | Hakem OOS B&H | Hakem 2022+ | B&H 2022+ | Hakem 2026 | Gidiş-dönüş/yıl | Ana zayıflık | İşlenebilirlik |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1-LOWMOM-h1 | VIOP | DUSUK | P=spot XAUUSD 15:00 UTC; x=ln(P_t/P_t-5); rv20=son 20 günlük ΔlnP std; q=rv20'nin 2010'dan beri genişleyen yüzdeliği (bugün dahil). q<1/3 (≈yıllık %11,7) ise t uzlaşmasında sign(x) yönünde 1 birim aç, t+1 uzlaşmasında kapat (aynı yön sürerse netleştir); q≥1/3 ise nakit. | t 15:00 UTC (Dukascopy 14:00 barı kapanışı) | 1 | 8,1 bps/aktif gün (OOS 14,9) | net %7,2/yıl (1x, tam); alfa %7,1 (t 2,9), OOS %7,6 (t 2,6) | 2,38 | 2,68 | 1,36 (dm 1,31) | 0,53 | 1,35 | 1,22 | 0,62 | 1,35 | 0,62 | — | 21,70 | Izgara tepesi (280 komşunun 99. yüzdeliği; medyan ≈0,4); 2017-19'da etki yok; en iyi 20 gün PnL'in %66-75'i; 2026'da hiç tetiklenmedi. | Uygulanabilir (VİOP, 5 bps, yılda ~22 gidiş-dönüş; TR yarım günleri hariç); 2026 rejiminde pasif. |
| A1-LOWMOM-h5 | VIOP | DUSUK | A1-LOWMOM-h1 ile aynı sinyal; t uzlaşmasında aç, t+5'te kapat; her gün sermayenin 1/5'i (kademeli). | t 15:00 UTC | 5 | 29,0 bps/aktif gün, 5 günlük (OOS 67,9) | net %5,4/yıl (1x, tam) | 0,64 | 3,64 | 1,69 (dm 1,63) | 0,53 | 1,70 | 1,63 | 0,62 | 1,70 | 0,62 | — | 11,10 | h1'in tutuş varyantı, bağımsız değil; IS IC t 0,64; 2017-19 negatif; OOS yalnız 278 aktif güne dayanıyor. | Uygulanabilir; 2026'da pasif. |
| A3_QEND_h3 | VIOP | DUSUK | Mar/Haz/Eyl/Ara'nın sondan 2. VİOP işlem günü uzlaşmasında UZUN, 3 VİOP günü sonra (yeni çeyreğin 2. günü) kapat; diğer günler nakit. | Takvim (önceden bilinir) | 3 | +76,7 bps/olay (diğer günler +8,3; fark +68,5) | net %1,0/yıl (maruziyet %1,6); alfa t 2,75 | 2,13 | 2,26 | 0,99 (dm 0,87) | 0,53 | 1,00 | 0,94 | 0,62 | 1,00 | 0,62 | 1,21 | 1,40 | 39 olay; sağlam kısım yıl dönümü; Mar/Haz/Eyl 2010-16'da yok (t 0,61); 2017-19 ve 2022-23 ≈0; BH q 0,06. | Uygulanabilir, çok düşük devir; tek başına küçük katkı. |
| A4-C1_GDXJ_artik_h3 | VIOP | DUSUK | e=r_GDXJ−β60·r_GLD (Yahoo adjclose, t-2→t-1 ABD kapanışı, VİOP satırlarında fark; β önceki 60 gün); z=e/std(e, önceki 120 gün). z>0,43 UZUN, z<−0,43 KISA; 3 gün kademeli. | t-1 16:00 ET ABD kapanışı (cutoff'tan 18-19 saat önce) | 3 | 12,1 bps/aktif gün, 3 günlük (OOS 16,9) | net %3,9/yıl (1x, tam); alfa %4,7 (t 1,8), OOS %7,6 (t 1,7) | 2,53 | 2,63 | 0,72 (dm 0,76) | 0,53 | 0,71 | 0,52 | 0,62 | 0,71 | 0,62 | 0,39 | 34,00 | Kanıt sıra IC'sinde; kural P&L t tam 1,64/IS 0,53; IS gücü 2017'den; 2025-26 IC t 0,86; 2010-16 spotta yok; ABD takvimiyle kurunca OOS 0,52. | Uygulanabilir; ETF tarafındaki E2-C2j ile aynı öngörücü (sıra korelasyonu 0,87). |
| A8-3_seg_last1h_h5 | VIOP | DUSUK | pos=sign(ln(p15/p14)) (spot 14:00→15:00 UTC); t uzlaşmasında gir, 5 gün kademeli; TR yarım günleri hariç. | t 15:00 UTC | 5 | 10,3 bps/aktif gün, 5 günlük (OOS 13,7) | net %3,9/yıl (1x, tam); alfa %3,6 (t 1,5), OOS %5,1 (t 1,25) | 1,32 | 2,05 | 0,63 (dm 0,57) | 0,53 | 0,66 | 0,51 | 0,62 | 0,66 | 0,62 | 1,93 | 25,40 | 2010-16'da h1-h3'te yok; 2024 Sharpe −2,31; kazanç 2026'ya yığılı; kısa bacak her dönemde zarar; 309 testten seçildi. | Uygulanabilir; Pazartesi 14-15 UTC verisi gerekir. |
| E1-C2_GDX_tatil_oncesi | ETF | ORTA | NYSE tatilinden önceki son işlem gününden bir önceki kapanışta GDX al, tatil öncesi gün kapanışında sat (yalnız uzun). | Takvim (önceden bilinir) | 1 | +47,3 bps/olay (diğer −0,2) | net %3,6/yıl (1x nominal, tam); B&H'ye göre alfa %3,3 (t 2,3), OOS %4,3 (t 2,1) | 1,71 | 2,45 | 0,75 (10 bps; dm 0,65) | 0,61 | 0,75 | 0,62 | 0,60 | 0,79 | 0,77 | 0,36 | 9,10 | IS t 1,71<2; global q 0,52; aynı gün GLD+SPY kontrolüyle 20 bps (t 2,0); ortalamanın 2/3'ü en iyi 10 günden; 1983-2007 madenci sepetinde 35 bps (t 2,16) kısmi teyit. | Midas'ta uygulanabilir (yılda ~9 işlem); açılış/kapanış emri gerekir. |
| E2-C2j_GDXJ_artik_h3 | ETF | ORTA | e=r_GDXJ−b_GLD·r_GLD−b_SPY·r_SPY (250 günlük yuvarlanan OLS, beta_t-1; getiriler t-2→t-1 kapanış); x=e_t-1 > IS (2008-17) %70 kantili (≈+0,67%) ise GDXJ'yi t kapanışında al, 3 gün kademeli; aksi nakit. | t-1 16:00 ET kapanışı (~23 saat önce) | 3 | 48,5 bps/aktif gün, 3 günlük (OOS 53,1) | net %13,1/yıl (1x, tam; beta dahil); alfa %9,2 (t 3,3), OOS %6,8 (t 1,95) | 1,90 | 3,04 | 0,64 log / 0,81 basit | 0,31 log / 0,54 basit | 0,81 | 0,70 | 0,54 | 0,90 | 0,71 | 0,21 | 16,90 | IS t 1,90; geniş ızgarada dürüst IS seçimi OOS'u ≈0'a indiriyor; Bonferroni'de elenir; 2025-26 IC 0,03 (t 0,6); 2026 YTD ≈0. | Midas'ta uygulanabilir (yalnız uzun); JDST'li ters sürüm KULLANMA. |
| E2-C2_GDX_artik_h3 | ETF | ORTA | GDX'in GLD+SPY'ye göre 3 günlük artık toplamı (t-1'de biter) > IS %70 kantili ise GDX uzun 3 gün; aksi nakit. | t-1 16:00 ET | 3 | 38,1 bps/aktif gün, 3 günlük (OOS 44,3) | net %10,5/yıl (1x, tam; beta dahil); alfa %6,8 (t 2,2), OOS %5,3 (t 1,3) | 2,24 | 2,34 | 0,58 log / 0,71 basit | 0,41 log / 0,60 basit | 0,71 | 0,60 | 0,60 | 0,69 | 0,77 | 0,23 | 17,50 | 2022+ B&H'yi geçmiyor (0,57'ye 0,58); 20 bps'de marjinal; C2j ile aynı fenomen. | Midas'ta uygulanabilir; C2j ile birlikte tek fenomen say. |
| E2-C1_madenci_oncu_GLD_h5 | ETF | ORTA | GDX'in GLD+SPY'ye göre 10 günlük artık toplamı > IS %80 kantili ise GLD uzun 5 gün kademeli; aksi nakit. Kaplama: GLD tut, yalnız < %20 kantilde nakit. | t-1 16:00 ET | 5 | 58,4 bps/aktif gün, 5 günlük (OOS 55,3) | net %5,4/yıl (1x, tam; beta dahil); alfa %3,5 (t 2,8), OOS %2,2 (t 1,3) | 3,46 | 1,94 | 0,73 log / 0,78 basit | 0,72 log / 0,81 basit | 0,78 | 0,69 | 0,81 | 0,84 | 0,95 | 1,16 | 5,60 | OOS t<2; yalnız uzun B&H'yi geçmiyor; 2018-24 IC≈0; kaplamanın üstünlüğü 2026 Oca-Şub çöküşüne dayanıyor. | Midas'ta uygulanabilir; en pratik kullanım GLD tutan için kaplama/risk filtresi. |
| E3-1_altin_gunici_GDXJ_donus | ETF | ORTA | m_t=ln(spot altın 15:00 ET_t / spot 16:00 ET_t-1). m_t<0 ise GDXJ'yi t kapanışında al, t+1 kapanışında sat (koşul sürerse koru); aksi nakit. ABD yarım günleri hariç. | t 15:00 ET (19:00/20:00 UTC) | 1 | 18,0 bps/aktif gün (OOS 20,8) | net %19,9/yıl (1x, tam; beta dahil); alfa %13,4 (t 2,5), OOS %10,6 (t 1,4) | -4,80 | -2,77 | 0,72 (10 bps) / 0,51 (20 bps) | 0,54 | 0,71 | 0,50 | 0,54 | 0,79 | 0,71 | 0,47 | 66,00 | Maliyet sonrası B&H'ye göre alfa OOS anlamsız (10 bps t 1,41; 20 bps t 0,54); etki 2013-17'de yoğun; GDX'te 2008 −%48,7 (kriz kuyruğu); doğrusal etki zayıf. | Midas'ta uygulanabilir ama yılda ~66 gidiş-dönüş; 1,5 USD/emir küçük hesapta pahalı. |
| E3-3_PHYS_GLD_iskonto | ETF | ORTA | z=[ln(PHYS/GLD)_t-1 − 60g medyan]/250g std. z<−1,5 iken altın alınacaksa PHYS'i seç (GLD yerine). | t-1 16:00 ET | 5 | z<−2: PHYS 5 günde +19-21 bps iyi | — | -4,31 | -4,87 | geçiş stratejisi IR −0,29 | — | — | — | — | — | — | — | — | Ekonomik büyüklük küçük; PHYS fiyat adımı 3-9 bps; Midas'ta PHYS doğrulanmadı. | Yönlü sinyal değil; yalnız araç seçimi. |
| E3-4_CEF_artik | ETF | ORTA | CEF−(β_g·GLD+β_s·SLV) artık z (t-1) < −2 iken CEF'i tercih et. | t-1 16:00 ET | 5 | z<−2: 5 günde +32/+59 bps | — | -5,15 | -4,41 | geçiş IR 0,07 | — | — | — | — | — | — | — | — | Asimetrik ve kararsız; geçiş kuralı OOS'ta başarısız. | Yalnız araç seçimi. |

Notlar:
- "B&H" sütunu, analistin kendi tanımında aynı enstrümanın sürekli uzun Sharpe'ıdır.
- ETF'de "yıllık net" değeri, sinyal aktifken sermayenin tamamı (1x) o ETF'deyse geçerlidir ve beta kazancını içerir.
- Alfa, aynı ETF'nin B&H getirisine regresyonun sabitidir (NW t, gecikme 5).

### 2.2 Bütün iddialar

| İddia | Cephe | h | Bilgi zamanı | Etki | t IS | t OOS | OOS net Sharpe | OOS B&H | İşlem/yıl | Analist | REP | ADV | SON | Ayakta | Ana zayıflık | İşlenebilirlik |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1-LOWMOM-h1 | VIOP | 1 | t 15:00 UTC (Dukascopy 14:00 barı kapanışı) | 8,1 bps/aktif gün (OOS 14,9) | 2,38 | 2,68 | 1,36 (dm 1,31) | 0,53 | 21,50 | ORTA | ORTA | DUSUK | DUSUK | EVET (DÜŞÜK'lerin en iyisi) | Izgara tepesi (280 komşunun 99. yüzdeliği; medyan ≈0,4); 2017-19'da etki yok; en iyi 20 gün PnL'in %66-75'i; 2026'da hiç tetiklenmedi. | Uygulanabilir (VİOP, 5 bps, yılda ~22 gidiş-dönüş; TR yarım günleri hariç); 2026 rejiminde pasif. |
| A1-LOWMOM-h5 | VIOP | 5 | t 15:00 UTC | 29,0 bps/aktif gün, 5 günlük (OOS 67,9) | 0,64 | 3,64 | 1,69 (dm 1,63) | 0,53 | 11,20 | ORTA | ORTA | DUSUK | DUSUK | EVET (LOWMOM'un 5 günlük tutuş varyantı) | h1'in tutuş varyantı, bağımsız değil; IS IC t 0,64; 2017-19 negatif; OOS yalnız 278 aktif güne dayanıyor. | Uygulanabilir; 2026'da pasif. |
| A1-VOLREG5-h5 | VIOP | 5 | t 15:00 UTC | — | 2,78 | 2,24 | 1,03 (dm 1,02) | 0,53 | 21,50 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | LOWMOM dışı kısmı (çalkantıda dönüş) 2010-16'da ve 2022-23'te negatif; k=10'da çöküyor. | Kullanılabilir içeriği LOWMOM ile aynı; 2026'da yalnız çürük bacak aktif olurdu. |
| A1-TAILMOM-BB-h1 | VIOP | 1 | t 15:00 UTC | — | 1,64 | 0,75 | 0,40 (dm 0,34) | 0,53 | 13,60 | DUSUK | DUSUK | YOK | YOK | HAYIR | BB dönüş kuralının aynası; hiçbir dönemde t>2 değil; eşiğe duyarlı. | Tek başına işlem sinyali değil. |
| A1-REV-NEG | VIOP | 1 | t 15:00 UTC | — | -2,15 | -1,14 | −0,57 | 0,53 | 13,60 | YOK | YOK | YOK | YOK | HAYIR | Negatif bulgu: dönüş kuralları üç dönemde de zarar; kayıp kısmen maliyetten. | KULLANMA (ortalama düşürme/dip alma işe yaramıyor). |
| A1-TREND-MA50 | VIOP | 1 | t 15:00 UTC | — | -0,72 | 1,82 | 0,96 (dm 0,83) | 0,53 | 17,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | OOS kârı 2022-26 boğa drift'i; yıl ortalaması çıkarınca Sharpe 0,03; IS negatif. | Trend filtresi yön kenarı vermiyor. |
| a2_c1_S2_gece | VIOP | 0 | t-1 20:00 → t 00:00 UTC takvim etkisi | ~3 bps/gün brüt | 3,60 | 4,57 | 0,28 (gerçek çıkış saatiyle ≈0) | — | 252 | ORTA | ORTA | DUSUK | DUSUK | HAYIR | Brüt kenar ≈ maliyet (5 bps); gerçekçi akşam maliyetiyle negatif; drift'in tahakkuk zamanı, lead-lag değil. | İŞLENEMEZ: kapanıştan kapanışa değil. |
| a2_c2_baz_donus | VIOP | 5 | t-1 15:10 UTC | — | -1,90 | -3,08 | 0,39 (fonlama sonrası ≈0) | — | 36,00 | ORTA | ORTA | DUSUK | DUSUK | HAYIR | İstatistik gerçek ama ekonomik değer yok: OOS kârı taşıma drift'i; düşük hacimli günlerde güçlü (bayat uzlaşma). | İŞLENEMEZ: göreli (spot bacak gerekir). |
| a2_c3_kis_fiks | VIOP | 1 | t 15:00 UTC | — | 1,63 | 2,08 | 1,02 | 0,53 | 100 | DUSUK | DUSUK | YOK | YOK | HAYIR | 30 saat×mevsim testinin en iyisi; erken dönemde yok; IS Sharpe 0,13; yaz fiks saati 0. | — |
| a2_c4_C_pre_h3 | VIOP | 3 | t 15:00 UTC | — | 1,10 | 2,11 | 0,30 | 0,53 | 83,00 | DUSUK | YOK | YOK | YOK | HAYIR | Yalnız h=3'te tepe; 2010-16'da IC 0; kâr 2025-26'dan. | — |
| a2_c5_NY_sabahi | VIOP | 5 | t 15:00 UTC | — | 0,33 | 2,33 | 0,77 | 0,53 | 31,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | IS'te hiçbir eşikte yok; erken dönemde ters; 2022-23'e yaslanıyor. | — |
| A3_QEND_h3 | VIOP | 3 | Takvim (önceden bilinir) | +76,7 bps/olay (diğer günler +8,3; fark +68,5) | 2,13 | 2,26 | 0,99 (dm 0,87) | 0,53 | 4,00 | ORTA | ORTA | DUSUK | DUSUK | EVET (DÜŞÜK'lerin en iyisi) | 39 olay; sağlam kısım yıl dönümü; Mar/Haz/Eyl 2010-16'da yok (t 0,61); 2017-19 ve 2022-23 ≈0; BH q 0,06. | Uygulanabilir, çok düşük devir; tek başına küçük katkı. |
| A3_NFP_MOM_h1 | VIOP | 1 | t 15:00 UTC (NFP 12:30/13:30 UTC) | +18 bps/olay (IS +5,7, OOS +31) | 0,55 | 3,46 | 0,90 | 0,53 | 11,40 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | IS'te yok (t 0,47); 2010-21 boyunca sıfır/ters; en iyi 5 olay çıkınca etki kayboluyor; CPI'da ters işaret. | Uygulanabilir ama yalnız OOS'ta bulunmuş; izleme listesi. |
| A3_NFP_MOM_h3 | VIOP | 3 | t 15:00 UTC | +35 bps/olay | 0,99 | 2,64 | 1,07 | 0,53 | 11,40 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | h1 ile aynı sinyal; fazladan iki gün t 1,53; OOS 2024-26'ya dayanıyor. | Bağımsız değil. |
| A3_OG_EXPIRY_DAY | VIOP | 1 | Takvim | −23,8 bps/olay | -0,95 | -3,11 | 1,03 | 0,53 | 12,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | 17 yıllık spotta etki 0 (t −0,35); tek günlük sivri tepe; 2024-26 birkaç düşüş günü. | — |
| A3_BAYRAM_POST | VIOP | 5 | Takvim | −78 bps/olay (düzeltilmiş) | -2,10 | -2,08 | 0,43 | 0,53 | 2,20 | DUSUK | DUSUK | YOK | YOK | HAYIR | Kod hatası (sahte olay); 20 olay; erken dönemde ters; mekanizma yok. | — |
| A3_JANUARY | VIOP | 1 | Takvim | +15 bps/gün fark | 0,72 | 2,00 | 0,84 | 0,51 | 1,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | 12 ay testinden biri; Ocak 2026 ve 2017 çıkınca t 0,94. | — |
| A4-C1_GDXJ_artik_h3 | VIOP | 3 | t-1 16:00 ET ABD kapanışı (cutoff'tan 18-19 saat önce) | 12,1 bps/aktif gün, 3 günlük (OOS 16,9) | 2,53 | 2,63 | 0,72 (dm 0,76) | 0,53 | 34,00 | ORTA | DUSUK | DUSUK | DUSUK | EVET (DÜŞÜK'lerin en iyisi) | Kanıt sıra IC'sinde; kural P&L t tam 1,64/IS 0,53; IS gücü 2017'den; 2025-26 IC t 0,86; 2010-16 spotta yok; ABD takvimiyle kurunca OOS 0,52. | Uygulanabilir; ETF tarafındaki E2-C2j ile aynı öngörücü (sıra korelasyonu 0,87). |
| A4-C1b_madenci_kompozit_h3 | VIOP | 3 | t-1 ABD kapanışı | — | 2,27 | 2,43 | 0,38 | 0,53 | 237 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | OOS backtest t 0,83; kısa bacak her iki dönemde zarar; kompozit tek madenciden zayıf. | A4-C1'in varyantı. |
| A4-C2_egri_d5_h1 | VIOP | 1 | t-1 22:00 UTC | — | 1,87 | 2,58 | 0,65 | 0,53 | 243 | DUSUK | DUSUK | YOK | YOK | HAYIR | Getiri 2020 ve 2025-26'dan; 2013-16'da anlamlı ters (t −2,09). | — |
| A4-C3_dxy_sapma_h1 | VIOP | 1 | t 15:00 UTC | — | -2,17 | -1,65 | 0,27 | 0,53 | 205 | DUSUK | YOK | YOK | YOK | HAYIR | OOS t −1,65; 10 bps'de negatif. | — |
| A4-D1_dolar_emilim | VIOP | 0 | t-1 22:00 UTC | — | 1,61 | 2,23 | — | — | 0,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | Etki giriş öncesi pencerede; doğrusal t 1,1. | İŞLENEMEZ (pencere VİOP girişinden önce kapanıyor). |
| A4-C4_reel_dolar_artik | VIOP | 1 | t 15:00 / t-1 | — | 1,62 | 1,70 | 0,36 (dm 0,06) | 0,53 | 218 | YOK | YOK | YOK | YOK | HAYIR | Drift ve momentum vekili. | — |
| a5_C1_makrogunu_artik_h3 | VIOP | 3 | t 15:00 UTC | — | 2,10 | 1,93 | 0,60 | 0,53 | 37,00 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | Spesifikasyona duyarlı (W120/W250'de zayıf); P&L t 1,3; OOS kazanç uzun bacakta; 2019-07 öncesinde yok. | Uygulanabilir ama OOS t<2. |
| a5_C4_londra_ny_artik_h1 | VIOP | 1 | t 15:00 UTC | — | 2,66 | 1,38 | 0,88 | 0,53 | 55,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | Tamamen eşik seçimine bağlı (sign kuralı OOS 0,04); erken vekilde sıfır. | — |
| a5_B1_altin_gumus_5g | VIOP | 1 | t 15:00 UTC | — | -0,68 | -2,82 | 1,12 | 0,53 | 99,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | Post-hoc; IS'te yok; Pearson t −0,56; 2022 sonrası rejim. | — |
| a5_yetisme_YOK | VIOP | 1 | t 15:00 UTC | — | -2,21 | -0,98 | −0,64 | — | 0,00 | YOK | YOK | YOK | YOK | HAYIR | Negatif bulgu: yetişme yok, işaret ters (sürme). | — |
| a5_15to15_artik_YOK | VIOP | 1 | t 15:00 UTC | — | 2,49 | -0,41 | −0,81 | — | 257 | YOK | YOK | YOK | YOK | HAYIR | Negatif bulgu: 297 testte /t/>2 oranı %2. | — |
| a5_oran_zskor_YOK | VIOP | 5 | t 15:00 UTC / t-1 | — | 2,11 | -0,17 | — | — | 0,00 | YOK | YOK | YOK | YOK | HAYIR | IS ve OOS işaretleri ters. | — |
| a6_cn_gold_res_comp_h5 | VIOP | 5 | t 07:00/08:10 UTC | — | 0,37 | 3,40 | 1,41 (REP 1,26) | 0,51 | 121 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | OOS dahil tam örneklemle seçildi; IS 2017-21 ve 2010-16'da t≈0; kanıt 2024-26'da. | Uygulanabilir ama yalnız OOS'ta bulunmuş; izleme listesi. |
| a6_res600547_h5 | VIOP | 5 | t 07:00 UTC | — | 0,86 | 3,08 | 1,02 | 0,51 | 119 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | Ana iddiayla aynı kanıt; 2022-23 negatif. | Varyant. |
| a6_hsi_h3 | VIOP | 3 | t 08:10 UTC | — | 2,37 | 2,11 | 0,24 | 0,51 | 132 | DUSUK | YOK | YOK | YOK | HAYIR | Spot altın kontrolüyle kayboluyor (OOS t 0,56). | — |
| a6_viop_oi5_x_trend_h5 | VIOP | 5 | t-1 bülten | — | -3,61 | -0,62 | 0,38 | 0,51 | 72,00 | DUSUK | YOK | YOK | YOK | HAYIR | Etki tamamen IS'te. | — |
| a6_gpr_z250_h5 | VIOP | 5 | D+1 23:00 varsayımı | — | -1,86 | -1,63 | 0,70 | 0,51 | 87,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | Yayın gecikmesine karşı istikrarsız; gerçek zamanlı veri değil. | — |
| a6_cn_res_sum5_h1 | VIOP | 1 | t 07:00/08:10 UTC | — | 0,90 | 3,64 | 0,97 | 0,51 | 50,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | Post-hoc varyant; aynı veri. | Varyant. |
| a7_C1_usdtry_carry | VIOP-USDTRY | 1 | t-1 15:00/15:10 | — | 3,21 | 2,48 | 1,19 (dm 0,88) | hep kısa +0,55 | 20,50 | ORTA | ORTA | DUSUK | DUSUK | HAYIR | Fiilen 20g kur momentumu; PnL birkaç epizotta; 2024-26'da zamanlama katkısı negatif, kâr carry'den. | Cephe dışı (altın değil). |
| a7_C2_fx_drift | VIOP-USDTRY | 5 | t 15:00 | — | — | 2,71 | — | — | 0,00 | ORTA | DUSUK | DUSUK | DUSUK | HAYIR | Sabit uzun dönem drift eşdeğer; h5 sonucu 2026'ya dayanıyor. | Tahmin, işlem kuralı değil. |
| a7_C3_gram_prim_donus | VIOP-gram | 3 | t-1 15:10 | — | -2,93 | -5,79 | −0,77 | — | 75,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | İstatistik çok güçlü (t −6,1) ama 3 bacak maliyetiyle net zarar. | İŞLENEMEZ (net zarar); yalnız araç seçiminde bilgi. |
| a7_C4_xau_after_usdtry | VIOP | 3 | t-1 15:10 | — | -1,56 | -1,45 | 0,21 (dm −0,01) | 0,53 | 104 | DUSUK | DUSUK | YOK | YOK | HAYIR | Tek tepe; drift'ten. | — |
| a7_C5_TR_sok | VIOP | 3 | t 15:00 / t-1 | −48 bps/olay | -2,29 | -1,48 | 0,45 | 0,53 | 11,80 | DUSUK | DUSUK | YOK | YOK | HAYIR | Kümeleme sonrası anlamsız; ~30 bağımsız epizot. | — |
| a7_C6_xautry_oi | VIOP | 3 | t-1 bülten | — | 0,38 | 2,62 | 0,28 | 0,53 | 109 | DUSUK | DUSUK | YOK | YOK | HAYIR | IS'te sıfır; roll sıçramaları. | — |
| A8-1_ML | VIOP | 1 | ≤ t 15:00 UTC | — | 1,08 | 1,17 | −0,91 | 0,53 | 0,00 | YOK | YOK | YOK | YOK | HAYIR | Negatif bulgu: 0/27 pozitif OOS R². | — |
| A8-2_nom2_d5 | VIOP | 1 | t-1 22:00 UTC | — | -0,26 | -2,48 | 0,66 | 0,53 | 57,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | OOS 2026'dan; IS'te yok; 309 testten seçildi. | — |
| A8-3_seg_last1h_h5 | VIOP | 5 | t 15:00 UTC | 10,3 bps/aktif gün, 5 günlük (OOS 13,7) | 1,32 | 2,05 | 0,63 (dm 0,57) | 0,53 | 25,00 | DUSUK | DUSUK | DUSUK | DUSUK | EVET (DÜŞÜK'lerin en iyisi) | 2010-16'da h1-h3'te yok; 2024 Sharpe −2,31; kazanç 2026'ya yığılı; kısa bacak her dönemde zarar; 309 testten seçildi. | Uygulanabilir; Pazartesi 14-15 UTC verisi gerekir. |
| A8-4_2s10s_d5 | VIOP | 1 | t-1 22:00 UTC | — | 1,50 | 2,53 | 0,85 | 0,53 | 58,00 | DUSUK | YOK | YOK | YOK | HAYIR | Bilgi −Δ2y bacağından; 2025-26'ya yığılı; erken dönemde ters. | — |
| A8-5_C1_combo | VIOP | 1 | ≤ t 15:00 | — | -0,65 | 1,85 | 0,90 | 0,53 | 36,00 | DUSUK | DUSUK | YOK | YOK | HAYIR | Yıl içi IC 7/9 yılda negatif; değer yavaş trendden. | — |
| A8-6_RF_V2_h3 | VIOP | 3 | ≤ t 15:00 | — | -0,92 | 2,11 | 0,80 | 0,53 | 24,00 | DUSUK | YOK | YOK | YOK | HAYIR | Tohuma duyarlı; VAL'de ters; şans düzeyinde. | — |
| E1-C1_madenci_takvim_sepeti | ETF | 1 | Takvim | +59,3 bps/olay (diğer −4,3) | 2,62 | 3,41 | 1,08 (10 bps) | — | 18,60 | ORTA | ORTA | DUSUK | DUSUK | HAYIR | 144 testten sonradan kurulan sepet; ayın ilk günü yarısı aynı gün GLD kontrolüyle kayboluyor; 1983-2007'de t 0,99. | Sağlam kısmı E1-C2 (tatil öncesi). |
| E1-C2_GDX_tatil_oncesi | ETF | 1 | Takvim (önceden bilinir) | +47,3 bps/olay (diğer −0,2) | 1,71 | 2,45 | 0,75 (10 bps; dm 0,65) | 0,61 | 9,30 | ORTA | ORTA | ORTA | ORTA | EVET (ORTA) | IS t 1,71<2; global q 0,52; aynı gün GLD+SPY kontrolüyle 20 bps (t 2,0); ortalamanın 2/3'ü en iyi 10 günden; 1983-2007 madenci sepetinde 35 bps (t 2,16) kısmi teyit. | Midas'ta uygulanabilir (yılda ~9 işlem); açılış/kapanış emri gerekir. |
| E1-C3_GDX_5gun_dusus | ETF | 1 | t-1 kapanış | +76,6 bps/olay | 2,07 | 2,98 | 0,78 | — | 3,40 | ORTA | DUSUK | YOK | YOK | HAYIR | 1.046 testin beklenen maksimumu; eşik 4/6'da çöküyor; GDXJ'de yok. | — |
| E1-C4_GLD_Ocak | ETF | 1 | Takvim | +17 bps/gün | 2,22 | 1,19 | 0,59 | 0,81 | 1,00 | ORTA | DUSUK | YOK | YOK | HAYIR | 48 testin en iyisi; 2001-07'de yok. | — |
| E1-C5_GLD_BollZ_alt | ETF | 5 | t-1 kapanış | +63,9 bps/olay | 0,90 | 2,52 | 0,70 | — | 2,20 | DUSUK | DUSUK | YOK | YOK | HAYIR | Parametreye duyarlı; IS'te yok. | — |
| E1-C6_GLD_gece | ETF | 1 | — | — | 1,08 | 3,37 | −0,79 | — | 252 | DUSUK | DUSUK | YOK | YOK | HAYIR | Başabaş maliyet 4-7 bps; kısmen mekanik. | İŞLENEMEZ (kapanıştan kapanışa değil, maliyet). |
| E2-C2j_GDXJ_artik_h3 | ETF | 3 | t-1 16:00 ET kapanışı (~23 saat önce) | 48,5 bps/aktif gün, 3 günlük (OOS 53,1) | 1,90 | 3,04 | 0,64 log / 0,81 basit | 0,31 log / 0,54 basit | 16,90 | YUKSEK | ORTA | ORTA | ORTA | EVET (ORTA) | IS t 1,90; geniş ızgarada dürüst IS seçimi OOS'u ≈0'a indiriyor; Bonferroni'de elenir; 2025-26 IC 0,03 (t 0,6); 2026 YTD ≈0. | Midas'ta uygulanabilir (yalnız uzun); JDST'li ters sürüm KULLANMA. |
| E2-C2_GDX_artik_h3 | ETF | 3 | t-1 16:00 ET | 38,1 bps/aktif gün, 3 günlük (OOS 44,3) | 2,24 | 2,34 | 0,58 log / 0,71 basit | 0,41 log / 0,60 basit | 17,50 | ORTA | ORTA | ORTA | ORTA | EVET (ORTA) | 2022+ B&H'yi geçmiyor (0,57'ye 0,58); 20 bps'de marjinal; C2j ile aynı fenomen. | Midas'ta uygulanabilir; C2j ile birlikte tek fenomen say. |
| E2-C1_madenci_oncu_GLD_h5 | ETF | 5 | t-1 16:00 ET | 58,4 bps/aktif gün, 5 günlük (OOS 55,3) | 3,46 | 1,94 | 0,73 log / 0,78 basit | 0,72 log / 0,81 basit | 5,60 | ORTA | ORTA | ORTA | ORTA | EVET (ORTA) | OOS t<2; yalnız uzun B&H'yi geçmiyor; 2018-24 IC≈0; kaplamanın üstünlüğü 2026 Oca-Şub çöküşüne dayanıyor. | Midas'ta uygulanabilir; en pratik kullanım GLD tutan için kaplama/risk filtresi. |
| E2-C5_asya_madenci_GLD | ETF | 3 | t 08:10 UTC | — | 2,08 | 2,48 | 0,84 | 0,72 | 35,00 | ORTA | ORTA | DUSUK | DUSUK | HAYIR | 2018-21 IC 0; 20 bps'de B&H altında; takvim hizasına duyarlı. | Teyit sinyali olabilir. |
| E2-C4_platin5_GDX | ETF | 3 | t-1 NYMEX kapanışı | — | -1,99 | -3,87 | 0,69 | 0,41 | 23,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | IS verisi kirli (PL=F 2008-09 sıçramaları); temiz PPLT ile IS t −0,7; mekanizma yok. | — |
| E2-C3_altin_gunici_GDX | ETF | 1 | t 15:00 ET | — | -3,25 | -2,05 | 0,37 (yalnız uzun) | 0,41 | 105 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | Maliyet sonrası ≈0; 2013-17'de yoğun; E3-2 ile aynı. | — |
| E3-1_altin_gunici_GDXJ_donus | ETF | 1 | t 15:00 ET (19:00/20:00 UTC) | 18,0 bps/aktif gün (OOS 20,8) | -4,80 | -2,77 | 0,72 (10 bps) / 0,51 (20 bps) | 0,54 | 66,00 | YUKSEK | YUKSEK | ORTA | ORTA | EVET (ORTA) | Maliyet sonrası B&H'ye göre alfa OOS anlamsız (10 bps t 1,41; 20 bps t 0,54); etki 2013-17'de yoğun; GDX'te 2008 −%48,7 (kriz kuyruğu); doğrusal etki zayıf. | Midas'ta uygulanabilir ama yılda ~66 gidiş-dönüş; 1,5 USD/emir küçük hesapta pahalı. |
| E3-2_altin_gunici_GDX | ETF | 1 | t 15:00 ET | — | -3,48 | -1,87 | 0,61 | 0,61 | 65,00 | ORTA | ORTA | DUSUK | DUSUK | HAYIR | OOS t −1,87; B&H'ye eşit; 2008'de ters. | E3-1'in uzantısı. |
| E3-3_PHYS_GLD_iskonto | ETF | 5 | t-1 16:00 ET | z<−2: PHYS 5 günde +19-21 bps iyi | -4,31 | -4,87 | geçiş stratejisi IR −0,29 | — | 7,00 | ORTA | ORTA | ORTA | ORTA | araç seçimi kuralı (ORTA) | Ekonomik büyüklük küçük; PHYS fiyat adımı 3-9 bps; Midas'ta PHYS doğrulanmadı. | Yönlü sinyal değil; yalnız araç seçimi. |
| E3-4_CEF_artik | ETF | 5 | t-1 16:00 ET | z<−2: 5 günde +32/+59 bps | -5,15 | -4,41 | geçiş IR 0,07 | — | 2,00 | ORTA | ORTA | ORTA | ORTA | araç seçimi kuralı (ORTA) | Asimetrik ve kararsız; geçiş kuralı OOS'ta başarısız. | Yalnız araç seçimi. |
| E3-5_GLDTR_prim | BIST-BYF | 1 | t ≤14:30 UTC | −18 bps (h1) | — | -3,85 | — | — | 0,00 | DUSUK | DUSUK | DUSUK | DUSUK | HAYIR | Veri kusuru (kış barları eksik); 3 yıl; IS yok. | Cephe dışı. |
| E3-6_GLD_akis | ETF | 1 | t-1/t-2 | — | 0,47 | -1,30 | 0,21 | 0,81 | 0,00 | YOK | YOK | YOK | YOK | HAYIR | Akış fiyatı takip ediyor. | — |

CSV'nin tamamı (kural metni, hakem sütunları): `sinyal_tablosu.csv`.

### 2.3 Yeniden hesap doğrulaması ve bir yöntem farkı

Hakem kodu (`sl.py`, `s03_dogrula.py`) ayakta kalan bütün sinyalleri analist tanımlarıyla baştan kurdu:
- VİOP sinyalleri ve E2 sinyalleri analistin log getirili Sharpe'larını 2 ondalığa kadar tuttu. Örnekler: LOWMOM h1 OOS 1,36 / dm 1,31; QEND OOS 0,99; A4-C1 OOS 0,72; C2j OOS yalnız uzun 0,64.
- **Tek tutarsızlık E3-1'de.** E3 basit getiri (e^r−1), diğer bütün aileler log getiri kullanmış. Sabit nominalli günlük pozisyonun gerçek P&L'i basit getiridir. Yüksek oynaklıklı madencilerde fark büyük:
  - GDXJ'nin OOS B&H Sharpe'ı log ile 0,31, basit ile 0,54.
  - GDX'te 0,41'e karşı 0,60.
  - Altında fark küçük: VİOP B&H 0,53'e karşı 0,62.
- **Sentezin bütün P&L'i basit getiriyle yapıldı.** E2 sinyallerinin B&H'ye üstünlüğü bu düzeltmeyle küçülmüyor; ikisi birlikte yükseliyor.
- **Yarım günler dışlandı.**
  - Türkiye yarım günlerinde (21 gün) 15:00 UTC bilgisi kullanan LOWMOM ve son saat sinyalleri sıfırlandı.
  - ABD yarım günlerinde E3-1 sıfırlandı.
  - Etkisi ≤0,02 Sharpe (LOWMOM tam 1,04 → 1,03).

| Sinyal (hakem kodu) | log tam | log IS | log OOS | B&H OOS log | basit tam | basit IS | basit OOS | B&H OOS basit |
|---|---|---|---|---|---|---|---|---|
| E_C1_h5 | 0,76 | 0,78 | 0,73 | 0,72 | 0,81 | 0,83 | 0,78 | 0,81 |
| E_C1kap_h5 | 0,67 | 0,47 | 0,90 | 0,72 | 0,75 | 0,56 | 0,98 | 0,81 |
| E_C2J_h3 | 0,55 | 0,47 | 0,64 | 0,31 | 0,72 | 0,65 | 0,81 | 0,54 |
| E_C2_h3 | 0,42 | 0,30 | 0,58 | 0,41 | 0,55 | 0,45 | 0,71 | 0,60 |
| E_GDXTATIL_h1 | 0,53 | 0,35 | 0,74 | 0,41 | 0,56 | 0,37 | 0,75 | 0,60 |
| E_M_GDXJ_h1 | 0,45 | 0,35 | 0,55 | 0,31 | 0,62 | 0,52 | 0,71 | 0,54 |
| V_GDXJRES_h3 | 0,53 | 0,24 | 0,72 | 0,53 | 0,52 | 0,23 | 0,71 | 0,62 |
| V_LAST1H_h5 | 0,53 | 0,38 | 0,65 | 0,53 | 0,54 | 0,39 | 0,66 | 0,62 |
| V_LOWMOM_h1 | 1,03 | 0,85 | 1,34 | 0,53 | 1,03 | 0,85 | 1,35 | 0,62 |
| V_LOWMOM_h5 | 1,01 | 0,59 | 1,69 | 0,53 | 1,02 | 0,60 | 1,70 | 0,62 |
| V_QEND_h3 | 0,94 | 0,98 | 0,99 | 0,53 | 0,96 | 0,99 | 1,00 | 0,62 |

---

## 3. Örtüşme: kaç bağımsız sinyal var?

### 3.1 Pozisyon ve P&L korelasyonları

VİOP, ham günlük sinyal pozisyonları:

|   | V_LOWMOM_h1 | V_QEND_h3 | V_GDXJRES_h3 | V_LAST1H_h5 |
|---|---|---|---|---|
| V_LOWMOM_h1 | 1,00 | -0,03 | 0,01 | 0,04 |
| V_QEND_h3 | -0,03 | 1,00 | 0,01 | 0,02 |
| V_GDXJRES_h3 | 0,01 | 0,01 | 1,00 | 0,00 |
| V_LAST1H_h5 | 0,04 | 0,02 | 0,00 | 1,00 |

VİOP, net günlük P&L:

|   | V_LOWMOM_h1 | V_QEND_h3 | V_GDXJRES_h3 | V_LAST1H_h5 |
|---|---|---|---|---|
| V_LOWMOM_h1 | 1,00 | -0,01 | 0,02 | 0,11 |
| V_QEND_h3 | -0,01 | 1,00 | 0,00 | 0,05 |
| V_GDXJRES_h3 | 0,02 | 0,00 | 1,00 | -0,10 |
| V_LAST1H_h5 | 0,11 | 0,05 | -0,10 | 1,00 |

ETF, ham pozisyonlar:

|   | E_GDXTATIL_h1 | E_C2J_h3 | E_C2_h3 | E_C1_h5 | E_M_GDXJ_h1 |
|---|---|---|---|---|---|
| E_GDXTATIL_h1 | 1,00 | -0,00 | -0,03 | 0,01 | -0,01 |
| E_C2J_h3 | -0,00 | 1,00 | 0,29 | 0,14 | 0,01 |
| E_C2_h3 | -0,03 | 0,29 | 1,00 | 0,33 | -0,01 |
| E_C1_h5 | 0,01 | 0,14 | 0,33 | 1,00 | -0,02 |
| E_M_GDXJ_h1 | -0,01 | 0,01 | -0,01 | -0,02 | 1,00 |

ETF, net günlük P&L:

|   | E_GDXTATIL_h1 | E_C2J_h3 | E_C2_h3 | E_C1_h5 | E_M_GDXJ_h1 |
|---|---|---|---|---|---|
| E_GDXTATIL_h1 | 1,00 | 0,09 | 0,11 | 0,06 | 0,11 |
| E_C2J_h3 | 0,09 | 1,00 | 0,61 | 0,32 | 0,51 |
| E_C2_h3 | 0,11 | 0,61 | 1,00 | 0,46 | 0,34 |
| E_C1_h5 | 0,06 | 0,32 | 0,46 | 1,00 | 0,24 |
| E_M_GDXJ_h1 | 0,11 | 0,51 | 0,34 | 0,24 | 1,00 |

**P&L'den hesaplanan etkin bağımsız sayı** (özdeğerlerden, (Σλ)²/Σλ²): VİOP 3,95/4, ETF 3,42/5.

ETF P&L korelasyonu pozisyon korelasyonundan yüksek. Örnek: C2j ile E3-1 pozisyonda 0,01, P&L'de 0,51. Neden: ikisi de yalnız uzun GDXJ tutuyor; aynı gün açık olduklarında aynı betayı taşıyorlar. Bu sinyal örtüşmesi değil, ortak madenci betası.

### 3.2 Aynı fenomenin yüzleri mi?

| Soru | Ölçüm | Hüküm |
|---|---|---|
| LOWMOM ile trend | Aktif günlerde LOWMOM, 5 günlük TSMOM ile %100 aynı işaretli (tanım gereği). MA50 konumuyla %70 aynı. LOWMOM P&L'i, MA50 ve koşulsuz TSMOM5 P&L'leri kontrol edilince alfa yılda %7,2 (t 3,3; R² 0,20). | Koşullama işi yapıyor; LOWMOM trendin kopyası değil. Koşulsuz TSMOM5 ve MA kuralları VİOP döneminde drift çıkarılınca ≈0 (a1). Ama aynı aile: "sakin piyasada kısa vadeli trend". |
| VİOP madenci artığı (A4-C1) ile ETF madenci artığı (E2-C2j) | Aynı ABD kapanışından kurulan iki öngörücünün sıra korelasyonu 0,865. | **Aynı fenomen**, iki cephede işleniyor. Birini seçin ya da yarım ağırlık verin. |
| Madenci artığı ile altının giriş öncesi gece hareketi | A4-C1 z'si ile altının [t-1 20:00 → t 15:00 UTC] hareketi: 0,008. Bu hareket kontrol edilince fwd3 kısmi t 3,45. | Etki VİOP girişinden önce fiyatlanmıyor. Giriş sonrası bilgi taşıyor. |
| Madenci artığı (C2j) ile altın gün içi dönüşü (E3-1) | x ile m_t arasında 0,018; pozisyon korelasyonu 0,01. | **Farklı fenomenler.** Biri madencinin kendi artığının sürmesi, öteki altın hareketinden sonra madencinin ertesi gün geri dönmesi. |
| C2j, C2, C1 | Pozisyon korelasyonu 0,14–0,43; hepsi "madenci artığı" ailesi (k=1/3/10, hedef GDXJ/GDX/GLD). | **Tek aile.** C1 en yavaş ve altını hedefleyen yüzü. |
| Son saat (A8-3) ile E3-1 | Aynı gün altın 14→15 UTC ile m_t arasında 0,33. | Bilginin bir kısmı ortak (altının geç saat hareketi), ama farklı hedef ve yön: VİOP'ta 5 günlük devam, GDXJ'de 1 günlük ters. Kısmen bağımsız. |
| Çeyrek sonu (QEND) ile tatil öncesi GDX | 39 QEND olayının 17'si bir tatil öncesi GDX olayıyla ±3 gün içinde. | Kısmen aynı "dönem sonu / tatil öncesi altın kuvveti" takvim ailesi. E1 REP'e göre GLD de aynı günlerde +15 bps (t 2,0). |

**Sonuç: iki cephede yaklaşık 5 bağımsız fenomen var.**

| # | Fenomen | Sinyaller | Kanıt düzeyi |
|---|---|---|---|
| 1 | Sakin rejimde kısa vadeli momentum | LOWMOM | VİOP, DÜŞÜK; 2026'da pasif |
| 2 | Takvim: çeyrek sonu / tatil öncesi | QEND (VİOP), tatil öncesi GDX (ETF) | |
| 3 | Madenci artığı momentumu / öncülüğü | A4-C1, C2j, C2, C1 | ETF alan içi BH q 0,02–0,07 |
| 4 | Altın gün içi hareketinden sonra madencinin ertesi gün dönüşü | E3-1 | Bonferroni'yi geçen tek fenomen |
| 5 | Son saat momentumu | A8-3 | DÜŞÜK |

Tek başına çoklu test düzeltmesinden sağ çıkan yalnız 4 numara.

---

## 4. Önceden tanımlı eşit ağırlıklı birleşim

**Uyarı.** Ağırlıklar önceden tanımlı (eşit) olsa da sinyaller binlerce testten sonradan seçildi. ETF'de IS (2008–2017) bile analistlerin aile tasarlarken gördüğü veridir. Aşağıdaki sonuçlar seçim yanlılığı içerir ve **üst sınır** sayılmalı.

**Tanım.**
- **VİOP.** LOWMOM-h1, QEND-h3, A4-C1-h3 ve LAST1H-h5'in kademeli etkin pozisyonlarının ortalaması (her biri 1/4). Tek enstrümanda (F_XAUUSD) netleşiyor. Maliyet 5 bps gidiş-dönüş, stres 10 bps.
- **ETF.** Beş sinyalin her biri sermayenin 1/5'i: tatil öncesi GDX, C2j (GDXJ), C2 (GDX), C1 (GLD), E3-1 (GDXJ). Aynı ETF'deki sinyaller netleşiyor. Yalnız uzun. Maliyet 10 bps, stres 20 bps. Kıyas: GDX/GDXJ/GLD eşit ağırlıklı sepet. Alfa = sepete regresyonun sabiti.
- P&L basit getiriyle hesaplandı.
- VİOP'ta OOS (2022-01 → 2026-11) ile 2022+ aynı dönemdir. ETF'de IS 2008–2017, OOS 2018–2026.

| Cephe | Dönem | Maliyet | Net Sharpe | t | Yıllık % | Vol % | Maks. düşüş % | Ort. mutlak poz. | B&H Sharpe | B&H yıllık % | Alfa % (sepete göre) | Alfa t | Yarıya: Sharpe | Yarıya: yıllık % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VIOP | tam | temel | 1,33 | 4,13 | 4,23 | 3,18 | -4,30 | 0,19 | 0,57 | 8,99 | — | — | 0,66 | 2,12 |
| VIOP | tam | stres | 1,08 | 3,35 | 3,44 | 3,19 | -4,40 | 0,19 | 0,57 | 8,99 | — | — | 0,54 | 1,72 |
| VIOP | IS | temel | 1,06 | 2,33 | 3,03 | 2,85 | -3,20 | 0,21 | 0,54 | 7,02 | — | — | 0,53 | 1,52 |
| VIOP | IS | stres | 0,76 | 1,66 | 2,16 | 2,85 | -4,00 | 0,21 | 0,54 | 7,02 | — | — | 0,38 | 1,08 |
| VIOP | OOS | temel | 1,59 | 3,49 | 5,53 | 3,48 | -4,30 | 0,17 | 0,62 | 11,19 | — | — | 0,80 | 2,76 |
| VIOP | OOS | stres | 1,38 | 3,03 | 4,80 | 3,48 | -4,40 | 0,17 | 0,62 | 11,19 | — | — | 0,69 | 2,40 |
| VIOP | 2022+ | temel | 1,59 | 3,49 | 5,53 | 3,48 | -4,30 | 0,17 | 0,62 | 11,19 | — | — | 0,80 | 2,76 |
| VIOP | 2022+ | stres | 1,38 | 3,03 | 4,80 | 3,48 | -4,40 | 0,17 | 0,62 | 11,19 | — | — | 0,69 | 2,40 |
| VIOP | 2026 | temel | 1,78 | 1,62 | 8,75 | 4,93 | -4,30 | 0,14 | -0,51 | -14,94 | — | — | 0,89 | 4,38 |
| VIOP | 2026 | stres | 1,65 | 1,51 | 8,13 | 4,93 | -4,40 | 0,14 | -0,51 | -14,94 | — | — | 0,82 | 4,07 |
| ETF | tam | temel | 0,86 | 3,72 | 9,99 | 11,64 | -21,70 | 0,25 | 0,34 | 11,09 | 6,85 | 4,48 | 0,43 | 5,00 |
| ETF | tam | stres | 0,69 | 2,99 | 8,02 | 11,64 | -25,80 | 0,25 | 0,34 | 11,09 | 4,73 | 3,10 | 0,34 | 4,01 |
| ETF | IS | temel | 0,72 | 2,28 | 8,50 | 11,79 | -21,70 | 0,25 | 0,02 | 0,78 | 8,59 | 3,80 | 0,36 | 4,25 |
| ETF | IS | stres | 0,57 | 1,79 | 6,68 | 11,79 | -25,80 | 0,25 | 0,02 | 0,78 | 6,48 | 2,88 | 0,28 | 3,34 |
| ETF | OOS | temel | 1,02 | 3,03 | 11,68 | 11,46 | -13,10 | 0,25 | 0,64 | 20,58 | 5,61 | 2,70 | 0,51 | 5,84 |
| ETF | OOS | stres | 0,83 | 2,48 | 9,55 | 11,46 | -13,10 | 0,25 | 0,64 | 20,58 | 3,48 | 1,68 | 0,42 | 4,78 |
| ETF | 2022+ | temel | 1,09 | 2,38 | 12,74 | 11,73 | -12,10 | 0,26 | 0,79 | 25,97 | 4,84 | 1,62 | 0,55 | 6,37 |
| ETF | 2022+ | stres | 0,90 | 1,98 | 10,57 | 11,73 | -13,10 | 0,26 | 0,79 | 25,97 | 2,67 | 0,90 | 0,45 | 5,28 |
| ETF | 2026 | temel | 0,66 | 0,61 | 11,67 | 17,68 | -12,10 | 0,30 | 0,18 | 8,16 | 8,90 | 0,86 | 0,33 | 5,84 |
| ETF | 2026 | stres | 0,54 | 0,49 | 9,48 | 17,67 | -13,00 | 0,30 | 0,18 | 8,16 | 6,71 | 0,65 | 0,27 | 4,74 |

Yukarıdaki "Yıllık %" sütunu yıllıklandırılmış ortalamadır (2026 için Ocak–Kasım ortalamasının yıllığa çevrilmiş hali). Takvim yılı toplamı (%, 1x):

| Yıl | VIOP_birlesim_% | VIOP_BH_% | ETF_birlesim_% |
|---|---|---|---|
| 2.008 | — | — | 6,40 |
| 2.009 | — | — | 8,20 |
| 2.010 | — | — | 14,80 |
| 2.011 | — | — | 4,40 |
| 2.012 | — | — | -3,10 |
| 2.013 | — | — | -7,80 |
| 2.014 | — | — | 7,40 |
| 2.015 | — | — | 12,60 |
| 2.016 | — | — | 19,90 |
| 2.017 | 4,10 | 4,90 | 21,90 |
| 2.018 | -1,60 | -3,70 | 9,50 |
| 2.019 | 2,90 | 14,60 | 10,00 |
| 2.020 | 6,00 | 22,30 | 22,90 |
| 2.021 | 3,10 | -4,10 | -0,50 |
| 2.022 | 3,30 | -3,60 | 7,80 |
| 2.023 | 5,90 | 5,00 | 2,60 |
| 2.024 | 1,70 | 17,10 | 11,40 |
| 2.025 | 7,90 | 46,60 | 29,90 |
| 2.026 | 7,40 | -12,30 | 9,70 |

**Okuma.**
- **VİOP.**
  - Birleşimin Sharpe'ı yüksek çünkü dört bileşen birbirine neredeyse dik (P&L |ρ| ≤ 0,12).
  - Ama ortalama maruziyet %19. 1x nominalde yıllık getiri yalnız %4,2, en büyük düşüş %4,3.
  - 10 yılın 9'unda pozitif; yalnız 2018 −%2,6.
  - 2026'nın +%7,4'ünün çoğu son saat sinyalinden geliyor; LOWMOM 2026'da hiç aktif değil.
- **ETF.**
  - Sepete göre alfa: tam dönem yılda %6,9 (t 4,5), OOS %5,6 (t 2,7), 2022+ %4,8 (t 1,6), 2026 %8,9 (t 0,9).
  - Alfa son yıllarda anlamlılığını kaybediyor.
  - 20 bps stres maliyette OOS alfa %3,5 (t 1,7).
  - En büyük düşüş −%21,7 (IS); 2013 −%7,8.
- **"Yarıya indir" kuralıyla gerçekçi beklenti.** Ölçülen büyüklüğün yarısı alındı.

  | Cephe | Sharpe | Yıllık getiri | Not |
  |---|---|---|---|
  | VİOP | 0,66 (tam) – 0,80 (OOS) | %2,1–2,8 (1x) | Nominal 3×'e çıkarılırsa ≈ %6–8, vol ≈ %10, beklenen en büyük düşüş ≈ %13 |
  | ETF | 0,43–0,55 | ≈ %5–6 | Bu getiri beta içeriyor |

  ETF'de yalnız alfa yarıya indirilirse OOS'ta yılda ≈ %2,8 kalıyor. Sepet betası 0,30.

  Bu beklentiler perakende maliyetlerini (Midas kur makası, 1,5 USD/emir; VİOP komisyon + BSMV) temel senaryodaki kadar varsayıyor. Küçük hesapta ETF tarafı daha da kötüleşir.

---

## 5. Bugünkü durum: Pazartesi 2026-11-09

Veri 2026-11-06 Cuma kapanışına kadar. Kod: `s05_bugun.py`, çıktı `bugun_2026_11_09.json`.

| Sinyal | Durum | Yön / büyüklük | Eksik veri |
|---|---|---|---|
| V LOWMOM (h1/h5) | **PASİF** | rv20 (spot 15:00 UTC) %21,0. 2010'dan beri yüzdeliği 0,88 (eşik 1/3 ≈ %11,7). 2026'da hiç tetiklenmedi; 2026'nın en düşük rv20'si %14,9. Son 5 günlük spot +%3,3; rejim olsaydı uzun olurdu. | Pazartesi 15:00 UTC spot. Rejimin değişmesi için oynaklığın yarıya inmesi gerekir. |
| V QEND (h3) | **PASİF** | Bir sonraki giriş: 2026-12-30 Çarşamba uzlaşması (Aralık'ın sondan 2. VİOP günü; 31 Aralık işlem günü varsayımıyla). Çıkış ≈ 2027-01-05. | Yok (takvim) |
| V A4-C1 GDXJ artığı (h3) | **AKTİF, yeni dilim UZUN** | Cuma GDXJ +%2,78, GLD −%0,79, β60 2,02 → z = +2,84 (>0,43). Açık dilimler: Perşembe +1, Cuma −1. Pazartesi uzlaşmasından sonra etkin pozisyon +1/3 birim. | Yok (Cuma ABD kapanışı biliniyor) |
| V LAST1H son saat (h5) | **KOŞULLU** | Pazartesi ln(spot15/spot14) > 0 ise yeni 1/5 dilim uzun, < 0 ise kısa. Açık dilimler (Salı −1, Çarşamba −1, Perşembe −1, Cuma +1) toplamı −2/5. Pazartesi sonrası etkin pozisyon −0,2 (uzun dilimle) ya da −0,6 (kısa dilimle). | Pazartesi 14:00 ve 15:00 UTC spot |
| **VİOP birleşimi (1/4'er)** | ≈ **DÜZ** | (0 + 0 + 0,333 + {−0,2 / −0,6}) / 4 = **+0,03 ya da −0,07 birim** | Pazartesi 14–15 UTC |
| E tatil öncesi GDX (h1) | **PASİF** | Bir sonraki olay 2026-11-25 (Şükran Günü öncesi). Giriş 2026-11-24 Salı kapanışı, çıkış 25 Kasım kapanışı. | Yok |
| E C2j GDXJ artığı (h3) | **AKTİF UZUN** | x = Cuma artığı +%3,67 (eşik +%0,67). Üç dilimin üçü uzun → GDXJ kolu tam dolu. | Yok |
| E C2 GDX 3 günlük artık (h3) | **AKTİF UZUN** | x = +%9,49 (eşik +%0,81) → GDX kolu tam dolu. | Yok |
| E C1 GDX 10 günlük artık → GLD (h5) | **AKTİF UZUN** | x = +%9,65 (eşik +%2,52). Cuma ve Pazartesi dilimleri uzun → GLD kolu 0,4. | Yok |
| E E3-1 altın gün içi → GDXJ (h1) | **KOŞULLU** | Pazartesi 15:00 ET'de spot altın < Cuma 16:00 ET fiyatı **4.065,68 USD** ise GDXJ'yi kapanışta al, Salı kapanışında sat. Değilse nakit. Cuma pozisyonu uzundu (m = −%0,87); Pazartesi kapanışında kapanır ya da koşul sürerse korunur. | Pazartesi 15:00 ET (20:00 UTC) spot altın |
| **ETF birleşimi (1/5'er)** | **UZUN** | GDX %20, GDXJ %20 (E3-1 tetiklenirse %40), GLD %8. Sermayenin %48–68'i uzun. | Pazartesi 15:00 ET altın |

**ETF uyarısı.** Sinyallerin hepsinin "madenci uzun" çıkmasının nedeni geçen haftaki sert madenci yükselişi: 4 Kasım'da GDXJ +%9,2, GLD +%3,6. Bu sinyallerin 2026 performansı zayıf:
- C2j 2026 Sharpe 0,21.
- C2 0,23.
- C2j'nin 2025–26 IC'si 0,03 (t 0,6).

GDXJ'nin 2026 yıllık oynaklığı %59.

### 2026 oynaklık rejiminde hangi sinyaller pasif ya da zayıf?

2026'da gerçekleşen yıllık oynaklık: VİOP %29,2, GLD %30,4, GDXJ %58,9. 2017–2026 VİOP ortalaması %15,8.

| Sinyal | Sharpe rv20<%18 | Sharpe rv20≥%18 | aktif gün rv<%18 | aktif gün rv≥%18 | Aktif gün payı (tüm) | Aktif gün payı 2026 | 2026 net % (1x) |
|---|---|---|---|---|---|---|---|
| E_C1_h5 | 0,94 | 0,49 | 1.087 | 405 | 0,19 | 0,33 | 13,23 |
| E_C1kap_h5 | 0,78 | 0,65 | 3.153 | 809 | 0,82 | 0,77 | 14,61 |
| E_C2J_h3 | 0,71 | 0,79 | 2.112 | 596 | 0,26 | 0,31 | 7,63 |
| E_C2_h3 | 0,66 | 0,24 | 1.703 | 509 | 0,30 | 0,33 | 7,26 |
| E_GDXTATIL_h1 | 0,53 | 0,94 | 117 | 35 | 0,04 | 0,03 | 2,62 |
| E_M_GDXJ_h1 | 0,49 | 0,89 | 1.544 | 433 | 0,47 | 0,50 | 16,84 |
| V_GDXJRES_h3 | 0,45 | 0,79 | 1.351 | 302 | 0,57 | 0,58 | 7,55 |
| V_LAST1H_h5 | 0,36 | 1,09 | 1.943 | 419 | 0,98 | 0,98 | 18,73 |
| V_LOWMOM_h1 | 1,14 | — | 981 | 0 | 0,40 | 0,00 | 0,00 |
| V_LOWMOM_h5 | 1,11 | — | 1.103 | 4 | 0,40 | 0,00 | 0,00 |
| V_QEND_h3 | 1,06 | — | 98 | 19 | 0,02 | 0,01 | 2,48 |

- **Yapısal olarak pasif:** LOWMOM. Yalnız rv20 < ≈%11,7 iken çalışıyor; 2026'da sıfır gün aktif. Yüksek oynaklık diliminde (rv20 ≥ %18) h1'de hiç, h5'te 4 aktif günü var.
- **Yüksek oynaklıkta zayıflayan:** C2 (Sharpe 0,24) ve C1 (0,49).
- **Yüksek oynaklıkta iyi görünen:** E3-1 (0,89), tatil öncesi GDX (0,94), son saat (1,09), A4-C1 (0,79), C2j (0,79). Ama yüksek oynaklık dilimi yalnız 434 VİOP / 878 ETF günü ve büyük ölçüde 2020 ile 2026'dan oluşuyor; bu farklar gürültü sınırında.
- **Takvim sinyalleri:** QEND ve tatil öncesi rejimden bağımsız, ama yılda 4 ve 9 işlem.

---

## 6. Literatür ile veri karşılaştırması

Kaynaklar: `research/r2_kisa_vade_strateji.md`, `r5_leadlag_literatur.md`, `m2_etf_strateji.md`.

### 6.1 Literatürde iddia edilip bizde tutmayanlar

| İddia (kaynak) | Bizim veri |
|---|---|
| Zaman serisi momentumu ve trend (MA, Donchian, 52 hafta, TSMOM; Moskowitz ve diğ., CTA'lar) | Altında 1–5 günde drift çıkarılınca ≈0 (TSMOM_60 0,31, MA50 0,34; yıl ortalaması çıkarınca 0,03). Yalnız sakin rejime koşullanınca iz var (LOWMOM). |
| Kısa vadeli dönüş, RSI(2)/Connors, Bollinger (perakende ve pratisyen) | Ters işaretli: drift çıkarılmış Sharpe −0,4 ile −0,67, yılların 9/10'unda zarar. Dip alma işe yaramıyor. |
| >2σ günden sonra ertesi gün hafif dönüş (Caporale–Plastun; anlamsız) | Dönüş yok, hafif devam: 2σ düşüşten sonra ertesi gün VİOP −8,5 bps, GLD −13,5, GDXJ −72 bps (t −2,0). Koşulsuz ortalama +1..+3 bps. |
| Pazartesi zayıf (Lucey–Tully), Eylül/Kasım (Baur), Ocak (WGC), festival talebi (Diwali, Akshaya, Çin Yeni Yılı), Ramazan | Hiçbiri tutmuyor. Ocak ve Bayram sonrası ADV'de çürüdü; Bayram sonrasında kod hatası da var. |
| Gece pozitif, gündüz negatif (Blose–Gondhalekar) ve "Asya alır, NY satar" | Gece sürüklenmesi var (20:00→00:00 UTC +3 bps/gün, t 6,6). Ama kapanıştan kapanışa işlemle yakalanamıyor; akşam→sabah kuralı maliyetten sonra ≈0. Asya/Londra asimetrisi 2017 sonrası yok. GLD'nin gün içi açığı yalnız OOS'ta ve ılımlı; madencilerde güçlü ama CO stratejisi 10 bps'te negatif. |
| FOMC öncesi sürüklenme (Lucca–Moench, hisse senedi) | Altında yok (mutlak t ≤ 1,2). FOMC günü ve sonrası da yok. |
| COT uçları karşıt sinyal, ETF akışları, Google Trends | Yok. Akış ve konum fiyatı izliyor (ters yön t 12). Literatürdeki "akış fiyatı takip eder" bulgusuyla uyumlu. |
| Şanghay primi "mütevazı öngörücü" (Meader) | 1–5 günde yok (en iyi mutlak t 1,99, IS'te ters). |
| Altın/gümüş oranı ortalamaya dönüş | Yok; IS ve OOS işaretleri ters. |
| Dolar, reel faiz, hisse, petrol, BTC gecikmeli öngörü | Yok. Literatür (Ferraro–Rogoff–Rossi) zaten günlük gecikmeli öngörünün geçici olduğunu söylüyor. Bizde ABD kapanış bilgisi VİOP girişine kadar geçen 18 saatte fiyatlanıyor (dolar emilim tanısı). Uyumlu. |
| Kaldıraçlı ETF dengeleme akışı → ertesi gün kısmi dönüş (Tuzun, Barbon ve diğ.) | Kısmen. Bizde "altın gün içi → GDXJ ertesi gün ters" var (E3-1), GDX'te NUGT sonrası güçleniyor (IC −0,016 → −0,060). ADV'ye göre mekanizma dengeleme saatiyle tam örtüşmüyor; ekonomik etki küçük. |
| LBMA fiks sızıntısı (Caminschi–Heaney) | Bugünkü elektronik fikste iz yok; kış fiks öncesi saat çürüdü. |
| Haberlere hızlı tepki (Elder ve diğ.) / aşırı tepki → dönüş (Smales) | NFP günü 12→15 UTC hareketi ertesi güne sürüyor (devam), ama yalnız 2022–26'da. DÜŞÜK. |

### 6.2 Bizde bulunup literatürde olmayanlar (ya da literatürün tersi)

| Bulgu | Literatür | Not |
|---|---|---|
| Madenci artığı → altın (E2-C1: GDX'in 10 günlük artığı → GLD 5 gün; A4-C1: GDXJ artığı → VİOP 3 gün) | Tersini söylüyor: altın madencilere öncülük eder (Lucey–O'Connor 2017). Kısa ufukta madenciyi altın dışı faktörler belirler. | ETF alan içi q 0,019 (C1) ve VİOP q 0,29 (A4-C1). Yön literatüre ters, kanıt orta–zayıf. Kazanç yüksek oynaklık dönemlerine yığılı (2013–17, 2025–26). |
| Madenci artığı momentumu (C2j/C2: GDXJ/GDX'in altın+SPY'den arındırılmış artığı 3 gün sürüyor) | Endüstri içi yavaş yayılım (Hou 2007) genel olarak var; ETF'e özgü çalışma yok. | q 0,056–0,069. |
| Altının 15:00 ET'ye kadarki hareketi → GDXJ ertesi gün ters (E3-1) | LETF dengeleme literatürü yakın ama bu biçimde bulunamadı. | Projede Bonferroni'yi geçen tek ilişki. Net alfa anlamsız. |
| Sakin rejimde 5 günlük momentum (LOWMOM) | Oynaklık yönetimli momentum hisse ve aylık ufukta var (Barroso–Santa-Clara, Moreira–Muir). Altında 1–5 günlük koşullu sürümü bulunamadı. | Erken dönemde (2010–16) aynı işaret (0,51–0,58). |
| Çeyrek sonu (sondan 2. gün → yeni çeyreğin 2. günü) altın kuvveti | Yalnız pratisyen iddiası; hakemli çalışma yok. Hisselerde tatil öncesi etkisi (Ariel 1990) var. | Tatil öncesi madenci etkisiyle kısmen aynı aile. |
| Platin 5 günlük hareketi → GDX ters (q 0,011) | Yok. | Mekanizma yok; IS verisi kirli (PL=F 2008–09); DÜŞÜK. |
| Gram altın sentetik priminin güçlü ortalamaya dönüşü (t −6,1) | Türkiye'ye özgü; yok. | 3 bacak maliyetiyle net zarar. Yalnız araç seçimine bilgi verir: prim yüksekse gram yerine ons al. |
| GLDTR (BIST BYF) priminin gram altına göre dönüşü | Yok. | Veri kusurlu (kış barları eksik). DÜŞÜK, cephe dışı. |

**Genel uyum.** Literatürün ana mesajı bizde de tutuyor. Günlük kapanıştan kapanışa altında güçlü bir gecikmeli öngörücü yok. Gerçekçi |IC| 0,03–0,07 bandında. Senkronsuzluk sahte öncülük üretiyor (r5'te 0,19–0,42). Bulduğumuz izler küçük, rejime bağlı ve çoğunlukla madenci ETF'leri tarafında.

---

## 7. Risk ve boyut

### 7.1 VaR ve ES

Basit getiri; tarihsel değerler örtüşen h günlük pencerelerden. "Normal" sütunu 2,326·σ·√h.

| Araç | Dönem | h | Yıllık vol % | VaR95 % | VaR99 % | ES97,5 % | VaR99 normal % | En kötü % |
|---|---|---|---|---|---|---|---|---|
| VIOP_F_XAUUSD | 2026 | 1 | 29,20 | 2,97 | 5,01 | 5,36 | 4,29 | 7,80 |
| VIOP_F_XAUUSD | 2026 | 3 | 29,20 | 4,32 | 10,12 | 8,96 | 7,42 | 11,61 |
| VIOP_F_XAUUSD | 2026 | 5 | 29,20 | 6,55 | 11,80 | 10,61 | 9,58 | 12,87 |
| VIOP_F_XAUUSD | 2017-2026 | 1 | 15,80 | 1,52 | 2,85 | 3,03 | 2,32 | 7,80 |
| VIOP_F_XAUUSD | 2017-2026 | 3 | 15,80 | 2,61 | 4,41 | 4,81 | 4,02 | 11,61 |
| VIOP_F_XAUUSD | 2017-2026 | 5 | 15,80 | 3,25 | 5,44 | 6,06 | 5,19 | 12,87 |
| GLD | 2026 | 1 | 30,40 | 3,19 | 4,14 | 5,16 | 4,46 | 10,27 |
| GLD | 2026 | 3 | 30,40 | 4,92 | 9,07 | 9,18 | 7,72 | 13,63 |
| GLD | 2026 | 5 | 30,40 | 6,52 | 10,84 | 10,39 | 9,96 | 12,25 |
| GLD | 2017-2026 | 1 | 16,70 | 1,62 | 3,05 | 3,14 | 2,45 | 10,27 |
| GLD | 2017-2026 | 3 | 16,70 | 2,59 | 4,60 | 5,01 | 4,24 | 13,63 |
| GLD | 2017-2026 | 5 | 16,70 | 3,37 | 5,92 | 6,13 | 5,47 | 12,25 |
| GDX | 2026 | 1 | 53,00 | 5,52 | 8,56 | 8,48 | 7,77 | 12,76 |
| GDX | 2026 | 3 | 53,00 | 9,51 | 13,63 | 13,21 | 13,46 | 16,02 |
| GDX | 2026 | 5 | 53,00 | 11,94 | 14,36 | 14,40 | 17,38 | 16,52 |
| GDX | 2017-2026 | 1 | 37,60 | 3,48 | 5,96 | 6,49 | 5,51 | 22,82 |
| GDX | 2017-2026 | 3 | 37,60 | 5,72 | 9,56 | 10,28 | 9,54 | 30,88 |
| GDX | 2017-2026 | 5 | 37,60 | 7,24 | 12,06 | 12,42 | 12,31 | 35,40 |
| GDXJ | 2026 | 1 | 58,90 | 6,07 | 8,88 | 9,30 | 8,63 | 13,63 |
| GDXJ | 2026 | 3 | 58,90 | 10,39 | 15,56 | 14,75 | 14,95 | 17,51 |
| GDXJ | 2026 | 5 | 58,90 | 13,71 | 15,68 | 15,85 | 19,30 | 17,19 |
| GDXJ | 2017-2026 | 1 | 44,20 | 4,04 | 6,97 | 7,55 | 6,47 | 26,27 |
| GDXJ | 2017-2026 | 3 | 44,20 | 6,45 | 10,94 | 12,16 | 11,21 | 40,72 |
| GDXJ | 2017-2026 | 5 | 44,20 | 8,10 | 13,53 | 14,50 | 14,47 | 44,74 |
| NUGT | 2026 | 1 | 106 | 11,00 | 16,91 | 16,86 | 15,49 | 25,24 |
| NUGT | 2026 | 3 | 106 | 18,74 | 26,91 | 25,59 | 26,84 | 30,98 |
| NUGT | 2026 | 5 | 106 | 23,79 | 27,44 | 27,69 | 34,65 | 30,95 |
| NUGT | 2017-2026 | 1 | 86,90 | 7,54 | 13,45 | 14,92 | 12,74 | 49,34 |
| NUGT | 2017-2026 | 3 | 86,90 | 12,63 | 20,34 | 23,81 | 22,06 | 73,73 |
| NUGT | 2017-2026 | 5 | 86,90 | 16,42 | 25,21 | 28,88 | 28,48 | 79,07 |

- **2026 rejimi** (VİOP yıllık vol %29). Parametrik VaR99: 1 gün %4,25, 3 gün %7,4, 5 gün %9,5. Tarihsel değerler daha kalın kuyruklu: 1 gün %5,0, 3 gün %10,1, 5 gün %11,8.
- **2017–2026 ortalaması** bunun yaklaşık yarısı: 1 gün %2,85, 5 gün %5,4. 2026'yı ortalama dönemin VaR'ıyla boyutlandırmak riski yarıya düşük gösterir.
- **ETF tarafı çok daha riskli.** 2026'da 5 günlük VaR99: GDX %14,4, GDXJ %15,7, NUGT %27,4. NUGT'nin 2017–26'daki en kötü 5 günü −%79.

### 7.2 ±%10 fiyat limiti ve teminat (VİOP)

**Fiyat limiti** (baz = önceki uzlaşma, ±%10):
- 2017–2026'da hiçbir VİOP günü %9'u aşmadı.
- En büyük düşüş −%7,8 (2026-01-30), en büyük yükseliş +%5,6 (2020-03-24).
- |getiri| > %5 olan 5 günün 4'ü 2026'da. |getiri| > %3 olan 38 günün 22'si 2026'da.
- Spot 2010–2026'da 15:00→15:00 bazında %9'u aşan tek gün var (2013-04-15, −%9,3).
- Limit günlük hareketi keser, ama riski kesmez. Limitte kilitlenen bir gün ertesi güne taşınır. Asıl risk birkaç günlük toplam: 2026'nın en kötü 3 günü −%11,6.

**Teminat.**
- Takasbank PSR %10 → 1 sözleşme (1 ons) ≈ 408 USD ≈ 20,4 bin TL (06.11.2026). Bazı aracı kurumlar %20 istiyor (r1).

| Nominal/özsermaye | Teminatın özsermayeye oranı % | 1g VaR99 kayıp % (2026) | 5g VaR99 kayıp % (2026) | En kötü 5g % (2026) | 5g VaR99 % (2017-26) |
|---|---|---|---|---|---|
| 1 | 10 | 5,00 | 11,80 | 12,90 | 5,40 |
| 2 | 20 | 10,00 | 23,60 | 25,70 | 10,90 |
| 3 | 30 | 15,00 | 35,40 | 38,60 | 16,30 |
| 5 | 50 | 25,00 | 59,00 | 64,40 | 27,20 |
| 10 | 100 | 50,10 | 118 | 129 | 54,40 |

- Nominal/özsermaye 10 (yalnız teminat kadar para) olursa 2026'nın tipik kötü 5 günü (VaR99 %11,8) özsermayenin tamamından fazlasını götürür.
- 5× nominalde kötü bir hafta özsermayenin %59'u eder.
- **Öneri: nominal ≤ 2× özsermaye** (5 günlük VaR99 ≈ %24). Bunun üstü ancak rejim sakinleşirse (rv20 < %15). Hesabın kalanı TL nakitte; teminatın en az %50'si TL olmalı (QNB kuralı).
- Birleşik VİOP sinyali ortalama 0,19 birim pozisyon taşıyor. 2× nominal tavanla günlük ortalama nominal ≈ 0,4× özsermaye olur.

### 7.3 Stop kullanımı: veri ne diyor?

2σ günlerden sonraki getiri (bps). 2σ = önceki 20 günün oynaklığıyla:

| Seri | 2σ düşüş sonrası 1g (bps) | t | 2σ düşüş sonrası 5g | 2σ yükseliş sonrası 1g | 2σ yükseliş sonrası 5g | Koşulsuz 1g | Koşulsuz 5g | 2σ düşüş sayısı |
|---|---|---|---|---|---|---|---|---|
| VIOP_2017_2026 | -8,50 | -0,66 | 22,30 | 15,30 | 25,50 | 3,10 | 15,50 | 93 |
| spot_2010_2026 | -9,50 | -0,81 | -4,20 | 5,30 | 12,50 | 3,00 | 14,60 | 158 |
| spot_2010_2016 | -24,00 | -1,16 | -44,00 | -2,50 | -10,80 | 0,20 | 0,30 | 70 |
| GLD_2008_2026 | -13,50 | -1,37 | 5,50 | 6,50 | 33,40 | 3,10 | 15,40 | 182 |
| GDX_2008_2026 | -33,70 | -1,19 | -5,70 | 28,00 | 71,10 | 1,50 | 6,80 | 166 |
| GDXJ_2010_2026 | -72,50 | -1,97 | -27,60 | 4,20 | 70,20 | 1,00 | 3,80 | 146 |

Uzun pozisyonda "2σ düşüş gününden sonra k gün nakitte bekle" kuralı:

| Araç | 2σ düşüşten sonra nakit gün | Stoplu Sharpe | B&H Sharpe | Stoplu yıllık % | B&H yıllık % | Fark (yüzde puan) | Nakitte gün payı |
|---|---|---|---|---|---|---|---|
| VIOP | 1 | 0,60 | 0,57 | 9,27 | 8,99 | 0,28 | 0,04 |
| VIOP | 3 | 0,64 | 0,57 | 9,30 | 8,99 | 0,31 | 0,11 |
| VIOP | 5 | 0,50 | 0,57 | 6,97 | 8,99 | -2,02 | 0,18 |
| spot2010 | 1 | 0,59 | 0,54 | 9,08 | 8,75 | 0,33 | 0,04 |
| spot2010 | 3 | 0,63 | 0,54 | 9,36 | 8,75 | 0,61 | 0,10 |
| spot2010 | 5 | 0,61 | 0,54 | 8,83 | 8,75 | 0,08 | 0,17 |
| GLD | 1 | 0,55 | 0,52 | 9,81 | 9,49 | 0,32 | 0,04 |
| GLD | 3 | 0,52 | 0,52 | 8,81 | 9,49 | -0,68 | 0,11 |
| GLD | 5 | 0,55 | 0,52 | 9,04 | 9,49 | -0,45 | 0,17 |
| GDX | 1 | 0,35 | 0,30 | 14,02 | 12,45 | 1,57 | 0,04 |
| GDX | 3 | 0,41 | 0,30 | 15,78 | 12,45 | 3,33 | 0,10 |
| GDX | 5 | 0,30 | 0,30 | 11,15 | 12,45 | -1,30 | 0,15 |
| GDXJ | 1 | 0,40 | 0,29 | 17,81 | 13,17 | 4,64 | 0,03 |
| GDXJ | 3 | 0,39 | 0,29 | 16,20 | 13,17 | 3,03 | 0,09 |
| GDXJ | 5 | 0,33 | 0,29 | 12,95 | 13,17 | -0,22 | 0,15 |

Aktif sinyal içinde "dünkü pozisyona karşı 2σ hareket olursa pozisyonu kapat" kuralı:

| Sinyal | Stopsuz Sharpe | Stoplu Sharpe | Stopsuz yıllık % | Stoplu yıllık % | Stop günü |
|---|---|---|---|---|---|
| V_LOWMOM_h1 | 1,03 | 1,02 | 7,19 | 7,07 | 38 |
| V_GDXJRES_h3 | 0,52 | 0,47 | 3,93 | 3,30 | 62 |
| V_LAST1H_h5 | 0,54 | 0,61 | 3,89 | 4,32 | 84 |

**Okuma.**
1. **2σ dönüş kuralları zarar ettiriyor** (A1-REV-NEG). Bollinger dönüşü −0,67, 2σ ters işlem −0,58, RSI2 −0,38, Connors −0,40. Üç dönemde de negatif. Büyük düşüşten sonra ertesi gün ortalaması koşulsuz ortalamanın altında; GDXJ'de −72 bps (t −2,0). **Ortalama düşürmeyin, düşüşü "dip" diye almayın.**
2. **Kısa stop (2σ düşüşten sonra 1 gün nakit) maliyetsiz ya da hafif yararlı.**
   - VİOP Sharpe 0,60, B&H 0,57.
   - GDXJ'de 0,40'a karşı 0,29.
   - Uzun bekleme (5 gün nakit) VİOP'ta yılda −2 puan getiri kaybettiriyor.
3. **Sinyal içi stoplar karışık:** LOWMOM 1,03 → 1,02, A4-C1 0,52 → 0,47, son saat 0,54 → 0,61. Stop bir alfa kaynağı değil.
4. **Pratik kural.**
   - Asıl risk aracı pozisyon büyüklüğü (§7.2).
   - Felaket stopu kullanın: 2026 rejiminde 3σ ≈ %5,5 ters hareket, ya da teminatın %50'si. Amaç marjin çağrısını ve limit kilidini önlemek; getiri artırmak değil.
   - Akşam seansında stop/piyasa emri kullanılamıyor (r1). Midas'ta "zarar durdur" yalnız normal seansta çalışıyor (m2).

---

## 8. Sınırlamalar ve açık riskler

- **Seçim yanlılığı.** VİOP'ta 2.621, ETF'te 2.130 birincil test yapıldı. Ayakta kalanlar en iyilerin içinden seçildi. ETF'de bile çoklu testi geçen yalnız bir fenomen var (E3-1) ve onun net alfası anlamsız. Birleşim sonuçları üst sınırdır.
- **OOS'un saflığı.** Birçok aday tam örneklem t'siyle seçildi (A4-C1, E2 aileleri, NFP, Çin). REP ve ADV bu adaylarda "OOS gerçek dışarıda bırakılmış örneklem değil" uyarısı yaptı. **Gerçek doğrulama ancak bundan sonraki canlı veriyle olur.** Önerim: sinyalleri en az 6 ay kâğıt üzerinde ya da çok küçük boyutla izlemek.
- **Rejim yığılması.** Kazançların önemli bir kısmı 2020, 2024–26 boğa ve çöküş dönemlerinde. 2017–19 ve 2022–23 sakin dönemlerinde çoğu sinyal sıfır civarında.
- **Midas'ta doğrulanmayanlar.** Bunlar, ETF tarafının işlenebilirliğini belirsiz bırakıyor:
  - TL→USD kur makası.
  - MOC emri.
  - Kaldıraçlı/ters ETF ve PHYS listelemesi.
  - SEC/FINRA ücretleri.
  - Satış tutarının T+1'de kullanılabilmesi. Bu, h=1 kuralını nakit hesapta her gün çeviremeyebilir.
- **Vergi.** Vergi sonrası farklar ETF aleyhine: VİOP %10 stopaj; ABD ETF kazancı kur farkı dahil artan oranlı beyan (m2).
- **Veri.** GPR panel sütunları sabitti; a6 ham dosyayı kullandı. PL=F 2008–09 kirli. BIST saatlik barları eksik. Dukascopy Ekim–Kasım 2026 dakikadan yamalı.

---

## 9. Dosyalar

`/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/sentez/`:

| Dosya | İçerik |
|---|---|
| `HAKEM.md` | Bu rapor |
| `sinyal_tablosu.csv` | 65 iddia; analist/REP/ADV/SON güven, kural, etki, hakem yeniden hesap sütunları |
| `fdr_siniflandirma.csv` | 7.446 testin sınıfı, alanı ve alan içi q/Bonferroni değerleri |
| `fdr_ozet.csv`, `fdr_gecenler.csv` | FDR özeti ve q<0,10 / Bonferroni geçen testler |
| `dogrulama.csv`, `islem_basi.csv`, `alfa_bh.csv` | Ayakta kalanların dönem bazında yeniden hesabı (log ve basit), işlem başı etki, B&H'ye göre alfa |
| `korelasyon_*.csv`, `s04_sonuc.json` | Pozisyon ve P&L korelasyonları, fenomen testleri |
| `birlesim.csv`, `birlesim_yillik.csv` | Eşit ağırlıklı birleşim |
| `rejim.csv`, `rejim_iki_dilim.csv`, `etkinlik_2026.csv` | Oynaklık rejimi ve 2026 etkinliği |
| `bugun_2026_11_09.json` | Pazartesi sinyal durumu |
| `risk_var.csv`, `risk_teminat.csv`, `risk_stop.csv`, `risk_stop_sinyal.csv`, `risk_ozet.json` | Risk |
| `poz_*.parquet`, `pnl_*.parquet`, `sinyal_*_ham.parquet` | Sinyal pozisyonları ve P&L serileri |
| `s01_fdr.py` … `s07_rapor.py`, `sl.py` | Kod. Sıra: s01, s03, s04, s05, s06, s02, s07 |
