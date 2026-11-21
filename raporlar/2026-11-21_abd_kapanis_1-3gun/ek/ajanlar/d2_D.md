# D · veri paneli

araç: 37/40

## Özet

Günlük panel kuruldu. 470 kodun hepsi geldi: 469'u kendi koduyla, BITF yerine KEEL. Satırlar SPY'ın Yahoo veri günleri: 5.507 NYSE işlem günü, 2005-01-03 → 2026-11-20.

pyarrow kurulu olmadığı için alan başına bir pandas pickle yazıldı: open, high, low, close, adjclose, volume (her biri ~20 MB). yukle.panel() adjopen = open × adjclose/close değerini de hesaplıyor. Farklı takvimli seriler borsanın yerel takvim tarihine göre hizalandı; ileri doldurma yapılmadı.

Önceki ajandan kalan ham JSON'lardan 3'ü yarım yazılmıştı (ABBV, PEP, SHY). Bunlar silinip yeniden indirildi. İndirici artık boş seriyi başarısız sayıyor ve dosyaları atomik yazıyor.

Ana ajanın verdiği referans değerlerin hepsi tuttu:
- NVDA: son kapanış 125,53; 52 haftalık zirve kapanışı 239,24 (2026-10-06).
- ^GSPC: son 6.910,39.
- SMH: zirve 668,91 (2026-06-22), son 400,06.

Diğer çıktılar:
- **evren.csv:** 470 satır. 193 ETF, 231 hisse, 28 endeks, 11 vadeli, 4 döviz, 3 kripto. Ek sütun: borsa_tz.
- **veri_kalite.csv:** kod başına eksik gün, |getiri| > %40 günleri (bölünme işaretiyle), bölünme listesi, adjclose/close oranındaki sıçramalar, son tarih, sıfır hacimli gün, OHLC tutarsızlığı.
- **bilanco_tarihleri.csv:** 212 hisse için 13.543 adet 8-K 2.02 kaydı (2004-12 → 2026-11). Seans dağılımı: 6.793 kapanış sonrası, 5.532 açılış öncesi, 1.218 seans içi. Bilanço tarihi olmayan 19 hissenin her biri boş satır ve notla dosyada duruyor.
- **dix_gex.csv:** yeniden indirildi; önceki kopyayla bayt bayt aynı. 2011-05-02 → 2026-11-20.

Kaldıraç tablosunu 2022–2026 yıllık betayla (dayanağa göre eğim) kontrol ettim. Buna göre TSLQ −1'den −2'ye, BITX'in dayanağı BTC-USD'den IBIT'e çevrildi. Emtia ürünlerinin dayanağı evrendeki ETF'lerdir (USO, UNG, SLV, GLD); UVXY ve SVXY'nin dayanağı VXX.

## Dosyalar

- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/veri_indir.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/panel_kur.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/bilanco.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/evren_tanim.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/yukle.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/BENIOKU.md
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/evren.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/veri_kalite.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/bilanco_tarihleri.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/dix_gex.csv
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel/open.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel/high.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel/low.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel/close.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel/adjclose.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel/volume.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ham/

## Yükleme örneği

import sys; sys.path.insert(0, "/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod")
from yukle import panel, bilanco, dix_gex, kalite
P = panel()   # keys: open high low close adjclose adjopen volume evren
r = P["adjclose"].pct_change(fill_method=None)
B = bilanco(); D = dix_gex()
# denendi (/tmp dizininden): P['close'].shape == (5507, 470); P['adjopen'].loc['2026-11-20','SPY'] == 713.56

## Başarısız kodlar

Gelmeyen kod yok.

Yerine konan tek kod: BITF → KEEL. Yahoo BITF için boş seri döndürüyor (firstTradeDate 2026-07, timestamp yok). Yahoo'da KEEL'in adı "Keel Infrastructure Corp."; Bitfarms'ın yeni adı olduğu varsayıldı, bağımsız olarak doğrulanmadı. Panelde ve bilanco_tarihleri.csv'de kod KEEL olarak geçiyor; evren.csv notunda "eski kod BITF" yazıyor.

