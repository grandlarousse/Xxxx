araç: 32/40

## Özet

Çıktılar yazıldı ve `run.sh` baştan sona çalışıyor (çıkış kodu 0). S1 ve S2'nin tam sepet rakamları birebir yeniden üretildi (S1 `per` 43,5 / 84,7 / 86,2 / havuz 82,6; S2 52,5 / 53,0 / 95,2 / 70,3).

**Ana sonuç: sepet en likit hisselere daraltılamaz, ama rastgele ya da orta likiditeden seçilerek küçültülebilir.**

- **En likit hisseler:** 2023 sonrasında etki yarıya iniyor. En likit 5'te OOS-1 26, kasa 39 (tam sepet 85 / 86); en likit 10'da 45 / 57; VİOP üçlüsünde kasa −25.
- **Tam sepetten kötü olmayanlar:** üç dönemde ve iki sinyalde de yalnız likiditesi alt yarıdakiler ve fiyatı 5 TL altındakiler. Farkların çoğunda |t| < 2; 30 varyant, çoklu test düzeltmesi yok.
- **Rastgele N:** ortalama değişmiyor, oynaklık artıyor. Olay başına standart sapma 308 (tam) → 425 (N = 3), 330 (N = 12).
- **Önerdiğim küçük sepet:** likidite sırası 6.–20. (15 hisse). S1 havuzda `per` 79 (t 2,8), net temel +49; tam sepet 83, +52. Bu varyantı ilk sonuçları gördükten sonra ekledim.
- **Sinyal birleştirme:** S2 günlerinin %37'si S1 günü. İkisi birlikte havuzda 125 (t 2,5; 54 gün); yalnız S2 OOS-1'de 9.
- **Pozisyon yenileme:** “sinyal sürdükçe tut, son sinyalden 3 gün sonra çık” S1'de yılda 45 işlemi 10 girişe indiriyor; gün başına maliyet 10 → 4 bps, giriş başına net +139.
- **Kapasite:** 100 bin TL sorunsuz, yalnız LYDYE alınamıyor (2.902 TL). 1 milyonda 3, 5 milyonda 13 hisse kapanış seansının %10'unu aşıyor. Tam sepet için üst sınır ≈ 610 bin TL.
- **Risk (S1 havuz):** en kötü %5 −401 ve altı, en kötü olay −891. İşlemlerin %1'inde çıkışta taban kilidi var (ortalama −%15). Zarar olasılığı (net) %44.
- **Koruma:** standart sapma %16 azalıyor, S1 `per` 78 → 59. Bir kontrat ≈ 149 bin TL, küçük sepette kurulamaz.
- **GNS fonu:** uygun değil; 13:30'dan sonraki alım “fiyat t+2” ile gerçekleşiyor, sinyalin ilk günü kaçıyor.
- **Ek bulgu (17:50 vekili):** XELKT'nin 17:50 değeri kapanış sinyalinin S1'de %96'sını, S2'de %90'ını yakalıyor.

**Dikkat edilecek üç ölçüm farkı:**
- Net rakamlarım gün ağırlıklı ve dönemin kendi maliyetiyle hesaplandı (havuz 30 bps, IS 42 bps). Bu yüzden S1 havuz neti +52; resmi tablodaki işlem ağırlıklı değer +40. IS'te net ≈ +2.
- `elib.fwd_exec` 5 günden uzun taban kilidinde işlemi hesaptan düşürüyor. Sinyal örnekleminde bu 1 işlem (MAGEN, −%32); sepet ortalamasına etkisi −1 bps.
- Koruma ve giriş gecikmesi satırlarında `per` sepet düzeyinde hesaplandı (S1 havuz 77,6); hisse düzeyindeki 82,6 ile küçük fark bundan.

## İddia defteri

