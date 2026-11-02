# EKGYO — Emlak Konut Gayrimenkul Yatırım Ortaklığı A.Ş.

Spot: `BIST:EKGYO` · VİOP pay vadelisi: `BIST:EKGYO1!` · Sektör: GYO (konut geliştirme; düşük fiyatlı, bireysel ağırlıklı, yüksek betalı)

## Özet
EKGYO yüksek betalı bir piyasa hissesi (beta 1,07; son 3 yıl 1,24) ve getirisinin %29'u BIST piyasası, %16'sı GYO kümesi; küresel blok yalnız %1,7 ve özgün katkısı ≈0. Doğrulama turu XU100 ve USDTRY dışında sağlam küresel sürücüsü olmadığını teyit etti; ABD konut/GYO emsalleri (XHB, ITB, VNQ, Vonovia) ile senkron ilişki yok, yalnız eşzamansız gap var. XU100 ötesindeki sağlam bağlar yurt içi GYO kümesi: hisse-hariç XGMYO kısmi 0,18 (OOS 0,21) ve ISGYO (0,15). TL faizi en anlamlı makro kanal: 2 yıllık DİBS getirisi arttığında EKGYO piyasaya göre düşüyor (OOS pc −0,11, son 1y −0,25, ORTA) ve dünkü faiz şoku bugünkü gün-içine negatif (t −3,5) — ama bu sinyalin backtesti yalnız OOS'ta pozitif (DÜŞÜK). Saatlik endeks öncülüğü (t 3–4) doğrulamada büyük ölçüde fiyat adımı/bayat fiyat etkisi sayıldı: işlem DÜŞÜK.

**Varyans ayrıştırması:** Tam dönem: R² %47; hisseye özgü %53; BIST piyasası %29 (son 1y %38); GYO kümesi %16; küresel blok %1,7 (son 1y %6,1; özgün ≈0); TR makro %0,5. XU100 corr 0,68 (IS 0,70 / OOS 0,68; 1y 0,74), beta 1,07 (3y 1,24, 1y 1,29). Diebold–Yilmaz net yayıcı 0,15.

**VİOP likidite/maliyet:** BIST:EKGYO1! sınıf A: 12 ay medyan günlük hacim 1.201 mn TL (25,9 mn USD), medyan 18.699 işlem; tik 0,01 TL ≈4,9 bps (son fiyatta 6,2 bps; düşük fiyat nedeniyle göreli tik yüksek); gidiş-dönüş maliyet küçük emir 9,1 bps, muhafazakâr 11,5 bps, 1 mn TL 16,9 bps, bireysel 25,9 bps; vadeli/spot hacim 0,47; vadeli 2017-03'ten beri.

## Sürücüler (güven sırasıyla)

