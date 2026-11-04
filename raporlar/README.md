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

Yatırım tavsiyesi değildir.

---

# Instagram tarih sayfası: görsel telif riski ve yasal görsel kaynakları (04.11.2026)

Klasör: `2026-11-04_instagram_gorsel_telif/`

- `RAPOR.md`: Sentez raporu. İçinde şunlar var:
  - Kısa cevap ve yıl eşiği (Türkiye ve ABD)
  - Kamu malı eserin kopyası sorunu ve Türk kurumlarının koşulları
  - Görsel türüne göre risk tablosu
  - Kaynaklar
  - Varna örneği
  - Günlük iş akışı ve atıf şablonları
  - Instagram özgünlük kuralı
  - Bildirim gelirse yapılacaklar
  - Bilinmeyenler
- `kaynaklar.csv`: 46 görsel kaynağı. Her biri için lisans, ticari kullanım, atıf, dikkat notu ve doğrulama durumu.
- `varna_gorselleri.csv`: Varna Savaşı için lisansı kontrol edilmiş 21 görsel ve kullanılmaması gereken 4 dosya. Her biri için Commons adresi, çözünürlük ve hazır atıf satırı.
- `ajanlar/`: Altı başlığın ham araştırma bulguları ve her bulgunun yanında çürütme ajanının kararı.

Hukuki tavsiye değildir.
