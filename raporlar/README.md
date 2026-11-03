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

# Nezaket örüntüsünü kırmak: aile kliniği, DUS uzmanlığı ve Kanada (03.11.2026)

Klasör: `2026-11-03_dishekimligi_isyeri/`

- `RAPOR.md`: Sentez. Beş hüküm, şimdi yapılacak üç şey, teşhis (üç tür kötü muamele, nezaket ve yatıştırma farkı), üç senaryo için öneriler, uzlaşı paketleri ve kelimesi kelimesine cümleler, senaryolar arası etkileşim, ana ajanın kendi okuması, oylama sonucu, düzeltilen hatalar, kanıt sınırları.
- `ajanlar/`: Brif, 8 araştırma raporu (`r1_*`), 5 panelistin iki turu (`t1_*`, `t2_*`), moderatör önermeleri, hakem kararı (`h_konsensus.md`), boşluk dosyaları (`b*`) ve ikinci tur tamamlamaları.
- `dogrulama/`: Her araştırma dosyası için bağımsız çürütme denemesi ve ikinci tur yeniden kontrol (`d_tekrar.md`).

Tıbbi, hukuki ya da göçmenlik tavsiyesi değildir.
