# ALARK — Alarko Holding A.Ş.

Spot: `BIST:ALARK` · VİOP pay vadelisi: `BIST:ALARK1!` · Sektör: Holding (enerji: Cenal kömür santrali gelirin ~%72'si, FAVÖK'ün ~%97'si; taahhüt; Alarko Carrier %42→%84; Alarko GYO)

## Özet
ALARK'ın dış sürücüleri çok zayıf: küresel blok varyans payı %1,3 (özgün ≈0), hisseye özgü pay %65; doğrulama turu XU100 ve USDTRY dışında sağlam küresel sürücüsü olmadığını teyit etti. Kömür santraline rağmen kömür (MTF/ATW), TTF, Brent ve Avrupa müteahhitleriyle XU100 kontrollü ilişki yok (pc ≈0); olası nedenler PTF tavanı/regülasyon, kömür–elektrik doğal hedge'i ve bayat MTF verisi. XU100 ötesindeki sağlam bağlar yurt içi ve senkron: grup şirketleri ALGYO (pc 0,21) ve ALCAR (0,15) ile orta ölçek faktörü (hisse-hariç XYUZO +0,23, XU030 −0,26; yılların %100'ü). TL değer kaybettiğinde ALARK piyasadan kötü (VİOP USDTRY/EURTRY pc −0,10…−0,11, ORTA). Uluslararası sürücüler (ES, TUR, Nikkei) yalnız açılış gap'inde; kendi açılış gap'inin geri dönüşü yalnız OOS'ta anlamlı (41 bps, t 2,5) ve işlem açısından DÜŞÜK.

**Varyans ayrıştırması:** Tam dönem: R² %35; hisseye özgü %65; BIST piyasası %18; holding kümesi %15 (2024–26 %18); küresel blok %1,3 (son 1y %4,0; özgün %0,1); TR makro %0,7. XU100 corr 0,59 (IS 0,58 / OOS 0,59), beta 0,88 (3y 0,95).

**VİOP likidite/maliyet:** BIST:ALARK1! sınıf B: 12 ay medyan günlük hacim 286 mn TL (6,3 mn USD), medyan 7.173 işlem; tik 0,01 TL (12 ay medyan ≈4,6 bps, son fiyatta 1,1 bps); gidiş-dönüş maliyet küçük emir 8,8 bps, muhafazakâr 11,0 bps, 1 mn TL 21,7 bps, bireysel 25,6 bps; vadeli/spot hacim 0,53. Vadeli 2022-11'den beri işlem görüyor: VİOP'ta IS dönemi yok.

## Sürücüler (güven sırasıyla)

| # | Sürücü | TradingView | Kapsam | İlişki | Rakamlar | Yön | İşlenebilirlik | Güven | Doğrulama |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD vadelileri ES/NQ gece | CME_MINI:ES1! (alt: CME_MINI:NQ1!) | uluslararası | gap öncü | ES gece → gap corr 0,33 (1y 0,43; IS 0,30 / OOS 0,38; gün-içi t −0,1); faktör kontrolünde ES 0,02, NQ 0,02 (OOS t 0,6–0,8) | + | hayır (açılışta fiyatlanıyor; pay vadelisinde akşam seansı yok) | YÜKSEK | doğrulandı (1. tur ana bulgusu KABUL/YÜKSEK; y_ag: yalnız ortak faktör) |
| 2 | Alarko GYO (ALGYO) | BIST:ALGYO | yurt içi | senkron | pc 0,205 (t 10,7); IS 0,26 / OOS 0,14; yılların %100'ü; f_y_hisse 0,194 (IS 0,26 / OOS 0,15); ham corr 1y 0,25 | + | hayır (senkron) | YÜKSEK | doğrulanmadı (iki ajan YÜKSEK) |
| 3 | Alarko Carrier (ALCAR) | BIST:ALCAR | yurt içi | senkron | pc 0,154 (t 8,6); IS 0,15 / OOS 0,14; yılların %100'ü; f_y_hisse 0,154 | + | hayır (senkron) | YÜKSEK | doğrulanmadı (r1 ORTA, ry_grup/ry_hisse YÜKSEK) |
| 4 | Orta ölçek faktörü (XYUZO / XU030, hisse-hariç) | BIST:XYUZO (alt: BIST:XU030 / BIST:XTUMY / BIST:XUTUM) | yurt içi | senkron | Hisse-hariç XYUZO kısmi +0,23 (IS 0,27 / OOS 0,20; %100 yıl); hisse-hariç XU030 −0,26 (IS −0,29 / OOS −0,24; %100). XYUZO ham corr 0,62, XU100 0,59; İki faktörlü ham kısmi (y_endeks YÜKSEK etiketlerinin kaynağı): XUTUM +0,16 (t 6,0; ham corr 0,60; mekanik içerme), XTUMY +0,22 (t 8,5; hisseyi içermez), XYUZO +0,26 (t 11,1); XYLDZ (Yıldız Pazar) +0,11 (t 4,7; DÜŞÜK), XUMAL −0,03 ve hisse-hariç XSD25 −0,07 (DÜŞÜK) | + orta ölçek / − büyük ölçek | hayır (senkron) | YÜKSEK | doğrulanmadı (y_endeks) |
| 5 | VİOP 09:30 açılışı → spot açılış gap'i | BIST:ALARK1! | yurt içi | mikroyapı | corr 0,67 (b 0,92; R² 0,45); spot gün-içi kalıntı yok | + | hayır | YÜKSEK | doğrulanmadı |
| 6 | TUR + TKC + EMB / TUR−EEM gece | NASDAQ:TUR (alt: NYSE:TKC / NASDAQ:EMB / NASDAQ:TUR/AMEX:EEM) | uluslararası | gap öncü | TUR gece → gap corr 0,21 (1y 0,31; IS 0,13 / OOS 0,32); Yahoo TUR_t−1 → gap t 6,5 (IS 5,9 / OOS 4,0; FDR); EMB_t−1 → gap t 3,3 (IS 2,6 / OOS 2,4); TUR−EEM t 3,0 (IS 2,9 / OOS 1,35). Senkron pc TUR 0,05; TKC (Turkcell ADR) gece → gap corr 0,16 (t 3,2; IS 0,15 / OOS 0,18; gün-içi −0,06; ORTA) | + | hayır (gap) | ORTA | doğrulandı (B1 genel KABUL; TV kodu NASDAQ:TUR) |
| 7 | Asya kapanışları: Nikkei, KOSPI | TVC:NI225 (alt: KRX:KOSPI) | uluslararası | gap öncü | Nikkei → gap corr 0,32 (t 4,2; IS 0,34 / OOS 0,29); tam faktör kontrolünde kısmi 0,21 (t 6,9); KOSPI 0,21 (t 7,6); Nikkei → gün-içi: ham −0,13 (ayrı satır), XU100 ve kendi gecikmesi kontrolünde −0,03 (t −0,5) | + | hayır | ORTA | doğrulanmadı (y_ag: A1 ayakta) |
| 8 | TL kuru (VİOP USDTRY/EURTRY, gram altın TL; negatif) | BIST:USDTRY1! (alt: BIST:EURTRY1! / FX:USDTRY / FX:EURTRY / BIST:XAUTRY1!) | yurt içi | senkron | VİOP (15:00 hizalı) pc: USDTRY −0,096 (IS −0,07 / OOS −0,11; %90 yıl; 1y −0,13), EURTRY −0,109 (IS −0,08 / OOS −0,12; %80), sepet −0,106, gram altın −0,091 (TRY bileşeni); FDR. Yahoo EURTRY −0,056 (r1; IS −0,06 / OOS −0,05), USDTRY 15:00 saatlik −0,058 (yıl %100). Rejim: yüksek kur-vol −0,08, carry 2023–25 +0,14. Haftalık kur geçişkenliği b −0,23 (t −2,4). Yahoo kur_t−1 → gap t −4,2 (IS −5,6 / OOS −0,7: eşzamansız, kayboldu); Yahoo sepet kur pc −0,047 (t −2,6; IS −0,04 / OOS −0,05; DÜŞÜK), Yahoo gram altın −0,051 (IS −0,04 / OOS −0,06; DÜŞÜK); Yahoo sepet kur_t−1 → gap t −3,6 (IS −5,5 / OOS 0,05; ajan 'ORTA (işlenemez)') | − (TL değer kaybında ALARK piyasadan kötü) | hayır (senkron) | ORTA | doğrulanmadı (ALARK'a özgü kur testi doğrulama turunda yok) |
| 9 | Kendi açılış gap'i (/gap/>%1) → gün-içi dönüş | BIST:ALARK | yurt içi | mikroyapı | IS 2014–20 +11,8 bps (t 0,9) / OOS 2021–26 +41,5 bps (t 2,5); %77 yıl +; FDR hayır; h1 2023-12+: açılış girişi 67,1, ilk 30 dk VWAP vekili 43,2 (t 2,3), 07:30 UTC girişi 28,4 bps. Gap kalıntısı → ilk 30 dk corr −0,19 (t −2,65), 07:30 sonrası −0,04. İstatistik ORTA (yalnız OOS) / işlem DÜŞÜK | − (gap tersine) | sınırda: gecikmeli girişte de pozitif (h1, kısa örneklem) ama IS yok ve vadeli B sınıfı (1 mn TL emirde ~22 bps) | ORTA | düzeltildi (Kendi gap fade genel: ilişki ORTA, işlem DÜŞÜK–ORTA; IS rakamları v3'te şişikti) |
| 10 | TUR_t−1 → ALARK gün-içi (USD-gelirli faktör) | NASDAQ:TUR | uluslararası | gün-içi öncü | 47 hisse taramasında TUR_t−1 → gün-içi t −3,2 (ENKAI −5,1, THYAO −4,4, SISE −3,7, FROTO/TKFEN −3,6); ihracatçı sepeti t −3,9: ortak USD-gelirli faktör. 2020–23 rejimine bağlı; İstatistik DÜŞÜK (ortak USD-gelirli faktör, rejime bağlı) / işlem ÇOK DÜŞÜK | − | hayır | DÜŞÜK | düzeltildi (v_H45_b: ortak faktör; 2014–19 ve 2024–25'te ≈0) |
| 11 | Brent gece | ICEEUR:BRN1! (alt: TVC:UKOIL) | uluslararası | gap öncü | Brent gece → gap corr −0,23 (1y −0,42; IS −0,07 / OOS −0,38) | − (2025+) | hayır | DÜŞÜK | düzeltildi (B5: 2026 petrol şoku tek ortak faktör) |
| 12 | Bitcoin gece | BITSTAMP:BTCUSD (alt: COINBASE:BTCUSD) | uluslararası | gap öncü | BTC gece → gap corr 0,18 (IS 0,17 / OOS 0,19; gün-içi t 1,1) | + | hayır | DÜŞÜK | doğrulanmadı |
| 13 | Lotte Chemical (011170.KS)_t−1 | KRX:011170 | uluslararası | gün-içi öncü | t 3,9 (IS 2,4 / OOS 3,1); kova içi BH geçer, tüm aile BH'de 0; /r/≈0,07; İstatistik DÜŞÜK / işlem ÇOK DÜŞÜK | + | hayır | DÜŞÜK | doğrulanmadı |
| 14 | Tarama sürprizleri: AUD/USD, demir cevheri (negatif pc) | FX:AUDUSD (alt: COMEX:TIO1!) | uluslararası | senkron | AUDUSD pc −0,049 (IS −0,09 / OOS −0,04; %77 yıl), TIO=F −0,058 (IS −0,05 / OOS −0,07; %92); CPNG −0,069, IHS −0,068, 2YY=F +0,056 (ÇOK DÜŞÜK); BH q 0,08–0,45 | − | hayır | DÜŞÜK | doğrulandı (olumsuz: TR3 – max /pc/ ≤0,10, replikasyon yok) |
| 15 | TL faizi: DİBS 5y/10y (negatif) | TVC:TR10Y (alt: TVC:TR05Y / TVC:TR02Y) | yurt içi | senkron | pc 10y −0,058 (IS −0,06 / OOS −0,06; %85 yıl; 1y −0,10; FDR), 5y −0,053 (%77); DİBS 2y_t−1 → gap t 2,7 (IS 2,3 / OOS 2,0; işlenemez) | − | hayır | DÜŞÜK | doğrulanmadı |
| 16 | Alarko–Carrier pay devri (olay, 07–10.08.2026) | BIST:ALARK (alt: BIST:ALCAR) | yurt içi | olay | İlk iş günü AR0 +%4,8 (t 3,1), CAR[0,1] +%3,4, CAR[2,10] −%5,2 (t −1,1), CAR[0,20] +%10,3 (XU100 piyasa modeli). NAV iskontosu 2026 YTD +49 (log, yaklaşık) | + | hayır (tek olay) | DÜŞÜK | doğrulanmadı (tek olay; genelleme yok) |
| 17 | Holding akranlarının açılış gap'i → ALARK gün-içi | BIST:KCHOL (alt: BIST:SAHOL) | yurt içi | mikroyapı | Akran (KCHOL, SAHOL, DOHOL, TKFEN, ENKAI) gap → ALARK gün-içi b 0,17 (t 2,0; 2021+ 0,08 t 0,4); h1 O→07:30 b 0,11 (t 1,0); kendi gap b −0,19 (t −3,3) | + | hayır | DÜŞÜK | doğrulanmadı |
| 18 | VİOP baz anomalisi → ertesi spot gap | BIST:ALARK1! | yurt içi | mikroyapı | 13,6 bps/σ (t 3,0; IS yok / OOS 3,0; FDR geçti); → vadeli gün-içi +17,7 bps/σ (t 1,5) | + | hayır (spot gap; kısa örneklem) | DÜŞÜK | doğrulanmadı |
| 19 | Kapanış müzayedesi hareketi (CA) → ertesi gün | BIST:ALARK | yurt içi | mikroyapı | gap_t+1 b −0,17 (t −0,9; IS −0,21 / OOS −0,22); O→07:30 b −0,14 | − | hayır (VİOP'ta uygulanamaz) | DÜŞÜK | düzeltildi (YG2: ilişki ORTA, VİOP net kâr DÜŞÜK) |
| 20 | XFINK (finansal kiralama) endeksi_t−1 | BIST:XFINK | yurt içi | gün-içi öncü | XFINK_t−1 → ALARK cc t −3,3, gün-içi t −3,2 (IS −2,5 / OOS −1,85); BH q 0,23–0,40; İstatistik DÜŞÜK / işlem ÇOK DÜŞÜK | − | hayır | DÜŞÜK | doğrulanmadı |
| 21 | XHOLD (Holding endeksi, hisse-hariç) | BIST:XHOLD | yurt içi | senkron | Ham kısmi 0,10; hisse-hariç 0,07 (IS 0,05 / OOS 0,08; %77 yıl); holding akran Shapley %15, özgün pay %1 | + | hayır | DÜŞÜK | doğrulanmadı |
| 22 | Yabancı akış (TCMB haftalık) | ? (TCMB EVDS; TV kodu yok) (alt: BIST:XU030) | yurt içi | senkron | corr −0,09 (t −2,5; FDR geçti); yayın sonrası 5 gün IS 0,03 / OOS 0,01 | − (yabancı alımında ALARK göreli zayıf) | hayır | DÜŞÜK | doğrulanmadı |
| 23 | ALARK_t−1 → EMB / TUR−EEM (ters yön) | NASDAQ:EMB (alt: NASDAQ:TUR/AMEX:EEM) | yurt içi | ters yön | ALARK_t−1 → EMB_t t −2,6 (IS −1,6 / OOS −2,1); → TUR−EEM t 2,5 (OOS 2,55); 1.071 ters testte 0 FDR | karışık | hayır | DÜŞÜK | doğrulanmadı |
| 24 | Nikkei → ALARK gün-içi (açılış aşırı tepkisinin dönüşü) | TVC:NI225 | uluslararası | gün-içi öncü | r1_gunici: Nikkei (06:30 UTC kapanış) → ALARK gün-içi corr −0,133 (t −3,8; IS −0,16 / OOS −0,10; BT brüt OOS −12,3 bps; ajan ORTA); y_ag claim_check (XU100 ve kendi gecikmesi kontrollü) −0,03 (t −0,5; q 0,80). İstatistik ÇOK DÜŞÜK (kontrolde kayboluyor) / işlem ÇOK DÜŞÜK | − (gap +, gün-içi −) | hayır: kontrol sonrası etki yok, backtest negatif | ÇOK DÜŞÜK | düzeltildi (y_ag claim_check: ORTA → ÇOK DÜŞÜK; piyasa geneli gap dönüşü) |
| 25 | Türkiye elektrik fiyatı (PTF) / kömür–elektrik spread'i | ? (EPİAŞ PTF; TV kodu yok) | yurt içi | hipotez | ALARK için test edilmedi; benzer test AKSEN'de aylık PTF pc 0,26 (IS 0,28 / OOS 0,24; E5 KABUL/ORTA), günlük ilişki yok. Kömür vadelisi (ATW) ile ilişki yok (olumsuzlar) | + (beklenen) | hayır | ÇOK DÜŞÜK | doğrulanmadı (test edilemedi) |

## Test edilip ilişki bulunmayanlar (olumsuzlar)
- Kömür (MTF=F, TV ICEEUR:ATW1!) pc 0,011 (IS −0,01 / OOS 0,03; MTF serisinin %19'u sıfır getiri, 2025-12'den beri bayat); MTF_t−1 → ALARK gün-içi backtest OOS −11,2 bps (15 bps −18,2).
- TTF doğalgaz pc −0,006; Brent senkron ≈0 (r1_holding).
- Avrupa müteahhitleri ACS, FER, HOT, SKA, VIE, STR pc ≈0 (ACS −0,001).
- Doğrulama (TR3, YÜKSEK): XU100 ve USDTRY dışında sağlam küresel sürücü yok (max |pc| ≤0,10).
- Hakem: ALARK yabancı emsal sepeti (BTU, ARCH, WHC, YAL, ACS, FER, HOT, SKA, VIE, STR, BBY, PAVE, TUI1) → hedge'li gün-içi −5,5 bps/σ (t −1,6; IS −2,35 / OOS −0,06); VİOP −2,8 (t −0,4).
- İştirak ALCAR açılış ayrışması → ALARK gün-içi: açılış girişli OOS kazancın neredeyse tamamı ALARK'ın kendi gap'inin dönüşü; hakem iştirak artığı (ALCAR)_t−1 → ALARK gün-içi t 0,68 (OOS −0,19).
- ENJSA_t−1 → ALARK gün-içi t −0,07 (f_y_hisse).
- TLREF pc 0,048 (ÇOK DÜŞÜK); zımni TL faizi −0,00…−0,02; DİBS 1y/2y senkron −0,01/−0,04.
- Gece sürücü sepeti → 07:30 sonrası gün-içi devam: IS −33,0 / OOS −0,9 bps.
- İlk yarım saat → son 30 dk momentumu: b −0,03 (OOS −0,07, t −2,2); 47 hissede 0 FDR.
- 5 dk ve saatlik hisse/endeks öncülüğü: 741+741 testte 0 FDR; ES/NQ/Brent/USDTRY 5 dk'da gecikme yok.
- Günlük endeks_t−1 → ALARK gün-içi: 12.726 testte 0 FDR (XFINK dışında |t|<3).
- 5 dk AKBNK → ALARK b −0,02 (t −0,8; DÜŞÜK); diğer 5 dk/60 dk hisse öncülükleri 0 FDR.
- Avrupa/Asya gece ve sabah sürücüleri: DAX ve STOXX600 gece → gap corr 0,04 (t ≤1,0), altın gece → gap 0,09 (t 1,5; IS −0,06 / OOS 0,21), Hang Seng (gün, açılış öncesi, 07:30→kapanış) → ALARK gün-içi |t| ≤1,1, USD/CNH 07:00–08:30 −0,04 (t −0,8) (hepsi ÇOK DÜŞÜK).
- Hisse-hariç endeks h1 (İş Yatırım 2017–26: XU030, XBANK, XLBNK, XUSIN, XHOLD) → ALARK Σβ |t| ≤1,9; m5 (60 gün) XBANK t 2,4, XLBNK 2,3, XU030 2,3, XUSIN 1,8 (ÇOK DÜŞÜK; bayat fiyat/tik etkisi).

## Çin/HK kodları yerine test edilmiş alternatifler
- Bu kartta doğrudan Çin borsası sürücüsü yok. Asya gap bilgisi için Şanghay yerine CBOE:CNYA / AMEX:ASHR (haftalık r 0,84–0,86) kullanılabilir.

## Açık sorular
- Alarko Carrier payı %84'e çıktıktan sonra (4Ç26) ALCAR–ALARK pc ve NAV iskontosu dinamiği nasıl değişecek? 2027'de yeniden test edilmeli.
- Cenal kömür santrali marjı (PTF − ithal kömür) ALARK fiyatına aylık ufukta yansıyor mu? EPİAŞ PTF verisiyle test edilmedi.
- TL kuru ile negatif bağın kaynağı (döviz borcu mu, iç talep mi) bilanço döviz pozisyonuyla teyit edilmeli.

## TradingView izleme listesi

```
BIST:ALARK,BIST:ALARK1!,BIST:ALGYO,BIST:ALCAR,BIST:XU100,BIST:XU030,BIST:XYUZO,BIST:XHOLD,BIST:KCHOL,BIST:SAHOL,CME_MINI:ES1!,NASDAQ:TUR,NASDAQ:EMB,TVC:NI225,KRX:KOSPI,BIST:USDTRY1!,BIST:EURTRY1!,FX:USDTRY,FX:EURTRY,BIST:XAUTRY1!,TVC:TR10Y,ICEEUR:BRN1!,ICEEUR:ATW1!,ICEENDEX:TFM1!,NYSE:TKC,BIST:XTUMY
```
