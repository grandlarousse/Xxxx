"""Gerçekleşen volatilite hesabı: Yahoo Finance günlük kapanışları (XU030.IS, XU100.IS).
Kullanım: python3 -I rv_calc.py <json_dosyasi>
"""
import json, math, sys, datetime as dt

path = sys.argv[1]
d = json.load(open(path))
r = d["chart"]["result"][0]
ts = r["timestamp"]
cl = r["indicators"]["quote"][0]["close"]
rows = [(dt.datetime.utcfromtimestamp(t + 10800).date(), c) for t, c in zip(ts, cl) if c is not None]
print("Sembol:", r["meta"]["symbol"], "gözlem:", len(rows), "ilk:", rows[0][0], "son:", rows[-1])
print("52h yüksek/düşük:", r["meta"].get("fiftyTwoWeekHigh"), r["meta"].get("fiftyTwoWeekLow"))

rets = [(rows[i][0], math.log(rows[i][1] / rows[i - 1][1])) for i in range(1, len(rows))]

def rv(n, end=None):
    x = [v for _, v in rets[-n:]] if end is None else [v for _, v in rets[end - n:end]]
    m = sum(x) / len(x)
    var = sum((v - m) ** 2 for v in x) / (len(x) - 1)
    var0 = sum(v * v for v in x) / len(x)  # sıfır ortalamalı
    return math.sqrt(var * 252), math.sqrt(var0 * 252)

for n in (10, 20, 60, 120, 250):
    if len(rets) >= n:
        a, b = rv(n)
        print(f"RV{n}: {a*100:.1f}% (sıfır-ort: {b*100:.1f}%)")
# 1 yıllık rolling 20g RV dağılımı
roll = []
for e in range(20, len(rets) + 1):
    x = [v for _, v in rets[e - 20:e]]
    roll.append(math.sqrt(sum(v * v for v in x) / 20 * 252))
roll_s = sorted(roll)
print(f"2y rolling RV20 (sıfır-ort) medyan {roll_s[len(roll_s)//2]*100:.1f}%, p10 {roll_s[len(roll_s)//10]*100:.1f}%, p90 {roll_s[int(len(roll_s)*0.9)]*100:.1f}%, maks {roll_s[-1]*100:.1f}%")
print("\nSon 45 gün (tarih, kapanış, log getiri %):")
for (day, c), (_, rr) in zip(rows[-45:], rets[-45:]):
    print(day, f"{c:,.2f}", f"{rr*100:+.2f}")
# zirve ve düşüş
pk = max(rows[-120:], key=lambda x: x[1])
print("\nSon 120 gün zirve:", pk, "son/zirve-1:", f"{(rows[-1][1]/pk[1]-1)*100:.1f}%")
# 5 günlük getiri dağılımı (gap/hafta riski için)
big = sorted(rets, key=lambda x: x[1])[:8]
print("En kötü 8 gün:", [(str(a), round(b * 100, 2)) for a, b in big])
