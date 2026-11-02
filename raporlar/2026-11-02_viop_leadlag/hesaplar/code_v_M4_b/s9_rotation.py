"""s9: Celik kompoziti 'Asya dongusel-defansif rotasyonu' veya genis piyasa vekili mi? intra ~ celik_z + defansif_z + genis_z (NW t)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
st, _ = vb.comp(vb.JP_AU); de, _ = vb.comp(["2502.T", "2503.T", "9432.T", "9501.T", "015760.KS"]); br, _ = vb.comp(["^N225", "^KS11", "^AXJO"])
dj, _ = vb.comp(["005490.KS", "004020.KS", "RIO.AX", "CIA.AX", "MIN.AX"])
X = pd.DataFrame({"comp": st, "defansif": de, "genis": br})
X2 = pd.DataFrame({"comp": dj, "defansif": de, "genis": br})
rows = []
for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
    y = vb.bist(s).intra
    for lab, XX in [("JP_AU", X), ("ayrik_celik", X2)]:
        for per, a, e in [("ALL", "2014", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027"), ("2024-26", "2024", "2027")]:
            m = (XX.index >= a) & (XX.index < e)
            res, n = vb.nwreg(y, XX[m])
            rows.append(dict(stock=s, basket=lab, period=per, t_celik=res.loc["comp", "t"], t_def=res.loc["defansif", "t"], t_genis=res.loc["genis", "t"], b_celik_bps=1e4 * res.loc["comp", "b"], n=n))
R = pd.DataFrame(rows); R.to_csv(os.path.join(vb.OUT, "res_s9_rotation.csv"), index=False)
print(R.round(2).to_string())
print("corr(celik, defansif)", round(st.corr(de), 3), "corr(celik, genis)", round(st.corr(br), 3))
