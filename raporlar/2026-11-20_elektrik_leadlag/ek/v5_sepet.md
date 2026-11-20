# V5 — sektör sepeti pratikte nasıl kurulur (betimsel; yeni kural üretmez)

Tablo: `ek/v5_sepet.csv`; kod: `kod/v5_sepet/run.sh <panel_full>`. Birim bps. `per` = sinyal günleri − dönemin sıradan günleri. Net = temel maliyet (25 bps + yarım fiyat adımı ≈ 30 bps) sonrası `per`. Havuz = 2023-01 → 2026-11. S1 = XELKT 20 günlük en yüksek kapanış; S2 = XELKT günlük getirisi ≥ 60 günlük standart sapması.

## ÖNERİLEN UYGULAMA

1. **17:50'de sinyale bak.** S1: XELKT, önceki 19 kapanışın en yükseğinin üstünde. S2: günlük artış ≥ son 60 günün standart sapması (bugün %2,1; 2023 sonrası medyan %1,7). 17:50 değeri kapanış sinyalinin S1'de %96'sını, S2'de %90'ını yakalıyor (kesinlik %95 / %94); eşik ≥ 25 bps aşıldıysa kesinlik %98.
2. **Sepet: en likit hisselere daraltma.**
   - Tam sepet: o gün tavanda olmayan bütün üyeler (~40 emir), eşit tutar. Doğrulanan sürüm budur.
   - 15 hisse: 60 günlük medyan TL hacim sırasında 6.–20. olanlar. Bugün: AHGAZ, ODAS, CANTE, METEN, HUNER, AKFYE, MASFN, BESTE, VEYAS, SMRTG, IZENR, ZOREN, MOGAN, BIOEN, KLYPV. Sınamada sıra her gün yenilendi; elle aylık güncelleme sınanmadı.
   - Listeden çıkar: 17:50'de tavanda olan; o gün sektör ortalamasının ≥ 5 puan gerisinde olan (K2).
3. **Emir:** kapanış seansı (18:01–18:05), kapanış fiyatından alım, hisse başına eşit TL.
4. **Çıkış:** 3. işlem günü kapanış seansında. Pozisyondayken yeni sinyal gelirse sat-al yapma; çıkışı son sinyalden 3 gün sonraya ertele.
5. **İşlem yapma:** tavanda olmayan hisse sayısı < 5 ise; sinyali ertesi günün kapanışına kadar kaçırdıysan (ertesi açılıştan giriş 78 → 64; ertesi kapanıştan 46, t 1,3); yalnız AKSEN/ENJSA/ODAS ya da en likit 5 hisseyle; GNS fonuyla.

## Beklenen getiri ve risk (olay başına 3 gün, S1, havuz, 174 sinyal günü)

| | Tam sepet | 15 hisse (6.–20.) | Rastgele 5 |
|---|---|---|---|
| Ham ortalama / medyan | 75 / 78 | 76 / 82 | 74 / 70 |
| `per` (t) | 83 (2,7) | 79 (2,8) | 83 |
| Net temel / muhafazakâr | +52 / +27 | +49 / +24 | +52 / +27 |
| %10 – %90 (ham) | −297 … +414 | −262 … +378 | −379 … +516 |
| Zarar olasılığı (net) | %44 | %41 | %45 |

- S2 tam sepet: `per` 70 (t 2,2), net +40 / +15. 2010–2022'de net temel ≈ +2: o dönemde maliyet (42 bps) etkiyi yiyordu.
- En kötü %5: −401 ve altı (ortalaması −575); en kötü olay −891 (17.03.2025), S2'de −1.038 (20.10.2026). En uzun zarar serisi: art arda 7 sinyal günü; ertelemeli işlemlerde 5.
- Taban kilidi: işlemlerin %1'inde çıkış günü hisse tabanda kilitli (ortalama sonuç −%15); olayların %21'inde sepette en az bir böyle hisse var. 5 günden uzun kilit: 1 işlem (MAGEN, −%32).
- Sıklık: S1 yılda ~45 sinyal günü. Ertelemeli tutmada yılda ~10 giriş, ortalama 7 gün, günlerin %29'unda pozisyon; “S1 ya da S2” ile ~20 giriş, günlerin %51'i.

