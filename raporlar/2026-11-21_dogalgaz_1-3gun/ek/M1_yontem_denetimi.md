araç: 9/12

(A) Zorunlu düzeltmeler
1. Seçim kuralının 2. ve 3. adımları işlem gören ürünün net getirisiyle uygulanır: yukarı sinyal için BOIL (ve UNG uzun), aşağı sinyal için KOLD uzun. Birleşik yön ve UNG açığa satış sonuçları BH sayımına girer ama etiket almaz, yalnız teşhis içindir.
2. t istatistiği olay dizisinden değil, işlem günü takvimindeki günlük strateji P&L dizisinden hesaplanır (çakışan lotlar toplanır). Newey–West gecikmesi h olur. Örtüşmeyen alt küme ayrıca verilir.
3. Gaz sinyali testlerinde IS 2011-10-06'da başlar, böylece UNG ile BOIL/KOLD aynı dönemi kapsar. UNG 2007–2011 yalnız sağlamlık içindir. Ek maliyet stresi: |z_UNG,t| > 2 olan günlerde maliyet 2 katına çıkar. Taban maliyetler gerçekçi.
4. Her hücrenin OOS'de tespit edebileceği en küçük etki (MDE) raporlanır: 1,65·σ_h/√n_bağımsız (bps). MDE, IS ortalamasının 2 katını aşıyorsa sonuç KULLANILAMAZ yerine "gücü yetersiz" diye etiketlenir.
5. NG=F günlük seri sinyal olarak kullanılmaz. |r_NG − r_UNG| > %6 olan 60 gün maskelenir; bunların çoğu ayın 27–30'u arasında vade sonu artefaktıdır (örneğin 2026-01-29'da log −0,644). Günlük ve saatlik NG=F asla karıştırılmaz, çünkü saatlik seri birkaç gün erken vade değiştiriyor (2026-11-20 03:00'te 3,198 → 3,583). G4 yalnız UNG saatlik veriyle yapılır.
6. "BOIL ≈ 2×UNG'den sapan günü at" kuralı kaldırılır. 2026-02-02 gerçek bir harekettir: BOIL −%50,5, UNG basit getirisi −%24,9 (2 katı −%49,8). Sapmaların kaynağı BOIL'un endeksindeki (Bloomberg NG alt endeksi) farklı vade geçiş takvimidir. Kontrol basit getiriyle yapılır. Gün yalnız ham fiyat oranı 1:N bölünme oranına uyuyorsa atılır. Düzeltilmiş veride |r| > %60 olan gün yok, beklenen atma sayısı 0.
7. L1 erimesi şöyle ayrıştırılır: gerçekleşen BOIL(h) − 2×birikimli UNG(h) farkı = kuramsal oynaklık erimesi (BOIL ≈ σ², KOLD ≈ 3σ², pencere içi UNG günlük varyans toplamı) + ücret (yıllık %0,95, günde yaklaşık 0,4 bps) + artık (vade takvimi farkı). Ortalamalar örtüşmeyen pencerelerle alınır.
8. Sepet: CRK'de 2015–16'da |r| > %25 olan 19 gün var (2015-08-12'de +%67). Sinyal kurulurken üye getirileri ±%15'te kırpılır, P&L ham kalır. CRK'li ve CRK'siz sonuç ayrı verilir. Üyelik şartı: önceki 60 günün medyan dolar hacmi ≥ 20 milyon $. Hacmi 0 olan günler (NEXT'te 335 gün) eksik veri sayılır.
9. G8 için UNL: kapanışı değişmeyen günler (yaklaşık %3) ve hacmi 0 olan günler eksik veri sayılır. 20 günlük toplam için en az 15 geçerli gün gerekir.
10. TTF=F'de hacmi 0 olan 469 gün var. X1, kayan 60 günde hacmin %90'dan fazla gün pozitif olduğu ilk tarihten başlar. Sinyal z'si ±4'te kırpılır. Duyarlılık testi olarak ayın son 2 ve ilk 2 işlem günü hariç tutulur (vade geçişi).

(B) Eklenecek testler
- T1 Trend ve kırılım: UNG kapanışının 10 ve 20 günlük ortalamaya göre konumu ile 20 günlük en yüksek/en düşük kırılımı → BOIL/KOLD, h ∈ {1,2,3}. Perakende yatırımcının en çok kullandığı yöntem; boş çıksa da kullanıcı için bilgi değeri var.
- T2 G1 × oynaklık rejimi: σ60 üçte birliklerine göre ayrı sonuç, yalnız h=1. Dönüş ve momentum etkisi genellikle rejime bağlıdır.

(C) Çıkarılacak testler
- E7: beklenti zaten boş, kullanıcı için karar değeri yok.
- X4: 2023'ten kısa örneklem, mekanizma zayıf, test sayısını şişirir.
- G9 yapılmıyorsa test sayımına girmez.

(D) Veri kontrol hükümleri
- NG=F günlük kapanışı 14:30 ET uzlaşma fiyatıdır. Günlerin %92'sinde 14:00–15:00 barının aralığına düşüyor; 16:00–17:00 barında bu oran %41. Fiyat 16:00'da biliniyor, yani ileri bakış yok. Ama seri vadesi dolan kontratı izliyor ve vade sonu sıçramaları içeriyor (yukarıda madde 5).
- TTF=F'nin t tarihli barı aynı günün ICE kapanışıdır. Son saatlik bar 11:00–12:00 ET'de; gecikme 0'da medyan fark %0,45, ±1 günde %2,0. Bar 16:00 ET'de biliniyor. Bir gün geciktirme yalnız duyarlılık testi olarak tutulur.
- UNG günlük kapanışı 16:00 kapanışıdır (15:30 barının kapanışıyla %91 eşleşme). Bölünmeler düzeltilmiş.
- Hayatta kalma yanlılığı doğrulandı: SWN, eski CHK, CTRA/COG yok; 2021 öncesi sepet yalnız hayatta kalanlardan oluşuyor. Bu, E testlerini iyimser gösterir; raporda belirtilmeli.
