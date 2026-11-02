# v_tv — TradingView kod denetimi (bağımsız, şüpheci doğrulayıcı)
Tarih: 02.11.2026 (12:48 UTC). Girdi: 21 `f_*.csv` (13 uluslararası + 8 yurt içi `f_y_*`; son eklenen `f_y_makro_y.csv` 12:37) = **12.459 satır, 1.109 benzersiz `driver_yahoo`, 846 benzersiz TV kodu**; `tv_map.csv` (1.212 satır), `cin_alternatifler.csv` (339 satır).
Çıktı: `out/tv_final.csv` (yahoo, aciklama, tv_kodu, tv_alternatif, durum, not) — **1.214 satır**. Kod: `out/code_v_tv/`.

## 1. Net sonuçlar
| Ölçüt | Sonuç |
|---|---|
| tv_final kapsamı | f_*.csv'deki **1.109 sürücü dizgesinin 1.109'u** `yahoo` sütununda birebir var (birleştirme anahtarı = f_ dosyasındaki `driver_yahoo`), ayrıca bileşik sürücülerin atomik bileşenleri, 47 hisse (`BIST:<KOD>`), 47 pay vadelisi (`VIOP:<KOD>1!` → `BIST:<KOD>1!`), 4 endeks vadelisi + 9 döviz/metal vadelisi |
| tv_final'deki kodların bağımsız okunması | tv_kodu + tv_alternatif'teki **943 benzersiz kodun 943'ü** halka açık `tradingview.com/symbols/<BORSA>-<SEMBOL>/` sayfasından bu denetimde **HTTP 200** ile okundu (kendi ayrıştırıcım; `pro_symbol` + açıklama + ISIN kaydı) |
| Rastgele 40 VERIFIED_PAGE (WebFetch) | **40/40 teyit** (sembol, şirket adı, ISIN tv_map ile uyumlu). Örneklem `random_state=20261102`; sıfır hata → gerçek hata oranı üst sınırı ≈ %7,5 (3/40, %95) |
| tv_map VERIFIED_PAGE en iyi kodlar | 1.163'ün **743'ü** yeniden okundu: **0 adet 404**; 3'ü başka kanonik koda yönleniyor (çalışıyor ama tercih edilen kod farklı): `CBOT:2YY1!→CBOT_MINI:2YY1!`, `TWSE:TAIEX→TWSE:IX0001`, `MYX:FBMKLCI→FTSEMYX:FBMKLCI`. tv_map alternatif kodları: 177/231 okundu, 0 adet 404. Ad/ISIN tutarlılığı: 721 kodda Yahoo adı ↔ TV açıklaması karşılaştırıldı, gerçek uyuşmazlık 0 (yalnız aksan/çeviri farkı) |
| f_*.csv'deki kodlar | 846 kodun hepsi okundu: **11 kod TradingView'da YOK (404)** → 167 satır etkileniyor (tablo 2) |
| Çin borsası öneki (SSE/SZSE/SHFE/DCE/ZCE/CFFEX/INE/GFEX) | f_*.csv `tv_ticker` sütunlarında **0** (iyi). tv_final'de **0** (lint ile zorunlu). Not: f_cin `driver_desc`'te `FUT:HC`, `SIDX:sh000300` gibi iç veri etiketleri var — bunlar TV kodu DEĞİL; tv_final'e girmedi |
| HKEX | 20 HK sembolü; f_*'te **21 çift / 71 satırda** ABD/OTC alternatifi yoktu → hepsine sayfası okunmuş alternatif eklendi (tablo 5) |
| Boş/`?` kod | 24 çift / 74 satır kod yoktu (çoğu `f_y_grup` NaN, `çoklu`, `?`); 10 Çin çifti (30 satır) yalnız "ÇİN-AÇILMAZ" yazıp alternatif vermemişti → dolduruldu. 56 çift / **773 satırda** kod doğru ama gereksiz `?` vardı → tv_final'de `?` yok |

