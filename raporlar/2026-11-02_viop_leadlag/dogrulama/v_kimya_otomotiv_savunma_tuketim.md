# v_kimya_otomotiv_savunma_tuketim — bağımsız doğrulama notları (02.11.2026)

Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_kimya_otomotiv_savunma_tuketim/`
(vk.py yardımcılar; fx_timing_check, a1_sync … a6_extra; çıktılar res/*.csv, res/*.log). ll.py import edilmedi. Her şey ham parquet'ten hesaplandı.

## Yöntem (kendi uygulamam)
- BIST: v=0 günleri atıldı, kendi işlem günleri üzerinden getiri hesaplandı, sonra XU100 takvimine oturtuldu (ffill yok). Fiyat oranı >1,105 veya <0,895 olan günler NaN yapıldı.
- Ayrıştırma: cc=ln(adj), intra=ln(c/o), gap=cc−intra. 2014 öncesi gap/intra yok sayıldı; şüpheli açılışlar NaN.
- Yurt dışı seriler: "yerel tarih ≤ t" kuralıyla ffill, tatil sıfırları NaN, 8σ sıçramalar NaN.
- FX zaman damgası saatlik veriyle doğrulandı (2024-02+). Yahoo günlük c(t), 00:00 UTC t fiyatıyla medyan 2–3 bps farkla örtüşüyor (15:00 ve 21:00 UTC'de 20–35 bps). Düzeltme olarak satır kaydırma uygulandı; bu düzeltme DOĞRU.
- pc: sabit + kontroller üzerinden artıkların korelasyonu, NW(5) t ile.
  - Ortak faktör seti (CF): XU100 + USDTRY + EEM_t + EEM_{t-1} (+ Avrupa emsallerinde ^STOXX).
  - Dönemler: tam = 2010+, IS 2014–20, OOS 2021–26, 1y = son 250 ortak gün.
  - Ek testler: yıllık işaret, haftalık pc, 250 günlük kayan pc, 15:00 UTC hizalı h1 (2023-12+).
- Sektör endeksleri: Yahoo'da günlük geçmiş YOK (XTAST, XKMYA, XGIDA, XILTM, XINSA, XHOLD, XMANA tek satır). Bu yüzden yalnız XUSIN kullanıldı; çimentoda ayrıca "çift hariç küme sepeti" denendi.
- FDR: 75 senkron testin 34'ü q<0,05 ile geçti, 20 plasebonun 0'ı geçti.

## Sonuç tablosu
| İddia | Bağımsız rakam | Karar | Yeni güven |
|---|---|---|---|
| K-a çimento | pc 0,22–0,40, 16–17/17 yıl, IS 0,18–0,44, OOS 0,25–0,44 (hepsi t>4), CF ile aynı. Son 1y: OYAKC–AKCNS 0,06, CIMSA–AFYON/KONYA 0,11–0,13. Çift hariç sepet kontrolünde CIMSA–OYAKC 0,34→0,17, CIMSA–AKCNS 0,41→0,31. Küçük→büyük bayat-fiyat öncülüğü yok. | KABUL | YÜKSEK |
| K-b GUBRF–BAGFS | 0,33 yalnız 2005+ başlangıçta çıkıyor (2005–09 dönemi 0,55). 2010+ 0,24, IS 0,23, OOS 0,20. 2025'te 0,10, 2026'da 0,03, son 250g 0,02. | DÜZELT | ORTA |
| K-c TKFEN–ENKAI | 2010+ 0,138 (2005+ 0,175), IS 0,10, OOS 0,15, 15/17 yıl, son 250g 0,02 | DÜZELT | ORTA |
| K-d SISE–XBANK | −0,165 (t −9,0), 16/17 yıl, son 250g +0,165. İşaret dönüşü SISE'ye özgü değil: EREGL, FROTO, TCELL, CIMSA, KCHOL da pozitife döndü; ASELS, TUPRS ve BIMAS ise daha negatif. | KABUL | ORTA |
| K-e küresel emsaller | Tümünde \|pc\|≤0,04, haftalıkta ≤0,09. İstisna: CIMSA–HEI 15UTC pc 0,09 (t 2,6), SISE–SGO +STOXX 0,11 (t 2,5); son 1y'de artış var. | KABUL | ÇOK DÜŞÜK (HEI/SGO DÜŞÜK) |
| O1 ASTOR–EUPWR/GESAN | 0,370 / 0,311. Yarı örneklemler 0,45→0,29 ve 0,41→0,20 (z 2,8 / 3,6). 2025'te 0,16 / 0,10. Örneklem kısa (2023+). | DÜZELT | ORTA |
| O2 TOASO–AB oto | pc\|XU100 0,066–0,097 tutuyor. CF+STOXX ile 0,02–0,04, 15UTC+STOXX ile 0,015–0,05 (t<1,6) → büyük kısmı Avrupa piyasa betası | DÜZELT | DÜŞÜK |
| O3 Kore şebeke→ASTOR gap | Ham gap t 3,8–4,6 ve gün-içinde etki yok, ikisi de tekrarlandı. Ancak KOSPI kontrolünde pc 0,01–0,06; XU100 gap + KOSPI + SPX_{t-1} kontrolünde ≈0. Plasebo: 50 hisse içinde ASTOR 23. sırada. Genel gece/Asya faktörü, şebekeye özgü değil. | DÜZELT | ÇOK DÜŞÜK |
| O4 FX düzeltmesi | Düzeltme doğru. USDTRY_{t-1}(UTC t-1)→ihracatçı intra: OOS t −0,2, pc\|XU100intra t 0,8. Düzeltme öncesi "lag1" look-ahead değildi, UTC t-2 bilgisiydi; bu bilgi hâlâ küçük (pc 0,06, t 3,6) ama net değil. t 4,7 tekrarlanamadı (sepet 2,4, FROTO 3,3). "OOS −17 bps" bulgusu TL'nin %69 gün değer kaybettiği dönemde fiilen sürekli-long gün-içi drift ölçüyor. | DÜZELT | ÇOK DÜŞÜK |
| S1 TCELL–TKC | corr 0,750, pc 0,622, CF 0,72, 17/17 yıl | KABUL | YÜKSEK |
| S3 ASELS–AB savunma | 2014–21 0,017 → 2022–26 0,113 (+STOXX 0,056→0,129, z 1,98). 2022–26 yılların 5/5'i pozitif. 15UTC tekil isimler 0,11–0,16. Üst %5 \|EU_DEF\| günleri çıkarılınca 0,048 (t 1,6). | KABUL | ORTA |
| S4 rearm günleri | AR0 +358 bps (t 3,3), 6/6 pozitif. Bölümler birleştirilince n=4, ort +537 bps. Rastgele plasebo p=0,0003. Etki gap'te değil gün-içinde: gap +2 bps, intra +420 bps. Olaylar sonradan seçildi, n küçük. | DÜZELT | DÜŞÜK |
| T1 AEFES–CCOLA | pc 0,222, IS 0,200, OOS 0,267, 16/17 yıl, CF 0,225 (kısmen sahiplik mekaniği) | KABUL | YÜKSEK |
| T2 AEFES–bira | 2010+ pc 0,03–0,09, 2014+ XU100+STOXX+SPX ile 0,06–0,09. Haftalık OOS 0,20–0,25 (t 2,5–4,1). Plasebo ≈0. | KABUL | ORTA |
| T3 kakao→ULKER | senkron pc 0,013. CC_{t-1}→intra −0,02, aylık lag0–6 anlamsız. BT negatif. | KABUL (olumsuz) | ÇOK DÜŞÜK |

## Eleştiri ve sınırlamalar
- XU100, hisseleri içerdiği için pc'de mekanik etki var. XBANK rotasyonu kısmen bu XU100 artıklandırma mekaniğinden geliyor.
- Sektör endekslerinin günlük geçmişi olmadığından "sektör kontrollü" test eksik kaldı.
- 2023+ hisselerde (ASTOR, EUPWR) IS 2014–20 tanımsız; yerine yarı örneklem kullanıldı.
- S4'teki olay tarihleri savunma ajanının listesinden alındı (veri olarak). Seçim yanlılığı düzeltilemez.
