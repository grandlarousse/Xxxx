"""Zamanlama: VİOP XAUUSD uzlaşma değişimi hangi saatteki GC=F fiyat değişimine karşılık geliyor? (5 dk ve 60 dk barlar)"""
import pl, numpy as np, pandas as pd
pl.install_panel()
g = pl.ev.R("XAUUSD")
rows = []
for kind, times in (("m5", [(h, m) for h in (13, 14, 15) for m in range(0, 60, 5)]), ("h1", [(h, 0) for h in (12, 13, 14, 15, 16, 17)])):
    for hh, mm in times:
        s = pl.snap("GC=F", kind, hh, mm); r = pl.snap_ret(s)
        b = pd.concat([g.rename("g"), r.rename("r")], axis=1).dropna()
        if kind == "h1": b = b[b.index >= "2024-07-01"]
        rows.append(dict(kind=kind, utc=f"{hh:02d}:{mm:02d}", tsi=f"{hh+3:02d}:{mm:02d}", n=len(b), corr=round(b.corr().iloc[0, 1], 4),
                         rmse_bps=round(((b.g - b.r) ** 2).mean() ** .5 * 1e4, 1), first=str(b.index.min().date()), last=str(b.index.max().date())))
T = pd.DataFrame(rows); print(T.to_string()); T.to_csv(pl.R + "/sonuc/zamanlama_corr.csv", index=False)
