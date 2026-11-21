# Yöntem ve ön kayıt (hesaplardan ÖNCE yazıldı, 21.11.2026)

Amaç: ABD'de işlem gören sektör, alt sektör ve emtia araçlarında, **ABD kapanışında (16:00 ET) verilen kararla alınıp 1–3 işlem günü taşınan** pozisyonlar için işe yarayan sinyalleri bulmak. Bu belge, sonuçlara bakmadan önce neyin nasıl test edileceğini ve bir sinyalin hangi koşulla "ayakta kaldı" sayılacağını sabitler. Sonradan yapılan her sapma raporda ayrıca yazılır.

## 1. İşlem profili

- Karar anı: t günü 16:00 ET (Türkiye saatiyle yazın 23:00, kışın 00:00). Sinyal, o ana kadar kesinleşmiş bilgiyle hesaplanır.
- Giriş: t günü kapanış fiyatı. Çıkış: t+1, t+2 ya da t+3 kapanışı (h = 1, 2, 3).
- Yön: asıl ilgi AL sinyalleri. SAT sinyalleri de test edilir (ters ETF ya da açığa satışla uygulanabilir) ve ayrı raporlanır.
- Günlük veriyle çalışıldığı için sinyal kapanış fiyatıyla hesaplanıp aynı kapanıştan girildiği varsayılır. Gerçekte sinyal 15:50 dolayında hesaplanır; bu fark sağlamlık testiyle ölçülür (bölüm 7, "ertesi açılış" ve "ertesi kapanış" girişleri).

## 2. Veri

