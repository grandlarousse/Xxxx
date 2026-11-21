araç: 33/35

# Fiyat / hacim / oynaklık tabanlı 1–3 günlük kurallar: literatür kanıtı

## Özet

Kapanışta alıp 1–3 gün tutan biri için kanıtı en güçlü kural ailesi **kısa vadeli dönüş**tür (short-term reversal, yani son günlerde sert düşenin geri toparlanması). Bu, akademide "likidite sağlama primi" diye okunur: Nagel (2012) dönüş getirisinin VIX ile güçlü biçimde arttığını, sektör portföylerinde bile yüksek VIX'te yüksek Sharpe verdiğini gösterir. Drechsler-Moreira-Savov (2018), 2001–2016 ondalık fiyatlama sonrası dönemde büyük hisselerde günlük sıralı, 1–5 gün tutulan dönüş stratejisinin 5 günde ortalama 27 bps (yıllık %13,6, Sharpe 0,59) kazandırdığını, ama VIX şoklarına karşı güçlü negatif duyarlılık taşıdığını bulur (VIX 1 puan artınca günlük −19 bps). Yani VIX 30 üstü rejimde **beklenen getiri artar, ama yolda kayıp riski de artar**. Bu rakamlar uzun-kısa kesit portföyüdür; yalnız uzun pozisyon alan kullanıcı için piyasa riski de eklenir.

Endeks düzeyinde: Baltussen-van Bekkum-Da (2019) 2000'lerden sonra büyük endekslerde günlük getirinin **negatif** otokorelasyona döndüğünü (endeks ürünlerinin yükselişiyle) gösterir. Bu, QQQ/SMH gibi ETF'lerde dip alımının (IBS, RSI(2)) mantıksal dayanağıdır. IBS için ana kaynak Pagonidis (2013): IBS < 0,2 sonrası ertesi gün ortalaması +%0,35, IBS > 0,8 sonrası −%0,13. Ancak Kinlay 2016'da SPY'da 2013 sonrası zayıflama buldu (2015–2016 negatif; %95'te anlamlı, %99'da değil). RSI(2) için bağımsız, maliyetli örneklem dışı akademik test bulunamadı; uygulayıcı testleri karışık.

Gece/gün içi: Lou-Polk-Skouras (2019) momentum getirisinin tamamının gece oluştuğunu, dönüş (reversal) kârlarının da gece kazanıldığını bildirir. Ama Boyarchenko-Larsen-Whelan'ın "gece sürüklenmesi" (2:00–3:00 ET, yılda ~%3,7) New York Fed'in Temmuz 2026 notuna göre 2021–25'te **sıfıra yakın**. Kapanışta alıp açılışta satma kuralı artık güçlü bir kanıta dayanmıyor.

Haber ayrımı kritik: Chan (2003) ve Savor (2012, ±%10 şoklar) haberli/analist raporlu şokların **devam ettiğini**, habersiz şokların **döndüğünü** gösterir. 20 Kasım gibi sektörel haber kaynaklı çöküşlerde basit "düşeni al" kuralı yanlış sınıfa girebilir.

Momentum tarafı: Medhat-Schmeling (2022) yüksek devirli hisselerde kısa vadeli momentum bulur, ama bu **aylık** oluşum/aylık tutmadır; 1–3 günlük kurala doğrudan aktarılamaz. 52 hafta zirvesi (George-Hwang 2004) ve yüksek hacim primi (Gervais vd. 2001) de aylık ufuktadır.

Zayıflama: McLean-Pontiff (2016) ortalama getirinin örneklem dışında %26, yayın sonrası %58 düştüğünü gösterir. Oynaklık yönetimi (Moreira-Muir 2017) aylık ölçekli ve Cederburg vd. (2020) tarafından sorgulanmıştır.

