"""TEST 2: Sentetik 1x/2x/3x gunluk yeniden dengelenen kaldiracli endeks + trend filtresi (200-DMA, 10-ay SMA).

Dayanaklar
  MKT : Ken French CRSP deger-agirlikli tum piyasa (Mkt-RF + RF), GUNLUK, TEMETTU DAHIL, 1926-07-01..2026-09-30.
        (S&P 500'un vekili; korelasyon ~0.99, S&P 500 degil.)
  NDX : FRED NASDAQ100 FIYAT endeksi 1986-01-02..2026-11-05 + yaklasik temettu 0.7%/yil (sabit, gunluk 0.007/252).
Risksiz: French gunluk RF (1-ay T-bill) ; 2026-09-30 sonrasi FRED DTB3/252.
LETF gunluk getiri = L*r - (L-1)*(rf + spread/252) - ER/252 ; -%99.9 ile tabanlanir.
Sinyal: t kapanisinda dayanak > MA ise t+1(+lag) gunu pozisyon; disarida T-bill. Gecis basina maliyet c.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from ortak import french_daily, fred, stats, md_table, fmt_pct, OUT

# ------------------------------------------------------------------ veri
ff, _ = french_daily("F-F_Research_Data_Factors_daily.csv")
mkt_r = ff["Mkt-RF"] + ff["RF"]
rf_ff = ff["RF"]
dtb3 = fred("DTB3").dropna() / 100 / 252

ndx_p = fred("NASDAQ100").dropna()
ndx_r = ndx_p.pct_change().dropna() + 0.007 / 252

def rf_for(idx):
    rf = rf_ff.reindex(idx)
    fill = dtb3.reindex(idx, method="ffill")
    return rf.fillna(fill).fillna(0)

UNDER = {
    "MKT": (mkt_r, (1 + mkt_r).cumprod()),   # TR endeksi sinyal icin (fiyat endeksi yok; not edildi)
    "NDX": (ndx_r, ndx_p.reindex(ndx_r.index)),
}

ER = {1: 0.0010, 2: 0.0090, 3: 0.0090}


def letf(r, rf, L, spread):
    out = L * r - (L - 1) * (rf + spread / 252) - ER[L] / 252
    return out.clip(lower=-0.999)


def ma_signal(price, n, band=0.0):
    ma = price.rolling(n).mean()
    if band == 0:
        s = (price > ma).astype(float)
        s[ma.isna()] = np.nan
        return s
    s = pd.Series(np.nan, index=price.index)
    state = np.nan
    p, m = price.values, ma.values
    out = np.empty(len(p)); out[:] = np.nan
    for i in range(len(p)):
        if np.isnan(m[i]):
            continue
        if np.isnan(state):
            state = 1.0 if p[i] > m[i] else 0.0
        elif state == 1.0 and p[i] < m[i] * (1 - band):
            state = 0.0
        elif state == 0.0 and p[i] > m[i] * (1 + band):
            state = 1.0
        out[i] = state
    return pd.Series(out, index=price.index)


def sma10m_signal(price):
    me = price.groupby([price.index.year, price.index.month]).tail(1)
    sig_me = (me > me.rolling(10).mean()).astype(float)
    sig_me[me.rolling(10).mean().isna()] = np.nan
    return sig_me.reindex(price.index).ffill()   # ay sonu kapanisinda karar, ay boyunca sabit


def run(r, rf, sig, L, spread, lag=0, cost=0.0):
    """sig: t kapanisindaki karar. Pozisyon t+1+lag gunu uygulanir."""
    pos = sig.shift(1 + lag)
    lr = letf(r, rf, L, spread)
    ret = pos * lr + (1 - pos) * rf
    sw = pos.diff().abs().fillna(0)
    ret = ret - sw * cost
    ret = ret[pos.notna()]
    return ret, sw[pos.notna()]


PERIODS_MKT = [("1926-2026 (tam)", "1926-07-01", "2026-12-31"), ("1950-2026", "1950-01-01", "2026-12-31"),
               ("1986-2026", "1986-01-01", "2026-12-31"),
               ("2010-2026", "2010-01-01", "2026-12-31"), ("2020-2026", "2020-01-01", "2026-12-31")]
PERIODS_NDX = [("1986-2026 (tam)", "1986-01-01", "2026-12-31"),
               ("2010-2026", "2010-01-01", "2026-12-31"), ("2020-2026", "2020-01-01", "2026-12-31")]
CRISES = [("1929-32", "1929-09-01", "1932-07-31"), ("1987 Ekim", "1987-08-01", "1987-12-31"),
          ("2000-02", "2000-01-01", "2002-12-31"), ("2008 (07/10-09/03)", "2007-10-01", "2009-03-31"),
          ("2020 Covid (Sub-Nis)", "2020-02-01", "2020-04-30"), ("2022", "2022-01-01", "2022-12-31")]

res_md = []
summary_rows = []
grid_rows = []
crisis_rows = []

for uname, (r_all, px_all) in UNDER.items():
    r_all = r_all.dropna()
    rf = rf_for(r_all.index)
    px = px_all.reindex(r_all.index)
    sigs = {"BH": pd.Series(1.0, index=r_all.index), "200DMA": ma_signal(px, 200), "10aySMA": sma10m_signal(px)}
    # baslangici esitle: tum stratejiler 200 gunluk MA hazir olduktan sonra baslar
    start = sigs["200DMA"].first_valid_index()
    start = max(start, sigs["10aySMA"].first_valid_index())
    periods = PERIODS_MKT if uname == "MKT" else PERIODS_NDX
    for L in (1, 2, 3):
        for sname, sig in sigs.items():
            sig = sig.loc[start:]
            for spread in (0.005, 0.01):
                for lag in (0, 1):
                    for cost in (0.0, 0.001):
                        if sname == "BH" and (lag or cost):
                            continue
                        ret, sw = run(r_all.loc[start:], rf.loc[start:], sig, L, spread, lag, cost)
                        for plab, a, b in periods:
                            rr = ret.loc[a:b]
                            if len(rr) < 200:
                                continue
                            st = stats(rr, rf.loc[a:b], ppy=252)
                            nsw = sw.loc[a:b].sum() / (len(rr) / 252)
                            summary_rows.append(dict(Dayanak=uname, L=L, Strateji=sname, Spread=spread, Lag=lag,
                                                     Maliyet=cost, Donem=plab, Gecis_yil=nsw, **st))
                        if spread == 0.01 and lag == 0 and cost == 0.0:
                            for clab, a, b in CRISES:
                                rr = ret.loc[a:b]
                                if len(rr) < 20:
                                    continue
                                nav = (1 + rr).cumprod()
                                crisis_rows.append(dict(Dayanak=uname, L=L, Strateji=sname, Kriz=clab,
                                                        Getiri=nav.iloc[-1] - 1, IcMaxDD=(nav / nav.cummax() - 1).min()))
    # ---------------- robustluk izgarasi: MA uzunlugu x bant x lag x maliyet (spread 1%)
    for L in (1, 2, 3):
        for n, band, lag, cost in itertools.product((100, 150, 200, 250), (0.0, 0.01, 0.02), (0, 1), (0.0, 0.001, 0.0025)):
            sig = ma_signal(px, n, band).loc[start:]
            ret, sw = run(r_all.loc[start:], rf.loc[start:], sig, L, 0.01, lag, cost)
            for plab, a, b in periods:
                rr = ret.loc[a:b]
                if len(rr) < 200:
                    continue
                st = stats(rr, rf.loc[a:b], ppy=252)
                grid_rows.append(dict(Dayanak=uname, L=L, n=n, bant=band, lag=lag, maliyet=cost, Donem=plab,
                                      Gecis_yil=sw.loc[a:b].sum() / (len(rr) / 252), **st))

S = pd.DataFrame(summary_rows)
G = pd.DataFrame(grid_rows)
C = pd.DataFrame(crisis_rows)
S.to_csv(os.path.join(OUT, "t2_ozet.csv"), index=False)
G.to_csv(os.path.join(OUT, "t2_izgara.csv"), index=False)
C.to_csv(os.path.join(OUT, "t2_kriz.csv"), index=False)

# ---------------- markdown ciktilari
md = []
cols = ["Donem", "L", "Strateji", "CAGR", "Vol", "Sharpe", "MaxDD", "EnKotuYil", "EnKotuYilT", "ExcessCAGR", "Gecis_yil"]
for u in ("MKT", "NDX"):
    md.append(f"\n#### {u}: ana sonuclar (spread T-bill+1.0%, ER 0.9%, sinyal t kapanis -> t+1, gecis maliyeti 10 bp)\n")
    sub = S[(S.Dayanak == u) & (S.Spread == 0.01) & (S.Lag == 0) & (((S.Strateji == "BH") & (S.Maliyet == 0)) | ((S.Strateji != "BH") & (S.Maliyet == 0.001)))]
    sub = sub[cols].copy(); sub["Gecis_yil"] = sub["Gecis_yil"].map(lambda x: f"{x:.1f}")
    md.append(md_table(sub))
    md.append(f"\n#### {u}: 1 gun ek gecikme (lag=1) + 10 bp, spread 1.0%\n")
    sub = S[(S.Dayanak == u) & (S.Spread == 0.01) & (S.Lag == 1) & (S.Maliyet == 0.001)][cols].copy()
    sub["Gecis_yil"] = sub["Gecis_yil"].map(lambda x: f"{x:.1f}")
    md.append(md_table(sub))
    md.append(f"\n#### {u}: spread hassasiyeti (CAGR; lag0, 10bp)\n")
    sub = S[(S.Dayanak == u) & (S.Lag == 0) & (((S.Strateji == "BH") & (S.Maliyet == 0)) | ((S.Strateji != "BH") & (S.Maliyet == 0.001)))]
    pv = sub.pivot_table(index=["Donem", "L", "Strateji"], columns="Spread", values="CAGR").reset_index()
    pv.columns = [str(c) if not isinstance(c, float) else f"CAGR spread {c:.1%}" for c in pv.columns]
    for c in pv.columns[3:]:
        pv[c] = pv[c].map(fmt_pct)
    md.append(md_table(pv, pct_cols=()))
    md.append(f"\n#### {u}: robustluk izgarasi (n in 100/150/200/250, bant 0/1/2%, lag 0/1, maliyet 0/10/25bp = 72 kombinasyon): MEDYAN ve [min,max]\n")
    g = G[G.Dayanak == u]
    agg = g.groupby(["Donem", "L"]).agg(CAGR_med=("CAGR", "median"), CAGR_min=("CAGR", "min"), CAGR_max=("CAGR", "max"),
                                         Sharpe_med=("Sharpe", "median"), MaxDD_med=("MaxDD", "median"),
                                         MaxDD_worst=("MaxDD", "min"), Gecis_med=("Gecis_yil", "median")).reset_index()
    for c in ["CAGR_med", "CAGR_min", "CAGR_max", "MaxDD_med", "MaxDD_worst"]:
        agg[c] = agg[c].map(fmt_pct)
    agg["Sharpe_med"] = agg["Sharpe_med"].map(lambda x: f"{x:.2f}")
    agg["Gecis_med"] = agg["Gecis_med"].map(lambda x: f"{x:.1f}")
    md.append(md_table(agg, pct_cols=()))
    md.append(f"\n#### {u}: kriz pencereleri (spread 1%, lag0, maliyetsiz): pencere getirisi / pencere ici MaxDD\n")
    c = C[C.Dayanak == u].copy()
    c["Deger"] = c.apply(lambda x: f"{100*x.Getiri:.0f}% / {100*x.IcMaxDD:.0f}%", axis=1)
    pv = c.pivot_table(index=["L", "Strateji"], columns="Kriz", values="Deger", aggfunc="first").reset_index()
    order = [k for k, _, _ in CRISES if k in pv.columns]
    md.append(md_table(pv[["L", "Strateji"] + order], pct_cols=()))

open(os.path.join(OUT, "t2_tablolar.md"), "w").write("\n".join(md))
print("\n".join(md))
