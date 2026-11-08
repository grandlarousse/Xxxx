# Aile: sektör ve tematik ETF'ler (75 ETF), 1-3 işlem günlük alım-satım

Hazırlanma: 7 Kasım 2026. Veri: 2016-11-07 ile 2026-11-06 arası (IS: 2021 sonuna kadar, OOS: 2022 ve sonrası). Kullanıcı: Midas üzerinden akşamları (TR saati) işlem yapan bireysel yatırımcı.
Kod: `kod/ajan_sektor_tematik/`. Tablolar: `sonuclar/aile_sektor_tematik/`. JSON: `sonuclar/aile_sektor_tematik/sonuc.json`.

## 0. Kısa sonuç

- **Kabul eşiğini geçen tek bağımsız bulgu yarı iletkenlerde.** S1: NASDAQ:SMH'de IBS < 0,20 olan gün SMH'yi kapanışta al, ertesi gün kapanışta sat. 2.500 $ pozisyonla n=492 işlem, net +41,8 bp, t 3,69. IS +43 bp, OOS +40 bp. 11 yılın 10'u pozitif. O1'de (ertesi gün açılışta giriş) brüt kenar +27 bp. Hem bu ajanın 1.302 testinde hem genel kütüphanenin 21.978 aile satırında BH-FDR'yi geçiyor.
- **S2, aynı sinyalin SOXL (3x) ile uygulanması.** Net +146 bp, t 4,23, maxDD −%54. Bağımsız kanıt değildir. SOXL'ün Midas'ta bulunurluğu doğrulanamadı. Risk eşdeğeri tutarla (SMH tutarının 1/3'ü) işlem başına kazandırdığı dolar, SMH ile neredeyse aynı.
- **S1 sektöre özgü değil, Nasdaq IBS etkisinin yüksek betalı hâli.** Sinyallerin %70'i QQQ IBS < 0,20 ile aynı güne düşüyor. abd_endeks ailesindeki QQQ/TQQQ IBS kuralıyla aynı bahis sayılmalı. Aynı kural diğer 35 küme temsilcisinde sıfır ya da negatif.
- **Reddedilenler.**
  - "Aşırı satılan sektörü al": sektörün SPY'a göre beta60 kalıntısı z < −2 olduğunda sektör ertesi gün de geride kalıyor (SPY hedge'li −14 bp, t −2,2). Yani dönüş değil, devam var.
  - ST02 (kesitsel 1 günlük dönüş), ST03 (5 günlük momentum), ST01, ST04, ST06.
  - Sekiz sektör içi çift.
  - Yarı iletken dışındaki kaldıraçlı araç uygulamaları.
- **"MR_ibs_lt01_dusus C1 h3 sektörlerin 33/34'ünde pozitif" bulgusu tek bir piyasa etkisi.** Etkin bağımsız seri sayısı yaklaşık 2,6. Küme-sağlam t 1,8-2,7. SPY'a göre hedge'li kenar yaklaşık 0.
- **Lead-lag.**
  - Gerçek gecikmeli öncüler yalnızca negatif yönlü: QQQ/SPY → IGV ve EEM → KWEB. Long-only bir yatırımcı için ancak "alma/çık" filtresi işlevi görüyorlar.
  - Yarı iletkenlerde NVDA, TSM, AVGO, EWT ve EWY öncü değil. SMH'nin kendi gecikmesi kontrol edildiğinde katkıları sıfır.
- **Takvim riski.** FOMC karar günü faize duyarlı sektörlerde (KRE, XLF, ITB, VNQ, XLU, KIE) gün içi brüt −26 bp. Bu etki hem IS'te hem OOS'ta negatif.
- **Ailede PTP/K-1 ürünü yok.** Tümü 1940 Kanunu fonu; FNGU/FNGD ise ETN.

## 1. Yöntem

### 1.1 Zamanlama ve maliyet

Zamanlama `kod/lib.py`'deki sözleşmeye uyar:
- Sinyal, t kapanışına kadarki bilgiyle hesaplanır.
- C0: t kapanışında giriş. O1: t+1 açılışında giriş. C1: t+1 kapanışında giriş.
- Çıkış, girişten h işlem günü sonraki kapanıştır.
- İşlemler çakışmaz: pozisyondayken gelen sinyal yok sayılır.

