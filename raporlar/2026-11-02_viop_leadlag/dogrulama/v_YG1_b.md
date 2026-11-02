# v_YG1_b — 2. aşama çürütme: YG1 (47 hissede açılış gap fade, CIMSA/OYAKC, hisseye özgü hedge'li fade)
Tarih: 02.11.2026 · Kod: `out/code_v_YG1_b/` (vb.py ortak; v1…v14; çıktılar `res/*_log.txt`, `res/*.csv`).
Bağımsızlık: ll.py ve v_YG1_a/vc.py import EDİLMEDİ; temizlik `vb.py`'de yeniden yazıldı.
Temizlik: bayat gün (v=0 ve h=l) atıldı; rejime bağlı eşik ±%20,5 (2020-03-13 öncesi) / ±%10,5 (sonrası), adj cc, adj gap ve ham açılış için; ardışık BIST günü şartı.
Çalıştırma: `cd out/code_v_YG1_b && nice -n 10 python3 -c "import vb,pandas as pd; pd.to_pickle(vb.panel(),'res/panel.pkl')"`, sonra v1 → v14 (v3 `res/basket.pkl`, v7 `res/h1.pkl` üretir).

## 0. Hüküm: DÜZELT — güven DÜŞÜK (iddia yazıldığı haliyle). Gerçek ama dar bir bileşen var.

Etkinin varlığı çürütülemedi. Tarih karıştırma, rastgele çift ve hisse jackknife plasebolarının hepsini geçiyor. Ama iddianın dört ana parçası yanlış ya da yanıltıcı:

1. **"47 hissede sistematik" değil.**
   - Ham portföy kârı birkaç büyük gün ve birkaç hisseden geliyor. OOS'ta medyan işlem 0,0 bps; işlemlerin %50'si pozitif. En iyi 10 gün atılınca 9,7 bps (t 1,7); en iyi 3 hisse (BRSAN, CIMSA, OYAKC) atılınca 11,6 (t 1,9).
   - |gap| %1–2 aralığındaki gap'lerde OOS dönüş yok: yukarı gap'lerde işlem-ağırlıklı (TW) −3 ile −5 bps. Etki yalnız |gap|>%3'te.
   - "%87 pozitif" oranının null'u (dairesel kaydırma) %58, yani %50 değil. BIST'in gün-içi düşüş eğilimi short ağırlıklı sinyali şişiriyor.
2. **"XU030 vadelisiyle hedge'li OOS 24,2 (t 4,2)" ölçüm hatasıyla şişmiş.** Yahoo XU030 açılışı 2014, 2015, 2021 ve 2022'de bileşenlerle tutarsız (§2). Kendini hariç tutan bileşen sepetiyle hedge edilince:
   - hisseye özgü fade OOS 18,5 (t 3,0) gün-ağırlıklı (DW) ve 22,6 (t 4,0) işlem-ağırlıklı (TW);
   - IS 24,4 (iddia 42,6, t 10,7).
3. **"İlk 30 dk VWAP girişi sadece −3 bps" bir iptal artefaktı.** Yukarı bacak +9 ve aşağı bacak −11 bps birbirini götürüyor. Kârlı bileşen olan hisseye özgü yukarı gap'te VWAP-30 vekili açılışa göre 21 bps kaybettiriyor (50 → 29). m5'te kaybın 25 bps'i ilk 5 dakikada.
4. **Dönüş açılış müzayedesi fiyatına bağlı.** Gap 10:30 fiyatıyla ölçülünce (müzayede baskısı sinyalden çıkınca) 10:30→kapanış fade'i yok:
   - hisseye özgü yukarı: 5,1 (t 1,2);
   - hisseye özgü her iki yön: 1,2;
   - ham her iki yön: −3,5.

   IS'te ham fade'in tamamı, açılış fiyatının günün ucu olduğu (sürekli işlemde o fiyattan hiç işlem olmayan) günlerin null'a göre fazlalığıyla açıklanıyor. Kalan kısım −0,3 bps. Bu, müzayede fiyat baskısının geri dönüşü. Ancak müzayedeye katılarak (spot) yakalanabilir; SSF ile değil.

