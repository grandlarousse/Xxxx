# Günlük öneri — Pzt 23.11.2026 kapanışı (üretim 23.11.2026 21:21 TSİ)

Sonraki BIST seansı: **Sal 24.11.2026**. Hesap büyüklüğü (durum.json): 1,0 mn TL. Bilgi amaçlıdır; yatırım tavsiyesi değildir. Kurallar: PLAN_BIST.md, PLAN_ABD.md, LEADLAG_UYGULAMA.md, 2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md.

## 0. BUGÜN NE YAPILIR (sonraki seans için, öncelik sırasıyla)

1. **İşlem yok** — BIST rejimi KAPALI, KRİZ yok, K4 nitelikli 0, K1 z −1,68; Koza z3 −0,49; Kural 0 teyitsiz (VİOP kâğıt); ABD KIRMIZI.
2. **Kural 0 teyitsiz** → Sal 24.11.2026 için bütün VİOP sinyalleri ve kayıtları **KÂĞIT** (K1, XU030 bazı, TUPRS, Koza, altın); yalnız spot kollar (burada K4) canlı açılabilir. Aracı kurumun yazılı cevabı gelince makro.json 'kural0_teyit': true.
3. KÂĞIT — ALTIN → TRALT: F_XAUUSD1226 uzlaşma değişimi +%2,7 (z 1,57) eşiği aştı; kural bugünkü uzlaşmada **TRALT1! AL + XU030D1! SAT** girerdi → yalnız kâğıt kaydı (düşük güvenli; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz, planda canlı kanalı yok); kâğıtta 2 gün sonra 17:55'te z'ye bak
4. KÂĞIT — XU030 bazı: |Δb| 131 bps (Δb 131) > std120 40 bps (z 3,26) → kural 18:10–18:15'te **XU030D1! SAT** açıp Sal 24.11.2026 uzlaşmasında kapatırdı; bu akşam için geç (yalnız canlı alarmla) — Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz
5. KÂĞIT kaydı için TradingView alarmları (Sal 24.11.2026 17:45–18:15; Kural 0 yazılı teyidi yok (makro.json kural0_teyit = false; PLAN_BIST §6.1): VİOP kolu canlı açılmaz): XU030D1!/XU030 oranı < 1,0404 AL / > 1,0492 SAT (18:08–18:15; std120 42 bps); TUPRS z (tuprs_alarm.pine, sabah); Koza TRMET ≥ 116,03 / ≤ 104,44 (kâğıt); altın 17:55 TVC:GOLD dünkü 17:55'e göre ±%1,70 (kâğıt); RYGYO ≥ 46,76 / ≤ 44,04 (bar kapanışı; K4 RYSAS filtresi, kâğıt)
6. ABD rejimi **KIRMIZI** (19.11 kapanışı) → yeni canlı giriş yok; en erken SARI kapanışı Pzt 30.11.2026, en erken pilot Sal 01.12.2026 16:45–17:15

**Yarın tetiklenebilecekler** (tetiğe ≤ %3; seviye = Sal 24.11.2026 kapanışı için kesin fiyat; 'aynı gün' satırları kararı o günün uzlaşmasında ister → 17:45–17:55 TradingView alarmı, bkz. ../TRADINGVIEW_ALARMLARI.md; **KÂĞIT** satırları canlı işlem değildir):

| Kol | Enstrüman | Koşul | Tetik | Bugün | Gereken | Tetiklenirse | Zaman |
|---|---|---|---|---|---|---|---|
| K1 | SAHOL | kapanış ≤ (AKBNK sabit) | 77,49 | 78,60 | −%1,4 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| K1 | AKBNK | kapanış ≥ (SAHOL sabit) | 66,24 | 65,30 | +%1,4 | z=−2 → ertesi gün F_SAHOL AL + F_AKBNK SAT — **KÂĞIT** | BIST kapanışı → ertesi gün (kâğıt kaydı) |
| KOZA | TRMET | kapanış ≤ (TRALT, TRENJ yatay) | 104,44 | 106,70 | −%2,1 | aynı gün uzlaşmada TRMET1! SAT + TRALT1! AL — **KÂĞIT** | aynı gün 17:45–17:55 alarm → yalnız kâğıt kaydı |
| ABD | S&P 500 | kapanış > yarının 200 GHO | 7.350,78 | 7.175,83 | +%2,4 | SARI şartı (S&P > 200 GHO) | ABD kapanışı (00:00 TSİ) |

