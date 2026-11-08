# KOLD — ProShares UltraShort Bloomberg Natural Gas

**TradingView:** `AMEX:KOLD` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı · ⚠ PTP/K-1 ürünü: satışta %10 brüt kesinti (1446(f)) riski

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 97 | 16.0 | 684 | %-38.4 | -2.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** [PTP] maliyet/oynaklık 0.023. S1 adayının aracı (-2x doğalgaz, 97 mn$, 16 bp). Koşullu: Midas'ta bulunurluk doğrulanamadı; ProShares Trust II PTP (26.02.2026 bildirimi 92 gün geçerliydi, sonrası kontrol edilmedi). Kaldıraç bozulması: koşulsuz günlük ort. -10 bp; yalnız 1 günlük tutuş için. **Ana ajan notu:** Koşullu: S1 zayıf; PTP; Midas'ta doğrulanmadı.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt — tek başına işlem gerekçesi değil)

#### EIA doğalgaz depolama raporu öncesi KOLD (yalnız Kasım-Mart)  
*İzlemede — zayıf kanıt · güven: dusuk · id: `enerji_tarim_S1`*

- **Sinyal (t kapanışında):** Takvim kuralı, fiyat göstergesi yok. EIA haftalık doğalgaz depolama raporunun (ir.eia.gov/ngs/schedule.html; normalde Perşembe 10:30 ET = TR 18:30 kış / 17:30 yaz; tatil haftalarında kayar) tarihi Kasım, Aralık, Ocak, Şubat veya Mart ayındaysa: rapordan bir önceki ABD işlem günü AMEX:KOLD (-2x doğalgaz) kapanışta alınır, rapor günü kapanışta satılır. Nisan-Ekim raporlarında işlem yok. Sinyal verisi: yalnız takvim; izleme: NYMEX:NG1! ve AMEX:KOLD.
- **Giriş:** Rapordan önceki işlem günü ABD kapanışına yakın: kış saatinde TR 23:45-23:59 (yaz 22:45-22:59) piyasa emri (MOC/LOC yok) ya da kapanış sonrası after-hours limit (TR 00:00-04:00; backtest kapanış fiyatını varsayar). Alternatif O1: rapor günü açılışta (TR 17:30 kış), rapordan önce al -> net daha düşük (aşağıda). Yakın tarihler: 12 Kas 2026 Per (rapor 13 Kas Cum), 18 Kas Çar, 24 Kas Sal (rapor 25 Kas Çar 12:00 ET = TR 20:00), 2 Ara, 9 Ara, 16 Ara, 23 Ara, 30 Ara.
- **Tutuş / çıkış:** 1 işlem günü (rapor günü kapanışına kadar) — Rapor günü ABD kapanışından dakikalar önce (TR ~23:45-23:59 kış) sat. Backtest stop kullanmaz; tek işlemde -%16'ya varan kayıp görüldü.
- **İşlem aracı:** KOLD (sinyal: takvim: data/events/eia_ng_storage.csv (EIA))
- **Geçmiş (ajan):** n=216, net 100.5 bp/işlem (brüt 116.5), kazanma %58, t=2.24, IS 113.4 / OOS 85.5 bp, yılların %64'i pozitif, en kötü işlem -1664 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500$):** C0: net 118 bp (t 2.5, n=203) · O1: net 79 bp (t 2.5, n=203) · C1: net -27 bp (t -0.6, n=203); 1.000$ pozisyonda ana mod net 100 bp (t 2.1)
- **Denetçi düzeltmesi:** Sayılar doğru. Ek: en iyi 10 hariç net 21,6 bp t 0,58; 2020 hariç t 1,84; 1.000$'da t 1,84; kış-yaz farkı t 1,78; dürüst (önceden belirlenmiş) tahmin tam yıl net 43 bp t 1,65.
- **Denetçi kural düzeltmesi:** Kural aynı; ancak 'aday strateji' değil 'izlenecek hipotez' olarak sunulmalı. Uygulanırsa: yalnız PTP kesintisi olmadığı teyit edilirse, küçük pozisyon (≥2.500$, 1.000$'da t<2), O1 girişi (rapor günü TR 17:30, rapor TR 18:30'dan önce) eşdeğer alternatif; 24 Ara 2026 erken kapanış ve rapor kayması kontrolü.
- **Denetim:** Bağımsız simülatörle (dsim.py; lib.trades/evaluate kullanılmadı) birebir: n=216, brüt 116,5 / net 100,5 bp, t 2,24, kazanma %58, PF 1,53, IS 113 bp (t 1,97) / OOS 86 bp (t 1,22), yıl+ 7/11, maxDD -%41,7, en kötü -1.664 bp; tüm C0/O1/C1 x h1-3 ızgarası ve UNG/BOIL/UNL ayna sonuçları da aynı. Rapor günlerinin hepsi KOLD dizininde; giriş arife kapanışı, çıkış rapor günü kapanışı; takvim önceden bilinir, ileriye bakma yok. KOLD~UNG yıllık beta -1,64..-1,93 (kaldıraç değişmemiş). En iyi 5 işlem (2018-11-15 +4.233 bp, 2024-11-27, 2022-02-03, 2020-12-03, 2023-01-05) gerçek doğalgaz çöküşleri, veri hatası yok. Sağlamlık: Lehte: %2,5 iki yanlı winsorize net 88 bp t 2,27; medyan işlem +114 bp brüt, işaret testi p 0,004; permütasyon p 0,005 (tüm günler), 0,023 (Kas-Mar günleri), 0,006 (Kas-Mar arife dışı); O1 h1 (rapor günü açılış, TR 17:30) net 64,5 bp t 2,13 -> kapanışa bağımlı değil; 2022 hariç t 2,55; 2020+2022 hariç t 2,13; komşu mevsimler (Eki-Mar 2,35, Kas-Nis 2,26, Kas-Şub 2,23) benzer ama Ara-Mar 1,64, Ara-Şub 1,60. Aleyhte: yukarıdaki sorunlar. Maliyet: 1.000$ 82,5 (t 1,84) / 2.500$ 100,5 (2,24) / 10.000$ 109,5 (2,44).
- **Denetçinin uyarıları:** (1) Kış (Kas-Mar) ayrımı post-hoc ve istatistiksel olarak desteklenmiyor: kış-yaz farkı t 1,78 (p 0,076), aylar arası ANOVA p 0,67 / Kruskal p 0,76; önceden belirlenmiş tam yıl versiyonu t 1,65 (eşik altı) dürüst tahmindir. (2) Kuyruğa bağımlı: en iyi 5 hariç net 52 bp t 1,34; en iyi 10 hariç 22 bp t 0,58 (OOS -18). (3) 2020 hariç t 1,84; Kasım 2018 hariç t 1,96; 1.000$ pozisyonda net 82,5 bp t 1,84 (<2). (4) OOS t 1,22; FDR geçmiyor (p 0,013; 8.635 testte eşik 1,2e-5, 319 aileye özel testte 3,1e-4). (5) Haftanın günü karışması ayrıştırılamıyor (kış Pazartesi hedefli günler de +92 bp; tatil kaymalı rapor n=22). (6) KOLD PTP (ProShares Trust II): %10 brüt kesinti -> ≈ -900 bp/işlem; Midas'ta bulunurluk doğrulanamadı. (7) 24 Ara 2026 rapor günü NYSE erken kapanış (13:00 ET = TR 21:00) ve olası federal kapanış kararnamesiyle rapor 23 Ara 12:00 ET'ye kayarsa giriş 22 Ara olur; strateji metninde uyarı yok.
- **Giriş zamanı sağlamlığı:** C0 h1: brüt 116 / net 100 bp (t 2.24); C0 h2: brüt 106 / net 90 bp (t 1.43); C0 h3: brüt 209 / net 193 bp (t 2.19); O1 h1: brüt 81 / net 65 bp (t 2.13); O1 h2: brüt 73 / net 57 bp (t 1.00); O1 h3: brüt 180 / net 164 bp (t 1.95); C1 h1: brüt -10 / net -26 bp (t -0.58); C1 h2: brüt 97 / net 81 bp (t 1.07); C1 h3: brüt 49 / net 33 bp (t 0.37). C1 negatif beklenen bir sonuç: etki rapor gününün kendisinde; O1 (rapor günü açılışta giriş) net 64,5 bp t 2,13 ile ayakta.
- **Maliyet duyarlılığı:** net bp: 1.000$ 82.5 / 2.500$ 100.5 / 10.000$ 109.5 (KOLD makas 4 bp)
- **Not:** IS t 1.97, OOS t 1.22 (ikisi de pozitif ama tek başına anlamsız). Kasım-Mart ayrımı tam yıl sonucu görüldükten SONRA eklendi (post-hoc); literatür (Prokopczuk ve diğ. 2021: rapor günü NG -%0,37) yönü destekliyor ama 2014-2018 alt döneminde etki yok demişti. Getiri kalın kuyruklu (en iyi işlem +%42, en kötü -%16, maxDD -%42). KOLD Midas'ta doğrulanamadı; ProShares Trust II PTP: %10 brüt satış stopajı uygulanırsa işlem başına ~-1000 bp => beklenti ~-900 bp. Her işlemden önce uygulamada PTP ibaresi/kesinti kontrol edilmeli; kesinti varsa İŞLEM YAPMA. Risk notu (aynı bulgu): UNG/BOIL long pozisyonu Çarşamba kapanışından Perşembe (rapor) kapanışına taşımayın (UNG rapor günü brüt ort. -28 bp; brüt yıl ortalaması 2018-2026'nın 9 yılının hepsinde negatif).
- Betik: `/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_enerji_tarim/aday_S1_eia_kold.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| UNG | `AMEX:UNG` | -0.97 | -1.81 |
| UNL | `AMEX:UNL` | -0.93 | -2.96 |
| USL | `AMEX:USL` | -0.24 | -0.82 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| EIA doğalgaz depolama raporu takvimi (Kasım-Mart) — takvim olayı, gecikmeli fiyat öncüsü değil | yok (takvim: ir.eia.gov/ngs/schedule.html) | takvim_olayi (doğrulanmamış: FDR geçmiyor, post-hoc mevsim ayrımı) | 1 gün (rapor günü) | Kas-Mar rapor günü KOLD +95 bp (diğer günler -20 bp); S1 net +100 bp (2.500$) | 2.2 (2.0/1.2) | KOLD +100 bp net; UNG/BOIL long negatif | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Henry Hub doğalgaz vadelisi (ön ay) | `NYMEX:NG1!` | dayanak; Globex'te gece işler |
| Doğalgaz 2. ay | `NYMEX:NG2!` | NG2!/NG1!-1 kontango göstergesi |
| Hollanda TTF gaz vadelisi | `ICEENDEX:TFM1!` | Avrupa gazı; ABD açılışından önce işler |

## 3. Takvim ve olay riskleri

EIA depolama: 13 Kas Cum, 19 Kas, 25 Kas Çar 12:00 ET, 3/10/17/24/31 Ara (TR 18:30); NG vadesi 25 Kas, 29 Ara; UNG roll 11-16 Kas, 15-18 Ara; BOIL/KOLD roll 8-14 Ara 2026.

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 16 bp maliyet; geçen 0). En güçlü geçmeyen: KWEB h3 t=-2.17 (IS -1.84/OOS -1.38, -50.8 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(UNG) h1 t=-0.85 (IS -0.96/OOS -0.43, -14.2 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
