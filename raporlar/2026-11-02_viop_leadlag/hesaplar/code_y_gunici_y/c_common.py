"""gunici_y (YURT İÇİ GÜN-İÇİ LEAD-LAG) ortak yardımcıları. ll.py'yi DEĞİŞTİRMEZ, sadece okur.

BAR YAPISI (bu ajan doğruladı, 0_checks çıktısı):
- m5 (2026-08-07..2026-10-30, 60 gün, tamamı AB yaz saati / BIST UTC+3 sabit):
  06:55 barı = açılış müzayedesi fiyatı (c = günlük 'o', hacim 0). 07:00..14:55 = sürekli işlem (96 bar).
  15:00 kapanış müzayedesi barı sadece son günde var -> kapanış = GÜNLÜK 'c'. 14:55 barının c'si = 15:00 (müzayede öncesi) fiyatı.
  Bar 'o' = bardaki ilk işlem (%62'sinde önceki barın c'sine eşit -> tik ayrıklığı). Hisselerde sürekli işlemde hacim=0 bar ~%0;
  fiyat değişmeyen bar %9 (KRDMD) .. %51 (SASA, fiyat 1,45 TL; tik 0,01 = 69 bps).
- h1 (2023-11-30..2026-10-30): bar etiketi = başlangıç. 06:30 barı c = 07:30 fiyatı (yazın hacmi 0 görünür: Yahoo kusuru),
  07:30..13:30 tam saat, 14:30 barı (14:30-15:00) SADECE AB yaz saati aylarında var; kışın 14:30-15:00 parçası eksik.
  Bu yüzden yıl boyu tutarlı parçalar: O(günlük o) -> P0730 -> P0830 ... -> P1430 -> C(günlük c). Yazın ek: P1500 (müzayede öncesi).
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code"); import ll  # noqa
OUT = SCR + "/out"; CODE = OUT + "/code_y_gunici_y"; RES = CODE + "/res"; os.makedirs(RES, exist_ok=True)
from universe import VIOP  # noqa
IDXL = ["XU030", "XBANK", "XLBNK", "XUSIN", "XHOLD"]
STKL = ["GARAN", "AKBNK", "YKBNK", "ISCTR", "THYAO", "ASELS", "KCHOL", "TUPRS", "BIMAS", "EREGL", "SAHOL"]
LEADERS = IDXL + STKL
SECTOR = {
    "banka": ["AKBNK", "GARAN", "HALKB", "ISCTR", "TSKB", "VAKBN", "YKBNK"],
    "holding": ["KCHOL", "SAHOL", "DOHOL", "ALARK", "TKFEN", "ENKAI"],
    "metal": ["EREGL", "KRDMD", "BRSAN", "TRALT", "TRMET"],
    "perakende": ["BIMAS", "MGROS", "SOKM"],
    "gida": ["AEFES", "ULKER"],
    "ulasim": ["THYAO", "PGSUS", "TAVHL"],
    "otomotiv_dayanikli": ["FROTO", "TOASO", "DOAS", "ARCLK", "VESTL"],
    "enerji": ["AKSEN", "ENJSA", "ODAS", "ASTOR"],
    "kimya_petrol": ["PETKM", "SASA", "TUPRS", "GUBRF", "HEKTS"],
    "insaat_cam_gyo": ["CIMSA", "OYAKC", "SISE", "EKGYO"],
    "telekom": ["TCELL", "TTKOM"],
    "savunma": ["ASELS"],
}
SEC_OF = {s: k for k, v in SECTOR.items() for s in v}
SEC_IDX = {"banka": "XBANK", "holding": "XHOLD"}  # diğerleri için XUSIN / akran ortalaması


def tick_spot(p):
    """BIST pay piyasası fiyat adımı (yaklaşık tablo; 0_checks'te ampirik olarak doğrulanır)."""
    p = np.asarray(p, float)
    return np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)


# ------------------------------------------------------------------ m5 panel
_M5 = {}
def m5_days():
    d = ll.raw("XU030.IS", "m5"); d = d[~d.index.duplicated(keep="last")]
    hm = d.index.hour * 100 + d.index.minute
    dd = d[(hm >= 700) & (hm <= 1455)]
    nb = pd.Series(1, index=dd.index.tz_convert(None).normalize()).groupby(level=0).sum()
    return nb  # gün -> sürekli bar sayısı (96 tam gün; yarım gün daha az)

SLOTS = pd.timedelta_range("06:55:00", "14:55:00", freq="5min")  # 97 slot (0 = açılış müzayedesi)

