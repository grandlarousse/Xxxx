# A7 — gün içi zamanlama ve dolum doğrulaması (aday üretmez; T3 = keşif)

Dönem: 2023-12-21 → 2025-06-30 (378 gün, 36 XELKT üyesi; iki kronolojik yarı). Kod: `kod/a7_gunici/run.sh <panel>`.

**SAPMA / veri sınırı.** `panel_dev`'de hisselerin 5 dakikalık verisi yok; snap'teki `p_1750` gerçekte 17:30 fiyatıdır. Hisselerde iki sınır ölçüldü: **17:30** (alt sınır) ve **18:00 son sürekli işlem fiyatı** (üst sınır; yalnız yaz saati ayları, 197 gün). Gerçek 17:50 yalnız XELKT endeksinde var (5 dk, 2017–2025/06).
**Veri kusuru (D2):** Yahoo gün içi fiyatları nakit temettü için de küçültülmüş; hisse-günlerin %21'inde fiyat medyan 8 bps düşük. `vekil.yahoo_artik()` düzeltir; düzeltilmezse tavan kilidi sayımı yanlış çıkar.

## T1 — 17:50 vekili (`a7_vekil_tablosu.csv`, `a7_vekil_tablosu_bant.csv`)

| | korelasyon | medyan fark | \|r\| ≥ %3 yakalama / kesinlik | z ≥ 2 |
|---|---|---|---|---|
| Hisse havuzu, 17:30 | 0,941 | 39 bps | 0,75 / 0,87 | 0,76 / 0,86 |
| Hisse havuzu, 18:00 son | 0,988 | 17 bps | 0,89 / 0,95 | 0,90 / 0,95 |
| XELKT, 17:30 (2017–25) | 0,967 | 24 bps | 0,75 / 0,86 | 0,72 / 0,91 |
| XELKT, **17:50** (2017–25) | 0,986 | 17 bps | 0,88 / 0,93 | 0,86 / 0,94 |
| XU030, 17:00 (2017–25) | 0,925 | 32 bps | 0,58 / 0,86 | 0,62 / 0,86 |

- Beklenti (%85–95 yakalama) hisselerde **tutmuyor**: 17:30'da %75, 18:00'de bile %89. Gerçek 17:50 için tahmin %83–87 (XELKT'deki 17:30→17:50 iyileşmesinden; doğrulanmadı).
- Eşiğe uzaklık belirleyici: 17:30'da eşiğin 0–25 bps üstündeki sinyalin %63'ü, ≥ 100 bps üstündekinin %96'sı kapanışta da geçerli. 18:00'de ≥ 50 bps üstü %98. İki yarıda sonuç aynı.

## T2 — kapanış seansı

- **Fiyat sapması** (`a7_kapanis_sapma.csv`, kilitsiz kapanışlar): 17:30 → kapanış medyan |sapma| 40 bps, %95'lik 180 bps, %16'sı > 100 bps. 18:00 son fiyat → kapanış (salt kapanış seansı): medyan 18 bps, %95'lik 86 bps; bir fiyat adımı ≈ 8 bps. AKSEN/ENJSA/ODAS: 21 / 22 / 20 bps.
- **Kilit** (`a7_kilit_gecis.csv`, `a7_kilit_riski.csv`): 209 tavan kapanışının %69'u 17:30'da zaten tavandaydı, %31'i sonradan oluştu; 18:00'de %95'i tavanda (kapanış seansında oluşan yalnız 6/121). Bozulma nadir: 17:30'da tavanda olanın %98'i tavanda kapanır. Taban: 71 kapanışın %73'ü 17:30'da tabanda; 17:30'da tabanda olanın %15'i kurtulur.
- Dolum riski: 17:30'da tavanda olmayan ama +%7–9'daki hissenin %22'si, ≥ +%9'dakinin %56'sı tavanda kapanır (alım dolmaz); +%5–7'de %3.
- **Hacim** (`a7_kapanis_hacim.csv`; dolaylı tahmin, barlarda kapanış seansı yok): kapanış seansı günlük hacmin yaklaşık **%2,5–4,5**'i (üye medyanı %3,7; ≈ 2,4 milyon TL). E9'daki “%1 günlük hacim” sınırı kapanış seansının medyan **%27**'sine denk geliyor (AKSEN %16, ENJSA %24, ODAS %22): tek fiyat seansı için büyük. Öneri: pozisyon ≤ kapanış seansı hacminin %10'u (medyan ≈ 240 bin TL; AKSEN ≈ 630, ENJSA ≈ 710, ODAS ≈ 530 bin TL).

## T3 — keşif (`a7_kesif.csv`; 35 test, BH q = 0,10'dan 5'i geçti)

- XU030 17:00 → kapanış getirisi → sektör sepeti ertesi gün: f1 katsayı 0,48 (t = 3,5), etkinin tamamı gün içinde (oc1 t = 3,3; gece ≈ 0). İki yarıda da pozitif; **2017–2022'de yok** (t = 0,15), 2023–2025/06'da t = 2,0. Dönemsel; aday değil.
- Kapanış seansı göreli sapması (kapanış / 18:00 son − 1, eksi sektör ortalaması) → ertesi gece: katsayı −0,13 (t = −4,0); uç beşte birlikler arası −12,5 bps (t = −3,8), iki yarıda da. Kısmi geri dönüş var ama maliyetin altında: sinyal değil, **dolum uyarısı**.
- Hissenin kendi 16:30 → kapanış getirisi → ertesi gece −11 bps (t = −3,4); günün daha erken bölümü ise devam ediyor (t = 4,6).
- XELKT ve BIG sepetinin son saati: anlamlı değil.

## Araç: `kod/a7_gunici/vekil.py`

```
python3 -I vekil.py <panel_full> ../a4_olay/rules.py --bas 2025-07-01 --cikti a4_vekil.csv
```
Her gün yalnız o günün kapanışa bağlı girdilerini (getiri, kilit, endeks, hacim) 17:50 fiyatıyla değiştirip `build()`'i yeniden çağırır; kesinlik, yakalama, kaçan/yanlış sinyallerin ortalama fazla getirisi ve “sinyal var ama kapanış kilitli” sayısını verir. Öz-denetim (vekil = kapanış) %100 örtüşüyor. Örnek kurallarda (`ornek_rules.py`, yalnız örtüşme) yakalama 0,77–0,88, kesinlik 0,83–0,99.

**Zayıflıklar:** VİOP uzlaşması vekillenemiyor (A6 iyimser kalır); kapanış hacmi dolaylı; dönem 18 ay; diğer ajanların kuralları kör protokol gereği burada çalıştırılmadı.
