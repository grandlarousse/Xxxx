# R1 — ENERJİ / RAFİNERİ / PETROKİMYA / ELEKTRİK (ajan: enerji)
Hisseler: TUPRS, PETKM, SASA, AKSEN, ENJSA, ODAS. Veri sonu 30.10.2026. Tüm sonuçlar FX_FIX=True ve simetrik ±%10,5 temizlikli panellerle (01.11.2026 14:39 UTC) YENİDEN üretildi.
Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_enerji/` (00→09 sırayla çalıştırılır; ara sonuçlar `res/`). Bulgular: `f_enerji.csv` (43 satır).

## 1. Net bulgular tablosu

| # | Hisse | Sürücü (Yahoo → TV) | İlişki | Kanıt (ana sayılar) | Güven |
|---|---|---|---|---|---|
| 1 | TUPRS | CRAK → AMEX:CRAK (rafineri ETF) | sync | corr 0,30, XU100-kısmi 0,17; haftalık 0,45 / kısmi 0,32; yılların %100'ünde +; IS/OOS kısmi 0,15/0,22; 250g kayan corr hep >0 | YÜKSEK |
| 2 | TUPRS | BZ=F → ICEEUR:BRN1! | sync | corr 0,17, kısmi 0,16 (t=9); haftalık kısmi 0,27; aylık USD kısmi 0,35 (OOS 0,51); yıl işareti %88; son 1y corr 0,34; 2026 haftalık kısmi 0,64 | YÜKSEK |
| 3 | TUPRS | AB rafineri sepeti (GPW:PKN, BME:REP, BET:MOL, ATHEX:MOH/ELPE, OMXHEX:NESTE, EURONEXT:GALP, VIE:OMV) | sync (aylık) | aylık USD kısmi 0,43 (IS 0,32 / OOS 0,58); günlük tekil kısmi 0,12–0,13 | YÜKSEK (aylık) / ORTA (günlük) |
| 4 | TUPRS | ABD rafineri sepeti t-1 (NYSE:VLO, MPC, PSX, PBF) | **lead_intra (işlenebilir)** | hedge'li gün-içi t=4,5 (ES lag1 ve Brent lag1 kontrollü); tarama: VLO FDR padj<0,001, IS t=3,8 / OOS t=4,5; hareketin ~%62'si gün-içinde (gap'te sadece %38). BT: \|z\|>1 filtreli tek bacak brüt IS 17,7 bps (t=2,4), OOS 25,6 bps (t=2,3); net 8 bps Sharpe IS 0,44 / OOS 0,62; 15 bps 0,12 / 0,37 | ORTA |
| 5 | TUPRS | Brent gece hareketi (BIST kapanışı→açılış, saatlik) | lead_gap | gap corr 0,57 (hedge'li 0,66), t=5,5, n=559 (2024-06+); sonrası gün-içi −0,10 → **açılışta fiyatlanıyor, işlenemez** | ORTA (kısa örnek) |
| 6 | TUPRS | Çeyrek ort. dizel crack değişimi | regime | aynı çeyrek corr 0,38, kısmi 0,47 (n=68); sonraki çeyreğe öncülük yok (0,02) | ORTA |
| 7 | AKSEN | PTF (EPİAŞ, TV'de yok) aylık ort. | sync (aylık) | USD kısmi 0,26 (IS 0,28 / OOS 0,24); TL + USDTRY kontrollü 0,24; günlük ilişki yok; öncülük yok | ORTA |
| 8 | AKSEN/ODAS | BIST:ZOREN, BIST:AKSEN, BIST:ODAS | sync (BIST içi) | ODAS~ZOREN kısmi 0,24 (hft 0,33), ODAS~AKSEN 0,19, AKSEN~ZOREN 0,18; %100 yıl | YÜKSEK |
| 9 | SASA | Bireysel-favori sepeti (BIST:HEKTS, KONTR, ASTOR, SMRTG, EUPWR, GESAN, CWENE, YEOTK, ALFAS) | sync | kısmi 0,19 (IS 0,11 / OOS 0,17); HEKTS tek başına 0,26 | ORTA |
| 10 | TUPRS | BIST:AYGAZ (Koç, dolaylı ortak) | sync | kısmi 0,28, %100 yıl, OOS 0,39 | YÜKSEK (BIST içi) |
| 11 | PETKM | BIST:TUPRS | sync | kısmi 0,14 (hft 0,09), IS/OOS 0,15/0,17 | ORTA |
| 12 | TUPRS | Brent şok (\|z\|>2) günü gap'i ters işlem | event | brüt IS −4 bps / OOS +56 bps (n=85) | DÜŞÜK |
| 13 | ODAS | USDTRY → FX:USDTRY | sync | haftalık XU100-kontrollü beta −0,28 (t=−3,2); aylık anlamsız | DÜŞÜK |
| 14 | ENJSA | PTF haberi t-1 → gün-içi | lead_intra | t=2,4 ama BT5 net negatif; aylık işaret tutarsız | DÜŞÜK |

## 2. Önemli OLUMSUZ bulgular (elenmedi, düşük güvenle listede)
- **TUPRS'ta crack spread ≠ günlük/haftalık sürücü.** HO*42−BZ, RB*42−BZ ve 3-2-1 değişimleri günlük corr ≈0,00, haftalık kısmi 0,02–0,04, yıl işareti %41–53. Çoklu regresyonda (TUPRS_USD ~ XU100 + Brent + Δcrack) Brent t=6,4, crack t≈−0,2 (haftalık). Crack yalnızca **çeyreklik** frekansta (kısmi 0,47) ve **2025–26 rejiminde** (haftalık kısmi 0,38 / 0,54) görünür. 2022 dizel crack patlamasında bile haftalık crack kısmi korelasyonu −0,12, Brent 0,43. Bu sonuç, NY ULSD/RBOB'un Akdeniz ürünleri için zayıf vekil olmasından ve vadeli roll gürültüsünden de gelebilir.
- **Crack ve Brent t-1 → TUPRS gün-içi işlenemiyor** (BT2 OOS Sharpe −0,55; BT3 filtresiz IS −0,46).
- **PETKM küresel petrokimyaya bağlı değil:** LYB, DOW, BASF, WLK, LG Chem, Lotte, SABIC, PTTGC ve Formosa için XU100 kontrollü kısmi korelasyon −0,02 ile 0,03 arası; aylık USD petrokimya sepeti 0,08. Asya lag0 PETKM'nin açılış gap'ini açıklıyor (t 3,4–5,5), gün-içini açıklamıyor (BT4 negatif).
- **SASA küresel polyester/PTA zincirine bağlı değil:** IVL, Alpek, 1326.TW, Toray, Reliance, Brent ve pamukta kısmi korelasyon ≈0; aylık sepet −0,04. SASA'yı yurt içi bireysel yatırımcı faktörü yönetiyor.
- **Elektrik hisseleri Avrupa gaz, kömür, karbon ve utility hisselerine bağlı değil:** TTF, NG, MTF, KRBN, EOAN, RWE, ENEL, IBE, ENGI, EDP, PGE, CEZ, PPC, ICLN, TAN ve VWS'de kısmi korelasyon \|pc\|≤0,05. 2021–22 gaz krizinde bile AKSEN~TTF haftalık kısmi −0,01. Olası neden: Türkiye'de PTF~TTF aylık korelasyonu sadece 0,13 (çeyreklik 0,43), çünkü BOTAŞ'ın düzenlemeli gaz fiyatı bağlantıyı kesiyor.
- **ODAS ~ altın yok:** günlük kısmi −0,02; aylık işaret dönüyor (IS +0,17 / OOS −0,22); BT6 net negatif. Altın projesi üretimde değil.
- **TUPRS'ta "dolar hissesi" etkisi zayıf:** XU100 kontrollü USDTRY betası haftalık 0,10 (t=1,3).
- **Saatlik Brent(h-1) → TUPRS(h):** anlamlı (t=3,5) ama brüt 3,3–6,6 bps/işlem, yani 8–15 bps maliyetin altında.
- **AB rafineri t-1 → TUPRS hedge'li gün-içi:** t=3,9 ama brüt yalnızca 8 bps; 2 bacak maliyetle negatif.

## 3. Yöntem
- Getiriler log ve BIST takviminde (ll.py konvansiyonu). Senkron ölçüler: tam dönem, son 3 yıl, son 1 yıl; XU100 kontrollü kısmi korelasyon; NW-t'li beta. Ayrıca haftalık (W-FRI) ve aylık/çeyreklik versiyonlar; bunlar eşzamansız kapanışı giderir. USD bazlı versiyon: hisse − USDTRY (FX_FIX sonrası).
- Öncülük: sürücü_{t-1} → gap_t ve gün-içi_t (ll.decomp, 2014+). Asya'nın BIST açılışından önce kapanan piyasaları (KRX, TWSE, TSE) için lag0 da test edildi. Hedge'li hedef = hisse gün-içi − XU100 gün-içi.
- Ters yön (hisse_{t-1} → sürücü_t) testi yapıldı. FX ve Asya'daki "ters" sinyaller zamanlama artefaktı (FX_FIX sonrası büyük ölçüde kayboldu).
- Saatlik analiz (ll.snap_daily / h1, 2024-06+): pencereler BIST kapanışı 15:00 → ABD 21:00 → BIST açılışı 07:00 → 15:00 (UTC). Ayrıca seans içi saatlik lead.
- Veri güdümlü tarama: 6 hisse × 1.085 sembol (zero_frac≤0,25, n≥750) × 6 test ailesi (S, PC, G1, I1, H1, REV) = **39.060 test**. Her ailede BH-FDR q=0,05. H1'de FDR'den geçen 20 çift IS/OOS ayrı kontrol edildi (`res/scan_H1_fdr_isoos.csv`).
- PTF: EPİAŞ API'si kimlik doğrulama istiyor. Saatlik PTF (2013-01 → 2026-09-27) GitHub'daki kamuya açık EPİAŞ dışa aktarımlarından alındı (monteburns/ems, onatuzkan/vep-forward-tvtp-option-pricing). 2018 ortalaması EPİAŞ yıllık bültenindeki 231,64 TL/MWh ile **birebir** tuttu. Zamanlama: PTF(t+1) t günü ~11:00 UTC'de ilan edilir. Günlük sinyal = (t−5..t+1) 7 günlük log PTF ortalamasının değişimi; bu, hafta sonu mevsimselliğini yok eder.
- Backtestler (17 strateji + 4 varyant, `res/backtests.csv`, `res/06b_bt_extra.log`): look-ahead yok; IS 2014–2020 / OOS 2021–2026; maliyet 8/15 bps, hedge'li stratejide 2 bacak. Sepetler sektör tanımıyla önceden sabitlendi.
- Şirket gerçekleri (WebSearch):
  - Tüpraş: 30 Mt kapasite, orta distilat payı ~%48–55, dizel ~%33–39.
  - Petkim: SOCAR %51; nafta STAR'dan boru hattıyla geliyor; Petkim'in STAR'da dolaylı %18 payı var.
  - SASA: Adana PTA tesisi Aralık 2024'te devreye girdi (1,75 Mt/yıl).
  - Odaş: Çan Kömür %100; altın projesi Kütahya/Uşak'ta (~348 bin oz kaynak), henüz üretimde değil.
  - Enerjisa: regüle RAB, Haziran–Haziran TÜFE ile endeksli; WACC ~%13,5.
  - Aksa: yurt dışında (Afrika ve Orta Asya) USD PPA'lı gaz santralleri.

## 4. Karşı argümanlar ve öz-eleştiri
- **Bulgu #4 (ABD rafineri t-1 → gün-içi)** tarama sonrası en güçlü işlenebilir aday. Ama seçim yanlılığı riski var: aynı panelden çıktı. Yine de IS'de de anlamlı (VLO IS t=3,8) ve sepet önceden tanımlandı. Net getiri maliyete duyarlı: 15 bps'de IS Sharpe 0,12. 2017 ve 2021 negatif. Yahoo açılış fiyatının (açılış seansı) doğruluğu bu sonucun ön koşulu. Gece Brent'inin gap'te tam fiyatlanması (bulgu #5) açılış verisinin genel olarak sağlıklı olduğunu destekliyor.
- **TUPRS~Brent senkron ilişkisi** kısmen eşzamansız kapanıştan şişiyor (lag1 corr 0,07). Haftalık ölçü (0,27) daha temiz. Brent'in etkisi stok kazancı/kaybı, USD bazlı fiyatlama ve "enerji betası"nın karışımı; bunlar ayrıştırılamadı.
- **AKSEN~PTF (aylık)** n=153 ay; çeyreklikte zayıflıyor (0,16). Yurt dışı (USD PPA) gelir payı arttıkça bağın zayıflaması beklenir. Ortak payda (USDTRY) etkisi TL versiyonla kontrol edildi.
- Kısmi korelasyon, XU100 içindeki ağırlıktan da etkilenir: TUPRS ve SASA XU100'de büyük ağırlıklı, bu yüzden kısmi korelasyon biraz düşük tahmin edilmiş olabilir. ENJSA~XBANK kısmi −0,12 mekanik bir sonuç; bulgu olarak sayılmadı.

## 5. Sınırlamalar ve yapılmayanlar
- ICE Gasoil, Akdeniz/Platts crack, nafta, paraksilen, PTA ve MEG fiyatları Yahoo'da yok. Çin ZCE PTA kullanılamıyor. Vekiller (HO/RB/Brent) zayıf olabilir.
- Saatlik veri yalnızca ~2,4 yıl. VİOP akşam seansı verisi yok, bu yüzden gece hareketinin VİOP'ta işlenebilirliği **test edilmedi**.
- **Yapılmadı:** 2018 kur krizi, Mart 2025 ve Eylül–Ekim 2026 fon krizi için olay-penceresi analizi (yalnızca yıllık kırılım var). Tüpraş bilanço günleri olay çalışması. Enerjisa için WACC/tarife kararı ve TÜFE açıklama günleri. EPİAŞ YAL/YAT ve azami fiyat tavanı rejim analizi. PTF verisi 2026-09-27'de bitiyor.
- MTF=F 2025-12'den beri bayat. 2010.SR, PTTGC.BK ve IVL.BK'de sıfır getiri oranı yüksek (%14–32).
