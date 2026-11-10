"""Denetim C0 lead-lag: bağımsız yardımcılar. lib.trades / lib.stats / lib.cost_bp / build_panel KULLANILMAZ.
Yalnız lib.load (toplam getiri düzeltmeli ETF fiyatı) veri katmanı olarak kullanılır; öncüler ham dosyalardan kurulur."""
import os, sys, math
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE); ROOT = os.path.dirname(KOD); DATA = os.path.join(ROOT, "data")
sys.path.insert(0, KOD)
import lib  # yalnız lib.load

LEADERS_ETF = ["SPY","QQQ","IWM","DIA","TLT","IEF","SHY","UUP","FXY","FXE","GLD","SLV","CPER","USO","BNO","UNG","UNL","USL",
               "HYG","LQD","EEM","FXI","KWEB","EWJ","SMH","XLE","XLF","KRE","XLK","GDX","XBI","IBIT","ETHA","BITO","DBA","TIP"]
_P = {}

def px(sym):
    if sym not in _P:
        _P[sym] = lib.load(sym)
    return _P[sym]

def my_cost(df, pos=2500.0):
    """Gidiş-dönüş bp: 2*1.5$/pos + makas kademesi (son 252 gün medyan dolar hacim) ve 1 sent taban."""
    t = df.tail(252)
    dv = float(np.nanmedian(t["raw_c"].values * t["v"].values))
    p = float(t["raw_c"].values[-1])
    if dv > 1e9: s = 1
    elif dv > 2e8: s = 2
    elif dv > 5e7: s = 4
    elif dv > 1e7: s = 8
    elif dv > 2e6: s = 15
    else: s = 35
    s = max(s, 100.0 / p)   # 0.01$/p * 1e4
    return 3.0 / pos * 1e4 + s

def spread_only(df):
    return my_cost(df) - 12.0

def _vol(name):
    return pd.read_parquet(os.path.join(DATA, "vol", name + ".parquet"))["close"].astype(float)

def _tsy(col, real=False):
    d = pd.read_parquet(os.path.join(DATA, "treasury", ("real" if real else "nominal") + ".parquet"))
    return pd.to_numeric(d[col], errors="coerce")

def _crypto16(pair):
    h = pd.read_parquet(os.path.join(DATA, "crypto", pair + "_h1.parquet"))
    idx = h.index.tz_convert("America/New_York")
    # Coinbase mum zaman damgası = mum BAŞLANGICI. 15:00 ET başlangıçlı mumun kapanışı = 16:00 ET fiyatı.
    m = pd.Series(h["c"].values, index=idx)
    m = m[m.index.hour == 15]
    d = m.index.tz_localize(None).normalize()
    m = pd.Series(m.values, index=d)
    return m[~m.index.duplicated(keep="last")]

def leaders(cal):
    """48 öncü, cal (SPY takvimi) üzerinde. ETF: log getiri; vol endeksleri: log değişim; Hazine: seviye farkı."""
    X = {}
    for L in LEADERS_ETF:
        p = os.path.join(DATA, "etf", L + ".parquet")
        if not os.path.exists(p): continue
        c = px(L)["c"]
        X[L] = np.log(c).diff().reindex(cal)     # kendi takviminde fark, sonra SPY takvimine
    vix = _vol("VIX").reindex(cal); v3 = _vol("VIX3M").reindex(cal)
    X["VIX_dlog"] = np.log(vix).diff()
    X["VIXTS_d"] = (vix / v3).diff()
    for nm in ["OVX", "GVZ", "VVIX"]:
        X[nm + "_dlog"] = np.log(_vol(nm).reindex(cal)).diff()
    X["BTC_16ET"] = np.log(_crypto16("BTC-USD").reindex(cal)).diff()
    X["ETH_16ET"] = np.log(_crypto16("ETH-USD").reindex(cal)).diff()
    d10 = _tsy("10 Yr"); d2 = _tsy("2 Yr"); d30 = _tsy("30 Yr"); r10 = _tsy("10 YR", real=True)
    X["DGS10_d"] = d10.reindex(cal).diff(); X["DGS2_d"] = d2.reindex(cal).diff(); X["DGS30_d"] = d30.reindex(cal).diff()
    X["DFII10_d"] = r10.reindex(cal).diff()
    X["T10YIE_d"] = (d10 - r10).dropna().reindex(cal).diff()
    return pd.DataFrame(X)

def zsc(x, n=60):
    sd = x.rolling(n).std().shift(1)
    return x / sd

def sim_greedy(sig, c, h):
    """Kendi C0 simülasyonum: sig[i] True ise c[i]'de al, c[i+h]'de sat; pozisyondayken gelen sinyaller atlanır;
    çıkış günü gelen sinyal aynı kapanışta yeniden girişe izin verir (i >= son giriş + h). Dönüş: giriş indeksleri, brüt getiri."""
    ev = np.flatnonzero(sig)
    n = len(c)
    ent = []
    nxt = -1
    for i in ev:
        if i < nxt: continue
        if i + h >= n: break
        ent.append(i); nxt = i + h
    ent = np.asarray(ent, dtype=int)
    g = c[ent + h] / c[ent] - 1 if len(ent) else np.array([])
    return ent, g

def tstat(x):
    x = np.asarray(x, float); n = len(x)
    if n < 2: return np.nan
    sd = x.std(ddof=1)
    return x.mean() / (sd / math.sqrt(n)) if sd > 0 else np.nan

def targets():
    scr = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv"))
    return scr[(scr["n"] >= 750) & (scr["med_dollar_vol_m"] >= 20)]["sym"].tolist()

def signals_for(T, X, kinds=("L_UP", "L_DN", "GERIDE", "ONDE"), thr=2.0, leaders_list=None):
    """Hedef T için {(L, kind): bool ndarray (T'nin kendi indeksinde)} ve T'nin kapanışları."""
    df = px(T)
    c = df["c"].values.astype(float)
    rT = np.log(df["c"]).diff()
    out = {}
    Ls = leaders_list if leaders_list is not None else list(X.columns)
    for L in Ls:
        if L == T: continue
        rL = X[L].reindex(df.index)
        if rL.notna().sum() < 400: continue
        if "L_UP" in kinds or "L_DN" in kinds:
            zL = zsc(rL)
            if "L_UP" in kinds: out[(L, "L_UP")] = (zL >= thr).values
            if "L_DN" in kinds: out[(L, "L_DN")] = (zL <= -thr).values
        if "GERIDE" in kinds or "ONDE" in kinds:
            beta = (rT.rolling(60).cov(rL) / rL.rolling(60).var()).shift(1)
            res = rT - beta * rL
            zr = res / res.rolling(60).std().shift(1)
            if "GERIDE" in kinds: out[(L, "GERIDE")] = (zr <= -thr).values
            if "ONDE" in kinds: out[(L, "ONDE")] = (zr >= thr).values
    for k in out:
        s = out[k].copy(); s[:80] = False; out[k] = s
    return out, c, df
