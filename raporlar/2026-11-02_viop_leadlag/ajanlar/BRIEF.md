# ORTAK BRİFİNG — VİOP pay vadelisi olan 47 BIST şirketinin dış sürücüleri (lead-lag + korelasyon)
Tarih: 31.10.2026 (Cumartesi). Son veri: 30.10.2026 kapanışı.

## Kullanıcının isteği (özet)
VİOP'ta pay vadelisi olan Türk şirketlerinin uluslararası endekslerden, emtialardan, şirketlerden ve AKLA GELEN/GELMEYEN her şeyden
nasıl etkilendiğini bul. GERÇEK korelasyon ve lead-lag ilişkilerini backtest ile tespit et. Bir ihtimali ELEME, zayıfsa DÜŞÜK GÜVEN etiketi koy.
Her ilişki için TradingView ticker kodu ver. ÇİN BORSALARI TradingView'da kullanıcıda AÇILMIYOR (SSE:, SZSE:, SHFE:, DCE:, ZCE:, CFFEX:, INE:, GFEX:;
HKEX: belirsiz -> 'açılmayabilir' notu ve alternatif ver). Bunların yerine test edilmiş alternatif ver (ör. ABD'de işlem gören ETF, COMEX/SGX vadelisi, ADR).
Kullanıcı tercihi: doğruluk > hız; kendi bulgunu eleştir; korelasyon ≠ nedensellik; sahte kesinlik yok; rakamla konuş.

## 47 VİOP pay vadelisi dayanağı (BIST bülteni 30.10.2026, SSF segmenti)
AEFES, AKBNK, AKSEN, ALARK, ARCLK, ASELS, ASTOR, BIMAS, BRSAN, CIMSA, DOAS, DOHOL, EKGYO, ENJSA, ENKAI, EREGL, FROTO, GARAN, GUBRF, HALKB, HEKTS, ISCTR, KCHOL, KRDMD, MGROS, ODAS, OYAKC, PETKM, PGSUS, SAHOL, SASA, SISE, SOKM, TAVHL, TCELL, THYAO, TKFEN, TOASO, TRALT, TRMET, TSKB, TTKOM, TUPRS, ULKER, VAKBN, VESTL, YKBNK

Not: KOZAL -> TRALT (Türk Altın), KOZAA -> TRMET (TR Anadolu Metal). Yahoo: <KOD>.IS. VİOP endeks vadelileri: XU030, XLBNK (likit banka), X10XB, XSD25.

## Veri (HER ŞEY HAZIR, yeniden indirme yapma; eksik sembol gerekiyorsa ydl.fetch ile indir)
- Kod dizini: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code  (ll.py = ortak kütüphane, ydl.py = Yahoo indirici, universe.py = evren). **ll.py / ydl.py / universe.py dosyalarını DEĞİŞTİRME** (kopyalayıp kendi dizininde değiştirebilirsin).
- Kullanım: `import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/code'); import ll`  -> ll.ret('THYAO'), ll.ret('BZ=F'), ll.decomp('THYAO') (cc/gap/intra), ll.ccf(a,b), ll.partial_corr, ll.backtest, ll.fdr, ll.snap_daily(sym,'15:00') (saatlik), ll.summarize_pair. ll.py başındaki ZAMANLAMA KONVANSİYONU'nu MUTLAKA oku.
- Günlük veri: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/daily/<SYM>.parquet (~1.000 sembol, 2000+). Katalog: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/catalog.csv (sym, group, name, ccy, exch, tz, first, n, zero_frac).
- Hazır panel: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/panel_ret_bistcal.parquet = tüm sembollerin BIST takvimine oturtulmuş günlük log getirileri (2005+). BIST dışı sembolde tatil günleri 0 getiri (ffill) olur -> zero_frac'a dikkat.
- BIST gap/gün-içi panel: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/panel_decomp_bist.parquet (MultiIndex sütun (hisse, cc|gap|intra), 2014+; 2014 öncesi Yahoo açılış verisi bozuk).
- Saatlik (60m, ~2023-11'den beri): /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/h1/  ve 5 dakikalık (son 60 gün): /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/m5/ — 47 hisse + XU030/XU100/XBANK/XUSIN/XHOLD/XLBNK + ~130 ana sürücü (ES=F, NQ=F, BZ=F, GC=F, TRY=X, ^GDAXI, TUR, TKC, BTC-USD ...). Liste: `ls /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/h1`.
  Bar zaman damgası = bar başlangıcı (UTC). BIST barları 06:30..14:30 UTC + 15:00 kapanış seansı.
- Ek sembol: `import ydl; ydl.fetch('SYM','daily'|'h1'|'m5')` (nazik ol; toplu indirmede 0,2 sn bekle).
- Saat dilimi: BIST kapanışı 15:00 UTC (18:00 TSİ). ABD kapanışı 20:00 UTC (yaz) / 21:00 UTC (kış). Avrupa 15:30/16:30 UTC. Asya 06:00–08:00 UTC.

## METODOLOJİ STANDARDI (herkes uyacak)
1. Getiri bazında çalış (seviye korelasyonu YASAK; ancak eşbütünleşme/oran analizi yapıyorsan açıkça belirt).
2. Her ilişki için ayrı ayrı raporla:
   a) SENKRON: corr(hisse_t, sürücü_t) tam dönem + son 3y + son 1y; XU100 kontrollü KISMİ korelasyon (hisseye özgü maruziyet mi, yoksa sadece piyasa mı?); beta.
   b) ÖNCÜLÜK (lead): sürücü_{t-1} -> hisse_t. MUTLAKA gap ve gün-içi olarak ayrıştır (ll.decomp). ABD/vadeli kapanışlı sürücülerde lag-1'in çoğu
      'eşzamansız kapanış' kaynaklıdır ve açılışta fiyatlanır -> BU İŞLENEBİLİR DEĞİLDİR (açılıştan önce pozisyon alamazsın; VİOP akşam seansı hariç).
      Gerçek/işlenebilir öncülük = sürücü bilgisi bilindikten SONRA girilen pozisyonun kazanması (ör. sürücü_{t-1} -> hisse gün-içi_t, veya t+2..t+5 sürüklenme).
   c) Hisse -> sürücü yönünü (ters nedensellik / BIST'in önde olması) de kontrol et.
3. Stabilite: yıllara göre korelasyon, 250g kayan korelasyon, iki yarı / IS (2014–2020) vs OOS (2021–2026) aynı işaret mi? Rejimler: 2018 kur krizi, 2021 Aralık, 2023 Haziran ortodoks dönüş, Mart 2025 (İmamoğlu şoku), Eylül–Ekim 2026 fon krizi.
4. Çoklu test: çok sayıda çift test ediyorsan Benjamini-Hochberg (ll.fdr) uygula ve kaç test yaptığını yaz.
5. Backtest: look-ahead YOK (sinyal pozisyondan önce bilinmeli; ABD kapanışı BIST kapanışından sonradır!). Maliyet: VİOP pay vadelisi için gidiş-dönüş ~8–15 bps (spread+komisyon) varsay ve hassasiyet ver. IS/OOS ayrı raporla. Yıllara göre kırılım.
6. TL vs USD: BIST getirileri TL. Küresel sürücülerle ilişki TL kurundan kirlenebilir; gerekirse USD bazlı (r_TL − r_USDTRY) ile de test et.
7. Veri tuzakları: Yahoo BIST verisinde bedelsiz/bölünme sıçramaları (|r|>%10,5 zaten NaN), vadeli roll sıçramaları, tatil ffill sıfırları, bayat fiyatlı illikit seriler (HRC=F %50 sıfır), hacimsiz günler.
8. GÜVEN ETİKETİ (tüm ajanlar aynı ölçeği kullanır):
   - YÜKSEK: makul ekonomik mekanizma + anlamlı büyüklük (senkron |corr|≥0,30 veya kısmi |pc|≥0,15; öncülükte |t|≥3) + yılların ≥%75'inde aynı işaret + IS ve OOS aynı işaret ve anlamlı + (çoklu testteyse) FDR'den geçer.
   - ORTA: mekanizma var, tam dönem anlamlı, OOS aynı işaret ama daha zayıf / istikrarsız.
   - DÜŞÜK: mekanizma makul ama istatistik zayıf/tutarsız; VEYA istatistik var ama mekanizma şüpheli; VEYA kısa örneklem.
   - ÇOK DÜŞÜK / SPEKÜLATİF: hipotez; veri yok/test edilemedi veya test başarısız ama mantıksal olarak dışlanamıyor. (ELEME YOK — listede kalır.)
9. TradingView: Her sürücü için TradingView ticker ADAYI yaz (ör. Yahoo BZ=F -> TV 'ICEEUR:BRN1!' veya 'TVC:UKOIL'; ^GSPC -> 'SP:SPX'; ES=F -> 'CME_MINI:ES1!'; TRY=X -> 'FX:USDTRY'; GC=F -> 'COMEX:GC1!'/'TVC:GOLD'; BIST hissesi -> 'BIST:THYAO').
   Emin değilsen '?' koy; ayrı bir ajan ticker'ları doğruluyor. Çin borsası ticker'ı VERME (alternatif ver).

## ÇIKTI FORMATI (zorunlu)
- Rapor: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/r1_<ajanadı>.md (Türkçe; önce net bulgular tablosu, sonra yöntem, kanıt, karşı argümanlar, sınırlamalar).
- Bulgular CSV: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/f_<ajanadı>.csv sütunları:
  stock,driver_yahoo,driver_desc,tv_ticker,relation,lag,corr_full,corr_3y,corr_1y,pcorr_xu100,beta,t_stat,gap_corr,intra_corr,is_oos,bt_oos_sharpe,bt_oos_mean_bps,n,confidence,mechanism,notes
  relation ∈ {sync, lead_gap, lead_intra, lead_multiday, reverse, regime, event, intraday_minutes, hypothesis}
- Kod: /tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_<ajanadı>/ altına (çalıştırılabilir, yeniden üretilebilir).
- Son mesajın (bana dönen) ≤ 500 kelime olsun: en güçlü 10 bulgu (güven etiketiyle), en önemli olumsuz bulgular, açık sorular. Ayrıntılar dosyada.
