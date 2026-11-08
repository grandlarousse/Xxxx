"""D6: S3 (IBS) ve S1 (ay sonu) kuralı ailede, kendi motorumla; madenci havuzu (aynı gün işlemler ortalanır, NW t).
Çalıştır: python3 -I kod/denetim_metal_madenci/d6_aile.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M
from d1_yeniden import ibs_sig, month_end

def warm(s, w=200):
    s = s.copy(); s.iloc[:w] = False; return s

def nw_mean_t(x, lags):
    x = np.asarray(x, float); n = len(x); e = x - x.mean(); s = e @ e / n
    for l in range(1, lags + 1): s += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / math.sqrt(s / n)

rows = []
FAM = ["GDX", "GDXJ", "RING", "SIL", "SILJ", "XME", "COPX", "GLD", "IAU", "GLDM", "SLV", "PPLT", "PALL", "URA", "REMX", "LIT", "CPER", "DBB"]
for tag, f in (("S3_IBS", ibs_sig), ("S1_aysonu", month_end)):
    txt = []; pool = []
    for s in FAM:
        drop = ("2021-03-08",) if s == "IAU" else ()
        d = M.px(s, drop); tr = M.sim(d, warm(f(d)), 3, "C0", M.cost_static(d)); r = M.summ(tr, f"{tag} {s}")
        rows.append(r); txt.append(f"{s}:{r['net_bp']:.0f}/t{r['t']:.2f}(IS {r['is_net_bp']:.0f})")
        if s in ("GDX", "GDXJ", "RING", "SIL", "SILJ"):
            tr["sym"] = s; pool.append(tr)
    print(tag, " ".join(txt))
    P = pd.concat(pool).groupby("sig")["net"].mean().sort_index()
    for nm, m in (("tüm", slice(None)), ("IS", P.index <= M.IS_END), ("OOS", P.index > M.IS_END)):
        x = P[m] if nm != "tüm" else P
        print(f"   madenci havuzu {nm}: olay n={len(x)} net={x.mean()*1e4:.0f} bp NW t={nw_mean_t(x.values, 3):.2f}")
        rows.append(dict(label=f"{tag} madenci havuzu {nm}", n=len(x), net_bp=x.mean() * 1e4, t=nw_mean_t(x.values, 3)))
pd.DataFrame(rows).to_csv(os.path.join(M.OUTD, "d6_aile.csv"), index=False)
