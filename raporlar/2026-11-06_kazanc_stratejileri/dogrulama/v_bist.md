# Doğrulama: BIST raporları (bist_kim_kazaniyor, bist_swing_kenarlar, bist_test), 06.11.2026

Karşı-doğrulayıcı raporu. Kapsam: üç ajan raporundaki karar açısından önemli iddialar, backtest kod denetimi ve eksikler. Yatırım tavsiyesi değildir.

## 0. Yöntem ve kısıtlar

- **Web arama kotası doluydu.** Oturumun ortak 200 aramalık kotası bu ajan başlamadan bitmişti; WebSearch hiç çalışmadı. Bu yüzden doğrulama şunlarla yapıldı:
  - Birincil kaynakların doğrudan indirilmesi: TSPB Excel ve PDF'leri, SPK bültenleri (2026/50–78, 29 bülten bu ajan tarafından ayrıca indirildi), TCMB faiz tabloları, Borsa İstanbul VİOP vergi sayfası, MPRA ve DergiPark PDF'leri.
  - İş Yatırım fiyat verisinin bağımsız olarak yeniden indirilmesi (XU100, USDTRY).
  - Oturumda daha önce indirilmiş fonveri.com (TEFAS kapanışı, 06.11.2026) fon getiri tablosu: 956 fon, 47 para piyasası fonu (PPF).
  - Ajan kodlarının okunması ve yeniden koşturulması.
