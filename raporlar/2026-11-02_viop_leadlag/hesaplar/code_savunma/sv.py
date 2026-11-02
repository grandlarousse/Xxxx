"""SAVUNMA-TELEKOM ajanı ortak yardımcıları (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
ASELS, TCELL, TTKOM için sürücü testleri.
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ll
OUT = SCR + "/out"
CODE = OUT + "/code_savunma"
RES = CODE + "/res"
os.makedirs(RES, exist_ok=True)

IS_END = pd.Timestamp("2020-12-31"); OOS_START = pd.Timestamp("2021-01-01")
START = pd.Timestamp("2010-01-01"); DSTART = pd.Timestamp("2014-01-01")

_panel = None
def panel():
    global _panel
    if _panel is None:
        _panel = pd.read_parquet(SCR + "/data/panel_ret_bistcal.parquet")
        _panel.index = pd.DatetimeIndex(_panel.index)
    return _panel

def fx_aligned(sym="TRY=X"):
    """VERİ TUZAĞI DÜZELTMESİ: Yahoo günlük FX barı (tarih D) 'c' alanı ~00:00 UTC D (= D-1 NY kapanışı sonrası) fiyatıdır
    (2011+ TRY=X, 2013+ EURTRY=X; saatlik veriyle doğrulandı: corr(günlük_D, saatlik D 00:30) = 0.88-1.0).
    Bu fonksiyon barı bir önceki iş gününe kaydırır -> BIST günü t için kur = ~00:00 UTC (t+1) fiyatı (BIST kapanışından ~9 saat sonra).
    2011 öncesi kaydırma yapılmaz (o dönemde lag0 baskın)."""
    d = ll.raw(sym); s = pd.Series(d["c"].values, index=pd.DatetimeIndex(d["ldate"].values)).astype(float)
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0]
    cut = pd.Timestamp("2011-01-01" if sym == "TRY=X" else "2013-01-01")
    new_idx = s.index.where(s.index < cut, s.index - pd.offsets.BDay(1))
    s = pd.Series(s.values, index=new_idx); s = s[~s.index.duplicated(keep="last")].sort_index()
    cal = ll.bist_cal(); cal = cal[cal >= s.index[0]]
    s = s.reindex(s.index.union(cal)).ffill().reindex(cal)
    r = np.log(s).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r

def R(sym):
    """BIST takviminde günlük log getiri. Panelden (hızlı); yoksa ll.ret."""
    p = panel()
    if sym in ("FXAL", "TRY=X_AL"): return fx_aligned("TRY=X")
    if sym == "EURTRY_AL": return fx_aligned("EURTRY=X")
    if sym in p.columns: return p[sym].astype(float)
    if sym + ".IS" in p.columns: return p[sym + ".IS"].astype(float)
    return ll.ret(sym)

def basket(syms, min_n=2):
    p = pd.concat([R(s).rename(s) for s in syms], axis=1)
    m = p.mean(axis=1, skipna=True); m[p.notna().sum(axis=1) < min_n] = np.nan
    return m

EU_DEF = ["RHM.DE", "BA.L", "LDO.MI", "HO.PA", "SAAB-B.ST", "KOG.OL", "HAG.DE", "R3NK.DE"]
US_DEF = ["LMT", "NOC", "RTX", "GD", "LHX"]
KR_DEF = ["012450.KS", "064350.KS", "079550.KS", "047810.KS"]
EU_TEL = ["DTE.DE", "ORA.PA", "TEF.MC", "VOD.L", "TEL.OL", "TELIA.ST", "KPN.AS", "HTO.AT"]
EM_TEL = ["MTN.JO", "VOD.JO", "AMX", "TIMB", "BHARTIARTL.NS", "OPL.WA", "MTELEKOM.BD", "TLKM.JK", "VEON"]

def drv(name):
    if name == "EU_DEF": return basket(EU_DEF, 3)
    if name == "US_DEF": return basket(US_DEF, 3)
    if name == "KR_DEF": return basket(KR_DEF, 2)
    if name == "EU_TEL": return basket(EU_TEL, 4)
    if name == "EM_TEL": return basket(EM_TEL, 4)
    return R(name)

def _corr(a, b, start=None, end=None):
    df = pd.concat([a, b], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index <= pd.Timestamp(end)]
    if len(df) < 40: return np.nan, len(df)
    return df.iloc[:, 0].corr(df.iloc[:, 1]), len(df)

def tstat_corr(a, b, start=None, end=None):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index <= pd.Timestamp(end)]
    if len(df) < 40: return np.nan, np.nan, len(df)
    za = (df.a - df.a.mean()) / df.a.std(); zb = (df.b - df.b.mean()) / df.b.std()
    b_, t, n = ll.nw_t(za, zb)
    return df.a.corr(df.b), t, n

def year_sign_frac(a, b, sign):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    yc = df.groupby(df.index.year).apply(lambda x: x.a.corr(x.b) if len(x) > 40 else np.nan).dropna()
    if len(yc) == 0: return np.nan, yc
    return float((np.sign(yc) == sign).mean()), yc

def pair(stock, dname, d=None, start=START):
    """Standart metrik seti. stock: 'ASELS'. dname: sürücü adı. d: sürücü serisi (opsiyonel)."""
    a = R(stock); m = R("XU100"); b = drv(dname) if d is None else d
    a = a[a.index >= start]; b = b[b.index >= start]
    dd = ll.decomp(stock); dd = dd[dd.index >= DSTART]
    last = a.dropna().index.max()
    o = {"stock": stock, "driver": dname}
    o["corr_full"], o["n"] = _corr(a, b)
    o["corr_3y"], _ = _corr(a, b, last - pd.DateOffset(years=3))
    o["corr_1y"], _ = _corr(a, b, last - pd.DateOffset(years=1))
    o["pcorr_xu100"], _ = ll.partial_corr(a, b, [m])
    x = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    o["beta"] = np.polyfit(x.b, x.a, 1)[0] if len(x) > 40 else np.nan
    o["c_is"], _ = _corr(a, b, DSTART, IS_END); o["c_oos"], _ = _corr(a, b, OOS_START)
    o["pc_is"], _ = ll.partial_corr(a[(a.index >= DSTART) & (a.index <= IS_END)], b, [m])
    o["pc_oos"], _ = ll.partial_corr(a[a.index >= OOS_START], b, [m])
    o["c0_t"] = tstat_corr(a, b)[1]
    fr, _ = year_sign_frac(a, b, np.sign(o["corr_full"]) if pd.notna(o["corr_full"]) else 1)
    o["yr_same_sign"] = fr
    # lead (lag1) cc / gap / intra
    b1 = b.shift(1)
    o["lag1_cc"], o["lag1_cc_t"], _ = tstat_corr(a, b1)
    o["gap_l1"], o["gap_l1_t"], o["n_gap"] = tstat_corr(dd["gap"], b1)
    o["intra_l1"], o["intra_l1_t"], _ = tstat_corr(dd["intra"], b1)
    o["intra_l1_is"], o["intra_l1_is_t"], _ = tstat_corr(dd["intra"], b1, DSTART, IS_END)
    o["intra_l1_oos"], o["intra_l1_oos_t"], _ = tstat_corr(dd["intra"], b1, OOS_START)
    o["gap_l1_is"], _, _ = tstat_corr(dd["gap"], b1, DSTART, IS_END)
    o["gap_l1_oos"], _, _ = tstat_corr(dd["gap"], b1, OOS_START)
    # lag0 -> gap / intra (Asya sürücüleri için lag0 zaten BIST seansından önce)
    o["gap_l0"], o["gap_l0_t"], _ = tstat_corr(dd["gap"], b)
    o["intra_l0"], o["intra_l0_t"], _ = tstat_corr(dd["intra"], b)
    # multi-day drift t+2..t+5: corr(sum a_{t+1..t+4}? ) -> corr(a_t, sum b_{t-2..t-5})
    b25 = b.shift(2).rolling(4).sum()
    o["lag2_5"], o["lag2_5_t"], _ = tstat_corr(a, b25)
    # reverse: stock_{t-1} -> driver_t
    o["rev_l1"], o["rev_l1_t"], _ = tstat_corr(b, a.shift(1))
    return o

def fmt(df, cols=None, nd=3):
    d = df.copy()
    for c in d.columns:
        if d[c].dtype.kind == "f": d[c] = d[c].round(nd)
    return d if cols is None else d[cols]
