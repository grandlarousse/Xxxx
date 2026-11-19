# Veri dosyalari (erisim: 2026-11-19; betik: hesap/01_veri_indir.py)

| Dosya | Kaynak URL | Satir | Aralik | Birim / not |
|---|---|---|---|---|
| yahoo_gunluk.csv | https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?period1=0&period2=1900000000&interval=1d | ~140 bin (19 ticker) | ticker'a gore, BA/GE/RTX/LMT/^GSPC 1970-01-02, DX-Y.NYB 1971-01-04, EUAD 2024-10-22; hepsi 2026-11-17/19'a kadar | close, adjclose yerel para birimi (AIR.PA, SAF.PA, RHM.DE EUR; RR.L, BA.L pence GBp) |
| yahoo_aylik.csv | ayni | 683 ay | 1970-01..2026-11 | ay sonu adjclose, genis tablo (^DJUSAE, ^DJSASD hemen hemen bos) |
| msci_aylik.csv | https://app2.msci.com/products/service/index/indexmaster/getLevelDataForGraph?... | bkz. asagi | 1998-12..2026-10 | ay sonu; USD/EUR x NETR/STRD; kod 990100 World, 990500 Europe, 763669 Europe A&D Capped |
| fed_ip_havacilik.csv | https://www.federalreserve.gov/releases/g17/ipdisk/ip_sa.txt | 3x658 | 1972-01..2026-10 | endeks 2017=100, mevsimsellikten arindirilmis. G3364 (havacilik urun+parca), G336411T3 (ucak+motor/parca alt kalemi), G3364T9 |
| eurostat_c303.csv | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_inpr_m?format=JSON&geo={geo}&nace_r2=C303&s_adj=SCA&unit=I21 | FR 441, DE 429, EU27 429, IT 321, ES 417 | 1990/91..2026-09 | endeks 2021=100, takvim+mevsim duzeltmeli |
| airbus_boeing_yillik.csv | https://en.wikipedia.org/wiki/Competition_between_Airbus_and_Boeing | 53 | 1974-2026 | adet; 2026 KISMI YIL (Airbus 621 / Boeing 524 teslimat) |

## Akil sagligi
- Yahoo: sifir/tekrar yok. Son kapanis: DXY 103.81, EURUSD 1.0975, ITA 69.39, XAR 218.95, PPA 153.61, EUAD 38.56, GSPC 7323.63, URTH 197.72, BA 162.91, GE 328.10, RTX 197.45, LMT 578.19, AIR.PA 201.10, SAF.PA 306.00, RHM.DE 760.90, RR.L 1326.6, BA.L 1860.5. EURUSD son tarih 11-19 (anlik/gun ici olabilir).
- ^DJUSAE (2822.49) ve ^DJSASD (52576.92) yalniz 1 nokta (2026-11-18); gecmis alinamadi.
- MSCI son degerler (2026-10-30): World NETR USD 15753.31; Europe NETR USD 13141.59; Europe A&D Capped NETR USD 5026.99 / EUR 5622.55. 763669 yalniz 2014-11'den.
- Fed son: G3364 96.74 (2026-10).
- Eurostat son: FR 140.1, DE 145.3, EU27 150.3 (2026-09).
- Airbus/Boeing teslimat 2018-2025 verilen degerlerle birebir eslesti (800/863/566/611/661/735/766/793; 806/380/157/340/480/528/348/600). Fark yok.

## Alinamayanlar
- MSCI World Aerospace & Defense ve (standart) MSCI Europe Aerospace & Defense endeks kodlari bulunamadi (msci.com sayfalari/arama ucu kod vermedi; searchIndexes bos). Tam endeks kodu icin deneme-yanilma taramasi izin disi kaldigindan yapilmadi. Yerine MSCI Europe A&D Capped (763669) proxy olarak indirildi; World A&D icin proxy: ITA/XAR/PPA. Gunluk MSCI verisi alinmadi.
- Dow Jones US A&D / Select Aerospace & Defense gecmisi alinamadi.
- Madde 6 (aylik/ceyreklik Airbus-Boeing teslimat) denenmedi/bulunamadi.
