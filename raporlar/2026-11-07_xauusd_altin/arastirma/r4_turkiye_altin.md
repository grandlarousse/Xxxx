# r4_turkiye_altin — Türkiye'de altın fiyatı nasıl oluşur, nasıl tahmin edilir

Tarih: 07.11.2026. Kapsam: gram altın (TL), Kapalıçarşı/fiziki, banka altın hesabı, BIST Kıymetli Madenler ve Kıymetli Taşlar Piyasası (KMKTP), VİOP gram altın (F_XAUTRYM) ve VİOP ons altın (F_XAUUSD) arasındaki fiyat ilişkileri. 1–5 gün ve 1–3 ay ufukta pratik tahmin çerçevesi.

**Yöntem notu.** Bu raporda üç tür kanıt var:
- (a) Birincil belgeler: BIST duyuruları ve aylık raporu, TCMB faiz tabloları, HMB duyurusu, WGC Q3 2026 Gold Demand Trends, Resmî Gazete özetleri.
- (b) İkincil haber kaynakları: Reuters, Bloomberg HT ve Türk basını. Bunlar "orta/düşük güven" olarak işaretlendi.
- (c) Ortak paneldeki kendi hesaplarım: VİOP bülteni, Dukascopy 15:00 UTC spot, Yahoo. Kodlar `$S/out/r4_turkiye_altin/`: `stats.py`, `stats2.py`, `decomp.py`, `spotdecomp.py`, `fx_regime.py`, `fx_forecast.py`, `tr_leadlag.py`.

Çalışma sırasında oturumun web arama bütçesi tükendi. Bu yüzden **Türkiye'ye özel akademik literatür taraması yapılamadı** (bkz. §11). Akademik bulgu yerine kendi ölçümlerim kondu.

---

## 0. Kısa özet (yük taşıyan bulgular)

1. **Formül doğru, ama hangi "gram altın"?** gram_TL ≈ ons_USD × USDTRY / 31,1035 × (1 + p). Burada p, ilgili piyasanın primi. Bu prim:
   - VİOP gram altında ≈ 0. VİOP sözleşmesi uluslararası pariteye arbitrajla bağlı.
   - BIST KMKTP toptan piyasasında Ekim–Kasım 2026'da ≈ 0 (−%0,6 ile +%0,4 arası, kendi hesabım).
   - Kapalıçarşı perakendede prim + alış-satış makası birlikte, ±%1 ile +%8 arası dalgalanıyor.
2. **2024–2026'da gram altın riskinin ≈ %97'si onstan geliyor.** VİOP vadeli getirileriyle ölçtüm:
   - 2024–2026 günlük varyans payları: ons %96,9, kur %4,3.
   - 2026'da ons %101, kur %0,3. Kovaryans terimi küçük negatif.
   - 2017–2021'de tablo tersti: günlük varyansın %86'sı kurdan geliyordu.
   - Sonuç: bugün gram altını tahmin etmek ≈ onsu tahmin etmek + bilinen kur kaymasını eklemek.
3. **USDTRY 2026'da neredeyse deterministik bir kayma.** Ocak–Ekim 2026 (Dukascopy 15:00 UTC):
   - Günlük ortalama +%0,073, standart sapma %0,090.
   - En büyük günlük artış +%0,44. Günlerin %89'unda kur yükseldi.
   - Nisan 2025'ten beri |günlük değişim| > %0,5 olan **hiç gün yok**.
   - Aylık artış 2026'da %1,15–1,91 (Yahoo ay sonu). Kayma Nisan'dan sonra hızlandı (Q1 ≈ %1,15–1,18, Nisan–Ekim ≈ %1,56–1,91).
4. **Kur için en iyi kısa vadeli tahminci son 20 günün kayma hızı, VİOP forward'ı değil.** Nisan 2025–Ekim 2026:
   - 5 günlük USDTRY değişiminde 20 günlük kayma tahmininin RMSE'si %0,207. VİOP USDTRY baz-ima tahmininin RMSE'si %0,307.
   - Forward 5 günde ortalama 0,24 puan fazla değer kaybı öngördü.
   - Yıllık bazda VİOP'un ima ettiği değer kaybı gerçekleşenin hep üstündeydi: 2024'te %44,5'e karşı %19,0; 2025'te %39,2'ye karşı %21,8; 2026'da %31,6'ya karşı %19,8.
5. **Kuyruk riski siyasi şoklarda.** 19.03.2025'te USDTRY 15:00→15:00 UTC +%3,33 arttı. Bu, Ağustos 2023'ten beri tek >%2'lik gün. TCMB tepkisi:
   - 20 Mart 2025'te gecelik borç verme faizini %44'ten %46'ya çıkardı.
   - 17 Nisan'da politika faizini %42,5'ten %46'ya çıkardı (TCMB tablosunda yürürlük 18.04.2025).
   - Mart 2026 İran savaşında kur kontrollü kaldı (VİOP USDTRY günlük |ret| < %0,6). Bunun bedeli: TCMB tahminen 60 ton altın sattı/swapladı, 26 milyar $ döviz sattı (ikincil kaynaklar).
6. **Politika faizi** (TCMB tablosu, yürürlük tarihleri): %50 (22.03.2024) → 47,5 → 45 → 42,5 (07.03.2025) → 46 (18.04.2025) → 43 → 40,5 → 39,5 → 38 → 37 (23.01.2026) → **36 (23.10.2026)**. Gecelik borç verme %39, borç alma %34,5.
7. **VİOP gram altın, VİOP ons × VİOP USDTRY / 31,1035 sentetiğiyle neredeyse birebir aynı.** Aynı vade ayında fark:
   - 2025'te ortalama +%0,018 (std %0,084), 2026'da +%0,020 (std %0,081).
   - 2026'da %5–95 bandı −%0,107 / +%0,162.
   - Bireysel yatırımcıya arbitraj fırsatı yok.
   - İstisna: Ağustos–Eylül 2018 kur krizi. Fark 31.08.2018'de %3,84'e çıktı.
8. **VİOP gram altın yüksek TL carry'si taşır.** Long pozisyon her seans spot paritenin gerisinde kalır:
   - Nisan 2025–Ekim 2026'da spot sentetiğe göre ortalama −%0,166/seans; 3 seansta −%0,50, 5 seansta −%0,83.
   - Takvim yayılımından ima edilen yıllık carry (medyan): gram altın 2024'te %57,5, 2025'te %44,8, 2026'da %43,4. USDTRY 47,3 / 38,7 / 34,4.
   - VİOP USDTRY long (zincirlenmiş aktif kontrat, log getiri): 2024 −%22,2, 2025 −%16,7, 2026 YTD −%12,1.
   - Yani TL'nin reel değerlenme politikası altında "gram altın vadeli long" = "ons long + kaybettiren USD/TRY long".
9. **VİOP ons altın da ABD faizinden yüksek carry ile işlem görüyor.** 2026 takvim yayılımı medyanı %7,2, 3 aylık UST ortalaması %3,84. Long pozisyonda spot sentetiğe göre −%0,034/seans (5 seansta −%0,17). Bu, kendi tahminim; nedeni muhtemelen yurt içi long talebi ve geri vadelerin sığlığı.
10. **İthalat kotasını Ticaret Bakanlığı değil, Hazine ve Maliye Bakanlığı koydu** (görev metnindeki varsayımın düzeltmesi):
    - Başlangıç 07.08.2023, aylık toplam kota. Haberlere göre 12 ton (uzun dönem 8 ton ortalamanın 1,5 katı).
    - 22.09.2023'ten itibaren kapsam ek GTİP'lere genişletildi (BIST, 25.09.2023).
    - Nisan 2024'ten itibaren Ziraat ve Vakıf Katılım'a kuyumcular için ayrıca kota verildi (HMB 2024/KM-4).
    - 2026'da kota bağlayıcı değil: KMKTP ithalatı Ocak–Eylül 2026'da 51,1 ton (aylık 1,1–10,1 t; Ağustos 1,08 t, Eylül 1,87 t).
