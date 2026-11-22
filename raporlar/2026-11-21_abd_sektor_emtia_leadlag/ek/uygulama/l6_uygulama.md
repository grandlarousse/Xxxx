# L6 · Uygulama: emir türleri, saatler, aracı kurumlar, maliyet

## Özet

Strateji teknik olarak uygulanabilir, ama kurum seçimi sonucu belirler. Kapanış fiyatından işlem için doğru araç "kapanışta piyasa" (MOC) ya da "kapanışta limit" (LOC) emridir: emir kapanış müzayedesinde, backtest'in kullandığı resmi kapanış fiyatından gerçekleşir. Kesim saatleri borsaya göre değişir: NYSE 15:50, Nasdaq MOC 15:55 / LOC 15:58, NYSE Arca 15:59 ET (Türkiye saatiyle kışın 23:50–23:59). Interactive Brokers MOC/LOC destekler ve maliyeti işlem başına 1–2 baz puan (bps; yüzde 0,01) düzeyindedir. Türkiye'deki banka kökenli kurumların %0,25–0,30'luk yüzdesel komisyonu gidiş-dönüşte 50–60 bps eder; işlem başına beklenen 10–50 bps kazancı tamamen siler. Midas'ın emir başına 1,5 dolarlık ücreti 5.000 doların üstündeki pozisyonlarda kabul edilebilir, ama MOC/LOC desteği bulunamadı. 25 bin dolarlık gün içi al-sat (PDT) kuralı 4 Haziran 2026'da kaldırıldı; zaten 1–3 gün taşıma bu kurala girmiyordu.

## Emir türleri ve saatler

**Terimler.** MOC (market-on-close): fiyat sınırı olmadan kapanış müzayedesine katılır, kapanış fiyatından dolar. LOC (limit-on-close): müzayedeye katılır ama yalnız limit fiyatınızdan ya da daha iyisinden gerçekleşir; dolmama riski vardır. Kapanışa yakın normal limit emir: müzayedeye değil sürekli piyasaya gider; alış-satış farkını (spread) ödersiniz, fiyat kapanıştan sapar.