| iddia | dosya ya da URL | sayı ya da alıntı | güven |
|---|---|---|---|
| S1 tam sepet yeniden üretildi | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v5_sepet.csv (soru=2_secim, tam_sepet) | per IS 43,5 (t 2,83); OOS1 84,7 (1,81); KASA 86,2 (2,47); HAVUZ 82,6 (2,75) | yüksek |
| S2 tam sepet yeniden üretildi | aynı | 52,5 (3,21); 53,0 (1,21); 95,2 (2,29); 70,3 (2,19) | yüksek |
| S1 net (gün ağırlıklı) | aynı | havuz +52,5 temel, +27,5 muhafazakâr; IS +1,7 ve −23,3; maliyet 30,1 (havuz), 41,8 (IS) | yüksek |
| Rastgele N: olay başına std (S1 havuz) | aynı (soru=1_rastgele_N) | tam 307; N=3: 425; 5: 377; 8: 348; 12: 330; 20: 315 | yüksek |
| Rastgele N: tam sepetten sapma | aynı | 294 / 219 / 163 / 121 / 71 bps | yüksek |
| Rastgele N: 174 olay sonunda net per %10–%90 | aynı | N=3: 22–82; N=5: 30–73; N=12: 41–65; N=20: 45–59 (tam 52) | yüksek |
| Rastgele N: zarar olasılığı (net) | aynı | tam %44; N=3 %46; N=5 %45; N=12 %44 | yüksek |
| En likit N, S1 per (IS/OOS1/KASA) | aynı (soru=2_secim) | likit5 51/26/39; likit10 44/45/57; likit20 43/65/76 | yüksek |
| VİOP üçlüsü zayıf | aynı | S1 75/44/−25; S2 47/62/47 | yüksek |
| Likidite alt yarı, tam sepete fark | aynı | S1 +3/+25/+10 (t 0,4/2,2/0,9); S2 +6/+9/+5 | orta |
| Fiyat < 5 TL, tam sepete fark | aynı | S1 +12/+13/+31; S2 +10/+24/+22; günde 3–6 hisse | orta |
| 15 hisse (sıra 6–20) | aynı | fark S1 −7/−7/+1, S2 +12/+1/+8; S1 havuz per 78,6 (t 2,8), net +48,6 | orta |
| Tavana ≥ %2 uzak ve K2 süzgeci | aynı | tavana: S1 +2/+2/0, S2 +3/+4/0; K2: S1 −0,4/+1,8/+8,2, S2 −1,1/+0,5/+15,7 | orta |
| T2'nin seçtikleri | aynı | fark S1 −38/+29/+6; S2 −28/+37/+36; günde 2–6 hisse | orta |
| Fiyat ≥ 5 TL | aynı | fark S1 −6/−2/−5; yarım adım 3,9 bps (tam 10,2) | yüksek |
| S1–S2 örtüşmesi (havuz, 971 gün) | aynı (soru=3_ortusme) | S1 174, S2 146, ikisi 54, biri 266; S2 günlerinin %37'si S1 | yüksek |
| Birleşik sinyaller | aynı (soru=3_birlesim) | S1 ve S2: havuz 124,6 (t 2,5), IS 47,1; yalnız S2: OOS1 8,9, KASA 88,3 | yüksek |
| Pozisyon politikaları (S1 havuz) | aynı (soru=3_politika) | ayrı dilim: 44,8 işlem/yıl, net +52; ertelemeli: 10,3 giriş/yıl, 7,1 gün, günlerin %29'u, per 169 (t 1,7), net +139; yok say: 21,1/yıl, net +51 | orta |
| Gün başına maliyet | aynı | 10,0 → 4,3 bps (ertelemeli) | yüksek |
| S1 ya da S2, ertelemeli | aynı | 19,6 giriş/yıl, 6,5 gün, günlerin %51'i, net +104 | orta |
| Kapasite (20.11.2026, 42 hisse) | aynı (soru=4_kapasite, 4_hisse) | 100 bin: 2.381 TL/hisse, en çok %1,6; 1 mn: 3 hisse > %10; 5 mn: 13 hisse > %10, 6 hisse > %25, ZEDUR %82 | orta |
| Sepet üst sınırı (hepsi ≤ %10) | aynı | tam ≈ 611 bin TL; sıra 6–20 ≈ 3,23 mn TL | orta |
| LYDYE 100 bin TL sepette alınamaz | aynı (4_hisse) | fiyat 2.902,50 TL > 2.381 TL | yüksek |
| Olay riski (havuz) | aynı (soru=5_risk) | S1: %5'lik −401, en kötü %5 ort. −575, en kötü −891 (2025-03-17); S2: −550, −1.038 (2026-10-20) | yüksek |
| Zarar serisi | aynı (5_risk, 3_politika) | S1 7, S2 6 sinyal günü; ertelemeli 5; yok say 3 | yüksek |
| Taban kilidi (S1 havuz) | aynı (5_risk) | işlemlerin %1'i, olayların %21'i (kasa %28); kilitli işlem ort. −1.508 bps; 5 günden uzun: 1 işlem, MAGEN −3.176 bps | yüksek |
| XU030 vadeli koruma (havuz) | aynı (soru=5_koruma) | S1 std 308 → 259, per 77,6 → 59,1; S2 351 → 298, 66,9 → 65,5; β 0,68; kontrat ≈ 148,9 bin TL | orta |
| Giriş gecikmesi (S1 havuz, sepet düzeyi) | aynı (soru=6_giris_gecikmesi) | t kapanış 77,6 (t 2,5); t+1 açılış 63,6 (2,1); t+1 kapanış 46,0 (1,3); h1 41,7 (3,5) | yüksek |
| 17:50 vekili (havuz, 959 gün) | aynı (soru=6_vekil_1750) | S1 yakalama 0,96, kesinlik 0,95; S2 0,90 / 0,94; ≥ 25 bps marjla kesinlik 0,98 | orta |
| GNS fiyat ve valör | https://www.garantibbvaportfoy.com.tr/assets/fon-brosuru-enerji-sirketleri-hisse-senedi-tl-fonu-gns-27032026.pdf | "13:30 … Alım t+1 t+1 / t+2 t+2; Satım t+1 t+2 / t+2 T+3"; "%0 stopaj"; "Yıllık Yönetim Ücreti: %3.20" | yüksek |
| GNS emir saati ve komisyon | https://kap.org.tr/tr/fon-bilgileri/genel/gns-garanti-portfoy-enerji-sirketleri-hisse-senedi-tl-fonu-hisse-senedi-yogun-fon | "Alım ve Satım Emirleri 13:30 a kadar verilir"; "Giriş komisyonu uygulanmayacaktır" | yüksek |

