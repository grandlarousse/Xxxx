"""Yahoo sembolü -> TradingView aday kodları (mekanik kural + elle override). Çıktı: candidates.json
Kullanım: python3 -I build_candidates.py"""
import csv, json, os
BASE = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
OUT = os.path.join(BASE, 'out', 'code_tv')

# --- Borsa (Yahoo 'exch' alanı) -> TradingView öneki ---
EXCH_RULE = {
    'NYSE': 'NYSE', 'NasdaqGS': 'NASDAQ', 'NasdaqGM': 'NASDAQ', 'NasdaqCM': 'NASDAQ', 'NYSEArca': 'AMEX',
    'NYSE American': 'AMEX', 'Cboe US': 'CBOE', 'OTC Markets OTCPK': 'OTC', 'OTC Markets OTCQX': 'OTC',
    'Istanbul': 'BIST', 'XETRA': 'XETR', 'Paris': 'EURONEXT', 'Amsterdam': 'EURONEXT', 'Brussels': 'EURONEXT',
    'Lisbon': 'EURONEXT', 'Irish': 'EURONEXT', 'Milan': 'MIL', 'MCE': 'BME', 'LSE': 'LSE', 'Swiss': 'SIX',
    'Stockholm': 'OMXSTO', 'Helsinki': 'OMXHEX', 'Copenhagen': 'OMXCOP', 'Oslo': 'OSL', 'Vienna': 'VIE',
    'Warsaw': 'GPW', 'Budapest': 'BET', 'Athens': 'ATHEX', 'Prague': 'PSECZ', 'Tokyo': 'TSE', 'KSE': 'KRX',
    'Taiwan': 'TWSE', 'NSE': 'NSE', 'BSE': 'BSE', 'Thailand': 'SET', 'ASX': 'ASX', 'Saudi': 'TADAWUL',
    'Mexico': 'BMV', 'São Paulo': 'BMFBOVESPA', 'Johannesburg': 'JSE', 'Tel Aviv': 'TASE', 'Toronto': 'TSX',
    'Jakarta': 'IDX', 'HKSE': 'HKEX', 'SES': 'SGX', 'EGX': 'EGX', 'Dubai': 'DFM', 'Qatar': 'QSE', 'MCX': 'MOEX',
    'IOB': 'LSE', 'Shanghai': 'SSE', 'Shenzhen': 'SZSE',
}
CHINA = {'Shanghai', 'Shenzhen'}

def mech(sym, exch):
    """Mekanik kural: Yahoo -> EXCH:SYM"""
    pre = EXCH_RULE.get(exch)
    if pre is None:
        return None
    base = sym.split('.')[0] if '.' in sym and not sym.startswith('^') else sym
    if exch in ('NYSE', 'NasdaqGS', 'NasdaqGM', 'NasdaqCM', 'NYSEArca', 'NYSE American', 'Cboe US', 'OTC Markets OTCPK', 'OTC Markets OTCQX'):
        base = sym.replace('-', '.')
    elif exch == 'Toronto':
        base = base.replace('-', '.')
    elif exch in ('Stockholm', 'Helsinki', 'Copenhagen'):
        base = base.replace('-', '_')
    elif exch == 'LSE' and len(base) < 3:
        base = base + '.'
    elif exch == 'HKSE':
        base = str(int(base)) if base.isdigit() else base
    elif exch == 'IOB':
        base = base  # GDR
    return f'{pre}:{base}'

