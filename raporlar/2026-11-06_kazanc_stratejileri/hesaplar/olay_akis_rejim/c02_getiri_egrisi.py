"""TCMB gosterge nitelikli DIBS degerlerinden (kirli fiyat) 2 yillik sabit vadeli bilesik getiri serisi.
Her tahvil/gun: nakit akislari (kupon tarihleri = vade - k*182 gun, kupon = '.ORAN' donemlik %, anapara 100) ile
P_kirli = sum CF/(1+r)^(gun/365) cozulur (r = yillik bilesik). 2Y = kalan vadesi 2 yili kesen iki tahvil arasinda dogrusal
interpolasyon (yalniz bir taraf varsa |tau-2|<=0.6 ise en yakin). Kalan vade <0.5 yil kullanilmaz. Cikti: tcmb/y2.parquet"""
import os, glob, numpy as np, pandas as pd
from scipy.optimize import brentq
import ortak as O
T = O.MY + "/tcmb"; RAW = O.MY + "/tcmb_raw"
sel = pd.read_csv(RAW + "/bond_sel.csv", parse_dates=["iss", "mat"]).set_index("code")
TK = O.islem_gunleri(); TK = TK[TK >= "2010-01-01"]
rows = []
for f in glob.glob(T + "/TP.TR*.parquet"):
    code = os.path.basename(f)[:-8]; info = sel.loc[code]; d = pd.read_parquet(f)
    c = code.replace(".", "_"); px = d[c].dropna(); cp = d[c + "_ORAN"].ffill() if (c + "_ORAN") in d else None
    M = info.mat; cds = []
    k = 0
    while True:
        x = M - pd.Timedelta(days=182 * k)
        if x < info.iss - pd.Timedelta(days=5): break
        cds.append(x); k += 1
    cds = np.array(sorted(cds), dtype="datetime64[ns]")
    px = px[px.index.isin(TK)]
    for t, p in px.items():
        tau = (M - t).days / 365.0
        if tau < 0.5 or tau > 3.2 or not (20 < p < 200): continue
        cf_t = []; cf = []
        if info.fix and cp is not None:
            cpn = cp.get(t, np.nan)
            if not np.isfinite(cpn): continue
            fut = cds[cds > np.datetime64(t)]
            for x in fut: cf_t.append((pd.Timestamp(x) - t).days / 365.0); cf.append(cpn)
            cf[-1] += 100.0 if len(cf) and abs((pd.Timestamp(fut[-1]) - M).days) < 3 else 0.0
            if not len(cf) or abs((pd.Timestamp(fut[-1]) - M).days) >= 3: cf_t.append(tau); cf.append(100.0)
        else:
            cf_t, cf = [tau], [100.0]
        cf_t = np.array(cf_t); cf = np.array(cf)
        try: r = brentq(lambda y: (cf / (1 + y) ** cf_t).sum() - p, -0.5, 10.0)
        except Exception: continue
        rows.append((t, code, tau, r, bool(info.fix)))
Y = pd.DataFrame(rows, columns=["t", "code", "tau", "y", "fix"])
Y = Y.drop_duplicates(["t", "tau", "y"])
Y.to_parquet(T + "/tahvil_getiri.parquet")
out = {}
for t, g in Y.groupby("t"):
    lo = g[g.tau <= 2].sort_values("tau").tail(1); hi = g[g.tau > 2].sort_values("tau").head(1)
    if len(lo) and len(hi) and (hi.tau.iloc[0] - lo.tau.iloc[0]) < 2.0:
        w = (2 - lo.tau.iloc[0]) / (hi.tau.iloc[0] - lo.tau.iloc[0]); out[t] = (1 - w) * lo.y.iloc[0] + w * hi.y.iloc[0]
    else:
        g2 = g.assign(dd=(g.tau - 2).abs()).sort_values("dd")
        if len(g2) and g2.dd.iloc[0] <= 0.6: out[t] = g2.y.iloc[0]
y2 = pd.Series(out).sort_index() * 100
y2.name = "y2"; y2.to_frame().to_parquet(T + "/y2.parquet")
print(len(Y), "gozlem;", len(y2), "gun", y2.index[0].date(), y2.index[-1].date())
print(y2.resample("QE").last().round(2).to_string())
dy = y2.diff(); print("buyuk gunluk degisim (>300bp):"); print(dy[dy.abs() > 3].round(2).to_string())
