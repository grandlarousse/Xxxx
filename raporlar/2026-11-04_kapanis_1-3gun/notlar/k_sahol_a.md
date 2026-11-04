# k_sahol_a: SAHOL/AKBNK oran ortalamaya dönüşü, kapanıştan kapanışa VİOP işlem planı

Kod `out/code_k_sahol_a/` altında: `00_update`, `00b_last`, `01_repro`, `02_c2c`, `03_detail`, `04_now`, `05_extra`. Ortak kütüphane `kl.py`. Çıktılar `res_*.csv` ve `log0*.txt`.
Günlük kullanım için iki dosya var: `out/code_k_sahol/sinyal.py` ve `out/code_k_sahol/sahol_akbnk_z.pine`.

**Veri**
- Spot: ortak veri 30.10.2026'ya kadar. Güncel indirme `dl_k_sahol_a/` altında; ortak veriye dokunulmadı.
- Yahoo günlük barı 02.11'e kadar dolu. **03.11.2026 kapanışı** Yahoo `regularMarketPrice` alanından alındı (18:09 TSİ): SAHOL 82,45, AKBNK 62,25.
- VİOP bülteni 02.11 ve **03.11.2026** indirildi, aynı ayrıştırıcıyla işlendi.
- Yeni indirmenin z değeri ortak veriyle 2010 sonrasında aynı (en büyük fark 3e-5).

## Hüküm
Bu, araştırmadaki bulgular içinde kapanıştan kapanışa çalışan bir yatırımcının gerçekten uygulayabileceği bir kural. Akşam kapanışta karar verilir, VİOP uzlaşmasından iki bacak açılır.

- **Kural A** (bant içi çıkış) profile en uygun olanı. Medyan tutma 2 gün, ortalama 3,7 gün.
- **OOS 2021–26, gerçek VİOP uzlaşması, 8 bps + tik:** işlem başı net +64 bps, t 3,1, yılda 18,5 işlem.
- **IS 2014–20, spot vekili:** +58 bps, t 3,5.
- **Koşullar:**
  - Maliyet bacak başına gidiş-dönüş ≤15 bps olmalı. 30 bps'te getiri ≈0.
  - Emir aynı akşam verilmeli.
  - İşlemlerin %10'u 10 günden uzun sürüyor. Zaman sınırı koymak sonucu bozuyor.
  - 2021–23 zayıftı. 2021-03 ile 2022-04 arasında SAHOL nominalinin %24'ü kadar düşüş yaşandı.
- **Sabit 1–2 gün tutma çalışmıyor.** Kapanıştan kapanışa ilk günün getirisi ≈0; dönüş 3. günden sonra geliyor.
- **Güven: ORTA. Kullanıcıya uygunluk: KOŞULLU.**

## 1. Kural (kesin)
- **Sinyal** (spot, temettü düzeltmeli kapanış, BIST takvimi):
  - Temizlik: |basit getiri| %20,5'ten (13.03.2020 öncesi) ya da %10,5'ten (sonrası) büyükse o gün NaN.
  - β_t = cov₂₅₀(r_SAHOL, r_AKBNK) / var₂₅₀(r_AKBNK). En az 125 gün, **1 gün gecikmeli**.
  - S_t = Σ(r_SAHOL − β·r_AKBNK). Bu, log SAHOL − β·log AKBNK'nın kayan-β'lı karşılığı.
  - z_t = (S − ort₆₀) / std₆₀.
- **Giriş:** |z| > 1,5 olan yeni bir bölümün ilk kapanışında. Her bölüme en fazla bir kez girilir.
  - z > +1,5: **SHORT spread**, yani F_SAHOL sat, F_AKBNK al.
  - z < −1,5: **LONG spread**, yani F_SAHOL al, F_AKBNK sat.
- **Çıkış**, z'nin döndüğü günün uzlaşmasından:
  - **A:** |z| ≤ 1,5 (bant içi; kaynak kural).
  - C: 1,0.
  - B: 0,5.
  - Zaman sınırı ve stop yok. Gerekçe aşağıda.
