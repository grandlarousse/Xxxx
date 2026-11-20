araç: 26/40

**Özet (A7 — aday üretmez; T3 = keşif)**

Dönem 2023-12-21 → 2025-06-30 (378 gün, 36 XELKT üyesi + 4 komşu), tek dönem + iki kronolojik yarı. panel_full ve raw açılmadı, veri indirilmedi.

SAPMA / veri sınırı: panel_dev'de hisselerin 5 dk verisi yok; snap'teki `p_1750` gerçekte 17:30 fiyatı. Hisselerde iki sınır ölçtüm: 17:30 (alt) ve 18:00 son sürekli işlem fiyatı (üst; yalnız yaz saati ayları, 197 gün). Gerçek 17:50 yalnız XELKT endeksinde var (5 dk, 2017–2025/06). "Son 10 dakika" kilit ölçümü de bu yüzden 17:30 ve 18:00 noktalarıyla yapıldı.

Veri kusuru (D2, yeni bulgu): Yahoo gün içi fiyatları nakit temettü için de küçültülmüş; hisse-günlerin %21'inde snap fiyatı medyan 8 bps düşük (AKFYE, NATEN, TATEN, ESEN, MAGEN bütün dönem). `vekil.yahoo_artik()` ile düzelttim. Düzeltilmeden "17:30'da tavanda" oranı %49 çıkıyordu, düzeltince %69.

T1: Beklentin (%85–95 yakalama) hisselerde tutmuyor. |r| ≥ %3 sinyalinde 17:30'da yakalama 0,75 / kesinlik 0,87; 18:00'de 0,89 / 0,95. XELKT'de gerçek 17:50: 0,88 / 0,93. Hisseler için 17:50 tahmini %83–87 (XELKT'den ara değer; doğrulanmadı). Eşiğe uzaklık belirleyici: 17:30'da eşiğin ≥ 100 bps üstündeki sinyalin %96'sı kapanışta da geçerli, 0–25 bps üstündekinin %63'ü.

T2: 17:30 → kapanış medyan |sapma| 40 bps (%95'lik 180); salt kapanış seansı (18:00 son → kapanış) medyan 18 bps (%95'lik 86). Tavan kilidi bozulmuyor (17:30'da tavanda olanın %98'i tavanda kapanır) ama geç oluşuyor: tavan kapanışlarının %31'i 17:30'dan sonra, yalnız %5'i kapanış seansında. Kapanış seansı hacmi günlük hacmin yaklaşık %2,5–4,5'i (dolaylı tahmin); E9'daki %1 günlük hacim sınırı kapanış seansının medyan %27'si ediyor, büyük.

T3 (keşif, 35 test, BH q=0,10'dan 5'i geçti): XU030 son saat → sektör sepeti ertesi gün gün içi pozitif (t=3,5) ama 2017–2022'de yok (t=0,15). Kapanış seansı göreli sapmasının %13'ü ertesi gece geri dönüyor (t=−4,0; uç beşte birlik farkı −12,5 bps): maliyetin altında, sinyal değil dolum uyarısı.

Araç: `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a7_gunici/vekil.py`. Her gün yalnız o günün kapanışa bağlı girdilerini değiştirip `build()`'i yeniden çağırır. Öz-denetim (vekil = kapanış) %100 örtüşüyor; 378 gün × 5 kural 8,5 sn. Kör protokol gereği A4/A5/A6 kurallarını çalıştırmadım; yalnız kendi örnek kurallarımla ve `--kor` (getirisiz) kipte sınadım.

