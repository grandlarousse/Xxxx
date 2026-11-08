# sinyal_altin.py — günlük kullanım

Bu betik, hakem sentezinde (HAKEM.md, sinyal_tablosu.csv) ayakta kalan 11 altın kuralını her gün hesaplar.
- **VİOP (F_XAUUSD):** 4 kural. Hepsinin güveni DÜŞÜK.
- **Midas / ABD ETF:** 5 yönlü kural ve 2 araç seçimi kuralı. Güvenleri ORTA.

Çıktı yatırım tavsiyesi değil, kuralların mekanik hesabıdır. Hakemin birleşim rakamları üst sınırdır. Gerçekçi beklentinin yarısı şöyle:
- VİOP: Sharpe ≈ 0,7, yılda ≈ %2 (1x nominal)
- ETF: Sharpe ≈ 0,4–0,5, sepete göre alfa yılda ≈ %3

---

## 1. Kurulum

- Python 3.9 ya da üstü gerekir (`zoneinfo` için). Paketler: `pandas`, `numpy`, `requests`. Gerisi standart kütüphane (`lzma`, `struct`, `json`, `argparse`).
- Tek dosya: `sinyal_altin.py`.
- Önbellek varsayılan olarak `~/.cache/sinyal_altin/` altında tutulur, `--onbellek DİZİN` ile değiştirilebilir. İçinde Dukascopy bi5 dosyaları, Yahoo JSON, VİOP bülteni ve Hazine CSV'si bulunur.
- **İlk çalıştırma uzun sürer.** LOWMOM, 2010'dan bu yana genişleyen yüzdelik kullandığı için Dukascopy'den yaklaşık 200 aylık XAUUSD dosyası iner.
  - Dukascopy sık sık 503 döndürür. Betik bu durumda bekleyip yeniden dener ve 3 paralel bağlantı kullanır.
  - İlk kurulum 10–60 dakika sürebilir. Sonraki günlerde 10–30 istek yeterlidir.
  - İlk kurulumu işlem saatinden önce yapın: `python3 -W ignore sinyal_altin.py --canli --tarih <dünün tarihi>`.
  - Araştırma ham dosyaları elinizdeyse kurulum saniyeler sürer: `--tohum-dizini <scratchpad>/data/duka_h/XAUUSD`. Bu seçenek `YYYY_AA0.bi5` dosyalarını önbelleğe kopyalar; ay numarası 0 tabanlıdır.

## 2. Ne zaman çalıştırılır

Türkiye kalıcı olarak UTC+3'te. ABD'de yaz saati Mart'ın 2. Pazarı başlar, Kasım'ın 1. Pazarı biter. Betik ET saatini kendisi çevirir.

| Cephe | Çalıştırma (TSİ) | Karar anı | Emir |
|---|---|---|---|
| VİOP, normal gün | **17:45–18:00** | 15:00 UTC = 18:00 TSİ | **18:00–18:10 TSİ** uzlaşma penceresi |
| VİOP, TR yarım günü (arife, 28 Ekim) | 12:15–12:30 | 09:30 UTC = 12:30 TSİ | 12:30–12:40 TSİ. LOWMOM ve son saat kuralı devre dışı. Akşam seansı yok |
| Midas, **kış** (ABD standart saati; 1.11.2026 → 14.3.2027) | **22:45–23:00** | 15:00 ET = 23:00 TSİ | **15:50–15:58 ET = 23:50–23:58 TSİ** |
| Midas, **yaz** (ABD yaz saati) | **21:45–22:00** | 15:00 ET = 22:00 TSİ | 15:50–15:58 ET = 22:50–22:58 TSİ |
| Midas, ABD yarım günü (3 Temmuz Pzt–Prş, Şükran Günü ertesi Cuma, 24 Aralık Pzt–Prş) | 12:00–12:45 ET (Kasım/Aralık: 20:00–20:45 TSİ; 3 Temmuz: 19:00–19:45 TSİ) | 12:00 ET (Kasım/Aralık 20:00 TSİ; 3 Temmuz 19:00 TSİ) | 12:50–12:58 ET = Kasım/Aralık 20:50–20:58 TSİ, 3 Temmuz 19:50–19:58 TSİ (kapanış 13:00 ET). E3-1 yeni pozisyon açmaz; bir önceki günün E3-1 GDXJ pozisyonu bu pencerede satılır. 2026'da: 27 Kasım ve 24 Aralık |

