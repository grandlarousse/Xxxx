# v_YA1_a — Bağımsız doğrulama: Fiyat limiti (tavan/taban) ve temettü ex-günü etkileri (iddia YA1, kaynak ry_akis bulgu 1–6)

**Doğrulayıcı:** v_YA1_a (1. aşama: bağımsız yeniden üretim + zamanlama/dolum) · **Veri sonu:** 30.10.2026
**Kod:** `out/code_v_YA1_a/` (v0…v8; ll.py ve kaynak kod import EDİLMEDİ) · **Loglar:** `log_v1..v8.txt`, `res_v2_bt.csv`, `res_v2_byyear.csv`

## 0. Karar özeti

| Alt iddia | Kaynak | Bağımsız sonuç | Karar |
|---|---|---|---|
| (a) Tavan kapanışı → ertesi açılış gap | +282 bps (t 44), işlenemez | **+288 (t 44,7)** kaynağın 177 hissesinde; 217 hissede +298 (t 50). P(t+1 tavan \| tavan)=0,26. **Vadeli de kilitli:** vadeli verisi olan TC günlerinin **%80'inde** vadeli de tavanda kapanıyor. Kilitli olmayan %20'de vadeli t kapanışında alınırsa t+1 açılışına yalnız +25 bps (aynı olaylarda spot gap +99): vadeli bilgiyi zaten büyük ölçüde fiyatlıyor. t+1 kapanışına 15 bps+tik sonrası ≈0 | **KABUL** (olgu ve işlenemezlik) |
| (b) Tavan ertesi gün-içi fade, VİOP47 @15 | +66 (t 3,2); IS +52 / OOS +80 | Spot açılış fiyatıyla +57 (t 2,5). Vadelinin gerçekten listelendiği olaylarda +65 (t 2,6). Tik maliyeti eklenince +42 (t 1,75). **Gerçek VİOP vadeli açılışından SAT → vadeli kapanışı: −4 bps @15+tik (t 0,15).** Brif IS'i (2020): −25. IS 2020–22: t 1,1. Yalnız 10:30 TSİ girişi (2023-11+, n=157, vadelinin spotu izlediği varsayımıyla) +84 @15+tik (t 2,5) | **DÜZELT** → DÜŞÜK |
| (c) Tavana dokunup altında kapanma → fade | Tüm evren +59 (t 6,4); VİOP47 +59 (t 3,0) | Tüm evren, sıkı dokunma: +43 (t 4,3). **VİOP47 sıkı dokunma: +13 (t 0,95). Vadelinin listeli olduğu günlerde: −2.** Vadeli fiyatıyla: −11 @15+tik. Kaynağın VİOP47 sonucu iki şeyden geliyor: tavana DOKUNMAYAN günler ve vadelinin henüz olmadığı olaylar | **RED** (VİOP47) / DÜZELT (spot, tüm evren) |
| (d) Taban sonrası sürüklenme | gap −388, t+2..5 −510; dolabilir +209 (t 4,6); VİOP47 +144 (t 2,1) | Olgular aynı (−435 / −515). Dolabilir versiyon: kaynağın 177 hissesinde gün-ağırlıklı +199 (t 4,1) ✓. 217 hissede +146 (t 3,35). **İşlem başı ortalama ise yalnız +31 (tüm) ve −2 (VİOP47).** Vadeli-listeli VİOP evreninde gün-ağırlıklı +94 (t 1,46), işlem başı −8 | **DÜZELT** → DÜŞÜK |
| Temettü ex-günü | açılış +92, gün-içi −61 (t −7,5); VİOP47 @15 +29, OOS +65 | 2014+: açılış +106, gün-içi **−82 (t −8,7)**. Kaynak 2010–13'ün bozuk açılış verisini kullanmış (o=c, %98,6), bu da IS'i aşağı çekmiş. VİOP47 @15 2014–26: +43 (t 4,4); IS 2014–20 +21 (t 1,9); OOS +67 (t 4,0). **Ama vadeli açılış→kapanış: brüt +6, @15+tik −16 (t −0,2).** 10:30 girişi (2023-11+): +21,5 @15+tik (t 1,7). Fade'in ~%55'i ilk 30 dakikada (spot açılış seansı fazla yüksek) | **DÜZELT** → DÜŞÜK (VİOP ile) |

