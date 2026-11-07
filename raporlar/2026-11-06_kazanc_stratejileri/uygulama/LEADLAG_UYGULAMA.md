# Lead-lag uygulama kartları: BIST TRADE/İZLE ve ABD Tier A (06.11 kapanışı → Pazartesi 9.11)

_08.11.2026 · profil: karar BIST kapanışında 18:00–18:15 TSİ, VİOP'ta 1–3 gün kapanıştan kapanışa, gün içi ekran yok; ABD'de emir 16:45–17:15 TSİ · yatırım tavsiyesi değildir_

**Kaynaklar** (yollar `raporlar/` köküne göre):
- Hesap raporları: [LB] `2026-11-06_kazanc_stratejileri/ajanlar/leadlag_bist_uygulama.md` (Ek A: kart sürücülerinin tamamı etiketli; Ek B: test tabloları) ve [LA] `…/ajanlar/leadlag_abd_uygulama.md`.
- Planlar ve listeler: [NB] `…/uygulama/NET_LISTE_BIST.md`, [NA] `…/uygulama/NET_LISTE_ABD.md`, [PB] `PLAN_BIST.md`, [PA] `PLAN_ABD.md`, [TVA] `…/uygulama/TRADINGVIEW_ALARMLARI.md`.
- Önceki çalışmalar: [LL] `2026-11-02_viop_leadlag/RAPOR.md` ve `hisse_kartlari/`; [PL] `2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md`; [RH-T/K/A] aynı klasörde `rehber/{tuprs,koza,altin}/`.
- Kod: `…/hesaplar/leadlag_uygulama/` ve `…/abd/`. Ham veri repo dışında: scratchpad `data/leadlag2/`.

**Ana sonuç:**
- Kapanıştan kapanışa ve maliyet sonrası **yeni** bir lead-lag kenarı çıkmadı.
- KENAR etiketli satırların hepsi önceden bilinen kurallar. Bunlardan yalnız **TUPRS ← ABD rafinerileri** gerçek bir lead-lag (ABD t−1 bilgisi BIST t kapanışında hâlâ işlenebilir). Diğerleri lead-lag değil: XU030 bazı mikroyapı, K1 ortalamaya dönüş, Koza göreli momentum, altın eksik aynı gün tepkisi, kredi notu olay.
- Yeni testlerden tek aday **RYGYO → RYSAS**; FILTRE düzeyinde kaldı (kural bağımsız olarak yeniden üretildi, §1.7).
- ABD Tier A'da KENAR yok. Test edilmiş tek FILTRE: hastaneler (`NYSE:HCA`) → `NYSE:BDX` önceliği (FDR'den geçmiyor).

**Etiketler:**
- **KENAR:** test edildi, bu zamanlamada maliyet sonrası ayakta.
- **FILTRE:** gerçek ilişki ama tek başına kenar değil; zamanlama, boyut ya da kaçınma için.
- **RISK:** bilgi açılış gap'inde ya da t gününün içinde fiyatlanıyor.
- **YOK:** test edildi, bir şey yok.
- **TEST EDİLMEDİ:** veri ya da kanıt yok.

