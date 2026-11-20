araç: 23/40

**Özet (hükümler)**

- **S3 (XU030 gecikmesi): ÇÜRÜTÜLDÜ (öneri olarak; biçimsel sınıf "güç yetersiz").** Havuzdaki +157 (t 3,0) birebir yinelendi, ama üç yerden zayıf:
  - **Kuyruk:** en iyi 2 gün (2023-05-26 ve 2024-04-04, seçim haftaları) çıkınca +106 (t 2,7), 5 gün çıkınca +70 (t 1,9), 10 gün çıkınca +25.
  - **Gecikme değil momentum:** aynı günlerde XU030'un kendisi de sürüyor. β korumalı üçlü havuzda +66 (t 1,85), kasada +11 (t 0,2). Gecikme koşulunun katkısı kasada −6. 2023+'da koşulsuz "XU030 z ≥ 1" β korumalı +70 (t 2,8); XELKT koşulu bir şey eklemiyor.
  - **Kasa:** +41 (t 0,8); temel maliyet sonrası işlem başına +11, muhafazakâr −14; etkiyi ENJSA taşıyor.
  - **Karar anı:** 17:30'da sinyalin %63'ü görünüyor, 17:50'de 18 sinyalin 16'sı (küçük örnek). Uygulanabilir yol 17:50–17:55'te bakıp kapanış seansına emir vermek.
  - **Vadeli:** 3 günde spotun 48–54 bps gerisinde; spot daha iyi. ODAS'ta bir fiyat adımı 23 bps.
  - **Beklenti:** olay başına brüt +40…+70, yılda ~10 olay; para yatırılacak kural değil.

- **T1 (model): ÇÜRÜTÜLDÜ (öneri olarak). T2 (sade): ŞARTLI KABUL, yalnız seçim süzgeci olarak.**
  - Kasadaki +41 / +38, kütüphanedeki çıkış ertelemesinin taban serilerini kıyasta şişirmesinden. Düz ertesi gün getirisiyle T1 +19, T2 +15.
  - Dört çöküş hissesi çıkınca T1 +13 (t 3,1), T2 +8 (t 1,4); kıyas "son 5 günde tabansız" olunca +7 ve +5 (t ≤ 1,6).
  - İsabet yok: seçilenlerin evren medyanını geçme oranı %50–51. Kazanç tavandan değil, sol kuyruktan kaçınmadan geliyor.
  - T2'nin taşıyıcısı tek koşul: düşük oynaklık (IS +5,4 / OOS-1 +8,0 / kasa +12,2; t 3,2–4,6). "Günün güçlüsü" koşulu tek başına etkisiz. TradingView vekiliyle de çalışıyor.
  - Beklenti günde +5…+12 bps; al-sat kuralı değil.

- **T + S birleşimi (doğrulanmadı):** IS'te ters işaret (−41, t −2,5); desteklenmiyor.

- **K1: ÇÜRÜTÜLDÜ (bağımsız bulgu olarak).** Tabanda kapananlar çıkınca −5 / −17 / −3; taban serilerinin gölgesi.

- **K2: ŞARTLI KABUL.**
  - Ana tablodaki −627 hesap yapıntısı; düz getiriyle kasa −270.
  - Tabana değenler çıkıp kıyas temizlenince −17 / −70 / −67; havuz −69 (t −3,6). IS'te yok.
  - Kayıp 2023+'da gün içinde; ertesi sabah açılışta almak kurtarmaz.
  - Pratik kural: "O gün tabana değmiş ya da XELKT endeksinin ≥ 5 puan gerisinde kapanmış hisse kapanışta alınmaz." Kapsam hisse-günlerin %3–5'i.

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v4_curutme_diger.md (699 kelime)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v4_curutme_diger.csv (496 satır; S3 olay listesi içinde)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v4_curutme_diger/run.sh (s3.py, tk.py, common.py, birlestir.py; günlükler out/ altında)

