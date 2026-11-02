"""BANKA ajanı ortak yardımcıları (ll.py'yi DEĞİŞTİRMEZ, sadece kullanır).
Zamanlama: ll.py ZAMANLAMA KONVANSİYONU. lag k>0 => sürücü önde. BIST kapanışı 15:00 UTC.
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code")
import ll
OUT = SCR + "/out"; CODE = OUT + "/code_banka"; RES = CODE + "/res"
os.makedirs(RES, exist_ok=True)
BANKS = ["AKBNK", "GARAN", "YKBNK", "ISCTR", "HALKB", "VAKBN", "TSKB"]
STATE = ["HALKB", "VAKBN"]; PRIVATE = ["AKBNK", "GARAN", "YKBNK", "ISCTR"]
ALL = BANKS + ["XBANK"]
YIELDS = {"^TNX", "^FVX", "^IRX", "^TYX", "2YY=F"}  # seviye farkı (yüzde puan) kullanılır
FIX_FX = False  # 01.11.2026: ll.py artık FX_FIX=True ile "=X" serilerini kendisi kaydırıyor ve panel yeniden üretildi -> burada tekrar KAYDIRMA YOK (çift kaydırma önlenir)
SPLIT = pd.Timestamp("2021-01-01"); IS0 = pd.Timestamp("2014-01-01")
P = pd.read_parquet(SCR + "/data/panel_ret_bistcal.parquet")
D = pd.read_parquet(SCR + "/data/panel_decomp_bist.parquet")

def R(sym):
    """BIST takviminde günlük getiri (log). Getiri yerine getiri farkı: getiri serisi ise log getiri; YIELDS ise seviye farkı."""
    y = ll.T(sym) if sym in ll._BIST_SET else sym
    if sym in YIELDS:
        s = ll.daily(sym).diff()
        sd = s.rolling(250, min_periods=60).std().shift(1); s[(s.abs() > 12 * sd) & sd.notna()] = np.nan
        return s
    s = P[y].copy() if y in P.columns else ll.ret(y)
    if FIX_FX and sym.endswith("=X"):
        # Yahoo FX günlük kapanışı (ldate=t) ~00:00 UTC t fiyatıdır (saatlik ile doğrulandı) -> 1 gün geri kaydır:
        # düzeltilmiş r_t = 00:00 UTC t -> 00:00 UTC t+1 (BIST t seansı + ABD seansı t). ABD kapanışlı sürücüler gibi yorumla.
        s = s.shift(-1)
    return s

def dec(sym, comp):
    if (sym, comp) in D.columns: return D[(sym, comp)].copy()
    return ll.decomp(sym)[comp]

def xu(): return R("XU100")

def hc_t(y, x):
    """y=a+bx, White(HC0) t. z-skorlu => b ~ corr."""
    df = pd.concat([y, x], axis=1).dropna()
    if len(df) < 60: return np.nan, np.nan, len(df)
    a = df.iloc[:, 0].values; b = df.iloc[:, 1].values
    a = (a - a.mean()) / a.std(); b = (b - b.mean()) / b.std()
    beta = (a * b).sum() / (b * b).sum(); e = a - beta * b
    se = np.sqrt(((b * e) ** 2).sum()) / (b * b).sum()
    return float(np.corrcoef(a, b)[0, 1]), float(beta / se), len(df)

def nwt(y, x, lags=5):
    b, t, n = ll.nw_t((y - y.mean()) / y.std(), (x - x.mean()) / x.std(), lags)
    return t

def pc(a, b, ctrl):
    v, n = ll.partial_corr(a, b, ctrl if isinstance(ctrl, list) else [ctrl]); return v

def corr_win(a, b, start=None, end=None):
    df = pd.concat([a, b], axis=1).dropna()
    if start is not None: df = df[df.index >= pd.Timestamp(start)]
    if end is not None: df = df[df.index < pd.Timestamp(end)]
    return df.iloc[:, 0].corr(df.iloc[:, 1]) if len(df) > 40 else np.nan, len(df)

def yr_sign_frac(a, b, k=0, minn=100, start="2010-01-01"):
    df = pd.concat([a.rename("a"), b.shift(k).rename("b")], axis=1).dropna(); df = df[df.index >= start]
    full = df["a"].corr(df["b"])
    yc = df.groupby(df.index.year).apply(lambda x: x["a"].corr(x["b"]) if len(x) >= minn else np.nan).dropna()
    return float((np.sign(yc) == np.sign(full)).mean()) if len(yc) else np.nan, yc

def pair(stock, drv, start="2010-01-01", usd=False, d=None):
    """Standart metrik seti (BRIEF 2a-2c + stabilite)."""
    s = R(stock); m = xu()
    if usd: s = s - R("TRY=X")
    d = R(drv) if d is None else d
    st = pd.Timestamp(start); s = s[s.index >= st]; d = d[d.index >= st]
    last = s.dropna().index.max()
    o = {"stock": stock, "driver": drv}
    o["corr_full"], o["n"] = corr_win(s, d)
    o["corr_3y"], _ = corr_win(s, d, last - pd.DateOffset(years=3))
    o["corr_1y"], _ = corr_win(s, d, last - pd.DateOffset(years=1))
    o["pcorr_xu100"] = pc(s, d, m) if stock != "XU100" else np.nan
    df = pd.concat([s, d], axis=1).dropna(); o["beta"] = df.cov().iloc[0, 1] / df.iloc[:, 1].var()
    o["sync_t"] = nwt(df.iloc[:, 0], df.iloc[:, 1])
    o["yr_same_sign"], _ = yr_sign_frac(s, d, 0, start=start)
    o["is_corr"], _ = corr_win(s, d, IS0, SPLIT); o["oos_corr"], _ = corr_win(s, d, SPLIT)
    o["is_pc"] = pc(s[(s.index >= IS0) & (s.index < SPLIT)], d, m); o["oos_pc"] = pc(s[s.index >= SPLIT], d, m)
    # öncülük
    c1 = pd.concat([s, d.shift(1)], axis=1).dropna(); o["lag1_cc_corr"] = c1.iloc[:, 0].corr(c1.iloc[:, 1]); o["lag1_cc_t"] = nwt(c1.iloc[:, 0], c1.iloc[:, 1])
    if True:
        try:
            g = dec(stock, "gap"); it = dec(stock, "intra")
            if usd: pass
            for nm, y in [("gap", g), ("intra", it)]:
                x = pd.concat([y, d.shift(1)], axis=1).dropna()
                o[f"{nm}_corr"] = x.iloc[:, 0].corr(x.iloc[:, 1]); o[f"{nm}_t"] = nwt(x.iloc[:, 0], x.iloc[:, 1])
                xi = x[x.index < SPLIT]; xo = x[x.index >= SPLIT]
                o[f"{nm}_is_corr"] = xi.iloc[:, 0].corr(xi.iloc[:, 1]); o[f"{nm}_oos_corr"] = xo.iloc[:, 0].corr(xo.iloc[:, 1])
                o[f"{nm}_oos_t"] = nwt(xo.iloc[:, 0], xo.iloc[:, 1]) if len(xo) > 60 else np.nan
                o[f"{nm}_is_t"] = nwt(xi.iloc[:, 0], xi.iloc[:, 1]) if len(xi) > 60 else np.nan
            # gap'te piyasa ötesi: XU100 gap kontrollü
            o["gap_pc_xugap"] = pc(g, d.shift(1), dec("XU100", "gap"))
            o["intra_pc_xuintra"] = pc(it, d.shift(1), dec("XU100", "intra"))
        except Exception as e:
            o["err"] = str(e)
    # ters yön: hisse_{t-1} -> sürücü_t
    rv = pd.concat([d, s.shift(1)], axis=1).dropna(); o["rev_corr"] = rv.iloc[:, 0].corr(rv.iloc[:, 1]); o["rev_t"] = nwt(rv.iloc[:, 0], rv.iloc[:, 1])
    # ters yön hisse-özgü: XU100_{t-1} kontrollü
    o["rev_pc"] = pc(d, s.shift(1), m.shift(1)) if stock != "XU100" else np.nan
    # çok günlü sürüklenme: sürücü_{t-1} -> hisse cc t+1..t+4 (t+0 hariç)
    fwd = sum(s.shift(-k) for k in range(1, 5))
    x = pd.concat([fwd, d.shift(1)], axis=1).dropna(); o["drift_t1_4_corr"] = x.iloc[:, 0].corr(x.iloc[:, 1]); o["drift_t"] = nwt(x.iloc[:, 0], x.iloc[:, 1], lags=8)
    return o

def conf_label(o, kind="sync"):
    """BRIEF güven ölçeği (yaklaşık otomatik ilk etiket; raporda elle gözden geçirilir)."""
    if kind == "sync":
        big = abs(o.get("corr_full", 0)) >= 0.30 or abs(o.get("pcorr_xu100", 0)) >= 0.15
        same = np.sign(o.get("is_corr", 0)) == np.sign(o.get("oos_corr", 0)) == np.sign(o.get("corr_full", 0))
        yrs = o.get("yr_same_sign", 0) >= 0.75
        if big and same and yrs: return "YÜKSEK"
        if same and abs(o.get("sync_t", 0)) >= 3: return "ORTA"
        if abs(o.get("sync_t", 0)) >= 2: return "DÜŞÜK"
        return "ÇOK DÜŞÜK"
    return "?"
