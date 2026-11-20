# V6 — karar anı ve dolum gerçekçiliği

Karar 17:55–18:04'te verilir, sinyaller 18:05 kapanışıyla tanımlı. Tablo: `ek/v6_zamanlama.csv`; kod: `kod/v6_zamanlama/run.sh`. Getiriler bps, 3 günlük `per`; giriş hep kapanış fiyatı. Endeks verisi 2017+ (2.450 gün).

## Hüküm

| Kural | Önceden uygulanır mı | Saat, eşik | Yakalama / kesinlik | Getiri kaybı |
|---|---|---|---|---|
| S1 zirve20 | Evet | 17:50, tamponsuz | 0,95 / 0,94 | −3 (2017+), +2 (2023+), kasa −10 |
| S2 z ≥ 1 | Evet | 17:50–17:55, z ≥ 1 | 0,87 / 0,91 (17:55: 0,90 / 0,93) | −6 (2017+), +5 (2023+) |
| S3 gecikme | Hayır; ancak 18:00 | 18:00 son değer | 0,89 / 0,83 (17:00: 0,56 / 0,66) | −25 (2017+), −66 (2023+) |
| T2 sade seçim | Evet | 17:30 fiyatı | 0,81 / 0,80 (18:00: 0,87 / 0,89) | yok (+32; kapanış +31) |
| K1 en kötü beşte bir | Evet | 17:30 | 0,80 / 0,80 | yok (−81, kapanış −72) |
| K2 5 puan geride | Evet | 17:30 | 0,76 / 0,90 | yok (−468, kapanış −409) |

- **Tampon (17:50).** S1'de +%0,3: kesinlik 0,99, yakalama 0,82, getiri 85 (tamponsuz 73). −%0,15: 0,98 / 0,88, getiri 68. S2'de z ≥ 1,2: 0,69 / 0,98, getiri 58 (kayıp −14); z ≥ 0,9: 0,94 / 0,83, getiri 70 (kayıp −2). Yanlış sinyaller zararsız (S1 +55, S2 +81), kaçanlar iyi (S2 +120). Tampon gerekmez; S2'de eşiği sıkılaştırmak kaybettirir.
- **Dönemler (17:50; kapanış sinyali → saatinde karar).** S1: IS (2017–2022) 74 → 68, OOS-1 82 → 94, kasa 81 → 71. S2: 76 → 64, 50 → 65, 95 → 83. Farklar ±15 bps içinde.
- **S3 kırılgan.** Kaçan günler en iyileri (18:00, 2023+: 7 gün, +508). Gevşek eşik (zX ≥ 0,9, zE < 0,7; 18:00): yakalama 1,00, kesinlik 0,56, getiri 101 (kapanış 120). XU030 5 dk verisi tamamlanamadı (sunucu kotası). 17:30–17:55 satırları 1.067 günlük alt örneklem (656 günü XU100 oranı vekili; hata medyan 2 bps); 17:00 ve 18:00 saatlik veriyle tam.

## Dolum

- Sinyal günü tavanda kapanan (alım dolmaz): S1 %4,3, S2 %5,6 (2017+); kasa %2,0 ve %3,6; bütün günler %2,6. 17:30'da tavanda olmayıp tavanda kapanan: hisse-günlerin %0,6'sı (S1), %1,0'ı (S2); tavan kapanışlarının dörtte biri 17:30'dan sonra oluşur. Tavana ≤ %1 yakın kilitsiz kapanış: %0,7 ve %1,1.
- 17:50–17:59'da sürekli işlemde almak: karar anı sinyaliyle koşullandığında XELKT kapanışı 17:50–18:00 ortalamasından +0,3 (S1), +2,5 (S2) bps farklı (2023+ +1, kasa −2); medyan mutlak fark 9–11. Hisse düzeyinde (2023-12+) kapanış 17:30 fiyatının 5–9, 18:00 son fiyatının 1–3 bps altında; hisse başına medyan sapma 16–37. Gerçek 17:50–17:59 hisse verisi 60 gün (3–5 sinyal günü): hüküm yok. Ortalamada fiyat avantajı yok; sürekli işlemde ayrıca alış-satış farkı ödenir.
- Çıkış günü (t+3) tabanda kilit: S1 %0,9, S2 %0,6, S3 0/430; bütün günler %0,8 (kasa %1,7).

## Kapanış seansı emri (borsaistanbul.com, piyasa işleyişi)

- 18:01–18:05: limit, piyasa, piyasadan limite emir girilebilir. Fiyat son işlem fiyatının ±%3'ünü aşamaz. Eşleşmeyen piyasa emri iptal edilir.
- 18:08–18:10: yalnız kapanış fiyatından limit emir; karşıda bekleyen varsa dolar.
- Risk: tavanda kapanışta alış dolmaz; limit kapanış fiyatının altındaysa dolmaz. KAFE (kapanış fiyatlı emir) birincil kaynakta doğrulanamadı.

## Akış

1. 17:30: T2/K1/K2 listesi (%80 doğru). +%7 üstündeki hisseleri sepetten çıkar (A7: tavanda kapanma %22–56).
2. 17:50: XELKT. S1: önceki 19 kapanışın en yükseğinin üstünde mi; S2: günlük getiri ≥ 60 günlük std.
3. 17:55–18:00: eşiğe yakınsa (zirveye ±%0,15; z 0,9–1,1) 18:00 değerini bekle. S3'e yalnız 18:00'de bak.
4. 18:01–18:04: kapanış seansına limit (öneri: son fiyatın 1–2 adım üstü) ya da piyasa emri.
5. 18:08–18:10: dolmayan kısım için kapanış fiyatından emir.
6. t+3: kapanış seansında sat.

**Zayıflıklar:** hisse gün içi verisi 2023-12 sonrası ve saatlik; kapanış seansı derinliği yok.
