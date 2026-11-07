# TradingView alarmları: canlı fiyat ya da ABD verisi gereken sinyaller

_08.11.2026. Günlük rapor (`gunluk/SON.md`) her iş günü ~21:05 TSİ'de çıkar. Bazı sinyallerin karar anı ise daha erkendir. TUPRS'un karar anı sabahtır, kapanış penceresi sinyallerininki 17:45–18:15'tir. Bu kural anlarını yalnız TradingView alarmı yakalar. Bu dosya alarmların adım adım kurulumunu anlatır. Bilgi amaçlıdır, yatırım tavsiyesi değildir._

> **Pine dosyalarının hiçbiri TradingView'da derlenmedi ve test edilmedi.** Bu ortamda Pine derleyicisi yok. İlk kullanımda göstergeyi grafiğe ekleyin. Derleme hatası çıkarsa satır numarasını not edin ve o sinyal için yalnız günlük rapora güvenin. Göstergenin son 5–10 günlük değerini günlük raporun §3 tablosuyla karşılaştırın. Fark büyükse (z'de > 0,1) raporu esas alın.

## 0. Önce: abonelik, veri ve genel ayarlar

**Alarm sayısı.** Aşağıdaki asgari set 9 alarm ister (§8). Ücretsiz Basic plan buna yetmez. Essential (≈20 alarm) yeter. Sayılar ve fiyatlar değişebilir; TradingView'ın plan sayfasından teyit edin. Ayrıca bazı planlarda alarmların süresi dolar (~2 ay). Takvime bir "alarmları yenile" notu koyun.

**Gerçek zamanlı veri.**
- BIST pay ve VİOP verisi TradingView'da varsayılan olarak **15 dakika gecikmelidir**. Gerçek zamanlı veri, Hesap → *Piyasa verisi abonelikleri* altında ayrı ücretli bir pakettir. Pay ve VİOP paketleri ayrı olabilir.
- Gecikmeye dayanıklı sinyaller:
  - **TUPRS:** Sinyal ABD'nin dünkü kapanışından hesaplanır.
  - **Altın:** TVC:GOLD genellikle gerçek zamanlıdır.
  - **ABD rejimi.**
- Gerçek zamanlı veri isteyen sinyaller: **Koza**, **SAHOL/AKBNK PRATİK** ve **XU030 bazı**. Gecikmeli veriyle 17:55'te ekranda 17:40 fiyatı görünür. XU030 bazında 18:10 fiyatı ancak 18:25'te gelir, yani işlem penceresi kapanmış olur. Paket alınmayacaksa bu sinyallerde alarmı yalnız hatırlatıcı sayın; kararı aracı kurumun canlı ekranından verin.

**Genel ayarlar.**
- Grafik saat dilimi: *(UTC+3) İstanbul*.
- Bildirim: TradingView mobil uygulamasında anlık bildirim, isteğe bağlı olarak e-posta.
- Alarm penceresinde *Koşul*, grafiğe eklediğiniz göstergenin adıdır. Ardından açılan listeden aşağıdaki alarm başlığını seçin.
- **Sıklık seçimi (günlük 1G grafikte):**

| Seçenek (TR arayüz) | Ne zaman tetikler | Ne için |
|---|---|---|
| **Bar başına bir kez** (Once Per Bar) | Gün içinde koşul ilk sağlandığında, bir kez | Canlı karar: Koza, altın, TUPRS'un sabah bildirimi |
| **Bar kapanışında bir kez** (Once Per Bar Close) | Günlük bar kapanınca. BIST payında ~18:10, gecikmeli veride ~18:25 | Kapanışla kesinleşen ve **ertesi gün** işlenen sinyaller: K1 oranı, kâğıt kaydı, ABD rejimi (~00:00 TSİ) |
| **Yalnızca bir kez** (Only Once) | Bir kez tetikler, sonra kapanır | Her akşam rapordan güncellenen seviye alarmları (XU030 bazı) |

