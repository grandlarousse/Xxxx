# v_S2_b — İddia S2'yi çürütme denemesi (2. aşama)

**İddia:** TKC (NYSE ADR) parite sapması D, TCELL'in ertesi gün gün-içi getirisini öngörüyor.

- Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_b/` (01–10, yardımcı modül `vb.py`). ll.py import edilmedi.
- Loglar: `code_v_S2_b/res/*.log`.
- Hizalama ve temizlik ham parquet'ten yeniden yazıldı. Hedef iki şekilde kullanıldı:
  - (a) iddiadaki gibi: yalnız cc/gap ±%10,5 temizliği;
  - (b) ek olarak |gün-içi| > %10,5 olan günler de atılmış hali.

## KARAR: DÜZELT

- İlişki gerçek görünüyor: güven ORTA.
- İddia edilen işlem stratejisi (Sharpe 1,07) uygulanabilir halde büyük ölçüde buharlaşıyor: güven DÜŞÜK.
- Saatlik alt iddia: güven DÜŞÜK.

## 1. Çürütme denemeleri — ilişkiyi YIKAMAYANLAR (dürüst kayıt)

| Test | Sonuç |
|---|---|
| Replikasyon (hedef a), intra1 ~ D + gap1 | ALL b 0,129 (t 2,76), IS 0,075 (t 1,91), OOS 0,148 (t 2,39). Birebir. |
| **Açılış gürültüsü / bid-ask sıçraması** | Regresyona gap kontrolü eklemek b_D'yi yalnız +0,004 değiştiriyor: a(gap~D) = 0,039, b_gap = −0,096. Mekanik değil. |
| Karıştırılmış-D plasebosu: U_p = D_perm − gap, \|U_p\|>50 (500 tekrar) | OOS −2,0 bps (sd 6,0), IS −4,6 bps; gerçek U ise +19,4 bps; p < 0,002. U'nun kârı gap-fade artefaktı değil. |
| Saf TCELL gap-fade | OOS −1,9…+4 bps. TCELL'de kendi gap'i tersine dönmüyor. |
| Diğer 46 VİOP hissesi plasebosu (D → hisse gün-içi_{t+1}) | TCELL ham t'de 47 hisse içinde 1. sırada, XU100'den arındırılmış t'de de 1. sırada (t 2,99 / 4,16). Diğerlerinde \|t\|>2 olan yalnız 1/46 (SISE 2,3). Etki hisseye özgü. |
| Huber robust regresyon | ALL b 0,109 (t 5,3); IS t 2,7; OOS t 4,1. |
| En etkili 5–40 gün atılınca | t yükseliyor (3,0 → 3,9). Uç değerler b'yi şişiriyor ama t'yi taşımıyor. |
| Kayan 500 günlük b | Pencerelerin %100'ünde pozitif (medyan 0,127, min 0,003). |
| **Gerçek işlem aracı:** VİOP F_TCELL (bülten, en likit kontrat, açılış → kapanış, 1.707 gün) | b 0,092 (t 2,20). Spot ile aynı. |
| FX zaman damgası, 2024+ (saatlik veri) | Yahoo bar L'nin `c` değeri ≈ L günü 00–07 UTC fiyatı: corr 0,87; 08 UTC'de 0,13'e düşüyor. corr(r_bar(L), L seansı kur hareketi) = 0,001. İleriye bakma yok. |
| FX zaman damgası, 2011–2020 | Bar (t+1) − bar t, XU100 gap_{t+1} ile −0,3…−0,46 korelasyonlu, gün-içi_{t+1} ile ≈ 0. Bar t+2 − bar t+1 gün-içi_{t+1} ile −0,15…−0,43 korelasyonlu. Konvansiyon tutarlı. |
| FX zaman damgası, 2021–23 (doğrulanamayan dönem) | D_fx0 (kur t sabahı, ileriye bakması imkânsız): OOS b 0,104 (t 2,72). OOS regresyonu kur zamanlamasına bağlı değil. |
| Sahte açılış (o==c) günleri | 2014–15'te günlerin %17–18'i. Atılınca sonuç değişmiyor (IS t 1,94, OOS t 2,27). |
| ADR oranı | 2 ADS = 5 hisse, 2005'ten beri. Kaynak: SEC 20-F. |
| KKM tarihi | 20.12.2021 akşamı, kabine toplantısı sonrası açıklandı (BIST kapanışından sonra). Yahoo FX barı (21.12): 13,475; kaynaktaki "gece kapanışı 13,44" ile tutarlı. |

## 2. Çürütme denemeleri — iddiayı DÜZELTENLER

1. **b 0,13, KKM uçlarıyla şişmiş.** Yalnız 5 gün (20/16/17.12.2021, 19/22.03.2021) atılınca:
   - ALL b 0,086 (t 2,96), OOS b 0,093.
   - \|gün-içi\| > %10,5 günleri atılınca ALL b 0,089 (t 3,06).
   - Gerçekçi büyüklük b ≈ 0,09–0,11: sapmanın ~%10'u ertesi gün gün-içinde kapanıyor. sd(D) ~150 bps için bu, sd başına ~13 bps; maliyetle aynı düzeyde.
2. **IS zayıf.** IS b 0,067–0,077, t 1,8–2,0. Kur t sabahından alınırsa IS t 1,3.
3. **Mekanizma "gece ADR fiyat keşfi" değil.**
   - OOS'ta D gap'i HİÇ öngörmüyor: gap1 ~ D OOS b 0,003 (t 0,1); IS'te 0,111 (t 3,9).
   - Bileşen ayrıştırmasında tahmin gücü TKC'nin gece hareketinden (t 1,5) ya da kurdan (t 0,7) çok, gecikmeli parite sapmasından geliyor (Lag t 2,5).
   - 2023-12+ dönemde etkinin ~1/4'ü TCELL kapanış seansı sapmasının ertesi gün geri dönmesi. D sürekli seans son fiyatıyla hesaplanınca b 0,132 → 0,096 (t 1,7).
4. **Backtest seçim yanlılığı.** Aynı sinyalin en az 8 varyantı var. **IS'te hiçbiri maliyet sonrası kâr etmiyor.**

   | Varyant | IS (bps / işlem) | OOS (bps / işlem) |
   |---|---|---|
   | D \|>0\| | −7,0 | +8,8 |
   | D \|>50\| | −2,0 | +9,3 |
   | D \|>100\| | +9,8 | +19,9 |
   | U \|>0\| | −4,0 | +7,2 |
   | U \|>25\| | −4,9 | +12,2 |
   | U \|>50\| | +0,9 | **+19,4** (seçilen) |
   | U \|>100\| | +2,9 | +21,0 |

   - Varyant tüm örneklem görüldükten sonra seçildi; bu yüzden "OOS" gerçek bir örneklem dışı test değil.
   - U \|>50\| OOS kârının %62'si 2021–22'den geliyor. 2023'te +0,8 bps.
5. **Uygulanabilir sinyal (yalnız D; açılıştan önce bilinir) çok zayıf.**
   - D \|>50\|: OOS +9,3 bps (Sh 0,52). OOS kârının %90'ı 2021–22'den ve **%100'ü en iyi 10 işlemden** geliyor; en iyi 10 hariç ortalama 0,0. 13 yılın yalnız 6'sı pozitif.
   - **Gerçek F_TCELL açılış → kapanış:**
     - \|D\|>0: +1,0 bps (Sh 0,07); \|D\|>50: +3,9 bps (Sh 0,22); en iyi 10 hariç −2,5 bps.
     - 2023-12+: +8,6 bps (Sh 0,68); \|D\|>50'de en iyi 10 hariç −3,8 bps.
6. **U açılış fiyatını bilmeyi gerektiriyor.** 2023-12+ saatlik veriyle:
   - U 07:30 UTC'de yeniden hesaplanırsa: +1,1 bps (\|>50\|).
   - D ile 07:30 girişi: +5,5…+6,9 bps (t ~1).
   - D 07:30 → kapanış getirisini hâlâ öngörüyor (b 0,118, t 2,3); ama kenar maliyet düzeyinde.
   - VİOP sürekli işlemi 09:30 TSİ'de (06:30 UTC) başlıyor, spot açılıştan 30 dk önce. Vadeli açılış seansı ince: medyan 3–4 işlem.
7. **Maliyet duyarlılığı.** U \|>50\| OOS: 12 bps'de Sh 0,86, 15 bps'de 0,69, 20 bps'de 0,41. IS ≥12 bps'de negatif. D \|>50\| 15 bps'de OOS Sh 0,13.
8. **XU030 hedge'li** (8+3 bps): D \|>50\| IS −7,8 / OOS +5,0 bps; U \|>50\| IS −3,4 / OOS +14,7 bps.
9. **Likidite (VİOP bülteni, F_TCELL en likit kontrat, medyan günlük hacim):**

   | Yıl | Medyan hacim |
   |---|---|
   | 2017 | 0,2 mn TL |
   | 2018 | 1,1 mn TL |
   | 2020 | 36 mn TL |
   | 2022 | 151 mn TL |
   | 2024 | 676 mn TL |
   | 2026 | 962 mn TL |

   IS döneminin (2014–2020) büyük kısmında vadeli işlemle uygulanamazdı. Bugün likit.

## 3. Saatlik alt iddia (tk_post = ln(TKC kapanış / TKC 15:30 UTC) → TCELL 07:30 → kapanış)

- Replike edildi: β 0,292 (t 2,68), n 693.
- Dönemler: 2023-12→2024 β 0,51 (t 3,3); 2025 β 0,02 (t 0,1); 2026 β 0,25 (t 1,35).
- ES kapanış-sonrası kontrolüyle (ortak örneklem, n 571) t 1,85. ES'ten arındırılmış tk_post için \|>50\| backtest +16 bps, \|>0\| +2,4 bps.
- D ile birlikte konunca tk_post t 0,96. Aynı bilgiyi taşıyor, bağımsız kanıt değil.
- Plasebolar: XU100 t 1,06, XU030 t 0,93, TTKOM t 1,28.
- Güven: DÜŞÜK.

## 4. Düzeltilmiş iddia

D_t = ln(TKC × USDTRY / (2,5 × TCELL)) − 20 günlük ortalama.

**İlişki (güven ORTA):** D, TCELL'in t+1 gün-içi getirisini hisseye özgü biçimde öngörüyor.
- Gerçekçi b ≈ 0,09–0,11: OLS t 2,6–3,1; Huber t 5,3; XU100'den arındırılmış hedefte t 4,2.
- IS t ~1,9, OOS t ~2,4.
- 47 VİOP hissesi içinde yalnız TCELL'de var.
- Gerçek F_TCELL getirilerinde de var (t 2,2).

**İşlem stratejisi (güven DÜŞÜK):**
- İddiadaki \|U\|>50 OOS +19 bps / Sh 1,07 rakamı şunlara dayanıyor:
  - açılış fiyatını bilip o fiyattan doldurulmak;
  - seçilmiş varyant;
  - kârın %62'sinin 2021–22'de olması;
  - IS ≈ 0.
- Açılıştan önce bilinen yalnız-D sinyalinin net kenarı:
  - spot: ~0–9 bps, 10 uç işleme bağımlı;
  - gerçek F_TCELL: ~1–4 bps.

**Saatlik tk_post (güven DÜŞÜK):** 2024'e yığılı.

## Kaynaklar
- KKM zamanlaması: https://medyascope.tv/2021/12/22/18-tlden-12ye-dusen-dolar-kurunun-saat-saat-seruveni/ , https://www.yeniakit.com.tr/haber/cumhurbaskani-erdogandan-dolar-ve-enflasyon-mesaji-1618271.html
- ADR oranı: https://www.sec.gov/Archives/edgar/data/0001071321/000119312509094063/d20f.htm , https://www.sec.gov/Archives/edgar/data/0001071321/000119312516510444/d135598d20f.htm
- VİOP açılış seansı ve saatleri: https://borsaistanbul.com/duyuru/14431/viopta-acilis-seansi-uygulamasi-ve-pay-vadeli-islem-ve-opsiyon-sozlesmelerinin-seans-sonu-saati-degisikligi-hk , https://www.borsaistanbul.com/files/viop-acilis-seansi-ve-pay-vis-ops-seans-sonu-deg-hk-duyuru.pdf
