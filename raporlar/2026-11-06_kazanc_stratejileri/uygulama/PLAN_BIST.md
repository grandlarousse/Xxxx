# BIST / VİOP swing planı (nihai): başlangıç Pazartesi 9.11.2026

- **Hazırlanma:** Cuma 06.11.2026, ~15:00 TSİ. **Son revizyon ~16:00–18:00 TSİ:** iki kırmızı takım raporu ve `dogrulama/v_olay.md` işlendi; değişiklikler ve reddedilen/değiştirilen bulgular §12'de. Fiyatlar aksi yazılmadıkça 05.11.2026 kapanışı ve 05.11 resmî VİOP uzlaşması. Cuma 6.11 kapanışıyla yeniden hesaplanacak kalemler §10'da; günlük sayılar `uygulama/tarama/bist_sinyal_YYYYMMDD.md` dosyasından okunur ([SİN]).
- **Nasıl üretildi:** Hakemlerin iki kez seçtiği C taslağı ("önce risk, kanıt minimalisti") iskelet olarak alındı. A'nın rejim merdiveni ve kırılım motoru ile mevduat ağırlığı eklendi. B'nin engel muhasebesi, Kural 0, zorunlu akış takvimi ve ZPAT hak sahipliği kontrolü eklendi. Hakemlerin bulduğu bütün ölümcül/ciddi kusurlar düzeltildi (liste §11.3). Taslaklardan sonra gelen iki olay çalışması (`olay_bedelsiz`, `olay_akis_rejim`) işlendi. `dogrulama/v_olay.md` revizyonda işlendi: yüksek verimli temettü duyuru koşusu (K3b) bağımsız veriyle yeniden üretildi (muhafazakâr kıyasla +%6–7 fazla), bedelsiz kaçınması doğrulandı, PPK–banka kuralı yalnız boyut eğilimi olarak kaldı, geri alım ve yabancı akımı sinyal değil.
- **Kanıt etiketleri:** **[D]** doğrulanmış (v_* dosyalarında DOĞRU/KISMEN ve yeniden üretilmiş). **[DM]** doğrulanmamış ajan bulgusu. **[TE]** test edilmemiş kural tasarımı (risk kontrolü). **[L]** literatür. **[Ö]** öznel tahmin.
- Yatırım tavsiyesi değildir. Kaldıraçlı VİOP'ta teminatın tamamı, teminat tamamlama ile daha fazlası kaybedilebilir. Bütün olasılıklar öznel tahmindir.

**Kaynak kısaltmaları** (yollar `raporlar/2026-11-06_kazanc_stratejileri/` altına göre; çelişkide doğrulama dosyası esas)

| Kısa | Dosya | Kısa | Dosya |
|---|---|---|---|
| [VB] | `dogrulama/v_bist.md` | [BT] | `ajanlar/bist_test.md` |
| [VC] | `dogrulama/v_capraz.md` | [BS] | `ajanlar/bist_swing_kenarlar.md` |
| [VD] | `dogrulama/v_dalga.md` | [DB] | `ajanlar/dalga_bist.md` |
| [VP] | `dogrulama/v_profesyonel.md` | [TM] | `ajanlar/tr_makro_engel.md` |
| [OB] | `ajanlar/olay_bedelsiz.md` ([VO] ile denetlendi) | [TP] | `ajanlar/tr_profesyonel.md` |
| [OA] | `ajanlar/olay_akis_rejim.md` ([VO] ile kısmen denetlendi) | [SE] | `ajanlar/seytan_taban_oranlar.md` |
| [HA] | `ajanlar/olay_halka_arz.md` | [KK] | `ajanlar/bist_kim_kazaniyor.md` |
| [HZ] | `uygulama/bist_hafta_hazirlik.md` | [TR] | `uygulama/tarama/bist_tarama_20261105.md/.csv`, kod `uygulama/kod/bist_tarama.py` |
| [TA] [TB] [TC] | `uygulama/taslak/bist_A.md`, `bist_B.md`, `bist_C.md` | [HK] [HU] [HD] | `uygulama/taslak/bist_hakem_kanit.md`, `_uygulama.md`, `_deger.md` |
| [KO] | `../2026-10-28_viop_komite_raporu.md` | [PL] | `../2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` |
| [BÜL] | Borsa İstanbul VİOP günlük bülteni `https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv` | [VO] | `dogrulama/v_olay.md` |
| [R1] [R2] | `uygulama/taslak/bist_kirmizi_1.md`, `bist_kirmizi_2.md` | [BİP] | Borsa İstanbul Pay Piyasası "Piyasa İşleyişi" (kapanış seansı, ±%3 marj) ve VİOP "Emirler" sayfaları; VİOP Prosedürü §7, Ek-3 ([R2] §C) |
| [SİN] | `uygulama/kod/bist_sinyal.py` ve çıktısı `uygulama/tarama/bist_sinyal_YYYYMMDD.md` | [RUT] | `uygulama/BIST_GUNLUK_RUTIN.md` |

---

## 0. Yönetici özeti (12 satır)

1. **Rejim bugün KAPALI (0/7).** XU100 11.333, SMA200'ün %16,5 altında. 12 aylık momentum kapalı (+%3,8'e karşı nakit ~%37–45). Makro tetiklerin hiçbiri yok. Likit evrende 52 hafta kırılımı veren hisse yok. 5–6.11 küresel şoku (Nasdaq-100 −%6,4; Nikkei ~−%6; KOSPI −%6/−%8) rejimi değiştirmiyor; ama KRİZ kesicisinin rezerv tetiği (d) 12.11 14:30 verisiyle ateşlenebilir ([HZ] §0 m.9; [TM] §4.3; [R1] B5).
2. **Pazartesi yapılacak tek finansal işlem çekirdeğin kurulması.** Hesabın %15'i doğrudan bankada 32 günlük mevduata (1. dilim), %85'i banka iştiraki PPF'ye. Kalıcı hedef %60 mevduat (dilimler 9/16/23/30.11; 4. dilim 35 gün) ve %40 PPF.
3. **Pazartesi açılmayanlar:** hisse veya endeks long, short F_USDTRY (brüt rezerv 158,1 < 160), XU030 nakit-taşıma (ima basit %29,3 < eşik %35,6), opsiyon. DİBS yalnız %0 stopaj yazılı teyit edilirse.
4. **Pazartesi kurulacaklar:** aracı kurum seçimi ve 12 yazılı soru (Kural 0: teminat faiz kazanmıyorsa VİOP kolu yok), kapanış bazlı alarmlar, dışlama listesi, işlem günlüğü, K9 fikir kartı şablonu ve ölçü biriminin (TL engeli ya da USD) yazılı seçimi. Akşam rutini [RUT], günlük sayılar [SİN].
5. **Emir tekniği:** Bütün spot emirler kapanış seansının emir toplama aşamasında (18:01–18:05) ve son fiyatın ±%3'ü içinde verilir. Risk azaltan çıkışlar izin verilen en düşük fiyatla girilir; böylece hisse kilitli değilse müzayede fiyatından dolar ([BİP]; [R1] B1; [R2] A.1).
6. **Rejimden bağımsız açık kalan doğrulanmış kollar (sinyal gelirse):** SAHOL↔AKBNK 20 günlük oran dönüşü (VİOP, t+1 kapanış girişi, komisyon ≤ 5 bps/bacak/yön) ve temettü hak kullanımından önceki 5 gün (spot; küçük kenar, olay başına +%0,2…+%0,5).
7. **Rejim dönerse devreye girecek yukarı motor:** 52 hafta kırılımı + trend şablonu + %15 iz-stop. Boyut KAPALI'da işlem başı %0,25 risk (en çok 2 sonda), GEÇİŞ'te %0,5, AÇIK'ta %0,75. En yakın tetikler: ENJSA 127,00 (3Ç bilançosu 02.11'de geldi; Pazartesi kapanış sinyali Salı girilebilir) ve AHGAZ 48,70 / ENERY 14,60 (tek isim, aktif ihraççı geri alımı, bilanço 9.11 akşamı; en erken giriş SPK kararından sonra). Üçü tek küme.
8. **Kaçınma takvimi:**
   - Bilançosunu 9.11 18:00'den önce açıklamamış isimlerde 9.11 kapanışında giriş yok.
   - 11.11 kapanışında hiçbir kolda; 11, 12 ve 13.11 kapanışlarında K3/K4/K5/K9'da yeni giriş yok. Kredili esneklik uzatılırsa ilk giriş 16.11; uzatılmazsa K4 23.11'den, VİOP-47 dışı long 30.11'den önce yok.
   - MSCI: her gözden geçirmede (12.11, Şubat 2027) ve her ad hoc duyuruda çıkarılan ya da ağırlığı düşürülen hisse yürürlüğe kadar alınmaz; danışma açılırsa KRİZ.
   - Bedelsiz hak gününden sonra 10, yüksek verimli temettüde 5 işlem günü alış yok.
   - 10.12 PPK sürprizsiz indirimse ~15.03.2027'ye kadar banka kümesinde yarım boy.
9. **Ölçüm birimi:** Her kol engele göre fazla getiriyle ölçülür, öldürülür ve büyütülür: R_fazla = (net K/Z − bağlanan nakit × engel × gün/365) / risk. Ham R kullanılmaz.
10. **Dürüst beklenti (12 ay, vergi sonrası, engele göre):** merkez **+1…+2 puan**, %80 aralık **−2…+5,5**. Toplam net nominal TL getirisi ~%33–37, reel ~%3–7. USD bazında ağırlıklı ~+%10 (çok belirsiz); S4'te şok anında −%10…−%21 (§9.2). Engelin altında kalma olasılığı ~%35–45. KAPALI rejim sürerse yalnız +0,5…+1,5 puan. Rejim 1–3 ayda dönerse kırılım ve endeks kollarından +3…+8 puan; kârın çoğu birkaç işlemden gelir.
11. **Plan dışı fren:** Plan dışı fikirler yalnız K9 serbest kolundan açılır (KAPALI'da işlem başı risk %0,25; birikimli −%1,5'te 6 ay kapanır). K1–K9 dışındaki tek bir işlem bütün uyduyu 1 ay kâğıda alır ([R1] B2).
12. **"Yüksek getiri" cevabı:** Bu rejimde kanıtın tavanı engel artı birkaç puan. +10–20 puan hedeflemek 3–5 kat risk ve engele göre −%25…−%40 düşüş toleransı ister; kanıt bunu desteklemiyor ([VB] §2.1, [VD] B2, [SE] §5.1). En büyük doğrulanmış yeni kenar K3b'dir (yüksek verimli temettü duyuru koşusu, [VO] §2.3); Şubat–Mayıs 2027 sezonunda yarım boylu, önceden kayıtlı pilot olarak açılır.

---

## 1. Sermaye dağılımı ve engel

### 1.1 Engel (birey, vergi sonrası)

| Kalem | Değer | Kaynak |
|---|---|---|
| Politika faizi / koridor | %36 / %34,5–39; sonraki PPK 10.12 (anket %35) | [VC] #1; [HZ] §0 m.7 |
| TLREF | %35,85 (5.11) | [HZ] §4c |
| Ekim TÜFE | Yıllık %29,77, aylık %2,58 (beklenti ~%2,2) | [VC] #2 |
| 32 gün mevduat, banka ortalaması (6.11, 100 bin TL) | Brüt %39,52 → net basit **%32,6** → aylık yenilemeyle net bileşik **~%37,9** (faiz sabitse) | [VC] #4; [TB] Ek A |
| Banka iştiraki PPF | Net ~%34–35 (1 yıl tutuş; stopaj bir kez). Son 1 yıl medyanı brüt %45,5 → net ~%37,5 | [VC] #4; [VB] #13 |
| İleriye dönük 12 ay net engel | Faiz sabitse ~%36–38; anket patikasında ~%31–33 | [VC] #4; [TM] §1.3 |
| Reel engel | ~%5–8 ("reel %40–50" algısı yanlış) | [VC] #3 |
| Stopaj | Spot pay ve pay/endeks VİOP %0. F_USDTRY ve diğer VİOP %10. PPF ve ≤6 ay mevduat %17,5. DİBS %0 yalnız 30.06.2026'ya kadarki alımlar için resmî; 31.12.2026 uzatması tek ikincil kaynakta | [VC] #6, #7, #8; [VB] #15 |
| 2027 riski | %17,5 oranı ve DİBS muafiyeti 31.12.2026'da bitiyor. Çekirdek Aralık'ın son haftasında yeniden seçilir | [VC] §2 m.6 |

**Plan içi engel tanımı (ölçüt):** Her uydu kolu, aynı dönemde kullanılan banka PPF'sinin vergi sonrası fiilî getirisiyle karşılaştırılır. Formül: engel_dönem = (PPF fiyatı çıkış / PPF fiyatı giriş − 1) × 0,825. Sabit bir %36 kullanılmaz ([TC] §1.1; [TB] §6.4).

### 1.2 Çekirdek araçları (5.11 fiyatlarıyla; Aralık vadesine kadar 56 gün)

| Araç | 56 günde net | Yıllık (basit / bileşik) | Risk | Hüküm | Kaynak |
|---|---|---|---|---|---|
| 32 gün mevduat merdiveni (≥2 büyük banka; doğrudan bankada) | ~%5,06 | %32,6 / ~%37,9 | Banka riski (TMSF limitini bankadan teyit et); vade bozulursa faiz yanar; her yenilemede indirime göre düşer | **Çekirdeğin ana gövdesi** | [VC] #4 |
| Banka iştiraki PPF (en az 2 fon) | ~%4,54 | ~%29,6 / ~%34–35 | Günlük likidite. Tasfiyedeki 15 PPF'nin 4'ü −%95…−%99,9 kaybetti → **yalnız mevduat bankası iştiraki PYŞ**; ters repo karşı tarafında grup ihracı olmayan fon. Tasfiyedeki 7 PYŞ (Pardus, Hedef, Atlas, Bulls, Pusula, A1, Tera) asla | **Likidite tamponu ve VİOP teminat kaynağı** | [VB] §3 m.3; [VB] #5; [TB] §1.2 |
| ≤12 ay vadeli DİBS | ~%5,2 | ~%39 bileşik (stopaj %0 ise) | Süre riski; S4'te hisseyle aynı yönde kaybeder | **Koşullu, ≤%10,** mevduat payından. Yalnız aracı kurum/banka 9–30.11 alımlarında %0 stopajı **yazılı** teyit ederse | [VC] #8; [HZ] §4c |
| XU030 nakit-taşıma (BIST30 BYF/sepet long + F_XU0301226 short) | %4,49 brüt, vergisiz | %29,3 / %33,1 | Takip hatası, teminat, temettü | **Bugün HAYIR.** Basitle basit: %29,3 < mevduat neti %32,6. Açma kuralı §1.5 | [VP] T12; [VC] §2 m.1 |
| Short F_USDTRY (TL carry) | — | Fazla getiri nominalin ~%8–12'si/yıl, %10 stopaj öncesi | Negatif çarpık. 2010–26 Sharpe −0,51, MaxDD −%90; tek ayda −%24…−%35. Prim daralıyor (28 → 22 → 17 → ~13 puan). USD teminat ~%0 kazanır | **Çekirdek değil.** Kapılı uydu K6, bugün 0 | [VC] #19, §2 m.3; [TM] §4.3; [BS] §8.1 |

Not (hata düzeltmesi): Tarama dosyası ve hazırlık notu §0 m.8, XU030 Aralık için %23,3 ima faiz veriyor. Bu **yanlış**, çünkü yanlış vadeli fiyatı (14.605) kullanılmış. Resmî uzlaşma 14.734'tür ([VP] T12). Bütün ima oran hesapları yalnız [BÜL] uzlaşmasıyla yapılır; taramanın VİOP tablosu kullanılmaz.

### 1.3 Karar: rejime göre dağılım (hesabın %'si)

| Kalem | KAPALI (bugün) | GEÇİŞ | AÇIK |
|---|---|---|---|
| 32 gün mevduat merdiveni | **%60** (4 × %15) | %50 | %30 |
| Banka iştiraki PPF (uydu kovası ve VİOP teminatı dahil) | **%40** | %50 | %70 |
| İçinden uydu spot sermayesi, azami | %15 | %25 | %40 |
| VİOP başlangıç teminatı, azami (bağlayıcı olan L1, aşağıda) | %15 | %20 | %25 |

Kurallar:
1. **Mevduat ağırlığı A'dan alındı.** Faiz sabitken mevduat PPF'den ~3 puan fazla kazanır; PPF'den mevduata kaydırılan her %15 hesaba risksiz ~+0,45 puan ekler ([HD] §2; [VC] #4). Sınırı likidite ihtiyacı belirler.
2. **Dilim takvimi:** 9.11, 16.11, 23.11 ve 30.11'de birer dilim (%15) açılır. Henüz bağlanmamış dilimler PPF'de bekler, yani PPF Pazartesi %85'tir ve 30.11'de %40'a iner ([TA] §1.3). Böylece her hafta hesabın %15'i vadeye gelir.
3. **Rejim yükselirse:** Uydular önce PPF'den, sonra vadesi gelen dilimden fonlanır. Vadesi gelen dilim yenilenmez, PPF'ye aktarılır. **Hiçbir dilim vadesinden önce bozulmaz.**
4. **Kredili işlem (spot kaldıraç) hiçbir rejimde yok.** Örtük maliyeti ~%60 ([VB] #3).
5. **20 mn TL hesap:** Mevduat en az 3 bankaya, PPF en az 2 PYŞ'ye bölünür.
6. **Teminat ve likidite: L1–L3 ([R1] B3).** Yukarıdaki %15 / %20 / %25 VİOP tavanları üst sınırdır; bağlayıcı olan L1'dir. Eski "serbest teminat ≥ 2 × başlangıç teminatı" kuralı mevduat bozulmadan sağlanamıyordu (KAPALI'da %15 spot + %15 teminat + %30 serbest = %60 ihtiyaç, PPF %40); L1 onun yerine geçti.
   - **L1 (her kapanış):** VİOP başlangıç teminatı (kurum oranıyla) ≤ (PPF − spot uydu nominali) / 3. Böylece oranların 3 katına çıkması mevduat bozulmadan karşılanır. Örnek (1 mn TL, KAPALI, 30.11 sonrası): PPF 400 bin, spot uydu 100 bin → teminat ≤ 100 bin. K1 QNB oranıyla (2 × 75 bin × %33,3) 50 bin tutar ve sığar; bacaklardan biri %100 sınıfına alınırsa 100 bin ister, yine sığar; ikisi birden alınırsa 150 bin ister → K1 2/3'e iner.
   - **L2:** L1 bozulursa (oran artışı ya da zarar) ertesi kapanışta VİOP pozisyonları orantılı küçültülür. Sıra K6 → K7 → K2 → K9 → K1; K1'in iki bacağı birlikte. Teminat için spot uydu satılmaz, mevduat bozulmaz.
   - **L3:** Teminat tamamlama PPF'den yapılır; satış emri PPF'nin saat sınırından (çoğunda 13:30; izahnameden teyit) önce verilir. VİOP hesabında her zaman ≥ 1 × başlangıç teminatı kadar fazla teminat durur: PPF teminat olarak kabul ediliyorsa PPF, edilmiyorsa nakit (bu durumda Kural 0 gereği boy yarıya iner).
   - **Çekirdek tanımı ([R2] A.13b):** Mevduat + PPF (teminata verilmiş PPF dahil) KAPALI'da ≥ %85, yani spot uydu ≤ %15. VİOP teminatı PPF'nin içinden L1 ile sınırlanır.
7. **Saklama ([R1] B7):** Mevduat dilimleri doğrudan bankada tutulur, aracı kurumda değil. PPF banka kanalından alınır (20 mn TL'de en az 2 kurum). Aracı kurumda yalnız L1–L3'ün gerektirdiği VİOP teminatı ve açık spot pozisyonlar durur; boştaki nakit gece aracı kurumda kalmaz, PPF'ye geçer. 20 mn TL hesapta spot ve VİOP iki ayrı kurumda tutulur.
8. **Nominal tavanı ([R1] B10):** Spot uydu tavanını (%15 / %25 / %40) aşacak yeni giriş §5'teki öncelik sırasına göre reddedilir; açık pozisyon küçültülmez. (KAPALI'da kolların azamileri toplanınca ~%24–28 ediyor; tavan bunları birlikte sınırlar.)

### 1.4 Pazartesi uygulaması: 1 / 5 / 20 mn TL

