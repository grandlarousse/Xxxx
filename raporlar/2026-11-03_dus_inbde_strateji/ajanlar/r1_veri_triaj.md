# R1 – Veri ve triaj mühendisi: "Önce ölç, sonra çalış"

Tarih: 3 Kasım 2026 · Rol: veri ve triaj mühendisi (5 stratejistten biri)
Dayanak: 00_koordinator_notlari, 00_bulgu_ozeti; tam okunanlar r0_triaj_ongoru, r0_dus_sinav, r0_dershane_pazar, r0_ai_yeninesil, r0_sprint_takvim; bölüm bölüm r0_ogrenme_bilimi, r0_ortusme, r0_inbde_*, r1_aktif_hatirlama, r1_kurumsal_reformcu.
Yeni web araması yapmadım: kararı değiştirecek boşluk kullanıcının kendi verisinde.
Hesapları (61 netin bileşimi, deneme gürültüsü, tahmin eşiği, lift) betikle yeniden yaptım: `/tmp/claude-0/-home-user-Xxxx/eb62f538-fa87-5a4c-809f-e9032ba91072/scratchpad/r1/calc.py`.
Etiketler: [resmi] [hakemli] [satıcı] [topluluk] [analiz].

---

## 0. Tez

1. Bugün masadaki her açıklama bir hipotez: "triaj kötüydü", "geri çağırma zayıftı", "arkadaşlar zaten güçlüydü". Bunları birbirinden ayırabilecek tek veri seti 11 Kasım 2026 23.59'da kapanıyor (r0_dus_sinav §5; r0_sprint_takvim §0.10).
2. Boş sayısı ne olursa olsun, 61 net 120 sorunun yaklaşık 65–73'ünü doğru yapmak demek. ~85 net için 15 boşla ~89 doğru gerekiyor. Hedefi "+20 doğru, en çok 15–20 yanlış" diye okumak gerekiyor [analiz, calc.py].
3. Dershanelerin "115/120 referans" sayısı bir kapsam (recall) ölçüsü. Triaj becerisi ancak lift ile ölçülür. DUSDATA'nın kendi rakamlarıyla RapiDUS, tam setin sayfalarının %27'siyle tam setin kapsadığı soruların %91'ini taşıyor (lift ≈3,4). Yani sayfa düzeyinde sıkıştırma işe yarıyor. Tekil "çıkacak" tahmini ise yaramıyor (isabet <%1).
4. Kendi triajın üç katmanlı olmalı:
   - Ders düzeyi: dağılım sabit, triaj gereksiz.
   - Konu düzeyi: hakemli dağılım makaleleri ve kendi kodladığın 2012–2026 arşivi.
   - Bilgi noktası düzeyi: öngörülemez; yalnızca geniş geri çağırmayla kapanır.
5. İlerleme saatle, sayfayla ya da tek deneme netiyle ölçülmemeli. Ölçü, büyük örneklemli doğruluk ve gecikmeli düzeltme oranı olmalı. Tek denemenin ±6 netlik gürültüsüne göre karar verilmez.

---

## 1. 11 Kasım'a kadar AİS denetimi: kodlama şeması

### 1.1 Kurallar ve süre bütçesi

- **Telif:** Soru metni kopyalanmaz, fotoğraflanmaz, hiçbir AI aracına yüklenmez (r0_dus_sinav §5). Notlar kendi cümlelerinle tutulur.
- **İki geçiş:**
  - 61 neti büyük olasılıkla hatırladığın cevaplarla hesapladın. Resmi aday cevapları sonuçla birlikte açılıyor: 2026/1'de 22.05.2026'da açıldı (r0_dus_sinav §6), 2026/2 için 26 Kasım bekleniyor.
  - **11 Kasım'a kadar** soruya bağlı her şeyi kodla: konu, bilgi noktası, kaynak durumu, hatırladığın cevap, güven.
  - **26 Kasım'da** D/Y/B sütununu resmi cevaplarla düzelt.
  - Soru metni ortadan kalkınca analizi "bilgi noktası" sütunu taşıyacak.
- **Bütçe:** Toplam ~7–9 saat, 3–4 oturum. Öncelik sırası:
  1. Bütün yanlış ve boşlar (~45–55 madde, madde başına 4–5 dk).
  2. Güveni ≤2 olan doğrular (şanslı doğrular).
  3. Kalan doğrularda yalnızca "kaynak durumu".
  - **3. adım atlanırsa lift hesaplanamaz.** Dershane triajı hakkında hüküm için paydanın, yani 120 maddenin tamamının kodlanması şart.
- **2026/1'e girdiysen** pencere kapandı; şema lisanslı 2026 Nisan kitapçığıyla daha zayıf biçimde uygulanır (r0_dus_sinav §5).

### 1.2 Sütunlar

