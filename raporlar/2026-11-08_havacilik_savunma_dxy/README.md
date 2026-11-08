# Havacılık ve Savunma Sektörü: Borsa Görünümü ve DXY–Teslimat İlişkisi (8 Kasım 2026)

Ana rapor (grafikli, Word/PDF'e aktarılabilir): https://claude.ai/artifact/SdnyRqmEQaxCVP23uv4Syv

## Bulgular
- MSCI World A&D yılbaşından 30 Ekim 2026'ya %-3,5 (MSCI World +%9,8); MSCI Europe A&D %-4,2 (MSCI Europe +%4,1).
- Gerilemenin kaynağı değerleme: ileri F/K 25,3 (piyasa 17,4). 3 yıllık yıllık getiriler hâlâ %25–35.
- DXY ile sivil uçak sipariş birikimi (karşılanmamış sipariş / aylık sevkiyat) arasında Granger nedenselliği yok
  (1992–2026, p = 0,59–0,96); 12 aylık değişimlerin korelasyonu 0,03.

## Veri
- MSCI endeks bilgi formları (30 Ekim 2026)
- Yahoo Finance: DX-Y.NYB, ITA, EUAD, ^GSPC, JETS ve hisseler
- FRED: ANAPUO, ANAPVS, IPG3364S, DTWEXBGS

## Tekrar üretim
`python3 analiz.py <veri_klasörü>`. Klasörde Yahoo chart JSON dosyaları (`y_*.json`, `d_*.json`) ile FRED CSV
dosyaları (`f_*.csv`) bulunmalıdır. Gereken kütüphaneler: pandas, numpy, statsmodels.
