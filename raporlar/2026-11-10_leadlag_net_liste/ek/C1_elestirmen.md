# C1 — eleştirmen turu (ham ajan çıktısı; taslak rapora itirazlar)

araç: 14/20

Bu not, raporun eleştirmen turundan ÖNCEKİ taslağına yazıldı. Ana ajanın her itiraza verdiği karar en sonda.

1. **[KRİTİK] Vadeli taşıma maliyeti hesaba katılmamış.** #1, #2 ve #4 VİOP vadelisiyle işlem görüyor ama hesap spot fiyatla yapılmış. Uzun vadeli pozisyonun getirisi kabaca spot getiri eksi faiz × gün. 2024–26'da hisse getirisi faizin altında kaldı, bu yüzden "yıl-eşleştirilmiş fazla" vadeli getiriyi şişiriyor. %40–50 faizle 3 günlük taşıma yaklaşık 40–55 bps eder; bu oran dosyada yok, benim tahminim. Dayanak: K2 yıl tablosunda 2026 için h3 brüt 48; vadelide ≈0. Düzeltme: vadeli getiriyi brüt eksi faiz × gün olarak göster ya da bu kuralları spota sınırla.

2. **[KRİTİK] "Kullanılabilir liste" başlığı ile "listeyi kullan" çelişiyor.** 7 kuraldan 4'ü kâğıtta izlenecek. TUPRS için "tek doğrulanmış" ve ORTA–DÜŞÜK etiketi fazla. Dayanak: K2 T6'da 44 bps'te fazla ≈0, OOS t 1,1, SON t 0,7. E3'te tek başına net +11 (t 1,0), etiketi "FILTRE". Düzeltme: listeyi ikiye böl: "gerçek para: QQQ/SMH, yarım boy" ve "kâğıt: diğerleri".

3. **[KRİTİK] Ana hüküm fazla genelleme.**
   - "Yetişmiyor" demek yerine "ek değeri kanıtlanamadı" denmeli. BIST'te YETISME_LONG medyan net +16,9, satırların %62'si pozitif, örneklem düz kuralın ~1/8'i (K1 Part B).
   - Karşı örnekler: IWM→UDOW GERIDE h3 +174, t 3,06, SAGLAM (K1 partA); IWM→SPY h3 +70, t 2,67, OOS t 2,72 (E4); XU030→FROTO YLONG h3 +128, t 3,2, FDR q0,10; XME→EREGL YLONG h1 t 2,4; KBE→AKBNK YLONG k1,5 h2 brüt 202 (n=18), düz kuralda 89.
   - "Devam" da genel değil: ABD'de SADE_LONG medyan −20,5, satırların yalnız %20'si pozitif; ABD'de çalışan kurallar dönüş kuralı (IBS, altın düşüşü → GDXJ); K2 T1: BIST'teki devam simetrik değil, "TL sürükleme izi".
   - Düzeltme: kısa yanıtın 1. ve 2. maddelerini bu sınırlarla yeniden yaz.

4. **[ÖNEMLİ] "Hedef artıda ise al" genel kural gibi veriliyor.** Tek bir kuralda, sonradan yapılmış bir bölmeden çıkıyor ve XU030 kontrolü yok; endeks kuralının kopyası olabilir. K1'de bu aile hiç test edilmedi. Düzeltme: "yalnız TUPRS için, kâğıtta" diye daralt.

5. **[ÖNEMLİ] SAHOL/AKBNK tutarsız.** Tablodaki kural "bant çıkışı"; K1 sabit 3 günlük tutuşu sınadı. K1'in h3 net +74 (t 5,2) sonucu hiç anılmıyor. "Fazla getiri" sütununa net değer yazılmış. Düzeltme: kâğıt listesine al; kuralı K1'de sınanan biçimiyle de yaz.

6. **[ÖNEMLİ] Aday seçimi çifte standartlı.** KBE→AKBNK FDR'yi yalnız q0,10'da geçiyor, 44 bps sürümünde SAGLAM 0, ama listeye alınmış. Buna karşın K1'de SAGLAM çıkan A6 satırları hiç anılmıyor: XLK→SMH ONDE h2 +70 (t 3,15), TLT→ASHR h1 +78 (t 4,2). XME→EREGL SD k1 h3 +67 (t 3,5) FDR q0,05'i geçen satırlardan biri, raporda yok. Düzeltme: bunları gerekçeli bir "elendi/kâğıt" satırıyla ekle.

