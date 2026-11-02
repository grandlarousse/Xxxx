# v_banka_holding — Banka ve holding iddialarının bağımsız doğrulaması (B1, B3, B4, B5, B7, H1, H2, H3)
Doğrulayıcı: v_banka_holding · Tarih: 02.11.2026 · Veri: 30.10.2026 kapanışına kadar
Kod: `out/code_v_banka_holding/`. Dosyalar: `vb.py` (kendi kütüphanem; ll.py import edilmedi), `01_sync.py`, `02_hourly.py`, `03_scan.py`, `04_placebo.py`. Sonuçlar `res/`, loglar `res_log0*.txt`.
Kısaltmalar: pc = XU100 kontrollü kısmi korelasyon. t = Newey-West(5). Tam dönem = 2010–2026. IS = 2014–2020. OOS = 2021–10.2026. 3y = son 3 yıl. 1y = 31.10.2025–30.10.2026.

## 0. Önce: ortak veri sorunu (bütün ajanları ilgilendiriyor)
**Yahoo '=X' FX serilerinin zaman damgası kuralı 04.08.2010'da değişiyor.** `ll.FX_FIX` serinin tamamını bir gün kaydırıyor. Bu kaydırma yalnızca 04.08.2010 ve sonrası için doğru.
- 04.08.2010'dan önce: ldate=d satırı d gününün kapanışını gösteriyor (~23:00 UTC). Kaydırma yapılmamalı.
- 04.08.2010 ve sonrası: satır d günü 00:00 UTC fiyatı, yani bir önceki günün sonu. Kaydırma gerekli.
- Kanıt (`res_log` ve 2010 günlük tablosu):
  - FXE ile EURUSD=X arasında aynı gün korelasyonu 2010-07'de +0,99, 2010-08'de +0,29. Ertesi gün korelasyonu 2010-08'de +0,93.
  - EZA/ZAR ve EWZ/BRL çiftlerinde de aynı kırılma görülüyor.
  - XU100 ile USDTRY: 2005–2009'da kaydırılmamış seride lag0 korelasyonu −0,35…−0,63. Kaydırılmış seride lag0 +0,04…+0,11, yani yanlış hizalı.
  - 03.08 ve 04.08.2010 satırları aynı fiyatı taşıyor; geçiş günü tekrarı.