| Kalem | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| Mevduat 1. dilim (%15, 32 gün), 9.11 | 150 bin | 750 bin | 3 mn (≥3 banka) |
| Mevduat 2., 3., 4. dilim (16, 23, 30.11; 4. dilim **35 gün** → 04.01.2027, çünkü 30.11 + 32 gün 01.01 tatiline düşer; banka 35 günü aynı orandan vermezse 31 gün) | 3 × 150 bin | 3 × 750 bin | 3 × 3 mn |
| PPF, 9.11 (kalıcı %40 + geçici %45) | 850 bin | 4,25 mn | 17 mn (≥2 PYŞ) |
| PPF, 30.11 sonrası (kalıcı %40) | 400 bin | 2 mn | 8 mn |
| DİBS (yalnız yazılı %0 stopaj teyidiyle; 4. dilimin yerine) | ≤100 bin | ≤500 bin | ≤2 mn |
| Çekirdeğin beklenen aylık net getirisi (~%2,5–2,7, faiz sabitse) | ~25–27 bin | ~125–135 bin | ~0,50–0,54 mn |
| Pazartesi açılan uydu pozisyonu | Yok | Yok | Yok |

### 1.5 İki açma kuralı (her akşam [BÜL] ile; karşılaştırma **basitle basit**)

