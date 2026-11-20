# V5 — sektör sepeti pratikte nasıl kurulur (betimsel; yeni kural üretmez)

Tablo `ek/v5_sepet.csv`, kod `kod/v5_sepet/run.sh`. Birim bps. `per` = sinyal günleri − dönemin sıradan günleri; net = `per` − temel maliyet (≈ 30 bps). Havuz = 2023-01 → 2026-11. S1: XELKT 20 günlük zirve. S2: XELKT getirisi ≥ 60 günlük standart sapma.

## ÖNERİLEN UYGULAMA

1. **17:50'de sinyale bak.** S1: XELKT önceki 19 kapanışın en yükseğinin üstünde. S2: günlük artış ≥ 60 günlük standart sapma (bugün %2,1). 17:50 değeri kapanış sinyalinin S1'de %96'sını, S2'de %90'ını yakalıyor (kesinlik %95, %94).
2. **Sepet: en likit hisselere daraltma.**
   - Tam sepet: tavanda olmayan bütün üyeler (~40 emir), eşit tutar. Doğrulanan sürüm.
   - 15 hisse: 60 günlük medyan TL hacim sırasında 6.–20. olanlar. Bugün: AHGAZ, ODAS, CANTE, METEN, HUNER, AKFYE, MASFN, BESTE, VEYAS, SMRTG, IZENR, ZOREN, MOGAN, BIOEN, KLYPV. Sınamada sıra her gün yenilendi.
   - Çıkar: 17:50'de tavanda olan; o gün sektör ortalamasının ≥ 5 puan gerisinde olan (K2).
3. **Emir:** kapanış seansında (18:01–18:05) kapanış fiyatından alım, hisse başına eşit TL.
4. **Çıkış:** 3. işlem günü kapanış seansı. Pozisyondayken yeni sinyal gelirse sat-al yapma; çıkışı son sinyalden 3 gün sonraya ertele.
5. **İşlem yapma:** tavanda olmayan hisse 5'ten azsa; sinyali kaçırıp ertesi kapanışa kaldıysan (ertesi açılıştan giriş 78 → 64; ertesi kapanıştan 46, t 1,3); yalnız AKSEN/ENJSA/ODAS ya da en likit 5 ile; GNS fonuyla.

## Beklenen getiri ve risk (S1, havuz, 174 sinyal günü, olay başına 3 gün)

| | Tam sepet | 15 hisse |
|---|---|---|
| Ham ortalama, medyan | 75, 78 | 76, 82 |
| `per` (t) | 83 (2,7) | 79 (2,8) |
| Net temel, muhafazakâr | +52, +27 | +49, +24 |
| %10 ve %90 (ham) | −297, +414 | −262, +378 |
| Zarar olasılığı (net) | %44 | %41 |

- S2 tam sepet: `per` 70 (t 2,2), net +40. 2010–2022'de net ≈ +2: maliyet (42 bps) etkiyi yiyordu.
- En kötü %5: −401 ve altı; en kötü olay −891 (17.03.2025), S2'de −1.038 (20.10.2026). En uzun zarar serisi 7 sinyal günü.
- Taban kilidi: işlemlerin %1'inde çıkış günü hisse tabanda kilitli (ortalama −%15); olayların %21'inde sepette böyle en az bir hisse var.
- Sıklık: yılda ~45 S1 günü. Ertelemeli tutmada ~10 giriş, ortalama 7 gün, günlerin %29'unda pozisyon.

## Altı soru

1. **Rastgele N hisse.** Ortalama aynı, oynaklık artıyor. Olay başına standart sapma: tam 308; N = 3, 5, 8, 12, 20 için 425, 377, 348, 330, 315. Rastgele 5'te zarar olasılığı %45, %10–%90 aralığı −379, +516. 174 olay sonunda net ortalamanın %10–%90 aralığı: N = 3'te 22–82, N = 12'de 41–65 (tam 52).
2. **Seçim.** En likit 5: OOS-1 26, kasa 39 (tam 85, 86). En likit 10: 45, 57. VİOP üçlüsü kasa −25. Üç dönemde ve iki sinyalde de tam sepetten kötü olmayanlar: likiditesi alt yarıdakiler, fiyatı 5 TL altı. Tavana ≥ %2 uzak: fark ≤ 4. K2 süzgeci: IS 0, OOS-1 +2'ye kadar, kasa +8 ile +16. T2'nin seçtikleri: IS −38 ve −28, sonrası +6 ile +37. Farkların çoğunda |t| < 2; 30 varyant, çoklu test düzeltmesi yok.
3. **Birleştirme.** S2 günlerinin %37'si S1 günü. İkisi birlikte: 125 (t 2,5; 54 gün). Yalnız S2: OOS-1 9, kasa 88. Her sinyal günü ayrı dilim: yılda 45 işlem, net +52. Ertelemeli: yılda 10 giriş, net +139; gün başına maliyet 10 → 4.
4. **Kapasite (42 hisse).** 100 bin TL: hisse başına 2.381 TL, kapanış seansının en çok %1,6'sı; LYDYE alınamaz (2.902 TL). 1 milyon: 3 hissede %10 aşılıyor (ZEDUR, ENDAE, CONSE). 5 milyon: 13 hissede %10, 6'sında %25 aşılıyor (ZEDUR %82). %10 sınırı için üst tutar: tam sepet ≈ 610 bin, 15 hisse ≈ 3,2 milyon TL. Yarım adım ortalama 10 (CANTE 54).
5. **Koruma (0,68 × XU030 vadeli SAT).** Standart sapma 308 → 259; `per` S1'de 78 → 59, S2'de 67 → 65. Kontrat ≈ 149 bin TL: ~220 bin TL altında kurulamaz. Önerilmez.
6. **GNS fonu.** Uygun değil: 13:30'dan sonraki alım “fiyat t+2” ile gerçekleşiyor, sinyalin ilk günü (etkinin yarısı) kaçıyor; satım nakdi t+2 ya da T+3.

## Doğrulanmış / betimsel

- **Doğrulanmış (kasa, Holm):** S1 ve S2, tam sepet, kapanıştan giriş, 3 gün (kasa +86, t 2,5; +95, t 2,3).
- **Betimsel:** alt sepetler (15 hisselik sepet ilk sonuçlardan sonra eklendi), ertelemeli tutma, 17:50 vekili, koruma, kapasite. Kapanış seansı hacmi dolaylı tahmin; komisyon varsayım; asgari komisyon ve toplu emir olanağı kontrol edilmedi.