Ek notlar:
- Karar anından önce çalıştırırsanız gün t'nin fiyatını kullanan sinyaller **ÖN-İZLEME** diye işaretlenir. Bunlar LOWMOM, son saat ve E3-1'dir.
  - Ön-izleme, o ana kadarki en son spot fiyatı kullanır. Dukascopy'nin saatlik tick dosyası saat bitmeden yayımlanmaz. Saatin kalan dilimi Yahoo GC=F vadeli fiyatından, Dukascopy'ye göre baz düzeltmesi yapılarak eklenir; bu değer yaklaşıktır.
  - Karar anı geçtiği hâlde Dukascopy'nin o saatlik dosyası henüz yayımlanmamışsa karar anı fiyatı yine GC=F'ten gelir. Bu durumda sinyal **YAKLAŞIK** diye işaretlenir; birkaç dakika sonra yeniden çalıştırın.
  - Değer eşiğe yakınsa (örneğin son saat sinyalinde birkaç bps) 18:00–18:02 TSİ'de, ETF'de 15:00–15:02 ET'de yeniden çalıştırın.
- Gün t işlem günü değilse betik **bir sonraki işlem gününü** hesaplar ve bunu "Not" satırında söyler. Örneğin Pazar günü çalıştırırsanız Pazartesi'nin ön-izlemesini verir.
- `--tarih YYYY-MM-DD` verilirse o günün karar anındaki veriyle hesaplanır. Geçmiş gün için canlı indirme bu yolla yapılır.

## 3. Komutlar

```bash
# Günlük (bugün; işlem günü değilse sonraki işlem günü)
python3 -W ignore sinyal_altin.py --canli
# Teminat/boyut için özsermaye (TL) ve JSON çıktısı
python3 -W ignore sinyal_altin.py --canli --ozsermaye-tl 500000 --json bugun.json
# Belirli bir günü ağdan yeniden üret
python3 -W ignore sinyal_altin.py --canli --tarih 2026-11-06
# Araştırma panellerinden geçmiş gün (doğrulama / geriye dönük kontrol)
python3 -W ignore sinyal_altin.py --panel --tarih 2026-11-06 [--panel-dizini <scratchpad>/panel] [--esik-yeniden]
# TEST: gün içi saati simüle et (karar anından 10 dk önce)
python3 -W ignore sinyal_altin.py --canli --tarih 2026-11-06 --simule-an 2026-11-06T14:50:00Z
```

Diğer seçenekler:
- `--olay-dizini`: `events_fomc/us_nfp/us_cpi.csv` dosyalarının bulunduğu dizin. Yerleşik ABD olay listesini genişletir.
- `--esik-yeniden`: E2 eşiklerini IS (2008–2017) verisinden yeniden hesaplar ve dondurulmuş değerlerle yan yana gösterir.
- `--sessiz`: stderr ilerleme satırlarını kapatır.

## 4. Çıktı nasıl okunur

Rapor beş bölümden oluşur:
- [1] VİOP
- [2] Midas/ETF
- [3] Takvim uyarıları (önümüzdeki ~10 gün)
- [4] Risk
- [5] Veri ve zaman damgası denetimi

Her sinyal için şu alanlar verilir:
- **değer** ve **eşik**
- **durum**:
  - AKTİF / PASİF / NAKİT / NÖTR
  - ÖN-İZLEME: karar anından önce, son fiyatla hesaplandı
  - BEKLİYOR: gün t verisi henüz yok
  - KOŞULLU: kural ve eşik fiyatı verilir
  - HESAPLANAMADI: veri eksik
  - DEVRE DIŞI: yarım gün; yeni dilim açılmaz, açık dilimler ve dünden kalan pozisyonun kapanışı yine "bugünkü işlem"e yazılır
  - NÖTR (spot piyasası kapalı): 25 Aralık, 1 Ocak, Kutsal Cuma gibi spotun işlem görmediği VİOP günlerinde son saat sinyalinin yeni dilimi 0'dır (hakem kuralı)
  - YAKLAŞIK: spot serisinde eksik gün var ya da karar anı fiyatı Yahoo GC=F'ten baz düzeltmeli (Dukascopy saat dosyası henüz yayımlanmadı)
  - HATA: ileriye bakma denetimi tetiklendi; sinyal üretilmez
