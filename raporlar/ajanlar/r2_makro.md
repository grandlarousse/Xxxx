# R2 — MAKRO çapraz kontrol | 28.10.2026

Etiketler: [D] doğrulandı · [H] benim hesabım · [V] varsayım. Birincil veri: Borsa İstanbul VİOP günlük bülteni 27.10 [B1].

## 1. Çelişki çözümleri

### 1a. Vadeli baz: iki taraf da haklı, farklı kararlar için
Değerler: S=13.961, F_XU0301226=14.644 (uzlaşma 14.638 [B1]), 64 gün. TLREF %35,8 brüt. Bireysel yatırımcının net nakit getirisi ~%29,5 [V: stopaj %17,5].

| Karar | 31.12 spot başabaşı | Kim haklı |
|---|---|---|
| (a) Long F mi, nakitte beklemek mi? | **14.644 (+%4,9)**. Nakit faizi her iki durumda da kazanılır; fark yalnızca S_T−F | ENDEKS ve ŞEYTAN. Yön kararları için geçerli olan bu |
| (b) Long F mi, spot hisse mi? | F+nakit, spottan **193 puan (%1,3)** üstün (vergisiz). Bireysel yatırımcıda yalnızca ~39 puan (%0,3) | Ben ve OPSİYON, yalnızca enstrüman seçimi için |
| (c) Spot hisse mi, nakit mi? | 14.837 (+%6,3) vergisiz; 14.683 (+%5,2) bireysel | Spot alıcının aşması gereken eşik daha yüksek |
| Teminat getirisi | Takasbank TL nakit teminatını nemalandırıyor. 5.000 TL alt sınırı var; Takasbank kesintisi ve stopaj düşülüyor [S1, ikincil] | Nema hiç olmasaydı maliyet 16,7 bin×%35,8×64/365 ≈ **105 puan** olurdu; bu, (b)'deki avantajı ~90 puana indirir. Nemalandırmayla maliyet ≈0 |

Sonuç: "ucuz" ifadesi hiçbir yön kararını değiştirmiyor; long vadeli başabaşı 14.644.

### 1b. USDTRY carry: kuyruk yeniden fiyatlandı [H, Yahoo TRY=X günlük kapanış, S2]
F0 = S0×(1+fark×64/365); fark o dönemin politika faizi − USD faizi [V].

| Şok | 64 günde spot | Maks. kapanış / gün içi | Kısa vadeli, stopsuz | Stoplu (F +%1,4, kapanışta) |
|---|---|---|---|---|
| Ağu 2018 (31.07 giriş) | +%23,1 | +%41 / +%44 | −%19,3 | −%3,4 |
| Ağu 2018 (09.08 giriş, şok öncesi gün) | +%6,6 | +%25 / +%27 | −%3,3 | **−%22,6 (gap)** |
| Kas–Ara 2021 | +%29,8 | +%61 / +%78 | −%26,5 | −%3,7 |
| Haz 2023 seçim sonrası | +%34,7 | +%35 / +%36 | −%31,3 | −%3,0 |
| Mar 2025 | +%6,0 | +%6 / **+%11,5** | **+%0,6** | −%3,5 |
| 2026: savaş, butlan, fon krizi | +%2,3–3,7 | — | +%1,6 / +%3,0 | stop tetiklenmedi |

- **Ortodoks dönem** (Ağu 2023–Ağu 2026, 778 kayan pencere): kısa vadeli 64 günde ortalama **+%2,6**, 5. yüzdelik −%1,0, en kötü −%5,5, %88 pozitif. Stoplu: ortalama +%2,5, en kötü −%3,5, %81 pozitif [H]. Prim varsayımı [V]: politika faizi − USD − 2 puan.
- **Hükmüm:** 1. turdaki +%12 gap senaryosu 2018/2021 kuyruklarını **temsil etmiyor**; ŞEYTAN haklı. O şoklar ortodoks olmayan dönemlerdeydi (bugün ex-ante reel faiz ~%9,8).
- **Revize beklenen değer** (kontrat başı, 64 gün):
  - %74 kontrollü patika: +793 TL
  - %17 hızlanma: +95 TL
  - %7 stoplu şok: −1.840 TL (−%3,5)
  - %2 2018 tipi gap: −10.500 TL (−%20)
  - Toplam **≈ +264 TL**; maliyet sonrası **~+230 TL** (1. turda +373).
  - Kırılma noktası: 2018 tipi gap olasılığı **>%4** ise beklenen değer negatif.
