# Altın: VİOP Ons Altın (F_XAUUSD) ve Midas ETF'leri ile 1–3–5 günlük trade, fiyat tahmini ve lead-lag araştırması

_Veri 06.11.2026 kapanışına kadar · Rapor 08.11.2026 · Yatırım tavsiyesi değildir_

Soruların cevabı bu dosyada. Derinlik için:
- `sentez/HAKEM.md`: Bütün bulguların hakem denetimi, çoklu test düzeltmesi ve son güven etiketleri.
- `sinyal/KULLANIM.md`: Günlük sinyal betiğinin kullanımı.
- `analiz/` ve `arastirma/`: Ajan raporları.

> Kaldıraçlı türev ürünlerde sermayenin tamamı kaybedilebilir. Aşağıdaki hiçbir kural canlı veride doğrulanmadı. Hepsi geçmiş veriye dayanıyor ve binlerce test içinden seçildi.

---

## Net cevap

1. **Altında 1–5 günlük yönü tahmin etmek çok zor.**
   - 7.446 hipotez kayda geçti. İşlenebilir öngörü testleri ayıklandıktan sonra VİOP için kalan 2.621 birincil testin **hiçbiri** çoklu test düzeltmesini geçmiyor (en küçük BH q 0,29).
   - 103 öznitelikli makine öğrenmesi modelleri (ridge, lasso, gradient boosting, random forest, topluluk) 27 kombinasyonun hiçbirinde örneklem dışında rastgele yürüyüşü yenmedi.
   - Akademik literatürün sonucu da aynı: günlük ve haftalık ufukta makro değişkenler altını örneklem dışında öngörmüyor.
2. **Bu işten para kazananlar** yön tahmin edenler değil, dört grup:
   - Piyasa yapıcılar ve yüksek frekanslı işlemciler: spread ve hız.
   - Risk primi taşıyanlar: oynaklık satıcıları, carry ve kira geliri alanlar.
   - Fiziki lojistik ve bilanço avantajı olan bankalar ve rafineriler: EFP ve bölgeler arası arbitraj.
   - Yavaş trend takipçileri.

   Perakende genelde bunların karşı tarafındadır. Türkiye'de 2016–2026 arasında kaldıraçlı işlem hesaplarının ortalama yalnız **%33'ü kârda** (TSPB, 36 kurum, 42 çeyrek).