| Borsa (listelendiği yer) | MOC giriş kesimi (ET) | LOC giriş kesimi (ET) | İptal/değişiklik | Kaynak |
|---|---|---|---|---|
| NYSE | 15:50 | 15:50 | 15:50 sonrası yalnız yayımlanan dengesizliğin karşı yönünde giriş; iptal yalnız belgelenmiş hata | Lightspeed rehberi (2019); NYSE belgeleri arama özeti |
| Nasdaq | 15:55 | 15:58 | 15:50'den sonra iptal/değişiklik yok | Nasdaq Closing Cross SSS |
| NYSE Arca (ETF'lerin çoğu) | 15:59 | 15:59 | 15:59 sonrası iptal yok | Lightspeed rehberi (2019); Cboe 2021 Federal Register özeti |
| Interactive Brokers iç kuralı | kapanıştan en az 15 dk önce (≈15:45) | aynı | NYSE emri borsaya 15:45'te iletilir | IBKR MOC sayfası ve SSS (arama özeti) |

Not: NYSE ve Arca saatleri 2019–2021 tarihli kaynaklara dayanıyor; NYSE'nin kendi sayfaları bu oturumda 403 verdi. Canlı hesapta kurumun emir ekranındaki kesim uyarısı esas alınmalı.

**Türkiye saati (TSİ, UTC+3).** ABD yaz saatindeyken kapanış 23:00, kış saatindeyken 00:00 TSİ. ABD kış saati 1 Kasım 2026'da başladı, 14 Mart 2027'de bitecek (doğrulanmadı, bellek; ikinci mart pazarı kuralı). Şu an kış saatindeyiz.

| Adım | Kış (şimdi) TSİ | Yaz TSİ |
|---|---|---|
| Sinyal için veri anlık görüntüsü (ET 15:30–15:40) | 23:30–23:40 | 22:30–22:40 |
| IBKR'de MOC/LOC girişi için son güvenli an (ET 15:45) | 23:45 | 22:45 |
| NYSE / Nasdaq MOC / Arca kesimi | 23:50 / 23:55 / 23:59 | 22:50 / 22:55 / 22:59 |
| Kapanış müzayedesi (ET 16:00) | 00:00 (ertesi takvim günü) | 23:00 |
| 1–3 gün sonra satış için MOC | aynı saatler | aynı saatler |

**Kritik uygulama tuzağı:** Sinyal "lider varlığın bugünkü kapanışı" ile hesaplanıyor ve takipçi aynı kapanışta alınıyorsa, bu canlıda yapılamaz: kapanış fiyatı MOC kesiminden sonra oluşur. İki dürüst seçenek var: (a) sinyali 15:40 ET fiyatıyla hesaplayıp backtest'i de bu anlık görüntüyle yeniden çalıştırmak, (b) sinyali kapanışla hesaplayıp ertesi günün kapanışında işlem yapmak (backtest de bir gün gecikmeli olmalı). Hangisi seçilirse backtest onunla tutarlı olmalı.

**Yarım günler:** 27 Kasım 2026 (Şükran Günü ertesi) ve 24 Aralık 2026'da kapanış 13:00 ET = 21:00 TSİ (NYSE takvimi). Kesimler orantılı olarak öne kayar (ör. NYSE 12:50; doğrulanmadı, bellek). 24 Aralık 2027 tam tatil.

**Takas ve gün içi kuralı:** Takas T+1 (doğrulanmadı, bellek; 28 Mayıs 2024). FINRA, 25 bin dolarlık "pattern day trader" alt sınırını ve gün içi işlem sayımını tümüyle kaldırıp yerine gün içi teminat kuralı getirdi; yürürlük 4 Haziran 2026, kurumlara 20 Ekim 2027'ye kadar geçiş süresi var. Bu stratejide pozisyon gece taşındığı için kural zaten geçerli değildi; ama aynı gün açıp kapatılan bir pozisyon (ör. stop ile çıkış) olursa kurumunuzun geçiş takvimini sorun.

## Aracı kurumlar

| Kurum | ABD hisse/ETF komisyonu | MOC/LOC | Kaldıraçlı ETF | Açığa satış | Kaynak |
|---|---|---|---|---|---|
| Interactive Brokers (Pro Fixed) | 0,005 $/hisse; en az 1 $, en çok işlem tutarının %1'i | Var | Hesap kuruluşuna bağlı (aşağıya bakın) | Var (teminatlı hesapta; ayrıntı bulunamadı) | IBKR komisyon sayfası; IBKR MOC sayfası |
| Interactive Brokers (Pro Tiered) | ≤300 bin hisse/ay: 0,0035 $/hisse, en az 0,35 $, + borsa/takas ücretleri | Var | aynı | aynı | IBKR komisyon sayfası |
| IBKR Lite (0 $) | Yalnız ABD yerleşiklerine | – | – | – | IBKR komisyon sayfası |
| Midas | Emir başına 1,5 $ | Bulunamadı (emir türleri: piyasa, limit, stop, stop limit, iz süren stop) | Bulunamadı | Bulunamadı | getmidas.com/ucretler; Midas Akademi |
| İş Yatırım (TradeMaster Int.) | %0,25; ülke/borsa bazlı asgari tutar; seans dışı ve ALGO emirde +0,5 cent/hisse | Bulunamadı | Bulunamadı | Bulunamadı | Tarife KMT-28082026 |
| İşCep Yurt Dışı (İş Bankası) | %0,25 | Bulunamadı | Bulunamadı | Pay senedinde yok (arama özeti) | İşbank komisyon tablosu 2024 |
| Garanti BBVA Yatırım | Binde 3 (%0,30), asgari 0 $ (8 Haziran 2024 tarifesi) | Bulunamadı; seans sonrası emir verilemiyor | Bulunamadı | Bulunamadı | garantibbvayatirim.com.tr (arama özeti); garantibbva.com.tr |
| Yapı Kredi Yatırım | %0,25, asgari 0,5 $; NYSE ARCA dahil | Bulunamadı | Bulunamadı | Bulunamadı | yapikredi.com.tr |
| Ak Yatırım, Gedik | Bulunamadı (Gedik yurt dışını GTN üzerinden yürütüyor) | Bulunamadı | Bulunamadı | Bulunamadı | gedik.com (arama özeti) |

**IBKR ve AB kuralı (aykırı kanıt):** IBKR, Avrupa Ekonomik Alanı ve İngiltere'deki bireysel müşteriler için "temel bilgi belgesi" (KID) olmayan ABD ETF'lerini engellemek zorunda; ABD ETF ihraççıları genelde KID yayımlamaz. Türkiye bu bölgede değil, ama Türkiye yerleşiklerinin hangi IBKR kuruluşunda açıldığı bu oturumda bulunamadı. Hesap açmadan önce XLE, SOXL gibi bir ETF'e emir ekranında izin olup olmadığını deneyin. Ayrıca kaldıraçlı ETF için ayrı bir işlem izni ve uygunluk testi istenebilir (doğrulanmadı).

**Türk kurumlarında MOC:** Hiçbir Türk kurumunun sayfasında MOC/LOC emri bulunamadı. Bu, "yok" demek değildir; ama yoksa tek seçenek 15:55 ET civarı limit emirdir ve kapanış fiyatına kilitlenmez.

## Maliyet

Örnek: 10.000 $ pozisyon, 50 $'lık ETF (200 hisse). Gidiş-dönüş = alış + satış.

| Kurum | Komisyon (gidiş-dönüş) | bps | 2.000 $ pozisyonda bps |
|---|---|---|---|
| IBKR Fixed | 2 × 1,00 $ | 2 | 10 (asgari 1 $ nedeniyle) |
| IBKR Tiered | 2 × ≈0,70 $ + ücretler | ≈1,5–2 | ≈4–6 |
| Midas | 2 × 1,5 $ | 3 | 15 |
| İş / Yapı Kredi (%0,25) | 2 × 25 $ | 50 | 50 |
| Garanti (%0,30) | 2 × 30 $ | 60 | 60 |

**Alış-satış farkı:** MOC/LOC ile müzayedede tek fiyattan dolarsınız; backtest'in kapanış fiyatına göre spread maliyeti fiilen sıfırdır (müzayede fiyatı etkisi büyük emirlerde ayrı konu). Normal limit/piyasa emriyle her yönde yarım spread ödenir: SPY, XLE gibi likit ETF'lerde 1–2 bps, küçük sektör ve kaldıraçlı ETF'lerde 3–10 bps ve üstü (doğrulanmadı, bellek; canlı kotasyondan kontrol edin).

**Kur çevrimi:** TL→USD çevrimi işlem başına değil, hesaba para girerken ve çıkarken bir kez yapılır; dolarlar hesapta kalırsa işlem maliyetine girmez. Banka kur makası bu oturumda doğrulanamadı.

**Gerçekçi gidiş-dönüş aralığı:** IBKR + MOC: 2–5 bps. Midas + kapanışa yakın limit: 5–25 bps (pozisyon büyüklüğüne ve spread'e göre). Banka kökenli kurum: 52–70 bps.

**Ne zaman biter?** İşlem başına beklenen brüt kazanç 10–50 bps. Kabaca kural: toplam maliyet beklenen kazancın yarısını geçerse istatistiksel avantaj (ve tahmin hatası) payı kalmaz. 10 bps beklentide 5 bps, 50 bps beklentide 25 bps sınır sayılabilir. %0,25'lik yüzdesel komisyon (50 bps gidiş-dönüş) en iyimser senaryoyu bile sıfırlar; bu kurumlarla strateji uygulanmamalı. IBKR ya da hisse başı/emir başı sabit ücretli bir kurum zorunludur.

## Kaldıraçlı ve ters ETF

- **Günlük sıfırlama:** SEC'e göre çoğu kaldıraçlı ve ters ETF hedefini yalnız günlük olarak tutturur; haftalar ve aylar boyunca getiri hedef katın çok dışına çıkabilir. SEC örneği: endeks önce %10 düşüp sonra %10 artınca %1 kaybeder, 2x ETF %4 kaybeder.
- **1–3 gün taşıma:** Sapma küçük ama sıfır değil; oynaklık arttıkça büyür. 1. dalgada ölçülen yıllık erime NUGT −15,4, SOXL −8,5, ERX −8,1 puan (2011–2025) idi; günlük işlem başına bu birkaç bps eder ve doğrudan beklenen kazançtan düşer. Backtest kaldıraçlı ETF'in kendi fiyat serisiyle yapılmalı, "taban getiri × 3" ile değil.
- **Kurallar:** (1) Pozisyon büyüklüğünü taban varlık riskine göre ayarlayın: 3x ETF'te 3.000 $ ≈ 9.000 $ taban riski. (2) Kaldıraçlı ETF'lerde spread ve gece boşluğu üç kat hissedilir. (3) Tek hisse kaldıraçlı ETF'ler SEC tarafından ayrıca uyarılan, bir günden uzun tutulunca sapması büyük ürünlerdir; bu stratejide kullanmayın.
- **Ters ETF ile açığa satış farkı:** Ters ETF'te en çok yatırdığınız kadar kaybedersiniz, ödünç alma ücreti ve teminat çağrısı yoktur, ama günlük sıfırlama erimesi ve yönetim gideri vardır. Açığa satışta kayıp teorik olarak sınırsızdır, teminat hesabı, ödünç alma ücreti ve temettü ödeme yükümlülüğü gerekir; erime yoktur. Türk kurumlarında ABD açığa satışı bulunamadı; pratikte "kısa" bacak için ters ETF tek seçenek olabilir.

## Riskler

- **Gece boşluğu:** Pozisyon kapanışta açılıp gece taşındığı için ertesi açılış fiyatı stop seviyelerini atlayabilir; stop emir gece korumaz.
- **İşlem durdurma (LULD):** Fiyat bantları aşılırsa işlem durur; kapanışa yakın durmada müzayede gecikebilir ya da MOC dolmayabilir (doğrulanmadı, ayrıntı aranmadı).
- **ETF kapanış sapması:** ETF kapanış fiyatı net varlık değerinden (NAV) sapabilir; özellikle emtia ve kaldıraçlı ETF'lerde.
- **Tek hisse haber riski:** Bilanço ve haber ertesi gün 5–20 % boşluk yaratabilir; bilanço günlerini takvimden dışlayın.
- **İptal edilemezlik:** NYSE'de 15:50, Nasdaq'ta 15:50 sonrası MOC/LOC iptal edilemez; yanlış emir düzeltilemez.
- **İnsan hatası ve saat:** Kışın emir penceresi gece 23:45–23:59. Otomasyon (IBKR API) ya da gün içinde girilen, günlük geçerli MOC emri önerilir.
- **Vergi:** Bu bölüm vergiye girmez; ABD stopajı, Türkiye beyanı ve kur farkı için mali müşavire danışın.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| Nasdaq MOC kesimi 15:55 ET | https://www.nasdaqtrader.com/content/productsservices/Trading/ClosingCrossfaq.pdf | "3:55 p.m. ET ... Nasdaq stops accepting MOC orders." | yüksek |
| Nasdaq LOC kesimi 15:58 ET | aynı | "LOC orders may be entered until 3:58 p.m. ET" | yüksek |
| Nasdaq 15:50'den sonra iptal yok | aynı | "Nasdaq continues accepting MOC, LOC and IO orders, but they may not be canceled or modified." | yüksek |
| NYSE MOC/LOC kesimi 15:50 ET | https://download.lightspeed.com/On%20Close%20and%20On%20Open%20Guide.pdf | "Market and Limit On Close Orders and Cancels in NYSE and AMEX symbols may be entered any time up until 3:50 pm ET." | orta (2019) |
| NYSE 15:50 sonrası yalnız dengesizlik karşısı | aynı | "After this time, On Close orders may be entered only on the contraside of a Regulatory Public Imbalance." | orta |
| NYSE Arca MOC/LOC kesimi 15:59 ET | aynı | "Market and Limit On Close Orders may be entered any time up until 3:59pm ET." | orta (2019) |
| NYSE kesimi 15:50 (resmi) | https://www.nyse.com/publicdocs/nyse/NYSE_Auctions_Closing_Process_Fact_Sheet.pdf | 3:50 p.m. (arama özeti; sayfa 403) | orta |
| IBKR: MOC en az 15 dk önce | https://www1.interactivebrokers.com/en/trading/orders/moc.php | "You must submit the MOC order at least 15 minutes prior to the close." (arama özeti) | orta |
| IBKR Fixed 0,005 $/hisse, en az 1 $ | https://www.interactivebrokers.com/en/pricing/commissions-stocks.php | "USD 0.005 ... Minimum per order ... USD 1.00" | yüksek |
| IBKR Tiered 0,0035 $, en az 0,35 $ | aynı | "≤ 300,000 USD 0.0035 ... USD 0.35" | yüksek |
| IBKR Lite yalnız ABD yerleşikleri | aynı | "IBKR Lite ... US Residents Only" | yüksek |
| Midas ABD işlem ücreti 1,5 $ | https://www.getmidas.com/ucretler/ | "Amerikan Borsası ... İşlem Ücreti 1,5 USD*" | yüksek |
| İş Yatırım yurt dışı pay %0,25 | https://www.isyatirim.com.tr/tr-tr/destek/Documents/pdf/komisyon-ve-masraf-tarifesi.pdf | "Uluslararası Pay alım-satım işlemlerinde %0,25 (onbinde yirmi beş) oranında komisyon tahsil edilir." | yüksek |
| İş Yatırım seans dışı/ALGO +0,5 cent | aynı | "pay adedi başına 0,5 (onda beş) cent üçüncü kişi kurum masrafı" | yüksek |
| İşCep yurt dışı pay %0,25 | https://www.isbank.com.tr/contentmanagement/Documents/mevduat-yatirim/2024/iscep-yurt-disi-piyasalar-komisyon-tablosu-24.pdf | "Alım Satım Aracılık Hizmeti %0,25 (Binde iki buçuk)" | yüksek |
| Yapı Kredi ABD %0,25, asgari 0,5 $ | https://www.yapikredi.com.tr/bireysel-bankacilik/yatirim-urunleri/hisse-senetleri/yurt-disi-hisse-senetleri | "NYSE_ARCA 1.00 $ 16:30 - 23:00 %0,25 (Binde 2,5) 0,5 $" | yüksek |
| Garanti BBVA ABD binde 3, asgari 0 | https://www.garantibbvayatirim.com.tr/tr/ucret-ve-komisyonlar | binde 3, 0 USD; 8 Haziran 2024 (arama özeti; sayfa JS) | orta |
| Garanti: ABD'de asgari komisyon yok | https://www.garantibbva.com.tr/tr/kendim-icin/yatirim/yurt-disi-hisse-senedi-islemleri | "ABD Borsalarında Minimum Komisyon Ücreti Yok!" | yüksek |
| FINRA PDT ve 25 bin $ kaldırıldı | https://www.finra.org/rules-guidance/notices/26-10 | "replace in their entirety ... the $25,000 pattern day trader minimum equity requirement" | yüksek |
| Yürürlük 4 Haziran 2026, geçiş 20 Ekim 2027 | aynı | "Effective Date: June 4, 2026; Phase-in Period: Ends October 20, 2027" | yüksek |
| IBKR AEA/İngiltere'de KID'siz ETF engeli | https://www.interactivebrokers.com/support/faq/content/1136192471 | "As a broker, we are required to block trading in a PRIIP if a KID is not available." | yüksek (Türkiye'ye uygulanırlığı belirsiz) |
| Kaldıraçlı ETF günlük sıfırlanır | https://www.investor.gov/publications-research-studies/info-sheets/Leveraged-Inverse-ETFs | "designed to achieve their stated objectives on a daily basis" | yüksek |
| SEC 2 günlük örnek: endeks −%1, 2x −%4 | aynı | "the index lost 1 percent ... while the 2x leveraged ETF lost 4 percent" | yüksek |
| Yarım gün 27.11.2026 ve 24.12.2026, 13:00 | https://www.nyse.com/markets/hours-calendars | "close early at 1:00 p.m. ... Friday, November 27, 2026 ... Thursday, December 24, 2026" (arama özeti) | orta-yüksek |
| Midas'ta piyasa kapalıyken piyasa emrine %3 marj | https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/amerikan-borsasi-piyasa-emirlerindeki-marj-kurali-nedir | %3 (arama özeti) | orta |
| ABD kış saati 1.11.2026–14.3.2027 | – | doğrulanmadı (bellek) | orta |
| Takas T+1 (28.5.2024'ten beri) | – | doğrulanmadı (bellek) | yüksek (bellek) |
