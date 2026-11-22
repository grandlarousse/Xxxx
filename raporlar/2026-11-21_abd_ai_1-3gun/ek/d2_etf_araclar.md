araç: 28/35

## Özet

**Doğru araç sırası (kapanışta al, 1–3 gün taşı):** Ana araç düz ETF: SMH (VanEck, %0,35, ~66–73 milyar $) ve SOXX (iShares, %0,33–0,34, ~44 milyar $). İkisinin de 60 günlük işlem hacmi günde ~4,4 milyar $, alım-satım farkı yok denecek kadar dar. Bellek için DRAM (Roundhill, aktif yönetilen, %0,65, 2 Nisan 2026'da açıldı, ~18–25 milyar $). Kaldıraç istenirse önce 2× (ProShares USD; hacmi düşük, günde ~51 milyon $), sonra 3× (SOXL; günde ~9,6 milyar $). Tek hisse 2× ürünler (NVDL, MUU, AMDL, AVGX/AVGG, SKHX/SKHU/SKHL) yalnızca küçük pozisyonla kullanılmalı. Gider oranları %0,75–1,3, oynaklıkları günlük %6–10 (risk_tablosu.csv).

**Mekanik.** Fon her gün kapanışta kaldıracı sıfırlar. Bu yüzden **1 günlük taşımada** fon endeksin günlük getirisinin tam L katını verir; sapma yalnız gider ve izleme hatasıdır. **2–3 günde** sapma tam olarak şöyle (r_i: endeksin günlük getirileri):
- 2 gün: sapma = L(L−1)·r1·r2
- 3 gün: sapma = (L²−L)(r1r2+r1r3+r2r3) + (L³−L)·r1r2r3

Yön değiştiren (testere) piyasada sapma eksi, aynı yönde süren trendde artıdır. Örnek: endeks +%5 sonra −%5 giderse endeks −%0,25 olur, 3× fon −%2,25'e düşer (hedef −%0,75). Simülasyonla, sıfır beklenen getiri ve günlük σ=%4,5 için 3× fonun 3 günlük sapmasının standart sapması 2,1 puan, en kötü %5'lik dilimi −3,0 puandır. −3×'te bunlar 4,2 ve −5,9 puan. Logaritmik (medyan) aşınma ≈ (L²−L)σ²/2, günde: 3× için %0,61, −3× için %1,2. σ=%3,2 (SMH'nin 60 günlük gerçekleşen oynaklığı) için 3×'te %0,31. Finansman (swap) maliyeti 1–3 günde küçüktür. Yıllık yaklaşık (L−1)×kısa vade faiz + spread demek, günde ~%0,03 (kendi tahminim). Asıl maliyet oynaklık aşınması ve boşluk (gap) riskidir.

**Aşırı gün.** Endeks tek günde %33,3 (3×) ya da %50 (2×) düşerse fonun değeri sıfıra iner. Direxion 2× belgeleri bunu açıkça yazıyor. Fon içinde otomatik bir “devre kesici” yok. Örnekler: XIV (Şubat 2018) gösterge değeri bir günde %80'den fazla düştü, ihraççı ürünü erken itfa etti (sonlandırdı). UCO 2020'de 1:25 ters bölünme yaptı. 2026'da Leverage Shares 13 ETF'i kapattı (Ekim), Tradr 5 tek hisse fonunu kapattı (Ekim), Defiance 2 fonu kapattı (Haziran). Leverage Shares Mayıs 2026'da ters bölünme yaptı.

**2026.** 5 Kasım'da SOX −%12,25 ile kaydın 2. en kötü gününü yaşadı (SMH −%11,21). risk_tablosu'na göre SOXL o gün −%38,7, 20 Kasım'da −%31,8 düştü. Zirveden kaybı −%89,7. SOXL'un varlığı Ekim'deki 24,3 milyar $'dan ~15,7 milyar $'a indi. SEC 19 Kasım 2026'da açık konuştu: 3× ve 5× tek hisse ETF'lerine onay “no chance”, sınır 2× (Kural 18f-4, riske maruz değer sınırı %200). SK hynix ADR'si **Nasdaq'ta** SKHY koduyla 10 Temmuz 2026'da açıldı; 2× ürünler 14–15 Temmuz'da çıktı.

