# TBT — ProShares UltraShort Lehman 20  Year Treasury

**TradingView:** `AMEX:TBT` · **Aile:** Tahvil ve döviz · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 12 | 20,0 | 123 | %-4,0 | -2,0x | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** B6'nın alternatif aracı (−2x TLT; TMV'ye göre daha düşük risk). Medyan 12,3 mn $/gün (tercih edilen eşiğin alt sınırı), maliyet 20 bp. ProShares Trust (1940 Yasası) fonu; PTP değil (teyit önerilir). Midas bulunurluğu doğrulanamadı.

*Dayanak / ana araç kartı: `kartlar/TMV.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B6 — 10 yıllık Hazine ihalesi öncesi uzun vade zayıflığı — TMV (−3x TLT) ile 2 gün  
*İzlemede — zayıf kanıt · güven: orta · aile kimliği: `tahvil_doviz_S1`*  
*Bu ETF'nin rolü: tercih edilen araç (−2x, daha düşük kuyruk)*

- **Sinyal (t kapanışında):** Takvim sinyali (fiyat göstergesi yok): A = ABD Hazinesi 10 yıllık tahvil (10-Year Note) ihale günü — TreasuryDirect 'Upcoming Auctions' / Hazine geçici ihale takvimi; TradingView Ekonomik Takvim'de '10-Year Note Auction' (sonuç 13:00 ET = TR 21:00 kış / 20:00 yaz). SİNYAL GÜNÜ = A'dan 3 işlem günü önceki gün (A-3; ihale Salı ise önceki Perşembe, Çarşamba ise önceki Cuma; NYSE tatilleri sayılmaz). İŞLEM: AMEX:TMV long (alternatif AMEX:TBT, −2x). A-3 günü al, A-1 günü (ihaleden bir önceki işlem günü) kapanışta sat; ihale günü tutulmaz. Stop yok, erken çıkış yok. 30 yıllık ihale (A30) penceresi KULLANILMAZ (zayıf). Dayanak kontrolü: NASDAQ:TLT aynı pencerede ortalama −41 bp.
- **Giriş:** A-3 günü kapanıştan 5-10 dk önce piyasa ya da agresif limit emriyle (kış saati TR ~23:50, yaz saati TR ~22:50; Midas'ta MOC/LOC yok). Sinyal takvimden bilindiği için aynı gün açılışta (TR 17:30 kış / 16:30 yaz) almak da test edildi ve benzer sonuç verdi. Sıradaki: 10 Kas 2026 (Sal) ihalesi -> A-3 = 5 Kas Per (geçti; açık pozisyon 9 Kas Pzt kapanışta kapanır); 8 Ara 2026 (Sal, yeniden ihraç) -> giriş 3 Ara 2026 Per TR ~23:50.
- **Tutuş / çıkış:** 2 işlem günü (A-2 ve A-1) — A-1 günü kapanıştan 5-10 dk önce (kış TR ~23:50 / yaz ~22:50) sat; örn. 8 Ara 2026 ihalesi için 7 Ara 2026 Pzt. Uzatılmış saatlerde yalnız limit emir verilebildiği için normal seansta çık.
- **İşlem aracı:** TMV, TBT (sinyal: takvim (10Y Hazine ihalesi); dayanak NASDAQ:TLT)
- **Geçmiş (ajan):** n=119, net 104.1 bp/işlem (brüt 124.1), kazanma %59, t=3.17, IS 108.2 / OOS 99.9 bp, yılların %91'i pozitif, en kötü işlem -764 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 61 bp (t 2,8, n=117) · O1: net 38 bp (t 1,6, n=117) · C1: net 17 bp (t 0,7, n=117); 1.000 $ pozisyonda ana mod net 43 bp (t 2,0)
- **Denetçi düzeltmesi:** Sayılar örneklem içinde birebir doğru (TMV C0 n=119, net 104 bp, t 3,17; TBT net 62 bp, t 2,87). Eklenmesi gerekenler: örneklem öncesi TLT 2002-2016 brüt +7,6 bp (t 0,79), TBT 2008-2016 brüt −17 bp (t −0,68, net −37 bp); havuzlanmış TBT 2008-2026 (n≈218) brüt ≈ +37 bp, net ≈ +17 bp; en iyi 10 hariç TMV net 34,6 bp t 1,30; OOS eşlenik-permütasyon fazlası ~76 bp (p 0,04). Güven 'orta' değil 'düşük'.
- **Denetçi kural düzeltmesi:** Kural aynı kalabilir ama 'kabul' değil 'zayıf / rejime bağlı deneme' olarak sunulmalı: giriş yalnız A-3 seansında (açılış ya da kapanıştan dakikalar önce; A-2'de girilmez), gece/hafta sonu taşıması zorunlu; araç olarak TBT (−2x; en kötü −516 bp, maxDD −%9) TMV'ye tercih edilmeli; küçük pozisyon; 2026 zayıflığı ve ihale yapısı değişiklikleri izlenmeli; sonraki 12 işlemde ortalama ≤ 0 ise bırakılmalı.
- **Denetim:** Kendi simülasyonum (lib.trades/evaluate/td.full_eval kullanılmadan; lib.load fiyatı, SPY/NYSE takvimi, hazine_ihale_10y30y.csv UST10Y): TMV C0 119/119 işlem tarih tarih eşleşti (brüt farkı ≤5e-12 bp). TMV C0: n=119, brüt 124,1 bp, net 104,1 bp (2.500$; 20 bp), t=3,17, kazanma 0,588, PF 2,19, IS 108,2 bp (t 2,44) / OOS 99,9 bp (t 2,03), yıl+ 0,91, maxDD −%13,0, en kötü −764 bp; 1.000$ 86 / 10.000$ 113 bp. O1 net 60,8 (t 1,99; OOS 23,2 t 0,55), C1 net 45,0 (t 1,14; OOS 11,5 t 0,23), A-3 açılış 98,1 (t 2,82; IS 93 / OOS 103). TBT C0 net 62,3 (t 2,87; IS 62,9 / OOS 61,6, t 1,88). İleriye bakma yok (takvim önceden ilan edilir; ihale günlerinin hepsi işlem günü); çakışma yok; maliyet bir kez düşülüyor; TMV/TBT ex-date'i pencere içinde yok (lib.load ile td.load farkı 0). En iyi 5 işlem gerçek faiz şokları (2025-04-04 +1510 bp, 2019-09-06 +1077, 2020-11-05 +973, 2022-12-07 +857, 2022-04-07 +778; ΔDGS30 +14..+30 bp; veri_kalitesi/veri_duzeltmeleri satırı yok). Hazine getirisinde de var (pencerede ΔDGS10 +2,80 bp, t 4,68): ETF/bayat fiyat artefaktı değil. Sağlamlık: Rastgele gün permütasyonu p=0,0010 (TMV), ay+gün eşlenik p=0,00005 (IS p=0,0002, OOS p=0,040; A-3=Cuma p=0,0038). Takvim ±5..20 gün kaydırma: 32 kaydırmanın hiçbiri −41 bp'ye yaklaşmıyor (en düşük −19,6). 2020 hariç 87,5 bp t 2,57; 2022 hariç 100,7 t 2,97; ikisi hariç 81,5 t 2,33; %5/%95 winsorize 99,7 t 3,54; medyan 63,5 bp. Komşu pencereler örneklemde plato (A-4→A-1 TBT +79 bp t 3,0; A-3→A TLT −43), örneklem öncesinde A-4→A-1 / A-5→A-1 doğru işaretli ama anlamsız (TBT +33 / +53 bp, t 1,05 / 1,48), A-3→A-1 yanlış işaretli.
- **Denetçinin uyarıları:** (1) ÖRNEKLEM ÖNCESİ TESTTE YOK: aynı kural TLT 2002-08..2016-10 n=141 brüt +7,6 bp (t 0,79; işaret yanlış), TBT 2008-05..2016-10 n=99 brüt −17,0 bp (t −0,68; net −37 bp, yılların %11'i pozitif); Hazine getirisinde 1990-2016 n=195 ΔDGS10 +0,40 bp (t 0,69), aynı aylık takvimli 2008-2016 n=102 +0,20 bp (t 0,25) — örneklemde +2,9 bp (t 5,0). Etki 2016-2026 rejimine özgü; 2008-2016'daki klasik desen (A-5→A-1 yükseliş + ihale sonrası toparlanma) da değişmiş. (2) OOS kenarı gece/hafta sonu taşımasına bağlı: TMV A-3 kapanış→A-2 açılış OOS +76 bp (t 3,21), A-2 açılış→A-1 kapanış OOS +43 bp (t 1,02); O1/C1 OOS ≈ 0 → 'kapanışa (gece taşımaya) bağımlı'. (3) Ay+haftanın günü eşlenik permütasyon OOS'ta p=0,040 (eşlenik rastgele pencereler de OOS'ta TMV'ye +44 bp veriyor; gerçek OOS fazlası ~76 bp). (4) Yoğunlaşma: en iyi 10 işlem hariç net 34,6 bp, t=1,30 (en iyi 5 hariç 63 bp, t 2,23); 2023-2026 n=46 t=1,71; 2024-2026 t=1,60; 2026 10 işlemde +20 bp. (5) Alt kesitler teoriyle çelişkili: yeni ihraç ayları (en büyük arz) n=39 net 58 bp t 0,97 < yeniden ihraç 127 bp t 3,22; 30Y ihale penceresi zayıf (ΔDGS30 +1,08 bp t 1,58); A-3=Cuma n=77 t 1,33; A-3=NFP günü n=74 t 1,41. (6) Global tek yönlü BH (12.515) ve Bonferroni'yi geçmiyor; yalnız 58 testlik önceden kayıtlı sette geçiyor; önceden kayıtlı hipotezin 30Y yarısı ve ihale sonrası toparlanma yarısı tutmuyor. (7) Midas: TMV/TBT bulunurluğu doğrulanmadı; −3x (en kötü 2 günlük −%7,6); MOC yok (kapanıştan dakikalar önce emir gerekir).
- **Giriş zamanı sağlamlığı:** C0: brüt 124 bp, net 104 bp, t=3.17 (OOS 100 bp); O1: brüt 81 bp, net 61 bp, t=1.98 (OOS 23 bp); C1: brüt 65 bp, net 45 bp, t=1.14 (OOS 12 bp); ek: A-3 AÇILIŞINDA giriş (TR 17:30 kış) brüt 118 bp, net 98 bp, t=2.82, IS 93 / OOS 103 bp. O1 (=A-2 açılışı) zayıf çünkü A-3 kapanışı→A-2 açılışı (çoğunlukla hafta sonu) boşluğu etkinin bir kısmını taşıyor: giriş A-3 seansı içinde yapılmalı.
- **Maliyet duyarlılığı:** TMV net/işlem: 1.000$: 86 bp | 2.500$: 104 bp | 10.000$: 113 bp (maliyet 2.500$'da 20 bp = 12 komisyon + 8 makas)
- **Not:** Literatür: Lou, Yan & Zhang (2013, RFS) ihale öncesi ikincil piyasa fiyat baskısı ve sonrası toparlanma; hipotez önceden kayıtlıydı (notlar/hipotezler.csv TD02 'Ek test: TLT C_A-3→C_A-1 <0'). IS t=2.44, OOS t=2.03; yılların 10/11'i pozitif (2017 hafif negatif). Plasebo (pencere ±5/±10 işlem günü kaydırılmış): etki yok (TLT −3..+17 bp, |t|<1,3). Haftanın günü eşlenik koşulsuz 2 günlük TLT ortalaması −2 bp. Pencerede CPI hiç yok, FOMC hiç yok; NFP içeren 26 pencerede etki daha büyük (TLT −66 bp) ama NFP'siz 93 pencerede de var (TLT −34 bp, TMV net +84 bp, t=2,18). 2020 hariç TMV net 88 bp (t=2,57); 2022 hariç 101 bp (t=2,97). İhale SONRASI toparlanma (A→A+2) ETF verisinde YOK (TLT −9 bp). Riskler: −3x kaldıraçlı ters ETF (en kötü 2 günlük işlem −%7,6, 2019-08; maxDD −%13); TMV/TBT'nin Midas'ta bulunurluğu doğrulanamadı; Treasury piyasa yapısı (ihale büyüklüğü, birincil bayi kapasitesi) değişirse etki zayıflayabilir; 2026'da 10 işlemde ortalama +20 bp (zayıfladı mı izlenmeli). Veri: Yahoo dağıtım düzeltmeli (TMV/TBT dağıtımları Nasdaq verisinde yoktu).
- Betik: `kod/ajan_tahvil_doviz/strateji_S1_ihale_oncesi.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| TLT — eşzamanlı, öncü değil | `NASDAQ:TLT` | -0.99 | -2.03 |
| ABD 30 yıllık getiri değişimi (yüzde puan; beta = getiri/1 puan) — eşzamanlı, öncü değil | `TVC:US30Y` | 0.96 | 0.31 |
| ABD 10 yıllık getiri değişimi (yüzde puan) — eşzamanlı, öncü değil | `TVC:US10Y` | 0.90 | 0.25 |
| IEF (7-10 yıl) — eşzamanlı, öncü değil | `NASDAQ:IEF` | -0.90 | -3.52 |
| LQD (yatırım yapılabilir kredi) — eşzamanlı, öncü değil | `AMEX:LQD` | -0.89 | -3.12 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| 10Y Hazine ihale takvimi: A-3 kapanışı → A-1 kapanışı penceresi | yok (takvim: TreasuryDirect 'Upcoming Auctions' / TradingView Ekonomik Takvim '10-Year Note Auction') | takvim olayı (önceden bilinir; gecikmeli öngörü) | t+1..t+2 (A-2, A-1) | TBT brüt +82 bp / pencere (t 3.79); TLT −41 bp | 3.8 (2.2/1.9) | net +62 bp/işlem (2.500 $; t=2.87) — strateji B6 | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Ultra T-Bond vadeli (CBOT) | `CBOT:UB1!` | TLT'nin süresine en yakın vadeli; CME Globex Pazar-Cuma neredeyse 23 saat (kış TR 02:00 → ertesi gün 01:00, 01:00-02:00 ara; yaz saatinde bir saat erken). TR 12:00-17:30 arasında TLT/TMV açılış boşluğunu önceden gösterir — öncü değil, izleme aracı. |
| 30 yıllık T-Bond vadeli (CBOT) | `CBOT:ZB1!` | UB1! ile aynı saatler; daha likit. |
| 10 yıllık T-Note vadeli (CBOT) | `CBOT:ZN1!` | Faiz piyasasının en likit vadelisi; ABD veri açıklamaları (TR 16:30) anında tepki. |
| ABD 30 yıllık getiri | `TVC:US30Y` | TLT ile eşzamanlı korelasyon −0,97; Asya/Avrupa saatlerinde de kotasyon. |
| ABD 10 yıllık getiri | `TVC:US10Y` | Genel faiz yönü; CPI/NFP (TR 16:30) tepkisi açılıştan önce görülür. |
| Almanya 10 yıllık getiri | `TVC:DE10Y` | Avrupa seansında (TR ~10:00-19:00) küresel faiz hareketi; ABD açılışından önce. |
| Japonya 10 yıllık getiri | `TVC:JP10Y` | Asya seansında (TR ~03:00-09:00) küresel uzun vade baskısı (BoJ). |

