"""TEST 1 (kesitsel momentum) + TEST 2 (kisa vadeli reversal) + rejim filtresi.
Evren: sinyal gununde 60g medyan TL hacme gore en likit N (100 / 150) GUNCEL-LISTELI hisse (survivorship!), >=260 gun gecmis.
Momentum skoru: P(t-21)/P(t-21-L)-1, L = 63/126/231 gun (3-1, 6-1, 12-1 ay). Rebalans: haftalik (W1), 2 haftalik (W2), 4 haftalik (W4).
Portfoy: en ust ondalik / besli dilim, EW. Long-only ve 'long - XU100 (VIOP kisa)'.
Reversal: son 5 gun (1 hafta) ve son 21 gun (1 ay) kaybedenler (alt dilim), W1 ve W4.
Maliyet: 25 bp gidis-donus (12.5/yon), stres 50 bp. Kiyas: ayni evrenin EW'si (ayni rebalans), XU100, TL rf. Placebo: motor.placebo."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
from motor import *
B = base(); cal = B.index
px = pd.read_parquet(f"{DD}/panel_px.parquet"); rank = pd.read_parquet(f"{DD}/panel_liqrank.parquet")
pxf = px.ffill()
xu = load_index("XU100").reindex(cal).ffill()
START = pd.Timestamp("2010-01-01")
rows = []; yt = {}; plac = {}; series = {}
NPL = int(os.environ.get("NPL", "200"))

def setup(freq):
    sd, ex = exec_dates(rebal_dates(freq, cal, "2009-06-01"))
    R = period_R(pxf, ex); n = len(R)
    xuR = period_R(xu.to_frame(), ex).iloc[:, 0].values
    rfp = compound_between(B.rf_d, ex).iloc[:n].values; tbp = compound_between(B.tb_d, ex).iloc[:n].values
    fxp = compound_between(B.fx_r, ex).iloc[:n].values
    sd, ex = sd[:n], ex[:n]
    reg = (xu > xu.rolling(200).mean()).reindex(sd).values
    st = np.flatnonzero(ex >= START)[0]
    return dict(sd=sd, ex=ex, R=R.values, xuR=xuR, rfp=rfp, tbp=tbp, fxp=fxp, reg=reg, st=st, ppy=len(ex) / ((ex[-1] - ex[0]).days / 365.25))

S = {f: setup(f) for f in ("W1", "W2", "W4")}

def rec(name, r, s, meta, rel=False):
    st = s["st"]; r = np.asarray(r)[st:]; d = s["ex"][st:]
    for cur in (("TL",) if rel else ("TL", "USD")):
        rr = r if cur == "TL" else to_usd(r, s["fxp"][st:]); rf = s["rfp"][st:] if cur == "TL" else s["tbp"][st:]
        if rel: rf = np.zeros(len(rr))   # goreli seri: CAGR = EW'ye gore yillik fark, Sharpe = bilgi orani
        a = stats(rr, rf, dates=d); m = d >= pd.Timestamp("2024-01-01"); b = stats(rr[m], rf[m], dates=d[m])
        rows.append(dict(strateji=name, para=cur, **meta, **a, CAGR_24_26=b.get("CAGR"), Fazla_24_26=b.get("Fazla"), MaxDD_24_26=b.get("MaxDD")))
        if cur == "TL": yt[name] = yearly(rr, d)

def avail_for(s, N):
    rk = rank.reindex(s["sd"]).values
    return (rk <= N) & ~np.isnan(rk)

for N in (100, 150):
    for f in ("W1", "W2", "W4"):
        s = S[f]; av = avail_for(s, N)
        # kiyas: ayni evrenin EW'si
        ew_sel = [np.flatnonzero(a) for a in av]
        r_ew, _ = period_engine(ew_sel, s["R"], 0.00125, s["rfp"])
        rec(f"EW evren top{N} {f}", r_ew, s, dict(test="kiyas", evren=N, frek=f))
        if N == 150 and f == "W4":
            rec("XU100 al-tut (W4 donem)", s["xuR"], s, dict(test="kiyas", evren=0, frek=f)); rec("TL rf (W4)", s["rfp"], s, dict(test="kiyas", evren=0, frek=f))
        for L, ln in ((63, "3-1"), (126, "6-1"), (231, "12-1")):
            sc = (pxf.shift(21) / pxf.shift(21 + L) - 1).reindex(s["sd"]).values
            for q, qn in ((0.1, "D10"), (0.2, "Q5")):
                sel = select(sc, av, q=q)
                for cn, cs in (("25bp", 0.00125), ("50bp", 0.0025)):
                    r, to = period_engine(sel, s["R"], cs, s["rfp"])
                    meta = dict(test="MOM", evren=N, frek=f, L=ln, dilim=qn, maliyet=cn, turnover=to[s["st"]:].mean())
                    rec(f"MOM{ln} {qn} top{N} {f} {cn}", r, s, meta)
                    if cn == "25bp":
                        rec(f"MOM{ln} {qn} top{N} {f} {cn} EW'ye gore fark", (1 + r) / (1 + r_ew) - 1, s, dict(meta, test="MOM-EW"), rel=True)
                        ls = r - (s["xuR"] - s["rfp"])
                        rec(f"MOM{ln} {qn} top{N} {f} {cn} LS(-XU100)", ls, s, dict(meta, test="MOM-LS"))
                        rr, _ = period_engine(apply_regime(sel, s["reg"]), s["R"], cs, s["rfp"])
                        rec(f"MOM{ln} {qn} top{N} {f} {cn} +rejim", rr, s, dict(meta, test="MOM-rejim"))
                        if N == 150 and qn == "Q5":
                            P_ = placebo(sel, av, s["R"], cs, s["rfp"], n=NPL, seed=L)
                            st = s["st"]; ppy = s["ppy"]
                            shp = np.array([sharpe(p[st:], s["rfp"][st:], ppy) for p in P_]); s0 = sharpe(r[st:], s["rfp"][st:], ppy)
                            cg = np.array([np.prod(1 + p[st:]) ** (ppy / len(p[st:])) - 1 for p in P_])
                            plac[f"MOM{ln} Q5 top150 {f}"] = dict(Sharpe=s0, CAGR=float(np.prod(1 + r[st:]) ** (ppy / len(r[st:])) - 1),
                                placebo_medyan_Sharpe=float(np.median(shp)), placebo_p95=float(np.percentile(shp, 95)), yuzdelik=float((shp < s0).mean()),
                                placebo_medyan_CAGR=float(np.median(cg)))
        # REVERSAL
        for L, ln in ((5, "1h"), (21, "1ay")):
            if (L == 5 and f != "W1") or (L == 21 and f == "W2"): continue
            sc = (pxf / pxf.shift(L) - 1).reindex(s["sd"]).values
            for q, qn in ((0.1, "D10"), (0.2, "Q5")):
                sel = select(sc, av, q=q, bottom=True)
                for cn, cs in (("25bp", 0.00125), ("50bp", 0.0025)):
                    r, to = period_engine(sel, s["R"], cs, s["rfp"])
                    meta = dict(test="REV", evren=N, frek=f, L=ln, dilim=qn, maliyet=cn, turnover=to[s["st"]:].mean())
                    rec(f"REV{ln} {qn} top{N} {f} {cn}", r, s, meta)
                    if cn == "25bp":
                        rec(f"REV{ln} {qn} top{N} {f} {cn} EW'ye gore fark", (1 + r) / (1 + r_ew) - 1, s, dict(meta, test="REV-EW"), rel=True)
                        if N == 150 and qn == "D10":
                            P_ = placebo(sel, av, s["R"], cs, s["rfp"], n=NPL, seed=L + 1)
                            st = s["st"]; ppy = s["ppy"]
                            shp = np.array([sharpe(p[st:], s["rfp"][st:], ppy) for p in P_]); s0 = sharpe(r[st:], s["rfp"][st:], ppy)
                            plac[f"REV{ln} D10 top150 {f}"] = dict(Sharpe=s0, placebo_medyan_Sharpe=float(np.median(shp)), placebo_p95=float(np.percentile(shp, 95)), yuzdelik=float((shp < s0).mean()))
# KISA VADELI KAZANANLAR (reversal'in aynasi; reversal negatif cikinca eklendi - post-hoc oldugu raporda belirtildi)
for N in (100, 150):
    for f in ("W1", "W4"):
        s = S[f]; av = avail_for(s, N)
        ew_sel = [np.flatnonzero(a) for a in av]; r_ew, _ = period_engine(ew_sel, s["R"], 0.00125, s["rfp"])
        for L, ln in ((5, "1h"), (21, "1ay")):
            if L == 5 and f != "W1": continue
            sc = (pxf / pxf.shift(L) - 1).reindex(s["sd"]).values
            for q, qn in ((0.1, "D10"), (0.2, "Q5")):
                sel = select(sc, av, q=q)
                r, to = period_engine(sel, s["R"], 0.00125, s["rfp"])
                meta = dict(test="KMOM", evren=N, frek=f, L=ln, dilim=qn, maliyet="25bp", turnover=to[s["st"]:].mean())
                rec(f"KMOM{ln} {qn} top{N} {f} 25bp", r, s, meta)
                rec(f"KMOM{ln} {qn} top{N} {f} 25bp EW'ye gore fark", (1 + r) / (1 + r_ew) - 1, s, dict(meta, test="KMOM-EW"), rel=True)
                if N == 150 and qn == "D10":
                    P_ = placebo(sel, av, s["R"], 0.00125, s["rfp"], n=min(NPL, 100), seed=L + 7)
                    st = s["st"]; ppy = s["ppy"]
                    shp = np.array([sharpe(p[st:], s["rfp"][st:], ppy) for p in P_]); s0 = sharpe(r[st:], s["rfp"][st:], ppy)
                    plac[f"KMOM{ln} D10 top150 {f}"] = dict(Sharpe=s0, placebo_medyan_Sharpe=float(np.median(shp)), placebo_p95=float(np.percentile(shp, 95)), yuzdelik=float((shp < s0).mean()))
df = pd.DataFrame(rows); df.to_csv(f"{OUTD}/t01_ozet.csv", index=False)
pd.DataFrame(yt).to_csv(f"{OUTD}/t01_yillik_TL.csv"); json.dump(plac, open(f"{OUTD}/t01_placebo.json", "w"), indent=1)
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 900)
T = df[df.para == "TL"]
print(T[T.test == "kiyas"][["strateji", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26"]].round(3).to_string())
for t in ("MOM", "MOM-EW", "MOM-LS", "MOM-rejim", "REV", "REV-EW", "KMOM", "KMOM-EW"):
    g = T[(T.test == t) & (T.maliyet == "25bp")]
    print(t, "izgara medyani (TL, 25bp):", g[["CAGR", "Fazla", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26"]].median().round(3).to_dict(), "n=", len(g))
print(T[T.test.isin(["KMOM", "KMOM-EW"])][["strateji", "turnover", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "CAGR_24_26", "Fazla_24_26"]].round(3).to_string())
print(T[T.test.isin(["MOM", "REV"]) & (T.maliyet == "25bp")][["strateji", "turnover", "CAGR", "Fazla", "Vol", "Sharpe", "MaxDD", "Isabet", "CAGR_24_26", "Fazla_24_26"]].round(3).to_string())
print(json.dumps(plac, indent=0))