**Bu profile en uygun 5 kural (test edilecek parametrelerle):**
1. ETF IBS dip alımı: QQQ/SMH/SOXX, IBS = (K−D)/(Y−D) < 0,2 iken kapanışta al; IBS > 0,8 kapanışı ya da en çok 3 gün sonra sat. Alt kırılım: gün aralığı 20 günlük ortalamanın üstünde; VIX < 20 / 20–30 / > 30.
2. RSI(2) < 10 (ve < 5) dip alımı, 200 günlük ortalama üstü ve altı ayrı; çıkış kapanış > 5 günlük ortalama ya da 3 gün.
3. Endeks/ETF büyük düşüş sonrası: günlük getiri < −2 standart sapma (20 gün) ya da < −%3 / −%5; 1, 2, 3 gün kapanıştan kapanışa; VIX > 30 ve VIX/VIX3M > 1 alt kümeleri.
4. Sektör içi kalıntı dönüş (hisse): AI/yarı iletken sepetinde günlük getiriyi SMH'ye göre artıklaştır, 20 günlük oynaklıkla normalleştir, en kötü 1–2 hisseyi al, 1–5 gün tut; bilanço günlerini çıkar.
5. Kapanış→açılış ve kapanış→kapanış ayrıştırması: kurallar 1–3'ün getirisini gece ve gün içine ayır; 2021 sonrası ayrı raporla.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| Dönüş getirisi VIX ile tahmin edilebilir (Nagel 2012, RFS 25(7)) | https://www.nber.org/papers/w17653 | "highly predictable with the VIX index" | yüksek |
| Sektör portföylerinden dönüş bile yüksek VIX'te yüksek Sharpe verir | https://www.nber.org/papers/w17653 | "Even reversal strategies formed from industry portfolios... produce high rates of return and high Sharpe Ratios during times of high VIX" | yüksek |
| Büyük hisse dönüşü, 2001–2016, 5 günlük getiri 27 bps, Sharpe 0,59 | https://conference.nber.org/conf_papers/f103855.slides.pdf | "Large-cap reversal strategy has an average five-day return of 27 bps (13.6% annual), Sharpe ratio 0.59" | yüksek |
| Dönüş stratejisi VIX şoklarına negatif duyarlı | https://conference.nber.org/conf_papers/f103855.slides.pdf | "Reversal strategy's daily β∆VIX = −19 bps (per 1 point ∆VIX)" | yüksek |
| DMS tasarımı: günlük sıralama, oynaklıkla normalleştirme, bilanço çıkarılmış, 1–5 gün tutma | https://conference.nber.org/conf_papers/f103855.slides.pdf | "drop penny stocks and earnings announcements... hold portfolios for one to five days" | yüksek |
| Büyük hisselerde dönüş 2000 sonrası belirgin azaldı (Cheng-Hameed-Subrahmanyam-Titman) | https://www.abfer.org/media/abfer-events-2014/annual-conference/investment-finance/short-term-reversals-and-the-efficiency-of-liquidity-provision.pdf | "reversals also decline substantially for all but the micro-cap stocks in the post-2000 period" (arama özeti) | orta |
| Sektör içi kalıntı dönüş, standart dönüşün 4 katı risk düzeltilmiş getiri (Da-Liu-Schaumburg 2014) | https://econpapers.repec.org/RePEc:inm:ormnsc:v:60:y:2014:i:3:p:658-674 | "risk-adjusted return four times the size of the standard reversal strategy" (arama özeti) | orta |
| Endeks günlük otokorelasyonu 2000'lerden beri negatif (20 endeks, 15 ülke) | https://www3.nd.edu/~zda/Indexing.pdf | "it switches to negative since the 2000s" (arama özeti) | yüksek |
| IBS < 0,2 sonrası ertesi gün +%0,35, IBS > 0,8 sonrası −%0,13 (Pagonidis örneği) | https://jonathankinlay.com/?p=2199 | "0.35%" / "-0.13%" (uygulayıcı, hakemsiz) | orta |
| IBS SPY/EWS stratejisi 1999–2016 YBBO ~%13 / %40, maliyetsiz | https://jonathankinlay.com/?p=2199 | "of the order of 13% for SPY and as high as 40% for EWS" | orta |
| IBS 2013 sonrası zayıflıyor; %99'da kesin değil | https://jonathankinlay.com/?p=2199 | "evidence of a weakening of the IBS effect since around 2013" | orta |
| IBS etkisi geniş aralıklı ve (ABD) yüksek hacimli günlerde | https://jonathankinlay.com/?p=2199 | "the effect is also larger after days with high range" (arama özeti) | düşük |
| Ülke ETF'lerinde 2009–2019 IBS<0,2 sonrası pozitif gün olasılığı ~0,55–0,61; etki 1 günü geçmiyor | https://arxiv.org/abs/2306.12434 | "does not seem to have an effect beyond horizons of one day" | orta |
| Connors testleri 1995–2007, maliyet ve veri madenciliği düzeltmesi yok | https://cxoadvisory.com/technical-trading/a-few-notes-on-short-term-trading-strategies-that-work | "1995-2007"; "hypothetical backtests without transaction costs or data mining corrections" (arama özeti) | orta |
| RSI(2) S&P 500 CFD, 2016–2026: yıllık ~%1,7 (al-tut %13,5) | https://backtrex.com/en/backtests/connors-rsi-2-sp-500 | "+18.1%, profit factor 1.43, 71% winners" (uygulayıcı) | düşük |
| Momentum kârlarının tamamı gecede (Lou-Polk-Skouras 2019 JFE) | https://personal.lse.ac.uk/polk/research/TugOfWar.pdf | "all of the abnormal returns on momentum strategies remarkably occur overnight" | yüksek |
| Dönüş ve momentum kârları gece; diğer stratejiler gün içi | https://personal.lse.ac.uk/polk/research/TugOfWar.pdf | "earned entirely overnight (for reversal and a variety of momentum strategies)" (arama özeti) | orta |
| Gece sürüklenmesi 1998–2020 yılda ~%3,7; 2021'den beri sıfıra yakın | https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ | "previously generated roughly 3.7 percent per annum has averaged close to zero since 2021" | yüksek |
| Kapanış satış dengesizliği sonrası gece sıçraması 2021–25'te zayıfladı | https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ | "In 2021–25... the spread is much narrower" | yüksek |
| Haberli kötü haberde devam, habersiz aşırı harekette dönüş (Chan 2003) | https://econpapers.repec.org/RePEc:eee:jfinec:v:70:y:2003:i:2:p:223-260 | "Reversal after extreme price movements unaccompanied by public news" (arama özeti); küçük/likit olmayanlarda | orta |
| Savor 2012: ±%10 şok; analist raporlu şok sürüklenir, raporsuz döner | https://econpapers.repec.org/RePEc:eee:jfinec:v:106:y:2012:i:3:p:635-659 | "no-information events produce reversals" (arama özeti) | orta |
| Savor stratejisi yıllık ~%35 anormal getiri (varsayımsal) | https://rpc.cfainstitute.org/research/cfa-digest/2013/02/stock-returns-after-major-price-shocks-the-impact-of-information-digest-summary | ~%35 yıllık (arama özeti) | düşük |
| Kısa vadeli momentum: en yüksek devir dilimi +%1,37/ay, en düşük −%1,41/ay; aylık ufuk | https://alphaarchitect.com/short-term-momentum/ | "1.37 percent per month" / "-1.41 percent per month" (arama özeti) | orta |
| Klasik aylık dönüşün maliyeti (%1,94/ay) brüt getiriyi siler | https://alphaarchitect.com/short-term-momentum/ | "1.94 percent" (arama özeti) | orta |
| 52 hafta zirvesi stratejisi ABD'de ~%0,45/ay (aylık ufuk) | https://www.bauer.uh.edu/tgeorge/papers/gh5-paper.pdf | "0.45% in the U.S. market in George and Hwang (2004)" (arama özeti, ikincil) | düşük |
| Yüksek hacim primi: olağandışı hacimli gün/hafta sonrası ay boyu yükseliş | https://sites.duke.edu/sgervais/?p=64 | "tend to appreciate (depreciate) over the course of the following month" | orta |
| Anomali getirisi örneklem dışı %26, yayın sonrası %58 düşük | https://ivey.uwo.ca/media/3775549/pontiff.pdf | "26% lower out-of-sample and 58% lower post-publication" (arama özeti) | yüksek |
| Oynaklık yönetimi: piyasa Sharpe +%25 (çalışma kâğıdı); aylık ölçek | https://www.nber.org/papers/w22208 | alfa %4,9, Sharpe +%25 (çalışma kâğıdı; arama özeti) | orta |
| VIX vadeli eğrisi ters dönüşü <%20 zaman; yön tahmini zayıf, dağılım geniş | https://www.cboe.com/insights/posts/inside-volatility-trading-is-vix-backwardation-necessarily-a-sign-of-a-future-down-market | "less than 20% of the time since 2010" (arama özeti) | orta |
| VIX %30+ sıçrama sonrası ~1 haftalık aşırı satım sıçraması, 10–20 günde zayıflık | https://www.investing.com/analysis/last-two-days-are-5-and-6-one-day-vix-spikes-in-history-262769 | "lasts approximately one week" (uygulayıcı, arama özeti) | düşük |

