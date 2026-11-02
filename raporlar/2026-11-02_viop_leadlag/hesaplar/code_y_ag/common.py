"""AĞ-SPILLOVER-REJİM ajanı (ag) — ortak veri/faktör tanımları.
Kaynak: data/panel_ret_bistcal.parquet (BIST takvimi, log getiri, FX_FIX ve ±%10,5 temizliği uygulanmış).
Zamanlama (ll.py konvansiyonu): sürücü_t = sürücünün yerel tarihi <= t olan son kapanışı. ABD/vadeli/FX kapanışları BIST
kapanışından (15:00 UTC) SONRA -> sürücü_t BIST kapanışı sonrası 3-9 saati de içerir; sürücü_{t-1} BIST_t açılış gap'ini besler.
"""
import os, sys, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, os.path.join(SCR, "code"))
OUT = os.path.join(SCR, "out"); CODE = os.path.join(OUT, "code_y_ag"); CACHE = os.path.join(CODE, "cache")
os.makedirs(CACHE, exist_ok=True)
from universe import VIOP
STOCKS = list(VIOP)
START, END = "2014-01-01", "2026-10-30"

GLOBAL = ["ES=F", "EEM", "^STOXX50E", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX"]
GL_NAME = {"ES=F": "S&P500 vadeli", "EEM": "EM hisse ETF", "^STOXX50E": "Euro Stoxx 50", "^VIX": "VIX",
           "DX-Y.NYB": "Dolar endeksi", "BZ=F": "Brent", "GC=F": "Altın", "^TNX": "ABD 10y faiz",
           "TRY=X": "USD/TRY", "TUR": "MSCI Türkiye ETF (NY)", "EMB": "EM USD tahvil ETF", "XU100.IS": "BIST 100"}
TV = {"ES=F": "CME_MINI:ES1!", "EEM": "AMEX:EEM", "^STOXX50E": "TVC:SX5E", "^VIX": "CBOE:VIX", "DX-Y.NYB": "TVC:DXY",
      "BZ=F": "ICEEUR:BRN1!", "GC=F": "COMEX:GC1!", "^TNX": "TVC:US10Y", "TRY=X": "FX:USDTRY", "TUR": "NASDAQ:TUR",
      "EMB": "NASDAQ:EMB", "XU100.IS": "BIST:XU100"}
# BIST kapanışından SONRA kapanan sürücüler (t+1 hizalama versiyonunda kaydırılır). Stoxx 15:30/16:30 UTC -> ~senkron, kaydırılmaz.
US_CLOSE = ["ES=F", "EEM", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX", "TRY=X", "TUR", "EMB"]

# Sektör/küme eşleştirmesi (eşit ağırlıklı, hisse HARİÇ akran ortalaması -> mekanik içerme yok)
CL = {
 "BANKA": ["AKBNK", "GARAN", "HALKB", "ISCTR", "VAKBN", "YKBNK", "TSKB", "ALBRK", "SKBNK"],
 "HOLDING": ["KCHOL", "SAHOL", "DOHOL", "ALARK", "AGHOL", "GLYHO"],
 "CELIK": ["EREGL", "KRDMD", "ISDMR", "BRSAN", "KBORU"],
 "ALTIN": ["TRALT", "TRMET", "TRENJ"],
 "CIMENTO": ["CIMSA", "OYAKC", "AKCNS", "NUHCM", "BTCIM", "BUCIM", "AFYON", "GOLTS", "KONYA", "BSOKE"],
 "PERAKENDE": ["BIMAS", "MGROS", "SOKM"],
 "GIDA_ICECEK": ["AEFES", "CCOLA", "ULKER", "TUKAS", "TABGD"],
 "HAVACILIK": ["THYAO", "PGSUS", "TAVHL", "CLEBI", "DOCO", "PASEU"],
 "OTOMOTIV": ["FROTO", "TOASO", "DOAS", "OTKAR", "TTRAK", "ASUZU", "KARSN", "BRISA"],
 "DAYANIKLI": ["ARCLK", "VESTL", "VESBE"],
 "ELEKTRIK": ["AKSEN", "ENJSA", "ODAS", "ZOREN", "AYDEM", "CANTE", "GWIND", "BIOEN", "ENERY", "AKFYE"],
 "ENERJI_EKIPMAN": ["ASTOR", "EUPWR", "GESAN", "CWENE", "SMRTG", "YEOTK", "ALFAS", "KONTR"],
 "RAFINERI": ["TUPRS", "AYGAZ", "PETKM"],
 "KIMYA": ["SASA", "PETKM", "AKSA", "KORDS", "ALKIM", "KMPUR"],
 "TARIM_KIMYA": ["GUBRF", "BAGFS", "HEKTS"],
 "TELEKOM": ["TCELL", "TTKOM"],
 "SAVUNMA": ["ASELS", "OTKAR", "SDTTR", "ALTNY"],
 "INSAAT": ["ENKAI", "TKFEN"],
 "GYO": ["EKGYO", "ISGYO", "RYGYO", "SNGYO", "ALGYO", "AKFGY", "PSGYO", "PEKGY"],
 "SANAYI_XUSIN": ["XUSIN"],  # SISE için net akran yok -> XUSIN (SISE'yi içerir: mekanik içerme notu)
}
SECT = {"AEFES": "GIDA_ICECEK", "AKBNK": "BANKA", "AKSEN": "ELEKTRIK", "ALARK": "HOLDING", "ARCLK": "DAYANIKLI", "ASELS": "SAVUNMA",
 "ASTOR": "ENERJI_EKIPMAN", "BIMAS": "PERAKENDE", "BRSAN": "CELIK", "CIMSA": "CIMENTO", "DOAS": "OTOMOTIV", "DOHOL": "HOLDING",
 "EKGYO": "GYO", "ENJSA": "ELEKTRIK", "ENKAI": "INSAAT", "EREGL": "CELIK", "FROTO": "OTOMOTIV", "GARAN": "BANKA", "GUBRF": "TARIM_KIMYA",
 "HALKB": "BANKA", "HEKTS": "TARIM_KIMYA", "ISCTR": "BANKA", "KCHOL": "HOLDING", "KRDMD": "CELIK", "MGROS": "PERAKENDE",
 "ODAS": "ELEKTRIK", "OYAKC": "CIMENTO", "PETKM": "KIMYA", "PGSUS": "HAVACILIK", "SAHOL": "HOLDING", "SASA": "KIMYA",
 "SISE": "SANAYI_XUSIN", "SOKM": "PERAKENDE", "TAVHL": "HAVACILIK", "TCELL": "TELEKOM", "THYAO": "HAVACILIK", "TKFEN": "INSAAT",
 "TOASO": "OTOMOTIV", "TRALT": "ALTIN", "TRMET": "ALTIN", "TSKB": "BANKA", "TTKOM": "TELEKOM", "TUPRS": "RAFINERI",
 "ULKER": "GIDA_ICECEK", "VAKBN": "BANKA", "VESTL": "DAYANIKLI", "YKBNK": "BANKA"}
PERIODS = {"2014-17": ("2014-01-01", "2017-12-31"), "2018-20": ("2018-01-01", "2020-12-31"), "2021-23": ("2021-01-01", "2023-12-31"),
           "2024-26": ("2024-01-01", "2026-10-30"), "son1y": ("2025-10-31", "2026-10-30"), "tam": ("2014-01-01", "2026-10-30")}
CRISES = {  # (başlangıç, bitiş, tür)
 "2015 Çin devalüasyonu": ("2015-08-11", "2015-09-30", "küresel"),
 "2016 darbe girişimi": ("2016-07-15", "2016-08-15", "yerel"),
 "2018 kur krizi": ("2018-08-01", "2018-09-14", "yerel"),
 "2020 COVID": ("2020-02-24", "2020-04-15", "küresel"),
 "2021 Ara TL çöküşü/KKM": ("2021-11-15", "2021-12-31", "yerel"),
 "2023 seçim+ortodoks dönüş": ("2023-05-15", "2023-07-14", "yerel"),
 "2024 Ağu carry çözülmesi": ("2024-08-01", "2024-08-20", "küresel"),
 "2025 Mar İmamoğlu+Nis tarife": ("2025-03-19", "2025-04-15", "yerel+küresel"),
 "2026 Eyl-Eki fon krizi": ("2026-09-01", "2026-10-30", "yerel"),
}

_P = None
def panel():
    global _P
    if _P is None:
        _P = pd.read_parquet(os.path.join(SCR, "data", "panel_ret_bistcal.parquet"))
        _P = _P[(_P.index >= "2013-06-01") & (_P.index <= END)]
    return _P

def col(s):
    P = panel()
    if s in P.columns: return s
    if s + ".IS" in P.columns: return s + ".IS"
    return None

def stock_rets():
    P = panel(); return P[[s + ".IS" for s in STOCKS]].rename(columns=lambda c: c[:-3])

def peer_factor(stock, R=None):
    """Hisse hariç küme akranlarının eşit ağırlıklı ortalaması (mevcut olanlar)."""
    P = panel(); cl = SECT[stock]; peers = [p for p in CL[cl] if p != stock]
    cols = [col(p) for p in peers if col(p) is not None]
    if not cols: return pd.Series(np.nan, index=P.index)
    X = P[cols]
    return X.mean(axis=1, skipna=True).where(X.notna().sum(axis=1) >= 1)

def factors():
    """Tüm faktör sütunları (BIST takvimi). _l1 = bir gün gecikmeli."""
    P = panel(); F = {}
    for g in GLOBAL + ["TRY=X", "TUR", "EMB"]:
        F[g] = P[g]; F[g + "_l1"] = P[g].shift(1)
    F["XU100"] = P["XU100.IS"]; F["XU100_l1"] = P["XU100.IS"].shift(1)
    return pd.DataFrame(F)

def ew_market_ex(stock):
    R = stock_rets(); return R.drop(columns=[stock]).mean(axis=1)

def dlog(x): return np.log(x).diff()
