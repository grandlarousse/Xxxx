# F3 çapraz varlık: not (21-22.11.2026)

Betik: `kod/f3_capraz.py` (ara sonuçlar `ara/`).

## Test sayısı ve beklenen yanlış pozitif
- Özel öncüler (bu betik): 1.110 test = 867 hipotez testi + 243 B1r (piyasadan arındırma) testi. 9'u keşif (yeni dip eşiği ajan seçimi: 250 günlük %95'lik). Beklenen yanlış pozitif: SAĞLAM 0,034, KOŞULLU 0,12.
- cift_motoru F3 satırları: 2.487 test (1.917 hipotez testi). Beklenen yanlış pozitif SAĞLAM 0,075, KOŞULLU 0,27.
- F3 toplamı: 2.784 hipotez testi; beklenen SAĞLAM 0,11, KOŞULLU 0,39.

## Eleme
- Özel öncüler: IS t ≥ 2,5 (A koşulu) geçen **0**. IS t ≥ 2,0 ve OOS t ≥ 1,5 olan (İZLE) **0**. Hepsi ELENDİ.
- cift F3: 2 İZLE, 0 KOŞULLU, 0 SAĞLAM. İkisi de çürütme testlerinde zayıfladı:
  - ^TNX → NLY (B1, h=1): öncüye özgü değil (B1r ölçütü). SPY'dan arındırılınca t 1,98. Ertesi açılıştan girişte 6,8 bps (t 1,35). 1 gün geç girişte −12 bps (t −2,1). Etki yalnız VIX > 20 olan günlerde ve 200 günlük ortalamanın altında. 2008 çıkarılınca t 1,7. SON dönem neti −5,1 bps.
  - UUP → PCAR (B2, h=3): kontrol regresyonunda OOS t 0,53. Bu bir artık dönüşü, öncüye özgü değil.
- Eşiğe yakın adaylar (`yakin_adaylar.csv`; sınıf almıyor): yalnız VIX 5 günlük sıçraması (z ≥ 2) → SPY, QQQ, XLK, h=1-2. Ortalama 40-60 bps, IS t 1,6-1,9, OOS t 1,1-1,6. Zayıf yanları:
  - VIX 1 gün gecikmeyle kullanılınca t 0-0,5'e düşüyor (VIX 16:15 ET'de kapanıyor).
  - Ertesi açılış girişinde kazancın yarısı gidiyor.
  - SPY'ın kendi günlük ve 5 günlük getirisi kontrol edilince t: IS 1,4, OOS 0,9.
  
  Sonuç: piyasanın kendi aşırı satışının dönüşü. Öncü bilgisi değil.

## Hipotezle çelişenler
- **VIX/VIX3M > 1 (ters yapı) AL:** 84 bağımsız dönem (IS 57, OOS 28). Hedeflerin hiçbirinde t > 1 yok. SPY h=1 IS t −0,16, OOS 0,05. Hipotezdeki "karşıt yönde getiri" desteklenmiyor.
- **VIX9D/VIX > 1,1:** IS'te pozitif, OOS'ta negatif (SPY OOS t −0,6).
- **VIX > 20/25/30/35 AL:** koşullu ortalama getiri yükseliyor. Örnek: VIX > 35'te SPY h=1 IS'te +16, OOS'ta +49 bps fark. Ama oynaklık 2,5-3,3 kat artıyor. t hiçbir yerde 1,3'ü geçmiyor. VIX > 35 yalnız 19 bağımsız dönemden oluşuyor (IS 10, OOS 9).
- **HYG kuyruğu sonrası AL:** OOS'ta negatif (IWM h=1 −17 bps, t −1,0). Zayıf da olsa "kredi stresi sürer" yönünde.
- **Genişlik < %20 / < %10 AL:** IS t ≈ 1,0, OOS t 0,1-1,1. Anlamsız.
- **Kripto ETF → madenciler:** IBIT/BITO yalnız OOS'ta var. OOS t ≤ 1,5. Ön testteki "öncülük yok" doğrulandı.
- **Ters yönde tutarlı 14 satır** (`ters_yon.csv`, sınıf almıyor). Hepsi B1r: risk iştahı farkının artığı yükselince ertesi gün QQQ/XLY'nin SPY'a göre artığı düşüyor (7-13 bps). En güçlüsü ^TNX → IGV B1r (IS t −7,9). IGV 2015'e kadar günde < 5 mn $ işlem görüyordu; bu satır büyük olasılıkla bayat kapanış yanılgısı.

## Veri sorunları
- Genişlik ölçüsü bugünkü 628 hisseden kuruldu. Hayatta kalma yanlılığı var; 2005'te geçerli hisse sayısı daha az.
- CPER bayat kapanışlı. CPER−GLD farkı öncü olarak kullanıldı, hedef olarak değil.
- 5 dakikalık veri yok. Bölüm 7.10 (15:50 ile 16:00 sinyalinin örtüşmesi) yapılmadı.

## Rejim tablosu (`rejim_tablosu.csv`)
Brüt, maliyetsiz, betimsel. Koşullu ve koşulsuz ortalama, isabet ve oynaklık oranı; IS / OOS / SON ayrı.
- Panik koşullarında ortalama yukarı, oynaklık 1,5-3,5 kat, isabet en çok 2-10 puan artıyor. SON dönem 3-25 günlük; yorumlanamaz.

## 20.11.2026 kapanışı (`son_degerler.csv`)
- Açık koşullar: VIX 35,9 (> 20/25/30/35), VIX/VIX3M 1,16 (4 gündür), VIX9D/VIX 1,13, VIX z5 2,57, genişlik %9,9 (< %10), yeni dip oranı %61 (eşik %28,5).
- HYG kuyruğu kapalı: 5 günlük −%0,80, eşik −%0,82.
- İki İZLE sinyali de açık: NLY AL (^TNX −14 bp, z −2,6) ve PCAR AL. Ama ikisi de çürütmede zayıf.
