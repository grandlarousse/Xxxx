"""Ek testler: (1) TUPRS/diğerleri USDTRY betası (haftalık/aylık TL getiri ~ USDTRY + XU100); (2) aylık USD bazlı sektör emsal ilişkileri;
(3) SASA 'bireysel yatırımcı faktörü'; (4) çeyreklik ortalama crack değişimi -> TUPRS aynı/sonraki çeyrek (bilanço kanalı);
(5) 250g kayan korelasyon özetleri (TUPRS~BZ, TUPRS~CRAK)."""
import pandas as pd, numpy as np, statsmodels.api as sm, elib
from elib import R, DEC, ll
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)
STK = ["TUPRS", "PETKM", "SASA", "AKSEN", "ENJSA", "ODAS"]
px = pd.concat({s: ll.daily(s) for s in STK + ["XU100", "TRY=X"]}, axis=1)
# (1) USDTRY betası
for rule, lab in [("W-FRI", "haftalık"), ("ME", "aylık")]:
    r = np.log(px.resample(rule).last()).diff(); r = r[r.index >= "2014-01-01"]
    row = []
    for s in STK + ["XU100"]:
        X = r[[s, "TRY=X"] + ([] if s == "XU100" else ["XU100"])].dropna()
        if s == "XU100":
            m = sm.OLS(X[s], sm.add_constant(X[["TRY=X"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 4}); row.append(f"XU100: b_usd={m.params['TRY=X']:.2f}(t={m.tvalues['TRY=X']:.1f})")
        else:
            m = sm.OLS(X[s], sm.add_constant(X[["TRY=X", "XU100"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
            row.append(f"{s}: b_usd|XU={m.params['TRY=X']:.2f}(t={m.tvalues['TRY=X']:.1f})")
    P(f"== (1) {lab} TL getiri ~ USDTRY (+XU100): " + "; ".join(row))
# (2) aylık USD bazlı emsal
def usd_m(sym):
    p = ll.daily(sym)
    if sym.endswith(".IS") or sym in STK or sym == "XU100": p = p / ll.daily("TRY=X")
    return np.log(p.resample("ME").last()).diff()
B = {"PETKM": {"PETCHEM": ["LYB", "DOW", "BAS.DE", "WLK", "051910.KS", "011170.KS", "PTTGC.BK", "1301.TW", "1303.TW"], "BZ": ["BZ=F"]},
     "SASA": {"POLYESTER": ["IVL.BK", "ALPEKA.MX", "1326.TW", "3402.T"], "BZ": ["BZ=F"], "PAMUK": ["CT=F"]},
     "AKSEN": {"EU_UTIL": ["EOAN.DE", "RWE.DE", "ENEL.MI", "IBE.MC", "ENGI.PA", "EDP.LS", "PGE.WA", "CEZ.PR", "PPC.AT"], "TTF": ["TTF=F"]},
     "ENJSA": {"EU_UTIL": ["EOAN.DE", "RWE.DE", "ENEL.MI", "IBE.MC", "ENGI.PA", "EDP.LS"], "TTF": ["TTF=F"]},
     "ODAS": {"ALTIN": ["GC=F"], "ALTIN_MAD": ["GDX"], "KOMUR": ["MTF=F"], "TTF": ["TTF=F"]},
     "TUPRS": {"US_REF": ["VLO", "MPC", "PSX", "PBF"], "EU_REF": ["PKN.WA", "MOL.BD", "MOH.AT", "ELPE.AT", "NESTE.HE", "GALP.LS", "REP.MC", "OMV.VI"], "BZ": ["BZ=F"]}}
xu_m = usd_m("XU100")
rows = []
for s, dd in B.items():
    a = usd_m(s)
    for nm, syms in dd.items():
        b = pd.concat([usd_m(x) for x in syms], axis=1).mean(axis=1)
        X = pd.concat([a.rename("a"), b.rename("b"), xu_m.rename("xu")], axis=1).dropna(); X = X[X.index >= "2014-01-01"]
        r = {"stock": s, "drv": nm, "n": len(X), "c": X.a.corr(X.b), "pc": ll.partial_corr(X.a, X.b, [X.xu])[0],
             "pc_is": ll.partial_corr(X[X.index < "2021"].a, X[X.index < "2021"].b, [X[X.index < "2021"].xu])[0],
             "pc_oos": ll.partial_corr(X[X.index >= "2021"].a, X[X.index >= "2021"].b, [X[X.index >= "2021"].xu])[0]}
        bl = X.b.shift(1); Y = pd.concat([X.a, bl, X.xu], axis=1).dropna(); r["pc_lead1m"] = ll.partial_corr(Y.iloc[:, 0], Y.iloc[:, 1], [Y.xu])[0]
        rows.append(r)
M = pd.DataFrame(rows); M.to_csv(elib.RES + "/monthly_usd_peers.csv", index=False)
P("== (2) aylık USD getiri, XU100(USD) kontrollü kısmi korelasyon"); P(M.round(2).to_string(index=False))
# (3) SASA bireysel faktör
RET = ["HEKTS", "KONTR", "ASTOR", "SMRTG", "EUPWR", "GESAN", "CWENE", "YEOTK", "ALFAS"]
rb = pd.concat([R(x) for x in RET], axis=1).mean(axis=1)
xu = R("XU100")
for s in ["SASA", "PETKM", "TUPRS", "ODAS", "AKSEN"]:
    a = R(s); full = ll.partial_corr(a, rb, [xu])[0]
    i_ = ll.partial_corr(a[(a.index >= "2014") & (a.index < "2021")], rb, [xu])[0]; o_ = ll.partial_corr(a[a.index >= "2021"], rb, [xu])[0]
    P(f"== (3) {s} ~ bireysel-favori sepeti ({','.join(RET)}) kısmi(XU100): tam={full:.2f} IS={i_:.2f} OOS={o_:.2f}")
# (4) çeyreklik ortalama crack -> TUPRS
cr = elib.cracks(); q = cr.resample("QE").mean()
tq = np.log((ll.daily("TUPRS") / ll.daily("TRY=X")).resample("QE").last()).diff(); xq = np.log((ll.daily("XU100") / ll.daily("TRY=X")).resample("QE").last()).diff()
for c in ["ho_crack", "c321"]:
    dc = q[c].diff() / q.BZ.shift(1)
    X = pd.concat([tq.rename("tu"), dc.rename("dc"), xq.rename("xu")], axis=1).dropna(); X = X[X.index >= "2010"]
    Y = pd.concat([tq.rename("tu"), dc.shift(1).rename("dc"), xq.rename("xu")], axis=1).dropna(); Y = Y[Y.index >= "2010"]
    P(f"== (4) çeyrek ort. {c} değişimi: aynı çeyrek c={X.tu.corr(X.dc):.2f} pc={ll.partial_corr(X.tu, X.dc, [X.xu])[0]:.2f} | sonraki çeyrek c={Y.tu.corr(Y.dc):.2f} pc={ll.partial_corr(Y.tu, Y.dc, [Y.xu])[0]:.2f} (n={len(Y)})")
# (5) kayan korelasyon özetleri
for d in ["BZ=F", "CRAK", "HO=F"]:
    rc = ll.rolling_corr(R("TUPRS"), R(d), 250).dropna(); rc = rc[rc.index >= "2012"]
    P(f"== (5) TUPRS~{d} 250g kayan corr: min={rc.min():.2f} medyan={rc.median():.2f} max={rc.max():.2f} >0 oranı={(rc > 0).mean():.2f} son={rc.iloc[-1]:.2f}")
open(elib.RES + "/07_misc.txt", "w").write("\n".join(out))