# --- Elle override (sıra = tercih). Her öğe: [aday1, aday2, ...] ---
OV = {
 # ABD / küresel endeksler
 '^GSPC': ['SP:SPX', 'TVC:SPX'], '^DJI': ['DJ:DJI', 'TVC:DJI'], '^IXIC': ['NASDAQ:IXIC', 'TVC:IXIC'],
 '^NDX': ['NASDAQ:NDX', 'TVC:NDX'], '^RUT': ['TVC:RUT', 'RUSSELL:RUT', 'CBOE:RUT'], '^SOX': ['NASDAQ:SOX', 'TVC:SOX'],
 '^GDAXI': ['XETR:DAX', 'TVC:DEU40'], '^FCHI': ['EURONEXT:PX1', 'TVC:CAC40', 'TVC:CAC'], '^FTSE': ['TVC:UKX', 'FTSE:UKX'],
 '^IBEX': ['BME:IBC', 'TVC:IBEX35'], 'FTSEMIB.MI': ['INDEX:FTSEMIB', 'TVC:FTSEMIB', 'MIL:FTSEMIB', 'FTSEMYX:FTSEMIB'],
 '^STOXX50E': ['TVC:SX5E', 'STOXX:SX5E'], '^STOXX': ['TVC:SXXP', 'STOXX:SXXP'], '^AEX': ['EURONEXT:AEX', 'TVC:AEX'],
 '^BFX': ['EURONEXT:BEL20', 'TVC:BEL20'], '^ATX': ['VIE:ATX', 'TVC:ATX', 'INDEX:ATX'], '^SSMI': ['SIX:SMI', 'TVC:SMI'],
 '^OMX': ['OMXSTO:OMXS30', 'TVC:OMXS30'], '^N225': ['TVC:NI225', 'INDEX:NKY', 'OSE:NK2251!'], '^KS11': ['KRX:KOSPI', 'TVC:KOSPI'],
 '^TWII': ['TWSE:TAIEX', 'TVC:TAIEX'], '^HSI': ['TVC:HSI', 'HSI:HSI'], '^HSCE': ['HSI:HSCEI', 'HSI:HSCE', 'TVC:HSCEI'],
 '^AXJO': ['ASX:XJO', 'TVC:XJO'], '^BSESN': ['BSE:SENSEX', 'TVC:SENSEX'], '^NSEI': ['NSE:NIFTY', 'TVC:NIFTY'],
 '^BVSP': ['BMFBOVESPA:IBOV', 'TVC:IBOV'], '^MXX': ['BMV:ME', 'TVC:ME'], '^GSPTSE': ['TSX:TSX', 'TVC:TSX'],
 '^J203.JO': ['JSE:J203', 'TVC:J203'], '^JKSE': ['IDX:COMPOSITE', 'TVC:JCI'], '^KLSE': ['MYX:FBMKLCI', 'TVC:FBMKLCI'],
 '^MERV': ['BCBA:IMV', 'TVC:IMV'], '^NZ50': ['NZX:NZ50G', 'TVC:NZ50G'], '^SET.BK': ['SET:SET', 'TVC:SET'],
 '^STI': ['TVC:STI', 'SGX:STI'], '^TA125.TA': ['TASE:TA125', 'TVC:TA125'], '^TASI.SR': ['TADAWUL:TASI', 'TVC:TASI'],
 '^CASE30': ['EGX:EGX30', 'TVC:EGX30'], '^BUX.BD': ['BET:BUX', 'TVC:BUX'], 'WIG20.WA': ['GPW:WIG20', 'TVC:WIG20'],
 'GD.AT': ['ATHEX:GD', 'TVC:GD'],
 # Volatilite / faiz
 '^VIX': ['CBOE:VIX', 'TVC:VIX'], '^VIX3M': ['CBOE:VIX3M', 'TVC:VIX3M'], '^VVIX': ['CBOE:VVIX', 'TVC:VVIX'],
 '^VXN': ['CBOE:VXN', 'TVC:VXN'], '^OVX': ['CBOE:OVX', 'TVC:OVX'], '^GVZ': ['CBOE:GVZ', 'TVC:GVZ'],
 '^SKEW': ['CBOE:SKEW', 'TVC:SKEW'], '^VXEEM': ['CBOE:VXEEM', 'TVC:VXEEM'], '^MOVE': ['TVC:MOVE'],
 '^TNX': ['TVC:US10Y', 'CBOE:TNX'], '^FVX': ['TVC:US05Y', 'CBOE:FVX'], '^TYX': ['TVC:US30Y', 'CBOE:TYX'],
 '^IRX': ['TVC:US03MY', 'CBOE:IRX'],
 # Vadeliler (sürekli kontrat 1!)
 'ES=F': ['CME_MINI:ES1!', 'TVC:SPX'], 'NQ=F': ['CME_MINI:NQ1!', 'TVC:NDX'], 'YM=F': ['CBOT_MINI:YM1!'],
 'RTY=F': ['CME_MINI:RTY1!'], 'BZ=F': ['ICEEUR:BRN1!', 'NYMEX:BB1!', 'TVC:UKOIL'], 'CL=F': ['NYMEX:CL1!', 'TVC:USOIL'],
 'HO=F': ['NYMEX:HO1!'], 'RB=F': ['NYMEX:RB1!'], 'NG=F': ['NYMEX:NG1!'], 'TTF=F': ['ICEENDEX:TFM1!', 'NYMEX:TTF1!'],
 'MTF=F': ['ICEEUR:ATW1!', 'NYMEX:MTF1!'], 'B0=F': ['NYMEX:B01!'], 'GC=F': ['COMEX:GC1!', 'TVC:GOLD', 'OANDA:XAUUSD'],
 'SI=F': ['COMEX:SI1!', 'TVC:SILVER', 'OANDA:XAGUSD'], 'PL=F': ['NYMEX:PL1!', 'TVC:PLATINUM'],
 'PA=F': ['NYMEX:PA1!', 'TVC:PALLADIUM'], 'HG=F': ['COMEX:HG1!', 'CAPITALCOM:COPPER'], 'ALI=F': ['COMEX:ALI1!'],
 'TIO=F': ['COMEX:TIO1!', 'SGX:FEF1!'], 'HRC=F': ['COMEX:HRC1!'], 'BUS=F': ['COMEX:BUS1!'], 'UX=F': ['COMEX:UX1!'],
 'ZW=F': ['CBOT:ZW1!'], 'KE=F': ['CBOT:KE1!'], 'ZC=F': ['CBOT:ZC1!'], 'ZS=F': ['CBOT:ZS1!'], 'ZL=F': ['CBOT:ZL1!'],
 'ZM=F': ['CBOT:ZM1!'], 'ZO=F': ['CBOT:ZO1!'], 'ZR=F': ['CBOT:ZR1!'], 'KC=F': ['ICEUS:KC1!'], 'CC=F': ['ICEUS:CC1!', 'ICEEUR:C1!'],
 'SB=F': ['ICEUS:SB1!'], 'CT=F': ['ICEUS:CT1!'], 'OJ=F': ['ICEUS:OJ1!'], 'HE=F': ['CME:HE1!'], 'LE=F': ['CME:LE1!'],
 'QA=F': ['FX:GBPAUD'], 'ZN=F': ['CBOT:ZN1!'], 'ZB=F': ['CBOT:ZB1!'], 'ZF=F': ['CBOT:ZF1!'], 'ZT=F': ['CBOT:ZT1!'],
 'SR3=F': ['CME:SR31!'], '2YY=F': ['CBOT:2YY1!'], 'DX-Y.NYB': ['TVC:DXY', 'ICEUS:DX1!'],
 # Kripto
 'BTC-USD': ['BITSTAMP:BTCUSD', 'COINBASE:BTCUSD', 'CRYPTO:BTCUSD'], 'ETH-USD': ['BITSTAMP:ETHUSD', 'COINBASE:ETHUSD'],
 'USDT-USD': ['KRAKEN:USDTUSD', 'COINBASE:USDTUSD', 'CRYPTOCAP:USDT'],
 # Tek tek özel durumlar
 'HSBK.IL': ['LSE:HSBK', 'KASE:HSBK', 'LSIN:HSBK'], 'ROSN.ME': ['MOEX:ROSN', 'RUS:ROSN'],
 'COMI.CA': ['EGX:COMI'], 'CNH=F': ['CME:CNH1!'], 'XIN9.FGI': ['FTSE:XIN9', 'TVC:XIN9', 'SGX:CN1!'],
 'HSTECH.HK': ['HSI:HSTECH', 'TVC:HSTECH'],
 'ALPEKA.MX': ['BMV:ALPEK/A', 'OTC:ALPKF'], 'BIMBOA.MX': ['BMV:BIMBO/A', 'OTC:BMBOY'], 'GFNORTEO.MX': ['BMV:GFNORTE/O', 'OTC:GBOOY'], 'MTELEKOM.BD': ['BET:MTELEKOM'],
}
# FX: =X çiftleri
FX_ORDER = ['FX', 'OANDA', 'FX_IDC', 'SAXO']
def fx_pair(sym):
    p = sym.replace('=X', '')
    if len(p) == 3:
        p = 'USD' + p
    return p
