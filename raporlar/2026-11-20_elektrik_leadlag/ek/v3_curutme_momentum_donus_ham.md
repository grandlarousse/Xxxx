araç: 19/40

## Özet

**Hüküm: S1 ÇÜRÜTÜLDÜ** (nakitten girip 3 gün taşınan bağımsız alım kuralı olarak; yalnız zamanlama süzgeci olarak şartlı kullanılabilir). **S2 ÇÜRÜTÜLDÜ.**

İstatistiksel "devam" etkisi gerçek görünüyor, çürüyen şey ekonomik iddia ("temel maliyet sonrası +37…+40"):

1. **Kıyas şişkin, asıl rakip nakit.** 2023 sonrasında sepetin sıradan 3 günü −3 bps, yani `per` ≈ ham getiri. XU030 vadeli bazından zımni TL faizi (alt sınır) %27–37; 3 gün ≈ 32–44 bps. Ham − temel maliyet (30) − faiz: S1 +6, S2 −4 bps; muhafazakâr maliyetle −19 / −29; kasada −18 / −6.
2. **Kümelenme (S1).** Havuzda 174 sinyal günü = 40 dalga, 18'i artıda; en iyi 3 dalga kazancın %83'ü, onlar hariç +19 bps. Dalga boyu taşıyan için gidiş-dönüş medyanı −44, kazanan %42. Trend denetimli regresyonda S1 +45 (t 1,2), kasada +20 (t 0,4).
3. **S2 zayıf.** Zirve olmayan z ≥ 1 günleri +35 (t 0,9); eşik 1,5'te +27 (OOS-1 −3); nakde göre dört yılın üçü ekside.
4. **Yıllık (nakde göre, puan; 2023/24/25/26):** S1 +16,1 / −1,5 / +2,8 / −7,0; S2 −3,5 / −11,0 / +11,4 / −5,2.
5. **Kazanç sağ kuyruktan:** sonraki 3 günde tavan yapan işlemler (%5,7) toplam kazancın %91'i; işlem medyanı +35 / +21. AKSEN −4, ENJSA −10.

**Çürütemediklerim:**
- Rejim yapaylığı değil. "Aynı ay" kıyası eksi (S1 −52) ama mekanik yanlı: karıştırılmış dünyada −109; düzeltilmiş +67. β-korumalı S1 +46 (t 2,0), S2 +63 (t 2,5).
- Yalnız sığ hisselerde değil: likit üçte birlik +66 / +64.
- Dolum: t+1 açılışından girişte +64 / +54; tavana yakınlar önemsiz.
- 17:50 kararı: yakalama %96 / %90.
- Parametre sivri değil: pencere 10–60'ta h3 +78…+96.

Etki sektöre özgü de değil: XUSIN +72 (t 3,0), XU030 −5.

**Dürüst beklenti:**
- S1, 3 günlük tek işlem (yılda ~21): ham ortalama +73, medyan +62, kazanan %59; maliyet ve faiz sonrası ≈ 0–10 bps. En kötü 3 gün −%8,9, en kötü dalga −%5,3.
- S1 yıllık net temel +%23,6 / +8,9 / +13,3 / +0,5; nakde göre −7 ile +16 puan; ralli yoksa sıfır dolayı.
- S2: işlem başına ham +50 (t 1,5); en kötü 3 gün −%10,4.

**Dosyalar**
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v3_curutme_momentum/run.sh
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v3_curutme_momentum/v3.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v3_curutme_momentum.csv (856 satır)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v3_curutme_momentum.md (692 kelime)

## İddia defteri

Kaynak hepsinde `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v3_curutme_momentum.csv`; ikinci sütun `saldiri` etiketi. Havuz = 2023-01 → 2026-11.

