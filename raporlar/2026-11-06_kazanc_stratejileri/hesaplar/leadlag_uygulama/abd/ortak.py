"""ABD Tier-A lead-lag uygulama testleri: ortak veri ve istatistik araclari.

Veri (repo DISINDA, scratchpad):
  - Ken French 49 sektor gunluk VW + FF3 gunluk (CRSP 202609; son gun 2026-09-30)
      .../scratchpad/data/dalga_abd/raw/ (onceki ajan indirdi; ayni kaynak)
  - FRED: DGS10, DCOILWTICO, VIXCLS, DTWEXBGS (varsayilan baslik, fredgraph.csv)
      .../scratchpad/data/leadlag2/abd/fred/
  - CBOE VIX gunluk: .../scratchpad/data/cboe_VIX.csv
Zamanlama: tum seriler ABD islem gunu t'ye hizali. Sinyal ABD kapanisi t'de bilinir
(= TSI t+1 gunu 23:00/00:00). Kullanicinin en erken islemi ABD acilisi t+1 (17:30 TSI).
Yahoo / Stooq KULLANILMADI.
"""
import io, os
import numpy as np
import pandas as pd
import statsmodels.api as sm

SP = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data"
RAW_FF = os.path.join(SP, "dalga_abd", "raw")
D2 = os.path.join(SP, "leadlag2", "abd")
CIKTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
os.makedirs(D2, exist_ok=True)
os.makedirs(CIKTI, exist_ok=True)


def _sections(path):
    with open(path, "r", encoding="latin-1") as f:
        lines = f.read().splitlines()
    out, i, n = {}, 0, len(lines)
    while i < n:
        ln = lines[i]
        if i + 1 < n and lines[i + 1].startswith(",") and ln.strip() and not ln.startswith(","):
            title, hdr = ln.strip(), i + 1
        elif ln.startswith(",") and i + 1 < n and lines[i + 1].split(",")[0].strip().isdigit():
            title, hdr = "main%d" % i, i
        else:
            i += 1
            continue
        cols = [c.strip() for c in lines[hdr].split(",")[1:]]
        j, rows = hdr + 1, []
        while j < n and lines[j].strip() and lines[j].split(",")[0].strip().isdigit():
            rows.append(lines[j]); j += 1
        if rows:
            df = pd.read_csv(io.StringIO("\n".join(rows)), header=None)
            df.columns = ["date"] + cols
            df = df.set_index("date").replace([-99.99, -999.0, -999], np.nan)
            out[title] = df
        i = j
    return out


def load_panel(start="2008-01-01"):
    """Gunluk getiriler (ondalik). Kolonlar: 49 sektor, MKT, SMB, RF, VIX, DGS10, WTI."""
    p = os.path.join(D2, "panel.pkl")
    if os.path.exists(p):
        return pd.read_pickle(p)
    s = _sections(os.path.join(RAW_FF, "49_Industry_Portfolios_Daily.csv"))
    vw = s["Average Value Weighted Returns -- Daily"].copy()
    vw.index = pd.to_datetime(vw.index.astype(str), format="%Y%m%d")
    ff = list(_sections(os.path.join(RAW_FF, "F-F_Research_Data_Factors_daily.csv")).values())[0]
    ff.index = pd.to_datetime(ff.index.astype(str), format="%Y%m%d")
    df = vw / 100.0
    df["MKT"] = (ff["Mkt-RF"] + ff["RF"]) / 100.0
    df["SMB"] = ff["SMB"] / 100.0
    df["RF"] = ff["RF"] / 100.0
    df = df[df.index >= start]
    # CBOE VIX kapanisi
    v = pd.read_csv(os.path.join(SP, "cboe_VIX.csv"))
    v.index = pd.to_datetime(v["DATE"], format="%m/%d/%Y")
    df["VIX"] = v["CLOSE"].reindex(df.index)
    for sid, col in [("DGS10", "DGS10"), ("DCOILWTICO", "WTI")]:
        f = pd.read_csv(os.path.join(D2, "fred", sid + ".csv"))
        f.index = pd.to_datetime(f.iloc[:, 0])
        x = pd.to_numeric(f.iloc[:, 1], errors="coerce")
        df[col] = x.reindex(df.index)  # tatil/eksik gun -> NaN (degisim de NaN)
    pd.to_pickle(df, p)
    return df


def roll_beta(r, m, w=252):
    """t'ye kadar (t dahil) bilinen kayan beta."""
    cov = r.rolling(w, min_periods=200).cov(m)
    var = m.rolling(w, min_periods=200).var()
    return cov / var


def resid(df, col, w=252):
    b = roll_beta(df[col], df["MKT"], w)
    return df[col] - b * df["MKT"], b


def zroll(x, w=252):
    mu = x.rolling(w, min_periods=200).mean()
    sd = x.rolling(w, min_periods=200).std()
    return (x - mu) / sd


def fwd_sum(x, h, skip=0):
    """t+1+skip .. t+h+skip toplam (t'de bilinmez; hedef)."""
    a = x.shift(-1 - skip)
    out = a.copy()
    for k in range(2, h + 1):
        out = out + x.shift(-k - skip)
    return out


def hac_ols(y, x, lags):
    d = pd.concat([y, x], axis=1).dropna()
    if len(d) < 300:
        return np.nan, np.nan, np.nan, len(d)
    X = sm.add_constant(d.iloc[:, 1].values)
    r = sm.OLS(d.iloc[:, 0].values, X).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return r.params[1], r.tvalues[1], r.pvalues[1], len(d)


def bh(p, q=0.10):
    """Benjamini-Hochberg: reddedilenler (bool) ve q-degerleri."""
    p = np.asarray(p, float)
    n = np.sum(~np.isnan(p))
    order = np.argsort(np.where(np.isnan(p), 2, p))
    ranked = np.where(np.isnan(p), np.nan, p)[order]
    qv = ranked * n / (np.arange(len(p)) + 1)
    qv = np.minimum.accumulate(qv[::-1])[::-1]
    out = np.empty(len(p)); out[order] = qv
    out = np.minimum(out, 1.0)
    return out <= q, out
