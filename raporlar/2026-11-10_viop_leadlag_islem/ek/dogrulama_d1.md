# d1 doğrulama: KCHOL (NAV sepeti) ve SAHOL/AKBNK dönüşü

Kod: kod/d1_holding.py (python3 -I, 5 sn). Sonuç: ek/d1_sonuc.csv (tüm satırlar), d1_islemler_*.csv, d1_durum.csv, d1_uyum.csv, d1_log.txt. Plan v2 tanımları; b1–b4 kodlarına bakılmadı. Plan dışı parametre aranmadı; duyarlılık tabloları olduğu gibi.

Uygulama notları: her çiftte işlemler örtüşmez (çıkış gününde yeni giriş serbest). Brüt = d·Σ fut_ret, bps. t = işlem düzeyi t. net = brüt − bireysel maliyet (KCHOL 23,5; roll'da ikinci gidiş-dönüş; hedge'li bacakta +6). B'de iki bacak tam maliyet (SAHOL 22,5 + AKBNK 22,4). Yön alt kümeleri birleşik işlem listesinden süzüldü. DOYGUN: fark = max(0,|zL|−d·zT)·σ_T, eşik 0,5·fark, en geç 3. gün; K1 vadeli uzlaşma getirisiyle, 1730 spot 17:30 fiyatıyla.

## Yeniden üretim (A, h=2, E0 aksi belirtilmedikçe)
| iddia | verilen | bizim | üretildi |
|---|---|---|---|
| REG S_KUL n / brüt / t | 208 / 71,5 / 3,10 | 197 / 65,0 / 2,8 | evet |
| OOS | 74,1 (2,45) | 79,4 (2,5) | evet |
| E2 | 43,0 | 43,2 | evet |
| KATI_1730 n / brüt (aynı dönem E0) | 61 / 113 (127) | 58 / 104 (128) | evet |
| net bireysel TAM / SON2Y | 45,8 / 111,7 | 39,0 / 95,6 | evet |
| en iyi 10 çıkınca | 32,7 | 26,3 (t 1,3) | evet (%20) |
| REG S_ONCU n / brüt / t; E2; KATI n, brüt | 427 / 49,3 / 2,95; 35,0; 161 / 65,0 | 411 / 44,1 / 2,6; 37,9; 159 / 78,2 | evet (KATI brüt %20 yukarıda) |
| EW S_KUL n / brüt; OOS | 212 / 59,4; 93,1 | 211 / 65,1; 97,1 | evet |
| YKBNK tek öncü n / brüt / t | 252 / 50,5 / 2,46 | 258 / 48,0 / 2,3 | evet |
| TUPRS tek öncü n / brüt; KATI | 262 / 38,3; 5,4 (n 73) | 263 / 36,6; 3,7 (n 72) | n ve TAM evet; KATI ortalaması mutlak 1,7 bps, göreli %31 sapma: sınırda |
| B n / brüt / t | 136 / 70,9 / 2,7 | 135 / 73,6 / 2,9 | evet |
| B OOS; E2 | 80,1 (3,0); 62,9 | 85,1 (3,4); 64,9 | evet |
| B KATI n 40 brüt 74,2 | | 43 / 81,6 | evet |
| B net bireysel | 27,9 | 20,8 | sınırda (%25,5 sapma; maliyet modeli farkı) |
| B SON2Y | +110 (5,0) n=39 | 111,2 (5,0) n=39 | evet |
| B 3 gün sınırlı brüt / net | 34,6 / −5,5 | 36,6 / −12,9 | brüt evet; net işaret aynı, 7 bps düşük |
| SAHOL←AKBNK tek bacak | n 188–198, 36–44, t 1,4–1,7 | 200, 49,7, t 2,1 | sınırda yüksek (üst uca göre %13) |

## A: sade kural ve REG, h=2 E0 (brüt, t; net bireysel)
| | TAM | OOS | SON2Y | E2 TAM | KATI (2023-12→) |
|---|---|---|---|---|---|
| REG S_KUL | 65,0 (2,8); 39 | 79,4 (2,5) | 122 (3,1); 96 | 43,2 (1,7) | 104 (2,5), n 58 |
| SADE | 20,3 (0,8); −5 | 54,0 (1,7) | 141 (3,4); 115 | 32,5 (1,3) | 51 (1,1), n 55 |
| SABİT %1,0 (keşif) | 44,4 (1,6) | 61,0 (1,6) | 127 (2,1) | 45,4 | 90 (1,4) |
| SABİT %1,5 (keşif) | −0,4 | 55,7 | 66 (n 10) | 55,8 | n 8 |

