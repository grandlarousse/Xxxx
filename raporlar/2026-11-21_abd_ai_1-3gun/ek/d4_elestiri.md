araç: 18/20

# D4 — Eleştiri (tek tur)

Ek hesaplar `veri/sonuc/B1_islemler.csv` ve `veri/gunluk` üzerinden. "Günlük t" = aynı günün altı ETF'i tek gözlem.

## İtirazlar (önem sırasıyla)

**1. Boyut tablosu kuralın çalıştığı rejimi dışarıda bırakıyor ve toplanabilir sanılıyor.**
Kanıt: tablo "2023'ten beri en kötü gün"e dayanıyor (risk_tablosu.csv). 2010'dan beri en kötü gün: QQQ −%12,0, SMH −%14,4, TQQQ −%34,5 (16.03.2020), SOXL −%38,7. En kötü iki gün: −%13,1 / −%15,5 / −%36,7 / −%46,3. Dört sınır birlikte kullanılırsa 20 Kasım gibi bir gün sermayenin %10,5'ini götürür.
Düzeltme: sınırlar iki günlük en kötüye göre: QQQ %23, SMH %19, TQQQ %8, SOXL %6. Cümle: "Bu sınırlar toplam içindir; dört araç tek bahistir, aynı anda yalnız birini kullan."

**2. 20 Kasım bölümü pazartesi açılışta alım çağrısı gibi okunuyor.**
Kanıt: 1.6 ("kural açıktı") ve 5. bölüm sonu ("dörtte üçü açılıştan sonra"). Açılış girişi önceden kayıtlı değil (PROTOKOL 1.1, ikincil sütun), t'si yok. VIX'in 30'u ilk aştığı ve 35 üstü kapandığı gün tarihte yalnız 5. SMH ≤ −%8 sonrası 8 olayın 4'ü Mart 2020, biri −%7,6.
Cümle: "Cuma sinyali kaçtı. Pazartesi açılışta almak bu raporda sınanmış bir kural değildir, önerilmez. Pazartesi yapılacak tek şey kapanışa 10 dakika kala koşullara yeniden bakmaktır."

**3. Kazanç VIX 35 üstünden geliyor; "30" sınırı ve "20–30 isteğe bağlı" satırı yanıltıcı.**
Kanıt: VIX 30–35: 266 işlem, +23 bps, günlük t 0,6. VIX ≥ 35: 179 işlem, 41 gün, 12 dönem, +210, t 3,0. Evren dışı 9 ABD ETF'inde aynı desen: 30–35 −5, ≥ 35 +152. VIX 25–30: +8 (t 0,0) ve örneklemin en kötü işlemi burada (19→20 Kasım, VIX 28,4, SMH −%10,6).
Düzeltme: eşik değişmesin, tablo açılsın: "30–35: +23, şanstan ayırt edilemiyor" ve "35 ve üstü: +210 (41 gün)". "20–30" satırı "işlem yapma" olsun.

**4. "Yaklaşık +%1, 18 dönemin 17'si" olduğundan iyi gösteriyor.**
Kanıt: B1_rejim.csv'de protokolün (10.3) istediği büzülmüş tahmin +56 bps, işlem isabeti %65; rapor ikisini de vermiyor. Evren dışında +59 (günlük t 2,6). Havuzda günlük t 2,7; dönem yeniden örneklemeli %95 aralık +53…+155. 18 dönemin 10'u 1–2 günlük; iki dönem (2011, 2020) işlemlerin yarısı. 2023 sonrası 2 dönem, 23 işlem, +15 bps, isabet %39. PROTOKOL 10.3–10.4: hücrede t verilmez, hücre geçme ölçütü değildir; 4.2'de "t 3,1", 1.2'de "61 testten ayakta kalan" yazıyor.
Cümle: "Tarihsel ortalama +98 bps; temkinli beklenti maliyet öncesi +55–60 bps. Üç işlemden biri zararla kapandı. Bu kural önceden kayıtlı 61 testten biri değil, sonradan öne çıkan bir rejim hücresidir."

**5. Yıllık katkı yazılmamış; kullanıcı büyük boyuta itilir.**
Kanıt: raporun kendi sınırlarıyla stres kuralı yılda yaklaşık: SMH %27 → +%1,3; QQQ %45 → +%2,0; SOXL %8 → +%1,2; SOXL %33 → +%5 (en büyük düşüş −%18). 2011–2026'nın 16 yılından 8'inde hiç sinyal yok.
Cümle: "Bu kural tek başına ciddi kazanç üretmez: önerilen boyutlarla yılda ortalama %1–2, yılların yarısında sıfır işlem."

