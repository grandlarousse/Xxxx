"""Zamanlama sağlık kontrolleri: KS11 günlük kapanışı saati; XU030 günlük 'o' = 5 dk 06:55 barı?; TUR/ES/GC/TRY h1 son bar saatleri."""
import numpy as np, pandas as pd
from vcore import *
log = open(f"{OUT}/v0_timing.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n")

for sym in ["^KS11", "^N225", "GC=F", "TUR", "ES=F", "TKC", "EEM", "XU030.IS", "TRY=X"]:
    try:
        h = bars(sym, "h1")
    except Exception as e:
        P(sym, "h1 yok"); continue
    d = frame(sym)
    st = h.index
    last = pd.Series(st, index=st).groupby(st.tz_convert(None).normalize()).max()
    P(f"{sym}: h1 son bar başlangıcı (UTC) dağılımı:", last.dt.strftime("%H:%M").value_counts().head(4).to_dict())
    # günlük c ile h1 son bar c eşleşmesi (aynı ldate)
    hl = h.groupby(h["ldate"]).last()["c"]; hl.index = pd.to_datetime(hl.index)
    j = pd.concat([d["c"].rename("d"), hl.rename("h")], axis=1, join="inner").dropna()
    P(f"   günlük c vs h1 aynı-ldate son bar c: |fark|<10bp oranı {((np.log(j.d / j.h)).abs() < 0.001).mean():.3f} (n {len(j)})")

# XU030 günlük o vs m5 06:55 barı
m = bars("XU030.IS", "m5"); d = frame("XU030.IS")
b655 = m[(m.index.hour == 6) & (m.index.minute == 55)]
b655.index = pd.to_datetime(b655["ldate"])
j = pd.concat([d["o"].rename("o"), b655["c"].rename("c655"), b655["o"].rename("o655")], axis=1, join="inner").dropna()
P("XU030 günlük o == m5 06:55 barı c (|fark|<1bp) oranı:", round(((np.log(j.o / j.c655)).abs() < 1e-4).mean(), 3), "; == 06:55 o:", round(((np.log(j.o / j.o655)).abs() < 1e-4).mean(), 3), "n", len(j))
# THYAO aynı
m = bars("THYAO.IS", "m5"); d = frame("THYAO.IS")
b655 = m[(m.index.hour == 6) & (m.index.minute == 55)]; b655.index = pd.to_datetime(b655["ldate"])
j = pd.concat([d["o"].rename("o"), b655["c"].rename("c655"), b655["o"].rename("o655")], axis=1, join="inner").dropna()
P("THYAO günlük o == m5 06:55 c:", round(((np.log(j.o / j.c655)).abs() < 1e-4).mean(), 3), "; == 06:55 o:", round(((np.log(j.o / j.o655)).abs() < 1e-4).mean(), 3), "n", len(j))
# KS11 günlük: ldate ile UTC tarih
k = raw("^KS11"); P("^KS11 günlük bar başlangıç saatleri:", pd.Series(k.index.strftime("%H:%M")).value_counts().head(3).to_dict(),
                     "ldate==UTC tarih oranı", round((pd.to_datetime(k["ldate"]).dt.date == k.index.tz_convert(None).date).mean(), 4))
log.close()
