"""v_G3_b ortak modül (BAĞIMSIZ: ll.py ve code_v_G3_a import EDİLMEZ).
- Yahoo günlük: data/daily/<SYM>.parquet (ldate = işlem günü). gap = ln(o_t/c_{t-1}), intra = ln(c_t/o_t).
- Temizlik (benim): |ln(c_t/c_{t-1})|>ln1.105 -> gün NaN; |gap|>ln1.105 veya |intra|>ln1.105 -> NaN; o<=0, o l/h dışı -> NaN.
  Hisselerde temettü: adj/c oranından gap'e geri eklenir (gap_tr). Endekste adj==c.
- İş Yatırım saatlik (data/isy/h1): etiket HH:00 = saatin SON fiyatı = (HH+1):00 UTC anlık değeri (m5 ile doğruladım: 07:00 etiketi = m5 07:55 bar kapanışı).
- VİOP bülteni: kendi ayrıştırıcım (cp1254, ';'), yalnız F_ vadeli satırları.
"""
import os, glob, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/data"; OUT = S + "/out/code_v_G3_b"; RES = OUT + "/res"
os.makedirs(RES, exist_ok=True)
LIM = np.log(1.105)
STOCKS = ("AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF "
          "HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO "
          "TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK").split()
BPS = 1e4


def yahoo(sym):
    d = pd.read_parquet(f"{D}/daily/{sym}.parquet")
    d = d.set_index(pd.to_datetime(d["ldate"]).dt.normalize()).drop(columns="ldate")
    d = d[~d.index.duplicated(keep="last")].sort_index()
    return d


def decomp(sym, clean=True, start="2005-01-01"):
    d = yahoo(sym)
    d = d[d.c > 0]
    out = pd.DataFrame(index=d.index)
    cp = d.c.shift(1)
    out["cc"] = np.log(d.c / cp)
    out["gap"] = np.log(d.o / cp)
    out["intra"] = np.log(d.c / d.o)
    # temettü bileşeni (hisseler): adj/c oranı değişimi
    if "adj" in d:
        f = (d.adj / d.c)
        out["div"] = np.log(f / f.shift(1)).fillna(0.0).clip(-0.2, 0.2)
        out.loc[out["div"].abs() < 1e-6, "div"] = 0.0
    else:
        out["div"] = 0.0
    out["gap_tr"] = out.gap + out["div"]
    out["o"] = d.o; out["c"] = d.c; out["h"] = d.h; out["l"] = d.l; out["v"] = d.v
    out["stale_open"] = (d.o == cp)
    if clean:
        bad = (out.cc.abs() > LIM) | (out.gap.abs() > LIM) | (out.intra.abs() > LIM) | (d.o <= 0)
        bad |= (d.o > d.h * (1 + 1e-6)) | (d.o < d.l * (1 - 1e-6))
        out.loc[bad, ["cc", "gap", "intra", "gap_tr"]] = np.nan
        out["bad"] = bad
    return out[out.index >= start]


def isy_h1(code):
    x = pd.read_parquet(f"{D}/isy/h1/{code}.parquet").px
    x.index = pd.to_datetime(x.index)  # UTC naive, etiket = saat başlangıcı, değer = saat sonu
    return x


def isy_d(code):
    d = pd.read_parquet(f"{D}/isy/d/{code}.parquet")
    return d.set_index(pd.to_datetime(d.ldate).dt.normalize()).px


# ---------------- VİOP ----------------
VCOLS = {0: "date", 1: "code", 4: "seg", 7: "und", 8: "exp", 9: "settle", 10: "psettle", 12: "open", 13: "low",
         14: "high", 15: "close", 16: "vwap", 17: "val", 19: "qty", 20: "ntr", 21: "oi", 23: "os_px", 24: "os_val",
         26: "os_qty", 27: "os_ntr"}


def viop_parse(force=False):
    p = RES + "/viop_fut_b.parquet"
    if os.path.exists(p) and not force:
        return pd.read_parquet(p)
    rows = []
    for f in sorted(glob.glob(f"{D}/viop/viop_*.csv")):
        try:
            with open(f, "rb") as fh:
                txt = fh.read().decode("cp1254", errors="replace").splitlines()
        except Exception:
            continue
        for ln in txt[2:]:
            if not ln.startswith("20"):
                continue
            a = ln.split(";")
            if len(a) < 23 or not a[1].startswith("F_"):
                continue
            if a[4] not in ("INF", "SSF"):
                continue
            r = {k: (a[i] if i < len(a) else "") for i, k in VCOLS.items()}
            rows.append(r)
    df = pd.DataFrame(rows)
    for c in df.columns:
        if c not in ("date", "code", "seg", "und", "exp"):
            df[c] = pd.to_numeric(df[c].replace("", np.nan), errors="coerce")
    df["date"] = pd.to_datetime(df["date"]); df["exp"] = pd.to_datetime(df["exp"])
    df.to_parquet(p)
    return df


