# v_YG1_a — Bağımsız doğrulama: YG1 (47 hissede açılış gap fade, CIMSA/OYAKC, hisseye özgü hedge'li fade)
Tarih: 02.11.2026 · Doğrulayıcı: v_YG1_a · Kod: `out/code_v_YG1_a/` (vc.py ortak; v1…v8; çıktılar `res/`). ll.py import EDİLMEDİ; temizlik/hizalama `vc.py`'de yeniden yazıldı.
Çalıştırma: `cd out/code_v_YG1_a && nice -n 10 python3 v1_daily.py` → v2_entry → v3_idio → v4_ssf → v5_costs → v6_cimsa → v7_checks → v8_idio_up (v2+ v1'in `res/v1_liq.csv` çıktısını okur).

## 0. Hüküm: DÜZELT
Başlık rakamları **ham veriden büyük ölçüde yeniden üretildi**: hisse medyanı OOS 18,4 bps (iddia 17,8), %87 pozitif, portföy OOS 16,7 bps (t 2,79), illikit/likit 26,9 / 2,2, CIMSA/OYAKC OOS 74 / 50, hisseye özgü hedge'li OOS 23,6 (t 4,0).
Ama yorum ve işlenebilirlik düzeltilmeli. Altı nokta:
1. **Simetrik bir 'fade' değil.** Gün-ağırlıklı (DW) portföyde kârın tamamı gap-UP short'tan geliyor: OOS +33,9 bps (t 4,6). Gap-DOWN long OOS'ta −19,2 (t −1,65), 2024+ −39 (t −2,7). İşlem-ağırlıklı (TW) ölçümde tablo tersine dönüyor. Sağlam olan bileşen tekil (hisseye özgü) yukarı gap'lerin gün içinde geri dönmesi.
2. **Koşulsuz gün-içi düşüş eğilimi karışıyor.** Hisse başına ortalama intra −10,6 bps/gün; işlemlerin %66'sı short. "|gap|>%1 günlerinde her zaman gün-içi short" kıyas stratejisi OOS DW 28,6 bps ile fade'den (16,7) daha iyi. Geçmiş 250 günün ortalama intra'sı çıkarılınca fade OOS 13,0 (t 2,2) kalıyor.
3. **IS istatistiği ölçüm hatasıyla şişmiş.** İddiadaki IS 28,0 (t 7,0) eski temizlik kuralıyla çıkıyor (tüm dönem ±%10,5; benim tekrarım 27,6, t 6,8). Bu kural 2020 öncesinde |cc|>%10,5 olan GERÇEK işlem günlerini atıyor. cc gün sonu bilgisi içerdiği için bu, sonuca göre koşullama (look-ahead) demek. Atılan 196 büyük gap işleminin ortalaması −155 bps. Güncel rejime bağlı kuralla IS 22,0 (t 5,2). Hisseye özgü fade'de IS 42,6 → 35,3. Hisse bazında FDR (tam dönem) 10/47 değil 6/47. Yalnız OOS t'siyle FDR'den geçen tek hisse CIMSA (1/47).
4. **Gerçekçi giriş etkiyi kırpıyor.** h1 döneminde (2023-12 → 2026-10):
   - E0 (açılış) → C: 25,2 bps DW / 16,8 TW.
   - İlk 30 dk VWAP vekili → C: 21,0 / 13,2. Vekilin açılışa göre ortalama kaybı 3,5 bps, iddia (≈3) doğrulandı. m5 (60 gün) gerçek 10:05–10:30 VWAP'ı ile vekil farkı −1,6 bps; vekil iyimser değil.
   - 10:30 (P0730) → C: 15,8 (t 2,15) / 7,5 (t 0,7).
   - Hisse bazında P0730→C: %62 pozitif, 0/47 FDR.
5. **Maliyetten sonra 47'lik portföy yok.**
   - E0, OOS: 8 bps + tik ile +2,7 (t 0,45); 15 + tik ile −4,3; kademeli 8/30 + tik ile −10,1.
   - Gerçekçi girişle (P0730) 8 + tik'te bile ≈0 (1,8).
   - Likit yarı brüt ≈0. Etki yalnız illikit yarıda; maliyet de en çok orada.
6. **CIMSA tek güçlü aday.** IS 45 (t 3,7), OOS 74 (t 3,9), iki yön de pozitif, permütasyon p<0,001, deprem dönemi hariç 69 (t 3,8).
   - Kırılganlık: en iyi 10 işlem çıkınca 30 bps (t 1,6). h1 döneminin 2. yarısında 10:30 girişi 25 bps (t 0,95). Dünkü gap'le yapılan plasebo da +46 (t 2,2); yani etki tamamen aynı güne özgü değil.
   - **OYAKC'de IS anlamlı değil:** 26 bps (t 1,3); 2016–20 23 (t 0,8). İddiadaki IS +48 (t 2,6) tekrarlanmadı.
   - Kimya ajanının +64/+40'ı aynı veri ve aynı sinyal; bağımsız teyit sayılmaz (74/50 brüt − 10 bps).

## 1. İddia ↔ bağımsız sonuç

| İddia (YG1) | İddia rakamı | Benim (vc.py, güncel kurallar) | Durum |
|---|---|---|---|
| Hisse medyanı OOS (|gap|>%1, E0) | +17,8 bps, %87 pozitif | +18,4 bps, %87 pozitif (OOS n=11.548) | ✔ |
| FDR | 10/47 | Tam dönem t ile 6/47 (AKSEN, CIMSA, DOHOL, ENKAI, OYAKC, SOKM). Yalnız OOS t ile 1/47 (CIMSA). |gap|>%2: 18/47 (tam), 14/47 (OOS); iddia 21 | ✘ (abartılı) |
| Portföy OOS | 16,5 (t 2,8) | DW 16,7 (t 2,79); TW 16,6 | ✔ |
| Portföy IS | 28,0 (t 7,0) | 22,0 (t 5,2). Eski ±%10,5 kuralıyla 27,6 (t 6,8); fark look-ahead'li filtreden | ✘ (düzeltilmeli) |
| İllikit / likit yarı OOS | 26,9 / 3,1 | 26,9 (t 3,96) / 2,2 (t 0,29). Dinamik (geçmiş 250g ciro) sınıflama: 29,4 / 2,7 | ✔ |
| İlk 30 dk VWAP giriş kaybı | −3 bps | +3,5 bps kötü (TP1 vekili). 10:30 son fiyat +9,2 bps kötü; 11:30 +5,1 | ✔ (vekil için) |
| CIMSA / OYAKC OOS | +74 / +50 | 74,1 (t 3,87) / 50,3 (t 2,76) | ✔ |
| CIMSA / OYAKC VWAP girişi | +78 / +48, FDR | 77,7 (t 3,2) / 48,0 (t 3,5), ikisi de FDR'den geçiyor (47 içinde). **Ama dönem 2023-12+ (h1), OOS 2021–26 değil.** 2. yarı (≈2025-05+): 34 / 30 (t 1,2 / 1,7) | ✔ rakam / ⚠ dönem |
| Hisseye özgü hedge'li OOS | 24,2 (t 4,2) | 23,6 (t 4,0) DW; 32,3 (t 4,0) TW. 2024+ 30,0 (t 3,4); 2025 23,2 (t 1,3); Ağu–Eki 2026 3,2 (t 0,1). IS 35,3 (iddia 42,6) | ✔ OOS |
| Kimya: CIMSA/OYAKC OOS +64/+40 | net 10 bps | 74/50 brüt; aynı seri ve aynı sinyal, bağımsız değil | ✔ ama bağımsız değil |

## 2. Zamanlama ve dolum
- **Sinyal:** gap = cc_adj − ln(C/O). 10:00 TSİ'de, spot açılış müzayedesi sonrasında biliniyor. Sinyalde look-ahead yok.
- **E0 (açılış fiyatından giriş):** Spot açılış müzayedesine emir girmeyi gerektiriyor. SSF ile bu fiyattan işlem yapılamaz (SSF 09:30'da açılıyor ve kendi fiyatıyla işliyor). E0 iyimser bir üst sınır.
- **h1 barları:** 06:30 barı 09:30–10:30 TSİ'yi kapsıyor. o = günlük açılış (%99,8); h/l açılış fiyatını içeriyor (h≥O, l≤O, %100); c = 10:30 fiyatı. Kontrol ettim.
- **h1–günlük tutarsızlıkları:** HEKTS 2024-09-09 → 11-14 arasında h1'de bölünme düzeltmesi günlükle uyumsuz (ln(h1_o/O) = 1,02). GUBRF'de 1 gün. Bu günleri atmayınca 2024 P0730→C 93 bps gibi sahte değerler çıkıyor; atıldı.
- **Çıkış:** kapanış (C) yerine 17:30 (P1430) ile çıkılınca E0 portföyü 25,2 → 19,3. Kârın ~6 bps'i son 30 dk + kapanış müzayedesinde. SSF 18:15'e kadar işlediği için C'ye yakın çıkış mümkün; baz riski var.
- **SSF bülteni testi (v4, 2.422 gün, kendi ayrıştırıcım):** SSF'nin kendi gap'iyle (ilk işlem / önceki uzlaşma) fade, ilk işlemden uzlaşmaya 70–80 bps (t 10–15) veriyor. Aynı örneklemde spot E0 18 bps.
  - Bu, ilk işlem fiyatındaki mekanik gürültünün (bid-ask / bayat ilk baskı) ne kadar büyük olduğunun kanıtı; işlenebilirlik kanıtı değil.
  - SSF gap ~ spot gap eğimi 0,47, korelasyon 0,56. Açılış fiyatına dayalı her fade bu tür mekanik dönüşle şişebilir.
- **Bid-ask / müzayede gürültüsü ayrıştırması:** 10:30 fiyatını referans almak bunu dışlıyor. O→10:30 parçası fade kârının yaklaşık %40'ı: 9,4 bps (t 2,1). 10:30→C kalan kısım DW 15,8 (t 2,15), TW 7,5 (t 0,7).

## 3. Yapısal bulgular (iddiada yok)

**Asimetri ve ağırlıklandırma.**

DW = her gün eşit sermaye; TW = her işlem eşit nominal.

| Dönem | Gap-UP short DW | Gap-UP short TW | Gap-DOWN long DW | Gap-DOWN long TW |
|---|---|---|---|---|
| IS 14–20 | 29,1 (t 5,2) | — | 2,9 (t 0,4) | — |
| OOS 21–26 | 33,9 (t 4,6) | 12,2 (≈ koşulsuz eğilim) | −19,2 (t −1,65) | +28 (havuz) |
| h1 dönemi | 46,7 | 14,6 | −39,3 | +21,3 |

**Aynı gün aynı yönde gap yapan hisse sayısına göre kovalar** (TW, OOS):
- Tekil (1–2 hisse) gap-UP short: IS 43 (t 3,7), OOS 59 (t 4,2).
- 3–5 hisse: 27 / 45.
- Toplu (16+) gap-UP: 5 / 4, yani dönüş yok.
- Tekil gap-DOWN long: 3 / −16, yani dönüş yok.
- Toplu gap-DOWN long: IS −6, OOS +73 (t 2,5). Az sayıda çöküş-rebound gününe dayanıyor; kırılgan.

**Havuz regresyonu** (gün kümelenmiş): intra ~ idio_gap + XU030_gap.
- OOS: idio −0,125 (t −3,0), piyasa −0,098 (t −1,0).
- 2024+: idio −0,193 (t −4,9), piyasa +0,059.
- |gap|>%1 alt örnekleminde OOS: yukarı eğim −0,25 (t −2,7), aşağı eğim −0,08 (t −1,1).

**Plasebo** (gap_{t−1} ile bugünü fade): portföyde IS 11,8 (t 2,6), OOS −5,5 (t −1,0). IS etkisinin bir kısmı aynı güne özgü değil; OOS'ta öyle.

**En tutarlı bileşen** (v8): hisseye özgü YUKARI gap (idio > +%1), hisse short + XU030 long.
- E0, brüt:
  - IS 28 DW / 43 TW.
  - OOS 42,6 / 34,7 (t 5,9 / 5,1).
  - 2025 49 / 37.
  - Ağu–Eki 2026 19,5 / 6,2.
- h1 dönemi, 15 + tik + 3 bps (hedge) net:
  - VWAP vekili girişi: 17,4 (t 2,1) DW, 8,0 (t 0,9) TW.
  - 10:30 girişi: 3,0 / −4,0.
- Likit yarıda net ≈0.

## 4. Maliyet duyarlılığı
Tik maliyeti = 1 tik (0,01 TL) / 30.10.2026 fiyatı. SASA 69 bps, HEKTS 62, ODAS 24, TSKB 11; diğerleri <10. Yahoo fiyatı bölünme düzeltmeli olduğundan tarihsel nominal fiyat yok.

Net bps (DW):

| Strateji / dönem | Brüt | 8 + tik | 15 + tik | 30 + tik | Kademeli 8/30 + tik |
|---|---|---|---|---|---|
| E0 47, OOS | 16,7 | 2,7 (t 0,45) | −4,3 | −19,3 | −10,1 |
| E0 illikit24, OOS | 26,9 | 10,0 (t 1,5) | 3,0 | −12,0 | −12,0 |
| E0 likit23, OOS | 2,2 | −7,9 | −14,9 | −29,9 | −7,9 |
| Gap-UP short 47, OOS | 33,9 | 20,4 (t 2,8) | 13,4 (t 1,8) | −1,6 | 7,6 |
| Hedge'li idio 47, OOS (+3 bps hedge) | 23,6 | 6,4 | −0,6 | −15,6 | −7,1 |
| h1 47, VWAP vekili → C | 21,0 | 7,0 | 0,0 | −15,0 | −5,7 |
| h1 47, 10:30 → C | 15,8 | 1,8 | −5,2 | −20,2 | −10,9 |
| CIMSA E0, OOS | 74,1 | 63,5 (t 3,3) | 56,5 (t 2,95) | 41,5 (t 2,2) | 41,5 |
| CIMSA 10:30 → C, h1 2. yarı | 25,2 | 14,6 | 7,6 (t 0,3) | −7,4 | −7,4 |
| OYAKC E0, OOS | 50,3 | 36,7 | 29,7 (t 1,6) | 14,7 | 14,7 |

TW değerleri genellikle daha düşük (ör. h1 10:30→C brüt 7,5; 8 + tik ile −6,3).

## 5. Yıllar
**E0 47, brüt DW (bps):**

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| −5,7 | 0,3 | 24,6 | 45,4 | 58,3 | 20,9 | 13,0 | 8,8 | −6,9 | 21,9 | 36,7 | 8,0 | 34,7 |

- 15 + tik sonrası belirgin pozitif yıllar yalnız 2017, 2018, 2024 ve 2026; 2016, 2019 ve 2023 ≈0; diğer 6 yıl negatif.
- Hedge'li idio brüt 13/13 yıl pozitif (8,8 … 63,4). 15 + tik sonrası 13 yılın 8'i pozitif (çoğu +5…+15).
- h1 dönemi:
  - 10:30 → C: 2024 30,8 / 2025 −1,0 / 2026 21,9.
  - VWAP vekili → C: 36,9 / 4,3 / 26,5.
- m5 (Ağu–Eki 2026, fon krizi): E0→C TW −43 bps, DW +0,7.

**CIMSA yıllara göre:** 2014 ve 2015 ≈ +10; 2016–2026 her yıl pozitif (2025 56 bps ama medyan −41).

**OYAKC yıllara göre:** 2016 −16, 2020 −23; diğer yıllar pozitif.

## 6. Veri kontrolleri (bu ajan)
- Yahoo açılışı 2014–15'te kısmen bozuk: o==c oranı medyan %13,7 ve %9,9, c==c_{−1} oranı %7,4 ve %6,3. 2016+ normal. Bu yüzden IS 2016–20 ayrıca raporlandı: E0 32,5 (t 5,8).
- Bayat gün kuralı: hacim 0 ve h==l. Önceki geçerli satır bir önceki BIST günü değilse gap NaN.
- Kurumsal işlem eşiği: rejime bağlı, ham oran ve adj oranı için ayrı ayrı uygulandı.
- Temettüden arındırılmamış ham gap ile OOS 13,5. Sonuç değişmiyor.

## 7. Sınırlamalar
- SSF gün-içi fiyatı ve kotasyonu yok; gerçek spread ve SSF'de 10:00–10:30 VWAP ile dolum test edilemedi. Bültendeki SSF ilk işlem fiyatı mekanik gürültü taşıyor (yukarıda).
- Evren bugünün 47 SSF dayanağı; hayatta kalma ve seçim yanlılığı var. Likidite sınıflaması statik (son 250 gün) ve dinamik olarak iki şekilde denendi; sonuç aynı.
- Tik maliyeti bugünkü fiyatla hesaplandı; spread'in 1 tik olduğu varsayıldı (illikit SSF'lerde çok tik olabilir).
- Çoklu test: 3 eşik × 47 hisse × 5 dönem + h1'de 8 giriş/çıkış × 47; BH yalnız aile içinde uygulandı.

## 8. Düzeltilmiş iddia (önerilen metin)
**47 hisselik sistematik gap fade:** brüt etki yeniden üretildi (OOS DW 16,7 bps, t 2,8). Ancak:
- Etki asimetrik: tekil yukarı gap'lerde var, aşağı gap'lerde yok. Ağırlıklandırmaya duyarlı.
- Kısmen BIST'in gün-içi negatif eğilimi.
- Likit yarıda yok.
- 10:30 girişiyle yarıya iniyor.
- 8–15 bps + tik maliyetiyle OOS net ≈0 ya da negatif.
- IS t 7,0 değil t 5,2 (eski filtre look-ahead'liydi). FDR 10/47 değil 6/47; OOS'ta 1/47.

Güven: ilişki ORTA, işlenebilirlik DÜŞÜK.

**Hisseye özgü yukarı gap short + XU030 hedge:** OOS brüt 35–43 bps (t ≥5). VWAP-30 girişi ve 15 + tik + hedge maliyetiyle net ~8–17 bps (t 0,9–2,1), 10:30 girişiyle ≈0. Güven ORTA–DÜŞÜK.

**CIMSA:** IS ve OOS ikisinde de anlamlı; E0 OOS net (15 + tik) 56 bps (t 2,95). Gerçekçi girişle ve son dönemde zayıflıyor (2. yarı 10:30 girişi net ≈ +8, t 0,3). Güven ORTA.

**OYAKC:** OOS 50 (t 2,8) ama IS anlamsız (t 1,3). Güven DÜŞÜK–ORTA.

TradingView adayları: BIST:CIMSA, BIST:OYAKC, BIST:CIMSA1!, BIST:OYAKC1! (SSF sürekli), BIST:XU030, BIST:XU0301! (hedge).