iddia | saldiri etiketi | sayı | güven
---|---|---|---
elib rakamları birebir üretildi | 0_yeniden | S1 havuz +82,6 (t 2,75); S2 +70,3 (t 2,19) | yüksek
Bağımsız hesap (px.c, kilit kaydırmasız) | 0_yeniden | S1 +75 (t 2,5); S2 +63 (t 2,0) | yüksek
Ham getiri kasada zayıf | 0_yeniden | S1 +48 (t 1,4); S2 +59 (t 1,4) | yüksek
±60 gün merkezli kıyas (bütün günler) | 1_kiyas | S1 +41 (t 1,4); S2 +43 (t 1,4) | yüksek
Aynı ay kıyası eksi ama mekanik yanlı | 1_kiyas, 1_yanlilik | S1 −52 (t −1,8); karıştırılmış dünya −109; düzeltilmiş +67 (p 0,067); S2 düzeltilmiş +73 (p 0,003) | orta
β·XU100 korumalı | 1_kiyas | S1 +46 (t 2,0); S2 +63 (t 2,5) | yüksek
Trend denetimli regresyon | 1_rejim | S1 havuz +45 (t 1,2), kasa +20 (t 0,4); S2 +69 (t 2,2), kasa +81 (t 1,9) | orta
Zirveye ≤ %2 yakın ama zirve değil | 1_rejim | −4 (t −0,1) | yüksek
BIST geneli, orta-küçük hisse olgusu | 1_genel | XUSIN +72 (t 3,0); XUTUM +49 (t 2,2); XU030 −5 | yüksek
S2'nin zirve dışı günleri zayıf | 1_ortusme | yalnız z ≥ 1: +35 (t 0,9), OOS-1 +9; ikisi birden +121 (t 2,4) | yüksek
S1 dalga yoğunlaşması (boşluk > 3 gün) | 2_kume | 40 dalga, 18 artı; en iyi 3 payı %83; hariç +19 bps | yüksek
S1 dalga yoğunlaşması, kasa | 2_kume | 15 dalga, 9 artı; en iyi 3 payı %106; hariç −9 bps | yüksek
S2 dalga yoğunlaşması | 2_kume | 83 dalga, 54 artı; en iyi 3 payı %64; hariç +26 bps | yüksek
Blok önyükleme (10 gün) %90 aralık | 2_kume | S1 [+22, +128]; S2 [+22, +113]; 36 bps altı olasılığı %11 / %13 | orta
Yalnız dalganın ilk günü | 2_kume | S1 +65 (t 1,7); 10 gün aradan sonra +28 (t 0,6); S2 +71 (t 1,8) | yüksek
Likidite üçte birlikleri (likit / orta / sığ) | 3_kimde | S1 +66 / +70 / +95; S2 +64 / +79 / +56 | yüksek
En likit 10 ve 5 hisse | 3_kimde | S1 +53 (t 1,6), +41 (t 1,0); S2 +57, +47 | yüksek
VİOP üçlüsü hisse bazında (S1) | v3.py çıktısı (CSV'de yok) | AKSEN −4, ENJSA −10, ODAS +56 | orta
Tavan yapan işlemlerin payı | 3_kimde | işlemlerin %5,7'si, per kazancının %91'i (S2 %6,6 / %106); işlem medyanı +35 / +21 | orta
Fiyat ≥ 5 TL; çöküş hisseleri hariç | 3_kimde | S1 +78; +64 (t 2,1); S2 +68; +60 | yüksek
Kapanış seansı kapasitesi (%10 kuralı) | 3_kimde | N×min 0,74 milyon TL; en sığ 5 hariç 2,1 milyon TL | orta
Tavana ≤ %1 yakınlar hariç | 4_dolum | S1 +77; S2 +68 (işlemlerin %0,5 / %1,1'i) | yüksek
Gecikmeli giriş | 4_dolum | t+1 açılış S1 +64 (t 2,2), S2 +54 (t 1,8); t+1 kapanış +46 (t 1,4), +50 (t 1,7) | yüksek
Çıkışta taban kilidi | 4_dolum | S1 %1,17 (66 işlem, ort. −1508 bps); S2 %0,52 | yüksek
Maliyet (havuz) | 5_maliyet | temel 30, muhafazakâr 55 bps; per net S1 +40 / +15, S2 +37 / +12 | yüksek
Zımni TL faizi (XU030 vadeli bazı) | 5_tasima | %30 / %37 / %33 / %27; 3 gün 36 / 44 / 39 / 32 bps | orta
Ham − temel maliyet − faiz | 5_maliyet | S1 +6 (kasa −18); S2 −4 (kasa −6) | orta
Yıllık strateji net temel (2023/24/25/26) | 5_yillik | S1 +%23,6 / +8,9 / +13,3 / +0,5; S2 +7,5 / +1,4 / +23,9 / +4,4 | orta
Nakde göre fazla (puan) | 5_yillik | S1 +16,1 / −1,5 / +2,8 / −7,0; S2 −3,5 / −11,0 / +11,4 / −5,2 | orta
17:50 vekili (havuz) | 6_karar | S1 yakalama %96, yanlış %5, +76 (t 2,5); S2 %90 / %6, +69 (t 2,1) | yüksek

## açık kalanlar

- TL faizi yalnız XU030 vadeli bazından türetildi (alt sınır); para piyasası fonu ya da mevduat getirisiyle doğrulanmadı. Gerçek oran daha yüksekse S1 de net ekside kalır; hüküm bu varsayıma duyarlı.
- Ek defter satırları (yer sınırı nedeniyle tabloya girmedi, CSV'de var): parametre ızgarası (7_param: S1 h3 pencere 10–60'ta +78…+96; S2 eşik 1,25 → +60, 1,5 → +27), aşağı yön (8_asagi: z ≤ −1 ertesi gün havuz −48, t −2,2; IS −22; OOS-1 −2; kasa −109), dalga düzeyi kâr dağılımı (5_yillik: S1 40 gidiş-dönüş, medyan −44, kazanan %42).
- "S1 ve S2 aynı gün" alt kümesi (+121, t 2,4) ve "XU100 z ≥ 1, XELKT z < 1 → sepet" (+114, t 2,4) sonradan bakılan kesitlerdir; dondurulmuş kural değil, sınanmadı.
- Yıllık benzetim basitleştirilmiş: dalga başına tek gidiş-dönüş maliyeti, dalga içinde yeniden dengeleme ve taban kilidi yok.
- Kapanış seansı hacmi A7'nin dolaylı tahminine dayanıyor (2023-12 → 2025-06); kasa döneminde yeniden ölçülmedi.
- Hayatta kalma yanlılığı (bugünkü XELKT üyeleri) giderilmedi.
- Tavan yapan işlemlerin ayıklanması geriye dönük tanıdır, uygulanabilir süzgeç değil.
- XBANK serisinde IS'te kırık var (−896 bps); genel momentum karşılaştırmasından çıkarıldı.