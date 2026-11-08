# Denetim: kripto ailesi (08.11.2026)

Denetlenen: `notlar/aile_kripto.md`, `kod/ajan_kripto/*.py`, `sonuclar/aile_kripto/*`.
Denetim kodu: `kod/denetim_kripto/` (`dk.py`, `d_S1.py`, `d_S2.py`, `d_leadlag.py`, `d_ek.py`, `yaz_json.py`).
Loglar ve tablolar: `sonuclar/aile_kripto/denetim/`. JSON: `sonuclar/aile_kripto/denetim.json`.

Yöntem:
- İşlem simülasyonu kendi çakışmasız döngümle yapıldı; `lib.trades`, `lib.evaluate` ve `lib.stats` kullanılmadı. Fiyatlar `lib.load` ve ham kripto parquet dosyalarından alındı.
- Maliyet = 2 × 1,5 $ / pozisyon + `tarama.csv` makası.
- Denetimde yaklaşık 220 ek test yapıldı. Bu testlerle yeni bir strateji iddia edilmiyor.

## Kısa sonuç

| Bulgu | Ajan | Denetim |
|---|---|---|
| S1 Perşembe gün içi SBIT | düşük güvenli aday | **ÇÜRÜTÜLDÜ** (aday değil; en fazla kağıt üstünde izlenecek hipotez) |
| S2 BTC trend → IBIT 3 gün | düşük güvenli aday | **ZAYIF** (strateji değil, rejim filtresi) |
| Doğrulanmış gecikmeli öncü yok | — | **doğrulandı** |
| COINBASE:BTCUSD açılış boşluğunu gösterir (R² 0,96) | — | **doğrulandı** (izleme aracı, öncü değil) |
| İzleme: SBIT kabul | kabul | **yedek** olmalı |
| GBTC / ETHE yedek | yedek | **IBIT / ETHA ile eş birincil** (Midas'ta doğrulanmış tek spot ETF'ler) |

## S1 — Perşembe gün içi ters BTC (SBIT)

**Yeniden üretim: birebir.**
- Ajanın tanımıyla (Çarşamba sinyali → O1 h=1): n=133, brüt 100,2 / net 84,2 bp, t=2,40.
- 133 işlemin hepsi ajanın listesiyle aynı.

**Kod kuralla uyuşmuyor.** Kural "Perşembe tatilse işlem yok" diyor. Ama "Çarşamba sinyali → sonraki işlem günü" tanımı 7 işlemi Cuma'ya kaydırıyor: 05.07.2024, 29.11.2024, 10.01.2025, 20.06.2025, 28.11.2025, 26.12.2025, 02.01.2026.

**Gerçek Perşembe ile sonuçlar** (`d_S1.py`):

| Ölçü | Değer |
|---|---|
| n | 129 |
| brüt / net (2.500$) | 95,5 / 79,5 bp |
| t | 2,23 |
| PF | 1,71 |
| maxDD | −%30,7 |
| en kötü işlem | −916 bp |
| net, 1.000$ | 61,5 bp (t=1,72; **< 2**) |
| net, 10.000$ | 88,5 bp (t=2,48) |
| yıllık net | 2024 +114 / 2025 +115 / **2026 +12 (t=0,19)** |
| son 12 ay | +66 bp (t=0,98) |
| 2026 2. yarı | −99 bp |
| en iyi 5 işlem hariç | 35,5 bp (t=1,15) |
| CPI günleri hariç | 58 bp (t=1,63) |

**Zamanlama ve veri kontrolü:**
- İleri bakış yok; kural saf takvim kuralı.
- SBIT açılış fiyatı güvenilir. IBIT'ten türetilen −2x gün içi getiriyle korelasyonu 0,9992, ortalama fark −2,4 bp.
- En büyük 5 kazanç:
  - 05.02.2026: veri_kalitesi.csv'de bayraklı, ama gerçek bir BTC çöküşü.
  - 19.12.2024: FOMC ertesi günü.
  - 20.11.2025.
  - 18.12.2025: CPI günü.
  - 14.11.2024.

  Hiçbiri veri hatası değil. Kazanç birkaç büyük düşüş Perşembesinden geliyor.

