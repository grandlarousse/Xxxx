"""s9: 11:00->kapanış kısa deseninin diğer endekslerde tekrarı (İş Yatırım saatlik + Yahoo açılış/kapanış)."""
import sys, os; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc
import importlib.util
spec = importlib.util.spec_from_file_location("s2", f"{bc.OUT}/s2_isy.py")
L=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s); L.append(s)
src = open(f"{bc.OUT}/s2_isy.py").read().split("for code, ysym in")[0]
ns = {}; exec(src, ns); build = ns["build"]
for code in ["XU030","XU100","XBANK","XUSIN","XLBNK","XHOLD","X10XB","XUTUM","XYUZO"]:
    if not os.path.exists(f"{bc.D}/daily/{code}.IS.parquet") or not os.path.exists(f"{bc.D}/isy/h1/{code}.parquet"): P(code,"veri yok"); continue
    o = build(code, code+".IS"); o = o[o.first_h==11.0]
    r = -np.log(o.c/o.p11); a = -o.intra; f = -np.log(o.p11/o.o)
    yrs = r.groupby(r.index.year).mean()
    P(f"{code}: n={len(o)} {o.index.min().date()}.. | aç-sat {bc.st(a)['mean']:.1f} (t {bc.st(a)['t']:.1f}) | ilk saat kısa {bc.st(f)['mean']:.1f} (t {bc.st(f)['t']:.1f}) | 11->K kısa {bc.st(r)['mean']:.1f} (t {bc.st(r)['t']:.1f}); "
      f"IS<=2020 {bc.st(r.loc[:'2020'])['mean']:.1f} OOS {bc.st(r.loc['2021':])['mean']:.1f} (t {bc.st(r.loc['2021':])['t']:.1f}); pozitif yıl {int((yrs>0).sum())}/{len(yrs)}")
open(f"{bc.RES}/s9_other_idx.log","w").write("\n".join(L))
