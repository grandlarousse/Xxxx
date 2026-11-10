# Ana kural: madenciler altından güçlüyse altın al (10.11.2026)

Kullanıcının istediği biçimde tek lead-lag kuralı: sinyali kapanışta gör, aynı kapanışta al, 1–3 gün sonra sat.

- **Sinyal:** güç = GDX'in son 10 işlem günlük getirisi − 1,4 × GLD − 0,8 × SPY (dünkü ABD kapanışına kadar). güç > +%2,5.
- **Al:** aynı gün 18:00–18:10 TSİ'de VİOP F_XAUUSD (Midas'ta kapanışa yakın GLD).
- **Sat:** son sinyal gününden 3 işlem günü sonra.

Bu, E2-C1 kuralının (`analiz/e2_etf_leadlag.md`, hakemde ORTA) VİOP hedefine aktarımı. Aktarım kontrolü: `c1_viop.py`.

VİOP 2017-03 → 2026-11 sonuçları (5 bps maliyet):
- 84 işlem, yılda ≈9, ortalama süre 8 gün.
- İşlem başına ortalama +%0,91, medyan +%0,84, %65 kârlı, en kötü −%5,5, en iyi +%9,4.
- Sinyalden sonraki 3 günde ortalama +%0,26 (tüm günler +%0,10), 5 günde +%0,48 (+%0,14).
- Sharpe 0,90 (sürekli tutmak 0,57); sürekli tutmaya göre alfa yılda %5,0 (t 2,3). 22 bps maliyetle Sharpe 0,73 (alfa t 1,6).
- 2022–2024'te etki yok (Sharpe ≈0). Kazanç 2017, 2020, 2025–26'da yoğun.
- Spot altın (15:00 UTC) 2010–2016: 3 günde fark +%0,31 (t 2,1), 5 günde +%0,49 (t 2,5).
- Altının kendi 10 günlük momentumu kontrol edilince sinyal kalıyor (korelasyon 0,02–0,05).

Sınırlar: kural 2008–2017 GLD verisinde seçilmişti; gerçekten dışarıda kalan dönem 2018–2026 (5 günlük fark t 2,2, 3 günlük t 1,65). Bağımsız yeniden üretim ve çürütme turu ayrıca çalıştırıldı; sonucu bu klasöre eklenecek.

Yatırım tavsiyesi değildir.
