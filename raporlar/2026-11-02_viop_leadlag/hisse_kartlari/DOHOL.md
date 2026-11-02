# DOHOL — Doğan Şirketler Grubu Holding A.Ş.

Spot: `BIST:DOHOL` · VİOP pay vadelisi: `BIST:DOHOL1!` · Sektör: Holding (NAV'ın ~%45'i nakit/USD; GWIND %70; halka açık olmayan iştirakler; Ditaş 2025'te satıldı)

## Özet
DOHOL dış sürücülerden en az etkilenen VİOP holdinglerinden: küresel blok varyans payı %1,2 (özgün ≈0), hisseye özgü pay %66 (2014–17 %84 → 2021–23 %50; piyasaya entegrasyonu arttı). Doğrulama turu XU100 ve USDTRY dışında sağlam bir küresel sürücüsü olmadığını teyit etti (max |pc| ≤0,10; YÜKSEK olumsuz bulgu). XU100 ötesindeki en net yurt içi bağ ölçek faktörü (hisse-hariç XU030 −0,17, XYUZO +0,14; yılların %100'ü); iştirak GWIND ile bağ yok (pc 0,04). USD nakit ağırlığına rağmen günlük kur bağı zayıf ve pozitif (pc +0,04–0,06) ve 2025-03 sonrası −0,12'ye döndü. En güçlü istatistik kendi açılış gap'inin gün içinde geri dönmesi (IS 51 bps, t 6,4; OOS 26 bps, t 1,4) ama vadeli C sınıfı ve gecikmeli girişte etki yarıya iniyor: işlem DÜŞÜK.

**Varyans ayrıştırması:** Tam dönem: R² %34; hisseye özgü %66; BIST piyasası %18; holding kümesi %14; küresel blok %1,2 (son 1y %4,8; özgün −%0,1); TR makro %0,2. Dönemler: hisseye özgü pay 2014–17 %84, 2018–20 %76, 2021–23 %50, 2024–26 %55. XU100 corr 0,54 (IS 0,38 / OOS 0,69), beta 0,88 (OOS 1,06). Diebold–Yilmaz net alıcı (−0,06).

**VİOP likidite/maliyet:** BIST:DOHOL1! sınıf C (47 içinde en illikitlerden): 12 ay medyan günlük hacim 200 mn TL (4,4 mn USD), medyan 7.673 işlem; tik 0,01 TL ≈4,8 bps (son fiyatta 6,3 bps); gidiş-dönüş maliyet küçük emir 9,0 bps, muhafazakâr 11,4 bps, 1 mn TL 25,1 bps, bireysel 25,8 bps; vadeli/spot hacim 0,84; ilk işlem 2018-12. 2015–20'de fiyat 0,6–1 TL, tik %1–1,7: o dönemin saatlik/gün-içi bulgularında fiyat adımı etkisi büyük.

## Sürücüler (güven sırasıyla)

| # | Sürücü | TradingView | Kapsam | İlişki | Rakamlar | Yön | İşlenebilirlik | Güven | Doğrulama |
|---|---|---|---|---|---|---|---|---|---|
| 1 | TUR (MSCI Türkiye ETF) + EMB gece | NASDAQ:TUR (alt: NASDAQ:EMB) | uluslararası | gap öncü | TUR gece → gap corr 0,33 (1y 0,36; IS 0,30 / OOS 0,37; gün-içi t 1,2); Yahoo TUR_t−1 → gap t 3,4 (IS 2,4 / OOS 2,8; FDR); TUR_t−1 → gün-içi t −2,1 (IS −0,9 / OOS −2,3; FDR yok); EMB_t−1 → gap t 4,4 (IS 3,5 / OOS 3,0). Faktör kontrolünde TUR kısmi 0,07 (t 2,1): ortak faktör. Senkron pc TUR −0,03, EMB −0,02 | + (gap) / − (gün-içi, zayıf) | hayır (gap; eşzamansız kapanış) | YÜKSEK | doğrulandı, kısmen (B1 TUR→banka gap KABUL; y_ag: DOHOL'de yalnız ortak faktör) |
| 2 | Ölçek faktörü (XU030 / XYUZO, hisse-hariç) | BIST:XYUZO (alt: BIST:XU030 / BIST:XTUMY / BIST:XUTUM) | yurt içi | senkron | Hisse-hariç XU030 kısmi −0,17 (IS −0,23 / OOS −0,15; yılların %100'ü); hisse-hariç XYUZO +0,14 (IS 0,16 / OOS 0,11; %100); XTUMY kısmi 0,14. XU100 corr 0,54; İki faktörlü ham kısmi (y_endeks YÜKSEK etiketlerinin kaynağı): XUTUM +0,09 (t 5,0; ham corr 0,54; mekanik içerme), XTUMY +0,14 (t 7,4), XYUZO +0,17 (t 9,0), XU030 −0,14 (t −8,1); XYLDZ (Yıldız Pazar) +0,06 (t 3,0; DÜŞÜK), XUMAL ≈0 (DÜŞÜK) | + orta ölçek / − büyük ölçek | hayır (senkron) | YÜKSEK | doğrulanmadı (y_endeks) |
| 3 | VİOP baz anomalisi → ertesi spot gap | BIST:DOHOL1! (alt: BIST:DOHOL) | yurt içi | mikroyapı | Baz anomalisi_t → spot gap_t+1 10,6 bps/σ (t 4,4; IS 2,5 / OOS 3,8; FDR geçti); → vadeli gün-içi_t+1 −12,0 bps/σ (t −1,6; IS −2,3 / OOS −0,3) | + | hayır (spot gap işlenemez; vadeli gün-içi tutarsız) | YÜKSEK | doğrulanmadı |
| 4 | VİOP 09:30 açılışı → spot açılış gap'i | BIST:DOHOL1! | yurt içi | mikroyapı | corr 0,58 (b 0,63; R² 0,34); spot gün-içi kalıntı yok | + | hayır | YÜKSEK | doğrulanmadı |
| 5 | ABD vadelileri ES/NQ + EEM gece | CME_MINI:ES1! (alt: CME_MINI:NQ1! / AMEX:EEM) | uluslararası | gap öncü | ES gece → gap corr 0,35 (1y 0,35; IS 0,38 / OOS 0,31; gün-içi t 1,5); EEM 0,19 (gün-içi t 1,4); NQ faktör kontrolünde 0,03 (OOS t 0,6); ES 07:00–08:30 → BIST ilk 1,5 saat 0,05 (t 1,3) | + | hayır (açılışta fiyatlanıyor) | ORTA | doğrulandı (genel mekanizma: 1. tur ana bulgusu KABUL/YÜKSEK; hisse düzeyinde ajan etiketi ORTA korunuyor; y_ag: yalnız ortak faktör) |
| 6 | Asya kapanışları: Nikkei, KOSPI, Şanghay (aynı gün) | TVC:NI225 (alt: KRX:KOSPI / CBOE:CNYA (Şanghay yerine; Çin kodu verilmez) / AMEX:ASHR) | uluslararası | gap öncü | Nikkei → gap corr 0,34 (t 3,8; IS 0,40 / OOS 0,28); tam faktör kontrolünde kısmi 0,17 (t 6,4); Şanghay Bileşik 0,14 (t 6,9; OOS tutarlı); KOSPI → gap corr 0,24 (t 2,9; IS 0,38 / OOS 0,22; DÜŞÜK); KOSPI → gün-içi 0,01, Nikkei → gün-içi −0,01 (ÇOK DÜŞÜK) | + | hayır | ORTA | doğrulanmadı (y_ag: A1 ayakta) |
| 7 | XHOLD (Holding endeksi, hisse-hariç) | BIST:XHOLD (alt: BIST:KCHOL / BIST:SAHOL) | yurt içi | senkron | Ham kısmi 0,18 (t 8,0); hisse-hariç kısmi 0,09 (IS 0,02 / OOS 0,17; %69 yıl); holding akran sepeti (KCHOL, SAHOL, ALARK, AGHOL, GLYHO) Shapley %14 (2021–23 %22), özgün pay %0,9 | + | hayır | ORTA | doğrulanmadı |
| 8 | KAREL | BIST:KAREL | yurt içi | senkron | pc 0,097 (t 5,3); IS 0,13 / OOS 0,08; %88 yıl; tarama FDR geçti | + | hayır | ORTA | doğrulanmadı |
| 9 | Kendi açılış gap'i (/gap/>%1) → gün-içi dönüş | BIST:DOHOL (alt: BIST:DOHOL1!) | yurt içi | mikroyapı | IS 2014–20 +50,9 bps (t 6,4) / OOS 2021–26 +25,8 bps (t 1,4); %69 yıl +; 47 testte BH-FDR evet; h1 2023-12+: açılış girişi 46,2, ilk 30 dk VWAP vekili 20,0 (t 1,1), 07:30 UTC girişi 8,8 bps. Gap kalıntısı → ilk 30 dk corr −0,18 (t −2,2), 07:30 sonrası −0,08. İstatistik ORTA / işlem DÜŞÜK | − (gap tersine) | sınırda/hayır: açılış müzayedesi derinliği sığ, gecikmeli girişte getiri yarıya iniyor; vadeli C sınıfı (1 mn TL emirde 25 bps) | ORTA | düzeltildi (Kendi gap fade: ilişki ORTA, işlem DÜŞÜK–ORTA; v3 temizliği IS'i şişirmişti; YG1: DOHOL tam dönem FDR geçen 6 hisseden biri, OOS'ta değil) |
| 10 | BIST Katılım Sürdürülebilirlik (XSRDK) | BIST:XSRDK | yurt içi | senkron | Ham kısmi 0,087 (t 2,6; ham corr 0,69; DOHOL ağırlığı ≈0 → hisse-hariç 0,09, OOS 0,09, yılların %100'ü); yalnız OOS (endeks ~2021+, n 1.239) | + | hayır (senkron) | ORTA | doğrulanmadı (ajan ORTA; IS verisi yok) |
| 11 | USDTRY gece hareketi → açılış gap'i | FX:USDTRY (alt: FX:EURTRY) | yurt içi | gap öncü | Saatlik gece USDTRY (15:00→06:00 UTC) → gap corr −0,16 (t −3,3; 1. yarı −2,0 / 2. yarı −3,4, bölünme 2025-06; XU100 gap kontrollü −1,8); EURTRY gece → gap 0,10 (t 1,7; ÇOK DÜŞÜK) | − | hayır: açılış gap'inde fiyatlanıyor (pay vadelisinde akşam seansı yok) | ORTA | doğrulanmadı (ajan 'ORTA (işlenemez)') |
| 12 | Brent gece | ICEEUR:BRN1! (alt: TVC:UKOIL) | uluslararası | gap öncü | Brent gece → gap corr −0,19 (1y −0,36; IS −0,03 / OOS −0,32) | − (2025+) | hayır | DÜŞÜK | düzeltildi (B5: 2026 petrol şoku tek ortak faktör) |
| 13 | Bitcoin gece | BITSTAMP:BTCUSD (alt: COINBASE:BTCUSD) | uluslararası | gap öncü | BTC gece → gap corr 0,25 (IS 0,30 / OOS 0,21; gün-içi t 2,1); faktör kontrolünde 0,00 (t 0,1) | + | hayır | DÜŞÜK | düzeltildi (y_ag: B3 gürültü; r1 ORTA → kartta DÜŞÜK) |
| 14 | Tarama sürprizleri (negatif pc): Peabody, bakır, Nedbank | NYSE:BTU (alt: COMEX:HG1! / JSE:NED) | uluslararası | senkron | BTU pc −0,063 (IS −0,07 / OOS −0,05; %80 yıl), HG=F −0,057 (IS −0,04 / OOS −0,06; %85), NED.JO −0,057 (OOS 0,005); CPNG −0,063, ANA (9202.T) −0,053 (ÇOK DÜŞÜK); BH q 0,08–0,49 | − | hayır | DÜŞÜK | doğrulandı (olumsuz: TR3 – XU100+USDTRY dışında max /pc/ ≤0,10, FDR+replikasyon yok) |
| 15 | USDTRY (kur) senkron | FX:USDTRY (alt: BIST:USDTRY1!) | yurt içi | senkron | pc: Yahoo +0,057 (IS 0,01 / OOS 0,06; FDR), r1 +0,043 (OOS 0,064), VİOP USDTRY +0,049 (3y −0,01, 1y −0,17), doğrulama taraması +0,059; sepet kur +0,047 (t 2,0; IS −0,00 / OOS 0,06; DÜŞÜK), EURTRY +0,04 (ÇOK DÜŞÜK); 2025-03 sonrası −0,12. Haftalık USD bazlı beta −0,20 (t −1,5); çeyreklik XU100'e göreli kur geçişkenliği −0,37 (TL riski). Gece kur → gap ayrı satırda | + (zayıf, tam dönem) / − (son 1y ve çeyreklik) | hayır | DÜŞÜK | doğrulandı, kısmen (TR3/v_cin_gunici_olay_tarama: DOHOL–USDTRY pc +0,059) |
| 16 | TL faizi: DİBS 5y/10y (pozitif) | TVC:TR05Y (alt: TVC:TR10Y) | yurt içi | senkron | pc DİBS 5y +0,052 (IS 0,03 / OOS 0,07; %85 yıl; FDR), 10y +0,045 (%69 yıl; FDR); DİBS 1y_t−1 → gap t 2,5 (IS 1,7 / OOS 1,95) | + (faiz ↑ günlerinde DOHOL piyasadan iyi) | hayır | DÜŞÜK | doğrulanmadı |
| 17 | Gram altın / ons altın | FX_IDC:XAUTRYG (alt: COMEX:GC1!) | yurt içi | senkron | Gram altın 15:00 hizalı (2024-06+) pc 0,053 (1y 0,08); altın gece → gap corr 0,10 (IS −0,03 / OOS 0,20; gün-içi t 1,9). Ons altın senkron pc −0,009 | + (zayıf) | hayır | DÜŞÜK | doğrulanmadı |
| 18 | Saatlik/5 dk endeks → DOHOL (XHOLD, XU030, XUSIN, XBANK) | BIST:XHOLD (alt: BIST:XU030 / BIST:XUSIN) | yurt içi | mikroyapı | h1 (İş Yatırım 2017–26): XHOLD Σβ_lag1..3 0,25 (t 6,8; IS 0,31 t 4,5 / OOS 0,13 t 3,1), XU030 0,24 (t 6,1; OOS t 2,2), XUSIN 0,29 (t 6,5; OOS t 1,8); 5 dk (60 gün): XBANK t 3,0, XUSIN t 3,7. Ters yön de anlamlı (t 4,5); IS'te DOHOL fiyatı 0,6–1 TL (tik %1–1,7), 2016'da günlerin %56'sında açılış = önceki kapanış; İstatistik YÜKSEK/ORTA (ajan: XHOLD ve XU030 h1 YÜKSEK, XUSIN ORTA; bayat fiyat şüphesi) / işlem DÜŞÜK | + | hayır: fiyat adımı/bayat fiyat kaynaklı, maliyeti karşılamaz | DÜŞÜK | doğrudan test edilmedi (v_wf4 genel sorunlar 'PLAUSIBLE': büyük ölçüde fiyat ayrıklığı/bayat fiyat; işlem için DÜŞÜK önerildi) |
| 19 | Holding akranlarının açılış gap'i → DOHOL gün-içi | BIST:KCHOL (alt: BIST:SAHOL / BIST:ALARK) | yurt içi | mikroyapı | Akran (KCHOL, SAHOL, ALARK, TKFEN, ENKAI) gap → DOHOL gün-içi b 0,195 (t 1,8; 2021+ 0,21 t 0,9); h1 O→07:30 b 0,21 (t 2,3), 07:30→kapanış −0,02; kendi gap b −0,27 (t −5,5) | + | hayır (ilk 30 dakikada tükeniyor) | DÜŞÜK | doğrulanmadı |
| 20 | Kapanış müzayedesi hareketi (CA) → ertesi sabah | BIST:DOHOL | yurt içi | mikroyapı | gap_t+1 b −0,25 (t −1,4; IS −0,53 / OOS −0,03); O→07:30_t+1 b −0,54 (t −2,3) | − | hayır (VİOP'ta uygulanamaz) | DÜŞÜK | düzeltildi (YG2: ilişki ORTA, VİOP'ta net kâr DÜŞÜK) |
| 21 | Yabancı akış (TCMB haftalık) | ? (TCMB EVDS; TV kodu yok) (alt: BIST:XU030) | yurt içi | senkron | Akış_w ~ DOHOL fazla getirisi corr −0,106 (t −2,7; FDR geçti); yayın sonrası 5 gün IS 0,00 / OOS 0,05 (FDR yok) | − (yabancı alımında DOHOL göreli zayıf) | hayır | DÜŞÜK | doğrulanmadı |
| 22 | İştirak DITAS (2025'te satıldı) | BIST:DITAS | yurt içi | senkron | pc 0,075 (t 4,0); IS 0,11 / OOS 0,03; %88 yıl | + | hayır | DÜŞÜK | doğrulanmadı (ajan ORTA; %68,24 pay 2025'te satıldığı için güncel kullanım DÜŞÜK) |
| 23 | TKFEN | BIST:TKFEN | yurt içi | senkron | pc 0,056 (IS −0,01 / OOS 0,12; yıllık işaret %69) | + | hayır | DÜŞÜK | doğrulanmadı |
| 24 | DOHOL_t−1 → kur/altın/TUR (ters yön) | FX:USDTRY (alt: BIST:XAUTRY1!) | yurt içi | ters yön | DOHOL_t−1 → sepet kur (15:00) t 2,6 (OOS); → VİOP gram altın t 2,4 (IS 1,9 / OOS 1,5); → zımni faiz t 2,0; → TUR t −2,1; 1.071 ters testte 0 FDR | karışık | hayır | DÜŞÜK | doğrulanmadı |
| 25 | Gece/gün-içi ayrışması (gap>0, gün-içi<0) | BIST:DOHOL | yurt içi | rejim | h1 döneminde ort. gap +13,9 bps, gün-içi −10,5 bps; BT IS +6,7 / OOS −2,5 bps | gap +, gün-içi − | hayır | DÜŞÜK | düzeltildi (TL taşıma maliyeti; net ≈0) |
| 26 | USD nakit NAV'ı ve halka açık olmayan iştirakler | ? (veri yok) | yurt içi | hipotez | NAV'ın ~%45'i USD nakit: USD bazında 'dolar hissesi' davranışı beklenir; günlük/haftalık veride görülmedi (haftalık USD beta −0,20). Hepiyi, Doğan Trend vb. halka açık olmadığı için test edilemedi; seviye/eşbütünleşme ve NAV iskontosu seviye testi yapılmadı | ? | hayır | ÇOK DÜŞÜK | doğrulanmadı (test edilemedi) |

## Test edilip ilişki bulunmayanlar (olumsuzlar)
- Doğrulama (TR3, YÜKSEK): XU100 ve USDTRY dışında, TR aynaları (TKC/TUR/ADR) hariç sağlam küresel sürücü yok: 992 sürücü × 2 gecikme, max |pc| ≤0,10, FDR+replikasyon geçen yok.
- Altın (GC=F) pc −0,009, gümüş ve BTC senkron pc ≈0 (f_holding).
- İştirak GWIND ile pc 0,04 (t 1,5; %67 yıl); GWIND gap ayrışması → DOHOL gün-içi OOS +4,9 bps (t 0,3), 15 bps'te −2,1.
- İştirak sepeti açılış ayrışması sinyali DOHOL'de hiç yok (ry_grup).
- Hakem: DOHOL yabancı emsal sepeti (GDX, ICLN) → hedge'li gün-içi 3,8 bps/σ (t 1,1), VİOP −0,8 (t −0,2); net 16 bps OOS −9,8 bps.
- TLREF pc 0,01; zımni TL faizi −0,02; DİBS 1y/2y pc 0,02–0,03 (ÇOK DÜŞÜK); EMB/TUR/TUR−EEM senkron pc −0,03…0,00.
- Gece sürücü sepeti → 07:30 sonrası gün-içi devam: IS +2,5 / OOS +3,1 bps (t 1,4).
- ES 07:00–08:30 UTC → BIST ilk 1,5 saat corr 0,05 (t 1,3).
- İlk yarım saat → son 30 dk momentumu: b −0,03 (OOS −0,08, t −2,0); 47 hissede 0 FDR.
- 5 dk ve saatlik hisse/endeks öncülüğü (y_gunici_y): 741 ileri + 741 ters testte 0 FDR; ES/NQ/Brent/USDTRY 5 dk'da işlenebilir gecikme yok.
- Günlük endeks_t−1 → DOHOL gün-içi: 12.726 testte gün-içi 0 FDR.
- TKFEN_t−1 → DOHOL gün-içi t −0,3 (f_y_hisse).
- DAX ve STOXX600 gece → gap corr 0,05 (t 1,2–1,5; ÇOK DÜŞÜK); Hang Seng (gün, açılış öncesi ve 07:30→kapanış) → DOHOL gün-içi |t| ≤1,9 (ÇOK DÜŞÜK); USD/CNH 07:00–08:30 ≈0.
- 5 dk ve 60 dk: GARAN, AKBNK, YKBNK, ISCTR, THYAO, ASELS, TUPRS, EREGL, BIMAS ve XLBNK → DOHOL |t| ≤2,2 (ÇOK DÜŞÜK); tek uç BIMAS 60 dk t −3,9 (IS −3,3 / OOS −2,2; FDR yok); XLBNK m5 t 3,0 (kriz öncesi Σβ 0,22 / fon krizi 0,07), h1 t 0,3.

## Çin/HK kodları yerine test edilmiş alternatifler
- Şanghay Bileşik (gap sürücüsü; SSE kodu verilmez): CBOE:CNYA (haftalık r 0,86), AMEX:ASHR (0,84), AMEX:KBA (0,80); ABD seansında işlem gördükleri için zaman hizası farklı.

## Açık sorular
- USD nakit ağırlıklı NAV'a rağmen günlük kur bağının yokluğu: aylık/çeyreklik NAV iskontosu seviye serisiyle (eşbütünleşme) test edilmeli.
- Kendi gap fade etkisi DOHOL vadelisinin (C sınıfı) açılış seansı derinliğinde uygulanabilir mi? Gerçek VİOP açılış/VWAP fiyatıyla backtest yapılmadı.

## TradingView izleme listesi

```
BIST:DOHOL,BIST:DOHOL1!,BIST:XU100,BIST:XU030,BIST:XYUZO,BIST:XTUMY,BIST:XHOLD,BIST:KCHOL,BIST:SAHOL,BIST:KAREL,BIST:GWIND,NASDAQ:TUR,NASDAQ:EMB,CME_MINI:ES1!,AMEX:EEM,TVC:NI225,CBOE:CNYA,FX:USDTRY,BIST:USDTRY1!,TVC:TR05Y,FX_IDC:XAUTRYG,ICEEUR:BRN1!,BITSTAMP:BTCUSD,BIST:XSRDK,KRX:KOSPI
```
