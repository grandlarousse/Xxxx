# motor.py — ortak backtest motoru (YONTEM sürüm 2)

Test: `python3 -I test_motor.py`. Örnek: `python3 -I ornek_kural.py`.

## Bir kural, 15 satır

```python
import sys; sys.path.insert(0, "/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod")
import motor as M
m = M.Motor()                                   # panel + önbellek
def kural(mm):                                  # t satırı = t kapanışında bilinen
    r = mm.girdi_getiri("XLE")                  # güvenli girdi (SONRA/VIX1615 1 gün gecikmeli)
    vix = mm.girdi("^VIX", "close")             # VIX(t-1) gelir
    esik = M.genisleyen_esik(r, 0.05)           # yalnız t-1'e kadar
    return ((r < esik) & (vix > 20)).astype(int)    # +1 al, -1 sat, 0 yok
tamam, rapor = m.bakis_testi(kural); assert tamam   # ileriye bakma denetimi
sonuc = m.degerlendir(kural(m), "XLE", kural_id="D-017", aile="D",
                      ad="XLE %5 düşüş, VIX>20", girdi="XLE, ^VIX(t-1)", bootstrap=True)
M.yaz_sonuc(sonuc, ".../veri/sonuc_D.csv", ekle=True)   # standart şema (M.SEMA)
```

Çok hedefli: `sinyal` = DataFrame (tarih × hedef), `guc` = sinyal gücü.

## İşlevler

- Girdi: `girdi`, `girdi_getiri`, `getiri`, `df` (güvenli; `ham=True` yalnız hedef fiyatı için; `sizintili=True` yalnız VIX ailesi), `artik_getiri`, `z_skor`, `genisleyen_esik`, `genisleyen_sira`.
- Hedef: `ileri(giris, h, cikis)`, `beta(piyasa, 250|60)`, `ileri_korunmali`, `sigma20`, `hedef_uygun`, `kosulsuz_taban`.
- Rejim: `rejim()` → vix_1, vix_kova, ust200, rejim, bolum.
- Maliyet: `kademe`, `bacak_bps`, `ham_fiyat`, `temettu_orani`.
- İşlem: `islemler(...)` (örtüşmeyen liste), `gunluk(isl, komisyon)`, `bolum_ozeti`, `degerlendir(...)`.
- İstatistik: `bootstrap_p`, `wilcoxon_p`, `bh`, `mdd`.
- Tarama: `tarama_regresyon`, `tekillestir`, `kumele`, `sepet_getiri`, `tarama_hedef_maskesi`, `blok_permutasyon`, `dairesel_kaydir`.
- Evren: `donem_basi_evreni`, `evren_maskesi`. Dönemler: `M.DONEMLER`, `M.YENI_YAPI` (`donemler=["IS2","OOS2"]`).

## Yorumlar (belirsiz noktalarda muhafazakâr seçim)

