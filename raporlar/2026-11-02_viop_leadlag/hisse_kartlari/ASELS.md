# ASELS — Aselsan (Savunma elektroniği)

Spot: `BIST:ASELS` · VİOP pay vadelisi: `BIST:ASELS1!`

## Özet
ASELS 47 hisse içinde en 'yerli' hisselerden: küresel faktör payı yalnız %1,0 (son 1y %3,0), hisseye özgü pay %63. Avrupa savunma sepetiyle bağ 2022 sonrası doğdu (kısmi corr 2014–21 0,02 → 2022–26 0,11–0,13; doğrulandı, ORTA) ama büyük ölçüde savunma haber günlerinden geliyor; yeniden silahlanma haber günlerinde AR0 +358 bps (n küçük, DÜŞÜK). Hiçbir dış sürücü için işlenebilir gün-içi öncülük bulunamadı (EU savunma t-1 → gün-içi OOS Sh −0,52; 13.662 testte FDR 0). Yurt içinde banka↔sanayi rotasyonunun defansif tarafında (XBANK kısmi −0,17; son 250g −0,40) ve teknoloji endeksi/yerli savunma akranlarıyla senkron.

## Sürücüler
| # | Güven | Kapsam | İlişki | Sürücü | TradingView | Rakam | İşlenebilir | Doğrulama |
|---|---|---|---|---|---|---|---|---|
| 1 | YÜKSEK | Yİ | senkron | BIST piyasa faktörü (XU100) — + | BIST:XU100 (alt: BIST:XU030 \| BIST:XU030D1! \| BIST:XUTUM \| BIST:XYUZO \| BIST:XUSIN \| BIST:XMESY) | corr 0,60 (IS 0,54 / OOS 0,64); R² 0,36 (3y 0,30); Shapley piyasa %27,5; geniş endeksler aynı faktör: XU030 0,59 (pc −0,01), XUTUM 0,60 (pc 0,03), XYUZO (BIST 100-30) 0,55 (hisse-hariç pc 0,02; IS 0,14 / OOS −0,09), XTUMY 0,51 (pc 0,09); XUSIN 0,56 ve XMESY 0,51 (pc ≈0,035; ASELS içermez; DÜŞÜK) | endeks vadelisiyle hedge | doğrulandı (v_duyarlilik) |
| 2 | YÜKSEK | Yİ | senkron | BIST Teknoloji endeksi (hisse-hariç) — + | BIST:XUTEK | hisse-hariç pc 0,17 (IS 0,20 / OOS 0,15; %77 yıl); ham XUTEK corr 0,93 / R² 0,85 mekanik (ASELS ağırlığı ~%72) → hisse-hariç corr 0,48, R² 0,24 | hayır — senkron | kısmen (v_metodoloji: hisse-hariç sektör faktörü ayakta) |
| 3 | YÜKSEK | Yİ | mikroyapı | VİOP baz anomalisi_t → ertesi spot açılış gap'i — + | BIST:ASELS1! (alt: BIST:ASELS) | t 3,51 (IS 2,50 / OOS 2,42); 1.152 testte FDR geçti; kesitte +5,2 bps/sd (t 12,6) | hayır — gap'te fiyatlanır | kısmen (v_metodoloji: baz anomalisi ayakta, kapasite düşük) |
| 4 | YÜKSEK | Yİ | mikroyapı | VİOP 09:30 açılışı → spot açılış gap'i — + | BIST:ASELS1! | corr 0,535 (R² 0,29) | hayır — spot gap'i tahmin eder | doğrulanmadı |
| 5 | ORTA | UL | rejim | Avrupa savunma sepeti (RHM, BAE, Leonardo, Thales, Saab, Kongsberg, Hensoldt, Renk) — + | XETR:RHM (alt: LSE:BA. \| MIL:LDO \| EURONEXT:HO \| OMXSTO:SAAB_B \| OSL:KOG \| XETR:HAG \| XETR:R3NK \| CBOE:EUAD) | pc 2014–21 0,017 → 2022–26 0,113 (XU100+STOXX kontrolüyle 0,056 → 0,129, Fisher z 1,98); 2025+ 0,125 (+STOXX 0,157); 2022–26 yıllık 5/5 pozitif; 15:00 UTC hizalı RHM 0,135, LDO 0,111, SAAB 0,150, BAE 0,112; haftalık 0,08 → 0,22; üst %5 savunma günleri çıkarılınca 0,048 (t 1,6); tekil BAE pc 0,05–0,07 (OOS 0,13; FDR), Saab OOS 0,10; tarama: BAE ORTA (pc 0,074; IS 0,03 / OOS 0,13), Saab/Thales/RHM DÜŞÜK (0,06–0,07; OOS 0,10); y_ag tam faktör kontrolüyle BAE 0,10 (OOS 0,13), Saab 0,09 (OOS 0,11), Thales 0,09 ORTA kalır; EUAD (Avrupa A&D ETF, 2024-10+) pc 0,055 (savunma ajanı DÜŞÜK), ry_ag tam kontrolle 0,13 (kısa örneklem) | hayır — senkron; t-1 öncülük yok | doğrulandı (S3 KABUL ORTA) |
| 6 | ORTA | UL | olay | AB savunma şok günleri (veri güdümlü, \|z\|>2–3) — + | XETR:RHM (alt: LSE:BA. \| MIL:LDO \| EURONEXT:HO \| OMXSTO:SAAB_B \| OSL:KOG \| XETR:HAG \| XETR:R3NK \| CBOE:EUAD) | 2022–26: yukarı (n 13, \|z\|>3) AR0 +284 bps, aşağı (n 10) −181; z>2 günleri +127 bps (t 2,5, n 38), z<−2 −142 (t −3,6); 2014–21 +58 (t 1,9); ertesi gün etkisi yok | hayır — senkron; ertesi gün yok | kısmen (S4: veri güdümlü sürüm aynı yönde, 2022 sonrası güçlü ama senkron) |
| 7 | ORTA | UL | gap öncü | TUR / EMB t-1 → açılış gap'i — + | NASDAQ:TUR (alt: NASDAQ:EMB) | TUR_{t-1}→gap t 5,1–5,9 (IS 4,2 / OOS 3,3); EMB_{t-1}→gap t 3,3 (IS 3,2 / OOS 1,9); EMB senkron pc −0,05 (%77 yıl) | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | doğrulandı (genel: ABD t-1 etkisi gap'te, KABUL) |
| 8 | ORTA | Yİ | senkron | Banka↔sanayi rotasyonu (XBANK) — − | BIST:XBANK (alt: BIST:XLBNK \| BIST:XLBNKD1!) | XU100 kontrollü pc −0,16/−0,17 (t −7,1); son 250g −0,40 (ASELS defansif tarafta kaldı; TUPRS, BIMAS ile) | hayır — senkron | doğrulandı (K-d KABUL ORTA: genel rotasyon faktörü, kısmen XU100 artıklandırma mekaniği) |
| 9 | ORTA | Yİ | senkron | Otokar (OTKAR, yurt içi savunma emsali) — + | BIST:OTKAR | pc 0,11 (IS 0,14 → OOS 0,06; %100 yıl); ry_hisse 0,09 | hayır — senkron; OTKAR_{t-1}→ASELS gün-içi t 1,9 | doğrulanmadı |
| 10 | ORTA | Yİ | mikroyapı | Saatlik/5 dk banka endeksi → ASELS (ters) — − | BIST:XBANK (alt: BIST:XLBNK \| BIST:XHOLD) | saatlik XBANK (hisse-hariç) Σβ(1..3) −0,072 (t −3,0; IS −2,4 / OOS −2,3); 5 dk XBANK/XLBNK→ASELS b1 −0,09 (t −3,7; bar-içi −3,2; FDR evet); saatlik XHOLD (hisse-hariç) Σβ(1..3) −0,085 (t −2,7; IS −1,9 / OOS −2,0; DÜŞÜK); diğer 5 dk/60 dk kaynaklar FDR'den geçmiyor | hayır — maliyet | doğrulanmadı (kaynak YÜKSEK; küresel Bonferroni eşiği \|t\|≥5,5 geçilmiyor → ORTA) |
| 11 | DÜŞÜK | UL | olay | Yeniden silahlanma haber günleri (ReArm Europe vb.) — + | XETR:RHM (alt: XETR:RHM \| CBOE:EUAD) | n=6 (4 bağımsız bölüm): AR0 ort +358 bps (t 3,3), 6/6 pozitif, CAR0–5 +770 bps; tepki gap'te değil gün-içinde (gap +2, intra +420 bps); plasebo p 0,0003 (seçim yanlılığını içermez) | teorik — haber açılıştan önce biliniyorsa; n çok küçük | düzeltildi (S4 DÜZELT DÜŞÜK: olaylar sonradan seçildi) |
| 12 | DÜŞÜK | UL | olay | Barış / savaş başlangıcı haber günleri — barış −, savaş karışık | XETR:RHM (alt: CBOE:VIX) | Ukrayna barış haberleri (n=9) AR0 −85 bps (t −1,9), CAR0–5 +200 (kalıcı değil); savaş başlangıçları AR0 +318 (t 1,4) ama 24.02.2022 −%10,5 taban (AR −302), sonraki 5 günde CAR +1.295 | hayır | doğrulanmadı |
| 13 | DÜŞÜK | UL | gün-içi öncü | Kore savunma sepeti (Hanwha Aero, Hyundai Rotem, LIG, KAI) — + | KRX:012450 (alt: KRX:064350 \| KRX:079550 \| KRX:047810 \| KRX:KOSPI) | lag0→gün-içi t 1,9 (KS11+ES kontrolüyle 1,6); lag0→gap t 4,8 (piyasa geneli); pc 0,04 (IS/OOS 0,05; %81 yıl); BT z>1 OOS +11 bps, Sh 0,33 | hayır | doğrulanmadı |
| 14 | DÜŞÜK | UL | senkron | ABD savunma (LMT, NOC, RTX, GD, LHX, XAR, ITA) ve Elbit — + | AMEX:XAR (alt: NYSE:LMT \| NYSE:NOC \| NYSE:RTX \| NYSE:GD \| NYSE:LHX \| CBOE:ITA \| AMEX:PPA \| NASDAQ:ESLT) | ABD sepeti pc 0,03 (IS 0,01 / OOS 0,09; %88 yıl); ESLT 0,055 (IS 0,01 / OOS 0,10); ITA/XAR/PPA gap_l1 t 2,9–3,9 = ABD eşzamansızlığı (kısmi ~0) | hayır | doğrulanmadı |
| 15 | DÜŞÜK | UL | gap öncü | Gece küresel/Asya sinyalleri (ES, NQ, Nikkei, KOSPI, Brent, altın) → gap — + | CME_MINI:ES1! (alt: CME_MINI:NQ1! \| TVC:NI225 \| KRX:KOSPI \| ICEEUR:BRN1! \| COMEX:GC1! \| FX:USDTRY) | gece ES 0,22 (IS 0,32 / OOS 0,04), NQ 0,24; N225 0,26 (OOS 0,10), KOSPI 0,19; Brent gece 0,15 (IS 0,35 / OOS 0,03); altın gece 0,10; G1: savunma/enerji/kimya 0,22–0,26 en düşükler; ES gece alt pencereleri (15–16 / 16–20 / 20–07 UTC) t 1,3 / 2,7 / 2,1; gece USDTRY → gap −0,15 (IS −0,16 / OOS −0,11; DÜŞÜK); gece TUR 0,10 (IS 0,17 / OOS 0,02), TKC 0,11, EEM 0,05, BTC 0,09, EURTRY −0,05, DAX/STOXX ≈0 (ÇOK DÜŞÜK) | hayır — açılış müzayedesinde fiyatlanır; pay vadelisinin akşam seansı yok | kısmen (G1 KABUL: piyasa faktörü; ASELS'te OOS çökmüş) |
| 16 | DÜŞÜK | UL | rejim | 2026 petrol-şoku rotasyonu (Brent ile pozitif) — + | ICEEUR:BRN1! (alt: TVC:UKOIL) | 2025-11..2026-10 XBANK analizinde ASELS–Brent pc +0,17 (TUPRS +0,45, PETKM +0,40 ile aynı taraf; havayolu/banka negatif) | hayır — tek yıl | düzeltildi (B5 DÜZELT DÜŞÜK: tek petrol-şoku faktörü) |
| 17 | DÜŞÜK | UL | gün-içi öncü | TUR−EEM (Türkiye'ye özgü risk primi) t-1 → gün-içi (ters) — − (ters) | NASDAQ:TUR (alt: formül: NASDAQ:TUR/AMEX:EEM) | TUR−EEM_{t-1}→gün-içi t −3,3 (IS −1,9 / OOS −2,6); TUR_{t-1}→gün-içi −0,08 (t −3,2; FDR geçmez); TUR−EEM senkron pc +0,04 (IS 0,02 / OOS 0,06; DÜŞÜK); TUR−EEM_{t-1}→gap t 2,8 (IS 3,1 / OOS 0,9; işlenemez); ters yön ASELS_{t-1}→TUR t −2,1 (IS −1,2 / OOS −1,45; FDR yok) | hayır | doğrulanmadı (H45 benzeri kanal: rejime bağlı, DÜŞÜK) |
| 18 | DÜŞÜK | Yİ | senkron | Yerli savunma akranları (ALTNY, SDTTR) — + | BIST:ALTNY (alt: BIST:SDTTR) | ALTNY pc 0,26, SDTTR 0,21 (yalnız 2023+; %100 yıl); savunma akran bloğu Shapley payı tam %8,2 → son 1y %19,5; öncülük yok (t ≤0,3) | hayır — senkron; akranlar VİOP'ta yok | doğrulanmadı (kaynak ORTA; brifing tanımı gereği kısa örneklem → DÜŞÜK) |
| 19 | DÜŞÜK | Yİ | mikroyapı | Kendi açılış gap'inin gün içinde dönüşü (gap fade) — − (gap'e ters) | BIST:ASELS1! (alt: BIST:ASELS) | açılış girişi IS 24,9 bps (t 2,2) / OOS 31,9 (t 1,3); yılların %69'u +; h1 ilk-30 dk VWAP girişi 28,0 bps (t 0,8); 10:30 girişi 20,7; 47 testte FDR yok | sınırda — açılış dolumu iyimser, VİOP açılışı spottan 36–46 bps sapıyor | düzeltildi (YG1 DÜZELT DÜŞÜK, K1 DÜZELT DÜŞÜK) |
| 20 | DÜŞÜK | Yİ | senkron | TL faizi (DİBS) ve katılım endeksi — + | TVC:TR05Y (alt: TVC:TR02Y \| TVC:TR01Y \| BIST:XKTUM) | 5y DİBS senkron pc +0,05 (OOS 0,07; 3y 0,14; 1y 0,19; %85 yıl; FDR); 1y/2y DİBS_{t-1}→gap t 2,2–2,6 (işlenemez); XKTUM pc 0,35 (yalnız OOS; ASELS ağırlığı ~%18, mekanik) | hayır | doğrulanmadı |
| 21 | DÜŞÜK | Yİ | senkron | Diebold–Yilmaz ağ merkeziliği ('net alıcı') — − | BIST:XU100 | net spillover −%7,2 (2014–17 −30,1 / 2021–23 +17,9 / 2024–26 −37,2 / son 1y −33,6; B-hizalı −2,5) — son dönemde belirgin net alıcı (en 'yerli' hisselerden) | hayır — yön bilgisi değil | ry_ag kendi yöntem eleştirisi: günlük veride 'yayıcı/alıcı' = korelasyon merkeziliği (H=1 / H=10 Spearman 0,994); yön yorumu DÜŞÜK |
| 22 | ÇOK DÜŞÜK | UL | senkron | Tarama yan bulguları (Arkema, Lufthansa, Richemont, Ferrari, Nu) — − | OTC:ARKAY (alt: XETR:LHA \| SIX:CFR \| NYSE:RACE \| NYSE:NU) | pc −0,07…−0,08 (Arkema −0,084; LHA −0,08, IS −0,03 / OOS −0,115; Richemont −0,08; Ferrari −0,075; Nu −0,07) | hayır | doğrulanmadı (mekanizma yok) |
| 23 | ÇOK DÜŞÜK | UL | hipotez | CSG N.V. (Czechoslovak Group, 2026-01+) — + | EURONEXT:CSG | ~190 gün veri; test edilemez | bilinmiyor | test edilemedi |
| 24 | ÇOK DÜŞÜK | Yİ | hipotez | İhracat sözleşmesi / savunma bütçesi KAP duyuruları — + | BIST:ASELS | olay testi yapılmadı (ihracat teslimat payı 2024 %19 → 2025 %25; 2025'te >2 mlr $ ihracat sözleşmesi) | bilinmiyor | test edilemedi |

## Olumsuz bulgular (test edildi, ilişki yok/çöktü)
- EU savunma sepeti t-1 → ASELS gün-içi: BT OOS Sh −0,52 (t 0,95).
- Avrupa kapanış sonrası (15:00→16:40 UTC) → ertesi gün-içi Sh 0,49 (t 0,8); şok günü ertesi Sh 0,09; saatlik EU savunma → sonraki saat t <1,8.
- Tam panel taraması (13.662 test, BH q 0,05): gün-içi lag1'de FDR'den geçen dış sürücü 0.
- Hakem sektör emsal artığı (19 savunma emsali) → gün-içi: 5,05 bps/σ (t 1,29; q 0,40); VİOP t 1,42.
- USDTRY senkron pc ≈−0,01 (kur-vol rejimleri arasında fark yok); Yahoo USDTRY/EURTRY/sepet_{t-1} → gap t −2,3…−2,6 (IS −4,3…−4,7 / OOS +0,8…+1,8: işaret dönüyor; DÜŞÜK); TKC/TUR gece → gap 0,10–0,11 (OOS −0,03/0,02).
- 5 dk XU030 → ASELS gecikmeli tepki yok (b 0,03); saatlik XU030/THYAO → ASELS yok.
- THYAO ile senkron pc 0,02 (IS 0,13 / OOS −0,08).
- Kapanış müzayedesi → ertesi sabah t −0,16; ilk yarım saat momentum OOS 0,2 bps.
- VİOP baz anomalisi → vadeli gün-içi t −1,16; yabancı akış corr −0,05 (t −1,4).
- OTKAR/SDTTR/ALTNY → ASELS öncülük t ≤1,9; ASELS_{t-1} → THYAO gün-içi t −2,2 (zayıf, PRE −2,9).
- Şanghay aynı gün → gap 0,074 (t 1,6), → gün-içi 0,03 (t 0,9); HSI sabah → kalan gün t ≤1,4; USDCNH 07:00–08:30 −0,02 (t −0,5).
- Gece/gün-içi ayrışması: h1 ort. gap +24,2 / gün-içi +5,0 bps; 8 bps BT IS −16,5 / OOS −8,8 bps (DÜŞÜK, kârsız); gece sürücü sepeti (ES+BZ+GC+TRY+TUR+DAX) 07:30 girişli BT IS −5,1 / OOS −35,6 bps; açıklanamayan gap kalıntısı → ilk 30 dk −0,04 (t −0,7).
- Hisse-hariç XU030/XMESY/XU100_{t-1} → ASELS cc/gap/gün-içi: BH yok (XU100 hisse-hariç → gap OOS t 3,15 ama IS 0,5) — ÇOK DÜŞÜK; savunma akranları açılış gap'i → ASELS gün-içi b 0,07 (t 1,4); THYAO_{t-1}→ASELS gün-içi t 1,6.
- DİBS 10y/1y, TLREF, zımni TL faizi, VİOP USDTRY/EURTRY/sepet, gram altın (Yahoo/VİOP/15:00) senkron pc |≤0,05| (ÇOK DÜŞÜK); BTC hafta sonu → Pazartesi gap 0,05 (t 0,8).
- Saatlik/5 dk yurt içi kaynaklar (AKBNK, GARAN, ISCTR, YKBNK, KCHOL, SAHOL, BIMAS, EREGL, TUPRS, THYAO, XUSIN; 34 satır) → ASELS: Wald FDR'den geçen yok (|t| ≤3,0; ÇOK DÜŞÜK).

## Çin/HK kodları yerine test edilmiş alternatifler
- 000001.SS (Şanghay Bileşik; SSE kodu VERİLMEZ) -> CBOE:CNYA (haftalık r 0,85, YÜKSEK) | AMEX:ASHR (0,84) | AMEX:KBA (0,80)
- ^HSI (Hang Seng) -> TVC:HSI (HKEX'e bağlı olmayan TV akışı; HSI:HSI de var) - açılmazsa AMEX:FXI (haftalık r 0,87) | NASDAQ:MCHI (0,86)
- CNH=X (offshore yuan) -> FX:USDCNH (Çin borsası değil; tv_final alternatifi FX_IDC:USDCNH; onshore vekil FX_IDC:USDCNY, haftalık r 0,75, ORTA)

## Varyans ayrıştırması
Shapley (2014–26, düz. R² 0,37): piyasa %27,5, sektör (OTKAR, SDTTR, ALTNY) %8,2, küresel-8 %1,0, TR makro %0,5, hisseye özgü %62,9. Küresel pay 2024–26 %1,6, son 1y %3,0; küresel pay sırası tam 44., son 1y 37. (en yerli hisselerden); sektör payı son 1y %19,5.

## VİOP likidite / maliyet
BIST:ASELS1! sınıf A: 12 ay medyan günlük hacim 3.428 mn TL (72,1 mn USD), medyan 27.529 işlem, açık pozisyon ~4.928 mn TL; tik 0,05 TL (12 ay medyan 1,4 bps); gidiş-dönüş maliyet küçük emir 6,1 bps, muhafazakâr 8,0, 1 mn TL 11,4, bireysel 22,9 bps; vadeli/spot hacim 0,32; akşam seansı yok.

## Açık sorular
- Savunma haber günlerini açılıştan önce sistematik tanımlamak mümkün mü? (Tepki gap'te değil gün-içinde: +420 bps.)
- 2022 sonrası Avrupa savunma rejimi kalıcı mı; barış süreci bağı tersine çevirir mi?
- Şirkete özgü KAP ihracat duyurularının olay çalışması yapılmadı.

## TradingView izleme listesi
```
BIST:ASELS, BIST:ASELS1!, XETR:RHM, LSE:BA., MIL:LDO, EURONEXT:HO, OMXSTO:SAAB_B, OSL:KOG, XETR:HAG, CBOE:EUAD, AMEX:XAR, KRX:012450, BIST:OTKAR, BIST:ALTNY, BIST:SDTTR, BIST:XUTEK, BIST:XBANK, BIST:XU100, BIST:XU030D1!, NASDAQ:TUR, NASDAQ:EMB, CME_MINI:ES1!, CBOE:VIX, ICEEUR:BRN1!, TVC:TR05Y, TVC:SXXP
```

Kısaltmalar: UL = uluslararası, Yİ = yurt içi; pc = XU100 kontrollü kısmi korelasyon; IS 2014–20 (aksi yazılmadıkça), OOS 2021–26; bps = baz puan. Güven: brifing ölçeği; doğrulama varsa doğrulayıcı etiketi.
