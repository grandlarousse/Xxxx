# v_V1_a — Bağımsız doğrulama: Kredi notu değişikliği sonrası kontraryen ("haberi sat") stratejisi
Doğrulayıcı: V1_a · Tarih: 02.11.2026 · Kod: `out/code_v_V1_a/` (v1.py, v1b.py, v1c_viop.py, v1d.py, v1e.py; loglar log_*.txt).
Bağımsızlık: ll.py ve olib.py kullanılmadı. Ham parquet dosyaları `ldate` ile indekslendi. BIST takvimi XU100 günlerinden kuruldu. Getiriler doğrudan o/c fiyatlarından hesaplandı.

## 0. Karar
**DÜZELT. İddia ana hatlarıyla tekrar üretildi.** Zamanlama temiz, ileriye bakma yok. Ancak üç hata ve iki önemli nüans var:

**Hatalar:**
1. Olay listesinden bir not indirimi eksik: Fitch, 11.02.2022'de notu BB-'den B+'ya indirdi. Ayrıca 08.07.2022 kararı "BB-→B" değil "B+→B".
2. "Olay öncesi 5 gün +234 bps (t 2,7)" rakamı yanlış: 18.08.2018'de aynı akşam açıklanan S&P ve Moody's kararları ayrı ayrı sayılmış (n=20, bir olay iki kez). Doğrusu 19 olayda +211 bps (t 2,38). Düzeltilmiş 20 olayda +173 bps (t 1,88), yani anlamlı değil.
3. Görünüm listesi eksik: 8 görünüm değişikliği yok.

**Nüanslar:**
- XBANK'ın +320 bps'i büyük ölçüde beta. XBANK − XU100 fazlası +95 bps (t 1,6, medyan ≈ 0).
- Etki not değişikliğine özgü. Görünüm değişikliklerinde (n=20) hiç yok.

**Gerçek F_XU030 vadelisiyle** (Pazartesi uzlaşma → Çarşamba uzlaşma, 4 bps maliyet): olay başına +152 bps, t 3,1, n=17.

**Güven: ORTA** (değişmedi). Rakamlar güçlü: plasebo p≈0,0004, 8/8 yıl pozitif, bağımsız veride (TUR ETF) ve gerçek vadelide tekrar ediyor. Ama sınırlar var:
- Örneklem küçük: n=20, yılda ~2 olay.
- Yön ve vade sonradan seçilmiş.
- Mekanizma görünüm olaylarında doğrulanmıyor.
- Getirinin önemli kısmı iki rejim kümesinden geliyor: 2018 krizi ve 2024 artırımları.

## 1. Olay tarihleri — birincil/ikincil kaynak doğrulaması
Kaynaklar şunlar: TradingEconomics ve countryeconomy tabloları (birbirini tutuyor), Bloomberg/Reuters haber başlıkları, Garanti BBVA IR/KAP bildirimleri (Fitch tarihlerini resmi olarak listeliyor), Hürriyet DN, bianet, CNBC, intellinews. Ajans sitelerine (fitchratings/spglobal/moodys) doğrudan erişilemedi; bunlar giriş duvarlı.

**Not değişiklikleri (büyük üç, 2014–2026), n=20 tepki günü:**

