# Kırmızı takım 2: PLAN_ABD.md olgu ve kural denetimi

**Tarih:** Cuma 06.11.2026, ~15:00 TSİ.
**Denetlenen dosya:** `uygulama/PLAN_ABD.md`.
**Mercek:** Plandaki her sayı, tarih, eşik ve iddia; iç tutarlılık (risk matematiği, çalışılmış örnekler, emir tiplerinin gerçekten var olması, kuralların tek anlamlı olması, gün içi ekrana bağımlılık).

## 0. Yöntem

1. **Dosyalarla karşılaştırma.**
   - Plandaki rakamlar şu dosyalarla tek tek karşılaştırıldı: HAZ, VA, VC, VD, VP, DLG, SEY, PROF, TEST ve hakem raporları (HK, HU).
   - Bu dosyalar planın kendi kısaltmalarıyla anılıyor. VA, VC, VD, VP doğrulama dosyaları; HAZ hafta hazırlık dosyası; DLG, SEY, PROF, TEST ajan raporları.
2. **Bağımsız hesap.**
   - S&P ve NDX hareketli ortalamaları FRED ham verisinden yeniden hesaplandı.
   - Ardışık kayıp olasılıkları dinamik programlamayla hesaplandı.
   - Engel tablosu `plan_final/at.py` ile yeniden çalıştırıldı.
   - IBKR faiz kademesi düzeltmesi ayrıca hesaplandı.
3. **Birincil sayfalar** (curl, varsayılan başlıklar):
   - IBKR faiz oranları sayfası.
   - TradingView fiyat sayfası.
   - NVIDIA newsroom.
   - Berkshire Hathaway 04.11.2026 duyurusu (PDF).
   - Medtronic newsroom ve IR sayfası.
   - Census takvimi açıldı ama Kasım 2026 satırı listede yoktu; perakende satış tarihi açık kaldı.