- **Hedge:** O_USDTRYKE1226C57000'in uzlaşması 246,7 TL, AP 25, işlem yok. C56000'in uzlaşması 295,9, kapanışı 418,4 TL (168 adet, AP 4.668) [B1]; maliyet nominalin %0,56–0,80'i. Bu, beklenen değerin (%0,43) tamamını yiyor. OPSİYON haklı, **hedge yok, boyut küçültülüyor.**
- **FOMC ve 30.10:**
  - FedWatch (20.10): sabit %83, +25 bp %17 [S3, ikincil]. Plan geçerli; ek koşullar:
    - 30.10'da TCMB gösterge kurunun ortası ≤50,00 olmalı.
    - F_USDTRY1226 ≤52,70 olmalı.
    - SPK veya siyasi şok olmamalı.
  - Yarısı 30.10'da, yarısı 3.11 TÜFE sonrası; 02.11 Takasbank güncellemesi [S4] için teminat tamponu.

### 1c. Fed iddiası: doğrulandı
federalreserve.gov, 16.09.2026: "*raise the target range … by 1/4 percentage point to 3-3/4 to 4 percent*", oylama 12–0 [S5, birincil]. Düzeltme gerekmiyor.

## 2. Diğer ajanların fikirleri

**ENDEKS F1 — rallide short F_XU0301226**
- Olgular: Aralık uzlaşması 14.638, AP 314.401; Ekim uzlaşması 13.954 [B1] ✓.
- Risk: 450 puan×10 = 4.500 TL = %0,45 ✓. Ancak stop 1,3×ATR(344); gürültüyle stoplanma olasılığı yüksek.
- Fiyat limiti çelişkisi açık: ENDEKS ±%15, OPSİYON ±%10.
- **Oy: KOŞULLU EVET, 5.** ŞEYTAN'ınkiyle tek fikirde birleşmeli. USDTRY carry için doğal hedge işlevi görür (Mart 2025'te BIST −%16 iken kur +%3,5–6).

**ENDEKS F2 — dipte koşullu long**
- **Oy: HAYIR, 3.** Kendi hesabı bile beklenen değeri ≈0 buluyor; carry R/R'yi 1,3'e indiriyor.

**HİSSE F1 — long GARAN / short YKBNK**
- Risk: %0,97 ✓.
- Olgu ekleri:
  - GM 2174'te GARAN-YKBNK ürünleri arası teminat kredisi %60, SAHOL-AKBNK %50 [S6]. Teminat tahmini muhafazakâr; gerçek değer %40–50 daha düşük.
  - 02.11 Takasbank güncellemesi teyit edildi [S4].
- Makro boşluk: YKBNK 3.11'de hem bilanço hem TÜFE'ye maruz. FX eğrisi (%34–35) ve tahviller zaten yavaş indirimi fiyatlıyor → sürpriz asimetrisi güvercin yönde, pair'in aleyhine.
- **Oy: KOŞULLU, 5.** Giriş 3.11'den sonra, risk %0,5.

**HİSSE F2 — long SAHOL / short AKBNK**
- **Oy: HAYIR, 3.** SAHOL, tasfiyedeki fonlarda en sık bulunan BIST 30 payı. Carry beklenen kârın çoğunu yiyor.

**OPSİYON F1 — koşullu straddle**
- Kontrol: 800 puan ≈ σ%17 (T≈57 gün) ✓. Risk %0,8 ✓.
- Takvim makro açıdan yoğun: FOMC, 2.11, 3.11, 12.11, 27.11, 10.12.
- **Oy: EVET, 6** (fiyat koşuluyla).

**OPSİYON F2 — 14.500/15.500 boğa call spread**
- **Oy: KOŞULLU, 4.** Yalnızca 1. turdaki makro tetikleyicilerim gerçekleşirse:
  - TÜFE ≤%2,3
  - CDS ≤235
  - 2 hafta yabancı girişi
