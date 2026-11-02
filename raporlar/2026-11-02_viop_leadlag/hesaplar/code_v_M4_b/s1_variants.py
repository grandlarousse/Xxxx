"""s1: Kurgu/parametre varyantlari -> OOS duyarliligi (veri madenciligi kirilganligi). Cikti res_s1_variants.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
T = {s: vb.bist(s) for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]}
T2 = {s: vb.bist(s, lim="regime") for s in ["EREGL.IS", "KRDMD.IS"]}
rows = []
cA, _ = vb.comp(vb.JP_AU); cB, _ = vb.comp_ffill(vb.JP_AU); cC, ZC = vb.comp(vb.JP_AU, minc=3)
def add(name, sig, tgt, **kw):
    for s, b in tgt.items():
        o = vb.bt(sig, b.intra, **kw); r = vb.isoos(o); r.update(variant=name, stock=s); rows.append(r)
add("kendi-takvim, thr1, w250, 15bps", cA, T)
add("ffill-BISTtakvim (orijinale benzer)", cB, T)
add("kendi-takvim, en az 3 bilesen", cC, T)
add("fiyat marji rejime bagli (+-20 2020 oncesi)", cA, T2)
for thr in (0.5, 0.75, 1.25, 1.5, 2.0):
    add(f"thr {thr}", cA, T, thr=thr)
add("isaret (thr 0)", cA, T, thr=0.0)
add("re-z yok, ham kompozit |c|>1", cA, T, rez=False)
for w in (120, 500):
    cw, _ = vb.comp(vb.JP_AU, w=w); add(f"z penceresi {w}", cw, T, w=w)
for cost in (8, 25):
    add(f"maliyet {cost}", cA, T, cost=cost)
# esit agirlikli ham getiri (z'siz) kompoziti
R = pd.DataFrame({s: vb.dret(s).reindex(vb.cal()) for s in vb.JP_AU}).mean(axis=1)
add("ham getiri ortalamasi (z'siz bilesen)", R, T)
V = pd.DataFrame(rows); V.to_csv(os.path.join(vb.OUT, "res_s1_variants.csv"), index=False)
pd.set_option("display.width", 250)
print(V[["variant", "stock", "IS_n", "IS_bps", "IS_t", "OOS_n", "OOS_bps", "OOS_t", "OOS_sh"]].round(2).to_string())
