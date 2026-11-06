# BIST / VİOP swing planı (nihai): başlangıç Pazartesi 9.11.2026

- **Hazırlanma:** Cuma 06.11.2026, ~15:00 TSİ. Fiyatlar aksi yazılmadıkça 05.11.2026 kapanışı ve 05.11 resmî VİOP uzlaşması. Cuma 6.11 kapanışıyla yeniden hesaplanacak kalemler §10'da.
- **Nasıl üretildi:** Hakemlerin iki kez seçtiği C taslağı ("önce risk, kanıt minimalisti") iskelet olarak alındı. A'nın rejim merdiveni ve kırılım motoru ile mevduat ağırlığı eklendi. B'nin engel muhasebesi, Kural 0, zorunlu akış takvimi ve ZPAT hak sahipliği kontrolü eklendi. Hakemlerin bulduğu bütün ölümcül/ciddi kusurlar düzeltildi (liste §11.3). Taslaklardan sonra gelen iki olay çalışması (`olay_bedelsiz`, `olay_akis_rejim`) işlendi. **`dogrulama/v_olay.md` bu plan yazılırken hâlâ yoktu.** Bu iki rapora dayanan getiri iddiaları kâğıt üzerinde kaldı; maliyetsiz kaçınma kuralları ihtiyatla canlıya alındı.
- **Kanıt etiketleri:** **[D]** doğrulanmış (v_* dosyalarında DOĞRU/KISMEN ve yeniden üretilmiş). **[DM]** doğrulanmamış ajan bulgusu. **[TE]** test edilmemiş kural tasarımı (risk kontrolü). **[L]** literatür.
- Yatırım tavsiyesi değildir. Kaldıraçlı VİOP'ta teminatın tamamı, teminat tamamlama ile daha fazlası kaybedilebilir. Bütün olasılıklar öznel tahmindir.

**Kaynak kısaltmaları** (yollar `raporlar/2026-11-06_kazanc_stratejileri/` altına göre; çelişkide doğrulama dosyası esas)

| Kısa | Dosya | Kısa | Dosya |
|---|---|---|---|
| [VB] | `dogrulama/v_bist.md` | [BT] | `ajanlar/bist_test.md` |
| [VC] | `dogrulama/v_capraz.md` | [BS] | `ajanlar/bist_swing_kenarlar.md` |
| [VD] | `dogrulama/v_dalga.md` | [DB] | `ajanlar/dalga_bist.md` |
| [VP] | `dogrulama/v_profesyonel.md` | [TM] | `ajanlar/tr_makro_engel.md` |
| [OB] | `ajanlar/olay_bedelsiz.md` [DM] | [TP] | `ajanlar/tr_profesyonel.md` |
| [OA] | `ajanlar/olay_akis_rejim.md` [DM] | [SE] | `ajanlar/seytan_taban_oranlar.md` |
| [HA] | `ajanlar/olay_halka_arz.md` | [KK] | `ajanlar/bist_kim_kazaniyor.md` |
| [HZ] | `uygulama/bist_hafta_hazirlik.md` | [TR] | `uygulama/tarama/bist_tarama_20261105.md/.csv`, kod `uygulama/kod/bist_tarama.py` |
| [TA] [TB] [TC] | `uygulama/taslak/bist_A.md`, `bist_B.md`, `bist_C.md` | [HK] [HU] [HD] | `uygulama/taslak/bist_hakem_kanit.md`, `_uygulama.md`, `_deger.md` |
| [KO] | `../2026-10-28_viop_komite_raporu.md` | [PL] | `../2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` |
| [BÜL] | Borsa İstanbul VİOP günlük bülteni `https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv` | | |

---

## 0. Yönetici özeti (10 satır)

1. **Rejim bugün KAPALI.** XU100 11.333, SMA200'ün %16,5 altında. 12 aylık momentum kapalı (+%3,8'e karşı nakit ~%37–45). Makro tetiklerin hiçbiri yok. Likit evrende 52 hafta kırılımı veren hisse yok.
2. **Pazartesi yapılacak tek finansal işlem çekirdeğin kurulması.** Hesabın %15'i 32 günlük mevduata (1. dilim) ve %85'i banka iştiraki PPF'ye. Kalıcı hedef %60 mevduat (4 haftalık dilim: 9/16/23/30.11) ve %40 PPF.
3. **Pazartesi açılmayanlar:** hisse veya endeks long, short F_USDTRY (brüt rezerv 158,1 < 160), XU030 nakit-taşıma (ima %29,3 < mevduat neti %32,6), opsiyon. DİBS yalnız %0 stopaj yazılı teyit edilirse.
4. **Pazartesi kurulacaklar:** aracı kuruma 10 yazılı soru (Kural 0: teminat faiz kazanmıyorsa VİOP kolu yok), kapanış bazlı alarmlar, dışlama listesi, işlem günlüğü.
5. **Rejimden bağımsız açık kalan doğrulanmış kollar (sinyal gelirse):** SAHOL↔AKBNK 20 günlük oran dönüşü (VİOP, t+1 kapanış girişi) ve temettü hak kullanımından önceki 5 gün (spot; alış gün −6, satış gün −1).
6. **Rejim dönerse devreye girecek yukarı motor:** 52 hafta kırılımı + trend şablonu + %15 iz-stop. Boyut KAPALI'da işlem başı %0,25 risk (en çok 2 sonda), GEÇİŞ'te %0,5, AÇIK'ta %0,75. En yakın tetikler kapanış > ENJSA 127,00 / AHGAZ 48,70 / ENERY 14,60; üçü tek küme sayılır.
7. **Kaçınma takvimi:**
   - 9.11 akşamı bilanço açıklayanlara giriş yok.
   - 11.11 kapanışında hiçbir kolda yeni giriş yok.
   - MSCI'ın 12.11'de çıkardığı ya da ağırlığını düşürdüğü hisseler 30.11'e kadar alınmaz.
   - Kredili esneklik 13.11'de uzatılmazsa 16–20.11 kırılım girişi yok; 27.11'e kadar VİOP-47 dışında long yok.
   - Bedelsiz ve yüksek verimli temettüde hak gününden sonra 10 gün alış yok.
   - 10.12 PPK sonrası banka aşırı ağırlığı yok.
8. **Ölçüm birimi:** Her kol engele göre fazla getiriyle ölçülür, öldürülür ve büyütülür: R_fazla = (net K/Z − bağlanan nakit × engel × gün/365) / risk. Ham R kullanılmaz.
9. **Dürüst beklenti (12 ay, vergi sonrası, engele göre):** merkez **+1,5…+2,5 puan**, %80 aralık **−2…+6**. Toplam net nominal TL getirisi ~%33–38, reel ~%3–8. Engelin altında kalma olasılığı ~%35–45. KAPALI rejim sürerse yalnız +1…+1,5 puan. Rejim 1–3 ayda dönerse kırılım ve endeks kollarından +3…+8 puan, kârın çoğu birkaç işlemden.
10. **"Yüksek getiri" cevabı:** Bu rejimde kanıtın tavanı engel artı birkaç puan. +10–20 puan hedeflemek 3–5 kat risk ve engele göre −%25…−%40 düşüş toleransı ister; kanıt bunu desteklemiyor ([VB] §2.1, [VD] B2, [SE] §5.1).

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
| 32 gün mevduat merdiveni (≥2 büyük banka) | ~%5,06 | %32,6 / ~%37,9 | Banka riski (TMSF limitini bankadan teyit et); vade bozulursa faiz yanar; her yenilemede indirime göre düşer | **Çekirdeğin ana gövdesi** | [VC] #4 |
| Banka iştiraki PPF (en az 2 fon) | ~%4,54 | ~%29,6 / ~%34–35 | Günlük likidite. Tasfiyedeki 15 PPF'nin 4'ü −%95…−%99,9 kaybetti → **yalnız mevduat bankası iştiraki PYŞ**; ters repo karşı tarafında grup ihracı olmayan fon. Tasfiyedeki 7 PYŞ (Pardus, Hedef, Atlas, Bulls, Pusula, A1, Tera) asla | **Likidite tamponu ve VİOP teminat kaynağı** | [VB] §3 m.3; [VB] #5; [TB] §1.2 |
| ≤12 ay vadeli DİBS | ~%5,2 | ~%39 bileşik (stopaj %0 ise) | Süre riski; S4'te hisseyle aynı yönde kaybeder | **Koşullu, ≤%10,** mevduat payından. Yalnız aracı kurum/banka 9–30.11 alımlarında %0 stopajı **yazılı** teyit ederse | [VC] #8; [HZ] §4c |
| XU030 nakit-taşıma (BIST30 BYF/sepet long + F_XU0301226 short) | %4,49 brüt, vergisiz | %29,3 / %32,2 | Takip hatası, teminat, temettü | **Bugün HAYIR.** Basitle basit: %29,3 < mevduat neti %32,6. Açma kuralı §1.5 | [VP] T12; [VC] §2 m.1 |
| Short F_USDTRY (TL carry) | — | Fazla getiri nominalin ~%8–12'si/yıl, %10 stopaj öncesi | Negatif çarpık. 2010–26 Sharpe −0,51, MaxDD −%90; tek ayda −%24…−%35. Prim daralıyor (28 → 22 → 17 → ~13 puan). USD teminat ~%0 kazanır | **Çekirdek değil.** Kapılı uydu K6, bugün 0 | [VC] #19, §2 m.3; [TM] §4.3; [BS] §8.1 |

Not (hata düzeltmesi): Tarama dosyası ve hazırlık notu §0 m.8, XU030 Aralık için %23,3 ima faiz veriyor. Bu **yanlış**, çünkü yanlış vadeli fiyatı (14.605) kullanılmış. Resmî uzlaşma 14.734'tür ([VP] T12). Bütün ima oran hesapları yalnız [BÜL] uzlaşmasıyla yapılır; taramanın VİOP tablosu kullanılmaz.

### 1.3 Karar: rejime göre dağılım (hesabın %'si)

| Kalem | KAPALI (bugün) | GEÇİŞ | AÇIK |
|---|---|---|---|
| 32 gün mevduat merdiveni | **%60** (4 × %15) | %50 | %30 |
| Banka iştiraki PPF (uydu kovası ve VİOP teminatı dahil) | **%40** | %50 | %70 |
| İçinden uydu spot sermayesi, azami | %15 | %25 | %40 |
| VİOP başlangıç teminatı, azami | %15 | %20 | %25 |

