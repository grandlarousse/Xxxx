# ABD net liste: neyi izle, neyi bekle, neyi at (9 Kasım 2026 haftası)

_Hazırlanma: Pazar 08.11.2026, ~01:00 TSİ. Kapsam: `abd_hafta_hazirlik.md` (HAZ) §4'teki 38 kalemin hepsi (35 hisse + 3 ETF). Kurallar `PLAN_ABD.md`'den (PLAN), günlük uygulama `ABD_GUNLUK_RUTIN.md`'den (RUTİN), rejim okuması `tarama/abd_rejim_20261106.md`'den (RJ). Kısaltmalar PLAN'ın kaynak tablosundaki gibi (TEST, KEN, KIM, DLG, PRA, VA, VD, VP). Doğrulama dosyaları raporlarla çelişirse doğrulama geçerlidir. Fiyat ve 52H uzaklıkları 5.11 kapanışıdır (HAZ §4). [hesap] = bu dosyanın kendi hesabı, [Ö] = bu dosyanın önerisi (plan kuralı değil)._

## 0. Özet

- **Plan şu an KIRMIZI.** 05.11'de VIX/VIX3M 1,10'du ve bu değer son iki kapanışın içinde kaldığı için Cuma 06.11'de de KIRMIZI sürüyor (RJ). Canlı ABD girişi yok. İlk pilot en erken **Pt 16.11, 16:45–17:15 TSİ**. Pilot yakın bölgede açılacak (S&P/200 GHO 1,007 < 1,02): tek pozisyon, risk E'nin %0,25'i, AI dışı ve izinli küme (PLAN §2.6, §0 #2).
- **Tier A (5 isim, 4 küme):** BDX ya da EHC (sağlık; aynı anda yalnız biri), TW, ACGL, MAR. Yakın bölgede bunlardan **yalnız 1** açılır. Seçim PLAN §4.4 #6 sırasıyla yapılır: RS, sıkılık, pivota yakınlık.
- **Tier C (atılanlar):** CNC, KDP, MDT (Kasım için), XLV/IHI/XLP (işlem aracı değil, yalnız ölçüt).
- **Lead-lag:** Bu 38 isim için araştırmamızda doğrulanmış bir lead-lag yok. TradingView'de yalnız teyit ve risk grafikleri kurulur: rejim, küme RS'i, emsal bilanço takvimi, gece vadelisi (§4).
- **1–3 gün:** ABD'de bu ufukta yaşayan bir kenar bulunmadı. Plan S1/S2 swing kullanıyor ve ilk 3–4 seansı kısa işlem gibi yönetiyor (§3).

## 1. Tier A: rejim SARI olunca ilk pilot adayları

