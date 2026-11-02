"""2b) Düğüm-sayısı artefaktına karşı sağlamlık + kriz dinamiği:
S1 = XU100 + 10 sürücü (11 düğüm), S2 = 12 sektör portföyü (VİOP hisselerinden EW) + 10 sürücü (22 düğüm).
Kayan pencereler 60/120 gün (S1) ve 120 gün (S2); A/B hizalama; C (15:00 UTC anlık) 2024-06+ statik.
"""
import numpy as np, pandas as pd, time
from common import *
from dy import DRV, SHORT, matrix, fit_window, summarize, gfevd, var_fit
SECP = {"BANKA": ["AKBNK", "GARAN", "HALKB", "ISCTR", "VAKBN", "YKBNK", "TSKB"], "HOLDING": ["KCHOL", "SAHOL", "DOHOL", "ALARK"],
        "HAVACILIK": ["THYAO", "PGSUS", "TAVHL"], "OTOMOTIV": ["FROTO", "TOASO", "DOAS"], "CELIK": ["EREGL", "KRDMD", "BRSAN"],
        "ALTIN": ["TRALT", "TRMET"], "PERAKENDE_GIDA": ["BIMAS", "MGROS", "SOKM", "AEFES", "ULKER"], "ENERJI": ["AKSEN", "ENJSA", "ODAS", "ASTOR"],
        "PETRO_KIMYA": ["TUPRS", "PETKM", "SASA", "GUBRF", "HEKTS"], "TELEKOM": ["TCELL", "TTKOM"],
        "SANAYI": ["SISE", "ARCLK", "VESTL", "ASELS", "CIMSA", "OYAKC"], "INSAAT_GYO": ["ENKAI", "TKFEN", "EKGYO"]}
GLOB = ["ES", "EEM", "SX5E", "VIX", "DXY", "BRENT", "ALTIN_F", "US10Y"]

def s2_matrix(align):
    M = matrix(STOCKS, align=align); out = pd.DataFrame(index=M.index)
    for k, v in SECP.items(): out["P_" + k] = M[v].mean(axis=1)
    for d in DRV: out[SHORT[d]] = M[SHORT[d]]
    return out

def roll(M, w, step, label):
    rows = []
    for e in range(w, len(M) + 1, step):
        W = M.iloc[e - w:e]; th, names = fit_window(W)
        tot, tab = summarize(th, names)
        bist = [i for i, n in enumerate(names) if n.startswith("P_") or n == "XU100"]
        glob = [i for i, n in enumerate(names) if n in ("ES", "EEM", "SX5E", "VIX", "DXY", "BRENT", "ALTIN", "US10Y")]
        trm = [i for i, n in enumerate(names) if n in ("USDTRY", "TUR")]
        r = {"date": M.index[e - 1], "label": label, "total": 100 * tot,
             "bist_from_glob": 100 * th[np.ix_(bist, glob)].sum(1).mean(), "bist_from_tr": 100 * th[np.ix_(bist, trm)].sum(1).mean(),
             "glob_from_bist": 100 * th[np.ix_(glob, bist)].sum(1).mean(), "tr_from_bist": 100 * th[np.ix_(trm, bist)].sum(1).mean(),
             "bist_own_block": 100 * th[np.ix_(bist, bist)].sum(1).mean()}
        for n in names: r["net_" + n] = 100 * tab.loc[n, "net"]
        rows.append(r)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    t0 = time.time(); out = []
    for al in ["A", "B"]:
        M = matrix([], align=al)[["XU100"] + [SHORT[d] for d in DRV]]; M = M[M.index >= START]
        out.append(roll(M, 60, 5, f"S1_w60_{al}")); out.append(roll(M, 120, 5, f"S1_w120_{al}")); out.append(roll(M, 250, 5, f"S1_w250_{al}"))
        M2 = s2_matrix(al); M2 = M2[M2.index >= START]
        out.append(roll(M2, 120, 5, f"S2_w120_{al}")); out.append(roll(M2, 250, 5, f"S2_w250_{al}"))
        print(al, round(time.time() - t0), flush=True)
    R = pd.concat(out); R.to_csv(os.path.join(CACHE, "dy2_rolling.csv"), index=False)
    # statik: S1 ve S2, dönemler; A/B ve C (2024-06+, EEM/TUR hariç)
    st = []
    for al in ["A", "B"]:
        M = matrix([], align=al)[["XU100"] + [SHORT[d] for d in DRV]]; M2 = s2_matrix(al)
        for pn, (a, b) in list(PERIODS.items()) + [("fonkrizi", ("2026-09-01", "2026-10-30")), ("2026oca-agu", ("2026-01-01", "2026-08-31"))]:
            for nm, MM in [("S1", M), ("S2", M2)]:
                W = MM[(MM.index >= a) & (MM.index <= b)]
                if nm == "S2" and len(W) < 120: continue
                th, names = fit_window(W); tot, tab = summarize(th, names)
                for i, n in enumerate(names):
                    st.append({"net": nm, "align": al, "period": pn, "node": n, "to": tab.loc[n, "to"], "from": tab.loc[n, "from"], "netsp": tab.loc[n, "net"], "total": 100 * tot,
                               **({"xu_to_node": th[i, names.index("XU100")], "node_to_xu": th[names.index("XU100"), i]} if "XU100" in names else {})})
    drvC = ["ES=F", "^STOXX50E", "^VIX", "DX-Y.NYB", "BZ=F", "GC=F", "^TNX", "TRY=X"]
    for al in ["A", "B", "C"]:
        M = matrix([], drivers=drvC, align=al)[["XU100"] + [SHORT[d] for d in drvC]]
        W = M[(M.index >= "2024-06-12") & (M.index <= "2026-10-30")]
        th, names = fit_window(W); tot, tab = summarize(th, names)
        for i, n in enumerate(names):
            st.append({"net": "S1C", "align": al, "period": "2024-06..2026-10", "node": n, "to": tab.loc[n, "to"], "from": tab.loc[n, "from"], "netsp": tab.loc[n, "net"], "total": 100 * tot,
                       "xu_to_node": th[i, names.index("XU100")], "node_to_xu": th[names.index("XU100"), i]})
    pd.DataFrame(st).to_csv(os.path.join(CACHE, "dy2_static.csv"), index=False)
    print("done", round(time.time() - t0))
