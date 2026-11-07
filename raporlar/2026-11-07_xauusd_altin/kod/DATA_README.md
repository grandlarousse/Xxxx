# Ortak veri ve kurallar — VİOP Ons Altın (XAUUSD) lead-lag çalışması

Kök dizin: `S=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad`

## Zaman çizelgesi (kritik)
- Türkiye kalıcı UTC+3. VİOP kıymetli maden normal seansı 09:30–18:15 TSİ (06:30–15:15 UTC), akşam seansı 19:00–23:00 TSİ (16:00–20:00 UTC; ons altında 18.09.2020'den beri). **Günlük uzlaşma fiyatı = seans sonundan önceki son 10 dakikanın miktar ağırlıklı ortalaması ≈ 15:05–15:15 UTC VWAP (İşbank VİOP eğitim dokümanı 2024, BIST duyurusu 30572). Vade sonu uzlaşma = son işlem günü LBMA Gold Price PM (BIST duyurusu 11834).** Bu, dakikalık spot verisiyle ölçüldü: uzlaşma–spot farkının sapması 15:10 UTC'de minimum (MAD 3,7 bps; 14:00'te 12, 17:00'de 8 bps). Bülten "KAPANIŞ FİYATI" (son işlem) ≈ 15:15–15:20 UTC.
- 18.09.2020'den beri VİOP gün t'nin işlemleri önceki akşam 19:00 TSİ (16:00 UTC) akşam seansıyla başlar (akşam seansının baz fiyatı normal seans uzlaşmasıdır), gün t 18:15 TSİ'de biter. Bültendeki AÇILIŞ FİYATI büyük olasılıkla akşam seansının ilk işlemidir; ACILIS SEANSI FIYATI ayrı sütun.
- **Karar anı (cutoff) = gün t 15:00 UTC.** Sinyal yalnızca bu andan ÖNCE yayımlanmış/kapanmış bilgiyle kurulabilir. Giriş = gün t uzlaşması. Çıkış = t+h uzlaşması.
- Hedef: `fwd{h}` (h=1,3,5,10) = `v_ret`'in t+1..t+h toplamı. `v_ret` = aktif kontratın aynı kontrat içindeki log(UZLAŞMA/ÖNCEKİ UZLAŞMA). Aktif kontrat = önceki gün açık pozisyonu en büyük vade (roll ileriye bakmasız). Roll günleri ayrıca kontrol edilmeli (`v_code` değişimi).
- Kapanış saatleri (yerel → UTC; yaz saati otomatik): ABD hisse/ETF 16:00 ET (20:00/21:00 UTC); COMEX/NYMEX/CBOT vadeli Yahoo kapanışı 17:00 ET varsayıldı; DXY (ICE) 17:00 ET; ^TNX vb. 16:00 ET; VIX/GVZ/OVX 16:15 ET; Nikkei 15:30 JST (06:30 UTC; Kasım 2024 öncesi 15:00), KOSPI 06:30 UTC, Şanghay 07:00 UTC, Hong Kong 08:10 UTC, Hindistan NSE 10:00 UTC, ASX ~05–06 UTC; DAX/STOXX 17:30 CET ve FTSE 16:30 Londra (cutoff'tan SONRA → ancak t-1); BIST 18:10 TSİ (15:10 UTC → cutoff'tan sonra, ancak t-1); Yahoo `=X` kurları ve kripto bar sonu 24:00 UTC (+1 saat pay) → ancak t-1. **Yahoo `=X` kurlarının günlük kapanışı güvenilmez/kaymış olabilir (önceki çalışmada bir gün kaymış bulundu); kur için Dukascopy `dk_*` ya da VİOP `vo_usdtry_*` kullan.**

## Dosyalar (`$S/panel/`)
- `panel_viop.parquet` — gün endeksi = VİOP işlem günleri 2017-03-06 → 2026-11-06. Ana çalışma tablosu.
- `panel_spot.parquet` — gün endeksi = Dukascopy XAUUSD'nin 15:00 UTC fiyatı olan iş günleri 2010-01-04 → 2026-11-06. Hedef `s_ret` (15:00→15:00 UTC spot), `sfwd{h}`. Uzun örneklem sağlamlık testi ve 2017 öncesi için. VİOP sütunları (`v_ret` vb.) 2017 sonrası eklenmiş.
- `viop_long.parquet` — bültenin bütün hisse dışı vadeli satırları (her kontrat, her gün): settle, prev_settle, open, high, low, close, vwap, value (TL), volume (kontrat), trades, oi, os_* (açılış seansı).
- `viop_<ROOT>.parquet` — sürekli seriler: XAUUSD, XAUTRYM (gram altın TL), XAGUSD (2021+), USDTRY, XU030, EURUSD.
- `duka/<SYM>.parquet` — Dukascopy BID saatlik mumlar (index = bar başlangıcı UTC; **fiyat anı = index + 1 saat**). XAUUSD 2008–2026 (2009–2015 doluluk kontrol et), diğerleri 2016+ (DOLLARIDXUSD 2017-12+, USTBONDTRUSD 2019+). Ekim–Kasım 2026 XAUUSD/USDJPY dakikadan saatliğe yamalı (panel kurucuda).
- `duka_min_XAUUSD.parquet` — örnek günlerde dakikalık XAUUSD (kalibrasyon için).
- `yahoo/<TICKER>.parquet` — günlük OHLC (+adjclose), `_meta.json` borsa/zaman dilimi. `yahoo_h/` — son 730 gün saatlik.

## Panel sütunları (gün t satırında, hepsi karar anı t'de bilinen değerler)
- `v_*`: VİOP aktif kontrat (code, expiry, settle, prev_settle, ret, close, open, high, low, vwap, volume, trades, oi, os_price, tot_volume, tot_oi, next_code, next_settle, dte, value). **Not: `v_settle`, `v_ret`, `v_close` gün t'nin 15:10 UTC değerleri → giriş fiyatı; sinyalde kullanılırsa "kapanış anında hesaplanan sinyal" olur (15:10'da bilinir, uzlaşmayla aynı anda). Daha temiz: sinyalde t-1'e kadar `v_*` kullan ya da 15:00 UTC spot `xau_p15` ile hesapla.**
- `vo_<xautry|xag|usdtry|xu030|eurusd>_<settle|ret|expiry|code|volume|oi|dte>`: diğer VİOP sürekli seriler (aynı 15:10 UTC damgası, aynı uyarı).
- `tr_prem_matched`: log(XAUTRYM) − log(XAUUSD × USDTRY / 31,1035), aynı vade ayındaki kontratlarla (yurt içi gram altın sentetik primi; 15:10 UTC).
- `xau_pHH` (HH=00,07,12,13,14,15,16,20): spot XAUUSD gün t HH:00 UTC fiyatı. `xau_p15_prev`, `xau_p20_prev`: bir önceki endeks gününün 15:00 ve 20:00 UTC fiyatı. **16 ve 20 cutoff'tan sonra → gün t sinyalinde kullanma (yalnız t-1).**
- `dk_<SYM>_p15`, `dk_<SYM>_p07`: Dukascopy çapraz varlıkların gün t 15:00 ve 07:00 UTC fiyatı (XAGUSD, XPTUSD, DOLLARIDXUSD, USTBONDTRUSD [ABD T-bond CFD fiyatı; faiz ↑ → fiyat ↓], USA500IDXUSD, USDJPY, EURUSD, USDCNH, USDTRY, BRENTCMDUSD, COPPERCMDUSD, VOLIDXUSD [VIX CFD], BTCUSD). İndirme bazılarında eksik olabilir — `notna()` kontrol et.
- `y_<TICKER>`: Yahoo son bilinen kapanış (hisse/ETF'de temettü düzeltmeli adjclose), `y_<TICKER>_avail`: o kapanışın UTC zamanı. Değişim için `np.log(y).diff()` — bu, karar anı t-1'den t'ye bilinen kapanıştaki değişimdir (ABD varlıklarında ≈ t-2 ABD kapanışı → t-1 ABD kapanışı). Aynı kapanış tekrar ederse fark 0'dır.
- `ust_<real5|real10|nom3m|nom2|nom5|nom10|nom30|be5|be10>`: ABD Hazinesi par getirileri (yüzde), gün D değeri D 22:00 UTC'de mevcut sayıldı → gün t'de son değer t-1. Fark için `.diff()`.
- `cot_<gold|silver>_<mm_net|mm_net_oi|oi|swap_net|pm_net|mm_long|mm_short|reportdate>`: CFTC disaggregated, Salı pozisyonu, Cuma 21:00 UTC mevcut varsayıldı (Cuma VİOP gününde o haftanın raporu yok, Pazartesi var). **Uyarı: ABD hükümeti kapanmalarında (22.12.2018–25.01.2019, sonrası Mart 2019'a kadar telafi; 01.10.2025–12.11.2025 ve telafisi) raporlar geç yayımlandı — bu dönemlerde varsayım ileriye bakar; bu dönemleri dışlayarak da test et.**
- `shfe_<AU0|AG0>_c`, `shfe_*_date`: SHFE altın/gümüş sürekli vadeli (Sina) gündüz kapanışı (CNY/gram; 15:00 CST = 07:00 UTC → gün t'de aynı gün kullanılabilir). Şanghay primi için `dk_USDCNH_p07` ve `xau_p07` ile: prem = log(AU0 × 31,1035 / USDCNH) − log(xau_p07) (vadeli carry içerir; seviyeden çok değişim/sapma anlamlı).
- `gpr_*`: Caldara–Iacoviello günlük jeopolitik risk; D değeri D+1 23:00 UTC mevcut varsayıldı (gerçek zamanlı yayın haftalık olabilir → DÜŞÜK güven).
- `fred_*`: (indirilebildiyse) FRED serileri, D+1 22:00 UTC.
- `fwd1, fwd3, fwd5, fwd10` (VİOP), `sfwd*` (spot panel).

## Zorunlu yöntem kuralları (her analiz ajanı)
1. **İleriye bakma yok.** Her öngörücünün bilgi zamanını yaz; 15:00 UTC'den sonra biten hiçbir şey gün t sinyaline girmez. `placebo_lead()` ile kontrol et.
2. Örtüşen getiriler (h=3,5) için Newey-West lag ≥ h (`lib_altin.ic`, `nw_ols`, `split_stats` bunu yapar).
3. IS = 2017-03..2021-12, OOS = 2022-01..2026-11. Ayrıca yıl yıl işaret tutarlılığı. Parametre seçimi yalnız IS'te; OOS'ta tek sefer değerlendir. Spot panelde 2010–2016 ek "erken OOS".
4. **Drift tuzağı:** Altın 2017–2026'da güçlü yükseldi (≈1.230 → ≈4.100 USD). Uzun ağırlıklı her kural iyi görünür. Her stratejide (a) her zaman uzun (buy & hold) ile karşılaştır, (b) `demean=True` (drift çıkarılmış) Sharpe ver, (c) uzun ve kısa bacakları ayrı raporla.
5. Maliyet: temel 5 bps gidiş-dönüş (`COST_BPS`), stres 10 bps. Tutuş 1/3/5 gün, kademeli (örtüşen) uygulama `backtest()`.
6. **Her testi `register()` ile kaydet** (başarısızlar dahil). Global FDR bu kayıttan yapılacak. Test sayısını raporla.
7. Kod ve çıktıları `$S/out/<ajan_anahtarı>/` altına yaz. Kodun tek başına yeniden çalışabilmeli.
8. Sonuçları abartma: "bulunamadı" kabul edilebilir ve değerli bir sonuçtur.