- **yön**: UZUN, KISA ya da NAKİT. ETF'de açığa satış olmadığı için KISA hiç çıkmaz; kısa bölge NAKİT demektir.
- **tutuş**: kademeli tutuşta (h=3 ya da 5) her gün sermayenin 1/h'i ile yeni bir dilim açılır ve h gün sonra kapanır.
  - "Yeni dilim" bugün açılan dilimdir.
  - "Açık dilimler" önceki h−1 günün dilimleridir.
  - **etkin poz.** bugün uzlaşma/kapanıştan sonra taşınacak toplam pozisyondur (dilimlerin ortalaması).
  - **bugünkü işlem** = etkin(t) − etkin(t−1). Süresi dolan dilim bu farkın içinde otomatik olarak kapanır.
- **güven**: hakemin son güveni, yani min(REP, ADV). Ayrıca hakem notu ve kuralın kendisi verilir.
- **Birleşik:**
  - VİOP: 4 sinyalin eşit ağırlıklı ortalaması, tek kontratta netleşir.
  - ETF: 5 sinyalin her biri sermayenin 1/5'i, aynı ETF'te netleşir.
  - Koşullu sinyaller (son saat, E3-1) için iki **senaryo** satırı yazılır.

### Sinyaller ve kuralları

| Kimlik | Cephe | Güven | Kural (özet) | Bilgi zamanı | Tutuş |
|---|---|---|---|---|---|
| A1-LOWMOM-h1 | VİOP | DÜŞÜK | rv20'nin 2010'dan beri yüzdeliği 1/3'ün altındaysa (≈ yıllık %11,7) 5 günlük spot getirisinin işaretinde 1 birim | t 15:00 UTC spot | 1 gün (h=5 varyantı da gösterilir, bağımsız değil) |
| A3_QEND_h3 | VİOP | DÜŞÜK | Mar/Haz/Eyl/Ara'nın sondan 2. VİOP günü UZUN | takvim | 3 VİOP günü |
| A4-C1_GDXJ_artik_h3 | VİOP | DÜŞÜK | GDXJ'nin GLD'ye göre artık z'si: z > 0,43 ise UZUN, z < −0,43 ise KISA | t-1 ABD kapanışı | 3, kademeli |
| A8-3_seg_last1h_h5 | VİOP | DÜŞÜK | sign(ln spot15/spot14 UTC) | t 15:00 UTC | 5, kademeli |
| E1-C2_GDX_tatil_oncesi | ETF | ORTA | NYSE tatilinden önceki son günden bir önceki kapanışta GDX al | takvim | 1 |
| E2-C2j_GDXJ_artik_h3 | ETF | ORTA | GDXJ artığı (GLD+SPY, 250g OLS) > +%0,667 ise GDXJ | t-1 kapanış | 3, kademeli |
| E2-C2_GDX_artik_h3 | ETF | ORTA | GDX 3g artığı > +%0,806 ise GDX | t-1 kapanış | 3, kademeli |
| E2-C1_madenci_oncu_GLD_h5 | ETF | ORTA | GDX 10g artığı > +%2,515 ise GLD. Kaplama (GLD tutana): x < −%4,02 olan günün 1/5 dilimi nakit, öbür günler GLD; kaplama da 5 gün kademelidir (betik kademeli etkin GLD oranını yazar) | t-1 kapanış | 5, kademeli |
| E3-1_altin_gunici_GDXJ_donus | ETF | ORTA | spot 15:00 ET < spot 16:00 ET (t-1) ise GDXJ; ABD yarım gününde yeni pozisyon yok (dünkü pozisyon o gün kapanışta satılır) | t 15:00 ET | 1 |
| E3-3_PHYS_GLD_iskonto | ETF | ORTA | Araç seçimi: z < −1,5 ise GLD yerine PHYS | t-1 kapanış | — |
| E3-4_CEF_artik | ETF | ORTA | Araç seçimi: z < −2 ise CEF | t-1 kapanış | — |

Örtüşme uyarısı: **A4-C1 (VİOP) ile E2-C2j (ETF) aynı fenomendir** (sıra korelasyonu 0,87). İki cephede birden tam ağırlıkla kullanmayın; birini seçin ya da her birine yarım ağırlık verin. C2j, C2 ve C1 de tek ailedir.

## 5. Emir nasıl verilir

### VİOP (F_XAUUSD; 1 sözleşme = 1 ons, fiyat adımı 0,10 USD)

