"""s3c: ACILIS'in tam bayatlık payları ve isy saatlik veri kalitesi (Yahoo günlük [l,h] içinde mi)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc
L=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s); L.append(s)
J = pd.read_parquet(f"{bc.RES}/s3_join.parquet")
y = J.index.year
P("ACILIS == önceki UZLAŞMA payı:", (J.open == J.psettle).groupby(y).mean().round(3).to_dict())
P("ACILIS == önceki KAPANIS (aynı sözleşme) payı:", (J.open == J.pclose_same).groupby(y).mean().round(3).to_dict())
P("|ln(ACILIS/önceki KAPANIS)| < 1 tik payı (~2bps 2017-21, 0.3-0.9 sonra):", (J.f_gapc.abs() < np.where(J.index.year<=2021, 2.5e-4, 1e-4)).groupby(y).mean().round(3).to_dict())
P("medyan |f_gapc| vs |s_gap| (bps):", {k: (round(a,1), round(b,1)) for k,a,b in zip(sorted(set(y)), (J.f_gapc.abs().groupby(y).median()*1e4).values, (J.gap.abs().groupby(y).median()*1e4).values)})
# isy kalite
s = pd.read_parquet(f"{bc.RES}/s2_XU030.parquet"); yh = bc.yahoo("XU030.IS")
s["h"] = yh.h.reindex(s.index); s["l"] = yh.l.reindex(s.index)
cols = [c for c in s.columns if c.startswith("p") and c[1:].isdigit()]
out = pd.Series(False, index=s.index)
for c in cols:
    out |= (s[c] > s.h * 1.0005) | (s[c] < s.l * 0.9995)
P("isy saatlik değerlerden biri Yahoo [l,h] dışında olan gün payı (yıl):", out.groupby(s.index.year).mean().round(3).to_dict())
open(f"{bc.RES}/s3c_stale.log","w").write("\n".join(L))
