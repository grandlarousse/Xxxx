# Denetim: metal_madenci (07.11.2026)

Denetlenen: `notlar/aile_metal_madenci.md`, `kod/ajan_metal_madenci/*.py`, `sonuclar/aile_metal_madenci/sonuc.json`.
Denetim kodu: `kod/denetim_metal_madenci/` (motor.py, d1-d6). Tablolar ve çıktı kayıtları: `sonuclar/aile_metal_madenci/denetim/`.
JSON: `sonuclar/aile_metal_madenci/denetim.json`. Çalıştırma: `python3 -I kod/denetim_metal_madenci/d1_yeniden.py` (d2…d6 aynı şekilde, tek süreç, toplam ~10 sn).

## Kısa sonuç

- **Kod ve zamanlama temiz.** İşlem simülasyonunu `lib.trades` / `lib.evaluate` kullanmadan yeniden yazdım (`motor.py`). Beş adayın da işlem tarihleri ve brüt getirileri ajanınkiyle birebir aynı (fark < 1e-16). İleriye bakma, yanlış gün ya da maliyet hatası bulmadım. NYSE takvimine göre veride eksik ya da fazla gün yok, yani ay sonu tespiti doğru.
- **Çoklu test sonrası ayakta kalan aday yok.** Ajanın "tek yönlü BH'de hiçbir şey geçmiyor" sonucu doğru. S3 için "iki yönlü BH'de geçer" ifadesi ise anlamsız: o eşiği, maliyet yüzünden anlamlı negatif çıkan yüzlerce test gevşetiyor.
- **Kararlarım:**
  - **S3 (GDXJ IBS):** zayıf. Ailenin en sağlam bulgusu ama ajanın "orta" güveni fazla.
  - **S1 / S2 (ay sonu):** zayıf. İkisi aynı bahis.
  - **S4 (GLD IBS):** çürütüldü.
  - **S5 (SILJ Bollinger):** çürütüldü.
- **Lead-lag:** "Doğrulanmış, kullanılabilir gecikmeli öncü yok" sonucu doğrulandı. DBB←KWEB'in hacmi düşük günlerde güçlendiğini gösterdim; bu, bayat fiyat artefaktına işaret ediyor.

## A) Yeniden üretim ve zamanlama

| id | denetim: n / brüt / net bp / t | IS net (t) / OOS net (t) | ajanla aynı mı |
|---|---|---|---|
| S1 GDX ay sonu C0 h3 | 111 / 97,7 / 84,5 / 2,20 | 82,3 (1,75) / 86,5 (1,44) | evet |
| S2 GLD ay sonu C0 h3 | 111 / 52,9 / 39,9 / 2,45 | 33,8 (1,65) / 45,4 (1,81) | evet |
| S3 GDXJ IBS C0 h3 | 240 / 121,2 / 107,2 / 3,39 | 85,4 (1,82) / 127,6 (2,99) | evet |
| S4 GLD IBS C0 h3 | 140 / 52,3 / 39,3 / 2,07 | 54,6 (1,90) / 27,4 (1,08) | evet |
| S5 SILJ BB C1 h3 | 48 / 208,6 / 192,6 / 3,10 | 189,4 (1,87) / 195,3 (2,49) | evet |

Kontroller:

- **Sinyaller:**
  - IBS ve `close<close[1]` t barından hesaplanıyor; bölme sıfır olduğunda NaN kalıyor ve sinyal üretmiyor.
  - BB20 `rolling(20)` ile, t dahil. Ay sonu takvimden geliyor.
  - Hiçbiri t+1 verisi kullanmıyor.
- **Giriş ve çıkış:** C0 = c[t] → c[t+3]; O1 = o[t+1] → c[t+3]; C1 = c[t+1] → c[t+4]. Çakışma kuralı doğru. Maliyet işlem başına bir kez düşülüyor.
- **Maliyet modeli:** Makas kademesi son 252 günün likiditesine dayanıyor (hafif ileriye bakma). Tarihsel likiditeyle hesaplayınca etki küçük; tek fark S5'te:
  - S3: 106,6 bp / t 3,38.
  - S5: maliyet ortalaması 27,7 bp, net 181 bp.
