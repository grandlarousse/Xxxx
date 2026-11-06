"""Ortak yardimcilar: veri okuma (Ken French, FRED, Chen-Zimmermann) ve performans istatistikleri.

Ham veri: scratchpad/data altinda (repo disinda). Bu modul sadece okur.
"""
import os
import re
import numpy as np
import pandas as pd

DATA = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data"
FR = os.path.join(DATA, "french", "x")
FRED = os.path.join(DATA, "fred")
CZ = os.path.join(DATA, "cz")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------- French
def french_sections(fname):
    """French CSV dosyasini bolumlerine ayirir -> [(baslik, DataFrame)]. Degerler % cinsinden."""
    lines = open(os.path.join(FR, fname), encoding="latin-1").read().splitlines()
    out, i, title = [], 0, ""
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith(",") or (ln.strip() and ln.split(",")[0].strip() == "" and "," in ln):
            cols = [c.strip() for c in ln.split(",")[1:]]
            rows = []
            j = i + 1
            while j < len(lines) and lines[j].strip() and re.match(r"^\s*\d", lines[j]):
                parts = [p.strip() for p in lines[j].split(",")]
                rows.append(parts)
                j += 1
            if rows:
                idx = [r[0] for r in rows]
                vals = np.array([[float(x) if x not in ("",) else np.nan for x in r[1:len(cols) + 1]] for r in rows])
                df = pd.DataFrame(vals, index=idx, columns=cols)
                df = df.replace([-99.99, -999.0], np.nan)
                out.append((title, df))
            i = j
            continue
        if ln.strip():
            title = ln.strip()
        i += 1
    return out


def _to_monthly_index(df):
    df = df[[len(x) == 6 for x in df.index]].copy()
    df.index = pd.to_datetime(df.index, format="%Y%m") + pd.offsets.MonthEnd(0)
    return df


def _to_daily_index(df):
    df = df[[len(x) == 8 for x in df.index]].copy()
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    return df


def french_monthly(fname, section=0):
    secs = [s for s in french_sections(fname) if len(s[1].index[0]) == 6]
    return _to_monthly_index(secs[section][1]) / 100.0, secs[section][0]


def french_daily(fname, section=0):
    secs = [s for s in french_sections(fname) if len(s[1].index[0]) == 8]
    return _to_daily_index(secs[section][1]) / 100.0, secs[section][0]


# ---------------------------------------------------------------- FRED
def fred(series):
    df = pd.read_csv(os.path.join(FRED, series + ".csv"))
    df.columns = ["date", series]
    df["date"] = pd.to_datetime(df["date"])
    df[series] = pd.to_numeric(df[series], errors="coerce")
    return df.set_index("date")[series]


# ---------------------------------------------------------------- istatistik
def stats(r, rf=None, ppy=12):
    """r: periyodik basit getiri serisi (ondalik). rf: ayni frekansta risksiz getiri."""
    r = r.dropna()
    if len(r) < 3:
        return {}
    nav = (1 + r).cumprod()
    yrs = len(r) / ppy
    cagr = nav.iloc[-1] ** (1 / yrs) - 1 if nav.iloc[-1] > 0 else -1.0
    vol = r.std() * np.sqrt(ppy)
    if rf is not None:
        rfa = rf.reindex(r.index).fillna(0)
        ex = r - rfa
        rf_cagr = (1 + rfa).prod() ** (1 / yrs) - 1
    else:
        ex = r
        rf_cagr = 0.0
    sharpe = ex.mean() / r.std() * np.sqrt(ppy) if r.std() > 0 else np.nan
    peak = nav.cummax()
    mdd = (nav / peak - 1).min()
    yr = (1 + r).groupby(r.index.year).prod() - 1
    # tam olmayan ilk/son yillari da gosteriyoruz; en kotu yil tum takvim yillari icinden
    worst = yr.min()
    return dict(CAGR=cagr, Vol=vol, Sharpe=sharpe, MaxDD=mdd, EnKotuYil=worst,
                EnKotuYilT=int(yr.idxmin()), ExcessCAGR=cagr - rf_cagr, N=len(r))


def fmt_pct(x, d=1):
    return "" if pd.isna(x) else f"{100 * x:.{d}f}%"


def stats_table(series_dict, rf, ppy, periods):
    """series_dict: {ad: getiri serisi}; periods: [(etiket, bas, son)] -> markdown satirlari listesi."""
    rows = []
    for lab, a, b in periods:
        for name, r in series_dict.items():
            rr = r.loc[a:b]
            s = stats(rr, rf.loc[a:b] if rf is not None else None, ppy)
            if not s:
                continue
            rows.append(dict(Donem=lab, Strateji=name, **s))
    return pd.DataFrame(rows)


def md_table(df, pct_cols=("CAGR", "Vol", "MaxDD", "EnKotuYil", "ExcessCAGR"), num_cols=("Sharpe",), drop=("N",)):
    df = df.copy()
    for c in drop:
        if c in df:
            df = df.drop(columns=c)
    for c in df.columns:
        if c in pct_cols:
            df[c] = df[c].map(lambda x: fmt_pct(x))
        elif c in num_cols:
            df[c] = df[c].map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)
