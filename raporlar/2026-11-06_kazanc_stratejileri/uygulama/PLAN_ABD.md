# ABD Swing Planı (nihai, kırmızı takım sonrası): 9 Kasım 2026'dan itibaren

**Hazırlanma:** Cuma 06.11.2026, ~14:00 TSİ; kırmızı takım revizyonu ~16:00 TSİ. Son kapanış Perşembe 05.11.2026.
- Ekim tarım dışı istihdam (NFP) bugün 16:30 TSİ'de açıklanıyor. Bu dosyadaki rejim okuması NFP öncesine ait.
- Rejim **Cumartesi 07.11 sabahı Cuma kapanışıyla yeniden okunur** (§2.6).

**Başlangıç:** Pazartesi 09.11.2026. ABD seansı 17:30–00:00 TSİ. ABD 1 Kasım'dan beri kış saatinde (EST); TSİ = ET + 8.

**Kullanıcı:**
- Türkiye'de yerleşik; BIST spot ve VİOP tecrübeli.
- Swing ufku: günler–haftalar, en çok birkaç ay.
- Gün içi ekran işlemi yok, al-tut yok.
- Tematik kümelerle ("stratejik küme") çalışmayı seviyor; yüksek ödül arıyor.

**Nasıl üretildi:**
- Girdiler: üç bağımsız taslak (`taslak/abd_A.md`, `abd_B.md`, `abd_C.md`) ve üç hakem raporu (kanıt, uygulama, değer).
- **İskelet C'den** (kanıt ve değer hakemlerinin kazananı). **İşlem mekaniği A'dan** (uygulama hakeminin kazananı). Kademeli transfer ve vergi tablosu B'den.
- **B'nin kaldıraçlı endeks çekirdeği reddedildi.** Bu, fiilen kaldıraçlı al-tut; 2010 sonrasında filtre getiriyi de kesti (VA §2.1).
- **İki kırmızı takım turu uygulandı:** pre-mortem (KT1) ve olgu/kural denetimi (KT2). 2 + 2 KRİTİK ve 5 + 4 ÖNEMLİ bulgunun hepsi uygulandı; hangisinin nerede ve nasıl uygulandığı §12'de.
- Taslaklardan düzeltilen kusurlar §11.2'de.

Yatırım tavsiyesi değildir. Vergi satırları mali müşavirle teyit edilmeli.

**Kaynak kısaltmaları.** Yollar `raporlar/2026-11-06_kazanc_stratejileri/` altında. Doğrulama dosyaları raporlarla çeliştiğinde doğrulama geçerli.

| Kısaltma | Dosya |
|---|---|
| KIM / KEN / TEST / PRA / PROF | `ajanlar/abd_kim_kazaniyor.md` / `abd_swing_kenarlar.md` / `abd_test.md` / `abd_pratik.md` / `abd_profesyonel.md` |
| DLG / SEY / TRM | `ajanlar/dalga_abd.md` / `seytan_taban_oranlar.md` / `tr_makro_engel.md` |
| VA / VC / VD / VP | `dogrulama/v_abd.md` / `v_capraz.md` / `v_dalga.md` / `v_profesyonel.md` |
| HAZ | `uygulama/abd_hafta_hazirlik.md` |
| A / B / C | `uygulama/taslak/abd_A.md` / `abd_B.md` / `abd_C.md` |
| HK / HU / HD | Hakem raporları: `taslak/abd_hakem_kanit:.md` / `abd_hakem_uygulama:.md` / `abd_hakem_deger:.md` |
| KT1 / KT2 | Kırmızı takım: `taslak/abd_kirmizi_1.md` (pre-mortem) / `taslak/abd_kirmizi_2.md` (olgu ve kural denetimi) |
| RUTİN / PINE | `uygulama/ABD_GUNLUK_RUTIN.md` / `uygulama/kod/abd_rejim_ve_sablon.pine` |

**Adlandırma:** Kümeler K1–K11 (§4.2). Öldürme kriterleri DUR-1…DUR-10 (§8.5; önceki sürümde K1–K10). Kurulumlar S1, S2; gölge kollar G1–G3.

