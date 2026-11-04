"""Sinyal üreticileri (c1/c2 ile aynı tanım)."""
import numpy as np, pandas as pd, cl
def _res(mem, mkt):
    rm = cl.lret(mkt, "adj"); out = []
    for m in mem:
        r = cl.lret(m, "adj"); b = cl.roll_beta(r, rm.reindex(r.index), 250, 100); out.append(r - b * rm.reindex(r.index))
    return pd.concat(out, axis=1)
def z_ref(c=None):
    df = _res(["VLO", "MPC", "PSX", "PBF"], "^GSPC"); P = df.mean(axis=1).where(df.notna().sum(axis=1) >= 3)
    return cl.zscale(cl.to_bist(P, "after", c), 250, 100)
def z_asx(c=None):
    df = _res(["FMG.AX", "BHP.AX"], "^AXJO"); P = df.mean(axis=1).where(df.notna().sum(axis=1) >= 2)
    return cl.zscale(cl.to_bist(P, "before", c), 250, 100)