- **Hedge ve kontrat oranı:** β-ağırlıklı TL nominal, girişte sabitlenir. N_AKBNK = yuvarla(N_SAHOL·β·F_SAHOL/F_AKBNK).
  - Bugün oran 0,666·84,38/63,64 = **0,883**, yani 1 çift = 1 SAHOL + 1 AKBNK kontratı; 10 SAHOL'e 9 AKBNK.
  - Eşit TL alternatifinde oran 1,33 olur.
- **Vade:** vadesine 1 iş gününden fazla kalan en yakın vade tutulur. Kalan 1 iş gününde uzlaşmadan bir sonraki vadeye geçilir.
  - Kasım vadesi için devir günü **27.11.2026** (Aralık vadesine).
  - Pay vadelileri fiziki teslimatlı; vadeye taşınmamalı.
- **Maliyet modeli:**
  - Her bacakta gidiş-dönüş c bps + 1 tik/fiyat. VİOP'ta tik 0,01 TL; spot vekilde BIST fiyat adımı.
  - Devirde iki bacakta tam gidiş-dönüş: eski vadeyi kapat + yenisini aç = 2 yarım spread.
  - Teminat: Takasbank başlangıç teminatı SAHOL %14, AKBNK %15 (08.06.2026 Gedik VİOP bülteni).

## 2. Zamanlama
- Spot kapanış seansı yaklaşık 18:00–18:05'te biter. Karar bu fiyatlarla verilir.
- VİOP uzlaşma fiyatı, seansın son 10 dakikasındaki işlemlerin miktar ağırlıklı ortalaması. Seans sonu kaynağa göre 18:10 ya da 18:15.
- Pratik rutin:
  1. 18:05'ten sonra `sinyal.py --fa F_SAHOL --fb F_AKBNK` çalıştırılır ya da TV göstergesine bakılır.
  2. "AÇ" ya da "KAPAT" çıkarsa iki bacak aynı dakikalarda, orta fiyata yakın limit emirle verilir.
- **Gecikme duyarlılığı** (ertesi gün uzlaşmasıyla uygulama): OOS VİOP A 94 bps (t 3,33). Ama IS spot A 23 bps (t 1,04). 2014–20'de dönüş hızlıydı. **Aynı akşam uygulamak gerekiyor.**
- v_YR1_a'nın testi: sinyal 17:30 fiyatıyla üretilip aynı gün kapanışta girilince t 2,30. Karar fiyatındaki birkaç dakikalık fark kritik değil.

## 3. Yeniden üretim (spot, t+1 açılış girişi; ortak veri, son gün 30.10)
| | IS 2014–20 | OOS 2021–26 |
|---|---|---|
| Kaynak muhasebesi, 8 bps (bps/aktif gün) | 19,9 (t 3,40); res_bt.csv'de 18,2 (3,13). Fark sonradan düzeltilen rejim temizliğinden | **27,1 (t 3,54), birebir** |
| Kaynak muhasebesi, 15 bps | 18,0 | 25,2 |
| Doğru muhasebe (vb.pnl_open), 8 / 15 / 30 bps | 13,9 (3,19) / 11,4 / 6,2 | 20,0 (3,40) / 17,6 / 12,4 (2,16) |

`kl.signal` z'si kaynakla 2005-08 sonrasında birebir aynı. `sinyal.py` z'si `kl` ile 2012 sonrasında birebir aynı (fark 0,0).

## 4. Kapanıştan kapanışa sonuçlar (aynı gün uzlaşma girişi; işlem başı net bps, t işlem bazında)
8 bps + tik. IS = spot kapanış vekili (iyimser; 2021–26'da spot vekili VİOP'tan işlem başına ~14 bps yüksek). OOS = gerçek VİOP.

