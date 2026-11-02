# v_M4_b — 2. aşama doğrulama (şeytanın avukatı): JP/AU çelik-madenci z-kompoziti (t) → EREGL/KRDMD/BRSAN gün-içi (t)
Doğrulayıcı: v_M4_b · 02.11.2026
Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_M4_b/`
- `vb.py`: kendi modülüm. ll.py, mh.py ve v.py import edilmedi; her şey ham parquet ve `ldate` üzerinden.
- Betikler s1…s9; sonuçlar aynı dizinde `res_*.csv`.

## HÜKÜM: DÜZELT
- **İstatistiksel ilişki: ORTA güven.** Gerçek, sektöre özgü; Avrupa çeliğinde ve gerçek VİOP vadeli verisinde de görülüyor.
- **İddia edilen işlem getirisi: DÜŞÜK güven.** Rakamlar kurguya ve parametreye duyarlı, seçimle şişirilmiş ve 2024–26'da ≈0.
- 1. aşamayla genel olarak hemfikirim. Üç noktada ayrılıyorum (bkz. §8):
  - Dürüst seçim sonucu 1. aşamanın bulduğu kadar kötü değil.
  - "Kâr en iyi 10 günde" eleştirisi yanıltıcı.
  - VİOP vadeli testi yeni ve karışık bir kanıt.

---

## 1. Yeniden üretim ve kurgu duyarlılığı (s1)
| Kurgu (15 bps, \|z\|>1) | EREGL IS | EREGL OOS | KRDMD IS | KRDMD OOS | BRSAN OOS |
|---|---|---|---|---|---|
| ffill / BIST takvimi (orijinal kurguya benzer) | +12,1 (1,47) | **+27,3 (2,31)** | +26,3 (2,33) | **+32,1 (2,18)** | +35,4 (2,10) |
| **Kendi kurgum** (sürücü kendi takviminde, ldate==t ise atanır, ffill yok) | +12,4 (1,57) | +23,1 (2,00) | +23,6 (2,14) | +27,8 (1,82) | +38,3 (2,24) |
| En az 3 bileşen zorunlu | +13,4 | +18,9 (1,59) | +21,0 | +23,8 (1,52) | +36,1 (2,08) |

- İddia ffill kurgusuyla birebir tekrarlanıyor.
- Eşit derecede makul başka bir hizalamayla OOS t değerleri 2,34/2,18'den **2,00/1,82**'ye iniyor. Yani raporlanan rakamlar aralığın üst ucunda.

Korelasyon (kendi kurgum, z_t ile gün-içi_t, NW t):
- EREGL: r 0,082 (t 4,6; IS 3,6; OOS 3,0).
- KRDMD: r 0,083 (t 4,4; IS 2,9; OOS 3,4).
- BRSAN: r 0,066 (t 3,9).

Parametre duyarlılığı (OOS, EREGL / KRDMD):
| Varyant | EREGL | KRDMD |
|---|---|---|
| eşik 0,5 | +5,2 (0,64) | +16,8 (1,60) |
| eşik 0,75 | +20,8 (2,19) | +29,7 (2,34) |
| eşik 1,25 | +17,6 (1,20) | +30,7 (1,82) |
| eşik 1,5 | +29,1 (1,61), ama IS −4,3 | — |
| işaret modu (eşiksiz) | −4,2 | −0,9 |
| z penceresi 120 | +20 (1,7) | +25 (1,8) |
| z penceresi 500 | +20,5 (1,65) | +24,3 (1,57) |
| 25 bps maliyet | +13,1 (1,14) | +17,8 (1,16) |

**Veri madenciliği sayımı (kaynak ajan):**
- Tarama: 28.655 test. Bunların 360'ı "açılış-öncesi Asya → gün-içi" ailesi (72 sembol × 5 hisse).
- Backtest: 96 + 80 = 176 konfigürasyon. bt.csv'de OOS t>2 olan yalnız 5/96 satır var.
- Kompozit için mod seçimi yapılmış: işaret modu OOS −8,3 / −1,9, z-modu raporlanmış.
- Bileşenler FDR listesinden yarı-a-priori seçilmiş (çelik + makine + cevher). EREGL için 2. sıradaki Kawasaki Heavy (7012.T), KRDMD için 1. sıradaki dışarıda bırakılmış.

## 2. Seçim yanlılığı — ileriye yürüyen (walk-forward) dürüst seçim (s7)
Yöntem:
- Her yıl Y için yalnız 2014…Y−1 verisi kullanıldı.
- 72 açılış-öncesi Asya sembolünden, hedefin gün-içi getirisiyle en yüksek korelasyonlu k sembol seçildi.
- Y yılında işlem yapıldı. Maliyet 15 bps.

| Seçim | 2017–26 | 2021–26 | 2024–26 |
|---|---|---|---|
| EREGL, k=5 | +15,2 (1,60) | +19,3 (1,55) | +9,0 (0,52) |
| KRDMD, k=5 | +14,6 (1,50) | +15,8 (1,26) | +14,1 (0,89) |
| BRSAN, k=5 | +6,9 (0,61) | −0,6 | −0,8 |
| Havuz (EREGL+KRDMD) k=5 → EREGL / KRDMD | +16,0 (1,79) / +20,3 (1,93) | +24,2 / +25,8 | +21,8 / +23,9 (t 1,3–1,5) |
| Referans: sabit JP_AU, aynı pencere | +19,1 (2,29) / +26,8 (2,42) | | |

Değerlendirme:
- 15 konfigürasyonun **15'i de pozitif**, ama hiçbiri t>2 değil.
- Seçimin getiriyi şişirme payı ≈5–10 bps/işlem. Seçim etkiyi sıfırlamıyor, ancak anlamlılığı alıyor.
- Komatsu (6301.T) her yıl seçiliyor; 5411.T 2019'dan beri seçiliyor. Seçim istikrarlı.

## 3. Ortak faktör kontrolleri (s4, s9; NW t, kompozit katsayısı)
| Model | EREGL tam / IS / OOS | KRDMD tam / IS / OOS | BRSAN tam / OOS |
|---|---|---|---|
| Yalın | 4,51 / 3,51 / 2,90 | 4,51 / 3,00 / 3,40 | 3,77 / 2,58 |
| Açılışta bilinen tüm kontroller (1) | 2,95 / 2,47 / 1,82 | 3,14 / 2,09 / 2,44 | 1,75 / 1,40 |
| Aynı kontroller, geniş Asya hariç | 5,34 / 4,83 / 2,97 | 4,79 / 3,75 / 3,17 | 3,60 / 2,19 |
| + eş-zamanlı XU100 gün-içi_t (işlenemez; hisseye özgülük testi) | 3,87 / 2,60 / 3,35 | 4,26 / 2,61 / 3,50 | 3,44 / 2,60 |
| + eş-zamanlı XU100 ve XUSIN gün-içi_t | 2,22 / **0,88** / 2,44 | 3,23 / 1,54 / 2,97 | 2,81 / 2,15 |
| + defansif Asya ve geniş Asya z_t | 4,70 / 3,80 / 3,12; **2024–26: 0,81** | 4,61 / 3,17 / 3,50; **2024–26: 0,99** | 3,25 / 2,59 |

(1) Kontroller: kendi gap_t, XU100 gap_t, kendi gün-içi ve cc t−1, XU100 gün-içi t−1, SPY/EEM/ES/SLX/HG t−1, USDTRY (Yahoo ldate t = 00:00 UTC, açılış öncesi), N225/KS11/AXJO z_t.

Değerlendirme:
- Kontroller sonrası ilişki kalıyor, ancak tam kontrollü OOS t 1,8–2,4'e iniyor.
- EREGL'de IS dönemindeki etkinin tamamı sanayi endeksi (XUSIN) ile açıklanıyor. XUSIN EREGL'i de içerdiği için bu kısmen mekanik.
- **Yeni gözlem:** Defansif Asya sepetinin (Asahi, Kirin, NTT, TEPCO, KEPCO) bağımsız katsayısı negatif: OOS t −2,8 / −2,7. 2024–26'da çelik katsayısı anlamsız (t 0,8–1,0), defansif katsayısı ise anlamlı (−2,2).
  - Yorum: son dönemde sinyal kısmen "Asya döngüsel-defansif rotasyonu" gibi davranıyor.
  - Bu yeni bir veri-madenciliği adayı; doğrulanmadan işlenmemeli.

## 4. Plasebolar (s3)
**Bayatlatma** (NW t; backtest bps):
- lag1: korelasyon t 2,97 / 1,97, ama backtest IS −8,9 / −8,8, OOS +10 / +7 (t ≤ 0,9).
- lag2: OOS −8,6 / +5,6.
- lag3: OOS −25 / −18.
- Sonuç: işlem değeri aynı güne özgü.

**Dairesel kaydırma null'u (1000 çekiliş):**
- OOS medyan −15,5 / −14,9 bps (yani ≈ −maliyet), %95'lik dilim +3,7 / +7,8.
- Gözlenen +23,1 / +27,8 → p = 0,001 / <0,001.

**Rastgele işaret (2000 permütasyon):** p < 0,002.

**Başka hisseler (47 VİOP + endeksler, korelasyon t'si):**
- Sıralama: EREGL 4,62 > KRDMD 4,43 > KRDMA 4,30 > KRDMB 4,17 > BRSAN 3,95 > XUSIN 3,64 > AEFES 2,63 (OOS −0,4) > ISDMR 2,15.
- Bankalar, perakende ve diğerleri ≈0 veya negatif.
- **Sektöre özgülük güçlü.**

**Başka sepetler:**
| Sepet | Korelasyon t (EREGL / KRDMD / BRSAN) | OOS backtest |
|---|---|---|
| Ayrık çelik (POSCO, Hyundai Steel, RIO, CIA, MIN — iddiayla ortak bileşen yok) | 3,75 / 3,46 / 3,49; IS 2,6 / 2,2 / 2,9; OOS 2,7 / 2,7 / 2,3 | +4,4 (0,39) / +14,8 (1,26) / +19,1 (1,2) |
| Defansif | — | −36 / −43 (t −3,2) |
| Banka | — | ≈ −10 |
| Otomotiv / elektrik | — | ≈0 |
| Geniş endeks (N225, KS11, AXJO) | t < 1,9 | — |

- Ayrık çelik sepeti korelasyon düzeyinde **bağımsız bir replikasyon**. Ancak eşikli backtest zayıf.

## 5. Alt dönem istikrarı (s2, kendi kurgum, 15 bps, \|z\|>1; bps (t), r)
| Dönem | EREGL | KRDMD | BRSAN |
|---|---|---|---|
| 2014–17 | +17,2 (1,88), r 0,125 | +21,0 (1,54), r 0,102 | +16,0 (1,90) |
| 2018–20 | +6,3 (0,46), r 0,051 | +26,9 (1,49), r 0,054 | +2,5 (0,17) |
| 2021–23 | **+41,1 (2,44)**, r 0,129 | **+63,8 (2,78)**, r 0,135 | +53,2 (2,03) |
| 2024–26 | +4,2 (0,29), r 0,024 | **−10,8 (−0,62)**, r 0,047 | +22,6 (1,07) |

- 4 dönemin 2'si anlamlı.
- 2024–26'da long tarafı −18 / −50 bps, short tarafı +30 / +33 bps.
- Gün-içi drift'ten arındırınca sonuç değişmiyor (OOS +23,6 / +28,9).

## 6. Uç değer bağımlılığı (s2, OOS)
| Kırpma | EREGL | KRDMD |
|---|---|---|
| Yalnız en iyi 10 gün atılınca | +6,5 (0,64) | +7,7 (0,57) |
| Yalnız en iyi 20 gün atılınca | −5,2 | −7,1 |
| **Simetrik: en iyi 10 + en kötü 10** | **+19,4 (2,08)** | **+25,2 (2,00)** |
| Simetrik: en iyi 20 + en kötü 20 | +18,1 (2,09) | +23,4 (2,17) |
| %1–99 winsorize | +22,0 (1,97) | +25,7 (1,74) |

- Yalnız en iyi günleri atmak her düşük isabetli (%52–55) stratejiyi öldürür. Adil test simetrik kırpmadır ve onda sonuç ayakta kalıyor.
- Yani "uç değerlerle şişmiş" değil. Ama kenar ince.
- En iyi günler arasında kriz günleri var: 07.02.2023 deprem (XU100 −%8,5), 15.08.2018 kur krizi, 23.10.2026 fon krizi.

## 7. Açılış gerçekçiliği ve GERÇEK VİOP vadelisi (s5a–d, s6)
**VİOP bülteni (2017-03…2026-10, 2.424 gün).** Her gün en yüksek hacimli kontrat; açılış (ilk işlem, 09:30 TSİ) → kapanış (son işlem).

| \|z\|>1 | EREGL vadeli | KRDMD vadeli |
|---|---|---|
| 2017–26, 15 bps | **+33,7 (3,77)**, n 663 | **+46,7 (4,10)**, n 668 |
| 2017–26, tik bazlı maliyet (1 tik + 4 bps) | +38,0 (4,25) | +37,8 (3,32) |
| 2017–20 | +38,8 (2,88); medyan tik 11–13 bps | +57,9 (3,58); tik 25–48 bps → tik bazlı +31 (1,9) |
| 2021–23 | +55,6 (2,98) | +77,6 (3,32) |
| **2024–26** | **+9,6 (0,68)**; tik bazlı +17,8 (1,25) | **+0,1 (0,00)**; tik bazlı +7,8 (0,41) |
| Tokyo'nun 06:30 UTC kapanış dönemi (2024-11-05+) | +13,2 (0,74) | −9,0 (−0,40) |
| XU030 vadelisiyle hedge (geçmiş beta) 2017–26 | +12,5 (1,70) | +20,6 (2,19) |

Yıllık net (15 bps):
- EREGL: 2024 −0,3, 2025 +29,8, 2026 +5,3.
- KRDMD: 2024 +9,3, 2025 +22,2, 2026 **−28,1**.

**Uyarı — vadelideki fazla getirinin bir kısmı çelik dışı:**
- Kompozit, XU030 VADELİ açılış→kapanışını da öngörüyor: 2017–20 r 0,17 (t 3,5); 2021–23 t 2,6.
- Oysa XU030 SPOT gün-içinde etki yok (t 0,75 / 1,89).
- Vadelinin ilk işlemi (06:30 UTC), spot müzayededen (≈06:55 UTC) önce ve Asya kapanışını eksik yansıtıyor. ABD t−1 bilgisini ise yansıtıyor: SPY t−1 → vadeli o→c t ≈ −0,7…0,8.
- Yani fazla getirinin bir kısmı BIST genelinde vadeli açılışının ağırdan alması.
- 2017–19'da ilk işlemin büyük hacimle yapılabilirliği şüpheli: medyan günlük işlem sayısı EREGL'de 84–900, KRDMD'de 83–1.400.

Spot alternatif giriş (h1 ilk bar kapanışı ≈07:30 UTC = 10:30 TSİ), 2023-11…2026-10, 197 işlem, 15 bps net:

| Hisse | 07:30→kapanış | açılış→kapanış |
|---|---|---|
| EREGL | −3,3 (−0,26) | +8,2 |
| KRDMD | −10,9 (−0,65) | −6,4 |
| BRSAN | −9,5 | — |

- BRSAN'ın brüt kazancı açılış→07:30 arasında: +32 bps, korelasyon t 3,3.
- Günlük `o` ile h1 ilk bar açılışı %99,7–99,9 eşit.

**Likidite (VİOP bülteni, en hacimli kontrat, medyan):**
| Kontrat | Günlük hacim (milyon TL) | Tik |
|---|---|---|
| EREGL | 1,4 (2017) → 45 (2020) → 288 (2021) → 1.529 (2026) | 12,9 bps (2017) → 2–4 bps (2024–26) |
| KRDMD | 2,4 (2017) → 96 (2020) → 771 (2026) | 48 / 25 / 44 / 34 bps (2017–20), 13 (2021), 8 (2022), 2,5–4,4 (2023–26) |
| BRSAN | 63–323 (yalnız 2024+) | — |

- 2017–2020 IS benzeri dönemde KRDMD'de 15 bps maliyet gerçekçi değil.

## 8. 1. aşamayla farklarım
1. **Dürüst seçim.** 1. aşama yalnız-IS seçimiyle EREGL OOS +3,9 (t 0,35) buldu. Bu tek bölmeli ve gürültülü bir test. Walk-forward seçim 2017–26'da +15 (t 1,6), havuzda +16…20 (t 1,8–1,9) veriyor ve 15/15 konfigürasyon pozitif. Seçim yanlılığı getiriyi kesiyor ama sıfırlamıyor.
2. **Yoğunlaşma.** "%71–81 en iyi 10 günden" metriği asimetrik. Simetrik kırpmada OOS t ≈2,0–2,2 kalıyor.
3. **Kurgu duyarlılığı (1. aşama farkedilmedi).** Raporlanan rakamlar ffill hizalamaya bağlı. Kendi-takvim hizalamasında OOS t 2,00 / 1,82.
4. **VİOP vadeli (yeni).** Vadeli o→c'de etki daha güçlü (t 3,8–4,1), ama bir kısmı genel vadeli açılış gecikmesi (XU030 vadelisi de etkileniyor). Hedge'li hali t 1,7–2,2. 2024–26'da ≈0.
5. **Mekanizma desteği (yeni).** Kompozit Avrupa çelik gün-içini de öngörüyor: VOE.VI r 0,12 (t 4,4; OOS 2,35), SZG.DE t 3,3, SSAB t 3,5 (OOS 0,57). ABD çeliğinde etki yok. Bu, küresel çelik fiyatlamasında Asya bilgisinin yavaş yayılmasıyla tutarlı. OOS'ta Avrupa'da da sönüyor; arbitraj ediliyor olabilir.
6. **FMG.AX tek başına** (önceden belirlenmiş hipotez) en istikrarlı parça:
   - KRDMD r 0,081 (t 4,1; IS 2,3; OOS 3,9; 2024–26 r 0,098, t 2,9).
   - EREGL t 3,9 (2024–26: 1,97); BRSAN t 4,3 (2024–26: 2,3).
   - Ancak \|z\|>1 backtest'i KRDMD OOS +23,5 (t 1,67), IS +7.

## 9. Sonuç
- **İlişki:** Japon çelik/makine ve Avustralya cevher hisselerinin aynı günkü (BIST açılışından önce bilinen) getirisi, BIST çelik hisselerinin gün-içi getirisiyle r ≈ 0,07–0,09. İlişki sektöre özgü, kontrollere dayanıklı, ayrık sepetle ve Avrupa çeliğinde tekrarlanıyor → **ORTA**.
- **İşlem iddiası:** "OOS +27,7 / +32,1 bps/işlem, 15 bps" şişkin. Dürüst seçim ve alternatif kurguyla ≈ +15…23 bps, t 1,5–2,0. 2024–26 spotta +4 / −11, vadelide ≈0…+10. 10:30 TSİ girişinde negatif → **DÜŞÜK**.
- **Uygulanabilir tek biçim:** VİOP EREGL/KRDMD vadelisi, XU030 vadelisiyle hedge'li, otomatik emir (06:30 UTC civarı). 2024–26'da kanıt yok. Bağımsız strateji olarak önermiyorum; en fazla küçük boyutlu, ileriye dönük (paper) izleme.
