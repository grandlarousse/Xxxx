# Kullanım: elektrik sinyal araçları

## Kurulum (bir kez)

1. Bilgisayar ya da bulut: Python 3.9+ ve `pip install pandas numpy requests`.
2. TradingView → İzleme listesi → **Listeyi içe aktar** → `izleme_listesi.txt` (endeksler, vadeliler, likidite sırasıyla 42 hisse).
3. Pine Editor'e `elektrik_sinyal.pine` kodunu yapıştırın, **BIST:XELKT günlük** grafiğine ekleyin. `hisse_sektor_fark.pine` bir hissenin günlük grafiğine eklenir.
4. Alarm: gösterge → Alarm ekle → koşul S1, S2 ya da S3 → **Çubuk kapanışında bir kez**.

## Günlük akış

- **17:50:** TradingView'da XELKT ve XU030 değerini okuyun:
  `python3 sinyal.py --gunici XELKT=552,4 XU030=13950`
  EVET çıkarsa kapanış seansı (18:01–18:05) için emri hazırlayın.
- **18:10 sonrası:** `python3 sinyal.py` kesin sonucu ve yarının tetik düzeylerini verir. Düzeyleri TradingView'a fiyat alarmı olarak girebilirsiniz.
- **Çıkış:** S1, S2, S3 için 3 işlem günü sonra kapanışta.
- Geçmiş bir gün: `--tarih 2026-11-12`. Tablo dosyası: `--csv hisse.csv`. Son günlerin dökümü: `--gecmis 20`.

## Çıktı nasıl okunur

- **S1 / S2 / S3:** EVET ya da HAYIR; altında bugünkü değer ve eşik.
- **Yarın için tetik düzeyleri:** XELKT (S3 için ayrıca XU030) yarın hangi değerde kapanırsa sinyal oluşur.
- **Sepet:** bugün alınabilir hisseler, likidite sırasıyla. Sütunlar: fiyat, bir fiyat adımı (bps; büyükse maliyet yüksek), 60 günlük medyan hacim (milyon TL), günlük getiri, sektöre göre fark (puan).
- **Kaçınma:** sektörden 5 puan geride kapananlar, günün en kötü beşte birliği, tabana değenler. Sinyal olsa da bunları almayın.
- **T2:** sakin ve güçlü hisseler; sepet içinde seçim yardımcısı.
- Örnek: `ornek_cikti_2026-11-20.txt`.

## Sınırlar

- İş Yatırım'ın günlük endeks serisi **son gün için güvenilmez** (aynı istek farklı değer döndürebiliyor). Betik son günleri saatlik serinin 18:00 kapanışıyla düzeltir ve NOT satırı yazar. Başlıktaki tarih bugün değilse biraz sonra yeniden çalıştırın.
- `--gunici` yalnız endeks sinyallerini günceller; hisse listeleri son kapanışa göredir. Bugün tavanda kapananı sepetten kendiniz çıkarın.
- Pine kodları TradingView'da derlenmedi. İlk hafta işaretleri `--gecmis` dökümüyle karşılaştırın. Pine'da S2'nin “en az 5 dolabilir hisse” koşulu yoktur.
- `hisse_sektor_fark.pine` kıyas olarak XELKT'yi kullanır; araştırmadaki kıyas eşit ağırlıklı sepettir. Eşiğe yakın günlerde betiğin listesi geçerlidir.
- Hisse listesi sabittir (20.11.2026, 42 üye). Endeks üyeliği değişirse `sinyal.py` içindeki `XELKT` satırını güncelleyin.
- Ölçümler maliyet öncesidir. S1 ve S2 temel maliyetten sonra yaklaşık +40 bps bırakıyor; T2 maliyetle sıfıra yakın. S3 son dönemde zayıf (14 olay). VİOP SAT kuralları doğrulanmadı; araçlarda yok.
- Betiğin kural kodlarıyla aynı sonucu verdiği `dogrula.py` ile sınandı (`dogrulama_sonucu.txt`).
