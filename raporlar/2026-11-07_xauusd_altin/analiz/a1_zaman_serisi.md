# a1_zaman_serisi — Altının kendi fiyat dinamiği ile VİOP F_XAUUSD (uzlaşmadan uzlaşmaya 1/3/5 gün)

Tarih: 2026-11-07. Veri: VİOP paneli 2017-03-06 → 2026-11-06 (2.427 işlem günü), spot paneli 2010-01-04 → 2026-11-06 (Dukascopy XAUUSD, 15:00 UTC).
Kod: `out/a1_zaman_serisi/` (`run_all.sh` hepsini baştan üretir, ~50 sn). Tüm tablolar `tables.md` ve CSV dosyalarında. Bu raporun sonunda tabloların tamamı ek olarak var.

## 0. Kısa sonuç

1. **Toplam 984 test kaydedildi.** Bunların 918'i birincil, 66'sı sağlamlık testi. 102'sinde p<0,05 çıktı (beklenen ≈49). Testler birbiriyle güçlü korelasyonlu. **Bu ajanın kaydı içinde BH-FDR sonrası hiçbir test q<0,10'u geçmiyor; en iyi q = 0,30.** Altının kendi geçmiş fiyatından 1–5 günlük yön öngörüsü genel olarak zayıf.
2. **En iyi aday: "sakin piyasa momentumu" (LOWMOM).** 20 günlük gerçekleşen oynaklık, 2010'dan beri oluşan dağılımın alt üçte birindeyse, son 5 günün yönünde pozisyon alınır. Diğer günlerde pozisyon yok.
   - VİOP'ta drift çıkarılmış net Sharpe: h=1'de 0,99 (t=3,06), h=5'te 0,95 (t=2,96).
   - IS ve OOS ayrı (h=1 / h=5): IS 0,82 / 0,55, OOS 1,31 / 1,63.
   - Erken spot dönemi 2010–2016 aynı işarette ama anlamsız: 0,51–0,58 (t≈1,4–1,6). Tam spot dönemi 2010–2026: 0,71–0,80 (t≈3).
   - Güven etiketi **ORTA**. h=1'de sayısal YÜKSEK eşiklerinin hepsini geçiyor, ama üç sorun var: çoklu test düzeltmesinden sonra anlamlı değil, IS'te tek başına t<2, ve aşağıdaki kritik uyarı.
   - **Kritik uyarı:** 2026'da bu rejim hiç oluşmadı. rv20 ≈ %21, eşik ≈ %11,7. Kural şu an pasif.
3. **Oynaklık rejimine göre iki yönlü kural (VOLREG_5).** Sakin piyasada momentum, çalkantılı piyasada (oynaklık üst üçte birde) 5 günlük dönüş.
   - VİOP'ta h=5 drift çıkarılmış Sharpe 1,07 (t=3,33). IS 1,27, OOS 1,02, yılların 8/10'unda pozitif.
   - Ancak **çalkantı bacağı 2010–2016'da ters çalışıyor** (−0,27 ile −0,43). Birleşik kuralın erken dönem Sharpe'ı 0,16 (t=0,43).
   - 2026'da yalnızca bu güvenilmez bacak aktif. Etiket **DÜŞÜK**.
4. **Uç günlerin tersine işlem yapmak para kaybettiriyor.** RSI(2)<10 al/>90 sat, Bollinger(20,2) bandı dışında ters pozisyon, 2σ günden sonra ters işlem, 3+ günlük seriyi tersine çevirme ve 1 günlük dönüş kurallarının hepsi IS, OOS ve 2010–2016'da negatif. Örnekler:
   - Bollinger ters h=1: −0,67 (IS −0,98, OOS −0,52, erken −0,60).
   - 2σ ters h=1: −0,58 (IS −0,60, OOS −0,63, erken −0,51).
   - Bu kuralların tersi zayıf bir "kuyruk momentumu" veriyor. Bollinger kırılımı yönünde 1 günlük işlem: drift çıkarılmış 0,47 (t=1,46), erken dönem 0,39. Etiket DÜŞÜK; asıl etki aşağı yönlü kırılımlarda.
5. **Klasik trend kuralları rejime bağlı ve sağlam değil.** Fiyat>MA, MA kesişimleri, Donchian, 52 hafta zirvesi ve TSMOM işaret kurallarının hepsi aynı tabloyu veriyor: 2022–2026 boğa piyasasında OOS'ta iyi (örneğin fiyat>MA50 OOS 0,83), IS'te negatif (−0,33), 2010–2016'da sıfır civarı.
   - Ham Sharpe'larının büyük kısmı drift. Örnek: TSMOM_250 ham 0,17, drift çıkarılmış −0,07.
   - Karşılaştırma: VİOP vadelisini sürekli tutmanın (buy&hold) Sharpe'ı 0,49.
6. **Şunlarda ilişki yok (YOK):**
   - GVZ seviyesi ve değişimi, GVZ − gerçekleşen oynaklık farkı.
   - Gerçekleşen oynaklık seviyesi.
   - VİOP hacim şoku, açık pozisyon değişimi, fiyat×AP ve fiyat×hacim teyidi.
   - Uzlaşmanın gün aralığındaki yeri (temiz t-1 sürümü).
   - Uzlaşma−VWAP farkı.
   - 1–250 günlük ham getiriler. Hiçbiri tam dönemde |t|≥2 ve IS/OOS tutarlı değil.
7. **İleriye bakma tuzağı gösterildi.** Gün t'nin (uzlaşma − kapanış) farkı fwd1'i t=−2,92 ile "öngörüyor". Ama kapanış fiyatı uzlaşmadan **sonra** oluşuyor (15:15–15:20 UTC), yani bu mekanik bir ilişki. Temiz t-1 sürümünde t=0,14.
8. **VİOP vadelisi spot altının gerisinde kalıyor.** Taşıma maliyeti (contango) her roll'da ortalama 74 bps. Aynı dönemde vadeli buy&hold yılda %7,8, spot yılda %12,3 getirdi. Uzun ağırlıklı her stratejide bu fark kullanıcının cebinden çıkar.

---

## 1. Veri, zamanlama, bilgi zamanları

**Hedef.** `fwd{h}`, aktif kontratın aynı kontrat içindeki uzlaşma getirilerinin t+1..t+h toplamı (log). Roll ileriye bakmasız: önceki günün en büyük AP'si seçiliyor. Giriş, gün t uzlaşması (son 10 dakika VWAP, ≈15:05–15:15 UTC). **Karar anı 15:00 UTC.**

**Sinyal kaynakları:**

| Kod | Kaynak | Bilgi zamanı (UTC) | Temiz mi? |
|---|---|---|---|
| `spot` | Dukascopy XAUUSD BID, gün t 14:00–15:00 saatlik barının kapanışı (`s_p15`). Bütün fiyat dinamiği öznitelikleri (getiri, MA, RSI, BB, rv, seri, z) bu seriden. | gün t 15:00 | Evet. Uzlaşmadan 5–15 dakika önce. |
| `vt` | VİOP roll-ayarlı uzlaşma endeksi exp(Σ v_ret), gün t dahil | gün t 15:10 | **Hayır: "kapanışta hesaplanan".** Giriş fiyatıyla eş zamanlı, uygulanamaz; yalnız kıyas için. |
| `vt1` | Aynı seri, bir gün geri | gün t-1 15:15 | Evet (1 gün bayat) |
| `gvz` | `y__GVZ` (CBOE altın VIX), t-1 ABD kapanışı 16:15 ET | t-1 ≈20:15/21:15 | Evet |
| `mt` | VİOP gün t yüksek/düşük (önceki akşam seansı dahil), toplam hacim, toplam AP, kapanış, VWAP | gün t 15:15–15:20 ve gün sonu | **Hayır: cutoff sonrası** |
| `mt1` | Aynı değişkenler t-1 | gün t-1 | Evet |
| gün içi segmentler | Spot fiyatlar: p15(t-1)→p20(t-1), p20(t-1)→p07, p07→p13, p13→p15 | ≤ gün t 15:00 | Evet |
| `loc_s` | Spot (15:00 t-1, 15:00 t] saatlik yüksek/düşük aralığında p15'in yeri | gün t 15:00 | Evet |

**Ek kontroller:**
- Spot öznitelikler spot takviminde hesaplandı. VİOP günlerine as-of taşındı (en fazla 1 gün ileri doldurma).
- rv20'nin yüzdeliği (`rvq`) 2010'dan itibaren genişleyen pencereyle ve yalnızca geçmiş bilgiyle hesaplandı.
- **Placebo:** Ana sinyal (ret5, düşük oynaklık) bir gün eskiye kaydırıldığında IC 0,117'den 0,075'e iniyor, sonra 0,049 ve 0,057. Kademeli bir düşüş bu; ileriye bakma izi yok. Bir gün geleceğe kaydırıldığında 0,46 (beklendiği gibi). Tablo T17.

## 2. Yöntem

- **IC:** Spearman sıra korelasyonu. NW-HAC t (lag = max(h,5)). Tam dönem, IS (2017-03..2021-12), OOS (2022-01..2026-11) ve yıl yıl işaret tutarlılığı (`lib_altin.split_stats`).
- **Erken OOS:** Aynı öznitelik spot panelde. Hedef `sfwd{h}` (15:00→15:00 UTC spot), dönem 2010–2016.
- **Backtest:** `lib_altin.backtest`. Kademeli h alt portföy kullanılıyor, aynı yöndeki yenilemeler netleşiyor. Temel maliyet 5 bps gidiş-dönüş, stres 10 bps.
  - "Katı" maliyet: her alt portföy h günde kapatılıp yeniden açılır, netleşme yok (`strict5dm_oos`).
  - Her strateji için ham Sharpe, drift çıkarılmış Sharpe, uzun ve kısa bacak ayrı, VİOP buy&hold karşılaştırması (Sharpe 0,49) ve erken spot kopyası raporlandı.
- **Parametre seçimi yalnız IS'te yapıldı** (T7 ve T8). Her aile ve h için IS'te en yüksek |t| ya da en yüksek drift çıkarılmış Sharpe seçildi; OOS bir kez okundu.
- **Izgara:**
  - (a) k ∈ {1,2,3,5,10,20,60,120,250}, ham ve oynaklık ölçekli.
  - (b) Fiyat>MA{20,50,100,200}; kesişimler 5/20, 10/50, 20/100, 50/200; Donchian 20/55 olay ve durum; 52 hafta uzaklığı.
  - (c) RSI2, RSI14 (sürekli ve uç: <10/>90, <30/>70); BB z(20,2) sürekli ve |z|>2; seri sayısı ve ±3; z=r/σ20 ve >2σ / <−2σ ayrı.
  - (d) rv5/20/60, log(rv5/rv60), GVZ seviyesi, ΔGVZ 1 ve 5 gün, GVZ−rv20; oynaklık tercillerine koşullu ret1/5/20.
  - (e) Uzlaşmanın gün aralığındaki yeri (VİOP ve spot), hacim şoku, Δlog toplam AP, işaret×AP ve işaret×hacim.
  - (f) Uzlaşma−kapanış, uzlaşma−VWAP.
  - (g) Gün içi 4 segment.
- **Kayıt:** Her test `register(agent='a1_zaman_serisi')` ile `out/registry/a1_zaman_serisi.csv` dosyasına yazıldı.

## 3. Aile sonuçları

### (a) Geçmiş getiriler ve TSMOM — YOK
- Spot sinyalli 54 IC testinin hiçbiri hem IS hem OOS'ta |t|≥2 değil. En büyük |t| 2,29 (vsr250, h=1), ama yıllarda aynı işaret yalnız 3/10. Erken dönemdeki işaretler karışık (T2).
- **TSMOM işaret backtestleri (T5)** sıfır civarında.
  - TSMOM_60 h=1: drift çıkarılmış 0,31 (IS 0,21, OOS 0,38).
  - TSMOM_120 h=3: 0,24 (IS 0,05).
  - TSMOM_250: −0,07.
- **IS seçimi:** h=1 için ret2 (IS t=2,09) seçildi; OOS t=0,05. h=3 ve h=5 için seçilen ret5 ve ret3 OOS'ta işaret değiştirdi (T7).
- **Kısa dönüş (−sign(r1)) h=1:** drift çıkarılmış −0,64, IS −1,21, OOS −0,26, erken −0,44. Yıllık devir 249 ve 5 bps ile yılda ≈%6 maliyet. Yön sinyali de zaten ters.

### (b) MA, kesişim, Donchian, 52 hafta — DÜŞÜK (rejime bağlı)
Kurallar 2022–2026 boğa piyasasında OOS'ta iyi, IS'te kötü, erken dönemde sıfır:

| Kural | h | Ham Sh | Drift çık. Sh | IS | OOS | Erken spot |
|---|---|---|---|---|---|---|
| Fiyat>MA50 | 1 | 0,42 | 0,34 | −0,33 | 0,83 | 0,16 |
| MA20/100 kesişimi | 5 | 0,57 | 0,39 | −0,17 | 0,77 | −0,24 |
| Donchian55 durum | 1 | 0,24 | 0,03 | −0,74 | 0,58 | −0,28 |
| MA50/200 | 1 | 0,25 | 0,02 | 0,09 | −0,03 | −0,04 |
| 52 hafta zirvesine ≤%2 → uzun | 1 | 0,68 | 0,47 | 0,20 | 0,65 | −0,11 |

Uzun bacak ham Sharpe'ları buy&hold'a (0,49) yakın. Drift çıkarılınca istikrarlı katkı kalmıyor. IS seçimiyle seçilen dbrk20 ve dst55 OOS'ta anlamsız ya da işaret değiştiriyor (T7).

### (c) Kısa vadeli dönüş — YOK (tersi zayıf momentum)
Bütün "uç noktayı sat, dibi al" kuralları negatif (T5):

| Kural | h | Drift çık. tam | IS | OOS | Erken | Pozitif yıl |
|---|---|---|---|---|---|---|
| BB(20,2) tersine | 1 | −0,67 | −0,98 | −0,52 | −0,60 | 1/10 |
| 2σ gün sonrası ters | 1 | −0,58 | −0,60 | −0,63 | −0,51 | 2/10 |
| RSI2 Connors (MA200 filtreli) | 1 | −0,40 | −0,44 | −0,38 | 0,06 | 2/10 |
| RSI2 <10 al / >90 sat | 1 | −0,38 | −0,80 | −0,10 | −0,24 | 3/10 |
| 3+ gün serisini tersine | 3 | −0,55 | −0,50 | −0,59 | 0,08 | 0/10 |

**Kuyruk momentumu.** Yön IS'ten alındı: IS'te tersine işlem negatif çıktığı için hareket yönünde pozisyon alındı (T6, T8).
- **BB kırılım yönünde, h=1:** ham 0,51, drift çıkarılmış 0,47 (t=1,46), IS 0,75, OOS 0,34 (net 0,40, 10 bps ile 0,25). Pozitif yıl 8/10. Erken 0,39 (t=1,05).
- **Bacaklar:** Aşağı kırılım sonrası kısa pozisyon daha sağlam: OOS 0,45, erken 0,65. Yukarı kırılım sonrası uzun pozisyon OOS 0,11, erken −0,29.
- **2σ eşiği** 1,5/2/2,5 varyantlarında h=1'de 0,09–0,29. Kenar küçük ve yalnız aynı gün bilgisiyle var: t-1 sürümü 0,08 (`TAILMOM_bb2.0_vt1`).
- **Karar:** DÜŞÜK. Pratik ders olarak tersine işlem yapmamak gerekiyor.

### (d) Oynaklık rejimi — LOWMOM ORTA, VOLREG DÜŞÜK, GVZ YOK
- **Seviye olarak oynaklığın yönle ilişkisi yok.** rv5/20/60, GVZ, ΔGVZ ve GVZ−rv20'de |t| en fazla 1,8. GVZ'nin altın yönünü öngördüğüne dair kanıt yok. Bu literatürle uyumlu.
- **Koşullu momentum ve dönüş çarpıcı biçimde tutarlı** (T3, d_vol satırları):
  - Düşük oynaklık tercilinde ret1, ret5 ve ret20'nin hepsi pozitif ve 9 testin hepsinde t>1,6. Örnek: ret5_loV h=1 IC 0,117, t=3,45 (IS 2,38, OOS 2,68).
  - Yüksek oynaklık tercilinde 9 testin 8'i negatif. Örnek: ret5_hiV h=5 t=−2,88 (IS −3,03, OOS −1,83).
  - Erken dönemde düşük oynaklık testleri pozitif (t≈0–1,0). Yüksek oynaklık testleri negatif (t −0,2 ile −1,8), yani sıra korelasyonu dönüşle uyumlu.
  - Ama işarete dayalı backtest 2010–16'da negatif. Büyük hareketlerin devam ettiği birkaç gün (ör. Nisan 2013) dönüş kârını siliyor.
