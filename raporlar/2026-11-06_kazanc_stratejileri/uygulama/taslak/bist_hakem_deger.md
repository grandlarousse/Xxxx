# Hakem raporu (DEĞER lensi): BIST/VİOP taslakları A, B, C

- **Tarih:** Cuma 06.11.2026, ~14:00 TSİ. Plan başlangıcı Pazartesi 09.11.2026.
- **Lens:** Maliyet ve vergi sonrası beklenen değer, vergiye göre düzeltilmiş TL engeliyle (ileriye dönük net ~%31–36) karşılaştırılıyor. Sorular: "yüksek getiri" isteği dürüstçe karşılanıyor mu, beklenmesi gereken getiri ve düşüş dağılımı ne?
- **Okunanlar:** Üç taslak, `dogrulama/v_bist.md`, `v_capraz.md`, `v_profesyonel.md` (T12), `v_dalga.md` (B2, B12), `ajanlar/bist_test.md` §5, `bist_swing_kenarlar.md` §5.1, §5.3, §9.1, `tr_makro_engel.md` §5, `olay_halka_arz.md` §0, komite raporu §2 ve §4.1–4.2, 5.11 resmi VİOP bülteni (`viop_20261105.csv`, oturum önbelleği) ve A'nın ek betikleri (`scratchpad/bistA/an1.py`, `an2.py`).
- **Taslaklardan sonra gelen dosya:** `ajanlar/olay_akis_rejim.md` (11:23) artık klasörde. A ve B yazılırken yoktu; C yalnız ara tablolarını gördü. Doğrulaması (`v_olay.md`) ve `olay_bedelsiz.md` hâlâ yok. Bu raporda `olay_akis_rejim` bulguları **doğrulanmamış** diye işaretlenmiştir.
- **Uygulama hakemiyle ilişki:** Uygulama hakeminin (`bist_hakem_uygulama.md`) bulduğu çelişkilerin bir kısmını birincil veriden yeniden kontrol ettim ve aynı sonuca vardım: komite §4.2'deki 160 mlr $ eşiği, bültendeki opsiyon işlem fiyatları, temettü penceresinin günü. Değer lensinin farkı, beklenen değer muhasebesi ve kazanan seçimidir.

---

## 0. Kısa hüküm

1. **"Yüksek getiri" isteğini bu rejimde dürüstçe karşılayan taslak yok, ve karşılayabilecek bir kanıt da yok.** Düzeltmelerden sonra üçünün engel üstü merkezi beklentisi birbirine yakın: yılda **+1…+2 puan**. Hepsinde 12 ayda engelin altında kalma olasılığı %35–50.
2. **Farkı üç şey yaratıyor:**
   - Beklentinin engele göre doğru hesaplanıp hesaplanmadığı.
   - Kuyruk riskinin büyüklüğü.
   - Rejim dönerse yukarı opsiyonelliğin ne kadar hazır olduğu.
3. **Kazanan (değer lensi): C, A'nın yukarı motoru aşılanarak.**
   - C kanıta en sadık plan. Engeli en doğru ölçüyor ve kuyruğu en dar tutuyor. Bugün pozitif beklentili, doğrulanmış küçük kenarları da açık tutuyor.
   - A'nın kırılım motoru ve bekleme listesi, rejim döndüğünde kullanıcının istediği sağ kuyruğu veren tek hazır yapı.
4. **B'nin Pazartesi eylemleri** (carry açılışı ve settlement fiyatından strangle) doğrulanmış kaynaklarla çelişiyor. B'nin engel muhasebesi formülü ise en iyisi ve alınmalı.

---

## 1. Puan tablosu (0–10)