- 1. turdaki koşullu F_XU030 long fikrimi bununla değiştiriyorum: tanımlı risk, gap ve limit kilidine karşı daha iyi.
- Küçük not: F=S·e^(0,36t) adil vadeliyi hafif abartıyor; basit TLREF ile 14.837.

**ŞEYTAN — rallide short**
- Risk: 7×688×10 = 48 bin TL = %0,96 ✓. Kapanış bazlı stop ve 2× gap ile %1,9.
- Olgu düzeltmesi: "2 yıllık %39,8 > politika faizi %36" büyük olasılıkla **bileşik** getiri. Basit karşılığı 2×(√1,398−1) ≈ **%36,5** ≈ politika faizi.
  - Asıl sinyal: getiri anketin 12 aylık %29 patikasının ~7 puan üstünde → risk primi.
- Rezerv verisini benimsiyorum: swap hariç ~56 (Ağu) → 37,8 (2.10) → 44,2 (9.10).
- **Oy: KOŞULLU EVET, 5** (ENDEKS ile tek kova).

## 3. Kendi revizyonum

| | 1. tur | 2. tur | Neden |
|---|---|---|---|
| Aralık likiditesi | "8.848 adet" | **AP 895.093; 27.10 hacmi 28.987** [B1] | Foreks gün içi kısmi veriydi; hatam |
| Beklenen değer | +373 TL | **~+230 TL** | Kuyruk %20 gap ile yeniden fiyatlandı |
| Boyut (1 mn TL) | 6 kontrat | **4 kontrat** (0,21x) | Stop %0,33; USDTRY +%8 stresi %1,7; +%20 gap %4,2 |
| Güven | 6 | **5** | Kırılma noktası 2018 tipi gap olasılığı %4 |
| Fikir 2 | F_XU030 long | OPSİYON F2'ye devredildi | Tanımlı risk |

Aynı kalanlar: tez, 53,20 stopu (stoplu en kötü sonuç −%3,5; gap hariç), yanlışlama koşulları.

## 4. Komite portföyü (OPSİYON bütçesi; stop bazlı riskler)

| Sıra | Pozisyon | Risk | Kova |
|---|---|---|---|
| 1 | MAKRO: short F_USDTRY1226, 4 kontrat / 1 mn TL | %0,33 (stres %1,7) | TL |
| 2 | ENDEKS+ŞEYTAN birleşik: 15.000–15.100'den short F_XU0301226, stop 15.550 | %0,75 | BIST short |
| 3 | OPSİYON: straddle, prim ≤800 ise | %0,6 | Vol (Δ≈0) |
| 4 | HİSSE: GARAN/YKBNK, 3.11 sonrası | %0,5 | Banka pair (β≈0) |
| Toplam | | **%2,2 ≤ %4 ✓** | |

- Ortak stres (BIST −%15, USDTRY +%8): USDTRY −%1,7; short F +%2,2; straddle +; pair ≈−%0,5 → **net pozitif**.
- Zayıf nokta: 2021 tipi senaryo, yani TL çöker ama nominal BIST yükselir. Bu durumda 1 ve 2 birlikte kaybeder (−%0,33 −%0,75, gap ile ~−%3). Straddle kısmen telafi eder.

## Kaynaklar
B1 https://www.borsaistanbul.com/data/vadeli/viop_20261027.csv · S1 https://www.gcmyatirim.com.tr/egitim/makaleler/viop-hesaplarinin-nemalandirmasi-nedir-ve-nema-nasil-hesaplanir , https://paratic.com/takasbanktan-viop-islemlerine-yonelik-yeni-duyuru · S2 https://query1.finance.yahoo.com/v8/finance/chart/TRY=X?period1=1514764800&period2=1793000000&interval=1d · S3 https://www.noradarealestate.com/blog/interest-rate-predictions-october-2026/ · S4 https://www.foreks.com/haber/detay/6ae0c15f58b1b941c20921a0/FRKS/tr/takasbank-risk-parametrelerini-guncelledi-27-10-26/ · S5 https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm · S6 https://www.isyatirim.com.tr/tr-tr/Resmi-Duyurular/Documents/GenelMektup2174.pdf
