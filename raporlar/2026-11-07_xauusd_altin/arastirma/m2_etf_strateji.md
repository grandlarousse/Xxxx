# m2 — Altın, gümüş ve madenci ETF'lerinde 1–5 günlük stratejiler ve öncülük ilişkileri (Midas ve BIST BYF cephesi)

Hazırlanma tarihi: 07.11.2026. Kapsam: ABD'de işlem gören altın/gümüş/madenci ETF'leri (GLD, IAU, GLDM, SGOL, SLV, GDX, GDXJ, NUGT, JNUG, DUST, JDST, UGL, GLL, AGQ, ZSL), kapalı uçlu fiziki metal fonları (PHYS, PSLV, CEF) ve BIST altın BYF'leri (GLDTR, ZGOLD). Ufuk: 1, 3 ve 5 gün, ABD kapanışından (16:00 ET) kapanışına. Genel altın stratejileri (TSMOM, takvim, olaylar, COT) için r2_kisa_vade_strateji.md dosyasına bakın. Bu dosya ETF'e özgü olanları ele alıyor.

Güven etiketleri: **yüksek** = birincil kaynak (ihraççı belgesi, SEC dosyası, hakemli makale) okundu. **orta** = hakemli kaynağın özeti ya da ihraççı sayfasının arama özeti. **düşük** = pratisyen ya da ikincil kaynak, veya tarihi belirsiz.

---

## 0. Tek bakışta sonuç

1. **ETF cephesinde VİOP'ta olmayan üç gerçek kenar adayı var:**
   - **(a)** Madencilerin altına gecikmeli tepkisi (GDX/GDXJ ← altın).
   - **(b)** Kaldıraçlı madenci ETF'lerinin gün sonu yeniden dengeleme baskısı ve ertesi açılıştaki kısmi dönüşü.
   - **(c)** Gece/gündüz getiri ayrışması.
   - Üçü de **kanıtı orta ya da zayıf** adaylar. Maliyet sonrası hiçbiri kanıtlanmış değil.
2. **GLD'nin NAV'ı 16:00 ET'de değil, LBMA Gold Price PM'de (≈10:00 ET) belirleniyor** (SPDR Gold Trust 10-Q). Bu yüzden 16:00'da görünen "prim/iskonto" büyük ölçüde altının 10:00→16:00 hareketidir, mispricing değildir. Gerçek prim artığı küçük olmalı. Bunu bizim veride test edeceğiz (H19).
3. **Gece etkisi büyük ölçüde veri yanılsaması olabilir.** GDX'te OHLC açılış fiyatıyla gece getirisi yılda ~%30, gerçekçi 09:31 dolumuyla **%8,58** (Quantpedia 2025). Blose ve Gondhalekar (2014) ve Blose, Gondhalekar ve Kort (2018) gece pozitif, gündüz negatif asimetriyi altın vadelisi, London fix, madenci hisseleri, kapalı uçlu fonlar ve ETF'lerde buluyor. Asimetri "belirgin şekilde zayıflamış".
4. **Kaldıraçlı ETF akışının etkisi istatistiksel olarak var ama ekonomik olarak küçük.**
   - Barbon ve diğ. (2021): hisse senetlerinde 1σ ortak yeniden dengeleme son yarım saate **±2,87 bps** ekliyor. Ortalama kapanış getirisi 0,24 bps. LETF etkisinin **üçte biri ertesi açılışta geri dönüyor.**
   - Ivanov ve Lenkey (2018) ve Lenkey (2024 derleme): para akışları hesaba katılınca etki "ekonomik olarak önemsiz".
   - Madenci LETF'lerinin (NUGT, DUST, JNUG, JDST) 2026 büyüklüğüyle +%1'lik bir GDX gününde zorunlu alım kabaca **27–30 milyon $**.
5. **Kaldıraçlı ETF aşınması 1–5 günde küçük, ama ters ETF'lerde üç kat.** Avellaneda–Zhang formülüyle GDX oynaklığı %40 ise 5 günde aşınma 2x ETF'te **−%0,32**, −2x ETF'te **−%0,95**. GDXJ oynaklığı %50 ise −%0,50 ve −%1,49.
6. **ETF akışları büyük olasılıkla fiyatı takip ediyor, öngörmüyor.**
   - WGC (Ocak 2023): vadeli pozisyonlanma Kuzey Amerika ETF akışlarına öncülük ediyor (Granger F=7,93, p=0,000). Ters yön yok (F=0,38, p=0,68).
   - Brown, Davies ve Ringgenberg (2021, RoF) genel ETF örnekleminde yüksek akışın **sonraki getiriyi düşürdüğünü** buluyor: uzun-kısa portföy ayda %1,1–2,0.
7. **Midas'ın kendi sitesinde doğrulanan maliyet:** ABD'de emir başına **1,5 $**, gidiş-dönüş 3 $. 10.000 $'lık pozisyonda bu 3 bps, 2.000 $'da 15 bps. GLD/IAU/GLDM'nin medyan alış-satış farkı ~1 bps (ikincil kaynak, Ağustos 2026).
8. **Midas'ta bulunamayanlar:** TL→USD kur makası, kaldıraçlı/ters ETF'lerin açık olup olmadığı, açığa satış, kapanış (MOC) emri. Uygulamadan kontrol edilmeli.
9. **Vergi farkı VİOP lehine.**
   - Yurt dışı ETF satış kazancı TL bazında hesaplanıyor ve **kur farkı dahil** artan oranlı tarifeyle (%15–40) beyan ediliyor (Yapı Kredi 2026 notu, GVK mük. 80–81).
   - VİOP'ta %10 stopaj var (r1).
   - BIST altın BYF'lerinde 09.07.2025 sonrası alımlara **%17,5 stopaj** uygulanıyor (ikincil kaynak, CBK 10041).
10. **Pratik engel:** ABD kapanışı kışın **00:00 TSİ**, yazın 23:00 TSİ. Midas'ta MOC emri doğrulanamadı. "Kapanıştan kapanışa" ETF trade'i ya gece yarısı limit emriyle ya da VİOP uzlaşmasıyla aynı saatte (18:05–18:15 TSİ = 10:05–10:15 ET kış) ABD seans içi işlemle yapılabilir. Test bu iki zaman damgasıyla ayrı yapılmalı.

---

## 1. Zaman çizelgesi (07.11.2026 itibarıyla kış: ET = UTC−5, TSİ = UTC+3; ABD yaz saati 8 Mart 2027'de başlıyor)

