# Altın Trade Rehberi (uygulama sayfası)

- `altin_rehberi.html`: Adım adım uygulama sayfası (claude.ai'da yayımlanan Artifact'ın kaynağı). İçerik:
  - Pazartesi 9 Kasım 2026 durumu ve günlük rutin.
  - Kural kartları ve hesaplayıcı.
  - 2027 Temmuz'a kadar takvim, boyut ve risk bölümü.
  - Sinyal tablosu ve rapor özetleri.
- `sade_backtest.py`, `sade_sonuc.csv`, `sade_ozet.csv`: Elle uygulanabilir sade sürümlerin geriye dönük testi ve asıl (kademeli) kurallarla karşılaştırması.
  - Midas: sade plan (sinyal gelince kolu tamamen al, son sinyalden h gün sonra sat) asıla yakın ya da daha iyi. 1,5 USD/emir komisyonla 10.000 USD hesapta OOS Sharpe 0,89; kademeli planda 0,55.
  - VİOP: sayım yöntemi asıla eşit.
  - Tam kollu ve çoğunluk oylu VİOP basitleştirmeleri belirgin kötü.
- `parametreler.json`: Hesaplayıcı katsayıları ve eşikleri (06.11.2026), 12 aylık aralıkları ve güncelleme önerisi.
- `takvim.csv`: 09.11.2026–06.07.2027 işlem ve risk günleri (NYSE, BLS, Fed, TR tatilleri, VİOP vadeleri).

Yatırım tavsiyesi değildir.
