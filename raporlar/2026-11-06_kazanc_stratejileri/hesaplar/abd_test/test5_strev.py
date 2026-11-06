"""TEST 5: Kisa vade reversal faktoru (French ST_Rev aylik ve gunluk) - 2010 sonrasi davranis.
Net getiri icin VARSAYIM: her bacakta aylik tek-yon devir ~%90 (aylik formasyon) -> aylik maliyet = 2 bacak * 0.9 * 2 (al+sat) * c.
Gunluk-rebalance edilen gunluk ST_Rev icin devir cok daha yuksek; net hesaplanmadi (uygulanamaz).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from ortak import french_monthly, french_daily, md_table, fmt_pct, OUT, stats

ff, _ = french_monthly("F-F_Research_Data_Factors.csv"); rf = ff["RF"]
st, _ = french_monthly("F-F_ST_Reversal_Factor.csv"); st = st.iloc[:, 0]
std, _ = french_daily("F-F_ST_Reversal_Factor_daily.csv"); std = std.iloc[:, 0]
umd, _ = french_monthly("F-F_Momentum_Factor.csv"); umd = umd.iloc[:, 0]

PER = [("1927-2026", "1927-01-01", "2026-12-31"), ("1963-1989", "1963-01-01", "1989-12-31"), ("1990-2009", "1990-01-01", "2009-12-31"),
       ("2010-2026", "2010-01-01", "2026-12-31"), ("2020-2026", "2020-01-01", "2026-12-31")]
rows = []
for lab, a, b in PER:
    x = st.loc[a:b]; xd = std.loc[a:b]
    row = dict(Donem=lab, Ay=len(x), Ort_ay=x.mean(), Yillik=12 * x.mean(), t=x.mean() / x.std() * np.sqrt(len(x)),
               Sharpe=x.mean() / x.std() * np.sqrt(12), Pozitif_yil=((1 + x).groupby(x.index.year).prod() > 1).mean(),
               Gunluk_STR_yillik=252 * xd.mean() if len(xd) else np.nan,
               Gunluk_Sharpe=xd.mean() / xd.std() * np.sqrt(252) if len(xd) else np.nan)
    for c in (0.0005, 0.001, 0.002):
        row[f"Net_yillik_c{int(c * 1e4)}bp"] = 12 * (x.mean() - 2 * 0.9 * 2 * c)
    rows.append(row)
T = pd.DataFrame(rows)
o = T.copy()
for c in ["Ort_ay", "Yillik", "Gunluk_STR_yillik", "Pozitif_yil"] + [c for c in o.columns if c.startswith("Net")]:
    o[c] = o[c].map(fmt_pct)
for c in ["t", "Sharpe", "Gunluk_Sharpe"]:
    o[c] = o[c].map(lambda v: f"{v:.2f}")
md = ["\n#### French ST_Rev (onceki ay kaybedenler - kazananlar, VW 2x3), brut; net = VARSAYIMSAL maliyet\n", md_table(o, pct_cols=(), num_cols=())]
# yillik getiriler 2010+
yr = (1 + st.loc["2010":]).groupby(st.loc["2010":].index.year).prod() - 1
yu = (1 + umd.loc["2010":]).groupby(umd.loc["2010":].index.year).prod() - 1
Y = pd.DataFrame({"Yil": yr.index, "ST_Rev": yr.map(fmt_pct).values, "UMD": yu.reindex(yr.index).map(fmt_pct).values})
md += ["\n#### 2010+ takvim yili getirileri (2026 = Ocak-Eylul)\n", md_table(Y, pct_cols=())]
open(os.path.join(OUT, "t5_tablolar.md"), "w").write("\n".join(md))
print("\n".join(md))
