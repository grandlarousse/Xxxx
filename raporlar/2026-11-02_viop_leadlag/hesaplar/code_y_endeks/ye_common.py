"""YURT İÇİ ENDEKS ajanı — ortak yardımcılar (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
Endeks verisi: İş Yatırım ChartData (isy_fetch.py) -> data/isy/{d,h1,m5}/<KOD>.parquet (Yahoo'da XU030/XU100/XBANK/XUSIN dışındaki
BIST endekslerinin günlük geçmişi YOK: tek satır). İş Yatırım günlük XU030 kapanışı Yahoo ile 2009-2026 birebir (getiri corr 0,99997).
"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code"); import ll  # noqa
ISY = SCR + "/data/isy"; OUT = SCR + "/out"; RES = OUT + "/code_y_endeks/results"
os.makedirs(RES, exist_ok=True)
END = pd.Timestamp("2026-10-30"); START = pd.Timestamp("2014-01-01"); SPLIT = pd.Timestamp("2021-01-01")
VIOP = ll.VIOP

IDX_DESC = {
 "XU100": "BIST 100", "XU030": "BIST 30", "XU050": "BIST 50", "XUTUM": "BIST Tüm", "XYUZO": "BIST 100 dışı 30 (orta ölçek; BIST100 hariç)",
 "XTUMY": "BIST Tüm-100 (BIST100 dışı tüm hisseler; küçük ölçek)", "XKOBI": "BIST KOBİ Sanayi", "XKTUM": "BIST Katılım Tüm", "XK030": "BIST Katılım 30",
 "XK100": "BIST Katılım 100", "XK050": "BIST Katılım 50", "XBANK": "BIST Banka", "XLBNK": "BIST Likit Banka", "X10XB": "BIST Banka Dışı Likit 10",
 "XHOLD": "BIST Holding ve Yatırım", "XUSIN": "BIST Sınai", "XUMAL": "BIST Mali", "XUHIZ": "BIST Hizmetler", "XUTEK": "BIST Teknoloji",
 "XULAS": "BIST Ulaştırma", "XELKT": "BIST Elektrik", "XGIDA": "BIST Gıda İçecek", "XKMYA": "BIST Kimya Petrol Plastik", "XMANA": "BIST Metal Ana",
 "XMADN": "BIST Madencilik", "XTAST": "BIST Taş Toprak", "XTEKS": "BIST Tekstil Deri", "XINSA": "BIST İnşaat", "XKAGT": "BIST Orman Kağıt Basım",
 "XBLSM": "BIST Bilişim", "XILTM": "BIST İletişim", "XTCRT": "BIST Ticaret", "XGMYO": "BIST GYO", "XSGRT": "BIST Sigorta", "XYORT": "BIST Menkul Kıymet YO",
 "XFINK": "BIST Finansal Kiralama Faktoring", "XAKUR": "BIST Aracı Kurumlar", "XSPOR": "BIST Spor", "XTRZM": "BIST Turizm", "XTMTU": "BIST Temettü",
 "XHARZ": "BIST Halka Arz", "XSD25": "BIST Sürdürülebilirlik 25", "XUSRD": "BIST Sürdürülebilirlik", "XKURY": "BIST Kurumsal Yönetim (ölçek endeksi DEĞİL)",
 "XBANA": "BIST Ana Pazar (yıldız dışı)", "XYLDZ": "BIST Yıldız Pazar", "XSIST": "BIST İstanbul (şehir)", "XMESY": "BIST Metal Eşya Makine", "XSRDK": "BIST Sürdürülebilirlik Katılım",
 "XU500": "BIST 500",
}
# Önsel sektör eşlemesi (BIST sektör sınıflaması; veriyle de R² ile seçiliyor)
SECT = {
 "AEFES": ["XGIDA", "XUSIN"], "AKBNK": ["XBANK", "XLBNK", "XUMAL"], "AKSEN": ["XELKT", "XUHIZ"], "ALARK": ["XHOLD", "XUMAL"], "ARCLK": ["XMESY", "XUSIN"],
 "ASELS": ["XMESY", "XUSIN", "XUTEK"], "ASTOR": ["XMESY", "XUSIN"], "BIMAS": ["XTCRT", "XUHIZ"], "BRSAN": ["XMANA", "XUSIN"], "CIMSA": ["XTAST", "XUSIN"],
 "DOAS": ["XTCRT", "XUHIZ"], "DOHOL": ["XHOLD", "XUMAL"], "EKGYO": ["XGMYO", "XUMAL"], "ENJSA": ["XELKT", "XUHIZ"], "ENKAI": ["XINSA", "XUHIZ"],
 "EREGL": ["XMANA", "XUSIN"], "FROTO": ["XMESY", "XUSIN"], "GARAN": ["XBANK", "XLBNK", "XUMAL"], "GUBRF": ["XKMYA", "XUSIN"], "HALKB": ["XBANK", "XLBNK", "XUMAL"],
 "HEKTS": ["XKMYA", "XUSIN"], "ISCTR": ["XBANK", "XLBNK", "XUMAL"], "KCHOL": ["XHOLD", "XUMAL"], "KRDMD": ["XMANA", "XUSIN"], "MGROS": ["XTCRT", "XUHIZ"],
 "ODAS": ["XELKT", "XUHIZ"], "OYAKC": ["XTAST", "XUSIN"], "PETKM": ["XKMYA", "XUSIN"], "PGSUS": ["XULAS", "XUHIZ"], "SAHOL": ["XHOLD", "XUMAL"],
 "SASA": ["XKMYA", "XUSIN"], "SISE": ["XHOLD", "XTAST", "XUSIN"], "SOKM": ["XTCRT", "XUHIZ"], "TAVHL": ["XULAS", "XUHIZ"], "TCELL": ["XILTM", "XUTEK", "XUHIZ"],
 "THYAO": ["XULAS", "XUHIZ"], "TKFEN": ["XHOLD", "XINSA", "XUMAL"], "TOASO": ["XMESY", "XUSIN"], "TRALT": ["XMADN", "XUSIN"], "TRMET": ["XMADN", "XHOLD"],
 "TSKB": ["XBANK", "XUMAL"], "TTKOM": ["XILTM", "XUHIZ"], "TUPRS": ["XKMYA", "XUSIN"], "ULKER": ["XGIDA", "XUSIN"], "VAKBN": ["XBANK", "XLBNK", "XUMAL"],
 "VESTL": ["XMESY", "XUSIN"], "YKBNK": ["XBANK", "XLBNK", "XUMAL"],
}
NATIONAL = ["XU100", "XU030", "XU050", "XUTUM", "XYUZO", "XTUMY", "XKTUM", "XK030", "XTMTU", "XHARZ", "XSD25", "XUSRD", "XKURY"]
SECTORS = ["XBANK", "XLBNK", "X10XB", "XHOLD", "XUSIN", "XUMAL", "XUHIZ", "XUTEK", "XULAS", "XELKT", "XGIDA", "XKMYA", "XMANA", "XMADN", "XTAST",
           "XTEKS", "XINSA", "XKAGT", "XBLSM", "XILTM", "XTCRT", "XGMYO", "XSGRT", "XMESY", "XTRZM", "XYORT", "XFINK"]

_tv = None
def tv(code):
    """TradingView kodu: tv_map.csv'de doğrulanmışsa onu, değilse 'BIST:<KOD>?'."""
    global _tv
    if _tv is None:
        m = pd.read_csv(OUT + "/tv_map.csv"); _tv = dict(zip(m["yahoo"].astype(str), m["tv_best"].astype(str)))
        p = RES + "/tv_check.csv"
        if os.path.exists(p):
            for _, r in pd.read_csv(p).iterrows():
                if r["ok"] == 1: _tv.setdefault(r["code"] + ".IS", "BIST:" + r["code"])
    c = code.replace(".IS", "")
    v = _tv.get(c + ".IS")
    return v if v and v != "nan" else f"BIST:{c}?"

