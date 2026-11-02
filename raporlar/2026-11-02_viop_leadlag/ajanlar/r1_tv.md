# r1_tv — Yahoo → TradingView ticker eşlemesi (ajan: tv)
Tarih: 01.11.2026. Çıktı: `out/tv_map.csv` (yahoo,name,tv_best,tv_alt,status,evidence_url,notes). Kod: `out/code_tv/`.

## 1. Net bulgular
- **1212 satır** (1176 katalog sembolü + 36 ek satır: VİOP vadelileri, TR tahvil faizleri, CFD'ler vb.). Durum dağılımı: VERIFIED_PAGE=1165, CHINA_BLOCKED=42, UNCERTAIN=5.
- VERIFIED_PAGE = halka açık `tradingview.com/symbols/EXCH-SYM/` sayfası **bu oturumda okundu** ve sayfadaki `symbolInfo` (resolved_symbol, açıklama, ISIN) kaydedildi; hisse/ETF'lerde Yahoo adı ile TV açıklaması karşılaştırıldı (uyuşmazlık → UNCERTAIN).
- **VİOP TradingView'da VAR** (BIST öneki, 15 dk gecikmeli ücretsiz): endeks vadelisi `BIST:XU030D1!` (kök `XU030D`, D = vadeli), pay vadelisi `BIST:THYAO1!` (kök = hisse kodu), döviz `BIST:USDTRY1!`, altın `BIST:XAUTRY1!`. `BIST:XU0301!`, `BIST:F_XU0301!`, `BIST:F_THYAO1!`, `BIST:THYAOD1!` **YOK** (404).
- Önek tuzakları (sayfa ile doğrulandı): NYSE Arca ETF'leri **AMEX:** (AMEX:EEM, AMEX:FXI, AMEX:GDX); Nasdaq'ta işlem gören iShares'ler **NASDAQ:** (NASDAQ:TUR, NASDAQ:EMB, NASDAQ:EUFN, NASDAQ:MCHI); Cboe BZX'e taşınan iShares'ler **CBOE:** (CBOE:ITA; AMEX:ITA/BATS:ITA yazılınca CBOE:ITA'ya çözülüyor). LSE'de 2 harfli kodlar nokta ile biter (LSE:BA., LSE:QQ., LSE:BP., LSE:NG.). İskandinav B/A hisseleri alt çizgi (OMXSTO:SAAB_B, OMXCOP:CARL_B, OMXHEX:NDA_FI).
- **Ticker çakışmaları**: LSE:IAG (IAG havayolu) ≠ NYSE:IAG (IAMGOLD); NYSE:B = Barrick (yeni kod), NYSE:GOLD = Gold.com (Barrick DEĞİL); NYSE:HEI = HEICO ≠ XETR:HEI (Heidelberg Materials); NYSE:TS = Tenaris; NYSE:SMA = SmartStop; NYSE:STC = Stewart Information (Yahoo grubu "tel" yanlış etiketli olabilir).
- **Türkiye CDS TradingView'da bulunamadı** (denenen adaylar 404; arama sonucu yok) → alternatif vekil: `TVC:TR10Y`, `TVC:TR02Y`, `OTC:AKBTY`/`NYSE:TKC` spread, `NASDAQ:TUR`, `NASDAQ:EMB`.
- Çin borsaları için kod verilmedi (CHINA_BLOCKED); ABD ETF alternatifleri sayfa ile doğrulandı (AMEX:ASHR, CBOE:CNYA, AMEX:FXI, NASDAQ:MCHI, AMEX:KWEB). HKEX: semboller TV'de mevcut ama kullanıcıda açılmayabilir → her HK satırına ADR/OTC alternatifi eklendi.