def m5_panel(sym):
    """dict: C,O,H,L,V (gün x 97). Eksik bar: C ileri doldurulur (bayat), V=0, O=H=L=C. Gün listesi m5_days()."""
    if sym in _M5: return _M5[sym]
    nb = m5_days(); days = nb.index
    d = ll.raw(ll.T(sym), "m5"); d = d[~d.index.duplicated(keep="last")].sort_index()
    t = d.index.tz_convert(None)
    day = t.normalize(); slot = t - day
    ok = day.isin(days) & (slot >= SLOTS[0]) & (slot <= SLOTS[-1])
    d = d[ok]; day = day[ok]; slot = slot[ok]
    di = days.get_indexer(day); si = ((slot - SLOTS[0]) / pd.Timedelta("5min")).astype(int)
    out = {}
    for f in ["c", "o", "h", "l", "v"]:
        A = np.full((len(days), len(SLOTS)), np.nan); A[di, si] = np.array(d[f].values, dtype=float); out[f.upper()] = A
    out["miss"] = np.isnan(out["C"])
    C = pd.DataFrame(out["C"]).ffill(axis=1).values.copy()
    # yarım gün: kapanıştan sonraki slotlar NaN kalsın
    for i, n in enumerate(nb.values):
        if n < 96: C[i, 1 + n:] = np.nan
    for f in ["O", "H", "L"]:
        A = out[f]; A[np.isnan(A)] = C[np.isnan(A)]; out[f] = A
    out["V"] = np.where(np.isnan(out["V"]), 0.0, out["V"]); out["C"] = C
    # günlük kapanış/açılış
    dl = ll.raw(ll.T(sym)).copy(); dl.index = pd.DatetimeIndex(dl["ldate"].values); dl = dl[~dl.index.duplicated(keep="last")]
    out["dO"] = dl["o"].reindex(days).values; out["dC"] = dl["c"].reindex(days).values; out["dV"] = dl["v"].reindex(days).values
    out["days"] = days; out["nb"] = nb.values
    _M5[sym] = out
    return out

def m5_ret(sym, kind="cc"):
    """gün x 96 getiri matrisi (slot 1..96 = 07:00..14:55 barları). kind='cc': log(C_t/C_{t-1}) (07:00 barı açılış müzayedesine göre);
    kind='oc': log(C_t/O_t) (bar içi: ilk işlemden son işleme; 'bayat son fiyat' sıçramasını dışlar)."""
    P = m5_panel(sym)
    if kind == "cc": R = np.log(P["C"][:, 1:] / P["C"][:, :-1])
    elif kind == "oc": R = np.log(P["C"][:, 1:] / P["O"][:, 1:])
    elif kind == "jump": R = np.log(P["O"][:, 1:] / P["C"][:, :-1])  # bar arası sıçrama (önceki son işlem -> ilk işlem)
    else: raise ValueError(kind)
    R[np.abs(R) > 0.08] = np.nan
    return R


# ------------------------------------------------------------------ h1 parçaları
_H1 = {}
H1_PIECES = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]  # O->07:30, 07:30->08:30, ..., 13:30->14:30, 14:30->C
def h1_days():
    h = ll.raw("XU030.IS", "h1"); h = h[~h.index.duplicated(keep="last")]
    hm = h.index.hour * 100 + h.index.minute
    day = pd.DatetimeIndex(h.index.tz_convert(None).normalize())
    nb = pd.Series(1, index=day).groupby(level=0).sum()
    has1430 = pd.Series(hm == 1430, index=day).groupby(level=0).any()
    df = pd.DataFrame({"nb": nb, "summer": has1430})
    df["half"] = df["nb"] <= 6
    return df