**İddia defteri** (bps; sıra IS / OOS-1 / kasa; D = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag)

iddia | dosya | sayı | güven
--- | --- | --- | ---
S3 yineleme, havuz (elib ve bağımsız kısa kod) | D/kod/v4_curutme_diger/out/s3_log.txt | +156,7 (t 3,01; 45 gün, 39 bağımsız); kısa kod +157,3 | yüksek
S3 en iyi 2 / 3 / 5 / 10 gün hariç | D/ek/v4_curutme_diger.csv | +106 (t 2,68) / +94 (2,44) / +70 (1,93) / +25 (0,73) | yüksek
S3 en iyi iki olay ve o günkü XU030 getirisi | aynı csv, test = "olay" | 2023-05-26: +1349 (XU030 +%3,71); 2024-04-04: +1139 (XU030 +%2,39) | yüksek
S3 yıllar (per, gün ortalaması) | aynı csv | 2023 +173; 2024 +189; 2025 +204; 2026 +50 | yüksek
S3 günlerinde XU030'un kendi 3 günlük getirisi | s3_log.txt | +54 (t 2,6) / +139 (2,5) / +34 (0,8) | yüksek
S3 β korumalı üçlü | s3_log.txt | +29 (t 1,2) / +97 (2,0) / +11 (0,2); havuz +66 (1,85) | yüksek
Gecikme koşulunun katkısı (sektör geride − sektör de güçlü) | s3_log.txt | +61 (t 1,8) / +131 (1,5) / −6 (−0,1) | yüksek
2023+ koşulsuz XU030 z ≥ 1 → üçlü | s3_log.txt | per +98 (t 2,7); β korumalı +70 (t 2,8); IS β korumalı +4 | yüksek
S3 kıyas duyarlılığı | s3_log.txt | merkezli ±60 gün +63 / +205 / +46; aynı ay +50 / +208 / +63 | yüksek
S3 karar anı 17:00, 2023+ | s3_log.txt | yakalama %58; yanlış %32; sonuç +93 (t 1,5) | yüksek
S3 karar anı 17:30, 2023+ | s3_log.txt | 38 sinyalin 24'ü (%63); yanlış %29; sonuç +80 (t 1,3); kaçanlar +193 | orta
S3 karar anı 17:50 (XU030 5 dk verisi 410 gün) | s3_log.txt | 18 sinyalin 16'sı yakalanıyor; 21 sinyalin 5'i yanlış | düşük (küçük örnek)
S3 karar anı 18:00 (sürekli işlem sonu) | s3_log.txt | yakalama %92 (2017–22) / %84 (2023+); yanlış %22 / %7; sonuç +98 / +111 | yüksek
Üçlünün 17:30 → kapanış getirisi, sinyal günleri | s3_log.txt | −0,1 (n 38) | orta
S3 t+1 kapanışından giriş | s3_log.txt | OOS-1 +73 (t 1,2); kasa +47 (0,6); havuz +63 (1,3) | yüksek
Vadeli − spot, aynı olaylar, 3 gün | s3_log.txt | AKSEN −54; ENJSA −48; ODAS −50; taşıma −14…−15 bps/gün | yüksek
ODAS fiyat adımı | s3_log.txt | son fiyat 4,35 TL; bir adım 23 bps (spot ve vadeli) | yüksek
S3 spot temel maliyet (30) sonrası net, işlem başına | s3_log.txt | OOS-1 +191; kasa +11 (muhafazakâr −14) | yüksek
S3 olay sıklığı | s3_log.txt | 2023+ yılda 10,1 bağımsız olay | yüksek
S3 kasa, tek hisse | s3_log.txt | AKSEN +7; ENJSA +102 (t 2,0); ODAS +15 | yüksek
S3 en kötü olaylar (ham 3 gün) | s3_log.txt | üçlü −508, −310, −260; tek hisse −892 (ODAS, 2023-11-27); işlemlerin %36'sı zararda | yüksek
T1 / T2 düz ertesi gün getirisiyle (çıkış ertelemesiz) | D/kod/v4_curutme_diger/out/tk_log.txt | T1 +5,5 / +22,9 / +19,4; T2 +9,2 / +16,3 / +15,3 | yüksek
T1 / T2 kasa, çöküş hisseleri hariç; kıyas "son 5 günde tabansız" | tk_log.txt | T1 +13,3 (t 3,1) ve +6,7 (1,6); T2 +8,3 (1,4) ve +5,2 (0,9) | yüksek
Seçilenlerin evren medyanını geçme oranı (havuz) | tk_log.txt | T1 %51,1; T2 %49,6 | yüksek
T2 seçilenlerinde ertesi gün tavan / taban oranı (havuz) | tk_log.txt | tavan %1,4 (evren %1,9); taban %0,2 (evren %1,2) | yüksek
T2 sadeleştirme | tk_log.txt | yalnız sakin yarı +5,4 / +8,0 / +12,2 (t 3,2–4,6); yalnız üst üçte bir +3 / +4 / +4; TradingView vekili +7,7 / +10,5 / +17,2 | yüksek
S1 günü T2 seçilenleri − sepet, 3 gün (DOĞRULANMADI) | tk_log.txt | −41 (t −2,5) / +30 (1,0) / +22 (1,0) | orta
K1 düz; tabanda kapananlar hariç | tk_log.txt | −12,5 / −25,7 / −49; hariç −4,9 (t −0,9) / −16,7 (−3,4) / −3,2 (−0,5) | yüksek
K2 düz; tabana değenler hariç ve temiz kıyas | tk_log.txt | −78 / −119 / −270; temiz −17 (t −0,7) / −70 (−2,7) / −67 (−2,5); havuz −69 (−3,6) | yüksek
Pratik kural: XELKT'den ≥ 5 puan geride ya da tabana değdi | tk_log.txt | kapsam %3,1 / %3,4 / %4,6; ertesi gün −81 / −102 / −236; rastgele alıcıya katkı +1,6 / +3,3 / +10,9 bps | yüksek