| # | Sürücü | TradingView | Kapsam | İlişki | Rakamlar | Yön | İşlenebilirlik | Güven | Doğrulama |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD vadelileri ES/NQ + EEM gece (+VIX_t−1) | CME_MINI:ES1! (alt: CME_MINI:NQ1! / CBOE:VIX / AMEX:EEM) | uluslararası | gap öncü | ES gece → gap corr 0,43 (1y 0,47; IS 0,47 / OOS 0,42; gün-içi t 0,2); VIX_t−1 → cc kısmi −0,068 (t −4,2; IS −2,3 / OOS −3,6; gap −0,13, gün-içi −0,01); faktör kontrolünde ES 0,04, NQ 0,02; EEM gece → gap corr 0,18 (t 4,3; IS 0,15 / OOS 0,21; ajan ORTA) | + (VIX −) | hayır (açılışta fiyatlanıyor; pay vadelisinde akşam seansı yok) | YÜKSEK | doğrulandı (1. tur ana bulgusu KABUL/YÜKSEK; y_ag: yalnız ortak faktör) |
| 2 | TUR + EMB / TUR−EEM gece | NASDAQ:TUR (alt: NASDAQ:EMB / NASDAQ:TUR/AMEX:EEM / NYSE:TKC) | uluslararası | gap öncü | TUR gece → gap corr 0,30 (1y 0,36; IS 0,23 / OOS 0,37); faktör kontrolünde ayakta (kısmi 0,13, t 3,2); Yahoo TUR_t−1 → gap t 7,0 (IS 6,4 / OOS 3,95; FDR); EMB_t−1 → gap t 3,7 (IS 3,7 / OOS 2,0); TUR−EEM t 3,0 (IS 3,7 / OOS 0,8); TUR_t−1 → gün-içi t −2,0 (FDR yok). Senkron pc TUR ≈0, EMB −0,047; TKC gece → gap corr 0,11 (t 2,2; IS 0,10 / OOS 0,14; DÜŞÜK) | + | hayır (gap) | YÜKSEK | doğrulandı (B1 genel KABUL; y_ag A3 ayakta; TV kodu NASDAQ:TUR) |
| 3 | GYO endeksi XGMYO (hisse-hariç) | BIST:XGMYO | yurt içi | senkron | Hisse-hariç kısmi 0,18 (IS 0,14 / OOS 0,21; %77 yıl); ham kısmi 0,63 (t 24; EKGYO ağırlığı ≈%11); ham corr 0,82 (IS 0,90 / OOS 0,77). GYO akran sepeti Shapley %16, özgün %1,7 | + | hayır (senkron) | YÜKSEK | doğrulanmadı (y_endeks; İş Yatırım endeks verisi) |
| 4 | ISGYO (GYO akranı) | BIST:ISGYO | yurt içi | senkron | pc 0,152; IS 0,26 / OOS 0,11; yıllık artık korelasyonun %92'si pozitif; ham corr 0,45 | + | hayır (senkron) | YÜKSEK | doğrulanmadı |
| 5 | VİOP 09:30 açılışı → spot açılış gap'i | BIST:EKGYO1! | yurt içi | mikroyapı | corr 0,56 (b 0,68; R² 0,31); spot gün-içi kalıntı yok | + | hayır | YÜKSEK | doğrulanmadı |
| 6 | Asya kapanışları: Nikkei, KOSPI | TVC:NI225 (alt: KRX:KOSPI / TVC:HSI) | uluslararası | gap öncü | Nikkei → gap corr 0,40 (t 5,8; IS 0,44 / OOS 0,35); tam faktör kontrolünde kısmi 0,24 (t 9,3); KOSPI 0,22 (t 8,1); Hang Seng 07:30→kapanış (BIST açılışından sonra, eşzamanlı) → EKGYO kalan gün-içi corr 0,09 (t 2,9; IS 0,12 / OOS 0,04; ES kontrollü 0,04; DÜŞÜK; HK lag0 → gün-içi iddiaları look-ahead nedeniyle RED, bu yalnız eşzamanlı örtüşme) | + | hayır | ORTA | doğrulanmadı (y_ag: A1 ayakta) |
| 7 | TL faizi: DİBS 2y / 1y (senkron) | TVC:TR02Y (alt: TVC:TR01Y / TVC:TR05Y) | yurt içi | senkron | pc DİBS 2y −0,080 (t −3,4; IS −0,00 / OOS −0,11; %69 yıl; 3y −0,10, 1y −0,25; FDR); 1y −0,073 (IS −0,00 / OOS −0,10; %77); 5y/10y −0,068 (1y −0,23). Ham corr 2y −0,21 (1y −0,46) | − (faiz ↑ → EKGYO piyasaya göre ↓) | hayır (senkron) | ORTA | doğrulanmadı (ry_makro_y: GYO ham −0,25, kısmi −0,07 → büyük kısmı piyasa faktörü) |
| 8 | Büyük hisse sepetine ters (XU030 hisse-hariç) | BIST:XU030 (alt: BIST:XTUMY / BIST:XUTUM) | yurt içi | senkron | Hisse-hariç XU030 kısmi −0,18 (IS −0,35 / OOS −0,10; %92 yıl); hisse-hariç XYUZO +0,07 (IS 0,13 / OOS 0,02); İki faktörlü ham kısmi (y_endeks YÜKSEK etiketlerinin kaynağı): XU030 −0,07 (t −2,9), XUTUM +0,09 (t 3,2), XTUMY +0,12 (t 4,9; hisseyi içermez), XYUZO +0,07 (t 3,4); XUMAL ham 0,14 (t 5,6; mekanik; DÜŞÜK), XYLDZ ≈0 (DÜŞÜK) | − | hayır | ORTA | doğrulanmadı (mekanizma net değil → kartta ORTA) |
| 9 | USDTRY gece ve eşzamansız kur (gap) | FX:USDTRY (alt: BIST:USDTRY1!) | yurt içi | gap öncü | USDTRY gece (15:00→07:00 UTC) → gap corr −0,16 (t −3,8; IS −0,18 / OOS −0,16); saatlik gece serisi t −3,3 (2. yarı −3,3); Yahoo USDTRY_t−1 → gap t −3,5 (IS −4,7 / OOS 0,3). Senkron: 15:00 hizalı (2024+) pc +0,088, Yahoo/VİOP ≈0; haftalık XU100'e göreli geçişkenlik −0,12 (t −2,3); Sepet kur_t−1 → gap t −2,8 (IS −4,4 / OOS 1,1; DÜŞÜK) | − (gap) | hayır (gap) | ORTA | doğrulanmadı |
| 10 | VİOP baz anomalisi → ertesi spot gap / vadeli gün-içi | BIST:EKGYO1! (alt: BIST:EKGYO) | yurt içi | mikroyapı | Baz anomalisi_t → spot gap_t+1 8,2 bps/σ (t 2,8; IS 2,1 / OOS 1,9; FDR geçti); → vadeli gün-içi_t+1 −15,3 bps/σ (t −2,3; IS −1,4 / OOS −2,1; FDR yok) | + (gap) / − (vadeli gün-içi) | hayır/sınırda: spot gap işlenemez; vadeli gün-içi bacağı FDR'den geçmiyor ve açılış derinliği sığ | ORTA | doğrulanmadı |
| 11 | PSGYO / RYGYO (GYO akranları) | BIST:PSGYO (alt: BIST:RYGYO) | yurt içi | senkron | PSGYO pc 0,161 (yalnız OOS; kısa örneklem; %100 yıl); RYGYO 0,065 (t 3,7; IS 0,04 / OOS 0,06; %81 yıl); RYGYO göreli öncülük t 3,9 (IS 3,0 / OOS 2,6; BH yok, seçilim gürültüsü) | + | hayır | ORTA | doğrulanmadı |
| 12 | Rafineri ETF (CRAK) / petrol hisseleri (negatif) | AMEX:CRAK (alt: NYSE:CVX / ICEEUR:BRN1!) | uluslararası | senkron | CRAK pc −0,058 (t −3,2; IS −0,07 / OOS −0,05; %67 yıl; tarama FDR); CVX −0,060 (IS −0,05 / OOS −0,07; %85, ÇOK DÜŞÜK); Brent gece → gap corr −0,365 (1y −0,59; IS −0,06 / OOS −0,53) | − | hayır | DÜŞÜK | düzeltildi kısmen (B5: 2026 petrol şoku tek ortak faktör) |
| 13 | ABD konut ETF'i XHB_t−1 → gap | AMEX:XHB | uluslararası | gap öncü | XHB_t−1 → gap t 5,6 (gün-içi ≈0; IS −0,34 / OOS 0,64); senkron pc −0,005 | + | hayır (eşzamansız kapanış) | DÜŞÜK | doğrulanmadı |
| 14 | Bitcoin gece | BITSTAMP:BTCUSD (alt: COINBASE:BTCUSD) | uluslararası | gap öncü | BTC gece → gap corr 0,26 (IS 0,33 / OOS 0,20; gün-içi t 1,5); faktör kontrolünde 0,02 (t 0,9) | + | hayır | DÜŞÜK | düzeltildi (y_ag: B3 gürültü; r1 ORTA → kartta DÜŞÜK) |
| 15 | DİBS faizi_t−1 → EKGYO gün-içi | TVC:TR02Y (alt: TVC:TR05Y) | yurt içi | gün-içi öncü | DİBS 2y_t−1 → gün-içi t −3,5 (IS −3,0 / OOS −2,9; FDR yok; ry_makro özetinde −3,51); 5y −3,1 (OOS −3,0); 10y −2,5; 1y −2,4. BT (DİBS 2y /z/>1 → EKGYO gün-içi, 8 bps): IS −5,6 bps (t −0,6) / OOS +41,8 (t 2,3), brüt OOS 49,8. Mekanizmanın büyük kısmı DİBS serisinin otokorelasyonu (0,24). İstatistik ORTA / işlem DÜŞÜK | − (dün faiz ↑ → bugün gün-içi ↓) | sınırda: yalnız OOS'ta pozitif; IS'te maliyet sonrası negatif | DÜŞÜK | doğrulanmadı (ry_makro_y #7 DÜŞÜK) |
| 16 | Saatlik endeks → EKGYO (XU030, XHOLD, XUSIN) | BIST:XU030 (alt: BIST:XHOLD / BIST:XUSIN) | yurt içi | mikroyapı | h1 (İş Yatırım 2017–26) Σβ_lag1..3: XU030 0,14 (t 3,4; IS 3,0 / OOS 2,1), XHOLD 0,14 (t 3,7; OOS 1,7), XUSIN 0,16 (t 3,9; OOS 1,8); 5 dk'da ≈0 (/t/ ≤1,3). Düşük fiyat → göreli tik ~5–6 bps; İstatistik YÜKSEK/ORTA (ajan: XU030 h1 YÜKSEK, XHOLD ve XUSIN ORTA; bayat fiyat şüphesi) / işlem DÜŞÜK | + | hayır: fiyat adımı/bayat fiyat kaynaklı; maliyeti karşılamaz | DÜŞÜK | doğrudan test edilmedi (v_wf4 genel sorunlar 'PLAUSIBLE': DOHOL/TSKB/EKGYO saatlik öncülüğü büyük ölçüde fiyat ayrıklığı/bayat fiyat; işlem için DÜŞÜK önerildi) |
| 17 | XGMYO_t−1 → EKGYO gap | BIST:XGMYO | yurt içi | gap öncü | Hisse-hariç XGMYO_t−1 → gap t 3,6 (IS 2,95 / OOS 2,1); cc t 2,7; BH q 0,21 | + | hayır (gap) | DÜŞÜK | doğrulanmadı |
| 18 | OYAKC_t−1 → EKGYO gün-içi | BIST:OYAKC | yurt içi | gün-içi öncü | kısmi 0,054; gün-içi t 2,4 (IS 1,3 / OOS 1,9); hacim filtreli 2,8; BH (214 çift) geçmedi; BT OOS 11,4 bps brüt; İstatistik DÜŞÜK / işlem ÇOK DÜŞÜK | + | hayır | DÜŞÜK | doğrulanmadı |
| 19 | EKGYO_t−1 → gram altın (ters yön) | BIST:XAUTRY1! (alt: FX_IDC:XAUTRYG) | yurt içi | ters yön | EKGYO_t−1 → VİOP gram altın t −2,1 (IS −1,5 / OOS −1,7); Yahoo gram altın −2,1; 1.071 ters testte 0 FDR | − | hayır | DÜŞÜK | doğrulanmadı |
| 20 | TÜFE açıklaması (ayın 3'ü, 10:00 TSİ = açılış) | BIST:EKGYO (alt: BIST:XBANK) | yurt içi | olay | TÜFE günlerinde EKGYO'nun mutlak gün-içi hareketi normal günün 1,18 katı (YKBNK 1,20, ISCTR 1,18; XBANK ilk saat mutlak getirisi 182 bps, normalde 84); ilk saatten sonra devam yok. Yön test edilemedi | ? | hayır (yalnız volatilite bilgisi) | DÜŞÜK | doğrulanmadı (r1_olay: volatilite ORTA / yön ÇOK DÜŞÜK; hisse düzeyinde DÜŞÜK) |
| 21 | Tarama sürprizleri: EHang, L3Harris, SPIE (negatif) | NASDAQ:EH (alt: NYSE:LHX / EURONEXT:SPIE) | uluslararası | senkron | EH pc −0,066, LHX −0,061 (%77 yıl), SPIE.PA −0,061 (%92); BH q 0,04–0,18 | − | hayır | ÇOK DÜŞÜK | doğrulandı (olumsuz: TR3 – max /pc/ ≤0,10, replikasyon yok) |
| 22 | Konut satışları, konut kredisi faizi, kamu arsa ihaleleri | ? (TÜİK/TCMB; TV kodu yok) | yurt içi | hipotez | Test edilmedi: aylık konut satışları, konut kredisi faizi ve gelir paylaşımı ihaleleri (olay) veri setinde yok; Yahoo'da TR tahvili yoktu, DİBS ancak 2. turda BAP verisiyle eklendi | + (satış/ihale) / − (faiz) | hayır | ÇOK DÜŞÜK | doğrulanmadı (test edilemedi) |

## Test edilip ilişki bulunmayanlar (olumsuzlar)
- ABD/Avrupa konut ve GYO emsalleri XHB, ITB, VNA.DE, VNQ ile senkron pc ≈0 (XHB −0,005, VNA 0,02); yalnız eşzamansız gap var.
- ABD 10y faizi (^TNX) pc 0,018; ^TNX_t−1 → EKGYO gün-içi BT IS −16,7 bps (t −2,3) / OOS +11,1 (t 0,8): işaret tutarsız.
- Doğrulama (TR3, YÜKSEK): XU100 ve USDTRY dışında sağlam küresel sürücü yok (max |pc| ≤0,10).
- Hakem: EKGYO yabancı emsal sepeti (XHB, ITB, VNA, LEG, VNQ) → hedge'li gün-içi 1,2 bps/σ (t 0,4); VİOP 2,1 (t 0,5); GYO akranları (PSGYO, RYGYO) artığı_t−1 t −0,15.
- Kendi açılış gap'i fade yok: IS −11,8 bps (t −1,2) / OOS +4,2 (t 0,2); h1 ilk 30 dk VWAP vekili −22,5 bps.
- Kapanış müzayedesi CA → ertesi gap b +0,22 (t 0,8; ters işaret); sektör akranlarının gap'i → gün-içi b −0,06 (t −0,6); ilk yarım saat momentumu b 0,02 (t 0,8).
- VİOP USDTRY/EURTRY/gram altın vadeli ve Yahoo kur ile senkron pc −0,04…−0,01; TLREF −0,03; zımni faiz −0,03.
- Yabancı akış (TCMB haftalık) senkron corr 0,03 (t 1,05), öncülük yok.
- Gece sürücü sepeti → 07:30 sonrası gün-içi: IS +28,0 / OOS −10,7 bps; gap kalıntısı → gün-içi t 0,1.
- 5 dk endeks/hisse öncülüğü ve günlük endeks_t−1 → gün-içi: FDR geçen yok.
- DAX ve STOXX600 gece → gap corr 0,05 (t ≤1,5), altın gece → gap 0,10 (t 1,2; IS −0,19 / OOS 0,24), Hang Seng gün / açılış öncesi → gün-içi |t| ≤0,9, USD/CNH 07:00–08:30 0,02 (hepsi ÇOK DÜŞÜK).
- Hisse-hariç XBANK ve XLBNK h1 → EKGYO Σβ |t| ≤0,9; m5 (60 gün) XU030/XUSIN/XHOLD/XBANK/XLBNK |t| ≤1,3; 5 dk / 60 dk KCHOL, SAHOL, AKBNK, GARAN, THYAO, TUPRS, ASELS, BIMAS, EREGL → EKGYO 0 FDR (ÇOK DÜŞÜK).

## Çin/HK kodları yerine test edilmiş alternatifler
- Bu kartta doğrudan Çin borsası sürücüsü yok. Asya gap bilgisi için Şanghay yerine CBOE:CNYA / AMEX:ASHR (haftalık r 0,84–0,86) kullanılabilir.
- Hang Seng: TVC:HSI (HKEX kodu değil) veya ABD alternatifleri AMEX:FXI / NASDAQ:MCHI (haftalık r 0,86–0,87; ABD kapanışı nedeniyle bir gün önde).

## Açık sorular
- DİBS 2y şoku → EKGYO gün-içi sinyalinin OOS kârı (+42 bps, t 2,3) 2026 fon krizi ve faiz oynaklığı dışında da sürüyor mu? Önceden kayıtlı OOS (2027) testi gerekli.
- Aylık konut satışları ve konut kredisi faizi EKGYO getirisini XU100'ün ötesinde açıklıyor mu?
- EKGYO VİOP vadelisinde baz anomalisi → vadeli gün-içi bacağı (t −2,3) gerçek açılış dolumlarıyla işlenebilir mi?

## TradingView izleme listesi

```
BIST:EKGYO,BIST:EKGYO1!,BIST:XGMYO,BIST:ISGYO,BIST:PSGYO,BIST:RYGYO,BIST:XU100,BIST:XU030,TVC:TR02Y,TVC:TR01Y,TVC:TR05Y,CME_MINI:ES1!,CBOE:VIX,NASDAQ:TUR,NASDAQ:EMB,TVC:NI225,KRX:KOSPI,FX:USDTRY,BIST:USDTRY1!,AMEX:CRAK,ICEEUR:BRN1!,AMEX:XHB,AMEX:EEM
```
