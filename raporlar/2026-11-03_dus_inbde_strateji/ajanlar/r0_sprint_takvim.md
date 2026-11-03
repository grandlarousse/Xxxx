# R0: Tekrar giren aday için optimum sprint süresi, yoğunluk, periyodizasyon ve 2027 takvimi

Hazırlayan: sınav hazırlığı periyodizasyonu ve tükenmişlik araştırmacısı (ajan r0_sprint_takvim). Tarih: 3 Kasım 2026.

**Etiketler**
- **[resmi]**: ÖSYM, JCNDE/ADA, NDEB ya da NBME belgesi
- **[hakemli]**: hakemli dergi makalesi
- **[satıcı]**: firma beyanı
- **[topluluk]**: forum veya sosyal medya anekdotu
- **[analiz]**: bu raporun hesabı ya da çıkarımı

**Erişim notu.** Bu turun ortak web arama kotası (200 arama) bu ajan başlamadan dolmuştu, bu yüzden arama motoru hiç kullanılamadı. Bulgular dört yoldan geldi:
1. Bilinen birincil kaynakların doğrudan indirilmesi: Ericsson 1993 tam metni, PMC'deki Parry 2019, OpenAlex/Crossref DOI kayıtlarındaki özetler.
2. Kardeş ajanların indirdiği resmi belgeler. Bunlar yerelde yeniden okundu: ÖSYM 2027 takvim PDF'i, JCNDE 2026 Aday Kılavuzu, JCNDE 2025 Teknik Raporu, Burk-Rafel 2017 tam metni, NBME posteri, Bootcamp sayfaları.
3. osym.gov.tr (503) ve travel.state.gov (403) otomatik erişime kapalıydı. Ekşi Sözlük Cloudflare engeline takıldı. X ve YouTube taranamadı.
4. Bu yüzden **TUS/DUS'a ikinci kez girenlerin "kaç ay çalıştım, kaç net arttı" anekdotları toplanamadı** (§2.3).

---

## 0. Yönetici özeti

1. **2027 DUS tarihi doğrulandı: 24 Ekim 2027 (Pazar), tek oturum.** Başvuru 7–15 Eylül, geç başvuru 23 Eylül, sonuç 18 Kasım 2027. Kaynak ÖSYM'nin "2027 Yılı Sınav Takvimi" PDF'i. PDF'in oluşturulma tarihi 28.10.2026, Excel çıktısı. ÖSYM sitesi kapalı olduğu için ayna kopyadan okundu. Bugünden sınava **50,7 hafta** var ve bu yılın tek şansı. [resmi] ([ÖSYM 2027 takvimi, ayna](https://www.isinolsa.com/wp-content/uploads/2026/10/osym-2027-yili-sinav-takvimi-7d09wi-28090734.pdf))
2. **Tam zamanlı çalışabilen biri için optimum yoğun DUS sprinti 14–18 hafta, merkezi 16 hafta.** 16 haftalık sprint 5 Temmuz 2027'de başlar. Tam zamanlı bir işte çalışan için sprint 20–24 haftadır (başlangıç 10 Mayıs – 7 Haziran). Hedef toplam süre ~500–600 saat odaklı çalışma. Sprintten önceki aylar ya INBDE'ye ya da haftada 4–8 saatlik düşük dozlu bakıma ayrılmalı. 11 ay boyunca tam yük önerilmez. [analiz; dayanakları §2–§4]
3. **ABD verisine göre "daha uzun yoğun dönem" ortalamada daha iyi puan getirmiyor.**
   - Burk-Rafel 2017 (n=274): yoğun dönem ortalama 35,3 gün ve günde 11 saat sürdü. Ne süre ne günlük saat Step 1 puanıyla ilişkiliydi.
   - Puanla ilişkili olan, çözülen **farklı soru sayısı**: her +286 yeni soru ≈ +1 puan.
   - Parry 2019 (n=170): yoğun gün sayısı puanla negatif korele (r = −0,225). Bir kohortta 6 haftadan sonra ortalama düştü. Ancak zayıf öğrenciler daha uzun çalışıyor; ters nedensellik olası. [hakemli]
