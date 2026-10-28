"""Örnek yapıların Black-Scholes/Black-76 fiyatlaması — BIST30 Aralık 2026 (vade 31.12.2026).
Çarpan: 10 TL / endeks puanı (Borsa İstanbul sözleşme şartnamesi).
python3 -I structures.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs import b76, greeks76, N

MULT = 10
r = 0.36
T = 64 / 365            # 28.10.2026 -> 31.12.2026
S = 13900.0
F_theo = S * math.exp(r * T)
F_mkt_ratio = 14644 / 13961  # 28.10 Aralık vadeli / spot (foreks + Yahoo)
F_mkt = S * F_mkt_ratio
print(f"S={S:.0f} r={r:.0%} T={T:.4f}y  teorik F=S*e^(rT)={F_theo:.0f} (+{(F_theo/S-1)*100:.2f}%)  piyasa F≈{F_mkt:.0f} (+{(F_mkt/S-1)*100:.2f}%)")
print(f"Piyasa vadelisinin ima ettiği taşıma oranı: {math.log(F_mkt_ratio)/T*100:.1f}%/yıl; teorik F'ye göre iskonto {(F_mkt/F_theo-1)*100:.2f}%  DF={math.exp(-r*T):.4f}")

STRUCTS = {
    "(a) Boğa call spread 14500/15500": [(+1, "C", 14500), (-1, "C", 15500)],
    "(b) Ayı put spread 14000/13000 (hedge)": [(+1, "P", 14000), (-1, "P", 13000)],
    "(c) Risk reversal -P13250/+C15500": [(-1, "P", 13250), (+1, "C", 15500)],
    "(c') Risk reversal -P13500/+C15000": [(-1, "P", 13500), (+1, "C", 15000)],
    "(d) Uzun straddle 14500": [(+1, "C", 14500), (+1, "P", 14500)],
}

def payoff(legs, X):
    return sum(q * (max(X - K, 0) if cp == "C" else max(K - X, 0)) for q, cp, K in legs)

def analyze(name, legs, F, sig, label):
    prem = sum(q * b76(F, K, T, r, sig, cp) for q, cp, K in legs)  # + = net borç (ödenen)
    g = {k: sum(q * greeks76(F, K, T, r, sig, cp)[k] for q, cp, K in legs) for k in ("delta", "gamma", "vega", "theta")}
    grid = [x for x in range(9000, 21001, 5)]
    pl = [payoff(legs, X) - prem / math.exp(-r * T) * 0 - prem for X in grid]  # vade P/L (prim faizi ihmal)
    mx, mn = max(pl), min(pl)
    bes = [grid[i] for i in range(1, len(grid)) if (pl[i - 1] < 0) != (pl[i] < 0)]
    # olasılıklar: risk-nötr (F merkezli) ve sıfır drift (spot merkezli, muhafazakâr)
    def p_profit(center):
        s = sig * math.sqrt(T); tot = 0.0
        for i in range(len(grid)):
            if pl[i] > 0:
                X = grid[i]
                lo, hi = X - 2.5, X + 2.5
                z = lambda y: (math.log(y / center) + 0.5 * s * s) / s
                tot += N(z(hi)) - N(z(lo))
        return tot
    ev = 0.0
    s = sig * math.sqrt(T)
    for X in grid:
        z = lambda y: (math.log(y / F) + 0.5 * s * s) / s
        ev += (N(z(X + 2.5)) - N(z(X - 2.5))) * payoff(legs, X)
    print(f"  [{label} σ={sig:.0%} F={F:.0f}] net prim {prem:8.1f} puan = {prem*MULT:9,.0f} TL | maks kâr {mx:8.1f} ({mx*MULT:,.0f} TL) | maks zarar {mn:8.1f} ({mn*MULT:,.0f} TL) | başabaş {bes} | Δ {g['delta']:+.3f} vadeli-eşd. (={g['delta']*MULT*F:,.0f} TL) | vega/1vp {g['vega']*MULT:,.0f} TL | theta/gün {g['theta']*MULT:,.0f} TL | P(kâr) RN {p_profit(F)*100:.0f}% / sıfır-drift {p_profit(S)*100:.0f}%")
    return prem

for name, legs in STRUCTS.items():
    print("\n" + name)
    for sig in (0.20, 0.24, 0.32):
        analyze(name, legs, F_mkt, sig, "B76 piyasa F")
    analyze(name, legs, F_theo, 0.24, "BS teorik F")
    analyze(name, legs, F_mkt, 0.12, "işlem-IV 27.10")

# Faizin etkisi: aynı strike, F_theo vs F_mkt vs r=0 (F=S)
print("\nFaiz etkisi (σ=24%):")
for K, cp in ((14000, "C"), (14000, "P"), (14500, "C"), (14500, "P")):
    a = b76(S, K, T, 0.0, 0.24, cp)
    b = b76(F_theo, K, T, r, 0.24, cp)
    c = b76(F_mkt, K, T, r, 0.24, cp)
    print(f"  {cp}{K}: r=0 (F=S) {a:7.1f} | r=36% teorik F {b:7.1f} | r=36% piyasa F {c:7.1f}")

# Senaryo P/L tablosu (vade, puan)
print("\nVade senaryoları (puan, prim dahil, σ=24% piyasa F):")
lv = [12000, 13000, 13900, 14600, 15000, 15500, 16500]
print("  " + " ".join(f"{x:>7d}" for x in lv))
for name, legs in STRUCTS.items():
    prem = sum(q * b76(F_mkt, K, T, r, 0.24, cp) for q, cp, K in legs)
    print(f"  {name[:34]:34s} " + " ".join(f"{payoff(legs, x) - prem:7.0f}" for x in lv))