| Kriter | A | B | C | Gerekçe (kısa) |
|---|---|---|---|---|
| Kanıt sadakati | 7 | 5 | 8 | A: bist_test'e sadık. Basit ve bileşik oranlar karıştırılmış, S1 katkısı engelden düşülmemiş. B: birincil veri işi iyi, ama dört kuralı kaynağıyla çelişiyor (§4). C: gecikmeli çift rakamları, düzeltilmiş rf ve iskontolar doğru kullanılmış |
| Pazartesi uygulanabilirlik (gün içi yok, teminat, emir, likidite, limit kilidi) | 7 | 5 | 6 | A: Pazartesi yalnız çekirdek ve alarm var, emirler kapanış seansında. B: Pazartesi 10:00'a yazılı aracı kurum cevabı gerekiyor, ayrıca carry ve iki bacaklı opsiyon emri var. C: çiftler 09:30 limitle ve 17:50 bacak kontrolüyle giriliyor; mevduat dilimleri aynı haftaya yığılmış |
| Risk kontrolü ve en kötü durum | 6 | 6 | 8 | A: AÇIK rejimde brüt %60, iki taban stresi %11,4; öldürme kuralları engele göre düzeltilmemiş. B: ortak stres sınırı ≤%10 iyi, ama Pazartesi kuyruğu banka long'uyla aynı yönde olan carry açılıyor. C: açık risk %2,5, stres %6, birikimli −%4/−%6 kesicileri var |
| Beklenen değerin engele göre gerçekçiliği | 5 | 6 | 8 | A: S1'de brüt nominal × brüt hareket hesaplanmış, işlem başı R engelden düşülmemiş. B: "bağlanan nakit × engel" formülü doğru, ama S1'deki banka katkısı tetiğin zamanında gelmesine koşullu ve olasılıkla ağırlıklandırılmamış. C: bileşenlerin toplamı tutuyor, kıyas PPF kovasına göre yapılmış, 12 ayda ayrışmanın istatistiksel olarak görünmeyeceği söylenmiş |
| Profil uyumu (swing, yüksek ödül, kümeler) | 8 | 6 | 5 | A: kırılım, küme, piramit ve pay vadelisi kullanıyor, sağ kuyruk peşinde. B: makro ve opsiyon ağırlıklı, kümeler yalnız risk bloğu. C: yüksek ödülü açıkça kapsam dışı bırakıyor |
| **Toplam / 50** | **33** | **28** | **35** | |

---

## 2. Değer muhasebesi: iddia edilen ve düzeltilmiş beklenti (12 ay, vergi ve maliyet sonrası, engel üstü puan)

| Taslak | İddia: merkez (%80 aralık) | İddia: P(engel altı) / düşüş | Düzeltilmiş merkez (bu hakem) | Ana düzeltme |
|---|---|---|---|---|
| **A** | ≈ +2 (−4…+12) | %40–50; KAPALI'da düşük, AÇIK'ta hesap düzeyinde −%10…−%20 | **≈ +1…+1,5** | (1) A'nın kendi §8.1 tablosunun orta noktaları **+3,4** veriyor, metin **+2** diyor; tablo iç tutarsız. (2) S1 satırı (+5…+15), "brüt %30–50 nominal × liderlerde %20–40 hareket" olarak hesaplanmış. Kullanılan nakdin ~6–9 aylık engel getirisi (spotta %16–27, vadelide ima taşıma %13–20) düşülmemiş. Düzeltilince S1 ≈ +1…+10, merkez ~+4,5. (3) İşlem başı E[R] = +0,3…+0,5R engelden düşülmemiş. 40–60 günlük tutmada engel ≈ %4–6 ≈ 0,3–0,4R. A'nın kendi [EK-1] verisinde VİOP-47 2024–26 ortalaması **+%4,2 / ~60 gün** (t 1,9), yani aynı dönemde nakdin (~%6–7) altında |
| **B** | +0…+4, merkez +2…+3 | %35–45; engele göre −%6…−%10 | **≈ +1,5…+2** | (1) Tablonun orta noktaları +3,5 veriyor. Bunun +3,85'i S1'deki K2'den geliyor ve "tetik zamanında ateşlenirse" koşuluna bağlı. Tetik için L1, L2 ve ≥5/8 birlikte gerekiyor; P(zamanında \| S1) ≈ %50–60 alınınca S1 katkısı ~+2. (2) L2, kaynağındaki "2 ay üst üste" yerine tek ayla kurulmuş (§4). (3) K2 tam 10.12 PPK indirimini kapsıyor; döngü içi indirimlerden sonra bankalar XU100'ün gerisinde kalıyor (`olay_akis_rejim` §4.2, doğrulanmamış). (4) Carry Pazartesi açılıyor: +0,2…+0,5 puanlık beklenti karşılığında −2,5…−3,5 puanlık, banka kuyruğuyla aynı yönde bir kuyruk alınıyor |
| **C** | +1,5 (KAPALI −2…+3); ağırlıklı +1,7 (−2…+5) | Merkez %33–37 toplam; uydu −%4/−%6 kesicileri | **≈ +1…+1,5** | (1) K6 carry kapısı kapalı olduğu halde +0,3 puan sayılmış (yarım yıl açık varsayımı); ~+0,1. (2) Teminat faizsizse çift kollarında −0,3…−0,6 puan teminat sürtünmesi var; C bunu kendisi yazıyor. (3) Çift girişi 09:30 limitle yapılıyor, test edilen giriş t+1 kapanışı; ters seçim riski var. (4) Temettü kolu hedge'siz kalırsa piyasa düzeltmeli +%0,9'un tamamı engel üstü sayılamaz |