- **Uzlaşma fiyatı**, 18:00:00–18:10:00 TSİ arasındaki işlemlerin miktar ağırlıklı ortalamasıdır. Yarım günde pencere 12:30–12:40'tır. Akşam seansı uzlaşmaya girmez.
- Giriş ve çıkışı uzlaşmaya yaklaştırmak için emri pencereye yayın. Örneğin 18:01, 18:05 ve 18:09'da üç parça verebilirsiniz. Normal seansta **piyasa emri** kullanılabilir. **Limit** emir kullanacaksanız alışta en iyi satışın 1–2 adım üstünü, satışta en iyi alışın 1–2 adım altını yazın; dolmayan kısmı pencere içinde güncelleyin.
- Pozisyon büyüklüğü:
  - 1 birim, seçtiğiniz tam nominaldir. Hakem önerisi: nominal ≤ 2 × özsermaye. `--ozsermaye-tl` verirseniz azami sözleşme sayısı yazılır.
  - Hedef sözleşme = round(N × birleşik etkin), N = 1 birimdeki sözleşme sayısı.
  - Kademeli dilimler 1/3 ve 1/5 olduğundan N küçükse yuvarlama baskın çıkar. Bu durumda tek tek sinyalleri değil birleşik pozisyonu izleyin.
- **Vade:** Aktif kontrat, bir önceki gün açık pozisyonu en büyük olan vadedir; betik bunu bültenden okur. Açık pozisyon genelde vadeye 3–4 iş günü kala yeni vadeye geçer. Kalan VİOP günü tutuş süresinden azsa bir sonraki vadeyi kullanın; betik ≤ 7 günde uyarır.
- **Aralık vadesi:** LBMA 24 ve 31 Aralık'ta yalnız AM ihalesi yapabilir. Bu durumda F_XAUUSD1226'nın vade sonu fiyatı AM ihalesine göre belirlenebilir. 31 Aralık'ta akşam seansı yoktur.

### Midas (ABD ETF'leri; nakit hesap, açığa satış yok)

- MOC (kapanışta piyasa), LOC ve kapanış müzayedesi emirleri Midas'ta **yok**. Bu yüzden emri **15:50–15:58 ET**'de verin:
  - Piyasa emri verebilirsiniz.
  - Ya da pazarlanabilir limit verin: alışta ask'ın birkaç sent üstü, satışta bid'in birkaç sent altı.
  - Uzatılmış ve gece seanslarında yalnız limit emir geçer. Normal seans dışına kalırsanız sinyal kapanış fiyatından sapar.
- Komisyon emir başına 1,5 USD'dir; gidiş-dönüş 3 USD.
  - E3-1 yılda ~66 gidiş-dönüş üretir.
  - ~3.000 USD'nin altındaki işlemlerde komisyon ve kur makası kenarı yer.
  - TL↔USD çevirisini her işlemde yapmayın, USD bakiyede kalın.
- KISA çıkan bir sinyal NAKİT demektir. Kaldıraçlı ve ters ETF'lerin Midas'ta listelendiği **teyit edilmedi**; kullanmayın.
- **Çıkış:** h gün sonra aynı pencerede yapılır. Kademeli sinyallerde "bugünkü işlem" satırı süresi dolan dilimi zaten düşer.
- **Araç seçimi:** E3-3 "ARAÇ: PHYS" derse ve GLD alınacaksa PHYS tercih edilebilir; E3-4 "ARAÇ: CEF" derse CEF. PHYS ve CEF'in Midas'ta işlem gördüğü teyit edilmedi; uygulamada kontrol edin.
- Temettü stopajı (GDX, GDXJ) Türkiye yerleşiği için %20'dir. Fiziki altın tröstleri (GLD, IAU, GLDM) dağıtım yapmaz.

## 6. TradingView izleme kodları

Aşağıdaki kodların hepsi 2026-11-08'de TradingView sembol sayfalarında (`tradingview.com/symbols/<BORSA>-<KOD>/`) tek tek açılarak doğrulandı; sayfa başlığı kodu gösteriyor. Uydurma bir kod (ör. AMEX:ZZQQXX) aynı yolda 404 veriyor. TV kodunun var olması, aracın Midas'ta işlem gördüğü anlamına gelmez (PHYS ve CEF için bkz. §5).

