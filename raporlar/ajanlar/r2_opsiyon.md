# OPSİYON — 2. Tur: Çapraz kontrol ve nihai komite portföyü (28.10.2026)

Etiketler: [D] kaynakla doğrulandı · [H] kendi hesabım (`r2_checks.py`, `r2_portfolio.py`) · [T] tahmin · [V] varsayım.

## A. Fikir bazında kontrol

**MAKRO-1 — F_USDTRY1226 kısa**
- **Doğrulananlar:** 1 kontrat = 1.000 $ (bülten çarpanı ≈1.000) [2]. PSR %11 → teminat 5.772 TL/kontrat [5]. Kur yılbaşından bu yana +%15,9, yıllık %19,3 (MAKRO %16,1 / %19,6 diyor) [1]. Fed 16.09'da +25 bp [12].
- **Hata:** "+%12 gap = −3.258 TL/kontrat (%2,0)" yanlış. Doğrusu 52,47 × %12 × 1.000 = **−6.297 TL/kontrat**. 6 kontratta 37,8 bin TL, yani 1 mn TL sermayenin **%3,8'i**. 3.258 TL aslında +%6,2'lik harekete denk geliyor. +%5'te kayıp %1,6. Stop riski %0,44 ✓.
- **Beklenen değer:** Şok kolunun yarısı +%12 sayılırsa beklenen değer +410'dan **+177 TL/kontrat**a iner.
- **Bağlam:** Son 2 yılın en büyük kapanış-kapanış artışı +%3,5 (20.03.2025) [1]. Yani +%12 gün içi ya da devalüasyon kuyruğu.
- **Oy: KOŞULLU, 6/10.** 1 mn TL başına 6 değil **3,5 kontrat** (stres ≤%2,5). Likidite el verirse kuyruğa C56000 (27.10'da 168 kontrat, 418 TL [2]).

**MAKRO-2 — koşullu long F_XU0301226**
- **Oy: KOŞULLU, 4/10.** "+%10 önce, −%6 sonra" olasılığını %45 varsayıyor; ENDEKS'in benzerlerinde aynı tip olasılık 0,32. 1 mn TL'de 0,5 kontrat uygulanamaz. Bu görüş call spread ile ifade edilmeli (bkz. D).

**ENDEKS-1 — rallide short**
- **Doğrulananlar:** AP 314.401 [2], PSR, taşıma 688/64 = 10,7 puan/gün, SPK esnekliğinin 30.10'da bitmesi [13]. XU100'ün Eylül kapanış zirvesi 9.09'da 14.505,5 [1]; benim 1. turdaki "11.09, 14.467" hatalıydı.
- **Çelişki:** Fiyat limiti ±%15 değil, 2020/20 duyurusuyla "ikinci duyuruya kadar" ±%10 [11].
- **Boyut ✓:** 1 kontrat → 4.500 TL (%0,45). Girişten +%8 squeeze olursa 1.204 puan = %1,2.
- **Oy: KOŞULLU, 5/10.** ŞEYTAN'la aynı enstrüman ve aynı yön; tek kova sayılmalı.

**ENDEKS-2 — dipte long**
- **Oy: HAYIR, 3/10.** ENDEKS'in kendi hesabıyla beklenen değer ≈0 ve taşıma aleyhte. Aynı görüş call spread ile tanımlı riskle alınabilir.

**ŞEYTAN — rallide short**
- **Olgu hatası:** "9 Eylül 14.405, tarihi zirve 14.601" yanlış. 9.09 kapanışı 14.505,5; 2 yıllık kapanış zirvesi 15.133,5 (11.05.2026) [1].
- **Mantık hatası 1:** "Spot 13.950'de yatay kalırsa bile +1.025 puan" tutmuyor. Spot yatay kalırsa vadeli 14.644'ten spota yakınsar ve 14.875'teki emir hiç dolmaz.
- **Mantık hatası 2:** "%1,2 baz iskontosu → kalabalık short" çıkarımı zayıf. İskonto Temmuz'da da vardı; yapısal (MAKRO, ENDEKS).
- **Beklenen değer:** 0,5 × 1,59R − 0,35R = **0,45R**, 0,6R değil.
- **Boyut:** 7 × 675 × 10 = 47,3 bin TL = 5 mn TL'nin %0,95'i ✓. Ancak stop kapanış bazlı; +%8 gap'te kayıp %1,7.
- **Oy: KOŞULLU, 5/10.** ENDEKS ile birleşsin, stop gün içi 15.550 olsun.

**HİSSE-1 — long GARAN / short YKBNK**
- **Doğrulananlar:** PSR %14,4 / %15,8 [5]; XU030 −%17,9 ✓.
- **Likidite sorunu:** 27.10'da F_GARAN1226 yalnızca 134 kontrat işlem gördü (AP 687), F_YKBNK1226 1.571 (AP 3.132). Kasım kontratları 46.467 ve 730.300 [2]. Kasım kontratı kullanılmalı; 27.11'de kapat veya çevir.
- **Teminat:** Nominal 241,6 + 208,7 bin TL; Takasbank teminatı 67,8 bin TL (%6,8), aracı kurum 2× uygularsa %13,6 ✓.
- **Gap:** Pair'in günlük σ'sı %1,0 (long nominaline göre); en kötü gün −%6,3, en kötü 3 gün −%7,4 [H,1]. Stop atlanırsa kayıp ~%1,5. YKBNK +%10 tavan yaparken GARAN sabit kalırsa −20,9 bin TL = **%2,1**.
- **Piyasa şokları:** ±%8 ve −%15 senaryolarında net etki ≈±%0,2 (beta nötr). Not: 40 günlük σ √t ile ~%6 çıkıyor, ~%4 değil; −%4 stop sanılandan sık tetiklenir.
- **Oy: KOŞULLU, 5/10.** Ön koşul: GARAN 3. çeyrek net kârı ≥30 mlr TL.

**HİSSE-2 — long SAHOL / short AKBNK**
- **Oy: HAYIR, 3/10.** HİSSE'nin kendi hesabıyla kâr taşımaya gidiyor. SAHOL tasfiyedeki fonlarda en yaygın BIST30 payı. F_SAHOL1226'da günde yalnızca 937 kontrat.

## B. Özel konular

**1. Baz çerçevesi.** S = 13.961, F = 14.644, S·(1 + 0,36 × 64/365) = 14.842.

| Karşılaştırma | Vadede P/L | Eşik |
|---|---|---|
| Long vadeli + TL nakit vs. yalnız TL nakit | S_T − F | S_T ≥ 14.644 (spot +%4,9) → **ENDEKS / ŞEYTAN** |
| Long vadeli + nakit vs. long spot | S·e^(rT) − F ≈ +200 puan | vadeli %1,4 avantajlı → **MAKRO / OPSİYON** |
| Spot tutup short vadeliyle hedge | kilitlenen %4,9 < faiz %6,5 | hedge maliyeti ~%1,4 |

- **İki çerçeve çelişmiyor.** %4,9, hisse riski almanın TL nakde karşı eşiği; %1,4 ise spot sahibine göre göreli değer.
- **İskontonun kaynağı:** Vergi sonrası ~%29 kazanan yatırımcı için adil vadeli 14.671 ≈ piyasa [V, MAKRO]. Yani iskonto yatırımcı tipine bağlı bir yapı.
- **Call spread'im için geçerli olan nakit çerçevesi.** Başabaş S_T ≥ 14.840 olmalı; primin faizi (~22 puan) eklenince ~14.860. Opsiyon piyasa vadelisinden fiyatlandığı için iskonto zaten maliyete yansımış: spread 350 puan, teorik vadeliyle 404 olurdu.

**2. IV anomalisi.**
- **Uzlaşma fiyatı (~%24 IV) işlem yapılabilir bir fiyat değil.** 27.10'da C14500'ün gün içi en yükseği 505'te kaldı, uzlaşma 628 [2].
- **Gerçek işlemler:**
  - 27.10'da C14500 492'de açıldı, 300'e indi; 324 işlemde 5.667 kontrat.
  - P14500 264'ten 168'e indi; ama yalnızca 29 işlemde 266 kontrat.
  - Gün içinde iki bacak birlikte düştü: straddle açılışta ~756 (IV ~%17), kapanışta 510 (~%11). Bu bir vol satış akışı.
  - 23.10 ve 26.10 kapanışlarında straddle 1.006 ve 924'tü (IV %21 / %20).
- **Hüküm:** ≤800 puan 27.10'da gün boyu işlenebilir bir seviyeydi; call bacağı derin, put bacağı sığ. 28.10 ekranı da benzer: P14500 186, P14750 satış 297. Ama kanatlarda kotasyonlar dağınık (P14250 satış 355 / son 112; C16000 23/100) [6]. Yani birkaç anlık fiyat değil, ama derinlik sınırlı.

Makasın beklenen değere etkisi [H] (puan; vadeye kadar tutulursa nakdi uzlaşma, çıkış makası yok):

| Orta fiyat / yarım makas | RV %17 | RV %24 | RV %27 |
|---|---|---|---|
| 800 / %2,5–7,5 | −36 / −76 | +282 / +242 | +418 / +378 |
| 1.100 / %2,5–7,5 | −343 / −398 | −26 / −81 | +111 / +56 |

**Sonuç:** Fikir ancak ≤800 seviyesinde, makas dahil, anlamlı. Uzlaşma seviyesinde (~1.100) beklenen değer negatif.

## C. Kendi fikirlerimin revizyonu
- **F1, straddle:**
  - Giriş eşiği ≤800 puan, makas dahil (limit fiyat).
  - Önce her bacaktan 1 lotla derinlik testi; put bacağı yoksa P14750 kullan (27.10'da 400 kontrat).
  - Boyut %0,8'den **%0,4**'e (10 mn TL'ye 5 straddle).
  - **Güven 6'dan 5'e.**
- **F2, call spread 14.500/15.500:** Rolü artık birleşik rally short'un sıkışma sigortası. Yön kanıtı zayıf (ENDEKS'in benzerleri). 14 spread, %0,48. **Güven 4/10.**
- **Kendi hatam:** 1. turdaki "yerel zirve 11.09" yanlıştı; doğrusu 9.09.

## D. Nihai komite portföyü (10 mn TL; % sermaye) [H, `r2_portfolio.py`]

Varsayımlar: pozisyonlar planlanan girişte açık; şok giriş fiyatından anlık; stop çalışmıyor; opsiyonlar şoktan sonra IV %32 / %24 / %35 ile yeniden fiyatlandı.

| Pozisyon | Stop riski | (i) BIST −%8, USD +%5 | (ii) BIST +%8 | (iii) USD +%12, BIST −%15 |
|---|---|---|---|---|
| MAKRO: kısa F_USDTRY1226 ×35 (52,47; stop 53,20) | 0,25 | −0,92 | 0,00 | −2,20 |
| Rally short F_XU0301226 ×13 (ENDEKS+ŞEYTAN; 14.875/15.050; gün içi stop 15.550) | 0,77 | +1,56 | −1,56 | +2,92 |
| HİSSE: GARAN/YKBNK Kasım ×135/420 (−%4 stop) | 0,70 | −0,12 | −0,02 | +0,04 |
| OPSİYON: straddle 14.500 ×5 @≤800 (koşullu) | 0,40 | +0,38 | +0,36 | +0,69 |
| OPSİYON: call spread 14.500/15.500 ×14 @≤340 | 0,48 | −0,23 | +0,44 | −0,37 |
| **Toplam** | **2,60** | **+0,66** | **−0,78** | **+1,07** |
| **Toplam, rally short dolmadıysa** | 1,83 | −0,89 | +0,77 | **−1,84** |
| (Opsiyonel) +C56000 USDTRY ×35 @420 | +0,15 | +0,21 | −0,04 | +1,02 |
| (İdiosenkratik) YKBNK tavan +%10 | — | −1,52 | −1,52 | −1,52 |

- **Limitlere uyum:** Fikir başı ≤%1 ✓. Toplam stop riski %2,6 ≤ %4 ✓. En kötü ortak stres −%1,84 (+ idiosenkratik −%1,5 ile −%3,4) ≤ %7 ✓. Tek kova (ENDEKS+ŞEYTAN) %0,77 ✓.
- **Teminat:** Takasbank ≈ %10,3; aracı kurum 1,5× ile %15,5 ≤ %20 ✓. 2.11 PSR artışına karşı tampon var.
- **Dışarıda kalanlar:** ENDEKS-2 ve HİSSE-2 (HAYIR). MAKRO-2, 20.11'e kadar 4 kapısı da açılırsa yalnızca +14 call spread olarak eklenir.
- **En büyük açık risk:** Senaryo (iii)'te rally short dolmamışsa kayıp MAKRO bacağında yoğunlaşıyor. C56000 dolarsa bu −%0,8'e iner.

## Kaynaklar
1. Yahoo günlük veri (XU030/XU100/GARAN/YKBNK/SAHOL/AKBNK .IS, TRY=X): https://query1.finance.yahoo.com/v8/finance/chart/GARAN.IS?range=2y&interval=1d
2. Borsa İstanbul VİOP bülteni 27.10: https://www.borsaistanbul.com/data/vadeli/viop_20261027.csv
5. Takasbank GM 2174: https://www.isyatirim.com.tr/tr-tr/Resmi-Duyurular/Documents/GenelMektup2174.pdf
6. Foreks ekranları 28.10: https://www.foreks.com/sembol-detay/H961658/o-xu030e1226p1475000/xu030-31-ara-26-satim-opsiyonu/ · https://www.foreks.com/sembol-detay/H967062/o-xu030e1226p1425000/xu030-31-ara-26-satim-opsiyonu/
11. Endeks vadeli ±%10: https://www.borsaistanbul.com/files/20221215-13341_viopta-bist-surdur.25-endeksi-vis-isl-acilmasi.pdf
12. Fed 16.09.2026: https://admiralmarkets.com/analytics/traders-blog/fed-raised-interest-rates
13. SPK kredili işlem esnekliği 30.10'a kadar: https://www.dunya.com/ekonomi/spkdan-kredili-islemler-icin-yeni-karar-sure-30-ekime-uzatildi-haberi-842452