**Zaman kuralı:**
- ABD günü d'nin kapanışı **00:00 TSİ**'de kesinleşir (kış saati 01.11.2026–14.03.2027). Bu bilgi d'den sonraki ilk BIST gününün kapanışında kullanılır.
- ABD'nin aynı günkü seans hareketiyle sinyal üretilmez [RH-T §3].
- Gece sürücüleri (`CME_MINI:ES1!`, `CME_MINI:NQ1!`, `NASDAQ:TUR`, `TVC:NI225`, gece Brent ve altın) açılışta fiyatlanır. Bunlar yalnız RISK'tir [LL §2].
- **9.11'e özel:** Kural 0'ın yazılı cevabı yok, bu yüzden bütün VİOP kolları **kâğıtta**; yalnız spot kollar (burada K4) canlı açılabilir. A1 gereği bilançosu 9.11 18:00'e kadar gelmemiş isimde giriş ya da taşıma yok. BIST rejimi KAPALI.
- **Risk bütçesi (plan):** Eski dört lead-lag sinyali ([PL] §1: XU030 bazı, TUPRS, Koza; SAHOL/AKBNK 1–3G K1'e devredildi) canlıya geçerse **hepsinin toplam açık riski ≤ %0,5** ve bu bütçe K4 sondalarından düşülür. Bunlar **K9 bütçesi değildir** [PB K9 "Eski lead-lag sinyalleri", §3.11]. Bu dosyadaki boylar işlem başına ~%0,25 varsayar (aynı anda iki sinyal sığsın diye). [TVA] §0'daki "bu sinyaller K9 kanalıdır" ifadesi plana aykırı. K9 yalnız plan dışı yeni fikirler içindir: fikir kartı 18:45'e kadar, **emir ertesi gün**, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli. Altın → TRALT ve kredi notu [PL]'de "düşük güvenli" listede, dörde dahil değil (NB: IZLE). Altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz → **yalnız kâğıt**. Kredi notu canlıya ancak K9'dan girebilir: fikir kartı tepki gününden önce yazılır, stop zorunlu, risk ≤ %0,25, ayrıca Kural 0 şart. RYGYO → RYSAS'ın canlı kanalı yok (§1.7).
- ABD rejimi KIRMIZI; ilk pilot en erken Pt 16.11, yalnız 13.11 kapanışında SARI olursa [NB §1, §5; NA §0; PA §7.2].

## 0. Özet

| Enstrüman | En iyi ilişkinin etiketi | Lider ticker(lar) | Eylem |
|---|---|---|---|
| **TUPRS** `BIST:TUPRS1!` (F_TUPRS1226) | **KENAR** | `NYSE:VLO`, `NYSE:MPC`, `NYSE:PSX`, `NYSE:PBF` − β·`SP:SPX` (ABD önceki gün) | 08:30–10:00 `sinyal_tuprs.py` ya da ~10:00–10:15 `tuprs_alarm.pine` alarmı. \|z\| > 1 ise aynı gün 18:00–18:10 z yönünde 1 kontrat, t+2'de kontrol. 9.11 kâğıt |
| **XU030 vadeli baz** `BIST:XU030D1!` | **KENAR** (mikroyapı, lead-lag değil) | Kendi bazı: `BIST:XU030D1!/BIST:XU030` | 18:10–18:15'te \|Δb\| > std120 (06.11: 68 bps) ise ters yönde 1 kontrat; ertesi gün uzlaşmada çık. 9.11 oran < 1,0343 AL, > 1,0484 SAT (kâğıt). yeni şok olmazsa std120 ~17.11'den itibaren ~42 bps'e iner; seviyeleri her akşam yeniden hesapla (§1.2) |
| **SAHOL/AKBNK K1** | **KENAR** (çift, 20 gün; lead-lag değil) | Öncü yok. `BIST:AKBNK` → SAHOL yalnız zayıf FILTRE | Oran ≥ 1,3556: ertesi gün 17:55 F_SAHOL SAT + F_AKBNK AL. ≤ 1,2249: tersi. 8 + 10 Aralık kontratı, 20 gün. Kural 0 ve ≤ 5 bps komisyon gelene kadar kâğıt |
| **ENJSA** `BIST:ENJSA` | **YOK** (öncülük); gece **RISK** | `CME_MINI:ES1!` gece (yalnız gap) | K4: kapanış > 127,00 (şablon ve RS ≥ 80 sürüyorsa) ise ertesi gün 18:01–18:05 spot, ~131 lot |
| **ENERY + AHGAZ** | **YOK** (öncülük); senkron **FILTRE** | Birbirleri, `BIST:XELKT` (aynı gün) | K4: 14,60 / 48,70; ikisinden yalnız biri; en erken 16.11 |
| **KCHOL** `BIST:KCHOL` | **YOK** (öncülük); gece **RISK** | `CME_MINI:ES1!` gece; senkron `BIST:ARCLK`, `BIST:FROTO`, `BIST:TOASO` | K4: kapanış > 225,50 ve > SMA50 210,94; en erken 16.11 |
| **RYSAS** `BIST:RYSAS` | **FILTRE** (kenar adayı) | `BIST:RYGYO` (t kapanışı → RYSAS t+1) | K4 30,28, en erken 16.11 (A4 uygulanırsa 30.11). Giriş günü RYGYO z < −1 (≈ −%3) ise o akşam girme. Kural ayrıca yalnız kâğıtta izlenir (canlı kanalı yok) |
| **BRSAN** `BIST:BRSAN` | **YOK** (öncülük); gece **RISK** | `BIST:BRYAT` (senkron) | K4: 769,50 **ve** dizilim (bugün ✗), stop %25, ~12 lot |
| **Koza** `BIST:TRMET1!` / `BIST:TRALT1!` | **KENAR**, sönmüş → kâğıt (lead-lag değil) | `BIST:TRALT`, `BIST:TRENJ` (grup artığı) | 17:50–17:55'te z3 > +1,5 ise TRMET1! AL + TRALT1! SAT (1:2). 9.11 tetiği TRMET ≥ 116,76 / ≤ 105,54; A1 nedeniyle canlı yok |
| **Altın → TRALT** `BIST:TRALT1!` | **KENAR** (DÜŞÜK) | `TVC:GOLD` 17:55 | \|g\| > %1,70 ise TRALT1! z yönünde (18:00–18:10) + XU030D1! ters (aynı anda; endeks uzlaşması ~18:05–18:15), 1 XU030D1! : 29 TRALT1!, 2 gün; yalnız kâğıt |
| **Kredi notu → F_XU030** `BIST:XU030D1!` | **KENAR** (DÜŞÜK, olay; n = 16, çoklu testten sonra p ≈ 0,14, yani istatistik eşiğini geçmiyor) | Not kararı (ticker değil) | Tepki günü uzlaşmasında (~18:05–18:15) kararın tersine, 2 gün. Kâğıt; canlı yalnız K9 + Kural 0. Takvim teyit edilmeli |
| **BDX** `NYSE:BDX` | **FILTRE** | `NYSE:HCA` (LL_z, L 5; kontrol `NYSE:UHS`) | S1/S2 hazır ve LL_z > +1 ise sağlık hakkı BDX'e. Rejim KIRMIZI → en erken 16.11 |
| **EHC** `NYSE:EHC` | **YOK** (öncülük); olay **RISK** | `NYSE:HCA`, `NYSE:UHS`, `NYSE:THC`, `NYSE:UNH` (bilanço günleri) | Kendi S1. CMS ve emsal bilanço haftasında ertele |
| **TW** `NASDAQ:TW` | **YOK**; rapor günü **RISK** | `TVC:MOVE` (bağlam, TEST EDİLMEDİ); aylık hacim raporları (RISK) | Kendi S1. Rapordan önceki kapanışta yeni tetik koyma |
| **ACGL** `NASDAQ:ACGL` | **YOK** (sektörde); afet **RISK** | `NYSE:BRK.B` (9.11 tepkisi), `NYSE:RNR` | Kendi S1. Afetten sonraki ilk seansta giriş yok |
| **MAR** `NASDAQ:MAR` | **YOK**; tüketici emsali **RISK** | `NYSE:DAL`, `AMEX:JETS` (YOK); tüketici bilançoları (RISK) | Kendi S1, tetik FTD ya da S&P 10 > 20. 17.11 plan yasağı; 18–19.11 emsal günlerinde ertele [Ö] |
| Yedekler TMO, RPRX, CME, MRSH, HLT, SN | YOK / RISK | §3.6 | Kendi kuralı; `NASDAQ:HLT` (NYSE değil) |

---

## 1. BIST kartları

### 1.1 TUPRS: ABD rafinerileri → F_TUPRS (KENAR)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:TUPRS` / VİOP `BIST:TUPRS1!`. Canlıda F_TUPRS1226 (A10: Kasım vadesi yeni pozisyonda yok; rehber 25.11'e kadar 1126 diyor, plan geçerli). **1-3G TRADE (mini)**, [PL #4] / [RH-T] |
| Lead-lag (lider → yön) | `NYSE:VLO`, `NYSE:MPC`, `NYSE:PSX`, `NYSE:PBF`, ABD önceki günün piyasa artığı → TUPRS, **aynı yön** |
| Formül | r_i = ln(adj_t/adj_t−1). β_i: 250 ABD günü cov(r_i, r_SPX)/var(r_SPX), o gün hariç, ≥ 100 gözlem. P = ort(r_i − β_i·r_SPX), en az 3 hisse dolu. z = P / std(P, önceki 250 BIST günü) |
| Eşik | \|z\| > 1 |
| Ne zaman bilinir (TSİ) | ABD d kapanışı 00:00. Okuma 08:30–10:00 (`sinyal_tuprs.py`; alarm BIST açılışında ~10:00–10:15) |
| Ne yapılır | Aynı BIST günü 17:45'te kademe ve limite yakınlık kontrolü. 18:00–18:09'da F_TUPRS'ta z yönünde limitli emir (karşı kademe; 3+ kontratta 2–3 parça). **Hedge yok** (XU030 hedge'i işe yaramıyor) [PL §3]. t+2 sabahı z yeniden: aynı yönde \|z\| > 1 ise UZAT, ters ise ÇEVİR, değilse 18:00–18:10'da KAPAT. Ara günlerde (t+1) yeni sinyale bakılmaz. **Stop:** test edilmedi; koruma boyuttur. **Boy (1 mn TL):** 1 kontrat (kontrat başı risk ≈ 2.057 TL → ~%0,2); rehber %0,5 → 2. Eski lead-lag sinyallerinin toplam açık riski ≤ %0,5 (K9 bütçesi değil) [PB §3.11; NB §1.2]. **Yapılmaz:** ABD tatili ertesi (27.11), işlem yönünde limit kilidi, kaçırılan pencere (ertesi gün girilmez), sepet değişikliği |
| Etiket | **KENAR**; 2024–26'da sönük → mini boy, Kural 0 cevabına kadar kâğıt |
| Kanıt | Net **+42 bps/işlem** (8 bps maliyet, t 2,72); 15 bps ile +35. IS +34,5 / OOS +48,8 (t 2,12). **2024–26 +26 (t 1,0)**. En iyi 10 işlem çıkınca t 1,45. ~53 işlem/yıl. En kötü tek pozisyon −%16,9. Tem–Eki 2026 en derin düşüş (fon krizinde 8 pozisyon ort. −165 bps) [NB §1.2; RH-T §7–8] |
| Pine / TradingView | `2026-11-04_kapanis_1-3gun/rehber/tuprs/tuprs_alarm.pine` → `BIST:TUPRS1!` 1G grafiği, ≥ 600 bar. Alarm "TUPRS herhangi bir kural olayı", **Bar başına bir kez** [TVA §2]. Derlenmedi: son 10–20 günü betikle karşılaştır, fark > 0,05 ise betik esas. Görsel bağlam (sinyal değil): `(NYSE:VLO+NYSE:MPC+NYSE:PSX+NYSE:PBF)/4`, `AMEX:CRAK/SP:SPX`, `ICEEUR:BRN1!`. Son 250 günde β'lar negatif (ort. −0,48), bu yüzden SPX'e oran grafiği sinyali yanlış gösterebilir |
| Güncel | **Hesaplanmadı:** izinli kaynakta ABD tek hisse serisi yok (Yahoo ve Stooq kapalı). 9.11 sabahı Pine'dan okunacak (ABD Cuma 6.11). 03.11 kısa pozisyonunun (z −1,47) 05.11 UZAT/KAPAT kararı dosyalarda yok → betikle kontrol. TUPRS bilançosunun açıklandığını KAP'ta teyit et (A1). 06.11: F_TUPRS1226 uzlaşma 354,65 (106 mn TL, AP 3.403). Bağlam: S&P 5.11 −%4,36; VIX 6.11 25,64 |

**Yan ilişkiler:**

| Lider | Yön | Etiket | Kanıt | Kullanım |
|---|---|---|---|---|
| `AMEX:XLE` − β·`SP:SPX`, ABD t−1 (test: FF49 Oil artığı) | aynı | **FILTRE** | +15,8 bps/1σ, NW t 3,96 (IS 2,09 / OOS 3,10 / 2024+ 1,69), q 0,003. Tek başına işlem (15,5 bps) net +11 (t 1,0); IS −6 | Rafineri z'si ile ters işaretliyse boyutu yarıya indir. Bu kombinasyon **TEST EDİLMEDİ**. Vekil: `ll_z_filtre.pine`, girdiler Öncü `AMEX:XLE`, L = 1, `AMEX:XLE` 1G grafiğinde dünkü bar (derlenmedi) |
| `ICEEUR:BRN1!`, ABD t−1 | aynı | YOK | t 2,23, q 0,19; net −1,9 | — |
| `ICEEUR:BRN1!` gece, `CME_MINI:ES1!` gece | aynı | RISK | Brent gece → gap corr 0,577 | Yalnız açılış beklentisi |
| `BIST:AYGAZ`, `ICEEUR:BRN1!` (senkron) | aynı | FILTRE | pc 0,278 / 0,158 | Konum, küme |