**Gün sonu dengelemesi.** Hem uzun hem ters kaldıraçlı fonlar düşüş gününde kapanışa doğru **satar**. Gereken işlem tutarı = L(L−1)·NAV·r. SOXL için 20 Kasım'da (NAV0 ~15,7–23 milyar $, r=−%10,6) bu kabaca **10–15 milyar $ satış** demek; tek fon için, bu benim hesabım. Kanıt karışık. Tuzun (2013) ve Barbon ve ark. bir etki buluyor; Ivanov-Lenkey (2018) fon giriş-çıkışları hesaba katılınca etkinin ekonomik olarak önemsiz olduğunu buluyor. Yani “kapanış satışı ertesi gün döner” fikri sinyal değil, hipotezdir; backtest gerekir.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| SOX 5 Kasım 2026'da −%12,25, kaydın 2. en büyük düşüşü | https://247wallst.com/investing/2026/11/06/chip-stocks-just-had-their-second-worst-day-on-record/ | "9,011.14 ... 1,257.52 points, or 12.25%"; "second-biggest one-day decline on record" | yüksek |
| SMH 5 Kasım −%11,21; SOXX −%12,15 | aynı | "SMH fell 11.21% to $447.73"; SOXX "down 12.15%" | yüksek |
| O hafta SOXX −%22,99, SMH −%20,29 | aynı (arama özeti) | 22.99% / 20.29% | orta |
| SOXL 5 Kasım −%38,7, 20 Kasım −%31,8, zirveden −%89,7 | /home/user/Xxxx/raporlar/2026-11-21_abd_ai_1-3gun/ek/risk_tablosu.csv | -38.707 (2026-11-05); -31.832; zirveden -89.726 | yüksek (yerel veri) |
| Benzinga SOXL düşüşünü “almost 20%” yazdı (muhtemelen gün içi) | https://www.benzinga.com/node/62545840 | "SOXL plunged almost 20%" (arama özeti) | düşük |
| SOXL: %0,75 gider oranı, 15,68 milyar $ varlık, NYSE Semiconductor Index, kuruluş 2010 | https://stockanalysis.com/etf/soxl/ | "0.75%"; "$15.68B" (tarih yok, 21 Kasım'da kontrol edildi) | orta |
| SOXL Ekim 2026'da 7,27 milyar $ giriş, varlık 24,31 milyar $ | https://www.advisorperspectives.com/articles/2026/10/15/1-trillion-chip-draws-billions-leveraged-etf-bets | 7.27B / 24.31B (d1 defteri) | orta |
| SEC: 3× ve 5× tek hisse ETF'ine onay yok | https://cryptobriefing.com/sec-caps-leveraged-etfs-2x-limit/ | "The law says 2x; we are stopping at 2x." (Brian Daly, 19 Kasım 2026) | orta |
| Dayanak Kural 18f-4: riske maruz değer referans portföyün %200'üyle sınırlı | aynı | "caps a fund's value-at-risk at 200%" | yüksek |
| SEC Aralık 2025'te 9 ihraççıya uyarı mektubu gönderdi | aynı | "warning letters to nine issuers" | orta |
| Ekim 2025'ten beri 100'den fazla 3×/5× başvurusu | https://www.morningstar.com/news/marketwatch/20251023222/the-race-to-launch-ever-riskier-leveraged-etfs-in-the-us-is-heating-up | "more than 100 funds targeting 3x or 5x" (arama özeti) | orta |
| DRAM: 2 Nisan 2026, %0,65, Cboe BZX | https://www.roundhillinvestments.com/etf/dram/ | "Expense Ratio 0.65%"; "April 2, 2026" | yüksek |
| DRAM varlığı ~18,26 milyar $ (22 Ekim); bir haber 25 milyar $ diyor | https://www.etfcentral.com/fund/DRAM | $18.26B (22.10.2026); 25 milyar $ tek kaynak (stocktwits) | orta |
| DRAM aktif yönetilir; açılışta MU, Samsung ve SK hynix portföyün ~3/4'ü | https://www.etf.com/sections/features/roundhill-launches-memory-etf-capture-ais-hottest-trade | roughly three-quarters (arama özeti) | orta |
| SK hynix ADR'si Nasdaq'ta SKHY koduyla 10 Temmuz 2026'da açıldı | https://www.indmoney.com/blog/us-stocks/sk-hynix-nasdaq-listing-skhy-ai-stock-explained | "Opening Bell ... July 10"; 10 ADS = 1 hisse | orta |
| SKHX (Leverage Shares 2×, %0,75) 14 Temmuz'da açıldı; ProShares SKHU, Direxion SKHL (15 Temmuz) ve HYNX de çıktı | https://www.structuredretailproducts.com/insights/84109/themes-etfs-launches-leveraged-sk-hynix-etfs | "200% (2x) ... SK Hynix American Depositary Receipt (Nasdaq: SKHY)" | orta |
| SMH %0,35, 72,82 milyar $ (9 Ekim); 65,74 milyar $ (11 Kasım) | https://www.etf.com/sections/news/smh-vs-soxx-which-semiconductor-etf-should-you-buy-2026 | "$72.82B ... 0.35%"; "$65.74 B" (arama özeti) | orta |
| SOXX %0,33–0,34, 43,77 milyar $ (11 Kasım) | https://www.etfcentral.com/compare-etfs/SOXX-vs-SMH | 0.33% / 0.34%; $43.77 B | orta |
| NVDL gider oranı %1,05–1,06, varlığı 4,28 milyar $ (19 Ekim) | https://www.etfcentral.com/fund/NVDL | "$4.28 B"; 1.05% net | orta |
| MUU net gider oranı %1,01, varlığı 3,31 milyar $ (14 Ekim) | https://www.direxion.com/product/daily-mu-bull-and-bear-leveraged-single-stock-etfs | "Net Expense Ratio would be 0.92%" (AFFE hariç); 1.01% | orta |
| AVGX Defiance 2× AVGO, %1,29; AVGG Leverage Shares 2× AVGO, %0,75 | https://www.defianceetfs.com/avgx/ | "two times (200%) the daily percentage change" | orta |
| 2× fon: endeks günde %50'den fazla ters giderse tüm para kaybedilir | https://www.sec.gov/Archives/edgar/data/1424958/000119312520092983/d852223d497.htm | "moves more than 50% ... investors would lose all of their money" | yüksek |
| XIV: gösterge değeri önceki kapanışın %20'sine inince erken itfa (acceleration) | https://credit-suisse.com/articles/media-releases/2018/02/en/credit-suisse-announces-event-acceleration-xiv-etn.html | "Acceleration Date for XIV is February 21, 2018" | yüksek |
| UCO 2020'de 1:25 ters bölünme (21 Nisan 2020) | https://www.businesswire.com/news/home/20200403005521/en/ProShares-Announces-ETF-Share-Splits | 1:25, "April 21, 2020" | yüksek |
| 2026 kapanışları: Leverage Shares 13 ETF (~22 Ekim), Tradr 5 tek hisse fonu (19 Ekim), Defiance BU ve CVNX (8 Haziran) | https://finviz.com/news/400863/leverage-shares-to-close-13-etfs | "close 13 ETFs" (arama özeti) | orta |
| SOXL'un 1 yıllık prim/iskonto aralığı −%0,43 / +%0,29 | https://www.trackinsight.com/en/fund/ARCX:SOXL | -0.43% to +0.29% (10 Temmuz 2026 raporu, arama özeti) | düşük |
| SOXL 23 Haziran 2026'da −%23,06 | https://247wallst.com/investing/2026/06/23/soxls-23-single-day-collapse-exposes-the-real-price-of-3x-leverage/ | 23.06% | orta |
| Ivanov-Lenkey: fon akışları hesaba katılınca dengeleme etkisi ekonomik olarak önemsiz | https://econpapers.repec.org/RePEc:eee:finmar:v:41:y:2018:i:c:p:36-56 | "economically insignificant" (özet, 2006–2014) | yüksek |
| Tuzun (Fed 2013): S&P +%1 → büyük hissede +6,9 baz puan fiyat etkisi | https://www.federalreserve.gov/pubs/feds/2013/201348/201348pap.pdf | "6.9 basis-point increase in price" | orta |
| Yarı iletken kaldıraçlı fonları her %1 harekette ~10 milyar $ işlem yapıyor; günlük toplam rekor 50 milyar $ | https://www.ainvest.com/news/semiconductor-deleveraging-storm-2607/ | ~$10B per 1%; $50B (tarihsiz, tahminci belirsiz, sayfa 403) | düşük |

