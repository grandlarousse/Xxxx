"""D1 ortak yukleyiciler: ham json -> DataFrame (index = borsa yerel tarihi)."""
import os, json
import numpy as np, pandas as pd

def load_isy_stock(raw, sym):
    v = json.load(open(os.path.join(raw, "isy_hisse", sym + ".json")))["value"]
    d = pd.DataFrame(v)
    d["date"] = pd.to_datetime(d["HGDG_TARIH"], format="%d-%m-%Y")
    out = pd.DataFrame({
        "c_raw": d["HG_KAPANIS"], "h_raw": d["HG_MAX"], "l_raw": d["HG_MIN"], "aof_raw": d["HG_AOF"],
        "c_adj": d["HGDG_KAPANIS"], "h_adj": d["HGDG_MAX"], "l_adj": d["HGDG_MIN"], "aof_adj": d["HGDG_AOF"],
        "vol_tl": d["HG_HACIM"], "mcap_tl": d["PD"], "sermaye": d["SERMAYE"]}).astype(float)
    out.index = d["date"].values
    out = out[~out.index.duplicated(keep="last")].sort_index()
    return out

def load_yahoo(raw, sym):
    res = json.load(open(os.path.join(raw, "yahoo", sym + ".json")))["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose")
    ts = pd.to_datetime(res["timestamp"], unit="s") + pd.Timedelta(seconds=res["meta"].get("gmtoffset", 10800))
    df = pd.DataFrame({"o": q["open"], "h": q["high"], "l": q["low"], "c": q["close"], "adj": adj if adj else q["close"],
                       "v": q["volume"]}, index=ts.normalize()).astype(float)
    df = df.dropna(subset=["c"]); df = df[~df.index.duplicated(keep="last")].sort_index()
    ev = res.get("events", {}) or {}
    def evdf(k, f):
        rows = [((pd.to_datetime(x["date"], unit="s") + pd.Timedelta(hours=3)).normalize(), f(x)) for x in ev.get(k, {}).values()]
        return pd.Series(dict(rows), dtype=float).sort_index()
    splits = evdf("splits", lambda x: x["numerator"] / x["denominator"])
    divs = evdf("dividends", lambda x: x["amount"])
    meta = res["meta"]
    return df, splits, divs, meta

def load_isy_index(raw, code):
    d = json.load(open(os.path.join(raw, "isy_endeks", code + ".json")))["data"]
    s = pd.Series([x[1] for x in d], index=(pd.to_datetime([x[0] for x in d], unit="ms") + pd.Timedelta(hours=3)).normalize(), dtype=float)
    return s[~s.index.duplicated(keep="last")].sort_index()

TICK_CHG = "2023-11-06"   # veriden saptandi: bu tarihten itibaren 250 TL ustu icin 0,25/0,50/1,00/2,50 adimlari; oncesinde >=100 TL icin 0,10

def tick_size(p, dates=None):
    """BIST pay piyasasi fiyat adimi. dates verilirse TICK_CHG oncesi icin eski tablo (>=100 TL: 0,10) kullanilir."""
    p = np.asarray(p, dtype=float)
    new = np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)
    if dates is None: return new
    old = np.select([p < 20, p < 50, p < 100], [0.01, 0.02, 0.05], 0.10)
    return np.where(np.asarray(pd.DatetimeIndex(dates) >= pd.Timestamp(TICK_CHG)), new, old)
