"""(4) Sinyal neyin vekili? Kontroller, ayrıştırma, basit biçimler, doz-tepki."""
import numpy as np, pandas as pd, statsmodels.api as sm
from adv_lib import *
R = us_returns(); e, B = rolling_resid(R); pv = viop(); r = pv.v_ret
bh = (np.exp(r) - 1).iloc[1:]
E10 = e.rolling(10).sum(); thr = E10[:"2017-12-31"].dropna().quantile(.8)
x, _ = map_us_to_viop(E10, pv.index); sig = (x > thr).astype(float)
def M(ser): return map_us_to_viop(ser, pv.index)[0]
def lr(tk, k):
    p = np.log(yahoo(tk)); return (p - p.shift(k))
C = pd.DataFrame(index=pv.index)
for k in (5, 10, 20): C[f"GLD{k}"] = M(R.GLD.rolling(k).sum())
C["GDX10"] = M(R.GDX.rolling(10).sum()); C["GDX5"] = M(R.GDX.rolling(5).sum()); C["SPY10"] = M(R.SPY.rolling(10).sum())
C["VIX10"] = M(lr("_VIX", 10)); C["DXY10"] = M(lr("DX-Y.NYB", 10)); C["UUP10"] = M(lr("UUP", 10)); C["GVZ10"] = M(lr("_GVZ", 10))
for k in (5, 10, 20): C[f"V{k}"] = r.rolling(k).sum()           # VİOP'un kendi momentumu, gün t uzlaşmasına kadar (giriş anında bilinir)
C["vol20"] = r.rolling(20).std()
print("sinyal (0/1) ile kontrollerin korelasyonu:"); print(C.corrwith(sig).round(2).to_string())
print("x (sürekli) ile:", C.corrwith(x).round(2).to_dict())
def reg(h, cols, a=None, b=None, L=10, sname="sig", s=sig):
    d = pd.concat([fwd(r, h).rename("y"), s.rename(sname), C[cols]], axis=1)[a:b].dropna()
    Z = d[cols]; Z = (Z - Z.mean()) / Z.std()
    m = sm.OLS(d.y, sm.add_constant(pd.concat([d[[sname]], Z], axis=1))).fit(cov_type="HAC", cov_kwds={"maxlags": max(L, h)})
    return m
sets = {"yok": [], "altın mom (GLD5,10,20)": ["GLD5", "GLD10", "GLD20"], "VİOP mom (V5,V10,V20; giriş anına kadar)": ["V5", "V10", "V20"], "GDX10 mutlak": ["GDX10"], "SPY10": ["SPY10"],
        "VIX10": ["VIX10"], "dolar (DXY10)": ["DXY10"], "GVZ10+vol20": ["GVZ10", "vol20"], "hepsi (GLD5/10/20,SPY10,VIX10,DXY10,vol20)": ["GLD5", "GLD10", "GLD20", "SPY10", "VIX10", "DXY10", "vol20"],
        "hepsi + GDX10": ["GLD5", "GLD10", "GLD20", "SPY10", "VIX10", "DXY10", "vol20", "GDX10"]}
print("\n=== KONTROLLÜ REGRESYON: fwd_h = a + b·SİNYAL + kontroller (z-skor) ; b % ve NW t ===")
for nm, a, b_ in [("2017-03..2026", None, None), ("2018..2026", "2018", None), ("2026 hariç", None, "2025")]:
    print(f"[{nm}]")
    for sn, cols in sets.items():
        o = []
        for h in (3, 5):
            m = reg(h, cols, a, b_); o.append(f"h{h}: b {m.params['sig']*100:+.3f}% t {m.tvalues['sig']:.2f}")
        ex = ""
        if cols:
            m = reg(5, cols, a, b_); ex = " | h5 kontrol t: " + ", ".join(f"{c} {m.tvalues[c]:+.1f}" for c in cols)
        print(f"  {sn:45s} " + " | ".join(o) + ex)
