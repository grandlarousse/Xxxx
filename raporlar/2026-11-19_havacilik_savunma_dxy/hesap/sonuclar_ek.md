# Sonradan eklenen sağlamlık kontrolleri (post hoc)

Bu tablolar önceden belirlenmiş planın dışında, veri kalitesi sorunu görüldükten sonra eklendi. Hüküm verirken ana tablolarla birlikte ve temkinle okunmalı.

## (a) Y6: toplam net sipariş / toplam teslimat (düzey)

Ortalama oran 1.47, medyan 1.38 (1974-2025).

| varyant               | dönem     |   n |   DXY +%10 etkisi (oran puanı) |   GA alt |   GA üst |   Wald p |    R2 |
|:----------------------|:----------|----:|-------------------------------:|---------:|---------:|---------:|------:|
| (i) kontrolsüz        | 1975-2025 |  51 |                         -0.545 |   -0.883 |   -0.207 |    0.002 | 0.144 |
| (ii) +resesyon+imalat | 1975-2025 |  51 |                         -0.612 |   -0.893 |   -0.331 |    0     | 0.286 |
| (iii) +olay yılı      | 1975-2025 |  51 |                         -0.558 |   -0.834 |   -0.281 |    0     | 0.451 |
| (ii) +resesyon+imalat | 1978-1999 |  22 |                         -0.534 |   -0.965 |   -0.103 |    0.015 | 0.289 |
| (ii) +resesyon+imalat | 2000-2025 |  26 |                         -0.758 |   -1.044 |   -0.471 |    0     | 0.413 |
| (ii) +resesyon+imalat | 1986-2025 |  40 |                         -0.723 |   -0.998 |   -0.449 |    0     | 0.275 |

## (b) Y1 toplam teslimat, varyant (ii): başlangıç yılına duyarlılık

| dönem           |   n |   DXY +%10 etkisi (%) |   GA alt |   GA üst |   Wald p |
|:----------------|----:|----------------------:|---------:|---------:|---------:|
| 1975-2025 (ana) |  51 |                -8.186 |  -14.643 |   -1.24  |    0.022 |
| 1986-2025       |  40 |                -1.519 |   -8.777 |    6.317 |    0.695 |
| 1990-2025       |  36 |                 0.176 |   -9.842 |   11.308 |    0.974 |

Küçük örneklem düzeltmeli HAC ve t dağılımıyla Y1 (ii): toplam b = -0.896, p = 0.039, n = 51.

Klasik OLS standart hatasıyla: p = 0.172.

## (c) Y1 (ii): birer yıl dışarıda bırakınca DXY +%10 etkisi

Aralık -10.2% .. -4.9%; p < 0,05 kalan: 47/51; p < 0,10 kalan: 50/51.

En etkili yıllar:

|   dışarıda bırakılan yıl |    etki |     p |
|-------------------------:|--------:|------:|
|                     1985 | -10.212 | 0.007 |
|                     2001 |  -9.073 | 0.011 |
|                     1983 |  -8.949 | 0.027 |
|                     1984 |  -4.93  | 0.247 |
|                     1978 |  -6.816 | 0.035 |
|                     1990 |  -6.855 | 0.049 |

## (d) Özet tablo (rapor için)

| Gösterge                                | Dönem                |   n | DXY +%10 sonrası toplam etki   | %95 güven aralığı   | p      |
|:----------------------------------------|:---------------------|----:|:-------------------------------|:--------------------|:-------|
| Toplam teslimat (Airbus+Boeing)         | 1975-2025            |  51 | -8,2 %                         | [-14,6; -1,2]       | 0,022  |
|                                         | 1986-2025 (sonradan) |  40 | -1,5 %                         | [-8,8; +6,3]        | 0,695  |
|                                         | 2000-2025            |  26 | -5,2 %                         | [-14,7; +5,4]       | 0,327  |
| Airbus teslimat                         | 1975-2025            |  51 | -11,7 %                        | [-20,7; -1,7]       | 0,023  |
|                                         | 2000-2025            |  26 | -4,0 %                         | [-10,2; +2,8]       | 0,243  |
| Boeing teslimat                         | 1975-2025            |  51 | -8,2 %                         | [-16,9; +1,5]       | 0,096  |
|                                         | 2000-2025            |  26 | -4,3 %                         | [-22,9; +18,7]      | 0,687  |
| ABD uçak ve parça üretimi (çeyreklik)   | 1973-2026            | 214 | -3,5 %                         | [-6,8; -0,1]        | 0,044  |
|                                         | 2000-2026            | 107 | -0,5 %                         | [-5,6; +4,9]        | 0,847  |
| Birikim/teslimat oranı (bekleme süresi) | 2000-2025            |  26 | -7,8 %                         | [-16,5; +1,8]       | 0,109  |
| Sipariş/teslimat oranı (ort. 1,47)      | 1975-2025 (sonradan) |  51 | -0,61 puan                     | [-0,89; -0,33]      | <0,001 |
|                                         | 2000-2025 (sonradan) |  26 | -0,76 puan                     | [-1,04; -0,47]      | <0,001 |