| Çıkış | IS spot 2014–20 | **OOS VİOP 2021–26** | VİOP 2017–20 | VİOP 2021–23 | VİOP 2024–26 | yılda işlem | ort./medyan tutma (gün) |
|---|---|---|---|---|---|---|---|
| **A bant içi (\|z\|≤1,5)** | 57,7 (3,53) | **63,7 (3,12)** | 27,5 (1,13) | 50,3 (1,79) | 81,9 (2,75) | 18,5 | 3,7 / 2 |
| C z<1 | 101,8 (3,63) | 136,9 (3,51) | | | | 11,2 | 8,7 / 5 |
| B z<0,5 | 152,2 (4,36) | 232,8 (3,80) | 70,9 (1,05) | 214,1 (2,11) | 250,8 (3,48) | 8,4 | 15,2 / 9 |
| z<0 | 163,6 (3,07) | 276,9 (3,12) | −4,4 | 140,1 (0,96) | 394,1 (3,80) | 6,7 | 24,6 |
| z<0,5 + en çok 5 gün | 55,0 (2,35) | 75,9 (2,18) | | | | 16,7 | 4,6 |
| z<0,5 + en çok 10 gün | 96,3 (2,96) | 116,8 (2,39) | | | | 13,2 | 7,8 |
| z<0,5 + en çok 20 gün | 118,5 (2,99) | 210,5 (3,73) | | | | 10,5 | 11,8 |
| A + en çok 3 / 5 / 10 gün | 33 (2,29) / 40 (2,37) / 53 (3,06) | 26 (1,28) / 42 (1,80) / 46 (1,85) | | | | | 2,1 / 2,6 / 3,2 |
| sabit 1 gün | −5,0 (−0,39) | −19,5 (−1,12) | | | | 18,5 | 1 |
| sabit 2 gün | 2,8 (0,18) | 10,7 (0,48) | | | | | 2 |
| sabit 3 gün | 41,4 (2,27) | 47,1 (1,71) | | | | 18,0 | 3 |
| sabit 5 / 10 gün | 39 (1,68) / 69 (1,98) | 69 (1,84) / 112 (1,89) | | | | | |

**Maliyete duyarlılık** (OOS VİOP / IS spot, net bps, t):
- A: 15 bps + tik → 50 (2,44) / 46 (2,83). 30 bps + tik → 21 (1,02) / 22 (1,33).
- B: 15 → 212 (3,40) / 141 (4,03). 30 → 169 (2,59) / 116 (3,33).
- Başabaş maliyet (bacak başına gidiş-dönüş): A ≈46 bps, C ≈71, B ≈93.
- Gerçekçi maliyet (`y_viop_likidite.csv`):
  - Küçük emir: SAHOL 5,3, AKBNK 5,6 bps.
  - 1 mn TL'lik emir: 11,5 / 9,8 bps.
  - 8–15 bps aralığı gerçekçi.
- Tik etkisi 2021 öncesinde büyük (fiyat 5–10 TL). Örneğin A IS'te tiksiz 78,6, tikli 57,7. 2024+ için ihmal edilebilir (tik 1,2–1,6 bps).

**Olay profili: ufuklar.** Bölüm başlangıcında uzlaşmada girildiğinde, h gün sonraki kümülatif BRÜT getiri (bps, t):

| h | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 |
|---|---|---|---|---|---|---|---|---|
| IS spot (n=128) | 29 (2,3) | 37 (2,4) | 72 (4,1) | 80 (3,5) | 75 (3,1) | 76 (2,8) | 65 (2,0) | 76 (2,0) |
| OOS VİOP (n=108) | 1 (0,1) | 34 (1,5) | 58 (2,2) | 71 (2,1) | 126 (3,2) | 172 (3,6) | 218 (3,9) | 253 (4,1) |

- İlk 3 günde IS ve OOS'ta ~60–70 bps brüt birikiyor. Gidiş-dönüş maliyeti bugün ~15 bps (iki bacak).
- 2021–26'da dönüş 20 güne kadar sürdü; 2014–20'de 3. günde doydu. B kuralının OOS'taki üstünlüğü bu rejim farkından geliyor.
- 1. gün OOS VİOP'ta ≈0. 1–2 günlük sabit tutma işlenebilir değil.