11. **Yerel prim tarihçesi:**
    - 2023'te kota sonrası 150 $/oz zirve (Metals Focus).
    - Mart 2024'te 200 $/oz, sonra 15–25 $/oz; Eylül 2024'te 20–50 $/oz.
    - Sonbahar 2025'te > %5. Aralık 2025'te "tarihsel ortalama ≈ %1,5"e döndü (Reuters).
    - Ocak 2026 zirvesi kg başına 12.500 $'a kadar (≈ %7–8, kendi çevirim).
    - Q3 2026'nın çoğunda **iskonto**, Eylül sonunda hafif prim (WGC).
12. **Türkiye dünya fiyatını hane talebiyle değil, TCMB işlemleriyle etkileyebilir.**
    - Q3 2026'da Türkiye bar-sikke 12,6 t + mücevher 6,9 t = 19,5 t. Bu, küresel 1.369 tonluk talebin ≈ %1,4'ü.
    - Ama Mart 2026'da TCMB ≈ 60 t sattı/swapladı (WGC verisine dayanan haberler). Aynı ay altın 2 Mart'tan 23 Mart'a ~%17 düştü (5.332 → 4.416 $, 15:00 UTC). Nedensellik kanıtlanmadı.
13. **Vergi/maliyet:**
    - VİOP'ta yerleşik gerçek kişiye %10 stopaj (r1).
    - Banka altın hesabında fiziki teslimatsız alımlar 17.03.2025'ten beri "kambiyo işlemi" sayılıyor (9595 sayılı CBK). Alımda binde 2 BSMV kesiliyor.
    - Kapalıçarşı'da makas tipik olarak birkaç yüzde. Örnek, düşük güven: Mayıs 2026'da alış 6.749 / satış 6.989 TL, %3,5.
