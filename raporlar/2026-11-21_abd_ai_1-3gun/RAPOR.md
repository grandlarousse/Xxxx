# ABD'de yapay zekâ, çip ve bellek hisseleri: 1–3 günlük işlem için araçlar ve yöntemler

**22 Kasım 2026 · Veri son günü: 20 Kasım 2026 kapanışı**

Yatırım tavsiyesi değildir. Buradaki sayılar geçmiş veriye dayanır; gelecekte aynı sonucu vermeyebilir. Kaldıraçlı ürünlerde tek günde paranın üçte biri kaybedilebilir.

Sık geçen terimler: **bps** (baz puan) yüzde birin yüzde biridir, 100 bps = %1. **ETF** borsada hisse gibi alınıp satılan fondur. **VIX** S&P 500 opsiyonlarından hesaplanan korku endeksidir. **Alfa** burada "sinyal günlerinde alınca, aynı aracı rastgele bir günde almaya göre fazladan kazanılan" demektir.

## 1. Kısa yanıt

1. **Araç:** Bu iş için doğru araçlar tek hisseler değil, likit yarı iletken ve teknoloji ETF'leri: SMH, SOXX, QQQ. Gaz pedalı olarak bunların 3 katlı kaldıraçlıları: SOXL ve TQQQ. Tek hisselerde (NVDA, AMD, MU ve diğerleri) test ettiğimiz hiçbir kural maliyetten sonra para bırakmadı.
2. **Yöntem:** Önceden tanımlanmış 61 testten, çürütme turundan sonra tek bir kural ayakta kaldı: **VIX 30'un üstündeyken, günün dibine yakın kapanan endeks ETF'ini kapanışta al, 1–2 gün tut.** Tarihsel sonuç işlem başına yaklaşık +%1 (SOXL'da yaklaşık +%3); 18 stres döneminin 17'sinde artı.
3. **Sakin piyasada bu kural da çalışmıyor:** VIX 20'nin altındayken kazanç sıfır. Yılda ortalama birkaç işlem çıkar ve hepsi kriz dönemlerine yığılır.
4. **Lead-lag (öncül–takipçi):** 27 test ve 84 kombinasyonluk taramadan hiçbiri geçmedi. Liderin bilgisi aynı gün ya da ertesi açılışta fiyatlanıyor; kapanışta alan birine bir şey kalmıyor.
5. **"Ciddi kazanç" sinyal bolluğundan değil, kaldıraç ve rejimden geliyor;** bedeli de büyük: aynı kural 19 Kasım'da SOXL'da sinyal verdi ve ertesi gün −%32 yazdı.
6. **Şu an:** VIX 35,9 ve cuma kapanışında kural altı ETF'in hepsinde açıktı. Bu, kuralın tarihsel olarak en çok kazandırdığı ama en sert kayıpların da görüldüğü bölge.

## 2. Ne yapmalıyım

**Adım 1 — Tek kuralı öğren ("stres günü dip kapanışı").**

- Koşul 1: VIX 30 ya da üstü (kapanışa 10 dakika kala bak).
- Koşul 2: Aracın o günkü kapanışı, günün en düşüğü ile en yükseği arasındaki aralığın alt beşte birinde. Ölçüsü IBS: (kapanış − en düşük) / (en yüksek − en düşük). IBS 0,2'nin altındaysa koşul sağlanır.
- Araç: SMH ya da QQQ. Daha saldırgan istersen SOXL ya da TQQQ (aşağıdaki boyut sınırıyla).
- Giriş: kapanıştan önceki son dakikalar (Türkiye saatiyle kışın 23:55–23:59), limit emirle.
- Çıkış: ertesi günün kapanışı ya da ikinci günün kapanışı. **Ertesi sabah açılışta satma:** kazancın büyük kısmı açılıştan sonra geliyor. Üçüncü gün ortalamada bir şey eklemiyor.

**Adım 2 — VIX'e göre davran.**

| VIX | Ne yap | Geçmişte işlem başına alfa (6 ETF havuzu) |
|---|---|---|
| 30 ve üstü | Kural geçerli | +98 bps (445 işlem, 18 dönem) |
| 20–30 | İsteğe bağlı, küçük boyutla; kanıt zayıf | +23 bps (1.383 işlem) |
| 20'nin altı | Bu kuralla işlem yapma | ≈ 0 (2.522 işlem) |

**Adım 3 — Boyutu en kötü güne göre seç.** Tek işlemde sermayenin %3'ünden fazlasını kaybetmemek için, 2023'ten beri görülen en kötü tek güne göre üst sınırlar:

| Araç | En kötü tek gün | Pozisyon üst sınırı (sermayenin yüzdesi) |
|---|---|---|
| QQQ | −%6,5 | %45 |
| SMH | −%11,2 | %27 |
| TQQQ | −%18,9 | %16 |
| SOXL | −%38,7 | %8 |

SOXL için backtest %33 pozisyonla da koşuldu: yıllık bileşik %12,8, en büyük düşüş −%18. Ama 20 Kasım gibi bir günde %33 pozisyon tek seferde sermayenin yaklaşık %10,5'ini götürür.

**Adım 4 — Bunları yapma (hepsi test edildi, sonuç olumsuz ya da anlamsız):**

- Bilanço öncesi alıp tepki günü satma. Eskiden çalışıyordu, 2023'ten beri etkisi yok; 2026'da işlem başına −88 bps.
- Bilanço sonrası %5'ten fazla düşeni alma: net −45 bps.
- Lider hisse yükseldi diye takipçisini alma, Asya kapanışına bakarak ABD'de alma, Bitcoin yükseldi diye madenci alma.
- Sert yükseliş gününün kapanışında alma. Alım için hiçbir kanıt yok; geçmişte ertesi gün ortalama −40 bps.
- "Üç gün üst üste düştü, alayım", RSI(2), 20 günlük zirve kırılımı, ay sonu ve FOMC öncesi alımları: hiçbiri testten geçmedi.

**Adım 5 — Aracı kurumu maliyete göre seç.** Kural yalnız işlem başı sabit ücretli kurumda (ör. işlem başı 1,5 $) çalışır. Oransal komisyonlu kurumlarda (gidiş-dönüş 50–60 bps) SOXL'un stres günleri dışındaki her şey zarara döner. İşlem yapmadan önce kurumuna iki şeyi sor: SOXL ve TQQQ alınabiliyor mu, kapanış müzayedesi emri (MOC) verilebiliyor mu. İkisini de doğrulayamadık.

**Adım 6 — Günlük kontrol.** `kod/sinyal.py` kapanıştan sonra, `--saat 1530` seçeneğiyle kapanıştan yarım saat önce çalışır; VIX'i, IBS'leri ve açık kuralları yazar. 15:30 fiyatıyla verilen sinyal, kapanışla verilenin kazancının yaklaşık dörtte üçünü yakaladı.

**Adım 7 — Önce kâğıt üstünde izle.** Kural yılda birkaç kez ve hep en gergin günlerde çalışır. İlk birkaç sinyali gerçek para koymadan ya da çok küçük boyutla izlemek, hem emir verebildiğini hem de o günlerdeki fiyat makasını görmeni sağlar.

## 3. Araçlar: hangi ETF ve hisseler

Hacim ve oynaklık kendi hesabımızdır (Yahoo verisi, son 60 işlem günü). "En kötü gün" 2023'ten beridir. Gider oranı ve fon büyüklükleri ihraççı ve veri sitelerinden doğrulandı.

### 3.1 ETF'ler ve kaldıraçlı ürünler

| Kod | Ne | Günlük hacim | Günlük oynaklık | En kötü gün | Not |
|---|---|---|---|---|---|
| SMH | Yarı iletken ETF'i | 4,4 mr $ | %3,2 | −%11,2 | Gider %0,35; ~61 mr $. Ana araç |
| SOXX | Yarı iletken ETF'i | 4,4 mr $ | %3,6 | −%12,2 | Gider %0,33–0,34; 31 mr $ |
| QQQ | Nasdaq-100 | 25,4 mr $ | %1,7 | −%6,5 | En likit, en sakin |
| DRAM | Bellek ETF'i (aktif) | 1,7 mr $ | %4,9 | −%18,0 | Nisan 2026'da açıldı; gider %0,65; 12,6 mr $. Geçmişi kısa, test edilemedi |
| SOXL | 3× yarı iletken | 9,6 mr $ | %11,0 | −%38,7 | Gider %0,75; zirveden −%90 |
| TQQQ | 3× Nasdaq-100 | 4,1 mr $ | %5,0 | −%18,9 | Zirveden −%53 |
| USD | 2× yarı iletken | 0,05 mr $ | %6,4 | −%27,5 | Hacmi düşük, makası geniş olabilir |
| TECL | 3× teknoloji | 0,11 mr $ | %6,4 | −%23,9 | Hacmi düşük |
| NVDL | 2× Nvidia | 0,35 mr $ | %6,0 | −%33,8 | Gider %1,05 |
| AMDL | 2× AMD | 0,14 mr $ | %11,1 | −%34,9 | Geçmişi kısa |
| MUU | 2× Micron | 0,66 mr $ | %9,5 | −%34,4 | Gider %1,01 |
| SOXS / SQQQ | −3× ters ürünler | 3,0 / 1,9 mr $ | %11,1 / %5,1 | −%56 / −%35 | Düşüş beklentisi için; kural olarak test edilmedi |

Tek hisse 2× ürünler başka hisselerde de var: Broadcom (AVGX), TSMC (TSMX, TSMG), Marvell (MVLL), SK hynix (SKHX, SKHU, SKHL ve diğerleri). Gider oranları %0,75–1,5 arasında. 2026'da en az 20 kaldıraçlı ürün kapatıldı; küçük fonlarda bu risk gerçek.

### 3.2 Hisseler

| Kod | İş | Günlük hacim | Günlük oynaklık | En kötü gün | Sıradaki takvimli olay |
|---|---|---|---|---|---|
| NVDA | GPU lideri | 26,1 mr $ | %3,0 | −%17,0 | Bilanço geçti (17 Kas); CEO ve SEC haberleri |
| AMD | GPU ve işlemci | 12,1 mr $ | %5,5 | −%17,3 | — |
| AVGO | Özel yapay zekâ çipi | 8,5 mr $ | %3,5 | −%17,4 | Bilanço 9 Ara, kapanış sonrası |
| TSM | Dökümhane | 4,6 mr $ | %3,0 | −%13,3 | Kasım geliri 10 Ara |
| MRVL | Özel çip, optik | 4,7 mr $ | %5,6 | −%19,8 | Bilanço 1 Ara, kapanış sonrası |
| LRCX | Çip ekipmanı | 2,6 mr $ | %4,7 | −%16,4 | — |
| AMAT | Çip ekipmanı | 2,8 mr $ | %4,3 | −%14,1 | — |
| INTC | İşlemci, dökümhane | 9,4 mr $ | %5,8 | −%28,6 | — |
| MU | Bellek (DRAM, HBM) | 23,8 mr $ | %4,8 | −%17,5 | Bilanço 17 Ara, 16:30 ET |
| SNDK | Flaş bellek (NAND) | 12,5 mr $ | %6,1 | −%22,3 | 19 Kas'ta 8'e 1 bölündü |
| WDC | Sabit disk | 2,9 mr $ | %5,0 | −%18,3 | — |
| STX | Sabit disk | 3,1 mr $ | %5,1 | −%16,4 | — |
| SKHY | SK hynix ADR'si | 3,0 mr $ | %5,1 | −%13,7 | Temmuz 2026'dan beri işlemde |
| ANET | Veri merkezi ağı | 1,0 mr $ | %4,1 | −%22,4 | — |
| CRDO | Bağlantı çipleri | 1,3 mr $ | %6,8 | −%46,8 | Bilanço 1 Ara, kapanış sonrası |
| CIEN | Optik ağ | 1,0 mr $ | %6,0 | −%21,0 | Bilanço 10 Ara, açılış öncesi |
| VRT | Güç ve soğutma | 1,3 mr $ | %5,1 | −%29,9 | — |
| DELL | Yapay zekâ sunucusu | 3,3 mr $ | %5,7 | −%19,0 | Bilanço 24 Kas |
| ORCL | Bulut altyapısı | 4,0 mr $ | %4,1 | −%13,8 | Bilanço 10–14 Ara (resmî değil) |
| CRWV | GPU bulutu | 2,8 mr $ | %6,6 | −%20,8 | — |
| NBIS | GPU bulutu | 3,3 mr $ | %6,7 | −%37,4 | — |
| IREN | Madencilikten yapay zekâya | 1,5 mr $ | %6,8 | −%24,3 | — |
| PLTR | Yapay zekâ yazılımı | 4,1 mr $ | %3,2 | −%15,1 | — |
| ANT | Anthropic | — | — | — | 19 Kas'ta halka arz oldu; 2 günlük veri var, ölçülemez |

Bu hisseler aynı anda düşer. Son bir yılın verisiyle çekirdek çip hisseleri, SMH ve SOXL tek bir küme oluşturuyor; bellek ve disk (MU, SNDK, WDC, STX) kendi içinde 0,79 korelasyonla ikinci küme. Beş ayrı çip hissesi almak beş ayrı bahis değil, tek bahistir.

Tek hisselerde neden kural çıkmadı: günlük oynaklığı %3,6 olan bir hissede 100 işlemle ancak 100 bps'lik bir kenar ayırt edilebiliyor. Daha küçük kenarlar gürültüden ayrılamıyor, ayrılabilenleri de 20–40 bps'lik maliyet yiyor.

### 3.3 Kaldıraçlı ETF'i 1–3 gün taşımak

- Fon kaldıracını her gün kapanışta sıfırlar. **Bir günlük taşımada** endeksin günlük getirisinin tam 3 katını alırsın; sapma yok.
- **İki ve üç günde** sapma başlar: piyasa yön değiştirirse eksi, aynı yönde giderse artı. Endeks +%5 sonra −%5 yaparsa endeks −%0,25'te, 3× fon −%2,25'tedir.
- Endeks tek günde %33'ten fazla düşerse 3× fonun değeri sıfıra iner; SOXL izahnamesi bunu açıkça yazıyor. 5 Kasım'da SOX −%12,25 düştü; bu, kayıtlardaki en kötü ikinci gündü.
- Kaldıraçlı fonlar düşüş gününde kapanışa doğru satmak zorundadır. 20 Kasım için SOXL'un tek başına yaklaşık 10–15 milyar $ sattığını hesapladık (kendi hesabımız). Bunun ertesi gün geri döndüğüne dair akademik kanıt bölünmüş durumda.

## 4. Yöntemler: ne test edildi, ne kaldı

### 4.1 Nasıl test ettik

- **Veri:** 140 kodun 2010'dan 20 Kasım 2026'ya günlük fiyatları, 95 kodun son iki yıllık saatlik fiyatları.
- **Kural:** Sinyal kapanışta bilinir, alım kapanışta yapılır, satış 1–3 gün sonraki kapanışta.
- **Önceden kayıt:** Hesaplardan önce 61 test, parametreleriyle birlikte yazıldı; sonradan eşik oynatmak yasaktı. Çoklu test düzeltmesi (61 testi birlikte değerlendiren Benjamini-Hochberg yöntemi) uygulandı.
- **Seçim yanlılığı:** Hisse listesi bugünün kazananlarından oluşuyor. Bu yüzden her sinyal, aynı aracın kendi ortalamasına göre ölçüldü ve ana sınama alanı olarak altı geniş ETF kullanıldı (SMH, SOXX, QQQ, XLK, SPY, IWM).
- **Maliyet:** Gidiş-dönüş 10 bps (dev hisseler ve büyük ETF'ler), 20 bps (orta), 40 bps (küçük).
- **Doğrulama:** Ayakta kalanları ikinci bir kodlayıcı yalnız protokol metninden sıfırdan yazdı; üçüncü bir kodlayıcı çürütmeye çalıştı.

### 4.2 Karar tablosu

| Kural | İlk sonuç (alfa, t) | Çürütmeden sonra | Karar |
|---|---|---|---|
| Dipte kapanış (IBS < 0,2), VIX ≥ 30, ETF | +98 bps, t 3,1 | Ayakta: 17/18 dönem artı; 2020 hariç +72 | **Kullanılabilir (koşullu)** |
| Dipte kapanış, bütün günler, ETF | +17 bps, t 3,1 | Zayıfladı: stres dışında +8 bps, maliyetin altında | Sakin piyasada kullanılamaz |
| Dipte kapanış, tek hisseler | +14 bps, t 2,5 | Maliyet sonrası −3 bps | Kullanılamaz |
| Üç gün üst üste düşük kapanış, ETF | +19 bps, t 2,6 | Çürüdü: başka ETF'lerde +5; en iyi 20 gün çıkınca 0 | Kullanılamaz |
| SOX −%3 ve altı gününde SMH al | +43 bps, t 2,1 | Çürüdü: 2020 dışında ayırt edilemiyor | Ayrı kural değil |
| Bilanço öncesi al, tepki günü sat | +58 bps, t 3,0 | Çürüdü: 2023'ten beri +14 (t 0,3); 2026 −88 | Kullanılamaz |
| Lead-lag, 27 test | En iyisi bile alımda ≈ 0 | — | Kullanılamaz |
| RSI(2), kırılım, göreli değer, VIX sıçraması, ay sonu, FOMC öncesi | Hepsinde t < 2 | — | Kullanılamaz |

### 4.3 Ayakta kalan kural: stres günü dip kapanışı

**Kazanç nereden geliyor.** Altı ETF'te IBS < 0,2 sonrası ertesi gün alfası, VIX düzeyine göre:

| VIX | İşlem sayısı | Alfa (bps) |
|---|---|---|
| 15'in altı | 1.023 | +2 |
| 15–20 | 1.499 | −2 |
| 20–30 | 1.383 | +23 |
| 30 ve üstü | 445 | +98 |

**IBS gerçekten bir şey katıyor mu.** Evet. Aynı stres günlerinde dibe yakın kapanmayan ETF'i almak ortalama −9 bps verdi; streste koşulsuz almak +27 bps (t 1,3). Yani kazanç "stres günü al"dan değil, "stres günü dibe yakın kapananı al"dan geliyor.

**Kaç gün tutmalı.** Stres günlerinde aynı girişin farklı çıkışları:

| Çıkış | Alfa (bps) |
|---|---|
| Ertesi açılış | +24 |
| 1. gün kapanışı | +98 |
| 2. gün kapanışı | +139 |
| 3. gün kapanışı | +143 |

İkinci gün ortalamada ekliyor (medyan +92 bps), üçüncü gün eklemiyor. Açılışta satmak kazancın dörtte üçünü bırakmak demek.

**Dönem dönem.** 2011'den beri VIX'in 30'u aştığı 18 dönemin 17'sinde kural artıdaydı. Tek eksi dönem Nisan 2025 (gümrük vergisi çöküşü): işlem başına −26 bps, iki günde −180. 2020 yılı tümüyle çıkarılınca ortalama +72 bps. En kötü tek işlem −%10,6.

**Maliyet ve yürütme.** Stres günlerinde makas açılır. 30 bps maliyet varsayımıyla bile işlem başına +68 bps kalıyor. Kapanışta değil ertesi açılışta alırsan (bütün günler ortalaması) açılıştan kapanışa +11 bps, ikinci kapanışa +20 bps kalıyor.

**Yıllık getiriye çevirirsek.** Kural bütün günlerde ve altı ETF'te uygulandığında yıllık bileşik net %8 verdi; aynı ETF'leri alıp tutmak %18. Yani bu kural "al-tut'u yener" değil; "zamanın küçük bir kısmında piyasada kalarak, o kısımda ortalamanın üstünde kazanır". Yalnız stres günlerine indirildiğinde işlem sayısı ETF başına yılda ortalama 4–5'e düşer ve hepsi 2011, 2020, 2022 gibi yıllara yığılır.

**Dürüst uyarı.** "VIX ≥ 30" koşulu, önceden tanımlı rejim hücrelerinden biriydi ama 61 birincil testten biri değildi. Önceden kayıtlı olan, kuralın VIX 25 üstü ile altı arasındaki farkıydı; o test eşiğin hemen altında kaldı (t 2,44) ve çürütmede zayıfladı. Dolayısıyla stres kuralı güçlü bir bulgu ama 18 döneme dayanıyor; kesin bir yasa değil.

### 4.4 Aynı kural kaldıraçla

| | SOXL | TQQQ |
|---|---|---|
| Kendi IBS'i < 0,2, bütün günler: alfa | +100 bps (t 3,2; 524 işlem) | +38 bps (t 2,1; 700 işlem) |
| Stres günlerinde, 1 gün | +309 bps (65 işlem) | — |
| Stres günlerinde, 2 gün | +438 bps | — |
| En kötü tek işlem | −%31,9 (19→20 Kas 2026) | −%18,4 (3→4 Nis 2025) |
| En uzun kayıp serisi | 6 işlem, toplam −%42 | 11 işlem, toplam −%40 |
| %33 pozisyonla yıllık bileşik | %12,8 | %6,7 |
| %33 pozisyonla en büyük düşüş | −%18 | −%18 |

Üç not:

- SOXL sinyalleri SMH sinyalleriyle aynı günlere düşüyor. Bu bağımsız bir kanıt değil, aynı bahsin 3 katı.
- Son üç yılda SOXL'un kendisi çok yükseldiği için, aynı sıklıkta rastgele günlerde alan birinin en iyi %5'lik sonucu (%60) bu kuralın sonucunu (%46) geçiyor. Yani 2023 sonrasında kuralın katkısı şanstan ayırt edilemiyor; tam dönemde ediliyor.
- 2026 bu kuralın SOXL'da iki yüzünü de gösterdi: 5 Kasım kapanışında alan ertesi gün +%12,5 kazandı; 19 Kasım kapanışında alan ertesi gün −%31,8 kaybetti. 13–20 Kasım haftasında SOXL ve TQQQ'daki dört işlemin (ikişer tane) toplamı −%49.

### 4.5 Lead-lag: neden bir şey çıkmadı

Test edilenler: Asya ve Avrupa liderlerinden ABD'ye (TSMC → TSM ve Nvidia; SK Hynix ve Samsung → Micron ve disk hisseleri; Tokyo Electron ve ASML → ekipman hisseleri), ABD devlerinden takipçilere (Nvidia, TSMC, Broadcom, Micron, Microsoft, Google, Meta, Amazon → diğer 39 hisse), emsal sepetinden geride kalana, makro göstergelerden (faiz, dolar, yen, bakır, kredi) Nasdaq ve SMH'ye, Bitcoin'den madencilere, lider bilançosundan emsallere. Ayrıca 43 öncülün iki hedef havuzuna karşı veriden taraması (84 geçerli kombinasyon).

Sonuç:

- **27 testin hiçbiri geçmedi.** Taramada da keşif aşamasını geçen kombinasyon çıkmadı.
- **Neden:** Liderin getirisini bir gün ileri kaydırınca (yani aynı günü kullanınca) ilişki çok güçlü çıkıyor; ertesi güne ise bir şey kalmıyor. Bilgi aynı gün fiyatlanıyor. Bu, VİOP çalışmandaki "açılış boşluğunda fiyatlanıyor" bulgusuyla aynı.
- **Tek istisna alım sinyali değil:** Tokyo Electron ve ASML'nin zayıf günü, ABD ekipman hisselerinde (AMAT, LRCX, KLAC) ertesi gün yaklaşık −20 bps ile ilişkili. Bu bir "o gün ekipman alma" bilgisi; alım yönünde karşılığı yok.
- **Bitcoin:** Bitcoin'in güçlü yükseldiği günün ertesinde madenci ve yapay zekâ veri merkezi hisseleri ortalama −100 bps (3 günde −263). Kovalamak zararlı.
- **Güç hesabı:** Havuzlanmış testler 11 bps'lik bir kenarı ayırt edebilecek güçteydi; bulunan eğimler ±4 bps düzeyinde. Bu hisselerde maliyet 20 bps. Yani bulamadığımız bir lead-lag varsa bile maliyeti karşılamaz.

Literatür de aynı yönde: güçlü lead-lag bulguları (müşteri–tedarikçi, ortak analist) aylık ufukta; büyük hisseler arasındaki günlük lead-lag 2000'e kadar kaybolmuş.

### 4.6 Elenenler hakkında kısa notlar

- **Bilanço öncesi alım.** 2010–2019'da işlem başına +90 bps'ti; 2020–2022'de +39; 2023'ten beri +14 (anlamsız); 2025'te −33, 2026'da −88. Bu sezon beklentiyi aşan teknoloji şirketleri bilanço günü ortalama −%1,5 tepki gördü.
- **Sert yükselişten sonra alım.** SOX +%3 ve üstü gününden sonra SMH ertesi gün ortalama −42 bps; +2 standart sapma gününden sonra −41 bps. Etki 2020–2022'den geliyor, son üç yılda sıfıra yakın. Sonuç: alım için gerekçe yok.
- **SMH'nin −%8 ve altı günleri.** 2010'dan beri 9 gün (20 Kasım dahil). Ertesi gün ortalama +%3,6 ve 8'in 7'si artı; ama dördü Mart 2020'de ve 3 Nisan 2025'in ertesi günü −%7,6 idi. Üç gün sonra ortalama sıfır.
- **Son 30 dakika.** "Düşüş gününde son yarım saat de aşağıysa ertesi gün döner" fikri ilk ölçümde iyi göründü (+85'e karşı −3 bps) ama ölçüm biçimine dayanıksız çıktı: gerçek kapanış fiyatıyla fark 27 bps'e indi ve örneklem 65 gün. Kural olarak kullanma.
- **Gece ve gün içi.** 2023'ten beri SMH'nin getirisi neredeyse tamamen gecede oluştu (günde +16 bps'e karşı gün içi +1). Ama bu genel bir betimleme; sinyal günlerinde açılışta satmak en kötü seçenek çıktı.

## 5. Piyasa şu an nerede, önümüzde ne var

**2026'nın özeti.** Yarı iletken endeksi SOX 22 Haziran'da 14.634,72 ile rekor kapanış yaptı. 5 Haziran'da −%10,3, 5 Kasım'da −%12,25 (kayıtlardaki en kötü ikinci gün), 20 Kasım'da −%10,7 düştü. SMH zirvesinin %40 altında.

**Kasım'da üst üste binenler** (hepsi en az bir kaynaktan doğrulandı):

- Fed faiz artırıyor: Eylül'de 25 baz puan artırdı, 28 Ekim'de 10'a 2 oyla bekledi (iki üye artış istedi). Aralık artışı %90'ın üstünde olasılıkla fiyatlanıyor.
- Ara seçimlerde Demokratlar Kongre'yi kazandı; veri merkezi kısıtlaması korkusu 5 Kasım düşüşünde anıldı.
- Nvidia'da Jensen Huang 12 Kasım'da CEO'luktan ayrıldı; Colette Kress geçici CEO. WSJ, SEC'in şirketin açıklamalarını incelediğini yazdı (isimsiz kaynak, resmî teyit yok). 17 Kasım bilançosu güçlüydü: gelir 115,8 milyar $, sonraki çeyrek yönlendirmesi 130 milyar $.
- 19 Kasım'da açığa satıcı Hunterbrook AMD hakkında rapor yayımladı; AMD reddetti.
- 20 Kasım: Nasdaq −%5,28, S&P 500 −%3,70, VIX 35,89.

**Bellek döngüsü.** DRAM sözleşme fiyatları 4. çeyrekte hâlâ artıyor (+%10–15). Flaş bellekte (NAND) dönüş başladı: TrendForce 19 Kasım'da 2027'nin ilk çeyreği için %0–5 düşüş öngördü. Goldman'ın bellek sepeti Haziran zirvesinden −%51.

**Takvim (kesinleşmiş olanlar).** Bunlar sinyal değil, risk günleri:

| Tarih | Olay |
|---|---|
| 23 Kas | HPE bilançosu (kapanış sonrası) |
| 24 Kas | Dell bilançosu |
| 26 Kas | Borsa kapalı (Şükran Günü) |
| 27 Kas | Erken kapanış, 13:00 ET |
| 1 Ara | Marvell, NetApp, Credo bilançoları (kapanış sonrası) |
| 4 Ara | İstihdam verisi |
| 9 Ara | Fed kararı; Broadcom bilançosu (kapanış sonrası) |
| 10 Ara | Enflasyon (TÜFE); Ciena bilançosu (açılış öncesi); TSMC Kasım geliri |
| 15 Ara | Üretici fiyatları (ÜFE) |
| 17 Ara | Micron bilançosu, 16:30 ET |
| 18 Ara | Üçlü opsiyon vadesi |
| 24 Ara | Erken kapanış; 25 Ara ve 1 Oca kapalı |
| 6–9 Oca | CES 2027 |
| 8 Oca / 13 Oca | İstihdam / TÜFE |
| 26–27 Oca | Fed toplantısı |

Resmî olmayanlar: Oracle bilançosu (10–14 Aralık), TSMC 4. çeyrek bilançosu (yaklaşık 14 Ocak), Samsung ön bilançosu (yaklaşık 7–8 Ocak), Nasdaq-100 yeniden yapılandırması (kurala göre duyuru 11 Aralık, yürürlük 21 Aralık).

**20 Kasım kapanışında sinyal durumu.** VIX 35,9; altı ETF'in hepsinde IBS 0,2'nin altında (SMH 0,08). Kural açıktı. Piyasa pazartesi açılıyor; kapanış girişi artık mümkün değil. Stres günlerinde kazancın yaklaşık dörtte biri gecede, dörtte üçü ertesi açılıştan sonra oluştu (98'e karşı 24 bps; ikisinin farkından çıkarım).

## 6. Erişim, maliyet, vergi

- **Kanal.** SPK'nın 17 Haziran 2026 tarihli kararıyla bankalar yurt dışı hisse emrine doğrudan aracılık edemiyor; işlem SPK yetkili aracı kurum üzerinden yapılıyor.
- **Komisyon** (gidiş-dönüş, 5.000 $ pozisyon): Midas işlem başı 1,5 $ → 6 bps. İş Yatırım %0,25 → 50 bps. Garanti BBVA Yatırım binde 3 → 60 bps. Interactive Brokers hisse başı 0,005 $, asgari 1 $ → 2–4 bps (Türkiye'den hesap açılabildiği yalnız ikincil kaynaklara dayanıyor).
- **Emir.** Midas'ta piyasa, limit, stop emirleri ve seans dışı işlem var; kapanış müzayedesi emri bulunamadı. Interactive Brokers'ta var.
- **Kur.** Çevirme maliyeti işlem başına değil, para girip çıkarken ödenir. Doları hesapta tutarsan 1–3 günlük işlemlere yansımaz.
- **Vergi** (Gelir İdaresi'nin 2026 rehberi): Yurt dışı hisse ve ETF kazancı değer artış kazancı olarak yıllık beyannameyle bildirilir; menkul kıymetlerde istisna tutarı yok. Aynı yıl içindeki zarar kârdan düşülür. ABD temettü stopajı bireyler için %20. Sık işlem yapan biri için beyan yükü ve TL bazında kur farkı önemli; bir mali müşavirle teyit et.

## 7. Emin olunmayanlar ve doğrulama kapsamı

**Emin olunmayanlar:**

- Stres kuralı 18 döneme dayanıyor ve son iki dönemden biri (Nisan 2025) eksiydi. Bu dönemin, yani Kasım 2026'nın nasıl biteceği bilinmiyor.
- "VIX ≥ 30" eşiği önceden tanımlı bir hücreydi ama birincil test değildi.
- Kaldıraçlı ETF'lerin Türkiye'deki aracı kurumlarda alınıp alınamadığı ve kapanış emri doğrulanamadı.
- Stres günlerinde gerçek alım-satım makası ölçülemedi; 30 bps varsayımıyla sonuç hâlâ artı.
- 15:30 testi yalnız son iki yılın saatlik verisine dayanıyor.
- Hafta sonu (21–22 Kasım) haber akışı bulunamadı.

**Doğrulama kapsamı:**

- **Sayısal:** 61 birincil test ve 84 kombinasyonluk tarama. Ayakta kalan ve kaçınma bulgusu olan 7 test bağımsız olarak yeniden kodlandı; yedisi de işlem sayısı ve alfa bakımından birebir tuttu. Çürütme turunda 8 saldırı denendi: iki aday kural ve bilanço kuralı çürüdü, ana kural stres günlerine daraldı, "en çok 1 gün tut" çıkarımımız çürüdü ve düzeltildi.
- **Kaynak iddiaları:** 130 iddia kontrol edildi: 98 doğru, 20 düzeltildi, 11 doğrulanamadı, 1 yanlış. Yanlış olan HPE bilanço tarihiydi (3 Aralık değil 23 Kasım). Düzeltilenlerin çoğu fon büyüklükleriydi (ör. SOXX 44 değil 31 milyar $). Raporda yalnız düzeltilmiş değerler var.
- **Kontrol edilmeyenler:** Hisse evreni defterlerindeki şirket bazlı ayrıntılar (gelir, borç rakamları) tek kaynaklıdır ve bu rapora alınmadı; ek dosyalarda duruyor.
- **Bulunan ve düzeltilen hatalar:** Etiketleme kodunda bir aile adı hatası (sonucu değiştirmedi); Yahoo'da SanDisk'in bölünme günü boş kapanışı (saatlik veriden yamandı); Bitcoin ve kur verilerinde zaman damgası kayması (hesaplardan önce yakalandı).

## 8. Kaynaklar

Kendi hesaplarımız: `kod/` (betikler) ve `ek/` (özet tablolar). Fiyat verisi: Yahoo Finance.

Piyasa ve şirket haberleri:
- Nvidia bilançosu: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/
- Nvidia CEO değişikliği: https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition
- SEC incelemesi haberi: https://www.thestar.com.my/tech/tech-news/2026/11/18/nvidia-facing-sec-probe-after-huang039s-resignation-wsj-reports
- 5 Kasım düşüşü: https://247wallst.com/investing/2026/11/06/chip-stocks-just-had-their-second-worst-day-on-record/
- 5 Haziran düşüşü: https://profit.pakistantoday.com.pk/2026/06/06/us-listed-chipmakers-slump-erases-dollar13-trillion-in-stock-market-value
- Fed kararı: https://stockanalysis.com/news/fed-holds-rates-steady-oct-2026/
- Fed takvimi: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Veri takvimi: https://www.bls.gov/schedule/2026/12_sched_list.htm
- Broadcom bilanço tarihi: https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announce-fourth-quarter-and-fiscal-year-2026
- Marvell bilanço tarihi: https://investor.marvell.com/news-events/press-releases/detail/1041/marvell-technology-inc-announces-conference-call-to-review-third-quarter-of-fiscal-year-2027-financial-results
- TrendForce NAND: https://www.trendforce.com/presscenter/news/20261119-13314.html
- TrendForce DRAM: https://www.trendforce.com/presscenter/news/20260930-13258.html
- Bellek sepeti: https://investinglive.com/stocks/goldman-s-ai-memory-basket-plunges-51-from-peak-jpmorgan-sees-earnings-buffer-for-now/

ETF ve düzenleme:
- Roundhill DRAM: https://www.roundhillinvestments.com/etf/dram/
- SOXL: https://stockanalysis.com/etf/soxl/
- SPK kararı: https://spk.gov.tr/data/6a3300ca8f95db19fcfc205f/2026-39.pdf
- Gelir İdaresi rehberi: https://intvrg.gib.gov.tr/hazirbeyan/assets/pdf/DUYURU_UNIVERSAL_2026_Diger_Kazanc_ve_Iratlar_2026.pdf
- Temettü stopajı tablosu: https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf
- Midas ücretleri: https://www.getmidas.com/ucretler/
- İş Yatırım tarifesi: https://www.isyatirim.com.tr/tr-tr/destek/Documents/pdf/komisyon-ve-masraf-tarifesi.pdf

Akademik:
- Nagel (2012), dönüş getirisi ve VIX: https://www.nber.org/papers/w17653
- Drechsler, Moreira, Savov (2018): https://conference.nber.org/conf_papers/f103855.slides.pdf
- Baltussen, van Bekkum, Da (2019), endekslerde negatif otokorelasyon: https://www3.nd.edu/~zda/Indexing.pdf
- IBS üzerine (uygulayıcı): https://jonathankinlay.com/?p=2199
- Baltussen, Da, Soebhag, gün sonu dönüşü: https://academicweb.nd.edu/~zda/EOD.pdf
- Martineau, bilanço sonrası sürüklenme: https://ideas.repec.org/p/osf/socarx/z7k3p.html
- Etula ve ark. (2020), ay sonu: https://acris.aalto.fi/ws/portalfiles/portal/40965155/hhz054.pdf
- Hou (2007), sektör içi lead-lag: https://econpapers.repec.org/RePEc:oup:rfinst:v:20:y:2007:i:4:p:1113-1138
- Tóth, Kertész, günlük lead-lag'in kaybolması: https://arxiv.org/abs/physics/0506071
- Cohen, Frazzini (2008), müşteri–tedarikçi: https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1977-2011.html
- Mourey ve ark. (2025), kripto hafta sonu: https://econpapers.repec.org/RePEc:hal:journl:hal-05415054

## 9. Devam notu

- **Bulgu:** 61 testten tek kural kaldı: VIX ≥ 30 iken IBS < 0,2 kapanan endeks ETF'ini (SMH, QQQ; kaldıraçlı SOXL, TQQQ) kapanışta al, 1–2 gün tut. Lead-lag yok; bilanço öncesi alım bitti.
- **Ana dosyalar:** `RAPOR.md` (bu dosya), `kod/PROTOKOL.md` (test tanımları), `kod/sinyal.py` (günlük sinyal), `ek/risk_tablosu.csv` (98 araç).
- **Sonuç tabloları:** `ek/d2_b1.md`, `ek/d2_b2.md`, `ek/d2_b3.md` (backtest), `ek/d3_curutme.md` (çürütme), `ek/d3_yeniden_kodlama.md`.
- **Yeniden üretim:** `python3 kod/indir.py` (veri), sonra `kod/b1_fiyat.py`, `b2_leadlag.py`, `b3_takvim.py`, `curutme.py`. `veri/` klasörü depoda yok; indir.py yeniden üretir.
- **Açık kalanlar:** aracı kurumda SOXL ve kapanış emri teyidi; Kasım 2026 stres döneminin sonucu; stres günlerinde gerçek makas.