- **Katı çakışma varyantı** (çıkış günü gelen sinyalle yeniden girilmez): S3 t 3,28 · S4 **t 1,68** · S5 t 3,25.
- **200 günlük ısınma:** Ajan bütün sinyallerde ilk 200 günü atıyor. Bu S5 için gereksiz ve sonucu güzelleştiriyor. 20 günlük ısınmayla S5: n=55, 150 bp, IS t 1,26.
- **En büyük kazançlar:**
  - S3'ün en büyük işlemi 12.03.2020: +%33,7. O gün GDXJ −%26,3 kapandı. Aynı gün GDX −%11,4 ve SILJ −%18,2; JNUG'dan çıkan endeks hareketi ~−%20,5. Kapanış NAV'a göre yaklaşık %6-7 iskontoluydu. Ertesi açılış +%18,8 (sinyal gecelerinin en büyüğü).
  - Bu bir veri hatası değil, gerçek bir likidite olayı (veri_kalitesi.csv'de var). Ama o günkü 2 bp makas varsayımı geçersiz.
  - Diğer büyük kazançlar 2026'daki altın boğasından (Şubat, Mart, Haziran, Ağustos). Tek olaya bağımlılık yok.
- **IAU 2021-03-08 hatalı bar:** Ajanın tespiti doğru (IAU +%8,5 iken GLD −%1). Bar dahilken IAU←GLD yetişme t'si 3,27; bar atılınca −0,56.
  - **Not:** Bu bar `lib.BAD_BARS`'ta yok. `genel_tum.csv` ve `leadlag_sweep.csv`'deki IAU satırları bu bardan etkileniyor.

## B) İstatistiksel sağlamlık (d2_saglamlik.log)

### S3: GDXJ IBS<0,10 ve düşüş, C0, 3 gün → zayıf

**Geçtiği testler:**

| Test | Net bp | t |
|---|---|---|
| 2020 hariç | 81,6 | 2,76 |
| 2022 hariç | — | 3,22 |
| 2020 + 2022 hariç | 80,9 | 2,54 |
| 2024-26 hariç | 74 | 2,04 |
| En iyi 5 işlem hariç | 70 | 2,65 |
| 1.000 $ pozisyon (32 bp maliyet) | 89 | 2,82 |
| 10.000 $ pozisyon | 116 | 3,68 |
| +10 bp ek kayma | 97 | 3,08 |

- Rastgele giriş permütasyonu (5.000 tekrar, aynı n, h=3): p=0,0004. Yıl tabakalı sürümde p=0,0002. Rastgele girişlerin ortalaması 23-25 bp.
- C0 modunda h=1-5 arasında her tutuşta t > 2,2.

**Kaldığı testler:**

1. **Çoklu test.** 8.316 aile satırının birincisi. Tek yönlü p≈0,0004; Bonferroni ya da BH (eşik ~6,7e-5) altında geçmez. Etkin bağımsız test sayısı ~300-1.000 olsa bile, bu kadar denemenin en iyisi için beklenen t ≈ 3,0-3,7. 3,39 bu aralıkta.
2. **IS kanıtı yalnız seçilen ETF'de.** Aynı kural IS'te GDX −3 bp, RING −11, SILJ −50, SIL +35. Madenci havuzunda IS 14 bp (t 0,51), OOS 113 bp (t 3,45).
   - Ayrıca "OOS" seçim sırasında görülmüş veri: seçim tam örneklem t'siyle yapıldı, yani gerçek bir holdout değil.
3. **Eşik komşuluğu IS'te çöküyor.** IS t: 0,125'te 0,49; 0,15'te 0,32; 0,20'de 0,28. OOS ise her eşikte 2,7-3,3.
   - Yani etki 2022-2026 madenci rejimine özgü.
4. **"O1'de de güçlü" ifadesi abartılı.** O1'de güçlü olan yalnız h=3; komşu tutuşlar zayıf:

   | O1 tutuşu | h1 | h2 | h3 | h4 | h5 |
   |---|---|---|---|---|---|
   | t | 0,68 | 1,39 | 2,74 | 1,15 | 1,50 |

   - Bu düz bir plato değil, sivri bir tepe. C1 h3: t 0,93.
   - Sinyal gecesinin ortalaması 33,7 bp; koşulsuz gece 10,5 bp. C0 kenarının ~1/3'ü bu ilk gecede.
   - Sonuç: kural **kapanışa bağımlı** olarak etiketlenmeli. Midas'ta MOC yok; sinyal 5-10 dk önceki fiyatla tahmin edilir. Bu yanlış sınıflandırma riski gün içi veri olmadan ölçülemiyor.
5. **Aynı bahis.** S4 sinyal günlerinin %52'si S3 ile aynı gün; işlem getirilerinin korelasyonu 0,81. S3 kenarı GLD'nin de zayıf kapandığı günlerde yoğunlaşıyor:
   - GLD IBS < 0,2 iken: 147 bp, t 3,09.
   - Diğer günler: 63 bp, t 1,55.
6. **Etki aileye özgü değil.** IBS etkisi geniş bir hisse ETF'i olgusu: genel kütüphanede ETF'lerin %84'ünde kenar pozitif, QQQ'da t 3,68. Bu, etkinin var olduğuna dair ön kanıtı destekliyor. Ama GDXJ'deki büyüklük seçimle şişmiş olmalı.

### S1 / S2: ay sonu → zayıf

**S1 (GDX):**
- En iyi 5 işlem hariç: 40 bp, t 1,17.
- 2020 hariç: t 1,58. 2024-26 hariç: t 1,29.
- Permütasyon p=0,025 (yıl tabakalı 0,028).
- 1.000 $ pozisyonda t 1,74; +10 bp kaymada t 1,94.
- O1 t 1,23; C1 t 1,36. İlk gece C0 h1'de 53 bp (t 2,40): büyük ölçüde kapanışa bağımlı.

**Giriş günü komşuluğu (S1):**
- Sondan 2., 3. ve 4. günde girişler h=1-3'te negatif. Etki yalnız yeni ayın ilk günlerinde.
- Son gün girişinde h=1…6 hep pozitif (t 1,8-2,6).
- Bu yapı ay dönümü literatürüyle uyumlu, ama tek kümede ve FDR'siz.

**S2 (GLD):**
- 2024-26 hariç: 16 bp, t 0,90 (son üç yılın altın boğasına bağlı).
- En iyi 5 işlem hariç: t 1,46. 1.000 $ pozisyonda t 1,34. Permütasyon p=0,012.
- 2021-2023 üç yıl üst üste ≤ 0.

S1 ile S2 aynı bahistir (GLD-GDX korelasyonu 0,86).

### S4: GLD IBS → çürütüldü

| Test | Net bp | t |
|---|---|---|
| En iyi 5 işlem hariç | 15,7 | 0,98 |
| 2020 hariç | — | 1,61 |
| 2020 + 2022 hariç | — | 1,03 |
| Katı çakışma | — | 1,68 |
| 1.000 $ pozisyon | — | 1,12 |
| +10 bp kayma | — | 1,54 |
| OOS | — | 1,08 |
| IAU kopyası | — | 0,98 |

- Eşik komşuları (0,05 / 0,075 / 0,125 / 0,15): t 1,88 / 1,82 / 1,37 / 1,62.
- S3'ten bağımsız günlerde: 33 bp, t 1,25.

### S5: SILJ Bollinger, C1 → çürütüldü

- **Parametre komşuluğu sivri:**
  - BB uzunluğu 25 → t 0,62; 30 → t 0,59.
  - k = 1,5 → t ≤ 1,40.
- **Bekleme süresi:** 0 / 1 / 2 / 3 gün → t 1,03 / 3,16 / 1,92 / 0,91. Yalnız 1 gün bekleme çalışıyor.
- 20 günlük ısınmayla IS t 1,26.
- 2020 + 2022 hariç: t 1,68. En iyi 5 işlem hariç: t 1,87.
- 8.316 satırda ikinci sırada; n=48.

## Lead-lag (d3_leadlag.log; kendi regresyonum, kendi 2 gecikmesi kontrollü, Newey-West)

| hedef ← öncü | t | IS / OOS | bp/sd vs maliyet | gece / gün içi t | karar |
|---|---|---|---|---|---|
| DBB ← KWEB | 3,94 | 2,60 / 3,02 | 10,4 < 27 | 2,97 / 2,55 | zayıf: düşük hacimli DBB günlerinde t 3,91, yüksek hacimli günlerde 1,74 → bayat fiyat |
| GDX ← GLD (yetişme) | L t 0,04 | 0,84 / −1,30 | — | — | çürütüldü (ajanla aynı) |
| GLD ← GDX | 2,33 | 1,52 / 1,58 | 10,6 < 13 | 2,16 / 1,52 | zayıf |
| SLV ← T10YIE_d | 3,04 | 2,69 / 1,83 | 13,5 ≈ 14 | 2,53 / 1,79 | kullanılamaz: kapanışta gözlenebilir vekil (TIP−β·IEF) OOS t 1,11 (h3 −1,14); kural t < 1,3 |
| PPLT ← GDX | 3,20 | 3,42 / 1,49 | 23 > 20 | 3,40 / 1,94 | zayıf: FDR yok, etki çoğunlukla gece |
| COPX ← GDX (h3) | 2,76 | 3,02 / 1,58 | 36 > 14 | 2,44 / 0,89 | zayıf: kural t 1,27 |
| GDX / GDXJ ← LQD | 2,0-2,2 | 3,1-3,3 / 0,00 | — | — | çürütüldü |
| URA ← SPY (−) | −2,67 | −2,38 / −1,49 | 22 > 16 | — | zayıf: FDR yok |
| XME ← DIA (−) | −2,80 | −2,69 / −1,47 | 28 > 14 | — | zayıf: FDR yok |
| IAU ← GLD | 3,27 | — | — | — | veri hatası (bar atılınca −0,56) |

`leadlag_sweep.csv`'de aile hedefleri için FDR'yi geçen tek satır DBB←KWEB. Ajanın gerçek zamanlı izleme önerileri (COMEX:GC1!, COMEX:SI1!, COMEX:HG1!, NYMEX:PL1!, OANDA:XAUUSD, TVC:DXY, CBOT:ZN1!, CME_MINI:ES1!, HKEX:HSI1!, FX_IDC:USDCNH) ve kullandığı 28 kodun tamamı `tv_dogrulama.csv` / `tv_etf.csv`'de doğrulanmış. TSX:U.UN ve NYSE:CCJ doğru biçimde `tv_dogrulanacak` listesinde.

## İzleme listesine itirazlar

- **SLV ve COPX "kabul" → "yedek / yalnız izleme".** İkisinde de doğrulanmış strateji ya da gecikmeli öncü yok; tek gerekçe gerçek zamanlı sürücü (SI1!, HG1!). SLV'de 30.01.2026'da tek gün −%28,5 kuyruk riski var.
- **GLD ve GDX kabul edilebilir** (ana araçlar). Ama gerekçe "doğrulanmış strateji yok; S2/S1 zayıf, S4 çürütüldü" diye düzeltilmeli.
- **GDXJ kabul edilebilir.** Etiket şöyle olmalı: "S3 zayıf, kapanışa bağımlı; maxDD −%26".
- **JNUG / NUGT "yedek (koşullu)".** Gerekçeler:
  - Midas'ta bulunurlukları doğrulanmadı.
  - 2020-Q2'ye kadar 3x'ti; geçmiş istatistikler karışık kaldıraçla hesaplandı.
  - JNUG ile S3: maxDD −%51, en kötü işlem −%21.
- **SILJ / SIL yedek kalabilir.** Ama S5 gerekçe olarak kullanılmamalı (çürütüldü).
- **IAU yedek kalabilir.** 2021-03-08 hatalı barı ortak `lib.BAD_BARS`'a eklenmeli.

## Kaçırılanlar

1. **Yoğunlaşma riski.** S3, S4, S1 ve S2 aynı altın kompleksi bahsi. S4 günlerinin %52'si S3 ile aynı gün (korelasyon 0,81); S3 sinyallerinin 15'i ay sonuna denk geliyor. Birlikte açılırsa risk 2-3 katına çıkar. Kural "aynı gün tek pozisyon (GDXJ)" olmalı.
2. **Stres anında kapanış/NAV sapması.** S3'ün en iyi işlemi kısmen NAV iskontosunun kapanmasından geldi. Böyle günlerde makas 2 bp değildir. Kapanışa yakın piyasa emri yerine limit emir kullanılmalı.
3. **Ortak kütüphanede eksik veri düzeltmesi.** IAU 2021-03-08 barı ortak veride düzeltilmemiş.
4. **Bayat fiyat.** DBB←KWEB, büyük olasılıkla bayat fiyat artefaktı: etki DBB'nin düşük hacimli günlerinde yoğunlaşıyor. PPLT←GDX ve GLD←GDX'te etkinin çoğu gecede.
5. **Yeni fırsat bulamadım.** Başabaş enflasyonu kapanışta gözlenebilir bir vekille test ettim (TIP − β·IEF; T10YIE_d ile korelasyon 0,68). IS'te güçlü, OOS'ta yok ya da ters (d4_kacirilan.log).

## Denetimde yapılan test sayısı

Yaklaşık 340 kural/regresyon (eşik, uzunluk, h, mod ve giriş günü komşulukları; yıl hariç tutmaları; aile ve havuz testleri; lead-lag regresyonları; vekil testleri) ve aday başına 2 × 5.000 permütasyon. Bunlar karar vermek için yapılmış saldırı testleridir, yeni aday aramak için değil. Hiçbir yeni bulgu aday olarak önerilmiyor.