**6. SOXL sunumu.**
Kanıt: 1.5'te "aynı kural 19 Kasım'da sinyal verdi" yanlış: 19 Kasım VIX 28,44; stres kuralı kapalıydı (5 Kasım +%12,5 de VIX 28,2). Adım 3'teki "%33 pozisyonla %12,8" bütün günler sürümünün sonucu (yılda 31 işlem; d3 §7); %8 sınırının hemen altında durması %33'e özendiriyor. 4.4'teki t'ler PROTOKOL 3.2 ve 5'e aykırı.
Düzeltme: 1.5 → "SOXL'da kuralın bütün günler sürümü 19 Kasım'da (VIX 28) sinyal verdi, ertesi gün −%32." %12,8 cümlesi Adım 3'ten, t'ler 4.4'ten çıksın.

**7. "İkinci gün ekliyor" sağlam değil.**
Kanıt: 2. günün katkısı +48 bps, günlük t 1,4; 18 dönemin 13'ünde artı. İki gün tutunca eksi dönem 1'den 4'e çıkıyor (d3 dönem tablosu).
Cümle: "Varsayılan çıkış ertesi günün kapanışı. İkinci gün ortalamada ekledi ama şanstan ayırt edilemiyor."

**8. Uygulama adımları eksik ya da belirsiz.**
- VIX kapanışı 16:15 ET'de belli olur; ücretsiz kaynaklar 15 dakika gecikmeli; kaynak yazılmamış. Protokol 2.3'ün istediği dünkü VIX sınaması raporda yok; sonucu olumlu: +144 bps (75 gün, t 2,9). Cümle: "VIX dün 30 üstünde kapandıysa koşul tamam; bugün ilk kez aşıyorsa 32'nin altını sayma."
- IBS: "Son fiyatı kapanış say. 0,15 altı net; 0,15–0,25 arasıysa alma."
- "15:30 dörtte üçünü yakaladı" bütün günler içindir (sinyal uyumu %66); stres günlerinde sınanmadı (d3 §4c).
- Limit emir dolmazsa: "Kovalama, o gün işlem yok."
- 27 Kasım ve 24 Aralık'ta giriş 20:55–20:59.
- sinyal.py telefonda çalışmaz; elle tarif gerekli.

**9. Eksik uyarılar.** Toplam kayıp sınırı (öneri: bir dönemde sermayenin %6'sı gidince dur); cuma sinyalinde hafta sonu boşluğu; devre kesici günü çıkamama; stres sinyallerinde SOXL'un on işleminden biri tek günde %12'den fazla kaybetti.

**10. Lead-lag ve kaçınma.** "Hiçbiri geçmedi" protokole göre doğru; Tokyo Electron/ASML sunumu yerinde (eğim q 0,013; alımda karşılığı yok). Bitcoin'de "kovalamak zararlı" fazla: p_perm 0,35, eğim t −1,4, ŞÜPHELİ bayrağı (d2_b2). Cümle: "…ortalama −100 bps; istatistiği zayıf, yalnız alım gerekçesi olmadığını gösterir."

## Sayı denetimi

Kontrol edilen yaklaşık 215 sayı: 1., 2., 4. bölümden 85; 3. bölümün 35 satırı; 13 takvim tarihi; 12 haber sayısı. Takvim ve haberde uyuşmazlık yok.

| Rapor | Kaynak | Dosya |
|---|---|---|
| 1.5: 19 Kasım "aynı kural" | VIX 28,44; stres kuralı kapalı | veri/gunluk/_VIX.csv |
| 4.3: "VIX'in 30'u aştığı 18 dönem" | 21 dönem; 18'inde sinyal | PROTOKOL 10.2 |
| SOXX en kötü gün −%12,2 | −%12,1 (−12,147) | risk_tablosu.csv |
| USD oynaklık %6,4 | %6,3 (6,348) | aynı |
| AMDL oynaklık %11,1 | %11,0 (11,049) | aynı |
| CRDO oynaklık %6,8 | %6,7 (6,748) | aynı |
| (kaynak içi) STRES dönem sayısı 10 | 18 | d3_curutme §5 |

## Ek hesaplar

- Eşik (alfa, günlük t, artı dönem): VIX ≥ 25: +54, 2,2, 24/31. ≥ 30: +98, 2,7, 17/18. ≥ 35: +210, 3,0, 11/12.
- İki gün tutma: +137, artı dönem 14/18.
- Stres işlemlerinde en kötü gün: QQQ −%6,2, SMH −%10,6, TQQQ −%18,3, SOXL −%23,5.
- Kaldıraçlı fon satırları yaklaşık (SOXL'da 79 işlem, raporda 65).

## Okunurluk: en kötü üç yer

4.2 karar tablosu (dört sütun, "alfa, t"); 3.2 hisse tablosu (altı sütun, 24 satır); 4.3 "Dürüst uyarı" paragrafı.
