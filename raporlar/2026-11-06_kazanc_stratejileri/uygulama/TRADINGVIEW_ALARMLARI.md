# TradingView alarmları: canlı fiyat ya da ABD verisi gereken sinyaller

_08.11.2026 (lead-lag kartlarıyla [LEADLAG_UYGULAMA.md] uyum düzeltmesi aynı gün). Günlük rapor (`gunluk/SON.md`) her iş günü ~21:05 TSİ'de çıkar. Bazı sinyallerin karar anı ise daha erkendir. TUPRS'un karar anı sabahtır, kapanış penceresi sinyallerininki 17:45–18:15'tir. Bu kural anlarını yalnız TradingView alarmı yakalar. Bu dosya alarmların adım adım kurulumunu anlatır. Bilgi amaçlıdır, yatırım tavsiyesi değildir._

> **Pine dosyalarının hiçbiri TradingView'da derlenmedi ve test edilmedi.** Bu ortamda Pine derleyicisi yok. İlk kullanımda göstergeyi grafiğe ekleyin. Derleme hatası çıkarsa satır numarasını not edin ve o sinyal için yalnız günlük rapora güvenin. Göstergenin son 5–10 günlük değerini günlük raporun §3 tablosuyla karşılaştırın. Fark büyükse (z'de > 0,1) raporu esas alın.

## 0. Önce: abonelik, veri ve genel ayarlar

**Alarm sayısı.** Aşağıdaki asgari set 9 alarm ister (§8). Ücretsiz Basic plan buna yetmez. Essential (≈20 alarm) yeter. Sayılar ve fiyatlar değişebilir; TradingView'ın plan sayfasından teyit edin. Ayrıca bazı planlarda alarmların süresi dolar (~2 ay). Takvime bir "alarmları yenile" notu koyun.

**Gerçek zamanlı veri.**
- BIST pay ve VİOP verisi TradingView'da varsayılan olarak **15 dakika gecikmelidir**. Gerçek zamanlı veri, Hesap → *Piyasa verisi abonelikleri* altında ayrı ücretli bir pakettir. Pay ve VİOP paketleri ayrı olabilir.
- Gecikmeye dayanıklı sinyaller:
  - **TUPRS:** Sinyal ABD'nin dünkü kapanışından hesaplanır.
  - **Altın:** TVC:GOLD genellikle gerçek zamanlıdır.
  - **ABD rejimi.**
- Gerçek zamanlı veri isteyen sinyaller: **XU030 bazı** ve **Koza** (Koza yalnız kâğıt kaydı). Gecikmeli veriyle 17:55'te ekranda 17:40 fiyatı görünür. XU030 bazında 18:10 fiyatı ancak 18:25'te gelir, yani işlem penceresi kapanmış olur. Paket alınmayacaksa bu sinyallerde alarmı yalnız hatırlatıcı sayın; kararı aracı kurumun canlı ekranından verin.
- SAHOL/AKBNK 1–3 gün PRATİK sinyali **emeklidir** (K1 ile değiştirildi). Alarm gerekmez.

**Genel ayarlar.**
- Grafik saat dilimi: *(UTC+3) İstanbul*.
- Bildirim: TradingView mobil uygulamasında anlık bildirim, isteğe bağlı olarak e-posta.
- Alarm penceresinde *Koşul*, grafiğe eklediğiniz göstergenin adıdır. Ardından açılan listeden aşağıdaki alarm başlığını seçin.
- **Sıklık seçimi (günlük 1G grafikte):**

| Seçenek (TR arayüz) | Ne zaman tetikler | Ne için |
|---|---|---|
| **Bar başına bir kez** (Once Per Bar) | Gün içinde koşul ilk sağlandığında, bir kez | Aynı gün karar: TUPRS'un sabah bildirimi; Koza ve altın (kâğıt kaydı) |
| **Bar kapanışında bir kez** (Once Per Bar Close) | Günlük bar kapanınca. BIST payında ~18:10, gecikmeli veride ~18:25 | Kapanışla kesinleşen ve **ertesi gün** işlenen sinyaller: K1 oranı, kâğıt kaydı, ABD rejimi (~00:00 TSİ) |
| **Yalnızca bir kez** (Only Once) | Bir kez tetikler, sonra kapanır | Her akşam rapordan güncellenen seviye alarmları (XU030 bazı) |

