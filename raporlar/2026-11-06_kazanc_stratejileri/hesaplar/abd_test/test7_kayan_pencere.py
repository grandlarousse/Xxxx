"""TEST 7 (ek): Baslangic tarihi duyarliligi. Kayan 3 ve 5 yillik CAGR dagilimi; engel oranlarini (USD %10 / %15 / %20) gecme olasiligi.
Seriler test2 ile ayni varsayimlar: spread T-bill+1%, ER 0.9%, sinyal t kapanisi -> t+2 (1 gun ek gecikme), 10 bp/gecis.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from ortak import french_daily, french_monthly, fred, md_table, fmt_pct, OUT

ff, _ = french_daily("F-F_Research_Data_Factors_daily.csv")
mkt = ff["Mkt-RF"] + ff["RF"]; rf_ff = ff["RF"]
dtb3 = fred("DTB3").dropna() / 100 / 252
ndx_p = fred("NASDAQ100").dropna(); ndx = ndx_p.pct_change().dropna() + 0.007 / 252


def rf_for(idx):
    return rf_ff.reindex(idx).fillna(dtb3.reindex(idx, method="ffill")).fillna(0)


def strat(r, px, L, filt, lag=1, cost=0.001, spread=0.01, er=0.009):
    rf = rf_for(r.index)
    lr = (L * r - (L - 1) * (rf + spread / 252) - (er if L > 1 else 0.001) / 252).clip(lower=-0.999)
    if not filt:
        return lr.iloc[200:]
    ma = px.rolling(200).mean()
    sig = (px > ma).astype(float); sig[ma.isna()] = np.nan
    pos = sig.shift(1 + lag)
    out = pos * lr + (1 - pos) * rf - pos.diff().abs().fillna(0) * cost
    return out[pos.notna()]


S = {}
mpx = (1 + mkt).cumprod()
for L in (1, 2, 3):
    S[f"MKT {L}x BH"] = strat(mkt, mpx, L, False)
    S[f"MKT {L}x 200DMA"] = strat(mkt, mpx, L, True)
    S[f"NDX {L}x BH"] = strat(ndx, ndx_p.reindex(ndx.index), L, False)
    S[f"NDX {L}x 200DMA"] = strat(ndx, ndx_p.reindex(ndx.index), L, True)

rows = []
for nm, r in S.items():
    m = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
    nav = (1 + m).cumprod()
    for yrs in (3, 5):
        n = 12 * yrs
        roll = (nav / nav.shift(n)) ** (1 / yrs) - 1
        for lab, a in [("1950+ baslangic", 1950), ("1990+ baslangic", 1990)]:
            x = roll[[i[0] >= a + yrs for i in roll.index]].dropna()
            if len(x) < 24:
                continue
            rows.append(dict(Strateji=nm, Pencere=f"{yrs}y", Ornek=lab, N=len(x), Medyan=x.median(), P10=x.quantile(0.1),
                             P90=x.quantile(0.9), Negatif=(x < 0).mean(), Gt10=(x > 0.10).mean(), Gt15=(x > 0.15).mean(),
                             Gt20=(x > 0.20).mean()))
T = pd.DataFrame(rows)
T = T[~((T.Strateji.str.startswith("NDX")) & (T.Ornek == "1950+ baslangic"))]
for c in ["Medyan", "P10", "P90", "Negatif", "Gt10", "Gt15", "Gt20"]:
    T[c] = T[c].map(fmt_pct)
T = T.rename(columns={"Gt10": ">%10", "Gt15": ">%15", "Gt20": ">%20", "Negatif": "<0"})
md = ["\n#### Kayan pencere CAGR dagilimi (aylik adim; pencere bitis yili >= baslangic+pencere). MKT verisi 2026-09, NDX 2026-10'a kadar\n",
      md_table(T.drop(columns=["N"]), pct_cols=())]
open(os.path.join(OUT, "t7_tablolar.md"), "w").write("\n".join(md))
print("\n".join(md))