**Ayakta kalan bileşen: hisseye özgü YUKARI gap → short + sepet hedge.**
- OOS 36,7 DW (t 5,1) / 30,7 TW (t 4,4).
- 72 spesifikasyonluk max-t düzeltmesinden sonra p<0,005; en iyi 10 hisse çıkınca 24,8 (t 3,0); yerel ±20 günlük taban çıkarılınca 37,1 (t 5,1).
- Fakat gerçekçi girişle maliyetten sonra ≈0: VWAP-30 + 15 + tik + 3 bps hedge ile DW 5,7 (t 0,6), TW −3,9.

## 1. Başlık rakamları — tekrar

| İddia | İddia rakamı | v_YG1_b | Not |
|---|---|---|---|
| Hisse medyanı OOS, %pozitif | 17,8, %87 | 17,3, %87 | Null (kaydırılmış sinyal): medyan 3,5, %58 (p95 %70). Sepet-hedge'li: medyan 6,5, %77 (null %51) |
| FDR | 10/47 | Tam dönem 8/47, yalnız OOS 0/47 (CIMSA p 0,0025 > 0,05/47) | ✘ |
| Portföy OOS | 16,5 (t 2,8) | DW 16,7 (t 2,77); TW 16,7 (gün kümelenmiş t **1,75**) | TW t zayıf |
| Portföy IS | 28,0 (t 7,0) | DW 22,1 (t 5,3); TW 10,8 (t 2,1) | 2014–17 TW −3,2 |
| İllikit / likit yarı | 26,9 / 3,1 | 27,0 / 2,1 | ✔ |
| VWAP-30 kaybı | −3 | Ham her iki yön 3,9; hisseye özgü yukarı **20,8** | ✘ yanıltıcı |
| Hisseye özgü hedge'li OOS | 24,2 (t 4,2) | XU030 ile 23,4 (t 3,9); **doğru sepetle 18,5 (t 3,0)** | ✘ şişkin |
| CIMSA / OYAKC OOS | 74 / 50 | 72,6 (t 3,1) / 51,2 (t 2,7) | ✔ rakam |
| CIMSA / OYAKC VWAP | 78 / 48 | h1 79 / 53. 2025-05+ dönemde 32 (t 1,2) / 36 (t 1,7) | Zayıflıyor |

## 2. Yeni bulgu: Yahoo XU030 açılışı bozuk yıllar (v2, v3)
- **Yöntem:** XU030 gap'ini, önceki 250 günün cirosuna göre en büyük 25 hissenin ciro ağırlıklı gap'iyle karşılaştırdım. Eğimler:
  - 2014: 0,21; 2015: 0,45; 2021: 0,61; 2022: 0,59;
  - diğer yıllar: 0,72–0,97.
- **Belirti:** Aynı yıllarda corr(Δgap, Δintra) −0,92 / −0,79 / −0,68 / −0,66. Gün-içi eğim ise 0,93–0,99. Bu, endeks açılışının gürültülü olduğunu gösteriyor: gürültü gap'e + olarak, intra'ya − olarak giriyor.
- **Sonuç:** Hedge ve hisseye özgü gap (gap − XU030 gap) bu yıllarda mekanik pozitif fade üretiyor.
  - O 4 yılda XU030 bazlı hisseye özgü fade DW 29,7 (t 5,8). Sepet bazlı karşılığı 1,3 (t 0,2).
  - Yıllara göre (XU030 → sepet): 2014 33 → −17; 2015 37 → 2; 2021 29 → 8; 2022 18 → 6.
- **Gerçekçi hedge:** XU030 vadelisi 10:00'da adil fiyattan işler, yani sepete yakındır. Yahoo XU030 açılışına dayanan bütün hedge ve hisseye özgü rakamlar (kaynak ve 1. aşama) bu yıllarda şişkin.

## 3. Ortak faktör (v1, v4)
- **Aynı gün XU030 gün-içine regresyon (OOS):**
  - portföy alfa 14,8 (t 2,6), beta −0,42 (net short);
  - yukarı bacak alfa 31,7 (t 5,3);
  - aşağı bacak alfa −10,0 (t −1,0).
