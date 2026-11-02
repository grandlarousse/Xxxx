# v_A4_b — 2. aşama çürütme (şeytanın avukatı): İddia A4

Konu: havayolu sepeti t-1 → THYAO / PGSUS / TAVHL gün-içi getirisi. Ayrıca TUR ve COMBO.
Tarih 02.11.2026. Veri sonu 30.10.2026.
Kod `out/code_v_A4_b/` altında: core.py, v1–v8; loglar v1.log … v8.log; ara sonuçlar res/.
ll.py, h.py ve v_A4_a/vcore.py import edilmedi. Hizalama, temizlik, backtest ve NW-OLS kodunu ham parquet'ten kendim yazdım.

## 0. Hüküm
**DÜZELT. Güven: ilişki ORTA, net işlenebilirlik DÜŞÜK.**

Çürütme denemelerinin çoğu başarısız oldu. İlişki gerçek ve havacılığa özgü:
- Rastgele sepet null'unda p<0,003.
- 159 BIST hissesi arasında THYAO, PGSUS ve TAVHL 1., 2. ve 3. sırada. Kaynakta hedef olarak hiç kullanılmamış DOCO 4. sırada.
- Ortak faktör kontrollerinden sonra da duruyor.
- Bayatlatılmış ve rastgele işaretli plasebolar boş çıkıyor.
- Kaynağın hiç bakmadığı 2008–2013 döneminde (geriye dönük test) THYAO ve TAVHL'de t≈2.

Başarılı çürütmeler işlenebilirlik ve büyüklük tarafında:
- **Parametre seçimi iyimser.** 144 varyantlık bir ızgarada IS ile OOS sıralamaları arasında korelasyon yok (Spearman 0,08). IS'te en iyi varyant OOS'ta yalnız t≈1,0–1,3 veriyor. Başlıktaki OOS t değeri, varyantların ilk ~%15'lik dilimine düşüyor.
- **Etki günün erken saatlerinde.** Giriş 10:30 TSİ'ye, VWAP'a veya 11:30'a kayınca net getiri sıfıra iniyor.
- **VİOP vadelisi ve son dönem zayıf.** 2024–26'da VİOP vadelisinde 8 bps maliyetle net getiri PGSUS'ta 9,6 bps (t 0,77), TAVHL'de 4,4 bps (t 0,32).
- **TUR bacağı son 3 yılda zararlı.**

## 1. Yeniden üretim (iki hizalama)
- **A:** kaynak mantığı, kendi kodumla. Seriler BIST takvimine ffill ediliyor, sonra shift(1).
- **C (kendi tasarımım):** her sepet kendi borsa takviminde artıklaştırılıp z'leniyor. BIST günü t için takvim tarihi t_prev ≤ D < t olan son sürücü günü D kullanılıyor.
- İki hizalama arasında corr 0,956, pozisyon uyumu %96.

| 8 bps net, bps (iid t) | IS 2014–20 | OOS 2021–26 | 15 bps OOS | brüt OOS |
|---|---|---|---|---|
| THYAO A | 17,2 (2,29) | 20,4 (2,41; NW 2,77) | – | 28,4 |
| THYAO C | 19,1 (2,53) | 17,7 (2,08) | 10,7 (1,26) | 25,7 |
| PGSUS C | 16,0 (1,83) | 18,8 (2,02) | 11,8 (1,27) | 26,8 |
| TAVHL C | 7,9 (1,07) | 19,6 (2,15) | 12,6 (1,38) | 27,6 |

XU100 brüt getirisi: IS 10,3 bps (t 2,2), OOS 4,6 bps (t 0,7). Yani "XU100'de ≈0" ifadesi yalnız net bazda doğru.

## 2. Özgüllük ve plasebolar (iddia burada ayakta kaldı)
**(a) Hedef kesiti (159 BIST hissesi, v2a).** Sürekli NW t değerleri:
- THYAO 4,24, PGSUS 4,14, TAVHL 3,26: sırasıyla 1., 2. ve 3.
- DOCO (DO&CO, havayolu ikram şirketi) 2,69 ile 4.
- Medyan 0,21.
- VİOP-47 içinde OOS t>2 olan yalnız bu üç hisse var.
- İstisna: CLEBI −0,18.
- Bankalarda IS'te brüt 10–15 bps'lik bir piyasa bileşeni var, ama OOS'ta yok.