Kurallar:
1. **Mevduat ağırlığı A'dan alındı.** Faiz sabitken mevduat PPF'den ~3 puan fazla kazanır; PPF'den mevduata kaydırılan her %15 hesaba risksiz ~+0,45 puan ekler ([HD] §2; [VC] #4). Sınırı likidite ihtiyacı belirler.
2. **Dilim takvimi:** 9.11, 16.11, 23.11 ve 30.11'de birer dilim (%15) açılır. Henüz bağlanmamış dilimler PPF'de bekler, yani PPF Pazartesi %85'tir ve 30.11'de %40'a iner ([TA] §1.3). Böylece her hafta hesabın %15'i vadeye gelir.
3. **Rejim yükselirse:** Uydular önce PPF'den, sonra vadesi gelen dilimden fonlanır. Vadesi gelen dilim yenilenmez, PPF'ye aktarılır. **Hiçbir dilim vadesinden önce bozulmaz.**
4. **Kredili işlem (spot kaldıraç) hiçbir rejimde yok.** Örtük maliyeti ~%60 ([VB] #3).
5. **20 mn TL hesap:** Mevduat en az 3 bankaya, PPF en az 2 PYŞ'ye bölünür.

### 1.4 Pazartesi uygulaması: 1 / 5 / 20 mn TL

| Kalem | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| Mevduat 1. dilim (%15, 32 gün), 9.11 | 150 bin | 750 bin | 3 mn (≥3 banka) |
| Mevduat 2., 3., 4. dilim (16, 23, 30.11) | 3 × 150 bin | 3 × 750 bin | 3 × 3 mn |
| PPF, 9.11 (kalıcı %40 + geçici %45) | 850 bin | 4,25 mn | 17 mn (≥2 PYŞ) |
| PPF, 30.11 sonrası (kalıcı %40) | 400 bin | 2 mn | 8 mn |
| DİBS (yalnız yazılı %0 stopaj teyidiyle; 4. dilimin yerine) | ≤100 bin | ≤500 bin | ≤2 mn |
| Çekirdeğin beklenen aylık net getirisi (~%2,5–2,7, faiz sabitse) | ~25–27 bin | ~125–135 bin | ~0,50–0,54 mn |
| Pazartesi açılan uydu pozisyonu | Yok | Yok | Yok |

### 1.5 İki açma kuralı (her akşam [BÜL] ile; karşılaştırma **basitle basit**)

- **İma basit oran:** i = (F_uzlaşma / S_kapanış − 1) × 365 / kalan gün. 5.11'de XU030 Aralık: (14.734 / 14.101 − 1) × 365/56 = **%29,3**. Bankalarda Kasım: GARAN %25,2, AKBNK %26,3, YKBNK %28,0 ([TB] Ek A; [TA] EK-6).
- **XU030 nakit-taşıma açılır:** i ≥ (32 gün mevduat brüt × 0,825) + 3 puan **ve** Kural 0 (§6.1) sağlanıyorsa. Bugün eşik %32,6 + 3 = %35,6 → **kapalı.** Açılırsa: BIST30 BYF ya da ≥10 hisselik BIST30 sepeti alınır, aynı kapanışta F_XU030 satılır, vadede kapanır ([TB] §1.5; [VC] §2 m.1).
- **Long için pay vadelisi:** Yalnız şu koşulların hepsi sağlanırsa (A'nın 8–13 puanlık bileşik/basit hatası düzeltildi; [HK] §3.1 m.4, [HD] §4):
  1. (Serbest kalan nakdin fiilen yattığı aracın net basit oranı − i) ≥ 3 puan. Bugün mevduata göre bankalarda ~4,6–7,4 puan, PPF'ye göre ~1,6–4,4 puan.
  2. Kural 0 sağlanıyor (teminat faizli ya da PPF/DİBS teminat kabul ediliyor).
  3. Ön ay açık pozisyon ≥ 20.000 kontrat ve günlük hacim ≥ 100 mn TL.
  4. Kurum teminat oranı ≤ %35.
  5. Kasım kontratı yeni pozisyonda kullanılmıyor.
- **Spotta kalma:** İma oran < %15 ya da negatifse (ör. ENJSA Kasım −%10,4) KAP'ta temettü veya sermaye işlemi aranır. Açıklanamıyorsa spot kullanılır ([TA] §2.1.3).

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
| M4 | CDS 5 yıl < 230 | evet | Günlük | ~248 (bağımsız teyit yok) | 0 | [TM] §5.1; [VC] §1 sonu |
| M5 | XBANK kapanış > kendi SMA200'ü | evet | Her kapanış | 16.085 vs 16.955 (−%5,1) | 0 | [TA] §3.1; [HZ] §4a |
| Bilgi | Yabancı hisse akımı (TCMB) | **Sayılmaz** | Perşembe 14:30 | Son hafta −66,3 mn $; 6 hafta −334,5 mn $ | — | [OA] §3: akım getiriyi izliyor, 2021–26'da ileri getiri anlamsız [DM] |
| Bilgi | Genişlik, sektör endeksleri | Sayılmaz | Cuma | BIST100'ün %13'ü SMA200 üstünde; hiçbir sektör endeksi SMA200 üstünde değil | — | [HZ] §4a, §6 |
| Bilgi | Brüt rezerv (yalnız K6 kapısı) | ≥ 160 mlr $ | Perşembe | 158,1 (önceki 162,2) | — | [KO] §4.2; [VC] #18 |

Makro eşikler 4 tarihî örnekten türetilmiş öznel eşikler; hayatta kalma ve rejim bağımlılığı yüksek ([TM] §5.3). Rejim filtresi getiri kaynağı değil, risk kontrolüdür ([BT] §6).

### 2.2 Durumlar ve izinler

| Durum | Tanım | İzinler | Kanıt |
|---|---|---|---|
| **AÇIK** | T1 = 1 (sinyal gününün kapanışında) | K4 tam boy (r₀ %0,75), K7 yalnız T2 = 1 ise, ekleme serbest | Test edilen kapı: S5 = kırılım + XU100 > SMA200, placebo üstü +%5,7, t 5,4 [D] ([BT] §5.1; [VB] #28) |
| **GEÇİŞ** | AÇIK değil **ve** T3 = 1 **ve** M1 = 1 **ve** {M2, M4, M5}'ten ≥ 1 | K4 yarım boy (r₀ %0,5), ekleme yok, K7 yok | [TE]: test edilmedi, bu yüzden yarım boy |
| **KAPALI** | Diğer bütün durumlar. **Bugünkü durum.** | K4 yalnız sonda (r₀ %0,25, en çok 2); K1, K3, K5 serbest (rejimden bağımsız); K6 kapıya bağlı; K7 kapalı | — |
| **KRİZ kesicisi** (her durumun üstünde) | XU100 bir haftada ≥ %8 düşer **ya da** USDTRY 10 iş günlük artışı yıllıklandırılmış > %35 **ya da** CDS > 300 | 5 işlem günü hiçbir kolda yeni giriş yok; K6 kapanır; mevcut stoplar işler | [TE]; [TC] §3.1; [KO] §4.2 |

- **Değerlendirme:** Durum her kapanışta (18:15) hesaplanır ve ertesi işlem gününden geçerli olur.
- **Düşüşler:** Mevcut K4 pozisyonlarını kapatmaz (testteki çıkış iz-stoptur). Yalnız yeni girişleri ve boyutu etkiler. K7 kendi çıkış kuralıyla kapanır.

### 2.3 Bugün ne diyor (05.11)

**KAPALI: 7 göstergenin 0'ı açık.** İzinler:
- Çekirdek ≥ %85; toplam açık risk ≤ %2,5; stres ≤ %6.
- K1 ve K3 sinyal gelirse açılabilir (K1 için önce Kural 0).
- K4 yalnız sonda; K6 kapalı (kapı); K7 kapalı.

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
- **Spot giriş ve çıkış:** Kapanış seansına (18:00–18:10, tek fiyat) limitli emir. Önceden girilemiyorsa emir toplama aşamasında (18:00'dan sonra ~18:07'ye kadar; tam saat aracı kurumla teyit) girilir. **Sabah normal limitli emir verilmez:** Sürekli işlemde dolar, kapanış fiyatı olmaz ([HU] §7).
- **VİOP:** 17:50–18:08 arasında limitli emir. Piyasa emri hiç kullanılmaz ([PL] §5). Pay vadelisi ve USDTRY'de akşam seansı yok ([HZ] §5).
- **Tavan kilidi:** Giriş günü hisse tavanda kilitliyse (≥ +%9,5) emir atlanır ([BT] §1, gerçekçi dolum).
- **Taban kilidi:** Çıkış emri her gün yenilenir.
- **Bilanço:** Sinyal kapanışı ile giriş kapanışı arasında finansal tablo açıklanacaksa giriş yok. Açıklamadan sonraki ilk kapanışta sinyal yeniden değerlendirilir [TE].
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
- 17:55'te iki bacak birden limitli emirle girilir. Limit = karşı en iyi fiyat ± %0,3 (alınan bacak üstü, satılan bacak altı).
- 18:05 kontrolü: Bir bacak dolmadıysa o bacağın limiti ± %0,6'ya çekilir.
- 18:08'de hâlâ tek bacak varsa dolan bacak ertesi gün 17:55'te aynı kuralla kapatılır ve "dolum hatası" diye kaydedilir.

**Çıkış:**
- **Zaman:** Girişten sonraki 20. işlem günü, aynı emir yöntemiyle, z ne olursa olsun.
- **Felaket stopu:** Bir kapanışta çift K/Z'si bacak nominalinin ≤ −%8'i ise ertesi gün çıkılır [TE: testte yok, kuyruk sigortası].
- **Kurumsal olay:** Sabancı/Akbank pay yapısı, birleşme ya da pay alım teklifi açıklanırsa ertesi gün çıkılır ve kol askıya alınır.

**Vade:**
- Pay vadelisi **fiziki teslimatlı**. Kasım bacakları en geç **25.11 kapanışında** kapatılır ya da Aralık'a devredilir.
- 20 günlük süre 30.11'i aşacaksa giriş doğrudan Aralık kontratıyla yapılır. Şart: Aralık alış-satış makası ≤ %0,3. Aralık hacmi 5.11'de SAHOL 22 mn TL, AKBNK 118 mn TL ([TC] §2.1).

**Boyut:**
- Bacak başına hesabın **%7,5'i** nominal; her rejimde aynı.
- Felaket stopu riski ≈ %0,6; tek bacak −%15 gap stresi ≈ hesabın −%1,1'i.

**Kapılar (hepsi gerekli):**
1. Kural 0 (§6.1).
2. Komisyon yön başına ≤ 15 bps (BSMV dahil).
3. Aracı kurum çift teminatını yazılı bildirmiş.

**Beklenti:**
- İşlem başına net **+80…+180 bps** (backtest'e %40 çürüme/seçim iskontosu); isabet %60–70; yılda ~5 işlem.
- Hesaba katkı merkez **+0,4 puan/yıl**, aralık 0…+0,9.
- Teminat faizsiz nakitse ~0,6 puan/yıl sürtünme kenarı sıfırlar; bu yüzden Kural 0 ([TC] §2.1).

**Bugün:**
- z = **−0,72**, sinyal yok.
- Yaklaşık tetikler (diğer bacak sabitken): z = +2 için SAHOL ≥ 90,85 ya da AKBNK ≤ 62,94; z = −2 için SAHOL ≤ 82,52 ya da AKBNK ≥ 69,30. Her akşam yeniden hesaplanır.

**Eski sürüm:** Kullanıcının 1–3 günlük SAHOL/AKBNK sinyali emekliye ayrılır. Aynı çiftte iki sinyal çalıştırılmaz ([PL] §1; [HK] §5 m.6).

### K2. KCHOL↔iştirak sepeti oran dönüşü (isteğe bağlı; varsayılan kâğıt)

**Kanıt [D]:** Bir gün gecikmeyle +128 / +175 bps, t 2,1 / 2,1; maliyet (40 bps) sonrası ~+88 / +135 bps ([VB] #25).

**Kural:**
- Sepet TUPRS, FROTO, TOASO, ARCLK, YKBNK, AYGAZ. AYGAZ'ın VİOP'u yok: sinyal 6 hisseyle hesaplanır, işlem 5 bacakla yapılır.
- Diğer her şey K1 gibi; boyut yarım (KCHOL %5, sepet 5 × %1).
- **Yalnız yeni kesişimde girilir:** z, |z| < 2'den |z| ≥ 2'ye geçtiği ilk kapanış; giriş t+1. Uzun süredir açık "kalıcı" sinyallerin kanıtı karışık: 2010–18 −53 bps (n=35), 2019–26 +272 bps (n=26) ([TC] §2.2; [HK] §3.3).

**Kapılar:** ≥ 5 mn TL hesap, komisyon yön başına ≤ 8 bps, Kural 0. Aksi halde yalnız kâğıt üzerinde kayıt.

**Bugün:** z = +2,23, ama sinyal 20.10'dan beri açık (kalıcı) → **giriş yok.** KCHOL ve ARCLK bilançosu 9.11 akşamı.

**Beklenti:** İşlem başına +40…+90 bps; katkı ~0…+0,15 puan. İlk kapatılacak kol.

### K3. Temettü hak kullanımı öncesi 5 gün (yalnız spot; rejimden bağımsız)

**Kanıt [D]:**
- [BS] §5.3: n=1.109, [−5,−1] ortalama +%1,2, medyan +%0,8.
- [VB] #26: Haftalık kümelemeyle **t 6,5**; ortalama 17 yılın hepsinde pozitif, medyan 2014 ve 2026'da negatif; maliyet sonrası ~+%0,9.
- Kenar yalnız spotta var: VİOP temettüyü önceden fiyatlıyor ([PL] §2).

**Kural:**
- **Evren:** 60 günlük medyan TL hacme göre ilk 100 hisse, dışlama listesi (§4.2) hariç. KAP'taki kâr payı bildirimine göre brüt temettü / son kapanış ≥ %2 ve < %5. (≥ %5 olanlar K3b'nin konusu; K3b canlı değilken K3 bunları da kapsar.)
- **Takvim:** Gün 0 = hak kullanım günü, temettüsüz ilk işlem günü.
- **Alış:** Gün −6'nın kapanış seansında limitli emir; limit = gün −7 kapanışı × 1,04. B'nin gün −5'i bir gün geçti; [−5,−1] penceresi gün −6 kapanış girişi ister ([HK] §3.2 m.4).
- **Satış:** Gün −1'in kapanış seansında limitli emir; limit = önceki kapanış × 0,94. Hak kullanımına girilmez, temettü alınmaz.
- **Stop:** Pencere içinde kapanış giriş × 0,92'nin altındaysa ertesi kapanışta çıkılır [TE].
- **Boyut:** Olay başına %3,5. ≥ 5 mn TL hesapta beta hedge'li olay başına %5. Eşzamanlı en çok 3 olay; aynı kümeden en çok 2.
- **Hedge (≥ 5 mn TL):** Toplam K3 nominali × β ≥ 1 F_XU030 nominali (~147 bin TL) ise, aşağı yuvarlanmış kontrat sayısıyla F_XU030 satılır. Hedge maliyeti yalnız (mevduat neti − ima) ≈ 3,3 puan/yıl'ın 7 güne düşen payı. TUPRS, PETKM ve ASELS'te XU030 hedge'i işe yaramaz, hedge'e katılmaz ([PL] §3).
- **11.11 kuralı:** Gün −6 = 11.11 Çarşamba ise olay atlanır (§3.10).

**Beklenti:**
- Olay başına net **+%0,5…+%0,7** (%30 iskonto); isabet %55–65 (medyandan çıkarım); olay kuyruğu −%5…−%10.
- Sezon Mart–Haziran. Kasım–Aralık'ta olay az; kol büyük olasılıkla boş kalır.
- Katkı merkez **+0,5 puan/yıl**, aralık 0…+1,2.

### K3b. Yüksek verimli temettü duyuru koşusu (KÂĞIT; önceden kayıtlı pilot)

**Kanıt [DM], tek ajan "hızlı bakış":** [OB] §0 ve §8.
- **Bulgu:** Duyuru verimi ≥ %5 olan nakit temettülerde (N=400), duyurudan sonraki ilk kapanışta alıp hak −1 kapanışında satmak: BHAR (XU100'e göre) **+%8,5**, medyan +%6,5, t 11,1, isabet %74, medyan 28 işlem günü.
- **Dönem ve sağlamlık:** 2024–26'da +%14,4 (N=67, t 7,6); 12 yılın 12'sinde pozitif; XUTUM ve XYUZO kıyasıyla da +%7,6–8,2.
- **Uyarılar:** İptal edilen teklifler örnekte yok (hayatta kalma). Genel kurul tutarı değiştirebilir. Duyuru yıllık sonuçlarla çakışıyor, yani etkinin bir kısmı kazanç sürprizi olabilir. Hisselerin %29'unda tavan kilidi bilgisi yok. Ajanın kendisi ayrı ve bağımsız bir yeniden test öneriyor.
- Bu, çalışmadaki en büyük ve en tutarlı yeni kenar, ama doğrulanmadı. Bu yüzden canlı kol değil.

**Bugün: yalnız kâğıt.** 9.11'den itibaren KAP'taki her uygun ilk "Kâr Payı Dağıtım İşlemlerine İlişkin Bildirim" kâğıt günlüğe yazılır.

**Canlıya geçiş koşulları (hepsi):**
1. `v_olay.md` ya da bağımsız bir yeniden test, bir günlük gecikmeli girişte işlem başına BHAR ≥ +%4 ve t ≥ 3 buluyor.
2. Etki likit ilk 100'de ve 2024–26'da pozitif.
3. İptal edilen teklifler eklenince etki < %50 küçülüyor.
4. ≥ 10 kâğıt olay.

**Pilot kural (koşullar sağlanırsa; Şubat–Mayıs 2027 sezonu):**
- **Evren:** İlk 100 likit, dışlama hariç. YK teklifindeki brüt temettü / bildirimden önceki kapanış ≥ %5.
- **Giriş:** Bildirim 18:00'den önceyse aynı gün kapanış seansında, sonraysa ertesi gün. Limit = önceki kapanış × 1,04; tavan kilidinde atlanır.
- **Çıkış:** Hak −1 kapanış seansı. Genel kurul tutarı %20'den fazla düşürür ya da iptal ederse ertesi kapanışta.
- **Stop:** Kapanış giriş × 0,88'in altındaysa ertesi kapanışta [TE].
- **Boyut:** Olay başına %2,5; eşzamanlı en çok 4; aynı hissede K3 açılmaz. ≥ 5 mn TL'de K3 gibi beta hedge.
- **Beklenti (gerçekse, %50 iskontoyla):** olay başına +%3…+%6 fazla; katkı +0,5…+2 puan/yıl. **Merkez beklentiye katılmadı.**

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
- Limitli alış; limit = t kapanışı × 1,06.
- Tavan kilidinde atlanır; ertesi kapanışta koşullar sürüyorsa yeniden denenir.
- Bilanço kuralı (ortak kurallar).
- 18:00'de erişim yoksa yedek: t+1 açılış seansında (09:40–09:55) limit = t kapanışı × 1,03. Test edilmedi; günlükte işaretlenir ([TA] §2.1 m.7).

**Çıkış:**
- **E1, iz-stop:** Kapanış ≤ girişten beri en yüksek kapanış × 0,85 → ertesi gün kapanış seansında satış; limit = önceki kapanış × 0,94; taban kilidinde her gün yenilenir.
- **E2, süre:** 120 işlem günü (testte de 120). Hedef fiyat ve kısmi kâr alma yok: Kısmi satış tam da kârın geldiği sağ kuyruğu keser ([TA] §2.1).
- **E3, yedek felaket emri:** Aracı kurum sunucu taraflı şartlı emir sunuyorsa tetik = en yüksek kapanış × 0,80, limit = tetik × 0,97; her Cuma güncellenir [TE]. Sunmuyorsa koruma yalnız boyuttur.
- **E4, dışlama:** Hisse VBTS tedbirine girerse, SPK listesine eklenirse ya da fon payı / fiili dolaşım > %20 olursa ertesi kapanışta koşulsuz çıkış [TE].
- **E5, büyük kazanç:** Pozisyon ≥ +%100 kâra ulaşırsa iz-stop %15'ten %10'a iner [TE].
- **E6, bedelsiz:** Pozisyondaki hissede oranı ≥ %500 bir bedelsizin hak günü gelirse hak −1 kapanışında satılır [TE]. Dayanak: [OB] §7, hak sonrası 10 günde −%6,1, t −3,3. Daha düşük oranlarda testteki kural korunur.

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

**Spot mu vadeli mi?** Yalnız VİOP-47'de ve §1.5'teki koşullarla pay vadelisi kullanılır. Nominal spot formülünü aşamaz. Devir vadeden 3 iş günü önce (Kasım için 25.11). Yeni vadenin günlük hacmi < 20 mn TL ise pozisyon spota taşınır.

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
2. **Hak sahipliği:** Bilgi formunda "kimler katılabilir" okunur. Teklif "kontrol devrinin kamuya açıklandığı tarihte pay sahibi olanlara" yapılıyorsa, sonradan alınan pay teklife verilemez → **işlem yok.** PEKGY kararındaki ifade SPK 2026/58'de; AKCNS metninde tarih kaydı yok ([TB] K4; [HK] §3.2).
3. Teklif sahibi grup dışı ve mali gücü belgelenmiş (yabancı sanayi şirketi, banka vb.). Grup içi fon krizi teklifleri hariç.
4. Teklif penceresi fiilen başlamış.
5. Spot ≤ teklif × (1 − toplam maliyet − PPF net faizi × kalan gün/365 − %2 güvenlik payı).
6. Pay, teklif süresi içinde aracı kuruma verilen katılım talimatıyla teklife verilir; teklif sonrası tutulmaz.

**Boyut:** Olay başına ≤ %5, toplam ≤ %10. Teklif iptali senaryosunda −%20 varsayımıyla olay riski ≤ %1.

**Beklenti:** Yılda 0–3 olay; katkı 0…+0,5 puan, merkez +0,1.

**Bugün:**
- AKCNS: SPK 2026/59 Heidelberg için 260,25 TL ile 5,627434 $'ın TL karşılığından yüksek olanı onayladı; hisse 184,5 TL. Halka açık piyasa değeri 24.09–07.10 arasında 8,1 mlr TL'den 2,2 mlr TL'ye düştü; bu, teklifin uygulanıp kapandığıyla tutarlı ([TC] §2.5; [HK] §2).
- **Açık olduğu KAP'tan teyit edilmedi → işlem yok.** Bugün nitelikli olay yok.

### K6. TL carry, short F_USDTRY (koşullu; Pazartesi 0)

**Kanıt:**
- [VC] #19 [D]: 07/2023–10/2026 yıllık %20,8 USD, ama 2018 −%11,4, 2021 −%30,3, en kötü aylar −%24.
- Sharpe 2,2 örneklem içi; rejim başlangıcı bilinerek seçildi ([VB] §2.6).
- Prim ~13 puana daraldı ([TM] §4.3). Carry ile banka long'u aynı şokta birlikte kaybeder ([VC] §2 m.8).
- B'nin Pazartesi açılışı kaldırıldı. Kaynağı ([KO] §4.2) "brüt rezerv < 160 → çık" diyor ve değer 158,1.

**Açılış kapısı (hepsi):**
1. Swap hariç net rezervin 2 haftalık değişimi ≥ −2 mlr $ ve seviye ≥ 20 mlr $.
2. Haftalık yabancı DİBS akımı ≥ −500 mn $.
3. CDS ≤ 275.
4. USDTRY 10 iş günlük artışı yıllıklandırılmış ≤ %30.
5. **Brüt rezerv ≥ 160 mlr $.**
6. Kural 0.

**Kapanış (herhangi biri; ertesi kapanışta):**
- Net rezerv < 15 mlr $ ya da haftalık değişim ≤ −5 mlr $.
- Yabancı DİBS akımı ≤ −1 mlr $/hafta.
- CDS > 300.
- 10 günlük hız > %35.
- Brüt rezerv < 160.
- Uzlaşma ≥ giriş × 1,04.
- Siyasi/hukuki şok (erken seçim, TCMB yönetim değişikliği, repo ihalesinin durması): o günün kapanış penceresinde.

**Boyut:**
- ≤ 0,10x nominal: 1 / 5 / 20 mn TL'de 2 / 9 / 38 Aralık kontratı (1 kontrat ≈ 52,3 bin TL).
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
- 1x'i aşmaz (2x'te MaxDD −%69; [BT] §2). Akşam seansı kullanılmaz.

**Bugün:** KAPALI. T2 için XU100 ≈ 15.860 gerekir; 2026 içinde pratikte imkânsız ([TA] §3.2). 12 ay ilk 3 küme RAFİNERİ, HOLDİNG, KOZA_ALTIN; üçünün de 3 aylık getirisi negatif → filtre nakit ([TA] §2.2).

**Beklenti:** Açık olduğu yıllarda nominalin +%4…+%7'si (rf üstü), yani %20'de +1…+1,5 puan. Sahte sinyal yıllarında −1…−3 puan.

### K8. Halka arz katılımı (isteğe bağlı; risk bütçesi dışında)

**Kanıt:** Arz başına medyan +%45, ama hesap başına yılda 10–27 bin TL ([HA] §0, §3b). 3 Eylül'den beri halka arz onayı yok ([HZ] §1a) → bugün 0.

**Kural:**
- Yalnız eşit dağıtımlı arzlara katılınır; talep PPF teminatıyla verilir.
- Tavan serisi bittiği günün kapanışından sonra ertesi sabah açılış seansında satılır (limit = önceki kapanış × 0,97).
- **Seri bittikten sonra asla alınmaz:** 52/53 düştü (doğrulamaya göre ~50–51/53), medyan −%55; seri sonrası 21 günde medyan −%11 ([VB] #11; [HA] §0).

**Katkı:** 1 mn TL'de +1…+2,7 puan, 20 mn TL'de ~0. Merkez beklentiye katılmadı.

### 3.10 Kaçınma kuralları (bütün kollar; zorunlu akış alfası değil, kayıptan kaçınma)

| # | Olay | Kural | Kanıt |
|---|---|---|---|
| A1 | Konsolide 3Ç son günü, **9.11 akşamı** (KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK; tarihsiz kalanlar EREGL, ARCLK, KRDMD, ASTOR, GUBRF, HEKTS, OYAKC, CIMSA, ENJSA, TKFEN, TRALT, TRMET, EKGYO, VESTL, ODAS). Bankalar 19.11 | Bilanço gecesi bu isimlerde pozisyon taşınmaz, yeni giriş yok. İlk karar Salı 10.11 kapanışı | [HZ] §2; [TE] |
| A2 | **11.11 Çarşamba kapanışı** (MSCI 12.11 01:00) | Hiçbir kolda yeni giriş yok. Salı sinyalleri Perşembe 12.11 kapanışında (t+2) uygulanır | [TA] §2.1 m.6; [TE] |
| A3 | **MSCI Kasım** (duyuru 12.11 01:00, yürürlük 30.11 kapanışı). Artışlar dondu, azaltmalar sürüyor | Çıkarılan ya da FIF/NOS'u düşürülen hisse 30.11 kapanışına kadar alınmaz; K4/K7'de tutuluyorsa 12.11 kapanışında çıkılır. 01.12'de evrene döner | [VC] #17; [HZ] §0 m.4 |
| A4 | **Kredili esneklik** (%35 → %20) 13.11 seans sonunda bitiyor. Karar 12–13.11 SPK bülteninde; şimdiye kadar 3/3 uzatıldı | **Uzatılmazsa:** 16–20.11 hiçbir yeni K4 girişi yok; 16–27.11 VİOP-47 dışında hiçbir kolda yeni uzun pozisyon yok; düşen hisse "dipten" alınmaz. K1 normal. **Uzatılırsa** değişiklik yok | [VB] #7; [HZ] §0 m.3; [BT] §4 (kısa vadeli dönüş BIST'te kaybettiriyor) |
| A5 | **Bedelsiz hak günü** | Hiçbir kolda bedelsiz hak gününe yeni pozisyonla girilmez. Hak günü dahil 10 işlem günü yeni alış yok (−%3,3, t −6,1); oran ≥ %500 ise 20 gün (−%7,2). YK duyurusunda, başvuruda ya da SPK onayında **alış yok**: duyuru etkisinin tamamı tavan kilitli günlerde, kilitsiz giriş 5 günde −%1,8; onay → hak −1 net −%0,07; başvuru → hak −1, 2024–26 medyan −%2,9 | [OB] §0, §5, §6, §7 [DM, büyük N; 12 yılın 12'sinde aynı yön; 2024–26'da zayıflamış] |
| A6 | **Temettü (verim ≥ %5) hak günü** | Hak günü dahil 5 işlem günü yeni alış yok (−%2,1, t −7,7). K3/K3b pozisyonları asla hak gününe taşınmaz | [OB] §8 [DM]; [BS] §5.3 ([+1,+5] −%0,6) |
| A7 | **Banka zamanlaması, 10.12 PPK** | Karar anket medyanının (%35) ±25 bp içindeyse ("sürprizsiz indirim"): 11.12.2026–10.03.2027 (63 işlem günü) arasında BANKA kümesinde yeni K4 girişi yarım boy ve en çok 1. K7'nin banka payı F_XU030'a gider; rejim dönüşünün ilk aracı F_XU030 olur, F_XLBNK değil. Şahin sürprizde ya da sabit kararda kısıt yok | [OA] §4.2, §4.5 [DM]: indirimden 63 gün sonra XBANK/XU100 6/6 döngüde negatif (ort. −%6,3, t −4,2); sürprizsiz indirimlerde −%6,6 (n=24); bankalar 63 günde zaten +%26 koştu |
| A8 | Bedelli (rüçhan) duyurusu | Kural yok, yalnız bilgi. Duyuru [0,1] −%2,8, sonrasında anlamlı drift yok | [OB] §8 |
| A9 | BIST30 blok kilidi ~03.02.2027'de açılıyor; fon uyumu 31.01.2027; tasfiye ~17.03.2027 | 29.01–05.02.2027 arasında K1'de yeni giriş yok (SAHOL arzı). 31.01.2027'ye kadar K3/K4'te VİOP-47 dışı hisselerde fon payı / fiili dolaşım ≥ %8 olanlar alınmaz. Dışlama listesi en az 17.03.2027'ye kadar geçerli | [VP] T7, T8; [TP] §4.5; [TB] K4 |
| A10 | Vade günü | Kasım pay vadelisi yeni pozisyonda kullanılmaz; açık bacaklar en geç 25.11 kapanışında kapanır ya da devredilir. Vade gününe pozisyon taşınmaz | [HZ] §1b, §5 |

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
| Geri alım ve içeriden alım taklidi | Kontrol düzeltmeli kenar yok; içeriden alımda işaret ters (60 günde −%3,35, t −1,7). VİOP'lu geri alım programı yalnız zayıf aday (n=41) → izleme listesi | [OA] §0, §2.3; [VB] #18 |
| Yabancı akımına göre işlem veya rejim tetiği | Akım fiyatı izliyor, öngörmüyor | [OA] §3 [DM] |
| PEAD | Literatür, doğrulanamadı → yalnız kâğıt kaydı | [VB] #21 |
| Kredili spot | Örtük maliyet ~%60 | [VB] #3 |
| Halka arzda tavan serisi sonrası alım | 50–52/53 düştü | [VB] #11 |
| Eski 4 lead-lag sinyali | 2024–26'da t 1,0–1,2. XU030 baz sıçraması 18:10–18:15 ekranı istiyor. SAHOL/AKBNK 1–3 gün → K1 ile değiştirildi. **Diğerleri kâğıt.** Canlı sürdürülecekse toplam açık risk ≤ %0,5 ve bu bütçe K4 sondalarından düşülür | [PL] §1, §5 |

---

## 4. Evren, dışlama listesi, kümeler, güncel adaylar

### 4.1 Evren

| Kol | Evren |
|---|---|
| K1 / K2 | İlgili VİOP pay vadelileri |
| K3 / K3b | Tarama evreni (VİOP-47 ∪ BIST100) içinde 60 günlük medyan TL hacme göre ilk 100 |
| K4 | Aynı sırada **ilk 75** (test top75 evreninde MaxDD −%27; [BT] §5.2), ≥ 252 işlem günü geçmişi olan. Öncelik VİOP-47; diğerleri spot × 0,75 |
| K7 | F_XU030 ve küme sepetleri için VİOP-47 |

Likidite sırası ([TC] §4.1, 248 hisselik önbellek): ENERY 36, ENJSA 48, AHGAZ 63 → K4'e uygun. ISDMR 106, GLYHO 136 → dışında. RYSAS hesaplanamadı; Pazartesi kontrol edilecek.

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
| **Bu plan:** ENERJİ_DAĞITIM | ENJSA, AHGAZ, ENERY: aynı iş (gaz/elektrik dağıtımı). Korelasyonu ölçülmedi; ihtiyaten **tek küme** ([TA] §4.3) |

- **Güncel küme durumu:** 12 ay RS ilk 3 RAFİNERİ (+%26,5), HOLDİNG (+%23,9), KOZA_ALTIN (+%18,9). 126 günlük RS kırılımı BANKA ve HAVACILIK. Filtreli kurallar nakitte. Düşen piyasada RS liderliği büyük ölçüde düşük beta demektir ([VD] §5 m.3).
- **Çift kolları:** K1/K2 piyasa-nötr oldukları için Blok 1 sayımına girmez. Ama ikisi aynı anda açıksa Blok 1'in yönlü pozisyon hakkı yarıya iner ([TC] §4.3).

### 4.4 Güncel adaylar (05.11 kapanışı; Cuma 6.11 ve Pazartesi kapanışıyla yenilenir)

**Nitelikli (giriş koşulu bugün sağlanmış): yok.**

**Bekleyenler:**

| Kol | Aday | Tetik (kapanış >) / koşul | Son | Gereken | Not |
|---|---|---|---|---|---|
| K4 | **ENJSA** (VİOP-47) | **127,00** (17.04.2026 zirvesi) | 119,30 | +%6,5 | TT 7/7, RS 93. Bilanço ≤ 9.11 akşamı → en erken karar Salı kapanışı. Kasım vadelisi ima oranı anormal (−%10,4) → **spot**. β 0,60 |
| K4 | **AHGAZ** (spot) | **48,70** | 46,00 | +%5,9 | TT 7/7, RS 98; × 0,75 |
| K4 | **ENERY** (spot) | **14,60** | 13,80 | +%5,8 | TT 7/7, RS 97; ATR yüksek; × 0,75 |
| K4 | RYSAS (spot) | 30,28 | 26,68 | +%13,5 | Likidite sırası teyit edilmedi; bist_test evreninde yoktu ([VB] §2.4) |
| K4 izleme (TT eksik) | KCHOL | 225,50 | 202,30 | +%11,5 | 6/7 (fiyat < SMA50 211,11); Blok 1 |
| K4 izleme | BIMAS | 433,75 | 369,25 | +%17,5 | 6/7 |
| K4 izleme | TUPRS | 409,90 | 331,75 | +%23,6 | 6/7; ayrıştırıcı küme |
| K4 izleme | GARAN | 158,59 | 142,00 | +%11,7 | 3/7 → kırılsa bile S2 değil, **giriş yok** |
| K1 | SAHOL↔AKBNK | \|z\| ≥ 2 | z −0,72 | — | Yaklaşık tetikler §3 K1 |
| K2 | KCHOL↔sepet | Yeni kesişim | z +2,23 (kalıcı) | — | Giriş yok |
| K3 | KAP: 30 gün içindeki hak kullanımları | Verim %2–5, ilk 100 | — | — | Cuma akşamı taranır |
| K5 | AKCNS | KAP'ta açık teklif + hak sahipliği | — | — | Teyit yok → işlem yok |
| K6 | Carry | Kapı (6 koşul) | 3 koşul sağlanmıyor | — | En erken 19.11 |
| K7 | Endeks/küme | T1 ve T2 | 0 / 0 | — | — |
| İzleme (sinyal değil) | VİOP'lu geri alım programları: GARAN (04.11), SAHOL (16.10), GUBRF, TCELL, ODAS (26.10) | — | — | — | [OA] §0 m.4 [DM, zayıf aday] |

**Kural:** ENJSA, AHGAZ ve ENERY tek küme. KAPALI'da üçü birden tetiklenirse yalnız ENJSA alınır (VİOP-47 önceliği). GEÇİŞ'te ikinci isim RS'si yüksek olan (AHGAZ 98 > ENERY 97).

---

## 5. Risk limitleri

| Limit | KAPALI | GEÇİŞ | AÇIK | Gerekçe |
|---|---|---|---|---|
| K4 işlem başı risk r₀ | %0,25 | %0,50 | %0,75 (en çok %1,0, §8.4) | Tıraşlanmış SR'nin ≤ ¼ Kelly'si ([SE] §3.3, §5.3) |
| K4 azami açık pozisyon | 2 | 4 | 6 | — |
| Küme başına yönlü pozisyon | 1 | 2 | 2 | Küme tek bahis; ρ 0,8'de 5 pozisyon ≈ 1,19 bahis ([SE] §3.6) |
| Blok 1 yönlü pozisyon | 1 | 2 | 3 | Korelasyon 0,77–0,79 ([VD] B12) |
| Tek hisse spot nominal | %3,5 | %3,5 | %7,5 (ekleme dahil) | 3 ardışık taban (−%27): ≤ %1 / ≤ %2 |
| **Toplam açık stop riski** (K1 felaket stopu + K3 stopları + K4 r₀ + K5 olay riski + K6 nominal × %4) | **%2,5** | %3,5 | %5,5 | [TC] §5; [TB] §5 |
| **Stres tavanı** (her Cuma) | **%6** | %8 | **%10** | A'nın %60 brüt sınırının yerine bağlayıcı ([HU] §5 m.2) |
| VİOP başlangıç teminatı | ≤ %15 | ≤ %20 | ≤ %25 | Serbest teminat her zaman ≥ 2 × kullanılan başlangıç teminatı |
| Net endeks betası (Σ β × nominal) | ≤ +%10 | ≤ +%25 | ≤ +%40 | — |
| Aylık uydu kaybı (çekirdeğe göre) | −%2,5 → ay sonuna kadar yeni giriş yok | −%2,5 | −%3 | — |
| Birikimli uydu düşüşü (çekirdeğe göre) | −%4 → bütün uydu boyları yarıya, 3 ay. −%6 → uydu kapanır, 3 ay kâğıt | aynı | −%6 → yarıya; −%10 → uydu kapanır | [SE] §5.2 m.8 küçük ölçekli uyarlama |
| Kredili işlem, opsiyon satışı | Yok | Yok | Yok | [VB] #3; [BS] §8.3 |

**Stres formülü** (B'nin formülü, C'nin senaryosu; [TB] §5; [TC] §5):

Stres_TL = 0,19 × (Blok 1 dışı uzun hisse + endeks nominali) + 0,25 × (Blok 1 uzun nominali) + 0,30 × (short F_USDTRY nominali) + 0,15 × (çift kollarında tek bacak nominali) + 0,05 × (beta hedge'li K3 nominali) − (tanımlı riskli korumanın azami ödemesi; bu planda 0).

- Varsayımlar: 2 ardışık taban (−%19), bankalar −%25, USDTRY +%30, çift bacağı −%15.
- Örnek (KAPALI, 1 mn TL, her şey dolu): K1 (tek bacak 75 bin) → 11,3 bin; K3 3 × 35 bin hedgesiz → 20 bin; K4 2 × 16,7 bin → 6,3 bin; K5 50 bin → 9,5 bin. Toplam **~47 bin = %4,7 < %6.**
- AÇIK'ta çiftler açıkken toplam uzun nominal en çok ~(%10 − ~%2) / 0,19–0,25 ≈ **%30–40.** A'nın %60'ı fiilen bu formülle sınırlanır.

**Bütçe bağlayınca öncelik:** K1 > K3 > K5 > K4 > K2 > K6. K7 yalnız AÇIK'ta ve en sonda.

**Limit kilidi:**
- Pay ve VİOP günlük limiti ±%10; taban serisinde stop dolmaz. 2026'da ODINE 29 ardışık taban yaptı ([VB] #27).
- Spot kilitliyken pay vadelisi olayların %83'ünde kilitli ([PL] §2). Pay vadelisi çıkış yolu değildir.
- Bu yüzden koruma boyutla yapılır: tek hisse sınırı, dışlama, likidite filtresi, %25 stop mesafesi.
- Rutin gece hedge'i yapılmaz: 1–3 günlük riskin ~%11'i gecede oluşuyor ([PL] §3).

**En kötü hafta (bu kurulumla, 9–13.11 ve 16–20.11):**
- İki K4 sondası iki taban: 2 × %1,67 × %19 ≈ −%0,6.
- Bir K1 bacağı −%15 gap: −%1,1.
- Toplam ≤ ~**%1,8**; %6 stres tavanının içinde.
- Pazartesi uydu pozisyonu olmadığı için ilk hafta pratikte ~0.

---

## 6. Uygulama

### 6.1 Kural 0 ve aracı kuruma yazılı sorular

**Kural 0:** VİOP nakit teminatı faiz kazanmıyorsa **ve** PPF/DİBS teminat olarak kabul edilmiyorsa hiçbir VİOP kolu açılmaz (K1, K2, K6, K7, vadeli finansman, K3 hedge'i). Nakit teminat TLREF'in %80'inden az kazanıyorsa VİOP kollarının boyutu yarıya iner. Gerekçe: boştaki teminatın maliyeti teminat × ~%33 ([SE] §5.1 sıra 0; [VC] §2 m.2).

**Cevap gelene kadar:** Yalnız spot kollar (K3, K4 spot, K5) açılabilir. Pazartesi için bir son saat yok ([HU] §3).

**Sorular** (Cuma akşamı e-postayla; [TC] §6.3 ve [TB] §1.3 birleşimi):
1. VİOP nakit teminatı nemalandırılıyor mu? Oranı ne (TLREF'in yüzdesi)?
2. PPF katılma payı ve DİBS VİOP teminatı olarak kabul ediliyor mu? Kesinti oranları ne?
3. Kurum teminat oranları: F_SAHOL, F_AKBNK, F_KCHOL, F_TUPRS, F_FROTO, F_TOASO, F_ARCLK, F_YKBNK, F_ENJSA, F_XU030, F_USDTRY. SAHOL–AKBNK çiftinde mahsup var mı? (Takasbank asgarisi XU030 %11,4, pay vadelileri %12,7–17,0; QNB örneği XU030 %20, çoğu pay vadelisi %33,3; [VB] #16, [HZ] §5.)
4. Komisyon, yön başına, BSMV dahil, spot ve VİOP ayrı. Hedef VİOP ≤ on binde 1,5, spot ≤ on binde 2.
5. Kapanış seansı için emir önceden (sabah) girilebiliyor mu? Girilemiyorsa emir toplama aşamasının tam saatleri ne?
6. Sunucu taraflı şartlı (stop-limit) emir ve geçerlilik süresi.
7. Takvim yayılımı (vade devri) emri var mı?
8. 9–30.11 arasında alınacak DİBS'te stopaj %0 mı? Yazılı olarak.
9. Pay vadelisinde vade öncesi zorunlu kapatma ve fiziki teslimat süreci; son işlem günü.
10. ZPAT'a katılım talimatı kanalı ve son saati; F_USDTRY %10 stopajında zarar mahsubu.

### 6.2 Emir tipleri ve saatler (TSİ; [HZ] §5)

| İş | Seans | Emir | Ne zaman |
|---|---|---|---|
| Spot giriş (K3, K3b, K4, K5) | Kapanış seansı 18:00–18:10 | Limitli. K3/K3b limit = önceki kapanış × 1,04; K4 limit = t kapanışı × 1,06 | Önceden girilebiliyorsa sabah; girilemiyorsa 18:00 sonrası emir toplama aşaması. Tek bir 10 dakikalık pencere; ekran takibi değil |
| Spot çıkış | Kapanış seansı | Limitli; limit = önceki kapanış × 0,94. Taban kilidinde her gün yenilenir | Aynı |
| VİOP çift girişi ve çıkışı (K1, K2) | Normal seans, 18:10'a kadar | Limitli; karşı fiyat ± %0,3 → 18:05'te ± %0,6 | 17:55–18:08 |
| VİOP K6 / K7 / hedge | Normal seans | Limitli, kapanışa yakın | 17:50–18:05 |
| Vade devri | Normal seans | Takvim yayılımı emri, yoksa iki limitli emir | Kasım için en geç 25.11 |
| Şartlı emir | — | Yalnız K4'te yedek felaket emri (E3), sunucu taraflıysa | Cuma 18:30 güncellenir |
| Piyasa emri | — | **Hiç kullanılmaz** | — |
| Akşam seansı (19:00–23:00) | Yalnız endeks vadelileri | Kullanılmaz. İstisna: KRİZ kesicisi gecesinde mevcut K7 pozisyonunu azaltmak | — |

### 6.3 Günlük ve haftalık rutin

**Her kapanış, 18:15–18:45 (~20–30 dk):**
1. `python3 bist_tarama.py --veri ~/bist_veri --cikti ../tarama` (kod klasöründe).
2. [BÜL] `viop_YYYYMMDD.csv` indirilir; ima oranlar hesaplanır.
3. K1/K2 z-skorları; K4 iz-stoplar ve yeni B52 tetikleri; K3 takvimi.
4. Rejim tablosu (§2.1).
5. Ertesi günün emirleri hazırlanır; günlüğe yazılır.

**Bildirim:** Bekleme listesindeki her hisse için kapanış bazlı alarm (ör. "BIST:ENJSA, Kapanış > 127,00, bar kapanışında bir kez"). XU100 > 12.691 (SMA50) ve > 13.572 (SMA200) alarmları da kurulur. Alarmlar 18:15'te okunur ([TA] §2.1 m.8).

**Haftalık, Cuma 18:30 (~45 dk):** rejim, stres, açık risk, dışlama listesi (VBTS, MSCI, bedelsiz/temettü takvimi), K6 kapısı, mevduat dilimi, yedek felaket emirleri.

### 6.4 Maliyetler ve kol kapatma eşikleri

| Kalem | Değer | Kaynak |
|---|---|---|
| Borsa payı | Endeks vadeli on binde 0,4; pay ve döviz vadeli on binde 0,3 | [HZ] §5 |
| Aracı kurum komisyonu | Banka liste fiyatı on binde 8–10; aktif bireyde on binde 1–4 (teyitsiz); üzerine %5 BSMV | [HZ] §5 |
| Test maliyet varsayımları | K1 20 bps, K2 40 bps gidiş-dönüş; K4 25 bps (50 bps streste yılda −1,4 puan); K3 ~30 bps | [VB] #25, §2.6 |
| **Kol kapatma eşikleri** (yön başına, BSMV dahil) | VİOP > 15 bps → K1 kapalı. > 8 bps → K2 kapalı. Spot > 15 bps → K3 kapalı. K4 toplam gidiş-dönüş > 40 bps → yalnız VİOP-47 | [TC] §6.2; [TA] §6 |
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

1. 18:20 sonrası tarama (6.11 kapanışı). §4.4 tetikleri, TT puanları, SMA50/200, XBANK güncellenir. Tarama 6.11 seans sonrası TUPRS, ENKAI, ULKER, BRSAN bilançolarından önce kapanışı yakalar.
2. ~18:30 sonrası `viop_20261106.csv` indirilir (komut Ek A). F_XU030 Aralık uzlaşmasından ima oran yeniden hesaplanır; Pazartesi kararında bu değer kullanılır.
3. K1/K2 z-skorları 6.11 kapanışıyla.
4. KAP taraması:
   - 9.11–11.12 arasındaki temettü hak kullanımları (verimleriyle).
   - Açık ZPAT'lar ve AKCNS'nin durumu.
   - Bedelsiz hak günleri (kaçınma listesi).
5. Aracı kuruma §6.1'deki 10 soru.
6. En az 2 bankadan 32 gün mevduat teklifi. PPF izahnamesinden ücret, ters repo karşı tarafı ve emir saat sınırı (çoğunda 13:30; teyit).
7. Dışlama listesi emir ekranında "yasak" olarak işaretlenir. Günlük şablonu ve hipotez kartları tarihlenir.

### 7.2 9–13 Kasım

| Gün | Saat | Olay ([HZ] §1a) | Yapılacak | Yapılmayacak |
|---|---|---|---|---|
| **Pzt 9.11** | 09:00–12:00 | Konsolide 3Ç son günü; Hazine ihaleleri | Çekirdek: mevduat 1. dilim %15 (32 gün), PPF %85. DİBS yalnız yazılı %0 teyidiyle | Gün içi ekran yok |
| | 18:15–18:45 | Akşam bilanço yağmuru (§3.10 A1) | Rutin. Bilanço açıklamayan bir isimde K4 tetiği gelirse Salı kapanışına emir. K1'de \|z\| ≥ 2 ise Salı 17:55 emirleri | Bilanço açıklayan isimlerde emir yok |
| **Sal 10.11** | 10:00 / 16:30 | Eylül sanayi üretimi; ABD Ekim TÜFE | Eylem yok | Bilanço gap'i kovalanmaz ([BS] §3.3) |
| | 18:15 | Bilanço sonrası ilk temiz kapanış | Pazartesi akşamı açıklayanlar (ENJSA dahil) için K4 yeniden değerlendirilir. Sinyal varsa giriş **Perşembe 12.11** kapanışında (A2) | — |
| **Çar 11.11** | kapanış | MSCI 12.11 01:00 | Yalnız rutin ve kayıt | **Hiçbir kolda yeni giriş yok** |
| **Per 12.11** | 07:00 | MSCI sonuçları | Çıkarılan ve ağırlığı düşen hisseler 30.11'e kadar evrenden çıkar; elde varsa kapanışta satılır (A3) | MSCI akışına karşı işlem yok |
| | 10:30 | TCMB Enflasyon Raporu | Bilgi | — |
| | 14:30 | Rezerv + haftalık menkul kıymet | M1 (1. hafta), K6 kapısı, brüt rezerv | — |
| | 18:00 | — | Salı/Çarşamba K4 sinyalleri (en çok 2 sonda) | — |
| | akşam | SPK bülteni | Kredili esneklik kararı okunur | — |
| **Cum 13.11** | 10:00 | Ödemeler dengesi | Bilgi | — |
| | seans sonu | Esneklik bitiyor | Uzatılmadıysa A4 kısıtları 16.11'den itibaren | — |
| | 18:30 | — | Haftalık gözden geçirme; stres; mevduat 2. dilimi Pazartesi | — |

### 7.3 16–30 Kasım

| Tarih | Olay | Plan |
|---|---|---|
| Pzt 16.11 | Mevduat 2. dilim | A4 uygulanıyorsa: K4 girişi yok (20.11'e kadar), VİOP-47 dışı long yok (27.11'e kadar) |
| 18.11 | FOMC tutanakları (tahmini) | Bilgi |
| Per 19.11 | Banka konsolide son günü (HALKB); 14:30 rezerv (2. hafta) | Bilançosu gelecek bacakta K1 girişi yok. M1 2. hafta; K6 kapısının ilk olası açılışı |
| 13 veya 20.11 | Kasım Piyasa Katılımcıları Anketi (tarih teyitsiz) | 10.12 için anket medyanı not edilir (A7 eşiği) |
| Pzt 23.11 | Mevduat 3. dilim | — |
| **Çar 25.11** | Kasım pay vadelisi | Açık Kasım bacakları kapanışta kapatılır ya da devredilir (A10) |
| **Per 26.11** | 14:30 rezerv (3. hafta) | **M1 olası 1.** T3 ve M4/M5'ten biri de 1 ise GEÇİŞ 27.11'den geçerli |
| Cum 27.11 | TCMB Finansal İstikrar Raporu; A4'ün VİOP-47 dışı kısıtının son günü | Haftalık gözden geçirme |
| **Pzt 30.11** | VİOP Kasım vadesi; MSCI kapanışta; ay sonu | T2 hesabı. 12 ay küme RS sıralaması (K7 filtresi). Mevduat 4. dilim; PPF %40'a iner. Aylık rapor (§8.5) |
| Sal 01.12 | — | MSCI listesi evrene geri döner |

### 7.4 Aralık 2026 – Haziran 2027

| Tarih | Olay | Plan |
|---|---|---|
| Per 3.12 10:00 | Kasım TÜFE | M2'nin 1. ayı |
| Per 10.12 | PPK (anket %35) | A7 banka kuralı; çekirdek faizleri yenilenir |
| 21–23.12 | Devir haftası | Aralık VİOP pozisyonları Şubat/Ocak'a devredilir ya da kapatılır |
| 24–31.12 | Stopaj süresi bitiyor | 2027 stopaj oranlarına göre çekirdek araçları yeniden seçilir ([VC] §2 m.6) |
| Per 31.12 | Aralık vadesi (XU030, USDTRY, pay vadelileri) | Devredilmeyen her şey kapanmış olmalı |
| ~4.1.2027 | Aralık TÜFE | M2'nin 2. ayı; M2 en erken burada 1 olur |
| 29.01–05.02.2027 | Blok kilidi (~3.2) ve fon uyumu (31.1) | A9: K1'de yeni giriş yok |
| Şubat–Mayıs 2027 | Temettü duyuru ve hak sezonu | K3 en aktif dönem; K3b canlıya geçiş koşulları kontrol edilir |
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
hedef_giris_fiyati (t+1 kapanis), gerceklesen_fiyat, kayma_bps, dolum_hatasi(E/H),
arac (spot/F_kodu), adet_veya_kontrat, nominal_TL, hesap_yuzdesi, teminat_TL, teminat_faizi,
stop_mesafesi, R_TL, ima_tasima_orani (VIOP ise),
cikis_tarihi, cikis_nedeni (E1..E6/zaman/felaket/kurumsal/rejim/kural_disi), cikis_fiyati,
brut_TL, komisyon+BSMV_TL, stopaj_TL, net_TL, R,
PPF_ayni_donem_% (engel), baglanan_nakit_TL, fazla_TL, R_fazla,
MAE_%, MFE_%, gun_sayisi, XU030_ayni_donem_%, kural_sapmasi(E/H)+not
```

Kâğıt kolları (K2 kalıcı sinyaller, K3b, PEAD, eski lead-lag sinyalleri, geri alım izleme) aynı alanlarla ayrı sayfada tutulur.

### 8.3 Hipotez kartları (09.11.2026 tarihli; değiştirilemez)

| Kol | Mekanizma | Beklenen net / işlem | İsabet | İşlem/yıl | 1R | Beklenen R_fazla | Denenen varyant |
|---|---|---|---|---|---|---|---|
| K1 | Holding–iştirak fiyat sapmasının sınırlı arbitrajla kapanması | +80…+180 bps (bacak nominali) | %60–70 | ~5 | Bacak × %8 | +0,08…+0,2 | 108 hücre ([BS] §9.1) |
| K2 | Aynı | +40…+90 bps | %55–60 | ~5 | Bacak × %8 | +0,03…+0,1 | Aynı |
| K3 | Temettü öncesi talep | +%0,5…+%0,7 (piyasa düzeltmeli) | %55–65 | 25–40 | Pozisyon × %8 | +0,05…+0,08 | Az |
| K3b (kâğıt) | Yüksek verimli temettüye kayma | +%3…+%6 (iskontolu) | %65–75 | 10–25 | Pozisyon × %12 | +0,25…+0,5 | Tek ajan, birkaç eşik ([OB] §8) |
| K4 | Zirve kırılımında gecikmeli tepki; kazananı koşturma | AÇIK'ta R_fazla 0…+0,3; KAPALI'da ≈ 0 | %40–45 | KAPALI 0–5, AÇIK 20–40 | Nominal × %15 (%25) | 0…+0,3 | 25 kombinasyon, 36 portföy varyantı ([BT] §5) |
| K5 | Zorunlu teklifle sabitlenen fiyat | +%2…+%8 | %80–90 | 0–3 | Pozisyon × %20 | +0,1…+0,4 | Test yok |
| K6 | Carry primi (satılmış kuyruk) | Nominalin ayda ~%0,7–0,9'u | aylık %80+ | Kapıya bağlı | Nominal × %4 | — | 1 kural |

### 8.4 Ölçekleme (boyut artırma)

**Genel kural:** 12 ay dolmadan ve aşağıdaki minimum işlem sayısına ulaşmadan hiçbir kolda boyut artmaz. Bu sürede yalnız küçültme ya da kapatma kararı verilir ([SE] §5.3 m.4).

**Minimum işlem sayıları:**

| Kol | Minimum | Tahmini süre |
|---|---|---|
| K1 | 20 işlem | ~4 yıl |
| K2 | 20 işlem | ~4 yıl |
| K3 | 60 olay | ~2 sezon |
| K4 | 40 kapanmış işlem | — |

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
| K3 temettü −6/−1 | +0,5 | 0…+1,2 | Sezon (Mart–Haziran), olay kuyruğu |
| K3b (kâğıt; canlıya geçerse) | 0 (geçerse +0,5…+2) | — | Doğrulama |
| K4 sondaları | 0 | −0,3…+0,3 | Rejim |
| K5 özel durumlar | +0,1 | 0…+0,5 | Olay bulunması |
| K6 carry | +0,1 | −3…+0,6 | Kur şoku (negatif çarpık) |
| **Toplam, KAPALI** | **≈ +1…+1,5** | **−2…+3** | |
| Rejim dönerse ek (K4 tam boy + K7) | +3…+8 | −4…+15 | Sağ kuyruk; sahte sinyalde negatif |

Çekirdeğin mevduat ağırlığı (%60), tümü PPF'de tutulan bir çekirdeğe göre risksiz ~+1,5–1,8 puan ekler. Bu katkı engelin içinde sayıldı, uydu fazlasına eklenmedi.

### 9.2 Senaryo bazında (olasılıklar öznel, [TM] §5.2)

| Senaryo | Olasılık | Çekirdek net (nominal) | Uydu fazlası (puan) | Hesap toplamı (net nominal TL) |
|---|---|---|---|---|
| S1 sönümlenme, rejim 1–6 ayda döner | %35 | %30–33 (hızlı indirim) | +3…+8 | %34–40 |
| S2 yatay kanama, carry kazanır | %40 | %33–37 | 0…+2,5 | %33–38 |
| S3 kontrollü kur hızlanması | %15 | %35–38 | −1…+1,5 | %34–39 |
| S4 kırılma (kur +%15–30, acil faiz artışı) | %10 | %38–45 | −4…−1 | %35–43 nominal; USD bazında belirgin negatif |
| **Ağırlıklı** | | **~%33–36** | **≈ +1,5…+2,5** (%80 aralık −2…+6) | **≈ %34–38** |

**Dağılımın özellikleri:**
- P(12 ayda engelin altında) ≈ **%35–45.**
- Engele göre kötü %10'luk kuyruk −3…−5 puan; stres tavanıyla sınırlı.
- İyi %10'luk kuyruk +8…+15 puan; S1 ile kırılımın sağ kuyruğu birlikte gelirse.
- Reel karşılık ~%3–8.

### 9.3 TL karşılıkları (uydu fazlası; merkez +1,5…+2,5, %80 aralık −2…+6)

| Hesap | Merkez | %80 aralık | Halka arz eklentisi (onaylar başlarsa) |
|---|---|---|---|
| 1 mn TL | +15…+25 bin TL | −20…+60 bin | +10…+27 bin |
| 5 mn TL | +75…+125 bin | −100…+300 bin | Aynı TL (yüzde olarak küçük) |
| 20 mn TL | +300…+500 bin | −0,4…+1,2 mn | Aynı TL (~0 puan) |

Kapasite 20 mn TL'ye kadar bağlayıcı değil. İstisnalar: K1/K2 Aralık kontrat derinliği ve K4'te hacmin %2 sınırı.

### 9.4 "Yüksek getiri" sorusuna açık cevap

1. **Bu rejimde yılda engel + 1…3 puan, merkez ~+2.** Getirinin %90'ından fazlası çekirdekten gelir. Uydunun bugünkü asıl değeri, rejim dönüşüne hazır, ölçülmüş ve maliyeti bilinen bir süreçtir.
2. **Rejim dönerse yılda +3…+8 puan.**
   - Koşul: M1 ile T3 ya da T1 açılmalı ve kırılım ile endeks kolları devreye girmeli.
   - Kârın >%50'si birkaç işlemden gelir.
   - 2017/2020/2022 tipi bir yılda iki haneli fazla mümkün, ama planlanamaz ([TA] §8.2).
   - Rejim kırılmalarından sonra bankaların 3–6 ayda dolar bazında +%40–90 kazandığı gözlem n = 4 ([TM] §2.3), ve [OA] §4 bunun PPK sonrası zamanlamasının aleyhinde.
3. **+10–20 puan isteniyorsa:** Bu planın 3–5 katı açık risk (%8–12), engele göre −%25…−%40 düşüş toleransı ve sağ kuyruğa bağımlılık gerekir ([SE] §5.1). Kanıt bu rejimde bunu desteklemiyor:
   - Kırılım portföyü 2024–26'da engelin 2–8 puan altında ([VB] §2.1).
   - 456 küme kuralının 0'ı rf'yi geçti ([VD] B2).
   - 3 yılda hisse fonlarının neredeyse hiçbiri PPF'yi geçmedi ([VP] T1–T2).
4. **En büyük doğrulanmamış yukarı olasılık K3b.** Doğrulanırsa Şubat–Mayıs 2027 sezonundan +0,5…+2 puan ekleyebilir. Doğrulanmadan para konmaz.

---

## 10. Pazartesi 9.11.2026 kontrol listesi

**Cuma 6.11 akşamı / hafta sonu**
- [ ] `bist_tarama.py` (6.11 kapanışı). §4.4 tetikleri yeniden hesaplanır (zirve52 tuzağına dikkat: bugünü hariç tut). RYSAS'ın likidite sırası kontrol edilir.
- [ ] `viop_20261106.csv` indirilir; XU030 Aralık ima oranı **uzlaşmayla** hesaplanır; §1.5 iki açma kuralı kontrol edilir (beklenen: ikisi de kapalı).
- [ ] K1 z (05.11: −0,72) ve K2 z (+2,23, kalıcı) 6.11 kapanışıyla.
- [ ] KAP: 9.11–11.12 temettü hak kullanımları (K3: verim %2–5, ilk 100; ≥ %5 olanlar K3b kâğıt), bedelsiz hak günleri (A5), açık ZPAT'lar, AKCNS.
- [ ] Aracı kuruma §6.1'deki 10 soru. Cevap gelmeden VİOP kolu yok.
- [ ] 2 banka mevduat teklifi; banka iştiraki PPF seçimi (tasfiyedeki 7 PYŞ asla; KAP portföy raporunda grup ihracı yok; emir saat sınırı).
- [ ] Dışlama listesi (§4.2) emir ekranında "yasak".
- [ ] Alarmlar (kapanış bazlı): ENJSA 127,00; AHGAZ 48,70; ENERY 14,60; RYSAS 30,28; KCHOL 225,50; BIMAS 433,75; TUPRS 409,90; XU100 12.691 ve 13.572; XBANK 16.955.
- [ ] Günlük şablonu (§8.2) ve hipotez kartları (§8.3), 09.11 tarihli.

**Pazartesi 09:00–12:00 (tek seferlik)**
- [ ] Mevduat 1. dilim: hesabın %15'i, 32 gün (150 bin / 750 bin / 3 mn TL; 20 mn'de ≥ 3 banka).
- [ ] PPF: hesabın %85'i (850 bin / 4,25 mn / 17 mn; ≥ 2 PYŞ). Kalıcı %40; geçici %45, 16/23/30.11 dilimleri için.
- [ ] DİBS yalnız yazılı %0 stopaj teyidiyle, ≤ %10, ≤ 12 ay vade.
- [ ] Bilanço açıklayacak hisselerde (§3.10 A1) emir yok. Hisse/endeks long, short F_USDTRY, XU030 nakit-taşıma ve opsiyon yok.

**Pazartesi 18:15–18:45**
- [ ] Rejim tablosu (§2.1). Beklenen: KAPALI, 0/7.
- [ ] K4: Bilanço açıklamayan bir isimde B52 + TT 7/7 kapanışı varsa Salı kapanış seansına sonda emri (r₀ %0,25, limit × 1,06; aynı kümeden 1, toplam 2).
- [ ] K1: \|z\| ≥ 2 ve Kural 0 cevabı geldiyse Salı 17:55 emirleri (eşit TL; 20 gün 30.11'i aşıyorsa Aralık kontratı).
- [ ] Açık risk ≤ %2,5; stres ≤ %6; VİOP teminatı ≤ %15.
- [ ] Günlük kaydı.

**Hafta içi sabitler**
- [ ] Sal 10.11 18:15: Bilanço sonrası K4 değerlendirmesi; giriş Perşembe.
- [ ] Çar 11.11: Yeni giriş yok.
- [ ] Per 12.11: 07:00 MSCI → dışlama. 14:30 rezerv → M1, K6 kapısı. 18:00 K4 sondaları (varsa). Akşam SPK bülteni.
- [ ] Cum 13.11: Kredili esneklik kararı → A4. 18:30 haftalık gözden geçirme.
- [ ] Pzt 16.11: Mevduat 2. dilim.

**Asla:** Kredili spot; dışlama listesindeki hisse; tavan serisi sonrası halka arz alımı; bedelsiz/temettü hak gününe pozisyon taşımak; piyasa emri; vadede fiziki teslimata kalmak; KAPALI'da tam boy giriş; opsiyon satışı.

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
| Yabancı akımı sayılmaz | [OA] §3 | [DM] | Teyit göstergesi |
| KRİZ kesicisi | [KO] §4.2; [TC] §3.1 | [TE] | — |
| K1 SAHOL↔AKBNK, t+1 kapanış | [VB] #25, §2.5; [BS] §9.1 | [D] (gecikmeli t 2,4/2,8) | %40 iskonto; C'nin 09:30 girişi düzeltildi |
| K2 yalnız yeni kesişim | [VB] #25; [TC] §2.2 | [D] (t 2,1); kalıcı sinyal karışık | Varsayılan kâğıt |
| K3 temettü −6/−1 | [VB] #26; [BS] §5.3 | [D] (t 6,5) | %30 iskonto; B'nin gün −5'i düzeltildi |
| K3b yüksek verimli duyuru | [OB] §8 | [DM] (t 11,1, N=400) | Kâğıt; canlıya geçiş koşullu |
| K4 kırılım S2 + iz %15 | [BT] §5.1–5.2; [VB] #28, §2.1 | [D] işlem düzeyi; 2024–26 engelin altında | %50 iskonto; KAPALI'da sonda |
| K4'te S1 yok | [BT] §5.2 | [D] | — |
| K4 ekleme | [TA] §2.1 | [TE] (aritmetik risk-nötr) | Yalnız AÇIK, ayrı satır |
| Küme RS filtre değil | [TA] EK-3; [VD] §5 m.1 | Örneklem içi; doğrulanmamış ek hesap | Yalnız öncelik ve sınır |
| K5 ZPAT kontrol listesi + hak sahipliği | [VB] §3 m.4; [TB] K4; [TC] §2.5; [HK] §3.2 | Çalışılmadı | Küçük boy |
| K6 carry kapısı + brüt ≥ 160 | [VC] #18, #19; [KO] §4.2; [TM] §4.3 | [D] veri; [TE] kapı | Pazartesi 0 |
| K7 TSMOM12 + küme filtresi | [BT] §2; [VD] B3, §5 m.1; [DB] §3.7 | [D] (anlamlılık zayıf) | %20 nominal, 1x |
| K8 halka arz katılımı | [HA] §0, §3b; [VB] #11 | [D] (küçük TL) | Risk bütçesi dışında |
| A1 bilanço gecesi yok | [HZ] §2 | [TE] | — |
| A3 MSCI çıkarmaları | [VC] #17 | [D] (asimetri) | — |
| A4 kredili esneklik | [VB] #7; [HZ] §0 m.3; [BT] §4 | [D] takvim; [TE] kural | — |
| A5 bedelsiz kaçınma | [OB] §0, §6, §7 | [DM] (t −6,1; 2024–26 zayıf) | Maliyetsiz kaçınma |
| A6 temettü hak sonrası | [OB] §8; [BS] §5.3 | [DM] / [D] yön | — |
| A7 banka–PPK | [OA] §4.2, §4.5 | [DM] (6/6 döngü, t −4,2) | İhtiyat kuralı |
| A9 blok kilidi / fon uyumu | [VP] T7, T8; [TP] §4.5 | [D] takvim | — |
| Dışlama listesi | [VP] T6, T10; [TP] §4.4–4.5, §6; [VB] #27, #28 | [D] | — |
| Stres formülü ve tavanlar | [TB] §5; [TC] §5; [VC] §2 m.8 | [TE] | — |
| R_fazla ölçüm birimi | [TB] §6.4; [HK] §5 m.1; [HD] §6 m.1 | Muhasebe | A'nın ölümcül kusuru düzeltildi |
| Ölçekleme eşikleri | [SE] §3.7, §5.3; [HK] §5 m.1 | [L] / [TE] | — |

### 11.2 Açık sorular (cevap gelene kadar ilgili kural kapalı ya da ihtiyatlı)

1. **`dogrulama/v_olay.md` yok.** Geldiğinde şunlar yeniden değerlendirilir:
   - (a) K3b'nin canlıya geçişi.
   - (b) A5/A6 kaçınma pencereleri.
   - (c) A7 banka–PPK kuralı.
   - (d) Yabancı akımının rejimden çıkarılması.
   - (e) VİOP'lu geri alım izleme listesi.
2. **Aracı kurum cevapları (§6.1):** teminat faizi, PPF/DİBS teminatı, kurum teminat oranları, çift mahsubu, komisyon, kapanış seansına önceden emir, sunucu taraflı stop. K1, K2, K6, K7 ve vadeli finansman buna bağlı.
3. **DİBS stopajı:** 9–30.11 alımlarında %0 mı? 31.12.2026 uzatması yalnız ikincil kaynakta.
4. **2027 stopaj takvimi:** Mevduat/PPF için %17,5 ve DİBS muafiyeti 31.12.2026'da bitiyor. İndirim haberi tek ikincil kaynakta. Engel 1–3 puan oynayabilir.
5. **AKCNS ZPAT'ın KAP'taki durumu** ve katılım hakkının kayıt tarihi.
6. **6.11 VİOP bülteni:** İma oranlar ve K1/K2 z'leri 6.11 kapanışıyla yeniden hesaplanmalı.
7. **CDS 248** bağımsız teyit edilmedi ([VC] §1 sonu). TMSF mevduat sigortası limiti, Kasım PKA tarihi, HALKB bilanço tarihi ve güncel VBTS listesi teyitsiz.
8. **RYSAS likidite sırası;** RS yüzdeliğinin test tanımıyla (150 hisse) tarama tanımı (100 hisse) arasındaki fark.
9. **Takasbank genel mektup numarası:** GM 2174 ([KO]) mı 2176 ([HZ])? Oranlar aynı; aracı kurumdan teyit.
10. **Ortak kör nokta:** Bütün backtest kanıtı aynı İş Yatırım verisinden ve hayatta kalan hisse evreninden geliyor ([VB] §2.4; [BT] §1). 2020 öncesi limit modeli de hatalı (±%9,5 yerine ±%20; [VB] §2.2).

### 11.3 Taslaklardaki kusurların düzeltilmesi

| Kusur | Kaynak taslak | Bu plandaki düzeltme | Dayanak |
|---|---|---|---|
| Öldürme/ölçekleme mutlak R ile | A | Bütün testler R_fazla ile | [HK] §3.1 m.1 |
| Basit ve bileşik oran karışıklığı (XU030 "8 puan", vadeli "8–13 puan") | A | Basitle basit: 3,3 puan; vadeli avantajı mevduata göre ~4,6–7,4, PPF'ye göre ~1,6–4,4 | [VP] T12; [HD] §4 |
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
| Tarama `zirve52` bugünü içeriyor | Tarama | B52 tanımı düzeltildi | `bist_tarama.py` satır 129–137 |

---

## Ek A. Formüller ve komutlar

**Resmî VİOP bülteni** (varsayılan başlıklarla; [TB] Ek A):

```
G=20261106
curl -s -o viop_$G.csv https://www.borsaistanbul.com/data/vadeli/viop_$G.csv
awk -F';' '$2~/^(F_XU0301226|F_USDTRY1226|F_XLBNK1226|F_SAHOL1126|F_AKBNK1126|F_SAHOL1226|F_AKBNK1226|F_ENJSA1126)$/ {print $2, "uzlasma="$10, "kapanis="$16, "adet="$20, "islem="$21, "acikpoz="$22}' viop_$G.csv
```

Sütunlar: 2 = sözleşme kodu, 10 = uzlaşma, 16 = kapanış, 20 = işlem miktarı, 21 = işlem sayısı, 22 = açık pozisyon ([TB] Ek A; sütun sırası ilk kullanımda başlık satırıyla teyit edilmeli).

**Formüller:**
- İma basit oran: `i = (F_uzlaşma / S_kapanış − 1) × 365 / kalan_gün`.
- Mevduat neti: basit `brüt × 0,825`; aylık yenilemeyle bileşik `(1 + brüt × 0,825 × 32/365)^(365/32) − 1`. %39,52 → %32,6 / %37,9.
- K1 z: `x = ln(SAHOL) − ln(AKBNK)`; `z = (x − ort60) / std60` (bugün dahil).
- K4 kontrat ya da adet: `floor(hesap × r₀ × çarpan / (stop_mesafesi × fiyat × kontrat_çarpanı))`. Pay vadelisinde kontrat = 100 pay; F_XU030 = 10 TL × endeks.
- K3 hedge kontratı: `floor(Σ(βᵢ × nominalᵢ) / (F_XU030 × 10))`.
- R_fazla ve stres: §8.1 ve §5.
- TSMOM12 eşiği (30.11): `XU100(28.11.2025) = 10.898,7` × (1 + 12 ay nakit) → %37,3 ile ~14.960; %45,5 ile ~15.860 ([TA] EK-4).
