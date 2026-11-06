# Olgu denetimi: RAPOR.md (06.11.2026)

Denetçi: v_ana_rapor_olgu. Kapsam: `RAPOR.md`'deki her sayı, tarih, yüzde, t istatistiği ve adlandırılmış iddia. RAPOR.md değiştirilmedi.

**Yöntem.** Her iddia için kaynak bu sırayla arandı: `dogrulama/*.md` (araştırma raporlarıyla çeliştiğinde geçerli), `ajanlar/*.md`, `uygulama/PLAN_BIST.md` ve `PLAN_ABD.md` (plan özetleri için tek ölçüt). Gerekince `hesaplar/` kodu okundu. Dışarıdan veri çekilmedi.

**Etiketler.**
- **DOĞRU:** Doğrulanmış değerle ya da nihai planla tutuyor.
- **DÜZELT:** Külliyat başka bir şey söylüyor. Düzeltilmiş metin ve kaynak verildi.
- **KAYNAKSIZ:** Külliyatta kaynağı yok.

Satır numaraları RAPOR.md'nin 06.11.2026 13:19 sürümüne göre.

## Özet

- ~190 olgu kontrol edildi. **DÜZELT: 55 satır (yaklaşık yarısı küçük ekleme ya da atıf), KAYNAKSIZ: 3**, gerisi DOĞRU.
- Ağırlık sırasıyla en önemli düzeltmeler:
  1. **§5 m.3:** Risk tavanları nihai planlarda yok. `%3/%5/%6` ve `küme ≤%1,5` ABD taslakları ile abd_profesyonel'den geliyor.
  2. **§1.5 m.2–3 ve §5 m.4:** "Bankalar ve VİOP ile kaldıraç", "yabancı alımı tetik", "zorunlu satıcıların karşısında dur" ifadeleri nihai BIST planıyla çelişiyor. Planda kredili işlem ve 1x üstü kaldıraç yok, yabancı akımı sayılmıyor, zorunlu akış yalnız kaçınma kuralı.
  3. **Plan özetlerinde kural hataları:**
     - K1 z-skoru 60 günlük; 20 gün tutma süresi.
     - K8 satışı 18:00'de "E kapanış" kuralıyla yapılıyor; gün içi değil.
     - K3b girişi 17:00 kesimine bağlı ve hedge koşullu.
     - ABD Faz 3 riski %0,75–1; %0,5 değil.
     - ABD vergi istisnası zarar değil, kazanç hasadı.
     - XU100 12 ay getirisi +%3,8; +%3,3 değil.
  4. **"91 fondan 1'i":** v_profesyonel T1'e göre KISMEN (DDF, TTL; vergi sonrası 4 fon).
  5. **Chen-Zimmermann satırı:** Doğrulanmamış 212 sinyallik medyanlar, doğrulanmış 165 sinyallik setin %16 payıyla karıştırılmış.
  6. **Doğrulanamayan rakamlar:**
     - §1.3: banka getirileri ve %26 oranı.
     - §5: 0,72 korelasyonu.
     - §3.2: SG Trend "en kötü 12 ay".
     - Bunlar "yalnız doğrulamadan geçen rakamlar var" cümlesine rağmen işaretsiz.
  7. **Küçük sayı ve atıf hataları:**
     - Erdem: −%0,281 ham ortalama getiri, piyasaya göre düzeltilmiş değil.
     - ABD kaldıraçlı beta MaxDD aralığı −%41'den başlıyor.
     - Ajan raporu sayısı 16; 14 değil.

---

