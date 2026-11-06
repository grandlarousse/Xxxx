"""Tum analizleri calistirir, tablolari sonuc/ altina yazar (csv + md)."""
import os, numpy as np, pandas as pd
import f20_es as E, f30_analiz as A
OUT = A.OUT
def md(df, cols, fmt=None, fname=None):
    fmt = fmt or {}
    d = df[cols].copy()
    for c in cols:
        if c in fmt: d[c] = d[c].map(lambda v: fmt[c](v) if pd.notna(v) else "")
    s = "| " + " | ".join(cols) + " |\n|" + "|".join(["---"] * len(cols)) + "|\n"
    for _, r in d.iterrows(): s += "| " + " | ".join(str(x) for x in r.values) + " |\n"
    return s
P = lambda v: f"{100*v:+.1f}%"; P2 = lambda v: f"{100*v:+.2f}%"; T = lambda v: f"{v:.2f}"; I = lambda v: f"{int(v)}"; H = lambda v: f"{100*v:.0f}%"
FMT = dict(ort=P2, med=P2, ort_mm=P2, med_mm=P2, ort_b=P2, t=T, isabet=H, p5=P, p95=P, N=I, G=I)
def main():
    M = E.matrisler()
    ev = pd.read_pickle(f"{E.CACHE}/olaylar_bedelsiz.pkl")
    ev = ev[(ev.hak >= "2015-01-01")].copy()                    # analiz donemi: hak gunu 2015-01-01 .. 2026-11-05
    # veri hatasi: hak gununde gozlenen duzeltme carpani teorikten >%5 sapan (duzeltilmemis/islem gormeyen pay gruplari, or. ISATR/ISBTR)
    dz = pd.read_csv(f"{E.CACHE}/dogrulama_duzeltme.csv", parse_dates=["hak"])
    dz["sapma"] = (dz.carpan / dz.teorik - 1).abs()
    bad = dz[(dz.sapma > 0.05) & (dz.bedelli.fillna(0) == 0)][["kod", "hak"]]
    n0 = len(ev); ev = ev.merge(bad.assign(_bad=1), on=["kod", "hak"], how="left"); ev = ev[ev._bad.isna()].drop(columns="_bad")
    print("veri hatasi nedeniyle dislanan:", n0 - len(ev), bad.kod.tolist())
    H = A.hazirla(M, ev); H.to_pickle(f"{OUT}/H.pkl")
    C = A.car_tablosu(M, H); C.to_pickle(f"{OUT}/C.pkl")
    C["oran_g"] = C.oran.map(A.oran_grup)
    q = C.drop_duplicates("i").pd_rel.quantile([1/3, 2/3]).values
    C["boy_g"] = pd.cut(C.pd_rel, [-np.inf, q[0], q[1], np.inf], labels=["kucuk", "orta", "buyuk"])
    C["donem"] = np.where(C.yil >= 2024, "2024-26", np.where(C.yil >= 2020, "2020-23", "2015-19"))
    C["kilit"] = np.where(C.t0_tavan, "t0 tavan kilitli", "t0 kilitsiz")
    res = {}
    res["genel"] = A.tablo(C)
    gb = C.groupby(["asama", "pencere"], sort=False).car_b.mean().rename("ort_b").reset_index()
    res["genel"] = res["genel"].merge(gb, on=["asama", "pencere"], how="left")
    for by in ["oran_g", "boy_g", "donem", "yil", "kilit"]:
        res[by] = A.tablo(C, by)
    for k, v in res.items(): v.to_csv(f"{OUT}/car_{k}.csv", index=False)
    return M, H, C, res
if __name__ == "__main__":
    M, H, C, res = main()
    s = "# CAR tablolari (otomatik)\n\n## Genel\n\n" + md(res["genel"], ["asama", "pencere", "N", "ort", "med", "t", "isabet", "p5", "p95", "ort_b", "ort_mm", "G"], FMT)
    for by in ["oran_g", "boy_g", "donem", "kilit"]:
        s += f"\n## {by}\n\n" + md(res[by], ["asama", "pencere", by, "N", "ort", "med", "t", "isabet"], FMT)
    open(f"{OUT}/car_tablolar.md", "w").write(s); print(s[:3000])