- **Kesitsel arındırılmış gün-içi:** OOS 16,1 (t 3,6); yukarı 26,4, aşağı −5,3.
- **Rastgele çift** (j'nin gap'iyle i'nin gün-içi, 300 eşleme): OOS 0,3 (sd 2,9, en yüksek 8,6); hissenin kendi gap'iyle 16,7. Etki hisseye özgü; ortak faktör değil.

## 4. Plasebolar (v4, v5)
- **Tarih karıştırma** (hisse içi dairesel kaydırma, 500 tekrar):
  - ham, OOS: null 3,6 ± 2,4, gerçek 16,7 (p<0,002);
  - hisseye özgü yukarı: null 2,6 ± 3,7, gerçek 36,7.
- **Bayatlatılmış sinyal (ham, OOS):**
  - 1 gün gecikmeli (L1): −5,5 (t −1,0);
  - L2: 12,0 (t 2,1); L10: 11,3 (t 2,1). Bunlar gün-içi eğilimden.
- **Bayatlatılmış sinyal (hisseye özgü yukarı + sepet, OOS):**
  - L1: 9,7; L2: 16,9 (t 2,7); L10: 12,9 (t 2,3).
  - Kalıcı bir "gece yukarı / gün-içi aşağı" bileşeni var. Ama yerel ±20 günlük taban çıkarılınca aynı gün etkisi 37,1 (t 5,1).
- **Olay profili:** Hisseye özgü yukarı gap'ten bir gün önce gün-içi +88 bps (OOS). Yani dünkü sert gün-içi yükseliş, ardından bugün gap ve gün-içi dönüş (−31).

## 5. Alt dönemler (DW bps, t)

| | 2014–17 | 2018–20 | 2021–23 | 2024–26 |
|---|---|---|---|---|
| 47 ham her iki yön | 15,0 (2,9) | 31,2 (4,6) | 7,9 (0,95) | 26,4 (3,0) |
| 47 ham her iki yön, TW | −3,2 (−0,7) | 33,0 (2,9) | 15,2 (1,1) | 18,8 (1,6) |
| ham aşağı (long) | −2,7 | 11,7 | 1,9 | −38,5 (−2,5) |
| Hisseye özgü yukarı + sepet | 12,1 (1,5) | 41,9 (4,9) | 23,7 (2,4) | 51,8 (5,0) |
| Hisseye özgü her iki yön, XU030 hedge | 33,5 | 37,6 | 17,4 | 30,0 |
| Hisseye özgü her iki yön, sepet hedge | 15,9 (2,5) | 33,9 (5,1) | 8,3 (1,0) | 29,9 (3,3) |
| CIMSA | 19,6 (1,3) | 77,6 (3,2) | 59,7 (1,7) | 92,6 (3,3) |
| OYAKC | 20,3 (1,1) | 34,5 (1,0) | 49,6 (1,8) | 53,5 (2,3) |

## 6. Veri madenciliği (v10)
- **Spesifikasyon yüzeyi:** 72 spesifikasyon (eşik 0 / 0,5 / 1 / 1,5 / 2 / 3% × ham/hisseye özgü sinyal × her iki yön/yukarı/aşağı × hedge'siz/sepet hedge).
  - Etki eşikle düzgün ve monoton artıyor; %1 seçilmiş bir tepe değil.
  - 46/72 spesifikasyonda hem IS hem OOS t>2. Aşağı bacak hemen her eşikte OOS'ta ≈0 ya da negatif.
- **Null max-t:** Hisse içi dairesel kaydırma, 200 tekrar.
  - Bütün 72 spesifikasyon üzerinden: IS medyan 4,15 / p95 4,66; OOS 2,83 / 3,77. Eşiksiz short spesifikasyonları eğilim yüzünden null'da bile t≈4 alıyor.
  - Başlık spesifikasyonu (ham, iki yön, %1): OOS t 2,77. Aile düzeltmeli p: 72'lik ailede 0,56, yalnız 36 sepet-hedge'li ailede 0,12. **OOS tek başına çoklu test sonrası anlamlı değil**; IS'te p<0,005.
  - Hisseye özgü yukarı + sepet: OOS t 5,08, iki ailede de p<0,005.

## 7. Uç değer bağımlılığı (v5, v6)
**Ham iki yön, OOS:**
- medyan gün 6,3, medyan işlem 0,0, pozitif işlem %50;
- günlerin en iyi %1'i atılınca 8,2; en iyi %5'i atılınca −11,5;
- winsor %1–99 ile 16,0.

**Hisseye özgü yukarı:**
- medyan işlem 54, pozitif %57;
- en iyi 10 gün atılınca 29,0 (t 4,2); en iyi %5 gün atılınca 7,7.

**Tavan/taban yakını açılışlar** (limite 1 puandan yakın):
- OOS işlemlerin %1,5'i, TW kârın %17'si;
- bu işlemlerde ortalama 190 bps, %85'i pozitif;
- hariç tutulunca ham 14,9, hisseye özgü yukarı 35,9.

## 8. Mekanik / bid-ask ve dolum (v7, v8, v9, v14)
**h1 dönemi** (2023-12 → 2026-10), hisseye özgü yukarı + sepet:

| Giriş | DW (t) | TW (t) |
|---|---|---|
| E0 (açılış) → C | 50,2 (4,8) | 41,5 (4,0) |
| O → 10:30 | 29,3 (5,0) | 28,5 (5,1) |
| VWAP-30 vekili → C | 29,4 (3,3) | 20,1 (2,3) |
| 10:30 → C | 20,9 (2,4) | 13,0 (1,5) |
| Sinyal 10:30'da ölçülen gap, 10:30 → C | 5,1 (1,2) | 3,7 (0,9) |

2. yarıda (2025-05+) sinyal@10:30 sonucu 0,8.

**m5 (60 gün):** Hisseye özgü yukarıda O → 10:05 = 24,6 bps (t 2,2). Dönüş ilk 5 dakikada.

**Açılış = günün ucu** (short'ta O=H, long'da O=L) — null'a göre:
- IS ham: kalan −0,3 (null sd 1,9). IS etkisinin tamamı müzayede fiyatının uç kalmasından.
- OOS ham: 9,7 (sd 2,7).
- Hisseye özgü yukarı: IS 3,9 (anlamsız), OOS 25,3 (sd 3,7).

**SSF bülteni (2017-03+):**
- Sinyal günlerinde SSF işlem sayısı bol: medyan 5–18 bin işlem, 150–780 mn TL. Bağlayıcı kısıt hacim değil, fiyat.
- İşlemlerin %1,6–4'ünde SSF gün boyu spot açılış eşdeğerinin (O × baz) %0,5 yakınına bile gelmedi. Bu günlerde spot fade ortalaması 420–530 bps.
- Bu günler hariç tutulunca spot fade (OOS):
  - ham 14,2 → 7,4;
  - hisseye özgü yukarı 23,0 → 7,9 (illikitte 30,2 → 11,2).
- En iyi durum sınırı (gün tepesinden ya da O eşdeğerinden short): 18,3.
- Uyarı: bu bölmeler sonuca bağlı koşullama. Ancak kârın büyük kısmının SSF'nin hiç işlemediği fiyatlarda oluştuğunu gösteriyor.

## 9. CIMSA / OYAKC (v11)
**CIMSA:**
- IS t'sine göre 47 içinde 4. sırada, yani önceden seçilebilirdi. IS'in en iyi 5'i OOS'ta 37,9 (t 3,2) verdi; hisse düzeyinde kalıcılık var.
- Zayıf yanları:
  - sepet hedge'le IS 23,7 (t 1,65), OOS 46,8 (t 2,2);
  - OOS'ta en iyi 10 işlem atılınca 28,8 (t 1,4);
  - 2014–17'de medyan 0, işlemlerin %43'ü pozitif;
  - **L1 bayat sinyal OOS 46,4 (t 2,1)**, yani aynı güne özgü değil;
  - OOS'ta aşağı bacak 149 (t 3,6) > yukarı bacak 49 (portföyün tersi).
- h1: ilk yarı (n 39) 144 bps → 2. yarı 46 (t 1,5). Sinyal@10:30 6,8 (t 0,5).

**OYAKC:**
- IS t'sine göre 16. sırada; öne çıkması OOS'a dayanıyor, yani seçim yanlılığı.
- IS'te en iyi 5 işlem atılınca 8,7 (t 0,5); sepet hedge'le IS 19 (t 0,9).
- h1 2. yarı VWAP-30: 36 (t 1,7).

## 10. Maliyet sonrası (v12; gidiş-dönüş, 1 tik = 0,01 TL / 30.10.2026 fiyatı, hedge +3 bps)
DW (t) / TW (t):

| Strateji | Brüt | 8 + tik | 15 + tik |
|---|---|---|---|
| 47 ham, E0, OOS | 16,7 / 16,7 | 2,7 (0,4) / 2,7 | −4,3 / −4,3 |
| Hisseye özgü yukarı + sepet, E0, OOS | 36,7 / 30,7 | 19,6 (2,7) / 13,5 (2,0) | 12,6 (1,7) / 6,5 (0,9) |
| Hisseye özgü yukarı, h1, VWAP-30 | 29,4 / 20,1 | 12,7 (1,4) / 3,1 | 5,7 (0,6) / −3,9 |
| Hisseye özgü yukarı, h1, 10:30 | 20,9 / 13,0 | 4,1 / −4,0 | −2,9 / −11,0 |
| CIMSA, E0, OOS | 72,6 | 62,0 (2,6) | 55,0 (2,3) |
| CIMSA, VWAP-30, 2025-05+ | 32,4 | 21,9 (0,8) | 14,9 (0,6) |
| OYAKC, E0, OOS | 51,2 | 37,6 (2,0) | 30,6 (1,6) |
| OYAKC, VWAP-30, 2025-05+ | 35,7 | 22,1 (1,1) | 15,1 (0,7) |

## 11. Düzeltilmiş iddia
- **47 hissede gap fade:**
  - Brüt etki istatistiksel olarak var (IS DW 22, t 5,3; OOS 16,7, t 2,8).
  - Ama sistematik değil: medyan işlem 0; birkaç büyük gün ve birkaç hissede yoğun. OOS tek başına çoklu test sonrası anlamlı değil (p 0,12–0,56).
  - Kârın büyük kısmı açılış müzayedesi fiyatının günün ucunda kaldığı günlerden geliyor (IS'te tamamı). Bu fiyatlarda SSF hiç işlem görmemiş olabilir.
  - Maliyetten sonra ≈0 ya da negatif. Güven DÜŞÜK.
- **Hisseye özgü YUKARI gap short (kendini hariç tutan sepet / XU030 vadelisi hedge'li):**
  - Bütün plasebolardan, veri madenciliği düzeltmesinden ve uç değer testlerinden geçen tek bileşen: OOS 31–37 bps, t 4,4–5,1; 4 alt dönemin 3'ünde anlamlı.
  - Mekanizma: müzayede fiyat baskısı. Dönüşün %60'ı ilk 30 dakikada, büyük kısmı ilk 5 dakikada. Gap 10:30'da ölçülünce etki yok.
  - Gerçekçi SSF girişiyle (VWAP-30 ya da 10:30) ve 15 bps + tik + hedge maliyetiyle net ≈0. İlişki: ORTA–YÜKSEK. İşlenebilirlik: DÜŞÜK (yalnız spot açılış müzayedesine katılımla ve açığa satış imkânıyla).
- **XU030 hedge'li hisseye özgü fade (iddia 24,2, t 4,2):** Yahoo XU030 açılışı 2014, 2015, 2021 ve 2022'de bozuk. Doğru sepetle 18,5 (t 3,0); IS 24 (42,6 değil).
- **CIMSA:** ORTA–DÜŞÜK. Önceden seçilebilir ve IS/OOS pozitif. Ama hedge'le IS anlamsız, bayat sinyal de çalışıyor, uç değerlere bağımlı ve son dönemde gerçekçi girişle zayıf (t 0,6).
- **OYAKC:** DÜŞÜK. IS anlamsız ve seçim OOS'a dayanıyor.
- **Kimya ajanının bulgusu:** Aynı seri ve aynı sinyal; bağımsız teyit değil.

TradingView: BIST:CIMSA, BIST:OYAKC, BIST:CIMSA1!, BIST:OYAKC1!, BIST:XU030, BIST:XU0301!.
