# V7 — araçlar (20.11.2026)

## Ne üretildi (`araclar/`)

- `sinyal.py`: İş Yatırım'dan XELKT, XU030, XU100 ve 42 hisseyi çeker; S1, S2, S3 durumu, yarının tetik düzeyleri, dolabilir sepet (likidite sırası, TradingView kodu, fiyat, adım, medyan hacim), kaçınma listeleri ve T2 listesi.
- `dogrula.py` ve `dogrulama_sonucu.txt`: betiği kural kodlarıyla karşılaştırır.
- `elektrik_sinyal.pine` (XELKT grafiği: S1, S2, S3, alarmlar, tetik çizgileri) ve `hisse_sektor_fark.pine` (hisse − XELKT, ≤ −5 puan “ALMA”).
- `izleme_listesi.txt`: 3 endeks, 4 vadeli, 42 hisse; hepsi doğrulanmış kod.
- `KULLANIM.md`, `ornek_cikti_2026-11-20.txt`, `ornek_hisse_2026-11-20.csv`.

## Doğrulama (son 400 işlem günü, 2025-04-17 → 2026-11-20)

- S1 86 gün, S2 58 gün, S3 19 gün: kural kodlarıyla fark 0. Ham dosyalarda ve canlı indirmede aynı.
- Hisse düzeyi: sepet 14.880, 5 puan geride 518, en kötü beşte birlik 2.863, tabana değen 390, T2 2.268 hücre; fark 0.
- Varsayılan 450 günlük pencere, uzun pencereyle aynı sonucu veriyor (son 150 gün, fark 0).

## Bulgu: İş Yatırım günlük endeks serisinin son günü güvenilmez

Aynı istek 20.11 için XELKT'de 537,06 / 539,06 / 539,83 / 545,14, XU030'da 13.957,13 / 13.976,42 / 14.010,74 döndürdü; 8 XU030 isteğinin 5'inde gün hiç yoktu. Saatlik serinin 18:00 değeri 14 istekte değişmedi ve son 400 günün 395'inde günlük kapanışla aynı (5 günde 18:00 damgası yok). Betik son 10 günü bu değerle düzeltir ve NOT satırı yazar. Panelin son günü doğru (537,06). Hisse ucu üç indirmede aynıydı (12.106 satır).

## Bilinen sınırlar

- Pine kodları derlenmedi; iki kez satır satır gözden geçirildi.
- `--gunici` yalnız endeks sinyallerini günceller; hisse listeleri son kapanışa göredir.
- Uç noktaların seans içindeki ve 18:10'daki davranışı sınanmadı (koşular gece yapıldı). Yarım günlerde 18:00 damgası yok; betik uyarır.
- Üye listesi sabit (42 hisse). T1 (model) araçlarda yok.
- Betik Yahoo yamalarını ve temettü tarihlerini kullanmaz; son 400 günde fark doğurmadı.

## Bugünün çıktısı (2026-11-20)

