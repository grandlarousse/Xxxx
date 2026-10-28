# R1 — MAKRO (Faiz/Kur) | 28.10.2026

Etiketler: **[D]** doğrulandı (kaynak var) · **[T]** tek kaynak/kısmen doğrulandı · **[H]** benim hesabım · **[V]** varsayım/tahmin.

## 0. Veri doğrulama (baseline düzeltmeleri)
| Kalem | Değer | Not |
|---|---|---|
| Politika faizi | %37→%36; gecelik borç verme 40→39, borçlanma 35,5→34,5 [D] | Baseline doğru. Yönlendirme: kararlar "toplantı bazında", gerekirse sıkılaştırma [S1] |
| Takvim | Ekim VİOP vadesi **30.10** (kontrat adları) [D]; Ekim TÜFE **3.11 10:00** [V: TÜİK takvim kuralı]; Enflasyon Raporu **12.11**, FİR **27.11**, PPK **10.12** [D, S2]; **FOMC bu akşam 21:00 TSİ** |
| Fed | 16.09'da **+25 bp → %3,75–4,00** [D, S3] | ABD faizi varsayımı: %3,9 |
| Anket (12–14.10, n=71) | YS TÜFE %29,63; 12 ay TÜFE %23,89; YS politika %35,00; 12 ay %29,01; YS USDTRY **51,55** [D, S4] | Aralıkta 100 bp fiyatlı |
| Reel faiz | ex-post (1,36/1,2973)−1=%4,8; **ex-ante (1,36/1,2389)−1=%9,8** [H] | Mevduat/PPF hâlâ hisseyle rekabetçi |
| TLREF | %35,87 (27.10), %35,77 (28.10) [T, S5] | Politika faizinin hafif altı → likidite sıkışması yok |
| Spot | TCMB 27.10 15:30 alış 49,6997 / satış 49,7892 → **orta 49,744** [D, S6] | Hesapta S=49,76 |
| Rezerv | Brüt 171,6 mlr $ (9.10) [D, S7]; 16.10 tahmini 169,1 [T]; swap-hariç net ~56 (Ağu sonu) → 44,2 (9.10) [T] | Fon krizinde 16.09'da tek günde ~5–5,2 mlr $ satış (bankacı hesabı) [T, S8] |
| Fon krizi etkisi | Mevduat +800 mlr TL; 3 ay mevduat faizi %44,4→%43,79; CDS 218→255 (2.10)→244 [T, S9] | |
| Teminat | Takasbank GM 2174 (15.10'dan geçerli): **PSR USDTRY %11,0; XU030 %11,4**; USDTRY vadeler arası yayılma 2.170 TL [D, S10] | Aracı kurum çarpanı (1–2x) ayrıca |
| Sözleşme | USDTRY 1.000 $; vade sonu fiyatı = son gün 15:30 TCMB gösterge **alış-satış ortalaması** [D, S11]; XU030 çarpanı 10 TL/puan [H: Gedik hacim/adet] |

## 1. Rejim
- **TCMB**: Ihtiyatlı 100 bp adımlar; anket YS %35 ve 12 ayda %29. Fon krizine rağmen indirime devam etti, likiditeyi repo artırımıyla destekledi [S12].
- **Kontrollü TL patikası**: 31.12.2025 (F_USDTRY1225 son uzlaşma 42,884 [S13]) → 27.10.2026 (49,79): **+%16,1, yıllıklandırılmış ~%19,6** [H]. Son 3 hafta hızlandı: 9→27 Ekim **~%23,6** yıllık [H]. Beklenen TÜFE ~%29,6 → TL reel değerlenmesi sürüyor.
- **2026'da emilen şoklar**: İran savaşı (Şub–Nis; TCMB rezerv kullandı, fonlamayı %40'a çekti), Mayıs "mutlak butlan", Eylül fon krizi. Hepsinde patika korundu, bedeli rezervle ödendi [S14]. Bu, carry tezinin temeli **ve** kuyruk riskinin kaynağı.
- **Ekim TÜFE** [V/H]: 2026 anketini bulamadım. Anket YS %29,63 + Ekim 2025 aylık %2,55 [D, S15] + Kas/Ara 2025 ~%0,87/0,89 (hafızadan, doğrulanmadı) → tutarlı Ekim 2026 aylık **~%2,0–2,4**. >%2,6 "şahin sürpriz".

