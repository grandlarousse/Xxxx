# a3_takvim_olay — Takvim ve olay etkileri: VİOP Ons Altın (F_XAUUSD), uzlaşmadan uzlaşmaya 1-3-5 gün

**Kısa sonuç.** 178 yön testi ve 4 oynaklık testi yapıldı (toplam 182 kayıt). Bunların 22'sinde |t| ≥ 2 çıktı; şans eseri yaklaşık 8 beklenirdi. 7 testte |t| ≥ 3 çıktı; şans eseri 0,5 beklenirdi. Yani takvim ailesinde gürültünün üstünde bir şey var, ama çoğu aday sağlamlık kontrollerinden geçemedi. Ayakta kalan iki kural var, ikisi de **ORTA** güvende:

1. **Çeyrek dönümü (QEND):** Mart, Haziran, Eylül ve Aralık'ın sondan ikinci VİOP günü uzlaşmasında uzun girip 3 gün tutmak. Olay başına ortalama +77 bps getirdi, diğer günlerin ortalaması +8 bps. Fark t = 3,08 (IS 2,13, OOS 2,26). 10 yılın 8'inde işaret aynı. Spot veride 2010–2026 aralığında da var (t = 3,29). Ancak mekanizma doğrulanamadı ve olay sayısı yalnızca 39.
2. **NFP tepki momentumu:** NFP gününde spot XAUUSD'nin 12:00→15:00 UTC (15:00→18:00 TSİ) yönünde uzlaşmada girip 1 gün (Cuma→Pazartesi) ya da 3 gün tutmak. 2022 sonrasında güçlü (OOS t = 3,5–7), 2017–2021'de zayıf (IS t = 0,6–0,8), 2010–2016 spot veride ise ters işaretli (t ≈ −1,0/−1,2). Rejime bağımlı.

