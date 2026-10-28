# HİSSE — 2. Tur (28.10.2026)

Etiketler: [D] doğrulanmış, [H] benim hesabım, [T] tahmin.
Ana veri: Borsa İstanbul VİOP bülteni 27.10 (`https://www.borsaistanbul.com/data/vadeli/viop_20261027.csv`; 28.10 dosyası henüz yayımlanmamış) ve Yahoo'dan 3 yıllık günlük kapanışlar.

## 1. Garanti 3Ç 2026: AÇIKLANMADI
Bu turu yazarken KAP'ta ya da haberlerde Garanti'nin 3Ç 2026 sonucu yoktu; en güncel haber hâlâ "bu akşam bekleniyor" diyor [D] https://tr.investing.com/news/stock-market-news/akbankn-kar-18-geriledi-sra-garantide-beklenti-3231-milyar-tl-4123374. Yatırımcı ilişkileri sayfasında en son 1Ç26 duyurusu var; bulduğum "9 aylık" haber 2025'e ait.

- **Konsensüs:** medyan 32,31 mlr TL (Deniz 32,54, Şeker 32,7, Ak 31,2) [D].
- **Ön koşul aynen geçerli:** net kâr ≥30 mlr TL ve NIM en az yatay. <29 mlr gelirse iptal. 30.10 açılışından önce kontrol edilecek.

## 2. Kendi hatalarım
1. **Yanlış vade seçmişim.** Pay vadelileri aylık açılıyor ve likidite Kasım vadesinde. 27.10 verisi:
   - **F_GARAN1126:** 46.467 kontrat, açık pozisyon 102.845. **F_GARAN1226:** yalnızca 134 kontrat, açık pozisyon 687.
   - **YKBNK:** Kasım 730 bin kontrat, Aralık 1.571 kontrat [D, bülten].
   - Sonuç: pair **F_GARAN1126 / F_YKBNK1126** ile kurulmalı. Vade 30.11, fiziki teslimat; en geç 26.11'de kapatılacak.
2. **Likidite sıralamam yanlıştı.** 27.10 pay vadeli işlem hacimleri (mn TL): YKBNK 6.641, AKBNK 6.274, ASELS 5.820, THYAO 4.584, SAHOL 4.309, ISCTR 3.621, GARAN 1.734 [D]. Bankalar arasında en az likit olan GARAN; SAHOL ise sanılandan likit.
3. **Bazı abartmıştım.** Aralık bazını +%6,2 varsaymıştım; gerçekleşen değer GARAN için +%5,4, YKBNK için +%5,3 (yıllık %31). Kasım bazı +%2,4–2,5 [H]. Taşıma maliyeti buna göre küçülüyor.

## 3. Faiz duyarlılığı: pair fiilen "short faiz indirimi" mi?
Hesap: PPK günlerinde GARAN − 0,85×YKBNK günlük getirisi [H, Yahoo].

| Gün | Karar | Pair | XBANK |
|---|---|---|---|
| 26.12.2024 | −250bp (ilk indirim) | **−3,14%** | +6,18% |
| 23.01.2025 | −250bp | −2,30% | −1,95% |
| 06.03.2025 | −250bp | −0,77% | +0,36% |
| 24.07.2025 | −300bp | −1,72% | +1,12% |
| 11.09.2025 | −250bp | −1,43% | −2,89% |
| 23.10 / 11.12.2025 | −100 / −150bp | −0,18 / +0,11% | |
| 22.01.2026 | −100bp | −0,16% | |
| 22.10.2026 | −100bp | −0,52% | −3,62% |

- **Faiz indirimi günleri:** 9 indirimin **8'inde pair negatif**; ortalama −%1,12, medyan −%0,77. Sabit tutma günlerinde ortalama ~0.
- **Diğer günler:** Ekim TÜFE açıklama günlerinde (n=34) pair'in XBANK betası +0,08 (korelasyon 0,18), yani anlamlı değil. Tüm günlerde banka faktörüne beta −0,05 ile −0,09 arasında.

**Sonuç:** Evet, pair karar günlerinde "short faiz indirimi" pozisyonu. MAKRO'nun itirazı veriyle doğrulandı. Ancak risk büyük ölçüde PPK gününde yoğunlaşıyor. **Kasım vadesi 10.12 PPK'dan önce kapandığı için bu risk pencere dışına çıkıyor.** Kalan risk: düşük TÜFE (3.11) sonrası beklentilerin yeniden fiyatlanması. ŞEYTAN'a göre 2 yıllık tahvil %39,8 ve politika faizinin üstünde; yani güvercin yönlü yeniden fiyatlama için yer var.

