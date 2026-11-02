"""v_YG1_a — BAĞIMSIZ doğrulama ortak modülü (ll.py import EDİLMEZ; tüm temizlik/hizalama burada yeniden yazıldı).

TEMİZLİK KURALLARI (görev metninden, kendim uyguladım):
- Günlük: index = ldate. Bayat gün = hacim 0 VE h==l (seride hacim çoğunlukla >0 ise) -> satır atılır.
- Önceki geçerli satır, BIST takviminde bir önceki iş günü değilse gap/cc NaN (çok günlük gap'i tek gün sanmamak için).
- Kurumsal işlem eşiği (fiyat bazında, rejime bağlı): 2020-03-13 öncesi oran (0,795 ; 1,205) dışı, sonrası (0,895 ; 1,105) dışı -> NaN.
  Hem düzeltilmiş (adj) cc hem ham c/c_{-1} hem de gap için uygulanır.
- gap = cc_adj − intra  (temettü düzeltmesi gap'e değil düzeltmeye gider);  intra = ln(c/o).
- Bozuk açılış: o<=0, o NaN, o [l,h] dışı, (h==l ve o==c_{-1}) -> intra/gap NaN. 2014 öncesi atılır (Yahoo açılışı bozuk).
- Not (bu ajanın kontrolü): 2014–2015'te o==c oranı (medyan %10–14) c==c_{-1} oranının (%6–7) belirgin üstünde -> açılış verisi
  2014–15'te hâlâ kısmen bozuk; 2016+ ile dayanıklılık testi yapılır.
- Yahoo c bölünme/bedelsiz düzeltmeli (SASA 2012 c=0,006) -> tarihsel nominal fiyat yok; tik maliyeti GÜNCEL fiyatla hesaplanır.
SAATLİK: bar etiketi = bar başlangıcı (UTC). 06:30 barı = 09:30–10:30 TSİ; o = günlük açılış müzayedesi fiyatı (%99,7),
  h/l AÇILIŞ FİYATINI İÇERİR (h>=O, l<=O %100). c = 10:30 TSİ fiyatı. 13:30 barı c = 17:30 TSİ. 14:30 barı yalnız yazın.
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
DATA = SCR + "/data"; OUT = SCR + "/out"; CODE = OUT + "/code_v_YG1_a"; RES = CODE + "/res"
os.makedirs(RES, exist_ok=True)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
SWITCH = pd.Timestamp("2020-03-13")
SPLIT = pd.Timestamp("2021-01-01")


def read_daily(sym):
    d = pd.read_parquet(f"{DATA}/daily/{sym}.IS.parquet")
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"].values)).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d[["o", "h", "l", "c", "adj", "v"]].astype(float)


_CAL = None
def cal():
    global _CAL
    if _CAL is None:
        d = read_daily("XU100")
        if (d["v"].fillna(0) > 0).mean() > 0.5: d = d[d["v"].fillna(0) > 0]
        _CAL = d.index
    return _CAL


def bad_ratio(lr, idx):
    pre = np.asarray(idx < SWITCH)
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    return (lr > up) | (lr < dn)


def decomp(sym, start="2014-01-01"):
    """DataFrame: o,c,cc,gap,gap_raw,intra (index BIST günleri, start sonrası)."""
    d = read_daily(sym)
    if (d["v"].fillna(0) > 0).mean() > 0.5:
        stale = (d["v"].fillna(0) <= 0) & (d["h"] == d["l"])
        d = d[~stale]
    d = d[(d["c"] > 0) & (d["adj"] > 0)]
    C = cal(); pos = C.get_indexer(d.index)
    prev_ok = pd.Series(pos, index=d.index).diff() == 1  # bir önceki BIST iş günü de geçerli satır
    pc = d["c"].shift(1); padj = d["adj"].shift(1)
    cc = np.log(d["adj"] / padj); ccraw = np.log(d["c"] / pc)
    intra = np.log(d["c"] / d["o"])
    bad_open = (d["o"] <= 0) | d["o"].isna() | (d["o"] > d["h"] * 1.0005) | (d["o"] < d["l"] * 0.9995) | ((d["h"] == d["l"]) & (d["o"] == pc))
    intra[bad_open] = np.nan
    gap = cc - intra; gap_raw = np.log(d["o"] / pc)
    out = pd.DataFrame({"o": d["o"], "c": d["c"], "v": d["v"], "cc": cc, "gap": gap, "gap_raw": gap_raw, "intra": intra})
    bad = (~prev_ok) | bad_ratio(cc, d.index) | bad_ratio(ccraw, d.index) | bad_ratio(gap, d.index).fillna(False) | bad_ratio(gap_raw, d.index).fillna(False)
    out.loc[bad.values, ["cc", "gap", "gap_raw", "intra"]] = np.nan
    out.loc[out["gap"].isna(), "intra"] = np.nan
    out["oc_eq"] = (d["o"] == d["c"]).values
    out["turn"] = d["c"] * d["v"]
    return out[out.index >= start]


def h1_panel(sym):
    """Gün bazında saatlik fiyat noktaları. O = günlük açılış (06:30 bar o'su ile %99,7 aynı)."""
    h = pd.read_parquet(f"{DATA}/h1/{sym}.IS.parquet"); h = h[~h.index.duplicated(keep="last")].sort_index()
    day = pd.DatetimeIndex(h.index.tz_convert(None)).normalize(); hm = h.index.hour * 100 + h.index.minute
    df = pd.DataFrame({"d": day, "hm": hm, "o": h["o"].values, "h": h["h"].values, "l": h["l"].values, "c": h["c"].values, "v": h["v"].values})
    out = {}
    for f in ["o", "h", "l", "c", "v"]:
        out[f] = df.pivot_table(index="d", columns="hm", values=f, aggfunc="last")
    nb = df.groupby("d").size()
    P = pd.DataFrame(index=out["c"].index)
    P["h1_o"] = out["o"].get(630)
    P["P0730"] = out["c"].get(630)                      # 10:30 TSİ son fiyat
    P["TP1"] = (out["h"].get(630) + out["l"].get(630) + out["c"].get(630)) / 3   # kaynak ajanın E2 vekili (açılış fiyatını içerir)
    P["H1"] = out["h"].get(630); P["L1"] = out["l"].get(630)
    P["P0830"] = out["c"].get(730)                      # 11:30 TSİ
    P["TP2"] = (out["h"].get(730) + out["l"].get(730) + out["c"].get(730)) / 3   # 10:30–11:30 TSİ tipik fiyat (müzayedeyi içermez)
    P["P1430"] = out["c"].get(1330)                     # 17:30 TSİ (yıl boyu)
    P["P1500"] = out["c"].get(1430) if 1430 in out["c"] else np.nan   # 18:00 TSİ (yalnız yaz)
    P["nbars"] = nb
    P["half"] = nb <= 6
    return P


def nw_mean(x, lags=5):
    """Ortalama ve Newey–West (Bartlett) t. NaN atılır."""
    x = np.asarray(pd.Series(x).dropna(), float); n = len(x)
    if n < 20: return np.nan, np.nan, n
    m = x.mean(); u = x - m
    s = u @ u / n
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1); s += 2 * w * (u[k:] @ u[:-k]) / n
    se = np.sqrt(s / n)
    return m, (m / se if se > 0 else np.nan), n


def bh(p, q=0.05):
    p = np.asarray(p, float); n = np.sum(~np.isnan(p)); rej = np.zeros(len(p), bool); padj = np.full(len(p), np.nan)
    ok = ~np.isnan(p); pv = p[ok]; o = np.argsort(pv); r = np.arange(1, len(pv) + 1)
    adj = np.minimum.accumulate((pv[o] * n / r)[::-1])[::-1]; adj = np.minimum(adj, 1)
    pa = np.empty_like(pv); pa[o] = adj; padj[ok] = pa; rej[ok] = pa <= q
    return rej, padj


def t2p(t):
    from scipy import stats
    return 2 * (1 - stats.norm.cdf(np.abs(np.asarray(t, float))))


def tick_ssf(p):
    return 0.01 * np.ones_like(np.asarray(p, float))
