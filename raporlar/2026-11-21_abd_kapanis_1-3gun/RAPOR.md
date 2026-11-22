# ABD piyasasında kapanış sinyali ve 1–3 gün taşıma: ne çalışıyor, ne çalışmıyor

22 Kasım 2026 · Yatırım tavsiyesi değildir.

**Profil:** Gün içi işlem yok. Karar ABD kapanışında (16:00 New York saati; kışın 00:00 TSİ) veriliyor, pozisyon 1–3 işlem günü taşınıyor. Bakılan şey lead-lag: bir varlığın bugünkü hareketi başka bir varlığın sonraki günlerini öngörüyor mu?

Raporda geçen terimler: **bps** (baz puan) = %0,01. **VIX** = S&P 500 opsiyonlarından hesaplanan beklenen oynaklık endeksi. **Örneklem dışı** = kuralın seçilmesinde kullanılmayan, yalnız sınamaya ayrılan dönem. **Korunma** = pozisyonun piyasa riskini ters yönlü bir endeks pozisyonuyla azaltma. Köşeli parantezdeki kodlar (ör. [R9-01]) kaynak listesindeki satırları gösterir.

## 1. Kısa yanıt

- **ABD'de bu yöntemle kullanılabilir bir kural bulamadım.** 3.420 önceden yazılı kural varyantı ve 27.351 tarama regresyonu sınandı; maliyet sonrası, örneklem dışı dönemde ayakta kalan ve bugün kullanılabilecek kural yok.
- **Lead-lag bilgisi var ama aynı gün fiyatlanıyor.** Ertesi günlere kalan kısım işlem başına brüt 5–30 bps; bireysel yatırımcının maliyetini karşılamıyor.
- **Bugün "düşeni al" sinyallerinin neredeyse hepsi yanıyor** (S&P 500 yedi gün üst üste düştü, VIX 35,9). Bu kurallar ne 2010–2019 eleğinden ne de 1993–2004 sınavından geçti. Pazartesi tetiklenirlerse bu doğrulanmış bir kenar değil, çıplak risktir.
- **Kaldıraç kenar üretmiyor, yalnız riski büyütüyor.** 3x ETF'ler bu oynaklıkta üç günde 27–88 bps'i yalnız yapıları gereği kaybettiriyor.
- **Senin varsayımın için düzeltme:** riski kabul etmek tek başına "ciddi kazanç" getirmiyor; kazanç için sınanmış bir kenar gerekiyor ve ABD içinde bu yöntemle çıkmadı. VİOP'taki kenarının kaynağı (ABD kapandıktan sonra BIST'in açılması) ABD'nin kendi içinde yok.

## 2. Ne yapmalıyım

1. **Bu yöntemle ABD'de gerçek parayla işleme başlama.** Aşağıdaki hiçbir kural "uygun" ya da "koşullu" sınıfına giremedi.
2. **Pazartesi (23 Kasım) için:** S&P 500 düşüşle kapanırsa RSI(2), "kapanış günün dibinde" ve "üst üste düşüş" sinyalleri tetiklenecek. Bunlara dayanarak alım yapacaksan bunu sinyal değil, kendi takdirin olan bir bahis say. Boyutu 3.8'deki tablonun "VIX 30 üstü kuyruk" sütununa göre seç ve kaldıraçlı ETF'yi üç gün taşıma.
3. **İki hipotezi 2–3 ay kâğıt üstünde izle** (3.12). Gerçek paraya ancak izleme döneminde de tutarlarsa ve küçük boyutla geç.
4. **Aracı kurumuna şu beş soruyu sor** (yanıtlar hangi kuralın uygulanabileceğini belirler): ABD'de kapanış emri (MOC/LOC) verebiliyor muyum; açığa satış var mı; TQQQ, SQQQ, SOXL gibi kaldıraçlı/ters ETF'ler alınabiliyor mu; seans öncesi/sonrası emirde ek ücret ne; işlem başına toplam komisyon ne.
5. **Vergi için bir danışmana tek soru sor:** yurt dışı hisse/ETF alım satımında alış ve satış hangi günün kuruyla TL'ye çevrilir? Resmî metinde bunu göremedik (3.10).
6. **Aynı yöntemi kenarın yapısal olduğu yerde kullan.** ABD kapanışındaki bilgi BIST'e ertesi gün yansıyor; ABD'nin kendi içinde aynı gün yansıyor. Emeğin karşılığı büyük olasılıkla birinci tarafta (önceki VİOP çalışman), ikincisinde değil. Bu bir çıkarımdır; bu raporda ayrıca sınanmadı.

## 3. Gerekçe ve kanıt

### 3.1 Ne sınandı, nasıl

- **Veri:** 470 kod (ETF, hisse, endeks), 2005–2026 günlük açılış/kapanış; bilanço tarihleri (SEC kayıtları), opsiyon konumlanma verisi, son iki yılın saatlik verisi.
- **Kurallar hesaptan önce yazıldı:** 12 araştırma ajanının literatürden çıkardığı 94 kural ve yöntem denetçisinin ekledikleri; toplam 3.420 varyant (tutma süresi 1, 2, 3 gün ve "ertesi açılışta çık").
- **Üç dönem:** 2010–2019 keşif, 2020–2023 örneklem dışı doğrulama, 2024–2026 kilitli son dönem. Bir kural önce keşif döneminde aday olmalı, sonra doğrulamadan geçmeli.
- **Maliyet:** bacak başına alış-satış farkı ve komisyon; uzun pozisyonda nakit faizi, açığa satışta ödünç ücreti. Ayrıca yalnız komisyonlu ikinci bir senaryo (3.5).
- **Yanlış pozitife karşı önlemler:** VIX gibi kapanıştan sonra kesinleşen seriler bir gün gecikmeli kullanıldı; tek yönlü (yalnız alım) kurallarda kazancın varlığın kendi yükselişinden ayrışması arandı; sistematik taramada bütün zincir 400 kez plaseboyla (sinyal ile getiri bağı koparılarak) yeniden çalıştırıldı.
- **Motorun denetimi:** hesap motorunu ayrı bir ajan denetledi; 9.941 işlem motoru kullanmadan yeniden hesaplandı, fark çıkmadı. Kasıtlı olarak bir gün ileri kaydırılmış hileli bir sinyali motor yakalıyor.