Maliyet, `cost_bp` = 2 × 1,5 $ / pozisyon + kademeli makas tahmini. Varsayılan pozisyon 2.500 $ (SMH için 13 bp). Duyarlılık için 1.000 $ ve 10.000 $ da hesaplandı.

### 1.2 Kopya kümeleri

`ortak.py` → `CLUSTERS` 37 küme tanımlar. Ölçüt: 2023 sonrası günlük getiri korelasyonu yaklaşık 0,93'ün üstündeyse ya da dayanak aynıysa aynı küme. Kaldıraçlı ve ters ürünler dayanaklarının kümesine konur. Her kümenin temsilcisi, en likit kaldıraçsız ETF'idir. Örnekler:

| Küme | ETF'ler | Korelasyon |
|---|---|---|
| Yarı iletken | SMH, SOXX, SOXL, SOXS | 0,98 |
| Bölgesel banka | KRE, KBE | 0,993 |
| Gayrimenkul | VNQ, XLRE, IYR | 0,98-0,99 |
| Konut | ITB, XHB, NAIL | 0,97 |
| Siber güvenlik | CIBR, HACK | 0,97 |
| Uranyum/nükleer | URA, URNM, NLR | 0,95 |
| ARK inovasyon | ARKK, ARKW | 0,95 |
| Robotik | BOTZ, ROBO, DRIV | 0,93 |

Kaldıraçlı ürünlerin dayanağıyla korelasyonu 0,99-0,998.

### 1.3 Havuzlanmış aile testi

Bütün küme temsilcilerinin işlemleri birleştirilir. Ortalama işlem düzeyindedir. t istatistiği küme-sağlam (CR1) standart hatayla hesaplanır; küme olarak **sinyal haftası** (ayrıca muhafazakâr kontrol olarak sinyal ayı) kullanılır. Böylece aynı haftada birçok sektörde birden tetiklenen sinyal tek gözlem gibi sayılır.

Sektöre özgü kenarı ayırmak için her işlemde SPY beta-hedge'li getiri ayrıca raporlanır (yalnız teşhis amaçlı; Midas'ta açığa satış yok).

### 1.4 Parametreler

Tarama yapılmadı. Eşikler literatürdeki standart değerlerdir: IBS 0,20, z = ±2, beta ve standart sapma penceresi 60 gün, h ∈ {1, 2, 3}. S1 için komşu eşikler yalnızca raporlandı; seçimde kullanılmadı.

### 1.5 Test sayısı

Bu ajanın kendi testleri toplam **1.302**. BH-FDR (q=0,10) sonrası 92 test geçti; bunların yalnızca 22'si pozitif etkili. Dökümü (`fdr_tum_testler.csv`):

| Kaynak | Test sayısı |
|---|---|
| Genel kütüphane havuzu | 297 |
| Hipotezler | 630 |
| Ek lead-lag regresyonu | 102 |
| Lead-lag kuralları | 225 |
| FOMC | 6 |
| XME→COPX | 24 |
| S1 satırları | 18 |

Pozitif etkili 22 testin 21'i yarı iletken/teknoloji IBS kümesinde (SMH/SOXX → SMH/SOXX/SOXL, XLK → TECL); biri XBI IBS → LABU C0 h2 (IS t 1,2, kararsız). Negatif etkili geçenler, maliyetin brüt getiriden büyük olduğu satırlar.

Ayrıca genel_tum'un 21.978 aile satırı ayrıca incelendi; aile içi BH-FDR sonrası 995 satır geçti, bunların %96'sı negatif.

## 2. İşlenebilirlik (tarama.csv) ve izleme listesi

