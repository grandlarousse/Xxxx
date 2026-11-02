"""V2 ek: haftanın günü etkisi ES vadeli verisine mi özgü? ^GSPC_{t-1} ile aynı kırılım + FOMC tutanakları (karardan 3 hafta sonra Çarşamba) etkisi."""
import numpy as np, pandas as pd
from vcore import *
c = cal(); g = decomp("XU100.IS")
MY = pd.DatetimeIndex(open("v3_olay.py").read().split('MY = """')[1].split('"""')[0].split())
react = pd.DatetimeIndex([c[c.searchsorted(d, side="right")] for d in MY])
# FOMC tutanakları: kararın 21 gün sonrası (Çarşamba), 2014+ kural
mins = MY + pd.Timedelta(days=21); react_m = pd.DatetimeIndex([c[c.searchsorted(d, side="right")] for d in mins if c.searchsorted(d, side="right") < len(c)])
out = open(f"{OUT}/v3d_weekday_spx.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")
for nm in ["^GSPC", "ES=F"]:
    x = ret(nm, "c").shift(1)
    df = pd.DataFrame({"y": g.gap, "x": x, "F": c.isin(react), "M": c.isin(react_m), "wd": c.weekday}, index=c).loc["2014":].dropna()
    s = []
    for wd in range(5):
        d = df[(df.wd == wd) & ~df.F]; s.append(f"{['Pzt','Sal','Çar','Per','Cum'][wd]} β {hc_t(d.y, d.x)[0]:.3f} (r {d.y.corr(d.x):.2f})")
    P(f"{nm}_{{t-1}} -> XU100 gap, FOMC-dışı, tepki gününe göre: " + " | ".join(s))
    d = df[(df.wd == 3) & ~df.F & ~df.M]; P(f"   Per, FOMC ve tutanak dışı: β {hc_t(d.y, d.x)[0]:.3f} r {d.y.corr(d.x):.2f} n {len(d)}")
    d = df[df.M]; P(f"   FOMC tutanak gecesi: β {hc_t(d.y, d.x)[0]:.3f} r {d.y.corr(d.x):.2f} n {len(d)}")
    d = df[df.F]; P(f"   FOMC karar gecesi: β {hc_t(d.y, d.x)[0]:.3f} r {d.y.corr(d.x):.2f} n {len(d)}")
out.close()
