# Kırmızı takım 2: PLAN_BIST.md sayı, tarih ve kural denetimi (06.11.2026)

**Bakış açısı:** Olgu ve kural kontrolü. Plandaki sayılar, tarihler, eşikler ve iddialar iki kaynakla karşılaştırıldı: araştırma ve doğrulama dosyaları ile birincil kaynaklar.

**Birincil kaynaklar** (hepsi varsayılan başlıklarla, 06.11 ~15:00–15:40 TSİ):
- Borsa İstanbul VİOP bülteni: `viop_20261105.csv`. 6.11 dosyası henüz 404.
- Borsa İstanbul Pay Piyasası "Piyasa İşleyişi" sayfası ve VİOP "Emirler" sayfası.
- VİOP Prosedürü PDF'i (§7, Ek-3).
- KAP: `api/member/filter`, `api/disclosure/members/byCriteria` ve bildirim sayfaları.
- İş Yatırım ChartData: SAHOL, AKBNK, ENJSA, AKCNS, KCHOL, XU100, XU030 ve KCHOL sepeti.

İndirilen dosyalar ve betikler: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/kirmizi2/`.

**Ciddiyet ölçeği:**
- **KRİTİK:** Kural uygulandığında emir reddedilir ya da yanlış işlem yapılır.
- **ÖNEMLİ:** Yanlış olgu ya da beklenti; karar veya takvim değişir.
- **KÜÇÜK:** Tutarsızlık, yuvarlama ya da etiket hatası.

---

## A. Hatalar ve düzeltmeler

### 1. KRİTİK: Kapanış seansının işleyişi yanlış tarif edilmiş. Planın limit fiyatları kapanış seansında kabul edilmez.

**Plandaki yeri:**
- §3 "Ortak kurallar": emir toplama "18:00'dan sonra ~18:07'ye kadar".
- §6.2: "Tek bir 10 dakikalık pencere".
- Limitler: K3/K3b alışta önceki kapanış × 1,04; K4 alışta t kapanışı × 1,06; bütün spot çıkışlarda önceki kapanış × 0,94.

**Birincil kaynak:** Borsa İstanbul, Pay Piyasası Piyasa İşleyişi, "Kapanış Seansı" ve "Kapanış Seansında Fiyat Marjı Uygulaması".

Kapanış seansının aşamaları:

| Aşama | Saat |
|---|---|
| Emir toplama | 18:01–18:05 (4 dk) |
| Fiyat belirleme ve kapanış seansı işlemleri | 18:05–18:07 |
| Kapanış fiyatından işlemler | 18:08–18:10 |

- Kapanış seansında girilen emrin fiyatı, son normal işlem fiyatından ±%3'ten fazla farklı olamaz. Üst sınır aşağı, alt sınır yukarı fiyat adımına yuvarlanır. Günlük ±limit de aşılamaz.
- Sürekli işlemde gerçekleşmeyen günlük emirler kapanış seansına aktarılır. Pay Piyasası'nda tarihli emir kullanılmıyor, borsa düzeyinde stop emri de yok.

**Sonuç:**
- Fiyat gün içinde yatay kaldığında ×1,04, ×1,06 ve ×0,94 limitlerinin hepsi ±%3 bandının dışında kalır ve emir reddedilir.
- Stop günü çıkış emri reddedilirse pozisyon taşınmış olur.
- 18:05'ten sonra girilen emir müzayedeye girmez.

**Düzeltme** (§3, §6.2, K3, K3b, K4, K5 ve E1'deki bütün kapanış seansı emirleri için tek kural):
- Emir 18:01–18:05 arasında, son işlem fiyatı P_son görülerek girilir.
- Alış limiti = min(plan limiti; P_son × 1,03, aşağı fiyat adımına yuvarlanmış).
- Satış limiti = max(plan tabanı; P_son × 0,97, yukarı fiyat adımına yuvarlanmış).
- 18:05 kaçırılırsa 18:08–18:10 aşamasında kapanış fiyatından emir girilir ve günlüğe "geç" diye yazılır.
- Plan limiti P_son × 1,03'ün altındaysa (gün içi sıçrama) plan limiti kullanılır. Dolmazsa ertesi gün aynı kural uygulanır.
- §6.1'deki 5. soru şöyle değiştirilir: "Kapanış seansına özel emir ya da dengeleyici (imbalance) emir sunuyor musunuz?" Borsa düzeyinde dengeleyici emir tipi var.

### 2. ÖNEMLİ: K5 AKCNS bilgisi yanlış ve eksik. Teklif kapandı; hak sahipliği 18.06.2026'ya bağlı.

**Plandaki yeri:**
- §3 K5 "Bugün": fiyat 260,25 TL ile USD karşılığından yüksek olanı; "açık olduğu teyit edilmedi".
- K5 kural 2: "AKCNS metninde tarih kaydı yok".

**Birincil kaynak:** KAP 1666313 (21.09), 1666829 (22.09) ve 1673963 (06.10.2026).
- Teklif 23.09.2026 09:00'da başladı, 06.10.2026 14:00'te bitti. Aracı TEB Yatırım.
- Teklif fiyatı **274,24 TL**. Bu, 22.09 TCMB kuruyla 5,627434 USD'nin karşılığı; 260,25 TL değil.
- **"Pay Alım Teklifinden Yararlanabilecek Pay Sahiplerinin … Belirlenmesinde Esas Alınan Tarih: 18.06.2026."** Liste MKK tarafından hazırlandı (PAT Tebliği md. 11/4). O tarihten sonra yapılan satışlar LIFO esasıyla düşüldü.
- 1.062 pay sahibi, 29,49 mn TL nominal pay sattı. Bu, sermayenin ~%15,4'ü. Heidelberg'in payı ~%94,8'e çıktı (hesap: 79,43 + 15,4).

**Sonuç:**
- AKCNS'deki 184 TL ile 274 TL arasındaki fark hiçbir zaman yeni alıcıya açık değildi.
- Planın "hak sahipliği" uyarısı bu örnekte tam olarak gerçekleşti.

**Düzeltme:**
- K5 "Bugün" şöyle yazılır: "AKCNS: teklif 06.10.2026'da kapandı (KAP 1673963); hak sahipliği 18.06.2026 kaydına bağlıydı → kalıcı olarak çıkar."
- Kural 2'deki "AKCNS metninde tarih kaydı yok" ifadesi silinir.
- Zorunlu tekliflerde kayıt tarihi kuralı varsayılan kabul edilir. Bilgi formunda "Esas Alınan Tarih" alanı, sonradan alınan payı kapsamıyorsa işlem yok.
- K5 beklentisi: zorunlu teklifler için ~0; yalnız gönüllü teklif ve satma hakkı kalır. Katkı merkezi +0,1'den ~0'a (0…+0,2) iner. §9.1 de buna göre düzeltilir.

### 3. ÖNEMLİ: K4 adaylarında bilanço takvimi ters. AHGAZ ve ENERY'de ihraççı geri alımı var.

**Plandaki yeri:** §3.10 A1, §4.4 (ENJSA notu), §7.2 (Salı satırı).

**Birincil kaynak:** KAP, 01.10–06.11.2026 bildirimleri.
- **ENJSA** 3Ç finansal raporunu **02.11.2026'da** yayımladı (KAP 1691179; faaliyet raporu 1691180). Bu yüzden ENJSA'ya 9.11 bilanço kısıtı uygulanmaz.
- **AHGAZ, ENERY ve RYSAS**'ın KAP'ta 3Ç finansal raporu yok. Yasal son gün 9.11, yani üçü de büyük olasılıkla Pazartesi akşamı açıklayacak. A1 listesinde üçü de yok.
- AHGAZ ve ENERY, 17.09.2026 YK kararıyla ve her biri azami 2 mlr TL'lik programla **neredeyse her gün geri alım yapıyor** (son bildirimler 1693367 ve 1693368, 05.11). İki şirket aynı Ahlatcı bildirimlerini paylaşıyor (Ahlatcı Altın, Dünya Katılım halka arzı). Yani tek grup. RS 97–98 liderliğinin bir kısmı ihraççı alımıyla destekleniyor.

**Düzeltme:**
- A1'den ENJSA çıkarılır; AHGAZ, ENERY ve RYSAS eklenir.
- §4.4'teki ENJSA notu şöyle olur: "Bilanço 02.11'de açıklandı. Pazartesi kapanış sinyali Salı kapanışında girişe uygun."
- AHGAZ, ENERY ve RYSAS'ta ilk karar Salı 10.11 kapanışında verilir; giriş A2 nedeniyle Perşembe yapılır.
- AHGAZ ile ENERY tek isim sayılır. "Aktif ihraççı geri alımı" bayrağı eklenir ([OA] §2.3: VİOP dışı geri alımda kenar yok).
- GEÇİŞ'teki "AHGAZ 98 > ENERY 97" seçim kuralı kaldırılır.

### 4. ÖNEMLİ: VİOP bülteni ve uzlaşma saatleri planın rutin saatleriyle uyuşmuyor.

**Plandaki yeri:** §6.3 m.2 (18:15–18:45'te [BÜL] indirilir), §7.1 m.2 ("~18:30 sonrası viop_20261106.csv").

**Birincil kaynak:**
- VİOP Prosedürü Ek-3: akşam seansında olmayan sözleşmelerde uzlaşma fiyatı ilanı 18:55 ve sonrası; akşam seansındakilerde 18:45 ve sonrası.
- Bülten CSV'sinin `Last-Modified` saatleri: 02.11 20:35, 03.11 20:49, 04.11 20:28, 05.11 20:44 TSİ.

**Düzeltme:** Rutin iki adıma bölünür.
1. 18:15'te spot tarama, K1/K2 z-skorları ve K4 tetikleri.
2. 20:45'ten sonra [BÜL] indirilir; ima oranlar ve K6/§1.5 kapıları hesaplanır.

VİOP kararları zaten ertesi gün uygulanıyor. Cuma 6.11 kontrol listesinde de bülten için "≥20:45" yazılır.

### 5. ÖNEMLİ: K1 komisyon kapısı test maliyetinin üç katına izin veriyor.

**Plandaki yeri:** K1 kapı 2 ("yön başına ≤ 15 bps"), §6.4.

**Kontrol:** [VB] #25'in maliyet varsayımı bütün çift için gidiş-dönüş 20 bps. İki bacak ve iki yönde 15 bps ise toplam 60 bps eder. Bu durumda net beklenti +80…+180 bps değil, ~+40…+140 bps olur.

**Düzeltme** (iki seçenekten biri):
- Kapı "bacak ve yön başına ≤ 5 bps (BSMV ve borsa payı dahil)" yapılır.
- Ya da 15 bps korunur ve K1 beklentisi +40…+140 bps, katkısı merkez +0,25 puana (0…+0,6) indirilir.

### 6. ÖNEMLİ: K3 beklentisinin etiketi yanlış.

**Plandaki yeri:** §8.3 K3 "+%0,5…+%0,7 (piyasa düzeltmeli)", §9.1 K3 +0,5.

**Kontrol:** [BS] §5.3 ve [VB] #26'daki +%1,2 **ham** getiri; piyasaya göre düzeltilmemiş. Hesap:
- XU100'ün ~%20/yıllık drifti 5 günde ~%0,35 eder. Bunu ve 30 bps maliyeti düşünce fazla getiri ~+%0,55 kalır.
- %30 iskontoyla ~+%0,4 olur.
- Bugünkü engel 7 takvim gününde ≈ %0,65–0,7 tutar. R_fazla ancak piyasanın engel kadar kazandığı varsayımıyla pozitif kalır.

**Düzeltme:**
- Etiket "ham getiriden; piyasa ≈ engel varsayımıyla" olarak değiştirilir.
- Olay başı +%0,2…+%0,5; katkı merkez +0,3 (0…+0,8).
- Hedge'li sürüm (≥ 5 mn TL) bu varsayıma bağlı değildir; tercih edilir.

### 7. KÜÇÜK: XU030 Aralık bileşik oranı yanlış.

- **Yeri:** §1.2 "%29,3 / %32,2".
- **Kontrol:** (14.734/14.101)^(365/56) − 1 = **%33,1**. [VP] T12'deki %32,2 de yanlış. Basit oran (%29,3) ve kararlar değişmiyor.

### 8. KÜÇÜK: Vadeli finansman avantajı yasaklanan kontratla hesaplanmış.

- **Yeri:** §1.5, "bankalarda ~4,6–7,4 puan".
- **Kontrol:** Bu rakamlar Kasım kontratından; plan Kasım'ı yeni pozisyonda yasaklıyor. 5.11 Aralık uzlaşmasıyla ima oranlar: GARAN %26,9, AKBNK %30,6, YKBNK %30,7, KCHOL %30,0, SAHOL %32,1, ENJSA %9,8.
- Mevduat netine (%32,6) göre yalnız GARAN 3 puan eşiğini geçiyor (5,7). AKBNK ve YKBNK ~1,9–2,0 ile geçmiyor.
- Koşul 3'ü (açık pozisyon ≥ 20.000 kontrat, hacim ≥ 100 mn TL) hiçbir Aralık pay kontratı sağlamıyor. Örnek: AKBNK Aralık açık pozisyonu 16.098, hacmi 118 mn TL.
- **Düzeltme:** Rakamlar yukarıdakilerle değiştirilir. Koşul 3 "kullanılacak kontratın" verisi olarak yazılır.

### 9. KÜÇÜK: K6 boyutu kendi sınırını aşıyor.

- **Yeri:** K6, 1 mn TL'de 2 kontrat.
- **Kontrol:** 2 × 52,3 bin TL, nominalin 0,105 katı eder; sınır ≤ 0,10x.
- **Düzeltme:** Kontrat sayısı floor ile hesaplanır: 1 / 9 / 38 kontrat.

### 10. KÜÇÜK: Kredili işlem esnekliği "3/3 uzatıldı" değil.

- **Yeri:** A4.
- **Kontrol:** [VB] #7'deki karar zinciri 2026/60 (ilk tedbir), 2026/68 ve 2026/78. Yani iki uzatma var.
- **Düzeltme:** "2/2 uzatıldı."

### 11. KÜÇÜK: K2 sinyalinin "20.10'dan beri kalıcı" olduğu yanlış.

- **Kontrol:** Kendi yeniden hesabım: günlük eşit ağırlıklı sepet, 60 gün, z 5.11'de 2,25. z 22.10–02.11 arasında 2'nin altına indi (1,21–1,93). 03.11'de 2,03 ile yeniden kesti.
- Planın kuralına göre bu yeni bir kesişimdi (giriş 04.11 olurdu). Pazartesi kararı değişmiyor (bayat sinyal, giriş yok), ama gerekçe yanlış.
- **Düzeltme:** Günlükte kesişim tarihi z serisiyle tutulur.

### 12. KÜÇÜK: Takvim ve vade düzeltmeleri.

- **(a) Mevduat 4. dilim:** 30.11 + 32 gün = **01.01.2027**, resmî tatil. Dilim 31 ya da 35 gün vadeli açılır.
- **(b) A7 bitiş tarihi:** Mart 2027'de Ramazan Bayramı tatili var (yaklaşık 9–12.03; takvimden teyit edilmeli). 63 işlem günü 10.03'te değil, ~15.03'te biter.
- **(c) §0 m.7 ile A6 çelişiyor:** §0 m.7'de "yüksek verimli temettüde 10 gün", A6'da 5 gün yazıyor ([OB] §8). §0 m.7 "5 gün" yapılır.

### 13. KÜÇÜK: İç tutarlılık sorunları.

- **(a) Stres örneği:** §5'teki "her şey dolu" örneğinin açık stop riski 0,6 + 0,84 + 0,5 + 1,0 = **%2,94**. Bu, %2,5 tavanını aşıyor. Örnekten K5 çıkarılır ya da "öncelik kuralı K4'ü keser" diye not düşülür.
- **(b) Çekirdek oranı:** §2.3'te "çekirdek ≥ %85" yazıyor, ama §1.3 KAPALI'da %15 spot ve %15 VİOP teminatına izin veriyor (çekirdek %70'e kadar iner). Biri seçilir.
- **(c) Halka arz sayısı:** §3.11'de "50–52/53", K8'de ve [VB] #11'de "~50–51/53". Rakam 50–51/53 yapılır.
- **(d) A9'daki %8 kuralı:** [VP] T7'ye göre %8 sınırı fon başına geçerli. Kural ihtiyat filtresi olarak kalabilir, ama etiketi [TE] olmalı.
- **(e) Ek A awk komutu:** 18. sütun (işlem hacmi, TL) eklenir. §1.5 ve K1/K4'teki hacim kuralları bu sütuna bakıyor.
- **(f) M4 tanımı:** [TM] §5.1'deki tetik "CDS < 230 **ve düşüyor**". Plana bu ek konur.

### 14. KÜÇÜK: VİOP emir tipleri soru değil, birincil kaynakta belli.

**Birincil kaynak:** Borsa İstanbul VİOP "Emirler" sayfası.
- Geçerlilik türleri: GUN, IKG, TAR, GIE, KIE.
- Emir yöntemleri: Limit, Piyasadan Limite, **Şarta Bağlı (SAR)**, **Strateji (STJ)**.
- Piyasa emri 1.3.2021'den beri yasak.

**Akşam seansı** (VİOP Prosedürü §7): Yalnız BIST30, Likit Banka, Banka Dışı Likit 10 ve Sürdürülebilirlik 25 endeks vadelileri ile metal vadelileri işlem görür. Pay ve USDTRY vadelileri akşam seansında yok; plan bu konuda doğru.

**Düzeltme:**
- §6.1'deki 6. ve 7. sorular "aracı kurum SAR ve STJ emirlerini iletiyor mu?" olarak değiştirilir.
- §6.2'deki akşam seansı istisnasına not düşülür: yalnız K7'nin F_XU030 yarısı akşam seansında azaltılabilir.

### 15. KÜÇÜK: K1 tetik seviyeleri yaklaşık.

- **Kontrol:** z bugünü de içeren 60 günlük pencereyle tam çözüldü:
  - SAHOL: 91,10 / 82,35 (planda 90,85 / 82,52).
  - AKBNK: 62,78 / 69,44 (planda 62,94 / 69,30).
- **Düzeltme:** Alarmlar tam seviyelerle kurulur ya da "yaklaşık ±%0,3" notu düşülür.

---

## B. Doğrulanan kalemler (değişiklik gerekmez)

**VİOP (5.11 bülteni):**
- F_XU0301226 uzlaşma 14.734, kapanış 14.745; XU030 14.101; 56 gün; basit oran %29,3.
- Çarpanlar: XU030 = 10 TL × endeks (hacim/adet ≈ 149 bin TL/kontrat); pay vadelisi 100 pay; USDTRY 1.000 $.
- F_USDTRY1226 52,296; F_ENJSA1126 −%10,4.
- Kasım ima oranları: GARAN %25,2, AKBNK %26,3, YKBNK %28,0.
- Aralık hacmi: SAHOL 22,4 mn, AKBNK 117,6 mn, KCHOL 30,0 mn TL.
- Bülten sütun numaraları (2, 10, 16, 20, 21, 22) doğru.

**İş Yatırım verisi:**
- XU100 11.333; SMA200 13.572 (−%16,5); SMA50 12.691 (−%10,7); 12 ay +%3,84.
- XU100(28.11.2025) = 10.898,70; TSMOM eşikleri ~14.960 / ~15.860.
- XBANK SMA200 16.955.
- K1 z = −0,72 (SAHOL 85,10, AKBNK 67,20).
- ENJSA'nın 52 haftalık zirvesi 127,00, 17.04.2026'da.

**Tarama tetikleri ve şablon:**
- Tetikler: AHGAZ 48,70, ENERY 14,60, RYSAS 30,28, KCHOL 225,50, BIMAS 433,75, TUPRS 409,90, GARAN 158,59.
- Şablon puanları ve SMA50 değerleri (KCHOL 211,11) tutuyor. Taramadaki `zirve52`, ertesi günün B52 eşiğine eşit.

**Test ve doğrulama sonuçları:**
- [BT] §5.1–5.2: 2.073 işlem, +%5,3, t 5,1; S5 +%5,7, t 5,4; MaxDD −%27 / −%45 / −%61; en fazla 120 gün.
- [HK] n = 56, −0,22R; [SE] %26.
- [OB] A5, A6, E6 ve K3b rakamları; [OA] 6/6 döngü, −%6,3, t −4,2, n = 24.
- [VC] #18 rezerv, #19 carry; [KO] §4.2 brüt rezerv < 160; [TM] M2 "2 ay üst üste".
- [HA] 10–27 bin TL; [VP] T6 ve T10 listeleri.

**Hesaplar:**
- Mevduat: net basit %32,6, bileşik %37,9; 56 günde %5,06.
- Stres örneği: ~47 bin TL.
- Ekleme hesabı: 0,1475.
- Kontrat formülü ve 1 / 5 / 20 mn TL tabloları.

---

## C. Kaynak listesi (birincil)

- `https://www.borsaistanbul.com/data/vadeli/viop_20261105.csv` (ve 02–04.11 başlık saatleri)
- `https://borsaistanbul.com/piyasalar/pay-piyasasi/piyasa-isleyisi` (kapanış seansı, ±%3, emir tipleri)
- `https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/emirler`
- `https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf` (§7, Ek-3)
- KAP bildirimleri: 1664883, 1666313, 1666829, 1673963 (AKCNS); 1691179 (ENJSA 3Ç); 1693367 (AHGAZ geri alım); 1693368 (ENERY geri alım)
- SPK bülteni 2026/59 (AKCNS onayı; yerel kopya `verif_bist/spk/2026-59.txt`)
