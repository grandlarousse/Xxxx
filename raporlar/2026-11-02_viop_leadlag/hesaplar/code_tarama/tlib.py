"""tarama ajanı yardımcı kütüphanesi (ll.py'ye dokunmaz; ondan bağımsız vektörize hesap).
Tüm korelasyonlar 'pairwise complete' örneklem üzerinde, maske matris çarpımlarıyla hesaplanır.
t istatistiği: heteroskedastisiteye dayanıklı (White/HC0, H0 altında): t = S_xy / sqrt(sum((x-mx)^2 (y-my)^2)).
"""
import os, sys, numpy as np, pandas as pd
from scipy import stats

SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DATA = os.path.join(SCR, "data"); OUT = os.path.join(SCR, "out"); CODE = os.path.join(OUT, "code_tarama")
CACHE = os.path.join(CODE, "cache"); os.makedirs(CACHE, exist_ok=True)
sys.path.insert(0, os.path.join(SCR, "code"))

START = "2014-01-01"; END = "2026-10-30"
WIN = {"full": ("2014-01-01", "2026-10-30"), "is": ("2014-01-01", "2020-12-31"), "oos": ("2021-01-01", "2026-10-30"),
       "3y": ("2023-10-31", "2026-10-30"), "1y": ("2025-10-31", "2026-10-30")}

VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
IDXROWS = ["XU100", "XU030", "XBANK"]
# Türkiye 'ayna' enstrümanları (TR varlığının yurtdışı kotasyonu veya TL kuru) -> mekanik ilişki
MIRROR = {"TUR", "TKC", "AKBTY", "TKGBY", "TYIDY", "YKBNY", "TURKF", "HALKF", "TRYUSD=X", "TRY=X", "EURTRY=X", "GBPTRY=X", "^XU100"}

def load_panels():
    P = pd.read_parquet(os.path.join(DATA, "panel_ret_bistcal.parquet"))
    P = P.loc[START:END]
    DP = pd.read_parquet(os.path.join(DATA, "panel_decomp_bist.parquet")).loc[START:END]
    return P, DP

# ---------------- kapanış saati kovası (UTC) ----------------
# asia_pre: BIST açılışından (07:00 UTC) ÖNCE kapanır -> lag0 bilgisi BIST gün-içi için işlenebilir
# asia_mid: ~07:00 UTC (Şanghay) ; during: BIST seansı sırasında kapanır (HK, Singapur, Hindistan, Körfez, İsrail, Mısır, J'burg)
# eu: BIST kapanışından 0,5-1,5 saat sonra ; us: ABD/vadeli/FX/kripto (20-24 UTC)
TZ_BUCKET = {"Asia/Tokyo": "asia_pre", "Asia/Seoul": "asia_pre", "Asia/Taipei": "asia_pre", "Australia/Sydney": "asia_pre",
             "Pacific/Auckland": "asia_pre", "Asia/Shanghai": "asia_mid", "Asia/Hong_Kong": "during", "Asia/Singapore": "during",
             "Asia/Jakarta": "during", "Asia/Kuala_Lumpur": "during", "Asia/Bangkok": "during", "Asia/Kolkata": "during",
             "Asia/Riyadh": "during", "Asia/Dubai": "during", "Asia/Qatar": "during", "Asia/Jerusalem": "during",
             "Africa/Cairo": "during", "Africa/Johannesburg": "during", "Europe/Moscow": "eu", "UTC": "us"}
def bucket(sym, tz, exch):
    if exch == "CCY": return "us"          # Yahoo FX günü ~22-23 UTC kapanır
    if isinstance(tz, str) and tz.startswith("Europe/"): return TZ_BUCKET.get(tz, "eu")
    if isinstance(tz, str) and tz.startswith("America/"): return "us"
    return TZ_BUCKET.get(tz, "us")

# ---------------- vektörize korelasyon ----------------
def _prep(A):
    A = np.asarray(A, float); M = ~np.isnan(A); A0 = np.where(M, A, 0.0); return A0, M.astype(float)

