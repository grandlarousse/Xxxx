# Günlük öneri — Cum 27.11.2026 kapanışı (üretim 27.11.2026 21:22 TSİ)

Sonraki BIST seansı: **Pzt 30.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

> **Uyarı:** makro.json 11 gündür güncellenmedi (son 2026-11-16) → M1/M2/KRİZ (c, d)/K6 BAYAT olabilir.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −0,15; Koza z3 −1,10; Kural 0 teyitsiz (VİOP kâğıt); ABD KIRMIZI.
2. **Kural 0 teyitsiz** → Pzt 30.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. KÂĞIT kaydı için TradingView alarmları (Pzt 30.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz): XU030D1!/XU030 oranı < 1,0269 AL / > 1,0358 SAT (18:08–18:15; std120 43 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 109,98 / ≤ 99,11 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 43,19 / ≤ 40,65 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
4. Takvim Pzt 30.11.2026 [BIST]: VİOP Kasım vadesi; MSCI yürürlüğü; ay sonu — Vade gününe pozisyon taşınmaz. T2 ve 12 ay küme RS sırası. MSCI'dan çıkarılan hisseler bu kapanışa kadar alınmaz.
5. ABD rejimi **KIRMIZI** (25.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Çar 02.12.2026, en erken pilot Per 03.12.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Pzt 30.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| ABD FTD | S&P 500 | kapanış ≥ +%1,5 (ralli ≥4. gün) | 7.290,52 | 7.182,78 | +%1,5 | FTD adayı (hacim teyidi elle) → SARI tetiği | ABD kapanışı (00:00 TSİ) |
| ABD FTD | Nasdaq-100 | kapanış ≥ +%1,5 (ralli ≥4. gün) | 26.437,60 | 26.046,90 | +%1,5 | FTD adayı (hacim teyidi elle) → SARI tetiği | ABD kapanışı (00:00 TSİ) |
| KOZA | TRMET | kapanış ≤ (TRALT, TRENJ yatay) | 99,11 | 101,40 | −%2,3 | aynı gün uzlaşmada TRMET1! SAT + TRALT1! AL — **KÂĞIT** | aynı gün 17:45–17:55 alarm → yalnız kâğıt kaydı |
| ABD | S&P 500 | kapanış > yarının 200 GHO | 7.354,56 | 7.182,78 | +%2,4 | SARI şartı (S&P > 200 GHO) | ABD kapanışı (00:00 TSİ) |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 10.977 vs 13.414 (−%18,2) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%0,6 vs TLREF +%47,0; eşik ~16.047 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 11.805 (−%7,0) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 → 27,4 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 14.705 vs 16.746 (−%12,2) | 0 |

**Durum: KAPALI** (0/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | −%1,4 | — |
| b USDTRY 10g yıllık > %35 | +%22,7 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 / 3,1 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %31,8 | — |
| f MSCI danışma | hayır | — |

Makro: makro.json (güncellendi 2026-11-16, 11 gün önce → BAYAT).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −0,15 | 2026-11-17 | sinyal yok |
| K2 | −0,04 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 75,60, AKBNK 59,95): z=+2 → SAHOL ≥ 81,64 ya da AKBNK ≤ 55,51; z=−2 → SAHOL ≤ 70,67 ya da AKBNK ≥ 64,13. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3619** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,1789** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2611. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,36 | 14,86 | +%3,5 | ✓✓✓✓✓ | 98 | 32 | ENERJİ_DAĞITIM | — |
| THYAO | 314,00 | 348,25 | +%10,9 | ✗✓✓✓✓ | 90 | 2 | HAVACILIK | — |
| ALARK | 105,20 | 117,40 | +%11,6 | ✓✗✓✓✓ | 88 | 44 | HOLDİNG | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%24,2 | +%4,8 | −%19,7 | H | 20 | %0,0 |
| 2 | ÇELİK | Diğer | +%19,4 | −%3,4 | −%26,0 | H | 65 | %42,9 |
| 3 | HOLDİNG | Blok1 | +%15,8 | +%9,6 | −%16,1 | H | 33 | %12,5 |
| 4 | PERAKENDE | Diğer | +%6,5 | −%1,9 | −%24,9 | H | 31 | %0,0 |
| 5 | KOZA_ALTIN | Ayrıştırıcı | −%2,4 | −%10,9 | −%31,8 | H | 44 | %0,0 |
| 6 | SAĞLIK | Blok3 | −%2,5 | −%18,1 | −%37,2 | H | 55 | %20,0 |
| 7 | GYO | Blok1 | −%3,6 | +%1,7 | −%22,1 | H | 36 | %0,0 |
| 8 | BANKA | Blok1 | −%5,2 | +%16,4 | −%10,9 | H | 13 | %11,1 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-27)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 34 | 14.192 | 13.764 | %33,4 | %38,9 | %39,0 | %35,6 | kapalı |
| F_XU0300227 | 91 | 14.879 | 13.764 | %32,5 | %36,7 | %39,0 | %35,6 | kapalı |
| F_XU0300427 | 154 | 15.490 | 13.764 | %29,7 | %32,3 | %39,0 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1226: uzlaşma 52,09, spot 50,78, 34 gün → ima TL basit **%31,8** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1226 | 34 | 78,19 | 75,60 | %36,8 | -4,2 | 1.653 | 364.115 | H |
| F_SAHOL0127 | 63 | 80,09 | 75,60 | %34,4 | -1,8 | 3 | 1.391 | H |
| F_AKBNK1226 | 34 | 61,85 | 59,95 | %34,0 | -1,4 | 3.160 | 850.524 | H |
| F_AKBNK0127 | 63 | 63,39 | 59,95 | %33,2 | -0,6 | 24 | 7.668 | H |
| F_GARAN1226 | 34 | 142,50 | 138,10 | %34,2 | -1,6 | 1.274 | 124.095 | H |
| F_GARAN0127 | 63 | 145,80 | 138,10 | %32,3 | +0,3 | 8 | 560 | H |
| F_YKBNK1226 | 34 | 34,04 | 32,92 | %36,5 | -3,9 | 2.890 | 1.296.801 | H |
| F_YKBNK0127 | 63 | 34,90 | 32,92 | %34,8 | -2,2 | 29 | 9.461 | H |
| F_KCHOL1226 | 34 | 195,70 | 189,40 | %35,7 | -3,1 | 1.118 | 148.169 | H |
| F_KCHOL0127 | 63 | 201,10 | 189,40 | %35,8 | -3,2 | 3 | 824 | H |
| F_TUPRS1226 | 34 | 341,15 | 330,00 | %36,3 | -3,7 | 1.493 | 73.421 | H |
| F_TUPRS0127 | 63 | 350,55 | 330,00 | %36,1 | -3,5 | 14 | 557 | H |
| F_THYAO1226 | 34 | 324,20 | 314,00 | %34,9 | -2,3 | 2.904 | 244.635 | H |
| F_THYAO0127 | 63 | 329,50 | 314,00 | %28,6 | +4,0 | 12 | 796 | H |
| F_TRALT1226 | 34 | 36,67 | 35,54 | %34,1 | -1,5 | 783 | 169.121 | H |
| F_TRALT0127 | 63 | 37,36 | 35,54 | %29,7 | +2,9 | 4 | 1.540 | H |
| F_TRMET1226 | 34 | 104,55 | 101,40 | %33,3 | -0,7 | 206 | 25.522 | H |
| F_TRMET0127 | 63 | 107,00 | 101,40 | %32,0 | +0,6 | 1 | 257 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✓; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✓; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 308 bps, Δb 4 bps, z 0,10 (std120 dün 43 bps) | 18:08–18:15 F/S oranı **> 1,0358 SAT / < 1,0269 AL** (\|Δb\| > std120 = 43 bps; bugünkü spotla F ≥ 14.257 / ≤ 14.134; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 142 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 1.809 TL = 100 × 341,15 × L %5,3 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 −1,10, σ60 185 bps, β_TA 0,71 | TRMET ≥ 109,98 (AL) / ≤ 99,11 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,0); 7:14 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g +%1,4, z 0,84 (karar σ %1,70 sabit; vekil σ162 %1,52) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 3723,3 / 3598,8) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 29 TRALT1! (β 1,33); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 41,90 (+%1,0), sd250 %3,01 → z 0,32 (sinyal yok) | RYGYO kapanışı ≥ 43,19 (z > +1) / ≤ 40,65 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,01) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 24,24 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −1,30, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 83,79 ya da AKBNK ≤ 51,31; z=−1,5: SAHOL ≤ 74,89 ya da AKBNK ≥ 60,81 | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: yok, bugün KAPAT |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **43 bps** (117 gözlem; geçmiş 165 bülten günü, başlangıç 01.04.2026). Pencerede şok: 16.09.2026 Δb −190 bps (F_XU0301026 −%7,4, spot −%5,6) → Cum 05.03.2027 akşamı pencereden çıkar. Şoklar hariç std ≈ **40 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur). Not: 3 eksik gün bültenden dolduruldu.

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ162 = %1,52: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10; 11.11 LONG (z −1,88) → 27.11

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
| 30.11 | BIST | VİOP Kasım vadesi; MSCI yürürlüğü; ay sonu | Vade gününe pozisyon taşınmaz. T2 ve 12 ay küme RS sırası. MSCI'dan çıkarılan hisseler bu kapanışa kadar alınmaz. |
| 03.12 | BIST | 10:00 Kasım TÜFE | makro.json 'tufe_aylik' listesine ekle (M2). |
| 08.12 | ABD | Makro gap-ayarlı ısı kontrolü | Aşan kısım 9.12 MOO. |
| 09.12 | ABD | FOMC 22:00 | Yeni giriş yok. |
| 10.12 | BIST | TCMB PPK (anket %35) | Sürprizsiz indirimde (±25 bp) 11.12'den ~15.03.2027'ye kadar BANKA kümesinde yeni K4/K9 yarım boy, en çok 1 (A7). makro.json 'ppk_10_12_surprizsiz_indirim'. |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **25.11.2026** (FRED SP500 son 2026-11-25; CBOE VIX son 2026-11-26). Bu çalışmada işlenen yeni ABD günleri: 2026-11-20, 2026-11-23, 2026-11-24, 2026-11-25.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.182,78 (−%0,3) | — |
| S&P / 200 GHO | 7.352,49 → oran 0,977 | **altında**; yakın bölge (< 1,02) |
| S&P 10 / 20 / 50 GHO | 7.294 / 7.423 / 7.603 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 26.810 / 27.407 (2026-11-25) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 1,08 / 1,03 | KIRMIZI (a) |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | evet | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 6.910,39 (2026-11-20); 1. gün 2026-11-23, bugün 3. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 25.028,98 (2026-11-20); 1. gün 2026-11-23, bugün 3. gün | — |
| FTD | yok | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 0 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: KIRMIZI** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Pzt 30.11.2026 kapanışı; SARI tetiği (FTD/10>20) Cum 27.11.2026; SARI kapanışı Çar 02.12.2026; canlı pilot Per 03.12.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-19 KIRMIZI; 11-20 KIRMIZI; 11-23 KIRMIZI; 11-24 KIRMIZI; 11-25 KIRMIZI

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-27 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-25 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-25 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-26 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-25 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-27 | OK | 163/163 seri; bulunamayan: —; 245 istek; eksik geçmiş tekrarı 17 (hâlâ kısa/delikli: XU030, ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-27 | OK | önceki bülten 2026-11-26; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-27 | OK | 165 bülten günü (2026-04-01…); std120(Δb) bundan; 3 eksik gün bültenden dolduruldu |
| makro.json (elle) | 2026-11-16 | BAYAT | 11 gün önce |
| durum.json ABD sayaçları | 2026-11-25 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 181 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