- **İma basit oran:** i = (F_uzlaşma / S_kapanış − 1) × 365 / kalan gün. 5.11'de XU030 Aralık: (14.734 / 14.101 − 1) × 365/56 = **%29,3** (bileşik %33,1). Pay vadelileri, **Aralık** kontratı (5.11; [R2] A.8): GARAN %26,9, AKBNK %30,6, YKBNK %30,7, KCHOL %30,0, SAHOL %32,1, ENJSA %9,8. (Kasım: GARAN %25,2, AKBNK %26,3, YKBNK %28,0; Kasım yeni pozisyonda kullanılmaz.)
- **XU030 nakit-taşıma açılır:** i ≥ (32 gün mevduat brüt × 0,825) + 3 puan **ve** Kural 0 (§6.1) sağlanıyorsa. Bugün eşik %32,6 + 3 = %35,6 → **kapalı.** Açılırsa: BIST30 BYF ya da ≥10 hisselik BIST30 sepeti alınır, aynı kapanışta F_XU030 satılır, vadede kapanır ([TB] §1.5; [VC] §2 m.1).
- **Long için pay vadelisi:** Yalnız şu koşulların hepsi sağlanırsa (A'nın 8–13 puanlık bileşik/basit hatası düzeltildi; [HK] §3.1 m.4, [HD] §4):
  1. (Serbest kalan nakdin fiilen yattığı aracın net basit oranı − i) ≥ 3 puan. Aralık kontratlarında bugün mevduat netine (%32,6) göre yalnız GARAN geçiyor (+5,7 puan); AKBNK +2,0, YKBNK +1,9, KCHOL +2,6, SAHOL +0,5 geçmiyor.
  2. Kural 0 sağlanıyor (teminat faizli ya da PPF/DİBS teminat kabul ediliyor).
  3. **Kullanılacak kontratta** açık pozisyon ≥ 20.000 kontrat ve günlük hacim ≥ 100 mn TL (bülten sütun 22 ve 18). 5.11'de hiçbir Aralık pay kontratı sağlamıyor (ör. AKBNK Aralık açık pozisyon 16.098, hacim 118 mn TL) → **bugün long için pay vadelisi kullanılmaz, spot kullanılır.**
  4. Kurum teminat oranı ≤ %35.
  5. Kasım kontratı yeni pozisyonda kullanılmıyor.
- **Spotta kalma:** İma oran < %15 ya da negatifse (ör. ENJSA Kasım −%10,4, Aralık %9,8) KAP'ta temettü veya sermaye işlemi aranır. Açıklanamıyorsa spot kullanılır ([TA] §2.1.3).

---

## 2. Rejim anahtarı ve bugünkü okuma

### 2.1 Göstergeler

| Kod | Gösterge | Açık (=1) koşulu | Ne zaman | 05.11 değeri | Durum | Kaynak |
|---|---|---|---|---|---|---|
| T1 | XU100 kapanış > SMA200 | evet | Her kapanış | 11.333 vs 13.572 (−%16,5; gereken +%19,8). Yatay kalırsa SMA200 30.11'de ~13.380 | 0 | [BT] §5.1 (S5); [VD] B12; [TA] EK-4 |
| T2 | TSMOM12: XU100 12 ay getirisi > aynı 12 ayın TL nakit getirisi | evet | Ay sonu kapanışı | +%3,8 vs ~%37 (test serisi) / ~%45,5 (gerçekleşen brüt PPF). 30.11 eşiği ~14.960 / ~15.860; **karar için 15.860 kullanılır** | 0 | [BT] §2; [VB] #23; [TA] §3.2 |
| T3 | XU100 son 5 kapanışın 5'inde SMA50 üstünde | evet | Her kapanış | SMA50 12.691 (−%10,7). Yatay kalırsa 30.11'de ~11.700 | 0 | [TA] §3.1, EK-4 |
| M1 | Swap hariç net rezerv 3 hafta üst üste artış | evet | Perşembe 14:30 | 30,8 → 24,3 mlr $ (−6,5) | 0 | [TM] §5.1; [VC] #18 |
| M2 | Aylık TÜFE < %2,0, **2 ay üst üste** (kaynağın tanımı; taslaklardaki tek ay hatası düzeltildi) | evet | Ayın 3'ü 10:00 | Ekim %2,58 | 0 | [TM] §5.1 (satır 313); [HD] §4 B m.3 |
| M4 | CDS 5 yıl < 230 **ve düşüyor** (20 iş günü öncesinin altında); yalnız teyitli veriyle ([R2] A.13f) | evet | Günlük | ~248 (bağımsız teyit yok) | 0 | [TM] §5.1; [VC] §1 sonu |
| M5 | XBANK kapanış > kendi SMA200'ü | evet | Her kapanış | 16.085 vs 16.955 (−%5,1) | 0 | [TA] §3.1; [HZ] §4a |
| Bilgi | Yabancı hisse akımı (TCMB) | **Sayılmaz** | Perşembe 14:30 | Son hafta −66,3 mn $; 6 hafta −334,5 mn $ | — | [OA] §3: akım getiriyi izliyor, 2021–26'da ileri getiri anlamsız [DM] |
| Bilgi | Genişlik, sektör endeksleri | Sayılmaz | Cuma | BIST100'ün %13'ü SMA200 üstünde; hiçbir sektör endeksi SMA200 üstünde değil | — | [HZ] §4a, §6 |
| Bilgi | Brüt rezerv (yalnız K6 kapısı) | ≥ 160 mlr $ | Perşembe | 158,1 (önceki 162,2) | — | [KO] §4.2; [VC] #18 |
| Bilgi | Küresel şok | Sayılmaz | Günlük | 5.11 Nasdaq-100 −%6,4; 6.11 Nikkei ~−%6, KOSPI −%6/−%8; Brent 6.11 ~95,5 $ | — | [HZ] §0 m.9; [R1] B5 |

Makro eşikler 4 tarihî örnekten türetilmiş öznel eşikler; hayatta kalma ve rejim bağımlılığı yüksek ([TM] §5.3). Rejim filtresi getiri kaynağı değil, risk kontrolüdür ([BT] §6).

### 2.2 Durumlar ve izinler

| Durum | Tanım | İzinler | Kanıt |
|---|---|---|---|
| **AÇIK** | T1 = 1 (sinyal gününün kapanışında) | K4 tam boy (r₀ %0,75), K7 yalnız T2 = 1 ise, ekleme serbest | Test edilen kapı: S5 = kırılım + XU100 > SMA200, placebo üstü +%5,7, t 5,4 [D] ([BT] §5.1; [VB] #28) |
| **GEÇİŞ** | AÇIK değil **ve** T3 = 1 **ve** M1 = 1 **ve** {M2, M4, M5}'ten ≥ 1 | K4 yarım boy (r₀ %0,5), ekleme yok, K7 yok | [TE]: test edilmedi, bu yüzden yarım boy |
| **KAPALI** | Diğer bütün durumlar. **Bugünkü durum.** | K4 yalnız sonda (r₀ %0,25, en çok 2); K1, K3, K3b (pilot dönemi), K5 serbest (rejimden bağımsız); K9 risk %0,25; K6 kapıya bağlı; K7 kapalı | — |
| **KRİZ kesicisi** (her durumun üstünde) | Herhangi biri: (a) XU100 son 5 işlem günü kapanıştan kapanışa ≤ −%8; (b) USDTRY (S_t / S_t−10)^(252/10) − 1 > %35; (c) teyitli CDS > 300; (d) swap hariç net rezerv 2 hafta üst üste ≤ −5 mlr $ ya da seviye < 0; (e) F_USDTRY ön ay ima basit faizi > politika faizi + 5 puan ([BÜL] uzlaşması, §1.5 formülü; 5.11'de ~%32–34); (f) MSCI'ın Türkiye için sınıflandırma danışması açması | 5 işlem günü hiçbir kolda yeni giriş yok; K6 kapanır. **Açık pozisyonlar, ertesi kapanış:** hedgesiz K3/K3b kapanır; K4, K5, K9 stopu = max(iz-stop, KRİZ günü kapanışı × 0,90); K1 sürer, bir bacak kilitliyse diğer bacak kapatılmaz; K7 kendi kuralıyla (gerekirse akşam seansında F_XU030 yarısı azaltılır) | [TE]; [TC] §3.1; [KO] §4.2; [TM] §5.1; [R1] B5 |

- **Değerlendirme:** Durum her kapanıştan sonra (18:20 sonrası, [SİN]) hesaplanır ve ertesi işlem gününden geçerli olur.
- **Düşüşler (AÇIK → GEÇİŞ → KAPALI):** Mevcut K4 pozisyonlarını kapatmaz (testteki çıkış iz-stoptur). Yalnız yeni girişleri ve boyutu etkiler. K7 kendi çıkış kuralıyla kapanır. **KRİZ ise açık pozisyonlara dokunur** (yukarıdaki eylem).

### 2.3 Bugün ne diyor (05.11)

**KAPALI: 7 göstergenin 0'ı açık.** İzinler:
- Mevduat + PPF ≥ %85 (spot uydu ≤ %15); VİOP başlangıç teminatı ≤ L1 (§1.3); toplam açık risk ≤ %2,5; stres ≤ %6.
- **KRİZ yakın tetiği:** Swap hariç net rezerv son hafta −6,5 mlr $. 12.11 14:30 verisi bir hafta daha ≤ −5 mlr $ gösterirse (d) tetiklenir ([TM] §4.3: "bu hızla 4 haftada sıfır").
- K1 ve K3 sinyal gelirse açılabilir (K1 için önce Kural 0 ve komisyon ≤ 5 bps/bacak/yön).
- K4 yalnız sonda; K9 yalnız fikir kartıyla (risk %0,25); K6 kapalı (kapı); K7 kapalı.

**En erken değişebilecek göstergeler:**
- **M1:** 12, 19 ve 26.11 verilerinin üçü de artış gösterirse 26.11'de 1 olur.
- **T3:** SMA50 düştüğü için haftalar içinde gelebilir. Yatay piyasada Kasım sonu uzaklık ~%3 ([TA] §3.2).
- **M2:** En erken ~4.1.2027 (Kasım ve Aralık TÜFE'si).
- **T1 ve T2:** Haftalar içinde ilgisiz. T1 için +%18–20, T2 için +%32–40 gerekir.

**Sonuç:** GEÇİŞ için en erken gerçekçi tarih **26.11 kapanışı**. Koşul: M1 ve T3 ile birlikte M4 veya M5 açık olmalı.

---

## 3. Kollar: kesin kurallar

**Ortak kurallar (bütün kollar)**
- Sinyal kapanış verisiyle (18:10 sonrası) hesaplanır, işlem **ertesi gün** yapılır. Bu, doğrulamadaki gerçekçi gecikme varsayımıdır ([VB] #25, §2.5).
- **Spot emirleri, kapanış seansı ([BİP]; [R2] A.1).** Aşamalar: emir toplama **18:01–18:05**, fiyat belirleme 18:05–18:07, kapanış fiyatından işlemler 18:08–18:10. Kapanış seansında girilen emrin fiyatı, kapanış seansından önceki son işlem fiyatının (P_son) **±%3'ünden** fazla farklı olamaz; günlük ±%10 limit de aşılamaz. Bu yüzden:
  - **Alış limiti** = min(plan limiti; P_son × 1,03), aşağı fiyat adımına yuvarlanır. Plan limiti P_son × 1,03'ün altındaysa (gün içi sıçrama) plan limiti kullanılır; dolmazsa ertesi gün aynı kural.
  - **Risk azaltan satış** (K4 E1/E3/E4/E6/E7; K3 gün −1 satışı ve stopu; K3b çıkışları; K5 çıkışı; K8 satışı; K9 stopu; A3, A4, KRİZ, L2 ve dışlama çıkışları): limit = **izin verilen en düşük fiyat** = max(günün taban fiyatı; P_son × 0,97), yukarı fiyat adımına yuvarlanır. Tek fiyatlı müzayedede emir eşleşme fiyatından dolar. Dolmamışsa hisse tabanda kilitlidir ve emir ertesi gün aynı kuralla yenilenir ([R1] B1). Test, çıkışı yalnız ≤ −%9,5 günlerinde erteledi ([BT] §1 m.3); bu kural testle uyumludur, eski "önceki kapanış × 0,94" limiti değildi (5 gün üst üste kilitsiz −%7'de emir hiç dolmaz, kayıp −%30).
  - **Acil olmayan satış** (yalnız K4 E2 süre çıkışı): limit = max(önceki kapanış × 0,94; P_son × 0,97).
  - 18:05 kaçırılırsa 18:08–18:10 aşamasında kapanış fiyatından emir girilir ve günlüğe "geç" yazılır. O da kaçarsa ertesi gün aynı kural.
  - Sürekli işlemde gerçekleşmeyen günlük emirler kapanış seansına aktarılır; ama sabah girilen limitli emir gün içinde dolabilir ve kapanış fiyatı olmaz. Bu yüzden **sabah normal limitli emir verilmez** ([HU] §7). Aracı kurum yalnız kapanış seansına özel emir ya da dengeleyici emir sunuyorsa (§6.1 soru 5) önceden girilebilir; limit kuralları aynıdır.
  - Ekran yükü: emir olan günlerde 18:00–18:05 arasında tek bir 5 dakikalık pencere. Gün içi izleme yok.
- **VİOP emirleri (Kural 0 sağlanmışsa):** Giriş 17:55'te karşı en iyi fiyat ± %0,3; 18:05'te dolmayan bacak ± %0,6. **Çıkış:** 17:55'te ± %0,3; 18:05'te ± %1; 18:08'de günlük fiyat limiti; kilitte ertesi gün aynı sıra ([R1] B1). Piyasa emri VİOP'ta 1.3.2021'den beri yok ([BİP]; [PL] §5). Pay vadelisi ve USDTRY'de akşam seansı yok ([HZ] §5; VİOP Prosedürü §7).
- **Tavan kilidi:** Giriş günü hisse tavanda kilitliyse (≥ +%9,5) emir atlanır ([BT] §1, gerçekçi dolum).
- **Bilanço:** Sinyal kapanışı ile giriş kapanışı arasında finansal tablo açıklanacaksa giriş yok. Açıklamadan sonraki ilk kapanışta sinyal yeniden değerlendirilir [TE].
- **Tavanlar:** Yeni giriş spot uydu nominal tavanını (§1.3 m.8), açık risk ya da stres tavanını (§5) ya da L1'i aşacaksa §5'teki öncelik sırasına göre reddedilir; açık pozisyon küçültülmez ([R1] B10).
- **KRİZ (§2.2) ve birikimli −%4 kuralı (§5) açık pozisyonlara da uygulanır** ([R1] B5).
- **Engel muhasebesi:** Her işlemin fazla getirisi kaydedilir. VİOP'ta bağlanan nakit, faiz kazanmayan teminattır (§8.1).

### K1. SAHOL↔AKBNK oran dönüşü, 20 gün (VİOP pay vadelisi; rejimden bağımsız)

**Kanıt [D]:**
- [BS] §9.1: L=60, |z|≥2, H=20; aynı kapanış girişiyle +250 / +388 bps.
- [VB] #25: Bir gün gecikmeyle **+160 / +310 bps** (2010–18 / 2019–26), **t 2,4 / 2,8**. Maliyet sonrası (20 bps) ~+140 / +290 bps. Çift önceki çalışmadan seçildi (seçim yanlılığı). En kötü işlem −%5,8 / −%8,3.
- [TC] §2.1: Örtüşen tüm |z|≥2 günlerinde gecikmeli 20 gün +133 / +280 bps (isabet %65 / %64).

**Sinyal (her kapanış, 18:15 sonrası):**
1. Düzeltilmiş kapanışlarla x = ln(SAHOL) − ln(AKBNK). Günlük |getiri| > %60 maskelenir ([VB] `rv_lag.py` tanımı).
2. m ve s, bugün dahil son 60 günün ortalaması ve standart sapması; z = (x − m) / s.
3. z ≥ +2 → **F_SAHOL SAT + F_AKBNK AL**. z ≤ −2 → tersi. TL nominaller eşit.
4. Aynı çiftte açık işlem varken yeni giriş yok.

**Giriş (t+1; C'nin 09:30 sabah limiti kaldırıldı):**
- **17:50 kontrolü:** Bacaklardan biri gün içinde ±%9 ya da ötesindeyse o gün giriş yok; sinyal ertesi kapanışta yeniden değerlendirilir ([R1] B9).
- 17:55'te iki bacak birden limitli emirle girilir. Limit = karşı en iyi fiyat ± %0,3 (alınan bacak üstü, satılan bacak altı).
- 18:05 kontrolü: Bir bacak dolmadıysa o bacağın limiti ± %0,6'ya çekilir.
- 18:08'de hâlâ tek bacak varsa: 18:10'a kadar dolan bacağın β × nominali kadar **ters yönde F_XU030** açılır (bankalarda ve SAHOL'de 1–3 günlük varyansı ~%41–44 azaltır; [PL] §3). β = son 250 günün günlük getiri betası, günlükte tutulur. Ertesi gün 17:55'te bacak ve hedge birlikte VİOP çıkış sırasıyla kapatılır ve "dolum hatası" diye kaydedilir.

**Çıkış:**
- **Zaman:** Girişten sonraki 20. işlem günü, VİOP çıkış sırasıyla (§3 ortak kurallar), z ne olursa olsun.
- **Felaket stopu:** Bir kapanışta çift K/Z'si bacak nominalinin ≤ −%8'i ise ertesi gün çıkılır [TE: testte yok, kuyruk sigortası].
- **Kurumsal olay:** Sabancı/Akbank pay yapısı, birleşme ya da pay alım teklifi açıklanırsa ertesi gün çıkılır ve kol askıya alınır.
- **KRİZ:** K1 sürer. Bir bacak kilitliyse diğer bacak kapatılmaz (tek bacak yönlü riske dönüşür; [R1] B5).

**Vade:**
- Pay vadelisi **fiziki teslimatlı**. Kasım bacakları en geç **25.11 kapanışında** kapatılır ya da Aralık'a devredilir.
- 20 günlük süre 30.11'i aşacaksa giriş doğrudan Aralık kontratıyla yapılır. Şart: Aralık alış-satış makası ≤ %0,3. Aralık hacmi 5.11'de SAHOL 22 mn TL, AKBNK 118 mn TL ([TC] §2.1).
- Aralık bacakları en geç **23.12 kapanışında** Ocak/Şubat kontratına devredilir ya da kapanır (A10).

**Boyut:**
- Bacak başına hesabın **%7,5'i** nominal; her rejimde aynı.
- Felaket stopu riski ≈ %0,6; tek bacak −%15 gap stresi ≈ hesabın −%1,1'i.

**Kapılar (hepsi gerekli):**
1. Kural 0 (§6.1).
2. Komisyon **bacak ve yön başına ≤ 5 bps** (BSMV ve borsa payı dahil). Test çift başına gidiş-dönüş 20 bps varsaydı = 4 dolum × 5 bps ([VB] #25; [R2] A.5). 5 bps'yi aşarsa K1 yalnız kâğıt.
3. Aracı kurum çift teminatını yazılı bildirmiş.

**Beklenti:**
- İşlem başına net **+80…+180 bps** (backtest'e %40 çürüme/seçim iskontosu); isabet %60–70; yılda ~5 işlem.
- Hesaba katkı merkez **+0,4 puan/yıl**, aralık 0…+0,9.
- Teminat faizsiz nakitse ~0,6 puan/yıl sürtünme kenarı sıfırlar; bu yüzden Kural 0 ([TC] §2.1).

**Bugün:**
- z = **−0,72** (5.11), sinyal yok.
- Tam tetikler (diğer bacak sabitken; 60 gün, bugün dahil; [R2] A.15): z = +2 için SAHOL ≥ 91,10 ya da AKBNK ≤ 62,78; z = −2 için SAHOL ≤ 82,35 ya da AKBNK ≥ 69,44. Her akşam [SİN] yeniden hesaplar.

**Eski sürüm:** Kullanıcının 1–3 günlük SAHOL/AKBNK sinyali emekliye ayrılır. Aynı çiftte iki sinyal çalıştırılmaz ([PL] §1; [HK] §5 m.6).

### K2. KCHOL↔iştirak sepeti oran dönüşü (isteğe bağlı; varsayılan kâğıt)

**Kanıt [D]:** Bir gün gecikmeyle +128 / +175 bps, t 2,1 / 2,1; maliyet (40 bps) sonrası ~+88 / +135 bps ([VB] #25).

**Kural:**
- Sepet TUPRS, FROTO, TOASO, ARCLK, YKBNK, AYGAZ. AYGAZ'ın VİOP'u yok: sinyal 6 hisseyle hesaplanır, işlem 5 bacakla yapılır.
- Diğer her şey K1 gibi; boyut yarım (KCHOL %5, sepet 5 × %1).
- **Yalnız yeni kesişimde girilir:** z, |z| < 2'den |z| ≥ 2'ye geçtiği ilk kapanış; giriş t+1. Uzun süredir açık "kalıcı" sinyallerin kanıtı karışık: 2010–18 −53 bps (n=35), 2019–26 +272 bps (n=26) ([TC] §2.2; [HK] §3.3).

**Kapılar:** ≥ 5 mn TL hesap, komisyon yön başına ≤ 8 bps, Kural 0. Aksi halde yalnız kâğıt üzerinde kayıt.

**Bugün:** z = +2,23–2,25 (5.11). z 22.10–02.11 arasında 2'nin altına indi (1,21–1,93) ve **03.11'de 2,03 ile yeniden kesti** → kurala göre giriş 04.11 olurdu; bugün bayat → **giriş yok** ([R2] A.11; eski "20.10'dan beri kalıcı" gerekçesi yanlıştı). Kesişim tarihi [SİN] çıktısında tutulur. KCHOL ve ARCLK bilançosu 9.11 akşamı.

**Beklenti:** İşlem başına +40…+90 bps; katkı ~0…+0,15 puan. İlk kapatılacak kol.

### K3. Temettü hak kullanımı öncesi 5 gün (yalnız spot; rejimden bağımsız)

**Kanıt [D]:**
- [BS] §5.3: n=1.109, [−5,−1] ortalama +%1,2, medyan +%0,8.
- [VB] #26: Haftalık kümelemeyle **t 6,5**; ortalama 17 yılın hepsinde pozitif, medyan 2014 ve 2026'da negatif; maliyet sonrası ~+%0,9.
- Kenar yalnız spotta var: VİOP temettüyü önceden fiyatlıyor ([PL] §2).

**Kural:**
- **Evren:** 60 günlük medyan TL hacme göre ilk 100 hisse, dışlama listesi (§4.2) hariç. KAP'taki kâr payı bildirimine göre brüt temettü / son kapanış ≥ %2 ve < %5. (≥ %5 olanlar K3b'nin konusu; K3b canlı değilken K3 bunları da kapsar.)
- **Takvim:** Gün 0 = hak kullanım günü, temettüsüz ilk işlem günü.
- **Alış:** Gün −6'nın kapanış seansında (18:01–18:05) limitli emir; limit = min(gün −7 kapanışı × 1,04; P_son × 1,03) (§3 ortak kurallar). B'nin gün −5'i bir gün geçti; [−5,−1] penceresi gün −6 kapanış girişi ister ([HK] §3.2 m.4).
- **Satış:** Gün −1'in kapanış seansında **risk azaltan satış** (limit = izin verilen en düşük fiyat, §3). Hak kullanımına girilmez, temettü alınmaz. Hisse gün −1'de tabanda kilitliyse pozisyon istemeden hak gününe taşınır; günlükte "kilit" yazılır ve gün 0 kapanışında aynı kuralla satılır ([R1] B1).
- **Stop:** Pencere içinde kapanış giriş × 0,92'nin altındaysa ertesi kapanışta çıkılır [TE].
- **Boyut:** Olay başına %3,5. ≥ 5 mn TL hesapta beta hedge'li olay başına %5. Eşzamanlı en çok 3 olay; aynı kümeden en çok 2.
- **Hedge (≥ 5 mn TL; tercih edilen sürüm):** Toplam K3 nominali × β ≥ 1 F_XU030 nominali (~147 bin TL) ise, aşağı yuvarlanmış kontrat sayısıyla F_XU030 satılır. Hedge maliyeti yalnız (mevduat neti − ima) ≈ 3,3 puan/yıl'ın 7 güne düşen payı. TUPRS, PETKM ve ASELS'te XU030 hedge'i işe yaramaz, hedge'e katılmaz ([PL] §3).
- **11–13.11 kuralı:** Gün −6 = 11, 12 ya da 13.11 ise olay atlanır (A2).

**Beklenti ([R2] A.6):**
- Olay başına net fazla **+%0,2…+%0,5.** +%1,2 **ham** getiridir, piyasaya göre düzeltilmemiştir. XU100'ün ~%20/yıllık driftinin 5 güne düşen ~%0,35'i ve ~30 bps maliyet düşülünce ~+%0,55; %30 iskontoyla ~+%0,4 kalır. Bugünkü engel 7 takvim gününde ~%0,65–0,7 tutar; hedgesiz sürümün R_fazla'sı ancak piyasa engel kadar kazanırsa pozitiftir. **Beta hedge'li sürüm bu varsayıma bağlı değildir; bu yüzden tercih edilir.**
- İsabet %55–65 (medyandan çıkarım); olay kuyruğu −%5…−%10.
- **Uyarı ([VO] §2.3):** Duyurudan hak −1'e kadarki pencerede verim %2–5 kovasının fazla getirisi ≈ 0. [−5,−1] penceresinin %2–5 kovası ayrıca test edilmedi ([BS] §5.3 örneği verim %2–15). K3 küçük ve ilk kapatılacak kollardandır.
- Sezon Mart–Haziran. Kasım–Aralık'ta olay az; kol büyük olasılıkla boş kalır.
- Katkı merkez **+0,3 puan/yıl**, aralık 0…+0,8.

### K3b. Yüksek verimli temettü duyuru koşusu (önceden kayıtlı pilot 01.02.2027; o zamana kadar kâğıt)

**Kanıt:**
- [OB] §0, §8 [DM]: Duyuru verimi ≥ %5 olan nakit temettülerde duyurudan sonraki ilk kapanışta alıp hak −1 kapanışında satmak: XU100'e göre +%8,5, t 11,1, N=400.
- **[VO] §2.3 [D], bağımsız fiyat serisiyle:** Mekanik hata yok; hak günü doğru, verim duyuruda biliniyor (ileriye bakış yok). XU100'e göre +%8,7 (N=361, isabet %74). **Muhafazakâr kıyasla** (aynı evrenin eşit ağırlıklı, temettü dahil toplam getirisi) **+%6,5, medyan +%4,1, t_ay 6,5, isabet %67**; koşulsuz tabandan arındırılmış ≈ +%6,9. 17:00 kesimiyle +%8,4. **2024–26: +%13,5 (N=61).** Hacim ≥ 20 mn TL (N=119): +%10,2, t 8,4. En iyi %5 hariç +%6,3. Girişlerin %81'i Şubat–Mart; medyan 27 işlem günü.
- **Verim kovaları:** %2–5 ≈ 0, < %2 −%1,4 → kural yalnız ≥ %5 ([VO] §2.3; raporun +%5,0 / +%3,4 değerleri kıyas yanlılığıydı).
- **Engel:** Hedgesiz ham getiri ortalama +%8,8, medyan +%4,8. F_XU030 hedge'iyle getiri ≈ TL faizi + BHAR → işlem başına +%6–7 fazla ([VO] §2.3).
- **Açık riskler:** Yalnız gerçekleşen temettüler örnekte (iptal ya da genel kurulda düşürülen teklifler yok); etkinin bir kısmı aynı dönemdeki kazanç açıklaması olabilir; önceden kayıtlı bir test değil (ama %3 ve %8 eşiklerinde de sürüyor).

**Kural (09.11.2026 tarihli hipotez kartı; değiştirilemez):**
- **Evren:** 60 günlük medyan TL hacim ≥ 20 mn TL, dışlama listesi hariç. KAP'taki ilk "Kâr Payı Dağıtım İşlemlerine İlişkin Bildirim"deki brüt nakit temettü / bildirimden önceki kapanış ≥ %5.
- **Giriş:** Bildirim 17:00'den önceyse aynı gün kapanış seansında, sonraysa ertesi gün (18:01–18:05). Limit = min(önceki kapanış × 1,04; P_son × 1,03). Tavan kilidinde atlanır; ertesi gün bir kez daha denenir, sonra olay bırakılır.
- **Çıkış:** Hak −1 kapanış seansında risk azaltan satış. Genel kurul tutarı %20'den fazla düşürür ya da iptal ederse ertesi kapanışta.
- **Stop:** Kapanış giriş × 0,88'in altındaysa ertesi kapanışta [TE].
- **Hedge (Kural 0 sağlanmışsa zorunlu):** Σ(β × K3b nominali) ≥ 1 F_XU030 kontratı (~147 bin TL) olunca aşağı yuvarlanmış kontrat sayısıyla F_XU030 satılır. 1 mn TL hesapta genelde mümkün değil → hedgesiz, boy aynı.
- **Boyut:** Pilot (01.02–31.05.2027) olay başına **%1,25**; eşzamanlı en çok 4; aynı hissede K3 açılmaz. Pilotta ≥ 10 olay ve ortalama R_fazla > 0 ise 2028 sezonunda %2,5.
- **Kasım 2026–Ocak 2027:** Her uygun bildirim aynı alanlarla kâğıt günlüğe yazılır.

**Beklenti:** Olay başına +%3…+%3,5 fazla (muhafazakâr +%6–7'nin yarısı); isabet %60–67; likit evrende sezonda ~6–10 olay. 12 aylık katkı (yarım boy) merkez **+0,3 puan**, aralık 0…+1,2. Gerçekse tam boyda yılda +0,5…+2 puan.

### K4. Kırılım motoru: 52 hafta zirvesi + trend şablonu + %15 iz-stop (rejime bağlı yukarı motor)

**Kanıt:**
- [BT] §5.1 ve [VB] #28, S2 = B52 + TT, iz %15 [D]: 2.073 işlem; aynı gün rastgele likit hisseye göre **+%5,3** (ay-kümeli t 5,1); 17 yılın 15'inde pozitif; isabet %45; kazanç/kayıp 3,3; medyan −%2,9.
- **Kuyruk:** En iyi %5 işlem kârın **~%70'i.** En büyük kazançlar 2026'da −%93…−%98 çöken pump hisseleri (KTLEV, ODINE, HEDEF, PEKGY) → dışlama listesi şart.
- S5 (+ XU100 > SMA200): +%5,7, t 5,4 [D].
- [VB] §2.1: Düzeltilmiş risksiz faizle portföy 2024–26'da engelin **2–8 puan altında.**
- [HK] §3.1: VİOP-47 alt kümesinde 2024 sonrası girişler (n=56) mutlak +%4,15, aynı tutmada rf'ye göre **−%3,3/işlem (−0,22R).** Tüm örneklemde R_fazla ≈ +0,56.
- [BT] §5.2: Top75 evren S2 iz %15'te MaxDD −%27; gerçekçi dolumla ana evrende −%45.
- **Yalnız S2:** B52'nin şablonsuz hali (S1) gerçekçi dolumda MaxDD −%61 ve 2024–26'da rf'nin −18 puan altında ([BT] §5.2). A'nın "S1 yarım boy" kuralı alınmadı.

**Sinyal (t kapanışı), 7 koşulun hepsi:**
1. **B52:** Kapanış > önceki 252 işlem gününün en yüksek kapanışı.
   - **Tarama uyarısı:** `bist_tarama.py`'deki `zirve52` bugünün kapanışını **içeriyor** (`c.iloc[-252:]`). Bu yüzden B52 = "`zirveye` = 0 ve kapanış > önceki günün `zirve52` değeri". Bu planın tetik tablosu (§4.4) bugünü hariç tutan seviyeleri verir.
2. Kapanış > SMA50 > SMA150 > SMA200 (`t_dizilim`).
3. SMA200 > 21 işlem günü önceki SMA200 (`gho200_yukselen`).
4. Kapanış ≥ 1,25 × 52 hafta dibi. Taramanın `t_dip30` eşiği 1,30, test eşiği 1,25: **`dipten` ≥ 0,25 kullanılır.**
5. Kapanış ≥ 0,75 × 52 hafta zirvesi.
6. RS yüzdeliği ≥ 80. Test, en likit 150 içinde 0,4·R3a + 0,2·R6a + 0,2·R9a + 0,2·R12a kullanıyor. Tarama `rs` sütunu 100 hisselik evrende benzer bir yüzdelik; yaklaşık olarak kullanılır ve fark günlükte not edilir. Taramanın `sablon` alanı RS ≥ 70 kullandığı için karar için kullanılmaz.
7. Evren ve dışlama (§4.1–4.2).

**Giriş (t+1 kapanış seansı):**
- Limitli alış (18:01–18:05); limit = min(t kapanışı × 1,06; P_son × 1,03), aşağı fiyat adımına yuvarlanır (§3).
- Tavan kilidinde atlanır; ertesi kapanışta koşullar sürüyorsa yeniden denenir.
- Bilanço kuralı (ortak kurallar).
- 18:05'e kadar erişim yoksa 18:08–18:10'da kapanış fiyatından emir ("geç" kaydı). O da kaçarsa ertesi gün aynı kural; koşullar sürmüyorsa giriş yok. Açılış seansı yedeği kaldırıldı (test edilmemişti).

**Çıkış:**
- **E1, iz-stop:** Kapanış ≤ girişten beri en yüksek kapanış × 0,85 → ertesi gün kapanış seansında **risk azaltan satış** (limit = izin verilen en düşük fiyat, §3); dolmazsa (kilit) her gün aynı kural.
- **E2, süre:** 120 işlem günü (testte de 120); limit = max(önceki kapanış × 0,94; P_son × 0,97). Hedef fiyat ve kısmi kâr alma yok: Kısmi satış tam da kârın geldiği sağ kuyruğu keser ([TA] §2.1).
- **E3, yedek felaket emri:** Pay Piyasası'nda borsa düzeyinde stop emri yok ([BİP]). Aracı kurumun kendi sistemi şartlı emir sunuyorsa tetik = en yüksek kapanış × 0,80, limit = tetik × 0,97; her Cuma güncellenir [TE]. Sunmuyorsa koruma yalnız boyuttur.
- **E4, dışlama:** Hisse VBTS tedbirine girerse, SPK listesine eklenirse ya da fon payı / fiili dolaşım > %20 olursa ertesi kapanışta koşulsuz çıkış [TE].
- **E5, büyük kazanç:** Pozisyon ≥ +%100 kâra ulaşırsa iz-stop %15'ten %10'a iner [TE].
- **E6, bedelsiz:** Pozisyondaki hissede oranı ≥ %500 bir bedelsizin hak günü gelirse hak −1 kapanışında satılır [TE]. Dayanak: [OB] §7, hak sonrası 10 günde −%6,1, t −3,3. Daha düşük oranlarda testteki kural korunur.
- **E7, KRİZ ve kredili uçurum [TE]:** KRİZ günü (§2.2) stop = max(iz-stop, KRİZ günü kapanışı × 0,90). Kredili esneklik uzatılmazsa A4'teki 13.11 kuralı uygulanır ([R1] B4, B5).
- **Aktif ihraççı geri alımı olan isimler (AHGAZ, ENERY):** program durursa ya da tavan tutara ulaşırsa günlüğe yazılır; çıkış kuralı değişmez ([R2] A.3; [OA] §2.3: VİOP dışı geri alımda kenar yok).

**Boyut:** nominal = hesap × r₀ / stop mesafesi.
- **Stop mesafesi:** %15. İki durumda %25: son 3 yılda yılda ≥ 5 limit günü olan isimler (GUBRF, TKFEN, BRSAN, HALKB, SASA, ASTOR, VESTL, HEKTS) ve ATR% > 4,5 ([PL] risk tablosu).
- **Çarpan:** VİOP-47 dışı spot isim × 0,75.
- **Likidite:** Pozisyon ≤ 60 günlük medyan günlük TL hacmin %2'si.

| Rejim | r₀ (işlem başı risk) | Nominal (stop %15) | Azami açık K4 | Ekleme |
|---|---|---|---|---|
| KAPALI | %0,25 (sonda; ölçüm amaçlı) | %1,67 | 2; aynı kümeden 1 | Yok |
| GEÇİŞ | %0,50 | %3,33 | 4 | Yok |
| AÇIK | %0,75 (ölçeklemeyle en çok %1,0; §8.4) | %5,0 | 6 | 1 kez |

**Ekleme (yalnız AÇIK; risk-nötr; etkisi test edilmedi):**
- Koşullar: pozisyon kapanışı ≥ giriş × 1,10; aynı gün yeni 20 günlük kapanış zirvesi; küme, blok ve stres sınırları aşılmıyor.
- Miktar ve zaman: ilk adedin %50'si, t+1 kapanış seansında.
- İz-stop bütün pozisyon için aynı kalır. Giriş 1, ekleme 1,10'da yapılırsa stopta toplam kayıp 0,1475 olur; bu, ilk riskin (0,15) altında ([TA] §2.1; [HK] §3.1).
- Günlükte ayrı satır olarak tutulur.

**Spot mu vadeli mi?** Yalnız VİOP-47'de ve §1.5'teki koşullarla pay vadelisi kullanılır (5.11'de koşul 3'ü sağlayan Aralık pay kontratı yok → K4 spot). Nominal spot formülünü aşamaz. Devir vadeden 3 iş günü önce (Kasım için 25.11). Yeni vadenin günlük hacmi < 20 mn TL ise pozisyon spota taşınır.

**Kümeler:**
- Küme RS'si **giriş filtresi değildir.** Sinyal günü 12 aylık sıralamada ilk 3 kümeden gelen kırılımlar +%4,9, alt yarıdan gelenler +%5,3 verdi ([TA] EK-3; [VD] §5 m.1). C'nin "son 6 kümeden giriş yok" filtresi kaldırıldı.
- Küme sırası yalnız iki işe yarar: slot rekabetinde öncelik ve yoğunlaşma sınırı (§5).

**Beklenti:**
- **KAPALI:** Katkı ≈ 0 (−0,3…+0,3 puan). Amaç veri toplamak ve rejim dönüşünde ilk lideri tutmak.
- **AÇIK:** Rastgele hisseye göre işlem başı +%1…+%3 (%50 iskonto; pump isimleri dışlandığı için daha düşük olabilir). Engele göre R_fazla 0…+0,3; isabet %40–45.
- Kol 50 işlemde gerçek bir kenarla bile ~%26 olasılıkla negatif toplam verebilir ([SE] §3.5). En uzun kayıp serisi 8–13 işlem ([TA] EK-5).

### K5. Özel durumlar (ZPAT, satma ve ayrılma hakkı): yalnız KAP teyidiyle

**Kanıt:**
- Alan çalışılmadı ([VB] §3 m.4). Ağustos–Ekim SPK bültenlerinde 13 ZPAT atfı var.
- **Karşı taraf emsali:** Tera, PEKGY ZPAT yükümlülüğünü yerine getirmedi (SPK 2026/64, 2026/71).

**Kural (hepsi gerekli):**
1. SPK onaylı pay alım teklifi bilgi formu var. KAP'ta fiyat (TL ya da "USD karşılığı, hangisi yüksekse"), başlangıç ve bitiş tarihleri, aracı kurum ve ödeme günü açıklanmış.
2. **Hak sahipliği:** Bilgi formunda "kimler katılabilir" okunur. Teklif "kontrol devrinin kamuya açıklandığı tarihte pay sahibi olanlara" yapılıyorsa, sonradan alınan pay teklife verilemez → **işlem yok.** Zorunlu tekliflerde bilgi formundaki "Pay Alım Teklifinden Yararlanabilecek Pay Sahiplerinin … Belirlenmesinde Esas Alınan Tarih" alanı okunur; tarih bugünden önceyse sonradan alınan pay teklife verilemez (PAT Tebliği md. 11/4; MKK listesi, sonraki satışlar LIFO ile düşülür). **Varsayılan: zorunlu teklifte kayıt tarihi kuralı vardır** ([R2] A.2; AKCNS'de 18.06.2026, KAP 1666313; PEKGY ifadesi SPK 2026/58).
3. Teklif sahibi grup dışı ve mali gücü belgelenmiş (yabancı sanayi şirketi, banka vb.). Grup içi fon krizi teklifleri hariç.
4. Teklif penceresi fiilen başlamış.
5. Spot ≤ teklif × (1 − toplam maliyet − PPF net faizi × kalan gün/365 − %2 güvenlik payı).
6. Pay, teklif süresi içinde aracı kuruma verilen katılım talimatıyla teklife verilir; teklif sonrası tutulmaz.

**Boyut:** Olay başına ≤ %5, toplam ≤ %10. Teklif iptali senaryosunda −%20 varsayımıyla olay riski ≤ %1.

**Beklenti:** Zorunlu tekliflerde kayıt tarihi kuralı yüzünden katkı ~0; yalnız gönüllü teklif ve satma hakkı kalır. Yılda 0–2 olay; katkı merkez **~0**, aralık 0…+0,2 ([R2] A.2).

**Bugün:** AKCNS teklifi 23.09–06.10.2026'da **274,24 TL**'den (22.09 TCMB kuruyla 5,627434 $; 260,25 TL değil) yapıldı ve kapandı (KAP 1666829, 1673963); yararlanma hakkı **18.06.2026** kaydına bağlıydı (KAP 1666313). 1.062 pay sahibi sermayenin ~%15,4'ünü sattı. 184 TL ile 274 TL arasındaki fark yeni alıcıya hiç açık değildi → **AKCNS kalıcı olarak çıkar.** Bugün nitelikli olay yok.

### K6. TL carry, short F_USDTRY (koşullu; Pazartesi 0)

**Kanıt:**
- [VC] #19 [D]: 07/2023–10/2026 yıllık %20,8 USD, ama 2018 −%11,4, 2021 −%30,3, en kötü aylar −%24.
- Sharpe 2,2 örneklem içi; rejim başlangıcı bilinerek seçildi ([VB] §2.6).
- Prim ~13 puana daraldı ([TM] §4.3). Carry ile banka long'u aynı şokta birlikte kaybeder ([VC] §2 m.8).
- B'nin Pazartesi açılışı kaldırıldı. Kaynağı ([KO] §4.2) "brüt rezerv < 160 → çık" diyor ve değer 158,1.

**Açılış kapısı (hepsi):**
1. Swap hariç net rezervin 2 haftalık değişimi ≥ −2 mlr $ ve seviye ≥ 20 mlr $.
2. Haftalık yabancı DİBS akımı ≥ −500 mn $.
3. F_USDTRY ön ay ima basit faizi ≤ politika faizi + 5 puan ([BÜL]; teyitsiz CDS'in yerine, [R1] B5).
4. USDTRY 10 iş günlük artışı yıllıklandırılmış ≤ %30.
5. **Brüt rezerv ≥ 160 mlr $.**
6. Kural 0.

**Kapanış (herhangi biri; ertesi kapanışta):**
- Net rezerv < 15 mlr $ ya da haftalık değişim ≤ −5 mlr $.
- Yabancı DİBS akımı ≤ −1 mlr $/hafta.
- F_USDTRY ön ay ima > politika + 5 puan ya da teyitli CDS > 300.
- 10 günlük hız > %35.
- Brüt rezerv < 160.
- Uzlaşma ≥ giriş × 1,04.
- Siyasi/hukuki şok (erken seçim, TCMB yönetim değişikliği, repo ihalesinin durması): o günün kapanış penceresinde.

**Boyut:**
- ≤ 0,10x nominal, aşağı yuvarlanır: 1 / 5 / 20 mn TL'de **1 / 9 / 38** Aralık kontratı (1 kontrat = 1.000 $ × 52,296 ≈ 52,3 bin TL; [R2] A.9).
- **K6 kapısı kapalıyken hiçbir kolda (K9 dahil) short F_USDTRY yok** ([R1] B2).
- +%30 kur şokunda kayıp ≈ hesabın %3'ü. Ortak strese girer (§5).
- Teminat PPF/DİBS ile verilir. Bir sonraki ayın kontratı kullanılır, vadeden 2 iş günü önce devredilir.
- %10 stopaj, sözleşme kapanışında kesilir.

**Bugün:**
- Kapı koşulları 1, 2 ve 5 sağlanmıyor (net rezerv −6,5 mlr $, yabancı DİBS −750 mn $, brüt 158,1) → **KAPALI.**
- En erken değerlendirme 19.11 (iki olumlu haftalık veriden sonra).
- **Beklenti:** Kapı büyük olasılıkla bir süre kapalı kalacak; merkez katkı ~+0,1 puan. Açık olduğu yarım yılda +0,3…+0,6, şok yılında ~−3.

### K7. Endeks ve küme beta kolu (yalnız T2 = 1 iken)

**Kanıt:**
- XU100 TSMOM12, 2010–26'da rf'nin +6,8 puan üstü. Placebo yüzdeliği 0,86–0,88, yani anlamsız; 2019–26'da yardımcı ([BT] §2; [BS] §4).
- SMA200 ve 50/200 kuralları endekste değer katmıyor ([BT] §7). SMA200 burada yalnız izin kapısıdır.
- Küme rotasyonu (12 ay RS, ilk 3), yanlılıktan arındırılmış EW kümelere göre +5 ± 5 puan; MaxDD −%40/−%48; 2024–26'da hiçbir küme kuralı rf'yi geçmedi ([VD] B2, §5 m.1).

**Kural:**
- **Açılış:** Ay sonunda T2 = 1 **ve** T1 = 1 ise, ertesi gün kapanışa yakın limitli emirle %20 nominal uzun.
- **Araç:** Yarısı F_XU030, yarısı 12 ay RS ilk 3 kümenin en likit 2–3 VİOP dayanağından eşit ağırlıklı sepet. Kümeye giriş şartı: kümenin 3 aylık TL getirisi aynı dönemin TL nakit getirisini geçiyor ([DB] §3.7, "B" filtresi). Geçmeyen kümenin payı F_XU030'a gider. Banka kümesi için §3.10 kuralı geçerli.
- **Çıkış:** Ay sonunda T2 = 0 ya da XU100 SMA200 altında 3 ardışık kapanış → ertesi gün.
- 1x'i aşmaz (2x'te MaxDD −%69; [BT] §2). Akşam seansı kullanılmaz; istisna: KRİZ gecesinde yalnız F_XU030 yarısı akşam seansında azaltılabilir (akşam seansında yalnız endeks ve metal vadelileri var; VİOP Prosedürü §7, [R2] A.14).
- MSCI danışma duyurusunda (A3) K7 kapanır ve MSCI kararına kadar kapalı kalır.

**Bugün:** KAPALI. T2 için XU100 ≈ 15.860 gerekir; 2026 içinde pratikte imkânsız ([TA] §3.2). 12 ay ilk 3 küme RAFİNERİ, HOLDİNG, KOZA_ALTIN; üçünün de 3 aylık getirisi negatif → filtre nakit ([TA] §2.2).

**Beklenti:** Açık olduğu yıllarda nominalin +%4…+%7'si (rf üstü), yani %20'de +1…+1,5 puan. Sahte sinyal yıllarında −1…−3 puan.

### K8. Halka arz katılımı (isteğe bağlı; risk bütçesi dışında)

**Kanıt:** İleriye bakışsız satışla katılımcı primi medyan **+%33–38** (raporun +%45'i, E gününün kapanışta bilinmesi yüzünden ileriye bakış içeriyor); hesap başına yılda ~**8–22 bin TL** ([VO] §3, §5 m.3; [HA] §0, §3b). 3 Eylül'den beri halka arz onayı yok ([HZ] §1a) → bugün 0.

**Kural:**
- Yalnız eşit dağıtımlı arzlara katılınır; talep PPF teminatıyla verilir.
- **Satış:** 18:00'de son fiyat tavan değilse (seri bozulmuşsa) o günün kapanış seansında risk azaltan satış (§3). Bu "E kapanış satışı"dır, medyan +%38 ([VO] §3).
- **Seri bittikten sonra asla alınmaz:** 50–51/53 düştü, medyan −%55; seri sonrası 21 günde medyan −%11,2, 2024–26'da −%17,3 ([VB] #11; [HA] §0).

**Katkı:** 1 mn TL'de +0,8…+2,2 puan, 20 mn TL'de ~0. Merkez beklentiye katılmadı.

### K9. Serbest kol (plan dışı fikirlerin tek kanalı; [R1] B2)

**Neden:** Rejim 0/7 ve uydu büyük olasılıkla Aralık'a kadar boş. En olası kayıp yolu kullanıcının plan dışına çıkmasıdır (öznel %20–35). Örnek: %25 nominal banka vadelisi S4'te −%5…−%6; 0,5x short F_USDTRY Mart 2025 tipi bir kur sıçramasında tek günde −%5,8. Bugünün göz alıcı adayları (banka ve havacılık RS kırılımı) tam Blok 1'dir ([R1] §1 yol A; [HZ] §0 m.2; [VD] B12; [VC] §2 m.4).

**Kural:**
- **Kapsam:** K1–K8 kurallarına uymayan her fikir: küme ya da banka RS kırılımı, haber, sezgi.
- **Araç:** Yalnız VİOP-47 hissesi spot ya da 1x pay/endeks vadelisi. F_USDTRY, opsiyon ve kredili işlem yok.
- **Boyut:** İşlem başı risk (nominal × stop mesafesi) KAPALI'da ≤ %0,25, GEÇİŞ ve AÇIK'ta ≤ %0,5. Nominal ≤ %5; eşzamanlı en çok 2. Açık risk, stres, nominal tavanı, L1 ve Blok 1 sayımına (K4 ile birlikte) girer.
- **Süreç:** Fikir kartı (mekanizma, giriş, stop, çıkış, beklenen süre) 18:45'e kadar günlüğe yazılır; emir ertesi gün kapanış seansında. Stop zorunlu; çıkış risk azaltan satışla (§3). A1–A10 kaçınma kuralları K9'a da uygulanır.
- **Fren:** K9'un birikimli kaybı hesabın %1,5'ine ulaşırsa K9 6 ay kapanır. K1–K9 dışında tek bir işlem (kural_sapmasi = E) → bütün uydu 1 ay kâğıt; ikinci kez 3 ay.
- **Eski lead-lag sinyalleri:** 6.11 itibarıyla açık pozisyonlar kendi çıkış kurallarıyla kapanır; yeni sinyal yalnız §3.11'deki %0,5'lik bütçeyle açılır (K9 bütçesi değil).

**Beklenti:** R_fazla ≤ 0 [Ö]; merkez −0,1 puan, aralık −1,5…+0,3. Amaç getiri değil, plan dışı kaybı hesabın %1,5'iyle sınırlamak (yol A'nın kuyruğu −%5…−%6'dan −%1,5'e iner).

### 3.10 Kaçınma kuralları (bütün kollar; zorunlu akış alfası değil, kayıptan kaçınma)

| # | Olay | Kural | Kanıt |
|---|---|---|---|
| A1 | Konsolide 3Ç son günü, **9.11 akşamı**. Planlı: KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK. Tarihsiz kalanlar: EREGL, ARCLK, KRDMD, ASTOR, GUBRF, HEKTS, OYAKC, CIMSA, TKFEN, TRALT, TRMET, EKGYO, VESTL, ODAS ve **AHGAZ, ENERY, RYSAS** (KAP'ta 3Ç raporu yok). **ENJSA 02.11'de açıkladı** (KAP 1691179) → kısıt yok. Bankalar 19.11 | Bilançosunu **9.11 18:00'den önce KAP'ta açıklamamış** isimlerde 9.11 gecesi pozisyon taşınmaz, yeni giriş yok. İlk karar Salı 10.11 kapanışı; giriş A2'ye tabi | [HZ] §2; [R2] A.3; [R1] B11 a; [TE] |
| A2 | **11–13.11:** MSCI 12.11 01:00; SPK kredili esneklik kararı 12–13.11 bülteninde; esneklik 13.11 seans sonunda bitiyor | 11.11 kapanışında hiçbir kolda yeni giriş yok. 11, 12 ve 13.11 kapanışlarında **yeni K3, K4, K5, K9 girişi yok** (K1 12.11'den itibaren normal; MSCI için A3). İlk giriş: esneklik uzatıldıysa **16.11 kapanışı**; uzatılmadıysa ya da 13.11 seans sonuna kadar karar yoksa A4 | [TA] §2.1 m.6; [R1] B4; [TE] |
| A3 | **MSCI: her gözden geçirme ve her ad hoc Türkiye duyurusu.** Kasım: duyuru 12.11 01:00, yürürlük 30.11 kapanışı. Sonraki: Şubat 2027 (tarihler 1.12'de MSCI takviminden günlüğe). Artışlar dondu, azaltmalar sürüyor | Duyurudan önceki kapanışta yeni giriş yok. Silinen ya da FIF/NOS'u düşürülen hisse yürürlük kapanışına kadar alınmaz; K4/K7/K9'da tutuluyorsa duyuru günü kapanışında risk azaltan satışla çıkılır. K1'de bu hisse yürürlüğe kadar yalnız short bacak olabilir; long bacak gerekiyorsa giriş yok. FIF/NOS listesi kamuya açık değilse yalnız silinenler uygulanır ve günlüğe not edilir. **Danışma duyurusu:** KRİZ (f); MSCI kararına kadar Blok 1 yönlü hakkı 0, K7 kapalı, K4'teki VİOP-47 önceliği askıda. Yürürlükten sonraki gün hisse evrene döner | [VC] #17, §2 m.7; [TM] §4.3 m.6; [R1] B6 |
| A4 | **Kredili esneklik** (%35 → %20) 13.11 seans sonunda bitiyor. Şimdiye kadar **2/2 uzatıldı** (ilk tedbir 2026/60; uzatmalar 2026/68, 2026/78) | **Uzatılırsa:** kural yeni bitiş tarihine aynen uygulanır (uzatma uçurumu kaldırmaz, erteler); oran kısmen artırılırsa (ör. %20 → %25–30) da. **Uzatılmazsa:** K4 girişi 23.11 kapanışından, VİOP-47 dışı long 30.11 kapanışından önce yok; düşen hisse "dipten" alınmaz. 13.11 kapanışında açık VİOP-47 dışı spot pozisyon zarardaysa kararın bilindiği günden sonraki ilk kapanışta (13.11 ya da 16.11) risk azaltan satışla satılır; kârdaysa iz-stop 27.11'e kadar %10 [TE]. K1 normal | [VB] #7; [HZ] §0 m.3; [BT] §4 (kısa vadeli dönüş BIST'te kaybettiriyor); [R1] B4; [R2] A.10 |
| A5 | **Bedelsiz hak günü** | Hiçbir kolda bedelsiz hak gününe yeni pozisyonla girilmez. Hak günü dahil 10 işlem günü yeni alış yok; oran ≥ %500 ise 20 gün (−%7,2). YK duyurusunda, başvuruda ya da SPK onayında **alış yok**: duyuru etkisinin büyük kısmı tavan kilitli günlerde; dolabilir ilk kapanışta alıp 5 gün tutmak −%1,6; onay → hak −1 net −%0,07; başvuru → hak −1, 2024–26 medyan −%2,9 | [OB] §0, §5, §6, §7; **[VO] §2.2 [D]:** hak [1,10] −%3,26 (t −5,5); 2024–26 −%1,45 (t −1,5, zayıflamış) |
| A6 | **Temettü (verim ≥ %5) hak günü** | Hak günü dahil 5 işlem günü yeni alış yok (−%2,1, t −7,7). K3/K3b pozisyonları bilerek hak gününe taşınmaz | [OB] §8 [DM]; [BS] §5.3 ([+1,+5] −%0,6, t −3,9) |
| A7 | **Banka zamanlaması, 10.12 PPK** | Karar anket medyanının (%35) ±25 bp içindeyse ("sürprizsiz indirim"): 11.12.2026'dan itibaren 63 işlem günü (01.01 ve Ramazan Bayramı tatiliyle **~15.03.2027**; bayram günleri takvimden teyit edilir) BANKA kümesinde yeni K4/K9 girişi yarım boy ve en çok 1. K7'nin banka payı F_XU030'a gider; rejim dönüşünün ilk aracı F_XU030 olur, F_XLBNK değil. Şahin sürprizde ya da sabit kararda kısıt yok | [OA] §4.2, §4.5; **[VO] §4.1:** sayılar birebir doğru (6/6 döngü, −%6,3, t −4,2) ama etkin n = 6 → yalnız boyut eğilimi; [R2] A.12b |
| A8 | Bedelli (rüçhan) duyurusu | Kural yok, yalnız bilgi. Duyuru [0,1] −%2,8, sonrasında anlamlı drift yok | [OB] §8 |
| A9 | BIST30 blok kilidi ~03.02.2027'de açılıyor; fon uyumu 31.01.2027; tasfiye ~17.03.2027 | 29.01–05.02.2027 arasında K1'de yeni giriş yok (gerekçe: K1'in AKBNK bacağı blok listesinde, 2,28 mr TL, sermayenin %1'inin altında; SAHOL listede yok). 31.01.2027'ye kadar K3/K3b/K4/K9'da VİOP-47 dışı hisselerde **tek bir fonun** payı / fiili dolaşım ≥ %8 olanlar alınmaz (%8 fon başınadır, aynı kurucuda 2 kat) [TE]. Veri: fonoloji/spk-tasfiye ve KAP pay sahipliği; veri yoksa sonda yarım boy (rapor yayımlamayan fonlarda ~24,9 mr TL bilinmeyen pozisyon). Dışlama listesi en az 17.03.2027'ye kadar geçerli | [VP] T7, T8; [TP] §4.5(b); [R1] B11 b–c; [R2] A.13d |
| A10 | Vade günü | Kasım pay vadelisi yeni pozisyonda kullanılmaz; açık Kasım bacakları en geç 25.11 kapanışında kapanır ya da devredilir. **Aralık bacakları en geç 23.12 kapanışında** (31.12 stopaj değişikliğiyle aynı hafta). Vade gününe pozisyon taşınmaz | [HZ] §1b, §5; [R1] B11 d |

### 3.11 Bilerek kullanılmayanlar

| Fikir | Neden yok | Kaynak |
|---|---|---|
| Kesitsel 12-1 momentum, kısa vadeli dönüş, "düşeni al" | BIST'te başarısız; haftalık kaybedenler kaybetmeye devam ediyor | [BT] §4; [BS] §3.3 |
| Endeks SMA200, 50/200 kuralları (getiri kuralı olarak) | Değer katmıyor | [BT] §2, §7 |
| Sektör endeksi rotasyonu | 2024–26'da her yıl rf altında | [BT] §3 |
| 52 hafta zirvesine yakınlık sıralaması | 2022 çıkarılınca anlamsız (t 1,50 / 0,85) | [VB] #24 |
| S1 (şablonsuz B52) yarım boy (A) | Gerçekçi dolumda MaxDD −%61, 2024–26'da rf −18 puan | [BT] §5.2 |
| "Önce bankalar" rejim kolu (B K2) | n=4 tarihsel örnek; zamanlaması 10.12 indirimini kapsıyor ve [OA] §4 bunun aleyhinde | [HK] §3.2; [OA] §4.2 |
| Olay strangle'ı ve diğer opsiyon alımları (B K3) | BIST'te vol primi test edilmedi; opsiyon alıcılarının ortalaması negatif; uzlaşmalar işlem fiyatlarının ~%30 üstünde (strangle işlemle ~199 puan, uzlaşmayla 311) | [VB] §3 m.6; [VP] A6; [HU] §4 #4 |
| Opsiyon satışı | Kanıt eşiğini geçen test yok; çöküşte yıkıcı | [BS] §8.3 |
| Bedelsiz koşusu (bütün aşamalar) | Hiçbir alış kuralı engeli geçmiyor; 2024–26 negatif | [OB] §0, §6 |
| Geri alım ve içeriden alım taklidi | Kontrol düzeltmeli kenar yok; içeriden alımda işaret ters (60 günde −%3,35, t −1,7). VİOP'lu geri alım adayı (n=41) doğrulanamadı → kullanılmaz; yalnız bilgi bayrağı (AHGAZ, ENERY) | [OA] §0, §2.3; [VO] §4.3; [VB] #18 |
| Yabancı akımına göre işlem veya rejim tetiği | Akım fiyatı izliyor; ileri 8 hafta tahmini zayıf (2021–26 t 1,87, 2024–26 t 1,06) | [OA] §3; [VO] §4.2 |
| PEAD | Literatür, doğrulanamadı → yalnız kâğıt kaydı | [VB] #21 |
| Kredili spot | Örtük maliyet ~%60 | [VB] #3 |
| Halka arzda tavan serisi sonrası alım | 50–51/53 düştü; seri sonrası 21 günde medyan −%11,2 | [VB] #11; [VO] §3 |
| Eski 4 lead-lag sinyali | 2024–26'da t 1,0–1,2. XU030 baz sıçraması 18:10–18:15 ekranı istiyor. SAHOL/AKBNK 1–3 gün → K1 ile değiştirildi. **Diğerleri kâğıt.** 6.11 itibarıyla açık pozisyonlar kendi çıkış kurallarıyla kapanır. Canlı sürdürülecekse toplam açık risk ≤ %0,5 ve bu bütçe K4 sondalarından düşülür ([R1] B2) | [PL] §1, §5 |

---

## 4. Evren, dışlama listesi, kümeler, güncel adaylar

### 4.1 Evren

| Kol | Evren |
|---|---|
| K1 / K2 | İlgili VİOP pay vadelileri |
| K3 / K3b | Tarama evreni (VİOP-47 ∪ BIST100) içinde 60 günlük medyan TL hacme göre ilk 100 |
| K4 | Aynı sırada **ilk 75** (test top75 evreninde MaxDD −%27; [BT] §5.2), ≥ 252 işlem günü geçmişi olan. Öncelik VİOP-47; diğerleri spot × 0,75 |
| K7 | F_XU030 ve küme sepetleri için VİOP-47 |

Likidite sırası ([TC] §4.1, 248 hisselik önbellek): ENERY 36, ENJSA 48, AHGAZ 63 → K4'e uygun. ISDMR 106, GLYHO 136 → dışında. [SİN] (5.11, VİOP-47 ∪ BIST100 içinde 60 günlük medyan TL hacim, HisseTekil): ENERY 35, ENJSA 43, RYSAS 51, AHGAZ 54 → dördü de K4 evreninde; TRGYO 85 ve GLYHO 97 dışında. Sıra her akşam yeniden hesaplanır.

### 4.2 Dışlama listesi (hiçbir kolda uzun yok; açıksa ertesi kapanışta çıkılır)

1. **SPK suç duyurulu 13 hisse:** KTLEV, GUNDG, DSTKF, OZATD, TRHOL, ODINE, VSNMD, IEYHO, ALKLC, ANELE, PASEU, SELEC, MANAS ([VP] T10).
2. **Fon payı / fiili dolaşım > %20 (arz baskısı):** PASEU, KTLEV, ANELE, TEHOL, DSTKF, IEYHO, TMPOL, ODINE, ISVEA, MAGEN, BALSU, ISKPL, DAGI, INFO ([VP] T6). Ayrıca TRHOL, OZATD, GUNDG, PEKGY, SKYLP, SELEC, KARCL ([TP] §4.5). GLRMK: Pusula payı fiili dolaşımın %22'si ([TP] §6).
3. **Tera / Pusula / Hedef grubu ve kayyumlular:** TERA, TEHOL, TRHOL, HEDEF, HDFGS, DSTKF, BIGEN ([TP] §4.4, §6).
4. **Dinamik (her girişten önce kontrol):**
   - VBTS tedbirli hisseler (KAP / Borsa "Tedbirli Hisseler", her Cuma ve giriş günü).
   - Halka arzdan bu yana < 252 işlem günü.
   - Son 60 işlem gününde ≥ 3 kez ±%9,5'te kapanan (kilit/pump vekili; [VB] #27).
   - MSCI Kasım çıkarma veya azaltma listesi (30.11 kapanışına kadar).
   - Bedelsiz ve temettü hak sonrası pencereleri (§3.10 A5–A6).
   - Aynı hisse başka bir kolda ters yönde açık.
5. **Yalnız VİOP için dışlananlar** (spotta K4'e uygun olabilir): Aracı kurum teminatı ≥ %50 olanlar (QNB 3.11: ASTOR, HALKB, VESTL %100; GUBRF %50; [VB] #16). Gidiş-dönüş makası > 20 bps olanlar (HEKTS 36, SASA 43 bps; [PL] risk tablosu).

### 4.3 Kümeler ve bloklar ([DB] §1, §5; [VD] B12)

| Blok (risk sayımında) | Kümeler ve VİOP'lu ana üyeler |
|---|---|
| **Blok 1: büyük finans ve beta** (korelasyon 0,77–0,79) | BANKA (AKBNK, GARAN, YKBNK, ISCTR, VAKBN, HALKB, TSKB), HOLDİNG (KCHOL, SAHOL, DOHOL, ALARK, TKFEN; AGHOL, GLYHO), HAVACILIK (THYAO, PGSUS, TAVHL), TELEKOM (TCELL, TTKOM), GYO (EKGYO) |
| **Blok 2: küçük-orta tema** | ELK_EKİPMAN (ASTOR…), YENİLENEBİLİR, TEKNOLOJİ, ELK_ÜRETİM (AKSEN, ODAS) |
| **Blok 3: sanayi** | ÇİMENTO (CIMSA, OYAKC), OTO_YAN, KİMYA (SASA), CAM (SISE), BEYAZ_EŞYA (ARCLK, VESTL), SAĞLIK |
| **Ayrıştırıcılar** (her biri ayrı) | RAFİNERİ (TUPRS, PETKM; AYGAZ): bankayla fazla getiri korelasyonu −0,42, beta 0,54. SAVUNMA (ASELS): −0,35. KOZA_ALTIN (TRALT, TRMET): ~0 |
| **Diğer** (her biri ayrı) | ÇELİK (EREGL, KRDMD, BRSAN; ISDMR), PERAKENDE (BIMAS, MGROS, SOKM), OTOMOTİV (FROTO, TOASO, DOAS), GIDA (ULKER, AEFES, CCOLA), GÜBRE (GUBRF, HEKTS) |
| **Bu plan:** ENERJİ_DAĞITIM | ENJSA, AHGAZ, ENERY: aynı iş (gaz/elektrik dağıtımı). Korelasyonu ölçülmedi; ihtiyaten **tek küme** ([TA] §4.3). AHGAZ ile ENERY ayrıca **tek isim**: aynı grup (Ahlatcı) ve 17.09'dan beri neredeyse her gün ihraççı geri alımı (azami 2'şer mr TL; KAP 1693367, 1693368) → "aktif geri alım" bayrağı; RS 97–98 liderliğinin bir kısmı ihraççı alımı ([R2] A.3) |

- **Güncel küme durumu:** 12 ay RS ilk 3 RAFİNERİ (+%26,5), HOLDİNG (+%23,9), KOZA_ALTIN (+%18,9). 126 günlük RS kırılımı BANKA ve HAVACILIK. Filtreli kurallar nakitte. Düşen piyasada RS liderliği büyük ölçüde düşük beta demektir ([VD] §5 m.3).
- **Çift kolları:** K1/K2 piyasa-nötr oldukları için Blok 1 sayımına girmez (K9 girer). Ama ikisi aynı anda açıksa Blok 1'in yönlü pozisyon hakkı yarıya iner ([TC] §4.3).

### 4.4 Güncel adaylar (05.11 kapanışı; Cuma 6.11 ve Pazartesi kapanışıyla yenilenir)

**Nitelikli (giriş koşulu bugün sağlanmış): yok.**

**Bekleyenler** (05.11 değerleri; 6.11 ve sonrası için [SİN] çıktısı esas):

| Kol | Aday | Tetik (kapanış >) / koşul | Son | Gereken | Not |
|---|---|---|---|---|---|
| K4 | **ENJSA** (VİOP-47) | **127,00** (17.04.2026 zirvesi) | 119,30 | +%6,5 | TT 7/7, RS 93. 3Ç bilançosu **02.11'de açıklandı** (KAP 1691179) → Pazartesi kapanış sinyali Salı kapanışında girişe uygun. Pay vadelisi ima oranı anormal (Kasım −%10,4, Aralık %9,8) → **spot**. β 0,60 |
| K4 | **AHGAZ / ENERY** (spot; **tek isim**) | **48,70 / 14,60** | 46,00 / 13,80 | +%5,9 / +%5,8 | TT 7/7, RS 98 / 97; × 0,75. **Aktif ihraççı geri alımı.** 3Ç raporu yok → 9.11 akşamı (A1); ilk karar 10.11 kapanışı; giriş A2/A4'e tabi (en erken 16.11) |
| K4 | RYSAS (spot) | 30,28 | 26,68 | +%13,5 | TT 7/7, RS 96; likidite sırası 51 ([SİN]). 3Ç raporu yok (9.11 akşamı); bist_test evreninde yoktu ([VB] §2.4) |
| K4 izleme (TT eksik) | KCHOL | 225,50 | 202,30 | +%11,5 | 6/7 (fiyat < SMA50 211,11); Blok 1; bilanço 9.11 |
| K4 izleme | BIMAS | 433,75 | 369,25 | +%17,5 | 6/7; bilanço 9.11 |
| K4 izleme | TUPRS | 409,90 | 331,75 | +%23,6 | 6/7; ayrıştırıcı küme; bilanço 6.11 akşamı |
| K4 izleme | GARAN | 158,59 | 142,00 | +%11,7 | 3/7 → kırılsa bile S2 değil, **giriş yok** |
| K1 | SAHOL↔AKBNK | \|z\| ≥ 2 | z −0,72 | — | Tam tetikler §3 K1 |
| K2 | KCHOL↔sepet | Yeni kesişim | z +2,23 (03.11 kesişimi bayat) | — | Giriş yok |
| K3 | KAP: 30 gün içindeki hak kullanımları | Verim %2–5, ilk 100 | — | — | Cuma akşamı taranır |
| K3b | KAP: verim ≥ %5 ilk bildirimler | Hacim ≥ 20 mn TL | — | — | Kâğıt (pilot 01.02.2027) |
| K5 | — | KAP'ta açık teklif + "Esas Alınan Tarih" | — | — | AKCNS kapandı → yok |
| K6 | Carry | Kapı (6 koşul) | 3 koşul sağlanmıyor | — | En erken 19.11 |
| K7 | Endeks/küme | T1 ve T2 | 0 / 0 | — | — |
| K9 | Serbest kol | Fikir kartı (§3 K9) | — | — | Banka/havacılık RS kırılımı fikri yalnız buradan |

**Kural:** ENJSA ile AHGAZ/ENERY aynı küme (ENERJİ_DAĞITIM); AHGAZ ile ENERY ayrıca tek isim. KAPALI'da kümeden 1 pozisyon: aynı gün tetiklenirlerse ENJSA (VİOP-47 önceliği). GEÇİŞ'te ikinci pozisyon AHGAZ ya da ENERY'den yalnız biri; likidite sırası yüksek olan ([R2] A.3; eski "AHGAZ 98 > ENERY 97" kuralı silindi).

---

## 5. Risk limitleri

| Limit | KAPALI | GEÇİŞ | AÇIK | Gerekçe |
|---|---|---|---|---|
| K4 işlem başı risk r₀ | %0,25 | %0,50 | %0,75 (en çok %1,0, §8.4) | Tıraşlanmış SR'nin ≤ ¼ Kelly'si ([SE] §3.3, §5.3) |
| K4 azami açık pozisyon | 2 | 4 | 6 | — |
| Küme başına yönlü pozisyon | 1 | 2 | 2 | Küme tek bahis; ρ 0,8'de 5 pozisyon ≈ 1,19 bahis ([SE] §3.6) |
| Blok 1 yönlü pozisyon | 1 | 2 | 3 | Korelasyon 0,77–0,79 ([VD] B12) |
| Tek hisse spot nominal | %3,5 | %3,5 | %7,5 (ekleme dahil) | 3 ardışık taban (−%27): ≤ %1 / ≤ %2 |
| **Toplam açık stop riski** (K1 felaket stopu + K3/K3b stopları + K4 r₀ + K5 olay riski + K6 nominal × %4 + K9 riski) | **%2,5** | %3,5 | %5,5 | [TC] §5; [TB] §5 |
| **Stres tavanı** (her Cuma) | **%6** | %8 | **%10** | A'nın %60 brüt sınırının yerine bağlayıcı ([HU] §5 m.2) |
| VİOP başlangıç teminatı | ≤ min(%15; L1) | ≤ min(%20; L1) | ≤ min(%25; L1) | L1: ≤ (PPF − spot uydu) / 3; L2 küçültme sırası; L3 fazla teminat (§1.3 m.6; [R1] B3) |
| Spot uydu nominali | ≤ %15 | ≤ %25 | ≤ %40 | Aşacak yeni giriş öncelik sırasıyla reddedilir ([R1] B10) |
| K9 serbest kol | risk ≤ %0,25/işlem; nominal ≤ %5; en çok 2 | risk ≤ %0,5 | risk ≤ %0,5 | Birikimli −%1,5 → K9 6 ay kapalı ([R1] B2) |
| Net endeks betası (Σ β × nominal) | ≤ +%10 | ≤ +%25 | ≤ +%40 | — |
| Aylık uydu kaybı (çekirdeğe göre) | −%2,5 → ay sonuna kadar yeni giriş yok | −%2,5 | −%3 | — |
| Birikimli uydu düşüşü (çekirdeğe göre) | −%4 → açık yönlü pozisyonlar ertesi kapanışta yarıya (K1'in iki bacağı birlikte) ve yeni boylar 3 ay yarım. −%6 → uydu kapanır, 3 ay kâğıt | aynı | −%6 → yarıya; −%10 → uydu kapanır | [SE] §5.2 m.8 küçük ölçekli uyarlama |
| Kredili işlem, opsiyon satışı; K6 kapısı kapalıyken short F_USDTRY | Yok | Yok | Yok | [VB] #3; [BS] §8.3; [R1] B2 |

**Stres formülü** (B'nin formülü, C'nin senaryosu; [TB] §5; [TC] §5):

Stres_TL = 0,19 × (Blok 1 dışı uzun hisse + endeks nominali) + 0,25 × (Blok 1 uzun nominali) + 0,30 × (short F_USDTRY nominali) + 0,15 × (çift kollarında tek bacak nominali) + 0,05 × (beta hedge'li K3 nominali) − (tanımlı riskli korumanın azami ödemesi; bu planda 0).

- Varsayımlar: 2 ardışık taban (−%19), bankalar −%25, USDTRY +%30, çift bacağı −%15.
- Örnek (KAPALI, 1 mn TL, [R2] A.13a düzeltmesi): K1 (tek bacak 75 bin) → 11,3 bin; K3 3 × 35 bin hedgesiz → 20 bin; K5 50 bin → 9,5 bin. Stres **~41 bin = %4,1 < %6.** Açık stop riski 0,6 + 0,84 + 1,0 = **%2,44**: %2,5 tavanına dayandığı için K4 sondaları ve K9 öncelik kuralıyla reddedilir. K5 yoksa (bugün yok) iki K4 sondası sığar: 0,6 + 0,84 + 0,5 = %1,94; stres ~38 bin.
- AÇIK'ta çiftler açıkken toplam uzun nominal en çok ~(%10 − ~%2) / 0,19–0,25 ≈ **%30–40.** A'nın %60'ı fiilen bu formülle sınırlanır.

**Bütçe ya da tavan bağlayınca öncelik:** K3b > K1 > K3 > K5 > K4 > K2 > K9 > K6. K7 yalnız AÇIK'ta ve en sonda. Öncelik yalnız yeni girişi reddeder; açık pozisyon küçültülmez (L2, KRİZ ve −%4 kuralı hariç).

**Limit kilidi:**
- Pay ve VİOP günlük limiti ±%10 (Pay Piyasası fiyat marjı %10; kapanış seansında ayrıca son fiyat ±%3; [BİP]). Taban serisinde stop dolmaz. 2026'da ODINE 29 ardışık taban yaptı ([VB] #27).
- Spot kilitliyken pay vadelisi olayların %83'ünde kilitli ([PL] §2). Pay vadelisi çıkış yolu değildir.
- Bu yüzden koruma boyutla yapılır: tek hisse sınırı, dışlama, likidite filtresi, %25 stop mesafesi.
- Rutin gece hedge'i yapılmaz: 1–3 günlük riskin ~%11'i gecede oluşuyor ([PL] §3).

**En kötü hafta (bu kurulumla, 9–13.11 ve 16–20.11):**
- İki K4 sondası iki taban: 2 × %1,67 × %19 ≈ −%0,6.
- Bir K1 bacağı −%15 gap: −%1,1.
- Toplam ≤ ~**%1,8**; %6 stres tavanının içinde. Bu, risk azaltan satış kuralıyla (§3) kilitsiz günlerde stopların dolduğunu varsayar; kilit dizileri çözümsüzdür, onlara karşı koruma boyuttur.
- Pazartesi uydu pozisyonu olmadığı için ilk hafta pratikte ~0.

---

## 6. Uygulama

### 6.1 Kural 0 ve aracı kuruma yazılı sorular

**Kural 0:** VİOP nakit teminatı faiz kazanmıyorsa **ve** PPF/DİBS teminat olarak kabul edilmiyorsa hiçbir VİOP kolu açılmaz (K1, K2, K6, K7, vadeli finansman, K3 hedge'i). Nakit teminat TLREF'in %80'inden az kazanıyorsa VİOP kollarının boyutu yarıya iner. Gerekçe: boştaki teminatın maliyeti teminat × ~%33 ([SE] §5.1 sıra 0; [VC] §2 m.2).

**Cevap gelene kadar:** Yalnız spot kollar (K3 hedgesiz, K4 spot, K5, K9 spot) açılabilir. Pazartesi için bir son saat yok ([HU] §3).

**Aracı kurum ve saklama ([R1] B7):**
- Kurum: mevduat bankası iştiraki ya da SPK tedbiri altında olmayan büyük bir aracı kurum. Emsal: Tera Yatırım'ın lisansları 26–27.10.2026'da iptal edildi ([TP] §4.1 takvim); TRHOL dosyasında 24 lisans iptal edildi ([KK] §2.4).
- Mevduat dilimleri doğrudan bankada; PPF banka kanalından (20 mn TL'de ≥ 2 kurum).
- Aracı kurumda yalnız L1–L3'ün gerektirdiği VİOP teminatı ve açık spot pozisyonlar durur; boştaki nakit gece aracı kurumda kalmaz, PPF'ye geçer.
- 20 mn TL hesapta spot ve VİOP iki ayrı kurumda.

**Sorular** (Cuma akşamı e-postayla; [TC] §6.3, [TB] §1.3, [R1] ve [R2] birleşimi):
1. VİOP nakit teminatı nemalandırılıyor mu? Oranı ne (TLREF'in yüzdesi)?
2. PPF katılma payı ve DİBS VİOP teminatı olarak kabul ediliyor mu? Kesinti oranları ne?
3. Kurum teminat oranları: F_SAHOL, F_AKBNK, F_KCHOL, F_TUPRS, F_FROTO, F_TOASO, F_ARCLK, F_YKBNK, F_ENJSA, F_XU030, F_USDTRY. SAHOL–AKBNK çiftinde mahsup var mı? (Takasbank asgarisi XU030 %11,4, pay vadelileri %12,7–17,0; QNB örneği XU030 %20, çoğu pay vadelisi %33,3; [VB] #16, [HZ] §5.)
4. Komisyon, yön başına, BSMV ve borsa payı dahil, spot ve VİOP ayrı. Kapılar: VİOP ≤ 5 bps/bacak/yön (K1), ≤ 8 bps (K2); spot ≤ 15 bps (K3).
5. Kapanış seansına özel emir ya da dengeleyici (imbalance) emir sunuyor musunuz; sabahtan girilebiliyor mu? Sürekli işlemden aktarılan emirlere kapanış seansının ±%3 marjı nasıl uygulanıyor? ([R2] A.1)
6. VİOP'ta borsa düzeyindeki Şarta Bağlı (SAR) emirleri iletiyor musunuz; hangi geçerlilik türleriyle (GUN, IKG, TAR)? Pay Piyasası için kurum içi şartlı (stop-limit) emir var mı? ([R2] A.14)
7. VİOP Strateji (STJ) emirlerini (vade devri, mümkünse iki farklı dayanaklı çift) iletiyor musunuz?
8. 9–30.11 arasında alınacak DİBS'te stopaj %0 mı? Yazılı olarak.
9. Pay vadelisinde vade öncesi zorunlu kapatma ve fiziki teslimat süreci; son işlem günü.
10. ZPAT'a katılım talimatı kanalı ve son saati; F_USDTRY %10 stopajında zarar mahsubu.
11. Kapanış seansına "izin verilen en düşük fiyat" (taban fiyatı ya da son fiyat × 0,97) ile satış emri kabul ediliyor mu; sabahtan girilebiliyor mu? ([R1] B1)
12. Yatırımcı Tazmin Merkezi kapsamı nedir; nakit bakiye nerede ve hangi hesapta tutuluyor? ([R1] B7)

### 6.2 Emir tipleri ve saatler (TSİ; [HZ] §5; [BİP])

| İş | Seans | Emir | Ne zaman |
|---|---|---|---|
| Spot giriş (K3, K3b, K4, K5, K9) | Kapanış seansı, emir toplama | Limitli; limit = min(plan limiti; P_son × 1,03). Plan limitleri: K3/K3b önceki kapanış × 1,04; K4 t kapanışı × 1,06 | 18:01–18:05; kaçarsa 18:08–18:10 kapanış fiyatından ("geç") |
| Spot risk azaltan çıkış | Kapanış seansı | Limit = max(taban; P_son × 0,97) → müzayede fiyatından dolar; dolmazsa kilit, ertesi gün aynı | 18:01–18:05 |
| Spot acil olmayan çıkış (K4 E2) | Kapanış seansı | Limit = max(önceki kapanış × 0,94; P_son × 0,97) | 18:01–18:05 |
| VİOP çift girişi (K1, K2) | Normal seans | Karşı fiyat ± %0,3 → 18:05'te ± %0,6; 18:08'de tek bacaksa F_XU030 hedge | 17:50 kontrol; 17:55–18:10 |
| VİOP çıkışları (K1, K2, K6, K7, K9, hedge) | Normal seans | ± %0,3 → 18:05'te ± %1 → 18:08'de fiyat limiti | 17:55–18:10 |
| VİOP K6 / K7 / hedge girişi | Normal seans | Limitli, kapanışa yakın | 17:50–18:05 |
| Vade devri | Normal seans | STJ (strateji) emri, yoksa iki limitli emir | Kasım en geç 25.11; Aralık en geç 23.12 |
| Şartlı emir | — | VİOP'ta borsa düzeyinde SAR; Pay Piyasası'nda yalnız aracı kurum sistemiyle (K4 E3) | Cuma 18:30 güncellenir |
| Piyasa emri | — | **Hiç kullanılmaz** (VİOP'ta 1.3.2021'den beri yok) | — |
| Akşam seansı (19:00–23:00) | Yalnız endeks ve metal vadelileri | Kullanılmaz. İstisna: KRİZ gecesinde K7'nin F_XU030 yarısını ya da K1 tek bacak hedge'ini azaltmak | — |

### 6.3 Günlük ve haftalık rutin

**Her işlem günü iki adım** (tek sayfalık sıra [RUT]; [R2] A.4):
1. **18:15–18:45, spot:** `python3 -I kod/bist_sinyal.py --veri ~/bist_veri --cikti tarama` → rejim, KRİZ (a)–(d), K4 tetikleri ve iz-stoplar, küme sırası, K1/K2 z-skorları ve kesişim tarihleri. Ertesi günün spot emirleri ve VİOP çift emirleri hazırlanır, günlüğe yazılır. K9 fikir kartı varsa 18:45'e kadar.
2. **20:45 sonrası, VİOP:** Bülten CSV'si 20:28–20:49 TSİ'de yayımlanıyor; pay ve USDTRY vadelilerinde uzlaşma 18:55 sonrası ilan ediliyor (VİOP Prosedürü Ek-3). Betik yeniden çalıştırılır: XU030 ima oranı ve nakit-taşıma kuralı (§1.5), F_USDTRY ön ay ima oranı (KRİZ e, K6), pay vadelisi ima oranları. VİOP kararları zaten ertesi gün uygulandığı için gecikme kararı değiştirmez. Bülten henüz yoksa betik bir önceki bülteni kendi tarihindeki spotla eşleyip "BAYAT" diye işaretler.

**Bildirim:** [SİN]'in bekleme listesindeki her hisse için kapanış bazlı alarm (ör. "BIST:ENJSA, Kapanış > 127,00, bar kapanışında bir kez"). XU100 > SMA50 ve > SMA200, XBANK > SMA200 alarmları da kurulur. Alarmlar 18:15'te okunur ([TA] §2.1 m.8).

**Haftalık, Cuma 18:30 (~45 dk):** rejim, stres, açık risk, L1, dışlama listesi (VBTS, MSCI, bedelsiz/temettü takvimi), K6 kapısı, mevduat dilimi, yedek felaket emirleri. Perşembe 14:30 rezerv ve yabancı DİBS verisi, ayın 3'ünde TÜFE `makro.json` dosyasına işlenir.

### 6.4 Maliyetler ve kol kapatma eşikleri

| Kalem | Değer | Kaynak |
|---|---|---|
| Borsa payı | Endeks vadeli on binde 0,4; pay ve döviz vadeli on binde 0,3 | [HZ] §5 |
| Aracı kurum komisyonu | Banka liste fiyatı on binde 8–10; aktif bireyde on binde 1–4 (teyitsiz); üzerine %5 BSMV | [HZ] §5 |
| Test maliyet varsayımları | K1 20 bps, K2 40 bps gidiş-dönüş; K4 25 bps (50 bps streste yılda −1,4 puan); K3 ~30 bps | [VB] #25, §2.6 |
| **Kol kapatma eşikleri** (yön başına, BSMV ve borsa payı dahil) | VİOP > 5 bps → K1 kâğıt ([R2] A.5). > 8 bps → K2 kâğıt. Spot > 15 bps → K3 kapalı. K4 toplam gidiş-dönüş > 40 bps → yalnız VİOP-47 | [TC] §6.2; [TA] §6 |
| Makas | Kasım kontratları dar; Aralık sığ (5.11 hacim SAHOL 22 mn, KCHOL 30 mn, AKBNK 118 mn TL) | [TC] §6.2 |
| Teminat fırsat maliyeti | Faizsiz nakitte yılda teminat × ~%33 | Kural 0 |

### 6.5 Vergi (birey)

| Kalem | Stopaj | Kaynak |
|---|---|---|
| BIST pay alım-satım kazancı | %0 (GVK geçici 67, 31.12.2030'a uzatıldı) | [VC] #9 |
| Pay ve pay endeksi VİOP | %0 | [VC] #7 |
| F_USDTRY ve diğer VİOP | %10, sözleşme kapanışında; zarar %0'lı hisse kazancından düşülemez | [VC] #7; [TB] K1 |
| PPF, ≤ 6 ay mevduat | %17,5 (31.12.2026'ya kadar) | [VC] #6 |
| DİBS | Yalnız muafiyet döneminde alınana %0 | [VC] #8 |
| Temettü | K3/K3b hak kullanımından önce sattığı için temettü alınmaz | — |

Beyan yükümlülüğü mali müşavirle teyit edilir; bu plan bunun bağımsız teyidini yapmadı.

### 6.6 Kayıt

- **Günlük işlem defteri:** tek tablo; alanlar §8.2.
- **Günlük NAV:** iki satır, çekirdek ve uydu.
- Her akşamın [BÜL] dosyası ve tarama çıktısı arşivlenir.
- Aylık ekstreler (aracı kurum, MKK e-Yatırımcı) ve stopaj belgeleri saklanır.
- **Hipotez kartları (§8.3)** ilk işlemden önce tarihli kaydedilir. Kart değişirse yeni hipotez sayılır; eski işlemlerle karıştırılmaz.

---

## 7. Takvim: gün gün 6–13.11 ve Kasım sonuna kadar

### 7.1 Cuma 6.11 akşamı ve hafta sonu

1. 18:20 sonrası `bist_sinyal.py` (6.11 kapanışı; komut §6.3). §4.4 tetikleri, TT puanları, SMA50/200, XBANK, K1/K2 z-skorları güncellenir. Betik 6.11 seans sonrası TUPRS, ENKAI, ULKER, BRSAN bilançolarından önce kapanışı yakalar.
2. **20:45 sonrası** betik yeniden çalıştırılır ya da `viop_20261106.csv` indirilir (Ek A). F_XU030 Aralık uzlaşmasından ima oran yeniden hesaplanır; Pazartesi kararında bu değer kullanılır.
3. K1/K2 z-skorları 6.11 kapanışıyla.
4. KAP taraması:
   - 9.11–11.12 arasındaki temettü hak kullanımları (verimleriyle).
   - Açık ZPAT'lar ve bilgi formlarındaki "Esas Alınan Tarih" (AKCNS kapandı, çıkarıldı).
   - Bedelsiz hak günleri (kaçınma listesi).
5. Aracı kurum seçimi (§6.1) ve 12 soru.
6. En az 2 bankadan 32 gün mevduat teklifi. PPF izahnamesinden ücret, ters repo karşı tarafı ve emir saat sınırı (çoğunda 13:30; teyit).
7. Dışlama listesi emir ekranında "yasak" olarak işaretlenir. Günlük şablonu, hipotez kartları ve K9 fikir kartı şablonu tarihlenir.
8. Ölçü birimi (TL engeli ya da USD) yazılı seçilir (§9.2).
9. `makro.json` 05.11 değerleriyle kurulur ([RUT]).

### 7.2 9–13 Kasım

| Gün | Saat | Olay ([HZ] §1a) | Yapılacak | Yapılmayacak |
|---|---|---|---|---|
| **Pzt 9.11** | 09:00–12:00 | Konsolide 3Ç son günü; Hazine ihaleleri | Çekirdek: mevduat 1. dilim %15 (32 gün, doğrudan bankada), PPF %85. DİBS yalnız yazılı %0 teyidiyle | Gün içi ekran yok |
| | 18:15 / 20:45 | Akşam bilanço yağmuru (A1) | Rutin. Bilançosunu **9.11 18:00'den önce** açıklamış bir isimde K4 tetiği gelirse (ör. ENJSA > 127,00) Salı kapanış seansına emir. K1'de \|z\| ≥ 2 ise Salı 17:50/17:55 emirleri | A1 listesindeki isimlerde emir yok |
| **Sal 10.11** | 10:00 / 16:30 | Eylül sanayi üretimi; ABD Ekim TÜFE | Eylem yok | Bilanço gap'i kovalanmaz ([BS] §3.3) |
| | 18:01–18:05 | — | Pazartesi sinyali varsa giriş | — |
| | 18:15 | Bilanço sonrası ilk temiz kapanış | Pazartesi akşamı açıklayanlar (AHGAZ/ENERY, RYSAS, KCHOL, BIMAS…) için K4 yeniden değerlendirilir. Sinyal varsa giriş en erken **16.11** (A2) | — |
| **Çar 11.11** | kapanış | MSCI 12.11 01:00 | Yalnız rutin ve kayıt | **Hiçbir kolda yeni giriş yok** |
| **Per 12.11** | 07:00 | MSCI sonuçları | Çıkarılan ve ağırlığı düşen hisseler yürürlüğe kadar evrenden çıkar; elde varsa kapanışta satılır (A3) | MSCI akışına karşı işlem yok |
| | 10:30 | TCMB Enflasyon Raporu | Bilgi | — |
| | 14:30 | Rezerv + haftalık menkul kıymet | `makro.json`; M1 (1. hafta), K6 kapısı, brüt rezerv. **Swap hariç net rezerv haftalık değişimi yine ≤ −5 mlr $ ise KRİZ (d)** → 5 işlem günü yeni giriş yok, açık pozisyon eylemi (§2.2) | — |
| | 18:01–18:05 | — | Yalnız risk azaltan çıkışlar; K1 normal | Yeni K3/K4/K5/K9 girişi yok (A2) |
| | akşam | SPK bülteni | Kredili esneklik kararı okunur | — |
| **Cum 13.11** | 10:00 | Ödemeler dengesi | Bilgi | — |
| | 18:01–18:05 | Esneklik seans sonunda bitiyor | Uzatılmadığı 12.11 akşamı belliyse VİOP-47 dışı zarardaki pozisyonlar satılır (A4) | Yeni K3/K4/K5/K9 girişi yok (A2) |
| | akşam / 18:30 | SPK bülteni (karar 13.11'deyse) | Haftalık gözden geçirme; stres; L1; mevduat 2. dilimi Pazartesi | — |

### 7.3 16–30 Kasım

| Tarih | Olay | Plan |
|---|---|---|
| Pzt 16.11 | Mevduat 2. dilim | Esneklik uzatıldıysa yeni girişler bu kapanıştan itibaren serbest (A2). Uzatılmadıysa A4: K4 girişi yok (23.11'e kadar), VİOP-47 dışı long yok (30.11'e kadar); zarardaki VİOP-47 dışı pozisyon satılır |
| 18.11 | FOMC tutanakları (tahmini) | Bilgi |
| Per 19.11 | Banka konsolide son günü (HALKB); 14:30 rezerv (2. hafta) | Bilançosu gelecek bacakta K1 girişi yok. M1 2. hafta; KRİZ (d) kontrolü; K6 kapısının ilk olası açılışı |
| 13 veya 20.11 | Kasım Piyasa Katılımcıları Anketi (tarih teyitsiz) | 10.12 için anket medyanı not edilir (A7 eşiği) |
| Pzt 23.11 | Mevduat 3. dilim | A4 uygulanıyorsa K4 girişleri bu kapanıştan serbest |
| **Çar 25.11** | Kasım pay vadelisi | Açık Kasım bacakları kapanışta kapatılır ya da devredilir (A10) |
| **Per 26.11** | 14:30 rezerv (3. hafta) | **M1 olası 1.** T3 ve M4/M5'ten biri de 1 ise GEÇİŞ 27.11'den geçerli |
| Cum 27.11 | TCMB Finansal İstikrar Raporu | Haftalık gözden geçirme; A4 uygulanıyorsa kârdaki VİOP-47 dışı pozisyonların %10 iz-stopunun son günü |
| **Pzt 30.11** | VİOP Kasım vadesi; MSCI kapanışta; ay sonu | T2 hesabı. 12 ay küme RS sıralaması (K7 filtresi). Mevduat 4. dilim (35 gün → 04.01.2027); PPF %40'a iner. A4 uygulanıyorsa VİOP-47 dışı long bu kapanıştan serbest. Aylık rapor (§8.5) |
| Sal 01.12 | — | MSCI listesi evrene geri döner; Şubat 2027 MSCI duyuru ve yürürlük tarihleri günlüğe yazılır (A3) |

### 7.4 Aralık 2026 – Haziran 2027

| Tarih | Olay | Plan |
|---|---|---|
| Per 3.12 10:00 | Kasım TÜFE | M2'nin 1. ayı |
| Per 10.12 | PPK (anket %35) | A7 banka kuralı; çekirdek faizleri yenilenir |
| 21–23.12 | Devir haftası | Aralık VİOP pozisyonları en geç 23.12 kapanışında Ocak/Şubat'a devredilir ya da kapatılır (A10) |
| 24–31.12 | Stopaj süresi bitiyor | 2027 stopaj oranlarına göre çekirdek araçları yeniden seçilir ([VC] §2 m.6) |
| Per 31.12 | Aralık vadesi (XU030, USDTRY, pay vadelileri) | Devredilmeyen her şey kapanmış olmalı |
| ~4.1.2027 | Aralık TÜFE | M2'nin 2. ayı; M2 en erken burada 1 olur |
| 29.01–05.02.2027 | Blok kilidi (~3.2) ve fon uyumu (31.1) | A9: K1'de yeni giriş yok |
| 01.02.2027 | K3b pilot başlangıcı | Yarım boy (%1,25), hedge'li (§3 K3b) |
| Şubat 2027 | MSCI Şubat gözden geçirmesi | A3 aynen (duyurudan önceki kapanışta yeni giriş yok) |
| Şubat–Mayıs 2027 | Temettü duyuru ve hak sezonu | K3 en aktif dönem; K3b pilotu canlı |
| ~15.03.2027 | A7 bitişi (63 işlem günü; Ramazan Bayramı tatili tahmini 9–11.03, teyit edilir) | Banka kümesinde boy kısıtı kalkar |
| ~17.03.2027 | Tasfiye azami süresi | Dışlama listesi gözden geçirilir |
| Haziran 2027 | MSCI sınıflandırma değerlendirmesi | Mayıs'ta rejim ve MSCI riski yeniden değerlendirilir |
| Kasım 2027 | 12 ay | Ölçekleme kararı (§8.4) |

---

## 8. Öldürme kriterleri ve ölçüm

### 8.1 Ölçüm birimi: engele göre fazla getiri (A'nın ölümcül kusuru düzeltildi)

- Fazla_TL = net K/Z_TL − bağlanan_nakit_TL × engel_dönem.
  - **Bağlanan nakit:** Spotta pozisyon maliyeti. VİOP'ta faiz kazanmayan teminat; teminat PPF payıysa ya da TLREF ile nemalanıyorsa 0.
  - **engel_dönem:** Aynı günlerde banka PPF'sinin vergi sonrası getirisi (§1.1).
- R_fazla = Fazla_TL / R_TL. R_TL = ilk stop riski (K4: nominal × stop mesafesi; K1/K2: bacak nominali × %8; K3: pozisyon × %8; K5: pozisyon × %20).
- **Neden:** Bugünkü faizde 45 işlem günlük bir K4 tutuşunda engel ≈ %5,6–6,2 ≈ 0,37–0,41R. Mutlak R > 0 olan bir kol engeli kaybediyor olabilir ([HK] §3.1 m.1; [HD] §6 m.1).
- **Bütün öldürme ve büyütme testleri yalnız R_fazla ile yapılır.**

### 8.2 Günlük alanları (işlem başına bir satır; ekleme ayrı satır)

```
islem_id, kol, hipotez_karti, hisse/kontrat, kume, blok, rejim, T1..M5_degerleri,
sinyal_tarihi, sinyal_degeri (z / B52 seviyesi / hak gunu / teklif fiyati),
hedef_giris_fiyati (t+1 kapanis), son_fiyat_18:00, emir_asamasi (18:01-05 / 18:08-10 gec), gerceklesen_fiyat, kayma_bps, dolum_hatasi(E/H), kilit(E/H),
arac (spot/F_kodu), adet_veya_kontrat, nominal_TL, hesap_yuzdesi, teminat_TL, teminat_faizi,
stop_mesafesi, R_TL, ima_tasima_orani (VIOP ise),
cikis_tarihi, cikis_nedeni (E1..E6/zaman/felaket/kurumsal/rejim/kural_disi), cikis_fiyati,
brut_TL, komisyon+BSMV_TL, stopaj_TL, net_TL, R,
PPF_ayni_donem_% (engel), baglanan_nakit_TL, fazla_TL, R_fazla,
MAE_%, MFE_%, gun_sayisi, XU030_ayni_donem_%, kural_sapmasi(E/H)+not
```

Kâğıt kolları (K2 bayat sinyaller, K3b Ocak 2027'ye kadar, PEAD, eski lead-lag sinyalleri) aynı alanlarla ayrı sayfada tutulur. K9 fikir kartı: tarih, mekanizma, giriş, stop, çıkış, beklenen süre, sonuç.

### 8.3 Hipotez kartları (09.11.2026 tarihli; değiştirilemez)

| Kol | Mekanizma | Beklenen net / işlem | İsabet | İşlem/yıl | 1R | Beklenen R_fazla | Denenen varyant |
|---|---|---|---|---|---|---|---|
| K1 | Holding–iştirak fiyat sapmasının sınırlı arbitrajla kapanması | +80…+180 bps (bacak nominali) | %60–70 | ~5 | Bacak × %8 | +0,08…+0,2 | 108 hücre ([BS] §9.1) |
| K2 | Aynı | +40…+90 bps | %55–60 | ~5 | Bacak × %8 | +0,03…+0,1 | Aynı |
| K3 | Temettü öncesi talep | +%0,2…+%0,5 (ham getiriden; piyasa ≈ engel varsayımıyla) | %55–65 | 25–40 | Pozisyon × %8 | +0,03…+0,06 | Az |
| K3b (pilot 01.02.2027) | Yüksek verimli temettüye kayma | +%3…+%3,5 fazla (muhafazakâr +%6–7'nin yarısı) | %60–67 | ~6–10 (likit) | Pozisyon × %12 | +0,25…+0,3 | Tek ajan + bağımsız yeniden üretim; %3/%5/%8 eşikleri ([OB] §8; [VO] §2.3) |
| K4 | Zirve kırılımında gecikmeli tepki; kazananı koşturma | AÇIK'ta R_fazla 0…+0,3; KAPALI'da ≈ 0 | %40–45 | KAPALI 0–5, AÇIK 20–40 | Nominal × %15 (%25) | 0…+0,3 | 25 kombinasyon, 36 portföy varyantı ([BT] §5) |
| K5 | Teklifle sabitlenen fiyat (yalnız gönüllü teklif / satma hakkı) | +%2…+%8 | %80–90 | 0–2 | Pozisyon × %20 | +0,1…+0,4 | Test yok |
| K6 | Carry primi (satılmış kuyruk) | Nominalin ayda ~%0,7–0,9'u | aylık %80+ | Kapıya bağlı | Nominal × %4 | — | 1 kural |
| K9 | Plan dışı fikirlerin sınırlı kanalı | ≤ 0 (amaç kayıp sınırı) | — | ≤ 10 | Nominal × stop | ≤ 0 | Serbest |

### 8.4 Ölçekleme (boyut artırma)

**Genel kural:** 12 ay dolmadan ve aşağıdaki minimum işlem sayısına ulaşmadan hiçbir kolda boyut artmaz. Bu sürede yalnız küçültme ya da kapatma kararı verilir ([SE] §5.3 m.4).

**Minimum işlem sayıları:**

| Kol | Minimum | Tahmini süre |
|---|---|---|
| K1 | 20 işlem | ~4 yıl |
| K2 | 20 işlem | ~4 yıl |
| K3 | 60 olay | ~2 sezon |
| K4 | 40 kapanmış işlem | — |
| K3b | 10 olay (pilot) | 1 sezon; 2028 boy kararı |

**Artış koşulları (hepsi birlikte):**
- Ortalama R_fazla > 0 ve t ≥ 1,5.
- Canlı ortalama ≥ backtest beklentisinin %50'si.
- Kayma, kenarın %30'unun altında.
- Kol düşüşü beklenti bandının içinde.

**K4 için ek koşullar:** AÇIK'ta r₀ %0,75 → %1,0 yalnız şu koşullarla: ≥ 40 işlem, ortalama R_fazla ≥ +0,15, t ≥ 1,5 ve kol düşüşü hiç −6R'yi aşmamış ([HK] §5 m.1). %1,0'ın üstü 24 ay boyunca yok.

**Artış adımı:** En çok 1,33–1,5×, yılda en çok bir kez. KAPALI tablosuna göre toplam en çok 2×.

**Gerçekçilik:**
- +0,2R'lik bir sistemi doğrulamak ~400 işlem ister ([SE] §3.7).
- 12 ayda uydu fazlasının sıfırdan istatistiksel olarak ayrışma olasılığı < %30 ([TC] §8.3 m.4).
- İlk yıl ağırlıkla yürütmeyi (kayma, dolum, kurala uyum) test eder; "kenar kanıtlandı" denemez.

### 8.5 Öldürme kriterleri (sayısal, önceden yazılı)

| Kriter | Eşik | Sonuç | Kaynak |
|---|---|---|---|
| Mekanizma kırılması | K1/K2'de pay yapısı değişikliği, birleşme, ZPAT. K3'te temettü vergisi ya da hak kullanım kuralı değişikliği. K4'te SPK/BIST'in fiyat limitini ya da açığa satış rejimini değiştirmesi | Kol hemen kapanır ya da incelenir; t'ye bakılmaz | [SE] §5.2 m.5 |
| Uygulama farkı | Ortalama kayma + maliyet > backtest brüt kenarının %50'si (K1 > ~75 bps, K2 > ~45 bps, K3 > %0,45, K4 > 40 bps gidiş-dönüş) | Kol kapanır ya da emir yöntemi değişir | [SE] §5.2 m.3 |
| Erken uyarı | K1/K2: 10 işlemde ortalama R_fazla < 0 ve ≥ 7 kayıp. K3: 15 olayda ortalama ≤ −%0,5. K4: 30 işlemde ortalama R_fazla < −0,20 | Boyut yarıya | [SE] §5.2 m.4; [TA] §7.5 |
| Beklenti testi | K1/K2 20 işlemde, K3 40 olayda: ortalama net fazlanın bootstrap %90 güven aralığının üst sınırı < tahmini maliyet | Kol kapanır | [SE] §5.2 m.2 |
| K4 durdurma | 60 işlemde ortalama R_fazla'nın %90 güven aralığının üst sınırı < +0,10 | K4 durur; yeni hipotez kartı gerekir | [TA] §7.5 K2 (R_fazla'ya çevrildi) |
| K4 kapatma | 100 işlemde ortalama R_fazla ≤ 0 | K4 kapanır | [HK] §5 m.1 |
| Tek işlem kuyruğu | K1/K2'de tek işlem bacak nominalinin −%12'sini aşarsa (backtest en kötüsü −%8,3) | Askıya alma, inceleme | [TC] §7.3 |
| Kol düşüşü | K4'te −8R; K1+K2 toplamında −4R | 3 ay kâğıt | [SE] §5.2 m.1 |
| Negatif çarpık kol | K6'da tek kayıp > hesabın %3'ü, ya da 3 ay içinde 2 kapanış koşulu | K6 kalıcı ya da çeyrek boyunca kapalı | [SE] §5.2 m.6; [TB] §7.1 |
| Beta sızıntısı | K1/K2'nin 12 ay getirisinin XU030 ile korelasyonu > 0,5; K4'te korelasyon > 0,7 ve XU030 + çekirdeğe göre kalıntı alfa ≤ 0 | Hedge gözden geçirilir; K4 durur, yerine K7 | [SE] §5.2 m.7 |
| K9 freni | K9'un birikimli kaybı hesabın %1,5'i | K9 6 ay kapalı | [R1] B2 |
| Plan dışı işlem | K1–K9 dışında tek işlem (kural_sapmasi = E) | Bütün uydu 1 ay kâğıt; ikinci kez 3 ay | [R1] B2 |
| Toplam uydu | §5'teki aylık ve birikimli eşikler | Dur / yarıya / kapat | §5 |

### 8.6 Gözden geçirme takvimi

| Sıklık | İş |
|---|---|
| Her kapanış | §6.3 rutini |
| Cuma | Rejim, stres, açık risk, dışlama, K6 kapısı, mevduat dilimi |
| Ay sonu (ilk 30.11) | T2; kol bazında R_fazla dağılımı, kayma; aylık limit; çekirdeğe göre uydu fazlası. En iyi %5 ve %10 işlemin kâr payı (>%50 normaldir) |
| Her 10 işlem/olay | Erken uyarı (§8.5) |
| 3 ayda bir | Hipotez kartlarıyla kıyas |
| Kasım 2027 | Ölçekleme kararı (§8.4) |

---

## 9. Beklenen sonuçlar (12 ay, maliyet ve vergi sonrası, engele göre)

### 9.1 Kol bazında (rejim KAPALI sürerse)

| Kol | Katkı, merkez (puan) | ~%80 aralık | Belirsizliğin ana kaynağı |
|---|---|---|---|
| K1 SAHOL↔AKBNK | +0,4 (teminat faizsizse 0, kol kapalı) | 0…+0,9 | Teminat faizi, komisyon, yılda ~5 işlemin gürültüsü |
| K2 KCHOL↔sepet (isteğe bağlı) | +0,05 | −0,2…+0,3 | Zayıf kenar, 6 bacak |
| K3 temettü −6/−1 | +0,3 | 0…+0,8 | Ham getiri; %2–5 kovası ayrıca test edilmedi; sezon |
| K3b (pilot Şubat–Mayıs 2027; yarım boy) | +0,3 | 0…+1,2 | İleri test; iptal edilen teklifler örnekte yok |
| K4 sondaları | 0 | −0,3…+0,3 | Rejim |
| K5 özel durumlar | ~0 | 0…+0,2 | Zorunlu tekliflerde kayıt tarihi kuralı |
| K6 carry | +0,1 | −3…+0,6 | Kur şoku (negatif çarpık) |
| K9 serbest kol | −0,1 | −1,5…+0,3 | Davranış; fren −%1,5 |
| **Toplam, KAPALI** | **≈ +0,5…+1,5 (merkez ~+1)** | **−2,5…+3** | |
| Rejim dönerse ek (K4 tam boy + K7) | +3…+8 | −4…+15 | Sağ kuyruk; sahte sinyalde negatif |

Çekirdeğin mevduat ağırlığı (%60), tümü PPF'de tutulan bir çekirdeğe göre risksiz ~+1,5–1,8 puan ekler. Bu katkı engelin içinde sayıldı, uydu fazlasına eklenmedi.

### 9.2 Senaryo bazında (olasılıklar öznel, [TM] §5.2)

| Senaryo | Olasılık | Çekirdek net (nominal) | Uydu fazlası (puan) | Hesap toplamı (net nominal TL) | USDTRY 12 ay (öznel) | Hesap, USD bazında |
|---|---|---|---|---|---|---|
| S1 sönümlenme, rejim 1–6 ayda döner | %35 | %30–33 (hızlı indirim) | +3…+7 | %34–40 | +%15…+%20 | +%12…+%22 |
| S2 yatay kanama, carry kazanır | %40 | %33–37 | 0…+2 | %33–37 | +%18…+%23 | +%8…+%16 |
| S3 kontrollü kur hızlanması | %15 | %35–38 | −1…+1,5 | %34–39 | +%30…+%40 | −%4…+%7 |
| S4 kırılma (kur birkaç haftada +%15–30, acil faiz artışı) | %10 | %38–45 | −4…−1 | %35–43 | +%45…+%70 | 12 ayda −%21…−%1; **şok anında −%10…−%21** |
| **Ağırlıklı** | | **~%33–36** | **≈ +1…+2** (%80 aralık −2…+5,5) | **≈ %33–37** | | **≈ +%10** (çok belirsiz) |

- **Kur varsayımları** öznel: vadeli eğri 12 ayda ~+%33, anket +%19,5, 2026'da gerçekleşen hız ~%20/yıl ([TM] §1, §4.3). USD sütunu = (1 + TL getiri) / (1 + kur değişimi) − 1.
- **Ölçü birimi ([R1] B8):** Plan TL engeline göre kuruludur. Kullanıcı ölçü birimini **yazılı** seçer. USD seçilirse plan yanlış ölçüte göre kurulmuş demektir. Koruma iki yolla alınabilir, ikisi de pahalı: korunan nominal üzerinden yılda ~13 puan carry primi ya da OTM USDTRY call (Aralık C56000 nominalin %0,56–0,80'i; [TM] §4.3). Planın kanıtı korumayı önermez; **S4'teki USD kaybı bilinçli olarak kabul edilmiştir.**

**Dağılımın özellikleri:**
- P(12 ayda engelin altında) ≈ **%35–45.**
- Engele göre kötü %10'luk kuyruk −3…−5 puan; stres tavanıyla sınırlı.
- İyi %10'luk kuyruk +8…+15 puan; S1 ile kırılımın sağ kuyruğu birlikte gelirse.
- Reel karşılık ~%3–7. USD karşılığı ağırlıklı ~+%10, S4'te şok anında −%10…−%21.

### 9.3 TL karşılıkları (uydu fazlası; merkez +1…+2, %80 aralık −2…+5,5)

| Hesap | Merkez | %80 aralık | Halka arz eklentisi (onaylar başlarsa) |
|---|---|---|---|
| 1 mn TL | +10…+20 bin TL | −20…+55 bin | +8…+22 bin |
| 5 mn TL | +50…+100 bin | −100…+275 bin | Aynı TL (yüzde olarak küçük) |
| 20 mn TL | +200…+400 bin | −0,4…+1,1 mn | Aynı TL (~0 puan) |

Kapasite 20 mn TL'ye kadar bağlayıcı değil. İstisnalar: K1/K2 Aralık kontrat derinliği ve K4'te hacmin %2 sınırı.

### 9.4 "Yüksek getiri" sorusuna açık cevap

1. **Bu rejimde yılda engel + 0,5…2,5 puan, merkez ~+1,5.** Getirinin %90'ından fazlası çekirdekten gelir. Uydunun bugünkü asıl değeri, rejim dönüşüne hazır, ölçülmüş ve maliyeti bilinen bir süreçtir.
2. **Rejim dönerse yılda +3…+8 puan.**
   - Koşul: M1 ile T3 ya da T1 açılmalı ve kırılım ile endeks kolları devreye girmeli.
   - Kârın >%50'si birkaç işlemden gelir.
   - 2017/2020/2022 tipi bir yılda iki haneli fazla mümkün, ama planlanamaz ([TA] §8.2).
   - Rejim kırılmalarından sonra bankaların 3–6 ayda dolar bazında +%40–90 kazandığı gözlem n = 4 ([TM] §2.3), ve [OA] §4 bunun PPK sonrası zamanlamasının aleyhinde.
3. **+10–20 puan isteniyorsa:** Bu planın 3–5 katı açık risk (%8–12), engele göre −%25…−%40 düşüş toleransı ve sağ kuyruğa bağımlılık gerekir ([SE] §5.1). Kanıt bu rejimde bunu desteklemiyor:
   - Kırılım portföyü 2024–26'da engelin 2–8 puan altında ([VB] §2.1).
   - 456 küme kuralının 0'ı rf'yi geçti ([VD] B2).
   - 3 yılda hisse fonlarının neredeyse hiçbiri PPF'yi geçmedi ([VP] T1–T2).
4. **En büyük doğrulanmış yeni kenar K3b** ([VO] §2.3: muhafazakâr kıyasla +%6–7 fazla, bağımsız veriyle). Önceden kayıtlı pilot olarak yarım boyla Şubat–Mayıs 2027'de canlı. Tam boyda ve gerçekse bir sezonda +0,5…+2 puan ekleyebilir; merkeze yalnız +0,3 kondu.

---

## 10. Pazartesi 9.11.2026 kontrol listesi

**Cuma 6.11 akşamı / hafta sonu**
- [ ] 18:20 sonrası `bist_sinyal.py` (6.11 kapanışı): §4.4 tetikleri (zirve52 tuzağı betikte çözülü: tetik = bugün dahil 252 gün zirvesi, B52 = bugün hariç), TT, SMA50/200, XBANK, K1/K2 z ve kesişim tarihleri, RYSAS likidite sırası.
- [ ] **20:45 sonrası** betik yeniden (ya da Ek A komutu): `viop_20261106.csv`; XU030 Aralık ima oranı **uzlaşmayla**; §1.5 iki açma kuralı (beklenen: ikisi de kapalı); F_USDTRY ön ay ima (KRİZ e).
- [ ] KAP: 9.11–11.12 temettü hak kullanımları (K3: verim %2–5, ilk 100; ≥ %5 olanlar K3b kâğıt), bedelsiz hak günleri (A5), açık ZPAT'lar ve "Esas Alınan Tarih". AHGAZ, ENERY, RYSAS 3Ç raporu (9.11 akşamı bekleniyor).
- [ ] Aracı kurum seçimi (§6.1) ve 12 soru. Cevap gelmeden VİOP kolu yok.
- [ ] 2 banka mevduat teklifi (32 gün; 30.11 dilimi için 35 gün oranı da sorulur); banka iştiraki PPF seçimi (tasfiyedeki 7 PYŞ asla; KAP portföy raporunda grup ihracı yok; emir saat sınırı).
- [ ] Dışlama listesi (§4.2) emir ekranında "yasak".
- [ ] Alarmlar (kapanış bazlı): ENJSA 127,00; AHGAZ 48,70; ENERY 14,60; RYSAS 30,28; KCHOL 225,50; BIMAS 433,75; TUPRS 409,90; XU100 12.691 ve 13.572; XBANK 16.955; K1 SAHOL 91,10 / 82,35, AKBNK 62,78 / 69,44 (6.11 kapanışıyla [SİN] günceller).
- [ ] Günlük şablonu (§8.2), hipotez kartları (§8.3) ve K9 fikir kartı şablonu, 09.11 tarihli. `makro.json` (rezerv, TÜFE, CDS, politika faizi, Kural 0) 05.11 değerleriyle ([RUT]).
- [ ] Ölçü birimi yazılı seçilir: TL engeli (plan) ya da USD (§9.2).
- [ ] Eski lead-lag sinyallerinde açık pozisyon varsa kendi çıkış kuralıyla kapanış takvimi yazılır.

**Pazartesi 09:00–12:00 (tek seferlik)**
- [ ] Mevduat 1. dilim: hesabın %15'i, 32 gün, **doğrudan bankada** (150 bin / 750 bin / 3 mn TL; 20 mn'de ≥ 3 banka).
- [ ] PPF: hesabın %85'i (850 bin / 4,25 mn / 17 mn; ≥ 2 PYŞ). Kalıcı %40; geçici %45, 16/23/30.11 dilimleri için.
- [ ] DİBS yalnız yazılı %0 stopaj teyidiyle, ≤ %10, ≤ 12 ay vade.
- [ ] Hisse/endeks long, short F_USDTRY, XU030 nakit-taşıma ve opsiyon yok.

**Pazartesi 18:15–18:45 ve 20:45 sonrası**
- [ ] Rejim tablosu (§2.1). Beklenen: KAPALI, 0/7; KRİZ yok.
- [ ] K4: Bilançosunu 9.11 18:00'den önce açıklamış bir isimde B52 + TT 7/7 kapanışı varsa Salı kapanış seansına sonda emri (r₀ %0,25; limit = min(t kapanışı × 1,06; P_son × 1,03); aynı kümeden 1, toplam 2).
- [ ] K1: \|z\| ≥ 2, Kural 0 cevabı geldi ve komisyon ≤ 5 bps ise Salı 17:50/17:55 emirleri (eşit TL; 20 gün 30.11'i aşıyorsa Aralık kontratı).
- [ ] Açık risk ≤ %2,5; stres ≤ %6; VİOP teminatı ≤ L1; spot uydu ≤ %15.
- [ ] Günlük kaydı.

**Hafta içi sabitler**
- [ ] Sal 10.11 18:15: Bilanço sonrası K4 değerlendirmesi; giriş en erken 16.11 (A2).
- [ ] Çar 11.11: Hiçbir kolda yeni giriş yok.
- [ ] Per 12.11: 07:00 MSCI → dışlama (A3). 14:30 rezerv → M1, K6 kapısı, **KRİZ (d)**. Akşam SPK bülteni.
- [ ] Cum 13.11: Kredili esneklik kararı → A4. 18:30 haftalık gözden geçirme.
- [ ] Pzt 16.11: Mevduat 2. dilim; esneklik uzatıldıysa ilk yeni giriş kapanışı.

**Asla:** Kredili spot; dışlama listesindeki hisse; tavan serisi sonrası halka arz alımı; bedelsiz/temettü hak gününe bilerek pozisyon taşımak; piyasa emri; vadede fiziki teslimata kalmak; KAPALI'da tam boy giriş; opsiyon satışı; K6 kapısı kapalıyken short F_USDTRY; K1–K9 dışında işlem.

**Hiçbir koşul tetiklenmezse** pozisyonsuz kalınır. Çekirdekte beklemek bu planın varsayılan ve meşru sonucudur ([KO] §8).

---

## 11. İzlenebilirlik ve açık sorular

### 11.1 Kural → bulgu tablosu

| Kural | Bulgu (dosya + bölüm) | Kanıt durumu | Plan içi iskonto / not |
|---|---|---|---|
| Çekirdek %60 mevduat / %40 banka PPF | [VC] #4; [VB] #13, §3 m.3; [HD] §2 | [D] | Faiz sabitse mevduat ~+3 puan |
| DİBS yalnız yazılı %0 teyidiyle | [VC] #8 | [D] (30.06.2026'ya kadar resmî) | — |
| XU030 nakit-taşıma kapalı; ima ≥ mevduat neti + 3 ise açılır | [VP] T12; [VC] §2 m.1; [TB] §1.5 | [D] fiyat; [TE] eşik | Basitle basit |
| Vadeli finansman ≥ 3 puan ve Kural 0 | [VP] T12; [TA] §2.1.3; [HK] §3.1 m.4 | [D] fiyat; [TE] kural | A'nın 8–13 puanı → 3,5–7,5 |
| Kural 0 (teminat faizi) | [SE] §5.1 sıra 0; [VC] §2 m.2; [VB] #16 | [TE] (maliyet aritmetiği) | — |
| Rejim AÇIK = XU100 > SMA200 | [BT] §5.1 (S5 t 5,4); [VB] #28 | [D] | Bir risk kontrolü, getiri kaynağı değil ([BT] §6) |
| GEÇİŞ tanımı (T3 + M1 + 1) | [TM] §5.1; [TA] §3.1 | [TE] | Yarım boy |
| M2 = 2 ay üst üste < %2 | [TM] §5.1 | Kaynağa uygun | Taslaklardaki tek ay düzeltildi |
| Yabancı akımı sayılmaz | [OA] §3; [VO] §4.2 | [D] zayıf (2021–26 t 1,87) | Teyit göstergesi |
| KRİZ kesicisi (a)–(f) ve açık pozisyon eylemi | [KO] §4.2; [TC] §3.1; [TM] §5.1; [R1] B5 | [TE] | CDS yalnız teyitliyse |
| K1 SAHOL↔AKBNK, t+1 kapanış | [VB] #25, §2.5; [BS] §9.1 | [D] (gecikmeli t 2,4/2,8) | %40 iskonto; komisyon ≤ 5 bps/bacak/yön ([R2] A.5); tek bacak hedge'i ([R1] B9) |
| K2 yalnız yeni kesişim | [VB] #25; [TC] §2.2 | [D] (t 2,1); kalıcı sinyal karışık | Varsayılan kâğıt |
| K3 temettü −6/−1 | [VB] #26; [BS] §5.3; [R2] A.6; [VO] §2.3 | [D] (t 6,5; ham getiri) | Olay başı +%0,2…+%0,5; hedge'li sürüm tercih |
| K3b yüksek verimli duyuru | [OB] §8; [VO] §2.3 | [D] (bağımsız: +%6,5, t_ay 6,5; 2024–26 +%13,5, N=61) | %50 iskonto; pilot 01.02.2027, yarım boy |
| K4 kırılım S2 + iz %15 | [BT] §5.1–5.2; [VB] #28, §2.1 | [D] işlem düzeyi; 2024–26 engelin altında | %50 iskonto; KAPALI'da sonda |
| K4'te S1 yok | [BT] §5.2 | [D] | — |
| K4 ekleme | [TA] §2.1 | [TE] (aritmetik risk-nötr) | Yalnız AÇIK, ayrı satır |
| Küme RS filtre değil | [TA] EK-3; [VD] §5 m.1 | Örneklem içi; doğrulanmamış ek hesap | Yalnız öncelik ve sınır |
| K5 ZPAT kontrol listesi + kayıt tarihi | [VB] §3 m.4; [TB] K4; [HK] §3.2; [R2] A.2 (KAP 1666313, 1673963) | Çalışılmadı; AKCNS kapandı | Katkı ~0 |
| K6 carry kapısı + brüt ≥ 160 | [VC] #18, #19; [KO] §4.2; [TM] §4.3 | [D] veri; [TE] kapı | Pazartesi 0 |
| K7 TSMOM12 + küme filtresi | [BT] §2; [VD] B3, §5 m.1; [DB] §3.7 | [D] (anlamlılık zayıf) | %20 nominal, 1x |
| K8 halka arz katılımı | [HA] §0, §3b; [VB] #11; [VO] §3 | [D] (prim medyan +%33–38; 8–22 bin TL/yıl) | Risk bütçesi dışında; E kapanış satışı |
| K9 serbest kol ve plan dışı fren | [R1] B2; [VP] T1–T2; [SE] §1.1 | [TE] | Kayıp sınırı −%1,5 |
| A1 bilanço gecesi yok (ENJSA çıktı; AHGAZ/ENERY/RYSAS eklendi) | [HZ] §2; [R2] A.3 (KAP 1691179) | [TE] | — |
| A3 MSCI (her gözden geçirme ve ad hoc duyuru) | [VC] #17; [TM] §4.3 m.6; [R1] B6 | [D] asimetri; [TE] kural | — |
| A2/A4 11–13.11 girişsiz; esneklik her bitiş tarihine | [VB] #7; [HZ] §0 m.3; [BT] §4; [R1] B4 | [D] takvim; [TE] kural | — |
| A5 bedelsiz kaçınma | [OB] §0, §6, §7; [VO] §2.2 | [D] (hak [1,10] −%3,26, t −5,5; 2024–26 −%1,45, t −1,5) | Maliyetsiz kaçınma |
| A6 temettü hak sonrası | [OB] §8; [BS] §5.3 | [DM] / [D] yön | — |
| A7 banka–PPK | [OA] §4.2, §4.5; [VO] §4.1 | [D] sayılar; etkin n = 6 döngü | Yalnız boyut eğilimi; bitiş ~15.03.2027 |
| A9 blok kilidi / fon uyumu | [VP] T7, T8; [TP] §4.5 | [D] takvim | — |
| Dışlama listesi | [VP] T6, T10; [TP] §4.4–4.5, §6; [VB] #27, #28 | [D] | — |
| Stres formülü ve tavanlar | [TB] §5; [TC] §5; [VC] §2 m.8 | [TE] | — |
| R_fazla ölçüm birimi | [TB] §6.4; [HK] §5 m.1; [HD] §6 m.1 | Muhasebe | A'nın ölümcül kusuru düzeltildi |
| Ölçekleme eşikleri | [SE] §3.7, §5.3; [HK] §5 m.1 | [L] / [TE] | — |
| Kapanış seansı emir kuralları (18:01–18:05, ±%3; risk azaltan satış = izin verilen en düşük fiyat) | [BİP]; [BT] §1 m.3; [R1] B1; [R2] A.1 | Borsa kuralı; [TE] | Testteki çıkış varsayımına yaklaştırır |
| L1–L3 teminat ve likidite | [R1] B3; [VB] #16; [HZ] §5 | [TE] (aritmetik) | Mevduat bozulmaz |
| Aracı kurum seçimi ve saklama | [R1] B7; [TP] §4.1; [KK] §2.4 | [TE] | — |
| USD ölçü sütunu, ölçü biriminin yazılı seçimi | [R1] B8; [TM] §4.3 | Öznel senaryo | Koruma alınmaz, risk bilinçli kabul |
| Rutinin 18:15 / 20:45 bölünmesi | [R2] A.4 (VİOP Prosedürü Ek-3; bülten Last-Modified 20:28–20:49) | Borsa takvimi | — |

### 11.2 Açık sorular (cevap gelene kadar ilgili kural kapalı ya da ihtiyatlı)

1. **Aracı kurum cevapları (§6.1):** teminat faizi, PPF/DİBS teminatı, kurum teminat oranları, çift mahsubu, komisyon (K1 ≤ 5 bps), kapanış seansına özel emir, en düşük izinli fiyatlı satış, SAR/STJ, Yatırımcı Tazmin Merkezi kapsamı. K1, K2, K3/K3b hedge'i, K6, K7, K9 vadelisi ve vadeli finansman buna bağlı.
2. **DİBS stopajı:** 9–30.11 alımlarında %0 mı? 31.12.2026 uzatması yalnız ikincil kaynakta.
3. **2027 stopaj takvimi:** Mevduat/PPF için %17,5 ve DİBS muafiyeti 31.12.2026'da bitiyor. İndirim haberi tek ikincil kaynakta. Engel 1–3 puan oynayabilir.
4. **6.11 VİOP bülteni:** 20:45 sonrası yayımlanır; ima oranlar ve K1/K2 z'leri 6.11 kapanışıyla [SİN] çıktısında.
5. **CDS 248** bağımsız teyit edilmedi ([VC] §1 sonu). Bu yüzden M4 ve KRİZ (c) yalnız teyitli veriyle; K6'da CDS'in yerine F_USDTRY ima oranı. TMSF mevduat sigortası limiti, Kasım PKA tarihi, HALKB bilanço tarihi, güncel VBTS listesi ve 2027 Ramazan Bayramı tatil günleri (A7 bitişi) teyitsiz.
6. **K3b:** İptal edilen ya da genel kurulda düşürülen teklifler örnekte yok ([VO] §2.3); pilot boyu (%1,25) bu yüzden küçük. Teklif tutarı KAP metninden alınmalı.
7. **K3 %2–5 kovası:** [−5,−1] penceresinde ayrıca test edilmedi; [VO] duyuru penceresinde ≈ 0 buldu.
8. **RS yüzdeliği:** test tanımı (en likit 150) ile [SİN] tanımı (fiyatı çekilen ~160 hisse içinde en likit 150) arasındaki fark (ENJSA: tarama 93, [SİN] 94).
9. **Takasbank genel mektup numarası:** GM 2174 ([KO]) mı 2176 ([HZ])? Oranlar aynı; aracı kurumdan teyit.
10. **Ortak kör nokta:** Bütün backtest kanıtı aynı İş Yatırım verisinden ve hayatta kalan hisse evreninden geliyor ([VB] §2.4; [BT] §1). 2020 öncesi limit modeli de hatalı (±%9,5 yerine ±%20; [VB] §2.2).

### 11.3 Taslaklardaki kusurların düzeltilmesi

| Kusur | Kaynak taslak | Bu plandaki düzeltme | Dayanak |
|---|---|---|---|
| Öldürme/ölçekleme mutlak R ile | A | Bütün testler R_fazla ile | [HK] §3.1 m.1 |
| Basit ve bileşik oran karışıklığı (XU030 "8 puan", vadeli "8–13 puan") | A | Basitle basit: 3,3 puan; vadeli avantajı Aralık kontratlarıyla mevduata göre yalnız GARAN'da ≥ 3 puan ([R2] A.8; eski ~4,6–7,4 Kasım kontratındandı) | [VP] T12; [HD] §4 |
| AÇIK'ta brüt %60 (iki tabanda −%11,4) | A | Stres ≤ %10 bağlayıcı; fiilen uzun nominal ≤ ~%30–40 | [HU] §3 A m.3 |
| S1 yarım boy | A | Yalnız S2 | [BT] §5.2 |
| TSMOM12 eşiği tutarsız (%45 / %37) | A, C | İki eşik yazıldı; karar için 15.860 | [VB] #23 |
| Pazartesi carry (brüt rezerv < 160) | B | Pazartesi 0; brüt ≥ 160 kapı koşulu | [KO] §4.2; [VC] #18 |
| "Önce bankalar" rejim kolu, 10.12'yi kapsıyor | B | Kaldırıldı; A7 kuralı | [OA] §4.2 |
| Strangle, uzlaşma fiyatı limitiyle | B | Kaldırıldı | [HU] §4; [VP] A6 |
| SPK onayında bedelsiz alımı | B | Kaldırıldı; [OB] bütün aşamaları reddetti | [OB] §0 |
| Temettü alışı gün −5 | B | Gün −6 | [BS] §5.3 |
| TÜFE < %2 tek ay | B (A, C) | 2 ay üst üste | [TM] §5.1 |
| Çift girişi 09:30 uzlaşma ± %0,5 | C | t+1 kapanış penceresi | [VB] #25, §2.5 |
| KCHOL↔sepet kalıcı sinyalle, MSCI'dan önceki gece | C | Yalnız yeni kesişim; varsayılan kâğıt | [HK] §3.3 |
| ZPAT'ta hak sahipliği kontrolü yok | C | Kontrol listesine eklendi | [HK] §3.3 m.2 |
| Mevduat dilimleri aynı haftaya yığılmış | C | 9/16/23/30.11 | [HU] §3 C m.3 |
| "Son 6 kümeden giriş yok" (test edilmemiş) | C | Kaldırıldı | [TA] EK-3 |
| Yabancı alımı rejim tetiği | A, B, C | Yalnız bilgi | [OA] §3 |
| Tarama `zirve52` bugünü içeriyor | Tarama | B52 tanımı düzeltildi; [SİN] B52'yi bugün hariç, tetiği bugün dahil hesaplar | `bist_tarama.py` satır 129–137 |
| Tarama XU030 ima oranı %23,3 (ChartData vadeli fiyatı 14.605) | Tarama, [HZ] §0 m.8 | `bist_tarama.py` `viop_fiyatlama` artık yalnız [BÜL] uzlaşmasını, bülten tarihindeki spotla kullanır → %29,3 | [VP] T12; 06.11 düzeltmesi |
| Kırmızı takım bulguları (R1: 11, R2: 15 madde) | Plan | §12 | [R1]; [R2] |

---

## Ek A. Formüller ve komutlar

**Resmî VİOP bülteni** (varsayılan başlıklarla; [TB] Ek A):

```
G=20261106   # bülten ~20:28–20:49 TSİ'de yayımlanır
curl -s -o viop_$G.csv https://www.borsaistanbul.com/data/vadeli/viop_$G.csv
awk -F';' '$2~/^(F_XU0301226|F_USDTRY1126|F_USDTRY1226|F_XLBNK1226|F_SAHOL1226|F_AKBNK1226|F_GARAN1226|F_ENJSA1226)$/ {print $2, "uzlasma="$10, "kapanis="$16, "hacimTL="$18, "adet="$20, "islem="$21, "acikpoz="$22}' viop_$G.csv
```

Sütunlar: 2 = sözleşme kodu, 9 = vade tarihi, 10 = uzlaşma, 16 = kapanış, 18 = işlem hacmi (TL), 20 = işlem miktarı, 21 = işlem sayısı, 22 = açık pozisyon (5.11 başlık satırıyla teyit edildi; [R2] B). İlk satır Türkçe, ikinci satır İngilizce başlıktır.

**Günlük betik:** `python3 -I kod/bist_sinyal.py --veri ~/bist_veri --cikti tarama [--makro ~/bist_veri/makro.json] [--tarih YYYY-MM-DD]`. Varsayılan başlıklar, istekler arası 0,7 sn. `bist_tarama.py`'deki vadeli fiyatı hatası (ChartData fiyatı → %23,3) düzeltildi: iki betik de yalnız bülten uzlaşmasını, bültenin kendi tarihindeki spot kapanışıyla kullanır.

**Formüller:**
- İma basit oran: `i = (F_uzlaşma / S_kapanış − 1) × 365 / kalan_gün`. Bileşik: `(F/S)^(365/gün) − 1` (5.11 XU030 Aralık %33,1).
- F_USDTRY ima TL oranı: `((F/S) × (1 + r_USD × gün/360) − 1) × 365 / gün` (r_USD varsayımı %3,9; spot ChartData kapanışı, saat farkı ±1–2 puan).
- Kapanış seansı limitleri: alış `min(plan; P_son × 1,03)` aşağı adım; risk azaltan satış `max(taban; P_son × 0,97)` yukarı adım.
- Mevduat neti: basit `brüt × 0,825`; aylık yenilemeyle bileşik `(1 + brüt × 0,825 × 32/365)^(365/32) − 1`. %39,52 → %32,6 / %37,9.
- K1 z: `x = ln(SAHOL) − ln(AKBNK)`; `z = (x − ort60) / std60` (bugün dahil).
- K4 kontrat ya da adet: `floor(hesap × r₀ × çarpan / (stop_mesafesi × fiyat × kontrat_çarpanı))`. Pay vadelisinde kontrat = 100 pay; F_XU030 = 10 TL × endeks.
- K3 hedge kontratı: `floor(Σ(βᵢ × nominalᵢ) / (F_XU030 × 10))`.
- R_fazla ve stres: §8.1 ve §5.
- TSMOM12 eşiği (30.11): `XU100(28.11.2025) = 10.898,7` × (1 + 12 ay nakit) → %37,3 ile ~14.960; %45,5 ile ~15.860 ([TA] EK-4).

---

## 12. Kırmızı takım notları (06.11.2026 revizyonu)

Kırmızı takım 1 ön-ölüm yaptı ([R1]), kırmızı takım 2 sayı, tarih ve kuralları birincil kaynaklarla denetledi ([R2]). Bütün KRİTİK ve ÖNEMLİ bulgular uygulandı; KÜÇÜK bulguların hepsi ucuz olduğu için uygulandı. Hiçbir bulgu bütünüyle reddedilmedi; üçü değiştirilerek uygulandı (aşağıda **D**). Pazartesi 9.11'in işlemleri değişmedi (yalnız mevduat ve PPF çekirdeği).

| # | Bulgu | Ciddiyet | Durum | Nerede |
|---|---|---|---|---|
| R1-1 | Spot çıkış limiti (× 0,94) kriz günlerinde stopları çalıştırmıyor | KRİTİK | **D:** "limit = taban fiyatı" kapanış seansında reddedilir, çünkü emir son fiyattan en çok ±%3 sapabilir ([BİP], R2-1). Aynı amaçla limit = izin verilen en düşük fiyat = max(taban; P_son × 0,97). VİOP çıkış merdiveni ve 11. soru aynen | §3 ortak kurallar; §6.1; §6.2 |
| R1-2 | Plan dışı işlem için bütçe ve fren yok | KRİTİK | Uygulandı: K9 serbest kol, −%1,5 freni, plan dışı işlemde uydu 1 ay kâğıt, K6 kapalıyken short F_USDTRY yok | §3 K9; §5; §8.5 |
| R1-3 | Teminat kuralları kendi içinde çelişiyor | ÖNEMLİ | Uygulandı: L1–L3; L2 sırasına K9 eklendi (K6 → K7 → K2 → K9 → K1) | §1.3 m.6; §5 |
| R1-4 | 12.11 K4 girişleri SPK kararından ve uçurumdan önce | ÖNEMLİ | **D:** R1 metni hem "11, 12, 13.11'de giriş yok" hem "uzatıldıysa 13.11" diyordu; tutarlılık için 13.11 de girişsiz, uzatılırsa ilk giriş 16.11. Uzatılmazsa K4 23.11, VİOP-47 dışı long 30.11; her yeni bitiş tarihine aynen | §3.10 A2, A4; §7 |
| R1-5 | KRİZ kesicisi açık pozisyonlara dokunmuyor, teyitsiz CDS'e dayanıyor | ÖNEMLİ | Uygulandı: tetikler (a)–(f), açık pozisyon eylemi, −%4'te açık pozisyonlar yarıya, K6'da CDS yerine F_USDTRY ima; 12.11 rezerv tetiği; küresel şok notu | §2.1; §2.2; §5; K6 |
| R1-6 | MSCI kuralı yalnız Kasım'ı kapsıyor | ÖNEMLİ | Uygulandı: her gözden geçirme ve ad hoc duyuru; danışmada KRİZ, Blok 1 hakkı 0, K7 kapalı | §3.10 A3 |
| R1-7 | Aracı kurum riski ele alınmamış | ÖNEMLİ | Uygulandı: kurum seçimi, saklama kuralları, 12. soru | §1.3 m.7; §6.1 |
| R1-8 | USD ölçüsündeki kayıp yazılmamış | ÖNEMLİ | Uygulandı: §9.2 USD sütunu, yazılı ölçü seçimi, korumanın maliyeti, risk "bilinçli kabul" | §0 m.10; §9.2 |
| R1-9 | K1'de tek bacakla gece taşınabiliyor | KÜÇÜK | Uygulandı: ±%9 kontrolü, 18:08'de F_XU030 hedge'i | §3 K1 |
| R1-10 | KAPALI'da spot tavanı kolların toplamıyla çelişiyor | KÜÇÜK | Uygulandı: tavanı aşan yeni giriş öncelik sırasıyla reddedilir | §1.3 m.8; §5 |
| R1-11 | Belirsiz maddeler (bilanço ifadesi, A9 %8 fon başına ve veri kaynağı, SAHOL gerekçesi, Aralık devri) | KÜÇÜK | Uygulandı | §3.10 A1, A9, A10; §7.2 |
| R2-1 | Kapanış seansı yanlış tarif edilmiş (18:01–18:05, ±%3) | KRİTİK | Uygulandı: alış min(plan; P_son × 1,03), satış max(plan tabanı; P_son × 0,97), 18:08–18:10 yedeği, soru 5 | §3; §6.2 |
| R2-2 | AKCNS teklifi kapandı; fiyat 274,24; kayıt tarihi 18.06 | ÖNEMLİ | Uygulandı: AKCNS kalıcı çıktı; zorunlu teklifte kayıt tarihi varsayılan; K5 katkısı ~0 | §3 K5; §9.1 |
| R2-3 | Aday bilanço takvimi ters; AHGAZ/ENERY geri alımı | ÖNEMLİ | Uygulandı: ENJSA A1'den çıktı, AHGAZ/ENERY/RYSAS eklendi; AHGAZ+ENERY tek isim ve geri alım bayrağı; "98 > 97" kuralı silindi | §3.10 A1; §4.3; §4.4 |
| R2-4 | Bülten saatleri rutinle uyuşmuyor | ÖNEMLİ | Uygulandı: 18:15 spot / 20:45 VİOP | §6.3; §7.1; [RUT] |
| R2-5 | K1 komisyon kapısı testin üç katına izin veriyor | ÖNEMLİ | **D:** seçenek 1 (kapı ≤ 5 bps/bacak/yön), beklenti korundu; gerekçe aşağıda | §3 K1; §6.4 |
| R2-6 | K3'ün +%1,2'si ham getiri | ÖNEMLİ | Uygulandı: olay başı +%0,2…+%0,5, katkı +0,3; hedge'li sürüm tercih; [VO] %2–5 kovası uyarısı eklendi | §3 K3; §8.3; §9.1 |
| R2-7 | XU030 bileşik %33,1 | KÜÇÜK | Uygulandı | §1.2; §1.5 |
| R2-8 | Vadeli avantajı Kasım kontratından | KÜÇÜK | Uygulandı: Aralık oranları; koşul 3 "kullanılacak kontrat"; bugün long için pay vadelisi yok | §1.5; K4 |
| R2-9 | K6 boyutu 0,105x | KÜÇÜK | Uygulandı: 1 / 9 / 38 kontrat | §3 K6 |
| R2-10 | "3/3 uzatıldı" değil "2/2" | KÜÇÜK | Uygulandı | §3.10 A4 |
| R2-11 | K2 "20.10'dan beri kalıcı" değil; 03.11 yeniden kesişim | KÜÇÜK | Uygulandı; karar değişmedi (bayat) | §3 K2; [SİN] |
| R2-12 | Takvim: 4. dilim 01.01'e düşüyor; Ramazan Bayramı A7'yi kaydırıyor; §0'da 10/5 gün | KÜÇÜK | Uygulandı: 35 gün (04.01.2027); A7 ~15.03.2027 (teyit); §0 düzeltildi | §1.4; §3.10 A7; §0 m.8 |
| R2-13 | İç tutarlılık (stres örneği %2,94; çekirdek ≥ %85; 50–51/53; %8 [TE]; awk 18. sütun; M4 "ve düşüyor") | KÜÇÜK | Uygulandı | §5; §1.3 m.6; §3.11; A9; Ek A; §2.1 |
| R2-14 | VİOP emir tipleri belli (SAR, STJ, IKG; piyasa emri yok; akşam seansı yalnız endeks/metal) | KÜÇÜK | Uygulandı: sorular 6–7 değişti; akşam seansı istisnası | §6.1; §6.2; K7 |
| R2-15 | K1 tetikleri tam çözümle | KÜÇÜK | Uygulandı: 91,10 / 82,35 ve 62,78 / 69,44; [SİN] her akşam çözer | §3 K1; §10 |

**Değiştirilerek uygulananların üçüncüsü (D):** R2-5'te iki seçenekten kapı seçildi, çünkü aktif bireysel VİOP komisyonu (on binde 1–4 + %5 BSMV + borsa payı on binde 0,3) 5 bps'nin altında kalabiliyor ve kenarı testteki maliyetle korumak, beklentiyi kesmekten daha ucuz.

**Testi geçen ve bilerek değiştirilmeyen kurallar ([R1] §3):** Kural 0; mevduat dilimlerinin bozulmaması; kredili işlem yasağı; K6 kapısı ve brüt rezerv ≥ 160; dışlama listesi; R_fazla ölçü birimi; stres tavanı; Blok 1 sayımı; KAPALI'da K4'ün yalnız sonda olması; çift kollarının piyasa-nötr sayılması.

**v_olay ile gelen değişiklikler (kırmızı takım dışı):** K3b doğrulandı ve pilota alındı; A5 [D] oldu; A7 yalnız boyut eğilimi; K8 primi +%33–38'e indi ve satış "E kapanış satışı" oldu; geri alım izleme listesi kaldırıldı ([VO] §0, §5).
