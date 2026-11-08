# BIST VİOP — 5 Ajanlı Yatırım Komitesi (28.10.2026)

- `2026-10-28_viop_komite_raporu.md`: Sentez raporu. Net öneriler, oy tablosu, düzeltilen hatalar, stres testleri, sınırlamalar.
- `ajanlar/`: Ham ajan çıktıları.
  - `00_baseline.md`: Koordinatörün hazırladığı ortak başlangıç verisi. Hataları raporda düzeltildi.
  - `r1_*.md`: 1. tur, ajanların bağımsız fikirleri.
  - `r2_*.md`: 2. tur, çapraz kontrol, oylar ve revizyonlar.
- `hesaplar/`: Ajanların hesap betikleri (Black-76, gerçekleşen volatilite, carry, kur şoku backtest'i, tarihsel benzerler, tetiklenme olasılığı, portföy stres testi).
  - Betikler indirilen veri dosyalarına (Yahoo, Borsa İstanbul bülten CSV'leri) bağlı. Bu veriler repoya eklenmedi.
  - `koordinator/check.py` bağımsız çalışır.

Yatırım tavsiyesi değildir.

---

# VİOP pay vadelisi olan 47 hissenin sürücüleri ve lead-lag analizi (02.11.2026)

Klasör: `2026-11-02_viop_leadlag/`

- `RAPOR.md`: Sentez. Net cevap, varyans ayrıştırması, zamanlama (gap ve gün-içi ayrımı), doğrulanmış öncülükler, yurt içi bağlar, işlenebilir adaylar, karşı argümanlar ve sınırlamalar, düzeltilen veri hataları.
- `HISSE_KARTLARI.md` ve `hisse_kartlari/`: 47 hisse için kart. Her kartta bütün sürücüler, rakamları, güven etiketi (doğrulama sonrası), işlenebilirlik notu ve TradingView kodları var.
- `izleme_listeleri/`: TradingView izleme listeleri. Her hisse için `<KOD>.txt`; hepsi bölümlü olarak `TUM_HISSELER_bolumlu.txt`.
- `viop_surucu_haritasi.html`: Etkileşimli sayfa, tek dosya.
- `tradingview_kodlari.csv`: Yahoo → TradingView eşlemesi (sayfa okunarak doğrulandı).
- `bulgular_tum_ajanlar.csv`, `dogrulama/`, `ajanlar/`, `veri_ozet/`, `hesaplar/`: Ham bulgular, doğrulama notları, ajan raporları, özet veriler ve kod.

Yatırım tavsiyesi değildir.

---

# Kapanıştan kapanışa 1–3 gün tutan VİOP yatırımcısı için pratik liste (04.11.2026)

Klasör: `2026-11-04_kapanis_1-3gun/`

- `PRATIK_LISTE.md`: Ayakta kalan sinyaller (kural, TradingView kodları, beklenti, güven), bu profil için elenenler, risk/hedge kuralları.
- `risk_ve_boyut_tablosu.csv`: 47 pay vadelisi için β, 1/2/3 günlük risk, limit günleri, teminat ve boyut.
- `kod/sinyal.py`, `kod/sahol_akbnk_z.pine`: Günlük SAHOL/AKBNK sinyali ve TradingView göstergesi.
- `notlar/`, `kod/`: Yeniden test ve çürütme notları, araştırma kodu.
- `rehber/tuprs`, `rehber/koza`, `rehber/altin`: TUPRS ← ABD rafinerileri, TRMET/TRALT göreli momentum ve TRALT ← altın için saat saat uygulama rehberi, günlük sinyal betiği ve TradingView göstergesi (derlenmedi).

Yatırım tavsiyesi değildir.

---

# Carl Gustav Jung'un bütün kitapları (05.11.2026)

Klasör: `2026-11-05_jung_kitaplari/` (giriş için klasördeki `README.md`)

- `ajan_ciktilari/`: Alt ajanların çıktıları. 50 kitap raporu (her birinde yazar–hakem tartışma eki), 12 küme sentezi, envanter denetimi, üç bakışlı tartışma ve "Ajanların Ortak Raporu".
- `ana_ajan_analizi/`: Ana ajanın ayrı analizi. Ajan bulgularının denetimi ve güven haritası, külliyat haritası ve 50 eserlik tablo, tartışmanın hakemliği ve Türkçe okuma yolları, düzeltmeler ve açık sorular.

---

# Midas'ta ABD ETF'leriyle 1-3 günlük alım-satım: stratejiler, izleme listesi, lead-lag (07.11.2026)

Klasör: `2026-11-07_midas_etf_1-3gun/`

- `RAPOR.md`: Net cevap, Midas koşulları (komisyon, saatler, MOC yok, PTP riski), denetimden geçen 2 kural (QQQ ve SMH IBS dönüşü), zayıf kanıtlı 10 kural, popüler ama çalışmayanlar (doğalgaz, petrol, altın, VIX, kripto, sektör, takvim), lead-lag sonuçları ve akşam rutini (TR saati).
- `IZLEME_LISTESI.md`: 77 ETF (22 kabul, 55 yedek); kademe (A/B/C), TradingView kodu, maliyet, kural, sürücü ve gerçek zamanlı izleme kodları.
- `kartlar/<SYM>.md`: ETF başına kart: kurallar, ajan, denetçi ve son kontrol rakamları, aynı gün sürücüler, gecikmeli öncüler, gerçek zamanlı izleme (TradingView kodları sayfa okunarak doğrulandı).
- `izleme_listeleri/`: TradingView'a içe aktarılacak listeler (aile bazında ve tümü, bölümlü).
- `kod/sinyal.py`: Akşam kontrol betiği (`--canli` ile kapanış öncesi). `kod/tradingview/*.pine`: IBS ve RSI(2) göstergeleri (derlenmedi).
- `notlar/`, `sonuclar/`, `kod/`: Aile ajanlarının ve bağımsız denetçilerin notları, tablolar, tüm kod. Ham veri repoda yok (`kod/dl.py all`, `kod/temettu_yahoo.py` ile yeniden indirilir); olay takvimleri `data/events/` altında.

Yatırım tavsiyesi değildir.
