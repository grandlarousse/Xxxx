# M1: Midas üzerinden altın ETF'leri trade etmenin pratik koşulları (7 Kasım 2026 itibarıyla)

Kapsam: Türkiye'de yerleşik, tam mükellef bireysel yatırımcı. Altın 1, 3 ve 5 günlük ufukta, kapanıştan kapanışa trade ediliyor. Karşılaştırılan üç kanal: VİOP Ons Altın (F_XAUUSD), Midas üzerinden ABD ETF'leri, BIST altın/gümüş BYF'leri.

Yöntem: Midas'ın kendi sayfaları (ücretler, destek SSS, Genel Çerçeve Sözleşmesi PDF'i), ihraççı sayfaları (SSGA, iShares, VanEck, ProShares, Sprott SEC dosyası), IRS, SPK rehberi, fon şirketi sayfaları, KAP. Bulunamayan her şey "bulunamadı" diye işaretlendi. Kur dönüşümleri 6.11.2026 Midas sayfasındaki 50,16 TL/USD ile yapıldı.

---

## 0. En önemli bulgular

1. **Midas'ta VİOP var, ama Ons Altın (F_XAUUSD) yok.** Midas'ın VİOP'ta sunduğu dayanaklar pay, endeks, USD/TRY, EUR/TRY ve XAU/TRY. Sayfanın ifadesi: "Diğer emtia ve döviz dayanaklı sözleşmeler ile opsiyon ürünleri şu anda Midas'ta sunulmamaktadır." F_XAUUSD için başka bir aracı kurum gerekiyor. [Midas VİOP SSS](https://www.getmidas.com/destek/borsa-istanbul/viop/viopta-islem-goren-kontratlar-nelerdir)
2. **ABD ETF komisyonu emir başına sabit 1,5 USD.** Tutar fark etmiyor. Gidiş-dönüş 3 USD. Bu 1.000 USD'lik işlemde %0,30, 10.000 USD'lik işlemde %0,03 ediyor. [Midas Ücretler](https://www.getmidas.com/ucretler/), [Genel Çerçeve Sözleşmesi Ek-5](https://webcdn.getmidas.com/uploads/2025/12/04155923/genel-cerceve-sozlesme.pdf)
3. **TL↔USD kur makası Midas'ta hiçbir yerde yayımlanmıyor.** Ücret sayfasında, sözleşme tarifesinde ve SSS'de yok. Bulunamadı. Bu yüzden TL'den USD'ye çevirip geri dönen bir 1.000 USD'lik işlemin toplam maliyeti, varsayılan makasa göre %0,49 ile %1,31 arasında değişiyor (bkz. §3). Bakiyeyi USD'de tutan biri için bu kalem sıfır.
4. **ABD hesabı nakit hesap.** Midas'ta ABD için kredili işlem veya açığa satış olduğuna dair hiçbir bilgi bulunamadı. Sözleşme md. 5.2'ye göre emirler hesaptaki nakitle sınırlı. Kısa pozisyon pratikte iki yolla alınabiliyor: ters ETF (GLL, DUST, JDST, ZSL) ya da ABD opsiyonlarında put alımı. Opsiyon komisyonu kontrat başına 1,5 USD.
5. **İşlem saatleri hafta içi 24 saat.** Kış saatinde (ABD'de 1.11.2026'dan itibaren) TSİ ile: gece 04:00–12:00, açılış öncesi 12:00–17:30, normal seans 17:30–00:00, kapanış sonrası 00:00–04:00. Gece seansında yalnızca limit emir verilebiliyor. MOC (kapanışta piyasa emri) veya kapanış müzayedesi emri **bulunamadı**. Emir tipleri piyasa, limit, stop, stop-limit ve kâr al/zarar durdur ile sınırlı. [Midas saatler](https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/hangi-saatler-arasinda-emir-verebilirim), [emir tipleri](https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/midasta-hangi-emir-tiplerini-kullanabilirim), [gece emri](https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-emir-turunu-kullanabilirim)
6. **Saklama yapısı:** ABD'deki aracı Alpaca Securities LLC, takas ve saklama DTCC'de. Koruma, standart SIPC (500 bin USD, bunun en fazla 250 bini nakit) artı Alpaca'nın Lloyd's'tan aldığı ek SIPC poliçesi (müşteri başına 75 milyon USD menkul kıymet ve 75 milyon USD nakit, toplam tavan 250 milyon USD). BIST tarafında Yatırımcı Tazmin Merkezi (YTM) var. 2026 azami tazmin tutarı 2.065.145 TL. [Midas yasal sorumluluklar](https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-sirketi-hakkinda-genel-bilgiler/midasi-guvenilir-kilan-yasal-sorumluluklari-neler), [Alpaca SIPC PDF](https://files.alpaca.markets/disclosures/library/SIPC%20and%20Excess%20SIPC%20Protection.pdf)
7. **Vergi farkı büyük.** ABD ETF alım-satım kazancı değer artış kazancı (GVK mük. 80) sayılıyor. İstisna ya da beyan sınırı yok. 2026 ücret dışı tarifesiyle %15–%40 arasında beyan ediliyor ve kur farkı da matraha giriyor. BIST altın BYF'lerinde 9.7.2025'ten sonra alınan paylarda %17,5 stopaj var. VİOP'ta (pay ve endeks dışı sözleşmeler) %10 stopaj var.
8. **ABD temettü stopajı Türkiye için %20, %15 değil.** IRS Tablo 1'e göre Türkiye'de yerleşik birine ABD şirketlerinin ödediği genel temettülerde oran %20. %15 yalnızca doğrudan iştirak (≥%10 pay) için geçerli. RIC (ETF) temettüleri de %20 sütununda. Midas'ın destek sayfasındaki %15 örneği bu yüzden yanıltıcı olabilir. GLD, IAU, GLDM gibi fiziki altın trust'ları zaten temettü dağıtmıyor. [IRS Tablo 1](https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf)
9. **ABD veraset vergisi riski gerçek.** ABD'li olmayan ve ABD'de yerleşik olmayan birinin ABD-situs varlıkları 60.000 USD'yi aşarsa Form 706-NA verilmesi gerekiyor. Türkiye, ABD'nin veraset ve hibe anlaşması yaptığı 15 ülke arasında yok. GLD'nin kendi 10-K'sı payların "ABD'de bulunuyor sayılması kuvvetle muhtemel" (*may well be considered to be situated in the U.S.*) diyor. Oran %40'a kadar çıkıyor. [IRS 706-NA](https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns), [IRS anlaşma listesi](https://www.irs.gov/businesses/small-businesses-self-employed/estate-gift-tax-treaties-international), [GLD 10-K 2024](https://www.sec.gov/Archives/edgar/data/1222333/000143774924036161/gld20240930_10k.htm)
10. **Darphane Altın Sertifikası (ALTINS1) gram altının yaklaşık %9 üstünde işlem görüyor.** 6.11.2026'da ALTINS1 71,45 TL'ydi (1 sertifika = 0,01 g), yani gram başına 7.145 TL. Aynı gün Midas'taki gram altın 6.555 TL'ydi. 1–5 günlük altın takibi için prim oynaklığı ek risk yaratıyor.

---

## 1. Midas'ta ABD tarafındaki ürün evreni

### 1.1 Midas'ın genel ifadesi
- Midas'ın destek sayfasına göre NASDAQ ve NYSE hisseleri, popüler OTC hisseleri ve yabancı ETF'ler işlem görüyor. ETF'ler uygulamadaki "Keşfet" sekmesinden aranıyor. [Midas: hangi yatırımlar](https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-ile-neler-yapabilirim/midas-yatirim-hesabin-ile-hangi-yatirimlari-yapabilirsin)
- Gece seansında "yaklaşık 2.000 farklı hisse ve yatırım fonu" işlem görüyor. Listeye uygulamada Keşfet > Tarayıcı > Amerikan Borsası > 24 Saat İşlem yolundan ulaşılıyor. GLD'nin bu listede olup olmadığı **bulunamadı**. [Gece piyasası hisseleri](https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-hisselerde-islem-yapabilirim)
- **Ticker bazında doğrulama yapılamadı.** Midas'ın sitesinde ETF'lere ait sayfa yok. ABD sitemap'inde 1.691 ABD hissesi var, ama SPY, QQQ, GLD, IAU, GDX, NUGT, SLV hiçbiri listede değil ve hepsi 404 dönüyor. Yani Midas'ın sitesi ETF'leri listelemiyor. Bu, ETF'lerin alınamadığı anlamına gelmez, çünkü Midas yabancı ETF'lerin alınabildiğini açıkça yazıyor. Ancak tek tek tickerlar (özellikle kaldıraçlı, ters ve ETN'ler) için uygulama içinden teyit gerekiyor.