**Plan kısıtları alarmlar için de geçerlidir.**
- **Bu sinyaller K9 kanalı değildir** (PLAN_BIST K9 "Eski lead-lag sinyalleri", §3.11). Eski lead-lag sinyalleri (XU030 bazı, TUPRS, Koza) canlıya geçerse **hepsinin toplam açık riski ≤ %0,5** olur ve bu bütçe **K4 sondalarından düşülür**. Boylar işlem başı ~%0,25 varsayar; böylece aynı anda iki sinyal sığar. Rapor açık riski `durum.json` → `acik_pozisyonlar`'dan hesaplar ve K4 tavanından düşer.
- **K9 yalnız plan dışı yeni fikirler içindir:** fikir kartı 18:45'e kadar, emir **ertesi gün** kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli. Aynı gün uzlaşmada giren bir alarm sinyali K9 olamaz.
- **Yalnız kâğıt:**
  - Altın → TRALT ve kredi notu tersi düşük güvenlidir, eski dörde dahil değildir. Altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz.
  - Koza: NET_LISTE_BIST'te IZLE (2024–26 net ≈ +1 bps). Canlıya almak için `durum.json` → `ayarlar.koza` = `"canli"` gerekir.
  - SAHOL/AKBNK 1–3G: emekli (K1, 20 gün).
  - RYGYO → RYSAS: yalnız K4 RYSAS girişi için FİLTRE ve kâğıt kural; canlı işlem kanalı yok.
