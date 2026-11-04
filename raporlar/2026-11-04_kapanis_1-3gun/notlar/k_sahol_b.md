# k_sahol_b: SAHOL/AKBNK kapanıştan kapanışa VİOP spread'i, çürütme denemesi

Kod `out/code_k_sahol_b/` altında:
- `lb.py`: kendi kütüphanem. k_sahol_a kodu import edilmedi.
- `common.py`
- `01_base` … `09_now`, logları `log0*.txt`.
- Çıktılar: `res_grid.csv`, `res_pairs.csv`, `tr_viop_*.csv`.

**Veri**
- Spot: ydl.fetch kopyası (`ydl_b.py`) ile `dl_k_sahol_b/` dizinine yeniden indirildi; ortak veriye dokunulmadı. Günlük bar 02.11.2026'ya kadar dolu. 03.11 kapanışı saatlik 15:00 UTC barından alındı: SAHOL 82,45, AKBNK 62,25.
- VİOP: 02.11 ve 03.11 bültenleri kendi ayrıştırıcımla işlendi. **Son veri tarihi 03.11.2026.**

Birim: bps, SAHOL bacağı nominaline göre. Maliyet aksi yazılmadıkça bacak başına gidiş-dönüş 8 bps + 1 tik; her devirde tekrar alınır.

## Hüküm: KOŞULLU, güven ORTA (alt uç)
Mekanik hatalar çürütülemedi:
- Zamanlama ve ileriye bakma sorunu yok.
- Temettü ve devir P&L'i doğru.
- Maliyet ve tam sayı kontrat sorun değil.
- Rastgele giriş plasebosu p≈0,002.

Ama "OOS t ~3" iddiası abartılı. Kenar bölgesel ve dönemsel; ileriye dönük beklenti yaklaşık yarısı alınmalı (işlem başı ~30–50 bps):
- 2005–13 spot'ta Kural A sıfır (net −6 bps).
- VİOP 2017–22'de zayıf (t 1,24).
- Kazancın çoğu 2023 ve 2026'dan geliyor.
- Kardeş çiftlerde tekrarlanmıyor.

**Öneri (kullanıcı profili için):**
- Kural A (β250, z60, giriş |z|>1,5, çıkış |z|≤1,5), zaman sınırı ve stop yok, küçük boyut.
- İşlemlerin %67'si ≤3 gün sürüyor, ama kuyruk (%10'u ≥11 gün, en çok 17 gün) taşınmalı.
- 1–4 hafta kabul ediliyorsa Kural C (çıkış |z|≤1) maliyete ve parametreye daha dayanıklı.

## Bağımsız yeniden hesap
VİOP gerçek uzlaşma, aynı gün uzlaşmadan giriş ve çıkış. Ön vade tutulur; 1 iş günü kala devredilir.

| | VİOP 2021–26 | VİOP 2017–20 | Spot 2014–20 | Spot 2005–13 |
|---|---|---|---|---|
| **A** | 106 işlem (18,2/yıl), brüt 93,6, **net 69,7**, medyan 112, isabet %75, **t 3,35** (NW 2,57), Sharpe 0,92 | 28,9 (t 1,17) | 55,5 (3,30) | **−5,8 (−0,20)**; brüt 39 (1,35) |
| **C** | 64 işlem, net 143,0 (t 3,44) | 41,7 (0,86) | 98,1 (3,25) | 73,8 (1,49) |
| **B** | 49 işlem, net 247,1 (t 3,80) | 70,1 (0,96) | 151,9 (4,14) | 67,5 (0,87) |

Kural A, VİOP 2021–26 ayrıntıları:
- Tutma ortalama 3,8, medyan 2 gün; %75'i ≤4, %90'ı ≤11, en uzun 17 gün.
- Maks. düşüş −2.515 bps: 01.04.2021'den 12.04.2022'ye. Eski zirveye ancak 16.03.2023'te dönüldü; yaklaşık 23 ay su altında.
- En kötü işlem −777, 5. yüzdelik −306. En uzun ardışık kayıp serisi 3.