- Uyguladığım düzeltme (`vb.fx_align`, FXMODE='fix2'): 2010-08-04 öncesi kaydırılmadı, sonrası 1 satır kaydırıldı.
- Etkisi:
  - 2010+ iddialarında küçük (yalnız 2010'un ilk 7 ayı etkileniyor).
  - **2005–2010 dönemini kullanan bütün FX sonuçları ll.FX_FIX ile hatalı.** Örnek: ENKAI–USDTRY pc 2005+ fix1 ile 0,038, fix2 ile 0,093. 2005–09'daki "negatif pc" bir artefakttı. AKBNK–USDTRY pc 2005+ fix1 ile −0,108, fix2 ile −0,031.
  - **Koordinatöre öneri:** ll.FX_FIX'e 2010-08-04 kırılmasını ekleyin ve 2005–2010 dönemini kullanan FX bulgularını yeniden çalıştırın.
- İkinci FX notu: 2024+ saatlik veriyle 15:00 UTC USDTRY'yi günlük kaydırılmış seriyle karşılaştırdım. İki getiri arasındaki korelasyon yalnız 0,63. Günlük FX, BIST penceresinin gürültülü bir vekili. Bu yüzden günlük pc'ler mutlak değerce biraz küçülüyor; işaretler ise değişmiyor (aşağıda).

## 1. Özet tablo
| İddia | Bağımsız sonuç | Karar | Güven (eski → yeni) |
|---|---|---|---|
| B1 TUR 15:30 UTC→ABD kapanışı → XBANK gap (t+1) | corr **0,362** (t 7,0; n 697); yarılar 0,36/0,37; gün-içi −0,002; günlük vekil 2014–26'da 13/13 yıl + | KABUL | YÜKSEK → YÜKSEK (yalnız gap; spotta işlenemez; büyük kısmı piyasa) |
| B3 ES 15:00→06:00 UTC → banka gap | XBANK **0,474** (t 5,7; n 567); GARAN 0,52, AKBNK 0,46; gün-içi ≈0 | KABUL | YÜKSEK → YÜKSEK (gap; işlenemez) |
| B4 USDTRY → banka-özgü negatif | XBANK pc **−0,157** (t −6,5); IS −0,207 / OOS −0,125; 3y −0,055, 1y −0,045 (anlamsız); **pc yılların 12/17'sinde negatif** (ham corr 17/17) | DÜZELT | YÜKSEK → **ORTA** (tam dönem); güncel DÜŞÜK |
| B5 2026 banka ↔ Brent/SAN/EMB/BBVA | pc −0,289 / +0,284 / +0,260 / +0,226 (birebir tuttu); 2021–24 ≈0; **dört sürücü tek faktör (petrol şoku rotasyonu)** | DÜZELT (yorum) | DÜŞÜK → DÜŞÜK |
| B7 BBVA ↔ GARAN | pc **+0,022** (t 1,2); IS −0,02 / OOS +0,04; 2026 1y +0,27 ama SAN.MC de +0,31 (ortak faktör) | KABUL | DÜŞÜK → ÇOK DÜŞÜK (özgü bağ yok) |
| H1 SAHOL–AKBNK | pc **0,243** (t 10,8); IS 0,244 / OOS 0,352; 1y 0,53; 14/17 yıl +; banka sepeti (AKBNK hariç) kontrolüyle 0,183 | KABUL | YÜKSEK → YÜKSEK (2017 öncesi ≈0; büyük kısmı SAHOL↔özel banka faktörü) |
| H2 KCHOL–ARCLK/FROTO/YKBNK/TOASO/TUPRS | 0,157 / 0,152 / 0,122 / 0,120 / 0,117; plasebo: 46 hisse içinde sıra 2–6 (grup dışı medyan −0,018, p90 0,045) | DÜZELT (hisse bazında) | YÜKSEK → ARCLK, FROTO, TOASO YÜKSEK; **TUPRS, YKBNK ORTA** |
| H3 ENKAI–USDTRY | pc **+0,094** (t 5,3); IS 0,101 / OOS 0,087; 14/17 yıl +; **3y 0,017, 1y 0,049 (anlamsız)**; 47 hisse içinde 1. sırada | DÜZELT (güncellik notu) | ORTA → ORTA (tam dönem); güncel DÜŞÜK |

## 2. Ayrıntılar

### B1 — TUR, BIST kapanışından sonra
- **Zamanlama:** TUR saatlik barları :30'da başlıyor. Başlangıç fiyatı = 14:30 barının kapanışı, yani **15:30 UTC** (BIST kapanışından 30 dk sonra; temiz pencere). Bitiş = günün son ABD barı.
  - İddiada "15:00→" yazıyor ama ölçüm aslında 15:30'dan.
  - 14:30 başlangıcı kullanılırsa (BIST kapanışından önceki 30 dk dahil, kirli pencere) corr 0,307'ye düşüyor. Doğal; pencerede BIST'in zaten fiyatladığı bilgi var.
- **Sonuçlar (XBANK gap):**
  - corr 0,362 (t 7,0), beta 0,97.
  - Günlük kapanışla 0,363. Tatilleri içeren tam pencereyle 0,376.
  - Bankalar: GARAN 0,38, AKBNK 0,35, YKBNK 0,34, ISCTR 0,34, VAKBN 0,33, HALKB 0,25. XU100 gap 0,33.
- **Bankaya özgü kısım küçük:** XU100 gap kontrolüyle pc 0,150 (t 2,2; 1. yarı 0,09). Yani etki esas olarak piyasa gap'i.
- **Gün-içi:**
  - corr −0,002. Kendi gap'i kontrolüyle +0,007.
  - Üst %20 sinyal günlerinde sign×intra −4,6 bps (t −0,25).
  - Basit backtest (10 bps maliyet): −0,9 bps/gün (brüt +9,1).
  - XU100 gün-içi kontrolüyle pc −0,067 (t −1,9; 2. yarı −0,15, t −3,0). Bankalar gün içinde piyasaya göre hafif geri veriyor olabilir. Bu bir hipotez (ÇOK DÜŞÜK): FDR uygulanmadı, yalnız bir yarıda var.
- **Uzun örneklem (günlük vekil, 2014–2026):** XBANK gap_{t+1} ~ TUR_t, XU100_t ve XBANK_t kontrollü.
  - pc 0,217 (t 8,0), IS 0,27 / OOS 0,19, **13/13 yıl pozitif**.
  - Gün-içi pc −0,026 (t −1,1).
  - Böylece YÜKSEK etiketinin "yıl" ve "IS/OOS" koşulu da sağlanıyor.
- **ES ile örtüşme:** ES gecesi kontrol edilince TUR'un pc'si 0,18'e iniyor. ES, TUR kontrol edilince 0,33'te kalıyor. TUR'un ek bilgisi sınırlı.

### B3 — ES gece 15:00→06:00 UTC
- XBANK gap 0,474 (t 5,7 NW; iddia 0,49 ve t 7,2; iddiadaki t muhtemelen OLS). Yarılar 0,46/0,53. Gün-içi −0,001.
- **Bileşenler:**
  - 15→20 UTC (ABD seansı) corr 0,25.
  - **20→06 UTC (Asya gecesi) 0,46.**
  - 06→07 UTC (pencere sonrası, açılış öncesi) 0,07.
- **Bankaya özgü:** XU100 gap kontrolüyle 0,169 (t 2,0; 1. yarı 0,07).
- **Uzun vekil:** ES günlük → gap pc 0,123, 13/13 yıl pozitif. Gün-içi pc −0,041 (t −2,0): zayıf geri dönüş eğilimi, test edilmedi.
- **Backtest** (sign × intra, 10 bps): −0,3 bps. İşlenebilir değil.
- VİOP akşam seansı (XLBNK/XU030) test edilemedi; veri yok.

### B4 — USDTRY (bankaya özgü)
- **Ana sonuçlar (fix2):**
  - XBANK pc −0,157 (t −6,5). XU100+EEM+ES kontrolüyle −0,155. Lag'ler eklenince −0,155. EM/ABD faktörü açıklamıyor.
  - IS −0,207 (iddia −0,18), OOS −0,125 (iddia −0,15), 3y −0,055 (t −1,2), 1y −0,045 (t −0,7).
- **Yıllık pc:**
  - 2014 −0,14 · 2017 −0,12 · 2018 −0,34 · 2020 −0,33 · 2021 −0,22 · 2023 −0,24 · 2024 −0,12.
  - ≈0 olan yıllar: 2010–13, 2015–16, 2019, 2022, 2025 (+0,01), 2026 (−0,03).
  - Negatif yıl sayısı 12/17 (%71 < %75). "Her yıl negatif" ifadesi yalnız **ham** korelasyon için doğru; ham korelasyon büyük ölçüde piyasa kanalı.
  - 2005–2009 (fix2 ile): pc ≈0 veya pozitif (2006 +0,25).
- **Saatlik 15:00 UTC FX (2024-01+):** XBANK pc −0,058 (t −1,5). Günlük seride −0,042. Son dönemdeki zayıflık zamanlama hatasından değil.
- **Bankalar tek tek (tam dönem):** GARAN −0,137, VAKBN −0,120, AKBNK −0,115, YKBNK −0,112, ISCTR −0,096, HALKB −0,092, TSKB −0,044.
- **Ayna etki:** XUSIN pc +0,109 (t 5,2). Bu bir banka↔sanayi (ihracatçı) TL rotasyonu. 47 hisse içinde en negatif olanlar bankalar ve SAHOL.
- **Yeni etiket:** ORTA. Tam dönemde anlamlı ve OOS'ta aynı işaret, ama dönemsel. Kur krizlerinde güçlü, 2025–26'da sıfır.

### B5 — 2026 rejimi
- **Rakamlar birebir:** XBANK pc Brent −0,289 (t −5,3), SAN.MC +0,284, EMB +0,260, BBVA.MC +0,226. 2021–24 ≈0, 2025 ≈0 (EMB +0,11).
  - XU100+TRY+EEM kontrolüyle: −0,254 / +0,255 / +0,195 / +0,204.
  - ES de eklenince: −0,244 / +0,243 / +0,176 / +0,189.
  - Pencere yarıları (11/25–04/26, 05–10/26): Brent −0,27/−0,26, SAN +0,25/+0,30.
  - Lag1 ≈0, yani senkron.
  - En büyük 10 gün çıkarılınca Brent −0,25 kalıyor; SAN 0,16'ya iniyor.
- **Tek faktör:**
  - XU100 artıkları arasında BZ–SAN −0,50, SAN–BBVA +0,83, BZ–EMB −0,45.
  - Dördü aynı regresyona konunca: BZ t −2,0, SAN 1,7, EMB 2,0, BBVA 0,1.
- **Seçim yanlılığı ve null taraması (03_scan):** 1.001 BIST dışı sürücü, 15 adet 12 aylık pencere.
  - Son pencerede |pc|>0,20 olan sürücü **86 tane**. Önceki 14 pencerede bu sayı 0–16.
  - Son pencerede medyan |pc| 0,078; diğer pencerelerde 0,03–0,06.
  - En yüksekler: GSG −0,31, IAG.L +0,30, RYA.IR +0,30, DBC −0,30, RB=F −0,30, TUI1.DE +0,30. Yani emtia/petrol ve Avrupa havayolu/turizm.
  - İddiadaki sürücülerin sırası: BZ 8., SAN 9., EMB 21., BBVA 43.
  - Bağımsız null'da |pc|>0,226 için beklenen sayı 0,38; gözlenen 43. Fakat testler bağımsız değil; tek bir faktör var.
- **BIST içi kompozisyon:**
  - Brent ile pc: TAVHL −0,41, PGSUS −0,40, THYAO −0,33, SAHOL −0,29, bankalar −0,25…−0,29.
  - Ters yönde: TUPRS +0,45, PETKM +0,40, XUSIN +0,27, ASELS +0,17.
  - XU100+TUPRS+ASELS+THYAO kontrolüyle XBANK~BZ −0,089 (t −1,7).
- **Yorum:** Bu bankaya özgü bir küresel bağ değil. 2026 petrol şokuyla oluşan BIST içi rotasyon: petrole duyarlı yurt içi hisseler (havayolu, banka, holding) bir yanda, rafineri/petrokimya diğer yanda.
- **Etiket:** DÜŞÜK kalıyor. Tek bir yıl, tek bir tema; mekanizma petrol → enflasyon → faiz.

### B7 — BBVA ↔ GARAN
- GARAN~BBVA.MC pc +0,022 (t 1,2). IS −0,017 / OOS +0,038. XU100+TRY+EEM kontrolüyle 0,009. Banka sepeti kontrolüyle −0,010.
- Yılların yalnız %35'inde pozitif. ADR (BBVA) ile de aynı: 0,025.
- 2026 1y pc +0,27 (t 4,0). Ama GARAN~SAN.MC 1y +0,31. Bu GARAN'a özgü değil; B5'teki ortak faktör.
- **Ters yön (BBVA.MC ~ GARAN):**
  - Yalnız SAN kontrolüyle 0,10 (IS 0,14 / OOS 0,06 / 3y 0,03).
  - XU100 de eklenince 0,033 (t 1,9). EUFN de eklenince 0,029, 1y −0,01.
- **Sonuç:** Özgü bağ yok. İlişki etiketi ÇOK DÜŞÜK; "bağ yok" bulgusunun kendisi sağlam.

### H1 — SAHOL–AKBNK
- pc 0,243 (t 10,8), IS 0,244, OOS 0,352, 3y 0,361, 1y 0,527 (t 9,2). 2005+ dönemde 0,313. Yıllık: 2010–16 −0,12…+0,08 (≈0); 2017'den itibaren 0,15–0,56.
- **Kontroller:**
  - XU100+TRY+EEM: 0,237.
  - Aynı kontroller + AKBNK hariç banka sepeti: **0,183** (IS 0,184 / OOS 0,238; 15/17 yıl pozitif).
  - XBANK kontrolüyle 0,158. XBANK AKBNK'yi içerdiği için bu aşırı kontrol; son 3 yılda 0,07.
- **Plasebo (XU100 kontrollü):** SAHOL'un diğer bankalarla pc'si GARAN 0,163, YKBNK 0,194, ISCTR 0,171. Banka sepeti kontrolüyle bunlar 0,065 / 0,109 / 0,078'e iniyor; AKBNK 0,183'te kalıyor.
  - SAHOL'un 46 hisse içindeki en yüksek pc'si KCHOL ile: 0,250 (holding faktörü).
- **Mekanik içerme:** XU100 her iki hisseyi de içeriyor. Endeks kontrolü tahmini aşağı çekiyor; tahmin muhafazakâr. Kaba "XU100-ex" düzeltmeleri (ağırlık %5–8) pc'yi 0,35–0,42'ye çıkarıyor ama ağırlıklar bilinmediği için güvenilir değil.
- **Etiket:** YÜKSEK. Ancak ilişkinin yaklaşık üçte ikisi "SAHOL = özel banka + holding vekili" faktörü. AKBNK'ye özgü fazlalık pc ~0,18.

### H2 — KCHOL ve iştirakleri
| İştirak | pc (t) | IS / OOS | 3y / 1y | Aynı işaretli yıl | +sektör (XUSIN ya da banka sepeti) | +SAHOL | Yeni etiket |
|---|---|---|---|---|---|---|---|
| ARCLK | 0,157 (8,5) | 0,182 / 0,149 | 0,184 / 0,229 | 17/17 | 0,166 | 0,151 | YÜKSEK |
| FROTO | 0,152 (7,5) | 0,141 / 0,193 | 0,226 / 0,280 | 15/17 | 0,169 | 0,158 | YÜKSEK |
| TOASO | 0,120 (6,5) | 0,138 / 0,120 | 0,174 / 0,178 | 17/17 | 0,136 | 0,123 | YÜKSEK (pc <0,15, ama plasebo ve istikrar güçlü) |
| TUPRS | 0,117 (5,6) | 0,162 / **0,071** | 0,124 / **0,029** (t 0,4) | 15/17 | 0,144 | 0,130 | **ORTA** |
| YKBNK | 0,122 (4,4) | **0,079** / 0,204 | 0,203 / 0,158 | 12/17 | 0,143 | **0,079** (1y −0,12) | **ORTA** |

- **Plasebo:** KCHOL'un diğer 46 VİOP hissesiyle pc'si sıralandığında 1. sırada SAHOL (0,250), 2.–6. sıralarda **beş iştirak** var. Grup dışı 41 hissede medyan −0,018, p90 0,045. Eşit ağırlıklı ve grup hariç sepet kontrolüyle de sonuç değişmiyor. İştirak bağı gerçek ve plaseboyla açıkça ayrışıyor.
- **YKBNK:** Bağ 2020 sonrasında ortaya çıkıyor (2023: 0,45, 2024: 0,30). Bu, Koç'un YKB payını artırmasıyla uyumlu. Kısmen SAHOL ile ortak "holding ve banka" faktörü.
- **TUPRS:** OOS'ta yarıya iniyor, son 1 yılda sıfır. 2026'da TUPRS petrol şokuyla ayrıştı (B5'te Brent pc +0,45).

### H3 — ENKAI–USDTRY
- pc 0,094 (t 5,3). XU100+EEM+ES kontrolüyle 0,098. XUSIN de eklenince 0,091.
- IS 0,101 (t 3,7) / OOS 0,087 (t 2,8). **3y 0,017 (t 0,5), 1y 0,049 (t 1,0).** Saatlik 15:00 FX ile 2024+ dönemde 0,044 (t 1,1).
- Yıllık: 14/17 pozitif. 2005–2026'da 18/22 (fix2). Büyük katkı 2014, 2018, 2020, 2021, 2023'ten. 2024 −0,06.
- **Plasebo:** 47 VİOP hissesi içinde USDTRY pc'si en yüksek ENKAI (2. AEFES 0,074, 3. TOASO 0,070). Göreli hedge özelliği gerçek.
- **Mekanizma** (USD sunum para birimi, net nakit) makul. Fakat 2024'ten bu yana yönetilen TL rejiminde, günlük kur oynaklığı ~22 bp iken, kanal görünmüyor.
- **Etiket:** Tam dönem için ORTA. Güncel kullanım için DÜŞÜK.

## 3. Karşı argümanlar ve sınırlamalar
- **Saatlik pencere kısa.** B1 ve B3 yalnız ~2,9 yıllık (B3 için 2,4 yıllık) saatlik veriye dayanıyor. Uzun dönem kanıtı günlük vekilden geliyor; bu vekil, BIST kapanışında zaten fiyatlanmış kısmı XU100_t ve XBANK_t ile kontrol ediyor.
- **XBANK gap ölçümü.** Gap'i günlük Yahoo endeks açılışından hesapladım. Açılış seansının tek fiyatlı yapısı ve dolum varsayımı test edilmedi.
- **Çoklu test.** Doğrulamalar hedefli yapıldı. Tek tarama B5 için (1.001 sürücü × 15 pencere); null dağılımı olarak raporlandı.
- **Mekanik içerme.** Kontrol endeksleri (XU100, XBANK, XUSIN) hedef hisseleri de içeriyor. XYUZO, XHOLD, XUHIZ, XINSA serilerinin günlük geçmişi yok (her biri tek satır). Alternatif olarak eşit ağırlıklı ve grup hariç VİOP sepeti kullanıldı.
- **Korelasyon nedensellik değildir.** B5 ve B4 rejime bağlı. H1 ve H2 sahiplik yapısına dayanıyor; yapı zamanla değişiyor (YKB payı, 2017 öncesinde SAHOL–AKBNK ≈0).

## 4. TradingView
NASDAQ:TUR, CME_MINI:ES1!, BIST:XBANK, BIST:GARAN, BIST:AKBNK, FX:USDTRY, ICEEUR:BRN1! (alternatif TVC:UKOIL), BME:SAN, NASDAQ:EMB, BME:BBVA, NYSE:BBVA, BIST:SAHOL, BIST:KCHOL, BIST:ARCLK, BIST:FROTO, BIST:TOASO, BIST:TUPRS, BIST:YKBNK, BIST:ENKAI, BIST:XUSIN.
