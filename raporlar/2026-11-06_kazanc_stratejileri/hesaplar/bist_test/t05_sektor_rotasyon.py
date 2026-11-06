"""TEST 5 (+6): BIST sektor endeksleri arasinda momentum rotasyonu. Ay sonu sinyal, ertesi gun kapanis islem, 1 ay tut.
Lookback {1,3,6,12} ay, en iyi {2,3} sektor, EW. Maliyet 25 bp gidis-donus (sepet ile spot uygulamasi), stres 50 bp.
Varyant: rejim filtresi (XU100 > SMA200 sinyal gununde, degilse nakit rf). Kiyas: EW tum sektorler, XU100, TL rf.
Placebo: ayni sayida/ayni yenileme oranli rastgele sektor secimi (500)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
from motor import *
SEK = "XBANK XSGRT XFINK XGMYO XHOLD XELKT XILTM XULAS XTCRT XTRZM XSPOR XGIDA XKMYA XMANA XMESY XKAGT XTAST XTEKS XUTEK XMADN XINSA".split()
SET = os.environ.get("SET", "tum")
if SET == "buyuk":   # sig/kucuk sektorler (spor, tekstil, kagit, madencilik, faktoring, turizm) cikarildi -> 15 sektor
    SEK = [c for c in SEK if c not in ("XSPOR", "XTEKS", "XKAGT", "XMADN", "XFINK", "XTRZM")]
SUF = "" if SET == "tum" else "_" + SET
B = base(); cal = B.index
px = pd.DataFrame({c: load_index(c) for c in SEK}).reindex(cal).ffill()
xu = load_index("XU100").reindex(cal).ffill()
sd, ex = exec_dates(rebal_dates("M", cal, "2009-01-01"))
R = period_R(px, ex); n = len(R)
xuR = period_R(xu.to_frame(), ex).iloc[:, 0].values
rfp = compound_between(B.rf_d, ex).iloc[:n].values
tbp = compound_between(B.tb_d, ex).iloc[:n].values
fxp = compound_between(B.fx_r, ex).iloc[:n].values
sd, ex = sd[:n], ex[:n]
regime = (xu > xu.rolling(200).mean()).reindex(sd).values
start = np.flatnonzero(ex >= pd.Timestamp("2010-01-01"))[0]
avail = px.reindex(sd).notna().values & np.r_[[True] * n][:, None]
rows = []; yt = {}; pl_out = {}
def rec(name, r, extra=None):
    r = r[start:]; d = ex[start:]
    for cur in ("TL", "USD"):
        rr = r if cur == "TL" else to_usd(r, fxp[start:]); rf = rfp[start:] if cur == "TL" else tbp[start:]
        st = stats(rr, rf, dates=d); m24 = d >= pd.Timestamp("2024-01-01")
        st24 = stats(rr[m24], rf[m24], dates=d[m24])
        rows.append(dict(strateji=name, para=cur, **st, CAGR_24_26=st24.get("CAGR"), Fazla_24_26=st24.get("Fazla"), **(extra or {})))
        yt[(name, cur)] = yearly(rr, d)
# kiyaslar
ew = np.nanmean(R.values, axis=1); rec("EW tum sektorler (aylik)", ew); rec("XU100 al-tut", xuR); rec("TL rf", rfp)
for L in (1, 3, 6, 12):
    sc = (px.reindex(sd) / px.shift(21 * L).reindex(sd) - 1).values   # ~L ay (21 islem gunu/ay)
    for k in (2, 3):
        sel = select(sc, avail, k=k)
        for cn, cs in (("25bp", 0.00125), ("50bp", 0.0025)):
            r, to = period_engine(sel, R.values, cs, rfp)
            rec(f"MOM{L}ay top{k} {cn}", r, {"turnover_ay": to[start:].mean()})
            if cn == "25bp":
                rr, _ = period_engine(apply_regime(sel, regime), R.values, cs, rfp)
                rec(f"MOM{L}ay top{k} 25bp +rejim(XU100>SMA200)", rr)
                P = placebo(sel, avail, R.values, cs, rfp, n=300, seed=L * 10 + k)
                shp = [sharpe(p[start:], rfp[start:], 12) for p in P]
                s0 = sharpe(r[start:], rfp[start:], 12)
                cg = [(np.prod(1 + p[start:]) ** (12 / len(p[start:])) - 1) for p in P]
                pl_out[f"MOM{L}ay top{k}"] = {"Sharpe": s0, "placebo_medyan_Sharpe": float(np.median(shp)), "placebo_p95_Sharpe": float(np.percentile(shp, 95)),
                                             "yuzdelik": float(np.mean(np.array(shp) < s0)), "placebo_medyan_CAGR": float(np.median(cg))}
df = pd.DataFrame(rows); df.to_csv(f"{OUTD}/t05_ozet{SUF}.csv", index=False)
pd.DataFrame({" ".join(k): v for k, v in yt.items()}).to_csv(f"{OUTD}/t05_yillik{SUF}.csv")
json.dump(pl_out, open(f"{OUTD}/t05_placebo{SUF}.json", "w"), indent=1)
# secim sikligi (MOM12 top3)
sc = (px.reindex(sd) / px.shift(252).reindex(sd) - 1).values; sl = select(sc, avail, k=3)
fq = pd.Series(np.concatenate(sl[start:])).map(dict(enumerate(px.columns))).value_counts() / (n - start)
print("MOM12 top3 secim sikligi:", fq.round(2).to_dict())
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
print(df[["strateji", "para", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "Isabet", "CAGR_24_26", "Fazla_24_26", "turnover_ay"]].round(3).to_string())
grid = df[(df.para == "TL") & df.strateji.str.match(r"MOM\d+ay top\d 25bp$")]
print("IZGARA MEDYANI (TL, 25bp):", grid[["CAGR", "Fazla", "Sharpe", "MaxDD"]].median().round(3).to_dict())
print(json.dumps(pl_out, indent=0))