| Olay | ET | UTC (kış / yaz) | TSİ (kış / yaz) | Kaynak |
|---|---|---|---|---|
| ABD pre-market (borsa tanımı) | 04:00–09:30 | 09:00–14:30 / 08:00–13:30 | 12:00–17:30 / 11:00–16:30 | Midas Akademi |
| ABD normal seans | 09:30–16:00 | 14:30–21:00 / 13:30–20:00 | 17:30–00:00 / 16:30–23:00 | Midas destek (yaz saatiyle 16:30–23:00 TSİ) |
| ABD 08:30 verileri (CPI, NFP) | 08:30 | 13:30 / 12:30 | 16:30 / 15:30 | r2 |
| LBMA Gold Price PM (GLD/IAU/GLDM NAV'ı) | 10:00 (yılda ~3 hafta 11:00) | 15:00 / 14:00 | 18:00 / 17:00 | GLD 10-Q, iShares 10-K, IBA |
| VİOP F_XAUUSD uzlaşma penceresi | 10:05–10:15 (kış) / 11:05–11:15 (yaz) | 15:05–15:15 (her iki mevsim) | 18:05–18:15 | r1, r2 |
| COMEX GC günlük settlement | 13:29–13:30 | 18:30 / 17:30 | 21:30 / 20:30 | r2 (CME) |
| FOMC kararı / basın toplantısı | 14:00 / 14:30 | 19:00 / 18:00 | 22:00 / 21:00 | r2 |
| VİOP akşam seansı sonu | 15:00 (kış) / 16:00 (yaz) | 20:00 | 23:00 | r1 |
| ABD kapanışı, NYSE Arca kapanış müzayedesi | 16:00 | 21:00 / 20:00 | 00:00 / 23:00 | — |
| GLD yaratma/itfa emir kesimi | 15:59:59–16:00 | 21:00 / 20:00 | 00:00 / 23:00 | GLD prospektüs ve emir formu (çelişkili, §3.9) |
| ASX (Avustralya madencileri, GDX'in ~%8,6'sı) | 18:00/19:00–00:00/01:00 (önceki gün) | 23:00–05:00 (AEDT) / 00:00–06:00 (AEST) | 02:00–08:00 / 03:00–09:00 | Borsa saatleri; VanEck ülke ağırlığı |
| Şanghay Altın Borsası gündüz | 20:00–02:30 (önceki gün) | 01:00–07:30 | 04:00–10:30 | r2 |
| Midas uzatılmış saatler (yaz saatine göre yayımlanmış) | — | — | Pre 11:00–16:30, Post 23:00–03:00, Gece 03:00–11:00 | Midas destek (arama özeti), Midas haber 15.06.2023 |

**Not (Midas saatleri):** Midas'ın 15.06.2023 tarihli duyurusu ve arama özetindeki destek sayfası saatleri **yaz saatine göre** veriyor. Kışın ABD saatleri bir saat kaydığı için uygulamadaki saat muhtemelen +1 saattir. Bir Midas sayfası pre-market'i 12:00–16:30 diye yazıyor, yani sayfalar tutarsız. Uygulamadan teyit edin. Gece ve uzatılmış seanslarda **yalnızca limit emir** geçiyor. "Kâr al/zarar durdur" yalnızca normal seansta çalışıyor. https://www.getmidas.com/midasin-kulaklari/midasta-gunler-uzuyor-uzatilmis-islem-saatleri-simdi-midasta-p-22615 , https://www.getmidas.com/midas-akademi/abd-acilis-oncesi-islemler-ve-kapanis-sonrasi-pre-market-post-market-nedir/

---

## 2. Araçların yapısı (strateji tasarımını belirleyen gerçekler)

### 2.1 Fiziki altın/gümüş ETF'leri (grantor trust)

- **GLD (SPDR Gold Trust):**
  - **NAV:** Trustee NAV'ı "**LBMA Gold Price PM veya 12:00 New York saatinden hangisi önceyse**" o andaki değerle belirliyor. PM fiyatı yoksa en son LBMA fiyatı (AM veya PM) kullanılıyor.
  - **Pay başına NAV:** NAV, NYSE Arca kapanışındaki pay sayısına bölünüyor.
  - **Sponsor ücreti:** yıllık %0,40.
  - **Sepet:** 100.000 pay.
  - **31.12.2024 rakamları:** NAV/pay 241,00 $, piyasa fiyatı 242,13 $, 303,8 milyon pay, 28.052.231,5 ons. Pay başına **0,0923 ons** (hesap).
  - **Güven: yüksek.** https://www.sec.gov/Archives/edgar/data/1222333/000143774925002865/gld20241231_10q.htm
- **IAU (iShares Gold Trust):** Trustee altını "o günün LBMA Gold Price PM"iyle değerliyor. PM yoksa en son AM kullanılıyor (10-K, arama özeti). Güven: orta. https://www.sec.gov/Archives/edgar/data/1278680/000143774923004329/iau20221231_10k.htm
- **GLDM:** Administrator LBMA Gold Price PM bazında değerliyor. PM 12:00 NY'ye kadar açıklanmazsa en son LBMA fiyatı kullanılıyor (GLDM SSS, arama özeti). Güven: orta. https://www.spdrgoldshares.com/media/GLD/file/GLDM/GLDM-FAQs-December-2025.pdf
- **Ücretler (ikincil kaynak, Ekim 2026):** GLDM %0,10, SGOL %0,17, IAU %0,25, GLD %0,40. 1–5 günlük tutuşta etkisi önemsiz: GLD için günde ~0,16 bps. GLDM, GLD ve IAU'nun 30 günlük medyan alış-satış farkı Ağustos 2026 sonunda **%0,01**. Güven: düşük. https://247wallst.com/investing/2026/07/05/gold-is-up-again-in-2026-and-after-reviewing-every-way-to-own-bullion-these-3-etfs-cover-the-trade-at-three-cost-levels/
- **Strateji sonucu:**
  - 16:00 ET kapanış fiyatı ile NAV arasında altı saatlik bir zaman farkı var. "Prim" ölçerken NAV'ı değil, 16:00'daki spot altını referans alın.
  - Ivanov (2013, JEF 37(3):453–462): gün içi veride ETF'lerin varlığı altın ve gümüşte **fiyat keşfini ETF piyasasına kaydırmış**. Bu dakika ölçeğinde bir bulgu, 1–5 günle ilgisi yok. Güven: orta. https://ideas.repec.org/a/spr/jecfin/v37y2013i3p453-462.html

### 2.2 Madenci ETF'leri

- **GDX ülke ağırlıkları (VanEck, 30.09.2026):** Kanada %47,95, ABD %21,89, **Avustralya %8,60**, Brezilya %5,53, Güney Afrika %4,67.
  - Avustralya payları ASX'te işlem görüyor ve ABD seansında kapalı. Bu GDX'te **bayat bileşen** demek.
  - Güven: orta (arama özeti). https://www.vaneck.com/us/en/investments/gold-miners-etf-gdx/overview/
- **GDXJ'nin 17.06.2017 endeks değişikliği:**
  - Fon endeksine göre çok büyüdüğü için kapsam genişletildi: bileşen sayısı 48'den 69'a, ağırlıklı ortalama piyasa değeri 967 milyon $'dan 1,7 milyar $'a çıktı.
  - GDX ile 37 ortak hisse var, ama GDXJ ağırlığının %66'sı GDX'te yok.
  - **2017 öncesi ve sonrası GDXJ verisi aynı "genç madenci" serisi değil.** Testler 17.06.2017'de bölünmeli.
  - Güven: orta. https://www.etf.com/sections/news/popular-gold-miner-etf-change-dramatically , https://www.marketvector.com/news/index-updates/marketvector-indexes-announces-rule-changes-for-the-mvgdxj-index
- **Büyüklük (tarihsiz):** GDX ~27,6 milyar $, GDXJ ~10,0 milyar $. Güven: düşük. https://www.bestetf.net/etf/DUST/

### 2.3 Kaldıraçlı ve ters ETF'ler

- **NUGT/DUST (GDX endeksi ±2x) ve JNUG/JDST (GDXJ endeksi ±2x), Direxion:**
  - NUGT ve JNUG **31.03/01.04.2020 civarında 3x'ten 2x'e** indi. İsim değişikliği 19.05.2020. 24.03.2020'de maruziyet geçici olarak %260'a, ertesi gün ~%220'ye düşürülmüştü.
  - **Kaldıraç rejimi 2020'de kırılıyor**, testlerde ayrı ele alınmalı.
  - Güven: orta. https://www.etf.com/sections/news/direxion-ratchets-down-geared-etfs , https://benzinga.com/news/20/12/18726460/the-3x-gold-trade-is-back
  - Direxion ürün sayfası 403 verdi, birincil sayfadan doğrulanamadı.
- **2026 büyüklükleri (aracı siteler, farklı tarihler):**
  - NUGT: 828 milyon $ (08.06.2026), 1,02 milyar $ (30.04.2026), 1,2 milyar $ (Eylül 2026).
  - JNUG: 495–650 milyon $.
  - DUST: 110–170 milyon $.
  - JDST: ~40 milyon $.
  - Güven: düşük. https://ycharts.com/companies/NUGT/total_assets_under_management , https://ycharts.com/companies/JNUG/total_assets_under_management , https://www.bestetf.net/etf/DUST/
- **UGL/GLL (altın ±2x), AGQ/ZSL (gümüş ±2x), ProShares Trust II:**
  - Vadeli kontrat tabanlı. **Vergi açısından ortaklık (Schedule K-1)** sayılıyorlar (SEC POS AM).
  - ABD'de yabancıların PTP satışlarında brütten %10 stopaj (IRC 1446(f), 01.01.2023'ten beri) gündeme geliyor. ProShares'in 22.02.2023 tarihli "qualified notice"ı bu dört fon için **"%10 istisnası"nın 07.12.2022 itibarıyla geçerli olduğunu** söylüyor. Güncel bildirim bulunamadı.
  - Gider oranı %0,95 (aracı siteler).
  - Güven: orta. https://www.proshares.com/globalassets/proshares/documents/qualified-reports/pst_ii_qualified_report_022223.pdf , https://www.sec.gov/Archives/edgar/data/1415311/000119312524062361/d740797dposam.htm , https://www.eisneramper.com/insights/blogs/financial-services/broker-withholding-ptp-fs-blog-0623/
  - **Pratik:** Türk yatırımcı için NUGT/DUST/JNUG/JDST (1940 Act fonları) bu açıdan daha temiz. UGL/GLL/AGQ/ZSL'de aracı kurumun 1446(f) uygulamasını Midas'a sorun.

### 2.4 Kapalı uçlu fiziki fonlar

- **PHYS (Sprott Physical Gold Trust):**
  - **Aylık fiziki itfa** hakkı var. Asgari miktar bir London Good Delivery külçesi (~400 ons). Bildirim ayın 15'inde saat 16:00'ya (Toronto) kadar verilmeli.
  - Teslimat, ilgili SEC dosyasına göre ay sonundan ~10 iş günü sonra.
  - **Arbitraj yavaş ve büyük ölçekli.** Perakende için iskonto kapanışını zorlayacak bir mekanizma yok.
  - Güven: orta. https://sprott.com/investment-strategies/physical-bullion-trusts/how-to-redeem/
- **PHYS iskontosu:**
  - 07.08.2026'da −%2,33. 12 aylık ortalama −%2,08. Kuruluştan beri +%23,88 ile −%3,58 arası.
  - MER %0,39.
  - ATM ihraç programı Aralık 2024'te 1 milyar $'a genişletildi. "Yalnızca primde ihraç" kuralı **doğrulanamadı**.
  - Güven: düşük–orta (arama özeti; Sprott sayfaları 500 verdi). https://sprott.com/investment-strategies/physical-bullion-trusts/gold/
- **PSLV iskontosu:**
  - 2025'te 250 günün tamamı iskontoda geçti, primli gün yok. 2026'nın Ç1–Ç3'ünde de tüm günler iskontoda.
  - Kuruluştan beri +%33,91 ile −%10,34 arası.
  - 02.10.2026'da ~−%5,0. CEFConnect 02.11.2026'da −%5,74 ve 1 yıllık ortalama −%4,87 veriyor.
  - Güven: düşük–orta. https://sprott.com/investment-strategies/physical-bullion-trusts/silver/ , https://www.cefconnect.com/fund/PSLV
- **CEF (Central Fund of Canada):** 2018'de Sprott bünyesine geçti, bugün "Sprott Physical Gold and Silver Trust". 2018 öncesi seri farklı bir yapı.

### 2.5 BIST altın BYF'leri

- **GLDTR (QNB Portföy Altın Katılım BYF):** 995/1000 saflıkta fiziki altın tutuyor. Yönetim ücreti yıllık ~%0,47. Sayfada NAV saati, pay başına gram, piyasa yapıcı ve fiziki itfa bilgisi **yok**. Güven: yüksek (ihraççı sayfası). https://www.qnbinvest.com.tr/gldtr
- **ZGOLD (Ziraat Portföy):** BIST Spot Altın Endeksi'ni izliyor, ücret %0,25 (aracı kurum sayfası). Güven: düşük. https://www.gcmyatirim.com.tr/borsa/hisse/zgold-ziraat-portfoy-altin-katilim-borsa-yatirim-fonu
- **Vergi:** Kıymetli maden fonları ve BYF'lerde gerçek kişi stopajı, alım tarihine göre değişiyor:
  - 23.12.2020–30.04.2024 arası: %0
  - 01.05.2024 sonrası: %7,5
  - 01.11.2024 sonrası: %10
  - 01.02.2025 sonrası: %15
  - **09.07.2025 sonrası: %17,5** (CBK 10041)
  - Kaynak bir hukuk bürosu blogu, Resmî Gazete metniyle teyit edilmedi. Güven: düşük–orta. https://hukukcularevi.com/altin-fonu-vergisi-byf-altin-tahvili-kira-sertifikasi-altins1-stopaj/

### 2.6 Midas: doğrulanmış ve bulunamamış koşullar

- **Ücretler (Midas ücret sayfası, tarih yok):**
  - ABD: işlem başı 1,5 $. Fiyatı 1 $'ın altında olup 300 adedi aşan emirlerde her ek adet için 0,005 $.
  - ADR saklama: pay başı 0,01–0,03 $.
  - Dışarı ACATS transferi 25 $, DTC transferi pay başı 5 $.
  - ABD opsiyon: 0–500 kontrat için kontrat başı 1,50 $.
  - **VİOP:** aylık hacmi 0–10 milyon TL olan için %0,05.
  - BIST pay: komisyonsuz.
  - Güven: yüksek. https://www.getmidas.com/ucretler/
- **Uzatılmış saatler:** Ek ücret yok (2023 duyurusu). Midas ana sayfası "Amerikan borsaları Midas'ta hafta içi 24 saat açık" diyor. https://www.getmidas.com/
- **Kısmi pay** var. ABD işlemleri SIPC kapsamında (sayfadaki tutar yazımı hatalı görünüyor). https://www.getmidas.com/blog/yurt-disi-hisse-almak/
- **Piyasa kapalıyken emir:** Piyasa emrine %3, stop emrine %2,5 marj bloke ediliyor (arama özeti).
- **Bulunamadı:**
  - TL→USD kur makası ve dönüşüm ücreti
  - Kaldıraçlı/ters ETF'lerin açık olup olmadığı veya karmaşık ürün testine tabi olup olmadığı
  - ABD'de açığa satış
  - MOC/kapanış emri
  - Takas sonrası nakit kullanımı (T+1) kuralları
  - **Açığa satış yoksa "kısa" görüş yalnızca ters ETF'le (DUST, JDST, GLL, ZSL) alınabilir.** Ters ETF'ler en hızlı aşınanlar (§3.8).
- **Vergi (Yapı Kredi, 01.01.2026 mevzuatı):**
  - Yabancı menkul kıymet satış kazancı **değer artış kazancı** sayılıyor (GVK mük. 80–81).
  - Alış ve satış bedelleri **işlem günlerinin kuruyla TL'ye çevriliyor**. Yİ-ÜFE artışı ≥%10 ise maliyet endeksleniyor.
  - **İstisna ve beyan sınırı yok.** Artan oranlı tarife %15–40.
  - **Kur farkı vergiye tabi:** dolar bazında zarar varken TL bazında kâr çıkabilir.
  - Komisyon gider yazılabiliyor.
  - **Zararlar yalnızca aynı yılın diğer yabancı menkul kıymet kazançlarına** mahsup ediliyor (Maliye basın açıklaması).
  - Güven: orta–yüksek (banka notu). https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view
  - Midas'ın örneği: 150.000 TL kazanç %15 dilimine düşüyor. 2025 ücret geliri ≥4,3 milyon TL ise bu kazançlar %40 dilimine düşebiliyor. https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/yurt-disi-hisse-alim-satim-ve-temettu-gelirlerim-icin-ne-kadar-vergi-odemeliyim
