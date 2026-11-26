# Model sonuçları (v2): net odaklı çalışma saati

Her sayı `cikti/` altındaki bir CSV dosyasından `python3 sim.py rapor` ile yazılmıştır; saatler 0,5 hassasiyetle yuvarlanmıştır. Model ölçüm değil, hesap aracıdır; "optimum" yalnız bu varsayımlar altında geçerlidir. Senaryo başına 2000 kabul edilmiş çekim (iki tohum), kabul oranı %40–%42 (kabul_orani.csv).

## 1. Ana sonuç

Bu varsayımlar altında, 180 günlük ufukta K3 seviyesinde (a) amacının sağlam politikası girdideki tavanı izler (hA + hB): h3 = 5 → 4,0 + 0,0 saat × 7 gün (haftada 28,5); h3 = 6 → 5,0 + 0,0 saat × 7 gün (haftada 35,0); h3 = 7 → 5,5 + 0,0 saat × 7 gün (haftada 38,5); h3 = 8 → 6,0 + 0,0 saat × 7 gün (haftada 42,5); saat sayısı h3 girdisinin geri gelişidir, bağımsız bulgu değildir. Modelin kendi katkısı biçimdir: pişmanlık eğrisi asimetriktir (h3 = 6, K3, (a), ufuk ortalaması: günde 1 saat az çalışmak çıktıyı %11 düşürür; 1 saat fazlası çekimlerin %99'inde uçuruma götürür ve çıktıyı %45 düşürür). Çekim başına optimum, kronik birikimin başladığı h1 eşiğinin çevresindedir (h3 = 6, K3, (a), 180 gün: optimum hA − h1 ortancası -0,20 saat [-0,64; 0,00]); sonucu en çok eB, v1, h0 parametreleri oynatır, 30 günlük ufuk ise K3 tavanını 360 güne göre yalnız ×1,02 yükseltir.

## 2. Ana tablo (h3 = 6 ve h3 = 7)

Sağlam politika: çekimler üzerinde beklenen pişmanlığı en küçük politika (kısıtı çiğnediği çekimde pişmanlık 1). "Aralık" = varsayım aralığı: çekim başına optimum hA ortancası [Q1–Q3]. Son dönem: gün × ψ. Öteki h3 senaryoları, hB aralığı, pişmanlık, ihlal ve uçurum olasılığı ana_tablo.csv dosyasındadır.

**Tablo 2 — h3 = 6 (kaynak: cikti/ana_tablo.csv)**

| Ufuk | K | (a) hA + hB | gün | hafif | son dönem | hft. saat | aralık (hA) | (b1) hA + hB | gün | hafif | son dönem | hft. saat | aralık (hA) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 30 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 30 | K2 | 4,5 + 0,0 | 7 | 3 hf | 7 g × 1,25 | 29,5 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 3 hf | 7 g × 1,25 | 26,5 | 4,5 [4,0–5,0] |
| 30 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 36,0 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 34,0 | 5,0 [4,5–5,0] |
| 90 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 90 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 90 | K2 | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 28,0 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 28,0 | 4,5 [4,0–5,0] |
| 90 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 35,5 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 34,5 | 4,5 [4,0–5,0] |
| 120 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 120 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 120 | K2 | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 27,0 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 6 hf | yok | 26,5 | 4,5 [4,0–5,0] |
| 120 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 35,0 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 35,0 | 4,5 [4,0–5,0] |
| 150 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 150 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 150 | K2 | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 26,5 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 6 hf | yok | 26,0 | 4,5 [4,0–5,0] |
| 150 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 35,0 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 35,0 | 4,5 [4,0–5,0] |
| 180 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 180 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 180 | K2 | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 26,5 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 6 hf | yok | 26,0 | 4,5 [4,0–5,0] |
| 180 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 35,0 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 35,0 | 4,5 [4,0–5,0] |
| 270 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 270 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 270 | K2 | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 26,0 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 6 hf | yok | 26,0 | 4,5 [4,0–5,0] |
| 270 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 35,0 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 35,0 | 4,5 [4,0–5,0] |
| 360 | K0 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 360 | K1 | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,0 [3,5–4,5] |
| 360 | K2 | 4,0 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 26,0 | 4,5 [4,0–5,0] | 4,0 + 0,0 | 7 | 6 hf | yok | 26,0 | 4,5 [4,0–5,0] |
| 360 | K3 | 5,0 + 0,0 | 7 | yok | 3 g × 1,25 | 35,0 | 5,0 [4,5–5,0] | 5,0 + 0,0 | 7 | yok | 3 g × 0,75 | 35,0 | 4,5 [4,0–5,0] |

**Tablo 2 — h3 = 7 (kaynak: cikti/ana_tablo.csv)**

| Ufuk | K | (a) hA + hB | gün | hafif | son dönem | hft. saat | aralık (hA) | (b1) hA + hB | gün | hafif | son dönem | hft. saat | aralık (hA) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 30 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 30 | K2 | 5,0 + 0,0 | 7 | 3 hf | 7 g × 1,25 | 33,0 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 3 hf | 7 g × 1,25 | 29,5 | 5,0 [4,5–5,5] |
| 30 | K3 | 6,0 + 0,0 | 7 | yok | yok | 42,0 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 37,5 | 5,5 [5,0–6,0] |
| 90 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 90 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,5] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 90 | K2 | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 31,5 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 31,5 | 5,0 [4,5–5,5] |
| 90 | K3 | 5,5 + 0,0 | 7 | yok | 7 g × 1,25 | 39,0 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 38,0 | 5,5 [5,0–6,0] |
| 120 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 120 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 120 | K2 | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 30,5 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 6 hf | 3 g × 0,75 | 29,5 | 5,0 [4,5–5,5] |
| 120 | K3 | 5,5 + 0,0 | 7 | yok | 3 g × 1,25 | 38,5 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 38,5 | 5,5 [5,0–5,5] |
| 150 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 150 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 150 | K2 | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 30,0 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 6 hf | yok | 29,5 | 5,0 [4,5–5,5] |
| 150 | K3 | 5,5 + 0,0 | 7 | yok | 3 g × 1,25 | 38,5 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 38,5 | 5,5 [5,0–5,5] |
| 180 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 180 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 180 | K2 | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 30,0 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 6 hf | yok | 29,0 | 5,0 [4,5–5,5] |
| 180 | K3 | 5,5 + 0,0 | 7 | yok | 3 g × 1,25 | 38,5 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 38,5 | 5,5 [5,0–5,5] |
| 270 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 270 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 270 | K2 | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 29,5 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 6 hf | yok | 29,0 | 5,0 [4,5–5,5] |
| 270 | K3 | 5,5 + 0,0 | 7 | yok | 3 g × 1,25 | 38,5 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 38,5 | 5,5 [5,0–5,5] |
| 360 | K0 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 360 | K1 | 4,0 + 0,0 | 7 | yok | yok | 28,0 | 4,5 [4,0–5,0] | 3,5 + 0,0 | 7 | yok | yok | 24,5 | 4,5 [4,0–5,0] |
| 360 | K2 | 4,5 + 0,0 | 7 | 6 hf | 14 g × 1,25 | 29,5 | 5,0 [4,5–5,5] | 4,5 + 0,0 | 7 | 6 hf | 3 g × 0,75 | 29,0 | 5,0 [4,5–5,5] |
| 360 | K3 | 5,5 + 0,0 | 7 | yok | 3 g × 1,25 | 38,5 | 5,5 [5,0–6,0] | 5,5 + 0,0 | 7 | yok | 3 g × 0,75 | 38,5 | 5,5 [5,0–5,5] |

