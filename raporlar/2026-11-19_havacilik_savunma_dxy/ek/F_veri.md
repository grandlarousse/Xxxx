araç: 22/35

| dosya | seri | tarih aralığı | satır | kaynak | son değer |
|---|---|---|---|---|---|
| yahoo_gunluk.csv | 17 ticker günlük close/adjclose (+^DJUSAE, ^DJSASD tek nokta) | 1970..2026-11-19 (ticker'a göre) | ~140 bin | query1.finance.yahoo.com v8 chart | DXY 103.81; ITA 69.39; BA 162.91 |
| yahoo_aylik.csv | ay sonu adjclose geniş | 1970-01..2026-11 | 683 | aynı | - |
| msci_aylik.csv | World 990100, Europe 990500, Europe A&D Capped 763669 (USD/EUR, NETR/STRD) | 1998-12..2026-10 (763669: 2014-11) | 143-335 / seri | app2.msci.com getLevelDataForGraph | World NETR USD 15753.31; Europe 13141.59; Eur A&D Capped 5026.99 |
| fed_ip_havacilik.csv | G3364, G336411T3, G3364T9 (2017=100, SA) | 1972-01..2026-10 | 3x658 | federalreserve.gov ip_sa.txt | G3364 96.74 |
| eurostat_c303.csv | C30.3 FR, DE, EU27, IT, ES (2021=100) | 1990/91..2026-09 | 321-441 | Eurostat sts_inpr_m | FR 140.1, DE 145.3, EU27 150.3 |
| airbus_boeing_yillik.csv | teslimat+net sipariş | 1974-2026 | 53 | Wikipedia Competition_between_Airbus_and_Boeing | 2026 kısmi: Airbus 621, Boeing 524 |

Alınamayanlar: MSCI World A&D ve standart MSCI Europe A&D kodları bulunamadı (arama uçları boş, sayfalar kod vermedi; kod taraması izin sistemince reddedildi, aşılmadı). Proxy: 763669 (Europe A&D Capped) indirildi; World için ITA/XAR/PPA. ^DJUSAE/^DJSASD geçmişi yok (1 nokta). MSCI günlük alınmadı. Madde 6 (aylık/çeyreklik teslimat) denenmedi.

Uyarılar: Airbus/Boeing 2018-2025 teslimatları verilen değerlerle birebir uyuştu. 2026 satırı kısmi yıl. MSCI son nokta 2026-10-30. RR.L/BA.L pence cinsinden. EURUSD 1.0975 son değer (gün içi olabilir). Betik: hesap/01_veri_indir.py (MSCI_EXTRA ortam değişkeniyle ek kod; 763669 için MSCI_EXTRA='{"763669":"..."}' ile çalıştırıldı). README: veri/README.md.
