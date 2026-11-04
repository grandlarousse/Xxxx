# Kapanıştan kapanışa, 1–3 gün tutan VİOP yatırımcısı için pratik liste (04.11.2026)

**Profil:** Gün içinde işlem yok. Karar BIST kapanışında (18:00–18:15 TSİ) veriliyor, VİOP'ta pozisyon açılıp 1–3 gün taşınıyor. Bir sinyalin bu profilde kullanılabilmesi için iki şart var:
1. Sinyal en geç 18:10'da (spot kapanış seansı sonu) bilinmeli.
2. Kazanç VİOP uzlaşmasından uzlaşmaya oluşmalı.

**Yöntem:** Önceki çalışmadaki bütün adaylar bu kuralla yeniden test edildi (~130 bin test). Ayakta kalanlar bağımsız kodla ikinci kez çürütülmeye çalışıldı. Ayrıntılar `notlar/` altında.

Yatırım tavsiyesi değildir. Bütün kenarlar küçüktür ve geçmiş veriye dayanır. Gerçek parayla işlem yapmadan önce en az 2–3 ay ileriye dönük (kâğıt üstünde) izlemek gerekir.

## 1. Ayakta kalanlar

| # | Sinyal | Kural (özet) | TradingView | Beklenti (doğrulama sonrası) | Uygunluk / güven |
|---|---|---|---|---|---|
| 1 | **XU030 vadelisi kapanış bazı sıçraması** | 18:10'da spot kapanışı çıkar. b = ln(XU030 vadeli son fiyat / XU030 spot kapanış). Δb = b − dünkü b (aynı vade). Δb kendi 120 günlük std'sinin 1 katını (~50 bps) aşarsa ters yönde işlem açılır: vadeli ucuz kapandıysa AL, pahalıysa SAT. 18:15'e kadar girilir, **ertesi gün uzlaşmada** kapatılır. | BIST:XU030, BIST:XU030D1! | Yılda ~65 işlem; son fiyattan girişte brüt +25 bps, uzlaşmadan +19; ~5 bps maliyetle net ~+14…+20 bps/işlem. IS +24, OOS +25 (t 1,85); 2024–26 +17 (t 1,1), yani zayıflıyor. En iyi 10 işlem çıkınca +12 (t 1,6). Alım tarafı daha sağlam. | **UYGUN / ORTA** |
| 2 | **SAHOL/AKBNK oranının ortalamaya dönüşü** | S = Σ(r_SAHOL − β·r_AKBNK); β 250 günlük ve 1 gün gecikmeli. z = (S − ort60)/std60. z > +1,5 → F_SAHOL SAT, F_AKBNK AL. z < −1,5 → tersi. Kapanışta hesaplanır, aynı akşam uzlaşmadan girilir. \|z\| ≤ 1,5 olunca uzlaşmadan çıkılır. Kontrat oranı N_AKBNK = N_SAHOL·β·F_SAHOL/F_AKBNK (bugün ~0,88; pratikte 1:1). | BIST:SAHOL1!, BIST:AKBNK1! | Yılda ~18 işlem. Tutma süresi medyan 2, ortalama 3,8 gün; işlemlerin %10'u 11 günü aşıyor. Raporlanan net +64–70 bps; gerçekçi beklenti işlem başına **+30–50 bps**. 2021–22'de çalışmadı; en büyük düşüşten çıkış ~23 ay sürdü. 3 güne zorla sınırlamak sonucu bozuyor. | **KOŞULLU / ORTA** |
| 3 | **Koza grubu göreli momentumu (TRMET)** | u = r_TRMET − β·ort(r_TRALT, r_TRENJ). z3 = son 3 günün u toplamı / (σ60·√3). z3 > +1,5 → TRMET1! AL ve ~0,7×TRALT1! SAT. z3 < −1,5 → tersi. 2 gün tutulur. | BIST:TRMET1!, BIST:TRALT1! (BIST:TRENJ yalnız girdi) | Uzlaşmadan girişte h2 +45 bps (t 4,05); ertesi gün girişte +30 (t 2,6), 8/8 yıl. 2024–26 +21 (t 1,2), yani zayıflıyor. Yaklaşık 120 bağımsız olay. Mekanizma belirsiz; kurumsal olay riski yüksek (TMSF, birleşme). | **KOŞULLU / ORTA** |
| 4 | **ABD rafinerileri → TUPRS** | P = ort(VLO, MPC, PSX, PBF) − β·S&P500, ABD'nin dünkü (t-1) günü. z = P / 250 günlük std. \|z\| > 1 → F_TUPRS z yönünde t uzlaşmasında açılır, **t+2 uzlaşmasında** kapatılır. | NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF, SP:SPX, BIST:TUPRS1! | Yılda ~53 işlem; net +42 bps (8 bps maliyetle, t 2,7), 15 bps maliyetle +35. 2024–26 +26 (t 1,0). En iyi 10 işlem çıkınca t 1,45. Sepet PBF'ye bağımlı. | **KOŞULLU / ORTA** |

