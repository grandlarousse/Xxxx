# v_C4C5_a — Bağımsız doğrulama: Çin/HK sürücüleri → TRALT / KRDMD (zamanlama denetimi)
Kod: `out/code_v_C4C5_a/` (vlib.py kendi hizalama/temizlik; ll.py import edilmedi). s01 yeniden üretim, s02–s03 HK zamanlaması, s04 SHFE gece/gündüz ayrıştırması (Sina 60 dk, `dl_v_C4C5a/sina60/`), s05 yıllar+maliyet+blok permütasyon, s06–s07 haftalık altın, s08 kontrollü regresyon, s09 h1 backtest. Loglar: `log_s0*.txt`, tablolar `s0*.csv`.
Yeni veri: Yahoo h1/m5 1787.HK, 2899.HK, 600547.SS, 601899.SS (data/h1, data/m5). HK h1 2024-Q3 öncesi günlük kapanışla tutarsız (sd 100+ bps) → h1 sinyalleri 2024-09+.

## Karar: DÜZELT (üç iddia da sayısal olarak birebir üretildi; ama zamanlama/yorum hatalı)

### (a) 1787.HK → TRALT gün-içi — YÜKSEK → **DÜŞÜK**
- Yeniden üretim birebir: t=4,15, OOS Sharpe 0,55, net 10,7 bps; 600547.SS t=3,34; 2899.HK t=3,84.
- İleriye bakma DOĞRULANDI: HK kapanışı 08:00 UTC (müzayede 08:10); BIST sürekli işlem 07:00 UTC → 70 dk örtüşme. Örtüşen kısım (HK 06:30→kapanış) TRALT gün-içiyle r=0,10 (t=2,3) ama eşzamanlı altın (GC 07–15 UTC) kontrol edilince t=0,74 → öncülük değil, eşzamanlı altın hareketi.
- Açılıştan ÖNCE bilinen varyantlar:
  - HK açılışı (01:30 UTC, 2018-10+, n=1911): r=0,039, t=1,85, net10 −4,4 bps (IS −3,1 / OOS −5,0), 5/9 yıl pozitif.
  - Bayat D_{t-1}: t=1,94, net −2,3, IS Sharpe −1,10.
  - HK öğlen arası 04:00 UTC (h1, 2024-09+, n=512): r=0,094, t=2,00, net10 +17,6 bps, Sharpe 0,95, BT t=1,30.
  - HK 06:30 UTC (n=512): r=0,111, t=2,39; net10 +10,0 bps, Sharpe 0,54, BT t=0,71; 15 bps'te +5,0. GC gece getirisi ve kendi gap/gecikme kontrolünden sonra t=2,2–2,9 kalıyor. Örneklem kısa (~2 yıl, altın boğa rejimi).
  - 600547.SS (aynı şirketin A payı, 07:00 UTC kapanış ≈ BIST açılış müzayedesi; birkaç dakikalık iyimserlik var): 2014+, t=3,33; net10 IS +10,1 (Sh 0,60), OOS +6,6 (Sh 0,35); 15 bps'te OOS Sh 0,08. Alt dönemlerde t: 2018–20 4,63, 2021–23 1,29, 2024–26 1,98. 2024-09+ örnekleminde t=1,65, net ≈0.
  - 1787.HK'nin 600547.SS'nin ötesindeki katkısı (dik bileşen): net −2,7 bps. Yani HK'ye özgü ek bilgi işlenebilir değil.
  - TRALT h1 (yalnızca 2025-11-24+, n≈218): HK kapanışından sonra 08:30'da giriş → kapanış: r=0,10, t=1,42, net +2,1 bps.
