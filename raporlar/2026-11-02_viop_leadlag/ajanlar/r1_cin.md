# r1_cin — Çin/Asya sürücüleri: TradingView'da açılan alternatifler ve BIST ilişkisi
Ajan: cin · Veri sonu: 30.10.2026 · Dosyalar: `out/cin_alternatifler.csv` (339 orijinal–alternatif çifti), `out/f_cin.csv` (474 satır = 237 hisse–sürücü çifti × {sync, lead_intra}), `out/code_cin/` (c01–c07, cin_lib.py, pairs_def.py, roll_check.csv, tio_dom.csv, orig_vs_alt_bist.csv, bist_pairs.csv)

## 1. Net bulgular

### 1a. Alternatifin orijinali ne kadar iyi temsil ettiği (haftalık getiri korelasyonu; ortak işlem günleri)
Vekil sadakat etiketi: YÜKSEK = haftalık r ≥ 0,80, 2 günlük r ≥ 0,70 ve son 3 yılın haftalık r'si ≥ 0,75. ORTA = haftalık r ≥ 0,60. DÜŞÜK = haftalık r ≥ 0,30. ÇOK DÜŞÜK = bunun altı.

| Orijinal (TV'de açılmıyor) | En iyi alternatif (TV adayı) | sync | 2g | haftalık | 3y haft. | n (gün) | Etiket |
|---|---|---|---|---|---|---|---|
| CSI 300 (SSE:000300) | AMEX:ASHR / CBOE:CNYA? / AMEX:KBA | 0,79 / 0,77 / 0,79 | 0,87 / 0,88 / 0,86 | 0,87 / 0,89 / 0,83 | 0,85 / 0,86 / 0,83 | 3050 / 2434 / 2974 | YÜKSEK |
| Şanghay Bileşik (SSE:000001) | ASHR / CNYA | 0,76 / 0,74 | 0,84 | 0,84 / 0,86 | 0,82 / 0,84 | 3050 | YÜKSEK |
| Shenzhen (SZSE:399001) | AMEX:CNXT | 0,80 | 0,86 | 0,85 | 0,86 | 2881 | YÜKSEK |
| ChiNext (SZSE:399006) | AMEX:CNXT | 0,82 | 0,89 | 0,89 | 0,88 | 2881 | YÜKSEK |
| SSE 50 | CNYA / ASHR | 0,72 / 0,75 | 0,83 / 0,82 | 0,83 / 0,82 | 0,81 / 0,82 | 2434 / 3050 | YÜKSEK |
| Hang Seng (HKEX belirsiz) | AMEX:FXI / NASDAQ:MCHI / AMEX:EWH | 0,62 / 0,63 / 0,62 | 0,79 / 0,79 / 0,77 | 0,87 / 0,86 / 0,84 | 0,84 / 0,84 / 0,79 | 4035 | YÜKSEK (haftalık) |
| HSCEI | FXI / FLCH / MCHI | 0,66 | 0,82 | 0,89 / 0,87 / 0,87 | 0,87 | 4035 | YÜKSEK |
| USD/CNH | FX:USDCNH zaten açılmalı (Çin borsası değil). Test: Yahoo CNY=X | 0,60 | 0,74 | 0,75 | 0,46 | 3114 | ORTA (veri kalitesi notu: CNY=X) |
| DCE demir cevheri | COMEX:TIO1! (TIO=F) | 0,42 | 0,57 | 0,60 | 0,60 | 1849 | ORTA (TIO1! sorunlu, bkz. 1c) |
| SHFE inşaat demiri / HRC | TIO=F; FMG.AX (ASX:FMG) | 0,37–0,38 | 0,44–0,45 | 0,47 | 0,47–0,48 | 1852 | DÜŞÜK |
| DCE kok / koklaşabilir kömür | NYSE:AMR, NYSE:HCC | 0,16–0,19 | 0,2–0,3 | 0,34–0,39 | 0,46–0,53 | 1336–1846 | DÜŞÜK |
| SHFE bakır | COMEX:HG1! / AMEX:CPER / AMEX:COPX | 0,41 / 0,34 / 0,37 | 0,64 / 0,61 / 0,55 | 0,68 / 0,69 / 0,65 | 0,54–0,59 | 1811 | ORTA |
| SHFE alüminyum | COMEX:ALI1! | 0,41 | 0,56 | 0,59 | 0,47 | 1751 | DÜŞÜK (sınırda) |
| SHFE nikel | ASX:IGO, HG=F | 0,22–0,26 | 0,26–0,29 | 0,32–0,35 | 0,28–0,39 | 1865 | DÜŞÜK |
| SHFE altın | COMEX:GC1! / AMEX:GLD | 0,41 / 0,36 | 0,69 / 0,56 | 0,73 / 0,75 | 0,73 / 0,75 | 1867 | ORTA |
| INE ham petrol | ICEEUR:BRN1! / NYMEX:CL1! | 0,34 / 0,28 | 0,59 / 0,53 | 0,77 / 0,73 | 0,80 / 0,76 | 1764 | ORTA |
| ZCE PTA / PX / PF | BRN1! | 0,26 / 0,31 / 0,27 | 0,47 / 0,49 / 0,45 | 0,54 / 0,60 / 0,52 | 0,56–0,60 | 1854 / 724 / 1415 | DÜŞÜK / ORTA / DÜŞÜK |
| DCE MEG, PP, LLDPE | BRN1! | 0,26–0,30 | 0,40–0,43 | 0,43–0,47 | 0,60–0,67 | 1759–1864 | DÜŞÜK |
| DCE PVC | BRN1! | 0,18 | 0,27 | 0,28 | 0,42 | 1856 | ÇOK DÜŞÜK |
| ZCE metanol | BRN1!; NASDAQ:MEOH | 0,26 / 0,18 | 0,37 / 0,29 | 0,42 / 0,34 | 0,58 / 0,43 | 1843 | DÜŞÜK |
| ZCE cam / soda külü | (HKEX:868 Xinyi), TSE:5201, NSE:TATACHEM | ≤0,20 | ≤0,18 | ≤0,26 | ≤0,33 | ~1600–1850 | ÇOK DÜŞÜK, iyi vekil yok |
| ZCE üre | CF, NTR, YAR, NG | ≤0,11 | ≤0,17 | ≤0,23 | ≤0,14 | 1684 | ÇOK DÜŞÜK, vekil yok |
| GFEX lityum karbonat | NYSE:ALB / SQM / LIT | 0,43–0,46 | 0,46–0,54 | 0,55–0,61 | 0,56–0,61 | 760 | DÜŞÜK–ORTA (kısa örneklem) |
| BYD H (1211.HK) | OTC:BYDDY / OTC:BYDDF | 0,84 | 0,93 | 0,95 | 0,90 | 4039 | YÜKSEK |
| BYD A (002594.SZ) | HKEX:1211 (belirsiz) / BYDDY | 0,71 / 0,62 | 0,73 / 0,68 | 0,74 / 0,72 | 0,86 / 0,80 | 3600 | ORTA |
| Haier A | HKEX:6690 (belirsiz) / OTC:HSHCY? | 0,77 / 0,64 | 0,84 / 0,77 | 0,87 / 0,79 | 0,79 / 0,77 | 1372 / 1168 | YÜKSEK / ORTA |
| Shandong Gold A | HKEX:1787 (belirsiz) | 0,80 | 0,83 | 0,83 | 0,88 | 1896 | YÜKSEK (HK açılırsa) |
| Conch (A/H) | OTC:AHCHY (H'ye karşı) | 0,66 | 0,74 | 0,71 | 0,94 | 4037 | ORTA |
| Zijin H | OTC:ZIJMF / AMEX:COPX | 0,45 / 0,35 | 0,56 / 0,53 | 0,75 / 0,60 | 0,78 / 0,67 | 4038 | ORTA |
| PetroChina H / Sinopec H | OTC:PCCYF / OTC:SNPMF; AMEX:FXI | 0,28 / 0,23; 0,39 | 0,42 / 0,31 | 0,57 / 0,46; 0,55 | 0,72 / 0,49 | ~3850–4040 | DÜŞÜK (OTC bayat fiyat) |
| CATL A | HKEX:3750 (2025+) / CNXT / LIT | 0,81 / 0,56 / 0,42 | 0,82 / 0,62 / 0,51 | 0,81 / 0,56 / 0,46 | — | 343 / 1962 | ORTA (HK) / DÜŞÜK |
| Midea, Gree, Hisense, TCL, Baosteel (yalnız A-pay) | ASHR / CNYA / KBA (H-payı varsa: 0300.HK Midea 0,63; 0347.HK Ansteel 0,66) | 0,41–0,48 | 0,45–0,56 | 0,44–0,51 | 0,21–0,44 | 3048 | DÜŞÜK. Şirkete özgü vekil yok |

### 1b. BIST tarafı: Çin sürücüsü, orijinal ile alternatif karşılaştırması (haftalık r, parantezde XU100 kontrollü haftalık kısmi korelasyon)
| Hisse | Orijinal Çin serisi | ABD/ASX alternatifi | Yorum |
|---|---|---|---|
| XU100 | CSI300 0,18; HSI 0,31; HSCEI 0,30 | ASHR 0,17; CNYA 0,16; FXI 0,28; EWH 0,30; MCHI 0,26 | Alternatifler orijinal kadar iyi. Çin A-pay piyasasının BIST ile bağı zayıf (günlük 0,10). |
| EREGL | SHFE HRC 0,25 (0,12); RB 0,24 (0,13); DCE I 0,22 (0,10); Baosteel? Ansteel 0,20 | SLX 0,42 (0,15); MT 0,38 (0,12); BHP 0,36 (0,13); PKX 0,35; RIO.AX 0,32 (0,19) | Alternatifin ham korelasyonu orijinalden YÜKSEK, çünkü küresel döngüsel ve dolar faktörünü de taşıyor. Kısmi korelasyonlar benzer (0,10–0,19). |
| KRDMD | SHFE HRC 0,27 (0,13); RB 0,25 (0,15) | SLX 0,33; FMG.AX 0,20 (0,17); 0347.HK 0,22 (0,20) | Benzer |
| TRALT | **SHFE altın 0,32 (0,29)** | GC=F 0,24 (0,11); GLD 0,26 (0,12); GDX 0,22 (0,15); 1787.HK 0,26 (0,20) | Çin altın fiyatı (CNY ve Çin primi dahil) TRALT'ı COMEX'ten daha iyi temsil ediyor. Bunun TV'de birebir karşılığı yok. |
| TRMET | SHFE altın 0,28 (0,26) | GC=F 0,22; COPX 0,26; 2899.HK 0,22 | Aynı örüntü |
| TUPRS | INE SC 0,33 (0,35) | BZ=F 0,26 (0,27); 0857.HK 0,27 | INE biraz daha iyi; muhtemel sebep zaman penceresi (SC_t, BIST t-1 seansı ile gecesini kapsıyor) |
| SISE | Cam/soda külü (Sina) haftalık < 0,2 | SGO.PA 0,26 (0,04) | Çin cam/soda külü sinyali yok. SGO yalnızca piyasa faktörü taşıyor. |
| SASA | PTA/PX/PF/MEG ≤ 0,13 | IVL.BK, 1326.TW, CL=F ≤ 0,13 | İlişki yok (DÜŞÜK / ÇOK DÜŞÜK) |
| PETKM | PP/L/PVC/MEG/MA ≤ 0,15 | LYB 0,15; WLK 0,14 | Zayıf |
| ARCLK / VESTL | Midea/Haier/Gree/TCL ≤ 0,17 | WHR 0,19; ELUX 0,17; CHIQ 0,17 | "Çin rekabeti" günlük ya da haftalık getiride görünmüyor. Bu ilişki yapısal/uzun vadeli bir hipotez olarak kalıyor. |
| FROTO / TOASO / DOAS | BYD, CATL zayıf | KARS 0,29 / 0,25 / 0,21; CHIQ 0,23 | Zayıf, piyasa faktörü baskın |
| GUBRF | ZCE üre 0,04 | YAR.OL 0,10 | Yok |
| CIMSA / OYAKC | Conch 0,04–0,08 | 0914.HK 0,08–0,14 | Yok |
| ASTOR | XD Electric 0,10; TBEA 0,11; Sieyuan 0,08 | HG=F, COPX zayıf | Zayıf (n = 940, 2023 sonrası) |

### 1c. En güçlü 10 bulgu (güven etiketiyle)
1. **CSI300/SSE/SZSE → ASHR, CNYA, KBA, CNXT**: haftalık r 0,83–0,89, 3 yıllık 0,82–0,88. Vekil sadakati YÜKSEK. Günlük senkron r yalnızca 0,74–0,82: ABD ETF'leri ~13 saat sonra kapanıyor ve ertesi günün Çin hareketini kısmen önceden fiyatlıyor (alt_t → orig_{t+1} r = 0,10–0,16).
2. **HSI/HSCEI → FXI / MCHI / EWH**: haftalık r 0,84–0,89 (YÜKSEK), günlük 0,62–0,66 (kapanış farkı ~12–13 saat; alt_t → orig_{t+1} r = 0,29). BIST için temsil gücü orijinale eşit (XU100 haftalık: HSI 0,31, EWH 0,30, FXI 0,28).
3. **BYD H → OTC:BYDDY / BYDDF**: haftalık r 0,95, n = 4039. YÜKSEK.
4. **TRALT ← Çin altını (SHFE AU)**: haftalık r 0,32, kısmi 0,29. Senkron sync FDR'den geçiyor, etiket YÜKSEK. COMEX altını daha zayıf (haftalık kısmi 0,11). TV'de karşılığı olmadığı için pratik vekil COMEX:GC1! (ORTA) + FX:USDCNH.
5. **1787.HK (Shandong Gold H) → TRALT gün-içi** (HK kapanışı t → BIST açılış→kapanış t): t = 4,15; OOS Sharpe 0,55; net 10,7 bps/işlem; etiket YÜKSEK. **Uyarı:** HK kapanışı 08:00 UTC, BIST açılışından 1 saat sonra. Bu yüzden tam işlenebilirlik saatlik veriyle doğrulanmadı ve sonuç bu haliyle iyimser. 600547.SS (07:00 UTC) için t = 3,34, OOS 6,7 bps. 2899.HK için t = 3,84.
6. **SHFE HRC → KRDMD gün-içi**: t = 3,33, OOS Sharpe 0,65, 11,7 bps; ORTA (FDR geçti). SHFE RB için t = 3,12 (ORTA).
7. **FMG.AX (ASX kapanışı 05–06 UTC) → KRDMD / EREGL / BRSAN gün-içi**: t = 4,39 / 3,87 / 3,51, OOS Sharpe 0,80 / 0,19 / 0,28; ORTA. Korelasyon küçük (0,06–0,08) ve maliyete duyarlı.
8. **INE SC → TUPRS**: haftalık r 0,33 (kısmi 0,35); günlük sync YÜKSEK. Alternatif BRN1! (haftalık 0,26); INE SC ile BRN1! arasında haftalık r 0,77.
9. **EREGL ↔ SLX / MT / BHP**: haftalık r 0,36–0,42, Çin çelik vadelilerinden (0,22–0,25) yüksek. Kısmi korelasyonlar ise benzer (~0,12–0,15), yani fark büyük ölçüde ortak küresel döngü faktöründen geliyor.
10. **COMEX:TIO1! sorunlu**: Yahoo'daki TIO=F ön ayı aylık ortalama fiyatlı bir kontrat. Mutlak günlük getirisi ay başında %2,13, ay sonunda %0,24'e düşüyor; DCE ile korelasyonu 0,64'ten 0,43'e iniyor (`tio_dom.csv`). **Öneri: COMEX:TIO2! veya SGX:FEF2! kullanmak** (bu iki kontrat test edilmedi; ticker'lar '?').

### 1d. Olumsuz bulgular
- SASA–PTA/PX/MEG, PETKM–PP/PE/PVC, SISE–cam/soda külü, GUBRF–üre, CIMSA/OYAKC–Conch, ARCLK/VESTL–Çin beyaz eşyası: haftalık r ≤ 0,17 ve kısmi korelasyon ~0. Günlük frekansta Çin emtia/rakip sinyali yok (DÜŞÜK / ÇOK DÜŞÜK; listeden çıkarılmadı).
- Cam, soda külü, üre ve PVC için TV'de açılabilecek anlamlı vekil bulunamadı (haftalık r < 0,3).
- XU100–USDCNH gün-içi "öncülüğü" (t = -2,7) GEÇERSİZ: Sina CNH kapanışı UTC günü sonu, dolayısıyla seri eşzamanlı. f_cin.csv'de işaretlendi.

## 2. Yöntem
- **Orijinal veri:** Yahoo'nun 000300.SS, 000016.SS, 000905.SS, 399006.SZ, XIN9.FGI ve CNH=X için tüm parametrelerde **tek satır** döndürdüğü görüldü. Bu seriler Sina'dan alındı (`c03`). Çapraz kontrol: SSE Sina–Yahoo günlük r = 0,9995.
- **Çin vadelileri (DCE/SHFE/ZCE/INE/GFEX, 29 kontrat kodu):** Sina sürekli serisinin roll gürültüsü büyük (ham ile düzeltilmiş arasındaki korelasyon: I 0,93, SA 0,87; `roll_check.csv`). Bu yüzden tekil kontratlardan, bir önceki günün maksimum açık pozisyonuna göre ve yalnızca ileri vadeye geçen bir **roll-düzeltilmiş seri** kuruldu. Tekil kontrat verisi 2018-05'ten itibaren mevcut olduğundan analiz dönemi yaklaşık **2018-12 → 2026-10** (~1.900 gün).
- **Zamanlama:** Çin kapanışı 07:00 UTC (BIST sürekli işlem açılışıyla aynı an), HK 08:00 UTC. Çin vadelilerinde gece seansı ertesi işlem gününe yazılıyor. Bu nedenle D_t penceresi (07:00 t-1, 07:00 t] ve BIST t-1 seansını da içeriyor. ABD ETF/ADR/OTC kapanışı 20/21 UTC, COMEX ~17–19 UTC. FX_FIX'li ll kullanıldı.
- **Orijinal ile alternatif:** ortak işlem günlerinde senkron, alt_t → orig_{t+1}, örtüşmeyen 2 günlük ve Cuma–Cuma haftalık getiri. Kapanış farkı nedeniyle esas ölçüt haftalık getiri.
- **BIST:** ll.ret ve ll.decomp. Asya sürücüsünde D_t → gün-içi_t, ABD sürücüsünde A_{t-1} → gün-içi_t işlenebilir öncülük olarak test edildi. ll.backtest: 10 bps maliyet, IS < 2021 ≤ OOS. Yıllara göre işaret istikrarı, USD bazlı korelasyon ve XU100 kısmi korelasyonu hesaplandı.
- **Çoklu test:** 237 senkron + 237 gün-içi test, BH q = 0,05 (iki ayrı aile). Senkronda 191 test, gün-içinde 18 test geçti. Senkronda geçenlerin çoğu çok küçük etkiler; büyük n nedeniyle anlamlı çıkıyorlar.

## 3. Karşı argümanlar ve sınırlamalar
- Alternatiflerin BIST ile ham korelasyonunun orijinalden yüksek çıkması (ör. SLX ile Baosteel: 0,32'ye karşı 0,13) "alternatif daha iyi Çin göstergesi" anlamına gelmiyor. Fark, ABD seansının BIST seansıyla örtüşmesinden ve ortak küresel faktörden geliyor.
- Gün-içi öncülük etkileri küçük (r 0,05–0,10). Maliyet 15 bps'ye çıkarsa birkaçı sıfırlanır. IS dönemi vadelilerde yalnızca 2019–2020. HK için 08:00 UTC örtüşmesi saatlik veriyle temizlenmedi. Hiçbiri nedensellik kanıtı değil.
- Sina verisi kamuya açık ama resmî değil. Roll kuralı yaklaşık. Sina CNH'nin kapanış saati belirsiz (korelasyon örüntüsüne göre UTC günü sonu). Yahoo CNY=X'in son 3 yıllık kalitesi şüpheli.
- OTC ADR'ler (SNPMF, PCCYF, ZIJMF, CMCLF) seyrek işlem görüyor: günlük korelasyonları düşük, haftalık korelasyonları daha yüksek.

## 4. TradingView / HKEX notları ve yapılmayanlar
- HKEX: `HKEX:` hisse ticker'ları ve `HSI:HSI` endeksi açılmayabilir (doğrulanmadı). Güvenli alternatifler AMEX:FXI, NASDAQ:MCHI ve AMEX:EWH (HSI'ya haftalık r 0,84–0,87). TVC:HSI ve HSI:HSI ise '?'.
- **Yapılmadı:** CFD'lerin testi (OANDA:CN50USD, CAPITALCOM:CN50, OANDA:HK33HKD; bu seriler veri kaynağımızda yok), SGX:FEF / SGX:CN1! / COMEX:TIO2! / LME:MCU1!? / LME:MAL1!? (veri yok, '?'; LME abonelik gerektirebilir), saatlik HK hizalaması, SHFE–COMEX altın primi sentetiği, 47 hissenin tamamında Çin taraması (yalnız ilgili hisseler + XU100/XU030 test edildi), 2018 öncesi vadeli dönemi.