- **Kural 0:** Aracı kurumun yazılı cevabı gelene kadar bütün VİOP kolları kâğıttır. Rapor bunu `gunluk/makro.json` → `kural0_teyit` alanından okur (varsayılan `false`). `false` iken §0 hiçbir VİOP sinyalini canlı işlem olarak yazmaz; "KÂĞIT" ve neden yazar.
- Takvim engelleri:
  - 9.11: A1. Bilançosu gelmemiş TRALT, TRMET vb.
  - 11.11: hiçbir yeni giriş yok.
  - 12–13.11: K3/K4/K5/K9 girişi yok. Rapor eski lead-lag sinyallerinde de yeni giriş yazmaz (bütçeleri K4'ten geldiği için ihtiyat).
  - Ayrıca KRİZ kesicisi.
- Günlük raporun §0 bölümü bu engelleri her akşam yazar. Alarm çalsa da engel varsa işlem yapılmaz.

## 1. Özet: hangi ticker, hangi yön, hangi alarm

| # | Sinyal | Öncü (lead) | İşlem bacağı (lag) | Yön | Pine / alarm | Grafik | Sıklık | Bildirim (TSİ) | İşlem (TSİ) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **TUPRS ← ABD rafinerileri** | NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF; SP:SPX'e göre β-arındırılmış ortalama artık, ABD'nin t−1 günü | BIST:TUPRS1! | **Aynı yön.** Rafineriler dün S&P'yi geçtiyse (z > +1) F_TUPRS AL, geride kaldıysa (z < −1) SAT | `rehber/tuprs/tuprs_alarm.pine` → "TUPRS herhangi bir kural olayı" | BIST:TUPRS1! 1G | Bar başına bir kez | ~10:00–10:15 (BIST açılışı) | Aynı gün 18:00–18:10 giriş; t+2 uzlaşmasında çıkış kontrolü. Kural 0 teyidine kadar kâğıt |
| 2 | **Altın → TRALT** | TVC:GOLD (17:55 fiyatı, bir önceki BIST gününün 17:55'ine göre) | BIST:TRALT1! + hedge BIST:XU030D1! | **Aynı yön.** Altın z > +1 ise TRALT1! AL + XU030D1! SAT; z < −1 ise tersi | `rehber/altin/altin.pine` → "Altın sinyali (geçici)" (dosyada zaten var) | BIST:TRALT1! 1G | Bar başına bir kez | Gün içinde ilk eşik aşımında; **karar 17:55** | **Yalnız kâğıt** (18:00–18:10; 2 BIST günü) |
| 3 | **Koza göreli momentumu** | Lead-lag yok. TRMET'in BIST:TRALT ve BIST:TRENJ ortalamasına göre son 3 günlük artığı | BIST:TRMET1! + BIST:TRALT1! (β_TA ≈ 0,69 → ~1:2 kontrat) | **Momentum yönü.** z3 > +1,5 ise TRMET1! AL + TRALT1! SAT; z3 < −1,5 ise tersi | `rehber/koza/koza_alarm.pine` (yeni) → "KOZA \|z3\| eşik üstü" + "KOZA bugün çıkış günü" | BIST:XU030 1G | Bar başına bir kez | 17:45–18:10 penceresi; çıkış hatırlatması sabah | **Kâğıt** (NET_LISTE_BIST: IZLE). Kural: 18:00–18:10; 2 gün, sinyal sürerse +2 (≤ 6) |
| 4 | **SAHOL/AKBNK 1–3G PRATİK** (β'lı artık z) | Lead-lag yok, ortalamaya dönüş | — | — | Kurulmaz | — | — | — | **Emekli** (PLAN_BIST §3.11: K1 ile değiştirildi). Rapor §3'te yalnız "kâğıt (emekli)" satırı |
| 5 | **K1 SAHOL↔AKBNK** (plan, 20 gün) | Lead-lag yok, 60 günlük ln oran z | F_SAHOL ve F_AKBNK, Aralık vadesi | **z'nin tersi.** Oran üst seviyeyi geçerse SAHOL SAT + AKBNK AL; alt seviyenin altına inerse tersi | Fiyat alarmı, spread sembolü `BIST:SAHOL/BIST:AKBNK`. Seviyeler raporun §2 K1 satırında | BIST:SAHOL/BIST:AKBNK 1G | Bar kapanışında bir kez | ~18:10 | **Ertesi gün** 17:55. Kural 0 ve ≤ 5 bps komisyon teyidine kadar kâğıt |
| 6 | **XU030 kapanış bazı sıçraması** | BIST:XU030 spot kapanışı ile BIST:XU030D1! son fiyatı (18:10–18:15) | BIST:XU030D1! | **Bazın tersi.** Vadeli dünküne göre pahalı kapandıysa (oran üst seviyenin üstünde) SAT, ucuz kapandıysa AL | Fiyat alarmı, spread sembolü `BIST:XU030D1!/BIST:XU030`. İki seviye (std120 eşiği) raporun §3 tablosunda ve §0 TradingView satırında, **her akşam yeni** | aynı spread, 1 dk | Yalnızca bir kez | Yalnız 18:08–18:15 arası anlamlı | 18:15'e kadar giriş; ertesi gün uzlaşmada çıkış. Kural 0 teyidine kadar kâğıt |
| 7 | **ABD rejimi** | SP:SPX, NASDAQ:NDX, CBOE:VIX/CBOE:VIX3M | ABD hesabı (IBKR) | Durum değişimi | `uygulama/kod/abd_rejim_ve_sablon.pine` → "Rejim degisti" (dosyada zaten var) | SP:SPX 1G | Bar kapanışında bir kez | ~00:00–00:30 | Ertesi gün 16:45–17:15 emir bloğu |

**Önerilmeyenler.** PRATIK_LISTE'deki düşük güvenli lead-lag'ler için alarm kurmayın. Bunlar ASX:FMG + ASX:BHP → EREGL, VİOP USDTRY → THYAO, ay dönümü ve kredi notu tersidir. Kredi notu kâğıtta izlenir; canlıya ancak K9'dan girer (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra. Kenarları ya küçük ya da yalnız belirli rejimlerde var. Ayrıca "bilgi BIST kapanışından sonra geliyor" grubundaki hiçbir sinyal (ABD vadelisi → açılış gap'i vb.) bu profil için uygun değildir.

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
   - Boyut (rehber §4): kontrat = taban(sermaye × risk / (100 × fiyat × L)). L ≈ 1,65 × σ60 × √2, taban %4. Risk eski lead-lag bütçesinden gelir (K9 değil): işlem başı ~%0,25, toplam ≤ %0,5, K4 sondalarından düşer. 1 mn TL'de 1 kontrat (06.11: F_TUPRS1226 354,65, L %5,9 → kontrat başı risk ≈ 2.081 TL, ~%0,2). Rapor §3 bu sayıyı her akşam yeniden yazar.
   - Kural 0 yazılı teyidi gelene kadar yalnız kâğıt.
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
   - Kontrat oranı rapordadır (06.11: 1 : 2,0). İşlem başı ~%0,25 ile (eski lead-lag bütçesi, K9 değil) 1 mn TL'de 6 TRMET1! : 12 TRALT1!.
   - **Koza şu an kâğıttır** (NET_LISTE_BIST: IZLE; 2024–26 net ≈ +1 bps). Alarm kâğıt kaydı içindir.
   - Vade, planlanan çıkıştan **sonra** biten en yakın vadedir. 26.11'den sonraki girişlerde Aralık vadesi.
6. **Pencere ayarı:** Göstergenin *Ayarlar → Girdiler → Alarm* grubundaki saatler değiştirilebilir. Arife günlerinde (yarım gün) pencereyi 12:00–12:30'a çekin ya da o gün alarmı yok sayın.

## 4. Altın → TRALT (`altin.pine`, alarm zaten var) — yalnız kâğıt

`altin.pine` dosyasında `alertcondition(provSig, "Altın sinyali (geçici)")` zaten var. Yeni kopya yazılmadı.

**Yalnız kâğıt kaydı.** Bu sinyal düşük güvenlidir ve eski dört lead-lag sinyaline dahil değildir. Aynı gün uzlaşmasında girdiği için K9'un "emir ertesi gün" kuralıyla da açılamaz. Planda canlı kanalı yoktur [PLAN_BIST §3.11; LEADLAG_UYGULAMA §1.10]. Aşağıdaki adımlar kâğıt kaydının nasıl tutulacağını anlatır.

1. **BIST:TRALT1!** grafiğini açın, zaman dilimi **1G**. `rehber/altin/altin.pine` dosyasını ekleyin.
   - *Altın sembolü:* TVC:GOLD (varsayılan). COMEX:GC1! kullanmayın, vade geçişinde sıçrar.
   - σ için yeterli alt zaman dilimi geçmişi yoksa (Basic planda ~200 gün) *Elle σ* girdisine **1,70** yazın. Günlük rapor da bu sabiti kullanır.
   - Rapor ayrıca vekil σ'yı yazar: VİOP F_XAUUSD uzlaşma değişiminin σ'sı. Geçmiş `gunluk/altin_vekil.csv`'de tutulur, her akşam bir satır eklenir. 06.11'de σ150 = **%1,48**. Bu yalnız kontroldür, karar eşiği 1,70'tir. Vekil 250 güne ulaşınca (≈ Mart 2027) fark 0,3 puanı aşarsa altin.pine'ın kendi σ250'sine bakın.
2. Alarm: **"Altın sinyali (geçici)"**, Bar başına bir kez.
   - Gün içinde |z| ilk kez 1'i aştığında çalar. Sinyal sonradan kaybolabilir.
   - **Karar yalnız 17:55'te** verilir: g = ln(TVC:GOLD 17:55 / dünkü 17:55), z = g / 0,0170.
   - |z| > 1 ise 18:00–18:10'da girin. Yön: z > 0 ise TRALT1! AL + XU030D1! SAT, z < 0 ise tersi.
   - Oran: 1 XU030D1! kontratına karşı N TRALT1!. 06.11 için N = 29, β 1,30. Günlük rapor her akşam yeniden yazar.
   - Kâğıt boyu: 1 mn TL'de **1 birim**.
3. Çıkış: 2 BIST günü sonra 17:55'te yeniden bakılır.
   - Aynı yönde |z| > 1 ise tutulur. Ters yönde ise çevrilir.
   - Sinyal yoksa 18:00–18:10'da iki bacak birlikte kapatılır.
4. Günlük rapor F_XAUUSD uzlaşma değişimini **vekil** olarak gösterir. Bu, araştırmanın asıl sinyalidir ama işlemle aynı dakikada oluşur. Bu yüzden 21:05'te yalnız "bugün tetiklendi mi" bilgisi verir.

## 5. SAHOL/AKBNK: PRATİK artık z ve plan K1

**5a. PRATİK 1–3G artık z: emekli.**
- PLAN_BIST §3.11 bu sinyali K1 (20 gün) ile değiştirdi. Aynı çiftte iki sinyal çalıştırılmaz.
- Alarm kurmayın. `sahol_akbnk_z.pine` yalnız isteğe bağlı kâğıt kaydı içindir.
- Rapor bu sinyali §0'a ve `BILDIRIM.txt`'nin yakın tetik satırına yazmaz. §3'te yalnız "kâğıt (emekli)" satırı kalır.
- `durum.json` → `ayarlar.pratik_sahol_akbnk` alanı artık yok sayılır. 6.11'den önce açılmış bir pozisyon varsa `acik_pozisyonlar`'da `PRATIK_SAHOL` olarak kalır ve kendi çıkış kuralıyla (|z| ≤ 1,5) kapanır.

**5b. K1 (plan): oran alarmı.**
- Sembol kutusuna **`BIST:SAHOL/BIST:AKBNK`** yazın. TradingView bunu oran grafiği olarak açar. Zaman dilimi 1G.
- İki fiyat alarmı kurun, ikisi de *Bar kapanışında bir kez*:
  - "Yukarı kesişme" → raporun §2 K1 satırındaki **üst oran**. 06.11 için 93,03 / 68,65 = 1,3552 (z=+2): ertesi gün F_SAHOL SAT + F_AKBNK AL.
  - "Aşağı kesişme" → **alt oran**. 06.11 için 84,05 / 68,65 = 1,2243 (z=−2): ertesi gün F_SAHOL AL + F_AKBNK SAT.
  - Rapor seviyeyi yarının 60 günlük penceresiyle (en eski gün düşer) kesin çözer. `bist_sinyal.py` bugünün değerini değiştirerek yaklaşık verir (06.11: 93,06 / 84,09; fark 3–4 kuruş).
- Seviyeler 60 günlük pencereyle her gün biraz kayar. **Her akşam rapordan güncelleyin** (2 dakika).
- Giriş ertesi gün 17:50 kontrolü ve 17:55 limitli emirle yapılır, tutma 20 iş günüdür (PLAN_BIST K1). Kural 0 (`makro.json` → `kural0_teyit`) ve komisyon kapısı (≤ 5 bps) açılmadan K1 kâğıttır.

## 6. XU030 kapanış bazı sıçraması (fiyat alarmı, Pine yok)

Bu kural için Pine dosyası yok. Karar 18:10'daki spot kapanışı ile o anki vadeli fiyatını gerektirir.

**Eşik sabit değildir.** Kural |Δb| > std120(Δb)'dir [LEADLAG_UYGULAMA §1.2]. Burada b = ln(F / S) ve Δb = b − dünkü b'dir (aynı sözleşme). Eski sabit "50 bps" yanlıştır.
- Günlük rapor geçmişi `gunluk/xu030_baz.csv`'de tutar: tarih, sözleşme, F (bülten kapanış fiyatı, yoksa uzlaşma), spot kapanış, b, Δb. Lead-lag çalışmasının 150 bülten günüyle (01.04–06.11.2026) başlatıldı. Her akşam bir satır eklenir. Devir günü Δb boş kalır.
- std120, son 120 bülten gününün std'sidir. Araştırmadaki gibi bir gün gecikmelidir: yarının eşiği bugünkü std120'dir. Devir günleri pencerede yer tutar.
- Rapor her akşam iki oran seviyesi yazar: **üst = e^(b_bugün + std120)** (SAT), **alt = e^(b_bugün − std120)** (AL). Seviyeler §3 tablosunun "XU030 kapanış bazı" satırında ve §0'daki TradingView satırındadır.
- **06.11 → 9.11 için:** std120 = **68 bps**, b = +405 bps. Oran **< 1,0343 AL**, **> 1,0484 SAT**. 06.11 spotuyla (14.290) bu F ≤ 14.781 / ≥ 14.982 demektir. 9.11'de spot değişeceği için F'yi değil oranı kullanın.
- **Mayıs 2026 şoku:** 68 bps tek bir şoktan şişiyor. 21.05.2026'da Δb −458 bps oldu (F_XU0300626 −%10,0, spot −%5,8), 22.05'te +352 bps. Bu iki gün hariç std ≈ **42 bps**. 21.05, 12.11 akşamı 120 günlük pencereden çıkar; 22.05 ertesi akşam (13.11). Yeni şok olmazsa 16.11 seviyeleri ~42 bps'e göre daralır. Rapor şokları ve çıkış tarihlerini §3'ün altında her akşam yazar.
  - Not: LEADLAG_UYGULAMA §1.2 eskiden "~17.11" diyordu (120 **geçerli** gözlem sayımı). Araştırma kodunun tanımı (`06_baz_std.py`: `rolling(120)`, devir günleri dahil 120 satır; kural bir gün gecikmeli) 12–13.11'i verir. Rapor bu tanımı kullanır; LEADLAG 08.11 yeniden testte düzeltildi.

1. Sembol kutusuna **`BIST:XU030D1!/BIST:XU030`** yazın. Zaman dilimi 1 dakika.
2. İki alarm kurun, ikisi de *Yalnızca bir kez*, *Bitiş*: ertesi gün 18:16:
   - "Yukarı kesişme" → üst oran. Vadeli dünküne göre pahalı kapanıyor: **XU030D1! SAT**.
   - "Aşağı kesişme" → alt oran. Vadeli ucuz kapanıyor: **XU030D1! AL**.
   - **Seviyeleri her akşam rapordan yeniden kurun.** std120 ve b her gün değişir.
3. **Yalnız 18:08–18:15 arasında çalan alarm geçerlidir.**
   - Spot kapanış fiyatı ~18:08'de oluşur. Ondan önce oran sürekli işlem fiyatlarıyla hesaplanır ve kuralla ilgisi yoktur.
   - Gün içinde çalarsa yok sayın ve 18:08 sonrası için yeniden kurun.
4. Giriş 18:15'e kadar limitli emirle yapılır, çıkış ertesi gün uzlaşma penceresinde (≈ 18:05–18:15). 1 mn TL'de en çok 1 kontrat (≈ 149 bin TL nominal). Stop yok (1 gün).
   - Bütçe: eski lead-lag bütçesi (K9 değil). Toplam açık risk ≤ %0,5, K4 sondalarından düşer.
   - Kural 0 yazılı teyidi (`makro.json` → `kural0_teyit`) gelene kadar **kâğıt**.
5. **Sınırlar:**
   - Gerçek zamanlı VİOP ve BIST verisi şarttır. Gecikmeli veriyle bu kural uygulanamaz.
   - Rapordaki b bültenin kapanış fiyatıyla hesaplanır. Kural 18:10 son fiyatını ister, yani rapor değeri yaklaşıktır. Eşik (std120) aynı yöntemle ölçüldüğü için tutarlıdır.
   - XU030D1! sürekli sembolü vade geçişinde (Aralık vadesi 31.12) sözleşme değiştirir. Geçişten önceki ve sonraki gün alarmı kurmayın. Rapor vadeye ≤ 2 iş günü kalınca "alarm kurma" yazar.
   - Kenar zayıflıyor: 2024–26'da t 1,1.

## 6b. RYGYO → RYSAS filtresi (isteğe bağlı fiyat alarmı, kâğıt)

Bu bir işlem sinyali değildir [LEADLAG_UYGULAMA §1.7].
- **(a) K4 RYSAS filtresi:** RYSAS'ta K4 girişi beklenen gün RYGYO z < −1 ise o akşam girilmez. z = ln(RYGYO_t / RYGYO_t−1) / sd250 (önceki gün dahil), ±5'te kırpılır.
- **(b) Kâğıt kural:** z > +1 ise RYSAS 18:10–18:15 kapanış fiyatından işlemler seansında alınır, ertesi kapanışta satılır. Yalnız kâğıt kaydı.
- **Canlı kanal yok.** RYSAS VİOP-47 hissesi değildir ve K9 emri ertesi güne atar (1 gün geç giriş −15,8 bps).

Kurulum: `BIST:RYGYO` üzerinde iki fiyat alarmı, *Bar kapanışında bir kez*. Seviyeler raporun §3'ündeki RYGYO satırındadır (= kapanış × e^(±sd250)). 06.11 → 9.11: **≥ 50,61** (z > +1) / **≤ 47,63** (z < −1); sd250 %3,03. Rapor üst seviyeyi yukarı, alt seviyeyi aşağı yuvarlar; böylece yazılan fiyat kuralı kesin sağlar (47,64'te z −0,997 olurdu). K4 emri 18:01'de verildiği için RYGYO kapanışı o anda bilinmez. Vekil olarak 17:55'teki canlı değişimi (≤ −sd250, ≈ −%3) kullanın. Gecikmeli veriyle alarm 18:25'te gelir. Yalnız RYSAS K4 girişi yaklaşırken kurun.

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
| 7–8 | XU030 bazı oran üst / alt | her akşam yeniden kur (std120 seviyeleri) | rapor §3 ve §0 |
| 9 | ABD rejim değişti | bir kez | FTD/fren girdileri elle |
| (10–11) | RYGYO ≥ / ≤ (K4 RYSAS filtresi, kâğıt) | yalnız RYSAS K4 girişi yaklaşırken | rapor §3 |
| — | SAHOL/AKBNK 1–3G PRATİK | **kurmayın** (emekli) | — |

**Unutmayın:**
- Alarm emir vermez. Emir aracı kurumda, kapanış penceresinde ve limitli verilir.
- Raporun §0 bölümündeki takvim, KRİZ ve Kural 0 engelleri alarmdan önce gelir. Kural 0 teyitsizken bütün VİOP alarmları yalnız kâğıt kaydı içindir.
- Pine dosyaları derlenmeden kullanılmamalıdır; ilk kurulumda derleme ve karşılaştırma şart.
