"""Aday 6: kredi notu kademe kararı -> tepki günü uzlaşmasında ters yön, 2 gün (F_XU030). Kendi olay listem (kademe değişiklikleri, 2017-03+)."""
import numpy as np, pandas as pd, cl, ev
EV = [("2018-03-07", "MOODYS", -1), ("2018-05-01", "SP", -1), ("2018-07-13", "FITCH", -1), ("2018-08-17", "SP+MOODYS", -1), ("2019-06-14", "MOODYS", -1),
      ("2019-07-12", "FITCH", -1), ("2020-09-11", "MOODYS", -1), ("2022-07-08", "FITCH", -1), ("2022-08-12", "MOODYS", -1), ("2022-09-30", "SP", -1),
      ("2024-03-08", "FITCH", 1), ("2024-05-03", "SP", 1), ("2024-07-19", "MOODYS", 1), ("2024-09-06", "FITCH", 1), ("2024-11-01", "SP", 1), ("2025-07-25", "MOODYS", 1)]
c = cl.cal(); r = ev.R("XU030")
rows = []
for d, ag, dr in EV:
    k = np.searchsorted(c.values, np.datetime64(d), side="right")  # açıklama BIST kapanışından sonra -> ilk işlem günü > d
    t0 = c[k]
    rr = r.reindex(c)
    react = rr.iloc[k] * 1e4
    h = {hh: rr.iloc[k + 1:k + 1 + hh].sum() * 1e4 for hh in (1, 2, 3)}
    rows.append(dict(ann=d, react=t0.date(), agency=ag, dir=dr, react_ret=round(react, 0), **{f"h{hh}": round(-dr * v, 0) for hh, v in h.items()}))
E = pd.DataFrame(rows); print(E.to_string())
for hh in (1, 2, 3):
    x = E[f"h{hh}"]; print(f"h{hh}: ort {x.mean():.0f} t {cl.tstat(x):.2f} isabet {(x > 0).mean():.2f} n {len(x)}; net8 {x.mean() - 8:.0f}; medyan {x.median():.0f}")
# tepki gününde beklenen yönde hareket var mı? (düşürme -> düşüş)
print("tepki günü işaret = karar yönü oranı:", (np.sign(E["react_ret"]) == E["dir"]).mean())
# rejim drifti: aynı takvim yılındaki tüm 2 günlük getirilerin ortalaması x işlem yönü
y2 = cl.fwd(r, 2) * 1e4; ym = y2.groupby(y2.index.year).mean()
E["drift_y"] = [(-dr) * ym.loc[pd.Timestamp(t).year] for t, dr in zip(E["react"], E["dir"])]
# yerel drift: olaydan önceki 60 günün 2 günlük ortalaması
y2t = y2.rolling(60, min_periods=40).mean().shift(2)
E["drift_60"] = [(-dr) * y2t.loc[pd.Timestamp(t)] for t, dr in zip(E["react"], E["dir"])]
E["h2_adj_y"] = E["h2"] - E["drift_y"]; E["h2_adj_60"] = E["h2"] - E["drift_60"]
print(E[["react", "dir", "h2", "drift_y", "h2_adj_y", "drift_60", "h2_adj_60"]].round(0).to_string())
for col in ("h2", "h2_adj_y", "h2_adj_60"):
    x = E[col]; print(col, "ort", round(x.mean(), 0), "t", round(cl.tstat(x), 2), "isabet", round((x > 0).mean(), 2))
# bootstrap: aynı yıldaki rastgele günler, aynı yön -> ortalama dağılımı
rng = np.random.default_rng(3); y2d = y2.dropna(); sims = []
for _ in range(20000):
    s = 0
    for t, dr in zip(E["react"], E["dir"]):
        pool = y2d[y2d.index.year == pd.Timestamp(t).year]; s += (-dr) * pool.iloc[rng.integers(len(pool))]
    sims.append(s / len(E))
sims = np.array(sims); obs = E["h2"].mean()
print("aynı-yıl rastgele tarih plasebo: null ort", round(sims.mean(), 0), "p(null>=obs)", round((sims >= obs).mean(), 4))
# pazartesi plasebosu: aynı yılın tüm Pazartesi girişleri
mon = y2d[y2d.index.dayofweek == 0]; sims2 = []
for _ in range(20000):
    s = 0
    for t, dr in zip(E["react"], E["dir"]):
        pool = mon[mon.index.year == pd.Timestamp(t).year]; s += (-dr) * pool.iloc[rng.integers(len(pool))]
    sims2.append(s / len(E))
sims2 = np.array(sims2); print("aynı-yıl Pazartesi plasebo: null ort", round(sims2.mean(), 0), "p", round((sims2 >= obs).mean(), 4))
# alt dönem ve son olaylar
for a, b in (("2017", "2019"), ("2020", "2021"), ("2022", "2023"), ("2024", "2026")):
    x = E[(pd.to_datetime(E["react"]) >= a) & (pd.to_datetime(E["react"]) < str(int(b) + 1))]["h2"]; print(a, b, "n", len(x), "ort", round(x.mean(), 0) if len(x) else None)
x = E["h2"].sort_values(); print("en iyi 3 çıkınca ort", round(x.iloc[:-3].mean(), 0), "t", round(cl.tstat(x.iloc[:-3]), 2))
E.to_csv(cl.OUT + "/c6_rating.csv", index=False)
