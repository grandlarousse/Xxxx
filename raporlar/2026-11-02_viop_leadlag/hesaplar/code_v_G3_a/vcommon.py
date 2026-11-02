"""v_G3_a ortak yardımcılar — ll.py'den BAĞIMSIZ (import edilmez).
Günlük Yahoo verisi: index = bar başlangıç zamanı (UTC), ldate = yerel işlem günü.
Temizlik: fiyat bazlı (c_t/c_{t-1}) +/-%10,5 dışı BIST günleri NaN (simetrik). Bölünme/bedelsiz sıçramaları buradan elenir.
Temettü: adj/c oranındaki değişim temettü bileşeni; gap_tr = ln(o_t/c_{t-1}) + temettü bileşeni (temettü gece oluşur).
"""
import numpy as np, pandas as pd, os
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/data"
STOCKS = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK".split()
assert len(STOCKS) == 47
LIM = np.log(1.105)

def daily(sym):
    d = pd.read_parquet(f"{D}/daily/{sym}.parquet")
    d = d.copy(); d["ldate"] = pd.to_datetime(d["ldate"]).dt.normalize()
    d = d[~d["ldate"].duplicated(keep="last")].set_index("ldate").sort_index()
    for k in "ohlc":
        d.loc[d[k] <= 0, k] = np.nan
    return d

def decomp(sym, start="2014-01-01", lim=LIM, open_fix=True):
    """cc, gap (fiyat), div, gap_tr, intra. Temizlik: |ln(c_t/c_{t-1})|>lim -> o gün NaN (cc, gap, intra)."""
    d = daily(sym)
    c = d["c"]; o = d["o"]; a = d["adj"] if "adj" in d else c
    cp = c.shift(1)
    cc_p = np.log(c / cp)
    ratio = (a / c)
    div = np.log(ratio / ratio.shift(1)).fillna(0.0)
    div = div.where(div.abs() < 0.2, 0.0)  # temettü bileşeni makul aralıkta
    gap = np.log(o / cp); intra = np.log(c / o)
    bad = cc_p.abs() > lim
    # açılış bozuksa (o, [l,h] dışında) NaN
    if open_fix and "h" in d:
        badopen = (o > d["h"] * 1.0001) | (o < d["l"] * 0.9999)
        gap = gap.where(~badopen); intra = intra.where(~badopen)
    # gap ve intra kendi başına da sınırlı: |gap|>lim ya da |intra|>lim -> NaN
    bad2 = (gap.abs() > lim) | (intra.abs() > lim)
    out = pd.DataFrame({"cc": cc_p + div, "cc_p": cc_p, "gap": gap, "div": div, "gap_tr": gap + div, "intra": intra,
                        "o": o, "c": c, "h": d.get("h"), "l": d.get("l"), "v": d.get("v")})
    out.loc[bad | bad2, ["cc", "cc_p", "gap", "gap_tr", "intra"]] = np.nan
    # ardışık eksik gün: önceki kapanış yoksa NaN
    out.loc[cp.isna(), ["cc", "cc_p", "gap", "gap_tr"]] = np.nan
    return out[out.index >= start]

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def nw_t(x, L=5):
    """Newey-West t (Bartlett, L gecikme)."""
    x = pd.Series(x).dropna().values; n = len(x)
    if n < 10: return np.nan
    m = x.mean(); e = x - m
    g0 = (e @ e) / n; s = g0
    for l in range(1, L + 1):
        g = (e[l:] @ e[:-l]) / n; s += 2 * (1 - l / (L + 1)) * g
    return m / np.sqrt(s / n)

def h1(sym):
    h = pd.read_parquet(f"{D}/h1/{sym}.parquet").copy()
    h["ldate"] = pd.to_datetime(h["ldate"]).dt.normalize()
    h["hm"] = h.index.strftime("%H:%M")
    return h