**(b) Rastgele sepet null'u (v2c).** 400 çekiliş, her birinde havacılık ve turizm dışından 7 AB + 6 ABD hissesi; kural aynı.

| | THYAO | PGSUS | TAVHL |
|---|---|---|---|
| Gözlenen ALL t | 3,27 | 2,71 | 2,29 |
| Null %99 | 1,24 | 1,81 | 1,72 |
| p | <0,0025 | <0,0025 | <0,0025 |
| Brüt null medyanı (bps) | 4,0 | 6,5 | 7,7 |
| Gözlenen brüt (bps) | 26 | 25 | 21 |

TAVHL'nin IS sonucu null'dan ayırt edilemiyor (p 0,49).

**(c) Sektör sepetleri (aynı kural, v2b).**
- Hiçbir sektör sepeti IS ve OOS'ta birlikte çalışmıyor.
- Havacılık dışı seyahat sepeti (TUI, Meliá, Accor, CCL, RCL, BKNG, EXPE, MAR): IS t 2,3–3,2, OOS ≈0.
- Çimento ve kimya: sürekli t 2,6–3,4, ama backtest OOS'ta zayıf. Avrupa döngüsellerinden gelen genel ve zayıf bir yayılma ihtimali dışlanamaz.

**(d) Bayatlatma ve rastgele işaret.**
- Ek 1 gün gecikme: t 0,05–0,85. Ek 2, 3 ve 5 gün gecikmede etki ≈0 veya negatif.
- Yıl içinde işaret karıştırma: p<0,001.

**(e) Geriye dönük holdout, 2008–2013 (v7).** Yahoo açılışı bu dönemde bozuk olduğu için hedef cc. 2014+ döneminde AIR→gap ≈0 (t 0,3) olduğundan cc, gün-içinin vekili.

| 2008–2013 | Katsayı | t | Brüt bps (t) |
|---|---|---|---|
| THYAO | 0,071 | 2,02 | 22,7 (2,17) |
| TAVHL | 0,059 | 2,07 | 21,3 (2,24) |
| XU100 | 0,032 | 0,97 | – |

THYAO yıllık brüt: 2008 48, 2009 58, 2010 21, 2011 16, 2012 35, 2013 −39 bps.

## 3. Ortak faktör kontrolleri (v3, v3b, v5)
Model: intra_t ~ AIR + kontroller. Standartlaştırılmış katsayılar, NW t. AIR'in t değeri:

| Kontrol seti | THYAO | PGSUS | TAVHL |
|---|---|---|---|
| Yalın | 4,24 | 4,14 | 3,26 |
| Hepsi (aşağıda) | 4,70 | 4,06 | 3,35 |
| Eşzamanlı XU100 gün-içi_t (işlenemez) | 5,05 | 3,86 | 2,76 |

"Hepsi" kontrol seti şunlardan oluşuyor:
- Kendi ve XU100 cc_{t-1} ile intra_{t-1}
- Kendi ve XU100 gap_t
- TUR, EEM, ES, VIX, STOXX, SPX
- USDTRY, EURUSD, Brent

IS/OOS ayrımında AIR t her spesifikasyonda: THYAO 3,2–4,0 / 2,6–3,7; PGSUS 2,6–3,5 / 2,1–2,8; TAVHL 1,2–2,4 / 2,3–2,8.

