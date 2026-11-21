"""Eleştirmen turunda öne sürülen üç sayının kontrolü. Kullanım: python3 03_ek_kontrol.py <veri_klasoru> <K1_tum_testler.csv>"""
import sys, pandas as pd, numpy as np
D, K1 = sys.argv[1], sys.argv[2]
ld = lambda t: pd.read_csv(f"{D}/d_{t}.csv", index_col=0, parse_dates=True)
kold, ung = ld("KOLD").Close, ld("UNG").Close
# (a) Şükran haftası Çarşambası: Salı kapanışı -> Çarşamba kapanışı, KOLD
r = kold.pct_change()
rows = []
for y in range(2012, 2026):
    nov = pd.date_range(f"{y}-11-01", f"{y}-11-30")
    thu = [d for d in nov if d.weekday() == 3][3]          # dördüncü Perşembe
    wed = thu - pd.Timedelta(days=1)
    if wed in r.index: rows.append((y, round(r[wed] * 100, 2)))
v = np.array([x[1] for x in rows])
print("(a) Şükran Çarşambası KOLD %:", rows)
print("    ortalama %.2f, medyan %.2f, artıda %d/%d" % (v.mean(), np.median(v), (v > 0).sum(), len(v)))
# (b) UNG 60 günlük oynaklık ve eşik
ru = ung.pct_change()
s60 = ru.rolling(60).std().shift(1)
print("(b) UNG σ60 son gün %.2f%% -> 2σ eşiği %.2f%%; 2022+ medyan σ60 %.2f%%; 2011-10..2021 medyan %.2f%%" % (
    ru.rolling(60).std().iloc[-1] * 100, 2 * ru.rolling(60).std().iloc[-1] * 100,
    s60["2022":].median() * 100, s60["2011-10-06":"2021"].median() * 100))
# (c) Lead-lag testlerinde tespit edilebilir en küçük etki (MDE) ve ölçülen etki
k = pd.read_csv(K1)
for t in ["E1", "E2", "E3", "E4", "E5", "E6"]:
    x = k[k.test == t]
    if "MDE" in x and len(x):
        print("(c) %s: satır %d, medyan MDE %.0f bps, medyan |OOS ort| %.0f bps, medyan |IS ort| %.0f bps" % (
            t, len(x), x.MDE.median(), x.OOS_ort.abs().median(), x.IS_ort.abs().median()))