- **ABD tarafı:** Yerleşik olmayanların alım-satım kazancından ABD'de vergi alınmadığını yalnızca ikincil kaynaklar söylüyor. Temettü stopajında ABD–Türkiye anlaşması oranı (%20 genel / %15 doğrudan iştirak) IRS tablosundan **doğrulanamadı**. GLD, IAU ve PHYS temettü dağıtmaz. GDX ve GDXJ yılda bir dağıtım yapar.

---

## 3. Strateji ve öncülük aileleri

Her başlıkta beş alt başlık var: Mekanizma, Kanıt, Yayın sonrası durum, Maliyet sonrası beklenti ve Bizim veride test kuralı. Getiri tanımları:
- r_X(a→b): X'in a anından b anına log getirisi.
- **C_t:** t günü 16:00 ET kapanışı.
- **O9:31_t:** t günü 09:31 ET işlem fiyatı. Dakika verisi yoksa 09:35 VWAP.
- **OHLC açılışı kullanılmayacak** (Quantpedia uyarısı, §3.1).

### 3.1 Gece (C→O) ve gün içi (O→C) getiri ayrışması: GLD, IAU, GDX, SLV

**Mekanizma.** İki açıklama öne sürülüyor:
- Açılışta fiyatın sistematik olarak yüksek oluşması (Blose ve diğ.).
- Asya talebinin ABD gece saatlerinde fiyatı yukarı itmesi (CBS tezi, hakemsiz).

Hisse senetlerinde tartışılan "gece sürüklenmesi" kanalları burada ayrıntılı ele alınmadı.

**Kanıt.**
- **Blose ve Gondhalekar (2014, Applied Economics Letters 21(18):1269–1272):**
  - COMEX ön ay kontratı, 1985–2012. Gece getirisi anlamlı pozitif, gündüz getirisi anlamlı negatif.
  - GLD'de gece getirisi gündüzden anlamlı yüksek.
  - "Asimetri yıllar içinde belirgin şekilde zayıfladı ama hâlâ var."
  - Büyüklük özette yok. Güven: orta. https://ideas.repec.org/a/taf/apeclt/v21y2014i18p1269-1272.html
- **Blose, Gondhalekar ve Kort (2018, J. Economics and Finance 42(3):526–549):**
  - Aynı desen COMEX, London fix spot, **altın madenci hisseleri, altınla ilgili kapalı uçlu fonlar ve ETF'lerde** de var. Yükselen ve düşen piyasada sürüyor.
  - Özete göre "işlem maliyetleri sonrası ekonomik olarak önemli".
  - Tam metin erişilemedi, büyüklükler bulunamadı. Güven: orta. https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html
- **Quantpedia (Dujava, 14.02.2025), GDX:**
  - OHLC verisiyle gece yılda ~%30, gün içi ~−%25 görünüyor.
  - Satış 09:31'e çekilince (QuantConnect 1 dakikalık veri) gece getirisi **yılda %8,58**, oynaklık %16,9, en büyük düşüş −%40,7 (ücret ve kayma öncesi).
  - Neden: OHLC açılışı ilk işlemden geliyor, açılış müzayedesi değil, ve gerçekçi bir dolum fiyatı değil.
  - GLD için "son 20 yılda gün içi performans ihmal edilebilir" deniyor, rakam yok.
  - Güven: orta (pratisyen, şeffaf yöntem). https://quantpedia.com/dangers-of-relying-on-ohlc-prices-the-case-of-overnight-drift-in-gdx-etf/
- **SLV:** Bir R-bloggers analizi (2014 civarı) kümülatif gece +%39,1, gün içi −%36,6 buluyor. Güven: düşük. https://www.r-bloggers.com/2014/01/overnight-vs-intraday-etf-returns/
- **"Altın Asya'da yükselir, NY'de düşer":** CBS yüksek lisans tezi (2019) "şapka şeklinde" gün içi desen raporluyor: Doğu saatlerinde yükseliş, sonrasında düşüş. Hakemsiz. https://research.cbs.dk/en/studentProjects/gold-price-dynamics-around-the-clock/
- **Fiks etkisi:** Caminschi ve Heaney (2014, JFM 34(11):1003–1039), eski PM fiksinin GC ve **GLD** üzerinde maddi etkisi olduğunu ve bilginin açıklamadan önce sızdığını buluyor (2015 öncesi telefonlu fiks). https://ideas.repec.org/a/wly/jfutmk/v34y2014i11p1003-1039.html

**Yayın sonrası.** Yazarlar 2014'te zayıflamayı kendileri raporluyor. 2015 sonrası elektronik LBMA müzayedesi için ayrı bir çalışma **bulunamadı**.

**Maliyet sonrası.**
- Her gece ayrı bir gidiş-dönüş demek.
- 10.000 $'lık GLD pozisyonunda gecelik maliyet ≈ 3 bps komisyon + ~1 bps spread = **~4 bps**, yılda ~252 × 4 = **~%10**. Bu GDX'in %8,58'lik gece getirisini bile siler.
- 50.000 $'da maliyet ~1,6 bps/gece, ~%4/yıl. Kenar ancak marjinal kalır.
- Kur makası (bulunamadı) ve %15–40 vergi eklenince saf gece stratejisi Midas'ta **cazip değil**.
- **Kullanışlı yanı zamanlama:** 1–5 günlük bir pozisyona girişi ve çıkışı kapanışa veya açılışa koymak.

**Test kuralı.**
- **T1.1:** g_t = r(C_{t−1}→O9:31_t), d_t = r(O9:31_t→C_t). Ortalamaları, HAC t'yi ve yıllık getiriyi 2006–2012, 2013–2019 ve 2020–2026 alt dönemlerinde raporla.
- **T1.2 (giriş zamanlaması):** Aynı 1/3/5 günlük sinyal için iki uygulamayı karşılaştır. (a) C_t'de gir, C_{t+h}'de çık. (b) C_t'de gir, O9:31_{t+h}'de çık. Fark = b − a. Beklenti: fark > 0, yani sinyalin son gün içi parçasını atlamak kazandırır.
- **T1.3:** Gece getirisini Asya (SGE gündüz 01:00–07:30 UTC) ve Londra (07:00–14:30 UTC) dilimlerine ayır. XAUUSD saatlik veriyle hangi dilimin taşıdığını göster.

### 3.2 GLD/GDX'te kısa vadeli dönüş ve RSI(2) / Connors

**Mekanizma.** Likidite sağlayıcılar geçici fiyat baskısının tersine pozisyon alır.

**Kanıt.**
- Kurallar Connors ve Alvarez (2008) ve Connors'ın *High Probability ETF Trading* (2009) kitabından geliyor: 20 likit ETF'lik bir sepet. **GLD'nin ayrı sonucu bulunamadı.**
- Hakemli bir GLD veya GDX RSI(2) testi **bulunamadı**. Dolaşan "GLD'de işlem başı %1,5" iddiası kural tanımsız ve doğrulanamadı (r2 §3.2).
- Emtiada saf dönüş stratejilerinin tutarlı biçimde kârsız olduğu kaydı için r2'deki Bianchi, Drew ve Fan (2015) özetine bakın.

**Maliyet sonrası.** Sinyal başı ortalama getiri birkaç bps düzeyindeyse Midas'ta 4 bps'lik gidiş-dönüş maliyeti sınırda kalır. 5 günlük çıkışta daha makul. Beklenti sıfıra yakın.

**Test kuralı.**
- **T2.1:** Wilder RSI(2)_t < 10 ve C_t > SMA200 ise C_t'de uzun. Çıkış C > SMA5 olduğunda veya h = 5 dolunca. GLD, GDX, GDXJ ve SLV için ayrı ayrı.
- **T2.2 (madenci artığı dönüşü):** e_t = r_GDX,t − β̂_60·r_GLD,t. e_t en alt %10'da ise ertesi 1–5 günün e toplamı.
- **T2.3:** Aynı kuralı VİOP F_XAUUSD'de uygula (r2). Kenar ETF'e özgü mü, altına mı ait, bunu ayırt et.

### 3.3 Trend ve momentum

**Kanıt ve kurallar r2 §3.1'de.** ETF'e özgü tek fark kaldıraçlı ETF'lerde ortaya çıkıyor: trend dönemlerinde günlük yeniden dengeleme "yükselişte daha çok al, düşüşte sat" etkisi yaratır ve yapı trendde kazandırır, yataydaki oynaklıkta kaybettirir (§3.8).

**Test kuralı.** **T3.1:** TSMOM sinyali (r2) ile GLD'ye karşı NUGT'yi karşılaştır. Aynı sinyalde NUGT − 2·GDX farkını gerçekleşen varyansa regres et (§3.8 formülü).

### 3.4 Madenciler ↔ altın: kim öncü, beta ve kaldıraç

**Mekanizma.**
- **Altın → madenci:** İşletme kaldıracı. Kâr = (altın − maliyet) × üretim, dolayısıyla madenci getirisi altının ~2 katı. Hisse piyasası bilgiyi yavaş sindirirse bir gecikme oluşur.
- **Madenci → altın:** Hisse yatırımcısı altın görüşünü önce madencide ifade eder. Bunu pratisyen anlatısı öne sürüyor.

**Kanıt.**
- **Tufano (1998, JF 53(3):1015–1052):** Kuzey Amerika madencileri, 1990'ların başı. **Altındaki %1'lik hareket ortalama madenci hissesini ~%2 oynatıyor.** Maruziyet zamanla ve firmaya göre değişiyor. Altın fiyatı ve oynaklığı yükseldikçe, çeşitlendirme ve hedge arttıkça maruziyet düşüyor. Güven: orta (özet ve tablo alıntısı). https://zendy.io/title/10.1111/0022-1082.00042
- **Lucey ve O'Connor (2017, AEL 24(2):90–94), "Are Gold Bugs Coherent?":**
  - Ocak 1998 – Kasım 2015, günlük COMEX altın ve NYSE Arca Gold Bugs (HUI), dalgacık analizi.
  - **Altın vadelisi madencilere çoğunlukla en az bir hafta öncülük ediyor.** İlişki 1 yıl ve üzeri ölçekte daha güvenilir.
  - **Çok kısa aralıklarda madenci getirilerini altın dışı faktörler belirliyor.**
  - Güven: orta. https://ideas.repec.org/a/taf/apeclt/v24y2017i2p90-94.html , https://www.cxoadvisory.com/gold/gold-futures-vs-gold-miner-stocks/
- **Ters yön:** Bir kantil nedensellik çalışması (Resources Policy, 2016–17) "altın hisse getirilerinden altın fiyatına tutarlı kantil nedensellik" buluyor, ters yön karışık. Tam metin 403 verdi, yazar ve örneklem doğrulanamadı. Güven: düşük. https://www.sciencedirect.com/science/article/abs/pii/S0301420716304081
- **Pratisyen:** Seeking Alpha'nın XAU/HUI incelemesi dönüm noktalarında madencilerin öncü olduğu örnekler kadar geride kaldığı örnekler de buluyor. Yani **"madenciler altını önden gösterir" desteklenmiyor**. Güven: düşük. https://seekingalpha.com/article/4318023-do-gold-mining-stocks-lead-gold
- **GDX'in 2026 altın betası:** Birincil kaynak **bulunamadı**. ETF.com 2025'te GDX getirisinin spot altının iki katı olduğunu yazıyor: bu bir getiri karşılaştırması, beta değil. https://www.etf.com/sections/data-dive/gdx-stock-vs-gold-price-miner-etf