## 4. SAHOL ve tasfiye → Fikir 2 GERİ ÇEKİLDİ
- **SAHOL'a dönük tasfiye baskısı küçük, muhtemelen büyük ölçüde geride.** Gedik: tasfiyedeki fonlarda likit hisse pozisyonu yalnızca 32,5 mlr TL (101 hisse; toplam hisse pozisyonlarının ~%10'u) ve "kısa sürede satılabilecek" türden. 60 günü aşan yük likiditesi sınırlı 123 hissede (ilk 10'u tutarın %86'sı) [D] https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf. ENDEKS'in "60+ gün" uyarısı SAHOL için değil, küçük hisseler için geçerli.
- **Ancak katalizör zayıf.**
  - Geri alım fiilen günde ~290 bin lot, yaklaşık 25 mn TL. Toplam 876 bin lot, sermayenin %0,04'ü [D] https://www.borsatek.com/sahol-27-ekimde-geri-alim/. Bu, SAHOL vadelisinin günlük hacminin (4,3 mlr TL) ~%0,6'sı; akış değil, sinyal.
  - NAV iskontosu %60, 1 yıllık ortalama %58: ciddi bir sapma yok.
  - SAHOL piyasa değeri / Akbank payı oranı 1,31; 1 yıllık medyan 1,27. Akbank'a göre ucuz değil.
- Avantaj kanıtlanamadı, **izleme listesine alındı.** Tetik: iskonto ≥%65.

## 5. Revize Fikir 1: Long F_GARAN1126 / Short F_YKBNK1126
**Fiyatlar** (28.10 spot, Kasım vadelisi 27.10 bazıyla tahmin [H]): GARAN 126,70 → ~129,7; YKBNK 34,48 → ~35,35.

| | Tam boy (18 / 56) | 1. dilim (9 / 28) |
|---|---|---|
| Long nominal / Short nominal | 233,4k / 197,9k TL (oran 0,848) | 116,7k / 99,0k TL |
| Net β (XU030), β250 / β60 | +2,0k / +24,9k TL (≈0 / 0,11×) | +1,0k / +12,4k TL |
| Net β (XBANK) | −4,6k TL | −2,3k TL |
| Teminat (%14,4 / %15,8) | 64,9k TL (%6,5) | 32,4k TL |
| Stop'ta zarar (pair −%4) | **9,3k TL (%0,93)** | 4,7k TL |
| Hedef (+%6) | 14,0k TL | 7,0k TL |
| **YKBNK +%8 gap, GARAN yatay** | **−15,8k (%1,58)** | −7,9k (%0,79) |
| YKBNK +%8 gap, GARAN +%3 (birlikte hareket) | −8,8k (%0,88) | −4,4k |
| YKBNK +%8 gap, GARAN −%2 (en kötü) | −20,5k (%2,05) | −10,3k (%1,03) |

- **Gap senaryosunun bağlamı:** Son 3 yılda YKBNK'nin XBANK'a göre kendine özgü günlük hareketinde 99. yüzdelik +%2,3, en büyük mutlak hareket %5,7 [H]. Yani +%8 uç bir stres senaryosu.
- **Değişiklikler:**
  - Giriş iki dilime bölündü: 30.10'da %50 (Garanti koşulu sağlanırsa), kalan %50 YKBNK sonucundan sonra 4.11'de. 4.11 girişi için şart: YKBNK swap düzeltmeli NIM'de ≥+30bp sürpriz olmaması.
  - Süre 26.11'e kısaldı.
  - Taşıma maliyeti ~0,9k TL.
- **Aynı kalanlar:** Hedge oranı 0,85; oran bazında stop/hedef (spot GARAN/YKBNK oranı 3,675 → stop ~3,52, hedef ~3,90).
- **Güven: 5 → 4,5.** Faiz indirimi günü betası teyit edildi ve Garanti sonucu hâlâ bilinmiyor.

