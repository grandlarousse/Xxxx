"""Saatlik ve 5 dakikalık lead-lag: USDTRY / EURTRY / sepet / gram altın (GC=F x TRY=X) / ons altın  <->  BIST.
Saatlik hizalama: BIST barı (T-60dk, T], T ∈ {08:30..14:30 UTC} (ilk bar = açılış gap'i ve kapanış seansı hariç).
Sürücü penceresi j: (T-30-60j, T+30-60j]  -> j=0 ve j=1 yarı örtüşür; j>=2 sürücü tamamen ÖNDE (>=30 dk boşluk); j<=-1 BIST ÖNDE.
5 dk: aynı ızgara (bar başlangıcı), j adım = 5 dk; j>=1 sürücü önde. Kontroller: hisse_{k-1}, XU100 aynı bar.
Çıktı: res/hourly_ll.csv, res/m5_ll.csv"""
import numpy as np, pandas as pd
import mlib as M, ll
TG = M.BANKS + ["XBANK", "XU100", "XU030", "TRALT", "TRMET", "EREGL", "KRDMD", "FROTO", "TOASO", "ENKAI", "TUPRS", "THYAO", "PGSUS", "ASELS", "SISE",
                "ARCLK", "BIMAS", "MGROS", "EKGYO", "KCHOL", "SAHOL", "TCELL", "TTKOM", "PETKM", "SASA", "GUBRF", "CIMSA", "OYAKC", "TAVHL", "AEFES", "VESTL"]
def bist_h1(sym):
    d = ll.raw(sym if "." in sym else sym + ".IS", "h1"); c = d["c"].astype(float)
    st = d.index; end = st + pd.Timedelta(minutes=60)
    s = pd.Series(c.values, index=end); s = s[(s.index.hour * 60 + s.index.minute >= 7 * 60 + 30) & (s.index.hour * 60 + s.index.minute <= 14 * 60 + 30)]
    s = s[~s.index.duplicated()]
    r = np.log(s).diff(); dn = s.index.normalize(); r[np.r_[True, dn[1:] != dn[:-1]]] = np.nan  # gün başı (07:30 barı) -> sadece referans
    return r.dropna(), s
def drv_px(sym):
    if sym == "XAUTRY":
        a = drv_px("GC=F"); b = drv_px("TRY=X"); j = pd.concat([a, b], axis=1, join="inner").dropna(); return np.exp(np.log(j.iloc[:, 0]) + np.log(j.iloc[:, 1]))
    if sym == "BSK":
        a = drv_px("TRY=X"); b = drv_px("EURTRY=X"); j = pd.concat([a, b], axis=1, join="inner").dropna(); return np.exp(0.5 * (np.log(j.iloc[:, 0]) + np.log(j.iloc[:, 1])))
    d = ll.raw(sym, "h1"); s = pd.Series(d["c"].astype(float).values, index=d.index + pd.Timedelta(minutes=60)); return s[~s.index.duplicated()].sort_index()
def px_at(s, times, maxage=pd.Timedelta(minutes=61)):
    pos = s.index.searchsorted(times, side="right") - 1
    v = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan); t0 = s.index.values[np.clip(pos, 0, None)]
    age = times.values - t0; v[age > maxage.to_timedelta64()] = np.nan; return v
rows = []
xu_r, _ = bist_h1("XU100")
for dsym in ["TRY=X", "EURTRY=X", "BSK", "XAUTRY", "GC=F"]:
    P = drv_px(dsym)
    for s in TG:
        try: r, _ = bist_h1(s)
        except Exception as e: print(s, e); continue
        T = r.index
        dn = T.normalize(); own = r.shift(1).where(np.r_[False, dn[1:] == dn[:-1]])
        m = xu_r.reindex(T)
        for j in [-2, -1, 0, 1, 2, 3]:
            a = px_at(P, T + pd.Timedelta(minutes=30 - 60 * j)); b = px_at(P, T - pd.Timedelta(minutes=30 + 60 * j))
            x = pd.Series(np.log(a) - np.log(b), index=T)
            q = M.ols(r, pd.DataFrame({"x": x, "own": own}), lags=8)
            qm = M.ols(r, pd.DataFrame({"x": x, "own": own, "m": m}), lags=8) if s != "XU100" else None
            df = pd.concat([r, x], axis=1).dropna()
            rows.append({"driver": dsym, "stock": s, "j": j, "corr": df.corr().iloc[0, 1] if len(df) > 50 else np.nan, "n": len(df),
                         "b": q[0]["x"] if q else np.nan, "t": q[1]["x"] if q else np.nan, "tX": qm[1]["x"] if qm else np.nan,
                         "first": str(df.index.min())[:10] if len(df) else ""})
    print(dsym, flush=True)
H = pd.DataFrame(rows); H.to_csv(M.RES + "/hourly_ll.csv", index=False)
# ----- 5 dakika (son ~60 gün) -----
def m5(sym):
    d = ll.raw(sym, "m5"); s = pd.Series(d["c"].astype(float).values, index=d.index); s = s[~s.index.duplicated()].sort_index(); return s
rows = []
P5 = {"TRY=X": m5("TRY=X"), "GC=F": m5("GC=F")}
P5["XAUTRY"] = np.exp(np.log(P5["GC=F"]) + np.log(P5["TRY=X"].reindex(P5["GC=F"].index, method="ffill")))
for s in ["XBANK", "AKBNK", "GARAN", "YKBNK", "ISCTR", "TRALT", "TRMET", "XU100", "XU030", "EREGL", "THYAO", "ENKAI", "TUPRS", "FROTO"]:
    try: b = m5(s + ".IS")
    except Exception as e: print(s, e); continue
    hm = b.index.hour * 60 + b.index.minute; b = b[(hm >= 7 * 60 + 5) & (hm <= 14 * 60 + 50)]
    r = np.log(b).diff(); dn = b.index.normalize(); r[np.r_[True, dn[1:] != dn[:-1]]] = np.nan; r = r.dropna()
    dn = r.index.normalize(); own = r.shift(1).where(np.r_[False, dn[1:] == dn[:-1]])
    for dsym, P in P5.items():
        rp = np.log(P).diff()
        for j in [-3, -2, -1, 0, 1, 2, 3, 6]:
            x = rp.shift(j).reindex(r.index)
            q = M.ols(r, pd.DataFrame({"x": x, "own": own}), lags=12)
            df = pd.concat([r, x], axis=1).dropna()
            rows.append({"driver": dsym, "stock": s, "j5m": j, "corr": df.corr().iloc[0, 1] if len(df) > 50 else np.nan, "n": len(df), "t": q[1]["x"] if q else np.nan})
F = pd.DataFrame(rows); F.to_csv(M.RES + "/m5_ll.csv", index=False)
print(H.pivot_table(index=["driver", "stock"], columns="j", values="t").round(1).to_string())
print(F.pivot_table(index=["driver", "stock"], columns="j5m", values="corr").round(3).to_string())