def mcorr(Y, X, need_t=True, min_n=250):
    """Y: T x a, X: T x b (NaN'li). Dönüş: corr (a x b), n, t_hc, beta (Y'nin X'e regresyon eğimi)."""
    Y0, My = _prep(Y); X0, Mx = _prep(X)
    N = My.T @ Mx
    Sy = Y0.T @ Mx; Sx = My.T @ X0
    Syy = (Y0 ** 2).T @ Mx; Sxx = My.T @ (X0 ** 2); Sxy = Y0.T @ X0
    with np.errstate(invalid="ignore", divide="ignore"):
        a = Sy / N; b = Sx / N
        cxy = Sxy - N * a * b; vy = Syy - N * a * a; vx = Sxx - N * b * b
        corr = cxy / np.sqrt(vy * vx); beta = cxy / vx
        t = np.full_like(corr, np.nan)
        if need_t:
            S22 = (Y0 ** 2).T @ (X0 ** 2); S21 = (Y0 ** 2).T @ X0; S12 = Y0.T @ (X0 ** 2)
            # sum (y-a)^2 (x-b)^2
            Q = (S22 - 2 * b * S21 + b * b * Syy - 2 * a * S12 + 4 * a * b * Sxy - 2 * a * b * b * Sy
                 + a * a * Sxx - 2 * a * a * b * Sx + N * a * a * b * b)
            t = cxy / np.sqrt(Q)
    bad = N < min_n
    corr[bad] = np.nan; t[bad] = np.nan; beta[bad] = np.nan
    return corr, N, t, beta

def resid(A, C):
    """A: T x m (NaN'li), C: T x k kontrol (NaN satırlar dışlanır). Her sütun kendi örnekleminde sabit+C'ye regres edilir; artık döner."""
    A = np.asarray(A, float); C = np.asarray(C, float)
    okc = ~np.isnan(C).any(1)
    Z = np.column_stack([np.ones(len(C)), np.where(okc[:, None], C, 0.0)])  # T x (k+1)
    M = (~np.isnan(A)) & okc[:, None]; A0 = np.where(M, A, 0.0); Mf = M.astype(float)
    K = Z.shape[1]
    # ZtZ per sütun: (m x K x K)
    ZZ = np.einsum("tp,tq->tpq", Z, Z).reshape(len(Z), K * K)
    G = (Mf.T @ ZZ).reshape(-1, K, K)
    h = (Z.T @ A0).T  # m x K
    G = G + np.eye(K)[None] * 1e-12
    B = np.linalg.solve(G, h[:, :, None])[:, :, 0]  # m x K
    R = A - Z @ B.T
    R[~M] = np.nan
    return R

def p_from_t(t): return 2 * stats.norm.sf(np.abs(t))

def bh(p, q):
    p = np.asarray(p, float); ok = ~np.isnan(p); out = np.zeros(len(p), bool)
    if ok.sum() == 0: return out, np.nan
    ps = np.sort(p[ok]); m = len(ps); thr = q * np.arange(1, m + 1) / m
    k = np.where(ps <= thr)[0]
    if len(k) == 0: return out, 0.0
    cut = ps[k.max()]; out[ok] = p[ok] <= cut; return out, cut

def bh_adj(p):
    p = np.asarray(p, float); ok = ~np.isnan(p); adj = np.full(len(p), np.nan)
    ps = p[ok]; m = len(ps); o = np.argsort(ps); r = np.empty(m); r[o] = np.arange(1, m + 1)
    a = ps * m / r; a_sorted = np.minimum.accumulate(a[o][::-1])[::-1]; aa = np.empty(m); aa[o] = np.minimum(a_sorted, 1)
    adj[ok] = aa; return adj

