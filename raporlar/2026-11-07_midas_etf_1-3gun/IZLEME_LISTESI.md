# İzleme listesi — Midas ETF 1-3 gün (07.11.2026)

Kademe: **A** = denetimden geçmiş kural var · **B** = kural var ama kanıt zayıf (küçük boyut / kağıt üstünde) · **C** = kural yok, sürücüleriyle takip.
Karar: **kabul** = ana izleme · **yedek** = alternatif/kopya/kaldıraçlı araç. Ayrıntı ve tam lead-lag: `kartlar/<SYM>.md`. TradingView içe aktarma: `izleme_listeleri/`.
⚠ = PTP/K-1 ürünü (Midas'ta satışta %10 brüt kesinti riski). Maliyet = 2.500$ pozisyonda gidiş-dönüş (komisyon 12 bp + makas).

## ABD endeks ve faktör

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **QQQ** | `NASDAQ:QQQ` | kabul | A | 13 | 134 | Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) (doğrulandı) | `AMEX:XLK`, `AMEX:SPY` | `CME_MINI:NQ1!`, `CBOE:VX1!` |
| **SPY** | `AMEX:SPY` | kabul | B | 13 | 85 | Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) (zayıf) | `NASDAQ:QQQ`, `CBOE:VIX` | `CME_MINI:ES1!`, `CBOE:VX1!` |
| **QLD** | `AMEX:QLD` | yedek | A | 14 | 266 | Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) (doğrulandı) | `NASDAQ:QQQ`, `AMEX:XLK` | `CME_MINI:NQ1!` |
| **TQQQ** | `NASDAQ:TQQQ` | yedek | A | 14 | 396 | Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) (doğrulandı) | `NASDAQ:QQQ`, `AMEX:XLK` | `CME_MINI:NQ1!` |
| **SPXL** | `AMEX:SPXL` | yedek | B | 14 | 256 | Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) (zayıf) | `AMEX:SPY`, `NASDAQ:QQQ` | `CME_MINI:ES1!` |
| **SSO** | `AMEX:SSO` | yedek | B | 14 | 170 | Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) (zayıf) | `AMEX:SPY`, `NASDAQ:QQQ` | `CME_MINI:ES1!` |
| **IWM** | `AMEX:IWM` | yedek | C | 13 | 117 | — | `AMEX:SPY`, `AMEX:DIA` | `CME_MINI:RTY1!`, `CME_MINI:ES1!` |
| **MDY** | `AMEX:MDY` | yedek | C | 14 | 97 | — | `AMEX:IWM`, `AMEX:SPY` | `CME_MINI:RTY1!`, `CME_MINI:ES1!` |