SQ→XYZ ve GOLD→B değişikliğine gerek kalmadı; XYZ ve B doğrudan geldi.

SEC tarafı: www.sec.gov/files/company_tickers.json 403 ("Request Rate Threshold Exceeded") döndürdü, 5 denemede de gelmedi. Kod→CIK eşlemesi bunun yerine efts.sec.gov varlık aramasıyla yapıldı. data.sec.gov submissions sorunsuz çalıştı.

## Kalite özeti

**Son tarih:** 2026-11-20 olmayan tek kod ^BVSP (son 2026-11-19; 20 Kasım Brezilya tatili). Kripto hamı 2026-11-21 kısmi barını içeriyor; panelde yok.

**Eksik gün:** ABD16 kodlarının hiçbirinde ilk tarihten sonra eksik gün yok.

**Bölünme kontrolü:** Yahoo close bölünmeye göre düzeltilmiş. |getiri| > %40 olup aynı gün bölünme kaydı bulunan ve fiyatın düzeltilmediği bir durum çıkmadı. ERX 2020-03-24 (+%40, 1:10) ile UCO 2020-04-21 (−%57, 1:25) gerçek hareketler; ters ürünleri (ERY, SCO) aynı gün ayna hareketi yapıyor. Kaldıraçlı ETF'lerdeki büyük günler (2008–09, 2020-03, 2025-04-09, AGQ/ZSL 2026-01-30, BOIL/KOLD 2026-02-02) ters çiftleriyle tutarlı.

**Şüpheli seriler:**
- Şirket birleşmesi öncesi kabuk ya da penny-stock dönemleri:
  - QUBT 2018 öncesi (170 büyük gün, +%3900).
  - MARA 2012–13.
  - CLSK 2016–18.
  - WULF 2014–2021 (eski Ikonics).
  - KEEL 2019–20.
  - LEU 2011–16 (USEC dönemi).
  - VKTX.
  - BBAI 2023-01-12 (+%261).
- ^IRX: sıfıra yakın getiri nedeniyle 322 "büyük getiri" günü; yüzde getiri anlamsız, fark (seviye değişimi) kullanılmalı.
- CL=F 2020-04-20 negatif fiyat.

**adjclose/close sıçraması:** temettüyle açıklanmayan 33 sıçrama var. Hepsi yıl sonu ya da özel dağıtım: EWT, TAN, ASHR 2015 (+%30), MSTX 2024-12-31 (+%37), KLAC 2014 özel temettü, MS 2007 Discover ayrılması, VST 2016. adjclose bunları içeriyor.

**Sıfır hacimli günler:** SOXS (1.986), TECS (1.269), UVXY (576), QUBT (1.742), WULF (1.185), CLSK, MARA, KEEL. Çoğu ağır ters bölünme düzeltmesinde hacmin sıfıra yuvarlanmasından ya da OTC dönemlerinden kaynaklanıyor; eski hacmi kullanmayın.

**OHLC tutarsızlığı:** GC=F (221), SI=F (207), HG=F (138), BZ=F (53), TRY=X (33).

**2021 sonrası başlayan kodlar (ilk tarih sırasıyla):** SOFI, IONQ, AFRM, RBLX, BBAI, COIN, APP, RGTI, PL, BITQ, OKLO, DUOL, HOOD, TOST, BITO, RIVN, LUNR, IREN, NU, CEG, CRDO, WGMI, SMR, APLD, SOUN, TSLQ, TSLL, CONL, NVDL, MAGS, TLN, BITX, ARM, IBIT, CORZ, ALAB, RDDT, GEV, NNE, TEM, ETHA, MSTX, MSTU, NBIS, CRWV, GLXY, CRCL, FIG, KLAR (49 kod).

