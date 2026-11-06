"""Hizli bakis: bedelli (ruchan hakli) sermaye artirimi ve nakit temettu duyurulari. Ayni motor (XU100'e gore AR, tarih kumelenmis t).
Bedelli: P1 = ilk 'bedelli/rüçhan/nakden' KAP bildirimi (yalniz ozet), hak = ruchan hakki kullanim baslangici (Is Yatirim).
Temettu: P1 = ilk 'Kar Payi Dagitimi' KAP bildirimi (hak gunu oncesi <=200 gun), hak = temettu hak gunu; verim = 1 - Is Yatirim fiyat ayar orani."""
import os, numpy as np, pandas as pd
import f20_es as E
from f31_calistir import md, P2, T, I, H as HP
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonuc")
COST = 0.0025
W1 = [(-20, -1), (-5, -1), (0, 0), (0, 1), (1, 5), (1, 10), (1, 20)]
W2 = [(-10, -1), (-1, -1), (0, 0), (1, 5), (1, 10), (1, 20)]
def calis(M, ev, grpcol=None):
    cal = M["cal"]; rec = []
    for _, e in ev.iterrows():
        k = e.kod
        if k not in M["R"].columns: continue
        for s, W in [("p1", W1), ("hak", W2)]:
            j0 = E.t0_idx(cal, e.p1) if s == "p1" else E.day_idx(cal, e.hak)
            if j0 is None or pd.isna(e[s]): continue
            if s == "p1" and E.day_idx(cal, e.hak) is not None and j0 >= E.day_idx(cal, e.hak): continue
            for a, b in W:
                rec.append(dict(kod=k, asama=s, pencere=f"[{a},{b}]", a=a, b=b, t0=cal[j0], car=E.car(M, k, j0, a, b),
                                grp=e[grpcol] if grpcol else "hepsi", yil=e.hak.year))
    C = pd.DataFrame(rec); out = []
    for kk, g in C.groupby(["asama", "pencere", "a", "b", "grp"], sort=False):
        z = E.ozet(g.car, g.t0); z.update(dict(zip(["asama", "pencere", "a", "b", "grp"], kk))); out.append(z)
    T_ = pd.DataFrame(out); T_["_o"] = T_.asama.map({"p1": 0, "hak": 1}); return C, T_.sort_values(["_o", "grp", "a", "b"]).drop(columns="_o")
if __name__ == "__main__":
    M = E.matrisler()
    bl = pd.read_pickle(f"{E.CACHE}/olaylar_bedelli.pkl"); bl = bl[bl.hak >= "2015-01-01"]
    bl["grp"] = np.where(bl.oran >= 100, "bedelli>=%100", "bedelli<%100")
    tm = pd.read_pickle(f"{E.CACHE}/olaylar_temettu.pkl"); tm = tm[(tm.hak >= "2015-01-01") & (tm.verim > 0) & (tm.verim < 0.5)]
    tm["grp"] = pd.cut(tm.verim, [0, 0.02, 0.05, 1], labels=["verim<%2", "%2-5", ">=%5"]).astype(str)
    s = "# Bedelli ve temettu (otomatik)\n"
    for ad, ev in [("bedelli", bl), ("temettu", tm)]:
        C1, T1 = calis(M, ev); C2, T2 = calis(M, ev, "grp")
        T1.to_csv(f"{OUT}/{ad}_car.csv", index=False); T2.to_csv(f"{OUT}/{ad}_car_grp.csv", index=False)
        F = dict(ort=P2, med=P2, t=T, isabet=HP, N=I, G=I, p5=P2, p95=P2)
        s += f"\n## {ad} (N olay={len(ev)})\n\n" + md(T1, ["asama", "pencere", "N", "ort", "med", "t", "isabet", "p5", "p95", "G"], F)
        s += f"\n### {ad} alt grup\n\n" + md(T2, ["asama", "pencere", "grp", "N", "ort", "med", "t", "isabet"], F)
        C1["donem"] = np.where(C1.yil >= 2024, "2024-26", "2015-23")
        out = []
        for kk, g in C1.groupby(["asama", "pencere", "donem"], sort=False):
            z = E.ozet(g.car, g.t0); z.update(dict(zip(["asama", "pencere", "donem"], kk))); out.append(z)
        s += f"\n### {ad} donem\n\n" + md(pd.DataFrame(out), ["asama", "pencere", "donem", "N", "ort", "med", "t", "isabet"], F)
    open(f"{OUT}/bedelli_temettu.md", "w").write(s); print(s)
