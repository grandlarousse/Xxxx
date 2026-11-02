# ry_akis: yurt içi akış, mikroyapı ve takvim bulguları (47 VİOP hissesi ve geniş BIST evreni)

**Ajan:** akis · **Veri sonu:** 30.10.2026 · **Kod:** `out/code_y_akis/` · **Bulgular:** `out/f_y_akis.csv` (72 satır)
**Yeni ortak veri:** `data/akis/tcmb_foreign_equity_weekly.csv` (TCMB haftalık yabancı hisse akışı ve stoku, 2005-01 → 2026-10-23, 1.137 hafta)

Olay ajanının bulguları tekrar edilmedi: PPK, FOMC, TÜFE, not kararları, bayram gap'i ve ay sonu |kapanış seansı| büyüklüğü.

---

## 1. Net bulgular

| # | Bulgu | Rakamlar | İşlenebilir mi? | Güven |
|---|---|---|---|---|
| 1 | **Tavan kapanışında fiyatlanamayan bilgi ertesi açılışa taşınıyor** (±%10 rejimi, 2020-03 sonrası, 177 hisse) | Ertesi gün gap **+282 bps** (t 44, %83 pozitif, n=5.340). IS +292 / OOS +274. VİOP47'de 47/47 hissede pozitif. Kilitli tavanda (h=l=c) +761 bps. Dokunup altında kapananda yalnız +20 bps. P(ertesi gün yine tavan \| tavan)=0,26, koşulsuz 0,021 | **Hayır.** Kilitli tavanda kapanıştan alım dolmuyor; dolan alımlar seçilmiş (ters seçim) | YÜKSEK (olgu) |
| 2 | **Tavan ertesi gün-içi geri dönüş** (gap'in bir kısmı gün içinde geri veriliyor) | Ertesi gün açılışta sat, kapanışta kapat. VİOP47 net +73 bps @8 / +66 @15 (t 3,2–3,6). IS(20–22) +59 (t 1,7) / OOS(23–26) +87 (t 3,6). Tüm evrende +58 @15 (t 5,2). Yılların 6/7'sinde pozitif. Kriz günleri hariç +83 brüt | Evet (VİOP pay vadelisi, açılış dolumu iyimser varsayım) | **ORTA** |
| 3 | **Tavana dokunup geri dönen gün → ertesi gün-içi düşüş** | Gap ~0, gün-içi −68 bps. Fade stratejisi @15: tüm evren +59 (t 6,4; IS +47 / OOS +68; 7/7 yıl). Likit tercil +76 (t 4,4). VİOP47 +59 (t 3,0) | Evet | **ORTA** |
| 4 | **Taban kapanışı: devam/sürüklenme var, geri dönüş yok** | Ertesi gap −388 bps (t −28). Sonra t+2..t+5'te XU100'e göre −510 bps (t −12,6). t+1 yine tabansa giriş yapılmayan ("dolum uygun") short: tüm evren +209 bps @15 (t 4,6; IS +153 t 1,8 / OOS +239 t 4,6). VİOP47 +144 (t 2,1) | Kısmen (VİOP short; spotta açığa satış kısıtı var). Naif BT (+628 bps) dolum yanılsaması | **ORTA** (tüm evren) / DÜŞÜK (VİOP47) |
| 5 | **Temettü ex-günü: açılış pahalı, gün içinde düşüyor** | Ex-gün açılışı teorik ex fiyatın +92 bps üstünde. Gün-içi −61 bps (t −7,5; IS −34 / OOS −105). VİOP47'de ex-günü açılışta sat, kapanışta kapat: @15 +29 bps (t 3,3; IS +8 / OOS +65 t 3,5). Açılış h1 verisiyle doğrulandı (veri hatası değil) | Evet (tarih önceden ilan ediliyor) | **ORTA** |
| 6 | **Temettü öncesi 5 gün yükseliş, sonrası geri veriş** | ex−5 → ex−1 fazla getiri +93 bps (t 6,0). @15 BT: tüm evren IS +55 (t 3,4) / OOS +115 (t 4,2). VİOP47: IS +25 / OOS +61 (t 1,8). Ex sonrası 5 gün −32 (OOS −102, t −4,2) | Evet | **ORTA** (evren) / DÜŞÜK (VİOP47) |
| 7 | **Yabancılar getiriyi takip ediyor, öncülemiyor** (TCMB haftalık, 2005–2026) | Önceki hafta USD getirisi → bu hafta akış: corr **0,32** (t 11,9). 22/22 yıl pozitif; IS 0,32 / OOS 0,31. Senkron 0,25. Akış → yayın sonrası 5 gün: corr 0,03 (OOS −0,03). BT: −5 bps @8 | Hayır | **YÜKSEK** (ters yön olgusu) / ÇOK DÜŞÜK (öncülük) |
| 8 | Yayın anı tepkisi: Perşembe 14:30 TSİ'de akış haberi | Akış_z ile yayın günü 11:30→kapanış XU030 getirisi corr 0,22 (n=153, 2023-11+). Plasebo günlerde −0,18..+0,05. Etki ilk saatte; 12:30 sonrası giriş @15'te −4 bps | Hayır (saniyeler/dakikalar içinde fiyatlanıyor) | DÜŞÜK |
| 9 | Yabancı akış kesiti: bankalar ↑, savunmacı ↓ (senkron) | Akış ile XU100'e göre fazla getiri: YKBNK +0,19, AKBNK/ISCTR +0,16, GARAN/SAHOL/KCHOL +0,12. BIMAS −0,19, OYAKC −0,13, DOHOL −0,11. 16/47 FDR'den geçti. Öncülük (post5) 0/47 FDR | Hayır (senkron) | DÜŞÜK |
| 10 | **2026 fon krizi: tasfiye hisseleri çöktü, öncülük yok** | 11.09–30.10 medyan getiri: tasfiye10 **−%96**, diğer BIST −%37, VİOP47 −%21. Kesit regresyonu (n=184): önceki 12 ay getirisi (−), oynaklık (−), hacim (+); tasfiye kuklası log −1,68 (z −5,4). Sepet_{t−1} → XU030_t corr 0,00 | Hayır (öncülük yok) | ORTA (olgu) / ÇOK DÜŞÜK (öncülük) |
| 11 | Endeks dönem değişikliği (6 çeyrek, 118 olay) | Duyuru sonrası ilk gün işaretli fazla getiri +322 bps (6/6 çeyrek). 2026Q4 hariç +86 (t 1,9; 5/5 çeyrek). Arifeye kadar sürüklenme yok (−122). Arife günü −100 bps (t −2,5; 0/5 çeyrek) | Tepki gece fiyatlanıyor; arifeye kadar tutmak −137 bps @15 | DÜŞÜK |
| 12 | Ayın ilk işlem günü (XU100/XU030) | d1 cc +32 bps vs diğer günler +5,6 (t 2,2; 17/22 yıl). BT: ay sonu kapanışında al, d1 kapanışında sat. IS −1 bps / OOS +80 (t 4,2) | Evet ama yalnız 2021+ rejiminde | DÜŞÜK |
| 13 | Endeks devre kesici günleri (XU100 gün-içi dip ≤ −%5; 32 gün) | Ertesi gün cc +102 bps (t 1,75; 20/32 pozitif). Gap +8, gün-içi +94. t+1..20 +360 (t 2,2) | Zayıf | DÜŞÜK |
| 14 | Vade sonu kapanış seansı (h1, 36 vade sonu) | \|auc\| 46 bps vs normal 31. Ertesi gün geri dönüş katsayısı −0,37 vs normal 0,00. −işaret(auc) stratejisi +30 bps brüt (t 1,4) | Sınırda (VİOP 18:15'e kadar açık) | DÜŞÜK |
| 15 | Bedelsiz ex sonrası düşüş (92 olay) | +1..+5 gün −338 bps (t −3,0), +1..+20 gün −511 (t −2,5). VİOP47'de 2010+ olay yok | Spot short kısıtlı, VİOP'ta yok | DÜŞÜK |
| 16 | Taban/tavan günü VİOP vadeli−spot primi → ertesi gap | Taban: corr 0,56 (IS 0,15 / OOS 0,67). Üst %20 prim → gap +109 bps, alt %80 −227..−368. Gün-içi Spearman IC 0,07 (t 0,8). Tavan: IC 0,25 (t 2,3) | Teorik olarak evet (taban kapanışından alım kolay dolar) | DÜŞÜK (aykırı değere dayalı) |
| 17 | **OLUMSUZ – Mıknatıs etkisi yok** (h1, ~100 hisse) | Limite yakın başlangıçta P(önce limit)=0,623 vs martingal 0,564 (+6 puan). Plasebo seviyede +10 puan. Fazlalık genel gün-içi momentum | — | DÜŞÜK (olumsuz) |
| 18 | **OLUMSUZ – MSCI/FTSE/ay sonu günleri** | Endeks getirisinde anlamlı yön yok (\|t\| < 1,7) | — | ÇOK DÜŞÜK |
| 19 | Veri yok: günlük açığa satış, kredili işlem serisi, MKK hisse bazlı yabancı payı, TEFAS günlük akış | Açığa satış yasağı dönemleri rejim olarak test edildi: tavan/taban etkileri farklı değil (taban sürüklenmesi, brüt: yasakta +122, dışında +292) | — | ÇOK DÜŞÜK (veri yok) |

**TradingView:**
- Spot hisse: `BIST:<KOD>`
- Pay vadelisi: `BIST:<KOD>1!` (tv ajanı 47/47 doğruladı)
- Endeks vadelisi: `BIST:XU030D1!`
- Endeksler: `BIST:XU100`, `BIST:XU030`
- TCMB yabancı akışı ve fon/açığa satış verilerinin TradingView karşılığı yok (`?`).

---

## 2. Önemli yan bulgu: ll.py temizlik kuralı ve fiyat limiti rejimleri

**Fiyat limiti rejimleri veriden tespit edildi** (177 hisse, R = adj_t/adj_{t−1}):

| Dönem | Kural | Veride görünen |
|---|---|---|
| 2015-11 öncesi | Baz fiyat ağırlıklı ortalama fiyat | Kapanış oranı limitle örtüşmüyor |
| 2015-12 .. 2020-03-10 | **±%20** | R=1,19–1,21 yığılması; 2016–2019'da yılda 38–53 gün |
| 2020-03-13 sonrası | **±%10** | R=1,095–1,105'te yılda 570–1.240 gün; R>1,11 neredeyse sıfır |

- Geçiş haftasında (9–13 Mart 2020) 87 adet −%11'den büyük düşüş görülüyor.
- **Sonuç:** `ll._bad` (fiyat bazında ±%10,5 dışı = NaN) **2015-12..2020-03 arasında gerçek %10,5–20 hareketlerini siliyor.** 177 hissede 2016–2019 arasında yılda ~150–250 gün, toplam ~800 hisse-gün (bir kısmı gerçekten kurumsal işlem/veri hatası olabilir).
- Bu, o dönemin büyük şok günlerini (2018 kur krizi gibi) diğer ajanların örnekleminden atıyor ve oynaklığı küçültüyor.
- ll.py'yi değiştirmedim. Koordinatörün rejime bağlı eşik (2020-03-13 öncesi ±%20,5) düşünmesini öneririm.
- Bu rapordaki limit analizleri kendi panelimle (`alib.panel`, temizlemesiz) yapıldı.

**VİOP pay vadelisi limitleri:** Bültenlerde en yüksek fiyat / önceki uzlaşma oranı en çok 1,100. Yani vadeli de ±%10 limitli. Spot kilitlendiğinde vadeli de kilitleniyor, "gerçek fiyat" vadelide görünmüyor (#16'daki sinyal yalnızca vadeli limitte kalmadığında oluşuyor).

---

## 3. Yöntem

### 3.1 Tavan/taban (a_limit.py, f_bt.py, f2_robust.py, f3_fill.py, g_viop_limit.py, h_magnet.py)

**Evren:** 177 BIST hissesi (47 VİOP + 130 diğer; 2026 krizine kadar likit/illikit karışık).

**Rejimler:** P10 = 2020-03-13+ (ana) ve P20 = 2015-12..2020-03-10 (kontrol). P20'de olay sayısı az (TC 202, BC 41) ama işaretler aynı: tavan sonrası gap +529, taban sonrası −826.

**Sınıflar** (P10 eşikleri; tik yuvarlama toleransı ile):

| Kod | Tanım |
|---|---|
| TC | Tavan kapanışı: R ≥ 1,0925 ve c ≥ 0,999h |
| TCL | Kilitli tavan: TC ve l ≥ 0,999h |
| TU | Tavana dokundu (h-oranı ≥ eşik) ama R < eşik − 0,01 ile kapandı |
| BC / BCL / BU | Tabanda simetrik tanımlar |
| UP6 / DN6 | Kontrol: limite dokunmayan ±%6–9 günler |

**Ölçüler:**
- gap_{t+1} = cc − intra (temettü düzeltmeli)
- intra_{t+1} = log(c/o)
- cc_{t+2..t+5}
- Hepsi ham ve XU100'e göre fazla getiri olarak hesaplandı.
- t-istatistikleri tarih kümelemeli (gün ortalamalarının t'si).
- Backtest t'leri: günlük portföy getirisi, Newey-West (5 gecikme).

**IS/OOS:**
- P10 rejiminde brifteki 2014–2020 / 2021–2026 ayrımı neredeyse boş IS bırakıyor (2020-03..12).
- Bu yüzden ana ayrım IS = 2020-03..2022-12 / OOS = 2023-01..2026-10.
- Brif ayrımı da raporlandı (`res_bt_all.json`, anahtarlar `IS_brief_2020` / `OOS_brief_21_26`).

**İşlenebilirlik kontrolleri:**
- (i) Tavan kapanışında alım kilitli tavanda dolmaz → gap stratejisi yok.
- (ii) Taban sürüklenmesinde t+1 de tabansa short dolmaz → yalnız "dolum uygun" giriş.
- (iii) Açılış fiyatından dolum iyimser varsayım.
- (iv) Küçük hisselerde spread 15 bps'i aşar; likit tercilde ayrıca raporlandı.

**Mıknatıs testi:** Saatlik bar kapanışında +%7–8 bandındaki hisse, aynı gün önce limite (+%9,8) mi yoksa 3 puan aşağıya mı ulaşıyor? Martingal (Brown hareketi) beklentisi ve +%3–4 plasebo bandı ile karşılaştırıldı.

### 3.2 Yabancı akışı (b_flows.py, b2_release_placebo.py, b3_release_drift.py)

**Kaynak:** TCMB Menkul Kıymet İstatistikleri.
- TCMB sayfasındaki zip yalnız son 5 haftayı içeriyor.
- Tam geçmiş için **EVDS3'ün halka açık web arayüzünün kendi veri uç noktası** kullanıldı (`/igmevdsms-dis/fe`; anahtar/oturum gerekmedi).

**Seriler:**

| Seri | Kod | Dönem |
|---|---|---|
| Hisse net hareket | TP.PYUK3 (arşiv) | 2005–2021-08 |
| Hisse net hareket | TP.MKNETHAR.M7 (yeni) | 2020-09+ |
| Hisse stoku | TP.PYUK1 / TP.MKNETHAR.M1 | — |

Örtüşen 48 haftada eski ve yeni seri corr 0,99999.

**Uyarı (diğer ajanlar için):** API binlik ayırıcılı ("31,569.27") dönüyor. `groupSeperator:false` kullanın, yoksa >1.000'lük değerler NaN olur.

**Zamanlama:**
- Hafta w = Pzt..Cuma.
- Yayın izleyen Perşembe 14:30 TSİ. D_w = Cuma + 6 gün (tatilse sonraki iş günü).
- Yayın sonrası pencere: D_w kapanışı → 5 iş günü sonrası kapanışı.
- Akış ölçeği: geçmiş 52 haftanın std'si (look-ahead yok).

**Kesit:** 47 hisse; senkron ve post5 testleri, BH-FDR (2×47 test).

### 3.3 Fon krizi (e_crisis.py)

- Tasfiye10 listesi (fonların fiili dolaşımdaki payı en yüksek 10 hisse): borsaningundemi.com haberi. Eksik semboller ydl ile indirildi.
- Kriz takvimi: Gedik 05.10.2026 raporu, Tablo 3.
- Gedik raporu hisse adı vermiyor. Verdiği rakamlar:
  - Tasfiye fonları 31.08'de 1.233 → 30.09'da 652 mlr TL.
  - Likit olmayan 123 hisse pozisyonu 146,5 mlr TL; ilk 10 hisse %86.
  - Bunların %45'inin satışı 60 işlem gününden uzun sürüyor.

### 3.4 Takvim (c_calendar.py, c2_auction.py, c3_divsplit.py, d_index.py)

- **Olaylar:** ay sonu (= VİOP vade sonu), TOM (−1..+3), ilk 3 gün, tatil öncesi/sonrası, dini bayram arifesi (≥2 hafta içi kapanış öncesi = yarım gün), MSCI (Şub/May/Ağu/Kas son iş günü), FTSE (Mar/Haz/Eyl/Ara 3. Cuma), çeyrek sonu.
- **Kapanış seansı getirisi:** log(günlük kapanış / 15:00 UTC h1 fiyatı), 2023-11+.
- **Temettü:** adj/c oranındaki sıçramadan (verim %0,3–25; 1.195 olay, 130 hisse).
- **Bedelsiz:** Yahoo split meta (oran > 1,05; ±20 gün içinde düzeltilmemiş sıçrama varsa olay hariç).
- **Endeks değişiklikleri:** 6 çeyrek, web haberleri (`index_events.py`, kaynak ve saat notlarıyla).
  - Seans içi duyuru (23.12.2025, 17:33 TSİ) ayrı işlendi.
  - Arife yarım gününde (19.03.2026) yapılan duyuru ertesi işlem gününe kaydırıldı.

---

## 4. Kanıt ayrıntıları

### 4.1 Tavan/taban ertesi gün (P10, tüm evren; bps, tarih kümelemeli t)

| Sınıf | n | gap_{t+1} | gün-içi_{t+1} | t+2..5 (XU100'e göre) | P(gap>0) |
|---|---|---|---|---|---|
| TC tavan kapanış | 5.340 | +282 (t 44) | −68 (t −6,7) | +60 (t 2,4); halka arz hariç −5 | 0,83 |
| TCL kilitli tavan | 393 | +761 | −171 | +868 (halka arz hariç +63) | 0,93 |
| TU dokundu, kapanmadı | 3.297 | +20 | −68 (t −7,9) | −41 (t −2,9) | 0,60 |
| UP6 (+%6–9, dokunmadı) | 3.875 | +30 | −9 (t −2,1) | −12 | 0,61 |
| BC taban kapanış | 2.468 | −388 (t −28) | +121 (t 1,0) | −510 (t −12,6) | 0,20 |
| BCL kilitli taban | 392 | −763 | +246 (t 4,9) | −1.640 | 0,12 |
| BU dokundu, kapanmadı | 1.531 | −9 | −24 | −77 (t −3,6) | 0,48 |
| DN6 (−%6–9) | 2.744 | +32 | +9 | −57 (t −2,9) | 0,57 |

**Okuma:**
- Limit, kapanışta fiyatlanması gereken bilginin bir kısmını ertesi açılışa taşıyor. Tavanda +282 bps, tabanda −388 bps; dokunup kapanmayan günlerde ve kontrol günlerinde bu taşınma yok.
- **Tavan sonrası:** taşınan kısım gün içinde %25 kadar geri veriliyor (aşırı tepki).
- **Taban sonrası:** satış birkaç güne yayılıyor (sürüklenme). Zorunlu satış ve teminat tamamlama ile tutarlı; kredili veri olmadığı için bu mekanizma test edilmedi.
- **Halka arz:** ilk 40 işlem günündeki tavan serileri t+2..5 sürüklenmesini tek başına üretiyor; halka arz hariç sürüklenme yok.
- **Hisse bazında** (`res_limit_viop47_bystock.csv`): tavan sonrası gap 47/47 VİOP hissesinde pozitif. En çok tavan: BRSAN 75, SASA 44, GUBRF 38, HALKB 37, DOAS 35, HEKTS 34, ASTOR 34.

### 4.2 Backtestler (özet; tamamı `res_bt_all.json`)

| BT | Evren | @8 bps tümü | @15 tümü | IS (2020–22) | OOS (2023–26) | Not |
|---|---|---|---|---|---|---|
| BT1a: tavan → ertesi açılış SAT / kapanış AL | VİOP47 | +73 (t 3,6) | +66 (t 3,2) | +52 @15 (t 1,5) | +80 @15 (t 3,4) | n=722 işlem, 439 gün |
| BT1a | tüm evren | +65 (t 5,8) | +58 (t 5,2) | +21 (t 1,3) | +85 (t 5,6) | IS zayıf |
| BT1b: dokunup dönen → ertesi gün-içi SAT | tüm evren | +66 (t 7,2) | +59 (t 6,4) | +47 (t 3,0) | +68 (t 5,9) | 7/7 yıl + |
| BT1c: kilitli taban → ertesi gün-içi AL | tüm evren | +179 (t 4,4) | +172 (t 4,2) | +212 (t 2,9) | +151 (t 3,3) | isabet %30, çarpık |
| BT1d: taban → t+1 kapanış SAT, t+5 kapat (fazla getiri) | tüm evren, dolum-uygun | — | +209 (t 4,6) | +153 (t 1,8) | +239 (t 4,6) | naif hali +628 (dolum yanılsaması) |
| BT1d | VİOP47, dolum-uygun | — | +144 (t 2,1) | +98 (t 1,0) | +169 (t 1,8) | n=350 |
| BT2: endeks değişikliği tepki kapanışı → arife | 50 olay (2026Q4 hariç) | −130 | −137 | — | — | başarısız |
| BT3: vade sonu kapanış seansı geri dönüşü | VİOP47, 36 gün | +30 brüt (t 1,4) | — | — | — | n küçük |
| BT4: yabancı akış işareti → XU030 haftalık | 881 hafta | −5 (t −0,4) | −12 | −6 | −4 | başarısız; \|z\|>1: IS +35 / OOS −12 |
| BT5: ay sonu kapanış → d1 kapanış XU030 | 203 ay | +27 (t 2,1) | +20 | −1 / −8 | +80 / +73 (t 3,8) | yalnız 2021+ |
| BT6a: temettü ex−5 → ex−1 (fazla getiri) | tüm evren | +85 (t 5,9) | +78 (t 5,4) | +55 (t 3,4) | +115 (t 4,2) | VİOP47 @15: +38 (t 2,1) |
| BT6b: ex-gün açılış SAT / kapanış AL | VİOP47 | +36 (t 4,0) | +29 (t 3,3) | +8 (t 0,9) | +65 (t 3,5) | IS isabet %32 |

**Kriz kümeleri** (2020-03, 2021-12, 2023-02, 2025-03/04, 2026-09/10) hariç (brüt, maliyetsiz):

| Strateji | Tümü | Kriz hariç |
|---|---|---|
| BT1a (VİOP47) | +81 | +83 |
| BT1b (tüm evren) | +74 | +73 |
| BT1d naif (VİOP47) | +407 | +508 |
| BT1d naif (tüm evren) | +636 | +601 |

Aynı gün 5'ten az olay olan günlerle sınırlayınca da aynı tablo çıkıyor (tüm evren, brüt: BT1d +612, BT1a +73). Yani sonuçlar kalabalık çöküş günlerinden gelmiyor.

### 4.3 Yabancı akış: yıllara göre korelasyon (`res_flow_byyear.csv`)

- **Ters yön** (getiri_{w−1} → akış_w): 2005–2026 arasında 22/22 yıl pozitif (0,02..0,65).
- **Öncülük** (akış → post5): işaret yıldan yıla değişiyor (−0,37..+0,31), ortalama ~0.
- Son 3 yılda akış → sonraki hafta yayın öncesi getiri −0,19. Bu kısım işlenemez (akış henüz bilinmiyor) ve büyük olasılıkla kısa vadeli getiri geri dönüşünün yansıması.

### 4.4 Endeks değişiklikleri (çeyrek × endeks × yön; işaretli fazla getiri, bps)

**Duyuru tepkisi:**
- Tepki günü 6/6 çeyrekte pozitif.
- Örnekler: 2025Q4 BIST30'a giren DSTKF +362, 2026Q2 VAKBN +159, 2026Q4 TRMET +718.

**Arifeye kadar sürüklenme:**
- 2026Q4 dışında çoğunlukla negatif.
- 2024Q4: girenler −509, çıkanlar −477. 2025Q3: −548 / −498.

**2026Q4 (fon krizi):**
- Çıkanlar arifeye kadar 2.272 bps daha düştü (DSTKF, KTLEV, PASEU ...). Bu endeks etkisi değil, kriz etkisi.

**Genel değerlendirme:** Türkiye'de pasif fon payı küçük. Etki duyuru gecesi fiyatlanıyor; yürürlük kapanışında ek baskı görülmüyor (arife günü işaretli −100 bps).

---

## 5. Karşı argümanlar ve sınırlamalar

### 5.1 Tavan/taban
- **Ortak bileşen:** Olayların bir kısmı aynı günlere yığılıyor (çöküş ve ralli günleri). Tarih kümelemeli t ve kriz hariç testler bunu kısmen kontrol ediyor.
- **Veri:** Yahoo açılış fiyatı açılış seansı fiyatı mı, ilk işlem mi, belirsiz. Saatlik ilk barla günlük açılış 96/96 eşleşti (temettü testi).
- **Dolum varsayımları:** Açılışta VİOP'tan açığa giriş varsayıldı. Pay vadelilerinin çoğu illikit (BRSAN, GUBRF, HEKTS). Gerçek maliyet 15 bps'i aşabilir. Yarı yarıya ihtimalle 15–30 bps.
- **Tavan sonrası gap:** BIST'in tavan kilidinin bilgi taşıdığını gösterir; ama mekanizma "manipülatif tavan serisi" de olabilir (SPK tedbirli hisseler, halka arzlar). Halka arz hariç sonuç değişmiyor; tedbir listesi verisi yok.
- **Taban sürüklenmesi:** Spotta açığa satış dönem dönem yasak (2025-03..08, 2026-03..06) ve yukarı adım kuralı var. Etki büyük ölçüde küçük hisselerde. VİOP47'de dolum-uygun versiyon IS'te anlamsız (t 1,0).
- **±%20 rejimi** (2015–2020): olay sayısı az. Sonuçlar ±%10 rejimine genellenmemeli; işaretler aynı.

### 5.2 Yabancı akış
- Haftalık veri hisse bazında değil. TCMB serisi "fiyat ve kur etkisinden arındırılmış net alım" ama saklamacı bazlı.
- Senkron ilişkinin bir kısmı aynı haftadaki fiyat hareketini yabancıların tetiklemesinden, bir kısmı getiriyi takipten geliyor; ayrıştırılamaz.
- Öncülük testi olumsuz. Yayın anı tepkisi (corr 0,22) yalnız 153 hafta; 1 saat içinde bitiyor.

### 5.3 Fon krizi
- Kesit sonucu güçlü ama tek olay; nedensellik zayıf. Tasfiye hisseleri önceden %458 (medyan) yükselmişti; "balon sönmesi" ile "zorunlu satış" ayrıştırılamıyor.
- TEFAS günlük akış verisi alınamadı: site WAF ile reddetti, atlatma denenmedi. Fon akışı → getiri öncülüğü **test edilemedi.**

### 5.4 Endeks olay listesi
- 6 çeyrek, haber kaynaklı; BIST100 listeleri bazı kaynaklarda çelişkili. Çelişkili çeyreklerde (2025Q3 BIST100) yalnız BIST30/50 kullanıldı.
- BIST30 değişikliklerinin 2015–2024 tarihçesi derlenemedi (KAP/BIST arşivine erişim yok). **n küçük.**

### 5.5 Takvim
- d1 ve TOM etkileri yalnız 2021+ dönemde güçlü (yüksek enflasyon/TL rejimi). Rejime bağlı; geleceğe genellenmemeli.
- Vade sonu kapanış seansı analizi yalnız 36 vade sonu içeriyor.

### 5.6 Devre kesici
- EBDKS günleri veriden tahmin edildi (dip ≤ −%5); resmi liste yok.
- Bazı günlerde kapanış = dip (2022–2023). Yahoo'nun günlük düşük fiyatı muhtemelen kapanışa eşit kaydedilmiş; bu, devre kesicinin gerçekten çalıştığını kanıtlamıyor.
- Eşik 5/7'den tek aşamalı %6'ya değişmiş; tarihi doğrulanamadı.

### 5.7 Erişilemeyen veriler
- Açığa satış hisse bazlı günlük veri: fintables 403, BIST'te yok.
- Kredili işlem serisi.
- MKK hisse bazlı yabancı takas oranı arşivi.

Hepsi ÇOK DÜŞÜK (veri yok) olarak listede.

---

## 6. Kaynaklar

- TCMB Menkul Kıymet İstatistikleri: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Parasal+ve+Finansal+Istatistikler/Menkul+Kiymet+Istatistikleri/
- EVDS3 veri grupları: https://evds3.tcmb.gov.tr/tumSeriler/450301/bie_mknethar (bie_mknethar) ve arşiv bie_yymkpyuk.
- Gedik Yatırım tasfiye raporu (05.10.2026): https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf
- Tasfiye fonlarının hisseleri: https://www.borsaningundemi.com/haber/iste-tasfiye-karari-verilen-fonlarin-elindeki-hisseler-1908618
- Endeks değişiklikleri:
  - https://genelekonomi.com/2026/09/21/bist-30-bist-50-ve-bist-100-endekslerine-giren-ve-cikan-hisseler-aciklandi/
  - https://infoyatirim.com/blog/borsanin-gozunden/borsa-istanbul-2026-1-ceyrek-endeks-donemsel-degisiklikleri
  - https://www.cnbce.com/borsa/borsada-endeksleri-degisecek-hisseler-belli-oldu-ulker-cikiyor-vakifbank-giriyor-h27000
  - https://www.borsagundem.com.tr/bistte-2025in-4-ceyreginde-30-hisse-endeks-degisikligine-gidilecek
  - https://www.borsagundem.com.tr/borsa-istanbulda-3-ceyrek-endeks-degisiklikleri-belli-oldu
  - https://www.foreks.com/haber/detay/66eee6e7f92141287cafbc44/PICNEWS/tr/bist-pay-endekslerinde-2024-yili-dorduncu-ceyrek-donem-degisiklikleri-belirlendi/
  - https://www.getmidas.com/midasin-kulaklari/bist-endekslerinde-degisiklige-gidildi-2-p-148884
- Açığa satış yasağı dönemleri: https://www.capital.com.tr/piyasalar/borsa/spk-aciga-satis-yasagini-12-hazirana-kadar-uzatti , https://www.karar.com/ekonomi-haberleri/spkdan-aciga-satis-karari-yasak-29-agustosa-kadar-uzatildi-1971550 , https://www.borsaningundemi.com/etiket/aciga-satis-yasagi
- Devre kesici kuralı: https://www.capital.com.tr/piyasalar/borsa/borsada-endeks-bazli-devre-kesici-onlemi , https://www.ntv.com.tr/ekonomi/borsada-devre-kesici-nedir-ne-demek-borsada-devre-kesilirse-ne-olur,gfwzlnjm-0ucKDqXkAZfNw
- VİOP günlük bülteni: data/viop/ (başka ajan indirdi; 2017–2026, 1.759 gün).

## 7. Yeniden üretim (sıra)

Çalıştırma: `cd out/code_y_akis && nice -n 10 python3 <betik>`

| Adım | Betik | İçerik |
|---|---|---|
| 1 | alib.py | Ortak yardımcılar; panel önbelleği `_panel_ohlc.parquet` |
| 2 | a_limit.py | Tavan/taban olay tanımı ve ertesi gün etkileri |
| 3 | b0_fetch_tcmb.py, b_flows.py, b2_release_placebo.py, b3_release_drift.py | Yabancı akış (b0 veriyi `data/akis/` altına indirir) |
| 4 | c_calendar.py, c2_auction.py, c3_divsplit.py | Takvim, kapanış seansı, temettü/bedelsiz |
| 5 | d_index.py | Endeks değişiklikleri (olay listesi `index_events.py`) |
| 6 | e_crisis.py | Devre kesici günleri ve fon krizi |
| 7 | f_bt.py, f2_robust.py, f3_fill.py, f4_shortban.py | Backtestler ve sağlamlık |
| 8 | g_viop_limit.py, g2_viop_prem.py | VİOP vadeli−spot primi |
| 9 | h_magnet.py | Mıknatıs testi |
| 10 | z_findings.py | `f_y_akis.csv` |
