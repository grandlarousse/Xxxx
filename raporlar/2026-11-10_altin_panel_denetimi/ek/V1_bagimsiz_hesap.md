araç: 8/20

# V1 bağımsız hesap (kod: kod/V1/v1.py, v1b.py; çıktı: hesap/V1/v1_log.txt, v1b_log.txt, reg_cases.csv, trades_*.csv)

Not: K1/K2 kodu ancak kendi hesabım bittikten sonra okundu. Birim: bps. t = işlem başına basit t (maddeler 1-4), Newey-West gecikme 4 (madde 5).

## 5 sayı

| no | K1/K2 sayısı | benim sayım (şartnameye birebir) | fark | karar |
|---|---|---|---|---|
| 1 A2 k2 düşük | n 408, +43,2, t 2,55 | n 408, +42,6, t 2,55 | -0,6 | doğrulandı |
| 2 R1 brüt | +34,5 | +33,3 | -1,2 | küçük fark |
| 2 R1 bireysel net | +11,5 (t 0,58) | +10,3 (t 0,53) | -1,2 | küçük fark |
| 2 en iyi %2 çıkınca | -12,7 (9 işlem) | -12,6 (9 işlem); 8 işlemde -10,5 | ~0 | doğrulandı |
| 2 rejim 2019-20 / 21-23 / 24-26 | +52,6 / -66,5 / +49,9 | +46,3 / -62,2 / +47,5 | -6,3 / +4,3 / -2,4 | küçük fark, işaretler aynı |
| 3 R2 (A3) bireysel | +2,6 (t 0,13), n? | +0,7 (t 0,04), n 399 | -1,9 | doğrulandı (sıfır) |
| 4 R3a (B1) brüt / bireysel | +8,2 / -1,8 (t -0,23) | +6,2 / -3,8 (t -0,48) | -2,0 | küçük fark, sıfır |
| 5 d tüm / <2022 / ≥2022 / ≥2024 | 30,2 (3,38) / t 4,29 / 1,56 / 1,50 | 29,1 (3,32) / 4,16 / 1,47 / 1,40 | -1,1 | doğrulandı |

Fark nedeni (kanıtlı): K1/K2 çıkış günü TRALT limit günüyse çıkışı 1-3 gün erteliyor (k2.py:81, k1_prep.py:60); şartnamede yok. Bunu ekleyince (v1b) A1 brüt +34,5, bireysel +11,5 (t 0,58) ve A2 +43,2 (t 2,55) birebir çıkıyor. Yani 1 ve 2 aynen yeniden üretildi; R2/R3a/rejim farkları aynı ve benzeri kaynaklı (A3 ve B1 için ayrıca denemedim).

## Çürütme (madde 5, d = bps/σ; <2022 / ≥2022 / ≥2024 parantezde t)

| test | tüm (t) | <2022 | ≥2022 | ≥2024 |
|---|---|---|---|---|
| baz (A3,k3,eGDXJ) | 29,1 (3,32) | 4,16 | 1,47 | 1,40 |
| a) d*+1 plasebo (t günü seansı) | 18,2 (2,43) | 2,07 | 1,48 | 0,81 |
| a) d*-1 plasebo | 21,7 (1,71) | 46,5 (2,19) | 0,41 | 0,03 |
| b) 2019 at | 32,5 (3,62) | 4,27 | 1,47 | 1,40 |
| b) yalnız 2020-07+ | 24,4 (1,70) | 0,76 | 1,47 | 1,40 |
| c) winsor %1-99 | 28,9 (3,40) | 4,24 | 1,56 | 1,50 |
| c) en büyük 10 |y| at | 28,5 (3,32) | 4,05 | 1,81 | 1,79 |
| d) A1 k1 | 19,7 (2,98) | 2,18 | 2,13 | 0,89 |
| d) A1 k2 | 30,6 (2,62) | 2,55 | 1,87 | 1,42 |
| d) A1 k3 | 35,2 (2,85) | 4,54 | 1,15 | 1,07 |
| d) e_GDX, A3 k3 | 13,0 (1,19) | 2,04 | 0,21 | 0,79 |
| d) e_GDX, A1 k3 | 15,5 (1,36) | 1,13 | 0,75 | 1,13 |
| e) hedef F_XU030 k3 | 25,6 (4,02) | 6,22 | 1,64 | 0,54 |
| e) aynısı, kontrol XU030'un kendi r'si | 25,6 (4,10) | 6,40 | 1,66 | 0,53 |

