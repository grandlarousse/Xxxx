# Günlük öneri — Sal 17.11.2026 kapanışı (üretim 17.11.2026 21:21 TSİ)

Sonraki BIST seansı: **Çar 18.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **Kural 0 teyitsiz** → Çar 18.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
2. K4 **ENERY AL (spot)** — Çar 18.11.2026 18:01–18:05 kapanış seansı limitli alış, limit min(15,75; P_son × 1,03); iz-stop (E1) kapanış ≤ girişten beri en yüksek kapanış × 0,85 (bugünkü kapanışla ≈ 12,63); boyut 12 bin TL (stop mesafesi %15 ile; 1,0 mn TL hesap, r₀ %0,25); çıkış iz-stop ya da 120 gün
3. ABD rejimi **SARI** (16.11 kapanışı) → pilot izinli: 16:45–17:15 TSİ bekleyen emir, işlem başı %0,25 risk, yakın bölgede tek pozisyon (PLAN_ABD §2.2)
4. K1: z −2,09 ama modelde açık K1 işlemi var (sinyal 22.10) → yeni giriş yok
5. KÂĞIT kaydı için TradingView alarmları (Çar 18.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz): XU030D1!/XU030 oranı < 1,0333 AL / > 1,0418 SAT (18:08–18:15; std120 41 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 115,32 / ≤ 103,68 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 48,37 / ≤ 45,52 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
6. Takvim Çar 18.11.2026 [ABD]: 22:00 FOMC tutanakları — Giriş emirleri GTD, 21:55 TSİ'de düşer.

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Çar 18.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 82,94 | 83,00 | −%0,1 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 69,10 | 69,05 | +%0,1 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| ABD VIX | VIX/VIX3M | ≥ 1,00 | 1,00 | 1,00 | +%0,5 | KIRMIZI (a) yeniden | VIX kapanışı (00:15 TSİ) |
| ABD ralli | S&P 500 | kapanış < ralli dibi | 7.353,73 | 7.416,59 | −%0,8 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| ABD | S&P 500 | kapanış < yarının 200 GHO | 7.344,55 | 7.416,59 | −%1,0 | 2 kapanış üst üste altında → KIRMIZI (b), sayım yeniden | ABD kapanışı (00:00 TSİ) |
| KOZA | TRMET | kapanış ≥ (TRALT, TRENJ yatay) | 115,32 | 113,50 | +%1,6 | aynı gün uzlaşmada TRMET1! AL + TRALT1! SAT — **KÂĞIT** | aynı gün 17:45–17:55 alarm → yalnız kâğıt kaydı |
| ABD ralli | Nasdaq-100 | kapanış < ralli dibi | 26.629,81 | 27.197,15 | −%2,1 | ralli denemesi sıfırlanır, FTD en erken 4 seans sonra | ABD kapanışı (00:00 TSİ) |
| Rejim M5 | XBANK | kapanış > yarının SMA200 | 16.892,49 | 16.450,47 | +%2,7 | M5=1 | BIST kapanışı → ertesi gün emir |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 11.661 vs 13.522 (−%13,8) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%10,4 vs TLREF +%47,5; eşik ~15.580 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.286 (−%5,1) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 → 27,4 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 16.450 vs 16.905 (−%2,7) | 0 |

**Durum: KAPALI** (0/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | −%0,0 | — |
| b USDTRY 10g yıllık > %35 | +%24,1 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 / 3,1 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %31,9 | — |
| f MSCI danışma | hayır | — |

Makro: makro.json (güncellendi 2026-11-16, 1 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −2,09 | 2026-11-17 | SİNYAL; model işlemi: sinyal 22.10, çıkış 20. gün |
| K2 | 0,83 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 83,00, AKBNK 69,05): z=+2 → SAHOL ≥ 93,84 ya da AKBNK ≤ 61,08; z=−2 → SAHOL ≤ 82,94 ya da AKBNK ≥ 69,10. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3590** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,2012** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2020. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

| Hisse | Kapanış | RS | Lik. | Küme/Blok | Stop | Boyut bin TL | Engel (sonraki seans) |
|---|---|---|---|---|---|---|---|
| ENERY | 14,86 | 99 | 33 | ENERJİ_DAĞITIM/Diğer | %15 | 12 | — |

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENJSA | 118,00 | 127,00 | +%7,6 | ✓✓✓✓✓ | 94 | 42 | ENERJİ_DAĞITIM | — |
| MPARK | 458,75 | 495,00 | +%7,9 | ✗✓✓✓✓ | 90 | 55 | SAĞLIK | — |
| BIMAS | 393,25 | 433,75 | +%10,3 | ✗✓✓✓✓ | 91 | 13 | PERAKENDE | — |
| ALARK | 105,80 | 117,40 | +%11,0 | ✓✗✓✓✓ | 84 | 44 | HOLDİNG | — |
| KCHOL | 202,00 | 225,50 | +%11,6 | ✗✓✓✓✓ | 82 | 8 | HOLDİNG | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%21,3 | +%7,4 | −%13,4 | H | 12 | %0,0 |
| 2 | HOLDİNG | Blok1 | +%16,1 | +%10,0 | −%11,3 | H | 25 | %12,5 |
| 3 | ÇELİK | Diğer | +%10,0 | −%6,3 | −%24,4 | H | 57 | %0,0 |
| 4 | PERAKENDE | Diğer | +%6,6 | +%1,9 | −%17,8 | H | 23 | %0,0 |
| 5 | KOZA_ALTIN | Ayrıştırıcı | +%2,9 | +%0,4 | −%19,1 | H | 36 | %0,0 |
| 6 | BANKA | Blok1 | +%2,8 | +%26,2 | +%1,8 | H | 5 | %55,6 |
| 7 | SAĞLIK | Blok3 | −%1,9 | −%9,6 | −%27,1 | H | 47 | %20,0 |
| 8 | GYO | Blok1 | −%2,3 | +%13,1 | −%8,8 | H | 28 | %14,3 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-17)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 44 | 15.175 | 14.615 | %31,8 | %36,6 | %35,8 | %35,6 | kapalı |
| F_XU0300227 | 101 | 15.857 | 14.615 | %30,7 | %34,3 | %35,8 | %35,6 | kapalı |
| F_XU0300427 | 164 | 16.458 | 14.615 | %28,1 | %30,3 | %35,8 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,91, spot 50,41, 13 gün → ima TL basit **%31,9** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 13 | 84,13 | 83,00 | %38,2 | -5,6 | 943 | 561.754 | H |
| F_SAHOL1226 | 44 | 86,55 | 83,00 | %35,5 | -2,9 | 114 | 28.715 | H |
| F_AKBNK1126 | 13 | 69,86 | 69,05 | %32,9 | -0,3 | 1.806 | 742.996 | H |
| F_AKBNK1226 | 44 | 71,94 | 69,05 | %34,7 | -2,1 | 101 | 31.999 | H |
| F_GARAN1126 | 13 | 150,20 | 148,70 | %28,3 | +4,3 | 1.175 | 141.828 | H |
| F_GARAN1226 | 44 | 154,20 | 148,70 | %30,7 | +1,9 | 87 | 13.899 | H |
| F_YKBNK1126 | 13 | 37,80 | 37,36 | %33,1 | -0,5 | 1.611 | 1.238.670 | H |
| F_YKBNK1226 | 44 | 38,93 | 37,36 | %34,9 | -2,3 | 86 | 63.070 | H |
| F_KCHOL1126 | 13 | 204,15 | 202,00 | %29,9 | +2,7 | 1.733 | 190.759 | H |
| F_KCHOL1226 | 44 | 210,15 | 202,00 | %33,5 | -0,9 | 78 | 13.675 | H |
| F_TUPRS1126 | 13 | 349,90 | 345,25 | %37,8 | -5,2 | 1.699 | 112.471 | H |
| F_TUPRS1226 | 44 | 359,95 | 345,25 | %35,3 | -2,7 | 144 | 7.908 | H |
| F_THYAO1126 | 13 | 326,05 | 322,25 | %33,1 | -0,5 | 2.859 | 289.050 | H |
| F_THYAO1226 | 44 | 335,55 | 322,25 | %34,2 | -1,6 | 202 | 14.276 | H |
| F_TRALT1126 | 13 | 38,15 | 37,84 | %23,0 | +9,6 | 816 | 219.747 | H |
| F_TRALT1226 | 44 | 39,18 | 37,84 | %29,4 | +3,2 | 28 | 22.387 | H |
| F_TRMET1126 | 13 | 115,05 | 113,50 | %38,3 | -5,7 | 194 | 37.266 | H |
| F_TRMET1226 | 44 | 117,50 | 113,50 | %29,2 | +3,4 | 5 | 4.166 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✓; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✓; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 369 bps, Δb 8 bps, z 0,19 (std120 dün 41 bps) | 18:08–18:15 F/S oranı **> 1,0418 SAT / < 1,0333 AL** (\|Δb\| > std120 = 41 bps; bugünkü spotla F ≥ 15.226 / ≤ 15.102; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 152 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 2.038 TL = 100 × 359,95 × L %5,7 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 1,09, σ60 188 bps, β_TA 0,70 | TRMET ≥ 115,32 (AL) / ≤ 103,68 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,1); 6:13 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g −%0,5, z −0,29 (karar σ %1,70 sabit; vekil σ157 %1,49) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 3950,0 / 3817,9) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 30 TRALT1! (β 1,30); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 46,92 (+%0,0), sd250 %3,03 → z 0,01 (sinyal yok) | RYGYO kapanışı ≥ 48,37 (z > +1) / ≤ 45,52 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %3,03) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 24,48 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −2,24, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 92,03 ya da AKBNK ≤ 59,03; z=−1,5: SAHOL ≤ — ya da AKBNK ≥ — | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: LONG (4 g), bugün TUT |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **41 bps** (117 gözlem; geçmiş 157 bülten günü, başlangıç 01.04.2026). Pencerede şok: 16.09.2026 Δb −190 bps (F_XU0301026 −%7,4, spot −%5,6) → Cum 05.03.2027 akşamı pencereden çıkar. Şoklar hariç std ≈ **38 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ157 = %1,49: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10; 11.11 LONG açık

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
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