## 2. F_USDTRY fiyatlaması (28.10 ~12:39, Foreks [S16])
Formüller: prim=F/S−1; yıllık=prim×365/n; ima TL=[(F/S)(1+0,039·n/360)−1]×365/n.

| Kontrat | n | F | Prim | Yıllık prim | İma TL faizi | Likidite (gün içi) |
|---|---|---|---|---|---|---|
| F_USDTRY1126 | 33 | 51,151 | %2,80 | %30,9 | %35,0 | 765.816 adet, 0,3 kuruş fark |
| **F_USDTRY1226** | 64 | **52,473** | %5,45 | %31,1 | %35,3 | 8.848 adet, 0,2 kuruş |
| F_USDTRY0127 | 93 | 53,692 | %7,90 | %31,0 | %35,3 | 1.695, 3,5 kuruş |
| F_USDTRY0227 | 121 | 54,925 | %10,38 | %31,3 | %35,7 | 43, 6 kuruş |
| F_USDTRY1227 | 429 | 69,198 | %39,1 | %33,2 | %38,7 | 96 (illikit) |

- **Carry = ~%31 yıllık prim; gerçekleşen kur hızı ~%20–24 → ~7–11 puan yıllık fazla getiri** [H].
- **Kırılma noktası (Aralık)**: vade sonu kur **52,473** (bugünden +%5,45 = **%31,1 yıllık hız**). S=49,84 alınırsa %30,1.
- **Geriye dönük test** [H]: Ocak-26 kontratı 31.12.25'te %31,5 yıllık prim fiyatladı, gerçekleşen ~%19,6. 19.06'da F_USDTRY0726 47,972 açığı 47,411'de kapandı (+%1,17/42 gün) [S13]. Temmuzda yıl sonu vadeli 53,85 vs medyan 51 [S14].
- Eğri düz (ileri-ileri Ara→Şub ima TL %34,1, Kas→Ara %34,5) → ek indirim neredeyse fiyatlanmamış. 2027 sonu kontratı (%38,7) risk primi taşıyor ama işlem görmüyor.

