"""(A) Olay calismasi: BHAR (hisse BH - XU100 BH) ve piyasa modeli CAR, 5/20/60 gun; giris = olay gunu kapanisi.
Tarih kumesi = giris haftasi (W-FRI). Tavan kilitli girisler (gun0 >= %9.5 ve kapanis = gun ici en yuksek) ayri raporlanir.
Maliyet: 25 bp gidis-donus (net = BHAR - 0.25%)."""
import numpy as np, pandas as pd
import ortak as O
E = pd.read_pickle(O.MY + "/olaylar_A.pkl")
xu = O.endeks("XU100")
rows = []
for r in E.itertuples():
    o = O.olay_getiri(r.kod, pd.Timestamp(r.t0), xu, None)
    if o is None: continue
    o.update(olay=r.olay, viop=r.viop, t=r.t); rows.append(o)
R = pd.DataFrame(rows)
R["hafta"] = R.t0.dt.to_period("W-FRI").astype(str); R["yil"] = R.t0.dt.year
R["donem"] = np.where(R.t0 >= "2024-01-01", "2024-26", "2018-23")
liq = R.groupby("olay").vol20.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["dusuk", "orta", "yuksek"]))
R["likidite"] = liq.astype(str)
R.to_pickle(O.MY + "/A_sonuc.pkl")
C = ["on", "gun0", "ar5", "ar20", "ar60", "mm5", "mm20", "mm60", "bh20", "bh60"]
out = []
def bas(t): out.append("\n### " + t + "\n")
for ol in ["GA_YENI", "GA_PROG", "GA_ISLEM", "PAS_ALIS", "PAS_ALIS_KUME", "PAS_SATIS", "PAS_HEPSI"]:
    d = R[R.olay == ol]
    bas(f"{ol}: n={len(d)}, hisse={d.kod.nunique()}, hafta-kume={d.hafta.nunique()}, tavan-kilitli giris={int(d.tavan.sum())}")
    out.append(O.md(O.tablo(d, C).round(2)))
    df = d[~d.tavan]
    bas(f"{ol} | tavan kilitli girisler HARIC (n={len(df)}) | net = AR - 0.25")
    t = O.tablo(df.assign(net20=df.ar20 - .0025, net60=df.ar60 - .0025), ["ar5", "ar20", "ar60", "net20", "net60", "mm20", "mm60"]).round(2)
    out.append(O.md(t))
    for by in ["viop", "donem", "likidite", "yil"]:
        rr = []
        for k, g in df.groupby(by):
            s5 = O.ozet(g, "ar5"); s20 = O.ozet(g, "ar20"); s60 = O.ozet(g, "ar60")
            rr.append({by: k, "n": s20.get("n"), "ar5%": s5.get("ort%"), "ar20%": s20.get("ort%"), "t20": s20.get("t_kume"), "med20%": s20.get("medyan%"),
                       "isabet20%": s20.get("isabet%"), "ar60%": s60.get("ort%"), "t60": s60.get("t_kume"), "med60%": s60.get("medyan%")})
        out.append(f"\n{ol} — {by} kirilimi\n\n" + O.md(pd.DataFrame(rr).set_index(by).round(2)))
open(O.OUTD + "/A_tablolar.md", "w").write("\n".join(out))
print("\n".join(out)[:20000])
