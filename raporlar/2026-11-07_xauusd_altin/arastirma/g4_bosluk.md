# g4_bosluk — 1-3-5 günlük VİOP F_XAUUSD işleminde risk, pozisyon boyutu, teminat ve boşluk riski

Tarih: 08.11.2026. Sözleşme: VİOP F_XAUUSD (Dolar/Ons Altın vadeli, 1 ons). Son veri 06.11.2026: F_XAUUSD1226 uzlaşma 4.078,8 USD, F_USDTRY uzlaşma 51,008.

Kod ve çıktılar: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/g4_risk/`. `run_all.sh` hepsini baştan üretir (≈1 dakika). Kayıt defteri: `out/registry/g4_risk.csv`, 75 test. Bu dosyanın aynısı `research/g4_bosluk.md`.

Not: Bu turda web arama kotası baştan dolmuştu (WebSearch "limit doldu" döndü). Birincil kaynakları bilinen adreslerden doğrudan indirdim: Takasbank genel mektup PDF'leri, Takasbank duyuru listesi, QNB/GCM/Gedik duyuru sayfaları, LBMA sayfası, yerelde duran BIST VİOP Prosedürü rev. 70 metni. Arama gerektiren noktalar "bulunamadı" olarak kaldı.

---

## 0. Kısa sonuç

1. **Oynaklık tahmini (OOS 2022-01 → 2026-11).** Modeller EWMA'yı yalnız biraz geçiyor.
   - En iyisi KOMB = (GJR-GARCH + kalibre GVZ)/2. QLIKE kaybı EWMA'ya göre h=1/3/5'te %3,2 / %9,2 / %13,5 daha düşük. Diebold–Mariano t = −4,1 / −4,5 / −4,6.
   - Mincer–Zarnowitz testi KOMB'u reddetmiyor (p = 0,86 / 0,82 / 0,58). EWMA h=5'te reddediliyor (b = 0,66, p = 0,009).
   - HAR-RV (saatlik spot, gün/akşam/gece bileşenli) EWMA'yı **geçemedi**. OOS'ta sistematik düşük tahmin veriyor (ortalama %16,4–17,1, gerçekleşen %18,2). MZ testi reddediyor (b ≈ 0,5–0,8).
   - RV20 en kötüsü.
2. **2026 rejimi.** VİOP gerçekleşen oynaklığı yıllık %29,3. Ocak 2026'da %43 gerçekleşti, bütün modeller %22–28 bekliyordu. Hepsi kaçırdı.
   - 2026'da ham GVZ en iyi QLIKE'ı verdi. 2022–2025'te GVZ gerçekleşeni ≈%20 aşıyordu (oynaklık primi). 2026'da bu fark kapandı (GVZ ort. %29,0, gerçekleşen %29,3).
3. **Gece ve akşam bileşeni.** Ertesi günün varyansını en çok **akşam (16–20 UTC) varyansı** taşıyor. Tam örneklem HAC katsayısı 1,18 (t 7,0). Gündüz bileşeni 0,28 (t 2,3). Gece/hafta sonu bileşeni ≈0 (0,06; t 0,5).
   - 2026'da toplam varyansta gece payı %42,5'e çıktı. 2017–2025'te %20–29 idi.
4. **Oynaklık yön öngörmüyor.**
   - Oynaklık seviyesinin fwd1/3/5 getirisiyle IC'si −0,02 ile +0,01 arasında, |t| ≤ 0,63.
   - 5 günlük oynaklık değişimi h=1'de IC +0,04 (t 1,9–2,0). Ancak IS t 0,3–0,7 ve aile içi FDR q ≥ 0,40.
   - Oynaklık seviyesi |getiri|'yi güçlü öngörüyor: IC 0,19–0,28, t 6–13.
5. **Oynaklık hedeflemesi (σ* = yıllık %15, en fazla 2 kat, 2018–2026).** Harvey ve ark. (2018) ile uyumlu: Sharpe'a etkisi istatistiksel olarak yok, kuyruğu kesiyor.
   - **Al-tut:** Sharpe 0,57 → 0,74 (drift çıkarılmış −0,01 → 0,05). Bootstrap farkı +0,06, t 0,54.
     - %10 oynaklığa ölçekli maksimum düşüş −%25,0 → −%17,0. En kötü gün −%4,80 → −%3,53. Oynaklığın oynaklığı 0,40 → 0,12. Basıklık 5,6 → 1,6.
     - 30.01.2026 (−%7,80) 1x nominal kaybı −%7,80 → −%3,48. Hedefleme o gün pozisyonu 0,45'e indirmişti.
   - **LOWMOM:** hedefleme zarar veriyor. Drift çıkarılmış Sharpe farkı h1'de −0,06 (t −1,2), h5'te −0,13 (t −2,1). Sinyal zaten düşük oynaklıkta açılıyor.
   - **GDXJ artığı:** +0,11 (t 1,1). Basıklık 56 → 12.
   - **NFP:** −0,08 / −0,11, anlamlı değil.
   - 10 bps maliyet sıralamayı değiştirmiyor. Al-tut'ta hedefleme yılda ≈8,7 gidiş-dönüş devir ekliyor.
6. **Takasbank teminatı (birincil kaynak).** XAUUSD PSR 15.06.2026'dan beri **%10,0** ve değişmedi. Kaynak: GM 2150, 2163 (17.08), 2169 (15.09), 2171 (01.10), 2174 (15.10), 2176 (02.11.2026).
   - Vadeler arası yayılma riski 305 → 325 → 325 → 310 → 310 → **295 USD**.
   - Başlangıç teminatı ≈ 0,10 × 4.078,8 = **407,9 USD/sözleşme** (≈20.800 TL).
7. **Aracı kurumlar.**
   - QNB Invest kendi PSR'ı **%20,0** (08.10.2026 duyurusu) → 815,8 USD/sözleşme. Gün sonu teminat başlangıç teminatının %100'ünün altına inerse çağrı yapılıyor. Anlık oran %50'nin altına inerse bildirim/işlem yapılıyor. Teminatın ≥%50'si TL olmalı.
   - GCM 02.11.2026 tablosu: XAUUSD %10.
   - Gedik: XAUUSD ek teminatı 01.07.2026'dan itibaren %11 → %0.
8. **Etkin kaldıraç ve çağrı olasılığı.** Yalnız başlangıç teminatı yatırılırsa (Takasbank tabanında 10x, QNB'de 5x) gün sonu çağrı olasılığı ≈%50/gün, 5 günde %70–79. Nedeni basit: her zarar çağrı üretiyor.
   - 2 kat teminat (Takasbank tabanında 5x) ile 5 günde çağrı olasılığı 2017–2026'da %0,2–0,3, 2026'da %1,6–2,2.
   - Ocak 2026 oynaklığıyla (%43) simülasyonda bu oran %3,6 (uzun) ve %9,0 (kısa).
   - 3 kat teminat (3,3x) ile tarihte %0. Ocak-2026 simülasyonunda ≤%0,4.
9. **±%10 fiyat limiti uzlaşmada hiç dolmadı.** Uzlaşmadan uzlaşmaya en büyük hareket −%7,80 (30.01.2026).
   - Gün içinde limit üç günde aşıldı ya da limite dayandı:
     - **02.02.2026:** normal seans en düşüğü baz fiyatın −%13,73 altında (F_XAUUSD0426 −%16,25).
     - **23.03.2026:** −%12,86.
     - **24.08.2023:** tam −%10,00 (tek seferlik limit fiyatlı işlem, uzlaşma +%0,20).
   - 02.02.2026'da gram altın en düşükleri tam −%20,00'de, gümüş −%30,00'da duruyor. Bu, limitlerin geçici olarak genişletildiğini gösteriyor. Prosedür md. 49'a göre limitler Genel Müdür Yardımcısı/Piyasa Müdürü kararıyla "iki katına kadar" yükseltilebilir. O güne ait BIST duyurusu **bulunamadı**.
   - Sonuç: limit, zararı durduran bir taban değil.
10. **Boşluk riski (TR tatili, dünya açık).** İşlenemeyen boşluğun std'si:
    - 2017–2026: %1,55 (70 kapanış).
    - 2020-09 → 2025: %0,99 (35 kapanış).
    - 2026: **%3,32** (8 kapanış, ortalama −%1,93).
    - En kötüsü 19.03 (yarım gün, 09:40 UTC) → 23.03.2026 06:30 UTC: **−%9,90** (92,8 saat). Açılış günü VİOP en düşüğü −%12,86, uzlaşma getirisi −%5,24.
    - Tatil açılış günleri günlerin %2,9'u ama uzlaşma varyansının %6,0'ı (OOS %6,3; 2026 %6,9). Ortalama r² diğer günlerin 2,1 katı. 5 günlük pencerelerin %13,7'si bir tatil açılışı içeriyor ve 5 günlük varyansın %15,1'ini taşıyor (2026'da %23,4).
11. **Cuma→Pazartesi (20:00→07:00 UTC).**
    - 2017–2026 std %0,728. Hafta içi gecede %0,504. r6'daki %0,726 yeniden üretildi; hafta içi değer 0,474 değil, 0,504 çıktı.
    - 2026: %1,85'e karşı %1,15. Pazartesi açılışında |boşluk| > %2 olasılığı %12,2.
    - En kötüsü 30.01 → 02.02.2026: −%9,08.
    - GARCH/EWMA ve KOMB tahminleri Pazartesi pencerelerinde riski %17–19 düşük gösteriyor (gerçekleşen/tahmin = 1,17–1,19).
12. **Aralık 2026 vadesi.** F_XAUUSD1226'nın son işlem günü 31.12.2026 (Perşembe, tam gün, akşam seansı yok). Prosedür Ek-1 R: PM ihalesi yapılmazsa vade sonu fiyatı LBMA **sabah (AM, 10:30 Londra = 13:30 TSİ)** fiyatı olur.
    - 31.12.2025'te F_XAUUSD1225 vade sonu fiyatı 4.308,0 idi. 10:30 UTC spot 4.309,5 (−%0,03); 15:00 UTC spot 4.343,4 (−%0,81; saatlik veriyle −%0,86).
    - 10:30 → 15:00 hareketinin std'si 2026'da %0,86. Günlerin %14,4'ünde |hareket| > %1.
    - **Öneri:** 1226'yı 31.12'ye taşımayın. Mevcut pozisyonları 24–30.12.2026 arasında normal seansta vadeler arası strateji emriyle F_XAUUSD0227'ye devredin. 24.12'den itibaren açılan 5 günlük işlemleri doğrudan 0227'de açın.
13. **Boyutlandırma formülü:** N = ⌊ b·√h·E_USD / (κ·σ̂_{t,h}·F_t) ⌋, b = %1/gün. Ayrıntı ve kısıtlar bölüm 5'te.
    - 06.11.2026'da 1 milyon TL (19.605 USD) özsermaye için σ̂ (KOMB) = %1,46 / %2,48 / %3,16 → **3 sözleşme**: nominal 12.236 USD, kaldıraç 0,62x. QNB teminatı özsermayenin %12,5'i. %99 1 günlük kayıp ≈ 497 USD (%2,5).
    - Pencere bir TR tatili içeriyorsa (κ = √2) 2 sözleşme.
    - Bu kuralla 1 sözleşme için asgari özsermaye ≈ 5.946 USD ≈ 303 bin TL.

---

## 1. Oynaklık tahmini

### 1.1 Kurulum

- **Hedef:** y_h(t) = Σ_{k=1..h} v_ret²_{t+k}. v_ret = aktif kontratın aynı kontrat içindeki log uzlaşma getirisi. Pozisyon gün t uzlaşmasında açılıyor.
  - Sağlamlık hedefi: aynı uzlaşma pencerelerinin Dukascopy saatlik spot getiri karelerinin toplamı. Daha az gürültülü bir vekil.
- **Bilgi seti:** gün t 15:00 UTC'ye kadarki spot (saatlik ve 15:00→15:00 günlük), GVZ_{t−1} (ABD kapanışı t−1), VİOP t−1'e kadar.
  - 13.02.2023'ten beri uzlaşma penceresi 15:00–15:10 UTC (g2). Pratikte boyut 17:59 TSİ'de hesaplanıp pencereye dilimli emirle girilir.
- **Modeller:**
  - EWMA λ=0,94.
  - GARCH(1,1) ve GJR-GARCH(1,1,1): normal QML, spot 15:00 günlük getirisi 2010+, aylık genişleyen yeniden tahmin.
    - Çok adımlı varyans analitik hesaplanıyor. h VİOP günü = n_h spot iş günü, böylece tatil boşluğu hesaba giriyor.
    - Kalıcılık 0,984–0,993. Uzun dönem oynaklığı yıllık %15,3–17,2. GJR'nin asimetri katsayısı 2021'den beri **negatif** (−0,006 ile −0,024): altında ters kaldıraç etkisi var, yükselişler oynaklığı daha çok artırıyor.
  - RV20.
  - Ham GVZ: (GVZ/100)²/252·n_h.
  - GVZ-kal: y/h ~ a + b·GVZ², genişleyen OLS.
  - HAR-RV (Corsi 2009 biçimi): RVd + RVw(5) + RVm(22).
  - HAR-BİL: günlük RV'nin gün (07–15 UTC), akşam (16–20 UTC) ve gece (geri kalanı) bileşenleri + RVw + RVm.
  - HAR-GVZ, log-HAR.
  - KOMB = (GJR + GVZ-kal)/2.
  - HAR'lar 2017-04'ten itibaren VİOP takviminde genişleyen OLS ile kuruldu, aylık yeniden tahmin edildi, ilk tahmin 2018-01.
- **Değerlendirme:**
  - QLIKE (Patton 2011; y=0 günleri için ln f + y/f biçimi).
  - MSE.
  - Diebold–Mariano: EWMA'ya göre, NW lag 2h.
  - Mincer–Zarnowitz: y = a + b·f, H0: a=0, b=1, HAC.
- **Dönemler:** 2018–2021 (model seçimi), OOS 2022-01 → 2026-11, ayrıca 2026.
- **Seçim:** IS QLIKE'a göre h=1 ve 5'te KOMB, h=3'te GVZ-kal (`secilen_model.json`).
  - Uyarı: KOMB'u ilk sonuçları gördükten sonra ekledim. IS'te de en iyi olduğu için seçim yine IS'te yapıldı, ama bu post-hoc bir birleşim.

### 1.2 Sonuçlar (ana hedef VİOP Σr²)

QLIKE, parantezde EWMA'ya karşı DM t (negatif = daha iyi):

| Model | 2018–21 h1 | h3 | h5 | OOS 2022–26 h1 | h3 | h5 | 2026 h1 | h3 | h5 |
|---|---|---|---|---|---|---|---|---|---|
| EWMA | 1,700 | 0,710 | 0,498 | 1,460 | 0,558 | 0,377 | 1,548 | 0,673 | 0,534 |
| GARCH | 1,686 (−0,8) | 0,691 (−1,2) | 0,474 (−1,4) | 1,451 (−1,0) | 0,551 (−0,7) | 0,370 (−0,6) | 1,567 (+0,7) | 0,701 (+0,7) | 0,570 (+0,8) |
| GJR | 1,687 (−0,7) | 0,692 (−1,2) | 0,474 (−1,4) | 1,445 (−1,7) | 0,543 (−1,9) | 0,361 (−2,0) | 1,549 (0,0) | 0,672 (−0,1) | 0,532 (−0,1) |
| GVZ ham | 1,685 (−0,3) | 0,691 (−0,5) | 0,474 (−0,6) | 1,452 (−0,3) | 0,542 (−0,6) | 0,357 (−0,7) | **1,465** (−1,5) | **0,558** (−1,4) | **0,393** (−1,2) |
| GVZ-kal | 1,654 (−1,6) | 0,663 (−1,9) | 0,458 (−1,6) | 1,415 (−2,6) | **0,502** (−3,2) | **0,319** (−3,4) | 1,525 (−0,6) | 0,606 (−1,3) | 0,454 (−1,3) |
| **KOMB** | **1,653** (−2,3) | 0,664 (−2,5) | **0,454** (−2,4) | **1,413** (−4,1) | 0,506 (−4,5) | 0,326 (−4,6) | 1,518 (−1,6) | 0,622 (−1,8) | 0,479 (−1,7) |
| HAR | 1,714 (+0,5) | 0,718 (+0,3) | 0,549 (+0,9) | 1,450 (−0,4) | 0,556 (−0,1) | 0,372 (−0,3) | 1,691 (+1,6) | 0,807 (+1,8) | 0,659 (+1,7) |
| HAR-BİL | 1,730 (+0,9) | 0,727 (+0,6) | 0,564 (+1,0) | 1,459 (0,0) | 0,564 (+0,3) | 0,381 (+0,2) | 1,711 (+1,9) | 0,830 (+1,9) | 0,695 (+1,7) |
| log-HAR | 1,670 (−1,2) | 0,676 (−1,7) | 0,468 (−1,6) | 1,443 (−0,8) | 0,552 (−0,3) | 0,369 (−0,4) | 1,641 (+1,2) | 0,786 (+1,2) | 0,638 (+1,2) |
| RV20 | 1,773 (+3,2) | 0,786 (+3,1) | 0,564 (+2,8) | 1,481 (+2,2) | 0,578 (+2,1) | 0,392 (+1,6) | 1,576 (+1,0) | 0,702 (+1,0) | 0,544 (+0,4) |
| HAR-GVZ | 1,920 | 0,699 | 0,517 | 1,659 | 0,640 | 0,379 | 2,961 | 1,363 | 0,741 |

- HAR-GVZ'nin büyük QLIKE değerleri, seviye OLS'nin bazı günlerde tabana (günlük %0,3) düşen tahminlerinden geliyor. Bu, doğrusal HAR'ın QLIKE altında kırılganlığını gösteriyor.
- Saatlik spot RV hedefiyle sıralama aynı. OOS'ta KOMB'un DM t değerleri −4,7 / −4,8 / −4,8, GJR −2,6 / −2,7 / −2,7, RV20 +3,8 / +3,7 / +3,3. 2026'da hiçbir model EWMA'dan anlamlı ayrışmıyor.

**Mincer–Zarnowitz (OOS 2022–26, ana hedef):**

| Model | b (h1/h3/h5) | p (a=0, b=1) | Ortalama tahmin / gerçekleşen (yıllık %) |
|---|---|---|---|
| EWMA | 0,88 / 0,73 / 0,66 | 0,89 / 0,12 / **0,009** | 18,5 / 18,2 |
| GJR | 1,14 / 0,98 / 0,89 | 0,92 / 0,73 / 0,50 | 17,9 / 18,2 |
| GVZ ham | 1,30 / 1,21 / 1,11 | **0,000** (seviye sapması) | 20,2 / 18,2 |
| GVZ-kal | 1,00 / 1,00 / 0,99 | 0,71 / 0,36 / 0,24 | 17,9 / 18,2 |
| KOMB | 1,17 / 1,09 / 1,04 | 0,86 / 0,82 / 0,58 | 17,9 / 18,2 |
| HAR | 0,68 / 0,57 / 0,53 | **0,003 / 0,001 / 0,002** | 17,1 / 18,2 |
| RV20 | 0,66 / 0,56 / 0,52 | 0,08 / **0,001 / 0,000** | 18,5 / 18,2 |

- 2026'da bütün modellerde h=3/5 için b < 1. Örnek: KOMB 0,79 / 0,51, EWMA 0,41 / 0,21. Yüksek tahminlerin ardından oynaklık beklenenden hızlı söndü (Şubat–Mayıs).
- Ham GVZ'de 2026'da b = 1,78 / 1,40 / 1,02, p = 0,19 / 0,59 / 0,995. Seviye sapması 2026'da kayboldu.

**2026 aylık (yıllık %, h=1 ortalama tahmin):**

| Ay | Gerçekleşen | EWMA | GJR | HAR-BİL | GVZ | KOMB |
|---|---|---|---|---|---|---|
| Ocak | 43,0 | 23,7 | 22,9 | 27,0 | 27,7 | 23,7 |
| Şubat | 40,0 | 44,3 | 40,3 | 46,1 | 34,9 | 38,5 |
| Mart | 36,5 | 38,2 | 33,2 | 31,4 | 36,8 | 36,9 |
| Nisan | 22,8 | 32,4 | 29,0 | 25,4 | 33,0 | 31,4 |
| Mayıs | 19,0 | 25,9 | 23,5 | 18,7 | 28,9 | 24,8 |
| Haziran | 30,1 | 27,3 | 25,0 | 24,1 | 27,4 | 26,2 |
| Temmuz | 23,9 | 26,4 | 24,2 | 21,8 | 26,1 | 24,8 |
| Ağustos | 24,3 | 24,0 | 23,5 | 19,3 | 25,7 | 24,5 |
| Eylül | 20,8 | 22,4 | 21,2 | 21,1 | 25,4 | 23,3 |
| Ekim | 19,3 | 19,8 | 18,5 | 16,9 | 23,4 | 20,3 |
| Kasım (4 gün) | 25,1 | 20,5 | 19,4 | 20,8 | 25,5 | 22,4 |

- 06.11.2026 tahmini (yıllık): KOMB %23,1, EWMA %21,5, GVZ-kal %25,4.
- Standartlaştırılmış getiri z = r/σ̂ (KOMB, 2018–2026): std 0,985, fazla basıklık 1,71. P(|z|>3) = %0,99 (normalde %0,27). %1 kantil −2,70; yeniden standartlaştırınca −2,79. **%99 kayıp için 2,33 değil ≈2,8σ̂ kullanın.**

### 1.3 HAR bileşenleri: gece mi, akşam mı?

Ertesi gün(ler)in VİOP varyansı ~ gün + akşam + gece + RVw + RVm (HAC t, `log_01_vol.txt` sonu):

| h | Dönem | Gün | Akşam (16–20 UTC) | Gece (20–07 UTC + hafta sonu/tatil) | RVm |
|---|---|---|---|---|---|
| 1 | 2017–2026 | 0,28 (t 2,3) | **1,18 (t 7,0)** | 0,06 (t 0,5) | 0,28 (t 3,3) |
| 1 | 2022–2026 | 0,19 (t 0,9) | **1,24 (t 7,8)** | 0,18 (t 0,8) | 0,29 (t 3,0) |
| 5 | 2017–2026 | 0,20 (t 1,9) | **0,27 (t 5,3)** | 0,06 (t 0,6) | 0,31 (t 3,8) |

- Kalıcı bilgi akşam penceresinde (ABD sabahı ve COMEX). Gece hareketleri (Asya, hafta sonu) büyük ama kalıcı değil.
- Bu bilgi örneklem dışı tahminde EWMA'yı geçmeye yetmedi (HAR-BİL OOS DM ≈ 0). Pratik faydası şu: akşam seansı hareketi büyükse ertesi günün boyutunu küçültün.
- Bileşen payları 2017–2026'da gün %45, akşam %22, gece %33. 2026'da gece payı %42,5.

### 1.4 Oynaklık tahmini yönü öngörüyor mu?

Hayır. `register` ailesi `oynaklik_yon`, 15 test:

- Seviye: EWMA, HAR-BİL ve GVZ seviyesinin fwd1/3/5 ile IC'si −0,024 ile +0,012 arasında, |t| ≤ 0,63. OOS IC −0,08 ile −0,01 arasında, hepsi anlamsız.
- Değişim: 5 günlük log σ̂ değişimi h=1'de IC +0,041 (t 1,93), GVZ 5 günlük değişimi +0,044 (t 2,01). Ancak IS t 0,3–0,7. Aile içi BH-FDR'de en küçük q 0,40. Kabul edilmedi.
- Aynı seviyeler |fwd| ile IC 0,19–0,28 (t 6–13). Yani **oynaklık tahmini boyut için kullanılır, yön için değil.**

---

## 2. Oynaklık hedefli boyutlandırma

### 2.1 Kurulum

- w_t = min(2, σ*·√h / σ̂_{t,h}), σ* = yıllık %15 (≈ 2017–2026 VİOP ortalaması %15,8). Pozisyon = sinyal × w.
- Kademeli h günlük tutuş (her gün 1/h dilim). P&L = eff_{t−1}·(e^{r_t}−1) − |Δeff|·maliyet/2. Maliyet 5 ve 10 bps.
- σ̂: KOMB (IS'te seçilen), ayrıca EWMA ve GVZ-kal.
- Sinyaller sentezdeki tanımlarla birebir (`sentez/sinyal_viop_ham.parquet`):
  - LOWMOM h1/h5.
  - GDXJ artığı h3.
  - NFP kuralı h1/h3 (g2 tanımı, 110 olay).
  - Al-tut.
- Ortak dönem 2018-01 → 2026-11.
- Kuyruk ve düşüş karşılaştırmasında her seri ex-post %10 yıllık oynaklığa ölçeklendi (Harvey ve ark. yöntemi). Sharpe bundan etkilenmez.

### 2.2 Sonuçlar (2018–2026; tam tablo `hedef_sonuclar.csv`)

| Sinyal | Boyut | Sharpe 5 bps | 10 bps | Drift çık. | Devir/yıl | MDD (%10 vol) | En kötü gün | Basıklık | Vol-of-vol | 30.01.2026 (1x nominal) |
|---|---|---|---|---|---|---|---|---|---|---|
| Al-tut | ham | 0,57 | 0,57 | −0,01 | 0,1 | −25,0 | −4,80 | 5,6 | 0,40 | −7,80 |
| Al-tut | KOMB | 0,74 | 0,72 | 0,05 | 8,7 | **−17,0** | **−3,53** | 1,6 | **0,12** | **−3,48** |
| Al-tut | EWMA | 0,72 | 0,70 | 0,04 | 14,0 | −20,3 | −4,02 | 2,3 | 0,12 | −3,68 |
| LOWMOM h1 | ham | 0,90 | 0,75 | 0,84 | 40,2 | −16,8 | −3,76 | 14,0 | 0,64 | 0 (pasif) |
| LOWMOM h1 | KOMB | 0,84 | 0,68 | 0,78 | 55,2 | −18,6 | −4,06 | 12,1 | 0,67 | 0 |
| LOWMOM h5 | ham | 0,93 | 0,83 | 0,86 | 20,5 | −43,4 | −3,87 | 15,8 | 0,69 | 0 |
| LOWMOM h5 | KOMB | 0,80 | 0,69 | 0,73 | 28,4 | −47,4 | −4,21 | 17,1 | 0,73 | 0 |
| GDXJ artığı h3 | ham | 0,48 | 0,25 | 0,51 | 72,0 | −14,6 | −4,52 | 56,5 | 0,57 | **+7,79** (kısa) |
| GDXJ artığı h3 | KOMB | 0,57 | 0,27 | 0,62 | 79,2 | −16,7 | −5,21 | 11,8 | 0,25 | +3,97 |
| NFP h1 | ham | 0,52 | 0,35 | 0,53 | 22,8 | −16,8 | −6,17 | 119 | 0,56 | 0 |
| NFP h1 | KOMB | 0,45 | 0,26 | 0,45 | 24,8 | −19,7 | −5,83 | 103 | 0,53 | 0 |
| NFP h3 | ham | 0,73 | 0,62 | 0,74 | 7,6 | −23,0 | −5,42 | 51 | 0,46 | 0 |
| NFP h3 | KOMB | 0,63 | 0,51 | 0,63 | 8,3 | −25,0 | −4,82 | 37 | 0,36 | 0 |

Ek notlar:
- **Mart 2026** (%10 vol ölçeğinde ay toplamı):
  - Al-tut −%9,09 → −%4,61, en kötü gün −%3,14 → −%1,28.
  - GDXJ artığı −%2,33 → −%1,29.
  - NFP h1 −%3,59 → −%1,46.
- **2026'da** al-tut Sharpe −0,51 (ham) → −0,32 (KOMB). Ortalama maruziyet 0,58; zarar −%15,0 → −%5,1 (yıllıklandırılmış).
- **OOS 2022–2026:**
  - Al-tut 0,62 → 0,93 (drift çıkarılmış 0,01 → 0,21).
  - GDXJ 0,71 → 0,92.
  - LOWMOM h5 1,70 → 1,66.
- **Bootstrap Sharpe farkı (hedefli − ham, drift çıkarılmış, durağan blok 20 gün, 2000 tekrar):**
  - Al-tut +0,06 (t 0,54); OOS +0,19 (t 1,25).
  - GDXJ +0,11 (t 1,14); OOS +0,24 (t 1,76).
  - LOWMOM h1 −0,06 (t −1,23), h5 −0,13 (t −2,10).
  - NFP h1 −0,08, h3 −0,11.
  - Aile içi en küçük FDR q 0,48 (24 test).

### 2.3 Harvey ve ark. (2018) ile karşılaştırma

- **Makale:** Harvey, Hoyle, Korgaonkar, Rattray, Sargaison, Van Hemert (2018), "The Impact of Volatility Targeting", *Journal of Portfolio Management* 45(1).
  - 60'tan fazla varlık, 1926'ya uzanan günlük veri.
  - Özet: Sharpe iyileşmesi yalnız "riskli varlıklarda" (hisse, kredi) var ve kaldıraç etkisiyle bağlantılı. "Tahvil, döviz ve emtiada oynaklık hedeflemenin Sharpe'a etkisi ihmal edilebilir." Ama "uç getiri olasılığını bütün varlık sınıflarında azaltıyor" ve oynaklığın oynaklığını düşürüyor.
  - Kaynak: özet metni Quantpedia sayfasından okundu; SSRN 3175538 sayfası 403 verdi.
- **Bizim bulgu bununla aynı:**
  - Al-tut altında Sharpe farkı anlamsız (+0,06).
  - Maksimum düşüş %32 azaldı (−25,0 → −17,0). En kötü gün %26 azaldı. Vol-of-vol 0,40 → 0,12. Basıklık 5,6 → 1,6.
  - Altında kaldıraç etkisi ters: GJR γ < 0. Hisse senedindeki "momentum benzeri" kazanç beklenmez, beklendiği gibi de çıkmadı.
- **Sinyallerde:** hedefleme kuyruğu kısaltıyor (GDXJ basıklığı 56 → 12) ama Sharpe'ı artırmıyor. LOWMOM'da düşürüyor, çünkü LOWMOM zaten düşük oynaklık rejiminde açılıyor. Hedefleme o günlerde pozisyonu 1,4–2 kata çıkarıyor ve devri %37 artırıyor.
- **Öneri:** al-tut ve GDXJ benzeri sürekli maruziyetlerde oynaklık hedefi kullanın (risk aracı olarak). LOWMOM'u sabit nominalle tutun. NFP gibi olay kurallarında hedefleme gerekmez, ama σ̂ ile üst sınır koyun (bölüm 5).

---

## 3. Teminat, etkin kaldıraç, çağrı olasılığı, limit geçmişi

### 3.1 Takasbank risk parametreleri (birincil kaynak, PDF'lerden)

| Genel mektup | Tarih | Geçerlilik | VİOP XAUUSD PSR | XAUUSD vadeler arası yayılma riski |
|---|---|---|---|---|
| GM 2126 (r1'den) | 12.02.2026 | 17.02 / 02.03.2026 | %6,7 / %10,0 | — |
| GM 2150 | 11.06.2026 | 15.06.2026 | %10,0 | 305 USD |
| GM 2163 | 13.08.2026 | 17.08.2026 | %10,0 | 325 USD |
| GM 2169 | 11.09.2026 | 15.09.2026 | %10,0 | 325 USD |
| GM 2171 | 29.09.2026 | 01.10.2026 | %10,0 | 310 USD |
| GM 2174 | 13.10.2026 | 15.10.2026 | %10,0 | 310 USD |
| GM 2176 | 27.10.2026 | 02.11.2026 | %10,0 | **295 USD** |

- Aynı mektuplar: aşırı hareket senaryo çarpanı 3, kapsama oranı %32.
- Düz vadeli pozisyonda aşırı hareket kaybı 3 × PSR × 0,32 = 0,96 × PSR < PSR olduğu için bağlamıyor. Başlangıç teminatı ≈ PSR × fiyat. Bu bir çıkarım; BISTECH yönteminin tam formülünü Takasbank prosedüründen ayrıca okumadım.
- GM 2177 (06.11.2026) risk parametresi içermiyor (tatbikat duyurusu). 06.11.2026 itibarıyla geçerli değer GM 2176'dakidir.
- Takasbank'ın VİOP için sabit bir "sürdürme teminatı = %75" kuralı birincil kaynakta **bulunamadı**. GM tablolarındaki "Günsonu Sürdürme Seviyesi Katsayısı %100" Kıymetli Madenler Piyasası'na (spot) ait, VİOP'a değil.

### 3.2 Aracı kurumlar

| Kurum | XAUUSD | Kural | Kaynak |
|---|---|---|---|
| QNB Invest | Kurum PSR **%20,0** (08.10.2026 güncellemesi; r1'e göre 02.06.2026'dan beri %20) | Gün sonu teminat < başlangıç teminatının %100'ü → akşam SMS/e-posta çağrısı. Anlık oran ≥ %50 olmalı. Teminatın ≥ %50'si TL | qnbinvest.com.tr duyuru 08.10.2026; VİOP teminatları sayfası |
| GCM Yatırım | %10 → %10 (02.11.2026 gün başı) | — | gcmyatirim.com.tr duyuru 30.10.2026 |
| Gedik | Ek teminat %11 → **%0** (01.07.2026 seans açılışı). 27.02.2026'da "güncel %85 → yeni ek %11" | Ek teminat Takasbank tutarının üstüne ekleniyor (oranın tanımı sayfada açık değil) | gedik.com 30.06.2026 ve 27.02.2026 duyuruları |
| Diğer (İş, Yapı Kredi, Garanti BBVA, Ak) | **bulunamadı** | — | — |

Sözleşme başına teminat (F = 4.078,8):

- Takasbank tabanı: 407,9 USD (≈20.805 TL).
- QNB: 815,8 USD (≈41.610 TL).

### 3.3 Etkin kaldıraç ve teminat tamamlama çağrısı olasılığı

- **Model:**
  - Hesaba E_0 = k × IM_0 yatırılıyor. IM_t = PSR × uzlaşma_t, yani fiyat değiştikçe IM de değişiyor. Etkin kaldıraç = 1/(k·PSR).
  - Çağrı: gün sonu E_t < IM_t (QNB'nin %100 kuralı).
  - Anlık kontrol: önceki akşam ve normal seans en düşük/en yüksek fiyatıyla E < 0,5 × IM.
- **Veri:** örtüşen başlangıç günleri, aynı kontrat içinde (`teminat_cagri_olasilik.csv`).

| Dönem | Kurum PSR | k (IM katı) | Kaldıraç | Yön | Çağrı h1 | h3 | h5 | Çağrı ya da anlık <%50, h5 |
|---|---|---|---|---|---|---|---|---|
| 2017–2026 | %10 | 1,0 | 10x | uzun / kısa | %47,3 / %52,4 | %64,7 / %71,0 | %70,4 / %78,6 | %70,4 / %78,6 |
| 2017–2026 | %10 | 1,5 | 6,7x | uzun / kısa | %0,1 / %0,1 | %0,5 / %1,3 | %1,3 / %3,9 | %1,3 / %3,9 |
| 2017–2026 | %10 | 2,0 | 5x | uzun / kısa | %0 / %0 | %0 / %0,1 | %0,2 / %0,3 | %0,2 / %0,3 |
| 2017–2026 | %10 | 3,0 | 3,3x | ikisi | %0 | %0 | %0 | %0 |
| 2026 | %10 | 1,5 | 6,7x | uzun / kısa | %1,0 / %0,5 | %4,1 / %8,2 | %8,8 / %14,8 | %8,8 / %14,8 |
| 2026 | %10 | 2,0 | 5x | uzun / kısa | %0 / %0 | %0,5 / %0,5 | %2,2 / %1,6 | %2,7 / %1,6 |
| 2026 | %20 (QNB) | 1,0 | 5x | uzun / kısa | %51,5 / %48,1 | %68,0 / %63,4 | %73,6 / %72,0 | aynı |
| 2026 | %20 (QNB) | 1,5 | 3,3x | uzun / kısa | %0 / %0 | %0,5 / %1,0 | %0,5 / %3,3 | %0,5 / %3,3 |

**İleriye dönük simülasyon** (`teminat_cagri_simulasyon.csv`): KOMB standartlaştırılmış artıkları, 200.000 yol, %10 PSR.

| Senaryo (yıllık σ) | k=1,5 (6,7x) uzun / kısa, h5 | k=2 (5x) uzun / kısa, h5 | k=3 (3,3x), h5 |
|---|---|---|---|
| 06.11.2026 KOMB (%23,1) | %5,3 / %10,4 | %0,1 / %0,5 | %0 |
| 2026 ortalaması (%29) | %10,4 / %17,5 | %0,5 / %2,0 | %0 |
| Ocak 2026 (%43) | %22,4 / %31,5 | %3,6 / %9,0 | %0 / %0,4 |

- **%99 kayıp, özsermayenin yüzdesi** (KOMB σ̂ 06.11.2026, z_%1 = −2,79): 10x kaldıraçta 1/3/5 gün için %40,7 / %69,2 / %88,0. 5x'te %20,3 / %34,6 / %44,0. 3,3x'te %13,6 / %23,1 / %29,3. 2x'te %8,1 / %13,8 / %17,6.
- **Kısalar daha sık çağrı alıyor.** Fiyat yükselince hem zarar hem IM artıyor. Ayrıca 2017–2026 boyunca yükseliş eğilimi vardı.
- **Pratik:** VİOP'ta "teminat = risk" değil. 1–5 günlük taşımada **en az 2 kat başlangıç teminatı** tutun (Takasbank tabanlı kurumda ≤5x, QNB'de ≤2,5x). Ocak–Mart 2026 benzeri rejimde **3 kat** (≤3,3x) tutun.

### 3.4 ±%10 fiyat limiti geçmişi (ön vade, 2017-03 → 2026-11; `limit_gecmisi.csv`)

- **Kural:** baz fiyat = önceki günün uzlaşması. Akşam seansında baz = aynı günün uzlaşması. Limit ±%10 (Prosedür rev. 70, Ek-1 R).
- **Md. 49:** "olağanüstü durumların ortaya çıkması veya piyasa koşulları çerçevesinde" Genel Müdür limitleri geçici olarak değiştirebilir. Genel Müdür Yardımcısı/Piyasa Müdürü sözleşme bazında "iki katına kadar" yükseltebilir.
- **Uzlaşma değişimi:** en büyük −%7,80 (30.01.2026) ve +%5,59 (24.03.2020). |Δ| > %5 olan 5 gün, > %7 olan 2 gün, ≥ %10 olan gün yok.
- **Normal seans gün içi sapma (en düşük/baz):**
  - 02.02.2026 −%13,73
  - 23.03.2026 −%12,86
  - 24.08.2023 −%10,00
  - 30.01.2026 −%8,97
  - 16.03.2020 −%7,40
  - Yukarı en fazla +%6,39 (24.03.2020).
- **Bütün vadeler:** en kötü −%16,25 (F_XAUUSD0426, 02.02.2026), en yüksek tam +%10,00 (F_XAUUSD1222, 06.07.2022, uzak vadede tek işlem).
- **Akşam seansı:** en kötü −%5,69 (29.01.2026), en iyi +%3,43.
- **02.02.2026 yorumu:** gram altın (F_XAUTRYM) en düşükleri üç vadede de **tam −%20,00**, gümüş **−%30,00**. Bu, limitlerin o gün iki katına çıkarıldığını gösteriyor. Altında ±%10 aşıldı, yeni bant bağlamadı. Duyuru metni **bulunamadı**; bu bir çıkarım.
- **24.08.2023:** F_XAUUSD0823 tam alt limitte işlem gördü (1.728,3), uzlaşma +%0,20. Tek bir limit fiyatlı emir. Piyasa ve stop emirleri limite kadar dolabilir.
- **Spot 15:00→15:00 (2010–2026):** en kötü −%9,31 (15.04.2013). Tek gün > %9.

---

## 4. Boşluk (gap) riski

### 4.1 TR tatilleri: VİOP kapalı, dünya açık

**Tanım** (`tatil_bosluklari.csv`, 70 kapanış, 2017–2026):

- İşlenemez boşluk = ln spot(ilk işlem anı) − ln spot(son işlem anı).
- Son işlem anı: önceki günün normal seans sonu (15:10 UTC; yarım günde 09:40) ya da varsa akşam seansı sonu (20:00 UTC).
- İlk işlem anı: açılıştan önceki takvim gününde akşam seansı varsa 16:00 UTC, yoksa 06:30 UTC.

| Dönem | n | Std | |boşluk|>%1 | |boşluk|>%2 | En kötü |
|---|---|---|---|---|---|
| 2017-03 → 2026-11 | 70 | %1,55 | %35,7 | %2,9 | −%9,90 |
| 2020-09 → 2025 | 35 | %0,99 | %31,4 | %0 | −%1,82 |
| 2026 | 8 | **%3,32** (ort. −%1,93) | %50 | %12,5 | −%9,90 |

**2026 kapanışları:**

| Son işlem (eve) | Açılış | Kapalı iş günü | Saat | Spot boşluğu | Ara en düşük | Açılış günü VİOP v_ret | Açılış günü en düşük/baz |
|---|---|---|---|---|---|---|---|
| 31.12.2025 | 02.01 | 1 (01.01) | 39,3 | +%0,73 | −%0,80 | +%0,23 | +%0,05 |
| 19.03 (yarım) | 23.03 | 1 (20.03) + h.sonu | 92,8 | **−%9,90** | −%8,86 | **−%5,24** | **−%12,86** |
| 22.04 | 24.04 | 1 (23.04) | 34,5 | −%1,29 | −%1,45 | −%0,40 | −%1,55 |
| 30.04 | 04.05 | 1 (01.05) + h.sonu | 82,5 | −%0,51 | −%1,18 | −%1,28 | −%2,35 |
| 18.05 | 20.05 | 1 (19.05) | 34,5 | −%1,88 | −%2,14 | −%0,26 | −%1,67 |
| 26.05 (yarım) | 01.06 | 3 (27–29.05) + h.sonu | 140,8 | −%0,31 | −%3,39 | −%1,42 | −%1,66 |
| 14.07 | 16.07 | 1 (15.07) | 34,5 | −%0,67 | −%0,77 | −%2,36 | −%2,85 |
| 28.10 (yarım) | 30.10 | 1 (29.10) | 44,8 | −%1,64 | −%1,53 | −%3,51 | −%4,06 |

- Açılış günü VİOP getirisi işlenemez boşlukla 0,79 korelasyonlu (n=43, 2020-09+).
- Boşluk sırasında spotun ara sapması kapanış sonucundan büyük olabiliyor. Örnek: 26.05 → 01.06 arasında −%3,39'a indi, −%0,31'de kapandı.
- **1/3/5 günlük getiriye katkı** (`bosluk_katki.csv`):

| Dönem | Tatil açılış günü payı | Uzlaşma varyansındaki payı | Ort. r² oranı | h=5 pencere payı / varyans payı |
|---|---|---|---|---|
| 2017–2026 | %2,88 | %5,97 | 2,14 | %13,7 / %15,1 |
| OOS 2022–2026 | %2,79 | %6,29 | 2,34 | %13,7 / %16,4 |
| 2026 | %3,77 | %6,87 | 1,88 | %16,5 / **%23,4** |

- **Tahmin modelleri bu günlerde nasıl?** (gerçekleşen r² / tahmin, `takvim_kalibrasyon.csv`):
  - Spot gün sayısıyla ölçeklenen GARCH/GJR/EWMA tatil açılışında 0,85–0,89. Takvimi hesaba katıyorlar.
  - VİOP günüyle ölçeklenen GVZ-kal 1,92, HAR'lar 2,43–2,48, KOMB 1,22.
  - **HAR/GVZ kullanıyorsanız tatil penceresinin varyansını spot gün sayısıyla çarpın** ya da en az 2 katına çıkarın.
- **Yön:** tatil açılışından ya da Pazartesiden sonra yön etkisi yok. 6 test, |t| ≤ 1,28, en küçük q 0,83.

### 4.2 Cuma → Pazartesi

`bosluk_ozet.csv`; r6 tanımı 20:00 → 07:00 UTC:

| Dönem | Hafta içi gece std | Cuma→Pzt std | Oran | Pzt |boşluk|>%2 | En kötü Pzt |
|---|---|---|---|---|---|
| 2017-03 → 2026-11 | %0,504 | **%0,728** | 1,44 | %1,29 | −%9,08 (02.02.2026) |
| 2020-09 → 2025 | %0,408 | %0,532 | 1,30 | %0 | −%1,55 |
| 2026 | %1,145 | **%1,851** | 1,62 | %12,2 | −%9,08 |

- r6'daki %0,726'yı %0,728 olarak yeniden ürettim. Hafta içi değer bende %0,504 çıktı (r6: %0,474; dönem ya da gün seçimi farkı olabilir).
- Akşam seansı sonu → 06:30 tanımıyla 2020-09+ varyans oranı 2,15 (F p ≈ 0, Levene p = 0,00013).
- Uzlaşmadan uzlaşmaya Pazartesi günleri: std %1,065'e karşı %0,981. Varyans payı %21,8, gün payı %19,2.
- Bütün modeller Pazartesi penceresinde riski 1,17–1,19 kat (HAR'da 1,27–1,38) düşük gösteriyor.

### 4.3 Aralık 2026 vadesi: LBMA AM uzlaşması ve roll

- **Kural (Prosedür rev. 70, Ek-1 R):** vade sonu fiyatı LBMA Gold Price PM. "Son işlem gününde Londra'da öğleden sonra altın fiyat sabitleme seansı yapılmazsa, sabah seansında oluşan altın Dolar/Ons fiyatı" kullanılır. Hiç fiyat yoksa 17:00 TSİ spot alış-satış ortalaması.
  - Son işlem günü vade ayının son iş günü: **31.12.2026 Perşembe**.
  - O gün yılın son işlem günü olduğu için akşam seansı yok (tatiller.csv; r1).
- **LBMA:** 15.12.2025 duyurusu: "24 ve 31 Aralık 2025'te altın, platin ve paladyum için PM ihalesi yapılmayacak". 2026 duyurusu henüz yok (2025'teki duyuru 15 Aralık'ta çıkmıştı).
- **Veri** (`yil_sonu_uzlasma.csv`):

| Vade | Vade sonu fiyatı | Spot 10:30 UTC (dakika) | Spot 15:00 UTC (dakika) | Fark AM | Fark PM |
|---|---|---|---|---|---|
| F_XAUUSD1219 (31.12.2019) | 1.523,0 | 1.522,9 | 1.518,3 | +%0,01 | +%0,31 |
| F_XAUUSD1225 (31.12.2025) | 4.308,0 | 4.309,5 | 4.343,4 | −%0,03 | **−%0,81** |

  - Diğer yıllar saatlik veriyle ayırt edilemedi (fark ≤ %0,4).
- **Risk:** 1226'yı vadeye taşıyan işlemcinin çıkış fiyatı 18:00–18:10 TSİ VWAP yerine 13:30 TSİ (10:30 UTC) fiyatı olur.
  - 10:30 → 15:00 UTC spot hareketinin std'si 2017–2026'da %0,58, 2026'da %0,86. 2026 günlerinin %14,4'ünde |x| > %1, en büyük %4,60.
  - Beklenen değerde sapma yok, ama ≈1σ = %0,86'lık planlanmamış bir zamanlama riski var.
  - Aynı gün 0227'ye roll ortak bir fiyattan yapılamaz: 1226 AM'de kapanır, 0227 akşam 18:10'da uzlaşır.
- **Roll önerisi:**
  1. 1226 pozisyonunu **en geç 30.12.2026 uzlaşmasında** kapatın ya da devredin. 31.12'ye taşımayın.
  2. Devri **24–30.12.2026** arasında yapın. Normal seansta F_XAUUSD 1226/0227 vadeler arası strateji emri kullanın (fiyat limiti sabiti k = 15 USD, akşam seansında strateji emri yok). Ya da iki bacağı 18:00–18:10 TSİ uzlaşma penceresinde dilimli emirle aynı anda girin.
     - Geçmişte hacim ön vadeden sonraki vadeye vadeden 0–5 iş günü önce geçti (Aralık 2019: 4, 2023: 4, 2024: 1–5, 2025: 1; g2 `hacim_devri.csv`).
     - Devir sırasında takvim farkı pozisyonu için teminat 295 USD (GM 2176).
  3. Yeni işlemleri 0227'de açın: h=5 işlemlerde 24.12'den, h=3'te 28.12'den, h=1'de 30.12'den itibaren. Böylece hiçbir çıkış 31.12'ye düşmez.
  4. 31.12 akşamı seans yok, 01.01.2027 Cuma tatil. 31.12 uzlaşmasından sonra 0227 pozisyonu 4 gün işlemsiz kalır (dünya piyasaları da 01.01'de büyük ölçüde kapalı).

---

## 5. Somut boyutlandırma formülü

**N (sözleşme) = ⌊ b · √h · E_USD / ( κ · σ̂_{t,h} · F_t · 1 ons ) ⌋**

Değişkenler:
- E_USD = özsermaye (TL / USDTRY).
- b = günlük 1σ risk bütçesi (öneri %1 ≈ yıllık %15,9; h günlük işlemde b·√h).
- σ̂_{t,h} = h günlük tahmini oynaklık. KOMB önerilir: √[(GJR_h + GVZ-kal_h)/2]. Basit alternatif: EWMA λ=0,94 × √(spot gün sayısı).
- F_t = vadeli fiyat.
- κ = takvim düzeltmesi:
  - Pencerede hafta sonu varsa √1,18 = 1,09.
  - TR tatil açılışı varsa √2 = 1,41. 2026'daki 23.03 olayı yüzünden muhafazakâr seçildi; KOMB için 2018–2026 ortalaması √1,22.
  - Ertesi gün tahmini için akşam seansı varyansı yüksekse ek pay.

Kısıtlar (hangisi daha küçük N veriyorsa):
1. **Teminat:** N · PSR_kurum · F_t ≤ E_USD / 2. Kurum PSR'ı %10 ise kaldıraç ≤ 5x, QNB %20 ise ≤ 2,5x. Ocak 2026 benzeri rejimde (σ̂ > yıllık %35) payda 3 olsun.
2. **Kuyruk:** N · F_t · 2,8 · κ · σ̂_{t,h} ≤ K_max · E_USD (öneri K_max = %3 h=1 için, %6 h=5 için). 2,8 = KOMB artıklarının %1 kantili.
3. **Uç durum:** tatil ya da hafta sonu penceresinde spot boşluk senaryosu −%10 ile N · F_t · 0,10 ≤ %15 · E_USD. 23.03.2026 boşluğu −%9,90 idi.

Eşdeğeri: oynaklık hedefi w = σ*/σ̂ (nominal/özsermaye). σ* = yıllık %15 için N = w·E/F.

**Örnek (06.11.2026; F = 4.078,8, USDTRY = 51,008, KOMB σ̂ = %1,46 / %2,48 / %3,16):**

| Özsermaye | h | Pencere | N (kesirli) | N | Nominal | Kaldıraç | QNB IM / özsermaye | %99 kayıp |
|---|---|---|---|---|---|---|---|---|
| 1.000.000 TL (19.605 USD) | 1 | normal | 3,30 | 3 | 12.236 USD | 0,62x | %12,5 | 497 USD (%2,54) |
| 1.000.000 TL | 1 | TR tatili | 2,33 | 2 | 8.158 USD | 0,42x | %8,3 | 469 USD (%2,39) |
| 1.000.000 TL | 5 | normal | 3,40 | 3 | 12.236 USD | 0,62x | %12,5 | 1.077 USD (%5,49) |
| 5.000.000 TL (98.024 USD) | 1 | normal | 16,48 | 16 | 65.261 USD | 0,67x | %13,3 | 2.653 USD (%2,71) |
| 300.000 TL (5.881 USD) | 1 | normal | 0,99 | 0 | — | — | — | — |

- **Taneciklik:** 1 sözleşme ≈ 4.079 USD ≈ 208 bin TL nominal. b = %1/gün ile 1 sözleşmeyi taşımak için ≈ 5.946 USD ≈ 303 bin TL özsermaye gerekir. Daha küçük hesapta tek sözleşme bile hedeflenen riskin üstündedir. Bu durumda h'yi kısaltın ya da F_XAUTRYM (gram, TL; PSR %14) ile daha küçük adım kullanın.

---

## 6. Bulunamayanlar ve zayıflıklar

- **Bulunamadı:**
  - 02.02.2026 ve 23.03.2026'da XAUUSD fiyat limitlerinin genişletildiğine dair BIST duyurusu (veriden çıkarım).
  - LBMA'nın 31.12.2026 için PM ihalesi kararı.
  - Takasbank VİOP sürdürme teminatı oranı.
  - İş, Yapı Kredi, Garanti BBVA ve Ak Yatırım'ın XAUUSD ek teminatı.
  - Gedik'teki "ek teminat oranı"nın tam tanımı.
- **Oynaklık hedefi KOMB:** ilk sonuçlardan sonra eklenmiş bir birleşim; IS'te de en iyiydi. Oynaklık testlerinde vekil gürültülü (günlük r²). Spot saatlik RV ile sıralama teyit edildi.
- **Çağrı olasılıkları:** örtüşen pencerelerden geliyor (bağımsız değil). 2026 yalnız 182 başlangıç günü. Simülasyon i.i.d. artık varsayıyor. Ocak 2026 senaryosu kümelenmeyi kısmen yansıtıyor.
- **Boşluk istatistikleri** küçük örneklemli: 2026'da 8 tatil, 41 Pazartesi. 2026 rakamlarını rejim göstergesi olarak okuyun, kalıcı parametre olarak değil.
- **Sinyal Sharpe'ları sentez sinyalleriyle aynı.** Bu raporda yeni sinyal aranmadı. Oynaklık hedefi sinyallerin seçim yanlılığını gidermez.

---

## 7. Kaynaklar

**Birincil (indirildi, `scratchpad/dl_g4/`):**
- Takasbank GM 2150: https://marbas.com.tr/assets/Takasbank-Genel-Mektup-2150.pdf
- Takasbank GM 2163: https://marbas.com.tr/assets/Takasbank-Genel-Mektup-2163.pdf
- Takasbank GM 2169: https://www.takasbank.com.tr/documents/file/Takasbank_Announcement/2169-5f98f54a-f484-48ab-b280-c47642afef92.pdf
- Takasbank GM 2171: https://www.takasbank.com.tr/documents/file/Takasbank_Announcement/2171-9bb642b4-c7eb-4c00-82cc-c1d603345ebb.pdf
- Takasbank GM 2174: https://www.takasbank.com.tr/documents/file/Takasbank_Announcement/2174-5201d2a7-ed08-4591-a8cd-a4e092e45951.pdf
- Takasbank GM 2176: https://www.takasbank.com.tr/documents/file/Takasbank_Announcement/2176-a7dd95c4-3dec-453f-8106-05643d3da68e.pdf
- Takasbank GM 2177: https://www.takasbank.com.tr/documents/file/Takasbank_Announcement/2177-b19b9bc9-62db-4bb8-bd7c-bd31d23be775.pdf
- Takasbank genel mektup listesi: https://www.takasbank.com.tr/tr/duyurular/genel-mektuplar
- QNB PSR 08.10.2026: https://www.qnbinvest.com.tr/duyuru/-viop-psr-oran-guncellemesi-08102026
- QNB VİOP teminatları: https://www.qnbinvest.com.tr/viop-teminatlari
- GCM 30.10.2026: https://www.gcmyatirim.com.tr/duyurular/duyuru-viop-baslangic-teminat-degisikligi-hakkinda-30-10-2026
- GCM 26.05.2026: https://www.gcmyatirim.com.tr/duyurular/duyuru-viop-baslangic-teminat-degisikligi-hakkinda-26-05-2026
- Gedik 30.06.2026: https://gedik.com/viop-duyurulari/teminat-degisiklikleri/viop-ek-teminat-degisikligi-3006
- Gedik 27.02.2026: https://gedik.com/viop-duyurulari/teminat-degisiklikleri/viop-teminat-degisikligi-2702
- BIST VİOP Prosedürü rev. 70 (01.07.2026): md. 7 (akşam seansına dahil sözleşmeler: Dolar/Ons Altın), md. 49 (limit değişikliği), Ek-1 R (Dolar/Ons Altın). https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf (yerel metin `dl1/proc.txt`)
- BIST duyuru 30572 (19.11.2024): bakır vadelisi. Ekindeki md. 7 tablosunda Dolar/Ons Altın akşam seansında. https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- LBMA, 15.12.2025: https://www.lbma.org.uk/articles/market-and-lbma-price-auction-closing-times-2025
- BIST günlük ve akşam bültenleri: https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv ; viop_as_bul_YYYYMMDD.csv

**Akademik:**
- Harvey, C. R., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M., Van Hemert, O. (2018), "The Impact of Volatility Targeting", JPM 45(1).
  - Özet: https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies
  - SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3175538 (403)
- Yöntem referansları (bu turda yeniden okunmadı): Patton (2011), J. Econometrics 160(1), QLIKE/MSE'nin gürültülü vekile dayanıklılığı. Corsi (2009), J. Financial Econometrics 7(2), HAR-RV.

**Kod** (`out/g4_risk/`):
- `g4_common.py`
- `g4_01_vol.py`: tahmin, değerlendirme, yön testleri.
- `g4_02_hedef.py`: oynaklık hedefi.
- `g4_03_teminat.py`: PSR tablosu, çağrı olasılığı, limit geçmişi.
- `g4_04_bosluk.py`: tatil ve hafta sonu boşlukları, yıl sonu AM.
- `g4_05_boyut.py`: takvim kalibrasyonu, boyut örneği.
- `run_all.sh`.
- Kayıt: `out/registry/g4_risk.csv` (75 test: 30 DM, 15 yön, 24 hedefleme Sharpe farkı, 6 boşluk yönü).