7. **[ÖNEMLİ] QQQ/SMH tablosu tam kapanış rakamıyla verilmiş.** Kapanıştan 10 dk önce tahminle girince QQQ 76'dan 56'ya iniyor (E4). Kapanış öncesi girişin ek maliyeti ~15–20 bps, after-hours girişin ~6 bps (E4); raporda yok. QQQ 2026'da +5 (n=10); SMH düşük oynaklık döneminde +14 (t 1,1). Düzeltme: gerçekçi beklenti sütunu ekle.

8. **[ÖNEMLİ] TradingView kodları doğrulanmadı.** VİOP'ta 18:00–18:10 dolumu ile spot kapanış müzayedesi arasındaki fark ölçülmemiş. Düzeltme: kodları "teyit et" diye işaretle ve dolum farkı uyarısı ekle.

9. **[KÜÇÜK] SMH için "2016'dan beri her yıl pozitif" yanlış.** K2 T8'de 10/11.

10. **[KÜÇÜK] "Yıl" sütunu ve RYSAS rakamı hatalı.** XU030 ≈ 29 (taslakta 31); KBE ≈ 15 (16); TUPRS'un ~26'sı süzgeçsiz kural için. RYSAS için verilen "+34,8" iki yönlü, hedge'li kuralın sonucu; yalnız uzun sürüm +56.

11. **[KÜÇÜK] Doğrulama kapsamı abartılmış.** V1'de 6 satırın bazı parçalarına bakılmadı. K2 özeti "1'i çürütüldü" diyor; oysa T4'te TUPRS ve ASELS de çürütüldü, T8'de 2016 sonrası "AYAKTA".

12. **[KÜÇÜK] Maliyet ve risk ifadeleri belirsiz.** "~44 bps bireysel komisyon" olgu gibi sunulmuş, K2'de varsayım. "%0,25" pozisyon büyüklüğü mü, risk mi belli değil.

**Sayı kontrolü:** 33 sayı kontrol edildi: 28 doğru, 1 yanlış (SMH "her yıl"), 4 kısmen (TUPRS'un 44 bps'te kalanı, Koza "net ~0", XU030 ve KBE yıllık işlem sayısı).

**Hüküm:** Taslak bu hâliyle tam savunulamaz. Sayıların çoğu doğru, ama üç sorun var: hüküm düşük güçlü bir testten kesin olumsuz sonuç çıkarıyor; BIST'teki devam etkisinin önemli kısmı TL sürüklenmesi olabilir ve vadeli taşıma maliyeti hesaba katılmadı; "kullan" başlığı gerçek parayla yanlış işleme yol açabilir. Gerçek parayla yalnız QQQ/SMH (yarım boy), geri kalanı kâğıtta denmeli.

## Ana ajanın kararı

| # | Karar |
|---|---|
| 1 | Kabul. BIST adayları TL faizi düşülerek yeniden hesaplandı (`yeniden_hesap/FAIZ_USTU.md`); rapordaki BIST sayıları artık faiz üstü getiridir. Sonuç: TUPRS ve KBE → AKBNK'de sayı düşmedi, XU030 kuralının son üç yılı zayıf çıktı. |
| 2 | Kabul. Liste "gerçek parayla (QQQ, SMH)" ve "kâğıtta izle (BIST)" diye ikiye bölündü. |
| 3 | Kabul. Kısa yanıt "çalışmıyor" yerine "çalıştığı gösterilemedi" diye yazıldı; ABD ve BIST ayrımı ve tekil istisnalar eklendi. |
| 4 | Kabul. "Artıda ise al" yalnız TUPRS için bir gözlem olarak bırakıldı. |
| 5 | Kabul. SAHOL/AKBNK kâğıt listesine alındı; iki hesabın kuralı ve sayıları ayrı yazıldı. |
| 6 | Kabul. "Taramada iyi görünen, kanıt saymadıklarım" tablosu eklendi. KBE → AKBNK kâğıt listesinde kaldı. |
| 7 | Kabul. Gerçekçi beklenti sütunu ve yürütme maliyeti notu eklendi. |
| 8 | Kısmen. VİOP kodları 02.11 çalışmasında iki kez doğrulanmış (`tradingview_kodlari.csv`); doğrulanmayan ETF kodları raporda işaretlendi. Dolum farkı uyarısı eklendi. |
| 9–12 | Kabul; düzeltildi. |