## açık kalanlar

- **Kapanış seansı hacmi dolaylı.** A7'nin hisse bazlı payı × güncel 60 günlük medyan hacim; 8 hissede pay yerine üye medyanı kullanıldı. Kapasite sınırları bu yüzden yaklaşık.
- **Aracı kurum ayrıntıları kontrol edilmedi:** asgari komisyon, toplu (sepet) emir olanağı, kapanış seansı emir türü. 40 emrin 18:01–18:05 arasında elle girilip girilemeyeceği bilinmiyor.
- **GNS'te “fiyat t+1” ifadesinin hangi günün değerlemesi olduğu izahnameden okunmadı.** Her iki yorumda da 13:30 sonrası talimat sinyal gününün kapanışını kaçırıyor; sonuç değişmiyor. TEFAS sayfası erişimi reddetti.
- **15 hisselik sepet sonradan eklendi** ve sıra sınamada her gün yenilendi; elle aylık güncelleme sınanmadı.
- **17:50 vekili yalnız endeks düzeyinde sınandı.** 17:45 damgalı barın 17:50 değeri olduğu varsayıldı. Hisselerin 17:50'deki tavan durumu burada ölçülmedi (A7'de var).
- **Koruma maliyeti varsayım** (vadeli gidiş-dönüş 10 / 20 bps). 2017-03 öncesinde vadeli yerine XU030 endeksi kullanıldı.
- **Ertelemeli tutma dondurulmuş kuralla aynı şey değil:** sepet ilk sinyal günü kurulup yenilenmiyor, t değeri 1,7.

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v5_sepet.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v5_sepet.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v5_sepet/run.sh
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v5_sepet/v5.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v5_sepet/ozet.py