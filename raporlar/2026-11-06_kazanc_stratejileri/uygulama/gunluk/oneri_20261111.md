# Günlük öneri — Çar 11.11.2026 kapanışı (üretim 11.11.2026 21:21 TSİ)

Sonraki BIST seansı: **Per 12.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −2,10; Koza z3 −0,48; Kural 0 teyitsiz (VİOP kâğıt); ABD TURUNCU.
2. **Kural 0 teyitsiz** → Per 12.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. Takvim Per 12.11.2026 [BIST]: MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2) — Yeni K3/K4/K5/K9 girişi yok; eski lead-lag sinyallerinde de yeni giriş yok (K9 değiller ama bütçeleri K4 sondalarından düşer; ihtiyat); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d).
4. K1: z −2,10 ama modelde açık K1 işlemi var (sinyal 22.10) → yeni giriş yok
5. KÂĞIT kaydı için TradingView alarmları (Per 12.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz; MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2): Yeni K3/K4/K5/K9 girişi yok; eski lead-lag sinyallerinde de yeni giriş yok (K9 değiller ama bütçeleri K4 sondalarından düşer; ihtiyat); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d).): XU030D1!/XU030 oranı < 1,0352 AL / > 1,0493 SAT (18:08–18:15; std120 67 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 120,41 / ≤ 108,15 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 49,23 / ≤ 46,33 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
6. ABD rejimi **TURUNCU** (10.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Cum 13.11.2026, en erken pilot Pzt 16.11.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Per 12.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 86,13 | 86,15 | −%0,0 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 70,82 | 70,80 | +%0,0 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.930,01 | 16.977,16 | −%0,3 | M5=1 | BIST kapanışı → ertesi gün emir |
| ABD FTD | S&P 500 | kapanış ≥ +%1,5 (ralli ≥4. gün) | 7.633,74 | 7.520,93 | +%1,5 | FTD adayı (hacim teyidi elle) → SARI tetiği | ABD kapanışı (00:00 TSİ) |
| ABD FTD | Nasdaq-100 | kapanış ≥ +%1,5 (ralli ≥4. gün) | 28.156,91 | 27.740,80 | +%1,5 | FTD adayı (hacim teyidi elle) → SARI tetiği | ABD kapanışı (00:00 TSİ) |
| ABD ralli | S&P 500 | kapanış < ralli dibi | 7.353,73 | 7.520,93 | −%2,2 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| ABD | S&P 500 | kapanış < yarının 200 GHO | 7.332,85 | 7.520,93 | −%2,5 | 2 kapanış üst üste altında → KIRMIZI (b), sayım yeniden | ABD kapanışı (00:00 TSİ) |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.666 vs 13.549 (−%13,9) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%8,1 vs TLREF +%47,2; eşik ~15.884 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.466 (−%6,4) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 16.977 vs 16.936 (+%0,2) | 1 |

**Durum: KAPALI** (1/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%1,6 | — |
| b USDTRY 10g yıllık > %35 | +%22,9 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %31,8 | — |
| f MSCI danışma | hayır | — |

> KRİZ (d) yakın: son haftalık net rezerv değişimi −6,5 mlr $. Bir hafta daha ≤ −5 gelirse tetiklenir (12.11 Perşembe 14:30 rezervi).

Makro: makro.json (güncellendi 2026-11-05, 6 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −2,10 | 2026-11-11 | SİNYAL; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 1,11 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 86,15, AKBNK 70,80): z=+2 → SAHOL ≥ 96,02 ya da AKBNK ≤ 63,52; z=−2 → SAHOL ≤ 86,13 ya da AKBNK ≥ 70,82. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3562** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2165** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2168. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,10 | 14,60 | +%3,5 | ✓✓✓✓✓ | 98 | 33 | ENERJİ_DAĞITIM | — |
| AHGAZ | 45,90 | 48,70 | +%6,1 | ✓✓✓✓✓ | 98 | 53 | ENERJİ_DAĞITIM | — |
| ENJSA | 119,00 | 127,00 | +%6,7 | ✓✓✓✓✓ | 94 | 43 | ENERJİ_DAĞITIM | — |
| KCHOL | 204,00 | 225,50 | +%10,5 | ✗✓✓✓✓ | 86 | 8 | HOLDİNG | — |
| MPARK | 437,00 | 495,00 | +%13,3 | ✗✓✓✓✓ | 80 | 57 | SAĞLIK | — |
| BIMAS | 377,50 | 433,75 | +%14,9 | ✗✓✓✓✓ | 91 | 13 | PERAKENDE | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%23,6 | +%15,7 | −%4,5 | H | 8 | %0,0 |
| 2 | HOLDİNG | Blok1 | +%16,9 | +%10,0 | −%9,2 | H | 21 | %0,0 |
| 3 | KOZA_ALTIN | Ayrıştırıcı | +%15,7 | −%0,1 | −%17,5 | H | 32 | %0,0 |
| 4 | BANKA | Blok1 | +%6,7 | +%28,5 | +%6,1 | H | 1 | %66,7 |
| 5 | PERAKENDE | Diğer | +%5,7 | −%0,5 | −%17,9 | H | 19 | %0,0 |
| 6 | ÇELİK | Diğer | +%4,3 | −%5,4 | −%21,9 | H | 53 | %0,0 |
| 7 | GYO | Blok1 | −%3,3 | +%11,0 | −%8,4 | H | 24 | %14,3 |
| 8 | SAĞLIK | Blok3 | −%4,8 | −%8,5 | −%24,5 | H | 43 | %20,0 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-11)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 50 | 15.255 | 14.644 | %30,4 | %34,8 | %35,5 | %35,6 | kapalı |
| F_XU0300227 | 107 | 15.936 | 14.644 | %30,1 | %33,4 | %35,5 | %35,6 | kapalı |
| F_XU0300427 | 170 | 16.600 | 14.644 | %28,7 | %30,9 | %35,5 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,96, spot 50,23, 19 gün → ima TL basit **%31,8** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 19 | 87,54 | 86,15 | %31,0 | +1,6 | 983 | 536.604 | H |
| F_SAHOL1226 | 50 | 89,91 | 86,15 | %31,9 | +0,7 | 13 | 14.176 | H |
| F_AKBNK1126 | 19 | 71,82 | 70,80 | %27,7 | +4,9 | 1.824 | 710.421 | H |
| F_AKBNK1226 | 50 | 73,87 | 70,80 | %31,7 | +1,0 | 99 | 24.346 | H |
| F_GARAN1126 | 19 | 156,75 | 154,80 | %24,2 | +8,4 | 1.307 | 147.702 | H |
| F_GARAN1226 | 50 | 160,60 | 154,80 | %27,4 | +5,3 | 39 | 8.450 | H |
| F_YKBNK1126 | 19 | 39,02 | 38,44 | %29,0 | +3,6 | 1.763 | 1.287.923 | H |
| F_YKBNK1226 | 50 | 40,13 | 38,44 | %32,1 | +0,5 | 35 | 42.173 | H |
| F_KCHOL1126 | 19 | 207,30 | 204,00 | %31,1 | +1,5 | 2.430 | 190.849 | H |
| F_KCHOL1226 | 50 | 213,40 | 204,00 | %33,6 | -1,0 | 89 | 11.595 | H |
| F_TUPRS1126 | 19 | 354,45 | 348,50 | %32,8 | -0,2 | 2.665 | 118.344 | H |
| F_TUPRS1226 | 50 | 365,15 | 348,50 | %34,9 | -2,3 | 172 | 5.496 | H |
| F_THYAO1126 | 19 | 319,80 | 314,75 | %30,8 | +1,8 | 2.670 | 301.195 | H |
| F_THYAO1226 | 50 | 329,15 | 314,75 | %33,4 | -0,8 | 79 | 11.457 | H |
| F_TRALT1126 | 19 | 39,36 | 38,72 | %31,8 | +0,9 | 828 | 208.179 | H |
| F_TRALT1226 | 50 | 40,45 | 38,72 | %32,6 | -0,0 | 38 | 12.949 | H |
| F_TRMET1126 | 19 | 113,00 | 112,00 | %17,2 | +15,5 | 133 | 25.574 | H |
| F_TRMET1226 | 50 | 117,00 | 112,00 | %32,6 | +0,0 | 3 | 3.264 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✗; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✗; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 414 bps, Δb −9 bps, z −0,14 (std120 dün 68 bps) | 18:08–18:15 F/S oranı **> 1,0493 SAT / < 1,0352 AL** (\|Δb\| > std120 = 67 bps; bugünkü spotla F ≥ 15.366 / ≤ 15.160; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 153 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz; takvim engeli) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 2.149 TL = 100 × 365,15 × L %5,9 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz; takvim engeli) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 −0,48, σ60 193 bps, β_TA 0,69 | TRMET ≥ 120,41 (AL) / ≤ 108,15 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,0); 6:12 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g −%0,8, z −0,47 (karar σ %1,70 sabit; vekil σ153 %1,47) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 4111,8 / 3974,4) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 29 TRALT1! (β 1,31); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 47,76 (−%2,4), sd250 %3,03 → z −0,78 (sinyal yok) | RYGYO kapanışı ≥ 49,23 (z > +1) / ≤ 46,33 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 25,12 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −1,88, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 93,69 ya da AKBNK ≤ 62,31; z=−1,5: SAHOL ≤ — ya da AKBNK ≥ — | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: LONG (0 g), bugün AÇ LONG |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **67 bps** (117 gözlem; geçmiş 153 bülten günü, başlangıç 01.04.2026). Pencerede şok: 21.05.2026 Δb −458 bps (F_XU0300626 −%10,0, spot −%5,8) → Per 12.11.2026 akşamı pencereden çıkar; 22.05.2026 Δb 352 bps (F_XU0300626 +%8,7, spot +%4,9) → Cum 13.11.2026 akşamı pencereden çıkar. Şoklar hariç std ≈ **41 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ153 = %1,47: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10; 11.11 LONG açık

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
| 12.11–13.11 | BIST | MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2) | Yeni K3/K4/K5/K9 girişi yok; eski lead-lag sinyallerinde de yeni giriş yok (K9 değiller ama bütçeleri K4 sondalarından düşer; ihtiyat); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d). |
| 13.11 | BIST | Kredili esneklik seans sonunda bitiyor (A4) | Uzatılmazsa: K4 girişi 23.11'e, VİOP-47 dışı long 30.11'e kadar yok; zarardaki VİOP-47 dışı spot satılır. makro.json 'kredili_esneklik_uzatildi' alanını doldur. |
| 13.11 | ABD | 16:30 PPI | Veri günü kuralı. En erken SARI kapanışı. |
| 17.11 | ABD | NVDA sonuçları (kapanış sonrası) | Bütün kümelerde yeni giriş yok. |
| 18.11 | ABD | 22:00 FOMC tutanakları | Giriş emirleri GTD, 21:55 TSİ'de düşer. |
| 19.11 | BIST | Banka konsolide son günü; 14:30 rezerv (2. hafta) | Bilançosu gelecek bacakta K1 girişi yok (AKBNK açıkladı mı KAP'tan bak). M1 2. hafta, KRİZ (d) kontrolü. |
| 20.11 | ABD | Aylık opsiyon vadesi | Bilgi. |
| 23.11 | BIST | A4 uygulanıyorsa K4 girişleri bu kapanıştan serbest | — |
| 25.11 | BIST | Kasım pay vadelisi son devir günü (A10) | Açık Kasım bacakları kapanışta kapatılır ya da Aralık'a devredilir. |
| 25.11 | ABD | GSYH, PCE, Bej Kitap | Yeni giriş yok. |
| 26.11 | BIST | 14:30 rezerv (3. hafta) | M1 olası 1; GEÇİŞ 27.11'den geçerli olabilir. |
| 26.11 | ABD | Şükran Günü: piyasa kapalı | — |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **10.11.2026** (FRED SP500 son 2026-11-10; CBOE VIX son 2026-11-10). Bu çalışmada işlenen yeni ABD günleri: 2026-11-10.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.520,93 (−%0,4) | — |
| S&P / 200 GHO | 7.331,08 → oran 1,026 | üstünde |
| S&P 10 / 20 / 50 GHO | 7.564 / 7.631 / 7.673 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 28.148 / 28.812 (2026-11-10) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 0,94 / 0,96 | < 1,00 ✓ |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 3. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 3. gün | — |
| FTD | yok | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 0 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: TURUNCU** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Sal 10.11.2026 kapanışı; SARI tetiği (FTD/10>20) Çar 11.11.2026; SARI kapanışı Cum 13.11.2026; canlı pilot Pzt 16.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-05 KIRMIZI; 11-06 KIRMIZI; 11-09 KIRMIZI; 11-10 TURUNCU

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-11 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-10 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-10 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-10 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-10 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-11 | OK | 163/163 seri; bulunamayan: —; 177 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-11 | OK | önceki bülten 2026-11-10; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-11 | OK | 153 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-05 | OK | 6 gün önce |
| durum.json ABD sayaçları | 2026-11-10 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 130 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