**Kural A ve B istatistikleri** (8 bps + tik; IS spot / OOS VİOP):
| | A IS | A OOS | B IS | B OOS |
|---|---|---|---|---|
| İşlem (yılda) | 128 (18,3) | 108 (18,5) | 67 (9,6) | 49 (8,4) |
| Brüt / net / medyan net (bps) | 92 / 58 / 81 | 88 / 64 / 107 | 186 / 152 / 197 | 269 / 233 / 326 |
| İsabet | %77 | %70 | %85 | %82 |
| t (işlem / günlük NW) | 3,53 / 2,84 | 3,12 / 2,43 | 4,36 / 2,91 | 3,80 / 2,68 |
| Yıllık (bps, SAHOL nominaline) / Sharpe | 1.051 / 0,97 | 1.188 / 0,87 | 1.398 / 0,99 | 2.019 / 1,06 |
| Maks. düşüş (bps) | −1.233 | −2.365 (10.03.2021→12.04.2022) | −2.130 | −2.788 |
| En kötü işlem / 5. yüzdelik (bps) | −902 / −270 | −719 / −291 | −1.467 / −202 | −1.232 / −610 |
| Ardışık kayıp (maks.) | 2 | 3 | 2 | 2 |
| Tutma süresi | medyan 2; %75 ≤4; %90 ≤10; maks. 17 | | | medyan 9; %90 ≤37; maks. 71 |

- Diğer gözlemler:
  - Long ve short ikisi de kârlı (A OOS: short 67 işlem 59 bps, long 41 işlem 71 bps).
  - Son 12 ay (11.2025+): A 17 işlem, 106 bps.
  - Devirli işlem oranı: A %19, B %57.
  - Devir 1 yerine 2 iş günü kala yapılırsa fark yok (63,7 → 62,6).

**Yıllara göre, Kural A** (2014–20 spot, 2021+ VİOP; işlem / ort. net bps / yıl toplamı bps):

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 19 / 105 / 1.992 | 16 / −24 / −379 | 15 / 62 / 931 | 15 / 34 / 507 | 24 / 99 / 2.375 | 16 / 50 / 801 | 23 / 50 / 1.120 | 19 / −37 / −655 | 20 / 58 / 1.166 | 23 / 115 / 2.648 | 13 / 76 / 983 | 19 / 49 / 926 | 14 / 133 / 1.857 |

11/13 yıl pozitif. Kural B'de 13/13 yıl toplamı pozitif; 2021'de işlem ortalaması −14,5 bps.

**Sağlamlık**
- **Eşik × pencere** (eşik 1,25–2,0, pencere 40/60/90; t işlem bazında):
  - A: IS 2,0–4,4, OOS 2,1–3,9; 12 kombinasyonun 12'sinde OOS t > 2.
  - B: IS 2,3–4,5, OOS 1,7–4,6; 11/12.
  - Not: v_YR1_b'nin daha geniş ızgarasında (pencere 250 dahil, t+1 açılış) OOS t medyanı 1,96 idi. "Dürüst" beklenti, burada bulunan t ~3'ün altıdır.
- **Stop zarar veriyor** (A OOS): stop yok 64 (3,12); %3 stop 16 (0,65); %5 stop 37 (1,49); %8 stop 57 (2,52). Ortalamaya dönüşte stop ters seçim yapıyor. Risk, stop yerine boyutlamayla yönetilmeli.
- **Hedge ve kontrat oranı** (A OOS):

  | Varyant | Net bps (t) | Günlük vol (bps) |
  |---|---|---|
  | β250 | 63,7 (3,12) | 160 |
  | Eşit TL | 86,3 (3,07) | 192 |
  | Tam sayı N_SAHOL=1 (çoğunlukla 1:1) | 62,9 (2,91) | 170 |
  | Tam sayı 3 / 10 / 30 | 64,4 / 63,0 / 64,1 | |

  Tam sayı yuvarlama sorun değil. Eşit TL daha fazla bps getiriyor ama riski de orantılı artırıyor (t aynı).
