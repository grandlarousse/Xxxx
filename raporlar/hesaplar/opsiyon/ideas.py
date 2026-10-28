"""Önerilen iki fikrin güncel piyasa girdileriyle fiyatlaması (28.10.2026).
F = Aralık vadeli 14.644 (foreks 28.10 13:11), S = 13.961 (Yahoo 28.10), vade 31.12.2026.
python3 -I ideas.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs import b76, greeks76, iv76, N

F, S, r, T, M = 14644.0, 13961.0, 0.36, 64 / 365, 10
s_ = lambda sig: sig * math.sqrt(T)
def p_above(K, sig, center):
    s = s_(sig); return N((math.log(center / K) - 0.5 * s * s) / s)

legs1 = [(+1, "C", 14500), (-1, "C", 15500)]
legs2 = [(+1, "P", 14000), (-1, "P", 13250)]
for name, legs in (("Fikir1 C14500/C15500", legs1), ("Fikir2 P14000/P13250", legs2)):
    print("\n" + name)
    for sig in (0.12, 0.17, 0.24, 0.32):
        prem = sum(q * b76(F, K, T, r, sig, cp) for q, cp, K in legs)
        d = sum(q * greeks76(F, K, T, r, sig, cp)["delta"] for q, cp, K in legs)
        v = sum(q * greeks76(F, K, T, r, sig, cp)["vega"] for q, cp, K in legs)
        th = sum(q * greeks76(F, K, T, r, sig, cp)["theta"] for q, cp, K in legs)
        width = abs(legs[0][2] - legs[1][2])
        if legs[0][1] == "C":
            be = legs[0][2] + prem
            pp_rn, pp_0 = p_above(be, sig, F), p_above(be, sig, S)
            pmax_rn, pmax_0 = p_above(legs[1][2], sig, F), p_above(legs[1][2], sig, S)
        else:
            be = legs[0][2] - prem
            pp_rn, pp_0 = 1 - p_above(be, sig, F), 1 - p_above(be, sig, S)
            pmax_rn, pmax_0 = 1 - p_above(legs[1][2], sig, F), 1 - p_above(legs[1][2], sig, S)
        print(f"  σ={sig:.0%}: prim {prem:6.1f}p ({prem*M:,.0f} TL) maksKâr {(width-prem)*M:,.0f} TL R/R {(width-prem)/prem:.2f} BE {be:,.0f} (spota göre {(be/S-1)*100:+.1f}%) Δ {d:+.3f} vega/vp {v*M:,.0f} TL theta/gün {th*M:,.0f} TL | P(kâr) RN {pp_rn*100:.0f}% sıfır-drift {pp_0*100:.0f}% | P(maks) RN {pmax_rn*100:.0f}% sıfır-drift {pmax_0*100:.0f}%")
print("\nTek bacak fiyatları ve limit fiyatların IV karşılığı:")
for cp, K in (("C", 14500), ("C", 15500), ("P", 14000), ("P", 13250)):
    print(f"  {cp}{K}: σ12% {b76(F,K,T,r,.12,cp):6.1f} σ17% {b76(F,K,T,r,.17,cp):6.1f} σ24% {b76(F,K,T,r,.24,cp):6.1f} σ32% {b76(F,K,T,r,.32,cp):6.1f}")
for cp, K, px in (("C", 14500, 420), ("C", 14500, 450), ("P", 14000, 180), ("P", 14000, 200)):
    print(f"  {cp}{K} @ {px} -> IV {iv76(px, F, K, T, r, cp)*100:.1f}%")
# Ara dönem değer: 10 Aralık'ta (21 gün kala) spread değeri farklı spotlarda (σ=24%, F/S oranı sabit taşıma ile)
print("\nFikir1 spread değeri 10.12.2026'da (T=21g, σ=24%, F = S*e^(0.272*T)):")
T2 = 21 / 365
for Sx in (13000, 13500, 14000, 14500, 15000, 15500, 16000):
    Fx = Sx * math.exp(0.272 * T2)
    val = b76(Fx, 14500, T2, r, .24, "C") - b76(Fx, 15500, T2, r, .24, "C")
    val2 = b76(Fx, 14000, T2, r, .24, "P") - b76(Fx, 13250, T2, r, .24, "P")
    print(f"  spot {Sx}: F {Fx:,.0f} call spread {val:6.1f}p | put spread {val2:6.1f}p")
# Hedge örneği: 1 mn TL beta-1 BIST30 long'a karşı put spread adedi ve sonuç
E = 1_000_000
n = round(E / (M * 14000))
for sig in (0.24,):
    prem = b76(F, 14000, T, r, sig, "P") - b76(F, 13250, T, r, sig, "P")
print(f"\nHedge: {E:,} TL long (beta 1) için {n} put spread; maliyet {n*prem*M:,.0f} TL ({n*prem*M/E*100:.2f}%)")
for X in (12000, 12500, 13000, 13250, 13961, 14640, 15500):
    port = E * (X / S - 1)
    hedge = n * M * (max(14000 - X, 0) - max(13250 - X, 0)) - n * prem * M
    print(f"  endeks {X}: portföy {port:,.0f} TL, hedge {hedge:,.0f} TL, net {port+hedge:,.0f} TL")
# Vadeli teminat ve kaldıraç
psr = 0.114
notional = F * M
print(f"\nBIST30 Aralık vadeli 1 kontrat nominal {notional:,.0f} TL; PSR %11.4 -> başlangıç teminatı ≈ {psr*notional:,.0f} TL; kaldıraç ≈ {1/psr:.1f}x; sürdürme (%75) için tetik hareket ≈ {psr*0.25*100:.2f}% ({psr*0.25*F:,.0f} puan)")
for mv in (-0.06, -0.10, -0.175):
    print(f"  {mv*100:.1f}% gap: kontrat başı zarar {mv*notional:,.0f} TL = başlangıç teminatının {abs(mv)/psr:.2f} katı")
