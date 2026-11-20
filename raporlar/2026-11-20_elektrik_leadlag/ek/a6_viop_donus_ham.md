araç: 17/40

## Özet (A6 — VİOP, yalnız IS → 2022-12-30)

- **Tarama:** önceden yazılı ızgara 234 kural (= 234 test): V1 kendi baz sıçraması 72, V2 hacim/açık pozisyon 18, V3 XU030 vadelisi bazı 72, V4 çapraz 72. Ek olarak 17 keşif testi (kontrol, alt küme). Toplam 251 test.
- **Aile sonucu zayıf:** BH (q=0,10) geçen kural yok. t>2 olan 11, t<−2 olan 5 kural. Aile içi en iyi kuralın yer değiştirme p-değeri 0,28: 234 testin en iyisi şansla açıklanabilir.
- **Beklenti doğrulanmadı:** baz sıçramasından sonra ters yönde dönüş yok. Baz yukarı sıçrayınca spot ve vadeli aynı yönde sürüyor (zayıf, az olaylı). V3 bütünüyle olumsuz (sektör AL her hücrede net negatif). Kısa (SAT) yönde ölçütleri geçen kural yok.
- **Dondurulan: 1 birincil + 6 ikincil.** Birincil `A6_V4_akran_vadeli_getiri_z1_spotAL_h2`: üçlüden hedef dışındaki bir üyenin vadeli uzlaşma getirisi ≥ 1σ (60 günlük gecikmeli std) → hedef spot AL, 2 gün. Yedi ölçütün hepsini karşılıyor. Ancak **vadeliye özgü değil**: aynı kural spot getirisiyle de +53 bps (t=2,7) veriyor; A1/A2 kurallarıyla örtüşebilir, ana ajan tekilleştirmeli.
- İkinciller: aynı sinyalin h=3 ve vadeli AL sürümü (vadelide IS kanıtı yok, t=0,9), V1 baz yukarı z≥1,5 h2 ve z≥1 h3 (spot AL), V2 vadeli hacim 3× + yukarı gün h3, bir keşif kuralı (birincil + hedef henüz hareket etmemiş; ızgara dışı, aday olamaz).
- **Vadelinin gerçek maliyeti:** IS'te işlemsiz gün yok. ODAS vadelisinde fiyat adımı medyan 47 bps (2022: 32): tek adımlık makas temel senaryodaki 35 bps'ye yakın ya da üstünde, yani ODAS maliyeti eksik sayılmış. Uzlaşma − son fiyat mutlak farkı 22–37 bps. Uzun vadeli pozisyon spota göre günde 9–15 bps taşıma ödüyor.
- **Öz-denetim:** `self_check_causal` yedi kuralda 0,0 (iki kesim tarihi); build 0,1 sn, deterministik. `run.sh` baştan sona 44 sn'de çalışıyor.
- Kütüphane hatası görmedim. Not: `evaluate_viop` en iyi 10 hariç, yarı ve t+1 girişi vermiyor; bunları aynı tanımla `02_tara.py` içinde hesapladım.
- SAPMA yok. Yalnız `panel_is` okundu, veri indirilmedi.

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a6_viop/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a6_viop/run.sh
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a6_viop_sonuc.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a6_viop_likidite.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a6_viop.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a6_viop/_tanilar.txt

## İddia defteri

Kısaltmalar: SONUC = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a6_viop_sonuc.csv; LIK = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a6_viop_likidite.csv; TANI = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a6_viop/_tanilar.txt; OZD = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a6_viop/_ozdenetim.txt

