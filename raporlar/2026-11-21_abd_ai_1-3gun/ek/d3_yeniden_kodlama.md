araç: 25/40

# D3 — Bağımsız yeniden kodlama (protokol madde 12, ölçüt 9) ve günlük sinyal aracı

Tarih: 22.11.2026. Kod yalnız `kod/PROTOKOL.md` ve ham veriden (veri/gunluk, veri/bilanco, veri/bolunme.csv, veri/fomc.csv) sıfırdan yazıldı. `ortak.py`, `b1_fiyat.py`, `b2_leadlag.py`, `b3_takvim.py` ve `*_islemler.csv` okunmadı, içe aktarılmadı. Kör sonuç hedef sayılara bakılmadan `veri/sonuc/yeniden_kodlama_kor.csv` dosyasına yazıldı.

Dosyalar:
- `kod/yeniden_kodlama.py`: bağımsız backtest (tanım seçenekleri bayrakla değiştirilebilir)
- `kod/sade_tablo.py`: son karşılaştırma dosyası + madde 3 sade tablolar
- `kod/sinyal.py`: günlük sinyal aracı (yalnız pandas, numpy, yfinance)
- `veri/sonuc/yeniden_kodlama_kor.csv`, `veri/sonuc/yeniden_kodlama.csv`, `veri/sonuc/yeniden_kodlama_sade.md`
- `ek/d3_sinyal_20kasim.txt`: 20 Kasım 2026 kapanışı için aracın çıktısı

## 1. Kör turda kullanılan tanımlar (protokolden okunan)

