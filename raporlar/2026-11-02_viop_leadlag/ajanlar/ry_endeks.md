# ry — YURT İÇİ ENDEKS ajanı: BIST endeksleri ↔ 47 VİOP hissesi

> Not: Bu dosyayı koordinatör yazdı. Ajanın rapor dosyası yazma isteği araç tarafından reddedildi. İçerik ajanın son raporundan alındı; ayrıntılar `f_y_endeks.csv` (1.595 satır, notlar sütununda), `code_y_endeks/results/*.csv` ve `data/isy/` altında.

## Sonuç

Günlük ve saatlik ölçekte işlenebilir bir endeks öncülüğü bulunamadı. 5 dk'daki gecikme mikro yapıdan (fiyat adımı/bayat fiyat) kaynaklanıyor ve işlem maliyetini karşılamıyor. Ana betiklerin hepsi ll v4 ile yeni bir süreçte yeniden çalıştırıldı.

## Veri uyarısı (önemli)

Yahoo'da XU030, XU100, XBANK ve XUSIN dışındaki BIST endekslerinin (XYUZO, XTUMY, XHOLD, XLBNK, sektörler…) günlük geçmişi **tek satır**. Paneldeki bu sütunları kullanan analizlerde ilgili kısım veri bulamadı; sonuç sahte değil, eksik.

Endeks verisi İş Yatırım ChartData'dan indirildi:
- Günlük: 49 endeks, 2000 sonrası.
- Saatlik: 34 endeks ve 47 hisse, 2015 sonrası.
- Kayıt yeri: `data/isy/{d,h1}/`.
- Doğrulama: XU030 getirileri Yahoo ile korelasyon 0,99997; 5 dk barlar Yahoo ile birebir aynı.

## En güçlü 10 bulgu

1. **Senkron yapı ve mekanik içerme (YÜKSEK).**
   - Son 3 yılda medyan R²: XU100 0,40, XYUZO 0,33 (XYUZO hisseyi içermez). En iyi ham endeks 0,56, hisse-hariç endeksle 0,42.
   - Endeks hisseyi içerdiği için R² şişiyor (ham → hisse-hariç):

     | Hisse–endeks | Ham R² | Hisse-hariç R² |
     |---|---|---|
     | TCELL–XILTM | 0,97 | 0,38 |
     | THYAO–XULAS | 0,94 | 0,40 |
     | BIMAS–XTCRT | 0,92 | 0,48 |
     | ASELS–XUTEK | 0,85 | 0,24 |
     | TUPRS–XKMYA | 0,73 | 0,27 |
     | ENKAI–XINSA | 0,69 | 0,09 |

2. **Gerçek sektör faktörü (YÜKSEK).** Hisse-hariç sektör endeksiyle kısmi korelasyon (XU100 kontrollü):
   - YKBNK 0,76, ISCTR 0,74, TRMET 0,74, AKBNK 0,71, GARAN 0,70, TRALT 0,63, VAKBN 0,56, PGSUS 0,53, CIMSA 0,46, OYAKC 0,41, ASTOR 0,40, KRDMD 0,39.
   - Toplam 29/47 hisse ≥0,15'te ve yılların ≥%75'inde aynı işarette.

3. **5 dk'da endeks önde (ilişki ORTA, işlenebilirlik YOK).**
   - XU030 → hisse gecikmeli payın medyanı %12 (Σβ1..6 = 0,13); 47 hissenin 10'unda t>3.
   - Hisse-hariç ile ham endeks arasında fark ≈0, yani etki mekanik içermeden gelmiyor.
   - Fiyat adımı ayrıklığıyla açıklanıyor: Spearman(gecikmeli pay, sıfır-getiri bar oranı) 0,31–0,42. HEKTS ve SASA'da göreli tik ~43 bps.

4. **Saatlikte gecikme yok (2017–2026).**
   - XU030 → hisse gecikmeli pay medyanı ≈0, her yıl ≈0.
   - 2017–20'deki IS gecikmesi düşük fiyatlı hisselerde (TSKB, DOHOL, EKGYO, YKBNK) görülüyor; OOS'ta zayıflıyor (tik etkisi).

5. **Saatlik endeksler arası ilişki (ilişki ORTA, strateji kârsız).**
   - XBANK_{b−1..3} → XUSIN Σβ −0,088 (t −6,5; IS −5,5 / OOS −4,6).
   - XLBNK → X10XB −0,086 (t −4,6).
   - Basit stratejiler kârsız: (X10XB−XLBNK) spread devamı brüt OOS +6,4 bps (t 3,6), bacak başı 4 bps maliyet sonrası −1,7 bps.