Okuma: (a) ileriye bakma izi yok: d*+1 daha güçlü değil (18 < 29). Ama d*-1 de tam sönmüyor (<2022'de 46,5, t 2,19): etki "son seans" özgül değil. (b) 2019 sorun değil; 2020-07+ t 1,70'e düşüyor, <2022 dilimi 0,76. (c) aykırı değerden değil. (d) A1'de de var, e_GDX'te yok: etki GDXJ'ye özgü. (e) En kötü sonuç: ilgisiz hedef XU030'da etki aynı büyüklükte ve daha anlamlı (t 4,02; <2022 t 6,22). Mekanizma TRALT'a özgü değil, ortak bir risk faktörü ya da dönem artefaktı gibi.

**Karar: kırılgan, muhtemelen sahte (para kararına temel yapma).** Gerekçe: ≥2022'de ve ≥2024'te anlamsız (t 1,5), kazanç 2020-21 dönemine yaslı; ilgisiz hedefte aynı sinyal; d*-1 plaseboda sönmüyor; K1 yaklaşık 19 öngörücü x 3 hedef x 3 ufuk denedi (kaba Bonferroni eşiği |t|>~3,6; baz t 3,32 geçmez). Doğrudan bir ileriye bakma yok.

## Kod incelemesi (k2.py, k1_prep.py, k1_reg.py)

- Hizalama doğru: d* = t'den kesin önceki ABD günü (k1_prep.py:121-123), tekrar eden d* NA (123-124), betalar ve σ shift(1) (k1_reg.py:11-14; k2.py:48,54,58), spot beta ffill sonra shift(1) sızdırmıyor. Hedef t+1..t+k günlerini topluyor (k1_prep.py:62, k2.py:35), t günü getirisi hedefe sızmıyor. Maliyet katsayıları doğru (k2.py:60,94). Örtüşme: çıkış gününde giriş serbest, doğru (k2.py:66,82).
- Hata/sapma 1 (şartname dışı, çıkış ertelemesi): k2.py:81 ve k1_prep.py:60,99: çıkış günü limit günüyse çıkış ertelenir. Giriş sinyalinde sızıntı değil ama çıkış getirisi sonuca göre seçiliyor; etkisi ~+1,2 bps brüt (R1: 33,3 -> 34,5). Sonucu değiştirmez.
- Sapma 2 (ayar): k2.py:112-116 min_periods'i n=405-423 çıkana dek deniyor; yani n=408 hedefe uydurulmuş seçim. Benim şartname hesabım (60) zaten n=408 verdi, sonuç etkilenmedi.
- Sapma 3: K1 σ/β için min_periods=100 (k1_reg.py:11,14), şartnamede 60; rTz √d'ye bölünmüyor (k1_reg.py:18); A3 için XAU hacmi>0 şartı ekli (k1_reg.py:56); eGDXJ getirisi kapanış (c) üzerinden (k1_prep.py:129), şartname adj diyor. Etki: d farkı ≤1,1 bps.
- Bakılmadı: gdxT / saatlik anlık fiyat (o1430) kısmı, 5 sayıda kullanılmıyor.

## Açık kalanlar
- R2/R3a/rejim farkı çıkış ertelemesiyle doğrudan denenmedi.
- Madde 2 rejim t'leri, bootstrap ve K1 FDR/plasebo bölümü (k1_reg.py 130-249) okunmadı.
- d*-1 plasebonun neden sönmediği (eGDXJ ile gizli ortak faktör) araştırılmadı; eGDXJ ile g_z korelasyonu 0,02, eGDXJ(d*) ile eGDXJ(d*-1) -0,10.
