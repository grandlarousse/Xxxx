"""enerji_tarim ailesi: ortak yardımcılar (lib.py / strategies.py DEĞİŞTİRİLMEDEN genişletme).

Zamanlama sözleşmesi lib.py ile aynıdır: sinyal t kapanışına kadarki bilgiyle; olay takvimleri önceden bilinir.
Bu modül:
  * aile listesi, kopya kümeleri, PTP/K-1 bayrakları,
  * olay takvimi yükleyicileri (EIA, roll, vade),
  * test kaydı (her test tek yönlü p ile kaydedilir -> BH-FDR q=0.10),
  * tam istatistik standardı (n, brüt/net, kazanma, PF, t, IS/OOS, yıllar, maxDD, en kötü,
    maliyet duyarlılığı 1.000/2.500/10.000 $, C0/O1/C1 modları).
"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
from scipy import stats as st
import lib

ROOT = lib.ROOT
OUT = os.path.join(ROOT, "sonuclar", "aile_enerji_tarim"); os.makedirs(OUT, exist_ok=True)
EV = os.path.join(ROOT, "data", "events")

FAM = "USO BNO USL UCO SCO UNG UNL BOIL KOLD UGA DBO XLE DBC PDBC GSG DBA CORN WEAT SOYB CANE COMT BCI XOP OIH GUSH DRIP ERX ERY".split()

# Kopya / yakın kopya kümeleri (2022+ günlük getiri korelasyonu >= ~0.9 ya da aynı dayanak)
KUME = {
    "ham_petrol": ["USO", "BNO", "USL", "DBO", "UCO", "SCO(ters)", "UGA(benzin, 0.86)"],
    "genis_emtia_enerji_agirlikli": ["DBC", "PDBC", "GSG", "COMT", "BCI(0.74 USO)"],
    "dogalgaz": ["UNG", "UNL", "BOIL", "KOLD(ters)"],
    "enerji_hisse": ["XLE", "ERX", "ERY(ters)", "XOP", "GUSH", "DRIP(ters)", "OIH(0.86 XLE)"],
    "tarim": ["DBA", "CORN", "WEAT", "SOYB", "CANE(şeker, ayrık)"],
}
# PTP / K-1 durumu. 'PTP' = midas_kosullari.md §5.4'te adı geçen (USCF, ProShares Trust II);
# 'K1_muhtemel' = ihraççı yapısı ortaklık (K-1), Midas'ta PTP ibaresi bu çalışmada doğrulanmadı;
# '40act' = 1940 Kanunu fonu / K-1'siz (stopaj riski yok).
PTP = {s: "PTP" for s in ["USO", "BNO", "USL", "UNG", "UNL", "UGA", "UCO", "SCO", "BOIL", "KOLD"]}
PTP.update({s: "K1_muhtemel" for s in ["DBO", "DBC", "DBA", "GSG", "CORN", "WEAT", "SOYB", "CANE"]})
PTP.update({s: "40act" for s in ["PDBC", "BCI", "COMT", "XLE", "XOP", "OIH", "GUSH", "DRIP", "ERX", "ERY"]})

POS_LEVELS = (1000.0, 2500.0, 10000.0)

_tar = None
def tarama():
    global _tar
    if _tar is None:
        _tar = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym")
    return _tar

def spread_bp(sym):
    return float(tarama().loc[sym, "spread_bp"])

def cost_at(sym, pos):
    return 2 * lib.COMM_USD / pos * 1e4 + spread_bp(sym)

def cost(sym):
    return cost_at(sym, 2500.0)

# ---------------- olaylar ----------------
def events(fname, event=None):
    d = pd.read_csv(os.path.join(EV, fname + ".csv"), parse_dates=["date"])
    if event is not None:
        d = d[d["event"] == event]
    return d

def day_before(idx, dates):
    """t: bir sonraki işlem günü 'dates' içinde olan günler (olay takvimi önceden bilinir)."""
    dates = pd.DatetimeIndex(pd.to_datetime(dates)).normalize()
    nxt = pd.Series(list(idx[1:]) + [pd.NaT], index=idx)
    return pd.Series(nxt.isin(dates).values, index=idx)

def on_dates(idx, dates):
    dates = pd.DatetimeIndex(pd.to_datetime(dates)).normalize()
    return pd.Series(idx.isin(dates), index=idx)

# ---------------- test kaydı ----------------
REG = []

def p_one(t, n, sign=+1):
    if not np.isfinite(t) or n < 3: return np.nan
    return float(st.t.sf(sign * t, n - 1))

def register(hyp, sym, desc, mode, h, s, sign=+1, kind="strateji"):
    rec = {"hyp": hyp, "sym": sym, "desc": desc, "mode": mode, "h": h, "kind": kind, "sign": sign,
           "n": s.get("n", 0), "gross_bp": s.get("mean_gross_bp", np.nan), "net_bp": s.get("mean_net_bp", np.nan),
           "t": s.get("t", np.nan), "is_net_bp": s.get("is_net_bp", np.nan), "oos_net_bp": s.get("oos_net_bp", np.nan),
           "is_t": s.get("is_t", np.nan), "oos_t": s.get("oos_t", np.nan), "years_pos": s.get("years_pos_frac", np.nan),
           "win": s.get("win", np.nan), "pf": s.get("pf", np.nan), "maxdd": s.get("maxdd", np.nan),
           "worst_bp": s.get("worst_bp", np.nan), "edge_bp": s.get("edge_bp", np.nan), "cost_bp": s.get("cost_bp", np.nan)}
    # 'kaçın' (sign=-1) testlerinde maliyet işareti yanıltmasın diye brüt t kullanılır
    if sign == -1 and np.isfinite(s.get("t_gross", np.nan)):
        rec["t"] = s["t_gross"]
    rec["p1"] = p_one(rec["t"], rec["n"], sign)
    REG.append(rec)
    return rec

def save_registry(name):
    df = pd.DataFrame(REG)
    df.to_csv(os.path.join(OUT, f"testler_{name}.csv"), index=False)
    return df

def full(trade_sym, sig, h, mode="C0", exit_sig=None, df=None):
    """Bir sinyalin tam istatistiği (2.500 $ maliyeti) + maliyet duyarlılığı."""
    if df is None: df = lib.load(trade_sym)
    c = cost(trade_sym)
    sig = sig.reindex(df.index).fillna(False).astype(bool)
    s, tr = lib.evaluate(df, sig, h, mode, c, exit_sig=exit_sig)
    if len(tr):
        g = tr["gross"].values
        s["t_gross"] = float(g.mean() / (g.std(ddof=1) / math.sqrt(len(g)))) if len(g) > 2 and g.std(ddof=1) > 0 else np.nan
        for pos in POS_LEVELS:
            s[f"net_bp_{int(pos)}"] = float(g.mean() * 1e4 - cost_at(trade_sym, pos))
    return s, tr

def grid(hyp, trade_sym, sig, desc, hs=(1, 2, 3), modes=("C0", "O1", "C1"), sign=+1, exit_sig=None, df=None, reg=True):
    """Modlar x ufuklar; hepsi kaydedilir (test sayısı)."""
    rows = []
    for mode in modes:
        for h in hs:
            s, tr = full(trade_sym, sig, h, mode, exit_sig, df)
            if reg: register(hyp, trade_sym, desc, mode, h, s, sign)
            r = {"hyp": hyp, "sym": trade_sym, "desc": desc, "mode": mode, "h": h}
            r.update({k: v for k, v in s.items() if k not in ("label",)})
            rows.append(r)
    return pd.DataFrame(rows)

def fmt(df, cols=None):
    cols = cols or ["sym", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "win", "pf", "is_net_bp", "is_t",
                    "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp", "edge_bp"]
    cols = [c for c in cols if c in df.columns]
    return df[cols].round(3).to_string(index=False)

def nw_t(y, x, lags):
    n, k = x.shape
    xtx = np.linalg.inv(x.T @ x); b = xtx @ x.T @ y; e = y - x @ b
    u = x * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

def fwd(r, h):
    """r(t+1)+...+r(t+h) (log getiri)."""
    return r[::-1].rolling(h).sum()[::-1].shift(-1)

def logret(sym):
    return np.log(lib.load(sym)["c"]).diff()

def ttest_diff(a, b):
    a = pd.Series(a).dropna(); b = pd.Series(b).dropna()
    t, p = st.ttest_ind(a, b, equal_var=False)
    return float(t), float(p)