1. Giriş G: t+1 kapanışında girilir, h gün tutulur (çıkış t+1+h).
2. Hacim kademesi günlüktür (t−1'e kadar 60 gün) ama evren.csv `maliyet_bps`'in altına inmez.
3. 0,5 sent tabanı ve hisse başı komisyon gerçek (bölünmesi geri alınmış) fiyattan.
4. Maliyet ×2: sinyal günü ya da bacak günü VIX(önceki gün) > 30 ise.
5. Nakit faizi her uzun pozisyonda h gün (gün içi A, h=1 dahil); kısa pozisyona faiz geliri yok.
6. Temettü: `yukle.temettu()` tablosu ile adjclose/close oranının büyüğü; özel dağıtımlar da %30 kesilir.
7. Zor ödünç (+%10): kaldıraçlı/ters ürünler ve 60 günlük hacmi < 50 milyon $.
8. Hedef yalnız ABD16; ilk 60 gün ve hacmi < 20 milyon $ günler hedef olamaz.
9. Bölüm: iki VIX > 30 günü arasında < 20 gün boşluk. Kovalar: < 20; 20–30 (uçlar dahil); > 30.
10. Anormal getiri tabanı ana dönem × VIX kovası ortalamasıdır; tanım gereği dönemin tamamını kullanır.
11. `t_olcekli`, `p_wilcoxon` net getiriden; `net_sigma` = net / 20 günlük σ ortalaması.
12. `yillik_net_pct` günlük seriden; `pozitif_yil_orani` yalnız işlem olan yıllar.
13. Maliyet ×2 yalnız işlem maliyetini ikiye katlar; finansman aynı kalır.
14. Kabuk kesimi `KABUK_KESIM`; β en az pencere/2 gözlem ister; kümeleme SPY'dan arındırılmış IS getirileriyle.

## Bilinen sınırlar

- `bakis_testi` yalnız gelecekteki veriyi yakalar; ham (`ham=True`) SONRA serisini aynı gün kullanmayı yakalamaz.
- Kapanış/açılış fiyatından dolum varsayılır; kayma ve emir kesim saati modellenmez.
- Portföy ağırlıkları her gün eşitlenir; yeniden dengeleme maliyeti yok.
- Ağır ters bölünmeli ürünlerde (SOXS, TECS, UVXY) eski hacim güvenilmez: o günler hedef dışı kalabilir.
- STRES için dönem başı evreni yok; 2010 evreninde 122 hisse.
- Kümelenmiş standart hata sinyal gününe göredir; günler arası bağımlılığı bootstrap yakalar.
- Çok hedefli `degerlendir` ~10 sn; keşifte `rejimler=False`, tek komisyon. scipy yok: Wilcoxon normal yaklaşımla.

## Denetim notları (KD, 22.11.2026; `python3 -I test_denetim.py`, sonuç `veri/denetim_sonuc.csv`)

- Çok hedefli (havuzlanmış) kuralda `t_olcekli` kullanılmaz: aynı gün tetiklenen işlemler bağımlıdır, gürültü kurallarında |t| ≥ 1,96 oranı %55 çıktı. Karar için `t_kume` ve `p_bootstrap` (ikisi de ≈ %5).
- `t_olcekli`, `p_wilcoxon`, `p_bootstrap` net getiridendir, anormal getiriden değil. Yalnız uzun yönlü kuralda hedefin kendi yükseliş eğilimi t'ye girer (rastgele giriş, h=3, AAPL: ortalama t ≈ 2). `anormal_bps` ile birlikte okuyun; gerekirse `islem_dondur=True` ile `anormal / sigma20` t'sini hesaplayın.
- `guc` verilmezse 5 pozisyon tavanında seçim sütun sırasına göredir; günlük seri (p_bootstrap, mdd, yıllık net) yalnız ilk sütunları yansıtır. Çok hedefli kuralda `guc` verin.
- `p_bootstrap` yalnız `bootstrap=True` ile dolar. Tabanı olmayan (dönem × VIX kovasında < 20 gün; örn. SON × V>30) işlemler `anormal_bps` ortalamasına girmez; sayısı `notlar` içinde `anormal_eksik=k`.
- `blok_permutasyon` artık hiçbir günü yerinde bırakmaz (≤ 20 günlük hücreler hariç); eski sürümde IS günlerinin ~%10'u yerinde kalıyordu.

## Ana ajan düzeltmeleri (22.11.2026, kod denetiminden sonra)

- `SEMA`'ya `t_anormal` eklendi: anormal getirinin tarihe göre kümelenmiş t'si. Tek yönlü (yalnız uzun ya da yalnız kısa) kurallarda karar bu sütunla birlikte verilir.
- Anormal getiri tabanı: dönem × VIX kovası hücresinde 20'den az gözlem varsa aynı VIX kovasının bütün dönemlerdeki havuzlanmış ortalaması kullanılır (son dönem × VIX > 30 işlemleri artık düşmüyor).
- `guc` verilmezse portföy tavanındaki eşitlik sabit tohumlu rastgele sırayla bozulur (sütun sırasıyla değil). Çok hedefli kurallarda yine de `guc` verin.
- Karar ölçüsü: tek hedefli kuralda `t_olcekli`; çok hedefli kuralda `t_kume` ve `p_bootstrap`. Adaylarda `bootstrap=True` kullanın.
- Önbellekten dönen nesneleri (`getiri()`, `beta()`, `rejim()` vb.) yerinde değiştirmeyin; kopya alın.
- Testler: `python3 -I test_motor.py` (18/18) ve `python3 -I test_denetim.py` (54/54) düzeltmelerden sonra geçiyor.
- Maliyet duyarlılığı için ek komisyon senaryosu `"muzayede"`: kapanış/açılış müzayedesi emri (MOC/MOO). Bacak maliyeti yalnız komisyon (1,5 bps); hacim kademesi ve VIX çarpanı yok. Varsayılan senaryolara dahil değildir; `degerlendir(..., komisyon=("hisse","muzayede"))` gibi açıkça istenir. İşlem listesinde `net_muzayede` sütunu her zaman bulunur.