## Listede olmayan önemli bulgular
- Tek hisse 2× ürünlerde gider oranları sanılandan yüksek: NVDL %1,05, MUU %1,01, AVGX %1,29.
- Uzun ve ters kaldıraçlı fonların ikisi de düşüş gününde satıcıdır. Dengeleme işlemi L(L−1) ile ölçeklenir: 3× için 6, −3× için 12. SOXS'un küçük varlığı bile satış baskısına eklenir.
- Bellek için tek hisse kaldıraçlı ürünler artık var: SKHX, SKHU, SKHL, HYNX (SKHY'ye bağlı). Sayılarının bu kadar hızlı artması dayanak hissenin oynaklığını yükseltebilir.
- SMH'nin 60 günlük gerçekleşen günlük oynaklığı %3,19 (risk_tablosu). Görevdeki “%4–5” varsayımı son iki şok gününe göre yüksek kalıyor. Hesapları iki değerle de verdim.
- 1 günlük taşımada sıfırlamadan kaynaklanan sapma yoktur. Aşınma ancak 2. günden itibaren başlar. Ortalama sapma sıfıra yakın, dağılımı geniş: testere piyasası zarar yazdırır, trend kazanç yazdırır.

## Listeyle çelişen kanıt
- SK hynix ADR'si NYSE'de değil, **Nasdaq**'ta işlem görüyor.
- SOXL'un dayanağı artık “ICE Semiconductor” değil, “NYSE Semiconductor Index” olarak listeleniyor. Gider oranı %0,75 (aralığın alt ucu).
- SOXL varlığı Ekim'deki 24,3 milyar $'dan ~15,7 milyar $'a indi. Önceki dalganın rakamı artık güncel değil.
- Akademik kanıt kapanış dengelemesinin fiyat etkisi konusunda bölünmüş (Ivanov-Lenkey: önemsiz). Hipotez ancak backtestle kesinleşir.
- “TSMX” ve “MVLL” kodları doğrulanamadı.

## Açık kalanlar
- 20 Kasım 2026 için haber kaynağı bulunamadı. SOXL −%31,8 ve SMH −%10,6 yalnız yerel veriden geliyor. O günün dengeleme satış tahmini de yok (yukarıdaki 10–15 milyar $ benim hesabım).
- Direxion sayfası 403 verdi. SOXL/SOXS'un resmi varlığı, prim/iskonto ve 2026 bölünme bilgisi ihraççıdan doğrulanmadı.
- ProShares USD/SSG, TQQQ, TECL gider oranları ve Kasım 2026 varlıkları bu oturumda kontrol edilmedi. Kendi bilgime göre USD %0,95, TQQQ %0,84; doğrulanmadı.
- Swap finansman faizi ve spread için kaynak bulunamadı. “Günde ~%0,03” kendi tahminim.
- 2020 petrol örneklerinde UWT/DWT kapanışı doğrulanmadı. Yalnız UCO'nun ters bölünmesi doğrulandı.
- Barbon ve ark.'ın etki büyüklüğü (baz puan) hâlâ eksik.
