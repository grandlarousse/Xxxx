"""Korelasyon ve stres: XU030 vs XBANK vs USDTRY (Yahoo günlük). python3 -I corr_stress.py <dl_dir>"""
import json, math, sys, datetime as dt, os

d = sys.argv[1]
def load(fn):
    j = json.load(open(os.path.join(d, fn)))["chart"]["result"][0]
    out = {}
    for t, c in zip(j["timestamp"], j["indicators"]["quote"][0]["close"]):
        if c is not None:
            out[dt.datetime.fromtimestamp(t + 10800, dt.timezone.utc).date()] = c
    return out

x30, xb, usd = load("y_XU030.IS.json"), load("y_XU100.IS.json"), load("y_TRY.json")
xbank = load("y_XBANK.IS.json")
days = sorted(set(x30) & set(xbank) & set(usd))
def rets(s):
    return [math.log(s[days[i]] / s[days[i - 1]]) for i in range(1, len(days))]
r30, rbk, rus = rets(x30), rets(xbank), rets(usd)
def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    c = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return c / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
for n in (60, 250):
    print(f"{n}g korelasyon XU030-XBANK {corr(r30[-n:], rbk[-n:]):.2f} | XU030-USDTRY {corr(r30[-n:], rus[-n:]):.2f}")
    # beta XBANK on XU030
    a, b = r30[-n:], rbk[-n:]
    ma, mb = sum(a) / n, sum(b) / n
    beta = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / sum((x - ma) ** 2 for x in a)
    print(f"   XBANK beta(XU030) {beta:.2f}; USDTRY RV {math.sqrt(sum(v*v for v in rus[-n:])/n*252)*100:.1f}%")
# XU030 tüm geçmiş (2y) en kötü k-günlük getiriler
s = [x30[k] for k in sorted(x30)]
for k in (1, 3, 5, 10):
    worst = min(s[i] / s[i - k] - 1 for i in range(k, len(s)))
    best = max(s[i] / s[i - k] - 1 for i in range(k, len(s)))
    print(f"XU030 2y en kötü {k}g: {worst*100:.1f}%  en iyi: {best*100:.1f}%")
# Tatil/hafta sonu boşlukları: >1 takvim günü aradan sonraki getiriler
ks = sorted(x30)
gaps = [(ks[i], x30[ks[i]] / x30[ks[i - 1]] - 1) for i in range(1, len(ks)) if (ks[i] - ks[i - 1]).days > 3]
print("Tatil sonrası (>3 gün ara) getiriler:", [(str(a), round(b * 100, 2)) for a, b in gaps])
