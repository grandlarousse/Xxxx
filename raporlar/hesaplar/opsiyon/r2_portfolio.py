"""Nihai komite portföyü: stop-bazlı risk ve 3 stres senaryosu (sermaye 10 mn TL).
Varsayım: tüm pozisyonlar planlanan giriş fiyatında açık; şok giriş fiyatından anlık; stoplar çalışmıyor (gap).
python3 -I r2_portfolio.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs import b76

CAP = 10_000_000
r, T0, T1 = 0.36, 60 / 365, 58 / 365      # giriş ~2.11, şok birkaç gün sonra
F0 = 14644.0
SCN = {"i": (-0.08, 0.05, 0.32), "ii": (+0.08, 0.0, 0.24), "iii": (-0.15, 0.12, 0.35)}  # (BIST, USDTRY, şok sonrası IV)

def opt_val(legs, F, T, sig):
    return sum(q * b76(F, K, T, r, sig, cp) for q, cp, K in legs)

out = []
# 1) MAKRO: F_USDTRY1226 kısa, 35 kontrat @52,473; stop 53,20
n_usd, Fu = 35, 52.473
row = {"poz": "MAKRO kısa F_USDTRY1226 ×35", "stop": n_usd * (53.20 - Fu) * 1000}
for k, (b, u, iv) in SCN.items():
    row[k] = -n_usd * Fu * u * 1000
out.append(row)
# 1b) opsiyonel kuyruk hedge: O_USDTRYKE1226C56000 ×35 @ 420 TL/1.000$
row = {"poz": "  + (ops.) C56000 USDTRY ×35 @420", "stop": 35 * 420}
for k, (b, u, iv) in SCN.items():
    Fs = Fu * (1 + u)
    val = b76(Fs, 56.0, T1, r, 0.20 if u > 0.06 else 0.17, "C") * 1000  # TL/1.000$
    row[k] = 35 * (val - 420)
out.append(row)
# 2) Rally short (ENDEKS+ŞEYTAN birleşik): 13 kontrat, ort. giriş 14.960, gün içi stop 15.550
n_s, Fe = 13, 14960.0
row = {"poz": "Rally short F_XU0301226 ×13 @14.960", "stop": n_s * (15550 - Fe) * 10}
for k, (b, u, iv) in SCN.items():
    row[k] = -n_s * Fe * b * 10
out.append(row)
# 3) HİSSE GARAN/YKBNK (Kasım kontratı), 135 GARAN / 420 YKBNK
g_n, y_n = 135 * 100 * 130.3, 420 * 100 * 36.27   # F_GARAN1126 / F_YKBNK1126 27.10 uzlaşma
row = {"poz": "HİSSE L GARAN/S YKBNK (Kas) 135/420", "stop": 0.04 * g_n}
for k, (b, u, iv) in SCN.items():
    bg, by = (1.06, 1.24) if b > 0 else (0.98, 1.03)
    if k == "iii":
        bg, by = 1.06, 1.24
    row[k] = g_n * b * bg - y_n * b * by
out.append(row)
row = {"poz": "  (idiosenkratik: YKBNK tavan +%10)", "stop": 0, "i": -y_n * 0.10, "ii": -y_n * 0.10, "iii": -y_n * 0.10}
out.append(row)
# 4) OPSİYON F1: straddle 14.500 ×5 @800
legs1 = [(1, "C", 14500), (1, "P", 14500)]
row = {"poz": "OPSİYON straddle 14.500 ×5 @800", "stop": 5 * 800 * 10}
for k, (b, u, iv) in SCN.items():
    row[k] = 5 * 10 * (opt_val(legs1, F0 * (1 + b), T1, iv) - 800)
out.append(row)
# 5) OPSİYON F2: call spread 14.500/15.500 ×14 @340
legs2 = [(1, "C", 14500), (-1, "C", 15500)]
row = {"poz": "OPSİYON call spread 14.5/15.5 ×14 @340", "stop": 14 * 340 * 10}
for k, (b, u, iv) in SCN.items():
    row[k] = 14 * 10 * (opt_val(legs2, F0 * (1 + b), T1, iv) - 340)
out.append(row)

print(f"{'Pozisyon':42s} {'stop %':>7s} {'(i) %':>7s} {'(ii) %':>7s} {'(iii) %':>8s}")
tot = {"stop": 0, "i": 0, "ii": 0, "iii": 0}
for row in out:
    print(f"{row['poz']:42s} {row['stop']/CAP*100:7.2f} {row['i']/CAP*100:7.2f} {row['ii']/CAP*100:7.2f} {row['iii']/CAP*100:8.2f}")
    if not row["poz"].startswith("  "):
        for k in tot: tot[k] += row[k]
print(f"{'TOPLAM (ops. hedge ve idiosenkratik hariç)':42s} {tot['stop']/CAP*100:7.2f} {tot['i']/CAP*100:7.2f} {tot['ii']/CAP*100:7.2f} {tot['iii']/CAP*100:8.2f}")
short = out[2]
print(f"{'TOPLAM, rally short dolmamışsa':42s} {(tot['stop']-short['stop'])/CAP*100:7.2f} {(tot['i']-short['i'])/CAP*100:7.2f} {(tot['ii']-short['ii'])/CAP*100:7.2f} {(tot['iii']-short['iii'])/CAP*100:8.2f}")
h = out[1]
print(f"{'TOPLAM, short dolmamış + C56000 hedge':42s} {(tot['stop']-short['stop']+h['stop'])/CAP*100:7.2f} {(tot['i']-short['i']+h['i'])/CAP*100:7.2f} {(tot['ii']-short['ii']+h['ii'])/CAP*100:7.2f} {(tot['iii']-short['iii']+h['iii'])/CAP*100:8.2f}")
# teminat kullanımı
m = n_usd * Fu * 1000 * 0.11 + n_s * Fe * 10 * 0.114 + g_n * 0.144 + y_n * 0.158 + 14 * 8180
print(f"\nTakasbank teminatı ≈ {m:,.0f} TL = %{m/CAP*100:.1f} (aracı kurum 1,5x: %{1.5*m/CAP*100:.1f}); prim: {(5*800+14*340)*10:,.0f} TL")
# Straddle beklenen değer makas sonrası
for mid in (800, 1100):
    for hs in (0.025, 0.075):
        cost = mid * (1 + hs)
        for sig in (0.17, 0.24, 0.27):
            fair = b76(F0, 14500, 64/365, r, sig, "C") + b76(F0, 14500, 64/365, r, sig, "P")
            print(f"  straddle orta {mid}, yarım makas %{hs*100:.1f} -> maliyet {cost:.0f}; RV %{sig*100:.0f}: EV {fair-cost:+.0f} puan")