### 1.2 XU030 vadeli kapanış bazı sıçraması (KENAR; mikroyapı, lead-lag değil)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:XU030D1!` = F_XU0301226 (vade 31.12). **1-3G TRADE (mini)**, [PL #1] |
| Lead-lag (lider → yön) | Lider yok; kendi bazının günlük değişimi → **ters yön** |
| Formül | b = ln(F_XU0301226 18:10 son fiyat / XU030 spot kapanış). Δb = b − dünkü b (aynı vade; devir günü sinyal yok). z = Δb / std120(Δb) |
| Eşik | \|Δb\| > 1·std120. 06.11'de std120 = **68 bps** (VİOP bülteni, 150 gün; NB'deki "~50"den yüksek). **Dikkat (08.11 kontrolü, `xu030_baz.csv`):** 68 bps tek bir şoktan şişiyor: 21.05.2026 Δb −458 bps, 22.05 +352 bps (F_XU0300626 bir günde ~−%10, spot −%5,8). Bu iki gün hariç std ≈ **42 bps** (MAD-σ 38). 21.05, 7 seans sonra (~17.11) 120 günlük pencereden çıkar; 22.05 bir gün sonra. Ondan sonra eşik ~42 bps olur. Seviyeleri her akşam std120'den yeniden hesapla; sabit 50 de sabit 68 de yanlış olur |
| Ne zaman bilinir (TSİ) | 18:08–18:10 (spot kapanış). Yalnız 18:08–18:15 arasındaki değer geçerli |
| Ne yapılır | Vadeli ucuz kapandıysa (Δb < −68) AL, pahalıysa (Δb > +68) SAT. Giriş 18:10–18:15 limitli; çıkış ertesi gün uzlaşmasında. Aynı akşam yapılmazsa hiç yapılmaz (1 gün geç giriş −2,5 bps). **Stop:** yok (1 gün). **Boy:** 1 mn TL'de en çok 1 kontrat (~149 bin TL nominal). Canlı BIST + VİOP verisi şart |
| Etiket | **KENAR** |
| Kanıt | Net **+14…+20 bps/işlem** (~5 bps maliyet; brüt son fiyattan +25, uzlaşmadan +19). IS +24 / OOS +25 (t 1,85). **2024–26 +17 (t 1,1)**. Eğim −0,76 → −0,27 (sönüyor). Yalnız alım tarafı +28,5 (t 2,9). ~65 işlem/yıl [NB §1.1]. Maliyet 10–15 bps olursa net ≈ +4…+15 (hesap: brüt − maliyet); bireysel komisyonla kenar büyük ölçüde gider [PL §5] |
| Pine / TradingView | Pine yok. Oran sembolü `BIST:XU030D1!/BIST:XU030` (ya da `BIST:XU030DZ2026/BIST:XU030`), 1 dk. İki fiyat alarmı, **Yalnızca bir kez**, bitiş ertesi gün 18:16 [TVA §6]. 15 dk gecikmeli veriyle uygulanamaz |
| Güncel | 06.11: b +405 bps, Δb **−41 bps** → z −0,61, sinyal yok. **9.11 seviyeleri (std120 = 68 bps):** oran < **1,0343** ise AL, > **1,0484** ise SAT (06.11 spotu 14.290 ile F ≤ 14.781 / ≥ 14.982; 9.11'de spot değişeceği için oranı kullan). **Dikkat:** günlük rapor ve [TVA] sabit 50 bps ile 1,0361 / 1,0466 veriyor; kural std120 dediği için 9.11'de 68 bps'lik seviyeleri kullan, ~17.11'den sonra ~42 bps'e göre yeniden kur. Vade geçişinden (31.12) önceki ve sonraki gün alarm kurma [TVA §6] |

Küresel bağ: `CME_MINI:ES1!` gece → XU030 gap 0,45–0,47 → **RISK**. Akşam seansı hareketinin ertesi güne öngörüsü yok (corr −0,04) [PL §2].

### 1.3 SAHOL / AKBNK, K1 (KENAR; çift, 20 gün)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:SAHOL1!` / `BIST:AKBNK1!`; işlemde Aralık kontratları `BIST:SAHOLZ2026`, `BIST:AKBNKZ2026`. **SWING TRADE (K1)**, [PB K1] |
| Lead-lag (lider → yön) | Ortalamaya dönüş; lider yok. Oran yükselince SAHOL SAT + AKBNK AL (**oranın tersi**) |
| Formül | x = ln(SAHOL) − ln(AKBNK); z = (x − ort60) / std60, bugün dahil |
| Eşik | z ≥ +2 ya da z ≤ −2 |
| Ne zaman bilinir (TSİ) | t kapanışı, 18:15 sonrası (`bist_sinyal.py`) |
| Ne yapılır | **Ertesi gün:** 17:50'de bir bacak gün içinde ±%9'un ötesindeyse giriş yok. 17:55'te iki bacak limitli (karşı en iyi ± %0,3); 18:05'te dolmayan bacak ± %0,6. 18:08'de tek bacak kaldıysa β × nominal ters F_XU030 açılır; ertesi gün ikisi birlikte kapatılır. **Çıkış:** 20. işlem günü (z ne olursa olsun). **Felaket stopu:** çift K/Z ≤ bacak nominalinin −%8'i. **Vade:** doğrudan Aralık; Aralık bacakları en geç 23.12'de devredilir ya da kapanır (A10). 29.01–05.02.2027 yeni giriş yok (A9). **Boy:** bacak başına %7,5 → **8 F_SAHOL1226 + 10 F_AKBNK1226** (stop riski ≈ %0,6). **Kapılar:** Kural 0; komisyon ≤ 5 bps/bacak/yön |
| Etiket | **KENAR** |
| Kanıt | 1 gün gecikmeyle **+160 / +310 bps/işlem** (2010–18 / 2019–26), t 2,4 / 2,8; 20 bps ile ~+140 / +290 [VB #25]. Seçim yanlılığı var. Plan beklentisi net +80…+180, ~5 işlem/yıl |
| Pine / TradingView | Oran sembolü `BIST:SAHOL/BIST:AKBNK` 1G. İki fiyat alarmı, **Bar kapanışında bir kez**: ≥ 1,3556 ve ≤ 1,2249 (seviyeler her akşam rapordan güncellenir). Pine'sız yol: Bollinger (60, 2). `kod/sahol_akbnk_z.pine` β250 kullanıyor → yalnız alarm, karar betikten |
| Güncel | 06.11 z **−0,54** (oran 1,2717). Tetikler (öbür bacak sabitken): z = +2 için SAHOL ≥ 93,06 ya da AKBNK ≤ 64,40; z = −2 için SAHOL ≤ 84,09 ya da AKBNK ≥ 71,27 |

**Yan ilişkiler:**

| Lider | Yön | Etiket | Kanıt | Kullanım |
|---|---|---|---|---|
| `BIST:AKBNK`_t → SAHOL t→t+1 | aynı | FILTRE (zayıf) | +22,4 bps/1σ, t 2,96, q 0,03. Tek bacak F_SAHOL net −4,6 bps | K1'e dokunma (≈11 bps, K1 ise 140–290) |
| `SP:SPX` t−1 → SAHOL; `CBOE:VIX` → AKBNK | — | YOK | t 0,66 / −1,27 | — |
| `CME_MINI:ES1!` / `NQ1!` gece, `NASDAQ:TUR`, `TVC:NI225` | aynı | RISK | ES → gap 0,47 | Yalnız gap beklentisi |
| `TVC:TR05Y`, `BIST:USDTRY1!` (senkron) | ters | FILTRE | AKBNK pc −0,157 / −0,166 | Boyut; PPK (A7) |

### 1.4 ENJSA (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:ENJSA` (spot); VİOP `BIST:ENJSA1!` ince (likidite C). **IZLE → SWING K4**, kümede öncelikli |
| Lead-lag | **Islenebilir lead-lag yok.** En yakın bağ `CME_MINI:ES1!` gece → açılış gap'i (RISK) |
| Formül (alternatif: K4) | Kapanış > önceki 252 günün en yüksek kapanışı + trend şablonu + RS ≥ 80 |
| Eşik | Kapanış > **127,00** (+%4,1) |
| Ne zaman bilinir (TSİ) | t kapanışı 18:10 |
| Ne yapılır | t+1 kapanış seansında 18:01–18:05 spot limitli; limit = min(t kapanışı × 1,06; P_son × 1,03). **Çıkış:** kapanış ≤ en yüksek kapanış × 0,85 ise ertesi kapanışta sat; süre 120 gün. **Boy:** risk %0,25 / stop %15 → 16.667 TL ≈ 131 lot. ENJSA, ENERY ve AHGAZ'dan en çok 1 pozisyon. **Takvim:** 9.11 sinyali → 10.11 girişi; 10.11 sinyali → 11.11 yasak (A2) → 16.11 ya da 23.11 (A4) |
| Etiket | Öncülük **YOK**; gece **RISK**; kapanış müzayedesi **FILTRE** (yalnız spot yürütme) |
| Kanıt | ES/NQ gece → gap 0,21–0,25; E.ON pc 0,03, TTF 0,007. Yeni: ENERY_t / AHGAZ_t → ENJSA t+1: t −1,91 / −1,71, q 0,29 / 0,37 (YOK). Aynı gün artık bağ ENERY 0,05, AHGAZ −0,01. Kendi kapanış müzayedesi hareketi ertesi sabah geri dönüyor (açılış → 10:30 TSİ b −0,58, t −4,3, FDR): müzayedede sert yükselen günde kapanıştan alma (eşik tanımı yok; K4 ile birlikte test edilmedi). K4 kanıtı: rastgele hisseye göre +%5,3 (t 5,1), ama KAPALI rejimde katkı ≈ 0 [PB K4] |
| Pine / TradingView | Kapanış alarmı: "`BIST:ENJSA` kapanış > 127,00, Bar kapanışında bir kez". Küme bağlamı: `BIST:XELKT`, `BIST:AKSEN`. Risk: `CME_MINI:ES1!` |
| Güncel | 06.11: 122,00. F_ENJSA1226 124,35 (spota göre +%1,9). Kasım vadelisinin ima faizi anormal (−%6,2) → KAP'ta temettü ya da sermaye işlemi kontrol et (K3/A6) |

Plan için not: Ölçülen bağ çok zayıf (0,05 / −0,01). Bu yüzden ENJSA ile ENERY/AHGAZ ayrı küme sayılabilir; karar planın, bu dosya kuralı değiştirmiyor [LB §3.4].

### 1.5 ENERY + AHGAZ, tek isim (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:ENERY` ([TV] CSV), `BIST:AHGAZ` (CSV'de yok; 08.11'de TradingView sembol sayfasından doğrulandı) (spot; VİOP yok). **IZLE → SWING K4**, ikisi tek isim sayılır |
| Lead-lag | **Islenebilir lead-lag yok.** Bağ yalnız senkron: birbirleri ve `BIST:XELKT` |
| Formül (alternatif: K4) | §1.4'teki K4 kuralı |
| Eşik | ENERY > **14,60** (+%3,9), AHGAZ > **48,70** (+%4,0) |
| Ne zaman bilinir (TSİ) | t kapanışı 18:10 |
| Ne yapılır | K4 girişi t+1 18:01–18:05 spot limitli. **Boy:** VİOP-47 dışı × 0,75 → 12.500 TL (ENERY ≈ 856 lot, AHGAZ ≈ 256 lot). İkisi aynı gün tetiklerse likidite sırası yüksek olan alınır; ENJSA ile birlikte en çok 1 pozisyon. **Takvim:** bilanço 9.11 akşamı → ilk karar 10.11 → giriş en erken 16.11; A4 uygulanırsa (esneklik uzatılmazsa) VİOP-47 dışı long 30.11'den önce yok. Aktif ihraççı geri alımı yalnız bayrak |
| Etiket | Öncülük **YOK**; senkron **FILTRE** |
| Kanıt | 18 öngörü testinde en iyi \|t\| 1,87 (AKSEN → ENERY), q ≥ 0,29. Bütün \|z\| > 1 kuralları maliyet sonrası negatif (−3 … −62 bps). Aynı gün ENERY–AHGAZ artık korelasyonu **0,61** (son 1 yıl 0,63) → "tek isim" kuralını doğruluyor. `BIST:XELKT` 0,46 / 0,41. Henry Hub → ENERY gap günü 0,098 (RISK, zayıf). Örneklem kısa (2023+); "YOK" küçük bir etkiyi dışlamıyor |
| Pine / TradingView | Kapanış alarmları `BIST:ENERY` > 14,60 ve `BIST:AHGAZ` > 48,70. Oran grafiği `BIST:ENERY/BIST:AHGAZ` (yalnız hangisinin önde olduğunu görmek için). Bağlam: `BIST:XELKT`, `BIST:XUTUM/BIST:XU100` |
| Güncel | 06.11: ENERY 14,05 (+%1,81), AHGAZ 46,82 (+%1,78) |

### 1.6 KCHOL (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:KCHOL`; VİOP `BIST:KCHOL1!` (F_KCHOL1226 215,70). **IZLE → SWING K4**; K2 KCHOL↔sepet kâğıtta |
| Lead-lag | **Islenebilir lead-lag yok.** Gece ES/NQ, `NASDAQ:TUR` ve `TVC:NI225` → gap (RISK). İştirakler yalnız senkron |
| Formül (alternatif: K4) | K4 kuralı + kapanış > SMA50 şartı |
| Eşik | Kapanış > **225,50** (+%9,4) **ve** > SMA50 **210,94** |
| Ne zaman bilinir (TSİ) | t kapanışı 18:10 |
| Ne yapılır | K4 girişi t+1 18:01–18:05 spot limitli. **Boy:** 16.667 TL ≈ 73 lot. **Takvim:** bilanço 9.11 → en erken giriş 16.11. K4 spot ve hedge'sizdir; `BIST:XU030D1!`'in KCHOL'de iyi hedge olması [PL §3] yalnız VİOP kolları için bilgi (Kural 0'a bağlı), K4'e hedge eklemek plan dışıdır. K2 yalnız yeni \|z\| ≥ 2 kesişiminde, ≥ 5 mn TL hesap ve ≤ 8 bps komisyonla |
| Etiket | Öncülük **YOK**; gece **RISK**; iştirakler **FILTRE** |
| Kanıt | ES gece → gap 0,49. VIX_t−1 → cc −0,085 (yalnız gap kanalı). Yeni: `SP:SPX` t−1 → KCHOL t+1 +4,1 bps/1σ, t 0,86 (YOK). İştirak_t → KCHOL_t+1 ≈ 0. NAV iskontosu VİOP fiyatıyla t 1,0–1,5 (YOK) |
| Pine / TradingView | Kapanış alarmı `BIST:KCHOL` > 225,50 (SMA50 göz kontrolü). Göreli değer: `BIST:KCHOL/BIST:ARCLK`, `BIST:KCHOL/BIST:FROTO`, `BIST:KCHOL/BIST:SAHOL`. Risk: `CME_MINI:ES1!` |
| Güncel | 06.11: 206,10 |

### 1.7 RYSAS: RYGYO → RYSAS (FILTRE, kenar adayı; yeni)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:RYSAS` (spot; VİOP yok; kod 08.11'de doğrulandı). **IZLE → SWING K4** |
| Lead-lag (lider → yön) | `BIST:RYGYO`'nun t kapanış getirisi → RYSAS t→t+1, **aynı yön**. Grup iştiraki; 19 GYO plasebosunda \|t\| > 2 olan yok, yani bağ RYGYO'ya özgü |
| Formül | z = ln(RYGYO_t / RYGYO_t−1) / sd250(önceki gün dahil), ±5'te kırpılır |
| Eşik | \|z\| > 1. 9.11 için: RYGYO kapanışı ≥ **50,61** (z > +1) ya da ≤ **47,63** (z < −1) |
| Ne zaman bilinir (TSİ) | 18:08–18:10, RYGYO kapanışı |
| Ne yapılır | **(a) K4 filtresi** (asıl kullanım): K4 RYSAS girişi tetik 30,28 ile t+1'de (boy 12.500 TL ≈ 412 lot, VİOP-47 dışı × 0,75). Giriş günü RYGYO z < −1 ise o akşam girme. Ertesi gün K4'ün kaçan giriş kuralıyla, yani yalnız koşullar sürüyorsa denenir [PB K4 "Giriş"]. z > +1 ise kural değişmez. K4 emri 18:01–18:05'te verildiği için RYGYO kapanışı o anda bilinmez: 17:55'teki canlı değişimini (≤ −%3) vekil al ya da planın "geç" yolunu kullan (18:08–18:10 kapanış fiyatından emir; günlüğe "geç" yaz). Bu kullanım K4 ile birlikte **TEST EDİLMEDİ**. **(b) Yalnız kâğıt kural** (2–3 ay): z > +1 → RYSAS'ı 18:10–18:15 kapanış fiyatından işlemler seansında al (z < −1'de işlem yok), ertesi kapanışta sat; XU030 hedge'i isteğe bağlı; stop yok (1 gün). **Canlı kanal yok:** plan dışı fikir yalnız K9'dan açılır, K9 ise yalnız VİOP-47 hissesine izin verir (RYSAS değil) ve emri ertesi güne atar. 1 gün geç giriş −15,8 bps, yani K9 süreciyle kenar sıfırlanır. Canlıya almak plan değişikliği ister |
| Etiket | **FILTRE** (kenar adayı) |
| Kanıt | Öngörü: +32,7 bps/1σ, NW t 3,15 (IS 1,30 / OOS 2,53 / 2024+ 3,17), q 0,02 (38 test). Kural (25 + 3 bps): net **+34,8 bps (t 2,40)**, OOS +56,5 (t 2,98), **2024–26 +97,5 (t 3,92)**, 2014–20 +14,6 (t 0,67). Yalnız uzun (hedge'li) +56,0 (t 2,80). **Zayıf yanlar:** en iyi 10 işlem çıkınca +13,6 (t 1,04); 2014–23'te t < 0,7; **1 gün geç giriş −15,8** (bilgi tek günde tükeniyor); KFİ seansının derinliği gözlenmedi. **Bağımsız tekrar (08.11, aynı İş Yatırım önbelleği, ayrı kod):** kural n 792, brüt +62,5, net +34,5 (t 2,37); 2014–20 +14,6 (t 0,67), 2024–26 +97,4 (t 3,92); yalnız uzun +55,3 (t 2,77). Kural tutuyor. Regresyonda lider ham getiri yerine σ-normalize z alınınca NW t 3,15 → 2,8 (IS katsayısı +7 / OOS +38 bps): etki yine OOS'a yığılı |
| Pine / TradingView | Pine yok. `BIST:RYGYO` üzerinde iki fiyat alarmı (≥ 50,61 / ≤ 47,63), **Bar kapanışında bir kez**; seviyeler her akşam `03_guncel.py`'den güncellenir (= kapanış × e^(±sd250); sd250 bugün %3,03). Gecikmeli veriyle alarm 18:25'te gelir, yani KFİ penceresi kaçar. Grafik: `BIST:RYSAS/BIST:RYGYO`. Bağlam: `BIST:XGMYO`, `BIST:XULAS` (öngörü YOK) |
| Güncel | 06.11: RYGYO 49,10 (+%0,69) → z +0,23, sinyal yok. RYSAS 27,34; K4 tetiği 30,28 (+%10,8). Bilanço 9.11 akşamı → 9.11'de giriş yok. K4 girişi en erken 16.11; A4 uygulanırsa 30.11 |

### 1.8 BRSAN (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:BRSAN`; VİOP `BIST:BRSAN1!` ince (F_BRSAN1226 705,30, AP 317). **IZLE → SWING K4** |
| Lead-lag | **Islenebilir lead-lag yok.** Asya çeliği (`ASX:FMG`, `TSE:5411`) gün içinde t 3,5 veriyor ama kazanç ilk 30 dakikada bitiyor (RISK). Metal akranlarının gap'i ve kendi gap fade'i açılış emri ister (YOK) |
| Formül (alternatif: K4) | K4 kuralı (7 koşulun hepsi) |
| Eşik | Kapanış > **769,50** (+%12,8) **ve** dizilim (kapanış > SMA50 > SMA150 > SMA200). Dizilim bugün ✗ (şablon 4/5), yani fiyat tek başına yetmez |
| Ne zaman bilinir (TSİ) | t kapanışı 18:10 |
| Ne yapılır | K4 girişi t+1 18:01–18:05 spot limitli. **Stop %25** (kilit riski) → 10.000 TL ≈ 12 lot. 2020-03'ten beri 75 tavan kapanışı var: kilitli tavanda dolum yok, kovalanmaz |
| Etiket | Öncülük **YOK**; gece **RISK**; `BIST:BRYAT` **FILTRE** |
| Kanıt | Yeni: `BIST:BRYAT`_t → t+1 t −0,78 (OOS −2,13, işaret dönüyor). ABD çeliği (≈ `AMEX:SLX` − β·`SP:SPX`) t−1 → t+1 t 1,24. İkisi de YOK. ES/NQ/TUR gece → gap 0,27/0,29/0,16. BRYAT senkron pc 0,56 |
| Pine / TradingView | Kapanış alarmı `BIST:BRSAN` > 769,50. NAV/senkron: `BIST:BRSAN/BIST:BRYAT`. Bağlam: `BIST:XUSIN` |
| Güncel | 06.11: 682,00. Bilançonun 6.11'de çıktığını teyit et |

### 1.9 Koza göreli momentum: TRMET1! / TRALT1! (KENAR, sönmüş → kâğıt; lead-lag değil)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | Sinyal grafiği `BIST:TRMET1!` / `BIST:TRALT1!`; işlem kontratı A10'a göre Aralık: F_TRMET1226 (ince, 06.11 hacmi 9 mn TL) ve F_TRALT1226 (rehber "çıkıştan sonra biten en yakın vade" diyor; plan geçerli). **IZLE (kâğıt)**, [RH-K §1] |
| Lead-lag (lider → yön) | Klasik öncülük yok: TRALT(t−1) → TRMET 2022–26'da −0,13 (t −2,4). Kural TRMET'in grubuna göre kendi momentumudur: **TRMET artığı yönünde** |
| Formül | u = r_TRMET − β_g·ort(r_TRALT, r_TRENJ); β_g 250 gün, bir gün gecikmeli. z3 = (u_t + u_t−1 + u_t−2) / (σ60·√3) |
| Eşik | \|z3\| > 1,5 |
| Ne zaman bilinir (TSİ) | 17:50–17:55, canlı fiyatla (kesin değer 18:10'da) |
| Ne yapılır | z3 > +1,5 ise TRMET1! AL + TRALT1! SAT; z3 < −1,5 ise tersi. TRALT nominali = β_TA (0,69) × TRMET nominali (≈ 1:2 kontrat). 18:00–18:10'da iki bacak birlikte girilir: önce az likit olan TRMET1!, hemen ardından TRALT1!, 2–3 parçada. Tutma 2 gün; sinyal sürerse uzatılır (en çok 6). **Yapılmaz:** limit kilidi, kurumsal olay günü ve ertesi günü, tek bacak. **Stop:** kümülatif −800 bps'te kural durdurulur. **Boy:** işlem başı ~%0,25 → 6 TRMET1! : 12 TRALT1! (G ≈ 122 bin TL; günlük rapor); rehber %0,5 → 14 : 28. Eski lead-lag toplam bütçesi ≤ %0,5, K9 bütçesi değil (başlıktaki risk bütçesi notu) |
| Etiket | **KENAR**, sönmüş → kâğıt |
| Kanıt | Brüt +51,7 bps (t 3,0); net (15 bps + tik) +28,8. **2024–26 net ≈ +1**; 2026 −29 bps/işlem, yıl toplamı −458 bps. Uzlaşma girişiyle h2 +45 (t 4,05) [RH-K §3, §8, §9.2]. Kurumsal olay riski: CAR −%10…−%41 (RISK) |
| Pine / TradingView | `2026-11-04_kapanis_1-3gun/rehber/koza/koza_alarm.pine` → `BIST:XU030` 1G grafiği. Alarmlar: "KOZA \|z3\| eşik üstü (durumdan bağımsız)" ve "KOZA bugün çıkış günü (sabah hatırlatma)", **Bar başına bir kez**, pencere 17:45–18:10. Canlı veri şart |
| Güncel | 06.11: z3 **+0,71** (u +130 bps, σ60 195 bps, β_g 0,88), pozisyon yok. **9.11 tetiği** (TRALT ve TRENJ yatay kalırsa): AL TRMET ≥ **116,76**, SAT ≤ **105,54** (06.11 111,90). 9.11 bilanço belirsizliği (A1) → canlı giriş yok |

Yan ilişki: grup içi ters dönüş (TRALT+TRENJ artığı t−1 → TRMET) kapanıştan kapanışa t −1,63, q 0,39. Tek başına YOK; z3 kuralının içinde zaten var (FILTRE). Senkron TRMET–grup 0,845.

### 1.10 Altın → TRALT (KENAR, DÜŞÜK; eksik aynı gün tepkisi)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:TRALT1!` + hedge `BIST:XU030D1!`; işlem kontratı A10'a göre F_TRALT1226 (06.11 hacmi 35 mn TL) + F_XU0301226. **IZLE (kâğıt)**, [RH-A §1] |
| Lead-lag (lider → yön) | `TVC:GOLD` (yedek `OANDA:XAUUSD`; `COMEX:GC1!` kullanılmaz, vade geçişinde sıçrar) → TRALT, **aynı yön**. Kaynağı eksik aynı gün tepkisi: altın katsayısı t 2,84, TRALT'ın kendi hareketi t 0,29 |
| Formül | g = ln(GOLD 17:55 / önceki BIST günü 17:55); z = g / σ250 (σ ≈ %1,70) |
| Eşik | \|z\| > 1, yani \|g\| > ~%1,70 |
| Ne zaman bilinir (TSİ) | 17:55 |
| Ne yapılır | z > +1 ise TRALT1! AL + XU030D1! SAT; z < −1 ise tersi. TRALT1! 18:00–18:10 (pay vadelisi uzlaşması), XU030D1! aynı anda (endeks vadelisi 18:15'e kadar açık, uzlaşma ~18:05–18:15). Bir bacak dolmazsa dolanı da aynı gün kapat; yarım hedge'le gece taşınmaz. Kilit kontrolü: AL'da TRALT tavanda, SAT'ta tabanda kilitliyse girilmez [RH-A §3]. Oran N = yuvarla(10·XU030 / (β·100·TRALT)); β TRALT/XU030 250 günlük beta. 2 BIST günü sonra 17:55'te bakılır: aynı yönde sinyal varsa uzat, ters sinyalde çevir, yoksa iki bacak birlikte kapat. **Stop:** test edilmedi. **Boy:** 1 mn TL'de 1 birim (1 XU030D1! + N TRALT1!). ~700 bin TL'nin altında yapılmaz; arife günü yok. Planda canlı kanalı yok, yani kâğıt (başlıktaki risk bütçesi notu) |
| Etiket | **KENAR (DÜŞÜK)**; yalnız altın rallisi rejimlerinde çalışıyor |
| Kanıt | 8 + 3 bps maliyetle net **+35,5 bps (t 2,20)**. **2024–26 +54 (t 1,96)**. En iyi 10 işlem çıkınca t 0,94. 2021 −48, 2023 0; fon krizinde −82 [RH-A §8] |
| Pine / TradingView | `2026-11-04_kapanis_1-3gun/rehber/altin/altin.pine` → `BIST:TRALT1!` 1G; *Elle σ* = 1,70. Alarm "Altın sinyali (geçici)", Bar başına bir kez. Karar 17:55'te `TVC:GOLD` grafiğinde verilir |
| Güncel | VİOP F_XAUUSD1226 uzlaşma vekili (17:55 değeri elde yok): 6.11 −%1,50 → z −0,88, sinyal yok. 5.11 +%1,81 → z +1,07 (AL adayıydı; kâğıtta açıldıysa 9.11 17:55'te z'ye bak: aynı yön > +1 ise tut, < −1 ise çevir, yoksa 18:00–18:10 kapat). Not: rehber 04.11'i de AL adayı sayıyordu (z +1,47) [NB §1.5]. 04.11'de açıldıysa kural gereği 05.11 sinyaline bakılmaz ve çıkış günü 06.11'dir. Kâğıt kaydında hangisinin açıldığını kontrol et. N = 29 (β 1,30) |

**Yan ilişkiler:**
- ABD altın madencileri (≈ `AMEX:GDX` − β·`SP:SPX`) t−1 → TRALT t+1: t 0,78 → **YOK**. Aynı bilgi BIST'in t gününde fiyatlanıyor (pc 0,114) → **RISK**.
- `COMEX:GC1!` senkron pc 0,21 → **FILTRE**.

### 1.11 Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `BIST:XU030D1!`. **IZLE (olay günü)**, [PL; NB §1.7] |
| Lead-lag (lider → yön) | Ticker değil: S&P, Moody's ya da Fitch'in Türkiye not kademesi kararı → **kararın tersi** (not artırımında SAT, indiriminde AL) |
| Formül | Yalnız kademe değişimi sayılır (görünüm değişimi değil) |
| Eşik | Kademe değişti mi (evet/hayır) |
| Ne zaman bilinir (TSİ) | Karardan sonraki ilk BIST seansı (tepki günü) |
| Ne yapılır | Tepki gününün F_XU030 uzlaşma penceresinde (endeks vadelisi ~18:05–18:15) kararın tersine. 2 gün tut, uzlaşmada çık. Test stopsuz. **Kanal:** eski dört sinyalden değil; canlı yalnız K9'dan (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra. Şimdilik kâğıt |
| Etiket | **KENAR (DÜŞÜK, olay)**: çoklu test düzeltmesinden sonra anlamsız |
| Kanıt | n = 16. 8 bps maliyetle net h2 **+142 (t 2,93)**, isabet %75. En iyi 3 olay çıkınca +94 (t 1,87). **Bonferroni p ≈ 0,14.** Son iki karar −217 (S&P 2024-11) ve −53 (Moody's 2025-07). 2000–13'te ve diğer gelişen piyasalarda çalışmıyor |
| Pine / TradingView | Pine yok; `BIST:XU030D1!` 1G |
| Güncel | Karar takvimi dosyalarda yok → ajans ya da aracı kurum takviminden teyit et |

---

## 2. Bu profilde lead-lag sayılmayacaklar (BIST, hepsi)

- **RISK, açılışta fiyatlanır:** `CME_MINI:ES1!` / `NQ1!` gecesi, `NASDAQ:TUR`, `TVC:NI225`, KOSPI, `CBOE:VIX`_t−1, gece Brent ve gece altın, `FX:EURTRY` gecesi.
- **YOK, açılış emri ister:** VİOP'un 09:30 açılışı → spot açılış; açılış gap fade'i (ENJSA, BRSAN); akranın gap'ine gün içinde yetişme (BRSAN).
- **Gün içi öncüler (kapanıştan kapanışa kalmıyor):** Avrupa rafineri sepeti t−1 → TUPRS: **YOK** (brüt 8,5 bps < maliyet). `ASX:FMG` / `TSE:5411` → BRSAN: **RISK** (kenar ilk 30 dakikada). AKBNK_t−1 → SAHOL: gün içi sürüm maliyeti karşılamıyor, kapanıştan kapanışa sürüm zayıf **FILTRE** (§1.3). `ASX:FMG` → EREGL: NB'de HAYIR [LB Ek A; NB §1.6].
- **Doğrulandı:** günlük hisse→hisse ve endeks→hisse öncülüğü FDR'den geçmedi (~170 bin test) [LL].

---

## 3. ABD Tier A kartları

**Hepsi için ortak:**
- **Emir kartı** [NA §1; PA §3.1–3.5]:
  - Giriş: 16:45–17:15 TSİ'de BUY STOP-LIMIT (DAY, yalnız normal seans) ve ekli GTC SELL STOP.
  - S1: tetik = pivot × 1,001; limit = min(tetik × 1,01; tetik + 0,3·ATR14). Stop = son daralmanın dibi − %0,1. Tetikten stopa mesafe 1,0–2,0 ATR ve ≤ %8 olmalı.
  - Çıkış: ilk 3 seansta başarısız kırılım olursa MOO ile çık. +2R'de ya da 4. seansta ≥ +1R ise yarısını sat. +1,5R'de stop başabaşa. Kapanış < 20 GHO ise çık. Bilançodan önceki son seansta MOC ile çık.
  - S1'de en çok 5 seans her gün yeniden girilir; kapanış pivot × 1,05'in üstündeyse kurulum iptal. S2: tetik = sinyal günü tepesi × 1,001, 2 seans; stop = min(sinyal günü dibi; 20 GHO − 0,25 ATR) − %0,1.
  - Çıkış kararı kapanış bloğunda (00:30–01:00 ya da 08:00–09:00), emir ertesi açılışta MOO. Başarısız kırılım (ilk 3 seans): S1'de kapanış < pivot − 0,5 ATR. 10. seansta kâr < +1R ve son 5 seansta yeni en yüksek kapanış yoksa çık. Ön filtre: son çeyrekte EPS ve gelir beklentiyi aşmış, bilançodan sonraki 3 seans SPY'ye göre ≥ 0.
  - **Boy:** adet = ⌊E × %0,25 / (limit − stop)⌋; pozisyon ≤ E'nin %7,5'i. E = ABD strateji sermayesi (USD; servetin %10'u, en çok %15; PA §5.4, §10). Örnek: E = 50k $ → 1R = 125 $ [NA §1]. BIST'teki 1 mn TL'lik hesap ABD E'si değildir. Yalnız long.
- **Rejim** (`SP:SPX` 1G grafiğinde `uygulama/kod/abd_rejim_ve_sablon.pine`, derlenmedi): şu an **KIRMIZI**. Yakın bölgede yalnız 1 pozisyon, risk %0,25, ısı ≤ %0,5; ilk pilot en erken **Pt 16.11, 16:45–17:15**, yalnız 13.11 kapanışında SARI olursa [PA §7.2]. Yasak günler: 17.11, 25.11, 27.11, 9.12. CPI (10.11) ve PPI (13.11) günlerinde 16:45'te `CME_MINI:ES1!` ±%1,5'ten fazla oynadıysa yeni giriş yok.
- **Test sınırı** [LA §1, §5]:
  - Kullanılan veri Ken French 49 sektör portföyü (son gün 30.09.2026). ABD'de tek hisse serisi yok, bu yüzden hisse düzeyindeki her etki zayıflar ve hisseye özgü her kanal TEST EDİLMEDİ.
  - Zamanlama iki varyantla ölçüldü: A (t+1..t+h, üst sınır) ve B (t+1 atlanır, muhafazakâr). Gerçek getiri ikisinin arasında.
  - Önceden yazılmış 150 testin hiçbiri FDR'den geçmedi (en düşük q 0,24).
  - Yaklaşık 1.320 testlik taramada 4 test geçti; B'de hepsi sıfıra iniyor.
  - Literatürdeki müşteri→tedarikçi ve ekonomik bağ etkileri (Cohen–Frazzini 2008, Menzly–Ozbas 2010) **aylık** ufukta; günlükte zayıf ve yayımdan sonra aşınıyor (McLean–Pontiff) [LA §5; dalga_abd §2]. Bu yüzden sektör düzeyindeki "YOK", aylık bir etkiyi dışlamaz; yalnız bu 1–5 günlük kullanımda işe yaramadığını söyler.
- **İzleme listesi:** `hesaplar/leadlag_uygulama/abd/ABD_TierA_izleme.txt`, TradingView'e "Listeyi içe aktar" ile. Oran grafikleri listede değil, sembol kutusuna aşağıdaki gibi yazılır.

### 3.1 BDX: hastaneler → medtech (FILTRE)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `NYSE:BDX`. **Tier A**, sağlık süper-kümesi (K1 medtech). S1 (pivot ≤ %3) ya da baz 15 seansı doldurmadıysa S2. EHC ile aynı anda açılmaz |
| Lead-lag (lider → yön) | `NYSE:HCA` (FF49 Hlth'in vekili; ikinci kontrol `NYSE:UHS`) piyasa artığı → BDX, **aynı yön**. Müşteri→tedarikçi kanalı (prosedür hacmi). Etki yalnız güçlü kuyrukta |
| Formül | e = r_HCA − β252·r_SPX (log). S = son 5 günün e toplamı. z = (S − ort252(S)) / std252(S). Test edilen: FF49 Hlth artığının 5 günlük toplamı, 252 günlük z → MedEq artığının sonraki 3–5 günü |
| Eşik | z > +1. z < −1 bilgi taşımıyor; kaçınma sinyali değil |
| Ne zaman bilinir (TSİ) | ABD t kapanışı 00:00. Okuma 00:30–01:00 ya da 08:00–09:00. Geçerlilik sonraki 3–5 seans |
| Ne yapılır | Yalnız sıralama. BDX'te S1/S2 hazırsa (ABD_RJ "S1 ön koşul / S2 lider" EVET, pivot ≤ %3, stop 1,0–2,0 ATR ve ≤ %8) **ve** z > +1 ise sağlık kümesinin tek hakkını BDX'e ver (EHC ve TMO yerine). Emir, stop, çıkış ve boy ortak karttan. z ≤ +1 ise PLAN §4.4 #6 sırası geçerli. z tek başına giriş sebebi değil |
| Etiket | **FILTRE** |
| Kanıt | Sektör düzeyi: b +11,4 bps/σ, **t 2,82 (A) / 2,38 (B)**; IS 1,95 / OOS 2,02 (A); q 0,24, yani FDR'den geçmiyor. Komşu (L, h) 3–5 aynı. z > +1 kuyruğu (varyant B): 5 günde **+25 bps** artık (IS +30 / OOS +17,5). OOS net: 10 bps maliyetle +7,5, **20 bps ile −2,5**. 17 yılın 14'ünde eğim pozitif; negatifler 2016–18, yani 2024–26'da pozitif (2024–26 için ayrı net hesaplanmadı). Hisse ve HCA vekili düzeyinde TEST EDİLMEDİ (daha gürültülü) |
| Pine / TradingView | `hesaplar/leadlag_uygulama/abd/ll_z_filtre.pine` → `NYSE:HCA` 1G. Girdiler: Öncü `NYSE:HCA`, Piyasa `SP:SPX`, L 5, W 252. Derlenmedi; ilk kullanımda 1–2 günü elle kontrol et. Teyit seti: `NYSE:BDX/AMEX:IHI` ve `AMEX:IHI/SP:SPX` 50 GHO'nun üstünde; `NYSE:BDX/SP:SPX` (ABD_RJ RS/52H: S1 ≥ 0,97, S2 ≥ 0,95). `AMEX:IHI` 08.11'de doğrulandı |
| Güncel | Hesaplanmadı (ABD hisse verisi yok). 5.11: 212,52, 52H −%1,1 [NA]. Rejim KIRMIZI → işlem yok |

**Yan ilişkiler:**

| Lider | Etiket | Kullanım |
|---|---|---|
| `NYSE:MDT` bilançosu 24.11 BMO; `NYSE:BDX/NYSE:MDT` | RISK (24.11 gap'i) | Açık BDX varsa 23.11 kapanış bloğunda gap-ayarlı ısıya bak. 24.11 sabahına yeni S1 tetiği koyma; MDT tepkisinden sonraki seansa bırak |
| `NYSE:SYK`, `NYSE:BSX`, `NASDAQ:ISRG`, `NYSE:EW` (Ocak sonu bilançoları) | RISK | Takvime yaz. BDX'in kendi bilançosu Oca sonu–Şub 2027 (IR'den teyit et) |
| MedEq ← Drugs, LabEq, MKT, SMB, ΔVIX, kendi geçmişi | YOK (\|t\| < 2,1) | Kullanma |
| `TVC:DXY` (çevrim) | TEST EDİLMEDİ | Yalnız rehber bağlamı |

### 3.2 EHC (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `NYSE:EHC`. **Tier A**, sağlık süper-kümesi (K3 hizmet); S1. BDX ile aynı anda açılmaz |
| Lead-lag | **Islenebilir lead-lag yok.** Ödeyici → sağlayıcı (`NYSE:UNH`) günlükte YOK. Hastanelerin gücü (LL_z) **BDX'i** öne alır, EHC'yi değil |
| Formül (alternatif) | PLAN S1: tetik = pivot × 1,001 |
| Eşik | ABD_RJ satırları: TT EVET, RS/52H ≥ 0,97, pivot ≤ %3 |
| Ne zaman bilinir (TSİ) | ABD kapanışı 00:00; okuma 00:30–01:00 ya da 08:00–09:00 |
| Ne yapılır | Ortak emir kartı. **Kaçınma (RISK):** CMS IRF PPS kuralları (taslak genelde Nisan, nihai Temmuz sonu–Ağustos başı) ve Medicare Advantage oran duyuruları ikili olaydır, olaydan önceki 10 seansta giriş yok. Hastane emsal bilançoları (HCA, UHS, THC; Oca sonu–Şub) haftasında yeni giriş ertelenir. UNH, ELV ve CI bilanço günleri olay günüdür. LL_z(HCA) > +1 ise sağlık hakkı BDX'e geçer |
| Etiket | Öncülük **YOK**; olay **RISK** |
| Kanıt | Hlth ← Insur: \|t\| ≤ 1,4 (A ve B). En iyi test MKT (1,1): t 2,15, OOS 0,59, B 0,42, q 0,55. Emsal bilanço ve CMS: TEST EDİLMEDİ |
| Pine / TradingView | Asıl ölçüt `NYSE:EHC/NYSE:HCA` ve `NYSE:EHC/AMEX:XLV`; `AMEX:XLV/SP:SPX`. NA'daki `NYSE:EHC/AMEX:IHF` dikkatle kullanılmalı: IHF ağırlıkla yönetilen sağlık, EHC'nin emsali değil |
| Güncel | 5.11: 141,27, 52H −%1,5 [NA] |

### 3.3 TW (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `NASDAQ:TW`. **Tier A**, K4 borsalar; S1. K4 ve K5'in toplam ısısı ≤ %1,25 |
| Lead-lag | **Islenebilir lead-lag yok.** Faiz oynaklığı → hacim kanalı yalnız bağlamdır |
| Formül (alternatif) | PLAN S1 |
| Eşik | ABD_RJ satırları |
| Ne zaman bilinir (TSİ) | 00:00; aylık hacim raporları ayın ilk iş günlerinde |
| Ne yapılır | Ortak emir kartı. **Kaçınma (RISK):** aylık hacim raporunun (TW, MKTX, ICE, CME) yayınlanacağı günden önceki kapanışta yeni S1 tetiği koyma; tarihler IR'den. **Bağlam (TEST EDİLMEDİ):** `TVC:MOVE` 50 GHO'nun üstündeyse çeyrek hacmini destekler. MOVE ve VIX çökerken TW geride kalabilir. Günlük vekiller (\|ΔDGS10\|, ΔVIX) sektörde YOK çıktı; MOVE izinli kaynakta yok |
| Etiket | Öncülük **YOK**; MOVE **TEST EDİLMEDİ** (yalnız bağlam; [LA] "FILTRE (bağlam)" diyor ama günlük vekiller YOK); rapor günü **RISK** |
| Kanıt | Fin ← \|ΔDGS10\|, ΔVIX: \|t\| ≤ 1,4. Fin ← SMB (5,5): t 2,17, q 0,55. Taramada FDR'den geçen 4 test (Fin'in ertesi günü ← Insur −, Hardw +, Food −, Paper −) B'de sıfıra iniyor (q ≥ 0,60); OOS 1–9 bps, 10 bps maliyetin altında. Vekil zayıf: Fin portföyünde REIT'ler de var |
| Pine / TradingView | `NASDAQ:TW/AMEX:IAI` ve `AMEX:IAI/SP:SPX` (NA'daki `NASDAQ:TW/AMEX:XLF`'ten daha uygun); `NASDAQ:TW/NASDAQ:MKTX`. Bağlam: `TVC:MOVE`, `TVC:US02Y`, `CBOT:ZN1!` |
| Güncel | 5.11: 127,56, 52H −%1,1 [NA] |

### 3.4 ACGL (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `NASDAQ:ACGL`. **Tier A**, K5 sigorta; S1. Sigorta izni reasürans grubunun üstte olmasına bağlı |
| Lead-lag | **Islenebilir lead-lag yok.** Afet ve emsal bilgisi gap'te fiyatlanır |
| Formül (alternatif) | PLAN S1 |
| Eşik | ABD_RJ satırları |
| Ne zaman bilinir (TSİ) | 00:00; afet haberi gece |
| Ne yapılır | Ortak emir kartı. **RISK:** Büyük afet (kasırga, deprem, yangın) ikili olaydır: haberden sonraki ilk seansta yeni giriş yok; açık pozisyonda gap-ayarlı ısıya bak. Kasırga sezonu 30.11'de bitiyor. `NYSE:BRK.B`'nin 07.11 bilançosuna Pt 9.11'deki tepkisi K5 notu olarak yazılır. **TEST EDİLMEDİ (olası FILTRE):** Aralık'taki reasürans fiyat yorumları ve 1 Ocak yenilemeleri. Fiyatlar yumuşuyorsa K5'te boyut küçült |
| Etiket | Öncülük **YOK**; afet **RISK** |
| Kanıt | Insur'da kasırga sezonu farkı +1,69 bps/gün, t 0,75 (YOK). Insur ← ΔDGS10, Fin, ΔVIX, MKT, SMB: YOK. Kendi (5,5): −10,9 bps/σ, t −2,54 (IS −2,52 / OOS −1,03), q 0,42 (YOK). Vekil zayıf: Insur portföyünde BRK, UNH ve PGR var. ACGL'ye özgü afet etkisi TEST EDİLMEDİ |
| Pine / TradingView | `NASDAQ:ACGL/AMEX:KIE`, `NASDAQ:ACGL/NASDAQ:KBWP`, reasürans içi `NASDAQ:ACGL/NYSE:RNR`; NA'daki `NASDAQ:ACGL/AMEX:XLF`. Emsaller: `NYSE:EG`, `NYSE:CB`, `NYSE:TRV`, `NYSE:BRK.B` |
| Güncel | 5.11: 110,57, 52H −%2,7 [NA] |

### 3.5 MAR (Islenebilir lead-lag yok)

| Alan | İçerik |
|---|---|
| Enstrüman · hüküm | `NASDAQ:MAR`. **Tier A**, K8 konaklama; S1. Tetik FTD ya da S&P 10 > 20; yakın bölge bitince açılır [NA Ö] |
| Lead-lag | **Islenebilir lead-lag yok.** Havayolu ve seyahat (`NYSE:DAL`, `AMEX:JETS`) → otel bilgisi t+1'de fiyatlanıyor |
| Formül (alternatif) | PLAN S1 |
| Eşik | ABD_RJ satırları + FTD ya da S&P 10 > 20 |
| Ne zaman bilinir (TSİ) | 00:00 |
| Ne yapılır | Ortak emir kartı. **RISK takvimi:** HD 17.11 (17.11 genel yasak); TGT, TJX ve LOW 18.11; WMT 19.11 BMO; DAL Ocak ortası; BKNG, EXPE ve ABNB Şubat. Zayıf RevPAR haftasında yeni girişi ertele (TEST EDİLMEDİ) |
| Etiket | Öncülük **YOK**; tüketici emsalleri **RISK** |
| Kanıt | Meals ← Trans (1,3): t 2,02 (A), 0,61 (B), q 0,55 (YOK). Meals ← Rtail, ΔWTI, MKT, SMB: YOK. Meals ← Autos IS ve OOS'ta anlamlı ama 20 bps sonrası net −10. RevPAR ve TSA verisi yok (TEST EDİLMEDİ) |
| Pine / TradingView | `NASDAQ:MAR/AMEX:PEJ` ve `AMEX:PEJ/SP:SPX` (NA'daki `NASDAQ:MAR/AMEX:XRT`'den daha uygun); küme içi `NASDAQ:MAR/NASDAQ:HLT`. **NA'daki `NYSE:HLT` yanlış; TradingView 404 veriyor.** Emsaller `NYSE:H`, `NYSE:IHG`, `NYSE:WH` |
| Güncel | 5.11: 417,28, 52H −%3,7 [NA] |

### 3.6 Yedekler (kısa)

| İsim · TV | Test (sektör) → etiket | Hisseye özgü kanal | Grafik |
|---|---|---|---|
| TMO `NYSE:TMO` | LabEq ← Drugs, MedEq: YOK. LabEq ← MKT (5,5) t −2,89, OOS −1,55: YOK | Emsal bilançolar (`NYSE:DHR`, `NYSE:A`, `NYSE:WAT`, `NYSE:MTD`, `NYSE:IQV`; Ocak sonu): RISK. Biyotek fonlaması (`AMEX:XBI`): TEST EDİLMEDİ (olası FILTRE) | `NYSE:TMO/AMEX:XLV`, `NYSE:TMO/NYSE:DHR` |
| RPRX `NASDAQ:RPRX` | Drugs ← ΔDGS10, Hlth, Insur: YOK. Kendi (1,1) t 3,07, B'de −0,05: YOK | `TVC:US10Y` (duration): TEST EDİLMEDİ (olası FILTRE). Ortak ilaç haberleri (`NASDAQ:VRTX`): RISK. SIC kodunu (6794) teyit et | `NASDAQ:RPRX/AMEX:XLV`, `NASDAQ:RPRX/NASDAQ:IBB` |
| CME `NASDAQ:CME` | TW ile aynı: YOK | Oynaklık (`CBOE:VIX`, `TVC:MOVE`, `CME:SR31!`): TEST EDİLMEDİ (bağlam; sektörde ΔVIX YOK). Aylık ADV raporu: RISK | `NASDAQ:CME/AMEX:IAI`, `NASDAQ:CME/NYSE:ICE` |
| MRSH `NYSE:MRSH` | Insur testleri: YOK | P&C fiyat döngüsü: TEST EDİLMEDİ (olası FILTRE). `NYSE:AON`, `NYSE:AJG`, `NASDAQ:WTW`, `NYSE:BRO` bilançoları: RISK | `NYSE:MRSH/AMEX:KIE`, `NYSE:MRSH/NYSE:AON` |
| HLT `NASDAQ:HLT` | MAR ile aynı: YOK | MAR ile aynı | `NASDAQ:HLT/AMEX:PEJ`, `NASDAQ:HLT/NASDAQ:MAR` |
| SN `NYSE:SN` | Hshld ← Rtail: YOK. Kendi (5,5) t −2,01: YOK | Müşteri bilançoları (TGT 18.11, WMT 19.11, `NYSE:BBY` 24.11 BMO, `NASDAQ:AMZN`): RISK. Tarife: RISK | `NYSE:SN/AMEX:XLY`, `NYSE:SN/AMEX:XRT` |

---

## 4. Pazartesi 9.11: saat akışı (yalnız lead-lag ile ilgili satırlar)

| TSİ | İş | Araç |
|---|---|---|
| 00:30–01:00 ya da 08:00–09:00 | ABD_RJ (KIRMIZI mı?), `LL_z(HCA)`, olay takvimi (BRK.B tepkisi 9.11; CPI 10.11) | `SP:SPX` + ABD_RJ; `NYSE:HCA` + `ll_z_filtre.pine` |
| 08:30–10:00 (Pine'da ~10:00–10:15) | TUPRS z (ABD Cuma 6.11). \|z\| > 1 ise kâğıda yaz: z yönünde 1 kontrat, 18:00–18:10. Yan kontrol: `AMEX:XLE` artığı | `sinyal_tuprs.py` sabah; `tuprs_alarm.pine` (`BIST:TUPRS1!`) bugünün z'sini ancak BIST barı açılınca gösterir |
| Gün içi | Gece sürücüleri sinyal değil | — |
| 17:50–17:55 | Koza z3 (TRMET ≥ 116,76 / ≤ 105,54) ve `TVC:GOLD` 17:55 değişimi (±%1,70). A1 → ikisinde de canlı yok | `koza_alarm.pine`, `altin.pine` |
| 18:00–18:10 | F_TUPRS, Koza, altının TRALT bacağı uzlaşma penceresi (kâğıt); altının XU030D1! bacağı ~18:05–18:15 | Aracı kurum ekranı |
| 18:08–18:15 | XU030 Δb: oran < 1,0343 AL / > 1,0484 SAT (kâğıt; std120 68 bps, ~17.11'den sonra ~42). RYGYO kapanışı ≥ 50,61 / ≤ 47,63 (RYSAS kâğıt kuralı; RYSAS bilançosu 9.11 → işlem yok) | `BIST:XU030D1!/BIST:XU030`; `BIST:RYGYO` alarmları |
| 18:15 sonrası | K1 oranı (≥ 1,3556 / ≤ 1,2249 → giriş Salı 17:55). K4 kapanış alarmları: ENJSA 127,00 · ENERY 14,60 · AHGAZ 48,70 · KCHOL 225,50 · RYSAS 30,28 · BRSAN 769,50 | `BIST:SAHOL/BIST:AKBNK`; `bist_sinyal.py` |

## 5. Düzeltmeler ve açık işler

- **Kod:** Hilton `NASDAQ:HLT`; `NYSE:HLT` TradingView'de 404 veriyor. NA'daki `NASDAQ:MAR/NYSE:HLT` ve `NYSE:HLT/AMEX:XRT` düzeltilmeli.
- **Kod doğrulaması:**
  - `AMEX:IHI`, `BIST:RYSAS` ve `BIST:AHGAZ` 08.11'de TradingView sembol sayfasından doğrulandı (varsayılan istek, HTTP 200, başlıkta aynı kod).
  - LA §0'daki listede IHI adı geçiyor ama `tv_kod_kontrol.csv`'de yoktu; şimdi doğrulandı.
  - Bu dosyadaki diğer kodlar ya `tradingview_kodlari.csv`'de ya da `tv_kod_kontrol.csv`'de var.
  - Vade kodları (`BIST:XU030DZ2026`, `BIST:SAHOLZ2026`, `BIST:AKBNKZ2026`) [TV]'nin not sütunundaki kalıptan; ilk kullanımda sembol kutusunda teyit et.
- **XU030 bazı:**
  - std120 = 68 bps, ama 21–22.05.2026'daki tek şoktan şişmiş; bu iki gün hariç ~42 bps. ~17–18.11'de pencereden çıkıyorlar.
  - Günlük rapor ve [TVA] §6 sabit 50 bps kullanıyor. Raporun σ'sını std120'ye bağla; seviyeleri her akşam yeniden kur.
- **Plan uyumu (bu kontrolde düzeltildi):**
  - Eski lead-lag sinyallerinin bütçesi PB §3.11'deki toplam %0,5'tir, K9 değil. [TVA] §0, §2, §3 ve §6'daki "K9 kanalı / K9 riski" ifadeleri plana aykırı; TVA ayrıca düzeltilmeli.
  - Altın → TRALT ve RYSAS kâğıt kuralının planda canlı kanalı yok; kredi notu canlıya yalnız K9'dan girebilir (başlıktaki not).
  - ABD boyu E (USD) üzerinden hesaplanır; 1 mn TL'lik BIST hesabından türetilmez.
- **Pine dosyaları:**
  - `ll_z_filtre.pine`, `abd_rejim_ve_sablon.pine`, `tuprs_alarm.pine`, `koza_alarm.pine` ve `altin.pine` derlenmedi.
  - İlk kullanımda son günleri betik ya da rapor değerleriyle karşılaştır.
- **Hesaplanamayanlar:**
  - TUPRS rafineri z'si ve `TVC:GOLD` 17:55 değeri: ABD hisse verisi ve gün içi altın verisi izinli kaynakta yok.
  - ABD'de LL_z: Ken French verisi 30.09'da bitiyor.
  - Üçü de TradingView'dan okunacak.
- **Plan kararına bırakılan:** ENJSA ile ENERY/AHGAZ ayrı küme sayılabilir mi (ölçülen bağ 0,05 / −0,01).
