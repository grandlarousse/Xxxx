import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
cA, _ = vb.comp(vb.JP_AU)
# (e) genislik: ayni sinyal tum VIOP hisseleri + endeksler
import json
cat = pd.read_csv(os.path.join(vb.DATA, "catalog.csv"))
viop = cat[cat.group == "VIOP"].sym.tolist()
idx = ["XU100.IS", "XU030.IS", "XUSIN.IS", "XBANK.IS", "XMANA.IS", "XHOLD.IS", "XUMAL.IS", "XKMYA.IS", "XMADN.IS", "XTAST.IS", "XUHIZ.IS", "XGIDA.IS", "ISDMR.IS", "KRDMA.IS", "KRDMB.IS"]
br = []
for s in viop + idx:
    if not os.path.exists(os.path.join(vb.DATA, "daily", s + ".parquet")): continue
    try:
        b = vb.bist(s)
    except Exception as e:
        continue
    if b.intra.notna().sum() < 500: continue
    r = vb.isoos(vb.bt(cA, b.intra)); cr = vb.corr_t(cA, b.intra)
    cri = vb.corr_t(cA[cA.index < vb.SPLIT], b.intra); cro = vb.corr_t(cA[cA.index >= vb.SPLIT], b.intra)
    br.append(dict(sym=s, IS_bps=r["IS_bps"], IS_t=r["IS_t"], OOS_bps=r["OOS_bps"], OOS_t=r["OOS_t"], corr=cr[0], corr_t=cr[1], corr_IS_t=cri[1], corr_OOS_t=cro[1], n=cr[2]))
BR = pd.DataFrame(br).sort_values("corr_t", ascending=False); BR.to_csv(os.path.join(vb.OUT, "res_s3_breadth.csv"), index=False)
print(BR.round(2).to_string())