Geri kalan ailelerin hiçbirinde güvenilir bir 1–5 günlük yön kenarı bulunamadı: haftanın günü, genel ay dönümü, ay mevsimselliği (Baur'un Eylül/Kasım etkisi dahil), FOMC öncesi/günü/sonrası, CPI, tatil öncesi/sonrası, COMEX opsiyon vadesi/FND/BCOM roll, VİOP vadesi, Çin Yeni Yılı, Altın Haftası, Diwali ve Akshaya Tritiya. Ayrıntı için §5'e bakın.

---

## 1. Veri ve zaman kuralları

- **Hedef:** `fwd{h}`, yani VİOP aktif kontratın gün t uzlaşmasından (≈15:05–15:15 UTC VWAP) t+h uzlaşmasına kadarki log getirisi. h = 1, 3, 5. Panel 2017-03-06 → 2026-11-06, 2.427 gün. Al-tut Sharpe değeri tam dönemde 0,49, IS'te 0,48, OOS'ta 0,51. Bu bir vadeli getirisi olduğu için taşıma maliyeti düşülmüş halde: `v_ret`, 15:00 UTC spot getirisinden günde ortalama 1,9 bps düşük (yılda yaklaşık %4,7, USD faizine uyuyor).
- **Erken dönem tekrarı:** `panel_spot`, Dukascopy XAUUSD 15:00→15:00 UTC (`sfwd{h}`), 2010-01-04 → 2017-03-03. Aynı takvim tanımları spot iş günü takvimine eşlendi.
- **Karar anı:** gün t 15:00 UTC. Takvim kuklaları (FOMC, CPI ve NFP takvimleri, tatiller, vadeler) aylar ya da yıllar önceden bilinir, dolayısıyla ileriye bakma riski yok. Plansız FOMC toplantıları (03.03.2020 ve 15.03.2020) kullanılmadı. Koşullu sinyaller yalnız `xau_p12` ve `xau_p15` kullanıyor (gün t 12:00 ve 15:00 UTC spot), ikisi de 15:00 UTC'de biliniyor. `v_ret_t` kullanan varyantlar **"kapanışta hesaplanan"** diye işaretlendi (15:10 UTC).
- **Veri uyarısı (diğer ajanlar için de önemli):** Türkiye yarım günlerinde (bayram arifeleri ve 28 Ekim) VİOP normal seansı erken kapanıyor. Uzlaşma 15:10 UTC'deki değil, yaklaşık 09:30–10:00 UTC'deki fiyatı yansıtıyor. Uzlaşma ile spot arasındaki mutlak sapmanın medyanı yarım günlerde 15:00 spota göre 56 bps, 12:00 spota göre 26 bps. Normal günlerde 15:00'e göre 29 bps. Örnek: 19.03.2026 uzlaşması 4.771,5, spot 07:00'de 4.763, 15:00'te 4.602. Bu günlerde `xau_p15` ile kurulan her sinyal ileriye bakar. Bu çalışmadaki spot tabanlı koşullu sinyallerde yarım günler dışlandı.
- **Roll günleri** (`v_code` değişimi, 60 gün): Roll günü `v_ret` ortalaması −26,6 bps, aynı günlerin spot 15:00 getirisi −26,2 bps. Yani veri hatası yok, düşüş gerçek fiyat hareketi. Aktif kontratta sıfır hacimli gün yok (en düşük hacim 600 kontrat).

## 2. Olay takvimleri (kurulan dosyalar)

`data/events/` boştu, bu yüzden takvimler kod içinde kuruldu (`build_events.py`).

| Dosya | İçerik ve kaynak | Not |
|---|---|---|
| `events_fomc.csv` | 2009–2027 planlı toplantılar (karar günü). 2009–2020 federalreserve.gov `fomchistorical<YIL>.htm`, 2021–2027 `data/misc/fomc_calendar.html` | Açıklama 18:00/19:00 UTC (2013 öncesi 18:15/19:15; 2011–12'deki basın toplantılı toplantılarda 12:30 ET). Hepsi uzlaşmadan **sonra**. |
| `events_us_cpi.csv`, `events_us_nfp.csv` | BLS arşiv sayfalarındaki bağlantılarda yer alan **gerçek** yayım tarihleri (MMDDYYYY). CPI 213, NFP 215 yayım. | 08:30 ET = 12:30 UTC (yaz) / 13:30 UTC (kış). 2013 ve 2025 hükümet kapanması gecikmeleri dahil. Ekim 2025 CPI yayımlanmadı. |
| `events_comex.csv` | OG opsiyon vadesi = opsiyon ayından önceki ayın **sondan 4. iş günü**; Cuma ya da tatil arifesine denk gelirse bir önceki iş günü. GC FND = teslim ayından önceki ayın son iş günü. BCOM roll = Ocak, Mart, Mayıs, Temmuz ve Kasım'ın 6.–10. iş günleri. | Kural bilinen vadelerle tutuyor: OGZ25 = 24.11.2025, OGG26 = 27.01.2026, OGJ25 = 26.03.2025, OGM25 = 27.05.2025, OGV25 = 25.09.2025. Görev metnindeki "son iş gününden 4 iş günü önce" tanımı `og_alt` sütununda duyarlılık için ayrıca tutuldu. CME sayfası 403 verdi, kural belgeden doğrulanamadı. |
| `events_tatiller.csv` | `holidays` 0.108 paketi: NYSE, XLON (LSE), XSHG (Şanghay), Türkiye | TR kapanışları ayrıca VİOP takvimindeki boşluklardan da çıkarıldı. |
| `events_tr_bayram.csv` | Ramazan ve Kurban Bayramı başlangıcı ve arifesi (holidays.Turkey) | |
| `events_asya_festival.csv` | Çin Yeni Yılı (ay takvimi), Altın Haftası (1 Ekim), Diwali (holidays.India), Dhanteras = Diwali − 2 gün (yaklaşık), Akshaya Tritiya | Akshaya Tritiya tarihleri 2021–2026 için drikpanchang.com'dan doğrulandı. 2010–2020 tarihleri bellekten geliyor (DÜŞÜK güven). Web arama kotası dolduğu için ek doğrulama yapılamadı. |

## 3. Yöntem

- **Kukla testi:** D_t = 1 ise gün t uzlaşmasında gir, h gün tut. Etki = ort(fwd_h | D = 1) − ort(fwd_h | D = 0). t değeri, `lib_altin.ic(method='pearson')` ile Newey–West (lag = max(h, 5)) altında y ~ a + b·D regresyonunun t'sidir. IS 2017-03..2021-12, OOS 2022-01..2026-11. Yıl yıl farkın işareti ayrıca sayıldı. Erken spot tekrarı aynı tanımlarla 2010–2017/03 aralığında yapıldı.
- **Koşullu olay testi** (CPI, NFP, FOMC): yalnız olay günlerinde x = tepki. Tablodaki t, sürekli tepkiyle fwd_h arasındaki Pearson IC'nin NW t'sidir. İşlem kuralı ise tepkinin **işaretini** kullanır; işarete dayalı t ayrıca verildi.
- **Backtest:** pos = sign(IS etkisi) × D. Yön yalnız IS'ten seçildi, OOS tek sefer değerlendirildi. Kullanılanlar: `bt_summary` (5 bps gidiş-dönüş), 10 bps stres, demeaned Sharpe, uzun ve kısa bacak ayrı, OOS al-tut Sharpe karşılaştırması.
- **Sağlamlık:** (i) Mart 2020 ile Ocak–Şubat 2026 hariç tutuldu, (ii) roll gününe dokunan pencereler hariç tutuldu, (iii) %0,5 winsorize, (iv) Spearman. Adaylar için ayrıca komşu pencereler, kontrol grupları ve placebo_lead testleri yapıldı.
- **Çoklu test:** Yön testlerinin (178) içinde Benjamini–Hochberg uygulandı. Bonferroni için |t| eşiği 3,63 (182 testte %5).

## 4. Aday bulgular

### 4.1 Çeyrek dönümü: QEND_TDE1_h3 — ORTA

**Kural:** Mart, Haziran, Eylül ve Aralık'ın sondan 2. VİOP işlem günü (TDE1) uzlaşmasında F_XAUUSD aktif kontratta uzun gir. 3 VİOP günü sonraki uzlaşmada (yeni çeyreğin 2. işlem günü) çık. Yılda 4 işlem, ortalama pozisyon payı %2. Haziran ve Aralık'ta bu tarih roll'dan sonraya düşer; yeni aktif kontrat kullanılır.

| Ölçü | Değer |
|---|---|
| Olay sayısı (VİOP) | 39 |
| Olay ortalaması fwd3 / diğer günler | +76,7 bps / +8,3 bps (fark +68,5 bps; IS +58, OOS +79) |
| t tam / IS / OOS | 3,08 / 2,13 / 2,26 |
| İsabet | %67 |
| Yıl aynı işaret | 8/10 (2017: −13, 2023: −45 bps) |
| Uç dönemler hariç / roll hariç / winsorize / Spearman t | 3,42 / 3,22 / 3,07 / 2,84 |
| Erken spot 2010–2017/03 | +41 bps, t = 1,30 (2010–2016 alt örneklemi: +50 bps, t = 1,53, 28 olay) |
| Spot 2010–2026 | +64 bps, t = 3,29, 67 olay, 17 yılın 12'sinde pozitif |
| Net Sharpe (5 bps), tam / IS / OOS | 0,94 / 0,98 / 0,99 (OOS demeaned 0,87; OOS 10 bps 0,93; OOS al-tut 0,53) |
| Bacaklar | Yalnız uzun bacak var; kısa bacak tanımsız |
| BH q (178 yön testi) | 0,06 |

**Sağlamlık.**
- Komşu pencerelerin hepsi pozitif. TDE0_h3 için +50 bps (t = 2,23), TDE2_h5 için +65 bps (t = 2,29), TDE2_h3 için +39 bps (t = 1,46). Etki tek bir güne bağlı değil.
- Çeyrek sonu olmayan ay sonlarında etki **yok**: −22 bps, t = −0,93. Yani bu genel bir ay dönümü etkisi değil, çeyreğe özgü.
- Aralık hariç tutulunca t = 2,17. Mart + Eylül ortalaması +81 bps, Haziran + Aralık +72 bps. Haziran ve Aralık VİOP vade aylarıdır, dolayısıyla etki VİOP vadesine bağlı bir artefakt değil.
- placebo_lead değerleri düz (−0,03 … +0,05).

**Mekanizma.** Zayıf ve doğrulanamadı. Akla gelen açıklamalar çeyrek sonu yeniden dengeleme ile yeni çeyrek tahsisleri ve ETF girişleri. Dolar kanalı **reddedildi**: Aynı pencerede EURUSD −23 bps (t = −1,68) değişti, yani dolar güçlendi. Altın doların zayıflamasıyla değil, ona rağmen yükseliyor.

**Neden YUKSEK değil.** Sayısal YUKSEK eşiklerinin hepsini geçiyor. Ancak olay sayısı 39, mekanizma doğrulanamadı ve BH q = 0,06 (FDR %5'te anlamlı değil). Bu kural bir sinyalden çok küçük bir **takvim ek pozisyonu** olarak düşünülmeli.

### 4.2 NFP tepki momentumu: NFP_cond_spot12to15 — ORTA (rejime bağımlı)

**Kural:** NFP yayım günü VİOP açıksa (ve yarım gün değilse), 15:00 UTC'de (18:00 TSİ) x = sign(ln(spot 15:00 / spot 12:00)) hesapla. Uzlaşma penceresinde (18:05–18:15 TSİ) x yönünde pozisyon al. Ertesi VİOP günü (genellikle Pazartesi) uzlaşmasında çık (h = 1); varyantta 3 gün tutulur (h = 3). Yılda yaklaşık 11 işlem.

| Ölçü | h = 1 | h = 3 |
|---|---|---|
| Olay sayısı | 109 | 109 |
| Ortalama sign(x)·fwd (bps), tam / IS / OOS | +18,0 / +5,7 / +31,1 | +35,4 / +14,4 / +57,7 |
| t (sürekli IC), tam / IS / OOS | 3,62 / 0,79 / 7,03 | 2,58 / 0,70 / 3,02 |
| t (işaret kuralı), tam / IS / OOS | 2,42 / 0,55 / 3,46 | 2,51 / 0,99 / 2,64 |
| Yıl aynı işaret | 8/10 | 7/10 |
| Erken spot 2010–2016 (işaret t) | −1,01 (IC −0,12, olay başına −5,8 bps) | −1,19 |
| Net Sharpe, OOS (5 bps / 10 bps / demeaned) | 0,90 / 0,73 / 0,90 | 1,07 / 0,97 / 1,07 |
| Bacaklar, OOS Sharpe | uzun 0,57; kısa 0,74 | uzun 0,79; kısa 0,72 |
| Tam dönem / IS Sharpe | 0,47 / 0,03 | 0,67 / 0,22 |
| BH q | 0,03 | 0,16 |

**Kontroller.**
- Aynı 12→15 sinyali tüm günlerde zayıf (t = 1,26). NFP ve CPI dışı günlerde de t = 1,26, NFP olmayan Cumalarda t = 1,03. Etki genel bir gün içi momentum değil, NFP'ye özgü.
- Yayım öncesi pencere (07→12 UTC) placebo olarak sıfır çıktı (t = −0,15).
- Pencere duyarlılığı: 13→15 için t = 3,68 (IS 1,41), 14→15 için t = 2,43 (IS 1,57), 12→14 için t = 1,86 (IS −0,28). Bunlar sonradan bakılmış varyantlar, seçim için kullanılmadı. Erken spot dönemde 13→15 ve 14→15 de sıfır (t = 0,2–0,3).
- Büyük tepkiler taşıyor: IS medyanının üstündeki tepkilerde olay başına +28 bps, altındakilerde +2,6 bps.
- **Kırılganlık:** En kârlı 5 olay çıkarılınca ortalama +6 bps'ye, t 0,84'e düşüyor. İsabet IS'te %46, OOS'ta %60.
- Ayrıştırma (2022–2026): Devamın küçük kısmı aynı gün 15→20 UTC'de geliyor (+8,5 bps), büyük kısmı 20:00 UTC → ertesi gün 15:00 UTC arasında (+22 bps). Bu, hafta sonu ve Pazartesi Asya-Avrupa seansını kapsıyor.
- CPI'da aynı sinyal ters ve zayıf (t = −1,35). Bu da "makro habere yetersiz tepki" açıklamasını zayıflatıyor.

**Neden ORTA, neden YUKSEK değil.** İşaret kuralında t_tam = 2,42 < 3. IS zayıf, 2010–2016 ters işaretli ve sonuç birkaç büyük olaya bağlı. 2022 sonrası faiz rejimine özgü olabilir. Canlıda küçük pozisyonla izlenmeli; 2010–2016'daki ters işaret bu etkinin kalıcı olmayabileceğini gösteriyor.

### 4.3 Diğer |t| ≥ 2,5 adaylar — DUSUK (büyük olasılıkla şans ya da kırılgan)

| Test | Etki | t tam / IS / OOS | Neden düşük |
|---|---|---|---|
| BAYRAM_post_h5 (bayram sonrası ilk VİOP günü gir, 5 gün) | −101 bps | −3,22 / −2,51 / −2,08 | Erken spotta aynı tarihler **ters**: +71 bps, t = +1,53. Bayram tarihleri takvimde kayıyor ve küresel altın için bir mekanizma yok. 21 olay. |
| OG_OEday_h1 (COMEX OG vade günü getirisi) | −24 bps | −3,03 / −0,95 / −3,11 | Erken spot **ters** (+20 bps, t = +1,6). Alternatif tarih kuralında t = −1,23. Etki 2020 ve 2024–2026'dan geliyor. |
| VEXP_last5_h5 (VİOP vadesinin son 5 günü) | −64 bps | −2,58 / −0,12 / −3,20 | IS'te yok. Roll günü içeren pencereler çıkarılınca t = −0,82. |
| CPI_pre_h1 (CPI gününden önceki uzlaşmada gir) | +21 bps | 2,56 / 4,25 / 0,35 | Yalnız IS'te var; OOS ve erken dönemde yok. |
| YEND_TDE1_h3 (yıl dönümü) | +110 bps | 2,66 / 3,47 / 0,88 | 9 olay; QEND'in alt kümesi. |
| MONTH_Oca_h1 (Ocak etkisi) | +15 bps/gün | 2,03 / 0,72 / 2,00 | 2026 hariç t = 1,07. Erken spot +12 bps, t = 1,56. 12 ay testinden yalnızca biri. |
| MONTH_Haz_h1 (Haziran negatif) | −16 bps/gün | −2,20 / −0,66 / −2,48 | Erken dönemde yok (−0,04). |

## 5. Negatif bulgular (test edildi, kural yok)

- **Haftanın günü** (15 test): Hiçbirinde |t| ≥ 2 yok. Cuma girişi, yani Pazartesi getirisi: −5,5 bps, t = −1,1. Erken dönemde ters (+2,1). Lucey–Tully'nin "negatif Pazartesi" bulgusu VİOP'ta yok.
- **Genel ay dönümü** (21 test): Son 1–2 ve ilk 1–3 gün kurallarının hiçbiri tutmadı. Ayın ilk gününün getirisi (TDE0 girişi, h = 1) +4,8 bps, t = 0,4. Incrementum'un GLD'deki ilk gün etkisi burada yok. TDE3_h1 −20 bps (t = −2,1) ama IS'te −3,5, OOS'ta −0,6; tutarsız.
- **Ay mevsimselliği** (14 test): Baur'un Eylül/Kasım etkisi yok; Eylül −10,8 bps/gün (t = −1,75), Eylül + Kasım t = −1,48. Kış etkisi (Aralık–Şubat) t = 1,58, zayıf.
- **FOMC** (18 test):
  - FOMC günü girip açıklamayı taşımak: +2,9 bps, t = 0,2.
  - FOMC öncesi 1, 2 ve 3 gün tek tek: |t| ≤ 1,2. F−3 → F: −15 bps (t = −0,8). F−5 → F: −43 bps (t = −1,77).
  - FOMC sonrası 1, 3 ve 5 gün: −24, −39 ve −42 bps, |t| ≤ 1,5.
  - Koşullu tepki sürüklenmesi ya da dönüşü (spot ve kapanış varyantları): |t| ≤ 1,8.
  - SEP toplantıları: −12 bps, t = −0,5.
  - FOMC bir yön değil, oynaklık olayı: F+1 günü mutlak getirisi diğer günlerin 1,69 katı (t = 4,2).
- **CPI** (10 test): Koşulsuz sonrası ve koşullu sürüklenme ya da dönüş yok. CPI günü VİOP oynaklığı diğer günlerden **yüksek değil** (oran 0,90).
- **NFP koşulsuz** (4 test): Öncesi ve sonrası yok. NFP günü oynaklığı 1,21 kat.
- **Tatiller** (25 test):
  - NYSE, LSE ve SSE tatil öncesi, tatil günü ve sonrası: yok. LSE tatil öncesi IS'te 4,7, OOS'ta −0,7.
  - TR tatili öncesi ve sonrası (h = 1, 3, 5): yok. Kapsanan gün sayısına normalize edilmiş haliyle t = −1,3.
  - Arife yarım günü, bayram öncesi: yok.
  - Bayram sonrası 5 gün: DUSUK, bkz. §4.3.
- **COMEX** (13 test):
  - OG vadesi öncesi 3 ve 5 gün (pinning ya da baskı): yok.
  - Vade sonrası 1, 3 ve 5 gün: yok.
  - Yalnız ana vadeler: yok.
  - GC FND roll penceresi, FND günü ve FND sonrası: yok.
  - BCOM roll: yok.
  - OG vade günü: DUSUK, bkz. §4.3.
- **VİOP vadesi** (4 test): Vade günü ve vade sonrası: yok. Roll günü −30 bps (t = −2,35); spot getirisi de aynı, yani gerçek fiyat hareketi. Mekanizma yok.
- **Asya festivalleri** (12 test):
  - Çin Yeni Yılı öncesi 5 ve 10 gün, tatil sırası ve sonrası: yok (9 olay).
  - Ekim Altın Haftası öncesi, sırası ve sonrası: yok. Tatil sonrası +86 bps, t = 1,3.
  - Dhanteras öncesi ve Diwali sonrası: yok. Diwali sonrası −174 bps, t = −1,97, 10 olay, erken dönemde ters.
  - Akshaya Tritiya öncesi ve sonrası: yok.
- **Çeyrek sonunun son 5 günü** (TDE5 → TDE0): −40 bps, t = −1,4; yok.
- **Test edilmedi:** TCMB PPK (USD bazlı XAUUSD için mekanizma yok, USDTRY ve gram altın ailesine ait) ve jeopolitik olay takvimi (GPR başka ailede).

## 6. Test sayısı ve çoklu test

- **Kayıt** (`out/registry/a3_takvim_olay.csv`): 182 satır. Bunların 178'i yön, 4'ü oynaklık testi. Aile dağılımı:

  | Aile | Test |
  |---|---|
  | cpi_nfp | 33 |
  | tatil | 25 |
  | ay_donumu | 21 |
  | fomc | 18 |
  | ceyrek_yil | 16 |
  | haftanin_gunu | 15 |
  | ay_mevsim | 15 |
  | comex_vade | 13 |
  | asya | 12 |
  | kontrol | 6 |
  | viop_vade | 4 |
  | oynaklik | 4 |

  İki test aynı tanımın ikinci kaydıdır (QDECOMP_Qlast_day_h1 = QEND_TDE1_h1, QDECOMP_Qnew_day1_h1 = QEND_TDE0_h1). Bu yüzden ayrı test sayısı yaklaşık 180.
- Yön testlerinde |t| ≥ 2 olan 22 test var (şans beklentisi yaklaşık 8). |t| ≥ 3 olan 7 test var (şans beklentisi yaklaşık 0,5).
- BH q < 0,05 yalnız NFP koşullu varyantlarında çıkıyor (q ≈ 0,02–0,03).
- QEND_TDE1_h3, BAYRAM_post_h5 ve OG_OEday_h1 için q ≈ 0,06.
- Bonferroni eşiğini (|t| ≥ 3,63) yalnız NFP 13→15 varyantı geçiyor (3,68). Bu varyant sonradan bakılmış bir pencere.

## 7. Pratik çıkarım (Türkiye'den VİOP ile işlem)

- Takvim ailesi tek başına bir **ana strateji** sunmuyor. İnsanların takvim olaylarından para kazanması çoğunlukla dakikalar içinde (HFT ya da haber işlemi) veya opsiyonla oynaklık satıp alarak oluyor. Kapanıştan kapanışa 1–5 günlük yön kenarı bu verilerde neredeyse yok.
- **Kullanılabilecek iki küçük kenar:**
  1. Çeyrek dönümünde 3 gün uzun kalmak (yılda 4 işlem). Al-tut pozisyonuna ek ağırlık ya da ayrı küçük bir pozisyon olarak.
  2. NFP gününde 15:00–18:00 TSİ spot yönünde Pazartesiye kadar kalmak (yılda yaklaşık 11 işlem). Sinyal yayımdan sonraki 2–3 saatlik spot hareketinden geliyor ve en az 18:00 TSİ'den önce hesaplanabilir.
  - İkisinin olay başına kenarı 18–77 bps, yani 5–10 bps maliyeti rahatça karşılıyor. Ama sermaye kullanımı çok düşük (%2–5).
- **Risk yönetimi için takvim:** FOMC ertesi gün (×1,7 oynaklık) ve NFP günü (×1,2) pozisyon boyutunu küçültmek için kullanılmalı. Bu günlerde yön tahmini yapılamıyor.
- Bayram tatillerinde VİOP kapalıyken küresel altın işlem görmeye devam eder. Bayram sonrası getiri bulgusu (−101 bps) erken dönemde ters işaretli olduğu için işlem kuralı olarak **önerilmez**.

## 8. Dosyalar ve yeniden üretim

- `run_all.sh`: Bütün zinciri çalıştırır (`build_events.py`, `a3_analiz.py`, `a3_derin.py`, `a3_oynaklik.py`, `a3_tablolar.py`). Registry sıfırlanıp yeniden yazılır.
- `results_all.csv` 147 ana testi, `results_derin.csv` derin kontrolleri, `registry_with_q.csv` BH q-değerlerini içerir. `log_*.txt` dosyaları ayrıntılı çıktılardır.
- `events_*.csv` olay takvimleridir. `dl/` indirilen kaynak sayfalarını, `pylib/` `holidays` paketini içerir.

## 9. Tam test tabloları (ana tarama, 147 test)

Sütunlar: "fark" kukla testlerinde olay ortalaması eksi diğer günler (bps), koşullu testlerde ort(sign(x)·fwd). Sharpe değerlerinde yön IS'ten seçildi. Erken spot dönemi 2010–2017/03. q: 178 yön testi içinde BH.

**Haftanın günü** (15 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DOW_entry_Pzt_h1 | 485 | -1.3 | -0.26 | -0.41 | -0.01 | 5/10 | 0.30 | -0.67 | -0.60 | -0.35 | 0.93 |
| DOW_entry_Pzt_h3 | 485 | 2.4 | 0.35 | -0.26 | 0.62 | 5/10 | -1.76 | 0.09 | -0.82 | -0.41 | 0.93 |
| DOW_entry_Pzt_h5 | 484 | 1.9 | 0.27 | 0.27 | 0.14 | 7/10 | -0.02 | 0.00 | 0.55 | 0.05 | 0.93 |
| DOW_entry_Sal_h1 | 485 | 5.9 | 1.23 | 0.22 | 1.34 | 7/10 | -1.36 | 1.13 | 0.46 | 0.23 | 0.55 |
| DOW_entry_Sal_h3 | 485 | 10.6 | 1.60 | 0.90 | 1.33 | 8/10 | -1.54 | 1.81 | 0.63 | 0.23 | 0.51 |
| DOW_entry_Sal_h5 | 484 | 5.2 | 0.81 | 0.42 | 0.70 | 8/10 | 0.15 | 0.82 | 0.66 | 0.17 | 0.77 |
| DOW_entry_Çar_h1 | 485 | -1.8 | -0.35 | 0.08 | -0.49 | 5/10 | -1.29 | -0.00 | -0.29 | -0.53 | 0.93 |
| DOW_entry_Çar_h3 | 484 | -4.6 | -0.68 | 0.07 | -0.89 | 7/10 | 0.76 | -0.36 | -0.04 | -0.42 | 0.85 |
| DOW_entry_Çar_h5 | 484 | -3.0 | -0.47 | -0.36 | -0.31 | 7/10 | -0.20 | -0.37 | -0.46 | 0.03 | 0.93 |
| DOW_entry_Per_h1 | 489 | 2.6 | 0.55 | 1.05 | -0.05 | 7/10 | 0.45 | 0.83 | -0.09 | -0.31 | 0.91 |
| DOW_entry_Per_h3 | 488 | -3.3 | -0.47 | 0.01 | -0.60 | 8/10 | 1.86 | -0.41 | 0.02 | -0.37 | 0.93 |
| DOW_entry_Per_h5 | 488 | -3.0 | -0.43 | -0.18 | -0.40 | 6/10 | 0.12 | -0.35 | -0.41 | 0.09 | 0.93 |
| DOW_entry_Cum_h1 | 482 | -5.5 | -1.08 | -0.91 | -0.71 | 8/10 | 2.15 | -1.25 | -0.22 | -0.01 | 0.62 |
| DOW_entry_Cum_h3 | 482 | -5.1 | -0.76 | -0.74 | -0.40 | 6/10 | 0.68 | -1.10 | -0.46 | -0.07 | 0.78 |
| DOW_entry_Cum_h5 | 482 | -1.0 | -0.16 | -0.15 | -0.08 | 7/10 | -0.04 | -0.10 | -0.51 | -0.01 | 0.94 |

**Ay dönümü** (21 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TOM_entry_TDE3_h1 | 117 | -19.9 | -2.09 | -3.55 | -0.59 | 9/10 | -0.86 | -2.68 | 0.02 | 0.12 | 0.31 |
| TOM_entry_TDE3_h3 | 117 | -17.0 | -1.23 | -2.01 | -0.09 | 7/10 | -0.66 | -1.20 | -0.22 | -0.05 | 0.55 |
| TOM_entry_TDE3_h5 | 116 | -2.0 | -0.11 | -0.59 | 0.35 | 6/10 | 0.53 | 0.38 | -0.44 | -0.22 | 0.95 |
| TOM_entry_TDE2_h1 | 117 | 12.9 | 1.37 | -0.35 | 1.90 | 7/10 | -1.10 | 1.17 | -1.09 | -0.99 | 0.55 |
| TOM_entry_TDE2_h3 | 116 | 7.5 | 0.42 | -0.21 | 0.63 | 6/10 | 0.36 | 1.36 | -0.50 | -0.34 | 0.93 |
| TOM_entry_TDE2_h5 | 116 | 23.4 | 1.30 | 0.23 | 1.49 | 6/10 | 0.63 | 1.97 | 0.63 | 0.42 | 0.55 |
| TOM_entry_TDE1_h1 | 117 | -9.8 | -0.88 | 0.18 | -1.08 | 5/10 | 0.52 | -0.22 | -0.51 | -0.59 | 0.72 |
| TOM_entry_TDE1_h3 | 116 | 8.8 | 0.49 | 1.04 | -0.08 | 7/10 | 1.48 | 1.75 | 0.02 | -0.14 | 0.93 |
| TOM_entry_TDE1_h5 | 116 | 8.3 | 0.39 | 0.86 | -0.07 | 7/10 | 1.44 | 1.44 | 0.11 | -0.11 | 0.93 |
| TOM_entry_TDE0_h1 | 116 | 4.8 | 0.40 | -0.15 | 0.56 | 7/10 | 0.88 | 1.39 | -0.44 | -0.36 | 0.93 |
| TOM_entry_TDE0_h3 | 116 | 20.5 | 1.28 | 0.34 | 1.40 | 6/10 | 1.01 | 1.69 | 0.58 | 0.42 | 0.55 |
| TOM_entry_TDE0_h5 | 116 | 10.3 | 0.52 | 0.11 | 0.61 | 7/10 | 0.78 | 0.87 | 0.40 | 0.16 | 0.93 |
| TOM_entry_TDM1_h1 | 117 | 11.6 | 1.15 | 1.41 | 0.34 | 6/10 | 0.92 | 0.63 | 0.12 | 0.01 | 0.60 |
| TOM_entry_TDM1_h3 | 117 | 9.9 | 0.59 | 0.85 | 0.09 | 4/10 | 1.14 | 0.28 | 0.15 | -0.04 | 0.90 |
| TOM_entry_TDM1_h5 | 116 | -6.7 | -0.32 | -1.17 | 0.50 | 5/10 | 1.36 | -0.82 | -0.61 | -0.35 | 0.93 |
| TOM_entry_TDM2_h1 | 117 | 2.5 | 0.25 | -1.31 | 1.11 | 5/10 | -0.00 | -0.01 | -0.73 | -0.63 | 0.93 |
| TOM_entry_TDM2_h3 | 117 | -8.4 | -0.57 | -0.80 | -0.07 | 6/10 | -0.08 | -0.71 | -0.28 | -0.07 | 0.91 |
| TOM_entry_TDM2_h5 | 116 | -6.7 | -0.35 | -1.52 | 0.76 | 7/10 | 1.48 | -0.60 | -0.70 | -0.44 | 0.93 |
| TOM_entry_TDM3_h1 | 117 | -4.0 | -0.45 | 1.26 | -1.54 | 6/10 | 1.05 | -0.05 | -0.72 | -0.84 | 0.93 |
| TOM_entry_TDM3_h3 | 116 | -19.2 | -1.22 | -1.57 | -0.19 | 8/10 | 1.13 | -1.26 | -0.25 | -0.03 | 0.55 |
| TOM_entry_TDM3_h5 | 116 | -1.4 | -0.07 | -0.35 | 0.18 | 6/10 | 1.42 | -0.15 | -0.45 | -0.17 | 0.97 |

**Ay mevsimselliği** (14 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MONTH_Oca_h1 | 194 | 15.0 | 2.03 | 0.72 | 2.00 | 8/10 | 1.56 | 1.40 | 0.84 | 0.72 | 0.34 |
| MONTH_Şub_h1 | 181 | -7.4 | -1.00 | -1.36 | -0.24 | 7/9 | 1.89 | -1.10 | -0.06 | 0.07 | 0.66 |
| MONTH_Mar_h1 | 215 | -0.3 | -0.03 | -0.37 | 0.28 | 4/10 | -1.06 | -0.06 | -0.28 | -0.15 | 0.99 |
| MONTH_Nis_h1 | 202 | 4.7 | 0.65 | 0.83 | 0.26 | 7/10 | 0.50 | 0.88 | 0.24 | 0.10 | 0.86 |
| MONTH_May_h1 | 197 | -3.3 | -0.49 | 0.87 | -1.21 | 9/10 | -1.63 | -0.39 | -0.36 | -0.51 | 0.93 |
| MONTH_Haz_h1 | 200 | -15.7 | -2.20 | -0.66 | -2.48 | 8/10 | -0.04 | -2.11 | 0.74 | 0.88 | 0.26 |
| MONTH_Tem_h1 | 208 | 3.6 | 0.58 | 1.32 | -0.34 | 6/10 | 0.35 | 0.71 | 0.03 | -0.13 | 0.90 |
| MONTH_Ağu_h1 | 206 | 6.5 | 0.87 | 0.61 | 0.62 | 5/10 | 2.47 | 0.98 | 0.51 | 0.31 | 0.72 |
| MONTH_Eyl_h1 | 212 | -10.8 | -1.75 | -2.32 | -0.52 | 8/10 | -1.11 | -1.65 | 0.03 | 0.22 | 0.42 |
| MONTH_Eki_h1 | 215 | 1.1 | 0.17 | 0.18 | 0.10 | 5/10 | -0.02 | 0.28 | 0.18 | 0.04 | 0.94 |
| MONTH_Kas_h1 | 198 | -2.6 | -0.35 | -1.33 | 0.66 | 3/10 | -1.34 | -0.26 | -0.47 | -0.32 | 0.93 |
| MONTH_Ara_h1 | 198 | 9.0 | 1.69 | 2.40 | 0.17 | 7/9 | -1.62 | 1.86 | 0.22 | 0.05 | 0.45 |
| MONTH_SepNov_h1 | 410 | -7.5 | -1.48 | -2.57 | 0.13 | 8/10 | -1.81 | -1.34 | -0.32 | -0.08 | 0.55 |
| MONTH_Winter_h1 | 573 | 7.0 | 1.58 | 0.86 | 1.33 | 6/10 | 1.23 | 1.14 | 0.68 | 0.45 | 0.52 |

**Çeyrek / yıl sonu** (7 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| QEND_TDE1_h1 | 39 | 19.4 | 1.99 | 2.08 | 0.72 | 6/10 | 0.69 | 2.42 | 0.28 | 0.16 | 0.34 |
| YEND_TDE1_h1 | 9 | 13.3 | 0.65 | 4.29 | -1.48 | 6/9 | 1.12 | 0.69 | -0.57 | -0.60 | 0.86 |
| QEND_TDE1_h3 | 39 | 68.5 | 3.08 | 2.13 | 2.26 | 8/10 | 1.30 | 3.42 | 0.99 | 0.87 | 0.06 |
| YEND_TDE1_h3 | 9 | 109.7 | 2.66 | 3.47 | 0.88 | 8/9 | 1.95 | 2.70 | 0.35 | 0.29 | 0.15 |
| QEND_TDE1_h5 | 39 | 62.7 | 2.22 | 2.53 | 0.98 | 7/10 | 1.11 | 2.21 | 0.55 | 0.38 | 0.26 |
| YEND_TDE1_h5 | 9 | 90.2 | 1.86 | 1.70 | 0.90 | 7/9 | 1.59 | 1.91 | 0.31 | 0.23 | 0.39 |
| QEND_last5_h5 | 39 | -40.4 | -1.42 | -0.67 | -1.26 | 6/10 | -0.37 | -1.29 | 0.29 | 0.44 | 0.55 |

**FOMC** (18 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FOMC_entryF_h1 | 77 | 2.9 | 0.17 | 0.27 | -0.01 | 4/10 | -0.22 | -0.21 | -0.02 | -0.09 | 0.94 |
| FOMC_entryF_h3 | 77 | -31.9 | -1.13 | 0.74 | -1.85 | 7/10 | -0.84 | -0.65 | -0.72 | -0.83 | 0.60 |
| FOMC_entryF_h5 | 77 | -33.3 | -1.06 | 0.06 | -1.35 | 7/10 | -0.91 | -0.77 | -0.43 | -0.58 | 0.62 |
| FOMC_pre_F-1_h1 | 77 | -0.1 | -0.01 | -0.26 | 0.13 | 4/10 | 0.23 | -0.59 | -0.28 | -0.19 | 0.99 |
| FOMC_pre_F-2_h1 | 77 | -11.9 | -1.20 | -0.46 | -1.12 | 7/10 | -0.45 | -1.03 | 0.27 | 0.36 | 0.56 |
| FOMC_pre_F-3_h1 | 77 | -3.1 | -0.30 | 1.45 | -1.18 | 5/10 | 0.04 | -0.69 | -0.55 | -0.64 | 0.93 |
| FOMC_pre_F-3_h3 | 77 | -15.3 | -0.77 | 0.43 | -1.08 | 6/10 | -0.11 | -1.25 | -0.45 | -0.62 | 0.78 |
| FOMC_pre_F-5_h5 | 77 | -43.0 | -1.77 | -0.58 | -1.70 | 7/10 | -0.26 | -2.32 | 0.54 | 0.75 | 0.42 |
| FOMC_post_F+1_h1 | 78 | -23.6 | -1.36 | -0.11 | -1.49 | 6/10 | -1.61 | -0.87 | 0.52 | 0.57 | 0.55 |
| FOMC_post_F+1_h3 | 78 | -38.6 | -1.50 | -0.28 | -1.62 | 8/10 | -0.85 | -1.01 | 0.52 | 0.63 | 0.55 |
| FOMC_post_F+1_h5 | 78 | -42.1 | -1.39 | -0.38 | -1.39 | 7/10 | -1.67 | -0.87 | 0.41 | 0.58 | 0.55 |
| FOMC_SEP_entryF_h1 | 38 | -12.0 | -0.46 | 0.01 | -0.72 | 5/10 | -0.59 | -0.44 | -0.33 | -0.38 | 0.93 |
| FOMC_cond_spot_h1 | 78 | -21.5 | -0.91 | -1.39 | -0.65 | 8/10 | 0.99 | 0.46 | 0.15 | 0.15 | 0.70 |
| FOMC_cond_close_h1 | 78 | -22.7 | -1.77 | -1.41 | -1.87 | 8/10 | 0.99 | 0.17 | 0.15 | 0.15 | 0.42 |
| FOMC_cond_spot_h3 | 78 | -25.5 | -1.30 | -0.29 | -1.43 | 7/10 | 0.33 | 0.30 | 0.07 | 0.06 | 0.55 |
| FOMC_cond_close_h3 | 78 | -29.4 | -1.38 | -0.01 | -1.79 | 7/10 | 0.33 | 0.16 | 0.07 | 0.06 | 0.55 |
| FOMC_cond_spot_h5 | 78 | 3.4 | -0.31 | -0.55 | -0.16 | 6/10 | 1.54 | 1.09 | -0.49 | -0.50 | 0.93 |
| FOMC_cond_close_h5 | 78 | -0.6 | -0.77 | -0.38 | -0.77 | 4/10 | 1.54 | 1.00 | -0.49 | -0.50 | 0.78 |

**CPI / NFP** (20 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CPI_pre_h1 | 115 | 21.2 | 2.56 | 4.25 | 0.35 | 6/10 | -0.33 | 2.81 | 0.11 | -0.01 | 0.16 |
| CPI_post_h1 | 116 | -9.0 | -0.90 | -0.43 | -0.81 | 5/10 | -0.62 | -0.35 | 0.10 | 0.21 | 0.70 |
| CPI_cond_spot12to15_h1 | 109 | -13.5 | -1.35 | 0.09 | -1.68 | 8/10 | -0.10 | -2.01 | 0.61 | 0.63 | 0.55 |
| CPI_cond_close_h1 | 112 | -0.7 | 0.24 | -0.67 | 0.48 | 3/10 | 0.37 | -0.04 | -0.18 | -0.21 | 0.93 |
| CPI_post_h3 | 116 | -10.4 | -0.63 | -1.14 | 0.25 | 6/10 | -0.36 | 0.00 | -0.39 | -0.19 | 0.88 |
| CPI_cond_spot12to15_h3 | 109 | 1.7 | -0.27 | 0.55 | -1.08 | 5/10 | 0.77 | -1.40 | -0.23 | -0.26 | 0.93 |
| CPI_cond_close_h3 | 112 | -1.4 | -0.37 | 0.66 | -0.63 | 3/10 | 0.96 | -0.62 | -0.30 | -0.35 | 0.93 |
| CPI_post_h5 | 116 | -2.7 | -0.14 | -1.07 | 0.89 | 5/10 | -1.13 | 0.31 | -0.68 | -0.42 | 0.94 |
| CPI_cond_spot12to15_h5 | 109 | 1.0 | 0.14 | 0.43 | -0.18 | 6/10 | 1.70 | -0.96 | -0.07 | -0.10 | 0.94 |
| CPI_cond_close_h5 | 112 | 18.8 | 0.43 | 0.71 | 0.32 | 7/10 | 0.92 | 0.27 | 0.30 | 0.24 | 0.93 |
| NFP_pre_h1 | 116 | -4.8 | -0.48 | 0.10 | -0.72 | 6/10 | 0.62 | -0.73 | -0.35 | -0.46 | 0.93 |
| NFP_post_h1 | 116 | -8.0 | -0.92 | -1.00 | -0.32 | 6/10 | 2.83 | -1.03 | -0.18 | -0.04 | 0.70 |
| NFP_cond_spot12to15_h1 | 109 | 18.0 | 3.62 | 0.79 | 7.03 | 8/10 | -1.18 | 3.36 | 0.90 | 0.90 | 0.03 |
| NFP_cond_close_h1 | 113 | 9.2 | 2.43 | 0.16 | 4.62 | 6/10 | -1.57 | 2.49 | -0.92 | -0.91 | 0.19 |
| NFP_post_h3 | 116 | 3.0 | 0.21 | 0.31 | 0.00 | 7/10 | 2.79 | 0.43 | 0.13 | -0.10 | 0.94 |
| NFP_cond_spot12to15_h3 | 109 | 35.4 | 2.58 | 0.70 | 3.02 | 7/10 | -0.60 | 2.48 | 1.07 | 1.07 | 0.16 |
| NFP_cond_close_h3 | 113 | 19.0 | 1.91 | 0.76 | 1.83 | 6/10 | -1.17 | 2.09 | 0.54 | 0.53 | 0.38 |
| NFP_post_h5 | 116 | 19.7 | 1.13 | 0.23 | 1.31 | 6/10 | 2.12 | 1.68 | 0.71 | 0.43 | 0.60 |
| NFP_cond_spot12to15_h5 | 109 | 35.2 | 1.06 | -0.07 | 1.21 | 6/10 | -1.55 | 0.94 | 0.70 | 0.71 | 0.62 |
| NFP_cond_close_h5 | 113 | 22.8 | 1.13 | 0.03 | 1.33 | 7/10 | -2.51 | 1.63 | -0.85 | -0.84 | 0.60 |

**Tatiller ve bayramlar** (24 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HOL_NYSE_pre_h1 | 87 | 13.5 | 1.56 | 2.45 | 0.15 | 9/10 | 0.19 | 1.81 | 0.02 | -0.11 | 0.52 |
| HOL_NYSE_over_h1 | 87 | 8.6 | 1.24 | 0.90 | 0.87 | 7/10 | 2.37 | 1.25 | 0.34 | 0.18 | 0.55 |
| HOL_NYSE_post_h1 | 90 | 9.7 | 1.01 | 1.06 | 0.43 | 6/10 | 0.25 | 1.27 | 0.15 | 0.03 | 0.65 |
| HOL_LSE_pre_h1 | 58 | 20.5 | 1.77 | 4.70 | -0.70 | 6/10 | 3.24 | 1.84 | -0.34 | -0.43 | 0.42 |
| HOL_LSE_over_h1 | 58 | 16.1 | 1.44 | 0.96 | 1.09 | 9/10 | 1.94 | 1.51 | 0.45 | 0.36 | 0.55 |
| HOL_LSE_post_h1 | 56 | -8.1 | -0.65 | 0.17 | -0.88 | 5/10 | -0.61 | -0.60 | -0.41 | -0.49 | 0.86 |
| HOL_SSE_pre_h1 | 62 | -1.6 | -0.14 | 2.35 | -1.48 | 4/10 | -0.69 | 0.08 | -0.68 | -0.76 | 0.94 |
| HOL_SSE_over_h1 | 62 | -2.1 | -0.16 | -0.00 | -0.20 | 6/10 | 1.18 | -0.04 | -0.12 | -0.03 | 0.94 |
| HOL_SSE_post_h1 | 64 | 2.6 | 0.19 | 0.60 | -0.14 | 6/10 | 0.89 | 0.18 | -0.09 | -0.16 | 0.94 |
| HOL_SSE_post_h5 | 64 | 20.3 | 0.80 | 0.40 | 0.69 | 6/10 | 0.98 | 0.64 | 0.43 | 0.24 | 0.78 |
| HOL_TR_pre_h1 | 70 | -13.4 | -0.78 | 0.11 | -1.00 | 4/10 |  | -0.74 | -0.46 | -0.52 | 0.78 |
| HOL_TR_pre_h3 | 70 | -3.3 | -0.15 | 0.46 | -0.63 | 3/10 |  | -0.09 | -0.16 | -0.28 | 0.94 |
| HOL_TR_pre_h5 | 70 | -17.3 | -0.75 | 0.51 | -1.46 | 7/10 |  | -0.66 | -0.34 | -0.51 | 0.79 |
| HOL_TR_pre_h1_perday | 70 | -10.3 | -1.27 | -0.70 | -1.07 | 5/10 |  | -1.19 |  |  | 0.55 |
| HOL_TR_post_h1 | 70 | 2.9 | 0.27 | 1.26 | -0.81 | 5/10 |  | 0.03 | -0.39 | -0.49 | 0.93 |
| HOL_TR_post_h3 | 70 | 0.3 | 0.02 | 0.59 | -0.39 | 4/10 |  | -0.07 | -0.08 | -0.23 | 0.99 |
| HOL_TR_post_h5 | 70 | -40.7 | -1.83 | -0.92 | -1.63 | 7/10 |  | -2.00 | 0.34 | 0.54 | 0.40 |
| BAYRAM_arifeday_h1 | 14 | -16.1 | -0.57 | 0.53 | -0.94 | 6/10 |  | -0.55 | -0.41 | -0.44 | 0.91 |
| BAYRAM_pre_h1 | 20 | -13.5 | -0.32 | 1.15 | -1.43 | 6/10 |  | -0.31 | -0.60 | -0.62 | 0.93 |
| BAYRAM_post_h1 | 21 | -9.3 | -0.39 | 0.09 | -0.67 | 7/10 |  | -0.36 | -0.31 | -0.36 | 0.93 |
| BAYRAM_pre_h3 | 20 | -13.7 | -0.31 | 1.17 | -2.68 | 5/10 |  | -0.28 | -0.51 | -0.57 | 0.93 |
| BAYRAM_post_h3 | 21 | -45.9 | -1.22 | -0.31 | -1.35 | 7/10 |  | -1.18 | 0.42 | 0.49 | 0.55 |
| BAYRAM_pre_h5 | 20 | -62.2 | -1.24 | 0.89 | -3.27 | 7/10 |  | -1.19 | -0.76 | -0.84 | 0.55 |
| BAYRAM_post_h5 | 21 | -101.0 | -3.22 | -2.51 | -2.08 | 8/10 |  | -3.16 | 0.43 | 0.52 | 0.06 |

**COMEX opsiyon vadesi / FND / BCOM** (12 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OG_pre5_h5 | 116 | 0.5 | 0.02 | 1.78 | -1.64 | 5/10 | -1.01 | -0.94 | -0.48 | -0.74 | 0.99 |
| OG_pre3_h3 | 116 | -4.0 | -0.26 | 1.36 | -1.74 | 6/10 | -0.55 | -1.04 | -0.54 | -0.75 | 0.93 |
| OG_OEday_h1 | 116 | -23.8 | -3.03 | -0.95 | -3.11 | 6/10 | 1.60 | -2.84 | 1.03 | 1.15 | 0.06 |
| OG_post_h1 | 117 | -10.2 | -1.23 | -2.77 | 0.16 | 8/10 | -0.14 | -1.83 | -0.36 | -0.24 | 0.55 |
| OG_post_h3 | 117 | -22.6 | -1.61 | -1.87 | -0.54 | 10/10 | -0.19 | -1.59 | -0.08 | 0.09 | 0.51 |
| OG_post_h5 | 117 | -12.6 | -0.68 | -1.02 | -0.04 | 6/10 | 0.82 | -0.22 | -0.27 | -0.05 | 0.85 |
| OGmaj_pre5_h5 | 58 | -10.7 | -0.31 | 0.74 | -1.30 | 6/10 | -1.32 | -1.37 | -0.42 | -0.60 | 0.93 |
| OGmaj_post_h5 | 59 | 25.8 | 0.94 | -0.08 | 1.28 | 6/10 | 0.35 | 1.41 | -0.57 | -0.44 | 0.70 |
| GCFND_roll_h5 | 58 | 11.0 | 0.33 | -0.47 | 0.69 | 3/10 | -1.71 | -1.00 | -0.58 | -0.41 | 0.93 |
| GCFND_day_h1 | 58 | 3.4 | 0.19 | 1.51 | -0.39 | 7/10 | 0.75 | 2.03 | -0.19 | -0.25 | 0.94 |
| GCFND_post_h5 | 59 | -6.7 | -0.24 | -0.30 | -0.04 | 5/10 | 1.62 | -0.07 | -0.19 | -0.03 | 0.93 |
| BCOM_roll_h5 | 48 | -16.3 | -0.48 | -0.92 | 0.09 | 5/10 | -0.07 | -0.20 | -0.25 | -0.09 | 0.93 |

**VİOP vadesi / roll** (4 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VEXP_last5_h5 | 58 | -64.0 | -2.58 | -0.12 | -3.20 | 8/10 |  | -2.75 | 0.98 | 1.15 | 0.16 |
| VEXP_day_h1 | 58 | -12.6 | -0.93 | -0.42 | -0.84 | 6/10 |  | -1.02 | 0.20 | 0.27 | 0.70 |
| VEXP_post_h5 | 58 | 10.7 | 0.38 | -0.33 | 0.80 | 6/10 |  | 0.66 | -0.57 | -0.38 | 0.93 |
| VROLL_day_h1 | 60 | -30.4 | -2.35 | -2.37 | -1.03 | 8/10 |  | -2.57 | 0.26 | 0.34 | 0.22 |

**Asya festivalleri** (12 test)

| test | n olay | fark/koşullu ort. (bps) | t tam | t IS | t OOS | yıl aynı işaret | erken spot t | t (uç hariç) | OOS Sharpe net | OOS Sharpe demeaned | q (BH) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CNY_pre5_h5 | 9 | 13.1 | 0.31 | 3.13 | -0.66 | 7/9 | 0.20 | 0.26 | -0.17 | -0.27 | 0.93 |
| CNY_pre10_h5 | 9 | -18.3 | -0.34 | -1.01 | 0.02 | 4/9 | -0.49 | 0.83 | -0.06 | -0.02 | 0.93 |
| CNY_during_h5 | 9 | -9.6 | -0.16 | -1.16 | 0.92 | 5/9 | 1.42 | -0.37 | -0.38 | -0.30 | 0.94 |
| CNY_post_h5 | 9 | -4.0 | -0.08 | -1.53 | 0.40 | 4/9 | 0.88 | -0.28 | -0.27 | -0.18 | 0.97 |
| GOLDEN_WEEK_pre5_h5 | 10 | -71.0 | -1.24 | -0.97 | -0.82 | 6/10 | -1.98 | -1.21 | 0.22 | 0.30 | 0.55 |
| GOLDEN_WEEK_pre10_h5 | 10 | -65.5 | -1.02 | -1.40 | 0.06 | 5/10 | -0.21 | -0.99 | -0.17 | -0.06 | 0.65 |
| GOLDEN_WEEK_during_h5 | 10 | 5.4 | 0.10 | 0.06 | 0.08 | 5/10 | 0.07 | 0.14 | 0.11 | 0.02 | 0.96 |
| GOLDEN_WEEK_post_h5 | 10 | 85.6 | 1.26 | 2.06 | 0.58 | 6/10 | 0.76 | 1.29 | 0.36 | 0.28 | 0.55 |
| DHANTERAS_pre5_h5 | 10 | 25.7 | 0.38 | -0.52 | 0.71 | 5/10 | -0.53 | 0.41 | -0.39 | -0.32 | 0.93 |
| DHANTERAS_post5_h5 | 10 | -174.1 | -1.97 | -1.58 | -1.60 | 7/9 | 1.40 | -1.95 | 0.63 | 0.67 | 0.35 |
| AKSHAYA_pre5_h5 | 10 | -53.1 | -0.96 | -0.22 | -1.06 | 6/10 | -1.30 | -0.92 | 0.26 | 0.33 | 0.69 |
| AKSHAYA_post5_h5 | 11 | -99.0 | -1.44 | -1.61 | -0.63 | 5/10 | -0.38 | -1.41 | 0.23 | 0.31 | 0.55 |