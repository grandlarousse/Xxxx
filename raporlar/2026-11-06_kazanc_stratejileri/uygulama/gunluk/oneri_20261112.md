# Günlük öneri — Per 12.11.2026 kapanışı (üretim 12.11.2026 21:22 TSİ)

Sonraki BIST seansı: **Cum 13.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −2,31; Koza z3 −0,81; Kural 0 teyitsiz (VİOP kâğıt); ABD TURUNCU.
2. **Kural 0 teyitsiz** → Cum 13.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. Takvim Cum 13.11.2026 [BIST]: MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2) — Yeni K3/K4/K5/K9 girişi yok; eski lead-lag sinyallerinde de yeni giriş yok (K9 değiller ama bütçeleri K4 sondalarından düşer; ihtiyat); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d).
4. KÂĞIT — ALTIN → TRALT: F_XAUUSD1226 uzlaşma değişimi −%3,7 (z −2,19) eşiği aştı; kural bugünkü uzlaşmada **TRALT1! SAT + XU030D1! AL** girerdi → yalnız kâğıt kaydı (düşük güvenli; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz, planda canlı kanalı yok); kâğıtta 2 gün sonra 17:55'te z'ye bak
5. K1: z −2,31 ama modelde açık K1 işlemi var (sinyal 22.10) → yeni giriş yok
6. KÂĞIT kaydı için TradingView alarmları (Cum 13.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz; MSCI sonuçları (12.11 01:00), 14:30 rezerv, SPK kredili esneklik kararı (A2): Yeni K3/K4/K5/K9 girişi yok; eski lead-lag sinyallerinde de yeni giriş yok (K9 değiller ama bütçeleri K4 sondalarından düşer; ihtiyat); K1 normal. 12.11 14:30 rezervi makro.json'a yaz: haftalık değişim ≤ −5 mlr $ ise KRİZ (d).): XU030D1!/XU030 oranı < 1,0313 AL / > 1,0423 SAT (18:08–18:15; std120 53 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 115,30 / ≤ 103,75 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 47,79 / ≤ 44,97 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
7. Takvim Cum 13.11.2026 [BIST]: Kredili esneklik seans sonunda bitiyor (A4) — Uzatılmazsa: K4 girişi 23.11'e, VİOP-47 dışı long 30.11'e kadar yok; zarardaki VİOP-47 dışı spot satılır. makro.json 'kredili_esneklik_uzatildi' alanını doldur.
8. Takvim Cum 13.11.2026 [ABD]: 16:30 PPI — Veri günü kuralı. En erken SARI kapanışı.
9. ABD rejimi **TURUNCU** (11.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Cum 13.11.2026, en erken pilot Pzt 16.11.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Cum 13.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.923,36 | 16.859,08 | +%0,4 | M5=1 | BIST kapanışı → ertesi gün emir |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 69,73 | 70,10 | −%0,5 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 84,95 | 84,50 | +%0,5 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K4 | ENERY | kapanış > | 14,60 | 14,45 | +%1,0 | K4 sinyali → Pzt 16.11.2026 18:01–18:05 AL (limit kapanış×1,06 / P_son×1,03) | BIST kapanışı → ertesi gün emir |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.811 vs 13.543 (−%12,8) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%11,7 vs TLREF +%47,2; eşik ~15.570 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.421 (−%4,9) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 16.859 vs 16.930 (−%0,4) | 0 |

**Durum: KAPALI** (0/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%4,2 | — |
| b USDTRY 10g yıllık > %35 | +%20,1 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %32,6 | — |
| f MSCI danışma | hayır | — |

> KRİZ (d) yakın: son haftalık net rezerv değişimi −6,5 mlr $. Bir hafta daha ≤ −5 gelirse tetiklenir (19.11 Perşembe 14:30 rezervi).

Makro: makro.json (güncellendi 2026-11-05, 7 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −2,31 | 2026-11-11 | SİNYAL; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 1,18 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 84,50, AKBNK 70,10): z=+2 → SAHOL ≥ 95,19 ya da AKBNK ≤ 62,23; z=−2 → SAHOL ≤ 84,95 ya da AKBNK ≥ 69,73. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3579** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2119** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2054. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,45 | 14,60 | +%1,0 | ✓✓✓✓✓ | 98 | 33 | ENERJİ_DAĞITIM | — |
| AHGAZ | 46,20 | 48,70 | +%5,4 | ✓✓✓✓✓ | 98 | 53 | ENERJİ_DAĞITIM | — |
| ENJSA | 118,50 | 127,00 | +%7,2 | ✓✓✓✓✓ | 94 | 42 | ENERJİ_DAĞITIM | — |
| KCHOL | 208,20 | 225,50 | +%8,3 | ✗✓✓✓✓ | 86 | 8 | HOLDİNG | — |
| MPARK | 452,50 | 495,00 | +%9,4 | ✗✓✓✓✓ | 84 | 58 | SAĞLIK | — |
| ALARK | 106,70 | 117,40 | +%10,0 | ✓✓✓✓✓ | 85 | 44 | HOLDİNG | — |
| BIMAS | 388,00 | 433,75 | +%11,8 | ✗✓✓✓✓ | 91 | 13 | PERAKENDE | — |
| TUPRS | 357,00 | 409,90 | +%14,8 | ✗✓✓✓✓ | 96 | 5 | RAFİNERİ | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%26,3 | +%12,7 | −%6,1 | H | 9 | %0,0 |
| 2 | HOLDİNG | Blok1 | +%15,7 | +%9,7 | −%8,6 | H | 22 | %12,5 |
| 3 | KOZA_ALTIN | Ayrıştırıcı | +%10,7 | −%1,3 | −%17,7 | H | 33 | %0,0 |
| 4 | BANKA | Blok1 | +%5,1 | +%27,6 | +%6,4 | H | 2 | %77,8 |
| 5 | ÇELİK | Diğer | +%4,7 | −%5,9 | −%21,6 | H | 54 | %0,0 |
| 6 | PERAKENDE | Diğer | +%4,7 | −%1,9 | −%18,2 | H | 20 | %0,0 |
| 7 | SAĞLIK | Blok3 | −%3,1 | −%7,2 | −%22,7 | H | 44 | %40,0 |
| 8 | GYO | Blok1 | −%3,3 | +%10,0 | −%8,3 | H | 25 | %14,3 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-12)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 49 | 15.362 | 14.815 | %27,5 | %31,0 | %35,6 | %35,6 | kapalı |
| F_XU0300227 | 106 | 16.053 | 14.815 | %28,8 | %31,8 | %35,6 | %35,6 | kapalı |
| F_XU0300427 | 169 | 16.687 | 14.815 | %27,3 | %29,3 | %35,6 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,96, spot 50,25, 18 gün → ima TL basit **%32,6** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 18 | 85,84 | 84,50 | %32,2 | +0,4 | 2.102 | 546.428 | H |
| F_SAHOL1226 | 49 | 88,56 | 84,50 | %35,8 | -3,2 | 106 | 17.089 | H |
| F_AKBNK1126 | 18 | 71,00 | 70,10 | %26,0 | +6,6 | 2.938 | 744.818 | H |
| F_AKBNK1226 | 49 | 73,06 | 70,10 | %31,5 | +1,2 | 134 | 26.145 | H |
| F_GARAN1126 | 18 | 154,35 | 152,60 | %23,3 | +9,3 | 1.590 | 149.704 | H |
| F_GARAN1226 | 49 | 158,20 | 152,60 | %27,3 | +5,3 | 94 | 9.654 | H |
| F_YKBNK1126 | 18 | 38,38 | 37,90 | %25,7 | +6,9 | 2.744 | 1.301.629 | H |
| F_YKBNK1226 | 49 | 39,54 | 37,90 | %32,2 | +0,4 | 94 | 48.795 | H |
| F_KCHOL1126 | 18 | 211,10 | 208,20 | %28,2 | +4,4 | 2.543 | 183.731 | H |
| F_KCHOL1226 | 49 | 217,55 | 208,20 | %33,5 | -0,8 | 99 | 11.404 | H |
| F_TUPRS1126 | 18 | 361,10 | 357,00 | %23,3 | +9,3 | 2.594 | 113.085 | H |
| F_TUPRS1226 | 49 | 370,85 | 357,00 | %28,9 | +3,7 | 141 | 5.157 | H |
| F_THYAO1126 | 18 | 323,65 | 319,00 | %29,6 | +3,0 | 3.758 | 292.446 | H |
| F_THYAO1226 | 49 | 332,90 | 319,00 | %32,5 | +0,1 | 376 | 11.121 | H |
| F_TRALT1126 | 18 | 38,15 | 37,68 | %25,3 | +7,3 | 983 | 216.742 | H |
| F_TRALT1226 | 49 | 39,05 | 37,68 | %27,1 | +5,5 | 33 | 15.205 | H |
| F_TRMET1126 | 18 | 109,75 | 108,30 | %27,1 | +5,5 | 141 | 25.542 | H |
| F_TRMET1226 | 49 | 112,65 | 108,30 | %29,9 | +2,7 | 11 | 3.365 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✗; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✗; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 361 bps, Δb −53 bps, z −0,78 (std120 dün 67 bps) | 18:08–18:15 F/S oranı **> 1,0423 SAT / < 1,0313 AL** (\|Δb\| > std120 = 53 bps; bugünkü spotla F ≥ 15.442 / ≤ 15.279; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 154 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz; takvim engeli) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 2.105 TL = 100 × 370,85 × L %5,7 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz; takvim engeli) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 −0,81, σ60 194 bps, β_TA 0,69 | TRMET ≥ 115,30 (AL) / ≤ 103,75 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,0); 7:14 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g −%3,7, z −2,19 (karar σ %1,70 sabit; vekil σ154 %1,50) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 3961,7 / 3829,2) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 30 TRALT1! (β 1,30); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 46,36 (−%3,0), sd250 %3,03 → z −0,98 (sinyal yok) | RYGYO kapanışı ≥ 47,79 (z > +1) / ≤ 44,97 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 25,62 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −2,26, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 93,12 ya da AKBNK ≤ 60,48; z=−1,5: SAHOL ≤ — ya da AKBNK ≥ — | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: LONG (1 g), bugün TUT |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **53 bps** (117 gözlem; geçmiş 154 bülten günü, başlangıç 01.04.2026). Pencerede şok: 22.05.2026 Δb 352 bps (F_XU0300626 +%8,7, spot +%4,9) → Cum 13.11.2026 akşamı pencereden çıkar. Şoklar hariç std ≈ **41 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ154 = %1,50: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

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
| 27.11 | ABD | Erken kapanış 21:00 TSİ | Yeni giriş yok. |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **11.11.2026** (FRED SP500 son 2026-11-11; CBOE VIX son 2026-11-11). Bu çalışmada işlenen yeni ABD günleri: 2026-11-11.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.619,38 (+%1,3) | — |
| S&P / 200 GHO | 7.334,28 → oran 1,039 | üstünde |
| S&P 10 / 20 / 50 GHO | 7.552 / 7.626 / 7.673 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 28.004 / 28.733 (2026-11-11) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 0,91 / 0,94 | < 1,00 ✓ |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 4. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 4. gün | — |
| FTD | 2026-11-11 NDX +%2,3 (hacim teyidi: None; durum.json 'ftd_hacim_teyit' true/false); 15 seans içinde 10>20: henüz yok (0. seans); FTD günü dibi (YEŞİL şartı, durum.json abd.ftd.gun_dibi elle): girilmedi | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 1 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: TURUNCU** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Çar 11.11.2026 kapanışı; SARI tetiği (FTD/10>20) mevcut; SARI kapanışı Cum 13.11.2026; canlı pilot Pzt 16.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

- 2026-11-11: NDX +%2,28 ile FTD ADAYI (ralli 4. gün). Hacim teyidi elle: SPY/QQQ hacmi önceki günden yüksek mi?

Son günler: 11-05 KIRMIZI; 11-06 KIRMIZI; 11-09 KIRMIZI; 11-10 TURUNCU; 11-11 TURUNCU

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | YEDEK | BIST100 100 hisse (yedek) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-12 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-11 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-11 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-11 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-11 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-12 | OK | 163/163 seri; bulunamayan: —; 175 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-12 | OK | önceki bülten 2026-11-11; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-12 | OK | 154 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-05 | OK | 7 gün önce |
| durum.json ABD sayaçları | 2026-11-11 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 126 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
