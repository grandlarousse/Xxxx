# Ana kural: madenciler altından güçlüyse altın al (10.11.2026)

Kullanıcının istediği biçimde tek lead-lag kuralı: sinyali gör, kapanışta al, birkaç gün sonra sat. **Son güven: DÜŞÜK.**

## Kural (sade biçim)

- **Sinyal:** güç = GDX'in son 10 işlem günlük getirisi − GLD'nin son 10 işlem günlük getirisi (dünkü ABD kapanışına kadar). güç > +3,6 puan.
- **Al:** o gün 18:00–18:10 TSİ'de VİOP F_XAUUSD (Midas'ta kapanışa yakın GLD).
- **Sat:** son sinyal gününden 3 işlem günü sonra.

Tam biçim (E2-C1, `analiz/e2_etf_leadlag.md`): GDX₁₀ − b_GLD·GLD₁₀ − b_SPY·SPY₁₀ > %2,3–2,5 (250 günlük OLS betaları; Kasım 2026'da 1,4 ve 0,8). Sade biçim tam biçimle aynı sonucu veriyor.

## Sonuçlar (VİOP 2017-03 → 2026-11, 5 bps)

- 78–85 işlem, yılda 8–9. Ortalama süre 8,5 VİOP günü (medyan 6, en uzun 34). İşlemlerin %18'i 3 günde kapanıyor.
- İşlem başına ortalama +%1,0, medyan +%0,6, %59–66 kârlı, en kötü −%5,5 (pozisyon içinde −%8…−%9).
- Sinyalden sonraki 3 günde ortalama +%0,27 (tüm günler +%0,09), 5 günde +%0,50 (+%0,16). Fark NW t: 3 gün 1,9–2,1, 5 gün 2,4–2,6.
- Sharpe 0,93–1,00 (vadeli sürekli tutmak 0,57, spot 0,78). Alfa yılda %5,3–6,0 (t 2,4–2,6).
- Rastgele giriş plasebosuna (1.000 simülasyon) göre %99'un üstünde.
- Altının kendi momentumu, SPY, VIX, dolar ve oynaklık kontrol edilince sinyal kalıyor.

## Zayıflıklar (bağımsız yeniden üretici: ORTA, çürütücü: DÜŞÜK)

- **2018–2024 (7 yıl, 59 işlem):** altını sürekli tutmaktan iyi değil. Sharpe 0,42'ye karşı 0,51, alfa %1,1 (t 0,5), işlem başına +%0,34. 2022–2024'te 23 işlem toplam −%0,3.
- Kazancın %66'sı 2025–26'dan, %50'si en iyi 5 işlemden.
- Kuralın kendi tutuş süresi (3 gün) için 2018–2026 t değeri 1,4–1,65.
- Maliyet: 22 bps + vade devirleriyle Sharpe 0,78, alfa t 1,7. 40 bps'te t 1,2.
- Biçime duyarlı: GDXJ ile t 0,4/1,0; sabit beta 2 ile 0,6/1,4. GDX sürümü dağılımın üst ucunda.
- Üst uçta doz-tepki yok; q90 eşiğinde etki kayboluyor.
- Yavaş gösterge: sinyal 3–5 gün geciktirilince sonuç aynı. 1 günlük etki zayıf (+%0,09, t 1,9).
- Sinyal ABD kapanışında oluşuyor; VİOP girişi medyan 19 saat sonra.
- Spot 2010–2016 tekrarı bağımsız değil (kuralın seçildiği dönem); etkinin tamamı 2013–16'dan.

## Dosyalar

- `c1_viop.py`: ana ajanın aktarım kontrolü.
- `yeniden_uretim/`: bağımsız yeniden üretim kodu ve logları.
- `curutme/`: çürütme denemesi kodu ve logları (ızgara, plasebo, kontroller, sade biçimler, maliyet, 2026 işlemleri).

Yatırım tavsiyesi değildir.