| Konu | Kör tanım |
|---|---|
| Giriş / çıkış | t kapanışı → t+h kapanışı, AClose'tan basit getiri, bps |
| Bozuk satır | ham O/H/L/C ile High < max(O,C), Low > min(O,C), High = Low (kesin karşılaştırma) |
| 3 $ eşiği | **bölünmemiş** fiyat (yfinance Close × t'den sonraki bölünme oranları, `bolunme.csv`) |
| Ciro | Close × Volume, t dahil 20 günlük medyan ≥ 20 milyon $ |
| Geçmiş | t'den önce en az 250 bar |
| Tek pozisyon | açık pozisyon çıkış gününden önce gelen sinyal atılır (h=1'de etkisiz) |
| Bilanço maskesi | F1–F5: tepki günü [t, t+h] içindeyse işlem atılır (T ETF'lerinde bilanço yok) |
| Tepki günü | "sonra" → ertesi işlem günü; "once"/"seans" → aynı gün (hafta sonuysa sonraki işlem günü); "bilinmiyor" → aday iki günden göreli hacmi (hacim / önceki 20 gün ort.) büyük olan |
| Ç evreni | `veri/bilanco` içindeki hedef hisselerden ilk günlük verisi ≤ 2016-01-01 olan 40 hisse |
| Alfa (4.1) | getiri − aracın giriş dönemindeki (P1/P2/P3) tüm günlerin ortalama günlük getirisi × h |
| t | giriş tarihine göre kümeli (CR1) standart hata |
| F3 | en az 3 üst üste düşük kapanış (seri ≥ 3; seri sürdükçe her gün sinyal) |
| F4b | r_t > 2 × σ(r), σ: t−1'e kadar 60 gün |
| F11 | ^SOX AClose günlük değişimi (t barı) ≤ −%3 / ≥ +%3 → SMH, SMH'de sinyal koşulları |
| F9b | A = duyurudan önceki son kapanış (A'da sinyal koşulları), çıkış tepki günü kapanışı (hepsi h=1 çıktı) |
| F1d | F1a işlemleri (Ç+T, maskeli) alfa ~ 1 + 1[VIX_t ≥ 25], kümeli; katsayı = fark |
| Son 12 ay | giriş ≥ 2025-11-21; P3 sabitinden arındırılmış alfa ortalaması |

## 2. Test başına sonuç

Ölçüt: n_islem ±%1 ve alfa ±1 bps. Kör tur hedefle **iki ondalığa kadar birebir** tuttu; bu yüzden tanım hizalaması gerekmedi ve `ek/d2_b*.md` sapma bölümlerine başvurulmadı. Son sonuç = kör sonuç.

| Test | Kör n | Kör alfa | t_kume | P1 / P2 / P3 | Son 12 ay (n) | Hedef n / alfa | Fark | Karar |
|---|---|---|---|---|---|---|---|---|
| F1a_T_h1 | 4350 | +17,21 | 3,08 | +7,9 / +37,9 / +17,3 | +32,0 (268) | 4350 / +17,21 | 0 / 0,00 | TUTTU |
| F3_T_h1 | 1996 | +18,92 | 2,61 | +8,2 / +36,2 / +26,8 | +11,2 (134) | 1996 / +18,92 | 0 / 0,00 | TUTTU |
| F9b_C_h1 | 2079 | +57,66 | 2,97 | +90,4 / +38,6 / +14,3 | −94,2 (161; t −1,10) | 2079 / +57,66 | 0 / 0,00 | TUTTU |
| F11a_SMH_h1 | 226 | +43,35 | 2,13 | +26,4 / +66,2 / +36,0 | +20,2 (39) | 226 / +43,35 | 0 / 0,00 | TUTTU |
| F11b_SMH_h1 | 220 | −42,22 | −2,44 | −8,7 / −109,8 / −1,3 | +30,5 (32) | 220 / −42,22 | 0 / 0,00 | TUTTU |
| F4b_T_h1 | 628 | −40,63 | −2,28 | −18,3 / −121,1 / −16,7 | +32,1 (48) | 628 / −40,63 | 0 / 0,00 | TUTTU |
| F1d_CT_h1 | 30587 | +56,86 | 2,44 | +40,0 / +58,8 / +85,3 | −20,0 | 30587 / +56,86 | 0 / 0,00 | TUTTU |
| (F1a_C_h1, ek) | 26237 | +14,16 | 2,52 | +6,0 / +32,4 / +14,3 | +43,8 | 26237 / +14,16 | 0 / 0,00 | TUTTU |

Net alfa da tuttu: F1a_T +7,21, F9b_C +40,43, F3_T +8,92, F11a +33,35. Tek fark: F1d'de `n_son12` hedefte 316, bende 2284 (ben son 12 aydaki tüm F1a Ç+T işlemlerini sayıyorum; hedef büyük olasılıkla yalnız VIX ≥ 25 işlemlerini sayıyor). alfa_son12 (−20,02) aynı; karar etkilenmez.

### Tanım duyarlılığı (yalnız bilgi; bayrakla yeniden koşuldu)

| Varyant | Etkilenen test | Sonuç |
|---|---|---|
| 3 $ eşiği **düzeltilmiş Close**'a | F9b_C | n 2044, alfa **+51,54**, t **2,64** (kör: 57,66 / 2,97) |
| 3 $ eşiği AClose'a | F9b_C | n 2026, alfa +49,55, t 2,52 |
| F3 = **tam** 3 düşük kapanış | F3_T | n 1145, alfa +20,30, t 2,27 |
| Bilanço maskesi kapalı | F1a_C, F1d | F1a_C 27169 / +15,48; F1d +54,63 (T testleri değişmez) |
| Ciro medyanına t hariç | hepsi | en çok 5 işlem, ≤ 0,3 bps |
| Bozuk satırda 1e-6 tolerans | hepsi | değişiklik yok |
| Son 12 ay kendi ortalamasıyla | son 12 sütunu | F9b −89,2 (−94,2 yerine) |

Yorum: F9b, 3 $ eşiğinin hangi fiyata uygulandığına duyarlı. Protokoldeki "fiyat ≥ 3 $" en doğal okumayla o gün gerçekten işlem gören (bölünmemiş) fiyattır; iki bağımsız kod da bunu seçti, bu yüzden hata değil. Ama F9b'nin t'si 2,97'den 2,64'e iniyor: bulgu eşik seçimine kırılgan. F9b'de en iyi %1 işlem (21 işlem) çıkınca alfa +26,9 bps'e iniyor; tek bir hisse (AAOI, 19 işlem, ortalama +693 bps) çıkınca yaklaşık +51,8. Son 12 ay −94 (t −1,1) "soluyor" notunu doğruluyor.

Diğer sağlamalar: F1a_T'de en iyi %1 çıkınca alfa +9,8; F11a'da +6,6 (işaret korunuyor ama F11a'nın kenarı büyük ölçüde birkaç kriz gününden geliyor: 2020-03, 2025-04-08).

## 3. Betimsel sayıların sağlaması

| İddia | Benim sonucum | Karar |
|---|---|---|
| STRES (VIX ≥ 30) hücresinde F1a_T ortalama +98 bps, n 445, 18 epizot | n 445, **alfa** +98,5, ham ortalama +104,9; 101 gün; epizot (arada ≥ 10 işlem günü) 18 | TUTTU ("ortalama" = alfa) |
| SMH ≤ −%8 günleri 9 | 9 gün: 2020-03-09/12/16/18, 2025-01-27, 2025-04-03, 2026-06-05, 2026-11-05, **2026-11-20** (sonrası yok) | TUTTU |
| Ertesi gün SMH +360 bps (7/8), 3 günde +1 | h1 +360 (7/8), h2 +27, h3 +1 (6/8 pozitif) | TUTTU |
| SOXL h1 +875, h3 −416 | h1 +875 (7/8), h2 −155, h3 −416 (3/8) | TUTTU (NVDA: h1 +493, h3 −94) |
| Taşıma: F1a SOXL +100 bps/işlem (n 524), TQQQ +38 | SOXL n 524, alfa +99,6 (ham +127,7); TQQQ n 700, alfa +38,4 (ham +58,3) | TUTTU (sayılar alfa) |
| Saatlik tanı: SMH ≤ −%3 ve son 30 dk aşağı (n 41) → ertesi gün +85; yukarı (n 24) → −3 | "son 30 dk" = **Yahoo 15:30 saatlik barının kapanış/açılış** oranıyla: 41 / +85, 24 / −3 → birebir. "son 30 dk" = **resmî günlük kapanış / 15:30 fiyatı** ile: aşağı n 37, +64; yukarı n 28, +37 | TANIM FARKIYLA TUTTU — dikkat |

Saatlik tanıyla ilgili bulgu: Yahoo'nun 15:30 saatlik barının "kapanışı" kapanış müzayedesini içermeyen son işlem fiyatıdır; resmî kapanış fiyatı (giriş fiyatı) farklıdır. Gerçek giriş fiyatı olan resmî kapanışla ölçülünce iki grup arasındaki fark 88 bps'ten 27 bps'e iniyor ve "yukarı" grubu da pozitif (+37). Bu tanı karar kuralı olarak kullanılmamalı; en fazla zayıf bir betimsel not.

## 4. Sade sağlama tabloları (sabit etkisiz, protokolden bağımsız)

Sinyal günü = backtest işlem giriş günü (filtreler uygulanmış). "Diğer" = aynı aracın 2010–2026 arasındaki bütün diğer günleri. Değerler 1 günlük ortalama getiri, bps.

Özet: F1a_T sinyal sonrası ortalama +24,7 bps, diğer günler +3,9 (fark +20,7); 6 ETF'in hepsinde fark pozitif; 17 yılın 15'inde fark pozitif. F3_T: +26,4'e karşı +5,9 (fark +20,5), 6/6 ETF, 16 yılın 13'ü. F11a: +54,9'a karşı +7,5 (fark +47,4), 16 yılın 12'si; ancak yıllık örneklemler küçük (3–39 gün) ve fark 2020 (+192) ile 2019/2018/2025'te yoğun.

### F1a_T (IBS < 0,2)

Arac arac (2010-2026, sinyal gunu sonrasi 1 gunluk ortalama getiri vs diger butun gunler):

| araç | sinyal_ort_bps | sinyal_n | diger_ort_bps | diger_n | fark_bps |
|---|---|---|---|---|---|
| IWM | 13 | 784 | 2.9 | 3463 | 10.1 |
| QQQ | 23.5 | 701 | 4.1 | 3546 | 19.4 |
| SMH | 32.9 | 803 | 4.7 | 3444 | 28.2 |
| SOXX | 43.8 | 602 | 4 | 3645 | 39.8 |
| SPY | 12.7 | 706 | 4.1 | 3541 | 8.6 |
| XLK | 25 | 754 | 3.7 | 3493 | 21.3 |
| toplam | 24.7 | 4350 | 3.9 | 21132 | 20.7 |

Yil yil (araclar havuzlanmis):

| yil | sinyal_ort_bps | sinyal_n | diger_ort_bps | diger_n | fark_bps |
|---|---|---|---|---|---|
| 2010 | 53.9 | 2 | 7 | 1510 | 46.9 |
| 2011 | 26.5 | 293 | -5.6 | 1219 | 32 |
| 2012 | 5.8 | 219 | 6.5 | 1281 | -0.6 |
| 2013 | 16.7 | 196 | 9.5 | 1316 | 7.1 |
| 2014 | 11.2 | 226 | 7 | 1286 | 4.2 |
| 2015 | -9.6 | 315 | 3.5 | 1197 | -13.1 |
| 2016 | 16.8 | 267 | 7.4 | 1245 | 9.4 |
| 2017 | 45.7 | 188 | 6.3 | 1318 | 39.4 |
| 2018 | 11.1 | 336 | -5.4 | 1170 | 16.4 |
| 2019 | 19.1 | 221 | 15.3 | 1291 | 3.8 |
| 2020 | 94 | 331 | -6.7 | 1187 | 100.7 |
| 2021 | 24.2 | 295 | 10.1 | 1217 | 14.1 |
| 2022 | 15.6 | 385 | -21.0 | 1121 | 36.7 |
| 2023 | 23.4 | 325 | 13.9 | 1175 | 9.5 |
| 2024 | 15.8 | 285 | 8.8 | 1227 | 6.9 |
| 2025 | 35.6 | 232 | 7.4 | 1268 | 28.2 |
| 2026 | 41.5 | 234 | -3.1 | 1104 | 44.5 |

Farkin pozitif oldugu yil: **15 / 17** (sinyal olan yillar). Sinyal gunu ortalamasinin kendisi pozitif olan yil: 16 / 17.

### F3_T (3+ dusuk kapanis)

Arac arac (2010-2026, sinyal gunu sonrasi 1 gunluk ortalama getiri vs diger butun gunler):

| araç | sinyal_ort_bps | sinyal_n | diger_ort_bps | diger_n | fark_bps |
|---|---|---|---|---|---|
| IWM | 21.3 | 372 | 3.2 | 3875 | 18.1 |
| QQQ | 30.8 | 320 | 5.3 | 3927 | 25.5 |
| SMH | 29.9 | 379 | 8.1 | 3868 | 21.8 |
| SOXX | 24.7 | 269 | 8.7 | 3978 | 16 |
| SPY | 21.3 | 337 | 4.2 | 3910 | 17.1 |
| XLK | 30.4 | 319 | 5.6 | 3928 | 24.8 |
| toplam | 26.4 | 1996 | 5.9 | 23486 | 20.5 |

Yil yil (araclar havuzlanmis):

| yil | sinyal_ort_bps | sinyal_n | diger_ort_bps | diger_n | fark_bps |
|---|---|---|---|---|---|
| 2010 | nan | 0 | 7.1 | 1512 | nan |
| 2011 | 23.8 | 155 | -2.0 | 1357 | 25.8 |
| 2012 | 15 | 166 | 5.3 | 1334 | 9.7 |
| 2013 | 45.9 | 72 | 8.7 | 1440 | 37.2 |
| 2014 | 51.3 | 73 | 5.4 | 1439 | 45.9 |
| 2015 | -19.1 | 161 | 3.1 | 1351 | -22.3 |
| 2016 | -14.9 | 124 | 11.2 | 1388 | -26.1 |
| 2017 | 49.6 | 74 | 9.2 | 1432 | 40.4 |
| 2018 | 23 | 152 | -4.5 | 1354 | 27.5 |
| 2019 | 4 | 95 | 16.6 | 1417 | -12.7 |
| 2020 | 44.8 | 92 | 13.3 | 1426 | 31.4 |
| 2021 | 47.1 | 128 | 9.7 | 1384 | 37.4 |
| 2022 | 38.1 | 229 | -20.6 | 1277 | 58.7 |
| 2023 | 40.6 | 127 | 13.7 | 1373 | 27 |
| 2024 | 42.9 | 119 | 7.3 | 1393 | 35.6 |
| 2025 | 41.6 | 117 | 9.3 | 1383 | 32.3 |
| 2026 | 24.6 | 112 | 2.9 | 1226 | 21.7 |

Farkin pozitif oldugu yil: **13 / 16** (sinyal olan yillar). Sinyal gunu ortalamasinin kendisi pozitif olan yil: 14 / 16.

### F11a (^SOX <= -%3 -> SMH)

Arac arac (2010-2026, sinyal gunu sonrasi 1 gunluk ortalama getiri vs diger butun gunler):

| araç | sinyal_ort_bps | sinyal_n | diger_ort_bps | diger_n | fark_bps |
|---|---|---|---|---|---|
| SMH | 54.9 | 226 | 7.5 | 4021 | 47.4 |
| toplam | 54.9 | 226 | 7.5 | 4021 | 47.4 |

Yil yil (araclar havuzlanmis):

| yil | sinyal_ort_bps | sinyal_n | diger_ort_bps | diger_n | fark_bps |
|---|---|---|---|---|---|
| 2010 | nan | 0 | 6.9 | 252 | nan |
| 2011 | -40.8 | 15 | 1.7 | 237 | -42.6 |
| 2012 | 36.8 | 4 | 4.6 | 246 | 32.1 |
| 2013 | 20 | 3 | 9.9 | 249 | 10.1 |
| 2014 | -104.4 | 3 | 12.8 | 249 | -117.2 |
| 2015 | -26.1 | 3 | 0.8 | 249 | -26.9 |
| 2016 | 34 | 9 | 12.8 | 243 | 21.2 |
| 2017 | 50 | 3 | 14 | 248 | 35.9 |
| 2018 | 88.5 | 15 | -8.8 | 236 | 97.3 |
| 2019 | 147 | 8 | 17.6 | 244 | 129.4 |
| 2020 | 194.2 | 24 | 2.3 | 229 | 191.8 |
| 2021 | 40.1 | 12 | 15.4 | 240 | 24.7 |
| 2022 | 11.3 | 39 | -18.5 | 212 | 29.8 |
| 2023 | 1.3 | 7 | 23.1 | 243 | -21.8 |
| 2024 | 51.2 | 24 | 13.7 | 228 | 37.5 |
| 2025 | 108.5 | 20 | 12.2 | 230 | 96.3 |
| 2026 | 33.6 | 37 | 2.1 | 186 | 31.6 |

Farkin pozitif oldugu yil: **12 / 16** (sinyal olan yillar). Sinyal gunu ortalamasinin kendisi pozitif olan yil: 13 / 16.

## 5. Günlük sinyal aracı (`kod/sinyal.py`)

- Bağımsız: yalnız pandas, numpy, yfinance; `ortak.py`'ye ve `yeniden_kodlama.py`'ye bağımlı değil. Bilanço maskesi için varsa yerel `veri/bilanco/<kod>.csv`, yoksa yfinance bilanço takvimi.
- Kullanım: `python kod/sinyal.py` (son işlem günü), `--tarih 2026-11-20`, `--saat 1530` (15:30 fiyatıyla; 60m bar, ^VIX için 30m bar, çünkü Yahoo'da ^VIX saatlik barları tam saatte başlıyor), `--yerel veri/gunluk` (Yahoo yerine yerel CSV), `--cikti dosya`.
- Sağlama: yerel veride geçmişe vektörel uygulandığında sinyal günleri backtest işlemleriyle F3_T (1996), F4b_T (628), F11a (226) için **birebir**; F1a_T'de 4350'ye karşı 4346. Fark 4 gün (QQQ 2012-02-22, 2012-11-27; XLK 2011-12-14; IWM 2018-06-13): IBS tam 0,2000; düzeltilmiş sütunlarda kayan nokta yuvarlaması 0,2'nin bir tık altına düşürüyor, ham × çarpan hesabı düşürmüyor. Protokol "< 0,2" dediği için araç doğru tarafta; backtest etkisi ihmal edilebilir (4/4350).
- 20 Kasım 2026: Yahoo çıktısı ile yerel veri çıktısı satır satır aynı. Rejim: VIX 35,89, VIX/VIX3M 1,160 (ters eğri), ^SOX −%10,73, SMH 250 günlük zirveden −%40,2; STRES ve BUGÜN bayrakları EVET. SMH −%10,60 (yukarıdaki SMH ≤ −%8 listesinin 9. günü). F1a: 6 T ETF'inin hepsinde AL; F3: SMH, SPY; F11a: EVET; kaçınma F4b/F11b yok. DRAM sinyal sayılmaz (162 gün geçmiş < 250). 15:30 modu aynı günü verdi (VIX 36,00, ^SOX −%10,25; aynı sinyaller).

## 6. Bulunan hatalar ve uyarılar

1. Hedef sonuçlarda hata bulunmadı: 7 test (+F1a_C) n ve alfada birebir, dönem ve son 12 ay alfaları da birebir.
2. Tek tutarsızlık sütun tanımı: F1d `n_son12` 316 (hedef) / 2284 (ben); alfa aynı.
3. Kırılganlık: F9b, 3 $ eşiğinin düzeltilmiş fiyata uygulanmasıyla t 2,97 → 2,64. Bölünmemiş fiyat protokolün doğru okuması, ama bulgu bu seçime duyarlı.
4. Saatlik "son 30 dk" tanısı yalnız Yahoo bar kapanışıyla tutuyor; resmî kapanışla fark 88 → 27 bps. Kural olarak kullanılmamalı.
5. Betimsel "ortalama" sayıları (STRES +98, SOXL +100, TQQQ +38) ham ortalama değil alfa; ham ortalamalar daha yüksek (+105, +128, +58).
6. Kayan nokta sınır durumu (IBS = 0,2) backtestte 4 işlemi içeri alıyor; ihmal edilebilir.
