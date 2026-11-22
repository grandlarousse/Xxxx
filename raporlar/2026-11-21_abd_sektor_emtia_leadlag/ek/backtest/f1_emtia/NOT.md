# F1 emtia → hisse/ETF: not (22.11.2026)

Betik: `kod/f1_emtia.py` (~35 sn; `--yeniden` önbelleği siler).

## Test sayısı ve beklenen yanlış pozitif
- Hazır çiftler (cift_motoru, aile F1): 2.427 hipotez testi (+810 B1r arındırma testi).
- Özel öncüler (bu betik): 403 hipotez testi (+87 B1r). Ayrıca 248 kontrol testi yapıldı (1 gün gecikmeli öncü, ETF öncü kıyası, ters yön). Bunlar sayılmadı.
- F1 toplamı: 2.830 test (ZL/ZS → BG/ADM'deki 36 test iki tarafta da var). Rastgelelikten beklenen yanlış pozitif: **SAĞLAM 0,11, KOŞULLU 0,40**.

## Sonuç
- **SAĞLAM: 0 · KOŞULLU: 1 · İZLE: 8** (5'i hazır, 4'ü özel; ZS=F→BG iki tarafta da var).
- Tek KOŞULLU sinyal: 3-2-1 crack (rafineri marjı) dolar değişimi z ≥ 1 → VLO, B1r, h=2. 28 bps/işlem, IS t 2,51, OOS t 2,11, BH geçti. B koşulu (OOS t ≥ 2,5) sağlanmadı. Bulunan tek KOŞULLU, şansla beklenen 0,40 ile aynı büyüklükte.
- Eleme (özel): IS t ≥ 2,5 olan 4 testten yalnız 1'i OOS t ≥ 2,0; 2,5'i geçen yok. 485 test ELENDİ.

## Çürütme testleri (ELENDİ dışı 9 satır, `curutme.csv`)
- **Gecikmeli öncü:** öncü 1 gün geciktirilince bütün vadeli/crack sinyalleri kayboluyor (VLO OOS t 2,11 → 0,63). Bu, 1 günlük öncülük için beklenen sonuç; ileri bakış izi yok.
- **Rejim:** crack → VLO yalnız VIX ≤ 20 iken çalışıyor (t 3,96). VIX > 20'de etki yok (t 0,80). Bugün VIX ~36 olduğu için şu an uygulanabilirliği zayıf.
- **Kriz dönemleri hariç** tutulunca crack → VLO'nun OOS t'si 1,81'e, **maliyet iki katına** çıkınca da 1,81'e düşüyor. **Sınır sinyalleri hariç** tutulunca güçleniyor (2,52). En büyük 20 işlem çıkarılınca t 3,06.
- ZS=F → CTVA (h=1): eşik 1,5'e çıkınca kayboluyor (OOS t 0,28). Güçlü sinyal daha iyi çalışmıyor, yani kırılgan. ETF öncü SOYB ile OOS t 2,34.
- UNG → NRG (B3): sınır sinyalleri hariç tutulunca dağılıyor (OOS t 1,16). Kırılgan.
- TIO=F → CLF: 78–88 bps/işlem (CLF çok oynak). Bozuk veri yok; öncüye özgü değil.

## Yeni rejim adayları (IS t < 2, OOS t ≥ 2,5; sınıf almaz; `yeni_rejim.csv`)
**Soya yağı (ZL=F) → BG / ADM, B1r h=1: OOS t 3,63 / 3,44, IS t ≈ −0,5.** Yıl yıl dağılım çok net bir kırılma gösteriyor:
- BG: 2012–2019 yıllarının hepsi negatif, 2020–2026 yıllarının hepsi pozitif (+19 ile +46 bps).
- ADM: 2019–2026 yıllarının hepsi pozitif.
- ZS=F'de de aynı desen var.

Bu, yenilenebilir dizel ve RFS (ABD Yenilenebilir Yakıt Standardı) büyümesiyle uyumlu bir **rejim değişikliği** deseni. VIX > 20'de de çalışıyor (t 2,4–3,2). Ama 2.830 testte OOS t ≥ 3,4 çıkan yaklaşık 1 sonuç şansla da beklenir. Ayrıca öncü 1 gün gecikince kayboluyor. Hüküm: **ilginç aday, kanıtlanmış değil.**

Diğer adaylar (crack → PBF, HO=F → CVI, UNL → AR, MTF=F → ARLP) yılların ancak yarısında pozitif; çoğu 2019–22 enerji oynaklığından.

## Hipotezle çelişen / şaşırtıcı bulgular
- 1. dalga ön testi crack için 2016 sonrası t ≈ 3,1–3,3 bulmuştu. Burada maliyet ve sürüklenme düzeltmesiyle sepet OOS t'si 1,4 (B1) ile 1,8 (B1r) arasında kaldı. Yalnız VLO ve PBF'de güçlü. ETF vekili (UGA−USO) aynı etkiyi doğrulamıyor.
- **52 hafta zirvesi AL kuralı tersine çalışıyor:** sepet OOS t −1,9, DBA −4,0, CPER −3,2 (açılış girişiyle), DBB −2,4. Zirveye yakın emtia ETF'leri sonraki gün geriliyor. Bu yönde önceden yazılı bir hipotez yok; ters yön sınıf almaz.
- Altın/gümüş oranı ortalamaya dönüşü: hiçbir hedefte yok (OOS t ≤ 0). Vade eğrisi vekilleri, TIP, UUP, GDX → metal madencileri ve USO'nun 5/10 günlük birikimli şoku: hepsi ELENDİ (en iyi OOS t: JETS 2,35, ama IS t −1,2).
- Rapor günü: UNG perşembe SAT 15 bps (t 0,9 / 1,2); USO günleri boş.

## Veri sorunları
- PARR 2012-09-13: −19.583 bps'lik işlem (Delta Petroleum'un iflastan çıkış sıçraması). Sepet bundan etkilenmiyor (en büyük 20 hariç t 2,88).
- USL ve UNL kapanışı bayat. Eğri vekilleri bu yüzden kirli olabilir ama zaten ELENDİ.
- CL=F'in 20.04.2020'deki negatif fiyatı crack'i bozuyor. Kriz hariç testi bunu da dışarıda bırakıyor.
- Vade geçişi sıçramaları temizlenmedi. Havuzda E, F ve H yaklaşık hesaplandı.