## 2. Yöntem
- Yalnızca **halka açık sembol sayfaları** düz GET ile okundu (curl varsayılan UA; Origin/Referer taklidi YOK, iç API/websocket YOK), ~1 istek/sn, en fazla 2 sıralı işçi. Kod: `code_tv/tvpage.py`, `run_verify.py`, `finalize.py`; ham sonuçlar `code_tv/cache*.jsonl`.
- Kanıt mantığı: HTTP 200 + `symbolInfo` → sembol var; 404 → yok. Bazı sayfalar (FX, SP:SPX, XAUTRY) 301 ile kanonik `/symbols/SYM/` sayfasına yönleniyor; bu **yalnızca sembol mevcutsa** oluyor (kontrol: `FX-NOTREAL`, `OANDA-XAUTRY`, `FX-XAUTRY` → 404; `FX_IDC-XAUTRY`, `SAXO-XAUTRY` → 301). Bu durumda talep edilen kod geçerli kabul edildi, notta kanonik sayfanın gösterdiği kod yazıldı.
- Talep edilen kod başka bir koda çözülüyorsa (ör. AMEX:ITA → CBOE:ITA) **tv_best = çözülen kod**.
- WebSearch: VİOP kodu (`BIST-XU030D1!` arama sonucu), TradingView veri kapsamı sayfası (https://www.tradingview.com/data-coverage/).

## 3. Kurallar tablosu (Yahoo borsası → TradingView öneki)
| Yahoo exch | TV öneki | n | sayfa ile doğrulanan | UNCERTAIN | yalnız kural | örnek |
|---|---|---|---|---|---|---|
| NYSE | NYSE | 210 | 210 | 0 | 0 | AA → NYSE:AA |
| Istanbul | BIST | 134 | 134 | 0 | 0 | AEFES.IS → BIST:AEFES |
| NYSEArca | AMEX | 91 | 91 | 0 | 0 | ASHR → AMEX:ASHR |
| NasdaqGS | NASDAQ | 56 | 56 | 0 | 0 | AAL → NASDAQ:AAL |
| XETRA | XETR | 47 | 47 | 0 | 0 | 8TRA.DE → XETR:8TRA |
| HKSE | HKEX | 43 | 43 | 0 | 0 | 0001.HK → HKEX:1 |
| LSE | LSE | 35 | 35 | 0 | 0 | AAL.L → LSE:AAL |
| Tokyo | TSE | 33 | 32 | 1 | 0 | 2502.T → TSE:2502 |
| Paris | EURONEXT | 33 | 33 | 0 | 0 | AC.PA → EURONEXT:AC |
| Shanghai | (kod yok) | 26 | 0 | 0 | 0 | 000001.SS →  |
| KSE | KRX | 25 | 25 | 0 | 0 | 000270.KS → KRX:000270 |
| OTC Markets OTCPK | OTC | 25 | 24 | 1 | 0 | AHCHY → OTC:AHCHY |
| NasdaqGM | NASDAQ | 24 | 24 | 0 | 0 | ACWI → NASDAQ:ACWI |
| CCY | FX | 20 | 20 | 0 | 0 | AUDUSD=X → FX:AUDUSD |
| MCE | BME | 18 | 18 | 0 | 0 | ACS.MC → BME:ACS |
| NSE | NSE | 17 | 17 | 0 | 0 | ADANIGREEN.NS → NSE:ADANIGREEN |
| Shenzhen | (kod yok) | 16 | 0 | 0 | 0 | 000100.SZ →  |
| CCY | FX_IDC | 16 | 16 | 0 | 0 | AED=X → FX_IDC:USDAED |
| Stockholm | OMXSTO | 16 | 16 | 0 | 0 | AXFO.ST → OMXSTO:AXFO |
| Warsaw | GPW | 14 | 14 | 0 | 0 | ALE.WA → GPW:ALE |
| CBOT | CBOT | 13 | 13 | 0 | 0 | 2YY=F → CBOT:2YY1! |
| ASX | ASX | 13 | 13 | 0 | 0 | BHP.AX → ASX:BHP |
| Toronto | TSX | 12 | 12 | 0 | 0 | ARE.TO → TSX:ARE |
| Milan | MIL | 12 | 12 | 0 | 0 | BRE.MI → MIL:BRE |
| Amsterdam | EURONEXT | 11 | 11 | 0 | 0 | AD.AS → EURONEXT:AD |
| Athens | ATHEX | 11 | 11 | 0 | 0 | AEGN.AT → ATHEX:AEGN |
| Swiss | SIX | 10 | 10 | 0 | 0 | ABBN.SW → SIX:ABBN |
| Johannesburg | JSE | 10 | 10 | 0 | 0 | ABG.JO → JSE:ABG |
| Cboe US | CBOE | 10 | 10 | 0 | 0 | CNYA → CBOE:CNYA |
| Taiwan | TWSE | 9 | 9 | 0 | 0 | 1101.TW → TWSE:1101 |
| Brussels | EURONEXT | 8 | 8 | 0 | 0 | ABI.BR → EURONEXT:ABI |
| Jakarta | IDX | 8 | 8 | 0 | 0 | ADRO.JK → IDX:ADRO |
| Oslo | OSL | 8 | 8 | 0 | 0 | AKRBP.OL → OSL:AKRBP |
| COMEX | COMEX | 8 | 7 | 1 | 0 | ALI=F → COMEX:ALI1! |
| Saudi | TADAWUL | 7 | 7 | 0 | 0 | 1120.SR → TADAWUL:1120 |
| São Paulo | BMFBOVESPA | 7 | 7 | 0 | 0 | ASAI3.SA → BMFBOVESPA:ASAI3 |
| NY Mercantile | NYMEX | 7 | 7 | 0 | 0 | B0=F → NYMEX:B01! |
| Chicago Options | CBOE | 7 | 7 | 0 | 0 | ^GVZ → CBOE:GVZ |
| Vienna | VIE | 6 | 6 | 0 | 0 | OMV.VI → VIE:OMV |
| EGX | EGX | 5 | 5 | 0 | 0 | ABUK.CA → EGX:ABUK |
| Mexico | BMV | 5 | 5 | 0 | 0 | ALPEKA.MX → BMV:ALPEK/A |
| Copenhagen | OMXCOP | 5 | 5 | 0 | 0 | CARL-B.CO → OMXCOP:CARL_B |
| Helsinki | OMXHEX | 5 | 5 | 0 | 0 | FIA1S.HE → OMXHEX:FIA1S |
| NYSE American | AMEX | 4 | 4 | 0 | 0 | BTG → AMEX:BTG |
| ICE Futures | ICEUS | 4 | 4 | 0 | 0 | CC=F → ICEUS:CC1! |
| CME | CME | 4 | 4 | 0 | 0 | CNH=F → CME:CNH1! |
| Thailand | SET | 4 | 4 | 0 | 0 | CPALL.BK → SET:CPALL |
| Lisbon | EURONEXT | 4 | 4 | 0 | 0 | EDP.LS → EURONEXT:EDP |
| Budapest | BET | 4 | 4 | 0 | 0 | MOL.BD → BET:MOL |
| Cboe Indices | TVC | 4 | 4 | 0 | 0 | ^FVX → TVC:US05Y |
| CME | CME_MINI | 3 | 3 | 0 | 0 | ES=F → CME_MINI:ES1! |
| Nasdaq GIDS | NASDAQ | 3 | 3 | 0 | 0 | ^IXIC → NASDAQ:IXIC |
| OTC Markets OTCQX | OTC | 2 | 2 | 0 | 0 | AKBTY → OTC:AKBTY |
| NasdaqCM | NASDAQ | 2 | 2 | 0 | 0 | BIOX → NASDAQ:BIOX |
| CCC | BITSTAMP | 2 | 2 | 0 | 0 | BTC-USD → BITSTAMP:BTCUSD |
| NY Mercantile | ICEEUR | 2 | 2 | 0 | 0 | BZ=F → ICEEUR:BRN1! |
| CCY | OANDA | 2 | 2 | 0 | 0 | CZK=X → OANDA:USDCZK |
| SES | SGX | 2 | 2 | 0 | 0 | D05.SI → SGX:D05 |
| Tel Aviv | TASE | 2 | 2 | 0 | 0 | ELAL.TA → TASE:ELAL |
| Dubai | DFM | 2 | 2 | 0 | 0 | EMAAR.AE → DFM:EMAAR |
| HKSE | HSI | 2 | 2 | 0 | 0 | HSTECH.HK → HSI:HSTECH |
| Zurich | TVC | 2 | 2 | 0 | 0 | ^STOXX → TVC:SXXP |
| Prague | PSECZ | 1 | 1 | 0 | 0 | CEZ.PR → PSECZ:CEZ |
| NY Mercantile | ICEUS | 1 | 1 | 0 | 0 | CT=F → ICEUS:CT1! |
| ICE Futures | TVC | 1 | 1 | 0 | 0 | DX-Y.NYB → TVC:DXY |
| Milan | INDEX | 1 | 1 | 0 | 0 | FTSEMIB.MI → INDEX:FTSEMIB |
| IOB | LSIN | 1 | 1 | 0 | 0 | HSBK.IL → LSIN:HSBK |
| ICE Futures | FX | 1 | 1 | 0 | 0 | QA=F → FX:GBPAUD |
| Qatar | QSE | 1 | 1 | 0 | 0 | QNBK.QA → QSE:QNBK |
| MCX | MOEX | 1 | 1 | 0 | 0 | ROSN.ME → MOEX:ROSN |
| Irish | EURONEXT | 1 | 1 | 0 | 0 | RYA.IR → EURONEXT:RYA |
| NY Mercantile | ICEENDEX | 1 | 1 | 0 | 0 | TTF=F → ICEENDEX:TFM1! |
| CCC | KRAKEN | 1 | 1 | 0 | 0 | USDT-USD → KRAKEN:USDTUSD |
| FTSE Index | FTSE | 1 | 1 | 0 | 0 | XIN9.FGI → FTSE:XIN9 |
| CBOT | CBOT_MINI | 1 | 1 | 0 | 0 | YM=F → CBOT_MINI:YM1! |
| BSE | BSE | 1 | 1 | 0 | 0 | ^BSESN → BSE:SENSEX |
| DJI | DJ | 1 | 1 | 0 | 0 | ^DJI → DJ:DJI |
| FTSE Index | TVC | 1 | 1 | 0 | 0 | ^FTSE → TVC:UKX |
| SNP | SP | 1 | 1 | 0 | 0 | ^GSPC → SP:SPX |
| HKSE | TVC | 1 | 1 | 0 | 0 | ^HSI → TVC:HSI |
| Kuala Lumpur | MYX | 1 | 1 | 0 | 0 | ^KLSE → MYX:FBMKLCI |
| Buenos Aires | BCBA | 1 | 1 | 0 | 0 | ^MERV → BCBA:IMV |
| NYSE | TVC | 1 | 1 | 0 | 0 | ^MOVE → TVC:MOVE |
| Osaka | TVC | 1 | 1 | 0 | 0 | ^N225 → TVC:NI225 |
| NZSE | NZX | 1 | 1 | 0 | 0 | ^NZ50 → NZX:NZ50G |
| Chicago Options | TVC | 1 | 1 | 0 | 0 | ^RUT → TVC:RUT |
| SES | TVC | 1 | 1 | 0 | 0 | ^STI → TVC:STI |
| Cboe Indices | CBOE | 1 | 1 | 0 | 0 | ^VIX → CBOE:VIX |

Ek kurallar: ABD sınıf hisseleri `-` → `.` (BRK-B → NYSE:BRK.B); Stockholm/Helsinki/Kopenhag `-` → `_`; LSE 2 harf → sonuna `.`; HKEX baştaki sıfırlar atılır (0700.HK → HKEX:700); BMV seri harfi `/` ile (GFNORTEO.MX → BMV:GFNORTE/O, BIMBOA.MX → BMV:BIMBO/A, ALPEKA.MX → BMV:ALPEK/A; `BMV:ALPEKA` 404); Toronto `-` → `.` (HPS-A.TO → TSX:HPS.A, kural); Kore/Tayvan/Japonya/Suudi sayısal kod aynen (KRX:005930, TSE:7203, TADAWUL:2222); vadeli = `KÖK1!` (ön ay sürekli), `KÖK2!` ikinci ay; vade kodu = KÖK+ay harfi+yıl (BIST:XU030DZ2026 = Aralık 2026).

## 4. VİOP — TradingView durumu
| VİOP sözleşmesi | TradingView kodu | durum |
|---|---|---|
| VİOP BIST30 endeks vadeli (sürekli) | `BIST:XU030D1!` | VERIFIED_PAGE |
| VİOP Likit Banka endeks vadeli | `BIST:XLBNKD1!` | VERIFIED_PAGE |
| VİOP Banka Dışı Likit 10 vadeli | `BIST:X10XBD1!` | VERIFIED_PAGE |
| VİOP BIST Sürdürülebilirlik 25 vadeli | `BIST:XSD25D1!` | VERIFIED_PAGE |
| VİOP USDTRY vadeli (sürekli) | `BIST:USDTRY1!` | VERIFIED_PAGE |
| VİOP EURTRY vadeli | `BIST:EURTRY1!` | VERIFIED_PAGE |
| VİOP Altın (TL/gram) vadeli | `BIST:XAUTRY1!` | VERIFIED_PAGE |
| VİOP Gram gümüş vadeli | `BIST:XAGTRY1!` | UNCERTAIN |
| VİOP BIST30 Aralık 2026 kontratı (örnek vade kodu) | `BIST:XU030DZ2026` | VERIFIED_PAGE |

**Pay vadelileri:** 47 VİOP dayanağından 47 tanesinin `BIST:<KOD>1!` sürekli kontrat sayfası okundu (VERIFIED_PAGE); hepsi mevcut. Kodlar tv_map.csv'de ilgili hissenin `tv_alt` sütununda.
- Not: VİOP verisi ücretsiz kullanıcıya **15 dk gecikmeli**; gerçek zamanlı "Borsa Istanbul futures/options" paketi ücretli. Pay vadelilerinde hacim düşük olduğundan sürekli kontrat grafiği boşluklu/bayat olabilir; roll günlerinde (vade sonu) baz farkı kadar sıçrama olur.
- Akşam seansı: VİOP akşam seansı barlarının TradingView'da görünüp görünmediği bu çalışmada doğrulanmadı (sayfa seans bilgisi vermiyor) — UNCERTAIN.

## 5. Öncelikli liste (görev 2–3) — seçilen kodlar
| Yahoo | tv_best | tv_alt | durum | not |
|---|---|---|---|---|
| XU100.IS | `BIST:XU100` | — | VERIFIED_PAGE | TV: BIST 100 Index |
| XU030.IS | `BIST:XU030` | — | VERIFIED_PAGE | TV: BIST 30 Index |
| XBANK.IS | `BIST:XBANK` | — | VERIFIED_PAGE | TV: BIST Banks Index |
| XUSIN.IS | `BIST:XUSIN` | — | VERIFIED_PAGE | TV: BIST SINAI |
| XHOLD.IS | `BIST:XHOLD` | — | VERIFIED_PAGE | TV: BIST HOLDING VE YATIRIM |
| XLBNK.IS | `BIST:XLBNK` | — | VERIFIED_PAGE | TV: BIST Liquid Banks Index |
| ^GSPC | `SP:SPX` | `TVC:SPX` | VERIFIED_PAGE | TV: S&P 500 |
| ^NDX | `NASDAQ:NDX` | `TVC:NDX` | VERIFIED_PAGE | TV: NASDAQ-100 Index |
| ^DJI | `DJ:DJI` | `TVC:DJI` | VERIFIED_PAGE | TV: Dow Jones Industrial Average |
| ^RUT | `TVC:RUT` | `RUSSELL:RUT` / `CBOE:RUT` | VERIFIED_PAGE | TV: US Small Cap 2000 Index |
| ^SOX | `NASDAQ:SOX` | `TVC:SOX` | VERIFIED_PAGE | TV: PHLX Semiconductor |
| ^GDAXI | `XETR:DAX` | `TVC:DEU40` | VERIFIED_PAGE | TV: DAX Index |
| ^STOXX50E | `TVC:SX5E` | `STOXX:SX5E` | VERIFIED_PAGE | TV: STOXX 50 |
| ^STOXX | `TVC:SXXP` | `STOXX:SXXP` | VERIFIED_PAGE | TV: STOXX 600 |
| ^FTSE | `TVC:UKX` | `FTSE:UKX` | VERIFIED_PAGE | TV: UK 100 INDEX |
| ^FCHI | `EURONEXT:PX1` | `TVC:CAC40` | VERIFIED_PAGE | TV: CAC 40 Index |
| ^IBEX | `BME:IBC` | `TVC:IBEX35` | VERIFIED_PAGE | TV: IBEX 35 Index |
| FTSEMIB.MI | `INDEX:FTSEMIB` | — | VERIFIED_PAGE | TV: FTSE MIB INDEX |
| ^N225 | `TVC:NI225` | `INDEX:NKY` / `OSE:NK2251!` | VERIFIED_PAGE | TV: Japan 225 Index |
| ^KS11 | `KRX:KOSPI` | `TVC:KOSPI` | VERIFIED_PAGE | TV: KOSPI Composite Index |
| ^HSI | `TVC:HSI` | `HSI:HSI` | VERIFIED_PAGE | TV: Hang Seng Index |
| ^BVSP | `BMFBOVESPA:IBOV` | — | VERIFIED_PAGE | TV: Bovespa Index |
| DX-Y.NYB | `TVC:DXY` | `ICEUS:DX1!` | VERIFIED_PAGE | TV: U.S. Dollar Currency Index |
| ^VIX | `CBOE:VIX` | `TVC:VIX` | VERIFIED_PAGE | TV: CBOE Volatility Index |
| ^MOVE | `TVC:MOVE` | — | VERIFIED_PAGE | TV: ICE BofAML U.S. Bond Market Option Volatility Estimate Index |
| ^TNX | `TVC:US10Y` | — | VERIFIED_PAGE | TV: United States 10 Year Government Bonds Yield |
| ES=F | `CME_MINI:ES1!` | `TVC:SPX` | VERIFIED_PAGE | TV: E-mini S&P 500 Futures |
| NQ=F | `CME_MINI:NQ1!` | `TVC:NDX` | VERIFIED_PAGE | TV: E-mini Nasdaq-100 Futures |
| YM=F | `CBOT_MINI:YM1!` | — | VERIFIED_PAGE | TV: E-mini Dow Jones Industrial Average Index Futures |
| BZ=F | `ICEEUR:BRN1!` | `NYMEX:BB1!` / `TVC:UKOIL` | VERIFIED_PAGE | TV: Brent Crude Futures |
| CL=F | `NYMEX:CL1!` | `TVC:USOIL` | VERIFIED_PAGE | TV: Crude Oil Futures |
| HO=F | `NYMEX:HO1!` | — | VERIFIED_PAGE | TV: NY Harbor ULSD Futures |
| RB=F | `NYMEX:RB1!` | — | VERIFIED_PAGE | TV: RBOB Gasoline Futures |
| NG=F | `NYMEX:NG1!` | — | VERIFIED_PAGE | TV: Henry Hub Natural Gas Futures |
| TTF=F | `ICEENDEX:TFM1!` | `NYMEX:TTF1!` | VERIFIED_PAGE | TV: Dutch TTF Natural Gas Futures |
| MTF=F | `ICEEUR:ATW1!` | — | VERIFIED_PAGE | TV: API2 Rotterdam Coal Futures |
| GC=F | `COMEX:GC1!` | `TVC:GOLD` / `OANDA:XAUUSD` | VERIFIED_PAGE | TV: Gold Futures |
| SI=F | `COMEX:SI1!` | `TVC:SILVER` / `OANDA:XAGUSD` | VERIFIED_PAGE | TV: Silver Futures |
| PL=F | `NYMEX:PL1!` | `TVC:PLATINUM` | VERIFIED_PAGE | TV: Platinum Futures |
| PA=F | `NYMEX:PA1!` | `TVC:PALLADIUM` | VERIFIED_PAGE | TV: Palladium Futures |
| HG=F | `COMEX:HG1!` | `CAPITALCOM:COPPER` | VERIFIED_PAGE | TV: Copper Futures |
| ALI=F | `COMEX:ALI1!` | — | VERIFIED_PAGE | TV: Aluminum Futures |
| TIO=F | `COMEX:TIO1!` | `SGX:FEF1!` | VERIFIED_PAGE | TV: Iron Ore CFR China (Platts) Futures |
| HRC=F | `COMEX:HRC1!` | — | VERIFIED_PAGE | TV: U.S. Midwest Domestic Hot-Rolled Coil Steel (CRU) Index Futures |
| ZW=F | `CBOT:ZW1!` | — | VERIFIED_PAGE | TV: Chicago SRW Wheat Futures |
| ZC=F | `CBOT:ZC1!` | — | VERIFIED_PAGE | TV: Corn Futures |
| ZS=F | `CBOT:ZS1!` | — | VERIFIED_PAGE | TV: Soybean Futures |
| KC=F | `ICEUS:KC1!` | — | VERIFIED_PAGE | TV: Coffee C Futures |
| CC=F | `ICEUS:CC1!` | `ICEEUR:C1!` | VERIFIED_PAGE | TV: Cocoa Futures |
| SB=F | `ICEUS:SB1!` | — | VERIFIED_PAGE | TV: Sugar No. 11 Futures |
| CT=F | `ICEUS:CT1!` | — | VERIFIED_PAGE | TV: Cotton No. 2 Futures |
| ZN=F | `CBOT:ZN1!` | — | VERIFIED_PAGE | TV: 10-Year T-Note Futures |
| TRY=X | `FX:USDTRY` | `OANDA:USDTRY` / `FX_IDC:USDTRY` / `SAXO:USDTRY` | VERIFIED_PAGE | TV: US Dollar vs. Turkish Lira |
| EURTRY=X | `FX:EURTRY` | `OANDA:EURTRY` / `FX_IDC:EURTRY` / `SAXO:EURTRY` | VERIFIED_PAGE | FX:EURTRY sayfası kanonik sayfaya yönleniyor (orada OANDA:EURTRY gösteriliyor) — FX:EURTRY |
| EURUSD=X | `FX:EURUSD` | `OANDA:EURUSD` / `FX_IDC:EURUSD` / `SAXO:EURUSD` | VERIFIED_PAGE | FX:EURUSD sayfası kanonik sayfaya yönleniyor (orada OANDA:EURUSD gösteriliyor) — FX:EURUSD |
| CNH=X | (katalogda yok) | | | |
| CNY=X | `FX_IDC:USDCNY` | — | VERIFIED_PAGE | TV: U.S. DOLLAR / CHINESE YUAN |
| ZAR=X | `FX:USDZAR` | `OANDA:USDZAR` / `FX_IDC:USDZAR` / `SAXO:USDZAR` | VERIFIED_PAGE | FX:USDZAR sayfası kanonik sayfaya yönleniyor (orada OANDA:USDZAR gösteriliyor) — FX:USDZAR |
| MXN=X | `FX:USDMXN` | `OANDA:USDMXN` / `FX_IDC:USDMXN` / `SAXO:USDMXN` | VERIFIED_PAGE | TV: US Dollar vs. Mexican Peso |
| BRL=X | `FX_IDC:USDBRL` | — | VERIFIED_PAGE | TV: U.S. DOLLAR / BRAZILIAN REAL |
| HUF=X | `FX:USDHUF` | `OANDA:USDHUF` / `FX_IDC:USDHUF` / `SAXO:USDHUF` | VERIFIED_PAGE | FX:USDHUF sayfası kanonik sayfaya yönleniyor (orada OANDA:USDHUF gösteriliyor) — FX:USDHUF |
| PLN=X | `FX:USDPLN` | `OANDA:USDPLN` / `FX_IDC:USDPLN` / `SAXO:USDPLN` | VERIFIED_PAGE | FX:USDPLN sayfası kanonik sayfaya yönleniyor (orada FX_IDC:USDPLN gösteriliyor) — FX:USDPL |
| JPY=X | `FX:USDJPY` | `OANDA:USDJPY` / `FX_IDC:USDJPY` / `SAXO:USDJPY` | VERIFIED_PAGE | TV: US Dollar vs. Japanese Yen |
| BTC-USD | `BITSTAMP:BTCUSD` | `COINBASE:BTCUSD` / `CRYPTO:BTCUSD` | VERIFIED_PAGE | TV: Bitcoin / U.S. dollar |
| TUR | `NASDAQ:TUR` | — | VERIFIED_PAGE | TV: iShares MSCI Turkey ETF (US4642867158) |
| EEM | `AMEX:EEM` | — | VERIFIED_PAGE | TV: iShares MSCI Emerging Markets ETF (US4642872349) |
| EMB | `NASDAQ:EMB` | — | VERIFIED_PAGE | TV: iShares JP Morgan USD Emerging Markets Bond ETF (US4642882819) |
| JETS | `AMEX:JETS` | — | VERIFIED_PAGE | TV: U.S. Global Jets ETF (US26922A8421) |
| ITA | `CBOE:ITA` | `AMEX:ITA` | VERIFIED_PAGE | TV: iShares U.S. Aerospace & Defense ETF (US4642887602) |
| GDX | `AMEX:GDX` | — | VERIFIED_PAGE | TV: VanEck Gold Miners ETF (US92189F1066) |
| GDXJ | `AMEX:GDXJ` | — | VERIFIED_PAGE | TV: VanEck Junior Gold Miners ETF (US92189F7915) |
| SLX | `AMEX:SLX` | — | VERIFIED_PAGE | TV: VanEck Steel ETF (US92189F2056) |
| XME | `AMEX:XME` | — | VERIFIED_PAGE | TV: State Street SPDR S&P Metals & Mining ETF (US78464A7550) |
| FXI | `AMEX:FXI` | — | VERIFIED_PAGE | TV: iShares China Large-Cap ETF (US4642871846) |
| ASHR | `AMEX:ASHR` | — | VERIFIED_PAGE | TV: Xtrackers Harvest CSI 300 China A-Shares ETF (US2330518794) |
| MCHI | `NASDAQ:MCHI` | — | VERIFIED_PAGE | TV: iShares MSCI China ETF (US46429B6719) |
| KWEB | `AMEX:KWEB` | — | VERIFIED_PAGE | TV: KraneShares CSI China Internet ETF (US5007673065) |
| EUFN | `NASDAQ:EUFN` | — | VERIFIED_PAGE | TV: iShares MSCI Europe Financials ETF (US4642891802) |
| KBE | `AMEX:KBE` | — | VERIFIED_PAGE | TV: State Street SPDR S&P Bank ETF (US78464A7972) |
| CRAK | `AMEX:CRAK` | — | VERIFIED_PAGE | TV: VanEck Oil Refiners ETF (US92189F5851) |
| KRBN | `AMEX:KRBN` | — | VERIFIED_PAGE | TV: KraneShares Global Carbon Strategy ETF (US5007676787) |
| GRID | `NASDAQ:GRID` | — | VERIFIED_PAGE | TV: First Trust Nasdaq Clean Edge Smart GRID Infrastructure Index (US33737A1088) |
| URA | `AMEX:URA` | — | VERIFIED_PAGE | TV: Global X Uranium ETF (US37954Y8710) |
| TKC | `NYSE:TKC` | `BIST:TCELL` | VERIFIED_PAGE | TV: Turkcell Iletisim Hizmetleri A.S. Sponsored ADR (US9001112047) |
| AKBTY | `OTC:AKBTY` | `BIST:AKBNK` | VERIFIED_PAGE | TV: Akbank T.A.S. Shs Sponsored American Depositary Receipt Repr 2 Shs (US0097195012) |
| TKGBY | `OTC:TKGBY` | `BIST:GARAN` | VERIFIED_PAGE | TV: Turkiye Garanti Bankasi Anonim Sirketi Sponsored ADR (US9001487019) |
| BBVA | `NYSE:BBVA` | `BME:BBVA` | VERIFIED_PAGE | TV: Banco Bilbao Vizcaya Argentaria, S.A. Sponsored ADR (US05946K1016) |
| — | `TVC:TR10Y` | — | VERIFIED_PAGE | Türkiye 10Y tahvil faizi |
| — | `TVC:TR02Y` | — | VERIFIED_PAGE | Türkiye 2Y tahvil faizi |
| — | `TVC:TR05Y` | — | VERIFIED_PAGE | Türkiye 5Y tahvil faizi |
| — | `TVC:US02Y` | — | VERIFIED_PAGE | ABD 2Y tahvil faizi |
| — | `TVC:TR5YCDS` | — | UNCERTAIN | Türkiye 5Y CDS (TradingView aday) |
| — | `FX_IDC:XAUTRY` | `SAXO:XAUTRY` | VERIFIED_PAGE | Ons altın TL (XAUTRY) |
| — | `TVC:UKOIL` | — | VERIFIED_PAGE | Brent CFD |
| — | `TVC:USOIL` | — | VERIFIED_PAGE | WTI CFD |
| — | `TVC:GOLD` | `OANDA:XAUUSD` | VERIFIED_PAGE | Altın CFD |
| — | `TVC:SILVER` | — | VERIFIED_PAGE | Gümüş CFD |
| — | `SGX:FEF1!` | — | VERIFIED_PAGE | SGX demir cevheri 62% (FEF) |
| — | `CME:BTC1!` | — | VERIFIED_PAGE | CME Bitcoin vadeli |
| — | `ICEEUR:ATW1!` | — | VERIFIED_PAGE | ICE Rotterdam kömür (API2) |
| — | `ICEENDEX:ECF1!` | — | VERIFIED_PAGE | Avrupa karbon (EUA) vadeli |
| — | `CBOE:VX1!` | — | VERIFIED_PAGE | CBOE VIX vadeli |

Sektör emsalleri (görev 3):

| Yahoo | tv_best | tv_alt | durum | not |
|---|---|---|---|---|
| RHM.DE | `XETR:RHM` | — | VERIFIED_PAGE | TV: Rheinmetall AG (DE0007030009) |
| LDO.MI | `MIL:LDO` | — | VERIFIED_PAGE | TV: Leonardo SpA (IT0003856405) |
| BA.L | `LSE:BA.` | — | VERIFIED_PAGE | TV: BAE Systems plc (GB0002634946) |
| SAAB-B.ST | `OMXSTO:SAAB_B` | — | VERIFIED_PAGE | TV: Saab AB Class B (SE0021921269) |
| KOG.OL | `OSL:KOG` | — | VERIFIED_PAGE | TV: Kongsberg Gruppen ASA (NO0013536151) |
| HO.PA | `EURONEXT:HO` | — | VERIFIED_PAGE | TV: Thales SA (FR0000121329) |
| HAG.DE | `XETR:HAG` | — | VERIFIED_PAGE | TV: HENSOLDT AG (DE000HAG0005) |
| R3NK.DE | `XETR:R3NK` | — | VERIFIED_PAGE | TV: RENK Group AG (DE000RENK730) |
| BBVA.MC | `BME:BBVA` | `NYSE:BBVA` | VERIFIED_PAGE | TV: Banco Bilbao Vizcaya Argentaria, S.A. (ES0113211835) |
| LHA.DE | `XETR:LHA` | — | VERIFIED_PAGE | TV: Deutsche Lufthansa AG (DE0008232125) |
| AF.PA | `EURONEXT:AF` | — | VERIFIED_PAGE | TV: Air France-KLM SA (FR001400J770) |
| IAG.L | `LSE:IAG` | `BME:IAG` / `OTC:ICAGY` | VERIFIED_PAGE | TV: International Consolidated Airlines Group SA (ES0177542018) |
| RYAAY | `NASDAQ:RYAAY` | `EURONEXT:RYA` | VERIFIED_PAGE | TV: Ryanair Holdings PLC Sponsored ADR (US7835132033) |
| RYA.IR | `EURONEXT:RYA` | `NASDAQ:RYAAY` | VERIFIED_PAGE | TV: Ryanair Holdings PLC (IE00BYTBXV33) |
| WIZZ.L | `LSE:WIZZ` | — | VERIFIED_PAGE | TV: Wizz Air Holdings Plc (JE00BN574F90) |
| ADP.PA | `EURONEXT:ADP` | — | VERIFIED_PAGE | TV: Aeroports de Paris (FR0010340141) |
| FRA.DE | `XETR:FRA` | — | VERIFIED_PAGE | TV: Fraport AG (DE0005773303) |
| AENA.MC | `BME:AENA` | — | VERIFIED_PAGE | TV: Aena SME SA (ES0105046017) |
| VLO | `NYSE:VLO` | — | VERIFIED_PAGE | TV: Valero Energy Corporation (US91913Y1001) |
| PKN.WA | `GPW:PKN` | — | VERIFIED_PAGE | TV: ORLEN Spolka Akcyjna (PLPKN0000018) |
| MOL.BD | `BET:MOL` | — | VERIFIED_PAGE | TV: MOL Hungarian Oil & Gas Plc Class A (HU0000153937) |
| MOH.AT | `ATHEX:MOH` | — | VERIFIED_PAGE | TV: MOTOR OIL (HELLAS) CORINTH REFINERIES S.A. (GRS426003000) |
| ELPE.AT | `ATHEX:ELPE` | — | VERIFIED_PAGE | TV: HELLENiQ ENERGY Holdings S.A. (GRS298343005) |
| MT | `NYSE:MT` | `EURONEXT:MT` | VERIFIED_PAGE | TV: ArcelorMittal SA ADR (US03938L2034) |
| MT.AS | `EURONEXT:MT` | `NYSE:MT` | VERIFIED_PAGE | TV: ArcelorMittal SA (LU1598757687) |
| TKA.DE | `XETR:TKA` | — | VERIFIED_PAGE | TV: thyssenkrupp AG (DE0007500001) |
| SZG.DE | `XETR:SZG` | — | VERIFIED_PAGE | TV: Salzgitter AG (DE0006202005) |
| VOE.VI | `VIE:VOE` | — | VERIFIED_PAGE | TV: voestalpine AG (AT0000937503) |
| VALE | `NYSE:VALE` | — | VERIFIED_PAGE | TV: Vale S.A. Sponsored ADR (US91912E1055) |
| TS | `NYSE:TS` | `MIL:TEN` | VERIFIED_PAGE | TV: Tenaris S.A. Sponsored ADR (US88031M1099) |
| NEM | `NYSE:NEM` | — | VERIFIED_PAGE | TV: Newmont Corporation (US6516391066) |
| SSRM | `NASDAQ:SSRM` | `TSX:SSRM` | VERIFIED_PAGE | TV: SSR Mining Inc (CA7847301032) |
| EGO | `NYSE:EGO` | `TSX:ELD` | VERIFIED_PAGE | TV: Eldorado Gold Corporation (CA2849025093) |
| CF | `NYSE:CF` | — | VERIFIED_PAGE | TV: CF Industries Holdings, Inc. (US1252691001) |
| NTR | `NYSE:NTR` | — | VERIFIED_PAGE | TV: Nutrien Ltd. (CA67077M1086) |
| YAR.OL | `OSL:YAR` | — | VERIFIED_PAGE | TV: Yara International ASA (NO0010208051) |
| F | `NYSE:F` | — | VERIFIED_PAGE | TV: Ford Motor Company (US3453708600) |
| STLA | `NYSE:STLA` | `MIL:STLAM` | VERIFIED_PAGE | TV: Stellantis N.V. (NL00150001Q9) |
| STLAM.MI | `MIL:STLAM` | `NYSE:STLA` / `EURONEXT:STLAP` | VERIFIED_PAGE | TV: Stellantis N.V. (NL00150001Q9) |
| RNO.PA | `EURONEXT:RNO` | — | VERIFIED_PAGE | TV: Renault SA (FR0000131906) |
| VOW3.DE | `XETR:VOW3` | — | VERIFIED_PAGE | TV: Volkswagen AG Pref (DE0007664039) |
| WHR | `NYSE:WHR` | — | VERIFIED_PAGE | TV: Whirlpool Corporation (US9633201069) |
| ELUX-B.ST | `OMXSTO:ELUX_B` | — | VERIFIED_PAGE | TV: Electrolux AB Class B (SE0016589188) |
| 066570.KS | `KRX:066570` | — | VERIFIED_PAGE | TV: LG Electronics Inc. (KR7066570003) |
| 034220.KS | `KRX:034220` | `NYSE:LPL` | VERIFIED_PAGE | TV: LG Display Co., Ltd (KR7034220004) |
| 267260.KS | `KRX:267260` | — | VERIFIED_PAGE | TV: HD Hyundai Electric (KR7267260008) |
| 298040.KS | `KRX:298040` | — | VERIFIED_PAGE | TV: Hyosung Heavy Industries Corp. (KR7298040007) |
| 010120.KS | `KRX:010120` | — | VERIFIED_PAGE | TV: LS Electric Co., Ltd. (KR7010120004) |
| 012450.KS | `KRX:012450` | — | VERIFIED_PAGE | TV: Hanwha Aerospace Co., Ltd. (KR7012450003) |
| 064350.KS | `KRX:064350` | — | VERIFIED_PAGE | TV: Hyundai Rotem Co. (KR7064350002) |
| 079550.KS | `KRX:079550` | — | VERIFIED_PAGE | TV: LIG Defense&Aerospace (KR7079550000) |
| ENR.DE | `XETR:ENR` | — | VERIFIED_PAGE | TV: Siemens Energy AG (DE000ENER6Y0) |
| GEV | `NYSE:GEV` | — | VERIFIED_PAGE | TV: GE Vernova Inc. (US36828A1016) |
| SGO.PA | `EURONEXT:SGO` | — | VERIFIED_PAGE | TV: Compagnie de Saint-Gobain SA (FR0000125007) |
| OI | `NYSE:OI` | — | VERIFIED_PAGE | TV: O-I Glass Inc (US67098H1041) |
| HEI.DE | `XETR:HEI` | — | VERIFIED_PAGE | TV: Heidelberg Materials AG (DE0006047004) |
| HOLN.SW | `SIX:HOLN` | — | VERIFIED_PAGE | TV: Holcim Ltd (CH0012214059) |
| CX | `NYSE:CX` | — | VERIFIED_PAGE | TV: Cemex SAB de CV Sponsored ADR (US1512908898) |
| LYB | `NYSE:LYB` | — | VERIFIED_PAGE | TV: LyondellBasell Industries NV (NL0009434992) |
| BAS.DE | `XETR:BAS` | — | VERIFIED_PAGE | TV: BASF SE (DE000BASF111) |
| 051910.KS | `KRX:051910` | — | VERIFIED_PAGE | TV: LG Chem Ltd. (KR7051910008) |
| IVL.BK | `SET:IVL` | — | VERIFIED_PAGE | TV: Indorama Ventures Public Co. Ltd. (TH1027010004) |
| ALPEKA.MX | `BMV:ALPEK/A` | `OTC:ALPKF` | VERIFIED_PAGE | TV: Alpek, S.A.B. de C.V. Class A (MX01AL0C0004) |
| RELIANCE.NS | `NSE:RELIANCE` | — | VERIFIED_PAGE | TV: Reliance Industries Limited (INE002A01018) |
| 2010.SR | `TADAWUL:2010` | — | VERIFIED_PAGE | TV: Saudi Basic Industries Corp. (SA0007879121) |
| 3402.T | `TSE:3402` | — | VERIFIED_PAGE | TV: Toray Industries, Inc. (JP3621000003) |
| KO | `NYSE:KO` | — | VERIFIED_PAGE | TV: Coca-Cola Company (US1912161007) |
| CCH.L | `LSE:CCH` | `ATHEX:EEE` | VERIFIED_PAGE | TV: Coca-Cola HBC AG (CH0198251305) |
| HEIA.AS | `EURONEXT:HEIA` | `OTC:HEINY` | VERIFIED_PAGE | TV: Heineken NV (NL0000009165) |
| ABI.BR | `EURONEXT:ABI` | `NYSE:BUD` | VERIFIED_PAGE | TV: Anheuser-Busch InBev SA/NV (BE0974293251) |

## 6. Çin ve Hong Kong
- SSE:/SZSE:/SHFE:/DCE:/ZCE:/CFFEX:/INE:/GFEX: için **kod verilmedi** (status=CHINA_BLOCKED). TradingView'da doğrulanmış alternatifler: `AMEX:ASHR` (CSI 300), `CBOE:CNYA` (MSCI China A), `AMEX:FXI`, `NASDAQ:MCHI`, `AMEX:KWEB`, `SGX:CN1!` (FTSE China A50 vadeli, SGX — Çin borsası değil), `FX:USDCNH` (offshore yuan), `FX_IDC:USDCNY`. Çin emtiaları yerine: demir cevheri `SGX:FEF1!` / `COMEX:TIO1!`, çelik `COMEX:HRC1!`, bakır `COMEX:HG1!` / `LME:CA1!` (LME gün sonu). Hangi alternatifin veride en iyi temsil ettiğini cin ajanı test ediyor.
- HKEX: hisse sayfaları TV'de mevcut (ör. `HKEX:700`, `HKEX:9988`) ama **kullanıcıda açılmayabilir** → her HK satırına ADR/OTC alternatifi (`OTC:TCEHY`, `NYSE:BABA`, `OTC:BYDDY`, `OTC:XIACY` …) konuldu. Hang Seng endeksi için HKEX'e bağlı olmayan `TVC:HSI` (TradingView kendi akışı) önerilir; `HSI:HSCEI` (H-share endeksi) Hang Seng Indexes kaynaklı, açılması belirsiz; alternatif `AMEX:FXI`. `HKEX:HSI1!` vadelisi HKEX verisi (muhtemelen açılmaz).

## 7. Ücretli / gecikmeli veri akışları (kaynak: https://www.tradingview.com/data-coverage/ , 01.11.2026 okundu; fiyatlar değişebilir)
| Akış | Ücretsiz | Gerçek zamanlı |
|---|---|---|
| BIST hisse/endeks | 15 dk gecikmeli | ücretli (~8 $/ay non-pro) |
| BIST vadeli/opsiyon (VİOP) | 15 dk gecikmeli | ücretli (~7 $/ay) |
| CME/CBOT/COMEX/NYMEX (ES1!, CL1!, GC1!, ZW1! …) | 10 dk gecikmeli | CME paketi ücretli (~7 $/ay non-pro) |
| ICE US (KC1!, CC1!, SB1!, CT1!, DX1!) | 10 dk gecikmeli | pahalı (~139 $/ay) |
| ICE Europe (BRN1!, ATW1!) / ICE Endex (TFM1!, ECF1!) | 10 dk gecikmeli | pahalı (~130–152 $/ay) |
| SGX vadeli (FEF1!, CN1!) | 10 dk gecikmeli | pahalı (~132 $/ay) |
| LME (CA1!) | gün sonu | ücretli |
| NYSE/NASDAQ/AMEX hisse-ETF | Cboe One ile sınırlı gerçek zamanlı | tam akış ücretli (düşük) |
| Cboe endeksleri (VIX, OVX, GVZ) | 15 dk gecikmeli | ücretli |
| S&P (SP:SPX) / Dow Jones (DJ:DJI) | 10 dk gecikmeli | ücretli |
| Avrupa borsaları (XETR, EURONEXT, LSE, SIX, MIL, BME, Nordic, OSL, VIE, GPW, BET, ATHEX) | 15 dk gecikmeli | ücretli |
| TSE, KRX, ASX, BMV | 20 dk gecikmeli | ücretli |
| TVC: (UKOIL, USOIL, GOLD, DXY, US10Y, TR10Y, UKX, SX5E, NI225, HSI) | ücretsiz (TradingView türetilmiş/CFD) | — |
| FX:, FX_IDC:, OANDA:, SAXO:, BITSTAMP: | ücretsiz | — |

Pratik: gün-içi/canlı izleme için ücretsiz ve gecikmesiz olanlar TVC:/FX: CFD'leridir (TVC:UKOIL, TVC:GOLD, TVC:DXY, FX:USDTRY). Vadeli kontrat (1!) ile CFD arasında baz/vade farkı olur; backtest'te kullanılan Yahoo serisi vadeli ise grafikte de 1! kullanmak daha tutarlıdır.

## 8. FX günlük bar kapanışı (koordinatör notu)
- Doğrulanan: `FX:USDTRY` sayfasındaki `symbolInfo.timezone = America/New_York` (FXCM akışı). BIST sembolleri `Europe/Istanbul`.
- Doğrulanamayan (yalnız topluluk/forum kaynakları): TV FX günlük barı 17:00 New York'ta kapanır (= 21:00 UTC yaz / 22:00 UTC kış). Yani TV'deki FX:USDTRY günlük kapanışı BIST kapanışından (15:00 UTC) ~6–7 saat sonra; Yahoo `TRY=X` günlük barı ile birebir aynı olmayabilir. Kullanıcı BIST kapanışı anındaki kuru görmek isterse 1 saatlik grafikte 15:00 UTC (18:00 TSİ) barına bakmalı. Durum: UNCERTAIN (seans dosyası halka açık sayfada yok).

## 9. Tuzaklar ve sınırlamalar
- Katalogda isim/grup uyuşmazlıkları (TV açıklamasıyla teyitli): `NYSE:SMA` = SmartStop Self Storage (SMA Solar değil → `XETR:S92`), `NYSE:STC` = Stewart Information (Saudi Telecom değil → `TADAWUL:7010`), `NYSE:EDF` = Virtus Stone Harbor EM fonu (Électricité de France değil), `NYSE:GOLD` = Gold.com (Barrick = `NYSE:B`), `NYSE:IAG` = IAMGOLD (IAG havayolu = `LSE:IAG` / `BME:IAG`), `NYSE:HEI` = HEICO (Heidelberg = `XETR:HEI`). `ICEEUR:G1!` = UK Short Gilt (gasoil değil).
- `MOEX:ROSN` sayfası `RUS:ROSN`'a yönleniyor; Rusya verisi yaptırımlar nedeniyle bayat/sınırlı olabilir. `OTC:TYIDY` (Toyota Industries ADR) ve `TSE:5202` (Nippon Sheet Glass) 404 — muhtemelen delist/özelleştirme; UNCERTAIN.
- `COMEX:BUS1!` (busheling hurda) ve `BIST:XAGTRY1!` 404 → UNCERTAIN. Türkiye CDS: TradingView'da bulunamadı.
- Doğrulama tarihi 01–02.11.2026; semboller zamanla değişebilir (ör. kod değişikliği KOZAL→TRALT, KOZAA→TRMET; ikisi de BIST'te doğrulandı). Sayfa varlığı, kullanıcının hesabında verinin açılacağını garanti etmez (bölgesel/lisans kısıtları). Mekanik kuralla eşlenip sayfası okunamayan satırlar CONVENTION olarak işaretli.
- Yöntem dışı bırakılanlar: TradingView iç API'leri/websocket ve başlık sahteciliği kullanılmadı; seans saatleri ve akşam seansı kapsamı bu nedenle doğrulanamadı.
