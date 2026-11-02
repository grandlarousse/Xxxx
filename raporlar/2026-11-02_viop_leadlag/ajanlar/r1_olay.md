# r1_olay — Yurt içi makro, olay çalışmaları ve "akla gelmeyenler" (47 VİOP hissesi)
Ajan: olay · Veri sonu: 30.10.2026 · Kod: `out/code_olay/` · Olay listeleri: `out/olay_tarihleri.csv` (453 olay) · Bulgular: `out/f_olay.csv` (26 satır)

## 1. Net bulgular
| # | İlişki | Rakam | İşlenebilir mi? | Güven |
|---|---|---|---|---|
| 1 | **Not değişikliğinde kontraryen ("haberi sat")**: S&P/Moody's/Fitch not artırımı/indirimi → Pazartesi açılışta ters yönde gir, t+2 kapanışta çık | XU100 +215 bps/olay (15 bps maliyet sonrası), t=3,7, isabet %84. IS (2014–20) +182 (t 2,5, n=10) / OOS (2021–26) +252 (t 2,7, n=9). XBANK +320 (OOS +472, t 3,8). Olay öncesi 5 gün işaretli +234 bps (t 2,7) | Evet (açılıştan sonra giriliyor) | **ORTA** (n=19) |
| 2 | **FOMC gecesi gap büyümesi**: karar 18/19 UTC'de, BIST kapanışından sonra | XU100 gap ~ ES(d): FOMC gecesi β=0,22, corr 0,35; normal gece β=0,09, corr 0,15. \|gap\| 1,34x (XBANK 1,38x). Ertesi gün gün-içi corr 0,00 | Hayır (gap'te fiyatlanıyor). Gün-içi devam stratejisi OOS −45 bps | **ORTA** |
| 3 | FOMC günü ABD 10y faiz ↑ → BIST gap ↓ (ES kontrollü) | b=−0,027/yp, t=−2,2; XBANK t=−2,2 | Hayır | DÜŞÜK |
| 4 | **Negatif siyasi şoklar** (n=18): banka ↓, döviz gelirli ↑ (göreli) | XU100 gap −215 bps (t −3,2), XBANK cc −399 bps (t −3,3). XU100'e göre VAKBN/HALKB/YKBNK/GARAN/ISCTR −120..−140 bps; TAVHL/ENKAI/TKFEN/TUPRS/TRALT/CIMSA +124..+223 bps. t+1..5 sistematik sürüklenme yok | Hayır (gap); kesit bilgisi korunma için | **ORTA** |
| 5 | **TR risk primi proxy'si = USDTRY**: TL zayıflayınca bankalar piyasanın altında kalıyor | Kısmi korelasyon (XU100 kontrollü): XBANK −0,18, GARAN/VAKBN −0,16, AKBNK −0,14; ENKAI +0,13, EREGL +0,10. XBANK−XU100 spread β=−0,32 (t −8,5) | Senkron | **ORTA** |
| 6 | EMB−IEF (gelişen piyasa kredi spreadi) ve CEW → banka primi | Spread β: EMB−IEF t=5,8, CEW t=6,8. XU100 corr 0,28. Öncülük yalnız gap'te (0,10), gün-içinde 0 | Hayır | DÜŞÜK |
| 7 | **TCMB PPK sürprizi** (karar 11:00 UTC, seans içi) | Şahin sürpriz → XBANK gün-içi +244 bps; güvercin −79. İşaretli +161 bps (t 2,0, n=10). En duyarlı: AKBNK/GARAN/YKBNK; ters yönde: ASTOR/CIMSA/DOAS/ODAS. Saatlik: tepkiden sonra devam yok | Tepki 1 saat içinde bitiyor | DÜŞÜK (sürpriz sınıflaması hafızadan) |
| 8 | **TÜFE (ayın 3'ü, 10:00 TSİ = açılış)**: etki gap'te değil, ilk saatte | İlk saat \|getiri\|: XBANK 182 bps (normal 84), XU030 100 (normal 58). Günlük \|gün-içi\| oranı: YKBNK 1,20, ISCTR/EKGYO 1,18. İlk saatten sonra devam yok | Sadece volatilite (yön test edilemedi) | ORTA (volatilite) / ÇOK DÜŞÜK (yön) |
| 9 | **OLUMSUZ – ABD verisi (NFP/CPI, 8:30 ET = 15:30 TSİ yaz / 16:30 TSİ kış)**: BIST ilk saatte tepki vermiyor | Senkron corr −0,05 (n=51); \|tepki\| 30 bps (normal gün 33). Sonraki saatlerde hafif ters hareket var (CPI corr −0,56, n=27) ama brüt +12,8 bps < maliyet | Hayır | DÜŞÜK |
| 10 | BTC hafta sonu getirisi (BIST ve ES kapalıyken) → Pazartesi XU100 gap | corr 0,10 (t 2,2); IS 0,02 / OOS 0,23. Pazartesi gün-içi 0 | Hayır | DÜŞÜK |
| 11 | **OLUMSUZ – kripto ↔ bireysel yatırımcı hisseleri** | ASTOR/SASA/HEKTS/ODAS/PETKM/KONTR için XU100 üstü gap corr −0,05..0,07; günlük BTC kısmi corr ≤0,04. İstisna: TRALT 0,14 (muhtemelen Pazar akşamı altın açılışı) | — | ÇOK DÜŞÜK |
| 12 | XAUTRY (gram altın) | TRALT kısmi corr 0,29, GUBRF 0,26, TRMET 0,25, PETKM −0,19. "İkame etkisi" (altın-TL ↑ → borsa ↓) sadece 2021 öncesi: XU100 corr IS −0,23 / OOS +0,06; XBANK kısmi corr −0,10 (günlük), 0,03 (saatlik hizalı) | Senkron | ORTA (TRALT) / DÜŞÜK (ikame) |
| 13 | Bayram ve uzun kapanışlar (n=49) | Kapanış süresince ES ile ilk gün gap corr 0,56; gün-içi 0,38. Gün-içi strateji OOS +39 bps (t 1,35), IS +2 | Zayıf | DÜŞÜK |
| 14 | Ay sonu (VİOP vade sonu) kapanış seansı | XU030 \|kapanış seansı getirisi\| 27 bps (normal 18,5). MSCI ayları ek etki göstermiyor. Yön yok | Hayır | DÜŞÜK |
| 15 | TCMB haftalık yabancı akış verisi (Perşembe 14:30 TSİ) | Açıklama barında \|r\| 42 bps (diğer günler 41) → etki yok. Akış verisi alınamadı | — | ÇOK DÜŞÜK |
| 16 | TR 10y/2y faiz ve 5y CDS (doğrudan) | Test edilemedi, veri yok | — | ÇOK DÜŞÜK (hipotez) |

**TradingView adayları:** ES=F → `CME_MINI:ES1!`; ^TNX → `TVC:US10Y`; USDTRY → `FX:USDTRY`; EMB/IEF → `NASDAQ:EMB`, `NASDAQ:IEF`; CEW → `AMEX:CEW`; BTC → `BITSTAMP:BTCUSD`; XAUTRY → `COMEX:GC1!*FX:USDTRY` (spread sözdizimi) veya `FX_IDC:XAUTRY` (?); TR faizleri → `TVC:TR10Y`, `TVC:TR02Y` (muhtemelen geçerli); **Türkiye CDS için güvenilir bir TradingView kodu bulunamadı (?)**.

## 2. Yöntem
- **Zamanlama:** ll.py konvansiyonu kullanıldı. Olayın BIST'e ilk ulaştığı gün (`react_date`) olayın saatine göre belirlendi:
  - Seans içi olaylar: PPK 11:00 UTC, ABD verisi 12:30/13:30 UTC, TÜFE 07:00 UTC (açılışla eşzamanlı).
  - BIST kapanışından sonraki olaylar: FOMC 18–19 UTC, not kararları Cuma ~20:30 UTC.
  - Hafta sonu olayları.
- **Gap/gün-içi ayrımı:** Kendi panelim kullanıldı (`olib.decomp2`). Bu panelde, ll.py'nin eski versiyonundaki asimetrik temizleme hatası (−%10 taban günleri atılıyor, +%10 tavan günleri kalıyordu; 47 hissede 492 gün) simetrik eşikle (ln 1,105 / ln 0,895) düzeltildi. Hatayı koordinatöre bildirdim, ll.py'de de düzeltildi; iki kural aynı. Endekslerde temizleme yok.
- **Saatlik analiz:** BIST barları :30'da, ES barları :00'da başlıyor. Bu yüzden ABD verisi için pencereler şöyle kuruldu:
  - ES penceresi: R−30 dk → R+30 dk
  - BIST tepki penceresi: R → R+60 dk
  - Devam penceresi: R+60 dk → kapanış (R+60'ta bilinen sinyal kullanıldığı için ileriye bakış yok)
- **Backtest:** Maliyet 8 ve 15 bps. IS: 2014–2020, OOS: 2021–2026 (ABD verisinde IS 2024-06..2025-06, OOS 2025-07 sonrası). Olay sayısı küçük olduğu için t'ler olay bazında, güven etiketi n'ye göre kırpıldı.
- **Not kontraryen sonucunun sağlamlığı:**
  - TL nominal sürüklenmesi çıkarıldı (geçmiş 250 gün ortalaması ve ±60 gün merkezli ortalama): XU100 +200..215 bps (t 3,85–3,9).
  - USD bazlı: +214 bps (t 3,4).
  - Aynı gün açıklanan iki karar (17.08.2018) tek olay sayıldı.
- **Çoklu test:** Yaklaşık 15 ana olay hipotezi ve 47 hisse kesiti var. Kesit sıralamaları (en çok/en az etkilenen hisseler) betimleyicidir, FDR'den geçirilmedi. Bu yüzden hisse bazında hiçbir sonuç YÜKSEK değil.

## 3. Olay tarihleri ve kaynakları (`olay_tarihleri.csv`, `verified` sütunu)
- **PPK:** Faiz değişiklikleri (52 adet, 2014–2026) TCMB 1 hafta repo tablosundan alındı (yürürlük tarihi −1 iş günü = karar günü). 2026 sabit kararları haberden (cnbce, qnbinvest): 12.03, 22.04, 11.06, 23.07, 10.09. 22.10.2026'da faiz 100 bp indirilerek %36'ya düştü (beklenti 100 bp). 2023-06 sonrası sürpriz yönü **hafızadan** (anket medyanları); doğrulanmalı.
- **FOMC:** 2021–2026 tarihleri federalreserve.gov'dan, 2014–2020 hafızadan.
- **Not kararları:** countryeconomy.com (kısmi, tablo bozuk) + hafıza. 2026'da not değişikliği bulunamadı; Fitch 23.01.2026'da görünümü pozitife çevirdi.
- **NFP/CPI:** BLS sayfası yalnızca gelecek tarihleri gösterdi. Geçmiş tarihler hafıza + kural (2025 kapanma gecikmeleri: 24.10 CPI, 20.11 ve 16.12 NFP); doğrulanmalı.
- **TÜFE:** Kural ile üretildi (ayın 3'ü; hafta sonu/tatilse sonraki iş günü).
- **Siyasi olaylar** (26 adet), fon krizi dahil:
  - 15.09.2026: Pusula temerrüdü
  - 16.09.2026: BIST100 gün-içi −%5,5, devre kesici 13:04 UTC
  - 17.09.2026: SPK 131 fonu TEFAS'ta kapattı; gün-içi +%4,2
  - 22.09.2026: BIST 50'de açığa satışa yukarı adım kuralı
  - 27.10.2026: 7596 sayılı Kanun yürürlüğe girdi
  - Kaynaklar: kureansiklopedi, hukukcularevi, turkiyetoday, dailysabah

## 4. Karşı argümanlar ve sınırlamalar
- **Not kontraryen:** 2014–2020'deki indirimler kriz diplerine denk geliyor (genel kısa vadeli geri dönüş). 2024'teki artırımlardan sonra 5 Ağustos 2024 küresel çöküşü yaşandı (tesadüf olabilir). n=19 küçük. Mekanizma (takvimli kararın önceden fiyatlanması) makul ama kanıtlanmış değil.
- **FOMC:** Gap'teki büyüme işlenebilir değil; sadece risk yönetimi ve VİOP akşam seansı için anlamlı.
- **ABD verisi:** ES h1 verisi Yahoo'da 730 gün sınırı nedeniyle yalnızca 2024-06'dan itibaren var; tarih listesi hafızadan. Gün boyu ES–XU030 gün-içi korelasyonu 0,29 (kontrol testi), yani BIST ABD'yi takip ediyor ama veri saatinde değil.
- **TR CDS/tahvil:** Tarihsel veri alınamadı:
  - investing.com: bot korumalı; WebFetch yalnız son ayı gösteriyor
  - stooq: JS doğrulaması
  - worldgovernmentbonds: veri JS ile yükleniyor
  - FRED: Türkiye için yalnız aylık reeskont faizi
  - EVDS: API anahtarı gerekiyor

  Kullanılan proxy'ler (USDTRY, EMB−IEF, CEW) küresel bileşen taşıyor; Türkiye'ye özgü risk primini tam yakalamıyor.
- **PPK ve TÜFE:** Beklenti anketi verisi yok, sürpriz sınıflaması hafızadan.
- **USDTRY ve gün-sonu senkronu:** TRY=X ll düzeltmesiyle ~24 UTC kapanışlı, yani senkron korelasyonun bir kısmı BIST kapanışından sonraki saatlere ait.
- **Fon krizi:** Eylül–Ekim 2026 likidite krizi (işlem hacmi çöktü, bonolar fiyat gözetmeksizin satıldı) en son dönem korelasyonlarını bozabilir. 1 yıllık tahminlere temkinli bakılmalı.