| Kod | Ne | Durum |
|---|---|---|
| BIST:XAUUSD1! | VİOP ons altın, sürekli kontrat. Vadeli kodlar: BIST:XAUUSDZ2026 (Ara 2026), BIST:XAUUSDG2027 (Şub 2027) … | doğrulandı (vadeli kodlar da). TV'de "settlement as close" ayarı kapalıysa günlük kapanış 23:00 TSİ'deki son işlem olur, uzlaşma değil |
| OANDA:XAUUSD | Spot altın (OANDA) | doğrulandı. Dukascopy BID'inden birkaç sent–dolar farklı olabilir |
| TVC:GOLD | Spot altın (TradingView endeksi) | doğrulandı |
| COMEX:GC1! | COMEX altın vadeli, sürekli | doğrulandı |
| AMEX:GLD | SPDR Gold Shares (NYSE Arca; TV'de "AMEX:" öneki) | doğrulandı |
| AMEX:GDX | VanEck Gold Miners | doğrulandı |
| AMEX:GDXJ | VanEck Junior Gold Miners | doğrulandı |
| AMEX:IAU, AMEX:GLDM, AMEX:SLV, AMEX:SPY | diğer ETF'ler | doğrulandı |
| AMEX:PHYS | Sprott Physical Gold Trust | doğrulandı (Midas'ta listelendiği teyit edilmedi) |
| AMEX:CEF | Sprott Physical Gold and Silver Trust | doğrulandı (Midas'ta listelendiği teyit edilmedi) |
| BIST:USDTRY1! | VİOP dolar/TL vadeli, sürekli | doğrulandı |
| FX_IDC:USDTRY | spot dolar/TL | doğrulandı |

Eşik karşılaştırmasını aynı kaynağın iki fiyatıyla yapın. Önce grafiğin saat dilimini ayarlayın (sağ alttaki saat → "(UTC+3) Istanbul" ya da ET için "(UTC-5/-4) New York"). TV'de saatlik mumun etiketi **başlangıç** saatidir; mumun kapanışı bir saat sonraki fiyattır (Dukascopy kuralıyla aynı: bar başlangıcı + 1 saat).
- **Son saat sinyali (A8-3):** OANDA:XAUUSD 1 saatlik grafik, İstanbul saati. p14 = 16:00 mumunun kapanışı (17:00 TSİ fiyatı), p15 = 17:00 mumunun kapanışı (18:00 TSİ fiyatı). p15 > p14 ise UZUN; pratikte 17:00 mumunun rengi.
- **E3-1:** Betiğin yazdığı eşik fiyatı Dukascopy'nin önceki ABD seansı 16:00 ET fiyatıdır. TV'de aynı kaynakta, New York saatiyle, önceki seansın 15:00 mumunun kapanışını (16:00 ET) bugünkü 14:00 mumunun kapanışıyla (15:00 ET) karşılaştırın. Kışın 15:00 ET = 23:00 TSİ, yazın 22:00 TSİ.

## 7. Risk ve boyut

- Risk bölümünde şunlar yazılır:
  - rv20 (yıllık)
  - 1/3/5 günlük %95 hareket: normal varsayımla ±1,96σ√h, ayrıca son 250 günün tarihsel %2,5–%97,5 aralığı
  - tarihsel VaR99
- 2026 rejiminde F_XAUUSD için 1 günlük VaR99 ≈ %5, 5 günlük ≈ %12. 2017–2026 ortalaması bunun yaklaşık yarısıdır.
- **Teminat yaklaşımı:**
  - Takasbank PSR %10 × uzlaşma fiyatı ≈ sözleşme başına 400–410 USD. Kaynak: GM 2150, 15.06.2026'dan geçerli.
  - Aracı kurumlar %20 isteyebilir (ör. QNB).
  - Sonraki genel mektuplardaki XAUUSD PSR değeri okunamadı. **Güncel değeri Takasbank risk parametrelerinden kontrol edin.**
  - Teminat TL olduğu için USDTRY ile birlikte artar. Betik kur olarak VİOP F_USDTRY yakın vade uzlaşmasını kullanır; bu vadeli fiyattır ve taşıma maliyetini içerir.
- ±%10 VİOP fiyat limitine 2017–2026'da hiç ulaşılmadı; en büyük günlük düşüş −%7,8.
- 2σ dip alma (dönüş) kuralları zarar ediyor. 1 günlük kısa stop maliyetsiz ama getiri eklemiyor.

## 8. Veri, zaman damgası ve ileriye bakma

Her cephe için önce karar anı belirlenir:
- VİOP: t 15:00 UTC; TR yarım gününde 09:30 UTC
- ETF: t 15:00 ET; ABD yarım gününde 12:00 ET

Her gözlem kendi yayın ya da kapanış zamanıyla taşınır:

| Veri | Zaman damgası |
|---|---|
| Dukascopy saatlik mum | bar başlangıcı + 1 saat |
| Dukascopy dakika mumu | saatlik kapanışa çevrilir |
| Dukascopy tick | tick anı |
| Yahoo günlük ABD kapanışı | gün 16:00 ET (yarım günde de 16:00; muhafazakâr) |
| VİOP bülteni | gün 20:15 UTC (23:15 TSİ akşam gün sonu; muhafazakâr, yalnız t-1 bülteni kullanılır) |
| Hazine | gün 22:00 UTC |

Hesapta yalnız damgası ≤ karar anı olan gözlemler kullanılır. Her kullanım [5] numaralı bölüme yazılır. İhlal olursa o sinyal HATA olur ve üretilmez. Testte panelin ilk gününde bu kontrol gerçek bir hatayı yakaladı; hata düzeltildi.

Kurallarda uygulanan özel durumlar:
- **TR yarım günlerinde** LOWMOM ve son saat sinyali devre dışıdır (veri notu 1). Açık dilimler sürer.
- **ABD yarım günlerinde** E3-1 yeni pozisyon açmaz (veri notu 3); bir önceki günün E3-1 pozisyonu o gün kapanışta satılır ("bugünkü işlem" −1).
- **Spotun kapalı olduğu VİOP günlerinde** (25 Aralık, 1 Ocak, Kutsal Cuma) son saat sinyalinin yeni dilimi 0'dır; LOWMOM bir önceki spot gününün değerini kullanır (≤4 gün).
- Panelin bilinen hatalı sütunları kullanılmaz: `gpr_*` ve ilk satırdaki `*_prev`.

Eksik veri şöyle ele alınır:
- Ağ hatasında her istek geri çekilmeli olarak yeniden denenir (Dukascopy'de 10 kez; `SINYAL_AG_DENEME` ortam değişkeniyle değiştirilebilir). 503, zaman aşımı ve sıfırlanan bağlantı (Dukascopy'de sık) bu sınıftadır.
- Bağlantı hiç kurulamıyorsa (vekil hatası, DNS, bağlantı reddi) ve kaynak bu çalıştırmada henüz hiç yanıt vermediyse istek 3 denemede bırakılır.
- Bir kaynak art arda 3 kez hiç yanıt vermezse o çalıştırmada atlanır (devre kesici). Hiç yanıt vermeyen iki kaynak olursa ağ yok sayılır ve kalan kaynaklar beklemeden atlanır; önbellekte dosya varsa o kullanılır. Böylece ağ kesikken betik dakikalarca beklemez.
- Önbellekteki bozuk bi5 dosyası silinir ve yedek kaynağa geçilir. Saat sayısı tutmayan (ay içinde indirilmiş) aylık dosya önbelleğe alınmaz; `--tohum-dizini` de bu dosyaları atlar.
- Dukascopy günlük dosyası alınamazsa yalnız gereken saatlerin tick dosyalarına geçilir.
- O da alınamazsa gün "EKSİK" sayılır ve uyarı yazılır. LOWMOM bu durumda YAKLAŞIK diye işaretlenir; eşiğe yakınsa HESAPLANAMADI olur.
- Gerekli t-1 kapanışı yoksa ilgili sinyal HESAPLANAMADI olur.
- Henüz yayımlanmamış bir dosyanın 404'ü önbellekte kalıcı boş kayıt olarak tutulmaz.
- Yahoo alınamazsa önbellekteki eski dosya kullanılır ve uyarı yazılır. Tarih denetimi eksik günü ayrıca yakalar.

## 9. Doğrulama özeti (2026-11-08)

Testi yeniden çalıştırmak için: `python3 -W ignore test_sinyal_altin.py 2008-01-01` (~6 dk). Çıktılar `dogrulama_sinyal_betigi.csv` ve `dogrulama_sinyal_toplu.csv` dosyalarına yazılır.

**1. Panel modu, CLI üzerinden 56 geçmiş gün.** Bu günler arasında 11 TR yarım günü, 9 ABD yarım günü, çeyrek sonu ve tatil öncesi giriş günleri, LOWMOM'un aktif olduğu 4 gün, spotun olmadığı günler (25 Aralık, Kutsal Cuma) ve 2026-11-09 var.
- Toplam 2.029 değer karşılaştırıldı. Karşılaştırma kaynakları:
  - Analistin kendi kod yolu: a1_feats, a3 cal_pos, a4 miner_resid/zscale, a8 features.build, e1 c_masks, e2 s1_signals.pkl + pos_from_signal, e3 g_main_claim ve c_cef.
  - Hakem serileri: sinyal_*_ham ve poz_*.
  - Hakemin Pazartesi tablosu: bugun_2026_11_09.json.
- **11 fark** çıktı, hepsi beklenen türden:
  - (a) A4-C1, 2017-06-15 ve 2017-08-31: ısınma dönemi. Analist ve hakem serileri panelin ilk günü olan 2017-03-06'dan başlıyor; betik daha uzun ABD kapanış geçmişi kullanıyor. Pozisyon farkı yalnız 2017-06-15'te.
  - (b) A8-3, spot fiyatın olmadığı 3 VİOP günü (2024-12-25, 2025-12-25, 2026-04-03): analist a8 kodu önceki günün değerini ileri dolduruyor (ffill). Betik hakemin kuralını izliyor ve bu günlerde dilimi 0 sayıyor; hakem serisiyle aynı.
- Zaman damgası denetiminde 56 günün hiçbirinde ihlal yok.
- A4-C1 için analistin kaydettiği P&L serisi (s4_pnl_C1_GDXJ_artik.parquet), aynı pozisyonla birebir yeniden üretiliyor (maks |Δ| = 0).

**2. Toplu kontrol (modül içinden, panelin tamamı).**
- Kapsam: VİOP 2017-03-06 → 2026-11-06 (2.427 gün), ETF 2008-01-02 → 2026-11-06 (4.743 gün).
- 9 yönlü sinyalin yeni dilimi ve etkin pozisyonu her gün hakem serileriyle karşılaştırıldı:
  - 8 sinyalde fark 0.
  - A4-C1'de 106 satır farklı, hepsi 2017-03-06 → 2017-10-03 ısınma döneminde.
  - Denetim ihlali 0.
- Bu kontrol iki gerçek hatayı yakaladı; ikisi de düzeltildi:
  - Panelin ilk gününde "önceki seans" dizinde sarılıyordu. Denetim bunu İHLAL olarak işaretledi.
  - 2008–2009'da GDXJ henüz yokken GDX sinyalleri de "eksik" sayılıyordu.

**3. Takvimler.**
- NYSE seansları ve 42 yarım gün, exchange_calendars ile 2008–2027 arasında birebir aynı.
- COMEX OG vadesi, a3 events_comex.csv ile 216/216 aynı.
- VİOP takvimi panelle (2.427 gün) birebir aynı.
- E2 eşikleri IS verisinden aynen yeniden üretiliyor (`--esik-yeniden`).

**4. Canlı mod (ağ erişimiyle).**
- 2026-11-06 için ağdan indirilen veriyle bütün sinyallerin durum, dilim ve etkin pozisyonu panel moduyla aynı. Sayısal farklar ≤ 2e-8 göreli; nedeni Yahoo düzeltilmiş kapanışının yuvarlaması.
- İndirilen Dukascopy ay dosyaları (2015-03..11, 2026-07..10) ve dakika dosyaları (2–6 Kasım) araştırma ham dosyalarıyla bayt bayt aynı.
- Pazar günü (2026-11-08) çalıştırma Pazartesi ön-izlemesini verdi ve hakem tablosunu tuttu: z +2,84; x %3,674 / %9,493 / %9,653; E3-1 eşiği 4.065,68 USD; birleşik VİOP +0,033 / −0,067.
- Simülasyon sonuçları:
  - 14:50 UTC ön-izleme: p15 ≈ 4.046,97 (GC=F baz düzeltmeli); son saat UZUN.
  - 15:20 UTC: kesin değer, p15 = 4.048,545, panelle aynı.
  - ETF 19:50 UTC: m −88,2 bps.
  - ETF 20:10 UTC: m −86,8 bps, panelle aynı.
- Ağ kesintisi simülasyonu (kapalı porta yönlendirilmiş vekil; hem `https_proxy` hem `HTTPS_PROXY`):
  - Önbellek doluyken eski sürüm 5 dk 4 sn bekliyordu (her başarısız istek 7–10 deneme × geri çekilme). Hızlı bırakma eklendikten sonra 7 sn.
  - Gün içi tick dosyaları gerekirken (simüle 14:50 UTC) 9 sn; boş önbellekle (ilk kurulum) 5 sn.
  - Her durumda çökme yok: önbellekteki Yahoo dosyası kullanılıyor ve uyarı yazılıyor; veri yoksa sinyaller HESAPLANAMADI, takvim sinyalleri hesaplanıyor.

**5. Bağımsız denetim (2026-11-08, ayrı denetçi).** Betiğin kodu kullanılmadan, hakem tablosundaki kural metninden ve panel parquet'lerinden ayrı bir hesap yazıldı (`<scratchpad>/denetim_sinyal/bagimsiz_kontrol.py`).
- 53 gün karşılaştırıldı: 40 rastgele gün (VİOP 2018+, ETF 2009-06+) ve 13 uç gün (TR/ABD yarım günleri, QEND ve tatil öncesi girişleri, spotun kapalı olduğu günler, 2026-11-06). Toplam 2.225 değer.
- E2 eşikleri IS (≤2017) kantillerinden yeniden üretildi ve dondurulmuş değerlerle aynı çıktı.
- Bulunan ve düzeltilen hata: ABD yarım gününde E3-1 "DEVRE DIŞI" iken bir önceki günün pozisyonu yok sayılıyordu (etkin_önceki 0, işlem 0). Örneğin 2024-12-24'te dünkü GDXJ satışı (−1) ve birleşik ETF "önceki" ağırlığı eksik yazılıyordu. Yazar testine (`test_sinyal_altin.py`, toplu kontrol) etkin_önceki ve kademeli kaplama karşılaştırması eklendi. 2008–2026 panelinde fark yalnız panel başı ısınma döneminde kaldı (A4-C1 2017-03-06 → 2017-10-04, LOWMOM 2017-03-06 önceki gün); geri kalan her gün fark 0.
- Spotun kapalı olduğu VİOP günlerinde (2024-12-25, 2026-04-03) son saat sinyalinin yeni dilimi eskiden "—" yazılıyor ve durum HESAPLANAMADI çıkıyordu; etkin pozisyon aynıydı. Artık hakem kuralıyla 0 yazılıyor, durum "NÖTR (spot piyasası kapalı)". Düzeltmelerden sonra 2.225 değerin hepsi aynı (fark 0).
- Canlı mod: 2026-11-06 (ağdan) panelle aynı. Pazartesi 2026-11-09 ön-izlemesi panelden bağımsız hesapla aynı: z +2,8413; x %3,674 / %9,493 / %9,653; E3-1 eşiği 4.065,685.

## 10. Bilinen sınırlamalar ve bakım

- **Gün içi kaynak:** Dukascopy saatlik tick dosyası saat bitmeden yayımlanmaz. Karar anından önceki son dilim Yahoo GC=F'ten baz düzeltmeli yaklaşık değerdir. Yahoo vadeli verisi ~10 dk gecikmeli olabilir; betik gözlem saatini yazar.
- **Dukascopy 503:** ilk kurulum uzun sürebilir. Gün dosyası hiç alınamazsa o gün eksik kalır ve uyarı yazılır.
- **Yerleşik takvimler:**
  - TR tatil ve yarım günleri 2027 sonuna kadar tanımlı. 2027 bayram tarihlerini Diyanet takviminden kontrol edin.
  - NYSE kuralları kalıcıdır, ancak plansız kapanışları bilemez.
  - FOMC listesi 2027 sonuna kadar uzanıyor.
  - NFP listesi 2026-12-04'te, CPI listesi 2026-10-14'te bitiyor. Kasım ve Aralık 2026 CPI tarihleri (10 Kasım, 10 Aralık) tahminidir; BLS takviminden **kontrol edin**.
- **Dondurulmuş parametreler:** E2 eşikleri ve LOWMOM 1/3 eşiği IS döneminde donduruldu. Yeniden kalibre etmeyin, çünkü sinyaller zaten binlerce testten seçildi.
- **2026 rejimi:** LOWMOM yapısal olarak pasif (rv20 ≈ %21, eşik ≈ %11,7). C2 ve C1 yüksek oynaklıkta zayıflıyor; C2j'nin 2026 Sharpe'ı 0,21.
- **Kademeli dilimlerin geçmişi:** Betik geçmiş dilimleri kuralın kendisinden yeniden hesaplar; sizin gerçekte açtığınız pozisyonları bilmez. Bir günü kaçırdıysanız gerçek pozisyonunuzu "etkin poz." ile karşılaştırarak düzeltin.
