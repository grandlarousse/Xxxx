# ŞEYTAN — 2. Tur (Çapraz Kontrol) | 28.10.2026
Etiketler: [D] kaynakla doğrulandı · [H] benim hesabım · [T] tahmin. Kaynak kodları en altta.

## 1. Özel konular
**1a. MAKRO'nun iddiaları — üçü de DOĞRU:**
- Fed 16.09'da faizi 25 bp artırdı, aralık %3,75–4,00 (oylama 12–0) [F1].
- FOMC toplantısı 27–28 Ekim; karar 28.10, 21:00 TSİ [F2].
- Swap hariç net rezerv: Eylül başında 56 mlr $ [R2], 2.10'da 37,9, 9.10'da 44,2 [R1]. Benim 1. turda yazdığım "37,8" bir hafta eski kalmıştı.

**1b. Kendi rakamlarım (ikinci kaynakla):**
- **2 yıllık TL tahvil — HATA:** ING'nin %39,8'i bileşik getiri. Basit getiri 28.10'da %36,26; son bir ayda −77 bp [T1]. "2Y > politika faizi, yani indirim fiyatlanmıyor" iddiamı geri çekiyorum; eğri politika faizine göre düz.
- **Brent:** 110,5 $ bir dip günüydü. 23.10'da ~117,4 $, 26.10'da ~110 $, 28.10'da 115 $'ın üzerinde [B1][B2]. Petrol riski yazdığımdan büyük.
- **ABD 10 yıllık:** %5,086 (19.10) [U1] ✓.
- **Fon büyüklüğü:** Tasfiyedeki fonlar 31.08'de 1.233 mlr TL, 15.09'da 992 mlr TL, **30.09'da 652 mlr TL** [G1].
  - Bu, piyasa değerinin %4,2'si. Likiditesi sınırlı kısım %58,6 (~334 mlr TL); Tera'nın 3 fonu hariç tutulunca oran %23'e iniyor.
  - Baseline'daki "1,1 trn" büyük olasılıkla tüm kapalı fonların (299 fon) 15.09 toplamı (1.170 mlr TL); yani bayat veri.

**2. SPK kredili işlem esnekliği:** 28.10 itibarıyla 3.10 tarihli 65/1779 sayılı karardan sonra yeni bir karar bulamadım; SPK bülten sayfası 404 verdi [S1].
- **Uzatılmazsa satış ölçeği [T]:** Bakiye 90–110 mlr TL (Ağustos 129), bunun %10–25'i oranı %20–35 arası hesaplarda; %35'e dönmek bu borcun ~%31'i kadar satış ister → **2,8–8,5 mlr TL**, günlük hacmin %3–8'i (Eylül fiili çağrı 1,13 mlr TL).
- Endeks için küçük şok; etkisi küçük hisselerde. Tezimin A halkası zayıfladı.

**3. İşsizlik:** Eylül %8,4 **DOĞRULANDI** (TÜİK, 27.10) [I1].
- İşsiz sayısı +198 bin; genç işsizliği %14,8; atıl işgücü oranı %31,2.
- "+0,5 puan" ifadesi Ağustos'un (%7,8) revize edildiğini gösteriyor.

**4a. MAKRO carry trade'inin kuyruk riski [H]:**
- **Hesap hatası:** MAKRO "+%12 gap" kaybını (S×1,12 − F) = 3.258 TL/kontrat almış; oysa erken şokta vadeli, kalan primle birlikte yeniden fiyatlanır.