- **Erişilemeyenler (atlatma yapılmadı):** Boğaziçi dijital arşivi (güvenlik doğrulaması), EconBiz (Anubis bot koruması), SSRN ve ScienceDirect (403), PwC (403).
- **Betikler** (bu ajan yazdı): `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/verif_bist/kod/` altında `rerun_t03.py`, `rv_lag.py`, `h52_lag.py`. İndirilen ham dosyalar: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/verif_bist/`.

---

## 1. Hüküm tablosu

| # | İddia (rapor) | Hüküm | Düzeltme / not | Kaynak |
|---|---|---|---|---|
| 1 | Kaldıraçlı FX'te zararda olan hesap oranı: 41 çeyrek ortalaması %67, 2026/06'da %74,4, çeyrek aralığı %52–80 (kim) | **DOĞRU** | 41 çeyrek, 28–34 kurum ile yeniden hesaplandı: ortalama %67,0; 2022/12'de %52,0; 2016/12'de %80,0; 2026/06'da %74,4 (medyan %77,0). Oranlar ağırlıksız ve çeyreklik anlık görüntü; kümülatif zarar oranı değil. | https://tspb.org.tr/wp-content/uploads/2026/07/1_TSPB-Kar-Zarar-2026-2.xlsx (MD5, ajanın dosyasıyla aynı) |
| 2 | Erdem-Arık-Yüksel: bireyler endeksin haftada −%0,281 gerisinde; en yüksek devir dilimi −%0,538; en büyük portföy −%0,104; yatırımcıların ≈%70'i endeksi yenemiyor (kim) | **DOĞRU, bir nüansla** | Rakamlar Tablo 2 ve Tablo 5 ile birebir aynı. Nüans: tüm örneklemin CAPM alfası −%0,24/hafta ama t=−1,51, yani anlamsız. Anlamlı alfa yalnız küçük portföy dilimlerinde var. Geride kalmanın bir kısmı beta/piyasa etkisi. Örneklem yalnız 2011–12 (iki yıl). Okunan sürüm MPRA çalışma kağıdı (Mayıs 2013). | https://mpra.ub.uni-muenchen.de/46804/1/MPRA_paper_46804.pdf |
| 3 | TSPB 2025: müşteri faiz geliri 53.138 mn TL, aracılık geliri 32.316 mn TL; Tera Yatırım sektör kârının %35'i; "örtük kredi maliyeti ≈%45–50" (kim) | **Gelir rakamları DOĞRU; maliyet tahmini KISMEN** | Tablo 15 ve sayfa 16 teyit edildi. Kredi hacmi 62,7 milyar TL'den 109,9 milyar TL'ye çıktı. Bu iki bakiyenin ortalamasıyla 53,1 milyar TL faiz geliri **≈%60** örtük maliyet eder. Yani kredili spot işlemin engeli raporun dediğinden de yüksek. | https://tspb.org.tr/wp-content/uploads/2026/07/1-AK_202512-FINAL.pdf |
| 4 | TSPB 2026/03: yerli bireyler pay hacminin %48,5'i; DMA pay işlemlerinin %93'ü 2 kurumda; yabancı kurumlar vadeli hacminin %47'si (kim) | **DOĞRU** | Tablo 2'de yerli bireyler %48,5, yabancı kurumlar vadelide %47,0. DMA kanalı pay hacminin %28'i. DMA'yı "genellikle yüksek frekanslı ve/veya algoritmik işlem yapan yurtdışı kurumlar" kullanıyor (TSPB'nin ifadesi). | https://tspb.org.tr/wp-content/uploads/2026/09/Gosterge_Yaz_2026_.pdf |
| 5 | Tasfiyede 131 fon, 619,7 milyar TL (kim) | **Fon sayısı DOĞRU; tutar DOĞRULANAMADI** | SPK kararı 17.09.2026 tarihli (57/1706-1707), 7 portföy şirketi. Listede ≈130–131 fon var: Pardus 42, Hedef 31, Atlas 16, Bulls 15, Pusula 12, A1 9, Tera 5. Bunların **15'i PPF**. 619,7 milyar TL ve 722.914 yatırımcı yalnız Fonoloji'de var. | https://spk.gov.tr/data/6aab8e7b8f95db07100fd7b4/2026-60.pdf |
| 6 | "28.08.2026'da SPK fon rehberi değişti; fiili dolaşımı %25'in altındaki şirkette tek bir fon en fazla %8 tutabilir" (kim) | **KISMEN** | 28.08 tarihli Rehber değişikliği SPK 2026/54'te var. %8 sınırı birincil metinden okunamadı; Euronews bu sınırı "bir serbest fon" için veriyor. Raporun atladığı iki ilke kararı var. 31.08 kararı (2026/55) borsa dışı satışa %2/%4 sınırı getirdi. 03.09 kararı (2026/57) fiili dolaşımı MKK bazında yeniden tanımladı ve 11.09'dan itibaren günlük yayımlanmasını öngördü. | https://spk.gov.tr/data/6a91fe798f95db1fb01ff364/2026-54.pdf ; https://spk.gov.tr/data/6a959d0c8f95db2178a69d38/2026-55.pdf ; https://spk.gov.tr/data/6aa03af78f95db162c4bf407/2026-57.pdf ; https://tr.euronews.com/2026/09/17/turk-piyasalarinda-fon-skandali-tam-olarak-ne-oldu-ve-sirketler-neyle-suclaniyor |
| 7 | Kredili işlemde özkaynak oranının %35'ten %20'ye esnetilmesi 13.11.2026'ya uzatıldı (kim) | **DOĞRU** | Karar zinciri: 17.09'da 02.10'a kadar (2026/60), 03.10'da 30.10'a kadar (2026/68), 30.10'da 13.11'e kadar (2026/78). | https://spk.gov.tr/data/6ae4bb608f95db1f5c91eb9c/2026-78.pdf |
| 8 | Pusula 15.09'da temerrüde düştü; Eylül'de açığa satış yasağı var mıydı? | **DOĞRULANAMADI** | SPK 2026/55–78 bültenlerinde temerrüt ifadesi ve açığa satış yasağı geçmiyor. Açığa satış yasağı Borsa İstanbul kararı olacağı için BIST duyuruları ayrıca kontrol edilmeli. Temerrüt bilgisi haber kaynaklı. | SPK bültenleri (`verif_bist/spk/`) |
| 9 | BIST100 31.08–30.10 arasında −%24,94; 16.09'da −%5,54 ile 13.122; "2026 başından beri −%4,5" (kim) | **DOĞRU, tarih notuyla** | Bağımsız indirmeyle −%24,94, −%5,54 ve 13.122,6 teyit edildi. −%4,5, 30.10 itibarıyla doğru. 05.11 itibarıyla YTD **+%0,6** (11.261 → 11.333). 2026 zirvesi 11.05.2026'da 15.134. | İş Yatırım ChartData XU100 (yeniden indirildi) ; https://www.endeks24.com/bist-100-iki-ayda-yuzde-25-dustu |
| 10 | "28.08 kuralından sonra XU030 ve banka short'u 30.10'a kadar ≈+%25" (kim) | **KISMEN** | 28.08–30.10 arasında XU030 −%20,1, XBANK −%12,6, XUTUM −%34,3. Vadeli short'un taşıma getirisi (≈%36 × 2 ay ≈ +5–6 puan) eklenince XU030 short ≈+%25 tutar. Banka short'u ≈+%18 olur, %25 değil. Gözlem sayısı 1 (n=1). | `data/bist_test/endeks` (İş Yatırım) |
| 11 | 2026 halka arzları ortalama −%29, 36 arzın 27'si arz fiyatının altında; 2025–26'da seri bittikten sonra 53 hissenin 52'si düştü (kim) | **KISMEN** | hocaileborsa 30.10 tablosu teyit edildi: 36 arz, ortalama −%29, 9 pozitif / 27 negatif. Ama arzanaliz'in "güncel getiri" alanı bedelsize göre düzeltilmemiş. AKFIS −%64 görünüyor, düzeltilmiş getirisi **+%116**; VSNMD −%46 görünüyor, düzeltilmişi −%16; ZGYO +%16 görünüyor, düzeltilmişi +%27. İş Yatırım'la eşleşen 36 arzda medyan −%36,8'den −%34,6'ya değişiyor. Yön aynı; "52/53" sayısı muhtemelen 50–51/53. | https://www.hocaileborsa.com/halka-arz/tavan-serisi ; İş Yatırım HisseTekil (raw/adj faktörü) |
| 12 | MAC: 5 yılda +%2.643, son 1 yılda −%6,9 (kim) | **KISMEN** | +%2.643, Ağustos 2025'te biten 5 yıllık penceredir. fonveri'de 06.11.2026 itibarıyla 5 yıl **+%899**, 1 yıl −%6,3. Aynı tarihte hisse fonu medyanı 5 yılda +%838. Yani MAC'ın 5 yıllık üstünlüğü de neredeyse kayboldu; tez güçleniyor. | fonveri.com tüm fonlar tablosu (06.11.2026) |
| 13 | TL engeli: "net ≈%36" (kim); "PPF stopaj sonrası %31–33" (swing) | **swing YANLIŞ, kim KISMEN** | Gerçekleşen değerler: PPF medyanı (47 fon) 1 yılda brüt **+%45,5**; %17,5 stopajla ≈**%37,5**. 3 yılda +%258,7, yani **yılda %53,1** brüt; stopaj sonrası yılda ≈%46. 3 aya kadar mevduat %43,79 basit faizle %17,5 stopaj sonrası bileşik ≈**%41**. Kim'in %36'sı basit faizdir, alt sınırdır. Reel politika faizi ≈%4,8 doğru. | fonveri (TEFAS) ; Endeks24 (TCMB haftalık mevduat istatistiği) |
| 14 | TCMB 22.10.2026'da %37'den %36'ya indirdi; koridor %34,5–39 (swing) | **DOĞRU** | TCMB tablosunda yürürlük 23.10.2026. 2026'da koridor değişikliği yalnız 23.01 ve 23.10'da. | https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo ; .../faiz-oranlari |
| 15 | VİOP'ta bireysel stopaj pay ve pay endeksi sözleşmelerinde %0, diğerlerinde %10; PPF'de bireysel stopaj %17,5; 11734 sayılı karar kurumsal PPF stopajını %0'dan %10'a çıkardı (swing) | **VİOP DOĞRU; PPF KISMEN** | VİOP oranları BIST tablosunda teyit edildi. İş Portföy, 11734 sayılı kararı teyit ediyor (RG 05.09.2026, 33361). %17,5'i 9.7.2025 tarihli "genel fon stopajı" duyurusu olarak veriyor; gerçek kişi PPF oranı ayrıca yazılmamış. | https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme ; https://www.isportfoy.com.tr/medya-ve-blog/para-piyasasi-fonlarinda-kurumlara-uygulanan-stopaj-duzenlemesi-hakkinda-eylul-2026 |
| 16 | PSR oranları: XU030 %20, pay vadelilerinin çoğu %33,3, ASTOR/HALKB/VESTL %100, USDTRY %33,3 (swing) | **KISMEN** | Rakamlar doğru, ama bunlar QNB Invest'in kendi kurum PSR'si; Takasbank asgarisi değil. Ayrıca GUBRF %50, CNH %100. | https://www.qnbinvest.com.tr/duyuru/viop-psr-oran-guncellemesi-03112026 |
| 17 | Ünal (2021): kazananlar (6 ay oluşum) izleyen 12 ayda %29,7, diğer dilimler %37–41, t=7,3 (swing) | **DOĞRU** | Tablo 1 ile aynı: t=7,31. Çakışan getiriler t'yi şişirir. Çalışma eşit ağırlıklı ve tüm hisseleri kapsıyor. | https://dergipark.org.tr/en/download/article-file/1419417 |
| 18 | Avcı (2024, EJF): içeriden işlem sonrası 1 yılda %6,58 anormal kâr; taklit portföyü piyasayı yenebiliyor (swing) | **DOĞRU** | Özet teyit edildi: 2008–2019, ≈65.000 işlem. Getiri brüt ve maliyetsiz; KAP bildirim gecikmesi tam metinde. | https://research.sabanciuniv.edu/id/eprint/50115 |
| 19 | Bildik & Gülay (2007): zıtlık stratejisi yılda ≈%15 anormal; Tiniç & Salih: PIN getiri öngörmüyor (swing) | **DOĞRU** | Bildik-Gülay bu getiriyi ek risk primi olarak yorumluyor; dönem özetten teyit edilemedi. Tiniç-Salih, Applied Economics 52(13). | https://ideas.repec.org/a/bla/irvfin/v7y2007i1-2p61-87.html ; https://avesis.tedu.edu.tr/yayin/addb0698-c56a-492c-b751-360645ffdf84/informed-trading-order-flow-shocks-and-the-cross-section-of-expected-returns-in-borsa-istanbul |
| 20 | Gökçen: BIST'te en güçlü faktör değer; momentum yalnız 2005 sonrası anlamlı (swing) | **KISMEN** | İkincil özet "value is the strongest" diyor; değer primi tam örneklemde yılda %19, sonraki kısımda %14. Momentum için "2005 sonrası" bulgusu doğrulanamadı (SSRN ve ScienceDirect 403). | https://paperswithbacktest.com/strategies/factor-investing-in-the-turkish-equity-market |
| 21 | Ahlatçıoğlu-Okay PEAD %2,9/60 gün; Aslan (2019) BIST30 çıkışları −%4,07; Ülkü-İkizlerli yabancı akımı | **DOĞRULANAMADI** | Boğaziçi arşivi ve EconBiz bot koruması nedeniyle erişilemedi. | — |
| 22 | XU100 2010–26 arasında yılda %20,0 TL, 2024–26 arasında %15,8; USDTRY 1,474'ten 50,048'e (test) | **DOĞRU** | Bağımsız indirmeyle %19,9 ve %15,7. Ajan dosyasıyla en büyük fark %0,03. USDTRY 2026 YTD +%16,5. | İş Yatırım ChartData |
| 23 | "TL rf (TCMB 1 hafta repo) stopaj öncesi; engeli olduğundan yüksek gösterir, muhafazakâr" (test, swing) | **YANLIŞ** | Seri basit politika faizini yıllık efektif oran gibi kullanıyor. Son 1 yılda %37,3 verdi; PPF medyanı brüt %45,5. Kasım 2023–Kasım 2026 arasında seri yılda %43,1, PPF yılda %53,1 brüt, ≈%46 stopaj sonrası. Yani seri **vergi sonrası** gerçekleşen nakdin bile ≈3 puan/yıl altında. Ayrıntı §2.1'de. | `verif_bist` hesapları ; fonveri |
| 24 | 52 haftalık zirveye yakınlık "tek sağlam sinyal": 2016–26 Q5−Q1 +%1,56/ay, t=2,22 (swing) | **KISMEN** | Birebir yeniden üretildi. Bir gün gecikmeli girişte sinyal güçleniyor (+%1,83, t=2,47). Ama **2022 çıkarılınca** Q5−Q1 +%1,12 (t=1,50), Q5−EW +%0,35 (t=0,85). Long-only için anlamlılık büyük ölçüde tek yıla (2022) dayanıyor. | `h52_lag.py` |
| 25 | SAHOL↔AKBNK işlem başına +250/+388 bps; KCHOL↔sepet +212/+244 bps; iki alt dönemde t 2,8–3,8 (swing) | **KISMEN** | Kod, sinyalin oluştuğu kapanışta giriş varsayıyor; maliyet yok. Bir gün gecikmeyle SAHOL↔AKBNK 160/310 bps (t 2,4/2,8), KCHOL↔sepet 128/175 bps (t 2,1/2,1). Maliyet sonrası (20/40 bps) 88–290 bps. Kenar duruyor ama %30–45 küçük. Bu çiftler de önceki çalışmadan seçilmişti (seçim yanlılığı). | `rv_lag.py` |
| 26 | Temettü hak kullanımından önceki 5 gün +%1,2, t=7,8, n=1.109 (swing) | **DOĞRU** | Haftalık kümelenmeye göre t=6,5 (365 hafta). Ortalama 17 yılın hepsinde pozitif; medyan 2014 ve 2026'da negatif. İşlem başına küçük: maliyet sonrası ≈%0,9. | `bsk/events.pkl` |
| 27 | 2026'da ODINE 42 gün, PEKGY 31 gün taban kapattı (swing) | **DOĞRU** | ≤−%9,5 kapanan gün sayısı. ODINE'de en uzun ardışık seri 29 gün. DSTKF 47 gün, en uzun ardışık 35; KTLEV 31 gün. | İş Yatırım ham kapanış |
| 28 | Kırılım S2 + %15 iz-stop: 2.073 işlem, ortalama +%11,4, en iyi %5 işlem net kârın ≈%70'i; portföy CAGR %50,9 (test) | **DOĞRU (yeniden koşum), yorum KISMEN** | Birebir üretildi: CAGR %50,9, Sharpe 1,19, MaxDD −%38,6; en iyi %5 işlem kârın %69,6'sı. En büyük kazançlar KTLEV +%593, ODINE +%520, HEDEF ve PEKGY. Bunlar 2026'da −%93 ile −%98 çöken pump hisseleri. | `rerun_t03.py` |

---

## 2. Backtest denetimi (bist_test kodu ve bist_swing'in `bsk/kod` kodu)

### 2.1 Risksiz faiz serisi düşük (en önemli bulgu)

**Sorun.** İki kod da `rf_d = (1 + r)^(dt/365) − 1` kullanıyor; yani %37'lik basit politika faizini yıllık efektif getiri sayıyor. Gerçek PPF ve repo getirisi günlük bileşiyor. %37'nin günlük bileşik karşılığı ≈%44,7.

**Gerçekleşen PPF ile karşılaştırma** (fonveri, 47 PPF'nin medyanı, ücret sonrası, stopaj öncesi):

| Pencere | Ajan serisi | PPF medyanı (brüt) | PPF, %17,5 stopaj sonrası |
|---|---|---|---|
| 1 yıl | %37,3 | %45,5 | ≈%37,5 |
| 3 yıl, yıllık | %43,1 | %53,1 | ≈%46 |

**Yeniden koşum** (S2 + %15 iz-stop, 2024–26):

| rf varyantı | rf CAGR | Strateji CAGR | Fazla |
|---|---|---|---|
| Ajanın serisi | %43,9 | %125,1 | +%56,5 |
| Günlük bileşik (brüt) | %55,0 | %126,6 | +%46,2 |

**Sonuçlar:**
- "Muhafazakâr" iddiası yanlış.
- 36 varyantın 2024–26 medyanı raporda rf'ye eşit (−0,2 puan). Düzeltilmiş engelle **≈ −2 puan** (vergi sonrası PPF) ile **≈ −6…−8 puan** (vergi öncesi PPF) arasında.
- Swing'in "2024'te 52-hafta + rejim %44,3, nakit %49,2" karşılaştırmasında gerçek 2024 PPF ≈%53 (Kuveyt Türk). Fark raporda görünenden büyük.
- **Ek hata (swing):** `common.py` repo serisi 20.05.2010'da başlıyor; daha önceki dönemde rf = 0. Bu yüzden "2007–15 nakit %4,1" yanlış; gerçek değer yılda yaklaşık %9–10. Bu, 2007–15 satırlarındaki nakit üstü farkları şişiriyor.

### 2.2 Fiyat limiti modeli hatalı (bist_test "gerçekçi dolum")

- Veride 2009 – Mart 2020 arasında yılda 500–1.100 adet ±%10,5–20 günlük hareket var; Nisan 2020'den sonra yalnız 5 tane. Yani limit Mart 2020'ye kadar **±%20** idi.
- Kod tavan/tabanı her dönem için ±%9,5 kabul ediyor. 2010–2020 arasında yanlış giriş atlamaları ve gereksiz çıkış ertelemeleri üretiyor. Yönü belirsiz bir model hatası.

### 2.3 Kurumsal işlem temizliği kusurlu

- `clean_returns` fonksiyonu, düzeltilmiş ve ham getiri aynıysa sıçramayı "gerçek" sayıyor. Oysa düzeltmesi eksik bedelsiz işlemler tam da böyle görünür.
- Piyasa değeri kontrolüyle bulunan örnekler:
  - AKFGY, 03.08.2021: −%48 kaldı; piyasa değeri aynı gün +%35.
  - NTHOL, 2010: +%62 kaldı.
  - BURVA, 2010: +%82 kaldı.
- Etkisi küçük: hataların çoğu 2009–11'de ve Nisan 2020'den sonra >%10,5'lik düzeltilmiş hareket yok. Ama %25'in altındaki eksik düzeltmeler hiç yakalanmıyor.

### 2.4 Evren

- Hayatta kalan yanlılığı raporda kabul ediliyor.
- Çekilmeyen 99 kod "küçük hisseler" diye tanımlanmış; ama aralarında krizin iki ana pump hissesi **OZATD ve TEHOL** ile XU100 üyeleri PAHOL, RGYAS, RYSAS var.
- 2025–26 sonuçları, pompalanıp çöken isimlerin bir kısmını içermediği için iki yönde de çarpık.

### 2.5 Yürütme zamanlaması

- bist_test: t+1 kapanışı. Doğru.
- bist_swing (`xs.py`, `wk.py`, `rv.py`): sinyal ve giriş aynı kapanışta.
  - Çiftlerde bu varsayım kenarı %30–45 şişiriyor (bkz. §1, satır 25).
  - H52'de etkisi yok.
  - Haftalık devam testi yeniden koşturulmadı.

### 2.6 Diğer noktalar

- **Look-ahead:** t03, t04 ve t05'te bulunmadı. Hareketli ortalamalar, 252 günlük zirve (`shift(1)`), likidite sırası ve rejim sinyalleri sinyal günü bilgisiyle kuruluyor.
- **Maliyet:** Top-150 küçük ve orta hisselerde kırılım günü için 25 bp gidiş-dönüş iyimser. 50 bp stres testi yılda yalnız ≈1,4 puan kesiyor; kayma ve tavanda dolum asıl risk.
- **TL carry:** Hesap politika faiziyle kuruldu. VİOP'un örtük faizi muhtemelen daha yüksek, bu da carry'yi düşük gösterir. Ama aylık veri gün içi şokları gizliyor (Mart 2025). Sharpe 2,24, rejim başlangıcının bilinerek seçildiği örneklem içi bir dönemden geliyor.

---

## 3. Önemli eksikler

1. **Değer faktörü hiç test edilmedi.** Hakemli BIST kanıtının işaret ettiği en güçlü faktör değer (Gökçen: yılda %14–19 prim). Üç rapor da yalnız fiyat tabanlı sinyalleri test etti.

2. **Profesyonellerin bile nakde yenildiğinin sert verisi kullanılmadı** (fonveri, hayatta kalan fonlar; bu yüzden yukarı yanlı):

   | Kategori | 3 yıl medyanı | 5 yıl medyanı |
   |---|---|---|
   | Hisse fonları | +%86 | +%838 |
   | PPF | +%259 | +%447 |
   | Kıymetli madenler | — | **+%982** (en iyi kategori) |
   | Borçlanma araçları fonları | +%181 (PPF'nin altında) | — |

   - 108 hisse fonundan 3 yılda medyan PPF'yi geçen **1** tane var (vergi sonrası kıyasta 4).
   - 169 fondan 1 yılda geçen 5 tane.
   - 5 yılda ise 75 fonun 72'si PPF'yi geçti.
   - Hüküm: rejim, hisse seçiminden daha önemli.

3. **"Risksiz" engelin kendi riski yeterince işlenmedi.** Tasfiyedeki 15 PPF'nin 1 yıllık getirileri: HYV −%95,7, PAB −%99,1, BPZ −%99,9, AC4 −%99,9. Engel ancak banka iştiraki PPF veya mevduatla gerçekten risksiz.

4. **Özel durumlar (ZPAT, ayrılma hakkı, rüçhan kuponu) atlandı.**
   - Ağustos–Ekim 2026 bültenlerinde 13 ZPAT atfı var.
   - **Karşı taraf riski:** Tera Holding, PEKGY için ZPAT yükümlülüğünü yerine getirmedi (SPK 2026/64 ve 2026/71).
   - **Doğrulanmamış örnek:** SPK 2026/59 (16.09) Heidelberg'in AKCNS için 260,25 TL veya 5,627 $ (hangisi yüksekse) ZPAT bilgi formunu onayladı. AKCNS Ekim–Kasım'da 176–190 TL'de işlem gördü. Bu açıklığın koşulu veya takvimi KAP'tan teyit edilmeden bir fırsat sayılmamalı; piyasa büyük olasılıkla iptal veya gecikme riskini fiyatlıyor.

5. **Zorunlu satıcı tezinin asıl regülasyon takvimi eksik.** Raporlar yalnız 28.08'i anlatıyor. 31.08 ve 03.09 ilke kararları atlanmış. MKK'nın günlük fiili dolaşım yayını (11.09'dan beri) artık izlenebilir bir veri kaynağı. Tez hâlâ yalnız 1 gözleme (n=1) dayanıyor.

6. **Test edilmeyenler:** VİOP bireysel kâr/zarar verisi (yayımlanmıyor olabilir), XU030 opsiyon volatilite primi, yabancı akımı (TCMB haftalık menkul kıymet istatistikleri), MSCI ve FTSE dengelemeleri, açığa satış ve VBTS tedbirleri, gerçek VİOP USDTRY vadeli serisiyle carry, kilit (lock-up) bitişleri.

7. **Kredili spot maliyeti** ≈%60 (bkz. satır 3).

## 4. Net etki

- Raporların ana çerçevesi verilerle tutarlı: ortalama birey kaybediyor, kazanç yapısal konumlarda toplanıyor, rejim hisse seçiminden önemli, mikro kenarlar küçük.
- Sayısal düzeltmelerin hepsi stratejiler **aleyhine**:
  - Gerçek TL engeli son 1 yılda vergi sonrası ≈%37,5–41, son 3 yılda ≈%46/yıl.
  - Backtestlerin 2024–26'daki "engele eşit" sonuçları aslında engelin birkaç puan altında.
  - En sağlam görünen hisse sinyali (H52) büyük ölçüde 2022'ye bağlı.
  - Çift işlemleri gerçekçi yürütmeyle %30–45 küçülüyor.
