araç: 41/40 (41. çağrı bu teslim; kontrol noktasında iş bitmişti, devam edilmedi)

## Özet

Model: bu alt ajan Fable 5.2 (claude-fable-5-2) ile çalıştı.

Bütün paneller üretildi; önceki yarım denemenin D2 kalıntıları silindi, betikler baştan yazıldı. Tek eksik: İş Yatırım 5 dk verisi XU030 ve XU100 için kısmi kaldı (sunucu kotası).

**VİOP.** 2017-03-06 → 2026-11-19 arası 2.436 bülten indirildi, süzüldü, ham dosyalar silindi. `viop_daily` 75.075 satır, `viop_front` 11.138 satır. Bülten günleri spot günleriyle birebir örtüşüyor; tek fark 2023-02-08…14 (kapalı borsa, işlemsiz bülten). Uzlaşma/spot oranı makul (medyan 1,009–1,015). Vade geçişinde sıçrama yok. XU030 vadelisi 2020-07-27'de 10 kat ölçek değiştirdi (`fiyat_carpani` eklendi). Baz yük elektrik vadelisi 2022'den beri fiilen işlemsiz.

**Gün içi.** Yahoo saatlik 48 sembol (2023-12-21 →), 5 dk 48 sembol (2026-08-28 →). Veriden saptananlar:
- Saatlik barlar :30'da başlıyor (09:30 … 17:30). Kapanış seansı hiçbir gün içi barda yok; resmi kapanış yalnız günlük veride.
- 17:30 barı kış aylarında yok (hisse-günlerin %38'i).
- Yahoo gün içi fiyatları 15 hissede geçmişe dönük bölünme düzeltmeli. snap'te hisse fiyatları ham baza çevrildi (`yahoo_carpan`); p_close ve p_open D1'in `px.parquet` dosyasından alındı.
- Saatlik veride 17:00 ve 17:50 için tam bar yok: p_1700 = 16:30 fiyatı, p_1750 = 17:30 fiyatı (en yakın önceki bar). Tam değerler yalnız son 60 günde (5 dk).
- İş Yatırım: saatlik üç endekste 2017'den beri tam; 5 dk XELKT'de tam; period=15 ve 30 desteklenmiyor.

**snap.** 35.617 satır; sütunlar: date, sym, p_open, p_1630, p_1700, p_1730, p_1750, p_son, p_close, kaynak, bar_1700, bar_1750, bar_son, yahoo_carpan. Endeksler 2017'den itibaren var.

**panel_dev.** viop_daily, viop_front, snap, h1/ (42 dosya), h1_isy/ (3 dosya) 2025-06-30'da kesildi; denetimde kesim sonrası satır 0. m5 yalnız panel_full'da.

**Dosyalar**
- /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/panel_full/ (viop_daily.parquet, viop_front.parquet, snap.parquet, h1/, m5/, h1_isy/, m5_isy/, VERI_NOTU_D2.md)
- /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/panel_dev/
- /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/raw/d2/ (ham ve ara dosyalar, dogrulama_viop.txt, dogrulama_gunici.txt)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/VERI_NOTU_D2.md (489 kelime)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/d2_veri/ (run.sh, d2common.py, 01–08; eski yarım betikler silindi)

## İddia defteri

iddia | kaynak | alıntı ya da sayı | güven
---|---|---|---
Bülten kapsamı | https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv ; raw/d2/viop_filt/_status.json | "Counter({'200': 2436, '404': 101})" | yüksek
Takvim spotla örtüşüyor | raw/d2/dogrulama_viop.txt | "bülten günü 2436 spot günü 2431"; fark 2023-02-08…14 | yüksek
İlk tarih ve gün sayısı | panel_full/viop_front.parquet | AKSEN 2022-11-01 (1019), ENJSA 2018-12-14 (1989), ODAS 2021-04-22 (1398), ASTOR 2023-07-17 (841), ALARK 2022-11-01 (1019), XU030 2017-03-06 (2436) | yüksek
Sıfır hacimli gün oranı (yakın vade) | raw/d2/dogrulama_viop.txt | AKSEN 0,0049; ENJSA 0,0025; ODAS 0,0036; ASTOR 0; ALARK 0,0049; XU030 0,0021; ELCBAS 0,52 | yüksek
Uzlaşma/spot oranı makul | raw/d2/dogrulama_viop.txt | medyan 1,0093–1,0147; p1–p99 0,943–1,066 | yüksek
Oran sınır dışı yalnız ENJSA 4 gün | raw/d2/dogrulama_viop.txt | 2020-03-31 0,925; 2021-04-08 0,923; 2022-03-31 0,911; 2026-04-17 0,923 | yüksek (temettü yorumu: orta)
Vade geçişinde sıçrama yok | raw/d2/dogrulama_viop.txt | geçiş günü medyan vadeli−spot farkı 24–48 bps; naif seride 243–334 bps | yüksek
Vadeli–spot günlük getiri korelasyonu | raw/d2/dogrulama_viop.txt | 0,9415 (ENJSA) – 0,9859 (ODAS) | yüksek
XU030 ölçek değişimi | panel_full/viop_daily.parquet | F_XU0300820: 2020-07-24 135,525 → 2020-07-27 1358,00; önceki uzlaşma 1355,25 | yüksek
Bültenin önceki uzlaşması tutarlı | raw/d2/dogrulama_viop.txt | "ONCEKI UZLASMA != dünkü uzlasma: 3 {'XU030': 3}" | yüksek
Elektrik vadelisi işlemsiz | raw/d2/dogrulama_viop.txt | işlem olan gün: 2021: 222, 2022: 26, 2023: 2, 2024: 0, 2025: 1, 2026: 4 | yüksek
Son 1 yıl medyan günlük hacim (mn TL) | raw/d2/dogrulama_viop.txt | AKSEN 285; ENJSA 103; ODAS 214; ASTOR 1.934; ALARK 242; XU030 42.092 | yüksek
Yahoo saatlik kapsam | https://query1.finance.yahoo.com/v8/finance/chart/AKSEN.IS?range=730d&interval=60m | 48 sembol; 35'i 2023-12-21'den; 13'ü halka arz nedeniyle geç | yüksek
range=730d ENTRA ve MOGAN'da hata veriyor | aynı uç nokta | "The requested range must be within the last 730 d"; period1 ile alındı (n=4510) | yüksek
Saatlik bar ızgarası | panel_full/h1/ | başlangıçlar 09:30 … 17:30; 17:30 barı 18.307, diğerleri yaklaşık 29.300–29.600 | yüksek
Kapanış seansı gün içi barlarda yok | raw/d2/dogrulama_gunici.txt | "h1 17:30 barı kapanışı vs m5 17:55 barı kapanışı … birebir aynı oran 1.0" | yüksek
Son sürekli işlem fiyatı ile resmi kapanış farklı | raw/d2/dogrulama_gunici.txt | eşit olan oran 0,226; medyan fark 17 bps | yüksek
17:30 barı kışın yok | raw/d2/dogrulama_gunici.txt | çeyrek oranı: 2024Q1 0,0; 2024Q3 1,0; 2025Q1 0,0; 2025Q3 1,0; 2026Q1 0,06 | yüksek (nedeni bilinmiyor)
Yahoo gün içi fiyatları kısmen düzeltmeli | raw/d2/yahoo_carpan_kirilmalar.csv | 15 hisse, hisse-günlerin %18,3'ü; 21 kırılmanın 21'i D1 ca_day ile eşleşiyor | orta-yüksek
Ham baza çevirme sonrası kalan sapma | raw/d2/dogrulama_gunici.txt | p_1730/p_close sapması > %10,5: 10 hisse-gün; p_son için 0 | orta
Zaman damgaları doğru | raw/d2/dogrulama_gunici.txt | "doğru hiza \| kapsama oranı kış 1.0 yaz 1.0 \| n 722"; 1 saat kaydırınca 0,56–0,66 | yüksek
Saatlik ve 5 dk barlar tutarlı | raw/d2/dogrulama_gunici.txt | 15:30 ve 17:30 barlarında birebir oran 1,0; 16:30 barında 0,9996 | yüksek
17:50 yerine 17:30 fiyatının bedeli | raw/d2/dogrulama_gunici.txt | medyan fark 27,3 bps, p90 103,1 (n 2.760; 60 gün) | orta (kısa örneklem)
Gün içi fiyat ile kapanış farkı | raw/d2/dogrulama_gunici.txt | 17:50 → kapanış medyan 34,6 bps; 17:00 → kapanış 58,0 bps; 17:30 → kapanış 38,8 bps (tüm dönem) | yüksek
İş Yatırım saatlik geçmişi | https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll?period=60 | XELKT ve XU030 n=21479, 2017-01-02 → 2026-11-20, 2.478 gün | yüksek
İş Yatırım 5 dk XELKT | aynı uç nokta, period=5 | n=230445, 2.478 gün, günde medyan 97 bar | yüksek
İş Yatırım 5 dk XU030 ve XU100 kısmi | raw/d2/log/isy_m5_xu030_sabirli.log, isy_m5_xu100_sabirli.log | XU030 414 gün, kalan 50 pencere; XU100 1.050 gün, kalan 33 pencere | yüksek
period=15 ve 30 desteklenmiyor | aynı uç nokta | HTTP 200, 0 bayt (XELKT ve XU030, 2017 ve 2026 pencereleri) | yüksek
İş Yatırım günün son değeri = resmi kapanış | raw/d2/dogrulama_gunici.txt | D1 idx ile < 1 bps oranı 0,9996–1,0 (n 2.477) | yüksek
panel_dev kesimi temiz | 06_dev_kes.py çıktısı | "panel_dev D2 parquet 48 \| kesim sonrasi satir 0"; en son ts_tr 2025-06-30 18:00 | yüksek

## açık kalanlar

- **XU030 ve XU100 için İş Yatırım 5 dk eksik.** Sunucu bu iki seride birkaç pencereden sonra boş dönüyor; yaklaşık dakikada bir pencere alınabildi. Elde olan: XU030 2017, 2018 başı, 2026-05 sonrası; XU100 2017–2019 parçalı, 2025-01 sonrası. Eksik günlerde snap `isy_h1` kullanıyor: p_1700 tam, p_1750 50 dakika bayat. Tamamlamak için `python3 -I kod/d2_veri/04_isy_endeks.py m5 XU030 XU100 SABIRLI=3600` kaldığı yerden sürer (tahminen bir saat), ardından 05 ve 06 yeniden çalıştırılır.
- **Hisselerde tam 17:00 ve 17:50 fiyatı yalnız son 60 günde var.** Öncesi 16:30 ve 17:30 fiyatıdır; A7 ajanı `kaynak` ve `bar_*` sütunlarına göre ayırmalı. Önceki çalışmanın notuna göre aynı İş Yatırım uç noktası hisse için de saatlik ve 5 dk veri veriyor; görev bunu yalnız endeks için tanımladığından çekmedim. İstenirse dar bir takip görevi hisselerde 2017'den beri tam 17:00 ve 17:50 fiyatı sağlayabilir.
- **`yahoo_carpan` bir kestirimdir.** Kalan 10 hisse-günlük büyük sapma (ör. ESEN 2025-10-21, BIGEN 2026-11-02) gerçek hareket mi, baz hatası mı ayrılmadı. TATEN'de 2025-12-25 → 2026-01-06 arasında 17:30 fiyatı kapanışın %5–7 altında görünüyor; incelenmedi.
- snap'teki p_close ve p_open D1'in `px.parquet` dosyasına bağlı; D1 paneli yeniden üretilirse 05 ve 06 yeniden çalıştırılmalı.
- `viop_front` vadeyi aynı günün hacmine göre seçiyor; işlem kuralı için bir gün gecikmeli seçim gerekirse `viop_daily`'den kurulmalı.
- XELKT için açılış fiyatı yok (snap'te p_open boş).
- Sahibi belirsiz kalıntılara dokunmadım: scratchpad `el/kod_tmp/`, `el/an1.py`, `el/dl_yahoo.log`, `el/data/yahoo_raw/d/`.
- Git'e commit yapılmadı.