14. **Akşam seansı:** BIST duyurusu 30572 (19.11.2024) ekindeki Prosedür md. 7, akşam seansındaki sözleşmeleri sayıyor: endeksler, Dolar/Ons Altın, Gümüş, Platin, Paladyum (+ 06.12.2024'ten bakır).
    - **TL/gram altın ve USDTRY vadeli listede yok.** Yani 18:10 TSİ'den sonra VİOP'ta altına ancak F_XAUUSD ile tepki verilebilir.
    - 30572'nin konusu bakır. Altın akşam seansı 18.09.2020'de başladı (BIST duyurusu 12590; r1).
15. **Türkiye'ye özgü yerel sinyallerin hiçbiri ertesi 1/3/5 günün VİOP XAUUSD getirisini öngörmüyor.** Test ettiğim 6 öngörücü × 3 ufuk = 18 test, kayıtlı. Öngörücüler: gram–sentetik prim (seviye ve değişim), USDTRY günlük değişimi, gram altın hacim oranı, açık pozisyon değişimi, VİOP takvim carry zenginliği.
    - En güçlü sonuç: USDTRY değişimi, h=1, OOS t = −2,12. Ama IS t = −0,12 ve 18 test var. Kayda değer değil.

---

## 1. Türkiye'deki altın fiyat zinciri

**Temel denklem** (1 troy ons = 31,1035 g):

gram_TL(piyasa) = ons_USD × USDTRY / 31,1035 × (saflık) × (1 + p_piyasa) ± makas/2

| Fiyat | Neyi izler | Prim/iskonto | Saat | Not |
|---|---|---|---|---|
| "Spot gram altın" (ekranlardaki XAU/TRY, "serbest piyasa") | ons × USDTRY / 31,1035 | ≈ 0 (tanım gereği) | 7/24'e yakın | Haberlerdeki "spot gram" genelde bu |
| VİOP gram altın (F_XAUTRYM) | Aynı vade ayının VİOP ons × VİOP USDTRY / 31,1035 sentetiği | ≈ 0, ama **vade carry'si içerir** | 09:30–18:10 TSİ; akşam seansı **yok** (Prosedür md. 7) | Vade sonu = LBMA PM × TCMB 15:30 (alış+satış)/2 ÷ 31,1035 (r1, Prosedür Ek-1) |
| VİOP ons (F_XAUUSD) | Spot XAUUSD + USD carry | Küçük pozitif ek carry (§5) | 09:30–18:10 + 19:00–23:00 TSİ | Vade sonu LBMA PM (r1) |
| BIST KMKTP standart altın (995/1000, TL/kg, USD/ons) | Toptan; bankalar, KMAK'lar, TCMB | Ekim–Kasım 2026 ≈ 0 (§2.4) | Seans saatleri bu çalışmada teyit edilemedi | İthalat bu piyasa üyelerince yapılır |
| Banka altın hesabı (kaydi) | Banka kendi kotasyonu; KMKTP/spot | Banka makası | Banka saatleri / 7/24 | Alımda binde 2 BSMV (§7) |
| Kapalıçarşı has/gram (fiziki) | KMKTP + fiziki arz-talep | **Değişken prim**: −%1 ile +%8 | Çarşı saatleri | Haberlerdeki "makas" = prim + alış-satış farkı |
| Çeyrek/Cumhuriyet (ziynet) | Fiziki altın + işçilik + talep | Ek ziynet primi | Çarşı | Darphane ağırlık/ayar spesifikasyonu birincil kaynaktan teyit **edilemedi** |

**Pratik sonuç.** Kullanıcının işlem yaptığı F_XAUUSD ve F_XAUTRYM, uluslararası pariteye bağlı. Kapalıçarşı primi bu sözleşmelerin fiyatına **girmez**:
- Vade sonu uzlaşması LBMA ve TCMB kuruna dayanır.
- Gün içinde ise ons ve USDTRY vadelileriyle arbitraj vardır (§5).

Prim yalnızca fiziki altın tutan yatırımcının TL getirisini ve kuyumcuların hedge kararlarını etkiler.

---

## 2. Yerel prim: tanım, tarihçe, sürücüler, 2026 düzeyi

### 2.1 Ölçüm tuzakları
- Basındaki "Kapalıçarşı–spot makası", çoğunlukla **Kapalıçarşı satış fiyatı ile spot gram** arasındaki farktır. Bu sayı alış-satış farkını da içerir. Prim için orta fiyat (alış+satış)/2 kullanılmalı.
- 995/1000 külçe ile 999,9 has altın arasında yaklaşık %0,5 saflık farkı var.
- Saat uyuşmazlığı da sorun. Ons gün içinde %1–2 oynayabiliyor. Örneğin 05.11.2026'da 12:00–15:00 UTC arasında 4.112–4.133 $.

### 2.2 Prim tarihçesi (kaynaklı)

| Dönem | Prim / fark | Bağlam | Kaynak (güven) |
|---|---|---|---|
| 2022 | — | Ithalat 379 t (o dönem 3. en yüksek). KMKTP kaydı 264,8 t | Metals Focus PMW 94 (20.09.2024); BIST Eylül 2026 raporu (yüksek) |
| Ocak 2023 | — | Aylık ithalat rekoru 83 t | Metals Focus (orta) |
| Şubat 2023 | Darphane altın sertifikası BIST'te **%21 prim** (rekor) | Deprem + seçim öncesi talep | Gedik Yatırım, Bloomberg bülteni üzerinden (düşük; birincil teyit yok) |
| Şubat sonu–Mayıs 2023 | 20–30 $/oz; kota sonrası **150 $/oz**, Nisan sonu–Mayıs ≈ 100 $/oz | TCMB ithalatı kısıtladı, Mart–Mayıs 2023'te BIST üzerinden **159 t** sattı | Metals Focus (orta) |
| Haziran 2023 seçim sonrası | ≈ parite | Sert TL değer kaybı, faiz %8,5 → %15 | Metals Focus (orta) |
| 07.08.2023 | — | HMB aylık işlenmemiş altın ithalat kotası (12 t; haber) | BIST 28.03.2024 ve 25.09.2023 duyuruları; HMB açıklaması (yüksek: kota var; orta: 12 t) |
| 08.08.2023 | — | FTA'sız ve AB dışı ülkelerden altın mücevher/parça ithalatına **%20 ek mali yükümlülük** | Asharq Al-Awsat/Reuters (orta) |
| Aralık 2023 → Mart 2024 | 40 $/oz → **200 $/oz** | Yeni düzenleme, Mart 2024 yerel seçim öncesi talep | Metals Focus (orta) |
| Nisan–Eylül 2024 | 15–25 $/oz, Eylül 2024'te 20–50 $/oz | Faiz %50, TL carry cazip. Kayıt dışı arz (≈25 t yarı-mamul ithalatı) | Metals Focus (orta) |
| Sonbahar 2025 | **> %5** | Ons Eylül başı 3.500 $'dan Ekim'de 4.378 $ rekora | Reuters, Daily Sabah 08.12.2025 üzerinden (orta) |
| Aralık 2025 | ≈ **%1,5 ("tarihsel ortalama")** | KKM bakiyesi ≈ 0,6 milyar $. Talep normalleşti, Kapalıçarşı'ya arz geldi | Reuters, Daily Sabah üzerinden (orta) |
| Ocak 2026 | Kg başına **12.500 $'a kadar** (≈ 389 $/oz, ons 5.000–5.500 $ iken ≈ %7–8) | Ons 29.01.2026'da ≈ 5.496 $ zirve (15:00 UTC) | GZT 25.02.2026 (düşük-orta) |
| 27.01.2026 | Satış 7.320 TL / spot 7.070 TL ≈ **%3,5** (≈ 5.750 $/kg) | "Arz kısıtı + fiziki talep" | hisse.net, Türkiye Gazetesi üzerinden (düşük-orta) |
| 25.02.2026 | 7.530 / 7.310 ≈ **%3,0** (≈ 5.000 $/kg) | Kâr satışı, makas daraldı | GZT (düşük-orta) |
| Q3 2026 (Temmuz–Eylül) | **İskonto** (çeyreğin çoğu), Eylül sonunda hafif prim | Pahalıdan alanlar beklemede. Ağustos rallisinde kâr satışı. 6.400–6.500 TL/g (≈ 4.000 $/oz) civarında dip alımı | WGC GDT Q3 2026, 03.11.2026 (yüksek) |
| 12.10, 20.10, 05.11.2026 | KMKTP kapanışı ile sentetik arası **−%0,6 … +%0,4** | KMKTP standart altın: 6.595.001, 6.560.000, 6.642.000 TL/kg | Fiyatlar: haber derlemesi. Sentetik: Dukascopy 12–15 UTC × Yahoo USDTRY, kendi hesabım (orta; saat ve saflık belirsiz) |

**2026 güncel prim düzeyi.** Kasım 2026 başında toptan (KMKTP) prim ≈ 0, perakende prim büyük olasılıkla düşük tek hane. Bunun dayanakları:
- WGC'ye göre Q3'te iskonto, Eylül sonunda hafif prim vardı.
- İthalat Ağustos–Eylül'de 1–2 t'a düştü. Yerel fiyat dünya fiyatının altındayken ithalat yapmanın arbitraj getirisi yok, düşüş bununla tutarlı.

Kapalıçarşı orta fiyatıyla günlük ölçüm **yapılamadı**, çünkü veri setimizde zaman damgalı Kapalıçarşı serisi yok.

### 2.3 Primin sürücüleri

1. **İthalat kısıtları.** Arz tarafının tavanını belirler. Kota bağlayıcı olduğunda prim, ithalat lisansının kira değeri gibi davranır. 2023'te 150 $, Mart 2024'te 200 $/oz.
   - 2026'da kota bağlayıcı değil. Ocak–Eylül 2026 aylık KMKTP ithalatı (kg): Oca 7.792, Şub 10.067, Mar 8.512, Nis 5.294, May 4.871, Haz 7.147, Tem 4.455, Ağu 1.080, Eyl 1.867 (BIST Eylül 2026 raporu).
   - Çelişki: Aralık 2024 (14.557 kg), Nisan 2025 (15.229 kg), Ekim 2025 (13.433 kg) ve Kasım 2025 (13.857 kg) 12 t'u aşıyor. Banka kotası (2024/KM-4), DİR/bedelsiz ithalat istisnaları ya da kota artışı olabilir. Hangisi olduğu **bulunamadı**.
2. **Hane talebi şokları.** Prim, ons rallileriyle birlikte açılıyor (Ekim 2025, Ocak 2026). Ons düşüşü ve kâr realizasyonuyla iskontoya dönüyor (Q3 2026). Yani prim, onsun son 1–3 aylık momentumuna **pro-siklik**. Bu bizim veride test edilmedi (veri yok).
3. **TL alternatiflerinin getirisi.** Politika faizi %50 iken (2024) talep düştü, prim 15–25 $'a indi (Metals Focus). KKM'nin kapanışı da bir etken:
   - Tüzel kişiler için yeni hesap/yenileme 15.02.2025'te bitti, gerçek kişiler için 23.08.2025'te (YUVAM hariç).
   - KKM bakiyesi ≈ 140 milyar $ (Ağustos 2023) → 0,6 milyar $ (Aralık 2025). Böylece "KKM'den çıkan para altına" kanalı 2026'da tükendi.
4. **TCMB'nin arz rolü.**
   - 2023'te BIST üzerinden 159 t sattı (Mart–Mayıs; Metals Focus).
   - Mart 2026'da swap ve satış yaptı. Satış KMKTP'ye mi, uluslararası piyasaya mı yapıldı? Ayrım **bulunamadı**.
   - Zorunlu karşılıkta altın tesis imkânı var. Bankaların altın hesaplarındaki metal TCMB rezervine taşınıyor.
   - Aralık 2025'te kıymetli maden depo hesaplarında ZK oranı: vadesiz/≤1 ay %28 → %30, uzun vadeler %24–28 → %26 (Bloomberg HT, ikincil).
   - Temmuz 2026'da YP mevduatında ZK %30 → %32 ve %26 → %28 (17.07.2026'dan). Altın hesaplarının bu değişikliğe dahil olup olmadığı **teyit edilemedi**.
5. **Siyasi/kur stresi.** Seçimler (Mart 2023, Mart 2024), 19.03.2025 ve Mart 2026 savaşı. TL panik dönemlerinde fiziki talep primi açıyor. Ama TCMB kuru tuttuğu sürece etki kısa sürüyor.