Hesap günü **16.11.2026** (FRED SP500 son 2026-11-16; CBOE VIX son 2026-11-16). Bu çalışmada işlenen yeni ABD günleri: 2026-11-16.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.416,59 (−%1,9) | — |
| S&P / 200 GHO | 7.342,71 → oran 1,010 | üstünde; yakın bölge (< 1,02) |
| S&P 10 / 20 / 50 GHO | 7.525 / 7.600 / 7.661 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 27.769 / 28.472 (2026-11-16) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 1,00 / 0,94 | < 1,00 ✓ |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | hayır | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.353,73 (2026-11-05); 1. gün 2026-11-06, bugün 7. gün | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.629,81 (2026-11-05); 1. gün 2026-11-06, bugün 7. gün | — |
| FTD | 2026-11-11 NDX +%2,3 (hacim teyidi: None; durum.json 'ftd_hacim_teyit' true/false); 15 seans içinde 10>20: henüz yok (3. seans); FTD günü dibi (YEŞİL şartı, durum.json abd.ftd.gun_dibi elle): girilmedi | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 4 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: SARI** → günde ≤ 2 giriş, ≤ 4 açık, yakın bölgede 1 pozisyon / ısı ≤ %0,5; AI dışı izinli kümeler; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Pzt 16.11.2026 kapanışı; SARI tetiği (FTD/10>20) mevcut; SARI kapanışı Pzt 16.11.2026; canlı pilot Sal 17.11.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

Son günler: 11-10 TURUNCU; 11-11 TURUNCU; 11-12 TURUNCU; 11-13 SARI; 11-16 SARI

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-17 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-16 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-16 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-16 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-16 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-17 | OK | 163/163 seri; bulunamayan: —; 175 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-17 | OK | önceki bülten 2026-11-16; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-17 | OK | 157 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-16 | OK | 1 gün önce |
| durum.json ABD sayaçları | 2026-11-16 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 119 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
