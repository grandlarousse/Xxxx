"""G4 ek: TUR|ES kısmi korelasyonunun aykırı gözlem ve 2025 Mart duyarlılığı."""
import numpy as np, pandas as pd
from vcore import *
exec(open("v2_gunici.py").read().split("# 47 hisse")[0].replace('log = open(f"{OUT}/v2_gunici.log", "w")', 'log = open(f"{OUT}/v2b_tur_robust.log", "w")'))
df = pd.concat([GAP.rename("y"), TUR.rename("tur"), ES.rename("es")], axis=1).dropna()
ry = resid(df.y, df[["es"]]); rx = resid(df.tur, df[["es"]])
contrib = (ry - ry.mean()) * (rx - rx.mean()); top = contrib.abs().sort_values(ascending=False).index[:10]
P("\nG4 robustluk: TUR|ES pc katkısı en büyük 10 gün:", [(str(d.date()), round(df.y[d]*1e4), round(df.tur[d]*1e4), round(df.es[d]*1e4)) for d in top])
for k in [0, 3, 5, 10]:
    d2 = df.drop(contrib.abs().sort_values(ascending=False).index[:k])
    r = pc(d2.y, d2.tur, d2[["es"]]); P(f"  en etkili {k} gün hariç: pc {r['r']:+.3f} t {r['t']:.2f} n {r['n']}")
d3 = df[~((df.index >= "2025-03-17") & (df.index <= "2025-04-30"))]; r = pc(d3.y, d3.tur, d3[["es"]]); P(f"  17.03-30.04.2025 hariç: pc {r['r']:+.3f} t {r['t']:.2f}")
w = lambda s: s.clip(s.quantile(0.01), s.quantile(0.99))
r = pc(w(df.y), w(df.tur), w(df.es).to_frame()); P(f"  %1 winsor: pc {r['r']:+.3f} t {r['t']:.2f}")
r = pc(df.y.rank(), df.tur.rank(), df.es.rank().to_frame()); P(f"  rank (Spearman-kısmi): pc {r['r']:+.3f}")
log.close()
