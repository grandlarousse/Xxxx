"""Zaman damgası kontrolü: VİOP XAUUSD/USDTRY uzlaşması hangi UTC saatine karşılık geliyor? Yahoo TRY=X günlük hangi gün?"""
import numpy as np, pandas as pd, cl
def snap_h(sym, hh, mm=0):
    d = pd.read_parquet(f"{cl.S}/data/h1/{sym}.parquet"); d = d[~d.index.duplicated(keep="last")].sort_index()
    end = d.index + pd.Timedelta(minutes=60)
    s = pd.Series(d["c"].values, index=end)
    s = s[s > 0]
    days = pd.date_range(s.index[0].normalize(), s.index[-1].normalize(), freq="D", tz="UTC")
    tg = days + pd.Timedelta(hours=hh, minutes=mm)
    pos = np.searchsorted(s.index.values, tg.values, side="right") - 1
    v = s.values[np.clip(pos, 0, None)]; age = (tg.values - s.index.values[np.clip(pos, 0, None)]) / np.timedelta64(1, "h")
    v = np.where((pos >= 0) & (age < 30), v, np.nan)
    return pd.Series(v, index=days.tz_convert(None))
c = cl.cal()
for und, sym in [("XAUUSD", "GC=F"), ("USDTRY", "TRY=X")]:
    f = cl.front(und)["ret"].reindex(c)
    rows = []
    for hh in [9, 11, 12, 13, 14, 15, 16, 17, 19]:
        s = snap_h(sym, hh).reindex(c); r = np.log(s).diff()
        df = pd.concat([f, r], axis=1).dropna(); df = df[df.index >= "2024-07-01"]
        rows.append((f"{hh}:00", len(df), round(df.corr().iloc[0, 1], 3)))
    print(und, "VİOP uzlaşma getirisi ~ hourly snap(t,HH)-snap(t-1,HH) korelasyonu:", rows)
# TRY=X günlük ldate hizası
f = cl.front("USDTRY")["ret"]
y = cl.lret("TRY=X", "c")
for lag in [-1, 0, 1]:
    df = pd.concat([f, y.shift(-lag)], axis=1).dropna(); df = df[df.index >= "2019-01-01"]
    print("TRY=X günlük lag", lag, "(yahoo(t+lag) ~ viop(t)) corr", round(df.corr().iloc[0, 1], 3), len(df))
# ABD günlük: VLO günlük ldate getirisinin saatlik 20:00/21:00 snap ile eşleşmesi
y = cl.lret("VLO", "c")
for hh in [15, 21]:
    s = snap_h("VLO", hh); r = np.log(s.dropna()).diff()
    df = pd.concat([y, r], axis=1).dropna(); print("VLO günlük ~ saatlik snap", hh, round(df.corr().iloc[0, 1], 3), len(df))
# ASX günlük: FMG.AX ldate getirisi ~ saatlik 06:00 UTC snap
y = cl.lret("FMG.AX", "c")
for hh in [6, 23]:
    s = snap_h("FMG.AX", hh); r = np.log(s.dropna()).diff()
    df = pd.concat([y, r], axis=1).dropna(); print("FMG.AX günlük ~ saatlik snap", hh, round(df.corr().iloc[0, 1], 3), len(df))
