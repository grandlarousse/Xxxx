import numpy as np, pandas as pd, cl
def snap_h(sym, hh=15, mm=0, max_age_h=30):
    """UTC günü için hh:mm'de BİLİNEN son fiyat = bitiş zamanı (başlangıç+60dk) <= hh:mm olan son barın kapanışı."""
    d = pd.read_parquet(f"{cl.S}/data/h1/{sym}.parquet"); d = d[~d.index.duplicated(keep="last")].sort_index()
    s = pd.Series(d["c"].values, index=d.index + pd.Timedelta(minutes=60)); s = s[s > 0]
    days = pd.date_range(s.index[0].normalize(), s.index[-1].normalize(), freq="D", tz="UTC")
    tg = days + pd.Timedelta(hours=hh, minutes=mm)
    pos = np.searchsorted(s.index.values, tg.values, side="right") - 1
    v = s.values[np.clip(pos, 0, None)]; age = (tg.values - s.index.values[np.clip(pos, 0, None)]) / np.timedelta64(1, "h")
    v = np.where((pos >= 0) & (age < max_age_h), v, np.nan)
    return pd.Series(v, index=days.tz_convert(None))
def r_snap(sym, hh=15, mm=0, c=None):
    c = cl.cal() if c is None else c
    s = snap_h(sym, hh, mm); s = s.reindex(c); r = np.log(s).diff()
    first = s.first_valid_index(); r[r.index <= first] = np.nan
    return r
