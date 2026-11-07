# BIST net liste: TRADE / İZLE isimleri için uygulanabilir lead-lag haritası (06.11 kapanışı → Pazartesi 9.11)

_08.11.2026 · profil: karar BIST kapanışında 18:00–18:15 TSİ, VİOP'ta 1–3 gün kapanıştan kapanışa, gün içi ekran yok · yatırım tavsiyesi değildir_

Kapsam: `uygulama/NET_LISTE_BIST.md`'de TRADE ya da IZLE olan her kalem: TUPRS (ABD rafinerileri), XU030 vadeli kapanış bazı, SAHOL/AKBNK (K1), ENJSA, ENERY+AHGAZ (tek isim), KCHOL, RYSAS, BRSAN, TRMET/TRALT (Koza), altın → TRALT, kredi notu kararı → F_XU030.
Kaynak önceliği: doğrulama > plan > araştırma. Kısaltmalar NET_LISTE ile aynı: [LL] `2026-11-02_viop_leadlag/RAPOR.md`, [KART] `hisse_kartlari/<KOD>.md/.json`, [TV] `tradingview_kodlari.csv`, [PL] `2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md`, [RH-T/K/A] rehberler, [PB] `uygulama/PLAN_BIST.md`. "(yeni)" = bu çalışmada hesaplandı (kod: `hesaplar/leadlag_uygulama/`).

## 0. Etiketler ve zaman kuralı

| Etiket | Anlamı (bu kullanıcı için) |
|---|---|
| **KENAR** | Test edildi, kapanıştan kapanışa ve maliyet sonrası ayakta. 1–3 günlükler küçük ve 2024–26'da sönük; canlıda mini boy, Kural 0 cevabına kadar kâğıt |
| **FILTRE** | Gerçek ilişki, tek başına kenar değil; zamanlama, boyut, hedge, küme ya da kaçınma için kullanılır |
| **RISK** | Bilgi BIST açılış gap'inde ya da t gününün içinde fiyatlanıyor; kullanıcı girdiğinde fiyat zaten oynamış olur. Yalnız gap/risk beklentisi |
| **YOK** | Test edildi, kapanıştan kapanışa bir şey yok (ya da yalnız açılış emriyle var, yani profil dışı) |
| **TEST EDİLMEDİ** | Veri/kanıt yok |

