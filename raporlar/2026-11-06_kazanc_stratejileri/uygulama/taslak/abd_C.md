# ABD swing planı C: "Önce risk, kanıt minimalizmi"

**Hazırlanma:** Cuma 06.11.2026, ~14:00 TSİ. Son kapanış Perşembe 05.11.2026. Ekim NFP bugün 16:30 TSİ'de açıklanacak; buradaki rejim okuması **NFP öncesine** ait ve Cuma kapanışıyla (Cumartesi sabahı) yeniden yapılmalı.
**Başlangıç:** Pazartesi 09.11.2026. ABD seansı 17:30–00:00 TSİ (1 Kasım'dan beri EST, TSİ = ET + 8).
**Kullanıcı:** Türkiye'de yerleşik, BIST spot + VİOP tecrübeli. Swing ufku (günler–haftalar, en çok birkaç ay). Gün içi ekran işlemi yok, al-tut yok. Tematik küme ("stratejik küme") seviyor.
**Bu planın açısı:** Küçük başla, kenarı **kendi işlemlerinle** kanıtla, yalnız doğrulamadan sağ çıkan kurallarla oyna, kanıt gelmeden ölçek büyütme. Yüksek getiri hedefi, kanıttan **sonra** açılan bir kapı; baştan varsayılmıyor.
Yatırım tavsiyesi değildir. Vergi satırları mali müşavirle teyit edilmeli.

**Kaynak kısaltmaları** (yollar `raporlar/2026-11-06_kazanc_stratejileri/` altında; doğrulama dosyaları raporlarla çeliştiğinde doğrulama geçerli):

| Kısaltma | Dosya |
|---|---|
| KIM | `ajanlar/abd_kim_kazaniyor.md` |
| KEN | `ajanlar/abd_swing_kenarlar.md` |
| TEST | `ajanlar/abd_test.md` |
| PRA | `ajanlar/abd_pratik.md` |
| PROF | `ajanlar/abd_profesyonel.md` |
| DLG | `ajanlar/dalga_abd.md` |
| SEY | `ajanlar/seytan_taban_oranlar.md` |
| TRM | `ajanlar/tr_makro_engel.md` |
| VA / VC / VD / VP | `dogrulama/v_abd.md`, `v_capraz.md`, `v_dalga.md`, `v_profesyonel.md` |
| HAZ | `uygulama/abd_hafta_hazirlik.md` |
| C-TEST | Bu plan için yaptığım küçük hesaplar (repo dışında, scratchpad): `.../scratchpad/abd_C/vix_event.py`, `vix_event2.py`, `hurdle.py`, `ma.py`. Veri: Cboe VIX/VIX3M CSV, Ken French günlük faktörleri (2026-09'a kadar), FRED SP500/NASDAQ100 |

---

## 0. Tek paragrafta plan

Toplam likit sermayenin (C) yalnız **%10'unu (en çok %15'ini)** ABD strateji sermayesi (E) olarak ayır, geri kalanı TL'de bırak. Kenarı kanıtlanmamış bir sistemi büyük sermayeyle denemenin bedeli, aynı sistemi küçük sermayeyle denemekle R cinsinden aynı, ama lira cinsinden 7–10 kat fazla. E'nin içinde üç kol var:
- **S1, çekirdek:** rejim filtreli lider swing. İşlem başı risk ilk 50 işlemde **E'nin %0,25'i**. Bilanço serisi ve revizyon filtresi yalnız eleme için kullanılıyor.
- **S2, uydu:** fırsatçı insider küme alımları.
- **S3, uydu:** VIX panik çözülme penceresi. Kural ilk VIX>25 kapanışında almak değil, **vade yapısı normale döndüğünde** almak.

Opsiyon alımı IV yüksekken yasak; bugün (VIX 28,2, VIX/VIX3M 1,10) tamamen kapalı. Rejim anahtarı bugün **KIRMIZI**: Pazartesi S1'de yeni alım yok, yalnız hesap, emir testi, izleme listesi ve günlük kurulumu var. Ölçeği yalnız önceden yazılmış istatistik kapıları büyütür (50 işlem + t ≥ 1,0; 100 işlem + t ≥ 1,65). Öldürme kriterleri de önceden yazılı. 1. yılın dürüst beklentisi vergi öncesi USD **−%8 ile +%15** (merkez +%2–6). Bu, TL engelinin (%13–26) altında. Bilinçli olarak ödenen bir "ölçüm bedeli": C'nin ~%1–2,5'i.

---

## 1. Sermaye ve engel kararı: TL mi, USD mi, ne kadar?

### 1.1 Engelin bileşenleri (doğrulanmış)

| Kalem | Değer | Kaynak |
|---|---|---|
| TL'de kalmanın net nominal getirisi | Faiz sabitse ~%36–38 (32 günlük mevduat roll); anket patikasında ~%31–33 | VC #4 |
| TL'de kalmanın USD karşılığı, ileriye dönük | ~%13–15,5 (kur ~%17,5–20 artarsa). Kur vadelinin fiyatladığı kadar (%32,9) artarsa net PPF USD bazında ~−%1,5 | VA #34; TRM §1.4; VC #5 |
| TL carry'nin geçmişi (USD bazında) | 2010–26: **−%7,2/yıl, MaxDD −%85**. 2024–26: +%21/yıl | TEST §2; VA #34 |
| USD risksiz | 3 aylık T-bill %4,03 (DTB3, 4.11), 13 hafta kupon eşdeğeri %4,10; IBKR boş nakit faizi %3,38 | VC #13; PRA §4.1 |
| ABD kazancının TR vergisi | Değer artışı kazancı, TL bazında, **kur farkı dahil**, artan oranlı %15–40. Zarar yalnız aynı yıl içinde mahsup edilir, devredilmez. Yİ-ÜFE endekslemesi ancak ≥%10 artışta (~6 ay); swing'de pratikte yok. Margin faizi indirilemez | VC #10; PRA §2.1 |
| 2026 tarifesi | 190 bin / 400 bin / 1 mn / 5,3 mn TL; %15/20/27/35/40. **Doğrulanamadı** (VC #11); 2025 tarifesi GİB'de teyitli | PRA §2.1; VC #11 |
| Temettü | ABD stopajı %20 (gerçek kişi, W-8BEN ile) | VC #12 |
| Elde tutulan dövizin kur kazancı | Vergilenmez (döviz menkul kıymet değil). Menkul kıymet içindeki kur kazancı vergilenir | PRA §2.5, §4.2 (mali müşavirle teyit) |

### 1.2 Hesabın boyutuna göre gereken vergi öncesi USD getirisi (C-TEST `hurdle.py`)

**Model** (PRA §2.6 mantığının sadeleştirilmiş hâli):
- Vergilenebilir TL kazancı ≈ E × kur × [R × (1+d) + u × d].
  - R: vergi öncesi USD getirisi (boştaki nakdin faizi dahil).
  - d: yıllık USDTRY artışı.
  - u: sermayenin pozisyonda kaldığı pay. Pozisyondaki sermayenin kur farkı vergiye giriyor, boştaki USD nakdinki girmiyor.
- Başka beyan geliri yok; vergi ertelemesinin faydası sayılmadı (muhafazakâr).

| E (USD) | h=%31, d=%20 | h=%37, d=%20 | h=%31, d=%32,9 | h=%37, d=%32,9 | Not |
|---|---|---|---|---|---|
| 50.000, u=0,3 | **%12,7** | **%19,5** | −%0,3 | %5,4 | Bu planın tipik maruziyeti u≈0,3 |
| 250.000, u=0,3 | **%15,6** | **%23,3** | %0,7 | %7,7 | |
| 1.000.000, u=0,3 | **%17,5** | **%25,9** | %1,6 | %9,1 | Üst dilim %40 |
| 250.000, u=1,0 | %22,1 | %30,5 | %10,3 | %17,8 | Tam yatırım; doğrulanmış çapa "~%20–28" ile tutarlı (VC #22) |

**Okuma:**
1. Engel boyuta göre değişiyor. Küçük hesapta vergi dilimi düşük olduğu için engel de düşük.
2. Engelin büyük kısmı **kur varsayımı**. Kur 2024–26 temposunda (~%20) giderse ABD'nin TL'yi yenmesi için %13–26 gerekiyor. Vadelinin fiyatladığı hızla (%32,9) giderse ~%0–9 yetiyor. Yani "TL'de kalmak" risksiz bir seçenek değil, kurun vadeliden yavaş artacağına oynanan bir carry bahsi (TRM §1.4).
3. **Hayalet vergi.** Sıfır USD getiride bile pozisyondaki sermayenin kur farkı vergileniyor. u=0,3 ve d=%20 ile E'nin **%0,9 / %1,3 / %1,9**'u (50k / 250k / 1m). Pratik kural: boştaki USD **T-bill ya da ETF'te değil, aracı kurumda nakit** olarak beklemeli. Kur farkı vergisiz kalır, faiz %3,38 olur (PRA §2.5, §4.2; teyit şart).

### 1.3 Karar

| Durum | Karar | Gerekçe (sayılarla) |
|---|---|---|
| **Sermaye TL'de** | **E = C'nin %10'u** (en çok %15'i). Kalan %85–90 TL'de (mevduat/PPF net ~%31–38) | (a) S1'in bu kullanıcı için kenarı ölçülmedi; bu tarza en yakın test hiç yapılmadı (VA §4.2). (b) %0,25 riskte brüt maruziyet ~%15–35, yani E'nin ~%70'i nakitte, %3,38 kazanıyor. TL'nin ileriye dönük USD karşılığı ise %13–15,5 → boşta bekleyen kısım E'nin yılda ~%7–8,5'i kadar fırsat maliyeti yaratıyor. (c) 1. yıl beklentisi (§8) engelin altında; açık C'nin %1–2,5'i ile sınırlı. (d) USD'yi "TL şok sigortası" diye büyütmek de haklı değil: ortodoks rejimde başabaş şok olasılığı %39/%25, gözlenen sıklık ~%22/%11. Sigorta pahalı (VC #21) |
| **Sermaye zaten USD'de** (Eurobond, döviz hesabı) | E = min(eldeki USD, C'nin %20'si); çevrim yok | Kıyas artık TL değil, USD nakit/T-bill (~%3,4–4). Hayalet vergi ve maliyetle birlikte strateji vergi öncesi ~%5–8 USD yaparsa değer (yaklaşık; C-TEST mantığı). Risk kuralları aynı kalır |
| **Ölçek büyütme** | E'yi C'nin %25–35'ine çıkarmak **yalnız** §7'deki Faz 3 kapısı geçilirse | Kenar istatistiksel olarak görülmeden sermaye büyütmek SEY §3.3'teki "tahmin hatası Kelly'yi öldürür" tuzağı |

**Ayrı bir anahtar: makro döviz tahsisi.** Bu, işlem kenarından bağımsız bir karar. Aşağıdaki **iki** koşul oluşursa C'nin USD payını %25–35'e çıkar. Bu USD nakit olarak tutulur, işlem riski artırılmaz (TRM §5.1 "carry'den çık / long USD" tetikleri):
- Swap hariç net rezerv <0, ya da 2 hafta üst üste haftalık düşüş >5 mlr $. Şu an: 24,3 mlr $, son hafta −6,5 mlr $; koşulun yarısı oluştu.
- Yabancı DİBS çıkışı >1 mlr $, 2 hafta üst üste. Şu an −750 mn $.
- CDS 5 yıl >300. Şu an 248.
- 1 aylık USDTRY vadelisinin zımni yıllık getirisi politika faizini 5 puan aşıyor. Şu an ~%34, faiz %36.
- Ex-ante reel faiz <%3. Şu an %9,8; VC #3'e göre makul bant %5–8.

Bugün tam oluşan koşul yok. **Perşembe 12.11'deki rezerv verisi kritik:** ikinci bir >5 mlr $ düşüş birinci koşulu tamamlar.

---

## 2. Kollar: giriş, çıkış, stop, boyut, piramit ve emir tipi

### 2.0 Neden yalnız bu üç kol? (minimalizmin gerekçesi)

- **Elenenlerin çoğu öldü.** Yayınlanmış anomalilerin çoğu çürüdü: Chen-Zimmermann 2010 sonrası likit medyan aylık ~%0,13–0,20 (VA #22; TEST §6). 12-1 momentum 2010'dan beri yılda ~%2,6–4 (KEN §1.2; TEST §0.4). Büyük hissede PEAD yok (VA #23). Koşulsuz kısa vadeli reversal ~0 (TEST §7). Sektör momentumu 2010 sonrası risk-ayarlı olarak piyasa düzeyinde (VA §2.2, §3.1; VD U4, U7).
- **Kaldıraçlı trend bu planda yok.** 2x/3x + 200-DMA 2010–26'da %18–26 CAGR verdi ama düşüşleri −%55 ile −%97 arası, filtre de getiriyi kesti (VA §2.1). Bu bir kenar değil, kaldıraçlı beta; "önce risk" açısıyla çelişiyor.
- **Episodic pivot (bilanço sıçraması) giriş kolu da yok.** Giriş açılışın ilk 5–60 dakikasını gerektiriyor (KIM §5.4). Hakemli kanıtı yok, test de edilemedi (KEN §4.1; TEST §8). Bilanço tepkisi yalnız **filtre** olarak kullanılıyor.
- **Kalan üç kolun her biri** doğrulamadan geçmiş bir bulguya dayanıyor ve gün içi ekran istemeden **önceden yerleştirilen emirlerle** uygulanabiliyor.

### 2.1 S1: Rejim filtreli lider swing (çekirdek; işlemlerin ~%70–80'i)

**Kanıt ve sınırları:**
- Doğrulanmış kazananların ortak yöntemi: %0,25–1 risk, yapısal stop, %22–45 isabet ve 2–5R kazananlar, 3–5 günde kısmi satış, 10/20 GHO ile trail, yalnız kazanana ekleme, rejim anahtarı (PROF §1.3; KIM §4.2; VA #13–14).
- Payda kötü: USIC katılımcılarının yalnız %8–17'si kârlı (VA #14).
- Luk'un işlem istatistikleri ve Minervini'nin isabet rakamı **doğrulanamadı** (VA #15; VP A3).
- Tekil hissede trend takibi gerçek ama mütevazı: brüt CAGR %15,19 (1991–2024), işlemlerin <%7'si kârın çoğunu üretiyor (VA #18).
- Kurallı Kullamägi kopyası 2008–25'te %19 CAGR / −%21 MDD verdi; maliyet ve survivorship raporlanmadı. Kapanış bazlı 1 ATR stop ve 3 günlük çıkış kötü sonuç verdi (VP A12).
- Uzun-yalnız momentum 2010–26'da piyasayı getiride geçti (%17,8'e karşı %14,1), risk-ayarlı geçemedi (TEST §0.5).

**Evren (haftalık, Cumartesi):**
1. **Tarama** (HAZ §5a; TradingView Pine betiği HAZ'da hazır):
   - Fiyat >20 $, piyasa değeri >2 mlr $, 30 günlük ortalama hacim >750 bin, **50 günlük dolar hacmi ≥20 mn $**.
   - `TT = 1`: fiyat > 50 > 150 > 200 GHO, 200 GHO 21 gün öncesinden yüksek, fiyat ≥ 1,3 × 52 haftalık dip ve ≥ 0,75 × 52 haftalık zirve.
   - `RS line / 52w max ≥ 0,97`; 52 haftalık zirveye uzaklık ≥ −%10 (tercihen ≥ −%5).
   - Sıralama: `RS raw` azalan.
   - Finviz karşılığı (HAZ §5a, "sıkı versiyon"): `cap_midover, sh_avgvol_o1000, sh_price_o20, ta_highlow52w_b0to5h, ta_sma200_pa, ta_sma50_pa, ta_volatility_mo2`. Son filtre birleşme arbitrajı hisselerini eliyor.
2. **Küme filtresi** (aylık, ayın son hafta sonu): hisse yalnız izinli bir kümeden alınır (§4.2).
3. **Bilanço filtresi** (yalnız eleme). Üçü birden sağlanmalı:
   - (a) Son **2** çeyrekte EPS beklentiyi aştı. Bu, "earnings streak" sinyalinin sadeleştirilmiş hâli: Loh-Warachka, 2010 sonrası likit evrende uzun-kısa **%0,37/ay, t=2,6** (KEN §4; TEST §6.2).
   - (b) Son çeyrekte gelir beklentiyi aştı. RevenueSurprise likit evrende %0,26/ay, t≈1,9 (KEN §4).
   - (c) İçinde bulunulan mali yılın konsensüs EPS'i bugün 90 gün öncesinden düşük değil. REV6'nın 90 günlük vekili: likit evrende %0,43/ay, t=2,25 (KEN §4). Kaynak: Yahoo Finance "Analysis" sekmesi, "EPS Trend" satırı (bugün / 90 gün önce).
   - (d) Son bilanço sonrası 3 günlük getiri ≥ SPY'ninki. AnnouncementReturn, likit evrende %0,24/ay (KEN §4).
   - Sürpriz verisi için şirketin Nasdaq.com "Earnings" sayfası (son 4 çeyrek).
   - **Dürüst not:** Bu sinyallerin uzun-yalnız üst portföyü 2010–25'te VW piyasayı **geçmedi**: EarningsStreak +%0,7/yıl, AnnouncementReturn −%1,4/yıl. Getirinin çoğu kısa bacakta ve küçük hissede (TEST §0.8, §6.4). Filtrenin işi alfa üretmek değil, **kötü kuyruğu dışarıda bırakmak**. Beklenen katkı seçime yılda ~0 ile +2 puan, boyut-nötr t=1,3–2,7 (TEST §6.4).
4. **Kurulum şartları** (işlem kartına yazılır):
   - En az 10 seanslık (2–8 hafta) baz ya da sıkışma; baz derinliği ≤ %15.
   - Pivot = bazın tepesi. Fiyat pivotun en çok %5 altında.
   - Yapısal stop (son daralmanın dibinin %0,1 altı) ile pivot arası mesafe **0,75–2,0 × ATR14 aralığında ve ≤ %8**. Aralık dışındaysa işlem yok. Gerekçe: ≤1 ATR / %7–10 kuralı (PROF §1.3 madde 3), ama kapanış bazlı 1 ATR'nin kötü sonuç vermesi (VP A12) nedeniyle 2 ATR'ye kadar esneme.
   - Önümüzdeki **10 seans** içinde bilanço yok. Earnings Whispers / şirket IR'den teyit.
   - Son 3 ayda RS'te +%40'lık dikey sıçrama varsa kovalanmaz. 1–3 ay sonra medyan −%4/−%6 (DLG §0.5).

**Giriş (gün içi ekran yok):**
- Emir: **Buy STOP LIMIT, TIF=DAY, yalnız normal seans** (Outside RTH kapalı). Stop = pivot + 0,10 $ (≤ 50 $ hisselerde + 0,05 $). Limit = stop × 1,01. Hiçbir koşulda limit, stop + 0,30 × ATR14'ü aşmaz.
- Yerleştirme saati: **16:45–17:15 TSİ.** Makro veri günlerinde (CPI, PPI, NFP 16:30) 16:45'ten önce emir yok.
- Dolmazsa: Emir gün sonunda düşer. Ertesi gün kurulum geçerliyse yeniden yerleştirilir. Fiyat pivotun %5'ten fazla üstünde kapanmışsa (IBD alım bölgesi, PROF §1.1) setup iptal edilir; kovalanmaz. Kaçan sinyal günlüğe "kaçan" olarak yazılır.
- Gerekçe: Momentum kârının çoğu overnight oluşuyor (Lou-Polk-Skouras, KEN §3). Gün içi kovalamak yerine önceden yerleşen emir ve geceyi taşıyan pozisyon tercih ediliyor.

**Boyut:**
- Adet = ⌊(E × risk%) / (giriş − stop)⌋.
- Ardından üç tavan kontrol edilir:
  - (i) Pozisyon ≤ E'nin %20'si (Kullamägi'nin gece tavanı %30; PROF §3.1).
  - (ii) Gap-ayarlı risk = adet × max(giriş − stop, 1,5 × ATR14) ≤ 1,5 × (E × risk%) (PROF §3.5 madde 5).
  - (iii) Küme ve toplam ısı tavanları (§5).
- Risk%: Faz 1'de %0,25, Faz 2'de %0,50, Faz 3'te %0,75 (en çok %1). §7'ye bakın.

**Stop:**
- Dolumdan hemen sonra **GTC Sell STOP** (piyasa), yapısal stop seviyesine, yalnız normal seans.
- Stop asla aşağı çekilmez.
- Gap riski: stop gap'te kayar. Bu yüzden gap-ayarlı ısı kullanılıyor ve bilanço kuralı var.

**Kâr alma ve trail:**
1. Dolumdan hemen sonra pozisyonun **1/3'ü** için **GTC Sell LIMIT** girilir: giriş + 2R.
2. 5. seans kapanışında kısmi satış dolmadıysa ve kâr ≥ +1R ise, 1/3 ertesi gün açılışta satılır. IBKR'de MOO (TIF=OPG); Midas'ta seans öncesi girilen piyasa emri.
3. Kısmi satış gerçekleşince GTC stop **başabaşa** çekilir.
4. Kalan 2/3 trail edilir. Hisse 20 günlük ortalama günlük aralığı (ADR%) ≥ %4 ise **10 GHO**, değilse **20 GHO**. Kapanış bu ortalamanın altındaysa ertesi açılışta çıkılır. Sinyal sabah 08:00–12:00 TSİ arasında kapanış verisiyle kontrol edilir, emir 17:15'ten önce girilir.
- Gerekçe: 3–5 günde 1/3–1/2 satış ve 10/20 GHO ile kapanış bazlı trail (PROF §1.1 Kullamägi, §1.3 madde 7–8; PROF §3.5 madde 9).

**Bilanço:**
- Açık pozisyonun bilançosu yaklaşıyorsa, açıklamadan önceki son seansın açılışında pozisyon kapatılır. AMC açıklamada aynı günün açılışı, BMO açıklamada önceki günün açılışı.
- İstisna: kısmi satış yapılmış ve kâr ≥ +2R ise kalan taşınabilir. Şart: 2 × implied move büyüklüğünde bir gap'in kaybı ≤ 1R olacak boyuta indirilmesi ("earnings size"; PROF §1.3 madde 9, §3.5 madde 5).

**Piramit (yalnız Faz 2+ ve YEŞİL rejim):**
- Pozisyon ≥ +1,5R iken hisse yükselen 10/20 GHO'ya geri çekilip yeni bir sıkışma yaparsa, sıkışma tepesine buy-stop-limit ile **bir kez** eklenir.
- Ek boyut = ilk riskin %50'si.
- Ekleme sonrası tüm pozisyonun stopa kadar toplam riski ilk 1R'yi geçmez; gerekirse ilk lotun stopu yükseltilir.
- Kaybedene ekleme yok (PROF §1.3 madde 6, §1.1 IBD %50/30/20).

**Dürüst beklenti (S1):**
- İsabet %25–40; ortalama kazanç 2–3,5R; ortalama kayıp −1,0 ile −1,2R (gap'ler nedeniyle).
- E[R] aralığı **−0,2R ile +0,4R**. Öznel merkez +0,1 ile +0,2R [Ö]. Gerekçe: gün içi giriş (ORH) ve günün dibine stop çıkarıldı; kapanış bazlı varyantlar daha zayıf (VP A12, VP §3.8).
- Yılda 40–70 işlem.
- Ardışık kayıp serisi normal: %30 isabette 200 işlemde ≥10 ardışık kayıp olasılığı %84, ≥15 olasılığı %24 (KIM §5.3; VA #37).

### 2.2 S2: Fırsatçı insider küme alımları (uydu; yılda 5–15 işlem)

**Kanıt:**
- Cohen-Malloy-Pomorski: rutin olmayan insider alımlarından kurulan VW portföy **aylık 82 bp** anormal getiri, 1986–2007. Rutin işlemlerin bilgisi ≈0. Yayın sonrası bağımsız test yok (VA #26; KEN §6; SEY §2.3).
- Küme alımları: sonraki 21 günde ~%3,8, tekil alımda %2 (Alldredge-Blank 1986–2016; KEN §6). **Doğrulayıcı bu rakamı teyit etmedi.**
- Etki küçük ve orta ölçekli firmalarda yoğun (KEN §6, [H]).

**Sinyal (Form 4, SEC EDGAR, ücretsiz):**
- **≥3 farklı insider**, işlem kodu **P** (açık piyasa alımı), 10 işlem günü içinde. Toplam ≥ 300 bin $. En az biri CEO, CFO, Chair ya da President.
- **Fırsatçı şartı:** Son 3 yılın her birinde aynı takvim ayında işlem yapmış insider'lar sayılmaz (rutin tanımı, KEN §6).
- **Hariç:**
  - Yalnız %10+ sahiplerden (fonlardan) oluşan kümeler.
  - Halka arz veya ikincil arza katılım alımları (Form 4 "Remarks" ve dipnotları).
  - 10b5-1 planlı alımlar (bilgi değeri ≈0; KEN §6).
  - Fiyatı <5 $, piyasa değeri <300 mn $ ya da 20 günlük ortalama dolar hacmi <5 mn $ olanlar.
  - Önümüzdeki 5 seansta bilançosu olanlar.
- Kaynak: Tarama için openinsider.com "Cluster Buys" (ikincil, Form 4 türevi; 06.11'de 503 verdi, erişim teyit edilmeli). **Her sinyal EDGAR'daki Form 4 Tablo I'den teyit edilir.**

**Giriş:** 3. insider'ın Form 4'ü kamuya açıldıktan sonraki ilk seans. **Buy LIMIT, DAY**, limit = önceki kapanış × 1,015, 16:45–17:15 TSİ arasında girilir. Açılış önceki kapanışın %5'ten fazla üstünde olursa emir dolmayacak şekilde ayarlıdır; işlem yapılmaz.

**Stop ve boyut:**
- GTC Sell STOP, giriş − 2 × ATR14. Bu mesafe %12'yi aşıyorsa işlem yok.
- Risk%: Faz 1'de %0,25, Faz 2+'da %0,5.
- Pozisyon ≤ E'nin %10'u. 1 mn $'lık hesapta pozisyon ≤ 20 günlük ortalama dolar hacminin %1'i.

**Çıkış:**
- **21. seansın kapanışından sonra**, 22. seansın açılışında satış (21 günlük ufuk, KEN §6).
- Uzatma: 21. gün kapanışı 20 GHO'nun üstünde ve kâr ≥ +1R ise kalan pozisyon 20 GHO kapanış kuralıyla en çok 63 seansa kadar taşınır.
- Kısmi satış ve piramit yok.

**Rejim:** Her rejimde açık. KIRMIZI'da en çok 2 açık S2 pozisyonu.

**Dürüst beklenti:** Yayın sonrası tipik çürüme %35–58 (VA #19). Bu, 21 günde +%1–2 anormal getiri demek. İsabet ~%50–55. E[R] **−0,1R ile +0,25R**. Faz 1 boyutunda E'ye katkısı yılda ~0 ile +%0,5. Bu kol daha çok **ölçüm** için: kenar yaşıyorsa 30–50 olayda görünür.

### 2.3 S3: VIX panik çözülme penceresi (uydu; yılda 1–3 olay)

**Kanıt:**
- Nagel (2012): kısa vadeli reversal getirisi likidite sağlamanın bedeli ve VIX ile artıyor. Önceki ay sonu VIX>25 olan aylarda STR 2010–26'da +%0,55/ay (n=29), diğer aylarda −%0,08 (KEN §5; SEY §2.3).
- Uyarı: Ekim ay sonu VIX'i 19,42 idi (Cboe CSV). Bu yüzden Nagel'in koşulu **Kasım için oluşmadı.**

**Kendi mini testim (C-TEST, 1990–2026/09, CRSP VW piyasa toplam getirisi, sinyal t kapanışı, getiri t+1'den):**

| Tanım | n | 20 gün fazla getiri: ort / medyan / pozitif | 40 gün fazla getiri: ort / medyan / pozitif / p10 | Okuma |
|---|---|---|---|---|
| A) İlk VIX>25 kapanışı (öncesinde 40 gün ≤25) | 30 | **−%0,33** / +%1,73 / %63 (t=−0,24) | +%0,35 / +%3,00 / %63 / −%10,5 | **Kenar yok.** Koşulsuz 20 gün ortalaması +%0,73. 2020-02-24 olayı −%31. "Spike'ta al" kuralı reddedildi |
| B) Panik çözülmesi: son 10 seansta VIX>25 **ve** VIX/VIX3M>1 olmuş; bugün VIX/VIX3M ilk kez **<0,95**. Olaylar arası ≥40 seans | 25 (2009–26) | +%1,29 / +%2,20 / %72 (t=1,51) | **+%3,94 / +%4,94 / %80 / −%2,07 (t=3,69)** | Koşulsuz 40 gün ortalaması ~+%2,1 (2010+). Fark ~+1,8 puan |

Bu test **örneklem içi**. İki tanım denendi; dönem tek ve çoğunlukla boğa (2009–26), VIX3M verisi ancak 2009'dan başlıyor. Planda B'nin fazla getirisi **%50 tıraşlanarak** kullanılıyor: olay başına ~+%1 fazla, ~+%3 toplam.

**Kural:**
- **Kurulma:** VIX kapanışı >25 **ve** VIX/VIX3M >1,00 olan herhangi bir gün. S3 sonraki 10 seans için "kurulu" sayılır; yeni böyle bir gün pencereyi yeniler.
- **Tetik:** Kuruluyken VIX/VIX3M kapanışının ilk kez **<0,95** olması (TradingView `CBOE:VIX/CBOE:VIX3M`, HAZ §5d).
- **Giriş:** Ertesi seans. **SPY Buy LIMIT, DAY**, limit = tetik günü SPY kapanışı × 1,007, 16:45–17:15 TSİ arasında. Dolmazsa ertesi gün aynı kuralla bir kez daha denenir; sonra iptal.
- **Araç uyarısı:** IBKR hesabı IBIE'ye bağlanır ve PRIIPs nedeniyle ABD ETF'i engellenirse yedek araç CSPX (iShares Core S&P 500 UCITS, LSE; 10:00–18:30 TSİ). Yedek **test edilmedi** (HAZ §1.2).
- **Boyut:**
  - Stop mesafesi = max(%4, 2,5 × ATR14(SPY)).
  - Risk: Faz 1'de E'nin %0,5'i, Faz 2+'da %1,0'ı.
  - Pozisyon ≤ E'nin %25'i.
  - Tetik günü S&P 200 GHO'nun altındaysa boyut yarıya iner. Gerekçe: A tanımında 200 GHO altındaki olayların 40 günlük ortalaması −%1,36.
- **Çıkış:** **40. seans** kapanışından sonra, ertesi açılışta (MOO). Ya da GTC stop. Kısmi satış yok, uzatma yok.
- **Ayrıca rejim girdisi:** S3 tetiği, KIRMIZI'dan çıkışın bir parçası (§3).

**Dürüst beklenti:** Olay başına pozisyonda +%1 ile +%4. İsabet %65–80. Olay başına ≈ +0,25R ile +0,5R. E'ye katkısı olay başına +%0,1–0,5, yılda 1–3 olay. Ana değeri getiri değil: S1'i doğru zamanda yeniden açmak.

**Bugünkü durum:** 05.11 kapanışında VIX 28,18 ve oran 1,10. **S3 kurulu**; pencere en az 19.11'e kadar açık. Tetik için VIX3M ~25,5'te kalırsa VIX'in ~24,3'ün altında kapanması gerekiyor.

### 2.4 Opsiyon: IV yüksekken alım yok

**Kanıt:**
- Opsiyon alıcısı ortalamada kaybediyor. Zero-beta ATM straddle ≈ −%3/hafta; yüksek çarpıklıklı 7 günlük call'lar −%35/hafta (VP A6).
- Retail ~2,1 mlr $ kaybetti (VP A7). Retail spread'i ortalama %12,6 (VA #10).
- Opsiyon yalnız var olan bir kenarı, IV ucuzken büyütür (PROF §0.6, §2.3).

**Kural:** Opsiyon alımına **yalnız aşağıdaki şartların tümü** sağlanırsa izin var:
1. Faz ≥2 (§7).
2. Rejim YEŞİL.
3. VIX <20 ve VIX/VIX3M <0,90.
4. Hissenin IV30'u 52 haftalık aralığının alt %30'unda ve IV30 ≤ HV20 (Goyal-Saretto yönü; VP A8).
5. Opsiyonun ömründe bilanço yok.
6. 45–90 gün vade, delta 0,55–0,70.
7. ATM spread'i ≤ mid'in %5'i, OI ≥ 500.
8. Ödenen prim = riskin tamamı, ≤ 1R; ısı tavanına sayılır.
9. Emir mid'den limit; piyasa emri yok (PROF §2.4).

Debit spread, straddle ve opsiyon satışı bu planda yok. Kenar kanıtı değil, risk şekillendirme (KEN §12 madde 7). Midas'ta zaten yalnız call/put alımı var (HAZ §1.2).

**Bugün:** VIX 28,2, oran 1,10 → **opsiyon tamamen kapalı.**

### 2.5 Emir tipi özeti (gün içi ekran olmadan)

| Amaç | Emir | TIF / seans | Ne zaman (TSİ) | Not |
|---|---|---|---|---|
| S1 giriş | Buy STOP LIMIT (stop = pivot + 0,10 $, limit = stop × 1,01) | DAY, yalnız RTH | 16:45–17:15 | Makro veri günlerinde 16:45'ten sonra |
| S2 / S3 giriş | Buy LIMIT (önceki kapanış × 1,015 / × 1,007) | DAY | 16:45–17:15 | |
| İlk stop | Sell STOP (piyasa) | **GTC**, yalnız RTH | Dolumdan hemen sonra, aynı gece veya ertesi sabah | IBKR'de giriş emrine "attached" bracket olarak bağlanabilir |
| 1/3 kâr | Sell LIMIT, giriş + 2R | GTC | Dolumdan hemen sonra | OCA (biri dolunca diğer miktar güncellenir) |
| Trail çıkışı / 40 ve 21 seans çıkışı | MOO (IBKR TIF=OPG) ya da seans öncesi piyasa emri | Açılış | 12:00–17:15 | Sinyal önceki kapanış verisinden, sabah kontrol |
| Bilanço öncesi çıkış | MOO | Açılış | Açıklamadan önceki son seans | |

- **İlk işlemden önce** her emir tipi 1 adetle test edilir: GTC stop gerçekten GTC mi, stop-limit RTH dışında tetikleniyor mu, MOO destekleniyor mu?
- **Midas'ta** stop-limit, GTC stop ve MOO desteği kamuya açık sayfalarda yok (HAZ §1.2, §7). Desteklemiyorsa Midas yalnız S3 (SPY limit) ve S2 limit girişleri için kullanılır; S1 IBKR'ye kadar bekler.

---

## 3. Piyasa rejimi anahtarı: eşikler ve bugünkü okuma

### 3.1 Girdiler (her ABD kapanışından sonra; sabah 08:00–12:00 TSİ arası kontrol)

| Kod | Gösterge | Kaynak |
|---|---|---|
| G1 | S&P 500 kapanışı ile 50 ve 200 günlük basit ortalama | FRED SP500 / TradingView `SP:SPX` |
| G2 | Nasdaq-100'ün 10 ve 20 günlük basit ortalaması ve eğimleri | `NASDAQ:NDX` |
| G3 | VIX/VIX3M kapanış oranı | `CBOE:VIX/CBOE:VIX3M` |
| G4 | S5FI (S&P'de 50 GHO üstü hisse yüzdesi) ve S5TH (200 GHO üstü) | `INDEX:S5FI`, `INDEX:S5TH` |
| G5 | **Takip günü (FTD):** düzeltme dibinden sonraki ralli denemesinin ≥4. günü, S&P veya NDX ≥ +%1,5 kapanış, hacim bir önceki günden yüksek | HAZ §3; PROF §1.1 IBD |

### 3.2 Durumlar

| Durum | Koşul | S1 yeni giriş | S2 | S3 | Toplam ısı tavanı | Brüt maruziyet tavanı |
|---|---|---|---|---|---|---|
| **KIRMIZI** | Aşağıdakilerden **herhangi biri**: (a) VIX/VIX3M ≥ 1,00 kapanış. (b) S&P 2 kapanış üst üste 200 GHO altında. (c) S5FI <50 **ve** S5TH <60 | **Yok.** Yalnız izleme listesi | Açık, en çok 2 pozisyon | Kurulu / tetiklenebilir | **%1** | E'nin %25'i |
| **SARI** | KIRMIZI değil **ve** şunlardan biri: NDX 10 < 20 GHO, S&P < 50 GHO, ya da düzeltme dibinden beri FTD yok | **Pilot:** Faz risk%'i, günde en çok 2 yeni giriş, yalnız ilk 3 izinli kümeden | Açık | Açık | **%2** (Faz 1) / %3 (Faz 2+) | %50 |
| **YEŞİL** | S&P > 50 ve > 200 GHO; NDX 10 > 20 GHO ve ikisi yükseliyor; VIX/VIX3M <0,95; FTD gerçekleşti ve FTD gününün dibi kapanışta kırılmadı; S5FI ≥50 | Tam faz boyutu; Faz 2+'da piramit | Açık | Açık | **%3 / %5 / %6** (Faz 1 / 2 / 3; %6 yalnız yıl içi kâr yastığı ≥%10 ise) | %100, **margin yok** |

**Geçiş kuralları:**
- KIRMIZI → SARI için iki şart birlikte: VIX/VIX3M 2 kapanış üst üste <1,00 **ve** S&P 200 GHO'nun üstünde.
- YEŞİL → SARI: NDX 10<20 GHO'yu 2 kapanış korursa ya da S&P FTD gününün dibinin altında kapanırsa.
- Durum değiştiğinde açık pozisyonlar zorla kapatılmaz. Yalnız yeni giriş kuralı değişir. Isı tavanı düştüyse yeni giriş yapılmaz; mevcutlar kendi stop ve trail kurallarıyla küçülür.

**Kanıt:**
- Rejim filtresi en kritik hayatta kalma bileşeni. Kullamägi 2022'de filtresine uymadı ve −%57 yaptı; FFTY 2022'de −%51 (KIM §5.1; VA #16–17).
- Momentum çöküşleri panik sonrası toparlanmalarda geliyor; dinamik ölçekleme Sharpe'ı ~2 katına çıkarıyor (KEN §3; Daniel-Moskowitz VA #27).
- Drawdown kuralı yalnız performans rejime bağlıysa değer katıyor; birincil araç rejim filtresi (PROF §3.3).
- 10/20 kuralı, IBD düzeltme okuması ve pilot ≤%0,25 / ısı ≤%2 (PROF §1.4).
- VIX/VIX3M <1, S5FI >50 ve FTD şartları (HAZ §3, §5d).
- Endeks 50 GHO altında ve VIX>25 iken brütü yarıya indir (PRA §3.6).

**Belirsizlik:** Bu eşiklerin bu birleşimi hiç test edilmedi. Bileşenlerin kanıtı var, ama birleşimin yanlış alarm oranı bilinmiyor. Dürüst beklenti: yanlış başlangıçlar sık olacak, rejim filtresinin faydası çöküş yıllarında görünecek.

### 3.3 Bugün ne diyor? (05.11 kapanışı; C-TEST `ma.py`, HAZ §3)

| Girdi | Değer | Durum |
|---|---|---|
| S&P 500 | 7.353,73. 50 GHO 7.686,5 (**%−4,3**); 200 GHO 7.322,7 (**%+0,4**; 200 GHO bir ay önce 7.241, yükseliyor). 10/20 GHO 7.622 / 7.680 | 200 GHO'nun hemen üstünde, 50'nin altında |
| Nasdaq-100 | 26.629,8. 10 GHO 28.672 < 20 GHO 29.286 < 50 GHO 29.686; 200 GHO 27.977 (**%−4,8**). 10<20 durumu 19.10'dan beri | Kırık |
| VIX / VIX3M | 28,18 / 25,55 = **1,10** (4.11'de VIX 16,61) | **KIRMIZI tetikleyici** |
| S5FI / S5TH | 62,5 / 66,1 (TradingView önbelleği, zaman damgası karışık; HAZ §3) | Henüz kırmızı değil; teyit edilmeli |
| FTD | Yok; ralli denemesi başlamadı | — |
| **Sonuç** | **KIRMIZI** (koşul a). S3 kurulu. Opsiyon kapalı | |

### 3.4 Haftanın planı

**Cumartesi 07.11 sabahı:** Cuma kapanışı ve NFP sonrası rejimi yeniden oku.
- VIX/VIX3M Cuma <1,00 kapanırsa ve Pazartesi de öyle kalırsa, en erken Pazartesi kapanışında SARI olur; ilk pilot Salı.
- Cuma kapanışında oran <0,95 ise S3 tetiklenmiş olur: Pazartesi SPY girişi, ama yalnız IBKR ya da Midas hesabı fonlanmışsa. Fonlanmamışsa tetik kaçırılır ve günlüğe "kaçan" diye yazılır. Kovalanmaz.

| Gün | Olay (TSİ) | Ne yapılır |
|---|---|---|
| **Pt 09.11** | Bowman 16:40; 3 yıllık tahvil ihalesi 21:00. BMO: CEG, MNDY, NRG. AMC: RKLB, TTWO, HIMS vb. Finviz'e göre BRK-B bilançosu (teyit) | Muhtemelen KIRMIZI: **S1 girişi yok.** Hesap işleri, 1 adetlik emir testleri, izleme listesi, günlük kurulumu. S3 tetiği akşam kapanışta kontrol edilir |
| **Sa 10.11** | **CPI 16:30**; 10 yıllık ihale 21:00; AMC: CRWV | 16:45'ten önce emir yok. CPI sonrası S&P vadelisi ±%1,5'ten fazla oynarsa o gün **yeni giriş yok** (S3 dahil); kapanışta yeniden değerlendirilir |
| **Ça 11.11** | Gaziler Günü: hisse açık, tahvil kapalı. MSCI duyurusu ~00:00 (12.11) | Normal rutin |
| **Pe 12.11** | İşsizlik başvuruları 16:30; 30 yıllık ihale 21:00; **TCMB rezerv verisi** (Perşembe); AMC: **CSCO, AMAT**; BMO: NBIS | **Döviz tahsisi anahtarı** kontrol edilir (§1.3). AI kümesi zaten yasaklı; bilançolar yalnız endeks riski olarak izlenir |
| **Cu 13.11** | **PPI 16:30**; UMich 18:00 | Haftalık gözden geçirme: istatistikler, küme sıralaması, yeni izleme listesi |
| **16–20.11** | **NVDA 17.11 AMC** (çağrı 01:00 TSİ, 18.11; HAZ §2.1'e göre NVIDIA IR kaynaklı; "~19.11" tahmini yerine bu tarih kullanıldı, yine de teyit edin). FOMC tutanakları **18.11 22:00**. WMT 19.11 BMO. **Aylık opsiyon vadesi 20.11** | 17.11'de S1'de yeni giriş yok. 18.11'de 22:00'dan önce yeni giriş yok. Mevcutlar stoplarıyla kalır |
| **26–27.11** | Şükran Günü kapalı; 27.11 erken kapanış (21:00 TSİ) | 25.11'de yeni giriş yok (GSYH, PCE ve Bej Kitap aynı gün) |
| **Ara.** | NFP 04.12; FOMC 09.12 22:00 (artış olasılığı ~%67–70); CPI 10.12; bütçe süresi 11.12 | FOMC günü yeni giriş yok |

---

## 4. Evren ve izleme listesi yöntemi

### 4.1 Küme tanımı ve seçim sırası

1. **Küme:** Aynı anlatıya bağlı ya da 60 günlük getiri korelasyonu ≥0,6 olan hisseler tek kümedir (PROF §3.5 madde 2).
   - 2026'da yarı iletken, donanım/bellek, elektrik ekipmanı/güç ve mühendislik-inşaat **tek küme**. Chips–ElcEq korelasyonu 0,72, piyasadan arındırılmış 0,43 (PROF §3.2; VP A14 rakamı doğrulamadı ama yönü akla yatkın buldu).
   - Aynı kümede 5 pozisyon ≈ 1,3 bağımsız bahis (PROF §3.2; SEY §3.6).
2. **Küme izni (aylık, ayın son hafta sonu).** Küme, aşağıdakilerden biri sağlanırsa izinli:
   - (a) Temsilci ETF'i HAZ §5c skorunda **ilk 5**'te ve fiyatı 50 GHO'nun üstünde. Skor = 0,2 × (1 ay − SPY) + 0,4 × (3 ay − SPY) + 0,4 × (6 ay − SPY).
   - (b) Finviz endüstri grubu 3 aylık performansta ilk %20'de.
   - **Dürüst not:** Sektör momentumu 2010 sonrası risk-ayarlı olarak piyasa düzeyinde (VA §2.2; VD U4, U7). Bu adım bir kenar değil, kırık kümelerden uzak durma disiplini (TEST §9.3; DLG §0.4). Tema seçimi aylık, zamanlama tema içindeki hisse kurallarıyla yapılır (DLG §0.4).
3. **Hisse seçimi (haftalık):**
   - İzinli kümelerde §2.1'in tarama, bilanço ve kurulum şartlarını geçenler `RS raw`'a göre sıralanır.
   - **Kümede ilk 3–5 isim** izleme listesine alınır.
   - Faz 1'de kümede aynı anda en çok **3** açık S1 pozisyonu (küme ısısı ≤ %0,75).
4. **Yasaklı kümeler (Kasım 2026):**
   - AI donanım bloğu: yarı iletken, bellek, donanım, güç/elektrik ekipmanı, veri merkezi inşaatı. Kırık; Hardware canlı bir GSY olayı, tarihsel çöküş olasılığı %42–53 (DLG §0.7; HAZ §4).
   - Nükleer/uranyum, kuantum, neocloud/kripto madencileri, drone/uzay. Balon sonrası (DLG §0.8).
   - Enerji: lider kırılması, 50 GHO altında, İran anlaşması riski (HAZ §4).
   - Altın madencileri (zirveden −%11/−%27) ve savunma (ITA 3 ayda −%19).
   - Bu kümeler için yeniden giriş şartı: küme RS'i yeni 12 aylık zirve yapacak (DLG §7.4).

### 4.2 Bugünkü adaylar (HAZ §4 listesi, 5.11 kapanışı; öneri değil)

Rejim KIRMIZI olduğu için **bugün hiçbiri alınamaz.** Tablo, SARI'ya geçişte hangisinin tetik listesine girebileceğini gösteriyor. "Kontrol" sütunundaki şartlar (TT, RS çizgisi, baz, bilanço sürprizi, 90 günlük revizyon) bu dosyada **doğrulanmadı**, çünkü hisse bazında günlük veri yok. Cumartesi grafikte ve sürpriz sayfalarında kontrol edilmeli.

| Küme (izin gerekçesi) | Aday (52H'ye uzaklık) | Durum |
|---|---|---|
| **Medtech / cihaz** (IHI skor #2; finviz sağlık grupları önde) | BDX (−%1,1; 5.11 bilanço), EW (−%3,2; 4.11 bilanço), TMO (−%4,8), GEHC (−%6,7) | **Aday.** Bilanço filtresi kontrol edilecek. BDX ve EW yeni raporladı; baz oluşumu için 2+ hafta gerekebilir |
| | MDT (−%2,7) | **Bekle:** Kasım ortası/sonu bilançosu (teyit). Bilanço sonrası yeniden değerlendir |
| | IDXX (−%12,9) | **Elendi:** zirveye uzaklık >%10. EP kurulumu, ama bu planda EP kolu yok |
| **İlaç / sağlık hizmeti** (XLV #1, PPH #3, IHF #5). Medtech ile **ilişkili küme**, ortak tavan §5 | EHC (−%1,5), RPRX (−%3,6), LLY (−%7,1), REGN (−%9,8; sınırda) | **Aday** (LLY ve REGN zirveye uzak; öncelik düşük) |
| | CNC (−%5,9; 4.11'de tek günde +%12,6) | **Bekle:** dikey hareket sonrası baz gerek |
| **Borsalar / finansal veri** (finviz 3 ay +%12,4) | TW (−%1,1), CME (−%4,8), CBOE (−%4,9; 1 ayda +%25,4), +VRSK, FDS (HAZ §5b listesi) | **Aday.** CBOE'de dikey koşu sonrası baz bekle |
| **Sigorta / broker**. Borsalarla **ilişkili küme** (finansal) | MRSH (−%2,1), AJG (−%2,2), ACGL (−%2,7), +AON, RLI | **Aday** |
| | BRK-B (−%3,7) | **Bekle:** finviz'e göre 9.11 bilanço (teyit) |
| **Temel tüketim** (XLP #6; ilk 5 dışında, finviz indirim mağazası güçlü) | KDP (−%4,0; 3.11 bilanço) | Sınırda izin; aday |
| | BJ (−%1,8) | **Bekle:** 20.11 BMO bilanço |
| **Atık / su** (finviz atık yönetimi 1 ayda +%12,1) | AWK (−%0,8), RSG (−%2,0), VLTO (−%2,7) | **Aday.** Düşük oynaklık; ATR şartını (stop ≥ 0,75 ATR) kontrol et |
| **Konaklama** (finviz 3 ay +%17,5) | HLT (−%3,1), MAR (−%3,7; 2.11 bilanço) | **Aday** |
| **Dikey yazılım** (bilanço sonrası kırılımlar; 2026'da AI bloğuna negatif artık korelasyon, ama 2022'de herkes birlikte düştü; PROF §3.2) | ROP (−%3,2; 1 ayda +%36,9), MANH (−%3,2), GEN (−%3,3) | **Aday** ama dikey koşu var; baz şart |
| | U (−%2,3; haftada +%35) | **Bekle:** dikey; baz yok |
| **REIT (kule / depolama)**: faize duyarlı, 10 yıllık %4,84–4,90 | PSA (−%1,6), CCI (−%4,3; 1 ayda +%31,8) | Küme izni sınırda; düşük öncelik |
| Tekil | SN, HAS, EBAY, AAPL | Her biri ayrı küme sayılmaz; "diğer tüketim" tek küme |

**S2 adayı:** Bu dosyada güncel insider küme listesi **yok.** openinsider 06.11'de 503 verdi; veri uydurulmadı. İlk tarama Pazartesi sabahı 10:00–12:00 TSİ (§9).

---

## 5. Risk limitleri

### 5.1 Tablo (E = ABD strateji sermayesi)

| Limit | Faz 1 (ilk 50 işlem) | Faz 2 | Faz 3 | Kaynak |
|---|---|---|---|---|
| İşlem başı risk (S1, S2) | **%0,25** | %0,50 | %0,75 (en çok %1; yıl içi kâr yastığı ≥%10 ise) | PROF §3.5 madde 1; KIM §5.3 (risk %1'i aşınca bu yapı kırılıyor) |
| S3 işlem riski | %0,5 | %1,0 | %1,0 | §2.3 |
| Tek pozisyon (brüt) | ≤%20 (S2 ≤%10; S3 ≤%25) | aynı | ≤%25 | PROF §3.1 |
| **Küme ısısı** | ≤%0,75 (3 pozisyon) | ≤%1,5 | ≤%1,5 | Çapa; PROF §3.5 madde 3 |
| İlişkili kümeler toplamı (aynı sektör: sağlık, finansal) | ≤%1,25 | ≤%2,5 | ≤%2,5 | PROF §3.1 (Turtle 6/10/12 dönüşümü) |
| **Toplam açık risk** (gap-ayarlı) | KIRMIZI %1 / SARI %2 / YEŞİL %3 | %1 / %3 / %5 | %1 / %3 / %6 | Çapa 3/5/6; PROF §3.5 madde 4 |
| **Aylık devre kesici:** ayın gerçekleşen zararı + açık risk | ≥ min(%6, 12R) = **%3** → ay sonuna kadar yeni işlem yok | ≥%6 | ≥%6 | Elder %6 (PROF §3.1, §3.5 madde 8) |
| Margin / kaldıraç | **Yok** | Yok | Yalnız YEŞİL rejimde ≤1,3x (faiz %5,38, TR'de indirilemez) | VC #16; PRA §2.1 |

### 5.2 Düşüş merdiveni (E'nin zirvesinden, kapanış değeriyle)

| Zirveden düşüş | Eylem | Gerekçe |
|---|---|---|
| **−%4** | Risk% × 0,5 (en az %0,125). Piramit yok | %0,25 riskte bu 16R. ≥15'li kayıp serisinin olasılığı %24 (KIM §5.3); "normal kötü seri" sınırı |
| **−%7** | Yalnız S2, S3 ve en güçlü 2 kümedeki S1 kurulumları. Toplam ısı ≤%1,5 | PROF §3.5 madde 7 (−%10 kademesinin küçük risk için ölçeklenmiş hâli) |
| **−%10** | 10 seans yeni işlem yok. Tüm işlemlerin yazılı incelemesi | PROF §3.5 madde 7 |
| **−%15** | **Plan durur.** Pozisyonlar kapanır, E USD nakde ya da TL'ye döner. Yeniden başlamak için yeni hipotez kartı ve sıfırdan Faz 1 gerekir | SEY §5.2 madde 1 ve 8 |
| Geri yükleme | Kaybın yarısı geri gelince bir kademe yukarı | PROF §3.5 madde 7 |

**Değer ve bedel:** Merdiven %5 olasılıklı kötü MDD'yi yaklaşık yarıya indiriyor, medyan getiriden ~17 puan alıyor. Fayda yalnız rejime bağlı performansta oluşuyor (PROF §3.3, Model B).

### 5.3 Örnek hesaplar: 50 bin, 250 bin, 1 milyon $

Örnek S1 işlemi: hisse 100 $, ATR14 3,20 $, yapısal stop 94 $ (−%6, 1,9 ATR; şartı geçiyor). Gap-ayarlı mesafe = max(6; 1,5 × 3,2 = 4,8) = 6 $.

| Kalem | E = 50.000 $ | E = 250.000 $ | E = 1.000.000 $ |
|---|---|---|---|
| Faz 1'de 1R (%0,25) | 125 $ | 625 $ | 2.500 $ |
| Adet / pozisyon / E'nin yüzdesi | 20 adet / 2.000 $ / %4,0 | 104 / 10.400 $ / %4,2 | 416 / 41.600 $ / %4,2 |
| IBKR Pro Fixed (0,005 $/adet, en az 1 $) gidiş-dönüş | 2 $ = 0,016R | 2 $ = 0,003R | 4,16 $ = 0,002R |
| Midas (1,5 $/işlem) gidiş-dönüş | 3 $ = 0,024R | 3 $ = 0,005R | 3 $ = 0,001R |
| İş TMI (%0,25/yön) gidiş-dönüş | 10 $ = **0,08R** | 52 $ = **0,083R** | 208 $ = **0,083R** |
| Faz 2'de 1R (%0,5) | 250 $ | 1.250 $ | 5.000 $ |
| Küme ısısı tavanı, Faz 1 (%0,75) | 375 $ | 1.875 $ | 7.500 $ |
| Toplam ısı, Faz 1, KIRMIZI / SARI / YEŞİL | 500 / 1.000 / 1.500 $ | 2.500 / 5.000 / 7.500 $ | 10.000 / 20.000 / 30.000 $ |
| Aylık devre kesici, Faz 1 (%3) | 1.500 $ | 7.500 $ | 30.000 $ |
| Merdiven −%4 / −%10 / −%15 | 2.000 / 5.000 / 7.500 $ | 10.000 / 25.000 / 37.500 $ | 40.000 / 100.000 / 150.000 $ |
| S3 pozisyonu (risk %0,5, stop %4 → E'nin %12,5'i) | 6.250 $ | 31.250 $ | 125.000 $ |
| S2 pozisyonu (risk %0,25, stop %10 → %2,5) | 1.250 $ | 6.250 $ | 25.000 $ (20 günlük ortalama dolar hacmi ≥5 mn $ ise ≤ %0,5'i) |
| Gereken vergi öncesi USD getirisi, h=%31–37, d=%20, u=0,3 (§1.2) | %12,7–19,5 | %15,6–23,3 | %17,5–25,9 |
| Hayalet vergi (R=0, u=0,3, d=%20) | ~22,5 bin TL (E'nin %0,9'u) | ~165 bin TL (%1,3) | ~934 bin TL (%1,9) |
| ABD tereke vergisi riski (>60 bin $ ABD varlığı) | Sınırda | **Var** | **Var** |

- **Yüzdesel komisyon her boyutta işlem başına ~0,08–0,10R yiyor.** Bu, +0,2–0,3R'lik bir kenarın **%25–50'si**. Ana platform IBKR; küçük hesapta Midas kabul edilebilir.
- Garanti'nin %0,30 komisyonu ve %0,50 kur ücreti ~0,1R'nin üstünde (HAZ §1.2).
- Stop emirlerinde kayma ölçülmedi. 0,05–0,15 % varsayılıyor (≈0,01–0,025R); günlükte ölçülecek.

---

## 6. Erişim, uygulama, maliyet, vergi ve kayıt

### 6.1 Aracı kurum

| Seçenek | Rolü | Süre | Maliyet | Kısıt |
|---|---|---|---|---|
| **IBKR Pro (margin hesabı tipi, kaldıraçsız kullanım)** | **Ana platform.** GTC, stop-limit, bracket/OCA, MOO, koşullu emir; IV verisi | Açılış 1–3 iş günü + SWIFT 1–2 gün → ilk işlem gerçekçi olarak **11–13.11** | 0,005 $/adet (en az 1 $); margin %5,38; boş nakit faizi %3,38 | Bağlı olunacak IBKR şirketi (IB LLC / IBIE) doğrulanmadı. IBIE'de ABD ETF'leri PRIIPs ile kısıtlanabilir; başvuruda yazılı teyit alın (HAZ §1.2; VC #16; PRA §1.2) |
| **Midas** | Köprü: küçük E, S2/S3 limit emirleri | Onay 1–2 gün | 1,5 $/işlem; kur makası yayınlanmıyor | Yalnız call/put alımı; spread, yazım ve margin yok. Stop/GTC desteğini 1 adetle test edin (HAZ §1.2) |
| İş TMI / Garanti / Gedik | Önerilmez (S1 için) | Mevcut müşteri için birkaç gün | %0,25 / %0,30 (+%0,5 kur) / lot başı 0,05 $ | Yüzdesel komisyon kenarın %25–50'si (§5.3). Gedik lot bazlı ücreti büyük fiyatlı hissede makul olabilir (teyit) |

- **PDT:** 25 bin $ şartı kaldırıldı. SEC onayı 14.04.2026, yürürlük 04.06.2026. Ancak aracı kurumlar için geçiş 20.10.2027'ye kadar sürüyor (VC #15). Swing planında gün içi işlem yok, yani bağlayıcı değil.
- **Nakit hesap:** free-riding kısıtları sürüyor (VC #15). Margin tipi hesap seçin ama borç kullanmayın.
- **W-8BEN** imzalanmalı; yoksa temettü stopajı %30 (PRA §1.3).

### 6.2 Fonlama ve kur

- TL → USD çevrimi Türk bankasında yapılır, USD SWIFT ile IBKR'ye gönderilir.
- Kambiyo BSMV binde 2 (PRA §2.5; VC "doğrulanamadı"). Banka SWIFT masrafı ayrıca.
- İlk transferden önce bankanın kur makasını ölçün. Midas'ta küçük bir tutarla test edin.
- Boştaki USD **nakit olarak** kalır, T-bill ya da para piyasası ETF'ine **konmaz**. Kur farkı vergisi (§1.2) %3,38 ile %4,03 arasındaki 0,65 puanlık faiz farkından çok daha büyük. Mali müşavirle teyit edin.
- Transfer büyüklüğü: E'nin tamamı. E zaten C'nin %10–15'i.

### 6.3 Günlük ve haftalık rutin (TSİ)

| Saat | İş |
|---|---|
| 08:00–09:00 | Kapanış verileriyle rejim tablosu (§3.1). Dolumlar ve stop olanlar. Trail sinyalleri (10/20 GHO kapanış kuralı). S2/S3 gün sayaçları. Günlüğe kayıt |
| 10:00–12:00 | S2: önceki günün Form 4'leri (EDGAR). Bilanço takvimi (Earnings Whispers). Açık pozisyonların haberleri |
| 12:00–16:30 | Pre-market (12:00–17:30). Emirleri hazırla. Makro veri günlerinde 16:30'u bekle |
| **16:45–17:15** | **Tüm DAY emirleri** girilir, GTC stoplar kontrol edilir. MOO çıkışları 17:15'ten önce girilir |
| 17:30–00:00 | **Ekran yok.** Yalnız aracı kurumun dolum bildirimleri; dolum gelirse aynı gece veya ertesi sabah GTC stop + 2R limit girilir (IBKR'de bracket ile otomatik) |
| Cumartesi | Taramalar (§2.1, HAZ §5). Küme izni. İstatistikler (§7). Ertesi haftanın bilanço riski |
| Ayın son hafta sonu | ETF rotasyon skoru (HAZ §5c), küme izinleri, faz kapısı kontrolü |

### 6.4 Vergi ve kayıt (Türkiye beyanı için)

- **Her işlem için kaydedilecekler:** tarih, adet, USD fiyatı, komisyon, işlem günündeki **TCMB döviz alış kuru**.
  - GİB: alış ve satış bedeli o günlerin kurlarıyla TL'ye çevrilir (VC #10). Kur türünü mali müşavirle teyit edin.
  - TL kazanç/zarar = satış TL − alış TL − komisyonlar TL.
  - Kısmi satışlarda FIFO lot eşleştirmesi (IBKR raporuyla aynı yöntem).
- Yıllık beyan (Mart 2027), ödeme Mart ve Temmuz. Tutar ne olursa olsun beyan edilir; istisna yok (VC #10; PRA §2.1).
- **Zarar devredilmez.** Aralık'ın ilk haftası (01–04.12) bir vergi kontrol noktası. Yıl içi net TL kazancı pozitifse, zaten çıkış sinyali yakın olan zarardaki pozisyonlar kural dışı bekletilmez. Ama **yalnız vergi için çıkış yapılmaz**; kural önceliklidir.
- Endeksleme: elde tutma süresi ~6 ay ve üstünde, Yİ-ÜFE artışı ≥%10 ise (VC #10). S1/S2/S3'te pratikte uygulanmaz.
- Temettü: %20 ABD stopajı. Beyan sınırı 22.000 TL (VC #10, #12).
- Boştaki nakdin faizi menkul sermaye iradı olarak beyana tabi (PRA §4.1).
- **"Ticari kazanç" riski:** sık işlem bu nitelendirmeye yol açabilir; örnek bulunmadı (PRA §2.1). Mali müşavire işlem sıklığını önceden söyleyin.
- **Yıl sonu belgeleri:** IBKR Activity Statement (yıllık, CSV + PDF), 1042-S (temettü stopajı), banka SWIFT dekontları. 5 yıl saklanır.
- **ABD tereke vergisi:** 60 bin $ üstü ABD varlıkları için Form 706-NA (VA #36). 250 bin ve 1 mn $'lık hesaplarda risk gerçek. Avukat veya mali müşavirle görüşün. Boştaki S3 yedeği için UCITS ETF bu riski azaltabilir (teyit edilmedi).

---

## 7. Öldürme kriterleri ve ileriye dönük ölçüm protokolü

### 7.1 Hipotez kartları (işlemden önce yazılır, tarihli, değiştirilemez; SEY §5.3 madde 1)

| Kol | Mekanizma | Beklenen E[R] | İsabet | Kazanç/kayıp | İşlem/yıl | Denenen varyant (N) |
|---|---|---|---|---|---|---|
| S1 | Sağ kuyruk yakalama (Bessembinder %4; VA #29), rejim filtresiyle momentum | +0,1 ile +0,2R (aralık −0,2 ile +0,4R) | %25–40 | 2–3,5 | 40–70 | 1: §2.1 tek kural seti. Değişiklik yeni bir kart sayılır |
| S2 | Bilgi işleme: insider'ın özel bilgisi (SEY §2.3) | 0 ile +0,15R | %50–55 | ~1,2 | 5–15 | 1 |
| S3 | Likidite sağlama / panik primi (Nagel) | +0,25 ile +0,5R | %65–80 | ~1 | 1–3 | **2** (C-TEST A ve B; B seçildi) |

### 7.2 Günlük alanları (her işlem bir satır)

- **Kimlik:** No, kol (S1/S2/S3), küme, ticker, kurulum tipi (baz kırılımı / insider / VIX).
- **Durum:** rejim durumu ve faz giriş anında. Hipotez kartı sürümü.
- **Plan:** sinyal tarihi; planlanan giriş (pivot / limit); emir tipi.
- **Gerçekleşen:** dolum tarihi ve fiyatı; **kayma (bps)** = dolum − planlanan.
- **Risk:** ilk stop; ATR14; stop mesafesi (%, ATR cinsinden); adet; pozisyon (% E); 1R ($); gap-ayarlı risk; giriş sonrası toplam ısı ve küme ısısı.
- **Bilanço:** bir sonraki bilanço tarihi; bilanço filtresinin 4 maddesi (evet/hayır).
- **Seyir:** kısmi satış tarihi ve fiyatı; stopun başabaşa çekildiği tarih; piramit (tarih, fiyat, ek R).
- **Sonuç:** çıkış tarihi, fiyatı ve nedeni (stop / trail / zaman / bilanço / kural dışı). Tutma günü. **MAE** ve **MFE** (R cinsinden).
- **Hesap:** **R çarpanı** (tüm lotlar, komisyon dahil: net $ kâr / ilk 1R $). Komisyon. Alış ve satış TCMB kuru. TL kâr/zarar.
- **Disiplin:** kural ihlali (evet/hayır + açıklama). Ekran görüntüsü bağlantısı.
- **Ayrı sekme: "kaçan sinyaller"** (dolmayan emirler ve atlanan tetikler): sinyal fiyatı, 20 gün sonraki fiyat. Kaçırma maliyetini ölçmek için.

### 7.3 İstatistik ve kapılar

**Hesap (her 10 işlemde bir; kol bazında ve toplamda):**
- n; ortalama R (m); standart sapma (s); SE = s / √n; t = m / SE.
- İsabet; ortalama kazanç (R); ortalama kayıp (R); profit factor; en uzun kayıp serisi.
- Net kârın en iyi %10'luk işlemlerden gelen payı. Pozitif çarpık sistemde >%100 olması normal (SEY §5.3 madde 5).
- Rejime göre ayrışma; ortalama kayma; S&P'ye beta.

**Hesaplanmış örnek:** Bu tür sistemlerde s ≈ 2R alınabilir (SEY §3.7: +0,2R / 2,13R). n=50'de SE ≈ 0,28R; n=100'de ≈ 0,20R.

| Kapı | Şart | Sonuç |
|---|---|---|
| **Faz 1 → Faz 2** | n ≥ 50 (S1+S2) **ve** ≥4 ay **ve** m ≥ +0,25R **ve** t ≥ 1,0 (s=2R'de m ≳ 0,28R) **ve** zirveden düşüş <%7 **ve** kural ihlali <%10 | Risk %0,5; piramit serbest (YEŞİL'de) |
| **Faz 2 → Faz 3** | n ≥ 100 **ve** ≥9 ay **ve** m ≥ +0,25R **ve** t ≥ 1,65 (tek yönlü %95; m ≳ 0,33R) **ve** en az bir KIRMIZI → YEŞİL döngüsü yaşanmış **ve** son 12 ayın vergi öncesi USD getirisi §1.2 engelini geçmiş | Risk %0,75 (en çok %1); E'yi C'nin %25–35'ine çıkarma değerlendirilir |
| **"Kanıtlandı"** | SPRT H1'i kabul eder. +0,2R sistemde medyan ~390 işlem, yani bu tempoda 4–6 yıl (SEY §3.7) | Ancak o zaman E'nin "yüksek getiri" sürümü (progresif boyut, sınırlı margin) gündeme gelir |
| **Geri düşüş** | Son 50 işlemin m'si <0 | Bir faz aşağı |

- Ölçek **yalnız** bu kapılarla büyür. 12 ay ve 100 işlemden önce yalnız öldürme kararı verilebilir (SEY §5.3 madde 4).
- Faz 1'deki kapı (t ≥ 1,0) bilinçli olarak gevşek. Hata payı %0,25 → %0,5'lik küçük bir artışla sınırlı. Sermaye kararı (Faz 3) sıkı kapıya bağlı.

### 7.4 Öldürme kriterleri (önceden yazılı; SEY §5.2'den uyarlandı)

| # | Tetik | Eylem |
|---|---|---|
| K1 | Bir kolda n ≥ 30 ve m ≤ −0,3R ve t ≤ −1,3 | O kol durur. Hipotez kartı yeniden yazılmadan açılmaz |
| K2 | n ≥ 50 ve m + 1,28 × SE < 0 (80% güven aralığının üst sınırı negatif) | Kol durur |
| K3 | n ≥ 100 ve m + 1,65 × SE < +0,05R (yani maliyet düzeyinin altında) | Kol kalıcı olarak kapanır |
| K4 | Ortalama kayma > 0,15R ya da kenar tahmininin %50'si (n ≥ 20) | Emir yöntemi değişir (ör. stop-limit yerine kapanış teyitli limit); 20 işlem sonra düzelmezse kol durur |
| K5 | E zirveden −%15 (§5.2) | Plan durur |
| K6 | Kural ihlali oranı >%20 (n ≥ 20) | Tüm yeni işlemler 2 hafta durur. Sorun disiplin, kenar değil |
| K7 | Mekanizma ortadan kalktı (ör. S2 için Form 4 kuralı değişti; S3 için VIX3M yayını kesildi) | t-istatistiğine bakmadan kol durur (SEY §5.2 madde 5) |
| K8 | 12 aylık korelasyon S&P ile >0,7 **ve** S&P'ye göre kalıntı getiri ≤0 | Kol yalnız beta. Ucuz endeks pozisyonuyla değiştir ya da TL'ye dön (SEY §5.2 madde 7) |

**Kayıp serisi tek başına öldürme nedeni değil.** %25–30 isabette 200 işlemde ≥10 ardışık kayıp neredeyse kesin (%84–96; VA #37). Karar ortalama R ve düşüş üzerinden verilir.

---

## 8. Beklenen sonuç aralıkları ve engel karşılaştırması

**Varsayımlar:**
- E'nin ortalama brüt maruziyeti u ≈ 0,25–0,35.
- Boştaki nakit faizi ≈ +%2,4/yıl (%3,38 × ~0,7).
- Hepsi vergi öncesi, USD, E üzerinden.
- Olasılıklar öznel [Ö]. Taban oranlar sert: USIC %8–17 kârlı, Tayvan %13 kârlı (VA #8, #14); bu kullanıcı deneyimli, ama ABD'de ve kapanış bazlı uyarlamada ölçülmedi.

### 8.1 1. yıl (Kasım 2026 – Ekim 2027; çoğunlukla Faz 1, sonu Faz 2 olabilir)

| Senaryo [Ö olasılık] | S1 | S2 + S3 | Nakit faizi | E toplam | TL engeline göre (d=%20, §1.2) |
|---|---|---|---|---|---|
| Kenar yok, E[R] ≈ −0,1R [%40–50] | 50–60 işlem × %0,25–0,3 × −0,1 ≈ −%1,5 ile −%3 | ~0 | +%2,4 | **−%1 ile +%1** | 12–26 puan geride |
| Mütevazı kenar, +0,2R [%30–40] | ≈ +%3 ile +%4 | +%0,5 | +%2,4 | **+%5 ile +%7** | 6–20 puan geride |
| Güçlü kenar ve uygun rejim, +0,4R, Faz 2'ye geçiş [%10–20] | 70 işlem × ~%0,4 × 0,4 ≈ +%11 | +%1 | +%2,4 | **+%13 ile +%15** | Küçük hesapta başabaş, büyükte geride |
| Kötü kuyruk (%5) | Merdiven devreye girer | | | **−%6 ile −%10** | |

**Okuma:**
- 1. yılın aralığı **−%8 ile +%15**, merkez **+%2–6** (vergi öncesi USD).
- TL istikrarlı kalırsa (d≈%20) ABD kolu TL'nin gerisinde kalır. Toplam servete etkisi, E = C'nin %10–15'i ile **C'nin −%1 ile −%2,5'i**. Bu, ölçümün bilinçli bedeli.
- TL vadelinin fiyatladığı hızda (d≈%33) ya da şokla (d≥%45) değer kaybederse aynı sonuç TL'yi geçer (§1.2; PRA §4.2).
- İşlem başına standart sapma s≈2R iken 55 işlemin toplamının standart sapması ±15R (√55 × 2), yani %0,25 riskte ±%3,7. Tek yılın sonucu kenarı **kanıtlamaz**.

### 8.2 2.–3. yıl, yalnız Faz 3 kapısı geçilirse

| Durum | E getirisi | Dayanak |
|---|---|---|
| Medyan yıl (%0,75–1 risk, 70–100 işlem, +0,25–0,35R) | **+%17 ile +%30** | Aritmetik: 85 × %0,85 × 0,3 ≈ %22 + nakit ve uydular. PROF §3.3 Model B: %1 risk + merdiven → medyan %20,6 (orada yılda 160 işlem; bizde daha az) |
| İyi tema yılı | +%35 ile +%60 | KIM §5.2: %0,5 riskle 150 işlem ~%26; iyi yılda progresif boyutla %40–80 |
| Kötü rejim yılı | −%10 ile −%20 | KIM §7.1 (−%10 / −%25); FFTY 2022 −%51 filtresiz |
| %5 olasılıklı kötü MDD | −%15 ile −%25 | PROF §3.3 (−%18,9 merdivenle; kümeli kitapta daha kötü) |
| TL engeline göre | Medyan yıl engel civarında (%15–26), iyi yılda belirgin üstünde, kötü yılda altında | §1.2 |

### 8.3 "Yüksek getiri" sorusuna dürüst cevap

- %50–100+ yıllar, doğrulanmış kazananlarda %1 risk, yılda 150–400 işlem, progresif boyut, margin ve güçlü tema rejiminin çarpımından geliyor (PROF §1.2; KIM §5.2).
- Bu planın gün içi olmayan, kapanış bazlı sürümü işlem sayısını ve isabeti düşürüyor (VP §3.8).
- Bu yüzden bu yolu **kanıt gelmeden açmıyoruz.** Kanıt geldiğinde bile olasılık küçük: taban oran USIC'te %8–17 kârlı.
- Doğrulanmış bir sağ kuyruk var (Luk, J Law, Sean Ryan; VA #13–14). Plan C'nin amacı, kullanıcının bu kuyrukta olup olmadığını **en ucuz şekilde** öğrenmek.

**En büyük belirsizlikler:**
1. S1'in bu uyarlamasının hiç backtest'i yok (VA §4.2; TEST §8).
2. S3, tek bir örneklem içi testten geliyor.
3. S2'nin yayın sonrası kanıtı yok.
4. 2026 vergi tarifesi doğrulanmadı.
5. IBKR şirketi ve ETF erişimi doğrulanmadı.
6. Kurun yönü engeli 0'dan 26 puana kadar oynatıyor.

---

## 9. Pazartesi 09.11.2026: tek sayfalık kontrol listesi

**Hafta sonu (Cumartesi 07.11):**
- [ ] Cuma kapanışıyla rejim tablosu (§3.1): S&P / 200 GHO (7.323), NDX 10/20, **VIX/VIX3M** (≥1,00 → KIRMIZI), S5FI/S5TH. NFP sonucu not edildi.
- [ ] S3: Cuma kapanışında VIX/VIX3M <0,95 mi? Evet ve hesap fonluysa Pazartesi SPY girişi (§2.3); değilse "kaçan" yaz.
- [ ] E kararı yazılı: E = C × %10 (en çok %15) = ____ $. Sermaye zaten USD'deyse çevrim yok.
- [ ] Hipotez kartları S1/S2/S3 (§7.1) tarihli olarak yazıldı.
- [ ] Günlük (§7.2) ve "kaçan sinyaller" sekmesi hazır.
- [ ] TradingView: Pine tarayıcı (HAZ §5a), izinli küme izleme listeleri (§4.2), `CBOE:VIX/CBOE:VIX3M`, S5FI/S5TH, NDX 10/20 GHO grafiği.
- [ ] Adaylar için grafikte TT, RS çizgisi, baz, pivot, yapısal stop ve ATR şartı; sürpriz/revizyon filtresi (Nasdaq.com Earnings, Yahoo "EPS Trend"); sıradaki bilanço tarihleri (MDT, BRK-B, BJ teyit).

**Pazartesi sabah (08:00–12:00 TSİ):**
- [ ] IBKR başvuru durumu. Onaylandıysa USD SWIFT bugün gönderilir (bakiye Salı–Çarşamba). Başvuruda IBKR şirketini (IB LLC / IBIE) ve ABD ETF erişimini yazılı sor. W-8BEN.
- [ ] Midas onaylandıysa küçük bir TL → USD çevrimiyle kur makasını ölç.
- [ ] S2 taraması: son 10 işlem gününün küme alımları (openinsider) → EDGAR Form 4 teyidi → §2.2 filtreleri. Uyan varsa Salı girişi için kart.
- [ ] Mali müşavir: kur türü (TCMB alış), nakit USD'nin kur farkı, ticari kazanç riski, tereke vergisi.

**Pazartesi 16:45–17:15 TSİ:**
- [ ] Rejim KIRMIZI ise **S1 emri yok.** (Beklenen durum bu.)
- [ ] Hesap fonluysa **emir tipi testleri, 1 adet:** GTC sell stop, buy stop-limit (DAY, RTH), MOO, bracket/OCA. Sonra iptal ya da kapat; maliyeti günlüğe "test" diye yaz.
- [ ] Toplam ısı = 0; tavan KIRMIZI'da %1 (S2 en çok 2 pozisyon, S3).
- [ ] Opsiyon: **kapalı** (VIX 28, oran 1,10).

**17:30–00:00 TSİ:** Ekran yok.

**Salı 10.11 (CPI 16:30):** 16:45'ten önce emir yok. S&P vadelisi CPI sonrası ±%1,5'ten fazla oynarsa yeni giriş yok. Rejim SARI olduysa en çok 2 pilot S1 girişi (%0,25 risk, ilk 3 izinli küme).

**Perşembe 12.11:** TCMB swap hariç net rezerv. İkinci haftalık >5 mlr $ düşüş + bir başka TRM §5.1 tetiği → C'nin USD payını %25–35'e çıkar (nakit; işlem riski aynı) (§1.3).

**Cuma 13.11 (PPI):** Haftalık istatistik: n, m, s, t, ısı, kayma. Kuralları **değiştirme**; değişiklik yeni bir hipotez kartıdır.
