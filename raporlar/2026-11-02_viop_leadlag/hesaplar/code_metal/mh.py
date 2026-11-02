"""METAL ajanı yardımcı modülü (ll.py'yi DEĞİŞTİRMEZ, üstüne kurar).
Kullanım: import sys; sys.path.insert(0, CODE_METAL); import mh
"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, os.path.join(SCR, "code"))
import ll  # noqa
OUT = os.path.join(SCR, "out")
CM = os.path.join(OUT, "code_metal")
RES = os.path.join(CM, "res"); os.makedirs(RES, exist_ok=True)
STOCKS = ["EREGL", "KRDMD", "TRALT", "TRMET", "BRSAN"]
SPLIT = pd.Timestamp("2021-01-01")
START = pd.Timestamp("2010-01-01")

# Asya/Avustralya: yerel kapanışı BIST açılışından (07:00 UTC) önce/başında -> lag0 zaten BIST açılışında bilinir
ASIA_PRE_OPEN = {".AX", ".T", ".KS", "^N225", "^KS11", "^AXJO", ".NS", ".BO", "^NSEI", "^BSESN"}  # NSE 10:00 UTC kapanır -> BIST açılışından SONRA!
def is_preopen(sym):
    # Sydney (05-06 UTC), Tokyo (06:00 UTC), Seul (06:30 UTC) kapanışları BIST sürekli işlem başlangıcından (07:00 UTC) önce.
    return sym.endswith(".AX") or sym.endswith(".T") or sym.endswith(".KS") or sym in ("^N225", "^KS11", "^AXJO")

def R(sym, usd=False):
    r = ll.ret(sym)
    if usd and ll.is_bist(ll.T(sym)):
        r = r - ll.ret("TRY=X")
    return r

_dec = {}
def D(stock):
    if stock not in _dec: _dec[stock] = ll.decomp(stock)
    return _dec[stock]

def weekly(r):
    return r.resample("W-FRI").sum(min_count=1)

def onsTL():
    """Ons altın TL: GC=F (USD) + USDTRY (log toplam). Not: GC=F kapanışı ~17:30 UTC settle / USDTRY Yahoo ~21-23 UTC -> ikisi de BIST kapanışından sonra."""
    return ll.ret("GC=F") + ll.ret("TRY=X")

def corr_t(a, b):
    """corr + NW t (z-skorlarla)."""
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(df) < 40: return np.nan, np.nan, len(df)
    c = df["a"].corr(df["b"])
    za = (df["a"] - df["a"].mean()) / df["a"].std(); zb = (df["b"] - df["b"].mean()) / df["b"].std()
    _, t, n = ll.nw_t(za, zb)
    return c, t, n

def pair_stats(stock, driver, usd=False, start=START, drv_series=None, drv_name=None):
    """Brief standardı: senkron (tam/3y/1y), kısmi|XU100, beta, haftalık, lag1 (cc/gap/intra), ters yön, yıllık işaret tutarlılığı, IS/OOS."""
    a = R(stock, usd=usd); b = drv_series if drv_series is not None else R(driver)
    a = a[a.index >= start]; b = b[b.index >= start]
    m = R("XU100", usd=usd)
    out = {"stock": stock, "driver": drv_name or driver, "usd": usd}
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    df = df[(df["b"] != 0)]  # tatil ffill sıfırlarını at (sürücü işlem görmedi)
    last = df.index.max()
    for lab, st_ in [("full", None), ("3y", last - pd.DateOffset(years=3)), ("1y", last - pd.DateOffset(years=1))]:
        x = df if st_ is None else df[df.index >= st_]
        out[f"corr_{lab}"] = x["a"].corr(x["b"]) if len(x) > 40 else np.nan
    out["n"] = len(df)
    out["pcorr_xu100"], _ = ll.partial_corr(df["a"], df["b"], [m])
    out["beta"] = np.cov(df["a"], df["b"])[0, 1] / df["b"].var()
    c0, t0, _ = corr_t(df["a"], df["b"]); out["t_sync"] = t0
    # haftalık (eşzamansız kapanışı yok eder)
    wa, wb = weekly(a), weekly(b)
    out["corr_weekly"], _, _ = corr_t(wa, wb)
    wm = weekly(m); out["pcorr_weekly"], _ = ll.partial_corr(wa, wb, [wm])
    # IS / OOS senkron
    x = df[df.index < SPLIT]; y = df[df.index >= SPLIT]
    out["corr_IS"] = x["a"].corr(x["b"]) if len(x) > 40 else np.nan
    out["corr_OOS"] = y["a"].corr(y["b"]) if len(y) > 40 else np.nan
    yr = df.groupby(df.index.year).apply(lambda z: z["a"].corr(z["b"]) if len(z) > 40 else np.nan).dropna()
    s0 = np.sign(out["corr_full"]); out["yr_same_sign"] = float((np.sign(yr) == s0).mean()) if len(yr) else np.nan
    out["yr_n"] = len(yr)
    # lag1: sürücü_{t-1} -> hisse_t
    bl = b.where(b != 0).shift(1)
    out["corr_lag1"], out["t_lag1"], _ = corr_t(a, bl)
    # ters: hisse_{t-1} -> sürücü_t
    out["corr_rev"], out["t_rev"], _ = corr_t(b.where(b != 0), a.shift(1))
    if ll.is_bist(ll.T(stock)):
        dd = D(stock); dd = dd[dd.index >= max(start, pd.Timestamp("2014-01-01"))]
        g, i = dd["gap"], dd["intra"]
        if usd:  # USD bazlı gap: kur hareketini gap'ten düş (yaklaşık)
            pass
        out["gap_corr"], out["gap_t"], _ = corr_t(g, bl)
        out["intra_corr"], out["intra_t"], _ = corr_t(i, bl)
        # IS/OOS lag1 intra
        out["intra_corr_IS"], out["intra_t_IS"], _ = corr_t(i[i.index < SPLIT], bl)
        out["intra_corr_OOS"], out["intra_t_OOS"], _ = corr_t(i[i.index >= SPLIT], bl)
        # lag0 sürücü -> gap (Asya öncesi-açılış sürücüleri için anlamlı) ve intra
        b0 = b.where(b != 0)
        out["gap0_corr"], out["gap0_t"], _ = corr_t(g, b0)
        out["intra0_corr"], out["intra0_t"], _ = corr_t(i, b0)
        # çok günlü sürüklenme: sürücü_{t-1} -> hisse cc t+1..t+4 (t+0 hariç)
        fwd = sum(a.shift(-k) for k in range(1, 5))
        out["drift_corr"], out["drift_t"], _ = corr_t(fwd, bl)
    return out

def tv(sym):
    m = {"GC=F": "COMEX:GC1!", "SI=F": "COMEX:SI1!", "HG=F": "COMEX:HG1!", "ALI=F": "COMEX:ALI1!", "TIO=F": "COMEX:TIO1!",
         "HRC=F": "COMEX:HRC1!", "BUS=F": "COMEX:BUS1!", "CL=F": "NYMEX:CL1!", "BZ=F": "ICEEUR:BRN1!", "NG=F": "NYMEX:NG1!",
         "TRY=X": "FX:USDTRY", "AUDUSD=X": "FX:AUDUSD", "DX-Y.NYB": "TVC:DXY", "^GSPC": "SP:SPX", "ES=F": "CME_MINI:ES1!",
         "PL=F": "NYMEX:PL1!", "PA=F": "NYMEX:PA1!", "MTF=F": "NYMEX:MTF1!?", "^TNX": "TVC:US10Y", "^VIX": "TVC:VIX",
         "XU100": "BIST:XU100", "ONS_TL": "FX_IDC:XAUTRY (veya OANDA:XAUUSD*FX:USDTRY)", "^HSI": "TVC:HSI (HKEX açılmayabilir)",
         "TEN.MI": "MIL:TEN", "MT.AS": "EURONEXT:MT", "TKA.DE": "XETR:TKA", "SZG.DE": "XETR:SZG", "VOE.VI": "VIE:VOE",
         "SSAB-A.ST": "OMXSTO:SSAB_A", "OUT1V.HE": "OMXHEX:OUT1V", "APAM.AS": "EURONEXT:APAM", "TATASTEEL.NS": "NSE:TATASTEEL",
         "JSWSTEEL.NS": "NSE:JSWSTEEL", "005490.KS": "KRX:005490", "5401.T": "TSE:5401", "FMG.AX": "ASX:FMG", "FRES.L": "LSE:FRES",
         "AAL.L": "LSE:AAL", "GLEN.L": "LSE:GLEN", "ANTO.L": "LSE:ANTO", "NHY.OL": "OSL:NHY", "K.TO": "TSX:K", "ELD.TO": "TSX:ELD",
         "CG.TO": "TSX:CG", "TXG.TO": "TSX:TXG", "2899.HK": "HKEX:2899 (açılmayabilir)", "ISDMR": "BIST:ISDMR", "KRDMA": "BIST:KRDMA",
         "KRDMB": "BIST:KRDMB", "TRENJ": "BIST:TRENJ", "ASHR": "AMEX:ASHR", "FXI": "AMEX:FXI", "MCHI": "NASDAQ:MCHI", "GLD": "AMEX:GLD",
         "GDX": "AMEX:GDX", "GDXJ": "AMEX:GDXJ", "SLX": "AMEX:SLX", "XME": "AMEX:XME", "OIH": "AMEX:OIH", "XOP": "AMEX:XOP",
         "COPX": "AMEX:COPX", "PICK": "BATS:PICK", "SIL": "AMEX:SIL", "TUR": "NASDAQ:TUR", "EEM": "AMEX:EEM", "XLE": "AMEX:XLE",
         "CPER": "AMEX:CPER", "REMX": "AMEX:REMX", "URA": "AMEX:URA", "LIT": "AMEX:LIT", "TIP": "NASDAQ:TIP", "ZAR=X": "FX:USDZAR",
         "EURUSD=X": "FX:EURUSD", "CNH=X": "FX:USDCNH", "JPY=X": "FX:USDJPY", "BTC-USD": "BITSTAMP:BTCUSD"}
    if sym in m: return m[sym]
    if sym.endswith(".IS"): return "BIST:" + sym[:-3]
    if sym in ll._BIST_SET: return "BIST:" + sym
    if all(c.isalpha() or c == "-" for c in sym) and sym.isupper(): return "NYSE:" + sym + "?"
    return "?"