## 3. Pişmanlık eğrisinin asimetrisi

Sağlam politikanın hA değeri δ saat kaydırılmıştır (öteki alanlar sabit; ufuklar üzerinden ortalama). Pişmanlık tanımı gereği kısıtı çiğneyen çekimde 1 sayılır; kısıttan bağımsız ölçü "çıktı oranı" satırıdır (J(δ)/J(0)). Marjinal sınama (marjinal_sinama.csv; h3 = 6, 180 gün, (a)): ufkun ortasındaki bir güne +0,5 saat, K3 sağlam politikasında aynı gün 0,32 etkili saat kazandırır, sonraki günlerde 0,45 etkili saat kaybettirir (kayıp/kazanç 1,40; çekimlerin %59'inde kayıp büyük); K0 politikasında kayıp/kazanç 0,05.

**Tablo 3 — K3, ufuk ortalaması (kaynak: cikti/pismanlik_ozet.csv; ufuk bazında pismanlik_egrisi.csv)**

| h3 | amaç | ölçü | −2 | −1 | −0,5 | 0 | +0,5 | +1 | +2 |
|---|---|---|---|---|---|---|---|---|---|
| 6 | a | ort. pişmanlık % | 33 | 13 | 6 | 3 | 59 | 100 | 100 |
| 6 | a | %95 pişmanlık % | 42 | 23 | 14 | 10 | 100 | 100 | 100 |
| 6 | a | kısıt ihlali % | 0 | 0 | 0 | 0 | 57 | 100 | 100 |
| 6 | a | uçurum % | 0 | 0 | 0 | 0 | 11 | 99 | 100 |
| 6 | a | çıktı oranı | 0,69 | 0,89 | 0,96 | 1,00 | 0,96 | 0,55 | 0,41 |
| 6 | b1 | ort. pişmanlık % | 11 | 4 | 2 | 1 | 15 | 99 | 100 |
| 6 | b1 | %95 pişmanlık % | 18 | 8 | 5 | 5 | 87 | 100 | 100 |
| 6 | b1 | kısıt ihlali % | 0 | 0 | 0 | 0 | 11 | 99 | 100 |
| 6 | b1 | uçurum % | 0 | 0 | 0 | 0 | 0 | 92 | 100 |
| 6 | b1 | çıktı oranı | 0,90 | 0,97 | 1,00 | 1,00 | 0,97 | 0,79 | 0,71 |
| 7 | a | ort. pişmanlık % | 28 | 12 | 6 | 3 | 14 | 93 | 100 |
| 7 | a | %95 pişmanlık % | 38 | 22 | 14 | 9 | 40 | 100 | 100 |
| 7 | a | kısıt ihlali % | 0 | 0 | 0 | 0 | 11 | 93 | 100 |
| 7 | a | uçurum % | 0 | 0 | 0 | 0 | 2 | 56 | 100 |
| 7 | a | çıktı oranı | 0,74 | 0,91 | 0,97 | 1,00 | 0,99 | 0,91 | 0,46 |
| 7 | b1 | ort. pişmanlık % | 9 | 3 | 2 | 1 | 2 | 37 | 100 |
| 7 | b1 | %95 pişmanlık % | 16 | 8 | 5 | 4 | 7 | 87 | 100 |
| 7 | b1 | kısıt ihlali % | 0 | 0 | 0 | 0 | 0 | 34 | 100 |
| 7 | b1 | uçurum % | 0 | 0 | 0 | 0 | 0 | 0 | 100 |
| 7 | b1 | çıktı oranı | 0,92 | 0,98 | 0,99 | 1,00 | 0,99 | 0,95 | 0,75 |

## 4. Kısa ufukta tavanın üstüne çıkma

λ = 0 temel modelde 30 günlük ufuk tavanı az yükseltir: h3 = 6'da K3 haftalık tavanı 360 güne göre ortanca ×1,02 [1,02–1,07], 90 günde ×1,01. Altı gün/hafta düzeninde uçuruma düşmeden çıkılabilen en yüksek hA, 30 günde çekimlerin çoğunda h3'te kalır (ortanca fark 0,0 saat). Fark en çok şu parametrelere bağlıdır (kısmi sıra korelasyonu, h3 = 6, tavan oranı): tau2 (0,60), v1 (-0,34), h0 (-0,32); uçurumsuz en yüksek hA için: tau2 (0,41), v1 (-0,30), h0 (-0,30).

**Tablo 4 (kaynak: cikti/kisa_ufuk.csv, kisa_ufuk_duyarlilik.csv)**

| h3 | ufuk | uçurumsuz en yüksek hA (6 gün/hf) | K3 için en yüksek hA (6 gün/hf) | K3 tavanı (hft. saat) | tavan / 360 günlük tavan |
|---|---|---|---|---|---|
| 5 | 30 | 5,0 [5,0–5,0] | 5,0 [4,5–5,0] | 42,0 [38,5–43,0] | 1,02 [1,02–1,08] |
| 5 | 90 | 5,0 [5,0–5,0] | 4,5 [4,5–4,5] | 39,0 [38,5–42,5] | 1,01 [1,00–1,01] |
| 5 | 360 | 5,0 [5,0–5,0] | 4,5 [4,5–4,5] | 38,5 [38,5–42,0] | 1,00 [1,00–1,00] |
| 6 | 30 | 6,0 [6,0–6,0] | 6,0 [5,5–6,0] | 49,0 [45,5–50,0] | 1,02 [1,02–1,07] |
| 6 | 90 | 6,0 [6,0–6,0] | 5,5 [5,5–5,5] | 46,0 [45,5–49,5] | 1,01 [1,00–1,01] |
| 6 | 360 | 6,0 [6,0–6,0] | 5,5 [5,5–5,5] | 45,5 [45,5–49,0] | 1,00 [1,00–1,00] |
| 7 | 30 | 7,0 [7,0–7,0] | 7,0 [6,5–7,0] | 54,5 [52,5–57,5] | 1,04 [1,02–1,07] |
| 7 | 90 | 7,0 [7,0–7,0] | 6,5 [6,5–6,5] | 53,0 [49,5–56,0] | 1,01 [1,00–1,01] |
| 7 | 360 | 7,0 [7,0–7,0] | 6,5 [6,5–6,5] | 52,5 [49,0–56,0] | 1,00 [1,00–1,00] |
| 8 | 30 | 8,0 [8,0–8,5] | 8,0 [7,5–8,0] | 61,0 [59,5–63,0] | 1,05 [1,00–1,06] |
| 8 | 90 | 8,0 [8,0–8,0] | 7,5 [7,5–7,5] | 59,5 [56,0–60,5] | 1,00 [1,00–1,01] |
| 8 | 360 | 8,0 [8,0–8,0] | 7,5 [7,5–7,5] | 59,5 [56,0–59,5] | 1,00 [1,00–1,00] |

## 5. Son dönem (T, ψ) seçimleri

Sağlam politikalarda (ana_tablo.csv, 112 hücre/amaç): (a) son dönem yok 58, hızlanma (ψ > 1) 54, azaltma (ψ < 1) 0; (b1) yok 71, hızlanma 10, azaltma 31. Aşağıdaki tablo çekim başına optimumların payıdır (K3, dört h3 ortalaması).

**Tablo 5 — çekim başına optimumda son dönem payı, % (kaynak: cikti/son_donem_ozet.csv)**

| son dönem | (a) 30 gün | (a) 180 gün | (a) 360 gün | (b1) 30 gün | (b1) 180 gün | (b1) 360 gün |
|---|---|---|---|---|---|---|
| yok | 6 | 6 | 6 | 35 | 17 | 16 |
| 3 g × 0,50 | 0 | 0 | 0 | 3 | 10 | 10 |
| 3 g × 0,75 | 0 | 0 | 0 | 59 | 64 | 63 |
| 3 g × 1,25 | 55 | 46 | 46 | 2 | 0 | 0 |
| 7 g × 0,50 | 0 | 0 | 0 | 0 | 0 | 0 |
| 7 g × 0,75 | 0 | 0 | 0 | 0 | 8 | 10 |
| 7 g × 1,25 | 34 | 31 | 31 | 1 | 0 | 0 |
| 14 g × 0,50 | 0 | 0 | 0 | 0 | 0 | 0 |
| 14 g × 0,75 | 0 | 0 | 0 | 0 | 0 | 0 |
| 14 g × 1,25 | 5 | 16 | 17 | 0 | 0 | 0 |

## 6. (a) ile (b1) örtüşmesi

Çekim başına en iyi politikalar birebir nadiren aynıdır (son dönem ayrışır) ama günlük saatte yakındır: h3 = 6, K3, 180 günde hA farkı ≤ 0,5 olan çekim payı %95; (a)'nın en iyisi (b1) ölçüsünde ortalama %4,8 kaybeder. e1 = e2 = 0 referansı sınav günü yorgunluk cezasının payını gösterir: referansın en iyisinin (b1) pişmanlığı %4,6.

**Tablo 6 — K3 (kaynak: cikti/ortusme.csv)**

| h3 | ufuk | aynı politika % | aynı taban (hA, hB, gün, hafif) % | hA farkı ≤ 0,5 % | (a) en iyisinin (b1) pişmanlığı % | e=0 ile aynı politika % | e=0 en iyisinin (b1) pişmanlığı % | sağlam hA: a / b1 / e=0 |
|---|---|---|---|---|---|---|---|---|
| 6 | 30 | 3 | 67 | 93 | 4,4 | 3 | 4,3 | 5,0 / 5,0 / 5,0 |
| 6 | 90 | 1 | 75 | 95 | 4,7 | 1 | 4,5 | 5,0 / 5,0 / 5,0 |
| 6 | 120 | 1 | 75 | 95 | 4,8 | 1 | 4,6 | 5,0 / 5,0 / 5,0 |
| 6 | 150 | 1 | 74 | 95 | 4,8 | 1 | 4,6 | 5,0 / 5,0 / 5,0 |
| 6 | 180 | 1 | 74 | 95 | 4,8 | 1 | 4,6 | 5,0 / 5,0 / 5,0 |
| 6 | 270 | 0 | 74 | 95 | 4,9 | 1 | 4,6 | 5,0 / 5,0 / 5,0 |
| 6 | 360 | 0 | 74 | 95 | 4,9 | 1 | 4,6 | 5,0 / 5,0 / 5,0 |
| 7 | 30 | 2 | 64 | 90 | 3,9 | 2 | 3,8 | 6,0 / 5,5 / 5,5 |
| 7 | 90 | 1 | 72 | 94 | 4,3 | 1 | 4,1 | 5,5 / 5,5 / 5,5 |
| 7 | 120 | 0 | 71 | 93 | 4,4 | 1 | 4,1 | 5,5 / 5,5 / 5,5 |
| 7 | 150 | 0 | 72 | 92 | 4,4 | 1 | 4,2 | 5,5 / 5,5 / 5,5 |
| 7 | 180 | 0 | 72 | 92 | 4,4 | 1 | 4,2 | 5,5 / 5,5 / 5,5 |
| 7 | 270 | 0 | 72 | 92 | 4,4 | 1 | 4,2 | 5,5 / 5,5 / 5,5 |
| 7 | 360 | 0 | 72 | 92 | 4,4 | 1 | 4,2 | 5,5 / 5,5 / 5,5 |

## 7. (b2) Virtual OSCE: açık tablosu ve karar kuralı

Karar kuralı: Pr(geçme) ≥ 0,95 koşulunu çekimlerin en az %90'ında sağlayan politikalar içinde önce en düşük K, sonra en az toplam net saat (eşitlikte en düşük tepe f2); başlangıç gecikmesi D de seçilir. "Çekim başına" sütunu aynı kuralın her çekimde ayrı uygulanmasıdır. Gereken saat S kabulü ve κN varsayımına doğrudan bağlıdır; Pr yalnız sınav günü gürültüsünü kapsar. Öteki h3 senaryoları ve K bazında ayrıntı: b2_karar.csv, b2_acik_tablosu.csv.

**Tablo 7 — h3 = 6 (kaynak: cikti/b2_karar.csv)**

| açık (Pgeç − g0) | ufuk | karar K | gecikme (gün) | hA + hB | gün | toplam net saat | hft. saat | olurluk % | çekim başına toplam saat | çekim başına günlük saat | hiçbir politika yetmez % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0,05 | 30 | K3 | 0 | 5,0 + 0,0 | 7 | 141 | 33,0 | 90 | 55 [37–80] | 3,0 [2,5–4,0] | 8 |
| 0,05 | 90 | K0 | 23 | 3,5 + 0,0 | 7 | 220 | 23,0 | 90 | 86 [57–135] | 3,0 [2,5–3,5] | 0 |
| 0,05 | 120 | K0 | 30 | 3,0 + 0,0 | 7 | 265 | 20,5 | 91 | 95 [64–159] | 3,0 [2,5–3,5] | 0 |
| 0,05 | 150 | K0 | 75 | 3,5 + 0,0 | 7 | 260 | 24,5 | 90 | 105 [70–166] | 3,0 [2,0–3,5] | 0 |
| 0,05 | 180 | K0 | 90 | 3,5 + 0,0 | 7 | 303 | 23,5 | 91 | 112 [78–174] | 2,5 [2,0–3,5] | 0 |
| 0,05 | 270 | K0 | 135 | 3,0 + 0,0 | 7 | 374 | 19,5 | 90 | 138 [93–201] | 2,5 [1,5–3,0] | 0 |
| 0,05 | 360 | K0 | 180 | 2,5 + 0,0 | 7 | 452 | 17,5 | 90 | 156 [108–234] | 2,0 [1,5–3,0] | 0 |
| 0,15 | 30 | yok | – | – + – | – | – | – | – | 66 [45–95] | 3,5 [3,0–4,0] | 20 |
| 0,15 | 90 | K0 | 0 | 3,0 + 0,0 | 7 | 268 | 21,0 | 90 | 102 [64–158] | 3,0 [2,5–3,5] | 0 |
| 0,15 | 120 | K0 | 30 | 3,5 + 0,0 | 7 | 303 | 23,5 | 91 | 108 [70–175] | 3,0 [2,5–3,5] | 0 |
| 0,15 | 150 | K0 | 38 | 3,0 + 0,0 | 7 | 326 | 20,5 | 90 | 113 [76–188] | 3,0 [2,5–3,5] | 0 |
| 0,15 | 180 | K0 | 90 | 3,5 + 0,0 | 7 | 309 | 24,0 | 90 | 121 [81–195] | 3,0 [2,0–3,5] | 0 |
| 0,15 | 270 | K0 | 135 | 3,0 + 0,0 | 7 | 394 | 20,5 | 91 | 140 [95–212] | 2,5 [1,5–3,0] | 0 |
| 0,15 | 360 | K0 | 180 | 2,5 + 0,0 | 7 | 454 | 17,5 | 90 | 162 [108–234] | 2,0 [1,5–3,0] | 0 |
| 0,30 | 30 | yok | – | – + – | – | – | – | – | 77 [52–106] | 3,5 [3,0–4,0] | 32 |
| 0,30 | 90 | K0 | 0 | 3,5 + 0,0 | 7 | 312 | 24,5 | 90 | 120 [74–186] | 3,0 [2,5–4,0] | 1 |
| 0,30 | 120 | K0 | 0 | 3,0 + 0,0 | 7 | 355 | 20,5 | 91 | 120 [79–198] | 3,0 [2,5–3,5] | 0 |
| 0,30 | 150 | K0 | 38 | 3,5 + 0,0 | 7 | 361 | 22,5 | 91 | 126 [84–212] | 3,0 [2,5–3,5] | 0 |
| 0,30 | 180 | K0 | 45 | 3,0 + 0,0 | 7 | 394 | 20,5 | 90 | 130 [88–216] | 3,0 [2,0–3,5] | 0 |
| 0,30 | 270 | K0 | 135 | 3,0 + 0,0 | 7 | 400 | 20,5 | 90 | 147 [100–222] | 2,5 [2,0–3,0] | 0 |
| 0,30 | 360 | K0 | 180 | 2,5 + 0,0 | 7 | 459 | 18,0 | 91 | 166 [112–247] | 2,0 [1,5–3,0] | 0 |

## 8. Duyarlılık: ilk 5 parametre

Hedef: çekim başına optimum hA; kısmi sıra korelasyonu (PRCC) bütün hücrelerde hesaplanıp ortalanmıştır. "Üst − alt" = parametrenin üst ve alt yarısındaki optimum hA ortancalarının farkı. Bunlar ölçülmesi en değerli parametrelerdir; h3 ise senaryo eksenidir ve hepsinden baskındır (Tablo 2). K0–K2 için tol duyarlılığı: tol 0,01 ile sağlam hA ortalama 0,23 saat, tol 0,05 ile 0,40 saat değişir (ana_tablo.csv).

**Tablo 8 (kaynak: cikti/duyarlilik_ozet.csv; hücre bazında duyarlilik.csv)**

| amaç | sıra | parametre | ort. mutlak PRCC (hA) | ort. PRCC (hA) | ort. mutlak PRCC (hft. saat) | üst − alt yarı (hA, saat) |
|---|---|---|---|---|---|---|
| a | 1 | eB | 0,54 | -0,54 | 0,56 | -0,54 |
| a | 2 | v1 | 0,53 | 0,53 | 0,48 | 0,42 |
| a | 3 | h0 | 0,49 | 0,49 | 0,50 | 0,41 |
| a | 4 | cB | 0,42 | 0,42 | 0,61 | 0,39 |
| a | 5 | q1 | 0,29 | 0,29 | 0,38 | 0,26 |
| b1 | 1 | v1 | 0,55 | 0,55 | 0,50 | 0,48 |
| b1 | 2 | eB | 0,54 | -0,54 | 0,56 | -0,54 |
| b1 | 3 | h0 | 0,53 | 0,53 | 0,58 | 0,44 |
| b1 | 4 | cB | 0,44 | 0,44 | 0,62 | 0,39 |
| b1 | 5 | q1 | 0,30 | 0,30 | 0,32 | 0,28 |

## 9. Y senaryosu (yavaş birikim)

λ > 0 olduğunda girdi olarak verilen h3 artık süresiz sürdürülemez: h3 = 6'da 6 gün/hafta h3 saat çalışan düzen λ = 0,02 ile 90 günde çekimlerin %100'inde, 360 günde %100'inde çöker; K3 haftalık tavanı 360 günde 45,5 saatten (λ = 0) 42,0 (λ = 0,02) ve 42,0 (λ = 0,05) saate iner. Uzun ufuktaki temkin modelin temelinden değil bu senaryodan gelir.

**Tablo 9 — 1000 çekim, tohum 1, yalnız son dönemsiz politikalar (kaynak: cikti/y_senaryosu.csv)**

| h3 | λ | ufuk | K3 tavanı (hft. saat) | uçurumsuz en yüksek hA (6 gün/hf) | K3 için en yüksek hA (6 gün/hf) | h3 düzeninin çöktüğü çekim % |
|---|---|---|---|---|---|---|
| 5 | 0,00 | 90 | 38,5 [38,5–42,0] | 5,0 [5,0–5,0] | 4,5 [4,5–4,5] | 0 |
| 5 | 0,00 | 360 | 38,5 [38,5–42,0] | 5,0 [5,0–5,0] | 4,5 [4,5–4,5] | 0 |
| 5 | 0,02 | 90 | 38,5 [35,0–42,0] | 4,5 [4,5–4,5] | 4,5 [4,0–4,5] | 100 |
| 5 | 0,02 | 360 | 38,5 [35,0–38,5] | 4,5 [4,0–4,5] | 4,0 [4,0–4,5] | 100 |
| 5 | 0,05 | 90 | 38,5 [35,0–38,5] | 4,5 [4,0–4,5] | 4,0 [4,0–4,5] | 100 |
| 5 | 0,05 | 360 | 35,5 [35,0–38,5] | 4,0 [4,0–4,5] | 4,0 [4,0–4,5] | 100 |
| 6 | 0,00 | 90 | 45,5 [45,5–49,0] | 6,0 [6,0–6,0] | 5,5 [5,5–5,5] | 0 |
| 6 | 0,00 | 360 | 45,5 [45,5–49,0] | 6,0 [6,0–6,0] | 5,5 [5,5–5,5] | 0 |
| 6 | 0,02 | 90 | 45,5 [42,0–45,5] | 5,5 [5,0–5,5] | 5,0 [5,0–5,5] | 100 |
| 6 | 0,02 | 360 | 42,0 [42,0–45,5] | 5,0 [5,0–5,5] | 5,0 [5,0–5,5] | 100 |
| 6 | 0,05 | 90 | 42,0 [42,0–45,5] | 5,0 [5,0–5,5] | 5,0 [5,0–5,5] | 100 |
| 6 | 0,05 | 360 | 42,0 [38,5–45,5] | 5,0 [4,5–5,0] | 5,0 [4,5–5,0] | 100 |
| 7 | 0,00 | 90 | 52,5 [49,0–56,0] | 7,0 [7,0–7,0] | 6,5 [6,5–6,5] | 0 |
| 7 | 0,00 | 360 | 52,5 [49,0–56,0] | 7,0 [7,0–7,0] | 6,5 [6,5–6,5] | 0 |
| 7 | 0,02 | 90 | 49,0 [45,5–52,5] | 6,0 [6,0–6,5] | 6,0 [6,0–6,0] | 100 |
| 7 | 0,02 | 360 | 49,0 [45,5–52,5] | 6,0 [5,5–6,0] | 6,0 [5,5–6,0] | 100 |
| 7 | 0,05 | 90 | 49,0 [45,5–52,5] | 6,0 [5,5–6,0] | 6,0 [5,5–6,0] | 100 |
| 7 | 0,05 | 360 | 49,0 [45,5–49,0] | 5,5 [5,5–6,0] | 5,5 [5,5–6,0] | 100 |
| 8 | 0,00 | 90 | 59,5 [56,0–59,5] | 8,0 [8,0–8,0] | 7,5 [7,5–7,5] | 0 |
| 8 | 0,00 | 360 | 59,5 [56,0–59,5] | 8,0 [8,0–8,0] | 7,5 [7,5–7,5] | 0 |
| 8 | 0,02 | 90 | 52,5 [52,5–56,0] | 7,0 [6,5–7,0] | 7,0 [6,5–7,0] | 100 |
| 8 | 0,02 | 360 | 52,5 [49,0–56,0] | 6,5 [6,5–7,0] | 6,5 [6,0–7,0] | 100 |
| 8 | 0,05 | 90 | 52,5 [49,0–56,0] | 6,5 [6,0–7,0] | 6,5 [6,0–7,0] | 100 |
| 8 | 0,05 | 360 | 52,5 [45,5–56,0] | 6,5 [6,0–6,5] | 6,5 [6,0–6,5] | 100 |

## 10. Yorum kararları, sınamalar, azaltılanlar

**Yorum kararları (tanımda açık olmayan yerler)**

- S önseli tanımda yok: log-tekdüze 30–1000 etkili saat alındı; S ve τG öğrenme dayanağıyla kabul edildi.
- DUS için g0 = 0,3 (kabul dayanağındaki değer). (b2)'de g0 = Pgeç − açık, S_N = κN·S; gecikme süresince g unutmayla düşer; D = H·k/4 en yakın güne yuvarlandı.
- Hafta takvimi çalışmanın ilk gününe bağlıdır; dinlenme günleri haftanın son günleri, hafif haftalar n., 2n., … haftalardır.
- Son dönemde ψ çarpanı hafif haftanın yerine geçer, haftalık dinlenme sürer; T ufuktan uzunsa seçenek yok sayılır.
- Çöküşte hA ve hB birlikte yarıya iner. Tanımda sınav sabahı çöküş için P'ye ek ceza yok; bütün K seviyeleri çöküşü dışladığı için sonuca etkisi yok.
- K kümeleri yazıldığı gibi iç içe değil (aşağıda "K_literal" satırları): d = 7 ya da hafif haftasız politika K0'da olup K1/K2 koşuluna giremiyor; K1 ve K2 son kontrol sabahından sonraki çöküşe ya da 0,8·Fcrit aşımına izin veriyor. Tanım düzeltilmedi; uygulanan en yakın tutarlı yorum: K3 yazıldığı gibi, K2 = (K0 ∪ K1 ∪ K2 koşulu) ∩ K3, K1 = (K0 ∪ K1 koşulu) ∩ K3. K2 koşulu ufuk içinde en az bir tamamlanmış hafif hafta ister.
- Sağlam politikada kısıtı çiğneyen çekimin pişmanlığı 1 sayıldı. (b2)'de pişmanlık tanımlı olmadığından %90 olurluk kuralı kullanıldı.
- Tavan = kısıtı sağlayan politikaların en yüksek toplam net saati (haftalık ortalama olarak verildi). Uçurum eşiği sayısal olarak f2 ≥ Fcrit·(1 + 1e−9).
- Marjinal sınama: ufkun ortasındaki ilk çalışma gününde hA + 0,5 saat.

**Sınamalar (kaynak: cikti/sinamalar.csv, cikti/pytest.xml)**

pytest: 31 sınama, 24 geçti, 7 kaldı, 0 atlandı. Birim sınamalar (fazla yük yoksa f ≡ 0 ve q ≡ 1; s = 2'de arctan; durağan f1 ve Fcrit kapalı biçimi; g'nin durağan değeri; h3 rejimi; hızlı motor ile referans benzetici uyumu; K tavan sırası) geçti. Kalanlar: K_literal_K0_K1, K_literal_K1_K2, K_literal_K1_K2_uygulanabilir, K_literal_K1_K3, K_literal_K2_K3, izgara_ust_sinir_hB3, izgara_025_Jyildiz_kazanc.

| sınama | sonuç | sayı | eşik |
|---|---|---|---|
| K_tavan_sirasi | geçti | 1,0000 | =1 |
| K_literal_K0_K1 | kaldı | 0,3318 | =0 |
| K_literal_K0_K1_uygulanabilir | geçti | 0,0000 | =0 |
| K_literal_K1_K2 | kaldı | 0,3273 | =0 |
| K_literal_K1_K2_uygulanabilir | kaldı | 0,0001 | =0 |
| K_literal_K1_K3 | kaldı | 0,0002 | =0 |
| K_literal_K2_K3 | kaldı | 0,0027 | =0 |
| K_literal_K0_K3 | geçti | 0,0000 | =0 |
| iki_tohum_uyumu_hA | geçti | 0,9866 | >=0.9 |
| iki_tohum_uyumu_haftalik | geçti | 0,9821 | >=0.9 |
| izgara_ust_sinir_hA10 | geçti | 0,0000 | <0.05 |
| izgara_alt_sinir_hA1 | geçti | 0,0000 | <0.05 |
| izgara_ust_sinir_hB3 | kaldı | 0,1320 | <0.05 |
| izgara_025_yakinsama_hA | geçti | 1,0000 | >=0.9 |
| izgara_025_Jyildiz_kazanc_ort | geçti | 0,0075 | bilgi |
| izgara_025_Jyildiz_kazanc | kaldı | 0,0159 | <0.005 |
| motor_referans_tutarliligi | geçti | 0,0000 | <0.002 |
| h3_girdi_cikti | geçti | 1,0000 | =1 |
| kabul_sayisi | geçti | 1000,0000 | >=1000 |

Kalanların nedeni: "K_literal" satırları tanımdaki kümelerin yazıldığı gibi iç içe olmadığını gösterir (yukarıdaki yorumla giderildi; K_tavan_sirasi geçer). Öteki kalanlar: izgara_ust_sinir_hB3 (cekim basina optimumun hB=3 sinirina yapisma payi); izgara_025_Jyildiz_kazanc (0,25 izgaranin cekim basina en iyi J degerine en buyuk ortalama katkisi).

**Azaltılanlar.** Ana koşuda azaltma yok: tam ızgara (9.120 politika × 7 ufuk), senaryo ve tohum başına 1000 kabul. Yan koşular daha küçük: 0,25 ızgara yakınsaması yalnız h3 = 6 ve 250 çekim; Y senaryosu yalnız tohum 1 ve son dönemsiz politikalar; pişmanlık eğrisi yalnız hA ekseninde. İki aşamalı aramaya gerek kalmadı. Hesap süresi: 287 s (duvar saati, 4 süreç; sure.csv).

## 11. Bu çıktı hangi cümleyle sunulmalı

"Bu tablo bir ölçüm değil; 'süresiz sürdürebildiğin tavan h3 şu kadarsa, tutarlı program şudur' diyen bir hesap aracıdır. Saat sayıları girdideki h3 varsayımını geri verir; güvenilecek kısım biçimdir: tavanın biraz altında kalmanın maliyeti küçük, üstüne çıkmanın maliyeti büyüktür ve kısa ufuk bunu çok az değiştirir. Hepsi yeterli uyku koşuluna bağlıdır."