3. **Projede çoklu test düzeltmesinden sağ çıkan tek öncü ilişki VİOP'ta değil, ETF'te.** Altının bir önceki ABD kapanışından bugün 15:00 ET'ye kadarki hareketinden sonra, madenci ETF'i GDXJ ertesi gün ters yöne gidiyor (t −5,3; 18 yılın 15'inde aynı işaret; Bonferroni p 0,0002). Ama maliyet sonrası buy&hold'a göre net fazla getiri istatistiksel olarak anlamsız (10 bps maliyette t 1,4).
4. **Ayakta kalan kurallar küçük ve rejime bağlı.**
   - VİOP: 4 kural, hepsi DÜŞÜK güvenli. Sakin piyasa momentumu, çeyrek sonu, GDXJ artığı ve son saat momentumu.
   - Midas/ETF: 5 kural ORTA güvenli. Tatil öncesi GDX, üç "madenci artığı" kuralı ve altın gün içi → GDXJ dönüşü.
   - Eşit ağırlıklı birleşimin geçmiş sonucu VİOP'ta net Sharpe 1,3, ETF'de 0,9. Bu bir üst sınır. Gerçekçi beklenti bunun yarısı: VİOP'ta Sharpe ≈0,7 ve yılda ≈%2 (1x nominal), ETF'de sepete göre alfa yılda ≈%3.
5. **"Lead-lag" diye görünenlerin çoğu saat farkı.**
   - VİOP uzlaşması 18:00–18:10 TSİ'de, ABD piyasaları 23:00/00:00 TSİ'de kapanıyor.
   - Uzlaşmadan sonra oluşan hareketi "dünkü bilgi" diye etiketlemek sahte öncülük üretiyor. Örneğin gün t'nin 15:00→20:00 UTC spot hareketi ile t→t+1 uzlaşma getirisi arasında korelasyon 0,42.
   - Doğru zamanlamayla bakınca dolar, faiz, reel faiz, S&P, VIX ve petrol bilgisi VİOP kapanışına kadar geçen 18 saatte zaten fiyatlanıyor.
6. **Kesin olarak kaçınılacaklar:**
   - RSI(2), Bollinger, Connors ve "2σ düşüşte dip al" gibi dönüş kuralları. Üç ayrı dönemde de zarar ettirdi.
   - Haftanın günü, ay mevsimselliği, FOMC/CPI günü yön bahisleri.
   - COT, ETF akışı ve Şanghay primiyle yön tahmini.
   - Gram altın vadelisinde uzun kalmak. TL faiz farkı nedeniyle spot sentetiğin seans başına ≈%0,17 gerisinde kalıyor.
   - Kaldıraçlı ETF'leri birkaç gün tutmak. 2×GLD'ye göre yılda ≈%7, NUGT'de ≈%20 aşınma var.
7. **Dünya altın fiyatını 1–5 günde "tahmin" etmek yerine olay ve rejim yönetilir.**
   - 1–3 ayda Fed yolu, reel faiz değişimi, dolar ve ETF akışları önemli.
   - 6–12 ayda merkez bankası alım hızı ve Fed döngüsünün dönüşü belirleyici.
   - 2026'da reel faiz geri döndü: Fed Eylül'de faiz artırdı, altın Ocak zirvesinden ≈%25 düştü.
8. **Türkiye fiyatı ≈ ons × kur / 31,1035 × (1 + prim).**
   - 2024'ten beri gram altın riskinin ≈%97'si onstan geliyor.
   - Kur kayması yönetilen kur rejiminde öngörülebilir, ama bu kayma VİOP vadeli fiyatlarında zaten fazlasıyla fiyatlı.
   - VİOP ons altın Ocak–Mart 2026'da yurt içi talep nedeniyle spotun %1–4 üstünde işlem gördü. Bu, uzun pozisyon için ek bir risk.

---

## 1. Neyi trade ediyorsunuz: kontratlar, saatler, maliyetler

### 1.1 VİOP Ons Altın (F_XAUUSD) künyesi

Kaynak: VİOP Prosedürü rev. 70 (01.07.2026), Takasbank genel mektupları, GİB rehberi. Doğrulamadan geçti (`arastirma/r1_viop_kontrat.md`, `g2_bosluk.md`, `g4_bosluk.md`).

| Unsur | Değer |
|---|---|
| Dayanak / büyüklük | 1 ons saf altın, USD kotasyon, nakdi uzlaşma, T+1 takas |
| Fiyat adımı | 0,10 USD (≈0,25 bps). Eski kaynaklardaki 0,05 güncel değil |
| Vadeler | Şub, Nis, Haz, Ağu, Eki, Ara. En yakın 3 vade işlem görür. Son işlem günü vade ayının son iş günü |
| **"Kapanış" = günlük uzlaşma fiyatı** | Normal seans bitmeden önceki **son 10 dakikanın hacim ağırlıklı ortalaması**: **18:00–18:10 TSİ = 15:00–15:10 UTC**. 10.02.2023'e kadar pencere 18:05–18:15 TSİ'ydi. Yarım günlerde 12:30–12:40 TSİ |
| Seanslar | Açılış seansı 09:20–09:25, normal seans 09:30–18:10, akşam seansı 19:00–23:00 TSİ (18.09.2020'den beri). Yarım günlerde ve yılın son iş gününde akşam seansı yok. Akşamda piyasa emri ve stop kullanılamaz |
| Vade sonu fiyatı | LBMA Gold Price PM (15:00 Londra). PM ihalesi yapılmazsa AM fiyatı. 31.12.2025'te gerçekten AM kullanıldı |
| Fiyat limiti | Baz fiyatın (önceki uzlaşma) ±%10'u. 2017–2026'da uzlaşmada hiç dolmadı (en büyük günlük hareket −%7,8). Gün içinde 02.02.2026'da −%13,7 görüldü; limit iki katına çıkarıldı |
| Teminat | Takasbank PSR %10 → sözleşme başı ≈408 USD ≈20,4 bin TL. Bazı aracı kurumlar %20 istiyor (QNB) |
| Maliyet | Borsa yüzbinde 3 + Takasbank yüzbinde 1 (taraf başı), aracı kurum onbinde 0,9 ile binde 2 arası + %5 BSMV. Pazarlıklı komisyonla gidiş-dönüş ≈5 bps ≈2 USD/ons; varsayılan perakende tarifeyle 22–25 bps |
| Vergi (yerleşik gerçek kişi) | %10 stopaj, nihai vergi, üç aylık netleştirme. Zarar yalnız aynı takvim yılı içinde devrediyor. GVK geç. 67, 31.12.2030'a kadar |
| Likidite (2026) | Günlük medyan ≈43 bin sözleşme (≈230 milyon USD), açık pozisyon ≈140 bin. Ön vade payı %86. Yedi resmî piyasa yapıcı var |
| Kodlar | TradingView **BIST:XAUUSD1!** (sürekli), BIST:XAUUSDZ2026, BIST:XAUUSDG2027. Bloomberg XLTA Comdty |

**Uyarı:** TradingView'ın günlük çubuğu normal seans ile aynı günün akşam seansını birleştiriyor. "Use settlement as close" ayarı kapalıysa ekranda gördüğünüz kapanış 23:00 TSİ'deki son işlem olabilir. Akşam kapanışı uzlaşmadan medyan 35 bps sapıyor. Kapanıştan kapanışa kontrol için **uzlaşma fiyatını** kullanın.

**Aralık 2026 vadesi:**
- F_XAUUSD1226'nın son işlem günü 31.12.2026. LBMA o gün PM ihalesi yapmazsa vade sonu fiyatı AM fiyatı (13:30 TSİ) olur.
- 2026'da AM→PM hareketinin standart sapması %0,86.
- Öneri: pozisyonları 24–30.12.2026 arasında F_XAUUSD0227'ye devredin.

### 1.2 Önemli saatler (TSİ; Türkiye kalıcı UTC+3)

| Olay | Kış (ABD/İngiltere standart saat, 01.11.2026 → 14.03.2027) | Yaz |
|---|---|---|
| ABD 08:30 ET verileri (CPI, NFP) | 16:30 | 15:30 |
| LBMA Gold PM | **18:00** (uzlaşma penceresiyle aynı an) | 17:00 |
| **VİOP uzlaşma penceresi** | **18:00–18:10** | **18:00–18:10** |
| VİOP akşam seansı | 19:00–23:00 | 19:00–23:00 |
| COMEX GC uzlaşması | 21:30 | 20:30 |
| FOMC kararı (14:00 ET) | 22:00 | 21:00 |
| ABD borsa kapanışı (16:00 ET) | **00:00** | **23:00** |

ABD verileri VİOP uzlaşmasından **önce** gelir ve aynı günün getirisine yansır. FOMC ve ABD kapanışı uzlaşmadan **sonra** gelir ve ertesi günün getirisine yansır.

### 1.3 Üç kanal yan yana

Kaynak: `arastirma/m1_midas_platform.md` (doğrulama: 21 iddia doğru, 4 kısmen).

| | VİOP F_XAUUSD | Midas: ABD ETF'leri (GLD, IAU, GLDM, GDX, GDXJ, SLV…) | BIST altın BYF'leri (GLDTR, ZGOLD, ISGLK) |
|---|---|---|---|
| Nerede | Ons altın vadelisi sunan aracı kurum. **Midas'ta F_XAUUSD yok**; Midas VİOP'ta yalnız XAU/TRY (gram) var | Midas (aracı Alpaca, saklama DTCC) | Midas dahil BIST aracıları |
| Kaldıraç | ≈10x'e kadar (teminat %10) | Yok; kaldıraçlı/ters ETF'lerin Midas'ta listelendiği teyit edilemedi | Yok |
| Kısa pozisyon | Var | Açığa satış yok. Yalnız ters ETF (teyit edilmedi) ya da put | Yok |
| Kapanış | Uzlaşma 18:00–18:10 TSİ VWAP | 16:00 ET (kışın 00:00 TSİ). **MOC emri yok**; 15:50–15:58 ET'de limit/piyasa emri | 18:10 TSİ |
| Gidiş-dönüş maliyet | ≈5 bps (pazarlıklı) | 1,5 USD/emir + spread ≈1 bps + **açıklanmamış TL↔USD kur makası**. 1.000 USD'de %0,31, 10.000 USD'de %0,04 (bakiye USD'deyse) | Spread %0,09–0,27 |
| Vergi | %10 stopaj, nihai | Değer artışı beyanı, %15–40, **kur farkı dahil**. Midas stopaj kesmiyor | %17,5 stopaj (09.07.2025 sonrası alımlar) |
| Ek risk | Teminat çağrısı, limit, Q1 2026'daki gibi yerel prim | ABD veraset vergisi (ABD varlıkları 60.000 USD'yi aşarsa, %40'a kadar; Türkiye ile anlaşma yok). Satış parası T+1'de kullanılabiliyor | BYF'nin gram altına göre primi (Ocak–Şubat 2026'da +%3–8) |

ETF ayrıntıları:
- **ETF seçimi:** GLD likit ve spread ≈1 bps. GLDM'nin yönetim ücreti %0,10, GLD'ninki %0,40. 1–5 günde bu fark önemsiz.
- **GLD/IAU NAV'ı:** LBMA PM'de belirleniyor, borsa fiyatı ise 16:00 ET'de. Bu yüzden görünen prim/iskonto çoğunlukla altının 10:00→16:00 ET hareketi.

---

## 2. Altın trade'inden kim, nasıl para kazanıyor

Kaynak: `arastirma/r6_kim_kazaniyor.md` (24/25 iddia doğrulandı).

| Grup | Gelir kaynağı | Kanıt | Bireysel erişim |
|---|---|---|---|
| Otomatik piyasa yapıcılar / HFT | Spread, rebate, hız | COMEX altın hacminin %67,6'sı otomatik. Büyük otomatik işlemcilerin hacminin %52,9'u 1 dakika içinde netleşiyor, yani yön almıyorlar (CFTC, 2016–2018) | Yok |
| VİOP piyasa yapıcıları | Spread; azami spread 2,80 USD (normal seans) | QNB, İş, Yapı Kredi Ekim 2026'da USD kıymetli maden vadelilerinin %60'ını yaptı | Yok |
| Banka bullion masaları, rafineriler | EFP, bar dönüşümü, nakliye, kira (lease) | EFP kopuşları: 24.03.2020 ≈30–37 USD/ons; 08.08.2025 ≈40 USD fazlalık | Yok |
| Oynaklık satıcıları | Oynaklık risk primi | GVZ, sonraki 21 günün gerçekleşen oynaklığından ortalama 2,7 puan yüksek (günlerin %81'i). Kuyruğu kalın | Sınırlı (Midas'ta opsiyon yazma teyit edilmedi) |
| Yavaş trend takipçileri (CTA) | Trend primi | Altın trend vekili 2010–2026 Sharpe 0,49 (drift çıkarılmış 0,37). 2013 ve 2025 iyi, 2012, 2015–17 ve 2021 kötü yıllar | Var, ama 1–5 günde değil, aylarca tutarak |
| Carry farkında olanlar | Vadeli/spot ve TL/USD faiz farkı | VİOP gram altın vadelisinde uzun kalmanın maliyeti 2026'da yıllık ≈%43 (TL carry). VİOP ons vadelisi ABD 3 aylık faizinin üstünde ek taşıma içeriyor: 2017–25'te yılda 0,2–1,6 puan, 2026'da ≈2,9 puan | Var: hangi aracı tuttuğunu bilmek |
| **Perakende kaldıraçlı traderlar** | Ortalamada zarar | ESMA %74–89, FCA %82 zararda. Türkiye TSPB 2016–2026: kârdaki hesapların ortalama payı %33. Kurum-çeyreklerin %93'ünde zarar edenler daha fazla. 2017'deki 10:1 kaldıraç sınırı bu oranı değiştirmedi | — |

**Perakende zararın tipik nedenleri:**
- Aşırı kaldıraç ve teminat çağrısı.
- Maliyet: varsayılan perakende komisyonla 22–25 bps gidiş-dönüş, yüksek devirli bir kuralın kenarını yer.
- Haber anında genişleyen spread.
- Tatil ve hafta sonu boşlukları:
  - 2026'da TR tatil boşluğunun standart sapması %3,3.
  - 19.03 → 23.03.2026 arasında −%9,9.
  - Cuma→Pazartesi en kötüsü −%9,1.
- Dip alma: büyük düşüşten sonra ertesi gün ortalaması koşulsuz ortalamanın altında.

**Bireysel ölçekte gerçekçi kenar:**
- Maliyet disiplini (pazarlıklı komisyon, az işlem).
- Oynaklığa göre boyutlandırma.
- Carry farkındalığı: ons mu, gram mı, ETF mi?
- Olay ve tatil öncesinde pozisyon küçültme.
- Aşağıdaki küçük, rejime bağlı sinyalleri filtre olarak kullanmak.

---

## 3. 1–3–5 günlük strateji aileleri: literatür ne diyor, veri ne diyor

Literatür: `arastirma/r2_kisa_vade_strateji.md`, `r5_leadlag_literatur.md`, `m2_etf_strateji.md`, `g3_literatur_ek.md`.

Veri testi: VİOP 2017-03 → 2026-11 (2.427 gün), spot 2010 → 2026, ETF 2008 → 2026.

Hüküm ölçütleri:
- Bağımsız yeniden üretici ve çürütücü ajanların son kararı.
- 5 bps (VİOP) ve 10 bps (ETF) maliyet sonrası performans.
- Drift çıkarılmış Sharpe.
- 2010–2016 erken dönem tekrarı.

| Aile | Literatürde iddia | VİOP verisi | ETF verisi | Hüküm |
|---|---|---|---|---|
| Trend / momentum (MA, Donchian, 52 hafta, TSMOM) | Emtiada aylık ufukta var; günlükte zayıf | Drift çıkarılınca ≈0. 2022–26 boğasında iyi, 2017–21'de negatif. Kâr altının yükselişinden geliyor | GLD'de al-tut'u geçmiyor | **Çalışmıyor** (1–5 gün) |
| **Sakin piyasada momentum** (rv20 düşükken 5 günlük yön) | Oynaklık yönetimli momentum hisse ve aylık ufukta var; altında bu biçimde yok | Drift çıkarılmış Sharpe ≈1,0 (t 3,1), erken dönemde aynı işaret ama anlamsız. **2026'da hiç tetiklenmedi** | — | DÜŞÜK, şu an pasif |
| Kısa vadeli dönüş (RSI(2), Connors, Bollinger, 2σ, seri tersine) | Perakende popüler | **Ters işaretli**: drift çıkarılmış Sharpe −0,4 ile −0,7, yılların 9/10'unda zarar | GLD'de de yok | **Zararlı, kullanmayın** |
| Oynaklık rejimi / hedefleme / GVZ | Risk yönetimi aracı | Yön öngörmüyor. Hedefleme Sharpe'ı artırmıyor, maks. düşüşü %25'ten %17'ye indiriyor | — | Risk aracı, alfa değil |
| Haftanın günü, ay mevsimselliği, Ocak/Eylül/Kasım, festival (Diwali, Çin Yeni Yılı), Ramazan/bayram | Kararsız, yayın sonrası zayıflamış | Hiçbiri tutmuyor | GLD Ocak etkisi çürüdü | **Çalışmıyor** |
| **Çeyrek sonu** (sondan 2. gün → yeni çeyreğin 2. günü) | Yalnız pratisyen iddiası | +77 bps/olay (diğer günler +8), 39 olay, spot 2010–26 t 3,3. Ama 2017–19 ve 2022–23'te ≈0 | — | DÜŞÜK |
| **Tatil öncesi / ay başı (madenciler)** | Hisselerde tatil öncesi etkisi (Ariel 1990) | — | Tatil öncesi GDX +47 bps/olay (yılda ≈9 işlem). Ay başı + tatil öncesi GDXJ sepeti t 4,25 ama sonradan kurulmuş | Tatil öncesi GDX ORTA, sepet DÜŞÜK |
| Seans etkisi ("gece pozitif, NY negatif") | Blose–Gondhalekar: zayıflayarak sürüyor | 20:00→00:00 UTC +3 bps/gün (t 6,6; 17 yılın 15'i) **gerçek**. Ama kapanıştan kapanışa yakalanmıyor; akşam→sabah kuralı maliyetten sonra ≈0. Asya/Londra asimetrisi 2017 sonrası yok | GLD getirisinin çoğu gece oluşuyor, ama "kapanışta al, açılışta sat" için başabaş maliyet 4–7 bps | Olgu var, işlem yok |
| FOMC (öncesi sürüklenme, günü, sonrası) | Hissede FOMC öncesi sürüklenme | Yön kenarı yok (|t| ≤ 1,8). Ertesi günün hareketi normalin 1,7 katı | — | Yalnız risk olayı |
| CPI / NFP | Tepki dakikalar içinde | CPI'da kural yok. NFP günü 12→15 UTC tepkisinin yönü 1–3 gün sürüyor, ama yalnız 2022 sonrasında; 2010–16'da ters | — | NFP DÜŞÜK |
| COMEX opsiyon vadesi, GC roll, ay sonu dengeleme | Pratisyen iddiası | Opsiyon vade günü −24 bps, ama erken dönemde ters ve komşu günlerde işaret dönüyor | — | **Çalışmıyor** |
| COT (managed money uçları) | Kanıt zayıf | Yok. Pozisyon değişimi aynı haftanın getirisiyle 0,49, sonraki haftanınkiyle −0,002 korelasyonlu; fiyatı takip ediyor | — | **Çalışmıyor** |
| ETF akışları (GLD/GLDM pay sayısı) | Akış fiyatı takip eder | Yok | Yok (aynı gün t 12, fiyatı takip ediyor) | **Çalışmıyor** |
| Şanghay primi | "Mütevazı öngörücü" | 1–5 günde yok (IS'te ters) | — | **Çalışmıyor** |
| Altın/gümüş oranı | Ortalamaya dönüş | Yok; altın/gümüş 5 günlük göreli dönüş rejime bağlı, DÜŞÜK | — | **Çalışmıyor** |
| Reel faiz + dolar modeli artığı | Sapma kapanır | Yok. "Altın makroya göre geride kaldı, yetişir" mantığı veride yok, tersine zayıf devam var | — | **Çalışmıyor** |
| **Madenciler ↔ altın** | Literatür: altın madencilere öncülük eder | GDXJ'nin GLD'ye göre artığı VİOP 3 günü öngörüyor (IC t 3,5), işlem kuralı zayıf | Madenci artığı 3 gün sürüyor (C2j/C2) ve GDX'in 10 günlük artığı GLD'yi öngörüyor (C1). Altın gün içi düşüşünden sonra GDXJ ertesi gün yükseliyor (E3-1) | ETF tarafında ORTA; kanıtın en güçlü olduğu alan |
| Kaldıraçlı ETF dengelemesi | İstatistiksel var, ekonomik küçük | — | E3-1'in mekanizması bu; NUGT çıktıktan sonra GDX'te etki başlamış | ORTA (istatistik), net kâr zayıf |
| Kapalı uçlu fon iskontosu (PHYS, CEF) | Ortalamaya dönüş | — | Çok sağlam (t −6,4; 17 yılın 17'si), ama ±20 bps fark geçiş maliyetini karşılamıyor | Yalnız araç seçimi |
| Makine öğrenmesi birleşimi | Pierdzioch vd.: maliyet sonrası al-tut'u geçmiyor | 103 öznitelik, 27 kombinasyonun hiçbirinde OOS R² > 0 yok | — | **Çalışmıyor** |
| Perakende teknik (MACD, Fibonacci, destek-direnç, ICT) | Kanıt yok | Test edilmedi; veri madenciliği düzeltmesinden sonra çoğu kural kazandırmıyor (literatür) | — | Kanıt yok |

---

## 4. Lead-lag araştırması: VİOP F_XAUUSD, kapanıştan kapanışa

### 4.1 Nasıl yapıldı

- **Hedef:** Aktif kontratın uzlaşmadan uzlaşmaya getirisi. Aktif kontrat, önceki gün açık pozisyonu en büyük vade; bu seçim ileriye bakmıyor. Roll aynı kontrat içinde yapıldı. Giriş gün t uzlaşmasında, çıkış t+1, t+3 ve t+5 uzlaşmasında.
- **Karar anı:** gün t 15:00 UTC (18:00 TSİ). Uzlaşma zamanı dakikalık spot veriyle ölçüldü: en iyi uyum 15:00–15:15 UTC. 2023 öncesinde 15:15, sonrasında 15:10 UTC; Prosedür'le birebir uyumlu.
- **Hizalama:** Her öngörücü yalnız karar anından önce yayımlanmış ya da kapanmış haliyle kullanıldı. Bu yüzden:
  - ABD kapanışları t-1.
  - Asya kapanışları t (Tokyo, Seul, Şanghay, Hong Kong).
  - Avrupa kapanışları t-1, çünkü DAX ve FTSE uzlaşmadan sonra kapanıyor.
  - Dukascopy çapraz varlıkları t 15:00 UTC.
  - Türkiye yarım günlerinde uzlaşma 09:30–09:40 UTC'de oluştuğu için bu günler dışlandı.
- **Veri:**
  - Borsa İstanbul VİOP günlük bülteni (2.427 gün; ons ve gram altın, gümüş, USDTRY, XU030 vadelileri).
  - Dukascopy saatlik spot: altın 2008'den, 13 çapraz varlık 2016'dan; ayrıca dakikalık örnekler.
  - Yahoo'dan 143 sembol.
  - ABD Hazinesi nominal ve reel faizleri, CFTC COT, SHFE altın ve gümüş vadelileri, Caldara–Iacoviello günlük jeopolitik risk endeksi.
  - SSGA GLD/GLDM NAV ve pay sayısı (2004+).
- **İstatistik:**
  - Spearman IC ve Newey-West t (lag ≥ h).
  - IS 2017-03..2021-12, OOS 2022-01..2026-11. Parametreler IS'te seçildi.
  - Yıl yıl işaret tutarlılığı ve 2010–2016 spot erken dönem tekrarı.
  - Maliyet 5 bps (stres 10). Drift çıkarılmış Sharpe; uzun ve kısa bacak ayrı.
  - Her test kayda geçti, başarısızlar dahil. Global BH-FDR ve Bonferroni.
- **Doğrulama:**
  - Her ailenin iddiaları iki bağımsız ajandan geçti. Biri kodu sıfırdan yazıp yeniden üretti, diğeri çürütmeye çalıştı.
  - Son güven = ikisinden düşüğü.
  - Sonunda bir hakem bütün testleri sınıflandırıp çoklu testi alan bazında yeniden hesapladı.

### 4.2 En önemli ders: saat farkı tuzağı

| Öngörücü (yanlış hizalama) | t→t+1 uzlaşma getirisiyle korelasyon | Doğru hizalamayla |
|---|---|---|
| Gün t spot 15:00→20:00 UTC hareketi | **0,42** | ≈ −0,03 |
| COMEX'in aynı gün kapanıştan kapanışa getirisi | 0,19 | ≈ −0,01 |
| ABD 10 yıllık faiz aynı gün değişimi | −0,09 | ≈ 0 |

Bu ilişkiler VİOP uzlaşmasında işlemle kullanılamaz.

Dolar emilim tanısı:
- Dolar endeksinin ABD kapanışındaki hareketi, gece ve sabah altın fiyatına yansıyor (t 2,8).
- VİOP girişinden sonraki getiriyi ise öngörmüyor (t −0,95).
- Yani ABD bilgisi VİOP kapanışına kadar tükeniyor.

### 4.3 Ayakta kalan VİOP kuralları (hepsi DÜŞÜK güven)

Hiçbiri çoklu test düzeltmesini geçmiyor. Bunlar binlerce test içinden "en az kötü" olanlar. Tek başına işlem kuralı değil, küçük ağırlıklı bir sepet ya da filtre olarak düşünün.

| Kural | Bilgi zamanı | Tutuş | Geçmiş etki | OOS 2022–26 net Sharpe (B&H 0,62) | Ana zayıflık | 9 Kasım durumu |
|---|---|---|---|---|---|---|
| **Sakin piyasa momentumu (LOWMOM).** Spot 15:00 UTC'nin 20 günlük oynaklığı 2010'dan beri oluşan dağılımın alt üçte birindeyse (yıllık ≈%11,7'nin altı) son 5 günün yönünde pozisyon al, ertesi uzlaşmada kapat. Varyant: 5 gün tut | t 15:00 UTC | 1 (ya da 5) | +8 bps/aktif gün; yılda ≈22 işlem | 1,35 | Parametre ızgarasının tepe noktası; 2017–19'da etki yok; **2026'da hiç tetiklenmedi** | **Pasif** (rv20 %21) |
| **Çeyrek sonu.** Mar/Haz/Eyl/Ara'nın sondan 2. VİOP günü uzlaşmasında uzun gir, 3 VİOP günü sonra çık | Takvim | 3 | +77 bps/olay; yılda 4 işlem | 1,00 | 39 olay; mekanizma belirsiz; 2022–23'te ≈0 | Pasif. Sonraki giriş **30.12.2026** (0227 kontratında) |
| **GDXJ artığı → VİOP.** e = GDXJ getirisi − β60 × GLD getirisi (t-2→t-1 ABD kapanışı), z = e / std(e, 120 gün). z > 0,43 uzun, z < −0,43 kısa; 3 gün kademeli | t-1 ABD kapanışı | 3 | +12 bps/aktif gün | 0,71 | Kanıt sıra korelasyonunda; işlem kuralının t'si 1,6; 2025–26'da zayıf; ETF'deki C2j ile aynı fenomen | **Aktif, yeni dilim uzun** (z = +2,84) |
| **Son saat momentumu.** sign(ln(spot 15:00 / spot 14:00 UTC)) yönünde gir, 5 gün kademeli | t 15:00 UTC | 5 | +10 bps/aktif gün | 0,66 | 2010–16'da yok; 2024'te Sharpe −2,3; kazanç 2026'ya yığılı | Koşullu (Pazartesi 14→15 UTC) |

"Kademeli" uygulama: her gün sermayenin 1/h'i ile yeni dilim açılır, h gün sonra kapanır. Aynı yöndeki dilimler netleşir.

**Eşit ağırlıklı VİOP birleşimi (1/4'er)** sonradan seçildiği için üst sınır:

| Dönem | Net Sharpe (5 bps) | 10 bps | Yıllık (1x nominal) | Maks. düşüş | B&H Sharpe |
|---|---|---|---|---|---|
| 2017–2026 | 1,33 | 1,08 | %4,2 | −%4,3 | 0,57 |
| 2022–2026 (OOS) | 1,59 | 1,38 | %5,5 | −%4,3 | 0,62 |
| 2026 | 1,78 | 1,65 | %8,8 (yıllık) | −%4,3 | −0,51 |

Dört bileşen birbirine neredeyse dik: P&L korelasyonu |ρ| ≤ 0,12. Ortalama pozisyon 0,19 birim olduğu için 1x nominalde getiri küçük. 10 yılın 9'unda pozitif; yalnız 2018 −%1,6. **Gerçekçi beklenti:** Sharpe ≈0,7, yılda ≈%2 (1x). Nominali 3 kata çıkarırsanız yılda ≈%6–8, oynaklık ≈%10, beklenen en büyük düşüş ≈%13.

### 4.4 Test edilip VİOP'ta tutmayan öncüler

Her biri bağımsız doğrulamadan geçti; "yok" sonucu güvenilir.

| Grup | Öngörücüler |
|---|---|
| ABD ve küresel (t-1 kapanışlar) | Dolar (DXY, UUP), 10 yıllık nominal ve reel faiz, başabaş, 2 yıllık, eğri (DÜŞÜK, çürüdü), S&P, Nasdaq, VIX, GVZ, MOVE, HY kredi, petrol, bakır, gümüş, platin, paladyum, BTC, EEM, FXI, TUR. Reel faiz + dolar model artığı |
| Aynı saatte göreli değer (15:00 UTC) | Altının dolar, T-bond, S&P, USDJPY, USDCNH, BTC ve gümüşe göre yuvarlanan beta artığı (297 test); "altın geride kaldı, yetişir" mantığı. Tek iz: makro hareketin büyük olduğu günlerde altının açıklanmayan hareketinin 3 gün sürmesi (DÜŞÜK, filtre olabilir) |
| Gün-içi seanslar | Asya, Londra, NY sabahı, akşam seansı segmentleri ve kombinasyonları; LBMA fiks öncesi saat (çürüdü); hafta sonu boşluğu; büyük NY sabahı hareketleri |
| Konum ve akış | CFTC COT (managed money, swap, producer; seviye, değişim, uçlar), GLD/GLDM akışları, VİOP açık pozisyon × trend (çürüdü), VİOP hacim şokları |
| Asya ve Çin | Hang Seng (çürüdü), Nikkei, Şanghay, KOSPI, ASX; SHFE primi; Çin altın madencisi hisselerinin artığı (yalnız 2022 sonrası, DÜŞÜK); Çin altın ETF'i |
| Jeopolitik | GPR günlük endeksi (yayın zamanlaması belirsiz, DÜŞÜK/çürüdü) |
| Türkiye | VİOP USDTRY, ima edilen TL faizi, XU030, gram altın sentetik primi, XAUTRY hacmi ve açık pozisyonu, TL kriz günleri. VİOP ons uzlaşması dünya spotunu 0,98 betayla izliyor; TL şoklarında yerel prim yok |
| Takvim ve olaylar | FOMC, CPI, haftanın günü, ay dönümü, ay mevsimselliği, NYSE/LSE/SSE/TR tatilleri, bayram sonrası (kod hatası düzeltilince çürüdü), COMEX opsiyon vadesi (çürüdü), GC roll, VİOP vade günleri, Çin Yeni Yılı, Altın Hafta, Dhanteras/Diwali, Akshaya Tritiya |
| VİOP mikro yapı | Uzlaşma − kapanış (t −2,9 çıkıyor ama ileriye bakma artefaktı; temiz sürüm t 0,1), uzlaşma − VWAP, gün aralığındaki konum, baz sapması. Baz ortalamaya dönüyor ama ekonomik değer yok |

---

## 5. Midas cephesi: ABD ETF'leriyle 1–3–5 gün

### 5.1 Ne değişiyor?

- **Karar anı 15:00 ET** (kışın 23:00 TSİ). O saatte VİOP uzlaşması, Avrupa ve Asya kapanışları ve ABD seansının büyük kısmı zaten biliniyor.
- **Hedef:** ETF'nin 16:00 ET kapanışından kapanışına getirisi.
- **Uygulama kısıtları:**
  - Açığa satış yok. Her kural "yalnız uzun, değilse nakit" sürümüyle test edildi.
  - Ters ETF'li sürümler hiçbir kuralda OOS katkı vermedi.
  - MOC emri olmadığı için emir 15:50–15:58 ET'de limit ya da piyasa emriyle verilir.
- **Maliyet:** 10 bps (stres 20 bps).

### 5.2 Ayakta kalan ETF kuralları (ORTA güven)

| Kural | Hedef | Tutuş | Geçmiş etki | OOS 2018–26 net Sharpe / B&H | Ana zayıflık | 9 Kasım durumu |
|---|---|---|---|---|---|---|
| **E3-1: Altın düştüyse madenci ertesi gün toparlanır.** m = ln(spot 15:00 ET bugün / spot 16:00 ET dün). m < 0 ise GDXJ'yi kapanışta al, ertesi kapanışta sat (koşul sürerse koru) | GDXJ | 1 | +18 bps/aktif gün; IC t −5,3 (IS −4,8, OOS −2,8); **Bonferroni'yi geçen tek ilişki** | 0,71 / 0,54 (20 bps'de 0,50) | Maliyet sonrası B&H'ye göre alfa anlamsız; yılda 66 gidiş-dönüş; 2008'de GDX'te −%49 | **Koşullu:** Pazartesi 15:00 ET'de spot < **4.065,68 USD** ise al |
| **E2-C2j: GDXJ'nin kendi artığı sürer.** e = GDXJ − b·GLD − c·SPY (250 günlük beta). Dünkü e > +%0,67 ise GDXJ al, 3 gün kademeli | GDXJ | 3 | +49 bps/aktif dilim | 0,81 / 0,54 | IS t 1,9; 2025–26'da zayıf (2026 Sharpe 0,21) | **Aktif uzun** (e = +%3,67) |
| **E2-C2: GDX'in 3 günlük artığı sürer.** 3 günlük artık > +%0,81 ise GDX al, 3 gün | GDX | 3 | +38 bps/aktif dilim | 0,71 / 0,60 | 2022+'da B&H'yi geçmiyor; C2j ile aynı aile | **Aktif uzun** |
| **E2-C1: Madenciler altına öncü.** GDX'in 10 günlük artığı > +%2,52 ise GLD al, 5 gün. Kaplama sürümü: GLD tut, artık alt %20'deyse nakde geç | GLD | 5 | +58 bps/aktif dilim | 0,78 / 0,81 | Yalnız uzun sürüm B&H'yi geçmiyor; en iyi kullanımı risk filtresi | **Aktif uzun** |
| **E1-C2: Tatil öncesi GDX.** NYSE tatilinden önceki son işlem gününden bir önceki kapanışta GDX al, tatil öncesi günün kapanışında sat | GDX | 1 | +47 bps/olay; yılda ≈9 | 0,75 / 0,60 | IS t 1,7; etkinin yarısı aynı günkü altın hareketi | Pasif. Sonraki giriş **24.11.2026** kapanışı (Şükran Günü) |
| Araç seçimi: PHYS (ya da CEF) | — | 5 | ln(PHYS/GLD) 60 günlük medyanın 1,5σ altındaysa altını PHYS'le alın; 5 günde +19–21 bps | — | Midas'ta PHYS teyit edilmedi; PHYS fiyat adımı 3–9 bps | — |

**Eşit ağırlıklı ETF birleşimi (1/5'er, yalnız uzun):** tam dönem net Sharpe 0,86, OOS 1,02, 2022+ 1,09. Kıyas sepetinin (GDX/GDXJ/GLD) Sharpe'ı aynı dönemlerde 0,34, 0,64 ve 0,79. Sepete göre alfa OOS'ta yılda %5,6 (t 2,7), 2022+'da %4,8 (t 1,6), 20 bps maliyette %3,5 (t 1,7). Maks. düşüş −%22. **Gerçekçi beklenti:** alfa yılda ≈%3, beta dahil Sharpe 0,4–0,5. 1,5 USD/emir yüzünden küçük hesapta daha kötü.

**Pazartesi uyarısı:** Bütün madenci sinyallerinin "uzun" çıkmasının nedeni geçen haftaki sert madenci yükselişi (4 Kasım'da GDXJ +%9,2). Bu sinyallerin 2026 performansı zayıf, GDXJ'nin 2026 oynaklığı yıllık %59.

### 5.3 ETF tarafında tutmayanlar

- **GLD momentum, MA, Donchian, RSI(2), Connors, Bollinger, ardışık seri, 2σ.** Hiçbiri maliyet sonrası al-tut'u geçmiyor. IS'te seçilen 126 kuralın yalnız %49'u OOS'ta işaretini korudu.
- **GDX'te 5 gün üst üste düşüşten sonra al.** 1.046 testin en büyük |t|'si (3,4), gürültünün beklenen maksimumu. Çürüdü.
- **Kapanışta al, açılışta sat (gece etkisi).** GLD gece getirisi yılda %9, gün içi ≈0; madencilerde gece/gün içi ayrışması güçlü. Ama başabaş maliyet 4–7 bps, 10 bps'de yılda −%10.
- **Kaldıraçlı ETF'ler.** 1–5 günde nominal kaldıracı izliyor (UGL 2,00–2,02), ama 2×GLD'ye göre yılda −%6,9, NUGT'de −%20, 3x'te −%53 aşınıyor. Sharpe'ı iyileştirmiyor. UGL, AGQ, GLL ve ZSL K-1 düzenleyen ortaklık yapıları.
- **GLD/GLDM akışları ve GLD primi.** Prim 3–5 bps, maliyetin altında.
- **Hacim şokları.**
- **Asya altın madencilerinin artığı → GLD.** DÜŞÜK.
- **Platin → GDX.** Mekanizması yok, veri kirli. DÜŞÜK.

### 5.4 ETF'ler VİOP için öngörücü olarak

- **Madenci artığı (A4-C1):** VİOP'taki tek "dış" öncü. ETF tarafındaki C2j ile aynı fenomen (sıra korelasyonu 0,87). İkisinden birini seçin ya da her birine yarım ağırlık verin.
- **GLD/GLDM akışları, GLD hacmi ve Çin altın ETF'i hacmi:** VİOP'u öngörmüyor.
- **BIST altın BYF'leri:** GLDTR'nin gram altına göre primi geri dönüyor (t −3,9). Ama veri kusurlu (Yahoo saatlik), güveni DÜŞÜK. Pratik ders: BYF primi yüksekken BYF yerine ons ya da ETF alın.

---

## 6. Dünyadaki altın fiyatını nasıl yordarsınız

Kaynak: `arastirma/r3_kuresel_tahmin.md` (20 iddia doğru, 5 kısmen düzeltildi).

### 6.1 2026'da ne oldu

- **Seviye:**
  - 29.01.2026 zirvesi: LBMA PM 5.405 USD, gün içi 5.595 USD.
  - 30.10.2026 dibi: 3.870 USD.
  - 06.11.2026: ≈4.070 USD. Yılbaşından ≈−%5, zirveden ≈−%25.
- **Hikâye: reel faiz geri döndü.**
  - Mart 2026'daki İran savaşı Brent'i 71 USD'den Nisan'da 138 USD'ye taşıdı.
  - Enflasyon beklentisi Fed'i faiz artırımına itti: 16 Eylül'de +25 bps, %3,75–4,00.
  - Altın jeopolitik riske rağmen düştü; enflasyonist şokta güvenli liman olarak çalışmadı.
  - Altının haftalık getirisinin 10 yıllık TIPS değişimine betası 2024–25'te ≈0 idi, 2026'da −%16/puan oldu. Altın–Brent korelasyonu 2006–21'de +0,19 iken 2026'da −0,31.
- **Seviye modeli çöktü.** 2006–2021 verisiyle kurulan "log altın = a − b × reel faiz" modeli bugünkü %2,6 reel faizle ≈690 USD öngörüyor; fiyat bunun 5,7 katı. Reel faiz artık seviyeyi değil, en fazla **değişimi** açıklıyor.
- **Yapısal taban, merkez bankaları:**
  - 2022–2024'te her yıl >1.000 ton, 2025'te 863 ton, 2026'nın ilk 9 ayında 675 ton.
  - Goldman ayda ≈60 tonluk alımı taban kabul ediyor.
  - TCMB Mart 2026'da kur savunmasında rezervinden iki haftada ≈120 ton kullandı (satış + swap).
- **ETF'ler:** 2026 Ç3'te +211 ton, toplam rekor 4.275 ton. Ekim'de Kuzey Amerika fonlarından çıkış oldu.
- **Oynaklık rejimi:** 2026'da yıllık %29 (2015–24 ortalaması %15). Günlük standart sapma %1,9, 5 günlük %3,9. Aynı risk için pozisyon normal yıllara göre yarıya inmeli.

### 6.2 Ufuk bazında çerçeve

| Ufuk | Neye bakılır | Kanıt gücü |
|---|---|---|
| **1–5 gün** | Yön tahmini değil, olay ve rejim yönetimi. ABD veri takvimi (CPI, NFP 16:30 TSİ kışın), FOMC (22:00 TSİ, VİOP uzlaşmasından **sonra**), sürprizin yönü (2026'da güçlü veri → 2 yıllık faiz ve dolar ↑ → altın ↓), aynı günkü reel faiz, dolar ve petrol hareketi, pozisyon sıkışması, marj artışları, tatil boşlukları | Bizim testler: gecikmeli makro değişkenle OOS R² −%1,4 ile +%0,65 arası; ML ≤0 |
| **1–3 ay** | Fed yolu (FedWatch, dot plot), 10 yıllık TIPS **değişimi**, dolar (korelasyon ≈−0,4, istikrarlı), ETF akış trendi, merkez bankası aylık alımları, 2026'da petrol (negatif işaret), Çin primi ve Hindistan iskontosu | Orta. Rejime bağlı |
| **6–12 ay** | Merkez bankası alım hızı (aylık 60 ton ve üstü taban), Fed döngüsünün indirime dönüşü, de-dolarizasyon ve mali anlatı, özel yatırımcı çeşitlendirmesi. Değerleme: reel fiyat 1975–2012 ortalamasının ≈4 katı (Erb–Harvey) | Zamanlama aracı değil, senaryo bandı |

**Kurum modelleri:**
- Goldman: merkez bankası + ETF + spekülatif pozisyon çerçevesi.
- WGC: GRAM ve Qaurum modelleri.
- Bu modellerin hedefleri 2026'da fiyatı kovaladı. Goldman'ın 2026 sonu hedefi 4.900 → 5.400 → 4.900 → 4.650 → **4.150** (5 Kasım), 2027 sonu hedefi 4.800.
- Reuters anketi (27.10.2026): 2026 ortalaması 4.495, 2027 ortalaması 4.650. UBS Eylül 2027 için 5.400.

**Yaklaşan katalizörler:**
- ABD Ekim TÜFE: 10 Kasım, 16:30 TSİ.
- Kasım istihdamı: 4 Aralık.
- FOMC kararı: 9 Aralık 22:00 TSİ, yani VİOP uzlaşmasından sonra; etkisi ertesi günün getirisine düşer.
- Kasım TÜFE: 10 Aralık.
- 5–6 Kasım'da piyasa Aralık'ta faiz artırımına %64–81 olasılık veriyordu.

---

## 7. Türkiye'deki altın fiyatını nasıl yordarsınız

Kaynak: `arastirma/r4_turkiye_altin.md`, `g1_bosluk.md`, `analiz/a7_turkiye.md`.

### 7.1 Formül ve bileşenler

**gram altın (TL) ≈ ons (USD) × USDTRY / 31,1035 × (1 + p)**

Yerel prim p hangi piyasaya baktığınıza göre değişir:

| Piyasa | Prim p |
|---|---|
| VİOP gram altın (F_XAUTRYM) | ≈0. Aynı vade ayındaki "ons vadeli × USDTRY vadeli / 31,1035" sentetiğinden farkı 2026'da ortalama +%0,02, std %0,08. Bireye arbitraj yok |
| BIST KMKTP (toptan) | ≈0 (Ekim–Kasım 2026'da −%0,6 ile +%0,4) |
| Kapalıçarşı (perakende) | Prim + makas ±%1 ile +%8 arası. Ocak 2026'da ≈%7–8, 2026 Ç3'ün çoğunda iskonto |
| Darphane sertifikası (ALTINS1) | Gram altının ≈%9 üstünde (06.11.2026) |
| BIST altın BYF'leri | Ocak–Şubat 2026 çalkantısında +%3–8 |

### 7.2 Varyans: ons mu, kur mu?

| Dönem | Kurun gram altın günlük varyansındaki payı |
|---|---|
| 2017–2021 | ≈%86 (2018 %91, 2021 %94) |
| 2024 | %10 |
| 2025 | %8 |
| 2026 | ≈%0 |

VİOP vadeli getirileriyle 2024–2026 birlikte ölçülünce onsun payı %97.

Yıllık getiri katkısı örneği: 2021'de ons −%4, kur +%57 (log). 2024–2025'te ons baskın.

Sonuç: Bugün gram altını tahmin etmek ≈ onsu tahmin etmek (bölüm 6) + bilinen kur kaymasını eklemek demek.

### 7.3 Kur kayması tahmini

- **Yönetilen kur döneminde (2023-06+)** USDTRY'nin son 20 günlük ortalama günlük değişimi en iyi kısa vadeli tahminci.
  - Rastgele yürüyüşe göre R²: 1/3/5 gün için %8 / %14 / %16.
  - Nisan 2025'ten beri 60 günlük ortalamayla 5 günde %70–85.
  - 2026'da günlük ortalama +%0,073, std %0,090. Günlerin %89'unda kur yükseldi. Nisan 2025'ten beri |günlük değişim| > %0,5 olan gün yok.
- **VİOP USDTRY vadeli fiyatı kaymayı fazla fiyatlıyor.**
  - Yıllık ima edilen değer kaybı 2024'te %44,5, gerçekleşen %19.
  - 2025'te %39,2'ye karşı %21,8; 2026'da %31,6'ya karşı %19,8.
  - Bu fark TL carry primi. Gram altın vadelisinde uzun olana bedava kur getirisi yok, tersine maliyet.
- **Kuyruk riski siyasi şoklarda.**
  - 19.03.2025'te USDTRY tek günde +%3,3 arttı.
  - Mart 2026 savaşında kur kontrollü kaldı. Bedeli TCMB'nin ≈120 ton altın kullanımı ve büyük döviz satışıydı.
- **Politika faizi:** %36 (23.10.2026). Gecelik borç verme %39, borç alma %34,5.

### 7.4 Gram altın vadelisi (F_XAUTRYM) mi, ons vadelisi mi?

- **Gram altın vadelisi uzun = ons uzun + kaybettiren USD/TRY uzun.**
  - TL carry nedeniyle spot sentetiğin seans başına ≈%0,17 gerisinde kalıyor. Bu 3 seansta ≈%0,5, 5 seansta ≈%0,8 eder.
  - Takvim yayılımından ima edilen yıllık carry: 2024 %57,5, 2025 %44,8, 2026 %43,4.
- **1–5 günlük yön trade'i için F_XAUUSD daha temiz araç.**
  - Gram vadelisinin akşam seansı da yok.
  - Midas'taki VİOP yalnız gram altını sunuyor; bu, Midas'ta VİOP üzerinden altın almanın maliyetli yolu.
- **Gram vadelisinin sentetik primi** 1,4–3,9 günde ortalamaya dönüyor (t −6,9; 10/10 yıl). Ama üç bacaklı işlem maliyet sonrası zarar ediyor. Pratik kullanımı araç seçimi: prim yüksekken gram yerine ons al.

### 7.5 VİOP ons altının yerel primi (Q1 2026)

- **Q1 2026'da VİOP F_XAUUSD taşıma maliyetinin belirgin üstünde işlem gördü.**
  - Taşıma düşüldükten sonraki fazla baz aylık medyan olarak Ocak 2026'da 81 bps, Şubat'ta 61 bps, Mart'ta 124–136 bps idi.
  - En yüksek değer 03.03.2026'da 366–405 bps.
  - Nisan'da normale döndü; Ağustos–Kasım 2026'da 2–6 bps.
- **Sürücüler yurt içi.** Fazla bazın VİOP açık pozisyonuyla korelasyonu 0,68, BIST KMKTP altın işlem miktarıyla 0,59. USDTRY ile günlük ilişki yok.
- **Zamanlama:** TCMB 01.03.2026'da repo ihalelerine ara verdi. Ertesi gün fazla baz 260, 03.03'te 389 bps'e çıktı. Nedensellik kanıtlanmadı.
- **Pratik sonuç:** Prim yüksekken VİOP'ta uzun pozisyon, prim kapanırken spot hareketinin ötesinde ek kayıp yer. Fazla bazın gün bazında ortalamaya dönüşü istatistiksel olarak gerçek. Ancak ekonomik değeri drift ve taşıma etkisine gömülüyor, tek başına işlem kuralı değil.

### 7.6 Diğer Türkiye notları

- **İthalat kotası** Hazine ve Maliye Bakanlığı tarafından konuldu (07.08.2023'te yeniden). 2026'da bağlayıcı değil.
- **Türkiye'nin dünya fiyatına etkisi** hane talebinden çok TCMB işlemlerinden geliyor. 2026 Ç3'te Türkiye bar-sikke + mücevher talebi küresel talebin ≈%1,4'ü; 2020–24'te bar-sikke talebinde payı ≈%10.
- **Vergi ve maliyet:**
  - Banka altın hesabında fiziki teslimatsız alımda binde 2 BSMV.
  - Kapalıçarşı makası birkaç yüzde.
  - BIST altın BYF'leri %17,5 stopaj, VİOP %10.

---

## 8. Günlük rutin: sinyal betiği

`sinyal/sinyal_altin.py` ayakta kalan 11 kuralı her gün hesaplıyor. Ayrıntı `sinyal/KULLANIM.md`'de.

Doğrulama:
- Bağımsız bir denetçi 53 günde 2.225 değeri betiğin kodunu kullanmadan karşılaştırdı. Düzeltmelerden sonra fark 0, zaman damgası ihlali 0.
- Panelin tamamında (VİOP 2.427, ETF 4.743 gün) toplu kontrol yapıldı.

| Cephe | Çalıştır (TSİ) | Karar anı | Emir |
|---|---|---|---|
| VİOP, normal gün | 17:45–18:00 | 18:00 | 18:00–18:10 uzlaşma penceresinde |
| VİOP, TR yarım günü | 12:15–12:30 | 12:30 | 12:30–12:40. LOWMOM ve son saat kuralı devre dışı |
| Midas, kış (01.11.2026 → 14.03.2027) | 22:45–23:00 | 23:00 (15:00 ET) | 23:50–23:58 (15:50–15:58 ET) |
| Midas, yaz | 21:45–22:00 | 22:00 | 22:50–22:58 |

```bash
python3 -W ignore sinyal/sinyal_altin.py --canli                                   # bugün (ön-izleme ya da karar anı)
python3 -W ignore sinyal/sinyal_altin.py --canli --ozsermaye-tl 500000 --json bugun.json
python3 -W ignore sinyal/sinyal_altin.py --canli --tarih 2026-11-06                # geçmiş gün, ağdan
```

Bağımlılıklar `pandas`, `numpy` ve `requests`. İlk çalıştırma Dukascopy'den ≈200 aylık dosya indirdiği için 10–60 dakika sürebilir.

**TradingView izleme kodları** (08.11.2026'da sembol sayfalarından doğrulandı):

| Kullanım | Kodlar |
|---|---|
| VİOP | BIST:XAUUSD1!, BIST:XAUUSDZ2026, BIST:XAUUSDG2027, BIST:USDTRY1! |
| Spot ve COMEX | OANDA:XAUUSD, TVC:GOLD, COMEX:GC1! |
| ABD ETF'leri | AMEX:GLD, AMEX:IAU, AMEX:GLDM, AMEX:GDX, AMEX:GDXJ, AMEX:SLV, AMEX:SPY, AMEX:PHYS, AMEX:CEF |
| Kur | FX_IDC:USDTRY |

**Pazartesi 09.11.2026 tablosu** (Cuma verisiyle):

| Cephe | Sinyal | Durum |
|---|---|---|
| VİOP | LOWMOM | Pasif |
| VİOP | Çeyrek sonu | Pasif |
| VİOP | GDXJ artığı | Yeni dilim uzun |
| VİOP | Son saat | 14→15 UTC hareketine bağlı |
| VİOP | **Birleşik pozisyon** | **Fiilen düz** (+0,03 ya da −0,07 birim) |
| ETF | C2j, C2, C1 | Uzun |
| ETF | E3-1 | Spot altın 15:00 ET'de 4.065,68 USD'nin altındaysa GDXJ al |
| ETF | Tatil öncesi | Pasif (sonraki giriş 24 Kasım) |
| ETF | **Birleşim** | **Sermayenin %48–68'i uzun** (GDX %20, GDXJ %20 ya da %40, GLD %8) |

---

## 9. Risk, boyut, teminat

Kaynak: `sentez/HAKEM.md` §7, `arastirma/g4_bosluk.md`.

**VaR99 (tarihsel, %):**

| Araç | 2026, 1 gün | 2026, 5 gün | 2017–26, 1 gün | 2017–26, 5 gün |
|---|---|---|---|---|
| VİOP F_XAUUSD | 5,0 | 11,8 | 2,9 | 5,4 |
| GLD | 4,1 | 10,8 | 3,1 | 5,9 |
| GDXJ | 8,9 | 15,7 | 7,0 | 13,5 |
| NUGT | 16,9 | 27,4 | 13,5 | 25,2 (en kötü 5 gün −%79) |

**Kaldıraç:**
- Nominal/özsermaye 10 olursa (yalnız teminat kadar para), 2026'nın tipik kötü 5 günü özsermayenin tamamından fazlasını götürür.
- 5× nominalde kötü bir hafta özsermayenin %59'u eder.
- **Öneri: nominal ≤ 2× özsermaye** (5 günlük VaR99 ≈ %24). Hesabın kalanı TL nakitte olsun.

**Teminat çağrısı:**
- Yalnız başlangıç teminatıyla girilirse gün sonu çağrı olasılığı ≈%50/gün, 5 günde %70–79.
- 2 kat teminatla 5 günde 2017–2026'da %0,2–0,3, 2026'da %1,6–2,2.

**Boyutlandırma formülü (g4):**
- N = ⌊ %1 × √h × özsermaye_USD / (κ × σ̂_h × fiyat) ⌋. Tatil penceresinde κ = √2.
- σ̂ için en iyi model GJR-GARCH ile GVZ'nin ortalaması. EWMA ve RV20 daha kötü.
- Örnek: 06.11.2026'da 1 milyon TL özsermayeyle 3 sözleşme (0,62x kaldıraç). Pencere bir TR tatili içeriyorsa 2 sözleşme.

**Stop:**
- 2σ düşüşten sonra ortalama düşürmeyin ve "dip" diye almayın. Dönüş kuralları zarar ettiriyor; GDXJ'de 2σ düşüşten sonraki gün ortalaması −72 bps.
- "2σ düşüşten sonra 1 gün nakitte bekle" kuralı maliyetsiz ya da hafif yararlı: VİOP Sharpe 0,60, B&H 0,57.
- Asıl risk aracı pozisyon büyüklüğü. Felaket stopu (≈3σ ≈ %5,5) teminat çağrısını önlemek için.
- Akşam seansında stop kullanılamıyor.

**Tatil ve hafta sonu boşlukları:**
- TR tatil açılış günleri günlerin %2,9'u, ama uzlaşma varyansının %6'sını taşıyor.
- 5 günlük pencerelerin %14'ü bir tatil açılışı içeriyor.
- Pazartesi açılışında |boşluk| > %2 olasılığı %12. GARCH tipi modeller Pazartesi riskini %17–19 düşük gösteriyor.

---

## 10. Sınırlamalar ve sonucu bozabilecekler

- **Seçim yanlılığı.** Ayakta kalanlar binlerce test içinden seçildi. ETF'de çoklu testi geçen tek fenomen var (E3-1) ve onun net alfası anlamsız. Birleşim sonuçları üst sınır. **Gerçek doğrulama canlı veriyle olur:** sinyalleri en az 6 ay kâğıt üzerinde ya da çok küçük boyutla izleyin.
- **Saf olmayan OOS.** Birçok aday tam dönem t'siyle seçildi. Doğrulayıcılar "OOS gerçek dışarıda bırakılmış örneklem değil" uyarısı yaptı.
- **Rejim yığılması.** Kazançların önemli kısmı 2020 ve 2024–26 boğa/çöküş dönemlerinden. 2017–19 ve 2022–23 sakin dönemlerinde çoğu sinyal ≈0.
- **2026 rejimi istisnai.** Yıllık oynaklık %29, Ocak'ta %43. LOWMOM yapısal olarak pasif. Rejim sakinleşirse (rv20 < %12) yeniden devreye girer.
- **Midas'ta teyit edilemeyenler:** TL↔USD kur makası, MOC, kaldıraçlı/ters ETF ve PHYS listelemesi, SEC/FINRA satış ücretleri. Satış parasının T+1'de kullanılabilmesi 1 günlük kuralları kısıtlayabilir. ETF tarafının uygulanabilirliği uygulamadan kontrol edilmeli.
- **Maliyet.** Varsayılan perakende VİOP komisyonu (22–25 bps gidiş-dönüş) bütün yüksek devirli kuralları zarara çevirir. Komisyonu pazarlıkla ≈5 bps'e indirmeden bu kuralları kullanmayın.
- **Veri.**
  - Yahoo `=X` kurlarının günlük kapanışı kaymış; kurlar için Dukascopy ya da VİOP kullanıldı.
  - Yahoo PL=F 2008–09 kirli. BIST saatlik barları eksik.
  - Panelde jeopolitik risk endeksi sütunu hatalıydı. Ajanlar ham dosyayı kullandığı için sonuçlar etkilenmedi; kod düzeltildi.
  - Web arama kotası araştırmanın ortasında doldu. Türk akademik literatürü atıf zinciriyle tarandı. Ons altın vadelisi için Türkiye'de fiyat keşfi ya da lead-lag çalışması bulunamadı.
- **Korelasyon nedensellik değildir.** Mekanizması olan ilişkiler bile kısa vadede başka faktörlerle örtülebilir.

---

## Nasıl yapıldı

- **Ajanlar:** 59 alt ajan.
  - 9 web araştırmacısı, 9 bağımsız doğrulayıcı, 1 tamlık eleştirmeni, 4 boşluk doldurucu.
  - 11 kantitatif analist, 22 doğrulayıcı (11 bağımsız yeniden üretici, 11 çürütücü).
  - 1 metodoloji hakemi, 1 sinyal betiği yazarı, 1 kod denetçisi.
  - 221 araştırma iddiasının 188'i doğrulandı, 29'u kısmen doğru çıkıp düzeltildi, 1'i yanlış çıktı, 3'ü doğrulanamadı.
- **Test:** 7.446 kayıtlı test (`veri_ozet/test_kaydi/`). Hakem sınıflandırması: 4.751 birincil işlenebilir öngörü testi, 1.694 sağlamlık ve erken dönem varyantı, 1.001 tanı/mekanik/kopya.
- **Veri kaynakları:**
  - Borsa İstanbul VİOP günlük bülteni.
  - Dukascopy saatlik ve dakikalık BID.
  - Yahoo Finance.
  - ABD Hazinesi nominal ve reel faiz eğrileri.
  - CFTC disaggregated COT.
  - Sina (SHFE), Caldara–Iacoviello GPR, SSGA GLD/GLDM NAV geçmişi, Fed FOMC takvimi.
  - FRED bu ortamdan erişilemedi.

## Dosyalar

| Klasör / dosya | İçerik |
|---|---|
| `RAPOR.md` | Bu dosya |
| `sentez/HAKEM.md` | Çoklu test düzeltmesi, 65 iddianın son güven tablosu, örtüşme, birleşim, bugünkü durum, literatür karşılaştırması, risk |
| `sentez/sinyal_tablosu.csv` | 65 iddia: kural, bilgi zamanı, t, Sharpe, REP/ADV/SON güven |
| `sentez/fdr_*.csv`, `birlesim*.csv`, `risk_*.csv`, `s0*.py`, `sl.py`, `run_all.sh` | Hakem hesapları |
| `sinyal/sinyal_altin.py`, `sinyal/KULLANIM.md`, `sinyal/test_sinyal_altin.py`, `sinyal/bagimsiz_kontrol.py` | Günlük sinyal betiği, kullanım, testler, bağımsız denetim |
| `analiz/` | 11 kantitatif ailenin raporları |
| `arastirma/` | Web araştırma raporları: r1 kontrat, r2 stratejiler, r3 küresel tahmin, r4 Türkiye, r5 lead-lag literatürü, r6 kim kazanıyor, r7 olay takvimi; Midas için m1 platform ve vergi, m2 ETF stratejileri; boşluk raporları g1–g4 |
| `dogrulama/` | Yeniden üretici ve çürütücü hükümlerinin özetleri, araştırma doğrulamaları |
| `kod/veri_hazirlik/` | Panel kurucular (p1–p4), ortak kütüphane `lib_altin.py` |
| `kod/indirme/` | Veri indiriciler |
| `kod/analiz/` | Ajan analiz kodları |
| `kod/DATA_README*.md` | Panel sütunları ve zaman kuralları. Not: g2 bulgusuna göre bülten AÇILIŞ alanı 23.09.2022'den beri açılış seansı fiyatı; akşam seansı ana bültende yok |
| `veri_ozet/` | Getiri dağılımı, VİOP likidite ve baz tablosu, bütün test kayıtları |

Ham veri dosyaları (≈1 GB) repoya eklenmedi; indiricilerle yeniden indirilebilir. `sinyal_altin.py --canli` araştırma paneli olmadan çalışır.

Yatırım tavsiyesi değildir.
