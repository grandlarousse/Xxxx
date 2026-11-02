# v_YA1_b — Çürütme (2. aşama): fiyat limiti ve temettü ex-günü etkileri (iddia YA1)

**Doğrulayıcı:** v_YA1_b · **Veri sonu:** 30.10.2026
**Kod:** `out/code_v_YA1_b/` (b0…b7)
- ll.py, kaynak kod (code_y_akis) ve 1. aşama kodu (code_v_YA1_a) IMPORT EDİLMEDİ.
- Loglar: `log_b2.txt` (fade), `log_b3.txt` / `log_b3b.txt` (VİOP vadeli), `log_b4.txt` (temettü), `log_b5.txt` (taban), `log_b6.txt` (saatlik), `log_b7.txt` (olgular).

## 0. Karar özeti

**Genel hüküm: DÜZELT. Güven: DÜŞÜK.**
- Olgular sağlam: (a) tavan sonrası gap, taban sonrası gap ve sürüklenme, temettü açılış primi.
- İşlenebilirlik iddiaları büyük ölçüde çöküyor.
- 1. aşamanın bulmadığı yeni sorun: **kaynak (ve 1. aşama) short PnL'ini log getiriyle hesaplamış.** −log(c/o) ≥ 1−c/o olduğu için short getirisi ≈σ²/2 kadar şişiyor.
  - Gün-içi fade'de bu fark ~12–15 bps.
  - 4 günlük taban short'unda 50–70 bps; bu, (d)'nin "dolabilir" sonucunu tek başına siliyor.

| Alt iddia | Kaynak | Bu doğrulama (basit getiri, gerçek tik) | Hüküm |
|---|---|---|---|
| (a) Tavan → ertesi gap | +282 (t 44) | +301 bps (t 53, n 7.144, 217 hisse); VİOP47 +242. Olay günü t'de vadeli %83 tavanda kilitli | KABUL (olgu) / işlenemez |
| (b) Tavan ertesi gün-içi fade, VİOP47 @15 | +66 (t 3,2) | Spot açılışla +47 (t 2,1). +tik +39 (t 1,7). Piyasa-nötr +30 (t 1,6). 2020: −21. **Vadeli açılışından −21 @15+tik.** Vadeli VWAP girişi +41 @15+tik (t 2,6), piyasa-nötr +19 (t 1,6) | DÜZELT → DÜŞÜK |
| (c) Dokunup dönen fade | +59 (t 6,4); VİOP47 +59 | VİOP47 sıkı dokunma: brüt +22, plasebo p=0,15. Vadeli-listeli: brüt +8, p=0,53. Vadeliyle −28 @15+tik. Tüm evren spot: +34 @15 (t 3,6), limite özgü değil | RED (VİOP47) / DÜŞÜK (spot) |
| (d) Taban sürüklenmesi, dolabilir short | +209 (t 4,6); VİOP47 +144 | Olgu: gap −448, t+2..5 −554 (tüm olaylar). **Dolabilir short, basit getiri, @19: işlem başı −12 (t −0,3), gün-ağırlıklı +43 (t 1,0).** VİOP47: +10 / +134 (t 1,9). Vadeli-listeli: −2 / +87 (t 1,4). Vadeliyle +12 / +138; 2024–26 +23 (t 0,3) | RED (işlenebilirlik) / KABUL (olgu) |
| Temettü ex-günü | açılış +92; gün-içi −61; VİOP47 @15 +29 | Açılış +109 (eğim 0,15·verim + 53 bps sabit). Gün-içi −79. VİOP47 @15 +40 (t 3,5), +tik +28. 2014–17: −3. **Vadeli: açılış primi yok (+7 bps). open→close −29, VWAP→close −16 @15+tik** | DÜZELT: olgu ORTA / VİOP işlenebilirliği RED |

## 1. Yeni bulgu: log getiri yanlılığı

- Kaynak `a_limit.py` / `f_bt.py` / `f3_fill.py` ve 1. aşama `v1_events.py` / `v2_bt.py` short PnL'ini `-log(c/o)` veya log fazla getiri toplamıyla hesaplıyor.
- Short pozisyonun gerçek getirisi (notional başına) `1 − c/o`. Jensen eşitsizliği gereği log versiyonu her zaman daha büyük; fark ≈ var/2.

| Strateji | log brüt | basit brüt | fark |
|---|---|---|---|
| TC fade VİOP47, işlem başı | +74,4 | +62,1 | 12 |
| TC fade, tüm 217 | +60,8 | +44,6 | 16 |
| TU_src fade, tüm | +66,3 | +56,2 | 10 |
| BC dolabilir short, tüm 217, gün-ağırlıklı @19 | +110 | **+43** | 67 |
| BC dolabilir short, tüm 217, işlem başı | +39 | **−12** | 51 |
| Temettü VİOP47 | +58 | +55 | 3 |