## 1. BIST rejimi ve KRİZ kesicisi (PLAN_BIST §2)

| Kod | Koşul | Değer | Durum |
|---|---|---|---|
| T1 | XU100 > SMA200 | 10.987 vs 13.471 (−%18,4) | 0 |
| T2 | XU100 12 ay > nakit (max TLREF, PPF %45,5) | +%0,1 vs TLREF +%47,4; eşik ~16.180 | 0 |
| T3 | son 5 kapanış > SMA50 | SMA50 12.031 (−%8,7) | 0 |
| M1 | net rezerv 3 hafta artış (makro.json) | 30,8 → 24,3 → 27,4 mlr $ | 0 |
| M2 | aylık TÜFE < %2, 2 ay (makro.json) | 2026-10: 2,58 | 0 |
| M4 | CDS < 230 ve düşüyor (teyitli) | 248 (teyitli H) | 0 |
| M5 | XBANK > SMA200 | 15.782 vs 16.828 (−%6,2) | 0 |

**Durum: KAPALI** (0/7 açık) → K4 r₀ %0,25, K9 (yalnız plan dışı yeni fikir, fikir kartı) risk %0,25; eski lead-lag sinyalleri K9 değil: toplam ≤ %0,5, K4 sonda bütçesinden (§3); ertesi işlem gününden geçerli.

**KRİZ kesicisi:**
| Tetik | Değer | Tetiklendi |
|---|---|---|
| a XU100 5 gün ≤ −%8 | −%7,2 | — |
| b USDTRY 10g yıllık > %35 | +%23,2 | — |
| c CDS > 300 (teyitli) | 248 (teyitli: H) | — |
| d net rezerv 2 hafta ≤ −5 mlr $ ya da < 0 | −6,5 / 3,1 mlr $/hafta | — |
| e F_USDTRY ön ay ima > politika + 5 | %31,7 | — |
| f MSCI danışma | hayır | — |

Makro: makro.json (güncellendi 2026-11-16, 7 gün önce).

## 2. Plan kuralları (bist_sinyal.py mantığı)

### K1 SAHOL↔AKBNK (60 gün ln oran z, |z| ≥ 2, ertesi gün giriş, 20 gün) ve K2 KCHOL/sepet (kâğıt)
| Kol | z | Son \|z\|≥2 kesişimi | Not |
|---|---|---|---|
| K1 | −1,68 | 2026-11-17 | sinyal yok |
| K2 | −0,09 | 2026-11-09 | yalnız yeni kesişimde; varsayılan kâğıt |

K1 tam tetikler (öbür bacak sabit; SAHOL 78,60, AKBNK 65,30): z=+2 → SAHOL ≥ 89,00 ya da AKBNK ≤ 57,67; z=−2 → SAHOL ≤ 77,49 ya da AKBNK ≥ 66,24. Kapı: Kural 0 yazılı teyidi (makro.json kural0_teyit) = H, komisyon = — bps (≤ 5 gerekir) → K1 **kâğıt**.

TradingView oran alarmı (BIST:SAHOL/BIST:AKBNK, 1G, 'Bar kapanışında'): **≥ 1,3630** (z=+2 → F_SAHOL SAT + F_AKBNK AL) ya da **≤ 1,1866** (z=−2 → F_SAHOL AL + F_AKBNK SAT); bugünkü oran 1,2037. Seviyeler her akşam bu rapordan güncellenir; giriş ertesi gün 17:55.

### K4 kırılım (evren: ilk 75 likit; likidite 100 hissede)

Nitelikli: **yok**.