## 3. Takvim ve olay riskleri

10 Kas 2026 Sal: 10Y ihale (13:00 ET=TR 21:00) + CPI (TR 16:30) aynı gün; 11 Kas Çar Veterans Day (tahvil nakit piyasası kapalı, NYSE açık: ince işlem); 12 Kas Per 30Y ihale; 26 Kas NYSE kapalı, 27 Kas erken kapanış 13:00 ET (TR 21:00); 4 Ara Cum NFP (8 Ara ihale penceresinin içinde: tarihsel olarak etki daha büyük ama oynak); 8 Ara Sal 10Y yeniden ihraç; 9 Ara Çar FOMC (SEP; TR 22:00); 10 Ara Per 30Y + CPI; 24 Ara erken kapanış, 25 Ara kapalı. TMV/TBT çeyreklik dağıtım ex-date'leri ~Mar/Haz/Eyl/Ara 20-25'i (B6 penceresine denk gelmez).

## 4. Notlar

Fiyat/faiz/kredi/risk öncüleri arasında doğrulanmış gecikmeli öncü YOK: TBT için 18-19 aday × h∈{1,3} (kendi gecikmesi kontrollü, NW) içinde BH-FDR (224 testlik izleme seti) geçen 0; en güçlüsü DGS10_d (h3) t=2.30, +35 bp/sd. leadlag_sweep'te de bu hedef için FDR'li öncü yok. Tek gecikmeli öngörücü TAKVİM: 10Y ihale öncesi pencere (B6). Eşzamanlı sürücüler (30Y/10Y getiri, IEF, LQD) öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_tahvil_doviz.md`, `notlar/denetim_tahvil_doviz.md`.*