### 3.2 Aile aile sonuç

| Aile | Sınanan | Keşifte aday | Doğrulamadan geçen |
|---|---|---|---|
| Lider → takipçi (13 tema kümesi) | 1.048 | 1 | 0 |
| Çiftler, sektöre göre sapmanın dönüşü | 216 | 0 | 0 |
| Çapraz varlık → sektör (kredi, faiz, dolar, emtia) | 164 | 1 | 0 |
| Endekste uç hareket, "düşeni al" | 674 | 10 | 0 |
| Akış vekilleri, kapitülasyon, genişlik | 124 | 1 | 0 |
| Takvim ve olay (ay dönümü, FOMC, vade haftası) | 191 | 4 | 0 |
| Volatilite ürünleri ve konumlanma verisi | 449 | 5 | 0 |
| Bilanço etrafı | 376 | 23 | 1 |
| Gece–gündüz | 178 | 1 | 0 |
| **Toplam (önceden yazılı)** | **3.420** | **46** | **1** |
| Sistematik tarama (60 sepet × 173 hedef × 3 vade) | 27.351 | 26 | 0 |

Doğrulamadan geçen tek kural (bilanço öncesi dönüş) 2024–2026'da zarara döndü ve çoklu test düzeltmesinden geçemiyor (3.3). Tarama plasebodan ayırt edilemedi: gerçek zincirde geçen 0, plasebo koşularının %95'inde en çok 1.

Aile başına öne çıkanlar:

- **Lider → takipçi:** Nvidia/TSMC/Broadcom → yarı iletkenler, Bitcoin → kripto hisseleri, Tesla → elektrikli araçlar, JPMorgan → bankalar ve diğer kümeler. Yarı iletkende "takipçi lidere göre geride kaldıysa ertesi gün yakalar" kuralı 6.755 işlemde brüt +4,9 bps verdi; korunmalı bir işlemin modellenen gidiş-dönüş maliyeti ortalama 27 bps.
- **Çapraz varlık:** bilgi aynı gün bitiyor. 2010–2023'te petrol ETF'i ile enerji ETF'inin aynı gün korelasyonu 0,64, ertesi gün −0,02. Yüksek getirili tahvil ile S&P için 0,77'ye karşı −0,06; dolar ile gelişen piyasalar için −0,33'e karşı −0,03.
- **Sapmanın dönüşü:** büyük hisselerde istatistiksel olarak var (bacak başına brüt 1–5 bps), ekonomik olarak yok. Bilanço içeren sapmalar dönmüyor, sürüklenmeye devam ediyor.
- **Takvim:** yalnız alım yönlü takvim kurallarının çoğu endeksin genel yükselişini taşıyor. Tahvilde ay sonu etkisi 2010–2019'da güçlüydü, 2020'den sonra eridi.
- **Volatilite ürünleri:** vade yapısına dayalı kısa volatilite kuralları günlük ETF maliyetiyle zarar ediyor; temsilci stratejilerde en büyük düşüş %86–99,9.
- **Gece–gündüz:** S&P ETF'inde kapanıştan açılışa brüt getiri sürüyor (2021–2026'da günde +3,4 bps) ama gidiş-dönüş maliyeti (yaklaşık 5,7 bps) bunu aşıyor.

### 3.3 En yakın adaylar ve neden elendiler

