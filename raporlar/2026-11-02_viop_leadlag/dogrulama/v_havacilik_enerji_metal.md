# v_havacilik_enerji_metal — bağımsız doğrulama notları (02.11.2026)

Kod: `out/code_v_havacilik_enerji_metal/` (vlib.py = kendi hizalama/temizlik kütüphanem, ll.py import EDİLMEDİ; s1_sync → s2_hourly → s3_freq → s4_extra → s5_reconcile). Çıktılar: `res/` (s1_sync.csv, s2_night.csv, s2_sync1500.csv, *.txt).

## Yöntem (bağımsız)
- Günlük: ham parquet, BIST takvimi = XU100 hacimli günleri; sürücü = yerel tarihi ≤ t son kapanış (ffill). FX '=X': EURUSD h1 ile **kendim doğruladım** (günlük c(ldate t) ↔ t günü 00:00 UTC fiyatı medyan 2,3 bp; 15:00 UTC ile 21 bp) → 1 gün kaydırdım.
- BIST temizlik: log getiri > ln1,105 veya < ln0,895 → NaN. Sürücü: |r| > 12×önceki 250g std → NaN.
- Gap = ln(o_t/c_{t−1}) ham fiyat; temettü/bölünme günleri (adj/c oranı değişimi) gap'te NaN; bozuk açılış (o = önceki c ve h = l) NaN; 2014 öncesi NaN. Daily o, h1 06:30 barı açılışıyla %99,9 aynı.
- Kontrol setleri: K1 = XU100; K3 = XU100 + USDTRY + EEM; K4 = K3 + bölge/sektör (Avrupa: ^STOXX; ABD/emtia: ES=F; BIST çiftleri: XBANK + XUSIN). Dönemler: tam 2010+, IS 2014–2020, OOS 2021–2026, 1y 31.10.2025+. Not: 1. tur ajanlarının IS'si **2010–2020** idi (THYAO–LHA IS 0,141 ile birebir uzlaştı).
- Saatlik: sürücü fiyatı tam 15:00 UTC'de (BIST kapanışı) ve 06:00 / 07:00 / 21:00 UTC'de; BIST tarafı günlük o/c.