**Genel karar: DÜZELT.**
- Olgular (a, d-olgu, temettü açılış primi) sağlam.
- VİOP pay vadelisiyle işlenebilirlik iddiaları (b, c, d-VİOP, temettü-VİOP) gerçek vadeli fiyatlarıyla büyük ölçüde çöküyor.

---

## 1. Yöntem (bağımsız)

**Panel** (`v0_panel.py`): 217 BIST hissesi (kaynakta 177).
- İndeks: ldate.
- Bayat gün (v==0 VE h==l) atıldı. v==0 ama h≠l olan günler korundu (SASA).
- Açılış [l,h] dışındaysa NaN.
- Kurumsal işlem eşiği rejime bağlı: 2020-03-13 öncesi |R−1|>%20,5, sonrası >%10,5 → sınıflanmaz.
- Önceki satır bir önceki BIST işlem günü değilse olay sınıflanmaz. Yahoo'da 2020-03-11 147 hissenin 131'inde eksik; 03-12 getirisi aslında 2 günlük.
- Bölünmesiz fiyat meta/splits'ten. Meta eksik (ör. HEKTS 2015) olduğu için tik toleransı en çok %0,75 ile sınırlandı.

**Olaylar** (`v1_events.py`):
- Baz: b = c_{t−1}·f_{t−1}/f_t (f=adj/c), R = c/b.
- **TC (tavan kapanış):** R ≥ 1,10 − tol, tol = min(tik_rel+0,001, 0,0075), ve c≈h. Alternatifler: TC_B (kaynak gibi R≥1,0925, c≥0,999h) ve TC_S (katı). Sonuçlar ±%5 içinde aynı.
- **TU (sıkı dokunma):** gün yükseği tavanda (Rh ≥ 1,10 − tol), kapanış R < 1,09.
- **BC/BCL** simetrik.
- Kontroller: UP6/DN6.

**Backtest** (`v2_bt.py`):
- Raporlanan iki ortalama:
  - (i) **işlem başı** ortalama, tarih-kümelemeli t;
  - (ii) **gün-ağırlıklı** ortalama: aynı gün olaylarının eşit ağırlıklı ortalaması, Newey-West(5). Kaynak bunu kullanıyor.
- Maliyet: 8/15/30 bps + 1 tik (0,01 TL / fiyat; VİOP pay vadelisi tik = 0,01 TL). BC hedge'i için +4 bps.
- Dönemler: brif IS 2020-03..12 / OOS 2021–26; kaynak IS 2020–22 / OOS 2023–26; P20 rejimi (±%20, 2015-12..2020-03) ayrıca.

**Dolum gerçekçiliği:**
- `v4_viop.py`: VİOP bülteni (data/viop_panel.parquet, SSF). Ön vade = vadesi olay gününden sonra olan en yakın vade. Vadeli limit = prev_settle·(1±0,10). Kilit = kapanış limitte.
- `v5_h1.py`: 10:30 TSİ girişi = saatlik 06:30 UTC barının kapanışı (2023-11-30+). Günlük açılışla h1 ilk bar açılışı eşleşmeli (|fark| < %0,2). Ayrıca m5 ilk 30 dk VWAP (son ~60 gün).
- `v6_fut_vs_spot.py`: aynı olaylarda vadeli ve spot girişlerinin karşılaştırması.
- `v8_tradable_universe.py`: zaman-tutarlı VİOP evreni (olay günü vadeli bültende listeli mi?).

---

## 2. Kanıt

### 2.1 (a) Tavan → ertesi gap (P10, 2020-03-13+)

