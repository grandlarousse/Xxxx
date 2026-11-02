"""S5: uzlaştırma — IS tanımı (2010–2020 vs 2014–2020), CRAK ex-TUPRS yıl işareti, M5 son dönem, XMANA/XULAS (h1'den günlük, 2023-12+) mekanik içerme kontrolü."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal")
import vlib as V
RES = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal/res"
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
R = {}
def r(s):
    if s not in R: R[s] = V.ret(s)
    return R[s]
xu = r("XU100.IS")
P("== IS 2010–2020 tanımıyla (ajan IS'si) pc|XU100")
for st, dr in [("THYAO.IS", "LHA.DE"), ("THYAO.IS", "EZJ.L"), ("THYAO.IS", "IAG.L"), ("PGSUS.IS", "EZJ.L"), ("TAVHL.IS", "ADP.PA"), ("TUPRS.IS", "BZ=F"), ("TUPRS.IS", "CRAK"), ("EREGL.IS", "ISDMR.IS"), ("EREGL.IS", "KRDMD.IS"), ("TRALT.IS", "GC=F")]:
    P(f"  {st}~{dr}: IS10-20={V.pcorr(r(st), r(dr), [xu], '2010-01-01', '2020-12-31')[0]:.3f}")
tu = r("TUPRS.IS"); cx = (r("CRAK") - 0.04 * (tu - r("TRY=X"))) / 0.96
y = V.byyear(tu, cx, [xu]); P(f"== CRAK ex-TUPRS (w=0,04) yıllık pc|XU100: {y.round(2).to_dict()} -> pozitif {int((y>0).sum())}/{len(y)}")
eu = pd.concat([r(x) for x in ["MT.AS", "SSAB-A.ST", "VOE.VI", "SZG.DE"]], axis=1).mean(axis=1, skipna=False)
e = r("EREGL.IS"); x = pd.concat([e.rename("a"), eu.rename("b"), xu.rename("c")], axis=1).dropna(); x = x[x.index >= "2023-01-01"]
g = x.groupby([x.index.year, (x.index.month - 1) // 6]).apply(lambda q: V.pcorr(q.a, q.b, [q.c])[0])
P(f"== M5 EREGL~AB çelik(4) yarıyıllık pc|XU100 2023+: {g.round(3).to_dict()}")
yy = V.byyear(e, eu, [xu]); P(f"   yıllık: {yy.round(2).to_dict()}")
# h1'den XMANA / XULAS günlük kapanışları (Yahoo günlük verisi yok) — 2023-12+ kısa örneklem
def h1r(sym): return np.log(V.h1_daily_close(sym)).diff()
xm, xl, xui = h1r("XMANA.IS"), h1r("XULAS.IS"), h1r("XUSIN.IS")
for st, dr, sec in [("EREGL.IS", "ISDMR.IS", xm), ("EREGL.IS", "KRDMD.IS", xm), ("THYAO.IS", "PGSUS.IS", xl)]:
    a, b = r(st), r(dr)
    p1 = V.pcorr(a, b, [xu], "2023-12-01"); p2 = V.pcorr(a, b, [xu, sec], "2023-12-01"); p3 = V.pcorr(a, b, [xu, xui], "2023-12-01")
    P(f"  {st}~{dr} 2023-12+: pc|XU100={p1[0]:.3f} (n{p1[1]}) | +sektör endeksi (h1, hisseyi İÇERİR)={p2[0]:.3f} | +XUSIN={p3[0]:.3f}")
open(f"{RES}/s5_reconcile.txt", "w").write("\n".join(out))