4. **Günlük derin çalışma tavanı yaklaşık 4–5 saat.** Ericsson 1993'ün derlediği eğitim çalışmalarında günde 4 saatin üstü "esasen fayda yok", 2 saatin üstü azalan getiri. En iyi kemancılar günde ~3,5 saat yalnız pratik yaptı ve müzik öğretmenlerine göre üç kat fazla gündüz şekerlemesi yaptı. Uyarı: deliberate practice eğitim alanında performans varyansının yalnızca %4'ünü açıklıyor (Macnamara 2014). Bu yüzden "4 saat" bir yasa değil, sezgisel bir kural. Öneri: günde 5–6 saat odaklı ve 1 saat hafif çalışma, haftada 6 gün. [hakemli + analiz]
5. **Tükenmişlik ölçülebilir bir bedel.** 29 çalışmayı ve 109.396 öğrenciyi kapsayan meta-analizde toplam tükenmişlik ile akademik başarı arasında r = −0,24. En güçlü bileşen "yetkinlik algısının düşmesi" (r = −0,39). Planlama ilerlemeyi görünür kılmalı. Tükenme işaretleri çıktığında hafif haftaya geçilmeli. [hakemli] ([Madigan & Curran 2020](https://ray.yorksj.ac.uk/4545))
6. **Faz yapısı (16 hafta):**
   - Tanı: 1 hafta
   - Soru güdümlü ilk tur: 6 hafta
   - Aralıklı tekrar turları ve haftalık deneme: 7 hafta
   - Hafifletme (taper): 2 hafta

   Gerekçeler:
   - Aralıklı tekrarda en iyi aralık, sınava kalan sürenin yaklaşık %10–20'si. 3–4 aylık bir pencerede bu 2–3 haftaya denk gelir (Cepeda 2008).
   - Her bilgi en az 3 kez, araya geniş aralık konarak yeniden öğrenilmeli (Rawson & Dunlosky 2011).
   - Son 2 haftada hacim %40–60 azaltılır, yoğunluk korunur. Bu, sporda yarışma öncesi hafifletme meta-analizinden alınmış bir analoji (Bosquet 2007). [hakemli + analiz]
7. **Konu kitapları dolu biri için baştan konu okumaya gerek yok.** Hollanda'daki kesitsel bir çalışmada, kullanılmayan temel bilim bilgisinin son kullanımdan sonraki 1,5–2 yıl içinde çok az kaybolduğu bulundu (Custers & ten Cate 2011). 7–8 aylık birikim Temmuz 2027'ye kadar büyük ölçüde duruyor. Kasım–Haziran arasında haftada 4–8 saatlik bakım yeterli. [hakemli + analiz]
8. **INBDE takvimi esnek, bu esneklik bilinçli kullanılmalı.**
   - Sınav yıl boyunca yapılıyor. Başvuru onaylanınca 6 aylık bir uygunluk penceresi açılıyor.
   - Bu pencere bir kez, 150 $ karşılığında 45 gün uzatılabiliyor.
   - Randevu en az 30 iş günü önceden değiştirilirse ücret 50 $. 5–29 iş günü kala 70 $, 1–4 iş günü kala 150 $.
   - Kalınırsa tekrar giriş için en az 60 gün beklenir. Sonuç 3–4 haftada çıkar.
   - Pratik taktik: **Aralık başında başvur, Mart ortasına randevu al, en geç 1 Şubat 2027'de "tut ya da Mayıs'a kaydır" kararı ver.** [resmi + analiz] ([JCNDE 2026 Aday Kılavuzu](https://jcnde.ada.org/-/media/project/ada-organization/ada/jcnde/files/2026_inbde_candidate_guide.pdf))
9. **Periyodizasyon açısından en temiz kombinasyon "Mart INBDE + 16 haftalık DUS sprinti".**
   - İki zirve arasında yaklaşık 32 hafta var.
   - INBDE'de kalınırsa tekrar giriş Mayıs–Haziran'da yapılabilir ve DUS sprintinden önce sığar.
   - Mayıs INBDE'de kalınırsa tekrar giriş en erken Temmuz başına düşer, yani tam sprintin ortasına.
   - Mart'ın şartları: çalışmıyor olmak, İngilizce ≥B2 ve vizenin Şubat'a kadar hazır olması. Aksi halde Mayıs, ya da INBDE'yi DUS'tan sonraya bırakmak. [analiz]
10. **Acil tarih: 2026/2 DUS'un 120 sorusu 11 Kasım 2026 23.59'a kadar AİS'te görülebiliyor.** Resmi sonuç 26 Kasım 2026'da açıklanacak. Sorular madde madde denetlenmeli: konu, hata tipi, kitapta var mıydı. Sprintin tanı fazı bu veriye dayanır. [resmi/ikincil, kardeş ajan r0_dus_sinav] ([Milli Gazete](https://www.milligazete.com.tr/osym-dus-ve-sts-dis-hekimligi-cevap-anahtari-sorular-nerede-kitapcik-nasil-acilir-erisim-ne-zaman-bitecek))
11. **Kullanıcının kapatması gereken açık, "ortalama bir tekrar girişin" getirdiğinden büyük.**
   - NBME verisinde Step 2 CK'yi tekrar alanlar ortalama 20 puan (0,79 SS) kazanıyor. Bunun ~5 puanı ortalamaya gerileme.
   - Kullanıcının 61 netten en düşük genel tabana (K≈62,4) çıkması için yaklaşık +1,0–1,7 SS gerekiyor (kardeş modeline göre).
   - Yani yalnızca daha fazla zaman değil, yöntem değişikliği de gerekli. [resmi + analiz]

---

## 1. Takvim gerçekleri

### 1.1 ÖSYM 2027 [resmi]

Kaynak: ÖSYM 2027 takvim PDF'inin ayna kopyası. PDF'te "Oluşturma 28.10.2026, Microsoft Excel 2019" yazıyor. Yerel kopyanın yolu: `/tmp/claude-0/-home-user-Xxxx/eb62f538-fa87-5a4c-809f-e9032ba91072/scratchpad/web/osym/takvim2027.pdf`.

| Sınav | Başvuru | Geç başvuru | Sınav | Sonuç | Bu plan için anlamı |
|---|---|---|---|---|---|
| **2027-DUS** (takvimde tek satır) | 07–15.09.2027 | 23.09.2027 | **24.10.2027** | 18.11.2027 | Başvuru sprintin 10.–11. haftasına düşüyor. Hatırlatıcı kur |
| 2027-YDUS | 17–25.03.2027 | 01.04.2027 | 02.05.2027 | 04.06.2027 | Tıpta yan dal sınavı. Diş hekimini ilgilendirmez |
| 2027-YDS/1 | 03–11.02.2027 | 18.02.2027 | 28.03.2027 | 21.04.2027 | DUS yerleştirmesinde YDS ≥50 şartı var (kardeş ajan r0_dus_sinav). Gerekirse sprintten önce bitir |
| e-YDS İngilizce | — | — | 16.01, 06.02, 24.04, 26.06, 21.08, 25.09, 18.12.2027 | Aynı gün | 21.08 ve 25.09 sprintin içine düşüyor, bu tarihlerden kaçın |
| 2027-YDS/2 | 05–13.10.2027 | 20.10.2027 | 21.11.2027 | 10.12.2027 | DUS'tan sonra. Sonuç tercih dönemine yetişir mi, doğrulanmadı |
| (Karşılaştırma) TUS | — | — | 27.03 ve 22.08.2027 | — | TUS 2027'de hâlâ iki oturum. Yılda tek oturum yalnızca DUS'ta |

### 1.2 INBDE mekaniği [resmi]

Kaynak: [JCNDE 2026 Aday Kılavuzu](https://jcnde.ada.org/-/media/project/ada-organization/ada/jcnde/files/2026_inbde_candidate_guide.pdf); yerel metinden yeniden okundu.

| Kural | Değer | Takvim etkisi [analiz] |
|---|---|---|
| Uygunluk penceresi | Başvuru işlendikten sonra **6 ay** | Aralık 2026 başı başvuru → pencere ~Haziran 2027 başına kadar. Mart da Mayıs da kapsanır |
| Uzatma | **45 gün, 150 $, bir kez** | Pencereyi Temmuz ortasına kadar uzatabilir, ama bu DUS sprintine çarpar |
| Randevu değiştirme | ≥30 iş günü önce **50 $**, 5–29 iş günü 70 $, 1–4 iş günü 150 $ | 15 Mart randevusu için 50 $'lık son gün **1 Şubat 2027**, 22 Mart için 8 Şubat |
| Tekrar giriş | Başarısız iki deneme arası **≥60 gün**, 12 ayda en çok 4 deneme | 15 Mart'ta kalan en erken 14 Mayıs'ta, 3 Mayıs'ta kalan en erken 2 Temmuz'da girer |
| Sonuç | Hedef 4 hafta, çoğu durumda 3 hafta | Mart sınavının sonucu Nisan başı–ortasında gelir |
| Merkez | Yalnızca ABD ve Kanada (Quebec hariç); kardeş ajan r0_inbde_sinav | Vize kritik yol. Ankara ve İstanbul B1/B2 bekleme süresi **doğrulanamadı** (travel.state.gov 403) |
| Geçme oranı (2025) | CODA dışı mezun ilk girişte **%34,9 kalıyor**, tekrar girişte %50,5 ([Teknik Rapor 2025, Tablo 16.1](https://jcnde.ada.org/-/media/project/ada-organization/ada/jcnde/files/inbde_technical_report.pdf)) | Kalma olasılığı plana dahil edilmeli. Tekrar girişin hangi takvim penceresine düştüğü belirleyici |

### 1.3 Kanada ile çakışmalar [resmi, kardeş ajan r0_inbde_sinav]

Kaynak: [NDEB tarihleri](https://ndeb-bned.ca/examination-dates-and-locations/).
- AFK **13 Ağustos 2027**. Bu, 16 haftalık DUS sprintinin 6. haftasına denk geliyor.
- ACJ 2 Kasım 2027, DUS'tan 9 gün sonra.
- Şubat 2027 AFK'ya pratikte yetişilemiyor.

[analiz] Kanada yolu seçilirse AFK'yı Ağustos 2027'de almak DUS sprintini ikiye böler. Önerilen sıra: DUS (Ekim 2027), ardından 2028'deki ilk AFK. 2028 tarihi doğrulanmadı.

---

## 2. (a) Hazırlık süresi kanıtı

### 2.1 Yoğun dönem süresi ile puan

| Çalışma | Örneklem | Bulgu | Etiket ve sınır |
|---|---|---|---|
| **Burk-Rafel, Santen, Purkiss 2017**, *Acad Med* 92(11S):S67–74 ([doi](https://doi.org/10.1097/ACM.0000000000001916)) | 274 öğrenci (%82,5 yanıt), 2014–15 | Yoğun dönem ortalaması **35,3 gün** (SS 6,2, aralık 11–98), günde **11,0 saat** (SS 2,1). Süreye göre ≤31 gün, 32–36 gün ve ≥37 gün grupları arasında fark yok (NS). Günlük saat de anlamlı değil. Anlamlı olanlar: erken başlama (+4,2 puan), kitabı bir kez daha baştan sona okumak (+2,3), **her +286 yeni soru (+1,0)**. Aynı soruyu tekrar çözmek yeni soruya göre daha zayıf | [hakemli] Gözlemsel, öz bildirim, tek kurum. Yazarlar: "daha fazla çalışmaktan çok daha akıllı çalışma" |
| **Parry, Pachunka, Beck Dallaghan 2019**, *Med Sci Educ* 29:667–672 ([PMC8368955](https://pmc.ncbi.nlm.nih.gov/articles/PMC8368955/)) | 170 öğrenci, 2016–17 | Yoğun gün sayısı ile puan **r = −0,225** (p = 0,003). 2016 kohortunda ilişki yok (r = −0,04), 2017'de var (r = −0,304), ortalama "6 haftadan sonra düşüyor". Akademik başarı ile puan r = 0,719. Akademik başarı ile gün sayısı r = −0,292. Deneme sınavı sayısı anlamlı değil | [hakemli] **Ters nedensellik** güçlü: zayıf öğrenci daha uzun çalışıyor. "Uzun çalışma zarar verir" denemez, yalnızca "ortalamada getirmez" denebilir |
| **Deng, Gluckstein, Larsen 2015**, *Perspect Med Educ* ([doi](https://doi.org/10.1007/s40037-015-0220-x)) | 72 öğrenci | Her +445 soru ≈ +1 puan. Her +1.700 yeni Anki kartı ≈ +1 puan. **Sınav kaygısı negatif yordayıcı** (B = −1,99) | [hakemli] Küçük örneklem, gözlemsel |
| **NBME, Ling ve ark. 2016** ([poster](https://www.nbme.org/PDF/StaffPresentations/Ling%20Invest%20score%20gains%20for%20repeat%20AAMC%202016.pdf)) | 2.767 kişi, Step 2 CK tekrar girişi | Ortalama kazanç **20 puan (179 → 199; 0,79 SS)**. Bunun ~5 puanı ortalamaya gerileme | [resmi/kurum araştırması] İki giriş arası sürenin etkisi yok |

**Yorum [analiz]:**
- (i) Ortalamada süre değil, **içerik** belirleyici: farklı soru sayısı, aktif hatırlama, erken başlama.
- (ii) ABD verisi 5–7 haftalık bir yoğun dönemi anlatıyor. O sınavlar entegre müfredatın ve aylar süren "erken çalışma"nın üzerine kuruluyor. Burk-Rafel'de öğrencilerin %77'si yoğun dönemden önce başlamıştı.
- (iii) DUS bir **sıralama sınavı**. Kullanıcının +20–30 net kapatması gerekiyor (kardeş ajan r0_dus_sinav). Bu yüzden ABD'nin 5–7 haftası alt sınır olarak alınamaz. Ama ABD verisi "8–11 ay tam yük daha iyidir" tezini de **desteklemiyor**.

### 2.2 Bilgi ne kadar hızlı kaybolur? Bakım fazının gerekçesi

- **Custers & ten Cate 2011** (*Med Educ*, [doi](https://doi.org/10.1111/j.1365-2923.2010.03889.x)). Tekrarlanmayan temel bilim bilgisi son kullanımdan sonraki **1,5–2 yıl içinde çok az kayboluyor**. Sonrasında logaritmik bir unutma eğrisi başlıyor. [hakemli, kesitsel]
  - [analiz] Kasım 2026'da "dolu" olan bilgi Temmuz 2027'de büyük ölçüde duruyor.
  - DUS'taki ayrıntı soruları (bkz. r0_ortusme: KBT'nin ~%26'sı "detay") kavramsal bilgiden daha hızlı unutulabilir. Bu yüzden düşük dozlu **aktif** bakım (soru ve kart) gerekli, ama baştan konu okumaya gerek yok.
- **Cepeda ve ark. 2008** (*Psychol Sci*, [doi](https://doi.org/10.1111/j.1467-9280.2008.02209.x)). 1.350'den fazla katılımcı. En iyi tekrar aralığı, sınav gecikmesi 1 hafta olduğunda bunun **%20–40'ı**, 1 yıl olduğunda **%5–10'u**. [hakemli]
  - [analiz] Kasım–Haziran bakım fazında sınava 5–11 ay var, bu yüzden her dersin 2–4 haftada bir kısa tekrarı yeterli.
  - Sprintte sınava 2–4 ay kalıyor. Aralık ~1,5–3 haftaya iner, yani ders başına 3–4 dönüş.

### 2.3 TUS/DUS'a ikinci kez girenlerin deneyimleri

**Doğrulanamadı.** Ekşi Sözlük sayfaları Cloudflare engeline takıldı. Arama kotası dolduğu için X, YouTube ve forumlarda arama yapılamadı. İndirilebilen tek forum dizisinde (DonanımHaber) ölçülebilir bir "ay ya da net" verisi yoktu. DUS'a tekrar girenlerin net artışını ölçen hakemli ya da resmi bir veri de bulunamadı (kardeş ajan r0_ogrenme_bilimi aynı sonuca vardı).

Pazar verisi bir fikir veriyor [satıcı]: sağlayıcılar 3, 6, 9 ve 12 aylık paketler, ayrıca 11 aylık koçluk satıyor. Kamplar sınavdan ~2 ay önce açılıyor (kardeş ajan r0_dershane_pazar). Uzun paket satmak sağlayıcının **ticari çıkarına**. Bu sürelerin net getirisini gösteren bir veri yok.

---

## 3. (b) Günlük ve haftalık yoğunluk

### 3.1 Kanıt

| Konu | Bulgu | Kaynak ve etiket |
|---|---|---|
| Günlük tavan | Günde 1–8 saat arası pratik süreleri karşılaştıran eğitim çalışmalarında "**4 saati aşan sürelerin esasen faydası yok, 2 saati aşanların faydası azalıyor**". Romancılar sabah ~4 saat yazıp günün kalanında dinleniyor. En iyi iki keman grubu her gün, hafta sonu dahil **~3,5 saat yalnız pratik** yaptı (haftada 24,3 sa) ve pratiği öğleden önceye yığdı. Tüm kemancılar haftada ortalama 58,2 saat uyudu. En iyi iki grup gündüz şekerlemesine haftada 2,8 saat ayırdı, müzik öğretmenleri ise 0,9 saat. Toparlanamayan yük "staleness, overtraining, burnout" getiriyor | [Ericsson, Krampe, Tesch-Römer 1993, *Psychol Rev* 100:363–406](https://graphics8.nytimes.com/images/blogs/freakonomics/pdf/DeliberatePractice(PsychologicalReview).pdf) [hakemli; dayandığı eğitim çalışmaları 1954–1968 tarihli] |
| Tavanın ağırlığı | Deliberate practice performans varyansını oyunlarda %26, müzikte %21, sporda %18, **eğitimde %4** açıklıyor | [Macnamara, Hambrick, Oswald 2014](https://doi.org/10.1177/0956797614535810) [hakemli meta-analiz] |
| Saat ile not | Başlığı: "Çalışma süresi üniversite öğrencilerinin not ortalamasını neden yordamıyor" (çalışmanın niteliği ve ortamı öne çıkıyor) | [Plant, Ericsson ve ark. 2005](https://doi.org/10.1016/j.cedpsych.2004.06.001) [hakemli; özet bu turda okunamadı, yalnızca başlık ve künye doğrulandı] |
| Tükenmişlik | Toplam r = −0,24, yetkinlik algısı düşüşü r = −0,39 (29 çalışma, N = 109.396) | [Madigan & Curran 2020](https://ray.yorksj.ac.uk/4545) [hakemli] |
| Uyku | Öğrenmeden önce uykusuzluk belleği g ≈ 0,62 düşürüyor. Notla ilişkili olan sınavdan önceki tek gece değil, son hafta ve aylardaki uyku | Kardeş ajan r0_ogrenme_bilimi (Newbury 2021, Okano 2019) [hakemli] |
| Hafifletme (taper) | 27 sporcu çalışmasında en iyi strateji **2 haftalık** hafifletme: hacim üstel olarak **%41–60 azaltılıyor**, yoğunluk ve sıklık korunuyor (ES = 0,72) | [Bosquet ve ark. 2007](https://doi.org/10.1249/mss.0b013e31806010e0) [hakemli; **bilişsel sınava analoji**, doğrudan kanıt değil] |

### 3.2 Öneri: tam zamanlı sprint günü [analiz]

Tasarım ilkeleri: DUS saati 10.15–12.45 (150 dk, 120 soru, soru başına 75 sn). Derin çalışma tavanı ~4–5 saat. Uyku 7–9 saat.

| Saat | Blok | İçerik | Süre |
|---|---|---|---|
| 08.00–08.40 | Kart | Dünkü hata kartları ve aralıklı tekrar (Anki ya da kâğıt) | 40 dk (hafif) |
| **10.15–12.45** | Derin blok 1 | Sınav saatinde, zamanlı 60–100 soruluk karma ya da branş bloğu | 2–2,5 sa |
| 14.00–16.00 | Derin blok 2 | Blok 1'in analizi. Yanlış ve şüpheli sorular için dolu kitapta **yalnızca ilgili sayfa**. Hata defterine kayıt | 2 sa |
| 16.30–17.45 | Derin blok 3 | 30–50 soruluk zayıf branş bloğu ve hızlı analizi | 1–1,25 sa |
| 21.00–21.20 | Kart | Günün hatalarından üretilen kartlar | 20 dk |
| 23.00–07.00 | Uyku | Sabit saat. Son 4 haftada kalkış sınav gününe göre | 8 sa |

- **Haftalık:** 6 gün çalışma, 1 tam gün izin. Ericsson'un kemancıları her gün çalışıyordu, ama günlük yükleri bizimkinin yarısı kadardı. Bu yüzden 5–6 saatlik yükte haftalık izin gerekli [analiz].
- **Hafif hafta kuralı:** Şu üç işaretten ikisi görülürse 1 hafif hafta yapılır: (a) haftada 3 gece 7 saatin altında uyku, (b) deneme neti 3 hafta üst üste artmıyor, (c) haftada 2 gün blok bitirilemiyor. Hafif haftada hacim %40–50 azalır, deneme yapılmaz, öncelik uykudur. Bu kural Bosquet 2007 analojisinden ve tükenmişlik verisinden türetildi [analiz].
- **Soru hacmi:**
  - Faz 2'de günde ~100–120, Faz 3'te ~120–150, Faz 4'te ~60–80 soru.
  - Sprint toplamı ~7.000–10.000 soru maruziyeti. Bunun en az ~%70'i **daha önce görülmemiş** soru olmalı (Burk-Rafel'in yeni/tekrar soru ayrımı).
  - Havuz: ÖSYM'nin açık DUS arşivi (2012–2021, ~1.400 soru; r0_dus_sinav), TBT için TUS temel bilim çıkmışları, kurum denemeleri ve soru bankaları.
  - Bu rakamlar hedef aralıktır, kanıt değildir [analiz].
- **Deneme sayısı:** 1 tanı denemesi ve 9.–15. haftalarda haftalık 7 deneme, yani 8 tam süreli deneme. Parry 2019'da deneme sayısı puanla ilişkili değildi. Denemenin değeri sayısında değil, ardından yapılan 2–3 saatlik analizde [hakemli + analiz].

### 3.3 Klinikte çalışırken hazırlanmak [analiz]

| Durum | Haftalık süre | Yapı |
|---|---|---|
| Tam zamanlı iş (≥40 sa) | **18–22 sa** | Hafta içi her akşam 2–2,5 sa (40–60 soru, analiz, kart). Cumartesi 6–7 sa (10.15'te deneme ya da 100 soru ve analiz). Pazar izin. **Son 3–4 hafta yıllık izinle tam zamanlı** |
| Yarı zamanlı (2–3 gün klinik) | **28–35 sa** | Klinik olmayan günler tam zamanlı sprint günü (§3.2), klinik günleri 1–1,5 sa kart ve 30 soru |
| Çalışmıyor | **33–36 sa** | §3.2, haftada 6 gün |

Gerekçe: ~500–600 saatlik hedef sabit tutulur, takvim uzatılır.
- İzinli plan: 20 hafta × 20 sa ≈ 400 sa, son 4 haftada izinle ~100–130 sa daha, toplam ≈ 500–530 sa.
- İzinsiz plan: 24 hafta × 20 sa ≈ 480 sa.

---

## 4. (c) Periyodizasyon: 16 haftalık DUS sprinti (5 Temmuz – 24 Ekim 2027)

| Faz | Hafta (tarih) | Amaç | İçerik | Haftalık yük |
|---|---|---|---|---|
| **0. Hazırlık öncesi** | Kas 2026 – Haz 2027 | Bilgiyi korumak, idari işleri bitirmek | INBDE ya da düşük dozlu DUS bakımı (§5). 11 Kasım'a kadar AİS'te madde denetimi | 4–8 sa (yalnız DUS), INBDE'de daha fazla |
| **1. Tanı** | H1 (5–11 Tem) | Hata haritası | 1 tam deneme (10.15). Kasım 2026'daki madde denetimiyle birlikte branş × hata tipi matrisi: bilgi yok / hatırlayamadı / okuma hatası / eleme. 16 ders için öncelik sırası (net getirisi, r0_dus_sinav §1) | ~25 sa |
| **2. Soru güdümlü ilk tur** | H2–H7 (12 Tem – 22 Ağu, 6 hafta) | Her derse bir kez "önce soru, sonra kitap" | 8 TBT ve 8 KBT dersi, ders başına ~2–3 gün. Önce 40–80 çıkmış ve branş sorusu, sonra kitapta yalnızca hatalı yerler. Önceki derslerden günde 20–30 karma soru (ilk aralıklı dönüş). Not: 13 Ağu AFK bu faza denk gelir (§1.3) | 33–35 sa |
| **3. Aralıklı turlar ve haftalık deneme** | H8–H14 (23 Ağu – 10 Eki, 7 hafta) | Her derse 2 dönüş daha, sınav kondisyonu | Karma bloklar (dersler karışık). 9. haftadan itibaren her pazar 10.15'te tam deneme ve 2–3 sa analiz. Hata defterinden kart. **7–15 Eylül DUS başvurusu** | 33–36 sa |
| **4. Hafifletme** | H15–H16 (11–24 Eki, 2 hafta) | Zirve | Hacim %40–60 azalır, yoğunluk korunur. 17 Ekim'de son tam deneme. Yeni konu açılmaz, yalnızca hata kartları ve "yüksek getirili" listeler. Uyku ve kalkış saati sınav gününe göre. Son 2 gün çok hafif | 15–22 sa |

**Toplam:** ~6×34 + 7×35 + 25 + 2×18 ≈ **510 saat**, ~8.000–10.000 soru, 8 tam deneme.

**Faz sürelerine nasıl varıldı [analiz]:**
- **İlk tur 6 hafta.** 16 ders × 2–3 gün ≈ 32–48 gün, haftada 6 gün çalışmayla 5–8 hafta eder. Kitaplar dolu olduğu için alt uca yakın bir süre seçildi.
- **Tekrar turları 7 hafta.** Rawson & Dunlosky 2011'in önerisi: ilk öğrenmede 3 doğru hatırlama, ardından geniş aralıklarla **3 kez yeniden öğrenme**. İlk tur birinci karşılaşmadır. Cepeda'ya göre ~2,5–3 haftalık aralıklarla iki tam tur ≈ 6–7 hafta eder. Üçüncü dönüş taper'daki hata kartlarıyla yapılır.
- **Taper 2 hafta.** Bosquet 2007 analojisi.
- **Tanı 1 hafta.**
- **Toplam 16 hafta.** Alt sınır 14 hafta: ilk tur 5, tekrar turları 6, taper 2, tanı 1. 14 haftanın altında, 16 derse aralıklı 3 dönüşü ve haftalık denemeyi birlikte sığdırmak zorlaşır. Üst sınır 18 hafta: ilk tur 7–8 hafta ve tekrar turları 8 hafta olur. Tam yükte 18–20 haftanın üstü için ek fayda kanıtı yok, tükenmişlik riski ise artıyor. Daha uzun süre yalnızca **düşük yoğunlukla** mantıklı; Faz 0 bunun için var.

---

## 5. (d) Takvim etkileşimi: INBDE × DUS

| Seçenek | INBDE çalışma dönemi | INBDE sınavı ve sonucu | INBDE'den DUS sprintine | Kalırsa | Periyodizasyon riski [analiz] |
|---|---|---|---|---|---|
| **A. Mart INBDE** | 17 Kas – 14 Mar (17 takvim haftası): ilk 4 hafta hafif (video, İngilizce, idari işler), ardından **~13 hafta yoğun** | ~15–22 Mart, sonuç Nisan başı–ortası | ~15 hafta ara: 2 hafta dinlenme, sonra bakım, YDS, CAAPID evrakı | Tekrar en erken ~14–28 Mayıs. **Sprint başlangıcından (5 Tem) önce sığar** | En temiz seçenek. Ama Kasım–Mart yoğun, üstüne Temmuz–Ekim yoğun: iki zirve. Aradaki 2 haftalık gerçek dinlenme şart |
| **B. Mayıs INBDE** | Ocak – Nisan (~17 hafta). Kasım–Aralık: İngilizce, idari işler, DUS denetimi | ~3–24 Mayıs, sonuç Mayıs sonu–Haziran | 3 Mayıs'ta girilirse 2–3 hafta dinlenme, ardından 18 haftalık sprint (21 Haz). 24 Mayıs'ta girilirse yalnızca ~6 hafta ara | Tekrar en erken 2–23 Temmuz, **sprintin içine düşer** | Kalma olasılığı (%34,9) gerçekleşirse ya DUS sprinti bölünür ya INBDE tekrarı Kasım'a kalır. **Kural önceden konmalı:** kalınırsa tekrar DUS'tan sonra |
| **C. Önce DUS** | Kasım–Haziran bakım (4–8 sa/hafta), DUS sprinti Temmuz–Ekim. INBDE çalışması Kasım 2027 – Şubat 2028 | Şubat–Mart 2028 | — | — | En düşük tükenme riski. Ama 2027–28 CAAPID döngüsünün büyük kısmı kaçar (kardeş ajan r0_inbde_sinav) |
| **D. Paralel, hafif** | INBDE soru bankası bakım fazında "aktif hatırlama aracı" olarak, haftada 5–8 sa | Sınav yok ya da 2028 | — | — | Düşük risk. Son 14–18 hafta mutlaka Türkçe ve DUS formatında olmalı (r0_ogrenme_bilimi: format uyumu) |

**Esneklik taktiği [resmi + analiz]:**
1. Kasım: DENTPIN al, ECE course-by-course raporunu hızlı işlemle iste, vize randevusu al.
2. **Aralık başı:** JCNDE başvurusu. Pencere ~Haziran başına kadar açık kalır.
3. Ocak başı: 15–22 Mart için randevu al. İki gün en çok 7 gün arayla ve aynı merkezde olmalı.
4. **1 Şubat 2027 (22 Mart randevusu için 8 Şubat): karar noktası.** Ölçüt örneği [analiz]: son iki haftanın karma soru doğruluğu ve satıcının tahmin aracı yeterli değilse, ya da vize yoksa, randevuyu 50 $'la Mayıs başına kaydır.
5. Mayıs başına kaydırılırsa B seçeneğindeki "kalırsan tekrar DUS'tan sonra" kuralı devreye girer.

**Gözden kaçan çakışma [analiz].** Mart'ta geçilse bile 2027–28 CAAPID sürecinin yoğun bölümü DUS sprintine denk gelebilir: TOEFL, başvurular, olası mülakatlar ve el becerisi (bench) testleri yaz ve sonbahara düşebilir. Mülakat ve bench takvimleri **doğrulanamadı**. Bu yüzden Nisan 2027'de (INBDE sonucu geldiğinde) **birincil hedef seçilmeli**. ABD birincilse DUS sprinti hafif tutulur ya da DUS bırakılır. DUS birincilse CAAPID başvuruları Haziran'dan önce bitirilip yaz–sonbahar etkinlikleri en aza indirilir.

---

## 6. (e) Somut öneri: optimum sprint aralığı ve senaryolar

**Optimum aralık: tam zamanlı 14–18 hafta (önerilen 16). Tam zamanlı işte 20–24 hafta. Hedef ~500–600 saat odaklı çalışma ve ~7.000–10.000 soru.**

Bu aralığa varırken şu adımlar izlendi [analiz]:
- (1) ABD verisinde yoğun dönemin uzunluğu ortalamada puanı artırmıyor.
- (2) DUS'ta gereken kazanç büyük ve yöntem değişikliği istiyor.
- (3) Aralıklı tekrar ilkeleri her derse ≥3 dönüş gerektiriyor. 16 ders ve ~2,5–3 haftalık aralıkla bu en az ~12–14 hafta ediyor.
- (4) 2 haftalık hafifletme ve 1 haftalık tanı ekleniyor.
- (5) Tam yükte 18–20 haftanın üstünde ek fayda kanıtı yok, tükenmişlik bedeli var.

Kardeş ajan r0_ogrenme_bilimi de 14–18 haftaya vardı. Ancak iki çıkarım aynı ilkelere dayandığı için **bağımsız teyit sayılmaz.**

### Senaryo 1: Çalışmıyor, İngilizce ≥B2, ABD hedefi ciddi (önerilen: A seçeneği)

| Tarih | İş |
|---|---|
| 3–11 Kas 2026 | AİS'te 120 sorunun madde düzeyinde denetimi. Sorular kopyalanmaz, yalnızca not tutulur |
| 3–16 Kas | **En az 10–14 gün gerçek dinlenme.** Yalnızca denetim ve idari işler |
| 17 Kas – 13 Ara | INBDE hafif başlangıç (15–20 sa/hafta): video, tıbbi İngilizce, DENTPIN, ECE, vize |
| Ara başı | JCNDE başvurusu |
| 14 Ara – 14 Mar | INBDE yoğun (~30–35 sa/hafta, ~13 hafta) ve haftada 2–3 sa Türkçe DUS bakımı |
| 1 Şub | Tut ya da kaydır kararı |
| ~15–22 Mar | INBDE |
| Mar sonu – Nis başı | 2 hafta tam dinlenme |
| Nis – Haz | Bakım (6–10 sa/hafta). Gerekirse YDS 28 Mart ya da e-YDS 24 Nisan / 26 Haziran. CAAPID evrakı. Kalınmışsa Mayıs–Haziran'da tekrar giriş |
| **5 Tem – 24 Eki** | **16 haftalık DUS sprinti** (§4). 7–15 Eylül başvuru |

### Senaryo 2: Tam zamanlı klinikte çalışıyor (C ya da D seçeneği)

| Tarih | İş |
|---|---|
| Kas 2026 – Nis 2027 | 11 Kasım'a kadar denetim, ardından bakım (4–6 sa/hafta: 2–3 kez 40–60 Türkçe soru ve kart). Gerekirse Ocak–Nisan'da e-YDS ya da YDS |
| **10 May – 26 Eyl** | Yarı zamanlı sprint, 20 sa/hafta (§3.3). Faz 1: 1 hafta, Faz 2: ~9 hafta, Faz 3: ~10 hafta (her cumartesi 10.15'te deneme) |
| **27 Eyl – 24 Eki** | Yıllık izinle tam zamanlı: son 2 deneme ve 2 haftalık hafifletme |
| İzin yoksa | 24 haftanın tamamı yarı zamanlı. Son 2 haftada hacim azaltılır |
| INBDE | 2027'de önerilmez. Kasım 2027 – Şubat 2028 |

### Senaryo 3: Yarı zamanlı çalışıyor ya da İngilizce B1–B2 (B seçeneği, kurala bağlı)

| Tarih | İş |
|---|---|
| Kas – Ara 2026 | Denetim, dinlenme, İngilizce (TOEFL/YDS'ye ortak), idari işler |
| 4 Oca – 2 May 2027 | INBDE (~25–30 sa/hafta, ~17 hafta) |
| ~3–9 Mayıs | INBDE. **Kural: kalınırsa tekrar DUS'tan sonra yapılır** |
| May – Haz ortası | 2–3 hafta dinlenme ve bakım |
| **21 Haz – 24 Eki** | 18 haftalık DUS sprinti (28–35 sa/hafta) |

**Senaryo seçimini değiştiren değişkenler [analiz]:**
- İngilizce seviyesi: <B2 ise Mart gerçekçi değil.
- Vize randevu süresi doğrulanamadı. Uzunsa Mart düşer, Kanada'daki Prometric merkezleri değerlendirilir.
- Geçerli YDS ≥50 yoksa sınav sprintten önce bitirilmeli.
- Hedef branş: Ortodonti ve Cerrahi için ≈85–105 net gerekiyor. Bu durumda DUS birincil hedef olur ve C seçeneği öne çıkar.
- 61 netin ne kadarının boş ya da yanlış olduğu. Strateji hatası ağırlıklıysa kazanç daha hızlı gelebilir; sprint alt uca (14 hafta) çekilebilir.

---

## 7. Bu boyutun soruları

- **Q5 (optimum sprint):** Tam zamanlı 14–18 hafta (16 önerilir, 5 Temmuz – 24 Ekim 2027). Tam zamanlı işte 20–24 hafta ve son 3–4 hafta izin. Öncesinde 4–8 sa/hafta bakım ya da INBDE. Kasım'dan Ekim'e 11 ay tam yük önerilmez.
- **Q9 (INBDE yoğunluğu, takvim yönü):** Mart için ~4 hafta hafif ve ~13 hafta yoğun çalışma (~30–35 sa/hafta), toplam ~450–500 saat. Bu, kardeş ajanın 350–550 saatlik aralığıyla tutarlı. Satıcı 45 günlük bir takvim öneriyor ve yabancı mezunlar için bunun 3–4 aya uzatılabileceğini söylüyor ([Bootcamp](https://bootcamp.com/blog/how-to-pass-the-inbde-as-a-foreign-trained-dentist-2022)) [satıcı]. Kullanıcı yorumlarında hazırlık "2 haftadan" "5 aya" kadar değişiyor ([yorumlar](https://bootcamp.com/inbde/student-reviews)) [satıcı/topluluk; yalnızca geçenlerin yorumu, hayatta kalan yanlılığı].
- **Q10 (Mart mı, Mayıs mı):** Takvim ve periyodizasyon açısından **Mart'ı hedefle, Mayıs'ı yedek tut.** Mart; çalışmayan, İngilizcesi ≥B2 ve vizesi Şubat'ta hazır olan biri için yetişir. Kalma durumunda tekrar giriş DUS sprintinden önce sığar. Mayıs'ta bu tampon kalmaz.

---

## 8. Sınırlar ve açık sorular

- Arama kotası dolu olduğu için TUS/DUS'a tekrar girenlerin anekdotları, Türkçe tükenmişlik çalışmaları ve INBDE hazırlık süresini ölçen hakemli bir çalışma **bulunamadı**.
- Kesin bir "optimum hafta sayısı" deneysel olarak gösterilmiş değil. Önerilen aralık ilkelerden türetildi.
- Ericsson'un dayandığı eğitim çalışmaları eski. Taper kanıtı sporcu verisi, bilişsel sınava yalnızca analoji olarak aktarıldı.
- ABD vizesi bekleme süresi, 2027–28 CAAPID mülakat ve bench takvimi, e-YDS'nin DUS tercih dönemine yetişip yetişmediği ve 2028 AFK tarihi **doğrulanmadı**.
- ÖSYM 2027 takvimi ayna kopyadan okundu. Resmi alan otomatik erişime kapalıydı.

## Kaynaklar

- ÖSYM 2027 Yılı Sınav Takvimi (ayna): https://www.isinolsa.com/wp-content/uploads/2026/10/osym-2027-yili-sinav-takvimi-7d09wi-28090734.pdf
- JCNDE 2026 INBDE Aday Kılavuzu: https://jcnde.ada.org/-/media/project/ada-organization/ada/jcnde/files/2026_inbde_candidate_guide.pdf
- JCNDE INBDE Teknik Raporu 2025: https://jcnde.ada.org/-/media/project/ada-organization/ada/jcnde/files/inbde_technical_report.pdf
- NDEB sınav tarihleri: https://ndeb-bned.ca/examination-dates-and-locations/
- Burk-Rafel ve ark. 2017: https://doi.org/10.1097/ACM.0000000000001916
- Parry ve ark. 2019: https://pmc.ncbi.nlm.nih.gov/articles/PMC8368955/
- Deng ve ark. 2015: https://doi.org/10.1007/s40037-015-0220-x
- NBME Ling ve ark. 2016: https://www.nbme.org/PDF/StaffPresentations/Ling%20Invest%20score%20gains%20for%20repeat%20AAMC%202016.pdf
- Ericsson ve ark. 1993: https://graphics8.nytimes.com/images/blogs/freakonomics/pdf/DeliberatePractice(PsychologicalReview).pdf
- Macnamara ve ark. 2014: https://doi.org/10.1177/0956797614535810
- Plant ve ark. 2005: https://doi.org/10.1016/j.cedpsych.2004.06.001
- Madigan & Curran 2020: https://ray.yorksj.ac.uk/4545 (https://doi.org/10.1007/s10648-020-09533-1)
- Cepeda ve ark. 2008: https://doi.org/10.1111/j.1467-9280.2008.02209.x
- Rawson & Dunlosky 2011: https://doi.org/10.1037/a0023956
- Custers & ten Cate 2011: https://doi.org/10.1111/j.1365-2923.2010.03889.x
- Bosquet ve ark. 2007: https://doi.org/10.1249/mss.0b013e31806010e0
- Bootcamp (satıcı): https://bootcamp.com/blog/how-to-use-bootcamps-inbde-study-schedule · https://bootcamp.com/blog/how-to-pass-the-inbde-as-a-foreign-trained-dentist-2022 · https://bootcamp.com/inbde/student-reviews
- Kardeş raporlar (aynı klasör): r0_dus_sinav.md, r0_inbde_sinav.md, r0_inbde_kaynak.md, r0_ogrenme_bilimi.md, r0_ortusme.md, r0_dershane_pazar.md