**Bilanço tarihi bulunamayanlar:**
- Yabancı ihraççılar (20-F / 40-F / 6-K), 18 kod: TSM, ASML, ARM, NBIS, SPOT, NU, KLAR, CCJ, NIO, XPEV, LI, BABA, PDD, JD, BIDU, NVO, AEM, B.
- KEEL: SEC'te CIK bulunamadı. Bu, KEEL'e geçişten önce BITF için yapılan aramanın sonucu; KEEL için ayrıca aranmadı.
- NNE: 8-K 2.02 yok.
- Kısmi geçmiş, dönemin bir kısmında yabancı ihraççı: SHOP ve IREN (8'er kayıt), CLS (8), TEAM (18), NXPI (31).
- OKLO: son kayıt 2025-03.

## Notlar

1. **Tarih hizası.** Tarih, borsanın yerel takvim tarihidir. ONCE sınıfı (Asya, Avrupa) aynı gün ABD kapanışından önce kapanır. SONRA sınıfının (kripto 00:00 UTC, döviz Londra günü, vadeli 17:00 ET) aynı tarihli değeri ABD kapanışından sonraki bilgiyi içerir. Bu yüzden sinyalde SONRA serilerini t günü ABD16 kapanışıyla aynı anda kullanmak ileriye bakma (look-ahead) hatası olur; bir gün gecikmeli kullanın. ^VIX ve benzerleri 16:15 ET'de kapanır.
2. **Fiyat türleri.** close, open, high ve low yalnız bölünmeye göre düzeltilmiş; getiri için adjclose ya da adjopen kullanın. Gece getirisi = adjopen_t / adjclose_{t−1}. İleri doldurma yok: pct_change(fill_method=None) kullanın, NaN'ı açıkça ele alın.
3. **Kaldıraç tarihçesi.** Yıllık beta kontrolüne göre:
   - TSLL, CONL ve NVDL 2024 başına kadar 1,5×, sonra 2×.
   - TSLQ 2024 ortasına kadar −1×, sonra −2× (evrende −2).
   - MSTX başlangıçta yaklaşık 1,9×.
   - UCO/SCO'nun USO'ya göre betası 2022'de 1,8 iken 2026'da yaklaşık 1,1–1,2'ye düşmüş. UCO ile SCO birbirine ayna; veri hatası değil, endeks ya da dayanak farkı gibi görünüyor, doğrulanmadı.
   - VXX/VIXY'nin ^VIX betası yaklaşık 0,45; ^VIX yalnızca yaklaşık dayanaktır.
   - BITX dayanağı IBIT (beta 2,0); BTC-USD 00:00 UTC kapandığı için uygun değil.
4. **maliyet_bps** = 1,5 / 3 / 7 / 15, kaldıraçlıya +1. Endeks ve dövizde NaN. Vadelide adv kontrat çarpanını içermediği için yaklaşık. Kriptoda adv = Yahoo USD hacmi.
5. **Bilanço kayıtları.** acceptanceDateTime gerçekten UTC; NVDA ile doğrulandı. Yaz/kış saati zoneinfo ile çevrildi.
   - Yarım günlerde kapanış 13:00 kabul edildi (not=yarim_gun_13:00).
   - Hafta sonu ya da tatilde kabul edilen 17 kayıt not=islem_gunu_degil taşıyor (BRK-B Cumartesi açıklamaları gibi).
   - 8-K bülten saatinden geç kabul edilebilir; SEANS_ICI satırlarının bir kısmı aslında açılış öncesi bültendir. ilk_tepki_gunu bundan etkilenmez, açılış/seans ayrımı yapan testlerde dikkat edin.
   - Aynı çeyrekte ön duyuru gibi birden çok 2.02 olabilir; 8-K/A dahil edilmedi.
6. **Hisse evreni.** Panel bugünkü listeden kuruldu, yani hayatta kalanlar yanlılığı (survivorship bias) içerir. Birleşme öncesi kabuk dönemleri olan hisselerde (QUBT, WULF, MARA, CLSK, LEU, KEEL) başlangıç tarihini kendiniz kesin.
7. **Panel konumu.** /tmp scratchpad'de durur, temizlenebilir. Kaybolursa BENIOKU.md'deki dört komutla yeniden üretilir; ham dosyalar varsa indirme atlanır.
8. git commit/push yapılmadı.