4. İndirilen dosyalar: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/k2dl/`

## 1. Doğru çıkanlar (değiştirilmesin)

**Çalışılmış örnekler.**
- Örnek 1 (S1) ve örnek 2 (S2): adet, pozisyon, limitte ve tetikte risk, gap-ayarlı risk, IBKR ve İş TMI komisyonları kuruşuna kadar doğru.
  - S1: 18 / 93 / 375 adet; 6,66 $ hisse başı risk.
  - S2: 46 / 234 / 936 adet; 2,67 $ hisse başı risk.

**Engel tablosu ve vergi.**
- §1.2 engel tablosu `at.py` ile birebir tutuyor:
  - u=0,3 için 12,7/19,5, 15,6/23,3 ve 17,5/25,9.
  - Tam yatırımda (u=1) 17,1–33,7.
- §9.2 vergi sonrası satırları da tutuyor.

**Rejim verileri** (FRED/Cboe ile yeniden hesaplandı):
- S&P 10/20/50/200 GHO 7.622 / 7.680 / 7.687 / 7.323.
- 10 > 20 için gereken kapanış: 7 seans boyunca ~7.733 ya da 10 seans boyunca ~7.622.
- NDX 10/20/50/200 GHO 28.672 / 29.286 / 29.686 / 27.977. NDX'te 10 < 20 durumu 19.10'dan beri sürüyor.
- VIX/VIX3M = 28,18 / 25,55 = 1,103.

**Kayıp serisi olasılıkları** (200 işlem):
- %25 isabette ≥15'lik seri %48,6, ≥10'luk seri %96,1.
- %30 isabette ≥15'lik seri %24,0, ≥10'luk seri %83,5.

**Tutarlı çıkan diğer tablolar.**
- §5.4 dolar karşılıkları.
- §1.4 çevrim aşamaları.
- §5.2 merdiven yüzdeleri (Faz 1'de 16R = %4, 28R = %7, 40R = %10).
- §8.3 SE ve sahte geçiş olasılığı (~%16).

**Takvim.**
- Hafta günleri doğru: 26.11 Şükran Günü; 20.11 ve 18.12 ayın 3. Cuması.
- VIX vadesi 18.11, FOMC 08–09.12, TCMB PPK 10.12.
- 27.11 erken kapanış 21:00 TSİ.
- Bütün ET→TSİ dönüşümleri +8 saat ile doğru.

**Hukuki ve ücret kalemleri.**
- PDT tarihleri (VC #15).
- Fed oylaması ve faiz bandı.
- Temettü stopajı %20.
- W-8BEN yoksa stopaj %30.
- 150 bin TL istisnasının menkul kıymete uygulanmaması.
- Zarar mahsubunun yalnız aynı yıl içinde yapılması.

**Rejim akışı.**
- Pazartesi canlı giriş olamayacağı sonucu doğru.
- İlk pilotun en erken Perşembe 12.11 olabileceği zinciri tutarlı.
  - Cuma 1. gün olursa FTD en erken Çarşamba.
  - KIRMIZI'dan çıkış için Salı ve Çarşamba kapanışlarında VIX/VIX3M < 1 olmalı.

## 2. Bulgular

### KRİTİK

**K-1. Bilanço öncesi MOC çıkışı, canlı GTC stopla çakışıyor; margin hesapta istenmeyen açığa satış doğurabilir** (§3.6, §6.2, §3.5 emir hijyeni).
- **Sorun:**
  - Plan MOC'u seans öncesinde (16:45–17:15) giriyor ve stopu seans boyunca açık bırakmak zorunda. Gün içinde ekran yok.
  - Stop gün içinde tetiklenirse MOC kapanışta yine çalışır. Sonuç: tam pozisyon kadar açığa satış, bir gece korumasız.
  - §3.5'teki OCA hijyeni yalnız MOO'yu kapsıyor; MOC'u kapsamıyor.
- **Düzeltme:**
  - SELL MOC ile GTC SELL STP aynı **OCA grubuna** konur. IBKR'de "Cancel all remaining orders with block" seçilir; bu ayar aşırı dolum koruması sağlar.
  - Pazartesi 1 adetlik test listesine "MOC + STP aynı OCA'da" testi eklenir.
  - Test geçmezse bilanço çıkışı bir önceki günün kapanış kararıyla **MOO** olarak yapılır. Kuralın ilk satırı şöyle olur: "Bilançodan 2 seans önceki kapanışta karar, ertesi açılışta MOO."
- Aynı OCA yöntemi tam çıkış MOO'larında da kullanılmalı. Bugünkü "stopu iptal et" yöntemiyle MOO dolmazsa (reddedilen emir, işlem durdurma) pozisyon bütün seans korumasız kalır.

**K-2. Bekleyen giriş emirlerinin sayısına ve tutarına tavan yok** (§2.2, §4.4 #5, §5.1).
- **Sorun:**
  - Rejim tablosundaki "günde ≤2 giriş, ≤4/8 pozisyon, küme ≤1/3" sınırları ancak dolumdan sonra kontrol edilebiliyor.
  - SARI'da izinli 6 kümede 6 tane buy-stop, YEŞİL'de 7 kümede 3'er tane, yani 21 emir aynı anda bekleyebilir.
  - Güçlü bir FTD günü bunların çoğunu birlikte doldurur. YEŞİL'de brüt maruziyet %40 tavanını (21 × ~%4 ≈ %84) ve USD nakdini aşar.
  - Margin tipi hesapta bu, %5,38 faizli ve Türkiye'de indirilemeyen bir borç demek. Ekransız ve gün içi müdahalesiz.
- **Düzeltme.** Her gün 16:45'te bekleyen giriş emirleri için şu kural uygulanır:
  - Emir sayısı ≤ min(günlük kalan giriş hakkı; boş pozisyon yeri).
  - Kümede ≤ kalan küme hakkı.
  - Σ(adet × limit) ≤ min(kalan brüt tavan; serbest USD nakit − %5 tampon).
  - Σ gap-ayarlı risk ≤ kalan ısı.
  - Bu sınırın üstünde kalan adaylar IBKR OCA gruplarına bölünür. Örnek: SARI'da her biri en çok 1 dolum verecek 2 OCA grubu.
  - Kural metne "bekleyen emirler dolmuş sayılır" diye yazılır.

### ÖNEMLİ

**Ö-1. IBKR nakit faizi kademeli; plandaki nakit getirisi rakamları küçük hesapta yanlış** (§1.2 tablo sütunu, §1.6, §9.1 "+%2,4", §9.2 ve §8.6 kıyas satırları).
- **Kanıt:**
  - IBKR sayfası (Eylül 2026 itibarıyla): USD için ilk 10.000 $'a %0, üstüne %3,38 (BM − %0,5) ödeniyor.
  - Net varlık değeri (NAV) 100 bin $'ın altındaysa oran NAV/100 bin oranında düşüyor. Örnek: NAV 80 bin $, nakit 20 bin $ ise oran %1,352.
  - Plan bu bilgiyi "bellekten, doğrulanmadı" diye bırakmıştı. Şimdi doğrulandı.
- **Hesap:**
  - E=50 bin $ tamamı nakitte: vergi öncesi %1,35, vergi sonrası **%1,15**. Plandaki rakam %2,9.
  - u=0,3 ile boştaki %70: E'nin %0,84'ü. Plan %2,4 diyor.
  - Kademeli çevrimde (USD %40, boşta ~%10): her boyutta E'nin %0–0,3'ü.
  - 250 bin $ ve 1 milyon $'da tam çevrim varsayımıyla fark küçük: vergi sonrası %2,6 ve %2,4.
- **Düzeltme:**
  - §1.2'deki 50 bin $ satırı: USD nakit vergi sonrası %1,15. USD kökenli sermaye için gereken R %2,3 (u=0,3) / %6,0 (u=1).
  - §1.6'daki "kaybedilen faiz yalnız 0,65 puan" ifadesi 100 bin $ NAV altı için geçersiz.
  - §9.1'deki medyanlardan 2,4 puanlık nakit katkısı çıkarılır. Kalan işlem kâr/zararı: −%2,8 / −%1,3 / +%1,4 / +%4,3 / +%6,7.
  - Ağırlıklı merkez ~**−%1,5 ile +%1,5** olur, planın yazdığı +%1–4 değil.
  - Kademeli çevrimde TL tarafı (E'nin %60'ı) ayrı satırda gösterilir. Bir modelde iki varsayım karıştırılmamalı: 1. yıl tablosu tam çevrim varsayıyor, plan ise kademeli çevrim uyguluyor.

**Ö-2. Pine Screener, planın 50 bin $ için öngördüğü TradingView paketinde yok** (§1.3 veri satırı, §4.1 (a), §10).
- **Kanıt:** TradingView fiyat sayfasındaki tabloya göre `pine_screener` yalnız Premium ve üstünde var; Essential ve Plus'ta yok.
- **Fiyatlar:**
  - Essential 14,95 $/ay (yıllık ödemede 12,95 $).
  - Plus 34,95 $/ay (yıllık ödemede 29,95 $).
  - Premium 69,95 $/ay (yıllık ödemede 59,95 $, yılda ~719 $). 50 bin $'lık E'nin %1,4'ü; bu, 1. yıl beklenen getirinin tamamı kadar.
- **Düzeltme:**
  - 50 bin $'da tarama (a) HAZ §5a'daki finviz sıkı ve geniş URL'leri ile ücretsiz TradingView standart tarayıcısıyla yapılır.
  - 52 haftalık zirve/dip, 150 GHO ve RS çizgisi koşulları kısa listede grafik üzerinde elle kontrol edilir.
  - Premium, en erken 250 bin $'da (E'nin %0,29'u) kullanılır.
  - Fiyatların yıllık ödeme fiyatı olduğu not edilir.

**Ö-3. PDT geçiş dönemi ve aynı gün stop olma riski** (§6.1 "bağlayıcı değil").
- **Sorun:**
  - FINRA RN 26-10 aracı kurumlara 20.10.2027'ye kadar geçiş süresi veriyor. IBKR'nin yeni kurala geçip geçmediği bilinmiyor.
  - Buy-stop ile gün içinde dolup aynı gün stop olan işlem bir "day trade" sayılır.
  - 50 bin $ örneğinde ilk aşamadaki USD bakiyesi 20 bin $, yani 25 bin $'ın altında. 5 günde 4 aynı gün stop, eski kurala göre 90 günlük kısıt getirebilir.
- **Düzeltme:**
  - IBKR'ye yazılı soru: "Hesabım yeni FINRA kuralında mı?"
  - Teyit gelene kadar USD bakiyesi ≥ 25 bin $ tutulur. 50 bin $ için bu ilk aşamada %50 çevrim demek.
  - Ya da hesap tipi kararı (cash/margin) bu cevaba bağlanır.

**Ö-4. Gölge G1 taramasının saati ve filtreleri yanlış gün kümesini veriyor** (§3.8 G1 "Tarama", §6.3).
- **Sorun:**
  - 09:00–12:00 TSİ, ET'de 01:00–04:00'e denk gelir; finviz o sırada yeni ET gününü "bugün" sayar.
  - `earningsdate_yesterdayafter` önceki günün kapanış sonrası açıklayanlarını seçer. Bunların gap'i henüz oluşmamıştır.
  - `todaybefore` henüz açıklanmamış bilançoları seçer.
  - Pazartesi sabahı "dün" Pazar'dır; filtre boş döner.
  - HAZ §5b bu filtreleri **seans içi** kullanım için yazmıştı.
- **Düzeltme:** Sabah taraması `earningsdate_prevdays5` + `ta_gap_u8` + `sh_relvol_o3` + `sh_price_o20` ile yapılır. Gap ve RVOL filtreleri son tamamlanan seansa bakar; 1. gün = son seans olur.

### KÜÇÜK

1. **NVDA tarihi teyit edildi.**
   - NVIDIA newsroom (28.10.2026): konferans çağrısı **Salı 17.11, 17:00 ET**, yani 01:00 TSİ 18.11.
   - Görev notundaki "~19.11" yanlış. §7.2 ve §11.3'teki "teyit" ve "çelişki" notları silinir.
2. **BRK-B bilanço tarihi.**
   - Berkshire duyurusu (04.11.2026): bilanço **Cumartesi 07.11.2026, 07:00 CT**'de yayımlanıyor.
   - Pazartesi 9.11 ilk tepki seansı. §7.1'deki "9.11 olabilir" ifadesi düzeltilir.
   - Eleme filtresi (b) için 3 seans beklenir, yani en erken 11.11 kapanışı.
3. **MDT bilanço tarihi:** Medtronic IR'a göre **Salı 24.11 BMO**. "Bilançoya ≤10 seans kalmışsa giriş yok" kuralı 10.11'den itibaren MDT'yi kapatır.
4. **CSPX saatleri:** LSE 08:00–16:30 GMT, yani Kasım'da **11:00–19:30 TSİ**. Plandaki 10:00–18:30 değil. (PRIIPs AB/AEA mukimine uygulanır; Türk mukimi için ETF kısıtı büyük olasılıkla yok, teyit gerekir; VA §4 #7.)
5. **§1.5 döviz anahtarı:** 1 aylık USDTRY vadelisinin zımni getirisi VC #5'e göre ~%32 (Kasım) ile ~%33 (Aralık). Plandaki "~%34" düzeltilir.
6. **§1.2 hayalet vergi:** Yıl sonu kuruyla (60,06) E'nin %0,75 / %1,10 / %1,55'i. Plandaki %0,9 / %1,3 / %1,9 başlangıç kuruyla hesaplanmış; bu not edilir.
7. **§3.5 "Aşırı koşu" kuralı:**
   - Dayanak sektör düzeyinde, 24 aylık GSY olayları. VD U8 yalnız olay sayısını ve çöküş oranını doğruladı.
   - Aynı tabloda "hemen çık" seçeneği iz süren stopu domine ediyor (VD U9: ortalama +%9,7, kayıp oranı %0).
   - Etiket [H, sektör düzeyi] olur. Kural "+%100'de en az 1/2 MOO ile sat, kalanına %10 trail" diye yazılır.
8. **§2.5 MTUM rakamları** (−%15,5 / −%8,7) VC'de DOĞRULANAMADI listesinde. [K] etiketi eklenir.
9. **§0 #1:** "NDX 10 < 20" bir KIRMIZI koşulu değil; SARI tetiğinin olmaması. İfade buna göre düzeltilir.
10. **§6.1 ve §11.1 #32:** Gedik yüzdesel değil, lot başı 0,05 $ alıyor. Örneklerde ~0,015–0,04R; "0,07–0,2R" grubundan çıkarılır.
11. **§3.2 baz derinliği:** "Faz 1'de ≤%15, YEŞİL'de ≤%25" faz ile rejimi karıştırıyor. "SARI'da ≤%15, YEŞİL'de ≤%25 (her fazda)" diye yazılır.
12. **§4.3 temel tüketim:** "Sınırda izinli" diye bir durum tanımlı değil. XLP 6. sırada, yani (a) şartı sağlanmıyor. (b) yalnız indirim mağazaları grubunda sağlanıyor. K6 = yalnız BJ; KDP izinsiz.
13. **§1.3 (c):** 280–450 işlem bu planın temposunda (yılda 70–120 işlem) **2,3–6,4 yıl** eder; "2–4 yıl" değil.
14. **§8.3 veri kaynağı:** CRSP/WRDS bireye açık değil. Norgate ya da Sharadar gibi hayatta kalma yanlılığından arındırılmış ücretli veri yazılır.
15. **§4.5 IDXX:** 5. gün 6.11, yani pencere bugünkü seansla kapanıyor.
16. **§7.2 LLY kuralı:** ObesityWeek (14–17.11) kuralı 20.11 satırında duruyor. 13.11 satırına ve §4.5'e taşınır.
17. **§3.5 zaman stopu:** "Girişten beri yeni kapanış zirvesi yok" ifadesi belirsiz. "Son 5 seansta girişten beri en yüksek kapanış yok" diye yazılır.
18. **§10 emir testleri:** MOO ve MOC testleri açık pozisyon gerektiriyor. Sıra şöyle olur:
    - Pazartesi: 1 adet alım + ekli stop.
    - Salı: MOO satış.
    - Çarşamba: 1 adet alım + MOC/STP OCA testi.
19. **§1.4 TL payı:** E'nin %60'ının tamamı 32 günlük mevduata konursa 2. aşama çevrimi (YEŞİL) vade bozmayı gerektirir. Bir sonraki dilim (E'nin %10'u) banka PPF'sinde tutulur.
20. **§5.1 ısı tavanları erişilemez:** Faz 1'de "SARI %2 / YEŞİL %3" ısı tavanına ulaşılamıyor. 4 ve 8 pozisyon × %0,25 = %1 ve %2 (gap-ayarlı en çok %1,25 ve %2,5). Etkin tavan yazılır. Aylık devre kesicinin "gerçekleşen zarar"ı "ayın net gerçekleşen kâr/zararı (negatifse)" diye tanımlanır.
21. **§8.3 Faz 2 → 3 kapısı:** "Vergi sonrası getiri engeli geçmiş" ifadesi vergi öncesi bir R engeliyle karşılaştırılıyor. Doğrusu: "vergi öncesi R, §1.2'deki gereken R'yi geçmiş."
22. **§9.5:** "Bu sonuçların girdileri: %1 risk" ifadesi doğrulanmış aralıkla uyuşmuyor. Doğrusu %0,25–1 (VP A1).
23. **§2.8:** Kullamägi'nin −%57'si takvim yılı 2022 değil; Kasım 2021'den 2022 ortasına kadar zirveden dibe düşüş.
24. **§1.4 ilk aşama:** %40 çevrim "SARI brüt tavanı" ile gerekçelendiriliyor, ama rejim KIRMIZI. Ya çevrim ilk SARI kapanışına bağlanır, ya da gerekçe "pilot hazırlığı" olarak yazılır.

## 3. Kalan teyitler

- Midas emir tipleri: kamuya açık değil.
- IBKR'de MOO/MOC son giriş saatleri ve ekli emrin farklı TIF taşıması: 1 adetlik testle teyit edilir.
- Ekim perakende satış tarihi: Census listesinde Kasım satırı görünmedi.
- 2026 vergi tarifesi: VC #11 hâlâ DOĞRULANAMADI.