**Çürütme gerekçeleri:**

1. **"Dayanak satırları FDR'yi geçti" iddiası bir yöntem hatası.**
   - `fdr_tum.csv`'de long satırların p değeri **net** getiriden hesaplanmış. Negatif brüt ortalamaya long maliyeti eklenince t büyüyor. Örnek: SPY'de brüt −0,8 bp iken net t=−3,49 çıkıyor.
   - Doğru sıfır hipoteziyle (brüt getiri, 2023-06+) p değerleri: BTC 0,0037, IBIT 0,0014, ETHA 0,0012, BITO 0,0010, BITX 0,0008.
   - Ajanın kendi eşikleri p≤0,00047 (sweep hariç) ve p≤0,00010 (sweep dahil). Hiçbiri geçmiyor.
2. **Uzun dönem dayanak testi boş.** Kısa geçmişli ürünler için eşik "dayanakta uzun dönem testi" istiyor. Sonuçlar:

   | Seri | Dönem | Perşembe gün içi | Diğer günlerle fark (t) |
   |---|---|---|---|
   | GBTC tröstü (ABD seansı) | 2019-01..2024-01, n=254 | −20,7 bp | −0,48 |
   | ETHE tröstü | 2019-05..2024-07 | — | +0,34 |
   | BITO | 2021-10..2024-03 | −12,6 bp | — |
   | MSTR | 2020-2024 | — | −1,0 |
   | COIN | 2021-2024 | — | −1,1 |

   - GBTC tröstünün −2x eşdeğeri net +25 bp (t=0,55); 2019 ve 2020 negatif.
   - BITI'nin SBIT öncesi dönemi: net −19,7 bp.
   - Ajanın JSON'undaki `is_net_bp=9,2` gerçek bir IS değil, BITO'dan kurulmuş bir vekil.
3. **Etkinin yarısı hisse piyasasından geliyor.**
   - SBIT döneminde QQQ'nun Perşembe gün içi getirisi −25,7 bp (t=−2,53). 2016-2024 arasında +5 bp idi.
   - QQQ kontrol edilince SBIT'in Perşembe katsayısı 50 bp'ye iniyor (t=1,53).
4. **Desen sönüyor.** BTC 09:30-16:00 ET Perşembe getirisi: 2024 −60, 2025 −55, 2026 −16 bp.
5. **Perşembe gecesi geri dönüş var.**
   - IBIT Perşembe kapanış → Cuma açılış: +35,5 bp (t=2,24).
   - BTC 16:00 → Cuma 09:30 ET: +31,9 bp (t=2,21).
   - Yani Perşembe düşüşü kalıcı bir bilgi değil, seans içi bir akış deseni. Pozisyon asla geceye taşınmamalı; C1 sonucu (−61 bp brüt) da bunu gösteriyor.

**Lehte kanıt (örneklem içi):**
- Rastgele 129 gün permütasyonu p=0,0025.
- "5 günün en iyisi" seçim düzeltmeli permütasyon: SBIT p=0,012; BTC seansı p=0,0022.

Bunlar keşif örnekleminin içinde ve tek bir rejime (2024-2025) dayanıyor.

**Karar:** aday değil. Para yatırmadan 2026 Q4 – 2027 Q1'de 12 Perşembe kağıt üstünde izlenebilir. Brüt ortalama 40 bp'nin altında kalırsa bırakılmalı.

## S2 — BTC trend filtresi (c > SMA10 > SMA50) → 3 gün

