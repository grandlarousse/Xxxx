"""Ek tablolar: orneklem, asamalar arasi sure, sizinti (duyuru oncesi birikim payi + anormal hacim), yillik anahtar pencereler,
saglamlik (belirsiz P1 haric / en erken aday P1), VIOP'lu hisseler, kilit istatistikleri."""
import os, numpy as np, pandas as pd
import f20_es as E, f30_analiz as A
from f31_calistir import md, P, P2, T, I, H as HP
OUT = A.OUT
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO",
        "GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL",
        "THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
F = dict(ort=P2, med=P2, t=T, isabet=HP, N=I, G=I, p5=P, p95=P)
def main():
    M = E.matrisler(); H = pd.read_pickle(f"{OUT}/H.pkl"); C = pd.read_pickle(f"{OUT}/C.pkl")
    ev = pd.read_pickle(f"{E.CACHE}/olaylar_bedelsiz.pkl"); ev = ev[ev.hak >= "2015-01-01"]
    s = "# Ek tablolar (otomatik)\n"
    # --- orneklem
    ev["yil"] = ev.hak.dt.year; ev["oran_g"] = ev.oran.map(A.oran_grup)
    o = ev.groupby("yil").agg(N=("kod", "size"), p1=("p1", "count"), p2=("p2", "count"), p3=("p3", "count"), bulten=("bulten_onay_no", "count"),
                              oran_med=("oran", "median"), ge100=("oran", lambda x: (x >= 100).sum()), ge500=("oran", lambda x: (x >= 500).sum())).reset_index()
    o.loc[len(o)] = ["Toplam", len(ev), ev.p1.notna().sum(), ev.p2.notna().sum(), ev.p3.notna().sum(), ev.bulten_onay_no.notna().sum(), ev.oran.median(), (ev.oran >= 100).sum(), (ev.oran >= 500).sum()]
    s += "\n## Orneklem\n\n" + md(o, list(o.columns), dict(oran_med=lambda v: f"{v:.0f}%"))
    s += "\n\nTip dagilimi: " + ", ".join(f"{k}: {v}" for k, v in ev.tip.value_counts().items())
    s += f"\n\nP1 kaynagi: {ev.p1_kaynak.value_counts().to_dict()} ; P3 kaynagi: {ev.p3_kaynak.value_counts().to_dict()} ; P1 belirsiz (detaysiz daha erken aday var): {int(ev.p1_belirsiz.sum())}\n"
    # --- sureler (islem gunu)
    d = H.copy()
    for a, b in [("j_p1", "j_p2"), ("j_p2", "j_p3"), ("j_p3", "j_hak"), ("j_p1", "j_hak")]:
        d[f"{a[2:]}->{b[2:]}"] = d[b].astype(float) - d[a].astype(float)
    cols = ["p1->p2", "p2->p3", "p3->hak", "p1->hak"]
    sr = pd.DataFrame({c: d[c].describe(percentiles=[.1, .25, .5, .75, .9]) for c in cols}).T.reset_index().rename(columns={"index": "aralik"})
    s += "\n## Asamalar arasi sure (islem gunu)\n\n" + md(sr, ["aralik", "count", "10%", "25%", "50%", "75%", "90%"], {c: (lambda v: f"{v:.0f}") for c in ["count", "10%", "25%", "50%", "75%", "90%"]})
    d["donem"] = np.where(d.yil >= 2024, "2024-26", np.where(d.yil >= 2020, "2020-23", "2015-19"))
    sr2 = d.groupby("donem")[cols].median().reset_index()
    s += "\nMedyan, doneme gore:\n\n" + md(sr2, ["donem"] + cols, {c: (lambda v: f"{v:.0f}") for c in cols})
    # --- sizinti: P1 etrafinda
    X = C[C.asama == "p1"].pivot_table(index="i", columns="pencere", values="car")
    need = ["[-60,-1]", "[-20,-1]", "[-5,-1]", "[0,1]"]
    X = X.dropna(subset=need)
    rows = []
    for nm, pre in [("[-60,-1]", "[-60,-1]"), ("[-20,-1]", "[-20,-1]"), ("[-5,-1]", "[-5,-1]")]:
        tot = X[pre] + X["[0,1]"]
        rows.append(dict(on_pencere=pre, N=len(X), on_ort=X[pre].mean(), duyuru_ort=X["[0,1]"].mean(), on_pay_ort=X[pre].mean() / tot.mean(),
                         on_med=X[pre].median(), duyuru_med=X["[0,1]"].median(), on_pay_med=X[pre].median() / (X[pre].median() + X["[0,1]"].median()),
                         on_gt10=(X[pre] > 0.10).mean()))
    L = pd.DataFrame(rows)
    s += "\n## Sizinti: P1 oncesi birikim / (oncesi + [0,1])\n\n" + md(L, list(L.columns), dict(on_ort=P2, duyuru_ort=P2, on_pay_ort=HP, on_med=P2, duyuru_med=P2, on_pay_med=HP, on_gt10=HP, N=I))
    hv = H[["hacim_on5_p1", "hacim_t0_p1", "hacim_on5_hak", "hacim_t0_hak"]].describe(percentiles=[.25, .5, .75]).T.reset_index()
    s += "\nAnormal hacim (TL hacim / [-120,-21] medyani):\n\n" + md(hv, ["index", "count", "25%", "50%", "75%", "mean"], {c: (lambda v: f"{v:.2f}") for c in ["count", "25%", "50%", "75%", "mean"]})
    s += f"\nP1 oncesi 5 gunluk hacim >2x olan olay payi: {(H.hacim_on5_p1 > 2).mean():.0%} ; t0 hacmi >3x: {(H.hacim_t0_p1 > 3).mean():.0%}\n"
    # sizinti alt grup: oran ve boyut
    X2 = X.join(H.set_index("i")[["oran", "pd_rel", "yil"]])
    X2["oran_g"] = X2.oran.map(A.oran_grup); q = H.pd_rel.quantile([1/3, 2/3]).values
    X2["boy_g"] = pd.cut(X2.pd_rel, [-np.inf, q[0], q[1], np.inf], labels=["kucuk", "orta", "buyuk"]).astype(str)
    X2["donem"] = np.where(X2.yil >= 2024, "2024-26", np.where(X2.yil >= 2020, "2020-23", "2015-19"))
    for by in ["oran_g", "boy_g", "donem"]:
        g = X2.groupby(by).agg(N=("[0,1]", "size"), on60=("[-60,-1]", "mean"), on20=("[-20,-1]", "mean"), on20_med=("[-20,-1]", "median"), d01=("[0,1]", "mean"), d01_med=("[0,1]", "median")).reset_index()
        g["on20_pay"] = g.on20 / (g.on20 + g.d01)
        s += f"\n{by}:\n\n" + md(g, list(g.columns), dict(on60=P2, on20=P2, on20_med=P2, d01=P2, d01_med=P2, on20_pay=HP, N=I))
    # --- yillik anahtar pencereler
    key = [("p1", "[0,1]"), ("p1", "[1,20]"), ("p3", "[0,1]"), ("hak", "[-5,-1]"), ("hak", "[1,10]")]
    rows = []
    for (a, w) in key:
        for y, g in C[(C.asama == a) & (C.pencere == w)].groupby("yil"):
            z = E.ozet(g.car, g.t0); rows.append(dict(asama=a, pencere=w, yil=y, N=z["N"], ort=z["ort"], med=z["med"], t=z["t"]))
    Y = pd.DataFrame(rows).pivot_table(index="yil", columns=["asama", "pencere"], values="ort")
    Y.columns = [f"{a} {w}" for a, w in Y.columns]; Y = Y.reset_index()
    s += "\n## Yillik ortalama CAR (anahtar pencereler)\n\n" + md(Y, list(Y.columns), {c: P for c in Y.columns if c != "yil"})
    # --- saglamlik: belirsiz P1 haric ; VIOP'lu ; t0 kilitsiz
    ev_bel = ev[ev.p1_belirsiz].index
    rows = []
    for nm, mask in [("tum", C.i.notna()), ("P1 belirsiz haric", ~C.i.isin(ev_bel)), ("VIOP'lu hisseler", C.kod.isin(VIOP)), ("VIOP'suz", ~C.kod.isin(VIOP))]:
        for (a, w) in key + [("p1", "[-20,-1]"), ("p3", "[1,5]"), ("hak", "[0,0]")]:
            g = C[mask & (C.asama == a) & (C.pencere == w)]
            z = E.ozet(g.car, g.t0); rows.append(dict(alt=nm, asama=a, pencere=w, N=z["N"], ort=z["ort"], med=z["med"], t=z["t"], isabet=z["isabet"]))
    R = pd.DataFrame(rows)
    s += "\n## Saglamlik alt kumeleri\n\n" + md(R, list(R.columns), F)
    # --- alternatif kiyas: BIST 100 disi (XYUZO) ve XUTUM endeksleri
    rows = []
    for ix in ["XUTUM", "XYUZO"]:
        xr = pd.read_parquet(f"{E.CACHE}/px_chart/{ix}.parquet").px.reindex(M["cal"]).pct_change()
        M2 = dict(M); M2["rm"] = xr
        for (a, w0, w1) in [("p1", -20, -1), ("p1", 0, 1), ("p1", 1, 20), ("p3", 0, 1), ("p3", 1, 5), ("hak", -5, -1), ("hak", 1, 10), ("hak", 1, 20)]:
            vals, dates = [], []
            for _, h in H.iterrows():
                j0 = h["j_" + a]
                if j0 is None or pd.isna(j0): continue
                vals.append(E.car(M2, h.kod, int(j0), w0, w1)); dates.append(M["cal"][int(j0)])
            z = E.ozet(pd.Series(vals), pd.Series(dates)); rows.append(dict(kiyas=ix, asama=a, pencere=f"[{w0},{w1}]", N=z["N"], ort=z["ort"], med=z["med"], t=z["t"], isabet=z["isabet"]))
    s += "\n## Alternatif kiyas endeksi (XUTUM, XYUZO=BIST 100 disi)\n\n" + md(pd.DataFrame(rows), ["kiyas", "asama", "pencere", "N", "ort", "med", "t", "isabet"], F)
    # --- kilit istatistikleri
    k = C[C.pencere.isin(["[0,0]"])].groupby("asama").t0_tavan.mean()
    s += "\n## t0 gunu tavan kilitli olay payi\n\n" + ", ".join(f"{a}: {v:.0%}" for a, v in k.items()) + "\n"
    open(f"{OUT}/ek_tablolar.md", "w").write(s); print(s)
if __name__ == "__main__": main()
