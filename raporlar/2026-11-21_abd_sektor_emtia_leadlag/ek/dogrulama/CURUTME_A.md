# Çürütme A: panik dönüşü kümesi (S1, S2)

Betik: `kod/curutme_a.py` (17 sn, ortak.py'den bağımsız hesap). Döküm: `ek/dogrulama/curutme_a/ozet.txt`. "abn" = sürüklenme düzeltilmiş net.

## Hüküm
- **S1 ve S2 raporlandığı hâliyle (ayrı ETF sinyalleri 37–79 bps; "yarıiletkene özgü" 62 bps): kullanılamaz.** Sayılar yeniden üretildi ama ETF'e özgü değil, seçimle şişmiş ve bakılmamış 2000–2004 döneminde anlamsız.
- **Geriye tek bahis kalıyor: yüksek betalı ETF'lerde panik günü dönüşü. Koşullu kullanılabilir**: küçük pozisyon, kaldıraçsız, beklenti raporlananın yaklaşık yarısı.

## Destekleyenler
- Yeniden üretim birebir (IBB 238 / 79,1 / 2,70 / 2,59; yarıiletken grubu 742 gün / 61,7 / 2,70 / 2,84).
- Sabit 12 ETF sepeti, VIX > 25 ve IBS < 0,2, 2005–2026: 452 sinyal günü; h=1 net 51,7, abn 46,4 bps, t 3,68, isabet %58; 17 yılın 16'sı pozitif. h=2: abn 63,6, t 3,60.
- Krizler tek tek çıkınca t 2,7–3,8; dördü birden çıkınca (132 gün) 56 bps, t 2,90. En iyi 10 gün hariç 35 bps, t 3,0.
- Kazancı koşul değil kural getiriyor: "VIX > 25 her gün al" 3,9 bps; IBS ≥ 0,2 günleri −7,3 bps; rastgele gün plasebosu p < 0,004.
- Sınır hariç (IBS < 0,15) 42,9 bps; VIX 1 gün gecikmeli 55,5 bps (t 3,96).
- 5 dakikalık veri (59 gün, 5 ETF): 15:45 sinyali kapanış sinyalinin %81'ini yakalıyor, erken sinyalin %81'i kapanışta geçerli; VIX eşiği 1 günde farklı. Yanlış alınacak bant (IBS 0,20–0,35) 9 bps: beklenen kayıp yaklaşık %15.

## Zayıflatanlar
1. **Bakılmamış dönem 2000–2004:** 212 gün, 10,7 bps, t 0,54, isabet %50 (2002, 2003 negatif). 2000–2026 birleşik: 33,7 bps, t 3,16.
2. **Seçim yanlılığı:** sonuca bakılmadan kurulan sepet (9 sektör + DIA, MDY, EFA, VTI) 2005–26'da 27,8 bps (t 2,40; OOS t 0,98); 2000–26'da 15,9 bps, t 1,87. Yalnız SPY 17,6 bps, t 1,51. QQQ üç dönemde de pozitif (30 / 41 / 56 bps).
3. **OOS zayıf:** VIX > 25 h=1 OOS t 1,83 (eşik 2,0); h=2 2,11. VIX > 20'nin OOS gücü (t 3,51) IS'te ölü olan 20–25 bandından geliyor (IS t 0,77): eşik kararsız.
4. **Piyasa dönüşü:** SPY hedge'li 13,9 bps (OOS t 1,33); kazancın yaklaşık %70'i piyasa.
5. **Yavaş ayı piyasası:** 2022'de 66 günde 13 bps. Blokun ilk 3 gününde 25 bps (t 1,43), sonrasında 57 bps.
6. **Kümelenmiş t yanıltıcı:** 105 blok (95'inde sinyal), blok kümeli t 6,7; bloklar tanım gereği yükselişle bittiği için iyimser. Temkinli ölçü HAC t.

## Giriş ve çıkış
Yalnız gece 4,7 bps; ertesi gün içi 34,8 bps (t 3,29): ertesi açılış girişi ETF'te etkinin %75'ini koruyor. Bir gün geç giriş değersiz (10 bps, t 0,81). İkinci gün anlamlı ek getirmiyor; h=3'te t düşüyor.

## Tehlike
- Sepet-gün standart sapması %2,65; en kötü %5 eşiği −%3,7; en kötü gün −%11,2 (11.03.2020); tek ETF −%12,4.
- En büyük düşüş −%19,9 (30.09–15.10.2008); art arda 5 sinyal günü −%19,8.
- Kaldıraç: TQQQ, 3 × QQQ'nun 13,5 bps altında (t −2,8); standart sapma %7,7, en kötü −%18,3. SOXL en kötü −%31,8.
- Maliyet 20 bps olursa t 2,0.

## Yarıiletken grubu (S2)
- 2010 ve 2005 öncesi başlayan hisselerle sonuç aynı (58,5 / 60,8 bps). Batmış hisseler veride yok; asıl yanlılık sınanamadı.
- Yanlılıksız araçta "özgü" pay doğrulanmadı: SMH SPY hedge'li 26 bps, t 1,77 / 1,77; SOXX 11 bps, t −0,57 / 2,28.
- Hisseye özgü pay (SMH hedge'li) 30 bps, OOS t 1,51; VIX > 20'de OOS t 0,21.
- Grup kazancının 43 bps'i gecede, ertesi açılış girişi 5,8 bps (t 0,49). ETF'te tersi: gece 0,9, gün içi 53 bps. Hisse kapanış fiyatı etkisi ya da yanlılık şüphesi.

## Kasım 2026
Kural 5 gün tetiklendi: 5 Kas +%1,29, 6 Kas +%2,97, 17 Kas +%0,77, 19 Kas −%5,00 (toplam yaklaşık sıfır). 20 Kasım kapanışında 12 ETF'in tamamı açık, sonucu yok (SPY −%3,6; blokun 2. günü).

## Önerilen kural (kullanılacaksa)
15:45–15:50'de VIX > 25 ve IBS < 0,2 ise QQQ (isteğe göre IWM, SMH) kapanışta alınır, ertesi kapanışta satılır. Kaldıraç, hisse ve geç giriş yok. Beklenti: işlem başına net +%0,3 dolayı, isabet %55–58, standart sapma %2,7, en kötü işlem −%11–12, yılda ortalama 20–25 sinyal günü (medyan yıl 8; 22 yılın 5'inde hiç). Bırakma: strateji sermayesinde −%20 düşüş ya da 60 sinyal sonunda toplam ≤ 0.

## Açık kalanlar
Batmış yarıiletken hisseleri; 5 dakikalık örneklemde yalnız 5 panik günü; 2000–04 en yüksek/en düşük verisinin kalitesi; 20 Kasım sinyalinin sonucu.
