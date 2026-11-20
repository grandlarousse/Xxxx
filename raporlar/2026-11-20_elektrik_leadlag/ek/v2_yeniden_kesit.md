# V2 — kesit kurallarının bağımsız yeniden üretimi (T2, K1, K2) ve T1 denetimi

**Yöntem.** Ortak kütüphane ve hazır paneller kullanılmadı; getiri, tavan/taban bayrakları (E4), halka arz süzgeci, çıkış kaydırması ve 'sec' kıyası İş Yatırım ham JSON'larından kendi kodumla kuruldu (`kod/v2_yeniden_kesit/`). 8 hisse yeniden indirildi: ham dosyalarla fark sıfır. Panelle son karşılaştırma: 65.497 getiri hücresinin 15'i farklı (Yahoo yamaları).

**Hükümler** (bps; parantezde t; tablo `ek/v2_yeniden_kesit.csv`)

| Kural | IS | OOS-1 | Kasa | Havuz 2023+ | En büyük fark | Hüküm |
|---|---|---|---|---|---|---|
| T2 | +10,7 (2,8) | +16,2 (2,9) | +37,0 (4,7) | +23,7 (5,2) | 1,0 | **YENİDEN ÜRETİLDİ** |
| K1 | −18,7 (−3,1) | −29,0 (−5,4) | −125,6 (−7,4) | −64,0 (−8,9) | 0,3 | **YENİDEN ÜRETİLDİ** |
| K2 | −122,8 (−3,9) | −147,3 (−4,8) | −626,7 (−8,6) | −352,5 (−9,5) | 3,1 | **YENİDEN ÜRETİLDİ** |

İşaret farkı ve 5 bps'i aşan fark yok. Rakamlar doğru; T2'nin kasa yorumu aşağıda değişiyor.

**(a) Kıyas kirlenmesi: evet, kasada büyük.** Kasada kıyas sepetinin ertesi gün getirisi ortak tanımda −29,8 bps/gün; tabanda kapananlar çıkınca −3,2; kaydırmasız −7,6. Neden: 13.191 dolabilir hisse-günün 230'u taban kapanışı (BIGEN 29, LYDYE 14, MAGEN 13 gün art arda), çıkışları günlerce kayıyor. T2 bu hisseleri seçemiyor (bayrak süzgeci), kıyas içeriyor.

| T2 kıyası | IS | OOS-1 | Kasa | Havuz |
|---|---|---|---|---|
| ortak | +10,7 | +16,2 | +37,0 | +23,7 |
| tabanda kapanan yok | +8,2 (2,1) | +13,6 (2,5) | **+9,7 (1,6)** | +12,2 (2,9) |
| yalnız bayraksız hisseler | +7,8 | +12,6 | +7,8 (1,3) | +10,9 (2,6) |
| medyan | +29,0 | +41,8 | +31,8 | +38,2 |

Medyan kıyası her dönemde yukarı yanlıdır (kesit sağa çarpık). Sonuç: T2'nin üstünlüğü her dönemde ~8–14 bps; kasadaki +38 güçlenme değil, kıyasın çöküş serileriyle aşağı çekilmesidir. T2 IS+OOS-1 görülerek donduruldu; tek bağımsız sınavı olan kasada temiz kıyasla t 1,3–1,6. Temel maliyet (25 bps) sonrası eksi.

**(b) Çıkış kaydırması yok.** T2: +9,3 / +15,4 / +14,1 (2,3). K1: −12,4 / −25,9 / −49,2 (−7,0); havuz −34,3. K2: −78 / −118 / −270 (−9,8). İşaretler korunuyor; kasa büyüklüklerinin yarıdan fazlası kaydırmadan geliyor. K2, tabanda kapananlar hariç: −16 / −91 / −81 (ana ajan −13 / −91 / −74; fark bayrak tanımından). Kütüphane kaydırmayı +5 günle sınırlıyor; sınırsız kaydırmada T2 kasa +45, K2 kasa −730.

**(c) T2 ham getiri.** OOS-1: seçilen +15,8, seçilmeyen −2,2 (fark 18,0; t 2,9). Kasa: seçilen **+6,3**, seçilmeyen −37,4; kaydırmasız seçilmeyen −10,5 (fark 16,7; t 2,4).

**(d) T1 sızıntı denetimi: sızıntı yok.** Model her ayın ilk günü s'de eğitilir; son eğitim satırı s−7, etiketinin çıkışı en geç s−1 (1 gün + 5 gün kaydırma payı). Tahmin gününün etiketi eğitime girmiyor; özellikler shift/rolling. Kesme sınaması: panel 2025-06-30'da kesilince 10.717 sinyalin tamamı aynı. Ana tablodaki `nedensellik_oran` 0,059 sızıntı değil: panel_dev ile panel_full arasında 10 getiri hücresi < 1e-6 ayrışıyor, 4 haneli yuvarlama 9 hücrede dönüyor, ağaç bölünmeleri kayıyor (sayısal kırılganlık). Aynı sinyal benim getirilerimle: IS +4,5, OOS-1 +25,0, kasa +40,6 (ana ajanla aynı). Kıyas tabansız: OOS-1 +22,4 (5,3), **kasa +13,2 (3,1)**; ayrıca kaydırmasız +10,0 (2,4). T1'in kasa +41'i de aynı kirlenmeyi taşıyor; OOS-1 sağlam.

**Sınır.** T1 modeli yeniden yazılmadı; 2015-12 öncesi bayraklar güvenilmez.
