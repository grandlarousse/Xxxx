# TKFEN — Tekfen Holding A.Ş.

Spot: `BIST:TKFEN` · VİOP pay vadelisi: `BIST:TKFEN1!` · Sektör: Holding/taahhüt + tarım (2025 gelirinin %62'si taahhüt, %36'sı tarım/Toros gübre); 24.07.2026'dan beri OYAK (ON Investment BV) %42,8

## Özet
TKFEN'in getirisi büyük ölçüde hisseye özgü (tam dönem %71; 2024–26 %85, son 1y %82): OYAK'ın %42,8'lik payı devralması ve Libco/ARY işlemleri 2026'yı idiyosenkratik bir döneme çevirdi (devrin tamamlanmasında CAR(0,10) +%41, z 4,2; tek olay). Gübre emsalleri (CF, NTR, MOS, YAR, OCI), yabancı müteahhitler (FLR, KBR, ACS) ve tahıl/enerji fiyatlarıyla XU100 kontrollü ilişki yok; doğrulama da XU100+USDTRY dışında sağlam küresel sürücü bulmadı. XU100 ötesindeki bağlar yurt içi: taahhüt akranı ENKAI (pc 0,14, ORTA; 2026'da ≈0), ölçek faktörü (hisse-hariç XU030 −0,20, %100 yıl) ve USD-gelirli karakter (VİOP USDTRY pc +0,09, faiz ↑ günlerinde +0,08, siyasi şoklarda XU100'e göre +177 bps). Uluslararası sürücüler yalnız açılış gap'inde; OYAK grubu (HEKTS, OYAKC, EREGL) ile ortak fiyatlanma henüz başlamadı.

**Varyans ayrıştırması:** Tam dönem: R² %29; hisseye özgü %71 (2024–26 %85, son 1y %82); BIST piyasası %20 (2024–26 %9); taahhüt akranı (ENKAI) %7; küresel blok %1,3 (özgün ≈0); TR makro %0,2. XU100 corr 0,52 (IS 0,51 / OOS 0,53; 3y 0,39); yıllık volatilite son 1y %62. Diebold–Yilmaz net alıcı (−0,20; son 1y −0,35); Fon krizinde (Eyl–Eki 2026) TKFEN en çok 'kendine özgüleşen' hisselerden: hisseye özgü pay +11 puan (n 43; DÜŞÜK)

**VİOP likidite/maliyet:** BIST:TKFEN1! sınıf B: 12 ay medyan günlük hacim 474 mn TL (10,6 mn USD), medyan 10.160 işlem; tik 0,05 TL ≈2,1 bps (son fiyatta 2,6 bps); gidiş-dönüş maliyet küçük emir 8,1 bps, muhafazakâr 11,9 bps, 1 mn TL 26,0 bps, bireysel 24,9 bps; vadeli/spot hacim 0,70; vadeli 2018-12'den beri.

## Sürücüler (güven sırasıyla)