- Kaynak: Yahoo Finance günlük OHLCV, 2000'den bugüne (testler 2005 sonrası). 989 sembolün 979'u indi. Evren: `kod/evren.py`. Yükleyici ve test fonksiyonları: `kod/ortak.py`.
- Getiri: temettü ve bölünmeye göre düzeltilmiş kapanış. Açılış, yüksek ve düşük aynı katsayıyla düzeltilir.
- Takvim: NYSE işlem günleri. Yurt dışı seriler kendi takvimlerinde getiriye çevrilir, sonra NYSE gününe hizalanır (tatil getirileri bir sonraki NYSE gününde birikir).
- **Bilinen kusurlar:**
  1. *Hayatta kalma yanlılığı:* hisse evreni bugün işlem görenlerden oluşuyor (2026'da birleşen ya da borsadan çıkanlar yok). Hisse düzeyindeki AL sinyallerinin ham getirisi yukarı yanlıdır. Bu yüzden her sonuç "sürüklenme düzeltilmiş" olarak da verilir ve hisse sonuçları ETF sonuçlarından ayrı tutulur.
  2. *Yahoo hataları:* tek tük bozuk fiyat olabilir. ETF'lerde |günlük getiri| > %40, hisselerde > %80 olan günler işaretlenir ve sonuç bu günler çıkarılarak da kontrol edilir.
  3. *Tarih hatası (düzeltildi):* Yahoo'nun vadeli ve kur serileri gece yarısı damgalıdır; sabit saat farkıyla çevrilince yaz saatinde bir gün geriye kayıyordu. İndirici artık borsanın saat dilimini kullanıyor.
  4. Sürekli vadeli serilerde (=F) vade geçişi sıçramaları olabilir; emtia için birincil kaynak ETF'tir.

## 3. Zamanlama: 16:00 ET'de ne biliniyor?

| Seri türü | t çubuğu ne zaman kesinleşir | Sinyalde kullanım |
|---|---|---|
| ABD hisse ve ETF | 16:00 ET | t günü, gecikmesiz |
| Asya, Avustralya, Avrupa endeks ve hisseleri | ABD kapanışından saatler önce | t günü, gecikmesiz |
| Brezilya, Meksika, Kanada | ABD ile aynı saatlerde | t günü, gecikmesiz |
| Emtia ve finans vadelileri (=F) | Uzlaşma 13:00–14:30 ET; elektronik seans 17:00 ET | Ampirik sınamada ileri bakış izi yok (vadeli − ETF farkı ETF'in ertesi gece getirisini öngörmüyor: CL, GC, SI, NG, ES, NQ, ZN için \|corr\| < 0,06). t günü kullanılır; **birincil öncü yine ETF'tir** ve vadeli sinyali 1 gün gecikmeyle de raporlanır |
| Tahıl, yumuşak emtia, canlı hayvan vadelileri | 13:00–14:30 ET | t günü, gecikmesiz |
| Kripto spot (BTC-USD…) | 00:00 UTC (ABD kapanışından sonra) | Çubuk **kendinden sonraki ilk NYSE gününe** eşlenir (hafta sonu hareketi pazartesi sinyaline girer); birincil öncü IBIT/BITO/GBTC (16:00 ET) |
| Kur (=X) | Yahoo'nun t çubuğu ABD'nin t−1 gününe denk geliyor (FXE ile corr: t−1 günü 0,93; aynı gün 0,04) | Öncü olarak kullanılmaz; yerine kur ETF'leri (UUP, FXE, FXY, FXA, FXC, FXB) |
| Dolar endeksi (DX-Y.NYB) | ~17:00 ET | 1 gün gecikmeli; birincil UUP |
| VIX ailesi | 16:15 ET | t günü kullanılır, **15 dakikalık ileri bakış riski işaretlenir**; her VIX sinyali 1 gün gecikmeyle de raporlanır |
| ^TNX ve faiz endeksleri | ~15:00 ET | t günü |
| ^MOVE | zamanlaması doğrulanamadı | 1 gün gecikmeli |

Dikkat: bazı emtia ETF'lerinin kapanış fiyatı bayattır (son işlem 16:00'dan önce). CPER, CANE, WEAT'te "vadeli − ETF" farkı ETF'in ertesi gece getirisini öngörüyor (corr 0,31 / 0,24 / 0,17). Bu, işlenebilir bir öncülük değil, **bayat fiyat yanılgısıdır**: kapanışta o fiyattan alınamaz. Bu ETF'lerin hedef olduğu sonuçlar "bayat fiyat şüphesi" ile işaretlenir ve ertesi açılış girişiyle yeniden sınanır.

## 4. Sinyal aileleri

Her ailede sinyal biçimleri sabittir; parametre taraması yapılmaz. Eşikler: \|z\| ≥ 1 (ana), \|z\| ≥ 1,5 (yalnız sağlamlık). z = değer / önceki 60 günün standart sapması (yalnız geçmiş veri).

**Öncü–hedef biçimleri (F1, F2, F3 için ortak).** x = öncünün t günü getirisi (16:00 ET'de bilinen), r = hedefin t günü getirisi:
- **B1 ham öncü:** z(x) ≥ +1 → hipotez yönünde AL; ≤ −1 → SAT.
- **B1r arındırılmış öncü:** B1'in piyasadan arındırılmış hâli: öncü − β·SPY sinyali, hedef − β·SPY ileri getirisiyle test edilir. "Öncüye özgü" etiketi bu teste bağlıdır (bölüm 6).
- **B2 yetişme artığı:** e = r − β·x (β: 250 günlük, 1 gün gecikmeli). z(e) ≤ −1 (hedef öncünün gerisinde kaldı) → AL; ≥ +1 → SAT. Bu biçim çoğunlukla öncüden bağımsız "artık dönüşü"nü ölçer (sentetik sınamada öncüde hiç bilgi yokken t = 8,8 verdi). Bu yüzden kıyası hedefin SPY artığının dönüşüdür ve öncüye özgülük kısmi regresyonla sınanır (bölüm 6).
- **B3 çok günlü öncü:** öncünün 3 günlük toplam getirisinin z'si ≥ +1 → AL; ≤ −1 → SAT.

| Aile | İçerik | Öncüler → hedefler |
|---|---|---|
| **F1 Emtia → hisse** | Emtia fiyatı ilgili sektöre gecikmeyle yansıyor mu | Emtia ETF'leri ve vadelileri (petrol, doğal gaz, rafineri marjı, altın, gümüş, bakır, uranyum, tahıllar, kakao, kahve, kereste…) → ilgili ETF ve hisseler. Çiftler önceden yazılı hipotez listesinden gelir (`ek/hipotez/*.json`) |
| **F2 Hisse/sektör içi öncülük** | Öncü şirket ya da ETF → takipçiler; sektör → sektör; yabancı öncü (erken seans) → ABD | (a) Önceden yazılı hipotez çiftleri. (b) Körlemesine tarama: bütün ABD hisse ve ETF çiftleri; yalnız h = 1; öncü ve hedef SPY'dan arındırılmış, oynaklığa ölçekli, White t; BH (q = %10) IS p değerlerine; **seçim yalnız IS döneminde**, OOS yalnız seçilenlere bakılır |
| **F3 Çapraz varlık** | Faiz, kredi, dolar, volatilite, risk iştahı, yurt dışı seans, kripto → sektörler | TLT/IEF, HYG, LQD, UUP, VIXY, VIX/VIX3M, RSP−SPY, IWM−SPY, SPHB−SPLV, CPER−GLD, ülke ETF'leri, yabancı endeksler, IBIT/BITO → 11 sektör + alt sektör ETF'leri + ilgili hisse grupları |
| **F4 Aracın kendi geçmişi** | Kapanışta hesaplanan dönüş ve momentum kuralları | IBS < 0,2 / > 0,8; RSI(2) < 10 / > 90; 3 gün üst üste düşüş / yükseliş; günlük getiri z ≤ −1,5 / ≥ +1,5; 5 günlük getiri z ≤ −1,5 / ≥ +1,5; kapanış 20 günlük zirvede / dipte. Koşul ayrımları (önceden sabit): 200 günlük ortalamanın üstü/altı; VIX > 20 / ≤ 20. Ayrıca getirinin gece (kapanış→açılış) ve gün içi (açılış→kapanış) ayrışması |
| **F5 Takvim** | Ay dönümü, haftanın günü, tatil öncesi, FOMC öncesi, opsiyon vadesi haftası, çeyrek sonu | Bütün sektör, alt sektör ve emtia ETF'leri |
| **F6 Bilanço olayları** | (a) Bilanço sonrası sürüklenme: tepki günü kapanışında gir. (b) Emsallere yayılım: erken açıklayan şirketin tepkisi → henüz açıklamamış emsaller | ~600 ABD hissesi; tarihler SEC EDGAR 8-K (madde 2.02) kabul zamanından |

## 5. Ölçütler

- Ufuk: h = 1, 2, 3 gün. Örtüşen işlemlerde t istatistiği günlük seri üzerinden düz ağırlıklı HAC (Hansen–Hodrick, gecikme h−1) ile hesaplanır (`ortak.hac_t`).
- Maliyet (gidiş-dönüş): **işlem günündeki** 60 günlük medyan dolar hacmine göre (1 gün gecikmeli): ≥ 100 mn $ → 5 bps; 20–100 mn $ → 10 bps; < 20 mn $ → 20 bps; kaldıraçlı/ters ETF'te taban 10 bps (`ortak.maliyet_serisi`). Aracı kurum komisyonu dahil değildir; raporda komisyon duyarlılığı ayrıca verilir.
- Her sonuç iki biçimde verilir: **net** (ham getiri − maliyet) ve **sürüklenme düzeltilmiş net** (hedefin aynı dönemdeki koşulsuz h günlük ortalaması çıkarılmış). Karar ölçütü ikincisidir: yükselen piyasada her AL sinyali kazanır; önemli olan sinyalin fazladan kattığıdır.
- Dönemler: **IS** = 2005-01-01 … 2018-12-31; **OOS** = 2019-01-01 … 2026-11-20; **SON** = 2024-01-01 … (OOS'un alt kümesi, ayrıca raporlanır). 2015'ten sonra başlayan araçlarda IS/OOS örneklemin ilk %55'i / son %45'i olarak bölünür.

## 6. Çoklu test ve "ayakta kalma" koşulları (sürüm 2: eleştirmen denetiminden sonra sıkılaştırıldı)

Her aile yaptığı toplam test sayısını ve **beklenen yanlış pozitif sayısını** raporlar (test sayısı × sıfır hipotezinde geçme olasılığı: SAĞLAM için 3,9e-5, KOŞULLU için 1,4e-4). Bir sinyal ancak şu koşulların hepsini sağlarsa **SAĞLAM** sayılır:

| # | Koşul |
|---|---|
| A | **IS** döneminde sürüklenme düzeltilmiş t ≥ 2,5 (seçim yalnız IS'te yapılır) |
| B | **OOS**'ta aynı işaret ve sürüklenme düzeltilmiş t ≥ 2,5; ayrıca aile içinde, IS'ten seçilenlerin OOS p değerlerine Benjamini–Hochberg (q = %10) |
| C | SON dönemde (2024–26) net ortalama > 0 |
| D | Sürüklenme düzeltilmiş net ortalama ≥ 10 bps/işlem. SAT bacağında ayrıca ham net ortalama ≥ 0 (düşen piyasada "anormal" kazanç cebe girmez) |
| E | En iyi 10 işlem çıkarılınca net ortalama > 0 ve t ≥ 1,5 |
| F | İşlem olan yılların en az %60'ında net ortalama > 0 |
| G | Toplam n ≥ 100 ve OOS n ≥ 40 |
| H | Dairesel plasebo: sinyal rastgele (≥ 60 gün) kaydırılarak 1.000 kez yeniden test edilir; gerçek sinyal bu dağılımın üst %2,5'inde olmalı. Takvim sinyallerinde ek olarak 1–4 gün kaydırma |
| I | Ertesi açılıştan girişte etkinin işareti değişmiyor. Bayat fiyat işaretli ya da 20 bps sınıfındaki hedefte ertesi açılış girişinin **neti** > 0 olmalı |

Sınıflar: **SAĞLAM** (hepsi) · **KOŞULLU** (A; B'de OOS t ≥ 2,0; C–I'dan en çok biri eksik) · **İZLE** (IS t ≥ 2,0 ve OOS t ≥ 1,5, aynı işaret; kanıt yetersiz ama ilginç) · **ELENDİ**.

Ek kurallar:
- **Yön:** her hipotez yalnız önceden yazılı yönünde sınıf alır; ters yön raporlanır ama sınıflandırılmaz.
- **Öncüye özgü mü?** Bir öncü–hedef sinyali ancak piyasadan arındırılmış testte de (öncü − β·SPY → hedef − β·SPY) IS ve OOS'ta t ≥ 2,0 veriyorsa "öncüye özgü" etiketi alır. Vermiyorsa "piyasa dönüşü" (piyasanın kendi günlük dönüşünün kopyası) diye etiketlenir ve lead-lag sayılmaz.
- **B2 (yetişme artığı):** kıyas, hedefin SPY artığının dönüşüdür. B2 ancak öncü artığının katsayısı, SPY artığı ve hedefin kendi getirisi kontrol edilince de anlamlıysa (kısmi t ≥ 2,5) "öncüye özgü" sayılır; değilse "artık dönüşü"dür ve hedef başına tek sinyal olarak sayılır.
- **Hisse düzeyi AL-dönüş sinyalleri** (düşeni al türü; F4, B2, F6) hayatta kalma yanlılığı nedeniyle en çok KOŞULLU olabilir.
- **Kaldıraçlı/ters ETF'ler ve ikizler** (aynı gün korelasyonu > 0,95) ayrı keşif sayılmaz; kaldıraçlı ürün uygulama aracıdır.
- **Çok hedefli testlerde** (hisse grupları, bilanço olayları) t, sinyal günü başına eşit ağırlıklı portföy serisinden hesaplanır (`ortak.havuz_testi`).
- F4 kurallarının bir kısmına 1. dalga ajanları tüm örneklemde ön bakış yaptı; F4'ün OOS'u bu yüzden "bakılmış" sayılır ve yorumda dikkate alınır.

İlk elemeden geçen SAĞLAM ve KOŞULLU sinyaller, ayrı bir ajan tarafından **ortak kütüphane kullanılmadan sıfırdan yeniden üretilir** ve bir başka ajan tarafından çürütülmeye çalışılır (bölüm 7). Geçemeyen sinyal raporda "kullanılamaz" diye yazılır.

## 7. Sağlamlık ve çürütme testleri

1. Giriş gecikmesi: ertesi açılış; ertesi kapanış (1 gün geç).
2. Eşik: \|z\| ≥ 1,5; maliyet iki katı.
3. Yıl yıl tablo; en iyi 10 işlem hariç; en iyi yıl hariç.
4. Piyasa etkisinden arındırma: hedef − β·SPY (ya da sektör ETF'i) üzerinden aynı test. Sinyal yalnız piyasa yönünü mü yakalıyor?
5. Kıyas: aynı hedefte "her gün al" ve "rastgele aynı sayıda gün" (1.000 tekrar) dağılımı.
6. Rejim ayrımı: VIX > 20 / ≤ 20; hedef 200 günlük ortalamasının üstünde / altında.
7. Bayat fiyat ve ileri bakış denetimi: öncü 1 gün geciktirilince etki tümüyle kayboluyor mu (beklenen) yoksa aynı mı kalıyor (şüpheli: sinyal aslında başka bir şeyi ölçüyor)?
8. Veri hatası denetimi: en büyük 20 işlem tek tek kontrol edilir (bölünme, bozuk fiyat).
9. Sınır sinyalleri hariç (|z| 1,0–1,2; IBS 0,15–0,25): kapanışa 10 dakika kala hesaplanan sinyal kapanışta değişmiş olabilir; etki sınırdaki sinyaller çıkarılınca da sürmeli.
10. Son 60 günün 5 dakikalık verisiyle 15:50 ve 16:00 sinyallerinin örtüşme oranı.
11. Kriz dönemleri hariç (2008-09 … 2009-06 ve 2020-02 … 2020-04).
12. B2 için ilgisiz öncü plasebosu: aynı test ilgisiz bir öncüyle (ör. tahvil ETF'i) de aynı sonucu veriyorsa etki öncüye özgü değildir.

## 8. Ajan çıktı standardı (backtest aileleri)

Her kod ajanı şunları üretir:
- `kod/<aile>.py`: tek betik, baştan sona yeniden çalıştırılabilir; `kod/ortak.py` fonksiyonlarını kullanır.
- `ek/backtest/<aile>/sonuclar.csv`: test başına bir satır. Zorunlu sütunlar: `aile, sinyal_id, oncu, hedef, bicim, yon, h, havuz (tek hedef / portföy), bayat_isaret` + `ortak.donemli_test` (ya da `havuz_donemli`) çıktısındaki bütün sütunlar + `son_gun, son_sinyal` (son işlem gününde sinyal açık mı).
- `ek/backtest/<aile>/ayakta_kalanlar.csv`: bölüm 6 koşullarının her biri için geçti/kaldı sütunu ve sınıf.
- `ek/backtest/<aile>/NOT.md`: en çok 600 kelime; kaç test yapıldı, kaçı hangi aşamada elendi, şaşırtıcı bulgular, veri sorunları.

## 9. Dürüstlük notları

- Kısa vadeli öngörülebilirlik küçüktür. Beklenen büyüklük işlem başına 10–50 bps; daha büyüğü görülürse önce hata aranır.
- Geçmişte çalışmış olmak gelecekte çalışacağını göstermez; yayımlanan etkiler zayıflar. SON dönem bu yüzden ayrı raporlanır.
- Bu çalışma yatırım tavsiyesi değildir.

## 10. Eleştirmen denetimi (hesaplardan önce, 21.11.2026) ve yapılan değişiklikler

Bağımsız bir eleştirmen (Fable) bu belgeyi ve `kod/ortak.py`'yi sentetik ve gerçek veriyle sınadı (`kod/yontem_sinamasi.py`, çıktılar `ek/dogrulama/`). Sonuç: kütüphanede ileri bakış yok (zskor, kayan_beta, ileri_getiri temiz; sentetik 1 günlük öncülük doğru gecikmede bulundu, ters gecikmede bulunmadı). Ama ilk sürümdeki eşikler ve kıyaslar yanlış pozitif üretirdi. Kabul edilen değişiklikler:

| # | Sorun | Değişiklik |
|---|---|---|
| 1 | Tarama t'si ham getiride medyan 1,8 kat şişik; piyasanın günlük dönüşünü defalarca "öncülük" diye buluyor (20 ETF'te çiftlerin %49'u t ≤ −2; SPY'dan arındırınca %7) | Tarama: yalnız h = 1, z-skorlu ve SPY'dan arındırılmış öncü, oynaklığa ölçekli arındırılmış hedef, White t |
| 2 | Eski A∧B eşikleri 100 bin testte ~66 sahte SAĞLAM üretirdi | A = IS t ≥ 2,5; B = OOS t ≥ 2,5 + OOS üzerinde BH; beklenen yanlış pozitif satırı zorunlu |
| 3 | B2 kıyası yetersiz (öncüde bilgi yokken t = 8,8) | Kıyas SPY artığı dönüşü; öncüye özgülük kısmi regresyonla |
| 4 | Çok hedefli testte düz havuz t'si 5 kata kadar şişer | `havuz_testi`: gün bazlı eşit ağırlıklı portföy serisi |
| 5 | Newey–West(h−1) kalıcı sinyalde h = 2–3'te %10–13 şişik | Düz ağırlıklı HAC (`hac_t`) |
| 6 | Sabit kaydırmalı plasebo takvim sinyalinde aynı güne düşüyor | Dairesel rastgele plasebo (1.000 tekrar) |
| 7 | %55/%45 bölünme kütüphanede yoktu | `donem_sinirlari` |
| 8 | Maliyet sınıfı bugünkü hacimden seçiliyordu (2012'de sembollerin %44'ü daha pahalı sınıftaydı) | `maliyet_serisi`: işlem günündeki likidite |
| 9 | SAT bacağında sürüklenme düzeltilmiş ölçü cebe girenden fazla gösteriyor | D koşuluna "ham net ≥ 0" |
| 10 | Kripto spot gecikmesinde hafta sonu hareketi salıya düşüyordu | Sonraki ilk NYSE gününe eşleme |
| 11 | `hizali_getiri` 2005 öncesi getirileri ilk güne yığıyordu (eleştirmen düzeltti) | Tam NYSE takvimiyle eşleme |
| 12 | Koşullu hayatta kalma yanlılığı ("düşeni al" sinyalinde batan hisseler evrende yok) | Hisse düzeyi AL-dönüş en çok KOŞULLU |

Kabul edilmeyen ya da ertelenen: kullanıcının aracı kurum komisyonu bilinmiyor (raporda duyarlılık tablosu verilecek). `kod/yontem_sinamasi.py` içindeki eski `tarama` sınamaları (G3–G4, S6) artık yeni arayüzle çalışmaz; sonuçları `ek/dogrulama/yontem_sinamasi.csv` dosyasında kayıtlıdır.
