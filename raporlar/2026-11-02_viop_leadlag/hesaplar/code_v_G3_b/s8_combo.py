"""s8: Vadeli 'gece+sabah uzun (KAPANIS_{T-1} -> 11:00_T)' proxy'si, kombine strateji, kayan pencere istikrarı, son 12 ay."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc
L=[]
def P(*a):
    s=" ".join(str(x) for x in a); print(s); L.append(s)
J = pd.read_parquet(f"{bc.RES}/s3_join.parquet"); J = J[J.f_gapc.abs() < bc.LIM]
J["f_cc_close"] = np.log(J.close / J.pclose_same)      # aynı sözleşme kapanıştan kapanışa (roll yok)
J["long_on"] = J.f_cc_close - J.s_11c                   # vadeli KAPANIS_{T-1}->11:00_T proxy (öğleden sonrası spotla)
J["short_pm"] = -J.s_11c
J["combo"] = J.long_on + J.short_pm
for nm,a,b in [("2017-2020","2017","2020"),("2021-2022","2021","2022"),("2023-2026","2023","2026"),("2017-2026","2017","2026")]:
    g = J.loc[a:b]
    P(f"{nm}: vadeli cc {bc.st(g.f_cc_close)['mean']:.1f} | gece+sabah uzun proxy {bc.fmt(bc.st(g.long_on),('mean','t'))} | 11->K kısa {bc.fmt(bc.st(g.short_pm),('mean','t'))} | kombine {bc.fmt(bc.st(g.combo),('mean','t'))}")
P("gece+sabah uzun proxy yıllık:", {k: round(v*1e4,1) for k,v in J.long_on.groupby(J.index.year).mean().items()})
s = pd.read_parquet(f"{bc.RES}/s2_XU030.parquet"); s = s[s.first_h==11.0]
r = -np.log(s.c/s.p11)
roll = r.rolling(250).mean()*1e4
P(f"11->K kısa 250g kayan ortalama >0 gün payı {(roll.dropna()>0).mean():.2f}; min {roll.min():.1f} max {roll.max():.1f}")
P(f"son 250 gün {r.iloc[-250:].mean()*1e4:.1f} (t {bc.st(r.iloc[-250:])['t']:.2f}); 2026 Ocak-Ağustos {bc.st(r.loc['2026-01':'2026-08'])['mean']:.1f}; 2026 Eyl-Eki {bc.st(r.loc['2026-09':'2026-10'])['mean']:.1f}")
# UZLAŞMA ile çıkış (son 10 dk VWAP) vs KAPANIS
P(f"vadeli: ln(KAPANIS/UZLAŞMA) ort {np.log(J.close/J.settle).mean()*1e4:.2f} bps, sd {np.log(J.close/J.settle).std()*1e4:.1f}")
open(f"{bc.RES}/s8_combo.log","w").write("\n".join(L))