| # | Sürücü | TradingView | Kapsam | İlişki | Rakamlar | Yön | İşlenebilirlik | Güven | Doğrulama |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ölçek faktörü (XU030 / XYUZO, hisse-hariç) | BIST:XU030 (alt: BIST:XYUZO / BIST:XTUMY / BIST:XUTUM) | yurt içi | senkron | Hisse-hariç XU030 kısmi −0,20 (IS −0,19 / OOS −0,21; yılların %100'ü); hisse-hariç XYUZO +0,11 (IS 0,05 / OOS 0,15; %69). XU100 corr 0,52 (3y 0,39); İki faktörlü ham kısmi (y_endeks YÜKSEK etiketlerinin kaynağı): XU030 −0,14 (t −6,1), XYUZO +0,14 (t 6,1), XUTUM +0,10 (t 3,8; mekanik içerme), XTUMY +0,11 (t 4,8; hisseyi içermez) | − büyük ölçek / + orta ölçek | hayır (senkron) | YÜKSEK | doğrulanmadı (y_endeks) |
| 2 | VİOP 09:30 açılışı → spot açılış gap'i | BIST:TKFEN1! | yurt içi | mikroyapı | corr 0,59 (b 0,74; R² 0,35); spot gün-içi kalıntı yok | + | hayır | YÜKSEK | doğrulanmadı |
| 3 | ABD vadelileri ES/NQ gece | CME_MINI:ES1! (alt: CME_MINI:NQ1!) | uluslararası | gap öncü | ES gece → gap corr 0,25 (1y 0,26; IS 0,27 / OOS 0,22; gün-içi t −0,6); faktör kontrolünde NQ ≈0 (t 0,3) | + | hayır (açılışta fiyatlanıyor; pay vadelisinde akşam seansı yok) | ORTA | doğrulandı (genel mekanizma: 1. tur ana bulgusu KABUL/YÜKSEK; hisse düzeyinde ajan etiketi ORTA korunuyor; y_ag: yalnız ortak faktör) |
| 4 | TUR + EMB / TUR−EEM gece → gap | NASDAQ:TUR (alt: NASDAQ:EMB / NASDAQ:TUR/AMEX:EEM / NYSE:TKC) | uluslararası | gap öncü | TUR gece → gap corr 0,21 (1y 0,23; IS 0,18 / OOS 0,24; gün-içi t −2,0); Yahoo TUR_t−1 → gap t 5,4 (IS 5,5 / OOS 2,85; FDR); EMB_t−1 → gap t 2,8; TUR−EEM t 3,0 (IS 3,8 / OOS −0,3). Senkron pc TUR −0,057 (IS −0,10 / OOS 0,00); TKC gece → gap corr 0,10 (t 2,45; IS 0,10 / OOS 0,09; DÜŞÜK) | + (gap) | hayır (gap) | ORTA | doğrulandı (B1 genel KABUL; TV kodu NASDAQ:TUR) |
| 5 | Asya kapanışları: Nikkei, KOSPI | TVC:NI225 (alt: KRX:KOSPI) | uluslararası | gap öncü | Nikkei → gap corr 0,255 (t 4,6; IS 0,30 / OOS 0,20); tam faktör kontrolünde kısmi 0,19 (t 8,4); KOSPI 0,16 (t 7,0) | + | hayır | ORTA | doğrulanmadı (y_ag: A1 ayakta) |
| 6 | OYAK'ın %42,8 payı devralması (olay, 09.06 / 24.07.2026) | BIST:TKFEN (alt: BIST:OYAKC / BIST:HEKTS / BIST:EREGL) | yurt içi | olay | Görüşme KAP'ı (09.06.2026): CAR(0,0) −%5,3 (z −1,8), CAR(0,10) −%15,3 (z −1,6). Devir tamamlanınca (24.07.2026): CAR(0,10) +%40,9 (z 4,2; r1_kimya); ry_grup: AR0 +%3,9, CAR[2,10] +%33,9 (t 3,8), CAR[0,20] +%31,7. Aynı olayda EREGL CAR −%12 | + (devir tamamlanınca) | hayır (tek olay; genellenemez) | ORTA | doğrulanmadı (r1_kimya ORTA, ry_grup DÜŞÜK-tek olay) |
| 7 | ENKAI (taahhüt akranı) | BIST:ENKAI | yurt içi | senkron | pc 2010+ 0,138 (t 6,7; 2005+ 0,175); IS 0,10 / OOS 0,15; 15/17 yıl; haftalık 0,19, aylık 0,34, USD bazlı aylık 0,27; son 250g 0,02; f_y_hisse 0,135 | + | hayır (senkron) | ORTA | düzeltildi (K-c: YÜKSEK → ORTA; 0,17 yalnız 2005+ başlangıcıyla çıkıyor, OYAK devriyle bağ ≈0) |
| 8 | USDTRY / sepet kur (USD-gelirli karakter) | BIST:USDTRY1! (alt: FX:USDTRY / (BIST:USDTRY1!+BIST:EURTRY1!)/2) | yurt içi | senkron | pc: VİOP USDTRY (15:00 hizalı) 0,092 (t 4,5; IS 0,19 / OOS 0,03; %60 yıl; 1y −0,05), VİOP sepet 0,080, EURTRY 0,064; Yahoo USDTRY 0,062 (IS 0,10 / OOS 0,01); doğrulama taraması +0,062. Rejim: yüksek kur-vol 0,13 / orta 0,07 / düşük −0,03; 2025-03 sonrası 0,04. Haftalık XU100'e göreli geçişkenlik +0,16 (t 2,4); 2021-Q4 kriz penceresinde TL getirisi/USDTRY değişimi 0,90–1,05. Yahoo kur_t−1 → gap t −3,2 (IS −5,9 / OOS 0,0), → gün-içi t 2,3 (IS 3,4 / OOS −0,3). Tam dönem ORTA / güncel DÜŞÜK; Yahoo sepet kur pc +0,060 (t 3,7; IS 0,10 / OOS 0,01; DÜŞÜK); sepet kur_t−1 → gap t −2,6 (IS −5,7 / OOS 1,0; DÜŞÜK) | + (TL değer kaybında TKFEN XU100'den iyi) | hayır (senkron; kur şokunda göreli hedge) | ORTA | doğrulandı, kısmen (TR3: TKFEN–USDTRY pc +0,062) |
| 9 | TL faizi: DİBS 5y/10y/2y (pozitif) | TVC:TR05Y (alt: TVC:TR10Y / TVC:TR02Y) | yurt içi | senkron | pc 5y +0,093 (t 3,4; IS 0,09 / OOS 0,09; %69 yıl; 3y 0,18 / 1y 0,08; FDR), 10y +0,084 (IS 0,10 / OOS 0,08), 2y +0,076 (IS 0,05 / OOS 0,09; 3y 0,16) | + (faiz ↑ → TKFEN göreli ↑) | hayır (senkron) | ORTA | doğrulanmadı (ry_makro_y #1: faiz ↑ günlerinde ENKAI/SISE/TKFEN +0,08) |
| 10 | Seans dışı negatif siyasi şoklar (olay) | BIST:XU100 (alt: BIST:XBANK) | yurt içi | olay | 13 seans dışı negatif siyasi şokta XU100 gap −264 bps (t −3,0); kesitte TKFEN XU100'ün +177 bps üstünde (ENKAI +210, TAVHL +223; bankalar 120–140 bps altında); 5 günde sürüklenme yok | + (göreli) | hayır (betimleyici/korunma bilgisi) | ORTA | düzeltildi (V3 ORTA) |
| 11 | Banka↔sanayi rotasyonu (XLBNK, XUSIN) | BIST:XLBNK (alt: BIST:XUSIN / BIST:XBANK) | yurt içi | senkron | XLBNK (TKFEN'i içermez) kısmi −0,13 (t −4,5; IS −0,00 / OOS −0,14; yılların %100'ü; ham corr IS 0,65 / OOS 0,33); XUSIN ham kısmi +0,10 (t 4,3; hisse-hariç hesaplanamadı); XUMAL −0,05 (t −2,1; DÜŞÜK) | − banka / + sanayi | hayır | ORTA | doğrulandı, genel (K-d: banka↔sanayi rotasyonu faktörü, kısmen mekanik) |
| 12 | AKMGY (Tekfen ortaklı GYO) | BIST:AKMGY | yurt içi | senkron | pc 0,064 (t 3,8); IS 0,02 / OOS 0,09; %88 yıl | + | hayır | ORTA | doğrulanmadı (ortaklık oranı teyit edilmedi) |
| 13 | TUR_t−1 → TKFEN gün-içi (USD-gelirli faktör) | NASDAQ:TUR (alt: NASDAQ:EMB) | uluslararası | gün-içi öncü | TUR_t−1 → gün-içi t −3,0 (IS −2,1 / OOS −2,2; FDR yok); doğrulama taramasında TKFEN −3,6 (ENKAI −5,1, THYAO −4,4): ortak USD-gelirli faktör; EMB_t−1 → gün-içi t −2,4; TUR−EEM t −2,4; İstatistik DÜŞÜK (ortak USD-gelirli faktör, rejime bağlı) / işlem ÇOK DÜŞÜK | − | hayır | DÜŞÜK | düzeltildi (v_H45_b: ortak USD-gelirli/ihracatçı faktörü, 2020–23 rejimine bağlı) |
| 14 | Brent gece / aylık | ICEEUR:BRN1! (alt: TVC:UKOIL) | uluslararası | gap öncü | Brent gece → gap corr −0,16 (1y −0,33; IS 0,04 / OOS −0,29); aynı sinyal → gün-içi t 3,2 (tek test, FDR yok); günlük senkron pc 0,007, aylık USD bazlı pc +0,14 | − (gap, 2025+) / + (aylık) | hayır | DÜŞÜK | düzeltildi kısmen (B5: 2026 petrol şoku tek ortak faktör) |
| 15 | Asya/Hindistan tarama: Fuyao Glass (HK), Adani Green, SBI, Sumitomo Chemical India, Tata Power | HKEX:3606 (açılmayabilir) (alt: OTC:FYGGY / AMEX:FXI / NSE:ADANIGREEN / NSE:SBIN / NSE:SUMICHEM / NSE:TATAPOWER) | uluslararası | çok günlük | Fuyao (3606.HK) senkron pc 0,044 (IS 0,03 / OOS 0,06; %58 yıl); Adani Green 0,044; SBIN/SUMICHEM/TATAPOWER t+2..5 öncülük t 4,2–4,4 (kova içi BH geçer, tüm ailede 0; /r/≈0,07) | + | hayır (maliyet sonrası kâr beklenmez) | DÜŞÜK | doğrulandı (olumsuz: TR3 – max /pc/ ≤0,10, replikasyon yok) |
| 16 | Bitcoin gece | BITSTAMP:BTCUSD (alt: COINBASE:BTCUSD) | uluslararası | gap öncü | BTC gece → gap corr 0,11 (IS 0,19 / OOS 0,03); hafta sonu BTC → Pazartesi c ≈0 | + | hayır | DÜŞÜK | doğrulanmadı |
| 17 | Gübre hisseleri GUBRF / HEKTS (yurt içi) | BIST:GUBRF (alt: BIST:HEKTS) | yurt içi | senkron | GUBRF pc 0,118 (t 5,8; IS −0,02 / OOS 0,06; genişletilmiş kontrollü 0,08; haftalık 0,10); HEKTS 0,078 (IS 0,02 / OOS 0,01); TKFEN–HEKTS pc 0,21 → 0,01 OYAK devrinden sonra (n 101) | + | hayır | DÜŞÜK | doğrulanmadı |
| 18 | OYAKC_t−1 → TKFEN | BIST:OYAKC | yurt içi | gün-içi öncü | OYAKC_t−1 → TKFEN gün-içi t 2,8 (IS 0,9 / OOS 2,75); çok günlük t 3,4 (IS 1,6 / OOS 3,1); 712 testte FDR yok; İstatistik DÜŞÜK / işlem ÇOK DÜŞÜK | + | hayır (yalnız OOS) | DÜŞÜK | doğrulanmadı |
| 19 | Kapanış müzayedesi hareketi (CA) → ertesi sabah | BIST:TKFEN | yurt içi | mikroyapı | Hisse bazında gap_t+1 b −0,13 (t −1,1; IS −0,26 / OOS −0,05); doğrulamada /CA/>25 bps portföyünde TKFEN en güçlü hisselerden (30–43 bps/işlem; ODAS, TOASO, ENJSA, BRSAN, FROTO, HEKTS ile) | − | hayır: VİOP pay vadelisiyle uygulanamaz (SSF uzlaşması müzayedeyi izlemiyor); spotta yalnız kapanış fiyatından işlemler penceresi | DÜŞÜK | düzeltildi (YG2: ilişki ORTA, VİOP'ta net kâr DÜŞÜK) |
| 20 | DOHOL | BIST:DOHOL | yurt içi | senkron | pc 0,056 (IS −0,01 / OOS 0,12; %69 yıl); DOHOL_t−1 → TKFEN gün-içi t −2,0 (IS −1,4 / OOS −1,5; hacim filtreli −2,2) | + (senkron) / − (öncülük) | hayır | DÜŞÜK | doğrulanmadı |
| 21 | XHOLD / XINSA (Holding, İnşaat endeksleri) | BIST:XHOLD (alt: BIST:XINSA) | yurt içi | senkron | Ham kısmi 0,21 (t 9,8); hisse-hariç 0,06 (IS 0,10 / OOS 0,03; %69 yıl); XINSA (İnşaat) ham kısmi 0,12 (t 5,8; ham corr 0,40; TKFEN ağırlığı ≈0; hisse-hariç hesaplanamadı; DÜŞÜK) | + | hayır | DÜŞÜK | doğrulanmadı |
| 22 | Gece/gün-içi ayrışması | BIST:TKFEN | yurt içi | rejim | h1 döneminde ort. gap +28,8 bps, gün-içi +7,7 bps (diğer holdinglerin tersine gün-içi pozitif; 2026 OYAK rallisi) | gap +, gün-içi + (2026 olay dönemi) | hayır | DÜŞÜK | düzeltildi (genel: gap pozitifliği çoğunlukla TL taşıma maliyeti) |
| 23 | Libco/ARY %32 pay devri (olay, 26.06.2026) | BIST:TKFEN | yurt içi | olay | AR0 +%6,5 (t 2,3), CAR[0,1] +%6,9, CAR[2,10] −%3,1 (t −0,4), CAR[0,20] +%16,8 (XU100 piyasa modeli) | + | hayır (tek olay) | DÜŞÜK | doğrulanmadı (tamamlanma tarihi doğrulanamadı) |
| 24 | Üre/DAP gübre fiyatı (Toros Tarım) | CBOT:UFV1! (alt: CBOT:UME1!) | uluslararası | hipotez | Test edilemedi (Yahoo'da veri yok); vekil ABD gübre hisseleri ilişkisiz (olumsuzlar) | + (beklenen) | hayır | ÇOK DÜŞÜK | doğrulanmadı (test edilemedi; TV kodu tv_final'de KOD durumunda) |
| 25 | OYAK grubu (HEKTS, OYAKC, EREGL) ortak fiyatlanma | BIST:OYAKC (alt: BIST:HEKTS / BIST:EREGL) | yurt içi | hipotez | Devirden sonra 101–107 gün: TKFEN–EREGL pc −0,15, TKFEN–OYAKC 0,01→0,06, TKFEN–HEKTS 0,21→0,01: henüz ortak fiyatlama yok | + (beklenen) | hayır | ÇOK DÜŞÜK | doğrulanmadı (kısa örneklem; 2027'de yeniden test) |

## Test edilip ilişki bulunmayanlar (olumsuzlar)
- Gübre emsalleri CF, NTR, MOS, YAR, OCI, IPI/LXU/UAN pc −0,02…0,00 (CF −0,023, NTR −0,022, MOS −0,007); ABD gübre sepeti_t−1 → TKFEN gün-içi backtest OOS −17,1 bps (t −2,3; 10 bps maliyet): gap'te fiyatlanıp gün içinde geri dönüyor.
- Yabancı müteahhitler FLR, KBR, J, ACS, FER, SKA, HOT pc −0,03…0,00.
- Tahıllar (ZW, ZC, ZS), TTF, Henry Hub, Kazakistan tengesi (KZT) pc −0,03…+0,01; Brent günlük pc 0,007.
- Küresel endeksler S&P 500, ACWI, STOXX600, DAX, VIX pc −0,03…+0,02.
- Doğrulama (TR3, YÜKSEK): XU100 ve USDTRY dışında sağlam küresel sürücü yok (max |pc| ≤0,10).
- Hakem: TKFEN yabancı emsal sepeti (CF, YAR, NTR, MOS, OCI + EPC müteahhitleri) → hedge'li gün-içi −0,55 bps/σ (t −0,15); VİOP −2,5 (t −0,4); ENKAI artığı_t−1 → TKFEN t 1,15.
- Kendi açılış gap'i fade: IS +19,6 bps (t 1,6) / OOS +3,1 (t 0,1); ilk 30 dk VWAP vekili −19,7 bps.
- VİOP baz anomalisi → ertesi spot gap t 0,9, → vadeli gün-içi t −0,8 (FDR yok).
- ENKAI_t−1 → TKFEN gün-içi t 0,4 (f_y_hisse); holding akranlarının gap'i → TKFEN gün-içi b 0,08 (t 0,7); ilk yarım saat momentumu b −0,03 (t −1,5).
- Gram altın (VİOP/Yahoo/15:00) pc 0,02–0,04; TLREF 0,02; zımni faiz 0,02–0,03; EMB senkron −0,03; 15:00 saatlik USDTRY −0,03.
- Yabancı akış (TCMB haftalık) corr 0,02 (t 0,7), öncülük yok.
- Gece sürücü sepeti → 07:30 sonrası gün-içi: IS +22,3 / OOS −11,4 bps; gap kalıntısı t −1,7.
- 5 dk ve saatlik endeks/hisse öncülüğü 0 FDR; CF 15:00 UTC hizalı senkron ve kapanış sonrası → gün-içi FDR'den geçmedi.
- Tarama: Curtiss-Wright −0,053, Mitsubishi Heavy −0,044, Toyota −0,045 (ÇOK DÜŞÜK; mekanizma yok).
- DAX ve STOXX600 gece → gap corr −0,06 / −0,05 (t ≈−1,1), altın gece 0,04 (t 0,9), Hang Seng → gün-içi |t| ≤1,3, USD/CNH 07:00–08:30 −0,04 (hepsi ÇOK DÜŞÜK); ons altın senkron pc −0,034, EURUSD −0,024 (EURUSD_t−1 → gün-içi OOS t −2,2; ÇOK DÜŞÜK).
- Hisse-hariç endeks h1 (XU030, XBANK, XLBNK, XUSIN, XHOLD) → TKFEN Σβ |t| ≤1,4; m5 (60 gün) |t| ≤1,0; 5 dk / 60 dk KCHOL, SAHOL, bankalar, TUPRS, ASELS, BIMAS → TKFEN 0 FDR (ÇOK DÜŞÜK).

## Çin/HK kodları yerine test edilmiş alternatifler
- Fuyao Glass (3606.HK): HKEX:3606 açılmayabilir → OTC:FYGGY (OTC gri piyasa, bayat/boşluklu grafik riski) veya AMEX:FXI (geniş Çin büyük şirket ETF'i).
- Asya gap bilgisi için Şanghay yerine CBOE:CNYA / AMEX:ASHR (haftalık r 0,84–0,86).

## Açık sorular
- OYAK grubu (HEKTS, OYAKC, EREGL) ile ortak faktör oluşuyor mu? 2027'de en az 250 günlük örneklemle yeniden test edilmeli.
- OYAK yönetiminde Toros Tarım–Hektaş birleşmesi/sinerjisi gübre fiyatına (üre, CBOT:UFV1!) duyarlılığı artırır mı?
- ENKAI–TKFEN taahhüt bağının 2026'daki kaybı kalıcı mı, olay dönemine mi özgü?

## TradingView izleme listesi

```
BIST:TKFEN,BIST:TKFEN1!,BIST:ENKAI,BIST:OYAKC,BIST:HEKTS,BIST:GUBRF,BIST:EREGL,BIST:AKMGY,BIST:XU100,BIST:XU030,BIST:XYUZO,BIST:XLBNK,BIST:XUSIN,BIST:USDTRY1!,FX:USDTRY,TVC:TR05Y,TVC:TR10Y,CME_MINI:ES1!,NASDAQ:TUR,NASDAQ:EMB,TVC:NI225,KRX:KOSPI,ICEEUR:BRN1!,CBOT:UFV1!,AMEX:FXI,BIST:XINSA
```
