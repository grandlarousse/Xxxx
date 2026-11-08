# USO — United States Oil Fund

**TradingView:** `AMEX:USO` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı · ⚠ PTP/K-1 ürünü: satışta %10 brüt kesinti (1446(f)) riski

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 745 | 14.0 | 320 | %-9.8 | 1.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** [PTP] maliyet/oynaklık 0.044. Ham petrolün en likit ETF'i (745 mn$, 14 bp); S2 adayının aracı; NYMEX:CL1! ile gece/gündüz izlenebilir. PTP: %10 brüt satış stopajı riski (USCF bildirimi 31.10.2026'da süresi doldu) -> her işlemden önce uygulamada kontrol; Midas'ta bulunurluk doğrulanamadı. 2020 sonrası çok vadeli/5 günlük roll yapısı. **Ana ajan notu:** PTP %10 kesinti riski teyit edilene kadar referans/izleme; S2 zayıf.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt — tek başına işlem gerekçesi değil)

#### USO alt Bollinger kırılımı, 1 gün bekle, 2 gün long (ham petrol)  
*İzlemede — zayıf kanıt · güven: dusuk · id: `enerji_tarim_S2`*

- **Sinyal (t kapanışında):** AMEX:USO günlük grafiği, Bollinger Bantları (uzunluk 20, kaynak kapanış, StdDev 2.05 — TradingView popülasyon std kullandığı için 2.05, backtestteki örneklem std'li 2.0'a denk). Sinyal: t günü USO kapanışı alt bandın altında. t günü işlem YAPMA; t+1 günü kapanışa yakın AMEX:USO al (2x araç: AMEX:UCO), t+3 günü kapanışında sat. Pozisyondayken gelen yeni sinyaller yok sayılır. PTP'siz uygulama AMEX:XOP ile denendi: daha zayıf ve ufka duyarlı (notlar).
- **Giriş:** Sinyal gününden SONRAKİ işlem günü (t+1) ABD kapanışına yakın: kış TR 23:45-23:59, yaz 22:45-22:59 piyasa emri ya da after-hours limit. t kapanışında girmek (C0) zararlı çıktı.
- **Tutuş / çıkış:** 2 işlem günü (t+1 kapanışı -> t+3 kapanışı) — t+3 günü ABD kapanışından dakikalar önce sat (TR ~23:45-23:59 kış). Erken çıkış kuralı yok.
- **İşlem aracı:** USO, UCO (sinyal: USO)
- **Geçmiş (ajan):** n=54, net 121.4 bp/işlem (brüt 135.4), kazanma %68, t=2.95, IS 75.4 / OOS 167.5 bp, yılların %78'i pozitif, en kötü işlem -763 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500$):** C0: net -35 bp (t -0.7, n=72) · O1: net -4 bp (t -0.1, n=72) · C1: net 108 bp (t 2.8, n=59); 1.000$ pozisyonda ana mod net 90 bp (t 2.4)
- **Denetçi düzeltmesi:** Sayılar doğru. Ek: en iyi 5 hariç 74,6 bp t 1,89; 2022 hariç t 1,99; 2025-26 son 7 işlem ort. -32 bp; IS sırası 386/8.149; evrende ort. t -0,98.
- **Denetçi kural düzeltmesi:** Kural aynı; 'aday strateji' değil, veri madenciliğinden çıkmış ve yalnız WTI kümesine özgü bir gözlem olarak işaretlenmeli. UCO'yu '2x araç' diye önermek yerine '2026'da USO'ya göre ~1,1-1,6x' notu düşülmeli.
- **Denetim:** Bağımsız simülatörle birebir: n=54, brüt 135,4 / net 121,4 bp, t 2,95, kazanma %68,5, PF 2,63, IS 75 bp (t 1,13) / OOS 167 bp (t 3,47), yıl+ 7/9, maxDD -%9,3, en kötü -763 bp; C0/O1/C1 ızgarası, 'sinyal+1 gün O1 h2' (net 90 bp t 3,14) ve diğer ETF'ler (BNO 94, DBO 95, UCO 225, XOP 131, XLE 63, PDBC 41, SCO -277) aynı. Sinyal t kapanışıyla, giriş t+1 kapanışı, çıkış t+3 kapanışı; ileriye bakma yok. En iyi 5 işlem (2022-07-06, 2020-03-09, 2022-09-08, 2021-07-20, 2020-02-28) gerçek olaylar. TradingView 2,05 çarpanı doğru (2*sqrt(20/19)). Sağlamlık: Lehte: permütasyon p 0,005 (tüm günler) ve 0,005 (düşüş rejimi eşli); winsorize t 3,18; 2020 hariç t 3,44; 2020+2022 hariç t 2,35; 1.000$'da net 103 bp t 2,51; WTI fonları kendi bantlarıyla da pozitif (UCO 288 bp t 4,19, DBO 85 t 2,37, USL 61 t 1,85). Aleyhte: yukarıdaki sorunlar. Maliyet: 1.000$ 103 (t 2,51) / 2.500$ 121 (2,95) / 10.000$ 130 (3,17).
- **Denetçinin uyarıları:** (1) Seçim yanlılığı: genel taramadan (≈8.300 aile satırı) seçildi; IS t 1,13 ve IS sırası 8.149 satırda 386 -> IS'te seçilmezdi, 'OOS' gücü seçim açısından örneklem içi. Ailede IS'e göre seçilen en iyi 10/25/50/100 satırın OOS ortalaması +4/-40/-32/-24 bp (genel tarama bu ailede OOS'a bilgi taşımıyor). (2) Aynı kural (MR_bb20_alt C1 h2) evrende 312 ETF'te ortalama t -0,98, t>2 oranı %1,3 (şansın altında) -> genel bir olgu değil. (3) Sivri gecikme tepesi: giriş gecikmesi d=0 -38, d=1 +102, d=2 +15, d=3 -76 bp; aynı girişle h=3 net 8 bp; C0/O1 h1-h2 negatif. (4) Parametre ızgarasında tam örneklem t≥2 yalnız 6/35 hücre (köşegen sırt), IS net 24/35 hücrede negatif; OOS 34/35 pozitif -> Bollinger'a özgü değil, 2022-24 petrol rejimi. (5) Son 7 işlem (2025-26) ort. net -32 bp. (6) En iyi 5 hariç t 1,89 (IS 16 bp); 2022 hariç t 1,99. (7) Kendi bandıyla Brent (BNO 40 bp t 0,90) ve enerji hisseleri (XLE -20, XOP -42, OIH -36) çalışmıyor; tek bağımsız küme WTI fonları. (8) USO/UCO PTP: %10 kesinti -> negatif beklenti; UCO artık 2x USO değil (2026 betası 1,13). FDR geçmiyor.
- **Giriş zamanı sağlamlığı:** C0 h1: brüt -26 / net -40 bp (t -1.02); C0 h2: brüt -24 / net -38 bp (t -0.71); C0 h3: brüt 4 / net -10 bp (t -0.14); O1 h1: brüt -14 / net -28 bp (t -1.19); O1 h2: brüt 10 / net -4 bp (t -0.10); O1 h3: brüt 81 / net 67 bp (t 1.23); C1 h1: brüt 32 / net 18 bp (t 0.51); C1 h2: brüt 135 / net 121 bp (t 2.95); C1 h3: brüt 72 / net 58 bp (t 0.95). Kapanışa değil GECİKMEYE bağımlı: t+1 günü ortalama düşüş sürüyor, dönüş t+2..t+3'te. Sinyal 1 gün kaydırılıp t+2 açılışında girilse (h=2) net 90 bp t 3,14.
- **Maliyet duyarlılığı:** net bp: 1.000$ 103.4 / 2.500$ 121.4 / 10.000$ 130.4
- **Not:** IS t 1.13 (anlamsız), OOS t 3.47; yıl yıl 7/9 pozitif, 2026'da tek işlem (-149 bp); 2026 hariç t 3,04. IS dönemi USO'nun 2020 Nisan negatif fiyat ve çok vadeli yapıya geçiş dönemini içerir (2020: 9 işlem, ort. +28 bp). Önceden hipotez değildi (veri madenciliği riski). USO ve UCO PTP: USCF'nin 31.07.2026 qualified notice'ının 92 günü ~31.10.2026'da doldu, yenisi bulunamadı; %10 brüt stopaj uygulanırsa işlem başına ~-1000 bp => beklenti negatif. Midas'ta USO/UCO bulunurluğu doğrulanamadı. Son durum: 06.11.2026 USO kapanışı 148,41, alt bant ~144,5 (sinyal yok).
- Betik: `/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_enerji_tarim/aday_S3_uso_bb_gecikmeli.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| BNO | `AMEX:BNO` | 0.97 | 1.00 |
| USL | `AMEX:USL` | 0.91 | 1.46 |
| XLE | `AMEX:XLE` | 0.63 | 1.37 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| WTI ham petrol vadelisi (ön ay) | `NYMEX:CL1!` | dayanak; Globex ~23 saat, açılış boşluğunu önceden gösterir |
| WTI 2. ay | `NYMEX:CL2!` | CL2!/CL1!-1 kontango göstergesi |
| Brent vadelisi (ön ay) | `ICEEUR:BRN1!` | Brent; Londra saatlerinde fiyat keşfi |
| Dolar endeksi | `TVC:DXY` | dolar şoku emtiaya ters |

## 3. Takvim ve olay riskleri

EIA WPSR Çar 10:30 ET (TR 18:30; 12 Kas Per 12:00 ET); API Salı 16:30 ET; CL vadesi 20 Kas, 21 Ara 2026; USO roll 1-7 Ara 2026; OVX >= 1,25xSMA20 iken boyutu küçült.

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 14 bp maliyet; geçen 0). En güçlü geçmeyen: VVIX_dlog h3 t=-2.41 (IS -1.00/OOS -2.06, -23.1 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(USL) h3 t=-1.70 (IS -1.63/OOS -0.35, -40.9 bp/sd). Sürücüler eşzamanlıdır, öncü değildir. Kendi fiyat sinyali: S2 (düşük güven).

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