**Ortak emir kartı (bütün A'lar için aynı; PLAN §3.1–3.5, RUTİN):**
- **Giriş:** 16:45–17:15 TSİ arasında BUY STOP-LIMIT (DAY, yalnız normal seans) ve ekli GTC SELL STOP.
  - S1: tetik = pivot × 1,001; limit = min(tetik × 1,01; tetik + 0,3 × ATR14). En çok 5 seans her gün yeniden girilir. Kapanış pivot × 1,05'in üstündeyse kurulum iptal, kovalanmaz.
  - S2: tetik = sinyal günü tepesi × 1,001; emir 2 seans geçerli.
- **Stop:**
  - S1: son daralmanın dibi − %0,1.
  - S2: min(sinyal günü dibi; 20 GHO − 0,25 ATR) − %0,1.
  - Tetikten stopa mesafe **1,0–2,0 ATR ve ≤ %8** olmalı; değilse işlem yok.
- **Boyut:** adet = ⌊E × %0,25 / (limit − stop)⌋; pozisyon ≤ E'nin %7,5'i. E = 50k $ ise 1R = 125 $ (PLAN §5.4).
- **Çıkış:** Karar kapanış bloğunda verilir (00:30–01:00 ya da 08:00–09:00). Emir ertesi açılışta MOO olarak çalışır ve stopla aynı OCA grubundadır.
  - Başarısız işlem, ilk 3 seans: S1'de kapanış < pivot − 0,5 ATR, S2'de kapanış < sinyal günü dibi → tamamen çık.
  - +2R ya da 4. seansta ≥ +1R → yarısını sat (SARI).
  - +1,5R → stop başabaşa.
  - Kapanış < 20 GHO → tamamen çık. Hızlı hissede (ADR%20 ≥ %4 ya da girişten sonraki 10 seansta ≥ +3R) eşik 10 GHO.
  - 10. seansta kâr < +1R ve son 5 seansta yeni en yüksek kapanış yok → çık.
  - Bilançodan önceki son seansta MOC ile çık.
- **Ön filtre:** (a) son çeyrekte EPS ve gelir beklentiyi aşmış olmalı; (b) bilançodan sonraki 3 seans SPY'ye göre ≥ 0 olmalı (Nasdaq.com Earnings; PLAN §3.1).
- **Yön:** yalnız long (nakit hesap; açığa satış, opsiyon ve margin yok).

| Hisse · TV kodu (kod durumu) | Küme · ölçüt | HAZ §4 verisi | Beklenen kurulum | Yasak / tarih | TradingView teyit seti |
|---|---|---|---|---|---|
| **BDX** · `NYSE:BDX` (teyit et) | Sağlık süper-kümesi (K1 medtech) · IHI, XLV | 212,52; 52H −%1,1; YTD +%39,4; 1A +%16,3; bilanço 5.11 BMO, çöküş gününde zirve yakınında kaldı | S1 (pivot ≤ %3 ise); baz 15 seansı doldurmadıysa S2 | Sonraki bilanço Oca sonu–Şub 2027 (HAZ §4 genel notu; IR'den teyit et). Ön filtre (b) için seanslar 5, 6, 9.11 [hesap] | `NYSE:BDX/AMEX:IHI` ve `AMEX:IHI/SP:SPX` 50 GHO üstünde [Ö]. ABD_RJ korelasyon girdisi `AMEX:IHI`. Emsal: MDT 24.11 BMO |
| **EHC** · `NYSE:EHC` (teyit et) | Sağlık süper-kümesi (K3 hizmet) · IHF, XLV | 141,27; 52H −%1,5; YTD +%33,1; 200G ort.'nın %27,5 üstünde; bilanço 28.10 AMC | S1 | BDX ile aynı anda açılmaz (SARI'da sağlıkta 1 pozisyon; PLAN §4.5). CMS ya da düzenleyici karar tarihini IR'den kontrol et (ikili olay, PLAN §3.1) | `NYSE:EHC/AMEX:IHF` (IHF teyit et), `AMEX:XLV/SP:SPX` |
| **TW** · `NASDAQ:TW` (teyit et) | K4 borsalar · XLF | 127,56; 52H −%1,1; 3A +%24,3; bilanço 29.10 BMO | S1 | K4 + K5 toplam ısısı ≤ %1,25 (PLAN §5.1) | `NASDAQ:TW/AMEX:XLF` (XLF: CSV), `AMEX:XLF/SP:SPX`. Küme içi karşılaştırma: `NASDAQ:CME`, `CBOE:CBOE` (teyit et) |
| **ACGL** · `NASDAQ:ACGL` (teyit et) | K5 sigorta · XLF | 110,57; 52H −%2,7; 1A +%17,2; bilanço 27.10 AMC | S1 | Sigorta izninin dayanağı reasürans grubunun üstte olması (PLAN §4.3). Büyük afet haberini ikili olay say [Ö] | `NASDAQ:ACGL/AMEX:XLF`. Emsal: BRK-B bilançosu 07.11, ilk tepki Pt 9.11 |
| **MAR** · `NASDAQ:MAR` (CSV) | K8 konaklama · XRT | 417,28; 52H −%3,7; YTD +%34,5; 3.11'de 52H listesinde; bilanço 2.11 BMO | S1 | Tetik FTD ya da S&P 10 > 20. Yakın bölge bitince açılır [Ö], çünkü PLAN §0 #2 pilotu savunmacı kümeden istiyor | `NASDAQ:MAR/AMEX:XRT` (XRT: CSV), `AMEX:XRT/SP:SPX`, `NASDAQ:MAR/NYSE:HLT` (teyit et). Tüketici emsalleri 17–19.11 (§4c) |

- **Neden bu beşi:**
  - Hepsi PLAN §4.5'in "nitelikli aday" sınıfında: 52H'ye ≤ %5 uzaklar, uzamış değiller, kümeleri izinli, AI dışılar.
  - Her küme ayrı. SARI'da küme başına 1 pozisyon kuralına uyuyor.
  - Yedekler aynı kümeden: TMO ve RPRX (sağlık), CME (K4), MRSH (K5), HLT ve SN (K8).
- **Diğer usuller:**
  - BDX'te G1 bilanço gap'i yalnız gölge kayıtla izlenir. Önce 5.11'in 1. gün kriterleri teyit edilir: gap ≥ +%8, RVOL ≥ 3. Bu sağlanırsa 2.–5. gün 6, 9, 10 ve 11.11'dir [hesap].
  - Opsiyon, temettü ve çift işlemi hiçbir A'da yok (§5).
- **Faktör uyarısı:** Liste savunmacı ağırlıklı. NDX'te 10 > 20 kesişmesinden sonraki 20 seansta savunmacı sepet 2010 sonrasında piyasanın %0,66 gerisinde kaldı; olayların %60'ı negatif (PLAN §4.2 [H]).
- **Dürüst beklenti:** S1'de işlem başı E[R] −0,2R ile +0,4R arası, merkez +0,1R (PLAN §3.2). S2'de −0,1R ile +0,3R arası (PLAN §3.3).

## 2. Bütün liste (38 kalem)

**Kod durumu:**
- **CSV:** `2026-11-02_viop_leadlag/tradingview_kodlari.csv` içinde DOGRULANDI_2KEZ.
- **teyit et:** CSV'de yok; borsa öneki bu dosyanın tahmini.
- Hisse kartı ve izleme listesi dosyaları yalnız 47 VİOP dayanağını kapsıyor; bu isimlerin hiçbiri orada yok.

**Oran grafiklerinde payda:** `SP:SPX` (CSV). HAZ §5c'deki `AMEX:SPY` de kullanılabilir (teyit et).

**ETF kodları:** CSV'de yalnız `AMEX:XLF`, `AMEX:XRT`, `AMEX:XLP` var. Tablodaki diğer ETF kodlarının hepsi teyit et: `AMEX:XLV`, `AMEX:IHI`, `AMEX:IHF`, `NASDAQ:IBB`, `AMEX:XLRE`, `AMEX:XLU`, `AMEX:IGV`, `NASDAQ:QQQ`. Satırda ayrıca yazılmamış olsa da bu kural geçerli.

**ABD_RJ satırları** (PLAN §2.7; betik derlenmedi). Her hissede aynı eşikler okunur:
- TT = EVET.
- RS / 52H ≥ 0,97 (S1) ya da ≥ 0,95 (S2).
- 52H zirveye uzaklık ≥ −%10; S1'de ≤ −%5 tercih edilir.
- ADR%20 ≥ 2.
- "UZAMIS" yazmıyor (1A ≥ +%25 ya da 3A ≥ +%40 ise uzamış sayılır).
- 50 günlük dolar hacmi ≥ 20 mn $.
- Korelasyon girdisi küme ETF'i olur.

| # | Hisse · TV kodu | Kod | Küme (PLAN §4.2) | Tier | HAZ §4: 52H / not / son bilanço | Beklenen kurulum | Yasak / tarih | TV oran grafikleri |
|---|---|---|---|---|---|---|---|---|
| 1 | MDT · `NYSE:MDT` | teyit et | Sağlık (K1) | **C** (Kasım için) | −%2,7; 1A +%17,9 | — | Bilanço **24.11 BMO** (Medtronic IR; PLAN §4.5): 10.11'den itibaren giriş yok. Bilanço + 3 seans kuralı var; 25.11 ve 27.11 genel yasak → en erken ~30.11 [hesap] | Aralıkta yeniden bak: `NYSE:MDT/AMEX:IHI`. 24.11'i medtech emsal okuması olarak izle |
| 2 | EW · `NYSE:EW` | teyit et | Sağlık (K1) | B | −%3,2; 1A +%17,5; 4.11 AMC bilançosundan sonra zirvede | G1 yalnız gölge (1. gün 5.11; 2.–5. gün 6–11.11 [hesap]); sonra S2 ya da yeni baz | — | `NYSE:EW/AMEX:IHI` |
| 3 | BDX | — | Sağlık (K1) | **A** | §1 | §1 | §1 | §1 |
| 4 | GEHC · `NASDAQ:GEHC` | teyit et | Sağlık (K1) | B | −%6,7; 1A +%29,5 → uzamış; 28.10 BMO | Yalnız S2 | — | `NASDAQ:GEHC/AMEX:IHI` |
| 5 | TMO · `NYSE:TMO` | teyit et | Sağlık (K1 araçlar) | B (sağlık yedeği) | −%4,8; 6A +%45,8; 21.10 BMO | S1 | — | `NYSE:TMO/AMEX:XLV` |
| 6 | REGN · `NASDAQ:REGN` | teyit et | Sağlık (K2) | B (düşük öncelik) | −%9,8; 1A +%21; 30.10 BMO | Baz yok; yeni baz oluşursa S1 | PDUFA ve kongre tarihlerini IR'den kontrol et (PLAN §3.1) | `NASDAQ:REGN/NASDAQ:IBB` (IBB teyit et) |
| 7 | LLY · `NYSE:LLY` | teyit et | Sağlık (K2) | B | −%7,1; 1A +%15,4; 29.10 BMO | 17.11'den sonra yeni baz oluşursa S1 | ObesityWeek 14–17.11 ikili olay: **17.11'e kadar giriş yok** (PLAN §4.5) | `NYSE:LLY/AMEX:XLV` |
| 8 | RPRX · `NASDAQ:RPRX` | teyit et | Sağlık (K2) | B (sağlık yedeği) | −%3,6; YTD +%74; 4.11 BMO | S1 | Ön filtre (b) için seanslar 4, 5, 6.11 [hesap] | `NASDAQ:RPRX/AMEX:XLV` |
| 9 | CNC · `NYSE:CNC` | teyit et | Sağlık (K3, yönetilen sağlık) | **C** | −%5,9; 4.11'de tek günde +%12,6 | — | **Faz 1'de evren dışı** (PLAN §3.1; KT1 #5) | — |
| 10 | EHC | — | Sağlık (K3) | **A** | §1 | §1 | §1 | §1 |
| 11 | IDXX · `NASDAQ:IDXX` | teyit et | Sağlık (K1) | B | −%12,9 (S1 için > %10 uzak); 2.11'de beat & raise ile +%21,9 | Yalnız S2. G1 penceresi 6.11'de kapandı (PLAN §4.5) | — | `NASDAQ:IDXX/AMEX:XLV` |
| 12 | CBOE · `CBOE:CBOE` | teyit et | K4 | B | −%4,9; 1A +%25,4 → uzamış; 30.10 BMO | Yalnız S2 | VIX düşerse geride kalabilir (PLAN §4.2) | `CBOE:CBOE/AMEX:XLF`; `CBOE:VIX` (CSV) |
| 13 | CME · `NASDAQ:CME` | teyit et | K4 | B (K4 yedeği) | −%4,8; 3A +%16,5; 21.10 BMO | S1 | — | `NASDAQ:CME/AMEX:XLF` |
| 14 | TW | — | K4 | **A** | §1 | §1 | §1 | §1 |
| 15 | AJG · `NYSE:AJG` | teyit et | K5 | B | −%2,2; 1A +%26,9 → uzamış; 29.10 AMC | Yalnız S2 | — | `NYSE:AJG/AMEX:XLF` |
| 16 | MRSH · `NYSE:MRSH` | teyit et | K5 | B (K5 yedeği) | −%2,1; 1A +%20,6; 15.10 BMO | S1 | — | `NYSE:MRSH/AMEX:XLF` |
| 17 | ACGL | — | K5 | **A** | §1 | §1 | §1 | §1 |
| 18 | BRK-B · `NYSE:BRK.B` | teyit et | K5 | B | −%3,7; düşük oynaklık | S1, yalnız ADR%20 ≥ 2 ise | Bilanço Ct 07.11 (sonucu dosyalarda yok). İlk tepki 9.11; ön filtre (b) en erken 11.11 kapanışında (PLAN §4.5) | `NYSE:BRK.B/AMEX:XLF` |
| 19 | KDP · `NASDAQ:KDP` | teyit et | K6 temel tüketim | **C** | −%4,0; 3A +%23,9; 3.11 BMO | — | **İzinsiz** (XLP skorda 6.; PLAN §4.3, KT2 #12) | İzin 28–29.11'de değişirse: `NASDAQ:KDP/AMEX:XLP` |
| 20 | BJ · `NYSE:BJ` | teyit et | K6 (faiz duyarlı süper-küme) | B | −%1,8; YTD +%23,6 | 25.11 kapanışından sonra S1 | Bilanço **20.11 BMO**. Giriş en erken 25.11 kapanışından sonra (PLAN §7.2); 25 ve 27.11 genel yasak → pratikte ≥ 30.11 [hesap] | `NYSE:BJ/AMEX:XLP`. Emsal: WMT 19.11 BMO |
| 21 | CCI · `NYSE:CCI` | teyit et | K10 REIT (faiz duyarlı) | B | −%4,3; 1A +%31,8 → uzamış; 21.10 AMC | Yalnız S2 | REIT izni teyitsiz (PLAN §4.3). 10.11 CPI | `NYSE:CCI/AMEX:XLRE` (teyit et); `TVC:US10Y` (CSV) |
| 22 | PSA · `NYSE:PSA` | teyit et | K10 | B | −%1,6; 1A +%20,8; 26.10 AMC | S1, yalnız ADR%20 ≥ 2 ise | REIT izni teyitsiz | `NYSE:PSA/AMEX:XLRE`; `TVC:US10Y` |
| 23 | RSG · `NYSE:RSG` | teyit et | K7 atık (faiz duyarlı) | B | −%2,0; 3A +%16,3; 29.10 AMC | S1, yalnız ADR%20 ≥ 2 ise | Atık kümesi izinli | `NYSE:RSG/SP:SPX`; `TVC:US10Y` |
| 24 | VLTO · `NYSE:VLTO` | teyit et | K7 | B | −%2,7; 3A +%19,3; 29.10 AMC | S1, yalnız ADR%20 ≥ 2 ise | — | `NYSE:VLTO/SP:SPX` |
| 25 | AWK · `NYSE:AWK` | teyit et | K7 su | B | −%0,8; 1A +%19,7; 28.10 AMC | S1, yalnız ADR%20 ≥ 2 ise | Faiz duyarlı süper-küme: 18.11'de WMT/TGT öncesi giriş yok (PLAN §7.2) | `NYSE:AWK/AMEX:XLU` (teyit et); `TVC:US10Y` |
| 26 | MAR | CSV | K8 | **A** | §1 | §1 | §1 | §1 |
| 27 | HLT · `NYSE:HLT` | teyit et | K8 | B (K8 yedeği) | −%3,1; YTD +%28,6; 27.10 BMO | S1 | — | `NYSE:HLT/AMEX:XRT` |
| 28 | SN · `NYSE:SN` | teyit et | K8 | B | −%3,6; YTD +%94; 4.11 BMO | S1 ya da G1 yalnız gölge (1. gün 4.11; 2.–5. gün 5–10.11 [hesap]) | — | `NYSE:SN/AMEX:XRT` |
| 29 | HAS · `NASDAQ:HAS` | teyit et | K8 | B | −%3,6; 1A +%31,7 → uzamış; 20.10 BMO | Yalnız S2 | — | `NASDAQ:HAS/AMEX:XRT` |
| 30 | EBAY · `NASDAQ:EBAY` | teyit et | K8 | B | −%3,8; YTD +%41,2; 28.10 AMC | S1 | Perakende emsalleri 17–19.11 (§4c) | `NASDAQ:EBAY/AMEX:XRT` |
| 31 | AAPL · `NASDAQ:AAPL` | CSV | K11 mega-cap | B (YEŞİL'i bekler) | −%4,0; 5.11'de XLK −%8 iken ~−%1,5; 2.11 AMC | YEŞİL rejimde S1/S2 | NDX rejimine bağlı. BIST'teki AAPL varantı (HAZ §0 #8) opsiyon niteliğinde; Faz 1'de yok [Ö] | `NASDAQ:AAPL/NASDAQ:QQQ` (teyit et); `NASDAQ:NDX` 10/20 GHO (teyit et) |
| 32 | ROP · `NASDAQ:ROP` | teyit et | K9 dikey yazılım | B | −%3,2; 1A +%36,9 → uzamış; 22.10 BMO | Yalnız S2 | K9 izni teyitsiz. NDX 10 > 20 tek başına yalnız K9'u açar (PLAN §2.2). Emsal: PANW 18.11 AMC, INTU 19.11 AMC | `NASDAQ:ROP/AMEX:IGV` (teyit et) |
| 33 | MANH · `NASDAQ:MANH` | teyit et | K9 | B | −%3,2; 3A +%30,7; 27.10 AMC | S1 | K9 izni teyitsiz | `NASDAQ:MANH/AMEX:IGV` |
| 34 | U · `NYSE:U` | teyit et | K9 | B (yalnız gölge) | −%2,3; 5.11 bilançosuyla haftada +%35; 200G ort.'nın %60,7 üstünde | G1 yalnız gölge (1. gün 5.11; 2.–5. gün 6–11.11 [hesap]); sonra S2 | K9 izni teyitsiz | `NYSE:U/AMEX:IGV` |
| 35 | GEN · `NASDAQ:GEN` | teyit et | K9 | B | −%3,3; 1A +%36,7 → uzamış; 28.10 AMC | Yalnız S2 | K9 izni teyitsiz | `NASDAQ:GEN/AMEX:IGV` |
| 36 | XLV · `AMEX:XLV` | teyit et (PINE varsayılanı) | Sağlık ölçütü | **C** (işlem) / ölçüt | Skor #1 (19,2; HAZ §5c) | — | Plan ETF almıyor (PLAN §6.1). Sektör ETF rotasyonunun swing ufkunda kenarı yok: 40 varyantın 40'ı negatif (VD U7) | `AMEX:XLV/SP:SPX` 50 GHO üstünde = sağlık kümesi güçlü |
| 37 | IHI · `AMEX:IHI` | teyit et | Medtech ölçütü | **C** / ölçüt | Skor #2; 1A +%15,9 | — | Aynı | `AMEX:IHI/SP:SPX` |
| 38 | XLP · `AMEX:XLP` | CSV | Temel tüketim ölçütü | **C** / ölçüt | Skor #6, yani K6'da izin şartı (a) sağlanmıyor | — | Aynı | `AMEX:XLP/SP:SPX` |

- **Faiz duyarlı süper-küme tek küme sayılır:** BJ, RSG, VLTO, AWK, CCI, PSA. Isı tavanı ≤ %0,75; ADR%20 < %2 olan dışarıda kalır (PLAN §4.2, §4.5).
- **HAZ §4'ün baştan dışarıda bıraktıkları da C:**
  - SGRY, BRZE: birleşme arbitrajı profili.
  - APP, NET: zirveye uzak.
  - Enerji: 50 GHO kırıldı.
  - Altın madencileri.
  - Çip ve AI altyapısı: dönüş kuralı PLAN §4.6.

## 3. 1–3 gün sorusu: Türkiye'de yerleşik biri için dürüst cevap

**Kısa cevap:** ABD'de 1–3 günlük kapanıştan kapanışa işlem için araştırmamızda yaşayan bir kenar yok. VİOP'taki 1–3 günlük işlemlerin ABD karşılığı yok.

- **Kısa vade reversal öldü.**
  - 2010–2026'da brüt +%0,1/yıl (t 0,04); 10 bp maliyetle −%4,2/yıl. 2020–26'da −%5,2/yıl (TEST §7).
  - Günlük reversal 2010 sonrasında brüt %5,6/yıl yapıyor, ama günlük tam devirle uygulanamıyor (TEST §7). KEN §5'in hükmü: "Öldü".
- **PEAD büyük hissede yok.**
  - 2006'dan beri yok (Martineau; VA #23 DOĞRU).
  - Kazanç sinyallerinin sadece-uzun üst portföyü 2010–25'te değer ağırlıklı piyasayı geçmedi (TEST §0 #8).
- **Takvim etkileri bitti.** Pre-FOMC drift 2015'ten sonra yok, ay dönümü etkisi öldü, bayram öncesi etkisi önemsiz (KEN §5).
- **Kâr gece oluşuyor.** Momentum kârının neredeyse tamamı overnight oluşuyor (Lou-Polk-Skouras; KEN §3.1). Pozisyon geceyi taşımalı, ama yalnız-gece al-sat maliyeti kenarı yiyor.
- **Saat sorunu:**
  - ABD seansı 17:30–00:00 TSİ. BIST kapanışındaki karar anı (18:00) ABD seansının 30. dakikasına denk geliyor (HAZ §0 #8).
  - Plan 17:30–00:00 arasında emir değiştirmeyi kritik ihlal sayıyor (RUTİN).
  - Bu yüzden 1–3 günlük işlem iki yoldan biri demek: ertesi açılışta MOO ile girip çıkmak (iki gece gap'i taşınır) ya da gece yarısına kadar ekranda kalmak.
- **Gap riski:**
  - Stres varsayımı korele bir gecede −%15. 2026'nın tek gün hareketleri: INTC −%30, AMD −%17,3, MU −%17,5 (PLAN §5.3).
  - 1–3 günlük küçük hedefte bu kuyruk risk/getiri oranını bozar [Ö].
- **İstisna adayı tek:** VIX > 25 olan aylarda reversal +%0,55/ay (n = 29; KEN §5). Ama ufku aylık, doğrulama dosyalarında teyidi yok ve planda yer almıyor. Yalnız not olarak duruyor.
- **Bu yüzden plan S1/S2 swing kullanıyor.** Kanıt, kazananların ortak yöntemine ve tekil hissedeki sağ kuyruğa dayanıyor (PLAN §3.0; VA #13–14, #18, #29).
- **1–3 güne en yakın parça S1/S2'nin ilk 3–4 seansı:**
  - İlk 3 seansta başarısız kırılım → MOO ile çık.
  - +2R ya da 4. seansta +1R → yarısını sat; kalan yarı trende bırakılır (PLAN §3.2, §3.5).

## 4. Lead-lag sorusu: dürüst cevap ve meşru TradingView kurulumları

**Bu 38 isim için doğrulanmış bir lead-lag kenarı YOK. TradingView'de "X öncüdür, Y'yi şu yönde al" diye bir kurulum veremem.**

- **Kapsam:** Lead-lag çalışması yalnız 47 VİOP dayanağını kapsıyor (`2026-11-02_viop_leadlag/RAPOR.md` başlığı); hisse kartları da yalnız onlar için var. ABD hisseleri hiç test edilmedi.
- **O çalışmanın kendi bulguları:**
  - Günlük hisse→hisse ve endeks→hisse öncülüğü yok (≈170 bin test, FDR 0).
  - ABD sürücülerinin "öncülüğü" saat farkından ibaret; açılıştan sonra kalıntı ≈ 0 (RAPOR "Dört hüküm", §2).
- **ABD tarafı:**
  - Kısa ufuktaki kenarlar ABD'de de bozulmuş (TEST §7).
  - Lead-lag tipi küçük kenarlar breadth, düşük maliyet ve kaldıraç ister; bunlar bireyde yok (KIM §2.3, §7.2).
  - Sektörün piyasayı öncülemesi zayıf ve kırılgan (DLG §2, Hong–Torous–Valkanov).
- **Elimizdeki tek ABD bağlantılı lead-lag ters yönde:** ABD rafinerileri → TUPRS (`2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` §1 #4). Bu 38 isimle ilgisi yok.

**Meşru kurulumlar.** Bunların hiçbiri kenar değil: "giriş izni var mı, yok mu" ve "risk ne" sorularını cevaplar. Yön her zaman yalnız long.

**(a) Rejim göstergesi.** `SP:SPX` (CSV) günlük grafiğine ABD_RJ (`kod/abd_rejim_ve_sablon.pine`) eklenir. Betik derlenmedi; ilk kullanımda 05.11 değerleriyle karşılaştır (PLAN §2.7).

| Grafik | Okuma (PLAN §2.2) |
|---|---|
| `CBOE:VIX/CBOE:VIX3M` (VIX: CSV; VIX3M HAZ §5d'de doğrulanmış, CSV'de yok → teyit et) | Son iki kapanıştan birinde ≥ 1,00 → KIRMIZI. İki kapanış üst üste < 1,00 ve S&P > 200 GHO → TURUNCU (en erken 10.11; RJ). < 0,95 → YEŞİL şartlarından biri ve G2 gölge tetiği |
| `SP:SPX` 10/20/50/200 GHO | 2 kapanış üst üste 200 GHO altında → KIRMIZI. S&P/200 GHO < 1,02 → yakın bölge; 1,02 için S&P ≈ 7.472 gerekir (RJ). 10 > 20 → K9 dışı kümelerin tetiği |
| `INDEX:S5FI`, `INDEX:S5TH` (HAZ §5d; teyit et) | S5FI < 50 **ve** S5TH < 60 → KIRMIZI |
| `NASDAQ:NDX` 10/20 GHO (PINE; teyit et) | SARI'da NDX 10 > 20 tek başına yalnız K9'u açar. YEŞİL'in şartlarından biri: NDX 10 > 20 ve ikisi de yükseliyor (bütün kümeler için). K11 (AAPL) YEŞİL'i bekler |
| `INDEX:MAHQ-INDEX:MALQ` (HAZ §5d; teyit et) | Bilgi: 5.11'de 150 − 490 = −340 |

**(b) Küme RS çizgileri.**
- İki oran grafiği: `HİSSE/ETF` (kümenin içinde önde mi?) ve `ETF/SP:SPX` (küme piyasanın önünde mi?). Kodlar §2 tablosunda.
- Plan kuralı ABD_RJ'nin "RS / 52H" satırı (hisse/SPX): S1 için ≥ 0,97, S2 için ≥ 0,95.
- ETF'e göre oran yardımcı bir sıralama aracı [Ö]: iki oran da 50 GHO'nun altındaysa isim aday listesinde geriye düşer.
- 60 günlük korelasyon ≥ 0,6 olan isimler aynı küme sayılır. İlk ölçüm 07–08.11'de, ABD_RJ korelasyon satırıyla yapılır (PLAN §4.1e, §4.2).

**(c) Küme içi emsal bilanço takvimi.** Bu bir olay filtresidir, kanıtlanmış kenar değil. Kaynaklar HAZ §4 ve PLAN §4.5 ile §7.

| Küme | Emsal olay (TSİ) | Planın kuralı | [Ö] |
|---|---|---|---|
| Sağlık | MDT 24.11 BMO | Yalnız MDT'nin kendisine yasak | Açık sağlık pozisyonu varsa 23.11 kapanışında gap-ayarlı ısıya bak |
| K5 sigorta | BRK-B 07.11; ilk tepki Pt 9.11 | BRK-B'de ön filtre (b) en erken 11.11 | 9.11'deki tepkiyi K5 notu olarak günlüğe yaz |
| Tüketici (K6, K8) | HD 17.11; TGT, TJX, LOW 18.11; WMT 19.11 BMO; ROST, GAP 19.11 AMC; BBY 24.11 BMO | 18.11: faiz duyarlı süper-kümede ve perakendede WMT/TGT öncesi yeni giriş yok | — |
| K9 yazılım | PANW 18.11 AMC, INTU 19.11 AMC | — | K9'da yeni girişi 19.11'den sonraya bırak |
| Endeks | CSCO, AMAT 12.11 AMC; NVDA 17.11 AMC (konferans 18.11 01:00 TSİ) | **17.11'de bütün kümelerde yeni giriş yok** | — |

**(d) Gece vadelileri.**
- `CME_MINI:ES1!` ve `CME_MINI:NQ1!` (CSV) yalnız gap ve risk bilgisi verir.
- Tek kural: veri günlerinde (CPI 10.11, PPI 13.11) 16:45'te S&P vadelisi önceki kapanıştan ±%1,5'ten fazla oynadıysa o gün yeni giriş yok (RUTİN §2 #1).
- Faiz duyarlı kümelerde `TVC:US10Y` (CSV) de aynı türden risk bilgisidir (PLAN §4.2).

## 5. Diğer usuller (ABD)

| Usul | Durum | Neden |
|---|---|---|
| G1 bilanço gap'i (2.–5. gün) | Yalnız gölge kayıt. Adaylar U, EW, SN, BDX | Büyük hissede PEAD yok (VA #23). Sadece-uzun bilanço üst portföyü piyasayı geçmiyor (TEST §6.4) |
| G2 VIX panik çözülmesi (SPY, 40 seans) | Yalnız gölge; 05.11'den beri kurulu | Piyasaya göre fark ~+1,8 puan, t ≈ 1,7, n = 25, örneklem içi (PLAN §3.0, §3.8) |
| Opsiyon | Faz 1'de kapalı; açmak kritik ihlal | Sistematik alım ortalamada kaybettirir (VP A6, A8). Açılma şartları PLAN §3.9'da: Faz ≥ 2, YEŞİL, VIX < 20, VIX/VIX3M < 0,90 |
| Temettü yakalama | Yok | ABD stopajı %20 (PLAN §1.1). PRA §1.3: "Swing trader için temettü önemsizdir" |
| Çift işlemi / açığa satış | Yok | Nakit hesap (PLAN §3.10) |
| Sektör ETF rotasyonu | Yalnız küme izni filtresi | 40 varyantın 40'ı negatif (VD U7) |
| Insider küme alımı | Ertelendi | Kanıt 1986–2007'den, yayın sonrası test yok (VA #26) |

## 6. Günlük takip: 3 soru (uzun liste yerine)

1. **Durum SARI ya da YEŞİL mi?** ABD_RJ'ye `SP:SPX` grafiğinde bakılır. Değilse o gün iş bitti (2 dk).
2. **Tier A'da hangi isim hazır?** ABD_RJ'de "S1 ön koşul | S2 lider" EVET olmalı, pivot ≤ %3 uzakta olmalı, stop 1,0–2,0 ATR ve ≤ %8 olmalı. Yakın bölgede yalnız 1 isim.
3. **Bugün yasak var mı?**
   - Genel yasak günleri: 17.11, 25.11, 27.11, 9.12.
   - 18.11'de giriş emirleri GTD olur ve 21:55'te düşer.
   - Hissede 10 seans içinde bilanço ya da ikili olay var mı?
   - Bu dosyadaki tarihler: MDT 24.11, BJ 20.11, LLY 17.11'e kadar.

## Pazartesi 9.11 için ABD kısa liste

1. Canlı ABD girişi yok (KIRMIZI). İlk pilot en erken Pt 16.11, 16:45–17:15, tek pozisyon.
2. Sabah: Cuma 06.11'in resmi VIX/VIX3M ve NDX kapanışlarını ABD_RJ ile teyit et; ilk kullanımda betiği 05.11 değerleriyle karşılaştır.
3. TradingView'de izleme listesi kur: BDX, EHC, TW, ACGL, MAR ve ölçütler `AMEX:XLV`, `AMEX:IHI`, `AMEX:XLF`, `AMEX:XRT`, `SP:SPX`, `CBOE:VIX/CBOE:VIX3M`. Her A için pivot, stop ve ATR çiz; kodları teyit et.
4. BRK-B'nin 07.11 bilançosuna ilk tepkiyi K5 notu olarak yaz. G1 gölge kaydı tut: U, EW, BDX (6–11.11) ve SN (5–10.11); 1. gün kriterlerini teyit et.
5. MDT'yi 10.11'den itibaren listeden çıkar. LLY'de 17.11'e kadar giriş yok. CNC ve KDP listede değil.
6. Hesap tarafı: E'yi ve dur eşiğini (−%8 E) yazılı belirle (PLAN §10; RJ). SWIFT sabah, önce küçük tutarla kur makası. Hesap fonluysa 1 adetlik IBKR emir testleri (PLAN §6.2); Midas yalnız ≤ 500 $ test. Opsiyon, margin ve kaldıraç yok.
