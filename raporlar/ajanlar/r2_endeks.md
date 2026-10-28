# ENDEKS — 2. Tur (Çapraz Kontrol) | 28.10.2026

Etiketler: [D] birincil kaynak · [H] kendi hesabım (`scratchpad/scripts/trigger.py` ve önceki betikler) · [T] tahmin. Birincil kaynak: Borsa İstanbul VİOP günlük bülteni `https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv`.

## 1. Kendi hatalarım
- **Tarih karışıklığı:** 1. turda kullandığım 14.649 (Aralık) ve 13.986 (Ekim) 28.10 fiyatı değil, **27.10'a ait**. TradingView'daki −%0,34/−%0,45 değişim ve 314.401/210.894 açık pozisyon (OI) 27.10 bülteniyle birebir aynı [D]. Bunları 28.10 spotuyla eşleştirmiştim.
  - Doğru eşleşme 27.10: Aralık resmi uzlaşma **14.638** (kapanış 14.643), spot 13.934,7 → zımni faiz %28,3.
  - Doğru eşleşme 28.10: son işlem ~14.644 (Foreks, MAKRO ve ŞEYTAN'dan), spot 13.960,9 → zımni faiz **%27,9**.
  - Sonuç değişmiyor: baz yapısal, MAKRO da Temmuz için %28,7 buldu.
  - **28.10 resmi uzlaşma fiyatı bulunamadı.** `viop_20261028.csv` henüz yayımlanmamış, şimdilik geçerli rakam 14.644 (son işlem).
- **Boyut ifadesi:** "Risk %0,75" gap tamponlu bütçeydi: 0,75% × 1 mn = 7.500 TL; 7.500 / (450 × 10 × 1,5) = 1,11 → 1 kontrat. Gerçek stop riski **%0,45**; fark tam sayıya yuvarlamadan geliyor. Doğru ifade: 10 mn TL → 11 kontrat → stop %0,50, 1,5× gap %0,74.
- **Zirve [D+H]:**
  - XU100 Eylül kapanış zirvesi **9 Eylül 14.505,5**. Yahoo'nun 8 Eylül kapanışı (14.405,3) ve 9 Eylül açılışı (14.381,2), AA/Mynet'in verdiği rakamlarla aynı; seri hizalı. Gün içi zirve 14.673.
  - XU030'un Eylül kapanış zirvesi 11 Eylül'de 17.247,4.
  - Tüm zamanların kapanış zirvesi **11 Mayıs 2026, 15.133,5**.
  - Bu ayrımla diğer ajanların değerleri: OPSİYON'un 14.467'si XU100'ün 11 Eylül kapanışı (XU100 için zirve değil). ŞEYTAN'ın 14.405'i 8 Eylül kapanışı. "14.601" hiçbir seride yok.
- **Fikir 2'yi (dip testinde long) geri çekiyorum.** Carry sonrası beklenen değeri sıfıra yakın; yukarı yönlü dışbükeyliği OPSİYON'un straddle'ı daha iyi veriyor.

## 2. Bana özel çelişkiler
**2.1 HİSSE'nin itirazı: short squeeze.**
- XU030 ağırlıkları (27.10, borsaveyatirim; üçüncü taraf kaynak): ASTOR 2,77, SASA 1,36, TRALT 1,05, GUBRF 0,71, TRMET 0,61 → **toplam %6,5**. Ağırlık ASELS (15,1), TUPRS (12,9), BIMAS (11,1) ve bankalarda (~%22).
- Bu 5 hissenin XU030'un günlük getirisine katkısı (ağırlık × getiri), 15.09–28.10 arası [H]:
  - Hiçbir gün **±0,58 puanı** aşmadı.
  - 20.10'daki +%3,15'lik günde katkıları +0,23 puan.
  - 23→28.10 arasında ASTOR +%24 yükseldi, ama 5 hissenin toplam katkısı yalnızca +0,48 puan.
- Squeeze aritmetiği:
  - Spotun +%3 (≈ girişin karşılığı) yalnızca bu hisselerle gelmesi için hepsinin ortalama **+%46** yükselmesi gerekir. Stop seviyesi için +%100 gerekir.
  - "Rallinin büyük kısmı squeeze'den gelir" olasılığı **<%20** [T].
  - Girişten sonra bu 5 hissede ek +%30 ≈ endekste +%2 ≈ 290 puan; bu, 560 puanlık stop mesafesinin altında. **Tez bu riski kaldırıyor.**
  - Asıl risk ASELS: 3Ç beklentiyi geçti, 23.10'dan beri +%6,1, endekse +0,9 puan katkı.

**2.2 Tetiklenme olasılığı ve koşullu olasılık [H].** Varsayımlar: F0 = 14.644, carry kayması ≈ −%27,9/365 günlük, 1,5 günlük tatil ≈ +1 günlük varyans, 11 işlem günü (13.11'e kadar).

| Seviye | Spot karşılığı | σ=%22 | **σ=%27** | σ=%32 | Ampirik koşulsuz | Ampirik kriz durumu |
|---|---|---|---|---|---|---|
| 14.900 | +%2,2 | 0,64 | **0,72** | 0,76 | 0,68 | 0,82 |
| 15.050 | +%3,2 | 0,48 | **0,57** | 0,64 | 0,56 | 0,73 |

- En az bir kademenin dolma olasılığı ~**%65–70**. Dolmazsa beklenen değer sıfır (nakit faiz kazanır); kayıp yalnızca ayrılmış ama kullanılmamış risk bütçesi.
- Beklenen değer ≈ P(dolum) × EV|dolum ≈ 0,67 × (+0,24R) ≈ **+0,16R**. İnce bir pozitif.
- **Koşullu olasılık sorunu gerçek:** Dar bir ralli (ASELS ve fon hisseleri) bilgi taşımaz. Geniş bir ralli (bankalar önde, yabancı girişi var) krizin bittiğini gösterebilir. Tarihsel simülasyonda dolum sonrası hedef oranı %44 (n=16, ±12 puan); bunu ayıramıyor. Bu yüzden aşağıdaki **kompozisyon filtresini** ekliyorum.

## 3. Diğer fikirler: kontrol ve oy
| Fikir | Olgu kontrolü | Mantık / risk hesabı | Oy |
|---|---|---|---|
| **MAKRO-1** short F_USDTRY1226 | 27.10 uzlaşma 52,516, OI 895 bin [D] ✓. Stop: 0,70 TL × 1.000 + kayma = 730 TL × 6 = %0,44 ✓ | ✗ "+%12 gap = −3.258 TL/kontrat" yanlış: +%12 → **−6.300 TL** × 6 = **−%3,8**. OPSİYON stresinde (+%8) −4.200 × 6 = −%2,5, sınırda → 1 mn TL'ye **5 kontrat**. Artısı: TL şokunda XU030 short'u doğal hedge (Mart 2025: XU030 3 günde −%17,5) | **EVET (5 kontrat), 6/10.** Pozitif carry, kuyruğu portföyde dengelenir |
| **MAKRO-2** koşullu long XU030 | Rakamlar ✓ | ✗ Vadeli hedefi 16.100 → vadeye yakınsama nedeniyle spot +%11–15 gerekiyor. Carry kaymalı Brown hareketinde P(+%10 önce −%6) ≈ **%25**, %45 değil → EV negatif | **HAYIR, 3/10.** Hedef +%6 ve 4 hafta olursa yeniden bakılır |
| **HİSSE-1** GARAN/YKBNK | Yahoo: 126,7 / 34,48 ✓. 18×100×134,6 = 242 bin; −%4 = %0,97 ✓. ✗ Baseline'daki "−19,5/−23,2" doğruydu: 11.09→23.10 penceresi (XU030 −%19,56, XU100 −%23,16) [H] | YKBNK 3.11 bilançosu tutma süresi içinde, gap stopu atlar. YKBNK'nin XU030 ağırlığı (%4,34) GARAN'ınkinden (%2,81) büyük → endeks akışına daha açık | **KOŞULLU (GARAN ≥30 mlr), 5/10**; risk %0,75'e indirilmeli |
| **HİSSE-2** SAHOL/AKBNK | Oran 1,321 ✓ | 23.10'dan beri SAHOL −%4,3, AKBNK −%0,6 → şimdiden aleyhte. SAHOL tasfiyedeki fonlarda en yaygın BIST 30 payı; carry beklenen değeri yiyor | **HAYIR, 3/10** |
| **OPSİYON-1** straddle ≤800 | Bülten ✓: C14500 kapanış 329,6 / uzlaşma 627,8; P14500 180 / 482. P15500 VWAP 793, iskontolu içselin (~809) altında; OI +23.316 → yapılandırılmış akış | Uzlaşma–işlem farkı gerçek; ≤800 ≈ σ%16–17. Likidite ince (P14500 hacmi 266) | **EVET, 7/10.** Yön belirsizliğine ve gap'e en uygun fikir |
| **OPSİYON-2** 14500/15500 boğa call spread | Kapanış 329,6 − 60,4 = 269 ✓ | Adil fiyatta EV ≈ 0, carry aleyhte; yalnız short'a hedge olarak anlamlı | **KOŞULLU, 4/10** (≤280 ve short açıksa) |
| **ŞEYTAN** ralliyi sat | 7 kontrat × 675 × 10 = 47.250 = %0,95 ✓ | ✗ "Baz iskontosu = kalabalık short" yanlış: zımni faiz 2026 boyunca %24–33, yapısal. Kapanış bazlı stop gap riskini olduğundan küçük gösteriyor; tutma süresinin 24.12'ye uzaması PPK (10.12) gap'ini içine alıyor | **EVET (benimkiyle tek kova), 5/10** |

## 4. Revize fikir: birleşik "ralliyi sat" (ENDEKS + ŞEYTAN, tek kova)
- **Enstrüman ve giriş:** F_XU0301226, short. Kademeler **14.900 / 15.075**, son geçerlilik 13.11. 30.10'da ilk 30 dakika işlem yok.
- **Kompozisyon filtresi:** Giriş anında XBANK, 28.10'dan beri XU030'u >2 puan geçiyorsa **ve** TCMB verisi >200 mn $ yabancı hisse alımı gösteriyorsa girme: bu geniş yeniden fiyatlama.
- **Zarar-kes:** Gün içi sert stop **15.550**; kapanış bazlı değil. Gap sigortası: long C15500 yalnızca ≤100 puandan (27.10 kapanış 60,4, uzlaşma 247).
- **Hedef ve süre:** T1 14.100 (yarısı), sonra stop girişe çekilir; T2 13.700. Süre en geç **04.12**.
- **Boyut:** Ortalama giriş 14.988, stop 15.550 → 562 puan = 5.620 TL/kontrat. 10 mn TL için 11 kontrat: stop riski %0,62, 1,5× gap %0,93 ≤ %1 kova limiti. 1 mn TL için 1 kontrat (%0,56).
  - 1 kontrat: nominal ~150 bin TL, teminat ~17 bin TL (PSR %11,4).
- **Getiri/risk ve beklenen değer [T]:** Harmanlanmış getiri/risk 1,9. EV|dolum ≈ +0,24R; koşulsuz ≈ +0,16R.
- **Güven: 4/10** (değişmedi).

## 5. Komite portföyü (fikir başı ≤%1, toplam ≤%4, korele kova ≤%2)
| Sıra | Pozisyon | Stop/prim riski |
|---|---|---|
| 1 | OPSİYON-1 straddle (koşullu ≤800) | %0,8 |
| 2 | MAKRO-1 short USDTRY, 5 kontrat / 1 mn | %0,37 (+%8 stresinde %2,1) |
| 3 | ENDEKS+ŞEYTAN short XU030 | %0,62 (gap tamponlu %0,93) |
| 4 | HİSSE-1 pair (koşullu) | %0,75 |
| | **Toplam** | **%2,54** (gap tamponlu ~%3,4) ≤ %4 ✓ |

- **Ortak stres (BIST −%15, bankalar −%18, USDTRY +%8)** [H, kaba]: XU030 short +%2,5, straddle +%1,35, USDTRY short −%2,1, pair ~−%0,5 → **net ≈ +%1,2**.
- **Squeeze senaryosu:** XU030 short kaybeder, straddle ve USDTRY short (TL rallisinde) dengeler.
- Net hisse deltası ≈ −%16, sınırın (≤%50) içinde.
- **Dışarıda kalanlar:** MAKRO-2, HİSSE-2, benim Fikir 2'm (geri çekildi). OPSİYON-2 yalnız short hedge'i olarak.

**Kaynaklar:** BIST bülteni https://www.borsaistanbul.com/data/vadeli/viop_20261027.csv (ayrıca 20260908–20261026 arası) · Ağırlıklar https://www.borsaveyatirim.com/bist-30-hisselerinin-endeks-agirliklari · 8–9 Eylül AA https://finans.mynet.com/haber/detay/borsa/canli-borsa-borsa-gune-dususle-basladi-9-eylul-2026-bist-100/573366/ · Yahoo https://query1.finance.yahoo.com/v8/finance/chart/XU100.IS
