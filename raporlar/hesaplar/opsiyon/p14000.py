"""P14000 outright greeks ve hedge etkinliği; RV20 yüzdeliği. python3 -I p14000.py"""
import math, os, sys, json, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs import b76, greeks76, N
F, S, r, T = 14644.0, 13961.0, 0.36, 64/365
for sig in (0.17, 0.19, 0.24):
    p = b76(F, 14000, T, r, sig, "P"); g = greeks76(F, 14000, T, r, sig, "P")
    s = sig*math.sqrt(T); pr = lambda c: N((math.log((14000-p)/c) + 0.5*s*s)/s)
    print(f"P14000 σ={sig:.0%}: {p:.1f}p delta {g['delta']:+.3f} vega/vp {g['vega']*10:,.0f} TL theta/gün {g['theta']*10:,.0f} TL BE {14000-p:,.0f} P(BE altı) RN {pr(F)*100:.0f}% sıfır-drift {pr(S)*100:.0f}%")
prem = 200; n = 7; E = 1_000_000
for X in (12000, 13000, 13961, 15000):
    port = E*(X/S-1); h = n*10*(max(14000-X,0)) - n*prem*10
    print(f"  1mn TL long + 7xP14000@200: endeks {X}: portföy {port:,.0f} hedge {h:,.0f} net {port+h:,.0f}")
j = json.load(open("dl/y_XU030.IS.json"))["chart"]["result"][0]
c = [x for x in j["indicators"]["quote"][0]["close"] if x]
rt = [math.log(c[i]/c[i-1]) for i in range(1, len(c))]
roll = [math.sqrt(sum(v*v for v in rt[e-20:e])/20*252) for e in range(20, len(rt)+1)]
cur = roll[-1]; print(f"RV20 şu an {cur*100:.1f}%, 2y yüzdelik {sum(1 for x in roll if x <= cur)/len(roll)*100:.0f}")
