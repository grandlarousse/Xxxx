# Aile: enerji_tarim — Midas üzerinden 1-3 günlük ETF işlemleri (2026-11-07)

**Kısa sonuç.** 28 ETF'te toplam **8.635 test** yapıldı (319 aileye özel test + genel kütüphanenin aile içindeki 8.316 satırı). Birleşik BH-FDR (q=0,10) uygulandığında **hiçbir long strateji ayakta kalmıyor**. Bu ailede güvenilir ve işlenebilir bir strateji **bulunamadı**. Kabul eşiğini kâğıt üzerinde geçen **iki zayıf aday** var. İkisi de **düşük güven** etiketiyle raporlandı ve ikisi de **PTP** ürünlerinde işlem görüyor:

- **S1:** EIA doğalgaz raporundan önceki gün KOLD alınır, yalnız Kasım-Mart. İşlem başına net +100 bp, t 2,24. Mevsim ayrımı sonuçlar görüldükten sonra yapıldı (post-hoc).
- **S2:** USO alt Bollinger bandını kırdıktan sonra bir gün beklenir, sonra iki gün USO long tutulur. Net +121 bp, t 2,95. Genel taramadan seçildi. t kapanışında girilirse zarar ediyor.

En sağlam bulgu bir **kaçın kuralı**: UNG/BOIL long pozisyonunu EIA depolama raporu gününe (genelde Çarşamba kapanışından Perşembe kapanışına) taşımayın. Ailedeki ETF'ler için **doğrulanmış bir gecikmeli öncü yok**.

Tablolar: `sonuclar/aile_enerji_tarim/`. Kod: `kod/ajan_enerji_tarim/`. JSON: `sonuclar/aile_enerji_tarim/sonuc.json`.

---

## 1. Yöntem

- **Veri:** `lib.load` ile toplam getiri düzeltilmiş fiyatlar (2016-11-07..2026-11-06). Örneklem içi (IS) dönem 2016-11..2021, örneklem dışı (OOS) dönem 2022..2026-11. Takvimler: `eia_ng_storage`, `eia_petroleum`, `ung_uso_roll`, `vadeler`. OVX ve VIX/VIX3M için `lib.vol_index` kullanıldı.
- **Zamanlama:** lib.py sözleşmesi aynen uygulandı. Sinyal t kapanışına kadarki bilgiyle hesaplanır, takvimler önceden bilinir. Üç giriş modu var:
  - C0: t kapanışı
  - O1: t+1 açılışı
  - C1: t+1 kapanışı

  İşlemler çakışmaz, pozisyon açıkken gelen sinyal yok sayılır.
- **Maliyet:** Midas komisyonu emir başına 1,5 $, gidiş-dönüş 3 $. Buna tarama.csv'deki makas eklenir. Raporlanan ana pozisyon büyüklüğü 2.500 $; duyarlılık için 1.000 $ ve 10.000 $ da hesaplandı.
- **İstatistik:** her aday için şunlar raporlandı (`ortak.full`, `inceleme.rapor`):
  - n, brüt ve net ortalama, kazanma oranı, PF, t
  - IS ve OOS net getiri ile t değerleri
  - pozitif yılların oranı, maxDD, en kötü işlem
  - maliyet duyarlılığı ve C0/O1/C1 × h=1..3 ızgarası
  - aynı kuralın ailedeki diğer ETF'lerdeki sonucu
  - yıl yıl kırılım ve aykırı değer etkisi (en iyi %5 işlem çıkarılmış ortalama)
