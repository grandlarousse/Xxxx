# Hakem raporu (uygulama lensi): BIST/VİOP taslakları A, B, C

- **Tarih:** Cuma 06.11.2026, ~14:00 TSİ. Değerlendirilen plan Pazartesi 09.11.2026'da başlıyor.
- **Lens:** Bu kullanıcı için Pazartesi uygulanabilirlik ve risk. Ölçütler: VİOP teminatı ve kaldıraç, kapanış ve şartlı emirler, likidite, limit kilidi ve gap, arz baskılı (overhang) isimler, en kötü hafta (12.11 MSCI, 13.11 kredili işlem esnekliğinin bitişi, 16.11'den itibaren olası zorla satış).
- **Okunanlar:**
  - Üç taslak, tam metin.
  - Doğrulama dosyaları: `v_bist`, `v_capraz`, `v_profesyonel` (T5–T15, A6, eksikler).
  - `bist_hafta_hazirlik` §0–§5; komite raporu §1–§5; `bist_swing_kenarlar` §5.1 ve §5.3.
  - Yeni gelen `ajanlar/olay_akis_rejim.md` (11:23). Doğrulaması yok. `olay_bedelsiz.md` ve `v_olay.md` hâlâ yok.
- **Birincil veri kontrolü:** Resmî VİOP bülteni `viop_20261105.csv`. Kopyası `scratchpad/vcapraz/dl/` altında; dosyayı doğrulama ajanı varsayılan başlıklarla indirmişti, bu rapor için yalnız ayrıştırıldı.
- Yatırım tavsiyesi değildir.

---

## 1. Puan tablosu (0–10)

| Ölçüt | A (kırılım + küme + rejim) | B (rejim + carry + opsiyon + zorunlu akış) | C (önce risk, kanıt minimalisti) |
|---|---|---|---|
| Kanıta sadakat | 7 | 5 | 8 |
| Pazartesi uygulanabilirlik (gün içi ekran yok, VİOP teminatı, emir tipleri, likidite, limit kilidi) | 8 | 5 | 7 |
| Risk kontrolü ve en kötü hafta | 8 | 6 | 9 |
| Vergi sonrası TL engeline göre beklentinin gerçekçiliği | 7 | 6 | 8 |
| Profil uyumu (swing, yüksek getiri, küme) | 8 | 7 | 5 |
| **Toplam / 50** | **38** | **29** | **37** |

Puanlar hakemin yargısıdır. A ile C arasındaki 1 puanlık fark profil uyumundan geliyor. Uygulama ve risk ölçütlerinde ikisi başa baş.

---

## 2. Kazanan: A, ama iskelet olarak; C'nin risk zarfı ve iki küçük kenarı aşılanarak

**Gerekçe**

- **Pazartesi'nin en net ve en düşük riskli talimatı A'da.**
  - Pazartesi mevduat dilimi %15, kalanı banka iştiraki PPF. Merdiven 16, 23 ve 30.11'de kurulur.
  - Pilot pozisyon hesabın %0,25'i riskle, en fazla 2 tane.
  - Emir t+1 kapanış seansına limitli verilir: alışta önceki kapanış × 1,05, satışta × 0,95. Tavan veya taban kilidinde emir atlanır. Bilanço gecesi pozisyon taşınmaz. Çarşamba 11.11 kapanışında yeni giriş yok.
  - Pay vadelisi kullanımı dört yazılı koşula bağlı: teminat nemalanıyor, ima taşıma oranı TLREF'in en az 3 puan altında, likidite yeterli, kurum teminat oranı ≤ %35.
- **Kullanıcının istediği yapıyı korurken bugün sermayeyi riske atmayan tek taslak A.** İstenen yapı: pozitif çarpık, küme ve blok sınırlı, rejim dönünce ölçeklenen bir kol.
- **C daha muhafazakâr ve kanıta daha sadık.** Ancak "yüksek getiri" isteğini açıkça kapsam dışı bırakıyor. Çift işlemlerinin giriş mekaniği de (09:30'da uzlaşma ± %0,5 limitli emir) doğrulanan test koşuluyla örtüşmüyor (§3).
- **B iki kolu yanlış zamanda açıyor:** carry ve bedelsiz. Bazı kurallar kaynağıyla çelişiyor (§3, §4). B'nin değeri iskelette değil, aşılanacak parçalarda.

---

## 3. Ölümcül veya ciddi kusurlar

### A: ölümcül kusur yok

1. **KAPALI rejimde neredeyse hiç işlem yok.** Hesap çekirdek getirisine kilitleniyor. Rejimden bağımsız, doğrulanmış iki küçük kenar (temettü öncesi 5 gün, SAHOL↔AKBNK 20 günlük çift) "başka açıların kolu" diye dışarıda bırakılmış.
   - Temettü kenarı: `v_bist` #26.
   - Çift kenarı: `v_bist` #25.
2. **Basit ve bileşik oranlar karıştırılmış.** A §1.1'de XU030 nakit-taşıma "net mevduattan ~8 puan düşük" deniyor. Burada %29,3 basit oran, %37,9 bileşik oranla kıyaslanmış.
   - Doğru kıyas: basitte %29,3'e karşı %32,6, fark ~3,3 puan; bileşikte %32,2'ye karşı %37,9, fark ~5,7 puan (`v_profesyonel` T12).
   - Hüküm değişmiyor (bugün yapılmaz), ama pay vadelisi avantajı ("mevduattaysa 8–13 puan") da aynı hatayla şişiyor.
3. **AÇIK rejimdeki brüt %60 maruziyet bu hesapta büyük bir kuyruk.** A'nın kendi stres hesabıyla iki ardışık taban (−%19) hesabın ~%11,4'ü eder. Bugün geçerli değil; AÇIK'a geçişte C'nin %10'luk stres tavanı uygulanmalı.
4. **Küçük atıf hatası.** "Bir gün gecikme 52 hafta sinyalini zayıflatmıyor" için `v_bist` #24 gösterilmiş; o madde zirveye yakınlık sıralamasıyla ilgili, kırılımla değil. 120 işlem günü azami tutma da kullanıcının "en çok birkaç ay" ufkunun üst ucu (testte de 120 gün; değiştirilirse test dışına çıkılır).

### B: Pazartesi için ölümcüle yakın iki kusur

1. **Carry (K1) Pazartesi açılıyor, oysa B'nin dayandığı kaynak tam bu durumda çıkış diyor.**
   - Komite §4.2 carry'nin çıkış ve yanlışlama listesinde "**brüt rezerv 160 mlr $'ın altına inerse**" maddesini sayıyor.
   - Brüt rezerv 158,1 mlr $ (önceki hafta 162,2; `v_capraz` #18, DOĞRU). B bunu yalnız "SARI" sayıp 0,05x → 0,10x short F_USDTRY açıyor.
   - Aynı hafta swap hariç net rezerv −6,5 mlr $ düştü. Yabancı DİBS satışı −750 mn $, Nisan'dan beri en büyük satış.
   - Komitenin kendi başabaş hesabı (§2 hüküm 5): 2018 tipi gap olasılığı %4'ü aşarsa beklenen değer negatife döner. Öznel senaryolar ise 1–6 ayda %15 kur hızlanması + %10 kırılma veriyor.
   - Carry %10 stopajlı ve banka long'uyla aynı kuyrukta kaybediyor (`v_capraz` §2.8). **Hüküm: Pazartesi K1 = 0.**
2. **Bedelsiz kuralı test edilmemiş pencereye giriyor.**
   - Kural, SPK onayının yayımlandığı günden sonraki ilk kapanışta alıp hak kullanımına kadar tutmayı söylüyor.
   - Kanıt (`bist_swing_kenarlar` §5.1) yalnız hak kullanım gününe göre [−20,−1] penceresini test ediyor. Rapor, "YK kararı → SPK onayı" işleminin test edilmediğini ve SPK onayından sonraki günlerde literatürde **negatif** anormal getiri bulunduğunu (2016–17) yazıyor.
   - Bedelsiz için doğrulama raporu (`v_olay`) da yok.
3. **Ciddi ama düzeltilebilir kusurlar:**
   - **Pazartesi 10:00'a kadar yazılı aracı kurum cevabı gerçekçi değil.** Bu yüzden K1 ve K3 büyük olasılıkla Pazartesi zaten başlayamaz.
   - **Günlük 17:40–18:08 rutini ve iki bacaklı ayrı opsiyon emirleri** (bacak riski) bu kullanıcının "ekran yok" tercihini zorluyor.
   - **Temettü girişinde bir günlük kayma.** Kural "hak kullanımından 5 işlem günü önce kapanış" diyor; bu, gün −5 kapanışı demek. Test edilen [−5,−1] penceresi gün −6 kapanışında giriş ister. C bunu doğru kurmuş. B'nin sürümü sürüklenmenin ~1/5'ini kaçırır.
   - **O3 strangle fiyat sınırı gevşek.** Sınır uzlaşma fiyatında (≤320 puan), oysa 5.11'de işlemler uzlaşmanın ~%30 altında gerçekleşti:
     - P14000: uzlaşma 137,4, son işlem 100 (1.052 kontrat).
     - C15500: uzlaşma 174,1, son işlem 98,6 (73 kontrat, 9 işlem).
     - Bu, uzlaşmaların kuramsal olduğunu gösteriyor. Limit işlem seviyelerine çekilmezse ucuz vol avantajı dolumda kaybolabilir.
   - **K2 (önce bankalar) en erken 3.12'de tam açılıyor, yani 10.12 PPK'dan bir hafta önce.** Yeni ve doğrulanmamış `olay_akis_rejim` §4.2/§4.5'e göre döngü içi, sürprizsiz indirimlerden sonra XBANK, XU100'ün gerisinde kalıyor: 21/42/63 günde −%2,3/−%4,8/−%6,6 (n=24); döngü düzeyinde 6/6 negatif. B bu dosyayı göremezdi, ama "banka önce" önceliği PPK'yı aşan dönemde zayıf.

### C: ölümcül kusur yok

1. **Çift girişi (K1/K2) test koşulundan farklı.** Giriş 09:30'da, t uzlaşması ± %0,5 limitli emirle yapılıyor.
   - Doğrulanan kanıt t+1 kapanışında giriş varsayıyor ("1 gün gecikme", `v_bist` #25).
   - Sabah limitli emir ters seçim yaratır: Ucuz bacak düşmeye devam ederse emir dolar; hemen dönerse (en iyi işlemler) dolmaz.
   - 17:50 bacak tamamlama kontrolü de gün içi ekran ister.
   - Düzeltme: iki bacak t+1 kapanış penceresinde girilmeli.
2. **K2 (KCHOL↔sepet) 11.11'de, MSCI duyurusundan bir gece önce açılıyor.** Sinyal 20.10'dan beri açık, yani "kalıcı sinyal". C'nin kendi hesabına göre bu tür sinyallerin kanıtı karışık: 2010–18'de −53 bps (n=35), 2019–26'da +272 bps (n=26). Altı bacak var, Aralık kontratları sığ (KCHOL Aralık ~30 mn TL/gün). Yeni kesişim beklenmeli.
3. **İç tutarsızlık.** §1.3 "4 dilim, haftada bir dilim yenilenir" diyor, ama §3.2 dört dilimi aynı haftaya koyuyor (Pzt, Sal, Per, Cum). Bu vadeler haftalık değil, birkaç gün arayla yığılır.
4. **Profil uyumu düşük.** C, kullanıcının "yüksek getiri" isteğini kapsam dışı bırakıyor. Dürüst bir tutum, ama kullanıcıya rejim dönüşünde ne yapacağını A kadar somut göstermiyor (AÇIK'ta K4 riski %0,5).

---

## 4. Doğrulanmış gerçeklerle çelişkiler

| # | Taslak | İddia veya kural | Doğrusu | Kaynak |
|---|---|---|---|---|
| 1 | B | Brüt rezerv < 160 → SARI; carry açılır | Komitenin çıkış ve yanlışlama listesinde "brüt rezerv < 160 → çık". Değer 158,1 | Komite §4.2; `v_capraz` #18 |
| 2 | B | Bedelsiz: SPK onayı → hak kullanımı arası long | Test penceresi hak kullanımına göre. Onay sonrası literatürde negatif anormal getiri; onay günü işlemi test edilmedi | `bist_swing_kenarlar` §5.1 (satır 407, 455) |
| 3 | B | Temettü: gün −5 kapanışında alış | [−5,−1] penceresi gün −6 kapanışında alış ister | `bist_swing_kenarlar` §5.3; C §2.3 |
| 4 | B | O3 sınırı = uzlaşma toplamı (≤320) "ucuz vol" | 5.11 işlemleri uzlaşmanın ~%30 altında; strangle işlem fiyatlarıyla ~199 puan | `viop_20261105.csv` (bu rapor ayrıştırdı) |
| 5 | A | XU030 taşıma "mevduattan ~8 puan düşük" | Basit oranda 3,3, bileşikte ~5,7 puan | `v_profesyonel` T12; `v_capraz` #4 |
| 6 | A | TSMOM12 eşiği nakit %45 ile → XU100 ~15.800 | Test edilen kural ajanın rf serisini kullanıyordu (%37,3; `v_bist` #23). Bugün iki eşik de çok uzak, karar değişmiyor; ama bu test dışı bir varyant | `v_bist` #23; B/C ~15.000 |
| 7 | A | `v_bist` #24 kırılım gecikmesinin dayanağı olarak gösterilmiş | #24 zirveye yakınlık sıralamasıyla ilgili (2022 hariç zayıf) | `v_bist` #24 |
| 8 | C | Çift girişi 09:30, uzlaşma ± %0,5 | Doğrulanan gecikme t+1 kapanışı | `v_bist` #25, §2.5 |
| 9 | A, B | Banka bloğu rejim dönüşünün ilk aracı | Doğrulanmamış yeni bulgu: beklenen indirimlerden sonra bankalar XU100'ün gerisinde (6/6 döngü). 10.12 PPK sonrasına banka aşırı ağırlığı taşınmamalı | `olay_akis_rejim` §0, §4.5 (doğrulaması yok) |

Üç taslağın ortak doğru kararları:
- XU030 taşıma oranında %23,3 yanlıştı; doğrusu %29,3.
- DİBS ancak %0 stopaj yazılı teyit edilirse alınır.
- Arz baskılı ve SPK suç duyurulu hisseler dışlanır.
- Kredili spot işlem yok.
- Kasım pay vadelisi fiziki teslimat öncesi (25–26.11) kapatılır ya da devredilir.
- Pay vadelisinde akşam seansı yok.
- AKCNS'de işlem yok.

---

## 5. Aşılanacak en iyi fikirler

1. **B, Kural 0 (bütün VİOP kollarının ön koşulu).** Aracı kurumdan yazılı alınacaklar: nakit teminat nemalandırma oranı, PPF ve DİBS teminat kesintisi, kurum teminat oranları (PSR), sunucu taraflı şartlı emir, kombine opsiyon emri, komisyon.
   - Teminat faizi politika faizinin %80'inden azsa yapı değişir; teminat hiç faiz almıyorsa carry veya çift açılmaz (`seytan` §5.1; `v_capraz` §2.2).
   - Cevap gelmeden ilgili kol açılmaz (C §6.3'teki 9 soru listesi daha eksiksiz).
2. **C, KAPALI rejim risk zarfı (A'nın rejim merdivenine yerleştirilir).**
   - Toplam açık stop riski ≤ %2,5; stres ≤ %6; VİOP başlangıç teminatı ≤ %15; aylık −%2,5'te yeni giriş yok.
   - Birikimli −%4'te boyut yarıya, −%6'da uydu kolları kapanır.
   - GEÇİŞ'te %3,5 / %8, AÇIK'ta %5 / %10. AÇIK'ta brüt %60 yerine stres ≤ %10 bağlayıcı olur.
3. **A, kırılım makinesi (rejime bağlı tek yüksek getiri kolu).**
   - Kurallar: B52 + 7 koşullu trend şablonu; giriş t+1 kapanış seansına limit × 1,05; kapanış bazlı %15 iz süren stop; azami 120 gün.
   - Tavan kilidinde emir atlanır; bilanço gecesi pozisyon taşınmaz.
   - Limit riskli isimlerde %25 stop mesafesiyle boyutlanır. Tek ve risk-nötr ekleme yapılır.
   - Bugünkü pilot tetikleri: ENJSA > 127,00; AHGAZ > 48,70; ENERY > 14,60. Üçü tek küme sayılır, en çok 1 pilot.
   - Kanıt: `bist_test` §5.1; `v_bist` #28; 2024–26 engel altında (`v_bist` §2.1). Bu yüzden KAPALI'da yalnız ölçüm boyu.
4. **C, SAHOL↔AKBNK 20 günlük oran dönüşü (rejimden bağımsız, piyasa-nötr).**
   - Kural: |z| ≥ 2, 20 gün tutma, bacak başına %7,5, −%8 felaket stopu.
   - Kanıt: bir gün gecikmeyle +160/+310 bps, t 2,4/2,8 (`v_bist` #25). C'nin beklentisi +80…+180 bps.
   - **Değişiklik:** İki bacak t+1 kapanış penceresinde girilir. Komisyon yön başına > 15 bps ise kol kapalı. Kullanıcının 1–3 günlük SAHOL/AKBNK sürümü emekliye ayrılır; aynı çiftte iki sinyal çalıştırılmaz.
   - Bugün z −0,72, yani sinyal yok.
5. **C, temettü öncesi 5 gün (yalnız spot, sezonluk).**
   - Kural: gün −6 kapanışında alış, gün −1 kapanışında satış. Olay başına %3,5, eşzamanlı en çok 3. Temettü verimi ≥ %2, ilk 100 likit hisse.
   - Kanıt: t 6,5, maliyet sonrası ≈ +%0,9 (`v_bist` #26). Kasım–Aralık'ta az olay; asıl sezon Nisan–Haziran.
6. **B, zorunlu akış takvimi tablosu (K4), kaçınma kuralı olarak; A'nın günlük takvimiyle birleşir.**
   - 9.11 akşamı bilanço açıklayacak isimlerde pozisyon yok.
   - 11.11 kapanışında yeni giriş yok.
   - 12.11'de MSCI'ın çıkardığı veya ağırlığını azalttığı isimler 30.11'e kadar alınmaz (`v_capraz` #17: azaltmalar sürüyor).
   - 13.11'de kredili işlem esnekliği uzatılmazsa 27.11'e kadar BIST30 dışı spot long yok; 16–20.11'de düşen hisse alınmaz.
   - BIST30 blok kilidi ~03.02.2027'de açılıyor; fon uyumu 31.01.2027; tasfiye ~17.03.2027 (`v_profesyonel` T7, T8).
   - Yeni pozisyonda Kasım pay vadelisi kullanılmaz.
7. **B'nin ZPAT mekanizması ve C'nin 5 koşullu ZPAT kontrol listesi.**
   - B (SPK 2026/58 ve 2026/71 metnine göre): Teklif, kontrol devrinin kamuya açıklandığı tarihte pay sahibi olanlara yapılır. AKCNS'deki 260,25 TL'ye karşı ~184 TL farkı büyük olasılıkla bundan geliyor.
   - C'nin koşulları: onaylı bilgi formu, grup dışı ve mali gücü belgelenmiş teklif sahibi, fiilen başlamış pencere, maliyet ve güvenlik payı sonrası fark, katılım talimatı.
   - Hüküm: AKCNS'de işlem yok. Tera/PEKGY karşı taraf emsali var.
8. **C'nin carry kapısı ve komitenin brüt rezerv eşiği.**
   - Açılış için hepsi gerekli: swap hariç net rezervin 2 haftalık değişimi ≥ −2 mlr $ ve seviye ≥ 20 mlr $; haftalık yabancı DİBS akımı ≥ −500 mn $; CDS ≤ 275; 10 günlük kur hızı ≤ %30; **brüt rezerv ≥ 160 mlr $**.
   - Açılırsa ≤ 0,10x nominal, yalnız faizli teminatla. Bugün kapalı; en erken 19.11'de değerlendirilir.
9. **B'nin olay strangle'ı (isteğe bağlı, güven düşük).** Aralık P14000 + C15500, hesabın ≤ %0,3'ü prim, en geç 15.12'de kapanır.
   - Yalnız Kural 0 cevabı geldiyse açılır.
   - **Limit işlem seviyelerine yakın olmalı (~≤ 220–250 puan), uzlaşma toplamı (320) değil.**
   - BIST'te vol primi test edilmedi (`v_bist` §3-6); opsiyon alıcısının ortalaması negatif (`v_profesyonel` A6). Bu yüzden çekirdek beklentiye katılmaz.
10. **Yeni bulgu (doğrulanmamış), `olay_akis_rejim`.**
    - Rejim tetiği 3.12'de gelse bile banka aşırı ağırlığı 10.12 PPK'nın ötesine taşınmaz. İlk dilim XU030 ya da çok kümeli liderlerle açılır.
    - Yabancı akımı gecikmeli bir takip göstergesi, ticari kenar değil. A ve B'deki M3 ve L3 yalnız filtre olarak kalır.

---

## 6. Birleşik planın Pazartesi uygulaması (hakemin önerisi)

**Pazartesi sabah 09:00–12:00 (tek seferlik)**

| Kalem | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| Mevduat 1. dilim (%15, 32 gün); 16, 23 ve 30.11'de birer dilim daha | 150 bin | 750 bin | 3 mn (≥3 bankaya bölünür) |
| Banka iştiraki PPF (Pazartesi %85, 30.11'de %40'a iner) | 850 bin | 4,25 mn | 17 mn (≥2 PYŞ) |
| DİBS | Yalnız %0 stopaj yazılı teyit edilirse, ≤12 ay vade | aynı | aynı |
| Pilot kırılım, işlem başı risk %0,25 (nominal %1,67) | 2,5 bin risk / 16,7 bin nominal | 12,5 bin / 83 bin | 50 bin / 333 bin |
| SAHOL↔AKBNK, bacak başına %7,5 (yalnız |z| ≥ 2) | 75 bin; teminat ~25 bin (kurum PSR %33,3 varsayımıyla) | 375 bin / ~125 bin | 1,5 mn / ~500 bin (Aralık sığ: Kasım kontratı, 25–26.11'de devir) |
| Temettü olayı (%3,5) | 35 bin | 175 bin | 700 bin |

- PPF payı Pazartesi %85 (kalıcı %40 + 16/23/30.11 dilimleri için geçici %45); pilot ve olay bütçesi kalıcı %40'ın içinden.
- Çift teminatı tahmindir. C §1.5'teki ~50 bin, %33,3'ün iki bacağa ayrı ayrı uygulandığını varsayıyor; çift mahsubu ve kurum PSR'si aracı kurumdan teyit edilmeli (C §6.3, soru 3).

**Pazartesi açılmayanlar**
- Hisse veya endeks long.
- Short F_USDTRY: kapı kapalı; brüt rezerv 158,1 < 160.
- XU030 nakit-taşıma: %29,3 basit oran, %32,6 basit mevduat netinin altında.
- 9.11 akşamı bilanço açıklayacak isimlerde pozisyon.
- Kasım pay vadelisi.

**Pazartesi akşamı 18:15–18:45**
- Tarama, z-skoru ve tetikler 06.11 ve 09.11 kapanışıyla güncellenir.
- Rejim tablosu (beklenen: KAPALI).
- Kapanış bazlı alarmlar kurulur.

**Hafta takvimi**
- 11.11 kapanışında yeni giriş yok.
- 12.11 sabah MSCI dışlamaları; 14:30 rezerv ve akım verisi.
- 13.11 akşam SPK kararı. Uzatılmazsa 27.11'e kadar BIST30 dışı spot long yok.

**En kötü hafta tahmini (bu kurulumla)**
- İki pilot iki taban görürse: ~−%0,3.
- Bir çift −%15 bacak gap'i görürse: ~−%1,1.
- Toplam ≤ ~%1,5. C'nin %6'lık stres tavanının içinde.

**Beklenti (12 ay, vergi sonrası, engele göre)**
- Merkez +1,5…+2,5 puan; %80 aralık −3…+8.
- Engel ~%31–36 (faiz sabitse ~%37,9).
- Rejim dönerse (S1, öznel %35) kırılım kolundan +4…+8 puan. Bu kolun 2024–26 sonucu engelin altında; kanıt zayıf.

---

## 7. Teyit edilmeden kullanılmaması gerekenler

- Aracı kurumun nakit teminat faizi, PPF/DİBS teminat kabulü ve kesintisi, kurum PSR'leri, çift teminat mahsubu.
- Kapanış seansı için önceden emir girilebiliyor mu? Girilemiyorsa ve sabah normal limitli emir verilirse, emir sürekli işlemde hemen dolar; kapanışa kalmaz.
- Sunucu taraflı şartlı emir. Yoksa koruma yalnız boyuttur.
- DİBS stopajı (GİB metni 30.06.2026'ya kadarki alımları kapsıyor).
- TMSF limiti.
- AKCNS teklifinin KAP'taki durumu.
- 06.11 VİOP bülteni: uzlaşma ve ima oranlar Pazartesi kararından önce yeniden hesaplanmalı.
- `olay_akis_rejim` bulguları ve bedelsiz kanıtı için doğrulama raporu (`v_olay`) yok.
