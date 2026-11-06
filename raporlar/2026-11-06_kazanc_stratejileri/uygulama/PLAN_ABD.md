# ABD Swing Planı (nihai): 9 Kasım 2026'dan itibaren

**Hazırlanma:** Cuma 06.11.2026, ~14:00 TSİ. Son kapanış Perşembe 05.11.2026.
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
- Düzeltilen bütün kusurlar §11.2'de.

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

**Etiketler:**
- **[D]** Doğrulama turunda DOĞRU çıktı.
- **[K]** Kısmen doğru ya da doğrulanamadı.
- **[P]** Uygulayıcı kuralı veya öz beyan; akademik testi yok.
- **[H]** Hesap (taslak, hakem ya da bu dosya). Kalibre edilmemiş; yalnız göreli büyüklük olarak okunmalı (VP eksik #11).
- **[Ö]** Tasarım seçimi ya da öznel tahmin.

---

## 0. Yönetici özeti (10 satır)

1. **Pazartesi canlı risk sıfır.** Dört neden var:
   - Rejim KIRMIZI: VIX/VIX3M 1,10 ve NDX'te 10 GHO < 20 GHO.
   - IBKR'de gerçekçi ilk işlem 11–13.11.
   - Midas'ın emir tipleri teyitsiz.
   - Takip günü (FTD) en erken Çarşamba 11.11.

   Pazartesi yapılacaklar: hesap fonlama, 1 adetlik emir testleri, izleme listesi, işlem günlüğü.
2. **İlk canlı pilot en erken Perşembe 12.11'de, 16:45–17:15 TSİ'de girilir.** Koşul: Çarşamba geçerli bir FTD gelmesi ve rejimin SARI'ya dönmesi.
   - Pilot sayısı en çok 2; her biri E'nin %0,25'i riskle.
   - İki pilot farklı ve AI dışı kümelerden.
3. **Sermaye:** Para TL'deyse ABD strateji sermayesi E, likit servetin **%10'u** (en çok %15'i) olur.
   - Şimdi bunun yalnız **%40'ı** USD'ye çevrilir; kalanı TL mevduatta bekler, rejim tetikleriyle taşınır.
   - Para zaten USD'deyse E ≤ servetin %20'si ve çevrim yok.
   - Boştaki USD aracı kurumda nakit kalır; T-bill'e konmaz.
4. **Canlı kol tek:** rejim filtreli lider swing. İki kurulumu var: S1 baz kırılımı ve S2, yükselen 10/20 GHO'ya geri çekilme.
   - Bilanço gap'i (episodic pivot) ve VIX çözülmesi yalnız **gölge** kayıtta.
   - Insider kolu ertelendi; opsiyon kapalı; kaldıraçlı ETF, margin ve açığa satış yok.
5. **Emir rutini:**
   - Bütün emirler her gün 16:45–17:15 TSİ'de girilir.
   - Giriş: BUY STOP-LIMIT (DAY). Koruma: ekli GTC SELL STOP (piyasa, yalnız normal seans).
   - Çıkış kararları kapanışa göre verilir, ertesi açılışta MOO ile uygulanır.
   - 17:30–00:00 arası ekrana bakılmaz.
6. **Risk tavanları (Faz 1, ilk 50 işlem):**
   - İşlem başı risk %0,25. Küme ısısı %0,75.
   - Toplam açık risk: SARI'da %2, YEŞİL'de %3.
   - Aylık devre kesici %3.
   - Strateji zirveden −%15'e düşerse plan durur. E servetin %10'uysa bu servette ~−%1,5 eder.
7. **Engel (TL'den gelen sermaye):** TL'de kalmayı yenmek için gereken vergi öncesi USD getirisi.
   - Planın tipik maruziyetinde (pozisyonda kalma payı u ≈ 0,3): 50k / 250k / 1m $ hesapta **%12,7–19,5 / %15,6–23,3 / %17,5–25,9**.
   - Tam yatırımda ~%17–34; doğrulanmış çapa ~%20–28.
   - USD'den gelen sermayede engel ~%4–6.
8. **1. yıl beklentisi (dürüst):** Vergi öncesi USD medyan, kenara göre −%0,4 ile +%9,1 arası; ağırlıklı merkez **+%1–4**.
   - Vergi sonrası ~%0–2,5, yani USD nakit düzeyi.
   - TL engelini geçme olasılığı **< %5**.
   - Servete maliyet: TL'de kalmaya göre yılda ~%1–2,5.
9. **Yüksek ödül ancak kanıttan sonra gelir.** Faz 3 kapısı: 100 işlem, 12 ay, t ≥ 1,65 ve hayatta kalma yanlılığından arındırılmış gün sonu (EOD) backtest'i.
   - Kapıdan sonra risk %0,75–1'e çıkar; dürüst merkez yine de ~%8–16.
   - Medyanı %40+ olan bir yıl için üç şart gerekir: ≥+0,3R kenar, yılda ≥150 işlem ve %5 olasılıkla ~−%45'lik düşüşü kabul etmek.
   - Böyle bir kenarın bulunma olasılığı ~%7–10.
10. **Kurallar önceden yazılı:** ölçek kapıları ve öldürme kriterleri (§8), döviz anahtarı (§1.5; ilk kontrol Perşembe 12.11 TCMB rezerv verisi), takvim (§7).

---

## 1. Sermaye ve engel kararı

### 1.1 Girdiler (doğrulanmış)

| Kalem | Değer | Kaynak |
|---|---|---|
| TL'de kalmanın net nominal getirisi | Faiz sabit kalırsa ~%36–38 (32 günlük mevduat roll). Anket patikasında ~%31–33 | VC #4 [D] |
| TL'de kalmanın ileriye dönük USD karşılığı | ~%13–15,5. Faiz indirimi ya da kur şoku kuyruğunda %6–12. h=%31/35/37 ve kur +%20 ile **%9,2 / %12,5 / %14,2** | VA #34 [D]; HD §2.1 [H] |
| TL carry'nin geçmişi (USD bazında) | 2010–26: **−%7,2/yıl, en büyük düşüş −%85**. 2020–26: −%10,1/yıl | TEST §0 #10; VA #34 [D] |
| Kur vadelisi | 12 ay zımni ~%32,7–32,9. Bu bir tahmin değil, faiz paritesi (CIP) sonucu; uzak vadeler likit değil. Anketin 12 aylık kur beklentisi 59,26, yani ~%18,4 | VC #3, #5 [D] |
| USD risksiz getiri | 3 aylık T-bill %4,03 (iskonto), 13 hafta kupon eşdeğeri %4,10. IBKR boş nakit faizi %3,38 | VC #13 [D]; PRA §4.1 |
| ABD kazancının TR vergisi | Değer artışı olarak, TL bazında ve **kur farkı dahil** beyan edilir; artan oran %15–40. Zarar yalnız aynı yıl içinde mahsup edilir, devretmez. Yİ-ÜFE endekslemesi yalnız artış ≥%10 ise (~6 ay). Margin faizi indirilemez | VC #10 [D] |
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
- Betik: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/plan_final/at.py` (HD `ev.py` ile aynı model; sonuçlar birebir tuttu).

| E | USD nakit (%3,38), vergi sonrası | TL'yi yenmek için gereken R, u=0,3 (h=%31 / %37) | u=0,6 | u=1,0 | USD kökenli sermayede USD nakde eşit olmak için gereken R (u=0,3 / u=1) |
|---|---|---|---|---|---|
| 50.000 $ | %2,9 | **%12,7 / %19,5** | %14,5 / %21,4 | %17,1 / %24,7 | %4,4 / %8,4 |
| 250.000 $ | %2,7 | **%15,6 / %23,3** | %18,3 / %26,0 | %22,1 / %30,5 | %5,7 / %12,0 |
| 1.000.000 $ | %2,4 | **%17,5 / %25,9** | %20,9 / %29,2 | %25,3 / %33,7 | %6,3 / %14,0 |

**Okuma:**
1. Engel hesap büyüdükçe yükselir (vergi dilimi) ve maruziyet arttıkça yükselir (hayalet vergi). Tam yatırım satırı doğrulanmış çapayla tutarlı: ~%20–28 (VC #22).
2. **Hayalet vergi:** Sıfır USD getiride bile pozisyondaki sermayenin kur farkı vergilenir. u=0,3 ve d=%20 için E'nin ~%0,9 / %1,3 / %1,9'u eder (50k / 250k / 1m). TL karşılığı ~22,5 bin / 165 bin / 934 bin TL (C §1.2; HD §3.3 yeniden hesapladı).
3. d=%32,9 (kur vadelisinin fiyatladığı hız) satırı bir **senaryo**, tahmin değil (VC #5). O hızda ~%0–9'luk getiri yeterdi. Karar bu satıra dayandırılmaz.

### 1.3 Karar

| Durum | E (ABD strateji sermayesi) | Gerekçe |
|---|---|---|
| **Sermaye TL'de** | **Likit servetin %10'u**, en çok %15'i | Dört gerekçe: (a) Bu tarzın EOD uyarlaması hiç test edilmedi (VA §4.2; VP eksik #8). (b) Taban oranlar kötü: USIC'te katılımcıların %8–17'si kârda (VA #14). (c) +0,2–0,3R'lik bir kenarı şanstan ayırmak 280–450 işlem, yani 2–4 yıl ister (SEY §3.7). (d) 1. yıl beklentisi engelin altında (§9); TL'de kalmaya göre maliyet servetin yılda ~%1–2,5'i (HD §0) |
| **Sermaye zaten USD'de** (döviz hesabı, Eurobond) | min(eldeki USD, servetin %20'si). TL'ye çevrim yok; boştaki kısım USD nakitte | Kıyas artık TL değil, USD nakit. u=0,3'te gereken vergi öncesi R ~%4,4–6,3 (§1.2). Risk kuralları aynı kalır |
| **Ölçek büyütme** | E'yi servetin %25–35'ine çıkarmak **yalnız** Faz 3 kapısından sonra (§8.3) | Kenar istatistikle görülmeden sermaye büyütmek "tahmin hatası Kelly'yi öldürür" tuzağıdır (SEY §3.3, §5.3 #4) |

**Çalışılmış örnek (E üç boyutta):**

| | E = 50k $ | E = 250k $ | E = 1m $ |
|---|---|---|---|
| İma ettiği likit servet (%10) | 500k $ | 2,5m $ | 10m $ |
| Şimdi USD'ye çevrilecek (%40) | 20k $ | 100k $ | 400k $ |
| TL'de bekleyen (USD karşılığı) | 30k $ | 150k $ | 600k $ |
| Plan durursa (−%15) servete etkisi | −%1,5 | −%1,5 | −%1,5 |
| Veri ve yazılım | Yalnız TradingView Essential/Plus (12,95–29,95 $/ay) ve ücretsiz finviz: E'nin ~%0,3–0,7'si. Tam set (~1.000–1.300 $/yıl) E'nin %2–2,6'sı, çok yüksek | Tam set: E'nin ~%0,4–0,5'i | Tam set: E'nin ~%0,1'i |
| ABD veraset vergisi (60k $ üstü US-situs varlık) | Pozisyonlar dolarsa sınırda | **Risk var** | **Risk var** |

Veri ve yazılım maliyeti PRA §5'ten, veraset eşiği VA #36'dan.

### 1.4 Kademeli USD çevrimi

Rejimin kullanamayacağı USD boşta beklerse, boşta bekleyen kısım için yıllık fırsat maliyeti ~9–12 puandır (HD §3.1 [H]). Bu yüzden yalnız rejimin brüt tavanı ve %10 tampon USD'ye çevrilir. Dayanak: HD aşı 3; B §1.3; A C2.

| Aşama | Tetik | USD'deki pay (E'nin) | 50k | 250k | 1m |
|---|---|---|---|---|---|
| 1 | Şimdi | **%40** (Faz 1 SARI brüt tavanı %30 + tampon) | 20k | 100k | 400k |
| 2 | İlk YEŞİL kapanış | %50 (Faz 1 YEŞİL brüt tavanı %40 + tampon) | 25k | 125k | 500k |
| 3 | Faz 2 kapısı geçildi | %70 | 35k | 175k | 700k |
| 4 | Faz 3 kapısı geçildi | %100 | 50k | 250k | 1m |

- **TL'de bekleyen pay** büyük bankada 32 günlük mevduatta ya da banka iştiraki bir para piyasası fonunda (PPF) tutulur. Grup ihracı teminatlı fonlardan kaçınılır: PPF risksiz değil (VP eksik #2). Yeni alınan DİBS'in stopajı teyitsiz (VC #8).
- **Transfer:** tetik geldiği gün sabah SWIFT gönderilir; para 1–2 iş gününde ulaşır. Mevcut USD payı, transfer yolda iken yeni girişlere yetecek büyüklükte.
- **USD → TL geri dönüş** yalnız iki durumda yapılır: plan durursa (§8.5 K5) ya da 40 seans boyunca hiç yeni giriş açılamadıysa. Kur makası nedeniyle gidip gelinmez.
- **Risk tabanı (E):** ayın son iş günü güncellenir. E = USD hesap değeri + TL'de bekleyen payın o günkü TCMB kuruyla USD karşılığı. Bütün yüzde riskleri bu E üzerinden hesaplanır.
- **Düşüş merdiveni** yalnız stratejinin USD kâr/zararından ölçülür (§5.2). TL payının kur hareketi merdiveni etkilemez.

### 1.5 Döviz anahtarı (işlem kenarından bağımsız)

Servetin %85–90'ı TL'de kalıyor. Toplam riski en çok etkileyen kural bu yüzden budur (HD §0). Kaynak: TRM §5.1 "carry'den çık / long USD" tetikleri.

**Kural:** Aşağıdaki beş tetikten **ikisi** oluşursa servetin USD nakit payı **%25–35**'e çıkarılır.
- Fazla USD **nakit** olarak tutulur: döviz hesabı ya da aracı kurumda nakit.
- İşlem riski aynı kalır.
- E değişmez.

| Tetik | Bugün | Durum |
|---|---|---|
| Swap hariç net rezerv < 0, ya da 2 hafta üst üste haftalık düşüş > 5 mlr $ | 24,3 mlr $; son hafta −6,5 mlr $ (VC #18 [D]) | Yarısı oluştu |
| Yabancı DİBS çıkışı > 1 mlr $, 2 hafta üst üste | −750 mn $ | Yok |
| CDS 5 yıl > 300 | 248 (**DOĞRULANAMADI**, VC §1) | Yok; kaynağı teyit et |
| 1 aylık USDTRY vadelisinin zımni yıllık getirisi politika faizini 5 puan aşıyor | ~%34; politika faizi %36 | Yok |
| Ex-ante reel faiz < %3 | %9,8 (makul bant %5–8; VC #3) | Yok |

**Perşembe 12.11 rezerv verisi kritik:** ikinci bir >5 mlr $ haftalık düşüş birinci tetiği tamamlar.

### 1.6 Boştaki USD ve nakit

- **Aracı kurumda nakit kalır:** IBKR'de %3,38. T-bill'e ya da para piyasası ETF'ine (SGOV, BIL) **konmaz**.
  - %20 kur artışında T-bill pozisyonunun ~%5–7'si kur farkı vergisine gidebilir; buna karşılık kaybedilen faiz yalnız ~0,65 puan (HD §6 #2; PRA §2.5).
  - Müşavir teyidi şart.
- **IBKR faiz kademeleri:** Küçük hesapta ilk 10 bin $'a faiz ödenmeyebilir; 100 bin $ altında faiz orantılı düşebilir. Bu bilgi bellekten, doğrulanmadı (HK §3.3). 50k'lık hesapta nakit katkısı belirgin küçük olabilir.
- **Faiz geliri** menkul sermaye iradı olarak beyan edilir (PRA §4.1).
- **Veraset vergisi:** ABD hisseleri 60 bin $ üstünde US-situs varlık sayılır (VA #36). Aracı kurum nakdinin konumunu uzmana sorun.

---

## 2. Rejim anahtarı

### 2.1 Girdiler

Her ABD kapanışından sonra hesaplanır; kontrol sabah 08:00–09:00 TSİ.

| Kod | Gösterge | Kaynak |
|---|---|---|
| G1 | S&P 500 kapanışı; 10, 20, 50 ve 200 günlük basit ortalamalar (GHO) | `SP:SPX`, FRED SP500 |
| G2 | Nasdaq-100'ün 10 ve 20 GHO'su ve 1 günlük eğimleri | `NASDAQ:NDX` |
| G3 | VIX/VIX3M kapanış oranı | `CBOE:VIX/CBOE:VIX3M` |
| G4 | S5FI (S&P'de 50 GHO üstü hisse yüzdesi) ve S5TH (200 GHO üstü) | `INDEX:S5FI`, `INDEX:S5TH` |
| G5 | FTD (takip günü; §2.3) | Elle sayım |
| Bilgi | MAHQ − MALQ (Nasdaq 52 haftalık zirve − dip), RSP'nin 50 GHO'ya göre konumu | HAZ §5d |

### 2.2 Durumlar ve izinler

| Durum | Koşul | Yeni canlı giriş | Toplam açık risk, Faz 1 / 2 / 3 | Brüt maruziyet tavanı, Faz 1 / 2 / 3 |
|---|---|---|---|---|
| **KIRMIZI** | Herhangi biri: (a) VIX/VIX3M son iki kapanıştan herhangi birinde ≥ 1,00. (b) S&P 2 kapanış üst üste 200 GHO altında. (c) S5FI < 50 **ve** S5TH < 60 | **Yok.** Yalnız gölge kayıt | Yalnız mevcut pozisyonlar | Yeni giriş yok |
| **TURUNCU** (bekle) | KIRMIZI değil, ama SARI şartı yok | **Yok.** Yalnız gölge kayıt | Mevcutlar; ≤ %1 | Yeni giriş yok |
| **SARI** (pilot) | KIRMIZI değil (yani VIX/VIX3M 2 kapanış üst üste < 1,00) **ve** S&P > 200 GHO **ve** [geçerli FTD **ya da** S&P 10 > 20 GHO **ya da** NDX 10 > 20 GHO] | Günde en çok 2 yeni giriş. En çok 4 açık pozisyon. Kümede 1 pozisyon. Yalnız AI dışı ve izinli kümeler. Kısmi satış 1/2 | %2 / %3 / %3 | %30 / %40 / %50 |
| **YEŞİL** | S&P > 50 GHO ve > 200 GHO; NDX 10 > 20 GHO ve ikisi de yükseliyor; VIX/VIX3M < 0,95; S5FI ≥ 50; ve FTD gerçekleşmiş, FTD günü dibi kapanışla kırılmamış (ya da S&P ve NDX'te 10 > 20 en az 10 seanstır sürüyor) | Faz boyutu. En çok 8 açık pozisyon. Kümede en çok 3 pozisyon. Faz 2+'da piramit. Kısmi satış 1/3 | %3 / %5 / %6 (%6 yalnız yıl içi kâr yastığı ≥ %10 ise) | %40 / %60 / %100 |

- **Margin yok:** brüt tavan hiçbir fazda %100'ü geçmez.
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

- Durum kapanışta hesaplanır. Ertesi gün 16:45 emir penceresinden itibaren geçerlidir.
- **Durum düşerse açık pozisyonlar zorla kapatılmaz.** Yalnız yeni giriş izni değişir. Isı yeni tavanın üstündeyse yeni giriş yapılmaz; mevcutlar kendi stop ve trail kurallarıyla küçülür.
- **İstisna:** S&P 2 kapanış üst üste 200 GHO altındaysa bütün iz süren çıkışlar 10 GHO'ya sıkılaştırılır (A §3.2).
- **KIRMIZI'dan çıkış:** VIX/VIX3M 2 kapanış üst üste < 1,00 **ve** S&P > 200 GHO. Bu şartlar sağlanırsa durum TURUNCU olur; ayrıca FTD ya da 10 > 20 varsa SARI.

### 2.5 Bugünkü okuma (05.11 kapanışı, NFP öncesi)

| Girdi | Değer | Durum |
|---|---|---|
| S&P 500 | 7.353,73 (−%4,36). 200 GHO 7.322,7 (**+%0,4**; yükseliyor, Pazartesi ~7.330). 50 GHO 7.686,5 (−%4,3). 10/20 GHO 7.622 / 7.680 | 200 GHO'nun hemen üstünde, 50'nin altında; 10 < 20 |
| S&P 10 > 20 için gereken | Kabaca 7 seans ≥ 7.735'te ya da 10 seans ≥ 7.625'te kapanış (B §3.3 [H]) | 17.11'den önce olası değil |
| Nasdaq-100 | 26.629,8. 10 / 20 / 50 GHO: 28.672 / 29.286 / 29.686. 200 GHO 27.977 (−%4,8). Zirveden −%14,7. 19.10'dan beri 10 < 20 | Kırık (VP A11 [D]) |
| VIX / VIX3M | 28,18 / 25,55 = **1,10**. 4.11'de VIX 16,61'di: tek günlük sıçrama | **KIRMIZI tetikleyici** |
| VIX/VIX3M < 1,00 için | VIX3M ~25,5 kalırsa VIX ~25,5'in altında kapanmalı. < 0,95 için ~24,3'ün altında (C §2.3) | — |
| S5FI / S5TH | 62,5 / 66,1 (TradingView önbelleği, zaman damgası karışık; HAZ §3) | Kırmızı değil; teyit et |
| MAHQ − MALQ | 150 − 490 = −340 | Büyüme tarafı zayıf |
| RSP | 50 GHO'nun +%0,7 üstünde; zirveden −%3,5 | Savunmacı genişlik ayakta |
| FTD | Yok; ralli denemesi başlamadı | — |
| Bağlam | MTUM'da rekor göreli düşüş (Temmuz 2026 −%15,5; Ekim −%8,7). Liderlik sağlık, borsalar, sigorta, temel tüketim, atık/su ve konaklamaya döndü. Fed %3,75–4,00; 10 yıllık getiri %4,84–4,90 | PRA §3.4; HAZ §0, §3 |
| **Sonuç** | **KIRMIZI** (koşul a). Yeni canlı giriş yok. Opsiyon kapalı | |

### 2.6 Cuma 06.11 kapanışı → Pazartesi kararı

Okuma Cumartesi sabahı yapılır.

| Cuma kapanışında | Pazartesi durumu | Pazartesi | En erken canlı pilot |
|---|---|---|---|
| VIX/VIX3M ≥ 1,00 | KIRMIZI | Canlı giriş yok | Rejime ve FTD'ye bağlı; en erken Pe 12.11 |
| VIX/VIX3M < 1,00 (ilk kapanış) | KIRMIZI sürer: 5.11'de oran 1,10, iki kapanış şartı | Canlı giriş yok | Pazartesi de < 1 olursa Pazartesi kapanışından itibaren TURUNCU. SARI için ayrıca FTD ya da 10 > 20 gerekir |
| S&P ≤ 200 GHO (~7.327) | KIRMIZI riski: ikinci kapanış altta olursa | Canlı giriş yok | — |
| S&P artıda | Ralli denemesinin 1. günü 6.11 | FTD en erken **Ça 11.11** kapanışı | **Pe 12.11, 16:45–17:15** |
| S&P yeni dip yaptı | Sayım başlamadı | FTD en erken Pe 12.11 | Cu 13.11 (PPI sonrası, 16:45'ten sonra) |

**Sonuç: Pazartesi hiçbir koşulda canlı giriş yok.** Bu sonuç üç hakemin ortak hükmüyle aynı (HK §5; HU §6; HD §7).

### 2.7 TradingView rejim göstergesi (Pine v6)

Bu gösterge A §3.2'deki betiğin bu plana uyarlanmış hâlidir. Bu oturumda derlenmedi; önce kâğıt üzerinde doğrulanmalı. Semboller HAZ §5d'de teyitli.

```pine
//@version=6
indicator("ABD_Rejim_Nihai", overlay=false)
ftd      = input.bool(false, "Geçerli FTD (ya da S&P ve NDX'te >=10 seans 10>20) var mı? (elle)")
ftdBroke = input.bool(false, "FTD günü dibi kapanışla kırıldı mı? (elle)")
[spx, spx10, spx20, spx50, spx200, spx1, spx200p] = request.security("SP:SPX", "D", [close, ta.sma(close,10), ta.sma(close,20), ta.sma(close,50), ta.sma(close,200), close[1], ta.sma(close,200)[1]])
[ndx10, ndx20, ndx10p, ndx20p] = request.security("NASDAQ:NDX", "D", [ta.sma(close,10), ta.sma(close,20), ta.sma(close,10)[1], ta.sma(close,20)[1]])
vix  = request.security("CBOE:VIX",   "D", close)
vix3 = request.security("CBOE:VIX3M", "D", close)
s5fi = request.security("INDEX:S5FI", "D", close)
s5th = request.security("INDEX:S5TH", "D", close)
ratio  = vix / vix3
red    = ratio >= 1.0 or ratio[1] >= 1.0 or (spx < spx200 and spx1 < spx200p) or (s5fi < 50 and s5th < 60)
trig   = ftd or spx10 > spx20 or ndx10 > ndx20
yellow = not red and spx > spx200 and trig
green  = not red and spx > spx50 and spx > spx200 and ndx10 > ndx20 and ndx10 > ndx10p and ndx20 > ndx20p and ratio < 0.95 and s5fi >= 50 and ftd and not ftdBroke
lvl    = green ? 3 : yellow ? 2 : red ? 0 : 1
plot(lvl,   "0=KIRMIZI 1=TURUNCU 2=SARI 3=YESIL", color=color.blue, linewidth=3, style=plot.style_stepline)
plot(ratio, "VIX/VIX3M", color=color.red)
hline(1.0)
hline(0.95)
```

### 2.8 Kanıt ve belirsizlik

**Kanıt:**
- **Rejim filtresi en kritik hayatta kalma bileşeni.**
  - FFTY 2022'de −%51 yaptı; Kullamägi filtresine uymadığı 2022'de −%57 (KIM §5.1; VA #16–17 [D]).
  - Momentum çöküşleri panik sonrası toparlanmada geliyor; dinamik ölçekleme Sharpe'ı ~2 katına çıkarıyor (VA #27 [D]).
  - Merdivenden önce birincil araç rejim filtresi (PROF §3.3).
- **Pilot ancak FTD ya da 10 > 20 ile açılır** (PROF §1.4, §3.5 #6; SEY §5.1 #4).
- **VIX vade yapısının ters dönmesi zayıf bir gösterge** (tek günlük sıçrama; VP A11). Bu yüzden VIX/VIX3M < 1 gerekli bir şart, ama tek başına yeterli değil.

**Belirsizlik:**
- Bu dört durumun bu birleşimi hiç test edilmedi; yanlış alarm oranı bilinmiyor.
- Bedeli: dipten çıkışın ilk %5–10'u kaçırılır.
- Faydası çöküş yıllarında görünür, sakin yıllarda görünmez.

---

## 3. Kollar: kurallar

### 3.0 Kol özeti

| Kol | Durum | Gerekçe |
|---|---|---|
| **S1 Baz kırılımı** | **Canlı** (Faz 1 riski %0,25) | Doğrulanmış kazananların ortak yöntemi (PROF §1.3; VA #13–14). Tekil hissede trend takibinde sağ kuyruk gerçek (VA #18, #29). EOD uyarlaması test edilmedi |
| **S2 Yükselen 10/20 GHO'ya geri çekilme** | **Canlı** | Luk/Kell ailesi [P] (PROF §1.1). İşlem sayısını ~40–70'ten ~60–120'ye çıkarır, kanıt daha hızlı birikir (HD aşı 5) |
| G1 Bilanço gap'i (episodic pivot), 2.–5. gün | **Gölge** | Büyük hissede PEAD 2006'dan beri yok (VA #23). Sadece-uzun bilanço üst portföyleri VW piyasayı geçmiyor (TEST §6.4). Hisse düzeyinde test yapılamadı (TEST §8) |
| G2 VIX panik çözülmesi (SPY, 40 gün) | **Gölge** ve rejim bilgisi | Başlıktaki t=3,69 T-bill'e göre. Koşulsuz piyasaya göre fark ~+1,8 puan, t ≈ 1,7. Örneklem içi, n=25, iki tanım denendi (HU §3; HK C1) |
| G3 Insider küme alımı | **Ertelendi** | Kanıtın tamamı 1986–2007, yayın sonrası test yok (VA #26). Veri kaynağı 06.11'de 503 verdi. Ağır manuel iş (HU §3) |
| Opsiyon alımı | Kapalı (§3.9) | Sistematik alım ortalamada kaybettirir (VP A6–A8) |
| Kaldıraçlı ETF ve endeks çekirdeği, margin, açığa satış | Yok | 2010 sonrası filtre getiriyi kesti; düşüş −%55 ile −%97 arası (VA §2.1; TEST §0 #1–2). Profil al-tut yasaklıyor (HK B1) |

### 3.1 Evren ve eleme filtresi (her kurulum için)

**Evren:**
- Fiyat ≥ 20 $, piyasa değeri ≥ 2 mlr $ (HAZ §4).
- 50 günlük ortalama dolar hacmi ≥ 20 mn $; 1m $'lık hesapta ≥ 50 mn $. Pozisyon ≤ 20 günlük ortalama dolar hacminin %1'i [Ö].
- ADR%20 ≥ %2 [Ö]. ADR%20 = 100 × (20 günlük ortalama yüksek/düşük oranı − 1). Pozitif çarpıklık, büyük hareket edebilen hisse ister.
- Aylık oynaklık ≥ %2. Bu, satın alma/birleşme arbitrajı profilini eler (HAZ §4).
- Önümüzdeki **10 seansta bilanço yok** (Earnings Whispers ya da şirket IR'den teyit).
- Hisse izinli bir kümede (§4.3), yasaklı kümede değil (§4.6).

**Eleme filtresi (alfa değil, kötü kuyruğu dışarıda bırakmak için):**
- (a) Son çeyrekte hisse başı kâr ve gelir beklentiyi aştı.
- (b) Son bilançodan sonraki 3 seansın getirisi ≥ SPY'ninki.
- Kaynak: Nasdaq.com "Earnings" sayfası.
- Dayanak: KEN §4 (EarningsStreak, RevenueSurprise ve AnnouncementReturn likit evrende uzun-kısa %0,24–0,37/ay).
- **Dürüst not:** Bu sinyallerin sadece-uzun üst portföyü 2010–25'te VW piyasayı geçmedi (TEST §0 #8, §6.4). C'deki 90 günlük revizyon maddesi iş yükü yüzünden çıkarıldı (HU §3 C4).

**Ortak stop şartı (S1 ve S2):** Tetikten yapısal stopa mesafe **1,0–2,0 × ATR14 ve ≤ %8** olmalı. Bu aralığın dışındaysa işlem yok.
- Gerekçe 1: Uygulayıcı tavanları ≤1 ATR (Kullamägi), %7–8 (IBD), ≤%10 (Minervini) (PROF §1.3 #3 [P]).
- Gerekçe 2: Kapanış bazlı mekanik kopyada 1 ATR'nin altındaki stop kötü sonuç verdi (VP A12 [K]).
- A'nın 0,6 ATR'lik ve C'nin 0,75 ATR'lik tabanı bu yüzden 1,0 ATR'ye çekildi.

### 3.2 S1: Baz kırılımı (VCP / düz baz), gün sonu uyarlaması

| Adım | Kural | Dayanak |
|---|---|---|
| Ön koşul | Trend şablonu TT = 1: kapanış > 50 > 150 > 200 GHO; 200 GHO 21 seans öncesinden yüksek; kapanış ≥ 1,3 × 52 hafta dibi ve ≥ 0,75 × 52 hafta zirvesi. RS çizgisi / 52 haftalık zirvesi ≥ 0,97. Kapanış 52 hafta zirvesinin en çok %10 altında (≤ %5 tercih). Son 1 ayın getirisi < +%25 ve son 3 ayın < +%40; aksi halde "uzamış" sayılır ve yalnız S2 ile girilir | HAZ §5a (Pine `TT_RS_EP_Screen`); DLG §0.5: ani sıçramadan sonra 1–3 ay medyan −%4/−%6 |
| Baz | En az 15 seans. Derinlik (tepeden dibe) Faz 1'de ≤ %15, YEŞİL'de ≤ %25. Son daralma ≤ %10 ve ≤ 2,5 × ATR14. Son 5 seansın toplam aralığı ≤ 2 × ATR14. 10 günlük ortalama hacim < 50 günlük ortalama hacim | Minervini VCP, IBD baz [P] (PROF §1.1) |
| Pivot | Son daralmanın en yüksek seviyesi. Listeye girmek için kapanış pivotun en çok %5 altında olmalı | [P] |
| Giriş emri | **BUY STOP-LIMIT, DAY, yalnız normal seans.** Tetik = pivot × 1,001 (en az +0,05 $). Limit = min(tetik × 1,01; tetik + 0,3 × ATR14). Her gün 16:45–17:15'te yeniden girilir, en çok 5 seans. Kapanış pivot × 1,05'in üstündeyse kurulum iptal edilir ve "kaçan" yazılır; kovalanmaz | IBD alım bölgesi pivot +%5 [P]. Ekran olmadığı için limit daha sıkı [Ö]. Momentum getirisinin çoğu gece oluşur, bu yüzden geceyi taşıyan pozisyon tercih edilir (KEN §3, Lou-Polk-Skouras) |
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
- Pozisyon tutarı ≤ E'nin %15'i (Faz 3'te ≤ %20).
- Gap-ayarlı risk = adet × max(limit − stop; 1,5 × ATR14). Bu değer ≤ 1,25 × (E × risk%) olmalı.
- Küme, toplam ısı, brüt maruziyet ve en kötü hafta tavanları (§5).

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
| Pozisyon (limitte) / E'nin %'si | 1.819 $ / %3,6 | 9.399 $ / %3,8 | 37.898 $ / %3,8 |
| Risk: limitte dolum / tetikte dolum | 120 $ / 103 $ | 619 $ / 530 $ | 2.498 $ / 2.138 $ |
| Gap-ayarlı risk (E'nin %'si) | %0,24 | %0,25 | %0,25 |
| IBKR gidiş-dönüş komisyonu (0,005 $/adet, en az 1 $) | 2 $ = 0,016R | 2 $ = 0,003R | 3,75 $ = 0,002R |
| İş TMI gidiş-dönüş komisyonu (%0,25/yön) | 9 $ = 0,07R | 47 $ = 0,08R | 189 $ = 0,08R |

**Çalışılmış örnek 2 (S2):**
- Sinyal günü tepesi 50,00 $, ATR14 1,40 $. Stop = min(47,90; 48,20 − 0,35) − %0,1 ≈ 47,80 $.
- Tetik 50,05 $. Mesafe 2,25 $ = %4,5 = 1,61 ATR: şart sağlanıyor.
- Limit = min(50,55; 50,47) = 50,47 $. Boyut için hisse başı risk 2,67 $.
- Adet: 46 / 234 / 936. Pozisyon 2.322 / 11.810 / 47.240 $, yani E'nin ~%4,7'si.

### 3.5 Ortak çıkış kuralları

Çıkış kararları kapanış verisiyle verilir, emir ertesi gün 16:45–17:15'te girilir.

| Kural | Uygulama | Dayanak |
|---|---|---|
| **Kısmi kâr** | İlk gerçekleşen koşulda: (a) kapanış ≥ dolum + 2R, ya da (b) 4. seans kapanışı ≥ dolum + 1R. Ertesi açılışta **MOO** ile satılır: SARI'da pozisyonun 1/2'si, YEŞİL'de 1/3'ü. Aynı pencerede GTC stopun **adedi kalan adede düşürülür** ve fiyatı **dolum fiyatına** (başabaş) çekilir | Kullamägi: 3–5 günde 1/3–1/2 [P] (VP A1; PROF §1.3 #7–8, §3.5 #9) |
| Başabaş | Kısmi satış olmasa da kapanış ≥ +1,5R olunca GTC stop dolum fiyatına çekilir | [P] (PROF §1.3 #7) |
| **İz süren çıkış** | Kalan pozisyonda ilk kapanış < 10 GHO (hızlı hisse: ADR%20 ≥ %4 ya da girişten sonraki 10 seansta ≥ +3R) veya kapanış < 20 GHO (diğerleri) → ertesi açılışta MOO ile tamamen çık | Kullamägi 10/20 GHO [P]; VP A12'deki mekanik kopyada da MA trail var |
| Haftalık acil stop | Her Cuma kapanışından sonra GTC stop, son 10 seansın en düşük dibinin %0,5 altına yükseltilir (yükselme varsa). **Stop asla aşağı çekilmez** | [Ö] (A §2.4) |
| Zaman stopu | 10 seans sonunda kâr < +1R ve girişten beri yeni kapanış zirvesi yoksa ertesi açılışta MOO ile çık | [Ö]. Isıyı boşaltır (PROF §3.5 #9) |
| Aşırı koşu | Girişten +%100 olduysa: trail 10 GHO'ya ve tepeden %10 düşüş stopuna sıkılaştırılır | GSY replikasyonu: %10–15'lik iz süren stop en kötü sonucu −%69'dan −%22'ye çekiyor (DLG §5; VD U8 [D]) |
| Yeniden giriş | Stop olan hisseye yeni pivot oluşursa yeniden girilebilir. Aynı bazda en çok 2 deneme | [Ö] |

**OCA tuzağına karşı emir hijyeni** (HU §2.2; A §2.7):
- Faz 1'de +2R'de bekleyen bir kısmi satış limiti **kullanılmaz**. Bekleyen limit, tam adetli stopla aynı OCA grubundaysa iki emir birlikte dolabilir; margin tipi hesapta bu istenmeyen açığa satış doğurur.
- **Tam çıkış MOO** girildiğinde GTC stop aynı anda iptal edilir. Stop yalnız normal seansta tetiklendiği için açılışa kadar koruma gerekmiyor.
- **Kısmi MOO** girildiğinde stop adedi kalan adede indirilir.

### 3.6 Bilanço

- Bilançoya ≤ 10 seans kalmışsa yeni giriş yok.
- **Faz 1'de açık pozisyon bilançoya taşınmaz.** Açıklamadan önceki son seansta **MOC** ile çıkılır; emir o gün 16:45–17:15'te girilir.
  - Kapanış sonrası (AMC) açıklamada son seans açıklama günüdür.
  - Açılış öncesi (BMO) açıklamada son seans bir önceki gündür.
- **Faz 2+ istisnası:** kısmi satış yapılmış ve kâr ≥ +2R ise pozisyon taşınabilir. Şart: boyut, 2 × implied move büyüklüğünde bir gap ≤ 1R kaybettirecek kadar küçültülmeli ("earnings size").
- Dayanak: PROF §1.3 #9, §3.5 #5; PRA §3.6 #4 (bilanço öncesi taşımak negatif çarpık).

### 3.7 Piramit (yalnız kazanana)

- **Şartlar:** Faz 2+ ve YEŞİL rejim. Pozisyonun kapanış kârı ≥ +1,5R. Yeni geçerli bir S2 sinyali ya da yeni S1 bazı var. Bilançoya > 10 seans var.
- **Ek boyutu:** 1. ek ilk riskin 0,5'i, 2. ek 0,33'ü. En çok 2 ek.
- **Stop:** ekin kendi stopu. Ana lotun stopu en az başabaşa çekilir. Ek sonrası toplam gap-ayarlı risk ≤ ilk 1R.
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
- **Tarama:** sabah 09:00–12:00 finviz `earningsdate_yesterdayafter` / `todaybefore` (HAZ §5b). Gün içi tarama yok.
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
- Midas'ta zaten yalnız call/put alımı var (HAZ §1.2).
- **Bugün tamamen kapalı** (VIX 28,2; oran 1,10).

### 3.10 Bu planda olmayanlar

- **Kaldıraçlı endeks ya da ETF:**
  - 3x NDX + 200 GHO 2000–02'de −%89 yaptı.
  - Filtre 2010 sonrası getiriyi kesti (TEST §0 #1–2; VA §2.1).
  - B'nin çekirdeği 2010–26'da %13,8 getirdi; 1x al-tut %14,1 (HK B2).
- **Sektör ETF rotasyon kolu:** 2010 sonrası risk-ayarlı olarak piyasa düzeyinde (VA §2.2; VD U3–U4). Swing ufkunda kenarı yok: 40 varyantın 40'ı negatif (VD U7). Küme sıralaması yalnız filtre (§4.3).
- **Kısa vadeli reversal:** 2010'dan beri ~0 (TEST §0 #9).
- **Açığa satış:** ayı rallileri short'ları ezer (VA #27).
- **Margin:** faiz %5,38 ve Türkiye'de indirilemez (VC #16; VC #10).
- **AI kümesinde dip alımı** (§4.6).

---

## 4. Evren, kümeler, izleme listesi ve adaylar

### 4.1 Taramalar

| Tarama | Ne zaman (TSİ) | Ayar |
|---|---|---|
| (a) Trend şablonu + RS | Cumartesi (tam), hafta içi 08:00–09:00 (liste güncelleme) | HAZ §5a Pine `TT_RS_EP_Screen`: `TT = 1`, `RS line / 52w max ≥ 0,97`, `Dist to 52wH ≥ −10`, `50d $Vol ≥ 20`; `RS raw` azalan. Finviz sıkı sürümü (6.11'de 86 sonuç) ve geniş sürümü (412 sonuç) HAZ §5a'da |
| (b) Bilanço gap'i (yalnız G1) | 09:00–12:00, önceki günün olayları | HAZ §5b: `Gap % ≥ 8`, `RVOL ≥ 3`, `50d $Vol ≥ 20`, kapanış üst yarıda |
| (c) Küme/ETF skoru | Ayın son hafta sonu (ilki 28–29.11) | HAZ §5c: skor = 0,2·(1A − SPY) + 0,4·(3A − SPY) + 0,4·(6A − SPY); fiyat > 50 GHO |
| (d) Endüstri grupları | Her Cumartesi | Finviz grupları, 3 aylık sıralama (HAZ §3). İlk 10'a yeni giren ve 1 aylık getirisi pozitif grup aday kümedir |

### 4.2 Kümeler (Kasım 2026 başlangıç haritası)

**Kurallar:**
- Aynı anlatıya bağlı ya da 60 günlük getiri korelasyonu ≥ 0,6 olan hisseler tek kümedir (PROF §3.5 #2).
- Korelasyon ay sonunda TradingView "Correlation Coefficient (60)" ile ölçülür.
- Gerekçe: ρ = 0,6–0,8 iken aynı kümedeki 5 pozisyon yalnız 1,19–1,47 bağımsız bahis eder (SEY §3.6). Kümelenme, aynı beklentide kuyruk riskini ~%35–40 büyütür (PROF §3.3).

| Küme | İsimler (HAZ §4) | Ölçüt ETF | Not |
|---|---|---|---|
| **SAĞLIK süper-kümesi** (K1 medtech, K2 ilaç/biyotek, K3 sağlık hizmeti) | MDT, EW, BDX, GEHC, TMO, IDXX / LLY, REGN, RPRX / CNC, EHC | XLV, IHI, PPH, IBB, IHF | Korelasyon ölçülene kadar **tek küme**. Faz 1 ısısı ≤ %0,75 |
| K4 Borsalar / finansal veri | CBOE, CME, TW (+ VRSK, FDS) | XLF | CBOE oynaklıktan fayda sağlıyor; VIX düşerse geride kalabilir |
| K5 Sigorta / broker | AJG, MRSH, ACGL, BRK-B (+ AON, RLI) | — | K4 ile ilişkili: K4+K5 toplam ısısı ≤ %1,25 (Faz 1) |
| K6 Temel tüketim / indirim | KDP, BJ | XLP | Savunmacı |
| K7 Atık / su | RSG, VLTO, AWK | — | ADR%20 ≥ %2 şartını kontrol et |
| K8 Konaklama / tüketici | MAR, HLT, SN, HAS, EBAY | XRT | |
| K9 Dikey yazılım | ROP, MANH, U, GEN | IGV (zayıf) | Küme izni teyitsiz (§4.3) |
| K10 REIT (kule, depolama) | CCI, PSA | XLRE | Faize duyarlı; CPI riski |
| K11 Mega-cap teknoloji | AAPL | QQQ | NDX rejimine bağlı; YEŞİL'i bekler |

**Faktör uyarısı:** SARI'da açılacak pozisyonların çoğu savunmacı ve düşük betalı olacak; bu da kendi başına bir faktör kümesidir.
- Büyümeye sert dönüşte savunmacılar geride kalabilir. 2009'da kazanan desil +%8, kaybeden +%163 yaptı (VA #27).
- Sınırı toplam ısı tavanı koyar.

### 4.3 Küme izni (aylık, ayın son hafta sonu)

Küme şu iki koşuldan biri sağlanırsa izinlidir:
- (a) Temsilci ETF, HAZ §5c skorunda ilk 5'te ve 50 GHO'nun üstünde.
- (b) Finviz endüstri grubu 3 aylık performansta ilk %20'de.

**Dürüst not:** Bu adım bir kenar değil, kırık kümelerden uzak durma disiplini (VA §2.2; VD U4, U7; DLG §0.4). Getiri küme içindeki hisse kurulumlarından gelmek zorunda.

**Bugünkü izin durumu (HAZ §3 ve §5c, 6.11 sabahı):**

| Küme | Durum | Dayanak |
|---|---|---|
| Sağlık | İzinli | XLV #1, IHI #2, PPH #3, IBB #4, IHF #5 |
| Borsalar / finansal veri | İzinli | Finviz 3 ay +%12,4 |
| Sigorta | İzinli | Reasürans grubu üstte; XLF #7 |
| Konaklama | İzinli | 3 ay +%17,5 |
| Atık | İzinli | 1 ay +%12,1 |
| Temel tüketim | Sınırda izinli | XLP #6; indirim mağazaları güçlü |
| Dikey yazılım, REIT | **Teyit:** Cumartesi grup sıralamasında ilk %20'de mi? | — |
| Mega-cap teknoloji | YEŞİL'e kadar yok | — |

### 4.4 Küme başına isim seçimi

1. (a) taramasının sonuçları kümelere dağıtılır. Küme içinde `RS raw`'a göre sıralanır.
2. Evren ve eleme filtresini geçen **ilk 5** isim izleme listesine alınır.
3. Her isme etiket verilir: S1 (baz hazır, pivot ≤ %3 uzakta), S2 (geri çekilme sürüyor) ya da "uzamış / bekle".
4. Her isim için yazılır: pivot, tetik, limit, stop, stop %, stop/ATR, ADR%20, adet (limite göre) ve bilanço tarihi. Stop şartını sağlamayan isim kurulum listesine girmez.
5. Tetiklenince işleme alınacak sayı:
   - SARI'da kümenin yalnız 1. sırası.
   - YEŞİL'de ilk 3'e kadar (Faz 1'de küme ısısı izin verdiği kadar).
   - Diğerleri yedek.
6. Öncelik sırası: RS sırası, sonra sıkılık (son 5 seansın aralığı / ATR), sonra pivota yakınlık.

### 4.5 Güncel adaylar (5.11 kapanışı; öneri değil)

Fiyat ve 52H uzaklığı HAZ §4'ten.
- **Bugün hiçbiri alınamaz:** rejim KIRMIZI.
- Tablo, rejim SARI olduğunda hangi ismin tetik listesine girebileceğini gösterir.
- Grafik şartları (baz, pivot, ATR, eleme filtresi) bu dosyada **doğrulanmadı**; Cumartesi kontrol edilmeli.

| Sınıf | İsim (fiyat; 52H'ye uzaklık; son bilanço) | Ne yapılır |
|---|---|---|
| **Nitelikli aday:** grafik teyidiyle S1/S2 kurulumu olabilir | BDX (212,52; −%1,1; 5.11 b), EHC (141,27; −%1,5; 28.10 a), TMO (677,95; −%4,8; 21.10 b), RPRX (67,24; −%3,6; 4.11 b), TW (127,56; −%1,1; 29.10 b), CME (307,24; −%4,8; 21.10 b), MRSH (209,43; −%2,1; 15.10 b), ACGL (110,57; −%2,7; 27.10 a), HLT (369,36; −%3,1; 27.10 b), MAR (417,28; −%3,7; 2.11 b), SN (217,50; −%3,6; 4.11 b), EBAY (122,94; −%3,8; 28.10 a), MANH (255,17; −%3,2; 27.10 a) | Pivot, stop ve ATR'yi çiz. Sağlık isimleri tek küme: SARI'da yalnız 1 sağlık pozisyonu |
| **ADR şartı kontrol edilecek** (düşük oynaklık olabilir) | AWK (152,42; −%0,8), RSG (249,42; −%2,0), VLTO (115,86; −%2,7), KDP (36,30; −%4,0), PSA (340,50; −%1,6) | ADR%20 < %2 ise dışarı |
| **Uzamış:** son 1 ayda > +%25; yalnız S2 beklenir | AJG (1A +%26,9), CBOE (+%25,4), GEHC (+%29,5; 52H'ye −%6,7), HAS (+%31,7), ROP (+%36,9), GEN (+%36,7), CCI (+%31,8) | 10/20 GHO'ya geri çekilme beklenir; kovalanmaz (DLG §0.5) |
| **Bilanço bekle** | MDT (Kasım ortası/sonu, teyit), BRK-B (finviz'e göre 9.11, teyit), BJ (20.11 BMO) | Bilançodan önce giriş yok |
| **Olay / baz yok** | LLY (52H'ye −%7,1; ObesityWeek 14–17.11; DLG §6.2), REGN (−%9,8), CNC (4.11'de tek günde +%12,6) | Yeni baz oluşursa S1 |
| **G1 gölge** | U, EW, SN, BDX (1. gün kriterleri teyit edilecek). IDXX: 2.11 olayının 2.–5. gün penceresi kapandı; S2 adayı | Yalnız gölge günlüğe |
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

**Diğer kırık temalar** (nükleer, kuantum, kripto, drone/uzay, enerji, altın madencileri, savunma): kümenin RS'i yeni bir 12 aylık zirve yapmadan giriş yok (DLG §7.4).

**Hardw canlı bir GSY olayı:** tarihsel çöküş olasılığı %42–53 (DLG §0.7). Bu kümeye dönüşte iz süren stop tepeden %10 düşüşe sıkılaştırılır.

---

## 5. Risk limitleri

### 5.1 Tablo (E'nin yüzdesi)

| Limit | Faz 1 (ilk 50 canlı işlem) | Faz 2 | Faz 3 | Dayanak |
|---|---|---|---|---|
| İşlem başı risk | **%0,25** | %0,50 | %0,75 (en çok %1) | PROF §3.5 #1; KIM §5.3 (risk %1'i aşınca bu yapı kırılır; VA #37) |
| Tek pozisyon | ≤ %15 | ≤ %15 | ≤ %20 | PROF §3.1 (Kullamägi'de gece tavanı %30) |
| **Küme ısısı** | ≤ %0,75 (sağlık süper-kümesi dahil) | ≤ %1,5 | ≤ %1,5 (güçlü YEŞİL'de %2) | PROF §3.5 #3 |
| İlişkili kümeler (K4 + K5) | ≤ %1,25 | ≤ %2,5 | ≤ %2,5 | PROF §3.1 |
| **Toplam açık risk** (gap-ayarlı) | TURUNCU ≤ %1 / SARI %2 / YEŞİL %3 | %1 / %3 / %5 | %1 / %3 / %6 | PROF §3.5 #4, §1.4 (pilot ≤ %2) |
| Brüt maruziyet | SARI %30 / YEŞİL %40 | %40 / %60 | %50 / %100 | PRA §3.6; [Ö] |
| **En kötü hafta tavanı:** Σ pozisyon × max(stop %; %15) | ≤ %6 | ≤ %9 | ≤ %15 | HU §2.4 [Ö]: yalnız ısıya bakmak korele gap'te 2–3 kat yanıltır |
| **Aylık devre kesici:** ayın gerçekleşen zararı + açık risk | ≥ min(%6; 12R) = **%3** → ay sonuna kadar yeni giriş yok | ≥ %6 | ≥ %6 | PROF §3.5 #8 (Elder) |
| Açık pozisyon sayısı | SARI 4 / YEŞİL 8 | aynı | aynı | Kullamägi/Minervini 4–8 [P] |
| Margin, açığa satış, kaldıraçlı ürün | Yok | Yok | Yok | VC #16; §3.10 |

**İşlem riskini Faz 2'de %0,5'e çıkarmak bilinçli bir sapmadır.** SEY §5.3 #4 "12 ay ve 100 işlemden önce boyut artırılmaz" diyor.
- Bu plan **sermayeyi (E)** o kurala bağlar: E, 12 ay ve 100 işlemden önce artmaz.
- **İşlem riskini** ise 50 işlem ve t ≥ 1,0 ile %0,5'e çıkarmaya izin verir.
- Bu sapmanın bedeli küçük: E servetin %10'u olduğundan %0,5 risk servetin ≤ %0,05'i eder (HK §5 #3).

### 5.2 Düşüş merdiveni (yalnız canlı lider kolunda)

**Ölçüm:** stratejinin USD kâr/zararı (gerçekleşen + açık), E'ye oranla, zirveden ölçülür.

**Kalibrasyon:**
- Eşikler fazın taban riskiyle R cinsinden tanımlanır.
- Faz 1'de C §5.2 ile aynı yüzdeleri verir (−%4 / −%7 / −%10 / −%15).
- Faz 2–3'te yüzde sınırları önce gelir.

| Kademe | Tetik (hangisi önce gelirse) | Eylem |
|---|---|---|
| 1 | −16R ya da −%5 | Risk × 0,5 (en az %0,125). Piramit yok |
| 2 | −28R ya da −%8 | Yalnız en güçlü 2 kümede kurulum. Toplam ısı rejim tavanının yarısı |
| 3 | −40R ya da −%11 | 10 seans yeni işlem yok. Tüm işlemlerin yazılı incelemesi |
| **Dur** | **−%15** | **Plan durur** (§8.5 K5). Pozisyonlar kendi stop kurallarıyla kapanır; yeni işlem yok. USD nakit TL'ye dönebilir. Yeniden başlamak için yeni hipotez kartı ve sıfırdan Faz 1 gerekir |
| Geri yükleme | Kaybın yarısı geri gelince | Bir kademe yukarı |

**Gerekçe:**
- %0,25 riskte −%4, 16R eder. %30 isabette 200 işlemde ≥ 15 ardışık kayıp olasılığı ~%24; %25 isabette ~%49 (KIM §5.3; VA #37 [D]). Yani 16R "normal kötü seri" sınırıdır.
- Merdiven %5 olasılıklı kötü düşüşü yaklaşık yarıya indirir, ama medyan getiriden ~17 puan alır (PROF §3.3, %1 riskte).
- Değer kattığı tek durum, performansın rejime bağlı olması. Momentum swing bu durumda (PROF §3.3; Kaminski-Lo).
- Sistematik bir kolda merdiven yalnız getiri alır (B §5.3, BT-B [H]). Bu planda sistematik kol yok.

**Kayıp serisi tek başına öldürme nedeni değildir.** %25–30 isabette 200 işlemde ≥ 10'lu seri olasılığı %84–96 (VA #37).

### 5.3 Gap riski ve en kötü hafta

- **Gap-ayarlı risk** = adet × max(limit − stop; 1,5 × ATR14). Bilanço penceresinde 2 × implied move (PROF §3.5 #5).
- **Stres varsayımı:** korele bir gecede −%15 gap. 5.11'de SOXX −%12, MU −%17,5, AMD −%17,3 düştü (HAZ §0).
- **Faz 1 YEŞİL'de en kötü hafta:** brüt %40 × −%15 = E'nin **−%6'sı**. E servetin %10'uysa bu servetin **−%0,6'sı** eder.
- **Bu hafta (9–13.11):** canlı pozisyon yok, yani ~0.

### 5.4 Dolar karşılıkları

| Kalem | E = 50k $ | E = 250k $ | E = 1m $ |
|---|---|---|---|
| 1R: Faz 1 / 2 / 3 | 125 / 250 / 375 $ | 625 / 1.250 / 1.875 $ | 2.500 / 5.000 / 7.500 $ |
| Küme ısısı Faz 1 (%0,75) | 375 $ | 1.875 $ | 7.500 $ |
| K4 + K5 toplamı Faz 1 (%1,25) | 625 $ | 3.125 $ | 12.500 $ |
| Toplam ısı Faz 1: SARI / YEŞİL | 1.000 / 1.500 $ | 5.000 / 7.500 $ | 20.000 / 30.000 $ |
| Brüt tavan Faz 1: SARI / YEŞİL | 15k / 20k $ | 75k / 100k $ | 300k / 400k $ |
| Tek pozisyon tavanı (%15) | 7,5k $ | 37,5k $ | 150k $ (ve ≤ 20 günlük dolar hacminin %1'i) |
| Aylık devre kesici Faz 1 (%3) | 1.500 $ | 7.500 $ | 30.000 $ |
| En kötü hafta tavanı Faz 1 (%6) | 3.000 $ | 15.000 $ | 60.000 $ |
| Merdiven, Faz 1: −%4 / −%7 / −%10 / −%15 | 2.000 / 3.500 / 5.000 / 7.500 $ | 10k / 17,5k / 25k / 37,5k $ | 40k / 70k / 100k / 150k $ |

---

## 6. Uygulama: aracı kurum, emir tipleri, saatler, maliyet, vergi kaydı

### 6.1 Aracı kurum

| Kurum | Rol | Süre | Maliyet | Kısıt |
|---|---|---|---|---|
| **IBKR Pro** (margin tipi hesap, borç kullanılmaz) | **Ana platform.** BUY STP LMT, ekli GTC STP, MOO/MOC, koşullu emir, nakit faizi | Açılış 1–3 iş günü + SWIFT 1–2 iş günü. **Gerçekçi ilk işlem 11–13.11** | 0,005 $/adet (en az 1 $); margin faizi %5,38; boş nakit %3,38 | Türk müşterinin bağlanacağı IBKR şirketi (IB LLC ya da IBIE) doğrulanmadı. Bu plan ETF almadığı için kritik değil; ETF'ler yalnız ölçüt (HAZ §1.2; VC #16 [D]) |
| **Midas** | Koşullu köprü | Onay 1–2 gün | 1,5 $/işlem; kur makası yayınlanmıyor | Yalnız call/put alımı. **Ekli GTC stoplu buy-stop-limit ve MOO 1 adetle çalışmazsa S1/S2 için kullanılmaz;** ekransız korumasız pozisyon açılmaz (HAZ §1.2, §7) |
| İş TMI / Garanti / Gedik | Lider kolunda kullanılmaz | Mevcut müşteride birkaç gün | İş %0,25, pre/post-market'te +0,5 cent. Garanti %0,30 + %0,50 kur. Gedik lot başı 0,05 $ | Yüzdesel komisyon işlem başına ~0,07–0,2R; +0,2–0,3R'lik kenarın %25–60'ı (C §5.3; HK §4 #13) |

**Ek notlar:**
- **PDT:** 25 bin $ şartı kaldırıldı. SEC onayı 14.04.2026, yürürlük 04.06.2026; aracı kurumlar için geçiş 20.10.2027'ye kadar sürüyor (VC #15 [D]). Gün içi işlem olmadığı için bağlayıcı değil.
- **Nakit hesapta** free-riding kısıtları sürüyor. Margin tipi hesap seçilir, borç kullanılmaz; §3.5'teki emir hijyeni kazara açığa satışı önler.
- **IBKR başvurusu:** VİOP tecrübesi türev deneyimi olarak beyan edilir. **W-8BEN** doldurulur; yoksa temettü stopajı %30 olur (PRA §1.3).

### 6.2 Emir şablonları (IBKR)

| Amaç | Emir | TIF / seans | Ne zaman (TSİ) |
|---|---|---|---|
| S1/S2 giriş | Ana emir BUY STP LMT (tetik ve limit §3.2–3.3) | DAY, yalnız RTH ("outside RTH" kapalı) | 16:45–17:15 |
| İlk stop | Ana emre ekli (attached) SELL STP, piyasa. **Stop-limit değil:** gap'te stop-limit dolmayabilir | GTC, yalnız RTH | Giriş emriyle birlikte |
| Kısmi satış | SELL MOO (TIF = OPG) + aynı anda stop adedini düşür, stopu başabaşa çek | Açılış | 16:45–17:15 (MOO son giriş ~17:28 TSİ = 09:28 ET; bellek, teyit) |
| Tam çıkış (trail, zaman, başarısız kırılım) | SELL MOO + GTC stopu iptal et | Açılış | 16:45–17:15 |
| Bilanço öncesi çıkış | SELL MOC | Kapanış | Son seansın 16:45–17:15 penceresi (MOC son giriş ~23:50 TSİ = 15:50 ET; bellek, teyit) |
| Haftalık acil stop | GTC stop fiyatını yükselt | — | Cumartesi |

**Veri günleri (CPI, PPI, NFP; 16:30):**
- 16:45'ten önce yeni emir girilmez.
- 16:45'te S&P vadelisi önceki kapanışa göre **±%1,5'ten fazla** oynamışsa o gün yeni giriş yok. Çıkış emirleri normal girilir (C §3.4 [Ö]).

### 6.3 Günlük ve haftalık rutin (TSİ)

| Saat | İş | Süre |
|---|---|---|
| 08:00–09:00 | Kapanış verisiyle rejim tablosu (§2). Dolumlar ve stop olanlar. Çıkış sinyalleri: kısmi, trail, zaman, başarısız kırılım. Isı, küme ısısı, aylık zarar + ısı. Günlüğe kayıt | 20–30 dk |
| 09:00–12:00 | G1 gölge taraması. Bilanço takvimi. Açık pozisyonların haberleri | 15 dk |
| 16:30 | Veri günlerinde vadeliye bak | — |
| **16:45–17:15** | **Tüm emirler:** yeni girişler (her gün yeniden), MOO çıkışları, MOC bilanço çıkışları, stop düzeltmeleri. Emirler kaydedilir | 10–15 dk |
| 17:30–00:00 | **Ekran yok.** Yalnız aracı kurumun dolum bildirimleri. Stop ekli olduğu için dolumdan sonra işlem gerekmez | — |
| Cumartesi | Taramalar (a), (d). Kümeler. İzleme listesi. Acil stop yükseltmesi. 10 işlemde bir istatistik (§8.3) | 60–90 dk |
| Ayın son hafta sonu | Küme izni (c). E'nin yeniden hesabı. Aylık rapor (§8.6). Faz kapısı kontrolü | 60 dk |

### 6.4 Maliyetler (R cinsinden ölçülür)

- **Komisyon:** §3.4'teki tablo. IBKR ve Midas'ta ~0,001–0,024R; Türk kurumlarında ~0,07–0,2R.
- **Kayma:** stop emirlerinde ölçülmedi. Varsayım %0,05–0,15, yani ≈ 0,01–0,03R. Günlükte bps olarak ölçülür.
- **Kur dönüşümü:** banka makası + BSMV binde 2 (teyitsiz). İlk transferden önce küçük tutarla ölçülür.
- **Kural:** maliyet + kayma 20 işlem ortalamasında > 0,15R olursa emir yöntemi değişir (§8.5 K4).

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
- **Aralık'ın ilk haftası (1–4.12) vergi kontrol noktasıdır.** Yalnız vergi için çıkış yapılmaz; kural önceliklidir.

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
- 60 bin $ üstü US-situs varlıklar için veraset vergisi (Form 706-NA; VA #36).

---

## 7. Takvim

### 7.1 Hafta: 9–13 Kasım

| Gün | Olay (TSİ) | Ne yapılır |
|---|---|---|
| **Cu 06.11 (bugün)** | 16:30 NFP (beklenti +59–65 bin). HUM, VST, MRNA BMO | Midas ve IBKR başvuruları (HAZ §1.3). Kapanışta ralli denemesi gün sayımı başlar ya da başlamaz |
| **Ct 07.11** | — | §2.6 tablosu. §10 hafta sonu listesi |
| **Pt 09.11** | 16:40 Bowman (Barkin teyit). 21:00 3 yıllık ihale. BMO: CEG, MNDY, NRG (AI güç; dışarıda). AMC: RKLB, TTWO, ZETA, ASTS, HIMS, MARA, PLUG. BRK-B bilançosu bu gün olabilir (teyit) | **Canlı giriş yok.** SWIFT sabah. Hesap fonluysa 16:45–17:15'te 1 adetlik emir testleri. İzleme listesi. G1 gölge kaydı. BRK-B'ye bilanço öncesi giriş yok |
| **Sa 10.11** | 12:00 Waller. **16:30 Ekim CPI** (Cleveland nowcast: manşet aylık %0,24, çekirdek %0,21). 21:00 10 yıllık ihale. AMC: CRWV (AI turnusolu), RGTI. BMO: ONON, SE, QBTS | 16:45'ten önce emir yok; vadeli ±%1,5 kuralı. Pilot zaten mümkün değil: en iyi ihtimalle ralli denemesinin 3. günü. Kapanışta G2 tetiği kontrolü |
| **Ça 11.11** | Gaziler Günü: hisse açık, tahvil kapalı; hacim düşük olabilir. MSCI Kasım duyurusu ~00:00 (12.11). AMC: FNV, CTVA | **En erken FTD kapanışı** (Cuma 1. gün olduysa). FTD'nin hacim şartına dikkat |
| **Pe 12.11** | 16:30 işsizlik başvuruları. 18:00 Barr, mevcut konut satışları. 21:00 30 yıllık ihale. **TCMB haftalık rezerv verisi.** BMO: NBIS, LUNR. AMC: **CSCO, AMAT**, NU, CBRS | FTD geçerli ve rejim SARI ise: **en çok 2 pilot, 16:45–17:15.** Şartlar: IBKR fonlu ve testler geçmiş; %0,25 risk; farklı ve AI dışı kümeler; toplam ısı ≤ %2. **Döviz anahtarı kontrolü** (§1.5). AMAT/CSCO yalnız endeks riski olarak izlenir |
| **Cu 13.11** | **16:30 PPI.** 18:00 UMich (tarih teyit). Fed konuşmacıları | Veri günü kuralı. Kapanıştan sonra haftalık inceleme: rejim, gölge kayıtlar, izleme listesi, acil stop |

### 7.2 16–20 Kasım

| Gün | Olay | Kural |
|---|---|---|
| Pt 16.11 | BMO: XPEV, BIDU, TSN. AMC: PARA, POWL | Normal |
| **Sa 17.11** | 17:15 sanayi üretimi. Perakende satış tarihi çelişkili (17.11 ya da 25.11; Census'tan teyit). HD BMO. **NVDA AMC; konferans 01:00 TSİ (18.11)** | **17.11'de bütün kümelerde yeni giriş yok** (endeks olayı). Açık pozisyonlar stoplarıyla kalır |
| Ça 18.11 | TGT, TJX, LOW BMO; PANW AMC. 21:00 20 yıllık ihale. **22:00 FOMC tutanakları.** VIX vadesi | Giriş serbest. Temel tüketim ve perakende kümesinde WMT/TGT öncesi yeni giriş yok |
| Pe 19.11 | WMT BMO; ROST, GAP, INTU, KEYS AMC. 10 yıllık TIPS. Philly Fed (teyit) | Normal |
| **Cu 20.11** | **Aylık opsiyon vadesi.** BJ BMO | BJ'de giriş yok. Ayrıca LLY için ObesityWeek (14–17.11) öncesi giriş yok |

**NVDA tarihi:** HAZ §2.1, NVIDIA IR kaynağıyla 17.11 AMC diyor. Görev notundaki "~19.11" bununla çelişiyor. IR sayfası 06.11'de bot kontrolü verdi, aşılmaya çalışılmadı. **17.11 esas alınır; Cumartesi IR'den ya da aracı kurum takviminden teyit edilir.**

### 7.3 23–30 Kasım

| Gün | Olay | Kural |
|---|---|---|
| Pt–Sa 23–24.11 | 2 ve 5 yıllık ihale; BBY BMO (24.11) | Normal |
| **Ça 25.11** | 16:30 3. çeyrek GSYH 2. tahmin + Ekim PCE + kişisel gelir/harcama. 21:00 7 yıllık ihale. 22:00 Bej Kitap | **Yeni giriş yok** |
| **Pe 26.11** | Şükran Günü: piyasa kapalı | — |
| **Cu 27.11** | Erken kapanış: 21:00 TSİ (13:00 ET) | **Yeni giriş yok.** MOO çıkışları serbest |
| Pa 29.11 | OPEC+ toplantısı | — |
| **Pt 30.11** | Ay sonu. MSCI değişiklikleri kapanışta uygulanıyor | Hafta sonu (28–29.11): küme izni (§4.3), E'nin yeniden hesabı, aylık rapor |

### 7.4 1–11 Aralık

| Gün | Olay | Kural |
|---|---|---|
| 1–4.12 | **Vergi kontrol noktası** (§6.5). 3.12 TR Kasım TÜFE. 4.12 Kasım NFP | Yalnız vergi için çıkış yok |
| **Ça 09.12** | **FOMC 22:00** (artırım olasılığı ~%67–70; HAZ §2.2) | Yeni giriş yok |
| Pe 10.12 | 16:30 Kasım CPI. TCMB PPK | Veri günü kuralı |
| Cu 11.12 | ABD federal bütçe finansman süresi doluyor (kapanma riski) | Haber izlenir |
| 18.12 | Dörtlü vade (quad witching) | Normal |

---

## 8. Ölçüm protokolü ve öldürme kriterleri

### 8.1 Hipotez kartları

Kartlar ilk işlemden önce yazılır; tarihlidir ve değiştirilemez. Kuraldaki her değişiklik yeni bir kart sayılır (SEY §5.3 #1).

| Kart | Mekanizma | Beklenen E[R] | İsabet | Kazanç/kayıp | İşlem/yıl | Denenen varyant (N) |
|---|---|---|---|---|---|---|
| S1 | Sağ kuyruğu yakalama (Bessembinder %4; VA #29) + rejim filtreli momentum | +0,1R (aralık −0,2 ile +0,4R) | %25–40 | 2–3,5 | 40–70 | 1 |
| S2 | Trend içi likidite geri çekilmesi, lider devamı [P] | +0,1R (aralık −0,1 ile +0,3R) | %30–45 | 2–3 | 30–50 | 1 |
| G1 (gölge) | Bilgili şok drift'i (Savor; KIM §5.1) | −0,1 ile +0,3R | %30–45 | 2–5 | 10–25 | 1 |
| G2 (gölge) | Panik primi / likidite (Nagel; KEN §5) | Koşulsuz piyasaya göre olay başına +%0 ile +%1,8 | %65–80 | ~1 | 1–3 | **2** (C-TEST A ve B) |

### 8.2 Günlük alanları (her işlem bir satır; piramit ekleri ayrı satır)

- **Kimlik:** no, ana işlem no, canlı / gölge / test, kart sürümü, kol, kurulum, küme, ticker.
- **Bağlam:** rejim durumu, VIX/VIX3M, faz, bilançoya kalan seans, eleme filtresi (evet/hayır).
- **Plan:** pivot, tetik, limit, ilk stop, stop %, stop/ATR, ATR14, ADR%20, adet, pozisyon (E'nin %'si), 1R ($), gap-ayarlı risk; girişteki toplam ve küme ısısı, brüt maruziyet, en kötü hafta toplamı.
- **Uygulama:** dolum fiyatı ve saati, **kayma (bps ve R)**, komisyon, emir tipi.
- **Yönetim:** kısmi satış (tarih, fiyat, R), stop değişiklikleri, ekler.
- **Sonuç:** çıkış nedeni (stop / başarısız / kısmi / trail / zaman / bilanço / rejim / öldürme), çıkış fiyatı, **gerçekleşen R** (komisyon dahil), MAE ve MFE (R), tutma süresi (seans).
- **Vergi:** alış ve satış günü TCMB kuru, TL maliyet, TL bedel, TL kâr/zarar.
- **Disiplin:** kural ihlali (evet/hayır ve açıklama), ekran görüntüsü bağlantısı.
- **Ayrı sekme "kaçan sinyaller":** dolmayan emirler ve atlanan tetikler. Sinyal fiyatı ve 20 seans sonraki fiyat yazılır; ekransız ve limitli girişin bedelini ölçer (C §7.2).

### 8.3 İstatistik ve faz kapıları

**Her 10 canlı işlemde hesaplananlar** (kurulum bazında ve toplamda):
- n; ortalama R (m); standart sapma (s); SE = s/√n; t = m/SE.
- İsabet; ortalama kazanç ve kayıp; profit factor; en uzun kayıp serisi.
- Net kârın en iyi %10 işlemden gelen payı. Pozitif çarpık sistemde > %100 olması normal.
- Rejime göre ayrışma; ortalama maliyet + kayma (R); S&P'ye beta.

**İstatistik gerçeği:**
- s ≈ 2–2,5R alınırsa n=50'de SE ≈ 0,28–0,35R, n=100'de ≈ 0,20–0,25R (SEY §3.7).
- Faz 2 kapısını sıfır kenarlı bir sistem de ~%15–20 olasılıkla geçebilir [H]. Bu yüzden Faz 2 yalnız işlem riskini artırır, sermayeyi artırmaz.

| Kapı | Şartların tümü | Sonuç |
|---|---|---|
| **Faz 1 → 2** | n ≥ 50 canlı (S1 + S2); ≥ 4 ay; m ≥ +0,25R; t ≥ 1,0; zirveden düşüş < %7; kural ihlali < %10; maliyet + kayma ≤ 0,15R | İşlem riski %0,5. Piramit serbest (YEŞİL'de). USD çevrimi %70. **E aynı kalır** |
| **Faz 2 → 3** | n ≥ 100; **≥ 12 ay**; m ≥ +0,25R; **t ≥ 1,65**; en az bir KIRMIZI → YEŞİL döngüsü; son 12 ayın vergi sonrası getirisi gerçek u'ya göre engeli (§1.2) geçmiş; K9 geçilmiş; **EOD backtest geçilmiş** (aşağıda) | İşlem riski %0,75 (en çok %1). E'yi servetin %25–35'ine çıkarmak değerlendirilir |
| **"Kanıtlandı"** | SPRT H1'i kabul eder (+0,2R'lik sistemde ~300–450 işlem) ya da 3 yıl ve en az bir stres rejimi (SEY §5.3 #4) | Ancak o zaman "yüksek ödül" sürümü (progresif boyut) konuşulur |
| **Geri düşüş** | Son 50 işlemin m'si < 0 | Bir faz aşağı |

**EOD backtest şartı** (A §7.4; HK §7 #5):
- S1/S2'nin bu dosyadaki kuralları, hayatta kalma yanlılığından arındırılmış günlük veriyle (CRSP/WRDS ya da meşru ücretli sağlayıcı) test edilir.
- Örneklem içi 2012–19, dışı 2020–26. Maliyet: spread + 10 bp.
- Kabul: örneklem dışında E[R] > +0,3R ve yılda ≥ 40 işlem.
- Bu test geçilmeden risk %0,5'in üstüne çıkmaz.

### 8.4 Gölge kolların canlıya alınması

- **G1:** ≥ 30 gölge işlem, m ≥ +0,3R ve t ≥ 1,0, **ve** EOD backtest'te G1 örneklem dışı E[R] > +0,3R → Faz 1 riskiyle (%0,25) ayrı kartla canlıya alınır.
- **G2:** ≥ 5 örneklem dışı olay ve koşulsuz piyasaya göre ortalama fark > 0 → %0,25 riskle canlıya alınabilir. Pozisyon ≤ E'nin %6,25'i (stop %4).
  - SPY erişimi IBKR şirketine bağlı. IBIE'ye bağlanılırsa yedek CSPX (LSE; 10:00–18:30 TSİ) olur; bu yedek test edilmedi.

### 8.5 Öldürme kriterleri (önceden yazılı)

| # | Tetik | Eylem | Dayanak |
|---|---|---|---|
| K1 | Bir kurulumda n ≥ 30, m ≤ −0,3R ve t ≤ −1,3 | O kurulum durur; yeni kart yazılmadan açılmaz | C §7.4 |
| K2 | n ≥ 50 ve m + 1,28 × SE < 0 | Kurulum durur | SEY §5.2 #2 |
| K3 | n ≥ 100 ve (m < 0 **ya da** m + 1,65 × SE < +0,05R) | Kurulum kalıcı olarak kapanır | SEY §5.2 #2, #4 |
| K4 | n ≥ 20 ve maliyet + kayma > 0,15R ya da kenar tahmininin %50'si | Emir yöntemi değişir; 20 işlem sonra düzelmezse kol durur | SEY §5.2 #3 |
| K5 | Strateji zirveden −%15 (§5.2) | **Plan durur** | SEY §5.2 #1, #8 |
| K6 | n ≥ 20'de ihlal oranı > %20, ya da herhangi bir 20 işlemlik blokta ≥ 3 ihlal (stopu indirmek, boyut aşımı, rejim dışı giriş) | 2 hafta yeni işlem yok. Sorun disiplin, kenar değil | A K4; C K6 |
| K7 | Mekanizma ortadan kalktı (ör. emir tipi ya da erişim kapandı, vergi rejimi değişti) | t'ye bakmadan durur | SEY §5.2 #5 |
| K8 | 12 aylık S&P korelasyonu > 0,7 ve S&P'ye göre kalıntı getiri ≤ 0 | Kol yalnız beta: dur | SEY §5.2 #7 |
| K9 | 12 ayda strateji, aynı ortalama maruziyetle "rejim SARI/YEŞİL iken RSP, değilse T-bill" kuralını vergi öncesi geçemiyor | Seçim değer katmıyor: dur | SEY §5.3 #6; A K6 |
| K10 | 12 ay ve 100 işlemden sonra vergi sonrası TL getirisi < TL nakdin net getirisi **ve** m < +0,3R | Ölçek yok. Sürecekse yalnız Faz 1 boyutunda ve sermaye TL'ye dönmeye adaydır | A K7; §1.2 |

### 8.6 Aylık rapor (ayın son hafta sonu)

- Kurulum bazında: n, m, %90 bootstrap güven aralığı, t, isabet, profit factor, MAE/MFE, kayma, ısı kullanımı, rejim ayrışması, kaçan sinyallerin maliyeti.
- Gölge kolların aynı metrikleri (ayrı tablo).
- **Değer satırı:** E'nin vergi öncesi USD getirisi ve §1.2 modeliyle tahmini vergi sonrası USD getirisi. Bu satır üç kıyasla karşılaştırılır: USD nakdin vergi sonrası getirisi (%2,4–2,9), TL'de kalmanın USD karşılığı (%9–14) ve K9 kıyası (RSP / T-bill).
- Merdiven kademesi, faz, sonraki kapıya kalan.

---

## 9. Beklenen sonuçlar ve belirsizlik

### 9.1 1. yıl: Kasım 2026 – Ekim 2027 (çoğunlukla Faz 1) [H]

**Model** (HD §4.1):
- Faz 1, %0,25 risk, ~80 işlem, u ≈ 0,3.
- Boştaki USD'ye +%2,4 nakit faizi eklendi.
- Kümelenme var; merdiven uygulanıyor.
- Sonuçlar vergi öncesi USD, E üzerinden.
- Olasılıklar öznel [Ö]. Taban oranlar sert: USIC'te %8–17 kârlı, Tayvan'da %13 (VA #8, #14).

| Kenar (E[R]) | Öznel olasılık | Medyan | p10 / p90 | En büyük düşüş: medyan / %5 kötü |
|---|---|---|---|---|
| −0,1R (taban oranlara göre en olası) | %50–60 (0 ve altı) | −%0,4 | −%4,2 / +%7,9 | −%5,7 / −%8,3 |
| 0 | ↑ | +%1,1 | −%3,7 / +%10,3 | −%5,5 / −%8,1 |
| +0,15R | %25–30 | +%3,8 | −%2,8 / +%15,3 | −%5,2 / −%7,8 |
| +0,3R | %10–15 | +%6,7 | −%2,0 / +%19,9 | −%5,0 / −%7,5 |
| +0,45R (USIC tipi) | ≤ %5 | +%9,1 | −%1,2 / +%25,0 | −%4,9 / −%7,4 |

**Okuma:**
- Ağırlıklı merkez vergi öncesi **+%1–4**.
- Tek yılın sonucu kenarı kanıtlamaz. 80 işlemin toplam R'sinin standart sapması ±18R, yani %0,25 riskte ±%4,5 [H].
- Kademeli çevrim (§1.4) nedeniyle boştaki USD faizi gerçekte daha küçük (~+%0,7). E'nin ~%50–60'ı ise TL getirisini alır. TL istikrarlı kalırsa bu E'ye yılda ~+%3–6 puan USD karşılığı ekler, ama TL kuyruk riskini de taşır [H, kaba].

### 9.2 Vergi sonrası ve engelle karşılaştırma [H]

Model §1.2: u = 0,3, d = %20, 2026 tarifesi (doğrulanmadı). Betik `plan_final/at.py`.

| Vergi öncesi R → vergi sonrası USD | 50k | 250k | 1m |
|---|---|---|---|
| −%0,4 (kenar yok) | −%1,1 | −%1,4 | −%1,8 |
| +%1,1 | +%0,2 | −%0,3 | −%0,8 |
| +%3,8 (merkezin üst ucu) | +%2,4 | +%1,5 | +%0,9 |
| +%6,7 | +%4,7 | +%3,4 | +%2,7 |
| +%9,1 | +%6,5 | +%4,9 | +%4,1 |
| Kıyas: USD nakit, vergi sonrası | %2,9 | %2,7 | %2,4 |
| Kıyas: TL'de kalmanın USD karşılığı (h %31–37) | %9,2–14,2 | %9,2–14,2 | %9,2–14,2 |
| TL'yi yenmek için gereken vergi öncesi R (u = 0,3) | %12,7–19,5 | %15,6–23,3 | %17,5–25,9 |

**Sonuç:**
- 1. yıl vergi sonrası ~%0–2,5. Bu, USD nakit düzeyinde ya da biraz altında.
- **TL engelini geçme olasılığı < %5** (HD §4.1).
- Sermaye zaten USD'deyse 1. yıl USD nakde yakın biter. Fark, maruziyet sayesinde öğrenilen bilgidir.

### 9.3 Servete etkisi

E = servetin %10'u varsayımıyla:
- **Beklenen maliyet:** TL'de kalmaya göre yılda servetin ~%0,8–1,3'ü; E %15 ise ~%1,2–2. Kötü bir yılla birlikte bant ~%1–2,5 (HD §0). Kademeli çevrim bu maliyeti küçültür.
- **Kötü durum:** plan −%15'te durur (servetin −%1,5'i). Buna TL'ye göre fırsat maliyeti eklenince toplam kötü durum ~**−%2,5**.
- **Karşılığında alınan:** (i) ~%7–10 olasılıkla 2. yıldan itibaren ölçeklenebilir bir kenar opsiyonu (HD §2.4). (ii) TL şokuna karşı çeşitlendirme. 2018–26'da kurun ≥ %45 arttığı yıllar 2/9 (VC #21). Bu sigorta ortodoks rejimde pahalı.
- **Asıl risk** servetin %85–90'ının durduğu TL tarafında: carry 2010–26'da −%7,2/yıl, en büyük düşüşü −%85. Bunu yöneten kural döviz anahtarı (§1.5).

### 9.4 Kanıttan sonra (Faz 3, yıllık) [H, kaba MC]

HD §4.2 modeli: isabet %30, kayıpların %10'u gap'li −2R, dalgaların %30'unda küme birlikte bozuluyor. Bu plandaki merdiven C'ninkine eşdeğer (Faz 1) ya da biraz gevşek (Faz 2–3).

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

### 9.5 "Yüksek ödül" sorusuna dürüst cevap

- **Doğrulanmış sağ kuyruk gerçek.** Aracı kurum ekstreli USIC sonuçları: Luk 2024 +%283, 2025 +%970; Minervini 2021 +%334,8; Kell 2020 +%941 (VA #13–14 [D]).
- **Payda kötü:** katılımcıların yalnız %8–17'si kârda (VA #14). Luk ve Minervini'nin işlem istatistikleri doğrulanamadı (VA #15; VP A3).
- **Bu sonuçların girdileri:** %1 risk, yılda 150–400 işlem, progresif boyut, güçlü tema rejimi ve çoğunlukla gün içi giriş ve stop (ORH, günün dibi; VP eksik #8).
- **Bu plan sağ kuyruğu açık tutar:** S1/S2 aynı DNA'yı taşır; G1 kanıt gelirse canlıya geçer.
- **Ama sağ kuyruğu kanıttan önce satın almaz.** Medyanı %40+ olan yıl üç şartın birlikteliğini ister: ≥ +0,3R kanıtlı kenar, yılda ≥ 150 işlem ve merdivensiz, %5 olasılıklı ~−%45 düşüşü kabul etmek (HD §4.2).
- Bu kenarın bu kullanıcıda var olma olasılığı ~%7–10 [Ö]. Planın amacı, kullanıcının o kuyrukta olup olmadığını **en ucuz şekilde** öğrenmek.

### 9.6 En büyük belirsizlikler

1. S1/S2'nin EOD uyarlamasının hiç backtest'i yok (VA §4.2; TEST §8).
2. Öznel senaryo ağırlıkları ve kalibre edilmemiş Monte Carlo (VP #11).
3. 2026 vergi tarifesi ve elde tutulan USD'nin kur farkının vergisizliği teyitsiz.
4. Kurun yönü engeli 0 ile ~26 puan arasında oynatıyor.
5. Rejim bugün düşmanca. İlk 1–3 ayda işlem sayısı, dolayısıyla öğrenme hızı düşük olacak.

---

## 10. Pazartesi 09.11.2026: kontrol listesi

**Cuma 06.11 (bugün):**
- [ ] Midas başvurusu (kimlik + selfie). IBKR Pro başvurusu: margin tipi hesap; izin olarak ABD hisse yeterli.
- [ ] IBKR'ye yazılı soru: hangi IBKR şirketine bağlanacağım (IB LLC / IBIE)? ABD ETF erişimi?
- [ ] W-8BEN. VİOP tecrübesini türev deneyimi olarak beyan et.

**Cumartesi–Pazar (07–08.11):**
- [ ] Cuma kapanışıyla rejim tablosu (§2.5–2.6; Pine `ABD_Rejim_Nihai`). Not et:
  - S&P / 200 GHO (~7.327); S&P ve NDX 10/20 GHO.
  - **VIX/VIX3M** (≥ 1,00 → KIRMIZI).
  - S5FI / S5TH (grafikte teyit), MAHQ − MALQ, RSP / 50 GHO.
  - Ralli denemesinin 1. günü oldu mu?
- [ ] NFP sonucu; İran/Hürmüz ve Senato sonuçları (HAZ §6).
- [ ] **E kararı yazılı:** E = servet × %10 (en çok %15) = ____ $. Şimdi USD'ye çevrilecek: E × %40 = ____ $. Sermaye zaten USD'deyse çevrim yok.
- [ ] Hipotez kartları S1, S2, G1, G2 (§8.1); tarihli ve değiştirilemez.
- [ ] Günlük şablonu (§8.2): canlı, gölge, test, "kaçan sinyaller" sekmeleri.
- [ ] Taramalar (a) ve (d). İzinli kümeler (§4.3). Küme başına ilk 5 (§4.4).
- [ ] Her aday için: kurulum, pivot, tetik, limit, stop, stop %, stop/ATR (1,0–2,0 ve ≤ %8), ADR%20, adet (limite göre; 50k / 250k / 1m), bilanço tarihi. Şartı sağlamayanı ele.
- [ ] Teyit:
  - BRK-B (9.11?) ve MDT bilanço tarihleri.
  - NVDA 17.11 AMC.
  - U, EW, SN, BDX'te G1 1. gün kriterleri.
  - Perakende satış tarihi.
- [ ] Mali müşavire randevu (§6.5 soruları).

**Pazartesi 08:00–12:00 TSİ:**
- [ ] IBKR onaylandıysa **USD SWIFT bu sabah**, bankanın kesim saatinden önce. Önce küçük bir tutarla kur makasını ölç. Bakiye Salı–Çarşamba görünür.
- [ ] Midas onaylandıysa küçük bir TL → USD çevrimiyle makası ölç.
- [ ] TL'de bekleyen payı (E'nin %60'ı) 32 günlük mevduata ya da banka iştiraki PPF'ye koy.
- [ ] Gece bilançoları; G1 gölge kaydı.

**Pazartesi 16:45–17:15 TSİ:**
- [ ] **Canlı strateji emri yok.**
- [ ] Hesap fonluysa **emir testleri, 1 adet, likit bir hisse.** Emirleri kur, kaydet, sonra iptal et ya da kapat. Maliyeti günlüğe "test" diye yaz.
  - BUY STP LMT (DAY, yalnız RTH) ve ona ekli GTC SELL STP (yalnız RTH).
  - Pozisyon kapatmak için SELL MOO (TIF = OPG).
  - SELL MOC.
  - Bekleyen bir emrin adedini ve fiyatını değiştirmek.
- [ ] **Midas'ta da aynı testler.** Ekli stop ya da MOO yoksa Midas S1/S2 için kullanılmaz.
- [ ] Opsiyon: **kapalı.**

**17:30–00:00 TSİ:** ekran yok.

**Salı 10.11 (CPI):**
- [ ] 16:45'ten önce emir yok; vadeli ±%1,5 kuralı.
- [ ] Bu hafta pilot ancak FTD'den sonra (en erken Perşembe 12.11).

**Perşembe 12.11:**
- [ ] FTD ve SARI varsa en çok 2 pilot (§7.1).
- [ ] TCMB rezervi → döviz anahtarı (§1.5).

**Cumartesi 14.11:**
- [ ] Haftalık inceleme. **Kuralları değiştirme**; değişiklik yeni bir hipotez kartıdır.

**Asla:**
- [ ] AI çip veya güç dip alımı.
- [ ] Bilanço öncesi yeni giriş.
- [ ] Zarardaki pozisyona ekleme; stopu aşağı çekme.
- [ ] %1'in üstünde işlem riski.
- [ ] Opsiyonu IV pahalıyken almak.
- [ ] Margin, açığa satış, kaldıraçlı ETF.
- [ ] 17:30–00:00 arası emir değiştirmek.

---

## 11. İzlenebilirlik ve açık sorular

### 11.1 Kural → kanıt tablosu

| # | Kural | Dayanak (dosya § bölüm) | Kanıt gücü | Beklenen etki ve belirsizlik |
|---|---|---|---|---|
| 1 | E = servetin %10'u (≤ %15); ölçek yalnız Faz 3'te | VA §4.2; VA #14; SEY §3.3, §3.7, §5.3 #4; HD §2.4 | [D] taban oranlar; [H] maliyet | Servete maliyet yılda ~%1–2,5; kötü durum ~−%2,5 |
| 2 | Kademeli çevrim (%40 → %50 → %70 → %100) | HD aşı 3; B §1.3; A C2; VA #34 | [H] | Boştaki USD'nin yıllık ~9–12 puanlık fırsat maliyetini azaltır; TL kuyruk riskini korur |
| 3 | Boştaki USD nakitte, T-bill'de değil | PRA §2.5, §4.2; HD §2.3, §6 #2 | [K], müşavir teyidi | %20 kurda T-bill pozisyonunun ~%5–7'si kadar vergiden kaçınılır; faiz kaybı 0,65 puan |
| 4 | Döviz anahtarı (5 tetikten 2'si) | TRM §5.1; VC #18, #21 | [D] veriler; [Ö] eşikler | İşlem kenarından bağımsız; servetin büyük kısmının riskini yönetir |
| 5 | KIRMIZI: VIX/VIX3M ≥ 1, S&P 2 kapanış < 200 GHO, genişlik | HAZ §3, §5d; VP A11; PRA §3.6 | [D] veriler; [K] VIX zayıf | Sol kuyruğu keser; yanlış alarm oranı bilinmiyor |
| 6 | Pilot yalnız FTD (+%1,5) ya da 10 > 20 ile | PROF §1.4, §3.5 #6; SEY §5.1 #4; HAZ §3 | [P] | Dipten çıkışın ilk %5–10'u kaçırılır |
| 7 | Rejim filtresi birincil | KIM §5.1; VA #16–17, #27; PROF §3.3 | [D] FFTY / D-M; [P] Kullamägi | Çöküş yıllarında değer; sakin yılda maliyet |
| 8 | Risk %0,25 → %0,5 → %0,75; asla > %1 | PROF §3.5 #1; KIM §5.3; VA #37 | [D] seri matematiği; [P] | %0,25'te 15 ardışık kayıp ≈ −%3,7 |
| 9 | Stop 1,0–2,0 ATR ve ≤ %8, yapısal | PROF §1.3 #3; VP A12 | [P] + [K] | EOD'de dar stopun kötü sonucundan kaçınma; test edilmedi |
| 10 | Adet limite göre | HU §2.2 | Aritmetik | Gap'te riskin 1R'yi aşmasını önler |
| 11 | Seans öncesi buy-stop-limit, kovalamak yok | PROF §1.1; KEN §3 (gece momentumu) | [P] + [D] (KEN) | Kaçan sinyal maliyeti "kaçan" sekmesinde ölçülür |
| 12 | Kısmi satış (+2R ya da 4. seansta ≥ +1R), MOO, başabaş | PROF §1.3 #7–8; VP A1 | [P] öz beyan | Isıyı boşaltır; R dağılımını kırpar |
| 13 | Kapanış bazlı 10/20 GHO trail | VP A1, A12; PROF §3.5 #9 | [P] | Sağ kuyruğu korur; EOD'de gecikme |
| 14 | Zaman stopu (10 seans), başarısız kırılım (3 seans) | PROF §1.3 #3; A §2.1, §2.4 | [Ö] | Isı ve fırsat maliyetini azaltır; test edilmedi |
| 15 | Faz 1'de bilançoya taşımak yok; earnings size | PROF §1.3 #9, §3.5 #5; PRA §3.6 #4 | [P] | Gap kuyruğunu keser |
| 16 | Piramit yalnız kazanana, Faz 2+ YEŞİL | PROF §1.3 #6, §0 #1 | [P] | Sağ kuyruğu büyütür; kanıt gelene kadar kapalı |
| 17 | Küme tanımı (ρ ≥ 0,6); AI tek küme; sağlık süper-kümesi | PROF §3.2, §3.5 #2; SEY §3.6; VP A14 | [D] matematik; [K] 0,72 | 5 pozisyon ≈ 1,2–1,5 bağımsız bahis |
| 18 | Küme ısısı %0,75 / %1,5; ilişkili kümeler %1,25 | PROF §3.1, §3.3, §3.5 #3 | [H] MC | Kümelenme kuyruğu ~%35–40 büyütüyor |
| 19 | Toplam ısı 1/2/3 → 3/5/6 | PROF §3.5 #4, §1.4 | [P] (Elder) | — |
| 20 | Gap-ayarlı ısı ve en kötü hafta tavanı | PROF §3.5 #5; HU §2.4; HAZ §0 | [P] + [Ö] | Faz 1 YEŞİL'de en kötü hafta ≈ E'nin −%6'sı |
| 21 | Aylık devre kesici %3 (Faz 1) | PROF §3.5 #8 | [P] (Elder) | — |
| 22 | Düşüş merdiveni (R ve %), −%15'te dur | PROF §3.3, §3.5 #7; KIM §5.3; B §5.3; SEY §5.2 #1, #8 | [H] MC | %5 kötü düşüş ~yarıya iner; medyanı düşürür |
| 23 | Küme izni = filtre, kenar değil | VA §2.2, §3.1; VD U3, U4, U7; DLG §0.4 | [D] | Getiriye katkı ~0; kırık temadan uzak tutar |
| 24 | Dikey sıçramadan sonra kovalamak yok | DLG §0.5 | [H] sektör düzeyi | Hisse düzeyinde test yok |
| 25 | AI dönüş kuralı | DLG §0.7, §7.4; A §4.5 | [H] + [Ö] | Erken dönüşü kaçırabilir (D-M toparlanması) |
| 26 | Bilanço eleme filtresi | KEN §4; TEST §0 #8, §6.4 | [D] (uzun-kısa); sadece-uzun ≈ 0 | Alfa değil, kötü kuyruk elemesi |
| 27 | G1 gölgede | VA #23; TEST §6.4, §8; KEN §4.1 | Kanıt zayıf | Sağ kuyruk kaynağını açık tutar |
| 28 | G2 gölgede | C §2.3 (C-TEST); HU §3 C1; HK C1; HD §3.3 | [H] örneklem içi | Olay başına E'nin +%0,1–0,5'i; asıl işi rejim bilgisi |
| 29 | Insider ertelendi | VA #26; HU §3 C3 | Yayın sonrası test yok | Beklenen değeri ~0 |
| 30 | Opsiyon kapalı ve şartlı | VP A6–A8; PROF §0.6, §2.3 | [D] | Ortalama alıcı kaybeder |
| 31 | Kaldıraçlı çekirdek yok | VA §2.1; TEST §0 #1–3; HK B1–B2; HU §3 B | [D] | 2010 sonrası filtre getiriyi kesti; profil |
| 32 | IBKR ana; yüzdesel komisyonlu kurumlar dışarıda | VC #16; HAZ §1.2; C §5.3 | [D] tarifeler | Türk kurumlarında maliyet 0,07–0,2R |
| 33 | 1 adetlik emir testleri; Midas şartlı | HAZ §1.2, §7 | Erişim teyitsiz | Ekransız korumasız pozisyonu önler |
| 34 | Veri günü kuralı (16:45 ve ±%1,5) | C §3.4; HU §4 #2 | [Ö] | Olay gap'ine girişi azaltır |
| 35 | Vergi kaydı; kısa vergi yılı 2026 | VC #10–12; PRA §2.1 | [D] kurallar; [K] tarife | Zarar devretmez; dışbükeylik −0,4 puan |
| 36 | Hipotez kartı, N, t kapıları, kaçan sinyaller | SEY §3.7, §5.3; VA #37 | [D] matematik | Şansla ölçek büyütmeyi önler |
| 37 | Öldürme K1–K10 | SEY §5.2, §5.3 #6; A K6–K7; C §7.4 | Önceden yazılı | Kayıp serisi tek başına öldürme nedeni değil |

### 11.2 Taslaklardan alınanlar ve düzeltilen kusurlar

**Alınanlar:**
- **C'den (iskelet):**
  - Boyuta ve u'ya bağlı engel, hayalet vergi, döviz anahtarı.
  - Faz 1 risk kabuğu, t kapıları, K1–K8.
  - Tek emir penceresi 16:45–17:15 ve ±%1,5 veri kuralı.
  - Bilanço eleme filtresi, kaçan sinyaller sekmesi.
- **A'dan:**
  - S1 ve S2 (geri çekilme) mekaniği, EOD çıkışlar (kısmi, trail, zaman stopu, başarısız kırılım, acil stop).
  - Stop-market tercihi, OCA uyarısı.
  - AI dönüş kuralı, K6/K7 (burada K9/K10), 50k'da veri maliyeti disiplini, Pine iskeleti.
- **B'den:**
  - Kademeli transfer, boyuta göre vergi sonrası tablo mantığı.
  - Merdivenin yalnız takdirli kolda değer kattığı bulgusu.
  - Pasif beta için TEFAS notu (yalnız araştırma maddesi).

**Düzeltilen kusurlar:**
1. B'nin kaldıraçlı S&P çekirdeği reddedildi. Profile aykırı; beta, kenar değil; 2010–26'da 1x al-tutun altında (HK B1–B2; HD §3.2).
2. C'nin S3 (VIX) kolu gölgeye alındı; başlıktaki t=3,69 yerine artımsal t ≈ 1,7 yazıldı (HU §3; HK C1).
3. C'nin insider kolu ertelendi (veri 503, yayın sonrası kanıt yok).
4. A'nın bilanço gap'i kolu gölgeye alındı (VA #23; TEST §6.4).
5. Stop tabanı 0,6 / 0,75 ATR'den 1,0 ATR'ye çekildi (VP A12).
6. Boyut tetik yerine limit fiyatından hesaplanıyor (HU §2.2).
7. Bekleyen kısmi limit ile OCA miktar tuzağı yerine kapanışta karar ve MOO kullanılıyor; stop adedi düşürülüyor ya da stop iptal ediliyor (HU §3).
8. Pilot için FTD ya da 10 > 20 şartı eklendi; TURUNCU durumu getirildi (HK A2/C3; PROF §1.4).
9. FTD eşiği +%1,5'te birleşti (HAZ §3).
10. A'nın boştaki nakit için T-bill önerisi yerine nakit (PRA §2.5).
11. C'nin bütün E'yi hemen çevirmesi yerine kademeli çevrim (HD §3.3 #2).
12. C'nin Faz 3 "+%17–30" beklentisi yerine merdivenli merkez ~%8–16 (HD §4.2).
13. C'deki "50 işlemde riski artır" ile "12 ay ve 100 işlemden önce büyütme yok" çelişkisi: sapma adlandırıldı; E yalnız Faz 3'te artıyor (HK C3; SEY §5.3 #4).
14. Faz 3 için EOD backtest şartı eklendi (HK §7 #5).
15. CDS 248 "doğrulanamadı" olarak işaretlendi. d=%32,9 satırı tahmin değil senaryo (VC §1, #5).
16. NVDA tarihi 17.11 esas alındı; çelişki not edildi (§7.2).

### 11.3 Açık sorular ve teyit listesi

1. **EOD uyarlaması test edilmedi** (VA §4.2; VP eksik #8). Faz 3'ten önce §8.3'teki backtest şart.
2. **Uygulayıcı istatistikleri:** Luk'un isabet/R rakamları ve Minervini'nin isabeti doğrulanamadı (VA #15; VP A3). Kullamägi'nin rakamları öz beyan (VP A1–A2).
3. **IBKR:**
   - Bağlanılacak şirket (IB LLC / IBIE) ve ETF erişimi (bu plan için kritik değil).
   - MOO ve MOC son giriş saatleri (bellek).
   - Küçük hesapta nakit faizi kademeleri.
   - Ekli stopun "yalnız RTH" ayarı.
4. **Midas:** buy-stop-limit, ekli GTC stop, MOO/MOC, seans öncesi emir girişi ve kur makası kamuya açık sayfalarda yok (HAZ §7).
5. **Vergi:**
   - 2026 tarifesi (VC #11).
   - Elde tutulan USD'nin kur farkı vergisiz mi (PRA §2.5)?
   - TCMB kur türü ve FIFO.
   - "Ticari kazanç" riski.
   - Nakit faizinin beyanı.
   - US-situs veraset vergisi ve aracı kurum nakdinin konumu (VA #36).
   - Kambiyo BSMV (VC: doğrulanamadı).
6. **Takvim:**
   - NVDA (17.11 IR / ~19.11 görev notu).
   - BRK-B ve MDT bilanço tarihleri.
   - Perakende satış (17.11 / 25.11), UMich (13.11) (HAZ §7).
7. **Veri:** S5FI ve S5TH TradingView önbelleğinden, zaman damgaları karışık (HAZ §7). Küme korelasyonu 0,72 tekrarlanmadı (VP A14). CDS 248 doğrulanamadı (VC §1).
8. **Model:** Bütün Monte Carlo ve dağılım rakamları kalibre edilmemiş (VP #11; HD §8). İleriye dönük hisse primi tartışılmadı (VA §4 #4); kaldıraçsız beta beklentisi muhtemelen 2010–26'dan düşük.
9. **TL tarafı:** yeni alınan DİBS'te stopaj (VC #8). PPF'lerde teminat kalitesi (VP eksik #2). 2027 stopaj takvimi (VC §2 #6).
10. **Araştırma maddesi, kural değil** (HD aşı 10; PRA §2.4; VC #10): Kullanıcı bir gün pasif beta isterse iki seçenek önce değerlendirilmeli; müşavir teyidi şart.
    - TEFAS yabancı hisse fonu: %17,5 nihai stopaj.
    - ≥ 6 ay tutulan lotlarda Yİ-ÜFE endekslemesi: örnekte matrah −%86 düşüyor [H].