```
==========================================================================
ELEKTRİK SİNYALİ | 2026-11-20 Cuma | kaynak: İş Yatırım
==========================================================================
ENDEKSLER
  XELKT     537,06  günlük  %-2,33  z  -1,11  (60 g. std %2,09)
  XU030  13.957,13  günlük  %-2,40  z  -1,29  (60 g. std %1,86)
--------------------------------------------------------------------------
S1  XELKT 20 günlük en yüksek kapanış: HAYIR
      kapanış 537,06; eşik 571,59 (uzaklık %-6,04)
S2  XELKT z >= 1: HAYIR
      z -1,11; eşik getiri %+2,09 = XELKT 561,35
S3  XU030 z >= 1 ve XELKT z < 0,5: HAYIR
      XU030 z -1,29 (eşik getiri %+1,86); XELKT z -1,11 (üst sınır %+1,05)
--------------------------------------------------------------------------
YARIN İÇİN TETİK DÜZEYLERİ (yarın kapanışta; bugünkü değerlere göre)
  S1: XELKT >= 571,59  (%+6,43)
  S2: XELKT >= 548,31  (%+2,09)
  S3: XU030 >= 14.220,17  (%+1,88)  ve  XELKT < 542,68  (%+1,05)
--------------------------------------------------------------------------
SEPET: dolabilir 40 hisse (likiditeye göre sıralı) | eşit ağırlıklı sektör %-1,87
  #  TradingView    fiyat  adım  hacim   gün    fark  not
                      TL   bps  mn TL     %    puan
   1 BIST:ENERY     14,45     7    667   -2,5   -0,6  
   2 BIST:CWENE     16,71     6    567   -1,6   +0,3  
   3 BIST:AKSEN     63,80     8    396   -4,6   -2,7  en kötü 1/5, VİOP
   4 BIST:ENJSA    111,60     9    378   -1,4   +0,5  T2, VİOP
   5 BIST:MAGEN      4,62    22    257   -9,9   -8,1  KAÇIN-5, en kötü 1/5, taban
   6 BIST:AHGAZ     43,80     5    219   -3,0   -1,1  
   7 BIST:ODAS       4,35    23    217   -3,3   -1,5  VİOP
   8 BIST:CANTE      0,93   108    208   -2,1   -0,2  
   9 BIST:METEN     20,18    10    189   -3,1   -1,2  
  10 BIST:HUNER      3,69    27    145   -1,9   +0,0  
  11 BIST:MASFN     31,04     6    129   -3,4   -1,6  
  12 BIST:AKFYE      2,77    36    128   -3,5   -1,6  
  13 BIST:BESTE     15,35     6    105   -5,9   -4,1  en kötü 1/5
  14 BIST:IZENR      3,84    26    102   -4,5   -2,6  en kötü 1/5
  15 BIST:SMRTG      4,06    25    100   -3,8   -1,9  
  16 BIST:VEYAS     73,50     7     97   -3,5   -1,6  
  17 BIST:ZOREN      1,38    72     92   -2,8   -1,0  
  18 BIST:BIOEN     14,24     7     90   -1,3   +0,5  
  19 BIST:MOGAN      8,31    12     87   -4,6   -2,7  en kötü 1/5
  20 BIST:TATEN      3,75    27     79   -2,8   -1,0  
  21 BIST:KLYPV     48,80     4     79   -2,9   -1,0  
  22 BIST:ECOGR     18,60     5     71   -2,1   -0,2  
  23 BIST:AYDEM     19,44     5     53   +1,8   +3,6  
  24 BIST:GWIND     18,46     5     51   -1,8   +0,1  T2
  25 BIST:ENTRA      4,49    22     47   +0,2   +2,1  T2
  26 BIST:ALFAS     21,52     9     41   -4,2   -2,3  en kötü 1/5
  27 BIST:ESEN       1,98    50     40   -1,5   +0,4  T2
  28 BIST:AKSUE     12,67     8     39   -2,5   -0,7  
  29 BIST:ARFYE     11,51     9     35   +2,8   +4,6  
  30 BIST:NTGAZ      8,11    12     33   -1,7   +0,2  T2
  31 BIST:ENDAE      9,07    11     32   -2,5   -0,6  
  32 BIST:ARASE     54,10     9     29   -2,3   -0,5  
  33 BIST:AKENR      6,14    16     28   -1,6   +0,3  T2
  34 BIST:A1YEN      1,41    71     25   -1,4   +0,5  T2
  35 BIST:NATEN      2,90    34     22   -4,3   -2,4  en kötü 1/5
  36 BIST:LYDYE  2.902,50     9     16   +7,5   +9,4  
  37 BIST:AYEN      22,70     9     10   -1,0   +0,8  T2
  38 BIST:PAMEL     38,52     5      9   -3,8   -1,9  
  39 BIST:CONSE      1,33    75      8   -4,3   -2,4  en kötü 1/5
  40 BIST:ZEDUR      4,09    24      6   -3,1   -1,2  
  Sepet dışı: CATES (tavanda kapandı), BIGEN (tavanda kapandı)
--------------------------------------------------------------------------
KAÇINMA (bu hisseleri bugün kapanışta ALMA; 1 günlük)
  Sektörden >= 5 puan geride: MAGEN (-8,1)
  Günün en kötü beşte birliği: MAGEN (-8,1), BESTE (-4,1), MOGAN (-2,7), AKSEN (-2,7), IZENR (-2,6), CONSE (-2,4), NATEN (-2,4), ALFAS (-2,3)
  Tabana değen: MAGEN (tabanda kapandı)
--------------------------------------------------------------------------
T2 SAKİN VE GÜÇLÜ (1 gün, sektöre göre; maliyet sonrası ~0: yalnız seçim yardımcısı)
  ENJSA (gün -1,4, oynaklık 2,7), GWIND (gün -1,8, oynaklık 2,4), ENTRA (gün +0,2, oynaklık 2,8), ESEN (gün -1,5, oynaklık 3,4), NTGAZ (gün -1,7, oynaklık 2,4), AKENR (gün -1,6, oynaklık 3,1), A1YEN (gün -1,4, oynaklık 3,7), AYEN (gün -1,0, oynaklık 2,2)
```
