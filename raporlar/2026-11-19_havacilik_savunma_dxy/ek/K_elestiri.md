araç: 5/12

## A) Yöntem: zorunlu düzeltmeler
1. **Gecikme ≠ teslimat düzeyi.** Teslimat ve üretim, talep çevrimini (2-5 yıl önceki sipariş) ve arz kısıtını birlikte taşır. Bu yüzden H1-H2 "DXY gecikmeyi açıklamıyor" sonucunu tek başına veremez. Düzeltme: birikimi geriye kur (B(t-1) = B(t) − net sipariş(t) + teslimat(t); 2018-2025 gerçek birikimle sağla). 1974-2025 için birikim/teslimat oranını (yıl) birincil "gecikme" değişkeni yap. Teslimat düzeyi ikincil kalsın.
2. **G3364 uygun değil.** Savunma uçağı, füze ve uzay aracını (NAICS 336414) içeriyor; C30.3 de askerî ve uzay üretimini kapsıyor. G336411T3'ü kullan. G.17 yöntem notunda kalemin işçi saatinden türetilip türetilmediğini kontrol et: türetiliyorsa seri istihdamı ölçer, gecikmeyi ölçmez. Sonuç "sivil teslimat" diye yazılamaz.
3. **Yapısal kırılma ve olaylar.** 1997 Boeing-MDD birleşmesi, Boeing grevleri (1995, 2005, 2008, 2024), 2001, 2008-09, 2019-20 MAX yasağı ve COVID için kukla değişken zorunlu. Yalnız 2019-21'i dışlamak yetmez. Kararlılığı Chow testi ya da kayan pencereyle sına.
4. **Ortak etken.** Krizde dolar güçlenir, trafik düşer. Yıllık modele ABD resesyon kuklası ve imalat sanayi üretimi girsin. Petrol serisi yoksa bunu sınırlama olarak yaz.
5. **Tarama ve güç.** 0-36 ay × birden çok seri × alt dönem, "en iyi" gecikmeyi seçtirir. Örtüşen yıllık % değişim de otokorelasyonu şişirir. Önceden belirlenmiş tek bir dağıtılmış gecikme modeli kur, toplam etkiyi Wald testiyle sına ve HAC bant genişliğini ≥ 12 + gecikme al. n≈50, alt dönemde n≈25: \|r\| < 0,4 saptanamaz. Sonucu güven aralığı ve saptanabilir en küçük etkiyle ver. "Anlamsız" demek "ilişki yok" demek değildir.
6. **Kur tanımı.** DXY'nin ~%58'i EUR; gelişen ülke kuru yok, yani havayolu alım gücü kanalını ölçmez. Avrupa'da DXY ile EUR/USD neredeyse aynı şey: birini seç. Raporda "DXY ile ölçülen" diye sınırla.
7. **H3 ve H5.** ≥%10'luk dolar dönemleri yalnızca ~8-10 bağımsız bölüm: ortalama testi değil, vaka tablosu yap. USD cinsi Europe A&D'nin DXY ile ilişkisi kur çevirisinden gelen mekanik bir ilişki: EUR serisini kullan. EUAD 2024-10'dan başladığı için dışarıda kalsın. Kayan korelasyon yalnız betimsel kullanılsın.

## B) Taslağın zayıf noktaları
1. **S1 elma-armut.** World A&D net getiri/USD (30 Eki), Europe A&D fiyat getirisi/USD (30 Eki), ITA ise 18 Kas tarihli. EUR'da Europe A&D YTD +%0,8 (MSCI Europe +%9,6), yani USD'deki -%4,2'nin bir kısmı kurdan geliyor. Her sayıya getiri türü, para birimi ve tarih yaz. ITA, DJ US A&D'yi değil "Select" endeksini izliyor: vekil olduğunu belirt.
2. **S2 "çarpan daralması" kanıtsız.** Yalnız güncel F/K var, 2025 sonu F/K yok. Rekor birikim, yeni siparişlerin yavaşladığı ihtimalini dışlamaz. Alternatif açıklamalar da sayılmalı: Ukrayna barış sinyali, ABD geri alım kararnamesi, sektör rotasyonu. Bunu "olası açıklama" diye sınırla.
3. **S3.** Yüksek F/K bir kırılganlık göstergesi, düşüşün kanıtı değil. Factsheet F/K'sı ile ITA'nın ileri F/K'sı (39x) karıştırılmasın.
4. **S5.** 2018→2020 düşüşü gecikmeden değil, COVID talep çöküşü ve MAX yasağından. 5.300'lük açık, IATA'nın trend varsayımına dayanan bir model tahmini: öyle etiketle.
5. **S6 sessizlikten çıkarım.** Bu neden listeleri kura bakılarak hazırlanmaz. Ters yönlü bir kanal da atlanmış: zayıf dolar, maliyeti EUR/GBP, satışı USD olan tedarikçilerin marjını ezer; bu mali sıkıntı gecikme doğurabilir (2025: zayıf dolar ve yoğun darboğaz aynı dönemde). Doğru ifade "kaynaklar kuru neden saymıyor" olmalı, "kurun rolü yok" değil. Bu kanal H1'deki işaretle sınanmalı.
6. **S7.** (a) 2015 Rusya ertelemeleri yaptırımlar ve ruble/petrol çöküşüyle iç içe; DXY'nin kanıtı sayılmaz. (c) Gopinath'ın bulgusu genel ticaret için, uçağa özgü değil.
7. **S8 hesaptan önce yazılmış** (doğrulama yanlılığı riski). Koşullu yaz. "Gelişen ülke erteleme riski" kanıtsız bir hipotez: E dosyası iptal kanıtı bulamadı.

## C) Rapordan önce doğrulanması gereken 5 iddia
1. SIPRI 2025: 2,887 trilyon $, reel +%2,9, ABD -%7,5 (şaşırtıcı), Avrupa +%14.
2. Rheinmetall "2025 kapanışının ~yarısı" (kaynağın güveni düşük): RHM.DE'nin 2025 son kapanışını 760,90 € ile karşılaştır.
3. ITA YTD -%2,8 ve "son 3 ay -%10/-%14": 5 Kasım'daki 3'e 1 bölünmeye göre ayarlanmış veriyle kontrol et.
4. IATA Haziran 2026: açık ≥5.300, birikim 18.000+ (E: 18.100), filo yaşı 15,2, normale dönüş 2031-34. Şu an ikincil kaynaktan; birincil IATA metniyle doğrula.
5. MSCI World A&D: 2025 +%52,5, YTD -%2,9, F/K 33,9/25,3, ilk 10 = %69. Factsheet tarihi ve getiri türüyle birlikte doğrula.
