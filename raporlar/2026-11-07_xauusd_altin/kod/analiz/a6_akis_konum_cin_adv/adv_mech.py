"""Mekanizma/zamanlama: bileşik artık x_t hangi ileri pencereyi öngörüyor? Tek gün gecikme yapısı ve seans ayrıştırması (spot saatlik)."""
import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import load_viop, ic, IS_END, hourly
D = load_viop(); R = D["v_ret"]
F = pd.read_csv(f"{S}/out/a6_akis_konum_cin_adv/adv_cn_features.csv", index_col=0, parse_dates=True).reindex(D.index)
x = F["comp"]
print("Tek gün: corr(x_t, v_ret_{t+j}) Spearman, NW t (lag 5); tam / IS / OOS")
for j in range(-1, 8):
    y = R.shift(-j)
    a = ic(x, y, 5); b = ic(x[D.index <= IS_END], y[D.index <= IS_END], 5); c = ic(x[D.index > IS_END], y[D.index > IS_END], 5)
    print(f" j={j:+d}: {a['ic']:+.3f} ({a['t']:+.2f}) | IS {b['ic']:+.3f} ({b['t']:+.2f}) | OOS {c['ic']:+.3f} ({c['t']:+.2f})")
print("\nx_{t-k} -> fwd5: ", {k: round(ic(x.shift(k), sum(R.shift(-i) for i in range(1, 6)), 5)['ic'], 3) for k in range(0, 5)})
print("x otokorelasyon:", [round(x.autocorr(k), 3) for k in range(1, 6)])

# seans ayrıştırması: spot saatlik, gün t+1..t+5 için Asya (00->07), Avrupa/NY sabah (07->15), akşam (15->24) pencereleri
hx = hourly("XAUUSD"); G = hx["c"].copy(); G.index = G.index.tz_convert("UTC").tz_localize(None) + pd.Timedelta(hours=1)
def at(ts):
    ts = pd.DatetimeIndex(ts); i = G.index.searchsorted(ts, side="right") - 1
    v = G.values[np.clip(i, 0, None)]; t0 = G.index[np.clip(i, 0, None)]
    return pd.Series(np.where((i >= 0) & ((ts - t0) / pd.Timedelta(hours=1) <= 3), v, np.nan), index=ts)
days = D.index
nxt = {k: pd.DatetimeIndex(pd.Series(days).shift(-k).values) for k in range(0, 7)}
rows = []
for k in range(1, 6):
    d0 = nxt[k - 1]; d1 = nxt[k]
    p15_0 = at(d0 + pd.Timedelta(hours=15)).values
    p00_1 = at(d1 + pd.Timedelta(hours=0)).values; p07_1 = at(d1 + pd.Timedelta(hours=7)).values; p15_1 = at(d1 + pd.Timedelta(hours=15)).values
    for nm, a_, b_ in [("15->00 (ABD akşamı)", p15_0, p00_1), ("00->07 (Asya)", p00_1, p07_1), ("07->15 (Londra/NY sabah)", p07_1, p15_1)]:
        y = pd.Series(np.log(b_ / a_), index=days)
        f = ic(x, y, 5); o = ic(x[days > IS_END], y[days > IS_END], 5); i_ = ic(x[days <= IS_END], y[days <= IS_END], 5)
        rows.append(dict(gun=f"t+{k}", pencere=nm, ic=round(f["ic"], 3), t=round(f["t"], 2), ic_is=round(i_["ic"], 3), t_is=round(i_["t"], 2), ic_oos=round(o["ic"], 3), t_oos=round(o["t"], 2)))
print(pd.DataFrame(rows).to_string(index=False))
# toplam 5 gün içinde seans payı
for nm in ["15->00 (ABD akşamı)", "00->07 (Asya)", "07->15 (Londra/NY sabah)"]:
    pass
