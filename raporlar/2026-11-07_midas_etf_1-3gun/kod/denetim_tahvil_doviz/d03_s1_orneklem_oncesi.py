"""DENETİM tahvil_doviz — S1 örneklem ÖNCESİ test (gerçek dış örneklem):
 (1) TLT 2002-08..2016-11 ve TBT 2008-05..2016-11 (Yahoo günlük, temettü/bölünme düzeltmeli kapanış),
     aynı kural: 10Y ihale A-3 kapanış -> A-1 kapanış (C0), A-3 açılış -> A-1 kapanış (OA).
 (2) Hazine getirisinde (FRED DGS10/DGS30) pencere profili 1990-2007 ve 2008-2016 (Lou-Yan-Zhang tipi A-5 -> A).
 (3) TLT Pazartesi etkisi (haftanın günü) örneklemde.
Ham veri: sonuclar/aile_tahvil_doviz/denetim_ham/ (yahoo_TLT.json, yahoo_TBT.json, auc10.json, DGS*.csv).
Çalıştır: python3 -I kod/denetim_tahvil_doviz/d03_s1_orneklem_oncesi.py
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, pandas as pd
import lib
from d01_s1_yeniden import IDX, A10, ROOT, OUT, tstat, cost

HAM = os.path.join(ROOT, "sonuclar", "aile_tahvil_doviz", "denetim_ham")

def yahoo(sym):
    j = json.load(open(os.path.join(HAM, f"yahoo_{sym}.json")))["chart"]["result"][0]
    ts = pd.to_datetime(j["timestamp"], unit="s", utc=True).tz_convert("America/New_York").tz_localize(None).normalize()
    q = j["indicators"]["quote"][0]; ac = j["indicators"]["adjclose"][0]["adjclose"]
    d = pd.DataFrame({"o": q["open"], "c": q["close"], "ac": ac}, index=ts).dropna()
    f = d["ac"] / d["c"]
    d["oa"] = d["o"] * f
    return d[~d.index.duplicated(keep="last")]

J = json.load(open(os.path.join(HAM, "auc10.json")))["data"]
au = pd.DataFrame(J)
au = au[(au.inflation_index_security == "No") & (au.original_security_term == "10-Year") & (au.security_type == "Note")]
AD = pd.DatetimeIndex(sorted(pd.to_datetime(au.auction_date).unique()))
AD = AD[AD != pd.Timestamp("2019-06-21")]   # proje csv'si ile aynı (aynı ayda ikinci kayıt)

def window(d, dates, k1=3, k2=1, mode="C0"):
    idx = d.index; p = idx.searchsorted(dates); p = p[(p - k1 >= 0) & (p < len(idx))]
    p = p[idx[p] == dates[np.isin(dates, idx[p])][:len(p)]] if False else p
    if mode == "C0": r = d["ac"].values[p - k2] / d["ac"].values[p - k1] - 1
    else: r = d["ac"].values[p - k2] / d["oa"].values[p - k1] - 1
    return pd.Series(r, index=idx[p - k1])

res = []
for sym, lo in (("TLT", "2002-08-01"), ("TBT", "2008-05-01")):
    d = yahoo(sym); d = d[d.index < pd.Timestamp("2016-11-07")]
    dates = AD[(AD > pd.Timestamp(lo) + pd.Timedelta(days=10)) & (AD < pd.Timestamp("2016-11-07"))]
    # ihale günü ETF işlem günü mü?
    nt = [x for x in dates if x not in d.index]
    for mode in ("C0", "OA"):
        r = window(d, dates, 3, 1, mode)
        sp = 20.0 if sym == "TBT" else 13.2
        net = r - sp / 1e4
        for per, a, b in (("tümü", lo, "2016-11-07"), ("..2011", lo, "2011-12-31"), ("2012..2016-10", "2012-01-01", "2016-11-07")):
            m = (r.index >= a) & (r.index <= b)
            yrs = net[m].groupby(net[m].index.year).mean()
            res.append((sym, mode, per, int(m.sum()), r[m].mean() * 1e4, tstat(r[m]), net[m].mean() * 1e4, tstat(net[m]), (yrs > 0).mean()))
    # koşulsuz 2 günlük ortalama (aynı dönem)
    u = (d["ac"].shift(-2) / d["ac"] - 1).mean() * 1e4
    print(f"{sym} {d.index.min().date()}..{d.index.max().date()}: koşulsuz 2g ort {u:.1f} bp; ihale günü işlem günü değil: {len(nt)}")
R = pd.DataFrame(res, columns=["sym", "mode", "donem", "n", "brut_bp", "t_brut", "net_bp", "t_net", "yil_pozitif"])
print("\n=== ÖRNEKLEM ÖNCESİ (2002/2008 - 2016-10) — S1 penceresi (TLT long için işaret NEGATİF, TBT için POZİTİF beklenir) ===")
print(R.round(2).to_string(index=False))
R.to_csv(os.path.join(OUT, "d03_orneklem_oncesi_etf.csv"), index=False)
# TBT yıl yıl
d = yahoo("TBT"); d = d[d.index < pd.Timestamp("2016-11-07")]
r = window(d, AD[(AD > "2008-06-01") & (AD < "2016-11-07")], 3, 1, "C0")
print("TBT örneklem öncesi yıl yıl brüt bp:", (r.groupby(r.index.year).mean() * 1e4).round(1).to_dict())
dt = yahoo("TLT"); dt = dt[dt.index < pd.Timestamp("2016-11-07")]
rt = window(dt, AD[(AD > "2002-08-15") & (AD < "2016-11-07")], 3, 1, "C0")
print("TLT örneklem öncesi yıl yıl brüt bp:", (rt.groupby(rt.index.year).mean() * 1e4).round(1).to_dict())

# (2) Hazine getirisi pencere profili
def fred_csv(s):
    x = pd.read_csv(os.path.join(HAM, s + ".csv"), parse_dates=["observation_date"]).set_index("observation_date")[s]
    return pd.to_numeric(x, errors="coerce").dropna()
g10 = fred_csv("DGS10"); g30 = fred_csv("DGS30").reindex(g10.index)
cal = g10.index
prof = []
for per, lo, hi in (("1990-2007", "1990-01-01", "2007-12-31"), ("2008-2016-10", "2008-01-01", "2016-10-31"), ("2016-11-2026", "2016-11-01", "2026-11-06")):
    dd = AD[(AD >= lo) & (AD <= hi)]; p = cal.searchsorted(dd); p = p[(p >= 6) & (p < len(cal) - 3)]
    for k1, k2 in ((5, 0), (5, 1), (3, 0), (3, 1), (3, 2), (2, 1), (1, 0), (0, -2)):
        x = (g10.values[p - k2] - g10.values[p - k1]) * 100
        z = (g30.values[p - k2] - g30.values[p - k1]) * 100
        prof.append((per, f"A-{k1}->A{-k2:+d}", len(p), np.nanmean(x), tstat(x), np.nanmean(z), tstat(z)))
P = pd.DataFrame(prof, columns=["donem", "pencere", "n", "dDGS10_bp", "t10", "dDGS30_bp", "t30"])
print("\n=== Hazine getiri değişimi, 10Y ihale çevresi (pozitif = getiri yükseliyor = TLT düşüyor) ===")
print(P.round(2).to_string(index=False))
P.to_csv(os.path.join(OUT, "d03_hazine_profil.csv"), index=False)

# (3) TLT haftanın günü etkisi (örneklem), sinyal pencereleri hariç
t = lib.load("TLT").reindex(IDX)
r1 = t["c"].pct_change()
pos = IDX.searchsorted(A10); pos = pos[(pos >= 3) & (pos < len(IDX))]
inwin = np.zeros(len(IDX), bool)
for p in pos: inwin[p - 2] = True; inwin[p - 1] = True
dw = pd.Series(IDX.dayofweek, index=IDX)
tab = pd.DataFrame({"tum": r1.groupby(dw).mean() * 1e4, "pencere_haric": r1[~inwin].groupby(dw[~inwin]).mean() * 1e4,
                    "t_pencere_haric": r1[~inwin].groupby(dw[~inwin]).apply(lambda x: tstat(x.dropna()))})
print("\nTLT 1g ortalama haftanın günü (0=Pzt) 2016-2026:"); print(tab.round(2).to_string())
y = r1[(dw == 0) & ~inwin]; print("Pazartesi (pencere hariç) yıl yıl bp:", (y.groupby(y.index.year).mean() * 1e4).round(1).to_dict())