**Plan kısıtları alarmlar için de geçerlidir.**
- PLAN_BIST'e göre bu 1–3 günlük sinyaller **K9 kanalıdır**. Fikir kartı gerekir. Risk KAPALI rejimde işlem başı ≤ %0,25, diğer rejimlerde ≤ %0,5. Aynı anda en çok 2 işlem.
- Takvim engelleri:
  - 9.11: A1. Bilançosu gelmemiş TRALT, TRMET vb.
  - 11.11: hiçbir yeni giriş yok.
  - 12–13.11: K9 girişi yok.
  - Ayrıca KRİZ kesicisi.
- Günlük raporun §0 bölümü bu engelleri her akşam yazar. Alarm çalsa da engel varsa işlem yapılmaz.

## 1. Özet: hangi ticker, hangi yön, hangi alarm

| # | Sinyal | Öncü (lead) | İşlem bacağı (lag) | Yön | Pine / alarm | Grafik | Sıklık | Bildirim (TSİ) | İşlem (TSİ) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **TUPRS ← ABD rafinerileri** | NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF; SP:SPX'e göre β-arındırılmış ortalama artık, ABD'nin t−1 günü | BIST:TUPRS1! | **Aynı yön.** Rafineriler dün S&P'yi geçtiyse (z > +1) F_TUPRS AL, geride kaldıysa (z < −1) SAT | `rehber/tuprs/tuprs_alarm.pine` → "TUPRS herhangi bir kural olayı" | BIST:TUPRS1! 1G | Bar başına bir kez | ~10:00–10:15 (BIST açılışı) | Aynı gün 18:00–18:10 giriş; t+2 uzlaşmasında çıkış kontrolü |
| 2 | **Altın → TRALT** | TVC:GOLD (17:55 fiyatı, bir önceki BIST gününün 17:55'ine göre) | BIST:TRALT1! + hedge BIST:XU030D1! | **Aynı yön.** Altın z > +1 ise TRALT1! AL + XU030D1! SAT; z < −1 ise tersi | `rehber/altin/altin.pine` → "Altın sinyali (geçici)" (dosyada zaten var) | BIST:TRALT1! 1G | Bar başına bir kez | Gün içinde ilk eşik aşımında; **karar 17:55** | 18:00–18:10; 2 BIST günü tut |
| 3 | **Koza göreli momentumu** | Lead-lag yok. TRMET'in BIST:TRALT ve BIST:TRENJ ortalamasına göre son 3 günlük artığı | BIST:TRMET1! + BIST:TRALT1! (β_TA ≈ 0,69 → ~1:2 kontrat) | **Momentum yönü.** z3 > +1,5 ise TRMET1! AL + TRALT1! SAT; z3 < −1,5 ise tersi | `rehber/koza/koza_alarm.pine` (yeni) → "KOZA \|z3\| eşik üstü" + "KOZA bugün çıkış günü" | BIST:XU030 1G | Bar başına bir kez | 17:45–18:10 penceresi; çıkış hatırlatması sabah | 18:00–18:10; 2 gün, sinyal sürerse +2 (≤ 6) |
| 4 | **SAHOL/AKBNK PRATİK** (β'lı artık z) | Lead-lag yok, ortalamaya dönüş | BIST:SAHOL1! / BIST:AKBNK1! (≈ 1:1) | **z'nin tersi.** z > +1,5 ise SAHOL SAT + AKBNK AL; z < −1,5 ise tersi | `kod/sahol_akbnk_z.pine` → "LONG/SHORT spread girişi", "Spread çıkışı" (dosyada zaten var) | BIST:SAHOL 1G | Bar kapanışında bir kez (kâğıt kaydı) | ~18:10 (gecikmeli ~18:25) | **Varsayılan kâğıt** (PLAN_BIST K1 öncelikli) |
| 5 | **K1 SAHOL↔AKBNK** (plan, 20 gün) | Lead-lag yok, 60 günlük ln oran z | F_SAHOL ve F_AKBNK, Aralık vadesi | **z'nin tersi.** Oran üst seviyeyi geçerse SAHOL SAT + AKBNK AL; alt seviyenin altına inerse tersi | Fiyat alarmı, spread sembolü `BIST:SAHOL/BIST:AKBNK`. Seviyeler raporun §2 K1 satırında | BIST:SAHOL/BIST:AKBNK 1G | Bar kapanışında bir kez | ~18:10 | **Ertesi gün** 17:55 |
| 6 | **XU030 kapanış bazı sıçraması** | BIST:XU030 spot kapanışı ile BIST:XU030D1! son fiyatı (18:10–18:15) | BIST:XU030D1! | **Bazın tersi.** Vadeli dünküne göre pahalı kapandıysa (oran üst seviyenin üstünde) SAT, ucuz kapandıysa AL | Fiyat alarmı, spread sembolü `BIST:XU030D1!/BIST:XU030`. İki seviye raporun §3 tablosunda | aynı spread, 1 dk | Yalnızca bir kez | Yalnız 18:08–18:15 arası anlamlı | 18:15'e kadar giriş; ertesi gün uzlaşmada çıkış |
| 7 | **ABD rejimi** | SP:SPX, NASDAQ:NDX, CBOE:VIX/CBOE:VIX3M | ABD hesabı (IBKR) | Durum değişimi | `uygulama/kod/abd_rejim_ve_sablon.pine` → "Rejim degisti" (dosyada zaten var) | SP:SPX 1G | Bar kapanışında bir kez | ~00:00–00:30 | Ertesi gün 16:45–17:15 emir bloğu |

**Önerilmeyenler.** PRATIK_LISTE'deki düşük güvenli lead-lag'ler için alarm kurmayın. Bunlar ASX:FMG + ASX:BHP → EREGL, VİOP USDTRY → THYAO, ay dönümü ve kredi notu tersidir. Kenarları ya küçük ya da yalnız belirli rejimlerde var. Ayrıca "bilgi BIST kapanışından sonra geliyor" grubundaki hiçbir sinyal (ABD vadelisi → açılış gap'i vb.) bu profil için uygun değildir.

## 2. TUPRS ← ABD rafinerileri (`tuprs_alarm.pine`)

`tuprs.pine` dosyasında `alertcondition()` yoktu. `tuprs_alarm.pine` aynı hesaba yalnız 6 alarm satırı ekler.

1. TradingView'da **BIST:TUPRS1!** grafiğini açın. Zaman dilimi **1G**. En az ~600 günlük bar gerekir.
2. Pine Editör'ü açın, `2026-11-04_kapanis_1-3gun/rehber/tuprs/tuprs_alarm.pine` içeriğini yapıştırın ve *Kaydet*, ardından *Grafiğe ekle*.
3. Göstergenin sağ üstteki tablosunu kontrol edin. "Son kullanılan ABD günü (NY)" dünün ABD tarihi olmalıdır.
4. Alarm oluşturun (saat simgesi ya da Alt+A):
   - *Koşul:* "TUPRS-REF alarm" → **"TUPRS herhangi bir kural olayı"**. Ayrı bildirim istiyorsanız "TUPRS AÇ uzun", "TUPRS AÇ kısa", "TUPRS ÇEVİR" ve "TUPRS KAPAT" için 4 ayrı alarm kurun. "UZAT"ta işlem yoktur.
   - *Sıklık:* **Bar başına bir kez.** Z, BIST günü t için yalnız ABD'nin t−1 kapanışına bağlıdır ve gün içinde değişmez. Bildirim BIST açılışında (~10:00, gecikmeli veride ~10:15) gelir. "Bar kapanışında" seçerseniz bildirim 18:10'dan sonra gelir ve aynı günün uzlaşması kaçar.
   - *Bitiş:* en uzun süre. *Bildirim:* uygulama + e-posta.
5. **Alarm çalınca:**
   - Gösterge tablosunda yön ve olay türüne bakın: AÇ, UZAT, ÇEVİR ya da KAPAT.
   - Aynı gün 17:45'te aracı kurum ekranında F_TUPRS'un kademelerine ve limite yakınlığına bakın.
   - Emir 18:00–18:09 arasında, karşı kademeye limitli verilir. 3 ve üstü kontratta 2–3 parçaya bölün.
   - Kontrat: vadeye en az 3 BIST iş günü kalan en yakın vade. Kasım vadesi 25.11'den sonra kullanılmaz.
   - Boyut (rehber §4): kontrat = taban(sermaye × risk / (100 × fiyat × L)). L ≈ 1,65 × σ60 × √2, taban %4. K9 kanalında risk KAPALI rejimde %0,25: 1 mn TL'de ~1–2 kontrat.
   - Çıkış: t+2 iş günü sabahı yeni bir olay alarmı gelir (UZAT, ÇEVİR ya da KAPAT).
6. **Not:** ABD tatilinde, bir önceki ABD günü yoksa sinyal çıkmaz. NYSE verisinin 15 dk gecikmesi sorun değildir; yalnız dünkü kapanış kullanılır.

## 3. Koza göreli momentumu (`koza_alarm.pine`)

`koza.pine` dosyasında `alertcondition()` yoktu. `koza_alarm.pine` dosyasının sonuna şunlar eklendi:
- bir saat penceresi girdisi (varsayılan **17:45–18:10 TSİ**),
- 5 alarm satırı.

Hesap satırlarına dokunulmadı.

1. **BIST:XU030** grafiğini açın, zaman dilimi **1G**. Bu grafik, araştırmadaki birleşik BIST takvimini verir.
2. `rehber/koza/koza_alarm.pine` dosyasını yapıştırıp grafiğe ekleyin.
   - Tabloda z3, β_g, β_TA ve "Yarın AL için TRMET ≥" değerleri görünür.
   - Bu değerleri günlük raporun §3 satırıyla karşılaştırın. 06.11 kapanışında rapor şunu verdi: z3 0,71, TRMET ≥ 116,92 / ≤ 105,16.
   - **Tetik farkı beklenir:** Göstergenin (ve `sinyal_koza.py`'nin) "Yarın AL için TRMET ≥" satırı σ60'ı sabit varsayar ve 06.11'de 116,76 / 105,54 verir. Günlük rapor σ60'a yarının artığını da katarak kesin seviyeyi çözer (116,92 / 105,16). Karar için rapordaki seviyeyi ya da 17:50'deki z3'ü kullanın.
3. Alarm 1: **"KOZA |z3| eşik üstü (durumdan bağımsız)"**, Bar başına bir kez.
   - Alarm sayısında tasarruf için tek alarm yeter.
   - Yönü ayrı ayrı istiyorsanız bunun yerine "KOZA canlı giriş: TRMET1! AL / TRALT1! SAT" ve "… SAT / … AL" alarmlarını kurun. Bu ikisi kural durumunu da (pozisyon yokken ilk sinyal, kilit yok) kontrol eder.
4. Alarm 2: **"KOZA bugün çıkış günü (sabah hatırlatma)"**, Bar başına bir kez.
   - Planlanan çıkış ve uzatma günlerinde BIST açılışında bir kez çalar.
   - Not: Gösterge kural durumunu kendi geçmişinden kurar. Gecikmeli girdiyseniz (E2, ertesi gün giriş) çıkış gününüz göstergeninkinden 1 gün sonradır. Günlük rapordaki açık pozisyon satırını esas alın (durum.json'a pozisyonu yazdıysanız).
5. **Alarm çalınca (17:45–17:55):**
   - Aracı kurum ekranından TRMET, TRALT ve TRENJ'in canlı spot fiyatlarına bakın.
   - TRMET1! ya da TRALT1! ±%10 limitte kilitliyse girmeyin.
   - Yön tutuyorsa iki bacağı 18:00–18:10'da 2–3 parçada girin. Önce az likit TRMET1!, hemen ardından TRALT1!.
   - Kontrat oranı rapordadır (06.11: 1 : 2,0). K9 riski %0,25 ile 1 mn TL'de 6 TRMET1! : 12 TRALT1!.
   - Vade, planlanan çıkıştan **sonra** biten en yakın vadedir. 26.11'den sonraki girişlerde Aralık vadesi.
6. **Pencere ayarı:** Göstergenin *Ayarlar → Girdiler → Alarm* grubundaki saatler değiştirilebilir. Arife günlerinde (yarım gün) pencereyi 12:00–12:30'a çekin ya da o gün alarmı yok sayın.

## 4. Altın → TRALT (`altin.pine`, alarm zaten var)

`altin.pine` dosyasında `alertcondition(provSig, "Altın sinyali (geçici)")` zaten var. Yeni kopya yazılmadı.

1. **BIST:TRALT1!** grafiğini açın, zaman dilimi **1G**. `rehber/altin/altin.pine` dosyasını ekleyin.
   - *Altın sembolü:* TVC:GOLD (varsayılan). COMEX:GC1! kullanmayın, vade geçişinde sıçrar.
   - σ için yeterli alt zaman dilimi geçmişi yoksa (Basic planda ~200 gün) *Elle σ* girdisine **1,70** yazın. Günlük rapor da bu sabiti kullanır.
2. Alarm: **"Altın sinyali (geçici)"**, Bar başına bir kez.
   - Gün içinde |z| ilk kez 1'i aştığında çalar. Sinyal sonradan kaybolabilir.
   - **Karar yalnız 17:55'te** verilir: g = ln(TVC:GOLD 17:55 / dünkü 17:55), z = g / 0,0170.
   - |z| > 1 ise 18:00–18:10'da girin. Yön: z > 0 ise TRALT1! AL + XU030D1! SAT, z < 0 ise tersi.
   - Oran: 1 XU030D1! kontratına karşı N TRALT1!. 06.11 için N = 29, β 1,30. Günlük rapor her akşam yeniden yazar.
   - 1 mn TL'de **1 birim**.
3. Çıkış: 2 BIST günü sonra 17:55'te yeniden bakılır.
   - Aynı yönde |z| > 1 ise tutulur. Ters yönde ise çevrilir.
   - Sinyal yoksa 18:00–18:10'da iki bacak birlikte kapatılır.
4. Günlük rapor F_XAUUSD uzlaşma değişimini **vekil** olarak gösterir. Bu, araştırmanın asıl sinyalidir ama işlemle aynı dakikada oluşur. Bu yüzden 21:05'te yalnız "bugün tetiklendi mi" bilgisi verir.

## 5. SAHOL/AKBNK: PRATİK artık z ve plan K1

**5a. PRATİK artık z (`sahol_akbnk_z.pine`, alarmlar zaten var).**
- Grafik: **BIST:SAHOL** 1G. Göstergeyi ekleyin. Kural A ile giriş |z| > 1,5, çıkış |z| ≤ 1,5.
- Alarmlar: "LONG spread girişi", "SHORT spread girişi" ve "Spread çıkışı". Sıklık **Bar kapanışında bir kez**.
- PLAN_BIST bu 1–3 günlük sinyali K1 lehine emekliye ayırdı: aynı çiftte iki sinyal çalıştırılmaz. Bu yüzden varsayılan kullanım **kâğıt kaydıdır**.
- Canlı kullanmak isterseniz `gunluk/durum.json` → `ayarlar.pratik_sahol_akbnk` = `"canli"` yapın. K1 açıkken bu sinyalde işlem açmayın. Kuralın girişi aynı gün uzlaşmasıdır, o durumda alarmı "Bar başına bir kez" seçin ve kararı 17:50'de verin.

**5b. K1 (plan): oran alarmı.**
- Sembol kutusuna **`BIST:SAHOL/BIST:AKBNK`** yazın. TradingView bunu oran grafiği olarak açar. Zaman dilimi 1G.
- İki fiyat alarmı kurun, ikisi de *Bar kapanışında bir kez*:
  - "Yukarı kesişme" → raporun §2 K1 satırındaki **üst oran**. 06.11 için 93,03 / 68,65 = 1,3552 (z=+2): ertesi gün F_SAHOL SAT + F_AKBNK AL.
  - "Aşağı kesişme" → **alt oran**. 06.11 için 84,05 / 68,65 = 1,2243 (z=−2): ertesi gün F_SAHOL AL + F_AKBNK SAT.
  - Rapor seviyeyi yarının 60 günlük penceresiyle (en eski gün düşer) kesin çözer. `bist_sinyal.py` bugünün değerini değiştirerek yaklaşık verir (06.11: 93,06 / 84,09; fark 3–4 kuruş).
- Seviyeler 60 günlük pencereyle her gün biraz kayar. **Her akşam rapordan güncelleyin** (2 dakika).
- Giriş ertesi gün 17:50 kontrolü ve 17:55 limitli emirle yapılır, tutma 20 iş günüdür (PLAN_BIST K1). Kural 0 ve komisyon kapısı açılmadan K1 kâğıttır.

## 6. XU030 kapanış bazı sıçraması (fiyat alarmı, Pine yok)

Bu kural için Pine dosyası yok. Karar 18:10'daki spot kapanışı ile o anki vadeli fiyatını gerektirir. Günlük rapor her akşam iki oran seviyesini yazar (§3, "XU030 kapanış bazı" satırı). 06.11 için seviyeler 1,04656 (SAT) ve 1,03615 (AL)'dır.

1. Sembol kutusuna **`BIST:XU030D1!/BIST:XU030`** yazın. Zaman dilimi 1 dakika.
2. İki alarm kurun, ikisi de *Yalnızca bir kez*, *Bitiş*: ertesi gün 18:16:
   - "Yukarı kesişme" → üst oran. Vadeli dünküne göre pahalı kapanıyor: **XU030D1! SAT**.
   - "Aşağı kesişme" → alt oran. Vadeli ucuz kapanıyor: **XU030D1! AL**.
3. **Yalnız 18:08–18:15 arasında çalan alarm geçerlidir.**
   - Spot kapanış fiyatı ~18:08'de oluşur. Ondan önce oran sürekli işlem fiyatlarıyla hesaplanır ve kuralla ilgisi yoktur.
   - Gün içinde çalarsa yok sayın ve 18:08 sonrası için yeniden kurun.
4. Giriş 18:15'e kadar limitli emirle yapılır, çıkış ertesi gün uzlaşma penceresinde (≈ 18:05–18:15). 1 mn TL'de 1 kontrat; K9 riski %0,25 ve 1 kontrat ≈ 150 bin TL nominal.
5. **Sınırlar:**
   - Gerçek zamanlı VİOP ve BIST verisi şarttır. Gecikmeli veriyle bu kural uygulanamaz.
   - σ ≈ 50 bps sabittir; araştırmanın 120 günlük std ölçeği.
   - XU030D1! sürekli sembolü vade geçişinde (Aralık vadesi 31.12) sözleşme değiştirir. Geçişten önceki ve sonraki gün alarmı kurmayın.
   - Kenar zayıflıyor: 2024–26'da t 1,1.

## 7. ABD rejimi (`abd_rejim_ve_sablon.pine`, alarm zaten var)

- Grafik **SP:SPX** 1G. *Girdiler*:
  - FTD (`Gecerli FTD var mi?`),
  - pilot freni,
  - fren sonrası FTD.
- Bu girdileri günlük raporun §5 tablosuna göre elle işaretleyin. Gösterge bunları kendisi bilmez.
- Alarm: **"Rejim degisti"**, Bar kapanışında bir kez. ABD kapanışından sonra ~00:00–00:30 TSİ'de çalar.
- Günlük rapor aynı kuralı FRED ve CBOE verisiyle hesaplar ve sayaçları `gunluk/durum.json`'da tutar. Alarm ile rapor çelişirse kontrol listesi: VIX/VIX3M'in resmi kapanışı, FTD'nin hacim teyidi, S5FI/S5TH.

## 8. Asgari alarm seti ve günlük bakım

| # | Alarm | Kurulum | Bakım |
|---|---|---|---|
| 1 | TUPRS herhangi bir kural olayı | bir kez | — |
| 2 | Altın sinyali (geçici) | bir kez | — |
| 3 | KOZA \|z3\| eşik üstü | bir kez | arife günü pencere |
| 4 | KOZA bugün çıkış günü | bir kez | — |
| 5–6 | K1 oran üst / alt | her akşam seviye güncelle | rapor §2 |
| 7–8 | XU030 bazı oran üst / alt | her akşam yeniden kur | rapor §3 |
| 9 | ABD rejim değişti | bir kez | FTD/fren girdileri elle |
| (10–12) | SAHOL/AKBNK PRATİK giriş/çıkış (kâğıt) | isteğe bağlı | — |

**Unutmayın:**
- Alarm emir vermez. Emir aracı kurumda, kapanış penceresinde ve limitli verilir.
- Raporun §0 bölümündeki takvim ve KRİZ engelleri alarmdan önce gelir.
- Pine dosyaları derlenmeden kullanılmamalıdır; ilk kurulumda derleme ve karşılaştırma şart.
