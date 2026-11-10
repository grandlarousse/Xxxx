# Faiz üstü getiri: BIST adayları (ana ajan hesabı, 10.11.2026)

Eleştirmenin taşıma maliyeti itirazı üzerine eklendi. Faiz üstü = işlem getirisi − yıllık faiz × takvim günü / 365 (kısa işlemde tersi).
Faiz serisi yaklaşık yıllık ortalama politika faizidir (elle girildi; kod dosyasında). 2026 için %30 varsayıldı (endeks vadelisi priminden türetildi, teyitsiz).
Bu hesap ikinci bir kodla doğrulanmadı. Veri: Yahoo günlük spot (ek/yeniden_hesap/kod/k1_indir.py ile indirilen).

```
XU030 z>=1 -> XU030 uzun h2                  n= 519 brut=  31.2 | faiz_ustu=  17.3 (t  1.74) | -maliyet5:   12.3 | IS    6.9 (t  0.66) | 2022+   39.3 (t  1.84) | 2024+ n=96   28.6 (t  1.20) | ort.takvim gun 2.89
XU030 z>=1 -> XU030 uzun h3                  n= 458 brut=  51.8 | faiz_ustu=  31.2 (t  2.31) | -maliyet5:   26.2 | IS   22.2 (t  1.48) | 2022+   51.2 (t  1.82) | 2024+ n=82   20.0 (t  0.65) | ort.takvim gun 4.33
KBE z>=1.5 -> AKBNK uzun h2                  n= 232 brut=  77.2 | faiz_ustu=  63.7 (t  2.66) | -maliyet10:   53.7 | IS   59.2 (t  2.20) | 2022+   73.5 (t  1.50) | 2024+ n=40   99.2 (t  1.56) | ort.takvim gun 2.96
KBE z>=1.0 -> AKBNK uzun h2                  n= 490 brut=  48.7 | faiz_ustu=  35.5 (t  2.25) | -maliyet10:   25.5 | IS   30.7 (t  1.85) | 2022+   47.2 (t  1.31) | 2024+ n=85   34.3 (t  0.79) | ort.takvim gun 2.94
TUPRS rafineri z>1 uzun h2                   n= 435 brut=  61.3 | faiz_ustu=  46.1 (t  2.89) | -maliyet10:   36.1 | IS   28.4 (t  1.72) | 2022+   77.1 (t  2.34) | 2024+ n=98   25.6 (t  0.78) | ort.takvim gun 3.02
   ... ve TUPRS o gun artida h2              n= 255 brut=  84.5 | faiz_ustu=  68.8 (t  3.53) | -maliyet10:   58.8 | IS   47.1 (t  2.29) | 2022+  103.0 (t  2.70) | 2024+ n=62   76.5 (t  1.77) | ort.takvim gun 2.98
   ... ve TUPRS o gun ekside/yatay h2        n= 213 brut=  30.3 | faiz_ustu=  15.6 (t  0.64) | -maliyet10:    5.6 | IS   -5.8 (t -0.24) | 2022+   56.9 (t  1.07) | 2024+ n=45  -35.0 (t -0.78) | ort.takvim gun 3.06
TUPRS rafineri z<-1 KISA h2                  n= 427 brut=   5.8 | faiz_ustu=  21.1 (t  1.37) | -maliyet10:   11.1 | IS    6.7 (t  0.39) | 2022+   51.7 (t  1.67) | 2024+ n=91   35.0 (t  1.03) | ort.takvim gun 3.02
TUPRS rafineri z>1 uzun h3                   n= 390 brut=  86.0 | faiz_ustu=  63.7 (t  3.13) | -maliyet10:   53.7 | IS   46.6 (t  2.17) | 2022+   94.7 (t  2.26) | 2024+ n=86   42.7 (t  0.94) | ort.takvim gun 4.49
   ... ve TUPRS o gun artida h3              n= 238 brut= 116.8 | faiz_ustu=  93.6 (t  3.73) | -maliyet10:   83.6 | IS   76.1 (t  2.91) | 2022+  121.2 (t  2.43) | 2024+ n=56   60.6 (t  1.06) | ort.takvim gun 4.42
   ... ve TUPRS o gun ekside/yatay h3        n= 204 brut=  70.0 | faiz_ustu=  48.4 (t  1.73) | -maliyet10:   38.4 | IS   18.6 (t  0.62) | 2022+  106.7 (t  1.85) | 2024+ n=42    6.2 (t  0.10) | ort.takvim gun 4.59
TUPRS rafineri z<-1 KISA h3                  n= 377 brut=  12.7 | faiz_ustu=  35.3 (t  1.80) | -maliyet10:   25.3 | IS   21.8 (t  1.04) | 2022+   64.9 (t  1.53) | 2024+ n=79   52.3 (t  1.19) | ort.takvim gun 4.44
RYGYO z>1 -> RYSAS uzun h1                   n= 589 brut=  57.6 | faiz_ustu=  50.5 (t  3.29) | -maliyet10:   40.5 | IS   17.0 (t  0.98) | 2022+  114.3 (t  3.89) | 2024+ n=109  105.5 (t  2.79) | ort.takvim gun 1.44
XU030 h3 yil yil (n, brut, faiz_ustu): {2011: (24, 30, 23), 2012: (36, 3, -4), 2013: (32, 47, 42), 2014: (27, 13, 1), 2015: (24, 33, 24), 2016: (27, 43, 34), 2017: (35, 9, -3), 2018: (26, 22, -1), 2019: (29, 60, 36), 2020: (23, 84, 72), 2021: (33, 58, 36), 2022: (30, 214, 200), 2023: (30, 13, -12), 2024: (29, 77, 14), 2025: (26, 89, 37), 2026: (27, 48, 11)}
KBE>AKBNK h2 yil yil: {2011: (14, 125, 120), 2012: (15, 56, 51), 2013: (16, -20, -25), 2014: (15, 16, 9), 2015: (16, -28, -34), 2016: (16, 91, 84), 2017: (12, -5, -13), 2018: (11, 97, 80), 2019: (12, 151, 134), 2020: (15, 192, 184), 2021: (17, 92, 79), 2022: (18, 142, 133), 2023: (15, -50, -66), 2024: (14, 196, 151), 2025: (13, -48, -77), 2026: (13, 249, 220)}
```
