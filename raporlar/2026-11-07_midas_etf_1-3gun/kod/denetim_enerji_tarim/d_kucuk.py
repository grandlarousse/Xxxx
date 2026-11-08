"""Denetim küçük kontroller: S2 'sinyal+1 gün, O1 h2' iddiası; ERX~XLE yıllık beta (kaldıraç değişikliği -> ERX<-XLE FDR satırı artefaktı mı?).
Çalıştırma: python3 -I kod/denetim_enerji_tarim/d_kucuk.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dsim as D, lib
from d_s2_uso_bb import bb_sig
uso = lib.load("USO"); s = bb_sig(uso); s1 = np.zeros_like(s); s1[1:] = s[:-1]
st = D.st(D.sim(uso, s1, 2, "O1"), D.cost("USO")); print("S2 kaydırılmış O1 h2 (t+2 açılış -> t+3 kapanış):", {k: round(st[k], 2) for k in ["n", "net_bp", "t", "is_net_bp", "oos_net_bp"]})
st = D.st(D.sim(uso, s1, 3, "O1"), D.cost("USO")); print("S2 kaydırılmış O1 h3 (t+2 açılış -> t+4 kapanış):", {k: round(st[k], 2) for k in ["n", "net_bp", "t", "is_net_bp", "oos_net_bp"]})
r = pd.DataFrame({"e": lib.load("ERX")["c"].pct_change(), "x": lib.load("XLE")["c"].pct_change()}).dropna()
print("ERX~XLE yıllık beta:", r.groupby(r.index.year).apply(lambda g: np.polyfit(g["x"], g["e"], 1)[0]).round(2).to_dict())
m = r.index.year == 2020
for a, b in (("2020-01-01", "2020-03-31"), ("2020-04-01", "2020-12-31")):
    g = r[(r.index >= a) & (r.index <= b)]; print(f"  {a}..{b}: beta {np.polyfit(g['x'], g['e'], 1)[0]:.2f}")
