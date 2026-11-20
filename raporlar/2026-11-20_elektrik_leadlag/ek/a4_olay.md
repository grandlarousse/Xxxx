# A4 — Olaylar (tavan/taban bulaşması, sektör günü, genişlik, hacim patlaması)

**Veri:** yalnız `panel_is` (2010-01-04 → 2022-12-30). Tavan/taban bayrakları 2015-12-01'den itibaren kullanıldı. Karar ölçüsü `own`, her satır `elib.evaluate` çıktısı. Kütüphane hatası görülmedi.

**Taranan:** E1–E8, h = 1/2/3. Önceden yazılı ızgara 156 satır, komşu parametre/keşif 48 satır: **toplam 204 test**. Tek yönlü BH (q = 0,10): **geçen yok** (en küçük p = 0,007). Izgarada t > 2 yalnız 4 satır (tesadüf düzeyi).

## IS bulguları (bps, dolabilir; t tarih kümelemeli)

- **E1 tavan bulaşması:** h=1'de +10 (t=1,0), maliyet sonrası −18. h=2/3'te +33/+43 (t=1,8/1,7), net +7/+22. Beklentinin tersine doz-tepki yok: 2–3 tavan h=1 −15, ≥4 tavan −8…−36 (11–16 olay), pay ≥ %5 net negatif. Aynı kümede etki farklı kümeden zayıf. Gün düzeyi regresyonda sektör sepeti getirisi eklenince tavan kuklası anlamsız (t=0,4–0,9): etki bulaşma değil, sektör momentumu. 2021 negatif (−85).
- **E2 taban:** ≥2 taban günü ertesi gün +108 (27 olay) ama en iyi günler çıkınca −70, t+1 kapanışı girişinde −29. VİOP SAT: −28.
- **E3 sektör günü, E4 genişlik:** yukarı günlerden sonra AL anlamsız. Aşağı genişlik gününden sonra sektör zayıf kalıyor (AL −28, t=−1,6; komşularda −18…−32, iki yarıda da negatif).
- **E5:** patlama yapan hissede devam yok (−14, net −60). Akranlarda +10/+19/+30 (t=2,1–2,5) ama maliyetin altında.
- **E6:** tavana değip kapanmayan hisse ertesi gün **−99 (t=−2,5)**, iki yarıda da negatif; 2022'de ~0. Spotta satılamaz; VİOP üçlüsünde 7 olay. Tavanda kapanan hisse (alınamaz) +368. Tabana değip kapanmayan da toparlanmıyor (−99).
- **E7:** seri biten hissenin kendisi −144 (t=−1,7); akranlarda etki yok.
- **E8:** halka arzın ilk 5 gününde mevcut hisseler −26 (t=−1,3); 21 halka arz.

## Karar: BİRİNCİL KURAL DONDURULMADI

Hiçbir satır (i)–(vii)'nin tamamını karşılamıyor. E1 h=3 en yakını; (vi) ve (vii)'de kalıyor. Aşağıdaki 5 kural **ikincil (izleme)**. `self_check_causal`: beşi de 0,0; `build()` 0,1 sn.

### DONDURULMUŞ KURAL — A4_E1_herhangi_h3 (ikincil)
Girdi: `lim_up`, `tradable`. Koşul: t günü hedef dışında en az bir tradable XELKT üyesi tavanda kapandı. Evren: tradable, tavanda kapanmamış üyeler. Giriş t kapanışı, çıkış t+3 kapanışı, AL. IS: 181 bağımsız olay, +43,1 (t=1,68), net +21,5; yarılar +116 / +36; en iyi %5 hariç +0,4; t+1 girişinde +22,9; yer değiştirme p=0,003. Mekanizma: sektöre ilgi taşması.

### DONDURULMUŞ KURAL — A4_E1x_herhangi_sepet_arti_h2 (ikincil, KEŞİF)
Yukarıdaki koşul **ve** tradable üyelerin eşit ağırlıklı t getirisi > 0. AL, 2 gün. IS: 210 olay, +50,3 (t=2,59), net +26,0; yarılar +89 / +46; en iyi %5 hariç +18,1; t+1 girişinde +21,0. Izgara dışı; sektör momentumu.

### DONDURULMUŞ KURAL — A4_E4_eks_SAT_h2 (ikincil)
Girdi: `ret_cc`, `tradable`. Koşul: tradable üyelerin ≥ %50'si < −%2, en az 5 üye. Hedef: AKSEN/ENJSA/ODAS vadelisi, SAT, 2 gün. IS: 77 olay, spot fiyatla +74,5 (t=1,55), vadeli uzlaşmayla +46,3 (t=0,91), net +9; en iyi günler hariç −31; ENJSA payı %71; 2021 yoğun. Mekanizma: satış dalgasının devamı.

### DONDURULMUŞ KURAL — A4_E6_degdi_kapanmadi_SAT_h1 (ikincil)
Girdi: `lim_up_touch`, `lim_up`. Koşul: AKSEN/ENJSA/ODAS tavana değdi, tavanda kapanmadı. Aynı hissenin vadelisinde SAT, 1 gün. IS: 7 olay, +30 (t=0,1). Dayanak spot satırı (−99). Mekanizma: tavanda tutunamayan talebin çözülmesi.

### DONDURULMUŞ KURAL — A4_E5_akran_AL_h3 (ikincil)
Girdi: `vol_tl`, `ret_cc`. Koşul: başka bir tradable üyede hacim > 3 × önceki 20 günün medyanı ve getiri > +%3; hedef kendisi patlama yapmamış tradable üyeler. AL, 3 gün. IS: 548 olay, +30,0 (t=2,47), **net −5,9**; yarılar +34 / +22; en iyi %5 hariç −6.

## Bilinen zayıflıklar

- Tavan olaylarının neredeyse tamamı 2020–2022; ilk yarı 23–34 olay ve ±%20 marj dönemi.
- Adet eşikleri ölçeğe bağlı: “≥1 tavan” 2022'de günlerin %44'ünde doğru; 40+ hisseyle kural neredeyse sürekli açık kalır. Paya dayalı sürüm IS'te desteklenmedi.
- `own` kıyası 120 gün geçmiş ister: yeni halka arzların ilk ~6 ayı ölçüye girmiyor.
- VİOP satırları 2018-12 sonrası, ağırlıkla ENJSA.
- Hayatta kalma yanlılığı; VBTS tedbirleri yok.