Diğer kontroller:
- **JETS (ham):** THYAO katsayısı 0,083'ten 0,096'ya çıkıyor; JETS'in kendi katsayısı −0,02 ve anlamsız. S6'daki t düşüşü eşdoğrusallık ve örneklem farkından kaynaklanıyor.
- **Brent:** corr(AIR, Brent_{t-1}) −0,21. Brent kontrolü AIR'in t değerini artırıyor; etki petrolün vekili değil.
- **Saatlik dönem (2023-12+):** gece ES hareketi ve AB havayollarının BIST kapanışı sonrası parçası anlamsız. Ancak bu dönemde AIR'in t değeri de düşük: 2,26 / 1,13 / 1,21.
- **Brüt getirinin ayrıştırması (piyasa + hisseye özgü):**
  - OOS'ta piyasa payı THYAO 2,3, PGSUS 0,8, TAVHL 2,6 bps.
  - OOS'ta hisseye özgü pay THYAO 23,4 (t 3,8), PGSUS 26,0 (t 3,5), TAVHL 25,0 (t 3,5) bps.
  - IS'te piyasa payı 6–12 bps.

## 4. Alt dönemler, rejim ve uç değerler
Alt dönemler (C hizalaması, 8 bps net, bps ve t):

| | 2014–17 | 2018–20 | 2021–23 | 2024–26 |
|---|---|---|---|---|
| THYAO | 7,9 (1,06) | 33,5 (2,35) | 17,5 (1,19) | 17,8 (2,00) |
| PGSUS | 8,5 (1,04) | 25,8 (1,51) | 27,3 (1,76) | 10,7 (1,01) |
| TAVHL | −5,7 (−0,70) | 25,5 (1,92) | 26,8 (1,86) | 12,8 (1,12) |

- Pozitif yıl sayısı: THYAO 12/13, PGSUS 10/13, TAVHL 6/13.
- COVID dönemi (2020-02..2021-06) hariç IS: 12,8 (t 1,60) / 6,8 (t 0,79) / −6,5.
- **Etki yalnız kriz dönemlerinde değil.** Önceden bilinen 60 günlük volatiliteye göre en düşük tercile'de brüt THYAO 32,7 (t 4,5), PGSUS 17,4 (2,3), TAVHL 18,4 (2,3). Vol-ölçekli t: 4,9 / 3,9 / 3,4. "IS'in tamamı COVID" yorumu (1. aşama) aşırı. Yine de 2014–2017 sakin döneminde etki ≈0.

**Uç değerler (OOS):**
- En iyi 10 gün çıkarılınca: 7,5 (t 0,94) / 7,5 (0,86) / 9,7 (1,11).
- En iyi 20 gün çıkarılınca: ≈0.
- Bu test tek başına yanıltıcı. Rastgele işaret null'unda aynı istatistiğin medyanı −10…−11 bps; gözlenen değer 15–18 bps (p≤0,002).
- Simetrik kırpma (en iyi ve en kötü 10 gün): 17,9 / 18,6 / 19,8 (t 2,3–2,4).
- Hedefi %1–99'da winsorize etmek sonucu değiştirmiyor.
- Medyan brüt 19–23 bps, isabet oranı %54. Etki kuyruk günlerine bağlı değil.

**Uzun/kısa asimetrisi:** IS'te kazancı kısa taraf, OOS'ta uzun taraf taşıyor (THYAO OOS: uzun−düz 44, düz−kısa 8). İstikrarsızlık işareti.

## 5. Veri madenciliği / seçim yanlılığı (en önemli çürütme)
Kaynakta hipotezlerin kurulma sırası:
1. 16.365 testlik tarama: PGSUS'ta 1. sırada EZJ, THYAO'da 1. sırada TUR.
2. M1–M3 çok değişkenli regresyonlar.
3. Yaklaşık 14 sinyal varyantı backtest edildi. Önceden tanımlı ana sinyal COMBO'ydu. "AIR" bunun içinden atıf adımında (a5b) çıkarıldı. TUR bacağı, taramada 1. çıktıktan sonra eklendi.

Spesifikasyon eğrisi (v5). 144 varyant: artık/ham, β penceresi 120/250/500, z penceresi 120/250/500, EU/US/EU+US, eşik 0/0,5/1/1,5.

| | THYAO | PGSUS | TAVHL |
|---|---|---|---|
| OOS net >0 olan varyant oranı | %94 | %91 | %89 |
| OOS t>2 olan varyant oranı | %17 | %28 | %25 |
| OOS t medyanı | 1,03 | 1,69 | 1,08 |