| Kural | 2010–19 | 2020–23 | 2024–26 | Karar |
|---|---|---|---|---|
| Bilanço öncesi dönüş: bilançodan 2 gün önce, son 2 günde endekse göre en kötü beşte birlikteki büyük hisseyi al; bilanço tepki gününün ertesi günü sat | +85 bps | +124 bps | −59 bps | Düşük: son dönem negatif |
| Bilanço günü sektörüne göre %10'dan fazla düşen büyük hissede 3 gün açığa satış (endeks korunmalı; yalnız komisyonlu senaryo) | +123 bps | +135 bps (48 işlem) | +53 bps | Düşük: az olay, eşik altı |
| Bilanço öncesi prim: bilançodan 3–10 gün önce al, ertesi gün sat (yalnız komisyonlu senaryo) | +30 bps | +40–61 bps | −40 ile −43 bps | Elendi: son dönem negatif, profil dışı vade |
| Dow ETF'i 5 gün üst üste düşünce al, 1 gün tut | +33 bps | +42 bps (20 işlem) | −3 bps | Düşük: az olay |
| Tahvil ETF'i ay sonu alımı (son 3 gün) | +41 bps | +16 bps | +1 bps | Düşük: 2020 sonrası eridi |
| S&P → küçük hisseler, ters yön (S&P ±%1'den sonra) | +3 bps | +4 bps | +14 bps | Düşük: anlamsız, çok küçük |

Sayılar işlem başına net ortalamadır. İlk kuralda kazancın yaklaşık yarısı, verinin bugünün hisselerinden kurulmasının yarattığı yanlılıktan geliyor (iflas eden ve borsadan çıkan şirketler veride yok); en iyi %5 işlem çıkarılınca 2010–2019 ortalaması negatife dönüyor.

### 3.4 Bugünkü rejim ve "düşeni al"

**Piyasanın durumu (20 Kasım 2026 kapanışı):**
- S&P 500 %3,7 düşüşle 6.910; hafta −%8,6; 6 Ekim rekorundan %10'dan fazla aşağıda [R11-12]. Yedi gün üst üste düşüş. VIX 35,9.
- Nvidia 6 Ekim zirvesinden −%47,5. 12 Kasım'da CEO Jensen Huang istifa etti [R11-17]; 17 Kasım'da sonuçlar açıklandı (gelir 115,8 milyar $) [R11-20]; aynı gün ve 20 Kasım'da SEC incelemesi haberleri çıktı [R11-15, R11-16]. 20 Kasım'da hisse yaklaşık %14, yarı iletken endeksi %10,7 düştü [R11-14].
- Fed faiz artırıyor: 16 Eylül'de %3,75–4,00 [R11-01]; sonraki toplantı 8–9 Aralık [R11-04]. Vadeli piyasanın Aralık'ta artırıma yaklaşık %95 olasılık verdiği bilgisi tek bir ikincil kaynağa dayanıyor [R11-06].
- 10 yıllık Hazine faizi 5 Ekim'de %5,31 ile zirve yaptı, 20 Kasım'da %4,92 [R11-10].

**"Düşeni al" kurallarının sınavı:**
- 2010–2019'da tutmadılar: S&P ETF'inde RSI(2) < 10 (iki günlük göreli güç endeksi; çok sert kısa vadeli düşüşü gösterir) ve "kapanış günün dibinde" kuralları işlem başına net 1–18 bps verdi, anlamsız.
- VIX 30'un üstünde ve endeks 200 günlük ortalamasının altındayken 2005–2026 toplamında güçlü görünüyorlar: RSI(2) < 10 kuralı 61 işlemde +141 bps. Ama bu, sonuçlara bakıldıktan sonra seçilmiş bir alt küme.
- Bu yüzden hipotezi, projede hiç kullanılmamış 1993–2004 verisinde, ölçütleri önceden yazarak sınadım. **İkisi de elendi:** RSI(2) < 10 kuralı 35 işlemde net −9 bps, "kapanış günün dibinde" kuralı 41 işlemde +1 bps. İkisi de aynı rejimdeki sıradan bir günün ortalamasının (+15 bps) altında kaldı; beş bölümün yalnız ikisi artıda.
- Çekince: 1993–2004 örneklemi küçük. Test 2005–2026 büyüklüğünde bir etkiyi reddediyor, orta büyüklükte bir etkiyi dışlayamıyor. 2005–2026'daki kazancın %68'i iki bölümden (2008–09 ve 2020) geliyor.

**Bugüne benzeyen günler (betimsel; sinyal değil).** S&P ETF'inin 7 ve daha fazla gün üst üste düştüğü 2005'ten beri 7 seri:

| Sonraki | Ortalama | Medyan | Yükselen | En kötü |
|---|---|---|---|---|
| 1 gün | +%2,7 | +%0,8 | %71 | −%2,6 |
| 3 gün | +%2,3 | +%2,2 | %86 | −%4,3 |
| 5 gün | +%1,8 | +%1,7 | %86 | −%6,4 |

Ortalamayı 10 Ekim 2008'in tek günlük +%14,5'i taşıyor. Yedi gözlem bir kural kurmaya yetmez.

**Bu kuralların felaket dönemleri:** "VIX 35 üstünde al" kuralı Eylül–Kasım 2008'de 46 işlemde toplam −2.809 bps kaybetti (9 ardışık kayıp), Şubat–Mart 2020'de −1.927 bps. Ekim–Kasım 2026'da RSI(2) < 10 kuralı 7 işlemde −728 bps kaybetti.

### 3.5 Sonuç maliyet varsayımına bağlı mı?

Birincil maliyet modeli piyasa emrine göre kurulu. Oysa kapanış emri (MOC) kapanış müzayedesinin tek fiyatından dolar; alış-satış farkı ödenmez [R9-01, R9-12]. Bu yüzden bütün kuralları bacak başına yalnız 1,5 bps komisyonla yeniden elettim; ölçütleri yine önceden yazdım.

- Keşif dönemi adayı 46'dan 69'a çıktı.
- Doğrulama döneminde 5 kural anlamlı göründü; hepsi bilanço ailesinden.
- Hiçbiri ölçütlerin hepsini sağlamadı: dördü 2024–2026'da zarar ediyor, beşincisi (3.3'teki açığa satış kuralı) eşiğin altında ve 48 işleme dayanıyor.

Sonuç: "kullanılabilir kural yok" bulgusu maliyet varsayımından bağımsız.

### 3.6 Lead-lag neden burada çalışmıyor?

- **Eşzamanlılık.** ABD'de lider de takipçi de aynı saatlerde işlem görüyor; bilgi aynı gün fiyata giriyor (3.2'deki korelasyonlar). VİOP'ta bulduğun öncülükler, ABD seansı sırasında BIST'in kapalı olmasından doğuyordu.
- **Yayımlanmış kanıt da aynı yönde.** Günlük lider → takipçi stratejileri akademik çalışmalarda yalnız tek yön maliyet 10 bps'in altındayken kazandırıyor [R4-01]; lider/takipçi ilişkileri nadiren 6 aydan uzun yaşıyor [R4-11]. Büyük hisselerde bilanço sonrası sürüklenme 2006'dan beri yok [R6-01]. FOMC öncesi yükseliş 2015'ten sonra kayboldu [R7-13].
- **Kalan tek sistematik etki oynaklık satışına benziyor.** Kısa vadeli dönüşün getirisi VIX yükseldikçe artıyor [R5-14, R5-17], ama aynı strateji VIX sıçramaya devam ettiğinde kaybediyor [R5-18]. Yani "kazanç" büyük ölçüde taşınan kuyruk riskinin karşılığı.

### 3.7 Kaldıraçlı ETF'yi 1–3 gün taşımak

Kaldıraçlı ETF her gün yeniden dengelenir; birkaç gün tutulduğunda getirisi "kaldıraç × endeks getirisi"nden sapar. Bu sapma (maliyet ve oynaklık aşınması) 2010–2026 verisinde şöyle:

| Durum | TQQQ (3x Nasdaq) | SOXL (3x yarı iletken) | SQQQ (−3x) | SOXS (−3x) |
|---|---|---|---|---|
| VIX 30 üstü, 3 gün | −27 bps | −33 bps | −41 bps | −88 bps |
| S&P %3'ten fazla düştükten sonra, 3 gün | −90 bps | −97 bps | – | −189 bps |

- Tek günde sapma 2–5 bps; sorun birden fazla gün taşımakta ve yüksek oynaklıkta.
- Bugün ikisi de geçerli: VIX 35,9 ve S&P bir günde %3,7 düştü.
- En kötü tek gün: TQQQ −%34,5 (16 Mart 2020), SOXL −%38,7 (5 Kasım 2026).
- Tek hisse kaldıraçlı ürünlerde gider oranı kaynağa göre değişiyor (NVDL için %1,05 ya da %1,64) [R12-22]; prospektüse bakılmalı.