## 2. f_*.csv'deki YANLIŞ kodlar (sayfa 404 = TradingView'da böyle bir kod yok)
| f_ dosyası | sürücü | f_'deki kod | DOĞRU kod | satır | kanıt |
|---|---|---|---|---|---|
| gunici, y_ag, holding | TUR (iShares MSCI Turkey) | `AMEX:TUR` | **`NASDAQ:TUR`** | 66 | AMEX:TUR 404; BATS:TUR → NASDAQ:TUR'a yönleniyor |
| y_makro_y | USDTRY 1-3 ay yayılımı | `BIST:USDTRY3!` | **`BIST:USDTRYF2027/BIST:USDTRYX2026`** | 65 | TV'de yalnız `USDTRY1!`/`USDTRY2!` sürekli var; vade kodları (X2026, Z2026, F2027) sayfa ile var; vade geçtikçe güncellenmeli |
| metal, y_ag | SSRM (SSR Mining) | `NYSE:SSRM?` | **`NASDAQ:SSRM`** | 9 | NYSE:SSRM 404 |
| metal, y_ag | STLD (Steel Dynamics) | `NYSE:STLD?` | **`NASDAQ:STLD`** | 8 | NYSE:STLD 404 |
| metal | BUS=F (ABD busheling hurda) | `COMEX:BUS1!` | (TV'de yok) → vekil **`LME:SC1!`** (LME hurda CFR Türkiye) / `COMEX:HRC1!` | 7 | COMEX:BUS1! 404 (TV ajanı da UNCERTAIN demişti) |
| metal | MTF=F (API2 kömür) | `NYMEX:MTF1!?` | **`ICEEUR:ATW1!`** | 5 | NYMEX:MTF1! 404 |
| tarama, y_ag | BA.L (BAE Systems) | `LSE:BA` | **`LSE:BA.`** | 2 | LSE 2 harfli kod noktalı |
| tarama, y_ag | BP.L | `LSE:BP` | **`LSE:BP.`** | 2 | 〃 |
| tarama | NG.L (National Grid) | `LSE:NG` | **`LSE:NG.`** | 1 | 〃 |
| tuketim | KHC (Kraft Heinz) | `NASDAQ:KHC` | **`NYSE:KHC`** | 1 | NASDAQ:KHC 404 |
| banka | XLBNK vadeli akşam seansı | `BIST:XLBNK1!` | **`BIST:XLBNKD1!`** | 1 | endeks vadelisi kökü `<ENDEKS>D` |

Çalışan ama kanonik olmayan (TV başka koda yönlendiriyor): `BATS:PICK→CBOE:PICK` (6), `AMEX:ITB→CBOE:ITB` (2), `CBOT:2YY1!→CBOT_MINI:2YY1!` (9), `TWSE:TAIEX→TWSE:IX0001` (2), `MYX:FBMKLCI→FTSEMYX:FBMKLCI` (3). Geçerli ama tercih dışı: `TVC:FTMIB` (var; tercih `INDEX:FTSEMIB`), `TVC:VIX`, `TVC:KOSPI`, `HSI:HSI`, `FX_IDC:USDCZK/USDKRW` (hepsi sayfası var).

Yanlış ayrıştırma riski (koordinatör dikkat): `f_y_makro_y` sürücüsü **"BAP 2y/5y/10y DİBS"** — BAP = BIST Borçlanma Araçları Piyasası; Yahoo sembolü `BAP` (= NYSE:BAP **Credicorp**) ile karıştırılmamalı. Doğru: `TVC:TR02Y / TVC:TR05Y / TVC:TR10Y / TVC:TR01Y` (TR01Y "?" ile verilmişti → sayfa var). "TLREF bulunamadı" denmişti → **`BIST:TLREF` sayfası VAR** (TURK LIRASI GECELIK REFERANS FAIZ ORANI).

Formül düzeltmesi: `f_enerji` C321 `(2*RB1!*42+HO1!*42-3*BRN1!)/3` önek içermiyordu → `(2*NYMEX:RB1!*42+NYMEX:HO1!*42-3*ICEEUR:BRN1!)/3`.

Görev metnindeki tuzaklar — f_*'te durum: `NYSE:IAG` yalnız Yahoo `IAG` (= **IAMGOLD**, TRALT ile) için kullanılmış → doğru; havayolu IAG her yerde `LSE:IAG` (WebFetch: ES0177542018) → doğru. `NYSE:GOLD` hiç kullanılmamış; Barrick `NYSE:B` (sayfa: "Barrick Mining Corporation"; NYSE:GOLD = "Gold.com, Inc."). `XETR:HEI` = Heidelberg Materials, `NYSE:HEI` = HEICO (ikisi de okundu) → f_kimya doğru. Kore kodları KRX:<6 hane>, Japon TSE:<4 hane>, BMV `ALPEK/A` (ALPEKA 404) → biçim hatası 0 (lint).

## 3. Durum etiketleri (tv_final.durum)
| durum | n | anlam |
|---|---|---|
| DOGRULANDI_2KEZ | 747 | tv_map VERIFIED_PAGE **ve** v_tv sayfa okuması (curl veya WebFetch) aynı kodu verdi |
| DOGRULANDI_V | 77 | tv_map'te yok/UNCERTAIN; yalnız v_tv okudu (2. tur BIST hisse/endeksleri, VİOP metal vadelileri, FX:USDCNH …) |
| CIN_ENGELLI_ALT | 73 | Çin kodu verilmez; tv_kodu = `cin_alternatifler.csv`'de haftalık korelasyonu en yüksek, HKEX dışı alternatif (not'ta r ve güven) |
| HKEX_BELIRSIZ | 20 | HKEX kodu sayfada var ama kullanıcıda açılmayabilir; tv_alternatif = sayfası okunmuş ABD/OTC/ETF |
| BELIRSIZ | 2 | TV'de kod yok: `BUS=F` (vekil LME:SC1!), VİOP gram gümüş `BIST:XAGTRY1!` (404; vekil BIST:XAGUSD1!) |
| SEPET / FORMUL | 130 / 23 | bileşik sürücü: bileşen kodları ` | ` ile; formüller TV sembol kutusuna yazılabilir (ör. `NYMEX:HO1!*42-ICEEUR:BRN1!`, `(FX:USDTRY+FX:EURTRY)/2`, `NASDAQ:TUR/AMEX:EEM`) |
| KOD | 18 | Yahoo'da olmayan tek enstrüman (CBOT:UFV1! üre, MYX:FCPO1! palm, LME:SC1! hurda, BIST:TLREF, TVC:TR0xY …) |
| KENDI / TAKVIM / OLAY / MODEL / TV_YOK | 28 / 12 / 17 / 56 / 11 | hissenin kendi fiyatı (`BIST:<KOD>`, `BIST:<KOD>1!`), takvim, olay, backtest/özet satırı, TV'de karşılığı olmayan veri (EVDS, EPİAŞ, MKK, TEFAS, Türkiye CDS) |