**Yayın sonrası.** Lucey ve O'Connor örneklemi 2015'te bitiyor. Sonrası test edilmeli.

**Maliyet sonrası.** Gecikme 1–5 gün ölçeğinde varsa GDX'te alınabilir. Gerekli işlem sayısı düşük: yalnızca büyük altın günlerinde. Kenar hakkında kesin bir şey söylenemez.

**Test kuralı.**
- **T4.1 (altın → GDX):** r_GDX(C_t→C_{t+h}) = a + b·r_XAU(C_{t−1}→C_t) + c·r_GDX(C_{t−1}→C_t) + u. b > 0 ve anlamlıysa gecikme var. XAU yerine 16:00 ET spot ya da GLD kullan.
- **T4.2 (GDX → altın):** r_GLD(C_t→C_{t+h}) = a + b·e_t + c·r_GLD,t, e_t = GDX'in altına göre artığı. Ayrıca e_t'yi VİOP'ta bir sonraki uzlaşmadan uzlaşmaya getiriye (ertesi gün 15:15 UTC'ye) regres et. Bu, Midas'ta bilinen bir bilgiyle VİOP'u öngörme testi.
- **T4.3 (beta rejimi):** β_60 = cov(r_GDX, r_GLD) / var(r_GLD). β_60'ın 3 yıllık dağılımda üst veya alt %20'de olmasının T4.1'deki b'yi değiştirip değiştirmediğine bak.
- **T4.4 (oran):** z = (ln(GDX/GLD) − SMA60) / SD60. z < −2 ise GDX − β·GLD (β-nötr) 5 gün. Midas'ta açığa satış yoksa yalnızca uzun GDX olarak uygulanır. Kısa bacak VİOP'ta F_XAUUSD satılarak kurulabilir. Bu iki platformlu, β-nötr bir yapı olur ve zaman farkı (10:15 ve 16:00 ET) ayrıca hesaplanmalı.

### 3.5 GDXJ ↔ GDX gecikmesi (büyük → küçük)

**Mekanizma.** Endüstri bilgisi küçük ve az izlenen firmalara yavaş yayılır.

**Kanıt.**
- **Hou (2007, RFS 20(4):1113–1138):** Büyükten küçüğe lead-lag **ağırlıkla endüstri içi** bir olgu. Küçük, az rekabetçi ve az izlenen endüstrilerde daha güçlü. **Olumsuz bilgiye yavaş uyumdan** kaynaklanıyor. Güven: orta. https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html
- GDX→GDXJ için ETF'e özgü bir çalışma **bulunamadı**.

**Yayın sonrası ve yapısal not.** 2017 endeks genişlemesi GDXJ'yi büyük firmalara yaklaştırdı (§2.2), bu gecikmeyi azaltmış olmalı. Ayrıca ETF ve bileşenleri aynı anda işlem gördüğü için ETF seviyesinde gecikme hisse seviyesindekinden zayıf olur.

