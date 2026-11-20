# V1 — bağımsız yeniden üretim: S1, S2, S3 (zamanlama kuralları)

**Ne yapıldı.** Ortak kütüphane (`elib.py`) ve hazır paneller kullanılmadan, İş Yatırım ham JSON'larından (`raw/d1`) kendi kodumla kuruldu: düzeltilmiş getiri, tavan/taban kilidi, halka arz dışlaması, sinyaller, 3 günlük getiri (çıkış tabanda kilitliyse **ilk kilitsiz kapanış**), dönem-nötr kıyas (`per`). Kütüphane ve panel yalnız son adımda karşılaştırma için açıldı. Tablo: `ek/v1_yeniden_momentum.csv`. Kod: `kod/v1_yeniden_momentum/run.sh`.

**Ham veri denetimi.** 8 hisse (AKSEN, ENJSA, ODAS, ZOREN, BIGEN, AYDEM, LYDYE, MAGEN) ve XELKT yeniden indirildi: bütün satırlar ham dosyalarla aynı. XU030'da tek fark son günün yuvarlaması (13957,13 / 13957,12988). XU100 yeniden indirmesinde 94 tarih eksik geldi (93'ü 2010 öncesi, biri 2026-11-20); ortak tarihlerde değer farkı yok.

## Hüküm

| Kural | Hüküm | Ana ajan → V1 (fazla getiri, bps; t) |
|---|---|---|
| S1 zirve20 sepet | **YENİDEN ÜRETİLDİ** | IS 43,5 → 42,9 (2,8); OOS-1 84,7 → 83,6 (1,8); kasa 86,2 → 93,5 (2,7); havuz 82,6 → 85,1 (2,8) |
| S2 XELKT z ≥ 1 sepet | **YENİDEN ÜRETİLDİ** | IS 52,5 → 53,0 (3,2); OOS-1 53,0 → 53,1 (1,2); kasa 95,2 → 103,3 (2,4); havuz 70,3 → 73,4 (2,3) |
| S3 gecikme, üçlü | **YENİDEN ÜRETİLDİ** | IS 64,2 → 64,3 (2,4); OOS-1 220,6 → 221,0 (2,9); kasa 41,3 → 41,3 (0,8); havuz 156,7 → 156,9 (3,0) |

- Sinyal tarihleri örtüşmesi: S1 ve S3'te %100 (bütün dönemler); S2'de IS 442/444 (%99,5), sonrası %100. Eksik iki gün (2010-12-21, 2011-08-29) İş Yatırım'da hacmi 0 görünen, panelde Yahoo'dan yamalanan günler.
- Fark hiçbir satırda 10 bps'yi ve işareti aşmıyor. En büyük fark kasada (S1 +7,3; S2 +8,0 bps) ve nedeni **kıyas**: kütüphane çıkış kaymasını 5 günle sınırlıyor (`fwd_exec`, `max_delay=5`), yani uzun taban serilerinde kilitli kapanıştan çıkılmış sayıyor. Yönteme uygun hesapta (ilk kilitsiz kapanış) BIGEN'in kasa kıyası −360 yerine −579 bps, LYDYE ve MAGEN ~37 bps daha düşük. Kütüphaneyi taklit eden sürümüm ana rakamları 0,05 bps içinde veriyor. Ana ajanın rakamı bu yüzden temkinli taraftadır.
- Panel düzeyi: takvim aynı (4.238 gün); dolabilir hücrelerde fark 51/63.300; getiri farkı > %0,1 olan 13 hücre (Yahoo yaması günleri, LYDYE 2024-10-02).

## Ek sağlamlık (2023+ havuzu, V1 kodu)

| Kural | Blok önyükleme %90 GA (bps) | Kaydırma p (1.000 tekrar) | Çöküş hisseleri hariç |
|---|---|---|---|
| S1 | +31 … +136 | 0,002 | +67 (t 2,2) |
| S2 | +21 … +127 | 0,012 | +62 (t 2,0) |
| S3 | +77 … +247 | 0,005 | değişmez |

## Dikkat edilecek iki nokta

1. **`per` kasada çöküş hisselerine duyarlı.** BIGEN, LYDYE, MAGEN hedef ve kıyastan çıkarılınca kasa: S1 +93 → +59 (t 1,7), S2 +103 → +82 (t 2,1). Etki kaybolmuyor ama üçte biri kadarı bu üç hissenin "sıradan gün" zararından geliyor.
2. **Ham getiri `per`den düşük.** Kasada sinyal günü ham ortalaması S1 +48, S2 +57 bps; sinyal dışı günlerde sepet −65 / −55 bps. "Maliyet sonrası +40" `per` üzerinden hesaplanmış; yalnız AL yapan birinin cebine giren ham getiri − maliyettir (kasada S1 için yaklaşık +13 bps, havuzda yaklaşık +39 bps).

S3 kasada tek başına anlamsız (16 gün, 14 olay; %90 GA −40 … +139; p 0,32); havuz sonucu OOS-1'e dayanıyor.