- **Test sayımı ve FDR (`fdr_toplam.py`):**
  - Her test kaydedildi. Strateji testlerinde tek yönlü p (net > 0) kullanıldı. "Kaçın" testlerinde (yön −) maliyetin işareti yanıltmasın diye brüt t kullanıldı. Tanımlayıcı testlerde ve regresyonlarda iki yönlü p kullanıldı.
  - Aileye özel 319 testin dağılımı: 218 strateji, 25 tanımlayıcı, 76 regresyon. Bunlara genel kütüphanenin 8.316 satırı eklenince toplam 8.635.
  - BH-FDR yalnız aileye özel testlerde 3 sonuç bırakıyor. Bunlardan biri MR_bb20_alt sinyalinin UCO'daki gecikmeli kontrolü; bu sinyal zaten genel taramadan seçildiği için geçerli FDR birleşik olandır. Kalan ikisi CANE "kaçın" testi ve CANE regresyonu. Birleşik testte geçen: **0**.
- **Bağımsızlık:** kopya kümeleri aşağıda. Aynı kümedeki ETF'ler bağımsız kanıt sayılmadı. Aile tutarlılığı küme temsilcileriyle ölçüldü: USO, UNG, XLE, OIH, DBA, CORN, WEAT, CANE.

## 2. İşlenebilirlik ve kopya kümeleri (tarama.csv; 2022+ günlük korelasyon)

| Küme | ETF'ler (korelasyon) | En iyi araç |
|---|---|---|
| Ham petrol + enerji ağırlıklı geniş emtia | USO, BNO (0,98), USL (0,95), DBO (0,95), UCO 2x, SCO −2x, UGA (0,86); DBC/PDBC/GSG/COMT (0,89-0,94), BCI (0,74) | USO (745 mn$, 14 bp, maliyet/oynaklık 0,044). PTP'siz vekil: PDBC (0,13) |
| Doğalgaz | UNG, UNL (0,94), BOIL 2x (0,98), KOLD −2x (−0,97) | UNG referans; araç olarak BOIL/KOLD (0,026/0,023) |
| Enerji hisseleri | XLE, XOP (0,94), OIH (0,86), ERX/GUSH 2x, ERY/DRIP −2x | XLE (2 mlr$, 13,6 bp), XOP (532 mn$, 14 bp) |
| Tarım | DBA, CORN, WEAT, SOYB (0,42-0,65), CANE (ayrık) | Hiçbiri; maliyet/oynaklık 0,13-0,55, likidite 1,8-22 mn$ |