- **Backtestler (T6, T9–T13):** Ayrıntı bölüm 4'te.
  - Sakin piyasa bacağı (LOWMOM) üç dönemde de pozitif: spot 2010–16 0,51–0,58, 2017–21 0,43–0,79, 2022–26 1,22–1,35.
  - Çalkantı bacağı (HIGHVOL_REV) 2017–21'de iyi (1,30–1,37), 2022–26'da zayıf (0,40–0,46), 2010–16'da ters (−0,27 ile −0,43).
  - Birleşik VOLREG_5'in komşuluk duyarlılığı:
    - Oynaklık penceresi, tercil eşiği ve yüzdelik penceresi değiştiğinde sağlam: 0,64–1,11.
    - k'ye duyarlı: h=5'te k=3 → 0,75, k=5 → 1,07, k=10 → 0,09.

### (e) VİOP mikro yapı — YOK
- **Hacim, AP ve teyit sinyalleri:** Hacim şoku, Δlog(toplam AP), işaret×AP ve işaret×hacim, hem gün t hem t-1 sürümünde |t|≤1,49. IS'te tek tük |t|>2 var (doi_mt h=1 −2,31); OOS'ta işaret dönüyor.
- **Uzlaşmanın gün aralığındaki yeri (loc_v):** t-1 sürümünde IS ve OOS işaretleri tutarsız. Dikkat: 18.09.2020 sonrası VİOP yüksek/düşük değerleri önceki akşam seansını da kapsıyor.
- **Temiz spot karşılığı (loc_s):** h=1 t=2,09 (IS 2,46, OOS 0,65). Erken dönem −0,64; spot hedefle dönemlere bölündüğünde 2010–16'da −0,64, 2017–21'de 1,94, 2022–26'da 0,48 (T18). Karar: DÜŞÜK / istikrarsız.

### (f) Uzlaşma−kapanış ve uzlaşma−VWAP — YOK (temiz sürümde)
- **sc (gün t):** h=1 IC −0,068, t=−2,92. Kapanış uzlaşmadan sonra oluştuğu için bu sinyal t+1 getirisinin ilk 5–10 dakikasını içeriyor; mekanik bir ilişki, işlem yapılamaz. t-1 sürümünde t=0,14; placebo s=+1'de IC 0,003 (T17).
- **svw (uzlaşma−VWAP):** Hiçbir sürümde istikrarlı değil.

### (g) Gün içi segmentler — DÜŞÜK
- **Son iki saat (13→15 UTC):** fwd'yi pozitif öngörüyor (h=1 t=2,49, IS 2,40, OOS 1,19). Ama 2010–2016'da işaret ters (t=−1,84). Spot hedefle de aynı tablo çıkıyor (T18). Yani mesele hedef tanımı değil, dönem.
- **Diğer segmentler** (ABD öğleden sonra, Asya gecesi, Avrupa sabahı) anlamsız ya da OOS'ta işaret değiştiriyor.

## 4. Öne çıkan sinyal: sakin piyasa momentumu (LOWMOM_k5)

**Kural.** Hesap gün t 15:00 UTC'de (TSİ 18:00) Dukascopy/benzeri spot XAUUSD fiyatıyla yapılıyor:
- x = ln(P15_t / P15_{t−5}), yani son 5 iş gününün getirisi.
- rv20 = son 20 günlük ln P15 farklarının standart sapması.
- q = rv20'nin 2010'dan bugüne genişleyen yüzdeliği (bugün dahil).
- **q < 1/3 ise** gün t VİOP uzlaşmasında (18:05–18:15 TSİ VWAP penceresi) **sign(x)** yönünde 1 kontrat açılır ve t+h uzlaşmasında kapatılır. q ≥ 1/3 ise pozisyon yok.
- Bugünkü eşik rv20 ≈ yıllık %11,7 (IS sonu %11,4, 2016 sonu %12,7; istikrarlı).

| Metrik | h=1 | h=3 | h=5 |
|---|---|---|---|
| Ham net Sharpe, tam | 1,03 | 0,94 | 1,02 |
| Drift çıkarılmış net Sharpe, tam (t) | 0,99 (3,06) | 0,89 (2,75) | 0,95 (2,96) |
| IS drift çıkarılmış (t) | 0,82 (1,79) | 0,58 (1,28) | 0,55 (1,20) |
| OOS drift çıkarılmış (t) | 1,31 (2,88) | 1,40 (3,09) | 1,63 (3,58) |
| OOS ham net Sharpe 5 bps / drift çık. 10 bps | 1,36 / 1,19 | 1,46 / 1,32 | 1,69 / 1,56 |
| OOS katı maliyet (netleşmesiz, drift çık.) | 0,95 | 1,30 | 1,57 |
| OOS yıllık getiri (net) | %7,95 | %7,16 | %7,49 |
| Ortalama maruziyet / yıllık devir | 0,41 / 43 | 0,33 / 29 | 0,29 / 22 |
| Pozitif yıl (aktif yıllar) | 7/9 | 7/9 | 7/9 |
| OOS uzun / kısa bacak (drift çık.) | 0,84 / 1,04 | 0,80 / 1,07 | 0,97 / 1,10 |
| Erken spot 2010–16 drift çık. (t) | 0,51 (1,38) | 0,57 (1,53) | 0,58 (1,56) |
| Spot 2010–2026 tamamı (t) | 0,80 (3,34) | 0,73 (3,02) | 0,71 (2,94) |
| IC: ret5 (düşük oynaklık) tam / IS / OOS t | 3,45 / 2,38 / 2,68 | 2,53 / 1,03 / 3,04 | 2,51 / 0,64 / 3,64 |

**Yıllık sonuçlar** (VİOP, h=5, drift çıkarılmış):
- 2017: 1,59. 2018: −1,65. 2019: −0,15. 2020: 2,68. 2021: 0,31. 2022: 1,15. 2023: 1,00. 2024: 2,12. 2025: 2,39.
- 2026'da aktif gün yok.
- Spot verisinde 2011–2025 arasında 15 yılın 13'ünde pozitif (h=5). Negatif yıllar 2018 ve 2019.