**Düşük güvenli, yalnız küçük boyutla izlenebilecekler:**
- **Altın → TRALT:** VİOP altınının o günkü değişimi (18:00'e kadar). TRALT − β·XU030 hedge'li, 2 gün tutulur. Yalnız altın rallisi dönemlerinde çalışıyor (2019–20, 2025–26). DÜŞÜK.
- **ASX:FMG + ASX:BHP → EREGL:** Hedge'li, 3 gün. OOS t 0,9; 2022–23'te negatif. DÜŞÜK.
- **Kredi notu kademe kararı sonrası ters pozisyon:** Tepki gününün F_XU030 uzlaşmasında kararın tersine girilir, 2 gün tutulur. n=16, yılda 1–2 olay; son iki olay kaybettirdi. DÜŞÜK.
- **Ay dönümü:** Ayın son VİOP günü XU030D1! uzlaşmasında AL, ertesi gün SAT. Kazanç yalnız 2020–23 rejiminde. DÜŞÜK.
- **VİOP USDTRY 5 günlük değişimi → THYAO:** Kazancın kaynağı vadeli kurun taşıma eğilimi; drift düzeltilince 2024–26 t 0,8. ÇOK DÜŞÜK.
- **Yürütme ipucu (strateji değil):** Pay vadelisi kapanışta spota göre pahalıysa satışı öne al, alışı ertele; ucuzsa tersi. Getirisi ~5–10 bps.

## 2. Bu profil için elenenler

| Grup | Neden |
|---|---|
| ABD vadelisi, TUR, Brent, gece altını, TKC → açılış gap'i | Bilgi BIST kapanışından sonra geliyor ve ertesi açılışta fiyatlanıyor. Kapanıştan kapanışa yatırımcı bu hareketi zaten yaşamış oluyor. |
| Sektör emsallerinin gün içi öncülüğü (havayolu, TKC→TCELL, bira, Avrupa çeliği, savunma) | Yansıma t gününün içinde bitiyor. Ertesi kapanışa kalan kısım 8–26 bps, t ≤1,5. TUPRS ve EREGL istisna (yukarıda). |
| Tavan/taban sonrası | Olay günlerinin %83'ünde VİOP da limitte kilitli; dolum yok. |
| Hisse kapanış müzayedesi dönüşü | VİOP uzlaşması müzayede hareketinin yalnız ~%50'sini izliyor ve fark ertesi gün aynı yönde kapanıyor. |
| Temettü öncesi yükseliş | Yalnız spotta var; VİOP vadesi temettüyü önceden fiyatlıyor. Çürütmede DÜŞÜK. |
| Genel çift dönüşleri (bankalar, THYAO–PGSUS…), KCHOL NAV, TCELL–TTKOM | Maliyet sonrası ≈0 ya da çürütmede düştü. |
| Bayram/tatil, endeks dönem değişikliği | Sinyal yok. |
| FOMC / ABD istihdam / ABD TÜFE günleri | Bu günlerde 1–3 günlük risk artmıyor. Pozisyon küçültmeye gerek yok; bu bir "hiçbir şey yapma" bilgisi. |
| Akşam seansı hareketi | Ertesi gün için öngörü yok (corr −0,04). |

## 3. Önceki çalışmadaki korelasyonlardan pratikte işe yarayanlar

Bunlar alfa değil, risk aracıdır.
- **XU030 betası:** Medyan 0,89; bankalar 1,07–1,20; TUPRS 0,63.
  - Hisseye özgü bir görüşü taşırken piyasa riskini atmak için, pozisyonu açtığın uzlaşmada β×nominal kadar BIST:XU030D1! sat ve pozisyonu kapatana kadar tut.
  - Bu, 1–3 günlük varyansı medyan ~%41–44 azaltıyor. İyi çalıştığı hisseler: bankalar, SAHOL, KCHOL, THYAO, PGSUS, TCELL.
  - **TUPRS, PETKM ve ASELS'te XU030 hedge'i işe yaramıyor, hatta gece riskini artırıyor.**
- **Rutin gece hedge'i yapma:** Gece riski toplam 1–3 günlük riskin yalnız ~%11'i. Riskin büyük kısmı gün içinde, yurt içi haber ve akışla oluşuyor. Her akşam hedge açıp sabah kapatmak gece başına ~5–8 bps maliyet getirir.
- **TRALT/TRMET ↔ altın:** İkinci hedge bacağı olarak VİOP ons altın kullanılabilir (BIST:XAUUSD1!). β rejime bağlı: 2025'te ≈0, 2026'da 0,5–0,8.
- **Korelasyon kümeleri:** AKBNK, GARAN, YKBNK, ISCTR, SAHOL ve TSKB'nin ortalama korelasyonu 0,83. Hepsinde birden pozisyon tek bir büyük bahistir. Aynı mantık şu kümeler için de geçerli: THYAO+PGSUS(+TAVHL), KCHOL+SAHOL, TRALT+TRMET, TCELL+TTKOM, EREGL+KRDMD, FROTO+TOASO. Küme içindeki long/short çifti doğal hedge'tir ve teminat kredisi alır.
- **Boyut:**
  - 3 günlük taşımada, 1 günlük 1σ'ya göre hesaplanan kontrat sayısının ~0,57'sini kullan.
  - Kilit riski olan hisselerde (GUBRF, ASTOR, TKFEN, SASA, HALKB, BRSAN, VESTL, HEKTS) %99 kuyruğa göre boyutlan.
  - Hafta sonuna ~%11 küçülterek gir.
  - Teminat bağlayıcı kısıt değil (sermayenin %4–8'i). Bağlayıcı olan risk; kaldıraç tuzağına dikkat.
- Hisse bazındaki rakamlar: `risk_ve_boyut_tablosu.csv` (β, 1/2/3 günlük σ ve kuyruklar, limit günleri, teminat, 1 mn TL / %1 risk için kontrat sayısı, küme).

## 4. Günlük kullanım

- `kod/sinyal.py`: SAHOL/AKBNK z-skoru, sinyal ve kontrat oranı. Yalnız pandas, numpy ve requests gerektirir; kapanıştan sonra çalıştırılır.
- `kod/sahol_akbnk_z.pine`: TradingView Pine v5 göstergesi. **TradingView'da derlenip test edilmedi**; ilk kullanımda betiğin z-skoruyla karşılaştırın.
- 03.11.2026 kapanışında SAHOL/AKBNK z = −0,33, sinyal yok. 04.11 kapanışı için tetikler (diğer hisse sabitken):
  - Short spread: SAHOL ≥ 86,08 ya da AKBNK ≤ 58,35.
  - Long spread: SAHOL ≤ 80,16 ya da AKBNK ≥ 64,94.

## 5. Nerede bozulur?

- **Zayıflama:** Dört adayın dördü de son dönemde (2024–26) zayıflıyor. Kenarlar, yapanlar çoğaldıkça erir.
- **Maliyet:** Bireysel komisyonla (bacak başına ~22 bps) SAHOL/AKBNK ve TUPRS kenarının yarısı gider. Piyasa emri kullanmayın; limit emirle uzlaşma penceresinde girin.
- **Kurumsal olaylar:** Sabancı–Akbank payı ya da Koza grubundaki TMSF/birleşme kararları ilişkiyi tek günde bozabilir.
- **Kapasite:** XU030 bazı sinyali için 18:10–18:15 arasındaki 5 dakikada ekran başında olmak gerekiyor.
- **Veri notu:** Risk çalışmasında bir ajan akşam seansı fiyatlarını TradingView'ın iç websocket'inden, izin verilmemiş bir yöntemle çekmişti. O veri ve ondan türetilen akşam saatine özgü hedge sütunları silindi; bu tabloda yoktur. Kalan rakamlar Borsa İstanbul VİOP bülteni ve Yahoo verisine dayanıyor.