## Listede olmayan önemli bulgular

- **Drechsler-Moreira-Savov (2018, "Liquidity Creation as Volatility Risk")**: 2001–2016 için büyük hisselerde günlük dönüşün sayısal kanıtı ve çöküş rejimi davranışı (getiri VIX ile artar ama VIX şokunda kayıp). Bu, kullanıcının profiline en doğrudan uyan akademik çalışma.
- **Baltussen-van Bekkum-Da (2019 JFE)**: Endeks/ETF düzeyinde günlük negatif otokorelasyon. ETF dip alımının (IBS, RSI(2)) akademik dayanağı.
- **New York Fed, Temmuz 2026 "The Disappearing Overnight Drift"**: Gece primi 2021 sonrası sönmüş. Gece tutmanın ek avantajı artık kanıtlı değil.
- **Akbas-Boehmer-Jiang-Koch (2022 JFE)**: Ay içinde sık "pozitif gece + gün içi geri dönüş" yaşayan hisseler sonra daha yüksek getiri. Aylık sinyal; Çin'de tekrar edilemedi.
- **Cederburg vd. (2020 JFE)**: Oynaklık yönetimi doğrudan karşılaştırmada sistematik üstünlük göstermiyor.

## Listeyle çelişen kanıt

- Medhat-Schmeling, 52 hafta zirvesi ve yüksek hacim primi **aylık** ufuktaki bulgulardır; 1–3 günlük kurala kanıt sayılmaz.
- "Dönüş büyük hisselerde söndü" iddiası kısmen yanlış: DMS 2001–2016 büyük hisselerde günlük dönüşü Sharpe 0,59 ile buluyor (brüt, uzun-kısa). Aylık dönüş ise maliyet sonrası ölü.
- Gece/gün içi: 2023 makalesinin vurguladığı gece primi 2021–25'te yok; kapanış→açılış satış kuralı güncel kanıta dayanmıyor.
- IBS'in "hâlâ çalışıyor" olduğuna dair 2015 sonrası temiz, maliyetli, örneklem dışı akademik test bulunamadı; tek uygulayıcı kaynağı (Kinlay) zayıflama raporluyor, 2023 arXiv 2009–2019 ülke ETF'lerinde etkiyi koruyor.

## Açık kalanlar

- QQQ/SMH/SOXX için 2015–2026 IBS ve RSI(2) sonuçları ile VIX > 30 alt kümesi: veri ajanı hesaplamalı (yayımlanmış güvenilir rakam yok).
- Nagel (2012) makalesinden tam sayılar (yüksek VIX dönemindeki getiri, Sharpe) metinden çıkarılmadı.
- Cheng-Hameed-Subrahmanyam-Titman (JFQA 2017) metnine erişilemedi (core-prod.cambridgecore.org ağ izninde değil); iddia arama özetine dayanıyor.
- Moreira-Muir yayımlanmış sürüm rakamları ve McLean-Pontiff tam metin satırları doğrudan görülmedi.
- Cooper-Cliff-Gulen 2008 ve Tetlock 2011 için sayısal sonuç alınmadı.
