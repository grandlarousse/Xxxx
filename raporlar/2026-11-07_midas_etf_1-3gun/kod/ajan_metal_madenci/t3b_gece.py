"""H05 (MM01): gece (C_t-1 -> O_t) ve gün içi (O_t -> C_t) getiri ayrışması; C0 ile O1 girişinin farkı.
Uyarı: resmî açılış fiyatı (ilk işlem) gerçek dolum fiyatını iyimser gösterebilir (Quantpedia GDX notu).
Çalıştır: python3 -I kod/ajan_metal_madenci/t3b_gece.py
Çıktı: sonuclar/aile_metal_madenci/gece_gunici.csv, gece_gunici_yillik.csv, testler_t3b.csv"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mm, lib

def main():
    reg = mm.Registry("t3b")
    rows, yrows = [], []
    for s in mm.REP17 + ["IAU", "GLDM", "SIVR", "SPY"]:
        df = mm.load(s)
        on = np.log(df["o"] / df["c"].shift(1)).dropna()
        idy = np.log(df["c"] / df["o"]).dropna()
        on = on.iloc[1:]; idy = idy.loc[on.index]
        r = {"sym": s, "n": len(on)}
        for nm, x in (("gece", on), ("gunici", idy)):
            t = x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))
            r[f"{nm}_bp_gun"] = x.mean() * 1e4; r[f"{nm}_yillik_pct"] = x.mean() * 252 * 100; r[f"{nm}_t"] = t
            for per, m in (("is", x.index <= lib.IS_END), ("oos", x.index > lib.IS_END)):
                y = x[m]; r[f"{nm}_{per}_bp"] = y.mean() * 1e4
                r[f"{nm}_{per}_t"] = y.mean() / (y.std(ddof=1) / math.sqrt(len(y)))
            yr = x.groupby(x.index.year).sum()
            r[f"{nm}_yil_pozitif"] = float((yr > 0).mean())
            reg.add(f"MM01_{nm}_ortalama", s, "-", 1, len(x), t, x.mean() * 1e4)
        # "kapanışta al, ertesi açılışta sat" her gün: brüt gece - maliyet
        r["gece_islem_net_bp"] = r["gece_bp_gun"] - mm.cost(df)
        rows.append(r)
        if s in ("GLD", "SLV", "GDX", "GDXJ", "SIL"):
            yy = pd.DataFrame({"gece_pct": on.groupby(on.index.year).sum() * 100, "gunici_pct": idy.groupby(idy.index.year).sum() * 100})
            yy["sym"] = s; yrows.append(yy.reset_index().rename(columns={"date": "yil"}))
    R = pd.DataFrame(rows); R.to_csv(os.path.join(mm.OUTD, "gece_gunici.csv"), index=False)
    Y = pd.concat(yrows); Y.to_csv(os.path.join(mm.OUTD, "gece_gunici_yillik.csv"), index=False)
    reg.save()
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40)
    print(R[["sym", "n", "gece_bp_gun", "gece_t", "gece_is_t", "gece_oos_t", "gece_yillik_pct", "gunici_bp_gun", "gunici_t", "gunici_is_t",
             "gunici_oos_t", "gunici_yillik_pct", "gece_yil_pozitif", "gunici_yil_pozitif", "gece_islem_net_bp"]].round(2).to_string(index=False))
    print(Y.round(1).to_string(index=False))

if __name__ == "__main__":
    main()