Bekleme listesi (tetiğe ≤ %15, şablonun 5 koşulundan ≥ 4'ü):
| Hisse | Kapanış | Tetik (kapanış >) | Gereken | Şablon | RS | Lik. | Küme | Bilanço 9.11 |
|---|---|---|---|---|---|---|---|---|
| ENERY | 14,28 | 14,86 | +%4,1 | ✓✓✓✓✓ | 98 | 32 | ENERJİ_DAĞITIM | — |
| THYAO | 331,50 | 348,25 | +%5,1 | ✗✓✓✓✓ | 94 | 2 | HAVACILIK | — |
| ENJSA | 112,10 | 127,00 | +%13,3 | ✗✓✓✓✓ | 94 | 44 | ENERJİ_DAĞITIM | — |

### Küme 12 ay RS (K7 filtresi, K4 önceliği; ilk 8)
| Sıra | Küme | Blok | RS 12 ay | rel 3 ay | TL 3 ay | > nakit 3 ay | 126g RS zirvesinden gün | Genişlik 50 |
|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | Ayrıştırıcı | +%21,4 | +%9,2 | −%17,1 | H | 16 | %0,0 |
| 2 | HOLDİNG | Blok1 | +%17,2 | +%12,9 | −%14,3 | H | 29 | %0,0 |
| 3 | ÇELİK | Diğer | +%12,8 | −%6,3 | −%28,9 | H | 61 | %0,0 |
| 4 | PERAKENDE | Diğer | +%10,9 | +%1,0 | −%23,4 | H | 27 | %0,0 |
| 5 | BANKA | Blok1 | +%4,7 | +%28,2 | −%2,7 | H | 9 | %33,3 |
| 6 | GYO | Blok1 | +%1,9 | +%8,7 | −%17,5 | H | 32 | %0,0 |
| 7 | SAĞLIK | Blok3 | −%2,3 | −%13,1 | −%34,1 | H | 51 | %20,0 |
| 8 | KOZA_ALTIN | Ayrıştırıcı | −%4,5 | −%5,9 | −%28,6 | H | 40 | %0,0 |

### VİOP resmî bülten (uzlaşma; bülten 2026-11-23)
| Kontrat | Gün | Uzlaşma | XU030 | İma basit | İma bileşik | TLREF | Eşik (mevduat neti+3) | Nakit-taşıma |
|---|---|---|---|---|---|---|---|---|
| F_XU0301226 | 38 | 14.384 | 13.773 | %42,6 | %51,7 | %35,8 | %35,6 | AÇ (Kural 0 gerekli) |
| F_XU0300227 | 95 | 15.053 | 13.773 | %35,7 | %40,7 | %35,8 | %35,6 | AÇ (Kural 0 gerekli) |
| F_XU0300427 | 158 | 15.619 | 13.773 | %31,0 | %33,7 | %35,8 | %35,6 | kapalı |

F_USDTRY ön ay F_USDTRY1126: uzlaşma 50,87, spot 50,60, 7 gün → ima TL basit **%31,7** (KRİZ e eşiği %41).

Pay vadelileri (§1.5 long kuralı: mevduat neti − ima ≥ 3 puan, açık poz. ≥ 20.000, hacim ≥ 100 mn TL):
| Kontrat | Gün | Uzlaşma | Spot | İma | Mevduat neti − ima | Hacim mn TL | Açık poz. | Kural |
|---|---|---|---|---|---|---|---|---|
| F_SAHOL1126 | 7 | 78,69 | 78,60 | %6,0 | +26,6 | 813 | 572.926 | H |
| F_SAHOL1226 | 38 | 80,98 | 78,60 | %29,1 | +3,5 | 116 | 40.574 | E |
| F_AKBNK1126 | 7 | 65,63 | 65,30 | %26,4 | +6,3 | 3.475 | 610.738 | H |
| F_AKBNK1226 | 38 | 67,57 | 65,30 | %33,4 | -0,8 | 1.330 | 242.833 | H |
| F_GARAN1126 | 7 | 146,40 | 145,00 | %50,3 | -17,7 | 1.529 | 145.972 | H |
| F_GARAN1226 | 38 | 150,00 | 145,00 | %33,1 | -0,5 | 182 | 26.306 | H |
| F_YKBNK1126 | 7 | 36,99 | 36,66 | %46,9 | -14,3 | 3.770 | 1.077.932 | H |
| F_YKBNK1226 | 38 | 38,09 | 36,66 | %37,5 | -4,9 | 1.344 | 393.652 | H |
| F_KCHOL1126 | 7 | 191,85 | 189,70 | %59,1 | -26,5 | 2.323 | 179.612 | H |
| F_KCHOL1226 | 38 | 197,45 | 189,70 | %39,2 | -6,6 | 866 | 69.783 | H |
| F_TUPRS1126 | 7 | 326,20 | 324,00 | %35,4 | -2,8 | 2.472 | 95.173 | H |
| F_TUPRS1226 | 38 | 335,80 | 324,00 | %35,0 | -2,4 | 1.034 | 36.670 | H |
| F_THYAO1126 | 7 | 322,90 | 331,50 | −%135,3 | +167,9 | 5.692 | 259.337 | H |
| F_THYAO1226 | 38 | 332,45 | 331,50 | %2,8 | +29,9 | 2.149 | 65.585 | E |
| F_TRALT1126 | 7 | 35,94 | 35,74 | %29,2 | +3,4 | 967 | 210.586 | H |
| F_TRALT1226 | 38 | 36,81 | 35,74 | %28,8 | +3,8 | 119 | 31.199 | E |
| F_TRMET1126 | 7 | 107,30 | 106,70 | %29,3 | +3,3 | 418 | 38.339 | H |
| F_TRMET1226 | 38 | 110,10 | 106,70 | %30,6 | +2,0 | 59 | 6.627 | H |

**K6 carry kapısı:** KAPALI — 1 net rezerv 2 hf ≥ −2 ve ≥ 20: ✗; 2 yabancı DİBS ≥ −500 mn $: ✓; 3 F_USDTRY ima ≤ politika+5: ✓; 4 USDTRY 10g ≤ %30: ✓; 5 brüt rezerv ≥ 160: ✓; 6 Kural 0 (kural0_teyit): ✗

## 3. Eski lead-lag sinyalleri ve FİLTRE'ler (K9 DEĞİL)

**Bütçe (PLAN_BIST K9 'Eski lead-lag sinyalleri', §3.11):** XU030 bazı, TUPRS ve Koza canlıya geçerse hepsinin **toplam açık riski ≤ %0,5** ve bu bütçe **K4 sondalarından düşülür**; boylar işlem başı ~%0,25 (aynı anda iki sinyal sığsın). Bugün canlı açık eski lead-lag riski %0,00, kalan %0,50. **K9 bu sinyallerin kanalı değildir:** K9 yalnız plan dışı yeni fikirler içindir (fikir kartı 18:45'e kadar, emir ertesi gün kapanış seansında, stop zorunlu, yalnız VİOP-47 hissesi ya da 1x vadeli; risk %0,25). Altın → TRALT ve kredi notu düşük güvenli: **yalnız kâğıt** (altının aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz). SAHOL/AKBNK 1–3G emekli (K1, 20 gün). Kural 0 yazılı teyidi: **H** → bütün VİOP satırları kâğıt.

Karar anı kapanış penceresi (17:50–18:15). Bu rapor 21:05'te çıktığı için **bugün tetiklenen sinyalin kendi giriş anı geçmiştir**; rapor yarının tetik fiyatlarını verir, aynı gün yakalamak için TradingView alarmı gerekir.

| Sinyal | Bugün | Yarın tetik | Tetiklenirse işlem (1 mn TL) | Durum |
|---|---|---|---|---|
| XU030 kapanış bazı sıçraması (KENAR, mikroyapı) | b 438 bps, Δb 131 bps, z 3,26 (std120 dün 40 bps) | 18:08–18:15 F/S oranı **> 1,0492 SAT / < 1,0404 AL** (\|Δb\| > std120 = 42 bps; bugünkü spotla F ≥ 14.451 / ≤ 14.329; spot değişeceği için oranı kullanın) | ucuz kapandıysa XU030D1! AL, pahalıysa SAT; ertesi gün uzlaşmada kapat; 1 mn TL'de en çok 1 kontrat (≈ 144 bin TL nominal); stop yok (1 gün) | TradingView alarmı (canlı 18:10 fiyatı gerekir; bülten kapanış fiyatı yalnız yaklaşık); **KÂĞIT** (Kural 0 teyitsiz) |
| TUPRS ← ABD rafinerileri (VLO, MPC, PSX, PBF − β·SPX; KENAR) | ABD tekil hisse verisi meşru kaynaktan yok | sinyal ABD kapanışında (00:00 TSİ) kesinleşir; 08:30–10:00 sinyal_tuprs.py ya da tuprs_alarm.pine | \|z\|>1: F_TUPRS z yönünde aynı gün 18:00–18:09 limitli, t+2'de kontrol; hedge yok; 1 kontrat F_TUPRS1226 (kontrat başı risk ≈ 1.775 TL = 100 × 335,80 × L %5,3 → %0,2; işlem başı ~%0,25) | TradingView alarmı (tuprs_alarm.pine); **KÂĞIT** (Kural 0 teyitsiz) |
| Koza z3 (TRMET − β·ort(TRALT,TRENJ), 3 gün; KENAR, sönmüş) | z3 −0,49, σ60 187 bps, β_TA 0,70 | TRMET ≥ 116,03 (AL) / ≤ 104,44 (SAT), TRALT ve TRENJ yatayken | z3>+1,5: TRMET1! AL + TRALT1! SAT (1:2,1); 7:15 kontrat (G 122 bin TL, işlem başı ~%0,25); uzlaşmada gir, 2 gün, sinyal sürerse +2 (≤6) | model: pozisyon yok; **KÂĞIT** (NET_LISTE_BIST: IZLE); Kural 0 teyitsiz |
| Altın → TRALT (KENAR, DÜŞÜK; vekil: VİOP F_XAUUSD1226 uzlaşma değişimi) | g +%2,7, z 1,57 (karar σ %1,70 sabit; vekil σ161 %1,52) | yarın 17:55 TVC:GOLD, bugünkü 17:55 fiyatına göre ±%1,70 (VİOP uzlaşmasıyla ≈ 3757,7 / 3632,1) | z>+1: TRALT1! AL + XU030D1! SAT; 1 XU030D : 30 TRALT1! (β 1,29); kâğıt boyu 1 mn TL'de 1 birim; 2 gün | **yalnız KÂĞIT** (düşük güvenli, eski dörde dahil değil; aynı gün kuralı K9'un ertesi gün emriyle uyuşmaz); 17:55 altin.pine alarmı kâğıt kaydı için |
| RYGYO → RYSAS (FİLTRE, kenar adayı; LEADLAG §1.7) | RYGYO 45,38 (−%0,9), sd250 %3,00 → z −0,31 (sinyal yok) | RYGYO kapanışı ≥ 46,76 (z > +1) / ≤ 44,04 (z < −1) (= kapanış × e^(±sd250), sd250 bugün dahil %2,99) | (a) **K4 RYSAS filtresi:** giriş günü RYGYO z < −1 ise o akşam girme (emir 18:01'de: vekil 17:55 canlı değişim ≤ −sd250; K4 ile birlikte test edilmedi). (b) kâğıt kural: z > +1 → RYSAS 18:10–18:15 KFİ'de al, ertesi kapanışta sat | yalnız FİLTRE + kâğıt; **canlı işlem kanalı yok** (RYSAS VİOP-47 değil, K9 emri ertesi güne atar: 1 gün geç giriş −15,8 bps). RYSAS 25,24 |
| SAHOL/AKBNK 1–3G artık z — **kâğıt (emekli)** | z −2,23, β 0,66 | (kâğıt) z=+1,5: SAHOL ≥ 88,79 ya da AKBNK ≤ 54,33; z=−1,5: SAHOL ≤ — ya da AKBNK ≥ — | işlem yok: kural emekli, yerine K1 (20 gün; PLAN_BIST §3.11) | kâğıt model: LONG (8 g), bugün TUT |
| Kredi notu kararı → F_XU030 (KENAR, DÜŞÜK; olay) | karar takvimi dosyada yok (ajans/aracı kurumdan teyit) | — | tepki günü uzlaşmasında kararın tersine, 2 gün | **KÂĞIT**; canlı yalnız K9 (fikir kartı tepki gününden önce, stop zorunlu, risk ≤ %0,25, en çok 1 kontrat) ve Kural 0'dan sonra |

**XU030 eşiği std120(Δb)** (sabit 50 bps değil): gunluk/xu030_baz.csv'deki son 120 bülten günü (devir günü Δb boş ama pencerede yer tutar; araştırma tanımı rolling(120).std, bir gün gecikmeli). Bugün std120 **42 bps** (117 gözlem; geçmiş 161 bülten günü, başlangıç 01.04.2026). Pencerede şok: 16.09.2026 Δb −190 bps (F_XU0301026 −%7,4, spot −%5,6) → Cum 05.03.2027 akşamı pencereden çıkar. Şoklar hariç std ≈ **39 bps**: yeni şok olmazsa eşik şoklar çıktıkça buna iner, seviyeler daralır. Alarm seviyelerini her akşam bu rapordan kurun (sabit 50 de sabit 68 de yanlış olur).

**Altın σ:** karar eşiği sabit %1,70 (rehber σ250, TVC:GOLD 17:55 → 17:55; bu seri izinli kaynakta yok, değiştirmek için altin.pine'ın σ250'si). Vekil (F_XAUUSD uzlaşma değişimi, gunluk/altin_vekil.csv) σ161 = %1,52: yalnız kontrol; 250 güne ulaşınca (≈ Mart 2027) ve fark 0,3 puanı aşarsa altin.pine σ'sıyla karşılaştırın.

Koza kural (kâğıt), son işlemler (spot verisiyle yeniden oynatma): 26.06 +TRMET → 30.06; 24.07 +TRMET → 30.07; 23.09 +TRMET → 25.09

SAHOL/AKBNK 1–3G (kâğıt, emekli) model, son işlemler: 09.10 LONG (z −2,90) → 14.10; 15.10 LONG (z −1,51) → 16.10; 11.11 LONG açık

## 4. Takvim bayrakları (önümüzdeki 14 gün; statik tablo, PLAN_BIST §3.10/§7, PLAN_ABD §7)

| Tarih | Piyasa | Olay | Kural |
|---|---|---|---|
| 25.11 | BIST | Kasım pay vadelisi son devir günü (A10) | Açık Kasım bacakları kapanışta kapatılır ya da Aralık'a devredilir. |
| 25.11 | ABD | GSYH, PCE, Bej Kitap | Yeni giriş yok. |
| 26.11 | BIST | 14:30 rezerv (3. hafta) | M1 olası 1; GEÇİŞ 27.11'den geçerli olabilir. |
| 26.11 | ABD | Şükran Günü: piyasa kapalı | — |
| 27.11 | ABD | Erken kapanış 21:00 TSİ | Yeni giriş yok. |
| 30.11 | BIST | VİOP Kasım vadesi; MSCI yürürlüğü; ay sonu | Vade gününe pozisyon taşınmaz. T2 ve 12 ay küme RS sırası. MSCI'dan çıkarılan hisseler bu kapanışa kadar alınmaz. |
| 03.12 | BIST | 10:00 Kasım TÜFE | makro.json 'tufe_aylik' listesine ekle (M2). |
| 08.12 | ABD | Makro gap-ayarlı ısı kontrolü | Aşan kısım 9.12 MOO. |

Otomatik **değil**: temettü (K3/K3b, A6), bedelsiz (A5), ZPAT (K5) pencereleri ve KAP olayları (TVF/birleşme/tedbir). Her Cuma KAP taraması elle; bilançosunu açıklayan isimleri makro.json 'bilanco_aciklayanlar_9_11' listesine, MSCI'dan çıkarılanları 'msci_cikarilanlar' listesine yazın.

## 5. ABD rejimi (PLAN_ABD §2.2–2.6; durum.json)

Hesap günü **19.11.2026** (FRED SP500 son 2026-11-20; CBOE VIX son 2026-11-20). Bu çalışmada işlenen yeni ABD günleri: yok.

| Girdi | Değer | Koşul |
|---|---|---|
| S&P 500 | 7.175,83 (−%2,0) | — |
| S&P / 200 GHO | 7.348,02 → oran 0,977 | **altında**; yakın bölge (< 1,02) |
| S&P 10 / 20 / 50 GHO | 7.448 / 7.535 / 7.640 | 10 < 20 ✗ |
| Nasdaq-100 10 / 20 GHO | 27.508 / 28.090 (2026-11-19) | 10 < 20 ✗ |
| VIX/VIX3M bugün / önceki | 1,05 / 1,01 | KIRMIZI (a) |
| KIRMIZI (b) S&P 2 kapanış < 200 GHO | evet | — |
| KIRMIZI (c) S5FI<50 ve S5TH<60 | veri yok (TradingView INDEX:S5FI/S5TH, durum.json 'manuel') | elle |
| Ralli denemesi S&P | dip 7.175,83 (2026-11-19); başlamadı | FTD 4. günden itibaren |
| Ralli denemesi NDX | dip 26.517,05 (2026-11-19); başlamadı | — |
| FTD | yok | geçerli FTD ya da S&P 10>20 = SARI tetiği |
| SARI sayacı (3 kapanış kuralı) | 0 | 3 → SARI |
| Pilot freni (elle) | yok | aktifse FTD + S&P > 50 GHO ek şartı |

**Durum: KIRMIZI** → yeni canlı giriş yok, yalnız gölge kayıt; durum ertesi günün 16:45 emir bloğundan geçerli.

En erken: KIRMIZI (a) çıkışı Pzt 23.11.2026 kapanışı; SARI tetiği (FTD/10>20) Çar 25.11.2026; SARI kapanışı Pzt 30.11.2026; canlı pilot Sal 01.12.2026 16:45–17:15 TSİ (takvim yasakları ayrıca: 17.11, 25.11, 27.11, 9.12). YEŞİL için S5FI ≥ 50 elle teyit edilmeli.

- 2026-11-20 ABD kapanışı henüz işlenmedi: Nasdaq-100 verisi yok (sonraki çalışmada işlenir).

Son günler: 11-13 SARI; 11-16 SARI; 11-17 KIRMIZI; 11-18 KIRMIZI; 11-19 KIRMIZI

## 6. Veri tazeliği

| Kaynak | Son tarih | Durum | Not |
|---|---|---|---|
| KAP endeks listesi | — | OK | BIST100 100 hisse (KAP) |
| Borsa İstanbul pay piyasası bülteni | 2026-11-23 | OK | 60/60 gün; 60g medyan TL hacim (likidite sırası) ve yedek kapanış |
| FRED SP500 | 2026-11-20 | OK | FRED ~1 iş günü gecikmeli |
| FRED NASDAQ100 | 2026-11-19 | OK | FRED ~1 iş günü gecikmeli |
| CBOE VIX | 2026-11-20 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| CBOE VIX3M | 2026-11-20 | OK | ABD kapanışı 00:00 TSİ (kış); VIX 00:15 |
| İş Yatırım ChartData (fiyat) | 2026-11-23 | OK | 163/163 seri; bulunamayan: —; 175 istek; eksik geçmiş tekrarı 12 (hâlâ kısa/delikli: ALTNY, BINHO, ENERY, ENTRA, GLRMK, LMKDC, OBAMS, ONRYT, PAHOL, RGYAS …; yeni halka arzlar normal) |
| Borsa İstanbul VİOP bülteni | 2026-11-23 | OK | önceki bülten 2026-11-20; bülten ~20:28–20:49 TSİ'de çıkar |
| XU030 baz geçmişi (gunluk/xu030_baz.csv) | 2026-11-23 | OK | 161 bülten günü (2026-04-01…); std120(Δb) bundan |
| makro.json (elle) | 2026-11-16 | OK | 7 gün önce |
| durum.json ABD sayaçları | 2026-11-19 | OK | PLAN_ABD §2.3–2.4 |

Çalışma süresi 120 sn. Komut: `python3 kod/gunluk_oneri.py --cikti gunluk --veri <önbellek>`. Ayrıntı: ../OTOMASYON.md.