### 3.8 Risk ve boyut

10.000 $ sermayenin %1'ini (100 $) riske atan pozisyon büyüklüğü. "Olağan" sütun son 60 günün bir günlük standart sapmasına, "VIX 30 üstü kuyruk" sütunu VIX 30'un üstündeyken görülen en kötü %1'lik güne göre hesaplandı. Bugün ikinci sütun geçerli.

| Kod | Bir günlük σ | Olağan | VIX 30 üstü kuyruk | 3 gün, kuyruk |
|---|---|---|---|---|
| SPY | %1,1 | 9.100 $ | 1.280 $ | 860 $ |
| QQQ | %1,7 | 5.900 $ | 1.380 $ | 1.030 $ |
| NVDA | %3,0 | 3.300 $ | 810 $ | 550 $ |
| TSLA | %3,1 | 3.250 $ | 620 $ | 340 $ |
| MSTR | %5,5 | 1.830 $ | 940 $ | 580 $ |
| TQQQ | %5,0 | 2.000 $ | 520 $ | 350 $ |
| SQQQ | %5,1 | 1.980 $ | 460 $ | 350 $ |
| SOXL | %11,0 | 910 $ | 390 $ | 290 $ |
| SOXS | %11,1 | 900 $ | 320 $ | 240 $ |

- 343 kodun tamamı: `ek/veri/risk_ve_boyut_tablosu.csv`.
- Endeks korunması endeks, sektör ve kaldıraçlı endeks ETF'lerinde varyansı %55–90 azaltıyor; tek hisselerin çoğunda (Apple, Microsoft, Palantir, Eli Lilly ve benzerleri) %20'den az.
- Opsiyon gama pozisyonu (GEX) negatifken ertesi günün oynaklığı 2–3 katına çıkıyor. Bu bir kazanç kuralı değil, boyutu küçültme işareti.

### 3.9 Uygulama: emir, saat, maliyet