| ETF | Karar | Medyan $ hacim (mn) | Gidiş-dönüş maliyet (bp, 2.500$) | 1g oynaklık (bp) | Maliyet/oynaklık | TradingView | Not |
|---|---|---|---|---|---|---|---|
| SMH | **kabul** | 3.985 | 13,0 | 267 | 0,049 | NASDAQ:SMH | S1 |
| SOXL | **kabul** | 6.540 | 14,2 | 916 | 0,015 | AMEX:SOXL | S2 aracı; Midas'ta doğrulanamadı; 3x |
| SOXX | yedek | 3.333 | 13,0 | 309 | 0,042 | NASDAQ:SOXX | SMH kopyası |
| XLK | yedek | 1.896 | 13,0 | 178 | 0,073 | AMEX:XLK | IBS zayıf (OOS 5 bp) |
| IGV | yedek | 1.173 | 13,0 | 207 | 0,063 | CBOE:IGV | QQQ'dan negatif gecikme (filtre) |
| XBI | yedek | 1.237 | 13,0 | 189 | 0,069 | AMEX:XBI | IBS sınırda (t 1,8) |
| KRE | yedek | 1.022 | 13,4 | 130 | 0,103 | AMEX:KRE | sürücüler faiz/XLF; FOMC günü riski |
| XOP | yedek | 532 | 14,0 | 189 | 0,074 | AMEX:XOP | ham petrol sürücüsü |
| KWEB | yedek | 594 | 16,0 | 170 | 0,094 | AMEX:KWEB | EEM'den negatif gecikme (filtre) |
| COPX | yedek | 239 | 14,0 | 302 | 0,046 | AMEX:COPX | bakır sürücüsü |

