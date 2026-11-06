"""5) Swing ufku: haftalik kontrol, gunluk veri, 1 gun gecikmeli icra (French 49 sektor gunluk VW).
Giris: hafta sonu kapanisinda sektor RS'i (sektor/piyasa) yeni N-haftalik zirvede (N=26/52) [+opsiyonel: mutlak 26h getiri>0].
Cikis: (a) RS trailing X% (hafta sonu kontrol), (b) mutlak fiyat trailing X% (gunluk kapanis kontrol), (c) sure H hafta.
Icra: sinyal gununu izleyen gunun kapanisi. Maliyet tek yon 0.10% (stres 0.25%).
"""
import os, itertools
import numpy as np
import pandas as pd
from ff_load import load_daily49, load_ff_daily
from dalga_tanim import OUT

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)

d = load_daily49()["vw"] / 100
ff = load_ff_daily() / 100
d = d.loc["1928":]
ff = ff.loc[d.index]
rm = ff["Mkt-RF"] + ff["RF"]
rf = ff["RF"]
LP = np.log1p(d.fillna(0)).cumsum().values  # log fiyat
LM = np.log1p(rm).cumsum().values
LRF = np.log1p(rf).cumsum().values
LX = LP - LM[:, None]  # log RS
valid = d.notna().values
dates = d.index
wk = pd.Series(np.arange(len(dates)), index=dates).groupby(dates.to_period("W-FRI")).last().values  # hafta sonu indeksleri
cols = d.columns


def run(N=52, exit_kind="rstrail", X=0.10, H=13, absf=False, c=0.001):
    trades = []
    for j, ind in enumerate(cols):
        inpos = False
        for wi in range(N + 1, len(wk) - 1):
            t = wk[wi]
            if not valid[t, j]:
                continue
            if not inpos:
                past = LX[wk[wi - N:wi], j]
                if not valid[wk[wi - N], j]:
                    continue
                if LX[t, j] > past.max():
                    if absf and LP[t, j] - LP[wk[wi - 26], j] <= 0:
                        continue
                    e = t + 1  # ertesi gun kapanisi
                    if e >= len(dates):
                        break
                    inpos, ewi = True, wi
                    xpk = LX[e, j]
                    ppk = LP[e, j]
                    continue
            else:
                ex_t = None
                if exit_kind == "rstrail":
                    xpk = max(xpk, LX[t, j])
                    if LX[t, j] <= xpk + np.log(1 - X):
                        ex_t = t + 1
                elif exit_kind == "pxtrail":
                    # gunluk kontrol: onceki hafta sonundan bu hafta sonuna
                    t0 = wk[wi - 1] + 1
                    for s in range(t0, t + 1):
                        ppk = max(ppk, LP[s, j])
                        if LP[s, j] <= ppk + np.log(1 - X):
                            ex_t = s + 1
                            break
                elif exit_kind == "time":
                    if wi - ewi >= H:
                        ex_t = t + 1
                if ex_t is not None or wi == len(wk) - 2:
                    ex_t = min(ex_t if ex_t is not None else t, len(dates) - 1)
                    trades.append((ind, dates[e], dates[ex_t], ex_t - e,
                                   LP[ex_t, j] - LP[e, j], LX[ex_t, j] - LX[e, j], LRF[ex_t] - LRF[e]))
                    inpos = False
    tr = pd.DataFrame(trades, columns=["ind", "entry", "exit", "days", "labs", "lrel", "lrf"])
    tr["abs_net"] = np.expm1(tr.labs + 2 * np.log(1 - c))
    tr["rel_net"] = np.expm1(tr.lrel + 2 * np.log(1 - c))
    tr["exc_net"] = np.expm1(tr.labs - tr.lrf + 2 * np.log(1 - c))
    return tr


def port(tr, c=0.001):
    """EW acik pozisyon portfoyu (gunluk), bos gunler T-bill."""
    T = len(dates)
    s = np.zeros(T); n = np.zeros(T)
    dr = d.fillna(0).values
    for _, r in tr.iterrows():
        j = cols.get_loc(r.ind)
        a = dates.get_loc(r.entry); b = dates.get_loc(r.exit)
        seg = dr[a + 1:b + 1, j].copy()
        if len(seg) == 0:
            continue
        seg[0] = (1 + seg[0]) * (1 - c) - 1
        seg[-1] = (1 + seg[-1]) * (1 - c) - 1
        s[a + 1:b + 1] += seg
        n[a + 1:b + 1] += 1
    p = np.where(n > 0, s / np.maximum(n, 1), rf.values)
    return pd.Series(p, index=dates), pd.Series(n, index=dates)


def pstats(p, start):
    x = p.loc[start:]
    w = (1 + x).cumprod()
    yrs = len(x) / 252
    ex = x - rf.loc[x.index]
    return dict(cagr=w.iloc[-1] ** (1 / yrs) - 1, sharpe=ex.mean() / ex.std() * np.sqrt(252), maxdd=(w / w.cummax() - 1).min())


if __name__ == "__main__":
    rows = []
    store = {}
    grid = []
    for N in (26, 52):
        for absf in (False, True):
            for ek, X, H in [("rstrail", 0.06, 0), ("rstrail", 0.10, 0), ("rstrail", 0.15, 0),
                             ("pxtrail", 0.08, 0), ("pxtrail", 0.12, 0), ("pxtrail", 0.20, 0),
                             ("time", 0, 4), ("time", 0, 8), ("time", 0, 13), ("time", 0, 26)]:
                grid.append((N, absf, ek, X, H))
    mk = pd.Series(rm.values, index=dates)
    for N, absf, ek, X, H in grid:
        tr = run(N=N, exit_kind=ek, X=X, H=H, absf=absf)
        p, n = port(tr)
        name = f"N{N}_{ek}{int(X*100) if X else H}_{'abs' if absf else 'none'}"
        store[name] = tr
        tr["per"] = pd.cut(tr.entry.dt.year, [1900, 1999, 2014, 2030], labels=["1928-99", "2000-14", "2015-26"])
        row = dict(rule=name, ntr=len(tr), tr_yr=len(tr) / ((dates[-1] - dates[0]).days / 365.25), hold_d=tr.days.median(),
                   win_abs=(tr.abs_net > 0).mean(), win_rel=(tr.rel_net > 0).mean(), avg_rel=tr.rel_net.mean(),
                   med_rel=tr.rel_net.median(), avg_abs=tr.abs_net.mean(), avg_open=n.loc["1931":].mean())
        for per, g in tr.groupby("per", observed=True):
            row[f"rel_{per}"] = g.rel_net.mean()
            row[f"win_{per}"] = (g.rel_net > 0).mean()
        for st in ("1931", "2000", "2015"):
            ps = pstats(p, st)
            row[f"cagr{st[2:]}"] = ps["cagr"]; row[f"sh{st[2:]}"] = ps["sharpe"]; row[f"dd{st[2:]}"] = ps["maxdd"]
        rows.append(row)
        print(name, "done", flush=True)
    res = pd.DataFrame(rows)
    res.to_pickle(os.path.join(OUT, "swing_grid.pkl"))
    pd.to_pickle(store, os.path.join(OUT, "swing_trades.pkl"))
    for st in ("1931", "2000", "2015"):
        print("Piyasa", st, pstats(mk, st))
    print(res.round(3).to_string())
    print("\nGrid medyanlari:")
    print(res.drop(columns="rule").median().round(3).to_string())
