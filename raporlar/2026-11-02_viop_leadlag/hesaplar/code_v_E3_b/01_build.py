"""01: Ana veri çerçevesi + temel yeniden üretim."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
import vb, numpy as np, pandas as pd
cal = vb.bist_cal("2013-01-01")
tu = vb.bist_dec("TUPRS.IS", cal); xu = vb.bist_dec("XU100.IS", cal)
F = pd.DataFrame(index=cal)
F["y_raw"] = tu.intra; F["y_h"] = tu.intra - xu.intra; F["tu_gap"] = tu.gap; F["xu_gap"] = xu.gap
F["tu_cc"] = tu.cc; F["xu_cc"] = xu.cc; F["xu_intra"] = xu.intra; F["tu_cc_l1"] = tu.cc.shift(1); F["xu_cc_l1"] = xu.cc.shift(1)
F["tu_intra_l1"] = tu.intra.shift(1); F["tu_gap_l1"] = tu.gap.shift(1); F["y_h_l1"] = F.y_h.shift(1)
F["tu_o_eq_pc"] = tu.o_eq_pc; F["xu_o_eq_pc"] = xu.o_eq_pc
F["xkmya_cc_l1"] = np.log(vb.isy_close("XKMYA", cal)).diff().shift(1)
for b in ["XUSIN.IS", "XU030.IS", "AYGAZ.IS", "PETKM.IS", "XBANK.IS"]:
    d = vb.bist_dec(b, cal); k = b.split(".")[0].lower()
    F[k + "_cc_l1"] = d.cc.shift(1); F[k + "_intra"] = d.intra; F[k + "_gap"] = d.gap
US = ["VLO", "MPC", "PSX", "PBF", "DINO", "DK", "CVI", "PARR", "CLMT", "CRAK", "XLE", "XOP", "VDE", "IXC", "SPY", "EEM", "TUR", "XOM", "CVX", "COP", "SHEL", "BP"]
FUT = ["ES=F", "BZ=F", "CL=F", "HO=F", "RB=F", "NG=F", "GC=F", "^VIX"]
for s in US + FUT:
    try:
        fld = "adj" if s in US else "c"
        F["A_" + s] = vb.sig(s, cal, "A", fld); F["C_" + s] = vb.sig(s, cal, "C", fld)
    except FileNotFoundError:
        print("yok", s)
F["FX_TRY"] = vb.sig("TRY=X", cal, "A", "c")
F["A_USREF"] = F[["A_VLO", "A_MPC", "A_PSX", "A_PBF"]].mean(axis=1)
F["C_USREF"] = F[["C_VLO", "C_MPC", "C_PSX", "C_PBF"]].mean(axis=1)
F["A_USREF6"] = F[["A_VLO", "A_MPC", "A_PSX", "A_PBF", "A_DINO", "A_DK"]].mean(axis=1)
F["A_OUT"] = F[["A_DINO", "A_DK", "A_CVI", "A_PARR"]].mean(axis=1)   # sepet DIŞI ABD rafinerileri
F["C_OUT"] = F[["C_DINO", "C_DK", "C_CVI", "C_PARR"]].mean(axis=1)
F.to_parquet(vb.RES + "/F.parquet")
G = F[F.index >= "2014-01-01"]
print("n gün", len(G), "y_h n", G.y_h.notna().sum(), "y_raw n", G.y_raw.notna().sum())
print("o==prev c oranı TUPRS / XU100 yıllık:"); print(G.groupby(G.index.year)[["tu_o_eq_pc", "xu_o_eq_pc"]].mean().round(3).T.to_string())
def per(m): return {"ALL": m.index >= "1900", "IS": m.index < vb.SPLIT, "OOS": m.index >= vb.SPLIT}
rows = []
for y in ["y_h", "y_raw"]:
    for sg in ["A_USREF", "C_USREF", "A_VLO", "C_VLO", "A_OUT", "A_USREF6"]:
        for pk, m in per(G).items():
            g = G[m]
            p, t, n = vb.nw(g[y], g[[sg]]); rows.append(dict(y=y, sig=sg, ctrl="yok", per=pk, b=p[sg], t=t[sg], n=n))
            if sg in ("A_USREF", "C_USREF"):
                cs = [sg, "A_ES=F", "A_BZ=F"] if sg.startswith("A") else [sg, "C_ES=F", "C_BZ=F"]
                p, t, n = vb.nw(g[y], g[cs]); rows.append(dict(y=y, sig=sg, ctrl="ES+BZ", per=pk, b=p[sg], t=t[sg], n=n))
R = pd.DataFrame(rows); R.to_csv(vb.RES + "/01_base.csv", index=False)
pd.set_option("display.width", 200)
print(R.pivot_table(index=["y", "sig", "ctrl"], columns="per", values="t").round(2)[["ALL", "IS", "OOS"]].to_string())
