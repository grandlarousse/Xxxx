# Günlük öneri — Cum 13.11.2026 kapanışı (üretim 13.11.2026 21:21 TSİ)

Sonraki BIST seansı: **Pzt 16.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

> **Uyarı:** makro.json 8 gündür güncellenmedi (son 2026-11-05) → M1/M2/KRİZ (c, d)/K6 BAYAT olabilir.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −1,83; Koza z3 −0,19; Kural 0 teyitsiz (VİOP kâğıt); ABD TURUNCU.
2. **Kural 0 teyitsiz** → Pzt 16.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. KÂĞIT kaydı için TradingView alarmları (Pzt 16.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz): XU030D1!/XU030 oranı < 1,0345 AL / > 1,0431 SAT (18:08–18:15; std120 41 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 117,66 / ≤ 106,20 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 48,60 / ≤ 45,73 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
4. ABD rejimi **TURUNCU** (12.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Cum 13.11.2026, en erken pilot Pzt 16.11.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Pzt 16.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| K4 | ENERY | kapanış > | 14,60 | 14,60 | +%0,0 | K4 sinyali → Sal 17.11.2026 18:01–18:05 AL (limit kapanış×1,06 / P_son×1,03) | BIST kapanışı → ertesi gün emir |
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 84,57 | 85,20 | −%0,7 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 70,47 | 69,95 | +%0,8 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.917,32 | 16.743,11 | +%1,0 | M5=1 | BIST kapanışı → ertesi gün emir |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.843 vs 13.537 (−%12,5) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%11,3 vs TLREF +%47,2; eşik ~15.663 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.380 (−%4,3) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 16.743 vs 16.922 (−%1,1) | 0 |

**Durum: KAPALI** (0/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | +%3,1 | — |
| b USDTRY 10g yıllık > %35 | +%24,2 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %29,8 | — |
| f MSCI danışma | hayır | — |

> KRİZ (d) yakın: son haftalık net rezerv değişimi −6,5 mlr $. Bir hafta daha ≤ −5 gelirse tetiklenir (19.11 Perşembe 14:30 rezervi).

Makro: makro.json (güncellendi 2026-11-05, 8 gün önce → BAYAT).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −1,83 | 2026-11-11 | sinyal yok; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 1,05 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 85,20, AKBNK 69,95): z=+2 → SAHOL ≥ 94,94 ya da AKBNK ≤ 62,77; z=−2 → SAHOL ≤ 84,57 ya da AKBNK ≥ 70,47. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3572** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2089** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2180. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,60 | 14,60 | +%0,0 | ✓✓✓✓✓ | 99 | 33 | ENERJİ_DAĞITIM | — |
| ENJSA | 122,30 | 127,00 | +%3,8 | ✓✓✓✓✓ | 94 | 43 | ENERJİ_DAĞITIM | — |
| AHGAZ | 46,24 | 48,70 | +%5,3 | ✓✓✓✓✓ | 98 | 53 | ENERJİ_DAĞITIM | — |
| MPARK | 466,00 | 495,00 | +%6,2 | ✗✓✓✓✓ | 88 | 58 | SAĞLIK | — |
| ALARK | 109,10 | 117,40 | +%7,6 | ✓✓✓✓✓ | 88 | 44 | HOLDİNG | — |
| KCHOL | 207,50 | 225,50 | +%8,7 | ✗✓✓✓✓ | 86 | 8 | HOLDİNG | — |
| BIMAS | 395,50 | 433,75 | +%9,7 | ✗✓✓✓✓ | 91 | 13 | PERAKENDE | — |
| TUPRS | 359,00 | 409,90 | +%14,2 | ✗✓✓✓✓ | 96 | 5 | RAFİNERİ | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%27,0 | +%11,3 | −%6,7 | H | 10 | %0,0 |
| 2 | HOLDİNG | Blok1 | +%15,9 | +%8,9 | −%8,8 | H | 23 | %12,5 |
| 3 | ÇELİK | Diğer | +%8,0 | −%7,7 | −%22,6 | H | 55 | %0,0 |
| 4 | KOZA_ALTIN | Ayrıştırıcı | +%6,1 | −%1,0 | −%17,1 | H | 34 | %0,0 |
| 5 | PERAKENDE | Diğer | +%5,0 | −%0,1 | −%16,3 | H | 21 | %0,0 |
| 6 | BANKA | Blok1 | +%3,1 | +%25,6 | +%5,3 | H | 3 | %66,7 |
| 7 | SAĞLIK | Blok3 | −%1,9 | −%8,6 | −%23,4 | H | 45 | %20,0 |
| 8 | GYO | Blok1 | −%2,1 | +%10,8 | −%7,1 | H | 26 | %14,3 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-13)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 48 | 15.414 | 14.845 | %29,2 | %33,1 | %35,6 | %35,6 | kapalı |
| F_XU0300227 | 105 | 16.102 | 14.845 | %29,4 | %32,7 | %35,6 | %35,6 | kapalı |
| F_XU0300427 | 168 | 16.716 | 14.845 | %27,4 | %29,4 | %35,6 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,97, spot 50,37, 17 gün → ima TL basit **%29,8** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 17 | 86,32 | 85,20 | %28,2 | +4,4 | 948 | 556.391 | H |
| F_SAHOL1226 | 48 | 88,73 | 85,20 | %31,5 | +1,1 | 63 | 17.631 | H |
| F_AKBNK1126 | 17 | 70,90 | 69,95 | %29,2 | +3,4 | 2.117 | 746.600 | H |
| F_AKBNK1226 | 48 | 72,95 | 69,95 | %32,6 | -0,0 | 57 | 27.334 | H |
| F_GARAN1126 | 17 | 152,15 | 150,30 | %26,4 | +6,2 | 1.336 | 142.559 | H |
| F_GARAN1226 | 48 | 156,00 | 150,30 | %28,8 | +3,8 | 58 | 10.727 | H |
| F_YKBNK1126 | 17 | 38,23 | 37,78 | %25,6 | +7,0 | 2.056 | 1.273.780 | H |
| F_YKBNK1226 | 48 | 39,35 | 37,78 | %31,6 | +1,0 | 51 | 51.577 | H |
| F_KCHOL1126 | 17 | 210,05 | 207,50 | %26,4 | +6,2 | 1.941 | 184.751 | H |
| F_KCHOL1226 | 48 | 216,25 | 207,50 | %32,1 | +0,5 | 77 | 12.507 | H |
| F_TUPRS1126 | 17 | 363,35 | 359,00 | %26,0 | +6,6 | 2.276 | 115.851 | H |
| F_TUPRS1226 | 48 | 373,90 | 359,00 | %31,6 | +1,0 | 240 | 6.379 | H |
| F_THYAO1126 | 17 | 324,15 | 320,25 | %26,1 | +6,5 | 2.673 | 294.758 | H |
| F_THYAO1226 | 48 | 333,65 | 320,25 | %31,8 | +0,8 | 107 | 11.940 | H |
| F_TRALT1126 | 17 | 38,73 | 38,18 | %30,9 | +1,7 | 964 | 218.757 | H |
| F_TRALT1226 | 48 | 39,74 | 38,18 | %31,1 | +1,5 | 21 | 15.225 | H |
| F_TRMET1126 | 17 | 111,80 | 110,80 | %19,4 | +13,2 | 139 | 27.038 | H |
| F_TRMET1226 | 48 | 114,95 | 110,80 | %28,5 | +4,1 | 7 | 3.254 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✗; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✗; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 381 bps, Δb 20 bps, z 0,37 (std120 dün 53 bps) | 18:08–18:15 F/S oranı **> 1,0431 SAT / < 1,0345 AL** (\|Δb\| > std120 = 41 bps; bugünkü spotla F ≥ 15.485 / ≤ 15.357; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 154 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 2.124 TL = 100 × 373,90 × L %5,7 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 −0,19, σ60 191 bps, β_TA 0,69 | TRMET ≥ 117,66 (AL) / ≤ 106,20 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,0); 7:14 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g +%0,5, z 0,28 (karar σ %1,70 sabit; vekil σ155 %1,49) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 3980,3 / 3847,2) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 30 TRALT1! (β 1,31); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 47,14 (+%1,7), sd250 %3,03 → z 0,55 (sinyal yok) | RYGYO kapanışı ≥ 48,60 (z > +1) / ≤ 45,73 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 25,50 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −1,79, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 92,91 ya da AKBNK ≤ 61,33; z=−1,5: SAHOL ≤ — ya da AKBNK ≥ — | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: LONG (2 g), bugün TUT |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **41 bps** (117 gözlem; geçmiş 155 bülten günü, başlangıç 01.04.2026).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ155 = %1,49: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

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

