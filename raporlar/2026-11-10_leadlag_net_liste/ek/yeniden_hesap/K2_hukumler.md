# K2 — bağımsız sağlamlık hesabı: hükümler (ham ajan çıktısı)

araç: 9/30

Sekiz testin hepsi kendi kodumla (kod2/k2.py) yeniden hesaplandı. K1'in örneklemi yeniden üretildi: XU030 k1 h3 n458, KCHOL k1,5 h2 n245 (K1 246). Hiçbir sinyal 'AYAKTA' çıkmadı. Yıl-eşleştirilmiş fazla genelde brütün yaklaşık %40-60'ı kadar; 44 bps maliyette hisse kurallarının çoğu sıfırın altına iniyor. T1 ZAYIFLADI: endeks momentumu var (h3 fazla +30, t 2,3; h2 +15, t 1,5) ama IS zayıf, 2022 aşırı etkili, ayna taraf yok. T2 ÇÜRÜTÜLDÜ: hisse sepeti eksi XU030 farkı ~0, yani etki endeksin kendisi. T3 ZAYIFLADI: plasebo p 0,047 / 0,0025 / 0,0075, ama plasebo ortalaması gerçeğin yaklaşık yarısı. T4: KCHOL ZAYIFLADI, TUPRS ve ASELS ÇÜRÜTÜLDÜ, EREGL ZAYIFLADI. T5 ZAYIFLADI ve en sağlam aday: AKBNK k1,5 h2 fazla +64 (t 2,7), IS/OOS/SON pozitif, ama OOS t 1,1 ve net44 fazla yalnız +20. T6 ZAYIFLADI: 'hedef geride' koşulu ters çalışıyor, TUPRS aynı gün düşmüşse fazla ~0. T7 ZAYIFLADI: 1 gün geç girişte fazla +17 (t 1,0), likidite ince. T8: fark dönemden geliyor; 2016+ ayakta, 2011-15'te etki yok. Öz-denetim: T1'in ilk 3 işlemi ham JSON'dan saf python ile elle doğrulandı, pandas ile birebir. Eksik veri yok.

- **T1 endeks momentumu (XU030/XU100): ZAYIFLADI** — Yıl-eşleştirilmiş fazla h3 +30 (t 2,3), h2 +15 (t 1,5). IS t 1,4, 2022 tek başına aşırı (fazla +90). Ayna taraf yok: z<=-1 sonrası h2 ham getiri -2, h3 +20 bps. Simetrik momentum değil, TL sürüklemesinin izi olabilir.
- **T2 gün-kümeli 15 hisse sepeti: CURUTULDU** — Sepet eksi XU030 farkı ~0 (h3 fazla 0, t 0,0; h2 +5, OOS ve SON negatif). Hisse seçimi bir şey katmıyor, etki endeksin kendisi. 44 bps'te fazla eksi maliyet negatif (h3: 28-44).
- **T3 plasebo: ZAYIFLADI** — p 0,047 / 0,0025 / 0,0075: gerçek sinyal yıl dağılımının ürünü değil. Ama plasebo ortalaması gerçeğin yaklaşık yarısı (h3: 25 vs 54), yani brütün yarısı sürükleme. Fazla t 1,5-2,3 çoklu test düzeltmesini geçmez.
- **T4 hisseye özgü (KCHOL, TUPRS, ASELS, EREGL): ZAYIFLADI** — KCHOL k1,5 h2 artık +41 (t 3,4) ama OOS artık t 0,8, net44 fazla +20: ZAYIFLADI. TUPRS (k1 h3 fazla +40 t 2,2, artık +17 t 1,2, net44 fazla -4) ve ASELS (artık ~0): ÇÜRÜTÜLDÜ. EREGL k1,5 h2 fazla +53 t 2,7 ama k1 h2 ve h3'te t<=2: ZAYIFLADI. Etki büyük ölçüde endeks momentumu.
- **T5 KBE -> AKBNK: ZAYIFLADI** — k1,5 h2 fazla +64 (t 2,7), IS/OOS/SON pozitif ama OOS t 1,1, 11/16 yıl pozitif. Aynı gün XU030 z>=1 oranı %20; XU030 z<1 alt kümesinde de +56 (t 2,0), endeks etkisine indirgenmiyor. Sıra XU030 32 < 4 banka 50 < AKBNK 64 tutarlı. k1,0 h2 +40 (t 2,6) yönü doğruluyor. net44 fazla yalnız +20, çoklu test düzeltmesi yok. En sağlam aday ama ayakta değil.
- **T6 TUPRS <- ABD rafinerileri: ZAYIFLADI** — Uzun h2 fazla +33 (t 2,1), h3 +42 (t 2,1); OOS t 1,1, SON t 0,7; net44 fazla ~0. Kısa taraf brüt ~0 (-3/+3), kısa yok. 'Hedef geride' koşulu ters: TUPRS t günü <=0 ise fazla +1/+11 (t 0,1/0,4) ÇÜRÜTÜLDÜ; >0 ise +58/+67 (t 2,7/2,3). Endekse göre göreli alt gruplar tutarsız.
- **T7 RYGYO -> RYSAS: ZAYIFLADI** — z>1 h1 fazla +54 (t 3,1), net10 +63; IS t 1,5, OOS ve SON t 3,0 (yeni döneme yığılı). 1 gün geç girişte fazla +17 (t 1,0), net10 +26 (t 1,5), net44 -8. RYSAS 250 gün medyan hacim 145 mn TL, RYGYO 79 mn TL (ince). Kapanışa 10 dk kala RYGYO z'si kesin bilinmez.
- **T8 dönem uzlaştırması (QQQ, SMH): ZAYIFLADI** — Fark dönemden geliyor. QQQ h2 tüm dönem net +36 (t 2,9; K1 +34 t 2,7 ile uyumlu), 2016+ +53 (t 3,5), 2011-15 +1 (t 0,0). QQQ h3 2016+ +68 (t 3,7; önceki +77 t 3,9 ile uyumlu), 2011-15 +28 (t 1,1). SMH h1 2016+ +34 (t 3,3), 2011-15 -13 (t -1,4). 2016+ AYAKTA (QQQ 11/11 yıl fazla pozitif), 2011-15 YOK; rejim bağımlı, tüm dönemde zayıflıyor.

## Açık kalanlar
- Çoklu test düzeltmesi yok. K1 sinyalleri taramadan seçildiği için t değerleri iyimser.
- Blok/bootstrap t yok. Yıl yıl pozitiflik oranı n>=3 olan yıllarla hesaplandı.
- 2022 yılı dışarıda bırakılarak T1/T5/T6 yeniden denenmedi (T1'de 2022 fazla +90).
- Gerçek spread, likidite ve kayma ölçülmedi; maliyet 5/10/13/44 bps varsayım.
- Kapanışa 10 dk kala sinyal (vekil) yerine tam kapanış z kullanıldı; vekil sinyalin kenarı test edilmedi.
- T6 ve T7 için elle (saf python) doğrulama yapılmadı, yalnız T1'in ilk 3 işlemi doğrulandı.
- Veri hatası maskesi (|r|>0,25) PGSUS, RYGYO ve RYSAS için 1'er gün sildi; kalıcı seviye kayması türü hatalar ayrıca denetlenmedi.
- Hacmi 0 günler atıldığı için tek hisse getirileri hissenin kendi geçerli günlerine göre hesaplandı (T7 RYSAS dahil); sepet testlerinde sabit takvim kullanıldı.
- K1 kodu okunmadı, eksik sembol yok.
