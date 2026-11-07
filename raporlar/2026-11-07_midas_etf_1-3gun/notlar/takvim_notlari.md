# Faz 1 — Olay takvimleri: notlar ve doğrulama (2026-11-07)

Betik: `kod/faz1/takvim.py` (çalıştırma: `python3 -I kod/faz1/takvim.py .`; internete çıkmaz, yalnız
`ham_sayfalar/takvim/` altındaki indirilmiş ham dosyaları okur). Çıktılar: `data/events/*.csv`
(sütunlar `date, event, detail, source`), doğrulama özeti `data/events/_dogrulama.json`.
Aralık 2016-01-01 .. 2026-12-31 (NYSE tatilleri 2016-2027). "GELECEK" etiketi = 2026-11-07 sonrası.
Saatler ET; `detail` içinde TR karşılığı var (TR sabit UTC+3: ABD yaz saatinde ET+7, kış saatinde ET+8).

## Dosyalar ve satır sayıları (başlık hariç)

| Dosya | Satır | Olay türleri | Resmî liste / kural |
|---|---|---|---|
| `fomc.csv` | 96 | FOMC_karar 87, FOMC_plansiz 4, FOMC_iptal 1, FOMC_diger 4 | Tamamı resmî (federalreserve.gov) |
| `cpi.csv` | 132 | CPI 131, CPI_iptal 1 | Tamamı resmî (BLS arşivi + takvim) |
| `nfp.csv` | 132 | NFP 131, NFP_iptal 1 | Tamamı resmî (BLS arşivi + takvim) |
| `eia_ng_storage.csv` | 574 | EIA_NG_depolama | 2025-2026 resmî (105), 2016-2024 kural (469; 6'sı teyitli) |
| `eia_petroleum.csv` | 572 | EIA_WPSR | Tamamı resmî: 564 arşiv (gerçekleşen) + 8 takvim (gelecek) |
| `opex.csv` | 132 | OPEX_aylik 88, OPEX_ceyrek_triple_witching 44 | Kural (tatiller doğrulanmış takvimden) |
| `nyse_tatil.csv` | 139 | NYSE_tatil 115, NYSE_erken_kapanis 24 | 2026-2027 resmî (nyse.com), 2016-2025 kural + veri kontrolü |
| `vadeler.csv` | 396 | NG_vade 132, CL_vade 132, VIX_vade 132 | NG/CL kural (+EIA veri ve TradingView kontrolü); VIX resmî Cboe listesi |
| `ung_uso_roll.csv` | 1806 | UNG_roll 528, USO_roll 948, BOIL_KOLD_roll 330 | Tamamı kural (ihraççı belgelerinden) |
| `hazine_ihale_10y30y.csv` | 264 | UST10Y_ihale 132, UST30Y_ihale 132 | Resmî (fiscaldata.treasury.gov 260 gerçekleşen + 4 geçici takvim) |

## 1) FOMC — `fomc.csv`
- Kaynak: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm (2021-2027) ve
  https://www.federalreserve.gov/monetarypolicy/fomchistorical2016.htm … `2020.htm`.
- `date` = 2. gün (karar açıklaması 14:00 ET). SEP (projeksiyon) toplantıları `detail`'de "SEP/projeksiyon: EVET" (43 adet).
  Basın toplantısı 2016-2018'de yalnız SEP toplantılarında, 2019'dan beri her toplantıda (Fed sayfalarından parse edildi).
- Plansız / özel (saatler Fed basın bültenlerinden): 2019-10-11 (4 Eki plansız görüşme, açıklama 11:00 EDT, faiz değişmedi),
  2020-03-03 (10:00 EST, -50bp), 2020-03-15 (Pazar 17:00 EDT, 0-0.25%), 2020-03-23 (notation vote 08:00 EDT, sınırsız QE);
  FOMC_diger: 2020-03-19 (swap hatları 09:00), 2020-03-31 (FIMA repo 08:30), 2020-08-27 ve 2025-08-22 (uzun vadeli strateji bildirgesi);
  FOMC_iptal: 2020-03-18 (17-18 Mart toplantısı iptal).
- 2026'nın kalan toplantısı: **2026-12-09** (8-9 Aralık, SEP). 2027 tarihleri (CSV dışı): 27 Oca, 17 Mar*, 28 Nis, 9 Haz*, 28 Tem, 15 Eyl*, 27 Eki, 8 Ara*.
- Doğrulama: yıl başına 8 planlı toplantı (2020'de 7; Mart iptal). Çarşamba olmayan planlı kararlar seçim haftaları:
  2018-11-08, 2020-11-05, 2024-11-07 (Perşembe) — Fed sayfasıyla aynı.

## 2) CPI — `cpi.csv` ve 3) NFP — `nfp.csv`
- bls.gov `requests` ile 403 "Access Denied" döndü (bot politikası; aşılmaya çalışılmadı). Sayfalar WebFetch ile okundu,
  çıktı `ham_sayfalar/takvim/webfetch/bls_*.txt` dosyalarına kaydedildi.
- Geçmiş: arşiv sayfaları https://www.bls.gov/bls/news-release/cpi.htm ve …/empsit.htm — her yayının URL'sindeki MMDDYYYY yayım tarihidir
  (örn. `cpi_10242025.htm`). Gelecek: https://www.bls.gov/schedule/news_release/cpi.htm (10 Kas 2026, 10 Ara 2026) ve
  …/empsit.htm (4 Ara 2026).
- Kapanma kaymaları (https://www.bls.gov/bls/2025-lapse-revised-release-dates.htm):
  NFP Eyl 2025 3 Eki → **20 Kas 2025**; NFP Eki 2025 **iptal** (planlı 7 Kas; Ekim payroll verisi 16 Ara raporunda); NFP Kas 2025 5 Ara → **16 Ara 2025**;
  NFP Oca 2026 6 Şub → **11 Şub 2026**; CPI Eki 2025 **iptal** (planlı 13 Kas); CPI Kas 2025 10 Ara → **18 Ara 2025**; CPI Oca 2026 11 Şub → **13 Şub 2026**.
  CPI Eyl 2025 arşivde **24 Eki 2025**; orijinal planlı tarih resmî sayfada bulunamadı (haberlere göre 15 Eki — doğrulanmadı).
- Doğrulama: yılda 12 yayın (2025'te 11 + 1 iptal). NFP'nin Cuma dışı günleri: 2020-07-02, 2025-07-03, 2026-07-02 (4 Temmuz tatili),
  2025-11-20, 2025-12-16, 2026-02-11 (kapanma). NYSE kapalıyken (Good Friday) yayın: CPI 2017-04-14, 2020-04-10; NFP 2021-04-02,
  2023-04-07, 2026-04-03 — `detail`'de işaretli (ETF tepkisi ertesi işlem günü).

## 4) EIA haftalık doğalgaz depolama — `eia_ng_storage.csv`
- Resmî: https://ir.eia.gov/ngs/schedule.html — yalnız 2025-2026 istisnalarını listeliyor: 2025-01-03 Cum, 2025-01-08 Çar (Carter yas günü,
  güncellendi), 2025-06-18 Çar, 2025-11-14 Cum, 2025-11-26 Çar, **2025-12-29 Pzt** (Noel; ilk sürümde 24 Ara idi — irtest.eia.gov kopyası),
  2025-12-31 Çar, 2026-11-13 Cum (Veterans Day), 2026-11-25 Çar (Thanksgiving). Diğer haftalar Perşembe 10:30 ET.
- 2016-2024 için resmî takvim **bulunamadı** (web.archive.org bu ortamda engelli, UNT arşivi 503, ir.eia.gov/ngs_test 403) →
  **kural** uygulandı, `detail`'de "kural":
  - Perşembe federal tatil/kapanış → Çarşamba 12:00 ET;
  - aynı haftada Salı veya Çarşamba kapalı → Cuma 10:30 ET;
  - yalnız Pazartesi veya Cuma tatili → değişiklik yok (Perşembe 10:30).
  Federal kapanışlara Noel arifesi kararnameleri (2018-12-24, 2019-12-24, 2020-12-24, 2024-12-24, 2025-12-24/26) ve yas günleri dahil.
- Kuralın testi: 2025-2026 resmî takvimine uygulandığında tüm istisnalar tuttu; tek fark Noel 2025 (Çar-Per-Cum kapalı, resmî Pazartesi 29 Ara).
- Teyitli kural tarihleri (WebSearch özetleri, `webfetch/websearch_teyitler.txt`): 2021-11-10 Çar, 2023-07-07 Cum, 2023-11-22 Çar,
  2024-06-21 Cum, 2024-11-27 Çar, 2024-12-27 Cum.
- Kuraldan çıkan 2016-2024 istisnaları (24 adet; doğrulanmadı olanlar `detail`'de işaretli): 2016-11-23, 2017-07-07, 2017-11-22, 2018-07-06,
  2018-11-21, 2018-12-07 (BELİRSİZ: 5 Ara yas günü kısa sürede ilan edildi, Perşembe 6 Ara olabilir), 2018-12-28, 2019-01-04, 2019-07-03,
  2019-11-27, 2019-12-27, 2020-01-03, 2020-11-13, 2020-11-25, 2020-12-23, 2021-11-10, 2021-11-24, 2022-11-23, 2023-07-07, 2023-11-22,
  2024-06-21, 2024-07-03, 2024-11-27, 2024-12-27.
- Bilinmeyen tek seferlik gecikmeler (sistem arızası vb.) dahil değil. 2026-12-24 normal Perşembe; Noel arifesi kapanış kararnamesi çıkarsa değişebilir.

## 5) EIA WPSR — `eia_petroleum.csv`
- Gerçekleşen tarihler: https://www.eia.gov/petroleum/supply/weekly/archive/ (her yayının klasör adı tarih; 2016-01-06 .. 2026-11-04, 564 yayın).
  Kalan 2026: https://www.eia.gov/petroleum/supply/weekly/schedule.php (12 Kas Per 12:00 Veterans Day; 18, 25 Kas; 2, 9, 16, 23, 30 Ara Çar).
- Doğrulama: takvim sayfasındaki 2025-2026 istisnalarının tamamı arşivde mevcut. Çarşamba dışı 85 yayın (çoğu Pazartesi tatili → Perşembe).
  Atlanan haftalar (arşivde boşluk): 2022-06-22 (EIA sistem sorunu, 29 Haz'da iki hafta birlikte), 2023-11-08 (15 Kas'ta birlikte);
  Noel 2025: 2025-12-29 Pazartesi 17:00 ve 2025-12-31.

## 6) Opsiyon vadesi — `opex.csv`
- Kural: ayın 3. Cuması; borsa tatiliyse önceki iş günü. Mart/Haziran/Eylül/Aralık "OPEX_ceyrek_triple_witching".
- Perşembe'ye kayanlar: 2019-04-18, 2022-04-14, 2025-04-17 (Good Friday), 2026-06-18 (Juneteenth — Cboe 2026 tatil listesi
  https://www.cboe.com/about/hours/us-options/ ile tutarlı). Tümü kuraldan hesaplandı; resmî OCC/Cboe vade listesi metin olarak alınamadı
  (Cboe 2026 vade takvimi PDF'i renk kodlu, `ham_sayfalar/takvim/cboe/`).

## 7) NYSE tatil ve erken kapanış — `nyse_tatil.csv`
- Resmî: https://www.nyse.com/markets/hours-calendars (2026-2028). 2026-2027: kural ile resmî liste **20/20 tatil, erken kapanışlar birebir aynı**.
- 2016-2025 kural (Juneteenth 2022'den itibaren; Cumartesiye denk gelen 1 Ocak gözlenmez) + özel kapanışlar 2018-12-05 (Bush), 2025-01-09 (Carter).
  Veri kontrolü: 2016-01-01..2026-11-06 arası hesaplanan 103 hafta içi tatilin tamamı SPY (2016-11-07'den) / VIX (öncesi) günlük verisinde
  işlem görmeyen günlerle **birebir aynı** (0 fark). Not: VIX verisinde 2022 sonrası bazı tatillerde (Cboe GTH seansı) satır olduğu için
  VIX yalnız SPY öncesi dönemde kullanıldı.
- Erken kapanışlar (13:00 ET): Thanksgiving ertesi, 24 Aralık (Pzt-Per ise), 3 Temmuz (Pzt-Per ise). 2016-2025 için kural; günlük veriden doğrulanamaz.

## 8) Vadeler — `vadeler.csv`
- NG son işlem = teslim ayının 1. gününden önceki 3. iş günü; CL = teslim ayından önceki ayın 25'inden 3 iş günü önce (25'i iş günü değilse 4).
  Kurallar EIA tanım sayfalarında da yazılı: https://www.eia.gov/dnav/ng/TblDefs/ng_pri_fut_tbldef2.asp ,
  https://www.eia.gov/dnav/pet/TblDefs/pet_pri_fut_tbldef2.asp . CME tatili ≈ NYSE düzenli tatilleri (özel yas günleri hariç; sonuçları etkilemiyor).
  cmegroup.com bu ortamdan 403/503 → CME sayfası okunamadı.
- Doğrulama 1 (resmî EIA verisi): EIA günlük Contract 1-4 fiyatlarında (https://www.eia.gov/dnav/ng/hist/rngc1d.htm …, RCLC1D…; veri 2024-04-05'te bitiyor)
  kontrat geçiş günü testi. NG: 95 uyumlu, 1 belirsiz, 2 uyumsuz, 34 veri yok. CL: 78 uyumlu, 19 belirsiz (düz eğri), 2 uyumsuz, 33 veri yok.
  Uyumsuzlar elle incelendi: NGH24 (27 Şub 2024 C1=1.615 vade günü, ertesi gün geçiş açık → kural doğru), NGH16 ve CLN18 (düz eğri, test ayırt edemiyor),
  CLK20 (20 Nis 2020 negatif fiyat günü testi bozuyor; son işlem 21 Nis 2020).
  Örnek uyumlu: NGJ16 2016-03-29, NGM16 2016-05-26 (Memorial Day), NGJ18 2018-03-27 (Good Friday), NGM21 2021-05-26, NGF22 2021-12-29,
  NGJ24 2024-03-26 (Good Friday), CLJ16 2016-03-21 (25 Mart Good Friday), CLM20 2020-05-19 (25 Mayıs Memorial Day).
- Doğrulama 2 (ikincil kaynak): TradingView kontrat listeleri (NYMEX NG1!/CL1! contracts) 2026-11..2029 için 76/76 vade kuralla aynı
  (örn. NGZ26 2026-11-25, NGF27 2026-12-29, CLZ26 2026-11-20, CLF27 2026-12-21).
- VIX: resmî Cboe listesi https://www.cboe.com/us/futures/market_statistics/historical_data/product/list/VX/ (aylık seriler, 132 adet).
  Kural (sonraki ayın 3. Cuması − 30 gün; Cuma/Çarşamba tatilse önceki iş günü) ile **132/132 aynı**. Salı'ya kayanlar: 2019-03-19, 2022-03-15,
  2025-03-18 (Good Friday), 2024-06-18 (Juneteenth Çarşamba), 2026-05-19 (Juneteenth Cuma 19 Haz 2026). Kalan 2026: 18 Kas, 16 Ara.
  "İşlem uzlaşma sabahı 08:00 CT'de biter" bilgisi Cboe şartnamesine dayanır; şartname sayfası JS ile yüklendiğinden ham metinde yok.

## 9) Roll pencereleri — `ung_uso_roll.csv` (tamamı kuraldan)
- **UNG** (UNG 10-K FY2025, https://www.sec.gov/Archives/edgar/data/1376227/000110465926021507/ung-20251231x10k.htm): roll ön ay vadesinden
  "two weeks prior" başlar, 4 gün sürer (%25/%50/%75/%100, gün sonu). Kural: başlangıç = NG vadesi − 14 takvim günü; tatile denk gelirse önceki iş günü
  (VARSAYIM — belgede yazmıyor; 2018-01 ve 2024-01'de etkili). USCF'nin yayımladığı roll tarihleri CSV'si JS + yetkili API ile yükleniyor → **bulunamadı**.
  Görev tanımındaki "yaklaşık 2 hafta önce başlayan 4 iş günü" belgeyle uyumlu. Örnek: Kas 2026 penceresi 11-16 Kas (NGZ26→NGF27), Ara 2026 15-18 Ara.
- **USO**: 2016-01..2020-04 UNG ile aynı kural (CL vadesi − 14 gün, 4 gün; USO 10-K FY2016/FY2019). Mayıs 2020'den itibaren ayın ilk iş gününden başlayan
  10 günlük roll (2020-05..2025-12), 2026-01'den itibaren ayın ilk 5 işlem günü (USO 10-K FY2025 ve 424B3 Kasım 2025). 2020-05..2023-08 USO çok vadeli
  portföy tuttu; 2023-09..2024-01 tekrar ağırlıklı ön aya geçti. Nisan 2020'deki portföy yeniden yapılandırmalarının gün gün listesi **bulunamadı**.
- **BOIL/KOLD** (ProShares, Bloomberg Natural Gas Subindex): ayın 6.-10. iş günü, günde ~%20 (ProShares BOIL sayfası). Görev tanımındaki "aylık roll"
  **düzeltildi**: BCOM metodolojisi Table 9'a göre NG ana kontratı Oca-Şub Mart, Mar-Nis Mayıs, May-Haz Temmuz, Tem-Ağu Eylül, Eyl-Eki Kasım,
  Kas-Ara Ocak → roll yalnız **Şubat, Nisan, Haziran, Ağustos, Ekim, Aralık** aylarında (2 ayda bir). İş günü ≈ NYSE. Örnek: Ara 2026 8-14 Ara (NGF27→NGH27).
  BOIL'in 2016-2026 arasında endeks değiştirip değiştirmediğine dair kaynak bulunamadı; tüm dönem için güncel kural kullanıldı.

## 10) Hazine 10Y/30Y ihaleleri — `hazine_ihale_10y30y.csv` (opsiyonel)
- https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query (original_security_term 10-Year/30-Year;
  TIPS ve eski kağıtların 3 yıllık yeniden ihraçları çıkarıldı). Yılda 12 + 12 ihale. Aynı ayda ikinci kayıt olarak görünen 2019-06-21 (10Y, CUSIP 9128286T2)
  çıkarıldı. Gelecek: 10 Kas 2026 (10Y), 12 Kas 2026 (30Y), 8 Ara 2026 (10Y reopening), 10 Ara 2026 (30Y reopening) — Hazine geçici takvimi
  (https://home.treasury.gov/system/files/221/Tentative-Auction-Schedule.pdf) ve TreasuryDirect upcoming.

## Ham kaynaklar
`ham_sayfalar/takvim/`: Fed, EIA, NYSE, USCF, ProShares, Cboe sayfaları (`index.tsv` indirme günlüğü), `cboe/` (VX JSON, opsiyon takvimi PDF),
`eia_futures/` (C1-C4 tabloları), `treasury/` (fiscaldata JSON, geçici takvim PDF), `dosyalar/` (BCOM metodoloji PDF + metin),
`webfetch/` (BLS listeleri, SEC alıntıları, WebSearch teyitleri, TradingView kontrat listesi), `uscf_js/` (USCF sayfa betikleri; roll CSV'sine erişilemedi).
