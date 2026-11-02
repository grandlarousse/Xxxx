# EK BRİFİNG — YURT İÇİ (ULUSAL) LEAD-LAG TURU (02.11.2026)
Önce ana brifingi oku: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/BRIEF.md (metodoloji standardı, güven etiketleri, CSV formatı aynen geçerli). Bu dosya ekleri ve değişiklikleri içerir.

## Kullanıcının yeni isteği
"Ulusal endekslerle, ulusal hisselerle de lead-lag'lerini hepsinin analiz et. Sadece uluslararası değil." Hedef yine 47 VİOP pay vadelisi dayanağı; sürücüler artık BIST endeksleri, diğer BIST hisseleri, yurt içi makro/piyasa değişkenleri, VİOP verisi, akışlar.
Kullanıcı kotayı yükseltti: TASARRUF YOK, kapsamlı ve titiz ol. Ama CPU 4 çekirdek ve ~12 ajanla paylaşılıyor: ağır hesapları vektörize et ve 'nice -n 10' ile çalıştır.

## 1. turdan bilinenler (uluslararası; bunları tekrar etme, gerekirse referans ver)
- ABD/vadeli sürücülerin t-1 etkisi neredeyse tamamen BIST AÇILIŞ GAP'inde fiyatlanıyor; gün-içi kalıntı yok (612 gün-içi testte 0 FDR; 5 dk'da gecikme yok).
- VİOP akşam seansı (19:00–23:00 TSİ): sadece endeks vadelileri (XU030, XLBNK, X10XB, XSD25) + ons altın/gümüş/platin/paladyum + bakır. PAY VADELİLERİ ve USD/TL YOK (BIST duyuru 30572, 19.11.2024).
- Hisseye özgü (XU100 kontrollü) dış bağlar küçük; en güçlüleri yurt içi kümeler: EREGL–ISDMR–KRDMD, TRALT–TRMET–TRENJ, CIMSA–OYAKC–çimento kümesi, ASTOR–EUPWR–GESAN, MGROS–SOKM–BIMAS, THYAO–PGSUS (pc 0,51), SAHOL–AKBNK (0,24), AEFES–CCOLA, GUBRF–BAGFS, TKFEN–ENKAI, banka↔sanayi rotasyonu (SISE/BIMAS–XBANK negatif). BUNLARI SENKRON olarak biliyoruz; SEN LEAD-LAG (öncülük) boyutunu, gün-içini ve işlenebilirliği araştır.
- Gap/gün-içi: XU030 gap'i 13/13 yıl pozitif, gün-içi 11/13 yıl negatif; kendi gap'in gün-içinde kısmi geri dönüşü (CIMSA/OYAKC'de |gap|>%1 fade OOS +40–64 bps, açılış dolumu iyimser varsayım).

## 2. VERİ DÜZELTMELERİ (ll.py'de uygulandı — mutlaka bil)
- FX_FIX: Yahoo '=X' kur serilerinin günlük kapanışı t günü 00:00 UTC idi → 1 gün kaydırılarak düzeltildi (ll.daily/ll.ret otomatik). Kendi kodunda tekrar kaydırma.
- Simetrik temizlik: fiyat bazında +%10,5 üstü / −%10,5 altı BIST günleri NaN (ll._bad). TABAN günleri artık korunuyor.
- Saatlik BIST barları :30'da başlar (06:30..14:30 UTC) + 15:00 kapanış seansı barı; sürücü barları :00'da. Kış aylarında 14:30 barı eksik olabilir. 'Hisse önde' gibi görünen saatlik sonuçlar hizalama artefaktı olabilir — BIST-BIST karşılaştırmalarında iki seri de aynı bar ızgarasında, sorun yok; ama bayat son fiyat (illikit hisse) sahte lead-lag üretir.
- Endekslerde h1 ilk barın açılışı önceki kapanış olabilir; açılışı günlük veriden al.

## 3. Yeni veri
- Günlük: 223 BIST sembolü (≈178 hisse + ≈45 endeks: XU030, XU050, XU100, XUTUM, XYUZO (100 hariç 30), XTUMY, XKTUM, XK030, XK100, XBANK, XLBNK, X10XB, XHOLD, XUSIN, XUMAL, XUHIZ, XUTEK, XULAS, XELKT, XGIDA, XKMYA, XMANA, XMADN, XTAST, XTEKS, XINSA, XKAGT, XBLSM, XILTM, XTCRT, XGMYO, XSGRT, XYORT, XFINK, XAKUR, XSPOR, XTRZM, XTMTU (temettü), XHARZ (halka arz), XSD25, XUSRD, XKURY, XBANA, XSIST, XMESY, XYLDZ). Panel güncellendi: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/panel_ret_bistcal.parquet (catalog.csv'de group='VIOP' veya 'BIST_other').
- Saatlik: 47 VİOP hissesi + 6 endeks + BIST_EXTRA 55 sembol (/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/h1). 5 dk (son 60 gün): aynı set (/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/m5; ek semboller şu an iniyor). Eksik BIST sembolünü ydl.fetch('XXXX.IS','h1'|'m5') ile indir.
- VİOP günlük bülteni: https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv (windows-1254, ';' ayraç; ayrıştırıcı örneği: /home/user/Xxxx/raporlar/hesaplar/opsiyon/viop_parse.py; son iki gün /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/dl/viop/ altında). Geçmiş günleri gerektiği kadar indir (nazik ol: istek arası ≥0,3 sn), ortak dizine kaydet: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/viop/ (aynı günü iki kez indirme — dosya varsa atla).
- Mevcut uluslararası bulgular: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/master_findings_r1.csv (tüm f_*.csv birleşik) ve /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/r1_*.md.

## 4. Yurt içi lead-lag'e özgü tuzaklar (mutlaka kontrol et)
1. **Bayat fiyat (non-trading) etkisi:** İllikit hisse/endeks bileşenleri gecikmeli fiyatlanır → büyükten küçüğe sahte 'öncülük' (Lo–MacKinlay). Hacim/işlem sayısı filtrele, likit alt örneklemde tekrar et; endeks hesaplama gecikmesine dikkat.
2. **Mekanik içerme:** XU030/XU100/sektör endeksi hisseyi zaten içerir → senkron korelasyon şişer. Mümkünse hisse-hariç endeks (ör. XU030 − w·hisse, ağırlık yaklaşık) veya XYUZO / başka sektör kullan; en azından bunu not et.
3. **Kendi gecikmesi ve piyasa momentumu:** A_{t-1} → B_t testinde B_{t-1} ve XU100_{t-1}'i KONTROL ET; aksi halde ortak otokorelasyon sahte lead üretir.
4. **Bid-ask sıçraması:** 5 dk ve saatlik getirilerde negatif otokorelasyon mekanik; kendi lag'ini kontrol et, maliyeti (VİOP pay vadelisinde tik/spread) gerçekçi koy.
5. **Açılış ve kapanış seansları:** Tek fiyatlı açılış/kapanış emir toplama; açılış fiyatından dolum her zaman mümkün değil. Gap-fade gibi stratejilerde bunu tartış.
6. **Çoklu test:** 223×47×lag... yüz binlerce test → BH-FDR + IS (2014–2020) / OOS (2021–2026) replikasyonu + kaydırılmış/karıştırılmış null.
7. **Rejimler:** 2018, Ara 2021 (KKM), Haz 2023, Mar 2025, Eyl–Eki 2026 fon krizi (tasfiyedeki fonlar likit olmayan küçük hisseleri sattı → küçükler/büyükler ayrışması).
8. **İşlenebilirlik:** Sonuç VİOP pay vadelisiyle mi (47 hisse) işlenir, spotla mı? Lider hisse VİOP'ta olmayabilir (sinyal kaynağı olarak sorun değil). VİOP pay vadelilerinin çoğu illikit: bulgunu likiditeye göre değerlendir.

## 5. Çıktı formatı
- Rapor: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/ry_<ajanadı>.md ; bulgular: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/f_y_<ajanadı>.csv (ana brifingdeki sütunlar aynen; driver_yahoo = BIST kodu ör. 'XBANK.IS'; tv_ticker = 'BIST:XBANK' gibi; relation'a ek değerler serbest: lead_hourly, lead_5m, lead_auction, flow, liquidity). Kod: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_y_<ajanadı>/.
- Son mesaj ≤600 kelime: en güçlü 10 bulgu (güven etiketiyle), olumsuz bulgular, açık sorular.