| Açıklama | Gün | Ajans | Yön | Tepki (BIST) | Not |
|---|---|---|---|---|---|
| 20.07.2016 | Çar | S&P | ↓ BB+→BB | 21.07 | Takvim dışı, darbe sonrası. CNBC haberi 15:58 UTC'de, BIST kapanışından (15:00 UTC) hemen sonra; kesin saat bilinmiyor. Aynı akşam OHAL ilan edildi (karışık etki). |
| 23.09.2016 | Cum | Moody's | ↓ Baa3→Ba1 | 26.09 | |
| 27.01.2017 | Cum | Fitch | ↓ BBB-→BB+ | 30.01 | Aynı gün S&P görünümü negatife çekti. |
| 07.03.2018 | Çar gece | Moody's | ↓ Ba1→Ba2 | 08.03 | Takvim dışı. |
| 01.05.2018 | Sal gece | S&P | ↓ BB→BB- | 02.05 | 1 Mayıs tatili. |
| 13.07.2018 | Cum | Fitch | ↓ BB+→BB | 16.07 | |
| 17.08.2018 | Cum | S&P + Moody's | ↓ | 20.08 | 20.08 arife (yarım gün). t+2 = 28.08, arada 4 gün bayram var. |
| 14.06.2019 | Cum | Moody's | ↓ Ba3→B1 | 17.06 | |
| 12.07.2019 | Cum | Fitch | ↓ BB→BB- | 16.07 | 15.07 tatil. |
| 11.09.2020 | Cum | Moody's | ↓ B1→B2 | 14.09 | |
| **11.02.2022** | Cum | **Fitch** | ↓ BB-→B+ | 14.02 | **1. TUR LİSTESİNDE YOK** (Bloomberg 11.02.2022, Garanti BBVA IR) |
| 08.07.2022 | Cum (arife) | Fitch | ↓ **B+→B** | 13.07 | 1. tur "BB-→B" yazmış. |
| 12.08.2022 | Cum | Moody's | ↓ B2→B3 | 15.08 | |
| 30.09.2022 | Cum | S&P | ↓ B+→B | 03.10 | 03.10'da TÜFE açıklandı, gün-içi +%6. |
| 08.03.2024 | Cum | Fitch | ↑ B→B+ | 11.03 | |
| 03.05.2024 | Cum | S&P | ↑ B→B+ | 06.05 | |
| 19.07.2024 | Cum | Moody's | ↑ B3→B1 | 22.07 | |
| 06.09.2024 | Cum | Fitch | ↑ B+→BB- | 09.09 | |
| 01.11.2024 | Cum | S&P | ↑ B+→BB- | 04.11 | |
| 25.07.2025 | Cum | Moody's | ↑ B1→Ba3 | 28.07 | |