## açık kalanlar

- **Ölçüm notu, kapsam dışı:** `elib.fwd_exec` çıkış ertelemesi (tabanda kilitli çıkış 5 güne kadar kayıyor) taban serisindeki hisseleri her gün çok günlük kayıpla sayıyor. T1/T2/K1/K2'nin kasa rakamlarını bu şişirdi. S1/S2 sepet rakamları ve onların 'per' tabanı da aynı hesabı kullanıyor; kasada bunu sınamadım.
- **17:50–17:55 kanıtı ince:** XU030 5 dakikalık verisi yalnız 410 gün (2017, 2018 başı, 2026-05 sonrası). 2023+'da 6 sinyal var.
- **Haber eşlemesi yapılmadı:** yalnız tarihler ve XU030 getirileri listelendi (csv'de 45 olay).
- **Üçlünün saatlik fiyatı** 2023-12 sonrası; "17:30'da al" karşılaştırması 38 olayla.
- **TradingView vekili yaklaşık:** 20 günlük ortalama (yüksek − düşük) / düşük kullandım. Platformun "Oynaklık (ay)" tanımıyla birebir eşleşme doğrulanmadı.
- **Taban bayrakları** 2015-12 öncesinde güvenilmez; K kurallarının IS "tabansız" rakamları buna duyarlı.
- **Vadeli emir defteri** (alış-satış farkı) verisi yok; vadeli karşılaştırması uzlaşma fiyatıyla.
- **K2'nin tabansız kısmı IS'te anlamsız** (t −0,7); yalnız 2023+ bulgusu.
- **Depo durumu:** `git status` bu görevin bazı çıktılarını zaten izlenen dosya olarak gösterdi; başka bir süreç ara sürümleri işlemiş görünüyor. Ben commit yapmadım.