**Test kuralı.**
- **T5.1:** r_GDXJ(C_t→C_{t+1}) = a + b·r_GDX,t + c·r_GDXJ,t + u. Beklenti b > 0.
- **T5.2:** Asimetri için r_GDX,t < 0 günlerini ayrı al (Hou'nun öngörüsü).
- **T5.3:** 17.06.2017 öncesi ve sonrası ayrı.

### 3.6 Gümüş ↔ altın

**Mekanizma.** Ortak makro faktör. Gümüşün sanayi bileşeni ve daha yüksek betası.

**Kanıt.**
- Uzun dönem ilişki istikrarsız. Ciner (2001, Global Finance Journal 12:299–303) TOCOM 1992–1998'de istikrarlı bir eşbütünleşme bulamıyor. Lucey ve Tully bunu daha uzun veriyle sorguluyor. İkincil kaynak, güven orta. https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp55.pdf
- **Günlük ufukta altın–gümüş öncülüğünü test eden hakemli bir çalışma bulunamadı.** Çin vadelilerinde ABD gümüş vadelisinin fiyat keşfinde baskın olduğu söyleniyor (Jiang, Kellard ve Liu 2020, JFM). https://econpapers.repec.org/RePEc:wly:jfutmk:v:40:y:2020:i:10:p:1486-1507

**Test kuralı.**
- **T6.1:** r_SLV(C_t→C_{t+1}) = a + b·r_GLD,t + c·r_SLV,t, ve tersi.
- **T6.2:** GSR = GLD/SLV fiyat oranı (ons başına normalleştirilmiş), 60 günlük z. |z| > 2 ise oranın tersine (SLV uzun ve GLD kısa, ya da tersi), h = 5. Midas'ta kısa bacak yoksa yalnızca uzun bacak, ya da VİOP F_XAGUSD/F_XAUUSD ile.
- **T6.3:** AGQ ve ZSL'nin aşınması gümüşte daha büyük (§3.8).

### 3.7 Kaldıraçlı ETF gün sonu yeniden dengeleme akışı: gün sonu momentum ve ertesi gün dönüş

**Mekanizma.** Kaldıraç L, NAV A ve günlük getiri r olan bir fonun gün sonunda yapması gereken alım:
- Getiri sonrası maruziyet L·A·(1+r), yeni NAV A·(1+L·r), hedef maruziyet L·A·(1+L·r).
- Fark = **A·(L² − L)·r** (Cheng ve Madhavan 2009 formülü).
- L = 2 için 2·A·r, L = −2 için **6·A·r**. Yani hem uzun hem ters fonlar **yükselen günde alır, düşen günde satar**.
- Bu akış kapanışta (swap'lar kapanış fiyatıyla işaretleniyor) gerçekleşir.

**Kanıt.**
- **Cheng ve Madhavan (2009, Journal of Investment Management 7(4):43–62):** LETF'lerin toplam yeniden dengeleme talebi S&P 500 gün sonu getirisine baskı yapıyor. Formül yukarıdaki. Tam metin erişilemedi. Güven: orta. https://www.joim.com/the-dynamics-of-leveraged-and-inverse-exchange-traded-funds/
- **Tuzun (2013, Fed FEDS 2013-48):**
  - Aralık 2011 itibarıyla geniş endeksteki %1'lik hareket **1,04 milyar $** yeniden dengeleme akışı üretiyor. Bu günlük hisse hacminin ~%0,79'u.
  - Son saatte büyük hisselerde hacmin %2–3'ü, küçüklerde %18'e kadar.
  - %1'lik endeks gününde gün sonu fiyat etkisi: büyük hisse ~6,9 bps, finansal hisse ~13 bps.
  - **Ertesi gün getirisinde gecikmeli akış katsayısı negatif**, yani kısmi dönüş var.
  - Güven: yüksek. https://www.federalreserve.gov/pubs/feds/2013/201348/
- **Shum, Hejazi, Haryanto ve Rodier (2016, Review of Finance 20(6):2379–2409):** 2006–2011. Gün sonu oynaklığı, potansiyel yeniden dengeleme/hacim oranıyla pozitif ve anlamlı ilişkili. Etkiler hep ekonomik olarak önemli değil, en büyükleri oynak günlerde. Güven: orta. https://ideas.repec.org/a/oup/revfin/v20y2016i6p2379-2409..html
- **Bai, Bond ve Hatch (2015, Real Estate Economics 43:37–66):** 6 gayrimenkul LETF'i, 63 hisse. Son saatte artan oynaklık, hacim ve **getiri devamı**. Etki küçük ve oynak hisselerde. Güven: orta. https://ideas.repec.org/a/bla/reesec/v43y2015i1p37-66.html
- **Barbon, Beckmeyer, Buraschi ve Moerke (2021, HSG WP 2021/14; 2022 sürümü SFI 22-40):**
  - Örneklem: Ocak 2012 – Aralık 2019 (ortak örneklem). Gamma verisi Mayıs 2005 – Temmuz 2020.
  - LETF varlıkları kaldıraç ayarlı olarak ~40 milyar $'dan (2012) ~130 milyar $'a (2020) çıkmış.
  - Son yarım saat regresyonunda Ω_LETF katsayısı 44,36 (t = 4,56).
  - BB (opsiyon gamma'sı ve LETF aynı yönde alım) günlerinde **1σ ortak yeniden dengeleme son yarım saate +2,87 bps**, SS günlerinde −2,87 bps ekliyor. Ortalama kapanış getirisi 0,24 bps.
  - **Ertesi açılışta delta-hedge etkisinin %82'si, LETF etkisinin %32'si geri dönüyor.**
  - 2021 sürümüne göre LETF etkisi 2012–2019'da sabit. 2022 sürümünün özeti **"LETF etkileri zamanla belirgin şekilde azalıyor"** diyor.
  - Örneklem hisse senetleri. Altın veya madenci LETF'leri ayrıca incelenmemiş.
  - Güven: yüksek (2021 PDF okundu). https://www.alexandria.unisg.ch/server/api/core/bitstreams/5a99db31-0d37-4f86-9502-8cb0f3bff4fe/content , https://ideas.repec.org/p/chf/rpseri/rp2240.html
- **Karşı kanıt:**
  - **Ivanov ve Lenkey (2018, Journal of Financial Markets 41:36–56):** ABD hisse ETF'leri 2006–2014. Para akışları yeniden dengeleme talebini büyük ölçüde azaltıyor, ciddi stres dönemlerinde bile. Gün sonu getiri ve oynaklık etkisi **ekonomik olarak önemsiz**. https://econpapers.repec.org/RePEc:eee:finmar:v:41:y:2018:i:c:p:36-56
  - **Lenkey (2024, QFE 8(4):815–840) derlemesi:** Literatür tutarlı olarak istatistiksel anlamlılık buluyor. Ancak makalelerin çoğunda ciddi yöntem sorunları olabilir ve ekonomik etki önemsiz görünüyor. https://www.aimspress.com/article/doi/10.3934/QFE.2024031
- **Altın madenci LETF'lerine özgü kanıt:**
  - Hakemli bir çalışma **bulunamadı**.
  - Bir blog yazısı (Investing Whisperer, 2020) 2020'de NUGT ve JNUG'un zorunlu kaldıraç azaltımının GDX ve GDXJ'yi aşağı ittiğini iddia ediyor: NUGT haftanın son üç gününde −%23, −%36, −%46. Bu bir iddia, ölçüm değil. Güven: düşük. https://investingwhisperer.com/why-gold-and-gold-stocks-are-collapsing/
  - ETF Trends (Mart 2020) GDX'in iskontosunu, sepetin ~%30'unun ABD saatlerinde işlem görmemesine ve swap'ların kapanışta işaretlenmesine bağlıyor. Sayfa 403 verdi, arama özetinden. https://www.etftrends.com/2020/03/anatomy-of-a-discount-gdx-nugt-dust/

**Büyüklük tahmini (2026, kaba).**
- **GDX ailesi:** NUGT ≈ 1,0 milyar $ ve DUST ≈ 0,11–0,17 milyar $. +%1'lik GDX gününde zorunlu alım ≈ 2·1,0·%1 + 6·0,11..0,17·%1 ≈ **27–30 milyon $**. Bu GDX varlıklarının (~27,6 milyar $) ~%0,1'i.
- **GDXJ ailesi:** JNUG ≈ 0,5–0,65 milyar $ ve JDST ≈ 0,04 milyar $. +%1'de **~12–15 milyon $**.
- 2015–2016'da JNUG 3x ve GDXJ'ye göre çok büyüktü. Etkinin en güçlü olduğu dönem muhtemelen 2014–2017.
- **Bizim veride ölçülecek:** bu akışın GDX ve GDXJ'nin son 30 dakikalık dolar hacmine oranı.

**Maliyet sonrası.**
- Hisse senedinde 1σ etki ±3 bps. Midas'ta 4 bps'lik gidiş-dönüş ve kapanış dolumu belirsizliği varken bunu doğrudan trade etmek **olası değil**.
- Daha kullanışlı olan **ertesi gün dönüşü**. Ekstrem günlerde (|r_GDX| > 2σ) dönüş birkaç bps'i aşabilir. Test edilmeli.

**Test kuralı.**
- **T7.1:** Ω_t = Σ_i A_i,t−1·(L_i² − L_i)·r_GDX(09:30→15:30)_t / ADV$_GDX(son 20 gün). r_GDX(15:30→16:00)_t'yi Ω_t'ye ve r(09:30→15:30)_t'ye regres et. Beklenti: Ω katsayısı > 0.
- **T7.2:** r_GDX(16:00_t→09:35_{t+1}) ve r_GDX(16:00_t→16:00_{t+1})'i Ω_t'ye regres et. Beklenti negatif katsayı (kısmi dönüş).
- **T7.3:** Aynısını GDXJ için JNUG ve JDST ile. 2014–2017, 2018–Mart 2020 (3x) ve Nisan 2020–2026 (2x) olarak üç döneme böl.
- **T7.4 (yalnızca günlük veri varsa):** |r_GDX,t| en üst %10'luk günlerde r_GDX(C_t→C_{t+1}). Beklenti işaret −sign(r_t).
- A_i, ihraççının günlük "shares outstanding × NAV" verisinden. Tarih t−1 kapanışı.

### 3.8 Kaldıraçlı ETF oynaklık aşınması

**Formül.** Avellaneda ve Zhang (2010, SIAM J. Financial Mathematics 1:586–603; 2009 çalışma notu):

L_t/L_0 ≈ (S_t/S_0)^β · exp[ (β − β²)/2 · V_t + β·H_t + ((1 − β)·r − f)·t ]

- V_t: dayanak ETF'in gerçekleşen varyansı.
- H_t: ters fonlarda ödünç alma maliyeti.
- r: finansman faizi.
- f: gider oranı.
- **LETF sahibi gerçekleşen varyansa negatif maruz, β'nın işaretinden bağımsız olarak.**
- Güven: yüksek (PDF okundu). https://math.nyu.edu/~avellane/LeveragedETF20090515.pdf

**Rakamlar.** Hesap aşağıda, oynaklıklar varsayım ve bizim veride ölçülecek.

| Ürün (β) | Varsayılan yıllık σ | 1 gün aşınma | 5 gün aşınma |
|---|---|---|---|
| NUGT (+2, GDX) | %40 | −%0,06 | −%0,32 |
| DUST (−2, GDX) | %40 | −%0,19 | −%0,95 |
| JNUG (+2, GDXJ) | %50 | −%0,10 | −%0,50 |
| JDST (−2, GDXJ) | %50 | −%0,30 | −%1,49 |
| UGL (+2, altın) | %20 | −%0,02 | −%0,08 |
| GLL (−2, altın) | %20 | −%0,05 | −%0,24 |
| AGQ (+2, gümüş) | %35 | −%0,05 | −%0,24 |
| ZSL (−2, gümüş) | %35 | −%0,15 | −%0,73 |

**Finansman terimi.** r = %4 ve f = %1 varsayımıyla 5 günde β = +2 için −%0,10, β = −2 için +%0,22 (ödünç maliyeti hariç).

**Gözlenen uzun vade.** On yıl boyunca (29.09.2025'e kadar) GDXJ +%354, JNUG −%84 (Seeking Alpha). Güven: düşük. https://seekingalpha.com/article/4827566-jnug-primer-on-structure-and-suitability-of-leveraged-etf

**Strateji sonucu.**
- 1–3 günde aşınma uzun 2x ETF için ihmal edilebilir (≤0,2%). Ters 2x ETF'te 5 günde ~%1 civarında.
- **Midas'ta kısa görüşü ters ETF'le alacaksanız h = 1–3 ile sınırlayın.**
- Aşınmadan kazanmak için ikisini birden açığa satmak gerekir. Midas'ta açığa satış bulunamadığı için uygulanamaz.

**Test kuralı.**
- **T8.1:** Her ürün için ln(L_{t+5}/L_t) − β·ln(S_{t+5}/S_t) farkını V_{t→t+5}'e regres et. Eğimin (β − β²)/2'ye eşitliğini test et.
- **T8.2:** Aynı yön sinyalinde h = 1, 3, 5 için LETF ile 1x ETF'in kaldıraç ayarlı getirisini, maliyet dahil karşılaştır.

### 3.9 ETF akışları (GLD dolaşımdaki pay değişimi): öngörür mü, takip mi eder?

**Mekanizma.** İki rakip kanal:
- **(a)** Akış talebi fiziki altın alımıyla fiyata baskı yapar.
- **(b)** Yatırımcı geçmiş getiriyi kovalar (geri besleme). Temel dışı talep sonradan tersine döner.

**Kanıt.**
- **WGC Gold Market Commentary (Ocak 2023):**
  - Haftalık VAR, 20.06.2006–31.01.2023.
  - **Vadeli net uzun pozisyon değişimi Kuzey Amerika ETF akışlarına öncülük ediyor:** gecikme 1 katsayısı 45,03 (t = 3,39). Granger testi vadeli→ETF F = 7,93 (p = 0,000), ETF→vadeli F = 0,38 (p = 0,68).
  - ETF akışının fiyatı öngörüp öngörmediği test edilmemiş.
  - Güven: yüksek. https://www.gold.org/goldhub/research/gold-market-commentary-january-2023
- **Brown, Davies ve Ringgenberg (2021, Review of Finance 25(4):937–972):** ETF yaratma ve itfası temel dışı talep şoklarının sinyali. **Yüksek akışlı ETF'leri satıp düşük akışlıları alan portföy ayda %1,1–2,0** fazla getiri sağlıyor (geri dönüş). Örneklem geniş ETF evreni, altına özgü sonuç bulunamadı. Güven: orta. https://econpapers.repec.org/RePEc:oup:revfin:v:25:y:2021:i:4:p:937-972.
- Bir NCHU yüksek lisans tezi (2012), geçmiş 1–3 gün altın getirisi iyiyse yatırımcının GLD aldığını (geri besleme) buluyor. Güven: düşük. https://ndltd.ncl.edu.tw/handle/79415745161990386644
- **GLD'nin kendi notu (SEC FWP, 2013):** 11 Nisan 2013'e kadar 43 seans boyunca tutulan altın azaldı ya da sabit kaldı. 1 Ocak–11 Nisan arasında tutulan miktar %13 düşerken altın %6'dan az düştü. Hemen ardından 12 Nisan'da ~%5, 15 Nisan'da ~%10 düşüş geldi. Bu bir anekdot, nedensellik kurmuyor. https://www.sec.gov/Archives/edgar/data/1222333/000119312513201018/d532866dfwp.htm
- Deutsche Bank (Tickmill aktarımı) ve bir Aalto tezi fiyatın akışa öncülük ettiğini buluyor (r2 §3.9).

**Veri zamanlaması (kritik).**
- GLD yaratma/itfa emir kesimi prospektüse göre 16:00 ET veya NYSE Arca kapanışı. Trustee emir formunda **15:59:59**.
- Takas formun bir sürümünde T+2, 2024 8-K ekinde T+1.
- t günü ilan edilen pay sayısının t'nin mi t−1'in mi emirlerini yansıttığı **doğrulanamadı**.
- https://www.ssga.com/library-content/products/fund-docs/etfs/us/ps/SPDR_GOLD_TRUST_PROSPECTUS.pdf , https://www.sec.gov/Archives/edgar/data/1222333/000143774923032876/ex_583786.htm

**Maliyet sonrası.** Akış sinyali haftalık frekansta ve zayıf. Beklenti sıfıra yakın.

**Test kuralı.**
- **T9.1:** F_t = ΔPay_t / Pay_{t−1}. Bilgi zamanı muhafazakâr olarak t+1 sabahı. r_GLD(C_{t+1}→C_{t+1+h})'yi F_t'ye regres et. Ayrıca F_t en üst ve en alt %10 portföyleri.
- **T9.2:** F_{t+1..t+5}'i r_GLD(t−5→t)'ye regres et (geri besleme). Beklenti pozitif.
- **T9.3:** Hizalama duyarlılığı: F_t'yi hem t hem t−1 getirisiyle eşleştir. Hangisi eşzamanlı korelasyonu en büyütüyorsa ilan gecikmesi odur.

### 3.10 GLD NAV'ı LBMA PM'de, fiyatı 16:00'da: prim/iskonto ve ertesi gün dönüşü

**Mekanizma.** NAV ≈10:00 ET'de (LBMA PM), kapanış 16:00 ET'de belirleniyor. Ölçülen prim ≈ altının 10:00→16:00 getirisi + gerçek fiyatlama hatası. Gerçek hata, yaratma ve itfa arbitrajıyla ertesi gün kapanmalı.

**Kanıt.**
- **GLD 10-Q:** NAV, "LBMA PM veya 12:00 NY'den hangisi önceyse" o andaki değerle belirleniyor (§2.1).
- **Petajisto (2017, FAJ 73(1):24–54):**
  - 2007–2014, ABD ETF'leri.
  - Fiyat ile NAV arasındaki sapma tipik olarak ~200 bps'lik bir bant içinde. **Bayat fiyatlama, benzer fonlarla karşılaştırarak düzeltildiğinde bant ~100 bps.**
  - Ortalama prim 6 bps.
  - Sapmadan yararlanan stratejiler işlem maliyeti öncesi yılda ~%7 anormal getiri sağlıyor.
  - Emtia ETF'lerinde anormal getiri "çok mütevazı".
  - Güven: orta. https://econpapers.repec.org/RePEc:taf:ufajxx:v:73:y:2017:i:1:p:24-54
- GLD'ye özgü prim dönüşü çalışması **bulunamadı**.
- SPDR'ın sitesi ayrıca 16:30 NY spot fiyatını yayımlıyor. Bu NAV bazı değil. https://www.spdrgoldshares.com/usa/historical-data

**Maliyet sonrası.** GLD'nin likiditesi (~1 bps spread) gerçek primi 1–3 bps'e sıkıştırıyor olmalı. Perakende için trade edilebilir bir kenar beklenmiyor. Asıl önemi **ölçüm hatasını önlemek**: GLD'nin "primini" sinyal sanmamak.

**Test kuralı.**
- **T10.1:** π_t = C_GLD,t / NAV_t − 1. π_t'yi r_XAU(LBMA PM_t → 16:00_t)'ye regres et. Beklenti: eğim ≈ 1 ve R² > 0,9.
- **T10.2:** Artık ε_t. r_GLD(C_t→C_{t+1}) − r_XAU(16:00_t→16:00_{t+1})'i ε_t'ye regres et. Beklenti negatif.
- **T10.3:** Aynısı IAU, GLDM ve SLV için (SLV NAV'ı LBMA Silver Price'tan; bu çalışmada doğrulanmadı).

### 3.11 Kapalı uçlu fonlar (PHYS, PSLV, CEF): iskontonun ortalamaya dönüşü

**Mekanizma.** ETF'lerdeki günlük arbitraj yok. Yalnızca aylık fiziki itfa var (§2.4). İskonto yatırımcı duyarlılığını taşır ve ancak yavaş geri döner.

**Kanıt.**
- Genel kapalı uçlu fon literatürü (hisse fonları): bir Rutgers çalışmasına göre çoğu fonda primde anlamlı ortalamaya dönüş var. Sapma payı düzeltilmiş dönüş hızı **ayda %8,6, yarı ömür 7,7 ay**. Uç beşliklerle kurulan arbitraj stratejisi yılda %18,2. Ufuk aylık. Güven: düşük–orta (ikincil özet). https://hedgefundalpha.com/strategies/closed-end-fund-discounts/
- Blose, Gondhalekar ve Kort (2018) gece/gündüz asimetrisinin altınla ilgili kapalı uçlu fonlarda da olduğunu buluyor (§3.1).
- Central Fund of Canada için pratisyen notları: yüksek primler "genellikle ama her zaman değil" ara tepelere yakın. Tarihsel iskonto aralığı −%15 ile −%20. Güven: düşük. https://hedgefundalpha.com/stocks/a-look-at-cef-central-fund-of-canada-which-is-also-a-cef/
- **PHYS, PSLV veya CEF'te 1–5 günlük iskonto dönüşü çalışması bulunamadı.**

**Maliyet sonrası.** Yarı ömür aylar ölçeğinde. 1–5 günde dönüşün beklenen büyüklüğü (iskonto sapmasının ~%1–3'ü) birkaç bps ediyor. Kenar beklenmiyor. Ancak **"altını GLD yerine iskontolu PHYS'ten almak"** pasif bir maliyet avantajı sağlar: iskonto genişlemezse.

**Test kuralı.**
- **T11.1:** D_t = P/NAV − 1. 60 günlük z_t. z_t < −2 ise PHYS uzun, h = 5. Getiri = r_PHYS − r_GLD (altın nötr). Benzer kural PSLV − SLV için.
- **T11.2:** ΔD_{t→t+h}'yi D_t − D̄_60'a regres et. Dönüş hızını yarı ömre çevir.
- **T11.3 (duyarlılık):** PSLV'nin primden iskontoya geçişi (2025–2026'da sıfır primli gün) gümüşün sonraki 5–20 günlük getirisini öngörüyor mu? Karşıt beklenti: yüksek prim sonrası negatif getiri.
- NAV zamanlaması: Sprott NAV saati **bulunamadı**. CEFConnect'in günlük NAV'ını kullanın.

### 3.12 ETF opsiyon vadesi (OPEX) haftası

**Mekanizma.** Opsiyon piyasa yapıcılarının delta hedge pozisyonları vade haftasında çözülür. Fiyat kullanım fiyatına yapışabilir (pinning).

**Kanıt.**
- **Stivers ve Sun (2013, JBF 37(11):4226–4240):** S&P 100 hisseleri. Ayın üçüncü Cuma'sını içeren vade haftasının getirisi, opsiyon aktivitesi düşük hisselerden ve aynı hisselerin diğer haftalarından yüksek. CXO özetine göre 28 hisse, 1996–2008: **vade haftası %0,45, diğer haftalar %0,12**. Ertesi (4. Cuma) hafta hafifçe zayıf. Güven: orta. https://econpapers.repec.org/RePEc:eee:jbfina:v:37:y:2013:i:11:p:4226-4240
- GLD, GDX veya SLV opsiyon vadesine özgü çalışma **bulunamadı**. COMEX altın opsiyon vadesi için r2 §3.8'e bakın.
- Barbon ve diğ. (2021): negatif gamma dengesizliği gün sonu momentumu, pozitif dengesizlik dönüş yaratıyor. Hisse örneklemi.

**Test kuralı.**
- **T12.1:** Vade haftası (3. Cuma'yı içeren Pazartesi kapanışı → Cuma kapanışı) GLD, GDX ve SLV getirisi diğer haftalara karşı. Sonraki hafta ayrı.
- **T12.2:** Vade Cuma'sı r(C_{t−1}→C_t) ile sonraki Pazartesi r(C_t→C_{t+1}).
- Açık pozisyon verisi varsa GLD opsiyon gamma işaretine göre ayır.

### 3.13 Ay dönümü, haftanın günü, Aralık vergi zararı satışı, yarıyıl etkisi

**Kanıt.**
- **Incrementum, In Gold We Trust (hakemsiz, tarihsiz, kaynak Reuters Eikon):** Örneklem başlangıçları GLD 11/2004, GDX 05/2006, GDXJ 11/2009, sonu 12/2023.
  - **Ay dönümü:** GDX ayın 1. günü **+%0,34**, son günü **+%0,20**, ayın geri kalanı ~0. GDXJ ayın 1. günü **+%0,77**, geri kalanı −%0,02. GLD 1. günde "belirgin yüksek", rakam yok.
  - **Haftanın günü:** GLD Pazartesi −%0,01, Cuma +%0,11. GDX Pazartesi −%0,12, Çarşamba +%0,13, Cuma +%0,11. GDXJ Perşembe −%0,09, Cuma +%0,09.
  - **Ay:** Ocak ortalaması GLD +%3,31 (19 yılın 13'ünde pozitif), GDX +%2,74, GDXJ +%2,52. Eylül GDX −%3,03, GDXJ −%5,94.
  - **Yarıyıl (Kasım–Nisan / Mayıs–Ekim):** GLD %8,10 / %1,20, GDX %8,99 / −%4,00, GDXJ %3,44 / −%5,51.
  - Güven: düşük–orta (anlamlılık testi yok, veri madenciliği riski yüksek). https://ingoldwetrust.report/nuggets/calendar-anomalies-and-the-gold-market/?lang=en
- **Aralık vergi zararı satışı (madenciler):**
  - Globe and Mail'e göre 15 Kasım–15 Aralık arasında S&P/TSX Global Gold endeksi %12 düştü (yıl belirsiz). Kanada'da vergi zararı adayları Ocak'ta piyasayı ortalama ~4 puan geçiyor.
  - GDX veya GDXJ'ye özgü hakemli çalışma **bulunamadı**. Etkinin büyük hisselerde kaybolduğu, mikro ölçeklerde sürdüğü yorumu var.
  - Güven: düşük. https://arc-dev.theglobeandmail.com/investing/markets/inside-the-market/article-traders-hoping-for-an-even-better-january-effect-this-year , https://www.mining.com/web/will-the-january-effect-give-gold-and-silver-miners-a-bounce/
- **Türk yatırımcı açısından:** Yabancı menkul kıymet zararları yalnızca aynı yılın kazançlarına mahsup ediliyor (§2.6). Yıl sonundan önce zarar realize etmenin Midas'ta vergisel bir değeri var. Bu ABD'deki vergi zararı satışıyla aynı yönde.

**Maliyet sonrası.** Ay dönümü yılda 12 işlem (2 gün tutuş). Midas'ta 10.000 $'da işlem başı 4 bps. GDX'in 2 günlük ~%0,5'lik ortalaması doğru çıkarsa maliyeti rahat karşılar. Ancak sonuçlar 2004–2023'e ait ve test edilmemiş.

**Test kuralı.**
- **T13.1:** Ayın son iş günü kapanışından 1. iş günü kapanışına (h = 1) ve 2. iş günü kapanışına (h = 2). GLD, GDX ve GDXJ için. 2024–2026 yayın sonrası örneklem ayrı raporlanmalı.
- **T13.2:** Gün kuklaları. HAC ve Bonferroni.
- **T13.3 (Aralık):** GDX ve GDXJ'nin altına göre artığının e toplamı. 15.11–20.12 penceresinde beklenti negatif, 20.12–15.01 penceresinde pozitif. Aynı uzunluktaki rastgele pencerelere karşı.

### 3.14 FOMC günleri (14:00 ET açıklaması ABD kapanışından önce)

**Mekanizma.** Faiz ve dolar sürprizi aynı gün kapanışa yansır. İlk tepki kısmen geri alınabilir.

**Kanıt.**
- Altın için FOMC öncesi sürüklenme bulunamadı. Lucca ve Moench (2015) hisselerde buluyor (r2 §3.7).
- Awartani, Hussain ve Virk (2024, IRFA): altın gevşek yönlü sürprizlere daha duyarlı (r2).
- **Pratisyen:** Kensho'ya göre Mart 2014'ten beri FOMC açıklamalarından sonraki 3 günde GLD ve IAU ortalama **−%0,50** (ETF Trends aktarımı). SentimenTrader: GLD kısa vadede zayıf, uzun vadede güçlü. İstatistik testi yok. Güven: düşük. https://www.etftrends.com/?p=160607 , https://sentimentrader.com/blog/knee-jerk-buying

**ETF ve VİOP farkı.**
- ETF'te FOMC (19:00 UTC kış) **aynı günün** C_t kapanışına giriyor.
- VİOP uzlaşmasında (15:15 UTC) FOMC **ertesi günün** getirisine düşüyor (r2).
- FOMC günü 16:00 ET'deki ETF tepkisi, ertesi günkü VİOP uzlaşmasından **18 saat önce** biliniyor. Bu, iki platform arasında bir **bilgi zamanı avantajı** değil, sadece aynı bilgiyi farklı saatte fiyatlama farkı.

**Test kuralı.**
- **T14.1:** t = FOMC günü. r_GLD(C_{t−1}→C_t), r(C_t→C_{t+1}) ve r(C_t→C_{t+3}), FOMC dışı günlere karşı.
- **T14.2:** r_GLD(14:00→16:00)_t ile r(C_t→C_{t+1}) arasındaki korelasyon. Beklenti negatif (ilk tepkinin geri alınması).
- **T14.3:** GDX için aynısı. Beta ile ölçeklenmiş artık.

### 3.15 ABD kapanışından sonra ve açılıştan önce gelen Asya/Avrupa bilgisinin ETF açılışına geçişi

**Mekanizma.**
- GLD açılışı 16:00→09:30 arasındaki altın hareketini (Asya ve Londra) neredeyse tamamen yansıtmalı, çünkü dayanak 23 saat işlem görüyor.
- Madenci ETF'lerinde iki sürtünme var: (a) bileşen hisselerin açılışı gecikiyor, (b) ASX'teki bileşenler (~%8,6) bayat.

**Kanıt.**
- **Levy ve Lieberman (2013, JBF 37(5):1412–1421):** Ülke ETF'leri senkron saatlerde NAV'larıyla, senkron olmayan saatlerde S&P 500 ile hareket ediyor. ABD getirisine **aşırı tepki** var. Altın için doğrudan değil, ama GDX'in Avustralya bileşeni için bir analoji. Güven: orta. https://ideas.repec.org/a/eee/jbfina/v37y2013i5p1412-1421.html
- **Fiyat keşfi:** New York vadelisi (Hauptfleisch, Putniņš ve Lucey 2016, JFM 36(6):564–586) ve ETF'ler (Ivanov 2013). https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586
- GDX açılış boşluğunun gece altın hareketine eksik tepki verdiğine dair çalışma **bulunamadı**.

**Test kuralı.**
- **T15.1:** r_GLD(C_{t−1}→O9:31_t) = a + b·r_XAU(21:00 UTC_{t−1} → 14:31 UTC_t) (yazın 20:00→13:31). Beklenti b ≈ 1, artık ~0.
- **T15.2 (madenci eksik tepkisi):** r_GDX(O9:31_t→C_t) = a + b·r_XAU(gece) + c·r_GDX(gece). Beklenti b > 0 ve c < 0, yani gece altın hareketine açılışta yetersiz ayarlanma ve gün içinde tamamlanma.
- **T15.3:** ASX altın alt endeksinin seans getirisi (23:00–05:00 UTC, AEDT) eksi aynı penceredeki altın getirisi. GDX'in O→C getirisini öngörüyor mu? Ters yönde, r_GDX(O→C)_t, ertesi ASX seansındaki Avustralya madencilerinin altına göre artığını öngörüyor mu? Bu ikinci test Midas'ta kullanılamaz, mekanizma kontrolüdür.

### 3.16 BIST altın BYF'lerinde (GLDTR, ZGOLD) gram altına göre prim ve dönüşü

**Mekanizma.** Yaratma ve itfa arbitrajı sınırlı ve piyasa yapıcıya bağlı olduğu için BYF fiyatı gram altından sapabilir. BIST pay piyasası ile KMP ve spot altın saatleri farklı (bayat NAV).

**Kanıt.**
- TradingView sayfaları GLDTR için tarihsiz **+%3,34, +%3,37 ve +%4,37** prim gösteriyor. Başka bir aracı sitede +%0,42 ve −%0,4 var. Değerler büyük olasılıkla farklı tarihlerin NAV'ına göre ve **güvenilir değil**. Güven: düşük. https://www.tradingview.com/symbols/BIST-GLDTR/analysis , https://m.doviz.com/borsa/borsa-yatirim-fonlari/gldtr-qnb-portfoy-altin-katilim-byf
- Darphane altın sertifikası primi Şubat 2023'te %21'e çıkmıştı (r4). Türkiye'de altın araçlarının fiziki altına göre kalıcı prim alabildiğini gösteriyor.
- Akademik çalışma **bulunamadı**.

**Maliyet sonrası.**
- BIST'te pay komisyonu Midas'ta sıfır, ama spread ve **%17,5 stopaj** var.
- VİOP'la (F_XAUTRYM veya F_XAUUSD × USDTRY) prim arbitrajı teorik olarak mümkün. GLDTR'de açığa satış perakendeye pratik değil, yani yalnızca "primliyken GLDTR alma, iskontoluyken al" kuralı uygulanabilir.

**Test kuralı.**
- **T16.1:** p_t = P_GLDTR,t / (gram_t × k) − 1. gram_t = BIST KMP veya 18:00 TSİ spot gram altın, k = pay başına gram (KAP'tan veya NAV/gram oranından). 60 günlük z. ΔP_{t→t+h}'yi z_t'ye regres et. Beklenti negatif.
- **T16.2:** GLDTR ile gram altın arasında gün sonu zaman uyumsuzluğu var mı? r_GLDTR(t→t+1)'i gram altının t 18:00 sonrası hareketine regres et.

---

## 4. Maliyet ve vergi sonrası beklenti: Midas ETF ile VİOP

| Kalem | Midas – GLD/GDX (ABD) | VİOP F_XAUUSD (Midas tarifesi) | BIST GLDTR |
|---|---|---|---|
| Komisyon | 1,5 $/emir (yüksek). Gidiş-dönüş 2.000 $'da 15 bps, 5.000 $'da 6, 10.000 $'da 3, 25.000 $'da 1,2, 50.000 $'da 0,6 bps | %0,05/yön, 0–10 milyon TL aylık hacim (yüksek). Borsa ve Takasbank ~0,4 bps/yön (r1). Gidiş-dönüş ≈ 10,8 bps + spread | Komisyonsuz (Midas) |
| Spread | GLD/IAU/GLDM ~1 bps (düşük). GDX, NUGT, DUST ve JNUG ölçülmeli | Ölçülmeli (r2) | Ölçülmeli |
| Kur | TL→USD makası **bulunamadı**. USD bakiye tutmak önerilir | TL teminat, USD fiyat | TL |
| Kaldıraç | Midas ABD marjini **bulunamadı**. LETF'ler 2x | Teminatlı | Yok |
| Vergi | TL bazlı kazanç (kur farkı dahil) %15–40 beyan. Zarar yalnız aynı yıl yabancı menkul kıymet kazancına mahsup | %10 stopaj, üç aylık netleştirme, yıl içi devir (r1) | %17,5 stopaj (09.07.2025 sonrası alım; düşük–orta) |
| Kapanış saati | 16:00 ET = 00:00 TSİ (kış). MOC bulunamadı | 18:05–18:15 TSİ VWAP | ~18:00 TSİ (doğrulanmadı) |

**Örnek (varsayımsal).** Yıllık brüt getirisi %8 olan ve yılda 50 işlem yapan bir strateji:
- **Midas, 10.000 $:** maliyet 50 × 4 bps = %2. Net %6. %27 marjinal vergiyle ~%4,4.
- **VİOP, Midas tarifesi:** maliyet 50 × ~12 bps = %6. Net %2. %10 stopajla ~%1,8.
- **Sonuç:** Pozisyon ≥5.000 $ ise **işlem sıklığı yüksek stratejilerde Midas GLD işlem maliyetinde VİOP'tan ucuz. Vergide pahalı.**
- Düşük sıklıkta (yılda ≤12 işlem) fark vergiye kalır. Kazanç kendisini ödediğinde **VİOP üstün**.
- Kur makası bilinmeden kesin hüküm verilemez.

---

## 5. Veri ihtiyacı ve test protokolü (zorunlu)

1. **Seriler:**
   - Günlük OHLCV: GLD, IAU, GLDM, SGOL, SLV, GDX, GDXJ, NUGT, DUST, JNUG, JDST, UGL, GLL, AGQ, ZSL, PHYS, PSLV, CEF.
   - Açılış için mümkünse 1 dakikalık veri (09:31 veya 09:35).
   - XAUUSD ve XAGUSD saatlik spot, LBMA Gold Price PM, GLD günlük NAV ve pay sayısı (spdrgoldshares.com/usa/historical-data).
   - LETF'lerin günlük pay sayısı ve NAV'ı (ihraççı).
   - FOMC tarihleri, 3. Cuma takvimi, ASX altın endeksi, GLDTR fiyatı ve NAV'ı, BIST gram altın.
2. **Bilgi zamanı disiplini:** Her öngörücü yalnızca karar anında yayımlanmış veriyle hesaplanmalı. Karar anı C_t (21:00 UTC kış / 20:00 UTC yaz) ya da VİOP uzlaşması (15:15 UTC). GLD pay sayısı muhafazakâr olarak t+1.
3. **Alt dönemler:**
   - 2006–2012, 2013–2019, 2020–2026.
   - Yapısal kırılmalar: **17.06.2017** (GDXJ endeksi), **01.04.2020** (NUGT ve JNUG 3x→2x), **20.03.2015** (LBMA elektronik müzayede).
4. **İstatistik:** Newey-West HAC (gecikme h + 5). Örtüşen h-günlük getirilerde h'ye göre düzeltme. Aile içinde FDR ya da Bonferroni (25+ hipotez).
5. **Maliyet:** Midas için emir başı 1,5 $ + ölçülen yarım spread. VİOP için r1/r2 maliyeti. Her hipotez için başabaş pozisyon büyüklüğünü raporla.
6. **Vergi sonrası:** ETF için %27 (orta dilim) ve %40 senaryosu. VİOP için %10.

---

## 6. Bizim veride test edilecek hipotezler (30)

Bilgi zamanı: ET / UTC (kış; yazın UTC bir saat erken). C = 16:00 ET kapanışı. Beklenen işaret hedefin gelecekteki getirisi içindir.

| # | Hedef (ufuk) | Öngörücü | Bilgi zamanı | Beklenen işaret | Mekanizma | Kaynak |
|---|---|---|---|---|---|---|
| H1 | GLD gece r(C_{t−1}→O9:31_t) ve gün içi r(O9:31→C) | Seans ayrımı | Yapısal | Gece +, gün içi ≤0 | Açılış fiyatlama asimetrisi, Asya talebi | Blose ve Gondhalekar 2014; Blose ve diğ. 2018 |
| H2 | GDX gece (09:31 dolumu) | Seans ayrımı | Yapısal | + (yılda ~%8,6, OHLC ~%30 değil) | Aynı; OHLC yanılsaması | Quantpedia 2025 |
| H3 | SLV gece ve gün içi | Seans ayrımı | Yapısal | Gece +, gün içi − | Aynı | R-bloggers 2014 (zayıf) |
| H4 | 1–5 günlük sinyal: çıkışı C_{t+h} yerine O9:31_{t+h}'de yapmak | Çıkış zamanı | 09:31 ET / 14:31 UTC | + (b − a > 0) | Gün içi negatif bileşeni atlamak | H1–H2'den türetilmiş |
| H5 | GLD, GDX (h = 1–5) | RSI(2) < 10 ve C > SMA200 | C_t, 21:00 UTC | + | Kısa vadeli dönüş | Connors ve Alvarez 2008 (altına özgü kanıt yok) |
| H6 | GDX'in altına göre artığı e (h = 1–5) | e_t alt %10 | C_t | + (dönüş) | Likidite sağlama | Genel dönüş literatürü (r2); ETF'e özgü kanıt yok |
| H7 | GDX (h = 1, 3, 5) | r_XAU(C_{t−1}→C_t), r_GDX,t kontrollü | C_t | + | Madencilerin altına gecikmeli tepkisi | Lucey ve O'Connor 2017; Tufano 1998 |
| H8 | GLD ve ertesi VİOP uzlaşma getirisi | GDX artığı e_t | C_t (21:00 UTC), VİOP t+1 15:15 UTC | + (zayıf) | Hisse yatırımcısının erken sinyali | Kantil nedensellik (Resources Policy; düşük); karşı: Lucey ve O'Connor |
| H9 | GDX − β·GLD (h = 5) | ln(GDX/GLD) 60 günlük z < −2 | C_t | + | Göreli değerin ortalamaya dönüşü | Pratisyen; hakemli kanıt yok |
| H10 | GDXJ (h = 1) | r_GDX,t, r_GDXJ,t kontrollü | C_t | + (özellikle r_GDX < 0 günlerinde) | Büyükten küçüğe bilgi yayılımı | Hou 2007 |
| H11 | SLV (h = 1) | r_GLD,t, r_SLV,t kontrollü (ve tersi) | C_t | ? (iki yönlü test) | Ortak faktör, beta farkı | Hakemli günlük kanıt bulunamadı; Ciner 2001 |
| H12 | SLV − GLD (h = 5) | GSR 60 günlük z, |z| > 2 | C_t | Oranın tersine | Uzun dönem bağ (istikrarsız) | Ciner 2001; Lucey ve Tully |
| H13 | GDX son 30 dk r(15:30→16:00) | Ω_t = ΣA(L² − L)·r(09:30→15:30)/ADV | 15:30 ET / 20:30 UTC | + | LETF gün sonu zorunlu alımı | Cheng ve Madhavan 2009; Barbon ve diğ. 2021; Tuzun 2013 |
| H14 | GDX ertesi açılış r(C_t→O9:35_{t+1}) | Ω_t | C_t | − (etkinin ~1/3'ü geri döner) | Geçici fiyat baskısı | Barbon ve diğ. 2021; Tuzun 2013 |
| H15 | GDXJ son 30 dk ve ertesi açılış | Ω_t (JNUG, JDST) | 15:30 ET | + sonra − ; 2014–2017'de daha güçlü | Aynı | Aynı; karşı: Ivanov ve Lenkey 2018 |
| H16 | GDX ve GDXJ (h = 1) | |r_t| üst %10 | C_t | −sign(r_t) | LETF ve opsiyon kaynaklı aşırı hareketin dönüşü | Tuzun 2013; Barbon ve diğ. 2021 |
| H17 | ln(L_{t+5}/L_t) − β·ln(S_{t+5}/S_t) (NUGT, DUST, JNUG, JDST, UGL, GLL, AGQ, ZSL) | Gerçekleşen varyans V_{t→t+5} | Eşzamanlı (yapısal) | Eğim = (β − β²)/2 < 0 | Günlük yeniden dengeleme | Avellaneda ve Zhang 2010 |
| H18 | Ters ETF ile kısa görüş: DUST (h = 5) ile DUST (h = 1, üst üste) | Tutuş süresi | Yapısal | Uzun tutuşta −3V kadar kayıp | Varyans aşınması | Avellaneda ve Zhang 2010 |
| H19 | GLD r(C_{t+1}→C_{t+1+h}) | GLD akışı F_t = ΔPay/Pay | t+1 sabahı (muhafazakâr) | 0 veya − | Temel dışı talebin dönüşü | Brown, Davies ve Ringgenberg 2021; WGC 2023 |
| H20 | GLD akışı F_{t+1..t+5} | r_GLD(t−5→t) | C_t | + | Geri besleme (getiri kovalama) | WGC 2023; NCHU tezi 2012 |
| H21 | GLD prim artığı | π_t − b·r_XAU(LBMA PM→16:00) | C_t (NAV 10:00 ET) | Ertesi gün − (dönüş) | Bayat NAV düzeltildikten sonra gerçek fiyat hatası | GLD 10-Q; Petajisto 2017 |
| H22 | PHYS − GLD, PSLV − SLV (h = 5) | İskonto 60 günlük z < −2 | C_t | + (küçük) | Kapalı uçlu iskontonun ortalamaya dönüşü | CEF literatürü (yarı ömür 7,7 ay); Sprott itfa kuralları |
| H23 | SLV (h = 5–20) | PSLV primi yüksek ve iskontodan primlere geçiş | C_t | − (karşıt duyarlılık) | Duyarlılık | Pratisyen; düşük |
| H24 | GLD, GDX, SLV vade haftası | 3. Cuma haftası kuklası | Takvim | + (sonraki hafta −) | Delta hedge çözülmesi | Stivers ve Sun 2013 |
| H25 | GDX, GDXJ, GLD (h = 1–2) | Ayın son iş günü kapanışında gir | Takvim | + | Ay dönümü akışları | Incrementum (GDX gün 1 +%0,34, GDXJ +%0,77) |
| H26 | GDX Pazartesi | Gün kuklası | Takvim | − (−%0,12) | Hafta sonu bilgi ve risk primi | Incrementum; Lucey ve Tully 2006 (r2) |
| H27 | GDX ve GDXJ'nin altına göre artığı | 15.11–20.12 penceresi (−) ve 20.12–15.01 penceresi (+) | Takvim | −, sonra + | Vergi zararı satışı ve Ocak etkisi | Globe and Mail; Incrementum (düşük) |
| H28 | GLD r(C_t→C_{t+1}), r(C_t→C_{t+3}) | FOMC günü; r(14:00→16:00)_t | 16:00 ET / 21:00 UTC | − (ilk tepkinin geri alınması) | Aşırı tepki | Kensho/ETF Trends; SentimenTrader (düşük); Awartani ve diğ. 2024 |
| H29 | GDX gün içi r(O9:31→C) | Gece altın getirisi r_XAU(21:00 UTC_{t−1}→14:31 UTC_t), GDX gece getirisi kontrollü | 09:31 ET / 14:31 UTC | + | Madencilerin açılışta eksik ayarlanması, ASX bayatlığı | Levy ve Lieberman 2013 (analoji); kanıt yok |
| H30 | GLDTR (h = 1–5) | Gram altına göre prim z_t | ~18:00 TSİ / 15:00 UTC | − | BYF arbitraj sürtünmesi | TradingView anlık görüntüleri (düşük); r4 |

**Ek kontroller (hipotez değil):**
- H31: GLD ile VİOP'ta aynı sinyalin aynı zaman damgasında (VİOP uzlaşması 10:05–10:15 ET kış) uygulanması. Platform farkı yalnızca maliyet ve vergi kaynaklı mı?
- H32: Gao, Han, Li ve Zhou (2018, JFE 129:394–414) "piyasa gün içi momentumu" GLD'de var mı? Gece ve ilk 30 dakika getirisi son 30 dakikayı öngörüyor mu? Baltussen, Da, Lammers ve Martens (2021, JFE) bunu vadelilerde hedge talebine bağlıyor. Altının örneklemde olup olmadığı doğrulanmadı.

---

## 7. Bulunamayan veya doğrulanamayan kalemler

- **Midas:**
  - TL↔USD kur makası veya dönüşüm ücreti
  - Kaldıraçlı/ters ETF'lerin açık olup olmadığı ve karmaşık ürün uygunluk testine tabi olup olmadığı
  - ABD'de açığa satış ve marjin
  - MOC/kapanış emri
  - T+1 takas öncesi nakdin yeniden kullanımı
  - Kış saatindeki güncel uzatılmış ve gece seansı saatleri (sayfalar tutarsız, iki destek sayfası 404 verdi)
- **SPK:** Yabancı kaldıraçlı ETF ve ETN'lerin yerleşik perakendeye satışıyla ilgili güncel düzenleme bulunamadı. Bir banka sayfası "online platformdan alınamaz" dese de diğer kurumlar sunuyor.
- **Sprott:** PHYS, PSLV ve CEF'in NAV saati, ATM programının "yalnızca primde ihraç" kuralı, nakit itfa oranı. Sprott sayfaları 500 verdi.
- **Kaynak eksikleri:**
  - GLD prim dönüşü, GDX→GDXJ gecikmesi, GDX açılış eksik tepkisi ve madenci LETF gün sonu etkisi için hakemli çalışma yok.
  - GLD, GDX ve SLV opsiyon vadesi etkisi yok.
  - 2015 sonrası LBMA müzayedesi etrafında fiyat sürüklenmesi çalışması yok.
  - Altın–gümüş günlük öncülük çalışması yok.
  - Blose ve diğ. (2018) etki büyüklükleri ve örneklem dönemi (tam metin erişilemedi).
- **Tarih ve sürüm sorunları:** GDX'in güncel altın betası (birincil kaynak yok), NUGT, DUST, JNUG ve JDST'nin güncel ve tarihli büyüklükleri, Direxion birincil sayfası (403).
- **Vergi:**
  - ABD–Türkiye anlaşması temettü stopaj oranı IRS tablosundan doğrulanamadı.
  - GLDTR stopajı (%17,5) Resmî Gazete'den teyit edilmedi.
  - Yİ-ÜFE endekslemesinin 1–5 günlük işlemlerde pratikte devreye girmeyeceği (≥%10 şartı) çıkarım.
- **GLD pay sayısı:** İlan edilen pay sayısının hangi günün emirlerini yansıttığı.

---

## 8. Kaynaklar (başlıca)

- SPDR Gold Trust 10-Q (31.12.2024): https://www.sec.gov/Archives/edgar/data/1222333/000143774925002865/gld20241231_10q.htm
- SPDR Gold Trust prospektüs: https://www.ssga.com/library-content/products/fund-docs/etfs/us/ps/SPDR_GOLD_TRUST_PROSPECTUS.pdf
- iShares Gold Trust 10-K: https://www.sec.gov/Archives/edgar/data/1278680/000143774923004329/iau20221231_10k.htm
- GLDM SSS: https://www.spdrgoldshares.com/media/GLD/file/GLDM/GLDM-FAQs-December-2025.pdf
- Quantpedia (2025) GDX gece sürüklenmesi: https://quantpedia.com/dangers-of-relying-on-ohlc-prices-the-case-of-overnight-drift-in-gdx-etf/
- Blose ve Gondhalekar (2014): https://ideas.repec.org/a/taf/apeclt/v21y2014i18p1269-1272.html
- Blose, Gondhalekar ve Kort (2018): https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html
- Caminschi ve Heaney (2014): https://ideas.repec.org/a/wly/jfutmk/v34y2014i11p1003-1039.html
- Hauptfleisch, Putniņš ve Lucey (2016): https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586
- Ivanov (2013): https://ideas.repec.org/a/spr/jecfin/v37y2013i3p453-462.html
- Tufano (1998): https://zendy.io/title/10.1111/0022-1082.00042
- Lucey ve O'Connor (2017): https://ideas.repec.org/a/taf/apeclt/v24y2017i2p90-94.html ; CXO özeti: https://www.cxoadvisory.com/gold/gold-futures-vs-gold-miner-stocks/
- Hou (2007): https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html
- Cheng ve Madhavan (2009): https://www.joim.com/the-dynamics-of-leveraged-and-inverse-exchange-traded-funds/
- Tuzun (2013): https://www.federalreserve.gov/pubs/feds/2013/201348/
- Shum ve diğ. (2016): https://ideas.repec.org/a/oup/revfin/v20y2016i6p2379-2409..html
- Bai, Bond ve Hatch (2015): https://ideas.repec.org/a/bla/reesec/v43y2015i1p37-66.html
- Barbon ve diğ. (2021/2022): https://www.alexandria.unisg.ch/server/api/core/bitstreams/5a99db31-0d37-4f86-9502-8cb0f3bff4fe/content ; https://ideas.repec.org/p/chf/rpseri/rp2240.html
- Ivanov ve Lenkey (2018): https://econpapers.repec.org/RePEc:eee:finmar:v:41:y:2018:i:c:p:36-56
- Lenkey (2024): https://www.aimspress.com/article/doi/10.3934/QFE.2024031
- Avellaneda ve Zhang (2009/2010): https://math.nyu.edu/~avellane/LeveragedETF20090515.pdf
- WGC Ocak 2023: https://www.gold.org/goldhub/research/gold-market-commentary-january-2023
- Brown, Davies ve Ringgenberg (2021): https://econpapers.repec.org/RePEc:oup:revfin:v:25:y:2021:i:4:p:937-972.
- Petajisto (2017): https://econpapers.repec.org/RePEc:taf:ufajxx:v:73:y:2017:i:1:p:24-54
- Stivers ve Sun (2013): https://econpapers.repec.org/RePEc:eee:jbfina:v:37:y:2013:i:11:p:4226-4240
- Levy ve Lieberman (2013): https://ideas.repec.org/a/eee/jbfina/v37y2013i5p1412-1421.html
- Incrementum takvim anomalileri: https://ingoldwetrust.report/nuggets/calendar-anomalies-and-the-gold-market/?lang=en
- Sprott itfa: https://sprott.com/investment-strategies/physical-bullion-trusts/how-to-redeem/
- ProShares 1446(f) bildirimi: https://www.proshares.com/globalassets/proshares/documents/qualified-reports/pst_ii_qualified_report_022223.pdf
- Direxion kaldıraç değişikliği (ETF.com): https://www.etf.com/sections/news/direxion-ratchets-down-geared-etfs
- GDXJ endeks değişikliği (ETF.com): https://www.etf.com/sections/news/popular-gold-miner-etf-change-dramatically
- VanEck GDX: https://www.vaneck.com/us/en/investments/gold-miners-etf-gdx/overview/
- Midas ücretler: https://www.getmidas.com/ucretler/ ; uzatılmış saatler: https://www.getmidas.com/midasin-kulaklari/midasta-gunler-uzuyor-uzatilmis-islem-saatleri-simdi-midasta-p-22615 ; vergi: https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/yurt-disi-hisse-alim-satim-ve-temettu-gelirlerim-icin-ne-kadar-vergi-odemeliyim
- Yapı Kredi 2026 yabancı hisse vergi notu: https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view
- QNB GLDTR: https://www.qnbinvest.com.tr/gldtr
- BYF stopaj tablosu (ikincil): https://hukukcularevi.com/altin-fonu-vergisi-byf-altin-tahvili-kira-sertifikasi-altins1-stopaj/
