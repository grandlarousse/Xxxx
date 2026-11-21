"""L4 hızlı takvim testi: ay dönümü, tatil öncesi, opsiyon vadesi haftası. Kapanıştan kapanışa günlük getiri (adjclose).
Her gün t için r_t = C_t/C_{t-1}-1; 'pencere günü' r_t'yi kazanmak için t-1 kapanışında alınır."""
import os, sys
import numpy as np, pandas as pd
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = pd.read_parquet(os.path.join(KOK, "veri", "panel_adjclose.parquet"))
p.index = pd.to_datetime(p.index)
SEM = sys.argv[1:] or ["SPY", "QQQ", "IWM", "XLK", "XLE", "XLF"]
idx = p["SPY"].dropna().index
idx = idx[idx >= "2000-01-01"]
d = pd.DataFrame(index=idx)
ay = idx.to_period("M")
# ay sonuna göre konum: T = ayın son işlem günü
pos_end = pd.Series(range(len(idx)), index=idx).groupby(ay).transform(lambda s: s - s.max())
pos_beg = pd.Series(range(len(idx)), index=idx).groupby(ay).transform(lambda s: s - s.min() + 1)
d["tom7"] = ((pos_end >= -3) | (pos_beg <= 3)).values          # T-3..T+3
d["tom4"] = ((pos_end == 0) | (pos_beg <= 3)).values           # T..T+3
d["pretom"] = ((pos_end >= -8) & (pos_end <= -4)).values        # T-8..T-4
# tatil öncesi: bir sonraki işlem günü, bir sonraki iş gününden sonra
nxt = pd.Series(idx[1:].append(pd.DatetimeIndex([idx[-1] + pd.offsets.BDay(1)])), index=idx)
d["pretatil"] = (nxt > idx + pd.offsets.BDay(1)).values
# opsiyon vadesi haftası: ayın 3. cuması ile biten hafta (Pzt-Cum)
def ucuncu_cuma(ts):
    f = ts.replace(day=1); f = f + pd.Timedelta(days=(4 - f.weekday()) % 7); return f + pd.Timedelta(days=14)
tf = pd.DatetimeIndex([ucuncu_cuma(t) for t in idx])
d["opex"] = ((idx <= tf) & (idx > tf - pd.Timedelta(days=7))).values
d["opex_sonrasi"] = ((idx > tf) & (idx <= tf + pd.Timedelta(days=7))).values
DON = [("2000-2014", "2000", "2014"), ("2015-2026", "2015", "2026"), ("2020-2026", "2020", "2026"), ("2024-2026", "2024", "2026")]
satir = []
for s in SEM:
    r = p[s].reindex(idx).pct_change()
    for ad, a, b in DON:
        m = (idx.year >= int(a)) & (idx.year <= int(b))
        for k in ["tom7", "tom4", "pretom", "pretatil", "opex", "opex_sonrasi"]:
            x = r[m & d[k].values].dropna(); y = r[m & ~d[k].values].dropna()
            fark = x.mean() - y.mean(); se = np.sqrt(x.var() / len(x) + y.var() / len(y))
            satir.append([s, ad, k, len(x), round(x.mean() * 1e4, 1), round(y.mean() * 1e4, 1), round(fark * 1e4, 1), round(fark / se, 2)])
o = pd.DataFrame(satir, columns=["sembol", "donem", "etki", "n_gun", "ort_bps", "diger_bps", "fark_bps", "t"])
pd.set_option("display.width", 200); pd.set_option("display.max_rows", 500)
print(o.to_string(index=False))
o.to_csv(os.path.join(KOK, "ek", "literatur", "l4_takvim_hizli_test.csv"), index=False)