3. dalga kullanımı: `python3 -I vekil.py <panel_full> ../a4_olay/rules.py --bas 2025-07-01 --cikti a4_vekil.csv` (5 dk'lı son ~60 günde gerçek 17:50; öncesi 17:30. `--nokta p_son` üst sınır).

**İddia defteri** (yollar `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/` altında)

iddia | dosya yolu | sayı | güven
--- | --- | --- | ---
Hisse havuzu 17:30 vekili, r_cc ile korelasyon | ek/a7_vekil_tablosu.csv (HAVUZ, 1730, tum) | 0,941; medyan fark 39 bps; n=11.674 | yüksek
Hisse havuzu 18:00 son fiyat, korelasyon | ek/a7_vekil_tablosu.csv (HAVUZ, 1800son) | 0,988; medyan fark 17 bps; n=6.115 | yüksek
\|r\| ≥ %3, 17:30: yakalama / kesinlik | aynı (abs3) | 0,75 / 0,87 (2.702 gerçek sinyal) | yüksek
\|r\| ≥ %5, 17:30: yakalama / kesinlik | aynı (abs5) | 0,75 / 0,86 (980) | yüksek
\|r\| ≥ %3, 18:00: yakalama / kesinlik | aynı (1800son, abs3) | 0,89 / 0,95 (1.440) | yüksek
z ≥ 1 / 1,5 / 2 yakalama, 17:30 | aynı (absz1, absz1.5, absz2) | 0,75 / 0,73 / 0,76; kesinlik 0,87 / 0,86 / 0,86 | yüksek
z ≥ 2, 18:00 | aynı | 0,90 / 0,95 | yüksek
İki yarı, abs3 yakalama 17:30 | aynı (yari1, yari2) | 0,77 / 0,74 | yüksek
Hisse bazında abs3 yakalama aralığı, 17:30 | aynı (tur=hisse) | min 0,61, medyan 0,76, max 0,93 | orta (hisse başına az olay)
AKSEN / ENJSA / ODAS abs3 yakalama, 17:30 | aynı | 0,79 / 0,61 / 0,74 | orta
XELKT gerçek 17:50, 2017–2025/06 | aynı (XELKT, 1750, uzun) | korelasyon 0,986; abs3 0,88 / 0,93; z≥2 0,86 / 0,94; n=2.125 | yüksek
XELKT 17:30, aynı dönem | aynı (XELKT, 1730, uzun) | korelasyon 0,967; abs3 0,75 / 0,86 | yüksek
XU030 17:00 değeri, 2017–2025/06 | aynı (XU030, 1700, uzun) | korelasyon 0,925; abs3 0,58 / 0,86 | yüksek
Sektör sepeti 17:30 | aynı (SEPET, 1730) | korelasyon 0,978; abs3 0,76 / 0,76 (21 olay) | düşük (az olay)
Tavan kapanışı sinyali, 17:30: yakalama / kesinlik | aynı (tavan) | 0,69 / 0,98 (209); 18:00: 0,95 / 0,98 (121) | yüksek
Taban kapanışı sinyali, 17:30 | aynı (taban) | 0,73 / 0,85 (71) | orta
Eşik bandı: 17:30'da %3 eşiğinin 0–25 bps üstü → kapanışta geçerli | ek/a7_vekil_tablosu_bant.csv | %63 (n=331); 50–100 bps %83; ≥100 bps %96 (n=1.377) | yüksek
17:30 → kapanış sapması, kilitsiz havuz | ek/a7_kapanis_sapma.csv (HAVUZ, 1730) | medyan \|.\| 40 bps; %95'lik 180; %16'sı > 100 bps; n=11.394 | yüksek
18:00 son → kapanış sapması | ek/a7_kapanis_sapma.csv (HAVUZ, 1800son) | medyan 18 bps; %95'lik 86; %3,5'i > 100 bps; adım ≈ 8 bps | yüksek
AKSEN / ENJSA / ODAS kapanış seansı sapması | aynı | medyan 21 / 22 / 20 bps | yüksek
Tavan kilidi 17:30'dan sonra oluşma | ek/a7_kilit_gecis.csv | 64/209 (%31); kapanış seansında 6/121 (%5) | yüksek
Tavan kilidi bozulma | aynı | 3/148 (%2) | yüksek
Taban kilidi: sonradan oluşan / bozulan | aynı | 19/71 (%27) / 9/61 (%15) | orta
17:30'da tavanda değil, getirisi +%7–9 → tavanda kapanma | ek/a7_kilit_riski.csv | %22 (22/101); ≥ +%9: %56 (19/34); +%5–7: %3 | orta
Kapanış seansı hacim payı (üye medyanı) | ek/a7_kapanis_hacim.csv | %3,7 (kış tahmini %2,9, yaz %4,3, geçiş günleri doğrudan ≈ %2,5); ≈ 2,4 mn TL | düşük–orta (dolaylı)
E9 %1 sınırının kapanış seansına oranı | aynı | medyan %27; AKSEN %16, ENJSA %24, ODAS %22 | düşük–orta
17:50'ye kadar oluşan hacim payı (vekil.py varsayılanı 0,92) | aynı (hacim_payi_1750) | medyan 0,936 | düşük–orta
XU030 17:00→kapanış → sepet f1 (keşif) | ek/a7_kesif.csv | katsayı 0,48, t=3,53; oc1 t=3,27; co1 t=1,28; IS 2017–22 t=0,15; 2023–25/06 t=2,03 | orta (dönemsel)
Kapanış seansı göreli sapması → ertesi gece (keşif) | ek/a7_kesif.csv (kapanis_sapma_1800son_goreli, hisse_co1) | −0,13, t=−3,98; beşte birlik farkı −12,5 bps (t=−3,75); yarılar −13,6 / −10,9 | orta
Yahoo artık temettü çarpanı | kod/a7_gunici/vekil.py (yahoo_artik) | hisse-günlerin %21'i; medyan çarpan 0,99917 | yüksek

**açık kalanlar**

- Hisselerde gerçek 17:50 ölçülmedi (5 dk veri yalnız kasa döneminin son ~60 gününde). 3. dalgada `t1_vekil_tablosu.py` ve `vekil.py` panel_full'da çalıştırılırsa doğrudan ölçülür; %83–87 şimdilik tahmin.
- "Son 10 dakika" kilit geçişi de aynı nedenle 17:30 / 18:00 noktalarıyla verildi.
- Kapanış seansı hacmi doğrudan gözlenmiyor (barlarda yok); pay iki mevsimin farkından çıkarıldı. Borsa'nın seans bazlı hacim verisiyle doğrulanmalı.
- VİOP: gün içi vadeli verisi yok; `vekil.py` uzlaşmayı vekilleyemiyor. A6 kuralları için araç iyimser sonuç verir ve bunu `vekilsiz_girdi` sütununda bildirir.
- D2 kusuru panelde duruyor: snap'i doğrudan okuyan başka kod varsa düzeltmeyi `vekil.snap_fiyat()` üzerinden almalı. T1/T2'nin önceki (düzeltmesiz) çalıştırmasında tavan sayıları farklıydı; teslim edilen dosyalar düzeltilmiş hâldir.
- A4/A5/A6 kuralları kör protokol nedeniyle vekil aracından geçirilmedi; araç yalnız `ornek_rules.py` ile sınandı (yakalama 0,77–0,88, kesinlik 0,83–0,99; `ek/a7_vekil_ornek.csv`).
- `--mod hizli` çok günlük getiri ya da yürüyen std kullanan kurallarda yanlış (örnekte yakalama 0,88 yerine 0,75); varsayılan `tam` kullanılmalı.
- T3'teki XU030 son saat etkisi IS'te (2017–2022) yok; kasada sınanacaksa keşif etiketiyle ve tek kural olarak.
- Not uzunluğu: `ek/a7_gunici.md` tablo dahil yaklaşık 625 kelime (gövde 600 altı).