"""G1 (ES gece -> gap), G4 (TUR | ES), G5 (5 dk ES -> XU030 gecikme)."""
import numpy as np, pandas as pd
from vcore import *
log = open(f"{OUT}/v2_gunici.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n"); log.flush()

c = cal()
# yarım günler: XU030 h1 son bar başlangıcı < 12:00
hx = bars("XU030.IS", "h1"); lastbar = pd.Series(hx.index, index=hx.index).groupby(hx.index.tz_convert(None).normalize()).max()
half = set(lastbar[lastbar.dt.hour < 12].index)
P("yarım gün sayısı (h1 dönemi):", len(half), sorted(d.date() for d in half))
c = c[c >= "2023-11-30"]
prev = pd.Series(c[:-1], index=c[1:])  # t -> önceki BIST günü
ok = [t for t in prev.index if (t not in half) and (prev[t] not in half)]
prev = prev.loc[ok]

def overnight(sym, h0="15:00", h1="07:00", prev_=prev):
    sn = snap(sym, [h0, h1])
    a = sn[h0].reindex(prev_.values).values; b = sn[h1].reindex(prev_.index).values
    return pd.Series(np.log(b / a), index=prev_.index)

def us_close_window(sym, h0="15:30", prev_=prev):
    """t-1 günü h0 UTC -> t-1 ABD kapanışı (günlük c)."""
    sn = snap(sym, [h0])[h0]
    dc = frame(sym)["c"]
    a = sn.reindex(prev_.values).values; b = dc.reindex(prev_.values).values
    return pd.Series(np.log(b / a), index=prev_.index)

ES = overnight("ES=F")
ES06 = overnight("ES=F", "15:00", "06:00")
ES_a = overnight("ES=F", "15:00", "16:00"); ES_b = overnight("ES=F", "16:00", "20:00")
ES_c = pd.Series(np.log(snap("ES=F", ["07:00"])["07:00"].reindex(prev.index).values / snap("ES=F", ["20:00"])["20:00"].reindex(prev.values).values), index=prev.index)
TUR = us_close_window("TUR"); EEMw = us_close_window("EEM"); TKCw = us_close_window("TKC")
USD = overnight("TRY=X")
gx = decomp("XU030.IS").reindex(prev.index); g100 = decomp("XU100.IS").reindex(prev.index)
GAP = gx["gap"]; INTRA = gx["intra"]
P(f"\nG1 örneklem: {ES.dropna().index.min().date()}..{ES.dropna().index.max().date()} n(ES&gap)={pd.concat([ES, GAP], axis=1).dropna().shape[0]}")
def rep(y, x, ctrl=None, lab=""):
    df = pd.concat([y.rename("y"), x.rename("x")] + ([ctrl] if ctrl is not None else []), axis=1).dropna()
    out = {}
    for w, (a, b) in {"tam": ("2000", "2030"), "IS(<=2025-06)": ("2000", "2025-06-30"), "OOS(2025-07+)": ("2025-07-01", "2030"), "1y": ("2025-10-31", "2030")}.items():
        out[w] = pc(df.y, df.x, df.drop(columns=["y", "x"]) if ctrl is not None else None, (a, b))
    yrs = {yr: pc(df.y, df.x, df.drop(columns=["y", "x"]) if ctrl is not None else None, (f"{yr}-01-01", f"{yr}-12-31"))["r"] for yr in [2024, 2025, 2026]}
    s = " | ".join(f"{w}: r {v['r']:+.3f} b {v['b']:+.3f} tHC {v['t']:+.2f} tOLS {v.get('t_ols', np.nan):+.2f} n {v['n']}" for w, v in out.items())
    P(f"{lab:38s} {s} | yıllar {', '.join(f'{k}:{v:+.2f}' for k, v in yrs.items())}")
    return out
o = rep(GAP, ES, None, "XU030 gap ~ ES(15->07)")
rep(GAP, ES06, None, "XU030 gap ~ ES(15->06) [açılış öncesi]")
rep(g100["gap"], ES, None, "XU100 gap ~ ES(15->07)")
rep(GAP, ES, pd.concat([USD.rename("usd"), EEMw.rename("eem")], axis=1), "XU030 gap ~ ES | USDTRY gece + EEM")
rep(INTRA, ES, None, "XU030 gün-içi ~ ES gece (devam?)")
for nm, x in [("ES 15-16", ES_a), ("ES 16-20", ES_b), ("ES 20-07", ES_c)]:
    rep(GAP, x, None, f"XU030 gap ~ {nm}")
