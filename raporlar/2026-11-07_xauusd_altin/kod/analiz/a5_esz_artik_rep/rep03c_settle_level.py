"""Dakika verisiyle uzlaşma zamanı (seviye yöntemi): d(m) = log(settle) - log(spot(m)) - carry_hat; carry_hat = ±5 günlük merkezi medyan
(log settle - log p15, aynı kontrat). MAD(d(m)) hangi dakikada minimum? Yıl yıl."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
p15 = snap("XAUUSD", 15).reindex(va.index)
b15 = np.log(va.settle) - np.log(p15)
# aynı kontrat içinde merkezi medyan (kalibrasyon amaçlı; sinyal değil)
carry = b15.groupby(va.code).transform(lambda s: s.rolling(11, center=True, min_periods=5).median())
m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet"); m.index = pd.to_datetime(m.index)
days = sorted(set(m.index.normalize()) & set(va.index))
grid = [(h, mm) for h in (14, 15) for mm in range(0, 60, 5)] + [(16, 0)]
rows = {}
for d in days:
    s = m.loc[d + pd.Timedelta(hours=13, minutes=50): d + pd.Timedelta(hours=16, minutes=1), "c"]
    r = {}
    for h, mm in grid:
        t = d + pd.Timedelta(hours=h, minutes=mm); w = s[:t]
        r[f"{h:02d}:{mm:02d}"] = (np.log(va.at[d, "settle"]) - np.log(w.iloc[-1]) - carry[d]) * 1e4 if len(w) and (t - w.index[-1]) <= pd.Timedelta(minutes=3) else np.nan
    rows[d] = r
R = pd.DataFrame(rows).T
mad = R.abs().groupby(R.index.year).median().round(1)
mad["n"] = R.notna().any(axis=1).groupby(R.index.year).sum()
print("medyan |sapma| bps (yıl × UTC dakika)"); print(mad.to_string())
best = R.abs().groupby(R.index.year).median().idxmin(axis=1); print("yıl başına en iyi dakika:", best.to_dict())

# Sağlamlık: carry referansını 14:00 ve 16:00 görüntüsünden al, kendi günü hariç (leave-one-out) medyan -> referans saatine yanlılık olmasın
for HH in (14, 16):
    pH = snap("XAUUSD", HH).reindex(va.index)
    bH = np.log(va.settle) - np.log(pH)
    def loo(s):
        out = s.copy() * np.nan
        v = s.values
        for i in range(len(v)):
            w = np.r_[v[max(0, i - 5):i], v[i + 1:i + 6]]
            w = w[np.isfinite(w)]
            out.iloc[i] = np.median(w) if len(w) >= 4 else np.nan
        return out
    cH = bH.groupby(va.code).transform(loo)
    rows = {}
    for d in days:
        s = m.loc[d + pd.Timedelta(hours=13, minutes=50): d + pd.Timedelta(hours=16, minutes=1), "c"]
        r = {}
        for h, mm in grid:
            t = d + pd.Timedelta(hours=h, minutes=mm); w = s[:t]
            r[f"{h:02d}:{mm:02d}"] = (np.log(va.at[d, "settle"]) - np.log(w.iloc[-1]) - cH[d]) * 1e4 if len(w) and (t - w.index[-1]) <= pd.Timedelta(minutes=3) else np.nan
        rows[d] = r
    R2 = pd.DataFrame(rows).T
    per = pd.cut(R2.index.year, [2016, 2019, 2022, 2025, 2027], labels=["2017-19", "2020-22", "2023-25", "2026"])
    M = R2.abs().groupby(per).median().round(1)
    print(f"\ncarry ref {HH}:00 (LOO), dönem × dakika medyan |sapma| bps:"); print(M[[c for c in M.columns if c >= "14:40" and c <= "15:30"]].to_string())
    print("en iyi:", M.idxmin(axis=1).to_dict())