- **Kapanış emri kesimi:** New York borsasında 15:50'den sonra kapanış emri girilemez ve iptal edilemez [R9-01]. Interactive Brokers bütün borsalar için 15:50'yi esas alıyor [R9-03, R9-04]. Kışın 23:50 TSİ.
- **Sinyal 15:50'de hesaplanır, kapanışta değil.** Bu rapordaki kurallar kapanış fiyatıyla sınandı; gerçek uygulamada son 10 dakikanın hareketi sinyali değiştirebilir.
- **Kapanış fiyatının kendisi gürültülü:** müzayede öncesi fiyattan ortalama 8,1 bps sapıyor ve büyük hisselerde bu sapma gece geri dönüyor [R9-14].
- **Komisyon:** Interactive Brokers'ta hisse başına 0,005 $, en az 1 $ [R9-15]; 10.000 $'lık emirde gidiş-dönüş yaklaşık 2 bps. Komisyonsuz hesap türü yalnız ABD yerleşiklerine açık.
- **Gece seansı:** alış-satış farkı belirgin geniş (sık işlem gören hisselerde 28 bps'e karşı gündüz 20 bps) [R9-11]. Borsalarda neredeyse 24 saat işlemin 6 Aralık 2026'da başlaması planlanıyor [R9-07].
- **Açığa satış:** bir günde %10 düşen hissede o gün ve ertesi gün açığa satış kısıtlanır [R9-29]. Kaldıraçlı ETF'de teminat kaldıraçla çarpılır: 3x üründe uzun pozisyon için %75 [R9-24].
- **Mikro vadeli sözleşmeler:** S&P mikro sözleşmesinde sürdürme teminatı 2.919 $, Nasdaq'ta 4.574 $ (bir aracı kurumun sayfasından; borsanın tablosu görülemedi) [R9-28].

### 3.10 Türkiye: erişim ve vergi

- **Erişim:** yurt dışı hisse/ETF işlemi SPK yetkili banka ya da aracı kurum üzerinden yapılmak zorunda (Mart 2025 değişikliği) [R10-12]. Kendi başına yurt dışı kuruma gitme istisnası yalnız türev işlemler için [R10-13]. Kaldıraçlı işlem ve fark sözleşmeleri (CFD) yalnız SPK yetkili kurumlardan yapılabilir [R10-14].
- **Vergi:** yurt dışı borsadaki alım satım kazancı değer artışı kazancıdır ve yıllık beyannameyle beyan edilir [R10-01]. 2026'nın 150.000 TL'lik istisnası menkul kıymet kazancına uygulanmaz [R10-03]; elde tutma süresi istisnası da yok [R10-02]. Yani vergi ilk liradan başlar.
- **Zarar:** aynı yıl içindeki yurt dışı menkul zararları kazançtan düşülür; başka gelirlerden düşülemez [R10-07].
- **Oranlar (2026):** 190 bin TL'ye kadar %15, 400 bine kadar %20, 1 milyona kadar %27, 5,3 milyona kadar %35, üstü %40 [R10-09].
- **Beyan:** kanunda 1–25 Mart; idare 2025 kazancı için 31 Mart'a kadar kabul etti. Ödeme Mart ve Temmuz'da iki taksit [R10-11].
- **Doğrulanamayan nokta:** alış ve satışın hangi günün kuruyla TL'ye çevrileceği ve dolarda zarar varken TL'de çıkan kârın vergilenip vergilenmeyeceği resmî metinde açık değil [R10-05]. Sık işlem yapan biri için bu, her işlemde birkaç günlük kur farkı demek.
- **ABD tarafı:** satış kazancı ABD'de vergilenmez; temettüde anlaşma oranı en çok %20 [R10-24].

### 3.11 Önümüzdeki haftalar (risk takvimi; sinyal değil)

| Tarih | Olay |
|---|---|
| 25 Kasım | 3. çeyrek büyüme 2. tahmin, Ekim kişisel harcama fiyatları (PCE) [R12-04] |
| 26 Kasım | Borsa kapalı (Şükran Günü) |
| 27 Kasım | Yarım gün, kapanış 13:00 [R12-08] |
| 4 Aralık | Kasım istihdam raporu [R12-02] |
| 8–9 Aralık | Fed toplantısı, projeksiyonlu [R12-01] |
| 9 Aralık | Broadcom sonuçları, kapanış sonrası [R12-14] |
| 10 Aralık | Kasım tüketici enflasyonu [R12-02] |
| 18 Aralık | Üçlü opsiyon vadesi |
| 21 Aralık | Nasdaq-100 yıllık yeniden yapılandırması yürürlükte (hesapla bulunan tarih) [R12-10] |
| 24 Aralık | Yarım gün [R12-08] |

Diğer bilanço tarihleri (Salesforce, Oracle, Micron ve benzerleri) tahmini; şirket duyurusundan teyit edilmeli [R12-15].

### 3.12 İzleme listesi (kâğıt üstünde; gerçek para değil)

| # | Hipotez | Kural | Durumu |
|---|---|---|---|
| 1 | Bilanço şokunun devamı | Büyük bir hisse bilanço tepki gününde sektör ETF'ine göre %10'dan fazla düşerse, kapanışta açığa sat (endeks korunmalı), 3 gün sonra kapat | Düşük güven. Üç dönemde de işareti aynı (+123, +135, +53 bps) ama doğrulamada yalnız 48 işlem var; açığa satış gerektirir |
| 2 | Kriz rejiminde tepki alımı | VIX önceki gün 30'un üstünde ve S&P ETF'i 200 günlük ortalamasının altındayken RSI(2) < 10 kapanışında al, ertesi kapanışta sat | 1993–2004'te elendi; 2005–2026'da güçlü. Yalnız izlemek için |

İzleme için önceden ölçüt: en az 30 işlem; net ortalama pozitif; en iyi iki işlem çıkarılınca hâlâ pozitif. Ölçüt sağlanmadan boyut büyütülmez.

## 4. Emin olunmayanlar ve doğrulama kapsamı

**Sonucun sınırları:**
- **Hayatta kalma yanlılığı:** veri bugünün hisselerinden kuruldu; iflas eden ve borsadan çıkan şirketler yok. Bu, yalnız alım yönlü kuralları olduğundan iyi gösterir. Sonuç zaten olumsuz olduğu için yön değişmez, ama 3.3'teki bilanço kurallarının geçmiş kazancı şişkindir.
- **Kapsam:** sistematik tarama sepet düzeyinde ve doğrusal ilişki arar; hisse → hisse düzeyi ve 2018 sonrası listelenen 89 kod dışarıda kaldı. Kuantum kümesi hacim süzgecinden geçemediği için sınanamadı; uzay ve yapay zekâ yazılımı kümelerinde örneklem çok küçük.
- **Çıkış kuralları:** yalnız sabit süreli tutma sınandı (1, 2, 3 gün ve ertesi açılış). Eşiğe bağlı çıkışlar sınanmadı.
- **Keşif dönemi sakin bir dönem:** 2010–2019'da VIX'in 30'u aştığı gün az. Rejime bağlı bir etki bu elekten geçemeyebilir; bunu 1993–2004 testiyle ayrıca sınadım (3.4), o da olumsuz çıktı.
- **Bilanço ailesi:** bilanço tepki gününü belirleyen iki yöntem olayların %12–20'sinde uyuşmuyor; bu aile en iyi durumda "koşullu" olabilirdi.
- **Kapanış gerçekçiliği:** sinyalin 15:50'de hesaplanması yalnız birkaç kuralda, son iki yılın saatlik verisiyle yoklandı.
- **Aracı kurum:** kullandığın kurumun kapanış emri, açığa satış ve kaldıraçlı ETF sunup sunmadığını bilmiyorum.

**Doğrulama kapsamı:**
- **Olgu satırları:** 157 satır kaynağından kontrol edildi. 130'u doğrulandı, 22'si düzeltildi (düzeltilmiş hâlleri kullanıldı), 4'ü doğrulanamadı, 1'i yanlış çıktı ve rapora alınmadı. Türkiye erişim/vergi satırları resmî metinle ikinci kez kontrol edildi.
- **Hesap:** motor bağımsız kodla denetlendi (9.941 işlem). "Düşeni al" sonuçları motoru kullanmayan ayrı bir kodla birebir yeniden üretildi (61 ve 102 işlem, brüt ortalamalar aynı).
- **Yöntem:** plan hesaptan önce ayrı bir denetçiye eleştirtildi; 15 itirazın hepsi plana işlendi. Sonradan eklenen iki test (1993–2004 sınavı ve maliyet senaryosu) veriye bakılmadan önce yazılıp kaydedildi.
- **Açık kalanlar:** kur çevirme kuralı [R10-05]; komisyon ve faizin vergi matrahından indirimi [R10-06]; ISM veri tarihleri [R12-07]; Aralık artırım olasılığı ve 20 Kasım SEC haberi tek ikincil kaynağa dayanıyor; Şubat 2018'de kapanan ters volatilite ürününün fiyatları arama özetlerinden alındı.

## 5. Kaynaklar

<!--KAYNAKLAR-->
Köşeli parantezli kodlar bu listedeki satırlardır. Her satır bu oturumda kaynağından kontrol edildi; durum sütunu doğrulayıcının kararıdır.

- **[R4-01]** (doğrulandı) DeMiguel ve ark.: çapraz ve öz otokovaryansı kullanan VAR portföyleri, geleneksel portföyleri yalnız maliyet 10 bp'nin altındayken geçiyor (günlük veri). — https://typeset.io/pdf/stock-return-serial-dependence-and-out-of-sample-portfolio-z1r2jq0yiu.pdf
- **[R4-11]** (doğrulandı) Cartea ve ark.: lider/takipçi kimliği sık değişiyor; bir pencerede bulunan ilişki nadiren 6 aydan uzun kârlı kalıyor. — https://ora.ox.ac.uk/objects/uuid:173a88b2-f00c-4346-8868-aabbd97ec8d7/files/dt722h970m
- **[R5-14]** (doğrulandı) Nagel: koşulsuz getirisi düşük olan sektör portföyü dönüş stratejileri bile VIX yüksekken yüksek getiri ve Sharpe verir. — https://www.nber.org/system/files/working_papers/w17653/w17653.pdf
- **[R5-17]** (doğrulandı) Aynı çalışma: VIX'te 1 puan artış dönüş getirisini 9 bp artırır (ortalama 17 bp); bu Nagel'i yalnız büyük hisselerle doğrular. — https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2020/12/18-20.Drechsler2.pdf
- **[R5-18]** (doğrulandı) Dönüş stratejisi örtük olarak oynaklık satışıdır: VIX²'de 1 puan artış aynı dönemde 20 bp kayıpla ilişkili; 2008 ve 2020 krizlerinde risk en yüksek. — https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2020/12/18-20.Drechsler2.pdf
- **[R6-01]** (doğrulandı) Büyük hisselerde bilanço sonrası sürüklenme 2006'dan beri yok; mikro hisselerde yakın zamanda kayboldu (örneklem 1973/1984–2019). — https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf
- **[R7-13]** (doğrulandı) FOMC öncesi sürüklenme 2015 sonrasında fiilen kayboldu (Kurov ve ark. 2021; ön taramadan, sayfa yeniden açılmadı). — https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html
- **[R9-01]** (doğrulandı) NYSE kapanış müzayedesinde MOC/LOC emir girişi 15:50 ET'de kesilir; sonrasında yalnızca dengesizliği dengeleyen emirler girer ve iptal talepleri reddedilir. — https://www.nyse.com/trade/auctions ; https://www.nyse.com/publicdocs/nyse/NYSE_Auctions_Closing_Process_Fact_Sheet.pdf
- **[R9-03]** (doğrulandı) IBKR, NYSE Arca dahil tüm NYSE borsaları için MOC/LOC emrinin 15:50 ET'ye kadar alınması gerektiğini yazıyor (borsanın 15:59 kuralından daha sıkı). — https://www1.interactivebrokers.com/en/trading/orders/moc.php
- **[R9-04]** (doğrulandı) IBKR'de Nasdaq MOC emri 15:55'e, LOC 15:58'e kadar girilebilir ama 15:50'den sonra iptal ya da değişiklik yapılamaz. — https://www1.interactivebrokers.com/en/trading/orders/moc.php ; https://www.nasdaqtrader.com/content/productsservices/Trading/ClosingCrossfaq.pdf
- **[R9-07]** (doğrulandı) 23/5 işlem 6 Aralık 2026 Pazar akşamı başlıyor: Nasdaq, NYSE Arca, Cboe EDGX, MEMX ve 24X'te gece seansı 21:00–04:00 ET, her akşam 20:00–21:00 arası ara. — https://databento.com/blog/us-equities-overnight-trading ; https://www.nasdaq.com/23-5-trading
- **[R9-11]** (düzeltildi) Blue Ocean ATS'de gece (20:00–04:00) sık işlem gören 393 sembolde hacim ağırlıklı kote spread 28 bps, normal seansta 20 bps. Seyrek işlem görenler dahil geniş örneklemde gece 89 bps'nin üstünde, normal seansta yaklaşık 37 bps. — https://haslam.utk.edu/wp-content/uploads/2024/11/Eaton-Paper.pdf ; https://www.nyse.com/data-insights/night-moves-what-trades-and-when-in--the-overnight-market
- **[R9-12]** (doğrulandı) Kapanış müzayedesinde fiyat etkisi, Nasdaq mikro ölçekli hisseler dışında tüm hisselerde sürekli piyasadakinden düşük; kapanış müzayedeleri günlük hacmin yaklaşık %10'u. — https://jfqa.org/wp-content/uploads/2026/01/25551_Price_Impact.pdf
- **[R9-14]** (doğrulandı) Kapanış fiyatı müzayede öncesi fiyattan ortalama 8,1 bps (mutlak) sapar; sapma küçük hisselerde gece içinde büyük ölçüde, büyük hisselerde tamamen geri döner (Bogousslavsky–Muravyev; arama özeti). — https://aeaweb.org/conference/2021/preliminary/paper/H9T4hef7 ; https://thepluto.substack.com/api/v1/file/06bdf231-3aea-4e3a-8ca1-d5ef6ead54f9.pdf
- **[R9-15]** (doğrulandı) IBKR Pro sabit tarife 0,005 $/hisse, en az 1 $; kademeli tarife 0,0035 $/hisse, en az 0,35 $; işlem başına en çok işlem değerinin %1'i (ön tarama, IBKR sayfası). — https://www.interactivebrokers.com/en/pricing/commissions-stocks.php
- **[R9-24]** (doğrulandı) Kaldıraçlı ETF'de sürdürme teminatı kaldıraçla çarpılır: uzun pozisyonda 3×%25 = %75, açığa satışta 3×%30 = %90 (arama özeti). — https://www.interactivebrokers.com/support/faq/content/margin-requirement-leveraged-etf-products-1163247655
- **[R9-28]** (düzeltildi) AMP'nin güncel teminat sayfasında MES sürdürme teminatı 2.919 $, MNQ ise 4.574 $. İddiadaki 2.863 $ / 4.646 $ eski. CME'nin resmî tablosu 403 verdiği için görülemedi; teminatlar sık değişir, emir öncesinde aracı kurumdan… — https://www.ampfutures.com/trading-info/margins?hsLang=es
- **[R9-29]** (doğrulandı) Rule 201: hisse önceki kapanışa göre %10 düşünce o günün kalanında ve ertesi gün açığa satış yalnız en iyi alış fiyatının üstünden yapılabilir (ön tarama). — https://www.sec.gov/divisions/marketreg/rule201faq.htm
- **[R10-01]** (doğrulandı) Yurt dışı borsalarda yapılan menkul kıymet alım satım kazancı değer artışı kazancıdır ve yıllık gelir vergisi beyannamesiyle beyan edilir. — https://intvrg.gib.gov.tr/hazirbeyan/assets/pdf/DUYURU_UNIVERSAL_2026_Diger_Kazanc_ve_Iratlar_2026.pdf
- **[R10-02]** (doğrulandı) Mükerrer 80'deki 2 yıl istisnası yalnızca tam mükellef kurumların hisselerine uygulanır; ABD hissesi ve ETF'si elde tutma süresinden bağımsız vergilenir. — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-03]** (doğrulandı) Değer artışı istisnası (2026'da 150.000 TL) menkul kıymet ve sermaye piyasası aracı satışından doğan kazanca uygulanmaz. — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-05]** (doğrulanamadı) Alış ve satış bedeli alım ve satım tarihlerindeki kurla TL'ye çevrilir; dolarda zarar olsa bile TL'de kâr çıkarsa vergi doğar. — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-06]** (doğrulanamadı) Aracı kurum komisyonu matrahtan düşülür. Kredili alımda kredi faizi düşülemez. — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-07]** (doğrulandı) Aynı yıl içindeki yurt dışı menkul zararları kazançla netleşir; diğer kazanç ve irat zararları başka gelir unsurlarından düşülemez. — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-09]** (doğrulandı) 2026 tarifesi (ücret dışı): %15 190 bin TL'ye kadar, %20 400 bin'e kadar, %27 1 milyon'a kadar, %35 5,3 milyon'a kadar, %40 üstü (332 No'lu Tebliğ, RG 31/12/2025 sayı 33124 5. mükerrer). — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-11]** (düzeltildi) GVK 92'ye göre beyanname izleyen yılın Mart ayının 1'inden 25'ine kadar verilir. GİB 2025 kazancı için süreyi 1-31 Mart 2026 olarak uyguladı. GVK 117'ye göre vergi Mart ve Temmuz aylarında iki eşit taksitle ödenir. 2026… — https://www.mevzuat.gov.tr/mevzuatmetin/1.4.193.pdf
- **[R10-12]** (doğrulandı) RG 28/3/2025 değişikliğinden sonra yurt dışı menkul kıymet ve türev alım satımı SPK yetkili banka ve aracı kurum üzerinden yapılır. — https://www.mevzuat.gov.tr/MevzuatMetin/yonetmelik/9.5.11990.pdf
- **[R10-13]** (doğrulandı) Kendi inisiyatifinle yurt dışı kuruma gitme istisnası yalnızca türev işlemler içindir; bedel transferi bankadan yapılmak zorundadır. — https://www.mevzuat.gov.tr/MevzuatMetin/yonetmelik/9.5.11990.pdf
- **[R10-14]** (doğrulandı) Kaldıraçlı işlemler ve CFD yalnızca SPK yetkili kurumlardan yapılabilir; bunlar için yurt dışına transfer yasaktır. — https://www.mevzuat.gov.tr/MevzuatMetin/yonetmelik/9.5.11990.pdf
- **[R10-24]** (doğrulandı) TR-ABD anlaşmasıyla bireyin ABD temettü stopajı en çok %20; %10 ve üzeri oy hakkı olan şirket için %15. — https://www.irs.gov/pub/irs-trty/turkey.pdf
- **[R11-01]** (doğrulandı) Fed 16 Eylül 2026'da faizi 25 bp artırıp %3,75–4,00 aralığına getirdi; oy 12–0. — https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- **[R11-04]** (doğrulandı) Sonraki FOMC 8–9 Aralık 2026 ve SEP'li; Ekim tutanakları 18 Kasım'da yayımlandı. — https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- **[R11-06]** (doğrulandı) 21 Kasım'da vadeliler Aralık artırım ihtimalini ~%95 fiyatlıyor; Goldman Aralık ve Mart artırımlarıyla %4,25–4,5 tepe bekliyor. — https://fortune.com/2026/11/21/goldman-sachs-sp-500-correction-ai-unwind-bottom-three-conditions-hedge-funds-positioning/
- **[R11-10]** (doğrulandı) 10 yıllık Hazine faizinin 2026 zirvesi 5 Ekim'de %5,31; 20 Kasım'da %4,92 (19 Kasım'da %5,04); 2 yıllık %4,63. — https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve&field_tdr_date_value=2026&page&_format=csv
- **[R11-12]** (doğrulandı) 20 Kasım: S&P 500 −%3,7 ile 6.910,39, Nasdaq −%5,3 ile 22.617,73, Russell 2000 −%2,8; haftalık S&P −%8,6; S&P 6 Ekim rekorundan %10'dan fazla aşağıda. — https://www.lanacion.com.ar/usa/how-major-us-stock-indexes-fared-friday-11202026-nid20112026/
- **[R11-14]** (düzeltildi) 20 Kasım'da Philadelphia yarı iletken endeksi %10,73 düştü; 30 hissenin hepsi ekside kapandı. MU %13,9, AMD %13,3 düştü. NVDA günü yaklaşık %14,0 kayıpla kapattı (145,98'den 125,53 dolara; gün içi dip yaklaşık %−14,7). Kayıp,… — https://www.tradingkey.com/analysis/stocks/us-stocks/262316111-nasdaq-falls-ai-stock-selloff-nvidia-sec-probe-tradingkey
- **[R11-15]** (doğrulandı) 20 Kasım'da Reuters, SEC icra biriminin Nvidia'da olası muhasebe sorunlarını incelediğini yazdı; WSJ soruşturmayı ilk kez 17 Kasım'da duyurmuştu; bu suçlama anlamına gelmiyor. — https://www.investmentnews.com/equities/embattled-nvidia-faces-sec-probe-as-california-attorney-general-mulls-action/269054
- **[R11-16]** (doğrulandı) 17 Kasım'da WSJ, SEC'in Nvidia açıklamalarının yatırımcıyı yanıltıp yanıltmadığına dair hukuk soruşturması başlattığını yazdı; Kaliforniya başsavcısı da çip saptırma iddiasını inceliyor. — https://www.investmentnews.com/equities/embattled-nvidia-faces-sec-probe-as-california-attorney-general-mulls-action/269054
- **[R11-17]** (doğrulandı) Nvidia 12 Kasım'da Huang'ın CEO, başkan ve yönetim kurulu üyeliğinden hemen istifa ettiğini açıkladı; Kress geçici CEO, Harvey Jones yönetim kurulu başkanı. — https://www.credenceresearch.com/news/nvidia-q3-fiscal-2027-revenue-115-8-billion-vera-rubin-interim-ceo-kress
- **[R11-20]** (doğrulandı) Nvidia 3. çeyrek (çeyrek sonu 25 Ekim) sonuçları 17 Kasım kapanış sonrası açıklandı: gelir 115,8 milyar $, veri merkezi 107,6 milyar $; 4. çeyrek yönlendirmesi 130 milyar $; 2028 mali yılı büyüme hedefi %70'ten ~%75'e çıktı. — https://www.jamessharp.co.uk/market-news/nvidia-announces-financial-results-for-third-quarter-fiscal-2027/
- **[R12-01]** (doğrulandı) FOMC'nin son 2026 toplantısı 8–9 Aralık'ta ve SEP'li (projeksiyonlu); Ekim tutanakları 18 Kasım 2026'da yayımlandı. — https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- **[R12-02]** (doğrulandı) Kasım 2026 istihdam raporu 4 Aralık 08:30'da, Kasım TÜFE 10 Aralık'ta, Kasım ÜFE 15 Aralık'ta, ithalat fiyatları 17 Aralık'ta; 8 Aralık'taki yayın Verimlilik (R). — https://blsmon1.bls.gov/schedule/2026/12_sched_list.htm
- **[R12-04]** (doğrulandı) BEA, Ekim PCE'yi ve 3. çeyrek GSYH ikinci tahminini 25 Kasım'da, Kasım PCE'yi ve GSYH üçüncü tahminini 23 Aralık 2026'da 08:30'da yayımlıyor. — https://www.bea.gov/news/schedule
- **[R12-07]** (doğrulanamadı) ISM imalat 1 Aralık 2026'da (ilk iş günü kuralı), hizmet 3 Aralık'ta; Ocak'ta imalat büyük olasılıkla 4 Ocak'ta, hizmet 5 ya da 6 Ocak'ta (çelişkili, teyitsiz). — https://www.ismworld.org/supply-management-news-and-reports/reports/rob-report-calendar/
- **[R12-08]** (doğrulandı) NYSE 27 Kasım ve 24 Aralık 2026'da 13:00'te erken kapanıyor, 1 Ocak 2027'de kapalı. — https://www.nyse.com/markets/hours-calendars
- **[R12-10]** (doğrulandı) Nasdaq-100 yıllık yeniden yapılandırması üçüncü Cuma'dan sonraki ilk işlem günü açılışta yürürlüğe giriyor; duyuru yürürlükten 6 işlem günü önce kapanış sonrasında. Buna göre referans 30 Kasım, duyuru 11 Aralık, yürürlük 21… — https://indexes.nasdaqomx.com/docs/Methodology_NDX_Effective_May_1_2026.pdf
- **[R12-14]** (doğrulandı) Broadcom 4. çeyrek ve FY2026 sonuçlarını 9 Aralık 2026 Çarşamba kapanış sonrasında açıklayacak (17:00 ET konferans). — https://finviz.com/news/418980/broadcom-inc-to-announce-fourth-quarter-and-fiscal-year-2026-financial-results-on-wednesday-december-9-2026
- **[R12-15]** (doğrulandı) Nasdaq bilanço takvimi (çoğu tahmini): CRWD ve MRVL 1 Ara, CRM ve SNOW 2 Ara, ADBE 9 Ara, COST ve LULU 10 Ara, ORCL 14 Ara, MU 16 Ara, NKE ve ACN 17 Ara, CCL ve PAYX 18 Ara, DELL 24 Kas, JPM 12 Oca, BAC/WFC/C 13 Oca. — https://api.nasdaq.com/api/calendar/earnings?date=2026-12-10
- **[R12-22]** (düzeltildi) Hacimler ve fiyatlar doğru (NVDL 90,9 mn; NVD 63,5 mn; TSLL 46,2 mn; MSTZ 37,3 mn; CONL 28,8 mn ve 1,79 $; PLTD 59,5 mn; AMDL 7,1 mn). Schwab'a göre gider oranları: NVDL %1,05, NVD %1,35, CONL %1,04, AMDL %1,07; TSLL %0,83,… — https://www.schwab.wallst.com/Prospect/Research/etfs/summary.asp?symbol=nvdl