### 2.4 Toptan piyasa (BIST KMKTP) göstergeleri (BIST Eylül 2026 aylık raporu)
- Aylık ortalama altın işlem miktarı: 2025'te 25.076 kg, Ocak–Eylül 2026'da 30.039 kg. İşlem hacmi 113.049 → 201.164 milyon TL.
- Ortalama altın fiyatı (KMKTP): 2025'te 3.479 $/oz, 2026 (Eylül sonuna kadar) 4.529 $/oz. Raporda "%94 değişim" yazıyor ama doğru oran ≈ %30. Raporda yazım hatası olası.
- Yıllık ithalat: 2022'de 264.848 kg, 2023'te 318.978 kg, 2024'te 125.917 kg, 2025'te 126.272 kg, 2026 (Ocak–Eylül) 51.083 kg.
- Kıymetli maden depo hesapları (rapor tarihi): 4.735.689 milyon TL. 6.600 TL/g ile kabaca **≈ 717 ton** altın eşdeğeri (kendi çevirim).
- Darphane ziynet/sikke basımı aylık ortalaması: 2025'te 4.143 kg, 2026'da 4.529 kg.

---

## 3. USDTRY rejimi 2024–2026

### 3.1 TCMB faiz kararları (TCMB "1 Hafta Repo" ve "Faiz Oranları" tabloları; tarih = yürürlük)

| Yürürlük | Politika (1 hf repo) | O/N borç verme | O/N borç alma |
|---|---|---|---|
| 22.03.2024 | 50,00 | 53,00 | 47,00 |
| 27.12.2024 | 47,50 | 49,00 | 46,00 |
| 24.01.2025 | 45,00 | 46,50 | 43,50 |
| 07.03.2025 | 42,50 | 44,00 | 41,00 |
| 21.03.2025 (olağanüstü) | 42,50 | **46,00** | 41,00 |
| 18.04.2025 | **46,00** | 49,00 | 44,50 |
| 25.07.2025 | 43,00 | 46,00 | 41,50 |
| 12.09.2025 | 40,50 | 43,50 | 39,00 |
| 24.10.2025 | 39,50 | 42,50 | 38,00 |
| 12.12.2025 | 38,00 | 41,00 | 36,50 |
| 23.01.2026 | 37,00 | 40,00 | 35,50 |
| 23.10.2026 | **36,00** | 39,00 | 34,50 |

**Mart 2026.** Politika faizi %37'de sabit kaldı (12 Mart PPK). TCMB 1 Mart 2026'da bir hafta vadeli repo ihalelerine **ara verdi**. Fonlama fiilen O/N %40'tan yapıldı. İhaleler Ağustos 2026 ortasında yeniden başladı (24.08.2026 ihalesi %37). Kaynak ikincil (Forbes TR, CNBC-e, Gedik bülteni), orta güven.

Bir sonraki PPK 10.12.2026 (CNBC-e takvimi; ikincil).

### 3.2 Kur şokları
- **19.03.2025 (İmamoğlu gözaltısı).** USDTRY Dukascopy 15:00 UTC'de +%3,33. VİOP USDTRY uzlaşmasında +%4,17. Gün içinde 42 TL görüldü (haber).
  - TCMB 20 Mart'ta olağanüstü toplanıp O/N borç vermeyi %46'ya çıkardı. 17 Nisan'da politika faizini %46'ya yükseltti.
  - Mart 2025 aylık kur artışı +%3,99 (Yahoo ay sonu).
  - TCMB'nin 19–21 Mart'taki döviz satışı kaynağa göre 12–26 milyar $ (FT, Forbes TR; ikincil).
  - Gram altın VİOP o gün +%4,86. Ons +%0,21 iken kur +%4,17 oldu. Tek gerçek "kur kaynaklı gram altın sıçraması" bu.