# robust: winsorize %1
w = lambda s: s.clip(s.quantile(0.01), s.quantile(0.99))
rep(w(GAP), w(ES), None, "XU030 gap ~ ES (winsor %1)")
# Spearman
df = pd.concat([GAP, ES], axis=1).dropna(); P("Spearman XU030 gap~ES:", round(df.corr("spearman").iloc[0, 1], 3))

# 47 hisse
rows = []
for s in VIOP:
    g = decomp(s + ".IS").reindex(prev.index)["gap"]
    a = pc(g, ES); b = pc(g, ES, g100[["gap"]].rename(columns={"gap": "xu"}))
    t1 = pc(g, TUR, ES.rename("es").to_frame()); t2 = pc(g, TUR, pd.concat([ES.rename("es"), USD.rename("usd"), EEMw.rename("eem")], axis=1))
    rows.append(dict(stock=s, r_ES=a["r"], t_ES=a["t"], n=a["n"], pc_ES_xu100gap=b["r"], pc_TUR_ES=t1["r"], t_TUR_ES=t1["t"], pc_TUR_ES_USD_EEM=t2["r"]))
H = pd.DataFrame(rows).set_index("stock"); H.round(3).to_csv(f"{OUT}/g1_g4_stocks.csv")
P("\n47 hisse gap~ES gece: medyan r", round(H.r_ES.median(), 3), "| min/maks", H.r_ES.idxmin(), round(H.r_ES.min(), 2), H.r_ES.idxmax(), round(H.r_ES.max(), 2))
P("  bankalar:", H.loc[["AKBNK", "GARAN", "YKBNK", "ISCTR", "VAKBN", "HALKB"], "r_ES"].round(2).to_dict())
P("  SASA/ENJSA/ASELS:", H.loc[["SASA", "ENJSA", "ASELS"], "r_ES"].round(2).to_dict())
P("  XU100 gap kontrollü pc (hisseye özgü ES): medyan", round(H.pc_ES_xu100gap.median(), 3), "| |pc|>0,10 sayısı", int((H.pc_ES_xu100gap.abs() > 0.1).sum()))

P("\nG4: TUR(15:30->ABD kapanışı, t-1) ES'e ek bilgi")
rep(GAP, TUR, None, "XU030 gap ~ TUR")
rep(GAP, TUR, ES.rename("es").to_frame(), "XU030 gap ~ TUR | ES")
rep(GAP, TUR, pd.concat([ES.rename("es"), USD.rename("usd"), EEMw.rename("eem")], axis=1), "XU030 gap ~ TUR | ES+USDTRY+EEM")
rep(GAP, EEMw, ES.rename("es").to_frame(), "XU030 gap ~ EEM(15:30->kap) | ES")
rep(INTRA, TUR, ES.rename("es").to_frame(), "XU030 gün-içi ~ TUR | ES")
P("  hisseler: pc(TUR|ES) medyan", round(H.pc_TUR_ES.median(), 3), "; >0,10 olan", int((H.pc_TUR_ES > 0.1).sum()), "/47; pc(TUR|ES,USD,EEM) medyan", round(H.pc_TUR_ES_USD_EEM.median(), 3))
tc = decomp("TCELL.IS").reindex(prev.index)["gap"]
rep(tc, TKCw, None, "TCELL gap ~ TKC(15:30->kap)")
rep(tc, TKCw, pd.concat([ES.rename("es"), TUR.rename("tur")], axis=1), "TCELL gap ~ TKC | ES+TUR")

# ===================== G5: 5 dk =====================
P("\nG5: 5 dk ES -> XU030 (sürekli işlem 07:00-14:55 UTC bar başlangıcı)")
def m5ret(sym):
    m = bars(sym, "m5")
    cc = np.log(m["c"]); day = m.index.tz_convert(None).normalize()
    r = cc.groupby(day).diff()
    return r
