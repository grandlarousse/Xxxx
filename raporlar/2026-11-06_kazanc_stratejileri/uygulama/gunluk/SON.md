# Günlük öneri — Sal 10.11.2026 kapanışı (üretim 10.11.2026 21:21 TSİ)

Sonraki BIST seansı: **Çar 11.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −1,63; Koza z3 −0,14; Kural 0 teyitsiz (VİOP kâğıt); ABD KIRMIZI.
2. **Kural 0 teyitsiz** → Çar 11.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. Takvim Çar 11.11.2026 [BIST]: MSCI duyurusu öncesi kapanış (A2, A3) — Hiçbir kolda yeni giriş yok (K1 ve eski lead-lag sinyalleri dahil).
4. KÂĞIT kaydı için TradingView alarmları (Çar 11.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz; MSCI duyurusu öncesi kapanış (A2, A3): Hiçbir kolda yeni giriş yok (K1 ve eski lead-lag sinyalleri dahil).): XU030D1!/XU030 oranı < 1,0362 AL / > 1,0503 SAT (18:08–18:15; std120 68 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 120,78 / ≤ 108,47 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 50,41 / ≤ 47,44 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
5. Takvim Çar 11.11.2026 [ABD]: Gaziler Günü: tahvil kapalı, hisse açık — En erken FTD kapanışı (06.11 1. gün olduysa); hacim şartına dikkat.
6. ABD rejimi **KIRMIZI** (09.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Cum 13.11.2026, en erken pilot Pzt 16.11.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Çar 11.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.935,71 | 17.016,34 | −%0,5 | M5=1 | BIST kapanışı → ertesi gün emir |
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 86,27 | 87,30 | −%1,2 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 71,54 | 70,70 | +%1,2 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| ABD ralli | S&P 500 | kapanış < ralli dibi | 7.353,73 | 7.549,94 | −%2,6 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| ABD | S&P 500 | kapanış < yarının 200 GHO | 7.330,12 | 7.549,94 | −%2,9 | 2 kapanış üst üste altında → KIRMIZI (b), sayım yeniden | ABD kapanışı (00:00 TSİ) |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.662 vs 13.555 (−%14,0) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%6,7 vs TLREF +%47,6; eşik ~16.120 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.517 (−%6,8) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 17.016 vs 16.940 (+%0,5) | 1 |

**Durum: KAPALI** (1/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%5,8 | — |
| b USDTRY 10g yıllık > %35 | +%23,9 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %30,7 | — |
| f MSCI danışma | hayır | — |

> KRİZ (d) yakın: son haftalık net rezerv değişimi −6,5 mlr $. Bir hafta daha ≤ −5 gelirse tetiklenir (12.11 Perşembe 14:30 rezervi).

Makro: makro.json (güncellendi 2026-11-05, 5 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −1,63 | 2026-10-22 | sinyal yok; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 1,39 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 87,30, AKBNK 70,70): z=+2 → SAHOL ≥ 95,77 ya da AKBNK ≤ 64,45; z=−2 → SAHOL ≤ 86,27 ya da AKBNK ≥ 71,54. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3546** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2202** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2348. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,15 | 14,60 | +%3,2 | ✓✓✓✓✓ | 98 | 33 | ENERJİ_DAĞITIM | — |
| ENJSA | 119,00 | 127,00 | +%6,7 | ✓✓✓✓✓ | 94 | 43 | ENERJİ_DAĞITIM | — |
| AHGAZ | 45,46 | 48,70 | +%7,1 | ✓✓✓✓✓ | 99 | 54 | ENERJİ_DAĞITIM | — |
| KCHOL | 206,00 | 225,50 | +%9,5 | ✗✓✓✓✓ | 84 | 8 | HOLDİNG | — |
| ALARK | 104,70 | 117,40 | +%12,1 | ✗✓✓✓✓ | 86 | 44 | HOLDİNG | — |
| MPARK | 435,75 | 495,00 | +%13,6 | ✗✓✓✓✓ | 81 | 57 | SAĞLIK | — |
| BIMAS | 381,25 | 433,75 | +%13,8 | ✗✓✓✓✓ | 89 | 13 | PERAKENDE | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%19,4 | +%11,7 | −%7,7 | H | 7 | %0,0 |
| 2 | HOLDİNG | Blok1 | +%17,8 | +%8,7 | −%10,1 | H | 20 | %0,0 |
| 3 | KOZA_ALTIN | Ayrıştırıcı | +%17,0 | +%2,0 | −%15,7 | H | 31 | %0,0 |
| 4 | PERAKENDE | Diğer | +%8,3 | +%2,3 | −%15,4 | H | 18 | %0,0 |
| 5 | ÇELİK | Diğer | +%7,1 | −%2,8 | −%19,7 | H | 52 | %0,0 |
| 6 | BANKA | Blok1 | +%6,6 | +%28,4 | +%6,1 | H | **0** | %77,8 |
| 7 | GYO | Blok1 | −%1,8 | +%11,9 | −%7,5 | H | 23 | %28,6 |
| 8 | SAĞLIK | Blok3 | −%6,3 | −%8,8 | −%24,6 | H | 42 | %20,0 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-10)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 51 | 15.226 | 14.608 | %30,3 | %34,5 | %35,5 | %35,6 | kapalı |
| F_XU0300227 | 108 | 15.909 | 14.608 | %30,1 | %33,4 | %35,5 | %35,6 | kapalı |
| F_XU0300427 | 171 | 16.532 | 14.608 | %28,1 | %30,2 | %35,5 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,97, spot 50,23, 20 gün → ima TL basit **%30,7** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 20 | 88,79 | 87,30 | %31,1 | +1,5 | 1.058 | 522.039 | H |
| F_SAHOL1226 | 51 | 91,14 | 87,30 | %31,5 | +1,1 | 37 | 13.808 | H |
| F_AKBNK1126 | 20 | 71,86 | 70,70 | %29,9 | +2,7 | 2.205 | 704.272 | H |
| F_AKBNK1226 | 51 | 73,94 | 70,70 | %32,8 | -0,2 | 112 | 23.885 | H |
| F_GARAN1126 | 20 | 157,10 | 155,40 | %20,0 | +12,6 | 2.190 | 141.900 | H |
| F_GARAN1226 | 51 | 161,00 | 155,40 | %25,8 | +6,8 | 99 | 7.907 | H |
| F_YKBNK1126 | 20 | 39,12 | 38,48 | %30,4 | +2,3 | 2.394 | 1.304.751 | H |
| F_YKBNK1226 | 51 | 40,27 | 38,48 | %33,3 | -0,7 | 129 | 42.551 | H |
| F_KCHOL1126 | 20 | 209,60 | 206,00 | %31,9 | +0,7 | 3.423 | 182.777 | H |
| F_KCHOL1226 | 51 | 216,00 | 206,00 | %34,7 | -2,1 | 137 | 9.552 | H |
| F_TUPRS1126 | 20 | 337,90 | 331,25 | %36,6 | -4,0 | 2.887 | 114.591 | H |
| F_TUPRS1226 | 51 | 347,35 | 331,25 | %34,8 | -2,2 | 224 | 6.308 | H |
| F_THYAO1126 | 20 | 318,85 | 313,75 | %29,7 | +2,9 | 3.916 | 302.772 | H |
| F_THYAO1226 | 51 | 328,10 | 313,75 | %32,7 | -0,1 | 215 | 11.146 | H |
| F_TRALT1126 | 20 | 39,62 | 38,90 | %33,8 | -1,2 | 1.300 | 199.963 | H |
| F_TRALT1226 | 51 | 40,63 | 38,90 | %31,8 | +0,8 | 66 | 11.202 | H |
| F_TRMET1126 | 20 | 114,35 | 112,20 | %35,0 | -2,4 | 261 | 24.883 | H |
| F_TRMET1226 | 51 | 117,25 | 112,20 | %32,2 | +0,4 | 23 | 3.265 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✗; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✗; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 423 bps, Δb −6 bps, z −0,09 (std120 dün 68 bps) | 18:08–18:15 F/S oranı **> 1,0503 SAT / < 1,0362 AL** (\|Δb\| > std120 = 68 bps; bugünkü spotla F ≥ 15.342 / ≤ 15.136; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 152 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz; takvim engeli) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 1.976 TL = 100 × 347,35 × L %5,7 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz; takvim engeli) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 −0,14, σ60 194 bps, β_TA 0,69 | TRMET ≥ 120,78 (AL) / ≤ 108,47 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,0); 6:12 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g −%1,7, z −1,00 (karar σ %1,70 sabit; vekil σ152 %1,48) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 4144,7 / 4006,1) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 29 TRALT1! (β 1,32); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 48,90 (+%1,1), sd250 %3,03 → z 0,35 (sinyal yok) | RYGYO kapanışı ≥ 50,41 (z > +1) / ≤ 47,44 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 25,88 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −1,38, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 93,58 ya da AKBNK ≤ 63,61; z=−1,5: SAHOL ≤ 86,94 ya da AKBNK ≥ 71,15 | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: yok, bugün BEKLE |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **68 bps** (117 gözlem; geçmiş 152 bülten günü, başlangıç 01.04.2026). Pencerede şok: 21.05.2026 Δb −458 bps (F_XU0300626 −%10,0, spot −%5,8) → Per 12.11.2026 akşamı pencereden çıkar; 22.05.2026 Δb 352 bps (F_XU0300626 +%8,7, spot +%4,9) → Cum 13.11.2026 akşamı pencereden çıkar. Şoklar hariç std ≈ **42 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ152 = %1,48: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 16.09 LONG (z −2,67) → 01.10; 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
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
| 25.11 | BIST | Kasım pay vadelisi son devir günü (A10) | Açık Kasım bacakları kapanışta kapatılır ya da Aralık'a devredilir. |
| 25.11 | ABD | GSYH, PCE, Bej Kitap | Yeni giriş yok. |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **09.11.2026** (FRED SP500 son 2026-11-09; CBOE VIX son 2026-11-09). Bu çalışmada işlenen yeni ABD günleri: 2026-11-09.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.549,94 (+%2,3) | — |
| S&P / 200 GHO | 7.328,22 → oran 1,030 | üstünde |
| S&P 10 / 20 / 50 GHO | 7.585 / 7.645 / 7.676 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 28.339 / 28.953 (2026-11-09) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 0,96 / 1,04 | KIRMIZI (a) |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 2. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 2. gün | — |
| FTD | yok | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 0 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: KIRMIZI** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Sal 10.11.2026 kapanışı; SARI tetiği (FTD/10>20) Çar 11.11.2026; SARI kapanışı Cum 13.11.2026; canlı pilot Pzt 16.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-05 KIRMIZI; 11-06 KIRMIZI; 11-09 KIRMIZI

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-10 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-09 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-09 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-09 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-09 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-10 | OK | 163/163 seri; bulunamayan: —; 175 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-10 | OK | önceki bülten 2026-11-09; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-10 | OK | 152 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-05 | OK | 5 gün önce |
| durum.json ABD sayaçları | 2026-11-09 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 136 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
