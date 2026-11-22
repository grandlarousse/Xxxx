# F6 Bilanço olayları: not (22.11.2026)

**Sonuç: 1-3 günlük kapanış alımıyla işlenebilir bilanço etkisi bulunamadı. 74 testin 74'ü ELENDİ.**

## Test sayısı ve eleme
- Sınıflandırılan test: 74 (68 önceden yazılı + 6 keşif). Ayrıca 30 sağlamlık/kıyas satırı (sınıf almaz).
- Beklenen yanlış pozitif: SAĞLAM 0,003; KOŞULLU 0,010.
- A koşulunu (IS t ≥ 2,5) geçen: 0. Ön elemeyi (IS t ≥ 2,0 ve OOS t ≥ 1,5) geçen: 0. En yüksek IS t 2,04 (likit yarıda SAT, h=2; OOS 0,73). En yüksek OOS t 1,50 (bilanço öncesi prim; IS 0,15). 5 testte IS t ≤ −2 (hipotezin tersi).

## Bulgular (bps = işlem başına, maliyet sonrası, sürüklenme düzeltilmiş)
**(a) Bilanço sonrası sürüklenme.** |z| ≥ 2 tepki: 19.056 olay (10.165 AL, 8.891 SAT). AL h=1: −3,4 bps (IS −11,1, t −1,89; OOS +6,4, t 0,55). SAT h=1: +3,0 bps ama ham net −4,6 (açığa satan kaybediyor). Sürpriz işareti aynı yönde olanlar ve likidite yarıları aynı tabloyu veriyor. Kıyas: bilanço dışı günlerde aynı kural −15,5 / −17,6 bps (IS t −4,6): sıradan büyük hareket geri dönüyor, bilanço hareketi dönmüyor ama maliyeti aşan bir devam da yok. Betimsel: 2019 sonrası z > 4 tepkilerden sonra brüt +32 bps (h=1) var; gün bazlı t yetersiz (|z| ≥ 3 AL, OOS t 0,43).

**(b) Emsallere yayılım.** 215 bin emsal işlemi. Lider yönünde AL h=1: −4,2 bps; SAT: −8,4 bps (IS t −2,18; ham net −16,7). Lider en yüksek hacimli 3 hisseyle sınırlanınca: sıfır. Emsal t günü lider yönünde zaten hareket ettiyse (işlemlerin %16,7'si) kalan şey sürüklenme değil **geri dönüş**: SAT h=1 −16,8 bps (IS t −2,97), AL h=3 −16,4 (IS t −2,02). Bu dönüşü işleyen keşif testi maliyetten sonra +0,7 bps (IS t 0,60; OOS −0,40): kullanılamaz. 1-15 gün içinde açıklayacak emsaller: AL bacağı OOS'ta +11,8 / +20,9 / +27,4 bps (t 1,4-1,5) ama IS'te sıfır; SAT bacağı −13,5…−22,7. Thomas-Zhang sınaması: emsalin lidere erken tepkisi ile kendi bilanço tepkisi arasındaki eğim −0,030 (kümeli t −1,75): yön makaleyle aynı, zayıf.

**(c) Bilanço öncesi prim** (dolar hacmi ≥ 100 mn $; 21.604 işlem). İşlem ortalaması net +24,7 bps; standart sapma 694 bps; en kötü %5 eşiği −%10,0, en kötü %5'in ortalaması −%15,5; isabet %51,2. Gün bazlı portföyde +10,6 bps (IS t 0,15; OOS t 1,50). 2024-26'da medyan işlem −16,9 bps. Etiket gerektirmeyen 2 günlük sürüm: +15,0 bps (IS t 0,63; OOS 1,35). Tepki günü açılışından girince −10,5 bps: primin tamamı gece boşluğunda. Evren bugün hayatta olanlardan oluştuğu için bu sayı yukarı yanlı. Risk/getiri kötü: kullanılamaz.

**(d) Takvim.** `gelecek_bilanco.csv`: 20 Kasım - 18 Aralık arasında evrenden 61 şirket (27 kapanış sonrası, 16 açılış öncesi, 18 saati belirsiz). Büyükler: DELL, ADI, MDT (24 Kas), DE (25 Kas), MRVL, CRWD (1 Ara), CRM, SNOW (2 Ara), AVGO, ADBE (9 Ara), COST (10 Ara), ORCL (14 Ara), MU (16 Ara), NKE, ACN (17 Ara).

## Veri ve tepki günü çıkarımı
- Kural: {tarih, sonraki gün} içinde |z| × hacim oranı büyük olan. 'zaman' dolu 104 kayıtta (30 Oca - 19 Şub 2026) isabet %79,8; işlem açan |z| ≥ 2 olaylarda %93,3 (n = 60). EDGAR 8-K 2.02 (AAPL, NVDA, KO, JNJ; 135 olay, 2015+): %83,0; büyük tepkide %94,4; takvim tarihi EDGAR ile %100 aynı. XOM indirilemedi.
- |z| ≥ 3 olan olaylarda en büyük hareket %92-94 oranında tarih ya da ertesi günde: tarihler güvenilir.
- Geç etiketleme: ileri bakışsız kural (`a_nedensel`), yalnız tarih günü ve yalnız ertesi gün alt kümeleri aynı sonucu veriyor (hiçbirinde IS ve OOS aynı işaretli anlamlı etki yok).
- Pozitif kontrol: tepkiden bir gün önce tepki yönünde (ileri bakışlı) giriş 781 bps, t 65: hizalama doğru.
- 168 çift kayıt atıldı; 1.416 olayda geçmiş yetersiz; 1.134 sürpriz ±%200'e kırpıldı. Aşırı getiri (> %80) yalnız sağlamlık satırlarında: AEHR 16.07.2021, QBTS 19.05.2023.

## Çürütme testleri
Ayakta kalan olmadığı için bağımsız yeniden üretim gerekmedi. Zorla çalıştırılanlarda: (c) plasebo p 0,003 (bilanço günü sıradan günden farklı) ama SPY'dan arındırılınca OOS t 1,36. Rejim: VIX > 20 iken `b_yakinda` AL h=2 +36,6 bps (t 1,94); sınıf vermez, yalnız not.

## 20 Kasım 2026 kapanışı
INTU −4,6 z tepki verdi. Elenen kurallar "INTU sat, 30 yazılım emsalini sat" derdi; veriye göre emsaller ertesi gün geri dönüyor. İşlem önerilmez.

## Şaşırtıcı / hipotezle çelişen
Hipotez (Hou 2007: emsal gecikmeyle izler) 1-3 günde doğrulanmadı; işaret ters. Literatür notuyla (Martineau: büyük hissede sürüklenme yok) uyumlu.