| Küme | n | gap_{t+1} | gün-içi_{t+1} | t+2..5 (XU100'e göre) | P(gap>0) | P(t+1 tavan) |
|---|---|---|---|---|---|---|
| TC, kaynağın 177 hissesi | 5.111 | +288 (t 44,7) | −71 (t −7,0) | +63 | 0,84 | 0,26 |
| TC, 217 hisse | 6.904 | +298 (t 50) | −66 | +99 | 0,84 | 0,28 |
| TC, VİOP47 | 698 | +232 (t 19,9) | −72 | +30 | 0,84 | 0,16 |
| TCL kilitli (177) | 380 | +772 | −182 | — | 0,93 | 0,69 |
| P20 (±%20) TC | 264 | +565 | −41 | — | 0,88 | 0,19 |

**VİOP vadeli kontrolü (v4):**
- TC günlerinin %24'ünde ön vade yok. Nedeni: vadeli o tarihte listelenmemişti (BRSAN 2024-04, CIMSA/DOAS 2024-02, ASTOR 2023-07, AKSEN/ALARK 2022-11, HEKTS/ODAS/AEFES 2021-04).
- Kapsananların **%79,8'inde vadeli de tavanda kapanıyor.** Kilitli kalanlarda uzlaşma → t+1 açılış +167 bps (alınamaz).
- Kilitli olmayan 107 olay: vadeli t kapanışı → t+1 açılış +25 bps (t 2,2). Aynı olayların spot gap'i +99.
- Aynı 107 olay, t kapanışı → t+1 kapanış: +19 brüt, 15 bps+tik ile +0,7.
- **Sonuç: işlenemez.**

### 2.2 (b) Tavan ertesi gün-içi fade

**VİOP47, spot açılış girişi, işlem başı bps (t_cl):**

| Dönem | 0 | 8 | 15 | 30 | 15+tik | 30+tik |
|---|---|---|---|---|---|---|
| Tümü 2020-03..2026-10 (n=697) | 72 (3,2) | 64 | **57 (2,5)** | 42 (1,85) | 42 (1,75) | 27 (1,1) |
| Brif IS 2020 (n=110) | −10 | — | **−25 (−0,4)** | — | −70 | — |
| Brif OOS 2021–26 | 88 (3,8) | 80 | 73 (3,2) | 58 | 62 (2,7) | 47 |
| IS 2020–22 | 67 (1,55) | — | 52 (1,1) | — | 24 (0,2) | — |
| OOS 2023–26 | 78 (3,1) | — | 63 (2,6) | — | 59 (2,4) | 44 |

**Yıllar (@15):** 2020 −25 · 2021 +180 · 2022 +43 · 2023 +28 · 2024 +110 · 2025 +5 · 2026 +162. Yıllar istikrarsız; 2021, 2024 ve 2026 baskın.

**Piyasa gün-içi sürüklenmesi:**
- Her gün her VİOP47 hissesini açılışta SAT / kapanışta AL stratejisi koşulsuz olarak +9,8 bps/gün (t 2,5); 2023–26'da +17,9.
- XU100 gün-içi düşülünce: +29 @19 (t 1,8).
- Hissenin koşulsuz gün-içi ortalaması düşülünce: +45 @15 (t 2,0).

**Hisse dağılımı:**
- 47 hissenin 35'inde ortalama pozitif. Tek hisse dışarıda bırakılınca ortalama +53..+72 arasında kalıyor.
- SASA 52 olayda −124 bps (3 TL fiyat → 1 tik ≈ 30 bps).

**Gerçek vadeli fiyatı (v4/v8):**
- t+1 vadeli açılışından SAT, vadeli kapanışında kapat: brüt +19 (t 1,0), @15 +4, **@15+tik −4 (t 0,15)**, n=527.
- Dönemler (@15+tik): 2021–26 +9 (t 0,9); 2023–26 +33 (t 0,8).
- Vadeli açılışı (ilk işlem ~09:30, spot açılış seansından önce) spot açılışa göre medyan **−59 bps aşağıda**. Spot açılış fiyatı vadeliye göre şişkin.
- Vadeli tarafta limit sorunu yok: t+1 vadeli tavandan açılış oranı %0,1; işlem görme oranı %99,8; medyan ön vade işlem tutarı ~578 mn TL.

**10:30 girişi (h1, 2023-11-30+):**
- VİOP47 (n=162): açılış→10:30 +9 (t 0,9); 10:30→kapanış **+101 brüt (t 3,2)**; @15+tik +82 (t 2,5).
- Aynı 154 olayda vadeli açılış→kapanış yalnız +52 brüt (t 1,0).
- Yorum: Gerçek fade 10:30'dan sonra oluyor; vadeli 09:30'da henüz düşük fiyatlıyor. Vadeli 10:00'dan sonra spotu izliyorsa (baz sabitse) VİOP'ta **10:30'da SAT** stratejisi 2023-11+ döneminde +84 @15+tik (t 2,5), @30+tik +69 (t 2,0), n=157.
- Sınır: Vadeli gün-içi verisi yok. Bu tahmin bir varsayıma dayanıyor ve yalnız güçlü OOS dönemini kapsıyor. Aynı dönemde koşulsuz 10:30→kapanış short VİOP47'de +18 bps/gün (t 3,8).

### 2.3 (c) Tavana dokunup geri dönen

| Tanım (t+1 açılış SAT → kapanış, @15) | VİOP47 | 217 hisse |
|---|---|---|
| Sıkı dokunma (benim TU) | +13 (t 0,95) | +43 (t 4,3) |
| Kaynak tanımı (h ≥ 1,0925; R < 1,0825) | +44 (t 3,0) | +50 (t 5,9) |
| **YAKIN: 1,0925 ≤ h < tavan (tavana DOKUNMADI)** | **+88 (t 3,0)** | +53 (t 4,2) |
| Plasebo: h ∈ [%7, %9,25), kapanış h'nin ≥1 puan altında | −3 | +20 (t 4,7); koşulsuz fazlası +7 |

- Kaynak tanımı, yüksek fiyatlı hisselerde tavanın %0,3–0,75 altında kalan günleri de "dokundu" sayıyor. Rh histogramı: 1,098–1,100'de yığılma var, altı düz arka plan.
- VİOP47 sıkı TU: vadelinin o gün listeli olduğu olaylarda −2 @15 (n=275); listelenmeden önceki olaylarda +60 (n=90).
- Vadeli fiyatıyla: −11 @15+tik (t −0,65). 10:30 girişi: +28 @15+tik (t 1,0).
- Tüm evrende etki limite özgü değil: yakın-tavan günlerde de aynı büyüklükte. Genel "yüksekten gün-içi dönüş" geri dönüşü. Spotta açığa satış gerektiriyor.

### 2.4 (d) Taban sonrası sürüklenme

| | 177 | 217 | VİOP47 |
|---|---|---|---|
| BC gap_{t+1} | −435 (t −30) | −494 | −317 |
| t+2..5, XU100'e göre | −515 (t −12,7) | −708 | −196 |
| Dolum-uygun short @19 (15 + 4 hedge), **gün-ağırlıklı** | **+199 (t 4,1)** | +146 (t 3,35) | +127 (t 1,85) |
| Aynısı, **işlem başı** | +60 | **+31** | **−2** |
| Vadeli-listeli VİOP evreni (gün / işlem) | — | — | +94 (t 1,46) / −8 |

**Gün-ağırlıklı ile işlem başı arasındaki fark:**
- Kalabalık çöküş günlerinde (aynı gün ≥5 taban) short kaybediyor. VİOP47 işlem başı −52; 217 hissede −43.
- Tekil taban günlerinde kazanıyor. VİOP47 +215 (n=62, t 1,7); 217 hissede +145 (t 3,3).

**Dönem ve yıllar:**
- 217 hisse, işlem başı: IS 2020–22 −53 / OOS 2023–26 +88. Brif IS (2020): −105.
- VİOP47 yıllar (işlem başı): 2021 −196 · 2022 +239 · 2023 +118 · 2025 −39 · 2026 −68.

**Vadeli tarafı:**
- Taban günü t'de vadeli de %84 kilitli.
- t+1 dolum-uygun günlerde vadeli yalnız %2,7 kilitli: vadelide short açılabiliyor.
- Vadeli t+1 kapanışında SAT → t+5, XU100 hedge, 19 bps+tik: işlem başı +23, gün-ağırlıklı +146 (t 2,3), n=264.
- Hedgesiz: −28 / +63.
- Zamanlama notu: "t+1 taban değil" koşulu spot kapanış seansının sonucunu kullanıyor. Vadeli 18:15'e kadar açık olduğu için vadeliyle ileri bakış yok.

### 2.5 Temettü ex-günü (`v7_div.py`)

- Olay tespiti: Yahoo adj/c sıçraması, %0,3 < verim < %25.
- **Tarih doğruluğu:** ham fiyat değişiminin log(1−dy)'ye eğimi t günü 0,93; t±1 günlerinde ≈0. Yahoo ex-tarihi doğru.
- **2010–13:** gün-içi = 0 olan olay oranı %98,6 (açılış bozuk). Kaynağın IS'ine (2010–20) dahil.

| | n | gap0 (açılış − teorik ex) | gün-içi |
|---|---|---|---|
| Tümü 2014+ | 1.052 | **+106 (t 15,9)** | **−82 (t −8,7)** |
| VİOP47 2014+ | 429 | +101 | −58 (t −5,5) |
| IS 2014–20 | 539 | +120 | −58 |
| OOS 2021–26 | 513 | +91 | −108 |

**Backtest: ex-gün spot açılışında SAT → kapanış (VİOP47):**

| Dönem | @15 | @15+tik | @30 |
|---|---|---|---|
| 2014–26 | +43 (t 4,4) | +23 (t 2,9) | +28 |
| IS 2014–20 | +21 (t 1,9) | −12,5 | — |
| OOS 2021–26 | +67 (t 4,0) | +60 | — |

Yıllar (@15): 2014 −7 · 2016 −17 · 2019 −28 · 2021 −28; 2018 ve 2022–26 güçlü.

**VİOP vadeli:**
- Ex-günde vadeli fiyatı düzeltilmiyor (prev_settle/önceki uzlaşma medyan 1,000). Vadeli temettüyü baştan fiyatlıyor.
- **Vadeli açılış→kapanış SAT: brüt +6 (t 1,2), @15+tik −16 (t −0,2), n=265.** Aynı olaylarda spot +70.

**10:30 girişi (2023-11+, VİOP47, n=100):**
- Açılış→10:30 +48 (t 4,6); 10:30→kapanış +38 (t 2,6); @15+tik +21,5 (t 1,7).
- Etki ağırlıkla spot açılış seansının teorik fiyatın üstünde oluşmasından geliyor. Vadeliyle açılıştan yakalanamıyor.

---

## 3. Sorunlar ve karşı argümanlar

1. **Açılış fiyatı = vadeli dolumu varsayımı yanlış.** VİOP pay vadelisi 09:30'da, spot açılış seansından (09:55) önce işlem görüyor.
   - TC sonrası spot açılış vadeliye göre ~60 bps şişkin; ex-gününde de benzer.
   - "Açılışta sat" stratejisinin VİOP versiyonu gerçek vadeli fiyatlarıyla sıfır ya da negatif.
2. **Hayatta kalan / ileri bakışlı evren.** Bugünkü 47'lik VİOP listesi 2020'ye geri taşınmış.
   - TC olaylarının %21'i ve TU olaylarının %25'i vadeli henüz yokken gerçekleşmiş.
   - TU'nun VİOP47 sonucu tamamen bu olaylardan geliyor.
3. **Tanım gevşekliği (c).** "Dokundu" eşiği (Rh ≥ 1,0925) gerçek tavana dokunmayan günleri içeriyor. VİOP47 sonucunun çoğu bunlardan.
4. **Gün-ağırlıklı ortalama (d).** Kaynak olay günlerini eşit ağırlıklandırıyor. Bu, kalabalık çöküş günlerindeki kayıpları seyreltiyor. İşlem başı ortalama ≈0 (VİOP47) ve +31 (tüm).
5. **Temettü IS'i.** 2010–13'ün bozuk açılışı kaynağın IS'ini aşağı çekmiş (+8 → doğru IS 2014–20 +21). Bu, kaynak aleyhine bir hata. Ama OOS'un VİOP versiyonu yine çalışmıyor.
6. **Piyasa gün-içi sürüklenmesi.** 2021+ döneminde koşulsuz gün-içi short +11..+18 bps/gün (t 2,6–3,8). Fade'lerin bir kısmı bu genel BIST "gece +, gün-içi −" yapısı.
7. **Brif IS'i (2020-03..12) her fade'de zayıf ya da negatif.**
   - P20 (±%20) rejiminde TC fade 217 hissede +26 (t 1,2); VİOP47'de n=17.
   - Etkinin varlığı 2021+ rejimine bağlı.
8. **Tik.** VİOP tik'i 0,01 TL. Düşük fiyatlı hisselerde (SASA ~3 TL → 30 bps/tik; VİOP TC olaylarının %7'si 5 TL altında) maliyet 15 bps varsayımını aşıyor. VİOP47 TC fade tik ile +57 → +42 (t 1,75).
9. **Ölçülemeyen:** vadeli gün-içi fiyatı (10:30 vadeli girişi spot vekiliyle varsayıldı), açığa satış yasağı ve yukarı adım kuralı (spot), kapanış seansında alım kuyruğu sırası.

