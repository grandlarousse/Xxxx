"""Bilinen Türkiye arife/yarım gün tarihlerinde VİOP uzlaşmasının hangi UTC saatine denk geldiğini kontrol et.
Ölçü: |log(settle) − log(spot_H) − referans baz| (bps); referans baz = önceki ve sonraki 5 günün 15:00 bazının medyanı."""
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
v = pd.read_parquet(f"{OUT}/base_viop.parquet")
h = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet").c; h.index = h.index + pd.Timedelta(hours=1)
def at(dts, H):
    t = pd.DatetimeIndex(dts).tz_localize("UTC") + pd.Timedelta(hours=H)
    i = h.index.searchsorted(t, side="right") - 1
    age = (t.values - h.index.values[np.clip(i, 0, None)]) / np.timedelta64(1, "h")
    return pd.Series(np.where((i >= 0) & (age <= 1), h.values[np.clip(i, 0, None)], np.nan), index=pd.DatetimeIndex(dts))
D = pd.DataFrame({H: np.log(v.settle) - np.log(at(v.index, H)) for H in range(7, 18)})
ref = pd.concat([D[15].shift(k) for k in (-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)], axis=1).median(axis=1)
E = D.sub(ref, axis=0).abs() * 1e4
known = ["2017-06-23", "2017-08-31", "2018-06-14", "2018-08-20", "2018-10-29", "2018-12-31", "2019-06-03", "2019-08-09", "2019-10-28", "2019-12-31",
         "2020-05-22", "2020-07-30", "2020-10-28", "2020-12-31", "2021-05-12", "2021-07-19", "2021-10-28", "2021-12-31", "2022-04-29", "2022-07-08",
         "2022-10-28", "2022-12-30", "2023-04-20", "2023-06-27", "2023-12-29", "2024-04-09", "2024-06-14", "2024-10-28", "2024-12-31", "2025-03-28",
         "2025-06-05", "2025-10-28", "2025-12-31", "2026-03-19", "2026-05-26", "2026-10-28"]
k = [pd.Timestamp(x) for x in known if pd.Timestamp(x) in E.index]
T = E.loc[k].round(1); T["best_H"] = E.loc[k].idxmin(axis=1); T["vol"] = v.volume.reindex(k)
T["vol_med20"] = v.volume.rolling(20).median().reindex(k)
pd.set_option("display.width", 250); print(T.to_string())
# Resmi yarım günler (Ramazan/Kurban arifesi ve 28 Ekim; hafta içine denk gelenler). 31 Aralık yarım gün DEĞİL.
official = ["2017-08-31", "2018-06-14", "2018-08-20", "2019-06-03", "2019-10-28", "2020-07-30", "2020-10-28", "2021-05-12", "2021-07-19", "2021-10-28",
            "2022-07-08", "2022-10-28", "2023-04-20", "2023-06-27", "2024-04-09", "2024-10-28", "2025-06-05", "2025-10-28", "2026-03-19", "2026-05-26", "2026-10-28"]
off = [pd.Timestamp(x) for x in official if pd.Timestamp(x) in v.index]
X = T.loc[[x for x in off if x in T.index]]
print("resmi yarım gün sayısı (VİOP endeksinde):", len(off))
print("bunlarda hacim / 20g medyan oranı medyanı:", round(float((X.vol / X.vol_med20).median()), 2), " | E15 medyan bps:", float(X[15].median()), " min(E9..E12) medyan:", float(X[[9, 10, 11, 12]].min(axis=1).median()))
print("diğer günlerde E15 medyan bps:", float(E[15].drop(off, errors="ignore").median()), " min(E9..E12) medyan:", float(E[[9, 10, 11, 12]].drop(off, errors="ignore").min(axis=1).median()))
pd.Series(1, index=pd.DatetimeIndex(off), name="halfday").to_frame().to_parquet(f"{OUT}/halfday_flag.parquet")