## 4. VİOP (hepsi sayfa ile okundu)
- 47 pay vadelisi `BIST:<KOD>1!` → 47/47 HTTP 200 (ör. `BIST:THYAO1!` "…FUTURES"). Tekil sözleşme biçimi `BIST:<KOD><ay harfi><yıl>` örnekle doğrulandı: `BIST:THYAOX2026`, `BIST:THYAOZ2026`, `BIST:AEFESX2026`, `BIST:AEFESZ2026` (200). Akşam seansı YOK; 15 dk gecikmeli; illikit → bar boşlukları, vade dönüşünde baz sıçraması.
- Endeks vadelileri: `BIST:XU030D1!`, `BIST:XLBNKD1!`, `BIST:X10XBD1!`, `BIST:XSD25D1!` (4/4). Sözleşme kodu örneği `BIST:XU030DZ2026` (var), kontrol `BIST:XU030DZ2035` 404 → sözleşme sayfası yalnız gerçek vade için açılıyor.
- Diğer: `BIST:USDTRY1!`, `BIST:USDTRY2!`, `BIST:EURTRY1!`, `BIST:XAUTRY1!` (gram altın TL), akşam seanslı USD metaller `BIST:XAUUSD1!`, `BIST:XAGUSD1!`, `BIST:XPTUSD1!`, `BIST:XPDUSD1!`, `BIST:XCUUSD1!` (bakır) — hepsi 200. YOK: `BIST:XAGTRY1!`, `BIST:XLBNK1!`, `BIST:XU0301!`, `BIST:USDTRY3!`, `BIST:XAUTRYM1!`.

