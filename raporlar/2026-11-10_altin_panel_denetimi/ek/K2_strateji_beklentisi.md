araç: 5/35

# K2: Altın sinyali yalnız F_TRALT + F_XAUUSD ile, bireysel maliyetle

## Özet
Sonuç: Bu uygulama geçmiş veriye göre para kazandırdığı kanıtlanmış bir yöntem değil. Bireysel maliyetle (TRALT 23, XAUUSD 10 bps gidiş-dönüş) üç ana kuralın hiçbiri önceden sabit "kazandırır" ölçütünü geçmedi.
- R1 (yalnız TRALT, hedge'siz, k=2): işlem başı net +11,5 bps, t = 0,58, işlemlerin %51'i kârlı. Yılda ~52 işlem.
- R2 (TRALT − b·ons altın): net +2,6 bps, t = 0,13. Ons altın hedge'i getiriyi neredeyse sıfırlıyor.
- R3a (yalnız ons altın, g'yi izle): net −1,8 bps, t = −0,23. Tersine girmek (R3b) −18,2 bps, t = −2,35.
- Sağlama kuralı A2 (XU030 hedge'li, kullanıcının aracı değil): düşük maliyetle net +43,2 bps, t = 2,55 yeniden üretildi. Bireysel maliyetle +23,9 bps, t = 1,41; yani kullanıcı XU030 bacağını da işlese bile geçmez.
- Kazanç zamana çok bağlı: 2021–23 üç yıl da zarar (R1 toplam −9.117 bps), 2019–20 ve 2024–26 kâr. En iyi %2 işlem çıkınca R1 −12,7 bps, R2 −17,4 bps olur: sonuç az sayıda büyük işleme bağlı.
- Beklenen yıllık sonuç (bootstrap, bireysel maliyet, 20 bin USD TRALT): R1 ortalama +1.117 USD, medyan +1.304 USD, %5–%95 aralığı −8.002 … +10.395 USD, zararlı yıl olasılığı %42. R2 ortalama +306 USD, aralık −8.662 … +9.157 USD, zarar olasılığı %50. Ortalamaların güven aralığı sıfırı kapsıyor.
- Risk: son 12 ayda F_TRALT 2 günlük getiri std'si 576 bps (20 bin USD'de ~1.152 USD); %1 kuyruk −1.344 bps (~−2.688 USD). İşlem 2 günde tek kontrat zinciriyle yapıldığından likidite sorun değil (günlük miktarın %0,13'ünden az).
- Gerçek örneklem dışı (05.11.2026 sonrası): 0 işlem. 04.11'de açılan işlem (z = 1,36) 06.11'de kapandı; 05.11 z = 1,03 ama pozisyon açıktı, 06.11 ve 09.11'de sinyal yok.

Not: Beklenti zayıf kanıtlı, güven DÜŞÜK. Altın rallisi dönemi (2024–26) kârı taşıyor; tek başına "her zaman long" taban (R1 için) bireysel maliyetle −17,5 bps/işlem.

## Tablolar (k=2, örtüşmesiz, bps; bireysel maliyet, parantez içi düşük maliyet net)
| Kural | n | yıl/işlem | brüt | net (düşük) | net bireysel | t | isabet | 19–20 | 21–23 | 24–26 | en iyi %2 çıkık | en kötü | maks. düşüş | taban | Geçti |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 TRALT | 408 | 52,4 | 34,5 | 26,5 | 11,5 | 0,58 | 0,51 | 52,6 | −66,5 | 49,9 | −12,7 | −1.820 | 10.999 | −17,5 | Kaldı |
| R2 TRALT−b·XAU | 399 | 51,2 | 31,9 | 22,0 | 2,6 | 0,13 | 0,51 | 33,7 | −70,9 | 45,8 | −17,4 | −1.683 | 12.270 | −22,9 | Kaldı |
| R3a XAU izle | 418 | 53,7 | 8,2 | 5,2 | −1,8 | −0,23 | 0,49 | 23,2 | −14,1 | −8,5 | −13,4 | −715 | 4.509 | −1,4 | Kaldı |
| R3b XAU ters | 418 | 53,7 | −8,2 | −11,2 | −18,2 | −2,35 | 0,45 | −43,2 | −5,9 | −11,5 | −27,0 | −844 | 8.266 | −1,4 | Kaldı |
| R3c XAU long taban | 973 | 124,9 | 8,6 | 5,6 | −1,4 | −0,28 | 0,49 | 5,4 | −12,5 | 5,7 | −10,5 | −1.606 | 6.539 | | |
| A1c TRALT long taban | 957 | 122,9 | 5,5 | −2,5 | −17,5 | −1,21 | 0,46 | −12,0 | −9,2 | −30,1 | −44,7 | −2.220 | 22.445 | | |
| A2 (sağlama, XU030) | 408 | 52,4 | 53,7 | 43,2 | 23,9 | 1,41 | 0,52 | 48,1 | −33,5 | 56,3 | 2,8 | −1.425 | 5.367 | −17,5 | Kaldı (t<2) |

Ölçüt kırılımı (bireysel): R1 t≥2 hayır; en iyi %2 sonrası > 0 hayır; rejim ≥2 pozitif evet; taban üstü evet. R2 aynı. R3a: t hayır, ex2 hayır, rejim hayır (yalnız 19–20 pozitif), taban hayır. Baseline R2 için hedge'li "her zaman long" (A3c). Long/short (bireysel net): R1 +11,1 / +12,1; R2 +2,9 / +2,3; R3a +5,4 / −10,8 (short n=185). Başabaş maliyet (işlem başı brüt): R1 34,5; R2 31,9; R3a 8,2 bps. Yıl başına net bps toplamı (bireysel): 
| Yıl | R1 | R2 | R3a | A2 |
|---|---|---|---|---|
| 2019 | 1.496 | 989 | 362 | −177 |
| 2020 | 4.394 | 2.486 | 2.264 | 5.567 |
| 2021 | −3.543 | −3.935 | −584 | −2.983 |
| 2022 | −3.189 | −3.179 | −697 | −523 |
| 2023 | −2.385 | −2.605 | −701 | −1.083 |
| 2024 | 1.551 | 1.395 | −68 | 1.943 |
| 2025 | −167 | −264 | −1.362 | 3.349 |
| 2026 (9.11'e) | 6.542 | 6.153 | 40 | 3.665 |

k=1 ve k=3 (bireysel net, t): R1 +6,0 (0,47) / +26,3 (0,85); R2 −1,8 (−0,15) / +9,3 (0,31); R3a −7,4 (−1,41) / +0,9 (0,09); A2 +11,2 (1,05) / +31,6 (1,25). Hiçbiri geçmedi.

Bootstrap (6 aylık blok, 5.000 tekrar, bireysel maliyet, yıllık; USD = 20 bin nominal)
| Kural / senaryo | ort. bps | medyan | %5 | %95 | ort. USD | %5 USD | %95 USD | zarar olas. |
|---|---|---|---|---|---|---|---|---|
| R1 tam | 559 | 652 | −4.001 | 5.198 | 1.117 | −8.002 | 10.395 | 0,42 |
| R1 2019–20 | 2.925 | 2.461 | 640 | 6.219 | 5.851 | 1.280 | 12.437 | 0,00 |
| R1 2021–23 | −3.025 | −3.189 | −5.980 | 91 | −6.049 | −11.960 | 181 | 0,92 |
| R1 2024–26 | 2.611 | 2.638 | −167 | 6.542 | 5.222 | −334 | 13.083 | 0,15 |
| R1 en iyi %2 çıkık | −623 | −341 | −4.185 | 2.183 | −1.246 | −8.370 | 4.366 | 0,58 |
| R2 tam | 153 | 62 | −4.331 | 4.579 | 306 | −8.662 | 9.157 | 0,50 |
| R2 2019–20 / 21–23 / 24–26 (USD ort.) | | | | | 3.456 / −6.487 / 4.862 | | | 0,20 / 0,97 / 0,22 |
| R2 en iyi %2 çıkık | −832 | −658 | −4.623 | 2.805 | −1.663 | −9.246 | 5.610 | 0,61 |
| R3a tam | −99 | −109 | −1.449 | 1.608 | −197 | −2.898 | 3.217 | 0,52 |
| R3a en iyi %2 çıkık | −688 | −673 | −2.352 | 836 | −1.376 | −4.703 | 1.673 | 0,78 |
| A2 tam | 1.232 | 1.236 | −2.440 | 5.274 | 2.463 | −4.879 | 10.548 | 0,34 |
| A2 en iyi %2 çıkık | 153 | 80 | −2.559 | 2.946 | 307 | −5.119 | 5.892 | 0,48 |
(R3a ve A2 ve R2 için kalan rejim senaryoları bootstrap.csv'de.) Rejim senaryolarında yalnız 4–6 yarıyıl var; güvenilirlik düşük.

Hedge kontratı (R2; son b = 1,09; son 12 ay medyan b = 0,85; ons altın 4.144,5 USD)
| Nominal | ons kontrat (son b / medyan b) | yuvarlama hatası |
|---|---|---|
| 10 bin | 2,63 → 3 / 2,06 → 2 | %14,1 / %2,8 |
| 20 bin | 5,26 → 5 / 4,12 → 4 | %4,9 / %2,8 |
| 30 bin | 7,89 → 8 / 6,17 → 6 | %1,4 / %2,8 |
(Yuvarlamanın P&L'ye etkisi simüle edilmedi.)

Risk, son 12 ay (bps; 20 bin USD)
| Araç, k | std bps | %1 | %5 | std USD | %1 USD | %5 USD |
|---|---|---|---|---|---|---|
| F_TRALT 1g | 392 | −1.023 | −680 | 784 | −2.047 | −1.361 |
| F_TRALT 2g | 576 | −1.344 | −930 | 1.152 | −2.688 | −1.859 |
| F_TRALT 3g | 727 | −1.458 | −1.127 | 1.454 | −2.916 | −2.253 |
| F_XAUUSD 1g | 177 | −482 | −289 | 353 | −964 | −579 |
| F_XAUUSD 2g | 251 | −655 | −352 | 502 | −1.310 | −705 |
| F_XAUUSD 3g | 292 | −1.033 | −429 | 584 | −2.067 | −857 |
Kilit günü (TRALT, |r| ≥ vekil eşik): 2020: 3, 2021: 4, 2022: 7, 2023: 5, 2024: 1, 2025: 3, 2026 (9.11'e): 6 (2019: 0). Likidite (son 12 ay medyan): TRALT hacim 1,36 milyar TL/gün, 284.279 kontrat, açık pozisyon 249.178; 10/20/30 bin USD = 123 / 246 / 369 kontrat (günlük miktarın %0,04–0,13'ü; USDTRY 50,23, F_TRALT 40,79). XAUUSD hacim 7,21 milyar TL, 35.096 kontrat, açık pozisyon 94.772; 10/20/30 bin USD = 2,4 / 4,8 / 7,2 kontrat (%0,007–0,02). XAUUSD taşıma (yıllık, son 12 ay medyan): %6,46; 2 gün ≈ 3,5 bps (yalnız bilgi).

Güncel durum (26.10–09.11.2026)
| Tarih | g % | z | TRALT r % | not |
|---|---|---|---|---|
| 26.10 | 0,76 | 0,43 | −1,14 | |
| 27.10 | 0,63 | 0,36 | −1,26 | |
| 28.10 | −0,06 | −0,03 | 1,81 | arife |
| 30.10 | −3,51 | −1,42 | −10,36 | kilit, giriş yok |
| 02.11 | 1,01 | 0,57 | 4,90 | |
| 03.11 | −0,47 | −0,27 | 0,06 | |
| 04.11 | 2,39 | 1,36 | 7,26 | giriş long |
| 05.11 | 1,81 | 1,03 | 2,13 | pozisyon açık, giriş yok |
| 06.11 | −1,50 | −0,85 | 0,78 | sinyal yok |
| 09.11 | 1,60 | 0,90 | 5,31 | sinyal yok |
04.11 long işlemi 06.11'de kapandı: R1 brüt +291 bps (bireysel net +268), R2 brüt +257 (net +224), A2 brüt +417. 05.11 sonrası giriş: 0.

## Sonuç defteri
| sonuç | dosya | sayı | güven |
|---|---|---|---|
| Sağlama A2 k=2 (min_periods=60) | hesap/K2/k2.log | n 408, net +43,2, t 2,55 | orta |
| R1 bireysel net | hesap/K2/metrikler.csv | +11,5 bps, t 0,58 | düşük |
| R2 bireysel net | metrikler.csv | +2,6 bps, t 0,13 | düşük |
| R3a bireysel net | metrikler.csv | −1,8 bps, t −0,23 | düşük |
| R3b (ters) bireysel | metrikler.csv | −18,2 bps, t −2,35 | düşük |
| R1 en iyi %2 çıkık | metrikler.csv | −12,7 bps | orta |
| R1 yıllık (20k USD) | bootstrap.csv | ort +1.117, %5 −8.002, %95 +10.395, zarar %42 | düşük |
| R2 yıllık (20k USD) | bootstrap.csv | ort +306, zarar %50 | düşük |
| 2021–23 R1 | bootstrap.csv | ort −6.049 USD/yıl, zarar %92 | orta |
| Hedge kontratı | hedge_kontrat.csv | 20k: 5,26 (b=1,09), hata %4,9 | orta |
| Risk 12 ay | risk_12ay.csv | TRALT 2g std 576 bps | orta |
| Kilit günleri | kilit_gunleri.csv | 2026: 6 | orta |
| Likidite | likidite.csv | 20k = 246 TRALT kontrat, %0,09 | yüksek |
| Taşıma | k2.log | %6,46 yıllık | orta |
| Güncel | guncel_gunler.csv, guncel_islem_*.csv | 05.11 sonrası 0 işlem | yüksek |
| İşlem listeleri | islemler_k2_tralt.csv, islemler_k2_xau.csv | k=2 | |

## Şartnameden sapmalar
- Sağlama: σ250 ve β/b için tam 250 gün şartı n=360 verdi (beklenen 405–423 dışında). min_periods = 60 gözlem (pencere 250) ile n=408, net +43,2, t 2,55 (t beklenen 2,2–2,5'in biraz üstünde); aralık sağlandığı için tüm analiz bu ayarla (ilk geçerli z: 25.01.2019). Aşamalı taramada 30→n 414, 90→n 400.
- Örtüşmesiz: çıkış gününde yeni giriş serbest (idx ≥ çıkış). "Katı" varyant (çıkıştan bir gün sonra) n'yi 300–326'ya indiriyordu; sağlamada kullanılmadı.
- Taban "her zaman long": k=2 günde bir değil, aynı filtreler altında örtüşmesiz ardışık (n≈957–973); R2 için hedge'li long (A3c) taban alındı.
- A2 bireysel maliyeti: XU030 bacağı β×8 bps varsayıldı. t değerleri basit (örtüşmesiz olduğundan Newey–West kullanılmadı). Bootstrap A2 dahil bireysel maliyetle.
- Kilitli çıkışta çıkış en çok 3 gün ertelendi. Rejim bootstrap'inde yarıyıl sayısı 4–6.

## Yaptığım ileriye bakma kontrolleri
- σ250, β ve b hepsi 1 gün geciktirilmiş (shift(1)); rolling pencereler yalnız geçmiş.
- Sinyal g, aynı gün F_XAUUSD uzlaşma getirisi; giriş de aynı uzlaşmada: uzlaşma ~18:00 TSİ'de oluştuğu için karar anı (17:55) ile küçük bir ileriye bakma payı var (şartnamenin bilinen vekili). Gerçek uygulamada fiyat, sinyal anındaki fiyattan sapabilir; bu sapma ölçülmedi.
- Önceki uzlaşma düzeltmesi bültenden; ön vade yalnızca girişteki vadeye kalan gün sayısından seçildi, kontrat sonradan değiştirilmedi.
- Kilit/arife/sıfır işlem filtresi girişte bilinen bilgiden (o günkü r ve miktar; kilit vekili o günkü r'yi kullanır, bu da gün sonu bilgisi, uygulamada uzlaşma ile eşzamanlı). Çıkış ertelemesi çıkış günü r'sine dayanır ve tüm sonuçlarda aynıdır.
- Güncel işlemlerde sonuç bilinmeyen gün NaN bırakıldı. Yeni örneklem dışı için ayrı doğrulama yok.

## Açık kalanlar
- Yuvarlanmış tam sayı kontratla P&L simülasyonu yapılmadı.
- Plasebo/kaydırma ve ek rejim bootstrap sonuçlarının tamamı raporda yok (bootstrap.csv'de).
- Hedge b ve β'nın kararlılığı, XU030 ile TRALT arasındaki vade farkları ve kilit gününde gerçekleşebilir fiyat (limit) ayrıca test edilmedi.
- Gerçek maliyet tahmini (23/10 bps) kullanıcı beyanı; fiyat kayması (slippage) eklenmedi.
