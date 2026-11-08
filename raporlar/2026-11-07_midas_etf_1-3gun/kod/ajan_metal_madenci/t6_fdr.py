"""Toplam test sayısı ve BH-FDR (q=0.10).
Kapsam: (i) genel_tum.csv'nin aile satırları (28 ETF x 31 sinyal x mod x h [+erken çıkış]) — incelendiği için test sayılır,
(ii) t2 aile havuz testleri, (iii) t3 hipotez testleri, (iv) t3b gece/gün içi, (v) t4 lead-lag ek testleri.
İki sürüm: iki yönlü p (lib.t_to_p) ve tek yönlü p (H1: net > 0). Maliyet nedeniyle anlamlı NEGATİF çıkan çok sayıda test
iki yönlü BH eşiğini gevşetir; tek yönlü sürüm 'işe yarar mı?' sorusu için daha uygundur.
Çalıştır: python3 -I kod/ajan_metal_madenci/t6_fdr.py   (önce t2, t3, t3b, t4 çalışmış olmalı)
Çıktı: sonuclar/aile_metal_madenci/fdr_tum_testler.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats as st
import mm, lib

CAND = [("genel_MR_ibs_lt01_dusus_sabit", "GDXJ", "C0", 3), ("genel_CA_ay_sonu_sabit", "GDX", "C0", 3),
        ("genel_CA_ay_sonu_sabit", "GLD", "C0", 3), ("genel_MR_bb20_alt_sabit", "SILJ", "C1", 3),
        ("H03_ibs01_dusus_havuz", "MADENCI5", "C0", 3), ("H01_ay_sonu_havuz", "MADENCI5", "C0", 3),
        ("H01_ay_sonu_havuz", "REP12", "C0", 3), ("havuz_CA_ay_sonu_sabit", "REP12", "C0", 3)]

def main():
    g = pd.read_csv(os.path.join(mm.ROOT, "sonuclar", "genel_tum.csv"))
    g = g[g.sym.isin(mm.FAM)]
    G = pd.DataFrame({"betik": "genel_tum", "test": "genel_" + g.sig + "_" + g["exit"], "sym": g.sym, "mode": g["mode"], "h": g.h,
                      "n": g.n, "t": g.t, "net_bp": g.mean_net_bp})
    parts = [G]
    for nm in ("t2", "t3", "t3b", "t4", "t4b", "t4c"):
        p = os.path.join(mm.OUTD, f"testler_{nm}.csv")
        if os.path.exists(p): parts.append(pd.read_csv(p))
    A = pd.concat(parts, ignore_index=True)
    A = A[np.isfinite(A.t) & (A.n >= 3)].copy()
    A["p2"] = 2 * st.t.sf(A.t.abs(), A.n - 1)
    A["p1"] = st.t.sf(A.t, A.n - 1)          # tek yönlü, H1: ortalama > 0
    A["fdr2"] = lib.bh_fdr(A.p2.values, 0.10)
    A["fdr1"] = lib.bh_fdr(A.p1.values, 0.10)
    A.to_csv(os.path.join(mm.OUTD, "fdr_tum_testler.csv"), index=False)
    print("toplam test:", len(A), "| betiklere göre:", A.groupby("betik").size().to_dict())
    print("iki yönlü BH geçen:", int(A.fdr2.sum()), "(pozitif t:", int((A.fdr2 & (A.t > 0)).sum()), ")")
    print("tek yönlü BH geçen (net>0):", int(A.fdr1.sum()))
    thr1 = A.loc[A.fdr1, "p1"].max() if A.fdr1.any() else np.nan
    print("tek yönlü BH eşiği (geçen en büyük p):", thr1)
    pd.set_option("display.width", 220); pd.set_option("display.max_rows", 100)
    print(A[A.fdr1 | (A.fdr2 & (A.t > 0))].sort_values("t", ascending=False)[["betik", "test", "sym", "mode", "h", "n", "t", "net_bp", "p1", "fdr1", "fdr2"]].to_string(index=False))
    print("\nAday durumları:")
    for tst, s, m, h in CAND:
        r = A[(A.test == tst) & (A.sym == s) & (A["mode"] == m) & (A.h == h)]
        if len(r):
            r = r.iloc[0]
            print(f"  {tst} {s} {m} h{h}: n={r.n} t={r.t:.2f} p1={r.p1:.4f} fdr1={r.fdr1} fdr2={r.fdr2}")

if __name__ == "__main__":
    main()