**PTP / K-1 durumu:**
- **PTP (midas_kosullari.md §5.4):** USO, BNO, USL, UNG, UNL, UGA (USCF) ve UCO, SCO, BOIL, KOLD (ProShares Trust II).
- **K-1, muhtemel PTP; Midas'ta doğrulanmadı:** DBO, DBC, DBA (Invesco DB), GSG ve CORN, WEAT, SOYB, CANE (Teucrium).
- **PTP değil** (1940 Kanunu fonu ya da K-1'siz yapı): XLE, XOP, OIH, ERX, ERY, GUSH, DRIP, PDBC, BCI, COMT.

**%10 brüt satış stopajının anlamı:** bu kesinti uygulanırsa her işlem yaklaşık **−1000 bp** kaybeder. Bu ailede bulunan hiçbir etki işlem başına 250 bp'yi aşmıyor. Yani kesinti uygulanan bir PTP üründe hiçbir strateji para kazandırmaz. USCF'nin son qualified notice'ı (31.07.2026) yaklaşık 31.10.2026'da süresini doldurdu ve yenisi bulunamadı. ProShares bildirimi 26.02.2026 tarihli; sonraki bildirimler kontrol edilmedi.

## 3. Genel kütüphane, aile içi (`genel_aile.csv`, 8.316 satır)

- **Aile tutarlılığı:** 8 küme temsilcisinde Stouffer t en yüksek **2,10** çıktı (VX_backw_donus C0 h2). IS ve OOS'ta birlikte pozitif olan temsilci sayısı 8'de 2. Tek yönlü BH-FDR'yi geçen satır sayısı: **0**.
- **Kâğıt üzerinde eşiği geçen tek-ETF sonuçları** (23 satır) tek bir kümede yoğunlaşıyor: ham petrol (USO, UCO, DBO, BNO, UGA). İki sinyal öne çıkıyor:
  - **MR_bb20_alt** (C1 h2). İnceleme sonucu S2 olarak düşük güvenle tutuldu (§5).
  - **VX_backw_donus** (C1 h2). Elendi; getirinin büyük kısmı 2026'dan geliyor (§6).
- **Diğer tek-ETF sonuçlar** (CANE MO_z1_gt_2, ERY MO_z1_gt_2, KOLD CA_sal, GUSH MO_3gun) kendi kümelerinde tekrar etmiyor ya da IS ve OOS'ta işaret değiştiriyor.
- **Haftanın günü:** tek anlamlı örüntü Çarşamba → Perşembe. Bu, EIA rapor günü etkisinin kendisi:
  - UNG CA_car C0 h1 brüt −32 bp; net olarak 11 yılın hiçbirinde pozitif değil.
  - KOLD aynı günde net +54 bp, t 1,9.

## 4. Aileye özel hipotezler (hipotezler.csv EN01-EN08 + yönlendirme)

**Doğalgaz** (`h_dogalgaz.py` → `dogalgaz_*.csv`):

| Test | Sonuç |
|---|---|
| EN01 EIA depolama rapor günü (UNG / BOIL / KOLD günlük getiri, rapor günü vs diğer günler) | UNG −34 vs −4 bp (t −1,80); BOIL −85 vs −23 (t −2,01); KOLD +42 vs −24 (t 2,18). IS ve OOS'ta aynı işaret. |
| EN01 strateji: rapordan önceki gün KOLD, C0 h1 (önceden belirlenmiş) | Net 43 bp, t 1,65, IS 37 / OOS 50, pozitif yıl oranı %82. **Eşik altı.** En iyi %5 işlem çıkarılınca brüt −13 bp. |
| EN01 kış alt kümesi (Kas-Mar) → **S1** | Net 100 bp, t 2,24 (§5). Yaz (Nis-Eki): net 3 bp, t 0,10. |
| EN02 kontango vekili k20 = Δ20 ln(UNL) − Δ20 ln(UNG) > 0 → KOLD | C0 h3 net 103 bp, t 2,29. Komşu pencereler çöküyor (k10/k40/k60: t 0,54/0,96/0,51). Regresyon t −0,99. **Elendi.** |
| EN02 koşulsuz sürüklenme | UNG −10 bp/gün (t −1,48), BOIL −36 (t −2,73), KOLD −10, UNL −3. |
| EN03 UNG roll penceresi / BOIL-KOLD roll | KOLD (R1 öncesi) t ≤ 1,13 ve işaret değişiyor; UNG−UNL roll günü farkı t −0,89. **Elendi.** |
| NG son işlem günü / ertesi | t 1,61 / −1,38; IS ve OOS işaret değiştiriyor. **Elendi.** |
| Mevsim (Kas-Mar) | UNG −22 vs −2 bp/gün (t −1,37); kışın \|hareket\| 1,29 kat (t 6,6). |
| Büyük gün sonrası devam/dönüş | UNG/BOIL/KOLD'da pozitif t > 1 yok. **Elendi.** |

**Petrol ve enerji hisseleri** (`h_petrol.py` → `petrol_*.csv`):

| Test | Sonuç |
|---|---|
| EN04 WPSR günü | USO \|r\| oranı 1,04 (t 0,78); yön yok. |
| EN05 USO roll | USO−USL roll günü farkı t −0,24 (2020 öncesi −20 bp, t −1,04). |
| EN06 petrol → XLE/XOP/OIH yetişme (z(res) ≥ 2) | XLE C0 h1 net 50 bp (t 1,37) yalnız IS; OOS ~0; O1/C1 negatif. Kendi getirisi kontrol edilince yetişme katsayısı t 0,56. Ters yön (XLE → USO) negatif. **Elendi.** |
| EN07 OVX ≥ 1,25 × SMA20 | 3 günlük \|hareket\| 2,4 kat (t 5,8) → **boyut ve risk kuralı olarak geçerli**. Yön sinyali olarak USO C0 h3 net −186 bp. |
| EN08 IBS < 0,15 ve C > SMA200 (XLE, XOP, USO, BNO) | Net −32..+5 bp. **Elendi.** |
| USO/USL eğri vekili c20 | t ≤ 1,6. **Elendi.** |
| BNO−USO yayılımı z20 | Regresyon t −0,15 / 0,46. **Elendi.** |

**Tarım ve lead-lag kuralları** (`h_tarim_leadlag.py`):
- CANE ← BNO: z1(BNO) ≥ 1 sonrası CANE brüt +2 bp (net −25). Etki yalnız petrol düşüş günlerinde görülüyor.
- XOP ← UNG: net 36 bp, t 0,89, OOS negatif.
- DBA / CORN / WEAT / SOYB için petrol ve SPY'nin, ETF'in kendi gecikmesine ek katkısı yok (WEAT ve DBA'da yalnız OOS'ta t > 2).

## 5. Aday stratejiler (ikisi de DÜŞÜK güven)

### S1 — EIA doğalgaz raporu öncesi KOLD (yalnız Kasım-Mart) · `kod/ajan_enerji_tarim/aday_S1_eia_kold.py`

**Kural:** EIA depolama raporunun tarihi Kasım-Mart arasındaysa, rapordan önceki ABD işlem günü (genelde Çarşamba) AMEX:KOLD kapanışta alınır. Kış saatinde bu TR 23:45-23:59'dur. MOC (kapanışta piyasa emri) olmadığı için kapanıştan dakikalar önce piyasa emri verilir; alternatif olarak kapanış sonrası after-hours limit emri kullanılabilir. Pozisyon rapor günü kapanışta satılır.

**Yakın uygulama günleri:**
- 12 Kas Per (rapor 13 Kas Cum, Veterans Day nedeniyle)
- 18 Kas Çar
- 24 Kas Sal (rapor 25 Kas Çar 12:00 ET = TR 20:00)
- 2, 9, 16, 23, 30 Ara

**Sonuçlar:**

| Ölçü | Değer |
|---|---|
| n | 216 |
| Brüt / net (2.500 $) | 116,5 / 100,5 bp |
| Kazanma oranı | %58,3 |
| PF | 1,53 |
| t | 2,24 |
| IS net (t) | 113 bp (1,97) |
| OOS net (t) | 86 bp (1,22) |
| Pozitif yıllar | 7/11 |
| maxDD | −%41,7 |
| En kötü işlem | −1.664 bp |
| Maliyet duyarlılığı (1.000 / 2.500 / 10.000 $) | 82 / 100 / 109 bp |

**Mod sağlamlığı:**
- O1 (rapor günü açılışında giriş, TR 17:30): net 64,5 bp, t 2,13.
- C1: negatif. Bu beklenen bir sonuç, çünkü etki rapor gününün kendisinde.

**Ailedeki karşılıkları (aynı günler):**
- UNG: net −81 bp (t −3,34)
- BOIL: net −137 bp (t −3,08)
- UNL: net −81 bp

**Neden düşük güven:**
- Önceden belirlenmiş hipotez tam yıl versiyonuydu ve t 1,65'te kaldı. Kış ayrımı sonuçlar görüldükten sonra eklendi (post-hoc). Komşu mevsim tanımları destekliyor: Eki-Mar t 2,35, Kas-Nis 2,26, Kas-Şub 2,23, Ara-Şub 1,60.
- FDR'yi geçmiyor: p = 0,013, oysa birinci sıra için eşik 0,0003.
- Getiri kalın kuyruklu: en iyi işlem +%42.
- KOLD'un Midas'ta bulunurluğu doğrulanamadı.
- KOLD bir PTP ürünü.

Literatür yönü destekliyor: Prokopczuk ve diğ. (2021) rapor gününde NG vadelisinde −%0,37 buldu. Ancak aynı çalışma 2014-2018 alt döneminde etkinin olmadığını da bildiriyor.

### S2 — USO alt Bollinger kırılımı, 1 gün bekle, 2 gün long · `kod/ajan_enerji_tarim/aday_S3_uso_bb_gecikmeli.py`

**Kural:** AMEX:USO günlük grafiğinde Bollinger Bantları kullanılır: uzunluk 20, kaynak kapanış, **StdDev 2,05**. TradingView popülasyon standart sapması kullanır; 2,05 çarpanı backtestteki örneklem std'li 2,0'a denk gelir. Sinyal: t günü kapanış alt bandın altında.
- t kapanışında **girme**.
- t+1 kapanışına yakın (TR 23:45) USO ya da UCO al.
- t+3 kapanışında sat.

**Sonuçlar:**

| Ölçü | Değer |
|---|---|
| n | 54 |
| Brüt / net | 135 / 121 bp |
| Kazanma oranı | %68,5 |
| PF | 2,63 |
| t | 2,95 |
| IS net (t) | 75 bp (1,13) |
| OOS net (t) | 167 bp (3,47) |
| Pozitif yıllar | 7/9 |
| maxDD | −%9,3 |
| En kötü işlem | −763 bp |
| Maliyet duyarlılığı (1.000 / 2.500 / 10.000 $) | 103 / 121 / 130 bp |
| 2026 hariç | t 3,04 |

**Mod sağlamlığı:**
- C0 h2 net −38 bp; O1 h2 net −4 bp. Etki **1 günlük beklemeye bağlı**: t+1 günü düşüş sürüyor, dönüş t+2..t+3'te geliyor.
- Sinyal bir gün kaydırılıp t+2 açılışında girilirse (h=2): net 90 bp, t 3,14.

**USO sinyaliyle diğer ETF'ler:**

| ETF | Net (t) |
|---|---|
| BNO | 94 bp (2,30) |
| DBO | 95 bp (2,40) |
| UCO | 225 bp (2,86) |
| XOP | 131 bp (2,49), ancak h=1 ve h=3'te ~0 |
| XLE | 63 bp (1,80) |
| PDBC | 41 bp (1,78) |

ETF'ler kendi bantlarıyla sinyal üretirse sonuç zayıflıyor: BNO 40 bp (t 0,90), XLE −20, XOP −42.

**Neden düşük güven:**
- Genel taramadan seçildi: 31 sinyal × 9 varyant × 28 ETF.
- Birleşik FDR'yi geçmiyor.
- IS'te anlamsız (t 1,13).
- Sonuç sinyal günlerine duyarlı.
- USO ve UCO PTP ürünleri.

## 6. Elenenler (özet; ayrıntı sonuc.json → elenen)

- **VX_backw_donus → USO/BNO/UCO C1 h2:** kabul eşiğini kâğıt üzerinde geçiyor (USO net 162 bp, t 2,43) ama 2026'daki 6 işlem toplam getirinin yaklaşık %58'ini oluşturuyor. 2026 hariç tutulunca yaklaşık 77 bp ve t ~1,2'ye düşüyor. PTP'siz XLE'de t 1,37; SPY'de etki yok.
- **Diğer elenenler:** EN01 tam yıl, EN02 k20, EN03, EN04, EN05, EN06, EN07 (yön olarak), EN08, c20, BNO−USO yayılımı, NG vade günü, mevsim ve haftanın günü, büyük gün sonrası, CANE ← petrol, XOP ← UNG, tarım ve geniş emtia. Gerekçeler §4'te.

## 7. Risk kuralları (strateji değil, ama veriyle destekli)

1. **UNG/BOIL long'u EIA rapor gününe taşımayın.**
   - UNG rapor günü brüt ortalaması −28 bp; 2018-2026 arasındaki 9 yılın hepsinde brüt yıl ortalaması negatif.
   - BOIL brüt ortalaması −66 bp.
   - Kışın etki iki katına çıkıyor: UNG −58 bp, BOIL −119 bp.
2. **OVX ≥ 1,25 × SMA20 iken** petrolün 3 günlük ortalama \|hareketi\| 2,4 kat büyüyor. UCO/SCO açmayın ya da pozisyonu küçültün (EN07).
3. **PTP etiketli fonlarda** her işlemden önce uygulamadaki PTP ibaresine ve kesinti bilgisine bakın. Kesinti varsa hiçbir 1-3 günlük işlem kârlı olamaz.

## 8. İzleme listesi

| ETF | Karar | Not |
|---|---|---|
| USO | kabul | Ham petrolün ana aracı, S2. PTP; Midas'ta bulunurluk doğrulanmadı. |
| XLE | kabul | PTP'siz, en likit; strateji yok, sürücüleri net. |
| KOLD | kabul (koşullu) | S1 aracı. PTP; Midas'ta bulunurluk doğrulanmadı. |
| BNO | yedek | USO kopyası (Brent), PTP. |
| UCO | yedek | 2x petrol, S2 sinyali için, PTP. |
| SCO | yedek | −2x petrol, PTP. |
| UNG | yedek | Referans; long için önerilmez, PTP. |
| BOIL | yedek | 2x doğalgaz, PTP. |
| XOP | yedek | PTP'siz. |
| DRIP | yedek | −2x XOP, PTP'siz. |
| PDBC | yedek | K-1'siz petrol vekili. |
| Kalan 17 ETF | red | Ayrıntılar JSON'da. |

## 9. Lead-lag (kabul ve yedek ETF'ler; `leadlag_ozet.py` → `leadlag_ozet.csv`, `leadlag_yetisme_ek_katki.csv`)

- **(a) Eşzamanlı sürücüler (öncü değil):**
  - USO ← BNO (corr 0,97), USL (0,91), XLE (0,63), FRED:T10YIE (0,60)
  - XLE ← USL (0,70), BNO, USO
  - KOLD ← UNG (−0,97), UNL (−0,93)
  - XOP ← XLE (0,92)
  - PDBC ← BNO/USO (0,89-0,90)
- **(b) Gecikmeli öncü:** 11 hedefin **hiçbirinde doğrulanmış gecikmeli öncü yok**. Ölçüt: FDR + IS ve OOS'ta aynı işaret + bp/sd > maliyet; geçen 0.
  - En güçlü (ama geçmeyen) adaylar: VVIX, KWEB, CPER (h3, t 2,2-3,1, FDR yok, 15-50 bp/sd).
  - Yetişme boşluğunun, ETF'in kendi getirisine ek katkısı en çok XOP ← gap(UNG) h3'te görülüyor: t 2,70, ama OOS t 1,27.
  - Ailede FDR'yi geçen tek gecikmeli ilişki CANE ← petrol (t 3,3-4,4). Ekonomik büyüklüğü 10-12 bp/sd ve 27 bp'lik maliyetin altında.
- **(c) Gerçek zamanlı izlenecekler** (ETF kapalıyken işler; açılış boşluğunu önceden gösterir, öncü değildir):
  - Petrol: NYMEX:CL1!, NYMEX:CL2! (eğri), ICEEUR:BRN1!, TVC:DXY
  - Doğalgaz: NYMEX:NG1!, NYMEX:NG2!, ICEENDEX:TFM1!
  - Enerji hisseleri: CME_MINI:ES1!, NYMEX:CL1!, NYMEX:NG1!
  - PDBC: CL1!, BRN1!, COMEX:GC1!, COMEX:HG1!, CBOT:ZC1!

  Kodların hepsi `tv_dogrulama.csv`'de doğrulandı. Ek doğrulama gerektiren kod yok.
- **Takvim riskleri (yakın tarihler):**
  - EIA doğalgaz: 13 Kas Cum, 19 Kas, 25 Kas Çar 12:00 ET, 3/10/17/24/31 Ara
  - WPSR: 12 Kas Per 12:00 ET, 18 ve 25 Kas, Aralık'ta Çarşambalar
  - NG vadesi: 25 Kas ve 29 Ara; CL vadesi: 20 Kas ve 21 Ara
  - UNG roll: 11-16 Kas ve 15-18 Ara; BOIL/KOLD roll: 8-14 Ara; USO roll: 1-7 Ara
  - Makro: CPI 10 Kas, NFP 4 Ara, FOMC 9 Ara
  - Yarım gün: 27 Kas (TR 21:00)

## 10. Sınırlamalar

- **IS dönemi ve USO:** IS dönemi USO'nun 2020 Nisan negatif fiyat dönemini ve yapı değişikliğini içeriyor: çok vadeli portföy, 4 günlük roll'dan 10 güne, 2026'dan itibaren 5 güne geçiş. 2020 öncesi USO bugünkü fonu temsil etmiyor.
- **Eksik veri:** Henry Hub spot verisi ve NG/CL vadeli eğrisi yok. Kontango ancak UNG/UNL ve USO/USL oranlarıyla vekil olarak ölçülebildi.
- **Takvim kaynakları:** EIA doğalgaz takviminin 2016-2024 kısmı resmî kaynaktan değil, kurala göre üretildi. UNG roll tarihleri de kuraldan türetildi (USCF CSV'sine erişilemedi).
- **Makas:** makas, kademeli bir tahmin (`spread_bp_tier`). Kaldıraçlı fonlarda gerçek makas oynak günlerde daha geniş olabilir.
- **Kalın kuyruklar:** BOIL/KOLD/UCO getirileri kalın kuyruklu; t istatistikleri birkaç büyük günden etkileniyor (aykırı değer satırları aday betiklerinde).
- **Midas'a özgü belirsizlikler:** KOLD/UCO/SCO/BOIL/USO'nun Midas'ta bulunurluğu ve PTP kesinti durumu doğrulanamadı. Uzatılmış saatlerde yalnız limit emir verilebiliyor; MOC yok.

## 11. Tekrar üretim (`python3 -I`, proje kökünden; sırayla)

```
python3 -I kod/ajan_enerji_tarim/alt_kume.py                 # genel_aile.csv, leadlag_aile.csv, aile_tutarlilik.csv
python3 -I kod/ajan_enerji_tarim/h_dogalgaz.py
python3 -I kod/ajan_enerji_tarim/h_petrol.py
python3 -I kod/ajan_enerji_tarim/h_tarim_leadlag.py
python3 -I kod/ajan_enerji_tarim/leadlag_ozet.py
python3 -I kod/ajan_enerji_tarim/ek_kontroller.py
python3 -I kod/ajan_enerji_tarim/fdr_toplam.py
python3 -I kod/ajan_enerji_tarim/aday_S1_eia_kold.py        # S1 sayıları
python3 -I kod/ajan_enerji_tarim/aday_S3_uso_bb_gecikmeli.py  # S2 sayıları
python3 -I kod/ajan_enerji_tarim/aday_S2_vix_backw_petrol.py  # elenen VX_backw_donus incelemesi
python3 -I kod/ajan_enerji_tarim/rapor_json.py               # sonuc.json
```

`alt_kume.py`, hazır sonuçlardan (`sonuclar/genel_tum.csv`, `leadlag_sweep.csv`) aile alt kümesini ve küme temsilcileri için tutarlılık tablosunu (Stouffer t) üretir. Bu betik ilk çalıştırılmalıdır.

Genel kütüphanede eşiği kâğıt üzerinde geçen ve S1/S2 dışında kalan tek-ETF satırları ailede tekrar etmiyor: DBO MR_3gun_dusus, BNO MR_rsi2_lt10_ust200, UCO/BNO VX_kontango_09 (yalnız C0'da, yani VIX'in 16:15 kapanışına bağımlı), CANE MO_z1_gt_2, ERY MO_z1_gt_2, GUSH MO_3gun_yukselis. Gerekçeler sonuc.json'daki elenen listesinde.
