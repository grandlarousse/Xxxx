# Bağımsız yeniden üretim (S1–S8)

Betik: `kod/yeniden_uretim.py` (ortak.py / cift_motoru.py / f*.py okunmadı; evren.py'den yalnız grup listeleri `ast` ile alındı). Süre ~7 sn.
Çıktılar: `yeniden_uretim.csv` (ana), `yeniden_uretim_yillik.csv`, `yeniden_uretim_uc_islemler.csv`; `*_tamgecmis.csv` = göstergeler 2000'den ısıtılmış yorum.

## Sonuç
Tüm raporlanan sayılar ölçüt içinde **yeniden üretildi** (n, sürüklenme düzeltilmiş net, t IS/OOS). İki tanım ayrıntısı uyuşmayı belirliyor:
1. **Sürüklenme "dönem içi"**: IS işlemlerinden IS ortalaması, OOS işlemlerinden OOS ortalaması çıkarılıyor. Tüm örneklem ortalaması kullanılırsa S2'nin IS t'leri 2,54 / 2,45 / 2,16'ya düşer (A ölçütü 2,5 sınırında ya da altında).
2. **Göstergeler 2005-01-01'den başlıyor** (beta, sd, 200g ortalama ısınması 2005 içinde). 2000'den ısıtılınca S4/S5/S6/S7'de n %3 artar; S5 t IS 2,51 -> 3,03.

| sinyal | n | dadj net bps | t IS / OOS | rap. | durum |
|---|---|---|---|---|---|
| S1 IBB VIX25 h2 | 238 | 79,1 | 2,70/2,59 | 238, 79,1, 2,70/2,59 | UYUŞUYOR |
| S1 IJR VIX20 h1 | 479 | 37,2 | 3,26/2,19 | 479, 37,2, 3,26/2,20 | UYUŞUYOR |
| S1 EEM VIX20 h1 | 437 | 50,1 | 3,38/2,08 | 438, 50,0, 3,38/2,09 | UYUŞUYOR |
| S1 IBB VIX20 h2 | 446 | 47,7 | 2,58/2,24 | 446, 47,7, 2,58/2,23 | UYUŞUYOR |
| S1 XBI VIX20 h2 | 456 | 64,6 | 2,15/3,39 | 456, 64,5, 2,15/3,39 | UYUŞUYOR |
| S2 VIX25 h1 | 742 | 62,0 | 2,70/2,84 | 742, 61,6, 2,70/2,83 | UYUŞUYOR |
| S2 VIX20 h1 | 1525 | 35,0 | 2,73/2,69 | 1525, 34,4, 2,73/2,65 | UYUŞUYOR |
| S2 VIX20 h2 | 1524 | 50,4 | 2,54/2,44 | 1524, 49,5, 2,54/2,42 | UYUŞUYOR |
| S3 SAT h2 | 485 | 80,4 | 2,58/2,52 | 485, 80,3, 2,58/2,52 | UYUŞUYOR |
| S4 AL h1 | 1354 | 41,6 | 3,00/2,06 | 1354, 41,6, 3,00/2,06 | UYUŞUYOR |
| S5 VLO h2 | 1364 | 27,5 | 2,52/1,97 | 1365, 28,4, 2,51/2,11 | UYUŞUYOR |
| S6 WDC h3 | 1444 | 50,5 | 3,74/2,43 | 1444, 50,9, 3,74/2,43 | UYUŞUYOR |
| S7 BG h1 | 1639 | 8,4 (OOS 26,0) | -0,41/3,63 | 8,2 (26,0), -0,47/3,63 | UYUŞUYOR |
| S7 ADM h1 | 1639 | OOS 24,8 | -0,16/3,44 | OOS 24,8, t OOS 3,44 | UYUŞUYOR |
| S8 PBF h3 | 885 | 67,8 (OOS 98,3) | 1,14/2,56 | 890, 73,9 (108,7), 1,12/2,82 | UYUŞUYOR (sınırda) |

S1 İZLE listesi (QQQ, XLK, SMH, SOXX, IWM, IWO, KRE, XRT; 48 satır): n ve ortalama birebir, t farkı tümü-örneklem sürüklenmesiyle en çok 0,5 (dönem içi sürüklenme farkı açıklıyor).

## Sağlamlık (yeniden üretimin ötesinde, sonuca etkili)
- **S4 IS kanıtı CELH'den geliyor.** CELH 2007–2013'te tezgâh üstü kuruş hisse (hacim 0 günleri, 2009-12-24 ters bölünme gününde bozuk düşük fiyat 0,75). En büyük 10 kazancın 10'u CELH. CELH hariç: t IS 0,26, OOS 2,12, net 9,4 bps. Dolar hacmi >= 5 mn $ filtresiyle t IS 0,25. -> A ölçütü düşer.
- **S2 IS kanıtı likit olmayan hisselerden geliyor.** Dolar hacmi >= 5 mn $: t IS 2,13 / 1,22 / 1,04 (VIX25h1, VIX20h1, VIX20h2), >= 20 mn $: 1,96 / 1,63 / 1,21. OOS 2,3–3,1 ile ayakta. Uç işlemler ACLS/NVMI 2009 (düzeltilmiş fiyat < 1 $, kapanış = gün dibi, hacim 0–300 adet).
- **S3** AIG hariç güçleniyor (t IS 3,60, OOS 2,24). AIG 2009 hareketleri gerçek; bölünme düzeltmesi tutarlı.
- **S7 ADM** OOS'un en büyük işlemi 2024-01-19 (CFO skandalı, -%24): hariç OOS 20,9 bps, t 3,45.
- **S8** 2020: -223 bps/işlem; kazanç 2021–2023'te yoğun. IS t 1,1 (aday).
- **S1**: veri hatası bulunmadı; IBB VIX25 2019 tek işlem (850 bps).

## Açık şüpheler
- Enerji vadelilerinin Yahoo "close" saati doğrulanmadı (NYMEX 17:00 ET'ye kadar işlem görür). Kapanış 16:00 sonrası fiyatsa S5/S8 ileri bakış içerir; özgün F1 kontrolünde 1 gün gecikmeli öncü t'yi 0,5–1,0'a düşürüyor.
- Grup listeleri bugünün üyeleri (hayatta kalma yanlılığı; S2, S4).
