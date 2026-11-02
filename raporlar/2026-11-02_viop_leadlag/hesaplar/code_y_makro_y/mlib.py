"""makro_y yardımcı kütüphanesi (yurt içi makro/piyasa değişkenleri). ll.py'yi DEĞİŞTİRMEZ, sadece kullanır.
Zamanlama özeti (her seri için 'bilgi anı', UTC):
  y_*   : Yahoo günlük FX (ll.FX_FIX sonrası) -> UTC günü sonu (~24:00). BIST kapanışından ~9 saat SONRA biter.
  h15_* : Yahoo saatlik, 15:00 UTC anlık (BIST kapanışı) -> BIST cc ile tam senkron (2024-01+ FX, 2024-06+ altın).
  n_*   : gece hareketi 15:00 UTC(t-1) -> 06:00 UTC(t) (BIST açılışından önce bilinir).
  v_*   : VİOP vadeli uzlaşma fiyatı (aynı kontratın uzlaşma / önceki uzlaşma oranı; ~15:00-15:15 UTC) 2017-04+.
  ir_*  : VİOP USDTRY takvim yayılımından zımni TL faizi (yıllık %, ^IRX eklenir).
  dibs* : BAP kesin alım-satım kapanış bileşik getirisi (~14:00-14:30 UTC), gösterge-benzeri tahvil, aynı ISIN farkı.
  tlref : TLREF gecelik (yayın ~13:00 UTC; repo seansı içi).
"""
import os, sys, re, glob, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, S + "/code"); import ll
from universe import VIOP
D = S + "/out/code_y_makro_y"; RES = D + "/res"; os.makedirs(RES, exist_ok=True)
STOCKS = list(VIOP)
BANKS = ["AKBNK", "GARAN", "YKBNK", "ISCTR", "HALKB", "VAKBN", "TSKB"]
HOLD = ["KCHOL", "SAHOL", "ALARK", "DOHOL", "TKFEN"]
SPLIT = pd.Timestamp("2021-01-01")

_PD = None
def panel_decomp():
    global _PD
    if _PD is None: _PD = pd.read_parquet(S + "/data/panel_decomp_bist.parquet")
    return _PD
def dec(sym, col):
    p = panel_decomp()
    if (sym, col) in p.columns: return p[(sym, col)].astype(float)
    return ll.decomp(sym)[col]
def cc(sym): return ll.ret(sym if ("." in sym or sym in ll._BIST_SET) else sym + ".IS")

# ---------------- Yahoo FX / altın ----------------
def snap(sym, hhmm):
    s = ll.snap_daily(sym, hhmm); s.index = pd.DatetimeIndex(s.index); return s.astype(float)
def on_cal(s):
    cal = ll.bist_cal(); return s.reindex(cal)
def h15_ret(sym):
    """15:00 UTC anlık fiyattan BIST günleri arası log getiri (t-1 15:00 -> t 15:00)."""
    s = snap(sym, "15:00"); s = s.reindex(ll.bist_cal()); s = s[s.index >= s.first_valid_index()]
    return np.log(s).diff()
def night_ret(sym, a="15:00", b="06:00"):
    """Önceki BIST gününün a anından bugünün b anına (UTC) log getiri; index = bugünkü BIST günü."""
    cal = ll.bist_cal(); sa = snap(sym, a).reindex(cal); sb = snap(sym, b).reindex(cal)
    return np.log(sb) - np.log(sa.shift(1))
def day_ret(sym, a="06:00", b="15:00"):
    cal = ll.bist_cal(); sa = snap(sym, a).reindex(cal); sb = snap(sym, b).reindex(cal)
    return np.log(sb) - np.log(sa)

# ---------------- VİOP ----------------
_VX = None
def viop_raw():
    global _VX
    if _VX is None:
        _VX = pd.read_parquet(RES + "/viop_fx.parquet")
        _VX["und"] = _VX["SOZLESME KODU"].str.extract(r"^F_([A-Z0-9]+?)(?:M)?(\d{4})$")[0]
    return _VX
def viop_front(root, min_days=2, by="oi"):
    """root ör. 'USDTRY' / 'EURTRY' / 'XAUTRY' / 'XAUUSD' / 'XU030'. Her gün: vadesine > min_days takvim günü kalan,
    açık pozisyonu en yüksek kontrat. ret = ln(uzlaşma/önceki uzlaşma) AYNI kontrat (roll sıçraması yok)."""
    v = viop_raw(); x = v[v["SOZLESME KODU"].str.match(rf"^F_{root}M?\d{{4}}$")].copy()
    x["dte"] = (x["VADE TARIHI"] - x["TARIH"]).dt.days
    x = x[(x["dte"] > min_days) & (x["UZLASMA FIYATI"] > 0)]
    x = x.sort_values(["TARIH", "ACIK POZISYON" if by == "oi" else "dte"], ascending=[True, by != "oi"])
    f = x.groupby("TARIH").head(1).set_index("TARIH")
    r = np.log(f["UZLASMA FIYATI"] / f["ONCEKI UZLASMA FIYATI"]).where(f["ONCEKI UZLASMA FIYATI"] > 0)
    out = pd.DataFrame({"ret": r, "settle": f["UZLASMA FIYATI"], "code": f["SOZLESME KODU"], "dte": f["dte"], "oi": f["ACIK POZISYON"], "vol_tl": f["ISLEM HACMI"]})
    return out
