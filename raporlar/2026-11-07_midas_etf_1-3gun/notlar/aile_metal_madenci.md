# Aile: metal_madenci — 1-3 günlük işlem araştırması (07.11.2026)

28 ETF: GLD, IAU, GLDM, SLV, SIVR, PPLT, PALL, CPER, DBB, UGL, GLL, AGQ, ZSL, GDX, GDXJ, NUGT, DUST, JNUG, JDST, SIL, SILJ, RING, COPX, XME, URA, URNM, LIT, REMX.
Kod: `kod/ajan_metal_madenci/` · Tablolar: `sonuclar/aile_metal_madenci/` · JSON: `sonuclar/aile_metal_madenci/sonuc.json`.

## Kısa sonuç

- **Kesin bir strateji yok.** 10.049 test yapıldı (genel_tum'un aile satırları 8.316 + kendi testlerim 1.733). Tek yönlü BH-FDR'de (q=0,10, "net > 0") hiçbir strateji geçmiyor. Geçen 7 test yalnız ölçüm: madencilerdeki gece getirisi ve DBB←KWEB regresyonu.
- **Aile havuz testinde de (aynı gündeki işlemler tek olay sayıldı) hiçbir kural t ≥ 2,5'e ulaşmıyor.**
- Tek ETF eşik ölçütlerini geçen 5 aday var:
  - **S3 GDXJ IBS dip alımı** → "orta". n=240, net 107 bp, t 3,39. IS ve OOS pozitif, O1'de t 2,74. İki yönlü BH'de geçiyor.
  - **S1 GDX ay sonu** ve **S2 GLD ay sonu** → "düşük". t 2,20 / 2,45. FDR'yi geçmiyor, boğa yıllarına bağımlı, kısmen kapanışa bağlı.
  - **S4 GLD IBS** → "düşük". t 2,07, kopya ETF'lerde zayıf.
  - **S5 SILJ Bollinger (C1)** → "düşük". n=48, seçim yanlılığı yüksek.
- Yönlendirmedeki hipotezlerin çoğu maliyet düşülünce çalışmıyor: madencilerin GLD'ye yetişmesi, SIL←SLV, altın/gümüş oranı, GVZ, reel faiz + dolar, tatil öncesi, VIX backwardation. **FOMC sonrası altın beklenenin tersine zayıf** (anlamlı değil).
- **Lead-lag:** ailede ekonomik olarak kullanılabilir, doğrulanmış gecikmeli öncü yok. COMEX:GC1! / SI1! / HG1! gece işlediği için gerçek zamanlı izleme aracıdır, öncü değildir.
- **Uygulama için önemli:** altın, gümüş ve madencilerde getirinin neredeyse tamamı gece oluşuyor (kapanıştan açılışa). Gün içi getiri sıfıra yakın ya da negatif. Bu yüzden girişleri kapanışta (C0) yapmak açılışa (O1) göre belirgin avantajlı.

## Yöntem

- **Zamanlama:** `kod/lib.py`'deki sözleşme aynen uygulandı. Sinyal t kapanışına kadarki bilgiyle hesaplanır. C0 = t kapanışında giriş, O1 = t+1 açılışında, C1 = t+1 kapanışında. Çıkış girişten h gün sonraki kapanış. İşlemler çakışmaz.
- **Maliyet:** 2 × 1,5 USD komisyon / pozisyon + kademeli makas tahmini (`lib.spread_bp_tier`). Ana sonuçlar 2.500 $ içindir; 1.000 $ ve 10.000 $ duyarlılığı da verildi. Kodda: `mm.full`.
- **Aile havuz testi (`mm.pooled`):** Her ETF'de çakışmayan işlemler alınır. Aynı sinyal günündeki işlemler ortalanıp tek olay sayılır; olay serisinin t'si Newey-West (gecikme = h) ile hesaplanır. Kullanılan havuzlar:
  - **REP12:** her kümeden bir temsilci (GLD, SLV, PPLT, PALL, CPER, GDX, SIL, COPX, XME, URA, LIT, REMX).
  - **MADENCI5:** GDX, GDXJ, RING, SIL, SILJ. Son 1 yılda birbirleriyle korelasyonları 0,96-0,99; pratikte tek kümedir.
  - **METAL5:** GLD, SLV, PPLT, PALL, CPER.
- **Ek sağlamlık kontrolleri:**
  - Yıl ortalaması çıkarılmış kenar: boğa trendinin etkisini ayıklar.
  - En iyi yıl hariç sonuç.
  - 26.01-13.02.2026 gümüş şoku penceresi hariç sonuç.
  - Kopya ETF'lerde aynı kural.
  - Kaldıraçlı ürünle uygulama.
- **Parametre taraması yapılmadı.** Eşikler hipotez dosyasından ya da literatür varsayılanından alındı: IBS < 0,10, artık ≤ −1,5 sd, z20 ±2, GVZ +%15, FOMC D..D+3. Komşu h değerleri raporlandı.
- **FDR (`t6_fdr.py`):** Tüm testler tek havuzda BH q=0,10 ile değerlendirildi, iki sürümle:
  - İki yönlü p (`lib.bh_fdr`): eşik p ≤ 0,0045. Maliyet yüzünden anlamlı negatif çıkan yüzlerce test bu eşiği gevşetiyor.
  - Tek yönlü p (H1: net > 0): eşik p ≤ 6,7e-5. "İşe yarar mı?" sorusu için doğru sürüm budur.
- **Ek veri düzeltmesi (yalnız `mm.load`'da; lib'e dokunulmadı):** IAU 2021-03-08 barı hatalı ve atıldı. O gün IAU 35,12 (+%8,5) iken GLD ve GLDM −%1; ertesi gün tam geri dönüş var. Bu bar leadlag_sweep'te sahte bir "IAU←GLD yetişme" (t 2,29) üretiyor; bar atılınca t −0,43.
- **Direxion kaldıraç değişimi:** NUGT, DUST, JNUG ve JDST 2020-Q1'e kadar 3x, 2020-Q2'den beri 2x (çeyreklik beta 2,9 → 1,9). Kaldıraç kaybı ölçümü yalnız 2x döneminde yapıldı.

| Betik | İçerik | Test |
|---|---|---|
| t1_islenebilirlik.py | tarama.csv süzümü, kopya korelasyonları, yapı (PTP) | — |
| t2_genel_aile.py | 297 genel kombinasyon, aile havuzu + SPY karşılaştırması | 297 |
| t3_hipotez.py | H01-H14 (ay sonu, tatil, IBS, VIX, artık yetişme, oran, GVZ, reel faiz, FOMC, Çin, URA) | 1.253 |
| t3b_gece.py | MM01 gece / gün içi | 42 |
| t3c_kaldirac.py | MM06 kaldıraç sapması (ölçüm) | — |
| t4_leadlag.py (+`--breakeven`, `--gdxoncu`) | sweep süzümü, kendi gecikmesi kontrollü regresyonlar, 3 öncü kuralı | 81+36+24 |
| t5_adaylar.py | aday stratejilerin tam raporu (tekrar üretim betiği) | (tekrar) |
| t6_fdr.py | toplam test sayısı ve BH-FDR | — |
| t7_sonuc_json.py | sonuc.json | — |

Çalıştırma sırası (python3 -I, tek süreç): t1 → t2 → t3 → t3b → t3c → t4 → `t4 --breakeven` → `t4 --gdxoncu` → t5 → t6 → t7. Toplam süre ~1 dk.

## 1) İşlenebilirlik ve kopya grupları (`islenebilirlik.csv`, `kopya_korelasyon.csv`)

| Küme | ETF (medyan $ hacim, gidiş-dönüş maliyet, 1g oynaklık) | Not |
|---|---|---|
| Altın | **GLD** (3.739 mn, 13 bp, 182 bp) · IAU (535, 14) · GLDM (427, 14) · UGL 2x (147, 16) · GLL −2x (60, 16) | GLD/IAU/GLDM korelasyonu 0,998-0,999: kopya. UGL/GLL ProShares Trust II = **PTP/K-1** |
| Gümüş | **SLV** (1.376, 14, 398) · SIVR (123, 16) · AGQ 2x (306, 14) · ZSL −2x (105, 16) | SLV/SIVR 0,999. AGQ/ZSL **PTP/K-1**. 30.01.2026: SLV −%28,5, AGQ −%60 |
| Platin / paladyum | PPLT (44, 20, 320) · PALL (26,5, 20, 316) | fiziki trust |
| Bakır / baz metal | CPER (20,8, 20, 179; maliyet/oynaklık 0,11) · DBB (5,9, 27, 123; 0,22) | Emtia havuzu: **PTP/K-1 olasılığı yüksek** (yapıdan çıkarım; Midas'ta doğrulanmadı) |
| Altın madencileri | **GDX** (1.910, 13, 322) · **GDXJ** (563, 14, 356) · RING (30, 20) · NUGT 2x (110, 16) · JNUG 2x (48, 20) · DUST/JDST ters | GDX-RING 0,995, GDX-GDXJ 0,99 (1y) |
| Gümüş madencileri | SIL (135, 16, 350) · SILJ (139, 16, 378) | GDX-SIL 0,97 (1y): madencilerin hepsi aynı küme |
| Bakır madencileri / metal-madencilik | **COPX** (239, 14, 302) · XME (226, 14, 238) | COPX-XME 0,81 |
| Uranyum | URA (171, 16, 321) · URNM (34, 20) | 0,95-0,96 |
| Lityum / nadir toprak | LIT (17,9, 20, 191; maliyet/oynaklık 0,105) · REMX (68, 16, 290) | |

1-3 günlük hareket, likit ETF'lerde maliyeti rahatça karşılıyor: maliyet/oynaklık oranı GLD'de 0,07, GDX'te 0,04, SLV'de 0,035. Bu oran DBB (0,22), CPER (0,11) ve LIT (0,105) için zayıf.

## 2) Genel kütüphane aile içinde (`genel_aile_havuz.csv`, `genel_aile_satirlar.csv`)

- 297 kombinasyonun tamamı REP12 havuzunda test edildi (seçim yanlılığı olmasın diye). **Pozitif net ve FDR'de anlamlı tek kombinasyon yok.** FDR'de anlamlı çıkan 32 kombinasyonun hepsi negatif (maliyet yüzünden).
- En iyi kombinasyonlar:
  - CA_ay_sonu C0 h2 / h3: t 1,69 / 1,67; IS t ~2,0-2,1, OOS t ~0,55.
  - MO_3gun_yukselis C0 h3: t 1,49.
- Tek ETF'te öne çıkanlar:
  - GDXJ MR_ibs_lt01_dusus C0 h3: t 3,39.
  - SILJ MR_bb20_alt C1 h3: t 3,10.

  İkisi de genel_tum'un küresel (iki yönlü) FDR'sini geçiyor, ama havuzda zayıflar (sırasıyla t 0,61 ve 0,93). Etki madenci (ve altın) kümesine özgü.

## 3) Aileye özel hipotezler (`hipotez_etf.csv`, `hipotez_havuz.csv`, `hipotez_yillik.csv`)

**H01 Ay sonu** (son işlem günü kapanışı → yeni ayın h. günü):
- Madenci havuzunda C0 h1 net 55 bp (t 2,10), h3 net 72,5 bp (t 1,83).
- REP12 havuzunda C0 h3 t 1,67; METAL5'te t 0,80.
- Tek ETF, C0 h3: GDX 2,20 · GDXJ 1,98 · RING 2,25 · XME 2,33 · GLD 2,45 (IAU 2,45, GLDM 2,58) · UGL 2,38 · NUGT 2,19.
- Baz metallerde negatif: CPER 0,05 · DBB −1,0 · PALL −0,6. SPY'de zayıf (t 1,11).
- **Yıl bağımlılığı:** GDX'te 2020, 2025 ve 2026 çıkarılınca net 16 bp (t 0,42). Yıl ortalaması çıkarılmış kenar t 1,92 (GDX) ve 2,28 (GLD).
- **Mod bağımlılığı:** O1/C1'de net pozitif ama t 1,2-1,4. Etkinin yarısı ay başının ilk gecesinde.
- 30.01.2026 bir ay sonu günüydü (C0 girişi çöküşten sonra kapanışta); bu dönem hariç tutulunca sonuç değişmiyor (GDX 81 bp).

**H02 Tatil öncesi:** havuzda negatif ya da sıfır (REP12 C0 h1 −8 bp; madenciler O1/C1 negatif). **Reddedildi.**

**H03 IBS < 0,1 ve düşüş:**
- Madenci havuzu C0 h3: net 54 bp, t 2,49. IS 14 bp (t 0,51), OOS 113 bp (t 3,45).
- Madenciler, C0 h3: GDXJ 3,39 (IS 85 / OOS 128) · SIL 2,22 (IS 35) · GDX 2,14 (IS **−2,6**) · RING 2,03 (IS −11) · SILJ 1,28 (IS −50).
- Altın: GLD 2,07 (IAU 0,98, GLDM 1,60).
- Gümüş, PGM, uranyum ve REMX'te sıfır ya da negatif.
- Getiri 2024-2026 boğa yıllarında yoğun; IS dönemi geniş madenci kümesinde zayıf.

**H04 VIX backwardation dönüşü:** madenci havuzu C0 h2 net 85 bp (t 1,65, n=55), h3'te negatif. **Eşik altı.**

**H06 (MM02) madencilerin metale gecikmeli yetişmesi:**
- GDX/GDXJ/RING ← GLD, SIL/SILJ ← SLV, COPX ← CPER: tek ETF t ≤ 1,19; madenci havuzu t ≤ 0,94; COPX negatif.
- Kontrol (kendi düşüşü z < −1,5) de sıfır ya da negatif.
- **Kısa vadeli yetişme yok.**

**H07 Altın/gümüş oranı z20 ±2:** çalışmıyor (SLV t ≤ 0,02; GLD bazı modlarda t −3,7).

**H08 GVZ sıçrama / gerilme:** havuz t ≤ 1,07; işaret moda göre değişiyor.

**H09 (MM03) reel faiz + dolar:**
- G3 havuzu (GLD/SLV/GDX) C0 h3 net −27 bp: işaret ters.
- DFII10 günlük ±5 bp (O1/C1) anlamsız.
- UUP düşüşü sonrası GLD negatif (t −1,8).
- 2022 sonrası reel faiz–altın ilişkisinin kopmasıyla uyumlu (IS'te gecikmeli t −3,9, OOS'ta +1,0).

**H10 (MM04) FOMC:**
- Sonrası (C_D → C_D+3): G3 C0 h3 net **−69 bp** (t −1,6); 30.01.2026 hariç −44 bp.
- Öncesi (D−3 → D, D−1 → D) anlamsız.
- **Reddedildi**, işaret ters. Kısa yön için de anlamlı değil.

**H11 (MM05) GLD RSI(2):** GLD C0 net −5 bp (IS −31). **Reddedildi.**

**H05 (MM01) Gece / gün içi** (`gece_gunici.csv`):

| | gece bp/gün (t) | gün içi bp/gün (t) |
|---|---|---|
| GLD | +5,1 (3,20) | −0,6 (−0,48) |
| SLV | +6,6 (2,06) | −2,7 (−1,07) |
| GDX | +6,5 (2,20) | −1,4 (−0,36) |
| GDXJ | +9,1 (2,73) | −5,1 |
| SIL | +11,3 (3,59) | −8,7 (−2,18) |
| SILJ | +17,5 (4,86) | −15,3 (−3,24) |
| COPX | +11,9 (4,04) | −6,6 |
| URA | +12,1 (4,65) | −8,1 |

- IS ve OOS'ta aynı işaret. Gece getirisinin yılların %73-100'ü pozitif.
- "Kapanışta al, açılışta sat" her gün maliyeti karşılamıyor (GLD net −7,9 bp).
- **Uygulama sonucu:** girişler C0'da, çıkışlar kapanışta yapılmalı; açılışta alım gece primini kaçırır.
- Uyarı (literatür): resmî açılış fiyatı, gerçekte alınabilecek fiyattan iyimser olabilir (Quantpedia, GDX).

**H12 (MM06) kaldıraç kaybı** (`kaldirac_sapma.csv`, yalnız 2x dönemi):
- 3 günlük ortalama sapma: UGL −6,2 bp, AGQ −6,7, NUGT −5,0, JNUG −6,2 bp. Formül öngörüsü −3..−22 bp.
- Ters ürünlerde sapma ≈ 0 ya da pozitif (ortalamaya dönüş).
- 1-3 günde kayıp küçük. Asıl risk tek işlem kaybının ve maxDD'nin yaklaşık iki katına çıkması.

**H13 Çin → baz metal:** KWEB/FXI z > 1 → DBB/CPER/COPX kuralları net negatif.

**H14 SPY büyük düşüşü → URA:** t ≤ 1,5.

## 4) Lead-lag (`leadlag_aile.csv`, `leadlag_suruculer.csv`, `leadlag_ek_regresyon.csv`)

- **leadlag_sweep'te ailede FDR + IS/OOS aynı işaret ölçütünü geçen tek çift: DBB ← KWEB** (lag h1 t 4,05; IS 2,45 / OOS 3,20). Ama 1 sd KWEB hareketine düşen etki ~10 bp, DBB maliyeti 27 bp'nin altında. Kural testi de negatif. Yani istatistiksel olarak geçerli, ekonomik olarak kullanılamaz.
- **GDX ← GLD yetişmesi yok:**
  - Kontrolsüz catch t 0,56; kendi gecikmesi kontrol edilince 0,11. IS 0,53 / OOS −0,93; h3'te −0,15.
  - GDXJ, RING, NUGT, JNUG ← GLD ve SIL/SILJ ← SLV de sıfır ya da negatif.
  - Yetişme testindeki küçük pozitiflik tamamen kendi ortalamaya dönüşünden geliyor.
- **FDR'siz ama IS/OOS işareti tutarlı bulgular** (kurala çevrildi, hepsi maliyet sonrası anlamsız):
  - **GLD ← GDX:** t 2,40; 11 bp/sd. Kural C0 h3 t 1,29.
  - **Başabaş enflasyon (T10YIE) → SLV/GLD:** t 3,39 / 2,76. Veri kapanıştan sonra geldiği için O1/C1'de işlem yapılabiliyor ve orada negatif.
  - **GDX → COPX (h3):** t 2,63. Kural t 1,27, O1 negatif.
  - **GDX → PPLT (h1):** t 3,04. Uzun yönlü kural t 0,43. Yalnız GDX'in sert düştüğü günün ertesinde PPLT/COPX zayıf (PPLT O1 h1 net −40 bp, t −3,55); bu, "o gün alma" filtresi olarak kullanılabilir.
- **Eşzamanlı sürücüler** (öncü değil; son 1 yıl):

  | ETF | Sürücü: korelasyon (beta) |
  |---|---|
  | GLD | GDX 0,86 (0,49) · SLV 0,84 (0,37) · UUP −0,42 (−1,82) · DFII10 değişimi −0,22 |
  | SLV | GLD 0,84 (1,92) · GDX 0,81 · CPER 0,69 |
  | GDX | GLD 0,86 (1,53) · SLV 0,81 · UUP −0,44 |
  | COPX | CPER 0,82 (1,39) · GDX 0,80 · EEM 0,75 |
  | XME | GDX 0,75 · IWM 0,72 |
  | URA | EEM 0,69 · IWM 0,69 · SMH 0,67 (SPY betası 2,4) |

- **Gerçek zamanlı izlenecekler** (ETF kapalıyken işler; açılış boşluğunu gösterir):
  - Altın: COMEX:GC1!, OANDA:XAUUSD.
  - Gümüş: COMEX:SI1!, OANDA:XAGUSD.
  - Bakır: COMEX:HG1!.
  - Platin / paladyum: NYMEX:PL1! / NYMEX:PA1!.
  - Dolar ve faiz: TVC:DXY, CBOT:ZN1! (veya TVC:US10Y).
  - Hisse riski ve Çin: CME_MINI:ES1!, HKEX:HSI1!, FX_IDC:USDCNH.
  - Uranyum için doğrulanmış gerçek zamanlı kod yok. TSX:U.UN ve NYSE:CCJ doğrulanmadı; `tv_dogrulanacak` listesinde.

## 5) Aday stratejiler (tekrar üretim: `python3 -I kod/ajan_metal_madenci/t5_adaylar.py`)

| id | kural | n | brüt / net bp | t | IS / OOS net | yıl+ | maxDD | en kötü | FDR (tek / iki yönlü) | güven |
|---|---|---|---|---|---|---|---|---|---|---|
| S3 | GDXJ IBS < 0,10 ve close < close[1] → C0, 3 gün | 240 | 121 / 107 | 3,39 | 85 / 128 | 0,8 | −%26 | −855 | yok / var | **orta** |
| S1 | ayın son işlem günü kapanışı → 3. gün kapanışı, GDX | 111 | 98 / 85 | 2,20 | 82 / 87 | 0,9 | −%20 | −873 | yok / yok | düşük |
| S2 | aynı takvim kuralı, GLD | 111 | 53 / 40 | 2,45 | 34 / 45 | 0,7 | −%8 | −388 | yok / yok | düşük |
| S4 | S3 kuralı GLD'de | 140 | 52 / 39 | 2,07 | 55 / 27 | 0,7 | −%13 | −928 | yok / yok | düşük |
| S5 | SILJ close < SMA20 − 2·sd20 → C1, 3 gün | 48 | 209 / 193 | 3,10 | 189 / 195 | 0,9 | −%13 | −619 | yok / var | düşük |

**Mod sağlamlığı** (net bp / t):

| | C0 | O1 | C1 |
|---|---|---|---|
| S3 | 107 / 3,39 | 72 / 2,74 | 31 / 0,93 |
| S1 | 85 / 2,20 | 45 / 1,23 | 52 / 1,36 |
| S2 | 40 / 2,45 | 19 / 1,19 | 24 / 1,30 |
| S4 | 39 / 2,07 | 23 / 1,43 | 18 / 1,06 |
| S5 | 76 / 1,03 | 130 / 2,03 | 193 / 3,10 |

**Maliyet duyarlılığı** (1.000 $ / 10.000 $ net bp): S3 89 / 116 · S1 67 / 94 · S2 22 / 49 · S4 21 / 48 · S5 175 / 202.

**Kaldıraçlı uygulama:**
- S1 → NUGT: net 188 bp, t 2,19, maxDD −%37.
- S3 → JNUG: net 173 bp, t 2,70, maxDD −%51, en kötü işlem −%21.
- S2 → UGL: net 79 bp, t 2,38. UGL PTP olduğu için önerilmez.

**S3 için ek kontroller:**
- Yıl ortalaması çıkarılmış kenar 98 bp (t 3,14).
- En iyi yıl (2020) hariç t 2,76.
- Komşu h: h1 t 2,81, h2 t 2,48.
- Şok penceresi hariç 102 bp.
- **Uyarı:** genel taramanın en iyileri arasından geldi; geniş madenci havuzunda IS zayıf.

**Pratik uygulama (TR saati):**
- **C0 girişi:** kış saatinde (1 Kas 2026 - 14 Mar 2027) TR ~23:45-23:59, yaz saatinde ~22:45-22:59. Anlık fiyatla sinyali kontrol edip piyasa emri ya da son fiyatın biraz üstüne limit emir verin. Midas'ta MOC/LOC yok.
- **O1 alternatifi:** TR 17:30 (kış) / 16:30 (yaz).
- **Uzatılmış saatler:** yalnız limit emir.
- **S1/S2 sonraki tarihler:** 30.11.2026 (çıkış 03.12), 31.12.2026 (çıkış 06.01.2027), 29.01.2027 (çıkış 03.02.2027).
- S1 ile S2 aynı etkidir; ikisini birlikte açmak riski ikiye katlar.

## 6) İzleme listesi

| Karar | ETF |
|---|---|
| **Kabul** | GLD, GDX, SLV, GDXJ, COPX |
| **Yedek** | IAU, GLDM (GLD kopyaları) · SIVR (SLV kopyası) · NUGT, JNUG (kaldıraçlı uygulama; PTP değil, Midas'ta bulunurluk doğrulanmadı) · SIL, SILJ (madenci kümesi) · XME · URA · PPLT |
| **Red** | UGL, GLL, AGQ, ZSL (PTP/K-1, %10 brüt stopaj riski) · CPER, DBB (PTP olasılığı, düşük likidite / yüksek maliyet oranı) · RING (GDX kopyası, daha pahalı) · DUST, JDST (kısa yön sinyali yok) · URNM (URA kopyası) · PALL, LIT, REMX (strateji yok, sürücü zayıf ya da likidite sınırda) |

## 7) Elenenler

Tam liste `sonuc.json` → `elenen` alanında. Özet: genel kütüphanenin aile havuzu, tatil öncesi, VIX backwardation, MM02 yetişme, MM03, DFII10/UUP, FOMC (MM04), MM05, altın/gümüş oranı, GVZ, gece primi işlemi, T10YIE, Çin → baz metal, SPY → URA, GLD ← GDX, GDX → PPLT/COPX, baz metalde ay sonu.

## 8) Sınırlamalar

- **10 yıllık örneklem güçlü bir altın boğa piyasası içeriyor** (GLD ~3 kat). Uzun yönlü dip alımı ve ay sonu kuralları bundan yararlanıyor. Yıl ortalaması çıkarılmış kenar bunu kısmen ayıklıyor ama rejim değişikliği riski yüksek.
- **Örneklem küçük:** ay sonunda n=111; S5'te n=48.
- **Madenciler tek küme** (1y korelasyon 0,96-0,99). GDX, GDXJ, SIL, SILJ ve RING'deki sonuçlar bağımsız kanıt değildir. Kopya ETF'ler de (GLD/IAU/GLDM, SLV/SIVR) öyle.
- **C0 girişinde iki varsayım var:** kapanış fiyatından alınabildiği ve sinyalin son dakikalardaki fiyatla doğru hesaplandığı. IBS bu nedenle kapanışa duyarlıdır. Midas'ta MOC olmadığından gerçekte kapanış öncesi birkaç dakikalık kayma beklenmeli. Açılış fiyatı ölçüm sorunu da var.
- **Makas modeli kaba:** `spread_bp_tier`. BSMV ve döviz makası dahil değil.
- **Hazine faiz verisi** ~15:30 ET kotasyonlarına dayanıyor ve kapanıştan sonra yayımlanıyor. Bu yüzden C0'da kullanılamaz; testlerde t−1 ya da O1/C1 kullanıldı.
- **Midas bulunurluğu:** kaldıraçlı/ters ürünlerin Midas'ta bulunurluğu resmî olarak doğrulanamadı. PTP etiketi her işlemden önce uygulamada kontrol edilmeli. ProShares Trust II (26.02.2026) ve USCF (31.07.2026) 1446(f) "10% istisna" bildirimi yayımladı, ama 2024'te UNG'de geçici %10 kesinti bildirildi.
- **30.01.2026 gümüş çöküşü** gerçek bir olaydır. Aday stratejiler bu pencere hariç tutulunca değişmiyor. Gümüş ve kaldıraçlı gümüşte (AGQ −%60) tek gün kuyruk riskini gösteriyor.
