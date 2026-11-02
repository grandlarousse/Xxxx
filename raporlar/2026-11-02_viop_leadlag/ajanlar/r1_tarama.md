# r1_tarama — Sistematik kaba kuvvet tarama (47 VİOP hissesi × 1.024 BIST-dışı sürücü)
Ajan: tarama · Veri: panel_ret_bistcal / panel_decomp_bist (14:38–14:39 UTC sürümü: FX 1 gün kayma düzeltmesi + simetrik ±%10,5 temizliği dahil) · Dönem 02.01.2014–30.10.2026 · IS 2014–2020 / OOS 2021–2026 / 3y 31.10.2023+ / son 1y 31.10.2025+

## 1. Net bulgular

| # | Bulgu | Rakam | Güven |
|---|---|---|---|
| 1 | **Pay bazında işlenebilir öncülük FDR'den geçmiyor.** ABD/Avrupa sürücüsü_{t-1} → BIST gün-içi_t (intra_l1) ve sürücü lag 2–5 toplamı → cc_t (cum25): 2 × 48.124 testte **0** çift BH q<0,05 | p<0,05 sayısı 3.445 / 3.229; null ortalaması 2.369–2.638 → ≈%2'lik dağınık fazlalık, tek tek ayırt edilemiyor. IS top-200'ün OOS replikasyonu %5 (null %2–3) | (olumsuz) YÜKSEK |
| 2 | IS'de en iyi 10 öncülük adayının (IS \|t\| 3,8–4,8) hiçbiri OOS'ta tutmadı | 15 bps OOS Sharpe medyan −0,81 (en iyi −0,04); 8 bps medyan −0,35 (en iyi +0,30); hiçbirinde OOS t>2 yok | (olumsuz) YÜKSEK |
| 3 | ABD kapanışı BIST'e **açılış gap'inde** geçiyor, gün-içinde değil (eşzamansız kapanış) | XU100 gap_t ~ ^GSPC_{t-1} r=0,18, TUR 0,20, ^VIX −0,20; intra_t ~ ^GSPC_{t-1} r=−0,02. ABD-8 lag1 R²: gap 0,057, gün-içi 0,006 | YÜKSEK (işlenemez) |
| 4 | XU030'u ABD lag1 sinyaliyle gün-içi işlemek zarar ettiriyor | ^GSPC/ES=F/TUR/EEM/^VIX: 8 bps OOS Sharpe −0,30…−0,78; 15 bps −0,93…−1,41 | (olumsuz) YÜKSEK |
| 5 | **Tek umut verici zayıf öncülük: Asya (Kore) lag1 → BIST gün-içi** | XU030 intra_t ~ ^KS11_{t-1} r=0,071 (t=3,6; IS 0,075 / OOS 0,071 / 1y 0,16; 13 yılın 11'inde +); BIST'in kendi gecikmeleri + ABD lag1-2 kontrollü t=2,9. Kova içi FDR: Kore/Tayvan → THYAO, KCHOL, SISE, PGSUS… 10 çift. Backtest XU030 z>1: 8 bps OOS Sharpe 0,62 (t=1,3), 4 bps 0,82 (t=1,75); sign modu maliyet sonrası negatif | DÜŞÜK |
| 6 | Türkiye'nin küresel betası rejime bağlı: 2021–2025'te çöktü, 2026'da geri döndü | USD bazlı XU100 Dimson β(EEM): 2014–17 0,85 → 2022–May23 0,41 → 2023 yılı 0,15 → Mar–Ara 2025 0,17 → 2026 Oca–Ağu 0,60 → Eyl–Eki 2026 fon krizi 0,76 (n=43). Senkron R² (10 makro): 0,26 → 0,05–0,09 → 0,30 | ORTA (son pencere kısa) |
| 7 | En sağlam hisseye özgü küme (10 küresel faktör sonrası FDR + IS/OOS replike = 162 çift) sektör emsallerinden oluşuyor (%78'i sektör emsali) | THYAO 30, TUPRS 27, PGSUS 22, KRDMD 17, TAVHL 17, EREGL 15, AEFES 8, TRALT 7 çift; diğer 39 hissenin çoğunda 0–1 | YÜKSEK |
| 8 | THYAO/PGSUS/TAVHL ← Avrupa havayolları + havalimanları | THYAO–LHA.DE pc=0,21 (IS 0,18/OOS 0,24); PGSUS–EZJ.L 0,18; TAVHL–FRA.DE/ADP.PA 0,15 | YÜKSEK |
| 9 | TUPRS ← petrol/rafineri; TRALT ← altın | TUPRS–EQNR.OL 0,19, CRAK 0,18, BZ=F 0,17 (IS 0,10 → OOS 0,26); TRALT–GC=F 0,19 (IS=OOS), FRES.L 0,17 | YÜKSEK |
| 10 | EREGL/KRDMD ← Avrupa çeliği + demir cevheri; TOASO/FROTO ← VW/Porsche; AEFES ← CCH/Carlsberg; bankalar ← petrol (−) | EREGL–SSAB 0,12 (OOS 0,16); TOASO–VOW3 0,11; AEFES–CCH.L 0,10; AKBNK–BZ=F −0,07 | ORTA |
| 11 | Zamanlama sağlık kontrolü ham veride Yahoo '=X' kurlarının 1 gün geç etiketlendiğini yakaladı (VAKBN_t → TRY=X_{t+1} r=−0,21, t=−10,7; saatlik veriyle günlük "kapanış" = t günü 00:00 UTC) | Düzeltmeden sonra us/eu kovasında 'ters yön' kova-içi FDR geçişi 693 → 4. Kalan 28 bayrak \|r\|<0,07 (gürültü) | YÜKSEK |

## 2. Yöntem
- **Evren:** 47 VİOP hissesi (+ XU100/XU030/XBANK bilgi satırı, FDR dışı) × panelde verisi olan 1.024 BIST-dışı sembol. Seyrek bayrağı: 2014+ zero_frac>0,3 veya n<1000; TR-ayna bayrağı: TUR, TKC, AKBTY, TKGBY, YKBNY, TYIDY, TRY=X, EURTRY=X, GBPTRY=X… Katalogda grubu '?' olan 141 yeni sembol ad bazında yeniden gruplandı (tlib.regroup).
- **Aileler** (her biri ayrı test ailesi; pencere tam/IS/OOS/3y/1y): sync; sync_usd (cc−USDTRY); pc_xu (XU100 kontrollü kısmi); pc_xt (XU100+USDTRY); pc_glob (XU100, USDTRY, EEM, ^GSPC, ^STOXX50E, BZ=F, GC=F, HG=F, DXY, ^TNX sonrası); gap_l1 (d_{t-1}→gap_t); intra_l1 (d_{t-1}→intra_t); intra_l0 (d_t→intra_t); cum25 (Σd_{t-5..t-2}→cc_t); rev (cc_t→d_{t+1}).
- **Vektörizasyon:** maske matris çarpımlarıyla ikili-tam örneklem korelasyonu; kısmi korelasyon = her serinin kendi örnekleminde kontrollere göre artığı (Frisch–Waugh); t = heteroskedastisiteye dayanıklı (HC0, H0 altında). ll.ccf / ll.partial_corr ile çapraz kontrol: THYAO–^GSPC değerleri 4 haneye kadar aynı. Tüm matris ~40–60 sn.
- **Kapanış kovası (işlenebilirliğin anahtarı):** asia_pre (Tokyo/Seul/Taipei/Sidney/NZ: BIST açılışından önce kapanır → lag0 işlenebilir), asia_mid (Şanghay ~07:00 UTC), during (HK, Singapur, Hindistan, Körfez, J'burg: BIST seansı sırasında kapanır), eu (BIST'ten 0,5–1,5 sa sonra), us (ABD, vadeli, FX, kripto).
- **Çoklu test:** aile başına 48.124–48.128 test (47×1.024); 10 aile → tam dönemde **≈481 bin test**; IS/OOS/3y/1y ile ≈1,9 milyon korelasyon. BH-FDR aile içinde (q=0,05 ve 0,01); işlenebilir aileler için ayrıca kova içi BH.
- **Null:** sürücü matrisi 37/71/113/173/251/409 gün kaydırıldı (6 kopya) + 3 satır (tarih) permütasyonu; tüm aileler/pencereler aynen yeniden hesaplandı.
- **Backtest:** ll.backtest; aday seçimi YALNIZ IS \|t\| ile (sürücü başına 1), işaret IS korelasyonundan; hedef intra_t (lag1 veya Asya lag0) ya da cc_t (cum25); maliyet 8 ve 15 bps (XU030 için ayrıca 4); sign ve z>1 modları.

## 3. Çoklu test, null ve replikasyon (tam dönem, 47 VİOP)

| Aile | test | p<0,05 | BH q0,05 | BH q0,01 | Beklenen sahte (≤q·BH) | Null BH q0,05 (9 kopya ort.) | Null p<0,05 (shift/perm) | IS BH05 keşif | OOS replikasyon* | IS top-200 replikasyon |
|---|---|---|---|---|---|---|---|---|---|---|
| sync | 48.127 | 38.675 | 38.035 | 33.380 | ≤1.900 | 0,0 | 3.200 / 2.163 | 35.554 | %62 | %95 |
| pc_xu | 48.128 | 6.070 | 830 | 415 | ≤42 | 0,0 | 2.696 / 2.383 | 249 | %54 | %56 |
| pc_xt | 48.128 | 6.094 | 802 | 389 | ≤40 | 0,0 | 2.690 / 2.398 | 208 | %51 | %51 |
| pc_glob | 48.128 | 3.811 | 206 | 120 | ≤10 | 0,0 | 2.733 / 2.401 | 40 | %88 | %35 |
| gap_l1 | 48.124 | 19.025 | 14.631 | 9.293 | ≤730 | 0,0 | 2.649 / 2.614 | 3.500 | %69 | %62 |
| **intra_l1** | 48.124 | 3.445 | **0** | 0 | – | 0,17 | 2.440 / 2.369 | 0 | – | **%5,5** |
| intra_l0 (tüm kovalar) | 48.124 | 26.640 | 23.898 | 17.759 | (çoğu saat örtüşmesi) | 0,0 | 3.267 / 2.151 | 19.706 | %56 | %91 |
| **cum25** | 48.127 | 3.229 | **0** | 0 | – | 0,0 | 2.489 / 2.638 | 0 | – | **%5,0** |
| rev | 48.127 | 6.744 | 1.662 | 735 | (Asya örtüşmesi) | 0,0 | 2.695 / 2.155 | 889 | %44 | %58 |

\*OOS replikasyon = IS'de BH q<0,05 olan çiftlerin OOS'ta aynı işaret ve p<0,05 olma oranı; null altında beklenen ≈%2,5, IS top-200'ün null replikasyonu %2–4.

**Kova kırılımı (kova içi BH q<0,05):** intra_l1 → asia_pre 10, during 0, eu 0, us 0 · intra_l0 → asia_pre 4 (işlenebilir tek kova) · cum25 → during 7 (Hindistan: SBIN.NS, TATAPOWER.NS, SAIL.NS, SUMICHEM.NS → HALKB/ISCTR/TKFEN/VESTL), diğerleri 0 · rev → asia_pre 2.077 (Asya_{t+1} seansı BIST_t'den sonra başlar ve ABD_t'yi içerir: beklenen eser), us 4.

**Yorum.**
- Null kalibrasyonu iyi: kaydırılmış/karıştırılmış sürücüde BH geçişi ~0, p<0,05 oranı %4,5–6,7 (vol kümelenmesinden hafif şişkinlik). Gerçek veride BH'den geçenlerin tanım gereği ≤%5'i sahte.
- Senkron ailelerin büyük kısmı **saat örtüşmesi** (Avrupa/ABD lag0 BIST seansıyla örtüşür) veya piyasa faktörüdür: XU100 kontrolü 38.035 → 830'a, 10 küresel faktör kontrolü → 206'ya indiriyor.
- Hisseye özgü maruziyet gerçek ama küçük (\|pc\| 0,05–0,21). En sağlam küme pc_glob: IS'de keşfedilen 40 çiftin %88'i OOS'ta replike.
- **İşlenebilir öncülük yok denecek kadar zayıf**: intra_l1 ve cum25'te 0 FDR geçişi. Gerçek p<0,05 fazlası (~1.000 test) çok sayıda çok küçük (\|r\|≈0,02) etki olabilir; maliyet sonrası para kazandıracak büyüklükte değil.

## 4. Piyasa düzeyi (XU100/XU030)
Tek değişkenli tam dönem senkron korelasyon (XU100 TL / USD bazlı): ^STOXX50E 0,33/0,33 · ^GDAXI 0,32 · EEM 0,30/0,34 · ^GSPC 0,24/0,27 · ES=F 0,24 · EMB 0,21/0,27 · ^VIX −0,20/−0,24 · USDTRY −0,16/−0,60 (USD bazlıda mekanik) · ^TNX 0,11 · DXY −0,08 · GC=F 0,05 · BZ=F 0,04 · Asya (^N225/^KS11/^HSI) 0,15–0,17 · TUR 0,77/0,87 (ayna). Lag1 → gap: ^GSPC 0,18, ES=F 0,15, EEM 0,13, ^VIX −0,20, USDTRY −0,13; lag1 → gün-içi: hepsi \|r\|≤0,03 (Asya hariç: ^KS11 0,07, ^N225 0,05).

**Rejimler**

| Dönem | n | R² senkron 10 makro (TL) | R² (USD) | R² yalnız EEM | ABD lag1→gap R² | ABD lag1→intra R² | Dimson β USD~EEM | corr0 USD~EEM | Dimson β USD~^GSPC |
|---|---|---|---|---|---|---|---|---|---|
| 2014–2017 | 1007 | 0,26 | 0,28 | 0,15 | 0,05 | 0,02 | 0,85 | 0,48 | 0,87 |
| 2018 kur krizi | 248 | 0,23 | 0,24 | 0,12 | 0,15 | 0,07 | 0,68 | 0,32 | 0,38 |
| 2019–2020 | 497 | 0,36 | 0,29 | 0,23 | 0,14 | 0,04 | 0,74 | 0,49 | 0,67 |
| 2021 (Aralık şoku) | 247 | 0,07 | 0,14 | 0,02 | 0,06 | 0,04 | 0,57 | 0,21 | 1,08 |
| 2022–May 2023 heterodoks | 352 | 0,09 | 0,11 | 0,03 | 0,06 | 0,03 | 0,41 | 0,22 | 0,38 |
| Haz 2023–Mar 2025 ortodoks | 449 | 0,09 | 0,08 | 0,03 | 0,06 | 0,02 | 0,46 | 0,19 | 0,65 |
| Mar–Ara 2025 (İmamoğlu sonrası) | 195 | 0,13 | 0,13 | 0,01 | 0,17 | 0,03 | 0,17 | 0,12 | 0,21 |
| 2026 Oca–Ağu | 164 | 0,20 | 0,20 | 0,09 | 0,10 | 0,09 | 0,60 | 0,31 | 0,99 |
| Eyl–Eki 2026 fon krizi | 43 | 0,30 | 0,29 | 0,19 | 0,23 | 0,13 | 0,76 | 0,45 | 1,34 |
| Son 1y | 250 | 0,16 | 0,16 | 0,10 | 0,07 | 0,06 | 0,61 | 0,32 | 0,85 |
| Tam 2014–2026 | 3202 | 0,14 | 0,16 | 0,09 | 0,06 | 0,006 | 0,65 | 0,35 | 0,61 |

**Yıllara göre**

| Yıl | R² TL | R² USD | ABD lag1→gap R² | ABD lag1→intra R² | β USD~EEM | corr USD~EEM |
|---|---|---|---|---|---|---|
| 2014 | 0,28 | 0,36 | 0,11 | 0,07 | 1,08 | 0,54 |
| 2015 | 0,27 | 0,26 | 0,06 | 0,02 | 0,72 | 0,46 |
| 2016 | 0,34 | 0,38 | 0,03 | 0,07 | 0,87 | 0,55 |
| 2017 | 0,18 | 0,20 | 0,07 | 0,02 | 0,80 | 0,32 |
| 2018 | 0,23 | 0,24 | 0,15 | 0,07 | 0,68 | 0,32 |
| 2019 | 0,23 | 0,23 | 0,08 | 0,04 | 0,71 | 0,41 |
| 2020 | 0,48 | 0,40 | 0,20 | 0,08 | 0,75 | 0,54 |
| 2021 | 0,07 | 0,14 | 0,06 | 0,04 | 0,56 | 0,21 |
| 2022 | 0,17 | 0,18 | 0,11 | 0,06 | 0,53 | 0,34 |
| 2023 | 0,05 | 0,04 | 0,06 | 0,05 | 0,15 | 0,04 |
| 2024 | 0,16 | 0,18 | 0,09 | 0,04 | 0,49 | 0,22 |
| 2025 | 0,12 | 0,12 | 0,13 | 0,02 | 0,25 | 0,16 |
| 2026 (Eki'ye kadar) | 0,18 | 0,18 | 0,07 | 0,07 | 0,65 | 0,34 |

Yorum: küresel faktörler XU100 günlük getirisinin tam dönemde yalnız ~%14–16'sını açıklıyor; en düşük 2021 ve 2023 (yerel politika/kur rejimi baskın), en yüksek 2020 (COVID) ve Eyl–Eki 2026 (kriz dönemleri korelasyonu artırır). R² örneklem içi ve 9–10 regresörlü: kısa pencerelerde (43 gün) şişer, DÜŞÜK güven. ABD lag1 → gün-içi R² tam dönemde 0,006 → yıllık 0,02–0,09 değerleri büyük ölçüde aşırı uyum (8 regresör/250 gün ≈ 0,03 beklenen sahte R²).

## 5. Hisse başına ilk 5 dış sürücü (XU100+USDTRY kontrollü kısmi korelasyon)
Tam liste (47×5; IS/OOS/1y, 10 faktör sonrası pc, q, TV kodu, mekanizma etiketi): `code_tarama/cache/top5_per_stock.csv` ve f_tarama.csv (relation=sync, notes'ta "[hisse başına ilk 5]").

- **Net, sektör-tutarlı (sektör ajanlarını teyit):** THYAO (LHA.DE, EZJ.L, IAG.L, AF.PA, ICAGY; 0,17–0,21), PGSUS (EZJ.L, IAG.L, FRA.DE, ICAGY, AF.PA; 0,14–0,18), TAVHL (FRA.DE, IAG.L, ADP.PA, MTX.DE, EZJ.L; 0,13–0,15), TUPRS (EQNR.OL, CRAK, BZ=F, BNO, AKRBP.OL; 0,17–0,19), TRALT (GC=F, 1787.HK, GLD, FRES.L, SI=F; 0,17–0,19), TRMET (1787.HK, GLD, GC=F, RING; 0,11–0,14, OOS'ta güçleniyor), EREGL (SSAB-A.ST, MT.AS, VOE.VI, NHY.OL, 5411.T; 0,11–0,12), KRDMD (0347.HK, 0323.HK, SSAB, FMG.AX; 0,09–0,11), TOASO (VOW3.DE, EXV5.DE, PAH3.DE, ^FCHI; 0,10–0,11), FROTO (IVG.MI, PAH3.DE, VOW3.DE, EXV5.DE; 0,08–0,09), AEFES (CCH.L, CARL-B.CO, MC.PA; 0,09–0,10), CIMSA (STR.VI 0,08).
- **Makro, makul:** bankalar ← petrol negatif (AKBNK BZ=F −0,07 [IS −0,09/OOS −0,08], YKBNK −0,06, GARAN −0,05: cari açık/enflasyon kanalı); GUBRF ← altın/gümüş (yalnız OOS: IS 0,01–0,02 → OOS 0,12–0,13 → rejim); MGROS ← EURUSD −0,08 (IS −0,13 → OOS −0,02: söndü); SOKM ← ABD faizleri −0,08 (yalnız IS).
- **Anlamlı tek küresel sürücüsü olmayanlar (ilk 5 bile \|pc\|≤0,08 ve çoğu "beklenmeyen"):** AKSEN, ALARK, DOHOL, EKGYO, ENKAI, HALKB, HEKTS, ISCTR, ODAS, SASA, SISE, TCELL, TKFEN, TTKOM, ULKER, VAKBN, VESTL, TSKB, BIMAS, SOKM. Bu hisselerde sektör ajanlarının bulduğu ilişkiler büyük olasılıkla piyasa/kur faktörüdür (XU100+USDTRY kontrolünden sonra kalmıyor).
- **Kısa örneklem uyarısı:** IS değeri boş olan sürücüler (P911.DE, 9863.HK, IHS, CPNG, NU, ABNB, ARRY…) ve ASTOR (2023 halka arz) satırları yalnız OOS'a dayanıyor → DÜŞÜK.

f_tarama.csv'deki senkron satırların güven dağılımı (543 çift): YÜKSEK 29, ORTA 284, DÜŞÜK 111, ÇOK DÜŞÜK 119. YÜKSEK'lerin tamamı THYAO/PGSUS (Avrupa havayolları), TUPRS (petrol + Avrupa rafineri/petrol şirketleri) ve TRALT (altın) çiftleri.

## 6. Sürprizler (FDR'den geçen ama bariz mekanizması olmayan)
- pc_xt FDR'den geçen "beklenmeyen grup" etiketli 265 çift; 219'u OOS'ta replike, ama 10 küresel faktör kontrolünden sonra yalnız 21'i FDR'den geçiyor → çoğu **ortak faktör** (Avrupa/EM risk iştahı, sektör döngüsü) kalıntısı.
- Sağlam kümedeki (pc_glob FDR + replike) 25 "beklenmeyen" çift ve olası açıklama:
  1. **Grup etiketi hatası (gerçek sürpriz değil):** TRALT ← 2899.HK (Zijin Mining = altın/bakır madencisi; katalogda kömür listesine girmiş). Çin/HK kodları TV'de açılmayabilir → alternatif COMEX:GC1!, AMEX:GDX/GDXJ, LSE:FRES.
  2. **Sektör komşuluğu (makul):** TAVHL/PGSUS/THYAO ← MTX.DE (MTU motor bakım), AIR.DE/EADSY (Airbus), FGR.PA (Eiffage, havalimanı imtiyazları) = hava trafiği döngüsü; TUPRS ← CF, SDF.DE (gübre/potas = doğalgaz-emtia döngüsü); EREGL/KRDMD ← 7011.T/7012.T (Mitsubishi/Kawasaki Heavy = ağır sanayi/çelik talebi; Tokyo BIST açılışından önce kapandığı için kısmen öncü).
  3. **Jeopolitik kanal (makul):** AEFES ← RHM.DE (−) ve EQNR.OL (−): Rusya/savaş tırmanması günlerinde Rheinmetall ve Avrupa gazı yükselir, Rusya maruziyetli AEFES düşer.
  4. **Faiz faktörü:** ENJSA ← CABK.MC (−), THYAO ← EDP.LS (−): İspanyol bankası/ Portekiz utility'si faiz duyarlılığı vekili.
  5. **Zaman dilimi:** PGSUS ← 055550.KS (Shinhan, +): Kore kapanışı (06:30 UTC) gece ABD hareketini taşır ve BIST gap'ine girer.
  6. **Mekanizma bulunamadı (sahte olabilir; ≤10 sahte beklenir):** OYAKC ← KTOS (−0,10), DOAS ← SAAB-B.ST (+), GUBRF ← ENPH (+), SASA ← 000898.SZ (−), TCELL ← SKA-B.ST (−), TTKOM ← 0323.HK (−) → ÇOK DÜŞÜK.
- **Veri hatası:** bu turda saptanan sistematik hata FX zaman etiketiydi (düzeltildi). Kalan sağlık bayrakları gürültü düzeyinde (cache/health_timing.csv).

## 7. Backtest (görev 6)
Seçim yalnız IS \|t\|'ye göre, sürücü başına 1 (≈150 bin IS testinin en iyi 10'u → seçim yanlılığını doğrudan ölçer).

| Hisse | Sürücü (TV) | Aile | IS t | IS Sharpe 15bps | OOS Sharpe 15bps | OOS bps/işlem | OOS t | OOS Sharpe 8bps |
|---|---|---|---|---|---|---|---|---|
| AEFES | 2317.TW (TWSE:2317) | Asya lag0→intra | 4,84 | 0,34 | −1,05 | −18 | −2,6 | −0,64 |
| AEFES | BHP.AX (ASX:BHP) | Asya lag0→intra | 4,26 | −0,06 | −1,66 | −26 | −4,1 | −1,21 |
| AEFES | 000660.KS (KRX:000660) | Asya lag0→intra | 4,24 | 0,13 | −1,02 | −17 | −2,4 | −0,59 |
| THYAO | 011170.KS (KRX:011170) | lag1→intra | 3,96 | −0,09 | −0,55 | −8 | −1,2 | −0,08 |
| HALKB | EURTRY=X (FX:EURTRY) | lag1→intra | 3,89 | 0,06 | −1,06 | −19 | −2,8 | −0,66 |
| GUBRF | NKT.CO (OMXCOP:NKT) | lag2–5→cc | 3,87 | 0,21 | −0,04 | −1 | −0,1 | 0,30 |
| FROTO | JMT.LS (EURONEXT:JMT) | lag2–5→cc | 3,84 | 0,26 | −0,45 | −7 | −1,1 | −0,03 |
| SISE | ^KLSE (MYX:FBMKLCI?) | lag1→intra | 3,81 | −0,23 | −0,60 | −9 | −1,5 | −0,11 |
| EREGL | SZG.DE (XETR:SZG) | lag1→intra | 3,81 | 0,18 | −0,43 | −6 | −1,0 | 0,03 |
| TAVHL | CENX (NASDAQ:CENX) | lag1→intra | 3,81 | 0,58 | −1,51 | −24 | −3,6 | −1,06 |

8 bps: OOS Sharpe medyan −0,35 (en iyi +0,30); z>1 modunda en iyi SISE←^KLSE +0,59 (t=1,4, n=375), EREGL←SZG.DE +0,37 — anlamsız. Referans XU030 (^GSPC, ES=F, TUR, EEM, ^VIX lag1; ^N225, ^KS11 lag0): 8 bps OOS Sharpe −0,30…−0,78. Ayrı test: XU030 ← ^KS11_{t-1} (bulgu 5) z>1 modunda 4/8/15 bps OOS Sharpe 0,82/0,62/0,27 (t 1,75/1,33/0,59; IS 0,70/0,47/0,06) — işaret tutarlı ama istatistiksel olarak anlamsız; yıllık kârlılık 2025'te negatif, 2026'da pozitif. BIST'in kendi gap_{t-1} sinyali 8 bps'de IS −0,96 / OOS 0,11.

**Sonuç:** Günlük veriyle maliyet sonrası işlenebilir lead-lag stratejisi bulunamadı. Gün-içi hedefte \|r\|≈0,05–0,07'lik ilişkiler günlük 2–5 bps brüt kenar üretiyor; 8–15 bps maliyet bunu siliyor. Yalnız seyrek (z>1) Asya-lag1 sinyali düşük maliyetli XU030 vadelisinde izlenmeye değer (DÜŞÜK).

## 8. Karşı argümanlar ve sınırlamalar
- BH aile içi; aileler arası birleşik düzeltme yapılmadı (yapılsa daha da az geçer). Sürücüler kendi aralarında çok korelasyonlu (BH PRDS altında geçerli; etkin test sayısı daha düşük).
- Kısmi korelasyon için sürücüye özel artık (her seri kendi örnekleminde) kullanıldı; ikili örneklemler neredeyse aynı olduğundan fark ihmal edilebilir, ama yeni listelenen semboller IS'siz.
- USDTRY kontrolü düzeltilmiş FX'tir (UTC günü t; BIST kapanışından ~9 saat sonra biter) → kur kontrolü BIST kapanışı sonrası hareketi de içerir; USD bazlı getiri de aynı kaymayı taşır.
- Senkron korelasyonlarda asia_pre sürücülerinin lag0'ı BIST açılışından önce bilinir (gap'e girer); bu çiftler "senkron" sayıldı ama aslında gap kanalıdır.
- Günlük veri ABD vadelilerinin BIST açılışı öncesi gece hareketini ayrı ölçmüyor; saatlik öncülük bu taramanın kapsamı dışında (saatlik veri yalnız 2023-11+).
- intra = Yahoo açılışından kapanışa; VİOP pay vadelisi 09:30'da açılır, açılış fiyatına tam erişim yok → gerçek uygulanabilirlik daha kötü olabilir.
- Eyl–Eki 2026 penceresi 43 gün: rejim sayıları DÜŞÜK güven.

## 9. Dosyalar
- Master matris: `out/tarama_matrix.parquet` (51.400 satır = 50 satır×1.028 sürücü; her aile×pencere için corr, t, n, p, q; grup, kova, seyrek/ayna bayrağı, TV adayı).
- Bulgular: `out/f_tarama.csv` (623 satır): (A) 10 aile özeti (test sayısı, FDR, null'da beklenen sahte, replikasyon), (B) SAĞLAM küme 162 çift (pc_glob FDR + IS/OOS replike), (C) pc_xt FDR + replike \|pc\|≥0,08, (D) hisse başına ilk 5, (E) öncülük: kova-içi FDR 21 çift + Asya→XU030 + 10 backtest, (F) gap referansı (işlenemez), (G) 24 rejim/yıl satırı. Güven: brief ölçeği + yılların ≥%75'inde aynı işaret.
- Kod: `out/code_tarama/` → tlib.py (vektörize corr/HC-t/artık/BH/TV/regroup/mekanizma), matrix.py, health.py, fdr_null.py, breakdown.py, rest.py, asia_check.py, final_csv.py; ara sonuçlar cache/.
- Yeniden üretim: `cd out/code_tarama && nice -n 10 python3 matrix.py && python3 health.py && python3 fdr_null.py && python3 breakdown.py && python3 rest.py && python3 asia_check.py && python3 final_csv.py`.
