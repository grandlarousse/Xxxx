# Aile: kripto — 1-3 günlük işlem araştırması (07.11.2026)

ETF'ler (16): IBIT, FBTC, GBTC, BITB, ARKB, BITO, ETHA, ETHE, BITX, BITI, ETHU, SBIT, BITU, BLOK, MSTU, CONL.
Kod: `kod/ajan_kripto/` · Tablolar: `sonuclar/aile_kripto/` · JSON: `sonuclar/aile_kripto/sonuc.json`.

## 0. Kısa sonuç

- **Katı eşiği güvenle geçen strateji yok.** Biçimsel eşiği geçen iki aday var, ikisinin de güveni **düşük**:
  - **kripto_S1 — Perşembe gün içi ters BTC:** Perşembe ABD açılışında (kış TR 17:30) AMEX:SBIT (−2x BTC) al, aynı gün kapanışta (TR ~23:50) sat.
    Net +84 bp/işlem (2.500$), t=2,40, n=133, 2024-04..2026-11. Dayanak satırları (BTC 16:00 ET serisi, IBIT, BITO, ETHA) ailenin FDR'sini geçiyor.
    Ama etki 2024-2025'te yoğunlaşıyor. Daha önceki dönemde (BITO 2021-10..2024-03) neredeyse sıfır, 2026'da da zayıf (+12 bp). Mekanizması bilinmiyor ve SPY/QQQ'da da aynı dönemde görülüyor.
  - **kripto_S2 — BTC trend filtresi:** kapanış > SMA10 > SMA50 ise IBIT'i 3 gün tut.
    BTC 10 yıllık testte net +153 bp (t=3,42; IS 225 / OOS 58 bp; yılların %70'i pozitif; C1'de de pozitif). Komşu parametrelerde de sonuç benzer.
    Ama FDR'yi geçmiyor, kazancın çoğu IS'teki boğa piyasasından geliyor ve ayı yıllarında kaybettiriyor. IBIT döneminde (2024+) t<1, C1 modunda ≈0.
- **Elenenler:** IBIT "gece primi" (maliyet sonrası ≈0), hafta sonu etkisi (takvim günü drift'inden ibaret), haftalık momentum (OOS ≤0), ortalamaya dönüş sinyalleri, BTC→MSTR/COIN ertesi gün öncülüğü, yetişme kuralları, ETF akımı (veri yok).
- **Lead-lag:** doğrulanmış gecikmeli öncü **yok**. Gerçek zamanlı izlenecekler COINBASE:BTCUSD, CME:BTC1!, COINBASE:ETHUSD, CME:ETH1! ve CME_MINI:NQ1!.
  IBIT açılış boşluğu BTC'nin 16:00→09:30 ET hareketiyle neredeyse aynıdır (R²=0,96, eğim 1,00). Bu bir izleme aracıdır, öncü değildir.
- **İzleme listesi:**
  - kabul: IBIT, ETHA, SBIT
  - yedek: GBTC ve ETHE (Midas'ta sembol sayfası doğrulanmış tek spot ETF'ler), FBTC, BITX, BITI, ETHU
  - red: BITO, BITB, ARKB, BITU, BLOK, MSTU, CONL
- **İstatistiksel güç düşük.** Spot ETF'lerin geçmişi yaklaşık 700 işlem günü. BTC'nin günlük oynaklığı yaklaşık 300 bp olduğundan 700 günde 1 günlük ortalamanın standart hatası yaklaşık 11 bp. Yani 20 bp'lik bir kenar bile t≈1,8 verir.
  Uzun test yalnız dayanakta (BTC/ETH, 10 yıl) yapılabildi ve orada da 3-4 saatlik bir zaman kayması var.

## 1. Veri ve yöntem

**Zamanlama** (lib.py sözleşmesi): sinyal t kapanışına (16:00 ET) kadarki bilgiyle hesaplanır. Modlar C0 (t kapanışı), O1 (t+1 açılış) ve C1 (t+1 kapanış). İşlemler çakışmaz. Maliyet 2.500$ pozisyonda 12 bp komisyon + kademe makası (IBIT 14,3 bp; SBIT 16; BITX 18,4; ETHA 14; BITI 20).

**BTC/ETH dayanak serileri** (`kod/ajan_kripto/kr.py`):
- `BTC_D`, `ETH_D` (2016-11..2026-11): Coinbase günlük UTC mumları NYSE günlerine örneklendi. Pazartesi barı hafta sonu mumlarını da içerir.
  NYSE günü t'nin "kapanışı", t tarihli mumun kapanışıdır (00:00 UTC t+1 = 16:00 ET'den 3-4 saat sonra). Sinyal ve giriş aynı zaman damgasında olduğu için ileri bakış yoktur, ama ETF zamanlamasıyla birebir örtüşmez.
  Bu seride yalnız C0 ve C1 raporlandı; O1 anlamsız (24 saat açık piyasa). IS = 2016-11..2021, OOS = 2022..2026-11.
