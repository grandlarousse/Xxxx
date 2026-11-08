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

# Altın: VİOP Ons Altın (F_XAUUSD) ve Midas ETF'leri ile 1–3–5 günlük trade, fiyat tahmini ve lead-lag (07–08.11.2026)

Klasör: `2026-11-07_xauusd_altin/`

- `RAPOR.md`: Ana sentez.
  - Net cevap.
  - Kontrat, saat ve maliyet gerçekleri: VİOP, Midas ABD ETF'leri ve BIST BYF'leri yan yana.
  - Altından kim, nasıl kazanıyor.
  - 1–3–5 günlük strateji aileleri: literatür ve bizim test.
  - VİOP lead-lag sonuçları ve Midas ETF cephesi.
  - Dünya ve Türkiye altın fiyatının yordanması.
  - Günlük rutin, risk ve boyut, sınırlamalar.
- `sentez/HAKEM.md`: 7.446 testin çoklu test düzeltmesi, 65 iddianın son güven tablosu (yeniden üretici + çürütücü), örtüşme, eşit ağırlıklı birleşim, 09.11.2026 durumu, risk.
- `sinyal/sinyal_altin.py` + `sinyal/KULLANIM.md`: Ayakta kalan 11 kuralın günlük sinyal betiği. VİOP için 18:00 TSİ, Midas için 15:00 ET. Bağımsız denetimden geçti.
- `analiz/`, `arastirma/`, `dogrulama/`, `kod/`, `veri_ozet/`: Ajan raporları, araştırma ve doğrulama notları, kod, test kayıtları.

Yatırım tavsiyesi değildir.