| Spot şoku (erken) | Kayıp/kontrat | 6 kontrat | 10 kontrat |
|---|---|---|---|
| +%9 (Mart 2021'deki gün sonu kapanışı gibi) | 4.723 TL | %2,8 | %4,7 |
| +%12 | 6.297 TL | **%3,8** (iddia %2,0) | %6,3 |
| +%15 (kontrollü devalüasyon) | 7.871 TL | %4,7 | %7,9 |

- %11'lik Takasbank teminatı +%11'de tamamen silinir.
- **Beklenen değerin kuyruğa duyarlılığı:** Kuyruk olasılığı %3 olursa EV +170 TL/kontrat; %5 olursa ≈ +11 TL. Yani tezin artısı tamamen "kuyruk olasılığı ≤%3" varsayımına dayanıyor.

**4b. HİSSE GARAN/YKBNK pair'inin bilanço gap riski [H]:** Pozisyon 18 GARAN / 56 YKBNK kontrat. YKBNK 3. çeyrek sonuçları ve Ekim TÜFE aynı gün (3.11) açıklanıyor.

| Senaryo | Kayıp | Sermayeye oranı |
|---|---|---|
| YKBNK tavan (+%10), GARAN yatay | −20,5 bin TL | %2,0 |
| YKBNK +%10, GARAN −%5 (yüksek betaya rotasyon) | −32,6 bin TL | **%3,3** |
| YKBNK iki gün tavan, GARAN −%5 | −55,2 bin TL | %5,5 |

İddia edilen risk %0,97 (stop), kötü senaryo %1,5. Gerçekçi en kötü senaryo bunun 2–3 katı.

## 2. Fikirlere oylar
| Fikir | Olgu / mantık / boyut bulgusu | Oy | Puan |
|---|---|---|---|
| **MAKRO-1** kısa F_USDTRY1226 | Olgular doğru. Gap kaybı ~2 kat eksik hesaplanmış. 10 kontrat, stres sınırını (%2,5) aşıyor | KOŞULLU: 1 mn TL başına ≤4 kontrat (+%12 şokta %2,5); FOMC'den sonra gir | 5 |
| **MAKRO-2** koşullu long XU030 | Kapılar mantıklı. Ancak 22.10 indirim günü −%3 kapandı; makro iyileşme, tasfiye takvimi devam ederken fiyatı taşımayabilir | KOŞULLU (yedek; bear kovasının yerine geçer, ikisi aynı anda açılmaz) | 4 |
| **ENDEKS-1** rallide short | Boyut doğru (%0,45). Stop 1,3 ATR, dar. Carry yokken hedefe önce ulaşma olasılığı %26,5, carry ile ~%42; iddia ettiği %35–45 tutarlı | KOŞULLU: benimle tek kova | 5 |
| **ENDEKS-2** dipte long | Kendi hesabına göre maliyet sonrası EV ≈ 0 | HAYIR | 3 |
| **HİSSE-1** GARAN/YKBNK | GARAN sonucu açıklanmadı; sadece 32,4 mlr TL beklenti var [G2]. Pair aslında "şahin faiz" bahsi, bu yüzden bear kovasıyla pozitif korelasyonlu. Piyasa YKBNK'ye zaten daha yüksek F/K veriyor (5,5 vs 4,5); bu toparlanma beklentisi, hata değil | KOŞULLU: yarım boyut; 3.11 sonrası gir | 5 |
| **HİSSE-2** SAHOL/AKBNK | EV ince, taşıma maliyeti yiyor. SAHOL, tasfiyedeki fonlarda en çok tutulan BIST 30 payı (arz baskısı) | HAYIR | 3 |
| **OPSİYON-1** straddle ≤800 | RV %27'yle adil değer ≈ 1.320 puan [H]; 800'den dolarsa EV güçlü. Asıl risk: ucuz fiyatlar bayat işlem olabilir, dolum zor | EVET (koşullu dolum) | 6 |
| **OPSİYON-2** call spread 14500/15500 | Adil fiyattan EV ≈ 0; tek başına anlamsız | KOŞULLU: yalnızca short'a sigorta olarak | 4 |

## 3. Kendi fikrimin revizyonu
- **ENDEKS ile yakınsama:** Büyük ölçüde **ortak girdi yanlılığı**. İkimiz aynı vadeli fiyatı, aynı Ata dirençlerini ve aynı "baz short'a yarar" argümanını kullandık.
  - Baz bir avantaj değil: 2026 boyunca zımni faiz %24–33'te normal seyretti, BIST 30 ise yılbaşından beri +%14. Yıl boyu tutulan bir short, bazı kazanmasına rağmen kaybederdi.
  - Tek bağımsız kanıt ENDEKS'in tarihsel benzer analizi (63 günlük medyan +%2,9 < taşıma %4,9). O da kırılgan: tasarım değişince 21 günlük getiri +%5,9 çıkıyor.
  - Sonuç: iki fikir tek kova, toplam ≤%1.
- **HİSSE'nin itirazı:** Yönü doğru, büyüklüğü küçük. Fon krizinin sıkışmaya açık 5 hissesi (ASTOR, SASA, GUBRF, TRALT, TRMET) BIST 30 piyasa değerinin ~%6'sı [H, ING; serbest dolaşım ağırlığı değil]; %30'luk bir sıçrama endeksi ~%1,8 oynatır. Asıl sıkışma kaynağı bankalar ve ASELS (~%42); onları da politika haberi tetikler.
- **OPSİYON'un vol bulgusu:** Vol ucuzsa yönlü görüşü vadeli yerine **put spread** ile ifade etmek daha iyi: tanımlı risk, sıkışma ve gap riski yok.
- **Revize fikir:** Al O_XU030E1226P14000 / Sat P13000 (Aralık; Avrupa tipi, nakdi uzlaşmalı).
  - **Fiyat:** Limit ≤200 puan. 27.10 uzlaşma fiyatı 156, σ24 ile adil değer 227 (OPSİYON tablosu).
  - **Getiri profili:** Maks kayıp 2.000 TL, maks kazanç 8.000 TL. Başabaş spot 13.800; endeks yatay kalsa kayıp yalnızca −160 puan.
  - **Olasılık [T, kendi senaryo ağacımdan]:** Kâr %44, maks kâr %30 → EV ≈ +160 puan (+0,8R).
  - **Boyut:** Risk %0,5; 10 mn TL için 25 spread, emir başına ≤50.
  - **Giriş:** Kademeli, spot ≥14.200 rallisinde. **Çıkış:** spread ≥700 puanda kâr al; en geç 24.12.
  - **Yanlışlama:** Değişmedi.
  - **Yedek plan:** Opsiyonda dolum olmazsa vadeli short, yarım boyutla.
- **Güven: 5/10.**

## 4. Komite portföyü
Sıralama, kova riskleri (stop bazlı) ve gerekçeler:
1. **OPSİYON-1 straddle** — %0,8 (yalnız ≤800 puandan dolarsa). Yönden bağımsız; komitenin yön ayrılığını paraya çevirir.
2. **Bear kovası** — toplam %1,0 (ŞEYTAN put spread %0,5 + ENDEKS rallide short %0,5).
3. **MAKRO-1 carry** — 1 mn TL başına 4 kontrat; stop riski ~%0,33, +%12 streste %2,5. TL şokunda bear kovası kazanır; stres korelasyonu negatif, yani doğal hedge.
4. **HİSSE-1 pair** — %0,5, 3.11 sonrası.

| Kontrol | Sonuç | Sınır |
|---|---|---|
| Toplam stop bazlı risk | ≈ %2,6 | ≤%4 ✓ |
| Ortak stres (BIST −%15, banka −%18, USD/TRY +%8) [H] | Carry −%1,7; straddle ve bear kovası kazanır → net ≈ sıfır veya pozitif | ≤%7 ✓ |

Dışarıda kalanlar:
- ENDEKS-2 ve HİSSE-2: EV ≈ 0.
- MAKRO-2 ve OPSİYON-2: Boğa kapıları açılırsa (TÜFE ≤%2,3, CDS ≤235, yabancı girişi) bear kovasının **yerine** devreye girer.

## Kaynaklar
F1 https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm · F2 https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm · R1 https://www.hisse.net/haber/amp/6-haftadir-dusen-merkez-bankasi-rezervleri-yukselise-gecti-102415 · R2 https://cdn.gedik.com/cdn/bulletin/2026/09/03/Gedik_Yatirim_Parasal_Buyuklukler_Raporu_03092026_ed687479.pdf · T1 https://tradingeconomics.com/turkey/2-year-note-yield · B1 https://tr.euronews.com/2026/10/26/iran-diplomasisi-hizlanirken-petrol-savas-zirvesine-yakin-seviyelerden-6dan-fazla-dusuyor · B2 https://paratic.com/petrol-fiyatlari-yeniden-yukseldi-brent-116-dolara-cikti/ · U1 https://www.foreks.com/haber/detay/6ad5dce258b1b941c208c860/FRKS/tr/abd-tahvil-faizlerinde-gerileme-yasaniyor-19-10-26/ · I1 https://www.forbes.com.tr/haberler/tuik-eylul-2026-issizlik-oranlari-issizlik-yuzde-8-4-e-yukseldi , https://www.ahaber.com.tr/ekonomi/2026/10/27/tuik-eylul-isgucu-verilerini-acikladi-issizlik-yuzde-8-4e-yukseldi · S1 https://gazeteoksijen.com/ekonomi/spkdan-kredili-islemler-karari-ozkaynak-duzenlemesinde-sure-uzatildi-291599 · G1 https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf · G2 https://www.yatirimx.com.tr/piyasa/garanti-bbva-3-ceyrek-beklentisi-uc-araci-kurumdan-kr-artisi-tahmini/26515 · ING 27.10 bülteni ve ajan dosyaları (r1_*.md).