**Yeniden üretim** (`d_S2.py`):
- BTC_D serisi ajanınkiyle aynı (2.513 gün, fark 0).
- C0 h=3: n=320, net 154,8 bp, t=3,50; IS 227 (t 3,30) / OOS 58 (t 1,26).
- Ajanın sonucu n=317, net 152,8 bp. Fark yalnız ısınma penceresinden (ajan ilk 60 günü atlamış, ben ilk 50'yi).
- İleri bakış yok. Sinyal ve giriş aynı 00:00 UTC kapanışında; çıkış t+3 kapanışı; işlemler çakışmıyor; maliyet bir kez düşülüyor.

**Rastgele giriş permütasyonu** (aynı n, aynı 3 gün tutuş, 10.000 tekrar):

| Dönem | p |
|---|---|
| tüm dönem | 0,0125 |
| IS | 0,034 |
| OOS | **0,16** |

- OOS'ta drift üstü kenar 43,7 bp (t≈0,95).

**Sağlamlık kontrolleri:**
- 2017 hariç tüm dönem 92 bp (t 2,07); IS 130 bp (t 1,65).
- 2020 hariç 148 bp (t 3,09); 2022 hariç 165 bp; ikisi birden hariç 159 bp.
- En iyi 5 işlem gerçek rallilerden; net toplamın %32'si.
- **Parametre komşuluğu** (36 kombinasyon, 5-20 / 30-100): 35'inde OOS net > 0, ama OOS t'lerin hepsi < 2 (−0,45 ile 1,89 arası). Plato görünümü var ama anlamlılık yok.
- **Tutuş komşuluğu:** h1/h2/h5 için OOS 7 / 25 / 92 bp; hepsinde t < 1,3.
- **Zaman kayması:** aynı 2023-08+ döneminde 16:00 ET serisi C0 65 bp (t 1,34), 00:00 UTC serisi 89 bp. 3-4 saatlik kayma sonucu biraz iyileştiriyor.

**Uygulanacak araçta (IBIT) sonuç yok:**

| Sinyal | C0 | O1 | C1 |
|---|---|---|---|
| IBIT kendi grafiği | 19 bp (t 0,38) | 30 bp | −26 bp |
| BTC 16:00 ET | 44 bp | 17 bp | 0,6 bp |

- GBTC kendi sinyali C0: 13 bp.

**Maliyet duyarlılığı:**

| Pozisyon | Net | OOS |
|---|---|---|
| 1.000$ | 137 bp | 40 bp (t 0,87) |
| 2.500$ | 155 bp | 58 bp |
| 10.000$ | 164 bp | 67 bp |

**ETH sürümü:** ETH_D OOS 30 bp (t 0,48); ETHA kendi C1 −14 bp.

**Karar:** ZAYIF. Bu bir beta zamanlaması ("trend varken long BTC"). Strateji olarak değil, rejim filtresi olarak kullanılabilir.

## Lead-lag (`d_leadlag.py`)

**Sweep:** 765 satır / 3.060 test. Aile içi yeniden yapılan BH'de 0 satır geçiyor (en küçük p=0,0021).

**Bağımsız regresyonlar:**
- Kurulum: 90 test. Öncüler BTC/ETH 16:00 ET, QQQ, VIX ve DGS10; hedefler 9 ETF; dönem 2024+; kendi gecikmesi kontrollü, Newey-West.
- |t|≥2 olan 3 test var. FDR geçen 0. İki yarıda da aynı işaretli ve |t|≥2 olan 0.
- DGS10 → ETHA/ETHE/ETHU için h3 t≈2,1 çıkıyor, ama yalnız ilk yarıda.

**Kopya ve kapanış kontrolleri:**
- GBTC/FBTC ← IBIT (sweep t 2,7-2,8) bir kopyalar arası yetişme artefaktı. Korelasyon 0,999 olduğu için bp/sd ölçüsü şişiyor; gerçek fark sd'si ~11 bp, maliyetin altında.
- IBIT kapanışının BTC 16:00'a göre sapması (bayat kapanış/yetişme): sd 15 bp, ertesi gün C→C t=−0,27. Yetişme yok.

**Gerçek zamanlı izleme:**
- IBIT açılış boşluğu ~ BTC 16:00→09:30 ET: R²=0,962, eğim 1,00.
- BTC gece hareketi → IBIT gün içi: eğim 0,056 (t 0,90).

**BLOK ← reel faiz:** IS ve OOS'ta aynı işaretli, ama FDR geçmiyor ve BLOK zaten red. Ajanın elemesi doğru.

**Sonuç:** "Doğrulanmış gecikmeli öncü yok" sonucu doğru.

## Ek doğrulamalar (`d_ek.py`)

- **Kaldıraç kaybı** (günlük): BITX −11,5 bp (t −8,7), BITU −11,4, ETHU −7,9, SBIT +3,1, BITI +0,3. Ajanla aynı.
- **BITO:** veride hiç dağıtım kaydı yok. Ay başı açılış boşluğu IBIT'e göre −295 bp (diğer günlerde −3). Ajanın tespiti doğru.
- **TradingView kodları:** ajanın kullandığı ETF kodlarının tümü `tv_etf.csv`'de "dogrulandi". Öncü kodlarının tümü `tv_dogrulama.csv`'de "dogrulandi" veya "dogrulandi_kanonik": COINBASE:BTCUSD, COINBASE:ETHUSD, CME:BTC1!, CME:ETH1!, CRYPTOCAP:BTC.D, CME_MINI:NQ1!, CBOE:VIX.
- **PTP:** SBIT ve BITU, ProShares Trust II'nin 26.02.2026 tarihli 1446(f) bildiriminde yer almıyor. Ajanın "PTP görünmüyor" sonucu ham sayfayla uyumlu.

## Kaçırılanlar

1. **Ailenin FDR tablosunda yöntem hatası** (yukarıda S1, madde 1). FDR'yi geçen 30 satırın 24'ü negatif; bunların çoğu ya maliyetin t'yi şişirmesinden ya da BITO dağıtım artefaktından geliyor. Ters yönlü bir iddia, brüt getiriyle ya da ters ürünün net getirisiyle test edilmeli.
2. **Perşembe gecesi geri dönüş riski.** IBIT Perşembe gecesi +35,5 bp (t 2,24). "Perşembe gecesi IBIT" tamamlayıcı işlemi 2.500$'da net ~21 bp (t≈1,3) veriyor. Bu eşiğin altında ve aynı örneklemde veri madenciliği; aday değil.
3. **Hisse piyasası bağı.** QQQ'da da aynı dönemde Perşembe gün içi zayıf. Bu, ayrı bir kripto anomalisi değil, geniş risk iştahı deseni.
4. **Fırsat yok.** IBIT "gece primi" 10.000$ pozisyonda net +11 bp, 25.000$'da +13 bp (brüt t 1,89). Büyük pozisyonda bile eşiğin altında.

## İzleme listesi itirazları

| ETF | Ajanın kararı | Denetim önerisi | Gerekçe |
|---|---|---|---|
| SBIT | kabul | **yedek** | Kabulün tek gerekçesi S1'di ve S1 çürütüldü. Long-only hesapta kısa BTC aracı olarak yedek kalabilir. Midas'ta bulunurluğu doğrulanmadı. |
| GBTC | yedek | **IBIT ile eş birincil** | Midas'ta doğrulanmış tek spot BTC ETF'si. Ek maliyet yalnız ~2 bp. |
| ETHE | yedek | **ETHA ile eş birincil** | Midas'ta doğrulanmış. |
| ETHA | kabul | kabul | Kalabilir, ama "stratejisi yok, yalnız sürücüyle izleniyor" diye işaretlenmeli. |
| IBIT | kabul | kabul | Uygun; kabulü bir stratejiye değil, likiditeye ve sürücüye (BTC) dayanıyor. |
| Diğerleri | — | itiraz yok | BITX/BITI/ETHU/FBTC yedek; BITO, BITB, ARKB, BITU, BLOK, MSTU, CONL red. |

## Tekrar üretim

```
cd /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun
python3 -I kod/denetim_kripto/d_S1.py
python3 -I kod/denetim_kripto/d_S2.py
python3 -I kod/denetim_kripto/d_leadlag.py
python3 -I kod/denetim_kripto/d_ek.py
python3 -I kod/denetim_kripto/yaz_json.py
```

Betikler tek süreçle çalışır; toplam süre 15 saniyenin altında.
