# Hakem raporu (KANIT merceği): BIST/VİOP taslakları A, B, C

- **Tarih:** Cuma 06.11.2026, ~14:00 TSİ. Plan başlangıcı Pazartesi 09.11.2026.
- **Mercek:** Kanıta sadakat ve istatistiksel dürüstlük. Sorular şunlar: Her kural doğrulanmış bir bulgudan çıkıyor mu? Düzeltilmiş risksiz faiz serisi (v_bist §2.1) ve 1 gün gecikmeli giriş sonuçları (v_bist #25) kullanılıyor mu? Beklenen aralıklar destekleniyor mu?
- **Okunan dosyalar:** üç taslak (bist_A, bist_B, bist_C); doğrulama dosyaları v_bist, v_capraz, v_dalga, v_profesyonel; ajan raporları bist_test §0–7, bist_swing §5, olay_halka_arz §0, olay_akis_rejim §0–4 (bu dosya A ve B yazıldıktan sonra geldi; doğrulaması yok). `olay_bedelsiz.md` ve `v_olay.md` hâlâ yok.
- **Kendi kontrollerim** (scratchpad'de; repoya yazılmadı):
  - `hakem_iv.py`: 05.11 resmi bülteninden XU030 Aralık opsiyonlarının Black-76 zımni oynaklığı.
  - `hakem_r.py`: `t03_islemler_S2_iz15*.csv` işlemlerinde engele göre R hesabı.
  - A'nın `an2.py` portföy simülasyonunu yeniden koşturdum.
  - Yollar: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/hakem_iv.py`, `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/hakem_r.py`.

---

## 1. Puan tablosu (0–10)

| Kriter | A (kırılım/RS lideri) | B (rejim + carry + olay) | C (kanıt minimalisti) |
|---|---|---|---|
| Kanıta sadakat | 7 | 5,5 | **8,5** |
| Pazartesi uygulanabilirliği (gün içi ekran yok, VİOP teminatı, emir tipi, likidite, limit kilidi) | 7 | 5,5 | **7,5** |
| Risk kontrolü ve en kötü durum | 8 | 6,5 | **8,5** |
| Vergi sonrası TL engeline göre beklenen değerin gerçekçiliği | 5,5 | 5,5 | **8,5** |
| Kullanıcı profiline uyum (swing, yüksek getiri, kümeler) | **8** | 7 | 5 |
| **Toplam (50 üzerinden)** | **35,5** | **30** | **38** |

**Kazanan: C.** C ana gövde olarak alınmalı. A'nın rejim merdiveni ve kırılım makinesi, rejim GEÇİŞ veya AÇIK'a döndüğünde devreye girecek tek "yüksek getiri" kolu olarak C'ye eklenmeli. B'den yalnız ölçüm, kapı ve kaçınma kuralları alınmalı (§5).

---

## 2. Üç taslağın ortak doğruları (doğrulanmış gerçeklerle uyumlu)

- **XU030 vadeli fiyatı:** Üçü de tarama dosyasındaki yanlış %23,3'ü düzeltti ve resmi uzlaşmayı kullandı: 14.734 / 14.101 → %29,3 (v_profesyonel T12). Bülten satırlarını kendim okudum, rakamlar doğru.
- **Bugünkü rejim:** Üçü de "KAPALI" diyor ve bugün yönlü hisse/endeks long'u açmıyor. Doğrulanmış kanıtla uyumlu:
  - 2024–26'da 456 küme kuralının hiçbiri rf'yi geçmedi (v_dalga B2).
  - Kırılım portföyü düzeltilmiş rf ile engelin 2–8 puan altında (v_bist §2.1).
- **Çekirdek:** Üçünde de çekirdek yalnız banka iştiraki PPF ve mevduattan oluşuyor; tasfiyedeki PPF'ler dışarıda (v_bist §3.3). DİBS yalnız %0 stopaj yazılı teyit edilirse alınıyor (v_capraz #8).
- **Dışlanan yöntemler:** Kesitsel momentum, kısa vadeli dönüş, endeks SMA kuralları, tavan serisi sonrası halka arz alımı ve kredili spot hiçbirinde yok (bist_test §4, §2; v_bist #3, #11).
- **Dışlama listesi:** 13 SPK suç duyurulu hisse ve fon payı / fiili dolaşım oranı %20'yi aşan hisseler üçünde de var (v_profesyonel T6, T10).
- **AKCNS:** Hiçbiri işlem yapmıyor. SPK 2026/59 metnini okudum: 260,25 TL ile 5,627434 $'ın TL karşılığından yüksek olanı geçerli. Hisse 5.11'de 184,5 TL. C'nin gözlemi, halka açık piyasa değerinin 24.09–07.10 arasında 8,1 mlr TL'den 2,2 mlr TL'ye düşmesi; bu, teklifin büyük olasılıkla uygulanıp kapandığını gösteriyor.

---

## 3. Taslak bazında bulgular

### 3.1 Taslak A: "Trend/RS lideri + küme"

**Güçlü yanlar**
- **Kendi yan analizleri yeniden üretilebiliyor.** `an2.py`'yi koşturdum. VİOP-47 alt kümesi, 6 slot, boş nakit vergi sonrası:
  - 2010–26: %32,6
  - 2016–26: %44,4
  - 2024–26: %44,3; vergi sonrası engel %43,1
  - MaxDD: −%28 (gerçekçi dolumda −%34)

  Rakamlar birebir tuttu. Simülasyonda risksiz faiz günlük bileşik ve vergi sonrası; v_bist §2.1 düzeltmesine uygun.
- **EK-3, kanıtı daraltan dürüst bir bulgu.** Sinyal günü 12 ay RS sıralamasında ilk 3'teki kümelerden gelen kırılımlar +%4,9, alt yarıdakiler +%5,3 fark verdi. A bu yüzden küme sıralamasını giriş filtresi yapmıyor, yalnız öncelik ve yoğunlaşma sınırı olarak kullanıyor. Bu, v_dalga §5-1 hükmüyle tutarlı (küme kuralı bir getiri motoru değil, filtre).
- **Kesin tetik seviyeleri:** ENJSA 127,00; AHGAZ 48,70; ENERY 14,60; XU100 SMA50 12.691 ve SMA200 13.572. C ile aynı değerleri buluyor. "ENERJİ_DAĞITIM tek küme" ihtiyatı doğru.
- **Piramit algebrası doğru.** Giriş 1,0 ve ekleme 1,10'da yapılırsa stopta toplam kayıp 0,1475 olur; bu, ilk riskin (0,15) altında.

**Ciddi kusurlar**
1. **Öldürme ve ölçekleme testleri mutlak R ile tanımlanmış, engele göre değil (en önemli kusur).**
   - İlgili kurallar: §7.4 ve §7.5 K1–K3; ölçekleme şartı "ortalama R ≥ +0,30", öldürme şartı "100 işlemde ortalama R ≤ 0", SPRT için H1 = +0,4R.
   - Bugünkü faizle (~%36) ve ~45 işlem günlük (~63 takvim günü) tutmada işlem başına engel ≈ %5,6–6,2. %15 stopla bu ≈ **0,37–0,41R** eder.
   - A'nın hipotez kartındaki beklenti (+%4…+%8 = +0,3…+0,5R, mutlak) engele çevrilince ≈ **−0,13…+0,16R**, yani sıfır civarı.
   - Kendi hesabım (`hakem_r.py`), VİOP-47 kırılımları, giriş 2024 ve sonrası, n=56:
     - Ortalama net: +%4,15 (+0,28R, mutlak)
     - Aynı tutmadaki rf (ajanın düşük serisi bile): %7,41
     - Fark: **−%3,3/işlem (−0,22R)**
   - Düzeltilmiş rf ile fark daha da kötü. A'nın K3 kuralı engeli kaybeden bu kolu kapatmazdı.
   - Not: Tüm örneklemde engele göre R yaklaşık +0,56. Kenar vardı, ama bugünkü faizde değil.
2. **12 aylık beklenen değer (+2 puan; %80 aralık −4…+12) kendi işlem kartıyla çelişiyor.**
   - İşlem başına engel fazlası ≈ 0 iken hesap düzeyinde +2 puan ancak S1 senaryosunda büyük hareketlerle mümkün. S1'e +5…+15 puan yazılmış; bu, öznel %35 olasılığa ve rejimin 1–3 ay içinde GEÇİŞ, sonra AÇIK'a dönmesine bağlı.
   - AÇIK için XU100'ün +%19,8 yükselmesi gerekiyor. GEÇİŞ için 5 makro tetikten ≥3'ü gerekiyor ve bu kural test edilmemiş.
   - Daha savunulabilir merkez +0…+2 puan.
3. **Uzun vadeli +4…+8 puan/yıl iddiası bugünkü VİOP-47 listesine dayanıyor.** Bu liste ileriye bakma ve hayatta kalma yanlılığı taşıyor. A bunu kabul edip %30–50 iskonto uyguluyor. Ancak doğrulanmış taban (36 varyant medyanı %34,8; 2024–26'da engelin 2–8 puan altı; en iyi %5 işlem kârın %70'i ve bunların bir kısmı pump hisseleri) ana çerçeve olmalı, alt küme iyimser sınır.
4. **Vadeli avantajı abartılmış.** §2.1.3'teki "mevduattaysa ~8–13 puan" iddiası bileşik mevduat getirisini (%37,9) basit ima taşıma oranıyla (%25–29) karşılaştırıyor. Basitle basit karşılaştırınca (%32,6'ya karşı %25–29) avantaj **~4–8 puan**. B'nin 5–8 puanı doğru.
5. **Küçük tutarsızlık:** "12 ay nakit ~%45" ve TSMOM eşiği ~15.800. Sabit veri bu oranı %37 veriyor, eşik ~15.000 eder.
   - A, v_bist'in brüt PPF medyanını (%45,5) kullanıyor; bu savunulabilir.
   - Ancak iki eşik birlikte yazılmalı. Bugünkü kararı değiştirmiyor.

**Ölümcül mü?** Pazartesi için hayır. KAPALI rejimde en fazla 2 pilot var, toplam risk ≤%0,5. Ölçekleme mantığı için evet: düzeltilmeden r₀ büyütülmemeli.

### 3.2 Taslak B: "Rejim + carry + zorunlu akış"

**Güçlü yanlar**
- **Birincil veri işçiliği:**
  - Opsiyon değerlerini kendim yeniden hesapladım: Black-76 ile σ %20'de strangle 315 puan. Uzlaşmaların zımni oynaklığı P14000 %19,0, C15500 %20,7, C15000 %21,0, P13250 %23,1. B'nin rakamları tutuyor.
  - Çarpanlar doğru: XU030 opsiyon 1 puan = 10 TL; F_XLBNK = 10 × endeks.
  - Banka pay vadelilerinin ima taşıma oranı %25–28 doğru.
- **SPK metinleri:**
  - PEKGY kararlarındaki ifade (SPK 2026/58): teklif "iktisabın kamuya açıklandığı tarihte pay sahibi olan diğer ortaklara" yapılıyor. Metinde birebir var.
  - AKCNS metni ise bu tarih kaydını içermiyor. Yani B'nin "Türk uygulamasında genel kural" diye genellemesi kısmen destekli. Yine de zorunlu pay alım teklifinde (ZPAT) hak sahipliği kontrolünü plana sokması değerli.
- **Ölçüm muhasebesi en iyi B'de.** Kural 0: teminat faiz kazanmıyorsa VİOP yok. Fazla K/Z şöyle tanımlı: K/Z − bağlanan nakit × engel × gün/365. Öldürme kuralları (K4, K5) "engele göre fazla ≤ 0" üzerinden.
- **Ortak stres formülü:** Carry ile banka bloğunun aynı kuyruğu paylaştığını sayısallaştırıyor (v_capraz eksik 8).

**Ciddi kusurlar**
1. **K2'nin "önce bankalar" önermesi en yeni kanıtla çelişiyor.**
   - olay_akis_rejim §4.2 ve §4.5'e göre (doğrulanmamış):
     - İndirim döngülerinde bankalar karardan sonraki 63 günde XU100'ün gerisinde kaldı: 6/6 döngü, t −4,2.
     - Sürprizsiz döngü içi indirimlerde (n=24) 63 günlük fark −%6,6.
     - Bankalar zaten 63 günde XU100'e karşı +%26 koştu.
     - Hüküm: "Bugün yeni banka-uzun pozisyonu için destek yok."
   - B'nin en erken TAM girişi 3.12; bu da 10.12 PPK'dan (beklenen −100 bp) bir hafta önceye denk geliyor.
   - K2'nin kendi kanıtı n=4 rejim kırılması. Planın yüksek getiri bacağı en zayıf kanıtlı ve şimdi aleyhte veri olan bacak.
2. **Doğrulanmamış ya da test edilmemiş kanıta dayalı canlı kollar var.**
   - **Bedelsiz öncesi (K5, olay başına ≤%5 sermaye):**
     - Doğrulama raporu (v_olay) ve `olay_bedelsiz` raporu yok.
     - Likit üst yarıda [−5,−1] penceresi +%0,9, t 1,5, anlamsız.
     - Giriş SPK onayının ertesi günü. bist_swing §5.1'deki (doğrulanmamış) literatür onaydan sonraki 2., 3. ve 5. günlerde negatif KAAR buluyor.
   - **O3 strangle:**
     - BIST'te oynaklık primi test edilmedi (v_bist §3.6).
     - ABD'de opsiyon alıcısının ortalaması negatif (v_profesyonel A6).
     - %32'lik gerçekleşen oynaklık kriz döneminin 20 günlük geriye dönük değeri.
     - Boyutu küçük (%0,3), ama "pozitif beklenti" iddiası kanıtsız.
3. **Pazartesi negatif çarpık carry açılıyor (0,05x, 12.11'de 0,10x).**
   - Ortam: swap hariç net rezerv bir haftada −6,5 mlr $; yabancı DİBS satışı Nisan'dan beri en büyük; B'nin kendi göstergesinde 3 SARI.
   - 07/2023 sonrası Sharpe örneklem içi (v_bist §2.6).
   - B'nin kendi prim tahmini 5–8 puan. Beklenti +0,4…+0,8 puan, kuyruk −2,5…−3,5 puan.
   - SARI/YEŞİL eşikleri test edilmedi.
   - Gerekçe zayıf ama küçük. C'nin kapısı (rezerv ve DİBS akımı) burada daha tutarlı.
4. **Temettü penceresi bir gün kaymış.** "Hak kullanımından 5 işlem günü önce kapanışta al" kuralı yalnız [−4,−1]'i yakalıyor. Test penceresi [−5,−1] için alışın gün −6 kapanışında yapılması gerekir; C bunu doğru yapıyor.
   - Engelin düşülmesi: B, piyasaya göre düzeltilmiş bir anormal getiriden 5 günlük engeli de düşüyor. Bu ihtiyatlı (piyasanın beklenen getirisini sıfır sayıyor); hata değil.
5. **Uygulanabilirlik yükü ağır.**
   - 7 + 8 gösterge izleniyor, her gün 17:40–18:08 penceresi var, opsiyon bacakları ayrı ayrı giriliyor.
   - Opsiyonlarda kapanış ile uzlaşma arasında büyük fark var: C15500 uzlaşması 174, kapanışı 98,6.
   - Aracı kurumdan yazılı cevap Pazartesi 10:00'dan önce bekleniyor; bu gerçekçi değil, ama B'nin geri dönüş kuralı var.
6. **12 aylık p90'ın +12…+16 puan olması** n=4'lük banka kanıtına ve zamanında tetiğe dayanıyor. Merkez 0…+4 makul.

**Ölümcül mü?** Pazartesi için risk küçük olduğundan hayır. Planın getiri tezi (K2) için evet: K2 bugünkü haliyle aşılanmamalı.

### 3.3 Taslak C: "Önce risk, kanıt minimalisti"

**Güçlü yanlar**
- **Her kol doğrulanmış ve gecikmeli giriş rakamına bağlı.**
  - Çiftler (v_bist #25): SAHOL↔AKBNK 160/310 bps (t 2,4/2,8); KCHOL↔sepet 128/175 bps (t 2,1/2,1). Bunlara %40 çürüme ve seçim iskontosu uygulanıyor.
  - Temettü (v_bist #26): t 6,5; maliyet sonrası %0,9; %30 iskonto.
  - Kırılım (v_bist #28 ve §2.1): KAPALI'da yalnız sonda boyutu.
- **"Kullanılmayanlar" tablosu kanıt hiyerarşisini doğru uyguluyor.**
  - Bedelsiz yalnız kâğıt üzerinde, ama kaçınma kuralı canlı.
  - İçeriden alım kolu yok, çünkü literatür (+%6,6) ile yerel ara tablo (−%3,35, t −1,7) çelişiyor. olay_akis_rejim §2.3 bunu teyit ediyor.
  - Opsiyon satışı ve straddle yok.
- **Çekirdek hesabı en titiz C'de.** 56 günde XU030 nakit-taşıma %4,49, PPF net %4,54, mevduat %5,06. Yani "vadeli ~%1 ucuz" farkı brüttür; vergi sonrası birey için avantaj sayılmaz.
- **Beklenti dürüst.**
  - Merkez +1,5–2 puan, %80 aralık −2…+5.
  - 12 ayda kenarın sıfırdan ayrışma olasılığı <%30.
  - "+10–20 puan için 3–5 kat risk gerekir ve bu rejimde kanıt bunu desteklemiyor" ifadesi seytan §3.7 ve v_bist §2.1 ile tutarlı.
- **Komisyona bağlı kol kapatma eşikleri** (K1 > 15 bps, K2 > 8 bps) ve **eski 1–3 günlük SAHOL/AKBNK sinyalinin emekliye ayrılması** çift sayımı önlüyor.

**Kusurlar (ölümcül değil)**
1. **K2 girişi test edilen kural değil.** KCHOL↔sepet z = +2,23, ama sinyal 20.10'dan beri açık. v_bist sinyalin ilk kesişimini 1 gün gecikmeyle test etti. C'nin kendi hesabında "kalıcı" sinyaller 2010–18'de −53 bps (n=35), 2019–26'da +272 bps (n=26): karışık. 11.11 girişi yarım boy ve yalnız ≥5 mn TL hesap için. Yine de "ilk kesişim" kuralına bağlanmalı ya da kâğıt üzerinde kalmalı.
2. **K5'te ZPAT hak sahipliği kontrolü yok.** Teklif yalnız açıklama tarihindeki pay sahiplerine yapılıyorsa (SPK 2026/58'deki PEKGY ifadesi), sonradan alınan pay teklife verilemez ve işlem zararla biter. B'nin kontrolü buraya eklenmeli.
3. **Küçük tutarsızlıklar.**
   - TSMOM için §3.1'de "+%3,8 / ~%37", §2.7'de "+%3,3 / %37,3" yazıyor.
   - K1 girişi 09:30'da bırakılan GÜN emriyle yapılıyor, yani gün içinde doluyor. Test t+1 kapanışında giriş varsayıyordu. Etkisi küçük; günlüğe yazılmalı.
4. **Temettü kolu (K3):** Olay başına +%0,5…+%0,7 beklentisi beta riskini taşıyor. Hedge ancak ≈147 bin TL / β üstünde mümkün. Kasım–Aralık'ta olay yok denecek kadar az. Katkı merkezi +0,6 puan/yıl iyimser değil, ama ilk 6 ay ~0.
5. **Profil uyumu zayıf.** "Yüksek getiri" ve "kümeler" isteyen kullanıcıya bu rejimde ~+1,5 puan veriyor. Bu bilinçli ve dürüst bir seçim, ama rejim dönüşünde ne yapılacağı (K4 + K7) A kadar ayrıntılı değil.

---

## 4. Doğrulanmış gerçeklerle çelişkiler (özet liste)

| # | Taslak | İddia | Doğrulanmış gerçek / kendi kontrolüm | Ağırlık |
|---|---|---|---|---|
| 1 | A | Öldürme ve ölçekleme mutlak R ile | Bugünkü faizde işlem başı engel ≈ 0,37–0,41R. VİOP-47 kırılımları (2024+) rf'ye göre −0,22R (`hakem_r.py`); düzeltilmiş rf ile daha kötü (v_bist §2.1) | Yüksek |
| 2 | A | Vadeli avantajı 8–13 puan | Basit/basit karşılaştırmayla ~4–8 puan (bülten; v_profesyonel T12) | Orta |
| 3 | A | AÇIK rejimde E[R] +0,3…+0,5R → hesapta +2 puan | Engele çevrilince ≈ 0; +2 puan yalnız S1 varsayımından geliyor | Orta |
| 4 | B | K2: önce bankalar, 3.12 girişi 10.12 PPK'ya taşınıyor | İndirim sonrası bankalar 63 günde XU100'ün gerisinde (6/6 döngü, t −4,2); bankalar zaten +%26 koştu (olay_akis_rejim §4.2, §4.5; doğrulanmamış) | Yüksek |
| 5 | B | Bedelsiz öncesi canlı, giriş SPK onayında | Doğrulama yok; likit üst yarıda [−5,−1] t 1,5; literatürde onay sonrası negatif KAAR (bist_swing §5.1) | Orta |
| 6 | B | O3 "pozitif beklenti" | BIST'te test yok (v_bist §3.6); ABD'de opsiyon alıcıları kaybediyor (v_profesyonel A6) | Düşük (boyut %0,3) |
| 7 | B | Temettü alışı gün −5'te | Test penceresi [−5,−1], yani alış gün −6 kapanışında olmalı (bist_swing §5.3) | Düşük |
| 8 | B | Carry'de SARI rejimde 0,10x | Sharpe 2,2 örneklem içi (v_bist §2.6); prim daralıyor (v_capraz #19); rezerv verisi bozuluyor (v_capraz #18) | Orta |
| 9 | C | K2'de kalıcı sinyalle giriş | Test edilen kural ilk kesişim + 1 gün gecikme (v_bist #25) | Orta |
| 10 | C | ZPAT kuralında hak sahipliği yok | SPK 2026/58'de "açıklandığı tarihte pay sahibi olanlar" ifadesi | Orta |
| 11 | Hepsi | Yabancı net alımı (≥ +200 mn $) rejim tetiği | Yabancı akımı getiriyi izliyor; ileri getiri 2021–26'da anlamsız; "ticari kenar yok" (olay_akis_rejim §3; doğrulanmamış) | Orta: tetik yalnız teyit göstergesi olmalı |
| 12 | Hepsi | Makro tetik eşikleri (rezerv, TÜFE < %2, CDS < 230) | n=4 tarihsel örnekten türetilmiş, öznel (tr_makro §5.3). Üçü de "test edilmedi" diyor; dürüst | Bilgi |

---

## 5. Aşılanacak en iyi 10 fikir (öncelik sırasıyla)

1. **Engele göre fazla getiri birimi (B §6.4, Ek A).**
   - Tanım: fazla = K/Z − bağlanan nakit × engel × gün/365.
   - Her öldürme ve ölçekleme testi bu birimle yapılır. A'nın R testleri de "R_fazla = (net − aynı tutmada çekirdek getirisi) / risk" olarak yeniden yazılır.
   - Kırılım için ölçekleme eşiği R_fazla ≥ +0,15 ve t ≥ 1,5 olur. Öldürme: 100 işlemde R_fazla ≤ 0.
2. **A'nın rejim merdiveni ve tetik tablosu (A §3.1–3.2, §4.4).**
   - Eşikler: KAPALI/GEÇİŞ/AÇIK için XU100 12.691 (SMA50) / 13.572 (SMA200) ve TSMOM12. İşlem başı risk (r₀) %0,25 / 0,5 / 1,0.
   - Tetikler (kapanış >): ENJSA 127,00; AHGAZ 48,70; ENERY 14,60.
   - Kural: ENERJİ_DAĞITIM tek küme; KAPALI'da en çok 1 pozisyon.
   - Bu, C'nin K4 ve K7 kollarının yerine geçer. Kanıt: bist_test §5.1 S5 (+%5,7, t 5,4) ve §6 (bu bir risk kontrolü, getiri kaynağı değil).
3. **Küme RS'si giriş filtresi değil (A EK-3; v_dalga §5-1).** Kümeler yalnız sinyal önceliği ve yoğunlaşma sınırı için kullanılır. Sınırlar: küme başına 2, Blok 1 (banka + holding + havacılık) için 3 pozisyon. Gerekçe: korelasyon 0,77–0,79 (v_dalga B12).
4. **Kural 0 ve aracı kurum kapısı (B §1.3; C §6.3).** Teminat faizsizse ya da PPF/DİBS teminat olarak kabul edilmiyorsa VİOP kolu açılmaz. Gerekçe: boştaki teminatın maliyeti teminat × ~%33 (v_capraz eksik 2). Yazılı cevap gelmeden hiçbir VİOP kolu açılmaz.
5. **Resmi bültene dayalı taşıma kuralları (B §1.5, Ek A; C §1.2).**
   - Her akşam `viop_YYYYMMDD.csv` indirilir ve i = (F/S − 1) × 365/gün hesaplanır.
   - XU030 nakit-taşıma ancak i ≥ net mevduat (basit) + 3 puan ise açılır.
   - Long maruziyet, i ≤ net mevduat (basit) − 3 puan ise vadeliyle kurulur. Karşılaştırma basitle basit yapılır (A'nın bileşik/basit hatası düzeltilir).
6. **C'nin SAHOL↔AKBNK kolu (C §2.1).**
   - Kurallar: |z| ≥ 2, giriş t+1, 20 gün tutma, bacak başına %7,5, felaket stopu −%8.
   - Beklenti işlem başına +80…+180 bps. Komisyon yön başına > 15 bps ise kol kapalı.
   - Eski 1–3 günlük sürüm emekliye ayrılır.
   - Rejimden bağımsız tek doğrulanmış kenar bu.
7. **Ortak stres bütçesi (B §5; C §5).**
   - Stres = 0,20 × Blok 1 nominali + 0,30 × carry nominali − put spread'in azami ödemesi + 2 taban senaryosu.
   - Sınır: KAPALI ≤ %6, AÇIK ≤ %10. Her Cuma hesaplanır.
8. **Takvim kaçınma kuralları (A §3.3; B §2-K4; C §3.2).** Hepsinde ortak; zorunlu akış alfası değil, kayıptan kaçınma.
   - 9.11 akşamı bilanço açıklayacak isimlerde yeni pozisyon yok.
   - MSCI'dan çıkarılan veya ağırlığı azaltılan hisseler 30.11 kapanışına kadar alınmaz.
   - Kredili işlem esnekliği 13.11'de uzatılmazsa 16–27.11 arasında BIST30/VİOP-47 dışında long yok ve "dipten alım" yok.
   - Kasım pay vadelileri en geç 25–26.11 kapanışında devredilir.
   - **Yeni kural:** Banka aşırı ağırlığı 10.12 PPK'nın ötesine taşınmaz; sürprizsiz indirimden sonra 63 gün banka-uzun yok (olay_akis_rejim §4.5; doğrulanmamış, ihtiyat kuralı olarak).
9. **ZPAT hak sahipliği kontrolü (B §2-K4) C'nin K5 kontrol listesine eklenir.** Bilgi formunda "kimler katılabilir" ve kayıt tarihi okunmadan, ayrıca açıklamadan sonra alınan payın teklife verilebileceği yazılı teyit edilmeden işlem yok.
10. **Doğru temettü takvimi (C §2.3) ve beta hedge'i.** Alış gün −6 kapanış seansında (limit = gün −7 kapanışı × 1,04); satış gün −1. ≥ 5 mn TL hesapta β × nominal kadar F_XU030 short açılır.

Eklenmemesi gerekenler (bugünkü kanıtla):
- B'nin K2'si (önce bankalar) ve O3 strangle'ı.
- B'nin canlı bedelsiz kolu (v_olay gelene kadar kâğıt üzerinde).
- B'nin Pazartesi carry'si: C'nin rezerv/DİBS kapısı açılana kadar 0.

---

## 6. Kazanan ve gerekçe

**Kazanan: C** (38/50). A ikinci (35,5), B üçüncü (30).

- **C neden kazandı:** Kanıt hiyerarşisini en tutarlı uygulayan taslak. Her canlı kural doğrulanmış ve gecikmeli giriş rakamına dayanıyor. Doğrulanmamış her şey kâğıt üzerinde. Beklenen değer engele göre ve dürüst: +1,5–2 puan, %80 aralık −2…+5.
- **C'nin zayıflığı kanıt değil, profil uyumu.** Bunu A'nın rejim merdiveni ve kırılım makinesi kapatır. Rejim GEÇİŞ veya AÇIK olduğunda A'nın boyutlandırması (r₀ 0,5 / 1,0, brüt sınır %60, iki taban stresi ≈ −%11) devreye girer, ama ölçüm birimi engele göre fazla R olmak şartıyla.
- **A neden ikinci:** Profil uyumu en iyi, analiz işçiliği yeniden üretilebilir. Ama ölçüm birimi hatası, düzeltilmezse engeli kaybeden bir kolun büyütülmesine izin verir.
- **B neden üçüncü:** Veri işçiliği güçlü. Ancak yüksek getiri bacağı (K2) n=4'lük kanıta dayanıyor ve olay_akis_rejim ile çelişiyor. Bedelsiz ve opsiyon kolları canlı olmasına rağmen doğrulanmış değil.

**Birleşik planın dürüst beklentisi (12 ay, vergi sonrası, engele göre):**
- **KAPALI süresince:** +1…+2 puan; %80 aralık −2…+4; engelin altında kalma olasılığı ~%35–45.
- **S1 (rejim dönüşü) gelirse:** A'nın kırılım kolu üstüne +3…+10 puan. Bu aralık öznel %35 olasılığa ve zamanında tetiğe bağlı; kârın >%50'si birkaç işlemden gelir.
- **Toplam hesap:** net nominal TL ~%32–40, reel ~%3–9.
- **"Yüksek getiri":** Bu rejimde kanıtla desteklenmiyor. Ancak rejim dönerse ve sağ kuyruktan birkaç işlem yakalanırsa gelir.