**Ortak sonuç.** Üç plan da S2 (yatay kanama, %40) senaryosunda pratikte engelde kalıyor (−1…+2,5). Pozitif beklentinin büyük kısmı S1'den (%35, öznel) geliyor. Planların asıl farkı, S1 gelmezse ne kadar kaybettikleri ve gelirse ne kadarını yakaladıkları.

**Çekirdeğin bileşimi küçük değil.** Faizler sabit kalırsa 32 günlük mevduat merdiveni net ~%37,9 bileşik, banka PPF'si ~%34–35 (v_capraz #4). Aradaki fark ~3 puan:
- PPF'ten mevduata kaydırılan her %15, hesaba ~+0,45 puan ekler.
- A %60/%40, B %55/%30, C %45/%40. C'nin %15 DİBS'i teyit edilemezse C'de bu pay PPF'ye gider, yani 45/55 olur.
- A'nın çekirdeği C'ninkinden yılda ~+0,4–0,5 puan fazla kazandırır. Bu, C'nin uydu kenarlarının çoğundan büyüktür ve risksizdir. Sınırı likidite ihtiyacı belirler.

---

## 3. Kazanan ve gerekçe

**Kazanan: C (35/50), iskelet olarak.** Aşılar:
- A'nın A1 kırılım motoru, rejim tablosu ve bekleme listesi.
- A'nın mevduat ağırlığı.
- B'nin engel muhasebesi formülü ve XU030 nakit-taşıma açma kuralı.

Gerekçeler:
1. **Engel doğru tanımlanmış.** Uydu getirisi, aynı sermayenin PPF kovasında kazanacağı getiriye göre ölçülüyor (C §1.3 m.3). Hipotez kartlarındaki beklentiler "çekirdeğe göre" yazılmış (C §7.1). A'nın öldürme kuralları ise ham R üzerinden (A §7.5 K1–K3). Nakde yenilen bir kırılım kolu bu kurallarla yaşamaya devam edebilir.
2. **Bugün pozitif beklentili, doğrulanmış kenarlar açık.**
   - Temettü öncesi 5 gün: v_bist #26 DOĞRU, t 6,5.
   - SAHOL↔AKBNK 20 günlük çift: v_bist #25, gecikmeli t 2,4/2,8.
   - A ikisini "başka açıların kolu" diye dışarıda bırakıyor (A §2.4). S2'de A'nın getirisi bu yüzden yalnız çekirdek ±0,5.
3. **Kuyruk en dar.** KAPALI'da stres tavanı %6, birikimli −%6'da uydu kapanıyor. Kullanıcının bu rejimdeki en olası kötü yılı engelin ~4–6 puan altı. A'nın AÇIK rejimdeki −%10…−%20 bandı ve B'nin −%6…−%10'u daha geniş.
4. **"Yüksek getiri" sorusuna en dürüst cevap C'de** (C §8.3 m.3). +10–20 puan, 3–5 kat açık risk ve engele göre −%25…−%40 düşüş toleransı ister; bu rejimde kanıt bunu desteklemiyor.

**A neden ikinci (33):** Profile en uygun ve sağ kuyruğa en hazır plan A. Kırılım kanıtı da (bist_test §5.1, S5 t 5,4) bu çalışmanın en güçlü hisse seçimi bulgusu. Ancak beklenti tablosu engelden düşülmemiş, bugünkü pozitif kenarlar boş bırakılmış, AÇIK'ta brüt %60 bu kanıt düzeyi için ağır.

**B neden üçüncü (28):** Primer veri işi en iyi B'de: bülten ayrıştırması, SPK metinleri, Black-76, banka vadelilerinin ima faizi. "Engele göre fazla K/Z" formülü de en doğrusu. Ama Pazartesi yapılacak iki işlem (K1 carry, O3 strangle) doğrulanmış kaynaklarla çelişiyor. Yukarı motoru K2 (önce bankalar) ise n=4 kanıta dayanıyor ve yeni faiz döngüsü bulgusu zamanlamasının aleyhine.

