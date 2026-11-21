# E4 · Tarım, yumuşak emtialar, canlı hayvan, kereste

## Özet

ABD'de bu grupta tek emtiaya bağlı likit araç az. Fiyatı kendi başına taşıyabilen tek emtia ETF'leri CORN, WEAT, SOYB ve CANE (Teucrium, vadeli, K-1 formu çıkarır). Ama günlük hacimleri 1 ile 10 milyon dolar arasında. DBA sepeti (27 mn $/gün) en likit seçenek. Kaldıraçlı araç olarak yalnızca Teucrium'un 2 kat günlük getiri hedefleyen CXRN (mısır) ve WXET (buğday) fonları var. İkisi de K-1 yerine 1099 formu verir. Ters (inverse) tarım ETF'i bulunamadı. Kakao, kahve, pamuk ve canlı hayvan için ABD'de ETF/ETN yok: iPath ETN'leri kapandı ve yerlerine bir şey gelmedi. Bu emtialara ancak vadeli işlemle ya da vekil hisseyle (HSY, MDLZ, SBUX, TSN) erişilebilir.

Zamanlama tarafında, tahıl, yumuşak emtia ve canlı hayvan fiyatları 16:00 ET'den önce kesinleşir. **İstisna kereste:** 16:05 ET'ye kadar işlem görür. Kalıcı bir öncülük kaynağı var: tahıl 14:20 ET'de kapandıktan sonra dolar, petrol ve hisse piyasasında olan hareketler tahıla ancak 20:00 ET'de, gece seansı açılınca yansır. 2026'daki ana temalar şunlar: güçlü El Niño (kakao, pirinç, şeker), Brezilya'nın rekor kahve hasadı, Fed'den faiz artırımı beklentisiyle dolar ve ABD buğday üretimindeki çöküş.

## Araç tablosu

Sayılar ozet_istatistik.csv'den: fiyat, YTD (yılbaşından beri getiri, %), hacim20 (20 günlük ortalama günlük hacim, mn $), oyn60 (60 günlük yıllık oynaklık, %).