def h1_panel(sym):
    """DataFrame (gün): O, P0730..P1430, P1500 (yalnız yaz), C, gap (ll.decomp), cc, prevC + parça getirileri r1..r9, ca (müzayede, yaz), r9a (14:30-15:00 yaz)."""
    if sym in _H1: return _H1[sym]
    D = h1_days(); days = D.index
    h = ll.raw(ll.T(sym), "h1"); h = h[~h.index.duplicated(keep="last")].sort_index()
    hm = h.index.hour * 100 + h.index.minute; day = pd.DatetimeIndex(h.index.tz_convert(None).normalize())
    piv = pd.DataFrame({"d": day, "hm": hm, "c": h["c"].values}).pivot_table(index="d", columns="hm", values="c", aggfunc="last").reindex(days)
    dl = ll.raw(ll.T(sym)).copy(); dl.index = pd.DatetimeIndex(dl["ldate"].values); dl = dl[~dl.index.duplicated(keep="last")]
    if dl["v"].fillna(0).gt(0).mean() > 0.5: dl = dl[dl["v"].fillna(0) > 0]
    out = pd.DataFrame(index=days)
    out["O"] = dl["o"].reindex(days); out["C"] = dl["c"].reindex(days); out["V"] = dl["v"].reindex(days)
    labs = {630: "P0730", 730: "P0830", 830: "P0930", 930: "P1030", 1030: "P1130", 1130: "P1230", 1230: "P1330", 1330: "P1430", 1430: "P1500"}
    for k, v in labs.items(): out[v] = piv[k] if k in piv else np.nan
    dd = ll.decomp(sym).reindex(days)
    out["gap"] = dd["gap"]; out["cc"] = dd["cc"]; out["intra_dc"] = dd["intra"]
    seq = ["O", "P0730", "P0830", "P0930", "P1030", "P1130", "P1230", "P1330", "P1430", "C"]
    for i, nm in enumerate(H1_PIECES): out[nm] = np.log(out[seq[i + 1]] / out[seq[i]])
    out["intra"] = np.log(out["C"] / out["O"])
    out["r9a"] = np.log(out["P1500"] / out["P1430"]); out["ca"] = np.log(out["C"] / out["P1500"])
    nodaily = out["C"].notna().sum() < 100  # XLBNK/XHOLD: Yahoo günlük geçmişi yok -> r1 ve r9 NaN, r2..r8 kullanılır
    bad = D["half"].values | (out["intra_dc"].isna().values if not nodaily else False) | (out[H1_PIECES].abs() > 0.12).any(axis=1).values
    out.loc[bad, H1_PIECES + ["intra", "r9a", "ca"]] = np.nan
    out.loc[~D["summer"].values, ["r9a", "ca", "P1500"]] = np.nan
    out["summer"] = D["summer"].values; out["half"] = D["half"].values
    _H1[sym] = out
    return out


# ------------------------------------------------------------------ istatistik
def lagmat(X, k):
    """gün x bar matrisinde gün içi gecikme: X_{t-k}; gün başından önceki gecikmeler 0 (gün sınırını geçmez)."""
    L = np.zeros_like(X)
    if k == 0: return X.copy()
    L[:, k:] = X[:, :-k]
    return L

def ols_cl(y, X, groups):
    """OLS + gün kümelenmiş (cluster-robust) kovaryans. y (n,), X (n,p) sabit DAHİL DEĞİL -> eklenir. Dönüş: b, se, cov, r2, n."""
    X = np.column_stack([np.ones(len(y)), X])
    XtX = X.T @ X
    try: iXX = np.linalg.inv(XtX)
    except np.linalg.LinAlgError: iXX = np.linalg.pinv(XtX)
    b = iXX @ (X.T @ y); u = y - X @ b
    # cluster meat
    g = pd.factorize(groups)[0]; G = g.max() + 1
    S = np.zeros((G, X.shape[1])); np.add.at(S, g, X * u[:, None])
    meat = S.T @ S
    cov = iXX @ meat @ iXX * (G / (G - 1)) * ((len(y) - 1) / (len(y) - X.shape[1]))
    r2 = 1 - (u @ u) / (((y - y.mean()) ** 2).sum())
    return b, np.sqrt(np.clip(np.diag(cov), 0, None)), cov, r2, len(y)

def wald(b, cov, idx):
    from scipy import stats
    bb = b[idx]; V = cov[np.ix_(idx, idx)]
    try: w = float(bb @ np.linalg.solve(V, bb))
    except np.linalg.LinAlgError: return np.nan, np.nan
    return w, 1 - stats.chi2.cdf(w, len(idx))

def tsum(b, cov, idx):
    L = np.zeros(len(b)); L[idx] = 1
    s = L @ b; se = np.sqrt(L @ cov @ L); return s, s / se if se > 0 else np.nan

def nw_mean(x, lags=5):
    m, t, n = ll.nw_t(pd.Series(x).dropna(), None, lags); return m, t, n

def bt_stats(pnl, pos, ppy=252):
    pnl = pd.Series(pnl); pos = pd.Series(pos)
    act = pos != 0; n = int(act.sum())
    if n < 10: return {"n": n, "mean_bps": np.nan, "t": np.nan, "hit": np.nan, "sharpe": np.nan}
    pa = pnl[act]; m, t, _ = ll.nw_t(pa.reset_index(drop=True))
    vol = pnl.std() * np.sqrt(ppy)
    return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": t, "hit": float((pa > 0).mean()), "sharpe": pnl.mean() * ppy / vol if vol > 0 else np.nan}