Kalan 65 ETF **red** (gerekçeleri ETF bazında JSON'da). Ana nedenler:

- **Düşük 1 günlük oynaklık.** Maliyet/oynaklık oranı ≥ 0,11, kenar yok: XLF, XLV, XLI, XLY, XLP, XLU, XLB, XLC, VNQ, KIE, IYT, MOO.
- **Kopya.** KBE, IYR, XLRE, XHB, HACK, URNM, NLR, ARKW, ROBO, XAR, PAVE, SKYY, WCLD, ICLN, IBB.
- **Düşük likidite.** DRIV 1,3 mn $; RETL, UTSL, CURE, DFEN, LIT, BLOK, ARKW, HACK, ROBO < 20 mn $.
- **Ters ürünler.** SOXS, TECS, FAZ, LABD, ERY, DRIP, FNGD: kısa yön için doğrulanmış sinyal yok ve sürekli değer kaybediyorlar (SOXS 1 yılda −%90).
- **Kaldıraçlı ürünler.** TECL, FAS, LABU, ERX, GUSH, NAIL, DFEN, CURE, RETL, UTSL: dayanak sinyali bu araçlarda IS ve OOS'ta birlikte tutarlı değil.
- **FNGU.** 2025-02'de ETN olarak yeniden ihraç edildi, kısa geçmiş.
- **Tematikler.** ARKK, ARKG, TAN, ICLN, URA, LIT, REMX, BOTZ, QTUM, UFO, BLOK: ST06 dahil hiçbir kuralda kenar yok. URA, COPX ve XME metal_madenci; BLOK kripto; XOP, OIH ve ERX enerji_tarim ailesiyle ortak.

## 3. Genel kütüphanenin aile içi incelemesi (genel_tum.csv)

### 3.1 Tek ETF düzeyi

Kabul ölçütlerinin hepsini (net > 0, t ≥ 2, IS > 0, OOS > 0, yılların ≥ %60'ı pozitif, n ≥ 40) aynı anda sağlayan 286 satır var; 29 kümeye dağılıyorlar. Ancak 97'si yarı iletken, 60'ı teknoloji kümesinde. Diğerleri dağınık ve FDR'yi geçmiyor; 22 bin testte beklenen gürültü düzeyinde.

### 3.2 Aile havuzu (`a2_havuz_genel.py`, `havuz_genel.csv`)

37 küme temsilcisi üzerinden küme-sağlam t ile bakıldığında, **hiçbir pozitif sinyal BH-FDR'yi geçmiyor**. En yüksek havuz t değerleri:

| Sinyal | Mod / h | Net (bp) | t (hafta kümesi) | t (ay kümesi) | SPY hedge'li (bp) |
|---|---|---|---|---|---|
| MR_ibs_lt01_dusus | C1, h3 | 25,0 | 1,82 | 1,97 | −1,1 |
| CA_ay_sonu | C0, h2 | 24,7 | 1,36 | — | 10,6 |
| MR_ibs_lt02 | C0, h3 | 12,5 | 1,17 | — | −1,5 |

### 3.3 "33/34 sektörde pozitif" bulgusu (`a6_bagimsizlik.py`)

- 34 sektör ETF'inin getiri korelasyon matrisinden **etkin N = 2,6**.
- Sektör sinyallerinin %45'i SPY'ın aynı sinyaliyle aynı güne düşüyor.
- Havuz t: naif 8,5 → hafta kümeli 2,72 → ay kümeli 3,10.
- SPY hedge'li kenar +4 bp (t 0,86).
- Aynı sinyal SPY'da 55,7 bp, t 2,79.

Sonuç: bu, piyasa genelindeki "kapanış dibinde düşüş günü" etkisi. Sektör ETF'leri yalnızca oynaklığı büyüterek taşıyor; sektöre özgü bilgi yok. abd_endeks ailesine aittir.

## 4. Aileye özgü hipotezler (`a3_hipotezler.py`, `tests_hipotez.csv`)

| Hipotez | Birincil kural | Sonuç |
|---|---|---|
| ST01 sektör IBS | IBS < 0,2 & C > SMA200, C0 h1, 14 ETF | Net −2,9 bp (t_küme −0,74); O1 −11 bp. **Red.** |
| SPY'a göre kalıntı dönüşü | beta60 kalıntı z1 < −2 → al, 37 küme | C0 h1 net −28 bp (t −2,2), hedge'li −14 bp (t −2,2): **devam** var, dönüş yok. 11 SPDR'de −14 bp. Kontrol z1 > +2: +1,5 bp (h3 +23, t 1,7). **Red.** |
| ST02 kesitsel 1g dönüş | En kötü 2 SPDR (r−r_SPY), C0 h3 | Net −5,9 bp (t −0,9); brüt 7,8 < koşulsuz 12,9. **Red.** |
| ST03 5g momentum | En iyi 3 SPDR, C0 h3 | Net +1,3 bp (t 0,2) ≈ en kötü 3 kontrolü (0,7). **Red.** |
| ST04 büyük→küçük | r_büyük − r_küçük ≥ 1,5 puan → küçük, C0 h1 | IBB→XBI +10,7 (t 0,4); XLE→XOP −68; XLF→KRE −33; SPY→RSP n=9. XSD verisi yok. **Red.** |
| ST05 kaldıraç kaybı | Ölçüm | Log sapma teoriyi izliyor (SOXL h3, σ20 ≥ %3: −168 bp gözlenen / −159 bp teorik). Basit fark SOXL h1 −9 bp, h3 −31 bp; σ20 ≥ %3 iken h3 −75 bp. **Kural: σ20 ≥ %3 iken 3x ürünü en fazla 1 gün tut.** |
| ST06 tematik sert düşüş | r ≤ −2σ20 & C > SMA50, C0 h2, 8 ETF | Net −18,9 bp (t −0,6); IS −48 / OOS +28. **Red.** |
| Sektör içi çiftler | 8 çift, z1 ve z5, ±2, h 1-3, 3 mod (324 test) | Havuz z1 < −2 → geride kalanı al, C0 h1: −32 bp. Pozitif FDR geçen yok. **Red.** |
| Kaldıraçlı araç | 7 dayanak × 3 sinyal × 9 (189 test) | Yalnız SMH/SOXX → SOXL IS ve OOS'ta birlikte güçlü (S2). TECL'de OOS t 0,8; LABU'da IS t 0,8-1,2. |
| FOMC (`a5`) | Faize duyarlı 6 ETF | Karar günü O1 brüt −26 bp, net −41 bp (t −3,0; IS −32 / OOS −48; hedge'li −17 bp, t −2,3). **Takvim riski olarak raporlandı.** |

## 5. Aday stratejiler

Tekrar üretilebilir betik:

```
python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_sektor_tematik/strateji_adaylari.py
```

Betik tüm sayıları basar ve işlem listelerini `aday_*` CSV'lerine yazar. Çıktının kopyası: `sonuclar/aile_sektor_tematik/strateji_adaylari_cikti.txt`.

### S1: sektor_tematik_S1, SMH IBS < 0,20 → SMH, 1 gün (güven: orta)

**Kural.** TradingView'da NASDAQ:SMH günlük grafiğinde IBS = (close − low) / (high − low) hesaplanır (Pine: `(close-low)/(high-low)`). IBS < 0,20 ise SMH long alınır ve ertesi işlem günü kapanışında satılır. Filtre yok. Ertesi gün yine IBS < 0,20 olursa satılmaz, bir gün daha tutulur; bu, backtest'teki sat + yeniden al'dan 3 $ ucuzdur.

**Giriş saati.** Kış saatinde (1 Kas 2026 - 14 Mar 2027) TR 23:45-23:58, yaz saatinde TR 22:45-22:58. IBS anlık fiyatla hesaplanır. Midas'ta MOC/LOC yok; piyasa emri ya da son fiyatın biraz üstüne limit emir kullanılır. Giriş kaçırılırsa ertesi açılışta alınabilir (kış TR 17:30 / yaz TR 16:30); bu durumda beklenen net yaklaşık 15 bp'ye düşer.

**Temel istatistikler (2.500 $ pozisyon).**

| Ölçü | Değer |
|---|---|
| İşlem sayısı | 492 |
| Brüt / net ortalama | 54,8 / 41,8 bp |
| Medyan net | 40,9 bp |
| Kazanma oranı | %58,7 |
| PF | 1,60 |
| t | 3,69 |
| IS (256 işlem) | 43,3 bp, t 3,13 |
| OOS (236 işlem) | 40,1 bp, t 2,20 |
| Pozitif yıl | 10/11 (2016'da 6 işlem, negatif; 2022 +2 bp) |
| maxDD (işlem başına tam sermaye) | −%21 |
| En kötü işlem | −%10,7 (2020-03-11) |
| Diğer kötü işlemler | 2025-01-24 DeepSeek −%10,0; 2025-04-03 gümrük tarifesi −%7,7 |
| Sıklık | Yılda ~49 işlem; zamanın ~%20'si piyasada |

**Maliyet duyarlılığı (net, işlem başına).**

| Pozisyon | Net | t |
|---|---|---|
| 1.000 $ | 23,8 bp | 2,10 |
| 2.500 $ | 41,8 bp | 3,69 |
| 10.000 $ | 50,8 bp | 4,48 |

**Giriş modu ve tutuş sağlamlığı.**

| Mod / h | Net (bp) | t | Not |
|---|---|---|---|
| C0 h1 | 41,8 | 3,69 | birincil |
| C0 h2 | 51,7 | 3,4 | |
| C0 h3 | 66,0 | 3,3 | |
| O1 h1 | 15,5 | 1,83 | brüt 28,5, kenar +27 |
| O1 h2 | 30,3 | 2,2 | |
| O1 h3 | 42,0 | 2,3 | |
| C1 h1 | 2,3 | — | kenar yaklaşık 0 |
| C1 h3 | 46,6 | 2,15 | |

Etki ilk gün içinde sönüyor; O1'de brüt kenar pozitif olduğundan "yalnız kapanışa bağımlı" değil.

**Komşu eşikler (seçim yapılmadı).**

| IBS eşiği | Net (bp) | t |
|---|---|---|
| 0,10 | 55 | 3,7 |
| 0,15 | 39 | 3,2 |
| 0,25 | 40 | 4,1 |
| 0,30 | 29 | 3,2 |

**Aile içinde aynı kural** (her ETF kendi IBS'iyle, 39 ETF):

| ETF | Net (bp) | t | Not |
|---|---|---|---|
| SOXX | 43,3 | 3,9 | kopya |
| XLK | 19,0 | 2,2 | OOS 5 bp |
| QQQ | 17,6 | 2,1 | |
| XBI | 15,9 | 1,8 | |

Kalan 35 ETF'te sonuç yaklaşık 0 ya da negatif; pozitif oran %31.

**QQQ ile ayrıştırma (SMH'de işlem, C0 h1).**

| Durum | Net (bp) | t |
|---|---|---|
| SMH ve QQQ IBS'i birlikte < 0,2 | 53,8 | 3,8 |
| SMH < 0,2, QQQ değil | 14,4 | 0,8 |

QQQ beta-hedge'li kenar +18 bp (t 4,0). Yorum: yarı iletkenler Nasdaq'ın gün sonu dönüşünü yaklaşık 1,8 beta ile büyütüyor. Bağımsız kanıt sayısı 1 küme.

**Neden güven "orta".**
- Tek bir bağımsız küme var.
- Aday çok sayıda test içinden geldi (FDR'yi yine de geçiyor).
- C0 girişte IBS, kapanıştan yaklaşık 15 dakika önce tahmin ediliyor; eşiğe yakın günlerde yanlış sınıflama olabilir.
- Sert düşüş günlerinde de tetikleniyor.

### S2: sektor_tematik_S2, SMH IBS < 0,20 → SOXL, 1 gün (güven: orta; risk yüksek)

**Kural.** Sinyal S1 ile aynı ve SMH'den hesaplanır (SOXX IBS de kullanılabilir: 139 bp, t 4,3). İşlem AMEX:SOXL'de yapılır, tutuş 1 gün.

**Temel istatistikler.**

| Ölçü | Değer |
|---|---|
| İşlem sayısı | 492 |
| Brüt / net | 160 / 145,8 bp |
| t | 4,23 |
| IS / OOS | 144 / 148 bp |
| PF | 1,71 |
| Kazanma oranı | %60,8 |
| maxDD | −%54 |
| En kötü işlem | −%30,6 (2020-03-11) |
| O1 h1 | net 72 bp (t 2,7) |
| C1 h1 | kenar yaklaşık 0 |

**Risk eşdeğeri karşılaştırma.** SOXL'ü SMH tutarının 1/3'üyle (833 $) almak, 2.500 $'lık SMH ile işlem başına aşağı yukarı aynı dolar kârı verir: SOXL'de yaklaşık 10,1 $, SMH'de yaklaşık 10,4 $. Bunun nedeni, sabit 3 $ komisyonun küçük tutarda daha ağır basması. SOXL'ün tek avantajı sermaye verimliliği.

**Midas notu.** SOXL'ün bulunurluğu "doğrulanamadı" (`notlar/midas_kosullari.md`). İşlemden önce uygulamada Keşfet > Pay ara ile kontrol edilmeli. PTP değildir.

## 6. Lead-lag (kabul ve yedek ETF'ler)

Kaynaklar: `leadlag_sweep.csv`, ek testler `a4_leadlag.py` → `leadlag_ek.csv`, `leadlag_kural.csv`, `suruculer.csv`.

Önemli: süpürmedeki "yetişme" bayrakları (SMH 18, SOXX 14, SOXL 5) −r_T(t) terimi nedeniyle SMH'nin kendi dönüşünü yakalıyor. Bu öncülerin kendi gecikmesi kontrollü lag_t değerleri |t| < 1,7; öncü katkısı yok. İşlem kuralına çevrilmiş yetişme testi de anlamsız (SMH, QQQ'ya göre geride → SMH al: h1 18 bp, t 0,5).

### Eşzamanlı sürücüler

Bunlar öncü değildir; aynı gün birlikte hareket ederler. Değerler son 1 yılın korelasyonu (beta).

| ETF | Sürücüler |
|---|---|
| SMH | XLK 0,94 (1,40); QQQ 0,91 (1,82); TSM 0,86; EEM 0,85; NVDA 0,73 |
| SOXL | XLK 0,92 (4,86); QQQ 0,89 (6,29) |
| SOXX | XLK 0,91; QQQ 0,89 |
| XLK | QQQ 0,96; SMH 0,94; SPY 0,85 |
| IGV | MSFT 0,66; XLK 0,51; SPY 0,51 |
| XBI | IWM 0,63; SPY 0,52; VIX −0,51 |
| KRE | XLF 0,69; IWM 0,60; VIX −0,38 |
| XOP | XLE 0,92; BNO 0,71; USO 0,69 |
| KWEB | FXI 0,88; EEM 0,45 |
| COPX | CPER 0,82; EEM 0,75; GLD 0,71 |

### Gerçek gecikmeli öncüler

Ölçüt: kendi gecikmesi kontrollü, FDR'yi geçen, IS ve OOS'ta aynı işaretli ilişki.

**IGV ← QQQ ve SPY (negatif).**
- Regresyon: t −3,68; IS −2,29; OOS −2,40; 1 standart sapmalık QQQ hareketi başına −32 bp.
- Kural: QQQ'nun 1 günlük z-skoru > +1 ise ertesi gün IGV brüt −6,7 bp (C0) ve −11,3 bp (O1).
- Long-only'de maliyeti karşılamıyor (QQQ z < −1 → IGV al: net −2,6 bp). Yalnızca filtre: "QQQ güçlü yükseldiği akşam IGV alma".

**KWEB ← EEM (negatif).**
- Regresyon: t −3,84; IS −2,86; OOS −2,71; −37 bp/sd.
- Kural: EEM'in 1 günlük z-skoru > +1 ise ertesi gün KWEB brüt −34 bp (C0), −14 bp (O1), −25 bp (C1). Net IS −37 bp, OOS −62 bp; FDR'yi geçiyor.
- Long-only'de "alma/çık" kuralı. FXI de aynı yönde (−47 bp/sd, OOS t −1,7).

**Diğerleri: doğrulanmış gecikmeli öncü yok.**
- SMH, SOXX ve SOXL için QQQ/SPY negatif ilişkisi IS'te var (t −2,5) ama OOS'ta t −1,0.
- NVDA, TSM, AVGO, EWT, EWY kendi gecikmesi kontrol edilince t 0,2-0,7.
- XLK: AAPL h3 tek ufukta ve mekanizmasız; kullanılmadı.
- XBI: SPY/QQQ ilişkisi OOS'ta zayıf (t −1,2).
- KRE, XOP: yok.
- COPX ← XME: regresyonda t 2,47 ama işlem kuralında net 4,6 bp (t 0,36); yok.

### Gerçek zamanlı izleme araçları

Bunlar öncü değildir. ETF kapalıyken işleyen piyasalar olarak açılış boşluğunu önceden gösterirler.

| ETF | Araçlar |
|---|---|
| SMH, SOXL, SOXX | CME_MINI:NQ1!; KRX:KOSPI (TR yaklaşık 03:00-09:30); OSE:NK2251!; NASDAQ:NVDA uzatılmış seans (bilanço kapanış sonrası); NYSE:TSM pre-market (TR 12:00-17:30). NASDAQ:SOX yalnız ABD seansında hesaplanır. |
| XLK | NQ1!, ES1!, NVDA |
| IGV | NQ1!, NASDAQ:MSFT |
| XBI | CME_MINI:RTY1!, CBOE:VIX |
| KRE | RTY1!, CBOT:ZN1!, TVC:US02Y |
| XOP | NYMEX:CL1!, ICEEUR:BRN1! |
| KWEB | HKEX:HSI1! (KWEB varlıklarının çoğu Hong Kong'da işlem görüyor), TVC:HSI, FX:USDCNH, SGX:CN1! |
| COPX | COMEX:HG1!, FX:USDCNH |

**Doğrulanacak TradingView kodları:** TWSE:2330 (TSMC), KRX:000660 (SK Hynix). Tayvan endeksi için kontrol edilen TWSE:TAIEX kodu "yönlendirildi" çıktı; doğru kod (ör. TVC:TWII) doğrulanmalı. Bunlar doğrulanmış gibi kullanılmamalı.

### Takvim riskleri

| ETF | Riskler |
|---|---|
| SMH, SOXL, SOXX | NVDA bilançosu (ABD kapanışı sonrası; tarih şirketten doğrulanmalı), TSMC aylık satışları, FOMC, CPI |
| KRE | FOMC karar günü (yeni long açma), banka bilançoları, Fed stres testi |
| XOP | EIA haftalık petrol stokları (Çarşamba 10:30 ET: kış TR 18:30 / yaz TR 17:30), OPEC+ toplantıları, CL vade sonu |
| KWEB | Hong Kong tatilleri (ETF işlem görür, dayanak kapalı: bayat NAV), Çin PMI, Ekim Altın Haftası |
| IGV | MSFT, ORCL, CRM bilançoları |

## 7. Sınırlamalar

- **C0 girişi hafif iyimser.** IBS kapanış fiyatıyla hesaplandı; gerçekte kapanıştan yaklaşık 15 dakika önceki fiyatla tahmin edilir. O1 sonuçları gerçekçi alt sınırdır (S1 için net 15 bp).
- **Makas tahminleri kabadır.** Likidite kademesine dayanıyorlar. Kayma (slippage) ve TL↔USD kur makası maliyete dahil değil.
- **Hisse verisi temettüsüz.** NVDA, TSM, AVGO, MSFT, AAPL, TSLA ve COIN ham kapanıştan kullanıldı; günlük öncü testlerinde etkisi ihmal edilebilir.
- **XSD verisi yok.** ST04'ün SMH→XSD ayağı test edilemedi.
- **Kaldıraçlı ürünlerin geçmişi gerçek fon fiyatlarıdır** (Mart 2020 çöküşü dahil); geleceğin daha düşük ya da daha yüksek oynaklıkta geçmesi S2'nin riskini değiştirir.
- **Bağımsızlık.** S1, abd_endeks ailesinin Nasdaq IBS sonucuyla aynı bahistir; portföyde birlikte kullanılırsa çeşitlendirme sağlamaz.
- **Midas'ta bulunurluk.** SOXL ve SOXS doğrulanamadı. Ailede PTP ürünü yok; 1446(f) %10 kesinti riski bu ailede geçerli değil. FNGU/FNGD ise ETN olduğundan ihraççı kredi riski taşır.
- **Yayın sonrası zayıflama.** IBS dönüşü yaygın bilinen bir etki; literatürdeki taban orana göre beklenen büyüklük, geçmiş performansın yarısı kadar olabilir.

## 8. Dosyalar

| Dosya | İçerik |
|---|---|
| `kod/ajan_sektor_tematik/ortak.py` | kümeler, maliyet, küme-sağlam t |
| `kod/ajan_sektor_tematik/havuz.py` | havuz değerlendirme, SPY hedge |
| `kod/ajan_sektor_tematik/a1_genel_ozet.py` | genel_tum aile özeti → `genel_aile_ozet.csv` |
| `kod/ajan_sektor_tematik/a2_havuz_genel.py` | 297 havuz testi → `havuz_genel.csv` |
| `kod/ajan_sektor_tematik/a3_hipotezler.py` | ST01-ST06, kalıntı, çiftler, kaldıraçlı → `tests_hipotez.csv`, `st05_kaldirac_kaybi.csv` |
| `kod/ajan_sektor_tematik/a4_leadlag.py` | → `leadlag_ek.csv`, `leadlag_kural.csv`, `suruculer.csv` |
| `kod/ajan_sektor_tematik/a5_fomc_fdr.py` | → `fomc_sektor.csv`, `fdr_tum_testler.csv` |
| `kod/ajan_sektor_tematik/a6_bagimsizlik.py` | → `bagimsizlik.csv` |
| `kod/ajan_sektor_tematik/a7_xme_copx.py` | → `xme_copx_kural.csv` |
| `kod/ajan_sektor_tematik/strateji_adaylari.py` | S1/S2 tekrar üretim betiği → `aday_sektor_tematik_S1_*.csv`, `aday_sektor_tematik_S2_*.csv` |
| `kod/ajan_sektor_tematik/a8_sonuc_json.py` | → `sonuc.json` |

Çalıştırma sırası: a1 → a2 → a3 → a4 → a7 → strateji_adaylari → a5 → a6 → a8. Hepsi `python3 -I` ile, çoklu süreç kullanmadan çalışır.
