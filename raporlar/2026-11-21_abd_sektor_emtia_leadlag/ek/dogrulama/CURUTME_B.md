# Çürütme B: S3–S8 ve ek adaylar (22.11.2026)

Betik `kod/curutme_b.py`; çıktılar `ek/dogrulama/curutme_b/`. Taban satırlar raporlananla birebir tuttu. Sayılar: sürüklenme düzeltilmiş net bps, t IS / OOS.

| Sinyal | Hüküm | 20.11 kapanışı |
|---|---|---|
| S3 sigorta-borsa SAT | kullanılamaz | sinyal yok |
| S4 temel tüketim AL | kullanılamaz | yalnız CELH açık (kullanma) |
| S5 crack → VLO | koşullu (yalnız VIX ≤ 20) | kapalı (z −0,76; VIX 35,9) |
| S6 MU → WDC | koşullu (küçük boy) | yeni sinyal yok (z −0,82); 19.11 AL'si 24.11'e kadar açık |
| S7 soya yağı → BG/ADM | kullanılamaz (izleme adayı) | sinyal yok |
| S8 crack → PBF | kullanılamaz | sinyal yok |
| IYR SAT, EWJ AL | kullanılamaz | sinyal yok |

## S3
- Aynı kural 37 hisse grubunda: abn medyanı +14 bps, OOS t ortalaması +0,10; eşiği geçen tek grup bu. 8.673 portföy testinden seçildi.
- Komşu tanımlar tutmuyor: eşik 1,25'te OOS t 1,25; 1,75'te IS t 1,29; z penceresi 40'ta 1,63 / 1,93. En iyi yıl (2008) hariç IS t 1,15.
- Açığa satış ister; grubun ters ETF'i yok.

## S4
- IS tümüyle CELH'ten geliyor: CELH hariç IS t **0,25** (9 bps). CELH 2018'e kadar 0,67 $'lık, günde 0,02 mn $ dönen bir hisseydi; alınamazdı (hayatta kalma yanlılığı).
- CELH hariç OOS 19 bps, t 2,1; en iyi 10 gün de çıkınca 1,3. Eşik 1,0'da OOS 2 bps.

## S5
Destek:
- Öncüye özgü: ham petrol, Brent, XLE, XOM etki vermiyor; benzin marjı tek başına veriyor (36 bps; 3,45 / 2,37).
- Öncü 1 gün gecikince 10 bps (1,00 / 0,63). Hedefin aynı gün tepkisi kontrol edilince t 3,5 / 2,6.
- Sekiz rafinerinin sekizi pozitif (9–56 bps); entegre petrol ~5 bps.
- Ertesi açılış girişi 26 bps (2,86 / 1,72); gece payı ~2 bps: 16:00 sonrası vadeli bilgisine dayanmıyor.

Karşı:
- VIX > 20'de yok (0,03 / 0,94); VIX ≤ 20'de 35 bps (3,15 / 2,43).
- En iyi 10 işlem hariç OOS t 1,17; maliyet iki kat 1,99 / 1,81.
- **Hedge'siz AL: 38 bps, 2,31 / 1,35**; en iyi 10 hariç 22 bps (1,62 / 0,61).

Kural: crack z ≥ 1 ve VIX ≤ 20 ise VLO al, 2 gün tut. Beklenti 15–30 bps/işlem (2 günlük oynaklık ~%3,5), yılda ~20 işlem. Yalnız AL sürümü OOS'ta kanıtlanmış değil.

## S6
Destek:
- Önceden yazılı hipotez. Tüm örneklem t 4,4; IS 3,74 ile OOS 2,43'ün birlikte şansla beklenen sayısı 4.854 testte ~0,003.
- 59 yarıiletken/donanım öncüsü ve 99 rastgele hisse arasında MU 1. sırada; başka hiçbiri IS ve OOS t ≥ 2 vermiyor. 60 hedefte WDC 1. Ters yön sıfır.
- Aynı gün tepkisi kontrol edilince t 4,5 / 2,6. WDC o gün tepki vermediyse 69 bps, verdiyse 34 (yetişme deseni).
- Pencere, eşik, beta, kriz, sınır, en iyi 10 (3,07 / 1,98), ertesi açılış (41 bps; 3,24 / 1,90) testlerinde sürüyor.
- S2'nin parçası değil: S2'siz günlerde 42 bps (2,68 / 2,00); korelasyon −0,05.

Karşı:
- **Hedge'siz AL: 52 bps, 0,98 / 1,71** (tüm 1,99); en iyi 10 hariç 21 bps (0,46 / 0,84). IS'i SAT bacağı taşıyor.
- SMH'den arındırınca 32 bps (2,58 / 1,59): etkinin ~%40'ı sektör hareketi.

Kural: MU'nun SPY'dan arındırılmış getirisi z ≥ 1 ise WDC al, 3 gün tut. Beklenti 20–50 bps/işlem (oynaklık ~%5), yılda ~33 işlem.

## S7
- OOS içinde sağlam: eşikle büyüyor (26 → 36 → 63 bps), en iyi 10 hariç t 3,5, ertesi açılış t 2,6. ZS=F ve SOYB de veriyor; mısır, buğday, petrol vermiyor.
- Rejim açıklaması kısmen destekli: BG'nin aynı gün korelasyonu 0,01 (2013–18) → 0,33 (2024–26). Ama etki 2022'de başlıyor (2019–21: 9 bps, t 0,9); 2013–18 negatif (t −2,1).
- F1'de "IS yok, OOS t ≥ 2,5" çıkan test sayısı şansla beklenenden fazla değil (15–21'e karşı ~22). OOS t 3,6'nın 3.600 testte şansla çıkma olasılığı ~%40.
- **Hedge'siz AL: BG OOS 17 bps (t 1,55), ADM 17 (1,71).** Güçlü taraf SAT.

## S8
- IS'te yok; OOS 2022–23'ten (234 bps) geliyor. Aynı öncüyle VLO'da 2022 sonrası artış yok (22–23 bps; öncesi 33–54): rejim açıklaması tutarsız.
- Hedge'siz AL: OOS 115 bps (t 1,79); en iyi 10 hariç 30 bps (0,57).

## Ek adaylar
- IYR: n 64; en iyi 10 hariç IS t 0,62.
- EWJ: SPY'dan arındırınca OOS −1 bps; VIX ≤ 20'de OOS 4 bps. S1 kümesinin parçası.

## Açık kalanlar
- Yahoo vadeli kapanışı uzlaşma mı (14:30) son işlem mi (17:00), günlük veriyle ayrılamıyor.
- ZL=F'in CF, MOS, PSX, VLO, XOM'u da OOS'ta öngörmesinin mekanizması belirsiz.
- Bilanço günleri ayrıştırılmadı; vade geçişi günleri yaklaşık tanımlandı.