- **Cuma mı, hafta içi mi?** Olayların 17'si Cuma akşamı, ABD kapanışından sonra (AB CRA takvimi). 3'ü hafta içi ve takvim dışı (S&P 2016, Moody's 2018-03, S&P 2018-05).
- **Not mu, görünüm mü?** 20'sinin tamamı not kademesi değişikliği. 1. turun 19 olayı da sadece not değişikliğiydi (görünümler ayrı tutulmuş). Bu doğru.
- **2026'da not değişikliği yok:**
  - Fitch 23.01.2026'da görünümü pozitife çevirdi, 10.04.2026'da takvim dışı bir kararla durağana geri aldı (evrensel, QNB Invest, BloombergHT).
  - Fitch 17.07 ve Moody's 24.07 kararlarında not değişmedi.
  - S&P 16.10.2026'da değerlendirme yayımlamadı; not BB-/durağan.
- **Eksik görünüm olayları** (1. tur listesinde yok): S&P 06.05.2016 (+), S&P 04.11.2016 (+), S&P 27.01.2017 (−), Fitch 01.11.2019 (+), Fitch 19.02.2021 (+), Fitch 02.12.2021 (−), S&P 10.12.2021 (−), Fitch 10.04.2026 (−).

## 2. (a) Yeniden üretim
Kural: Pazartesi (tepki günü) açılışta notun tersi yönde gir, t+2 kapanışta çık, 15 bps maliyet.

| Küme | Endeks | Tümü | IS 2014–20 | OOS 2021–26 | İsabet |
|---|---|---|---|---|---|
| 1. tur 19 olay | XU100 | **+215,4 (t 3,74)** | +182,5 (t 2,53, n=10) | +251,9 (t 2,67, n=9) | %84 |
| 1. tur 19 olay | XBANK | +320,3 (t 3,56) | +184 (t 1,55) | +472 (t 3,80) | %74 |
| Düzeltilmiş 20 olay | XU100 | **+207,9 (t 3,77)**, medyan +161 | +182,5 (t 2,53) | +233,3 (t 2,69, n=10) | %85 |
| Düzeltilmiş 20 olay | XBANK | +302,5 (t 3,47) | +184 (t 1,55) | +421 (t 3,45) | %70 |
| Düzeltilmiş 20 olay | XU030 | +211,8 (t 3,48) | +180 (t 2,36) | +243 (t 2,49) | %75 |

1. turun rakamları ondalığına kadar aynı çıktı. Eksik Fitch 2022-02 olayı eklenince olay başına getiri +81 bps; sonuç değişmiyor.

## 3. (b) Zamanlama ve ileriye bakma denetimi
- **Sinyal pozisyondan önce biliniyor mu?** Evet.
  - Kararlar BIST kapanışından (15:00 UTC) sonra açıklanıyor, Cuma olaylarında ABD kapanışından da sonra.
  - Pozisyon bir sonraki BIST seansının açılışında alınıyor: Cuma olayında ~2,5 gün sonra, hafta içi olayda ~15 saat sonra.
  - Yön (artırım/indirim) açıklamayla birlikte belli oluyor; çıkış günü sabit.
- **VİOP akşam seansı:** Seans 23:00 TSİ'de (20:00 UTC) bitiyor; kararlar bundan sonra açıklanıyor. Cuma akşam seansında karar öncesi giriş mümkün değil, karar sonrası giriş de mümkün değil.
- **Açılış fiyatı (tuzak 3):** Endekslerde 2014+ açılış fiyatının bir önceki kapanışa eşit olduğu günler %0–2 (2015'te %9,5). Açılış fiyatına bağımlılık şu girişlerle test edildi:
  - **t0 kapanışında giriş → t+2:** XU100 +147 bps net (t 3,55), plasebo p<0,01.
  - **t+1 açılışında giriş:** +126 (t 3,42).
  - **İlk saatlik bar kapanışında giriş (≈10:30 TSİ, sadece 2024+ olaylar, n=6):** XU100 +134 (t 1,7); açılış girişi +171. XBANK +226'ya karşı +330.
  - **Gerçek F_XU030 vadelisi** (BIST VİOP bülteni, en çok işlem gören vade):
    - t0 uzlaşma → t+2 uzlaşma, 4 bps: **+152 bps, t 3,10, isabet %76, n=17**. IS +156 (t 1,9, n=7), OOS +150 (t 2,33, n=10).
    - 09:30 VİOP açılışında giriş (akşam seansı öncesi olaylar, n=16): +269 (t 3,39).
- **Getirinin günlere dağılımı** (XU100, işaretli, brüt):

  | Bileşen | Ortalama | t |
  |---|---|---|
  | Pazartesi gap (işlenemez) | −30 bps | −1,1 |
  | Pazartesi gün-içi | +61 | 1,4 |
  | t+1 | +71 | 2,96 |
  | t+2 | +91 | 2,77 |
  | t+3 | ≈0 | — |
  | t+4 | ≈0 | — |

  Yani piyasa karara açılışta neredeyse hiç tepki vermiyor (haber beklenmiş). Ters yöndeki hareket t+1 ve t+2'de gerçekleşiyor.
- **Ön-dönem iddiası:** 1. turdaki +234 bps çift sayım hatasından geliyordu (bkz. Bölüm 0). Ayrıca ön-dönem hareketi sonraki geri dönüşü AÇIKLAMIYOR:
  - Regresyon: strat = a + b·(−yön·pre5) için a = +229 bps (t 3,71), b = 0,03 (t 0,24).
  - Ön-dönemi not yönünde OLMAYAN 6 olayda da +219 bps var.
  - 20 günlük ön-trend ile: a = +232 (t 4,39).

## 4. (c) Sağlamlık
**Plasebo** (aynı yön etiketleri ve aynı haftanın günü; olay günü ±3..52 hafta kaydırılıyor):
- XU100: gerçek +223 brüt; plasebo ortalaması +19 (sd 52, %95 dilimi 106), p = 0/100 kaydırma.
- Her olay bağımsız rastgele kaydırılınca (10.000 çekiliş): tümü p=0,0004, IS p=0,0015, OOS p=0,015.
- XBANK: p=0,0001.
- Yerel plasebo (±3..8 hafta): en yüksek değer +139, gerçek +223.

**Olaydan bağımsız kısa vadeli geri dönüş yok:**
- Her Pazartesi önceki 5 günün tersine girip t+2'de çıkmak: −13 bps (t −1,2). Tüm günlerde −12 (t −2,6).
- Pazartesi ve |pre5|>%3 koşulunda: −7 bps.
- Dolayısıyla etki genel bir geri dönüş anomalisi değil.

**Vade duyarlılığı** (XU100, açılış girişi, net):

| Çıkış | Getiri | t |
|---|---|---|
| t0 | +46 | 1,06 |
| t+1 | +117 | 2,15 |
| t+2 | +208 | 3,77 |
| t+3 | +207 | 2,96 |
| t+5 | +247 | 2,86 |
| t+10 | +297 | 2,16 |

Sonuç tek bir vadeye bağlı değil; t+2 en yüksek t değerini veriyor ve sonradan seçilmiş.

**Alt kümeler** (XU100, net):
- Sadece Cuma olayları: +253 (t 4,47, n=17). Hafta içi olaylar: −46 (n=3).
- İndirimler (uzun): +224 (t 3,1, n=14). Artırımlar (kısa): +171 (t 2,11, n=6).
- Ajanslara göre: Moody's +216 (8/8 isabet), Fitch +260 (7/7), S&P +188 (t 1,13, medyan +2; S&P zayıf).
- 2016-07 ve 2018-08 hariç: +203 (t 3,54). Arada tatil olmayanlar: +219 (t 3,44).
- Tek olay çıkarma (leave-one-out): t 3,45–4,37 arasında kalıyor.
- En büyük 3 olay (2022-10 +850, 2018-08 +519, 2024-03 +453) çıkarılınca: +137 (t 3,2).
- Parametrik olmayan testler: Wilcoxon p=0,0004, işaret testi p=0,003. Bootstrap %95 GA: [+106, +317].

**USD bazlı:**
- XU100 − USDTRY: +166 (t 2,25). FX kapanışı ~24:00 UTC olduğundan yaklaşık bir hesap.
- **Bağımsız veri olarak TUR ETF** (NASDAQ, USD; Pazartesi ABD açılışı → t+2 kapanış, 15 bps): +159 (t 2,78), IS +159 / OOS +159. Kapanış girişi: +124 (t 2,89).

**XBANK:**
- XBANK − XU100 fazlası +95 (t 1,59, medyan +6, isabet %50). XBANK'ın büyüklüğü beta/kaldıraçtan geliyor.
- F_XLBNK vadelisi (n=11): +188, t 1,54, medyan −31. İllikit (60–2.000 sözleşme) ve işlenebilirliği zayıf.

**Görünüm/izleme olayları (n=20, 8 yeni olay dahil):**
- XU100 t+2: +11 bps (t 0,16); IS −173, OOS +195.
- 1. turun 13 görünüm olayında: −85 (t −1,1).
- **Mekanizma görünüm değişikliklerine genellenmiyor.**

## 5. (d) Yıllara göre (XU100, 15 bps, düzeltilmiş 20 olay)

| Yıl | 2016 | 2017 | 2018 | 2019 | 2020 | 2022 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|
| Ortalama (bps) | +77 | +358 | +141 | +375 | +1 | +327 | +198 | +36 |
| n | 2 | 1 | 4 | 2 | 1 | 4 | 5 | 1 |

- 8 yılın 8'i pozitif (2020 ≈ 0).
- XBANK'ta 7/8 pozitif (2020: −113).
- 2014, 2015, 2021, 2023 ve 2026'da not değişikliği yok.

## 6. (e) Maliyet duyarlılığı (düzeltilmiş 20 olay, açılış → t+2)

| Maliyet (bps) | 0 | 2 | 4 | 8 | 15 | 25 | 50 | 100 |
|---|---|---|---|---|---|---|---|---|
| XU100 (bps) | 223 | 221 | 219 | 215 | 208 | 198 | 173 | 123 |
| t | 4,04 | — | 3,97 | — | 3,77 | — | 3,14 | — |

- Başabaş maliyet ~223 bps. t=2'yi koruyan en yüksek maliyet ~113 bps.
- XBANK: 50 bps maliyette +268. XU030: başabaş ~227.
- Maliyet sonucu belirleyen faktör değil. Asıl sınır olay sayısı: yılda ~2 olay, olay başına ~3 gün pozisyon.

## 7. Karşı argümanlar ve sınırlamalar
1. **Küçük örneklem:** n=20 ve olaylar kümeli (2018'de 6 ayda 4 olay, 2024'te 8 ayda 5 olay). Etkin bağımsız gözlem sayısı daha düşük. Yıllık düzeyde 8/8 pozitif olması bunu kısmen dengeliyor.
2. **Sonradan seçim:** "Kontraryen" yönü ve "t+2" vadesi 1. turda tam örneklem görüldükten sonra seçildi. IS/OOS ayrımı gerçek bir ileri test değil. Yaklaşık 20–40 varyant düzeltmesi yapılsa bile plasebo p≈0,0004 × 40 ≈ 0,016.
3. **Rejim karışması:** IS dönemindeki tüm olaylar indirim (uzun pozisyon, kriz diplerine yakın), OOS'taki artırımların hepsi 2024–25'te. Plasebo bu yön-dönem yapısını kontrol ediyor ve etki yine kalıyor. Ama iki ayrı hikâyenin ("kriz dibi tepkisi" ve "2024 haberi sat") aynı mekanizma olduğu kanıtlanmadı.
4. **Mekanizma tutarsızlığı:** Görünüm değişikliklerinde etki yok. Ön-dönemde not yönünde hareket de anlamlı değil (t 1,9). "Söylentiyle al, haberle sat" hikâyesi doğrudan desteklenmiyor. Elimizde sadece "karar sonrası 2 gün ters hareket" olgusu var.
5. **Karışan olaylar:**
   - 03.10.2022'deki TÜFE günü tek başına +850 bps getiriyor.
   - 21.07.2016'da OHAL ilanı ve 20.08.2018'de bayram aynı pencereye denk geliyor.
6. **S&P zayıf:** n=6, medyan ≈ 0. Etki ağırlıkla Moody's ve Fitch olaylarından geliyor.
7. **Gelecek olaylar:** Takvim belli (AB CRA kuralı). Bir sonraki not değişikliğinin yönü ve tarihi bilinmiyor; 2026'da hiç not değişikliği olmadı.

## 8. TradingView
- Endeksler: BIST:XU100, BIST:XU030, BIST:XBANK.
- VİOP endeks vadelisi: BIST:XU0301! (? sürekli kontrat kodu doğrulanmalı).
- Banka endeks vadelisi: BIST:XLBNK1! (?).
- Bağımsız kontrol ETF'i: NASDAQ:TUR.

## 9. Kaynaklar
- https://tradingeconomics.com/turkey/rating · https://countryeconomy.com/ratings/turkey
- Bloomberg 2022-02-11 "Turkey's Sovereign Rating Cut Further Into Junk by Fitch" · Garanti BBVA IR "Announcement regarding Fitch Ratings" (2022-02, 2022-07, 2024-09) · bianet "Fitch lowers Turkey's credit rating"
- Bloomberg 2024-03-08, 2024-09-06 (Fitch artırımları) · invest.gov.tr
- Al Arabiya/Turkish Minute 13.07.2019 (Fitch) · CNBC 20.07.2016 (S&P, 11:58 EDT) · CNBC 20.08.2016 (Fitch görünüm)
- Duvar English / bianet (Fitch 01.11.2019) · Hurriyet DN (Fitch 19.02.2021) · fxstreet 02.12.2021 (Fitch) · capital.com.tr (S&P 10.12.2021)
- ntv (Fitch 23.01.2026) · evrensel 11.04.2026, QNB Invest, BloombergHT (Fitch 10.04.2026 takvim dışı karar) · foreks 17.10.2026 (S&P değerlendirme yayımlamadı)