def front(df, und, rule="vol"):
    """Tek dayanak için günlük ön vade. rule='vol': en çok işlem miktarlı; 'next': vade>tarih olan en yakın."""
    x = df[(df.und == und)].copy()
    x = x[x.close.notna() & x.open.notna() & (x.qty > 0)]
    if rule == "next":
        x = x[x.exp > x.date].sort_values(["date", "exp"]).groupby("date").head(1)
    else:
        x = x.sort_values(["date", "qty"], ascending=[True, False]).groupby("date").head(1)
    return x.set_index("date").sort_index()


def fut_series(df, und, rule="next"):
    """Aynı sözleşme ile f_gap (ACILIS/önceki UZLAŞMA), f_gapc (ACILIS/önceki gün aynı sözleşme KAPANIS), f_intra."""
    fr = front(df, und, rule)
    allx = df[df.und == und].set_index(["date", "code"]).sort_index()
    dates = fr.index
    prev_close = []
    prev_dates = pd.Series(dates).shift(1).values
    for d, code, pdt in zip(dates, fr.code.values, prev_dates):
        if pd.isna(pdt):
            prev_close.append(np.nan); continue
        try:
            prev_close.append(allx.loc[(pdt, code), "close"])
        except KeyError:
            prev_close.append(np.nan)
    fr["pclose_same"] = prev_close
    fr["f_gap"] = np.log(fr.open / fr.psettle)
    fr["f_gapc"] = np.log(fr.open / fr.pclose_same)
    fr["f_intra"] = np.log(fr.close / fr.open)
    fr["f_intra_u"] = np.log(fr.settle / fr.open)
    fr["f_o2vw"] = np.log(fr.vwap / fr.open)
    fr["f_vw2c"] = np.log(fr.close / fr.vwap)
    fr["f_cc"] = np.log(fr.settle / fr.psettle)
    return fr


# ---------------- istatistik ----------------
def nw_t(x, L=5):
    x = pd.Series(x).dropna().values
    n = len(x)
    if n < 10:
        return np.nan
    m = x.mean(); e = x - m
    g0 = (e @ e) / n
    s = g0
    for l in range(1, L + 1):
        g = (e[l:] @ e[:-l]) / n
        s += 2 * (1 - l / (L + 1)) * g
    return m / np.sqrt(s / n)


def st(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3:
        return dict(n=n, mean=np.nan, t=np.nan, nwt=np.nan, med=np.nan, pos=np.nan, sd=np.nan)
    return dict(n=n, mean=x.mean() * BPS, t=x.mean() / x.std() * np.sqrt(n), nwt=nw_t(x), med=x.median() * BPS,
                pos=(x > 0).mean(), sd=x.std() * BPS)


def by_year(df, cols):
    out = []
    for y, g in df.groupby(df.index.year):
        r = {"year": y}
        for c in cols:
            s = st(g[c]); r[c] = s["mean"]; r[c + "_t"] = s["t"]; r["n"] = s["n"]
        out.append(r)
    return pd.DataFrame(out).set_index("year")


def block_boot(x, block="Y", B=5000, seed=1):
    """Yıl (veya ay) blok bootstrap: ortalama %95 GA ve P(ort<=0)."""
    x = pd.Series(x).dropna()
    key = x.index.year if block == "Y" else x.index.to_period("M")
    groups = [g.values for _, g in x.groupby(key)]
    rng = np.random.default_rng(seed)
    k = len(groups)
    sums = np.array([g.sum() for g in groups]); ns = np.array([len(g) for g in groups])
    idx = rng.integers(0, k, size=(B, k))
    m = sums[idx].sum(1) / ns[idx].sum(1)
    return np.percentile(m, 2.5) * BPS, np.percentile(m, 97.5) * BPS, (m <= 0).mean()


def fmt(d, keys=("n", "mean", "t", "nwt", "med", "pos")):
    return " ".join(f"{k}={d[k]:.2f}" if isinstance(d[k], float) else f"{k}={d[k]}" for k in keys)
