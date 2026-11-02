# ry_ag — Ağ, spillover ve rejim: yurt içi + uluslararası sürücüler tek çerçevede (47 VİOP hissesi)
Ajan: ag · Veri: panel_ret_bistcal (FX_FIX + simetrik ±%10,5 temizliği), panel_decomp_bist, saatlik 15:00 UTC anlık fiyatlar (2024-06+) · Dönem 02.01.2014–30.10.2026 · Kod: `out/code_y_ag/`

## 0. Net bulgular

| # | Bulgu | Rakam | Güven |
|---|---|---|---|
| 1 | **Bir VİOP hissesinin günlük varyansının küresel faktörlere düşen payı küçük, yerli payı büyük.** Medyan hissede 12 yıllık dönemde Shapley payları: küresel %1,9, TR makro %0,4, XU100 %20,2, sektör/küme %19,7, hisseye özgü %58,2 | Küresel blok tek başına (üst sınır) %5,1; XU100+sektör+TR kontrolünden sonra özgün payı (alt sınır) %0,1. Küresel etki neredeyse tamamen XU100 üzerinden geçiyor | YÜKSEK |
| 2 | **Türkiye'nin küresel bağı rejime bağlı**: XU100 varyansında küresel pay %15 (2014–17) → %22 (2018–20) → **%5,5 (2021–23)** → %11 (2024–26) → %20 (son 1y) → %24 (2026 Oca–Ağu) | Hisse medyanı: %3,0 → %3,8 → **%0,6** → %2,3 → %4,8. 2021–23'te sektör payı %13'ten %26'ya çıktı (hisseler 'yerlileşti') | YÜKSEK |
| 3 | En küresel hisseler (2024–26 / son 1y): TUPRS, GUBRF, TAVHL, PGSUS, THYAO, TRALT, TRMET, SISE, PETKM; en yerli: SASA, ULKER, BRSAN, ALARK, ENJSA, VESTL, ASTOR, AKSEN | Küresel Shapley 2024–26: TUPRS %6,5 … SASA %0,5; son 1y: GUBRF %17, TAVHL %15, PETKM %14,5, TUPRS %13. Son 1 yıl **petrol rejimi**: Brent–XU100 r=−0,26 (petrol sektörlerini ayırıyor) | YÜKSEK (sıralama) / ORTA (son 1y) |
| 4 | **Günlük USD/TRY kapanışı (24:00 UTC) TR makro kanalını olduğundan küçük gösteriyor.** 15:00 UTC senkron kurla (2024-06+) XU100 varyansında TR makro payı %0,4 → %6,4; hisse medyanı %0,1 → %1,2 (tek başına %0,3 → %3,4) | Küresel pay ise değişmiyor (%2,7 → %2,6): Dimson t-1 terimi ABD eşzamansızlığını yakalıyor, kur gürültüsünü yakalamıyor | ORTA (2,4 yıllık pencere) |
| 5 | **Diebold–Yilmaz 'net yayıcı/alıcı' sıralaması günlük veride yön değil, korelasyon merkeziliği.** H=1 (salt eşzamanlı) ile H=10 net sıralaması Spearman 0,994; korelasyon merkeziliği ile 0,90 | Net yayıcılar: XU100, SAHOL, KCHOL, AKBNK, ISCTR, YKBNK, THYAO, GARAN, SISE; alıcılar: SASA, BRSAN, BIMAS, AEFES, HEKTS, ENKAI, TKFEN, TRALT | YÜKSEK (yöntem eleştirisi) / DÜŞÜK (yön yorumu) |
| 6 | **Hizalama yönü tersine çeviriyor.** XU100+10 sürücü ağında: A (ham) ES net +15, XU100 −9; B (ABD t+1 hizalı) ES −17, XU100 **+60**; C (gerçek senkron 15:00 UTC, 2024-06+) ES +8,7, XU100 −4,1 → doğruya A yakın, B sahte 'BIST önde' üretiyor | XU100 FEV'sinin ES'ten gelen payı C %8,1 / A %5,2 / B %1,4; USDTRY'den C %6,1 / A %0,8 | YÜKSEK |
| 7 | **Kriz türüne göre spillover zıt yönde hareket ediyor.** Küresel krizlerde BIST'in küresel sürücülerden aldığı pay artıyor (2015 Çin 27→44, COVID 50→55, Ağu 2024 33→41; 60g pencere), yerel krizlerde düşüyor ve BIST-içi bağ artıyor (2016 darbe 47→31, KKM 32→11, Mar 2025 36→18, **fon krizi 47→27**) | Sektör-portföy ağında BIST-içi blok payı KKM 86→93, fon krizi 77→81. İstisna 2018 kur krizi (22→38; dolar/ABD yaptırımı kaynaklı) | ORTA |
| 8 | **Granger ağı = eşzamansızlık ağı.** Kapanış-kapanış hedefte FDR'den geçen 31 kenarın 26'sı BIST kapanışından sonra kapanan sürücü (VIX 16, EEM 8, ES 1, altın 1); gap hedefinde 202 (TUR 47, VIX 47, ES 28, EEM 27, USDTRY 16); **gün-içi (işlenebilir) hedefte 0** (p=2'de 6). ABD sürücülerini t+1 hizalayınca (yani ABD t−2) 0 | Kaydırılmış-kaynak null'da 0–1 geçiş; dış gap kenarlarının IS→OOS replikasyonu %63, yurt içi kenarlarınki %2–8 (null ≈%2,5); yurt içi out-degree sıralaması IS/OOS Spearman −0,46 | YÜKSEK (olumsuz) |
| 9 | **Kriz anı korelasyon artışı 'bulaşma' değil, volatilite etkisi.** XU100 ile korelasyon her krizde artıyor (COVID 0,54→0,74; KKM 0,59→0,74; Mar 2025 0,60→0,82; ham testte hisselerin %30–50'si anlamlı), Forbes–Rigobon düzeltmesiyle %0–19'a iniyor. ES_{t-1} ile COVID'de değişim yok (kaynak vol 6×) | Fon krizi: XU100 korelasyonu 0,61→0,68 (FR 0,60), ES_{t-1} 0,09→0,04, USDTRY ≈0 → yerel, küresel bağı olmayan şok | YÜKSEK (bulaşma yok) |
| 10 | **USD/TRY–hisse bağı 2022'den beri kopuk.** DCC ortalaması −0,17…−0,21 (2014–2020) → −0,09 (2022) → −0,02 (2023) → −0,06/−0,08 (2024–26). USDTRY_{t-1} → gün-içi öncülüğü (SISE, PETKM, THYAO, VESTL; IS q<0,05) OOS'ta tamamen kayboldu | Yönetilen kur/KKM rejimi kur kanalını susturdu | YÜKSEK |
| 11 | **Sektör ajanlarının iddialarının yaklaşık yarısı ortak faktör.** 3.276 test edilebilir iddia satırında: %49 sadece ortak faktör, %26 zaten gürültü, %4 OOS'ta tutmuyor; ayakta kalan: hisseye özgü dış bağ %14, yerli küme %3, emtia/kur faktörüne özgün maruziyet %2 | YÜKSEK etiketli 262 iddianın 116'sı (%44) ortak faktör (çoğu NQ=F/ES=F/TUR→gap, banka ADR/ETF, metal emsalleri); ayakta kalanlar: havayolu, rafineri, çelik, savunma emsalleri + altın/Brent + yerli kümeler | YÜKSEK (sınıflama) |
| 12 | Yurt içi 'lider' adayı THYAO: 2021–26'da THYAO_{t-1} (XU100 lag kontrollü) 46/46 hedefin ertesi gün gün-içi getirisini pozitif öngörüyor; ama yalnız 2021–23 (XU100 intra hedefinde t=3,95), 2024–26 t=0,3; FDR'den geçmiyor | Tek piyasa-zamanlama faktörü gibi (hedefler bağımsız değil) | DÜŞÜK |

**Bunun 'öngörü' değil 'öngörü gücü testi' olduğunu vurguluyorum:** Granger ve DY sonuçlarının hiçbiri strateji değildir; işlenebilirlik için 1. tur tarama ajanının backtest'lerine bakınız (gün-içi öncülük OOS'ta maliyet sonrası negatif).

## 1. Varyans ayrıştırması (soru 1)

**Model.** r_hisse,t = α + Σ_küresel (b·f_t + c·f_{t−1}) + [USDTRY_t, USDTRY_{t−1}, TUR_{t−1}] + d·XU100_t + e·Sektör_t + ε.
- Küresel (16 regresör): ES=F, EEM, ^STOXX50E, ^VIX, DX-Y.NYB, BZ=F, GC=F, ^TNX, her biri t ve t−1 (Dimson: ABD kapanışı BIST'ten sonra olduğu için t−1 terimi BIST açılış gap'ini yakalar).
- TR makro: USDTRY (FX_FIX'li, UTC günü) t ve t−1 + TUR_{t−1} (NY'de BIST kapanışı sonrası fiyatlanan Türkiye riski). TUR_t KULLANILMADI: BIST seansını içerdiği için piyasa faktörünün aynası.
- Piyasa: XU100_t. Sektör: hisse HARİÇ küme akranlarının eşit ağırlıklı ortalaması (20 küme; mekanik içerme yok). SISE için net akran yok → XUSIN (SISE'yi içerir).
- Değer fonksiyonu: düzeltilmiş R² (16 küresel regresörün aşırı uyumunu cezalandırır). Shapley = genel dominans (4 grubun 24 sırası ortalaması). Ayrıca tek başına (üst sınır), özgün (alt sınır), sabit sıra (küresel→TR→piyasa→sektör) ve faktör-blok düzeyinde 12 bloklu Shapley.
- Sağlamlık: (i) piyasa = diğer 46 VİOP hissesinin EW ortalaması (mekanik içerme yok), (ii) TR = yalnız kur, (iii) küresel yalnız t (Dimson yok), (iv) 15:00 UTC senkron sürücüler (2024-06+), (v) fon krizi için kompakt model (9 regresör, n=43).

**Medyan hisse (47), Shapley payları (%)** — sütunlar: düzeltilmiş R², küresel, TR makro, piyasa, sektör, hisseye özgü, küresel tek başına, küresel özgün:

| period | r2_full_adj | sh_global | sh_trmakro | sh_piyasa | sh_sektor | idio | alone_global | uniq_global |
|---|---|---|---|---|---|---|---|---|
| 2014-17 | 35.8 | 3.0 | 1.8 | 18.8 | 12.8 | 64.2 | 7.7 | 0.2 |
| 2018-20 | 35.7 | 3.8 | 1.2 | 14.8 | 13.5 | 64.3 | 8.7 | 0.5 |
| 2021-23 | 51.3 | 0.6 | 0.2 | 23.3 | 25.5 | 48.7 | 2.1 | -0.1 |
| 2024-26 | 45.4 | 2.3 | 0.3 | 21.7 | 20.0 | 54.6 | 6.4 | 0.2 |
| son1y | 48.1 | 4.8 | -0.0 | 21.1 | 19.3 | 51.9 | 11.8 | 0.8 |
| tam | 41.8 | 1.9 | 0.4 | 20.2 | 19.7 | 58.2 | 5.1 | 0.1 |

Yorum:
- Tam dönem payları alt dönem ortalamalarından küçük (küresel %1,9 vs alt dönemlerde %0,6–4,8): betalar rejimden rejime değiştiği için sabit katsayılı 12 yıllık model daha az açıklıyor. Dönem bazlı rakamlar esas alınmalı.
- 2021–23 'yerlileşme' dönemi: küresel pay %0,6'ya, TR makro %0,2'ye düştü; buna karşın sektör payı %25,5'e, toplam sistematik R² %51'e çıktı → hisseler birbirleriyle çok, dünyayla az birlikte hareket etti (KKM, negatif reel faiz, yurt içi yatırımcı akımı).
- Sağlamlık: piyasa vekili EW-46 ile piyasa payı medyanı %20,1 (XU100 ile %20,2) → XU100'ün hisseyi içermesi medyanda sorun değil (ağır siklet hisselerde birkaç puan şişirme olabilir). Yalnız-kur TR modeli payları ≤0,1 puan değiştiriyor; Dimson t−1 terimi çıkarılınca küresel pay 0,3–1,0 puan düşüyor (ABD kapanış eşzamansızlığının payı).
- **Senkron kontrol (2024-06-12..2026-10-30, EEM/TUR hariç):** günlük kapanışlı (A) vs 15:00 UTC anlık (C): hisse medyanı küresel %2,7 → %2,6, TR makro %0,1 → %1,2 (tek başına %0,3 → %3,4); XU100: küresel %11,0 → %10,6, TR makro %0,4 → **%6,4**. Sonuç: küresel paylar sağlam, TR makro payı günlük veride sistematik olarak düşük ölçülüyor.

**XU100'ün kendisi (küresel + TR makro, %):**

| period | n | r2_full_adj | sh_global | sh_trmakro | alone_global | alone_trmakro |
|---|---|---|---|---|---|---|
| 2014-17 | 1007 | 27.9 | 15.2 | 12.7 | 19.7 | 17.2 |
| 2018-20 | 742 | 30.5 | 22.0 | 8.5 | 24.8 | 11.2 |
| 2021-23 | 743 | 5.3 | 5.5 | -0.2 | 5.5 | -0.1 |
| 2024-26 | 704 | 11.7 | 10.8 | 0.9 | 11.2 | 1.3 |
| son1y | 250 | 19.8 | 20.1 | -0.3 | 20.6 | 0.2 |
| 2026oca-agu | 164 | 24.1 | 24.3 | -0.3 | 24.5 | -0.1 |
| fonkrizi | 43 | 8.3 | 14.3 | -6.0 | 14.3 | -6.0 |
| tam | 3196 | 14.5 | 12.2 | 2.4 | 13.2 | 3.4 |

(fonkrizi = Eyl–Eki 2026, kompakt model, n=43 → DÜŞÜK güven; TR payının negatif çıkması düzeltilmiş R² cezası.)

**Faktör-blok düzeyi (hangi küresel faktör?).** Tam dönemde en büyük küresel blok 30/47 hissede Euro Stoxx 50 (medyan %0,9), 7'sinde EEM, 6'sında USDTRY; son 1 yılda EEM 19, **Brent 11**, Stoxx 7, altın 5 hissede birinci. Belirgin özgün bloklar: TRALT–altın %2,2 (tam), TUPRS–Brent %1,9 (tam) / %5,6 (son 1y), PGSUS/TAVHL–Brent %8,2/%8,3 (son 1y), GUBRF–altın %11,6 (son 1y; mekanizma belirsiz, 1. tur tarama da yalnız OOS'ta görmüştü), PETKM–Brent %4,8 (son 1y).

**Hisse bazında tablo (%, 2024–26 küresel payına göre sıralı).** 'küresel/sistematik' = küresel Shapley ÷ toplam R²; ihracatçı/emtia hisselerinde en yüksek (AEFES %7,9, FROTO %7,8, TUPRS %7,2, TOASO %7,2). Sektör payı en yüksek: TRMET %60, TRALT %42 (Koza grubu: aynı grup şirketleri), bankalar %40–42. Hisseye özgü pay en yüksek: BRSAN %78, SASA %78, TKFEN %71, AEFES %71, ENKAI %71, HEKTS %71, GUBRF %70.

| hisse | küresel_tam | küresel_24-26 | küresel_son1y | küresel_tek_başına_tam | küresel_özgün_tam | TRmakro_tam | piyasa_tam | sektör_tam | özgü_tam | küresel/sistematik_tam |
|---|---|---|---|---|---|---|---|---|---|---|
| TUPRS | 3.1 | 6.5 | 13.0 | 5.9 | 1.5 | 0.2 | 20.2 | 20.0 | 56.5 | 7.2 |
| GUBRF | 1.7 | 5.9 | 17.2 | 3.8 | 0.6 | 0.4 | 15.8 | 11.7 | 70.3 | 5.8 |
| TAVHL | 2.5 | 5.8 | 15.0 | 6.7 | 0.1 | 0.3 | 17.9 | 19.5 | 59.9 | 6.1 |
| PGSUS | 2.4 | 5.7 | 11.8 | 6.3 | 0.6 | 0.9 | 20.3 | 27.1 | 49.2 | 4.7 |
| TRALT | 3.5 | 5.1 | 8.1 | 6.5 | 1.4 | 0.2 | 11.4 | 41.6 | 43.3 | 6.2 |
| THYAO | 3.4 | 5.1 | 9.2 | 8.6 | 0.6 | 0.9 | 30.1 | 25.3 | 40.3 | 5.6 |
| TRMET | 1.9 | 4.3 | 9.8 | 4.9 | -0.0 | 0.2 | 11.5 | 60.2 | 26.3 | 2.5 |
| SISE | 2.5 | 4.1 | 7.3 | 6.9 | 0.3 | 0.3 | 26.2 | 21.4 | 49.5 | 4.9 |
| PETKM | 1.3 | 4.0 | 14.5 | 2.8 | 0.7 | 0.4 | 26.5 | 13.6 | 58.2 | 3.1 |
| KRDMD | 2.1 | 3.8 | 2.4 | 6.0 | 0.1 | 0.4 | 24.8 | 21.8 | 51.0 | 4.3 |
| TCELL | 1.9 | 3.8 | 7.1 | 5.4 | 0.1 | 0.3 | 23.9 | 20.0 | 53.8 | 4.2 |
| SAHOL | 3.7 | 3.6 | 10.0 | 10.6 | 0.2 | 1.8 | 37.0 | 21.1 | 36.4 | 5.8 |
| AEFES | 2.3 | 3.6 | 5.4 | 5.5 | 0.4 | 0.4 | 16.3 | 10.3 | 70.7 | 7.9 |
| GARAN | 2.5 | 3.5 | 10.5 | 8.0 | -0.0 | 1.8 | 25.4 | 40.9 | 29.4 | 3.6 |
| VAKBN | 2.4 | 3.4 | 7.2 | 7.7 | -0.0 | 1.9 | 23.7 | 39.5 | 32.5 | 3.6 |
| AKBNK | 2.9 | 3.3 | 8.1 | 9.0 | 0.1 | 1.6 | 27.9 | 41.9 | 25.6 | 3.9 |
| DOAS | 1.9 | 3.1 | 9.3 | 5.1 | 0.4 | 1.3 | 12.8 | 17.1 | 66.9 | 5.8 |
| EREGL | 2.8 | 2.8 | 0.4 | 7.1 | 0.5 | 0.4 | 21.7 | 22.5 | 52.6 | 5.9 |
| TOASO | 2.9 | 2.8 | 3.4 | 7.4 | 0.5 | 0.3 | 19.4 | 17.5 | 59.9 | 7.2 |
| TTKOM | 2.5 | 2.8 | 7.1 | 6.7 | 0.3 | 1.3 | 26.4 | 19.7 | 50.2 | 5.0 |
| ISCTR | 2.4 | 2.7 | 6.4 | 7.5 | 0.0 | 1.3 | 27.5 | 42.2 | 26.6 | 3.2 |
| MGROS | 2.3 | 2.4 | 5.3 | 5.5 | 0.5 | 1.3 | 22.1 | 16.8 | 57.6 | 5.3 |
| ENKAI | 1.4 | 2.3 | 4.7 | 3.2 | 0.1 | 0.8 | 20.3 | 6.8 | 70.7 | 4.9 |
| YKBNK | 2.4 | 2.3 | 8.7 | 7.6 | 0.0 | 1.5 | 26.3 | 41.1 | 28.7 | 3.4 |
| FROTO | 3.0 | 2.2 | 3.8 | 6.9 | 1.1 | 0.3 | 18.0 | 17.7 | 61.0 | 7.8 |
| HALKB | 2.2 | 2.2 | 2.5 | 7.0 | -0.0 | 1.4 | 21.8 | 30.4 | 44.2 | 3.9 |
| OYAKC | 0.9 | 2.1 | 5.8 | 2.2 | 0.4 | 0.2 | 13.8 | 25.7 | 59.4 | 2.3 |
| TSKB | 1.5 | 2.0 | 4.6 | 4.7 | 0.0 | 0.7 | 19.0 | 29.0 | 49.8 | 3.0 |
| KCHOL | 3.2 | 1.8 | 5.3 | 8.8 | 0.4 | 1.3 | 35.0 | 20.0 | 40.6 | 5.3 |
| HEKTS | 0.9 | 1.7 | 4.0 | 2.7 | -0.0 | 0.2 | 17.8 | 10.1 | 70.9 | 3.2 |
| CIMSA | 1.3 | 1.7 | 3.5 | 4.0 | -0.0 | 0.4 | 15.4 | 29.0 | 53.9 | 2.8 |
| ASELS | 1.0 | 1.6 | 3.0 | 2.4 | 0.1 | 0.5 | 27.5 | 8.2 | 62.9 | 2.6 |
| ARCLK | 2.1 | 1.6 | 4.2 | 5.6 | -0.1 | 0.5 | 29.2 | 10.2 | 58.0 | 5.0 |
| SOKM | 1.2 | 1.5 | 4.0 | 3.2 | 0.2 | 0.3 | 15.4 | 20.4 | 62.7 | 3.3 |
| EKGYO | 1.7 | 1.5 | 6.1 | 4.9 | 0.0 | 0.5 | 29.4 | 15.8 | 52.6 | 3.5 |
| BIMAS | 1.2 | 1.5 | 2.4 | 3.1 | 0.2 | 0.3 | 18.2 | 14.3 | 65.9 | 3.6 |
| TKFEN | 1.3 | 1.4 | 1.3 | 3.4 | 0.0 | 0.2 | 20.4 | 6.8 | 71.3 | 4.7 |
| DOHOL | 1.2 | 1.4 | 4.8 | 3.8 | -0.1 | 0.2 | 18.4 | 14.3 | 65.8 | 3.5 |
| ODAS | 0.8 | 1.4 | 3.8 | 2.7 | -0.1 | 0.7 | 13.7 | 17.2 | 67.6 | 2.5 |
| AKSEN | 1.5 | 1.3 | 1.4 | 4.2 | 0.0 | 0.4 | 18.0 | 15.4 | 64.8 | 4.3 |
| ASTOR | 0.5 | 1.1 | 2.7 | 1.4 | 0.1 | -0.0 | 14.5 | 23.2 | 61.8 | 1.3 |
| VESTL | 1.2 | 1.1 | 1.6 | 3.4 | 0.1 | 0.3 | 15.9 | 24.3 | 58.3 | 2.8 |
| ENJSA | 1.1 | 0.9 | 3.8 | 3.1 | 0.1 | 0.0 | 23.4 | 12.7 | 62.7 | 3.1 |
| ALARK | 1.3 | 0.9 | 4.0 | 4.0 | 0.1 | 0.7 | 18.3 | 14.9 | 64.7 | 3.8 |
| BRSAN | 1.1 | 0.7 | -0.6 | 3.4 | -0.2 | 0.2 | 15.0 | 5.6 | 78.1 | 5.2 |
| ULKER | 1.0 | 0.6 | 1.2 | 2.8 | 0.2 | 0.4 | 18.5 | 10.3 | 69.8 | 3.4 |
| SASA | 1.1 | 0.5 | -0.7 | 2.6 | 0.2 | 0.1 | 12.2 | 9.1 | 77.5 | 4.7 |

**Fon krizi (Eyl–Eki 2026, kompakt model; 2026 Oca–Ağu ile fark, medyan puan):** toplam sistematik R² +6,6, piyasa payı +6,3, sektör +1,7, küresel ≈0. En çok 'kendine özgüleşen': HALKB (özgü pay +20), TAVHL (+20), PGSUS (+13), TKFEN (+11), SAHOL (+11); en çok piyasaya bağlanan: ENJSA, ASTOR, BRSAN, PETKM, ENKAI (özgü pay −25…−42). n=43 → DÜŞÜK.

## 2. Diebold–Yilmaz spillover (soru 2)

**Kurulum.** Pesaran–Shin genelleştirilmiş FEVD, H=10, VAR(1) OLS (VAR(2) tam dönem toplam endeksi 81,5 vs 81,4; ridge λ=0,05 kayan endeks 1–2 puan düşük, aynı şekil). Üç ağ:
- **N58:** 47 hisse + XU100 + 10 sürücü (ES, EEM, SX5E, VIX, DXY, Brent, Altın, US10Y, USDTRY, TUR). Kayan 250g pencerede sabit düğüm seti için ASTOR/SOKM/ENJSA hariç 55 düğüm (2014+); tam 58 düğüm 2023+.
- **S1:** XU100 + 10 sürücü (11 düğüm) — düğüm sayısı artefaktı olmadan ülke–dünya yönü; 60/120/250g pencereler.
- **S2:** 12 sektör portföyü (VİOP hisselerinden EW) + 10 sürücü (22 düğüm), 120/250g.
- Hizalama: **A** ham BIST takvimi; **B** ABD/FX kapanışlı sürücüler (ES, EEM, VIX, DXY, Brent, Altın, US10Y, USDTRY, TUR) +1 gün (BIST t+1 ile hizalı; Stoxx kaydırılmadı); **C** saatlik 15:00 UTC anlık fiyat (gerçek senkron; 2024-06-12+, EEM/TUR hariç, 15:00 UTC'de ABD nakit seansı kış aylarında açık değil).

**Toplam spillover (N58, statik, %):** A: 2014–17 80,7 · 2018–20 81,8 · 2021–23 83,7 · 2024–26 83,4 · son 1y 85,7 · tam 81,4; B neredeyse aynı (80,6–87,0). Kayan 250g (N55-A) yıllık ortalama 79,4 (2018) – 86,4 (2016); 2020 85,0; 2022 85,9; 2026 84,4. Bu düzey, birbirine çok bağlı 45 BIST düğümünün GFEVD'de karşılıklı sayılmasından gelir; düzeyden çok değişim anlamlıdır.

**Bloklar (N55-A, kayan 250g, yıllık ort.):** hisselerin FEV'sinin küresel sürücülerden gelen payı 2014–2021 %3,4–5,5 → 2023–2025 %1,3–2,0 → 2026 %3,3; B hizalamasında %1,2–2,6. 'Küresel sürücülerin FEV'sinin BIST'ten gelen payı' %25–50 görünüyor — bu **düğüm sayısı artefaktı** (45 korelasyonlu BIST düğümünün her biri küçük ρ² ile sayılıyor), S1'de aynı ölçü %2–5.

**Net spillover = merkezilik eleştirisi (kritik).** Aynı tam dönem VAR'ında H=1 (salt eşzamanlı Σ) ve H=10 net sıralamaları Spearman 0,994; net sıralama ile mutlak korelasyon merkeziliği Spearman 0,90. GFEVD'de H=1'de θ_ij = ρ_ij² / Σ_k ρ_ik² → asimetri yalnız satır normalizasyonundan gelir. Yani günlük veride 'net yayıcı' = 'herkesle en çok korele olan' (endeks ağır sikletleri), 'net alıcı' = 'kendine özgü' hisse. Yönlü nedensellik yorumu YAPILMAMALI.

**N58-A net spillover (%; pozitif = net yayıcı):**

| düğüm | 2014-17 | 2018-20 | 2021-23 | 2024-26 | son 1y | tam | B tam |
|---|---|---|---|---|---|---|---|
| XU100 | 124 | 135 | 106 | 114 | 97 | 121 | 133 |
| TUR | 76 | 57 | 41 | 95 | 79 | 65 | −71 |
| SAHOL | 36 | 43 | 47 | 43 | 40 | 45 | 54 |
| KCHOL | 33 | 23 | 42 | 34 | 31 | 37 | 45 |
| AKBNK | 63 | 52 | 16 | 26 | 28 | 35 | 43 |
| ISCTR | 63 | 49 | 8 | 37 | 40 | 34 | 41 |
| GARAN | 62 | 53 | −8 | 27 | 40 | 25 | 32 |
| THYAO | 21 | 28 | 18 | 29 | 28 | 26 | 32 |
| SISE | 10 | −3 | 38 | 37 | 26 | 24 | 30 |
| HALKB | 55 | 29 | 2 | −13 | −19 | 14 | 21 |
| ES | −5 | −5 | −8 | −13 | −13 | −10 | −49 |
| USDTRY | −17 | −39 | −35 | −23 | −32 | −36 | −48 |
| SASA | −40 | −17 | −29 | −34 | −42 | −30 | −27 |
| BRSAN | −24 | −7 | −38 | −28 | −29 | −27 | −23 |
| BIMAS | −31 | −34 | −5 | −12 | −13 | −25 | −21 |

Hisse sıralaması A ile B arasında aynı (Spearman 1,00 tam dönem; son 1y 0,99), dönemler arası 0,34–0,87. **Bankaların 'yayıcı' rolü 2021–23'te çöktü** (GARAN −8, VAKBN +1,5, HALKB +1,9; KKM/makro-ihtiyati düzenleme dönemi) ve 2024–26'da HALKB dışında geri geldi. TUR, A'da BIST seansını içerdiği için yayıcı, B'de alıcı → ayna, yorumlanmamalı. En büyük ikili net spillover'lar küçük (tam dönem en büyük |net| 1,7 puan: KCHOL→TUPRS, SAHOL→BIMAS); son 1y PETKM→TUPRS 3,3, HEKTS→SASA 3,0.

**S1 (XU100 + 10 sürücü) net spillover (%) ve hizalama:**

| düğüm | A 2014-17 | A 2018-20 | A 2021-23 | A 2024-26 | A son1y | A fonkrizi | A tam | B tam | B son1y |
|---|---|---|---|---|---|---|---|---|---|
| EEM | 16,3 | 28,3 | 10,2 | 15,8 | 21,7 | 19,0 | 16,6 | −17,5 | −3,4 |
| ES | 16,3 | 23,0 | 12,5 | 11,7 | 20,3 | 16,7 | 14,8 | −17,1 | −5,4 |
| TUR | 19,1 | 16,3 | 6,7 | 5,0 | 4,6 | 0,3 | 14,3 | −32,8 | −64,0 |
| VIX | 4,3 | −4,7 | 1,1 | 5,0 | 9,1 | 1,4 | 0,4 | −18,7 | −12,9 |
| SX5E | 0,4 | 9,0 | −2,1 | −13,1 | 0,1 | −18,3 | −3,1 | 66,2 | 77,4 |
| XU100 | −12,0 | −3,6 | −4,0 | −3,0 | −3,0 | −2,6 | −8,6 | 59,6 | 91,6 |
| USDTRY | −7,0 | −15,8 | −7,9 | −3,8 | −13,5 | −9,3 | −11,2 | −16,8 | −8,4 |
| BRENT | −13,7 | −14,9 | −6,9 | −5,8 | −10,5 | −4,3 | −6,6 | −5,3 | −33,9 |

C (gerçek senkron, 2024-06..2026-10, 8 sürücü): ES +8,7, SX5E +3,8, VIX +3,6, DXY +0,3, US10Y −0,4, ALTIN −3,6, USDTRY −3,8, XU100 −4,1, BRENT −4,3; toplam endeks A 27,5 / B 24,8 / C 34,0. **A, C'ye çok daha yakın**; B, ABD sürücülerini BIST'in 'gerisine' iterek sahte 'BIST → dünya' yönü üretir (XU100 +60…+92, SX5E kaydırılmadığı için +66). XU100 FEV'sinin ES'ten gelen payı C %8,1 (A %5,2, B %1,4), USDTRY'den C %6,1 (A %0,8, B %0,7): günlük veri ABD bağını hafif, kur bağını belirgin biçimde eksik ölçüyor.

**Rejimler (kayan pencere; kriz başlangıcından bir gün önce → kriz sonu):**

| kriz | tür | S1-60g toplam | S1-60g BIST←küresel | S2-120g BIST←küresel | S2-120g BIST-içi | N55-250g hisse←küresel |
|---|---|---|---|---|---|---|
| 2015 Çin devalüasyonu | küresel | 58,9→68,5 | 27,1→43,6 | 10,8→12,0 | 79,3→79,0 | 3,9→4,0 |
| 2016 darbe girişimi | yerel | 73,6→71,9 | 47,2→30,6 | 13,7→8,2 | 79,1→83,3 | 4,9→4,3 |
| 2018 kur krizi | yerel (dolar) | 55,6→61,4 | 22,4→37,5 | 5,4→5,5 | 86,6→87,7 | 2,8→3,0 |
| 2020 COVID | küresel | 64,5→73,1 | 50,1→54,5 | 5,6→18,6 | 84,7→73,0 | 2,9→6,4 |
| 2021 Ara TL/KKM | yerel | 54,9→54,2 | 32,3→11,3 | 6,5→3,3 | 85,8→93,1 | 3,1→2,1 |
| 2023 seçim+ortodoks dönüş | yerel | 55,2→50,1 | 12,2→18,0 | 2,4→3,1 | 88,8→88,5 | 1,5→1,2 |
| 2024 Ağu carry çözülmesi | küresel | 59,2→60,1 | 32,5→40,7 | 9,1→9,0 | 81,7→82,0 | 1,2→1,5 |
| 2025 Mar İmamoğlu+Nis tarife | yerel+küresel | 51,2→63,2 | 36,3→17,6 | 7,3→6,6 | 82,9→84,7 | 2,5→2,1 |
| **2026 Eyl–Eki fon krizi** | yerel | 59,3→54,4 | **47,3→26,7** | 15,1→11,0 | 76,8→80,5 | 4,1→5,2 |

Fon krizi öncesi (Haz–Ağu 2026) BIST, 12 yılın en küresel dönemlerinden birindeydi (S1-60g BIST←küresel Haziran başı %54); kriz bu bağı yarıya indirdi ve BIST-içi bağı artırdı → küresel kökenli değil, yerel likidite şoku. 250g penceredeki artış (4,1→5,2) gecikmeli/seyreltik.

## 3. Granger nedensellik ağı (soru 3)

**Model.** y_t = c + Σ_{k≤p} a_k y_{t−k} + Σ m_k XU100_{t−k} + Σ g_k x_{t−k} + e; H0: g=0, HC1-dayanıklı Wald (χ²_p), p ∈ {1,2}. Hedef: 47 hisse × {cc, gap, intra}. Kaynak: 47 hisse + XU100 + 10 sürücü (58 kaynak; hedef başına 57). Dönem: tam, IS 2014–2020, OOS 2021–2026. BH-FDR her (hizalama × p × dönem × hedef) ailesi içinde (2.576–2.679 test). Toplam ≈ 82 bin regresyon (A 47,6k; B 16k; kaydırılmış null 16k; ters yön 2,9k).

| hizalama | p | dönem | hedef | test | FDR geçen | p<0,05 oranı % |
|---|---|---|---|---|---|---|
| A | 1 | tam | cc | 2.679 | 31 | 11,0 |
| A | 1 | tam | gap | 2.679 | 202 | 16,9 |
| A | 1 | tam | **intra** | 2.679 | **0** | 8,4 |
| A | 2 | tam | cc | 2.679 | 30 | 10,0 |
| A | 2 | tam | gap | 2.679 | 198 | 16,7 |
| A | 2 | tam | intra | 2.679 | 6 | 8,3 |
| A | 1 | IS / OOS | cc | 2.576 / 2.679 | 6 / 4 | 10,8 / 10,0 |
| A | 1 | IS / OOS | gap | 2.576 / 2.679 | 162 / 141 | 14,9 / 12,2 |
| A | 1 | IS / OOS | intra | 2.576 / 2.679 | 5 / 0 | 8,2 / 7,8 |
| B (ABD t+1 hizalı → ABD t−2 test) | 1 | tam/IS/OOS | cc | 2.679 | 0 / 1 / 0 | 7,1 |
| B | 1 | tam/IS/OOS | intra | 2.679 | 0 / 0 / 0 | 7,3 |
| Null (kaynak 157/409/733 gün kaydırılmış) | 1 | tam | cc / intra | 3×2.679 | 0 / 0–1 | 3,1–4,9 |

**Merkezilik (out-degree, FDR geçen hedef sayısı, tam dönem p=1):** cc: VIX 16, EEM 8, THYAO 3, EREGL/ALTIN/GUBRF/ES 1. gap: TUR 47, VIX 47, ES 28, EEM 27, USDTRY 16, XU100 9, DXY 6, KRDMD 5, BRENT 5. intra: yok. Yurt içi kaynak neredeyse hiç yok.

**İstikrar (IS'de p<0,01 olan kenarların OOS'ta aynı işaret ve p<0,05 olma oranı; null ≈ %2,5):** dış kaynak → gap %63 (182 kenar), dış → cc %30, dış → intra %4; yurt içi → cc %2,2, yurt içi → gap %8, yurt içi → intra %2,6. p<0,01 out-degree sıralaması IS/OOS Spearman: cc −0,28, gap 0,06, intra −0,35 (yurt içi: −0,46 / −0,42 / −0,35). IS'deki yurt içi 'liderler' (XU100, DOHOL, YKBNK, TCELL→intra 14 kenar) OOS'ta yok; OOS'un lideri THYAO (cc 13, intra 12 kenar p<0,01) IS'de yok.

**Ters yön (hisse/XU100_{t−1} → sürücü_t, kendi lag + XU100 lag kontrollü):** A'da 480 testte 0 FDR (p<0,05 oranı %5,8 = null) — BIST kapanışı ABD gününden önce bittiği için doğru sonuç. B'de **52 FDR geçişi** (XU100 → TUR t=41,6; XU100 → EEM t=10,6; XU100 → VIX t=−9,1; TRALT → altın t=8,6; TUPRS → Brent t=7,5) — tamamen hizalama artefaktı (kaydırılmış ABD günü BIST t−1 seansıyla örtüşür).

**Eşzamansızlık ağı nasıl çarpıtıyor (tartışma).**
1. ABD/vadeli/FX kapanışı (19:00–24:00 UTC) BIST kapanışından (15:00 UTC) sonra: sürücü_{t−1} → BIST_t 'Granger nedenselliği' büyük ölçüde ertesi sabah açılış gap'inde fiyatlanan eşzamanlı bilgidir. Kanıt: aynı kaynaklar gap hedefinde 202 kenar, gün-içi hedefte 0; ABD t−2'ye kaydırılınca (B) cc'de de 0.
2. Hizalamayı 'düzeltmek' için ABD'yi bir gün ileri almak (B) yönü tersine çevirir: BIST'i ABD'nin öncüsü gibi gösterir (ters yönde 52 sahte kenar; DY'de XU100 +60). Doğru senkron ölçüm (15:00 UTC anlık) A'ya yakın sonuç verdi.
3. TUR (NY'de Türkiye ETF'i) 47/47 hedefe gap kenarı veriyor; ES/VIX/EEM kontrolünden sonra da TUR_{t−1} → banka/holding gap'i kalıyor (kısmi r 0,12–0,17, OOS t 2,0–2,7): BIST kapanışından sonra NY'de fiyatlanan Türkiye'ye özgü haber. Gerçek ama işlenemez (pay vadelisinde akşam seansı yok).
4. Yurt içi kaynaklarda bayat fiyat (Lo–MacKinlay) etkisi sınırlı: 47 hissenin tümü likit (2021+ medyan günlük işlem hacmi 216 mn TL – 7,4 mlr TL; sıfır getiri oranı %1–4, SASA %12); büyük → küçük sistematik öncülük bulunmadı. Pozitif lag-1 otokorelasyonu en yüksek HALKB 0,12, SASA 0,12, VAKBN 0,11, ISCTR 0,10 — kendi lag kontrolü bu yüzden şart.
5. FDR'den geçen gün-içi kenarlar (p=2, 6 adet: THYAO → MGROS/TTKOM/KCHOL, USDTRY → FROTO/ENKAI, TUR → ENKAI) ve IS'deki USDTRY_{t−1} → SISE/PETKM/THYAO/VESTL gün-içi kenarları OOS'ta tekrarlamadı → ÇOK DÜŞÜK/DÜŞÜK.

**THYAO notu.** 2021–26'da THYAO_{t−1} (XU100_{t−1} kontrollü) 46/46 hedefin gün-içi getirisini pozitif öngörüyor (medyan t 2,0). XU100 intra hedefinde: 2021–23 THYAO t=3,95 ile XU100_{t−1} t=−4,0 (piyasa geri dönüşü + THYAO göreli gücü); 2024–26 t=0,3; 2014–20 t=0,9. Tek bir rejime özgü piyasa-zamanlama faktörü → DÜŞÜK.

## 4. Zamanla değişen korelasyon ve bulaşma (soru 4)

**Kurulum.** Tek değişkenli GARCH(1,1) (varyans hedeflemeli Gauss QMLE) + iki değişkenli DCC(1,1); karşılaştırma için EWMA (λ=0,94). 47 hisse ↔ XU100_t, ↔ ES_{t−1} (BIST_t açılışını besleyen ABD kapanışı), ↔ USDTRY_t. Medyan DCC parametreleri: XU100 a=0,030 b=0,944; USDTRY a=0,007 b=0,987; ES_{t−1} a=0,004 b=0,48 (korelasyon pratikte sabit ~0,05–0,07; EWMA daha oynak). Bulaşma testi: kriz penceresi vs kriz başından 20 gün önce biten 250 günlük sakin pencere; ham ve Forbes–Rigobon (kaynak değişken varyans artışıyla düzeltilmiş) korelasyon, Fisher-z.

**Yıllık ortalama korelasyon (47 hisse ortalaması):**
- XU100 DCC: 2014 0,59 · 2015 0,61 · 2016 0,61 · 2017 0,57 · 2018 0,58 · 2019 0,57 · 2020 0,60 · 2021 0,60 · 2022 0,62 · 2023 0,63 · 2024 0,60 · 2025 0,62 · 2026 0,59 (EWMA 0,52–0,68). 2026 aylık DCC: Haz 0,65 → Ağu 0,53 → Eki 0,62.
- USDTRY DCC: 2014–2021 −0,16…−0,21 → 2022 −0,09 → 2023 −0,02 → 2024 −0,06 → 2025 −0,08 → 2026 −0,08.
- ES_{t−1} EWMA: 2016 0,15, 2019 −0,02, 2023 0,00, 2024–26 0,09–0,11 (2026 Şub–Nis 0,15–0,21).

**Kriz testleri (47 hisse ortalaması; % = anlamlı artış gösteren hisse oranı, |z|>1,96):**

| kriz | kaynak | sakin ρ | kriz ρ (ham) | kriz ρ (FR) | kaynak vol oranı | ham artış % | FR artış % | FR azalış % |
|---|---|---|---|---|---|---|---|---|
| 2015 Çin | XU100 | 0,56 | 0,68 | 0,65 | 1,10 | 20 | 18 | 2 |
| 2016 darbe | XU100 | 0,62 | 0,75 | 0,61 | 1,62 | 30 | 0 | 0 |
| 2016 darbe | ES_{t−1} | 0,12 | 0,20 | 0,47 | 0,31 | 0 | 61 | 5 |
| 2018 kur krizi | XU100 | 0,54 | 0,56 | 0,45 | 1,42 | 4 | 0 | 13 |
| 2018 kur krizi | ES_{t−1} | 0,06 | 0,17 | 0,25 | 0,62 | 9 | 31 | 2 |
| 2020 COVID | XU100 | 0,54 | 0,74 | 0,49 | 2,11 | 50 | 4 | 13 |
| 2020 COVID | ES_{t−1} | −0,02 | −0,07 | −0,01 | 5,96 | 2 | 0 | 0 |
| 2020 COVID | USDTRY | −0,13 | −0,43 | −0,40 | 1,12 | 0 | 0 | 35 (daha negatif) |
| 2021 KKM | XU100 | 0,59 | 0,74 | 0,47 | 2,17 | 46 | 2 | 17 |
| 2023 seçim | USDTRY | −0,04 | 0,28 | 0,11 | 2,57 | 46 | 0 | 0 |
| 2024 Ağu carry | XU100 | 0,62 | 0,78 | 0,72 | 1,23 | 32 | 19 | 0 |
| 2024 Ağu carry | USDTRY | 0,00 | −0,25 | −0,43 | 0,49 | 0 | 0 | 40 (daha negatif) |
| 2025 Mar–Nis | XU100 | 0,60 | 0,82 | 0,58 | 2,21 | 45 | 4 | 0 |
| **2026 fon krizi** | XU100 | 0,61 | 0,68 | 0,60 | 1,24 | 9 | 2 | 9 |
| 2026 fon krizi | ES_{t−1} | 0,09 | 0,04 | 0,05 | 0,84 | 0 | 0 | 2 |
| 2026 fon krizi | USDTRY | −0,05 | −0,02 | −0,02 | 0,84 | 0 | 0 | 0 |

Yorum: (i) Yerli piyasa ile korelasyon her krizde yükseliyor ama artışın neredeyse tamamı volatilite artışının mekanik sonucu (Forbes–Rigobon: 'bulaşma değil, karşılıklı bağımlılık'); yalnız 2015 Çin ve Ağu 2024 carry çözülmesinde hisselerin ~%18–19'unda düzeltme sonrası da artış var (kısa pencere 14–35 gün → DÜŞÜK). (ii) ABD'den bulaşma kanıtı yok: COVID'de ES_{t−1} korelasyonu değişmedi; 2016 ve 2018'deki FR 'artışları' ES'nin sakin olmasından (vol oranı <1) kaynaklanan ters düzeltme + 22–28 günlük pencere → DÜŞÜK. (iii) Kur kanalı küresel risk-off'ta güçleniyor (COVID, Ağu 2024: TL değer kaybı = hisse düşüşü), yerel siyasi şokta tersine dönebiliyor (2023 seçim: TL zayıflarken nominal hisse yükseldi). (iv) Fon krizinde hisse–XU100 korelasyonu Ağustos dibinden (DCC 0,53) Ekim'de 0,62'ye döndü; en çok artanlar ALARK +0,22, MGROS +0,19, ODAS +0,19, SASA +0,17, PETKM +0,16 (zorunlu satışla 'hepsi birlikte'), HALKB −0,20 (DCC; EWMA −0,39: şirkete özgü ayrışma, nedeni bu çalışmada doğrulanmadı). Düzeltilmiş korelasyon artışı yok; küresel bağlar zayıfladı → yerel likidite şoku.

## 5. Sektör ajanlarının iddiaları bu çerçevede (soru 5)

**Yöntem.** master_findings_r1.csv (3.499 satır) + f_kimya/f_metal/f_otomotiv/f_tarama (1.518) = 5.017 iddia; günlük çerçevede test edilebilen 3.276 satır (47 hisse, panelde sürücü, relation ∈ sync/lead_gap/lead_intra/lead_multiday; saatlik/dakikalık segment iddiaları, olay/rejim/hipotez hariç), 3.021 tekil test, tam dönem + OOS.
- Senkron iddia: hisse_t ~ küresel 8×(t,t−1) + USDTRY(t,t−1) + TUR_{t−1} + XU100_t + sektör akranı_t + sürücü_t + sürücü_{t−1} (sürücü kontrol setindeyse kontrolden çıkarılır; sürücü hissenin akranıysa sektör faktörü çıkarılır).
- Öncülük iddiası: hedef (gap/intra/cc)_t ~ hisse_{t−1} + XU100_{t−1} + küresel 8_{t−1} + USDTRY_{t−1} + TUR_{t−1} + sürücü_{t−k}.
- Karar: BH-FDR (sınıf içi) q<0,05, iddiayla aynı işaret, |kısmi r| ≥ 0,05, OOS'ta aynı işaret ve |t| ≥ 2 → AYAKTA. Kontrol setindeki bir faktörle |r|>0,8 olan sürücüler (GLD~altın, CL=F~Brent, NQ=F~ES) 'ikiz' sayılıp o faktörün kendi testine bakıldı.
- **Uyarı:** ajanlar iddialarını 2021–26'yı da içeren tam veriyle seçti; buradaki 'OOS tutarlılığı' temiz bir örneklem dışı test DEĞİL, yalnız alt dönem istikrarıdır.

**Sonuç (iddia satırı sayısı; orijinal güven etiketine göre):**

| karar | YÜKSEK | ORTA | DÜŞÜK | ÇOK DÜŞÜK | toplam |
|---|---|---|---|---|---|
| A1 AYAKTA: hisseye özgü dış bağ | 34 | 225 | 135 | 61 | 455 (%14) |
| A1b AYAKTA ama küçük (\|pc\|<0,05) | 2 | 9 | 13 | 2 | 26 |
| A2 AYAKTA: yerli küme/sektör | 67 | 19 | 7 | 1 | 94 (%3) |
| A3 AYAKTA: ortak faktöre özgün maruziyet (emtia/kur/TUR, XU100 ötesi) | 25 | 36 | 10 | 7 | 78 (%2) |
| B0 AYNA (ADR/ETF) | 8 | 1 | 1 | 0 | 10 |
| **B1 SADECE ORTAK FAKTÖR** | **116** | **335** | 715 | 442 | **1.608 (%49)** |
| B2 ZAYIF / OOS'ta tutmuyor | 10 | 76 | 38 | 20 | 144 (%4) |
| B3 GÜRÜLTÜ (zaten zayıf) | 0 | 65 | 154 | 618 | 837 (%26) |
| B4 İŞARET TERS | 0 | 12 | 5 | 7 | 24 |
| toplam | 262 | 778 | 1.078 | 1.158 | 3.276 |

Ajan bazında 'sadece ortak faktör' oranı: banka 367/434 (%85; Avrupa/EM banka hisseleri, banka ETF'leri, ADR'ler), gunici 464/846 (%55; çoğu ES/NQ/TUR → gap: ABD gece hareketinin kendisi), metal 211/467 (%45), kimya 104/219 (%47), tarama 256/574 (%45; tarama zaten küresel-10 kontrolü kullanmıştı → en çok ayakta kalan: 187 A1).

**Ayakta kalanlar (tekil, tam faktör kontrollü kısmi r; OOS):**
- Havayolu emsalleri: THYAO ← LHA.DE 0,17 (0,16), AF.PA 0,12, EZJ.L 0,12, IAG.L 0,11, RYA.IR 0,11, ICAGY 0,11; PGSUS ← EZJ.L 0,12 (0,13), ICAGY 0,09, IAG.L 0,09. → YÜKSEK/ORTA.
- Rafineri/petrol: TUPRS ← CRAK 0,19 (0,18), PKN.WA 0,13, NESTE.HE 0,12, OXY 0,11, EQNR.OL 0,11, AKRBP.OL 0,11, ENI/REP/TTE 0,09–0,10; TUPRS ← Brent 0,15 (OOS 0,22). → YÜKSEK.
- Çelik/maden: EREGL ← MT.AS 0,09; KRDMD ← PICK 0,09; KRDMD/EREGL/BRSAN ← FMG.AX (Asya lag0) ve BHP/MT (ABD lag1) → gün-içi 0,06–0,08. → ORTA / DÜŞÜK (öncülük).
- Savunma: ASELS ← BA.L 0,10, HO.PA 0,09, SAAB 0,09, EUAD 0,13 (kısa örneklem). → ORTA.
- Altın: TRALT ← GC=F 0,13 (OOS 0,09, t 2,7); GUBRF ← altın 0,08 (OOS 0,13) → ORTA (GUBRF mekanizması belirsiz).
- Kur: SAHOL ← USDTRY −0,11; ENKAI +0,11 (döviz gelirli); EREGL +0,09 (ihracatçı); PGSUS −0,09; TTKOM −0,07 → ORTA.
- TUR_{t−1} → gap (bankalar, holdingler, EREGL, SISE…: 0,09–0,17) → ORTA, işlenemez.
- Yerli kümeler (A2): TRMET–TRENJ 0,77, TRALT–TRMET 0,66, KRDMD–KRDMA/KRDMB 0,59 (aynı şirketin pay grupları: mekanik), THYAO–PGSUS 0,52, EREGL–ISDMR 0,45, CIMSA–AKCNS 0,42, EREGL–KRDMD 0,39, ASTOR–EUPWR 0,37, CIMSA–OYAKC 0,35, TOASO–FROTO 0,34, TCELL–TTKOM 0,32, MGROS–SOKM 0,31, TUPRS–AYGAZ 0,30, SAHOL–AKBNK 0,29.
- Asya lag0 → gap (N225, KS11, SSE → tüm büyük hisseler, 0,22–0,27) ayakta ama BIST açılışında fiyatlanıyor; büyük olasılıkla ABD vadelilerinin Asya seansındaki hareketini taşıyor (günlük veriyle ayrıştırılamaz).

**Ortak faktöre indirgenen YÜKSEK iddialar (116):** gunici 62 (ES=F/NQ=F/TUR → gap: ilişki doğru ama 'ABD gece hareketi' tek ortak faktör; NQ=F ES'nin ikizi), banka 31 (ES/EEM/BBVA/ADR → gap/senkron), metal 19 (KRDMD/TRMET/BRSAN ← diğer metal hisseleri, gümüş, bakır), tarama 3 (TRALT ← SI=F/SLV/518880.SS: altın/gümüş, altın faktöründe eriyor), savunma 1 (TTKOM–TKC ADR). Ayrıca TCELL–TKC, bankalar–AKBTY/TKGBY: ADR aynası.

## 6. Karşı argümanlar ve sınırlamalar
- **Doğrusal, örneklem içi R².** Düzeltilmiş R² aşırı uyumu kısmen giderir; doğrusal olmayan (asimetrik, eşik) maruziyetler küçük ölçülür. Tam dönem payları rejim değişimi nedeniyle küçüktür; alt dönem rakamları esas.
- **Sektör tanımı benim seçimim.** TRALT/TRMET/TRENJ aynı grup (sektör payı şişkin); SISE için XUSIN (mekanik içerme); KRDMD akranlarından KRDMA/B çıkarıldı. XU100 hisseyi içerir; EW-46 sağlamlığı medyanda fark göstermedi, ağır sikletlerde birkaç puan fark olabilir.
- **Zaman uyumsuzluğu.** Günlük FX kapanışı TR makro payını düşük gösteriyor (senkron sürümle ~10 kat); senkron veri yalnız 2024-06+ (≈500–600 gün). EEM ve TUR 15:00 UTC'de ölçülemedi.
- **DY.** 55–58 düğümlü VAR(1)'de 250 gözleme 56 parametre: gecikme katsayıları gürültülü (ridge ile aynı sonuç). GFEVD net değeri günlük veride korelasyon merkeziliği; 'yayıcı' etiketini nedensellik olarak okumayın. Toplam endeks düğüm sayısına bağlı.
- **Granger.** Doğrusal ortalama öngörülebilirliği; varyans/kuyruk spillover'ı test edilmedi. FDR aile içinde; aileler arası düzeltme daha da az geçiş bırakır. Kaynaklar arası korelasyon yüksek (VIX/ES/EEM birbirinin ikamesi).
- **DCC.** İki değişkenli, Gauss QMLE; ES_{t−1} için DCC dinamiği zayıf (a≈0,004), EWMA daha bilgilendirici. Kriz pencereleri kısa (14–43 gün), Forbes–Rigobon kaynak volatilitesine duyarlı (kaynak sakinse ters yönde şişirir).
- **İddia kontrolü.** Ajanların seçimi tam veriye dayandığı için 'OOS tutarlı' gerçek replikasyon değil. Kontrol seti bir sektör ajanının sürücüsünü içerebilir (Brent, altın): bunlar ayrı sınıfta (A3) raporlandı. Saatlik/dakikalık ve olay iddiaları bu çerçevede test edilmedi (1.741 satır).
- **İşlenebilirlik.** Hiçbir bulgu strateji değildir; işlenebilirlik testi (maliyet, açılış dolumu) yapılmadı — 1. tur tarama sonucunu (gün-içi öncülük OOS'ta maliyet sonrası negatif) değiştirecek bir kanıt bulunmadı.

## 7. Dosyalar ve yeniden üretim
- Rapor: `out/ry_ag.md`; bulgular: `out/f_y_ag.csv` (1.203 satır; relation ∈ variance_share, spillover_net, spillover_pair, granger, regime, claim_check — standart dışı ilişkilerde sütun anlamı 'notes' içindeki SÜTUN NOTU'nda); varyans ayrıştırması: `out/y_varyans_ayristirma.csv` (47 hisse + XU100 × 6 dönem × 5 spesifikasyon + senkron karşılaştırma; Shapley, tek başına, özgün, iki sıralı ayrıştırma, 12 blok Shapley).
- Kod (`out/code_y_ag/`): common.py (faktörler, kümeler, dönemler), vardec.py, vardec_sync.py, dy.py (N58/N55, A/B/C), dy2.py (S1/S2, kriz pencereleri), granger.py, dcc.py, claims.py, final.py, md.py. Ara sonuçlar `cache/`: vardec_all.csv, vardec_sync_compare.csv, dy_rolling_total.csv, dy_rolling_nodes.csv.gz, dy_static_nodes.csv, dy_static_pairs.csv.gz, dy_align_compare.csv, dy2_rolling.csv, dy2_static.csv, granger_all.csv.gz, granger_reverse.csv, liquidity.csv, dcc_paths.parquet, ewma_paths.parquet, contagion_tests.csv, claims_tests.csv, claims_verdicts_final.csv.
- Yeniden üretim: `cd out/code_y_ag && export OMP_NUM_THREADS=1 && nice -n 10 python3 vardec.py && nice -n 10 python3 vardec_sync.py && nice -n 10 python3 dy.py && nice -n 10 python3 dy2.py && nice -n 10 python3 granger.py && nice -n 10 python3 dcc.py && nice -n 10 python3 claims.py && python3 final.py` (toplam ≈ 15 dk, tek çekirdek).