_cal = None
def cal():
    global _cal
    if _cal is None: c = ll.bist_cal(); _cal = c[c <= END]
    return _cal

_ic = {}
def idx_px(code):
    if code not in _ic:
        d = pd.read_parquet(f"{ISY}/d/{code}.parquet")
        d = d[d["ldate"].dt.dayofweek < 5]
        s = pd.Series(d["px"].values, index=pd.DatetimeIndex(d["ldate"])).astype(float)
        s = s[~s.index.duplicated(keep="last")]; s = s[(s > 0) & (s.index <= END)]
        c = cal(); c = c[c >= s.index[0]]
        _ic[code] = s.reindex(s.index.union(c)).ffill().reindex(c)
    return _ic[code]

def idx_ret(code):
    r = np.log(idx_px(code)).diff()
    r[(r.abs() > 0.2)] = np.nan
    return r

def stk_ret(s):
    r = ll.ret(s); return r[r.index <= END]

_dc = {}
def stk_dec(s):
    if s not in _dc:
        d = ll.decomp(s); _dc[s] = d[d.index <= END]
    return _dc[s]

def turnover(s):
    d = ll.raw(ll.T(s)); x = pd.Series((d["v"] * d["c"]).values, index=pd.DatetimeIndex(d["ldate"].values))
    return x[~x.index.duplicated(keep="last")]