## 4. Düzeltilmiş iddia (önerilen metin)

**(a) Tavan kapanışı (±%10, 2020-03+, 177–217 hisse) → ertesi açılış +288..+298 bps (t ≈45–50).**
- Spotta ve vadelide işlenemez: vadeli de günlerin %80'inde kilitli.
- Kilitli olmayan günlerde vadeli bilgiyi zaten fiyatlıyor: t kapanışı → t+1 açılış +25 bps; t+1 kapanışına net ≈0.
- **YÜKSEK (olgu) / işlenemez.**

**(b) Tavan ertesi gün-içi fade.**
- Spot açılış fiyatıyla VİOP47 @15: +57 (t 2,5); tikle +42 (t 1,75); brif IS'i (2020) negatif.
- **Gerçek VİOP vadeli açılışından girişle @15+tik ≈ −4 (t 0,2): açılışta VİOP'ta işlenemez.**
- 10:30 TSİ girişi (vadelinin spotu izlediği varsayımıyla, yalnız 2023-11+, n=157): +84 @15+tik (t 2,5).
- **DÜŞÜK.** Uzun dönem vadeli gün-içi verisiyle doğrulanmalı.

**(c) Tavana sıkı dokunup dönme.**
- VİOP47: +13 @15 (t 0,95); vadeli listeliyken −2; vadeli fiyatıyla −11.
- **RED (VİOP47).** Tüm evren spot +43 (t 4,3) ama limite özgü değil: yakın-tavan günlerde de aynı.
- **DÜŞÜK** (spot, açığa satış kısıtlı).

