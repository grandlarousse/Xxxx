import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal")
import vlib as V
cal = V.cal()
def windows(dr):
    """BIST günü t için: post = sürücü 15:00(t-1)->21:00(t-1) ; night = 21:00(t-1)->06:00(t) ; pre5 = 06:00->07:00(t); on07 = 15:00(t-1)->07:00(t); on06 = 15:00(t-1)->06:00(t);
    sess = 07:00(t)->15:00(t)."""
    s15 = V.snap(dr, "15:00"); s21 = V.snap(dr, "21:00"); s06 = V.snap(dr, "06:00"); s07 = V.snap(dr, "07:00")
    d = pd.DataFrame({"p15": s15, "p21": s21, "p06": s06, "p07": s07})
    # her BIST günü t için önceki BIST günü (t-1)
    c = cal[cal >= d.index[0]]
    prev = pd.Series(c[:-1], index=c[1:])
    D = pd.DataFrame(index=c[1:])
    g = lambda col, idx: d[col].reindex(idx).values
    D["p15_prev"] = g("p15", prev.values); D["p21_prev"] = g("p21", prev.values)
    D["p06"] = g("p06", D.index); D["p07"] = g("p07", D.index); D["p15"] = g("p15", D.index)
    W = pd.DataFrame(index=D.index)
    W["post"] = np.log(D.p21_prev / D.p15_prev); W["night"] = np.log(D.p06 / D.p21_prev); W["pre"] = np.log(D.p07 / D.p06)
    W["on06"] = np.log(D.p06 / D.p15_prev); W["on07"] = np.log(D.p07 / D.p15_prev); W["sess"] = np.log(D.p15 / D.p07)
    return W