## Sonuç tablosu (pc = XU100 kontrollü kısmi korelasyon)
| İddia | Yeniden üretim (tam / IS14-20 / OOS / 1y) | Yıl işareti | K3 / K4 | Not | Karar | Güven |
|---|---|---|---|---|---|---|
| A1 THYAO–LHA | 0,180 / 0,183 (IS10-20 0,141) / 0,241 / 0,331 | 16/17 | 0,187 / 0,207 | 15:00 UTC senkron pc 0,222 (std 0,219) → gerçek senkron | KABUL | YÜKSEK |
| A1 THYAO–EZJ | 0,160 / 0,166 / 0,208 / 0,163 | 15/17 | 0,165 / 0,174 | +Brent kontrolü 1y 0,03 | KABUL | YÜKSEK |
| A1 THYAO–IAG | 0,151 / 0,133 (IS10-20 0,111) / 0,222 / 0,319 | 16/17 | 0,157 / 0,171 | eşikte | KABUL | YÜKSEK/ORTA sınır |
| A1 PGSUS–EZJ | 0,169 / 0,159 / 0,206 / 0,217 | 12/14 | 0,174 / 0,188 | +Brent 1y 0,08 | KABUL | YÜKSEK |
| A2 THYAO–PGSUS | 0,501 / 0,474 / 0,573 / 0,617 | 14/14 | 0,501 / 0,484 | XULAS (h1, 2023-12+) kontrolü 0,03'e indiriyor: mekanik (endeks ≈ bu iki hisse) | KABUL | YÜKSEK |
| A3 TAVHL–ADP | 0,131 / 0,127 / 0,183 / 0,351 | 15/17 | 0,133 / 0,134 | haftalık 0,143, yıl 11/17 | KABUL | ORTA |
| E1 TUPRS–CRAK | 0,172 / 0,145 / 0,221 / 0,352; hft 0,316 | 11/11 | 0,246 / 0,261 | **CRAK, TUPRS'u ~%3,9 içeriyor**. CRAK'ın TUPRS_usd yüklemesi 0,038 (t 8,1; 17 rafineri kontrollü). Ex-TUPRS (w=0,04): 0,121 / 0,099 / 0,164 / 0,289; hft 0,268; yıl 10/11; K4 0,194. AB rafineri sepeti (içerme yok): 0,138 (IS 0,125 / OOS 0,256) | DÜZELT | ORTA |
| E2 TUPRS–BZ=F | 0,158 / 0,101 / 0,258 / 0,453; hft 0,269 (IS 0,18 / OOS 0,40) | 14/17 | 0,168 / 0,169 | aylık USD 0,350 (IS 0,13 / OOS 0,505; 2026 hariç 0,257). 15:00 senkron 2024+ pc 0,39 | KABUL | YÜKSEK (rejime bağlı büyüklük) |
| E4 Brent gece → TUPRS gap | corr 0,577 (NW-t 5,6), XU100 gap kontrollü 0,664, n=558 | yarıyıllar: 0,18 / 0,55 / 0,22 / 0,82 / 0,32 (hepsi +) | — | büyük hareket ağırlıklı: \|Brent\|>%1 0,62, küçük 0,10; Spearman 0,36; β 0,24. Pencere: 15–21 UTC 0,35, 21–06 UTC 0,43, 15→06 0,56. Gün-içi −0,09 (t −1,4); 2026Y1 −0,26 (kısmi geri dönüş) | KABUL | ORTA |
| E5 AKSEN–aylık PTF | USD 0,255 / 0,277 / 0,237 (n 153) | 11/13 (2022 −0,30) | K3: 0,220 (OOS 0,144) | TL+USDTRY 0,232; mevsimsellik arındırılmış 0,269; dairesel kaydırma null p<0,01 (%95 0,157); öncülük yok (−0,13). 2018 PTF ort. 231,64 tuttu (veri 3. taraf EPİAŞ dökümü) | KABUL | ORTA |
| M1 EREGL–ISDMR | 0,446 / 0,283 / 0,578 / 0,460 | 10/11 | 0,442 / 0,383 | ISDMR verisi 2016-04+; gecikme ±0,01 (bayat fiyat yok) | KABUL | YÜKSEK |
| M1 EREGL–KRDMD | 0,327 / 0,260 (IS10-20 0,198) / 0,520 / 0,469 | 15/17 | 0,325 / 0,252 (IS 0,144) | XMANA (h1) kontrolü ≈0: mekanik (endeks bu hisseleri içeriyor) | KABUL | YÜKSEK |
| M2 TRALT–GC=F | 0,214 / 0,193 / 0,191 / 0,335 | 17/17 (günlük) | 0,215 / 0,209 | haftalık yıllık: 2021 −0,05, 2022 0,05, 2023 −0,03, 2024 0,15, 2025 0,11, 2026 0,39 (iddia 2023 −0,11 / 2026 0,49 tam tutmadı). Yarıyıllık günlük pc 2023Y2–2024Y2 ≈0 | DÜZELT (sayılar) | YÜKSEK (rejim notuyla) |
| M3 altın gece → TRALT gap | 15→06 UTC: corr 0,420, pc 0,426, β-artık 0,422 (NW-t 6,3); 15→07: 0,453 | yarıyıllar: 2024Y2 0,12, 2025Y1 0,01, 2025Y2 −0,02, **2026Y1 0,81, 2026Y2 0,61** | — | Etkinin tamamı 2026'dan (~190 gün). Gün-içi devam yok (0,03). İşlenemez | DÜZELT | DÜŞÜK |
| M5 EREGL–AB çelik(4) | 0,128 / 0,115 / 0,148 / **0,038** | 17/17 | 0,119 / 0,119 | tekil 0,09–0,12; hft 0,254. Yarıyıllık: 2025Y2 −0,03, 2026Y1 0,08, 2026Y2 0,00 → son 1 yılda bağ kayboldu | DÜZELT | ORTA (günlük) |
| M5 aylık SLX / MT.AS | 0,410 / 0,392 / 0,517 ; 0,406 / 0,455 / 0,485 (TL, 2008+) | 16/19, 17/19 | K4 0,356 / 0,325 | son 36 ay 0,40 / 0,34 | KABUL | YÜKSEK |

## Zamanlama bulguları
- Avrupa sürücülerinde günlük "senkron" ilişki, 15:00 UTC anlık fiyatla yeniden ölçüldüğünde değişmiyor. Yani BIST kapanışından sonraki 0,5–1,5 saatin ürünü değil.
- Avrupa havayolu (t−1) → THYAO gün-içi (t): XU100 gün-içi, kendi gecikmesi ve XU100(t−1) kontrollü pc 0,07–0,08 (NW-t 3,6–4,3). IS ve OOS'ta da var. PGSUS'ta EZJ ve IAG ile aynı sonuç (t 3,1–3,4). TAVHL'de zayıf. Bu, 1. turun 4 numaralı bulgusunu (işlenebilir öncülük) destekliyor.
- Brent ve altın gece hareketi açılışta fiyatlanıyor; gün-içine taşmıyor. VİOP pay vadelisinin akşam seansı olmadığından nakitte işlenemez.

## Genel uyarılar
1. Hisseyi içeren sektör endeksleri (XULAS, XMANA) BIST çift korelasyonunu mekanik olarak sıfırlıyor. Yahoo'da bu endekslerin (ve XELKT'nin) günlük verisi yok (1 satır); yalnız h1 var (2023-12+).
2. CRAK, TUPRS'u içeriyor (MarketXLS 01.10.2026: %3,91). E1 büyüklüğünün ~%30'u mekanik.
3. 2026 savaş rejimi E4, M3 ve E2 (aylık) büyüklüklerini şişiriyor. M3 tamamen 2026'ya bağlı.
4. Son 1 yılda havayolu–EZJ ortak hareketi Brent kontrolüyle neredeyse kayboluyor (THYAO–EZJ 0,03). Yakın dönemdeki bağ ortak petrol şokundan geliyor.
5. ENJSA–PTF: ilişki yok. ODAS–PTF: zayıf (0,12; OOS 0,08).
