# TTKOM — Türk Telekom (Telekom)

Spot: `BIST:TTKOM` · VİOP pay vadelisi: `BIST:TTKOM1!`

## Özet
TTKOM'un dış sürücü beklentisi düşüktü ve doğrulandı: XU100 ve USDTRY dışında sağlam küresel sürücü yok (Avrupa telekom kısmi corr ≈0; 39.360 testte replike olan 0). Fiyatı ağırlıkla yurt içi faktörler belirliyor: TCELL (kısmi 0,31; OOS 0,40), hisse-hariç iletişim endeksi (0,30) ve piyasa betası; TKC ile bağ (0,21) TCELL üzerinden geliyor. TL kuru ve faizle negatif senkron bağ var (VİOP USDTRY pc −0,10, 5y DİBS −0,09; IS'de güçlü, OOS'ta −0,03/−0,04'e zayıf — yönetilen kur/rejim) — ORTA. Gece bilgisi (ES, TUR, USDTRY) gap'te fiyatlanıyor; işlenebilir gün-içi öncülük bulunamadı.

## Sürücüler
| # | Güven | Kapsam | İlişki | Sürücü | TradingView | Rakam | İşlenebilir | Doğrulama |
|---|---|---|---|---|---|---|---|---|
| 1 | YÜKSEK | UL | gap öncü | Gece ABD vadelileri (ES, NQ) → gap — + | CME_MINI:ES1! (alt: CME_MINI:NQ1! \| SP:SPX) | gece ES 0,37 (IS 0,40 / OOS 0,37); gece alt pencereleri (15–16 / 16–20 / 20–07 UTC) t 1,8 / 4,7 / 4,8; G1: piyasa faktörü — XU100 gap kontrolünden sonra hisseye özgü ≈0,04; y_ag tam faktör kontrolüyle ES_{t-1}→gap 0,03, NQ 0,015 (yalnız ortak faktör) | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | doğrulandı (G1 KABUL YÜKSEK) |
| 2 | YÜKSEK | Yİ | senkron | Turkcell (TCELL) — + | BIST:TCELL (alt: BIST:TCELL1!) | pc 0,29–0,31 (IS 0,19–0,20 / OOS 0,40; %100 yıl); tam faktör kontrollü OOS t 13,4 | hayır — senkron; TCELL_{t-1}→TTKOM gün-içi t 1,8 (DÜŞÜK) | doğrudan doğrulanmadı (y_ag claim_check YÜKSEK; senkron kümeler ayakta) |
| 3 | YÜKSEK | Yİ | senkron | BIST İletişim endeksi (hisse-hariç) — + | BIST:XILTM (alt: BIST:XUHIZ) | hisse-hariç pc 0,30 (IS 0,17 / OOS 0,41; %100 yıl); ham R² 0,52 (TTKOM ağırlığı ~%20); XUHIZ corr 0,67 (TTKOM ağırlığı ~%2; hisse-hariç corr 0,64; pc 0,21; kaynakta DÜŞÜK) | hayır — senkron | kısmen (hisse-hariç sektör faktörü ayakta) |
| 4 | YÜKSEK | Yİ | senkron | BIST piyasa faktörü (XU100) — + | BIST:XU100 (alt: BIST:XU030D1! \| BIST:XU030 \| BIST:XUTUM \| BIST:XYUZO \| BIST:XTUMY) | corr 0,67 (IS 0,63 / OOS 0,70); R² 0,45; Shapley piyasa %26,4; geniş endeksler aynı faktör: XU030 0,66 (pc −0,03), XUTUM 0,67 (pc 0,02), XYUZO (BIST 100-30) 0,62 (hisse-hariç pc 0,04), XTUMY 0,55 (pc 0,06) — XU100 ötesinde bilgi yok | endeks vadelisiyle hedge | doğrulandı (v_duyarlilik) |
| 5 | YÜKSEK | Yİ | mikroyapı | VİOP baz anomalisi_t → ertesi spot açılış gap'i — + | BIST:TTKOM1! (alt: BIST:TTKOM) | t 3,11 (IS 2,17 / OOS 2,51); FDR geçti | hayır — gap'te fiyatlanır | kısmen (v_metodoloji: baz anomalisi ayakta) |
| 6 | ORTA | UL | senkron | Turkcell ADR (TKC) — + | NYSE:TKC | corr 0,48 (1y 0,65); pc 0,21 (IS 0,19 / OOS 0,29; %100 yıl); tam faktör kontrolüyle t 0,68 → bağ TCELL üzerinden; TKC parite sapması TTKOM gün-içini öngörmüyor (BT IS −13 bps; plasebo t 0,6) | hayır — senkron | kısmen (S1 TTKOM–TKC 0,218 yeniden üretildi; ry_ag: ortak faktöre indirgeniyor); y_ag tam faktör kontrolüyle 0,015 (OOS 0,05) → 'yalnız ortak faktör' |
| 7 | ORTA | UL | senkron | iShares MSCI Turkey (TUR) senkron — + | NASDAQ:TUR | pc +0,086 (IS 0,11 / OOS 0,07; %69 yıl; FDR evet); 3y 0,01, 1y 0,09 | hayır — TUR BIST kapanışından sonra da işlem görür | doğrulanmadı |
| 8 | ORTA | UL | gap öncü | Gece Türkiye/EM risk vekilleri (TUR, EMB, TUR−EEM, USDTRY gece) → gap — TUR/EMB +, USDTRY − | NASDAQ:TUR (alt: NASDAQ:EMB \| formül: NASDAQ:TUR/AMEX:EEM \| FX:USDTRY \| FX:EURTRY \| AMEX:EEM) | TUR_{t-1}→gap t 7,3 (IS 6,9 / OOS 4,1); TUR gece 0,25 (IS 0,16 / OOS 0,32); EMB t 3,3; TUR−EEM t 3,7 (IS 3,8 / OOS 1,5); gece USDTRY → gap −0,135 (t −3,6; 2024+); gece EURTRY → gap +0,16 (IS 0,05 / OOS 0,29; DÜŞÜK), gece EEM 0,12 (IS 0,07 / OOS 0,16; DÜŞÜK) | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | doğrulandı-düzeltildi (G4 KABUL ORTA) |
| 9 | ORTA | UL | gap öncü | Nikkei (aynı gün) → gap — + | TVC:NI225 (alt: KRX:KOSPI) | 0,34 (IS 0,38 / OOS 0,30) | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | doğrulanmadı |
| 10 | ORTA | Yİ | senkron | USDTRY / kur sepeti (negatif) — − | BIST:USDTRY1! (alt: FX:USDTRY \| BIST:EURTRY1! \| FX:EURTRY) | VİOP USDTRY pc −0,10 (IS −0,19 / OOS −0,03; %80 yıl; FDR); VİOP sepet −0,10 (%90 yıl); Yahoo USDTRY −0,04…−0,06 (IS −0,10 / OOS −0,04–0,05; %76–94 yıl negatif); haftalık kur geçişkenliği XU100'e göre −0,28 (t −2,8); USDTRY_{t-1}→gap t −4,7 (IS −7,6 / OOS −0,4); EURTRY_{t-1}→gap t −3,3 (IS −6,5 / OOS 1,0) ve sepet_{t-1}→gap t −4,0 (IS −7,4 / OOS 0,5) — ORTA işlenemez, OOS'ta yok; gram altın TL_{t-1}→gap t −2,1 (IS −3,0 / OOS −0,1; DÜŞÜK); kur-vol rejimlerinde pc −0,11 / −0,05 / −0,02 (DÜŞÜK; bağ yüksek kur oynaklığında güçleniyor) | hayır — senkron; gap kısmı 2021 sonrası kayboldu | kısmen (TR3: TTKOM–USDTRY −0,059; v_metodoloji: TRY ilişkileri yönetilen kurda ölçülemez) |
| 11 | ORTA | Yİ | senkron | TL faizi (DİBS 5y/10y/2y) — − | TVC:TR05Y (alt: TVC:TR10Y \| TVC:TR02Y) | 5y pc −0,09 (IS −0,17 / OOS −0,04; %85 yıl; FDR); 10y −0,07 (IS −0,15 / OOS −0,03); 2y −0,06 (IS −0,11 / OOS −0,04); gün-içi öncülük: 2y_{t-1} t −2,8 (IS −1,2 / OOS −2,6), 5y_{t-1} t −2,4 (IS 0,1 / OOS −2,8) → DÜŞÜK | hayır — senkron; gün-içi kısmı yalnız OOS | doğrulanmadı |
| 12 | ORTA | Yİ | mikroyapı | VİOP 09:30 açılışı → spot açılış gap'i — + | BIST:TTKOM1! | corr 0,44 (R² 0,19) | hayır — spot gap'i tahmin eder | doğrulanmadı |
| 13 | DÜŞÜK | UL | gap öncü | Gece Brent → gap — − | ICEEUR:BRN1! (alt: TVC:UKOIL) | −0,36 (IS −0,15 / OOS −0,46) | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | kısmen (2026 rejimi şişiriyor) |
| 14 | DÜŞÜK | UL | gün-içi öncü | BIST açılışından sonra Asya/ABD sabah hareketi (HSI, ES) → kalan gün — + | TVC:HSI (alt: AMEX:FXI \| CME_MINI:ES1!) | HSI 07:30→kapanış → TTKOM kalan gün t 2,4 (IS 0,06 / OOS 0,12; brüt OOS 12,9 bps); ES 07:00→08:30 → kalan gün t 2,95 (IS 0,12 / OOS 0,11; brüt OOS 16,6 bps) | sınırda — brüt, maliyetsiz; tek test | doğrulanmadı |
| 15 | DÜŞÜK | UL | gap öncü | Bitcoin hafta sonu / gece → Pazartesi gap — + | BITSTAMP:BTCUSD (alt: COINBASE:BTCUSD) | hafta sonu corr 0,22 (2015–20 0,03 / 2021+ 0,18); hafta içi gece 0,23 → hafta sonuna özgü değil; gün-içi devam yok | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | kısmen (kaynak: gece→gap ORTA, hafta sonu DÜŞÜK; y_ag tam faktör kontrolüyle BTC_{t-1}→gap 0,015 → ÇOK DÜŞÜK, yalnız ortak faktör) |
| 16 | DÜŞÜK | UL | gün-içi öncü | Gece altın (açılıştan önce bilinir) → gün-içi — + | COMEX:GC1! (alt: FX_IDC:XAUTRYG) | t 2,2 (yarılar 1,9 / 1,4); FDR yok (255 test) | hayır | doğrulanmadı |
| 17 | DÜŞÜK | UL | gap öncü | Şanghay Bileşik (aynı gün) → gap — + | CBOE:CNYA (alt: AMEX:ASHR \| AMEX:KBA) | gap corr 0,17 (t 3,5; IS 0,10 / OOS 0,27); gün-içi ≈0 (t −0,1); y_ag: açılışta fiyatlanır; Çin'e özgü kısım EEM kontrolünden sonra ≈0 | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | kısmen (v_cin genel: Çin'e özgü faktör ≈0 → DÜŞÜK) |
| 18 | DÜŞÜK | Yİ | olay | İmtiyaz uzatımı (KAP 27.08.2025, 28.02.2050'ye) — − | BIST:TTKOM | AR 27.08 +48, 28.08 −388, 29.08 −419 bps; CAR(27.08–03.09) −710 bps; TCELL de −290 / −204 bps | hayır — tek olay | doğrulanmadı |
| 19 | DÜŞÜK | Yİ | gün-içi öncü | Yurt içi hisse/endeks t-1 → TTKOM gün-içi (PGSUS, XULAS, THYAO, TCELL) — + | BIST:PGSUS (alt: BIST:XULAS \| BIST:THYAO \| BIST:TCELL) | PGSUS_{t-1} t 3,6 (IS 2,1 / OOS 2,8; BH yok); XULAS_{t-1} t 3,5 (IS 2,3 / OOS 2,3; q 0,40); THYAO Granger p=2 t 3,6 (IS 1,8 / OOS 2,7; BH q 0,04, OOS'ta tekrarlamadı); TCELL_{t-1} t 1,8 (IS 2,1 / OOS 0,6; PRE −1,9); XULAS_{t-1}→TTKOM cc t 3,5 (IS 2,2 / OOS 2,3; q 0,23) | hayır | doğrulanmadı (ry_ag: FDR'den geçen gün-içi kenarlar OOS'ta tekrarlamadı; ry_hisse BH 0) |
| 20 | DÜŞÜK | Yİ | mikroyapı | 5 dk endeks → TTKOM gecikmeli tepki — + | BIST:XU030 (alt: BIST:XBANK \| BIST:XLBNK) | XU030→TTKOM b1 0,106 (t 4,9; XU030'daki 1σ 5 dk hareket başına +2,6 bps, tepki 5 dk); XBANK/XLBNK (hisse-hariç) m5 Σβ 0,22 (t 3,8; fon krizinde 0,24); AKBNK/ISCTR 5 dk Σβ 0,17–0,20; 5 dk XU030 Σb1..6 0,23 (t 4,8; iki yarıda b1 0,115; Wald FDR evet); XLBNK/AKBNK/ISCTR Wald FDR evet ama b1 ikinci yarıda ≈0; saatlik USDTRY (h1, ≥30 dk önde) t −3,05 ve sepet kur (BSK) t −2,8 (XU100 kontrollü −3,8/−2,7; 1.140 testte FDR yok; ÇOK DÜŞÜK); diğer 37 saatlik/5 dk satır FDR'den geçmiyor | hayır — spot tik 9,4 bps, barların %22'si değişmez | doğrulanmadı (fiyat adımı/bayat fiyat) |
| 21 | DÜŞÜK | Yİ | gap öncü | ASUZU t-2 → TTKOM gap — + | BIST:ASUZU | t 4,3 (IS 2,5 / OOS 3,6); yalnız (gap, lag) ailesinde BH; lider 3–15 kat daha illikit | hayır — gap | doğrulanmadı (ry_hisse: küçük-hisse faktörü) |
| 22 | DÜŞÜK | Yİ | rejim | Gece/gün-içi ayrışması ve kendi açılış gap fade — gap +, gün-içi − | BIST:TTKOM1! (alt: BIST:TTKOM) | h1 ort. gap +20,3 / gün-içi −7,8 bps; 8 bps BT IS −13,2 / OOS 15,1 (Sh 1,12); kendi gap fade IS 8,6 (t 0,9) / OOS 27,7 (t 1,3), h1 VWAP 25,8 (t 1,0) | sınırda — IS negatif | düzeltildi (YG1 DÜZELT DÜŞÜK) |
| 23 | DÜŞÜK | Yİ | senkron | Diebold–Yilmaz ağ merkeziliği ('net yayıcı') — + | BIST:XU100 | net spillover +%13,1 (2014–17 −7,0 / 2021–23 +20,2 / 2024–26 +17,9 / son 1y +26,8; B-hizalı +18,9) | hayır — yön bilgisi değil | ry_ag kendi yöntem eleştirisi: günlük veride 'yayıcı/alıcı' = korelasyon merkeziliği (H=1 / H=10 Spearman 0,994); yön yorumu DÜŞÜK |
| 24 | ÇOK DÜŞÜK | UL | senkron | Tarama yan bulguları (Maanshan Steel, Eldorado Gold, Hyosung, Palantir, KRBN) | OTC:MAANF (alt: HKEX:323 (açılmayabilir) \| AMEX:SLX \| NYSE:EGO \| KRX:298040 \| NASDAQ:PLTR \| AMEX:KRBN) | 0323.HK pc −0,061 (OOS −0,07); EGO/ELD 0,06; Hyosung −0,06; PLTR −0,06; KRBN_{t-1} −0,09 (TR3) | hayır | doğrulanmadı (mekanizma yok; TR3: FDR+replikasyon yok) |
| 25 | ÇOK DÜŞÜK | Yİ | olay | TVF sepeti artığı ve TVF stres rebound — + | BIST:XU100 | TVF sepeti artığı_{t-1}→TTKOM gün-içi t 2,3 (5 üyede çoklu test sonrası anlamsız); TVF ortak faktör pc −0,02; stres sonrası rebound OOS +56 bps (t 1,5) | hayır | doğrulanmadı |
| 26 | ÇOK DÜŞÜK | Yİ | hipotez | İmtiyaz bedeli USD borcu → kur duyarlılığında artış; BTK tarife kararları — − | BIST:TTKOM | test edilmedi (bedel 2026'dan itibaren ödeniyor; kur bağının OOS zayıflığı yönetilen kurdan) | bilinmiyor | test edilemedi |

## Olumsuz bulgular (test edildi, ilişki yok/çöktü)
- Avrupa telekom sepeti pc −0,003 (IS 0,06 / OOS 0,03); EM telekom ≈0 — dış sürücü beklentisi düşük, doğrulandı.
- TR3: XU100+USDTRY dışında sağlam küresel sürücü yok (max |pc| ≤0,10; 39.360 test; FDR+replikasyon 0).
- TKC parite sapması TTKOM gün-içini öngörmüyor (BT IS −13 bps; S2 plasebo t 0,6).
- Hakem telekom emsal artığı → gün-içi 2,87 bps/σ (t 0,85; q 0,65); VİOP t 1,6.
- TKC gece → gap 0,04 (t 0,8).
- Kapanış müzayedesi → ertesi sabah t −0,4; ilk yarım saat momentum OOS 0,4 bps; sektör akranı (TCELL) gap → gün-içi b 0,01 (t 0,2).
- VİOP baz anomalisi → vadeli gün-içi t −0,7.
- Yurt içi 47×177 hisse öncülük taraması BH 0; saatlik hisse öncülüğü BH 0.
- Gece altın 0,11 (IS −0,12 / OOS 0,21), DAX/STOXX ≈0,04 → gap; gece sürücü sepeti 07:30 girişli BT IS 38,7 / OOS −6,4 bps; açıklanamayan gap kalıntısı ≈0; Nikkei/KOSPI/Şanghay aynı gün → gün-içi |t| ≤1,9 — hepsi ÇOK DÜŞÜK.
- Hisse-hariç XU030/XILTM/XU100_{t-1} → TTKOM cc/gap/gün-içi |t| ≤2,1 (BH yok; ÇOK DÜŞÜK); TCMB haftalık yabancı akış corr −0,04 (t −1,0).
- 1y DİBS, TLREF, zımni TL faizi (VİOP 1–2/1–3 ay), VİOP gram altın, Yahoo gram altın, 15:00 UTC hizalı USDTRY/sepet/gram altın, EMB ve TUR−EEM senkron pc |≤0,05| (ÇOK DÜŞÜK).

## Çin/HK kodları yerine test edilmiş alternatifler
- 000001.SS (Şanghay Bileşik; SSE kodu VERİLMEZ) -> CBOE:CNYA (haftalık r 0,85, YÜKSEK) | AMEX:ASHR (0,84) | AMEX:KBA (0,80)
- ^HSI (Hang Seng) -> TVC:HSI (HKEX'e bağlı olmayan TV akışı; HSI:HSI de var) - açılmazsa AMEX:FXI (haftalık r 0,87) | NASDAQ:MCHI (0,86)
- CNH=X (offshore yuan) -> FX:USDCNH (Çin borsası değil; tv_final alternatifi FX_IDC:USDCNH; onshore vekil FX_IDC:USDCNY, haftalık r 0,75, ORTA)
- 0323.HK (Maanshan Iron & Steel; tarama yan bulgusu, ÇOK DÜŞÜK) -> HKEX:323 açılmayabilir; alternatif OTC:MAANF (gri piyasa, bayat olabilir) | AMEX:SLX

## Varyans ayrıştırması
Shapley (2014–26, düz. R² 0,50): piyasa %26,4, sektör (TCELL) %19,7, küresel-8 %2,5, TR makro (USDTRY+TUR) %1,3, hisseye özgü %50,2. Küresel pay 2024–26 %2,8, son 1y %7,1; küresel pay sırası tam 12., son 1y 18.

## VİOP likidite / maliyet
BIST:TTKOM1! sınıf B: 12 ay medyan günlük hacim 524 mn TL (11,5 mn USD), medyan 14.047 işlem, açık pozisyon ~798 mn TL; tik 0,01 TL (12 ay medyan 1,7 bps, son fiyatla 2,2); gidiş-dönüş maliyet küçük emir 6,1 bps, muhafazakâr 8,1, 1 mn TL 16,2, bireysel 22,9 bps; vadeli/spot hacim 0,37.

## Açık sorular
- İmtiyaz bedelinin (2,5 mlr $) ödemeye başlanmasıyla kur/faiz duyarlılığı serbest kur rejiminde yeniden test edilmeli.
- HSI/ES sabah hareketinin kalan güne yansıması (brüt 13–17 bps) maliyet sonrası ve ikinci örneklemde tekrarlanmalı.

## TradingView izleme listesi
```
BIST:TTKOM, BIST:TTKOM1!, BIST:TCELL, NYSE:TKC, BIST:XILTM, BIST:XU100, BIST:XU030D1!, BIST:USDTRY1!, FX:USDTRY, TVC:TR05Y, TVC:TR10Y, TVC:TR02Y, NASDAQ:TUR, NASDAQ:EMB, CME_MINI:ES1!, TVC:NI225, TVC:HSI, ICEEUR:BRN1!, XETR:DTE, LSE:VOD
```

Kısaltmalar: UL = uluslararası, Yİ = yurt içi; pc = XU100 kontrollü kısmi korelasyon; IS 2014–20 (aksi yazılmadıkça), OOS 2021–26; bps = baz puan. Güven: brifing ölçeği; doğrulama varsa doğrulayıcı etiketi.