# ---------------- TradingView ticker adayı ----------------
TV_MANUAL = {
 "^GSPC": "SP:SPX", "^NDX": "NASDAQ:NDX", "^IXIC": "NASDAQ:IXIC", "^DJI": "DJ:DJI", "^RUT": "TVC:RUT", "^SOX": "NASDAQ:SOX",
 "ES=F": "CME_MINI:ES1!", "NQ=F": "CME_MINI:NQ1!", "YM=F": "CBOT_MINI:YM1!", "RTY=F": "CME_MINI:RTY1!",
 "^STOXX50E": "TVC:SX5E", "^STOXX": "TVC:SXXP", "^GDAXI": "XETR:DAX", "^FCHI": "EURONEXT:PX1", "^FTSE": "TVC:UKX",
 "FTSEMIB.MI": "TVC:FTMIB?", "^IBEX": "BME:IBC", "^AEX": "EURONEXT:AEX", "^SSMI": "SIX:SMI", "GD.AT": "ATHEX:GD?",
 "^N225": "TVC:NI225", "^KS11": "TVC:KOSPI", "^TWII": "TWSE:TAIEX", "^HSI": "TVC:HSI (açılmayabilir; alt: AMEX:EWH)",
 "^HSCE": "HSI:HSCEI? (açılmayabilir; alt: AMEX:FXI)", "000001.SS": "ÇİN-AÇILMAZ (alt: AMEX:ASHR)", "399001.SZ": "ÇİN-AÇILMAZ (alt: AMEX:ASHR)",
 "^BSESN": "BSE:SENSEX", "^NSEI": "NSE:NIFTY", "^BVSP": "BMFBOVESPA:IBOV", "^MXX": "BMV:ME", "^J203.JO": "JSE:J203?",
 "^TA125.TA": "TASE:TA125?", "^GSPTSE": "TSX:TSX", "^AXJO": "ASX:XJO", "^JKSE": "IDX:COMPOSITE", "^KLSE": "MYX:FBMKLCI?",
 "IMOEX.ME": "MOEX:IMOEX?", "^PSI20": "EURONEXT:PSI20", "^OMX": "OMXSTO:OMXS30", "^OSEAX": "OSL:OSEAX?", "^ATX": "VIE:ATX?",
 "^BFX": "EURONEXT:BEL20", "^STI": "TVC:STI", "^NZ50": "NZX:NZ50G?", "^MERV": "BCBA:IMV",
 "^VIX": "CBOE:VIX", "^VXN": "CBOE:VXN", "^MOVE": "TVC:MOVE?", "^VIX3M": "CBOE:VIX3M", "^OVX": "CBOE:OVX", "^GVZ": "CBOE:GVZ",
 "^VVIX": "CBOE:VVIX", "^SKEW": "CBOE:SKEW",
 "^TNX": "TVC:US10Y", "^FVX": "TVC:US05Y", "^IRX": "TVC:US03MY", "^TYX": "TVC:US30Y", "2YY=F": "CBOT:2YY1!",
 "ZN=F": "CBOT:ZN1!", "ZB=F": "CBOT:ZB1!", "ZT=F": "CBOT:ZT1!", "ZF=F": "CBOT:ZF1!",
 "TRY=X": "FX:USDTRY", "EURTRY=X": "FX:EURTRY", "GBPTRY=X": "FX:GBPTRY", "EURUSD=X": "FX:EURUSD", "JPY=X": "FX:USDJPY",
 "GBPUSD=X": "FX:GBPUSD", "CNY=X": "FX_IDC:USDCNY", "CNH=X": "FX:USDCNH", "ZAR=X": "FX:USDZAR", "BRL=X": "FX_IDC:USDBRL",
 "MXN=X": "FX:USDMXN", "RUB=X": "FX_IDC:USDRUB", "HUF=X": "FX:USDHUF", "PLN=X": "FX:USDPLN", "CZK=X": "FX_IDC:USDCZK",
 "INR=X": "FX_IDC:USDINR", "KRW=X": "FX_IDC:USDKRW", "IDR=X": "FX_IDC:USDIDR", "CHF=X": "FX:USDCHF", "AUDUSD=X": "FX:AUDUSD",
 "NZDUSD=X": "FX:NZDUSD", "CAD=X": "FX:USDCAD", "DX-Y.NYB": "TVC:DXY", "SAR=X": "FX_IDC:USDSAR", "AED=X": "FX_IDC:USDAED",
 "KZT=X": "FX_IDC:USDKZT", "EGP=X": "FX_IDC:USDEGP", "ILS=X": "FX_IDC:USDILS", "COP=X": "FX_IDC:USDCOP", "CLP=X": "FX_IDC:USDCLP",
 "UAH=X": "FX_IDC:USDUAH", "EURCHF=X": "FX:EURCHF", "EURPLN=X": "FX:EURPLN", "EURHUF=X": "FX:EURHUF",
 "BTC-USD": "BITSTAMP:BTCUSD", "ETH-USD": "BITSTAMP:ETHUSD", "USDT-USD": "?",
 "BZ=F": "ICEEUR:BRN1!", "CL=F": "NYMEX:CL1!", "HO=F": "NYMEX:HO1!", "RB=F": "NYMEX:RB1!", "NG=F": "NYMEX:NG1!",
 "TTF=F": "ICEENDEX:TFM1!", "MTF=F": "NYMEX:MTF1!?", "GC=F": "COMEX:GC1!", "SI=F": "COMEX:SI1!", "PL=F": "NYMEX:PL1!",
 "PA=F": "NYMEX:PA1!", "HG=F": "COMEX:HG1!", "ALI=F": "COMEX:ALI1!", "TIO=F": "COMEX:TIO1! (alt: SGX:FEF1!)", "HRC=F": "COMEX:HRC1!",
 "ZW=F": "CBOT:ZW1!", "KE=F": "CBOT:KE1!", "ZC=F": "CBOT:ZC1!", "ZS=F": "CBOT:ZS1!", "ZM=F": "CBOT:ZM1!", "ZL=F": "CBOT:ZL1!",
 "KC=F": "ICEUS:KC1!", "CC=F": "ICEUS:CC1!", "SB=F": "ICEUS:SB1!", "CT=F": "ICEUS:CT1!", "LE=F": "CME:LE1!", "HE=F": "CME:HE1!",
 "OJ=F": "ICEUS:OJ1!", "LBS=F": "CME:LBR1!", "ZR=F": "CBOT:ZR1!", "ZO=F": "CBOT:ZO1!", "UX=F": "COMEX:UX1!", "QA=F": "?", "BUS=F": "COMEX:BUS1!?",
}
SUFFIX_TV = {".DE": "XETR", ".PA": "EURONEXT", ".AS": "EURONEXT", ".BR": "EURONEXT", ".LS": "EURONEXT", ".IR": "EURONEXT", ".L": "LSE",
             ".MI": "MIL", ".MC": "BME", ".SW": "SIX", ".ST": "OMXSTO", ".OL": "OSL", ".HE": "OMXHEX", ".CO": "OMXCOP", ".WA": "GPW",
             ".BD": "BET", ".AT": "ATHEX", ".VI": "VIE", ".PR": "PSECZ", ".T": "TSE", ".KS": "KRX", ".TW": "TWSE", ".NS": "NSE",
             ".AX": "ASX", ".TO": "TSX", ".SA": "BMFBOVESPA", ".MX": "BMV", ".JO": "JSE", ".SR": "TADAWUL", ".QA": "QSE", ".CA": "EGX",
             ".JK": "IDX", ".BK": "SET", ".KL": "MYX", ".SI": "SGX", ".TA": "TASE", ".ME": "MOEX", ".IL": "LSIN", ".AE": "DFM", ".PS": "PSE"}