- **Likidite** (2025+, pozisyon günlerinde tutulan sözleşmenin medyan günlük işlem değeri): SAHOL ~986 mn TL, AKBNK ~2.751 mn TL. 1 mn TL hesabın emirleri bunun yanında önemsiz.

## 5. TL karşılığı ve boyutlama (1 kontrat = 100 pay)
- **1 çift** (1 F_SAHOL + 1 F_AKBNK; OOS işlemlerin %91'inde N_AKBNK=1):
  - Kural A: OOS'ta tarihsel fiyatlarla işlem başı ort. **+50 TL**, 2026'da +144 TL. Bugünkü fiyatla 64 bps × 8.438 TL ≈ **54 TL/işlem**, yılda ≈ **1.000 TL/çift**.
  - Kural B: ≈197 TL/işlem, yılda ≈1.700 TL/çift.
  - Gidiş-dönüş maliyeti bugün çift başına ≈14 TL.
- **Teminat** (çift başına, mahsupsuz): 0,14·8.438 + 0,15·6.364 ≈ **2.136 TL**. Aracı kurum ek teminat isteyebilir.
- **Sermaye 1.000.000 TL, işlem başı risk %1 (10.000 TL):**
  - **Muhafazakâr** (risk birimi = tarihsel en kötü işlem ≈ SAHOL nominalinin %9'u):
    - Pozisyon: **13 F_SAHOL + 11 F_AKBNK**. Nominal 109.694 + 70.004 TL.
    - Teminat ≈ **25.900 TL (%2,6)**.
    - Beklenen yıllık (A) ≈ 13.000 TL (%1,3). OOS maks. düşüş ölçeğinde ≈ −25.900 TL (%2,6).
  - **Orta** (risk birimi = OOS 5. yüzdelik ≈ %3):
    - Pozisyon: **39 F_SAHOL + 34 F_AKBNK**. Nominal 329.082 + 216.376 TL.
    - Teminat ≈ 78.500 TL (%7,9).
    - Beklenen yıllık ≈ 39.000 TL (%3,9). Maks. düşüş ≈ −77.800 TL (%7,8).
    - En kötü işlem (−%7…−9) ≈ −24…−30 bin TL, yani %2,4–3.
- Yorum: %1 risk kuralıyla bu strateji sermayeye yıllık ~%1,3–4 katkı veriyor. Strateji tek başına büyük bir getiri kaynağı değil; düşük korelasyonlu bir ek.

## 6. Güncel durum (03.11.2026 kapanışı)
- **Fiyatlar ve z:**
  - SAHOL 82,45, AKBNK 62,25; β 0,666.
  - **z = −0,34**. Önceki günler: 02.11 −0,55, 30.10 −0,45, 28.10 −0,30, 23.10 +1,49 (eşiğin hemen altı).
  - **Sinyal yok, model pozisyonu yok.**
  - A'nın son işlemleri: 09.10→14.10 LONG (+196 bps spot), 15.10→16.10 LONG (+81).
- **04.11 kapanışı için tetikler** (diğer hisse sabitken):
  - z=+1,5 (SHORT spread) için spread +%4,28 olmalı: SAHOL ≥ 86,06 ya da AKBNK ≤ 58,37.
  - z=−1,5 (LONG spread) için −%2,80: SAHOL ≤ 80,18 ya da AKBNK ≥ 64,92.
- **VİOP** (03.11 uzlaşma): F_SAHOL1126 84,38, F_AKBNK1126 63,64, vade 30.11.2026. Kontrat oranı 0,883. Devir 27.11.2026.

## 7. Günlük kullanım
- **`out/code_k_sahol/sinyal.py`** (pandas/numpy/requests):
  - Yahoo'dan SAHOL.IS, AKBNK.IS ve XU100.IS (takvim için) çeker. Son barın kapanışı boşsa 18:05'ten sonra `regularMarketPrice` kullanır.
  - Yazdırdıkları: son 8 gün, z, sinyal bölgesi, modelin pozisyonu ve bugünkü eylem (AÇ/KAPAT/TUT/BEKLE), β, kontrat oranı, %1 risk boyutu ve teminat, yarın için tetik fiyatları, modelin son işlemleri.
  - Seçenekler: `--kural A|B|C`, `--fa/--fb` (vadeli fiyatları), `--sermaye`, `--risk`, `--risk-birim`, `--pozisyon long|short`, `--csv-sahol/--csv-akbnk`, `--canli` (seans içi tahmin).
  - Araştırma z'siyle birebir aynı (2012+ fark 0,0). CSV modunda takvim farkından −0,33 (Yahoo modunda −0,34).
- **`out/code_k_sahol/sahol_akbnk_z.pine`** (TradingView Pine v5, günlük grafik):
  - BIST:SAHOL ve BIST:AKBNK'yı temettü düzeltmeli çeker. 250 günlük kayan β (1 gün gecikmeli), 60 günlük z, ±1,5 giriş ve ±çıkış bantları.
  - Modelin pozisyonu arka plan rengiyle gösterilir. Giriş ve çıkış işaretleri ile alarmları var. Tabloda z, β, kontrat oranı ve bugünkü eylem.
  - **TV'de derlenip test edilmedi** (burada Pine motoru yok).
  - Temettü düzeltmesi açık kalmalı. Kapalıyken, nisan temettü gününde SAHOL'ün ~%3–4'lük düşüşü z'yi yaklaşık 1 birim kaydırır.

## 8. Riskler ve sınırlamalar
- **2021–23 VİOP'ta zayıf** (A t 1,79). 2021 yılı negatif. 14 ay süren −2.365 bps'lik düşüş var. 2017–20 VİOP likiditesi yetersizdi, bu dönem işlenemezdi.
- **IS spot vekili iyimser:** dolum, sinyali üreten kapanış fiyatından. 2021–26 karşılaştırmasında işlem başına ~14 bps fazla.
- **Maliyet:** A, 30 bps'te ≈0. Piyasa emriyle ve geniş spread'de işlem yapılmamalı.
- **Tutma süresi kuyruğu:** A'da %10 işlem 10 günden uzun (maks. 17); B'de 71 güne kadar. Zaman sınırı A'yı bozuyor (en çok 3 gün → t 1,28).
- **Veri madenciliği:** ilişki evrende 1/2.070 ve her yerde pozitif. Ama geniş ızgarada OOS t medyanı ~2. Burada raporlanan t ~3 üst sınır kabul edilmeli. B ve C çıkışları kaynak kuralı değil; v_YR1_a z=0,5 çıkışını önceden test etmişti (IS t 2,86 / OOS 3,13).
- **Yapısal risk:** Sabancı'nın Akbank payı değişirse, holding geri alım yaparsa ya da AKBNK sermaye işlemleri olursa ilişki bozulabilir. Temettüler mart–nisanda: vadeli düşmez; sinyal adj spottan hesaplanıyor. Bedelsiz ve benzeri işlemler z'yi yapay sıçratabilir; kurumsal işlem günleri kontrol edilmeli.
- **Teminat ve kaldıraç:** günlük teminat tamamlama var. Spread mahsubu varsayılmadı. Teminat oranları değişebilir; aracı kurumla teyit edilmeli.
- **Uygulama:** iki bacağın aynı uzlaşma penceresinde dolması gerekiyor (bacak riski). Yahoo'nun son günü geç ya da eksik gelebilir; betik bunu yazdırır.

Kaynaklar (web):
- Takasbank başlangıç teminatı, Gedik VİOP bülteni 08.06.2026: https://cdn.gedik.com/cdn/bulletin/2026/06/08/VIOP_Bulten_08062026_dc29d65f.pdf
- Uzlaşma fiyatı yöntemi, Borsa İstanbul VİOP kılavuzu: https://www.borsaistanbul.com/data/kilavuzlar/VIOP_vadeli_islem_sozlesmeleri.pdf
- Pay VİS seans saatleri: https://www.borsaistanbul.com/files/20221007-11671_yeni-pay-vis-acilmasi-ve-mevcut-pay-vis-deg.pdf