- `BTC_ET`, `ETH_ET` (2023-06..2026-11): saatlik veriden 16:00 ET fiyatı (`lib.btc_at_us_close`). Açılış = 09:30 ET tahmini (09:00 mumunun açılış-kapanış ortalaması).
  IBIT ile günlük getiri korelasyonu 0,999. Bu seri birebir ETF zamanlamasıdır.
- **Uyarı:** COINBASE:BTCUSD'nin TradingView günlük mumu 00:00 UTC'de (TR 03:00) kapanır. ABD kapanışında (TR 00:00, kış) bilinmez, bu yüzden sinyal hesabında kullanılmamalıdır.

**Veri sorunları** (`01_islenebilirlik.py`):
- **BITO'nun dağıtımları veri kaynağında yok.** Ayın ilk işlem günü açılış boşluğu IBIT'e göre ortalama −295 bp (n=34; diğer günlerde −3 bp). Bu yüzden BITO'nun kapanıştan kapanışa getirisi aşağı yanlı. Ay başı ve ay sonu FDR satırları bu artefakttan geliyor.
- **Kaldıraçlı ürünlerde takip kaybı** (2× dayanağa göre): BITX −11,5 bp/gün (t=−8,7), BITU −11,4, ETHU −7,9, MSTU −15, SBIT +3, BITI ~0.
- BITU'da 24.12.2025'te 2×IBIT'e göre açıklanamayan −21 puanlık fark var.
- BITI'de ay başlarında −5 puanlık farklar var; dağıtım kaydı eksik olabilir.
- CONL'un 2022-08..09 verisi dayanakla tutarsız.
- MSTR hisse verisi bölünmeye karşı düzeltildi (10:1, 2024-08).

**Kopya grupları** (günlük getiri korelasyonu):
- spot BTC {IBIT, FBTC 0,9993, GBTC 0,9992, BITB 0,9998, ARKB 0,9997}
- 2x BTC {BITX, BITU 0,987}
- spot ETH {ETHA, ETHE 0,9997}

Gruplar arası korelasyonlar:
- IBIT-BITO 0,96
- IBIT-BITX 0,998
- IBIT-ETHA 0,83
- IBIT-MSTU 0,80
- IBIT-BLOK 0,73
- IBIT-CONL 0,73
- IBIT-BITI −0,99

Bağımsız dayanak sayısı fiilen 2-3'tür: BTC, ETH ve kripto hisseleri. Kopyalar bağımsız kanıt sayılmadı.

## 2. Test sayısı ve FDR

| Kaynak | Test |
|---|---|
| genel_tum.csv aile satırları (16 ETF × 297) | 4.752 |
| Aynı 31 sinyal: BTC_D, ETH_D (C0/C1), BTC_ET, ETH_ET (C0/O1/C1) | 990 |
| Aileye özel hipotezler (KR01-06, seans, BTC desenleri, Perşembe) | 352 |
| Lead-lag ek regresyonlar ve kural backtestleri | 104 |
| Aday ayrıntı satırları (aktarım, mod) | 60 |
| leadlag_sweep aile satırları (765 × 4) | 3.060 |
| **Toplam** | **~9.273** |

BH-FDR (q=0,10), iki yönlü p:
- Sweep dahil eşik p≤0,00010 (10 satır geçiyor). Sweep hariç kendi 6.213 testimde eşik p≤0,00047 (30 satır geçiyor).
- Geçenlerin çoğu **negatif** satır: Perşembe gün içi long (BTC_ET, ETH_ET, IBIT, ETHA, BITX, BITO, BLOK, FBTC/GBTC/BITB/ARKB kopyaları) ve BITO dağıtım artefaktları.
- Geçen pozitif satırlar yalnız ETH_D momentum satırları: 20 gün zirvesi C0 h1/h2, RSI2>90 C0 h2, MO_trend C0 h3. Bunların hepsi IS (2016-2021) ağırlıklı; OOS +5..+46 bp.

Ayrıntı: `sonuclar/aile_kripto/fdr_tum.csv`.

