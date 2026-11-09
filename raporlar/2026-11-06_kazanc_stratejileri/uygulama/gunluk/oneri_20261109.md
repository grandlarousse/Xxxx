# Günlük öneri — Pzt 09.11.2026 kapanışı (üretim 09.11.2026 21:21 TSİ)

Sonraki BIST seansı: **Sal 10.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −1,34; Koza z3 0,26; Kural 0 teyitsiz (VİOP kâğıt); ABD KIRMIZI.
2. **Kural 0 teyitsiz** → Sal 10.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. KÂĞIT kaydı için TradingView alarmları (Sal 10.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz): XU030D1!/XU030 oranı < 1,0368 AL / > 1,0510 SAT (18:08–18:15; std120 68 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 120,35 / ≤ 108,20 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 49,87 / ≤ 46,93 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
4. Takvim Sal 10.11.2026 [ABD]: 16:30 TSİ Ekim CPI — ABD'de 16:45'ten önce emir yok (veri günü kuralı). MDT yasağı başlar.
5. ABD rejimi **KIRMIZI** (06.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Cum 13.11.2026, en erken pilot Pzt 16.11.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Sal 10.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| ABD ralli | S&P 500 | kapanış < ralli dibi | 7.353,73 | 7.376,86 | −%0,3 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.939,44 | 17.021,70 | −%0,5 | M5=1 | BIST kapanışı → ertesi gün emir |
| ABD | S&P 500 | kapanış < yarının 200 GHO | 7.327,11 | 7.376,86 | −%0,7 | 2 kapanış üst üste altında → KIRMIZI (b), sayım yeniden | ABD kapanışı (00:00 TSİ) |
| ABD ralli | Nasdaq-100 | kapanış < ralli dibi | 26.629,81 | 26.989,99 | −%1,3 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 86,74 | 88,40 | −%1,9 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 72,31 | 70,95 | +%1,9 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K4 | ENERY | kapanış > | 14,60 | 14,25 | +%2,5 | K4 sinyali → Çar 11.11.2026 18:01–18:05 AL (limit kapanış×1,06 / P_son×1,03) | BIST kapanışı → ertesi gün emir |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.713 vs 13.561 (−%13,6) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%5,8 vs TLREF +%47,6; eşik ~16.341 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.571 (−%6,8) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 17.022 vs 16.945 (+%0,5) | 1 |

**Durum: KAPALI** (1/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%6,9 | — |
| b USDTRY 10g yıllık > %35 | +%24,0 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %31,8 | — |
| f MSCI danışma | hayır | — |

> KRİZ (d) yakın: son haftalık net rezerv değişimi −6,5 mlr $. Bir hafta daha ≤ −5 gelirse tetiklenir (12.11 Perşembe 14:30 rezervi).

Makro: makro.json (güncellendi 2026-11-05, 4 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −1,34 | 2026-10-22 | sinyal yok; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 2,21 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 88,40, AKBNK 70,95): z=+2 → SAHOL ≥ 96,13 ya da AKBNK ≤ 65,24; z=−2 → SAHOL ≤ 86,74 ya da AKBNK ≥ 72,31. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3549** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2226** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2459. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,25 | 14,60 | +%2,5 | ✓✓✓✓✓ | 98 | 34 | ENERJİ_DAĞITIM | bekliyor |
| AHGAZ | 47,00 | 48,70 | +%3,6 | ✓✓✓✓✓ | 99 | 55 | ENERJİ_DAĞITIM | bekliyor |
| ENJSA | 120,60 | 127,00 | +%5,3 | ✓✓✓✓✓ | 92 | 43 | ENERJİ_DAĞITIM | — |
| KCHOL | 212,40 | 225,50 | +%6,2 | ✓✓✓✓✓ | 85 | 8 | HOLDİNG | bekliyor |
| TRGYO | 92,10 | 101,70 | +%10,4 | ✗✓✓✓✓ | 81 | 85 | GYO | — |
| MPARK | 442,00 | 495,00 | +%12,0 | ✗✓✓✓✓ | 82 | 57 | SAĞLIK | — |
| BRSAN | 685,00 | 769,50 | +%12,3 | ✗✓✓✓✓ | 91 | 26 | ÇELİK | — |
| BIMAS | 381,50 | 433,75 | +%13,7 | ✗✓✓✓✓ | 87 | 13 | PERAKENDE | bekliyor |
| RYSAS | 26,52 | 30,28 | +%14,2 | ✓✓✓✓✓ | 95 | 51 | — | bekliyor |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | KOZA_ALTIN | Ayrıştırıcı | +%24,5 | −%0,4 | −%14,9 | H | 30 | %0,0 |
| 2 | RAFİNERİ | Ayrıştırıcı | +%20,4 | +%8,2 | −%7,5 | H | 6 | %0,0 |
| 3 | HOLDİNG | Blok1 | +%19,8 | +%8,8 | −%7,0 | H | 19 | %12,5 |
| 4 | PERAKENDE | Diğer | +%9,7 | −%0,7 | −%15,1 | H | 17 | %0,0 |
| 5 | ÇELİK | Diğer | +%8,4 | −%3,9 | −%17,9 | H | 51 | %14,3 |
| 6 | BANKA | Blok1 | +%5,0 | +%28,9 | +%10,2 | E | **0** | %77,8 |
| 7 | GYO | Blok1 | −%1,7 | +%10,5 | −%5,5 | H | 22 | %42,9 |
| 8 | SAĞLIK | Blok3 | −%6,5 | −%9,6 | −%22,7 | H | 41 | %40,0 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-09)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 52 | 15.251 | 14.611 | %30,7 | %35,1 | %35,7 | %35,6 | kapalı |
| F_XU0300227 | 109 | 15.924 | 14.611 | %30,1 | %33,4 | %35,7 | %35,6 | kapalı |
| F_XU0300427 | 172 | 16.538 | 14.611 | %28,0 | %30,1 | %35,7 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,98, spot 50,18, 21 gün → ima TL basit **%31,8** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 21 | 89,97 | 88,40 | %30,9 | +1,7 | 1.398 | 513.547 | H |
| F_SAHOL1226 | 52 | 92,43 | 88,40 | %32,0 | +0,6 | 70 | 12.705 | H |
| F_AKBNK1126 | 21 | 72,15 | 70,95 | %29,4 | +3,2 | 3.014 | 725.382 | H |
| F_AKBNK1226 | 52 | 74,22 | 70,95 | %32,4 | +0,3 | 145 | 23.162 | H |
| F_GARAN1126 | 21 | 155,35 | 153,10 | %25,5 | +7,1 | 3.153 | 143.343 | H |
| F_GARAN1226 | 52 | 159,25 | 153,10 | %28,2 | +4,4 | 122 | 5.201 | H |
| F_YKBNK1126 | 21 | 39,38 | 38,74 | %28,7 | +3,9 | 2.747 | 1.344.907 | H |
| F_YKBNK1226 | 52 | 40,49 | 38,74 | %31,7 | +0,9 | 83 | 36.604 | H |
| F_KCHOL1126 | 21 | 216,40 | 212,40 | %32,7 | -0,1 | 2.076 | 163.687 | H |
| F_KCHOL1226 | 52 | 222,75 | 212,40 | %34,2 | -1,6 | 52 | 7.250 | H |
| F_TUPRS1126 | 21 | 338,65 | 332,25 | %33,5 | -0,9 | 4.393 | 113.507 | H |
| F_TUPRS1226 | 52 | 348,90 | 332,25 | %35,2 | -2,6 | 199 | 4.628 | H |
| F_THYAO1126 | 21 | 315,40 | 310,00 | %30,3 | +2,3 | 4.111 | 307.685 | H |
| F_THYAO1226 | 52 | 324,45 | 310,00 | %32,7 | -0,1 | 287 | 11.984 | H |
| F_TRALT1126 | 21 | 40,79 | 40,24 | %23,8 | +8,8 | 1.184 | 182.145 | H |
| F_TRALT1226 | 52 | 41,80 | 40,24 | %27,2 | +5,4 | 28 | 4.570 | H |
| F_TRMET1126 | 21 | 118,15 | 115,90 | %33,7 | -1,1 | 228 | 27.385 | H |
| F_TRMET1226 | 52 | 121,50 | 115,90 | %33,9 | -1,3 | 11 | 2.656 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✗; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✗; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 429 bps, Δb 24 bps, z 0,36 (std120 dün 68 bps) | 18:08–18:15 F/S oranı **> 1,0510 SAT / < 1,0368 AL** (\|Δb\| > std120 = 68 bps; bugünkü spotla F ≥ 15.355 / ≤ 15.149; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 153 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 1.997 TL = 100 × 348,90 × L %5,7 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 0,26, σ60 192 bps, β_TA 0,69 | TRMET ≥ 120,35 (AL) / ≤ 108,20 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,0); 6:12 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g +%1,6, z 0,94 (karar σ %1,70 sabit; vekil σ151 %1,48) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 4215,6 / 4074,6) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 28 TRALT1! (β 1,31); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 48,38 (−%1,5), sd250 %3,03 → z −0,49 (sinyal yok) | RYGYO kapanışı ≥ 49,87 (z > +1) / ≤ 46,93 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 26,52 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −1,00, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 93,83 ya da AKBNK ≤ 64,81; z=−1,5: SAHOL ≤ 87,25 ya da AKBNK ≥ 72,38 | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: yok, bugün BEKLE |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **68 bps** (117 gözlem; geçmiş 151 bülten günü, başlangıç 01.04.2026). Pencerede şok: 21.05.2026 Δb −458 bps (F_XU0300626 −%10,0, spot −%5,8) → Per 12.11.2026 akşamı pencereden çıkar; 22.05.2026 Δb 352 bps (F_XU0300626 +%8,7, spot +%4,9) → Cum 13.11.2026 akşamı pencereden çıkar. Şoklar hariç std ≈ **42 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ151 = %1,48: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 16.09 LONG (z −2,67) → 01.10; 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
| 10.11 | ABD | 16:30 TSİ Ekim CPI | ABD'de 16:45'ten önce emir yok (veri günü kuralı). MDT yasağı başlar. |
| 11.11 | BIST | MSCI duyurusu öncesi kapanış (A2, A3) | Hiçbir kolda yeni giriş yok (K1 ve eski lead-lag sinyalleri dahil). |
| 11.11 | ABD | Gaziler Günü: tahvil kapalı, hisse açık | En erken FTD kapanışı (06.11 1. gün olduysa); hacim şartına dikkat. |
| 12.11–13.11 | BIST | MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2) | Yeni K3/K4/K5/K9 girişi yok; eski lead-lag sinyallerinde de yeni giriş yok (K9 değiller ama bütçeleri K4 sondalarından düşer; ihtiyat); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d). |
| 13.11 | BIST | Kredili esneklik seans sonunda bitiyor (A4) | Uzatılmazsa: K4 girişi 23.11'e, VİOP-47 dışı long 30.11'e kadar yok; zarardaki VİOP-47 dışı spot satılır. makro.json 'kredili_esneklik_uzatildi' alanını doldur. |
| 13.11 | ABD | 16:30 PPI | Veri günü kuralı. En erken SARI kapanışı. |
| 17.11 | ABD | NVDA sonuçları (kapanış sonrası) | Bütün kümelerde yeni giriş yok. |
| 18.11 | ABD | 22:00 FOMC tutanakları | Giriş emirleri GTD, 21:55 TSİ'de düşer. |
| 19.11 | BIST | Banka konsolide son günü; 14:30 rezerv (2. hafta) | Bilançosu gelecek bacakta K1 girişi yok (AKBNK açıkladı mı KAP'tan bak). M1 2. hafta, KRİZ (d) kontrolü. |
| 20.11 | ABD | Aylık opsiyon vadesi | Bilgi. |
| 23.11 | BIST | A4 uygulanıyorsa K4 girişleri bu kapanıştan serbest | — |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

9.11'e kadar bilanço bekleyen (KAP teyitli değil): AHGAZ, AKSEN, ALARK, ARCLK, ASTOR, BIMAS, CIMSA, DOAS, EKGYO, ENERY, EREGL, GUBRF, HEKTS, KCHOL, KRDMD, ODAS, OYAKC, PGSUS, RYSAS, SOKM, TCELL, TKFEN, TRALT, TRMET, VESTL.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **06.11.2026** (FRED SP500 son 2026-11-05, S&P kapanışı teyitsiz kaynak (durum.json 'teyitsiz'); CBOE VIX son 2026-11-06). Bu çalışmada işlenen yeni ABD günleri: yok.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.376,86 (+%0,3) | — |
| S&P / 200 GHO | 7.325,05 → oran 1,007 | üstünde; yakın bölge (< 1,02) |
| S&P 10 / 20 / 50 GHO | 7.597 / 7.658 / 7.679 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 28.475 / 29.091 (2026-11-06) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 1,04 / 1,10 | KIRMIZI (a) |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | hayır | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 1. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 1. gün | — |
| FTD | yok | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 0 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: KIRMIZI** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Sal 10.11.2026 kapanışı; SARI tetiği (FTD/10>20) Çar 11.11.2026; SARI kapanışı Cum 13.11.2026; canlı pilot Pzt 16.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-05 KIRMIZI; 11-06 KIRMIZI

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-09 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-05 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-06 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-06 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-06 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-09 | OK | 163/163 seri; bulunamayan: —; 177 istek; eksik geçmiş tekrarı 14 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-09 | OK | önceki bülten 2026-11-06; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-09 | OK | 151 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-05 | OK | 4 gün önce |
| durum.json ABD sayaçları | 2026-11-06 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 213 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