Hesap günü **12.11.2026** (FRED SP500 son 2026-11-12; CBOE VIX son 2026-11-12). Bu çalışmada işlenen yeni ABD günleri: 2026-11-12.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.592,40 (−%0,4) | — |
| S&P / 200 GHO | 7.337,35 → oran 1,035 | üstünde |
| S&P 10 / 20 / 50 GHO | 7.539 / 7.618 / 7.671 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 27.892 / 28.651 (2026-11-12) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 0,93 / 0,91 | < 1,00 ✓ |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 5. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 5. gün | — |
| FTD | 2026-11-11 NDX +%2,3 (hacim teyidi: None; durum.json 'ftd_hacim_teyit' true/false); 15 seans içinde 10>20: henüz yok (1. seans); FTD günü dibi (YEŞİL şartı, durum.json abd.ftd.gun_dibi elle): girilmedi | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 2 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: TURUNCU** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Per 12.11.2026 kapanışı; SARI tetiği (FTD/10>20) mevcut; SARI kapanışı Cum 13.11.2026; canlı pilot Pzt 16.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-06 KIRMIZI; 11-09 KIRMIZI; 11-10 TURUNCU; 11-11 TURUNCU; 11-12 TURUNCU

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-13 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-12 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-12 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-12 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-12 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-13 | OK | 163/163 seri; bulunamayan: —; 175 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-13 | OK | önceki bülten 2026-11-12; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-13 | OK | 155 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-05 | BAYAT | 8 gün önce |
| durum.json ABD sayaçları | 2026-11-12 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 157 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