## 3. İşlenebilirlik (tarama.csv)

| ETF | Grup | Mn$/gün | Maliyet (2.500$) | 1g oynaklık | Maliyet/oynaklık | Karar |
|---|---|---|---|---|---|---|
| IBIT | spot BTC | 2.000 | 14,3 | 281 | 0,051 | kabul |
| FBTC | spot BTC | 291 | 14,0 | 281 | 0,050 | yedek |
| GBTC | spot BTC | 136 | 16,0 | 281 | 0,057 | yedek (Midas'ta doğrulanmış) |
| BITB / ARKB | spot BTC | 70 / 61 | 16,0 | 280 | 0,057 | red (kopya) |
| BITO | BTC vadeli | 875 | 21,9 | 288 | 0,076 | red (dağıtım/vergi/roll) |
| BITX / BITU | 2x BTC | 172 / 59 | 18,4 / 20,2 | 559 / 576 | 0,033 / 0,035 | yedek / red |
| BITI | −1x BTC | 38 | 20,0 | 288 | 0,069 | yedek |
| SBIT | −2x BTC | 57 | 16,0 | 562 | 0,028 | kabul (S1 aracı) |
| ETHA | spot ETH | 553 | 14,0 | 384 | 0,036 | kabul |
| ETHE | spot ETH | 50 | 17,6 | 381 | 0,046 | yedek (Midas'ta doğrulanmış) |
| ETHU | 2x ETH | 144 | 17,0 | 767 | 0,022 | yedek |
| BLOK | kripto hisse | 14 | 20,0 | 260 | 0,077 | red |
| MSTU | 2x MSTR | 176 | 16,0 | 1.026 | 0,016 | red (aşırı risk; 1y −89%) |
| CONL | 2x COIN | 111 | 47,8 | 906 | 0,053 | red (2,79$ fiyat → ~36 bp makas) |

Midas'taki bulunurluk: yalnız GBTC ile ETHE'nin sembol sayfası doğrulanmış. IBIT, FBTC ve ETHA "muhtemel". Kaldıraçlı ve ters ürünler (BITX, SBIT, BITI, ETHU) doğrulanamadı.
BITU ve SBIT, ProShares Trust II'nin 1446(f) PTP bildirim listesinde (26.02.2026) yer almıyor; PTP/K-1 görünmüyor, ama uygulamadaki "PTP" ibaresi yine de kontrol edilmeli.
BITO'nun yüksek aylık dağıtımları ABD'de %20 stopaja tabi; 1-3 günlük işlemde ex-date taşımamak gerekir.

## 4. Genel kütüphane (genel_tum.csv) aile içi bulgular — `02_genel_aile.py`

- 198 sinyal×mod×h×çıkış kombinasyonunun 45'i BTC_D ve ETH_D'de hem IS hem OOS'ta net>0 (yılların ≥%60'ı pozitif).
- Drift'ten arındırılmış kenar (brüt − koşulsuz aynı tutuş) IS ve OOS'ta iki dayanakta da >0 olanlar: **22**.
  - Bunlar ağırlıkla **momentum** (MO_trend_10_50, MO_20g_zirve, MO_rsi2_gt90, MO_3gun_yukselis, MO_z1_gt_2).
  - Bir kısmı da Perşembe/Cuma → Pazartesi tutuşları; bunların kenarı takvim günü sayısından gelir.
  - OOS kenarları küçük (12-43 bp); ETF döneminde IBIT'te hepsi t<1,8.
- Ortalamaya dönüş sinyallerinde (RSI2, IBS, BB, 3 gün düşüş, 5 gün dip) BTC ve ETH'de kenar yok, ya da kenar yalnız C0 h=1'de (kapanışa bağımlı).
- Tek ETF seçimi yapılmadı. Tutarlılık IBIT, ETHA, BLOK, MSTU ve CONL temsilcilerinde sayıldı (`genel_aile_tutarlilik.csv`).

## 5. Aileye özel hipotezler — `03_hipotezler.py`

| Hipotez | Sonuç |
|---|---|
| KR01 IBIT gece/gün içi | IBIT gece ort. +16,5 bp (t=1,89), gün içi −5,1 (t=−0,7). Ocak 2024'ten beri birikimli gece +%165, gün içi −%39 (literatürle uyumlu). **Her gece al-sat net +2 bp (t=0,25)**; 10.000$'da +11 bp. Kopyalar ve BTC_ET aynı. Elendi. |
| KR05 kış/yaz | IBIT gecesi kışın 28 bp, yazın 11 bp brüt (ikisi de t<1,7). BTC 21-23 UTC penceresi +6,4 bp (t=3,4, n=1.263) ama 14 bp maliyetin altında; 2026'da −0,5. Elendi. |
| Seanslar (saatlik, 2023-05+) | Hafta içi ABD akşamı 16-20 ET +6,4 bp (t=2,2); Avrupa 03-09 ET +5,9 (t=1,6); ABD seansı 09-16 ET −3,0 (t=−0,5); Asya ~0. 1-3 günlük kapanıştan kapanışa tutuşa doğrudan katkısı yok. |
| KR02 hafta sonu | BTC_D Cuma→Pzt net 55 bp (t=2,28; IS 87 / OOS 22); BTC_ET 35 (t=1,22); IBIT 30 (t=0,93); ETHA −14. **Takvim günü başına getiri hafta sonu ile hafta içi arasında farksız** (fark t=0,5-0,9). Etki 3 takvim günlük drift'ten ibaret. Elendi. |
| Pazartesi boşluğu | IBIT Pazartesi açılış boşluğu ≈ BTC Cuma 16:00 → Pzt 09:30 ET hareketi (R²=0,98, eğim 1,03). Gerçek zamanlı izleme aracı. Pazartesi gün içinde hafta sonu hareketinin devamı ya da tersi yok (eğim −0,04). |
| KR03 ETF akımı | Veri yok, test edilemedi. |
| KR04 haftalık momentum | BTC_D C0 net 175 bp ama OOS −5 (kenar −21); BTC_ET ve IBIT negatif (IBIT C0 −48). Elendi. |
| KR06 kaldıraç kaybı | BITX −11,5 bp/gün, 3 günde −37 bp; ETHU −7,9 / −25. σ20≥%4 iken BITX 3 günde −54 bp. Strateji değil; kaldıraçlı long ürün kullanmanın maliyeti. |
| BTC z1>+2 → 3 gün | BTC_D C0/C1 net 150/154 bp (t=1,83/1,85; IS ve OOS>0); BTC_ET üç modda +187..+245 (n=22-23, t≈1,8-1,9); IBIT +244..+292 (n=16-17). Eşik altı (t<2), izlemeye değer. Komşu z>1,5'te t=2,2-2,3, z>2,5'te 0,8-1,6. |
| BTC z1<−2, 3 gün düşüş | Kenar yalnız C0 h=1'de (kapanışa bağımlı) ya da hiç yok. |
| 20 gün zirve / dip | Zirve: OOS kenarı 13 bp, IBIT C1 −28 bp. Dip: kenar ≤0. |
| Perşembe gün içi | → S1 (aşağıda). |

## 6. Aday stratejiler — `05_adaylar.py` (çalıştırınca bütün sayıları basar)

### kripto_S1 — Perşembe gün içi ters BTC (SBIT) — güven: DÜŞÜK

- **Kural:** Her Perşembe (NYSE tam gün açıksa) AMEX:SBIT'i ABD açılışında al, aynı gün kapanıştan 5-10 dk önce sat. Gösterge yok; pozisyon gece taşınmaz.
- **Zamanlama:** Giriş kışın TR 17:30, yazın 16:30. Çıkış kışın TR ~23:50, yazın ~22:50. Midas'ta MOC yok; piyasa ya da agresif limit emir kullanılır.
- **Takvim istisnaları:** 26 Kas 2026 kapalı, işlem yok. 24 Ara 2026 erken kapanış; çıkış TR ~20:50.
- **Sonuç (SBIT 2024-04..2026-11):**
  - n=133, brüt 100 / net 84 bp; kazanma %48; PF 1,76; t=2,40
  - ilk yarı 84 / ikinci yarı 85 bp
  - yıllık net 2024 +105, 2025 +131, 2026 +12
  - maxDD −%31; en kötü işlem −916 bp
- **Maliyet duyarlılığı:** 1.000$'da 66, 2.500$'da 84, 10.000$'da 93 bp.
- **Mod sağlamlığı:**
  - C0 (Çarşamba kapanışında gir): net 74 bp (t=1,55)
  - C1 (Perşembe kapanış → Cuma): −77 bp
  - Etki yalnız Perşembe ABD seansında; açılış girişine bağımlı.
- **Dayanak ve aile** (long ürünlerde Perşembe gün içi brüt):
  - BTC 16:00 ET −40 bp (t=−4,0; FDR geçti), IBIT −55, ETHA −83, BITX −105, MSTU −177, CONL −71
  - BITO 2021-10+ −31 (t=−3,7; FDR geçti), BLOK 2018+ −19
  - SPY ve QQQ'da da 2023-06+ döneminde −12/−21 bp; 2016-2023'te pozitif
  - BITI net +8 bp (t=0,6)
  - SBIT'te diğer hafta günleri gün içi net −17..−40 bp; pozitif olan tek gün Perşembe
- **Güveni düşüren kanıtlar:**
  - SBIT öncesi dönem (BITO 2021-10..2024-03, n=125): Perşembe gün içi −12,6 bp (t=−0,5). SBIT-eşdeğeri net yalnız +9 bp; JSON'daki `is_net_bp` alanı bu değer. 2022'de işaret ters (+32 bp).
  - BITI 2022-06..2024-03 net −20 bp.
  - En iyi 5 işlem çıkarılınca net +42 bp (t=1,36), medyan −5 bp.
  - CPI günü olan Perşembeler çıkarılınca net 64 bp (t=1,81).
  - Mekanizma yok; 5 gün × 2 seans seçimi veri madenciliği riski taşıyor.
- **Öneri:** küçük pozisyonla canlı izle; 12 işlemde ortalama ≤0 olursa bırak.

### kripto_S2 — BTC trend filtresi → IBIT 3 gün — güven: DÜŞÜK

- **Kural:** NASDAQ:IBIT günlük kapanışı > SMA10 ve SMA10 > SMA50 ise kapanıştan 5-10 dk önce (kış TR ~23:50) IBIT al (yedek GBTC/FBTC). 3 işlem günü sonra kapanışta sat.
  Pine: `c > ta.sma(c,10) and ta.sma(c,10) > ta.sma(c,50)`
- **Dayanak (BTC_D 2016-11..2026-11):**
  - n=317, brüt 167 / net 153 bp; kazanma %54; PF 1,74; t=3,42
  - IS 225 / OOS 58 bp (OOS t=1,26); kenar IS 107 / OOS 44 bp
  - yılların %70'i pozitif; maxDD −%58; en kötü −2.498 bp
  - C1 net 135 (t=2,75; OOS 26)
  - Komşu SMA parametreleri (5/50, 10/30, 20/50, 10/100): t 3,4-4,2, OOS 41-58 bp
- **ETF dönemi:**
  - IBIT kendi grafiği: C0 +30 (t=0,57), O1 +36, C1 −42
  - BTC 16:00 ET sinyali IBIT'te: C0 +44, O1 +17, C1 +1
  - BITX +97 (t=0,98)
  - ETHA kendi +64; ETH_D net 261 (t=3,7; FDR geçti; OOS 30)
  - BLOK 2018+ +41 (t=1,83)
  - MSTU −303
- **Maliyet duyarlılığı:**
  - BTC_D: 1.000$'da 135, 10.000$'da 162 bp
  - IBIT 2024+: 1.000$'da 26, 10.000$'da 53 bp
- **Uyarılar:**
  - FDR'yi geçmiyor (p=0,0007).
  - Ayı yıllarında kaybettiriyor (2018 −444, 2022 −277 bp/işlem).
  - Kenarın bir kısmı BTC drift'i.
  - BTC_D sinyali 00:00 UTC kapanışında hesaplanıyor (3-4 saat kayma).
  - BITX kullanılırsa 3 günlük takip kaybı yaklaşık −37 bp.
  - Hafta sonu boşluk riski taşıyor.

## 7. Lead-lag — `04_leadlag.py`

**leadlag_sweep:** ailenin 765 satırında (3.060 test) global ve aile içi FDR'yi geçen satır 0.
IS ve OOS'ta aynı işaretli tek gecikmeli satırlar BLOK'ta reel faiz kanalı (TIP h3 t=3,0; DFII10 h3 t=−3,1; 36-41 bp/sd). Bunları kurala çevirince C0 net 55 bp (t=2,05) çıkıyor, ama DFII10 kapanışta bilinmiyor; O1 ve C1'de kenar yok. Elendi.

**Eşzamanlı sürücüler** (corr_1y / beta_1y; öncü DEĞİL):
- IBIT ← BTC 1,00/1,01; ETH 0,92/0,68; QQQ 0,49/1,03; VIX −0,46
- ETHA ← ETH 1,00/1,01; BTC 0,93/1,27; QQQ 0,49/1,40
- BITX ← BTC 1,00/2,01
- SBIT ← BTC −0,99/−2,01
- BITI ← BTC −0,98/−1,01
- ETHU ← ETH 1,00/2,03

**Ek testler** (2023-06+, BTC/ETH 16:00 ET, kendi gecikmesi kontrollü, Newey-West):
- BTC → MSTR t+1: t=−0,98. BTC → COIN: −1,14. BTC → MSTU: −0,17. BTC → BLOK: −1,06. BTC → ETHA: 0,61. ETH → IBIT: −0,44.
- "Yetişme" katkısı kendi getirisi kontrol edilince hiçbirinde |t|≥2 değil.
- Yetişme kuralları (u≥+2σ → long) n=7-27, t<1,2.
- BTC gece hareketi → IBIT gün içi: z≥+1'de IBIT +29 bp (t=1,4); z≤−1'de SBIT +48 (t=1,1).
- **Sonuç: doğrulanmış gecikmeli öncü yok.**

**Gerçek zamanlı izleme** (ETF kapalıyken işleyenler, açılış boşluğunu önceden gösterir):
- COINBASE:BTCUSD (7/24; IBIT boşluğu ≈ BTC 16:00→09:30 ET, R²=0,96)
- CME:BTC1! (Pazar-Cuma; kış TR 02:00→01:00; hafta sonu kapalı)
- COINBASE:ETHUSD
- CME:ETH1!
- CME_MINI:NQ1!
- CRYPTOCAP:BTC.D (ETH bağlamı)

## 8. Takvim riskleri (önümüzdeki günler, TR saati, ABD kış saati)

| Tarih | Olay |
|---|---|
| 10 Kas Sal 16:30 | CPI |
| 20 Kas Cum | OPEX |
| 26 Kas Per | Şükran Günü, kapalı |
| 27 Kas Cum | Erken kapanış 21:00 |
| 4 Ara Cum 16:30 | NFP |
| 9 Ara Çar 22:00 | FOMC (SEP) |
| 10 Ara Per 16:30 | CPI; S1 günü, çok oynak |
| 18 Ara Cum | Triple witching |
| 24 Ara Per | Erken kapanış 21:00 |
| 25 Ara, 1 Oca | Kapalı |

Kripto 7/24 işlediği için tatil ve hafta sonu hareketleri açılışta boşluk olarak gelir.

## 9. Sınırlamalar

1. **Kısa ETF geçmişi:** spot BTC 2024-01+, ETH 2024-07+. IS (≤2021) dönemi yalnız dayanakta var.
   BTC_D'nin 3-4 saatlik zaman kayması nedeniyle uzun test ETF zamanlamasıyla birebir değil. Saatlik 16:00 ET serisi 2023-06'dan başlıyor.
2. **Açılış fiyatı:** IBIT açılışı resmi açılış fiyatı; BTC_ET'de 09:30 tahmini kullanıldı. Gerçek dolum açılıştaki makas ve kaymaya bağlı.
   Uzatılmış saatlerde (after-hours ve pre-market) yalnız limit emir verilebiliyor ve bu saatlerin makası test edilmedi.
3. **Dağıtım verisi eksik:** BITO'da kesin, BITI/BITU/BITX'te olası. Bu ürünlerin kapanıştan kapanışa sonuçları aşağı yanlı.
4. **Midas bulunurluğu:** IBIT, ETHA ve kaldıraçlı/ters ürünler doğrulanamadı. Yalnız GBTC ve ETHE'nin sembol sayfası doğrulandı.
5. **Çoklu test:** yaklaşık 9.300 test yapıldı. Aday ETF satırları FDR'yi geçmiyor; S1'de yalnız dayanak satırları geçiyor.
6. **Dönem bağımlılığı:** kripto rejimleri 2017, 2021 ve 2024 boğaları ile 2018 ve 2022 ayıları arasında çok farklı. IS sonuçları boğa piyasası ağırlıklı.

## 10. Tekrar üretim

```
cd /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun
python3 -I kod/ajan_kripto/01_islenebilirlik.py
python3 -I kod/ajan_kripto/02_genel_aile.py
python3 -I kod/ajan_kripto/03_hipotezler.py
python3 -I kod/ajan_kripto/04_leadlag.py
python3 -I kod/ajan_kripto/05_adaylar.py      # adayların bütün sayıları + FDR
python3 -I kod/ajan_kripto/06_sonuc_json.py   # sonuclar/aile_kripto/sonuc.json
```
Çok işlemcili çalıştırma yok; toplam süre 1 dakikanın altında.