## Altı soruya kısa yanıt

1. **Sepet büyüklüğü (rastgele N).** Ortalama değişmiyor, oynaklık artıyor. Olay başına standart sapma: tam 308; N = 3 / 5 / 8 / 12 / 20 için 425 / 377 / 348 / 330 / 315. Tam sepetten sapma: 294 / 219 / 163 / 121 / 71. 174 olay sonunda net ortalamanın %10–%90 aralığı: N = 3'te 22…82, N = 12'de 41…65 (tam 52).
2. **Seçim.** En likit 5: OOS-1 26, kasa 39 (tam 85 / 86); en likit 10: 45 / 57; VİOP üçlüsü kasa −25. Üç dönemde ve iki sinyalde de tam sepetten kötü olmayan: likiditesi alt yarıdakiler, fiyatı 5 TL altı. Yalnız birinde: orta üçte birlik, o gün sektörün altında kalanlar, gaz, panel (S1); 6.–20., yenilenebilir, termik (S2). Tavana ≥ %2 uzak: fark ≤ 4. K2 süzgeci: IS 0, OOS-1 +0…+2, kasa +8…+16. T2'nin seçtikleri: IS −38 / −28, sonrası +6…+37. Farkların çoğunda |t| < 2; 30 varyant, çoklu test düzeltmesi yok.
3. **Birleştirme.** S2 günlerinin %37'si aynı zamanda S1 günü. İkisi birlikte: havuz 125 (t 2,5; 54 gün). Yalnız S2: OOS-1 9, kasa 88. S1'de her sinyal günü ayrı 3 günlük dilim: yılda 45 işlem, net +52; ertelemeli: yılda 10 giriş, giriş başına net +139; gün başına maliyet 10 → 4.
4. **Kapasite (20.11.2026, 42 hisse).** 100 bin TL: hisse başına 2.381 TL, kapanış seansının en çok %1,6'sı; LYDYE alınamaz (2.902 TL). 1 milyon: 3 hissede > %10 (ZEDUR, ENDAE, CONSE). 5 milyon: 13 hissede > %10, 6'sında > %25 (ZEDUR %82). Hepsi ≤ %10 kalsın diye üst sınır: tam sepet ≈ 610 bin TL, 6.–20. sepeti ≈ 3,2 milyon TL. Yarım adım: tam sepet ortalama 10 (CANTE 54), fiyatı ≥ 5 TL olanlarda 4.
5. **Koruma (β 0,68 × XU030 vadeli SAT).** Standart sapma 308 → 259 (−%16); `per` S1'de 78 → 59, S2'de 67 → 65. Bir kontrat ≈ 149 bin TL: ~220 bin TL altındaki sepette kurulamaz. Önerilmez.
6. **GNS fonu.** Uygun değil: 13:30'dan sonra verilen alım “fiyat t+2” ile gerçekleşiyor, yani sinyalin ilk günü (etkinin yaklaşık yarısı) kaçıyor; satım nakdi t+2 / T+3. Komisyon ve stopaj %0, yönetim ücreti %3,20.

## Doğrulanmış / betimsel

- **Doğrulanmış (kasa, Holm):** S1 ve S2; tam sepet, kapanıştan giriş, 3 gün (kasa +86, t 2,5; +95, t 2,3).
- **Betimsel (sonuçlar görüldükten sonra):** alt sepetler (6.–20. sepeti ilk sonuçlardan sonra eklendi), ertelemeli tutma, 17:50 vekili, koruma, kapasite. Kapanış seansı hacmi dolaylı tahmin; komisyon varsayım; asgari komisyon ve toplu emir olanağı kontrol edilmedi.