## 1. Giriş (satır 3–7)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 7 | "7 araştırma iş akışı, ~25 ajan" | **KAYNAKSIZ** | Külliyatta sayı yok. Görülen: 16 araştırma raporu (`ajanlar/`), 6 doğrulama raporu (`dogrulama/`), 3+3 taslak, 3+3 hakem, 2+2 kırmızı takım (`uygulama/taslak/`). Öneri: "16 araştırma raporu, 6 doğrulama raporu; planlar için 6 taslak, 6 hakem ve 4 kırmızı takım incelemesi". |
| 7 | "Her iş akışının sonunda ayrı bir doğrulayıcı ajan" | DOĞRU (yaklaşık) | 6 doğrulama dosyası 16 raporun hepsini kapsıyor. |
| 7 | "BIST'te 485 hisse ve 49 endeks (2010–2026)" | **485 DOĞRU; 49 KAYNAKSIZ** | bist_test §1: ≥120 günlük veri olan 485 hisse (496 dosya). `hesaplar/bist_test/f02_endeks.py` 33 endeks çekiyor; dalga_bist 29 / 22 endeks kullanıyor; 49 hiçbir yerde yok. Düzeltme: "485 hisse ve 33 endeks". |
| 7 | "ABD'de Ken French, Chen-Zimmermann, FRED ve AQR verileri" | DOĞRU | abd_test §1; abd_swing_kenarlar §0 (AQR TSMOM). |
| 7 | "burada yalnız doğrulamadan geçen ya da düzeltilmiş rakamlar var" | **DÜZELT** | Raporda doğrulanamamış rakamlar var: §1.3 banka getirileri ve %26 (v_capraz §1 sonu), §3.1 SG Trend "en kötü" (v_abd #7), §5 0,72 (v_profesyonel A14), §3.3 Minervini isabet ve 2,15× (v_profesyonel A3). Düzeltilmiş metin: "burada rakamların çoğu doğrulamadan geçti ya da düzeltildi; doğrulanamayanlar ayrıca işaretli." |

## 2. §0 Çıta (satır 13–26)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 13 | Politika faizi %36 (22.10.2026) | DOĞRU | v_capraz #1; v_profesyonel T14 (karar 22.10, yürürlük 23.10). |
| 13 | Ekim TÜFE yıllık %29,77 | DOĞRU | v_capraz #2. |
| 13 | Reel ~%4,8 geriye dönük, ~%5–8 beklentiye göre | DOĞRU | v_capraz #3 (ex-ante %9,8 abartılı; savunulabilir bant %5–8). |
| 13 | "%40–50 olan nominal faiz; 2024'te PPF'nin brüt bileşik getirisi %53–61'di" | **DÜZELT** | %53–61 kaynaklı: tr_makro_engel §0 m.1 ve §2; v_bist §2.1'e göre 2024 PPF ≈%53. Ama bugünkü nominal faiz %36; %40–50 2024–25'in nominal faizi ve bileşik PPF getirisiydi. Düzeltilmiş metin: "%40–50, 2024–25'in nominal faizi ve PPF'nin brüt bileşik getirisiydi (2024'te %53–61), algı oradan geliyor. Bugün brüt bileşik PPF ~%37–42." (tr_makro_engel §0 m.1) |
| 17 | "Faiz %36'da kalırsa ~%35–38" | **DÜZELT** | v_capraz #4 ve §2 m.11: faiz sabitse ~%36–38. PLAN_BIST §1.1: mevduat roll net ~%37,9, banka PPF'si 12 ay ~%34–35. Düzeltilmiş metin: "Faiz %36'da kalırsa ~%36–38 (32 günlük mevduat aylık roll ~%37,9; PPF'de 12 ay ~%34–35)". |
| 17 | Anket yolunda 12 ayda ~%29 → ~%31–33 | DOĞRU | v_capraz #3 (%29,01) ve #4. |
| 17 | Son 12 ay PPF medyanı brüt %45,5 → net ~%37,5 | DOĞRU | v_bist #13, §2.1. |
| 18 | Pay ve pay/endeks VİOP %0 stopaj | DOĞRU | v_capraz #7; v_profesyonel eksik #1. |
| 18 | Vergi avantajı ~5–7 puan | DOĞRU | v_capraz §2 m.1: brüt %42'de ~7 puan; anket yolunda ~5. |
| 19 | VİOP USDTRY ve diğerleri %10 | DOĞRU | v_capraz #7. |
| 20 | "ABD hisse/opsiyon kazancı ... beyan, %15–40" | **DÜZELT** | v_capraz §2 m.9: yurt dışı opsiyon/vadeli kazancının vergi niteliği belirsiz, özelge yok. Hisse için v_capraz #10 DOĞRU. Düzeltilmiş metin: "ABD hisse kazancı (opsiyon/vadeli kazancının vergi niteliği belirsiz, özelge yok)". |
| 20 | Zarar yalnız aynı yıl mahsup | DOĞRU | v_capraz #10 (kanunda açık hüküm yok, dipnot). |
| 20 | Vergi öncesi ~%20–28 USD/yıl | DOĞRU | v_capraz #22 (~%28 cebir); v_abd §4 m.1 (%20–25+); PLAN_ABD §0 m.8 ("doğrulanmış çapa ~%20–28"; u=0,3'te hesap boyuna göre %12,7–25,9). |
| 22 | Tasfiyedeki 15 PPF'den 4'ü %95–99,9 kaybetti | DOĞRU | v_bist §3 m.3; PLAN_BIST §1.2. |
| 22 | Çıtayı banka PPF'si, TLREF ya da DİBS ile ölç | DOĞRU | v_profesyonel eksik #2. |
| 23 | İleriye dönük net ~%13–15 | DOĞRU | v_abd #34 (~%13–15,5). |
| 23 | 2010–2026 −%7,2/yıl, MaxDD −%85 | DOĞRU | v_abd #34. |
| 23 | "Short F_USDTRY Temmuz 2023'ten beri yılda +%20,8 USD getirdi" | **DÜZELT** (çekince eksik) | Sayı doğru (v_capraz #19). Ama v_capraz #19'un uyarısı eksik: hesap USD teminatın T-bill kazandığını varsayıyor; Türk aracı kurumda ~%0 kazanır (yılda 3,7–5 puan); %10 stopaj ve komisyon hariç. Düzeltilmiş metin: "...yılda +%20,8 USD getirdi (brüt; USD teminatın T-bill kazandığı varsayımıyla; Türk aracı kurumda teminat ~%0 kazanır, yılda 3,7–5 puan eksik; %10 stopaj hariç)". Aynı çekince §1.3 satır 58 için de geçerli. |
| 23 | 2018–2026 toplamı +%4,3; 2021'de −%30 | DOĞRU | v_capraz #19, #21; tr_makro_engel §2.2. |
| 24 | "Son 3 yılda 91 hisse yoğun fondan yalnız 1'i PPF medyanını geçti ve o da şimdi tasfiyede." | **DÜZELT** | v_profesyonel T1 **KISMEN**: "yalnızca biri" yanıltıcı. Adında "Hisse Senedi Yoğun" geçen ama serbest şemsiyede listelenen DDF (+%271,65) ve %81 hisseli TTL (+%288,76) de PPF'yi geçiyor. v_bist §3 m.2: vergi sonrası kıyasta 108 hisse fonundan 4'ü geçiyor. BIH'in getirisi güvenilmez (tr_profesyonel §8). Düzeltilmiş metin: "Son 3 yılda, 3 yıllık verisi olan 91 yurt içi hisse senedi yoğun fondan yalnız 1'i (tasfiyedeki Pardus'un BIH'i; getirisi güvenilmez) PPF medyanını geçti. Serbest şemsiyedeki DDF ve %81 hisseli TTL de geçiyor; vergi sonrası kıyasta 4 fon geçiyor." |
| 24 | "Üç alt dönemin üçünde de PPF'yi yenen yönetici yok." | **DÜZELT** | v_profesyonel T2: hisse, serbest ve değişken fon için DOĞRU (yöntem sınırlı). PPF benzeri FSF üçünü de kazandı. Düzeltilmiş metin: "Üç alt dönemin üçünde de PPF'yi yenen hisse, serbest ya da değişken fon yok." |
| 24 | Beta yüksek reel faize yenildi | DOĞRU | v_profesyonel T1 ve eksik #3: medyan aktif HSYF endeks fonunu 3 yılda ~22 puan geçti. |
| 26 | "yılda ~%31–36 net TL'nin üstüne çıkması gerekiyor" | **DÜZELT** | Raporun kendi tablosu (17), §1.2 (45), §1.5 (96), §5 (264), v_capraz #4 ve PLAN_BIST §1.1 ~%31–38 diyor. Düzeltilmiş metin: "yılda ~%31–38 net TL'nin". |

## 3. §1.1–1.2 (satır 34–47)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 34 | MKK verisi, 20.000 birey, 2011–12; ~%70 endeksi yenemedi; Erdem vd. 2014 | DOĞRU | bist_kim_kazaniyor §2; v_bist #2. |
| 34 | "endeksin haftada %0,281 gerisinde kaldı, yılda ~14,6 puan" | **DÜZELT** | v_capraz #23: −%0,281 Tablo 2'deki **ham** haftalık ortalama getiri, piyasaya göre değil. Piyasaya göre düzeltilmiş değer −%0,286; en yüksek devirli dilim −%0,538. Düzeltilmiş metin: "endeksin haftada ~%0,29 gerisinde kaldı (piyasaya göre düzeltilmiş −%0,286), yılda ~15 puan". −%0,538 ve ~28 puan DOĞRU. |
| 34 | CAPM alfası anlamlı değil | DOĞRU | v_bist #2 (t = −1,51). |
| 35 | FX: %67 (41 çeyrek), 2026/06 %74,4 | DOĞRU | v_bist #1; v_capraz #23. |
| 36 | 53,1 mlr TL faiz, 32,3 mlr TL komisyon, ~%60 | DOĞRU | v_bist #3. |
| 37 | "53 arzın ~50'si seri sonundan sonra düştü, medyan −%55." | **DÜZELT** (küçük) | bist_kim_kazaniyor §0 m.5: 2025–26, 52/53, medyan −%55,5. v_bist #11: muhtemelen 50–51/53; kaynak bedelsize göre düzeltilmemiş. Düzeltilmiş metin: "2025–26'daki 53 arzın 50–51'i seri sonundan sonra düştü, medyan −%55 (bedelsize göre düzeltilmemiş)." |
| 37 | "2026 arzlarının 36'sından 27'si arz fiyatının altında." | **DÜZELT** (küçük) | v_bist #11: hocaileborsa 27/36, ama veri bedelsize göre düzeltilmemiş. AKFIS −%64 görünüyor, düzeltilmişi +%116. Düzeltilmiş metin: "2026 arzlarının 36'sından ~26–27'si arz fiyatının altında". |
| 43 | DMA pay %28, vadeli %33; DMA pay işlemlerinin %93'ü 2 kurumda; yabancı kurum vadelide %47 | DOĞRU | v_bist #4; bist_kim_kazaniyor §1.3 (2026/03). |
| 44 | Tera %35 | DOĞRU | v_bist #3. |
| 44 | TLY 3 yılda +%71.787, oynaklık %21, düşüş −%4,2 | DOĞRU | v_profesyonel T4. Aynı satırdaki %89 → %81,6 düzeltmesi RAPOR'da kullanılmamış. |
| 44 | Grup hisseleri 16.09'dan beri −%95/−%98 | DOĞRU | bist_kim_kazaniyor §0 m.4, §3. |
| 44 | KTLEV, ODINE, HEDEF, PEKGY en büyük kırılım kârları | DOĞRU | v_bist #28. |
| 45 | Net ~%31–38 | DOĞRU | v_capraz #4. |
| 47 | "İşlem başına 1–5%" | **DÜZELT** (küçük) | Raporun kendi tablosundaki kenarlar şunlar: +%1,2 (temettü öncesi), +1,3–3,1 (çiftler), +%5,3 (kırılım), +%6,5 (yüksek verimli temettü; v_olay §0). Düzeltilmiş metin: "İşlem başına %1–7". |
| 47 | Önceki 15–70 bps'lik kenarlar | DOĞRU | seytan_taban_oranlar §2 m.4; bist_swing_kenarlar §10 (+14…+50 bps). |

## 4. §1.3 Büyük para tablosu (satır 49–63)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 49 | Başlık: "(2018–2026, dolar bazında, VİOP vadelilerinden hesaplandı)" | **DÜZELT** | Banka, XU030 ve carry satırları VİOP uzlaşmalarından (tr_makro_engel §0 m.14). Long USD satırları spot kurdan (3,78 → 6,56; 8,3 → 18,36, Wikipedia). Son üç satır dalga_bist §2'den: XU100'e göre göreli, ex post dip-tepe ölçüsü (v_dalga B11). İlk dönem Aralık 2017'de başlıyor. Düzeltilmiş metin: "(Ara 2017–2026; bankalar, XU030 ve carry dolar bazında VİOP uzlaşmalarından, long USD spot kurdan; son üç satır XU100'e göre göreli ve ex post dip-tepe)". |
| 53, 54, 57 | GARAN +%91; bankalar +%52; +%45, +%73 | **DÜZELT** (işaret eksik) | Rakamlar tr_makro_engel §2.1 tablosuyla aynı, ama v_capraz §1 sonu "Banka hisselerinin dönem getirileri: GARAN +%91 / +%73, YKBNK +%149" için **DOĞRULANAMADI** diyor. Düzeltilmiş metin: her hücrede "(doğrulanamadı)" ya da başlıkta "banka getirileri doğrulamada teyit edilemedi". |
| 55 | XU030 +%110 | DOĞRU (yaklaşık) | v_capraz #20 (BIST 100 dolar 2022 +%111). |
| 55 | YKBNK +%149 | **DÜZELT** | DOĞRULANAMADI (v_capraz §1 sonu). |
| 55 | "Reel faiz −%50'ye yakın, hisse enflasyon kalkanı" | **KAYNAKSIZ** | tr_makro_engel §2.3 yalnız "ex-post reel faiz derin negatif (politika %14→%9, TÜFE %78,6 ve üzeri)" diyor. Bileşik hesap ~−%40. Düzeltilmiş metin: "Derin negatif reel faiz (politika %14→%9, TÜFE %78,6+), KKM; hisse enflasyon kalkanı". |
| 56 | "+%74, +%121" | **DÜZELT** (küçük) | tr_makro_engel §0 m.4c: "Ağu–Ara 2021 **tepeye kadar** +%121" (20.12.2021'in gün içi dibi/kur tepesi). Düzeltilmiş metin: "+%74, +%121 (spot kur; 2021'de tepeye kadar)". |
| 58 | Yılda +%20,8 USD | DOĞRU, çekince eksik | Bkz. satır 23. |
| 59 | Koza XU100'e göre +%88–100 | DOĞRU | dalga_bist §2 (rel +88% / +100%); v_dalga B11 (ex post). |
| 60 | Savunma göreli +%100, +%45 | DOĞRU | dalga_bist §2; v_dalga B11. |
| 61 | Rafineri göreli +%56 (XU100 −%27) | DOĞRU | dalga_bist §2 (bitiş 30.10 "teyitsiz"); v_dalga B11. |
| 63 | "Ortodoks dönemde 6 aylık pencerelerin yalnız %26'sında XU030 dolar bazında carry'yi geçti." | **DÜZELT** (işaret eksik) | Kaynak tr_makro_engel §0 m.3; v_capraz §1 sonu: **DOĞRULANAMADI**. Düzeltilmiş metin: "...carry'yi geçti (tr_makro_engel; doğrulamada teyit edilemedi)." |

## 5. §1.4 Swing kenarları (satır 67–92)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 71 | +%5,3 (t 5,1), 2.073 işlem, 17 yılın 15'i, isabet %45, 3,3× | DOĞRU | bist_test §5.1; v_bist #28; PLAN_BIST K4. |
| 71 | "10 slotlu portföyde medyan yılda %34,8 TL." | **DÜZELT** | bist_test §5.2: %34,8, **36 portföy varyantının** medyanı (S1 dahil, 4 evren/dolum × 9 kural). S2 + %15 iz-stop ana evrende %50,9, gerçekçi dolumla %36,2. Düzeltilmiş metin: "10 slotlu portföyde 36 varyantın medyanı yılda %34,8 TL (bu kuralın gerçekçi dolumlu sürümü %36,2)." |
| 71 | En iyi %5 işlem kârın ~%70'i | DOĞRU | v_bist #28 (%69,6). |
| 71 | Düzeltilmiş rf ile 2024–26'da çıtanın 2–8 puan altında | DOĞRU | v_bist §2.1. |
| 71 | "Tavan/taban dolum varsayımıyla en büyük düşüş −%45/−%61." | **DÜZELT** | bist_test §5.2: −%45,1 S2'ye (bu kural), −%61,3 şablonsuz S1'e ait. PLAN_BIST K4 de böyle ayırıyor. v_bist §2.2: dolum modeli Mart 2020 öncesi ±%20 limiti ±%9,5 sanıyor; hatanın yönü belirsiz. Düzeltilmiş metin: "Gerçekçi tavan/taban dolumuyla en büyük düşüş −%45 (şablonsuz S1'de −%61); dolum modeli 2020 öncesi limiti yanlış modelliyor." |
| 72 | %29,6, MaxDD −%34, yanlılık yok, 2024–26 risksizin altında | DOĞRU | bist_test §0 m.4 ve §3; PLAN_BIST §3.11. |
| 72 | "uzun dönemde risksizin +11 puan üstü" | **DÜZELT** (çekince eksik) | bist_test +%11,3, ama bu rf serisine göre; v_bist §2.1'e göre seri gerçek nakdi yılda birkaç puan düşük gösteriyor. Düzeltilmiş metin: "uzun dönemde (düşük hesaplanmış) risksizin +11 puan üstü". |
| 73 | Küme rotasyonu: +5 puan, MaxDD −%40/−%48, filtre | DOĞRU | v_dalga §5 m.1 (+5±5; yanlılıksız evrende t≈1,9). |
| 74 | H52 t 2,2–3,7; 2022 hariç t 0,85–1,5 | DOĞRU | bist_swing_kenarlar §3 (2016–26 t 2,22–2,31; 2021–26 t 3,29–3,67); v_bist #24. |
| 75 | Temettü öncesi 5 gün +%1,2, t 6,5–7,8, n=1.109 | DOĞRU | v_bist #26. Maliyet sonrası ~%0,9; planda olay başına net +%0,2…+0,5. |
| 76 | +%6,5, medyan +%4,1, t 6,5, ~27 işlem günü, 2024–26 +%13,5, likit hisselerde de var, %81 Şubat–Mart, 14–25 olay, ≈ TL faizi + %6–7 | DOĞRU | v_olay §0, §2.3, §5 m.2. |
| 76 | "Duyurunun ertesi kapanışında al" | **DÜZELT** (küçük) | v_olay §1 ve PLAN_BIST K3b: t0 = duyurudan sonraki ilk kapanış (17:00/18:00 kesimi). Düzeltilmiş metin: "Duyurudan sonraki ilk kapanışta al (bildirim 17:00'den önceyse aynı gün)". |
| 76 | "12 yılın 12'si pozitif" | **DÜZELT** (atıf) | olay_bedelsiz §0'ın XU100 kıyaslı +%8,5 sonucu. v_olay muhafazakâr kıyasta yıl dağılımını vermiyor. Düzeltilmiş metin: "XU100 kıyasında 12 yılın 12'si pozitif (olay_bedelsiz)". |
| 77 | 601 olay; [1,10] −%3,3 (t −5,5) | DOĞRU | olay_bedelsiz (N=601); v_olay §2.2 (−%3,26, t −5,5). |
| 77 | Eksik bilgi | **DÜZELT** (ekleme) | v_olay §2.2 ve §5 m.1: 2024–26'da −%1,45 (t −1,5), zayıflamış. Eklenecek metin: "; 2024–26'da zayıf (−%1,45, t −1,5)". |
| 77 | Onay → bölünme net −%0,07; duyuruda alıp 5 gün −%1,6 | DOĞRU | olay_bedelsiz §0; v_olay §0 (−%1,58). |
| 78 | Medyan +%33; 8–22 bin TL; 21 günde −%11, 2024–26 −%17 | DOĞRU | v_olay §0, §3. |
| 79 | "Gerçekçi 1 gün gecikmeyle işlem başına +128–310 bps, t 2,1–2,8" | **DÜZELT** (çekince) | v_bist #25: rakamlar maliyet öncesi; maliyet sonrası (20/40 bps) 88–290 bps. Düzeltilmiş metin: "...+128–310 bps (t 2,1–2,8, maliyet öncesi; maliyet sonrası +88–290 bps)". |
| 79 | "Önceki çalışmadaki SAHOL/AKBNK kenarının daha geniş bantlı hali." | **DÜZELT** | bist_swing_kenarlar §9.1: önceki 1–3 günlük +30–50 bps bulgusunun **20 günlük ufuktaki** karşılığı. v_bist #25: çiftler önceki çalışmadan seçildi (seçim yanlılığı). Düzeltilmiş metin: "Önceki çalışmadaki 1–3 günlük SAHOL/AKBNK kenarının 20 günlük karşılığı; çift o çalışmadan seçildi (seçim yanlılığı)." |
| 80 | "2019–26'da long/nakit yılda %48 (nakit %25)" | DOĞRU, çekince eksik | bist_swing_kenarlar §0 m.2. Nakit serisi v_bist §2.1'e göre düşük hesaplanmış; "(nakit %25, düşük hesaplanmış seri)" eklenmeli. |
| 80 | "Şu an kapalı: XU100 12 ayda +%3,3, nakit +%37." | **DÜZELT** | PLAN_BIST §0 m.1 ve §2.1 T2: +%3,8; nakit ~%37 (test serisi), gerçekleşen brüt PPF ~%45,5. +%3,3 bist_swing'in eski okuması. Düzeltilmiş metin: "Şu an kapalı: XU100 12 ayda +%3,8, nakit ~%37 (test serisi; gerçekleşen brüt PPF ~%45,5)." |
| 83 | 12-1 kesitsel momentum risksizin altında | DOĞRU | bist_test §0 m.1 (ızgara medyanı %15,2). |
| 84 | "Kısa vadeli reversal: yılda −%17,9." | **DÜZELT** (küçük) | bist_test §4: eşit ağırlıklı evrene göre −%17,9/yıl, mutlak değil. Düzeltilmiş metin: "Kısa vadeli reversal: eşit ağırlıklı evrene göre yılda −%17,9." |
| 85 | SMA200, 50/200 değer katmıyor | DOĞRU | bist_test §2. |
| 87 | Geri alım/içeriden alım kenarı yok | DOĞRU | olay_akis_rejim §0; v_olay §4.3. |
| 88 | "Yabancı akımı: fiyatı izliyor, öngörmüyor." | **DÜZELT** | v_olay §0 B ve §4.2 **KISMEN**: "Hiç yok değil, zayıf"; 2006–26 t 2,51, 2021–26 t 1,87, 2024–26 t 1,06. PLAN_BIST §3.11: "ileri 8 hafta tahmini zayıf". Düzeltilmiş metin: "Yabancı akımı: fiyatı izliyor; ileri getiriyi ancak zayıf öngörüyor (2024–26 t 1,1), işlem sinyali değil." |
| 89 | AKD/takas, PIN öngörmüyor | DOĞRU | v_bist #19; bist_swing_kenarlar §5.9. |
| 90 | Ramazan, A/B oranları | DOĞRU | bist_swing_kenarlar §0 m.9. |
| 92 | 63g sonra 6/6, −%6,3, t −4,2 | DOĞRU | v_olay §4.1. |
| 92 | Önce 63g +%3,2 | DOĞRU (zayıf) | olay_akis_rejim §0 (döngü düzeyinde 4/6, "zayıf pozitif"); v_olay yeniden hesaplamadı. |
| 92 | Son 63g +%26; anket 10.12'de indirim bekliyor; 6 döngü, boyut eğilimi | DOĞRU | v_olay §0 (+%26,3), §5 m.4; olay_akis_rejim §4.4 (anket %35). |

## 6. §1.5 Formül (satır 96–101)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 96 | Net ~%31–38 | DOĞRU | v_capraz #4. |
| 96 | "XU030 nakit-taşıma (...ima edilen faiz ~%29)" | **DÜZELT** (eksik) | v_profesyonel T12: %29,3 basit (DOĞRU). Ama PLAN_BIST §1.2 ve §1.5'e göre bugün HAYIR: %29,3 < mevduat neti %32,6; açılış eşiği %35,6. Düzeltilmiş metin: "XU030 nakit-taşıma (spot long + vadeli short; iki bacak da %0 stopaj, ima edilen basit faiz ~%29,3; bugün kapalı, açılış eşiği %35,6)". |
| 97 | "Tetikler: rezerv artışı, aylık TÜFE %2'nin altına inmesi, yabancı alımı, CDS 230'un altı, faiz indirim döngüsü. O zaman bankalar ve VİOP üzerinden kaldıraç." | **DÜZELT** | Tetiklerin kaynağı tr_makro_engel §5.1. Ama nihai plan farklı ve rapor planla çelişiyor. PLAN_BIST §2.1–2.2: TÜFE "2 ay üst üste"; yabancı akımı **sayılmaz**; GEÇİŞ için T3 (SMA50) + M1 + {M2, M4, M5}. §1.3 m.4: kredili işlem hiçbir rejimde yok. K7: 1x'i aşmaz. §3.10 A7: sürprizsiz indirimden sonra bankalarda yarım boy. §3.11: "önce bankalar" kolu reddedildi. Düzeltilmiş metin: "Tetikler (planın rejim anahtarı): XU100'ün 50 ve 200 günlük ortalamaların üstüne dönmesi, swap hariç net rezervin 3 hafta üst üste artması, 2 ay üst üste aylık TÜFE <%2, CDS <230 ve düşüyor, XBANK 200 günlüğün üstünde. Yabancı akımı sayılmaz. O zaman kırılım motoru tam boy ve 1x endeks/küme kolu; kredili işlem ve 1x üstü kaldıraç yok; sürprizsiz indirimden sonra bankalarda yarım boy." |
| 98 | "Çiftler, temettü öncesi spot, zorunlu satıcı olayları. Kırılımları da yalnız likit, VİOP'u olan ve fon tasfiyesi baskısı taşımayan hisselerde" | **DÜZELT** | PLAN_BIST §3.10 başlığı: "zorunlu akış alfası değil, kayıptan kaçınma"; rejimden bağımsız kol K5 (KAP teyitli özel durumlar). v_bist §3 m.5: zorunlu satıcı tezi n=1. §4.1: K4 evreni ilk 75 hisse; VİOP-47 öncelikli, diğerleri spot × 0,75. Düzeltilmiş metin: "Çiftler, temettü öncesi spot, KAP teyitli özel durumlar (ZPAT, satma hakkı). Kırılımları likit ilk 75 hissede (VİOP-47 öncelikli, diğerleri 0,75 boyla), fon tasfiyesi baskısı taşımayanlarda, küçük boyutla dene." |
| 99 | Fon payı / fiili dolaşım >%20; SPK suç duyurulu 13 hisse; liste planda | DOĞRU | v_profesyonel T6, T10; PLAN_BIST §4.2. |

## 7. §2 BIST planı özeti (satır 105–151); ölçüt PLAN_BIST.md

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 107 | Dosya yolları | DOĞRU | PLAN_BIST başlık; [SİN], [RUT]. |
| 108–110 | Taslaklar (trend/lider; rejim ve carry; önce risk), hakemler, C iskelet, iki çürütme | DOĞRU | taslak/bist_A, B, C başlıkları; PLAN_BIST başlık ("hakemlerin iki kez seçtiği C"), §12. |
| 116 | AÇIK: SMA200 13.572; risk %0,75; K7 T2'ye bağlı | DOĞRU | PLAN_BIST §2.1–2.2. |
| 117 | GEÇİŞ tanımı; 12.691; %0,5 | DOĞRU | PLAN_BIST §2.2 (rezerv "swap hariç net"; ekleme ve K7 yok). |
| 118 | KAPALI: 0/7; en çok 2 sonda, %0,25 | DOĞRU | PLAN_BIST §2.3. |
| 119 | KRİZ tetikleri | DOĞRU (küçük eksik) | PLAN_BIST §2.2: (d)'ye "ya da seviye < 0" eklenmeli. |
| 119 | "5 gün yeni giriş yok, açık pozisyonların stopu sıkılaşır" | **DÜZELT** | PLAN_BIST §2.2: "5 işlem günü yeni giriş yok; K6 kapanır; hedgesiz K3/K3b kapanır; K4, K5, K9 stopu = max(iz-stop, KRİZ günü kapanışı × 0,90); K1 sürer". Düzeltilmiş metin: "5 gün yeni giriş yok; K6 ve hedgesiz K3/K3b kapanır; K4, K5, K9 stopu KRİZ günü kapanışının en çok %10 altına çekilir; K1 sürer". |
| 121 | En erken GEÇİŞ 26.11; 12.11 rezerv → KRİZ (d) | DOĞRU | PLAN_BIST §2.3. |
| 127 | Çekirdek %15 / %85; hedef %60 / %40; 9/16/23/30.11 | DOĞRU | PLAN_BIST §0 m.2, §1.3. |
| 128 | "20 günlük oran z-skoru \|z\|≥2 olunca VİOP'ta ters spread, ertesi kapanışta giriş" | **DÜZELT** | PLAN_BIST K1: z son **60 günün** ortalaması ve standart sapmasıyla hesaplanıyor (L=60); 20, tutma süresi (H=20). Düzeltilmiş metin: "60 günlük oran z-skoru \|z\|≥2 olunca VİOP'ta ters spread, ertesi kapanışta giriş, 20 işlem günü tutulur". |
| 128 | Teminat faizli olmalı; komisyon ≤5 bps | DOĞRU | PLAN_BIST K1 kapıları ("bacak ve yön başına"). |
| 129 | K3: gün −6 al, gün −1 sat; +%0,2–0,5 | DOĞRU | PLAN_BIST K3. |
| 130 | "Duyuruda verimi ≥%5 olanı duyurunun ertesi kapanışında al, hak kullanımından önceki gün sat, XU030 vadelisiyle hedgele" | **DÜZELT** | PLAN_BIST K3b. Evren: 60 günlük medyan hacim ≥20 mn TL. Giriş: bildirim 17:00'den önceyse aynı gün, sonraysa ertesi gün. Hedge: yalnız Kural 0 sağlanırsa ve Σβ×nominal ≥ 1 kontrat ise; 1 mn TL'de genelde hedgesiz. Pilot boyu olay başına %1,25. Düzeltilmiş metin: "Verimi ≥%5 ve hacmi ≥20 mn TL olanı ilk bildirimden sonraki ilk kapanış seansında al (17:00'den önceyse aynı gün), hak kullanımından önceki gün sat; Kural 0 sağlanır ve tutar yeterse XU030 vadelisiyle hedgele". |
| 130 | +%6–7, ~27 gün, Şubat–Mayıs, 01.02.2027 pilot | DOĞRU | PLAN_BIST K3b. |
| 131 | K4 tetikleri: ENJSA 127,00; AHGAZ 48,70 / ENERY 14,60 tek isim; RYSAS 30,28 | DOĞRU | PLAN_BIST §4.4. |
| 132 | K5; AKCNS kapandı | DOĞRU | PLAN_BIST K5 (zorunlu tekliflerde kayıt tarihi kuralı yüzünden katkı ~0). |
| 133 | "Kapalı; brüt rezerv kapısı 160 mlr $ (şu an 158,1)" | **DÜZELT** (eksik) | PLAN_BIST K6 ve §4.4: 6 kapı koşulundan 3'ü sağlanmıyor (net rezerv −6,5, yabancı DİBS −750 mn $, brüt 158,1). En erken değerlendirme 19.11. Düzeltilmiş metin: "Kapalı: 6 kapı koşulundan 3'ü sağlanmıyor (net rezerv düşüşü, yabancı DİBS çıkışı, brüt rezerv 158,1 < 160 mlr $); en erken 19.11". |
| 134 | K7 kapalı | DOĞRU | PLAN_BIST K7. |
| 135 | "Tavan gün içinde ilk bozulduğunda sat; seri bitince alma" | **DÜZELT** | PLAN_BIST K8: "18:00'de son fiyat tavan değilse o günün kapanış seansında risk azaltan satış. Bu 'E kapanış satışı'dır, medyan +%38". Gün içi kural v_olay'ın ölçüsü (+%33); plan onu kullanmıyor. Düzeltilmiş metin: "Seri bozulduğu gün (18:00'de son fiyat tavan değilse) kapanış seansında sat (medyan +%38); seri bitince alma". |
| 135 | 8–22 bin TL | DOĞRU | PLAN_BIST K8. |
| 136 | K9: %0,25; −%1,5'te 6 ay | DOĞRU | PLAN_BIST K9 (KAPALI'da %0,25; GEÇİŞ ve AÇIK'ta %0,5). |
| 139 | "11–13.11 kapanışlarında K3, K4, K5 ve K9'da yeni giriş yok." | **DÜZELT** (eksik) | PLAN_BIST §0 m.8 ve §3.10 A1–A2: 11.11 kapanışında **hiçbir kolda** yeni giriş yok; 9.11'de bilançosunu açıklamamış isimlerde giriş yok. Düzeltilmiş metin: "11.11 kapanışında hiçbir kolda, 11–13.11 kapanışlarında K3, K4, K5 ve K9'da yeni giriş yok; 9.11'de bilançosunu 18:00'e kadar açıklamamış hisselere giriş yok." |
| 140–145 | Kredili esneklik (23.11 / 30.11), MSCI, 10.12 PPK → ~15.03.2027 yarım boy, dışlama | DOĞRU | PLAN_BIST §3.10 A3, A4, A7; §4.2. |
| 148 | +1…+2; −2…+5,5; ~%33–37 | DOĞRU | PLAN_BIST §0 m.10, §9.2. |
| 149 | Rejim dönerse +3…+8 | DOĞRU | PLAN_BIST §9.1, §9.4. |
| 150 | +10–20 puan için 3–5 kat risk, −%25…−%40 | DOĞRU | PLAN_BIST §0 m.12, §9.4. |

## 8. §3 ABD'de kazananlar (satır 159–211)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 160 | Jane Street ~39,6 mlr $ (basın) | DOĞRU | v_abd #1. |
| 161 | Virtu 2,44 mlr $, +%33,7 | DOĞRU | v_abd #3. |
| 162 | Citadel Securities ~12,2 mlr $ (doğrulanamadı) | DOĞRU (işaretli) | v_abd #2. |
| 163 | Spread %12,6 | DOĞRU | v_abd #10. |
| 165 | Pod getirileri; S&P +%16,4; çoğu altında | DOĞRU | v_abd #5. |
| 166 | "Arkasında 12x brüt kaldıraç ve pod başına %5–10'da mekanik risk kesme var." | **DÜZELT** (küçük) | abd_kim_kazaniyor §0 m.2 ve §2: 12x sektörün brüt kaldıracı (OFR, ikincil), net ~4,5x; pod başına ~%5 düşüşte risk kesme, %7,5–10'da tasfiye. Doğrulamada kontrol edilmedi. Düzeltilmiş metin: "Arkasında sektörde ~12x brüt (~4,5x net) kaldıraç ve pod başına ~%5 düşüşte risk kesme, %7,5–10'da tasfiye kuralı var." |
| 167 | Medallion +%76; RIEF −%22,6 | DOĞRU (küçük not) | v_abd #6: −%22,62 25 Aralık'a kadar; yıl sonu teyitsiz. "(25 Aralık'a kadar)" eklenmeli. |
| 168 | "sonra en kötü 12 ayını yaşadı (−%18'in üstünde)" | **DÜZELT** | v_abd #7: Nisan 2025'te 12 aylık kayıp −%18'i aşıyor; "en kötü" **doğrulanamadı**. Düzeltilmiş metin: "Nisan 2025'te 12 aylık kaybı −%18'i aştı ('en kötü' ifadesi doğrulanamadı)." |
| 168 | 2022 +%27,3; 2000'den beri %5,2 | DOĞRU | v_abd #7 (CAGR %5,23; tüm tarih MaxDD %20,61). |
| 173–176 | Tayvan %13 / <%1; Brezilya %97; 0DTE 358 bin $; SEBI %87,7 | DOĞRU | v_abd #8, #9, #11; v_capraz #23. 0DTE rakamı Mayıs 2022 sonrasına ait. |
| 177 | En iyi 500 günde 28 bps; toplam ~%5/yıl | DOĞRU | v_abd #8 (net 28,1 bps, day-trade portföyünde; toplam 2,0 bps/gün). |
| 179 | Luk 2024 +%283, 2025 +%970, 2026 9 ay +%786 | DOĞRU | v_abd #13; v_profesyonel A13. |
| 180 | J Law 1 mn $+ 2024 +%354, 2025 +%252 | DOĞRU | v_abd #14; abd_kim_kazaniyor §4. |
| 181 | Minervini 2021 +%335; Kell 2020 +%941; Sean Ryan 7/7, ~%81 | DOĞRU | v_abd #14 (+%6.232 toplam → ~%81/yıl). |
| 182 | Kârda biten: 2022 %8, 2026 %12–17 | DOĞRU | v_abd #14 (2022'nin 10 ayı 26/316; 2026 ilk yarı 115/688; 9 ay 85/712). |
| 182 | Luk −%27, bir başkası −%52 | DOĞRU | v_abd #14: 1.358,2 → 969,8 (−%26,6); Mikulka 960,4 → 409,6 (−%51,9). |
| 182 | Kullamägi 105 → ~45 mn $ (−%57) | DOĞRU | v_abd #16; v_profesyonel A2. |
| 183 | 700 kişi, %100 vol, medyan +%1.239 | DOĞRU (ajan hesabı) | seytan_taban_oranlar §0 m.6 [H]; v_capraz ayrıca kontrol etmedi. |
| 184 | FFTY 10 yılda %4,6/yıl, 2022 −%51 | DOĞRU | v_abd #17. |
| 188 | Risk %0,25–1; stop 1 ATR ya da %7–10 | DOĞRU | v_profesyonel A1; abd_profesyonel §0 m.1. |
| 189 | "İsabet %22–45, ortalama kazanç ortalama kaybın 2–5 katı. İşlem başına beklenti +0,4–0,6R." | **DÜZELT** | abd_kim_kazaniyor §0 m.8: isabet %22–35, kazanç/kayıp 3–5R. Üst sınır %45 ve alt sınır 2× Minervini'nin %44–63 / 2,15× rakamlarından; v_profesyonel A3'e göre **doğrulanamadı**. +0,4–0,6R için v_profesyonel eksik #10 "zayıf kanıt" diyor; Luk girdileri v_abd #15'e göre doğrulanamadı. Düzeltilmiş metin: "İsabet %22–35, ortalama kazanç ortalama kaybın 3–5 katı. İşlem başına beklenti tahmini +0,4–0,6R, ama zayıf kanıta dayanıyor (Minervini ve Luk'un işlem istatistikleri doğrulanamadı)." |
| 190–194 | Giriş tipleri, 3–5 günde 1/3–1/2, yalnız kazanana ekleme, Kullamägi %90, 4–8 pozisyon | DOĞRU | v_profesyonel A1, A2; abd_kim_kazaniyor §0 m.8. |
| 196 | Savor, George-Hwang, Moskowitz-Grinblatt; Bessembinder %4 | DOĞRU | abd_kim_kazaniyor §0 m.8; v_abd #29. |
| 196 | "Tekil hisse trend takibinin akademik testi yılda ~%15 brüt" | **DÜZELT** (atıf) | v_abd #18: Zarattini-Pagani-Wilcox uygulayıcı yazarlı çalışma kâğıdı. CAGR %15,19 brüt; maliyet varsayımı açıklanmamış. Düzeltilmiş metin: "Tekil hisse trend takibinin uygulayıcı yazarlı çalışma kâğıdı (Zarattini-Pagani-Wilcox) yılda ~%15 brüt buluyor". |
| 198 | Başlık "(kendi hesaplarımız)" | **DÜZELT** (atıf) | PEAD (Martineau), Pre-FOMC, S&P ekleme ve opsiyon satırları literatürden (v_abd #23–25; v_profesyonel A6). Düzeltilmiş metin: "(kendi hesaplarımız ve literatür)". |
| 202 | "212 yayımlanmış anomali (Chen-Zimmermann) \| Medyan ... %0,60/ay → ... %0,24 → 2010–25 likit evrende %0,13. Anlamlı kalan pay %16." | **DÜZELT** | İki set karışmış. 212 sinyal ve 0,60 / 0,24 / 0,13 medyanları abd_test §0 m.7'den; doğrulamada yeniden üretilmedi. "%16" abd_swing'in 165 sinyallik setinden; v_abd #22 bu seti yeniden üretti: ortalama 0,745 → 0,319 → 0,295 → likit 0,201; t>1,96 payı %16,4. Düzeltilmiş metin: "165 net yayımlanmış anomali (Chen-Zimmermann) \| Ortalama uzun-kısa getiri yayın öncesi %0,75/ay → yayın sonrası %0,32 → 2010 sonrası %0,30 → likit evrende %0,20. Anlamlı kalan pay %16." |
| 203 | UMD yılda %2,6–4, Sharpe 0,26 | DOĞRU | abd_test §0 m.4 (2010–26 UMD+RF %4,0, T-bill +2,6 puan, Sharpe 0,26). |
| 204 | PEAD 2006 / 2016 | DOĞRU | v_abd #23. |
| 205 | Reversal ~%0; VIX>25'te pozitif | DOĞRU | abd_test §0 m.9 (%0,1, t 0,04); abd_swing_kenarlar §2 (VIX>25'te +%0,55/ay, n=29). |
| 206 | Pre-FOMC, ekleme, spin-off, ay dönümü | DOĞRU | v_abd #24, #25; abd_swing_kenarlar §2. |
| 207 | "2010 sonrası risk ayarlı olarak piyasa düzeyinde, 2015 sonrası belirsiz" | **DÜZELT** (küçük) | v_abd §2.2: 2010–26'da top-5 Sharpe 0,86, piyasa 0,97; yani risk ayarlı olarak piyasanın altında. v_dalga §5 m.4: 2000 sonrası sınırda (t≈1,4). Düzeltilmiş metin: "2010 sonrası risk ayarlı olarak piyasanın biraz altında (Sharpe 0,86'ya karşı 0,97), 2015 sonrası belirsiz." |
| 208 | Straddle ~−%3/hafta; piyango call'ları −%35 | DOĞRU | v_profesyonel A6 (−%35,4, 7 günlük yüksek çarpıklıklı call'lar). |
| 209 | Skew t 5–6, revizyon, ardışık sürpriz; filtre | DOĞRU | abd_swing_kenarlar §5 (SmileSlope t 6,3 / 5,0); abd_test §0 m.8. |
| 211 | %15–25 bandı yalnız kaldıraçlı betayla; 2010–26 yılda %18–26 | DOĞRU | v_abd §2.1 (2x NDX lag1 %19,0; 3x lag0 %25,7); abd_test §0. |
| 211 | "Bedeli: en büyük düşüş −%55 ile −%97 arası" | **DÜZELT** | v_abd §2.1: 2x NDX 2010+ MaxDD **−%41**; v_abd §5: "−%40 ile −%97 arası". Düzeltilmiş metin: "Bedeli: en büyük düşüş −%41 (2x) ile −%97 (3x, tam dönem) arası". |
| 211 | 2000–02 3x −%89 | DOĞRU | v_abd §2.1 (lag0; bir gün gecikmeyle −%75,3). |
| 211 | "Filtre 2010–26'da getiriyi artırmadı, yalnız düşüşü kesti." | **DÜZELT** (küçük) | abd_test §0 m.1: 2010–26'da filtre getiriyi **düşürdü** (NDX 3x %35,6 → %24–26). Satır 217 de "getiriyi de kesti" diyor. Düzeltilmiş metin: "Filtre 2010–26'da getiriyi düşürdü (3x NDX'te %35,6'dan %24–26'ya), yalnız düşüşü kesti." |

## 9. §4 ABD planı özeti (satır 217–257); ölçüt PLAN_ABD.md

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 217 | Süreç; iskelet önce risk (C), mekanik lider momentumu (A); kaldıraçlı çekirdek reddedildi; Pine derlenmedi | DOĞRU | PLAN_ABD başlık, §2.7; taslak başlıkları. |
| 220–227 | Tek kol S1/S2; 16:45–17:15 BUY STOP-LIMIT + GTC SELL STOP; çıkışlar 00:30–01:00 ya da 08:00–09:00; 17:30–00:00 ekran yok; +2R ya da 4. seans ≥+1R; gölge kollar; opsiyon, margin, açığa satış, LETF yok | DOĞRU | PLAN_ABD §0 m.4–5, §3.5. |
| 229–234 | KIRMIZI; S&P +%0,4; VIX/VIX3M 1,10; 10<20; FTD yok | DOĞRU | PLAN_ABD §2.5. KIRMIZI'yı tek başına koşul (a) VIX/VIX3M ≥ 1,00 tetikliyor; diğerleri eksik SARI tetikleri. Bu ayrım eklenebilir. |
| 236 | 3 kapanış; Pazartesi yok; en erken 16.11; tek pozisyon; AI dışı | DOĞRU | PLAN_ABD §0 m.1–2, §2.6. |
| 239–240 | %10 (en çok %15); %40 USD/IBKR nakit; kalanı TL; USD'de %20 | DOĞRU | PLAN_ABD §0 m.3, §1.3. |
| 243–246 | %0,25; ≤%7,5; küme ≤%0,75; SARI %1,25 / YEŞİL %2,5; aylık %3; −%8; ihlal kuralı | DOĞRU | PLAN_ABD §0 m.6–7, §5.1. |
| 249–251 | IBKR Pro, 0,005 $, 11–13.11; Midas ≤500 $; PDT kalktı | DOĞRU | PLAN_ABD §6.1; v_capraz #15–16. PDT nakit hesaba zaten uygulanmıyor. |
| 253 | TL bazında, kur farkı dahil; zarar aynı yıl; TCMB kuru | DOĞRU | PLAN_ABD §1.1, §6.5. |
| 253 | "Aralıkta zarar realize ederek vergi düşürme ancak müşavir onayıyla." | **DÜZELT** | PLAN_ABD §6.5: Aralık'ın ilk haftası vergi kontrol noktası; yalnız vergi için çıkış yapılmaz. "Tek istisna **kazanç hasadıdır**": 2026 net TL sonucu < 0 ise kârdaki lotlar 30.12'ye kadar satılıp ertesi seans geri alınır; wash-sale benzeri kural olmadığı müşavirle yazılı teyit edilmeli. Zarar realizasyonu yalnız simetrik durumda ve müşavir onayıyla. 2026 zararı 2027'ye devretmez. Düzeltilmiş metin: "Aralık'ta yalnız vergi için çıkış yok. Tek istisna kazanç hasadı: 2026 net TL sonucu negatifse kârdaki lotlar en geç 30.12'de satılıp ertesi seans geri alınır (müşavirin yazılı teyidiyle); 2026 zararı 2027'ye devretmez." |
| 256 | Kenara göre −%2,5…+%6,5; TL'yi geçme olasılığı <%5 | DOĞRU | PLAN_ABD §0 m.9 (ağırlıklı merkez −%1,5…+%1,5). |
| 257 | 100 işlem, 12 ay, t ≥1,65 | DOĞRU, eksik | PLAN_ABD §8.3: EOD backtest şartı da var. |
| 257 | "O noktada risk işlem başına %0,5–1'e çıkar." | **DÜZELT** | PLAN_ABD §0 m.10 ve §8.3: Faz 3 kapısından sonra %0,75 (en çok %1). %0,5 Faz 2'nin riski (50 işlem, t ≥1,0). Dürüst merkez yine de ~%8–16. Düzeltilmiş metin: "100 işlem, 12 ay, t ≥1,65 ve hayatta kalma yanlılığından arındırılmış gün sonu backtest'i gerekiyor. O noktada risk işlem başına %0,75–1'e çıkar; dürüst merkez yine de yılda ~%8–16." |
| 257 | Üst dilimde %40+ | DOĞRU | PLAN_ABD §0 m.10 (üç şart, olasılık ~%7–10). |

## 10. §5 Ortak sonuç (satır 263–271)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 263 | 15–70 bps; %35–58 yayından sonra; BIST30 kenarları en hızlı sönen sınıf | DOĞRU | seytan_taban_oranlar §0 m.3, §2 m.2; v_capraz #24 (çalışma kâğıdı %35); v_abd #19 (JF %58). |
| 263 | "Hem BIST kırılım testinde hem ABD şampiyonlarında kârın çoğu en iyi %5–10'luk işlemlerden geliyor." | **DÜZELT** (atıf) | ABD şampiyonları için böyle bir istatistik yok; Luk'un işlem istatistikleri doğrulanamadı (v_abd #15). Kaynak ABD tekil hisse trend testi (v_abd #18: işlemlerin <%7'si kârın çoğu). Düzeltilmiş metin: "Hem BIST kırılım testinde (en iyi %5 işlem kârın ~%70'i) hem ABD tekil hisse trend testinde (işlemlerin <%7'si kârın çoğu) kâr az sayıda işlemden geliyor." |
| 264 | %31–38; %20–28; iki piyasada rejim kapalı | DOĞRU | v_capraz #4, #22; PLAN_BIST §2.3; PLAN_ABD §2.5. |
| 265 | Banka + holding + havacılık 0,77–0,79 | DOĞRU | v_dalga B12. |
| 265 | "ABD'de yarı iletken ve elektrik ekipmanı tek bahis (0,72)." | **DÜZELT** (işaret eksik) | v_profesyonel A14: **DOĞRULANAMADI** (ajan hesabı). Düzeltilmiş metin: "...tek bahis (0,72; ajan hesabı, doğrulanamadı)." |
| 265 | "Küme başına risk ≤%1,5, toplam açık risk rejime göre %3/%5/%6. Ay içi zarar ile açık risk toplamı %6'ya ulaşınca o ay yeni işlem yok." | **DÜZELT** | Kaynak abd_profesyonel §1.3 ve taslak/abd_A, B, C. İki nihai planda da yok. PLAN_ABD §5.1 (Faz 1): küme ısısı ≤%0,75, toplam açık risk SARI %1,25 / YEŞİL %2,5, aylık devre kesici %3. PLAN_BIST §5: küme başına 1/2/2 yönlü pozisyon, toplam açık stop riski %2,5 / %3,5 / %5,5, stres tavanı %6 / %8 / %10, aylık uydu kaybı −%2,5'te ay sonuna kadar giriş yok. Düzeltilmiş metin: "Planlarda: BIST'te küme başına 1 yönlü pozisyon (KAPALI), toplam açık stop riski %2,5/%3,5/%5,5 (KAPALI/GEÇİŞ/AÇIK), stres tavanı %6/%8/%10; ABD'de ilk 50 işlemde küme ısısı ≤%0,75, toplam açık risk SARI'da %1,25, YEŞİL'de %2,5, aylık devre kesici %3." |
| 266 | "Zorunlu satıcıların karşısında dur, ama hemen değil. ... Stres anında likidite sağlamanın primi var (reversal getirisi VIX ile artıyor). Yalnız akış bittikten sonra ve likit hisselerde." | **DÜZELT** | Nihai planlar bu ifadeyle çelişiyor. PLAN_BIST §3.10: "zorunlu akış alfası değil, kayıptan kaçınma"; A4: "düşen hisse dipten alınmaz". v_bist §3 m.5: tez n=1. bist_test §4: BIST'te kısa vadeli dönüş EW'ye göre −%17,9/yıl. VIX'li reversal primi yalnız ABD'de (abd_swing_kenarlar: VIX>25'te +%0,55/ay, n=29) ve PLAN_ABD'de yalnız gölge kol (G2). Düzeltilmiş metin: "**Zorunlu satıcılardan önce kaç; karşılarına geçmek henüz kanıtlı değil.** BIST'te zorunlu akış tezi tek gözleme dayanıyor ve kısa vadeli dönüş kaybettiriyor; planda MSCI, kredili tasfiye ve fon uyum takvimi kaçınma kuralı. ABD'de stres anında reversal primi var (VIX>25 aylarında +%0,55/ay, n=29), ama planda yalnız gölge kayıtta." |
| 267 | +0,2R ~390 işlem; Sharpe 1 → 4 yıl | DOĞRU | seytan_taban_oranlar §0 m.7 (SPRT medyan ~390, [H]); v_capraz #25 (16/4/1 yıl). |
| 269 | İlk 30–50 işlem küçük boyut | DOĞRU | PLAN_ABD Faz 1 (50 işlem). |

## 11. §6 ve Dosyalar (satır 277–308)

| Satır | İddia | Hüküm | Kaynak / düzeltme |
|---|---|---|---|
| 277 | Hepsi aleyhte | DOĞRU | v_bist §4. |
| 278 | Basit faiz; 2–8 puan altında | DOĞRU | v_bist §2.1. |
| 279 | Çiftler %30–45 küçüldü | DOĞRU | v_bist #25. |
| 280 | %23,3 → ~%29,3 | DOĞRU | v_profesyonel T12; PLAN_BIST §1.2 notu. |
| 281 | ABD sektör sıralaması abartılı; S&P eski veri | DOĞRU | v_abd #32, §3 m.1. |
| 282 | Küme rotasyonu kenarının ~yarısı seçimden | DOĞRU | v_dalga §2.2 (+12,6 → +6/+8). |
| 277–282 | Liste eksik | **DÜZELT** (ekleme önerisi) | Doğrulamada değişen ama listede olmayanlar: temettü +%8,5 → +%6,5 (v_olay); halka arz katılımcı primi medyan +%45 → +%33–38 (v_olay); Erdem −%0,281 → −%0,286 (v_capraz #23); "91 fondan 1" çerçevesi (v_profesyonel T1); TLY %89 → %81,6 (v_profesyonel T4); yabancı akımı "yok" → "zayıf" (v_olay). Eklenecek madde: "**Olay çalışmaları.** Yüksek verimli temettünün fazla getirisi muhafazakâr kıyasla +%8,5'ten +%6,5'e, halka arz katılımcı primi ileriye bakışsız kuralla medyan +%45'ten +%33–38'e indi." |
| 285 | Ortak web kotası 200 | DOĞRU | v_capraz, v_bist, v_abd §0. |
| 285 | "Doğrulayıcılar birincil kaynakları doğrudan indirerek çalıştı" | **DÜZELT** (küçük) | v_olay §1 ve v_dalga yöntem kısmı web araması kullandığını yazıyor; v_profesyonel "kendi aramam" diyor. Düzeltilmiş metin: "Doğrulayıcıların çoğu birincil kaynakları doğrudan indirerek çalıştı". |
| 286 | Yahoo sınırı, Stooq bot doğrulaması, TEFAS reddi; ABD hisse testi yok | DOĞRU | dalga_abd §1 (Stooq JS bot), abd_test §8 (Yahoo 429), tr_profesyonel §1 (TEFAS WAF), v_abd §4 m.2. |
| 287–290 | halkarz.com 403 / WebFetch; İş Yatırım ile doğrulama; kişi ve lot alanları KAP'tan alınmalı | DOĞRU | v_olay §0, §3 m.2. |
| 291 | Hayatta kalan yanlılığı | DOĞRU | v_bist §2.4. |
| 296 | "`ajanlar/`: 14 araştırma raporu." | **DÜZELT** | `ajanlar/` altında 16 dosya var; satır 297–299'daki liste de 16 ediyor (BIST 8, ABD 6, çapraz 2). Düzeltilmiş metin: "`ajanlar/`: 16 araştırma raporu." |
| 308 | Ham veri repoda yok | DOĞRU | `.gitignore` (*.parquet, *.pkl); hesaplar/ altında yalnız kod ve özet. |
