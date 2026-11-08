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


## Popüler ama izleme listesine alınmayanlar (neden?)

| ETF | TradingView | Aile | Neden alınmadı |
|---|---|---|---|
| BOIL ⚠ | `AMEX:BOIL` | Enerji ve tarım emtiası | Long stratejisi yok, koşulsuz bozulma -36 bp/gün, EIA günü -66 bp; yalnız 'kaçın' kuralı. |
| UVXY ⚠ | `CBOE:UVXY` | Volatilite (VIX) | 1,5x kısa vade; -18 bp/gün koşulsuz kayıp; rejim/sıçrama girişleri negatif (C1 h1 rejim girişi -284 bp); PTP riski; al-tut maxDD %-99,99. |
| UVIX | `CBOE:UVIX` | Volatilite (VIX) | 2x; -35 bp/gün koşulsuz kayıp; 1 günde -%43,8 görüldü; tüm long kurallar negatif (VIX gerilmesi O1 h2 -842 bp, t=-4,0). |
| SVIX | `CBOE:SVIX` | Volatilite (VIX) | Denetçi: kanıt yalnız 2022+, -1x yapı Şubat 2018 tipi olayda ~%90+ kayıp. |
| VIXY | `CBOE:VIXY` | Volatilite (VIX) | VXX ile aynı endeks (kopya); daha az likit; ProShares Trust II (PTP riski); -11 bp/gün koşulsuz kayıp. |
| SQQQ | `NASDAQ:SQQQ` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈33 bp sıfırlama kaybı. Yalnız koruma amaçlı. |
| SOXS | `AMEX:SOXS` | Sektör ve tematik | Ters 3x: kısa yön için doğrulanmış sinyal yok; sürekli değer kaybı (1 yıl -%90). Midas'ta bulunurluğu doğrulanamadı. |
| SPXU | `AMEX:SPXU` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈13 bp sıfırlama kaybı. Yalnız koruma amaçlı. |
| SPXS | `AMEX:SPXS` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈13 bp sıfırlama kaybı. Yalnız koruma amaçlı. SPXU kopyası. |
| TZA | `AMEX:TZA` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈25 bp sıfırlama kaybı. Yalnız koruma amaçlı. |
| SDS | `AMEX:SDS` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈7 bp sıfırlama kaybı. Yalnız koruma amaçlı. |
| SH | `AMEX:SH` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈2 bp sıfırlama kaybı. Yalnız koruma amaçlı. |
| PSQ | `AMEX:PSQ` | ABD endeks ve faktör | Ters ETF: kısa yön sinyali yok (RSI2>90, 3 gün yükseliş, IBS>0,8 -> ters ETF testleri net negatif); 3 günde ≈5 bp sıfırlama kaybı. Yalnız koruma amaçlı. |
| TNA | `AMEX:TNA` | ABD endeks ve faktör | IWM 3x: IWM sinyali zayıf (S1 C0 t=0,8); TNA'da S1 C1 en kötü işlem −%35, maxDD −%40. Kuyruk riski kazancı haklı çıkarmıyor. |
| UPRO | `AMEX:UPRO` | ABD endeks ve faktör | SPXL kopyası (0,9996); SPXL daha likit (aynı makas). |
| CONL | `NASDAQ:CONL` | Tek hisse kaldıraçlı | Fiyat 2,79$: 1 sentlik adım ~36 bp makas, maliyet 48 bp (ailede en yüksek). 1y getiri -%90. COIN'de S1 negatif (n=31, -71 bp); BTC öncülüğü yok. Kripto maruziyeti için MSTU daha ucuz. |
| TSLQ | `NASDAQ:TSLQ` | Tek hisse kaldıraçlı | Ters TSLA (2024-07'den beri -2x; öncesi -1x; tarama.csv 'lev=-1' eski). Ailede doğrulanmış kısa yön sinyali yok: büyük yükseliş sonrası ters (TH02c) C0 h2 -253 bp, RSI2>90 ve SMA200 altı (TH07) -44 bp, S1 aynası -194 bp. Uzun dönem pozitif sürüklenmeye karşı pozisyon. |
| NVDS | `NASDAQ:NVDS` | Tek hisse kaldıraçlı | Ters NVDA (-1,5x; 2024-07 öncesi -1,25x). Hacim yalnız 7,6 mn$, maliyet 27 bp, maliyet/oynaklık 0,075 (ailede en kötü). Büyük NVDA yükselişinden sonra NVDS almak (TH02c) C0 h2 -254 bp t=-3,05 (FDR'de anlamlı ZARAR); S1 aynası -324 bp t=-3,33. |
| AGQ | `AMEX:AGQ` | Değerli/sanayi metalleri ve madenciler | 2x gümüş, PTP/K-1 riski; 30.01.2026'da -%60 gün; strateji yok. |
| UGL | `AMEX:UGL` | Değerli/sanayi metalleri ve madenciler | 2x altın; ProShares Trust II = PTP/K-1 -> %10 brüt satış stopajı (1446(f)) riski; Midas'ta PTP ibaresi kontrol edilmeli. Kaldıraç gerekiyorsa pozisyon büyütmek (GLD) daha güvenli. |
| ZSL | `AMEX:ZSL` | Değerli/sanayi metalleri ve madenciler | -2x gümüş, PTP/K-1 riski; kısa yön sinyali yok. |
| GLL | `AMEX:GLL` | Değerli/sanayi metalleri ve madenciler | -2x altın, PTP/K-1 riski; doğrulanmış kısa yön sinyali yok (FOMC sonrası düşüş anlamsız: t -1,6). |
| DUST | `AMEX:DUST` | Değerli/sanayi metalleri ve madenciler | -2x GDX; doğrulanmış kısa yön sinyali yok; ters ürün. |
| JDST | `AMEX:JDST` | Değerli/sanayi metalleri ve madenciler | -2x GDXJ; kısa yön sinyali yok; 23 mn $. |
| TUR | `NASDAQ:TUR` | Uluslararası / ülke | Türk yatırımcı için ilginç ama ince: medyan 6,8 mn $/gün, tahmini makas 15 bp (gidiş-dönüş 27 bp; 1.000$'da 45 bp). Gecikmeli öncü yok (SPY/DIA/XLF'ten ters gecikme yalnız IS'te); genel kütüphanede hiçbir sinyal maliyeti geçmiyor. İzlenecekse BIST:XU100 ve FX_IDC:USDTRY gerçek zamanlı; uzatılmış saatte yalnız limit emir. |
| BITO | `AMEX:BITO` | Kripto | BTC vadeli ETF: veri kaynağında dağıtım kaydı YOK (ay başı açılışlarda IBIT'e göre ort. −295 bp boşluk = ex-date) → testler aşağı yanlı; yüksek aylık dağıtımlar ABD'de %20 stopaja tabi (ex-date taşımak vergi sızıntısı); vadeli roll maliyeti; fiyat ~10$ → 1 sent makas ~10 bp (22 bp). Spot ETF'ler varken gereksiz. |
| BITU | `AMEX:BITU` | Kripto | BITX kopyası (corr 0,987), daha az likit (59 mn$), takip kaybı −11 bp/gün; 24.12.2025'te 2×IBIT'e göre −21 puan açıklanamayan fark (dağıtım/veri). BITX tercih. |
| DIA | `AMEX:DIA` | ABD endeks ve faktör | Denetçi: SPY ile 0,84 korelasyon, daha az likit; bağımsız değer yok. |
| RSP | `AMEX:RSP` | ABD endeks ve faktör | Denetçi: SPY ile aynı sivri tepe; bağımsız değer yok. |
| XLK | `AMEX:XLK` | Sektör ve tematik | Denetçi: IBS kuralı OOS ~5 bp, SMH ile 0,94 korelasyon. |
| XLF | `AMEX:XLF` | Sektör ve tematik | Düşük 1g oynaklık (maliyet/oynaklık 0.14); doğrulanmış kural yok; bankalar KRE ile izlenir. |
| EFA | `AMEX:EFA` | Uluslararası / ülke | Günlük oynaklık 104 bp, maliyet/oynaklık 0,125; strateji/öncü yok. |
| VGK | `AMEX:VGK` | Uluslararası / ülke | Günlük oynaklık 105 bp, maliyet/oynaklık 0,13; strateji/öncü yok. |
| ARKK | `CBOE:ARKK` | Sektör ve tematik | ST06 (sert düşüş dönüşü) anlamsız; IBS ~0; QQQ'dan negatif gecikme yalnız IS'te. |
| URA | `AMEX:URA` | Sektör ve tematik | Kenar yok; SPY/NLR'den negatif gecikme OOS zayıf; metal_madenci ailesi kapsıyor. |
| TAN | `AMEX:TAN` | Sektör ve tematik | Kenar yok (ST06, IBS). |
| LABU | `AMEX:LABU` | Sektör ve tematik | XBI IBS -> LABU IS zayıf (IS t 0.8-1.2), OOS güçlü: kararsız; 3x. |
| FAS | `AMEX:FAS` | Sektör ve tematik | XLF sinyalleri OOS zayıf; 3x kaldıraç. |
| TECL | `AMEX:TECL` | Sektör ve tematik | XLK IBS kuralı OOS zayıf (TECL C0 h1 OOS 31 bp, t 0.8); kaldıraçlı araç gerekiyorsa SOXL daha güçlü sinyal ve likidite. |
| FNGU | `AMEX:FNGU` | Sektör ve tematik | 2025-02'de yeniden ihraç (ETN, ihraççı kredi riski); kısa geçmiş. |
| CPER | `AMEX:CPER` | Değerli/sanayi metalleri ve madenciler | Bakır vadeli fonu: 20,8 mn $, ~20 bp (maliyet/oynaklık 0,11), USCF emtia havuzu (PTP/K-1 olasılığı yüksek). Bakıra maruziyet için COPX daha likit; ay sonu/IBS kuralları CPER'de çalışmıyor. |
| DBA | `AMEX:DBA` | Enerji ve tarım emtiası | [K1_muhtemel] maliyet/oynaklık 0.279. Maliyet/oynaklık 0,28 (günlük oynaklık 72 bp); K-1; strateji yok. |
| UNL | `AMEX:UNL` | Enerji ve tarım emtiası | [PTP] maliyet/oynaklık 0.219. Likidite 0,45 mn$, maliyet 47 bp; UNG kopyası. Kontango vekili (UNG/UNL) testi de elendi. |
| WEAT | `AMEX:WEAT` | Enerji ve tarım emtiası | [K1_muhtemel] maliyet/oynaklık 0.129. 10 mn$, maliyet/oynaklık 0,13; K-1; genel kütüphanede tutarlı sinyal yok. |
| CORN | `AMEX:CORN` | Enerji ve tarım emtiası | [K1_muhtemel] maliyet/oynaklık 0.248. 4,7 mn$, 27 bp, maliyet/oynaklık 0,25; K-1; strateji yok. |
| SCHD | `AMEX:SCHD` | ABD endeks ve faktör | Temettü: dar hareket (75 bp/gün, maliyet/oynaklık 0,20); S1 kuralı bu ETF'de C1 h=3 net 31 bp (t=1.8) (eşik altı). |
| JEPI | `AMEX:JEPI` | ABD endeks ve faktör | Kapalı alım (covered call) fonu: yukarı hareket sınırlı, dar hareket (58 bp/gün, maliyet/oynaklık 0,24); S1 OOS'ta zayıf. |
| JEPQ | `NASDAQ:JEPQ` | ABD endeks ve faktör | Kapalı alım (NDX), 2022+ kısa geçmiş; QQQ dönüşünü kısmen keser. |

*Yatırım tavsiyesi değildir. Geçmiş performans geleceği garanti etmez.*