**(d) Taban sonrası gap −435 / t+2..5 −515 sürüklenmesi olgu olarak sağlam.**
- Dolabilir short, gün-ağırlıklı: +146..+199 (tüm evren, t 3,4–4,1). İşlem başı yalnız +31 (tüm) ve −2 (VİOP47).
- VİOP47 (zaman-tutarlı) gün-ağırlıklı +94 (t 1,5).
- Kalabalık çöküş günlerinde ters dönüyor.
- **DÜŞÜK** (VİOP47) / **DÜŞÜK–ORTA** (spot evren).

**Temettü ex-günü (2014+).**
- Açılış teorik ex fiyatın +106 bps üstünde; gün-içi −82 (t −8,7).
- VİOP47 spot @15: +43 (t 4,4); IS 2014–20 +21 / OOS +67.
- **Vadeli açılışından girişle −16 @15+tik.** 10:30 girişiyle +21,5 (t 1,7).
- **ORTA (olgu) / DÜŞÜK (VİOP işlenebilirliği).**

## 5. TradingView
- Spot: `BIST:<KOD>`
- Pay vadelisi sürekli kontrat: `BIST:<KOD>1!` (ör. `BIST:THYAO1!`, `BIST:SASA1!`)
- Hedge: `BIST:XU030D1!`
- Endeks: `BIST:XU100`