- **Mart 2026 (İran savaşı, 28.02.2026'da başladı).** VİOP USDTRY günlük getirileri 2 Mart–31 Mart 2026 arasında −%0,54 ile +%0,24 arasında kaldı.
  - TCMB 27 Şubat–19 Mart'ta ≈ 26 milyar $ döviz sattı (altın etkisinden arındırılmış).
  - Bloomberg'e göre iki haftada ≈ 60 t (≈ 8 milyar $) altın satıp swapladı. Reuters bankacı hesabına göre 42 t swap + 26 t satış.
  - Toplam rezervler 27 Mart haftasında 177,5'ten 155,3 milyar $'a düştü. Kaynaklar ikincil (CNBC-e, Medyascope, Bloomberg HT), orta güven.
  - O ay gram altını taşıyan şey ons oldu. 23.03.2026'da ons −%5,24, gram −%5,29.

### 3.3 Kendi ölçümüm: kayma hızı

**Yıl içi değişim (Dukascopy 15:00 UTC, ilk–son iş günü):**
- 2024: 29,725 → 35,353 (+%18,9)
- 2025: 35,305 → 42,963 (+%21,7)
- 2026: 43,038 → 49,946 (30.10.2026'ya kadar, +%16,1). Yahoo kapanışı 06.11.2026'da 50,153.

**Aylık değişim (Yahoo ay sonu, %):**

| Yıl | Oca | Şub | Mar | Nis | May | Haz | Tem | Ağu | Eyl | Eki | Kas | Ara |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 | 1,55 | 1,85 | **3,99** | 1,38 | 1,84 | 1,74 | 1,75 | 1,36 | 1,06 | 1,08 | 1,09 | 1,10 |
| 2026 | 1,17 | 1,15 | 1,18 | 1,56 | 1,61 | 1,63 | 1,85 | 1,57 | 1,58 | 1,91 | | |

Dukascopy ile 2024 aylık değişim aralığı −0,53 (Mayıs) ile +3,72 (Mart). Nisan–Mayıs 2024'te seçim sonrası kur yatay kaldı.

**Günlük istatistik (Dukascopy 15:00 UTC log değişim):**

| Dönem | Ortalama/gün | Std | |Δ|>%0,5 gün sayısı | Maks | Pozitif gün |
|---|---|---|---|---|---|
| 2024 | +0,072% | 0,265% | 14 | +1,16% | %66 |
| 2025 | +0,085% | 0,269% | 2 | +3,33% | %75 |
| Nis 2025–Eki 2026 | +0,069% | 0,110% | **0** | +0,47% | %84 |
| Oca–Eki 2026 | +0,073% | 0,090% | 0 | +0,44% | %89 |

**Forward/baz:**
- VİOP USDTRY aktif kontratın ima ettiği yıllık değer kaybı (aylık ortalama): Mart 2025'te %51,7, Mart 2026'da %39,5 (stres ayları). Ekim 2026'da %30,7.
- Bu, politika faizi %36 ile tutarlı: (1,36/1,04) − 1 ≈ %31.
- Gerçekleşen yıllıklaştırılmış değer kaybı ise ≈ %20. Forward'ın fazlası carry trade'in kazancı.

**Kısa vade tahmin performansı (Nisan 2025–Ekim 2026, USDTRY log değişimi):**

| Ufuk | Model | Sapma (bias) | RMSE |
|---|---|---|---|
| 1 gün | Son 20 gün kayma | −0,004% | **0,115%** |
| 1 gün | VİOP baz-ima | −0,046% | 0,152% |
| 1 gün | Değişim yok | +0,070% | 0,131% |
| 5 gün | Son 20 gün kayma | −0,020% | **0,207%** |
| 5 gün | VİOP baz-ima | −0,244% | 0,307% |
| 5 gün | Değişim yok | +0,347% | 0,381% |
| 21 gün | Son 20 gün kayma | −0,087% | **0,563%** |
| 21 gün | VİOP baz-ima | −1,040% | 1,148% |

**Sonuç.** VİOP USDTRY bazı, kurun beklenen yolunu değil **faiz farkını** gösteriyor. Kur yolu için en iyi tahmin, TCMB'nin uyguladığı son kayma hızı. Baz, "stres primi" göstergesi olarak kullanılabilir: Mart 2025'te ve Mart 2026'da sıçradı.

---

## 4. Gram altın TL getirisinin ayrıştırılması

### 4.1 Varyans payları (VİOP aktif kontrat aynı-kontrat uzlaşma getirileri: ons = F_XAUUSD, kur = F_USDTRY, gram = F_XAUTRYM)

Kontrol: gram − ons − kur kalıntısının günlük std'si 24,8 bp, ortalaması −0,8 bp.

| Dönem | Ufuk | Std gram | Std ons | Std kur | Ons payı | Kur payı | Kovaryans payı | Korelasyon(ons, kur) |
|---|---|---|---|---|---|---|---|---|
| 2017–2021 | 1g | 1,79% | 0,82% | 1,66% | 21% | 86% | −8% | −0,10 |
| 2017–2021 | 21g | 6,98% | 3,19% | 7,38% | 21% | 112% | −32% | −0,34 |
| 2022–2023 | 1g | 1,33% | 0,84% | 0,97% | 40% | 52% | +3% | +0,03 |
| 2024 | 1g | 0,88% | 0,84% | 0,32% | 92% | 13% | −6% | −0,08 |
| 2025 | 1g | 1,22% | 1,16% | 0,34% | 91% | 8% | −1% | −0,02 |
| 2026 | 1g | 1,83% | 1,84% | 0,09% | **101%** | **0,3%** | −1% | −0,13 |
| 2026 | 5g | 4,53% | 4,53% | 0,19% | 100% | 0,2% | 0% | −0,01 |
| 2024–2026 | 1g | 1,34% | 1,32% | 0,28% | 97% | 4% | −2% | −0,05 |
| 2024–2026 | 21g | 5,65% | 5,58% | 1,09% | 98% | 4% | +2% | +0,05 |

Günlük spot korelasyonu (ons, USDTRY): 2017'de −0,34, 2018–2026 arasında −0,14 ile +0,01. Kur stresinde ons ile kur arasında sistematik bir **birlikte hareket yok**.

### 4.2 Yıllık getiri: spot pariteye göre (yıl sonu → yıl sonu, log %)

Veri: ons Dukascopy 15:00 UTC, kur Yahoo.

| Yıl | Ons | USDTRY | Gram (sentetik) | Yıl sonu gram TL |
|---|---|---|---|---|
| 2018 | −1,6 | +33,4 | +31,8 | 217,1 |
| 2019 | +17,1 | +12,0 | +29,1 | 290,4 |
| 2020 | +22,0 | +21,5 | +43,5 | 448,7 |
| 2021 | −3,8 | +58,9 | +55,1 | 778,6 |
| 2022 | −0,2 | +34,2 | +34,0 | 1.093,7 |
| 2023 | +12,6 | +45,6 | +58,2 | 1.957,8 |
| 2024 | +23,7 | +17,9 | +41,6 (basit +%51,6) | 2.966,7 |
| 2025 | +50,8 | +19,6 | +70,4 (basit +%102) | 6.000,9 |
| 2026 (06.11'e kadar) | −7,1 | +15,5 | +8,4 (basit +%8,8) | 6.528,1 |

**Okuma:**
- 2018–2023'te gram altın getirisinin çoğu kurdan geldi.
- 2024–2025'te ons sürükledi, kur ≈ %18–20 ile sabit katkı verdi.
- 2026'da ons zirveden (29.01.2026, ≈ 5.496 $) düştü. Gram altın yıl başından beri yalnız ≈ %9 kazandırdı. TL mevduat faizi aynı dönemde ≈ %30+.

### 4.3 VİOP vadeli getirisi: carry dahil (aktif kontrat zinciri, yıllık log %)

| Yıl | F_XAUUSD | F_USDTRY | F_XAUTRYM |
|---|---|---|---|
| 2023 | +4,2 | +15,1 | +13,8 |
| 2024 | +16,3 | **−22,2** | −5,8 |
| 2025 | +44,9 | **−16,7** | +29,2 |
| 2026 YTD | −15,8 | **−12,1** | −26,0 |

**VİOP gram altın long'u 2024'te spot gram %41,6 yükselirken −%5,8 kaybettirdi.** Neden: vadeli fiyat TL faizini peşin içerir. Long, bu carry'yi her gün öder. TL'nin reel değerlenme politikası sürdükçe VİOP gram long = ons long + **kaybettiren USDTRY long**. Ons yönünde pozisyon almak isteyen Türk yatırımcı için F_XAUUSD daha "temiz" bir araç: TL carry'si yok, kâr/zarar TCMB kuruyla TL'ye çevrilir.

---

## 5. VİOP gram altın ile sentetik arasındaki fark: arbitraj, baz, faiz farkı

- **Aynı vade ayında sentetik fark** (`tr_prem_matched` = log F_XAUTRYM − log(F_XAUUSD × F_USDTRY / 31,1035), 15:10 UTC):

| Yıl | Ortalama | Std | %5 | %95 | Maks |
|---|---|---|---|---|---|
| 2018 | +0,208% | 0,513% | −0,129% | +0,643% | +3,840% (31.08.2018) |
| 2022 | +0,322% | 0,418% | −0,002% | +0,714% | +5,854% (27.05.2022; büyük olasılıkla vade sonu/veri artefaktı) |
| 2024 | −0,060% | 0,170% | −0,339% | +0,245% | +0,521% |
| 2025 | +0,018% | 0,084% | −0,127% | +0,135% | +0,374% |
| 2026 | +0,020% | 0,081% | −0,107% | +0,162% | +0,268% |

  2025–2026'da ±%0,15'lik bant, üç bacaklı bir arbitrajın komisyon, BSMV ve spread maliyetine yakın. Piyasa yapıcılar bandı kapatıyor, bireysel yatırımcıya edge yok.

- **Takvim yayılımından ima edilen yıllık carry** (aktif → sonraki vade, yıllık medyan):

| Yıl | F_XAUUSD | F_USDTRY | F_XAUTRYM | 3 ay UST (ortalama) |
|---|---|---|---|---|
| 2023 | 6,48% | 36,29% | 45,95% | — |
| 2024 | 5,82% | 47,31% | 57,49% | — |
| 2025 | 4,85% | 38,69% | 44,76% | 4,20% |
| 2026 | 7,18% | 34,36% | 43,40% | 3,84% |

  Tutarlılık: (1 + USDTRY carry) × (1 + XAUUSD carry) − 1 ≈ gram carry. 2026'da 1,3436 × 1,0718 − 1 = %44,0, gözlenen %43,4.

- **Kısa vade "carry sürüklenmesi"** (Nisan 2025–Ekim 2026; VİOP aktif kontrat getirisi − spot sentetik getirisi):
  - Gram: 1 seans −%0,166 (std %0,325), 3 seans −%0,495, 5 seans −%0,826.
  - Ons: 1 seans −%0,034, 5 seans −%0,168.
  - **Yani 5 günlük gram altın long'unun beklenen getirisi, spot gram beklentisinden ≈ 0,8 puan aşağıda.**
- **Cash-and-carry.** Fiziki altın tutan biri (ör. kuyumcu ya da yastık altı altını olan hane) VİOP gram altın satarak altının TL değerini ≈ %40 yıllık oranla "faizlendirebilir". Bu, kuyumcuların klasik hedge'i. Riskleri:
  - Kapalıçarşı priminin değişmesi (baz riski).
  - Teminat ve stopaj.
  - Fiziki altının nakde çevrilme makası.

---

## 6. Türkiye talebi, mevsimsellik, dünya fiyatına etki, TCMB rezervleri

**Talep (WGC):**
- Q3 2026 bar-sikke 12,6 t: yıllık −%12, çeyreklik −%39. YTD 59 t (+%19).
- Q3 2026 mücevher 6,9 t: yıllık −%4, çeyreklik −%15.
- Çeyreklik seri, bar-sikke: Q3'25 14,3; Q4'25 21,3; Q1'26 26,1; Q2'26 20,7; Q3'26 12,6.
- Çeyreklik seri, mücevher: 7,1; 7,7; 6,9; 8,1; 6,9.
- WGC'nin açıklaması: Ocak–Mayıs'ta yüksekten alanlar bekledi, Ağustos rallisi kâr satışına dönüştü. Mücevherde düğün kaynaklı mevsimsel talep, kalıcı yüksek enflasyon ve siyasi kaygıları telafi etmedi.

**Uzun dönem (WGC, Temmuz 2024):**
- 2023 bar-sikke rekor 150 t. 5 yıllık ortalama 94 t, 10 yıllık 66 t.
- Mücevher 2023'te 42 t (dünyada 4. pazar). 5 yıllık ortalama 35 t.
- Yurt içi altın stoku tahmini ≈ **4.500 t**. Resmî rezerv (TCMB + Hazine mülkiyeti) Mayıs 2024 sonunda 584 t, toplam rezervlerin %34'ü.

**Mevsimsellik.** Çeyreklik verideki dalgalanma (mücevher 6,9–8,1 t) fiyat ve kur etkilerinin yanında küçük kalıyor. Q2 (bahar düğünleri, bayramlar) mücevherde hafif yüksek. Bar-sikke talebi ise mevsimden çok **fiyat momentumu ve TL kaygısıyla** sürüyor: Q1'26'nın 26,1 t'u Ocak rallisiyle geldi.

Bayram tarihlerine bağlı prim/fiyat mevsimselliği için güvenilir ölçüm **bulunamadı**. Bizim veride Kapalıçarşı serisi olmadığından test edilemedi.

**Dünya fiyatına etki:**
- Hane talebi küçük. Q3 2026'da Türkiye tüketici talebi 19,5 t, küresel toplam talep 1.369 t: **≈ %1,4**. Küresel bar-sikkede payı 12,6 / 267,8 = **%4,7**.
- Yerel prim/iskonto ithalat kanalıyla dünyaya bağlanıyor. İskonto dönemlerinde ithalat çöküyor (Ağustos–Eylül 2026'da 1–2 t), dünya fiyatına baskı ihmal edilebilir.
- **TCMB ise farklı.**
  - WGC verisine dayanan haberlere göre Mart 2026'da 60 t (bir kısmı swap) ile küresel en büyük satıcı oldu. Rezervler Mart sonunda ≈ 693 t'a indi, Nisan ortasında ≈ 730 t'a çıktı (ikincil, orta-düşük güven).
  - Eylül 2026'da +3,58 t ile 794,94 t'a ulaştı. Haziran sonundan beri +65,1 t (Kettner, BIST/TCMB verisine atıfla; orta-düşük güven).
  - Bu tonaj tanımı, bankaların ZK/swap altınını da içeren uluslararası rezerv tanımı olabilir. WGC'nin "mülkiyet" tanımı (584 t, 2024) ile karıştırılmamalı.
  - Mart 2026'da ons ≈ %17 düştü, TCMB satışları bu sırada manşetteydi (BullionVault 24.03.2026). Ama Rusya satışları ve faiz/petrol şoku da aynı anda vardı. **Nedensellik kurulamaz.**

---

## 7. Türk yatırımcılar altından nasıl para kazanıyor (ve kaybediyor)

1. **"Kur + ons" çift getiri.** Spot gram 2018–2025'te her yıl pozitif oldu (+%29 ile +%70 log). Gerçek getiriyi belirleyen, **TL faizine göre fark**:
   - 2024: gram +%51,6 (basit), politika faizi %45–50 → aşağı yukarı başa baş.
   - 2025: gram +%102, faiz %38–46 → altın açık ara kazandı.
   - 2026: gram +%8,8, faiz %36–40 → TL kazandı.
   - Strateji yorumu: TCMB kuru tutarken altının TL'deki üstünlüğü yalnızca **ons rallisinden** gelir.
2. **Prim ticareti.** Ons düşüp yerel fiyat iskontoya geçtiğinde fiziki al (Q3 2026; WGC "6.400–6.500 TL/g'de dip alımı"). Panik/rallide yüksek primle sat (Ekim 2025, Ocak 2026).
   - Kazanç ≈ prim değişimi − makas. Örnek: iskonto %−1'den prim %+5'e geçiş, %3 makasla ≈ %3 net.
   - Riskleri: makas, likidite, sahte ürün, nakliye.
3. **Cash-and-carry / kuyumcu hedge'i.** Fiziki altın + VİOP gram altın short ≈ TL faizi (2026'da ≈ %40 brüt). Baz riski Kapalıçarşı primi.
4. **VİOP–sentetik arbitrajı.** 2025–2026'da fark ±%0,15. Fırsat piyasa yapıcılara ait, bireysele değil.
5. **Yön ticareti (kullanıcının yaptığı).** F_XAUUSD: ons yönü, TL carry'si yok, akşam seansı var. F_XAUTRYM: ons + kur + TL carry. Kısa ufukta kur katkısı ≈ +0,07%/gün, TL carry ≈ −0,17%/seans → net ≈ −0,1%/seans ters rüzgâr.
6. **Maliyet ve vergi farkları:**

| Araç | Vergi / gider | İşlem maliyeti | Kaynak (güven) |
|---|---|---|---|
| VİOP F_XAUUSD / F_XAUTRYM | Yerleşik gerçek kişiye kazançtan %10 stopaj. Üç aylık netleştirme, zarar devri yıl içinde | Borsa yüzbinde 3 + Takasbank yüzbinde 1 + aracı komisyonu (onbinde 0,9–binde 2) + %5 BSMV | r1 (BIST, GİB) (yüksek) |
| Banka altın hesabı (kaydi) | 17.03.2025'ten beri fiziki teslimatsız alım/satım "kambiyo işlemi" (9595 s. CBK, RG 15.03.2025/32842). Alımda **binde 2 BSMV** | Banka makası (bu çalışmada ölçülmedi) | alomaliye (RG metni) (yüksek); oran uygulaması: basın (orta) |
| | Danıştay 7. D. E:2026/1054, K:2026/1847 (RG 27.06.2026, 33293): kanun yararına bozma. Uyuşmazlığın vergi mahkemesinin görev alanında olduğuna hükmetti. **Vergiyi kaldırmadı** | | alomaliye/musavirlerkulubu (orta) |
| Kapalıçarşı fiziki | Gerçek kişinin fiziki altın satış kazancının vergilendirilmesi bu çalışmada **teyit edilemedi** | Makas birkaç %. Örnek, düşük güven: Mayıs 2026'da 6.749 / 6.989 TL (%3,5) | basın (düşük) |
| İthal mamul altın/mücevher | FTA'sız ve AB dışı menşede %20 ek mali yükümlülük (08.08.2023) | — | Reuters, Asharq Al-Awsat üzerinden (orta) |
| Darphane sertifikası, altın BYF (GLDTR) | Sertifika kazancı için GİB rehberinde %0 (r1). BYF vergisi teyit edilmedi | Pay piyasası komisyonu. Sertifika primi Şubat 2023'te %21'e çıkmıştı | r1; Gedik/Bloomberg (düşük) |

---

## 8. Pratik tahmin çerçevesi

### 8.1 1–5 gün (kapanıştan kapanışa, VİOP uzlaşması 15:00–15:10 UTC)

```
E[Δln F_XAUTRYM(t→t+h)] ≈ E[Δln ons(t→t+h)]                    # risk ≈ %97+
                         + kayma_20g × h                        # 2026: ≈ +0,07%/gün; 5 günde ≈ +0,35% (RMSE ≈ %0,21)
                         − carry_TL × (takvim günü/365)         # 2026: ≈ %40 yıllık → ≈ −0,17%/seans
                         + Δsentetik_fark                       # ≈ 0 (std ≈ %0,08)
E[Δln F_XAUUSD(t→t+h)] ≈ E[Δln spot ons] − ≈0,034%/seans       # USD carry + yurt içi ek
Fiziki (Kapalıçarşı):    yukarıdaki spot + Δprim               # prim ons momentumuna pro-siklik, ortalamaya döner
```

- **Ons tahmini işin %97'si.** Bunun için diğer raporlardaki küresel lead-lag sürücülerini kullanın: DXY, reel faiz, Asya seansı, ETF/CTA akışı.
- **Kur için kural:** Son 20 günün ortalama kaymasını ekleyin. VİOP USDTRY bazını kur tahmini olarak kullanmayın, çünkü sistematik olarak 0,24 puan/5 gün fazla değer kaybı öngörüyor.
- **Kuyruk filtresi:** Siyasi takvim (mahkeme kararları, seçim/olağanüstü gelişmeler), PPK günleri (10.12.2026), TCMB rezerv ve swap haberleri. USDTRY'de > %0,5'lik günlük hareket 2025-04'ten beri hiç yaşanmadı. Yaşanırsa rejim değişikliği sinyali sayın ve gram altın riskini kurla birlikte yeniden ölçün.
- **Saat uyumu:** F_XAUTRYM ve F_USDTRY akşam seansında işlem görmüyor. 15:10 UTC sonrası ABD verisine yalnızca F_XAUUSD akşam seansında (16:00–20:00 UTC) tepki verilebilir.

### 8.2 1–3 ay
- **Kur:**
  - Merkez senaryo: TCMB'nin aylık kayması, 2026'da %1,15–1,91.
  - Üst sınır göstergesi: VİOP forward (Ekim 2026'da ≈ %30,7/yıl ≈ %2,2/ay).
  - Takip edilecekler: aylık TÜFE ile kayma farkı (reel değerlenme hızı), PPK kararı, rezervler (WGC/TCMB haftalık), kur stres primi (baz sıçraması).
- **Ons:** Küresel makro modeller (diğer raporlar). Türkiye kaynaklı sinyal yok.
- **Prim** (yalnızca fiziki):
  - Ons hızla yükseliyorsa → prim açılır (+%3–8 tarihsel).
  - Ons düşüyorsa / kâr satışı varsa → iskonto (−%1 civarı).
  - Ortalama ≈ %1,5 (Reuters, 2025).
  - İthalat kotası 2026'da bağlayıcı değil. Prim tavanı ithalat açılabildiği için sınırlı. Kota bağlayıcı olursa (aylık ithalat ~12 t'a yaklaşırsa) tavan kalkar (2023–2024: 150–200 $/oz).
- **Carry:** 1–3 ayda VİOP gram long'u spot pariteye göre ≈ %3–10 geride kalır (36–40% TL faizi × 1–3 ay). Pozisyon ufku uzadıkça F_XAUUSD ile F_XAUTRYM arasındaki tercih kritikleşir.

---

## 9. Türkiye'ye özgü lead-lag testleri (kayıtlı: `out/registry/r4_turkiye_altin.csv`)

**Hedef:** VİOP XAUUSD fwd1/3/5. **Örneklem:** IS 2017-03..2021-12, OOS 2022-01..2026-11. NW lag ≥ max(h, 5). **Öngörücüler:** t-1 15:10 değerleri, USDTRY için t 15:00 UTC.

| Öngörücü | h | IC | t | IC_IS | t_IS | IC_OOS | t_OOS | Aynı işaretli yıl |
|---|---|---|---|---|---|---|---|---|
| Gram–sentetik prim seviyesi (t-1) | 1 | −0,005 | −0,23 | +0,023 | 0,75 | −0,024 | −0,87 | 5/10 |
| Prim değişimi (t-1) | 1 | −0,023 | −1,09 | −0,012 | −0,40 | −0,034 | −1,15 | 6/10 |
| USDTRY 15:00→15:00 değişimi (t) | 1 | −0,034 | −1,75 | −0,003 | −0,12 | −0,064 | **−2,12** | 7/10 |
| USDTRY 15:00→15:00 değişimi (t) | 3 | −0,031 | −1,50 | −0,029 | −0,96 | −0,022 | −0,74 | 6/10 |
| Gram altın hacim / 20g ortalama (t-1) | 5 | +0,017 | 0,59 | −0,023 | −0,62 | +0,052 | 1,27 | 6/10 |
| Gram altın açık pozisyon 5g değişimi (t-1) | 1 | +0,019 | 0,94 | +0,010 | 0,34 | +0,031 | 1,18 | 7/10 |
| VİOP XAUUSD takvim carry − 3 ay UST (t-1) | 5 | −0,019 | −0,52 | +0,041 | 0,94 | −0,078 | −1,44 | 4/10 |

18 testin tamamı CSV'de. **Hiçbiri IS ve OOS'ta tutarlı ve anlamlı değil.** Türkiye yurt içi göstergeleri (prim, hacim, açık pozisyon, kur) VİOP ons altının 1–5 günlük yönünü öngörmüyor. Bu, "Türkiye fiyat alıcısıdır" bulgusuyla tutarlı.

---

## 10. Test edilmesi gereken hipotezler

1. Kapalıçarşı fiziki primi, son 20/60 günlük ons getirisiyle pozitif ilişkili (pro-siklik). Primdeki aşırılık (ör. > %3) sonraki 1–4 haftada ons ve gram getirisi için ters sinyal. Gereken veri: zaman damgalı Kapalıçarşı veya KMKTP fiyat serisi.
2. KMKTP aylık ithalatının 12 t'a yaklaşması, primin aşırı genişleyeceğinin öncü göstergesi.
3. USDTRY 20 günlük kayma hızındaki ivmelenme (ör. aylık %1,2'den %1,6'ya geçiş, Nisan 2026) gram altın TL getirisini öngörülebilir biçimde artırıyor. Sinyal ons getirisinden bağımsız mı?
4. VİOP USDTRY baz-ima carry'sindeki ani sıçrama (stres primi; Mart 2025, Mart 2026) sonraki 1–5 günde XAUUSD'yi etkiliyor mu? TCMB rezerv satışları ve altın swapları ons için kısa vadeli baskı yaratıyor mu?
5. F_XAUUSD'nin ABD faizinin üstündeki ek carry'si (2026 ≈ +3 puan) zaman içinde yurt içi long konumlanmasını mı gösteriyor? Ek carry azaldığında sonraki getiriler düşüyor mu? İlk test: OOS t = −1,44 (h=5), anlamsız.
6. TCMB haftalık rezerv verisinde altın tonajındaki büyük düşüşler (Mart 2026'daki −120 t gibi), sonraki haftada ons getirisiyle negatif ilişkili mi? Ayrıca sonraki haftada Türkiye primini açıyor mu?

---

## 11. Bulunamayanlar / sınırlamalar

- **Akademik literatür:** Oturumun web arama bütçesi (200 arama) bu ajan çalışırken tükendi. Gram altın, Kapalıçarşı primi ve Türkiye kur–altın ilişkisi üzerine hakemli çalışma taranamadı. Bu boşluk takip araştırmasıyla kapatılmalı.
- **Kota miktarı:** Kotanın 12 t olduğu HMB açıklamasını aktaran haberlerden geliyor. Birincil BIST belgeleri miktar vermiyor ("üyeler direktörlükle iletişime geçsin"). 2024–2025'te bazı aylarda KMKTP ithalatının 12 t'u aşmasının nedeni **bulunamadı**. Kotanın 14 t'a çıkarılacağı haberinin tarihi ve teyidi **bulunamadı**.
- **Zorunlu karşılık:** 2026 itibarıyla güncel altın ZK oranları için TCMB sayfası yanıt vermedi (503). Aralık 2025 oranları ikincil kaynaktan.
- **TCMB altın tonajı:** 794,94 t (Eylül 2026) ve ≈ 693 t (Mart 2026) ikincil kaynaklardan geliyor. Rezervin tanımı (mülkiyet mi, ZK/swap dahil mi) belirsiz.
- **Kapalıçarşı zaman serisi** yok. Bu yüzden prim ölçümleri haber noktalarına ve 3 KMKTP gününe dayanıyor.
- **KMKTP seans saatleri ve standart altın fiyatının saflık birimi** teyit edilemedi. Prim hesabında ±%0,5 belirsizlik var.
- **Çeyrek/ziynet altın spesifikasyonu** (ağırlık/ayar) Darphane sayfasından alınamadı.
- **Fiziki altın satış kazancının gerçek kişi vergisi** ve GLDTR'nin vergi rejimi teyit edilmedi.
- **Ticaret Bakanlığı'nın** ithalat kotasında rolü, kuyumcu yetkilendirmesiyle sınırlı (Kuyum Ticareti Hakkında Yönetmelik). Kotayı HMB koydu.

---

## 12. Kaynaklar

**Birincil (kurum):**
- BIST duyurusu, İşlenmemiş Altın İthalat Kotası Hakkında (28.03.2024): https://www.borsaistanbul.com/files/islenmemis-altin-ithalat-kotasi-hakkinda.pdf
- BIST duyurusu, İşlenmemiş Altın İthalatı Kota Uygulaması ile İlgili Düzenleme (25.09.2023): https://borsaistanbul.com/files/duyuru_islenmemis_altin_ithalati_kota_uygulamasi_ile_ilgili_duzenleme.pdf
- HMB, Kuyum İşletmelerinin İhtiyacı İçin Bankalara Sağlanan Kota (2024/KM-4): https://ms.hmb.gov.tr/uploads/2024/03/Duyuru-Metni.pdf
- BIST KMKTP Aylık Rapor Eylül 2026: https://borsaistanbul.com/files/aylik-piyasa-raporu-eylul-2026.pdf
- BIST duyurusu 30572 (19.11.2024, Prosedür md. 7 akşam seansı listesi): https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- TCMB 1 Hafta Repo tablosu: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo
- TCMB Faiz Oranları (O/N) tablosu: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/faiz-oranlari
- WGC Gold Demand Trends Q3 2026, Investment (03.11.2026): https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q3-2026/investment
- WGC Gold Demand Trends Q3 2026, Jewellery: https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q3-2026/jewellery
- WGC, Perspectives on the Turkish gold market (Temmuz 2024): https://gold.org/download/file/18946/Perspectives%20on%20the%20Turkish%20gold%20market.pdf
- Metals Focus Precious Metals Weekly No. 94 (20.09.2024; Japonca çeviri): https://material.co.jp/metals_pdf/mt20240924134140.pdf
- 9595 sayılı CBK metni (RG 15.03.2025/32842): https://www.alomaliye.com/2025/03/15/cumhurbaskani-karari-9595-turk-parasi-koruma/
- Danıştay 7. D. kararı (RG 27.06.2026): https://www.alomaliye.com/2026/06/27/danistaydan-kaydi-altinda-bsmv-karari/

**İkincil (haber):**
- Reuters, Daily Sabah üzerinden (08.12.2025), prim %5 → %1,5: https://www.dailysabah.com/business/economy/physical-gold-gap-in-turkiye-narrows-as-demand-normalizes/amp
- hisse.net (27.01.2026), makas 250 bin TL/kg: https://www.hisse.net/haber/kapalicarsi-da-makas-acildi-fiziki-altin-spot-piyasayi-250-bin-tl-gecti-52555
- GZT (25.02.2026), 12.500 $/kg → 5.000 $/kg: https://www.gzt.com/ekonomi/25-subat-2026-altin-fiyatlari-gram-altin-fiyati-bugun-ne-kadar-iste-kapalicarsi-rakamlari-4019837
- Asharq Al-Awsat/Reuters (08.08.2023), %20 ek yükümlülük: https://english.aawsat.com/node/4476131
- Kettner Edelmetalle (21.10.2026), ithalat ve TCMB tonajı: https://www.kettner-edelmetalle.de/news/flaute-am-bosporus-turkische-silberimporte-fallen-fast-auf-null-21-10-2026
- BullionVault (24.03.2026), merkez bankası satışları: https://www.bullionvault.com/gold-news/gold-price-news/gold-central-bank-selling-032420261
- KKM sona erdi (23.08.2025): https://www.alomaliye.com/2025/08/23/kur-korumali-mevduat-kkm-hesap-acma-ve-yenileme-islemleri-sonlandirildi/amp/ ; Bloomberg HT: https://www.bloomberght.com/kur-korumali-mevduat-uygulamasi-sona-erdi-3755559
- Mart 2026 TCMB rezerv/altın: https://www.cnbce.com/altin/savasa-altin-kalkan-merkez-bankasi-ne-kadar-altin-satti-h27756 ; https://medyascope.tv/2026/03/24/tcmb-altin-rezervlerini-devreye-almayi-degerlendiriyor-bloomberg/
- Repo ihalelerine ara/yeniden başlama: https://www.forbes.com.tr/ekonomi/tcmb-repo-ihalelerine-yeniden-basladi-faiz-yuzde-37
- 19.03.2025 olağanüstü PPK: https://www.birgun.net/haber/merkez-bankasi-faizi-yeniden-yukseltti-616126 ; https://www.forbes.com.tr/para-yatirim/dalgali-haftanin-bilancosu-merkez-bankasi-rezervlerindeki-12-milyar-dolarlik-farkin-nedeni-ne
- Ekim 2026 PPK ve takvim: https://www.cnbce.com/piyasalar/merkez-bankasi-tcmb-ekim-2026-faiz-karari-ne-zaman-saat-kacta-aciklanacak-iste-merkez-bankasi-2026-faiz-kararlari-h39762
- ZK düzenlemeleri: https://www.bloomberght.com/tcmb-3762759
- Kota 12 t (HMB açıklaması haberleri): https://www.sozcu.com.tr/hazine-den-altin-ithalati-kotasi-hakkinda-aciklama-p44408

**Önceki ajan raporu:** `$S/research/r1_viop_kontrat.md` (sözleşme künyesi, uzlaşma, vergilendirme, BIST 12590).

**Kendi hesaplarım:** `$S/out/r4_turkiye_altin/*.py`, `tr_leadlag_results.csv`, `out/registry/r4_turkiye_altin.csv`.