def viop_implied_rate(root="USDTRY", n1=0, n2=1, min_days=3):
    """Ardışık iki vadenin uzlaşma oranı -> forward-forward faiz farkı (yıllık %, sürekli). + ^IRX (USD 3a)."""
    v = viop_raw(); x = v[v["SOZLESME KODU"].str.match(rf"^F_{root}\d{{4}}$")].copy()
    x["dte"] = (x["VADE TARIHI"] - x["TARIH"]).dt.days
    x = x[(x["dte"] > min_days) & (x["UZLASMA FIYATI"] > 0)].sort_values(["TARIH", "dte"])
    rows = []
    for t, g in x.groupby("TARIH"):
        if len(g) <= n2: continue
        a, b = g.iloc[n1], g.iloc[n2]
        dd = b["dte"] - a["dte"]
        if dd < 15: continue
        rows.append((t, 100 * np.log(b["UZLASMA FIYATI"] / a["UZLASMA FIYATI"]) * 365 / dd, a["dte"], b["dte"], a["SOZLESME KODU"], b["SOZLESME KODU"]))
    o = pd.DataFrame(rows, columns=["t", "diff", "dte1", "dte2", "c1", "c2"]).set_index("t")
    irx = ll.daily("^IRX").reindex(o.index).ffill()  # % (ABD kapanışı ~20 UTC; t-1 değeri kullanılır -> bilgi anı uyumlu)
    irx = ll.daily("^IRX").shift(1).reindex(o.index).ffill()
    o["usd"] = 100 * np.log(1 + irx / 100); o["ir"] = o["diff"] + o["usd"]
    return o

# ---------------- TLREF ----------------
def tlref():
    p = S + "/dl_makro_y/TLREFORANI_D/TLREFORANI_D.csv"
    t = open(p, encoding="utf-16").read().splitlines()
    rows = []
    for ln in t[1:]:
        f = ln.split(";")
        if len(f) > 6 and re.match(r"\d{2}/\d{2}/\d{4}", f[0]):
            rows.append((pd.to_datetime(f[0], dayfirst=True), float(f[5])))
    return pd.Series(dict(rows)).sort_index()

# ---------------- TÜFE ----------------
def cpi_monthly():
    c = pd.read_csv(RES + "/tufe_tcmb.csv"); c["month"] = pd.PeriodIndex(c["month"], freq="M")
    return c.set_index("month").sort_index()

# ---------------- istatistik ----------------
import statsmodels.api as sm
def ols(y, X, lags=5, min_n=60):
    """y ~ const + X (DataFrame). Dönüş: (params Series, t Series, n, r2). HAC(NW) t."""
    df = pd.concat([y.rename("_y"), X], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    if len(df) < min_n: return None
    m = sm.OLS(df["_y"].values, sm.add_constant(df.drop(columns="_y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    cols = ["const"] + list(df.drop(columns="_y").columns)
    return pd.Series(m.params, cols), pd.Series(m.tvalues, cols), len(df), m.rsquared
def pcorr(a, b, ctrls):
    df = pd.concat([a.rename("a"), b.rename("b")] + [c.rename(f"c{i}") for i, c in enumerate(ctrls)], axis=1).dropna()
    if len(df) < 60: return np.nan, len(df)
    C = np.column_stack([np.ones(len(df))] + [df[f"c{i}"].values for i in range(len(ctrls))])
    ra = df["a"].values - C @ np.linalg.lstsq(C, df["a"].values, rcond=None)[0]
    rb = df["b"].values - C @ np.linalg.lstsq(C, df["b"].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1]), len(df)
def corr(a, b, start=None, end=None):
    df = pd.concat([a, b], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    return (df.iloc[:, 0].corr(df.iloc[:, 1]), len(df)) if len(df) > 30 else (np.nan, len(df))
def year_sign_share(a, b, sign):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    yc = df.groupby(df.index.year).apply(lambda x: x["a"].corr(x["b"]) if len(x) > 40 else np.nan).dropna()
    return float((np.sign(yc) == sign).mean()) if len(yc) else np.nan, yc
def zs(x): return (x - x.mean()) / x.std()