## 3. TLREF vadeli
F_TLREF1M1026/1126/1226: **hacim 0**, kotasyon 29,20/43,78 (=36,49'un ±%20 limit bandı) [D, S17]. **Fiili piyasa yok → fikir yok.** Faiz indirimi görüşünün likit ifadesi zaten kısa F_USDTRY: F=S(1+(r_TL−r_USD)t) olduğundan, kısa vadeli = uzun TL süresi; daha hızlı indirim F'yi düşürür. Ara/Şub takvim yayılımı reddedildi: fiyat hatası yok, Şubat bacağının 6 kuruşluk farkı (~%0,11) beklenen hareketi (100 bp ≈ 8 kuruş) yer.

## 4. Makro → endeks zinciri (22 Ekim neden kurtarmadı?)
İndirim → mevduat maliyeti (%43,8, politika faizinin 7,8 puan üstü) **yavaş** düşer → banka net faiz marjı 1–2 çeyrek gecikmeli genişler; düşen TÜFE, TÜFE'ye endeksli tahvil gelirini azaltır → banka hisse başı kâr artışı 2027'ye kayar → bankaların ağırlığı yüksek BIST 30 ancak **risk primi** düşerse yeniden fiyatlanır.
22.10'da işlemeyen halkalar: (i) indirim %100 fiyatlıydı [S4]; (ii) satış faiz değil, **likidite/zorunlu satış** kaynaklı (131 fon tasfiyesi, teminat tamamlama); (iii) ex-ante reel faiz ~%9,8, mevduat +800 mlr TL; (iv) CDS +30 bp, yabancı −527 mn $.
**Ölçülebilir toparlanma koşulu**: CDS<235, 2 hafta üst üste yabancı hisse girişi, swap-hariç rezervde artış, Ekim TÜFE ≤ anket patikası.
**Baz notu (ENDEKS için)**: F_XU0301226 14.644 / F_XU0301026 13.982 → ima finansman **%27,9** vs. FX ima TL %35,3 ve TLREF %35,8 [H, S18]. Aralık kontratı "TL adil taşıma"nın **~181 puan (%1,2)** altında. Temmuzda da aynı fark vardı (%28,7 vs %33,6) → kriz anomalisi değil, yapısal (vergi sonrası bireysel finansman ~%29–30, temettü). Sonuç: vergiden muaf yatırımcı için vadeli long spota göre ucuz; vadeli short hedge ~%1/2 ay ek maliyetli.

## 5. İŞLEM FİKRİ 1 — TL carry: F_USDTRY1226 KISA
- **Enstrüman/yön/vade**: F_USDTRY1226, **satış**, 31.12.2026 vade sonuna kadar tut.
- **Giriş**: 52,40–52,60. FOMC (bu akşam) sonrası 30.10'da %50, 3.11 TÜFE sonrası %50 (TÜFE aylık ≤%2,6 ve kur 10 günlük hız <%30 ise).
- **Stop**: günlük uzlaşma **≥53,20** (+%1,4, kontrat başı −730 TL + kayma). **Hedef**: vade sonu ~51,5–51,8 (anket 51,55; %22 hızla 51,68) → **+650–950 TL/kontrat**. Fiyat 15.12'den önce ≤51,80 olursa yarısını kapat.
- **Büyüklük (1 mn TL sermaye başına)**: **6 kontrat** = 315 bin TL nominal (**0,31x kaldıraç**). Takasbank teminatı 6×5.772 = **34,6 bin TL (%3,5)**; aracı kurum çarpanıyla %5–7. Teminat tamamlamaya karşı ≥3x nakit tampon tut. Stop riski **%0,5**; şok (−1.650/kontrat) %1,0; 19 Mart 2025 tipi +%12 gap (−3.258/kontrat) **%2,0**. Azami 10 kontrat (0,52x).
- **Beklenen değer [V, olasılıklar tahmin]**: %70 olasılıkla patika (%22 hız) → +793; %20 olasılıkla hızlanma (%30) → +95; %10 olasılıkla şok/gap → −1.650. **EV ≈ +410 TL/kontrat** (nominalin %0,78'i, Takasbank teminatının %7,1'i, 64 gün). Maliyet varsayımı (gidiş-dönüş komisyon %0,06 + kayma) ≈36 TL → **net ≈ +373**. Kazanma olasılığı ~%75–80; nominal getiri/risk ~1:1, kuyruk asimetrisi negatif.
- **Tez**: TCMB fiyat istikrarı için TL'yi kur kanalı üzerinden kullanıyor (karar metni) → aylık ~%1,6–2,0 kontrollü kayma → vadeli %31 yıllık primle bu hızı fazla fiyatlıyor → fark vade sonunda kısa pozisyona akar. Rezerv tamponu (171 mlr $ brüt) ve 2026'da üç şokta patikanın korunması bunu destekliyor.
- **Karşı argümanlar**: (1) Negatif çarpıklık: küçük düzenli kazanç, nadir büyük kayıp (Mart 2025'te kur gün içi 41–42'ye fırladı, TCMB 4 günde ~25–28 mlr $ sattı [S19]). (2) Swap-hariç net rezerv ~12 mlr $ eridi [T]. (3) Fed faiz artırıyor; FOMC bugün. (4) Yerleşik dolarizasyonu (Eylülde DTH haftalık +3 mlr $) [S9]. (5) ENDEKS'in olası long'uyla **pozitif şok korelasyonu**: TL şokunda ikisi birden kaybeder; komite toplam riskinde çift sayım yapılmamalı.
- **Tez neye dayanıyor?** "TCMB 64 gün boyunca yıllık ~%31'in altında kontrollü kayma sürdürmeye **istekli ve muktedir**" varsayımına. Bu çökerse (rejim kırılması ya da rekabetçilik için bilinçli hızlandırma) tez biter.
- **Yanlışlama/çıkış**: (a) F_USDTRY1226 ≥53,20; (b) TCMB gösterge ortasında 10 iş günlük hız >%35 yıllık; (c) haftalık brüt rezerv <160 mlr $ veya swap-hariç net haftalık −10 mlr $; (d) bir haftalık repo ihalesinin durdurulması / fonlamanın üst banda kaydırılması (Mart 2025 stres işareti); (e) CDS >300; (f) siyasi/hukuki şok → açılışta çık.
- **Notlar**: Kasım kontratı daha likit (taşıma aynı, %30,9), fakat 30.11 rollover ve FİR (27.11) gerektirir. O_USDTRYKE1226C57000 kuyruk koruması: son 360 TL, satış kotasyonu yok, hacim 0 [S20]. Prim taşımanın büyük kısmını yer; OPSİYON fiyatlasın. Vergi/stopaj aracı kurumla teyit edilmeli.
- **Güven: 6/10.**

## 6. İŞLEM FİKRİ 2 (KOŞULLU) — F_XU0301226 UZUN, makro kapılı
- **Yalnızca 20.11'e kadar şu koşulların hepsi gerçekleşirse**: Ekim TÜFE aylık ≤%2,3; CDS ≤235; TCMB menkul kıymet istatistiklerinde 2 hafta üst üste yabancı hisse alımı; USDTRY hızı <%26. Koşulların oluşma olasılığı ~%30 [V].
- **Giriş**: tetik günü piyasa fiyatı. **Stop**: −%6 (14.644'ten ~13.765; analist desteği 13.800/13.700 ile uyumlu). **Hedef**: +%10 (~16.100). **Süre**: Aralık vadesi.
- **Büyüklük**: 1 kontrat = ~146 bin TL nominal, Takasbank teminatı ~16,7 bin TL (PSR %11,4). Risk %0,5–1 → **1 mn TL için 0,5–1 kontrat** (nominal %7–15).
- **EV [V]**: Koşullar sağlanırsa P(+%10 önce) ~%45 → 0,45×10 − 0,55×6 ≈ **+%1,2 nominal**, üstüne ~%1 baz yakınsaması. R/R 1,7:1.
- **Tez**: TÜFE uyumlu → Aralıkta 100–150 bp indirim inandırıcı → ex-ante reel faiz düşer → fon tasfiye yükü takvime bağlı ve sonlu → CDS normalleşir → yabancı girişi → bankalar ve BIST 30 yeniden fiyatlanır.
- **Karşı argüman / çöküş**: Satışın kaynağı tasfiye takvimiyse makro iyileşme fiyatı taşımaz; tasfiye 6 ay sürer. **Çıkış**: yeni fon temerrüdü/SPK tasfiye kararı, CDS >270, Kasım TÜFE (3.12'de açıklanması beklenir [V]) aylık >%1,8, haftalık kapanış 13.700 altı.
- **Güven: 4/10** (teknik onayı ENDEKS versin).

## Kaynaklar
S1 TCMB ANO2026-45: https://www.tcmb.gov.tr/wps/wcm/connect/en/tcmb+en/main+menu/announcements/press+releases/2026/ano2026-45 · S2 https://www.cnbce.com/faiz/turkiye-cumhuriyet-merkez-bankasi-2026-yili-para-politikasi-kurulu-ppk-toplantilari-ve-rapor-takvimini-acikladi-h22037 · S3 https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm · S4 https://www.foreks.com/haber/detay/6ad1d143422c786f3f7a43e8/PICNEWS/tr/piyasa-katilimcilarinin-yil-sonu-enflasyon-beklentisi-yuzde-29-63-e-yukseldi-16-10-26/ · S5 https://tr.investing.com/indices/try-overnight-reference-rate-scoreboard , https://borsa.doviz.com/endeksler/tlref-turk-lirasi-gecelik-referans-faiz-orani/haberler · S6 https://www.foreks.com/sembol-detay/o46/usdtry-tcmb/tcmb-abd-dolari-turk-lirasi/ · S7 https://www.qnbinvest.com.tr/investodak/qnbarastirma/tcmb-rezervleri-1716-milyar-dolara-yukseldi-bes-haftalik-dusus-serisi-sona-erdi ; tahmin https://www.cnbce.com/haberler/tcmb-rezervlerinin-25-milyar-dolar-azaldigi-hesaplandi-h39779 ; swap-hariç https://cdn.gedik.com/cdn/bulletin/2026/09/03/Gedik_Yatirim_Parasal_Buyuklukler_Raporu_03092026_ed687479.pdf , https://www.hisse.net/haber/amp/6-haftadir-dusen-merkez-bankasi-rezervleri-yukselise-gecti-102415 · S8 https://paratic.com/fon-krizinin-faturasi-tcmbnin-doviz-satisi-5-milyar-dolari-asti/ · S9 https://www.borsagundem.com.tr/fon-krizi-borsadan-ekonomiye-uzanan-etkiler · S10 https://www.isyatirim.com.tr/tr-tr/Resmi-Duyurular/Documents/GenelMektup2174.pdf · S11 https://www.borsaistanbul.com/files/VIOP_Doviz_Sozlesmeleri.pdf · S12 https://www.forbes.com.tr/ekonomi/tcmb-den-likidite-adimi-repo-fonlamasi-artirilacak · S13 https://cdn.gedik.com/media/media/hd5h42hm/viop_bulten_02012026.pdf , https://cdn.gedik.com/cdn/bulletin/2026/06/22/VIOP_Bulten_22062026_9936641f.pdf , https://cdn.gedik.com/cdn/bulletin/2026/07/31/VIOP_Bulten_31072026_23efc9ac.pdf · S14 https://www.bloomberght.com/carry-getirisinde-tl-ust-siralarda-3782076 , https://www.bloomberght.com/carry-trade-yatirimcilari-iran-iyimserligiyle-tlye-donus-yapti-3780967 , https://www.forbes.com.tr/ekonomi/morgan-stanley-den-turk-lirasi-karari-carry-trade-cazibesini-yitirmedi · S15 https://www.qnbinvest.com.tr/investodak/qnbarastirma/enflasyon-ekimde-329a-geriledi-son-47-ayin-en-dusuk-seviyesi · S16 https://www.foreks.com/sembol-detay/H791750/f-usdtry1226/usdtry-31-ara-26-vadeli/ (1126: H779932, 0127: H806248, 0227: H818494, 1026: H769000, 1227: H954798) · S17 https://www.foreks.com/sembol-detay/H899230/f-tlref1m1126/tlref-30-kas-26-vadeli/ · S18 https://www.foreks.com/sembol-detay/H845730/f-xu0301226/xu030-31-ara-26-vadeli/ , https://www.foreks.com/sembol-detay/H898940/f-xu0301026/xu030-30-eki-26-vadeli/ · S19 https://www.cnbce.com/doviz/reuters-tcmb-net-doviz-pozisyonu-sorusturmanin-ilk-4-gununde-yaklasik-28-milyar-dolar-geriledi-satislar-yavasladi-h10969 · S20 https://www.foreks.com/sembol-detay/H967760/o-usdtryke1226c57000/usdtry-31-ara-26-alim-opsiyonu/

Hesap betikleri: /tmp/claude-0/-home-user-Xxxx/e9cebbab-b80e-5b61-827f-5051f73327e4/scratchpad/viop/calc/carry.py , size.py
