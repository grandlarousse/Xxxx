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

# İkinci DUS ve INBDE: 2027 hazırlık stratejisi (03.11.2026)

Klasör: `2026-11-03_dus_inbde_strateji/`

- `RAPOR.md`: Sentez. Kullanıcının 13 sorusunun cevabı (DUS hazırlığı, dershanelerin faydası ve triajı, ikinci maratonda neyin değişeceği, optimum sprint süresi; INBDE/Kanada yolu, uygulamalar, geçme oranları, süre, Mart mı Mayıs mı, INBDE çalışmasının DUS'a faydası, arkadaşların neden daha yüksek net yaptığı). Dal A (CODA akrediteli Yeditepe 2024+ mezunu) / Dal B ayrımı, birleşik takvim, oy tablosu, azınlık görüşleri, doğrulamada düzeltilen hatalar, kaynaklar.
- `EYLEM_PLANI.md`: Uygulanabilir plan: bu hafta, ay ay takvim, haftalık şablon, metrikler, tarihli karar noktaları.
- `ajanlar/`: `00_koordinator_notlari.md`, `00_bulgu_ozeti.md`, 9 araştırma dosyası (`r0_*`), 5 stratejistin 1. tur (`r1_*`) ve 2. tur (`r2_*`, çapraz sorgu ve oylar) metinleri.
- `dogrulama/`: 3 bağımsız doğrulayıcının notları (Türkiye/DUS, ABD/Kanada, satıcı/bilim/AI).

Kariyer veya hukuk danışmanlığı değildir; tarih, ücret ve kurallar resmi kaynaklardan tekrar kontrol edilmelidir.