**Zaman kuralı (bütün satırlarda):**
- Yurt içi lider (BIST kapanışı t, 18:10'da kesin) → hedef kapanış t → t+1. Spot hedefte giriş 18:10–18:15 "kapanış fiyatından işlemler" seansında (sığ); VİOP'ta 18:00–18:10 uzlaşma penceresi.
- ABD tarihli lider (ABD günü d) → d'den sonraki ilk BIST günü t'nin kapanışında giriş → t+1 (ya da t+2) kapanışı. ABD d kapanışı kışın 00:00 TSİ'de kesin (01.11.2026–14.03.2027). ABD'nin **aynı gün** BIST seansı sırasındaki hareketiyle sinyal üretilmez [RH-T §3].
- [LL] çerçevesi geçerli: küresel "lead-lag"in çoğu gece bilgisi; açılışta fiyatlanır, pay vadelisinde akşam seansı yok. Sektöre özgü yabancı emsal bilgisinin ~%22'si açılışta, kalanı t gününün içinde fiyatlanır (brüt 3–11 bps). Günlük hisse→hisse ve endeks→hisse öncülüğü FDR'den geçmedi (~170 bin test).

## 1. Tek bakışta: her enstrüman, en iyi ilişki, etiket, 06.11 değeri

| Enstrüman (NET_LISTE hükmü) | En iyi ilişki (TradingView) | Etiket | Sayı | 06.11 / Pazartesi değeri |
|---|---|---|---|---|
| **TUPRS** (1-3G TRADE mini) | `NYSE:VLO`,`NYSE:MPC`,`NYSE:PSX`,`NYSE:PBF` − β·`SP:SPX` (ABD t−1) → `BIST:TUPRS1!` (F_TUPRS1226) t uzlaşma → t+2 | **KENAR** | 8 bps ile net +42 (t 2,72), 15 bps ile +35; IS +34,5 / OOS +48,8; 2024–26 +26 (t 1,0) [PL #4] | **Hesaplanamadı:** ABD tekil hisse verisi izinli kaynakta yok (Yahoo kapalı). Pazartesi 08:30–10:00 `tuprs_alarm.pine` / `tuprs.pine`. Bağlam: S&P 5.11'de −%4,36, VIX 16,6 → 28,2 → 25,6 (6.11) |
| | Bağımsız teyit (yeni): ABD enerji sanayi artığı (FF49 Oil − β·piyasa ≈ `AMEX:XLE`−β·`SP:SPX`) ABD t−1 → TUPRS t→t+1 | **FILTRE** | +15,8 bps/1σ, NW t 3,96 (IS 2,09 / OOS 3,10 / 2024+ 1,69), q 0,003; tek başına işlem 15,5 bps ile net +11 (t 1,0), IS negatif | French verisi ~1 ay gecikmeli (son 30.09) → canlıda `AMEX:XLE` ile göz kontrolü |
| **XU030 vadeli baz sıçraması** (1-3G TRADE mini) | Lead-lag değil, kapanış mikroyapısı: Δb = Δln(`BIST:XU030DZ2026`/`BIST:XU030`) | **KENAR** | net +14…+20 bps/işlem; OOS t 1,85; 2024–26 +17 (t 1,1); 1 gün geç giriş −2,5 [PL #1] | 6.11: b +405 bps, Δb **−41 bps**, std120(Δb) **68 bps** → z −0,61, sinyal yok. 9.11 eşiği **\|Δb\| > 68 bps** (yeni) |
| **SAHOL/AKBNK** (SWING K1) | Oran `BIST:SAHOL/BIST:AKBNK` z60 ±2 (çift, lead-lag değil) | **KENAR** (20 gün) | 1 gün gecikmeyle +160 / +310 bps/işlem (2010–18 / 2019–26), t 2,4 / 2,8 [VB #25] | z **−0,54**; tetik SAHOL ≥ 93,06 / ≤ 84,09, AKBNK ≤ 64,40 / ≥ 71,27 (diğeri sabit) |
| | `BIST:AKBNK`_t → SAHOL t→t+1 (yeni) | **FILTRE** (zayıf) | +22,4 bps/1σ, t 2,96 (IS 2,43 / OOS 1,73), q 0,03; tek bacak F_SAHOL net −4,6 bps | AKBNK 6.11 z +0,80 → sinyal yok |
| **ENJSA** (IZLE → K4) | Öncü yok. En yakın: `CME_MINI:ES1!` gece → açılış gap'i | **RISK** / öncülük **YOK** | ES gece → gap 0,21 [KART]; ENERY/AHGAZ_t → ENJSA t+1 t −1,9 / −1,7, q ≥ 0,29 (yeni) | Kapanış 122,00; K4 tetiği 127,00 (+%4,1) |
| **ENERY + AHGAZ** (IZLE → K4, tek isim) | Öncü yok. Senkron: birbirleri; `BIST:XELKT`; `BIST:XUTUM`−`BIST:XU100` | Öncülük **YOK**; senkron **FILTRE** | 18 öngörü testinde en iyi \|t\| 1,87, q ≥ 0,29; her kural maliyet sonrası negatif. Aynı gün artık korelasyon ENERY–AHGAZ **0,61** (son 1y 0,63); ENJSA ile 0,05 / −0,01 (yeni) | ENERY 14,05 (tetik 14,60, +%3,9) · AHGAZ 46,82 (tetik 48,70, +%4,0); bilanço 9.11 akşamı |
| **KCHOL** (IZLE → K4) | Öncü yok. Senkron: `BIST:ARCLK`/`FROTO`/`TOASO`, `BIST:SAHOL` | Öncülük **YOK**; ES gece **RISK** | `SP:SPX` t−1 → KCHOL t+1: +4 bps/1σ, t 0,86 (yeni); ES gece → gap 0,49 [KART] | 206,10; tetik 225,50 (+%9,4) ve SMA50 210,94 üstü şart |
| **RYSAS** (IZLE → K4) | `BIST:RYGYO`_t → `BIST:RYSAS` t→t+1 (iştirak/grup bağı) — **yeni** | **FILTRE** (kenar adayı) | +32,7 bps/1σ, t 3,15 (IS 1,30 / OOS 2,53 / 2024+ 3,17), q 0,02; 19 GYO plasebosunda en yüksek t 1,84. Kural net +34,8 (t 2,40) ama en iyi 10 işlem çıkınca +13,6 (t 1,04); 2014–23 t < 0,7 | RYGYO 6.11 z **+0,23** → yok. 9.11 eşiği: RYGYO kapanışı ≥ 50,61 (z>+1) / ≤ 47,63 |
| **BRSAN** (IZLE → K4) | Öncü yok. Senkron `BIST:BRYAT` | Öncülük **YOK**; gece **RISK** | BRYAT_t → t+1 t −0,78; ABD çelik (≈`AMEX:SLX`) t−1 → t+1 t 1,24 (yeni); ES gece → gap 0,27 [KART] | 682,00; tetik 769,50 (+%12,8) |
| **TRMET/TRALT Koza** (IZLE, kâğıt) | z3 = 3 günlük TRMET − β·ort(TRALT, TRENJ) artığı; `BIST:TRMET1!` / `BIST:TRALT1!` | **KENAR** (sönmüş → kâğıt) | P0L brüt +51,7 (t 3,0), net15+tik +28,8; 2024–26 net15+tik +1; 2026 −29 [RH-K §9.2] | z3 **+0,71** → yok. 9.11 tetiği (TRALT/TRENJ yatay): AL TRMET ≥ 116,76, SAT ≤ 105,54 |
| **Altın → TRALT** (IZLE, kâğıt) | `TVC:GOLD` 17:55 değişimi → `BIST:TRALT1!` + `BIST:XU030D1!` hedge, 2 gün | **KENAR** (DÜŞÜK) | 8+3 bps net +35,5 (t 2,20); 2024–26 +54 (t 1,96); en iyi 10 çıkınca t 0,94 [RH-A §8] | VİOP F_XAUUSD1226 uzlaşma vekili: 6.11 −%1,50 → z −0,88 (yok); 5.11 +%1,81 → z +1,07 (AL adayıydı, çıkış 9.11) |
| | ABD altın madencileri (FF49 Gold ≈ `AMEX:GDX`−β·`SP:SPX`) ABD t−1 → TRALT t→t+1 (yeni) | **YOK** (cc) / **RISK** | +4,7 bps/1σ, t 0,78; aynı bilgi BIST t günüyle pc 0,114 (q < 0,001): t gününde tükeniyor | — |
| **Kredi notu kararı → F_XU030** (IZLE, olay) | Karar sonrası ilk uzlaşmada kararın tersine, 2 gün; `BIST:XU030D1!` | **KENAR** (DÜŞÜK, olay; n=16) | net h2 +142 (t 2,93), Bonferroni p ≈ 0,14; son iki karar −217 / −53 [PL] | Takvim dosyalarda yok → teyit |

## 2. Veri ve doğrulama notları (önce oku)

- **İş Yatırım bağlantısı 07.11 gecesi kopuyordu** (proxy: `ws_closed_mid_exchange`, connection reset). Zorlanmadı. Bunun yerine aynı kaynaktan bu oturumda önceden indirilmiş önbellekler `leadlag2/isy/` altında birleştirildi (`01b_onbellek.py`): hisse HisseTekil (adj, 2009 → 05.11) + ChartData 06.11 kapanışı (06.11 20:53 TSİ'de indirilmiş).
- **Düzeltme:** `bist_test/endeks` önbelleği 06.11 **12:59 TSİ'de**, seans içinde indirilmiş; o günün endeks değerleri kapanış değil (ör. XU030 14.092 yerine kapanış 14.290; XU100 11.312 yerine 11.483). Satırlar atıldı; XU100, XU030 ve USDTRY için kapanış sonrası değer eklendi; XUTUM, XELKT, XGMYO ve XULAS 05.11'de bitiyor. İlk hesapta bu hata XU030 Δb'yi yanlış +98 bps (sinyal) gösteriyordu; doğrusu −41 bps (sinyal yok).
- FRED: SP500 05.11'e, Brent ve Henry Hub (EIA) 03.11'e kadar. CBOE VIX 06.11'e kadar. Ken French 49 sanayi 30.09'a kadar → FF tabanlı sinyaller **canlı değil**; yalnız geçmiş teyit için. VİOP bülteni 01.04–06.11 (150 gün; std120 için).
- Is Yatırım USDTRY'nin damga saati tanısı: corr(XU100_t, ΔUSD_t) −0,236; corr(XU100_t+1, ΔUSD_t) −0,010 → BIST kapanışıyla uyumlu kabul edildi.
- Yahoo ve Stooq kullanılmadı. Bu yüzden **TUPRS rafineri z'si ve TVC:GOLD 17:55 değeri hesaplanamadı**; ikisi de TradingView'dan okunur.

## 3. Enstrüman bazında (kart sürücüleri → etiket, yeni test, güncel değer, uygulama)

Kartların ORTA/YÜKSEK güvenli **bütün** sürücüleri etiketleriyle Ek A'da (117 satır: FILTRE 64, RISK 33, YOK 17, KENAR 3). Burada her isim için işe yarayanlar.

### 3.1 TUPRS — **KENAR** (ABD rafinerileri, kapanıştan kapanışa)

| Sürücü (TradingView) | İlişki | Sayı | Etiket |
|---|---|---|---|
| `NYSE:VLO`,`MPC`,`PSX`,`PBF` − β·`SP:SPX`, ABD t−1 → F_TUPRS t uzlaşma → t+2 | yavaş yayılma | Pratik kural 411 pozisyon, net8 +49,2 (t 2,53), net15 +42,2; IS +39,6 / OOS +58,2; **2024–26 +30,5 (t 0,90)**; en iyi 10 çıkınca +17 (t 1,0); 1 gün geç giriş +37 [RH-T §8] | **KENAR** |
| Aynı sinyalin gün içi sürümü (açılış seansı) [KART #5] | gün içi | hedge'li NW t 5,3; tek bacak net 8 bps OOS t 1,6; açılış seansı derinliği 3–15 kontrat | YOK (profil dışı) |
| (yeni) ABD enerji sanayi artığı, FF49 Oil (≈ `AMEX:XLE`−β·`SP:SPX`), ABD t−1 → t→t+1 | yavaş yayılma | +15,8 bps/1σ, t 3,96 (IS 2,09 / OOS 3,10 / 2024+ 1,69), q 0,003; 2 gün +22,6 bps/1σ, t 3,80. Rehber yapısıyla (hedge'siz, 2 gün, 15,5 bps) net +11 (t 1,0): IS −6, OOS +36 (t 1,8), en iyi 10 çıkınca −3 | **FILTRE** |
| (yeni) Brent (`ICEEUR:BRN1!`; veri EIA), ABD t−1 → t→t+1 | yavaş yayılma? | +10,4 bps/1σ, t 2,23 (IS 0,51 / OOS 2,68), q 0,19 → FDR'den geçmiyor; işlem net −1,9 | YOK |
| `ICEEUR:BRN1!` senkron [KART #0] | senkron | XU100 kısmi 0,158 (son 1y 0,45; haftalık 0,27) | FILTRE (konum) |
| `BIST:AYGAZ` senkron [KART #3] | senkron | pc 0,278 (yılların %100'ü); AYGAZ t−1 → TUPRS gün içi t 0,74 | FILTRE |
| Brent gece → açılış gap'i [KART #6] | gap | corr 0,577 (NW t 5,6); sonraki gün içi −0,09 | RISK |
| `BIST:XU030D1!` hedge | — | TUPRS'ta işe yaramıyor, gece riskini artırıyor [PL §3] | kullanma |

- **Okuma:** FF49 Oil testi, ABD bilgisinin TUPRS'a BIST t günü içinde bitmeden yayıldığını bağımsız ve izinli veriyle teyit ediyor (rafineri bulgusunun yapısı doğru). Ama genel enerji sinyali rafineri sepetinden zayıf (IS'de işlem negatif); kenarı taşıyan rafineri sepeti. Bu, kartın açık sorusuyla ("XLE'den arındırılmış rafineri kısmı IS'de t 1,65") tutarlı.
- **Uygulama:**
  - Pazartesi 08:30–10:00: TradingView `BIST:TUPRS1!` günlük grafiğinde `rehber/tuprs/tuprs_alarm.pine` (ya da `tuprs.pine`). Sinyal ABD Cuma 6.11 kapanışından. |z| > 1 ise 18:00–18:10'da F_TUPRS1226'da z yönünde 1–2 kontrat, **kâğıtta** (Kural 0).
  - FILTRE kullanımı: rafineri z'si ile `AMEX:XLE`'nin `SP:SPX`'e göre önceki gün artığı ters işaretliyse boyutu yarıya indir. Bu kombinasyon **test edilmedi**; yalnız güven ayarı.
  - 03.11 kısa pozisyonunun (z −1,47) 05.11 UZAT/KAPAT kararı dosyalarda yok → betikle kontrol.
- **06.11:** F_TUPRS1226 uzlaşma 354,65 (hacim 106 mn TL, AP 3.403); F_TUPRS1126 344,55 (2.168 mn TL, AP 94.540).

### 3.2 XU030 vadeli kapanış bazı — **KENAR** (mikroyapı, lead-lag değil)

- **Kural [PL #1]:** 18:10'da b = ln(F_XU0301226 son fiyat / XU030 spot kapanış), Δb = b − dünkü b (aynı vade). |Δb| > 1·std120(Δb) ise ters yön; 18:10–18:15 limitli giriş, ertesi gün uzlaşmada çıkış. Aynı akşam yapılmazsa hiç yapılmaz.
- **Güncel (yeni, bülten kapanış fiyatıyla; `06_baz_std.py`):**

| Gün | F_XU0301226 kapanış | XU030 spot | b (bps) | Δb (bps) |
|---|---|---|---|---|
| 03.11 | 14.411 | 13.754,46 | +466 | −21 |
| 04.11 | 15.026 | 14.330,93 | +474 | +7 |
| 05.11 | 14.745 | 14.101,00 | +447 | −27 |
| 06.11 | 14.881 | 14.290,21 | +405 | −41 |

  std120(Δb) = **68 bps** (NET_LISTE'deki "~50 bps"tan yüksek; fon krizi oynaklığı). 6.11 z −0,61 → sinyal yok. **9.11 eşiği |Δb| > 68 bps**, yani F/spot oranı ln-bazı +337 bps'in altına inerse AL, +473'ün üstüne çıkarsa SAT (hesap: 405 ± 68).
- Küresel bağ: `CME_MINI:ES1!` gece → XU030 gap 0,45–0,47 → **RISK**. VİOP akşam seansı (XU030D) gece bilgisinin yalnız %24–44'ünü görüyor; akşam seansı hareketinin ertesi güne öngörüsü yok (corr −0,04) [PL §2].
- TradingView: `BIST:XU030DZ2026/BIST:XU030` (15 dk gecikmeli → karar aracı kurumun canlı ekranından).

### 3.3 SAHOL / AKBNK — **KENAR** (K1, 20 gün); lead-lag'ler FILTRE/RISK

| Sürücü (TradingView) | Sayı | Etiket |
|---|---|---|
| Oran `BIST:SAHOL/BIST:AKBNK` z60 ±2, ertesi gün giriş, 20 gün [PB K1] | +160 / +310 bps/işlem (1 gün gecikmeli), 20 bps ile ~+140 / +290 | **KENAR** |
| (yeni) `BIST:AKBNK`_t → SAHOL t→t+1 (kendi ve XU100 kontrollü) | +22,4 bps/1σ, t 2,96 (IS 2,43 / OOS 1,73 / 2024+ 2,68), q 0,03; \|z\|>1 tek bacak F_SAHOL hedge'li: brüt +10,9, net −4,6 (t −0,9). Kart: gün içi t 3,6, net 8 bps OOS +3,8 | **FILTRE** (zayıf): K1'e dokunmaya değmez (≈11 bps vs 140–290) |
| SAHOL–AKBNK senkron | pc 0,28 (yeni; son 1y 0,53) | FILTRE (K1'in temeli) |
| `CME_MINI:ES1!`/`NQ1!` gece, `NASDAQ:TUR`, `CBOE:VIX`_t−1, `TVC:NI225` | ES → gap 0,47; TUR → XBANK gap 0,36; VIX_t−1 → cc −0,083 (yalnız gap kanalı) | RISK |
| (yeni) `SP:SPX` ABD t−1 → SAHOL t→t+1; `CBOE:VIX` → AKBNK t→t+1 | t 0,66 / −1,27 → gap'ten sonra kalıntı yok | YOK |
| `TVC:TR05Y`/`TR10Y` (DİBS) ve `BIST:USDTRY1!` senkron | AKBNK 5y pc −0,157; USDTRY −0,166 (2025-03 sonrası ≈0) | FILTRE (boyut; PPK/A7) |

- **06.11:** z **−0,54**. Tam tetikler (öbür bacak sabitken): z = +2 → SAHOL ≥ 93,06 ya da AKBNK ≤ 64,40; z = −2 → SAHOL ≤ 84,09 ya da AKBNK ≥ 71,27 (yeni hesap = [SİN]). Aralık kontratları: F_SAHOL1226 91,41, F_AKBNK1226 71,77.

### 3.4 ENJSA — öncülük **YOK**; gece **RISK**; küme **FILTRE**

- Kart: küresel bağ yok (E.ON pc 0,03, TTF 0,007). ES/NQ gece ve KOSPI/Nikkei → gap 0,21–0,27 (RISK). `BIST:AKSEN` pc 0,104, `BIST:XELKT` corr 0,67 (FILTRE, küme). Kendi kapanış müzayedesi hareketi ertesi sabah geri dönüyor (O→07:30 b −0,58, t −4,3, FDR) → **yalnız spot K4 yürütmesinde FILTRE:** 18:00–18:10 müzayedesinde sert yükselen günde kapanıştan alma; VİOP'ta uygulanamaz. Gap fade ve SAHOL açılış ayrışması açılış emri ister → YOK.
- Yeni: ENERY_t / AHGAZ_t → ENJSA t→t+1: −16,2 / −16,2 bps/1σ, t −1,91 / −1,71, q 0,29 / 0,37 → **YOK**. Aynı gün artık korelasyon ENJSA–ENERY 0,05, ENJSA–AHGAZ −0,01; ham 0,27 / 0,19; 5 günlük ham 0,22 / 0,09.
  - **Plan için bilgi (FILTRE):** [PB §4.3] ENJSA ile AHGAZ/ENERY'yi "korelasyonu ölçülmedi, ihtiyaten tek küme" sayıyor. Ölçülen bağ çok zayıf, ayrı küme sayılabilirler. Karar planın; bu rapor kuralı değiştirmiyor.
- **06.11:** 122,00; K4 tetiği 127,00 (+%4,1). F_ENJSA1226 uzlaşma 124,35 (spota göre +%1,9; NET_LISTE'deki temettü/ima faizi kontrolü geçerli).

### 3.5 ENERY + AHGAZ (tek isim) — kartsız; **yeni test**: öncülük **YOK**, senkron **FILTRE**

Önceden belirlenmiş liderler (her biri için aynı model): birbirleri, `BIST:ENJSA`, `BIST:AKSEN`, `BIST:AYGAZ`, `BIST:XELKT`, `BIST:XUTUM`−`BIST:XU100`, `FX:USDTRY`, Henry Hub (`NYMEX:NG1!`; veri FRED DHHNGSP), Brent (`ICEEUR:BRN1!`). Örneklem kısa: AHGAZ 01.2023+, ENERY 09.2023+ (ilk 20 gün atıldı); IS ≤ 2024 / OOS 2025+.

| Ölçü | ENERY | AHGAZ | Etiket |
|---|---|---|---|
| Öngörü (t→t+1), en güçlü | AKSEN −21,5 bps/1σ, t −1,87 (q 0,29); AYGAZ +15,3, t 1,42 | Brent −12,0, t −1,48 (q 0,48) | **YOK** |
| Öngörü, diğerleri | \|t\| ≤ 0,78 | \|t\| ≤ 0,91 | YOK |
| \|z\|>1 kuralları (25+3 bps) | 9 kuralın 9'u net negatif (−3 … −62 bps) | 9 kuralın 8'i negatif; Brent +1,9 (t 0,12) | YOK |
| Aynı gün, birbirleriyle | pc **0,613** (IS 0,61 / OOS 0,61 / son 1y 0,63); ham 0,65 | aynı | **FILTRE** (tek isim; ikisinden biri) |
| Aynı gün `BIST:XELKT` | 0,46 | 0,41 | FILTRE (sektör; kısmen mekanik içerme) |
| Aynı gün küçük-orta ölçek (`XUTUM`−`XU100`) | 0,20 (son 1y 0,12) | 0,21 (0,08) | FILTRE (rejim) |
| ENJSA / AKSEN / AYGAZ aynı gün | 0,05 / 0,09 / 0,00 | 0,04 / 0,05 / 0,00 | YOK |
| `NYMEX:NG1!` (HH) → BIST gap günü | 0,098 (q 0,016) | 0,013 | RISK (zayıf, yalnız ENERY) |
| `FX:USDTRY`, Brent | ≈0 | ≈0 | YOK |

- **Uygulama:** Lead-lag ile işlem yok. K4'te ikisinden yalnız biri (0,61'lik bağ "tek isim" kuralını doğruluyor). İkisi aynı gün tetiklerse likidite sırası yüksek olan [PB §4.3]. Aktif ihraççı geri alımı yalnız bayrak.
- **06.11:** ENERY 14,05 (+%1,81; tetik 14,60, +%3,9), AHGAZ 46,82 (+%1,78; tetik 48,70, +%4,0). Bilanço 9.11 akşamı (A1) → ilk karar 10.11, giriş en erken 16.11 (A2/A4; VİOP-47 dışı long 30.11).
- TradingView: `BIST:ENERY` (doğrulandı), `BIST:AHGAZ` ([TV]'de yok; kalıp, arama kutusunda teyit), `BIST:XELKT`, `BIST:XUTUM`, `NYMEX:NG1!`.

### 3.6 KCHOL — öncülük **YOK**; gece **RISK**; iştirakler **FILTRE**

- Kart: ES/NQ gece → gap 0,49, VIX_t−1 → cc −0,085 (gap kanalı), TUR, Nikkei 0,41 → RISK. İştirakler `BIST:ARCLK` 0,157 / `BIST:FROTO` 0,152 / `BIST:TOASO` 0,120 (17/17 yıl), `BIST:SAHOL` 0,25, `BIST:TUPRS` 0,117, `BIST:YKBNK` 0,122 → FILTRE (göreli değer/hedge). İştirak_t → KCHOL_t+1 ≈0. NAV iskontosu (VİOP t 1,0–1,5) ve açılış NAV ayrışması (OOS −6 bps) DÜŞÜK → YOK. Hedge: `BIST:XU030D1!` KCHOL'de iyi çalışıyor [PL §3].
- Yeni: `SP:SPX` ABD t−1 → KCHOL t→t+1: +4,1 bps/1σ, t 0,86 → YOK (gap'ten sonra kalıntı yok).
- **06.11:** 206,10; K4: kapanış > 225,50 (+%9,4) ve > SMA50 210,94. Bilanço 9.11. F_KCHOL1226 215,70. K2 kâğıt.

### 3.7 RYSAS — kartsız; **yeni**: `BIST:RYGYO` → RYSAS **FILTRE (kenar adayı)**

Önceden belirlenmiş liderler: `BIST:RYGYO` (Reysaş GYO, grup iştiraki), `BIST:XGMYO`, `BIST:XULAS`, `BIST:XUTUM`−`BIST:XU100`, `FX:USDTRY`, Brent. Örneklem 2014–2026 (IS 2014–20 / OOS 2021–26).

| Ölçü | Sonuç |
|---|---|
| RYGYO_t → RYSAS t→t+1 (kendi + XU100 kontrollü) | **+32,7 bps/1σ, NW t 3,15** (IS +19,9, t 1,30 / OOS +35,3, t 2,53 / 2024+ t 3,17); BH **q 0,02** (38 testin içinde) |
| Plasebo: 19 diğer GYO → RYSAS | medyan t −0,38; \|t\| > 2 olan yok; en yüksek +1,84 → bağ RYGYO'ya özgü |
| Ters yön RYSAS_t → RYGYO | net +9 bps (t 0,69) |
| Kural: \|z_RYGYO\| > 1, yön z, RYSAS − β·XU100, 1 gün, 25+3 bps | n 793; brüt +62,8; **net +34,8 (t 2,40)**; OOS +56,5 (t 2,98) |
| Dönemler (net) | 2014–20 +14,6 (t 0,67) · 2021–23 +18,3 (t 0,65) · **2024–26 +97,5 (t 3,92)**; brüt yıllar 2014 −60, 2015 −16, 2019 +130, 2020 +186, 2025 +171, 2026 +112 |
| Çürütme | En iyi 10 işlem çıkınca net +13,6 (t 1,04) · Ağu–Eki 2026 hariç +36,1 (t 2,44) · RYGYO limit günleri hariç +26,0 (t 1,98) · **1 gün geç giriş −15,8** (bilgi tek günde tükeniyor) |
| Yalnız uzun (spot açığa satış yok) | hedge'li net +56,0 (t 2,80); hedge'siz +64,3 (t 3,17) |
| Diğer liderler (öngörü) | XGMYO −7,1 (t −0,60), XULAS +9,8 (t 0,99), küçük-orta ölçek −4,0, USDTRY −2,8, Brent +7,2 → YOK |
| Aynı gün (FILTRE) | RYGYO pc 0,605 (son 1y 0,45), küçük-orta ölçek 0,275, XGMYO 0,243, XULAS 0,115 (son 1y 0,27) |

- **Neden KENAR değil:** Kâr birkaç büyük işlemde yoğun (en iyi 10 çıkınca t 1,0), 2014–23'te maliyet sonrası anlamsız, güç yalnız 2024–26'da. Mekanizma makul ama kanıtlanmadı. Ekonomik bağlı firmalarda gecikmeli yayılım (Cohen–Frazzini, Menzly–Ozbas; takip azaldıkça büyür, yayımdan sonra aşınır [dalga_abd §2]) ya da grup düzeyinde akım. Tek başına test, sonradan seçim riski düşük ama sıfır değil.
- **Uygulama (FILTRE):**
  - K4 RYSAS girişi (tetik 30,28) zaten t+1 kapanışında. Giriş günü RYGYO z < −1 ise (RYGYO kapanışı dünkünden ~%3 aşağı) o akşam girme, bir gün bekle. Giriş günü z > +1 ise öne alma yok, kural aynı. Bu kullanım K4 ile birlikte **test edilmedi**.
  - Kâğıt izleme (2–3 ay): RYGYO kapanışı ±1σ'yı (bugün ±%3,03) aşınca RYSAS'ı 18:10–18:15 KFİ'de kapanış fiyatından al (yalnız uzun), ertesi kapanışta sat; XU030 hedge'i isteğe bağlı.
- **06.11:** RYGYO 49,10 (+%0,69), sd250 %3,03 → z +0,23, sinyal yok. 9.11 eşiği RYGYO ≥ 50,61 / ≤ 47,63. RYSAS 27,34; K4 tetiği 30,28 (+%10,8). RYSAS bilançosu 9.11 akşamı (A1) → 9.11'de giriş yok.
- TradingView: `BIST:RYGYO` (doğrulandı), `BIST:RYSAS` ([TV]'de yok; kalıp, teyit), `BIST:XGMYO`, `BIST:XULAS`.

### 3.8 BRSAN — öncülük **YOK**; gece **RISK**; BRYAT **FILTRE**

- Kart: ES/NQ/TUR gece → gap 0,27/0,29/0,16, Nikkei 0,30 → RISK. `BIST:BRYAT` pc 0,56 (yılların %100'ü) → FILTRE (VİOP'ta yok, hedge değil). Asya çelik/FMG (`ASX:FMG`, `TSE:5411`) gün içi t 3,5 ama kazanç ilk 30 dk'da, 07:30 girişte negatif → RISK. Metal akranlarının açılış gap'ine yetişme ve kendi gap fade'i açılış ister → YOK. Tavan: 2020-03'ten beri 75 tavan kapanışı (VİOP-47'de en çok) → RISK (kilit; %25 stop ile boy).
- Yeni: BRYAT_t → BRSAN t→t+1 −8,5 bps/1σ, t −0,78 (OOS t −2,13, işaret dönüyor); ABD çelik sanayi artığı (FF49 Steel ≈ `AMEX:SLX`−β·`SP:SPX`) t−1 → t+1 +6,9, t 1,24 → YOK.
- **06.11:** 682,00; tetik 769,50 (+%12,8). F_BRSAN1226 705,30 (AP 317; ince).

### 3.9 TRMET / TRALT Koza göreli momentum — **KENAR** (sönmüş → kâğıt)

- **Kural [RH-K §1]:** u = r_TRMET − β_g·ort(r_TRALT, r_TRENJ); z3 = (u_t + u_t−1 + u_t−2)/(σ60·√3); |z3| > 1,5 → TRMET1! z yönünde + β_TA ≈ 0,69 nominal TRALT1! ters; 17:50–17:55 canlı fiyatla, 18:00–18:10 giriş, 2 gün (uzatmayla en çok 6).
- Lead-lag tarafı:
  - Klasik öncülük yok: TRALT(t−1) → TRMET 2022–26 −0,13 (t −2,4) [RH-K §9.5].
  - Kartın grup içi ters dönüşü (TRALT+TRENJ artığı t−1 → TRMET gün içi −21,6 bps/σ, t −4,59) kapanıştan kapanışa, kendi ve XU100 kontrollü: −25,7 bps/1σ, t −1,63 (IS −1,11 / OOS −1,22), q 0,39 (yeni). Tek başına FDR'den geçmiyor. Uygulanabilir biçimi zaten z3 kuralı → **FILTRE (kural içinde)**.
  - Senkron (FILTRE): TRMET–TRENJ 0,74, TRMET–TRALT 0,62; grup ortalamasıyla 0,845 (yeni). Altın (`COMEX:GC1!`/`TVC:GOLD`) TRMET pc 0,13, dolaylı.
  - Koza olay riski (kayyum, TVF devri, birleşme kararı ve iptali: CAR −%10…−%41) → RISK. Kurumsal olay günü ve ertesi işlem yok.
- **06.11 (yeni, `pr_koza` ile):** z3 **+0,71** (u +130 bps, σ60 195 bps, β_g 0,88, β_TA 0,69) → sinyal yok, açık pozisyon yok (son işlem 23–25.09). 9.11 kapanışı için tetik (TRALT/TRENJ yatay kalırsa): **AL TRMET ≥ 116,76** (6.11 111,90; +%4,3), **SAT ≤ 105,54**. 9.11 bilanço belirsizliği nedeniyle canlı giriş yok [NET_LISTE §1.4]. F_TRMET1226 118,05 (hacim 9 mn TL; ince), F_TRALT1226 39,66.
- TradingView: `BIST:TRMET1!`, `BIST:TRALT1!`, `BIST:TRENJ`, `rehber/koza/koza.pine` / `koza_alarm.pine` (`BIST:XU030` günlük grafiğinde).

### 3.10 Altın → TRALT — **KENAR** (DÜŞÜK, rejime bağlı)

- **Kural [RH-A §1]:** g = ln(`TVC:GOLD` 17:55 / önceki BIST günü 17:55), z = g/σ250 (σ ≈ %1,70). z > +1 → TRALT1! AL + XU030D1! SAT (N = yuvarla(10·XU030/(β·100·TRALT)); bugün β 1,30 → **N ≈ 29**); z < −1 tersi; 2 gün.
- Lead-lag değil, eksik aynı gün tepkisi: altın katsayısı t 2,84, TRALT'ın kendi hareketi t 0,29 [RH-A §9].
- Kart sürücüleri: `COMEX:GC1!` senkron pc 0,21 (15:00 UTC 0,30; son 1y 0,34; 2023Y2–2024Y2 bağ yok) → FILTRE. Altın madencileri sepeti t−1 → TRALT gün içi 19,4 bps/σ (t 4,39, 47 hissede 1.) → RISK: t gününde fiyatlanıyor. Yeni test de bunu teyit ediyor: FF49 Gold artığı ABD t−1 → TRALT t→t+1 +4,7 bps/1σ, t 0,78; aynı bilgi BIST t günüyle pc 0,114 (q < 0,001). Gece altın ve ES → gap → RISK.
- **06.11 (VİOP F_XAUUSD1226 uzlaşma vekili; pratik sinyal TVC:GOLD 17:55, elde yok):** 6.11 −%1,50 → z −0,88, sinyal yok. 5.11 +%1,81 → z +1,07, AL adayıydı. Kâğıtta açıldıysa planlı çıkış 9.11 18:00–18:10.
- TradingView: `TVC:GOLD` (yedek `OANDA:XAUUSD`), `BIST:XAUUSD1!` (bağlam), `BIST:TRALT1!`, `BIST:XU030D1!`, `rehber/altin/altin.pine`. `COMEX:GC1!` sinyal için kullanılmaz (vade sıçraması).

### 3.11 Kredi notu kararı → F_XU030 — **KENAR** (DÜŞÜK, olay)

- Not kademesi değişince tepki gününün uzlaşmasında kararın tersine, 2 gün. n=16; 8 bps ile net h2 +142 (t 2,93), isabet %75; en iyi 3 olay çıkınca +94 (t 1,87); Bonferroni p ≈ 0,14; son iki karar −217 (S&P 2024-11) ve −53 (Moody's 2025-07). Lead-lag değil. 2000–13 ve diğer EM'lerde çalışmıyor [LL].
- Güncel: karar takvimi dosyalarda yok → aracı kurum ya da ajans takviminden teyit. 1 kontrat ya da kâğıt. `BIST:XU030D1!`.

## 4. Yeni testlerin tasarımı ve FDR

- **Önceden belirlenmiş set (sonuçlara bakmadan yazıldı, `02_test.py` başlığı):**
  - Aile P, öngörü: 38 test. 24'ü kartsız üç isim için (ENERY 9, AHGAZ 9, RYSAS 6). 14'ü yeniden kontrol (ENJSA←ENERY/AHGAZ; TUPRS←FF49 Oil ve Brent, 1 ve 2 gün; KCHOL/SAHOL←SPX; SAHOL←AKBNK; AKBNK←VIX; BRSAN←FF49 Steel ve BRYAT; TRMET←Koza grubu; TRALT←FF49 Gold).
  - Aile S, senkron/gap günü: 36 test.
- **Model:** r(t→t+1) = a + b·L_t + c·r_hedef,t + d·r_XU100,t, NW(5). Lider z'si ±5'te kırpıldı. Hisse getirileri log; |basit getiri| > limit (%10,5; 13.03.2020 öncesi %20,5) ise NaN; hacim 0 günü bayat; halka arzdan sonraki ilk 20 gün atıldı.
- **Tek işlem kuralı:**
  - |z_L| > 1 → yön = işaret(b_IS)·işaret(z). Yön yalnız IS'den seçildi, OOS yön seçimine karışmaz.
  - Hedef − β250·XU100, 1 gün.
  - Maliyet gidiş-dönüş: spot 25 + hedge 3 bps; VİOP 12,5 + 3 bps.
- **FDR (BH, aile içinde):** Aile P'de q < 0,05 dört test: TUPRS←FF49 Oil (1 ve 2 gün, q 0,003), RYSAS←RYGYO (q 0,02), SAHOL←AKBNK (q 0,03). Maliyet sonrası pozitif ve OOS'ta anlamlı tek kural RYSAS←RYGYO (§3.7). Kartsız enerji isimlerinde (ENERY, AHGAZ) 18 testin hiçbiri q < 0,29 değil.
- **Duyarlılık:** `02b_rysas_saglamlik.py` (7 çürütme), `02c_tuprs_duyarlilik.py` (rehber yapısıyla 1/2/3 gün × 8/15,5 bps). Bunlar etiket seçimine girmedi, yalnız etiketin dayanıklılığını gösterir.

## 5. Pazartesi 9.11: TradingView kurulumu ve saat akışı (lead-lag kısmı)

| Saat (TSİ) | Ne | TradingView / kaynak |
|---|---|---|
| 08:30–10:00 | TUPRS rafineri z'si (ABD Cuma 6.11). \|z\|>1 → kâğıda yaz, 18:00–18:10 F_TUPRS1226 | `tuprs_alarm.pine` `BIST:TUPRS1!` günlük; bağlam `AMEX:XLE`, `AMEX:CRAK`, `ICEEUR:BRN1!` |
| Gün içi | Hiçbir gece sürücüsünü (`CME_MINI:ES1!`, `NASDAQ:TUR`, gece altın/Brent) sinyal sayma; yalnız gap/risk bilgisi | — |
| 17:50–17:55 | Koza z3 canlı (tetik TRMET ≥ 116,76 / ≤ 105,54); `TVC:GOLD` 17:55 değişimi (±%1,70) | `koza_alarm.pine`; `TVC:GOLD` |
| 18:00–18:10 | F_TUPRS / Koza / altın uzlaşma penceresi. 9.11 bilanço gecesi → Koza ve altında canlı giriş yok | aracı kurum ekranı |
| 18:10–18:15 | XU030 Δb (eşik ±68 bps; b dün +405 bps) | `BIST:XU030DZ2026/BIST:XU030` + canlı ekran |
| 18:15 sonrası | K1 z (tetikler §3.3); RYGYO z (≥ 50,61 / ≤ 47,63) yalnız K4 RYSAS filtresi ve kâğıt; K4 kapanış alarmları (ENJSA 127,00 · ENERY 14,60 · AHGAZ 48,70 · KCHOL 225,50 · RYSAS 30,28 · BRSAN 769,50) | `bist_sinyal.py` / `gunluk_oneri.py`; `03_guncel.py` |

İzleme listesi (bu rapora göre, lead-lag kısmı): `NYSE:VLO`, `NYSE:MPC`, `NYSE:PSX`, `NYSE:PBF`, `SP:SPX`, `AMEX:XLE`, `ICEEUR:BRN1!`, `BIST:TUPRS1!`, `BIST:XU030DZ2026`, `BIST:XU030`, `BIST:SAHOL`, `BIST:AKBNK`, `BIST:SAHOL1!`, `BIST:AKBNK1!`, `BIST:TRMET1!`, `BIST:TRALT1!`, `BIST:TRENJ`, `TVC:GOLD`, `BIST:XU030D1!`, `BIST:RYGYO`, `BIST:RYSAS`, `BIST:ENERY`, `BIST:AHGAZ`, `BIST:XELKT`, `BIST:ENJSA`, `BIST:KCHOL`, `BIST:BRSAN`, `BIST:BRYAT`; yalnız risk için `CME_MINI:ES1!`, `CBOE:VIX`, `NASDAQ:TUR`.

**RISK bağlamı (sinyal değil):** ABD 5.11'de S&P 500 −%4,36 (7.688,62 → 7.353,73), VIX 16,61 → 28,18; 6.11 VIX 25,64. BIST 6.11'de XU100 +%1,32 kapandı; gap fiyatlandı ve döndü. Cuma ABD kapanışı FRED'de henüz yok → Pazartesi açılış beklentisi için `CME_MINI:ES1!`.

## 6. Sınırlamalar

- Kartsız isimlerin (ENERY 3,2 yıl, AHGAZ 3,9 yıl) örneklemi kısa; "YOK" sonucu "küçük etkiyi dışlayamıyor" anlamında.
- RYSAS←RYGYO 38 testten biri ve FDR'den geçti. Yine de etki 2024–26'ya ve birkaç büyük işleme yığılı. Spot KFİ seansının derinliği gözlenmedi.
- FF49 sanayi serileri canlı değil. TradingView karşılıkları (`AMEX:XLE`, `AMEX:SLX`, `AMEX:GDX`) aynı şey değil, yalnız vekil.
- EIA Brent/HH tarih damgası (ABD günü) ICE Brent uzlaşmasıyla birebir değil; yön olarak muhafazakâr. Brent'in gece kısmı zaten RISK.
- Maliyetler model (spot 25, VİOP 12,5 bps). Bireysel komisyonla (bacak başına ~22 bps) [PL §5] KENAR'ların yarısı gider.

## 7. Dosyalar

- Kod: `hesaplar/leadlag_uygulama/`
  - `01_veri.py`: FRED, CBOE, Ken French, VİOP; İş Yatırım `--isy` ile.
  - `01b_onbellek.py`: aynı kaynaklı önbellek birleştirme ve seans içi satır düzeltmesi.
  - `ortak.py`.
  - `02_test.py`: aile P ve S.
  - `02b_rysas_saglamlik.py`, `02c_tuprs_duyarlilik.py`.
  - `03_guncel.py`: K1, Koza, altın vekili, XU030 Δb, RYGYO z, K4 uzaklıkları; `uygulama/kod/gunluk_oneri.py` ve `bist_sinyal.py` fonksiyonları kullanılır.
  - `04_kart_tablolari.py` (Ek A), `05_md_tablolar.py` (Ek B), `06_baz_std.py` (std120).
- Ham veri ve çıktılar (depoda değil): `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/leadlag2/` (`isy/`, `fred/`, `cboe/`, `french/`, `viop/`, `sonuc/aile_P.csv`, `aile_S.csv`, `rysas_saglamlik.txt`, `tuprs_duyarlilik.txt`, `guncel.txt`, `xu030_baz.csv`, `korelasyon_enerji.csv`).
- Yeniden çalıştırma (İş Yatırım açıkken): `python3 01_veri.py --veri <leadlag2> --isy && python3 02_test.py --cikti <leadlag2>/sonuc && python3 03_guncel.py --cikti <leadlag2>/sonuc && python3 06_baz_std.py`.

## Ek A. Kart sürücüleri (yalnız ORTA ve YÜKSEK güven) → bu profilin etiketi

Kaynak `2026-11-02_viop_leadlag/hisse_kartlari/<KOD>.json`. Sayılar kısaltıldı; tam metin kartta. Eşleme kuralı `hesaplar/leadlag_uygulama/04_kart_tablolari.py` başlığında. Kartı olmayanlar: ENERY, AHGAZ, RYSAS (§3).

Etiket sayımı (8 kart, ORTA+YÜKSEK): FILTRE 64, KENAR 3, RISK 33, YOK 17.

### TUPRS (`BIST:TUPRS`, `BIST:TUPRS1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | Brent ham petrol (aynı bilgi: WTI CL=F, BNO, USO, GSG/DBC emtia sepet… | `ICEEUR:BRN1!` | senkron | XU100-kısmi pc 0,158 (IS 0,10 / OOS 0,26 / son 1y 0,45; yılların 14/17'si +); ham corr 0,17 (3y 0,22, 1y 0,34); beta 0,157 (t 9,1); haftalık pc 0,27 (IS 0,18 / OOS 0,40)… | hayır (senkron; konumlama/hedge bilgisi) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 1 | Avrupa rafineri sepeti — AYLIK USD (PKN, MOL, MOH, ELPE, NESTE, GALP,… | `GPW:PKN, BET:MOL, ATHEX:MOH, ATHEX:ELPE, OMXHEX:NESTE, EURO…` | senkron | aylık USD kısmi korelasyon 0,43 (IS 0,32 / OOS 0,58) | hayır (aylık senkron) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 2 | BIST piyasa faktörü (XU100 / XU030) | `BIST:XU100` | senkron | v4 XU100 betası tam 0,85 (IS 0,76 / OOS 0,90 / 3y 0,66 / 1y 0,48); corr tam 0,61, 1y 0,30; XU100 Shapley varyans payı tam %20,2 (2021–23 %29,1, son 1y %5,7); XU030 corr… | evet (hedge bacağı: BIST:XU030D1!) — sinyal değil | YUKSEK | **FILTRE** | piyasa baglami; XU030 hedge'i TUPRS'ta ise yaramiyor, gece riskini artiriyor [PL s3] |
| 3 | AYGAZ (Koç kardeş şirket; Tüpraş'ın dolaylı ortağı) | `BIST:AYGAZ` | senkron | pc 0,278 (IS 0,22 / OOS 0,39; yılların %100'ü +); ham corr 0,52 (1y 0,66); haftalık pc 0,31; tam faktör kontrollü kısmi 0,32 (q 1e-39; OOS t 12,6) | hayır (AYGAZ VİOP'ta yok; senkron) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 4 | VİOP TUPRS vadeli açılışı (09:30) → spot açılış müzayedesi | `BIST:TUPRS1!` | mikroyapi | corr 0,57, R² 0,33; spot gün-içi kalıntısı b 0,02 (t 0,41); artık → gün-içi t −0,21 | hayır — tahmin edilen şey spot açılış fiyatının kendisi; gün-içi kalıntı yok (işlem güven… | YUKSEK | **YOK** | yalniz acilis icrasi |
| 5 | ABD rafineri/enerji hisseleri t−1 → TUPRS gün-içi (US_REF = VLO, MPC,… | `NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF` | gunici_oncu | XU100-hedge'li gün-içi NW t tam 5,3 / IS 3,1 / OOS 4,35; ES+Brent kontrollü 4,5 / 2,0 / 3,9; tüm ortak faktörler (XLE, emtia, BIST gecikmeleri) kontrollü 3,4 / 1,5 / 2,7… | sınırda — istatistik ORTA, işlem DÜŞÜK (tek bacak); yalnız VİOP açılış seansında, küçük b… | ORTA | **KENAR** | kapanis->kapanis surumu (US t-1 -> F_TUPRS t uzlasma -> t+2) rehberde test edildi: net +42 bps (8 bps), 2024-… |
| 6 | Brent gece hareketi (BIST kapanışı 15:00 UTC → açılış 07:00 UTC) | `ICEEUR:BRN1!` | gap_oncu | TUPRS gap ile corr 0,577 (NW-t 5,6), XU100 gap kontrollü 0,664, n=558 (2024-06+); yarıyıllar 0,18 / 0,55 / 0,22 / 0,82 / 0,32 (hepsi +); /Brent/>%1 günlerinde 0,62, küçü… | hayır — açılış gap'inde fiyatlanıyor; VİOP pay vadelisinde akşam seansı yok | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 7 | Avrupa petrol & rafineri hisseleri — GÜNLÜK (EQNR, AKRBP, BP, NESTE,… | `OSL:EQNR, OSL:AKRBP, LSE:BP., OMXHEX:NESTE, GPW:PKN, BME:RE…` | senkron | tarama tekil pc: EQNR 0,185 (IS 0,105 / OOS 0,27; 1y 0,44; yılların %100'ü), AKRBP 0,166, BP 0,158, NESTE 0,156, PKN 0,152, REP 0,152, ENI 0,151, TTE 0,147, SHEL 0,147,… | hayır (senkron; Avrupa kapanışı BIST'ten 0,5–1,5 saat sonra) | ORTA | **FILTRE** | zayif: ortak faktor kontrolunde ~0 (dolayli bag); oncu degil |
| 8 | VanEck rafineri ETF (CRAK) | `AMEX:CRAK` | senkron | ham pc 0,172 (IS 0,145 / OOS 0,221 / 1y 0,352), haftalık 0,316, yıl 11/11; CRAK TUPRS'u ~%3,9 içeriyor → TUPRS çıkarılmış CRAK pc 0,121 (IS 0,099 / OOS 0,164 / 1y 0,289)… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 9 | ABD entegre petrol/hizmet/altyapı hisseleri (OXY, COP, XLE, XOM, CVX,… | `AMEX:XLE, NYSE:OXY, NYSE:COP, NYSE:XOM, NYSE:CVX` | senkron | tarama pc: OXY 0,152 (IS 0,13 / OOS 0,19; %100 yıl; YÜKSEK), COP 0,136, XLE 0,134 (IS 0,10 / OOS 0,19), XOM 0,126, CVX 0,122, HAL 0,119, XOP 0,119, OIH 0,109, VLO 0,106,… | hayır (senkron; ABD kapanışı BIST'ten sonra → günlük ölçüm kısmen eşzamansız) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 10 | Dizel crack spread — ÇEYREKLİK ortalama (HO×42 − Brent) | `NYMEX:HO1!*42-ICEEUR:BRN1!` | rejim | aynı çeyrek corr 0,38, kısmi 0,47 (n=68 çeyrek); sonraki çeyreğe öncülük yok (pc 0,02); 2025–26 rejiminde haftalık pc 0,38 / 0,54; 4Ç26 ortalama HO crack ~93 $/varil (aş… | hayır (öncülük yok; düşük frekans) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 11 | Avrupa rafineri sepeti t−1 → TUPRS gün-içi | `GPW:PKN, BET:MOL, ATHEX:MOH, ATHEX:ELPE, OMXHEX:NESTE, EURO…` | gunici_oncu | hedge'li gün-içi t 3,93 (IS 3,0 / OOS 2,5); brüt yalnız 8,5 bps/işlem; 2 bacak maliyet sonrası negatif (BT1e Sharpe −0,68) | hayır — istatistik ORTA, işlem DÜŞÜK (brüt 8 bps < 2 bacak maliyeti) | ORTA | **YOK** | brut 8,5 bps < 2 bacak maliyeti |
| 12 | Asya rafinerisi S-Oil (KRX) | `KRX:010950` | senkron | tarama pc 0,101 (IS 0,064 / OOS 0,139; yılların %85'i; FDR+replike) | hayır (senkron; Kore kapanışı BIST açılışından önce ama pencere BIST t−1 seansını da içer… | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 13 | KCHOL (ana holding; TUPRS Koç NAV'ının ~%33'ü) | `BIST:KCHOL` | senkron | pc 0,117 (t 5,6; IS 0,16 / OOS 0,07; 3y 0,12 / 1y 0,03, t 0,4; 15/17 yıl +); XU100+TRY+EEM+sektör kontrollü 0,144; Koç plasebo sıralamasında iştirakler 2.–6. sırada | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 14 | PETKM (yurt içi petrokimya emsali) | `BIST:PETKM` | senkron | PETKM~TUPRS pc 0,136–0,168 (IS 0,15 / OOS 0,17–0,18; haftalık 0,09); ry_hisse yıllık artık korelasyon istikrarsız (−0,14…0,49); son 1y DY net spillover PETKM→TUPRS 3,3 p… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 15 | BIST 30 / banka / holding / sanayi endeksleri saatlik gecikmeli (XU03… | `BIST:XU030, BIST:XBANK, BIST:XHOLD, BIST:XLBNK, BIST:XUSIN` | gunici_oncu | saatlik Σβ(1..3): XU030 −0,111 (t −3,81; IS −0,165 t −3,12 / OOS −0,078 t −2,26), XBANK −0,100 (t −4,27; IS −0,147 t −3,55 / OOS −0,076 t −2,75; ters yön −0,054), XHOLD… | hayır — istatistik ORTA, işlem DÜŞÜK (endeks düzeyindeki benzer saatlik stratejiler maliy… | ORTA | **YOK** | saatlik, seans ici; maliyet sonrasi negatif |
| 16 | Büyük-ölçek faktörü (küçük/orta ölçek endeksleri karşısında) | `BIST:XYUZO, BIST:XTUMY, BIST:XUTUM` | senkron | XU100 + endeks iki faktörlü modelde endeks katsayıları: XYUZO −0,141 (t −6,5; hisse-hariç kısmi IS −0,09 / OOS −0,20; yılların %100'ü), XUTUM −0,119 (t −4,9), XTUMY −0,1… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 17 | TL faizleri (BAP gösterge-benzeri DİBS 10y / 5y / 2y) — faiz ↑ günler… | `TVC:TR10Y` | senkron | XU100-kısmi: 10y +0,125 (IS 0,09 / OOS 0,14; 3y 0,18 / 1y 0,30; yılların %85'i; FDR), 5y +0,103, 2y +0,095 (1y 0,24), 1y DİBS +0,06 | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 18 | Kur — VİOP USDTRY ön ay (15:00 UTC, BIST kapanışıyla hizalı) | `BIST:USDTRY1!` | senkron | XU100-kısmi 0,103 (IS 0,08 / OOS 0,10; 3y 0,08 / 1y 0,25; yılların %90'ı; FDR); VİOP sepet 0,094; Yahoo TRY=X 0,046 (zaman uyumsuz); kur-vol rejimi: yüksek 0,07 / düşük… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 19 | Kur gece hareketi (EURTRY / sepet, 15:00 UTC t−1 → 06:00 UTC t) | `FX:EURTRY` | gap_oncu | EURTRY gece → gap t −3,03 (1. yarı −1,08 / 2. yarı −3,26; XU100 gap kontrollü −3,47); sepet gece → gap t −3,22; 2024+ saatlik | hayır — açılış gap'inde fiyatlanıyor; VİOP pay vadelisinde akşam seansı yok | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 20 | Seans dışı negatif siyasi şok günleri | `BIST:XU100` | olay | 13 seans dışı şokta XU100 gap −264 bps (t −3,0); kesitte TUPRS XU100'e göre +150 bps (döviz gelirliler +124…+223); bankalar −120…−140; sonraki 5 günde sürüklenme yok (XU… | hayır (gap'te fiyatlanıyor; öngörü değeri yok) — korunma/kesit bilgisi | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 21 | Banka ↔ sanayi rotasyonu (XBANK karşısında defansif taraf) | `BIST:XBANK` | rejim | TUPRS–XBANK XU100-kısmi tam −0,244, son 250g −0,396 (faktör son yılda değişti: SISE/KCHOL bankalarla aynı yöne kaydı, TUPRS defansif kaldı); PCA PC3 (%4,8): perakende/gı… | hayır (rejim/konumlama) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |

### SAHOL (`BIST:SAHOL`, `BIST:SAHOL1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | ABD vadelileri ES/NQ gece hareketi (+VIX_t−1) | `CME_MINI:ES1!` | gap_oncu | ES gece → SAHOL gap corr 0,47 (1y 0,55; IS 0,47 / OOS 0,49; n 556); NQ 0,49; gün-içi t 1,0 (08:30→kapanış 0,01). VIX_t−1 → cc kısmi −0,083 (t −4,5; IS −2,4 / OOS −4,1; g… | hayır: açılış müzayedesinde fiyatlanıyor; pay vadelisinde akşam seansı yok | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 1 | TUR (MSCI Türkiye ETF) + EEM / EMB / TUR−EEM | `NASDAQ:TUR` | gap_oncu | TUR gece → gap corr 0,32 (1y 0,36; IS 0,27 / OOS 0,37); Yahoo TUR_t−1 → gap t 7,8 (IS 9,0 / OOS 3,7; FDR); faktör kontrolünde ayakta (kısmi 0,17, t 3,2). Senkron pc 0,10… | hayır (gap) | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 2 | AKBNK (en büyük iştirak) | `BIST:AKBNK` | senkron | pc 0,243 (t 10,8; n 4.212); IS 0,24 / OOS 0,35; son 3y 0,36 / 1y 0,53 (t 9,2); 14/17 yıl +; 2010–16 ≈0, 2017 sonrası 0,15–0,56. XU100+TRY+EEM kontrollü 0,237; AKBNK hari… | hayır (senkron); oran sinyali ayrı satırda | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 3 | SAHOL/AKBNK log-oranı ortalamaya dönüş (çift işlem) | `BIST:SAHOL/BIST:AKBNK` | cok_gunluk | log(SAHOL−β·AKBNK) 60 günlük ortalamasından >1,5σ saptığında ertesi açılışta ters pozisyon. Doğru muhasebeyle (8 bps): IS 2014–20 +13,9 bps/maruz gün (t 3,2), OOS 2021–2… | evet (2021–26, VİOP): vadeli fiyatları ve 15 bps ile t 2,25–2,70, ~20 bps/maruz gün; 10:3… | YUKSEK | **KENAR** | K1: z60 +-2, ertesi gun giris, 20 gun; 1 gun gecikmeyle +160/+310 bps/islem |
| 4 | Özel banka faktörü (YKBNK, GARAN, ISCTR; XUMAL) | `BIST:YKBNK` | senkron | SAHOL–YKBNK pc 0,25 (IS 0,16 / OOS 0,31; %92 yıl, f_y_hisse); v_banka_holding: GARAN 0,163, YKBNK 0,194, ISCTR 0,171 → banka sepeti kontrolünde 0,065 / 0,109 / 0,078. Hi… | hayır (senkron) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 5 | KCHOL (holding faktörü) | `BIST:KCHOL` | senkron | pc 0,250 (SAHOL'ün 46 hisse içinde en yüksek pc'si; grup dışı medyan −0,016); f_y_hisse: pc 0,293, IS 0,18 / OOS 0,38, yıllık işaret %100 | hayır (senkron) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 6 | Büyük ölçek faktörü (XYUZO / XTUMY / XUTUM, hisse-hariç) | `BIST:XYUZO` | senkron | Hisse-hariç XYUZO (BIST100 dışı orta ölçek) kısmi −0,25 (IS −0,22 / OOS −0,27; yılların %100'ü); hisse-hariç XU030 −0,09 (IS −0,23 / OOS −0,01). XU030 corr 0,81; İki fak… | hayır (senkron) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 7 | VİOP baz anomalisi → ertesi spot gap | `BIST:SAHOL1!` | mikroyapi | Baz anomalisi_t → spot gap_t+1 8,3 bps/σ (t 4,3; IS 3,2 / OOS 3,4; FDR geçti); → vadeli gün-içi_t+1 −6,9 bps/σ (t −1,3) | hayır (spot gap; vadelide kalıntı yok) | YUKSEK | **RISK** | ertesi spot gap; vadelide kalinti yok |
| 8 | VİOP 09:30 açılışı → spot açılış gap'i | `BIST:SAHOL1!` | mikroyapi | corr 0,52 (b 0,50; R² 0,27); spot gün-içi kalıntı yok | hayır | YUKSEK | **YOK** | yalniz acilis icrasi |
| 9 | EM bankaları (JSE: SBK, FSR, ABG, NED) | `JSE:SBK` | senkron | SBK pc 0,068–0,079 (t 3,6–4,2; IS 0,07 / OOS 0,10–0,11; yılların %92–100'ü; 1y 0,15); FSR 0,072 (IS 0,06 / OOS 0,09); ABG, NED benzer; tarama FDR geçti; tam faktör kontr… | hayır (senkron; JSE kapanışı BIST ile eşzamanlı) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 10 | Akbank ADR (AKBTY) | `OTC:AKBTY` | senkron | pc 0,101 (t 5,2); IS 0,13 / OOS 0,16; %71 yıl | hayır (aynı varlık; ABD seansı) | ORTA | **YOK** | ayni varlik (bayat ADR) |
| 11 | Asya kapanışları: Nikkei, KOSPI | `TVC:NI225` | gap_oncu | Nikkei → gap corr 0,41 (t 6,3; IS 0,39 / OOS 0,43); tam faktör kontrolünde kısmi 0,25 (t 9,7); KOSPI 0,25 (t 9,0) | hayır (VİOP 09:30 açılışında fiyatlanıyor) | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 12 | TL kuru: USDTRY / EURTRY (negatif) | `FX:USDTRY` | senkron | pc: r1 USDTRY −0,076 (t −3,7; IS −0,11 / OOS −0,12), EURTRY −0,084 (t −4,1); Yahoo −0,104 (IS −0,11 / OOS −0,12; 3y −0,07 / 1y −0,02; FDR); VİOP USDTRY 15:00 hizalı −0,0… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 13 | TL faizi: DİBS 10y/5y (senkron) | `TVC:TR10Y` | senkron | pc DİBS 10y −0,115 (t −4,1; IS −0,11 / OOS −0,12; %85 yıl; 3y −0,17 / 1y −0,27; FDR); 5y −0,095 (IS −0,10 / OOS −0,10; 1y −0,32); 2y −0,061 (1y −0,27); 1y −0,062. Ham co… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 14 | AKBNK_t−1 → SAHOL gün-içi | `BIST:AKBNK` | gunici_oncu | y_grup: AKBNK_t−1 → SAHOL gün-içi t 3,6 (IS 1,9 / OOS 2,6), kendi ve XU100 gecikmesi kontrollü, 712 testte FDR geçen 2 çiftten biri; f_y_hisse t 3,4 (IS 1,9 / OOS 2,5; %… | hayır: tek bacak brüt getiri maliyeti karşılamıyor (oran sinyali bunun daha iyi kullanımı) | ORTA | **FILTRE** | yeni cc testi: +22 bps/1sd, t 2,96 (q 0,03) ama tek bacak net -4,6 bps -> yalniz K1 bilgisi |
| 15 | Sabancı sanayi iştirakleri KORDS / BRISA / TKNSA (negatif pc) | `BIST:KORDS` | senkron | pc KORDS −0,060 (IS −0,09 / OOS −0,08; %76 yıl), BRISA −0,067 (%82 yıl), TKNSA −0,094 (IS −0,08 / OOS −0,11; %87 yıl). Ham corr 0,33–0,40 | hayır | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 16 | BIST Katılım Tüm (XKTUM): banka/holding dışı sepete ters | `BIST:XKTUM` | senkron | Ham ve hisse-hariç kısmi −0,45 (t −15,5; SAHOL endekste yok, ağırlık 0); yalnız OOS (endeks ~2021+), yılların %100'ünde aynı işaret; ham corr 0,68 | hayır (senkron; rotasyon bilgisi) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 17 | Yahoo kur_t−1 → açılış gap'i (eşzamansız) | `FX:USDTRY` | gap_oncu | Yahoo USDTRY_t−1 (~24:00 UTC) → gap t −3,7 (IS −7,9 / OOS 1,0; gap corr −0,10); sepet kur_t−1 → gap t −2,9 (IS −7,4 / OOS 2,0; DÜŞÜK) | hayır: eşzamansız kapanış; 2021 sonrası kur gece hareket etmiyor, etki kayboldu | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |

### AKBNK (`BIST:AKBNK`, `BIST:AKBNK1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | ABD hisse vadelileri gece hareketi (ES=F/NQ=F, 15:00→07:00 UTC) → açı… | `CME_MINI:ES1!` | gap_oncu | Gap corr 0,47 (t 7,5; saatlik 2024-06-11..2026-10-27, G1 örneklemi, n 558), NQ 0,50; XU100 gap kontrollü bankaya özgü kısım pc 0,16; gün-içi corr 0,05 (≈0). XBANK 0,474… | Hayır (işlenemez) — açılış müzayedesinde tamamen fiyatlanıyor, pay vadelisi akşam seansın… | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 1 | TUR (iShares MSCI Türkiye, ABD) BIST kapanışı sonrası hareketi (15:30… | `NASDAQ:TUR` | gap_oncu | Gap corr 0,35 (t 6,9; saatlik 2023-12+, n≈697); gün-içi 0,01; ES gecesi kontrolünde TUR'un ek bilgisi pc 0,17 (t 2,4). XBANK 0,362 (t 7,0), yarılar 0,36/0,37, bankaya öz… | Hayır (işlenemez) — gün-içi kalıntı ≈0. BT1h TUR_post→gün-içi (10 bps) OOS +1,9 bps/gün;… | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 2 | Kendi ADR'si AKBTY (Akbank, ABD OTC) — senkron ayna | `OTC:AKBTY` | senkron | XU100 kontrollü pc 0,440 (IS 0,49 / OOS 0,41), ham corr 0,67 (1y 0,50); tam faktör kontrollü 0,355 (OOS t 9,7); Garanti ADR TKGBY pc 0,267 (tam 0,166). "BIST→ADR" ters y… | Hayır — aynı varlık; ADR bilgi taşımıyor (bayat fiyat). | YUKSEK | **YOK** | ayni varlik (bayat ADR) |
| 3 | VIX_{t−1} (ABD kapanışı, BIST kapalıyken) → ertesi gün banka getirisi… | `CBOE:VIX` | gap_oncu | Granger (cc hedefi, kendi lag + XU100 lag kontrollü) kısmi korelasyon −0,064 (HC1 Wald t −3,59; BH q 0,034; aile 2.679 test); gap hedefli −0,130, gün-içi hedefli +0,004… | Hayır (işlenemez) — bilgi ertesi açılış müzayedesinde fiyatlanıyor, gün-içi kalıntı ≈0; p… | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 4 | TL devlet tahvili (DİBS) faizleri 2y/5y/10y — senkron | `TVC:TR05Y` | senkron | 5y pc −0,157 (IS −0,16 / OOS −0,15; yılların %85'i aynı işaret; 3y −0,28, 1y −0,36); 10y pc −0,154 (IS −0,16 / OOS −0,15); 2y pc −0,099; ham corr son 1y (5y) −0,53. XBAN… | Hayır (senkron) — risk/hedge bilgisi. | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 5 | Banka sektörü faktörü (XLBNK/XBANK hisse-hariç, yurt içi banka akranl… | `BIST:XLBNK` | senkron | XBANK hisse-hariç kısmi (XU100 kontrollü) 0,71 (IS 0,55 / OOS 0,76; yılların %100'ü); en yakın akranlar: GARAN artık ρ 0,69 (IS 0,63 / OOS 0,71), YKBNK 0,64 (IS 0,37 / O… | Hayır — senkron; spread/hedge için (öncülük yok). | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 6 | BIST piyasa faktörü (XU100/XU030) | `BIST:XU100` | senkron | XU100 corr 0,77 (IS 0,85 / OOS 0,71); çoklu beta β_XU100 IS 1,34 / OOS 1,15; XU030 iki faktörlü pc 0,32; piyasa varyans payı tam 0,28. / Ölçek endeksleri [YÜKSEK, y_ende… | Hayır — senkron; BIST:XU030D1! ile beta hedge. | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 7 | VİOP pay vadelisi 09:30 açılış seansı → spot 09:55/10:00 açılış gap'i | `BIST:AKBNK1!` | mikroyapi | corr 0,62 (R² 0,39); 47 hisse medyan β 0,64, R² 0,31; kalıntı → spot gün-içi medyan t −1,2. | Hayır — spot açılışı vadeliyi zaten fiyatlıyor, gün-içi kalıntı ~0 (BT4 net negatif); yal… | YUKSEK | **YOK** | yalniz acilis icrasi |
| 8 | SAHOL (Sabancı Holding, %40,75 pay) ↔ AKBNK — senkron holding–iştirak… | `BIST:SAHOL` | senkron | XU100 kontrollü pc 0,243 (t 10,8); IS 0,244 / OOS 0,352, 3y 0,361, 1y 0,527 (t 9,2); 14/17 yıl +; 2017 öncesi ≈0. XU100+TRY+EEM + AKBNK hariç banka sepeti kontrolüyle 0,… | Hayır (senkron) — çift işlemin temeli (aşağıdaki oran sinyali). | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 9 | SAHOL/AKBNK oranının ortalamaya dönüşü (çift işlem) | `BIST:SAHOL/BIST:AKBNK` | cok_gunluk | log(SAHOL − β·AKBNK) 60 günlük ortalamadan >1,5σ saparsa ertesi açılışta ters pozisyon (8 bps): doğru muhasebeyle IS 2014–20 +13,9 bps/maruz gün (t 3,2), OOS 2021–26 +22… | Evet (2021–26, VİOP) — vadeli fiyatlarıyla 8–15 bps'de t 2,3–3,1 (~20 bps/maruz gün); 10:… | YUKSEK | **KENAR** | K1 bacagi |
| 10 | TUR ETF ve TUR−EEM (Türkiye primi) — senkron, bankaya özgü kısım | `NASDAQ:TUR` | senkron | TUR pc 0,095 (IS 0,13 / OOS 0,12), ham corr 0,64 (1y 0,68); yurt içi ajan pc 0,133 (IS 0,13 / OOS 0,14); TUR−EEM pc 0,100 (IS 0,18 / OOS 0,06). XBANK pc 0,13 (IS 0,20 /… | Hayır — senkron; TUR banka hisselerini içerdiği için kısmen mekanik ayna. | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 11 | Asya endeksleri aynı gün (Nikkei 225, KOSPI, Şanghay Bileşik) → açılı… | `TVC:NI225` | gap_oncu | Nikkei → gap corr 0,42 (t 5,3; IS 0,41 / OOS 0,44); KOSPI 0,37 (t 3,9); Şanghay (vekil CBOE:CNYA) 0,20 (t 3,2). Gün-içi: Nikkei −0,05 (t −1,3), Hang Seng ilk 1,5 saat t… | Hayır (işlenemez) — açılış müzayedesinde fiyatlanır; ES gecesiyle büyük ölçüde örtüşür. | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 12 | FOMC gecesi (karar 18/19 UTC, BIST kapalıyken) | `CME_MINI:ES1!` | olay | XBANK /gap/ 1,38x (FOMC dışı gecelere göre), XU100 1,34x (p<0,001, IS 1,46 / OOS 1,29); AKBNK FOMC betası 0,32 vs normal 0,12 (ajan; V2: Çarşamba gecesi bileşim etkisi,… | Hayır — gap'te fiyatlanır; yalnız oynaklık/pozisyon boyutu bilgisi. | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 13 | USD/TRY kuru — senkron negatif maruziyet, gece hareketi → gap ve haft… | `FX:USDTRY` | senkron | XU100 kontrollü pc −0,115 (doğru FX hizalaması, 2010–26); VİOP F_USDTRY (15:00 UTC hizalı) pc −0,166 (IS −0,19 / OOS −0,14; yılların %70'inde aynı işaret; 3y −0,01, 1y −… | Hayır (senkron) — hedge/risk yönetimi bilgisi; BT3/BT4 USDTRY sinyali → (ihracatçı − bank… | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 14 | Seans dışı negatif siyasi şoklar — kesitsel tepki | `BIST:XBANK` | olay | AKBNK − XU100 cc −85 bps (t −1,38); XBANK cc −399 bps (t −3,3; n=18); seans dışı alt küme (n=13) XU100 gap −264 bps (t −3,0); t+1..5 sürüklenme yok (+101, t 0,9); döviz… | Hayır — öngörü değeri yok; korunma kesiti (banka short / döviz gelirli long) bilgisi. | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 15 | TÜFE açıklaması (ayın 3'ü, 07:00 UTC = açılış) — oynaklık | `BIST:XBANK` | olay | XBANK ilk saat /getiri/ 182 bps (normal 84), XU030 100 (normal 58); ilk saatten sonra devam yok; yön test edilemedi (yön: ÇOK DÜŞÜK). | Hayır — yalnız oynaklık bilgisi (pozisyon boyutu/stop). | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 16 | Banka akranlarının aynı gün açılış gap'i ayrışması → hisse gün-içi | `BIST:XLBNK` | gunici_oncu | b 0,48 (t 3,0) 2014+; 2021+ b 0,43 (t 1,7); saatlik 2023-12+: açılış→07:30 b 0,12 (t 0,9), 07:30→kapanış −0,60 → bilgi ilk 30 dakikada. | Hayır — 10:30 TSİ girişte lider bileşeni ≈0 (−20…+20 bps); açılış fiyatından dolum VİOP't… | ORTA | **YOK** | bilgi ilk 30 dk'da; profil disi |

### ENJSA (`BIST:ENJSA`, `BIST:ENJSA1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | Gece ABD vadelileri (ES/NQ, 15:00 → 07:00 UTC) ve Asya (KOSPI, Nikkei… | `CME_MINI:ES1!` | gap_oncu | ES gece → gap corr 0,21 (t 2,9; IS 0,28 / OOS 0,13), NQ 0,25 (t 2,89); G1 bağımsız: ENJSA r 0,216 (t 3,86; n 558; 47 medyanı 0,35), XU100 gap kontrollü pc −0,17 (hisseye… | hayır — açılış gap'inde fiyatlanıyor; VİOP pay vadelisinde akşam seansı yok | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 1 | BIST piyasa faktörü (XU100 / XUTUM) | `BIST:XU100` | senkron | v4 XU100 betası tam 0,83 (IS 0,61 / OOS 0,91 / 3y 0,90 / 1y 0,79); corr tam 0,61 (IS 0,49 / OOS 0,64), 1y 0,55; XU100 Shapley varyans payı tam %23,4 (2021–23 %26,8, 2024… | evet (hedge bacağı: BIST:XU030D1!) — sinyal değil | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 2 | VİOP ENJSA vadeli açılışı (09:30) → spot açılış müzayedesi | `BIST:ENJSA1!` | mikroyapi | corr 0,51, β 0,57, R² 0,27; spot gün-içi kalıntısı yok | hayır — tahmin edilen spot açılış fiyatının kendisi (işlem güveni ÇOK DÜŞÜK) | YUKSEK | **YOK** | yalniz acilis icrasi |
| 3 | TUR (ABD'de Türkiye ETF'i) gece / t−1 → ENJSA gap | `NASDAQ:TUR` | gap_oncu | TUR gece → gap corr 0,15 (t 3,34; IS 0,16 / OOS 0,15); TUR_{t−1} (24 UTC) → gap t 4,26 (IS 2,97 / OOS 3,42; FDR); temiz pencere G4: ES-kontrollü TUR kısmi 0,125 (t 1,69)… | hayır — açılış gap'inde fiyatlanıyor; VİOP pay vadelisinde akşam seansı yok | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 4 | Yurt içi elektrik kümesi (AKSEN, GWIND, ODAS, ZOREN; XELKT, akran sep… | `BIST:AKSEN, BIST:GWIND, BIST:XELKT` | senkron | AKSEN pc 0,104 (IS −0,03 / OOS 0,16; yıllık işaret %89); GWIND pc 0,165 (yalnız OOS, kısa örneklem); XELKT corr 0,67 (IS 0,72 / OOS 0,67), endeks katsayısı t 14,6, hisse… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 5 | Büyük-ölçek ↔ küçük/orta ölçek rotasyonu (XU030 karşısında, XYUZO/XTU… | `BIST:XU030, BIST:XYUZO, BIST:XTUMY` | senkron | XU100 + endeks iki faktörlü modelde endeks katsayıları: XU030 −0,218 (t −8,0), XYUZO +0,214 (t 7,9), XTUMY +0,128 (t 5,1), XUTUM +0,107 (t 4,2); Yıldız Pazar XYLDZ +0,09… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 6 | Kendi kapanış müzayedesi hareketi CA = log(C/P18:00 TSİ) → ertesi sab… | `BIST:ENJSA` | mikroyapi | ENJSA: gap_{t+1} b −0,333 (t −2,72), O→07:30 b −0,583 (t −4,3; 47 testte BH-FDR geçti; IS b 0,003 / OOS −0,466 — h1 yarıları); havuzda b −0,35 (t −6,1), ENJSA hisse P&L'… | hayır VİOP ile — SSF uzlaşması müzayede hareketinin yalnız %41'ini izliyor, SSF girişi −1… | ORTA | **FILTRE** | yalniz spot KFI 18:10-18:15 yurutmesi (sert CA yukselisinden sonra kapanistan alma); VIOP'ta yok |
| 7 | Kendi açılış gap'i (/gap/>%1) → gün-içi dönüş | `BIST:ENJSA1!` | mikroyapi | IS 2014–20 +58,5 bps (t 2,6) / OOS 2021–26 +26,4 bps (t 1,3); yılların %67'si +; h1 2023-12+: açılış +17,5, ilk 30 dk VWAP vekili +29,3 (t 1,0), 10:30 girişi +24,8 bps;… | sınırda — istatistik ORTA, işlem DÜŞÜK (VİOP'ta müzayede dolumu yok; ENJSA SSF sınıf C) | ORTA | **YOK** | acilis emri ister (profil disi) |
| 8 | SAHOL açılış gap ayrışması → ENJSA gün-içi (Sabancı %40 ortaklığı) | `BIST:SAHOL` | gunici_oncu | aynı gün lider gap ayrışması → ENJSA gün-içi t 3,19 (IS 0,71 / OOS 3,08; FDR); BT açılış girişi IS 51,2 bps (t 2,05) / OOS 45,8 (t 2,42), 15 bps'de OOS 38,8; ama lider b… | hayır — istatistik ORTA, işlem ÇOK DÜŞÜK (bilgi ilk 30 dk'da fiyatlanıyor) | ORTA | **YOK** | bilgi ilk 30 dk'da; profil disi |

### KCHOL (`BIST:KCHOL`, `BIST:KCHOL1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | ABD vadelileri ES/NQ gece hareketi (+VIX_t−1) | `CME_MINI:ES1!` | gap_oncu | ES 15:00→07:00 UTC getirisi → KCHOL açılış gap'i corr 0,49 (son 1y 0,55; IS 0,52 / OOS 0,49; n 557, 2024+ saatlik); NQ 0,52; gün-içi t 0,7, 08:30→kapanış corr 0,04. VIX_… | hayır: bilgi açılış müzayedesinde fiyatlanıyor; pay vadelisinde akşam seansı yok (gece bi… | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 1 | Koç iştirakleri ARCLK + FROTO + TOASO | `BIST:ARCLK` | senkron | XU100 kontrollü kısmi korelasyon (pc): ARCLK 0,157 (t 8,5; IS 0,18 / OOS 0,15; son 3y 0,18 / 1y 0,23; 17/17 yıl), FROTO 0,152 (t 7,5; IS 0,14 / OOS 0,19; 1y 0,28; 15/17)… | hayır (senkron; göreli değer/hedge bilgisi). Öncülük yok: iştirak_t−1 → KCHOL_t kontrollü… | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 2 | SAHOL (holding faktörü) | `BIST:SAHOL` | senkron | pc 0,250 (v_banka_holding; KCHOL'ün 46 hisse içinde en yüksek pc'si); f_y_hisse: pc 0,293, IS 0,18 / OOS 0,38, yıllık işaret tutarlılığı %100; ham corr 0,72 (1y 0,79) | hayır (senkron) | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 3 | VİOP 09:30 açılışı → spot açılış gap'i | `BIST:KCHOL1!` | mikroyapi | Vadeli açılış (uzlaşmaya göre) → spot gap corr 0,51 (b 0,49; R² 0,26); spot gün-içi kalıntı b −0,02 (t −0,4) | hayır: tahmin edilen şey spot açılış fiyatının kendisi | YUKSEK | **YOK** | yalniz acilis icrasi |
| 4 | TUR (MSCI Türkiye ETF) + EEM / EMB / TUR−EEM gece | `NASDAQ:TUR` | gap_oncu | TUR gece → gap corr 0,27 (1y 0,35; IS 0,19 / OOS 0,36); Yahoo TUR_t−1 → gap t 6,4 (IS 6,7 / OOS 3,4; FDR), hisseye özgü gün-içi t 2,2; EMB_t−1 → gap t 3,1; TUR−EEM t 3,0… | hayır (gap; eşzamansız kapanış) | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 5 | Asya kapanışları: Nikkei, KOSPI, Şanghay (aynı gün) | `TVC:NI225` | gap_oncu | Nikkei (06:30 UTC kapanış) → gap corr 0,41 (t 5,2; IS 0,40 / OOS 0,43); KOSPI 0,34; Şanghay Bileşik 0,19 (IS 0,15 / OOS 0,27). Tam faktör kontrolünde ayakta: Nikkei kısm… | hayır: VİOP 09:30 TSİ açılışı ve spot müzayede bilgiyi fiyatlıyor | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 6 | Koç iştiraki TUPRS | `BIST:TUPRS` | senkron | pc 0,117 (t 5,6); IS 0,16 / OOS 0,07; son 3y 0,12 / 1y 0,03 (t 0,4); 15/17 yıl aynı işaret; ham corr 1y 0,24 | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 7 | Koç iştiraki YKBNK | `BIST:YKBNK` | senkron | pc 0,122 (t 4,4); IS 0,08 / OOS 0,20; son 3y 0,20 / 1y 0,16; 12/17 yıl; XBANK kontrollü 0,156; SAHOL kontrollü 0,079 (1y −0,12); v4 temizliğiyle (f_y_hisse) 0,152 → 0,136 | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 8 | Diğer iştirakler AYGAZ, TTRAK (OTKAR yok) | `BIST:AYGAZ` | senkron | pc AYGAZ 0,053 (IS 0,06 / OOS 0,04; %65 yıl), TTRAK 0,062 (IS 0,05 / OOS 0,10; %71 yıl); OTKAR −0,001 | hayır | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 9 | Büyük ölçek faktörü (XYUZO / XTUMY / XUTUM / XU030) | `BIST:XYUZO` | senkron | Hisse-hariç XYUZO (BIST100 dışı orta ölçek) kısmi −0,16 (IS −0,08 / OOS −0,25; %92 yıl); hisse-hariç XU030 −0,09 (IS −0,26 / OOS 0,00). XU100 corr 0,77, XU030 corr 0,78;… | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 10 | BIST Sürdürülebilirlik 25 (XSD25, hisse-hariç) | `BIST:XSD25` | senkron | Hisse-hariç kısmi 0,29 (yalnız OOS; endeks ~2022+, n 982); ham corr 0,82 | hayır (senkron) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 11 | Banka↔sanayi rotasyonu (XBANK) | `BIST:XBANK` | rejim | Son 250 günde KCHOL–XBANK pc +0,16 (bankalarla aynı yöne kaydı; tam dönemde sanayi tarafı). SISE–KCHOL pc +0,18 | hayır (rejim bilgisi) | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 12 | VİOP baz anomalisi → ertesi spot gap | `BIST:KCHOL1!` | mikroyapi | Baz anomalisi_t → spot gap_t+1 8,5 bps/σ (t 3,6; IS 1,7 / OOS 3,9; 1.152 testte FDR geçti); aynı sinyal → vadeli gün-içi_t+1 −3,3 bps/σ (t −0,5) | hayır (spot gap işlenemez; vadeli kalıntı yok) | ORTA | **RISK** | ertesi spot gap; vadelide kalinti yok |
| 13 | USDTRY/EURTRY gece ve Yahoo kur_t−1 → açılış gap'i | `FX:USDTRY` | gap_oncu | Yahoo USDTRY_t−1 (~24:00 UTC) → gap t −3,1 (IS −6,3 / OOS 0,3; gap corr −0,09); saatlik gece USDTRY (15:00→06:00 UTC) → gap corr −0,14 (t −3,0; 1. yarı −1,6 / 2. yarı −3… | hayır: eşzamansız kapanış, açılış gap'inde fiyatlanıyor; Yahoo serisinde 2021 sonrası kay… | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |

### BRSAN (`BIST:BRSAN`, `BIST:BRSAN1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | ABD/Asya gece bilgisi (ES, NQ, TUR, Nikkei, KOSPI) → BRSAN açılış gap… | `CME_MINI:ES1!, CME_MINI:NQ1!, NASDAQ:TUR, TVC:NI225, KRX:KO…` | gap_oncu | Gece (2024-06+): ES c 0,27 (t 4,1; IS 0,28 / OOS 0,27), NQ 0,29 (t 4,0), TUR 0,16 (t 4,8); aynı gün Nikkei 0,30, KOSPI 0,24. Günlük TUR t−1 → gap t 3,5 (IS 2,4 / OOS 3,1… | Hayır: açılış gap'inde fiyatlanıyor; pay vadelisinin akşam seansı yok. | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 1 | Borusan Yatırım (BRYAT; ana ortak/yatırım şirketi) | `BIST:BRYAT` | senkron | XU100 kontrollü pc 0,56 (IS 0,47 / OOS 0,625); yıl %100. NAV iskontosu (BRYAT/BRSAN) 2026 YTD log −68 (BRSAN rallisi). BRYAT_{t−1} → BRSAN gün-içi t −1,99 (OOS −2,04), F… | Hayır (eşzamanlı; BRYAT VİOP'ta yok). | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 2 | BIST 100 / orta-küçük ölçek endeksleri (piyasa faktörü) | `BIST:XU100, BIST:XYUZO, BIST:XTUMY` | senkron | XU100 corr 0,48 (IS 0,53 / OOS 0,45); XU100 kontrollü ek kısmi: XU030 −0,25 (t −10,9), BIST 100-30 (XYUZO; BIST 100'ün BIST 30 dışındaki hisseleri) +0,24, Tüm-100 (XTUMY… | Piyasa riski kısmen BIST:XU030D1! ile hedge edilebilir (BRSAN'ın XU030'a kısmi ilişkisi n… | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 3 | VİOP BRSAN vadelisinin 09:30 açılışı → spot açılış gap'i | `BIST:BRSAN1!` | mikroyapi | corr 0,56, R² 0,32 (n 632; vadeli 2024-04'ten beri). | Hayır (gün-içi kalıntı ≈0; işlem güveni ÇOK DÜŞÜK). | YUKSEK | **YOK** | yalniz acilis icrasi |
| 4 | Asya çelik/cevher bilgisi (Fortescue; Japon/Avustralya z-kompoziti) →… | `ASX:FMG, TSE:5411, TSE:5401, TSE:6301, ASX:BHP` | gunici_oncu | FMG.AX: r 0,056, NW t 3,51 (IS 2,54 / OOS 2,48); XU100 hedge'li t 2,44; kontrollü t 3,22; doğrulayıcının kendi kurgusuyla t 4,3 (2024–26 t 2,3). /z/>1, 15 bps: IS +4,4 /… | Hayır: kenar ilk 30 dakikada tükeniyor; yalnız açılış müzayedesinden dolum (iyimser) ile… | ORTA | **RISK** | kenar ilk 30 dk'da; 07:30 sonrasi negatif |
| 5 | Hindistan çeliği (JSW Steel) | `NSE:JSWSTEEL` | senkron | pc 0,065 (pc_xt IS 0,066 / OOS 0,070), tarama FDR + replike. Haftalık pc 0,03; son 1y pc_xt 0,12; metal ajanı aynı seriyi pc 0,06 ile DÜŞÜK etiketledi. | Hayır. | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 6 | Metal akranlarının açılış gap'i (EREGL, KRDMD, TRALT, TRMET) → BRSAN… | `BIST:EREGL, BIST:KRDMD, BIST:TRALT, BIST:TRMET` | gunici_oncu | Kendi gap'i ve XU030 gap'i kontrollü: 2014+ b 0,246 (t 3,51), 2021+ b 0,401; 47 testte FDR geçti (6/47 hisseden biri). h1 2023-12+: O→07:30 b 0,234 (t 2,0), 07:30→kapanı… | Sınırda/hayır: havuzda etki ilk 30 dk'da; BRSAN'da 07:30 sonrası da b 0,20 görülüyor ama… | ORTA | **YOK** | acilis gap'ine gun ici yetisme; profil disi |
| 7 | Kendi açılış gap'ini fade (/gap/>%1, açılış müzayedesi aşırı tepkisi) | `BIST:BRSAN1!` | mikroyapi | Ajan (ry_gunici_y, v3 temizlik): IS 17,8 bps (t 1,4) / OOS net 8 bps +47, net 15 bps +40 (t 2,64); yılların %85'i pozitif; 47 testte FDR evet. DOĞRULAMA (v_YG1_a, güncel… | Sınırda/hayır: VİOP vadeli açılışı spottan medyan 36–46 bps sapıyor, açılış seansı derinl… | ORTA | **YOK** | acilis emri ister (profil disi) |
| 8 | Tavan/limit mikroyapısı (BRSAN, 2020-03 sonrası VİOP47 içinde en çok… | `BIST:BRSAN, BIST:BRSAN1!` | mikroyapi | Genel bulgu (177 hisse): tavan ertesi gap +282 bps (t 44), VİOP47'de 47/47 hisse pozitif; ertesi gün açılışta sat/kapanışta kapat VİOP47 net +66 bps @15 (t 3,2; IS +52 /… | Evet/sınırda (VİOP pay vadelisiyle; açılış dolumu iyimser, kilitli tavanda kapanıştan alı… | ORTA | **RISK** | kilitli tavanda dolum yok; boyut/kuyruk bilgisi |
| 9 | BIST Sınai (XUSIN) senkron | `BIST:XUSIN` | senkron | XU100 kontrollü pc 0,15 (metal; ham corr IS 0,53 / OOS 0,47; haftalık pc 0,16; yıl %100) / 0,14 (y_endeks iki faktörlü t 6,2; hisse ağırlığı ~%1); ry_ag ortak faktör son… | Hayır (senkron). | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |

### TRMET (`BIST:TRMET`, `BIST:TRMET1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | ABD/Asya gece bilgisi (ES, NQ, TUR, EMB, BTC, Nikkei, KOSPI, Şanghay)… | `CME_MINI:ES1!, CME_MINI:NQ1!, NASDAQ:TUR, NASDAQ:EMB, BITST…` | gap_oncu | Gece (2024-06+): NQ c 0,37 (t 5,3; IS 0,40 / OOS 0,37), ES 0,35 (t 4,95), TUR 0,25 (t 6,1), BTC 0,22; aynı gün Nikkei 0,37, KOSPI 0,29, Şanghay 0,19. Günlük TUR t−1 → ga… | Hayır: açılış gap'inde fiyatlanıyor; pay vadelisinin akşam seansı yok. | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 1 | Türk Altın (TRALT) — TRMET'in ~%47–48 dolaylı iştiraki | `BIST:TRALT` | senkron | XU100 kontrollü pc 0,62 (IS 0,61–0,63 / OOS 0,72; ham corr IS 0,63 / OOS 0,81); 13/13 yıl artık ρ ≥0,50; haftalık corr 2026'da 0,85. | Hayır (eşzamanlı). İki bacak da VİOP'ta; NAV iskontosu/oran stratejisi test edilmedi. | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 2 | TR Doğal Enerji (TRENJ; eski İpek, Koza grubu) | `BIST:TRENJ` | senkron | pc 0,74–0,75 (IS 0,79–0,80 / OOS 0,76; ham corr OOS 0,84); yıl %100. Grup çiftleri içinde en yüksek senkronlardan biri. | Hayır (eşzamanlı; TRENJ VİOP'ta yok). | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 3 | BIST Madencilik endeksi, BIST 100, BIST Sınai | `BIST:XMADN, BIST:XU100, BIST:XUSIN` | senkron | XMADN corr 0,89, pc 0,86 (mekanik içerme); XU100 corr 0,47 (IS 0,37 / OOS 0,58); XU030 ek kısmi −0,15 (t −7,9); XUSIN pc 0,20. Shapley: sektör (Koza grubu) %60,2 — 47 hi… | Piyasa riski BIST:XU030D1! ile hedge edilebilir; öngörü değil. | YUKSEK | **FILTRE** | zayif: ortak faktor kontrolunde ~0 (dolayli bag); oncu degil |
| 4 | VİOP TRMET vadelisinin 09:30 açılışı → spot açılış gap'i | `BIST:TRMET1!` | mikroyapi | corr 0,54, R² 0,29 (n 1.964); gün-içi kalıntı ≈0. | Hayır (işlem güveni ÇOK DÜŞÜK). | YUKSEK | **YOK** | yalniz acilis icrasi |
| 5 | Altın (COMEX ons altın; gram altın TL bunun türevi) | `COMEX:GC1!` | senkron | Günlük XU100 kontrollü pc 0,13 (IS 0,13 / OOS 0,18; haftalık 0,19); aylık pc 0,30 (IS 0,25 / OOS 0,31); gümüş aylık 0,28. XAUTRY tam dönem pc 0,10 (IS 0,03 / OOS 0,15; y… | Hayır (senkron). | ORTA | **FILTRE** | zayif: ortak faktor kontrolunde ~0 (dolayli bag); oncu degil |
| 6 | Altın/gümüş madencisi hisseleri senkron (GDX, GDXJ, Newmont, Agnico,… | `AMEX:GDX, AMEX:GDXJ, NYSE:NEM, NYSE:AEM, NYSE:B, LSE:FRES,…` | senkron | pc 0,08–0,14 (tarama pc_xt IS 0,04–0,08 → OOS 0,10–0,18: OOS'ta güçleniyor); Shandong Gold H 0,14 (IS 0,13 / OOS 0,14), Zhaojin H 0,105, Jiangxi Copper H 0,09. ABD kapan… | Hayır (senkron). | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 7 | Çin altını ve Çin/HK madenci hisseleri senkron (SHFE altın, Zijin A/H… | `AMEX:GLD, OTC:ZIJMF, OTC:CMCLF (Çin kodu yok)` | senkron | SHFE altın pc 0,15 (IS 0,09 / OOS 0,14), haftalık r 0,28 (kısmi 0,26); Zijin H 0,09 (IS 0,15 / OOS 0,13), Zijin A 0,09, CMOC A 0,06. TRALT'taki gibi COMEX altınına ek bi… | Hayır (senkron). | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 8 | Koza grubu içi ters dönüş: TRALT + TRENJ yurt içi artığı (t−1) → TRME… | `BIST:TRALT, BIST:TRENJ` | gunici_oncu | −21,6 bps/σ, t −4,59 (IS −3,86 / OOS −2,62), 45 hisse içinde BH q<0,01. Ayrıca TRENJ_{t−1} → TRMET gün-içi t −3,7 (IS −4,4 / OOS −1,3), 712 testlik ailede FDR geçti; TRA… | Test edilmedi: sinyal BIST kapanışında (15:00 UTC) biliniyor, ertesi gün VİOP TRMET vadel… | ORTA | **FILTRE** | Koza z3 kuralinin icinde (u = TRMET - b*grup); yeni cc testi tek basina t -1,6, q 0,39 |
| 9 | Kendi kapanış müzayedesi hareketi (CA = log(C/P18:00 TSİ)) → ertesi g… | `BIST:TRMET` | mikroyapi | TRMET CA → ertesi gap b −0,47 (t −2,78), 47 testte FDR geçen 6–7 hisseden biri. Havuz (47 hisse): b −0,35 (t −6,1); /CA/>25 bps portföy 14,1 bps (t 4,6). Örneklem 2023-1… | Hayır (VİOP'ta): SSF uzlaşması müzayede hareketinin yalnız %41'ini izliyor, SSF girişi −1… | ORTA | **FILTRE** | yalniz spot KFI yurutmesi; VIOP uzlasmasi CA'nin %41'ini izliyor |
| 10 | VİOP baz anomalisi → ertesi spot açılış gap'i | `BIST:TRMET1!` | mikroyapi | t 3,82 (IS 1,99 / OOS 3,91). Aynı sinyal → ertesi vadeli gün-içi t −1,16 (IS −1,45 / OOS −0,32; ÇOK DÜŞÜK). | Hayır (gap'te fiyatlanıyor). | ORTA | **RISK** | ertesi spot gap; vadelide kalinti yok |
| 11 | Koza grubu yönetim/olay riski (kayyum 28.10.2015; TVF devri 20.08.202… | `BIST:TRMET, BIST:TRALT, BIST:TRENJ` | olay | Kayyum: CAR[0,+20] XU100'e göre −%40,8 (z −3,5). TVF devri: AR0 +%6,1, CAR[2,10] −%14. Birleşme kararı: AR0 +%5,1, CAR[2,10] −%10. Birleşme iptali: AR0 −%10,0, CAR[0,1]… | Hayır (olaylar önceden bilinmiyor). | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 12 | Türkiye siyasi/TL şoku (19.03.2025 İmamoğlu şoku) | `BIST:XU100, FX:USDTRY` | olay | CAR[−1,+1] +%9,7, CAR[0,+20] XU100'e göre +%27,9 (z 2,5); aynı dönemde altın +%9,0. | Hayır (tek olay; gap'te oluşuyor). | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |

### TRALT (`BIST:TRALT`, `BIST:TRALT1!`)

| # | Sürücü | TradingView | İlişki | Sayılar (kart) | Kartın hükmü | Güven | Etiket | Not |
|---|---|---|---|---|---|---|---|---|
| 0 | Altın (COMEX ons altın; gram altın TL bunun türevi) | `COMEX:GC1!` | senkron | Günlük XU100 kontrollü pc 0,21 (IS 0,19 / OOS 0,19 / son 1y 0,34; v4 temizlikle IS 0,16); 17/17 yıl pozitif; USDTRY+EEM kontrollü 0,22. BIST kapanışıyla hizalı 15:00 UTC… | Hayır (senkron, 5 dk içinde fiyatlanıyor). Korunma/konumlama için. | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 1 | Altın madencileri sepeti (bölge endeksinden arındırılmış) → TRALT hed… | `AMEX:GDX, AMEX:GDXJ, NYSE:NEM, NYSE:AEM, NYSE:B, NYSE:KGC,…` | gunici_oncu | 19,4 bps/σ, t 4,39 (IS 3,27 / OOS 2,92), BH q 0,0005 — 47 hisse içinde en güçlü; VİOP vadelisinde 15,1 bps/σ (t 2,46). /z/>1 hedge'li brüt OOS 38,6 bps → 16 bps net +22,… | Sınırda: hisse bazında net pozitif görünüyor ama hisse sonradan seçildi; portföy düzeyind… | YUKSEK | **RISK** | t gununde fiyatlaniyor; yeni cc testi (FF49 Gold artigi -> TRALT t->t+1) +4,7 bps, t 0,78 |
| 2 | ABD/Asya gece bilgisi (ES, NQ, TUR, BTC, Nikkei, KOSPI) → TRALT açılı… | `CME_MINI:ES1!, CME_MINI:NQ1!, NASDAQ:TUR, BITSTAMP:BTCUSD,…` | gap_oncu | Gece (2024-06+): ES c 0,37 (t 5,05; IS 0,38 / OOS 0,39), NQ 0,39 (t 5,3), TUR 0,23 (t 5,1), BTC 0,24; aynı gün Nikkei 0,33, KOSPI 0,26. Günlük TUR t−1 → gap t 4,3 (IS 3,… | Hayır: açılış gap'inde fiyatlanıyor; pay vadelisinin akşam seansı yok. | YUKSEK | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 3 | TR Anadolu Metal (TRMET) ve TR Doğal Enerji (TRENJ) — Koza grubu | `BIST:TRMET, BIST:TRENJ` | senkron | TRMET pc 0,62 (IS 0,63 / OOS 0,81 ham corr; IS pc 0,61 / OOS 0,72); 13/13 yıl artık ρ ≥0,50; TRMET~TRALT haftalık corr 2026'da 0,85. TRENJ pc 0,51–0,52 (IS 0,53 / OOS 0,… | Hayır (eşzamanlı). TRMET de VİOP'ta; oran stratejisi test edilmedi. | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 4 | BIST 100 / BIST Madencilik (piyasa ve sektör endeksi) | `BIST:XU100, BIST:XMADN` | senkron | XU100 corr 0,47 (IS 0,37 / OOS 0,56); XU030 ek kısmi −0,12 (t −5,9); XMADN corr 0,94, pc 0,92 (mekanik içerme). Piyasa payı (Shapley) %11,4. XU100 kontrollü ek kısmi: XY… | Piyasa riski BIST:XU030D1! ile hedge edilebilir; öngörü değil. | YUKSEK | **FILTRE** | hedge / kume / boyut; oncu degil |
| 5 | VİOP TRALT vadelisinin 09:30 açılışı → spot açılış gap'i | `BIST:TRALT1!` | mikroyapi | corr 0,60, R² 0,36 (n 1.965); gün-içi kalıntı ≈0. | Hayır (tahmin edilen şey spot açılışın kendisi; işlem güveni ÇOK DÜŞÜK). | YUKSEK | **YOK** | yalniz acilis icrasi |
| 6 | Gümüş, platin ve paladyum (COMEX SI, NYMEX PL, NYMEX PA) | `COMEX:SI1!, NYMEX:PL1!` | senkron | Gümüş günlük pc 0,18 (IS 0,23 / OOS 0,22 ham), aylık 0,41 (IS 0,43 / OOS 0,44); platin pc 0,14. 30 dk m5 senkron gümüş r 0,43 (t 14,4). Paladyum pc 0,09 (pc_xt IS 0,06 /… | Hayır (senkron). | ORTA | **FILTRE** | zayif: ortak faktor kontrolunde ~0 (dolayli bag); oncu degil |
| 7 | Altın/gümüş madencisi hisseleri senkron (Fresnillo, RING, GDX, GDXJ,… | `LSE:FRES, NASDAQ:RING, AMEX:GDX, AMEX:GDXJ, NYSE:NEM, NYSE:…` | senkron | Fresnillo pc 0,17–0,18 (IS 0,17–0,24 / OOS 0,18–0,22; yıl %100) ve RING 0,15 tarama "SAĞLAM" (YÜKSEK); diğerleri pc 0,10–0,15 (IS 0,07–0,16 / OOS 0,13–0,22; son 1y ham c… | Hayır (senkron). | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 8 | Çin altını ve Çin/HK altın hisseleri senkron (SHFE altın, Shandong Go… | `AMEX:GLD, COMEX:GC1!, HKEX:1787 (açılmayabilir)` | senkron | SHFE altın günlük pc 0,17 (IS 0,25 / OOS 0,13); haftalık kısmi Cuma çapasında 0,32 vs COMEX 0,22, ama Pzt–Çar çapalarında 0,22–0,32 vs 0,23–0,31 (eşdeğer); günlük GC 0,2… | Hayır (senkron). | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 9 | ABD faizleri ve dolar (5y/10y T-Note vadelileri, ABD 5y getiri, dolar… | `CBOT:ZF1!, CBOT:ZN1!, TVC:US05Y, TVC:DXY` | senkron | Tahvil vadelileri pc 0,08–0,09, ABD 5y getiri −0,08 (IS 0,09 / OOS 0,07–0,08; tarama FDR + replike); dolar endeksi pc −0,07 (haftalık −0,11; yıl %82), ABD 10y getiri −0,… | Hayır (senkron). | ORTA | **FILTRE** | zayif: ortak faktor kontrolunde ~0 (dolayli bag); oncu degil |
| 10 | Bakır ve ons-TL — AYLIK | `COMEX:HG1!, FX_IDC:XAUTRY` | senkron | Aylık pc bakır 0,24 (t 3,4; IS 0,32 / OOS 0,28 ham), ons-TL 0,33 (IS 0,28 / OOS 0,24). Bakır günlük pc 0,07, ry_ag ortak faktör sonrası t 0,76 (DÜŞÜK). | Hayır. | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |
| 11 | Koza grubu yönetim/olay riski (kayyum 28.10.2015; TVF devri 20.08.202… | `BIST:TRALT, BIST:TRMET, BIST:TRENJ` | olay | Kayyum: CAR[0,+20] XU100'e göre −%35,8 (z −2,7). TVF devri: AR0 +%10,6 (t 5,4), ardından 2.–10. günlerde −%8…−14. Birleşme kararı: AR0 +%5,7, CAR[2,10] +%9,0. Birleşme i… | Hayır (olaylar önceden bilinmiyor; tek tek olaylar). | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 12 | Türkiye siyasi şok günleri (seans dışı negatif şoklar; ör. 19.03.2025… | `BIST:XU100, FX:USDTRY` | olay | Negatif siyasi şoklarda (n 18) TRALT XU100'e göre +144 bps (döviz gelirliler +124…+223). 19.03.2025: CAR[−1,+1] +%9,2, CAR[0,+20] +%23,2 (z 2,2; altın aynı dönemde +%9,0… | Hayır (gap'te oluşuyor; sonraki 5 günde sürüklenme yok). Korunma kesiti bilgisi. | ORTA | **RISK** | acilis gap'i / olay aninda fiyatlaniyor |
| 13 | BIST Sınai (XUSIN) senkron | `BIST:XUSIN` | senkron | XU100 kontrollü pc 0,21 (ham corr IS 0,40 / OOS 0,60; haftalık pc 0,23; yıl %100; metal YÜKSEK); y_endeks iki faktörlü t 9,4 (DÜŞÜK etiketli, hisse ağırlığı ~%2); ry_ag… | Hayır (senkron). | ORTA | **FILTRE** | hedge / kume / boyut; oncu degil |


## Ek B. Yeni testler: tam tablolar

### B1. Aile P — öngörü (38 test, BH-FDR aile içinde)

Model: r_hedef(t→t+1) = a + b·L_t + c·r_hedef,t + d·r_XU100,t; NW(5) t. Etki = b·sd(L), bps/1σ. ABD/EIA serileri ABD günü d'den sonraki ilk BIST gününe (t) eşlendi. Kural: |z_L|>1 → yön = işaret(b_IS)·işaret(z), hedef − β250·XU100, 1 gün (ufuk 2: 2 gün, örtüşmesiz); maliyet spot 25+3, VİOP 12,5+3 bps.

| Hedef | Lider (TradingView) | Ufuk | n | Etki bps/1σ | t | t IS / OOS / 2024+ | q | İşlem n | Brüt | Net (t) | Net OOS (t) | Net 2024+ | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ENERY | `BIST:AHGAZ` | 1 | 784 | +12,5 | +0,72 | +0,90 / +0,10 / +0,50 | 0,77 | 180 | +3,7 | -24,3 (-0,99) | -42,2 (-1,49) | -24,3 | **YOK** |
| ENERY | `BIST:ENJSA` | 1 | 784 | -8,2 | -0,65 | -0,46 / -0,58 / -0,58 | 0,77 | 179 | +8,6 | -19,4 (-0,86) | +0,2 (+0,01) | -19,4 | **YOK** |
| ENERY | `BIST:AKSEN` | 1 | 784 | -21,5 | -1,87 | -2,73 / -0,60 / -1,87 | 0,29 | 185 | +15,8 | -12,2 (-0,65) | -14,7 (-0,63) | -12,2 | **YOK** |
| ENERY | `BIST:AYGAZ` | 1 | 784 | +15,3 | +1,42 | +0,55 / +0,56 / +1,35 | 0,50 | 170 | +1,2 | -26,8 (-1,25) | -42,2 (-1,79) | -26,8 | **YOK** |
| ENERY | `BIST:XELKT` | 1 | 784 | -16,1 | -0,78 | -1,32 / -0,61 / -1,44 | 0,77 | 171 | +25,4 | -2,6 (-0,12) | +9,8 (+0,40) | -2,6 | **YOK** |
| ENERY | `BIST:XUTUM−BIST:XU100` | 1 | 784 | -5,0 | -0,37 | -0,87 / -0,39 / -0,92 | 0,82 | 203 | -15,4 | -43,4 (-1,87) | -66,3 (-2,33) | -43,4 | **YOK** |
| ENERY | `FX:USDTRY (BIST:USDTRY1!)` | 1 | 784 | +2,7 | +0,27 | -0,07 / +0,39 / -0,34 | 0,86 | 89 | -28,5 | -56,5 (-1,87) | -69,8 (-2,06) | -56,5 | **YOK** |
| ENERY | `NYMEX:NG1! (veri: FRED DHHNGSP)` | 1 | 751 | +2,9 | +0,27 | -0,03 / +0,21 / +0,59 | 0,86 | 52 | -33,5 | -61,5 (-1,44) | -75,0 (-1,48) | -61,5 | **YOK** |
| ENERY | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | 1 | 762 | +4,4 | +0,46 | -0,50 / +0,71 / +0,40 | 0,77 | 202 | -7,2 | -35,2 (-1,83) | -52,5 (-2,27) | -35,2 | **YOK** |
| AHGAZ | `BIST:ENERY` | 1 | 684 | -7,4 | -0,57 | -0,41 / -0,32 / -0,57 | 0,77 | 172 | +18,2 | -9,8 (-0,47) | -13,2 (-0,52) | -9,8 | **YOK** |
| AHGAZ | `BIST:ENJSA` | 1 | 947 | +6,5 | +0,64 | +0,41 / +0,25 / +0,07 | 0,77 | 214 | -0,2 | -28,2 (-1,66) | -41,4 (-1,81) | -34,8 | **YOK** |
| AHGAZ | `BIST:AKSEN` | 1 | 947 | +0,8 | +0,07 | -0,10 / +0,18 / -0,48 | 0,96 | 221 | -22,8 | -50,8 (-2,95) | -47,9 (-2,11) | -39,0 | **YOK** |
| AHGAZ | `BIST:AYGAZ` | 1 | 947 | +9,1 | +0,91 | +0,74 / +0,20 / +0,53 | 0,77 | 215 | +7,3 | -20,7 (-1,13) | -49,4 (-2,20) | -35,5 | **YOK** |
| AHGAZ | `BIST:XELKT` | 1 | 947 | -2,5 | -0,15 | -0,43 / +0,03 / -0,63 | 0,93 | 218 | +9,5 | -18,5 (-0,99) | -7,8 (-0,31) | -6,7 | **YOK** |
| AHGAZ | `BIST:XUTUM−BIST:XU100` | 1 | 947 | -5,5 | -0,46 | -0,85 / -0,20 / -0,37 | 0,77 | 236 | -13,9 | -41,9 (-2,40) | -48,9 (-2,11) | -48,6 | **YOK** |
| AHGAZ | `FX:USDTRY (BIST:USDTRY1!)` | 1 | 947 | +4,7 | +0,52 | +0,38 / -0,21 / -1,03 | 0,77 | 99 | +13,0 | -15,0 (-0,64) | -19,6 (-0,73) | -25,7 | **YOK** |
| AHGAZ | `NYMEX:NG1! (veri: FRED DHHNGSP)` | 1 | 908 | +0,4 | +0,05 | +0,26 / -0,19 / -0,21 | 0,96 | 71 | +5,0 | -23,0 (-0,90) | -22,2 (-0,52) | -25,7 | **YOK** |
| AHGAZ | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | 1 | 920 | -12,0 | -1,48 | -1,91 / -0,52 / -1,37 | 0,48 | 240 | +29,9 | +1,9 (+0,12) | -11,4 (-0,56) | +4,2 | **YOK** |
| RYSAS | `BIST:RYGYO` | 1 | 3221 | +32,7 | +3,15 | +1,30 / +2,53 / +3,17 | 0,02 | 793 | +62,8 | +34,8 (+2,40) | +56,5 (+2,98) | +97,5 | **FILTRE (kenar adayı)** |
| RYSAS | `BIST:XGMYO` | 1 | 3221 | -7,1 | -0,60 | -0,33 / -0,55 / +0,11 | 0,77 | 822 | -34,1 | -62,1 (-4,91) | -70,3 (-3,70) | -93,8 | **YOK** |
| RYSAS | `BIST:XULAS` | 1 | 3221 | +9,8 | +0,99 | +0,13 / +1,28 / +1,07 | 0,76 | 815 | +20,6 | -7,4 (-0,62) | +8,8 (+0,48) | +32,9 | **YOK** |
| RYSAS | `BIST:XUTUM−BIST:XU100` | 1 | 3221 | -4,0 | -0,45 | +0,70 / -0,68 / -0,36 | 0,77 | 988 | +20,4 | -7,6 (-0,62) | -38,3 (-2,12) | -37,0 | **YOK** |
| RYSAS | `FX:USDTRY (BIST:USDTRY1!)` | 1 | 3221 | -2,8 | -0,46 | -1,06 / -0,08 / -0,26 | 0,77 | 627 | +7,3 | -20,7 (-1,75) | -26,4 (-1,04) | -35,1 | **YOK** |
| RYSAS | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | 1 | 3144 | +7,2 | +1,01 | +1,20 / +0,03 / -0,60 | 0,76 | 837 | +0,6 | -27,4 (-2,28) | -31,2 (-1,68) | -53,3 | **YOK** |
| ENJSA | `BIST:ENERY` | 1 | 684 | -16,2 | -1,91 | – / -1,91 / -1,91 | 0,29 | 172 | +11,3 | -4,2 (-0,34) | -4,2 (-0,34) | -4,2 | **YOK** |
| ENJSA | `BIST:AHGAZ` | 1 | 847 | -16,2 | -1,71 | – / -1,71 / -2,53 | 0,37 | 213 | +16,4 | +0,9 (+0,07) | +0,9 (+0,07) | +10,8 | **YOK** |
| TUPRS | `AMEX:XLE−β·SP:SPX (veri: FF49 Oil)` | 1 | 3090 | +15,8 | +3,96 | +2,09 / +3,10 / +1,69 | 0,00 | 953 | +20,1 | +4,6 (+0,85) | +15,3 (+1,66) | +14,4 | **FILTRE** |
| TUPRS | `AMEX:XLE−β·SP:SPX (veri: FF49 Oil)` | 2 | 3090 | +22,6 | +3,80 | +1,76 / +3,14 / +1,22 | 0,00 | 721 | +19,7 | +4,2 (+0,46) | +22,1 (+1,50) | +12,7 | **FILTRE** |
| TUPRS | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | 1 | 3144 | +10,4 | +2,23 | +0,51 / +2,68 / +1,60 | 0,19 | 837 | +13,6 | -1,9 (-0,30) | +14,5 (+1,37) | +18,7 | **YOK** |
| TUPRS | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | 2 | 3144 | +15,7 | +2,12 | +0,76 / +2,44 / +1,96 | 0,21 | 649 | +17,2 | +1,7 (+0,16) | +27,5 (+1,73) | +23,9 | **YOK** |
| KCHOL | `SP:SPX (veri: FRED SP500)` | 1 | 2318 | +4,1 | +0,86 | +0,26 / +0,95 / -0,54 | 0,77 | 560 | -2,3 | -17,8 (-2,89) | -16,5 (-2,13) | -21,7 | **YOK** |
| SAHOL | `SP:SPX (veri: FRED SP500)` | 1 | 2318 | +3,8 | +0,66 | +0,66 / +0,16 / -1,06 | 0,77 | 560 | -10,9 | -26,4 (-4,49) | -26,7 (-3,55) | -38,8 | **YOK** |
| SAHOL | `BIST:AKBNK` | 1 | 3221 | +22,4 | +2,96 | +2,43 / +1,73 / +2,68 | 0,03 | 824 | +10,9 | -4,6 (-0,93) | -4,1 (-0,46) | -9,5 | **FILTRE (zayıf)** |
| AKBNK | `CBOE:VIX` | 1 | 3146 | -5,6 | -1,27 | -0,76 / -1,03 / -0,06 | 0,58 | 728 | +0,3 | -15,2 (-2,55) | -18,7 (-1,76) | -32,0 | **YOK** |
| BRSAN | `AMEX:SLX−β·SP:SPX (veri: FF49 Steel)` | 1 | 3090 | +6,9 | +1,24 | +0,58 / +1,08 / +1,46 | 0,58 | 901 | -8,1 | -23,6 (-2,82) | -32,4 (-2,07) | -13,1 | **YOK** |
| BRSAN | `BIST:BRYAT` | 1 | 3221 | -8,5 | -0,78 | +1,25 / -2,13 / +0,41 | 0,77 | 719 | +16,7 | +1,2 (+0,09) | -7,6 (-0,35) | +16,0 | **YOK** |
| TRMET | `(BIST:TRALT+BIST:TRENJ)/2` | 1 | 3221 | -25,7 | -1,63 | -1,11 / -1,22 / -0,97 | 0,40 | 800 | +9,3 | -6,2 (-0,47) | -11,0 (-0,79) | -33,1 | **YOK** |
| TRALT | `AMEX:GDX−β·SP:SPX (veri: FF49 Gold)` | 1 | 3090 | +4,7 | +0,78 | -0,19 / +1,54 / +1,39 | 0,77 | 780 | -5,8 | -21,3 (-2,04) | -31,2 (-2,12) | -45,6 | **YOK** |

### B2. Aile S — senkron / gap günü kısmi korelasyonu (XU100 kontrollü; 36 test)

| Hedef | Lider | Ölçü | n | pc | IS / OOS / son 1y | q | Etiket |
|---|---|---|---|---|---|---|---|
| ENERY | `BIST:AHGAZ` | ayni gun | 785 | +0,613 | +0,61 / +0,61 / +0,63 | 0,000 | FILTRE |
| ENERY | `BIST:ENJSA` | ayni gun | 785 | +0,047 | +0,11 / +0,01 / -0,01 | 0,266 | YOK |
| ENERY | `BIST:AKSEN` | ayni gun | 785 | +0,085 | +0,10 / +0,08 / +0,06 | 0,036 | YOK (pc 0,09) |
| ENERY | `BIST:AYGAZ` | ayni gun | 785 | +0,003 | +0,01 / -0,01 / +0,00 | 0,945 | YOK |
| ENERY | `BIST:XELKT` | ayni gun | 784 | +0,460 | +0,49 / +0,45 / +0,38 | 0,000 | FILTRE |
| ENERY | `BIST:XUTUM−BIST:XU100` | ayni gun | 784 | +0,196 | +0,26 / +0,16 / +0,12 | 0,000 | FILTRE |
| ENERY | `FX:USDTRY (BIST:USDTRY1!)` | ayni gun | 785 | -0,047 | +0,03 / -0,11 / +0,02 | 0,266 | YOK |
| ENERY | `NYMEX:NG1! (veri: FRED DHHNGSP)` | gap gunu (ABD bilgisi BIST t) | 751 | +0,098 | +0,11 / +0,09 / +0,10 | 0,016 | RISK (zayıf) |
| ENERY | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | gap gunu (ABD bilgisi BIST t) | 762 | +0,057 | +0,03 / +0,07 / +0,02 | 0,202 | YOK |
| AHGAZ | `BIST:ENERY` | ayni gun | 785 | +0,613 | +0,61 / +0,61 / +0,63 | 0,000 | FILTRE |
| AHGAZ | `BIST:ENJSA` | ayni gun | 948 | +0,035 | +0,10 / -0,04 / -0,09 | 0,337 | YOK |
| AHGAZ | `BIST:AKSEN` | ayni gun | 948 | +0,047 | +0,04 / +0,05 / -0,02 | 0,243 | YOK |
| AHGAZ | `BIST:AYGAZ` | ayni gun | 948 | +0,003 | -0,03 / +0,03 / +0,02 | 0,945 | YOK |
| AHGAZ | `BIST:XELKT` | ayni gun | 947 | +0,411 | +0,40 / +0,44 / +0,36 | 0,000 | FILTRE |
| AHGAZ | `BIST:XUTUM−BIST:XU100` | ayni gun | 947 | +0,208 | +0,30 / +0,12 / +0,08 | 0,000 | FILTRE |
| AHGAZ | `FX:USDTRY (BIST:USDTRY1!)` | ayni gun | 948 | -0,012 | -0,00 / -0,07 / +0,02 | 0,768 | YOK |
| AHGAZ | `NYMEX:NG1! (veri: FRED DHHNGSP)` | gap gunu (ABD bilgisi BIST t) | 908 | +0,013 | -0,01 / +0,03 / +0,02 | 0,768 | YOK |
| AHGAZ | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | gap gunu (ABD bilgisi BIST t) | 920 | +0,022 | +0,03 / +0,02 / -0,02 | 0,590 | YOK |
| RYSAS | `BIST:RYGYO` | ayni gun | 3222 | +0,605 | +0,68 / +0,52 / +0,45 | 0,000 | FILTRE |
| RYSAS | `BIST:XGMYO` | ayni gun | 3221 | +0,243 | +0,27 / +0,21 / +0,15 | 0,000 | FILTRE |
| RYSAS | `BIST:XULAS` | ayni gun | 3221 | +0,115 | +0,14 / +0,08 / +0,27 | 0,000 | FILTRE (zayıf) |
| RYSAS | `BIST:XUTUM−BIST:XU100` | ayni gun | 3221 | +0,276 | +0,41 / +0,23 / +0,10 | 0,000 | FILTRE |
| RYSAS | `FX:USDTRY (BIST:USDTRY1!)` | ayni gun | 3222 | -0,023 | -0,01 / -0,00 / -0,07 | 0,266 | YOK |
| RYSAS | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | gap gunu (ABD bilgisi BIST t) | 3144 | -0,022 | -0,00 / -0,05 / -0,14 | 0,278 | YOK |
| ENJSA | `BIST:ENERY` | ayni gun | 785 | +0,047 | – / +0,05 / -0,01 | 0,266 | YOK |
| ENJSA | `BIST:AHGAZ` | ayni gun | 948 | +0,035 | – / +0,04 / -0,09 | 0,337 | YOK |
| TUPRS | `AMEX:XLE−β·SP:SPX (veri: FF49 Oil)` | gap gunu (ABD bilgisi BIST t) | 3090 | +0,090 | +0,07 / +0,11 / +0,07 | 0,000 | RISK |
| TUPRS | `ICEEUR:BRN1! (veri: FRED DCOILBRENTEU)` | gap gunu (ABD bilgisi BIST t) | 3144 | +0,034 | +0,01 / +0,07 / +0,03 | 0,103 | YOK |
| KCHOL | `SP:SPX (veri: FRED SP500)` | gap gunu (ABD bilgisi BIST t) | 2419 | -0,004 | +0,01 / -0,02 / -0,13 | 0,873 | YOK |
| SAHOL | `SP:SPX (veri: FRED SP500)` | gap gunu (ABD bilgisi BIST t) | 2419 | -0,042 | -0,09 / -0,01 / -0,05 | 0,074 | YOK |
| SAHOL | `BIST:AKBNK` | ayni gun | 3222 | +0,280 | +0,21 / +0,34 / +0,53 | 0,000 | FILTRE |
| AKBNK | `CBOE:VIX` | gap gunu (ABD bilgisi BIST t) | 3147 | +0,021 | +0,05 / +0,01 / +0,01 | 0,321 | YOK |
| BRSAN | `AMEX:SLX−β·SP:SPX (veri: FF49 Steel)` | gap gunu (ABD bilgisi BIST t) | 3090 | +0,031 | +0,02 / +0,04 / +0,12 | 0,145 | YOK |
| BRSAN | `BIST:BRYAT` | ayni gun | 3222 | +0,565 | +0,48 / +0,63 / +0,63 | 0,000 | FILTRE |
| TRMET | `(BIST:TRALT+BIST:TRENJ)/2` | ayni gun | 3222 | +0,845 | +0,86 / +0,81 / +0,78 | 0,000 | FILTRE |
| TRALT | `AMEX:GDX−β·SP:SPX (veri: FF49 Gold)` | gap gunu (ABD bilgisi BIST t) | 3090 | +0,114 | +0,14 / +0,09 / +0,15 | 0,000 | RISK |