US_EXCH = {"NYSE": "NYSE", "NYSEArca": "AMEX", "NasdaqGS": "NASDAQ", "NasdaqGM": "NASDAQ", "NasdaqCM": "NASDAQ", "NYSE American": "AMEX",
           "Cboe US": "CBOE", "OTC Markets OTCPK": "OTC", "OTC Markets OTCQX": "OTC", "Nasdaq GIDS": "NASDAQ"}
def tv(sym, exch=None):
    if sym in TV_MANUAL: return TV_MANUAL[sym]
    if sym.endswith(".IS"): return "BIST:" + sym[:-3]
    if sym.endswith(".SS") or sym.endswith(".SZ"): return "ÇİN-AÇILMAZ"
    if sym.endswith(".HK"): return "HKEX:" + sym[:-3].lstrip("0") + " (açılmayabilir)"
    for suf, ex in SUFFIX_TV.items():
        if sym.endswith(suf):
            base = sym[: -len(suf)]
            q = "?" if suf in (".IR", ".KL", ".AE", ".IL", ".ME", ".PS") else ""
            return f"{ex}:{base.replace('-', '_')}{q}"
    if exch in US_EXCH: return f"{US_EXCH[exch]}:{sym.replace('-', '.')}"
    return sym + "?"

# ---------------- katalogda grubu '?' olan (sonradan eklenen) sürücüler için ad tabanlı grup ----------------
_KW = [("steel", ["Gold", "Zhaojin", "Zijin", "Steel", "Iron", "HBIS", "Baoshan", "Copper", "Aluminum", "Hongqiao", "CMOC", "Nickel", "South32", "IGO", "Rio Tinto"]),
       ("util", ["Coking", "Shenhua", "Natural Resource Partners"]),
       ("oil", ["PetroChina", "China Petroleum", "Genesis Energy"]),
       ("chem", ["Petrochemical", "Chemical", "Haihua", "Tongkun", "Xinfengming", "Methanex", "Albemarle", "Azoty", "K+S", "Fertiliz", "Agri-Nutrients", "CVR Partners", "KWS"]),
       ("cement", ["Cement", "Conch", "TCC Group", "Glass", "Kibing", "Ardagh"]),
       ("air", ["Air", "AerCap", "Accor", "Marriott", "Meli", "Carnival", "Royal Caribbean", "Trip.com", "JetBlue", "El Al"]),
       ("auto", ["Motor", "Automobile", "BYD", "Geely", "Great Wall", "Leapmotor", "NIO", "XPeng", "Li Auto", "Porsche", "Volvo Car", "Autonomous", "Electric Vehicle",
                 "Europe 600 Aut", "Contemporary Amperex", "Fuyao", "SAIC", "Midea", "Gree", "Hisense", "Haier", "TCL", "Skyworth", "Sony", "BOE", "AUO", "Innolux",
                 "Sieyuan", "TBEA", "XD Electric", "Iljin", "LS Corp", "Hammond", "Hitachi Energy", "Sewedy", "Chicago Rivet"]),
       ("bank", ["Bank"]), ("def", ["EHang"]), ("cons", ["Tencent", "Baidu", "Shenzhou"]),
       ("etf", ["ETF", "MSCI", "Insurance", "Golden Dragon", "Direxion", "Trust"])]
