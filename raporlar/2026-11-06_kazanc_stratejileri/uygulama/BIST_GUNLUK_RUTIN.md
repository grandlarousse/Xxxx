# BIST günlük akşam rutini (TSİ): tek sayfa

**Ne için:** `PLAN_BIST.md` kurallarının her işlem günü uygulanışı. Kural metni planda; § numaraları onu gösterir. Gün içinde ekran yok. Tek emir penceresi ertesi gün 17:50–18:05'tir ve yalnız emir varsa açılır.
**Araçlar:** `kod/bist_sinyal.py` (çıktı `tarama/bist_sinyal_YYYYMMDD.md`), `~/bist_veri/makro.json`, aracı kurum emir ekranı, işlem günlüğü (§8.2).
**Değişmez kurallar:** Piyasa emri yok. Sabah normal limitli emir yok. Kredili işlem yok. Dışlama listesi (§4.2) emir ekranında "yasak". K1–K9 dışında işlem yok; tek bir sapma bütün uyduyu 1 ay kâğıda alır (§8.5).

## 1. 18:20–18:30: veri ve rejim

1. **Komut:** `python3 -I kod/bist_sinyal.py --veri ~/bist_veri --cikti tarama`. Betik 18:20'den önce çalışırsa bugünün bitmemiş barını atar. Çıktının ilk satırını (Özet) günlüğe kopyala.
2. **Veri kontrolü:** Başlıktaki tarih bugün mü, "Bulunamayan kod" boş mu? Değilse bugün yeni giriş yok; çıkışlar dünkü stop seviyeleriyle hazırlanır.
3. **Rejim (§2.1–2.2):** AÇIK / GEÇİŞ / KAPALI ve 7 gösterge. Durum değişikliği ertesi işlem gününden geçerlidir. K4 r₀: %0,25 / %0,5 / %0,75.
4. **KRİZ (§2.2), tetik (a)–(f):** Biri EVET ise 5 işlem günü yeni giriş yok ve K6 kapanır. Ertesi kapanışta hedgesiz K3/K3b satılır. K4, K5 ve K9 stopu = max(iz-stop, bugünkü kapanış × 0,90) olur. K1 sürer.
5. **Frenler (§5):** Aylık uydu −%2,5'te ay sonuna kadar giriş yok. Birikimli −%4'te açık yönlü pozisyonlar ertesi kapanışta yarıya iner; −%6'da uydu kapanır. K9 için sınır −%1,5. L1: VİOP teminatı ≤ (PPF − spot uydu) / 3; bozulursa L2 sırası K6 → K7 → K2 → K9 → K1.

## 2. 18:30–18:45: sinyaller (önce açık pozisyonlar, sonra yeni girişler)

