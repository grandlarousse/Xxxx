# Strateji haritası: hangi işlem hangi stratejiyle (08.11.2026)

_Tek sayfa. Ayrıntılar: `LEADLAG_UYGULAMA.md`, `NET_LISTE_BIST.md`, `NET_LISTE_ABD.md`, `PLAN_BIST.md`, `PLAN_ABD.md`. Rakamlar 06.11 kapanışına göredir. Yatırım tavsiyesi değildir._

"Kâğıt" demek, aracı kurum VİOP teminatına faiz işlediğini yazılı teyit edene kadar (Kural 0) işlemin canlı açılmayıp yalnız deftere yazılmasıdır.

## BIST / VİOP

| # | İşlem (enstrüman) | Strateji | Nasıl yapılır (özet) | Şu an |
|---|---|---|---|---|
| 1 | **TUPRS** (F_TUPRS Aralık) | **Lead-lag**: ABD rafinerileri → TUPRS | Sabah `NYSE:VLO/MPC/PSX/PBF` artığından z okunur (`tuprs_alarm.pine`). \|z\| > 1 ise aynı gün 18:00–18:09'da z yönünde 1 kontrat; t+2'de çık ya da uzat | Kâğıt. Pazartesi z sabah okunacak |
| 2 | **XU030 vadeli** (F_XU030 Aralık) | **Baz sıçraması dönüşü** (mikroyapı) | 18:10–18:15'te vadeli/spot oranı eşiği aşarsa ters yönde 1 kontrat; ertesi gün uzlaşmada çık | Kâğıt. Pzt eşikleri: oran < 1,0343 ise AL, > 1,0484 ise SAT |
| 3 | **SAHOL + AKBNK** (Aralık vadelileri) | **Çift işlem / ortalamaya dönüş** (K1) | Oran z ±2'yi geçerse ertesi gün 17:55'te: oran yüksekse SAHOL SAT + AKBNK AL, düşükse tersi. 8 + 10 kontrat, 20 gün tut, −%8 felaket stopu | Kâğıt. z −0,54, sinyal yok (oran tetikleri 1,3556 / 1,2249) |
| 4 | **ENJSA** (spot) | **Kırılım** (K4: 52 hafta zirvesi + trend şablonu + %15 iz süren stop) | Kapanış > 127,00 → ertesi gün 18:01–18:05 kapanış seansında alış | Canlı olabilir (spot). Tetiğe +%4,1 |
| 5 | **ENERY veya AHGAZ** (spot, tek isim) | **Kırılım** (K4) | Kapanış > 14,60 / 48,70 → ertesi gün kapanış seansı | Bilanço 9.11 → en erken 16.11 |
| 6 | **KCHOL** (spot) | **Kırılım** (K4) | Kapanış > 225,50 ve 50 günlük ortalama üstü → ertesi gün kapanış seansı | Tetiğe +%9,4 |
| 7 | **RYSAS** (spot) | **Kırılım** (K4) + **RYGYO filtresi** | Kapanış > 30,28 → ertesi gün alış; giriş günü RYGYO sert düştüyse (z < −1) o akşam girme | Tetiğe +%10,8; en erken 16.11 |
| 8 | **BRSAN** (spot) | **Kırılım** (K4) | Kapanış > 769,50 ve ortalama dizilimi tamam → alış, stop %25 | Dizilim yok |
| 9 | **TRMET / TRALT** (vadeli) | **Koza grup içi göreli momentum** | 17:50–17:55'te z3 > +1,5 ise TRMET AL + TRALT SAT (1:2), 2 gün | Kâğıt (kenar sönmüş). z3 +0,71 |
| 10 | **TRALT** (vadeli) | **Altın → TRALT** | 17:55'te `TVC:GOLD` ±%1,70'ten fazla oynadıysa TRALT altın yönünde + ters XU030 hedge, 2 gün | Yalnız kâğıt |
| 11 | **F_XU030** | **Olay**: kredi notu kararı sonrası ters işlem | Karar sonrası ilk tepki gününün uzlaşmasında kararın tersine, 2 gün | Yalnız kâğıt; olay olunca |
| 12 | Temettü veren hisseler (spot) | **Olay**: temettü öncesi 5 gün (K3) | Hak kullanımından 6 gün önce al, 1 gün önce sat | Takvim KAP'tan elle |
| 13 | Verimi ≥ %5 temettüler (spot + XU030 hedge) | **Olay**: yüksek verimli temettü (K3b) | Duyurudan sonraki ilk kapanışta al, hak kullanımından önceki gün sat | Sezon Şubat–Mayıs; pilot 01.02.2027 |
| 14 | Sermayenin çoğu | **Taşıma (carry)**: mevduat + banka PPF | Pzt hesabın %15'i 32 gün mevduat, %85'i banka PPF; hedef %60 / %40 | **Pazartesi yapılacak tek finansal işlem** |

**Yapılmayanlar (bu planda işlem yok):** GARAN, YKBNK, THYAO, BIMAS, EREGL, TRGYO, GLYHO; holding, perakende ve GYO kümeleri yönlü olarak. Bankalarda 10.12 PPK sürprizsiz indirimse ~15.03.2027'ye kadar yarım boy. SAHOL/AKBNK'nin eski 1–3 günlük sürümü emekli (yerine 3 numara). Short USDTRY carry kapalı.

**Rejim şu an KAPALI.** Kırılım işlemleri (4–8) en çok 2 deneme ve işlem başına %0,25 riskle açılır. 1, 2, 9, 10 ve 11 numaralı eski sinyallerin toplam riski en çok %0,5'tir; bu, kırılım deneme bütçesinden düşülür.

## ABD

| İşlem | Strateji | Nasıl yapılır | Şu an |
|---|---|---|---|
| **BDX, EHC, TW, ACGL, MAR** (A grubu; aynı anda tek pozisyon) | **Lider swing**: S1 baz kırılımı ya da S2 yükselen 10/20 günlük ortalamaya geri çekilme | 16:45–17:15 TSİ'de bekleyen al-stop limit + ekli GTC stop; risk sermayenin %0,25'i. +2R'de ya da 4. seansta ≥ +1R ise 1/3–1/2 satılır; kalan 10/20 günlük ortalamayla taşınır | Rejim KIRMIZI → en erken **16.11**. BDX'e ek filtre: `NYSE:HCA` LL_z > +1 ise sağlık hakkı BDX'in |
| Diğer 27 isim | İzle (B grubu) | Kendi kurulumu oluşursa sıraya girer | — |
| CNC, KDP, MDT, XLV/IHI/XLP | Yapılmıyor (C grubu) | — | — |

## Günlük akış

- **17:55 bildirimi:** Bugünkü kapanış seansının emirleri, bugün tetiklenebilecek seviyeler ve XU030 AL/SAT oranları.
- **TradingView alarmları:** TUPRS sabah sinyali, 18:08–18:15 XU030 bazı.
- **21:20:** Rapor bugünkü kapanışla güncellenip dala kaydedilir.