**Etiketler:**
- **[D]** Doğrulama turunda DOĞRU çıktı.
- **[K]** Kısmen doğru ya da doğrulanamadı.
- **[P]** Uygulayıcı kuralı veya öz beyan; akademik testi yok.
- **[H]** Hesap (taslak, hakem, kırmızı takım ya da bu dosya). Kalibre edilmemiş; yalnız göreli büyüklük olarak okunmalı (VP eksik #11).
- **[Ö]** Tasarım seçimi ya da öznel tahmin.

**E ve NLV:** E = ABD strateji sermayesi (IBKR'deki USD + TL'de bekleyen pay). NLV = IBKR hesabının net likidasyon değeri, yani gerçekten ABD'de duran para. Şimdiki aşamada NLV = E'nin %40'ı; bu yüzden **E'nin %1'i NLV'nin %2,5'i eder**. Bütün limitler E ile tanımlanır ve NLV karşılığıyla birlikte yazılır (KT1 #1).

---

## 0. Yönetici özeti (10 satır)

1. **Pazartesi canlı risk sıfır.** Dört neden var:
   - Rejim KIRMIZI: VIX/VIX3M 1,10 (KIRMIZI koşulu a).
   - SARI tetiği de yok: S&P ve NDX'te 10 GHO < 20 GHO, FTD yok. Ayrıca SARI için şartların **3 kapanış üst üste** sağlanması gerekiyor.
   - IBKR'de gerçekçi ilk işlem 11–13.11.
   - Takip günü (FTD) en erken Çarşamba 11.11.

   Pazartesi yapılacaklar: hesap fonlama, 1 adetlik emir testleri (§6.2), izleme listesi, işlem günlüğü.
2. **İlk canlı pilot en erken Pazartesi 16.11, 16:45–17:15 TSİ.** Zincir: Cuma 6.11 ralli denemesinin 1. günü olur, Çarşamba 11.11 FTD gelir, 11–13.11 kapanışlarında SARI şartları sağlanır.
   - S&P 200 GHO'nun %2'den az üstündeyken ("yakın bölge") **en çok 1 açık pozisyon**, ısı ≤ E'nin %0,5'i, risk %0,25.
   - Pilot AI dışı, izinli ve savunmacı bir kümeden; tetik FTD ya da S&P 10 > 20.
3. **Sermaye:** Para TL'deyse E, likit servetin **%10'u** (en çok %15'i).
   - Şimdi E'nin **%40'ı** USD'ye çevrilir ve IBKR **nakit hesabına** gider. Kalan %60 TL'de: %10'u banka PPF'sinde (sonraki dilim), %50'si 32 günlük mevduatta.
   - Para zaten USD'deyse E ≤ servetin %20'si; çevrim yok.
   - Döviz anahtarı tetiklenirse gelen ek USD IBKR'ye değil, Türk bankasında döviz mevduatına gider.
4. **Canlı kol tek:** rejim filtreli lider swing. İki kurulumu var: S1 baz kırılımı ve S2, yükselen 10/20 GHO'ya geri çekilme.
   - Bilanço gap'i (G1) ve VIX çözülmesi (G2) yalnız **gölge** kayıtta. Insider kolu ertelendi.
   - Opsiyon kapalı; IBKR'de opsiyon izni Faz 2 kapısına kadar istenmez. Midas'ta ≤ 500 $ test parası dışında bakiye tutulmaz. Kaldıraçlı ETF, margin ve açığa satış yok.
5. **Emir rutini** (RUTİN dosyası):
   - **Kapanış bloğu** (gece 00:30–01:00 ya da sabah 08:00–09:00): rejim, çıkış emirleri (MOO/MOC, stopla aynı OCA grubunda), stop düzeltmeleri, stop mutabakatı, günlük.
   - **Akşam emir bloğu** (16:45–17:15): yalnız girişler. BUY STOP-LIMIT (DAY) + ekli GTC SELL STOP (yalnız normal seans). Bekleyen giriş emirleri dolmuş sayılır ve tavana tabidir.
   - 17:30–00:00 arası ekrana bakılmaz, emir değiştirilmez.
6. **Risk tavanları (Faz 1, ilk 50 işlem):**
   - İşlem başı risk %0,25. Tek pozisyon ≤ %7,5. Küme ısısı ≤ %0,75. Toplam açık risk (gap-ayarlı): SARI'da %1,25 (yakın bölgede %0,5), YEŞİL'de %2,5.
   - Aylık devre kesici %3.
   - Düşüş merdiveni −%3 / −%5 / −%6,5. Strateji zirveden **−%8**'e düşerse plan durur.
   - Hepsi E'nin yüzdesi. Aşama 1'de dur eşiği NLV'nin −%20'si, servetin −%0,8'i: 4.000 / 20.000 / 80.000 $ (E = 50k / 250k / 1m).
7. **Davranış freni:** Kritik ihlal listesi var (rejim dışı giriş, stopu indirmek, zarara ekleme, opsiyon/kaldıraç, AI dip alımı, seans içinde emir değiştirmek ve diğerleri; §8.5 DUR-6a). İlk ihlalde 10 seans işlem yapılmaz; ikinci ihlalde plan durur. Pre-mortem'in baskın yolu bu (KT1 §2).
8. **Engel (TL'den gelen sermaye):** TL'de kalmayı yenmek için gereken vergi öncesi USD getirisi.
   - Planın tipik maruziyetinde (pozisyonda kalma payı u ≈ 0,3): 50k / 250k / 1m $ hesapta **%12,7–19,5 / %15,6–23,3 / %17,5–25,9**. Tam yatırımda ~%17–34; doğrulanmış çapa ~%20–28.
   - USD'den gelen sermayede engel %2,3–6,2 (u = 0,3; IBKR'nin kademeli nakit faiziyle).
9. **1. yıl beklentisi (dürüst):** Yalnız strateji sonucu, nakit faizi hariç, vergi öncesi. Kenara göre medyan −%2,5 ile +%6,5 arası; ağırlıklı merkez **−%1,5 ile +%1,5**.
   - Vergi sonrası merkez ~−%2 ile +%1. Bu, USD nakdin vergi sonrası getirisinin (%1,15–2,6) altında.
   - Aşama 1'de boştaki USD'nin faizi E'nin yalnız ~%0–0,3'ü.
   - TL engelini geçme olasılığı **< %5**. Servete maliyet, TL'de kalmaya göre: aşama 1'de yılda ~%0,3–0,8; tam çevrimde ~%0,9–1,6.
10. **Yüksek ödül ancak kanıttan sonra gelir.** Faz 3 kapısı: 100 işlem, 12 ay, t ≥ 1,65 ve hayatta kalma yanlılığından arındırılmış gün sonu (EOD) backtest'i.
    - Kapıdan sonra risk %0,75–1'e çıkar; dürüst merkez yine de ~%8–16.
    - Medyanı %40+ olan bir yıl için üç şart gerekir: ≥ +0,3R kenar, yılda ≥ 150 işlem ve %5 olasılıkla ~−%45'lik düşüşü kabul etmek. Böyle bir kenarın bulunma olasılığı ~%7–10.
    - Kurallar önceden yazılı: ölçek kapıları ve öldürme kriterleri (§8), döviz anahtarı (§1.5; ilk kontrol Perşembe 12.11 TCMB rezerv verisi), takvim (§7).

---

## 1. Sermaye ve engel kararı

### 1.1 Girdiler (doğrulanmış)

| Kalem | Değer | Kaynak |
|---|---|---|
| TL'de kalmanın net nominal getirisi | Faiz sabit kalırsa ~%36–38 (32 günlük mevduat roll). Anket patikasında ~%31–33 | VC #4 [D] |
| TL'de kalmanın ileriye dönük USD karşılığı | ~%13–15,5. Faiz indirimi ya da kur şoku kuyruğunda %6–12. h = %31 / 35 / 37 ve kur +%20 ile **%9,2 / %12,5 / %14,2** | VA #34 [D]; HD §2.1 [H] |
| TL carry'nin geçmişi (USD bazında) | 2010–26: **−%7,2/yıl, en büyük düşüş −%85**. 2020–26: −%10,1/yıl | TEST §0 #10; VA #34 [D] |
| Kur vadelisi | 12 ay zımni ~%32,7–32,9. Bu bir tahmin değil, faiz paritesi (CIP) sonucu; uzak vadeler likit değil. Likit vadeler: Kasım ~%32, Aralık ~%33. Anketin 12 aylık kur beklentisi 59,26, yani ~%18,4 | VC #3, #5 [D] |
| USD risksiz getiri | 3 aylık T-bill %4,03 (iskonto), 13 hafta kupon eşdeğeri %4,10 | VC #13 [D] |
| IBKR boş nakit faizi (Pro) | **Kademeli:** ilk 10.000 $'a %0, üstüne %3,38 (BM − %0,5). NAV 100 bin $'ın altındaysa oran NAV / 100 bin oranında düşer. Örnek: NAV 80 bin $, nakit 20 bin $ → %1,352 | IBKR faiz sayfası, 18.09.2026 oranları (KT2 Ö-1) [D] |
| ABD kazancının TR vergisi | Değer artışı olarak, TL bazında ve **kur farkı dahil** beyan edilir; artan oran %15–40. Zarar yalnız aynı yıl içinde mahsup edilir, devretmez. Yİ-ÜFE endekslemesi yalnız artış ≥ %10 ise (~6 ay). Margin faizi indirilemez | VC #10 [D] |
| 2026 tarifesi | 190 bin / 400 bin / 1 mn / 5,3 mn TL; %15/20/27/35/40 | PRA §2.1; **VC #11: DOĞRULANAMADI** |
| Temettü | ABD stopajı %20 (gerçek kişi, W-8BEN ile). Beyan sınırı 22.000 TL | VC #10, #12 [D] |
| Elde tutulan USD | Dövizin kendi kur kazancı vergilenmez; menkul kıymet içindeki kur kazancı vergilenir | PRA §2.5, §4.2 [K, müşavir teyidi şart] |
| Kambiyo BSMV | Döviz alımında binde 2 | PRA §2.5; VC: DOĞRULANAMADI |

### 1.2 Hesap büyüklüğüne ve maruziyete göre engel [H]

**Model:** Vergilenebilir TL kazancı ≈ E × kur × [R × (1+d) + u × d] (C §1.2; HD §2.1; PRA §2.6 mantığı).
- E: ABD strateji sermayesi (USD).
- R: vergi öncesi USD getirisi.
- d: yıllık kur artışı (burada %20; kur 50,05).
- u: sermayenin pozisyonda kaldığı pay. Pozisyondaki sermayenin kur farkı vergiye girer; boştaki USD nakdinki girmez.
- Tarife: 2026 (doğrulanmadı). Başka beyan geliri yok. Vergi ertelemesinin değeri sayılmadı (muhafazakâr).
- Betik: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/plan_final/at.py` (HD `ev.py` ile aynı model; KT2 yeniden çalıştırdı, birebir tuttu). USD nakit sütunu IBKR kademeleriyle bu revizyonda yeniden hesaplandı.

| E | USD nakit (IBKR kademeli; E'nin tamamı nakitte), vergi sonrası | TL'yi yenmek için gereken R, u=0,3 (h=%31 / %37) | u=0,6 | u=1,0 | USD kökenli sermayede USD nakde eşit olmak için gereken R (u=0,3 / u=1) |
|---|---|---|---|---|---|
| 50.000 $ | **%1,15** (brüt %1,35) | **%12,7 / %19,5** | %14,5 / %21,4 | %17,1 / %24,7 | %2,3 / %6,0 |
| 250.000 $ | %2,6 (brüt %3,25) | **%15,6 / %23,3** | %18,3 / %26,0 | %22,1 / %30,5 | %5,5 / %11,8 |
| 1.000.000 $ | %2,4 (brüt %3,35) | **%17,5 / %25,9** | %20,9 / %29,2 | %25,3 / %33,7 | %6,2 / %14,0 |

**Okuma:**
1. Engel hesap büyüdükçe yükselir (vergi dilimi) ve maruziyet arttıkça yükselir (hayalet vergi). Tam yatırım satırı doğrulanmış çapayla tutarlı: ~%20–28 (VC #22).
2. **Hayalet vergi:** Sıfır USD getiride bile pozisyondaki sermayenin kur farkı vergilenir. u=0,3 ve d=%20 için yıl sonu kuruyla (60,06) E'nin ~%0,75 / %1,10 / %1,55'i eder (50k / 250k / 1m). Başlangıç kuruyla %0,9 / %1,3 / %1,9 görünür; TL tutarı aynıdır: ~22,5 bin / 165 bin / 930 bin TL (C §1.2; HD §3.3; KT2 küçük #6).
3. d = %32,9 (kur vadelisinin fiyatladığı hız) satırı bir **senaryo**, tahmin değil (VC #5). O hızda ~%0–9'luk getiri yeterdi. Karar bu satıra dayandırılmaz.
4. 50k'da USD nakit getirisi küçük: ilk 10 bin $'a faiz yok ve NAV 100 bin $'ın altında oran düşüyor. Aşama 1'de (NLV 20k, pozisyonlar ~15k) boştaki USD fiilen **faizsizdir** (§1.6).

### 1.3 Karar

| Durum | E (ABD strateji sermayesi) | Gerekçe |
|---|---|---|
| **Sermaye TL'de** | **Likit servetin %10'u**, en çok %15'i | Dört gerekçe: (a) Bu tarzın EOD uyarlaması hiç test edilmedi (VA §4.2; VP eksik #8). (b) Taban oranlar kötü: USIC'te katılımcıların %8–17'si kârda (VA #14). (c) +0,2–0,3R'lik bir kenarı şanstan ayırmak 280–450 işlem ister (SEY §3.7); bu planın temposunda (yılda 70–120 işlem) bu **2,3–6,4 yıl** eder (KT2 küçük #13). (d) 1. yıl beklentisi engelin altında (§9); TL'de kalmaya göre maliyet servetin yılda ~%0,3–1,6'sı (§9.3) |
| **Sermaye zaten USD'de** (döviz hesabı, Eurobond) | min(eldeki USD, servetin %20'si). TL'ye çevrim yok; boştaki kısım USD nakitte | Kıyas artık TL değil, USD nakit. u=0,3'te gereken vergi öncesi R ~%2,3–6,2 (§1.2). Risk kuralları aynı kalır |
| **Ölçek büyütme** | E'yi servetin %25–35'ine çıkarmak **yalnız** Faz 3 kapısından sonra (§8.3) | Kenar istatistikle görülmeden sermaye büyütmek "tahmin hatası Kelly'yi öldürür" tuzağıdır (SEY §3.3, §5.3 #4) |

**Çalışılmış örnek (E üç boyutta):**

| | E = 50k $ | E = 250k $ | E = 1m $ |
|---|---|---|---|
| İma ettiği likit servet (%10) | 500k $ | 2,5m $ | 10m $ |
| Şimdi USD'ye çevrilecek (%40) = aşama 1 NLV | 20k $ | 100k $ | 400k $ |
| TL'de bekleyen: PPF (%10, sonraki dilim) / 32 günlük mevduat (%50) | 5k / 25k $ | 25k / 125k $ | 100k / 500k $ |
| Plan durursa (−%8 E) | −4.000 $ = NLV −%20 = servet −%0,8 | −20.000 $, aynı oranlar | −80.000 $, aynı oranlar |
| Veri ve yazılım | TradingView ücretsiz ya da Essential (yıllık ödemeyle 12,95 $/ay ≈ 155 $/yıl, E'nin %0,3'ü) + ücretsiz finviz. **Pine Screener yalnız Premium'da** (yıllık ödemeyle 59,95 $/ay ≈ 719 $/yıl = E'nin %1,4'ü): **alınmaz** (KT2 Ö-2) | Premium uygun (E'nin %0,29'u). Tam set (~1.000–1.300 $/yıl) E'nin %0,4–0,5'i | Tam set: E'nin ~%0,1'i |
| ABD veraset vergisi (60k $ üstü US-situs varlık) | Pozisyonlar dolarsa sınırda | **Risk var** | **Risk var** |

Veri ve yazılım maliyeti PRA §5 ve TradingView fiyat sayfasından (KT2 Ö-2), veraset eşiği VA #36'dan.

### 1.4 Kademeli USD çevrimi

Rejimin kullanamayacağı USD boşta beklerse, boşta bekleyen kısım için yıllık fırsat maliyeti ~9–12 puandır (HD §3.1 [H]). Bu yüzden yalnız rejimin brüt tavanı ve %10 tampon USD'ye çevrilir. Dayanak: HD aşı 3; B §1.3; A C2.

| Aşama | Tetik | USD'deki pay (E'nin) | 50k | 250k | 1m |
|---|---|---|---|---|---|
| 1 | Şimdi. Gerekçe **pilot hazırlığı**: SWIFT 1–2 iş günü sürdüğü için para SARI gelmeden hazır olmalı. Faz 1 SARI brüt tavanı %30 + tampon | **%40** | 20k | 100k | 400k |
| 2 | İlk YEŞİL kapanış | %50 (Faz 1 YEŞİL brüt tavanı %40 + tampon) | 25k | 125k | 500k |
| 3 | Faz 2 kapısı geçildi | %70 | 35k | 175k | 700k |
| 4 | Faz 3 kapısı geçildi | %100 | 50k | 250k | 1m |

- **KIRMIZI'da bekleme maliyeti:** Aşama 1 parası rejim KIRMIZI iken de USD'de bekler. Maliyeti E'nin haftada ~%0,1'i: TL mevduatın USD karşılığı ile IBKR faizi arasındaki fark (KT1 #12 [H]). İlk SARI kapanışını beklemek ilk pilotu 1–2 gün geciktirirdi (KT2 küçük #24).
- **TL'de bekleyen pay:**
  - Sonraki dilim (E'nin %10'u) banka iştiraki bir para piyasası fonunda (PPF) tutulur. Böylece aşama 2 için vade bozmak gerekmez (KT2 küçük #19).
  - Kalan %50 büyük bankada 32 günlük mevduattadır.
  - Grup ihracı teminatlı fonlardan kaçınılır: PPF risksiz değil (VP eksik #2). Yeni alınan DİBS'in stopajı teyitsiz (VC #8).
- **Transfer:** tetik geldiği gün sabah SWIFT gönderilir; para 1–2 iş gününde ulaşır. Mevcut USD payı, transfer yolda iken yeni girişlere yetecek büyüklükte. İlk transferde kur makası küçük tutarla ölçülür (KT1 #12; VC #16: ölçülmedi).
- **USD → TL geri dönüş** yalnız iki durumda yapılır: plan durursa (§8.5 DUR-5) ya da 40 seans boyunca hiç yeni giriş açılamadıysa. Kur makası nedeniyle gidip gelinmez.
- **Risk tabanı (E):** ayın son iş günü güncellenir. E = NLV + TL'de bekleyen payın o günkü TCMB kuruyla USD karşılığı. Bütün yüzde riskleri bu E üzerinden hesaplanır.
- **Düşüş merdiveni** yalnız stratejinin USD kâr/zararından ölçülür (§5.2). TL payının kur hareketi merdiveni etkilemez.

### 1.5 Döviz anahtarı (işlem kenarından bağımsız)

Servetin %85–90'ı TL'de kalıyor. Toplam riski en çok etkileyen kural bu yüzden budur (HD §0). Kaynak: TRM §5.1 "carry'den çık / long USD" tetikleri.

**Kural:** Aşağıdaki beş tetikten **ikisi** oluşursa servetin USD nakit payı **%25–35**'e çıkarılır.
- Fazla USD **Türk bankasında döviz mevduatında** tutulur. **IBKR'ye gönderilmez** (KT1 #7). Üç neden var: E ile NLV karışmasın; teyitsiz IBKR kuruluşunda (IB LLC / IBIE) yoğunlaşma olmasın; ABD veraset riski büyümesin (VA #36). Elde tutulan dövizin kur kazancı vergisizdir (PRA §2.5 [K]).
- İşlem riski aynı kalır.
- E değişmez.

| Tetik | Bugün | Durum |
|---|---|---|
| Swap hariç net rezerv < 0, ya da 2 hafta üst üste haftalık düşüş > 5 mlr $ | 24,3 mlr $; son hafta −6,5 mlr $ (VC #18 [D]) | Yarısı oluştu |
| Yabancı DİBS çıkışı > 1 mlr $, 2 hafta üst üste | −750 mn $ | Yok |
| CDS 5 yıl > 300 | 248 (**DOĞRULANAMADI**, VC §1) | Yok; kaynağı teyit et |
| 1 aylık USDTRY vadelisinin zımni yıllık getirisi politika faizini 5 puan aşıyor | ~%32–33 (Kasım–Aralık vadeleri; VC #5); politika faizi %36 | Yok |
| Ex-ante reel faiz < %3 | %9,8 (makul bant %5–8; VC #3) | Yok |

**Perşembe 12.11 rezerv verisi kritik:** ikinci bir > 5 mlr $ haftalık düşüş birinci tetiği tamamlar.

### 1.6 Boştaki USD ve nakit

- **Aracı kurumda nakit kalır.** T-bill'e ya da para piyasası ETF'ine (SGOV, BIL) **konmaz**.
  - Gerekçe: %20 kur artışında T-bill pozisyonunun ~%5–7'si kur farkı vergisine gidebilir (HD §6 #2; PRA §2.5). Müşavir teyidi şart.
  - **Düzeltme (KT2 Ö-1):** Önceki sürümdeki "kaybedilen faiz yalnız 0,65 puan" ifadesi NAV 100 bin $'ın altında geçersiz. Küçük hesapta kaybedilen faiz T-bill getirisinin neredeyse tamamı (~%2,7–4). Kur %10 artarsa iki seçenek yaklaşık başa baş olur. Yine de nakit seçilir: tutar küçük ve iş yükü sıfır [Ö].
- **IBKR faiz kademeleri doğrulandı** (§1.1). Aşama 1'de boştaki USD'nin faizi:
  - 50k: ~0 (nakit ≤ 10 bin $).
  - 250k: E'nin ~%0,2'si.
  - 1m: E'nin ~%0,3'ü.
- **Faiz geliri** menkul sermaye iradı olarak beyan edilir (PRA §4.1).
- **Veraset vergisi:** ABD hisseleri 60 bin $ üstünde US-situs varlık sayılır (VA #36). Aracı kurum nakdinin konumunu uzmana sorun.

---

## 2. Rejim anahtarı

### 2.1 Girdiler

Her ABD kapanışından sonra kapanış bloğunda hesaplanır (gece 00:30–01:00 ya da sabah 08:00–09:00 TSİ). Hesap PINE dosyasındaki `ABD_RJ` göstergesiyle yapılır (§2.7).

| Gösterge | Kaynak |
|---|---|
| S&P 500 kapanışı; 10, 20, 50 ve 200 günlük basit ortalamalar (GHO); S&P / 200 GHO oranı | `SP:SPX`, FRED SP500 |
| Nasdaq-100'ün 10 ve 20 GHO'su ve 1 günlük eğimleri | `NASDAQ:NDX` |
| VIX/VIX3M kapanış oranı (VIX kapanışı 00:15 TSİ) | `CBOE:VIX/CBOE:VIX3M` |
| S5FI (S&P'de 50 GHO üstü hisse yüzdesi) ve S5TH (200 GHO üstü) | `INDEX:S5FI`, `INDEX:S5TH` |
| FTD (takip günü; §2.3) ve ralli denemesinin gün sayısı | Elle sayım |
| Ardışık SARI kapanış sayacı; pilot freni (§2.4) | `ABD_RJ` + elle |
| Bilgi: MAHQ − MALQ (Nasdaq 52 haftalık zirve − dip), RSP'nin 50 GHO'ya göre konumu | HAZ §5d |

### 2.2 Durumlar ve izinler

| Durum | Koşul | Yeni canlı giriş | Toplam açık risk (gap-ayarlı), Faz 1 / 2 / 3 | Brüt maruziyet tavanı, Faz 1 / 2 / 3 |
|---|---|---|---|---|
| **KIRMIZI** | Herhangi biri: (a) VIX/VIX3M son iki kapanıştan herhangi birinde ≥ 1,00. (b) S&P 2 kapanış üst üste 200 GHO altında. (c) S5FI < 50 **ve** S5TH < 60 | **Yok.** Yalnız gölge kayıt | Yeni giriş yok; mevcutlar kendi kurallarıyla | Yeni giriş yok |
| **TURUNCU** (bekle) | KIRMIZI değil, ama SARI şartı yok | **Yok.** Yalnız gölge kayıt | Yeni giriş yok | Yeni giriş yok |
| **SARI** (pilot) | Aşağıdaki şartlar **3 kapanış üst üste** sağlanır (KT1 #3): KIRMIZI değil (yani VIX/VIX3M 2 kapanış üst üste < 1,00) **ve** S&P > 200 GHO **ve** tetik. **Tetik:** K9 dışındaki bütün kümelerde [geçerli FTD **ya da** S&P 10 > 20 GHO]. NDX 10 > 20 GHO tek başına yalnız K9'u açar (KT1 #8). **Pilot freni** aktifse (§2.4) ek şart: yeni ralli denemesinde FTD **ve** S&P > 50 GHO | Günde en çok 2 yeni giriş. En çok 4 açık pozisyon. Kümede 1 pozisyon. Yalnız AI dışı ve izinli kümeler. Kısmi satış 1/2. **Yakın bölge (S&P / 200 GHO < 1,02): en çok 1 açık pozisyon ve ısı ≤ %0,5** (KT1 #3) | %1,25 / %2,5 / %3 | %30 / %40 / %50 |
| **YEŞİL** | SARI'nın 3 kapanış şartı sağlanmış **ve** S&P > 50 GHO ve > 200 GHO; NDX 10 > 20 GHO ve ikisi de yükseliyor; VIX/VIX3M < 0,95; S5FI ≥ 50; ve FTD gerçekleşmiş, FTD günü dibi kapanışla kırılmamış (ya da S&P ve NDX'te 10 > 20 en az 10 seanstır sürüyor) | Faz boyutu. Günde en çok 3 yeni giriş [Ö] (KT2 K-2). En çok 8 açık pozisyon. Kümede en çok 3 pozisyon. Faz 2+'da piramit. Kısmi satış 1/3 | %2,5 / %5 / %6 (Faz 3'te %6 yalnız yıl içi kâr yastığı ≥ %10 ise; değilse %5) | %40 / %60 / %95 |

- **Isı tavanları ulaşılabilir değerlerle yazıldı** (KT2 küçük #20). Faz 1'de 4 pozisyon × %0,25 × 1,25 (gap payı) = %1,25; 8 × %0,25 × 1,25 = %2,5. Önceki sürümdeki %2 / %3 tavanlarına zaten ulaşılamıyordu.
- **Margin yapısal olarak yok:** Hesap IBKR nakit hesabıdır (§6.1). Brüt maruziyet ayrıca **yerleşmiş USD nakit − NLV'nin %5'i** ile sınırlıdır. Faz 3 YEŞİL tavanı bu yüzden %95.
- **Aylık devre kesici** (§5.1) rejimden bağımsızdır. Aktifken rejim ne olursa olsun yeni giriş yok.

### 2.3 Takip günü (FTD)

Dayanak: HAZ §3 (+%1,5 eşiği), PROF §1.1 ve §1.4 (IBD). A ve B'nin +%1,25 eşiği bu dosyada tek eşikte birleştirildi.

- **Ralli denemesinin 1. günü:** düzeltmenin en düşük kapanışından sonraki ilk artı kapanış. S&P ve NDX için ayrı ayrı sayılır.
- **Sayım sıfırlanır:** endeks o en düşük kapanışın altında kapanırsa.
- **FTD:** 4. ya da sonraki gün, S&P veya NDX'te önceki kapanışa göre **≥ +%1,5** kapanış. Hacim önceki günden yüksek olmalı (borsa toplamı ya da SPY/QQQ).
- **FTD geçersiz olur:**
  - endeks ralli denemesinin dibinin altında kapanırsa, ya da
  - 15 seans içinde S&P ya da NDX'te 10 > 20 GHO oluşmazsa (A §3.2).
- **YEŞİL için ek şart:** FTD günü dibi kapanışla kırılırsa YEŞİL olunmaz.

### 2.4 Geçiş kuralları

- Durum kapanışta hesaplanır. Ertesi günün akşam emir bloğundan (16:45) itibaren geçerlidir.
- **3 kapanış kuralı (KT1 #3):** SARI'ya her girişte, SARI şartları art arda 3 kapanışta sağlanmalıdır; durum 3. kapanışta SARI olur. Bu kural KIRMIZI'dan, TURUNCU'dan ve fren sonrası dönüşlere de uygulanır. Şartlar kesintisiz sürdükçe sayaç sıfırlanmaz; bu yüzden YEŞİL'den SARI'ya düşüşte yeniden sayılmaz.
- **Pilot freni (KT1 #3):** Bir SARI bölümünde açılan pilotlardan ≥ 2'si, girişten sonraki 10 seans içinde stop ya da başarısız kırılımla kapanırsa fren devreye girer. Bölüm, SARI'nın başladığı günden durum SARI'nın altına düşene kadar sürer.
  - Fren aktifken bir sonraki SARI için ek şart gerekir: yeni bir ralli denemesinin FTD'si **ve** S&P > 50 GHO.
  - Fren, bu şartla açılan SARI'da ilk işlem +1R'ye ulaşınca ya da durum YEŞİL olunca kalkar [Ö].
  - Dayanak: PROF §1.3 #11 ("kaybederken küçült"); IBD'de FTD sonrası %40–60 maruziyet (PROF §3.1).
- **Durum düşerse açık pozisyonlar zorla kapatılmaz.** Yalnız yeni giriş izni değişir. Isı yeni tavanın üstündeyse yeni giriş yapılmaz; mevcutlar kendi stop ve trail kurallarıyla küçülür.
- **İstisna:** S&P 2 kapanış üst üste 200 GHO altındaysa bütün iz süren çıkışlar 10 GHO'ya sıkılaştırılır (A §3.2).
- **KIRMIZI'dan çıkış:** VIX/VIX3M 2 kapanış üst üste < 1,00 **ve** S&P > 200 GHO. Bu şartlar sağlanırsa durum TURUNCU olur. SARI için 3 kapanış kuralı ayrıca işler.

### 2.5 Bugünkü okuma (05.11 kapanışı, NFP öncesi)

| Girdi | Değer | Durum |
|---|---|---|
| S&P 500 | 7.353,73 (−%4,36). 200 GHO 7.322,7 (**+%0,4**, oran 1,004; yükseliyor, Pazartesi ~7.330). 50 GHO 7.686,5 (−%4,3). 10/20 GHO 7.622 / 7.680 | 200 GHO'nun hemen üstünde, 50'nin altında; 10 < 20. **Yakın bölge:** oran 1,02 için S&P ≈ 7.480 gerekir |
| S&P 10 > 20 için gereken | Kabaca 7 seans ≥ 7.735'te ya da 10 seans ≥ 7.625'te kapanış (B §3.3 [H]; KT2 yeniden hesapladı: ~7.733 / ~7.622) | 17.11'den önce olası değil |
| Nasdaq-100 | 26.629,8. 10 / 20 / 50 GHO: 28.672 / 29.286 / 29.686. 200 GHO 27.977 (−%4,8). Zirveden −%14,7. 19.10'dan beri 10 < 20 | Kırık (VP A11 [D]) |
| VIX / VIX3M | 28,18 / 25,55 = **1,10**. 4.11'de VIX 16,61'di: tek günlük sıçrama | **KIRMIZI tetikleyici** |
| VIX/VIX3M < 1,00 için | VIX3M ~25,5 kalırsa VIX ~25,5'in altında kapanmalı. < 0,95 için ~24,3'ün altında (C §2.3) | — |
| S5FI / S5TH | 62,5 / 66,1 (TradingView önbelleği, zaman damgası karışık; HAZ §3) | Kırmızı değil; teyit et |
| MAHQ − MALQ | 150 − 490 = −340 | Büyüme tarafı zayıf |
| RSP | 50 GHO'nun +%0,7 üstünde; zirveden −%3,5 | Savunmacı genişlik ayakta |
| FTD | Yok; ralli denemesi başlamadı | — |
| Bağlam | MTUM'da rekor göreli düşüş (Temmuz 2026 −%15,5; Ekim −%8,7) **[K: VC'de doğrulanamadı]**. Liderlik sağlık, borsalar, sigorta, temel tüketim, atık/su ve konaklamaya döndü. Fed %3,75–4,00; 10 yıllık getiri %4,84–4,90 | PRA §3.4; HAZ §0, §3 |
| **Sonuç** | **KIRMIZI** (koşul a). SARI tetiği de yok. Yeni canlı giriş yok. Opsiyon kapalı | |

### 2.6 Cuma 06.11 kapanışı → ilk pilot ne zaman?

Okuma Cumartesi sabahı yapılır. SARI'nın 3 kapanış kuralı ve iki kapanışlık VIX şartı birlikte işler: SARI'nın ilk günü t ise VIX/VIX3M t−3, t−2, t−1 ve t'de < 1,00 olmalıdır.

| Cuma kapanışında | Sonuç | En erken SARI kapanışı | En erken canlı pilot |
|---|---|---|---|
| S&P artıda | Ralli denemesinin 1. günü 6.11. FTD en erken **Ça 11.11** kapanışı | **Cu 13.11.** 11, 12 ve 13.11'de SARI şartları ve 10–13.11 arasındaki 4 kapanışta VIX/VIX3M < 1,00 gerekir | **Pt 16.11, 16:45–17:15** |
| S&P yeni dip yaptı | 1. gün en erken Pt 9.11. FTD en erken Pe 12.11 | Pt 16.11 | **Ça 18.11.** 17.11'de giriş yok (NVDA); 18.11 emirleri GTD 21:55 (FOMC tutanakları) |
| VIX/VIX3M ≥ 1,00 | KIRMIZI sürer | 10.11'den itibaren 4 kapanış < 1,00 olursa yine Cu 13.11 | Yukarıdaki satırlar gibi |
| S&P ≤ 200 GHO (~7.327) | İkinci kapanış da altta olursa KIRMIZI (b) | S&P 200 GHO'nun üstüne dönmeli; sayım yeniden başlar | En erken 18.11 |

**Sonuç: Pazartesi hiçbir koşulda canlı giriş yok; bu hafta da yok.** Bu sonuç üç hakemin ortak hükmünden (HK §5; HU §6; HD §7) bir hafta daha temkinli. Nedeni KT1 #3'teki whipsaw bulgusu.

### 2.7 TradingView rejim göstergesi (Pine v5)

- **Dosya:** `uygulama/kod/abd_rejim_ve_sablon.pine` (gösterge adı `ABD_RJ`). A §3.2 ve önceki sürümün Pine v6 betiğinin yerine geçer.
- **Bu betik TradingView'de derlenmedi ve test edilmedi.** İlk kullanımda `SP:SPX` günlük grafiğinde 05.11 barının değerleri §2.5 ile karşılaştırılır. Tutmazsa rejim elle hesaplanır.
- **Ne yapar:**
  - Durum (0–3), VIX/VIX3M ve ardışık SARI sayacı (3 kapanış kuralı; savunmacı tetik ve yalnız K9 için ayrı ayrı).
  - Yakın bölge ve pilot freni (fren elle girilir).
  - Grafikteki hisse için trend şablonu (TT), RS / 52H, 52H uzaklığı, ADR%20, ATR14, 50 günlük dolar hacmi ve "uzamış" kontrolü.
  - Seçilen ETF ya da hisseyle 60 günlük getiri korelasyonu.
  - Emir hesaplayıcı: pivot ve stop girilince tetik, limit, stop/ATR, adet (limite göre), alt lotlar, pozisyon % E ve gap-ayarlı risk.
- **Elle girilenler:** FTD, FTD dibinin kırılması, pilot freni ve küme izni. Betik bunları bilmez.
- Gösterge her TradingView planında grafiğe eklenebilir; Pine Screener gerektirmez (KT2 Ö-2). Semboller HAZ §5d'de teyitli.

### 2.8 Kanıt ve belirsizlik

**Kanıt:**
- **Rejim filtresi en kritik hayatta kalma bileşeni.**
  - FFTY 2022'de −%51 yaptı (VA #17 [D]).
  - Kullamägi kendi filtresine uymadığı dönemde, Kasım 2021 zirvesinden 2022 ortasına kadar −%57 düştü (105 mn $ → ~45 mn $). Bu bir takvim yılı rakamı değil, zirveden dibe düşüş (VA #16, beyan düzeyinde; KT2 küçük #23).
  - Momentum çöküşleri panik sonrası toparlanmada geliyor; dinamik ölçekleme Sharpe'ı ~2 katına çıkarıyor (VA #27 [D]).
  - Merdivenden önce birincil araç rejim filtresi (PROF §3.3).
- **Pilot ancak FTD ya da 10 > 20 ile açılır** (PROF §1.4, §3.5 #6; SEY §5.1 #4).
- **VIX vade yapısının ters dönmesi zayıf bir gösterge** (tek günlük sıçrama; VP A11). Bu yüzden VIX/VIX3M < 1 gerekli bir şart, ama tek başına yeterli değil.

**Belirsizlik (KT1 #3 testi, 23.08.2017–05.11.2026, 2.314 seans; FTD ve genişlik yok) [H]:**
- S&P 200 GHO'nun ±%2 içinde başlayan SARI bölümlerinin %59'u 10 seanstan kısa sürdü; bu bölümler boyunca S&P medyanı −%1,1 (n = 17). ±%2 dışında başlayanlarda kısa bölüm payı %18.
- 3 kapanış kuralı kısa bölümleri yılda 1,9'dan 1,0'a indirdi. Denenen üç varyanttan işe yarayan tek buydu; seçim tek örneklemde yapıldı.
- **Endeks düzeyinde filtre getiriyi korumadı.** SARI+ günlerinde S&P'nin ertesi gün getirisi yıllık +%10,7, diğer günlerde +%19,1. Bu, "2010 sonrası filtre getiriyi kesti" bulgusuyla (TEST §0; VA §2.1) ve panik sonrası toparlanma bulgusuyla (VA #27) tutarlı. Filtrenin faydası ancak kırılımların başarısızlık oranını düşürmesinden gelebilir; bu ölçülmedi (VA §4.2).
- Bu dört durumun bu birleşimi hiç test edilmedi; yanlış alarm oranı bilinmiyor.
- Bedeli: dipten çıkışın ilk %5–10'u kaçırılır. Faydası çöküş yıllarında görünür, sakin yıllarda görünmez.

---

## 3. Kollar: kurallar

### 3.0 Kol özeti

| Kol | Durum | Gerekçe |
|---|---|---|
| **S1 Baz kırılımı** | **Canlı** (Faz 1 riski %0,25) | Doğrulanmış kazananların ortak yöntemi (PROF §1.3; VA #13–14). Tekil hissede trend takibinde sağ kuyruk gerçek (VA #18, #29). EOD uyarlaması test edilmedi |
| **S2 Yükselen 10/20 GHO'ya geri çekilme** | **Canlı** | Luk/Kell ailesi [P] (PROF §1.1). İşlem sayısını ~40–70'ten ~60–120'ye çıkarır, kanıt daha hızlı birikir (HD aşı 5) |
| G1 Bilanço gap'i (episodic pivot), 2.–5. gün | **Gölge** | Büyük hissede PEAD 2006'dan beri yok (VA #23). Sadece-uzun bilanço üst portföyleri VW piyasayı geçmiyor (TEST §6.4). Hisse düzeyinde test yapılamadı (TEST §8) |
| G2 VIX panik çözülmesi (SPY, 40 gün) | **Gölge** ve rejim bilgisi | Başlıktaki t = 3,69 T-bill'e göre. Koşulsuz piyasaya göre fark ~+1,8 puan, t ≈ 1,7. Örneklem içi, n = 25, iki tanım denendi (HU §3; HK C1) |
| G3 Insider küme alımı | **Ertelendi** | Kanıtın tamamı 1986–2007, yayın sonrası test yok (VA #26). Veri kaynağı 06.11'de 503 verdi. Ağır manuel iş (HU §3) |
| Opsiyon alımı | Kapalı (§3.9) | Sistematik alım ortalamada kaybettirir (VP A6–A8) |
| Kaldıraçlı ETF ve endeks çekirdeği, margin, açığa satış | Yok | 2010 sonrası filtre getiriyi kesti; düşüş −%55 ile −%97 arası (VA §2.1; TEST §0 #1–2). Profil al-tut yasaklıyor (HK B1) |

### 3.1 Evren ve eleme filtresi (her kurulum için)

**Evren:**
- Fiyat ≥ 20 $, piyasa değeri ≥ 2 mlr $ (HAZ §4).
- 50 günlük ortalama dolar hacmi ≥ 20 mn $; 1m $'lık hesapta ≥ 50 mn $. Pozisyon ≤ 20 günlük ortalama dolar hacminin %1'i [Ö].
- ADR%20 ≥ %2 [Ö]. ADR%20 = 100 × (20 günlük ortalama yüksek/düşük oranı − 1). Pozitif çarpıklık, büyük hareket edebilen hisse ister.
- Aylık oynaklık ≥ %2. Bu, satın alma/birleşme arbitrajı profilini eler (HAZ §4).
- **Önümüzdeki 10 seansta bilanço yok** (Earnings Whispers ya da şirket IR'den teyit).
- **Önümüzdeki 10 seansta bilanço dışı ikili olay yok** (KT1 #5). Kontrol: şirket IR takvimi ve haber akışı.
  - FDA PDUFA tarihi ya da danışma kurulu.
  - Büyük tıp kongresinde pivot veri (ör. LLY, ObesityWeek 14–17.11).
  - Yatırımcı günü ya da kılavuz toplantısı.
  - CMS oran duyurusu, mahkeme ya da düzenleyici karar.
- **Faz 1'de yönetilen sağlık evren dışıdır** (CNC tipi sağlık planı şirketleri; KT1 #5). Tek günlük ikili hareketleri sık (CNC 4.11'de +%12,6; HAZ §4).
- Hisse izinli bir kümede (§4.3), yasaklı kümede değil (§4.6).

**Eleme filtresi (alfa değil, kötü kuyruğu dışarıda bırakmak için):**
- (a) Son çeyrekte hisse başı kâr ve gelir beklentiyi aştı.
- (b) Son bilançodan sonraki 3 seansın getirisi ≥ SPY'ninki.
- Kaynak: Nasdaq.com "Earnings" sayfası.
- Dayanak: KEN §4 (EarningsStreak, RevenueSurprise ve AnnouncementReturn likit evrende uzun-kısa %0,24–0,37/ay).
- **Dürüst not:** Bu sinyallerin sadece-uzun üst portföyü 2010–25'te VW piyasayı geçmedi (TEST §0 #8, §6.4). C'deki 90 günlük revizyon maddesi iş yükü yüzünden çıkarıldı (HU §3 C4).

**Ortak stop şartı (S1 ve S2):** Tetikten yapısal stopa mesafe **1,0–2,0 × ATR14 ve ≤ %8** olmalı. Bu aralığın dışındaysa işlem yok.
- Gerekçe 1: Uygulayıcı tavanları ≤ 1 ATR (Kullamägi), %7–8 (IBD), ≤ %10 (Minervini) (PROF §1.3 #3 [P]).
- Gerekçe 2: Kapanış bazlı mekanik kopyada 1 ATR'nin altındaki stop kötü sonuç verdi (VP A12 [K]).
- A'nın 0,6 ATR'lik ve C'nin 0,75 ATR'lik tabanı bu yüzden 1,0 ATR'ye çekildi.

### 3.2 S1: Baz kırılımı (VCP / düz baz), gün sonu uyarlaması

| Adım | Kural | Dayanak |
|---|---|---|
| Ön koşul | Trend şablonu TT = 1: kapanış > 50 > 150 > 200 GHO; 200 GHO 21 seans öncesinden yüksek; kapanış ≥ 1,3 × 52 hafta dibi ve ≥ 0,75 × 52 hafta zirvesi. RS çizgisi / 52 haftalık zirvesi ≥ 0,97. Kapanış 52 hafta zirvesinin en çok %10 altında (≤ %5 tercih). Son 1 ayın getirisi < +%25 ve son 3 ayın < +%40; aksi halde "uzamış" sayılır ve yalnız S2 ile girilir | HAZ §5a; PINE; DLG §0.5: ani sıçramadan sonra 1–3 ay medyan −%4/−%6 |
| Baz | En az 15 seans. Derinlik (tepeden dibe) **SARI'da ≤ %15, YEŞİL'de ≤ %25 (her fazda)** (KT2 küçük #11). Son daralma ≤ %10 ve ≤ 2,5 × ATR14. Son 5 seansın toplam aralığı ≤ 2 × ATR14. 10 günlük ortalama hacim < 50 günlük ortalama hacim | Minervini VCP, IBD baz [P] (PROF §1.1) |
| Pivot | Son daralmanın en yüksek seviyesi. Listeye girmek için kapanış pivotun en çok %5 altında olmalı | [P] |
| Giriş emri | **BUY STOP-LIMIT, DAY, yalnız normal seans.** Tetik = pivot × 1,001 (en az +0,05 $). Limit = min(tetik × 1,01; tetik + 0,3 × ATR14). Her gün akşam emir bloğunda yeniden girilir, en çok 5 seans. Kapanış pivot × 1,05'in üstündeyse kurulum iptal edilir ve "kaçan" yazılır; kovalanmaz | IBD alım bölgesi pivot +%5 [P]. Ekran olmadığı için limit daha sıkı [Ö]. Momentum getirisinin çoğu gece oluşur, bu yüzden geceyi taşıyan pozisyon tercih edilir (KEN §3, Lou-Polk-Skouras) |
| İlk stop | Dolumla birlikte ekli **GTC SELL STOP (piyasa)**, yalnız normal seansta tetiklenir. Seviye = son daralmanın dibi − %0,1. Mesafe §3.1'deki ortak şartı sağlamalı | PROF §1.3 #3; VP A12 |
| Başarısız kırılım | Dolumdan sonraki ilk 3 seansta kapanış < pivot − 0,5 × ATR14 → ertesi açılışta MOO ile tamamen çık | Minervini'de ortalama kayıp tavanın yarısı [P] (PROF §1.3 #3) [Ö] |

**Dürüst beklenti (S1, EOD, maliyet sonrası) [Ö]:**
- İsabet %25–40; ortalama kazanç 2–3,5R; ortalama kayıp −1,0 ile −1,2R (gap'ler nedeniyle).
- E[R] **−0,2R ile +0,4R** arası, merkez +0,1R. Yılda 40–70 işlem.
- En yakın kanıt: mekanik Kullamägi kopyası 2008–25'te %19 CAGR ve −%21 MDD verdi. Ama maliyet ve hayatta kalma yanlılığı raporlanmadı (VP A12 [K]).

### 3.3 S2: Yükselen 10/20 GHO'ya geri çekilme

| Adım | Kural | Dayanak |
|---|---|---|
| Lider | TT = 1. RS/52H ≥ 0,95. Son 20–40 seansta ≥ +%20 itki ya da son 6 haftada bir S1 kırılımı veya bilanço olayı. 10 GHO > 20 GHO > 50 GHO; 20 GHO 5 seans öncesinden yüksek | Luk: yükselen ortalamaya ilk geri çekilme; Kell: EMA crossback [P] (PROF §1.1) |
| Geri çekilme | Son tepeden 2–8 seans. Derinlik %5–15 ve ≤ 2,5 × ATR14. Düşüş günlerinde hacim 50 günlük ortalamanın altında | [P] |
| Sinyal günü | Gün dibi ≤ 10 GHO + 0,25 × ATR14 (10 ya da 20 GHO bölgesine değmiş). Kapanış ≥ 20 GHO ve gün aralığının ortasının üstünde | Raschke "Holy Grail" mantığı [P] (PROF §1.1) |
| Giriş emri | Ertesi seans **BUY STOP-LIMIT, DAY**. Tetik = sinyal günü tepesi × 1,001. Limit = min(tetik × 1,01; tetik + 0,3 × ATR14). 2 seans geçerli | [P] |
| İlk stop | Ekli GTC SELL STOP = min(sinyal günü dibi; 20 GHO − 0,25 × ATR14) − %0,1. Mesafe §3.1'deki ortak şartı sağlamalı | Luk'un gün içi stopu %1–4; EOD'de daha geniş [P]; VP A12 |
| Başarısız işlem | İlk 3 seansta kapanış < sinyal günü dibi → ertesi açılışta MOO ile çık | [Ö] |

**Dürüst beklenti (S2) [Ö]:**
- İsabet %30–45; kazanç 2–3R; E[R] −0,1R ile +0,3R arası. Yılda 30–50 işlem.
- Luk'un 104/319 istatistiği **DOĞRULANAMADI** (VA #15). Gün içi stop yerine EOD stop kullanıldığı için kazanç R'ı düşer.

### 3.4 Boyut

**Formül:**
- Adet = ⌊(E × risk%) / (**limit − stop**)⌋.
- Boyut tetiğe göre değil, limite göre hesaplanır. Gap'te limit fiyatından dolum olursa gerçek risk 1R'yi aşmasın diye (HU §2.2: tetiğe göre boyutta risk ~1,27R'ye çıkıyordu).

**Tavanlar (hepsi kontrol edilir):**
- **Pozisyon tutarı ≤ E'nin %7,5'i (Faz 1–2), ≤ %10 (Faz 3)** (KT1 #5). Aşama 1'de %7,5 E, NLV'nin %18,75'i eder; Minervini'nin %20–25'iyle uyumlu (PROF §3.1).
  - Faz 1'de tavan yalnız stop < %3,3 iken bağlar; o zaman işlem 1R'nin altında riskle açılır.
  - Faz 2'de (%0,5 risk) tavan stop < %6,7 iken bağlar. Bu bilinçli bir seçim: −%40'lık tek isim gap'i en çok E'nin −%3'ü olur.
- IBKR emir değeri ön ayarı aynı tavanla kurulur (§6.2).
- Gap-ayarlı risk = adet × max(limit − stop; 1,5 × ATR14). Bu değer ≤ 1,25 × (E × risk%) olmalı.
- Küme, toplam ısı, brüt maruziyet, en kötü hafta ve bekleyen emir tavanları (§5, §6.2).

**Alt lotlar (KT1 #10):**
- Her pozisyon iki alt lot olarak yönetilir. Lot A = yuvarla(adet/2) SARI'da, yuvarla(adet/3) YEŞİL'de; lot B = kalan.
- Bölme giriş emrinde yapılmaz; dolumdan sonraki ilk kapanış bloğunda stop üzerinde yapılır (§6.2).
- Neden: Girişte iki ayrı ana emir, fazla adayların OCA grubuyla çakışır; OCA ikinci alt lotu iptal eder. Stoplar yalnız normal seansta tetiklendiği için seans dışında bölmek korumasız an yaratmaz.

**R tanımı:**
- 1R = (dolum − ilk stop) × adet.
- Gerçekleşen R = net kâr/zarar (komisyon dahil) / 1R $.

**Çalışılmış örnek 1 (S1):**
- Pivot 100,00 $, ATR14 3,20 $, yapısal stop 94,40 $.
- Tetik 100,10 $. Limit = min(101,10; 100,10 + 0,96 = 101,06) = 101,06 $.
- Tetikten stop mesafesi 5,70 $ = %5,7 = 1,78 ATR: şart sağlanıyor.
- Boyut için hisse başı risk 6,66 $.

| %0,25 risk | E = 50k | E = 250k | E = 1m |
|---|---|---|---|
| 1R bütçesi | 125 $ | 625 $ | 2.500 $ |
| Adet | 18 | 93 | 375 |
| Alt lotlar A / B: SARI (YEŞİL) | 9 / 9 (6 / 12) | 47 / 46 (31 / 62) | 188 / 187 (125 / 250) |
| Pozisyon (limitte) / E'nin %'si / aşama 1 NLV'nin %'si | 1.819 $ / %3,6 / %9,1 | 9.399 $ / %3,8 / %9,4 | 37.898 $ / %3,8 / %9,5 |
| Risk: limitte dolum / tetikte dolum | 120 $ / 103 $ | 619 $ / 530 $ | 2.498 $ / 2.138 $ |
| Gap-ayarlı risk (E'nin %'si) | %0,24 | %0,25 | %0,25 |
| IBKR gidiş-dönüş komisyonu (0,005 $/adet, en az 1 $) | 2 $ = 0,016R | 2 $ = 0,003R | 3,75 $ = 0,002R |
| Gedik gidiş-dönüş (lot başı 0,05 $, en az 1 $) | 2 $ = 0,016R | 9,30 $ = 0,015R | 37,50 $ = 0,015R |
| İş TMI gidiş-dönüş komisyonu (%0,25/yön) | 9 $ = 0,07R | 47 $ = 0,08R | 189 $ = 0,08R |

**Çalışılmış örnek 2 (S2):**
- Sinyal günü tepesi 50,00 $, ATR14 1,40 $. Stop = min(47,90; 48,20 − 0,35) − %0,1 ≈ 47,80 $.
- Tetik 50,05 $. Mesafe 2,25 $ = %4,5 = 1,61 ATR: şart sağlanıyor.
- Limit = min(50,55; 50,47) = 50,47 $. Boyut için hisse başı risk 2,67 $.
- Adet: 46 / 234 / 936. Pozisyon 2.322 / 11.810 / 47.240 $, yani E'nin ~%4,7'si ve aşama 1 NLV'nin ~%11,7'si.

### 3.5 Ortak çıkış kuralları

Çıkış kararları kapanış verisiyle verilir. Emir **kapanış bloğunda** (gece 00:30–01:00 ya da sabah 08:00–09:00) girilir ve ertesi açılışta çalışır (KT1 #9). Akşam emir bloğu (16:45–17:15) BIST ve VİOP seansıyla çakıştığı için çıkışlar ona bağlanmaz.

| Kural | Uygulama | Dayanak |
|---|---|---|
| **Kısmi kâr** | İlk gerçekleşen koşulda: (a) kapanış ≥ dolum + 2R, ya da (b) 4. seans kapanışı ≥ dolum + 1R. Ertesi açılışta **lot A için MOO** (SARI'da 1/2, YEŞİL'de 1/3), lot A'nın stopuyla aynı OCA grubunda. Lot B'nin stopu **dolum fiyatına** (başabaş) çekilir | Kullamägi: 3–5 günde 1/3–1/2 [P] (VP A1; PROF §1.3 #7–8, §3.5 #9) |
| Başabaş | Kısmi satış olmasa da kapanış ≥ +1,5R olunca bütün stoplar dolum fiyatına çekilir | [P] (PROF §1.3 #7) |
| **İz süren çıkış** | Kalan pozisyonda ilk kapanış < 10 GHO (hızlı hisse: ADR%20 ≥ %4 ya da girişten sonraki 10 seansta ≥ +3R) veya kapanış < 20 GHO (diğerleri) → ertesi açılışta MOO ile tamamen çık | Kullamägi 10/20 GHO [P]; VP A12'deki mekanik kopyada da MA trail var |
| Haftalık acil stop | Her Cuma kapanışından sonra (Cumartesi) bütün stoplar, son 10 seansın en düşük dibinin %0,5 altına yükseltilir (yükselme varsa). **Stop asla aşağı çekilmez** | [Ö] (A §2.4) |
| Zaman stopu | 10. seans kapanışında kâr < +1R **ve** son 5 seansın hiçbirinde girişten beri en yüksek kapanış oluşmamışsa → ertesi açılışta MOO ile çık (KT2 küçük #17) | [Ö]. Isıyı boşaltır (PROF §3.5 #9) |
| Aşırı koşu | Kapanış girişten +%100 ya da fazla ise: ertesi açılışta **en az 1/2 MOO ile satılır**. Kalan için çıkış: kapanış ≤ girişten beri en yüksek kapanış × 0,90 ya da kapanış < 10 GHO → ertesi açılışta MOO | **[H, sektör düzeyi]**: 24 aylık GSY olayları; %10–15 iz süren stop en kötü sonucu −%69'dan −%22'ye çekiyor (DLG §5; VD U8). Aynı tabloda "hemen çık" tutmayı ve stopları domine ediyor (ortalama +%9,7, kayıp oranı %0; VD U9). Bu yüzden yarısı hemen satılır (KT2 küçük #7) |
| Yeniden giriş | Stop olan hisseye yeni pivot oluşursa yeniden girilebilir. Aynı bazda en çok 2 deneme | [Ö] |

**Emir hijyeni** (KT1 #10; KT2 K-1; HU §2.2):
- Bekleyen kısmi satış limiti **kullanılmaz** (tam adetli stopla birlikte dolabilir).
- **Her satış emri** (kısmi MOO, tam çıkış MOO, bilanço MOC), satılan lotun stopuyla **aynı OCA grubunda** girilir. Ayar: "Cancel all remaining orders with block". Biri dolunca diğeri iptal olur. MOO reddedilirse stop yerinde kalır, lot korumasız kalmaz.
- **Yedek 1:** Stop emrinin tipi MOO'ya çevrilir. Tek emir olduğu için çift satış olamaz.
- **Yedek 2:** Stop iptal edilir, MOO girilir. Nakit hesap fazla satışı reddeder, açığa satış oluşmaz. Ertesi kapanış bloğundaki stop mutabakatı stopsuz kalan lotu yakalar.
- Hangi yöntemin çalıştığı Pazartesi'den itibaren 1 adetlik testlerle belirlenir (§6.2). Sonuç günlüğe yazılır ve bundan sonra hep o yöntem kullanılır.

### 3.6 Bilanço

- Bilançoya ≤ 10 seans kalmışsa yeni giriş yok. İkili olaylar için de aynı kural geçerli (§3.1).
- **Faz 1'de açık pozisyon bilançoya taşınmaz.** Açıklamadan önceki son seansta çıkılır.
  - Kapanış sonrası (AMC) açıklamada son seans açıklama günüdür.
  - Açılış öncesi (BMO) açıklamada son seans bir önceki gündür.
- **Birincil yöntem:** son seansın kapanışında **SELL MOC**. Emir, son seanstan önceki kapanış bloğunda girilir ve pozisyonun stop(lar)ıyla **aynı OCA grubuna** konur. Böylece stop gün içinde tetiklenirse MOC iptal olur (KT2 K-1).
- **Yedek (MOC + OCA testi geçmezse):** Karar son seanstan bir önceki kapanışta verilir; çıkış son seansın açılışında MOO ile yapılır. Bu da stopla aynı OCA'da girilir.
- **Faz 2+ istisnası:** kısmi satış yapılmış ve kâr ≥ +2R ise pozisyon taşınabilir. Şart: boyut, 2 × implied move büyüklüğünde bir gap ≤ 1R kaybettirecek kadar küçültülmeli ("earnings size").
- Dayanak: PROF §1.3 #9, §3.5 #5; PRA §3.6 #4 (bilanço öncesi taşımak negatif çarpık).

### 3.7 Piramit (yalnız kazanana)

- **Şartlar:** Faz 2+ ve YEŞİL rejim. Pozisyonun kapanış kârı ≥ +1,5R. Yeni geçerli bir S2 sinyali ya da yeni S1 bazı var. Bilançoya ve ikili olaya > 10 seans var.
- **Ek boyutu:** 1. ek ilk riskin 0,5'i, 2. ek 0,33'ü. En çok 2 ek.
- **Stop:** ekin kendi stopu. Ana lotun stopu en az başabaşa çekilir. Ek sonrası toplam gap-ayarlı risk ≤ ilk 1R. Ek sonrası pozisyon tutarı tek pozisyon tavanını aşamaz.
- Her ek, bekleyen emir tavanında ve günlük giriş hakkında bir giriş sayılır.
- **Yasak:** zarardaki pozisyona ekleme; SARI'da ekleme.
- **Kayıt:** her ek ayrı satır.
- Dayanak: IBD %50/30/20; Turtle ½N [P] (PROF §1.3 #6).

### 3.8 Gölge kollar

Gölge işlemler canlı kapılara **sayılmaz**. Kâğıt üzerinde dolum varsayımı: dolum = max(tetik, açılış); limit aşıldıysa "dolmadı".

**G1: Bilanço gap'i (episodic pivot), 2.–5. gün** (A §2.2):
- **1. gün:** bilanço ya da büyük haberle açılış gap'i ≥ +%8. Hacim ≥ 3 × 50 günlük ortalama. Gün dolar hacmi ≥ 50 mn $. Kapanış gün aralığının üst yarısında ve ≥ açılış × 0,98.
- **Kalite:** gelir beklentiyi aşmış ve kılavuz yükselmiş. Gap öncesi 3 ayın getirisi ≤ +%30. Dayanak: Savor (2012), analist bilgisiyle desteklenen şok drift ediyor (KIM §5.1).
- **Giriş:** 2.–5. seans buy-stop-limit; tetik = olaydan beri en yüksek × 1,001, limit +%1,5.
- **Stop:** 1. gün dibi − %0,1. Mesafe ≤ %10 ve ≤ 2 × ATR14.
- **Tarama (KT2 Ö-4):** Kapanış bloğunda finviz `earningsdate_prevdays5` + `ta_gap_u8` + `sh_relvol_o3` + `sh_price_o20` (+ `cap_midover`). Gap ve RVOL filtreleri son tamamlanan seansa bakar; 1. gün = son seans olur. URL RUTİN §1 #7'de. Gün içi tarama yok.
  - Önceki sürümdeki `earningsdate_yesterdayafter` / `todaybefore` filtreleri seans içi kullanım içindi (HAZ §5b). Sabah 09:00 TSİ ET'de gece 01:00'dır; bu filtreler gap'i henüz oluşmamış ya da açıklanmamış bilançoları seçer. Pazartesi sabahı ise "dün" Pazar'dır ve filtre boş döner.
- **Bugünkü adaylar:** U (5.11 BMO), EW (4.11 AMC → 5.11 1. gün), SN (4.11 BMO), BDX (5.11 BMO). 1. gün kriterleri teyit edilmeli.

**G2: VIX panik çözülmesi** (C §2.3):
- **Kurulma:** VIX kapanışı > 25 ve VIX/VIX3M > 1,00 olan gün; 10 seans geçerli. **05.11'den beri kurulu.**
- **Tetik:** kuruluyken VIX/VIX3M'nin ilk kez < 0,95 kapanması.
- **Gölge pozisyon:** ertesi gün SPY, kapanış × 1,007 limit; 40. seansta çıkış. Stop max(%4; 2,5 × ATR14).
- **Ölçüt:** aynı tarihli koşulsuz 40 günlük SPY getirisine göre fark.
- **Rejim bilgisi:** G2 tetiği KIRMIZI'dan çıkış sürecinin işaretidir. Tek başına SARI açmaz.

**G3 Insider:** ertelendi. Ocak 2027'de veri kaynağı (openinsider + EDGAR Form 4) erişilebilir ve iş yükü kabul edilebilirse hipotez kartıyla gölgede başlatılır.

Gölge kolların canlıya alınma şartları §8.4'te.

### 3.9 Opsiyon

Opsiyon alımına yalnız **aşağıdakilerin tümü** sağlanırsa izin var (C §2.4):
1. Faz ≥ 2.
2. Rejim YEŞİL.
3. VIX < 20 ve VIX/VIX3M < 0,90.
4. Hissenin IV30'u 52 haftalık aralığının alt %30'unda ve IV30 ≤ HV20.
5. Opsiyonun ömründe bilanço yok.
6. Vade 45–90 gün, delta 0,55–0,70.
7. ATM spread'i ≤ mid'in %5'i; açık pozisyon (OI) ≥ 500.
8. Ödenen prim ≤ 1R ve ısıya sayılır.
9. Emir mid'den limit.

Dayanak: VP A6 (straddle −%3/hafta, piyango call −%35/hafta [D]), A8 (Goyal-Saretto yönü); PROF §0.6, §2.3.

**Teknik kilitler (KT1 #2):**
- IBKR'de **opsiyon işlem izni Faz 2 kapısına kadar istenmez.** VİOP tecrübesi başvuruda beyan edilir (ileride izin kolay alınsın diye), ama izin talep edilmez. Nakit hesapta uzun call/put alımı seviye 1–3 ile mümkündür (HAZ §1.2); spread gerekmiyor.
- Midas'ta call/put alımı açık (HAZ §1.2). Bu yüzden Midas'ta ≤ 500 $ test parası dışında bakiye tutulmaz (§6.1).
- Faz 1'de herhangi bir opsiyon alımı **kritik ihlaldir** (DUR-6a).
- **Bugün tamamen kapalı** (VIX 28,2; oran 1,10).

### 3.10 Bu planda olmayanlar

- **Kaldıraçlı endeks ya da ETF:**
  - 3x NDX + 200 GHO 2000–02'de −%89 yaptı.
  - Filtre 2010 sonrası getiriyi kesti (TEST §0 #1–2; VA §2.1).
  - B'nin çekirdeği 2010–26'da %13,8 getirdi; 1x al-tut %14,1 (HK B2).
- **Sektör ETF rotasyon kolu:** 2010 sonrası risk-ayarlı olarak piyasa düzeyinde (VA §2.2; VD U3–U4). Swing ufkunda kenarı yok: 40 varyantın 40'ı negatif (VD U7). Küme sıralaması yalnız filtre (§4.3).
- **Kısa vadeli reversal:** 2010'dan beri ~0 (TEST §0 #9).
- **Açığa satış:** ayı rallileri short'ları ezer (VA #27). Nakit hesapta zaten mümkün değil.
- **Margin:** faiz %5,38 ve Türkiye'de indirilemez (VC #16; VC #10). Nakit hesapta borç oluşmaz.
- **AI kümesinde dip alımı** (§4.6).

---

## 4. Evren, kümeler, izleme listesi ve adaylar

### 4.1 Taramalar

| Tarama | Ne zaman (TSİ) | Ayar |
|---|---|---|
| (a) Trend şablonu + RS | Cumartesi (tam); kapanış bloğunda liste güncelleme | **50k $:** HAZ §5a'daki finviz sıkı (6.11'de 86 sonuç) ve geniş (412 sonuç) URL'leri + TradingView ücretsiz standart tarayıcı. Kısa listede 52H zirve/dip, 150 GHO ve RS koşulları grafikte `ABD_RJ` ile elle kontrol edilir. **Pine Screener (`TT_RS_EP_Screen`) yalnız TradingView Premium'da** (KT2 Ö-2); en erken 250k $'da kullanılır: `TT = 1`, `RS line / 52w max ≥ 0,97`, `Dist to 52wH ≥ −10`, `50d $Vol ≥ 20`; `RS raw` azalan |
| (b) Bilanço gap'i (yalnız G1) | Kapanış bloğu | finviz `earningsdate_prevdays5`, `ta_gap_u8`, `sh_relvol_o3`, `sh_price_o20`, `cap_midover` (KT2 Ö-4). Kapanış üst yarıda ve dolar hacmi ≥ 50 mn $ elle kontrol |
| (c) Küme/ETF skoru | Ayın son hafta sonu (ilki 28–29.11) | HAZ §5c: skor = 0,2·(1A − SPY) + 0,4·(3A − SPY) + 0,4·(6A − SPY); fiyat > 50 GHO |
| (d) Endüstri grupları | Her Cumartesi | Finviz grupları, 3 aylık sıralama (HAZ §3). İlk 10'a yeni giren ve 1 aylık getirisi pozitif grup aday kümedir |
| (e) Küme korelasyonu | **07–08.11 (ilk girişten önce)**, sonra ayın son hafta sonu | Küme içi isimler ve ölçüt ETF'ler arasında 60 günlük getiri korelasyonu: `ABD_RJ` korelasyon satırı ya da TradingView "Correlation Coefficient" (60) (KT1 #8) |

### 4.2 Kümeler (Kasım 2026 başlangıç haritası)

**Kurallar:**
- Aynı anlatıya bağlı ya da 60 günlük getiri korelasyonu ≥ 0,6 olan hisseler tek kümedir (PROF §3.5 #2).
- Korelasyon ilk kez 07–08.11'de, sonra her ayın son hafta sonunda ölçülür.
- Gerekçe: ρ = 0,6–0,8 iken aynı kümedeki 5 pozisyon yalnız 1,19–1,47 bağımsız bahis eder (SEY §3.6). Kümelenme, aynı beklentide kuyruk riskini ~%35–40 büyütür (PROF §3.3).

| Küme | İsimler (HAZ §4) | Ölçüt ETF | Not |
|---|---|---|---|
| **SAĞLIK süper-kümesi** (K1 medtech, K2 ilaç/biyotek, K3 sağlık hizmeti) | MDT, EW, BDX, GEHC, TMO, IDXX / LLY, REGN, RPRX / EHC | XLV, IHI, PPH, IBB, IHF | Korelasyon ölçülene kadar **tek küme**. Faz 1 ısısı ≤ %0,75. **CNC (yönetilen sağlık) Faz 1'de evren dışı** (§3.1) |
| K4 Borsalar / finansal veri | CBOE, CME, TW (+ VRSK, FDS) | XLF | CBOE oynaklıktan fayda sağlıyor; VIX düşerse geride kalabilir |
| K5 Sigorta / broker | AJG, MRSH, ACGL, BRK-B (+ AON, RLI) | — | K4 ile ilişkili: K4+K5 toplam ısısı ≤ %1,25 (Faz 1) |
| **Faiz duyarlı savunmacı süper-küme** (K6 temel tüketim / indirim, K7 atık / su, K10 REIT) | BJ (KDP izinsiz; §4.3) / RSG, VLTO, AWK / CCI, PSA | XLP, XLRE | Aynı faiz faktörünü taşıyorlar; 10.11 CPI ve %4,84–4,90'lık 10 yıllık getiri bu riski canlı tutuyor. Korelasyon ölçülene kadar **tek küme**, ısı ≤ %0,75 (KT1 #8). K7/K10'da ADR%20 ≥ %2 şartını kontrol et |
| K8 Konaklama / tüketici | MAR, HLT, SN, HAS, EBAY | XRT | Tetik FTD ya da S&P 10 > 20 |
| K9 Dikey yazılım | ROP, MANH, U, GEN | IGV (zayıf) | Küme izni teyitsiz (§4.3). NDX 10 > 20 tek başına yalnız bu kümeyi açar |
| K11 Mega-cap teknoloji | AAPL | QQQ | NDX rejimine bağlı; YEŞİL'i bekler |

**Faktör uyarısı:** SARI'da açılacak pozisyonların çoğu savunmacı ve düşük betalı olacak; bu da kendi başına bir faktör kümesidir.
- Büyümeye sert dönüşte savunmacılar geride kalabilir. 2009'da kazanan desil +%8, kaybeden +%163 yaptı (VA #27).
- KT1 #8 testi (FF49 endüstri vekilleri, NDX'in ≥ %10 düşüşünden sonraki 10 > 20 kesişmesi; sonraki 20 seans) [H]: 1986–2026'da 113 olayda savunmacı sepetin piyasaya göre farkı +%0,02. **2010 sonrası 35 olayda −%0,66; olayların %60'ı negatif.** Kanıt zayıf, ama yönü tutarlı. Savunmacı kümelerde NDX tetiğinin kullanılmamasının nedeni bu.
- Sınırı toplam ısı tavanı koyar.

### 4.3 Küme izni (aylık, ayın son hafta sonu)

Küme şu iki koşuldan biri sağlanırsa izinlidir:
- (a) Temsilci ETF, HAZ §5c skorunda ilk 5'te ve 50 GHO'nun üstünde.
- (b) Finviz endüstri grubu 3 aylık performansta ilk %20'de.

Ara durum yoktur: koşul ya sağlanır ya sağlanmaz. Süper-kümede izin alt küme düzeyinde verilir, ısı tavanı süper-küme düzeyinde uygulanır.

**Dürüst not:** Bu adım bir kenar değil, kırık kümelerden uzak durma disiplini (VA §2.2; VD U4, U7; DLG §0.4). Getiri küme içindeki hisse kurulumlarından gelmek zorunda.

**Bugünkü izin durumu (HAZ §3 ve §5c, 6.11 sabahı):**

| Küme | Durum | Dayanak |
|---|---|---|
| Sağlık | İzinli | XLV #1, IHI #2, PPH #3, IBB #4, IHF #5 |
| Borsalar / finansal veri | İzinli | Finviz 3 ay +%12,4 |
| Sigorta | İzinli | Reasürans grubu üstte; XLF #7 |
| Konaklama | İzinli | 3 ay +%17,5 |
| Atık | İzinli | 1 ay +%12,1 |
| Temel tüketim | **Yalnız indirim mağazaları (BJ) izinli.** XLP skor sıralamasında 6., yani (a) sağlanmıyor; (b) yalnız indirim mağazaları grubunda sağlanıyor. **KDP izinsiz** (KT2 küçük #12). BJ'nin bilançosu 20.11; bu yüzden kümede 25.11'den önce giriş yok | HAZ §3, §5c |
| Dikey yazılım, REIT | **Teyit:** Cumartesi grup sıralamasında ilk %20'de mi? | — |
| Mega-cap teknoloji | YEŞİL'e kadar yok | — |

### 4.4 Küme başına isim seçimi

1. (a) taramasının sonuçları kümelere dağıtılır. Küme içinde `RS raw`'a göre (Pine Screener yoksa 6 aylık getiriye göre) sıralanır.
2. Evren ve eleme filtresini geçen **ilk 5** isim izleme listesine alınır.
3. Her isme etiket verilir: S1 (baz hazır, pivot ≤ %3 uzakta), S2 (geri çekilme sürüyor) ya da "uzamış / bekle".
4. Her isim için yazılır: pivot, tetik, limit, stop, stop %, stop/ATR, ADR%20, adet (limite göre), bilanço tarihi ve ikili olay tarihi. Stop şartını sağlamayan isim kurulum listesine girmez.
5. Tetiklenince işleme alınacak sayı:
   - SARI'da kümenin yalnız 1. sırası; **yakın bölgede bütün listeden yalnız 1 isim**.
   - YEŞİL'de ilk 3'e kadar (Faz 1'de küme ısısı izin verdiği kadar).
   - Diğerleri yedek. Bekleyen emir sayısı ve tutarı §6.2'deki tavana tabidir.
6. Öncelik sırası: RS sırası, sonra sıkılık (son 5 seansın aralığı / ATR), sonra pivota yakınlık.

### 4.5 Güncel adaylar (5.11 kapanışı; öneri değil)

Fiyat ve 52H uzaklığı HAZ §4'ten.
- **Bugün hiçbiri alınamaz:** rejim KIRMIZI; en erken pilot 16.11.
- Tablo, rejim SARI olduğunda hangi ismin tetik listesine girebileceğini gösterir.
- Grafik şartları (baz, pivot, ATR, eleme filtresi) bu dosyada **doğrulanmadı**; Cumartesi kontrol edilmeli.

| Sınıf | İsim (fiyat; 52H'ye uzaklık; son bilanço) | Ne yapılır |
|---|---|---|
| **Nitelikli aday:** grafik teyidiyle S1/S2 kurulumu olabilir | BDX (212,52; −%1,1; 5.11 b), EHC (141,27; −%1,5; 28.10 a), TMO (677,95; −%4,8; 21.10 b), RPRX (67,24; −%3,6; 4.11 b), TW (127,56; −%1,1; 29.10 b), CME (307,24; −%4,8; 21.10 b), MRSH (209,43; −%2,1; 15.10 b), ACGL (110,57; −%2,7; 27.10 a), HLT (369,36; −%3,1; 27.10 b), MAR (417,28; −%3,7; 2.11 b), SN (217,50; −%3,6; 4.11 b), EBAY (122,94; −%3,8; 28.10 a), MANH (255,17; −%3,2; 27.10 a) | Pivot, stop ve ATR'yi çiz. Sağlık isimleri tek küme: SARI'da yalnız 1 sağlık pozisyonu |
| **ADR şartı kontrol edilecek** (düşük oynaklık olabilir) | AWK (152,42; −%0,8), RSG (249,42; −%2,0), VLTO (115,86; −%2,7), PSA (340,50; −%1,6) | ADR%20 < %2 ise dışarı. Hepsi faiz duyarlı süper-kümede |
| **Uzamış:** son 1 ayda > +%25; yalnız S2 beklenir | AJG (1A +%26,9), CBOE (+%25,4), GEHC (+%29,5; 52H'ye −%6,7), HAS (+%31,7), ROP (+%36,9), GEN (+%36,7), CCI (+%31,8) | 10/20 GHO'ya geri çekilme beklenir; kovalanmaz (DLG §0.5) |
| **Bilanço bekle** | **MDT: 24.11 BMO** (Medtronic IR; KT2) → 10.11'den itibaren yeni giriş yok. **BRK-B: bilanço Cumartesi 07.11, 07:00 CT** (16:00 TSİ; Berkshire duyurusu; KT2). Pazartesi 9.11 ilk tepki seansı; eleme filtresi (b) için 3 seans gerekir, yani en erken 11.11 kapanışı. **BJ: 20.11 BMO** | Bilançodan önce giriş yok |
| **Olay / baz yok** | **LLY** (52H'ye −%7,1): ObesityWeek 14–17.11 ikili olaydır (DLG §6.2); 17.11'e kadar giriş yok, sonra yeni baz gerekir. REGN (−%9,8) | Yeni baz oluşursa S1 |
| **İzinsiz / evren dışı** | KDP (temel tüketim izni yok), CNC (yönetilen sağlık, Faz 1'de evren dışı) | — |
| **G1 gölge** | U, EW, SN, BDX (1. gün kriterleri teyit edilecek). IDXX: 2.11 olayının 5. günü 6.11; pencere bugünkü seansla kapanıyor (KT2 küçük #15); S2 adayı | Yalnız gölge günlüğe |
| **YEŞİL bekle** | AAPL | NDX rejimine bağlı |
| **Dışarıda** | AI çip, bellek, donanım, güç, veri merkezi (NVDA, AMD, MU, SNDK, MRVL, VRT, GEV, VST, CEG...); neocloud ve madenciler (CRWV, NBIS, IREN); nükleer/SMR; kuantum; kripto; drone/uzay; enerji (50 GHO kırıldı); altın madencileri; savunma; APP; NET | HAZ §4; DLG §0.7–0.8; §4.6 |

### 4.6 Kırık temalara dönüş kuralı

**AI kompleksi tek kümedir:** yarı iletken, bellek, donanım, elektrik ekipmanı/güç, veri merkezi altyapısı, neocloud. Chips–ElcEq korelasyonu 0,72 (PROF §3.2). Bu rakam ajanın kendi hesabı, tekrarlanmadı (VP A14 [K]); yön makul.

Dönüş iki adımda yapılır (A §4.5; DLG §7.4):
- **Pilot:** üç şart birlikte.
  - SMH 10 seans boyunca 50 GHO'nun üstünde kapanmalı.
  - SMH/SPY oranı 3 aylık zirve yapmalı.
  - Hisse yeni bir Stage 2 bazından (≥ 5 hafta) S1 vermeli.
  - Pilot yalnız YEŞİL rejimde açılır; küme ısısı tavanın yarısında tutulur.
- **Tam küme ısısı:** SMH/SPY'nin 12 aylık RS zirvesi yeniden görülmeli.
- Bu kural dışında AI kümesinde giriş **kritik ihlaldir** (DUR-6a).

**Diğer kırık temalar** (nükleer, kuantum, kripto, drone/uzay, enerji, altın madencileri, savunma): kümenin RS'i yeni bir 12 aylık zirve yapmadan giriş yok (DLG §7.4).

**Donanım canlı bir GSY olayı:** tarihsel çöküş olasılığı %42–53 (DLG §0.7). Bu kümeye dönüşte iz süren stop tepeden %10 düşüşe sıkılaştırılır.

---

## 5. Risk limitleri

### 5.1 Tablo (E'nin yüzdesi; NLV karşılığı §5.4'te)

| Limit | Faz 1 (ilk 50 canlı işlem) | Faz 2 | Faz 3 | Dayanak |
|---|---|---|---|---|
| İşlem başı risk | **%0,25** | %0,50 | %0,75 (en çok %1) | PROF §3.5 #1; KIM §5.3 (risk %1'i aşınca bu yapı kırılır; VA #37) |
| **Tek pozisyon** (ve IBKR emir değeri ön ayarı) | **≤ %7,5** | ≤ %7,5 | ≤ %10 | KT1 #5; PROF §3.1 (Minervini %20–25 hesap; Kullamägi'de gece tavanı %30) |
| **Küme ısısı** | ≤ %0,75 (sağlık ve faiz duyarlı süper-kümeler dahil) | ≤ %1,5 | ≤ %1,5 (güçlü YEŞİL'de %2) | PROF §3.5 #3 |
| İlişkili kümeler (K4 + K5) | ≤ %1,25 | ≤ %2,5 | ≤ %2,5 | PROF §3.1 |
| **Toplam açık risk** (gap-ayarlı; bekleyen emirler dolmuş sayılır) | SARI %1,25 (yakın bölge %0,5) / YEŞİL %2,5 | %2,5 / %5 | %3 / %6* | PROF §3.5 #4, §1.4 (pilot ≤ %2); KT2 küçük #20 |
| Brüt maruziyet (ayrıca ≤ yerleşmiş nakit − NLV'nin %5'i) | SARI %30 / YEŞİL %40 | %40 / %60 | %50 / %95 | PRA §3.6; [Ö]; KT1 #4 |
| Günlük yeni giriş | SARI 2 (yakın bölgede toplam 1 pozisyon) / YEŞİL 3 | aynı | aynı | [Ö]; KT2 K-2 |
| **En kötü hafta tavanı:** Σ pozisyon × max(stop %; %15) | ≤ %6 | ≤ %9 | ≤ %15 | HU §2.4 [Ö]: yalnız ısıya bakmak korele gap'te 2–3 kat yanıltır |
| **Aylık devre kesici:** ayın net gerçekleşen zararı (negatifse) + açık gap-ayarlı risk | ≥ min(%6; 12R) = **%3** → ay sonuna kadar yeni giriş yok. **İki ardışık ayda tetiklenirse Kademe 3** (§5.2) | ≥ %6 | ≥ %6 | PROF §3.5 #8 (Elder); KT1 #1; KT2 küçük #20 |
| Açık pozisyon sayısı | SARI 4 / YEŞİL 8 | aynı | aynı | Kullamägi/Minervini 4–8 [P] |
| Margin, açığa satış, kaldıraçlı ürün, opsiyon | Yok (nakit hesap; opsiyon izni yok) | Opsiyon §3.9 şartlarıyla | aynı | VC #16; §3.9, §3.10 |

\* Faz 3 YEŞİL'de %6 yalnız yıl içi kâr yastığı ≥ %10 ise; değilse %5.

**İşlem riskini Faz 2'de %0,5'e çıkarmak bilinçli bir sapmadır.** SEY §5.3 #4 "12 ay ve 100 işlemden önce boyut artırılmaz" diyor.
- Bu plan **sermayeyi (E)** o kurala bağlar: E, 12 ay ve 100 işlemden önce artmaz.
- **İşlem riskini** ise 50 işlem ve t ≥ 1,0 ile %0,5'e çıkarmaya izin verir.
- Bu sapmanın bedeli küçük: E servetin %10'u olduğundan %0,5 risk servetin ≤ %0,05'i eder (HK §5 #3).

### 5.2 Düşüş merdiveni (yalnız canlı lider kolunda)

**Ölçüm:** stratejinin USD kâr/zararı (gerçekleşen + açık), E'ye oranla, zirveden ölçülür. Aylık raporda NLV'ye oranı da yazılır.

**Kalibrasyon (KT1 #1):**
- Dur eşiği planın kendi 1. yıl modelinde en büyük düşüşün %5 kötü değerine (p95) konur. SEY §5.2 #1'e göre "gerçekleşen düşüş simülasyonun p95'ini aşarsa kol durur".
- Önceki sürümde eşik −%15'ti. Bu, modelin p95'inin (−%7,4…−8,3) ~2 katı ve aşama 1'de NLV'nin −%37,5'iydi. Yani pre-mortem bandı (NLV −%15…−25 = E'nin −%6…−10'u) planı durdurmuyordu.

| Kademe | Faz 1 tetik (E'nin %'si; aşama 1'de NLV karşılığı) | Faz 2 (varsayılan) | Faz 3 (varsayılan) | Eylem |
|---|---|---|---|---|
| 1 | **−%3** (NLV −%7,5; %0,25 riskte 12R) | −%4 | −%5 | Risk × 0,5 (en az %0,125). Piramit yok |
| 2 | **−%5** (NLV −%12,5) | −%6 | −%8 | Yalnız en güçlü 2 kümede kurulum. Toplam ısı rejim tavanının yarısı |
| 3 | **−%6,5** (NLV −%16) **ya da iki ardışık ayda aylık devre kesici** | −%8 | −%11 | 10 seans yeni işlem yok. Tüm işlemlerin yazılı incelemesi |
| **Dur** | **−%8** (NLV −%20; 4.000 / 20.000 / 80.000 $) | −%10 | −%15 | **Plan durur** (§8.5 DUR-5). Pozisyonlar kendi stop kurallarıyla kapanır; yeni işlem yok. USD nakit TL'ye dönebilir. Yeniden başlamak için yeni hipotez kartı ve sıfırdan Faz 1 gerekir |
| Geri yükleme | Kaybın yarısı geri gelince | aynı | aynı | Bir kademe yukarı |

- **Faz 2–3 eşikleri** aynı ilkeyle yazıldı [Ö]. Faz kapısında gerçekleşen işlem dağılımından bootstrap ile yeniden ölçülür. Sonuç bu varsayılanlardan gevşek olamaz. Faz 3 değeri §9.4'teki merdivenli %5 kötü düşüşle (~−%15) tutarlı.

**Gerekçe ve belirsizlik:**
- %25 isabette 200 işlemde ≥ 12 ardışık kayıp olasılığı %81,6 (VA #37 [D]). Yani Kademe 1 (12R) uzun vadede büyük olasılıkla bir kez tetiklenir. Bu bir durdurma değil, risk yarılamasıdır.
- **Bu revizyondaki 1. yıl modelinde** (§9.1) Faz 1'de −%8'e ulaşma olasılığı < %1, çünkü Kademe 1 riski önce yarıya indiriyor. Bu model kalibre değil; felaket gap'ini ve davranış hatasını içermiyor. KT1'in kaba tahmini, kenarı gerçekten +0,15–0,3R olan bir sistemin yanlışlıkla durdurulma olasılığı için %3–5. Dürüst aralık **%1–5** [H].
- Merdiven %5 olasılıklı kötü düşüşü yaklaşık yarıya indirir, ama medyan getiriden ~17 puan alır (PROF §3.3, %1 riskte).
- Değer kattığı tek durum, performansın rejime bağlı olması. Momentum swing bu durumda (PROF §3.3; Kaminski-Lo).
- Sistematik bir kolda merdiven yalnız getiri alır (B §5.3, BT-B [H]). Bu planda sistematik kol yok.
- Negatif kenarı asıl yakalayan araç merdiven değil, istatistik kriterleridir (DUR-1…DUR-3).

**Kayıp serisi tek başına öldürme nedeni değildir.** %25–30 isabette 200 işlemde ≥ 10'lu seri olasılığı %84–96 (VA #37).

### 5.3 Gap riski, ikili olay ve en kötü hafta

- **Gap-ayarlı risk** = adet × max(limit − stop; 1,5 × ATR14). Bilanço penceresinde 2 × implied move (PROF §3.5 #5).
- **Stres varsayımı:** korele bir gecede −%15 gap. 5.11'de SOXX −%12, MU −%17,5, AMD −%17,3 düştü (HAZ §0).
- **Faz 1'de en kötü hafta:**
  - SARI: brüt %30 × −%15 = E'nin −%4,5'i (aşama 1'de NLV −%11,25).
  - YEŞİL: %40 × −%15 = E'nin **−%6'sı** (aşama 2'de NLV −%12). E servetin %10'uysa bu servetin −%0,6'sı.
- **Tek isim gap'i (KT1 #5):** Corpus'taki 2026 tek gün hareketleri: INTC −%30, AMD −%17,3, MU −%17,5, MNTN −%55 (KIM §6; PRA §3.6 #3).
  - %7,5 E'lik pozisyonda −%40 gap = E'nin −%3'ü (NLV −%7,5). Önceki %15 tavanında bu −%6 E, yani NLV −%15'ti.
  - 1,5 × ATR14 bu kuyruğu görmez. Onu sınırlayan tek pozisyon tavanı ve ikili olay yasağıdır.
- **Makro olay kümesi 9–11.12 (FOMC, CPI, bütçe süresi; KT1 #11):** 8.12 kapanışında gap-ayarlı ısı yeniden hesaplanır.
  - Pozisyon başına gap = max(1,5 × ATR14 × adet; 2 × S&P ima hareketi × hisse betası × pozisyon tutarı).
  - S&P ima hareketi ≈ VIX/100 × √(3/252). Örnek: VIX 20 ise ~%2,2. Beta finviz'den alınır.
  - Toplam rejim ısı tavanını aşarsa, aşan kısım için en düşük R'li pozisyon 9.12 açılışında MOO ile kapatılır (stopla aynı OCA'da).
  - Dayanak: PROF §3.5 #5'teki bilanço kuralının makro olaya uyarlaması [Ö]. VIX'ten türetme, opsiyon verisi aboneliği gerekmesin diye seçildi.
- **Bu hafta (9–13.11):** canlı pozisyon yok, yani ~0.

### 5.4 Dolar ve NLV karşılıkları

NLV sütunu aşamaya göre yazılır: SARI ve Faz 1 limitleri için aşama 1 (NLV = %40 E), YEŞİL limitleri için aşama 2 (%50 E). Merdiven ve aylık raporda iki birim birlikte yazılır (KT1 #1).

| Kalem | % E | % NLV | E = 50k $ | E = 250k $ | E = 1m $ |
|---|---|---|---|---|---|
| 1R, Faz 1 | 0,25 | 0,625 | 125 $ | 625 $ | 2.500 $ |
| 1R, Faz 2 / Faz 3 (aşama 3–4: NLV %70 / %100 E) | 0,50 / 0,75 | 0,71 / 0,75 | 250 / 375 $ | 1.250 / 1.875 $ | 5.000 / 7.500 $ |
| Tek pozisyon ve emir değeri tavanı (Faz 1–2) | 7,5 | 18,75 | 3.750 $ | 18.750 $ | 75.000 $ (ve ≤ 20 günlük dolar hacminin %1'i) |
| Küme ısısı Faz 1 | 0,75 | 1,875 | 375 $ | 1.875 $ | 7.500 $ |
| K4 + K5 toplamı Faz 1 | 1,25 | 3,125 | 625 $ | 3.125 $ | 12.500 $ |
| Toplam ısı Faz 1: SARI yakın bölge / SARI | 0,5 / 1,25 | 1,25 / 3,125 | 250 / 625 $ | 1.250 / 3.125 $ | 5.000 / 12.500 $ |
| Toplam ısı Faz 1: YEŞİL | 2,5 | 5 | 1.250 $ | 6.250 $ | 25.000 $ |
| Brüt tavan Faz 1: SARI / YEŞİL | 30 / 40 | 75 / 80 | 15k / 20k $ | 75k / 100k $ | 300k / 400k $ |
| Aylık devre kesici Faz 1 | 3 | 7,5 | 1.500 $ | 7.500 $ | 30.000 $ |
| En kötü hafta tavanı Faz 1 | 6 | 12 | 3.000 $ | 15.000 $ | 60.000 $ |
| Merdiven Faz 1: −3 / −5 / −6,5 / **dur −8** | aynı | −7,5 / −12,5 / −16,25 / **−20** | 1.500 / 2.500 / 3.250 / **4.000 $** | 7.500 / 12.500 / 16.250 / **20.000 $** | 30k / 50k / 65k / **80k $** |

---

## 6. Uygulama: aracı kurum, emir tipleri, saatler, maliyet, vergi kaydı

### 6.1 Aracı kurum

| Kurum | Rol | Süre | Maliyet | Kısıt |
|---|---|---|---|---|
| **IBKR Pro, nakit hesap (cash)** | **Ana platform.** BUY STP LMT, ekli GTC STP, MOO/MOC, OCA, GTD, nakit faizi | Açılış 1–3 iş günü + SWIFT 1–2 iş günü. **Gerçekçi ilk işlem 11–13.11** | 0,005 $/adet (en az 1 $); boş nakit faizi kademeli (§1.1) | Türk müşterinin bağlanacağı IBKR şirketi (IB LLC ya da IBIE) doğrulanmadı. Bu plan ETF almadığı için kritik değil; ETF'ler yalnız ölçüt (HAZ §1.2; VC #16 [D]) |
| **Midas** | Yalnız test; **≤ 500 $ test parası**, test bitince geri çekilir | Onay 1–2 gün | 1,5 $/işlem; kur makası yayınlanmıyor | Call/put alımı açık, teknik kilit yok (KT1 #2). Ekli GTC stoplu buy-stop-limit ve MOO 1 adetle çalışmazsa S1/S2 için hiç kullanılmaz; ekransız korumasız pozisyon açılmaz (HAZ §1.2, §7) |
| İş TMI / Garanti | Lider kolunda kullanılmaz | Mevcut müşteride birkaç gün | İş %0,25, pre/post-market'te pay başı +0,5 cent. Garanti %0,30 + %0,50 kur | Yüzdesel komisyon işlem başına ~0,07–0,2R; +0,2–0,3R'lik kenarın %25–60'ı (C §5.3; HK §4 #13) |
| Gedik | Yedek (IBKR açılamazsa) | Mevcut müşteride kısa | Lot başı 0,05 $, en az 1 $: örneklerde ~0,015–0,04R (§3.4; KT2 küçük #10) | Emir tipleri (ekli GTC stop, MOO, OCA) bu oturumda teyit edilmedi |

**Neden nakit hesap (KT1 #4; KT2 K-1, K-2, Ö-3):**
- Fazla emir, OCA miktar hatası ya da stop + MOC çift dolumu **reddedilir**; borca ya da açığa satışa dönmez. Margin tipi hesapta bunlar %5,38 faizli, Türkiye'de indirilemeyen borca ya da korumasız bir gecelik açığa satışa dönerdi (VC #10, #16).
- **PDT nakit hesaba uygulanmaz:** kural margin hesaplarına ilişkin; nakit hesapta Reg T ve free-riding kısıtları sürüyor (VC #15 [D]). Bu yüzden 50k örneğinde 20 bin $'lık bakiye sorun değil. IBKR'den yine de yazılı teyit istenir (§10).
- **Free-riding / good-faith:** Yeni girişler yalnız yerleşmiş nakitle yapılır (§6.2 tavanı). Satış bedeli T+1'de yerleşir (PRA §1.4); swing tutma süresinde ihlal riski düşük.
- Başvuru margin olarak yapıldıysa Client Portal'dan hesap tipi "Cash" olarak değiştirilir (menü yeri bellekten yazıldı; teyit et).
- Margin hesabına geçiş ancak Faz 2 kapısında ve yalnız gerekçe varsa değerlendirilir. Margin hesabı kullanılırsa IBKR'nin yeni FINRA kuralına geçtiği yazılı teyit edilene kadar USD bakiyesi ≥ 25 bin $ tutulur (KT2 Ö-3).

**İzinler ve teknik kilitler (KT1 #2):**
- IBKR'de yalnız "Stocks – United States" işlem izni istenir. Opsiyon, vadeli ve margin izni istenmez. VİOP tecrübesi beyan edilir (§3.9).
- **IBKR emir ön ayarları** (TWS'te "Precautionary Settings"; ad ve yer bellekten, testte teyit): emir başı toplam değer tavanı = E'nin %7,5'i; adet tavanı = bu değer / 20 $.
- **W-8BEN** doldurulur; yoksa temettü stopajı %30 olur (PRA §1.3).

### 6.2 Emir şablonları, bekleyen emir tavanı ve testler (IBKR)

| Amaç | Emir | TIF / seans | Ne zaman (TSİ) |
|---|---|---|---|
| S1/S2 giriş | Ana emir BUY STP LMT (tetik ve limit §3.2–3.3); "outside RTH" kapalı | DAY. 22:00 TSİ olayı olan günde **GTD, 21:55 TSİ'de (13:55 ET) düşer** (KT1 #11) | Akşam bloğu 16:45–17:15 |
| İlk stop | Ana emre ekli (attached) SELL STP, piyasa, tam adet. **Stop-limit değil:** gap'te stop-limit dolmayabilir | GTC, yalnız RTH | Giriş emriyle birlikte |
| Stop bölme (alt lotlar) | Stop adedi lot B'ye indirilir; lot A için aynı fiyattan yeni GTC SELL STP girilir, OCA grup adı `TICKER-A` | GTC, yalnız RTH | Dolumdan sonraki ilk kapanış bloğu (seans dışı) |
| Kısmi satış | SELL MOO (TIF = OPG), lot A adedi, OCA = `TICKER-A` (stop A ile). Lot B'nin stopu dolum fiyatına | Açılış | Kapanış bloğu |
| Tam çıkış (trail, zaman, başarısız kırılım, aşırı koşu) | SELL MOO kalan adet; kalan bütün stoplarla aynı OCA grubunda | Açılış | Kapanış bloğu |
| Bilanço öncesi çıkış | SELL MOC; stoplarla aynı OCA grubunda. Yedek: son seansın açılışında MOO (§3.6) | Kapanış | Son seanstan önceki kapanış bloğu (en geç son seansın 16:45–17:15'i) |
| Stop yükseltme | GTC stop fiyatını yükselt; **asla indirme** | — | Kapanış bloğu; haftalık acil stop Cumartesi |
| Fazla adaylar | OCA grubu ("Cancel all remaining orders with block"); her grup en çok 1 dolum verir | DAY | Akşam bloğu |

**Son giriş saatleri:** MOO ~17:28 TSİ (09:28 ET), MOC ~23:50 TSİ (15:50 ET). Bunlar bellekten; IBKR'den yazılı teyit istenir. Kapanış bloğunda girilen emir bu saatlerden çok önce girildiği için sınır pratikte bağlamaz, ama emrin seans dışında kabul edildiği test edilir.

**Bekleyen giriş emri tavanı (KT1 #4; KT2 K-2).** Her akşam bloğunda, emir girmeden önce hesaplanır:
1. **Bekleyen emirler dolmuş sayılır.** Bütün tavanlar (ısı, küme, brüt, en kötü hafta) bu varsayımla kontrol edilir.
2. **Canlı giriş grubu sayısı** N = min(günlük kalan giriş hakkı; boş pozisyon yeri; ⌊kalan ısı / (1,25 × 1R)⌋). Kalan ısı = rejim ısı tavanı − açık gap-ayarlı risk.
3. **Tutar:** Σ (her grubun en büyük adet × limit tutarı) ≤ min(kalan brüt tavan; yerleşmiş USD nakit − NLV'nin %5'i).
4. **Küme:** Aynı kümenin adayları aynı OCA grubuna konur. Bir kümeden dolum sayısı kalan küme hakkını aşamaz.
5. N'den fazla aday varsa adaylar N tane OCA grubuna bölünür. Örnek: SARI'da 2 hak varsa 2 grup kurulur; her grup en çok 1 dolum verir.
6. Ana emri ekli stoplu (bracket) emirler OCA grubuna konamıyorsa yedek kural: yalnız öncelik sırasındaki ilk N aday canlı girilir, diğerleri yedek listede bekler.

**Veri günleri (CPI, PPI, NFP; 16:30):**
- 16:45'ten önce yeni emir girilmez.
- 16:45'te S&P vadelisi önceki kapanışa göre **±%1,5'ten fazla** oynamışsa o gün yeni giriş yok (C §3.4 [Ö]). Çıkış emirleri zaten kapanış bloğunda girilmiştir.

**1 adetlik test planı (fonlanan ilk günden itibaren; KT2 küçük #18; KT1 bellek notları).** Testler 2 adetle yapılır, böylece stop bölme de denenebilir. Maliyet ~5–8 $ komisyon; günlüğe "test" diye yazılır.

| Gün | Blok | Test | Geçerse / geçmezse |
|---|---|---|---|
| T1 | Akşam | (1) Likit bir hisseden 2 adet, piyasaya yakın LMT ile al, ekli GTC SELL STP (yalnız RTH, %10 aşağıda). (2) Uzak tetikli 2 BUY STP LMT, ekli stoplu, aynı OCA grubunda. (3) Uzak tetikli 1 BUY STP LMT, GTD 21:55 TSİ. (4) Emir değeri ön ayarının üstünde bir emir dene. (5) Elindekinden fazla (3 adet) SELL dene | (2) geçmezse fazla adaylar için yedek kural (§6.2 #6). (3) geçmezse 22:00 olay günlerinde yeni giriş yok. (4) uyarı vermezse ayar düzeltilir. (5) reddedilmezse hesap tipi kontrol edilir |
| T2 | Kapanış (seans dışı) | (6) Stopu böl: adet 1'e indir, 1 adet için yeni GTC STP (OCA adı `TEST-A`). (7) 1 adet SELL MOO, OCA = `TEST-A`. (8) (3)'teki GTD emri 21:55'te düştü mü? (2)'deki emirleri iptal et | (7) seans dışında kabul edilmez ya da OCA'ya girmezse yedek 1: stopun tipini MOO'ya çevir. O da olmazsa yedek 2 (§3.5) |
| T2 | Açılış sonrası kontrol (ertesi kapanış bloğunda) | MOO doldu mu, STP-A iptal oldu mu? | Sonuç günlüğe; kısmi ve tam çıkış yöntemi buna göre seçilir |
| T3 | Kapanış (seans dışı) | (9) Kalan 1 adet için SELL MOC, kalan stopla aynı OCA'da | Geçmezse bilanço çıkışı yedeği (son seans açılışında MOO) |
| Midas | — | Aynı testler (≤ 500 $ ile) | Ekli stop, MOO veya OCA yoksa Midas S1/S2 için kullanılmaz |

### 6.3 Günlük ve haftalık rutin (TSİ)

Uygulanacak tek sayfa RUTİN dosyasıdır (`uygulama/ABD_GUNLUK_RUTIN.md`). Özeti:

| Saat | İş | Süre |
|---|---|---|
| **Kapanış bloğu:** gece 00:30–01:00 **ya da** sabah 08:00–09:00 (birini seç, her gün aynısı) | Rejim (§2). Dolumlar ve stop olanlar. Çıkış sinyalleri (kısmi, trail, zaman, başarısız kırılım, aşırı koşu, bilanço). **Çıkış emirleri** (MOO/MOC, OCA'lı), stop bölme ve yükseltme. **Stop mutabakatı:** her pozisyonun doğru adetli, canlı, yalnız RTH GTC stopu var mı (KT1 #9). Isı, küme ısısı, aylık zarar + ısı, merdiven. Günlük. G1 gölge taraması | 20–30 dk |
| 16:30 | Veri günlerinde vadeliye bak | — |
| **16:45–17:15** | **Yalnız giriş emirleri** (her gün yeniden). Bekleyen emir tavanı. Emirler kaydedilir | 10–15 dk |
| 17:30–00:00 | **Ekran yok.** Yalnız aracı kurumun dolum bildirimleri. Stop ekli olduğu için dolumdan sonra işlem gerekmez. Bu saatte emir değiştirmek kritik ihlaldir | — |
| Perşembe | TCMB haftalık rezerv verisi → döviz anahtarı (§1.5) | 5 dk |
| Cumartesi | Taramalar (a), (d). Kümeler. İzleme listesi. Acil stop yükseltmesi. Haftalık uyum satırı (ihlal sayısı, "dışarıda kalma" günleri, G2 sonucu; fırsat kaçırma duygusu gölge günlüğüne yazılır, hesaba yansımaz; KT1 #2). 10 işlemde bir istatistik (§8.3) | 60–90 dk |
| Ayın son hafta sonu | Küme izni (c) ve korelasyonlar (e). E'nin yeniden hesabı. Aylık rapor (§8.6). Faz kapısı kontrolü | 60 dk |

### 6.4 Maliyetler (R cinsinden ölçülür)

- **Komisyon:** §3.4'teki tablo. IBKR ve Midas'ta ~0,001–0,024R; Gedik'te ~0,015–0,04R; yüzdesel komisyonlu Türk kurumlarında ~0,07–0,2R.
- **Kayma:** stop emirlerinde ölçülmedi. Varsayım %0,05–0,15, yani ≈ 0,01–0,03R. Günlükte bps olarak ölçülür.
- **Kur dönüşümü:** banka makası + BSMV binde 2 (teyitsiz). İlk transferden önce küçük tutarla ölçülür.
- **Veri:** 50k'da TradingView Premium alınmaz (§1.3).
- **Kural:** maliyet + kayma 20 işlem ortalamasında > 0,15R olursa emir yöntemi değişir (§8.5 DUR-4).

### 6.5 Vergi ve kayıt (Türkiye beyanı)

**Her lot için tutulacaklar:**
- Alış ve satış tarihi, adet, USD fiyat, komisyon.
- O günlerin **TCMB kuru** (hangi kur türü: müşavirle netleştir).
- TL maliyet, TL bedel, TL kâr/zarar.

**Yöntem ve beyan:**
- Maliyet yöntemi (FIFO ya da ortalama) müşavirle seçilir, bütün yıl aynı uygulanır.
- Kazanç tutarı ne olursa olsun Mart 2027'de beyan edilir; ödeme Mart ve Temmuz taksitleriyle. 150 bin TL istisnası menkul kıymete uygulanmaz (VC #10).

**Kısa vergi yılı 2026:**
- 9.11–31.12 kendi başına bir vergi yılı ve **2026 zararı 2027'ye devretmez** (VC #10). Bu yüzden 2026'da Faz 1 boyutunda kalınır.
- Kur her ay ~%1,5 arttığı için USD'de zarar eden lotlar bile TL'de kâr gösterebilir (PRA §2.1).
- **Aralık'ın ilk haftası (1–4.12) vergi kontrol noktasıdır.** Kural önceliklidir; yalnız vergi için çıkış yapılmaz. **Tek istisna kazanç hasadıdır** (KT1 #6):
  - **Şart 1:** 2026'nın net gerçekleşen TL sonucu < 0.
  - **Şart 2:** Açık pozisyonlarda TL bazında gerçekleşmemiş kâr var.
  - **Şart 3:** Türkiye'de wash-sale benzeri bir kural olmadığı müşavirle yazılı teyit edildi.
  - **Şart 4:** Geri alım anında kurulumun çıkış sinyali yok.
  - **İşlem:** En çok 2026 zararı kadar TL kârı olan lotlar, en geç 30.12'de **SELL MOC** ile satılır (stopla aynı OCA'da). Ertesi seans **BUY MOO** ile aynı adet geri alınır ve aynı stop yeniden eklenir.
  - **Bedel:** 2 komisyon (IBKR'de ~0,005R) ve bir gece piyasa dışında kalma.
  - **Fayda:** 2027'de vergilenecek kazancın E'nin ~%0,45 / %0,6–0,8 / %1,05'i kadar azalması (50k / 250k / 1m; KT1 #6 [H]; 2026 tarifesi doğrulanmadı).
  - Simetrik durum (2026 net TL kâr, açık lotlarda TL zarar) için de aynı işlem yapılabilir; yalnız müşavir onayıyla.

**Vergi dışbükeyliği:** Kötü yılda iade yok, iyi yılda tam vergi var. Oynaklık beklenen vergi sonrası getiriyi düşürür: A/C profilinde yılda ~−0,4 puan (HD §2.3 [H]).

**Diğer gelir kalemleri:**
- Nakit faizi menkul sermaye iradıdır (PRA §4.1).
- Temettüde %20 ABD stopajı uygulanır (Form 1042-S saklanır); beyan sınırı 22.000 TL (VC #10, #12).

**Belgeler (5 yıl saklanır):**
- IBKR aylık ve yıllık Activity Statement (CSV + PDF).
- SWIFT ve döviz alış dekontları.
- İşlem günlerinin TCMB kur tablosu.
- W-8BEN kopyası.

**Müşavire sorulacaklar:**
- Elde tutulan USD'nin kur farkı vergisiz mi?
- Yılda 60–120 işlem "ticari kazanç" nitelendirmesi riski doğurur mu (PRA §2.1)?
- Wash-sale benzeri kural yokluğu ve Aralık kazanç hasadı (yazılı).
- 60 bin $ üstü US-situs varlıklar için veraset vergisi (Form 706-NA; VA #36).

---

## 7. Takvim

### 7.1 Hafta: 9–13 Kasım

| Gün | Olay (TSİ) | Ne yapılır |
|---|---|---|
| **Cu 06.11 (bugün)** | 16:30 NFP (beklenti +59–65 bin). HUM, VST, MRNA BMO. IDXX'in G1 penceresi bugün kapanıyor | Midas ve IBKR başvuruları; IBKR **nakit hesap**, yalnız ABD hisse izni (§10). Kapanışta ralli denemesi gün sayımı başlar ya da başlamaz |
| **Ct 07.11** | **BRK-B bilançosu 07:00 CT (16:00 TSİ)** | §2.6 tablosu. §10 hafta sonu listesi. **Küme korelasyonları** (§4.1 e) |
| **Pt 09.11** | 16:40 Bowman (Barkin teyit). 21:00 3 yıllık ihale. BMO: CEG, MNDY, NRG (AI güç; dışarıda). AMC: RKLB, TTWO, ZETA, ASTS, HIMS, MARA, PLUG. BRK-B'nin ilk tepki seansı | **Canlı giriş yok.** SWIFT sabah. Hesap fonluysa T1 testleri. İzleme listesi. G1 gölge kaydı |
| **Sa 10.11** | 12:00 Waller. **16:30 Ekim CPI** (Cleveland nowcast: manşet aylık %0,24, çekirdek %0,21). 21:00 10 yıllık ihale. AMC: CRWV (AI turnusolu), RGTI. BMO: ONON, SE, QBTS | Veri günü kuralı. Pilot mümkün değil. **MDT'de yeni giriş yasağı başlar** (24.11 bilançosuna 10 seans). Kapanışta G2 tetiği kontrolü. Fonlandıysa testler |
| **Ça 11.11** | Gaziler Günü: hisse açık, tahvil kapalı; hacim düşük olabilir. MSCI Kasım duyurusu ~00:00 (12.11). AMC: FNV, CTVA | **En erken FTD kapanışı** (Cuma 1. gün olduysa); hacim şartına dikkat. SARI sayacı 1 olabilir. BRK-B için eleme filtresi (b) en erken bu kapanışta |
| **Pe 12.11** | 16:30 işsizlik başvuruları. 18:00 Barr, mevcut konut satışları. 21:00 30 yıllık ihale. **TCMB haftalık rezerv verisi.** BMO: NBIS, LUNR. AMC: **CSCO, AMAT**, NU, CBRS | **Pilot yok** (SARI sayacı en çok 2). **Döviz anahtarı kontrolü** (§1.5). AMAT/CSCO yalnız endeks riski olarak izlenir |
| **Cu 13.11** | **16:30 PPI.** 18:00 UMich (tarih teyit). Fed konuşmacıları. LLY için ObesityWeek 14–17.11 yaklaşıyor | Veri günü kuralı. **En erken SARI kapanışı** (3. kapanış). LLY'de 17.11'e kadar giriş yok (ikili olay). Kapanıştan sonra haftalık inceleme: rejim, gölge kayıtlar, izleme listesi, acil stop |

### 7.2 16–20 Kasım

| Gün | Olay | Kural |
|---|---|---|
| **Pt 16.11** | BMO: XPEV, BIDU, TSN. AMC: PARA, POWL | **En erken canlı pilot** (13.11 SARI olduysa): 16:45–17:15. Yakın bölgede 1 pozisyon, %0,25 risk, ısı ≤ %0,5 |
| **Sa 17.11** | 17:15 sanayi üretimi. Perakende satış tarihi açık (17.11 ya da 25.11; Census listesinde Kasım satırı yoktu, KT2). HD BMO. **NVDA sonuçları kapanıştan sonra; konferans 17:00 ET = 01:00 TSİ (18.11)** (NVIDIA newsroom 28.10.2026; KT2) | **17.11'de bütün kümelerde yeni giriş yok** (endeks olayı). Açık pozisyonlar stoplarıyla kalır |
| Ça 18.11 | TGT, TJX, LOW BMO; PANW AMC. 21:00 20 yıllık ihale. **22:00 FOMC tutanakları.** VIX vadesi | Giriş serbest; **giriş emirleri GTD, 21:55 TSİ'de düşer** (KT1 #11). Faiz duyarlı süper-kümede ve perakendede WMT/TGT öncesi yeni giriş yok |
| Pe 19.11 | WMT BMO; ROST, GAP, INTU, KEYS AMC. 10 yıllık TIPS. Philly Fed (teyit) | Normal |
| **Cu 20.11** | **Aylık opsiyon vadesi.** BJ BMO | BJ'de giriş yok (K6'da en erken 25.11 kapanışından sonra) |

### 7.3 23–30 Kasım

| Gün | Olay | Kural |
|---|---|---|
| Pt–Sa 23–24.11 | 2 ve 5 yıllık ihale; BBY BMO (24.11). **MDT BMO (24.11)** | Normal; MDT'ye bilanço + 3 seanstan önce giriş yok |
| **Ça 25.11** | 16:30 3. çeyrek GSYH 2. tahmin + Ekim PCE + kişisel gelir/harcama. 21:00 7 yıllık ihale. 22:00 Bej Kitap | **Yeni giriş yok** |
| **Pe 26.11** | Şükran Günü: piyasa kapalı | — |
| **Cu 27.11** | Erken kapanış: 21:00 TSİ (13:00 ET) | **Yeni giriş yok.** MOO çıkışları serbest |
| Pa 29.11 | OPEC+ toplantısı | — |
| **Pt 30.11** | Ay sonu. MSCI değişiklikleri kapanışta uygulanıyor | Hafta sonu (28–29.11): küme izni (§4.3), korelasyonlar, E'nin yeniden hesabı, aylık rapor |

### 7.4 1–11 Aralık

| Gün | Olay | Kural |
|---|---|---|
| 1–4.12 | **Vergi kontrol noktası** (§6.5). 3.12 TR Kasım TÜFE. 4.12 Kasım NFP | Kazanç hasadı yalnız §6.5 şartlarıyla |
| **Sa 08.12** | Kapanış | **Makro gap-ayarlı ısı** (§5.3); aşan kısım 9.12 MOO |
| **Ça 09.12** | **FOMC 22:00** (artırım olasılığı ~%67–70; HAZ §2.2) | Yeni giriş yok |
| Pe 10.12 | 16:30 Kasım CPI. TCMB PPK | Veri günü kuralı |
| Cu 11.12 | ABD federal bütçe finansman süresi doluyor (kapanma riski) | Haber izlenir |
| 18.12 | Dörtlü vade (quad witching) | Normal |
| 30.12 | Kazanç hasadı için son MOC günü (§6.5) | Yalnız şartlar sağlandıysa |

---

## 8. Ölçüm protokolü ve öldürme kriterleri

### 8.1 Hipotez kartları

Kartlar ilk işlemden önce yazılır; tarihlidir ve değiştirilemez. Kuraldaki her değişiklik yeni bir kart sayılır (SEY §5.3 #1). Kartlar bu revizyonun kurallarıyla yazılır: 3 kapanış SARI, yakın bölge, %7,5 tavan, alt lotlar.

| Kart | Mekanizma | Beklenen E[R] | İsabet | Kazanç/kayıp | İşlem/yıl | Denenen varyant (N) |
|---|---|---|---|---|---|---|
| S1 | Sağ kuyruğu yakalama (Bessembinder %4; VA #29) + rejim filtreli momentum | +0,1R (aralık −0,2 ile +0,4R) | %25–40 | 2–3,5 | 40–70 | 1 |
| S2 | Trend içi likidite geri çekilmesi, lider devamı [P] | +0,1R (aralık −0,1 ile +0,3R) | %30–45 | 2–3 | 30–50 | 1 |
| G1 (gölge) | Bilgili şok drift'i (Savor; KIM §5.1) | −0,1 ile +0,3R | %30–45 | 2–5 | 10–25 | 1 |
| G2 (gölge) | Panik primi / likidite (Nagel; KEN §5) | Koşulsuz piyasaya göre olay başına +%0 ile +%1,8 | %65–80 | ~1 | 1–3 | **2** (C-TEST A ve B) |

### 8.2 Günlük alanları (her işlem bir satır; piramit ekleri ayrı satır)

- **Kimlik:** no, ana işlem no, canlı / gölge / test, kart sürümü, kol, kurulum, küme, ticker.
- **Bağlam:** rejim durumu, SARI sayacı, yakın bölge (evet/hayır), VIX/VIX3M, faz, bilançoya ve ikili olaya kalan seans, eleme filtresi (evet/hayır).
- **Plan:** pivot, tetik, limit, ilk stop, stop %, stop/ATR, ATR14, ADR%20, adet, alt lotlar (A/B), pozisyon (E'nin ve NLV'nin %'si), 1R ($), gap-ayarlı risk; girişteki toplam ve küme ısısı, brüt maruziyet, en kötü hafta toplamı.
- **Uygulama:** dolum fiyatı ve saati, **kayma (bps ve R)**, komisyon, emir tipi, OCA grup adı.
- **Yönetim:** kısmi satış (tarih, fiyat, R), stop değişiklikleri, ekler, stop mutabakatı bulguları.
- **Sonuç:** çıkış nedeni (stop / başarısız / kısmi / trail / zaman / aşırı koşu / bilanço / rejim / öldürme), çıkış fiyatı, **gerçekleşen R** (komisyon dahil), MAE ve MFE (R), tutma süresi (seans).
- **Vergi:** alış ve satış günü TCMB kuru, TL maliyet, TL bedel, TL kâr/zarar.
- **Disiplin:** kural ihlali (yok / kritik / diğer ve açıklama), ekran görüntüsü bağlantısı.
- **Ayrı sekme "kaçan sinyaller":** dolmayan emirler ve atlanan tetikler. Sinyal fiyatı ve 20 seans sonraki fiyat yazılır; ekransız ve limitli girişin bedelini ölçer (C §7.2).
- **Ayrı sekme "haftalık uyum":** ihlal sayısı, rejim nedeniyle dışarıda kalınan gün sayısı, G2 sonucu, fırsat kaçırma notu (KT1 #2).

### 8.3 İstatistik ve faz kapıları

**Her 10 canlı işlemde hesaplananlar** (kurulum bazında ve toplamda):
- n; ortalama R (m); standart sapma (s); SE = s/√n; t = m/SE.
- İsabet; ortalama kazanç ve kayıp; profit factor; en uzun kayıp serisi.
- Net kârın en iyi %10 işlemden gelen payı. Pozitif çarpık sistemde > %100 olması normal.
- Rejime göre ayrışma; ortalama maliyet + kayma (R); S&P'ye beta.

**İstatistik gerçeği:**
- s ≈ 2–2,5R alınırsa n=50'de SE ≈ 0,28–0,35R, n=100'de ≈ 0,20–0,25R (SEY §3.7).
- Faz 2 kapısını sıfır kenarlı bir sistem de ~%15–20 olasılıkla geçebilir [H; KT2 ~%16 buldu]. Bu yüzden Faz 2 yalnız işlem riskini artırır, sermayeyi artırmaz.

| Kapı | Şartların tümü | Sonuç |
|---|---|---|
| **Faz 1 → 2** | n ≥ 50 canlı (S1 + S2); ≥ 4 ay; m ≥ +0,25R; t ≥ 1,0; zirveden en büyük düşüş < %6,5 E (Kademe 3'e hiç ulaşılmamış); son 50 işlemde kritik ihlal yok; diğer ihlal oranı < %10; maliyet + kayma ≤ 0,15R | İşlem riski %0,5. Piramit serbest (YEŞİL'de). USD çevrimi %70. Faz 2 merdiveni bootstrap ile yeniden ölçülür. **E aynı kalır** |
| **Faz 2 → 3** | n ≥ 100; **≥ 12 ay**; m ≥ +0,25R; **t ≥ 1,65**; en az bir KIRMIZI → YEŞİL döngüsü; son 12 ayın **vergi öncesi** USD getirisi, gerçek u ile §1.2'deki gereken R'yi geçmiş (KT2 küçük #21); DUR-9 geçilmiş; **EOD backtest geçilmiş** (aşağıda) | İşlem riski %0,75 (en çok %1). E'yi servetin %25–35'ine çıkarmak değerlendirilir |
| **"Kanıtlandı"** | SPRT H1'i kabul eder (+0,2R'lik sistemde ~300–450 işlem) ya da 3 yıl ve en az bir stres rejimi (SEY §5.3 #4) | Ancak o zaman "yüksek ödül" sürümü (progresif boyut) konuşulur |
| **Geri düşüş** | Son 50 işlemin m'si < 0 | Bir faz aşağı |

**EOD backtest şartı** (A §7.4; HK §7 #5):
- S1/S2'nin bu dosyadaki kuralları, hayatta kalma yanlılığından arındırılmış günlük veriyle test edilir. CRSP/WRDS bireye açık değil; **Norgate Data ya da Sharadar** gibi ücretli bir sağlayıcı kullanılır (KT2 küçük #14). Fiyatı satın almadan önce kontrol edilir.
- Örneklem içi 2012–19, dışı 2020–26. Maliyet: spread + 10 bp.
- Kabul: örneklem dışında E[R] > +0,3R ve yılda ≥ 40 işlem.
- Bu test geçilmeden risk %0,5'in üstüne çıkmaz.

### 8.4 Gölge kolların canlıya alınması

- **G1:** ≥ 30 gölge işlem, m ≥ +0,3R ve t ≥ 1,0, **ve** EOD backtest'te G1 örneklem dışı E[R] > +0,3R → Faz 1 riskiyle (%0,25) ayrı kartla canlıya alınır.
- **G2:** ≥ 5 örneklem dışı olay ve koşulsuz piyasaya göre ortalama fark > 0 → %0,25 riskle canlıya alınabilir. Pozisyon ≤ E'nin %6,25'i (stop %4).
  - SPY erişimi IBKR şirketine bağlı. IBIE'ye bağlanılırsa yedek CSPX olur (LSE 08:00–16:30 GMT; Kasım'da **11:00–19:30 TSİ**; KT2 küçük #4). Bu yedek test edilmedi. PRIIPs AB/AEA mukimine uygulanır; Türk mukimi için kısıt büyük olasılıkla yok, teyit gerekir (VA §4 #7).

### 8.5 Öldürme kriterleri (önceden yazılı)

| # | Tetik | Eylem | Dayanak |
|---|---|---|---|
| DUR-1 | Bir kurulumda n ≥ 30, m ≤ −0,3R ve t ≤ −1,3 | O kurulum durur; yeni kart yazılmadan açılmaz | C §7.4 |
| DUR-2 | n ≥ 50 ve m + 1,28 × SE < 0 | Kurulum durur | SEY §5.2 #2 |
| DUR-3 | n ≥ 100 ve (m < 0 **ya da** m + 1,65 × SE < +0,05R) | Kurulum kalıcı olarak kapanır | SEY §5.2 #2, #4 |
| DUR-4 | n ≥ 20 ve maliyet + kayma > 0,15R ya da kenar tahmininin %50'si | Emir yöntemi değişir; 20 işlem sonra düzelmezse kol durur | SEY §5.2 #3 |
| DUR-5 | Strateji zirveden fazın dur eşiğine düştü: **Faz 1 −%8 E** (aşama 1'de NLV −%20); Faz 2 −%10; Faz 3 −%15 (§5.2) | **Plan durur** | SEY §5.2 #1, #8; KT1 #1 |
| **DUR-6a** | **Kritik ihlal** (n'den bağımsız; KT1 #2): (1) KIRMIZI/TURUNCU'da, aylık devre kesici aktifken ya da 10 seanslık duraklama (Kademe 3, DUR-6a) sırasında canlı giriş; (2) girişte risk, yani adet × (dolum − stop), > 1,25 × 1R bütçesi (gap kaybı ihlal değildir); (3) stopu aşağı çekmek ya da iptal edip yeniden girmemek; (4) zarardaki pozisyona ekleme; (5) opsiyon, kaldıraçlı ETF, margin borcu ya da açığa satış (Faz 1'de); (6) AI kümesinde §4.6 dışında giriş; (7) 17:30–00:00 arası emir girmek, değiştirmek ya da iptal etmek | **1. ihlal:** 10 seans yeni işlem yok ve yazılı inceleme. **2. ihlal (12 ay içinde):** plan durur (DUR-5 gibi) | KIM §6 ("kuralın en çok ihlal edildiği an tam bu an"), §5.3; VA #16; VP A6–A7 [D]; KT1 §2 |
| DUR-6b | Diğer ihlaller (bilanço/ikili olay yasağı, tavan aşımı, emir hijyeni): n ≥ 20'de ihlal oranı > %20, ya da herhangi bir 20 işlemlik blokta ≥ 3 ihlal | 2 hafta yeni işlem yok. Sorun disiplin, kenar değil | A K4; C K6 |
| DUR-7 | Mekanizma ortadan kalktı (ör. emir tipi ya da erişim kapandı, vergi rejimi değişti) | t'ye bakmadan durur | SEY §5.2 #5 |
| DUR-8 | 12 aylık S&P korelasyonu > 0,7 ve S&P'ye göre kalıntı getiri ≤ 0 | Kol yalnız beta: dur | SEY §5.2 #7 |
| DUR-9 | 12 ayda strateji, aynı ortalama maruziyetle "rejim SARI/YEŞİL iken RSP, değilse T-bill" kuralını vergi öncesi geçemiyor | Seçim değer katmıyor: dur | SEY §5.3 #6; A K6 |
| DUR-10 | 12 ay ve 100 işlemden sonra vergi sonrası TL getirisi < TL nakdin net getirisi **ve** m < +0,3R | Ölçek yok. Sürecekse yalnız Faz 1 boyutunda ve sermaye TL'ye dönmeye adaydır. **TL kıyası yalnız bu 12 aylık kapıda kullanılır; çeyrek içinde TL kıyasıyla karar verilmez** (KT1 #12) | A K7; §1.2 |

**Davranış yolunun ağırlığı (KT1 §2) [H, kalibre değil]:** Kasten düşmanca bir rejim varsayan 3 aylık MC'de (işlem başı beklenti ≈ −0,4R) kurallara uyulursa P(NLV ≤ −%15) ≈ %0–0,4; medyan NLV −%4, %5 kötü NLV −%10. Riskin %1'e çıkarıldığı ve Midas'tan piyango call'ı alındığı "ihlal" senaryosunda P(NLV ≤ −%15) ≈ %38, P(NLV ≤ −%25) ≈ %12. DUR-6a bu yolu kesmek için var.

### 8.6 Aylık rapor (ayın son hafta sonu)

- Kurulum bazında: n, m, %90 bootstrap güven aralığı, t, isabet, profit factor, MAE/MFE, kayma, ısı kullanımı, rejim ayrışması, kaçan sinyallerin maliyeti.
- Gölge kolların aynı metrikleri (ayrı tablo).
- **Değer satırı:** Stratejinin vergi öncesi USD getirisi ve §1.2 modeliyle tahmini vergi sonrası USD getirisi; **% E, % NLV ve $** olarak (KT1 #1, #12).
  - Kıyas 1: USD nakdin vergi sonrası getirisi (%1,15–2,6; aşama 1'de boştaki USD faizi fiilen ~%0–0,3 E).
  - Kıyas 2: DUR-9 kıyası (RSP / T-bill).
  - Bilgi sütunu: "TL mevduata göre" fark (TL'de kalmanın USD karşılığı ~%9–14). Bu sütun karar için kullanılmaz; yalnız 12 aylık DUR-10 kapısında kullanılır.
- Merdiven kademesi (E ve NLV), faz, sonraki kapıya kalan, kritik ihlal sayısı.

---

## 9. Beklenen sonuçlar ve belirsizlik

### 9.1 1. yıl: Kasım 2026 – Ekim 2027 (çoğunlukla Faz 1) [H]

**Model (bu revizyonda yeniden çalıştırıldı):**
- HD §4.1 ile aynı aile (`scratchpad/hakem_deger/mc3.py` mantığı): isabet %30; işlemler 3'lü dalgalarda ve dalgaların %30'unda küme birlikte bozuluyor; kayıplar −1,05R, %10'u gap'li −2R; kazanç 0,5R + üstel dağılım, ortalama hedef E[R]'ye ayarlı.
- Faz 1, %0,25 risk, 80 işlem; 8.000 yol; tohum 11.
- **Yeni merdiven** (−%3 → risk × 0,5; −%6,5 → × 0,25; −%8'de dur).
- **Nakit faizi yok** (KT2 Ö-1). Önceki tablo boştaki USD'ye +%2,4 ekliyordu; IBKR kademeleri ve kademeli çevrim yüzünden bu katkı gerçekte E'nin ~%0–0,3'ü.
- Aylık devre kesici, felaket gap'i ve davranış hatası modelde yok.
- Kontrol: aynı model eski merdivenle çalıştırıldığında HD §4.1'in düşüş sütunları ±0,1 puanla, medyanları nakit katkısı çıkarılmış hâliyle ±0,2 puanla tuttu (−%2,8 / −%1,1 / +%1,4 / +%4,3 / +%6,9).
- Sonuçlar vergi öncesi USD, E üzerinden, yalnız strateji. Olasılıklar öznel [Ö]. Taban oranlar sert: USIC'te %8–17 kârlı, Tayvan'da %13 (VA #8, #14).

| Kenar (E[R]) | Öznel olasılık | Medyan | p10 / p90 | En büyük düşüş: medyan / %5 kötü | P(−%8 dur) |
|---|---|---|---|---|---|
| −0,1R (taban oranlara göre en olası) | %50–60 (0 ve altı) | **−%2,5** | −%6,1 / +%4,7 | −%5,2 / −%7,2 | < %1 |
| 0 | ↑ | −%1,2 | −%5,6 / +%7,5 | −%5,0 / −%7,1 | < %1 |
| +0,15R | %25–30 | +%1,0 | −%4,9 / +%11,9 | −%4,8 / −%7,0 | < %1 |
| +0,3R | %10–15 | +%3,7 | −%4,0 / +%17,0 | −%4,5 / −%6,9 | < %1 |
| +0,45R (USIC tipi) | ≤ %5 | +%6,5 | −%3,1 / +%21,7 | −%4,4 / −%6,8 | < %1 |

**Okuma:**
- Ağırlıklı merkez vergi öncesi **−%1,5 ile +%1,5** (önceki sürümde +%1–4; fark nakit katkısının çıkarılmasından geliyor; KT2 Ö-1).
- Yeni frenler (3 kapanış SARI, yakın bölgede tek pozisyon, %7,5 tavan) ilk aylarda işlem sayısını düşürür. 60 işlemle medyanlar −%2,1 / −%1,0 / +%0,7 / +%2,7 / +%4,6 [H].
- Yeni merdiven %5 kötü düşüşü ~0,5–1 puan iyileştiriyor (−%8,3 → −%7,2 en kötü senaryoda). Bedeli: pozitif kenarda medyandan ~0,4–0,6 puan alıyor; negatif kenarda kaybı ~0,3 puan azaltıyor.
- Tek yılın sonucu kenarı kanıtlamaz. 80 işlemin toplam R'sinin standart sapması ±18R, yani %0,25 riskte ±%4,5 [H].
- **TL tarafı ayrı satırdır** (KT2 Ö-1). Kademeli çevrimde E'nin %50–60'ı TL'de bekler ve TL mevduatın getirisini alır. Kur +%20 ve h = %31–37 varsayımıyla bu USD karşılığı E'ye yılda ~+%5,5–8,5 ekler. Kur şokunda bu katkı negatife döner. Bu katkı **strateji getirisi değildir**, TL'de kalmanın getirisidir. Strateji yalnız yukarıdaki tabloyla ölçülür.

### 9.2 Vergi sonrası ve engelle karşılaştırma [H]

Model §1.2: u = 0,3, d = %20, 2026 tarifesi (doğrulanmadı). Betik `plan_final/at.py`'deki `after()` fonksiyonu.

| Vergi öncesi R → vergi sonrası USD | 50k | 250k | 1m |
|---|---|---|---|
| −%2,5 (kenar −0,1R) | −%2,9 | −%2,9 | −%3,2 |
| −%1,2 (kenar 0) | −%1,8 | −%2,0 | −%2,3 |
| +%1,0 (+0,15R) | +%0,1 | −%0,4 | −%0,9 |
| +%3,7 (+0,3R) | +%2,3 | +%1,4 | +%0,9 |
| +%6,5 (+0,45R) | +%4,5 | +%3,3 | +%2,5 |
| Kıyas: USD nakit, vergi sonrası (E'nin tamamı nakitte, IBKR kademeli) | %1,15 | %2,6 | %2,4 |
| Kıyas: aşama 1'de boştaki USD'nin faizi (E'nin %'si) | ~0 | ~%0,2 | ~%0,3 |
| Kıyas: TL'de kalmanın USD karşılığı (h %31–37) | %9,2–14,2 | %9,2–14,2 | %9,2–14,2 |
| TL'yi yenmek için gereken vergi öncesi R (u = 0,3) | %12,7–19,5 | %15,6–23,3 | %17,5–25,9 |

Negatif USD getiride bile vergi sonrası sonuç daha kötü: pozisyondaki sermayenin kur farkı (hayalet vergi) TL'de kazanç yaratıyor.

**Sonuç:**
- 1. yıl vergi sonrası merkez ~**−%2 ile +%1**. Bu, USD nakdin vergi sonrası getirisinin altında.
- **TL engelini geçme olasılığı < %5** (HD §4.1). Yeni tabloda en iyi iki senaryonun p90'ı (+%17,0 / +%21,7) ancak engel bandının içine giriyor; bu senaryoların öznel olasılığı toplam %15–20.
- Sermaye zaten USD'deyse 1. yıl USD nakdin biraz altında biter. Fark, maruziyet sayesinde öğrenilen bilgidir.

### 9.3 Servete etkisi

E = servetin %10'u varsayımıyla [H, kaba]:
- **Beklenen maliyet (TL'de kalmaya göre):**
  - Aşama 1'de (%40 USD) yılda servetin ~%0,3–0,8'i.
  - Tam çevrimde ~%0,9–1,6. E %15 ise ~1,5 katı.
  - Kademeli çevrim bu maliyeti küçültür.
- **Kötü durum:** plan −%8 E'de durur, yani servetin −%0,8'i. Buna o yılın TL'ye göre fırsat maliyeti (~%0,4–0,6) eklenince toplam ~**−%1,5**. Önceki sürümde bu ~−%2,5'ti.
- **Karşılığında alınan:**
  - (i) ~%7–10 olasılıkla 2. yıldan itibaren ölçeklenebilir bir kenar opsiyonu (HD §2.4).
  - (ii) TL şokuna karşı çeşitlendirme. 2018–26'da kurun ≥ %45 arttığı yıllar 2/9 (VC #21). Bu sigorta ortodoks rejimde pahalı.
- **Asıl risk** servetin %85–90'ının durduğu TL tarafında: carry 2010–26'da −%7,2/yıl, en büyük düşüşü −%85. Bunu yöneten kural döviz anahtarı (§1.5).

### 9.4 Kanıttan sonra (Faz 3, yıllık) [H, kaba MC]

HD §4.2 modeli: isabet %30, kayıpların %10'u gap'li −2R, dalgaların %30'unda küme birlikte bozuluyor. Faz 3 merdiveni (−%5 / −%8 / −%11 / dur −%15) C'ninkine eşdeğer.

| Kenar, işlem/yıl, risk | Merdivensiz: medyan / %5 kötü düşüş | Merdivenli: medyan / %5 kötü düşüş |
|---|---|---|
| 0R, 85, %1 (şans) | −%4,7 / −%40 | −%4,3 / −%15 |
| +0,15R, 150, %1 | +%15 / −%49 | +%3,5 / −%15 |
| +0,3R, 85, %0,75–1 | +%15–20 / −%29…−%38 | **+%7,5–9 / −%14…−%15** |
| +0,3R, 150, %1 | +%39 / −%46 | **+%16 / −%15** |
| +0,45R, 150, %1 | +%72 / −%43 | +%29 / −%15 |

**Okuma:**
- Bu planın temposunda (yılda 60–120 işlem) Faz 3'ün dürüst merkezi **~%8–16**. C'nin "+%17–30"u merdiveni ve kümelenmeyi yok sayıyordu (HD §3.3).
- Kenar yokken bile %10 olasılıkla +%24–36'lık bir yıl gelebilir. Kapıların t istatistiğine bağlı olması bu yüzden (HD §4.2 #3).
- %7,5–10'luk tek pozisyon tavanı bu tabloda modellenmedi; sağ kuyruğu biraz kırpar.

### 9.5 "Yüksek ödül" sorusuna dürüst cevap

- **Doğrulanmış sağ kuyruk gerçek.** Aracı kurum ekstreli USIC sonuçları: Luk 2024 +%283, 2025 +%970; Minervini 2021 +%334,8; Kell 2020 +%941 (VA #13–14 [D]).
- **Payda kötü:** katılımcıların yalnız %8–17'si kârda (VA #14). Luk ve Minervini'nin işlem istatistikleri doğrulanamadı (VA #15; VP A3).
- **Bu sonuçların girdileri:** işlem başı **%0,25–1** risk (VP A1; KT2 küçük #22), yılda 150–400 işlem, progresif boyut, güçlü tema rejimi ve çoğunlukla gün içi giriş ve stop (ORH, günün dibi; VP eksik #8).
- **Bu plan sağ kuyruğu açık tutar:** S1/S2 aynı DNA'yı taşır; G1 kanıt gelirse canlıya geçer.
- **Ama sağ kuyruğu kanıttan önce satın almaz.** Medyanı %40+ olan yıl üç şartın birlikteliğini ister: ≥ +0,3R kanıtlı kenar, yılda ≥ 150 işlem ve merdivensiz, %5 olasılıklı ~−%45 düşüşü kabul etmek (HD §4.2).
- Bu kenarın bu kullanıcıda var olma olasılığı ~%7–10 [Ö]. Planın amacı, kullanıcının o kuyrukta olup olmadığını **en ucuz şekilde** öğrenmek.

### 9.6 En büyük belirsizlikler

1. S1/S2'nin EOD uyarlamasının hiç backtest'i yok (VA §4.2; TEST §8).
2. Öznel senaryo ağırlıkları ve kalibre edilmemiş Monte Carlo (VP #11).
3. 2026 vergi tarifesi, elde tutulan USD'nin kur farkının vergisizliği ve wash-sale benzeri kural yokluğu teyitsiz.
4. Kurun yönü engeli 0 ile ~26 puan arasında oynatıyor.
5. Rejim bugün düşmanca. İlk 1–3 ayda işlem sayısı düşük olacak (KT1: tahminen 10–20), dolayısıyla öğrenme hızı da düşük.
6. IBKR emir mekaniği (OCA'ya MOO/MOC eklemek, seans dışında MOO kabulü, saatli GTD, emir değeri ön ayarı, nakit hesap kuralları) bellekten yazıldı. Pazartesi'den itibaren testlerle doğrulanır (§6.2).

---

## 10. Pazartesi 09.11.2026: kontrol listesi

**Cuma 06.11 (bugün):**
- [ ] Midas başvurusu (kimlik + selfie). Onaylanırsa yalnız ≤ 500 $ test parası.
- [ ] IBKR Pro başvurusu: **nakit hesap (cash)**; işlem izni yalnız "Stocks – United States". Opsiyon, vadeli ve margin izni isteme. VİOP tecrübesini türev deneyimi olarak beyan et.
- [ ] W-8BEN.
- [ ] IBKR'ye yazılı sorular:
  - Hangi IBKR şirketine bağlanacağım (IB LLC / IBIE)? ABD ETF erişimi?
  - Nakit hesapta PDT uygulanmadığını teyit edin; hesabım yeni FINRA kuralında mı?
  - MOO ve MOC son giriş saatleri; seans dışında girilen MOO kabul ediliyor mu?
  - Bekleyen MOO/MOC bir stopla aynı OCA grubuna konabilir mi? Ana emri ekli stoplu emirler OCA grubuna konabilir mi?
  - Saatli GTD; emir değeri ön ayarı.

**Cumartesi–Pazar (07–08.11):**
- [ ] Cuma kapanışıyla rejim tablosu (§2.5–2.6; PINE `ABD_RJ`; önce 05.11 değerleriyle karşılaştır). Not et:
  - S&P / 200 GHO (~7.327; yakın bölge < 1,02); S&P ve NDX 10/20 GHO.
  - **VIX/VIX3M** (≥ 1,00 → KIRMIZI).
  - S5FI / S5TH (grafikte teyit), MAHQ − MALQ, RSP / 50 GHO.
  - Ralli denemesinin 1. günü oldu mu?
- [ ] NFP sonucu; İran/Hürmüz ve Senato sonuçları (HAZ §6). BRK-B bilançosu (07.11).
- [ ] **E kararı yazılı:** E = servet × %10 (en çok %15) = ____ $. Şimdi USD'ye: E × %40 = ____ $ (IBKR nakit hesap). TL'de: E × %10 = ____ $ karşılığı PPF, E × %50 = ____ $ karşılığı 32 günlük mevduat. Sermaye zaten USD'deyse çevrim yok.
- [ ] **Dur eşiği yazılı:** −%8 E = ____ $ (NLV'nin −%20'si). Kademe 1 / 2 / 3: −%3 / −%5 / −%6,5 E = ____ / ____ / ____ $.
- [ ] Hipotez kartları S1, S2, G1, G2 (§8.1); tarihli ve değiştirilemez.
- [ ] Günlük şablonu (§8.2): canlı, gölge, test, "kaçan sinyaller", "haftalık uyum" sekmeleri.
- [ ] Taramalar (a) ve (d). İzinli kümeler (§4.3). Küme başına ilk 5 (§4.4).
- [ ] **Korelasyonlar** (§4.1 e): sağlık, K4/K5, faiz duyarlı süper-küme, K8, K9; 60 günlük.
- [ ] Her aday için: kurulum, pivot, tetik, limit, stop, stop %, stop/ATR (1,0–2,0 ve ≤ %8), ADR%20, adet (limite göre; 50k / 250k / 1m; ≤ %7,5 E), alt lotlar, bilanço ve ikili olay tarihi. Şartı sağlamayanı ele.
- [ ] Teyit:
  - U, EW, SN, BDX'te G1 1. gün kriterleri.
  - Perakende satış tarihi (17.11 / 25.11).
  - UMich (13.11).
- [ ] Mali müşavire randevu (§6.5 soruları; wash-sale ve kazanç hasadı dahil).

**Pazartesi 08:00–12:00 TSİ:**
- [ ] IBKR onaylandıysa **USD SWIFT bu sabah**, bankanın kesim saatinden önce. Önce küçük bir tutarla kur makasını ölç. Bakiye Salı–Çarşamba görünür.
- [ ] Midas onaylandıysa ≤ 500 $ ile makası ölç.
- [ ] TL'de bekleyen payı yerleştir: E'nin %10'u banka iştiraki PPF, %50'si 32 günlük mevduat.
- [ ] Gece bilançoları; G1 gölge kaydı (yeni filtre).

**Pazartesi 16:45–17:15 TSİ:**
- [ ] **Canlı strateji emri yok.**
- [ ] Hesap fonluysa **T1 testleri** (§6.2). Fonlu değilse testler fonlanan ilk günden başlar (T1 → T2 → T3).
- [ ] **Midas'ta da aynı testler.** Ekli stop, MOO ya da OCA yoksa Midas S1/S2 için kullanılmaz.
- [ ] Opsiyon: **kapalı.**

**17:30–00:00 TSİ:** ekran yok.

**Salı 10.11 (CPI):**
- [ ] 16:45'ten önce emir yok; vadeli ±%1,5 kuralı.
- [ ] MDT'de giriş yasağı başlıyor.

**Çarşamba 11.11:**
- [ ] Kapanış: FTD oldu mu? SARI sayacı 1 mi?

**Perşembe 12.11:**
- [ ] TCMB rezervi → döviz anahtarı (§1.5).
- [ ] Pilot yok (SARI sayacı en çok 2).

**Cumartesi 14.11:**
- [ ] Haftalık inceleme ve uyum satırı. **Kuralları değiştirme**; değişiklik yeni bir hipotez kartıdır.
- [ ] 13.11 SARI olduysa Pazartesi 16.11 pilot adayı: 1 isim (yakın bölge), AI dışı, K9 dışı kümede tetik FTD ya da S&P 10 > 20.

**Asla (kritik ihlal; DUR-6a):**
- [ ] AI çip veya güç dip alımı.
- [ ] Bilanço ya da ikili olay öncesi yeni giriş.
- [ ] Zarardaki pozisyona ekleme; stopu aşağı çekme.
- [ ] Girişte 1,25R'nin, işlem başı %1'in üstünde risk.
- [ ] Opsiyon (Faz 1), margin, açığa satış, kaldıraçlı ETF.
- [ ] 17:30–00:00 arası emir değiştirmek.

---

## 11. İzlenebilirlik ve açık sorular

### 11.1 Kural → kanıt tablosu

| # | Kural | Dayanak (dosya § bölüm) | Kanıt gücü | Beklenen etki ve belirsizlik |
|---|---|---|---|---|
| 1 | E = servetin %10'u (≤ %15); ölçek yalnız Faz 3'te | VA §4.2; VA #14; SEY §3.3, §3.7, §5.3 #4; HD §2.4 | [D] taban oranlar; [H] maliyet | Servete maliyet yılda ~%0,3–1,6; kötü durum ~−%1,5 |
| 2 | Kademeli çevrim (%40 → %50 → %70 → %100); TL payı PPF + mevduat | HD aşı 3; B §1.3; A C2; VA #34; KT2 küçük #19, #24 | [H] | Boştaki USD'nin yıllık ~9–12 puanlık fırsat maliyetini azaltır; TL kuyruk riskini korur |
| 3 | Boştaki USD nakitte, T-bill'de değil | PRA §2.5, §4.2; HD §2.3, §6 #2; KT2 Ö-1 | [K], müşavir teyidi | Küçük hesapta başa başa yakın; tutar küçük |
| 4 | Döviz anahtarı (5 tetikten 2'si); ek USD Türk bankasında | TRM §5.1; VC #18, #21; KT1 #7 | [D] veriler; [Ö] eşikler | İşlem kenarından bağımsız; servetin büyük kısmının riskini yönetir |
| 5 | KIRMIZI: VIX/VIX3M ≥ 1, S&P 2 kapanış < 200 GHO, genişlik | HAZ §3, §5d; VP A11; PRA §3.6 | [D] veriler; [K] VIX zayıf | Sol kuyruğu keser; yanlış alarm oranı bilinmiyor |
| 6 | Pilot yalnız FTD (+%1,5) ya da 10 > 20 ile | PROF §1.4, §3.5 #6; SEY §5.1 #4; HAZ §3 | [P] | Dipten çıkışın ilk %5–10'u kaçırılır |
| 7 | Rejim filtresi birincil | KIM §5.1; VA #16–17, #27; PROF §3.3; KT1 #3 | [D] FFTY / D-M; [P] Kullamägi; [H] endeks düzeyinde getiri korumadı | Çöküş yıllarında değer; sakin yılda maliyet |
| 8 | Risk %0,25 → %0,5 → %0,75; asla > %1 | PROF §3.5 #1; KIM §5.3; VA #37 | [D] seri matematiği; [P] | %0,25'te 15 ardışık kayıp ≈ −%3,7 |
| 9 | Stop 1,0–2,0 ATR ve ≤ %8, yapısal | PROF §1.3 #3; VP A12 | [P] + [K] | EOD'de dar stopun kötü sonucundan kaçınma; test edilmedi |
| 10 | Adet limite göre | HU §2.2 | Aritmetik | Gap'te riskin 1R'yi aşmasını önler |
| 11 | Seans öncesi buy-stop-limit, kovalamak yok | PROF §1.1; KEN §3 (gece momentumu) | [P] + [D] (KEN) | Kaçan sinyal maliyeti "kaçan" sekmesinde ölçülür |
| 12 | Kısmi satış (+2R ya da 4. seansta ≥ +1R), lot A MOO, başabaş | PROF §1.3 #7–8; VP A1 | [P] öz beyan | Isıyı boşaltır; R dağılımını kırpar |
| 13 | Kapanış bazlı 10/20 GHO trail | VP A1, A12; PROF §3.5 #9 | [P] | Sağ kuyruğu korur; EOD'de gecikme |
| 14 | Zaman stopu (10 seans, son 5 seansta yeni zirve kapanış yok), başarısız kırılım (3 seans) | PROF §1.3 #3; A §2.1, §2.4; KT2 küçük #17 | [Ö] | Isı ve fırsat maliyetini azaltır; test edilmedi |
| 15 | Faz 1'de bilançoya taşımak yok; MOC + OCA; earnings size | PROF §1.3 #9, §3.5 #5; PRA §3.6 #4; KT2 K-1 | [P] | Gap kuyruğunu keser |
| 16 | Piramit yalnız kazanana, Faz 2+ YEŞİL | PROF §1.3 #6, §0 #1 | [P] | Sağ kuyruğu büyütür; kanıt gelene kadar kapalı |
| 17 | Küme tanımı (ρ ≥ 0,6); AI tek küme; sağlık ve faiz duyarlı süper-kümeler | PROF §3.2, §3.5 #2; SEY §3.6; VP A14; KT1 #8 | [D] matematik; [K] 0,72 | 5 pozisyon ≈ 1,2–1,5 bağımsız bahis |
| 18 | Küme ısısı %0,75 / %1,5; ilişkili kümeler %1,25 | PROF §3.1, §3.3, §3.5 #3 | [H] MC | Kümelenme kuyruğu ~%35–40 büyütüyor |
| 19 | Toplam ısı (gap-ayarlı) 1,25/2,5 → 2,5/5 → 3/6 | PROF §3.5 #4, §1.4; KT2 küçük #20 | [P] (Elder) | Tavanlar artık ulaşılabilir değerler |
| 20 | Gap-ayarlı ısı ve en kötü hafta tavanı | PROF §3.5 #5; HU §2.4; HAZ §0 | [P] + [Ö] | Faz 1 YEŞİL'de en kötü hafta ≈ E'nin −%6'sı |
| 21 | Aylık devre kesici %3 (Faz 1); net gerçekleşen zarar tanımı | PROF §3.5 #8; KT2 küçük #20 | [P] (Elder) | — |
| 22 | Düşüş merdiveni −3 / −5 / −6,5; dur −%8 E (Faz 1) | SEY §5.2 #1, #8; PROF §3.3, §3.5 #7; KIM §5.3; B §5.3; KT1 #1 | [H] MC | %5 kötü düşüş −%8,3 → −%7,2; yanlış durdurma %1–5 |
| 23 | Küme izni = filtre, kenar değil | VA §2.2, §3.1; VD U3, U4, U7; DLG §0.4 | [D] | Getiriye katkı ~0; kırık temadan uzak tutar |
| 24 | Dikey sıçramadan sonra kovalamak yok; +%100'de 1/2 sat | DLG §0.5, §5; VD U8, U9 | [H] sektör düzeyi | Hisse düzeyinde test yok |
| 25 | AI dönüş kuralı | DLG §0.7, §7.4; A §4.5 | [H] + [Ö] | Erken dönüşü kaçırabilir (D-M toparlanması) |
| 26 | Bilanço eleme filtresi | KEN §4; TEST §0 #8, §6.4 | [D] (uzun-kısa); sadece-uzun ≈ 0 | Alfa değil, kötü kuyruk elemesi |
| 27 | G1 gölgede; sabah filtresi | VA #23; TEST §6.4, §8; KEN §4.1; KT2 Ö-4 | Kanıt zayıf | Sağ kuyruk kaynağını açık tutar |
| 28 | G2 gölgede | C §2.3 (C-TEST); HU §3 C1; HK C1; HD §3.3 | [H] örneklem içi | Olay başına E'nin +%0,1–0,5'i; asıl işi rejim bilgisi |
| 29 | Insider ertelendi | VA #26; HU §3 C3 | Yayın sonrası test yok | Beklenen değeri ~0 |
| 30 | Opsiyon kapalı ve şartlı; IBKR'de izin yok | VP A6–A8; PROF §0.6, §2.3; KT1 #2 | [D] | Ortalama alıcı kaybeder |
| 31 | Kaldıraçlı çekirdek yok | VA §2.1; TEST §0 #1–3; HK B1–B2; HU §3 B | [D] | 2010 sonrası filtre getiriyi kesti; profil |
| 32 | IBKR ana; yüzdesel komisyonlu kurumlar dışarıda; Gedik yedek | VC #16; HAZ §1.2; C §5.3; KT2 küçük #10 | [D] tarifeler | Yüzdesel kurumlarda 0,07–0,2R; Gedik 0,015–0,04R |
| 33 | 2 adetlik emir testleri; Midas yalnız test | HAZ §1.2, §7; KT1 #2; KT2 küçük #18 | Erişim teyitsiz | Ekransız korumasız pozisyonu önler |
| 34 | Veri günü kuralı (16:45 ve ±%1,5) | C §3.4; HU §4 #2 | [Ö] | Olay gap'ine girişi azaltır |
| 35 | Vergi kaydı; kısa vergi yılı 2026; kazanç hasadı | VC #10–12; PRA §2.1; KT1 #6 | [D] kurallar; [K] tarife ve wash-sale | Zarar devretmez; dışbükeylik −0,4 puan; hasat E'nin ~%0,45–1,05'i |
| 36 | Hipotez kartı, N, t kapıları, kaçan sinyaller | SEY §3.7, §5.3; VA #37 | [D] matematik | Şansla ölçek büyütmeyi önler |
| 37 | Öldürme DUR-1…DUR-10 | SEY §5.2, §5.3 #6; A K6–K7; C §7.4 | Önceden yazılı | Kayıp serisi tek başına öldürme nedeni değil |
| 38 | Limitler E ve NLV ile yazılır | KT1 #1, #12 | Aritmetik | Payda yanılgısını ve intikam işlemini azaltır |
| 39 | Kritik ihlal freni (DUR-6a) ve teknik kilitler | KT1 #2; KIM §6, §5.3; VA #16; VP A6–A7 | [D] opsiyon alıcısı kaybı; [Ö] yaptırım; [H] MC | İhlal yolunda P(NLV ≤ −%15) ~%38; kuralın amacı bu yolu kapatmak |
| 40 | SARI için 3 kapanış; pilot freni; yakın bölgede tek pozisyon | KT1 #3; PROF §1.3 #11, §3.1 | [H] n = 17, örneklem içi | Kısa SARI bölümleri yılda 1,9 → 1,0; çeyrekte ~%0,5–1,5 E'lik whipsaw kaybını yarılar [H] |
| 41 | IBKR nakit hesap; bekleyen emir tavanı; OCA'lı satışlar | KT1 #4, #10; KT2 K-1, K-2, Ö-3; VC #15–16; PRA §1.4 | [D] PDT/margin kuralları; emir mekaniği teyitsiz | Kural dışı maruziyet, borç ve açığa satış ~0; bedeli kaçan sinyaller |
| 42 | Tek pozisyon ≤ %7,5 E; ikili olay yasağı; yönetilen sağlık dışarıda | KT1 #5; PROF §3.1; KIM §6; PRA §3.6 #3 | [P] + [Ö] | −%40 gap'te kayıp −%6 → −%3 E; MC'de küçük etki |
| 43 | Savunmacı kümelerde S&P/FTD tetiği; K6+K7+K10 tek küme; korelasyon ilk girişten önce | KT1 #8; PROF §3.5 #2 | [H] zayıf (2010 sonrası 35 olay −%0,66) | — |
| 44 | Çıkışlar kapanış bloğunda; stop mutabakatı | KT1 #9 | [Ö] | BIST/VİOP çakışmasını kaldırır |
| 45 | 22:00 olayında GTD 21:55; 8.12 makro gap ısısı | KT1 #11; PROF §3.5 #5 | [Ö] | Olay sıçramasında ters dolumu önler |
| 46 | IBKR faiz kademeleri; 1. yıl tablosu nakitsiz | KT2 Ö-1; IBKR faiz sayfası | [D] | 50k'da nakit katkısı ~0; merkez +%1–4 → −%1,5…+%1,5 |
| 47 | 50k'da Pine Screener yok | KT2 Ö-2; TradingView fiyat sayfası | [D] | E'nin %1,4'ü kadar maliyetten kaçınma |

### 11.2 Taslaklardan alınanlar ve düzeltilen kusurlar

**Alınanlar:**
- **C'den (iskelet):**
  - Boyuta ve u'ya bağlı engel, hayalet vergi, döviz anahtarı.
  - Faz 1 risk kabuğu, t kapıları, DUR-1…DUR-8.
  - ±%1,5 veri kuralı.
  - Bilanço eleme filtresi, kaçan sinyaller sekmesi.
- **A'dan:**
  - S1 ve S2 (geri çekilme) mekaniği, EOD çıkışlar (kısmi, trail, zaman stopu, başarısız kırılım, acil stop).
  - Stop-market tercihi, OCA uyarısı.
  - AI dönüş kuralı, A'nın K6/K7'si (burada DUR-9/DUR-10), 50k'da veri maliyeti disiplini, Pine iskeleti.
- **B'den:**
  - Kademeli transfer, boyuta göre vergi sonrası tablo mantığı.
  - Merdivenin yalnız takdirli kolda değer kattığı bulgusu.
  - Pasif beta için TEFAS notu (yalnız araştırma maddesi).

**Düzeltilen kusurlar (hakem turu):**
1. B'nin kaldıraçlı S&P çekirdeği reddedildi. Profile aykırı; beta, kenar değil; 2010–26'da 1x al-tutun altında (HK B1–B2; HD §3.2).
2. C'nin S3 (VIX) kolu gölgeye alındı; başlıktaki t = 3,69 yerine artımsal t ≈ 1,7 yazıldı (HU §3; HK C1).
3. C'nin insider kolu ertelendi (veri 503, yayın sonrası kanıt yok).
4. A'nın bilanço gap'i kolu gölgeye alındı (VA #23; TEST §6.4).
5. Stop tabanı 0,6 / 0,75 ATR'den 1,0 ATR'ye çekildi (VP A12).
6. Boyut tetik yerine limit fiyatından hesaplanıyor (HU §2.2).
7. Bekleyen kısmi limit ile OCA miktar tuzağı yerine kapanışta karar ve MOO kullanılıyor (HU §3). Kırmızı takım sonrası satışlar stopla aynı OCA'da (§3.5).
8. Pilot için FTD ya da 10 > 20 şartı eklendi; TURUNCU durumu getirildi (HK A2/C3; PROF §1.4).
9. FTD eşiği +%1,5'te birleşti (HAZ §3).
10. A'nın boştaki nakit için T-bill önerisi yerine nakit (PRA §2.5).
11. C'nin bütün E'yi hemen çevirmesi yerine kademeli çevrim (HD §3.3 #2).
12. C'nin Faz 3 "+%17–30" beklentisi yerine merdivenli merkez ~%8–16 (HD §4.2).
13. C'deki "50 işlemde riski artır" ile "12 ay ve 100 işlemden önce büyütme yok" çelişkisi: sapma adlandırıldı; E yalnız Faz 3'te artıyor (HK C3; SEY §5.3 #4).
14. Faz 3 için EOD backtest şartı eklendi (HK §7 #5).
15. CDS 248 "doğrulanamadı" olarak işaretlendi. d = %32,9 satırı tahmin değil senaryo (VC §1, #5).

Kırmızı takım düzeltmeleri §12'de.

### 11.3 Açık sorular ve teyit listesi

1. **EOD uyarlaması test edilmedi** (VA §4.2; VP eksik #8). Faz 3'ten önce §8.3'teki backtest şart (Norgate / Sharadar).
2. **Uygulayıcı istatistikleri:** Luk'un isabet/R rakamları ve Minervini'nin isabeti doğrulanamadı (VA #15; VP A3). Kullamägi'nin rakamları öz beyan (VP A1–A2).
3. **IBKR (testlerle ve yazılı soruyla):**
   - Bağlanılacak şirket (IB LLC / IBIE) ve ETF erişimi (bu plan için kritik değil).
   - MOO ve MOC son giriş saatleri; seans dışında MOO kabulü.
   - MOO/MOC'un stopla aynı OCA grubuna konması; ekli stoplu ana emirlerin OCA'ya konması.
   - Saatli GTD; emir değeri ön ayarının adı ve yeri.
   - Nakit hesapta PDT'nin uygulanmaması (VC #15 kuralın margin hesaplarına ilişkin olduğunu söylüyor); yerleşmemiş bedelle alım kuralı.
   - Ekli stopun "yalnız RTH" ayarı.
4. **Midas:** buy-stop-limit, ekli GTC stop, MOO/MOC, OCA, seans öncesi emir girişi ve kur makası kamuya açık sayfalarda yok (HAZ §7).
5. **Vergi:**
   - 2026 tarifesi (VC #11).
   - Elde tutulan USD'nin kur farkı vergisiz mi (PRA §2.5)?
   - Wash-sale benzeri kural yokluğu (kazanç hasadının ön koşulu).
   - TCMB kur türü ve FIFO.
   - "Ticari kazanç" riski.
   - Nakit faizinin beyanı.
   - US-situs veraset vergisi ve aracı kurum nakdinin konumu (VA #36).
   - Kambiyo BSMV (VC: doğrulanamadı).
6. **Takvim:** Perakende satış (17.11 / 25.11; Census listesinde Kasım satırı yoktu), UMich (13.11) (HAZ §7). NVDA (17.11 AMC), BRK-B (07.11) ve MDT (24.11 BMO) tarihleri KT2'de birincil kaynaktan **teyit edildi**.
7. **Veri:** S5FI ve S5TH TradingView önbelleğinden, zaman damgaları karışık (HAZ §7). Küme korelasyonu 0,72 tekrarlanmadı (VP A14). CDS 248 doğrulanamadı (VC §1). MTUM göreli düşüş rakamları doğrulanamadı.
8. **Model:** Bütün Monte Carlo ve dağılım rakamları kalibre edilmemiş (VP #11; HD §8). İleriye dönük hisse primi tartışılmadı (VA §4 #4); kaldıraçsız beta beklentisi muhtemelen 2010–26'dan düşük.
9. **TL tarafı:** yeni alınan DİBS'te stopaj (VC #8). PPF'lerde teminat kalitesi (VP eksik #2). 2027 stopaj takvimi (VC §2 #6).
10. **PINE dosyası** derlenmedi ve test edilmedi.
11. **Araştırma maddesi, kural değil** (HD aşı 10; PRA §2.4; VC #10): Kullanıcı bir gün pasif beta isterse iki seçenek önce değerlendirilmeli; müşavir teyidi şart.
    - TEFAS yabancı hisse fonu: %17,5 nihai stopaj.
    - ≥ 6 ay tutulan lotlarda Yİ-ÜFE endekslemesi: örnekte matrah −%86 düşüyor [H].

---

## 12. Kırmızı takım notları

İki tur: KT1 pre-mortem ("3 ayda ABD hesabının %15–25'i kaybedildi; nasıl?") ve KT2 olgu ve kural denetimi. **Reddedilen bulgu yok.** Üç bulgu değiştirilerek uygulandı; gerekçeleri aşağıda.

### 12.1 KRİTİK ve ÖNEMLİ bulgular

| Bulgu | Karar | Nerede |
|---|---|---|
| KT1 #1 KRİTİK: Payda yanılgısı; −%15 E dur eşiği NLV'nin −%37,5'i ve model p95'inin ~2 katı | **Uygulandı.** Faz 1 merdiveni −%3 / −%5 / −%6,5 (ya da 2 ardışık ay devre kesici); dur −%8 E. Bütün limitler E ve NLV ile yazıldı. **Genişletme:** Faz 2–3 eşikleri aynı ilkeyle (p95) yazıldı ve kapıda bootstrap ile yeniden ölçülecek | §0 #6, §5.2, §5.4, §8.5 DUR-5, §8.6 |
| KT1 #2 KRİTİK: Davranış freni yok | **Uygulandı.** Kritik ihlal listesi; 1. ihlal 10 seans, 2. ihlal plan durur. Opsiyon izni yok, emir değeri ön ayarı, Midas ≤ 500 $, haftalık uyum satırı | §3.9, §6.1, §6.3, §8.2, §8.5 DUR-6a, §10 |
| KT2 K-1 KRİTİK: MOC ile açık stop çakışıyor | **Uygulandı.** MOC ve bütün MOO'lar stopla aynı OCA'da; yedek: son seans açılışında MOO; test T3 | §3.5, §3.6, §6.2 |
| KT2 K-2 KRİTİK: Bekleyen buy-stop'lara tavan yok | **Uygulandı** (KT1 #4 ile birleştirildi). Bekleyen emirler dolmuş sayılır; N formülü; tutar, küme ve ısı kontrolü; OCA grupları. YEŞİL'e günde 3 giriş tavanı eklendi [Ö] | §2.2, §5.1, §6.2 |
| KT1 #3: 200 GHO çevresinde whipsaw | **Uygulandı.** 3 kapanış kuralı, pilot freni, yakın bölgede 1 pozisyon ve ısı ≤ %0,5. İlk pilot 12.11'den 16.11'e kaydı | §0 #2, §2.2, §2.4, §2.6, §2.8 |
| KT1 #4: Birlikte tetiklenen emirler; margin hesap | **Uygulandı.** IBKR nakit hesap | §6.1, §6.2 |
| KT1 #5: Tek isim gap'i ve ikili olay | **Uygulandı.** Tek pozisyon ≤ %7,5 E (Faz 1–2), ≤ %10 (Faz 3); ikili olay yasağı; yönetilen sağlık Faz 1'de dışarıda. Not: Faz 2'de (%0,5 risk) tavan stop < %6,7 iken bağlar; bu bedel bilerek kabul edildi | §3.1, §3.4, §4.2, §5.1, §5.3 |
| KT1 #6: 2026 kısa vergi yılı | **Uygulandı, müşavir teyidine bağlı.** Simetrik durum yalnız müşavir onayıyla eklendi | §6.5, §7.4 |
| KT1 #7: Döviz anahtarının USD'si | **Uygulandı.** Türk bankasında döviz mevduatı | §1.5 |
| KT2 Ö-1: IBKR faiz kademeleri | **Uygulandı.** §1.2 sütunu yeniden hesaplandı. 1. yıl tablosu yeni merdivenle ve nakit faizi olmadan yeniden simüle edildi; TL tarafı ayrı satırda | §1.1, §1.2, §1.6, §9.1, §9.2, §8.6 |
| KT2 Ö-2: Pine Screener yalnız Premium'da | **Uygulandı.** 50k'da finviz + ücretsiz tarayıcı + grafikte `ABD_RJ`; Premium en erken 250k'da | §1.3, §4.1 |
| KT2 Ö-3: PDT geçiş dönemi | **Değiştirilerek uygulandı.** Nakit hesapta PDT uygulanmaz (VC #15 [D]: kural margin hesaplarına ilişkin). Bu yüzden "USD ≥ 25 bin $" şartı yalnız margin hesap kullanılırsa geçerli. IBKR'ye yazılı soru yine sorulur. Gerekçe: 50k'da %50 çevrim TL fırsat maliyetini E'nin yılda ~%1'i kadar artırırdı | §6.1, §10 |
| KT2 Ö-4: G1 sabah filtresi yanlış | **Uygulandı** | §3.8, §4.1, RUTİN |

### 12.2 KÜÇÜK bulgular

| Bulgu | Karar | Nerede |
|---|---|---|
| KT1 #8: Tetik ile evren uyumsuz; K6+K7+K10 aynı faktör | Uygulandı. K9 dışındaki bütün kümelerde tetik FTD ya da S&P 10 > 20; K8 de buna dahil edildi (NDX tetiği teknoloji ağırlıklı). Faiz duyarlı süper-küme; korelasyon 07–08.11'de | §2.2, §4.1, §4.2 |
| KT1 #9: Emir penceresi BIST ile çakışıyor | Uygulandı. Ek: kapanış bloğu gece 00:30–01:00'da da yapılabilir (VIX kapanışından sonra) | §3.5, §6.3, RUTİN |
| KT1 #10: Kısmi MOO reddedilirse yarım pozisyon stopsuz | **Değiştirilerek uygulandı.** Alt lotlar girişte iki ana emirle değil, dolumdan sonraki ilk kapanış bloğunda stop bölünerek kurulur. Gerekçe: Girişte iki ana emir, fazla adayların OCA grubuyla çakışır; OCA ikinci alt lotu iptal eder. Stoplar yalnız RTH'de tetiklendiği için seans dışında bölmek korumasız an yaratmaz. İki yedek yöntem tanımlandı | §3.4, §3.5, §6.2 |
| KT1 #11: 22:00 olay günleri ve 9–11.12 | Uygulandı. GTD 21:55; 8.12 makro gap ısısı. **Değişiklik:** "S&P ima hareketi" opsiyon verisi aboneliği gerekmesin diye VIX'ten türetildi | §5.3, §6.2, §7 |
| KT1 #12: TL algısı | Uygulandı. Çeyrek içinde TL kıyasıyla karar yok; rapor USD, % E, % NLV; makas ilk transferde ölçülür | §1.4, §8.5 DUR-10, §8.6 |
| KT2 #1–3: NVDA 17.11 (01:00 TSİ 18.11), BRK-B 07.11, MDT 24.11 BMO | Uygulandı; "teyit/çelişki" notları silindi | §4.5, §7, §11.3 |
| KT2 #4: CSPX 11:00–19:30 TSİ | Uygulandı | §8.4 |
| KT2 #5: 1 aylık zımni getiri ~%32–33 | Uygulandı | §1.1, §1.5 |
| KT2 #6: Hayalet vergi yıl sonu kuruyla %0,75 / %1,10 / %1,55 | Uygulandı | §1.2 |
| KT2 #7: +%100 kuralı | Uygulandı: 1/2 sat + kalanına %10 trail, etiket [H, sektör düzeyi] | §3.5 |
| KT2 #8–9: MTUM [K]; "NDX 10 < 20" KIRMIZI koşulu değil | Uygulandı | §0 #1, §2.5 |
| KT2 #10: Gedik lot başı ücret | Uygulandı | §3.4, §6.1, §6.4 |
| KT2 #11–12: Baz derinliği; "sınırda izinli" yok, K6 = yalnız BJ | Uygulandı | §3.2, §4.3 |
| KT2 #13: 2,3–6,4 yıl | Uygulandı | §1.3 |
| KT2 #14: Norgate / Sharadar | Uygulandı | §8.3 |
| KT2 #15–16: IDXX penceresi; LLY kuralının yeri | Uygulandı | §4.5, §7.1 |
| KT2 #17: Zaman stopu ifadesi | Uygulandı | §3.5 |
| KT2 #18: Test sırası açık pozisyon gerektiriyor | Uygulandı: T1–T3, 2 adetle | §6.2 |
| KT2 #19: Sonraki dilim PPF'de | Uygulandı | §1.4 |
| KT2 #20: Isı tavanları ulaşılamaz; "gerçekleşen zarar" tanımı | Uygulandı | §2.2, §5.1 |
| KT2 #21: Faz 2→3 kapısında vergi öncesi kıyas | Uygulandı | §8.3 |
| KT2 #22: "%1 risk" → %0,25–1 | Uygulandı | §9.5 |
| KT2 #23: Kullamägi −%57'nin dönemi | Uygulandı | §2.8 |
| KT2 #24: %40 çevrimin gerekçesi | Uygulandı: gerekçe "pilot hazırlığı" olarak yazıldı; ilk SARI'ya bağlamak SWIFT süresi yüzünden ilk pilotu 1–2 gün geciktirirdi | §1.4 |

### 12.3 Bu revizyonda ayrıca

- Öldürme kriterleri K1–K10 → DUR-1…DUR-10 olarak yeniden adlandırıldı; kümelerle (K1–K11) karışıyordu. Eski K6, DUR-6a (kritik) ve DUR-6b (diğer) olarak ikiye ayrıldı.
- Rejim girdilerindeki G1–G5 kodları kaldırıldı; gölge kollarla (G1–G3) karışıyordu.
- Pine betiği v5'e taşındı ve ayrı dosyaya alındı (PINE): rejim, 3 kapanış sayacı, trend şablonu, korelasyon ve emir hesaplayıcı. **Derlenmedi, test edilmedi.**
- Tek sayfalık günlük rutin yazıldı (RUTİN).
- KT1'in MC sonuçları (§8.5 alt notu) ve whipsaw testi (§2.8) kalibre değil; n küçük; yalnız göreli büyüklük olarak okunmalı.
