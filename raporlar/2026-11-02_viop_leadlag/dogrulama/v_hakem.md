# v_hakem: tarama "0 FDR" ve sektör sepetlerinin "pozitif OOS" sonucu arasındaki çelişki

Tarih: 02.11.2026. Veri 30.10.2026'ya kadar. Bağımsız kod: `out/code_v_hakem/`. `ll.py` import edilmedi; hizalama, temizlik ve istatistik kodu `vh.py`'de, sıfırdan yazıldı.

Çalıştırma sırası: `peers.py` (ön-kayıt) → `h1_build` → `h2_main` → `h3_robust` → `h4_mech` → `h5_sideby` → `h6_viop` → `h7_index_family` → `h8_table`. Sonuçlar `res/` altında (her betik için `*_summary.txt` ve CSV).

## 0. Kısa hüküm

1. **İki taraf da kendi tanımına göre doğru. Çelişki, verinin değil tanımın ve test ailesinin ürünü.**
   - Tarama ajanı tek sürücü, ham (hedge'siz) gün-içi hedef ve 48.124'lük aile kullandı. Bu ailede BH'nin 1. sıra eşiği yaklaşık t≈4,9.
   - Gerçek etki küçük (|r|≈0,05–0,10) ve yüzlerce çifte dağılmış. Bu koşullarda tek tek hiçbir çift o eşiği geçemez.
   - Tarama matrisinin **kendi t değerleri** önceden tanımlanmış 560 (hisse, emsal) çiftine daraltılınca tablo değişiyor: t>2 olan 93 çift, t<−2 olan 2 çift; aile içi BH 25 geçiş (h7). Null altında her iki yönde ~14 çift beklenirdi.
2. **"Sektöre özgü bilgi açılışta eksik fiyatlanıyor, piyasa geneli bilgi tam fiyatlanıyor" hipotezi GENEL bir istatistiksel anomali olarak destekleniyor.** Birkaç seçilmiş örnekle sınırlı değil. Rakamlar:
   - 47 hissede havuzlanmış eğim 1σ sinyal başına **+4,6 bps**, Driscoll–Kraay t=7,1 (IS 4,0 / OOS 6,0).
   - 47 hissenin 39'unda eğim pozitif. 13 yılın 13'ünde pozitif.
   - Sektör-karıştırma permütasyonu: z=9,3.
   - "Ünlü" 6 hisse çıkarılınca t=5,1. Hangi sektör çıkarılırsa çıkarılsın t≥5,3.
   - Gerçek VİOP pay vadelisi fiyatlarıyla: t=7,1.
3. **Ekonomik büyüklük küçük.** Sektör sepeti sinyali gün-içinde 1σ başına ~5 bps getiriyor. |z|>1 günlerinde brüt kazanç pozisyon başına 7–11 bps. Gidiş-dönüş 8–15 bps maliyet bunu siliyor.
   - Kâr kalan tek yer keşif amaçlı bir eşik: |z|>2 ve VİOP. Orada net 8+3 bps maliyetle +16 bps/pozisyon, ama t=1,9 (OOS 1,7). Anlamlı değil.
   - Etki metal, havacılık, rafineri ve altında güçlü; bankalarda ve holdinglerde yok. Bu yüzden 1. turdaki "pozitif OOS" sepetleri doğru yerden ölçülmüş, ama işlem kârları iyimser (ayrıntı §5).

## 1. Ön-kayıt: sepetler ve tanımlar (sonuçlara bakmadan sabitlendi)

**Sepetler (`peers.py`, sha256: `res/peers_prereg.sha256`).**
- Her hisse için kendi sektör ajanının **hipotez listesi** alındı. Kaynak: o ajanın 01_hyp / a1_hyp / a1_pairs / sv.py / a1_curated dosyaları. FDR çıktıları kullanılmadı.
- Listeden BIST-dışı tekil hisseler ve sektör ETF'leri mekanik bir kuralla seçildi. Sonuç: 47 hisse, 288 kullanılabilir emsal.
- Çıkarılanlar:
  - geniş endeks ve ülke ETF'leri;
  - FX, emtia ve faiz serileri;
  - TKC gibi ayna enstrümanlar;
  - hedef hisseyi içeren ETF'ler (CRAK yaklaşık %3,9 TUPRS içeriyor);
  - BIST seansı içinde kapanan borsalar (HK, Çin, Hindistan, Körfez, JSE, Atina, Tel Aviv, Moskova);
  - OTC ADR'ler ve aynı şirketin ikinci kotasyonu.
- ARCH ve CRFB3.SA Yahoo'dan silinmiş (HTTP 404), sepette yer almıyor.

**Zamanlama (UTC, `vh.py`).** Emsal seansı, bittiği andan sonraki ilk BIST açılışına atandı:
- ABD ve Avrupa seansı yerel tarih d → BIST'te d'den sonraki ilk gün.
- Japonya, Kore, Tayvan ve Avustralya (06:30'dan önce kapanır) seansı d → d'ye eşit ya da sonraki ilk BIST günü.
- Tatillerde arada kalan seanslar toplandı.

**Sağlık kontrolü (zamanlama).** Post kovası sinyali bir gün kaydırılıp aynı günün seansı kullanılınca beklendiği gibi büyük ve senkron bir korelasyon çıkıyor: THYAO–LHA 0,23 (öncül tanımda 0,05). Yani hizalama doğru.

**Tarama ile uzlaşma.**
- KRDMD~FMG.AX lag0: benim t 4,29, tarama 4,28.
- TUPRS~VLO lag1: benim t 2,99, tarama 3,19 (fark tatil ffill farkından).

**Birincil tanım.**
- Sinyal: x = emsal sepetinin bölge endeksine göre **artığının** ortalaması. Artık = emsal − β·endeks, β geçmiş 250 günden. Endeksler: ABD ^GSPC, Avrupa ^STOXX, ^N225, ^KS11, ^TWII, ^AXJO, ^GSPTSE, ^MXX, ^BVSP. Sinyal geçmiş 250 güne göre z-skoruna çevrildi ve ±4'te kırpıldı.
- Hedef: y = **hedge'li gün-içi** = ln(c/o) − β·XU100 gün-içi (β geçmiş 250 günden).

**İstatistik.**
- Hisse bazında: NW(5) t, ardından 47 hisse üzerinde BH-FDR.
- Havuzlanmış: hisse sabit etkili OLS. SE iki türlü: Driscoll–Kraay (tarih skorları, NW 5) ve tarih kümeli.
- IS 2014–2020, OOS 2021–2026.

> **Kod hatası, kendim buldum ve düzelttim.** `vh.bucket()` ilk sürümde son eki olmayan Asya endekslerini (^N225, ^KS11, ^AXJO) "post" kovasına koyuyordu.
> - Ana panel (`h1_build`) **etkilenmedi**, çünkü orada endeks emsalin kovasıyla hizalanıyor.
> - Etkilenenler: h5'teki "Asya piyasası / kompozit artığı" satırları ve h7(a). İkisi de düzeltildi ve yeniden çalıştırıldı.

## 2. Aynı veride tanımlar yan yana: hangi fark ne kadar güç kazandırıyor (h2_ladder)

| Tanım (47 hisse) | b>0 | hisse t>2 | BH q<0,05 (47) | Havuzlanmış b (bps/σ) | DK t tam / IS / OOS |
|---|---|---|---|---|---|
| L0 tek emsal, ham gün-içi (= tarama; 560 çift) | %70 çift + | 106 (t<−2: 3) | aile-içi 37 / 48k-ailesinde 0 | — | en büyük t 4,29 < ~4,9 eşik |
| L1 ham sepet → ham gün-içi | 39 | 11 | 7 | 4,9 | 2,8 / 2,6 / 1,3 |
| L2 artık sepet → ham gün-içi | 43 | 14 | 10 | 6,5 | 5,4 / 5,2 / 2,6 |
| L3 ham sepet → hedge'li gün-içi | 32 | 11 | 5 | 3,4 | 4,7 / 2,8 / 4,0 |
| L4b emsal − endeks (β=1) → hedge'li | 37 | 13 | 7 | 4,4 | 6,7 / 3,6 / 6,0 |
| **L4 artık sepet → hedge'li (BİRİNCİL)** | **39** | **15** | **8** | **4,6** | **7,1 / 4,0 / 6,0** |

**Neden fark ediyor?**
- **Hedge'siz hedef** XU100 gün-içi gürültüsünü taşıyor, bu da gücü düşürüyor.
- **Ham sürücü** bölge piyasa bileşenini taşıyor. Bu bileşenin gün-içi etkisi yok (§3), bu yüzden sinyali sulandırıyor.
- **Sepet** emsale özgü gürültüyü ortalayıp azaltıyor.
- **Aile büyüklüğü**: 48.124 test, etkisi olmayan 1.024 sürücüyü de içeriyor. Bu, eşiği t≈4,9'a itiyor.
- Tarama ajanının **"IS t'ye göre en iyi 10 aday"** seçimi ~150 bin test arasından yapıldı. Null altında beklenen en büyük |t| 4,6–4,9, seçilen IS t'leri 3,8–4,8. Yani bu seçim gürültü topluyor; OOS Sharpe −0,81 beklenen sonuç.
- Aynı seçim benim 560'lık ön-kayıt ailemde yapılınca: 10 adayın 10'u OOS'ta aynı işarette, ama yalnız 1'inde OOS t>1,96. Doğru ailede bile kazananın laneti küçülme yaratıyor.

## 3. Hipotez testi: 47 hisse, havuzlanmış panel ve hisse bazında FDR

**Havuzlanmış etki (h2, h3).**
- Birincil: b=4,57 bps/σ, DK t 7,07 (kümeli 6,83).
- IS: 3,38 (t 4,01). OOS: 6,01 (t 6,03).
- Kontroller katsayıyı değiştirmiyor:
  - kendi artığı(t−1) ve XU100(t−1) eklenince: 4,59 (t 7,05);
  - aynı günün hedge'li gap'i de eklenince (açılışta bilinir): 4,80 (t 7,35). Gap'in kendi ters dönüş katsayısı −14 bps/σ.

**Genel mi, birkaç örnek mi? (h2_generality)**
- 39/47 pozitif (binom p<0,0001). OOS'ta 36/47.
- "Ünlüler" (TUPRS, THYAO, PGSUS, TAVHL, EREGL, KRDMD) çıkarılınca: b 3,44, t 5,09 (IS 2,78 / OOS 4,41); 33/41 pozitif.
- Herhangi bir sektör dışarıda bırakılınca t 5,3–7,5.
- Sektör içinde:

| Sektör | b (bps/σ) | t |
|---|---|---|
| metal | 12,3 | 5,7 |
| havacılık | 11,2 | 4,2 |
| otomotiv | 4,8 | 2,8 |
| savunma-telekom | 4,7 | 2,3 |
| enerji | 3,6 | 2,2 |
| tüketim | 3,5 | 1,9 |
| kimya | 2,8 | 1,8 |
| banka | 1,9 | 0,9 |
| holding | 1,2 | 1,0 |

- **Sektör-karıştırma permütasyonu** (5.000 tekrar; her hisseye başka sektörden rastgele bir hissenin sepeti verildi): null ortalaması −0,07 bps, sd 0,50; gerçek 4,57 → z 9,3 (IS 6,2 / OOS 7,4). Etki **sektöre özgü**; "herhangi bir yabancı artık" aynı sonucu vermiyor.
- Yıllar: 13/13 pozitif. 2017, 2020, 2022, 2025 ve 2026'da t>2. 2025–26 en güçlü yıllar (8,1 / 8,7 bps).
- Plasebo:
  - sinyal 1 gün bayatlatılınca (t−2 bilgisi): 2,8 bps (t 3,8). Çok günlü yavaş yayılım var;
  - 2 gün bayat: 0,9 bps (t 1,3), kayboluyor.

**Hisse bazında BH-FDR (47 test, birincil tanım).**
- Tam dönem 8 geçiş: TRALT 19,4 bps (t 4,39), EREGL 12,3 (4,04), TUPRS 12,1 (3,88), KRDMD 13,8 (3,67), THYAO 10,3 (3,24), PGSUS 14,0 (3,21), HALKB 8,9 (2,87), TAVHL 9,1 (2,74).
- IS'te 0 geçiş (güç düşük).
- OOS'ta 8 geçiş: TRALT, EREGL, TUPRS, THYAO, PGSUS, TAVHL, FROTO, PETKM.
- IS'te t>1,96 olan 5 hisseden 4'ü OOS'ta t>1,96 (TRALT, EREGL, KRDMD, PGSUS); HALKB OOS'ta 1,70.
- Negatif ama anlamsız: ALARK −1,6, AKSEN, ODAS, YKBNK.
- **Karar: genel bir anomali.** Ama hisse başına ancak ~8 hissede tek başına ayırt edilebilir büyüklükte; bunlar emsal mekanizması net olan hisseler (çelik/madenci, havayolu, rafineri, altın madencisi).

**"Eksik fiyatlama" ne kadar? Gap ile gün-içi karşılaştırması (h2).** Aynı sektör artığı sinyali için:
- Hedge'li gap eğimi 1,32 bps (t 3,6), gün-içi eğimi 4,57 (t 7,1).
- Tepkinin **%78'i açılıştan sonra** geliyor (IS %67, OOS %86).

**Piyasa geneli bilgi (hipotezin ikinci yarısı).**
- Panel içinde (h2), sepetin piyasa bileşeni (β·bölge endeksi):
  - hedge'li gün-içi: −0,6 (t −0,8);
  - ham gün-içi: +0,35 (t 0,15);
  - gap: +2,4 (t 3,2).
- Endeks düzeyinde (h7a; z başına bps, NW t):

| Öncül endeks penceresi | XU100 gap | XU100 gün-içi |
|---|---|---|
| ^GSPC (ABD) | 14,2 (t 7,3) | 0,5 (t 0,2) |
| ^N225 (Japonya) | 23,6 (t 10,5) | −0,02 |
| ^KS11 (Kore) | 23,4 (t 10,7) | 4,4 (t 1,65) |
| ^AXJO (Avustralya) | 20,5 (t 8,8) | 0,4 |
| ^STOXX (t−1 seansı; büyük kısmı BIST t−1 ile eşzamanlı) | 3,3 (t 1,8) | 3,3 (t 1,3) |

- **Piyasa geneli bilgi açılışta tam fiyatlanıyor.** Havuzlanmış emsal tanımında aşırı fiyatlama yok. Tarama ajanının bulduğu küçük negatif (XU100 gün-içi ~ ^GSPC_{t−1} r=−0,02) ile tutarlı; o değer de ≈0.

## 4. Alternatif açıklamalar ve test sonuçları

| Alternatif | Test | Sonuç |
|---|---|---|
| Küresel sektör momentumu: emsal artığı ertesi gün de aynı yönde gidiyor, BIST onu eşzamanlı izliyor | Sepet artığının otokorelasyonu; aynı bölgenin t seansı kontrol | Otokorelasyon AB 0,024, ABD 0,025, Asya 0,006. AB öncül eğimi tek başına 3,59 (t 5,3); eşzamanlı AB sektör hareketi kontrol edilince 3,77 (t 5,5). Eşzamanlı eğim 7,7 olduğundan momentum kanalı en fazla ~0,2 bps açıklar. ABD: 4,11 → 4,08. **Reddedildi** |
| Bayat açılış fiyatı veya illikit hisse (açılış seansı haberi yansıtmıyor, sonra yakalıyor) | Saatlik dilimler (2023-12+); likidite tercilleri | Açılış→07:30 UTC eğimi 0,2–0,75 bps (t 0,3–1,1). 07:30→kapanış 6,0 (t 5,5); 08:30→kapanış 4,9 (t 5,0). Sürüklenme gün boyu saatte ~1 bps (h4). Likidite: düşük tercil 1,6 (t 1,7), orta 6,7 (t 6,5), yüksek 5,4 (t 5,1). Etki likit hisselerde daha güçlü. **Reddedildi** |
| Kendi momentumu / piyasa momentumu (yurt içi brifing tuzak #3) | OWN_l1 ve XU100_{t−1} kontrolü | b 4,57 → 4,59. **Reddedildi** |
| Kendi gap'inin gün içinde geri dönmesi | Aynı gün gap kontrolü | b 4,80 (artıyor). **Reddedildi** |
| Spot açılış fiyatı varsayımı (işlenebilirlik) | Gerçek VİOP ön-ay kapanış/açılış; XU030 vadelisiyle hedge | b 7,23 (t 7,10); IS (2017-03–2020) 7,2 (t 4,0), OOS 7,2 (t 5,8). Uzlaşma fiyatıyla da 7,15. VİOP'ta b>0 olan 37/47, t>2 olan 17, BH 10. Likiditeye göre: düşük 5,0 (t 3,1), orta 7,8, yüksek 8,2 (t 6,1). **Etki vadelide de var** |
| VİOP açılışı (09:30 ilk işlem) kısmen bayat | XU030 vadelisi gün-içi ~ Asya endeksi lag0 | Vadelide b 10–12 (t 2,4–2,9), spotta ~0. VİOP ilk işlemi Asya kapanışıyla çakışıyor; piyasa bileşeni sızıyor. Hedge'li hisse vadelisinde bu sızıntı büyük ölçüde iptal oluyor: VİOP 7,2 vs aynı günlerde spot 6,6 |

## 5. Sektör ajanlarının birebir tanımları, benim verimle (h5)

### Enerji: ABD rafinerileri → TUPRS

| Tanım | Sonuç |
|---|---|
| Tarama tanımı: VLO_{t−1} → TUPRS ham gün-içi | r 0,067, HC t 2,98 (IS 1,66 / OOS 2,80) |
| Enerji H1 tanımı: TUPRS − XU100 gün-içi (β=1) | r 0,095, HC t 4,60 (iid 5,29; ajan iid 5,98); IS 3,05 / OOS 3,54 |
| US_REF z>1, 2 bacak 16 bps | Brüt IS 13,7 (t 1,7) / OOS 34,5 (t 3,9), ajan 17,7 / 25,6. Net IS −2,3 / OOS +18,5 (t 2,1) |
| Aynı sepet, işaret modu (her gün), 16 bps | IS −10,5 / OOS +0,8 |
| SPX_{t−1} → TUPRS hedge'li | t 1,0 (etki piyasadan gelmiyor) |
| Birincil tanım | 12,1 bps/σ, t 3,88 (IS 1,84 / OOS 3,59), q 0,002 |
| VİOP | 21,5 bps/σ (t 5,30); 47 hisse içinde en güçlü |

**Hüküm: DÜZELT, güven ORTA.** İstatistik gerçek; ama IS zayıf ve IS'te maliyet sonrası net negatif.

### Havacılık: AB+ABD havayolu sepeti → THYAO / PGSUS

| Tanım | Sonuç |
|---|---|
| AIR_only, \|.\|>1, ham gün-içi, 8 bps (THYAO) | IS 17,4 (t 2,2) / OOS 17,1 (t 2,4); ajan 17,6 / 20,3 |
| Aynı, PGSUS | 20,3 / 21,0; ajan 22,0 / 24,5 |
| Aynı sinyal → XU100 / XU030 | OOS −2,5 / −3,3 (havacılığa özgü) |
| 15 bps, tek bacak | THYAO 10,1 (t 1,4), PGSUS 14,0 (t 1,6) |
| β-hedge'li, 2 bacak 16 bps (OOS) | THYAO 3,8 (t 0,6), PGSUS 7,6 (t 1,0) |
| COMBO (TUR sonradan eklendi) | THYAO 23,3 / 24,9; ajanın sayısıyla örtüşüyor |
| Birincil tanım | THYAO 10,3 bps/σ (t 3,24), PGSUS 14,0 (t 3,21), TAVHL 9,1 (t 2,74) |
| VİOP | THYAO 12,0 (t 2,9), PGSUS 17,3 (t 2,7) |

**Hüküm: DÜZELT.** "+20–25 bps OOS" rakamı şu varsayımlara dayanıyor: 8 bps tek bacak, hedge'siz pozisyon (piyasa riski açık) ve COMBO'daki sonradan eklenmiş TUR bacağı.

### Metal: Japon/ASX kompoziti → EREGL / KRDMD

| Tanım | Sonuç |
|---|---|
| Ajanın ham z-kompoziti, z>1, 15 bps | EREGL IS 13,5 / OOS 26,3 (ajan 12,1 / 27,7); KRDMD 29,0 / 31,1 (ajan 26,3 / 32,1) |
| Aynı kompozit → XU100 | z>1 günlerinde brüt +15 bps (t 2,5 / 2,1); kenarın bir kısmı piyasa/döngüsel maruziyet |
| Artık kompozit (doğru hizalı) → ham gün-içi, net 15 bps | EREGL IS 15,2 (t 2,0) / OOS 8,2 (t 0,65); KRDMD 23,0 (t 2,2) / 17,9 (t 1,15) |
| Artık kompozit, hedge'li, 2 bacak 30 bps | Negatif |
| Asya piyasası (N225 + AXJO z) → EREGL / KRDMD | t 1,5 / 1,4. Eşzamanlı ilişki hisseye özgü; kenarı şişiren piyasa yönü |
| Birincil tanım | EREGL 12,3 (t 4,04), KRDMD 13,8 (t 3,67) |
| VİOP | EREGL 17,0 (t 4,1), KRDMD 19,0 (t 3,8) |

Ek sorunlar: kompozitin bileşenleri FDR geçenlerden seçildi (6301.T Komatsu çelik emsali değil).

**Hüküm: DÜZELT.** İstatistiksel öncülük gerçek ve en güçlüler arasında. "OOS +28–32 bps" ise seçim yanlılığı ve piyasa maruziyeti yüzünden abartılı.

### FMG.AX → KRDMD / EREGL

- Ham: t 4,31 / 3,97 (IS 2,58 / 2,50; OOS 3,82 / 3,14). Hedge'li: 3,87 / 3,49.
- FMG → XU100: t 2,6. Etkinin bir kısmı piyasa geneli.
- Tek sürücü backtesti (z>1, 15 bps): KRDMD IS 3 / OOS 22 bps (t 0,25 / 1,56).
- **Hüküm: KABUL.** İstatistik YÜKSEK, işlem değeri DÜŞÜK.

## 6. Backtest: hipotezin işlem değeri (ön-kayıt: pozisyon = sign(z))

| Kurgu | Pozisyon başına brüt bps (tam / OOS) | Net | Not |
|---|---|---|---|
| Spot hedge'li, her gün | 3,3 / 3,9 (portföy t 5,3) | 16 bps'de −12,7 | |
| Spot hedge'li, \|z\|>1 | 7,4 / 10,0 | 16 bps'de −8,6 / −6,0 | Hisse bazında OOS net>0: 13/47 |
| Spot ham, \|z\|>1 | 11,1 / 9,8 | 8 bps'de +3,1 (t 0,7) / +1,8; 15 bps'de −4,0 | Hisse bazında: 8 bps'de OOS net>0 29/47, OOS Sharpe medyanı 0,13 |
| VİOP hedge'li, \|z\|>1 | 11,5 / 11,2 | 8+0: +3,5; 8+3: +0,5; 15+3: −6,5 | |
| VİOP hedge'li, \|z\|>2 (KEŞİF, ön-kayıtta yok) | 27,2 / 25,7 | 8+3: +16,2 bps (portföy t 1,9; OOS t 1,7; Sharpe 0,54); 15+3: +9,2 (t 0,4) | |

- Brüt kenarın kayda değer kısmı açılıştan 30–60 dakika sonra da yakalanıyor: 07:30→kapanış eğimi tüm gün-içi eğimin ~%95'i (2023-12+). Yani açılış seansında dolum varsayımı kritik değil.
- **Sonuç:** VİOP maliyeti gidiş-dönüş 8–15 bps (artı hedge bacağı) olunca bu sinyal tek başına işlem stratejisi değil. Ancak şu kullanım için anlamlı bir **filtre / ağırlık** olarak değerlendirilebilir: başka bir nedenle zaten alınacak pozisyonun yönü ya da zamanlaması.

## 7. Yurt içi (ulusal) karşıt aile (kullanıcı isteği)

Yurt içi emsal artığının (BIST emsalleri − β·XU100; brifingdeki kümeler) t−1 değerinin hisseyi öncüleyip öncülemediği test edildi. Bu bilgi BIST kapanışında zaten biliniyor, yani "açılışta yeni bilgi" değil.

- Hedge'li gün-içi hedef: b 1,39 bps/σ (t 1,76). Kendi ve XU100 gecikmesi kontrol edilince 1,30 (t 1,9). Hisse bazında BH 1.
  - **Gün-içi öncülük yok.** Dış artık ile birlikte konunca dış sepetin katsayısı değişmiyor: 4,58 (t 6,9).
- Hedge'li gap hedef: 2,72 (t 4,36). Ama yalnız OOS'ta: OOS 5,31 (t 4,73), IS 0,45 (t 0,8).
  - Yurt içi sektör bilgisi kısmen ertesi açılışta devam ediyor. Bu rejime bağlı: 2021+ küçük-büyük hisse ayrışması ve bireysel yatırımcı akımı.
  - Kapanışta girilip açılışta çıkılarak işlenebilir; ama 2,7 bps maliyetin çok altında. Güven: DÜŞÜK.
- Hisse bazında öne çıkanlar:
  - **TRMET ← TRALT/TRENJ: negatif**, −21,6 bps/σ (t −4,6; IS −3,9 / OOS −2,6; q<0,01). Koza grubu içinde aşırı tepki ve ertesi gün geri dönüş, ya da karşılıklı iştirak NAV arbitrajı. Güven: ORTA.
  - **SASA ← bireysel-favori sepeti** (HEKTS, KONTR, ASTOR, SMRTG, EUPWR, GESAN, CWENE, YEOTK, ALFAS): +13,2 (t 3,0; IS 1,6 / OOS 2,8; q 0,05). Bireysel yatırımcı momentumu. Güven: DÜŞÜK–ORTA.
- **Hipotezle tutarlı karşıtlık:** BIST kapanışından **sonra** gelen dış sektör bilgisi gün-içinde yavaş fiyatlanıyor. BIST kapanışında zaten **bilinen** yurt içi sektör bilgisinin gün-içi öncülüğü yok.

## 8. Sınırlamalar ve öz-eleştiri

- Sepet kuralı mekanik, ama listeler sektör ajanlarının 1. tur hipotezlerinden geliyor. Ajanlar bu listeleri yazarken sektör literatürünü biliyordu. Tam bir "kör" ön-kayıt değil; ancak FDR çıktısı kullanılmadı.
- Benim de bazı sonuçları gördükten sonra eklediğim keşif analizleri var: |z|>2 eşiği, saatlik profil, VİOP. Bunlar keşif olarak etiketlendi.
- Hedge'li hedefte XU100 hisseyi de içeriyor (THYAO, TUPRS ağırlığı %5–8). Bu, etkiyi bir miktar küçültür; yani tahmin muhafazakâr.
- Birincil tanımda Avrupa emsallerinin t−1 seansının büyük kısmı BIST t−1 seansıyla eşzamanlı. "Açılışta yeni bilgi" yorumu tam olarak yalnız ABD ve Asya için geçerli. Avrupa için yorum "BIST'in Avrupa sektör bilgisini ertesi güne kadar yavaş fiyatlaması". Her iki bölge de ayrı ayrı anlamlı: AB 3,6 (t 5,3), ABD 4,1 (t 6,1), Asya 3,4 (t 3,4).
- Saatlik veri 2023-12'den başlıyor. VİOP verisi 2017-03'ten başlıyor ve ilk işlem fiyatı (09:30) kısmen bayat.
- Holding ve bankalarda emsal mekanizması zayıf. Bu sektörlerin sıfır sonucu "anomali yok" anlamına değil, "uygun emsal yok" anlamına gelebilir.
- DK SE 5 gecikme kullanıyor. Kesitsel bağımlılık hesaba katıldı. Aynı sepeti paylaşan 7 banka sorun değil.

## 9. Dosyalar (`out/code_v_hakem/res/`)

| Dosya | İçerik |
|---|---|
| `h2_ladder.csv` | Tanım merdiveni |
| `h2_per_stock_all_defs.csv` | Hisse bazında, tüm tanımlar |
| `h2_L0_full.csv` | 560 tek-emsal çifti |
| `h2_market_vs_resid.csv`, `h2_gap_vs_intra.csv`, `h2_regions.csv` | Piyasa/sektör ayrıştırması, gap/gün-içi, bölgeler |
| `h2_generality.csv`, `h2_perm.csv`, `h2_years.csv` | Genellik, permütasyon, yıllar |
| `h3_controls.csv`, `h3_buckets.csv`, `h3_liquidity.csv`, `h3_hourly_segments.csv` | Kontroller, z kovaları, likidite, saatlik dilimler |
| `h3_backtest_portfolio.csv`, `h3_backtest_stock.csv`, `h3_backtest_years.csv` | Backtestler |
| `h3_dom.csv`, `h3_dom_stock.csv` | Yurt içi aile |
| `h4_lead_vs_sync.csv`, `h4_hourly_profile.csv` | Mekanizma testleri |
| `h5_sideby.csv` | Ajan tanımları yan yana |
| `h6_viop_reg.csv`, `h6_viop_bt.csv`, `h6_viop_stock.csv` | VİOP testleri |
| `h7_index.csv`, `h7_tarama_prereg_family.csv` | Endeks düzeyi ve tarama ailesi |
| `h8_stock_table.csv` | 47 hisse birleşik tablo |

**TradingView karşılıkları (sepet örnekleri):**
- Rafineri: NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF.
- Havayolu: XETR:LHA, EURONEXT:AF, LSE:IAG, LSE:EZJ, LSE:WIZZ, NYSE:DAL, NASDAQ:UAL, NASDAQ:AAL.
- Çelik/madenci: EURONEXT:MT, OMXSTO:SSAB_A, XETR:SZG, VIE:VOE, AMEX:SLX, ASX:FMG, ASX:BHP, TSE:5401, TSE:5411.
- Altın madencisi: AMEX:GDX, AMEX:GDXJ, NYSE:NEM, NYSE:AEM.
- Bölge endeksleri: TVC:SXXP (STOXX 600), SP:SPX, TVC:NI225, ASX:XJO, TVC:KOSPI.
- Hedef ve hedge: BIST:<hisse>, BIST:XU100; VİOP XU030 vadelisi BIST:XU0301! (?).
