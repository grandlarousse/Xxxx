araç: 33/35
Model notu: bu alt ajan Fable 5.2 (claude-fable-5-2) ile çalıştı.

## Özet

**(A) XELKT**
- **Kural:** XELKT, BIST Hizmetler altındaki bir sektör endeksi. Yıldız, Ana ve Alt Pazar'daki elektrik sınıfı tüm paylar girer; büyüklük ya da likidite elemesi yok. Yakın İzleme Pazarı'na alınan pay aynı gün çıkar.
- **Güncelleme:** Dönemsel (üç aylık) gözden geçirme yok; kural setinin dönem tablosunda sektör endeksleri yer almıyor. fvt.com.tr'deki "genellikle üç ayda bir" ifadesi kural setiyle çelişiyor.
- **Yeni halka arz:** İlk işlem günü endekse girer (örnek: METEN, 28.07.2026). Faaliyet değişikliğinde, KAP bildirimini izleyen haftanın ilk işlem günü girer.
- **Ağırlık:** Fiili dolaşımdaki piyasa değerine göre, üst sınır yok. Fiili dolaşım oranı haftalık MKK verisinden gelir, yalnız 5 puanlık (oran %50 üstündeyse 10 puanlık) değişimde güncellenir ve tam sayıya yuvarlanır.
- **İlk 10 (yaklaşık, 20.11.2026 çekimi):** ENJSA 17,1; ENERY 14,6; AKSEN 9,7; AHGAZ 8,2; CWENE 4,5; CANTE 4,2; ODAS 3,0; AKFYE 2,9; ENTRA 2,3; BIOEN 2,3. İlk 5 toplam %54, ilk 10 toplam %69. Bunlar resmi BIST ağırlığı değil; İş Yatırım'ın piyasa değeri × halka açıklık oranından hesapladım.
- **Yapı:** Dağıtım ve gaz dağıtımı (ENJSA, ENERY, AHGAZ, ARASE, NTGAZ, VEYAS) endeksin yaklaşık %43'ü. VİOP kontratı olan üç hisse (AKSEN, ENJSA, ODAS) yaklaşık %30.
- **Giriş/çıkış:** Son 3 yılda yaklaşık 12 giriş buldum, çıkış bulamadım. Girişler: ENTRA ve MOGAN (2024), LYDYE (eski TETMT, kod 01.10.2024'te değişti), BIGEN, ENDAE, KLYPV (Şubat 2025), ECOGR (03.11.2025), ARFYE (05.01.2026), BESTE (11.02.2026), METEN (28.07.2026), MASFN (30.07.2026), VEYAS (20.08.2026).
- **Fon (aykırı bulgu):** YONTEM.md "XELKT'nin fonu yok" diyor; bu yanlış. Garanti Portföy Enerji Şirketleri Hisse Senedi (TL) Fonu (TEFAS kodu GNS) en az %80 XELKT payı tutuyor, ölçütü %90 BIST Elektrik Getiri. XELKT'yi izleyen BYF bulamadım.
- **Düzeltmeler:** A1YEN, eski Kartal Yenilenebilir (KARYE). ASTOR, EUPWR ve GESAN XELKT üyesi değil.

**(B) TradingView**
- 57 kodun 57'si doğrulandı (HTTP 200). Sayfadaki şirket adı CSV'nin `not` sütununda (`tv_adi=`).
- Vadeli URL kalıbı: `/symbols/BIST-AKSEN1!/` ve `/symbols/BIST-XU030D1!/`.
- ASTOR ve XU100 sayfalarının başlık biçimi farklı; bu ikisini kanonik URL ve `pro_symbol` alanıyla doğruladım.
- Olmayan kod 404 dönüyor.

**Dosyalar**
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/xelkt_uyeler.csv (42 satır; şemaya ek olarak sonda `not` sütunu var)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/tradingview_kodlari.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/r3_tv/tv_check.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/r3_tv/isy_parse.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/r3_tv/xelkt_tablo.py

## İddia defteri

KS = https://www.borsaistanbul.com/files/bist-pd-agirlikli-pay-endeksleri-ks-tr-2026-ekim-temiz.pdf

iddia | kaynak | alıntı ya da sayı | güven
1. XELKT tipi | https://www.borsaistanbul.com/endeks/xelkt | "Piyasa Değeri Ağırlıklı, Ağırlık Sınırlamalı Olmayan, Fiyat" | yüksek
2. Sektör endeksi kapsamı (md. 3.19) | KS | "Yıldız Pazar, Ana Pazar ve Alt Pazar'da işlem gören şirketlerin paylarından oluşur." | yüksek
3. Kapsam dışı pazarlar (md. 2.14) | KS | "Yakın İzleme Pazarı, Girişim Sermayesi Pazarı ve Piyasa Öncesi İşlem Platformu'nda işlem gören şirket payları" | yüksek
4. Yeni halka arz ilk gün girer (md. 8.4) | KS | "kapsamına girdiği diğer tüm endekslere işlem görmeye başladığı gün geçerli olacak şekilde dahil edilir" | yüksek
5. Sektör değişikliği (md. 8.7) | KS | "bildirimin KAP'ta yayımlandığı haftayı izleyen haftanın ilk işlem günü ... yeni sektör endekslerine alınır" | yüksek
6. Yakın İzleme'ye geçen çıkar (md. 8.1) | KS | "Yakın İzleme Pazarı'na alınan paylar ... kapsamında oldukları tüm endekslerden çıkarılır" | yüksek
7. Sektör endekslerinde dönemsel gözden geçirme yok | KS md. 2.17 tablosu | tabloda BIST 30/50/100/500, Likit Banka, Sürdürülebilirlik, Temettü, Katılım, Geri Alım var; sektör endeksi yok | yüksek (çıkarım)
8. Fiili dolaşım oranı güncelleme eşiği | KS | "%50 ve daha küçükse ve oranda 5 puan veya daha fazla bir değişim varsa" | yüksek
9. Fiili dolaşım oranı yuvarlama | KS md. 2.19 | "FDPO >= %1 ise tam sayı" | yüksek
10. Güncel kural seti yürürlük tarihi | https://www.borsaistanbul.com/bist-endeksleri/kural-setleri-ve-degisiklikleri | 28.10.2026 | orta
11. METEN ilk gün XELKT'ye alındı | https://www.kap.org.tr/tr/Bildirim/1637095 | "BIST Elektrik ve BIST İzmir endeksleri kapsamına dahil edilecek olup"; 28/07/2026; fiili dolaşım %21 | yüksek
12. Üye sayısı ve toplam piyasa değeri | https://fvt.com.tr/hisseler/yerli/sektor/elektrik | "XELKT kapsamında 42 şirket bulunuyor; toplam piyasa değeri yaklaşık 823,3 milyar ₺" (İş Yatırım toplamı 803.376 mn TL) | orta
13. Büyük üyelerin piyasa değeri ve halka açıklığı | https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx | ENJSA 131.807,3 mn TL / %20,0; ENERY 130.050 / %17,3; AHGAZ 113.880 / %11,1; AKSEN 78.240,4 / %19,0 | yüksek (kaynak), tarih: 20.11.2026 çekimi
14. İlk 10 yaklaşık ağırlık | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/xelkt_uyeler.csv | 17,13 / 14,62 / 9,66 / 8,22 / 4,47 / 4,21 / 3,00 / 2,91 / 2,33 / 2,28; toplam 68,8 | orta (hesap, resmi değil)
15. Halka açık piyasa değeri toplamı | aynı CSV | 153.847 mn TL (toplamın yaklaşık %19'u) | orta
16. VİOP'lu üç hissenin toplam ağırlığı | aynı CSV | 29,8 | orta
17. Faaliyet grubu ağırlıkları | aynı CSV | yenilenebilir 24,9; gaz dağıtımı 24,2; termik 20,0; dağıtım-perakende 19,3; panel-ekipman 8,6; diğer 2,9 | düşük-orta (sınıflama kısmen kendi bilgim)
18. İş Yatırım ve fvt piyasa değerleri örtüşüyor | iki kaynak | AHGAZ 113,9; AKSEN 78,2; ENERY 130,1; ENJSA 131,8; VEYAS 41,7 mlr TL | yüksek
19. XELKT'ye dayalı fon var | https://kap.org.tr/tr/fon-bilgileri/genel/gns-garanti-portfoy-enerji-sirketleri-hisse-senedi-tl-fonu-hisse-senedi-yogun-fon | "fon toplam değerinin en az %80'i devamlı olarak BIST Elektrik Endeksi'nde (XELKT) yer alan yerli ortaklık paylarına" | yüksek
20. Fonun ölçütü ve halka arzı | aynı sayfa | %90 "BIST Elektrik Getiri Endeksi (XELKT)" + %10 BIST-KYD Repo; 12/02/2025 | yüksek
21. ARFYE ilk işlem | https://www.bloomberght.com/ilk-ceyrekte-14-sirket-bist-te-islem-gormeye-basladi-3774104 | "5 Ocak'ta işlem görmeye başlayan ARF Bio Yenilenebilir Enerji" | orta (arama özeti)
22. BESTE ilk işlem | https://kap.org.tr/en/Bildirim/1552744 | "BESTE.E in the BIST Main as of 11/02/2026" | orta (arama özeti)
23. VEYAS ilk işlem | https://www.yenisafak.com/veyas-hisse-borsada-islem-gormeye-basladi-mi-turker-veyas-halka-arz-buyuklugu-aciklandi-h-4849586 | "İşlem Görmeye Başlayacağı Tarih 20/08/2026" | orta (arama özeti)
24. MASFN ilk işlem | https://kap.org.tr/en/api/BildirimPdf/1637308 | 30/07/2026 | orta (arama özeti; bildirim numarası eşleşmesi doğrulanmadı)
25. ECOGR ilk işlem | https://gedik.com/halka-arzlar/ecogreen-enerji-halka-arzi | "İlk İşlem Tarihi 03 Kasım 2025" | orta (arama özeti)
26. KLYPV, ENDAE, BIGEN 2025 | https://borsa.doviz.com/halka-arz/gecmis-halka-arzlar ve arama özetleri | KLYPV gong 13.02.2025; ENDAE 13.02.2025; BIGEN talep toplama 28-30.01.2025 | düşük-orta
27. LYDYE eski TETMT | https://halkarz.com/haberler/tetamat-gida-tetmt-sirket-unvan-degisikligi/ | "TETMT" kodu 01/10/2024'ten itibaren "LYDYE" | orta (arama özeti)
28. Eski üye sayısı | https://borsaistanbul.com/en/index-detail/216/bist-electricity | 32 (tarih belirsiz) | düşük
29. TradingView toplu doğrulama | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/tradingview_kodlari.csv | 57/57 HTTP 200 | yüksek
30. Vadeli URL kalıbı ve olmayan kod | https://www.tradingview.com/symbols/BIST-AKSEN1!/ | "AKSA ENERJI URETIM FUTURES Price Chart — BIST:AKSEN1! — TradingView"; BIST-ZZZZQ 404 | yüksek

## açık kalanlar
- **Resmi ağırlıklar yok:** Borsa İstanbul'un endeks sayfası bileşen ve ağırlık göstermiyor. BIST'in kullandığı tam sayıya yuvarlı ve eşikli fiili dolaşım oranı İş Yatırım'ın oranından sapabilir (METEN: KAP'ta %21, İş Yatırım'da %13,7).
- **Veri tarihi:** İş Yatırım sayfasında tarih etiketi yok; "20.11.2026 çekimi, son kapanış" varsayıldı.
- **Çıkışlar ve tam giriş listesi:** Son 3 yıl için resmi kaynaktan doğrulanmadı. "Çıkış yok" çıkarımı, kendi bilgimdeki yaklaşık 30 eski üyenin hepsinin bugünkü listede olmasına dayanıyor. Kesinleştirmek için KAP'taki "Endeks Şirketlerinde Değişiklik" bildirimlerini taramak gerekir.
- **"?" işaretli alanlar (CSV'de):** halka arz yılı A1YEN (2021?), LYDYE, PAMEL, ZEDUR; ana faaliyet BESTE, BIGEN, CONSE, ECOGR, LYDYE, MASFN, METEN, VEYAS, ZEDUR. İşaretsiz yıl ve faaliyetlerin çoğu da kendi bilgim, kaynakla doğrulanmadı.
- **Kısmi tarihler:** BIGEN ve ENDAE'nin kesin ilk işlem günü, KARYE→A1YEN değişikliğinin tarihi, LYDYE'nin XELKT'ye giriş tarihi bulunmadı.
- **BYF:** XELKT'yi izleyen BYF olmadığı tek aramaya dayanıyor; TEFAS ve BYF listesinden teyit edilmedi.
- **Erişilemeyen sayfa:** ekonomist.com.tr 403 verdi; aynı bildirim KAP'tan okundu.