k_sahol_a ile tutarlılık:
- A sonuçları uyumlu (108 işlem, 64 bps, t 3,12'ye karşı 106 / 69,7 / 3,35).
- Yıllık işlem sayıları ve ortalamaları da uyumlu.

## Kontroller
**(1) Zamanlama.**
- Pay vadeli seansı 18:10'da bitiyor. Uzlaşma 18:00–18:10 arasının VWAP'ı; spot kapanış ~18:05'te belli oluyor. Yani uzlaşma penceresinin yarısı sinyalden önce.
- Test: sinyali kapanış öncesi fiyattan ürettim. Saatlik 13:30 UTC barı ≈17:30 TSİ; 14:30 UTC barı ≈18:00 TSİ, yalnız yaz aylarında var. Tarihi Yahoo saatlik verisinde 15:00 barı yok.
- Ortak pencere 12.2023–11.2026, Kural A: kapanış sinyali 80,3 (t 2,85); 17:30 sinyali 78,6 (2,33); ~18:00 sinyali 77,8 (2,42).
  - C: 160 / 146 / 142.
  - B: 272 / 246 / 269.
- z korelasyonu 0,992–0,995.
- **Ertesi gün uzlaşmasıyla giriş-çıkış** (VİOP 2021–26):
  - A 82,7 (t 2,96); C 178,9 (4,49); B 205,4 (3,64).
  - 12.2023+ A 124,8 (3,53).
  - k_sahol_a'nın "aynı akşam şart" uyarısı spot vekiline ait bir artefakt (kapanış seansı sıçraması). VİOP'ta bir gün gecikme kenarı bozmuyor.
- Olay profili (A girişleri, VİOP brüt): 1. gün 13 (t 0,8), 2 gün 50 (2,4), 3 gün 67, 5 gün 78, 10 gün 159 (3,1).

**(2) Temettü ve devir.**
- Temettü (ex) günleri (SAHOL 10, AKBNK 8): vadeli getirisi − adj spot getirisi −1,25…+0,34 puan, ortalama ≈ −0,3. Ham spotla fark +1,2…+9,7 puan. Yani vadeli temettüde düşmüyor; adj sinyal doğru.
- Devir günü vadeli−spot farkı ortalama −8 bps (sd 48); normal günde −15 bps (sd 62, taşıma maliyeti). Aykırı değer yok.
  - Tek istisna 07–08.02.2023 deprem kapanışı (takvim artefaktı); o sırada açık işlem yok.
- **Taşıma (carry) asimetrisi:** β<1 olduğu için LONG spread net uzun nominal taşıyor ve faizi ödüyor.
  - LONG işlemler VİOP'ta spottan işlem başına −39,6 bps kötü; SHORT +3,8.
  - Bu VİOP P&L'inde zaten var, hata değil.
  - Eşit TL hedge'le nötrlenir: A eşit TL 107,5 bps (t 3,86), daha yüksek vol.
- Panelde Ocak 2019 F_AKBNK verisi eksik; o işlemler dışlandı (2021+ etkilenmiyor).

**(3) Parametre ızgarası.** Pencere 20/40/60/120 × eşik 1,0/1,5/2,0 × çıkış (A, 1,0, 0,5, 0). Tekrarlar ayıklanınca 44 kombinasyon.

| | β250 | β120 |
|---|---|---|
| OOS VİOP 2021–26 t>2 | **34/44** | 19/44 |
| net>0 | 44/44 | 44/44 |
| t medyanı / NW t medyanı | 2,71 / 1,91 | 1,88 / 1,44 |
| Yalnız A çıkışı t>2 | 10/12 (z20'de 1,24–2,18) | 1/12 (medyan 1,46) |
| 2021–22 t medyanı | 0,29 | 0,03 |
| 2023–26 t>2 | 44/44 | 39/44 |

- β penceresi (z60, 1,5, A): β60 t 1,54; β120 1,81; **β250 3,35**; β500 3,53; β750 3,28; sabit β=1 (saf oran) 1,47.
- Sonuç β≥250'de sağlam, kısa β'da zayıf.

**(4) Alt dönemler** (VİOP, A, net bps ve t):
- 2021–22: **21 (0,53)**.
- 2023: 136 (3,58).
- 2024: 55 (0,65).
- 2025: 51 (1,40).
- 2026: 137 (4,60).
- Fon krizi (16.09.2026+): 3 işlem, +50 bps ortalama (−142, +192, +101).
- Mart 2025 şoku: 7 işlem, 37 bps.
- Son 12 ay: 17 işlem, 109 (3,23).
- C ve B'de tablo aynı: 2021–22 t 0,6–0,8; 2023–26 güçlü.

**(5) En iyi işlemler çıkarılınca** (VİOP 2021–26):

| | Hepsi | En iyi 5 hariç | En iyi 10 hariç |
|---|---|---|---|
| A | 69,7 (t 3,35) | 53,4 (2,60) | 39,9 (1,93) |
| C | 143 (3,44) | 107 (2,57) | 79 (1,82) |
| B | 247 (3,80) | 180 (2,78) | 126 (1,84) |

**(6) Benzer çiftler**, aynı kural. A için VİOP 2021–26 net bps (t) | spot 2014–20:

| Çift | VİOP 2021–26 | Spot 2014–20 |
|---|---|---|
| SAHOL/AKBNK | **69,7 (3,35)** | 55 (3,30) |
| SAHOL/YKBNK | 29 (0,99) | 45 (3,59) |
| SAHOL/XBANK (bacak F_XLBNK) | 44 (1,60) | 62 (3,85) |
| SAHOL/GARAN | 17 (0,56) | 45 (2,01) |
| SAHOL/ISCTR | 5 (0,15) | −20 (−1,14) |
| KCHOL/YKBNK | −16 (−0,50) | −12 (−0,44) |
| KCHOL/AKBNK | 1 (0,04) | −6 (−0,23) |
| KCHOL/SAHOL | −26 (−0,90) | −31 (−0,82) |
| AKBNK/YKBNK | −42 (−1,25) | −10 (−0,55) |
| AGHOL/AEFES (yalnız spot; AGHOL'ün VİOP'u yok) | spot 2021–26: −108 (−0,97) | −134 (−2,29) |

- SAHOL–banka çiftlerinde zayıf pozitif bir aile etkisi var. Ama 2021–26'da yalnız SAHOL/AKBNK anlamlı.
- k_sahol_a'nın kaynağı da 24 ana/yavru çiftinden yalnız bunun çalıştığını yazıyor. Yani seçim yanlılığı var.
- Ekonomik gerekçe güçlü (Akbank, Sabancı NAV'ının en büyük kalemi) ama genelleme yok.

**(7) Plasebo** (VİOP 2021–26, A):
- Rastgele giriş: aynı işlem sayısı, aynı tutma dağılımı, aynı long/short oranı, 2.000 tekrar. Ortalama −23,9 bps (sd 30,1), %99'luk dilim 47,6. **p = 0,0015.**
- z zaman kaydırma (±20…750 gün, 148 kaydırma): ortalama −28, en yüksek 71,5. p = 0,007.
- C ve B için p ≤ 0,0005.

**(8) Gerçekçi maliyet** (`y_viop_likidite`). A, VİOP 2021–26:
- Küçük emir (SAHOL 5,7 / AKBNK 5,6 bps): 83,0 (t 4,05).
- 1 mn TL (11,5 / 9,8): 73,3 (3,56).
- 15 bps + tik: 56,6 (2,70).
- **Bireysel tarife** (onbinde 10 + BSMV ≈ 22,5 bps): **51,6 (2,47)**.
- 30 bps + tik: 28,6 (1,34).
- Başabaş maliyet (bacak başına gidiş-dönüş): A ≈50, C ≈75, B ≈105 bps.
- Tam sayı kontrat (küçük emir maliyeti), N_SAHOL = 1/2/3/5/13/39: A t 3,70–4,16, net 80–84 bps. Bugün 1 SAHOL'e 1 AKBNK (oran 0,88).

**(9) Güncel durum** (03.11.2026 kapanışı):
- z = −0,334, β = 0,665. Önceki günler: 02.11 −0,544; 30.10 −0,445; 23.10 +1,479 (eşik altı). k_sahol_a'nın −0,34'üyle ve `sinyal.py` çıktısıyla aynı.
- **Sinyal yok, pozisyon yok.** Fiyatlar değişmezse 04.11 z'si −0,32.
- 04.11 tetikleri (diğer hisse sabitken):
  - z=+1,5: SAHOL ≥86,08 (+%4,40) ya da AKBNK ≤58,35 (−%6,27).
  - z=−1,5: SAHOL ≤80,16 (−%2,78) ya da AKBNK ≥64,94 (+%4,33).
  - Kaynakla 1–2 tik fark.
- VİOP (03.11 uzlaşma):
  - F_SAHOL1126 84,38 (işlem 772 mn TL, açık pozisyon 472 bin).
  - F_AKBNK1126 63,64 (3,6 mlr TL).
  - Oran 0,882; 13 SAHOL'e 11,47 AKBNK.
  - Baz: SAHOL +%2,34, AKBNK +%2,23 (27 gün).
- Teminat: Gedik VİOP bülteni 08.06.2026 tablosunda SAHOL %14, AKBNK %15 doğrulandı. Çift başına ≈2.136 TL.
  - Dikkat: VİOP 2021–26 maks. düşüşü (−2.515 bps) çift başına ≈ −2.120 TL, yani teminatın kendisi kadar.

## Uygulama parametreleri (önerilen)
- Sinyal: adj spot kapanış. r temizliği ±%20,5 / ±%10,5. β = cov250/var250, 1 gün gecikmeli. S = Σ(rS − β·rA); z = (S − ort60)/std60.
- Giriş: |z|>1,5 bölümünün ilk kapanışında, aynı akşam ya da ertesi gün uzlaşmasında (ikisi de çalışıyor).
  - z>+1,5: F_SAHOL SAT, F_AKBNK AL.
  - z<−1,5: tersi.
- Çıkış: A |z|≤1,5 (1–3 gün profili). C |z|≤1 (1–2 hafta).
  - **Zaman sınırı koyma.** A + en çok 3 gün: 33,5 bps (t 1,65); en çok 5 gün: 51 (2,22).
- Kontrat: N_AKBNK = yuvarla(N_SAHOL·β·F_SAHOL/F_AKBNK). Devir vadeye 1 iş günü kala (Kasım için 27.11.2026).
- Boyut: VİOP maks. düşüşü teminata eşit. Çift başına en az 3× teminat (≈6.500 TL) nakit ayrılmalı. Beklenti bugünkü fiyatla çift başına işlem başı ~45–70 TL, yılda ~800–1.250 TL; ileriye dönük gerçekçi beklenti bunun yarısı.

Kaynaklar:
- Seans 09:30–18:10, uzlaşma son 10 dakika VWAP: https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf ; https://www.borsaistanbul.com/data/kilavuzlar/VIOP_vadeli_islem_sozlesmeleri.pdf
- Teminat: https://cdn.gedik.com/cdn/bulletin/2026/06/08/VIOP_Bulten_08062026_dc29d65f.pdf