print("\n=== AYRIŞTIRMA (sürekli): fwd_h ~ GDX10 + GLD10 + SPY10 (ham, katsayı = 1 birim getiri başına) ===")
for nm, a, b_ in [("2017-03..2026", None, None), ("2018..2026", "2018", None), ("2018..2024", "2018", "2024")]:
    for h in (3, 5):
        d = pd.concat([fwd(r, h).rename("y"), C[["GDX10", "GLD10", "SPY10"]]], axis=1)[a:b_].dropna()
        m = sm.OLS(d.y, sm.add_constant(d[["GDX10", "GLD10", "SPY10"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
        print(f"  [{nm}] h{h}: GDX10 {m.params['GDX10']:+.4f} (t {m.tvalues['GDX10']:.2f}) | GLD10 {m.params['GLD10']:+.4f} (t {m.tvalues['GLD10']:.2f}) | SPY10 {m.params['SPY10']:+.4f} (t {m.tvalues['SPY10']:.2f}) | −GLD/GDX oranı {(-m.params['GLD10']/m.params['GDX10']):.2f}")
        for c in ("GDX10", "GLD10", "x"):
            dd = pd.concat([fwd(r, h).rename("y"), (x if c == "x" else C[c]).rename("c")], axis=1)[a:b_].dropna()
            m1 = sm.OLS(dd.y, sm.add_constant(dd.c)).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
            print(f"       tek başına {c}: {m1.params['c']:+.4f} (t {m1.tvalues['c']:.2f})", end="")
        print()
print("\n=== DOZ–TEPKİ: x'in (2018 öncesi dağılıma göre) beşte birlik dilimleri → sonraki 3/5 gün ort. % ===")
qs = E10[:"2017-12-31"].dropna().quantile([.2, .4, .6, .8]).values; lab = pd.cut(x, [-np.inf, *qs, np.inf], labels=["Q1 (en zayıf)", "Q2", "Q3", "Q4", "Q5 (sinyal)"])
for nm, a, b_ in [("2017-03..2026", None, None), ("2018..2026", "2018", None), ("2018..2024", "2018", "2024"), ("2025..2026", "2025", None)]:
    d = pd.DataFrame({"q": lab, "f3": fwd(r, 3) * 100, "f5": fwd(r, 5) * 100})[a:b_].dropna()
    print(f"[{nm}]"); print(d.groupby("q").agg(n=("f3", "size"), h3=("f3", "mean"), h5=("f5", "mean")).round(3).T.to_string())
q9 = E10[:"2017-12-31"].dropna().quantile([.8, .9, .95]).values
d = pd.DataFrame({"x": x, "f3": fwd(r, 3) * 100, "f5": fwd(r, 5) * 100}).dropna()
for lo, hi, nm in [(q9[0], q9[1], "q80–q90"), (q9[1], q9[2], "q90–q95"), (q9[2], np.inf, ">q95")]:
    m = (d.x > lo) & (d.x <= hi); print(f"  sinyal içi {nm}: n {int(m.sum())} h3 {d.f3[m].mean():+.3f} h5 {d.f5[m].mean():+.3f}")
# ---------- basit biçimler
print("\n=== BASİT BİÇİMLER (eşik = her birinin 2018 öncesi q80'i; H=3, 5 bps) ===")
RJ = us_returns(("GDXJ", "GLD", "SPY")); ej, _ = rolling_resid(RJ, y="GDXJ")
e_ns, Bns = rolling_resid(R, xs=("GLD",))
V = {"V0 tam kural: GDX−b·GLD−b·SPY (250g OLS)": e.rolling(10).sum(),
     "V1 SPY'siz: GDX−b·GLD (250g OLS)": e_ns.rolling(10).sum(),
     "V2 sabit beta: GDX10−2·GLD10": (R.GDX - 2 * R.GLD).rolling(10).sum(),
     "V3 oran: ln(GDX/GLD) 10g değişimi (beta=1)": (R.GDX - R.GLD).rolling(10).sum(),
     "V4 sabit: GDX10−2·GLD10−0,5·SPY10": (R.GDX - 2 * R.GLD - 0.5 * R.SPY).rolling(10).sum(),
     "V4b sabit: GDX10−1,5·GLD10−0,5·SPY10": (R.GDX - 1.5 * R.GLD - 0.5 * R.SPY).rolling(10).sum(),
     "V5 yalnız GDX10 (mutlak)": R.GDX.rolling(10).sum(),
     "V6 yalnız GLD10 (altın momentumu)": R.GLD.rolling(10).sum(),
     "V7 GDX10−SPY10 (altınsız)": (R.GDX - R.SPY).rolling(10).sum(),
     "V8 GDXJ tam (250g OLS)": ej.rolling(10).sum(),
     "V9 −GLD10 (altın düşmüş)": -R.GLD.rolling(10).sum()}
rows = []
for nm, ser in V.items():
    th = ser[:"2017-12-31"].dropna().quantile(.8); xv, _ = map_us_to_viop(ser, pv.index); sv = (xv > th).astype(float)
    pos = position(sv, 3); p = pnl(pos, r, 5); t = trades(pos, r, 5); tc = t[~t.open_]
    row = dict(bicim=nm, esik=round(th * 100, 2), n=int(sv.sum()), ortusme_V0=round((sv[sig > 0] > 0).mean(), 2))
    for per, a, b_ in [("tam", None, None), ("18-26", "2018", None), ("18-24", "2018", "2024")]:
        row[f"h3t_{per}"] = round(nw_diff(fwd(r, 3)[a:b_], sv[a:b_], 10)["t"], 2); row[f"h5t_{per}"] = round(nw_diff(fwd(r, 5)[a:b_], sv[a:b_], 10)["t"], 2)
    row["Sharpe"] = round(sharpe(p), 2); al = alpha(p, bh); row["alfa%"] = round(al[0], 1); row["alfa_t"] = round(al[1], 2)
    al2 = alpha(p["2018":], bh["2018":]); row["alfa_t_18+"] = round(al2[1], 2); row["islem"] = len(tc); row["ort%"] = round(tc.ret.mean() * 100, 2); row["kazanan"] = round((tc.ret > 0).mean(), 2)
    rows.append(row)
pd.set_option("display.width", 250); print(pd.DataFrame(rows).set_index("bicim").to_string())
# yarış: V0 sinyali ile basit biçim sinyali aynı regresyonda
print("\n=== YARIŞ: V0 kukla + rakip kukla aynı regresyonda (h5, tam örneklem) ===")
for nm in ["V2 sabit beta: GDX10−2·GLD10", "V3 oran: ln(GDX/GLD) 10g değişimi (beta=1)", "V4 sabit: GDX10−2·GLD10−0,5·SPY10", "V5 yalnız GDX10 (mutlak)", "V6 yalnız GLD10 (altın momentumu)", "V7 GDX10−SPY10 (altınsız)"]:
    ser = V[nm]; th = ser[:"2017-12-31"].dropna().quantile(.8); xv, _ = map_us_to_viop(ser, pv.index); sv = (xv > th).astype(float)
    for h in (3, 5):
        d = pd.DataFrame({"y": fwd(r, h), "v0": sig, "alt": sv}).dropna()
        m = sm.OLS(d.y, sm.add_constant(d[["v0", "alt"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 10})
        print(f"  h{h} {nm:45s} V0 b {m.params['v0']*100:+.3f} t {m.tvalues['v0']:.2f} | rakip b {m.params['alt']*100:+.3f} t {m.tvalues['alt']:.2f}")
# sinyal aktifken altın momentumu yönü: sinyal & GLD10>0 / <0
print("\n=== Sinyal günlerini böl: önceki 10 günde altın yükselmiş mi düşmüş mü? ===")
d = pd.DataFrame({"s": sig, "g": C.GLD10, "gdx": C.GDX10, "f3": fwd(r, 3) * 100, "f5": fwd(r, 5) * 100}).dropna()
for nm, m in [("sinyal & GLD10>0", (d.s > 0) & (d.g > 0)), ("sinyal & GLD10<=0", (d.s > 0) & (d.g <= 0)), ("sinyal yok & GLD10>0", (d.s == 0) & (d.g > 0)), ("sinyal yok & GLD10<=0", (d.s == 0) & (d.g <= 0)),
              ("sinyal & GDX10>0", (d.s > 0) & (d.gdx > 0)), ("sinyal & GDX10<=0", (d.s > 0) & (d.gdx <= 0)), ("sinyal yok & GDX10>%5", (d.s == 0) & (d.gdx > .05))]:
    print(f"  {nm:25s} n {int(m.sum()):4d}  h3 {d.f3[m].mean():+.3f}  h5 {d.f5[m].mean():+.3f}")
