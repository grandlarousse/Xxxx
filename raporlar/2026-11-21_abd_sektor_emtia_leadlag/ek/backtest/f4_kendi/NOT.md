# F4: aracın kendi fiyatıyla dönüş ve momentum kuralları

Betik: `kod/f4_kendi.py`. Üç çalıştırmada bitti ve her seferinde kaldığı yerden sürdü. Verinin son günü 20.11.2026.

## Test sayısı ve beklenen yanlış pozitif
- **51.086 test.** Bunların 42.413'ü tek ETF testi (186 ETF), 8.658'i hisse grubu portföyü (40 grup), 15'i kesitsel kural.
- Bağımsızlık varsayımıyla beklenen yanlış pozitif: **SAĞLAM 2,0, KOŞULLU 7,2.** Testler iç içe koşullardan oluştuğu için bu sayı kabadır.
- **Eleme adımları:**
  - IS t ≥ 2,5 olan 404 test var. Hiçbir etki olmasa beklenen sayı 317'ydi.
  - Bunlardan OOS t ≥ 2,0 olan 15, OOS t ≥ 2,5 olan 4.
  - BH düzeltmesini geçen yok.
- **Sınıflar:** SAĞLAM 0, KOŞULLU 14, İZLE 116. KOŞULLU sayısı beklenen yanlış pozitif sayısına (7) yakın, yani aile düzeyinde kanıt zayıf.
- F4'ün OOS dönemine 1. dalgada bakılmıştı.

## Bulgular
1. **Tek tutarlı küme: VIX > 20 ya da > 25 iken IBS < 0,2 AL, hisse ETF'lerinde.** XLK, QQQ, SMH, IJR, IWO, XBI, IBB, EEM, KRE ve yarıiletken grubunda net anormal getiri işlem başına 30–100 bps. Bu kümedeki 27 sinyalin günlük getiri korelasyonu ortalama 0,54; yani aslında tek bir bahis.
2. **Kümenin çoğu piyasanın kendi dönüşü.** SPY'dan arındırınca IS ve OOS t ≥ 2 kalan yalnız 8 sinyal var:
   - yarıiletken grubu IBS (VIX > 25, h1; t 2,53 / 2,86)
   - sigorta-borsa ve fintech Z5_SAT
   - IYR Z5_SAT (200 gün ortalamasının altında)
   - temel tüketim Z1_AL (200 gün ortalamasının altında)
   - nükleer grubu IBS
   - SMH IBS (200 gün ortalamasının altında)

   IBB, KRE, QQQ, IWM ve XLK'de arındırılmış t < 2.
3. **Kazancı koşul değil kural getiriyor.** "VIX > 25 olan her gün al" kuralı tek başına 0–25 bps getiriyor. Kural bunun üstüne ekliyor: kural getirisinin medyan %95'i bu fazladan geliyor.
4. **Gece ve gün içi.** ETF'lerde kazancın %70–90'ı ertesi gün içinde ve sonrasında oluşuyor. Hisse gruplarında gece payı yüksek: yarıiletkende 0,6–0,8, nükleer ve temiz enerjide ~1. Koşulsuz gece primi (186 ETF'in medyanı): IS'te +5,4 bps/gece (t 3,0), OOS'ta +4,9 bps/gece (t 2,1); gün içi ~0. KRBN ters yönde: gece −21 bps, gün içi +24 bps.
5. **Çalışmayanlar.**
   - MOM20 (AL ve SAT), MAC5 ve Z1: ETF'lerde ortalama t < 0.
   - Kesitsel kuralların hepsi elendi. Sektörde 5 günün en kötü 2'si (VIX > 25) 3 günde +31 bps verdi ama t 1,3 / 0,3. Alt sektörde 21 günün en iyi 3'ü IS t −4,6. Emtiada 63 günün en iyi 2'si negatif.
6. **Hipotezle çelişki.** 1. dalganın "XLF, KRE, KIE'de 80–190 bps" bulgusu, örtüşme düzeltmesiyle anlamlı değil:
   - XLF: 101 bps, t 1,93 / 1,43, elendi
   - KRE: 132 bps, t 2,56 / 1,60, İZLE; SPY'dan arındırınca t 0,35
   - KIE: 48 bps, elendi

## Çürütme testleri
- **Dairesel plasebo:** neredeyse hepsinde p = 0,001. Rejime bağlı sinyalde bu test zayıf kalıyor; bu yüzden 3. maddedeki "koşulun kendisi" kıyası eklendi.
- **Kriz dönemleri hariç:** sonuç değişmiyor (t 2,5–4,5).
- **VIX 1 gün gecikmeli:** yarıiletken OOS t 2,76'da kalıyor. EEM 1,58'e, fintech 1,14'e düşüyor.
- **Ertesi açılış girişi:** yarıiletken grubu (VIX > 20) ve EWJ geçemiyor, çünkü kazançları gecede oluşuyor.
- **Diğerleri:** IBS < 0,15 ile sonuç korunuyor. Maliyet iki katına çıkınca ETF'lerde OOS t 1,7–3,2.
- **En büyük işlemler:** 2008, 2009, 2015, 2019 ve 2022 panik günleri (±%6–9). Bozuk veri yok.

## Bugün (20.11.2026)
VIX 35,9. Ayakta kalan 130 satırın 73'ü açık; neredeyse hepsi IBS_AL / VIX kümesinde. Bu, tek bir piyasa dönüşü bahsi demek. Açık SAT sinyali yok. Ayrıntı `bugun.csv` dosyasında.

## Yöntem notları
- Bayat kapanışlı hedeflerde ana giriş ertesi açılış.
- Hisse grubu AL-dönüş sinyallerinin sınıfı en çok KOŞULLU olabilir, çünkü hayatta kalma yanlılığı var. Portföy n'i gün sayısıdır.
- Portföy testlerinde plasebo, E ve F betikte yazıldı.
- D'deki SAT kuralı ve I'daki 20 bps kuralı `sinifla()` fonksiyonuna eklendi.
