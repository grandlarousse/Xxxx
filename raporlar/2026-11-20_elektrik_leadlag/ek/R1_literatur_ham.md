araç: 51/35 (devam nedeni: 35'te etki büyüklüğü sayıları ve BIST maliyet verisi eksikti; 36-48 arası çağrılar Lo-MacKinlay, Chen vd., Bennett vd. sayılarını ve borsa payını getirdi. Son 3 arama yeni bilgi getirmedi, durdum.)
model: claude-fable-5-2 (bu alt ajan Fable ile çalıştı)

## Özet

**(1) Büyüklük.** Sektör içi büyük → küçük öncülük ABD'de iyi belgelenmiş (Hou 2007; Chordia-Swaminathan 2000), ama özetlerde günlük katsayı yok; tam metinler ücretli. Bu oturumda görülen tek günlük brüt rakam: en likit 434 NYSE hissesinde lead-lag kümeleme sinyali ortalama 2,4 bps/gün, Sharpe 0,62, maliyetsiz ve 2012 sonrası zayıflıyor. Lo-MacKinlay'de haftalık kontraryan kârın en az yarısı çapraz etkilerden. Etki küçük, az rekabetli, az izlenen sektörlerde ve kötü haberde güçleniyor.

**(2) Borsa İstanbul.** Günlük sektör içi hisse düzeyinde öncülük çalışması bulunamadı. Altay (2003): büyük portföy küçüğü yalnız ilk alt dönemde öncülüyor; etki kararsız. BIST30 vadeli-spot öncülüğü dakikalık ölçekte (1 dk veride vadeli öncü, 5 dk veride baskın taraf yok); günlük sinyale çevrilemez. XELKT içeren sektörler arası günlük Granger çalışması bulunamadı; XELKT için yalnız petrol/kömür → endeks bulgusu var. Sektör bağlantılılığında sanayi şok yayıcı; bankaların rolü çalışmalar arasında çelişkili.

**(3) Tavan/taban taşması.** Kim-Rhee (Tokyo) ve Bildik-Gülay (İMKB) gecikmeli fiyat keşfi ve oynaklık taşmasını destekliyor; kilitlenme, yalnızca limite dokunmadan daha güçlü kanıt veriyor. Sayısal büyüklük yalnız Çin'den: tavan kapanışı sonrası gecelik +%2,44, gün içi −%0,30, 2. gün +%0,45, sonra 60 günde geri dönüş. Kazanç açılış boşluğunda; tavanda kilitli hisse alınamadığı için yakalanması şüpheli (çıkarımım). BIST için ertesi gün getirisini ölçen çalışma bulunamadı; BIST-50 gün içi çalışması limit sonrası geri dönüşün daha olası olduğunu söylüyor (aykırı kanıt).

**(4) Maliyet.** DeMiguel vd.: VAR tabanlı günlük portföyler yalnız 10 bps altı maliyette üstün; kontraryan/momentum 5 bps altında. Avramov vd.: kısa vadeli geri dönüş kârı olası maliyetin altında. Yayın sonrası getiriler %58 düşüyor. BIST borsa payı 0,25 bps; aracı komisyonu ve güncel alış-satış farkı doğrulanamadı.

**(5) Sahte öncülük.** Eşzamansız işlem, alış-satış sıçraması, marj sansürü, öncü firmanın çok sektörlü olması (Cen vd. 2013). Arındırma: yalnız likit ve eksiksiz işlem gören hisseler, aynı borsa, tavan/taban günlerini ayrı ele alma, sansürlü modeller (Chiang-Wei GMM, sansürlü GARCH), limit günü yerine %9-10 iç getirilerle karşılaştırma.

**BIST elektrik için beklenti (çıkarım, doğrulanmadı):** en olası aile büyük → küçük sektör içi 1 günlük gecikme ve kötü haber asimetrisi; tavan kilidi taşması güçlü ama uygulanması zor; endeks → hisse günlükte zayıf; saf geri dönüş maliyet sonrası kaybolur. Brüt birkaç bps/günlük etki 10 bps eşiğini geçemez.

**Listeyle çelişen ya da listede olmayan:** XELKT'li Granger çalışması yok; Bennett vd. maliyeti hesaba katmıyor; Cen vd. (2013), Avramov vd. (2006), Chen vd. (2019), Altay (2003), Danışoğlu-Güner (2018), Aktaş vd. (2021) listede yoktu.

## İddia defteri

iddia | kaynak | alıntı ya da sayı | güven
---|---|---|---
Haftalık kontraryan kârın çoğu çapraz etkilerden (551 hisse, 1962-87) | https://www.nber.org/system/files/working_papers/w2977/w2977.pdf | "less than 50 percent of the expected profits from a contrarian investment rule may be attributed to overreaction" | yüksek
Eşit ağırlıklı endekste haftalık otokorelasyon ~%30 | aynı | "equal-weighted index has a first-order autocorrelation of approximately 30 percent" | yüksek
Büyük → küçük öncülük esasen sektör içi | https://econpapers.repec.org/RePEc:oup:rfinst:v:20:y:2007:i:4:p:1113-1138 | "The lead-lag effect between big firms and small firms is predominantly an intra-industry phenomenon." | yüksek (özet; katsayı görülmedi)
Etki olumsuz bilgide ve küçük, az izlenen sektörlerde güçlü | aynı | "driven by sluggish adjustment to negative information"; "small, less competitive and neglected industries" | orta-yüksek
Yüksek hacimli portföy düşük hacimliyi günlük ve haftalık öncüler | https://econpapers.repec.org/RePEc:bla:jfinan:v:55:y:2000:i:2:p:913-935 | "Daily and weekly returns on high volume portfolios lead returns on low volume portfolios, controlling for firm size" | yüksek (özet)
Eşzamansız işlem bunu tek başına açıklamıyor | aynı | "Nonsynchronous trading or low volume portfolio autocorrelations cannot explain these findings." | yüksek (özet)
Aykırı: kısa vadeli otokorelasyonlar abartılmış | https://econpapers.repec.org/RePEc:oup:rfinst:v:7:y:1994:i:3:p:539-73 | "autocorrelations have been overstated in the existing literature" | orta (arama özeti)
Sektörler arası öncülük kısmen sahte | https://ideas.repec.org/a/inm/ormnsc/v59y2013i11p2566-2585.html | "most industry leaders have business segments in other industries, whereas most small firms are pure players" | orta (arama özeti)
VAR portföyleri yalnız 10 bps altı maliyette üstün | https://lbsresearch.london.edu/id/eprint/4 | "outperform the traditional unconditional portfolios only for transaction costs below ten basis points" | yüksek
Kontraryan/momentum arbitraj portföyü yalnız 5 bps altında kârlı | https://econpapers.repec.org/RePEc:cpr:ceprdp:9456 | 5 bps; VAR arbitraj 10 bps | orta (arama özeti; PDF 403)
Lead-lag kümeleme sinyali: 434 NYSE hissesi, 2000-2019, günlük | https://arxiv.org/pdf/2201.08283 | "The mean daily return of the trading signal is 2.4 basis points"; Sharpe 0.62 | yüksek
Aynı sinyal maliyetsiz hesaplanmış | aynı | "we do not take into account transaction costs when calculating the profit of our signal" | yüksek
Sinyal 2012 sonrası zayıflıyor | aynı | "there is a decay in the performance of the signal after 2012" | yüksek
Arındırma: aynı borsa, en likit hisseler | aynı | "restricting our attention to equities trading on the same exchange to avoid spurious lead-lag effects due to non-synchronous trading" | yüksek
Kısa vadeli geri dönüş kârı maliyetin altında | https://econpapers.repec.org/RePEc:bla:jfinan:v:61:y:2006:i:5:p:2365-2394 | "The contrarian trading strategy profits are smaller than the likely transactions costs." | yüksek (özet, arama üzerinden)
Yayın sonrası getiri düşüşü (97 değişken) | https://www.gwern.net/doc/economics/2016-mclean.pdf | "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication." | yüksek
Tokyo: fiyat limitleri üç hipotezi de destekliyor | https://econpapers.repec.org/RePEc:bla:jfinan:v:52:y:1997:i:2:p:885-99 | "evidence supports all three hypotheses suggesting that price limits may be ineffective" | orta-yüksek (arama alıntısı)
İMKB: oynaklık taşması, gecikmeli fiyat keşfi, işlem engeli destekleniyor; kilitlenmede daha güçlü | https://econpapers.repec.org/RePEc:bla:jfnres:v:29:y:2006:i:3:p:383-403 | "price limits have a significant effect on the stock market, casting doubt on their effectiveness" | yüksek (özet; büyüklük yok)
Çin: tavan sonrası devam, sonra geri dönüş | https://www.nber.org/papers/w24014.pdf | gecelik +%2,44; gün içi −%0,30; 2. gün +%0,45; 6-10. gün −%0,59; 11-20 −%0,87; 21-60 −%1,31 | yüksek
Çin: taban sonrası gecelik devam | aynı | gecelik −%1,13 (t=8,7); sonra +%0,34, +%1,33, +%1,68 | yüksek
Devam limite özgü; %9-10 iç getiride yok | aynı | "the price drops by -0.51% at the open price of day 1" | yüksek
BIST-50 (Mart 2008'den 13 ay, 1 saniyelik veri): mıknatıs etkisi | https://econpapers.repec.org/RePEc:eme:imefmp:imefm-04-2020-0151 | "magnet price effects, greater informational asymmetric effects of market quality and each version of price discovery" | yüksek (özet)
Aykırı: BIST-50'de limit sonrası geri dönüş daha olası (gün içi) | https://distantreader.org/stacks/cord/cord-1046529-uu4xmwxg.txt | "Reversals, lower price volatilities and thinner trading volumes are more likely after price limit hits" | orta (arama özeti)
BIST: limitler oynaklığı artırıp kalıcılaştırıyor, likiditeyi düşürüyor; 21 günlük pencere | https://link.springer.com/article/10.1007/s10479-016-2317-y | "do not experience any price limit hits during the 21-day window constructed around each limit hit event" | orta (snippet; sayfa açılamadı)
Türkiye: büyük → küçük öncülük yalnız ilk alt dönemde (günlük portföy) | https://econpapers.repec.org/RePEc:wpa:wuwpfi:0308005 | "this structure is seen only in the first subperiod of Turkish stock market" | yüksek (özet; dönem tarihleri görülmedi)
BIST30 vadeli-spot: 5 dk veride (2007-2010) baskın taraf yok; 1 dk veride (2010-2012) vadeli öncü | https://dergipark.org.tr/en/download/article-file/194210 ; https://dergipark.org.tr/tr/download/article-file/325228 | "neither of the markets is dominant over the other one in the price formation process" | orta-düşük (URL-çalışma eşleşmesi doğrulanmadı)
XELKT: petrol ve kömürden nedensellik/oynaklık yayılımı, doğal gazdan yok (2010-2020) | https://dergipark.org.tr/tr/download/article-file/1603280 | "BIST elektrik endeksi getirisi üzerinde güçlü bir oynaklık yayılma etkisi vardır" | orta (arama özeti)
BIST sektörleri: sanayi baskın şok yayıcı; bankalar net alıcı (günlük, 2009-2022) | https://search.trdizin.gov.tr/yayin/detay/439101 ; https://dergipark.org.tr/en/download/article-file/1575584 | "Sanayi ve finans sektörlerinin şok ve volatilite yayılımında öncü olduğu" (diğer çalışmayla bankalar konusunda çelişiyor) | orta (arama özeti)
BIST pay piyasası borsa payı | https://www.borsaistanbul.com/files/borsa-payi-ve-diger-ucretler-tarifesi.pdf | "Pay Piyasasındaki tüm pazarlarda (varant ve sertifika işlemleri hariç) gerçekleştirilen işlemler 0,25" (bps) | yüksek (yürürlük tarihi okunmadı)
BIST kuralları: hisse bazlı devre kesici ve VBTS | https://dergipark.org.tr/tr/download/article-file/5481283 | "±%5, ±%7,5 veya ±%10 oranlarında sapması durumunda işlemler 5 ila 15 dakika süreyle durdurularak"; VBTS 25.09.2017 | yüksek

## açık kalanlar

- Hou (2007) ve Chordia-Swaminathan (2000) günlük/haftalık katsayıları görülemedi (ücretli; scispace boş, CEPR 403). Sektör içi öncülüğün bps/gün büyüklüğü doğrulanmadı.
- BIST'te tavan/taban sonrası ertesi gün getirisini ölçen çalışma bulunamadı; Bildik-Gülay ve Danışoğlu-Güner tam metin sayıları görülmedi. Kendi veriyle ölçülmeli.
- BIST'te günlük, hisse düzeyinde sektör içi öncülük ve XELKT'li sektörler arası Granger çalışması bulunamadı.
- BIST aracı kurum komisyonu ve güncel alış-satış farkı doğrulanmadı; tek spread kaynağı 1996-97 verili (Önder-Güner 1998). Mart 2020'de marjın %10'a indirildiği yalnız arama özetinde görüldü.
- 2020-2023 bireysel yatırımcı dalgası ve halka arz tavan serileri için ölçümlü kanıt yok; COVID dönemi sürü çalışmaları birbiriyle tutarsız.
- Cohen-Frazzini, Menzly-Ozbas, Brennan vd. bu oturumda kontrol edilmedi (aylık ufuk, öncelik düşük).
- Chiang-Wei GMM ve sansürlü GARCH yalnız arama özetinden; defter dışı bırakıldı, yöntem ayrıntısı doğrulanmadı.