Bu rapordaki backtest sayılarının kaynağı kendi hesaplarımızdır: `ek/veri/` altındaki sonuç tabloları ve `ek/ajanlar/` altındaki ajan özetleri (d4 ve d5 ile başlayan dosyalar).

## 6. Devam notu

- **Bulunan:** ABD'de kapanış sinyali ve 1–3 gün taşımayla, 3.420 önceden yazılı varyant ve 27.351 tarama regresyonu içinde kullanılabilir kural çıkmadı; sonuç 1993–2004 sınavı ve yalnız komisyonlu maliyet senaryosuyla da değişmedi.
- **Ana dosya:** `raporlar/2026-11-21_abd_kapanis_1-3gun/RAPOR.md`. Yöntem ve ön kayıtlar: `ek/YONTEM.md` (Ek 1 ve Ek 2 dahil).
- **Sonuç tabloları:** `ek/veri/sonuc_K*.csv` (aile başına), `ek/veri/ek1_*.csv`, `ek/veri/sonuc_ek2_*.csv`, `ek/veri/risk_ve_boyut_tablosu.csv`, `ek/veri/hipotezler.csv`.
- **Kod:** `ek/kod/motor.py` (testler: `test_motor.py`, `test_denetim.py`), aile betikleri `aile_K*.py`. Veri paneli depoda değil; `ek/kod/BENIOKU.md` içindeki komutlarla yeniden kurulur.
- **Sırada ne olabilir:** 3.12'deki iki hipotezin ileriye dönük izlenmesi; aracı kurum yanıtlarına göre maliyetin netleştirilmesi; aynı motorun "ABD kapanışı → VİOP" yönünde kullanılması.

<!--MALIYET-->
