# Kullanım: elektrik sinyal araçları

**Önce şunu bil:** bu araçlar "al" demez; sinyalin oluştuğunu söyler. Raporun sonucu: S1 ve S2 istatistiksel olarak var ama maliyet ve faiz sonrası ortalama kazanç sıfıra yakın; S3 yalnız izleme içindir. Karar için `RAPOR.md` 2. bölüm.

## Kurulum (bir kez)

1. Bilgisayar ya da bulut: Python 3.9+ ve `pip install pandas numpy requests`. Bilgisayarın yoksa rapor 2.7'deki betiksiz yola bak.
2. TradingView → İzleme listesi → **Listeyi içe aktar** → `izleme_listesi.txt` (endeksler, vadeliler, likidite sırasıyla 42 hisse).
3. Pine Editor'e `elektrik_sinyal.pine` kodunu yapıştır, **BIST:XELKT günlük** grafiğine ekle. `hisse_sektor_fark.pine` bir hissenin günlük grafiğine eklenir.
4. Alarm: "çubuk kapanışında" çalan alarm kapanış seansından **sonra** gelir; işlem kararı için geç kalır, yalnız kayıt tutmaya yarar. 17:50 kararı için bir gece önce yazılan tetik düzeyine **fiyat alarmı** kur.

## Günlük akış

- **Bir gece önce:** `python3 sinyal.py` yarının tetik düzeylerini yazar; not al.
- **17:30:** hisselere elle bak (rapor 2.2, adım 1). Betik bu saatte hisse listesi vermez.
- **17:50:** XELKT değerini oku ve tetik düzeyiyle kıyasla. İstersen: `python3 sinyal.py --gunici XELKT=552,4 XU030=13950`. TradingView'da BIST verin gecikmeliyse değeri aracı kurum uygulamasından oku.
- **18:00:** S3'e yalnız bu saatte bak (XU030 ve XELKT'nin son değerleriyle).
- **18:10 sonrası:** `python3 sinyal.py` kesin sonucu, sepet ve kaçınma listesini ve yarının tetik düzeylerini verir. Bu çıktı kayıt içindir.
- **Çıkış:** sinyal günü 0 sayılır; 3. işlem günü kapanışta.
- Geçmiş bir gün: `--tarih 2026-11-12`. Tablo dosyası: `--csv hisse.csv`. Son günlerin dökümü: `--gecmis 20`.

## Çıktı nasıl okunur

- **S1 / S2 / S3:** EVET ya da HAYIR; altında bugünkü değer ve eşik. S3 yalnız izleme.
- **Yarın için tetik düzeyleri:** XELKT (S3 için ayrıca XU030) yarın hangi değerde kapanırsa sinyal oluşur.
- **Sepet:** bugün alınabilir hisseler, likidite sırasıyla. Sütunlar: fiyat, bir fiyat adımı (bps; 50'nin üstündeyse o hisse pahalıya gelir), 60 günlük medyan hacim (milyon TL), günlük getiri, sektöre göre fark (puan).
- **Kaçınma:** kural iki koşuldur: sektörden 5 puan geride kapanma ve tabana değme. "Günün en kötü beşte birliği" satırı ve tablodaki "alt 1/5 (bilgi)" etiketi kural değildir; dikkate alma.
- **T2:** doğrulanmamış bir kuraldır; bilgi içindir.
- Örnek: `ornek_cikti_2026-11-20.txt`.

## Sınırlar

- İş Yatırım'ın günlük endeks serisi **son gün için güvenilmez**. Betik son günleri saatlik serinin 18:00 kapanışıyla düzeltir ve NOT satırı yazar. Başlıktaki tarih bugün değilse biraz sonra yeniden çalıştır.
- `--gunici` yalnız endeks sinyallerini günceller; hisse listeleri son kapanışa göredir.
- Pine kodları TradingView'da derlenmedi. İlk hafta işaretleri `--gecmis` dökümüyle karşılaştır. Pine'da S2'nin "en az 5 dolabilir hisse" koşulu yoktur.
- `hisse_sektor_fark.pine` kıyas olarak XELKT'yi kullanır; araştırmadaki kıyas eşit ağırlıklı sepettir. Eşiğe yakın günlerde betiğin listesi geçerlidir.
- Yarım günlerde (resmî tatil öncesi) saatler farklıdır ve betik bu günlerde sınanmadı.
- Hisse listesi sabittir (20.11.2026, 42 üye). Endeks üyeliği değişirse `sinyal.py` içindeki `XELKT` satırını güncelle.
- Betiğin kural kodlarıyla aynı sonucu verdiği `dogrula.py` ile sınandı (`dogrulama_sonucu.txt`).