## 6. Diğer ajanların fikirleri
| Fikir | Olgu kontrolü | Mantık / boyut | Oy |
|---|---|---|---|
| **MAKRO-1:** Short F_USDTRY1226 | 27.10 uzlaşma **52,516** [D, bülten], 52,47 iddiasıyla tutarlı; teminat 0,11×52,5k=5,77k ✓ | Stop riski 6×730 = 4,4k (%0,44) ✓. **Hata:** "+%12 gap = −3.258/kontrat" hesabı vadelinin spota yakınsadığını varsayıyor. Gerçekçi gap'te vadeli de ~%12 sıçrar → ~−6,3k/kontrat; 6 kontratla %3,8. Bu, %2,5'lik stres sınırını aşıyor → **en fazla 4 kontrat** | **KOŞULLU EVET 6** — taşıma verisi sağlam, boyut stres sınırına göre küçültülmeli |
| **MAKRO-2:** Koşullu long F_XU030 | Koşullar ölçülebilir | 0,5–1 kontrat, stop %6 → ~8,8k ✓. ENDEKS'in short'uyla aynı anda tetiklenemez | **KOŞULLU 4** — koşullar gelirse |
| **ENDEKS-1:** Rallide short F_XU0301226 | Aralık 27.10: uzlaşma 14.638 / kapanış 14.643 ✓; XU030/XU100 1,195→1,250 ✓; XU100 9.09 kapanışı 14.505,5 ✓ | 1 kontrat, stop 450–500 puan → 4,5–5k ✓. Vadeli teorik değerin ~%1,3 altında → short ~190 puan baz riski taşıyor (MAKRO) | **EVET 5** — limit emirle, boyut doğru |
| **ENDEKS-2:** Dipte long | — | Beklenen değer maliyet sonrası ~0 (kendisi de söylüyor) | **HAYIR 3** |
| **OPSİYON-1:** Koşullu 14.500 straddle | C14500 uzlaşma 627,8 / kapanış 329,6; P14500 482,0 / 180 → straddle 1.110 / 510 ✓ [D]. Ancak P14500 kapanışı yalnızca 266 kontrata dayanıyor, bayat olabilir | 10 straddle ≤800 → %0,8 ✓; ATM≈0,8·F·σ·√T ile 800 ≈ σ %16,6 ✓ | **KOŞULLU EVET 6** |
| **OPSİYON-2:** 14.500/15.500 boğa call spread | 380 / 269 ✓ | Short'larla ters yönde, sigorta niteliğinde | **KOŞULLU 4** — yalnızca short'lar dolarsa hedge olarak |
| **ŞEYTAN:** Rallide short | Brent 111,3 $ ✓, ABD 10 yıllık %4,99 ✓ [Yahoo]. **Hata:** "tarihi zirve 14.601 / 9 Eylül 14.405" doğru değil: XU100 28.08 kapanışı 14.641,6, 11.05 kapanışı 15.133,5, 9.09 kapanışı 14.505,5 [H] | 7 kontrat/5 mn: 675×10×7 = 47,3k (%0,95) ✓. Açığa satış yasağı spot piyasayla ilgili; VİOP short'larını kilitlemez [T] | **EVET 5** — ENDEKS-1 ile aynı kova |

## 7. Komite portföyü (OPSİYON bütçesi: fikir başına ≤%1, toplam ≤%4, korelasyonlu kova ≤%2)
| Sıra | Pozisyon | Risk | Not |
|---|---|---|---|
| 1 | MAKRO short F_USDTRY1226, **4 kontrat** | %0,3 (stres %2,5) | En yüksek kazanma olasılığı |
| 2 | OPSİYON straddle (IV koşulu sağlanırsa) | %0,8 | TL şokunda ve sert rallide kazanır; 1 ve 3'ün kuyruklarını dengeler |
| 3 | ENDEKS + ŞEYTAN birleşik rallide short (tek kova) | %1,0 | TL şokunda MAKRO'nun zararını dengeler |
| 4 | HİSSE pair (Garanti koşuluyla, dilimli giriş) | %0,9 | Piyasa-nötr; faiz indirimi günü riski pencere dışında |
| **Toplam** | | **%3,0 ≤ %4** | |

**Ortak stres** (BIST −%15, banka −%18, USDTRY +%8): USDTRY short −%1,7, endeks short'ları +%2–4 (dolmuşlarsa), pair ±%1, straddle pozitif → net ≈0 ya da pozitif [T]. **Zayıf senaryo:** ralli + TL istikrarı; short'lar stop olur (−%1).