6. **Fon krizi, 01.09–30.10.2026 (ORTA).**
   - Getiriler: XU030 −%18,5, XYUZO −%42,4, XTUMY −%53,3.
   - corr(XU030, XTUMY) 0,62 (tüm dönemde 0,72). XTUMY öz-gecikmesi b 0,36 (t 2,6), hacim 0,60×.
   - VİOP hisseleri medyan −%15, VİOP dışı −%38. 15 spekülatif isim −%86…−97 (25–37 taban günü).

7. **Büyük→küçük öncülüğü, Lo–MacKinlay (DÜŞÜK).**
   - Ham asimetri var: corr(Q1_t, Q5_{t−1}) 0,065, corr(Q5_t, Q1_{t−1}) −0,014.
   - Takipçinin kendi gecikmesi kontrol edilince yok oluyor (b 0,00).
   - XU030 → XTUMY −0,08 (t −2,3); işaret yıla göre dönüyor: 2024 +0,29 (t 3,4), 2026 −0,32 (t −4,3).

8. **THYAO_{t−1} → XU030 gün-içi (DÜŞÜK).**
   - b 0,08 (t 2,95; ES/BZ/USDTRY kontrollü 2,8).
   - Backtest, 8 bps: OOS +25 bps/işlem (t 3,0, Sharpe 1,2); IS 2014–20 −1 bps.
   - Son 3 yılda b 0,02 (t 0,4). 47 hisselik taramada FDR'yi geçen yok. Hisse ajanının bulgusuyla aynı yönde.

9. **XU100_{t−1} → hisse gap'i (ilişki ORTA, işlenemez).** Medyan +0,057, 7 hissede t>3. Gün-içi −0,014.

10. **XU030 son saat → ertesi gün-içi dönüş (ÇOK DÜŞÜK).** 8 bps sonrası OOS +11,8 bps (t 0,9).

## Olumsuz bulgular

- **Günlük endeks_{t−1} → hisse** (kendi gecikmesi ve XU100_{t−1} kontrollü): 12.726 test.
  - FDR'yi geçen: cc 0, gün-içi 0, gap 1 (BIMAS–XTCRT, w 0,63, mekanik).
  - |t|>3 oranı %0,6–0,9; null'da %0,4.
- **Hisse → endeks:** 2.350 testte 0 FDR. **Endeks → endeks:** 2.450 testte 0 FDR.
- **Backtestler (8 bps):**

  | Strateji | Sonuç |
  |---|---|
  | Sektör yakalama L/S | OOS −10 bps (t −2,2) |
  | Sektör momentumu L/S | −10,5 bps |
  | XU030 → illikit gün-içi | +1,6 bps |
  | 5 dk şok | brüt 5,5 bps, net OOS −8,6 bps; OOS'ta pozitif kalan 3/47 |

## v4 temizlik düzeltmesinin etkisi

- |t| farkının medyanı 0,08; FDR sayıları değişmedi (gap 2→1).
- THYAO t 3,17 → 2,95.
- Evren 217 hisseye genişlediği için hacim beşlisi Q5'in fon krizi getirisi −%38,6'dan −%54,8'e değişti (spekülatif isimler girdi).

## Açık sorular

- NNLS ağırlıkları, bileşeni eksik endekslerde (XHOLD/XUSIN) yaklaşık. KCHOL'un XHOLD ağırlığı 0,07 çıktı; muhtemelen olduğundan düşük tahmin.
- İş Yatırım 5 dk (2024+) indirmesi sunucu yavaşlığı yüzünden iptal edildi; 5 dk sonuçları yalnız ~60 güne dayanıyor.
- VİOP gün-içi verisi olmadığı için vadeli–spot öncülüğü test edilemedi.

## TradingView kodları

- tv_map'te olmayan 23 endeks sayfası doğrulandı (HTTP 200): BIST:XYUZO, BIST:XTUMY, BIST:XKTUM, BIST:XK030, BIST:XTMTU, BIST:XHARZ, BIST:XSD25, BIST:XMESY, BIST:XKURY (kurumsal yönetim endeksi, ölçek endeksi değil), BIST:XKOBI …
- Endeks vadelileri: BIST:XU030D1!, BIST:XLBNKD1!, BIST:X10XBD1!, BIST:XSD25D1!.
