# Maliyet ve kural özeti (R2, 2026-11-20)

Kaynak: Pay Piyasası Prosedürü rev. 54 (21/09/2026), VİOP Prosedürü rev. 70 (01/07/2026), borsaistanbul.com.

| Konu | Doğrulanan kural |
|---|---|
| Spot seans | Açılış 09:40–09:55; sürekli 10:00–18:00; kapanış emir toplama 18:01–18:05, fiyat 18:05(+30 sn); kapanış fiyatından işlem 18:08–18:10 |
| VİOP pay vadeli | 09:30–18:10; akşam seansı yok; uzlaşma = son 10 dk (18:00–18:10) miktar ağırlıklı ortalama |
| Marj | Spot ±%10 (13/03/2020'den beri; kalıcı kural Yıldız ±%20, Ana ±%15); kapanış seansı son fiyat ±%3; pay vadeli ±%10 |
| Spot adım | <20: 0,01; 20–50: 0,02; 50–100: 0,05; 100–250: 0,10; 250–500: 0,25; 500–1000: 0,50; 1000–2500: 1; üstü 2,5 TL |
| Vadeli adım | <100: 0,01; 100–500: 0,05; 500–1000: 0,10; 1000–2500: 0,25; üstü 0,50 TL; sözleşme 100 pay, fiziki teslimat |
| Borsa payı (taraf başı) | Spot 0,25 bp; pay vadeli 0,3 bp |
| Açığa satış yasağı | 06/02/2023–01/01/2025 (tümü); 24/03–29/08/2025; 02/03–26/06/2026. Yalnız BIST 50'de serbest; 22/09/2026'dan beri yukarı adım kuralı |

Komisyon (taraf başı, +%5 BSMV; BSMV oranı doğrulanmadı): spot indirimli kurum 3–8 bp, banka 20 bp, yüksek hacim 1–2 bp (varsayım). VİOP: tarife tavanı 20 bp, banka 10 bp, pazarlıklı 2–5 bp (doğrulanmadı).

Bir fiyat adımı (yaklaşık fiyatla): AKSEN ~67 TL spot 7 bp, vadeli 1,5 bp; ENJSA ~120 TL spot 8 bp, vadeli 4 bp; ODAS ~9 TL her ikisi 11 bp.

## Gidiş-dönüş senaryoları (bp)

| Senaryo | Spot | VİOP |
|---|---|---|
| Düşük (yüksek hacim, iki bacak kapanış seansı) | 4–5 | 6–10 |
| Temel (indirimli bireysel, 1 adım kayma) | 18–25 | 15–30 |
| Yüksek (banka tarifesi) | 50+ | 45+ |

Not: VİOP senaryoları AKSEN/ENJSA/ODAS vadelilerinde alış-satış farkı ölçülmeden yazıldı; derinlik verisiyle doğrulanmalı. Backtest için öneri: spot 20 bp, duyarlılık 10 ve 40 bp.