- İşaret istikrarlı, ama anlamlılık parametreye bağlı.
- **IS ile OOS t sıralamalarının Spearman korelasyonu 0,08.** IS performansı OOS'u tahmin etmiyor.
- **Üç hissenin ortalama IS t'sine göre varyant seçilirse** (seçilen: artık, β500, z500, EU+US, eşik 1,5), OOS: THYAO 11,9 (t 1,19), PGSUS 15,7 (1,34), TAVHL 12,0 (1,01).
- Hisse bazında IS'te en iyi varyant seçilirse PGSUS ve TAVHL OOS'ta negatif.
- Başlık varyantı IS sıralamasında 144 içinde 23. Ailesi (artık EU+US, eşik 0,5–1) en tutarlı aile: OOS t medyanı 2,1–2,3. Tek bacaklı ve ham versiyonlar zayıf (OOS t medyanı 0,6–1,5).
- Üç hisse bağımsız tekrar sayılmamalı: sinyal aynı ve hisselerin gün-içi getirileri yüksek korelasyonlu.

**Gerçekçi ileriye dönük beklenti:** 8 bps maliyetle 10–15 bps/işlem, 6 yılda t≈1–1,5.

## 6. Açılış fiyatı gerçekçiliği ve VİOP
**Saatlik veri (2023-11-30..2026-10-30, n≈350 işlem; v4a):**

| | Açılış→kapanış brüt (t) | 10:30→kapanış brüt (t) | 10:30 giriş, 8 bps net | İlk saat tipik fiyattan giriş, net | 11:30 giriş, net |
|---|---|---|---|---|---|
| THYAO | 23,0 (2,60) | 15,6 (2,00) | 7,6 (0,98) | 9,4 | 6,0 |
| PGSUS | 18,6 (1,77) | 16,3 (1,74) | 8,3 (0,88) | 10,0 | −0,1 |
| TAVHL | 21,0 (1,87) | 8,0 (0,80) | ≈0 | 4,4 | 0,3 |

**VİOP bülteni (v4b).** 2.424 dosya, 2017-04..2026-10, eksik günler var. Her gün en yüksek hacimli kontrat kullanıldı, açılış→kapanış; yaklaşık 1.100 işlem.

| | ALL brüt (t) | ALL 8 bps net (t) | OOS 8 bps net (t) | 2024–26 8 bps net (t) | ALL 15 bps net (t) |
|---|---|---|---|---|---|
| THYAO | 31,8 (4,08) | 23,8 (3,06) | 15,1 (1,56) | 19,7 (1,93) | 16,8 (2,16) |
| PGSUS | 31,7 (3,41) | 23,7 (2,55) | 19,1 (1,77) | 9,6 (0,77) | 16,7 (1,80) |
| TAVHL | 26,8 (2,84) | 18,8 (1,99) | 14,7 (1,33) | 4,4 (0,32) | 11,8 (1,25) |

- **VWAP→kapanış:** brüt 12 / 12 / 8 bps, net ≈0–4. Kazanç seansın başında oluşuyor.
- **Yahoo açılışının 2017–2022 gerçekçiliği (dolaylı kontrol):** vadeli ile spot gün-içi getiri korelasyonu yıllara göre THYAO 0,87–0,96, PGSUS 0,69–0,95, TAVHL 0,84–0,93. Vadeli backtest'i spot sonucuyla uyumlu. Yahoo açılışı bir artefakt değil.
- **Likidite:** 2024–26 medyan vadeli işlem hacmi THYAO 1,8–3,5 milyar TL/gün, PGSUS 0,5–0,7 milyar, TAVHL 0,18–0,41 milyar.
  - 2017–2018'de PGSUS ve TAVHL vadelileri neredeyse işlem görmüyordu (0,2–0,6 milyon TL/gün, 26–69 işlem). Bu iki hissenin IS dönemi VİOP'la işlenemezdi.
  - VİOP açılış seansında medyan 2–5 işlem var.
  - Fiyat adımı 0,05 TL; ~200–300 TL fiyatta 1,7–2,5 bps.

