"""Hakem: C1 dış geçerlilik (kısmi) — 2010-2016 Yahoo USDTRY spot: 20g sürüklenme -> ileri spot değişimi (taşıma yok, yalnız momentum bileşeni)."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
import numpy as np, pandas as pd
import lib_altin as L
sp = L.load_spot()
u = np.log(sp.y_USDTRY_X)
du = u.diff().where(u.diff() != 0)
for lag in (1, 2):
    s = du.rolling(20, min_periods=15).mean().shift(lag)   # ekstra gecikme: Yahoo kapanış kayması riskine karşı
    for h in (1, 5):
        y = u.shift(-h) - u
        for a, b in [("2010", "2016"), ("2017", "2026")]:
            m = (sp.index.year >= int(a)) & (sp.index.year <= int(b))
            q = L.ic(s[m], y[m], max(h, 5)); print(f"lag={lag} h={h} {a}-{b}: IC {q['ic']:+.3f} t {q['t']:+.2f} n {q['n']}")
# Dukascopy 15:00 (2016+) aynı test
p = L.load_viop(); lfx = np.log(p.dk_USDTRY_p15)
s = lfx.diff().rolling(20).mean().shift(1)
for h in (1, 5):
    q = L.ic(s, lfx.shift(-h) - lfx, max(h, 5)); print(f"Dukascopy 2017+ h={h}: IC {q['ic']:+.3f} t {q['t']:+.2f}")