# Çin: kod verilmez; alternatif (cin ajanı veriyle test ediyor)
CHINA_ALT = {
 '000001.SS': 'AMEX:ASHR | CBOE:CNYA | AMEX:FXI', '000300.SS': 'AMEX:ASHR | CBOE:CNYA',
 '399001.SZ': 'AMEX:ASHR | CBOE:CNYA | AMEX:KWEB',
}
# HK: ABD/OTC/LSE alternatifleri (doğrulanacak)
HK_ALT = {
 '0700.HK': ['OTC:TCEHY'], '9988.HK': ['NYSE:BABA'], '0005.HK': ['LSE:HSBA', 'NYSE:HSBC'], '0386.HK': ['OTC:SNPMF'],
 '0857.HK': ['OTC:PCCYF'], '0883.HK': ['OTC:CEOHF'], '0941.HK': ['OTC:CHLKF'], '1211.HK': ['OTC:BYDDY'],
 '1398.HK': ['OTC:IDCBY'], '0939.HK': ['OTC:CICHY'], '1810.HK': ['OTC:XIACY'], '3690.HK': ['OTC:MPNGY'],
 '2318.HK': ['OTC:PNGAY'], '0388.HK': ['OTC:HKXCY'], '0001.HK': ['OTC:CKHUY'], '0016.HK': ['OTC:SUHJY'],
 '1928.HK': ['OTC:SCHYY'], '2899.HK': ['OTC:ZIJMY'], '1919.HK': ['OTC:CICOY'], '1088.HK': ['OTC:CSUAY'],
 '0902.HK': ['OTC:HUNGF'], '0753.HK': ['OTC:AIRYY'], '2382.HK': ['OTC:SOTGY'],
}
# Elle ek alternatifler (öncelikli listedeki çift listeli/ADR karşılıkları)
EXTRA_ALT = {
 'MT.AS': ['NYSE:MT'], 'MT': ['EURONEXT:MT'], 'STLAM.MI': ['NYSE:STLA', 'EURONEXT:STLAP'], 'STLA': ['MIL:STLAM'],
 'BBVA.MC': ['NYSE:BBVA'], 'BBVA': ['BME:BBVA'], 'RYA.IR': ['NASDAQ:RYAAY'], 'RYAAY': ['EURONEXT:RYA'],
 'IAG.L': ['BME:IAG', 'OTC:ICAGY'], 'AIR.PA': ['XETR:AIR', 'OTC:EADSY'], 'AIR.DE': ['EURONEXT:AIR'],
 'TITC.AT': ['EURONEXT:TITC'], 'TITC.BR': ['ATHEX:TITC'], 'TEN.MI': ['NYSE:TS'], 'TS': ['MIL:TEN'],
 'EDV.L': ['TSX:EDV'], 'ELD.TO': ['NYSE:EGO'], 'EGO': ['TSX:ELD'], 'K.TO': ['NYSE:KGC'], 'KGC': ['TSX:K'],
 'SHEL.L': ['NYSE:SHEL'], 'SHEL': ['LSE:SHEL'], 'HSBA.L': ['NYSE:HSBC'], 'ABI.BR': ['NYSE:BUD'], 'BUD': ['EURONEXT:ABI'],
 'VOD.L': ['NASDAQ:VOD'], 'VOD': ['LSE:VOD'], 'ING': ['EURONEXT:INGA'], 'INGA.AS': ['NYSE:ING'],
 'TKC': ['BIST:TCELL'], 'AKBTY': ['BIST:AKBNK'], 'TKGBY': ['BIST:GARAN'], 'BHP': ['ASX:BHP'], 'BHP.AX': ['NYSE:BHP'],
 'RIO': ['LSE:RIO'], 'RIO.L': ['NYSE:RIO'], 'GLEN.L': ['OTC:GLNCY'], 'TM': ['TSE:7203'], 'HMC': ['TSE:7267'],
 'LPL': ['KRX:034220'], '034220.KS': ['NYSE:LPL'], 'PKX': ['KRX:005490'], '005490.KS': ['NYSE:PKX'],
 'CCH.L': ['ATHEX:EEE'], 'HEIA.AS': ['OTC:HEINY'], 'TTE.PA': ['NYSE:TTE'], 'ENI.MI': ['NYSE:E'], 'EQNR.OL': ['NYSE:EQNR'],
 'REP.MC': ['OTC:REPYY'], 'BP.L': ['NYSE:BP'], 'SAN.MC': ['NYSE:SAN'], 'UBSG.SW': ['NYSE:UBS'], 'NESN.SW': ['OTC:NSRGY'],
 'BABA': ['HKEX:9988'], 'SSRM': ['TSX:SSRM'], 'NEM': ['TSX:NGT'],
}
# Öncelikli (tüm adayları sayfa ile doğrula)
PRIORITY_GROUPS = {'VIOP', 'idx', 'cmd', 'fx', 'rates', 'vol', 'tr_abroad'}
PRIORITY_SYMS = set('''TUR EEM EMB JETS ITA GDX GDXJ SLX XME FXI ASHR MCHI KWEB EUFN KBE CRAK KRBN GRID URA TKC AKBTY TKGBY BBVA
RHM.DE LDO.MI BA.L SAAB-B.ST KOG.OL HO.PA HAG.DE R3NK.DE BBVA.MC LHA.DE AF.PA IAG.L RYAAY WIZZ.L ADP.PA FRA.DE AENA.MC VLO
PKN.WA MOL.BD MOH.AT ELPE.AT MT MT.AS TKA.DE SZG.DE VOE.VI VALE TS NEM SSRM EGO CF NTR YAR.OL F STLA STLAM.MI RNO.PA VOW3.DE
WHR ELUX-B.ST 066570.KS 034220.KS 267260.KS 298040.KS 010120.KS 012450.KS 064350.KS 079550.KS ENR.DE GEV SGO.PA OI HEI.DE
HOLN.SW CX LYB BAS.DE 051910.KS IVL.BK ALPEKA.MX RELIANCE.NS 2010.SR 3402.T KO CCH.L HEIA.AS ABI.BR RYA.IR'''.split())