## 7. TUR ve COMBO
- TUR_{t-1} → gün-içi korelasyonu (C hizalaması):
  - THYAO −0,098 (t −4,3). 13 yılın 10'unda negatif; 2019, 2020 ve 2024 pozitif.
  - PGSUS −0,047 (t −1,7), TAVHL −0,039 (t −1,7).
- −TUR tek başına, 2024–26: −21 / −18 / −22 bps.
- COMBO, 2024–26: 10,3 (t 1,14) / 4,2 (0,41) / 9,7 (0,90). Aynı dönemde AIR 17,8 / 10,7 / 12,8.
- COMBO post-hoc kurgulanmış ve son dönemde AIR'in altında. **Güven: DÜŞÜK.**

## 8. 1. aşamayla farklar
1. "IS anlamlılığı COVID kaynaklı" yorumu kısmen yanlış. 2008–13 geriye dönük testi ve düşük volatilite tercile'si, etkinin krizlere bağlı olmadığını gösteriyor. 2014–17 dönemindeki zayıflık ise doğru.
2. TAVHL için ilişki kanıtı 1. aşamada sanılandan güçlü: kesitte 3. sıra, ALL rastgele null p<0,003, geriye dönük testte t 2,07. Buna karşılık IS (2014–20) zayıf ve yalnız 6/13 yıl pozitif. Güven: ilişki DÜŞÜK–ORTA, işlenebilirlik DÜŞÜK.
3. VİOP örneklemi 1. aşamadaki 225 işlemden ~1.100'e çıktı. Tüm dönemde anlamlı, ama OOS t 1,3–1,8 ve 2024–26'da yalnız THYAO t≈1,9.
4. Spesifikasyon seçimi yanlılığı yeni bir bulgu: başlık OOS rakamları varyant dağılımının üst ucunda.

## 9. Düzeltilmiş iddia
Avrupa+ABD havayolu artık sepeti (AIR; STOXX ve SPX'e göre kayan beta, z-skor) t-1'de |AIR|>1 olduğunda, ertesi gün BIST'te THYAO, PGSUS ve TAVHL'nin gün-içi getirisi aynı yöne gidiyor.
- İleriye bakma yok.
- Açılış gap'inde fiyatlanmıyor.
- Havacılığa özgü: 159 hisse içinde ilk 3 sırada, DOCO 4.
- Ortak faktörlerden bağımsız.
- Plasebolar boş çıkıyor.
- 2008–13 geriye dönük testinde tekrarlıyor.

Sürekli regresyon t: THYAO 4,2, PGSUS 4,1, TAVHL 3,3. Brüt getiri ~21–26 bps/işlem.

İşlenebilir net getiri iddia edilenden düşük:
- Açılış müzayedesinden 8 bps maliyetle OOS: 17,7–20,4 / 18,8–22,6 / 19,6–20,7 bps (iid t 2,0–2,4).
- 15 bps maliyetle: 11–13 bps (t 1,3).
- VİOP'ta 8 bps maliyetle OOS t 1,3–1,8.
- 10:30 TSİ girişte ≈0–8 bps.
- IS'te seçilen parametrelerle OOS t≈1,2.

## 10. Sınırlamalar
- Gerçek bir ileri-tarih holdout yok. 2008–13 geriye dönük testi en yakın yaklaşım; orada hedef cc, gün-içi değil.
- VİOP dosyaları başka bir ajan tarafından indirilmeye devam ediyordu. 2019 ve 2021 kısmen eksik.
- VİOP için gün-içi saatlik veri yok; açılış seansında dolum varsayımı iyimser.
- Spread tahmini (Abdi-Ranaldo) günlük veride işe yaramadı; maliyet tartışması fiyat adımına dayanıyor.

## TradingView
BIST:THYAO, BIST:PGSUS, BIST:TAVHL, BIST:DOCO; XETR:LHA, EURONEXT:AF, LSE:IAG, LSE:EZJ, LSE:WIZZ, LSE:JET2, NASDAQ:RYAAY (RYA.IR vekili); NYSE:DAL, NASDAQ:UAL, NASDAQ:AAL, NYSE:LUV, NYSE:ALK, NASDAQ:JBLU; AMEX:JETS; SP:SPX; TVC:SXXP (?); NASDAQ:TUR.