**Sağlamlık (T9).** Aşağıdaki varyantların hepsinde sonuç pozitif kaldı:
- k=1/3/10/20 (h=5): 0,98 / 0,75 / 0,51 / 0,47. k=5 IS'te seçildi.
- VİOP uzlaşma getirisiyle: gün t (kapanışta hesaplanan) 0,75; gün t-1 (temiz) 0,52 (OOS 1,06).
- Roll günü ±1 dışlanınca 0,83.
- Mart–Nisan 2020 ve Ocak–Mart 2026 dışlanınca 0,98. Bu dönemler zaten yüksek oynaklık rejiminde.
- Getiri %1–99 winsorize edilince 0,93.
- Sürekli sinyal z=x/(σ√5), [−1,1] aralığına kırpılmış: 0,84.
- Düşük likidite günleri dışlanınca (VİOP hacmi 250 günlük %10'luk dilimin altında): IC ret5_loV h=1 t=3,48; VOLREG_5 h=5 0,98.
- Akşam seansı öncesi ve sonrası: VOLREG_5'te 1,19 / 1,03.

**Mekanizma (olası).** Sakin rejimde fiyatı yavaş ve kalıcı akışlar sürüklüyor: merkez bankası ve ETF alımları, trend takipçisi (CTA) pozisyon artırımı. Haberlere tepki de eksik kalıyor; bu yüzden 1–5 günlük devam etkisi çıkıyor. Çalkantılı rejimde ise likidite sağlayıcılar ve aşırı tepki öne geçiyor; hisse senetlerinde kısa vadeli dönüş kazancının oynaklıkla arttığı biliniyor (Nagel 2012). Ancak bu ikinci kısım altında 2010–2016'da tutmuyor.

**Neden YÜKSEK değil:**
1. Bu ajanın 918 birincil testi içinde BH-FDR q=0,30.
2. IS'te backtest t<2: 1,79 / 1,28 / 1,20.
3. IC'de yılların yalnız 6/9'u aynı işarette (h=1).
4. Erken dönem anlamlı değil (t≈1,4–1,6).
5. **2026'da rejim hiç oluşmadı, kural şu an pasif.** Gerçekleşen oynaklık %21 civarında. 2026'nın en düşük rv20 değeri %14,9 ve bu bile eşiğin üstünde.

## 5. Sağlamlık kontrolleri (zorunlu madde 7)

- **Roll günleri:** 61 roll var. v_ret aynı kontrat içinde hesaplandığı için fiyat sıçraması yok. Roll ±1 gün ya da t..t+h penceresi roll içeriyorsa dışlandı (T15, T16). Ana bulgular değişmiyor; LOWMOM h=5 sonucu 0,95'ten 0,83'e iniyor.
- **Sıfır hacim:** Hiç sıfır hacimli gün yok. 7 günde v_ret=0. Hacmi 250 günlük %10'luk dilimin altında kalan günler dışlandı: IC ret5_loV h=1 t=3,45'ten 3,48'e çıkıyor, VOLREG_5 h=5 1,07'den 0,98'e iniyor.
- **Uç değerler:** Mart–Nisan 2020 ve Ocak–Mart 2026 dışlandı (2026'da tek günde −%8,1 ve −%7,8 var). Tail-momentum h=1 0,47'den 0,66'ya çıkıyor; LOWMOM değişmiyor; trend kurallarında fark küçük.
- **Akşam seansı kırılması (18.09.2020):** BB kuyruk momentumu öncesinde 1,08, sonrasında 0,29 (zayıflıyor). VOLREG her iki alt dönemde pozitif (1,19–1,25 ve 0,61–1,03).
- **Kaynak kıyası (spot 15:00 / VİOP t / VİOP t-1):** Kısa vadeli sinyallerde VİOP-t ile spot sonuçları birbirine yakın. Bu, uzlaşma serisinde sistematik bir bid-ask sıçraması olmadığını gösteriyor (r1 placebo IC'leri ±0,03). t-1 sürümlerinde kısa vadeli kenar kayboluyor (tail-momentum), LOWMOM'da yarıya iniyor.
- **İleriye bakma:** placebo_lead yukarıda; sc (uzlaşma−kapanış) gün t örneği bölüm 3(f)'de.

## 6. Çoklu test

- **Kayıt:** `out/registry/a1_zaman_serisi.csv`, 984 satır.
- **Aileler:**
  - IC testleri: a_mom 132, b_trend 78, c_rev 135, d_vol 54, e_micro 33, f_settle 12, g_intraday 12. Erken dönem kopyaları 195.
  - Backtestler: 159, erken dönem kopyaları 108.
  - Sağlamlık (robust_*): 66.
- **Sonuçlar:** p<0,05 olan 102 test; |t|≥3 olan 18 test. Birincil testlerde en küçük BH q=0,30. Global FDR bu kayıttan yapılmalı.
- En iyi 12 test `registry_summary.json` dosyasında. Hepsi ya düşük oynaklık momentumu / VOLREG ailesinden ya da ileriye bakan sc testinden.

## 7. Uygulama notları (kullanıcı için)

- **Hesap ve emir saati.** Sinyal 18:00 TSİ'de (15:00 UTC) spot fiyatla hesaplanıyor. Emir uzlaşma penceresinde (18:05–18:15 TSİ) VWAP'a yakın verilmeli. Kapanıştan kapanışa kontrol edilecekse aynı pencerede çıkılmalı.
- **Maliyet.** Gidiş-dönüş 5 bps varsayıldı. Perakende komisyonu (on binde 10 + BSMV) ile gidiş-dönüş ≈22–25 bps olur (r2 raporu). Bu durumda yüksek devirli kurallar açıkça negatife döner; örneğin 1 günlük dönüşün yıllık devri 249. LOWMOM h=1'in devri 43; 25 bps ile yılda ≈%5,4 maliyet, brüt ≈%9 getirinin yarısından fazlası. LOWMOM h=5'in devri ≈22; yılda ≈%2,8 maliyet, OOS net getirinin (%7,5) yaklaşık üçte biri.
- **Contango.** VİOP uzun pozisyonu spot altına göre yılda ≈%4,5 geride kalıyor (roll başına ≈74 bps). Bu yüzden uzun ağırlıklı trend kurallarının VİOP'taki ham Sharpe'ı spot'tan düşük.
- **Pozisyon boyutu.** Oynaklık, yön değil boyut aracı. Oynaklık hedefleme (TSMOM_20_VT10) Sharpe'ı iyileştirmedi (OOS 0,51, IS −0,21).

## 8. Dosyalar

- `a1_feats.py`: Öznitelikler (bilgi zamanları başlıkta).
- `a1_main.py`: IC testleri (456 + 195 erken) ve klasik backtestler (87 + 87 erken), placebo.
- `a1_deep.py`: Kuyruk momentumu, VOLREG, sağlamlık, gün içi segmentlerin spot hedefle kıyası.
- `a1_volreg.py`: VOLREG komşuluk duyarlılığı, bacak × dönem analizi.
- `a1_final.py`: LOWMOM sağlamlığı, placebo, yıllık tablolar, BH özeti, güncel durum (`lowmom_current.json`).
- `a1_tables.py`: Tablo üretimi (`tables.md`).
- `run_all.sh`: Hepsini sırayla çalıştırır.
- **Çıktılar:**
  - `ic_results.csv`, `bt_results.csv`, `bt2_results.csv`
  - `is_secim.csv`, `is_secim2.csv`
  - `robust_ic.csv`, `robust_bt.csv`
  - `lowmom_robust.csv`, `lowmom_spot_by_year.csv`
  - `volreg_sensitivity.csv`, `volreg_spot_periods.csv`, `volreg_regime_share.csv`
  - `placebo.csv`, `placebo_lowmom.csv`, `seg_spot_target.csv`
  - `buyhold.json`, `registry_summary.json`

---

## Ek: tüm tablolar (otomatik, `a1_tables.py`)
### T1. IC testleri aile × kaynak özeti (h=1,3,5 birlikte)
| fam | src | test | t2 | is_oos_t2 | maks_t |
|---|---|---|---|---|---|
| a_mom | spot | 54 | 2.00 | 0.00 | 2.29 |
| a_mom | vt | 54 | 3.00 | 0.00 | 2.57 |
| a_mom | vt1 | 24 | 0.00 | 0.00 | 1.12 |
| b_trend | spot | 39 | 1.00 | 0.00 | 2.27 |
| b_trend | vt | 39 | 4 | 0.00 | 2.56 |
| c_rev | spot | 45 | 5 | 0.00 | 2.59 |
| c_rev | vt | 45 | 5 | 0.00 | 2.55 |
| c_rev | vt1 | 45 | 2.00 | 0.00 | 2.93 |
| d_vol | gvz | 12 | 0.00 | 0.00 | 1.74 |
| d_vol | spot | 30 | 9 | 1.00 | 3.45 |
| d_vol | vt | 12 | 0.00 | 0.00 | 1.15 |
| e_micro | mt | 15 | 0.00 | 0.00 | 1.49 |
| e_micro | mt1 | 15 | 0.00 | 0.00 | 1.42 |
| e_micro | spot | 3.00 | 2.00 | 0.00 | 2.14 |
| f_settle | mt | 6 | 1.00 | 0.00 | 2.92 |
| f_settle | mt1 | 6 | 0.00 | 0.00 | 1.08 |
| g_intraday | spot | 12 | 3.00 | 0.00 | 2.49 |

### T2. (a) Geçmiş getiri → fwd: NW t (spot 15:00 UTC sinyal, VİOP hedef); t_e = erken spot 2010-2016
| feat | t_h1 | t_h3 | t_h5 | t_e_h1 | t_e_h3 | t_e_h5 |
|---|---|---|---|---|---|---|
| ret1 | 1.16 | 1.45 | 0.22 | -0.67 | -0.66 | 0.20 |
| ret2 | 1.31 | 0.60 | -0.64 | -0.43 | -0.52 | 0.20 |
| ret3 | 1.72 | 0.13 | -0.73 | -0.73 | -0.10 | 0.31 |
| ret5 | 0.48 | -0.22 | -0.41 | -0.13 | 0.44 | 0.57 |
| ret10 | 0.30 | 0.56 | 0.66 | -0.17 | 0.24 | 0.10 |
| ret20 | 0.52 | 0.36 | -0.02 | -0.63 | -0.37 | -0.43 |
| ret60 | 1.06 | 0.53 | 0.21 | -0.08 | -0.16 | -0.38 |
| ret120 | 1.66 | 1.25 | 1.21 | 0.58 | 0.54 | 0.34 |
| ret250 | 1.69 | 1.17 | 1.28 | 0.58 | -0.06 | -0.21 |
| vsr1 | 1.72 | 1.88 | 0.81 | -0.59 | -0.61 | 0.10 |
| vsr2 | 1.61 | 1.14 | -0.03 | -0.08 | -0.36 | 0.37 |
| vsr3 | 1.86 | 0.61 | -0.12 | -0.50 | 0.05 | 0.43 |
| vsr5 | 1.07 | 0.31 | 0.23 | 0.27 | 0.64 | 0.82 |
| vsr10 | 0.58 | 0.55 | 0.70 | 0.17 | 0.57 | 0.50 |
| vsr20 | 1.04 | 0.62 | 0.25 | -0.32 | -0.13 | -0.27 |
| vsr60 | 1.34 | 0.65 | 0.34 | 0.50 | 0.33 | 0.16 |
| vsr120 | 2.05 | 1.50 | 1.50 | 1.06 | 0.89 | 0.69 |
| vsr250 | 2.29 | 1.80 | 1.87 | 0.81 | 0.11 | -0.04 |

### T3. (b)(c)(d)(g) spot sinyaller: NW t tam / IS / OOS / erken
| fam | feat | t_h1 | t_is_h1 | t_oos_h1 | t_e_h1 | t_h5 | t_is_h5 | t_oos_h5 | t_e_h5 |
|---|---|---|---|---|---|---|---|---|---|
| b_trend | d52 | 1.92 | -0.05 | 2.28 | -0.23 | 1.34 | -1.19 | 2.24 | -0.89 |
| b_trend | dbrk20 | 1.49 | 1.07 | 1.02 | 0.05 | -0.09 | -0.71 | 0.39 | 0.41 |
| b_trend | dbrk55 | 2.27 | 0.95 | 2.11 | 1.39 | 0.94 | 0.10 | 1.05 | 1.15 |
| b_trend | dst20 | 0.88 | 0.24 | 0.90 | 0.12 | 0.66 | 0.29 | 0.55 | -0.38 |
| b_trend | dst55 | 0.96 | -1.06 | 2.27 | -0.77 | 0.51 | -1.60 | 1.94 | -1.66 |
| b_trend | pma100 | 1.08 | -0.05 | 1.42 | 0.96 | 1.10 | -0.68 | 1.91 | 0.04 |
| b_trend | pma20 | 0.62 | -0.27 | 1.02 | -0.09 | 0.67 | -0.25 | 1.03 | 0.30 |
| b_trend | pma200 | 0.66 | 0.09 | 0.86 | 0.55 | -0.07 | -1.22 | 0.86 | 0.12 |
| b_trend | pma50 | 1.82 | -0.18 | 2.60 | 0.63 | 1.57 | -0.31 | 2.26 | 0.55 |
| b_trend | x10_50 | 0.97 | -0.43 | 1.57 | 0.61 | 1.43 | -0.03 | 1.75 | 0.62 |
| b_trend | x20_100 | 1.75 | 0.14 | 2.18 | -0.15 | 1.80 | -0.56 | 2.79 | -1.03 |
| b_trend | x50_200 | 0.74 | 0.84 | 0.24 | 0.41 | 0.16 | 0.30 | -0.08 | -0.54 |
| b_trend | x5_20 | 1.23 | 0.15 | 1.51 | 0.41 | 0.73 | 0.04 | 0.89 | -0.03 |
| c_rev | bb_hi | 2.26 | 2.00 | 1.29 | -0.57 | 1.62 | 0.90 | 1.20 | -0.49 |
| c_rev | bb_lo | -1.79 | -1.63 | -1.06 | -2.24 | 1.05 | 1.44 | -0.01 | -0.68 |
| c_rev | bbz | 1.36 | 0.26 | 1.55 | 0.14 | 0.43 | -0.89 | 1.25 | 0.14 |
| c_rev | dn2s | -0.59 | -0.25 | -0.65 | -1.47 | 0.05 | 1.03 | -0.78 | -1.51 |
| c_rev | dn3 | -2.15 | -1.34 | -1.68 | 1.66 | -1.34 | -0.71 | -1.07 | 0.38 |
| c_rev | rsi14 | 1.43 | 0.09 | 1.80 | -0.12 | 0.93 | -0.62 | 1.61 | 0.01 |
| c_rev | rsi14_hi | 2.10 | 0.55 | 2.20 | -0.27 | 0.73 | 0.12 | 0.73 | 0.76 |
| c_rev | rsi14_lo | 0.61 | 0.29 | 0.59 | -0.15 | 2.01 | 1.30 | 1.53 | -0.12 |
| c_rev | rsi2 | 1.42 | 1.31 | 0.69 | -0.40 | 0.06 | -1.26 | 1.19 | 0.28 |
| c_rev | rsi2_hi | 0.43 | 0.91 | -0.28 | -0.57 | 0.74 | 0.05 | 0.82 | -0.77 |
| c_rev | rsi2_lo | -1.46 | -0.92 | -1.19 | 0.22 | 0.93 | 1.21 | 0.23 | -0.11 |
| c_rev | streak | 1.09 | 1.77 | -0.14 | -1.04 | 0.48 | -0.05 | 0.68 | -0.67 |
| c_rev | up2s | 1.07 | 1.37 | 0.38 | -0.19 | 0.89 | -0.03 | 1.13 | -0.83 |
| c_rev | up3 | 0.14 | 0.44 | -0.22 | -0.12 | 0.11 | -0.75 | 0.89 | -1.01 |
| c_rev | z1 | 1.72 | 2.23 | 0.26 | -0.58 | 0.81 | 0.27 | 0.85 | 0.13 |
| d_vol | dlrv | 1.82 | 0.23 | 2.17 | 0.57 | 0.61 | -0.21 | 0.88 | 0.51 |
| d_vol | ret1_hiV | -0.22 | 1.77 | -1.15 | -1.52 | -1.24 | -1.21 | -0.72 | -1.14 |
| d_vol | ret1_loV | 2.74 | 2.25 | 1.56 | 0.53 | 3.10 | 1.99 | 2.63 | 0.54 |
| d_vol | ret20_hiV | -0.93 | -1.70 | -0.21 | -1.16 | -1.31 | -1.90 | -0.67 | -1.37 |
| d_vol | ret20_loV | 2.49 | 1.48 | 2.09 | 1.01 | 1.65 | 0.73 | 1.74 | -0.01 |
| d_vol | ret5_hiV | -1.19 | -1.74 | -0.40 | -1.09 | -2.88 | -3.03 | -1.83 | -0.35 |
| d_vol | ret5_loV | 3.45 | 2.38 | 2.68 | 0.97 | 2.51 | 0.64 | 3.64 | 0.98 |
| d_vol | rv20 | 0.46 | 0.28 | -0.22 | 1.38 | -0.42 | -0.57 | -0.74 | 1.23 |
| d_vol | rv5 | 1.31 | 0.75 | 0.81 | 0.57 | 0.21 | 0.15 | -0.25 | 0.16 |
| d_vol | rv60 | 0.02 | 0.83 | -1.40 | 0.56 | -0.33 | 0.60 | -1.60 | 0.43 |
| e_micro | loc_s | 2.09 | 2.46 | 0.65 | -0.64 | 1.82 | 0.33 | 2.06 | 1.00 |
| g_intraday | segA_15p_20p | -1.02 | 1.17 | -2.30 | 0.30 | -1.12 | 0.58 | -1.88 | -0.68 |
| g_intraday | segB_20p_07 | 1.31 | 0.83 | 0.97 | -1.27 | -0.16 | -0.37 | -0.01 | 0.07 |
| g_intraday | segC_07_13 | -0.49 | -0.41 | -0.28 | 0.60 | -0.59 | -2.35 | 1.11 | 0.16 |
| g_intraday | segD_13_15 | 2.49 | 2.40 | 1.19 | -1.84 | 2.45 | 0.63 | 2.57 | -0.24 |

### T4. (d) GVZ ve (e)(f) VİOP mikro yapı: mt = gün t (cutoff SONRASI), mt1 = gün t-1 (temiz)
| feat | src | t_h1 | t_h3 | t_h5 | t_is_h1 | t_is_h3 | t_is_h5 | t_oos_h1 | t_oos_h3 | t_oos_h5 |
|---|---|---|---|---|---|---|---|---|---|---|
| dgvz | gvz | 0.52 | 0.85 | 0.94 | 0.73 | -0.29 | -0.25 | 0.13 | 1.41 | 1.47 |
| dgvz5 | gvz | 1.74 | 0.87 | 0.51 | -0.08 | -0.12 | -0.05 | 2.38 | 1.20 | 0.67 |
| doi | mt | -0.80 | -0.59 | -0.50 | -2.31 | -2.13 | -1.80 | 0.92 | 1.35 | 1.15 |
| doi | mt1 | -0.43 | -0.36 | 0.87 | -0.47 | -0.87 | 0.12 | -0.00 | 0.55 | 1.26 |
| gvz | gvz | 0.31 | -0.50 | -0.65 | 0.29 | -0.38 | -0.31 | -0.66 | -1.06 | -1.45 |
| loc_v | mt | 0.78 | 1.34 | 1.49 | 2.03 | 0.82 | -0.02 | -0.56 | 1.09 | 1.89 |
| loc_v | mt1 | 1.00 | 1.42 | 0.60 | 0.71 | -0.29 | -1.61 | 0.66 | 2.15 | 2.08 |
| pv_conf | mt | 0.32 | 0.32 | 0.23 | 0.85 | 0.86 | 0.62 | -0.56 | -0.77 | -0.51 |
| pv_conf | mt1 | 0.91 | -0.79 | -0.77 | 0.46 | -0.19 | -0.81 | 0.64 | -1.21 | -0.39 |
| sc | mt | -2.92 | -1.14 | -1.21 | -2.75 | -1.06 | -1.06 | -1.69 | -0.66 | -0.55 |
| sc | mt1 | 0.14 | -0.14 | 0.62 | -0.48 | -0.29 | -0.12 | 0.67 | 0.13 | 1.08 |
| svw | mt | 1.02 | 0.99 | 1.59 | 2.07 | 0.42 | -0.24 | -0.27 | 0.86 | 2.04 |
| svw | mt1 | 0.31 | 1.08 | 0.36 | 0.48 | -0.28 | -1.80 | -0.12 | 1.47 | 1.79 |
| vrp | gvz | -0.45 | -0.59 | -0.56 | -0.53 | -0.60 | -0.18 | -0.14 | -0.25 | -0.50 |
| vs_conf | mt | -1.19 | 1.11 | -0.08 | -2.03 | -0.30 | -1.32 | 0.10 | 1.41 | 0.65 |
| vs_conf | mt1 | 1.17 | 1.35 | 0.64 | 1.41 | 0.81 | -0.23 | 0.08 | 0.91 | 0.70 |
| vshock | mt | -0.06 | -0.15 | -0.41 | -0.83 | -1.21 | -0.86 | 0.56 | 0.77 | 0.23 |
| vshock | mt1 | 0.12 | 0.17 | 0.38 | -0.65 | -0.82 | -0.30 | 0.76 | 0.89 | 0.84 |

### T5. Klasik kurallar backtest (spot 15:00 sinyal → VİOP uzlaşma, 5 bps, kademeli). shdm = drift çıkarılmış Sharpe; early = spot 2010-2016
| strat | h | sh_full | shdm_full | shdm_is | shdm_oos | sh_oos | shdm_oos_10 | long_shdm_oos | short_shdm_oos | expo | turn | t_dm_full | yrs_pos_dm | early_shdm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TSMOM_1 | 1 | -0.11 | -0.15 | 0.27 | -0.43 | -0.39 | -0.78 | -0.28 | -0.34 | 1.00 | 249.20 | -0.45 | 4/10 | -0.32 |
| TSMOM_1 | 3 | 0.31 | 0.25 | 0.54 | 0.01 | 0.08 | -0.19 | 0.01 | -0.00 | 0.50 | 82 | 0.77 | 8/10 | -0.42 |
| TSMOM_1 | 5 | 0.17 | 0.10 | 0.13 | 0.10 | 0.19 | -0.04 | 0.06 | 0.03 | 0.38 | 49.20 | 0.30 | 7/10 | -0.26 |
| TSMOM_2 | 1 | 0.19 | 0.15 | 0.46 | -0.06 | -0.01 | -0.30 | -0.03 | -0.06 | 1.00 | 168.60 | 0.46 | 4/10 | -0.05 |
| TSMOM_2 | 3 | 0.15 | 0.10 | -0.09 | 0.21 | 0.29 | 0.06 | 0.13 | 0.13 | 0.61 | 83.40 | 0.30 | 7/10 | -0.18 |
| TSMOM_2 | 5 | 0.12 | 0.06 | -0.46 | 0.39 | 0.47 | 0.28 | 0.21 | 0.22 | 0.47 | 51.10 | 0.17 | 6/10 | 0.08 |
| TSMOM_3 | 1 | 0.37 | 0.33 | 0.28 | 0.38 | 0.44 | 0.20 | 0.27 | 0.27 | 1.00 | 133.30 | 1.02 | 6/10 | 0.03 |
| TSMOM_3 | 3 | 0.11 | 0.05 | -0.49 | 0.42 | 0.49 | 0.28 | 0.25 | 0.27 | 0.69 | 83.10 | 0.16 | 5/10 | -0.04 |
| TSMOM_3 | 5 | -0.09 | -0.15 | -0.77 | 0.24 | 0.32 | 0.14 | 0.14 | 0.14 | 0.55 | 51.40 | -0.48 | 4/10 | 0.29 |
| TSMOM_5 | 1 | 0.00 | -0.06 | -0.44 | 0.23 | 0.30 | 0.10 | 0.16 | 0.17 | 1.00 | 97.50 | -0.17 | 4/10 | 0.43 |
| TSMOM_5 | 3 | -0.26 | -0.33 | -1.09 | 0.19 | 0.26 | 0.10 | 0.12 | 0.13 | 0.77 | 63.80 | -1.01 | 4/10 | 0.52 |
| TSMOM_5 | 5 | -0.15 | -0.23 | -0.92 | 0.23 | 0.31 | 0.14 | 0.14 | 0.15 | 0.65 | 50.50 | -0.72 | 5/10 | 0.57 |
| TSMOM_10 | 1 | -0.13 | -0.19 | -0.17 | -0.20 | -0.13 | -0.30 | -0.12 | -0.17 | 1.00 | 73 | -0.60 | 4/10 | -0.36 |
| TSMOM_10 | 3 | 0.14 | 0.07 | -0.28 | 0.31 | 0.39 | 0.25 | 0.19 | 0.23 | 0.83 | 42.20 | 0.21 | 3/10 | 0.09 |
| TSMOM_10 | 5 | 0.26 | 0.19 | -0.16 | 0.45 | 0.53 | 0.39 | 0.27 | 0.32 | 0.76 | 33.70 | 0.59 | 5/10 | 0.13 |
| TSMOM_20 | 1 | 0.00 | -0.06 | -0.42 | 0.19 | 0.31 | 0.13 | 0.13 | 0.15 | 1.00 | 46.80 | -0.20 | 5/10 | 0.01 |
| TSMOM_20 | 3 | -0.06 | -0.13 | -0.53 | 0.13 | 0.25 | 0.09 | 0.08 | 0.10 | 0.89 | 29.70 | -0.40 | 4/10 | -0.14 |
| TSMOM_20 | 5 | -0.04 | -0.11 | -0.39 | 0.07 | 0.19 | 0.03 | 0.05 | 0.04 | 0.84 | 23.60 | -0.35 | 3/10 | -0.11 |
| TSMOM_60 | 1 | 0.47 | 0.31 | 0.21 | 0.38 | 0.60 | 0.36 | 0.23 | 0.38 | 1.00 | 22.30 | 0.96 | 6/10 | 0.17 |
| TSMOM_60 | 3 | 0.35 | 0.18 | 0.06 | 0.26 | 0.48 | 0.24 | 0.15 | 0.26 | 0.95 | 13.70 | 0.56 | 5/10 | 0.17 |
| TSMOM_60 | 5 | 0.31 | 0.14 | 0.13 | 0.16 | 0.38 | 0.14 | 0.10 | 0.14 | 0.92 | 10.70 | 0.45 | 5/10 | 0.18 |
| TSMOM_120 | 1 | 0.37 | 0.14 | -0.11 | 0.32 | 0.60 | 0.30 | 0.19 | 0.32 | 1.00 | 15.50 | 0.43 | 5/10 | 0.24 |
| TSMOM_120 | 3 | 0.47 | 0.24 | 0.05 | 0.35 | 0.63 | 0.35 | 0.21 | 0.36 | 0.96 | 9 | 0.74 | 5/10 | 0.38 |
| TSMOM_120 | 5 | 0.45 | 0.21 | 0.01 | 0.35 | 0.63 | 0.34 | 0.20 | 0.35 | 0.95 | 6.80 | 0.66 | 5/10 | 0.36 |
| TSMOM_250 | 1 | 0.17 | -0.07 | 0.00 | -0.17 | 0.19 | -0.19 | -0.08 | -0.30 | 1.00 | 15.10 | -0.21 | 5/10 | 0.03 |
| TSMOM_250 | 3 | 0.16 | -0.08 | -0.21 | -0.04 | 0.32 | -0.05 | -0.02 | -0.09 | 0.97 | 9.30 | -0.25 | 4/10 | 0.04 |
| TSMOM_250 | 5 | 0.15 | -0.09 | -0.23 | -0.04 | 0.32 | -0.05 | -0.01 | -0.11 | 0.95 | 7.30 | -0.28 | 4/10 | 0.08 |
| PMA_20 | 1 | 0.11 | 0.04 | -0.23 | 0.25 | 0.34 | 0.17 | 0.17 | 0.19 | 1.00 | 60.40 | 0.14 | 6/10 | 0.09 |
| PMA_20 | 3 | 0.12 | 0.04 | -0.31 | 0.30 | 0.39 | 0.25 | 0.19 | 0.22 | 0.86 | 36.70 | 0.14 | 5/10 | 0.23 |
| PMA_20 | 5 | 0.19 | 0.11 | -0.23 | 0.35 | 0.44 | 0.30 | 0.21 | 0.25 | 0.80 | 28.20 | 0.33 | 6/10 | 0.25 |
| PMA_50 | 1 | 0.42 | 0.34 | -0.33 | 0.83 | 0.96 | 0.79 | 0.52 | 0.71 | 1.00 | 34 | 1.06 | 6/10 | 0.16 |
| PMA_50 | 3 | 0.38 | 0.30 | -0.38 | 0.76 | 0.89 | 0.73 | 0.46 | 0.65 | 0.92 | 20.70 | 0.93 | 6/10 | 0.20 |
| PMA_50 | 5 | 0.37 | 0.28 | -0.22 | 0.62 | 0.76 | 0.60 | 0.38 | 0.54 | 0.88 | 16.50 | 0.87 | 5/10 | 0.23 |
| PMA_100 | 1 | 0.27 | 0.10 | -0.32 | 0.40 | 0.64 | 0.38 | 0.24 | 0.38 | 1.00 | 21.90 | 0.32 | 6/10 | 0.17 |
| PMA_100 | 3 | 0.31 | 0.14 | -0.44 | 0.53 | 0.77 | 0.52 | 0.31 | 0.51 | 0.95 | 12.80 | 0.42 | 5/10 | 0.17 |
| PMA_100 | 5 | 0.31 | 0.13 | -0.40 | 0.50 | 0.74 | 0.49 | 0.29 | 0.48 | 0.93 | 10 | 0.41 | 5/10 | 0.11 |
| PMA_200 | 1 | 0.20 | -0.02 | -0.41 | 0.24 | 0.53 | 0.23 | 0.15 | 0.25 | 1.00 | 15.50 | -0.08 | 4/10 | 0.14 |
| PMA_200 | 3 | 0.13 | -0.10 | -0.49 | 0.14 | 0.43 | 0.13 | 0.09 | 0.14 | 0.96 | 9.90 | -0.31 | 4/10 | 0.11 |
| PMA_200 | 5 | 0.15 | -0.08 | -0.47 | 0.17 | 0.47 | 0.16 | 0.11 | 0.17 | 0.95 | 7.80 | -0.26 | 4/10 | 0.15 |
| X_x5_20 | 1 | 0.31 | 0.24 | -0.03 | 0.45 | 0.53 | 0.40 | 0.30 | 0.35 | 1.00 | 31.50 | 0.75 | 7/10 | 0.25 |
| X_x5_20 | 3 | 0.24 | 0.17 | -0.06 | 0.34 | 0.43 | 0.30 | 0.22 | 0.27 | 0.92 | 29.10 | 0.53 | 6/10 | 0.10 |
| X_x5_20 | 5 | 0.17 | 0.09 | -0.06 | 0.22 | 0.31 | 0.18 | 0.14 | 0.16 | 0.86 | 26.70 | 0.29 | 6/10 | 0.12 |
| X_x10_50 | 1 | 0.20 | 0.12 | -0.34 | 0.42 | 0.55 | 0.40 | 0.26 | 0.36 | 1.00 | 12.80 | 0.38 | 5/10 | 0.26 |
| X_x10_50 | 3 | 0.30 | 0.22 | -0.15 | 0.46 | 0.59 | 0.44 | 0.28 | 0.40 | 0.97 | 12.40 | 0.68 | 5/10 | 0.20 |
| X_x10_50 | 5 | 0.31 | 0.24 | -0.10 | 0.44 | 0.58 | 0.43 | 0.27 | 0.38 | 0.94 | 11.80 | 0.73 | 6/10 | 0.23 |
| X_x20_100 | 1 | 0.50 | 0.32 | -0.14 | 0.63 | 0.87 | 0.63 | 0.37 | 0.63 | 1.00 | 5.30 | 1.01 | 7/10 | -0.04 |
| X_x20_100 | 3 | 0.52 | 0.35 | -0.16 | 0.69 | 0.93 | 0.69 | 0.40 | 0.69 | 0.99 | 5.20 | 1.08 | 7/10 | -0.16 |
| X_x20_100 | 5 | 0.57 | 0.39 | -0.17 | 0.77 | 1.01 | 0.77 | 0.45 | 0.76 | 0.97 | 5 | 1.22 | 7/10 | -0.24 |
| X_x50_200 | 1 | 0.25 | 0.02 | 0.09 | -0.03 | 0.24 | -0.03 | -0.01 | -0.05 | 1.00 | 3.00 | 0.05 | 4/10 | -0.04 |
| X_x50_200 | 3 | 0.23 | -0.00 | 0.13 | -0.10 | 0.17 | -0.10 | -0.05 | -0.12 | 0.99 | 3.00 | -0.01 | 4/10 | -0.06 |
| X_x50_200 | 5 | 0.24 | 0.00 | 0.17 | -0.11 | 0.16 | -0.12 | -0.05 | -0.14 | 0.99 | 3.00 | 0.01 | 4/10 | -0.05 |
| DON_20 | 1 | 0.20 | 0.16 | 0.02 | 0.26 | 0.35 | 0.24 | 0.17 | 0.20 | 1.00 | 16.50 | 0.50 | 5/10 | 0.13 |
| DON_20 | 3 | 0.13 | 0.09 | -0.07 | 0.20 | 0.29 | 0.18 | 0.13 | 0.16 | 0.96 | 16 | 0.29 | 5/10 | 0.00 |
| DON_20 | 5 | 0.10 | 0.06 | 0.01 | 0.10 | 0.20 | 0.08 | 0.07 | 0.07 | 0.92 | 15.80 | 0.19 | 4/10 | -0.04 |
| DON_55 | 1 | 0.24 | 0.03 | -0.74 | 0.58 | 0.83 | 0.58 | 0.35 | 0.56 | 1.00 | 5.30 | 0.09 | 6/10 | -0.28 |
| DON_55 | 3 | 0.21 | 0.00 | -0.74 | 0.52 | 0.77 | 0.52 | 0.31 | 0.51 | 0.99 | 5.30 | 0.01 | 5/10 | -0.33 |
| DON_55 | 5 | 0.22 | 0.01 | -0.71 | 0.50 | 0.75 | 0.50 | 0.30 | 0.49 | 0.97 | 5.30 | 0.02 | 5/10 | -0.35 |
| REV_1 | 1 | -0.68 | -0.64 | -1.21 | -0.26 | -0.30 | -0.61 | -0.19 | -0.18 | 1.00 | 249.20 | -1.98 | 2/10 | -0.44 |
| REV_1 | 3 | -0.75 | -0.69 | -1.05 | -0.41 | -0.48 | -0.60 | -0.20 | -0.20 | 0.50 | 82 | -2.14 | 2/10 | 0.00 |
| REV_1 | 5 | -0.50 | -0.42 | -0.50 | -0.40 | -0.49 | -0.55 | -0.16 | -0.17 | 0.38 | 49.20 | -1.32 | 1/10 | -0.07 |
| REV_5 | 1 | -0.31 | -0.25 | 0.06 | -0.49 | -0.56 | -0.62 | -0.37 | -0.34 | 1.00 | 97.50 | -0.78 | 4/10 | -0.70 |
| REV_5 | 3 | 0.02 | 0.09 | 0.77 | -0.38 | -0.45 | -0.47 | -0.26 | -0.24 | 0.77 | 63.80 | 0.27 | 6/10 | -0.74 |
| REV_5 | 5 | -0.06 | 0.02 | 0.63 | -0.40 | -0.48 | -0.49 | -0.27 | -0.23 | 0.65 | 50.50 | 0.05 | 5/10 | -0.77 |
| RSI2_CONNORS | 1 | -0.35 | -0.40 | -0.44 | -0.38 | -0.33 | -0.47 | -0.29 | -0.27 | 0.09 | 23.90 | -1.26 | 2/10 | 0.06 |
| RSI2_CONNORS | 3 | -0.30 | -0.36 | -0.51 | -0.25 | -0.18 | -0.31 | -0.10 | -0.33 | 0.09 | 12.60 | -1.12 | 5/10 | -0.12 |
| RSI2_CONNORS | 5 | -0.16 | -0.24 | -0.57 | -0.02 | 0.06 | -0.07 | 0.16 | -0.30 | 0.09 | 8.20 | -0.74 | 6/10 | -0.30 |
| RSI2_X | 1 | -0.44 | -0.38 | -0.80 | -0.10 | -0.17 | -0.25 | -0.47 | 0.20 | 0.29 | 67.70 | -1.19 | 3/10 | -0.24 |
| RSI2_X | 3 | -0.30 | -0.24 | -0.31 | -0.18 | -0.27 | -0.28 | -0.19 | -0.09 | 0.29 | 37.20 | -0.73 | 3/10 | 0.01 |
| RSI2_X | 5 | -0.22 | -0.14 | -0.04 | -0.21 | -0.31 | -0.28 | -0.03 | -0.23 | 0.28 | 24 | -0.45 | 3/10 | -0.04 |
| BB_REV | 1 | -0.70 | -0.67 | -0.98 | -0.52 | -0.57 | -0.60 | -0.55 | -0.25 | 0.12 | 27.20 | -2.07 | 1/10 | -0.60 |
| BB_REV | 3 | -0.54 | -0.50 | -0.49 | -0.52 | -0.59 | -0.58 | -0.38 | -0.37 | 0.12 | 15.10 | -1.55 | 1/10 | -0.22 |
| BB_REV | 5 | -0.21 | -0.16 | -0.03 | -0.24 | -0.31 | -0.29 | -0.08 | -0.23 | 0.12 | 11.10 | -0.49 | 4/10 | -0.15 |
| SIG2_REV | 1 | -0.58 | -0.58 | -0.60 | -0.63 | -0.63 | -0.74 | -0.61 | -0.28 | 0.07 | 34.70 | -1.79 | 2/10 | -0.51 |
| SIG2_REV | 3 | -0.32 | -0.31 | -0.36 | -0.30 | -0.30 | -0.36 | -0.17 | -0.19 | 0.07 | 11.80 | -0.95 | 3/10 | -0.39 |
| SIG2_REV | 5 | -0.13 | -0.12 | 0.11 | -0.26 | -0.27 | -0.31 | -0.22 | -0.14 | 0.07 | 7 | -0.39 | 4/10 | -0.37 |
| STREAK_REV | 1 | -0.69 | -0.64 | -0.83 | -0.47 | -0.53 | -0.64 | -0.64 | -0.07 | 0.25 | 61.30 | -1.98 | 1/10 | 0.03 |
| STREAK_REV | 3 | -0.61 | -0.55 | -0.50 | -0.59 | -0.67 | -0.72 | -0.61 | -0.25 | 0.25 | 35.90 | -1.71 | 0/10 | 0.08 |
| STREAK_REV | 5 | -0.52 | -0.45 | -0.19 | -0.69 | -0.78 | -0.78 | -0.50 | -0.45 | 0.23 | 22 | -1.40 | 2/10 | 0.15 |
| W52_NEARHIGH_LONG | 1 | 0.68 | 0.47 | 0.20 | 0.65 | 0.90 | 0.61 | 0.65 |  | 0.23 | 12.70 | 1.45 | 6/10 | -0.11 |
| W52_NEARHIGH_LONG | 3 | 0.55 | 0.34 | 0.05 | 0.52 | 0.77 | 0.49 | 0.52 |  | 0.23 | 8.40 | 1.05 | 6/10 | -0.20 |
| W52_NEARHIGH_LONG | 5 | 0.59 | 0.37 | 0.09 | 0.56 | 0.81 | 0.54 | 0.56 |  | 0.23 | 6.40 | 1.16 | 6/10 | -0.14 |
| TSMOM_20_VT10 | 1 | 0.24 | 0.15 | -0.21 | 0.51 | 0.65 | 0.43 | 0.41 | 0.30 | 0.76 | 39.50 | 0.48 | 5/10 | 0.14 |
| TSMOM_20_VT10 | 3 | 0.15 | 0.06 | -0.32 | 0.39 | 0.53 | 0.33 | 0.32 | 0.20 | 0.68 | 25.40 | 0.17 | 4/10 | -0.02 |
| TSMOM_20_VT10 | 5 | 0.18 | 0.09 | -0.17 | 0.33 | 0.49 | 0.29 | 0.32 | 0.10 | 0.64 | 20.20 | 0.28 | 5/10 | -0.03 |
| TSMOM_250_VT10 | 1 | 0.34 | 0.10 | 0.10 | 0.05 | 0.45 | 0.01 | 0.11 | -0.14 | 0.76 | 17.30 | 0.32 | 5/10 | 0.05 |
| TSMOM_250_VT10 | 3 | 0.30 | 0.06 | -0.16 | 0.20 | 0.60 | 0.18 | 0.19 | 0.06 | 0.74 | 11.20 | 0.18 | 4/10 | 0.09 |
| TSMOM_250_VT10 | 5 | 0.28 | 0.04 | -0.20 | 0.18 | 0.59 | 0.16 | 0.20 | -0.02 | 0.72 | 8.90 | 0.11 | 4/10 | 0.15 |

### T6. Kuyruk momentumu ve oynaklık rejimi backtestleri
| strat | h | sh_full | shdm_full | shdm_is | shdm_oos | sh_oos | shdm_oos10 | strict5dm_oos | long_shdm_oos | short_shdm_oos | expo | turn | t_dm_full | t_dm_is | t_dm_oos | yrs_pos | e_shdm | e_t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TAILMOM_z1.5 | 1 | 0.11 | 0.09 | 0.20 | 0.05 | 0.07 | -0.14 | 0.02 | -0.18 | 0.29 | 0.15 | 68.30 | 0.29 | 0.44 | 0.10 | 6/10 | 0.09 | 0.25 |
| TAILMOM_z1.5_vt | 1 | 0.14 | 0.13 | -0.17 | 0.34 | 0.36 | 0.16 | 0.32 | -0.14 | 0.69 | 0.15 | 68.80 | 0.41 | -0.38 | 0.75 | 5/10 |  |  |
| TAILMOM_z1.5_vt1 | 1 | -0.21 | -0.22 | 0.16 | -0.47 | -0.45 | -0.66 | -0.50 | -0.21 | -0.52 | 0.15 | 68.80 | -0.68 | 0.35 | -1.04 | 6/10 |  |  |
| TAILMOM_z1.5 | 3 | 0.42 | 0.39 | 0.39 | 0.40 | 0.44 | 0.29 | 0.39 | 0.28 | 0.19 | 0.13 | 23.20 | 1.21 | 0.85 | 0.88 | 6/10 | 0.05 | 0.13 |
| TAILMOM_z1.5_vt | 3 | 0.23 | 0.21 | -0.04 | 0.37 | 0.40 | 0.27 | 0.36 | 0.17 | 0.31 | 0.13 | 23.20 | 0.65 | -0.08 | 0.81 | 6/10 |  |  |
| TAILMOM_z1.5_vt1 | 3 | -0.16 | -0.18 | -0.58 | 0.04 | 0.06 | -0.06 | 0.02 | 0.10 | -0.09 | 0.13 | 23.20 | -0.55 | -1.27 | 0.09 | 3/10 |  |  |
| TAILMOM_z1.5 | 5 | 0.14 | 0.11 | -0.39 | 0.37 | 0.41 | 0.29 | 0.36 | 0.28 | 0.15 | 0.12 | 14.20 | 0.34 | -0.85 | 0.80 | 6/10 | -0.03 | -0.08 |
| TAILMOM_z1.5_vt | 5 | 0.05 | 0.03 | -0.41 | 0.29 | 0.32 | 0.22 | 0.28 | 0.17 | 0.21 | 0.11 | 13.90 | 0.08 | -0.91 | 0.64 | 5/10 |  |  |
| TAILMOM_z1.5_vt1 | 5 | -0.14 | -0.16 | -0.58 | 0.06 | 0.09 | -0.02 | 0.04 | 0.24 | -0.30 | 0.11 | 13.90 | -0.50 | -1.26 | 0.12 | 5/10 |  |  |
| TAILMOM_z2.0 | 1 | 0.30 | 0.29 | 0.11 | 0.41 | 0.41 | 0.29 | 0.40 | 0.13 | 0.45 | 0.07 | 34.70 | 0.91 | 0.23 | 0.89 | 7/10 | 0.21 | 0.57 |
| TAILMOM_z2.0_vt | 1 | 0.25 | 0.25 | 0.31 | 0.24 | 0.24 | 0.11 | 0.23 | -0.03 | 0.40 | 0.08 | 37.60 | 0.77 | 0.69 | 0.52 | 7/10 |  |  |
| TAILMOM_z2.0_vt1 | 1 | -0.28 | -0.28 | 0.34 | -0.70 | -0.70 | -0.84 | -0.71 | -0.25 | -0.95 | 0.08 | 37.60 | -0.87 | 0.75 | -1.54 | 6/10 |  |  |
| TAILMOM_z2.0 | 3 | 0.15 | 0.14 | 0.12 | 0.16 | 0.16 | 0.09 | 0.15 | 0.12 | 0.06 | 0.07 | 11.80 | 0.43 | 0.26 | 0.35 | 7/10 | 0.20 | 0.52 |
| TAILMOM_z2.0_vt | 3 | 0.06 | 0.05 | 0.24 | -0.06 | -0.06 | -0.14 | -0.07 | -0.05 | -0.02 | 0.08 | 12.70 | 0.16 | 0.52 | -0.13 | 6/10 |  |  |
| TAILMOM_z2.0_vt1 | 3 | -0.18 | -0.19 | -0.41 | -0.04 | -0.04 | -0.12 | -0.05 | 0.13 | -0.27 | 0.08 | 12.70 | -0.58 | -0.90 | -0.09 | 6/10 |  |  |
| TAILMOM_z2.0 | 5 | 0.01 | 0.00 | -0.29 | 0.17 | 0.17 | 0.12 | 0.16 | 0.09 | 0.13 | 0.07 | 7 | 0.01 | -0.63 | 0.37 | 6/10 | 0.22 | 0.59 |
| TAILMOM_z2.0_vt | 5 | -0.03 | -0.04 | -0.24 | 0.11 | 0.11 | 0.04 | 0.10 | 0.20 | -0.13 | 0.07 | 7.40 | -0.13 | -0.52 | 0.23 | 6/10 |  |  |
| TAILMOM_z2.0_vt1 | 5 | -0.35 | -0.36 | -0.53 | -0.24 | -0.23 | -0.30 | -0.24 | 0.08 | -0.47 | 0.07 | 7.40 | -1.12 | -1.17 | -0.52 | 5/10 |  |  |
| TAILMOM_z2.5 | 1 | 0.23 | 0.23 | 0.35 | 0.21 | 0.20 | 0.15 | 0.21 | -0.28 | 0.56 | 0.04 | 18.10 | 0.72 | 0.76 | 0.46 | 5/10 | 0.40 | 1.08 |
| TAILMOM_z2.5_vt | 1 | 0.28 | 0.28 | 0.54 | 0.20 | 0.20 | 0.15 | 0.20 | -0.09 | 0.42 | 0.04 | 16.80 | 0.88 | 1.18 | 0.44 | 7/10 |  |  |
| TAILMOM_z2.5_vt1 | 1 | -0.37 | -0.36 | 0.76 | -1.02 | -1.02 | -1.08 | -1.02 | -0.63 | -0.95 | 0.04 | 16.80 | -1.12 | 1.67 | -2.24 | 7/10 |  |  |
| TAILMOM_z2.5 | 3 | -0.13 | -0.13 | 0.35 | -0.42 | -0.43 | -0.46 | -0.42 | -0.36 | -0.05 | 0.04 | 6.20 | -0.39 | 0.77 | -0.92 | 5/10 | 0.41 | 1.09 |
| TAILMOM_z2.5_vt | 3 | -0.09 | -0.08 | 0.58 | -0.47 | -0.47 | -0.51 | -0.47 | -0.34 | -0.14 | 0.03 | 5.80 | -0.25 | 1.27 | -1.03 | 6/10 |  |  |
| TAILMOM_z2.5_vt1 | 3 | -0.41 | -0.40 | -0.23 | -0.52 | -0.53 | -0.56 | -0.52 | -0.24 | -0.55 | 0.03 | 5.80 | -1.24 | -0.49 | -1.15 | 4/10 |  |  |
| TAILMOM_z2.5 | 5 | -0.17 | -0.17 | -0.27 | -0.08 | -0.11 | -0.12 | -0.09 | -0.09 | 0.00 | 0.04 | 3.70 | -0.51 | -0.60 | -0.18 | 5/10 | 0.34 | 0.92 |
| TAILMOM_z2.5_vt | 5 | -0.27 | -0.25 | -0.09 | -0.39 | -0.40 | -0.42 | -0.39 | -0.19 | -0.24 | 0.03 | 3.40 | -0.79 | -0.21 | -0.85 | 6/10 |  |  |
| TAILMOM_z2.5_vt1 | 5 | -0.58 | -0.57 | -0.55 | -0.58 | -0.59 | -0.62 | -0.58 | -0.21 | -0.58 | 0.03 | 3.40 | -1.76 | -1.21 | -1.28 | 4/10 |  |  |
| TAILMOM_bb2.0 | 1 | 0.51 | 0.47 | 0.75 | 0.34 | 0.40 | 0.25 | 0.24 | 0.11 | 0.45 | 0.12 | 27.20 | 1.46 | 1.64 | 0.75 | 8/10 | 0.39 | 1.05 |
| TAILMOM_bb2.0_vt | 1 | 0.51 | 0.48 | 0.49 | 0.51 | 0.57 | 0.41 | 0.39 | 0.42 | 0.28 | 0.13 | 27.60 | 1.48 | 1.07 | 1.11 | 8/10 |  |  |
| TAILMOM_bb2.0_vt1 | 1 | 0.11 | 0.08 | 0.05 | 0.09 | 0.15 | 0.00 | -0.02 | 0.13 | -0.04 | 0.13 | 27.60 | 0.24 | 0.11 | 0.20 | 7/10 |  |  |
| TAILMOM_bb2.0 | 3 | 0.41 | 0.36 | 0.32 | 0.40 | 0.47 | 0.35 | 0.39 | 0.28 | 0.31 | 0.12 | 15.10 | 1.13 | 0.70 | 0.89 | 8/10 | 0.06 | 0.16 |
| TAILMOM_bb2.0_vt | 3 | 0.29 | 0.24 | -0.02 | 0.42 | 0.49 | 0.36 | 0.40 | 0.42 | 0.12 | 0.13 | 16.10 | 0.75 | -0.05 | 0.93 | 8/10 |  |  |
| TAILMOM_bb2.0_vt1 | 3 | 0.02 | -0.03 | -0.50 | 0.28 | 0.35 | 0.21 | 0.25 | 0.41 | -0.18 | 0.13 | 16.10 | -0.08 | -1.10 | 0.60 | 4/10 |  |  |
| TAILMOM_bb2.0 | 5 | 0.10 | 0.05 | -0.12 | 0.15 | 0.22 | 0.11 | 0.15 | 0.16 | 0.03 | 0.12 | 11.10 | 0.15 | -0.26 | 0.33 | 4/10 | 0.03 | 0.07 |
| TAILMOM_bb2.0_vt | 5 | 0.15 | 0.11 | -0.25 | 0.33 | 0.41 | 0.28 | 0.32 | 0.36 | 0.03 | 0.13 | 11.40 | 0.33 | -0.54 | 0.72 | 5/10 |  |  |
| TAILMOM_bb2.0_vt1 | 5 | 0.07 | 0.02 | -0.43 | 0.29 | 0.37 | 0.24 | 0.28 | 0.39 | -0.16 | 0.13 | 11.40 | 0.06 | -0.94 | 0.63 | 4/10 |  |  |
| VOLREG_1 | 1 | 0.01 | 0.01 | -0.21 | 0.18 | 0.17 | -0.10 | -0.06 | -0.05 | 0.30 | 0.73 | 190 | 0.03 | -0.45 | 0.40 | 6/10 | 0.03 | 0.09 |
| VOLREG_1_LOWVOL_MOM | 1 | 0.39 | 0.37 | 0.52 | 0.21 | 0.23 | -0.04 | -0.02 | 0.11 | 0.20 | 0.41 | 103 | 1.14 | 1.15 | 0.47 | 7/10 |  |  |
| VOLREG_1_HIGHVOL_REV | 1 | -0.22 | -0.21 | -0.87 | 0.11 | 0.09 | -0.09 | -0.06 | -0.11 | 0.25 | 0.32 | 87.80 | -0.65 | -1.91 | 0.24 | 4/10 |  |  |
| VOLREG_1_vt | 1 | -0.08 | -0.07 | -0.04 | -0.08 | -0.09 | -0.35 | -0.33 | -0.12 | -0.00 | 0.63 | 167.10 | -0.22 | -0.08 | -0.18 | 5/10 |  |  |
| VOLREG_1 | 3 | 0.18 | 0.18 | 0.41 | -0.01 | -0.02 | -0.18 | -0.15 | -0.17 | 0.17 | 0.38 | 66.10 | 0.54 | 0.90 | -0.01 | 7/10 | 0.30 | 0.80 |
| VOLREG_1_LOWVOL_MOM | 3 | 0.90 | 0.86 | 1.07 | 0.60 | 0.63 | 0.44 | 0.49 | 0.27 | 0.36 | 0.22 | 36.60 | 2.68 | 2.34 | 1.33 | 7/10 |  |  |
| VOLREG_1_HIGHVOL_REV | 3 | -0.36 | -0.35 | -0.52 | -0.26 | -0.29 | -0.38 | -0.36 | -0.31 | 0.05 | 0.17 | 30.10 | -1.08 | -1.13 | -0.57 | 3/10 |  |  |
| VOLREG_1_vt | 3 | 0.32 | 0.34 | 0.36 | 0.34 | 0.33 | 0.18 | 0.21 | 0.05 | 0.29 | 0.33 | 57.20 | 1.05 | 0.78 | 0.75 | 7/10 |  |  |
| VOLREG_1 | 5 | 0.60 | 0.59 | 0.87 | 0.42 | 0.40 | 0.29 | 0.32 | -0.01 | 0.36 | 0.30 | 41 | 1.83 | 1.90 | 0.92 | 7/10 | 0.06 | 0.15 |
| VOLREG_1_LOWVOL_MOM | 5 | 1.02 | 0.98 | 1.03 | 1.10 | 1.13 | 0.98 | 1.01 | 0.56 | 0.42 | 0.17 | 22.40 | 3.05 | 2.26 | 2.41 | 6/10 |  |  |
| VOLREG_1_HIGHVOL_REV | 5 | 0.03 | 0.05 | 0.16 | -0.00 | -0.03 | -0.09 | -0.07 | -0.24 | 0.23 | 0.12 | 19.20 | 0.17 | 0.34 | -0.00 | 4/10 |  |  |
| VOLREG_1_vt | 5 | 0.62 | 0.64 | 0.88 | 0.53 | 0.51 | 0.40 | 0.43 | 0.10 | 0.35 | 0.25 | 36.30 | 1.98 | 1.93 | 1.15 | 8/10 |  |  |
| VOLREG_5 | 1 | 0.82 | 0.80 | 1.09 | 0.64 | 0.64 | 0.51 | 0.24 | 0.28 | 0.61 | 0.73 | 83.20 | 2.48 | 2.39 | 1.40 | 7/10 | 0.05 | 0.13 |
| VOLREG_5_LOWVOL_MOM | 1 | 1.03 | 0.99 | 0.82 | 1.31 | 1.36 | 1.19 | 0.95 | 0.84 | 1.04 | 0.41 | 43 | 3.06 | 1.79 | 2.88 | 7/10 |  |  |
| VOLREG_5_HIGHVOL_REV | 1 | 0.33 | 0.34 | 0.72 | 0.17 | 0.16 | 0.09 | -0.10 | -0.06 | 0.29 | 0.32 | 40.40 | 1.06 | 1.59 | 0.38 | 5/10 |  |  |
| VOLREG_5_vt | 1 | 0.60 | 0.62 | 1.05 | 0.37 | 0.37 | 0.25 | -0.02 | 0.24 | 0.29 | 0.63 | 78.20 | 1.93 | 2.30 | 0.82 | 7/10 |  |  |
| VOLREG_5 | 3 | 1.02 | 1.00 | 1.31 | 0.85 | 0.86 | 0.76 | 0.74 | 0.43 | 0.69 | 0.57 | 55.70 | 3.10 | 2.86 | 1.87 | 8/10 | 0.04 | 0.09 |
| VOLREG_5_LOWVOL_MOM | 3 | 0.94 | 0.89 | 0.58 | 1.40 | 1.46 | 1.32 | 1.30 | 0.80 | 1.07 | 0.33 | 28.70 | 2.75 | 1.28 | 3.09 | 7/10 |  |  |
| VOLREG_5_HIGHVOL_REV | 3 | 0.63 | 0.63 | 1.33 | 0.38 | 0.37 | 0.32 | 0.31 | 0.11 | 0.38 | 0.25 | 27.50 | 1.97 | 2.91 | 0.85 | 7/10 |  |  |
| VOLREG_5_vt | 3 | 0.79 | 0.81 | 1.42 | 0.50 | 0.49 | 0.41 | 0.39 | 0.24 | 0.41 | 0.49 | 49.40 | 2.51 | 3.10 | 1.09 | 6/10 |  |  |
| VOLREG_5 | 5 | 1.10 | 1.07 | 1.27 | 1.02 | 1.03 | 0.94 | 0.96 | 0.50 | 0.73 | 0.49 | 42.90 | 3.33 | 2.78 | 2.24 | 8/10 | 0.16 | 0.43 |
| VOLREG_5_LOWVOL_MOM | 5 | 1.02 | 0.95 | 0.55 | 1.63 | 1.69 | 1.56 | 1.57 | 0.97 | 1.10 | 0.29 | 22.30 | 2.96 | 1.20 | 3.58 | 7/10 |  |  |
| VOLREG_5_HIGHVOL_REV | 5 | 0.66 | 0.67 | 1.34 | 0.46 | 0.45 | 0.40 | 0.43 | 0.09 | 0.45 | 0.20 | 21.10 | 2.09 | 2.93 | 1.02 | 7/10 |  |  |
| VOLREG_5_vt | 5 | 0.75 | 0.77 | 1.38 | 0.48 | 0.47 | 0.40 | 0.43 | 0.22 | 0.37 | 0.42 | 38.80 | 2.39 | 3.03 | 1.06 | 7/10 |  |  |
| VOLREG_20 | 1 | 0.50 | 0.49 | 0.72 | 0.37 | 0.35 | 0.29 | -0.07 | 0.09 | 0.40 | 0.73 | 49.80 | 1.51 | 1.57 | 0.81 | 7/10 | 0.18 | 0.50 |
| VOLREG_20_LOWVOL_MOM | 1 | 0.62 | 0.57 | 0.46 | 0.79 | 0.84 | 0.71 | 0.38 | 0.46 | 0.72 | 0.41 | 25.80 | 1.77 | 1.01 | 1.74 | 6/10 |  |  |
| VOLREG_20_HIGHVOL_REV | 1 | 0.22 | 0.22 | 0.55 | 0.09 | 0.05 | 0.03 | -0.22 | -0.14 | 0.21 | 0.32 | 24.20 | 0.70 | 1.21 | 0.19 | 6/10 |  |  |
| VOLREG_20_vt | 1 | 0.52 | 0.52 | 1.15 | 0.15 | 0.12 | 0.07 | -0.29 | 0.08 | 0.13 | 0.63 | 48.50 | 1.62 | 2.53 | 0.33 | 6/10 |  |  |
| VOLREG_20 | 3 | 0.45 | 0.43 | 0.56 | 0.37 | 0.35 | 0.32 | 0.24 | 0.12 | 0.36 | 0.65 | 31.90 | 1.34 | 1.23 | 0.81 | 5/10 | 0.36 | 0.96 |
| VOLREG_20_LOWVOL_MOM | 3 | 0.52 | 0.46 | 0.24 | 0.80 | 0.85 | 0.74 | 0.68 | 0.46 | 0.70 | 0.37 | 17.10 | 1.44 | 0.52 | 1.75 | 5/10 |  |  |
| VOLREG_20_HIGHVOL_REV | 3 | 0.22 | 0.22 | 0.57 | 0.09 | 0.04 | 0.05 | -0.01 | -0.10 | 0.18 | 0.29 | 15.20 | 0.70 | 1.25 | 0.19 | 4/10 |  |  |
| VOLREG_20_vt | 3 | 0.47 | 0.47 | 1.17 | 0.07 | 0.03 | 0.02 | -0.07 | -0.06 | 0.14 | 0.56 | 29 | 1.46 | 2.55 | 0.15 | 6/10 |  |  |
| VOLREG_20 | 5 | 0.47 | 0.45 | 0.52 | 0.45 | 0.43 | 0.41 | 0.38 | 0.18 | 0.41 | 0.62 | 24.30 | 1.40 | 1.14 | 1.00 | 6/10 | 0.19 | 0.52 |
| VOLREG_20_LOWVOL_MOM | 5 | 0.53 | 0.47 | 0.27 | 0.84 | 0.89 | 0.79 | 0.77 | 0.57 | 0.57 | 0.35 | 13.30 | 1.47 | 0.59 | 1.84 | 6/10 |  |  |
| VOLREG_20_HIGHVOL_REV | 5 | 0.23 | 0.24 | 0.48 | 0.17 | 0.12 | 0.14 | 0.11 | -0.10 | 0.26 | 0.27 | 11.40 | 0.76 | 1.04 | 0.37 | 4/10 |  |  |
| VOLREG_20_vt | 5 | 0.39 | 0.40 | 1.10 | 0.02 | -0.02 | -0.01 | -0.05 | -0.09 | 0.10 | 0.53 | 21.70 | 1.23 | 2.40 | 0.05 | 6/10 |  |  |

### T7. IS seçimi (spot kaynak, |t_IS| en büyük) ve tek seferlik OOS
| grup | h | secilen | ic_is | t_is | ic_oos | t_oos | ayni_isaret | t_full | yrs | ic_early | t_early |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TSMOM ham getiri ret_k | 1 | ret2 | 0.06 | 2.09 | 0.00 | 0.05 | True | 1.31 | 5/10 | -0.01 | -0.43 |
| TSMOM ham getiri ret_k | 3 | ret5 | -0.08 | -1.85 | 0.04 | 1.02 | False | -0.22 | 6/10 | 0.01 | 0.44 |
| TSMOM ham getiri ret_k | 5 | ret3 | -0.09 | -2.26 | 0.03 | 0.69 | False | -0.73 | 6/10 | 0.01 | 0.31 |
| TSMOM oynaklık ölçekli vsr_k | 1 | vsr2 | 0.07 | 2.38 | 0.00 | 0.09 | True | 1.61 | 6/10 | -0.00 | -0.08 |
| TSMOM oynaklık ölçekli vsr_k | 3 | vsr1 | 0.05 | 1.84 | 0.03 | 0.90 | True | 1.88 | 8/10 | -0.01 | -0.61 |
| TSMOM oynaklık ölçekli vsr_k | 5 | vsr3 | -0.07 | -1.70 | 0.06 | 1.29 | False | -0.12 | 6/10 | 0.01 | 0.43 |
| MA / kesişim / Donchian / 52h | 1 | dbrk20 | 0.03 | 1.07 | 0.03 | 1.02 | True | 1.49 | 6/10 | 0.00 | 0.05 |
| MA / kesişim / Donchian / 52h | 3 | dst55 | -0.06 | -1.39 | 0.10 | 2.12 | False | 0.79 | 3/8 | -0.05 | -1.33 |
| MA / kesişim / Donchian / 52h | 5 | dst55 | -0.08 | -1.60 | 0.11 | 1.94 | False | 0.51 | 3/8 | -0.07 | -1.66 |
| Kısa vade dönüş (RSI/BB/seri/2σ) | 1 | z1 | 0.07 | 2.23 | 0.01 | 0.26 | True | 1.72 | 6/10 | -0.01 | -0.58 |
| Kısa vade dönüş (RSI/BB/seri/2σ) | 3 | z1 | 0.05 | 1.86 | 0.03 | 0.91 | True | 1.89 | 8/10 | -0.01 | -0.62 |
| Kısa vade dönüş (RSI/BB/seri/2σ) | 5 | bb_lo | 0.06 | 1.44 | -0.00 | -0.01 | False | 1.05 | 7/10 | -0.02 | -0.68 |
| Oynaklık rejimi | 1 | ret5_loV | 0.09 | 2.38 | 0.17 | 2.68 | True | 3.45 | 6/9 | 0.04 | 0.97 |
| Oynaklık rejimi | 3 | ret1_loV | 0.11 | 2.66 | 0.12 | 1.85 | True | 3.19 | 7/9 | 0.02 | 0.47 |
| Oynaklık rejimi | 5 | ret5_hiV | -0.23 | -3.03 | -0.12 | -1.83 | True | -2.88 | 5/7 | -0.03 | -0.35 |
| Gün içi segmentler | 1 | segD_13_15 | 0.08 | 2.40 | 0.04 | 1.19 | True | 2.49 | 8/10 | -0.04 | -1.84 |
| Gün içi segmentler | 3 | segA_15p_20p | 0.06 | 2.03 | -0.06 | -2.24 | False | -0.55 | 6/10 | -0.03 | -1.14 |
| Gün içi segmentler | 5 | segC_07_13 | -0.07 | -2.35 | 0.03 | 1.11 | False | -0.59 | 7/10 | 0.00 | 0.16 |

### T8. IS seçimi (backtest, IS demeaned Sharpe en büyük)
| aile | h | secilen | shdm_is | shdm_oos | sh_oos | shdm_oos10 | t_dm_oos | e_shdm | yrs_pos |
|---|---|---|---|---|---|---|---|---|---|
| TAILMOM | 1 | TAILMOM_bb2.0 | 0.75 | 0.34 | 0.40 | 0.25 | 0.75 | 0.39 | 8/10 |
| TAILMOM | 3 | TAILMOM_z1.5 | 0.39 | 0.40 | 0.44 | 0.29 | 0.88 | 0.05 | 6/10 |
| TAILMOM | 5 | TAILMOM_bb2.0 | -0.12 | 0.15 | 0.22 | 0.11 | 0.33 | 0.03 | 4/10 |
| VOLREG | 1 | VOLREG_5 | 1.09 | 0.64 | 0.64 | 0.51 | 1.40 | 0.05 | 7/10 |
| VOLREG | 3 | VOLREG_5 | 1.31 | 0.85 | 0.86 | 0.76 | 1.87 | 0.04 | 8/10 |
| VOLREG | 5 | VOLREG_5 | 1.27 | 1.02 | 1.03 | 0.94 | 2.24 | 0.16 | 8/10 |

### T9. LOWMOM (sakin piyasa momentumu) sağlamlık
| sig | h | sh_full | shdm_full | t_full | shdm_is | t_is | shdm_oos | t_oos | sh_oos_net | shdm_oos_10 | ann_oos | expo | turnover | yrs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LOWMOM_k5(base) | 1 | 1.03 | 0.99 | 3.06 | 0.82 | 1.79 | 1.31 | 2.88 | 1.36 | 1.19 | 7.95 | 0.41 | 43 | 7/9 |
| LOWMOM_k1 | 1 | 0.39 | 0.37 | 1.14 | 0.52 | 1.15 | 0.21 | 0.47 | 0.23 | -0.04 | 1.35 | 0.41 | 103 | 7/9 |
| LOWMOM_k3 | 1 | 0.61 | 0.59 | 1.82 | 0.68 | 1.49 | 0.52 | 1.15 | 0.55 | 0.36 | 3.22 | 0.41 | 58.80 | 6/9 |
| LOWMOM_k10 | 1 | 0.53 | 0.48 | 1.49 | 0.36 | 0.79 | 0.72 | 1.59 | 0.77 | 0.63 | 4.50 | 0.41 | 33.40 | 7/9 |
| LOWMOM_k20 | 1 | 0.62 | 0.57 | 1.77 | 0.46 | 1.01 | 0.79 | 1.74 | 0.84 | 0.71 | 4.92 | 0.41 | 25.80 | 6/9 |
| LOWMOM_k5_viop_t | 1 | 0.81 | 0.77 | 2.39 | 0.66 | 1.45 | 1.01 | 2.22 | 1.04 | 0.90 | 6.06 | 0.41 | 42 | 8/9 |
| LOWMOM_k5_viop_t1 | 1 | 0.53 | 0.49 | 1.51 | 0.18 | 0.38 | 0.98 | 2.16 | 1.01 | 0.87 | 6.06 | 0.41 | 42 | 7/9 |
| LOWMOM_k5_excl_rollnear | 1 | 1.06 | 0.99 | 2.95 | 0.74 | 1.56 | 1.44 | 3.05 | 1.52 | 1.31 | 8.93 | 0.41 | 46.40 | 8/9 |
| LOWMOM_k5_excl_extreme | 1 | 1.06 | 1.01 | 3.07 | 0.84 | 1.81 | 1.34 | 2.88 | 1.39 | 1.22 | 8.38 | 0.41 | 44.90 | 7/9 |
| LOWMOM_k5_winsor | 1 | 1.02 | 0.96 | 2.99 | 0.78 | 1.71 | 1.30 | 2.86 | 1.36 | 1.18 | 7.93 | 0.41 | 43 | 6/9 |
| LOWMOM_k5_continuous | 1 | 1.02 | 0.97 | 3.01 | 0.95 | 2.07 | 1.10 | 2.41 | 1.16 | 0.97 | 5.08 | 0.27 | 36.90 | 8/9 |
| LOWMOM_k5(base) | 3 | 0.94 | 0.89 | 2.75 | 0.58 | 1.28 | 1.40 | 3.09 | 1.46 | 1.32 | 7.16 | 0.33 | 28.70 | 7/9 |
| LOWMOM_k1 | 3 | 0.90 | 0.86 | 2.68 | 1.07 | 2.34 | 0.60 | 1.33 | 0.63 | 0.44 | 2.19 | 0.22 | 36.60 | 7/9 |
| LOWMOM_k3 | 3 | 0.72 | 0.69 | 2.14 | 0.71 | 1.55 | 0.67 | 1.48 | 0.71 | 0.56 | 3.32 | 0.30 | 35.10 | 6/9 |
| LOWMOM_k10 | 3 | 0.47 | 0.41 | 1.28 | 0.31 | 0.67 | 0.61 | 1.35 | 0.66 | 0.55 | 3.48 | 0.35 | 21.10 | 6/9 |
| LOWMOM_k20 | 3 | 0.52 | 0.46 | 1.44 | 0.24 | 0.52 | 0.80 | 1.75 | 0.85 | 0.74 | 4.63 | 0.37 | 17.10 | 5/9 |
| LOWMOM_k5_viop_t | 3 | 0.78 | 0.73 | 2.26 | 0.48 | 1.05 | 1.14 | 2.50 | 1.17 | 1.06 | 6.10 | 0.33 | 28.40 | 7/9 |
| LOWMOM_k5_viop_t1 | 3 | 0.63 | 0.59 | 1.82 | 0.21 | 0.45 | 1.18 | 2.60 | 1.21 | 1.11 | 6.16 | 0.33 | 28.40 | 7/9 |
| LOWMOM_k5_excl_rollnear | 3 | 0.87 | 0.79 | 2.36 | 0.38 | 0.80 | 1.46 | 3.09 | 1.54 | 1.37 | 7.72 | 0.33 | 31 | 7/9 |
| LOWMOM_k5_excl_extreme | 3 | 0.96 | 0.91 | 2.76 | 0.60 | 1.29 | 1.44 | 3.09 | 1.50 | 1.36 | 7.55 | 0.33 | 30 | 7/9 |
| LOWMOM_k5_winsor | 3 | 0.93 | 0.86 | 2.67 | 0.53 | 1.17 | 1.39 | 3.06 | 1.46 | 1.31 | 7.16 | 0.33 | 28.70 | 7/9 |
| LOWMOM_k5_continuous | 3 | 0.88 | 0.83 | 2.57 | 0.64 | 1.39 | 1.16 | 2.55 | 1.23 | 1.08 | 4.96 | 0.24 | 23.10 | 7/9 |
| LOWMOM_k5(base) | 5 | 1.02 | 0.95 | 2.96 | 0.55 | 1.20 | 1.63 | 3.58 | 1.69 | 1.56 | 7.49 | 0.29 | 22.30 | 7/9 |
| LOWMOM_k1 | 5 | 1.02 | 0.98 | 3.05 | 1.03 | 2.26 | 1.10 | 2.41 | 1.13 | 0.98 | 3.19 | 0.17 | 22.40 | 6/9 |
| LOWMOM_k3 | 5 | 0.78 | 0.75 | 2.32 | 0.59 | 1.30 | 1.03 | 2.26 | 1.07 | 0.94 | 4.18 | 0.25 | 23.10 | 7/9 |
| LOWMOM_k10 | 5 | 0.58 | 0.51 | 1.59 | 0.40 | 0.88 | 0.75 | 1.65 | 0.81 | 0.70 | 3.96 | 0.32 | 17.20 | 6/9 |
| LOWMOM_k20 | 5 | 0.53 | 0.47 | 1.47 | 0.27 | 0.59 | 0.84 | 1.84 | 0.89 | 0.79 | 4.55 | 0.35 | 13.30 | 6/9 |
| LOWMOM_k5_viop_t | 5 | 0.80 | 0.75 | 2.32 | 0.45 | 0.99 | 1.22 | 2.69 | 1.25 | 1.16 | 5.88 | 0.29 | 22.10 | 7/9 |
| LOWMOM_k5_viop_t1 | 5 | 0.57 | 0.52 | 1.60 | 0.17 | 0.37 | 1.06 | 2.32 | 1.09 | 0.99 | 5.14 | 0.29 | 22.10 | 5/9 |
| LOWMOM_k5_excl_rollnear | 5 | 0.92 | 0.83 | 2.48 | 0.26 | 0.55 | 1.72 | 3.65 | 1.81 | 1.65 | 8.20 | 0.29 | 24 | 7/9 |
| LOWMOM_k5_excl_extreme | 5 | 1.04 | 0.98 | 2.97 | 0.57 | 1.22 | 1.67 | 3.58 | 1.73 | 1.60 | 7.90 | 0.29 | 23.30 | 7/9 |
| LOWMOM_k5_winsor | 5 | 1.00 | 0.93 | 2.88 | 0.50 | 1.10 | 1.62 | 3.55 | 1.69 | 1.55 | 7.49 | 0.29 | 22.30 | 7/9 |
| LOWMOM_k5_continuous | 5 | 0.90 | 0.84 | 2.62 | 0.49 | 1.07 | 1.39 | 3.06 | 1.47 | 1.33 | 5.38 | 0.22 | 18 | 7/9 |

### T10. LOWMOM yıllık demeaned Sharpe (VİOP)
| h | by_year |
|---|---|
| 1 | {"2017": 2.13, "2018": -0.16, "2019": -0.27, "2020": 3.25, "2021": 0.11, "2022": 0.53, "2023": 0.94, "2024": 1.79, "2025": 2.24} |
| 3 | {"2017": 2.02, "2018": -1.61, "2019": -0.35, "2020": 2.83, "2021": 0.53, "2022": 1.36, "2023": 0.76, "2024": 2.09, "2025": 1.83} |
| 5 | {"2017": 1.59, "2018": -1.65, "2019": -0.15, "2020": 2.68, "2021": 0.31, "2022": 1.15, "2023": 1.0, "2024": 2.12, "2025": 2.39} |

### T11. LOWMOM spot yıllık demeaned Sharpe 2011-2025 (spot hedef)
| h | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.00 | 1.34 | -0.02 | -0.34 | -0.00 | 0.56 | 1.92 | 1.74 | 0.04 | -0.37 | 3.06 | 0.38 | 0.48 | 0.67 | 2.32 | 2.30 |
| 3.00 | 0.97 | -0.05 | -0.54 | 1.04 | 0.70 | 1.38 | 1.58 | -1.47 | -0.11 | 2.49 | 0.69 | 1.13 | 0.51 | 1.86 | 1.86 |
| 5 | 0.73 | 0.11 | 0.10 | 1.74 | 0.37 | 0.59 | 1.22 | -1.70 | -0.25 | 2.55 | 0.10 | 1.27 | 0.70 | 1.73 | 1.99 |

### T12. VOLREG komşuluk duyarlılığı
| variant | h | shdm_full | t_full | shdm_is | shdm_oos | sh_oos | t_oos | yrs_pos | e_shdm | e_t | expo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VOLREG_5|k=3 | 1 | -0.11 | -0.35 | 0.09 | -0.23 | -0.24 | -0.52 | 3/10 | 0.18 | 0.49 | 0.73 |
| VOLREG_5|k=3 | 3 | 0.44 | 1.38 | 0.86 | 0.16 | 0.16 | 0.36 | 6/10 | -0.06 | -0.16 | 0.52 |
| VOLREG_5|k=3 | 5 | 0.75 | 2.32 | 1.01 | 0.61 | 0.61 | 1.35 | 7/10 | 0.11 | 0.30 | 0.42 |
| VOLREG_5|k=5 | 1 | 0.80 | 2.48 | 1.09 | 0.64 | 0.64 | 1.40 | 7/10 | 0.05 | 0.13 | 0.73 |
| VOLREG_5|k=5 | 3 | 1.00 | 3.10 | 1.31 | 0.85 | 0.86 | 1.87 | 8/10 | 0.04 | 0.09 | 0.57 |
| VOLREG_5|k=5 | 5 | 1.07 | 3.33 | 1.27 | 1.02 | 1.03 | 2.24 | 8/10 | 0.16 | 0.43 | 0.49 |
| VOLREG_5|k=10 | 1 | 0.38 | 1.17 | 0.10 | 0.60 | 0.59 | 1.33 | 6/10 | 0.36 | 0.97 | 0.73 |
| VOLREG_5|k=10 | 3 | 0.11 | 0.33 | 0.25 | 0.04 | 0.02 | 0.08 | 6/10 | 0.37 | 0.98 | 0.61 |
| VOLREG_5|k=10 | 5 | 0.09 | 0.28 | 0.36 | -0.05 | -0.06 | -0.10 | 6/10 | 0.51 | 1.37 | 0.56 |
| VOLREG_5|rvwin=10 | 1 | 0.34 | 1.05 | 0.45 | 0.29 | 0.30 | 0.64 | 6/10 | 0.26 | 0.71 | 0.71 |
| VOLREG_5|rvwin=10 | 3 | 0.54 | 1.68 | 0.62 | 0.52 | 0.54 | 1.15 | 7/10 | -0.02 | -0.05 | 0.55 |
| VOLREG_5|rvwin=10 | 5 | 0.64 | 2.00 | 0.84 | 0.58 | 0.59 | 1.27 | 6/10 | 0.06 | 0.16 | 0.47 |
| VOLREG_5|rvwin=60 | 1 | 0.76 | 2.37 | 0.74 | 0.80 | 0.82 | 1.76 | 8/10 | 0.16 | 0.42 | 0.71 |
| VOLREG_5|rvwin=60 | 3 | 0.71 | 2.22 | 0.72 | 0.73 | 0.76 | 1.61 | 8/10 | 0.30 | 0.82 | 0.56 |
| VOLREG_5|rvwin=60 | 5 | 0.82 | 2.54 | 0.75 | 0.90 | 0.92 | 1.97 | 8/10 | 0.45 | 1.22 | 0.47 |
| VOLREG_5|lo=0.25|hi=0.75 | 1 | 0.57 | 1.77 | 0.48 | 0.67 | 0.68 | 1.47 | 7/10 | 0.16 | 0.42 | 0.58 |
| VOLREG_5|lo=0.25|hi=0.75 | 3 | 0.77 | 2.37 | 0.74 | 0.83 | 0.84 | 1.82 | 8/10 | 0.11 | 0.29 | 0.45 |
| VOLREG_5|lo=0.25|hi=0.75 | 5 | 0.87 | 2.71 | 0.78 | 1.00 | 1.01 | 2.19 | 7/10 | 0.20 | 0.53 | 0.39 |
| VOLREG_5|lo=0.5|hi=0.5 | 1 | 0.63 | 1.94 | 1.17 | 0.27 | 0.28 | 0.59 | 7/10 | 0.06 | 0.17 | 1.00 |
| VOLREG_5|lo=0.5|hi=0.5 | 3 | 0.95 | 2.95 | 1.55 | 0.58 | 0.59 | 1.28 | 8/10 | -0.08 | -0.22 | 0.75 |
| VOLREG_5|lo=0.5|hi=0.5 | 5 | 1.07 | 3.33 | 1.50 | 0.87 | 0.88 | 1.92 | 8/10 | 0.18 | 0.48 | 0.63 |
| VOLREG_5|lo=0.2|hi=0.8 | 1 | 0.59 | 1.83 | 0.73 | 0.54 | 0.54 | 1.18 | 7/10 | 0.17 | 0.46 | 0.49 |
| VOLREG_5|lo=0.2|hi=0.8 | 3 | 0.61 | 1.91 | 0.59 | 0.66 | 0.67 | 1.45 | 7/10 | 0.06 | 0.16 | 0.38 |
| VOLREG_5|lo=0.2|hi=0.8 | 5 | 0.78 | 2.41 | 0.67 | 0.89 | 0.89 | 1.94 | 7/10 | 0.17 | 0.45 | 0.33 |
| VOLREG_5|qmode=500 | 1 | 0.79 | 2.44 | 1.06 | 0.63 | 0.62 | 1.38 | 7/10 | 0.06 | 0.15 | 0.73 |
| VOLREG_5|qmode=500 | 3 | 1.00 | 3.10 | 1.42 | 0.76 | 0.76 | 1.68 | 8/10 | -0.07 | -0.18 | 0.56 |
| VOLREG_5|qmode=500 | 5 | 1.05 | 3.26 | 1.36 | 0.92 | 0.91 | 2.02 | 8/10 | 0.04 | 0.10 | 0.48 |
| VOLREG_5|qmode=750 | 1 | 0.72 | 2.24 | 0.98 | 0.56 | 0.56 | 1.24 | 7/10 | 0.24 | 0.63 | 0.72 |
| VOLREG_5|qmode=750 | 3 | 1.04 | 3.24 | 1.41 | 0.84 | 0.85 | 1.86 | 9/10 | 0.34 | 0.90 | 0.56 |
| VOLREG_5|qmode=750 | 5 | 1.11 | 3.43 | 1.40 | 0.98 | 0.99 | 2.16 | 9/10 | 0.41 | 1.09 | 0.48 |
| VOLREG_5|qmode=1250 | 1 | 0.83 | 2.57 | 1.27 | 0.55 | 0.55 | 1.22 | 7/10 | 0.54 | 1.44 | 0.77 |
| VOLREG_5|qmode=1250 | 3 | 1.05 | 3.25 | 1.56 | 0.75 | 0.75 | 1.65 | 8/10 | 0.49 | 1.32 | 0.60 |
| VOLREG_5|qmode=1250 | 5 | 1.07 | 3.33 | 1.42 | 0.91 | 0.91 | 2.00 | 8/10 | 0.40 | 1.08 | 0.51 |
| VOLREG_5|side=lo | 1 | 0.99 | 3.06 | 0.82 | 1.31 | 1.36 | 2.88 | 7/10 | 0.51 | 1.38 | 0.41 |
| VOLREG_5|side=lo | 3 | 0.89 | 2.75 | 0.58 | 1.40 | 1.46 | 3.09 | 7/10 | 0.57 | 1.53 | 0.33 |
| VOLREG_5|side=lo | 5 | 0.95 | 2.96 | 0.55 | 1.63 | 1.69 | 3.58 | 7/10 | 0.58 | 1.56 | 0.29 |
| VOLREG_5|side=hi | 1 | 0.34 | 1.06 | 0.72 | 0.17 | 0.16 | 0.38 | 5/10 | -0.32 | -0.87 | 0.32 |
| VOLREG_5|side=hi | 3 | 0.63 | 1.97 | 1.33 | 0.38 | 0.37 | 0.85 | 7/10 | -0.43 | -1.15 | 0.25 |
| VOLREG_5|side=hi | 5 | 0.67 | 2.09 | 1.34 | 0.46 | 0.45 | 1.02 | 7/10 | -0.27 | -0.73 | 0.20 |

### T13. VOLREG bacaklar × dönem (spot hedef)
| side | h | donem | hedef | shdm | t | expo |
|---|---|---|---|---|---|---|
| both | 1 | 2010-2016 | spot 15->15 | 0.05 | 0.13 | 0.60 |
| both | 1 | 2017-2021 | spot 15->15 | 1.10 | 2.45 | 0.79 |
| both | 1 | 2022-2026 | spot 15->15 | 0.88 | 1.97 | 0.67 |
| both | 1 | 2010-2026 | spot 15->15 | 0.57 | 2.38 | 0.67 |
| both | 3 | 2010-2016 | spot 15->15 | 0.04 | 0.09 | 0.48 |
| both | 3 | 2017-2021 | spot 15->15 | 1.34 | 2.98 | 0.62 |
| both | 3 | 2022-2026 | spot 15->15 | 0.87 | 1.95 | 0.53 |
| both | 3 | 2010-2026 | spot 15->15 | 0.61 | 2.56 | 0.53 |
| both | 5 | 2010-2016 | spot 15->15 | 0.16 | 0.43 | 0.43 |
| both | 5 | 2017-2021 | spot 15->15 | 1.13 | 2.53 | 0.52 |
| both | 5 | 2022-2026 | spot 15->15 | 0.97 | 2.15 | 0.46 |
| both | 5 | 2010-2026 | spot 15->15 | 0.65 | 2.69 | 0.46 |
| lo | 1 | 2010-2016 | spot 15->15 | 0.51 | 1.38 | 0.34 |
| lo | 1 | 2017-2021 | spot 15->15 | 0.79 | 1.76 | 0.59 |
| lo | 1 | 2022-2026 | spot 15->15 | 1.35 | 3.01 | 0.23 |
| lo | 1 | 2010-2026 | spot 15->15 | 0.80 | 3.34 | 0.38 |
| lo | 3 | 2010-2016 | spot 15->15 | 0.57 | 1.53 | 0.28 |
| lo | 3 | 2017-2021 | spot 15->15 | 0.60 | 1.34 | 0.47 |
| lo | 3 | 2022-2026 | spot 15->15 | 1.22 | 2.72 | 0.19 |
| lo | 3 | 2010-2026 | spot 15->15 | 0.73 | 3.02 | 0.31 |
| lo | 5 | 2010-2016 | spot 15->15 | 0.58 | 1.56 | 0.25 |
| lo | 5 | 2017-2021 | spot 15->15 | 0.43 | 0.95 | 0.40 |
| lo | 5 | 2022-2026 | spot 15->15 | 1.33 | 2.96 | 0.18 |
| lo | 5 | 2010-2026 | spot 15->15 | 0.71 | 2.94 | 0.27 |
| hi | 1 | 2010-2016 | spot 15->15 | -0.32 | -0.87 | 0.26 |
| hi | 1 | 2017-2021 | spot 15->15 | 0.76 | 1.70 | 0.20 |
| hi | 1 | 2022-2026 | spot 15->15 | 0.40 | 0.89 | 0.44 |
| hi | 1 | 2010-2026 | spot 15->15 | 0.15 | 0.63 | 0.29 |
| hi | 3 | 2010-2016 | spot 15->15 | -0.43 | -1.15 | 0.20 |
| hi | 3 | 2017-2021 | spot 15->15 | 1.37 | 3.05 | 0.15 |
| hi | 3 | 2022-2026 | spot 15->15 | 0.44 | 0.97 | 0.34 |
| hi | 3 | 2010-2026 | spot 15->15 | 0.24 | 1.00 | 0.23 |
| hi | 5 | 2010-2016 | spot 15->15 | -0.27 | -0.73 | 0.18 |
| hi | 5 | 2017-2021 | spot 15->15 | 1.30 | 2.89 | 0.12 |
| hi | 5 | 2022-2026 | spot 15->15 | 0.46 | 1.03 | 0.29 |
| hi | 5 | 2010-2026 | spot 15->15 | 0.29 | 1.20 | 0.19 |

### T14. Rejim payları (yıl içi gün oranı)
| index | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lo | 0.00 | 0.35 | 0.44 | 0.26 | 0.62 | 0.38 | 0.35 | 0.86 | 0.87 | 0.72 | 0.20 | 0.23 | 0.16 | 0.45 | 0.30 | 0.22 | 0.00 |
| hi | 0.00 | 0.47 | 0.39 | 0.50 | 0.08 | 0.08 | 0.31 | 0.03 | 0.00 | 0.06 | 0.60 | 0.30 | 0.31 | 0.21 | 0.34 | 0.45 | 0.98 |

### T15. Sağlamlık (IC)
| sig | h | base | excl_roll_win | excl_roll_near | excl_extreme | winsor_y | excl_lowliq | pre_evening | post_evening | pearson |
|---|---|---|---|---|---|---|---|---|---|---|
| ret5_loV|spot | 1 | (0.1172, 3.45) | (0.109, 3.19) | (0.0909, 2.54) | (0.1172, 3.45) | (0.1172, 3.45) | (0.1243, 3.48) | (0.0964, 2.35) | (0.1583, 2.69) | (0.1347, 3.9) |
| ret5_loV|spot | 3 | (0.1232, 2.53) | (0.1042, 2.09) | (0.0842, 1.66) | (0.1232, 2.53) | (0.1232, 2.53) | (0.122, 2.5) | (0.0487, 0.81) | (0.2594, 3.31) | (0.1621, 3.07) |
| ret5_loV|spot | 5 | (0.1295, 2.51) | (0.0919, 1.69) | (0.0967, 1.8) | (0.1295, 2.51) | (0.1295, 2.51) | (0.126, 2.42) | (0.0337, 0.52) | (0.298, 3.72) | (0.1716, 2.96) |
| ret5_hiV|spot | 1 | (-0.0437, -1.19) | (-0.0444, -1.2) | (-0.0394, -1.04) | (-0.0542, -1.45) | (-0.0438, -1.19) | (-0.0507, -1.34) | (-0.2127, -2.1) | (-0.0196, -0.5) | (-0.0384, -0.75) |
| ret5_hiV|spot | 3 | (-0.1033, -2.01) | (-0.0948, -1.79) | (-0.0897, -1.71) | (-0.1137, -2.24) | (-0.1032, -2.01) | (-0.107, -1.97) | (-0.3615, -2.66) | (-0.0657, -1.2) | (-0.1176, -1.74) |
| ret5_hiV|spot | 5 | (-0.1524, -2.88) | (-0.1627, -2.87) | (-0.1286, -2.37) | (-0.1397, -2.67) | (-0.1526, -2.89) | (-0.1649, -2.97) | (-0.4146, -4.03) | (-0.1184, -2.04) | (-0.1817, -2.74) |
| ret1_loV|spot | 1 | (0.0981, 2.74) | (0.0927, 2.53) | (0.0924, 2.49) | (0.0981, 2.74) | (0.0981, 2.74) | (0.0983, 2.51) | (0.1037, 2.34) | (0.0894, 1.47) | (0.086, 2.29) |
| ret1_loV|spot | 3 | (0.1107, 3.19) | (0.1021, 2.84) | (0.0922, 2.6) | (0.1107, 3.19) | (0.1107, 3.19) | (0.1143, 3.11) | (0.1034, 2.53) | (0.1304, 2.07) | (0.1086, 2.91) |
| ret1_loV|spot | 5 | (0.1082, 3.1) | (0.0838, 2.27) | (0.1005, 2.82) | (0.1082, 3.1) | (0.1082, 3.1) | (0.1121, 3.09) | (0.0837, 1.94) | (0.1548, 2.61) | (0.1158, 2.92) |
| z1|spot | 1 | (0.0342, 1.72) | (0.0341, 1.69) | (0.0392, 1.92) | (0.0323, 1.57) | (0.0342, 1.72) | (0.0388, 1.83) | (0.0719, 1.97) | (0.0166, 0.7) | (0.0451, 2.01) |
| z1|spot | 3 | (0.0389, 1.89) | (0.037, 1.77) | (0.0413, 1.96) | (0.0365, 1.74) | (0.0389, 1.89) | (0.0456, 2.08) | (0.0854, 2.5) | (0.016, 0.62) | (0.0343, 1.54) |
| z1|spot | 5 | (0.0175, 0.81) | (0.0097, 0.43) | (0.023, 1.04) | (0.0135, 0.6) | (0.0175, 0.81) | (0.0224, 0.97) | (0.0256, 0.69) | (0.0144, 0.54) | (0.0197, 0.81) |
| segD_13_15|spot | 1 | (0.0545, 2.49) | (0.0562, 2.56) | (0.0568, 2.52) | (0.0376, 1.67) | (0.0544, 2.49) | (0.0582, 2.52) | (0.0893, 2.37) | (0.0393, 1.48) | (0.0706, 2.87) |
| segD_13_15|spot | 3 | (0.0431, 2.03) | (0.044, 2.0) | (0.0485, 2.2) | (0.026, 1.19) | (0.0431, 2.03) | (0.0343, 1.51) | (0.0542, 1.52) | (0.037, 1.43) | (0.0705, 3.23) |
| segD_13_15|spot | 5 | (0.0541, 2.45) | (0.0607, 2.56) | (0.0605, 2.62) | (0.0339, 1.55) | (0.0541, 2.45) | (0.0578, 2.45) | (0.024, 0.59) | (0.0639, 2.48) | (0.088, 3.18) |
| loc_s|spot | 1 | (0.0426, 2.09) | (0.0413, 1.99) | (0.042, 1.99) | (0.0316, 1.51) | (0.0426, 2.09) | (0.0468, 2.18) | (0.0841, 2.38) | (0.0245, 0.98) | (0.0429, 2.19) |
| loc_s|spot | 3 | (0.0432, 2.14) | (0.0415, 2.01) | (0.0424, 2.07) | (0.0294, 1.43) | (0.0432, 2.14) | (0.0426, 1.97) | (0.0672, 1.97) | (0.0321, 1.29) | (0.0437, 2.16) |
| loc_s|spot | 5 | (0.0374, 1.82) | (0.033, 1.53) | (0.0402, 1.91) | (0.0243, 1.16) | (0.0374, 1.82) | (0.0431, 1.98) | (0.0218, 0.62) | (0.0467, 1.84) | (0.0416, 1.92) |
| pma50|vt | 1 | (0.0519, 2.56) | (0.0512, 2.49) | (0.0508, 2.4) | (0.0486, 2.32) | (0.0519, 2.56) | (0.0425, 2.0) | (0.0377, 1.09) | (0.0588, 2.35) | (0.0383, 1.97) |
| pma50|vt | 3 | (0.0738, 2.43) | (0.0652, 2.08) | (0.0688, 2.23) | (0.0715, 2.28) | (0.0738, 2.43) | (0.0571, 1.85) | (0.0293, 0.58) | (0.0947, 2.5) | (0.0564, 1.87) |
| pma50|vt | 5 | (0.0817, 2.29) | (0.0725, 1.95) | (0.0788, 2.16) | (0.0868, 2.36) | (0.0817, 2.29) | (0.0626, 1.74) | (0.04, 0.68) | (0.1024, 2.28) | (0.0705, 2.0) |
| sc|mt | 1 | (-0.0681, -2.92) | (-0.0657, -2.75) | (-0.0677, -2.79) | (-0.0765, -3.28) | (-0.0682, -2.93) | (-0.0741, -2.97) | (-0.0972, -2.77) | (-0.0552, -1.85) | (-0.0833, -2.39) |
| sc|mt | 3 | (-0.0246, -1.14) | (-0.0208, -0.92) | (-0.0283, -1.28) | (-0.0267, -1.23) | (-0.0245, -1.14) | (-0.0278, -1.21) | (-0.0494, -1.39) | (-0.0133, -0.5) | (-0.0764, -1.7) |
| sc|mt | 5 | (-0.026, -1.21) | (-0.0192, -0.83) | (-0.025, -1.1) | (-0.0201, -0.93) | (-0.026, -1.21) | (-0.03, -1.28) | (-0.0382, -1.02) | (-0.0184, -0.69) | (-0.0586, -1.76) |
| rsi14_lo|vt1 | 1 | (-0.0027, -0.16) | (-0.0018, -0.11) | (0.0029, 0.17) | (-0.0018, -0.11) | (-0.0027, -0.17) | (-0.0157, -0.89) | (-0.0157, -0.58) | (0.0044, 0.21) | (0.0071, 0.43) |
| rsi14_lo|vt1 | 3 | (0.0486, 2.01) | (0.0498, 1.99) | (0.0578, 2.32) | (0.0516, 2.03) | (0.0486, 2.01) | (0.0353, 1.39) | (0.0206, 0.51) | (0.0662, 2.17) | (0.0506, 2.22) |
| rsi14_lo|vt1 | 5 | (0.0788, 2.93) | (0.0782, 2.64) | (0.0902, 3.23) | (0.0774, 2.79) | (0.0788, 2.93) | (0.0679, 2.54) | (0.0495, 1.03) | (0.0974, 3.02) | (0.0706, 3.05) |

### T16. Sağlamlık (backtest, demeaned Sharpe, t)
| sig | h | base_dm | excl_extreme_dm | excl_roll_near_dm | winsor_dm | excl_lowliq_dm | pre_evening_dm | post_evening_dm |
|---|---|---|---|---|---|---|---|---|
| TAILMOM_z2.0 | 1 | (0.29, 0.91) | (0.36, 1.09) | (0.34, 1.02) | (0.31, 0.96) | (0.41, 1.21) | (-0.12, -0.23) | (0.43, 1.05) |
| TAILMOM_z2.0 | 3 | (0.14, 0.43) | (0.35, 1.06) | (0.14, 0.43) | (0.28, 0.87) | (0.16, 0.47) | (0.38, 0.71) | (0.04, 0.1) |
| TAILMOM_z2.0 | 5 | (0.0, 0.01) | (0.36, 1.09) | (0.15, 0.45) | (0.18, 0.56) | (0.05, 0.15) | (-0.19, -0.36) | (0.07, 0.18) |
| TAILMOM_bb2.0 | 1 | (0.47, 1.46) | (0.66, 2.01) | (0.61, 1.83) | (0.62, 1.92) | (0.49, 1.43) | (1.08, 2.03) | (0.29, 0.71) |
| TAILMOM_bb2.0 | 3 | (0.36, 1.13) | (0.55, 1.67) | (0.4, 1.18) | (0.54, 1.66) | (0.29, 0.84) | (0.56, 1.04) | (0.3, 0.75) |
| TAILMOM_bb2.0 | 5 | (0.05, 0.15) | (0.22, 0.65) | (0.04, 0.13) | (0.2, 0.62) | (-0.08, -0.22) | (-0.01, -0.01) | (0.07, 0.18) |
| VOLREG_5 | 1 | (0.8, 2.48) | (0.93, 2.83) | (0.75, 2.23) | (0.84, 2.61) | (0.67, 1.96) | (1.25, 2.35) | (0.61, 1.51) |
| VOLREG_5 | 3 | (1.0, 3.1) | (1.1, 3.34) | (0.92, 2.76) | (1.01, 3.13) | (0.89, 2.61) | (1.24, 2.32) | (0.91, 2.25) |
| VOLREG_5 | 5 | (1.07, 3.33) | (1.2, 3.64) | (1.05, 3.12) | (1.09, 3.38) | (0.98, 2.86) | (1.19, 2.23) | (1.03, 2.56) |
| VOLREG_1 | 1 | (0.01, 0.03) | (0.13, 0.4) | (-0.09, -0.26) | (0.05, 0.14) | (0.16, 0.47) | (0.06, 0.11) | (-0.02, -0.05) |
| VOLREG_1 | 3 | (0.18, 0.54) | (0.32, 0.98) | (0.15, 0.43) | (0.19, 0.58) | (0.25, 0.72) | (0.53, 1.0) | (-0.01, -0.03) |
| VOLREG_1 | 5 | (0.59, 1.83) | (0.75, 2.28) | (0.55, 1.66) | (0.62, 1.92) | (0.53, 1.55) | (0.76, 1.42) | (0.5, 1.24) |
| PMA_50 | 1 | (0.34, 1.06) | (0.34, 1.04) | (0.23, 0.68) | (0.44, 1.38) | (0.21, 0.62) | (0.01, 0.02) | (0.48, 1.18) |
| PMA_50 | 3 | (0.3, 0.93) | (0.39, 1.17) | (0.17, 0.52) | (0.41, 1.29) | (0.14, 0.42) | (-0.19, -0.35) | (0.49, 1.22) |
| PMA_50 | 5 | (0.28, 0.87) | (0.4, 1.2) | (0.16, 0.47) | (0.41, 1.27) | (0.1, 0.3) | (-0.13, -0.24) | (0.44, 1.09) |
| X_x20_100 | 1 | (0.32, 1.01) | (0.35, 1.07) | (0.18, 0.54) | (0.42, 1.31) | (0.06, 0.17) | (0.01, 0.01) | (0.45, 1.11) |
| X_x20_100 | 3 | (0.35, 1.08) | (0.38, 1.15) | (0.2, 0.6) | (0.45, 1.38) | (0.07, 0.2) | (-0.01, -0.02) | (0.49, 1.21) |
| X_x20_100 | 5 | (0.39, 1.22) | (0.43, 1.31) | (0.25, 0.74) | (0.49, 1.54) | (0.1, 0.29) | (-0.01, -0.02) | (0.55, 1.37) |
| W52_NEARHIGH_LONG | 1 | (0.47, 1.45) | (0.44, 1.34) | (0.5, 1.49) | (0.56, 1.73) | (0.39, 1.13) | (0.08, 0.15) | (0.65, 1.61) |
| W52_NEARHIGH_LONG | 3 | (0.34, 1.05) | (0.41, 1.24) | (0.34, 1.01) | (0.48, 1.47) | (0.24, 0.7) | (-0.1, -0.18) | (0.54, 1.33) |
| W52_NEARHIGH_LONG | 5 | (0.37, 1.16) | (0.46, 1.38) | (0.38, 1.13) | (0.54, 1.66) | (0.27, 0.79) | (-0.06, -0.11) | (0.57, 1.41) |

### T17. Placebo (s<0 = gelecek bilgisi, s>0 = daha eski bilgi), Spearman IC
| sig | h | s-2 | s-1 | s0 | s1 | s2 | s3 |
|---|---|---|---|---|---|---|---|
| ret1|spot | 1 | 0.045 | 0.946 | 0.024 | -0.002 | 0.028 | -0.027 |
| ret1|spot | 5 | 0.426 | 0.390 | 0.005 | -0.029 | -0.006 | -0.017 |
| ret1|vt | 1 | 0.023 | 1.000 | 0.023 | -0.001 | 0.023 | -0.025 |
| ret1|vt | 5 | 0.438 | 0.411 | 0.004 | -0.024 | -0.005 | -0.017 |
| ret1|vt1 | 1 | 1.000 | 0.023 | -0.001 | 0.023 | -0.025 | 0.015 |
| ret1|vt1 | 5 | 0.411 | 0.004 | -0.024 | -0.005 | -0.017 | -0.010 |
| sc|mt | 1 | 0.011 | -0.074 | -0.068 | 0.003 | 0.032 | -0.015 |
| sc|mt | 5 | -0.041 | -0.059 | -0.026 | 0.013 | 0.018 | 0.034 |
| sc|mt1 | 1 | -0.074 | -0.068 | 0.003 | 0.032 | -0.015 | 0.012 |
| sc|mt1 | 5 | -0.059 | -0.026 | 0.013 | 0.018 | 0.034 | 0.033 |
| svw|mt | 1 | -0.006 | 0.615 | 0.022 | 0.006 | 0.018 | 0.021 |
| svw|mt | 5 | 0.282 | 0.289 | 0.034 | 0.007 | 0.013 | -0.004 |
| svw|mt1 | 1 | 0.615 | 0.022 | 0.006 | 0.018 | 0.021 | 0.015 |
| svw|mt1 | 5 | 0.289 | 0.034 | 0.007 | 0.013 | -0.004 | -0.019 |
| loc_v|mt | 1 | 0.019 | 0.634 | 0.016 | 0.020 | 0.026 | 0.019 |
| loc_v|mt | 5 | 0.297 | 0.293 | 0.031 | 0.012 | 0.017 | -0.001 |
| loc_v|mt1 | 1 | 0.634 | 0.016 | 0.020 | 0.026 | 0.019 | 0.007 |
| loc_v|mt1 | 5 | 0.293 | 0.031 | 0.012 | 0.017 | -0.001 | -0.015 |
| loc_s|spot | 1 | -0.011 | 0.785 | 0.043 | 0.009 | 0.025 | 0.011 |
| loc_s|spot | 5 | 0.352 | 0.357 | 0.037 | -0.003 | 0.013 | 0.002 |
| segD_13_15|spot | 1 | -0.009 | 0.453 | 0.054 | -0.002 | 0.035 | 0.023 |
| segD_13_15|spot | 5 | 0.232 | 0.245 | 0.054 | 0.017 | 0.020 | -0.000 |
| rsi2|spot | 1 | 0.479 | 0.737 | 0.029 | 0.010 | 0.011 | -0.008 |
| rsi2|spot | 5 | 0.520 | 0.298 | 0.002 | -0.012 | 0.005 | 0.002 |
| rsi2|vt | 1 | 0.486 | 0.755 | 0.029 | 0.013 | 0.016 | -0.003 |
| rsi2|vt | 5 | 0.533 | 0.311 | 0.008 | -0.004 | 0.006 | 0.001 |
| vshock|mt | 1 | 0.069 | 0.033 | -0.001 | 0.003 | 0.004 | 0.019 |
| vshock|mt | 5 | 0.014 | -0.008 | -0.011 | 0.011 | 0.024 | 0.024 |
| doi|mt | 1 | 0.055 | -0.105 | -0.016 | -0.009 | -0.021 | 0.007 |
| doi|mt | 5 | -0.029 | -0.057 | -0.010 | 0.018 | 0.026 | 0.023 |
| ret5_loV|spot | 1 | 0.471 | 0.458 | 0.117 | 0.075 | 0.049 | 0.057 |
| ret5_loV|spot | 3 | 0.538 | 0.326 | 0.123 | 0.091 | 0.072 | 0.043 |
| ret5_loV|spot | 5 | 0.437 | 0.277 | 0.130 | 0.083 | 0.050 | 0.020 |

### T18. Gün içi segment / konum: spot hedefle dönem kıyası
| sig | h | donem | hedef | ic | t |
|---|---|---|---|---|---|
| segD_13_15 | 1 | 2010-2016 | spot 15:00->15:00 | -0.04 | -1.84 |
| segD_13_15 | 1 | 2017-2021 | spot 15:00->15:00 | 0.06 | 1.96 |
| segD_13_15 | 1 | 2022-2026 | spot 15:00->15:00 | 0.03 | 1.13 |
| loc_s | 1 | 2010-2016 | spot 15:00->15:00 | -0.01 | -0.64 |
| loc_s | 1 | 2017-2021 | spot 15:00->15:00 | 0.05 | 1.94 |
| loc_s | 1 | 2022-2026 | spot 15:00->15:00 | 0.01 | 0.48 |
| segD_13_15 | 3 | 2010-2016 | spot 15:00->15:00 | -0.03 | -1.37 |
| segD_13_15 | 3 | 2017-2021 | spot 15:00->15:00 | 0.01 | 0.45 |
| segD_13_15 | 3 | 2022-2026 | spot 15:00->15:00 | 0.06 | 2.11 |
| loc_s | 3 | 2010-2016 | spot 15:00->15:00 | -0.00 | -0.02 |
| loc_s | 3 | 2017-2021 | spot 15:00->15:00 | 0.02 | 0.52 |
| loc_s | 3 | 2022-2026 | spot 15:00->15:00 | 0.05 | 1.67 |
| segD_13_15 | 5 | 2010-2016 | spot 15:00->15:00 | -0.01 | -0.24 |
| segD_13_15 | 5 | 2017-2021 | spot 15:00->15:00 | 0.01 | 0.26 |
| segD_13_15 | 5 | 2022-2026 | spot 15:00->15:00 | 0.06 | 1.93 |
| loc_s | 5 | 2010-2016 | spot 15:00->15:00 | 0.02 | 1.00 |
| loc_s | 5 | 2017-2021 | spot 15:00->15:00 | -0.00 | -0.15 |
| loc_s | 5 | 2022-2026 | spot 15:00->15:00 | 0.04 | 1.55 |