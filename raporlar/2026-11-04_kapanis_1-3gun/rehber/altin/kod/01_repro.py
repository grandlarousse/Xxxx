"""Adım 1: Araştırma kuralını birebir yeniden üret (c3_gold.py ana varyantı: VİOP XAUUSD uzlaşma z -> F_TRALT - b*F_XU030, h2, |z|>1)."""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_dis-suruculer_curut")
import numpy as np, pandas as pd, cl, ev
g = ev.R("XAUUSD"); z = cl.zscale(g, 250, 100)
res, G, tr = ev.evaluate("GOLD_V->TRALT h2 hedged", z, "TRALT", main=(2, 1.0, "hedged"), start="2018-12-17", nsim=0, placebo=False, verbose=False)
print(json.dumps(res, ensure_ascii=False, default=str, indent=0))
print(G[(G.h == 2) & (G.thr == 1.0)].round(2).to_string())
r3, _, _ = ev.evaluate("raw", z, "TRALT", main=(2, 1.0, "raw"), start="2018-12-17", nsim=0, placebo=False, verbose=False)
print("raw h2:", r3["net8"], r3["t8"], r3["drop_top10"])
# yayımlanan: n 405, 55/yıl, +42,9 (t 2,54), net15 +35,9, IS +44,1 (1,82) / OOS +42,3 (1,89), drop10 +20,7 (1,31), 2024-26 +69,7 (2,44)
tr.to_csv("/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/altin/sonuc/repro_trades.csv")