---

## 4. Ölümcül ve ciddi kusurlar (değer açısından)

### A: ölümcül kusur yok; değeri şişiren üç ciddi kusur var
1. **S1 katkısı ve işlem başı R engelden düşülmemiş** (A §8.1, §2.1 beklenti tablosu, §7.1). Hesap düzeyi beklenti ~+2 değil, ~+1…+1,5. Öldürme ve ölçekleme kuralları (A §7.4–7.5) ham R'ye bakıyor. 2024–26 tipi rejimde nakde yenilen bir kol "R > 0" diye büyütülebilir.
   - Düzeltme: R_fazla = (net_TL − bağlanan nakit × engel × gün/365) / R_TL. Kurallar R_fazla'ya bağlanmalı.
2. **Basit ve bileşik oranlar karıştırılmış** (A §1.1, §2.1.3).
   - XU030 taşıma için "mevduattan ~8 puan düşük" deniyor; doğrusu basitte 3,3, bileşikte ~5,7 puan (v_profesyonel T12; v_capraz #4).
   - Pay vadelisi finansman avantajı "mevduattaysa 8–13 puan" deniyor. Basit-basit kıyasla (mevduat net %32,6, ima %25–29) **~3,5–7,5 puan**. PPF'e göre (net ≈ TLREF × 0,825 ≈ %29,6 basit) **~0** (C §1.2 notu).
3. **KAPALI rejimde doğrulanmış küçük kenar yok.** %40'lık S2 senaryosunda plan çekirdekten ibaret kalıyor. Kullanıcı "stratejik küme" ve getiri istiyor; temettü ve çift kolları rejimden bağımsız.

### B: Pazartesi eylemleri için ölümcüle yakın
1. **K1 carry, kaynağının çıkış koşulu varken açılıyor.**
   - Komite §4.2'nin çıkış/yanlışlama listesinde "brüt rezerv 160 mlr $'ın altına inerse" var. Değer 158,1 (v_capraz #18).
   - Aynı hafta swap hariç net rezerv −6,5 mlr $, yabancı DİBS satışı −750 mn $ (Nisan'dan beri en büyük).
   - Komitenin başabaş hesabı (§2 m.5): 2018 tipi gap olasılığı %4'ü aşarsa beklenen değer negatif. Öznel S3+S4 olasılığı 1–6 ayda %25.
   - Getiri %10 stopajlı; kuyruğu banka long'uyla aynı (v_capraz §2.8). **Pazartesi K1 = 0 olmalı.**
2. **O3 strangle'ın limiti uzlaşma fiyatına bağlı (≤320 puan).**
   - 5.11 bülteni: P14000 uzlaşma 137,43, son işlem 100,0 (1.052 adet). C15500 uzlaşma 174,14, son işlem 98,6 (73 adet, 9 işlem). İşlem fiyatlarıyla strangle ~199 puan.
   - Komite §4.1'in uyarısı: "uzlaşma seviyesinden alınırsa beklenen değer sıfır veya negatif."
   - "Ucuz vol" avantajı ancak işlem seviyelerine yakın dolumla var; ≤320 limiti bunu korumuyor.
   - Büyüklük küçük (%0,3), değere etkisi ±0,1–0,3 puan. Ama kural yanlış kurulmuş.
3. **K2'nin zorunlu tetiği L2 kaynağından gevşetilmiş.** tr_makro §5.1 "aylık TÜFE < %2,0, **2 ay üst üste**" diyor; B tek ay alıyor ve "en erken TAM 3.12" diyor. Kaynağa göre en erken tarih Aralık TÜFE'sinin açıklandığı ~3.1.2027. A ve C de tek ay kullanıyor, ama orada tetik zorunlu değil, 3 tetikten biri.
4. **K2 zamanlaması yeni bulguyla çelişiyor** (doğrulanmamış).
   - `olay_akis_rejim` §4.2/§4.5: döngü içi sürprizsiz indirimden sonra XBANK/XU100 21/42/63 günde −%2,3 / −%4,8 / −%6,6 (n=24); döngü düzeyinde 6/6 negatif.
   - Bankalar son 63 günde XU100'e karşı zaten +%26 koştu.
   - B'nin "en erken TAM 3.12" tarihi 10.12 PPK'dan bir hafta önce. "Önce bankalar" önceliği tam bu pencerede zayıf.
5. **Bedelsiz ve temettü pencereleri test edilenden farklı.**
   - Bedelsiz: test penceresi hak kullanımına göre [−20,−1]. SPK onayı sonrası literatürde negatif KAAR var (bist_swing §5.1).
   - Temettü: B gün −5 kapanışında alıyor; test edilen [−5,−1] penceresi gün −6 kapanışında giriş ister (bist_swing §5.3). C doğru kurmuş. B'nin sürümü sürüklenmenin ~1/5'ini kaçırır.

### C: ölümcül kusur yok; ciddi kusurlar
1. **Çift girişi 09:30'da, uzlaşma ± %0,5 limitle** (C §2.1). Doğrulanan kenar t+1 kapanış girişine ait (v_bist #25, §2.5).
   - Sabah limiti ters seçim yaratır: dönüş hemen gelirse emir dolmaz, devam ederse dolar.
   - 17:50 bacak kontrolü gün içi ekran ister.
   - Düzeltme: iki bacak t+1 kapanış penceresinde.
2. **K2 (KCHOL↔sepet) "kalıcı" sinyalle, 11.11'de, MSCI'dan bir gece önce açılıyor.** C'nin kendi ölçümüne göre kalıcı sinyallerin kanıtı karışık: 2010–18'de −53 bps (n=35). Yeni bir kesişim beklenmeli. Beklentisi +0,15 puan; kaybı küçük, ama bu kol çıkarılabilir.
3. **Profil uyumu düşük.** AÇIK rejimde K4 riski en çok %0,5 ve piramit yok. Rejim dönerse sağ kuyruk A'ya göre yarı boyda yakalanır.
4. **K4'te test edilmemiş filtre.** "Son 6 kümede giriş yok" kuralı A'nın [EK-3] bulgusuyla çelişiyor: alt yarı kümelerden gelen kırılımlar +%5,3, ilk 3'ten gelenler +%4,9. Bu bulgu örneklem içi ve doğrulanmamış. Filtre işlem sayısını, değer katmadan azaltabilir.
5. **Mevduat merdiveni aynı haftaya yığılmış.** §1.3 "haftada bir dilim" diyor, §3.2 dört dilimi Pzt/Sal/Per/Cum'a koyuyor. Değere etkisi küçük; likidite takvimi bozuluyor.

---

## 5. Doğrulanmış gerçeklerle (ve yeni dosyayla) çelişkiler

| # | Taslak | İddia / kural | Doğrusu | Kaynak |
|---|---|---|---|---|
| 1 | A | XU030 taşıma "mevduattan ~8 puan düşük"; vadeli avantajı "8–13 puan" | Basitte 3,3; bileşikte ~5,7. Vadeli avantajı mevduata göre ~3,5–7,5, PPF'e göre ~0 | v_profesyonel T12; v_capraz #4; C §1.2 |
| 2 | A | S1 katkısı +5…+15 (brüt × brüt) | Kullanılan nakdin engel getirisi düşülmeli; ≈ +1…+10 | A §8.1; v_bist §2.1 (engel düzeltmesi) |
| 3 | A | TSMOM12 eşiğinde nakit ~%45 → ~15.800 | Test edilen kural ajanın rf serisini (%37,3) kullanıyordu → ~15.000. Karar değişmiyor; ama bu test dışı bir varyant | v_bist #23; bist_test §2 |
| 4 | A | t+1 girişinin dayanağı olarak v_bist #24 gösterilmiş | #24 zirveye yakınlık sıralamasıyla ilgili. Doğru dayanak bist_test'in t+1 kapanışı (v_bist §2.5 "doğru") | v_bist #24, §2.5 |
| 5 | B | Brüt rezerv < 160 → SARI; carry açılır | Komite: brüt rezerv < 160 → **çık**. Değer 158,1 | komite §4.2; v_capraz #18 |
| 6 | B | O3 limiti = uzlaşma toplamı (≤320) | İşlemler ~199 puandan. Uzlaşmadan alımda beklenen değer ~0 | viop_20261105.csv; komite §4.1 |
| 7 | B (A, C) | Aylık TÜFE < %2,0, tek ay | Kaynak: 2 ay üst üste | tr_makro §5.1 |
| 8 | B | Bedelsiz: SPK onayından hak kullanımına kadar long | Test edilen pencere hak kullanımına göre [−20,−1]; onay sonrası literatürde negatif | bist_swing §5.1 |
| 9 | B | Temettü girişi gün −5 kapanışı | [−5,−1] için giriş gün −6 kapanışı | bist_swing §5.3; C §2.3 |
| 10 | A, B | Banka bloğu rejim dönüşünün ilk aracı; 10.12'yi kapsayan banka long'u | Döngü içi indirimden sonra 63 günde XBANK/XU100 −%6,6, 6/6 döngü negatif; bankalar 63 günde +%26 ön koşu yaptı. Fonlama (AOFM) gevşemesi daha iyi banka tetiği (21g +%3,4, isabet %75) | olay_akis_rejim §4.1–4.5 (**doğrulanmamış**) |
| 11 | A, B, C | Yabancı hisse alımı (M3/L3) rejim tetiği | Akım getiriyi izliyor (aynı hafta t 10,7). İleri getiri 2021–26 ve 2024–26'da anlamsız. Tetik daha geç gelir, daha isabetli değil | olay_akis_rejim §0, §3 (**doğrulanmamış**) |
| 12 | C | Çift girişi 09:30, uzlaşma ± %0,5 | Doğrulanan gecikme t+1 kapanışı | v_bist #25, §2.5 |
| 13 | C | K4'te son 6 kümeden giriş yok | A [EK-3]: küme sırası kırılım getirisini ayırmıyor (örneklem içi) | A §2.2 |
| 14 | Bağlam | İçeriden alım taklidi yılda ~%6,6 anormal (literatür) | Kendi KAP verisi: kontrol düzeltmeli 60 günde −%3,35 (t −1,7, n=233). C doğru şekilde dışarıda bırakmış | v_bist #18; olay_akis_rejim §2.3 |

**Üçünün de doğru yaptıkları:**
- XU030 ima oranı %29,3; %23,3 yanlıştı.
- Nakit-taşıma bugün yapılmaz.
- DİBS yalnız %0 stopajın yazılı teyidiyle alınır.
- Kredili spot yok.
- Overhang hisseleri ve SPK'nın suç duyurusunda bulunduğu 13 hisse dışlanıyor.
- AKCNS'de işlem yok. C'nin "halka açık piyasa değeri 24.09–07.10 arasında 8,1 mlr TL'den 2,2 mlr TL'ye düştü" gözlemi teklifin büyük olasılıkla zaten uygulandığını gösteriyor.
- Kasım pay vadelisi 25–26.11'e kadar kapatılır ya da devredilir.

---

## 6. Aşılanacak en iyi fikirler (değer etkisi sırasıyla)

| # | Fikir (kaynak taslak) | Kanıt | Değer etkisi (12 ay, hesap puanı) |
|---|---|---|---|
| 1 | **Engel muhasebesi her kol için zorunlu.** Fazla K/Z = K/Z − bağlanan nakit × engel × gün/365. Vadelide bağlanan nakit = faiz kazanmayan teminat. Öldürme ve ölçekleme kuralları buna (R_fazla) bağlanır (B §6.4, Ek A; C §1.3 m.3) | v_bist §2.1 (engel 2–8 puan düşük ölçülmüştü) | Doğrudan getiri değil, kaybeden kolu erken kapatma: −1…−3 puanlık sessiz kanamayı önler |
| 2 | **Çekirdekte mevduat ağırlığı ≥%55–60, haftalık 4 dilim** (9/16/23/30.11); PPF yalnız banka iştiraki ve likidite tamponu (A §1.3) | v_capraz #4 (mevduat net ~%37,9 bileşik, PPF ~%34–35); v_bist §3 m.3 | C'ye göre **+0,3…+0,5**, risksiz |
| 3 | **Temettü öncesi 5 gün (spot)** (C §2.3). Giriş gün −6, çıkış gün −1 kapanış seansında limitli emirle. Boyut olay başına %5 (B'nin %7'si ile C'nin %3,5'i arası), aynı anda en çok 3 olay. ≥5 mn TL hesapta β × nominal F_XU030 short ile piyasa riski atılır | v_bist #26 (t 6,5; maliyet sonrası ~%0,9) | **+0,4…+1,0** (sezon Mart–Haziran) |
| 4 | **SAHOL↔AKBNK 20 günlük çift, t+1 kapanış girişi** (C §2.1; giriş C'nin 09:30'u değil, kapanış). Bacak başına %7,5. Komisyon yön başına >15 bps veya teminat faizsizse kapalı. Eski 1–3 günlük sürüm emekli edilir | v_bist #25 (gecikmeli +160/+310 bps, t 2,4/2,8) | **+0,2…+0,5**; teminat faizsizse ~0 |
| 5 | **A1 kırılım motoru ve bekleme listesi** (A §2.1, §4.4). KAPALI'da en çok 2 sonda × %0,25 risk; GEÇİŞ'te %0,5; AÇIK'ta %0,75–1. Brüt sınır C'nin stres tavanıyla bağlanır (AÇIK'ta stres ≤ %10). Piramit yalnız AÇIK'ta ve kayıtlı ayrı satırla | bist_test §5.1 (S5 +%5,7, t 5,4); v_bist #28 (kârın %70'i pump; dışlama listesi şart) | KAPALI'da ~0. Rejim dönerse **+3…+8**, sağ kuyruklu |
| 6 | **Vadeli finansman kuralı, doğru kıyasla** (A §2.1.3, B §1.2). Long için pay vadelisi yalnız iki koşulda kullanılır: (çekirdek net basit oran − ima basit taşıma) ≥ 3 puan ve teminat faizli. Kasım vadesi kullanılmaz ya da 25.11'de devredilir | v_profesyonel T12; 5.11 bülteni (banka ima %25–28) | Kullanılan nominal üzerinde yılda +3…+7 puan; hesapta +0…+1 (yalnız AÇIK'ta) |
| 7 | **XU030 nakit-taşıma açma kuralı** (B §1.5). İki koşul: ima ≥ (32 gün mevduat brüt × 0,825) + 3 puan ve teminat faizli. Vergisiz carry kanalı; bugün kapalı | v_capraz §2 m.1; v_profesyonel T12 | Açıldığı haftalarda mevduat üstü +1…+3 puan; yıllık +0…+0,3 |
| 8 | **Carry = 0 Pazartesi.** Yeniden açılış için komitenin bütün çıkış koşulları temizlenmeli: brüt rezerv ≥160, swap hariç net rezervde 2 hafta düşüş yok, yabancı DİBS akımı > −250 mn $, kur hızı < %30. Boyut ≤0,10x ve banka long'uyla ortak stres ≤%10 (B §5 formülü) | komite §4.2; v_capraz #19, §2.8; tr_makro §4.3 | Beklentiden −0,1…−0,3 puan vazgeçilir; S3/S4 kuyruğundan −2,5…−3,5 puan çıkarılır |
| 9 | **Banka zamanlaması: 10.12 PPK'yı kapsayan banka aşırı ağırlığı yok.** Rejim dönüşünün ilk aracı F_XU030 (C K7, A A3a), bankalar değil. Banka eğimi yalnız şu durumlarda: AOFM gevşemesi, şahin sürpriz, sabit karar | olay_akis_rejim §4.1–4.6 (**doğrulanmamış; v_olay gelince teyit**) | S1'de bankanın endekse göre −%5…−%7'lik göreli geri kalmasından kaçınma; yükü küçük |
| 10 | **Halka arz katılımı (küçük hesaplar)** (B K5). Eşit dağıtımlı arzlar, teminat PPF; seri bozulunca ertesi açılışta satış. Seri sonrası alım yok | olay_halka_arz §0 (yılda 10–27 bin TL/hesap; seri sonrası 21 gün medyan −%11) | 1 mn TL'de **+1…+2,7**, 20 mn TL'de ~0. 3 Eylül'den beri onay yok (hazırlık §1a); şimdilik 0 |
| 11 | **ZPAT ve özel durum kuralı** (C §2.5, B K4'teki hak sahipliği okumasıyla). KAP'taki bilgi formunda iki şey okunmadan işlem yok: "kimler katılabilir" ve teklif penceresinin başlamış olması | v_bist §3 m.4; SPK 2026/58, 59, 71 (B ve C okudu) | 0…+0,5; asıl değeri yanlış "bedava para"dan korumak |

---

## 7. Birleşik planın beklenen dağılımı (C iskeleti + §6 aşıları; 12 ay, vergi ve maliyet sonrası)

| Senaryo (öznel, tr_makro §5.2) | Çekirdek net | Uydu + motor, engel üstü | Toplam net nominal TL |
|---|---|---|---|
| S1 sönümlenme (%35) | %30–33 | +3…+8 (kırılım ve endeks motoru açılırsa) | %34–40 |
| S2 yatay kanama (%40) | %33–36 | 0…+2,5 (temettü, çift, sonda) | %33–38 |
| S3 kontrollü kur hızlanması (%15) | %35–38 | −1…+1,5 | %34–39 |
| S4 kırılma (%10) | %38–45 nominal (USD bazında negatif) | −4…−1 | %35–43 nominal |
| **Ağırlıklı** | | **≈ +1,5…+2,5** (%80 aralık −2…+6) | **≈ %34–38** |

**Dağılımın özellikleri:**
- P(12 ayda engelin altında) ≈ %35–40.
- Engele göre en kötü %10'luk kuyruk −3…−5 puan; stres tavanıyla sınırlı.
- En iyi %10'luk kuyruk +8…+15 puan; S1 ile kırılımın sağ kuyruğu birlikte gelirse.
- Reel karşılık ~%3–8.
- İlk 12 ayda uydu kenarının sıfırdan istatistiksel olarak ayrışma olasılığı < %30 (C §8.3 m.4).

**TL karşılıkları (engel üstü merkez +1,5…+2,5; %80 aralık −2…+6):**

| Hesap | Merkez | %80 aralık | Halka arz eklentisi (pipeline açılırsa) |
|---|---|---|---|
| 1 mn TL | +15…+25 bin | −20…+60 bin | +10…+27 bin |
| 5 mn TL | +75…+125 bin | −100…+300 bin | aynı TL (yüzde olarak küçük) |
| 20 mn TL | +300…+500 bin | −0,4…+1,2 mn | aynı TL (~0 puan) |

---

## 8. "Yüksek getiri" sorusuna dürüst cevap

- **Bu rejimde kanıtın verdiği tavan, engel artı birkaç puandır.** Bu rejim: pozitif reel faiz %5–8, XU100 SMA200'ün %16,5 altında, genişlik %13.
  - 2024–26'da 456 küme kuralının hiçbiri nakdi geçmedi (v_dalga B2).
  - Kırılım portföyü düzeltilmiş engelin 2–8 puan altında kaldı (v_bist §2.1).
  - 3 yılda hisse fonlarının neredeyse hiçbiri PPF'yi geçmedi (v_bist §3 m.2).
- **Yüksek getirinin tek gerçekçi yolu, rejim dönüşünü kırılım ve endeks motoruyla yakalamak.** Bunun için motorun bugünden kurulmuş, tetikleri yazılmış ve ölçülüyor olması gerekir. A'nın uzun vade tahmini: rejim normale dönerse yılda +4…+8 puan, hesap düzeyinde −%10…−%20 düşüşle. 2017/2020/2022 tipi bir yılda hesap +%40…+100 yapabilir, ama bu planlanamaz (A §8.2).
- **Bugün +10–20 puan hedeflemenin bedeli:** 3–5 kat risk ve engele göre −%25…−%40 düşüş toleransı, sağ kuyruğa bağımlılıkla birlikte (C §8.3 m.3; seytan §5.1). Kanıt bunu bu rejimde desteklemiyor. Bunu öneren bir plan değer testini geçemez.

---

## 9. Teyit edilmeden kullanılmayacaklar

- VİOP teminatının faizi, PPF/DİBS'in teminat olarak kabulü ve kurumun kendi teminat oranları. Cevap gelmeden çift, carry ve vadeli finansman kolları açılmaz.
- DİBS'te %0 stopaj (GİB metni 30.06.2026'ya kadarki alımları sayıyor; v_capraz #8).
- `olay_akis_rejim` bulguları (banka/PPK zamanlaması, yabancı akımı). `v_olay.md` gelince yeniden değerlendirilmeli.
- Bedelsiz koşusu (`olay_bedelsiz.md` ve `v_olay.md` yok). C'deki gibi kâğıt üzerinde kalmalı.
- Opsiyon dolumları: yalnız işlem fiyatlarına yakın limitle (strangle ~≤230 puan). Uzlaşmadan alınmaz.
- 2027 stopaj takvimi: %17,5 oranı 31.12.2026'da sona eriyor. Çekirdek Aralık'ın son haftasında yeniden seçilir.