## Sektör ve tematik

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **SMH** | `NASDAQ:SMH` | kabul | A | 13 | 267 | Yarı iletken gün sonu zayıflığı dönüşü (SMH IBS< (doğrulandı); S1'in 3x aracı: SMH IBS<0.20 sinyaliyle SOXL (1  (zayıf) | `AMEX:XLK`, `NASDAQ:QQQ` | `CME_MINI:NQ1!`, `KRX:KOSPI` |
| **SOXX** | `NASDAQ:SOXX` | yedek | A | 13 | 309 | SMH IBS<0,20 kopya aracı | `AMEX:XLK`, `NASDAQ:QQQ` | `CME_MINI:NQ1!`, `KRX:KOSPI` |
| **SOXL** | `AMEX:SOXL` | yedek | B | 14 | 916 | S1'in 3x aracı: SMH IBS<0.20 sinyaliyle SOXL (1  (zayıf) | `AMEX:XLK`, `NASDAQ:QQQ` | `CME_MINI:NQ1!`, `KRX:KOSPI` |
| **KRE** | `AMEX:KRE` | yedek | C | 13 | 131 | — | `AMEX:XLF`, `AMEX:IWM` | `CME_MINI:RTY1!`, `CBOT:ZN1!` |
| **KWEB** | `AMEX:KWEB` | yedek | C | 16 | 168 | — | `AMEX:FXI`, `AMEX:EEM` | `HKEX:HSI1!`, `TVC:HSI` |
| **XBI** | `AMEX:XBI` | yedek | C | 13 | 190 | — | `AMEX:IWM`, `AMEX:SPY` | `CME_MINI:RTY1!`, `CBOE:VIX` |

## Tek hisse kaldıraçlı

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **AMZU** | `NASDAQ:AMZU` | kabul | B | 16 | 424 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:AMZN`, `AMEX:SPY` | `NASDAQ:AMZN`, `CME_MINI:NQ1!` |
| **GGLL** | `NASDAQ:GGLL` | kabul | B | 16 | 428 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:GOOGL`, `AMEX:SPY` | `NASDAQ:GOOGL`, `CME_MINI:NQ1!` |
| **MSFU** | `NASDAQ:MSFU` | kabul | B | 16 | 422 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:MSFT`, `AMEX:SPY` | `NASDAQ:MSFT`, `CME_MINI:NQ1!` |
| **NVDL** | `NASDAQ:NVDL` | kabul | B | 16 | 479 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:NVDA`, `AMEX:XLK` | `NASDAQ:NVDA`, `CME_MINI:NQ1!` |
| **TSLL** | `NASDAQ:TSLL` | kabul | B | 23 | 575 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:TSLA`, `NASDAQ:QQQ` | `NASDAQ:TSLA`, `CME_MINI:NQ1!` |
| **AAPU** | `NASDAQ:AAPU` | yedek | B | 16 | 312 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:AAPL`, `AMEX:DIA` | `NASDAQ:AAPL`, `CME_MINI:NQ1!` |
| **METU** | `NASDAQ:METU` | yedek | B | 17 | 521 | Mega-cap hisse RSI(2) dibi (hisse 200 günlük ort (zayıf) | `NASDAQ:META`, `AMEX:SPY` | `NASDAQ:META`, `CME_MINI:NQ1!` |
| **MSTU** | `CBOE:MSTU` | yedek | C | 16 | 1026 | — | `NASDAQ:MSTR`, `NASDAQ:IBIT` | `COINBASE:BTCUSD`, `CME:BTC1!` |
| **NVDU** | `NASDAQ:NVDU` | yedek | C | 20 | 479 | — | `NASDAQ:NVDA`, `AMEX:XLK` | `NASDAQ:NVDA`, `CME_MINI:NQ1!` |

## Enerji ve tarım emtiası

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **XLE** | `AMEX:XLE` | kabul | C | 14 | 147 | — | `AMEX:USL`, `AMEX:BNO` | `CME_MINI:ES1!`, `NYMEX:CL1!` |
| **XOP** | `AMEX:XOP` | kabul | C | 14 | 189 | — | `AMEX:XLE`, `AMEX:USL` | `CME_MINI:ES1!`, `NYMEX:CL1!` |
| **KOLD** ⚠ | `AMEX:KOLD` | yedek | B | 16 | 684 | EIA doğalgaz depolama raporu öncesi KOLD (yalnız (zayıf) | `AMEX:UNG`, `AMEX:UNL` | `NYMEX:NG1!`, `NYMEX:NG2!` |
| **UCO** ⚠ | `AMEX:UCO` | yedek | B | 16 | 401 | USO alt Bollinger kırılımı, 1 gün bekle, 2 gün l (zayıf) | `AMEX:USL`, `AMEX:BNO` | `NYMEX:CL1!`, `NYMEX:CL2!` |
| **USO** ⚠ | `AMEX:USO` | yedek | B | 14 | 320 | USO alt Bollinger kırılımı, 1 gün bekle, 2 gün l (zayıf) | `AMEX:BNO`, `AMEX:USL` | `NYMEX:CL1!`, `NYMEX:CL2!` |
| **BNO** | `AMEX:BNO` | yedek | C | 16 | 309 | — | `AMEX:USO`, `AMEX:USL` | `NYMEX:CL1!`, `NYMEX:CL2!` |
| **DRIP** | `AMEX:DRIP` | yedek | C | 16 | 379 | — | `AMEX:XLE`, `AMEX:USL` | `CME_MINI:ES1!`, `NYMEX:CL1!` |
| **PDBC** | `NASDAQ:PDBC` | yedek | C | 17 | 134 | — | `AMEX:BNO`, `AMEX:USO` | `NYMEX:CL1!`, `ICEEUR:BRN1!` |
| **SCO** ⚠ | `AMEX:SCO` | yedek | C | 17 | 399 | — | `AMEX:USL`, `AMEX:BNO` | `NYMEX:CL1!`, `NYMEX:CL2!` |
| **UNG** ⚠ | `AMEX:UNG` | yedek | C | 23 | 363 | — | `AMEX:UNL`, `AMEX:USL` | `NYMEX:NG1!`, `NYMEX:NG2!` |

## Değerli/sanayi metalleri ve madenciler

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **GDX** | `AMEX:GDX` | kabul | B | 13 | 322 | Ay sonu (turn-of-month) - altın madencileri (GDX (zayıf) | `AMEX:GLD`, `AMEX:SLV` | `COMEX:GC1!`, `COMEX:SI1!` |
| **GDXJ** | `AMEX:GDXJ` | kabul | B | 14 | 357 | Genç altın madencileri IBS dip alımı (GDXJ) (zayıf) | `AMEX:GDX`, `AMEX:GLD` | `COMEX:GC1!`, `COMEX:SI1!` |
| **GLD** | `AMEX:GLD` | kabul | B | 13 | 182 | Ay sonu (turn-of-month) - altın (GLD) (zayıf) | `AMEX:GDX`, `AMEX:SLV` | `COMEX:GC1!`, `OANDA:XAUUSD` |
| **IAU** | `AMEX:IAU` | yedek | B | 14 | 180 | — | `AMEX:GLD`, `AMEX:SLV` | `COMEX:GC1!`, `OANDA:XAUUSD` |
| **JNUG** | `AMEX:JNUG` | yedek | B | 20 | 709 | Genç altın madencileri IBS dip alımı (GDXJ) (zayıf) | `AMEX:GDX`, `AMEX:GLD` | `COMEX:GC1!`, `COMEX:SI1!` |
| **NUGT** | `AMEX:NUGT` | yedek | B | 16 | 635 | Ay sonu (turn-of-month) - altın madencileri (GDX (zayıf) | `AMEX:GDX`, `AMEX:GLD` | `COMEX:GC1!`, `COMEX:SI1!` |
| **COPX** | `AMEX:COPX` | yedek | C | 14 | 302 | — | `AMEX:CPER`, `AMEX:GDX` | `COMEX:HG1!`, `HKEX:HSI1!` |
| **GLDM** | `AMEX:GLDM` | yedek | C | 14 | 181 | — | `AMEX:GLD`, `AMEX:SLV` | `COMEX:GC1!`, `OANDA:XAUUSD` |
| **PPLT** | `AMEX:PPLT` | yedek | C | 20 | 320 | — | `AMEX:SLV`, `AMEX:GLD` | `NYMEX:PL1!`, `COMEX:GC1!` |
| **SIL** | `AMEX:SIL` | yedek | C | 16 | 350 | — | `AMEX:GDX`, `AMEX:GLD` | `COMEX:GC1!`, `COMEX:SI1!` |
| **SILJ** | `AMEX:SILJ` | yedek | C | 16 | 377 | — | `AMEX:GDX`, `AMEX:GLD` | `COMEX:GC1!`, `COMEX:SI1!` |
| **SIVR** | `AMEX:SIVR` | yedek | C | 16 | 398 | — | `AMEX:SLV`, `AMEX:GLD` | `COMEX:SI1!`, `OANDA:XAGUSD` |
| **SLV** | `AMEX:SLV` | yedek | C | 14 | 398 | — | `AMEX:GLD`, `AMEX:GDX` | `COMEX:SI1!`, `OANDA:XAGUSD` |
| **URA** | `AMEX:URA` | yedek | C | 16 | 318 | — | `AMEX:EEM`, `AMEX:IWM` | `CME_MINI:ES1!`, `CME_MINI:NQ1!` |
| **XME** | `AMEX:XME` | yedek | C | 14 | 238 | — | `AMEX:GDX`, `AMEX:IWM` | `COMEX:HG1!`, `CME_MINI:RTY1!` |

## Tahvil ve döviz

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **TLT** | `NASDAQ:TLT` | kabul | C | 13 | 60 | — | `TVC:US30Y`, `NASDAQ:IEF` | `CBOT:UB1!`, `CBOT:ZB1!` |
| **TBT** | `AMEX:TBT` | yedek | B | 20 | 123 | 10 yıllık Hazine ihalesi öncesi uzun vade zayıfl (zayıf) | `NASDAQ:TLT`, `TVC:US30Y` | `CBOT:UB1!`, `CBOT:ZB1!` |
| **TMV** | `AMEX:TMV` | yedek | B | 20 | 178 | 10 yıllık Hazine ihalesi öncesi uzun vade zayıfl (zayıf) | `NASDAQ:TLT`, `TVC:US30Y` | `CBOT:UB1!`, `CBOT:ZB1!` |
| **TMF** | `AMEX:TMF` | yedek | C | 16 | 176 | — | `NASDAQ:TLT`, `TVC:US30Y` | `CBOT:UB1!`, `CBOT:ZB1!` |

## Volatilite (VIX)

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **SVXY** ⚠ | `CBOE:SVXY` | kabul | B | 16 | 202 | SVXY 2 günlük RSI dibi (200 günlük trend üstünde (zayıf) | `CBOE:VIX`, `CBOE:VVIX` | `CBOE:VX1!`, `CBOE:VX2!` |
| **VXX** | `CBOE:VXX` | yedek | C | 17 | 393 | — | `CBOE:VIX`, `CBOE:VVIX` | `CBOE:VX1!`, `CBOE:VX2!` |

## Kripto

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **ETHA** | `NASDAQ:ETHA` | kabul | C | 14 | 384 | BTC trend filtresi (kapanış > SMA10 > SMA50) → I (zayıf) | `COINBASE:ETHUSD`, `COINBASE:BTCUSD` | `COINBASE:ETHUSD`, `CME:ETH1!` |
| **ETHE** | `AMEX:ETHE` | kabul | C | 18 | 382 | — | `COINBASE:ETHUSD`, `NASDAQ:ETHA` | `COINBASE:ETHUSD`, `CME:ETH1!` |
| **GBTC** | `AMEX:GBTC` | kabul | C | 16 | 281 | BTC trend filtresi (kapanış > SMA10 > SMA50) → I (zayıf) | `COINBASE:BTCUSD`, `NASDAQ:IBIT` | `COINBASE:BTCUSD`, `CME:BTC1!` |
| **IBIT** | `NASDAQ:IBIT` | kabul | C | 14 | 281 | BTC trend filtresi (kapanış > SMA10 > SMA50) → I (zayıf) | `COINBASE:BTCUSD`, `COINBASE:ETHUSD` | `COINBASE:BTCUSD`, `CME:BTC1!` |
| **BITI** | `AMEX:BITI` | yedek | C | 20 | 279 | — | `COINBASE:BTCUSD`, `NASDAQ:IBIT` | `COINBASE:BTCUSD`, `CME:BTC1!` |
| **BITX** | `CBOE:BITX` | yedek | C | 18 | 556 | — | `COINBASE:BTCUSD`, `NASDAQ:IBIT` | `COINBASE:BTCUSD`, `CME:BTC1!` |
| **ETHU** | `CBOE:ETHU` | yedek | C | 17 | 767 | — | `COINBASE:ETHUSD`, `NASDAQ:ETHA` | `COINBASE:ETHUSD`, `CME:ETH1!` |
| **FBTC** | `CBOE:FBTC` | yedek | C | 14 | 281 | BTC trend filtresi (kapanış > SMA10 > SMA50) → I (zayıf) | `COINBASE:BTCUSD`, `NASDAQ:IBIT` | `COINBASE:BTCUSD`, `CME:BTC1!` |
| **SBIT** | `AMEX:SBIT` | yedek | C | 16 | 561 | — | `COINBASE:BTCUSD`, `NASDAQ:IBIT` | `COINBASE:BTCUSD`, `CME:BTC1!` |

## Uluslararası / ülke

| ETF | TradingView | Karar | Kademe | Maliyet (bp) | 1g oynaklık (bp) | Kural(lar) | Aynı gün sürücüler | Gerçek zamanlı izleme |
|---|---|---|---|---|---|---|---|---|
| **EWT** | `AMEX:EWT` | kabul | B | 14 | 219 | ABD sert düşüş günü Asya aşırı tepki dönüşü (UL0 (zayıf) | `AMEX:EEM`, `NASDAQ:SMH` | `CME_MINI:NQ1!`, `CME_MINI:ES1!` |
| **EWY** | `AMEX:EWY` | kabul | B | 13 | 377 | ABD sert düşüş günü Asya aşırı tepki dönüşü (UL0 (zayıf); EWY gün sonu dip dönüşü (IBS<0,10 ve düşüş günü) (zayıf) | `AMEX:EEM`, `NASDAQ:SMH` | `KRX:KOSPI`, `CME_MINI:NQ1!` |
| **FXI** | `AMEX:FXI` | kabul | B | 15 | 121 | ABD sert düşüş günü Asya aşırı tepki dönüşü (UL0 (zayıf) | `AMEX:KWEB`, `AMEX:EEM` | `HKEX:HSI1!`, `TVC:HSI` |
| **EWA** | `AMEX:EWA` | yedek | B | 16 | 115 | ABD sert düşüş günü Asya aşırı tepki dönüşü (UL0 (zayıf) | `AMEX:EWJ`, `AMEX:IWM` | `FX:AUDUSD`, `COMEX:HG1!` |
| **EWH** | `AMEX:EWH` | yedek | B | 16 | 107 | ABD sert düşüş günü Asya aşırı tepki dönüşü (UL0 (zayıf) | `AMEX:FXI`, `AMEX:KWEB` | `HKEX:HSI1!`, `TVC:HSI` |
| **EWJ** | `AMEX:EWJ` | yedek | B | 14 | 137 | ABD sert düşüş günü Asya aşırı tepki dönüşü (UL0 (zayıf) | `AMEX:EEM`, `AMEX:SPY` | `OSE:NK2251!`, `TVC:NI225` |
| **KORU** | `AMEX:KORU` | yedek | B | 26 | 1104 | — | `AMEX:EWY`, `AMEX:EEM` | `KRX:KOSPI`, `CME_MINI:NQ1!` |
| **ASHR** | `AMEX:ASHR` | yedek | C | 16 | 115 | — | `AMEX:EEM`, `NASDAQ:SMH` | `SSE:000300`, `SGX:CN1!` |
| **CQQQ** | `AMEX:CQQQ` | yedek | C | 20 | 194 | — | `AMEX:KWEB`, `AMEX:EEM` | `HKEX:HSI1!`, `FX:USDCNH` |
| **EEM** | `AMEX:EEM` | yedek | C | 14 | 165 | — | `NASDAQ:SMH`, `NASDAQ:QQQ` | `HKEX:HSI1!`, `KRX:KOSPI` |
| **EWZ** | `AMEX:EWZ` | yedek | C | 15 | 220 | — | `AMEX:EEM`, `AMEX:EWJ` | `BMFBOVESPA:IBOV`, `FX_IDC:USDBRL` |
| **IEMG** | `AMEX:IEMG` | yedek | C | 14 | 160 | — | `NASDAQ:SMH`, `NASDAQ:QQQ` | `HKEX:HSI1!`, `KRX:KOSPI` |
| **INDA** | `CBOE:INDA` | yedek | C | 14 | 102 | — | `AMEX:BNO`, `AMEX:DIA` | `NSE:NIFTY`, `CME_MINI:ES1!` |
| **YINN** | `AMEX:YINN` | yedek | C | 16 | 362 | — | `AMEX:FXI`, `AMEX:KWEB` | `HKEX:HSI1!`, `TVC:HSI` |

*Yatırım tavsiyesi değildir. Geçmiş performans geleceği garanti etmez.*