| Sütun | Değerler | Amaç |
|---|---|---|
| no, test, branş | 1–120; TBT/KBT; 16 ders | Ders bazında net, arkadaşlarla karşılaştırma (r0_ortusme §6.4) |
| konu_L1 | Hakemli makale başlıkları (§3.5) | Frekans haritasına bağlantı |
| bilgi_noktası | En çok 15 kelime, kendi cümlen | Metin kaybolunca analizin dayanağı |
| soru_tipi | bilgi / vaka / öncüllü / olumsuz kök / görselli | Biçim hataları |
| cevabım, güven | A–E ya da boş; güven 3 = emin, 2 = iki şıkka indim, 1 = bir şık eledim, 0 = kör | Tahmin kalibrasyonu (§4) |
| elenen_şık | 0–4 | §4 |
| sonuç | D/Y/B (26 Kasım'da kesinleşir) | |
| kaynak | Ç = dershane kitabında çizdirilmiş · G = kitapta var ama geçiştirilmiş · Y = kitapta yok · ? = bulamadım | Triaj testi |
| kamp | K1 = "Ne Çıktı Ne Çıkacak" PDF'inde spot olarak var · K0 = yok | Kampın kapsamı ve senin ölçtüğün tekrar oranı |
| hata_tipi | A–G (§1.3); yalnızca Y, B ve güveni ≤2 olan D için | |

### 1.3 Hata tipolojisi

Her maddeye tek birincil kod verilir: **ilk kırılma noktası** (sıra A → B → C/D → E → F/G).

- **A. Kapsam dışı:** Bilgi dershane kitabında yok.
- **B. Kapsamda ama çalışılmamış:** Kitapta var, ama geçiştirilmiş ve sen de üzerinde durmamışsın.
- **C. Çalışılmış ama hatırlanamamış:** Çizili ya da okunmuş, sınavda geri çağrılamamış.
- **D. Karıştırma:** İki benzer bilgi karışmış. Karışan çifti ayrıca kaydet.
- **E. Okuma hatası:** Olumsuz kök, öncül, "en az / en çok", birim.
- **F. Strateji hatası:** İki şıkka inip boş bırakmak ya da kör işaretlemek.
- **G. Süre:** Yetişmemek ya da acele etmek.

Şema; koordinatörün, r0_triaj_ongoru §6.2'nin ve r0_ogrenme_bilimi §4.2'nin kodlarını birbirini dışlayan tek listede birleştirir.

### 1.4 Dört sayı ve karar kuralları

1. **Kapsam_Ç** = Ç kodlu madde sayısı / 120. 120 maddede bu oranın belirsizliği yaklaşık ±%9 (%95 GA).
2. **h** = kitaplarda çizdirilmiş satırların payı. 14 kitabın her birinden 5 rastgele sayfa (70 sayfa, ~1 saat) yeter. Kitaplar sende kaldığı için bu adım 11 Kasım'dan sonra da yapılabilir.
   - **Lift = Kapsam_Ç / h.**
   - ≤1,2: çizdirme bilgi taşımıyor. 1,2–2: orta. >2: iyi.
3. **acc_Ç ile acc_G:** Çizili ve çizilmemiş maddelerdeki doğru oranın. acc_Ç belirgin biçimde yüksek değilse, çizdirme geri çağırmaya dönüşmemiş demektir.
4. **Kayıp dağılımı:** Yanlış ve boş maddelerin hata tiplerine dağılımı.

| Bulgu [analiz] | Teşhis | Plana etkisi |
|---|---|---|
| A+B ≥ %40 | Kapsam/triaj sorunu; şikâyetin haklı | K3 katmanı genişler, sprint 18 haftaya çıkar, başvuru kaynağı tam set olur |
| C+D ≥ %50 | Geri çağırma sorunu | Soru + aralıklı tekrar rejimi; kitap yalnızca başvuru kaynağı |
| F ≥ 5 madde | Strateji | Hemen düzeltilir, 2–5 net |
| E+G ≥ %10 | Okuma/süre | Zamanlı bloklar, kökü işaretleme alışkanlığı |
| Lift <1,2 ve acc_Ç ≈ acc_G | Çizdirme bu sınavda değersizdi | 2027'de çizili/çizilmemiş ayrımı yok sayılır |

- **Kendi tekrar oranın:** K1 maddelerin payını hesapla. DUSDATA 2026/1 için ~%35 sayıyor (r0_triaj_ongoru §2.2).
- K1 maddelerde doğru oranın düşükse, kamptaki spotlar da geri çağrılamamış demektir.

---

## 2. Dershane triaj iddiası nasıl okunur

- **Kapsam (recall):** Sınav sorularının notlarda "bir yerde" geçme oranı. Her sağlayıcı %82–98 ilan ediyor (r0_dershane_pazar §0.1). Bu yüzden sağlayıcıları birbirinden ayırmıyor.
- **İsabet (precision):** Vurgulananların ne kadarının sorulduğu. 3.676 sayfa ve 120 soru karşısında yapısal olarak küçük ve hiç yayımlanmıyor. Tekil bir "çıkacak" noktanın çıkma olasılığı %0,3–0,8 (r0_triaj_ongoru §4.2). "Çıkacak dedikleri yer çıkmadı" deneyimi beklenen sonuç.
- **Lift:** (vurgulanan alandan gelen soru payı) / (vurgulanan alanın payı). r0_triaj_ongoru §4.1'deki tabloya göre materyalin %40'ını vurgulayan ve lift'i 1,5 olan iyi bir sistemde bile 120 sorunun ~48'i vurgulanmayan yerden gelir. "Geçiştirdikleri yerden geldi" deneyimi bu yüzden tek başına kötü triajın kanıtı değil.
- **Satıcı verisinden hesaplanabilen tek lift** [satıcı verisi + analiz]:
  - RapiDUS (~997 sayfa) tam setin %27'si. Tam setin "referans" verdiği 115 sorunun 105'ini (%91) kapsıyor. Lift ≈3,4.
  - Kalan ~2.680 sayfa yalnızca ~10 soru getiriyor. Sayfa başına getiri RapiDUS'a göre ~28 kat düşük (r0_dershane_pazar §3.1).
  - Sonuç: Bu kullanıcının başvuru çekirdeği tam set değil, ~1.000 sayfalık sıkıştırılmış set olmalı.
  - Uyarı: "Referans" tanımı gevşek, değerlendirme sınavdan sonra ve aynı ekip tarafından yapılıyor, hesap tek oturuma dayanıyor.
- **Her "isabet" afişine sorulacak beş soru:**
  1. Payda ne (kaç sayfa, kaç nokta vurgulandı)?
  2. Tahmin önceden, zaman damgalı yayımlandı mı?
  3. Eşleşme bilgi noktası düzeyinde mi, konu başlığı düzeyinde mi?
  4. Değerlendirmeyi kim yaptı?
  5. Rastgele seçimle ya da bir rakiple kıyas (lift) var mı?

  Beşine de cevap "hayır" ise iddia pazarlamadır.
- **Kendi denetimin:** 2027'deki her "çıkacak" listesini (kamp, deneme, hoca) sınavdan önce tarihli PDF olarak sakla. 24 Ekim'den sonra isabeti, kapsamı ve listenin materyaldeki payını hesapla (r0_triaj_ongoru §6.2.7).

---

## 3. Kendi frekans haritası

### 3.1 Veri kaynakları

- **2012–2021 DUS:** ÖSYM "Geçmiş Yıllardaki Sorular", ~1.400 soru, ücretsiz [resmi] (r0_dus_sinav §5).
- **2022–2026:** Kamuya yalnızca %10'u açık. Lisanslı derlemeler: Klinisyen yıl yıl kitapçıkları (~321–429 TL), tüm DUS soruları uygulaması (960–1.680 TL) (r0_dershane_pazar §2.1).
  - Ürünün ÖSYM telif iznine sahip olup olmadığını kontrol et. Hatırlanan sorulardan kurulmuş setlerin cevap anahtarı hatalı olabilir.
- **2026/2:** Kendi AİS kodlaman.
- **TBT için TUS temel bilim çıkmışları:**
  - Yalnızca biyokimya, mikrobiyoloji, farmakoloji ve patoloji.
  - Son ~8 oturum (~550–600 soru), yalnızca DUS kapsamındaki başlıklar (r0_ortusme §6.3).
  - TUS'ta tekrar payı ~%50 (r0_triaj_ongoru §2.4).

### 3.2 Harita ayrı bir proje olmamalı

Haritayı arşivin ilk çözüm turunda kur: her soruyu çözdükten sonra 1 dakikalık bir etiket. Kaba hesap:
- ~2.640 DUS sorusu × ~2,5 dakika (çözüm, etiket, kısa analiz) ≈ **110 saat**.
- Aralık–Haziran'a yayılınca bu, yalnızca harita için haftada ~4 saat eder.

Bakım dozunun haftada **en az 6–8 saat** olması gerektiğinin veri gerekçesi bu. r0_sprint_takvim 4–8 saat, r1_aktif_hatirlama 8–10 saat öneriyor. Sprintin içinde harita kurmak 16 haftanın bir kısmını yer.

### 3.3 Şema: tek bir Sheets/Excel dosyası

- **`soru_bankası` sayfası:** soru_id (yıl-oturum-test-no), branş, konu_L1, konu_L2, bilgi_noktası, tip, kaynak_güveni (ÖSYM / lisanslı / hatırlanan), bağlı_soru_id (tekrar bağı), çeldirici_konuları.
- **`çözüm_kaydı` sayfası:** tarih, soru_id, banka, mod (zamanlı / konu), sonuç, güven, elenen_şık, süre, hata_tipi, kart_yazıldı.
- **`konu_skoru` pivotu:**
  - frekans: 22 oturum, son 8 oturum çift ağırlıklı.
  - çekirdek kitaptaki sayfa sayısı.
  - kişisel ilk-görüş doğruluk.

### 3.4 Puanlama

**Öncelik = (ağırlıklı frekans / oturum sayısı) × (1 − kişisel doğruluk) / saat maliyeti**

Bu formül "saat başına beklenen net kazancının" kaba hâli.

- **Zaman kişisel kayıp netine göre bölünmeli, dersin "önemine" göre değil.** Ders ağırlıkları sabit ve K puanında bir TBT neti ≈ bir KBT neti (0,48'e 0,49; r0_triaj_ongoru §1.1). Örnek: 10 soruda 4 doğru yaptığın dalda 6 net açık var, 8 doğru yaptığın dalda 2 net.
- **Oral Patoloji** hedefleniyorsa TBT ağırlığı ×1,5.
- **Katmanlar** (r0_triaj_ongoru §6.2):
  - K1: Tüm çıkmış noktalar ve bütün şıkları (sınavın ~%30–35'i).
  - K2: Öncelik sıralamasında ilk %30'a giren konular.
  - K3: Kalan konular, yalnızca soru ve kartla.
- **Sınır:** Bir oturumda başlık başına ~1 soru düşüyor. Harita zamanı dağıtır, soruyu tahmin etmez.

### 3.5 Ücretsiz hakemli taksonomi

Bağlantılar r0_triaj_ongoru §1.2'de.

| Branş | Kaynak | Taksonomi |
|---|---|---|
| Radyoloji | Yalçın & Topal 2025 | 4 kategori |
| Ortodonti | Aşkın & Kuğuoğlu 2026 | 13 başlık |
| Endodonti | Türkiye Klinikleri | 12 başlık |
| Periodontoloji | Güner 2025 | — |
| Restoratif | Acartürk 2023 | — |
| Cerrahi | Ünlü Kuzu & Şen 2026 | — |
| Pedodonti | Çerçi Akçay & Üstün 2026 | — |

- Protetik ve TBT için makale yok. Bu derslerde konu_L1 olarak RapiDUS içindekiler tablosu kullanılır.
- Makaleler çoğunlukla 2012–2021 verisine dayanıyor. Son 8 oturumu senin kendi kodlaman güncelleyecek.

---

## 4. −1/4 cezalı sınavda boş bırakma ve tahmin

- **Kural:** Seçeceğin şıkkın doğru olma olasılığı **%20'nin üstündeyse işaretle.** Beklenen net = (5p − 1)/4.
  - Bir şık elendiyse: +0,06.
  - İki şık elendiyse: +0,17.
  - İki şıkka inildiyse: +0,375 (r0_ogrenme_bilimi §4.3; r0_dus_sinav §1).
- **Eleme yanılabilir.** k şık elediysen, doğru cevabın kalan şıklar arasında olma olasılığı şu eşiklerin üstünde olmalı:
  - 1 şık elendiyse ≥%80,
  - 2 şık elendiyse ≥%60,
  - 3 şık elendiyse ≥%40.

  "İki şıkka indim" durumunda %40'lık eşik neredeyse her zaman aşılır. Bu yüzden iki şıkka inilmiş soru boş bırakılmaz.
- **Kalibrasyon:** Her blokta ve denemede güven kutusunu kaydet. Ayda bir "güven 2" kutusunun gerçek doğru oranına bak:
  - %40'ın altındaysa ÖSYM çeldiricisi seni sistematik olarak yanıltıyor (D tipi).
  - %20'nin altındaysa o tip soruda boş bırak.
- **Tavan:** Boş sayın 20 ise ve bunların yarısı iki şıkka inmişse, kural tek başına ~3–5 net getirir. Ucuz ama ana kaldıraç değil. Türkiye'deki cezalı sınav verisinde riskten kaçınma belgelenmiş (Akyol ve ark.; r0_ogrenme_bilimi §4.3).
- **Cevap değiştirme:** Gerekçeli değişiklikler daha sık yanlıştan doğruya gidiyor (Kruger 2005). "Değiştirdim" işaretini de kaydet.

---

## 5. Deneme kalibrasyonu ve haftalık metrikler

**Gürültü** [analiz, kaba model, calc.py]. %55–60 doğru yapan biri için madde örneklemesinden gelen gürültü:
- Tek denemenin netinde SD ≈ 6 net.
- İki deneme arasındaki farkta SD ≈ 9 net.
- Ardışık üçer denemenin ortalamaları arasındaki farkta SD ≈ 5 net.

Form zorluğundaki fark bunun üstüne eklenir. Yani tek denemede 8 net artış ya da düşüş bilgi taşımaz. Buna karşılık 300 soruluk kayan pencerede doğruluk oranının standart hatası ~3 puan, 500 soruda ~2 puan. Haftalık kararların aracı bu olmalı.

**Haftalık panel (6 sayı):**
1. Yeni (ilk kez görülen) soru sayısı. Sprintte haftada ~500–700 (r0_sprint_takvim §3.2).
2. İlk-görüş doğruluk: ÖSYM tipi, zamanlı, son 300 soru, TBT ve KBT ayrı.
3. **Gecikmeli düzeltme oranı:** En az 7 gün önce yanlış yapılan soruların yeniden çözümde doğru oranı. Anki'nin "true retention" değeriyle birlikte izlenir; hedef ≥%80–85. Teşhis "geri çağırma" çıkarsa birincil ölçü budur.
4. Son 2 haftanın hata tipi dağılımı. C+D payı düşmeli, E+F sıfıra inmeli.
5. Kalibrasyon: "güven 2" kutusunun gerçek isabeti ve iki şıkka inilip boş bırakılan soru sayısı (hedef 0).
6. Deneme neti: üçlü hareketli ortalama, TBT/KBT ayrı, boş sayısıyla birlikte. Sprintin 9. haftasından itibaren.

**Sağlık satırı:** 7 saatin altında uyunan gece sayısı ve hafif hafta kuralı (r0_sprint_takvim §3.2).

**İzlenmeyecekler:** sayfa sayısı, video saati, "kitap bitirme". Toplam saat de tek başına bir hedef değildir.

**Net hedefini doğruluk hedefine çevirme** [analiz]:
- 85 net (2026/1'de en düşük genel tabanların bandı; r0_dus_sinav §2.3) ≈ 15 boşla 89 doğru ≈ **%74 doğruluk**.
- Ortodonti/Cerrahi (~92–105 net) ≈ %78–85 doğruluk.
- Ara hedefler: Haziran sonu ilk-görüş doğruluk ≥%64, Eylül ortası ≥%70, Ekim ≥%73.
- Soru bankasının zorluğu ÖSYM'den farklı olabilir. Bu yüzden bir ankraj gerekiyor.

**Ankraj:**
- Kampta bütün spotları gördüğün için "hiç görülmemiş" bir ÖSYM oturumu muhtemelen kalmadı (r1_aktif_hatirlama §9 da bunu belirtiyor).
- En az 6 aydır tam olarak çözmediğin iki oturum ayır, örneğin 2023/1 ve 2024/1. Bunları Temmuz'da ve Ekim başında sınav saatinde çöz. Sonucu "üst sınır" olarak oku.
- Türkiye geneli denemelerde netten çok yüzdelik sırayı izle. Bu denemelerin norm grubu kurum öğrencileri ve ÖSYM netiyle korelasyonları yayımlanmıyor (r0_dershane_pazar §10).

**Büyüklük kontrolü** [hakemli, gözlemsel + analiz]:
- ABD verisinde +286 (Burk-Rafel) ile +445 (Deng) yeni soru ≈ +1 Step 1 puanı. Step 1'in SD'si ~20 puan alınırsa 1 SD ≈ 5.700–8.900 yeni soru.
- Kullanıcının +1,0–1,7 SD'lik açığı (r0_sprint_takvim §0.11) bu ölçekte kabaca 6.000–15.000 yeni soru eder. Bu yalnızca büyüklük sırası veriyor.
- **Kısıt:** Benzersiz ÖSYM DUS sorusu sayısı ~2.640. Hacmin geri kalanı denetlenmiş bir Türkçe bankadan, kurumların kamp ve denemelerinden ve ABD hedefi varsa INBDE bankasından gelmek zorunda. §6.2'deki platform denetimi bu yüzden zorunlu.

---

## 6. AI ve yeni nesil platformlar

### 6.1 AI'ın iş akışındaki yeri

| İş | AI kullanılır mı? | Koşul |
|---|---|---|
| AİS'teki 2026/2 soruları | Hayır | Telif. Yalnızca kendi notların |
| Sayım, pivot, metrik | Sayıyı tablo verir | AI formül yazabilir, sonucu tablo hesaplar |
| Taksonomi önerisi | Evet | Hakemli başlıkları verirsin, son kararı sen verirsin |
| Arşive etiket önerisi | Koşullu | %10'luk örneklemi elle etiketle. Uyum ≥%90 değilse bırak |
| Yanlış sonrası açıklama | Evet | Önce AI kapalıyken çöz. Claude learning mode ya da Gemini Guided Learning; P1 istemi (r0_ai_yeninesil §6.4) |
| Kaynaklı arama | Evet | Gemini Notebook (NotebookLM): kendi hata tablon, notların ve ÖSYM'nin açık 2012–2021 kitapçıkları. Her alıntıyı tıklayıp doğrula |
| Görselli soru, sayı, sınıflama | Hayır; kitaptan | Görselli sorularda doğruluk %45–64 (r0_ai_yeninesil §0.3) |
| "Çıkacak" tahmini | Hayır | Kanıt yok |

- **Başlamadan önce kalibrasyon:**
  - Cevabını bildiğin 50 ÖSYM sorusunu modele sor.
  - Bir branşta hata oranı %10'un üstündeyse o branşta açıklamayı yalnızca kitapla birlikte kullan.
  - Aynı soruyu iki ayrı sohbette sor. Cevap değişiyorsa o konuda modele güvenme (r0_ai_yeninesil §6.1).
- **Süre:** AI toplam sürenin %15–20'sini geçmemeli.

### 6.2 Platform seçim kriterleri

Yedi kriterden en az beşini sağlamayan platform ana banka olamaz.

1. **Soru kaynağı belli mi?** ÖSYM orijinali ya da lisanslı / kurum yazımı / hatırlanan soru / AI üretimi.
2. **Açıklamayı insan mı yazıyor, kaynak gösteriyor mu?**
3. **Örneklem denetimi:** 30 rastgele sorunun anahtarını ve açıklamasını kitapla kontrol et. 2 ya da daha fazla hata (~%7) çıkarsa platform yalnızca soru kaynağı olarak kullanılır.
4. **Biçim:** Türkçe, 5 şık, öncüllü ve olumsuz köklü sorular, zamanlı mod, cezalı net hesabı.
5. **Filtreler:** branş, konu, yıl, çözülmemişler, yanlışlarım.
6. **Veri dışa aktarımı:** Soru bazında sonuç, süre ve tarih CSV olarak alınabiliyor mu? Alınamıyorsa en azından branş istatistikleri.
7. **Süreklilik ve fiyat:** DUS Master'ın kapanma tartışması ve DUSPort'un ücretliye geçmesi örnek (r0_ai_yeninesil §3).

"AI destekli" etiketi tek başına artı değildir. Doğruluk verisi yayımlamayan ürün (EasyDUS, DusNote) 2. kriterden puan alamaz.

---

## 7. Dallanma: kullanıcı değişkenleri

| Değişken | Durum | Triaj ve ölçüm planına etkisi |
|---|---|---|
| Okul | CODA (Dal A, ör. 2024 sonrası Yeditepe; doğrulanmalı) | Kalma riski düşük (CODA ilk girişte %7,2; r0_inbde_sinav §5). INBDE bankası Kasım–Mart'ta aktif hatırlama aracı, sınav Mart'ta. DUS haritası Nisan–Haziran'a sıkıştırılır |
| | CODA değil (Dal B) | İlk girişte kalma ~%35, tekrar girişte ~%50. INBDE yalnızca ABD hedefi ciddiyse. Harita Kasım–Haziran'a yayılır |
| İngilizce | ≥B2 / B1–B2 / <B1 | ≥B2: AI açıklaması İngilizce istenebilir (~4 puan doğruluk farkı; r0_ai_yeninesil §0.4). <B1: 2027'de INBDE yok, önce YDS |
| Çalışma | yok / yarı zamanlı / tam zamanlı | Tam zamanlı: bakım 4–6 saat, sprint 20–24 hafta. Haritada yalnızca konu_L1 etiketi, bilgi noktası yok |
| Hedef | yalnız DUS / +ABD / +Kanada / önce ABD | Kanada: AFK, DUS'a INBDE'den daha yakın (r0_ortusme), ama 13 Ağustos 2027 sprintin içine düşüyor. Öneri: 2028 |
| Branş | Ortodonti/Cerrahi / diğerleri | Doğruluk hedefi %78–85 / %72–76 |
| YDS | yok | Ocak–Nisan 2027'de e-YDS ya da YDS. Sprintin içindeki tarihlerden kaçın |
| 61'in bileşimi | boş ≥20 | Önce §4'teki strateji düzeltmesi |
| AİS teşhisi | §1.4 | Karar kuralları planın ağırlığını belirler |

---

## 8. Ay ay takvim (Kasım 2026 – Ekim 2027)

Temel senaryo: çalışmıyor, DUS birincil hedef. Köşeli parantez içindekiler Mart INBDE dalı.

- **Kasım 2026:**
  - 3–11 Kasım: AİS denetimi, öncelik sırası 1–3.
  - 12–25 Kasım: dinlenme. Kitaplardan sayfa örneklemi (h). Arkadaşlardan veri: ders bazında net, boş sayısı, çözülen soru sayısı.
  - 26 Kasım: sonuç gelir. D/Y/B'yi düzelt, dört sayıyı hesapla, karar kuralını uygula.
  - Lisanslı 2022–2026 derlemesini al, tabloyu kur.
  - [DENTPIN, ECE, vize randevusu]
- **Aralık:**
  - AI kalibrasyon testi ve taksonomi.
  - Arşivin ilk turu TBT'den başlar (ortalama başarı düşük, kazanılacak alan geniş). Haftada 6–8 saat.
  - [JCNDE başvurusu]
- **Ocak 2027:**
  - Arşivin ilk turu sürer. Anki yalnızca kendi hatalarından.
  - 16 Ocak e-YDS (gerekirse).
  - [INBDE yoğun dönem. DUS'a haftada 2–3 saat, yalnızca kart.]
- **Şubat:**
  - Harita v1'in TBT kısmı biter. 6 Şubat e-YDS.
  - [1 Şubat karar kapısı: vize kesinleşti mi, ECE gönderildi mi, son 2 haftanın karma doğruluğu satıcının hedefinde mi?]
- **Mart:**
  - KBT arşivi. 28 Mart YDS.
  - [~15–22 Mart INBDE. Harita durur.]
- **Nisan:**
  - Harita v1 tamamlanır (2012–2026). konu_skoru'nun ilk sıralaması çıkar.
  - 24 Nisan e-YDS.
  - [2 hafta dinlenme, ardından haritaya haftada 9–10 saat]
- **Mayıs:**
  - TUS temel bilim katmanı. Karışıklık çiftleri listesi.
  - Arşivin ikinci turu başlar: yalnızca yanlışlar ve şıklar.
  - [Kalındıysa Mayıs sonunda tekrar giriş]
- **Haziran:**
  - Başvuru çekirdeği (~1.000 sayfa) seçilir.
  - 30 soruluk platform denetimi. Deneme serisi seçimi. Sprint panelinin kurulması.
  - Ara hedef: ilk-görüş doğruluk ≥%64.
- **Temmuz:**
  - 5 Temmuz: 16 haftalık sprint başlar (r0_sprint_takvim §4).
  - 1. hafta tanı: ankraj #1 ve AİS verisiyle birleşik branş × hata matrisi.
  - Faz 2: soru güdümlü ilk tur.
- **Ağustos:**
  - Faz 2 biter (22 Ağustos). Haftalık panel.
  - 21 Ağustos e-YDS'den ve 13 Ağustos AFK'dan kaçın.
- **Eylül:**
  - Faz 3: her pazar 10.15'te deneme ve ardından 2–3 saat analiz.
  - 7–15 Eylül: DUS başvurusu.
  - "Çıkacak" listelerini tarihli olarak arşivle.
  - Ara hedef: ≥%70.
- **Ekim:**
  - Ekim başı: ankraj #2.
  - 11–24 Ekim: hafifletme. Yeni konu yok; yalnızca hata kartları ve K1.
  - 17 Ekim: son deneme. 24 Ekim: DUS.
  - Sonra: "çıkacak" listelerinin isabet denetimi, 18 Kasım'da sonuç ve değerlendirme.

---

## 9. S1–S13

**S1 – Nasıl ve ne ile hazırlanmalı?**
- Döngü: teşhis (§1) → konu haritası (§3) → önce soru, sonra kitapta yalnızca ilgili sayfa → hatayı kodla, karta çevir → kalibre edilmiş deneme (§5).
- Araçlar: ÖSYM arşivi (resmi + lisanslı), seçilmiş TUS temel bilim soruları, ~1.000 sayfalık başvuru çekirdeği, Anki (FSRS), tek bir Sheets dosyası, §6.2'den geçen bir Türkçe banka, Türkiye geneli deneme serisi.
- Dayanak: r0_ogrenme_bilimi §7, r0_dershane_pazar §9.

**S2 – DUSDATA ve benzerleri ne kadar faydalı?**
- Veri altyapısı olarak faydalı (arşiv, kapsam haritası, deneme normu). Öğrenme yöntemi olarak (pasif anlatım, çizme) düşük faydalı (Dunlosky 2013). Triaj olarak ölçülmemiş.
- Senin için ucuz kalemlerin değeri yüksek (1.750–15.000 TL), tam paketlerinki (87.500 TL+) düşük (r0_dershane_pazar §2.2). Etkiyi ölçen hakemli çalışma yok (r0_triaj_ongoru §5).

**S3 – Dershaneler triaj görevini yerine getiriyor mu?**
- Sıkıştırma düzeyinde kısmen evet: RapiDUS lift ≈3,4, satıcı verisi.
- Tahmin düzeyinde hayır: tekil isabet <%1. "Referans" sayıları kapsam ölçüsü ve sağlayıcıları ayırt etmiyor.
- Senin şikâyetin taban orana uygun (§2). Lift hesabıyla, 11 Kasım verisinden test edilmeli.

**S4 – İkinci maratonda ne farklı olmalı, neyle çalışılmalı?**
- Girdi metriklerinden (sayfa, saat) çıktı metriklerine geçilmeli: gecikmeli düzeltme oranı ve ilk-görüş doğruluk.
- Kurumsal yalnızca arşiv ve deneme için; yeni nesil §6.2 denetiminden geçerse; AI öğretici ve kaynaklı modda, sürenin %15–20'si; ABD uygulaması yalnızca ABD hedefi varsa.
- "Neyle beraber": hata kodlarını çapraz kontrol edecek, haftalık paneli görecek bir hesap verebilirlik ortağı.

**S5 – Optimum sprint süresi:**
- 16 hafta (aralık 14–18), 5 Temmuz – 24 Ekim (r0_sprint_takvim §6).
- Veriye bağlı ayar:
  - F/E tipi baskınsa 14 hafta.
  - A/B tipi baskınsa 18 hafta.
  - C/D tipi baskınsa 16 hafta, ama bakım dozu haftada 6–8 saat ve harita sprintten önce bitmeli.
- Tam zamanlı çalışıyorsan 20–24 hafta.

**S6 – ABD/Kanada için en verimli yol:**
- INBDE'nin resmi test spesifikasyonu zaten resmi bir triaj haritası: Practice & Profession %22, FK9 %11, FK10 %10 (r0_inbde_kaynak §0). Dershaneye gerek yok.
- Tek bir banka seç, FK bazında ilk-görüş doğruluğunu izle. JCNDE'nin 39 örnek sorusunu ve satıcı simülasyonunu ankraj olarak kullan. Hatırlanan soru PDF'leri yasak.
- Kanada: NDEB'in ücretsiz 100 soruluk öz değerlendirmesi ankrajdır. AFK planı DUS'a daha yakın.
- CODA (Dal A) ve CODA dışı (Dal B) için risk ve hazırlık süresi farklı (§7).

**S7 – En verimli uygulama:**
- DUS: Doğruluğu bağımsız ölçülmüş bir uygulama yok. Pratik yığın: lisanslı tüm DUS soruları uygulaması + Anki + Sheets.
- INBDE: Booster ya da Bootcamp, ücretsiz denemeyle seçilir. Booster'ın garantisi uluslararası adayları da kapsıyor, Bootcamp'inki kapsamıyor (r0_inbde_kaynak §0). FK bazında analitiği olan tercih edilir.

**S8 – Başarı oranı en yüksek sistemler:**
- Hiçbir sistemin bağımsız ölçülmüş başarı oranı yok: derece afişlerinin paydası yok, iki INBDE satıcısı da "%90+ bizi kullandı" diyor (r0_inbde_kaynak §3). Puanla ilişkili olan sistem değil davranış (yeni soru, aralıklı tekrar, erken başlama); ticari kurslarla net ilişki yok (Burk-Rafel 2017).

**S9 – İdeal süre ve yoğunluk:**
- Sprintte ~500–600 saat odaklı çalışma ve 7.000–10.000 soru. Bakım döneminde ~150–200 saat.
- Günde 5–6 saat odaklı çalışma, haftada 6 gün (r0_sprint_takvim §3).
- Saat bir kısıt, hedef değil. İlk-görüş doğruluk 3 hafta üst üste artmıyorsa çözüm daha fazla saat değil, hafif bir hafta.

**S10 – Mart mı Mayıs mı?**
- Kapılar geçilirse (vize, ECE, hazırlık düzeyi) Mart, Mayıs'tan iyidir. Kalma durumunda tekrar giriş DUS sprintinden önce sığar.
- CODA dışı mezunda, DUS birincilse, Mart'ın asıl alternatifi Mayıs değil, DUS'tan sonrası.
- Mayıs yalnızca "kalırsam tekrar DUS'tan sonra" kuralını önceden koyarak seçilebilir.
- Karar 1 Şubat'ta veriye göre verilir (r0_sprint_takvim §5).

**S11 – ABD çalışmasının DUS'a faydası:**
- DUS sorularının ~%55–65'ini içerik olarak karşılıyor (r0_ortusme).
- En çok faydalı olduğu dersler: farmakoloji, patoloji, mikrobiyoloji, endodonti, periodontoloji, pedodonti, cerrahi. En az: biyokimya, genetik, ortodonti apareyleri, radyasyon fiziği.
- Ölçme yöntemi: INBDE sorularını DUS branşlarına etiketle ve branş doğruluğunun değişimini izle.

**S12 – DUS'a doğrudan ABD uygulamalarıyla girilirse:**
- Model ~47–73 net (ortası ~60). Hibrit yaklaşımda ~73–96 (ortası ~84) (r0_ortusme §6.1).
- Eksik kalanlar: ~%35'lik tekrar katmanı (K1), cezalı ve öncüllü format, Türkçe terimler.
- Ek risk: cezasız sınava alışmak, boş bırakma ve tahmin davranışını bozar.

**S13 – Arkadaşlar neden daha yüksek net yaptı?**
- En olası açıklama birden fazla etkenin toplamı: seçilim, yöntem, tazelik ve düşük kaygıyla daha cesur işaretleme (r0_ogrenme_bilimi §6).
- Arkadaşlardan istenecek veri: ders bazında net, boş sayısı, çözülen soru sayısı, fakülte ortalaması, DUS çıkmışı çözüp çözmedikleri. Yalnızca yüksek netler duyulmuş olabilir; deneme amaçlı girenlerin hepsinin netleri istenmeli.
- Öngörüler: örtüşme belirleyiciyse fark farmakoloji, patoloji, endodonti, periodontoloji ve pedodontide toplanır. Seçilim belirleyiciyse fark derslere eşit yayılır ve not ortalaması farkı görülür. Cesaret belirleyiciyse arkadaşlarda daha az boş, daha çok yanlış görülür.

---

## 10. Önermeler (oylanabilir)

1. **Tam payda kuralı:** 11 Kasım'a kadar 120 maddenin tamamı kodlanmalı; yalnızca yanlış ve boşlar değil. Doğruların da "kaynak durumu" doldurulmadan dershane triajı hakkında hüküm verilemez.
2. **Teşhis öngörüsü ve dallanma:** Kaybedilen maddelerin (yanlış ve boş) en az %50'si C/D tipinde (çalışılmış ama geri çağrılamamış ya da karıştırılmış) çıkacak, A tipi (materyalde yok) %15'i geçmeyecek. Plan şu kurala göre dallanmalı:
   - A+B ≥ %40 ise kapsam genişletilir.
   - C+D ≥ %50 ise geri çağırma rejimi uygulanır.
   - F ≥ 5 madde ise önce strateji düzeltilir.
3. **Başvuru çekirdeği:** 2027'de dolu tam set yeniden okunmamalı. Başvuru kaynağı ~1.000 sayfalık sıkıştırılmış set olmalı. Satıcının kendi verisine göre bu set, tam setin kapsadığı soruların ~%91'ini sayfaların ~%27'siyle taşıyor (lift ≈3,4).
4. **Harita sprintten önce:** Kendi frekans haritan (2012–2026 DUS ve seçili TUS temel bilim) 5 Temmuz 2027'den önce, arşivin ilk çözüm turunda etiketlenerek bitirilmeli. Bunun için Kasım–Haziran bakımı haftada en az 6–8 saat olmalı. INBDE dalında bu iş Nisan–Haziran'a sıkıştırılır.
5. **Haftalık ölçü:** Haftalık ilerlemenin birincil ölçüsü deneme neti değil, iki sayıdır: gecikmeli düzeltme oranı ve 300 soruluk kayan pencerede ilk-görüş doğruluk. Ardışık iki deneme arasındaki 9 nete kadar fark gürültü sayılmalı.
6. **%20 kuralı:** Seçilecek şıkkın doğru olma olasılığı %20'yi aşıyorsa işaretlenmeli. İki şıkka indirilmiş soru hiçbir zaman boş bırakılmamalı. Kural güven kalibrasyon tablosuyla doğrulanmalı. Kuralın tavanı ~3–5 net; ana kaldıraç değil.
7. **Lift'siz iddiaya para yok:** Lift'i ya da zaman damgalı isabet oranını yayımlamayan hiçbir "çıkacak" ürününe 2027'de para ve saat verilmemeli. "X/120 referans" afişleri triaj kanıtı sayılmamalı.
8. **AI ve platform kuralı:**
   - AI sayım ve tahmin yapmaz.
   - AİS soruları hiçbir AI aracına yüklenmez.
   - AI'dan arşiv etiketi alınacaksa %10 örneklemde ≥%90 uyum şartı aranır.
   - Platform 30 soruluk denetimde ≥2 hata çıkarırsa yalnızca soru kaynağı olur.
   - Soru bazında sonuç dışa aktaramayan platform ana banka olamaz.

---

## 11. Belirsizlikler ve kullanıcıdan istenen veri

**Belirsizlikler:**
- Net → puan modeli ±5–8 net belirsiz (r0_dus_sinav §7).
- Tekrar oranları ve "referans" sayıları satıcının kendi kodlaması.
- Lift ≈3,4 tek oturuma ve gevşek bir tanıma dayanıyor.
- Gürültü hesabı kaba bir binom yaklaşımı.
- ABD'deki soru-puan eğimleri gözlemsel ve DUS'a aktarılmaları belirsiz.
- Resmi aday cevaplarının 26 Kasım'da açılacağı 2026/1 örneğinden çıkarıldı. 2026/2 için doğrulanmadı.

**Kullanıcıdan istenen veri:**
- Hangi oturuma girdin, 61 neti nasıl hesapladın, TBT/KBT dağılımı ve boş sayısı.
- AİS kodlaması.
- Okul ve mezuniyet yılı (CODA).
- İngilizce düzeyi, çalışma durumu, hedef ve branş, YDS ve vize durumu.
- 7–8 ayda çözdüğün soru sayısı.
- Kamp PDF'ine ve dershane uygulamalarına erişimin ne zaman bitiyor.
- Arkadaşların ders bazında netleri, boş sayıları, çözdükleri soru sayısı ve fakülte ortalamaları.