- Gece COMEX altını (15:00 UTC t' → 06:00/07:00 UTC t) TRALT gün-içini tahmin ETMİYOR (r=0,03, t=0,46): TradingView'da işlenebilir bir vekil yok. TRALT gece altınını açılış gap'inde fiyatlıyor (gap ile korelasyon 0,48).
- Etkinin büyük kısmı 2018–2020'den geliyor (IS Sh 1,40). Yıllık korelasyon: 2021 −0,04, 2022 0,005, 2025 0,046.

### (b) SHFE HRC → KRDMD gün-içi — ORTA → **DÜŞÜK**
- Yeniden üretim birebir: t=3,33, OOS Sh 0,65, net 11,7 bps. **Ancak IS (2018-12…2020) Sharpe −0,61, net −10,5 bps.** Tüm dönem net +5,8, BT t=0,90. Yıllara göre net10: 2019 −5,6 · 2020 −19,2 · 2021 +23,5 · 2022 +19,1 · 2023 +16,6 · 2024 +1,1 · 2025 +2,7 · 2026 +6,1.
- Sina günlük bar (60 dk ile doğrulandı): t barı = gece seansı (21:00–23:00 Pekin = 13:00–15:00 UTC t-1) + gündüz seansı (01:00–07:00 UTC t). Bar açılışı gece açılışı, kapanışı 15:00 Pekin.
- 60 dk ayrıştırması (2023-08+, n≈713–734): FULL t=1,26; GECE (BIST t-1'in son 2 saatiyle eşzamanlı) t=1,56; GÜNDÜZ (15:00 UTC t-1 → 07:00 UTC t, saf açılış öncesi Çin bilgisi) **t=0,12**; 06:15 UTC'ye kadarki kısım t=1,39 (net +1,9); son 45 dk t=−0,27.
- Tüm dönem (günlük): GAPD (07–13 UTC t-1) t=2,37, OCD t=2,43; 2024–26'da GAPD t=−1,41.
- KRDMD h1 (2023-11-30+): SHFE kapanışından sonra 07:30'da giriş → kapanış: r=0,017, t=0,47, net −1,7 bps. Görülen etki ilk 30 dakikada (açılış→07:30, r=0,06, t=1,3); sinyal 07:00'de geldiği için bu kısım 8–15 bps maliyetle yakalanamıyor.
- Kontroller (kendi gecikmesi, XU100 gecikmesi, gap) etkiyi değiştirmiyor (t=3,24). EREGL'de aynı sinyal: t=2,3, net −1,5 bps.

### (c) TRALT: SHFE altını COMEX'ten iyi mi? — **Hayır, pratikte eşdeğer**
- Rapordaki rakamlar yanlış sütundan okunmuş. bist_pairs.csv'de SHFE AU haftalık r=0,286, kısmi 0,317 ("0,29" aslında gap korelasyonu 0,290). GC haftalık r=0,268, kısmi 0,242 ("0,11" aslında GC lag-1 gap korelasyonu 0,113). Üstelik iki seri farklı örneklemlerde ölçülmüş.
- Ortak örneklem (2018-11 → 2026-10, 415 hafta, Cuma çapası): AU kısmi 0,317 vs GC 0,220. Fark +0,097, bootstrap %95 GA [0,026; 0,186]. AU_USD 0,307, yani etki CNY'den gelmiyor.
- **Bu fark Cuma çapasına özgü bir artefakt.** Diğer çapalarda kısmi korelasyon (AU / GC): Pzt 0,218/0,233 · Sal 0,283/0,287 · Çar 0,319/0,300 · Per 0,372/0,335. 5 günlük bloklarda AU 0,28–0,36, GC 0,24–0,33 (ortalama fark ≈0,03). Günlük: GC 0,209 > AU 0,163. 2 günlük: 0,249 vs 0,238.
- 2024-06+ döneminde GC 15:00 UTC'de (BIST kapanışına hizalı) örneklendiğinde GC ≥ AU (günlük 0,273 vs 0,180; Çar 0,431 vs 0,371).
- Haftalık öncülük yok: AU_{w-1} t=−0,82, GC_{w-1} t=0,93.
- Sonuç: TRALT–altın senkron bağı gerçek (haftalık kısmi ~0,2–0,37, 7/8 yıl pozitif; IS 0,52, OOS 0,28). Ancak "SHFE > COMEX" iddiası desteklenmiyor. COMEX:GC1! / TVC:GOLD yeterli vekil.

## Sınırlamalar
- HK h1 verisi yalnızca 2024-09'dan güvenilir; TRALT h1 yalnızca 2025-11'den. Uzun dönemde temiz HK testi sadece açılış fiyatıyla yapılabildi.
- Açılış müzayedesinden dolum iyimser bir varsayım. VİOP pay vadelisi 09:30 TSİ'de (06:30 UTC) açılıyor; TRALT/KRDMD vadelilerinin o saatteki likiditesi test edilmedi.
- Yaklaşık 150 varyant/hedef kombinasyonu tanı amaçlı çalıştırıldı; FDR uygulanmadı. Tek tek t≈2 sonuçlar bu sayıya göre zayıf kanıttır.