### 1.2 Altın, gümüş ve madenci ETF'leri: ihraççı verileri

| Ticker | Tür / ihraççı | Yıllık gider | 30 günlük medyan alış-satış farkı | Büyüklük | Not | Kaynak |
|---|---|---|---|---|---|---|
| GLD | Fiziki altın grantor trust, SSGA | %0,40 | %0,01 | 135,5 milyar USD (6.11.2026) | NAV 371,11, kapanış 372,52 USD (6.11.2026). Saklamacı HSBC ve JPMorgan. 2025'te 78 gün primde, 170 gün iskontoda işlem gördü | [SSGA GLD](https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld) |
| IAU | Fiziki altın trust, iShares | %0,25 | %0,01 | 60,0 milyar USD | 30 günlük ortalama hacim 4,59 milyon pay (≈350 milyon USD/gün). 6.11.2026'da prim %0,37 | [iShares IAU](https://www.ishares.com/us/products/239561/ishares-gold-trust-fund) |
| GLDM | Fiziki altın, SSGA | %0,10 | %0,01 | 30,8 milyar USD | Önceki gün birincil borsa hacmi 948.869 pay | [SSGA GLDM](https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-minishares-trust-gldm) |
| SGOL / AAAU / BAR | Fiziki altın (abrdn / Goldman Sachs / GraniteShares) | %0,17 / %0,18 / %0,1749 | bulunamadı | — | Yalnızca ikincil kaynak, ihraççıdan doğrulanmadı | [etfcentral karşılaştırma](https://www.etfcentral.com/compare-etfs/SGOL-vs-AAAU) |
| PHYS | Sprott Fiziki Altın Trust, Ontario (Kanada) kapalı uçlu trust | Yönetim ücreti %0,35 | — | — | 2026 ilk yarısında NYSE Arca'da NAV'a göre ortalama **%2,5 iskonto** (2025'in aynı döneminde %1,7) | [Sprott SEC 6-K](https://www.sec.gov/Archives/edgar/data/0001477049/000199937126017864/ex99-1.htm) |
| CEF | Sprott Fiziki Altın ve Gümüş Trust | bulunamadı | bulunamadı | — | — | — |
| SLV | Fiziki gümüş trust, iShares | %0,50 | %0,02 | 26,3 milyar USD | 30 günlük ortalama hacim 18,9 milyon pay (≈885 milyon USD/gün) | [iShares SLV](https://www.ishares.com/us/products/239855/ishares-silver-trust-fund) |
| GDX | Madenciler, VanEck | %0,51 (ikincil kaynak) | bulunamadı | 26,9 milyar USD (6.11.2026) | NAV 87,37 USD | [VanEck GDX](https://www.vaneck.com/us/en/investments/gold-miners-etf-gdx/overview/) |
| GDXJ | Küçük madenciler, VanEck | %0,52 | bulunamadı | 7,9 milyar USD | NAV 107,36 USD | [VanEck GDXJ](https://www.vaneck.com/us/en/investments/junior-gold-miners-etf-gdxj/overview/) |
| RING, SIL | Madenciler (iShares, Global X) | bulunamadı | bulunamadı | — | — | — |
| UGL | 2x altın, ProShares (vadeli ve swap; **commodity pool, K-1 düzenliyor**) | %0,95 | %0,02 | 668 milyon USD | NAV 43,21 USD (6.11.2026). Gold'a doğrudan yatırım yapmıyor | [ProShares UGL](https://www.proshares.com/our-etfs/leveraged-and-inverse/ugl) |
| AGQ / GLL / ZSL | 2x gümüş / −2x altın / −2x gümüş, ProShares Trust II (K-1) | bulunamadı | bulunamadı | — | ProShares'in 26.02.2026 tarihli 1446(f) "qualified notice" bildirimi UGL ve AGQ için %10 istisnasının geçerli olduğunu söylüyor | [ProShares qualified notice 26.02.2026](https://www.proshares.com/globalassets/proshares/documents/qualified-reports/pst_ii_qualified_notice_02262026.pdf) |
| NUGT / DUST | 2x / −2x madenciler, Direxion | NUGT için kaynaklar %0,87 ile %1,13 arasında çelişiyor; DUST bulunamadı | bulunamadı | — | Direxion sayfaları erişime kapalı (403) | — |
| JNUG / JDST | 2x / −2x küçük madenciler, Direxion | %1,03 / %0,92 (31.10.2026, arama özetinden) | bulunamadı | — | — | [Direxion JNUG/JDST](https://www.direxion.com/product/daily-junior-gold-miners-bull-bear-2x-etfs) |
| GDXU | 3x madenciler **ETN**, BMO MicroSectors | %0,95 | bulunamadı | — | ETN olduğu için ihraççı kredi riski taşıyor | [etfdb GDXU](https://www.etfdb.com/etf/GDXU) |
| DZZ | −2x altın **ETN**, Deutsche Bank | — | — | ≈0,9–3 milyon USD | Varlığı ve hacmi yok denecek kadar az. Pratikte trade edilemez | [etfdb DZZ](https://etfdb.com/advisor_reports/DZZ/) |
| USLV | 3x gümüş ETN, Credit Suisse | — | — | — | **Yok.** Temmuz 2020'de borsadan çıkarıldı, Kasım 2023'te ihraççı opsiyonuyla erken itfa edildi | [Credit Suisse 2020](https://www.credit-suisse.com/articles/media-releases/2020/06/en/credit-suisse-ag-announces-its-intent-to-delist-and-suspend-further-issuances-of-its-velocitysharestm-etns.html), [2023](https://credit-suisse.com/articles/media-releases/2023/10/en/credit-suisse-announces-the-acceleration-at-its-option-of-its-previously-delisted-velocityshares-etns.html) |

Önemli ayrıntılar:
- **NAV ile fiyat aynı anı göstermiyor.** IAU'nun NAV'ı LBMA Gold Price'a göre hesaplanıyor. Borsa kapanışı ise 16:00 ET. 6.11.2026'daki %0,37'lik IAU primi büyük ölçüde fiyatlama sonrasındaki altın hareketinden geliyor. Kapanıştan kapanışa getiri serisi kurarken NAV değil, borsa kapanış fiyatı kullanılmalı.
- **K-1 düzenleyen ProShares fonları (UGL, AGQ, GLL, ZSL) ABD'de ortaklık (PTP) sayılıyor.** ABD dışı satıcılarda 1446(f) uyarınca brüt satış tutarının %10'u kesilebiliyor. ProShares 26.02.2026 bildirimiyle %10 istisnasının geçerli olduğunu duyurdu ve bunu yaklaşık 92 günde bir yeniliyor. Alpaca'nın ABD dışı hesaplarda PTP kısıtı olup olmadığı **bulunamadı**. K-1'in Türkiye beyanına etkisi de **bulunamadı**.
- **Avrupa tarafı:** Midas'ta Xetra (Almanya) ve Euronext Amsterdam var. Komisyon 1,5 EUR, işlem saatleri 10:00–18:30 TSİ, takas T+2. Ancak ETF ve ETC işlemine dair bir ifade **bulunamadı**. Yani 4GLD (Xetra-Gold) ya da Xetra'daki UCITS altın ürünlerinin Midas'ta alınabildiği doğrulanamadı. SGLN ve PHAU'nun ana kotasyonu Londra'da (LSE), Midas'ta LSE yok. [Midas Avrupa](https://www.getmidas.com/avrupa-borsalari/)

---

## 2. Kaldıraç, kısa pozisyon ve uygunluk testi

- **Uygunluk testi:** SPK Rehberi'ne göre (i-SPK.37.8, 10.03.2026) testten muaf olanlar yalnızca TEFAS fonları, para piyasası ve kısa vadeli borçlanma fonları ve Hazine borçlanma araçları. "Bunlar dışında kalan tüm sermaye piyasası araçları için, müşteri kendi talep etse de uygunluk testi yapılması gerekir." Test sonucunda ürün uygun çıkmazsa kurum müşteriyi yazılı veya elektronik olarak uyarıyor. Müşteri yine de isterse, hizmeti verip vermemek kurumun takdirinde. Midas'ın sözleşmesi de (md. 4/7-8) aynı düzeni kuruyor. [SPK Rehber PDF](https://spk.gov.tr/data/61e496a11b41c60d1404d6b2/Yat%C4%B1r%C4%B1m%20Hizmetleri%20ve%20Kurulu%C5%9Flar%C4%B1%20Rehberi%20(i-SPK.37.8)%2010%2003%202026.pdf)
- **Yurt dışı kaldıraçlı veya ters ETF'lere özgü bir SPK yasağı ya da ek test hükmü bulunamadı.** Rehberdeki "kaldıraçlı işlem" hükümleri forex ve CFD (teminatlı kaldıraçlı alım satım) içindir. Sözleşmedeki "İşlem Aracılığı" tanımı yurt dışına emir iletimini "kaldıraçlı işlemler hariç" tutuyor. Bu ifade forex ve CFD'yi kapsıyor. Borsada işlem gören kaldıraçlı ETF payını kapsayıp kapsamadığı **bulunamadı**.
- **Midas'ın kaldıraçlı ETF'leri listeleyip listelemediği bulunamadı.** Midas Akademi sayfası kaldıraçlı ve ters ETF'leri tanıtıyor ve SQQQ'yu örnek veriyor, ama Midas'ta işlem görüp görmediklerini söylemiyor. [Midas Akademi ETF](https://www.getmidas.com/midas-akademi/etf-nedir-nasil-alinir/)
- **ABD'de kredili işlem veya açığa satış: bulunamadı.** Kredili işlem yalnızca BIST için tanımlı. 2026 faiz oranları: 250 bin TL'ye kadar yıllık %66,5, 4 milyon TL üstü %48,5. ABD hesabında piyasa emirlerinde %3, stop emirlerinde %2,5 "marj" bloke ediliyor. Bu kredi değil, eksi bakiyeye düşmeyi önleyen bir tampon. [Midas marj kuralı](https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/amerikan-borsasi-piyasa-emirlerindeki-marj-kurali-nedir)
- **Kısa yön için pratik seçenekler:** GLL (−2x altın), DUST ve JDST (−2x madenciler), ZSL (−2x gümüş) ya da GLD veya GDX put opsiyonu alımı. Opsiyon komisyonu kontrat başına 1,5 USD (aylık 0–500 kontrat). Opsiyon yazma (satma) izni **bulunamadı**. [Midas ücretler](https://www.getmidas.com/ucretler/)
- **Kaldıraçlı ETF'lerde günlük yeniden dengeleme:** 1 günlük ufukta hedef çarpana çok yakın sonuç veriyor. 3–5 günlük ufukta oynaklık kayması (volatility decay) devreye giriyor. Bu bir mekanizma bilgisi. Bu raporda sayısal ölçüm yapılmadı.

---

## 3. Ücretler ve gidiş-dönüş maliyeti

### 3.1 Tarife (Midas'ın kendi sayfaları; yürürlük tarihi verilmiyor)
| Kalem | Midas | Kaynak |
|---|---|---|
| ABD hisse ve ETF komisyonu | Emir başına 1,5 USD. Fiyatı 1 USD altındaki paylarda, 300 adet üstündeki her pay için +0,005 USD | [Ücretler](https://www.getmidas.com/ucretler/), [Sözleşme Ek-5](https://webcdn.getmidas.com/uploads/2025/12/04155923/genel-cerceve-sozlesme.pdf) |
| Asgari ve azami komisyon | Yok ("alt/üst limit yok") | [ABD borsaları](https://www.getmidas.com/abd-borsalari/) |
| ABD opsiyon | Kontrat başına 1,5 USD (aylık 0–500 kontrat). 500 üstünde 0,25 veya 0,50 USD | [Ücretler](https://www.getmidas.com/ucretler/) |
| Avrupa (Xetra, Euronext Amsterdam) | Emir başına 1,5 EUR | [Ücretler](https://www.getmidas.com/ucretler/) |
| BIST pay komisyonu | "Ücretsiz". Sözleşme tavanı binde 2. BYF'lerin bu ücretsiz kapsama girip girmediği açıkça yazılmamış | [Ücretler](https://www.getmidas.com/ucretler/) |
| VİOP | Aylık hacme göre %0,05 (0–10 milyon TL), %0,02 (10–100 milyon TL), %0,01 (100 milyon TL üstü). İlk ay ücretsiz. Tarife BSMV hariç | [Ücretler](https://www.getmidas.com/ucretler/), [VİOP](https://www.getmidas.com/viop/) |
| Canlı veri (BIST, ABD, Avrupa) | Ücretsiz | [Ücretler](https://www.getmidas.com/ucretler/) |
| Hesap işletim ve saklama | Ücretsiz. ADR'lerde pay başına 0,01–0,03 USD periyodik ücret var | [Ücretler](https://www.getmidas.com/ucretler/) |
| Para yatırma | Midas ücret almıyor. SWIFT ve muhabir banka kesintileri müşteriye ait | [Para yatırma](https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/para-aktarma-islemi/para-yatirma-ucreti-var-mi) |
| Hisse transferi (dışarı) | Ücret sayfasında ACATS için 25 USD, DTC için hisse başına 5 USD. **Çelişki:** Sözleşme md. 5.3 yurt dışı çözüm ortağındaki varlıkların başka bir aracı kuruma "transfer edilemez (ACAT OUT)" diyor | [Ücretler](https://www.getmidas.com/ucretler/), [Sözleşme](https://webcdn.getmidas.com/uploads/2025/12/04155923/genel-cerceve-sozlesme.pdf) |
| TL↔USD dönüşüm makası | **Bulunamadı.** Döviz al-sat 7/24 açık ve çevrilen tutarla anında emir verilebiliyor. Kurların uygulamada farklı olabileceği belirtiliyor | [Döviz saatleri](https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/doviz-al-sat/hangi-saatler-arasinda-doviz-al-sat-yapabilirim), [Canlı dolar](https://www.getmidas.com/canli-doviz/dolar-fiyat/) |
| "Midas Plus" | **Bulunamadı.** Mevcut ücretli paket Midas Pro: BIST veya VİOP için ayda 1.200 TL, ikisi birlikte 2.200 TL. 10 kademe derinlik ve AKD veriyor. ABD tarafı için ücretli paket bulunamadı | [Midas Pro](https://www.getmidas.com/midas-pro/) |
| USD nakit neması | Midas, karşı taraftan aldığı oran ile müşteriye verdiği oran arasındaki farkın en fazla %25'ini hizmet komisyonu olarak alabiliyor | [Sözleşme Ek-5](https://webcdn.getmidas.com/uploads/2025/12/04155923/genel-cerceve-sozlesme.pdf) |

### 3.2 Gidiş-dönüş maliyet hesabı (GLD, IAU, GLDM; alış-satış farkı %0,01)
Varsayımlar: Komisyon 2 × 1,5 USD. ETF alış-satış farkının yarısı girişte, yarısı çıkışta ödeniyor, toplam = 1 × spread. Kur makası bilinmediği için üç senaryo kullanıldı. %0,18, 7.11.2026'daki serbest piyasa gösterge makası ([Mynet](https://finans.mynet.com/haber/detay/doviz/7-kasim-2026-dolar-bugun-kac-tl-serbest-piyasa-dolar-kuru/583283/): alış 49,9589, satış 50,0489 TL). %0,50 ve %1,00 stres senaryoları. TL→USD→TL'de makasın tamamı bir kez ödeniyor. Elde tutma gideri (GLD için %0,40/yıl) 5 günde ≈ %0,005. İhmal edilebilir.

| Tutar | Komisyon | ETF spreadi | Kur yok (USD bakiye) | Kur makası %0,18 | %0,50 | %1,00 |
|---|---|---|---|---|---|---|
| 1.000 USD | 3,00 USD | 0,10 USD | **3,10 USD (%0,31)** | 4,90 USD (%0,49) | 8,10 USD (%0,81) | 13,10 USD (%1,31) |
| 10.000 USD | 3,00 USD | 1,00 USD | **4,00 USD (%0,04)** | 22,00 USD (%0,22) | 54,00 USD (%0,54) | 104,00 USD (%1,04) |

UGL ve SLV için spread %0,02. Tutar 1.000 USD'de 3,20 USD (%0,32), 10.000 USD'de 5,00 USD (%0,05) oluyor (kur hariç). Kaldıraçlı ürünlerde aynı dolar maliyet 2 kat altın pozisyonu alıyor.

**Çıkarımlar:**
- Sabit 1,5 USD komisyon küçük tutarları cezalandırıyor. 1.000 USD'de gidiş-dönüş %0,31 eder. Bu, VİOP Midas tarifesindeki %0,05 × 2 + %5 BSMV ≈ %0,105'in üç katı.
- 10.000 USD'de ABD ETF komisyonu ve spreadi (%0,04) VİOP'tan daha ucuz.
- Asıl belirsizlik kur makası. TL bakiyeyle her işlemde çevirmek maliyeti 5 ile 25 kat artırabiliyor. Sık trade için bakiyenin USD'de tutulması, kur dönüşümünün işlem başına değil bir kez yapılması gerekiyor.

### 3.3 Karşılaştırma için BIST BYF ve VİOP maliyetleri
- **GLDTR:** Alış-satış 555,00 / 555,50 TL, yani yaklaşık %0,09 (tek anlık görüntü, tarihsiz). 1.000 USD karşılığı (≈50.160 TL) için ≈45 TL, 10.000 USD karşılığı (≈501.600 TL) için ≈450 TL spread maliyeti. Midas BIST komisyonu ücretsizse kur maliyeti yok. [GCM GLDTR](https://www.gcmyatirim.com.tr/borsa/hisse/gldtr-qnb-portfoy-altin-katilim-borsa-yatirim-fonu)
- **ZGOLD:** GCM'deki alış-satış verisi tutarsız. Investing.com'daki anlık 646,25 / 648,00 farkı %0,27 ediyor (tarihsiz). Güvenilir spread **bulunamadı**.
- **GMSTR:** 525,00 / 525,50 TL, ≈ %0,10 (tek anlık görüntü).
- **VİOP F_XAUUSD:** Midas'ta yok. Başka kurumda aracı komisyonu onbinde 0,9 ile binde 2 arasında, buna %5 BSMV, borsa payı yüzbinde 3 ve Takasbank yüzbinde 1 ekleniyor (kardeş rapor r1). Piyasa yapıcının azami spread yükümlülüğü normal seansta 2,80 USD (≈%0,07). Gerçekleşen tipik spread bulunamadı.

---

## 4. İşlem saatleri, emirler, takas, saklama, koruma

| Konu | Bulgu | Kaynak |
|---|---|---|
| Seanslar (kış saati, TSİ) | Gece 04:00–12:00, açılış öncesi 12:00–17:30, normal 17:30–00:00, kapanış sonrası 00:00–04:00. Hafta içi 24 saat. Yaz saatinde normal seans 16:30–23:00 (2023 duyurusunda açılış öncesi 11:00–16:30, kapanış sonrası 23:00–03:00 deniyordu) | [Saatler](https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/hangi-saatler-arasinda-emir-verebilirim), [2023 duyurusu](https://www.getmidas.com/midasin-kulaklari/midasta-gunler-uzuyor-uzatilmis-islem-saatleri-simdi-midasta-p-22615) |
| 24/5 altyapısı | Alpaca'nın 2025'te eklediği 24/5 işlem | [Alpaca blog, 17.03.2026](https://alpaca.markets/blog/how-midas-is-leveling-the-playing-field-for-turkish-investors/) |
| Emir tipleri | Piyasa, limit, stop, stop-limit, kâr al/zarar durdur. Uzatılmış ve gece seansında yalnızca limit | [Emir tipleri](https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/midasta-hangi-emir-tiplerini-kullanabilirim), [Gece](https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-emir-turunu-kullanabilirim) |
| MOC, LOC, kapanış müzayedesi, trailing stop, GTC | **Bulunamadı.** Listelenen tipler arasında yok | aynı |
| Kesirli pay | Var, 1 USD'den başlıyor. ETF'lerde de parçalı alım-satım mümkün | [ABD borsaları](https://www.getmidas.com/abd-borsalari/), [Parça hisse](https://www.getmidas.com/midas-akademi/parca-hisse-senedi-nedir/) |
| Takas | ABD: T+1, "genellikle bir sonraki iş günü saat 12:00'ye kadar". BIST: T+2 | [Takas süresi](https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/amerikan-borsasinda-takas-suresi-ne-anlama-gelir), [Çekilebilir tutar](https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/para-cekme-islemi/satisini-yaptigim-bir-hissenin-tutari-ne-zaman-cekilebilir-olur) |
| Gerçek zamanlı fiyat | ABD, BIST ve Avrupa canlı verisi ücretsiz | [Ücretler](https://www.getmidas.com/ucretler/) |
| ABD aracısı ve saklamacı | Aracı Alpaca Securities LLC, saklama ve takas DTCC. Midas ile Alpaca birbirinden bağımsız şirketler. Midas'a göre paylar yatırımcı "namına" yazılıyor | [Midas yasal](https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-sirketi-hakkinda-genel-bilgiler/midasi-guvenilir-kilan-yasal-sorumluluklari-neler), [Alpaca blog](https://alpaca.markets/blog/how-midas-is-leveling-the-playing-field-for-turkish-investors/) |
| SIPC | Standart: müşteri başına 500 bin USD (en fazla 250 bini nakit). Alpaca'nın ek poliçesi: 75 milyon USD menkul kıymet ve 75 milyon USD nakit, toplam tavan 250 milyon USD. Midas'ın "SIPA 150 milyon USD'ye kadar korur" ifadesi standart SIPC ile ek poliçeyi birbirine karıştırıyor. Piyasa kayıpları kapsam dışı | [Alpaca PDF](https://files.alpaca.markets/disclosures/library/SIPC%20and%20Excess%20SIPC%20Protection.pdf), [SIPC SSS](https://Sipc.org/for-investors/investor-faqs) |
| Türkiye tarafı koruma | Midas YTM üyesi. 2026 azami tazmin tutarı 2.065.145 TL (ikincil kaynaklar tutarlı, ytm.gov.tr'den doğrulanmadı). TMSF banka mevduatı içindir, aracı kurum hesapları YTM kapsamında | [Midas yasal](https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-sirketi-hakkinda-genel-bilgiler/midasi-guvenilir-kilan-yasal-sorumluluklari-neler), [YatırımX](https://www.yatirimx.com.tr/sirket-haberleri/tera-yatirim-icin-e-devlette-tazmin-basvuru-ekrani-acildi/27723) |

**Kapanıştan kapanışa trade için zamanlama:**
- VİOP F_XAUUSD'nin günlük uzlaşma fiyatı 18:00–18:10 TSİ arasındaki işlemlerin hacim ağırlıklı ortalaması (VWAP). Bu, kışın LBMA PM ihalesiyle (15:00 Londra = 15:00 UTC) aynı ana denk geliyor (kardeş rapor r1).
- ABD ETF kapanışı kışın 00:00 TSİ. Yani aynı günün iki "kapanışı" arasında 6 saat var.
- Midas'ta ABD normal seansı 17:30'da başladığı için, VİOP uzlaşma penceresinde (18:00–18:10) GLD veya IAU'yu normal seansta, piyasa emriyle almak mümkün. Bu sayede VİOP uzlaşmasına dayanan bir sinyal, ETF'te aynı anda uygulanabilir.
- Tersine, ETF'in 00:00 kapanışına göre kurulmuş bir sinyal MOC olmadığı için ancak 23:5x civarında piyasa veya limit emirle yaklaşık olarak uygulanabilir.

---

## 5. BIST tarafı (Midas'ta BYF'ler, Darphane sertifikası, VİOP)

Midas'ın destek sayfasına göre BIST'teki BYF'ler ve VİOP işlemleri Midas'ta var ([kaynak](https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-ile-neler-yapabilirim/midas-yatirim-hesabin-ile-hangi-yatirimlari-yapabilirsin)). Midas'ın BIST sitemap'inde ALTINS1 var. GLDTR, ZGOLD, ISGLK ve GMSTR için Midas'ta sayfa yok (404). BYF'lerin Midas'ta tek tek işlem görüp görmediği uygulamadan teyit edilmeli.

| Kod | Ürün | Dayanak | Yıllık yönetim ücreti | Fiyat ve likidite | Stopaj (gerçek kişi) | Kaynak |
|---|---|---|---|---|---|---|
| GLDTR | QNB Portföy Altın Katılım BYF (2007'den beri borsada) | 995/1000 fiziki altın. Pay başına ≈0,085 g altın ve 4,09 TL nakit dengeleme | ≈%0,47 | Kapanış 542,50 TL (4.11.2026). 42 günlük ortalama ≈262 bin lot ≈ 142 milyon TL/gün | %17,5 | [QNB](https://www.qnbinvest.com.tr/gldtr), [GCM](https://www.gcmyatirim.com.tr/borsa/hisse/gldtr-qnb-portfoy-altin-katilim-borsa-yatirim-fonu) |
| ZGOLD | Ziraat Portföy Altın Katılım BYF | Fon endeksi. Varlıkların %49,4'ü altın, %49,4'ü altına dayalı kira sertifikası, %1,2'si katılım hesabı | %0,40 (Ziraat). GCM %0,25 diyor, kaynaklar çelişiyor | Fiyat 657,56 TL. Fon büyüklüğü 82,3 milyar TL. 42 günlük ortalama ≈82 milyon TL/gün | %17,5 | [Ziraat Portföy](https://www.ziraatportfoy.com.tr/altin-katilim-borsa-yatirim-fonu-zgold), [GCM](https://www.gcmyatirim.com.tr/borsa/hisse/zgold-ziraat-portfoy-altin-katilim-borsa-yatirim-fonu) |
| ISGLK | İş Portföy Altın Katılım BYF (17.07.2024'ten beri borsada) | BIST Spot Altın Endeksi. Varlıkların %63,5'i kıymetli maden, %36,6'sı altına dayalı kamu kira sertifikası | %0,40 | Fiyat 669,44 TL (6.11.2026). Fon büyüklüğü 78,9 milyar TL. İşlem 10:00–18:10, takas T+2 | %17,5 (10041 sayılı CK) | [İş Portföy](https://www.isportfoy.com.tr/is-portfoy-altin-katilim-borsa-yatirim-fonu) |
| GMSTR | QNB Portföy Gümüş Katılım BYF | 999/1000 fiziki gümüş | ≈%0,47 | 520,50 TL (4.11.2026). 42 günlük ortalama ≈755 bin lot ≈ 393 milyon TL/gün | %17,5 | [QNB](https://www.qnbinvest.com.tr/gmstr), [GCM](https://www.gcmyatirim.com.tr/borsa/hisse/gmstr-qnb-portfoy-gumus-katilim-borsa-yatirim-fonu) |
| ALTINS1 | Darphane Altın Sertifikası (Kasım 2022'den beri) | 1 sertifika = 0,01 g. 50 g'dan itibaren fiziki teslim alınabiliyor | — | 71,45 TL (6.11.2026). Günlük hacim 702,6 milyon TL. **Gram altına göre ≈%9 prim** | %0 (yalnızca ikincil kaynaklar, resmi teyit yok) | [Midas ALTINS1](https://www.getmidas.com/canli-borsa/altins1-hisse/), [Midas gram altın](https://www.getmidas.com/altin/gram-altin/), [Bloomberg HT](https://www.bloomberght.com/borsa-istanbul-da-gong-darphane-altin-sertifikasi-icin-caldi-2319601) |

**NAV'a göre prim ve iskonto davranışı:**
- QNB Yatırım, 02.02.2026 tarihli KAP açıklamasında ons altın hareketleri nedeniyle GLDTR fiyatlarının "gösterge net aktif değerinden sapmalar gösterebileceğini" duyurdu. Yatırımcılara 15 saniyede bir güncellenen gösterge NAV'ı (kod GLDTRI) izlemelerini önerdi. [KAP 1550984](https://kap.org.tr/en/Bildirim/1550984)
- Sürekli bir prim/iskonto serisi **bulunamadı**. 1–5 günlük trade'de BYF'ler arasındaki farkın kaynağı bu sapma ve BIST seansının 18:10'da bitmesi.
- Kira sertifikası ağırlıklı yapılar (ZGOLD, ISGLK) altını birebir değil, TL getirili bir sepet üzerinden takip ediyor. Kısa ufukta izleme farkı olabilir. Bu raporda ölçülmedi.

**Midas'ta VİOP:**
- Mayıs 2026'da duyuruldu, Haziran 2026'da açılması planlanıyordu. [Forbes TR](https://www.forbes.com.tr/fintek/midas-islem-yelpazesine-bes-yeni-urun-ekledi)
- Dayanaklar pay, endeks, USD/TRY, EUR/TRY ve XAU/TRY. **XAU/USD (F_XAUUSD) ve opsiyon yok.**
- Gün seansı 09:30–18:10, akşam seansı 19:00–23:00 (yalnızca BIST'in belirlediği sözleşmelerde). Kardeş rapor r1'e göre gram altın (XAUTRY) akşam seansında **yok**.
- Teminat başlangıç listeleri 01.07, 01.09 ve 02.10.2026 tarihli. [Midas VİOP](https://www.getmidas.com/viop/)

---

## 6. Vergi (Türkiye'de tam mükellef gerçek kişi, 2026)

### 6.1 ABD ETF alım-satım kazancı
- **Nitelik:** Değer artış kazancı (GVK mük. 80). Hesaplama GVK mük. 81'e göre yapılıyor. Alış ve satış bedelleri, alım ve satım tarihlerindeki kurlarla TL'ye çevriliyor. **Kur farkı vergiye tabi.** Dolar bazında zarar edilse bile TL bazında kazanç çıkarsa vergi doğuyor. [Yapı Kredi 2026 vergi notu](https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view)
- **Endeksleme:** Alım ile satım arasında Yİ-ÜFE %10 veya daha fazla arttıysa maliyet endeksleniyor. 1–5 günlük işlemlerde bu eşik hiç aşılmaz. Pratikte endeksleme yok.
- **İstisna ve beyan sınırı yok.** Tutarı ne olursa olsun beyan ediliyor. Midas da yurt dışı hisse kazançlarının "tutarına bakılmaksızın" beyan edilmesi gerektiğini söylüyor. [Midas beyan](https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/beyanname-nasil-verilir)
- **Zarar mahsubu:** Aynı yıl içindeki yabancı para menkul kıymet zararları (yurt dışı hisse, fon, Eurobond) kazançlardan mahsup ediliyor. Bu, kanunda değil, Maliye'nin basın açıklamasında yer alıyor. Zarar kira veya serbest meslek gibi diğer gelirlerden düşülemiyor (GVK 88). Sonraki yıla devri **bulunamadı**. Komisyon ve aracı kurum ücretleri maliyete eklenebiliyor. [Yapı Kredi](https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view)
- **2026 ücret dışı gelir tarifesi** (332 Seri No.lu GVK Genel Tebliği, RG 31.12.2025): 190.000 TL'ye kadar %15; 400.000 TL'ye kadar %20; 1.000.000 TL'ye kadar %27; 5.300.000 TL'ye kadar %35; üstü %40. [alomaliye](https://www.alomaliye.com/2025/12/31/2026-yili-vergi-dilimleri/)
  - Başka geliri olmayan biri için örnekler: 100.000 TL net kazançta 15.000 TL vergi (%15). 500.000 TL'de 97.500 TL (ortalama %19,5). 1.000.000 TL'de 232.500 TL (%23,3).
  - Ücret geliri zaten üst dilimdeyse, Midas'ın 2025 örneğinde 4,3 milyon TL ve üstü, ek kazanç %40'tan vergilendiriliyor. [Midas](https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/yurt-disi-hisse-alim-satim-ve-temettu-gelirlerim-icin-ne-kadar-vergi-odemeliyim)
- **Beyan takvimi:** Mart ayında beyan ediliyor. 2025 kazançları 1–31 Mart 2026'da beyan edildi. Ödeme Mart ve Temmuz'da iki taksit.
- **Midas'ın uygulaması:** Türk vergisi için stopaj kesmiyor, beyan müşteriye ait. Talep edilirse yıllık "vergi durum özeti" hazırlıyor. [Midas vergi özeti](https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/midastaki-amerikan-borsasi-vergi-durumu-ozetimi-nereden-gorebilirim)

### 6.2 Dağıtımlar (temettü)
- **ABD stopajı:** Kanuni oran %30. Türkiye–ABD anlaşmasıyla genel portföy temettüsünde **%20**, ≥%10 doğrudan iştirakte %15. RIC dağıtımları %20 sütununda. W-8BEN ile anlaşma oranı uygulanıyor. [IRS Tablo 1 (Rev. Mayıs 2023, PDF 2026'da güncellendi)](https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf)
- **Midas'ın %15 örneği:** Midas'ın mahsup sayfası "ABD stopajı %15" diye bir örnek veriyor. IRS tablosuyla çelişiyor. W-8BEN ile kesilen gerçek oran 1042-S belgesinden kontrol edilmeli. [Midas mahsup](https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/amerikan-borsasindaki-temettu-odemelerinde-amerikada-kesilen-stopaji-turkiyede-vergi-beyan-ederken-mahsup-edebilir-miyim)
- **Türkiye'de beyan:** Yabancı temettü ve USD neması için 2026 beyan sınırı 22.000 TL (2025'te 18.000 TL). Sınır aşılırsa tamamı beyan ediliyor. ABD'de ödenen vergi GVK 123'e göre mahsup ediliyor. Hazır Beyan'da "Yabancı Ülkelerde Ödenen Vergiler" satırına apostilli 1042-S ile giriliyor. Fazla ödenen kısım iade edilmiyor.
- **Altın ETF'lerinde pratik etki:** GLD, IAU ve GLDM grantor trust olduğu için dağıtım yapmıyor. GLD 10-K'ya göre ABD dışı yatırımcının satış kazancı, 183 gün ABD'de bulunma veya ABD'de ticari faaliyet durumları dışında ABD vergisine tabi değil. GDX ve GDXJ dağıtım yapıyor ve %20 ABD stopajına giriyor. [GLD 10-K](https://www.sec.gov/Archives/edgar/data/1222333/000143774924036161/gld20240930_10k.htm)

### 6.3 BIST altın BYF'leri
- GVK geçici 67 kapsamında stopaj uygulanıyor. Oran, payın **alım tarihine** göre değişiyor. Kıymetli maden fonlarında:
  - 23.12.2020–30.04.2024: %0
  - 01.05–31.10.2024: %7,5
  - 01.11.2024–31.01.2025: %10
  - 01.02–08.07.2025: %15
  - **09.07.2025'ten itibaren: %17,5** (10041 sayılı Cumhurbaşkanı Kararı, RG 9.7.2025/32951)
  - [Garanti Portföy broşürü](https://www.garantibbva.com.tr/content/dam/public-website/pdf/yatirim/fonlar/garanti-portfoy-altin-fonu-brosur.pdf), [İş Portföy](https://www.isportfoy.com.tr/is-portfoy-altin-katilim-borsa-yatirim-fonu)
- 11107 sayılı CK (RG 27.03.2026) ve 11734 sayılı CK (RG 05.09.2026) bireylerin altın fonu oranını değiştirmedi. 11734 kurumların para piyasası fonlarıyla ilgili. [İş Portföy Mart 2026](https://www.isportfoy.com.tr/medya-ve-blog/yatirim-fonlarina-uygulanan-stopaj-duzenlemesi-hakkinda-mart-2026)
- Bireyler için stopaj kural olarak nihai vergi. Ayrıca beyan gerekmiyor. Zararlı satıştan stopaj kesilmiyor. BYF zararlarının aynı yıl içinde başka BYF kazançlarından mahsup edilip edilemeyeceği birincil kaynakta **bulunamadı**.

### 6.4 VİOP
- Pay ve pay endeksi dışındaki sözleşmelerde (döviz, emtia, kıymetli maden) bireysel yatırımcı için %10 stopaj var. BSMV istisnası var. [Borsa İstanbul vergilendirme](https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme)
- Kardeş rapor r1'e göre üç aylık dönemler itibarıyla netleştiriliyor. Zarar yalnızca aynı takvim yılında devrediliyor.

### 6.5 Vergi özeti (net kazanç 100.000 TL, başka gelir yok)
| Kanal | Vergi | Efektif oran |
|---|---|---|
| VİOP F_XAUUSD | 10.000 TL stopaj | %10 |
| BIST altın BYF (9.7.2025 sonrası alım) | 17.500 TL stopaj (zararların netleşebildiği varsayımıyla) | %17,5 |
| ABD ETF (beyan) | 15.000 TL. Ücret geliri üst dilimdeyse 40.000 TL | %15–%40. Ayrıca kur farkı matraha giriyor |

---

## 7. ABD veraset (estate) vergisi riski

- **Eşik:** ABD vatandaşı olmayan ve ABD'de yerleşik olmayan birinin ölüm anındaki ABD-situs varlıkları 60.000 USD'yi aşarsa Form 706-NA verilmesi gerekiyor. ABD kanunlarına göre kurulmuş şirketlerin payları, sertifikalar yurt dışında tutulsa bile ABD-situs sayılıyor (IRS, 27.06.2026 güncelleme). [IRS](https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns)
- **Anlaşma:** ABD'nin veraset ve hibe anlaşmaları 15 ülkeyle var: Avustralya, Avusturya, Danimarka, Fransa, Almanya, Japonya, İngiltere, Kanada, Finlandiya, Yunanistan, İrlanda, İtalya, Hollanda, Güney Afrika, İsviçre. **Türkiye yok.** [IRS](https://www.irs.gov/businesses/small-businesses-self-employed/estate-gift-tax-treaties-international)
- **GLD'nin kendi beyanı:** Paylar "kuvvetle muhtemel" ABD'de bulunuyor sayılır, bu durumda ABD dışı yatırımcının terekesine giriyor. Federal veraset vergisi %40'a kadar. Hibe vergisi açısından paylar maddi olmayan varlık sayıldığı için muhtemelen kapsam dışı. [GLD 10-K 2024](https://www.sec.gov/Archives/edgar/data/1222333/000143774924036161/gld20240930_10k.htm)
- **ABD ETF'leri (GLD, IAU, GLDM, UGL, NUGT vb.):** ABD'de kurulu, dolayısıyla ihtiyatlı varsayım ABD-situs.
- **ABD aracıda tutulan USD nakit:** ABD-situs sayılıp sayılmadığı **bulunamadı**.
- **Alternatifler:**
  - PHYS ve CEF Kanada (Ontario) trust'ı. ABD dışı situs olması beklenir, ama birincil kaynak **bulunamadı**. Ayrıca PHYS'in ortalama %2,5 iskontosu kısa vadeli trade'de gürültü yaratıyor.
  - UCITS ve ETC alternatifleri (SGLN, PHAU: LSE; 4GLD: Xetra, Deutsche Börse Commodities'in fiziki altın karşılıklı hamiline yazılı tahvili). Midas'ta LSE yok. Xetra var ama ETC ve ETF işlemi doğrulanamadı. Yani **Midas'ta UCITS altın alternatifi doğrulanamadı.** [Xetra-Gold](https://www.xetra-gold.com/en/product)
  - BIST BYF'leri ve ALTINS1 ABD veraset vergisinin dışında.
- **Pratik kural:** Pozisyon taşınmadığı günlerde ABD-situs bakiyesinin 60.000 USD altında tutulması, büyük pozisyonların gece boyunca ABD ETF'lerinde bekletilmemesi riski sınırlar. Bu bir öneri, kaynak değil.

---

## 8. Yan yana karşılaştırma (1, 3 ve 5 günlük trade için)

| Boyut | VİOP F_XAUUSD (başka aracı kurumda) | Midas: ABD ETF'leri (GLD, IAU, GLDM; UGL, NUGT; GLL, DUST) | Midas/BIST: altın BYF'leri (GLDTR, ZGOLD, ISGLK) |
|---|---|---|---|
| Midas'ta var mı? | **Hayır.** Midas'ta yalnızca XAU/TRY | Evet. Ticker bazında uygulamadan teyit gerekli | BYF'ler var (Midas SSS). Ticker bazında teyit gerekli |
| Gidiş-dönüş işlem maliyeti | Aracı komisyonu ≈ onbinde 0,9 ile binde 2 (×2) + %5 BSMV + borsa ve Takasbank payları. Piyasa yapıcı azami spreadi ≈ %0,07. Midas XAU/TRY için %0,05 × 2 + BSMV ≈ %0,105 | 3 USD komisyon + %0,01–0,02 spread. 1.000 USD'de %0,31, 10.000 USD'de %0,04. Her işlemde TL↔USD çevriliyorsa +kur makası (bilinmiyor; %0,18 alınırsa 1.000 USD'de toplam %0,49, 10.000 USD'de %0,22) | Midas BIST komisyonu "ücretsiz" (BYF teyit edilmeli) + spread ≈ %0,04–0,27. Kur dönüşümü yok |
| Kaldıraç | ≈10 kat (Takasbank PSR %10; bazı kurumlar %20 istiyor) | Yok. Kaldıraçlı ETF'lerle 2 kat (UGL, NUGT), ETN'le 3 kat (GDXU). Kredili işlem bulunamadı | Yok. BIST kredili işlem var (yıllık %48,5–66,5 faiz). BYF'lerin teminat ve kredi kapsamında olup olmadığı bulunamadı |
| Kısa pozisyon | Doğrudan satış | Açığa satış bulunamadı. Ters ETF (GLL, DUST, JDST, ZSL) veya put alımı | Açığa satış bulunamadı. Pratikte yok |
| İşlem saatleri (TSİ, kış) | 09:30–18:10 ve akşam seansı 19:00–23:00. Uzlaşma 18:00–18:10 VWAP | Hafta içi 24 saat. Normal seans 17:30–00:00. Gece ve uzatılmış seanslarda yalnızca limit. MOC yok | 10:00–18:10 |
| Takas | T+1 (kâr/zarar günlük) | T+1 (ertesi iş günü 12:00) | T+2 |
| Kur riski | Fiyat USD, kâr/zarar her gün TCMB kuruyla TL'ye çevriliyor. Teminat TL | Varlık USD. TL tabanlı yatırımcının kâr/zararı USD/TRY ile çarpılıyor. Çevirme maliyeti var | Fiyat TL (gram altın × kur). Dönüşüm maliyeti yok |
| Sermaye verimliliği | Teminat dışındaki nakit TL'de değerlendirilebilir | Tam nakit gerekiyor | Tam nakit gerekiyor |
| Vergi | %10 stopaj, nihai, üç aylık netleştirme | Beyan: %15–40 artan oranlı. Kur farkı dahil. Endeksleme pratikte yok. Yıl içinde zarar mahsubu var | %17,5 stopaj (9.7.2025 sonrası alım), nihai |
| Likidite | Medyan ≈43 bin sözleşme/gün (≈43 bin ons ≈ 175 milyon USD) | GLD, IAU, GLDM: 30 günlük medyan spread %0,01. IAU ≈350 milyon USD/gün, SLV ≈885 milyon USD/gün | GLDTR ≈142 milyon TL/gün (≈2,8 milyon USD). ZGOLD ≈82 milyon TL/gün. GMSTR ≈393 milyon TL/gün |
| Fiyat sapması riski | Vadeli-spot bazı (taşıma maliyeti) | GLD ve IAU'da NAV zamanlaması kaynaklı ±%0,4'e varan prim/iskonto. PHYS'te ≈%2,5 iskonto | KAP: gösterge NAV'dan sapma olabiliyor. ALTINS1 gram altının ≈%9 üstünde |
| Veraset riski | Yok (Türkiye varlığı) | **Var.** ABD-situs, 60.000 USD eşiği, %40'a kadar, anlaşma yok | Yok |
| Karşı taraf ve koruma | Takasbank merkezi karşı taraf. YTM | Alpaca/DTCC, SIPC (500 bin USD) + Alpaca ek poliçesi. ETN'lerde ihraççı kredi riski | MKK saklama. YTM 2.065.145 TL |

---

## 9. 1, 3 ve 5 günlük trade için platforma özgü çıkarımlar

1. **F_XAUUSD Midas'ta yok.** Midas'ta tek kalmak isteyen biri için altın kanalları XAU/TRY vadeli, BIST BYF'leri ve ABD ETF'leri. F_XAUUSD sinyalleri ABD ETF'leriyle (GLD, IAU, GLDM) uygulanabilir. Kış saatinde VİOP uzlaşma penceresi (18:00–18:10) ABD normal seansına denk geldiği için zamanlama uyumu iyi.
2. **İşlem büyüklüğü eşiği.** Sabit 1,5 USD komisyon yüzünden ABD ETF kanalı ancak işlem başına birkaç bin USD üstünde VİOP ile maliyet açısından yarışıyor. Başabaş, kur maliyeti yok sayılırsa ve Midas XAU/TRY oranı (≈%0,105) baz alınırsa, 3 / (0,00105 − 0,0001) ≈ 3.160 USD.
3. **Kur dönüşümü en büyük gizli maliyet.** Midas'ın kur makası yayımlanmıyor. Trade sermayesinin bir kez USD'ye çevrilmesi ve USD'de tutulması gerekiyor. Ancak TL tabanlı vergide kur farkı her satışta matraha giriyor.
4. **Vergi yükü stratejiyi değiştirebilir.** Brüt getirisi aynı olan bir strateji VİOP'ta %10, BYF'de %17,5, ABD ETF'te %15–40 vergi ödüyor. Yüksek gelirli biri için ABD ETF kanalı VİOP'a göre net getiride dezavantajlı.
5. **Kısa yön.** Midas'ta ABD tarafında yalnızca ters ETF ve put var. Ters ETF'ler 2 kat ve günlük yeniden dengeleniyor. 3–5 günlük tutmada yol bağımlılığı var. GLL ve ZSL K-1 düzenleyen ProShares ürünleri.
6. **Veraset.** 60.000 USD üstünde gece pozisyon taşıyan bir ABD ETF trader'ı, Türkiye ile anlaşma olmadığı için ölüm halinde %40'a varan ABD vergisine maruz kalabilir.
7. **BYF'lerde.** 18:10 kapanışı, gösterge NAV'dan sapma ve %17,5 stopaj var. ALTINS1'deki ≈%9 prim, onu kısa vadeli altın takibi için uygun olmaktan çıkarıyor.

---

## 10. Bulunamayanlar (açıkça)

- Midas TL↔USD döviz makası (oran veya tutar).
- Midas'ta GLD, IAU, GLDM, SGOL, AAAU, BAR, PHYS, CEF, GDX, GDXJ, RING, SIL, SLV, UGL, AGQ, NUGT, JNUG, GDXU, GLL, DZZ, DUST, JDST, ZSL için ticker bazında işlem izni. Sitede ETF sayfası yok.
- Midas'ın veya Alpaca'nın kaldıraçlı ETF, ters ETF, ETN ve PTP (K-1) ürünlerine özel kısıt koyup koymadığı.
- ABD tarafında açığa satış ve kredili işlem (bilgi yok, sözleşmeye göre nakit hesap).
- MOC, LOC, kapanış müzayedesi, trailing stop ve GTC emir tipleri.
- "Midas Plus" adlı bir paket. Yalnızca Midas Pro (BIST veya VİOP, 1.200 TL/ay) bulundu.
- Avrupa tarafında ETF ve ETC (4GLD, UCITS altın) işlemi.
- PHYS ve CEF'in ABD veraset vergisi açısından situs durumu (birincil kaynak).
- ABD aracıda tutulan USD nakdin veraset vergisi açısından durumu.
- NUGT, DUST, AGQ, GLL, ZSL, RING, SIL, CEF için ihraççıdan alınmış güncel gider oranı ve spread.
- BIST BYF'lerinde sürekli prim/iskonto serisi ve aynı yıl içinde zarar mahsubu.
- ALTINS1 için %0 stopajın resmi dayanağı.
- Yabancı ETF zararlarının sonraki yıla devri.
- YTM 2026 tutarının ytm.gov.tr'den birincil teyidi.

---

## 11. Kaynaklar

Midas:
- https://www.getmidas.com/ucretler/
- https://www.getmidas.com/destek/profil-ve-hesap-bilgileri/ucretler-ve-komisyon/komisyon-oranlari-nelerdir
- https://webcdn.getmidas.com/uploads/2025/12/04155923/genel-cerceve-sozlesme.pdf (Genel Çerçeve ve Hesap Açılış Sözleşmesi, Ek-5 tarife)
- https://www.getmidas.com/abd-borsalari/
- https://www.getmidas.com/viop/
- https://www.getmidas.com/destek/borsa-istanbul/viop/viopta-islem-goren-kontratlar-nelerdir
- https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/hangi-saatler-arasinda-emir-verebilirim
- https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/midasta-hangi-emir-tiplerini-kullanabilirim
- https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-emir-turunu-kullanabilirim
- https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-hisselerde-islem-yapabilirim
- https://www.getmidas.com/midasin-kulaklari/midasta-gunler-uzuyor-uzatilmis-islem-saatleri-simdi-midasta-p-22615
- https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/amerikan-borsasinda-takas-suresi-ne-anlama-gelir
- https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/para-cekme-islemi/satisini-yaptigim-bir-hissenin-tutari-ne-zaman-cekilebilir-olur
- https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/amerikan-borsasi-piyasa-emirlerindeki-marj-kurali-nedir
- https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-sirketi-hakkinda-genel-bilgiler/midasi-guvenilir-kilan-yasal-sorumluluklari-neler
- https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-ile-neler-yapabilirim/midas-yatirim-hesabin-ile-hangi-yatirimlari-yapabilirsin
- https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/doviz-al-sat/hangi-saatler-arasinda-doviz-al-sat-yapabilirim
- https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/doviz-al-sat/cevirdigim-para-ile-aninda-emir-verebilir-miyim
- https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/para-aktarma-islemi/para-yatirma-ucreti-var-mi
- https://www.getmidas.com/canli-doviz/dolar-fiyat/
- https://www.getmidas.com/midas-pro/
- https://www.getmidas.com/avrupa-borsalari/
- https://www.getmidas.com/midas-akademi/etf-nedir-nasil-alinir/
- https://www.getmidas.com/canli-borsa/altins1-hisse/
- https://www.getmidas.com/altin/gram-altin/
- https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/yurt-disi-hisse-alim-satim-ve-temettu-gelirlerim-icin-ne-kadar-vergi-odemeliyim
- https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/amerikan-borsasindaki-temettu-odemelerinde-amerikada-kesilen-stopaji-turkiyede-vergi-beyan-ederken-mahsup-edebilir-miyim
- https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/beyanname-nasil-verilir
- https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/midastaki-amerikan-borsasi-vergi-durumu-ozetimi-nereden-gorebilirim

Alpaca, SIPC:
- https://alpaca.markets/blog/how-midas-is-leveling-the-playing-field-for-turkish-investors/
- https://files.alpaca.markets/disclosures/library/SIPC%20and%20Excess%20SIPC%20Protection.pdf
- https://Sipc.org/for-investors/investor-faqs

ETF ihraççıları ve SEC:
- https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld
- https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-minishares-trust-gldm
- https://www.ishares.com/us/products/239561/ishares-gold-trust-fund
- https://www.ishares.com/us/products/239855/ishares-silver-trust-fund
- https://www.vaneck.com/us/en/investments/gold-miners-etf-gdx/overview/
- https://www.vaneck.com/us/en/investments/junior-gold-miners-etf-gdxj/overview/
- https://www.proshares.com/our-etfs/leveraged-and-inverse/ugl
- https://www.proshares.com/globalassets/proshares/documents/qualified-reports/pst_ii_qualified_notice_02262026.pdf
- https://www.direxion.com/product/daily-junior-gold-miners-bull-bear-2x-etfs (403, arama özeti)
- https://www.sec.gov/Archives/edgar/data/0001477049/000199937126017864/ex99-1.htm (Sprott PHYS)
- https://www.sec.gov/Archives/edgar/data/1222333/000143774924036161/gld20240930_10k.htm (GLD 10-K)
- https://www.credit-suisse.com/articles/media-releases/2020/06/en/credit-suisse-ag-announces-its-intent-to-delist-and-suspend-further-issuances-of-its-velocitysharestm-etns.html
- https://credit-suisse.com/articles/media-releases/2023/10/en/credit-suisse-announces-the-acceleration-at-its-option-of-its-previously-delisted-velocityshares-etns.html
- https://etfdb.com/advisor_reports/DZZ/ ; https://www.etfdb.com/etf/GDXU ; https://www.etfcentral.com/compare-etfs/SGOL-vs-AAAU

IRS:
- https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf
- https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns
- https://www.irs.gov/businesses/small-businesses-self-employed/estate-gift-tax-treaties-international

SPK, vergi, BIST:
- https://spk.gov.tr/data/61e496a11b41c60d1404d6b2/Yat%C4%B1r%C4%B1m%20Hizmetleri%20ve%20Kurulu%C5%9Flar%C4%B1%20Rehberi%20(i-SPK.37.8)%2010%2003%202026.pdf
- https://www.alomaliye.com/2025/12/31/2026-yili-vergi-dilimleri/
- https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view
- https://www.garantibbva.com.tr/content/dam/public-website/pdf/yatirim/fonlar/garanti-portfoy-altin-fonu-brosur.pdf
- https://www.isportfoy.com.tr/medya-ve-blog/yatirim-fonlarina-uygulanan-stopaj-duzenlemesi-hakkinda-mart-2026
- https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme
- https://kap.org.tr/en/Bildirim/1550984
- https://www.qnbinvest.com.tr/gldtr ; https://www.qnbinvest.com.tr/gmstr
- https://www.ziraatportfoy.com.tr/altin-katilim-borsa-yatirim-fonu-zgold
- https://www.isportfoy.com.tr/is-portfoy-altin-katilim-borsa-yatirim-fonu
- https://www.gcmyatirim.com.tr/borsa/hisse/gldtr-qnb-portfoy-altin-katilim-borsa-yatirim-fonu ; .../zgold-... ; .../gmstr-...
- https://www.forbes.com.tr/fintek/midas-islem-yelpazesine-bes-yeni-urun-ekledi
- https://www.yatirimx.com.tr/sirket-haberleri/tera-yatirim-icin-e-devlette-tazmin-basvuru-ekrani-acildi/27723
- https://finans.mynet.com/haber/detay/doviz/7-kasim-2026-dolar-bugun-kac-tl-serbest-piyasa-dolar-kuru/583283/
- https://www.xetra-gold.com/en/product
- Kardeş rapor: /tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/research/r1_viop_kontrat.md (VİOP uzlaşma penceresi, teminat, maliyet, likidite)
