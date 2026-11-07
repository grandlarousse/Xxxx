# ETF (Midas cephesi) paneli — ek kurallar

Önce `DATA_README.md`'yi oku (genel kurallar geçerli). Bu dosya ABD kapanışından kapanışına ETF işlemleri içindir.

## Zaman
- Giriş = gün t ABD kapanışı (16:00 ET; yazın 20:00, kışın 21:00 UTC). Çıkış = t+h ABD kapanışı (h=1,3,5 NYSE işlem günü).
- **Karar anı (cutoff) = gün t 15:00 ET** (`cut_utc` sütunu). Saatlik veri kullandığımız için kapanıştan 1 saat önce sabitlendi. Gerçek hayatta 15:45–15:55 ET'de karar verip kapanışa yakın emir (Midas'ta MOC yoksa limit/piyasa emri) varsayılır. Son saatteki hareket sinyale girmez; bu muhafazakârdır. Son 60 gün için 5 dakikalık veri var (`panel/yahoo_5m/`).
- Gün t'de bilinenler: VİOP uzlaşması (15:10 UTC), BIST kapanışı, Avrupa kapanışları (DAX/STOXX 17:30 CET, FTSE 16:30 Londra), Asya kapanışları, spot altın ve Dukascopy çapraz varlıkların 15:00 ET değeri, ABD Hazinesi t-1, COT (Cuma 21:00 UTC sonrası), SHFE (07:00 UTC t), GLD/GLDM NAV ve pay sayısı (t-1).
- **Gün t'de bilinmeyenler:** ETF'lerin gün t kapanışı (`c_*` sütunları = giriş fiyatı, sinyalde KULLANMA), gün t ABD kapanışlı her şey, gün t NAV (`flow_*_nav_t`; LBMA PM'den hesaplanır ama SSGA akşam yayınlar).

## Dosya: `$S/panel/panel_etf.parquet` (endeks = NYSE işlem günleri 2008-01-02 → 2026-11-06)
- `c_<TICKER>`: o enstrümanın **kendi yerel takvim günü t**'deki kapanışı (hisse/ETF'de temettü düzeltmeli). ABD ETF'leri için hedef: `np.log(c_GLD).shift(-h) - np.log(c_GLD)`. Yabancı borsalar için `c_*` farklı saatte kapanır. Lead-lag için `y_*` kullan.
- `y_<TICKER>`, `y_<TICKER>_avail`, `y_<TICKER>_vol`: cutoff'tan önce kapanmış son değer, zamanı ve hacmi. ABD varlıklarında bu t-1 kapanışıdır. Avrupa ve Asya'da gün t kapanışıdır.
- `xau_cut` (15:00 ET), `xau_close` (16:00 ET; sinyalde yasak), `xau_1500utc` (VİOP uzlaşma anı), `xau_00utc`, `xau_07utc`, `xau_12utc`: Dukascopy spot altın.
- `dk_<SYM>_cut`: Dukascopy çapraz varlıklar 15:00 ET'de (XAGUSD, XPTUSD, DOLLARIDXUSD, USTBONDTRUSD, USA500IDXUSD, USDJPY, EURUSD, USDCNH, USDTRY, BRENTCMDUSD, COPPERCMDUSD, VOLIDXUSD, BTCUSD).
- `viop_v_settle`, `viop_v_ret`, `viop_v_volume`, `viop_v_oi`, `viop_vo_xautry_settle`, `viop_vo_usdtry_settle`, `viop_tr_prem_matched`, `shfe_AU0_c`, `dk_USDCNH_p07`, `xau_p07`: aynı gün VİOP ve Şanghay bilgisi. Türkiye tatillerinde NaN.
- `ust_*` (t-1), `cot_gold_*`.
- `flow_gld_shares`, `flow_gld_nav`, `flow_gldm_shares`, `flow_gldm_nav`: SSGA günlük NAV ve dolaşımdaki pay (as-of t-1). Akış ≈ Δshares × NAV. Ham dosya `panel/etf_gld_navhist.parquet` (2004+). Pay sayısının hangi gün güncellendiği (oluşturma emri günü mü, T+1 mi) belirsiz. Hem t-1 hem t-2 gecikmesini test et.
- Kapsama: UGL/GLL 2008-12+, NUGT/DUST 2010-12+, JNUG/JDST 2013+, GDXU 2020-12+, GLDM 2018-06+, AAAU 2018-08+, PHYS 2010+, BIST BYF'leri (GLDTR_IS, ZGOLD_IS, ISGLK_IS, GMSTR_IS) Yahoo'dan; kapsamı kontrol et.
- Saatlik ETF: `panel/yahoo_h/<TICKER>.parquet` (son 730 gün, GLD, IAU, GLDM, GDX, GDXJ, SLV, NUGT, UGL, GLL, DUST, PHYS, SIL, RING, SPY; pre/post dahil olabilir; index ts_utc = bar başlangıcı). 5 dakikalık: `panel/yahoo_5m/` (son 60 gün: GLD, GDX, GDXJ, NUGT, SLV, IAU, GC=F).

## Midas gerçekleri (araştırma raporu `research/m1_midas_platform.md` gelince güncellenecek)
- Varsayılan maliyet: komisyon + kur makası + ETF spread toplamı. GLD/IAU için gidiş-dönüş 10 bps temel, 20 bps stres. Kaldıraçlı ETF'ler için 20/40 bps.
- Açığa satış olmadığını varsay. Kısa yön yalnız ters ETF'le (GLL, DUST, JDST, ZSL) ya da hiç. Her stratejide **yalnız uzun (değilse nakit)** sürümü ve **ters ETF'li** sürümü ayrı ayrı ver.
- Kaldıraçlı ETF'lerde günlük yeniden dengeleme aşınması var. 1/3/5 günde gerçekleşen kaldıracı ölç.