iddia | dosya yolu | sayı | güven
--- | --- | --- | ---
Izgara test sayısı | SONUC | 234 kural, 355 satır; + 17 keşif | yüksek
BH (q=0,10) geçen | SONUC (bh_gecti) | 0 | yüksek
t>2 / t<−2 kural sayısı | SONUC | 11 / 5 | yüksek
Aile içi en iyi t için yer değiştirme p | TANI | 0,282 (300 kaydırma) | orta
Birincil: bağımsız olay, fazla getiri, t | SONUC / OZD | 159; +85,3 bps; t=3,09 | yüksek
Birincil: temel maliyet sonrası net | SONUC | +46,6 bps | yüksek
Birincil: kronolojik yarılar | SONUC | +107 / +64 bps | yüksek
Birincil: yıllar 2019–2022 | SONUC (yillar_bps) | 181, 103, 61, 56 bps | yüksek
Birincil: en iyi 10 gün hariç | SONUC | +37,9 bps | yüksek
Birincil: t+1 kapanışından giriş | SONUC | +70,6 bps | yüksek
Birincil: gece payı, en yoğun hisse payı | SONUC | 0,2; 0,5 (AKSEN) | yüksek
Birincil: hedef bazında (AKSEN/ENJSA/ODAS) | SONUC | +84 / +80 / +85 bps | yüksek
Birincil komşuları (z1,5 h2; z2 h2; z1 h3) | SONUC | t=2,5; 1,8; 2,8 | yüksek
Birincil, kontrollü regresyon (kendi r, XU100) | TANI | +67 bps, t=2,44 | orta
Aynı kural spot getirisiyle (2019-03+) | TANI | +53 bps, t=2,72 | orta
Aynı kural vadeli yokken (2019-03 öncesi) | TANI | +26 bps, t=1,59 | orta
ENJSA kaynaklı kol 2022 | TANI | −17 bps | orta
Birincilin vadeli AL sürümü (h2) | SONUC | 82 olay; +40,9 bps; t=0,85; net +4,5; en iyi 10 hariç −52 | yüksek
V1 uzlaşma z≥1,5 yukarı, spot AL h2 | SONUC | 37 olay; +160 bps; t=3,0; son fiyat tanımında net +23; en iyi 10 hariç +4,5 | yüksek
V1 uzlaşma z≥1 yukarı, spot AL h3 | SONUC / TANI | 91 olay; +88 bps; t=2,0; kontrolde t=1,32 | yüksek
V2 vadeli hacim 3× + yukarı, spot AL h3 | SONUC | 53 olay; +143 bps; t=2,1; en iyi 10 hariç +11; t+1 girişi +216 | yüksek
Keşif kuralı (birincil + kendi z<1) | SONUC / TANI | 147 olay; +111 bps; t=3,81 | orta (sonradan tanımlandı)
V3 XU030 bazı → sektör AL, h1 net | SONUC | −27 ile −73 bps (bütün hücreler negatif) | yüksek
Fiyat adımı medyan (ODAS / ENJSA / AKSEN) | LIK | 46,5 / 9,7 / 2,1 bps; 2022: 32 / 6,5 / 2,1 | yüksek
Uzlaşma − son fiyat mutlak ortalama | LIK | AKSEN 37, ODAS 24, ENJSA 22, XU030 6 bps | yüksek
Vadeli − spot günlük getiri farkı (taşıma) | LIK | AKSEN −15,0; ODAS −13,6; ENJSA −9,3; XU030 −4,8 bps/gün | yüksek
Yıllık taşıma medyanı | LIK | ENJSA %19,8; AKSEN %26,3; ODAS %30,3; XU030 %13,0 | orta
Hafta sonu etkisi (hafta içi / hafta sonu fark) | LIK | ENJSA −13,4 / +6,7; AKSEN −23,3 / +21,6; ODAS −14,1 / −12,3 bps | düşük (gürültülü)
İşlemsiz gün oranı (en hacimli vade) | LIK | 0 (dört kontratta) | yüksek
Öz-denetim (7 kural, kesim 2021-06-30 ve 2022-06-30) | OZD | hepsi 0,0; build 0,1 sn | yüksek

## açık kalanlar

- AKSEN vadelisi IS'te 44 gün; z-skoru için en az 40–60 gün gerektiğinden hiçbir kuralda sinyal üretmedi. Kurallar fiilen ENJSA (2019-03+) ve ODAS (2021-07+) üzerinde sınandı.
- Birincil kural A1/A2 ailelerinin akran öncülüğü kurallarıyla büyük olasılıkla örtüşüyor; 28 birincil kural içinde çift sayılmaması için tekilleştirme ana ajanda.
- Sinyal uzlaşma fiyatına dayanıyor (18:10'da kesinleşir), spot kapanışı 18:05'te oluşuyor. t kapanışında giriş ancak yaklaşık hesapla olur; t+1 girişi pozitif ama gün içi veriyle (A7) doğrulanmadı.
- ODAS vadelisinde temel maliyet (35 bps) fiyat adımının altında kalıyor; ortak maliyet tablosu fiyat adımını vadeliye eklemiyor. Vadeli hedefli kurallar OOS'ta buna göre yeniden okunmalı.
- Aile düzeyi yer değiştirme testi basit t ile (HAC'siz) ve kural başına etkin pencerede yapıldı; p=0,28 yaklaşık bir değerdir.
- Vadeli hedefli hiçbir kural IS'te ölçütleri geçmedi: vadeli ile AL/SAT için bu aileden kanıt yok.