# ---------------- hızlı OLS + Newey-West ----------------
def ols_nw(y, X, lags=5, add_const=True):
    """y: (n,), X: (n,k) numpy. NaN satırları atar. Dönüş: beta(k+1), t(k+1), n, r2. NW (Bartlett) HAC."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if X.ndim == 1: X = X[:, None]
    ok = np.isfinite(y) & np.isfinite(X).all(1); y = y[ok]; X = X[ok]; n = len(y)
    if add_const: X = np.column_stack([np.ones(n), X])
    k = X.shape[1]
    if n < k + 30: return np.full(k, np.nan), np.full(k, np.nan), n, np.nan
    XtX_inv = np.linalg.pinv(X.T @ X); b = XtX_inv @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = u[L:].T @ u[:-L]; S += w * (G + G.T)
    V = XtX_inv @ S @ XtX_inv; se = np.sqrt(np.clip(np.diag(V), 1e-30, None))
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return b, b / se, n, r2

def zs(x):
    x = pd.Series(x); return (x - x.mean()) / x.std()

def frame(d, start=START, end=END):
    df = pd.concat(d, axis=1); return df[(df.index >= start) & (df.index <= end)]

REGIMES = {
 "2018_kur_krizi": ("2018-05-01", "2018-12-31"), "2021_Ara_KKM": ("2021-11-01", "2022-01-31"), "2023_Haz_ortodoks": ("2023-06-01", "2023-09-30"),
 "2025_Mar_Imamoglu": ("2025-03-19", "2025-05-31"), "2026_EylEki_fon_krizi": ("2026-09-01", "2026-10-30"),
}

_W = None
def weight_series(I, s, index):
    """NNLS tahmini ağırlık w_{I,s}(t): çeyrek başında tahmin (önceki 250 gün), çeyrek boyunca sabit. Yoksa 0."""
    global _W
    if _W is None: _W = pd.read_parquet(RES + "/weights.parquet")
    if (I, s) not in _W.columns: return pd.Series(0.0, index=index)
    w = _W[(I, s)].fillna(0.0)
    return w.reindex(w.index.union(index)).ffill().reindex(index).fillna(0.0)

def ex_ret(I, s, r_i=None, r_s=None):
    """Hisse-hariç endeks log getirisi: ((e^rI-1) - w (e^rs-1)) / (1-w)."""
    r_i = idx_ret(I) if r_i is None else r_i; r_s = stk_ret(s) if r_s is None else r_s
    df = pd.concat([r_i.rename("i"), r_s.rename("s")], axis=1)
    w = weight_series(I, s, df.index)
    x = ((np.exp(df["i"]) - 1) - w * (np.exp(df["s"]) - 1).fillna(0)) / (1 - w)
    return np.log1p(x)
