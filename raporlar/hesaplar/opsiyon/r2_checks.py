"""2. tur çapraz kontrol hesapları. python3 -I r2_checks.py"""
import json, math, csv, os, datetime as dt
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dl")

def load(fn):
    j = json.load(open(os.path.join(D, fn)))["chart"]["result"][0]
    return {dt.datetime.fromtimestamp(t + 10800, dt.timezone.utc).date(): c
            for t, c in zip(j["timestamp"], j["indicators"]["quote"][0]["close"]) if c}

# --- Bülten: Kasım pay vadelileri likiditesi
rows = []
with open(os.path.join(D, "bist/viop_20261027.csv"), encoding="windows-1254", errors="replace") as f:
    rd = csv.reader(f, delimiter=";"); h = [x.strip() for x in next(rd)]; next(rd)
    rows = [dict(zip(h, r)) for r in rd if len(r) >= 23]
for r in rows:
    if r["SOZLESME KODU"] in ("F_GARAN1126", "F_YKBNK1126", "F_SAHOL1126", "F_AKBNK1126"):
        print(r["SOZLESME KODU"], "uzl", r["UZLASMA FIYATI"], "adet", r["ISLEM MIKTARI"], "AP", r["ACIK POZISYON"])

# --- USDTRY: 31.12.2025 -> 27.10.2026
usd = load("y_TRY.json"); ks = sorted(usd)
a = max(k for k in ks if k <= dt.date(2025, 12, 31)); b = max(k for k in ks if k <= dt.date(2026, 10, 27))
chg = usd[b] / usd[a] - 1; days = (b - a).days
print(f"\nUSDTRY {a} {usd[a]:.3f} -> {b} {usd[b]:.3f}: {chg*100:.1f}% ({days}g, yıllık basit {chg*365/days*100:.1f}%)")
worst = sorted(((ks[i], usd[ks[i]] / usd[ks[i-1]] - 1) for i in range(1, len(ks))), key=lambda x: -x[1])[:3]
print("USDTRY en büyük günlük artışlar (kapanış):", [(str(x), round(y*100, 2)) for x, y in worst])

# --- XU100 zirveleri (ŞEYTAN/ENDEKS iddiaları)
x100 = load("y_XU100.IS.json"); k1 = sorted(x100)
sep = {k: v for k, v in x100.items() if dt.date(2026, 9, 1) <= k <= dt.date(2026, 9, 15)}
print("\nXU100 Eylül 1-15 kapanış maks:", max(sep.items(), key=lambda x: x[1]), "| 2y kapanış maks:", max(x100.items(), key=lambda x: x[1]))

# --- Pair: GARAN/YKBNK (0,85 hedge), SAHOL/AKBNK (0,70)
def pair(lng, sht, h):
    L, S = load(f"y_{lng}.json"), load(f"y_{sht}.json")
    days = sorted(set(L) & set(S))
    r = [(days[i], (L[days[i]] / L[days[i-1]] - 1) - h * (S[days[i]] / S[days[i-1]] - 1)) for i in range(1, len(days))]
    v = [x for _, x in r]
    sd = math.sqrt(sum(x*x for x in v[-250:]) / 250)
    w1 = sorted(r, key=lambda x: x[1])[:3]
    # 3 günlük
    r3 = []
    for i in range(3, len(days)):
        l3 = L[days[i]] / L[days[i-3]] - 1; s3 = S[days[i]] / S[days[i-3]] - 1
        r3.append((days[i], l3 - h * s3))
    w3 = min(r3, key=lambda x: x[1])
    # tek hisse en kötü/iyi günler
    rl = [L[days[i]] / L[days[i-1]] - 1 for i in range(1, len(days))]
    rs = [S[days[i]] / S[days[i-1]] - 1 for i in range(1, len(days))]
    print(f"\n{lng}/{sht} h={h}: günlük σ (long nominaline göre) {sd*100:.2f}% | 40g σ≈{sd*math.sqrt(40)*100:.1f}% | en kötü 1g {[(str(a), round(b*100,2)) for a,b in w1]} | en kötü 3g {w3[0]} {w3[1]*100:.2f}%")
    print(f"   {sht} en büyük günlük artış {max(rs)*100:.1f}% , {lng} en büyük düşüş {min(rl)*100:.1f}%")
    print(f"   son kapanış {lng} {L[days[-1]]:.2f} {sht} {S[days[-1]]:.2f} oran {L[days[-1]]/S[days[-1]]:.3f} ({days[-1]})")
pair("GARAN", "YKBNK", 0.85)
pair("SAHOL", "AKBNK", 0.70)

# --- Boyutlandırma kontrolleri
print("\nMAKRO F_USDTRY1226: 1 kontrat = 1.000 USD (bülten çarpanı ≈1000)")
F = 52.473
for n, cap in ((6, 1e6),):
    for g in (0.05, 0.12):
        loss = F * g * 1000 * n
        print(f"  {n} kontrat, +%{g*100:.0f} gap: kayıp {loss:,.0f} TL = sermayenin %{loss/cap*100:.2f}'i; teminat {n*F*1000*0.11:,.0f} TL")
    stop = (53.20 - F) * 1000 * n
    print(f"  stop 53,20: {stop:,.0f} TL = %{stop/cap*100:.2f}")
# MAKRO EV yeniden: %5 olasılık +%12 gap
ev = 0.7 * 793 + 0.2 * 95 + 0.05 * (-1650) + 0.05 * (-F * 0.12 * 1000)
print(f"  EV (şok kolunun yarısı +%12 gap): {ev:,.0f} TL/kontrat")

print("\nHİSSE GARAN/YKBNK: 18 GARAN @134,2 / 56 YKBNK @37,26 (27.10 uzlaşma)")
g, y = 18 * 100 * 134.2, 56 * 100 * 37.26
mg = g * 0.144 + y * 0.158
print(f"  nominal GARAN {g:,.0f} YKBNK {y:,.0f} oran {y/g:.2f}; Takasbank teminatı {mg:,.0f} TL (2x aracı {2*mg:,.0f})")
for name, gg, yy in (("i) BIST −%8 (β60)", -0.08*0.98, -0.08*1.03), ("ii) BIST +%8 (β250)", 0.08*1.06, 0.08*1.24),
                     ("iii) BIST −%15 (β250)", -0.15*1.06, -0.15*1.24), ("YKBNK +%10 tavan, GARAN 0", 0, 0.10),
                     ("GARAN −%10 taban, YKBNK 0", -0.10, 0)):
    pl = g * gg - y * yy
    print(f"  {name}: P/L {pl:,.0f} TL (%{pl/1e6*100:.2f} / 1 mn)")
print("\nHİSSE SAHOL/AKBNK: 14 SAHOL @90,72 / 13 AKBNK @67,95")
s_, a_ = 14 * 100 * 90.72, 13 * 100 * 67.95
print(f"  nominal {s_:,.0f}/{a_:,.0f}; teminat {s_*0.132+a_*0.157:,.0f}")
for name, ss, aa in (("i) −%8", -0.08*1.07, -0.08*1.23), ("ii) +%8", 0.08*1.07, 0.08*1.23), ("iii) −%15", -0.15*1.07, -0.15*1.23), ("SAHOL −%10 taban", -0.10, 0)):
    pl = s_ * ss - a_ * aa
    print(f"  {name}: {pl:,.0f} TL (%{pl/1e6*100:.2f})")