- **Açık pozisyonlar:**
  - K4: iz-stop (kapanış ≤ girişten beri en yüksek kapanış × 0,85), E2 (120 gün), E4 (dışlama), E6 (bedelsiz ≥ %500), E7 (KRİZ, A4).
  - K3: gün −1. K3b: hak −1 ya da stop (giriş × 0,88).
  - K1/K2: 20. işlem günü ya da felaket stopu (bacak nominalinin −%8'i).
  - Vadeli devir: Kasım 25.11, Aralık 23.12.
- **K4 yeni giriş:** Betikteki "Nitelikli" satırları. Takvim ve bilanço kontrolü (A1–A10): bilanço gecesi, 11–13.11, MSCI, kredili esneklik, bedelsiz ve temettü pencereleri. Ardından küme ve Blok 1 sayımı (ENJSA / AHGAZ+ENERY tek küme). Boyut betiğin % ve TL sütunlarından okunur; tutar 60 günlük medyan hacmin %2'sini aşmaz.
- **K1 / K2:** Betikteki z ve "Karar" sütunu. K1 için Kural 0 ve komisyon ≤ 5 bps/bacak/yön gerekir. K2'ye yalnız yeni kesişimde girilir.
- **K3 / K3b:** Cuma KAP taramasından gün −6 ve bildirim tarihleri. K3b, 01.02.2027'ye kadar yalnız kâğıt.
- **K9:** Fikir kartı (mekanizma, giriş, stop, çıkış) 18:45'e kadar yazılmazsa giriş yok.
- **Tavanlar:** KAPALI'da açık risk ≤ %2,5, stres ≤ %6, spot uydu ≤ %15, VİOP teminatı ≤ L1. Tavanı aşan yeni giriş şu öncelik sırasıyla reddedilir: K3b > K1 > K3 > K5 > K4 > K2 > K9 > K6.

## 3. 20:45 sonrası: VİOP bülteni (5–10 dk)

Bülten CSV'si 20:28–20:49'da çıkar. Uzlaşma fiyatı 18:55'ten sonra ilan edilir.

1. Betiği yeniden çalıştır. Çıktıdaki bülten tarihi bugün olmalı. "BAYAT" yazıyorsa 21:15'te bir kez daha dene. Hâlâ yoksa VİOP kararını dünkü bültenle ver ve günlüğe "bayat" yaz.
2. **XU030 nakit-taşıma (§1.5):** İma basit oran ≥ mevduat neti + 3 puan ve Kural 0 sağlanıyorsa ertesi gün açılır. 5.11'de oran %29,3, eşik %35,6: kapalı.
3. **F_USDTRY ön ay:** İma oran > politika faizi + 5 puan ise KRİZ (e) tetiklenir. K6 kapısının 6 koşulu da aynı tabloda.
4. **Pay vadelisiyle long:** Yalnız betikteki "Kural sağlanıyor = E" ise; değilse spot.

## 4. 21:00'e kadar: ertesi günün emir kâğıdı

Her emir için hisse ya da kontrat, kol, adet, plan limiti, stop seviyesi ve aşağıdaki formül yazılır. Böylece 18:00 penceresi mekanik olur.

| İş | Saat (ertesi gün) | Limit |
|---|---|---|
| Spot giriş (K3, K3b, K4, K5, K9) | 18:01–18:05 | min(plan limiti; P_son × 1,03), aşağı adıma. Plan limiti K4'te t kapanışı × 1,06, K3/K3b'de önceki kapanış × 1,04. Tavanda kilitliyse atla |
| Spot risk azaltan satış (stop, K3 gün −1, K3b, KRİZ, A3/A4, dışlama) | 18:01–18:05 | max(taban fiyatı; P_son × 0,97), yukarı adıma. Dolmazsa ertesi gün aynısı |
| Spot süre çıkışı (K4 E2) | 18:01–18:05 | max(önceki kapanış × 0,94; P_son × 0,97) |
| 18:05 kaçtıysa | 18:08–18:10 | Kapanış fiyatından; günlüğe "geç" |
| VİOP çift girişi (K1, K2) | 17:50 kontrol, 17:55, 18:05, 18:08 | Bir bacak ±%9'daysa giriş yok. Karşı en iyi fiyat ± %0,3, sonra ± %0,6. 18:08'de tek bacak dolmuşsa β × nominal ters F_XU030 |
| VİOP çıkışı | 17:55, 18:05, 18:08 | ± %0,3, sonra ± %1, sonra fiyat limiti |

P_son, kapanış seansından önceki son işlem fiyatıdır. Kapanış seansındaki emir bu fiyatın ±%3'ü dışında olamaz (Borsa İstanbul Pay Piyasası işleyişi; plan §3).

## 5. Günlük (her akşam, 5 dk)

- Her işlem için bir satır (§8.2): son_fiyat_18:00, emir aşaması, kayma, kilit, R, R_fazla, kural_sapmasi.
- NAV iki satır tutulur: çekirdek ve uydu.
- Sinyal çıktısı ve `viop_YYYYMMDD.csv` arşivlenir.

## 6. Haftalık ve takvim

| Ne zaman | İş |
|---|---|
| Perşembe 14:30 sonrası | TCMB swap hariç net rezerv, brüt rezerv ve yabancı DİBS akımı `makro.json`'a. Bunlardan M1, K6 kapısı ve KRİZ (d) güncellenir. **12.11'de haftalık değişim yine ≤ −5 mlr $ ise KRİZ (d) tetiklenir** |
| Ayın 3'ü 10:00 sonrası | TÜFE `makro.json`'a (M2) |
| Cuma 18:30 (~45 dk) | Stres, açık risk, L1. Dışlama listesi (VBTS, SPK, MSCI). KAP taraması: temettü, bedelsiz, ZPAT ve "Esas Alınan Tarih" (K3, K3b, K5, A5, A6). Mevduat dilimi, şartlı emirler |
| Dilim Pazartesileri | Mevduat 16.11, 23.11 ve 30.11. 30.11 dilimi 35 gün vadeli açılır (04.01.2027) |
| Ay sonu | T2, küme 12 ay RS sırası (K7), aylık rapor (§8.5–8.6) |
| Kasım'ın özel günleri | 9.11 bilanço gecesi (A1). 11.11 hiç giriş yok. 12.11: 07:00 MSCI, 14:30 rezerv, akşam SPK bülteni. 11–13.11 K3/K4/K5/K9 girişi yok (A2). 13.11 kredili esneklik (A4). 25.11 Kasım vadelileri. 30.11 vade, MSCI yürürlüğü, ay sonu |

**`makro.json` (05.11 değerleri; elle güncellenir):**

```json
{"kaynak": "elle, 05.11.2026", "politika_faizi": 36.0, "mevduat_32g_brut": 39.52,
 "net_rezerv_swap_haric": [["onceki hafta", 30.8], ["son hafta (5.11 yayini)", 24.3]],
 "brut_rezerv": 158.1, "yabanci_dibs_hafta_mn_usd": -750,
 "tufe_aylik": [["2026-10", 2.58]], "cds5y": 248, "cds5y_20g_once": null, "cds_teyitli": false,
 "msci_danisma": false, "kural0": false, "komisyon_viop_bps": null, "usd_faiz": 0.039}
```

Rezerv listesine her Perşembe yeni hafta eklenir. M1 için en az 4 seviye gerekir (3 hafta üst üste artış); KRİZ (d) son iki haftalık değişime bakar.