rx = m5ret("XU030.IS"); re = m5ret("ES=F")
J = pd.concat([rx.rename("x"), re.rename("e")], axis=1)
J = J[(J.index.hour * 60 + J.index.minute >= 7 * 60) & (J.index.hour * 60 + J.index.minute <= 14 * 60 + 55)]
J["day"] = J.index.tz_convert(None).normalize()
for k in range(1, 7):
    J[f"e{k}"] = J.groupby("day")["e"].shift(k); J[f"x{k}"] = J.groupby("day")["x"].shift(k)
J["e_lead1"] = J.groupby("day")["e"].shift(-1)
JJ = J.dropna()
P(f"  örneklem {JJ.day.min().date()}..{JJ.day.max().date()} gün {JJ.day.nunique()} bar {len(JJ)}")
P("  corr lag0", round(JJ.x.corr(JJ.e), 3), "| lag1 (ES_{k-1}->XU_k)", round(JJ.x.corr(JJ.e1), 3), "| lag2", round(JJ.x.corr(JJ.e2), 3),
  "| XU önde (XU_k -> ES_{k+1})", round(JJ.x.corr(JJ.e_lead1), 3), "| XU030 kendi lag1", round(JJ.x.corr(JJ.x1), 3))
import numpy.linalg as la
def ols_hc(y, X):
    X = np.column_stack([np.ones(len(X)), X]); b = la.lstsq(X, y, rcond=None)[0]; e = y - X @ b
    XtXi = la.inv(X.T @ X); V = XtXi @ (X.T * e ** 2) @ X @ XtXi
    return b, V
cols = ["e"] + [f"e{k}" for k in range(1, 7)] + [f"x{k}" for k in range(1, 7)]
b, V = ols_hc(JJ.x.values, JJ[cols].values)
w = np.zeros(len(b)); w[2:8] = 1; s1 = w @ b; se1 = np.sqrt(w @ V @ w)
P(f"  regresyon XU ~ ES0 + ES1..6 + XU1..6: β0 {b[1]:.3f} (t {b[1]/np.sqrt(V[1,1]):.1f}); Σβ1..6 {s1:.3f} (t {s1/se1:.2f}); gecikmeli pay {s1/(b[1]+s1):.3f}; β1 {b[2]:.3f} (t {b[2]/np.sqrt(V[2,2]):.2f})")
US = JJ[(JJ.index.hour * 60 + JJ.index.minute >= 13 * 60 + 30)]
P("  ABD açılış penceresi (13:30-14:55): lag0", round(US.x.corr(US.e), 3), "lag1", round(US.x.corr(US.e1), 3), "n", len(US))
# 47 hisse
cnt = 0; res = []
for s in VIOP:
    try: rs = m5ret(s + ".IS")
    except Exception: continue
    K = pd.concat([rs.rename("x"), re.rename("e")], axis=1)
    K = K[(K.index.hour * 60 + K.index.minute >= 7 * 60) & (K.index.hour * 60 + K.index.minute <= 14 * 60 + 55)]
    K["day"] = K.index.tz_convert(None).normalize()
    for k in range(1, 7):
        K[f"e{k}"] = K.groupby("day")["e"].shift(k); K[f"x{k}"] = K.groupby("day")["x"].shift(k)
    K = K.dropna()
    if len(K) < 500: continue
    b, V = ols_hc(K.x.values, K[cols].values); s1 = w @ b; se1 = np.sqrt(w @ V @ w)
    res.append(dict(stock=s, lag0=K.x.corr(K.e), lag1=K.x.corr(K.e1), sum16=s1, t16=s1 / se1, own1=K.x.corr(K.x1), n=len(K)))
R5 = pd.DataFrame(res).set_index("stock"); R5.round(3).to_csv(f"{OUT}/g5_stocks.csv")
P(f"  47 hisse: medyan lag0 {R5.lag0.median():.3f}, medyan lag1 {R5.lag1.median():.3f}, Σβ1..6 t>2 sayısı {int((R5.t16 > 2).sum())}/{len(R5)}, t<-2 {int((R5.t16 < -2).sum())}; kendi lag1 medyan {R5.own1.median():.3f}")
log.close()
