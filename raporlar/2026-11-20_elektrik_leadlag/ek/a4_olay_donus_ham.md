araç: 17/40

## Özet

**Birincil kural dondurulmadı.** IS'te (2010-01-04 → 2022-12-30) E1–E8 için 204 test yaptım (156 önceden yazılı ızgara + 48 komşu parametre/keşif); tek yönlü BH'den (q = 0,10) geçen satır yok ve hiçbir satır (i)–(vii)'nin tamamını karşılamıyor. 5 ikincil (izleme) kuralı dondurdum. `self_check_causal` beşi için 0,0; `build()` 0,1 sn; `run.sh` 16 sn'de baştan sona çalışıyor. Kütüphane hatası görmedim. Yalnız `panel_is` kullanıldı, veri indirilmedi.

Rakamlar bps, dolabilir gözlemler, `own` ölçüsü, t tarih kümelemeli:

- **E1 tavan bulaşması (beklentin):** h=1'de +10 (t=1,0), maliyet sonrası −18. h=2/3'te +33/+43 (t=1,8/1,7), net +7/+22. Beklentinin tersine çok tavanlı günlerde güçlenmiyor: 2–3 tavanda h=1 −15, ≥4 tavanda −8…−36 (11–16 olay). Sektör sepetinin o günkü getirisi kontrol edilince tavan kuklasının ek etkisi yok (t=0,4–0,9). Etki bulaşma değil, sektör momentumu görünüyor; 2021 negatif.
- **E6 (beklentin):** tavana değip kapanmayan hisse ertesi gün −99 (t=−2,5), iki yarıda da negatif. Geri dönüş var ama spotta satılamaz; VİOP üçlüsünde yalnız 7 olay. 2022'de etki ~0.
- **E4 genişlik:** aşağı genişlik gününden sonra sektör zayıf kalıyor (AL −28, t=−1,6; komşu eşiklerde −18…−32). VİOP SAT h=2 spot fiyatla +75, vadeli uzlaşmayla +46 (t=0,9); ENJSA ağırlıklı, en iyi günler çıkınca negatif.
- **E5:** patlama yapan hissede devam yok (−14). Akranlarda +30 (h=3, t=2,5; ızgaranın en yüksek t'si) ama temel maliyetin altında (net −6).
- **E2, E3, E7, E8:** kullanılabilir sinyal yok. E2 ≥2 taban +108 ama 27 olay ve en iyi günlere bağlı. E7'de seri biten hisse −144 (t=−1,7), akranlarda etki yok. E8'de mevcut hisseler −26 (t=−1,3).

**İkincil kurallar:** `A4_E1_herhangi_h3`, `A4_E1x_herhangi_sepet_arti_h2` (keşif, ızgara dışı), `A4_E4_eks_SAT_h2` (viop), `A4_E6_degdi_kapanmadi_SAT_h1` (viop), `A4_E5_akran_AL_h3`.

**Sapma notları:**
- `xelkt_uyeler.csv` dosyasını `head` ile açarken diğer sütunlar da ekrana geldi; kodda yalnız `ana_faaliyet` okunuyor (`usecols`) ve yalnız elenen kırılımlarda kullanıldı.
- IS yarıları bütün kurallarda ≤2019 / 2020–2022 alındı; kısa geçmişli hisseler için ayrı kronolojik yarı hesaplanmadı.
- Tavan/taban bayraklarını 2015-12-01'den itibaren kullandım (sabit, kodda yazılı).

## İddia defteri

iddia | dosya yolu | sayı | güven
---|---|---|---
Toplam test | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a4_olay_sonuc.csv | 204 satır (156 ızgara + 48 komşu/keşif) | yüksek
BH (q=0,10, tek yönlü) geçen | aynı csv, `bh_gecti` | 0; en küçük p = 0,0068 | yüksek
Seçim dağılımı | aynı csv, `secim` | birincil 0, ikincil 5, elendi 199 | yüksek
Izgarada t > 2 olan satır | aynı csv | 4 (E5_akran h1–3, E1_yalniz_farkli_kume h2) | yüksek
E1_herhangi h=1 | aynı csv | +9,8 bps, t=0,99, net −18,2, 374 olay | yüksek
E1_herhangi h=2 | aynı csv | +32,8, t=1,83, net +7,3, en iyi %5 hariç +1,0 | yüksek
E1_herhangi h=3 (ikincil) | aynı csv | +43,1, t=1,68, net +21,5, 181 olay; yarılar +115,7 (23 olay) / +35,8; en iyi %5 hariç +0,4; t+1 girişi +22,9 | yüksek
E1_herhangi h=3 yıllar | aynı csv, `yillar_bps` | 2016:−54; 2019:164; 2020:69; 2021:−85; 2022:99 | yüksek
E1 f_1 gece / gün içi | aynı csv | −12,4 / +24,0 | yüksek
E1 doz-tepki ters | aynı csv | n2_3 h1 −14,8; n4p h1/2/3 −7,9/−18,0/−36,0 (16/14/11 olay); pay20 h1 −37,3 | orta (olay az)
E1x_pay05 (ölçekten bağımsız komşu) | aynı csv | h2 +20,5 net −13,1; h3 +28,3 net −2,6 | yüksek
E1 yer değiştirme testi (300 kaydırma) | hesap oturumda; csv'de yok | h2 ve h3 p=0,003 | orta
Regresyon: tavan kuklası, sepet getirisi kontrollü | hesap oturumda; csv'de yok | t=0,44 / 0,93 / 0,58 (h=1/2/3); sepet getirisi t=1,7 / 2,4 / 2,2 | orta
E1x_herhangi_sepet_arti h=2 (ikincil, keşif) | aynı csv | +50,3, t=2,59, net +26,0, 210 olay; yarılar +89,2 / +45,6; en iyi %5 hariç +18,1 | yüksek
E1x_herhangi_sepet_eksi | aynı csv | h1/2/3 −33,6 / −57,1 / −32,4 | orta
E4_eks_sektor_AL h=1 | aynı csv | −27,7, t=−1,62, 240 olay; yarılar −15,6 / −52,5 | yüksek
E4_eks_SAT h=2 (ikincil) | aynı csv | spot fiyatla +74,5, t=1,55, net +43,7, 77 olay; en iyi günler hariç −31,5; ENJSA payı 0,71 | yüksek
E4_eks_SAT h=2 vadeli fiyatla | finalize.py çıktısı (eval_rule) | uzlaşma +46,3, t=0,91, net +9,1; son fiyat +53,0 | yüksek
E5_kendi_AL h=1 | aynı csv | −13,8, t=−0,85, net −60,2 | yüksek
E5_akran_AL h=3 (ikincil) | aynı csv | +30,0, t=2,47, net −5,9, 548 olay; yarılar +34,5 / +22,5; en iyi %5 hariç −6,0 | yüksek
E6_degdi_kapanmadi_AL h=1 | aynı csv | −98,9, t=−2,54, 207 olay; yarılar −264 / −83; 2022: +1 | yüksek
E6_degdi_kapanmadi_SAT h=1 (ikincil) | aynı csv | 7 olay, +30,0, t=0,12; vadeli uzlaşmayla +16,7 | düşük (olay az)
E6 tavanda kapanan (alınamaz, bilgi) | aynı csv, `hepsi_own_IS_bps` | h1 +368 (t=9,7), 518 hisse-gün | yüksek
E6 tabana değip kapanmayan AL h=1 | aynı csv | −99,4, t=−1,62 | yüksek
E2_n2p_AL h=1 | aynı csv | +108,4, t=1,84, 27 olay; en iyi günler hariç −69,9; t+1 girişi −29,1 | orta
E7_kendi_AL h=1 / akran h=1 | aynı csv | −143,5 (t=−1,69, 84 olay) / +5,1 (t=0,21) | yüksek
E8_ilk5_gun_AL h=1 | aynı csv | −25,7, t=−1,31, 90 olay (21 halka arz) | orta
Nedensellik öz-denetimi | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a4_olay/rules.py | 5 kuralın hepsi 0,0; build() 0,1 sn | yüksek
"≥1 tavan" günü sıklığı | hesap oturumda | 2020: %54, 2021: %38, 2022: %44 | yüksek
Not ve kod | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a4_olay.md ; /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a4_olay/ (run.sh, scan.py, finalize.py, rules.py) | not 595 kelime | yüksek

## açık kalanlar

- **Ölçek sorunu:** E1'in adet eşiği (≥1 tavan) 40+ hisselik 2023+ evreninde neredeyse her gün doğru olur; paya dayalı sürüm (≥%5, ≥%10) IS'te desteklenmedi. OOS'ta `A4_E1_herhangi_h3` kural olmaktan çok "sürekli açık" bir pozisyona dönebilir.
- **E6 geri dönüşü işlem yapılabilir araçta sınanamadı:** VİOP üçlüsünde 7 olay. Spot kanıtı güçlü ama 2022'de ve yeni listelenenlerde kayboluyor.
- **`own` kıyası 120 gün geçmiş istiyor:** yeni halka arzların ilk ~6 ayı hiçbir satıra girmiyor. Bu kütüphane tasarımı, hata değil; 2021–22 halka arzları için kanıt eksik.
- **Sektör momentumu A2'nin alanı:** E1 ve E5 akran etkisinin kaynağı büyük olasılıkla sepet getirisi. Bunu A2 sonuçlarıyla karşılaştırmadım.
- Yer değiştirme testi ve gün düzeyi regresyon çıktıları dosyaya yazılmadı; `run.sh` bunları yeniden üretmiyor.
- VBTS tedbirleri ve hayatta kalma yanlılığı sınanmadı.