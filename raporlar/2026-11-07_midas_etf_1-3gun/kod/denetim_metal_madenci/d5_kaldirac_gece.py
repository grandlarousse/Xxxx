"""D5: Kaldıraçlı uygulama (S3->JNUG, S1->NUGT) ve gece/gün içi iddiasının bağımsız kontrolü.
Çalıştır: python3 -I kod/denetim_metal_madenci/d5_kaldirac_gece.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M
from d1_yeniden import ibs_sig, month_end

def warm(s, w=200):
    s = s.copy(); s.iloc[:w] = False; return s

rows = []
for tag, base, lev, f in (("S3", "GDXJ", "JNUG", ibs_sig), ("S1", "GDX", "NUGT", month_end)):
    b = M.px(base); L = M.px(lev); s = warm(f(b)).reindex(L.index).fillna(False)
    for per, m in (("tüm", slice(None)), ("2x dönem (2020-04+)", L.index >= "2020-04-01")):
        ss = s.copy(); ss[~pd.Series(L.index >= "2020-04-01", index=L.index)] = False if per != "tüm" else ss[~pd.Series(L.index >= "2020-04-01", index=L.index)]
        tr = M.sim(L, ss, 3, "C0", M.cost_static(L)); r = M.summ(tr, f"{tag}->{lev} {per}")
        print(f"{r['label']}: n={r['n']} net={r['net_bp']:.0f} t={r['t']:.2f} IS={r['is_net_bp']:.0f} OOS={r['oos_net_bp']:.0f} maxDD={r['maxdd']:.2f} enkötü={r['worst_bp']:.0f}")
        rows.append(r)
for sym in ("GLD", "SLV", "GDX", "GDXJ"):
    d = M.px(sym); on = (d["o"] / d["c"].shift(1) - 1).dropna(); idr = (d["c"] / d["o"] - 1).dropna()
    print(f"{sym}: gece {on.mean()*1e4:.1f} bp (t {M.tstat(on):.2f}) | gün içi {idr.mean()*1e4:.1f} bp (t {M.tstat(idr):.2f})")
    rows.append(dict(label=f"{sym} gece/gunici", gece_bp=on.mean() * 1e4, gece_t=M.tstat(on), gunici_bp=idr.mean() * 1e4, gunici_t=M.tstat(idr)))
pd.DataFrame(rows).to_csv(os.path.join(M.OUTD, "d5_kaldirac_gece.csv"), index=False)