Sade kuralın yıl yıl E0 ortalaması: 2018 −57, 2019 −80, 2020 0, 2021 −16, 2022 −47, 2023 67, 2024 15, 2025 151, 2026 121. REG: 2019 62, 2020 66, 2021 27, 2022 −68, 2023 132, 2024 164, 2025 147, 2026 85 (E2: 2023 −10, 2026 −41).

## Çıkış (E0; TAM brüt/işlem, bps/gün; KATIDON = 2023-12→)
REG: h1 24,4 (24/gün); h2 65,0 (32,5); h3 58,0 (19,3); DOYGUN_K1 50,9 (18,0). KATIDON: h1 96,9/gün; h2 64,0; h3 45,2; DOYGUN_1730 139,3/işlem (60,7/gün, ort. 2,3 gün). SADE: h1 15,8; h2 20,3; h3 33,9; K1 29,0; KATIDON 1730 140,4 (63,6/gün) ve h1 89,5/gün. Yani son 3 yılda en iyi gün başına getiri h1; TAM'da h2. 1730 çıkışı h2'den işlem başına iyi, gün başına benzer.

## Ayrıntılar (REG h2 E0 TAM)
Yön: AL n113 68,4 (t 2,1; ex10 3,5), SAT n84 60,4 (1,8; ex10 −4,5). E1 girişi 63,9 (≈E0). Hedge'li (KCHOL−β·XU030): 33,9 (t 2,3), net 1,9; E2 hedge'li 42,1. Roll'suz n176 56,7; roll'lu n21 134,5 (t 1,8). Ex-temettü ±1 gün çıkarılınca n179 56,0 (t 2,4). 2020–22 çıkarılınca n100 119,1 (t 4,0). Eşik ızgarası (TAM, n/brüt/t): z≥0,75 ve hedef ≤0,25: 295/46,0/2,5; z≥1,5: 88/115,2/3,1; z≥2: 30/128,8/1,7; hedef eşiği 0: 157/62,1/2,4; 0,5: 237/59,7/2,8. Tüm hücreler pozitif; yüksek eşik n küçük, ex10 negatife döner.

## 17:50 uyumu (dk5, 59 gün, 14:45 çubuk kapanışı = 14:50 fiyatı)
| kural | aynı durum | kapanış sinyali | 14:45 sinyali | aynı yön | ters | kaçan |
|---|---|---|---|---|---|---|
| A REG | 51/59 | 8 | 10 | 5 | 0 | 3 |
| A SADE | 54/59 | 11 | 12 | 9 | 0 | 2 |
| B | 58/59 | 20 | 19 | 19 | 0 | 1 |

## B
Tutma (gün): medyan 2, %75 5, %90 10,6, ort 4,3. Bant çıkışı TAM 73,6 (net 20,8); en çok 3 gün: 36,6 (net −12,9); en çok 5 gün: 51,3 (net 1,1; OOS 68,3/net 18,4); en çok 10 gün: 56,9 (net 5,1). SON2Y: n39 111,2 (t 5,0); 5 günden uzun tutulan n5 −54,3 (toplamın %−6'sı); ≤5 gün ort 135,5; en iyi 3 işlem toplamın %25'i. Yani +110 uzun tutulan işlemlerden gelmiyor, tersine kısa işlemlerden. 2024'te −17 (n9), 2018 −85, 2022 −7.

## Bugün (10.11.2026 kapanış)
A REG zL 0,16, zT −2,19: tetik yok. Sade: öncü−XU030 −%0,16 (eşik ±%0,86), KCHOL−XU030 −%2,99: tetik yok (hedef eşiği %0,34). Yarın için eşikler ≈ %0,86 / %0,35. B z=−1,41, β 0,664: tetik yok. Yarın |z|>1,5 için (diğer hisse sabit): spread-AL (SAHOL al, AKBNK sat) AKBNK ≥ 71,09 (bugün 70,70) ya da SAHOL ≤ 86,98 (bugün 87,30); spread-SAT AKBNK ≤ 63,68 ya da SAHOL ≥ 93,58. Fiyatlar Yahoo günlük kapanışı (geçici olabilir).