## 5. Çin ve HKEX
- Çin satırları (73): kod verilmedi; ör. Şanghay/CSI300 → `CBOE:CNYA` (haftalık r 0,85/0,89, YÜKSEK), ChiNext → `AMEX:CNXT` (0,89), DCE demir cevheri → `COMEX:TIO1!` (0,60), SHFE bakır → `AMEX:CPER` (0,69), INE ham petrol → `ICEEUR:BRN1!` (0,78), lityum karbonat → `NYSE:ALB` (0,60), Sina USDCNH → `FX:USDCNH` (Çin borsası değil). Soda külü/cam/üre alternatifleri zayıf (r ≤ 0,23) → ÇOK DÜŞÜK güven notu korunuyor.
- `cin_alternatifler.csv`'de olmayan 3 A-payı (002028.SZ Sieyuan, 600089.SS TBEA, 601179.SS China XD) için genel `AMEX:ASHR` vekili, 518880.SS (Huaan altın ETF) için `AMEX:GLD` verildi — **şirkete özgü korelasyon test edilmedi** (mekanik vekil).
- HKEX alternatifleri (sayfası okunarak seçildi): 0700→OTC:TCEHY, 1211→OTC:BYDDY, 2899→OTC:ZIJMF, 0914→OTC:AHCHY, 0857→OTC:PCCYF, 0386→OTC:SNPMF, 3993→OTC:CMCLF, 6690→OTC:HSHCY/HRSHF, 0323→OTC:MAANF, 0347→OTC:ANGGF, 0358→OTC:JIAXF, 0868→OTC:XYIGF, 1818→OTC:ZHAOF, 3606→OTC:FYGGY, 1070→OTC:TCLHF, 1919→OTC:CICOY; ADR'i olmayanlar ETF: 0300→AMEX:CHIQ, 0941→AMEX:FXI, 1787→AMEX:GDX, 9863→AMEX:KARS. Reddedilen adaylar (404): OTC:CHLKF, OTC:SHDGF, OTC:MDEIF, OTC:FUYAF. **Uyarı:** "F" ile biten OTC kodları gri piyasa — grafik bayat/boşluklu olabilir; korelasyonları cin ajanı yalnız BYDDY/ZIJMF/AHCHY/PCCYF/CMCLF/SNPMF/HSHCY için ölçtü.
- Hang Seng: `TVC:HSI` (HKEX'e bağlı olmayan TV akışı) önerilir; `HSI:HSI` da var.

## 6. Yöntem (bağımsızlık)
- `ll.py` ve `code_tv/` import edilmedi. Kendi ayrıştırıcım (`common.tv_tokens`, `drivers.atoms`) f_*.csv'deki serbest metinden (`"AMEX:TUR (BATS:TUR?)"`, `"formül sepeti (…)"`, `"?; ?; ?"`) TV kodlarını, `driver_yahoo`'dan Yahoo atomlarını çıkarıyor (saf listeler `CF+MOS+NTR`, `EW akran: …`, `sektör akranları gap ort. (…)`; kısa kelime yanlış-pozitifleri için durak listesi: AG, B, F, BAP, MSCI…).
- Sayfa okuma: `fetch.py` — curl **varsayılan User-Agent**, Origin/Referer/çerez taklidi YOK, iç API/websocket YOK, tek işçi, ~1 istek/sn; HTML `dl/tvpages/` (güvenilmeyen veri dizini). Toplam 1.004 sayfa isteği: 973 × 200, 31 × 404.
- Yönlendirme mantığı: `/symbols/SYM/` (sağlayıcısız kanonik sayfa, FX/kripto) = kod geçerli, olduğu gibi kalır; `/symbols/BORSA2-SYM/` = başka koda çözülüyor → tv_kodu çözülen kod. **Kontroller:** `FX:NOTREALX`, `NYSE:NOTREALX`, `FX:XAUTRY`, `OANDA:XAUTRY`, `BIST:USDTRYF2035`, `BIST:XU030DZ2035` → hepsi 404 (yani 200/yönlendirme sahte pozitif üretmiyor); `SAXO:XAUTRY` → `FX_IDC:XAUTRY` kanonik sayfasına gidiyor (var).
- WebFetch: tv_map'ten rastgele 40 VERIFIED_PAGE satırı (`code_v_tv/sample40_webfetch.csv`), 40/40 sembol+ad(+ISIN) eşleşti.

## 7. Sınırlamalar / karşı argümanlar
- "Sayfa var" ≠ "kullanıcının hesabında veri açılır": bölgesel/lisans kısıtı (HKEX, ICE, SGX ücretli akışlar) ölçülemez. Çin kısıtı kullanıcı beyanı; HKEX "belirsiz" olarak bırakıldı.
- OTC gri piyasa kodlarının sayfası var ama işlem/likidite kontrol edilmedi.
- Sepet/formül satırları TV'de tek sembol değildir; ağırlıklar (eşit ağırlık, z-skor, vol-ölçek) TV formülüne birebir taşınmaz — yalnız bileşen kodları doğrulandı.
- `y_*` dosyalarında `tv_ticker` bazen sürücüyü değil HEDEF/işlem enstrümanını gösteriyor (ör. "sektör akranları gap ort. (…)" → `BIST:YKBNK (SSF…)`, `XBANK.IS` → `BIST:XU030D1!`): tv_final'de sürücü kodu verildi; `uyusmazliklar.csv` tur=HEDEF_KODU.
- Denetim 12:48 UTC'deki 21 dosyayı kapsar. Yeni `f_*.csv` gelirse: `sh out/code_v_tv/run_all.sh` (yeni kodları okur, tv_final'i yeniden üretir, lint çalıştırır).

## 8. Dosyalar
- `out/tv_final.csv` — nihai tablo (6 sütun). `VIOP:` önekli satırlar vadeli kontratlar.
- `out/code_v_tv/uyusmazliklar.csv` — tür bazında tüm sorunlar (tur, src, driver_yahoo, tv_ticker_f, dogru_kod, ayrinti, n_satir).
- `out/code_v_tv/f_tv_duzeltme_esleme.csv` — her (driver_yahoo, tv_ticker) çifti → doğru kod (f_*.csv'yi yamalamak için birleştirme tablosu; 1.619 çift).
- `out/code_v_tv/fetch_cache.jsonl` — 1.004 sayfa okumasının ham kaydı (http, yönlenen URL, pro_symbol, açıklama, ISIN, zaman).
- `out/code_v_tv/sample40_webfetch.csv`, `name_check.csv`, `lint_sorunlar.csv` (boş = biçim hatası yok).
- Kod: `common.py`, `drivers.py`, `special.py` (Yahoo dışı sürücü eşlemeleri), `audit.py`, `fetch.py`, `build_final.py`, `lint.py`, `run_all.sh`.
