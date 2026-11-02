# r1_kimya — Kimya / Gübre / Tarım İlacı / Çimento / Cam: GUBRF, HEKTS, TKFEN, SISE, CIMSA, OYAKC

Ajan: kimya · Veri: 30.10.2026 kapanışına kadar.
- Koordinatör düzeltmeleri uygulandı: FX_FIX=True ve simetrik ±%10,5 temizlik. Paneller 14:39 UTC'de yeniden üretildi, tüm betikler bundan sonra yeniden çalıştırıldı.
- Çıktılar: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/f_kimya.csv` (267 satır).
- Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_kimya/`
  - kc.py: yardımcı fonksiyonlar
  - a1: hipotez çiftleri
  - a2: haftalık/aylık + USD bazlı
  - a3: tarama + FDR
  - a4: backtest
  - a5: olay/rejim
  - a6: saatlik hizalama
  - a7: gap-fade/momentum
  - a8/a8b: tamamlayıcı analizler
  - a9: CSV üretici

## 1. Net bulgular

| # | Hisse | Sürücü (TV) | İlişki | Rakamlar | Güven |
|---|---|---|---|---|---|
| 1 | CIMSA ↔ OYAKC ↔ TR çimento kümesi (BIST:AKCNS, NUHCM, AFYON, BUCIM, KONYA) | yurt içi küme | sync | CIMSA–AKCNS r=0,56, XU100 kontrollü pc=0,41 (t18). CIMSA–OYAKC r=0,51, pc=0,34 (IS 0,19 / OOS 0,40). Haftalık pc 0,24–0,37, aylık 0,44–0,52. İşaret yılların %95–100'ünde aynı. 250g kayan pc CIMSA–AKCNS hiç negatif olmadı (min 0,14); CIMSA–OYAKC'de pozitif oran %94, son değer 0,38 | YÜKSEK |
| 2 | GUBRF ↔ BIST gübre/tarım teması (BIST:BAGFS, EGGUB, HEKTS) | yurt içi küme | sync | GUBRF–BAGFS r=0,48, pc=0,33 (t15,8; IS 0,23 / OOS 0,20). GUBRF–HEKTS pc 0,22, GUBRF–EGGUB pc 0,22. **Uyarı:** GUBRF–BAGFS'te son 250g pc yalnız 0,04 (medyan 0,27) | YÜKSEK (zayıflıyor) |
| 3 | TKFEN ↔ BIST:ENKAI (taahhüt) | yurt içi | sync | r=0,40, pc=0,17 (IS 0,10 / OOS 0,15), aylık 0,34. Son 250g: 0,05 | YÜKSEK (sınırda) |
| 4 | 6 Şubat 2023 depremi → CIMSA / OYAKC | olay | event | CAR(0,5): CIMSA +%46,6 (z7,9), OYAKC +%54,4 (z8,3). CAR(0,60): CIMSA −%9,7, OYAKC +%40,6. OYAKC'nin XU100 betası 0,84'ten 1,09'a çıktı. Tekrarlanamaz | YÜKSEK (olay) |
| 5 | CIMSA / OYAKC kendi açılış gap'i (\|gap\|>%1) → gün-içi geri dönüş | mikro-yapı | lead_intra | Net 10 bps: CIMSA IS +28 bps (t2,5) / OOS +64 (t3,3), 13 yılın 11'i +. OYAKC IS +37 (t2,1) / OOS +40 (t2,2), 13 yılın 12'si +. Gecikmeli giriş (2023-12+): CIMSA 10:30 TSİ girişte +59 bps (t2,5), 11:30'da +41 (t2,4). XU100'de etki yok | ORTA (dış sürücü değil) |
| 6 | HEKTS: r_{t-1} işareti × anormal TL hacmi üst tercil → cc_t | bireysel yatırımcı ilgisi | lead_multiday | Brüt IS +29 bps (t2,7) / OOS +41 (t2,7), 13 yılın 13'ü +. Net 10 bps OOS +31 (t2,0). Getiri GAP'te; aynı sinyalle intra_t ≈ 0. GUBRF'de benzeri: brüt t2,9/1,95, net OOS t1,4. Diğer 4 hissede yok | ORTA (HEKTS), DÜŞÜK (GUBRF) |
| 7 | OYAK'ın Tekfen'in %42,8'ini devralması | olay | event | Görüşme KAP'ı (09.06.2026): CAR(0,10) −%15,3 (z−1,6). Devir tamamlanınca (24.07.2026): **CAR(0,10) +%40,9 (z4,2)**. "OYAK kümesi" ortak hareketi yok: TKFEN–HEKTS pc 0,21 → 0,01 (n=101) | ORTA (olay) |
| 8 | SISE ↔ BIST:XBANK / KCHOL | stil faktörü | sync | XBANK pc −0,165 (t−8,8, yılların %94'ü). **Son 250g'de işaret döndü (+0,15).** KCHOL ile pc +0,18 | ORTA |
| 9 | TTF (TR makro faktörü) | 15:00 UTC hizalı | sync | 2024-06 sonrası ham r: SISE −0,15, GUBRF −0,17, CIMSA −0,16; XU100'ün kendisi −0,17 (FDR geçti). Kısmi pc: SISE −0,01, GUBRF −0,08, CIMSA −0,05 → sektöre değil ülkeye etki | ORTA (piyasa), DÜŞÜK (hisseye özgü) |
| 10 | Avrupa endeks/emsalleri → CIMSA gap | lead_gap | işlenemez | gap_l1_pc: ^STOXX r=0,08 (t4,9); 103 Avrupa sürücüsü FDR'den geçti. Gün-içi TERS: AB çimento sepeti → CIMSA intra brüt OOS −10 bps (t−2,7) | DÜŞÜK |
| 11 | CIMSA/OYAKC ↔ XETR:HEI, EURONEXT:SGO (15:00 UTC hizalı) | AB emsal | intraday_minutes | Gerçek senkron r≈0,20–0,22 (t5,5), pc≈0,09. Tam dönem günlük pc 0,01–0,05 | DÜŞÜK |
| 12 | Saatlik küme-içi öncülük: EGGUB/GUBRF → BAGFS, NUHCM/AKCNS → CIMSA | intraday_minutes | 40 testin 7'si FDR'den geçti (t 2,6–4,2). Ancak brüt 5–9 bps/işlem, 8–15 bps maliyetin altında | DÜŞÜK (işlenemez) |
| 13 | SISE ↔ USDTRY / EURTRY (FX düzeltmeli) | ihracatçı | sync (aylık) | Aylık pc +0,22 / +0,23. Günlük OOS pc 0,10 | DÜŞÜK–ORTA |

## 2. Yöntem
- **Hipotez testleri:**
  - 207 çift (FDR'den 33'ü geçti).
  - Metrikler: XU100 kontrollü kısmi korelasyon (pc); genişletilmiş pc (XU100 + USDTRY + ACWI lag0/lag1); haftalık ve aylık pc; USD bazlı getiri; lag1 → gap/intra (2014+); t+2..t+5 sürüklenme; ters yön; 250 günlük kayan korelasyon; yıllık işaret tutarlılığı.
- **Veri güdümlü tarama:** 6 hisse × 1.087 sürücü × 6 test = 39.132 test, BH q=0,05. Testler: sync_pc, gap_l1 (ham ve XU100 gap kontrollü), intra_l1 (ham ve kontrollü), rev_l1. FDR'den geçenlere NW-t, IS/OOS ve yıllık işaret kontrolü uygulandı; 1.571'i "sağlam" çıktı. Bunların çoğu gap_l1, yani işlenemez eşzamansız kapanış etkisi.
- **Backtestler:**
  - Dış sürücü: 30 spesifikasyon. BT1: ABD gübre → GUBRF/HEKTS/TKFEN; BT2: TTF/NG → SISE ve diğerleri; BT3: AB/ABD çimento → CIMSA/OYAKC; BT4/BT5: yurt içi küme.
  - Kendi sinyali: 34 spesifikasyon (gap-fade, momentum).
  - Hacim koşullu momentum: 6 hisse.
  - Hepsinde IS 2014–2020 / OOS 2021–2026, maliyet 0/8/10/15 bps ve yıllık kırılım (res_bt_years.csv, res_extra_bt_years_summary.csv).
- **Saatlik:**
  - 15:00 UTC'ye hizalı gerçek senkron ve sürücünün kapanış sonrası parçası (63 test, FDR).
  - ABD ilk saati → BIST son yarım saat.
  - Küme-içi saatlik öncülük (40 test, FDR).
  - Gap-fade için gecikmeli giriş.
- **Şirket gerçekleri (WebSearch):**
  - GUBRF: Tarım Kredi ~%76; Razi'de %48,88. Bir kaynağa göre İran gelirin ~%50'si, faaliyet kârının ~%85'i. Razi ihalesi 28.02.2025'te başladı, 28.11.2025'te sonlandırıldı.
  - HEKTS: **OYAK iştiraki; Gübretaş ile ortaklık bağı yok.**
  - TKFEN: 2025 gelirinin %62'si taahhüt, %36'sı tarım. **OYAK (ON Investment B.V.) Can Holding'in %42,8 payını aldı; KAP görüşme 09.06.2026, devir 24.07.2026.** Böylece TKFEN, HEKTS ve OYAKC'nin üçü de OYAK'ta.
  - SISE: İş Bankası grubu; Wyoming'de %51 (diğer %49 NRP), Pacific Soda'da %100.
  - CIMSA: döviz bazlı satış ≥%60–70; beyaz çimento satışlarının ~%90'ı ihracat; Mannok.
  - OYAKC: 2020'de 5 şirket birleşti, 2023'te Denizli eklendi; 2024'te TCC'ye %20 pay devredildi.

## 3. Önemli olumsuz bulgular
- **Gübre emsalleri:** CF, NTR, MOS, YAR, ICL, IPI, LXU, OCI, SQM, UAN, 2020.SR ve ABUK hiçbir hissede XU100 kontrollü anlamlı değil.
  - GUBRF–CF: pc −0,03, haftalık 0,01; 250g kayan pc'nin medyanı −0,02.
  - BT1: OOS net −2 bps; pozitif yıl sayısı IS 2/7, OOS 3/6.
- **Tarım ilacı:** HEKTS–CTVA/FMC/BAYN/UPL/NUF pc 0,00–0,02. Haftalık FMC 0,08 → DÜŞÜK.
- **Taahhüt:** TKFEN–FLR/KBR/J/ACS pc ≈ 0. BT1 → TKFEN OOS −17 bps (t−2,3).
- **Cam ve soda külü:** SISE–SGO/OI/VID/VRLA/AGC/GLW/SOLB/GEL/NRP pc ≈ 0. TATACHEM pc 0,06 → DÜŞÜK.
- **TTF şoku → SISE (BT2):** OOS −2 bps. Enerji maliyeti hipotezi hisseye özgü olarak desteklenmedi.
- **Çimento maliyet/talep vekilleri:** MTF=F (kömür, 2025-12'den beri bayat), XLB/XHB/ITB ve ABD çimentocuları için pc ≈ 0.
- **İran/İsrail ve Razi olayları:** GUBRF'de 9 olayın hiçbirinde |z|>2 yok.
- **Tahıllar:** pc ≈ 0.
- **ABD ilk saati → BIST 14:30–kapanış:** r≈0.
- **Yurt içi küme öncülüğü günlük bazda yok** (BT4/BT5 negatif).
- **Genel tablo:**
  - Küresel sürücülerin ham korelasyonu (0,05–0,26) XU100 kanalından geliyor.
  - ABD kaynaklı etki ertesi gün gap'te fiyatlanıyor: ES=F'nin kapanış sonrası parçası → XU100 gap r=0,24, intra 0,01.
  - Büyük gap'ler gün içinde kısmen geri dönüyor.

## 4. Karşı argümanlar ve sınırlamalar
- **Gap-fade:** Sürücü değil, mikro-yapı etkisi. VİOP pay vadelisinin açılış likiditesi spot piyasadan zayıf olabilir. Yine de gecikmeli girişte sonuç korunuyor.
- **Hacim koşullu momentum:** Getirinin büyük kısmı gap'te. Kapanışta giriş gerekir; spot 18:10'da kapanırken VİOP 18:15'e kadar açık, yani uygulanabilir ama baz riski var.
- **Tarama:** FDR bağımsızlık varsayar; Asya ve Avrupa kümeleri aynı faktörü defalarca saydırıyor. GUBRF–TAN/ICLN pc 0,08 ve Asya_t-1 → SISE intra (t4,5) mekanizması zayıf → DÜŞÜK.
- **Saatlik örneklem kısa** (2023-11+). NG=F kapanış sonrası → SISE intra (t3,5) FDR'den geçti ama işareti beklenenin tersi → DÜŞÜK.
- **Hiç test edilemeyenler (veri yok):**
  - Üre/DAP vadeli fiyatı (TV: CBOT:UFV1!, CBOT:UME1!).
  - Çin ZCE soda külü (kullanıcıda açılmıyor; alternatif NSE:TATACHEM).
  - Tahran borsası.
  - Petkok.
  - MKK bireysel yatırımcı payı (yerine hacim vekili kullanıldı).
- **OYAK–Tekfen sonrası örneklem 101 gün;** TKFEN–HEKTS–OYAKC kümesi oluşup oluşmadığı izlenmeli.

## 5. Kaynaklar
[intellinews Gübretaş/Razi](https://www.intellinews.com/speculator-offloads-istanbul-listed-gubretas-shares-as-price-nosedives-over-iran-court-dispute-306770) · [CNBC-e Razi ihalesi](https://www.cnbce.com/borsa/gubre-fabrikalarinin-razi-petrochemical-ihalesinde-acik-artirmaya-gecilmesine-karar-verildi-h13455) · [Midas Razi](https://www.getmidas.com/midasin-kulaklari/gubrf-razi-petrochemicaldaki-paylarinin-satisindan-vazgecti-p-218882) · [Hektaş/OYAK](https://www.gcmyatirim.com.tr/borsa/hisse/hekts-hisse-hektas-ticaret-t-a-s) · [CNBC-e OYAK–Tekfen %42,8](https://www.cnbce.com/borsa/tekfen-holdingde-ortaklik-degisimi-oyak-bagli-sirket-paylarin-yuzde-428ini-devraldi-h33805) · [CNBC-e görüşmeler](https://www.cnbce.com/borsa/tekfendeki-can-holding-hisselerinin-oyaka-devri-icin-gorusmelere-baslandi-h31332) · [Midas ON Investment](https://www.getmidas.com/midasin-kulaklari/can-kultur-tekfen-holdingdeki-yuzde-428-hissesini-oyak-istiraki-on-investmenta-devretti-p-629428) · [Glass International Şişecam–Ciner](https://www.glass-international.com/news/sisecam-completes-ciner-group-us-soda-ash-acquisition) · [Wyoming News](https://www.wyomingnews.com/rocketminer/sisecam-acquires-ciner-groups-shares-in-u-s-soda-ash-operations/article_1a60b1ce-c85a-11ef-b64b-8badc0971775.html) · [Fintables Çimsa](https://fintables.com/arastirma/yazilar/ne-is-yapiyor/cimsa-ne-is-yapiyor) · [CNBC-e Mannok](https://www.cnbce.com/haberler/cimsa-sabanci-holdingin-en-buyuk-yurt-disi-satin-alimini-gerceklestirdi-h10562) · [OYAK çimento](https://www.oyak.com.tr/en/oyak-companies/fields-of-activity/cimento-beton-kagit) · [S&C TCC](https://sullcrom.com/About/News-and-Events/Highlights/2023/December/S-C-Advises-Taiwan-Cement-Corporation-in-Raising-Stakes-in-Turkey-and-Portugal-Enhancing-Its-International-Eco-Friendly-Positio) · [Quartr Tekfen](https://quartr.com/events/tekfen-holding-anonim-sirketi-tkfen-q4-2025_FtpJSBRD) · [TradingView CBOT:UFV1!](https://in.tradingview.com/symbols/CBOT-UFV1%21/forward-curve) · [TradingView CBOT:UME1!](https://in.tradingview.com/symbols/CBOT-UME1%21/contracts)
