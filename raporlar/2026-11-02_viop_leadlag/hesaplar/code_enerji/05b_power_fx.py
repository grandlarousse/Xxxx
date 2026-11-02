"""05 sağlamlık: aylık AKSEN~PTF ilişkisi ortak USDTRY paydasından mı geliyor? TL bazlı, XU100 TL + USDTRY kontrollü; yıllık işaret."""
import pandas as pd, numpy as np, elib
from elib import ll
ptf = elib.ptf_daily()
px = pd.concat({s: ll.daily(s) for s in ["AKSEN", "ENJSA", "ODAS", "XU100", "TRY=X"]}, axis=1).resample("ME").last()
r = np.log(px).diff(); r["ptf_tl"] = np.log(ptf.tl.resample("ME").mean()).diff(); r["ptf_usd"] = np.log(ptf.usd.resample("ME").mean()).diff()
r = r[r.index >= "2014-01-01"].dropna(subset=["ptf_tl", "AKSEN"])
for s in ["AKSEN", "ODAS", "ENJSA"]:
    a = r[[s, "ptf_tl", "XU100", "TRY=X"]].dropna()
    out = [f"{s}: TL c={a[s].corr(a.ptf_tl):.2f}", f"pc(XU100,USDTRY)={ll.partial_corr(a[s], a.ptf_tl, [a.XU100, a['TRY=X']])[0]:.2f}"]
    for per, x in [("IS", a[a.index < "2021"]), ("OOS", a[a.index >= "2021"])]:
        out.append(f"{per} pc={ll.partial_corr(x[s], x.ptf_tl, [x.XU100, x['TRY=X']])[0]:.2f} n={len(x)}")
    # yıllık işaret (aylık, yıl içinde 12 gözlem: gürültülü)
    yc = a.groupby(a.index.year).apply(lambda x: ll.partial_corr(x[s], x.ptf_tl, [x.XU100])[0] if len(x) >= 10 else np.nan).dropna()
    out.append(f"yıllık pc>0 oranı={(yc > 0).mean():.2f} ({len(yc)} yıl)")
    # ertesi ay (öncülük): PTF ay m -> hisse ay m+1
    b = pd.concat([a[s], a.ptf_tl.shift(1), a.XU100], axis=1).dropna()
    out.append(f"lead1ay pc={ll.partial_corr(b.iloc[:,0], b.iloc[:,1], [b.XU100])[0]:.2f}")
    print(" | ".join(out))