def main():
    rows = list(csv.DictReader(open(os.path.join(BASE, 'data', 'catalog.csv'), encoding='utf8')))
    out = []
    for r in rows:
        s, ex, g = r['sym'], r['exch'], r['group']
        d = {'yahoo': s, 'name': r['name'], 'group': g, 'exch': ex, 'type': r['type'], 'cands': [], 'alt_cands': [],
             'china': False, 'hk': False, 'priority': (g in PRIORITY_GROUPS) or (s in PRIORITY_SYMS) or (ex == 'Istanbul')}
        if ex in CHINA:
            d['china'] = True; d['china_alt'] = CHINA_ALT.get(s, '')
            alts = [a.strip() for a in d['china_alt'].split('|') if a.strip()]
            d['alt_cands'] = alts
        elif s in OV:
            d['cands'] = OV[s]
        elif r['type'] == 'CURRENCY' or s.endswith('=X'):
            p = fx_pair(s); d['cands'] = [f'{e}:{p}' for e in FX_ORDER]
        else:
            m = mech(s, ex)
            d['cands'] = [m] if m else []
            if ex == 'Cboe US':
                d['cands'] += [f'AMEX:{s}', f'NASDAQ:{s}']
            if ex == 'HKSE':
                d['hk'] = True; d['alt_cands'] = HK_ALT.get(s, [])
        d['alt_cands'] = d['alt_cands'] + EXTRA_ALT.get(s, [])
        if ex == 'Istanbul' and r['type'] == 'EQUITY' and g == 'VIOP':
            d['alt_cands'] = d['alt_cands'] + [f"BIST:{s.split('.')[0]}1!"]  # VİOP pay vadelisi sürekli kontrat
        out.append(d)
    # Katalogda olmayan ama istenen ekstra satırlar
    extra = [
     ('', 'VİOP BIST30 endeks vadeli (sürekli)', ['BIST:XU030D1!']), ('', 'VİOP Likit Banka endeks vadeli', ['BIST:XLBNKD1!']),
     ('', 'VİOP Banka Dışı Likit 10 vadeli', ['BIST:X10XBD1!']), ('', 'VİOP BIST Sürdürülebilirlik 25 vadeli', ['BIST:XSD25D1!']),
     ('', 'VİOP USDTRY vadeli (sürekli)', ['BIST:USDTRY1!']), ('', 'VİOP EURTRY vadeli', ['BIST:EURTRY1!']),
     ('', 'VİOP Altın (TL/gram) vadeli', ['BIST:XAUTRY1!']), ('', 'VİOP Gram gümüş vadeli', ['BIST:XAGTRY1!']),
     ('', 'VİOP BIST30 Aralık 2026 kontratı (örnek vade kodu)', ['BIST:XU030DZ2026']),
     ('', 'Türkiye 10Y tahvil faizi', ['TVC:TR10Y']), ('', 'Türkiye 2Y tahvil faizi', ['TVC:TR02Y']), ('', 'Türkiye 5Y tahvil faizi', ['TVC:TR05Y']),
     ('', 'ABD 2Y tahvil faizi', ['TVC:US02Y']), ('', 'Almanya 10Y', ['TVC:DE10Y']),
     ('', 'Türkiye 5Y CDS (TradingView aday)', ['TVC:TR5YCDS', 'ECONOMICS:TRCDS', 'TVC:TURKEY5Y']),
     ('', 'Ons altın TL (XAUTRY)', ['FX_IDC:XAUTRY', 'SAXO:XAUTRY', 'OANDA:XAUTRY']), ('', 'Brent CFD', ['TVC:UKOIL']),
     ('', 'WTI CFD', ['TVC:USOIL']), ('', 'Altın CFD', ['TVC:GOLD', 'OANDA:XAUUSD']), ('', 'Gümüş CFD', ['TVC:SILVER']),
     ('', 'SGX demir cevheri 62% (FEF)', ['SGX:FEF1!']), ('', 'LME bakır (gecikmeli)', ['LME:CA1!']),
     ('', 'CME Bitcoin vadeli', ['CME:BTC1!']), ('', 'Euro Stoxx 50 vadeli (Eurex FESX)', ['EUREX:FESX1!']),
     ('', 'DAX vadeli (Eurex FDAX)', ['EUREX:FDAX1!']), ('', 'Nikkei 225 vadeli (OSE)', ['OSE:NK2251!']),
     ('', 'Hang Seng vadeli', ['HKEX:HSI1!']), ('', 'FTSE China A50 vadeli (SGX)', ['SGX:CN1!']),
     ('', 'ICE Rotterdam kömür (API2)', ['ICEEUR:ATW1!']), ('', 'ICE Newcastle kömür', ['ICEEUR:NCF1!']),
     ('', 'Avrupa karbon (EUA) vadeli', ['ICEENDEX:ECF1!']), ('', 'ICEEUR:G1! = UK Short Gilt vadelisi (gasoil DEĞİL; LGO1!/GO1! 404)', ['ICEEUR:G1!']),
     ('', 'iShares MSCI Türkiye (TUR) — kontrol', ['NASDAQ:TUR']), ('', 'Halk/HSBC ADR', ['NYSE:HSBC']),
     ('', 'CBOE VIX vadeli', ['CBOE:VX1!']), ('', 'US Dollar Index vadeli', ['ICEUS:DX1!']),
    ]
    for y, nm, c in extra:
        out.append({'yahoo': y, 'name': nm, 'group': 'extra', 'exch': '', 'type': '', 'cands': c, 'alt_cands': [],
                    'china': False, 'hk': False, 'priority': True})
    json.dump(out, open(os.path.join(OUT, 'candidates.json'), 'w'), ensure_ascii=False, indent=0)
    n = sum(1 for d in out); p = sum(d['priority'] for d in out)
    print('rows', n, 'priority', p, 'unique cands', len({c for d in out for c in d['cands'] + d['alt_cands']}))
    print('no cand:', [d['yahoo'] for d in out if not d['cands'] and not d['china']])

if __name__ == '__main__':
    main()
