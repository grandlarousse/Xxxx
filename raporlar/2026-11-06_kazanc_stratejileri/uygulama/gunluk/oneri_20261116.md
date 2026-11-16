# Günlük öneri — Pzt 16.11.2026 kapanışı (üretim 16.11.2026 21:26 TSİ)

Sonraki BIST seansı: **Sal 17.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **Kural 0 teyitsiz** → Sal 17.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
2. K4 **ENERY AL (spot)** — Sal 17.11.2026 18:01–18:05 kapanış seansı limitli alış, limit min(15,62; P_son × 1,03); iz-stop (E1) kapanış ≤ girişten beri en yüksek kapanış × 0,85 (bugünkü kapanışla ≈ 12,53); boyut 12 bin TL (stop mesafesi %15 ile; 1,0 mn TL hesap, r₀ %0,25); çıkış iz-stop ya da 120 gün
3. ABD rejimi **SARI** (13.11 kapanışı) → pilot izinli: 16:45–17:15 TSİ bekleyen emir, işlem başı %0,25 risk, yakın bölgede tek pozisyon (PLAN_ABD §2.2)
4. KÂĞIT kaydı için TradingView alarmları (Sal 17.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz): XU030D1!/XU030 oranı < 1,0325 AL / > 1,0410 SAT (18:08–18:15; std120 41 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 117,76 / ≤ 105,94 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 48,35 / ≤ 45,49 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
5. Takvim Sal 17.11.2026 [ABD]: NVDA sonuçları (kapanış sonrası) — Bütün kümelerde yeni giriş yok.

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Sal 17.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 84,26 | 84,70 | −%0,5 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 70,27 | 69,90 | +%0,5 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.907,65 | 16.643,80 | +%1,6 | M5=1 | BIST kapanışı → ertesi gün emir |
| KOZA | TRMET | kapanış ≥ (TRALT, TRENJ yatay) | 117,76 | 115,20 | +%2,2 | aynı gün uzlaşmada TRMET1! AL + TRALT1! SAT — **KÂĞIT** | aynı gün 17:45–17:55 alarm → yalnız kâğıt kaydı |
| ABD ralli | S&P 500 | kapanış < ralli dibi | 7.353,73 | 7.561,67 | −%2,7 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| ABD | S&P 500 | kapanış < yarının 200 GHO | 7.342,33 | 7.561,67 | −%2,9 | 2 kapanış üst üste altında → KIRMIZI (b), sayım yeniden | ABD kapanışı (00:00 TSİ) |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.842 vs 13.530 (−%12,5) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%11,4 vs TLREF +%47,5; eşik ~15.674 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.336 (−%4,0) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 → 27,4 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 16.644 vs 16.916 (−%1,6) | 0 |

**Durum: KAPALI** (0/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%1,1 | — |
| b USDTRY 10g yıllık > %35 | +%23,3 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 / 3,1 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %32,8 | — |
| f MSCI danışma | hayır | — |

Makro: makro.json (güncellendi 2026-11-16, 0 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −1,93 | 2026-11-11 | sinyal yok; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 0,85 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 84,70, AKBNK 69,90): z=+2 → SAHOL ≥ 94,91 ya da AKBNK ≤ 62,38; z=−2 → SAHOL ≤ 84,26 ya da AKBNK ≥ 70,27. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3577** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2054** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2117. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

| Hisse | Kapanış | RS | Lik. | Küme/Blok | Stop | Boyut bin TL | Engel (sonraki seans) |
|---|---|---|---|---|---|---|---|
| ENERY | 14,74 | 99 | 33 | ENERJİ_DAĞITIM/Diğer | %15 | 12 | — |

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENJSA | 121,10 | 127,00 | +%4,9 | ✓✓✓✓✓ | 94 | 42 | ENERJİ_DAĞITIM | — |
| MPARK | 462,75 | 495,00 | +%7,0 | ✗✓✓✓✓ | 90 | 58 | SAĞLIK | — |
| ALARK | 107,50 | 117,40 | +%9,2 | ✓✓✓✓✓ | 84 | 45 | HOLDİNG | — |
| KCHOL | 205,50 | 225,50 | +%9,7 | ✗✓✓✓✓ | 82 | 8 | HOLDİNG | — |
| BIMAS | 394,50 | 433,75 | +%9,9 | ✗✓✓✓✓ | 91 | 13 | PERAKENDE | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%25,3 | +%10,6 | −%7,3 | H | 11 | %25,0 |
| 2 | HOLDİNG | Blok1 | +%15,2 | +%8,4 | −%9,1 | H | 24 | %12,5 |
| 3 | ÇELİK | Diğer | +%7,2 | −%7,4 | −%22,4 | H | 56 | %0,0 |
| 4 | PERAKENDE | Diğer | +%6,8 | +%0,4 | −%15,8 | H | 22 | %0,0 |
| 5 | KOZA_ALTIN | Ayrıştırıcı | +%2,7 | +%3,5 | −%13,2 | H | 35 | %0,0 |
| 6 | BANKA | Blok1 | +%1,7 | +%25,1 | +%4,8 | H | 4 | %66,7 |
| 7 | SAĞLIK | Blok3 | −%0,1 | −%9,1 | −%23,8 | H | 46 | %20,0 |
| 8 | GYO | Blok1 | −%2,2 | +%11,0 | −%7,0 | H | 27 | %14,3 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-16)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 45 | 15.388 | 14.842 | %29,9 | %34,1 | %35,8 | %35,6 | kapalı |
| F_XU0300227 | 102 | 16.070 | 14.842 | %29,6 | %32,9 | %35,8 | %35,6 | kapalı |
| F_XU0300427 | 165 | 16.704 | 14.842 | %27,8 | %29,9 | %35,8 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,94, spot 50,39, 14 gün → ima TL basit **%32,8** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 14 | 85,70 | 84,70 | %30,8 | +1,8 | 633 | 552.346 | H |
| F_SAHOL1226 | 45 | 88,19 | 84,70 | %33,4 | -0,8 | 135 | 23.168 | H |
| F_AKBNK1126 | 14 | 70,68 | 69,90 | %29,1 | +3,5 | 1.651 | 742.076 | H |
| F_AKBNK1226 | 45 | 72,73 | 69,90 | %32,8 | -0,2 | 124 | 29.778 | H |
| F_GARAN1126 | 14 | 151,75 | 150,10 | %28,7 | +3,9 | 1.188 | 138.429 | H |
| F_GARAN1226 | 45 | 155,75 | 150,10 | %30,5 | +2,1 | 87 | 11.864 | H |
| F_YKBNK1126 | 14 | 37,95 | 37,48 | %32,7 | -0,1 | 1.390 | 1.245.999 | H |
| F_YKBNK1226 | 45 | 39,07 | 37,48 | %34,4 | -1,8 | 81 | 54.716 | H |
| F_KCHOL1126 | 14 | 207,90 | 205,50 | %30,4 | +2,2 | 1.481 | 189.303 | H |
| F_KCHOL1226 | 45 | 214,10 | 205,50 | %33,9 | -1,3 | 60 | 12.894 | H |
| F_TUPRS1126 | 14 | 360,55 | 356,00 | %33,3 | -0,7 | 1.877 | 112.677 | H |
| F_TUPRS1226 | 45 | 370,15 | 356,00 | %32,2 | +0,4 | 72 | 6.652 | H |
| F_THYAO1126 | 14 | 326,95 | 323,50 | %27,8 | +4,8 | 2.330 | 292.968 | H |
| F_THYAO1226 | 45 | 336,10 | 323,50 | %31,6 | +1,0 | 200 | 12.585 | H |
| F_TRALT1126 | 14 | 39,23 | 38,76 | %31,6 | +1,0 | 1.123 | 224.115 | H |
| F_TRALT1226 | 45 | 40,26 | 38,76 | %31,4 | +1,2 | 54 | 21.488 | H |
| F_TRMET1126 | 14 | 116,25 | 115,20 | %23,8 | +8,8 | 499 | 34.685 | H |
| F_TRMET1226 | 45 | 118,45 | 115,20 | %22,9 | +9,7 | 41 | 4.233 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✓; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✓; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 361 bps, Δb −20 bps, z −0,48 (std120 dün 41 bps) | 18:08–18:15 F/S oranı **> 1,0410 SAT / < 1,0325 AL** (\|Δb\| > std120 = 41 bps; bugünkü spotla F ≥ 15.451 / ≤ 15.324; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 154 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 2.076 TL = 100 × 370,15 × L %5,6 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 0,52, σ60 188 bps, β_TA 0,69 | TRMET ≥ 117,76 (AL) / ≤ 105,94 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,1); 6:12 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g −%0,3, z −0,16 (karar σ %1,70 sabit; vekil σ156 %1,49) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 3969,3 / 3836,6) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 29 TRALT1! (β 1,30); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 46,90 (−%0,5), sd250 %3,03 → z −0,17 (sinyal yok) | RYGYO kapanışı ≥ 48,35 (z > +1) / ≤ 45,49 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 25,50 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −1,91, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 92,79 ya da AKBNK ≤ 60,85; z=−1,5: SAHOL ≤ — ya da AKBNK ≥ — | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: LONG (3 g), bugün TUT |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **41 bps** (117 gözlem; geçmiş 156 bülten günü, başlangıç 01.04.2026). Pencerede şok: 16.09.2026 Δb −190 bps (F_XU0301026 −%7,4, spot −%5,6) → Cum 05.03.2027 akşamı pencereden çıkar. Şoklar hariç std ≈ **38 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ156 = %1,49: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10; 11.11 LONG açık

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
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
| 30.11 | BIST | VİOP Kasım vadesi; MSCI yürürlüğü; ay sonu | Vade gününe pozisyon taşınmaz. T2 ve 12 ay küme RS sırası. MSCI'dan çıkarılan hisseler bu kapanışa kadar alınmaz. |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **13.11.2026** (FRED SP500 son 2026-11-13; CBOE VIX son 2026-11-13). Bu çalışmada işlenen yeni ABD günleri: yok.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.561,67 (−%0,4) | — |
| S&P / 200 GHO | 7.340,32 → oran 1,030 | üstünde |
| S&P 10 / 20 / 50 GHO | 7.537 / 7.613 / 7.667 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 27.848 / 28.588 (2026-11-13) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 0,94 / 0,93 | < 1,00 ✓ |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 6. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 6. gün | — |
| FTD | 2026-11-11 NDX +%2,3 (hacim teyidi: None; durum.json 'ftd_hacim_teyit' true/false); 15 seans içinde 10>20: henüz yok (2. seans); FTD günü dibi (YEŞİL şartı, durum.json abd.ftd.gun_dibi elle): girilmedi | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 3 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: SARI** → günde ≤ 2 giriş, ≤ 4 açık, yakın bölgede 1 pozisyon / ısı ≤ %0,5; AI dışı izinli kümeler; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Cum 13.11.2026 kapanışı; SARI tetiği (FTD/10>20) mevcut; SARI kapanışı Cum 13.11.2026; canlı pilot Pzt 16.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-09 KIRMIZI; 11-10 TURUNCU; 11-11 TURUNCU; 11-12 TURUNCU; 11-13 SARI

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-16 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-13 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-13 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-13 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-13 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-16 | OK | 163/163 seri; bulunamayan: —; 175 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-16 | OK | önceki bülten 2026-11-13; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-16 | OK | 156 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-16 | OK | 0 gün önce |
| durum.json ABD sayaçları | 2026-11-13 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 131 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