def regroup(sym, group, name):
    if group != "?" and isinstance(group, str): return group
    if sym.endswith("=X") or sym.endswith("=F"): return "fx"
    n = str(name)
    for g, kws in _KW:
        if any(k in n for k in kws): return g
    return "?"

# ---------------- hisse sektörü / beklenen sürücü grupları / mekanizma etiketi (rest.py ile aynı) ----------------
SECT = {"AKBNK": "bank", "GARAN": "bank", "HALKB": "bank", "ISCTR": "bank", "VAKBN": "bank", "YKBNK": "bank", "TSKB": "bank",
        "KCHOL": "hold", "SAHOL": "hold", "DOHOL": "hold", "ALARK": "hold", "THYAO": "air", "PGSUS": "air", "TAVHL": "airport",
        "AKSEN": "util", "ENJSA": "util", "ODAS": "util", "EREGL": "steel", "KRDMD": "steel", "BRSAN": "steel", "TRALT": "gold", "TRMET": "metal",
        "PETKM": "chem", "SASA": "chem", "HEKTS": "agro", "GUBRF": "agro", "SISE": "glass", "TUPRS": "oil", "FROTO": "auto", "TOASO": "auto",
        "DOAS": "auto", "ARCLK": "white", "VESTL": "white", "ASTOR": "eleq", "ASELS": "def", "BIMAS": "retail", "MGROS": "retail", "SOKM": "retail",
        "ULKER": "food", "AEFES": "bev", "CIMSA": "cement", "OYAKC": "cement", "ENKAI": "constr", "TKFEN": "constr", "EKGYO": "re", "TCELL": "tel", "TTKOM": "tel"}
EXP = {"bank": {"bank", "re"}, "hold": {"bank", "auto", "oil", "util", "cons", "cement"}, "air": {"air", "oil"}, "airport": {"air"}, "util": {"util"},
       "steel": {"steel", "cement", "auto"}, "gold": {"steel"}, "metal": {"steel"}, "chem": {"chem", "oil"}, "agro": {"chem"}, "glass": {"chem", "cement", "cons"},
       "oil": {"oil"}, "auto": {"auto"}, "white": {"auto", "cons"}, "eleq": {"auto", "util"}, "def": {"def"}, "retail": {"cons"}, "food": {"cons"},
       "bev": {"cons"}, "cement": {"cement"}, "constr": {"cement", "util", "oil", "chem"}, "re": {"re", "cement", "bank"}, "tel": {"tel"}}
MACRO = {"idx", "etf", "fx", "vol", "rates", "cmd"}
def mech(stock, drv, grp):
    s = SECT.get(stock, "?")
    if drv in MIRROR or grp == "tr_abroad": return "TR-ayna (mekanik)"
    if grp in EXP.get(s, set()): return f"sektör emsali ({grp})"
    if grp in MACRO: return f"makro/emtia ({grp})"
    return f"BEKLENMEYEN ({grp})"