| Emtia | Ana ETF/ETN | Yapı ve maliyet | Kaldıraçlı/ters | İlgili hisseler | Not |
|---|---|---|---|---|---|
| Mısır (ZC=F) | CORN (hacim20 2,7; YTD -4,7) | CBOT vadelisi, 3 vadeye yayılmış; K-1 verir, 60/40 vergi kuralı (Section 1256) geçerli. Toplam gider ~%2 (doğrulanmadı, bellek). Contango'da (ileri vadeler pahalı) vade devri getiriyi aşındırır | CXRN 2x günlük (1940 Act fonu, 1099). Ters ürün yok | CF, NTR, MOS (gübre), DE, CTVA, ADM, GPRE*, INGR*, TSN/PPC* (yem maliyeti) | ZC=F hacim20 110 mn $, YTD -1,3 |
| Buğday (ZW=F, KE=F) | WEAT (9,5; YTD 7,4) | CBOT SRW buğdayı; K-1 verir | WXET 2x günlük (1099) | GIS, KHC (zayıf maliyet bağı), ADM, BG | KE=F YTD +21,3, ZW=F +13,3; son 3 ayda -16 ile -17 |
| Soya, yağ, küspe (ZS/ZL/ZM=F) | SOYB (0,9; YTD 17,0) | CBOT soya; K-1 verir. Soya yağı ve küspe için ayrı ETF yok | yok | ADM, BG (ezme marjı), DAR* (yenilenebilir dizel), DE | ZL=F YTD +24,4: biyoyakıt talebi |
| Pirinç (ZR=F) | yok (yalnızca DBA, TAGS dışında) | — | yok | — | ZR=F YTD +93,5, hacim20 ~0: Yahoo verisi neredeyse işlemsiz |
| Yulaf (ZO=F) | yok | — | yok | — | hacim20 0,2; gece/gün içi getiri ayrışması aşırı (veri kalitesi şüpheli) |
| Şeker (SB=F) | CANE (4,2; YTD 4,8) | ICE Sugar No.11; K-1 verir | yok | (KO, PEP zayıf bağ) | Brezilya reali ve etanol paritesi belirleyici |
| Kahve (KC=F) | ABD'de yok. JO (iPath) kapandı, yerine geçen yok | — | yok | SBUX, KDP* | KC=F YTD -21,2; 1 yılda -32,1 |
| Kakao (CC=F) | ABD'de yok. NIB kapandı, yerine geçen yok | — | yok | HSY, MDLZ | CC=F 5.125 $/t, YTD -15,5, oyn60 41,6 |
| Pamuk (CT=F) | ABD'de yok. BAL kapandı | — | yok | — | Tablodaki CT=F (75,5) ile TE'nin "82 sentin altı" ifadesi farklı vadeyi gösteriyor olabilir |
| Portakal suyu (OJ=F) | yok | — | yok | — | hacim20 0,1; oyn60 74,7; YTD -37,8 |
| Canlı ve besi sığırı (LE/GF=F) | ABD'de yok. COW kapandı | — | yok | TSN (sığır eti maliyeti: ters yön), HRL* | LE=F 223, YTD -3,9 |
| Domuz (HE=F) | yok | — | yok | TSN, SFD*, HRL* | HE=F 52,6, YTD -38,2, maxdd_1y -50 |
| Kereste (LBR=F) | WOOD, CUT (orman hisse ETF'leri, 1,1 ve 0,1) | Hisse ETF'i, vadeli değil | yok | WY, PCH, RYN, LPX, UFPI*, BCC* | LBR=F 537, hacim20 0,3 |
| Sepet | DBA (26,8; YTD 2,5), TAGS (0,3), TILL* (K-1'siz), MOO, VEGI (tarım hisse ETF'leri) | DBA: Invesco vadeli sepeti, K-1 verir, gider ~%0,85 (doğrulanmadı, bellek). TAGS'in gider oranı kaynaklarda %0,13 ile %1 arasında çelişkili. Fon içinde fon olduğu için toplam maliyet daha yüksek | yok | — | Kısa vadeli işlemde en uygulanabilir araç DBA ve tek tek hisseler |

\* Evrende yok, ek_semboller'e yazıldı.

## İşlem saatleri ve 16:00 ET'de bilinen bilgi

| Piyasa | Uzlaşma / kapanış (ET) | 16:00 ET'de durum |
|---|---|---|
| CBOT mısır, buğday, KC buğday, soya, yağ, küspe, pirinç, yulaf | Uzlaşma 13:14-13:15 CT'de hesaplanan hacim ağırlıklı ortalama fiyattır (VWAP) = 14:14-14:15 ET. Gündüz seansı 14:20 ET'de biter, gece seansı 20:00 ET'de açılır | Kesinleşmiş |
| ICE kakao 4:45-13:30, kahve 4:15-13:30, şeker 3:30-13:00, pamuk 21:00*-14:20, FCOJ 8:00-14:00 (NY saati, Eylül 2026 çizelgesi; PDF bozuk çıktığı için ürün eşleştirmesi bellekle yapıldı) | Uzlaşma her ürünün kapanışında (kakao 12:50 ve kahve 13:25 TAS saatleri haber özetinde geçiyor) | Kesinleşmiş |
| CME canlı sığır, besi sığırı, domuz | Gündüz seansı ~13:05 CT = 14:05 ET (doğrulanmadı; bulunan en yeni resmi kayıt 2016 tarihli, TAS işlemi 8:30-13:00 CT) | Kesinleşmiş |
| CME kereste (LBR) | 9:00-15:05 CT = **10:00-16:05 ET** | **Kesinleşmemiş.** Yahoo'daki kapanış ile hisse kapanışı arasında 5 dakika fark var |
| Brezilya B3 | 17:00 BRT = 15:00 ET (Kasım, BRT=UTC-3) | Kesinleşmiş |
| Dalian/Zhengzhou (soya, küspe, şeker, pamuk) | Gündüz 15:00 Pekin = 02:00 ET, gece seansı ~23:00 Pekin = 10:00 ET (bellek) | t günü sabah ET'de bilinir |
| ICE Londra (robusta kahve, beyaz şeker, Londra kakaosu) | ~11:30-12:55 Londra = 06:30-07:55 ET (bellek) | Kesinleşmiş |

Sonuç: Sinyal 16:00 ET'de sağlam ve kesinleşmiş tahıl, yumuşak emtia ve canlı hayvan fiyatıyla kurulabilir. Asıl fırsat şu boşlukta: tahıl 14:20 ET'de kapanıyor, ABD hisseleri 16:00 ET'de. Arada dolar endeksi (DXY), petrol ve SPY hareket ederse tahıl buna ertesi gün yetişir.

## 1-3 günlük sürücüler ve veri takvimi

| Açıklama | Kurum | Gün / saat ET | 16:00'ya göre |
|---|---|---|---|
| WASDE (dünya arz-talep tahmini) | USDA | Aylık 12:00 ET. 2026'nın kalan tarihi: **10 Aralık** | Önce |
| Grain Stocks, Prospective Plantings, Acreage | USDA NASS | 12:00 ET (2026: 12 Oca, 31 Mar, 30 Haz, 30 Eyl) | Önce |
| Crop Progress (ekim/hasat ilerlemesi) | USDA NASS | Pazartesi 16:00 ET, 6 Nisan-30 Kasım 2026 | **Sonra**: etkisi salı açılışında görülür |
| Export Sales (ihracat satışları) | USDA FAS | Perşembe 08:30 ET | Önce |
| Export Inspections (sevkiyat denetimi) | USDA AMS | Pazartesi 11:00 ET (bellek) | Önce |
| Cattle on Feed, Hogs and Pigs (çeyreklik), Cold Storage | USDA NASS | ~15:00 ET (2018 tarihli NASS notu; 2026 için doğrulanmadı) | Önce, ama vadeliler kapandıktan sonra: tepki hisselerde 15:00-16:00 arasında, vadelide ertesi gün |
| EIA etanol üretimi | EIA | Çarşamba 10:30 ET (bellek) | Önce |
| CFTC COT (pozisyon raporu) | CFTC | Cuma 15:30 ET (bellek) | Önce, vadeliler kapandıktan sonra |
| ICE sertifikalı stoklar, Fildişi Sahili liman girişleri | ICE, ihracatçılar | Günlük / haftalık | Çoğunlukla önce |

Saatli düzenli veriler dışındaki sürücüler şunlar:

- **Hava ve El Niño.** Fildişi Sahili meteoroloji kurumu Sodexam, 2026/27 kakao üretiminde %21-25 düşüş uyarısı yaptı. Güneydoğu Asya'da pirinç için kuraklık riski var.
- **Kur.** USD/BRL kahve, şeker ve soyayı etkiler. Dolar 19 ayın zirvesinde.
- **Faiz.** Aralık'ta faiz artırımı bekleniyor.
- **Petrol.** Biyoyakıt bağlantısı üzerinden soya yağı, şeker ve mısırı etkiler.
- **Ticaret politikası.** Trump-Xi görüşmeleri ve Çin'in 25 milyon ton soya alım taahhüdü. Kanada kerestesine %24,75 anti-damping ve telafi edici vergi, üstüne %10 gümrük vergisi.
- **Hastalık.** Yeni Dünya kurdu (screwworm) yüzünden Meksika sınırı canlı sığıra kapalı. Kasım ayındaki son durum doğrulanamadı.

## 2026 durumu

- **Tahıl.** Mısır ~4,3 $/bu ile Temmuz'dan beri en düşük seviyede. ABD 2026/27 mısır stoku 1.758 mn bu. Buğday ~5,7 $. ABD buğday üretimi 1.534 mn bu (geçen yıl 1.989). Buna karşılık Uluslararası Tahıl Konseyi (IGC) dünya tahminini 826 mt'ye yükseltti, Arjantin rekora yakın. Yani yerel kıtlık var ama küresel bolluk fiyatı baskılıyor.
- **Soya.** Soya ~12,1 $. Soya yağı biyoyakıt talebiyle güçlü (WASDE'de biyoyakıt kullanımı 17,8 mlr lb).
- **Pirinç.** YTD +%93. ABD ekim alanı 2,81'den 2,10 mn akre'ye indi, Asya'da El Niño etkisi var.
- **Kakao.** 10 Kasım'da 4.650 $ ile 4 ayın dibini gördü, 12 Kasım'da 5.200 $'ın üstüne çıktı. Ara hasat tahmini %42-50 düşük. Öte yandan sertifikalı stoklar 2,5 yılın zirvesinde. İki yönlü sert hareket bekleniyor.
- **Kahve.** ~2,7 $/lb, 1 yılda -%32. USDA Brezilya 2026/27 hasadını rekor 72,5 mn çuval olarak tahmin ediyor.
- **Şeker.** 17,03 sent, 1 ayda -%15.
- **Pamuk.** Zayıf ihracat, güçlü dolar.
- **Hayvancılık.** Sığır yatay: Aralık kontratı 2 Kasım'da 227,95. Domuz 52,6 ile YTD -%38, maxdd -%50.
- **Kereste.** Kereste 530-537 $ ile 1 ayın zirvesinde. Ekim konut başlangıçları +%9,9.
- **Önümüzdeki haftalar.** 26 Kasım Şükran Günü tatili, 27 Kasım kısa seans. 30 Kasım sezonun son Crop Progress raporu. 10 Aralık WASDE. Aralık Fed toplantısı. Aralık Cattle on Feed ve Hogs and Pigs. Ocak 2027 başında yıllık üretim ve Grain Stocks raporları (bellek).

## Tuzaklar

1. **Yahoo "=F" sürekli kontratları.** Vade değişiminde sahte getiri sıçramaları üretir. OJ=F, ZO=F, ZR=F ve LBR=F'de gece ve gün içi ortalamaların zıt işaretli ve büyük olması (OJ +18 / -25 bps) bayat ya da hatalı veri belirtisidir. Backtest için ya uzlaşma fiyatı ya da ETF kullanılmalı.
2. **Likidite.** SOYB, TAGS, CUT ve WOOD'un günlük hacmi 1 mn $'ın altında. Alış-satış farkı 1-3 günlük getirinin önemli bir kısmını yiyebilir.
3. **Limit hareketler.** Canlı sığır Kasım 2025'te limit düştü. Limitte kalan vadeli fiyatı gerçek fiyatı göstermez.
4. **TSN'in yönü sezgiye ters.** Sığır pahalanınca TSN zarar eder. Son 5 günde TSN +%10,7, LE +%1,1.
5. **Kaldıraçlı fonlarda günlük sıfırlama.** CXRN ve WXET 1-3 gün için uygundur, daha uzun tutuldukça oynaklık kaybı büyür.
6. **Vergi formu.** CORN, SOYB, WEAT, CANE ve DBA K-1 verir. CXRN, WXET ve TILL 1099 verir.
7. **Kerestede zaman hizası.** 16:05 ET kapanışı nedeniyle eşzamanlı ilişki öncülük gibi görünebilir.
8. **Tatil ve kısa seans.** Bu günlerde vadeli ile hisse kapanış saatleri arasındaki fark değişir.

## İddia defteri

| İddia | Kaynak URL | Birebir kısa alıntı ya da sayı | Güven |
|---|---|---|---|
| CBOT tahıl uzlaşması 13:14-13:15 CT VWAP | https://www.cftc.gov/filings/orgrules/rule060815cbotdcm001.pdf | "VWAP of the outright between 13:14:00 and 13:15:00 Central Time" (2015 dosyası) | orta |
| WASDE 12:00 ET, 2026 son tarihi 10 Aralık | https://www.cmegroup.com/articles/2026/understanding-major-usda-reports-in-2026.html | "November 10, and December 10, 2026, at 12:00 p.m. ET" | yüksek |
| Crop Progress Pazartesi 16:00 ET, 30 Kasım'a kadar | aynı | "Weekly April 6 2026, through November 30 2026, 4:00 p.m. ET" | yüksek |
| Export Sales Perşembe 08:30 ET | aynı | "each Thursday at 8:30 a.m ET" | yüksek |
| Cattle on Feed / Hogs and Pigs 15:00 ET | https://esmis.nal.usda.gov/sites/default/release-files/rj430453j/5q47rs43b/fn107254s/USDA_NASS_issues_new_release_date_for_December_Cattle_on_Feed_and_Hogs_and_Pigs_reports.pdf | "Thursday, Dec. 20 at 3:00 pm ET" (2018) | orta |
| ICE yumuşak emtia saatleri (kakao 4:45-13:30, kahve 4:15-13:30, şeker 3:30-13:00, pamuk 21:00-14:20, FCOJ 8:00-14:00) | https://www.ice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf | "8:00 - 14:00 … 4:15 - 13:30 … 4:45 - 13:30 … Sugar No. 11® 3:30 - 13:00 21:00* - 14:20" | orta (PDF bozuk) |
| Kereste 9:00-15:05 CT | https://cmegroup.com/markets/agriculture/lumber-and-softs/lumber_contract_specifications.html | "Monday - Friday: 9:00 a.m. - 3:05 p.m. CT" (arama özeti) | yüksek |
| Canlı hayvan TAS 8:30-13:00 CT (2016) | https://www.cmegroup.com/media-room/press-releases/2016/2/10/cme_group_announcesmeasurestofurtherenhancelivestockmarkets.html | "TAS Futures will be 8:30 am – 1:00pm (Central Time)" | düşük (eski) |
| iPath NIB/BAL/COW/JO kapandı, yeniden açılmayacak | https://www.etf.com/sections/daily-etf-watch/ipath-etn-redemptions-death-knell-wrapper | "no plans to relaunch the products" (arama özeti) | orta (kapanış tarihi doğrulanmadı) |
| CORN K-1 verir, Section 1256 | https://teucrium.com/corn | "CORN issues a K-1 and typically qualifies for Section 1256 tax treatment" | yüksek |
| CANE, SOYB K-1 verir | https://teucrium.com/cane | "CANE issues a K-1 and typically qualifies for Section 1256" | yüksek |
| CXRN 2x günlük mısır, 1099 | https://teucrium.com/cxrn | "1940 Act ETF that seeks 2x the daily return of corn futures" / "1099 (no K-1)" | yüksek |
| WXET 2x günlük buğday, 1099 | https://teucrium.com/wxet | "seeks 2x the daily return of wheat futures" | yüksek |
| TAGS gider oranı çelişkili | https://teucrium.com/hubfs/Teucrium_TAGS_Factsheet.pdf?hsLang=en | %0,18 (bilgi formu, 01/2025); ETFdb %0,13; YCharts %1,00 | düşük |
| ABD buğday üretimi 2026/27: 1.534 mn bu | https://esmis.nal.usda.gov/sites/default/release-files/796142/wasde1126.txt | "Production 1979 1989 1534 1534" | yüksek |
| ABD mısır stoku 2026/27: 1.758 mn bu | aynı | "Ending Stocks 1551 2095 1849 1758" | yüksek |
| Soya yağı biyoyakıt kullanımı 17,8 mlr lb | aynı | "Biofuel 3/ 11758 14900 17800 17800" | yüksek |
| ABD pirinç ekim alanı 2,81'den 2,10 mn akre'ye | aynı | "Area Planted 2.92 2.81 2.10 2.10" | yüksek |
| Kakao: El Niño ile 2026/27 üretiminde %21-25 düşüş uyarısı | https://tradingeconomics.com/commodity/cocoa/news/600828 | "cocoa production could fall between 21% and 25% in the 2026/27 season due to an exceptionally strong El Niño" | orta |
| Kakao sertifikalı stoklar 2,5 yılın zirvesi | https://tradingeconomics.com/commodity/cocoa/news/600828 (arama özeti) | "3,763,466 bags" | orta |
| Brezilya kahvesi rekor 72,5 mn çuval | https://tradingeconomics.com/commodity/coffee | "record 72.5 million bags, 15% above the estimated 63 million bags in 2025/26" | orta |
| Dolar 19 ayın zirvesinde, tahılı baskılıyor | https://tradingeconomics.com/commodity/corn | "The greenback climbed to a 19-month high on growing expectations of an interest-rate hike next month" | orta |
| IGC dünya buğday tahmini 826 mt | https://tradingeconomics.com/commodity/wheat | "raised its 2026/27 global wheat production forecast by 6 million tons to 826 million tons" | orta |
| Çin'in 25 mt soya taahhüdü | https://tradingeconomics.com/commodity/soybeans | "China is nearing its separate commitment to buy 25 million tonnes of US soybeans this year" | orta |
| Pirinç: El Niño ve Asya arzı | https://tradingeconomics.com/commodity/rice | "risk of El Niño-related drought across Southeast Asia" | orta |
| Kereste: Ekim konut başlangıçları +%9,9, Kanada vergisi %24,75 | https://tradingeconomics.com/commodity/lumber | "housing starts unexpectedly surged 9.9%" / "combined anti-dumping and countervailing duties of 24.75%" | orta |
| Canlı sığır Aralık kontratı 227,95 (2 Kasım) | https://www.cmegroup.com/videos/2026/11/02/live-cattle-futures-held-steady-as-cash-prices-fell-11-2-26.html | "December contract falling $5.82 to $227.95" | yüksek |
| Meksika sınırı canlı sığıra kapalı (Haziran 2026) | https://www.agweb.com/markets/market-analysis/cattle-crash-mexican-border-reopen-how-low-will-prices-fall-grains-set-ba (arama özeti) | "border will remain closed to Mexican cattle imports indefinitely" | düşük (Kasım durumu bilinmiyor) |
| Ters tarım ETF'i yok; kakao, kahve ve hayvancılık için ABD ETF'i yok | — | doğrulanmadı (bellek) | düşük |
| DBA gideri ~%0,85, K-1 | — | doğrulanmadı (bellek) | düşük |
