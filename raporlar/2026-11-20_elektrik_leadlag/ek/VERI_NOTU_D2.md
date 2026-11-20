# VERİ NOTU D2 — VİOP bülteni ve gün içi veri

**Dosyalar** (`panel_full/`; `panel_dev/` = 2025-06-30'da kesik kopya, m5 hariç)
- `viop_daily.parquet` (gün × sözleşme), `viop_front.parquet` (gün × dayanak; o gün hacmi en yüksek vade).
- `h1/`, `m5/`: Yahoo barları (ts_utc, ts_tr, o, h, l, c, v); 46 hisse + XU030, XU100.
- `h1_isy/`, `m5_isy/`: İş Yatırım endeks serileri (ts_utc, ts_tr, c); XELKT, XU030, XU100.
- `snap.parquet`: date, sym, p_open, p_1630, p_1700, p_1730, p_1750, p_son, p_close, kaynak, bar_1700, bar_1750, bar_son, yahoo_carpan.

**VİOP**
- 2017-03-06 → 2026-11-19, 2.436 bülten günü. İlk tarihler: XU030 ve elektrik 2017-03-06, ENJSA 2018-12-14, ODAS 2021-04-22, AKSEN ve ALARK 2022-11-01, ASTOR 2023-07-17.
- 2023-02-08…14 (deprem kapanışı) bültende var ama işlem yok; spot panelinde bu günler yok.
- `ret_settle`, `ret_last`: aynı sözleşmenin dünkü fiyatına göre, vade geçişinde sıçrama yok. `ret_settle_f1..f3`: t'de seçilen sözleşmenin ileri getirisi.
- XU030 vadelisi 2020-07-27'de 10 kat ölçek değiştirdi; seviye için `uzlasma × fiyat_carpani`.
- Baz yük elektrik (ELCBAS, ELCBASQ, ELCBASY) 2022'den beri fiilen işlemsiz; uzlaşması kuramsal, sinyal olarak kullanılmamalı.
- Temettü öncesinde vadeli spotun altına iner (ENJSA'da 4 gün oran < 0,93); baz sinyalinde ayıklanmalı.

**Yahoo saatlik barlar (TSİ)**
- Barlar :30'da başlar: 09:30 … 17:30. 09:30 barı açılış seansını içerir; hacmi güvenilmez. 17:30 barı 17:30–18:00'dir.
- **Kapanış seansı (18:00–18:10) hiçbir gün içi barda yok**; resmi kapanış yalnız günlük veride (`p_close`).
- 17:30 barı kış aylarında (yaklaşık kasım–mart) yok; son bar 16:30 olur. `p_son` hisse-günlerin %38'inde boş.
- Gün içi fiyatlar 15 hissede geçmişe dönük bölünme düzeltmeli: ham fiyat = bar / `yahoo_carpan`. snap'teki hisse fiyatları ham bazdadır; p_close ve p_open D1'in `px.parquet` dosyasından.
- Kapsam: saatlik 2023-12-21 → 2026-11-20 (13 hisse halka arz nedeniyle geç başlar); 5 dk 2026-08-28 → 2026-11-20.

**snap kuralları**
- `m5` (son 60 gün): p_1700 = 16:55 barı, p_1750 = 17:45 barı kapanışı.
- `h1`: en yakın önceki tamamlanmış bar: p_1700 = p_1630 (15:30 barı), p_1750 = p_1730 (16:30 barı); 30 ve 20 dakika bayat.
- Endeks `isy_m5`: 16:55 ve 17:45 barları. `isy_h1` (5 dk yoksa): p_1700 = 16:00 barı (tam), p_1750 = aynı bar (50 dk bayat).
- Yarım günlerde günün son barı kullanılır; `bar_*` sütunları kullanılan barı gösterir.

**İş Yatırım endeks verisi**
- Damga bar başlangıcı, değer aralığın son değeri; OHLC ve hacim yok. 18:00 damgalı değer resmi kapanış.
- period=60: üç endeks 2017-01-02'den beri tam. period=5: XELKT tam (2017-); XU030 414 gün (2017, 2018 başı, 2026-05 sonrası), XU100 1.050 gün (2017–2019 parçalı, 2025-01 sonrası). Sunucu bu iki seride birkaç pencereden sonra boş dönüyor (kota); `04_isy_endeks.py … SABIRLI=<sn>` kaldığı yerden sürdürür.
- period=15 ve 30: boş yanıt, desteklenmiyor. XELKT için açılış yok (p_open boş).

**Doğrulama**
- Bülten günleri = spot günleri + 5 kapalı gün. Uzlaşma/spot oranı medyan 1,009–1,015; vadeli-spot getiri korelasyonu 0,94–0,99.
- Saatlik 15:30, 16:30, 17:30 bar kapanışları 5 dk verisinin 16:25, 17:25, 17:55 barlarıyla birebir aynı.
- Yahoo XU030 saatlik barı İş Yatırım'ın aynı andaki değerini %100 kapsıyor: zaman damgaları doğru.
- 17:30 fiyatı ile resmi kapanış arasındaki medyan fark 39 bps; 17:50 (5 dk) ile 35 bps.
- Ayrıntı: `raw/d2/dogrulama_viop.txt`, `raw/d2/dogrulama_gunici.txt`. Kod: `kod/d2_veri/run.sh`.
