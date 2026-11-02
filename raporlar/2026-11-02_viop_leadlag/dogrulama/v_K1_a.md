# v_K1_a — Bağımsız doğrulama: K1 açılış gap-fade (CIMSA/OYAKC + 47 hisse)

Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a/` (vk.py kendi yükleyici; ll.py import EDİLMEDİ). e1..e12 betikleri, res_e*.csv çıktıları.
Tanım: cc=log(adj_t/adj_{t-1}), intra=log(c/o), gap=cc−intra; cc veya gap fiyat bazında +%10,5/−%10,5 dışı → NaN; |intra|>ln1,25 → NaN; hacimsiz gün atıldı. Strateji: |gap|>%1 günlerde −sign(gap)×intra − maliyet. IS 2014–2020, OOS 2021–2026. t = Newey-West(5).

## Karar: DÜZELT — etki gerçek ama "işlenebilir" kısmı zayıf

| Test | CIMSA | OYAKC |
|---|---|---|
| (a) Yeniden üretim, net 10 bps IS | +28,0 (t2,54), n287 | +37,5 (t2,09), n231 |
| OOS | **+63,8 (t3,32)**, n230 | **+39,7 (t2,19)**, n264 |
| Pozitif yıl | 12/13 (2014 +0,3; 2015 +1,1 ≈ 0) | 12/13 |
| Temiz IS 2016–20 | +54 (t2,9) | +46 (t1,8) |
| Bootstrap OOS (20 blok) P(ort≤0) | 0,000 | 0,001 |
| OOS'ta en iyi 10 işlemin kâr payı | **%71** | **%82** (en iyi 13 işlem: %98) |
| En iyi 10 işlem atılınca OOS | +23 (t1,25) | +18 (t1,16) |
| 47 hisse içinde seçim düzeltmeli (max-t permütasyonu) p | 0,04 | 0,22 |
| 47 hissede BH-FDR (OOS) | geçer (tek hisse) | geçmez |
| Açılış girişi, 2023-12+ (h1 örneklemi) | +78,6 (t2,93), n90 | +47,8 (t2,72), n106 |
| **10:30 TSİ girişi** (1. saatlik bar kapanışı) | **+58,6 (t2,52)**, iddiayla aynı | +33,6 (t2,49) |
| 11:30 TSİ girişi | +40,6 (t2,43) | +14,3 (t1,07) |
| 10:30 girişte en iyi 5 işlem hariç | +29 (t1,6) | +12 (t0,95) |
| Başabaş maliyet (açılış girişi, tüm dönem / OOS) | ~54 / ~74 bps | ~49 / ~50 bps |

Rakamlar kimya ajanınınkiyle birebir tutuyor. Yanlış olan kısım yorumu.

## (b) Zamanlama ve "açılış gürültüsü" testi
- Yahoo günlük açılışı = **açılış seansı müzayede fiyatı**. 2026 m5 verisinde 06:55 UTC'deki hacimsiz barla %100, h1 ilk barın açılışıyla %99,8 aynı. Yani gap bir bid/ask işlemi değil, tek fiyatlı müzayede fiyatıdır. Gap 09:55–10:00 TSİ'de belli olur.
- **VİOP bu fiyattan dolum veremez.** Vadeli 09:30'da açılıyor (spot müzayededen önce). Vadelinin açılış fiyatı ile spot açılışı arasındaki fark, baz düzeltmesinden sonra medyan 36–46 bps. Açılıştan dolum ancak spot müzayedesine katılarak mümkün; açık satış da kısıtlı.
- **Saf baskı gürültüsü küçük.** Müzayede fiyatından ilk sürekli işleme geçerken eğim −0,013 (t−3,9); düşük likiditede −0,027 (t−4,3). Ama büyüklük medyan 0–4 bps; 50–70 bps'lik getiriyi açıklayamaz.
- **İlk 30 dk payı büyük.** Havuzda (47 hisse, 2023-12+) gap'in açılış→10:30 getirisine eğimi −0,048 (t−5,6), 10:30→kapanış getirisine eğimi −0,034 (t−2,5). Geri dönüşün yaklaşık yarısı (hisse medyanı %53) ilk 30 dakikada gerçekleşiyor. Düşük likidite havuzunda net getiri açılış girişinde **+32 bps (t2,8)**, 10:30 girişinde **+12 bps (t1,3)**, 11:30'da +10 bps (t1,2).
- **Sinyal sadece müzayede gap'inde çalışıyor.** Sinyal 10:30 fiyatına kadarki toplam hareketle tanımlanırsa (gap2) etki kayboluyor: CIMSA −4, OYAKC +1, havuz −13 bps (t−3,0).
- **Vadelinin kendi açılış baskısı mekanik "kârı" gösteriyor.** Vadelinin ilk işlemi gürültülü olduğu için onun fade'i 47 hissenin 40'ında pozitif çıkıyor; likit hisselerde bile (AKBNK +38, TCELL +81, HALKB +95 bps). Aynı günlerde spot fade bunu göstermiyor. Gürültülü bir açılış baskısının sahte fade kârı ürettiğinin doğrudan örneği.
- **Ana kâr bid-ask sıçraması değil.** Kârın çoğu −8 ila −16%'lık gerçek gün-içi çöküş/dönüş günlerinden geliyor (2023 deprem sonrası çimento rallisi, Eyl–Eki 2023, 2021). Bu tablo aşırı tepki ya da likidite sağlama primine uyuyor.
- İleriye bakma: sinyal açılışta biliniyor, temizlik filtreleri geçerli günleri silmiyor (±%10 marj nedeniyle cc ≤ ln1,1). **Veri tuzağı:** 2014–2015 Yahoo açılışları şüpheli. GARAN/THYAO gap'inin XU100 gap'iyle korelasyonu o yıllarda 0,38–0,65, 2016 sonrasında 0,84–0,94; gap oynaklığı da 2 kat. CIMSA'nın 2014–15 katkısı ≈0 olduğu için sonucu şişirmiyor.

## (c) Sağlamlık (CIMSA / OYAKC, OOS net 10)
- Eşik taraması monoton: %0,5 → +29/+25, %1 → +64/+40, %2 → +82/+57. Plasebo (|gap|≤%1) ≈ 0.
- Yön: CIMSA'da long (gap<0) +141 (t3,9), short +41 (t1,9). OYAKC'de long +34 (t1,5), short +42 (t1,7).
- Deprem dönemi hariç +59/+37; tavan/taban açılışlar hariç +66/+40; ham gap (temettü düzeltmesiz) +58/+38.
- z-eşik (60 günlük gap σ): z>1,5 → +91/+45. Hisseye özgü gap fade'i +68/+42 veriyor. **Piyasa gap'i (XU100) hisseyi öngörmüyor** (+14/+15, t<0,6). XU100 hedge'iyle sonuç +47/+36.
- Gap kovası CIMSA'da monoton değil (%2–4 kovası OOS −2). Kâr %1–2 ve %4–9 kovalarında.

## (d) 47 hisse ve likidite grupları
- Koordinatörün "−0,03..−0,16" aralığı tutmuyor. Doğru değer corr(gap, intra) 2021+ için **−0,12..+0,03**, medyan −0,05, 47 hissenin 44'ünde negatif. ll panelinden hesaplanan değer de birebir aynı.
- |gap|>%1 fade, OOS net 10: 27/47 hisse pozitif, 2 hissede t>2, **FDR'yi sadece CIMSA geçiyor**. IS ve OOS'un ikisinde de pozitif olan 16/47.
- **Likidite eğimi belirgin.** t−1'e kadarki 60 günlük TL hacimle zamanla değişen terciller (havuz, eşit ağırlıklı günlük portföy, net 10):

| Tercil | IS | IS 2016–20 | OOS |
|---|---|---|---|
| Düşük | +30 (t5,8) | +46 (t6,4) | **+22 (t2,7)** |
| Orta | +8 | +20 (t2,8) | +4 |
| Yüksek | −9 | +2 | −13,5 |

  Tüm havuzun OOS'u +6,5 (t1,1).
- 10:30 girişinde 47 hissenin sadece 21'i net pozitif, medyan −1,2 bps; **BH-FDR'yi hiçbiri geçmiyor**. En iyisi CIMSA (p=0,009; ilk sıradaki hisse için BH eşiği 0,0011).
- XU100'de etki yok: |gap|>%1 OOS brüt +3,7, net −6. F_XU030 için 2–4 bps maliyetle bile kullanışsız.

## (e) Maliyet ve işlenebilirlik
- VİOP ön-ay vadeli likiditesi (545 bülten günü), medyan: CIMSA 137 mn TL/gün (5,4 bin işlem), OYAKC 161 mn TL/gün (7,6 bin işlem). Küçük pozisyon için yeterli. Bir tik CIMSA'da ≈3–5 bps, OYAKC'de ≈5–6 bps (tik büyüklüğü ?). Abdi-Ranaldo spread tahmini (140–270 bps) oynaklıkla kirlendiği için KULLANILMADI.
- 10:30 girişinde brüt getiri CIMSA ≈69, OYAKC ≈44, düşük likidite havuzu ≈22 bps. Bağlayıcı kısıt maliyet değil; örneklem (3 yıl, 90–106 işlem), kâr yoğunlaşması ve seçim yanlılığı. Kazananın laneti hesaba katılınca CIMSA için beklenen gerçekçi brüt değer 20–35 bps aralığında olmalı.
- Açık satış kısıtı ve yasakları (2023 deprem, Mart 2025) spotta short tarafını engeller. VİOP'ta engel yok.

## Güven
- İstatistiksel varlık, açılış fiyatıyla: CIMSA **ORTA**, OYAKC **DÜŞÜK** (seçim düzeltmesinden sonra anlamsız), 47 hisse düşük likidite tercili **ORTA**.
- İşlenebilir VİOP versiyonu (10:30 girişi): **DÜŞÜK**. Tek seçilmiş hisse, FDR'den geçmiyor, en iyi 5 işlem hariç t1,6.