Uzun pozisyonlu testlerde (BCL long) yanlılık ters yönde çalışır (bu iddianın konusu değil).

## 2. Testler ve sonuçlar

### 2.1 (b) Tavan ertesi fade, VİOP47 (P10; `log_b2.txt`, `log_b3.txt`, `log_b3b.txt`, `log_b6.txt`)

**Spot açılış girişi:**
- İşlem başı: brüt +62 (t 2,75); @15 +47 (t 2,1); @15+tik +39 (t 1,7); @30+tik +24.
- Tik maliyeti gerçek fiyat seviyesinden hesaplandı. Yahoo `c` bedelsizlerle geriye doğru düzeltilmiş (ör. SASA 2019'da gerçek fiyat ×50), bu yüzden vadeli uzlaşmasından gerçek fiyat kuruldu.

**Ortak faktör:**
- Aynı gün VİOP47 kesit ortalaması düşülünce @15: +30 (t 1,6). XU100-nötr: +25 (t 1,3).
- TC günleri piyasa ralli günlerine yığılıyor. Fade'in ~%40'ı piyasa geneli gün-içi geri dönüş.

**Alt dönemler (@15):**
- P20 rejimi (±%20): 2015-12..17 n=10, 2018..2020-03 n=8 (test edilemez).
- 2020-03..12: −21 (t −0,4). 2021–23: +50 (t 1,55). 2024–26: +92 (t 2,9).
- Yıllar: 2020 −3 · 2021 +161 · 2022 +39 · 2023 +12 · 2024 +94 · 2025 −1 · 2026 +151.
- Tüm 217 hissede P20: +99 (t 1,2) ve −32 (t −0,4).

**Uç değer:**
- Yalnız en iyi 10 gün (456 günün %2'si) çıkarılınca +7 (t 0,3).
- Simetrik (en iyi + en kötü 10 gün) çıkarılınca +40 (t 2,3). Kırpılmış 5/95: +34 (t 2,0). Medyan +32.
- Dağılım iki yönde de kalın kuyruklu; ortalama tek yönlü kuyruğa duyarlı.
- LOSO: +43..+61. Hisse ortalaması pozitif olan: 32/47.

**Plasebo:**
- Aynı hisse, rastgele gün: ort +9 [%95 sınır +25], p<0,001.
- Aynı gün, rastgele hisse: +12, p<0,001.
- **Gap-eşleşmeli kontrol:** VİOP47 fazlası +39 (t 1,75). **Tüm 217'de −8 (t −0,8): orada etki tamamen gap büyüklüğüyle açıklanıyor** (limite özgü değil).
- **Bayatlatılmış sinyal:** t+2 gün-içi short +51 (t 2,3), t+3 +38 (t 1,85); tüm evrende t+2 +51 (t 5,3). t+2 gap'i de +86 / +126. Etki t+1'e özgü bir açılış aşırılığı değil; "sıcak hisse gece +, gün-içi −" yapısı birkaç gün sürüyor.

**Mekanik bid-ask (h1, 2023-11+, n=158):**

| Bacak | bps (t) |
|---|---|
| Açılış → 10:30 | +2 (t 0,1): açılış gürültüsü yok |
| 10:30 → sürekli işlem sonu | +70 (t 2,7) |
| Kapanış seansı | +20 (t 2,8) |
| 10:30 → kapanış @15+tik | +71 (t 2,6) |
| Aynı, gap-eşleşmeli | +73 (t 2,7) |
| Aynı, piyasa-nötr | +70 (t 2,9) |

- 2023-11+ döneminde fade 10:30 sonrasında gerçekleşiyor; mekanik bid-ask kaynaklı değil.
- Bu dönem en güçlü alt dönem. En iyi 10 gün çıkarılınca +15 (t 0,65).

**Gerçek VİOP dolumu (bülten, n=548):**
- t+1'de vadeli açılışta limitte değil (%0,0). Medyan 18,6 bin işlem, 613 mn TL (%10 dilim 118 mn TL). Short açılabilir.
- Vadeli açılışı (≈09:30), spot açılış seansına göre bazı düşülünce **−53 bps** daha aşağıda.
- Vadeli open→close: brüt +2. **@15+tik −21 (t −0,8)** (1. aşamanın −4'ünü teyit ediyor). Açılıştan VİOP short'u çalışmıyor.
- **Vadeli VWAP girişi** (gün boyu VWAP emriyle short, kapanışta kapat; gerçekçi bir dolum):
  - brüt +64 (t 4,0); @15+tik **+41 (t 2,6)**, gün-ağırlıklı +30 (t 2,0).
  - Gap-eşleşmeli fazla +63 (t 3,9). Olay dışı günlerde koşulsuz +6.
  - **Piyasa-nötr +19 (t 1,6).** Simetrik 10+10 gün hariç +32 (t 2,9). En iyi 10 gün hariç +13 (t 1,0).
  - Alt dönemler: 2020 −20 · 2021–23 +57 (t 2,3) · 2024–26 +40 (t 2,0).
- Not: VWAP girişi, açılış girişi başarısız olduktan SONRA denendi. Bu bir seçim (veri madenciliği) riski.

**Hüküm:** Olgu var ama zayıf ve 2021+ rejimine bağlı; piyasa faktörünü çıkarınca t<2. **DÜŞÜK.**

### 2.2 (c) Tavana dokunup dönen (TU)

**VİOP47:**
- Kaynak tanımı (h≥1,0925): @15 +35 (t 1,8).
- Sıkı dokunma: @15 +7 (t 0,3). Plasebo p=0,15.
- Vadeli-listeli: brüt +8, @15 −7, plasebo p=0,53.
- Vadeli fiyatıyla: open→close −28 @15+tik; VWAP −11.
- h1 (2023-11+): sıkı TU VİOP47 10:30→kapanış +29 @15+tik (t 0,9).
- **RED.**

**Tüm evren (spot):**
- Sıkı TU: @15 +34 (t 3,6). Gap-eşleşmeli fazla +43 (t 4,6). h1'de 10:30→kapanış +48 (t 2,7), @15+tik +23 (t 1,3).
- Tavana dokunmayan YAKIN günlerde de benzer (h1: +79). Etki limite özgü değil, genel "yüksekten dönüş".
- Spotta açığa satış gerekiyor. **DÜŞÜK.**

### 2.3 (d) Taban sonrası (`log_b5.txt`, `log_b7.txt`)

**Olgu (basit getiri):**
- BC gap_{t+1}: −448 (t −13). t+2..5 XU100'e göre: −554 (t −7). VİOP47: −288 / −185. **KABUL.**
- Sürüklenme t+1'de yine tabanda kilitli kalan (dolamayan) olaylarda yoğunlaşıyor. Dolabilir olayların fazla getirisi işlem başı ≈ 0 (brüt +7).

**Dolabilir short** (t+1 kapanış → t+5, XU100 hedge, @19):

| Evren | İşlem başı | Gün-ağırlıklı |
|---|---|---|
| Tüm 217 | −12 (t −0,3) | +43 (t 1,0) |
| VİOP47 | +10 | +134 (t 1,9) |
| VİOP47 vadeli-listeli | −2 | +87 (t 1,4) |

- 2024–26 VİOP47: −87 / −30.
- Yıllar (VİOP47, işlem başı): 2021 −209 · 2022 +231 · 2023 +386 · 2025 −82 · 2026 −127.
- En iyi 10 gün hariç: −106 (t −2,1).

**Plasebo:**
- Aynı-hisse rastgele gün short'u −43; BC olayları buna göre p=0,004.
- Aynı-gün rastgele hisse (çöküş sonrası diğer hisseler XU100'ü +125 bps geçiyor): BC şirketleri göreli olarak geride.
- XU100 hedge'li işlenebilir short'ta bu fark kâra dönmüyor.

**Vadeli versiyonu** (t+1 uzlaşma → t+5 uzlaşma):
- t+1'de vadeli taban kilidi %1,8.
- İşlem başı +12 @19+tik (t 0,2), gün-ağırlıklı +138 (t 2,4).
- 2021–23: +238 (t 4,2). 2024–26: +23 (t 0,3).
- Kalabalık günlerde işlem başı −21.

**Hüküm:** Kaynağın +209 (t 4,6) sonucu log getiri + gün-ağırlıklandırma ürünü. **İşlenebilirlik RED; ÇOK DÜŞÜK–DÜŞÜK.**

### 2.4 Temettü ex-günü (`log_b4.txt`; 2014+, 1.051 olay, VİOP47 429)

**Veri kontrolü:**
- Açılış = önceki (düzeltmesiz) kapanış = gün kapanışı oranı %5,3. Bunlar bayat günler; gün-içi 0, sonucu seyreltiyor.
- h1 ilk bar açılışıyla günlük açılış 179/179 eşleşiyor.
- **Açılış primi = 53 bps + 0,15·verim.** 0,15'lik eğim, stopaj (%10–15) ile tutarlı rasyonel bir kısım. Brüt temettüyle teorik ex fiyat "pahalı" görünüyor.

**Alt dönemler (VİOP47 @15):**
- 2014–17: −3 (t −0,2) · 2018–20: +55 (t 2,1) · 2021–23: +55 (t 1,8) · 2024–26: +71 (t 3,5). Toplam +40 (t 3,5).
- Tüm evren 2014–17: +6 (t 0,55).
- İlk 4 yıl sıfır; 1. aşamanın IS düzeltmesi (+21) bununla tutarlı.

**Plasebo:**
- Rastgele gün p<0,001.
- ex−1: −2; ex+1: +14 (t 1,2). Etki ex-gününe özgü.

**Uç değer:** Simetrik 10+10 hariç +41 (t 4,5). Kırpılmış +39. 33/45 hisse pozitif. Sağlam.

**Mekanizma (h1 2023-11+):**
- Tüm evrende açılış→10:30 +81 (t 6,6), 10:30→kapanış +27. VİOP47: +48 / +37.
- Etkinin çoğu spot açılış seansının teorik fiyatın üstünde oluşmasından geliyor.

**VİOP:**
- Vadeli ex-gününde düzeltilmiyor. Açılış/önceki uzlaşma medyanı +7 bps (aynı olaylarda spot +68). **Vadelide prim hiç yok.**
- open→close: −29 @15+tik. VWAP→close: −16 (t −1,9).
- **VİOP ile RED.** Spotta açılış seansında açığa satış (kısıtlı) ya da 10:30 girişi (VİOP47 brüt +37, @15+tik ≈ +20) gerekiyor.

## 3. Veri madenciliği / çoklu test

- Kaynak 5 limit stratejisi × 3 evren × 2 maliyet = 30 BT ve 2 temettü × 2 evren × 2 maliyet = 8 BT çalıştırdı.
  - Ek olarak sınıf × ölçü × grup özet tablosu (113 satır) ve kriz/likidite kırılımları var.
- Başarısız BT1e (tavan → t+2..5 short; OOS −77) iddiaya alınmamış.
- Eşikler (1,0925; 0,999h; R<eşik−0,01) tek seçim, ama TU'da gevşek eşik sonucu taşıyor.
- Bonferroni benzeri ~10 bağımsız strateji-evren çifti için |t|>2,8 gerekir. Basit getiriyle bunu geçen işlenebilir VİOP versiyonu yok.
  - Geçenler yalnız olgular (a, d-olgu, temettü gün-içi) ve tüm evren spot fade'leri.
- Bu doğrulamada ~6 giriş yöntemi × 4 olay seti × 3 evren denendi. VWAP girişi sonradan eklendi; bulguyu DÜŞÜK güvenle raporluyorum.

## 4. Sorunlar listesi (öncelik sırasıyla)

1. **Log-getiri yanlılığı.** Short PnL'i −log(c/o) ile hesaplanmış. Fade'lerde +12–16 bps; taban short'unda +50–70 bps şişme. (d) dolabilir sonucu basit getiriyle işlem başı −12 (tüm) ve +10 (VİOP47).
2. **VİOP açılış dolumu imkânsız fiyat.** Vadeli açılışı spot açılış seansından önce ve ~53 bps aşağıda. TC fade vadeliyle −21 @15+tik; temettüde vadelide prim yok (−29).
3. **Ortak faktör.** TC fade'in ~%40'ı aynı gün piyasa gün-içi geri dönüşü. Piyasa-nötr: spot +30 (t 1,6), vadeli VWAP +19 (t 1,6).
4. **Limite özgü değil.** Tüm evrende TC fade gap-eşleşmeli kontrolle sıfır (−8). TU'da YAKIN günler aynı. Bayat sinyal (t+2) aynı büyüklükte.
5. **Hayatta kalan evren.** Bugünkü VİOP47 listesi geçmişe taşınmış. Vadeli-listeli olaylarda TU sıfır, BC işlem başı −2.
6. **Alt dönem.** 2020 (P10'un ilk yılı) her fade'de negatif. P20 rejiminde n çok küçük ya da sonuç işaretsiz. Temettü 2014–17'de sıfır. Etkiler 2021+ yüksek enflasyon / bireysel yatırımcı rejimine bağlı.
7. **Uç değer.** TC fade VİOP47'de en iyi 10 gün hariç +7. Taban short'unda −106. Simetrik kırpmada TC ve temettü ayakta, BC kısmen.
8. **Tik maliyeti.** Yahoo fiyatı bedelsizle geriye düzeltilmiş; ham `c` ile tik maliyeti 3 kat abartılıyor (22 bps; gerçekte 7). 1. aşama ve kaynak meta/splits kullanmış, oysa splits boş.

## 5. TradingView

| Amaç | Ticker |
|---|---|
| Spot | `BIST:<KOD>` |
| Pay vadelisi | `BIST:<KOD>1!` (ör. `BIST:THYAO1!`, `BIST:SASA1!`, `BIST:HALKB1!`, `BIST:GUBRF1!`, `BIST:BRSAN1!`) |
| Hedge | `BIST:XU030D1!` |
| Endeks | `BIST:XU100` |
