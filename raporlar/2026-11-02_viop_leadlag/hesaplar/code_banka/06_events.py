"""Olay çalışması: HALKB ABD davası + BBVA ihale + makro şoklar. Anormal getiri = hisse - beta*XBANK(ex) [beta: olaydan önce -260..-20 gün].
CAR[0], CAR[0,+2], CAR[0,+5]. t-istatistiği = CAR / (sigma_res * sqrt(L)). Tarihler WebSearch ile doğrulandı (bkz. rapor)."""
import bk, numpy as np, pandas as pd
EV = [("HALKB", "2016-03-21", "Zarrab ABD'de tutuklandı (19.03.2016 Cmt)"),
      ("HALKB", "2017-03-28", "Atilla NY'de tutuklandı (27.03.2017)"),
      ("HALKB", "2017-11-28", "Zarrab'ın itirafçı olduğu ortaya çıktı (Salı)"),
      ("HALKB", "2018-01-04", "Atilla jüri mahkumiyeti (03.01.2018 ABD akşamı)"),
      ("HALKB", "2018-05-17", "Atilla'ya 32 ay (16.05.2018)"),
      ("HALKB", "2019-10-16", "ABD iddianamesi (15.10.2019)"),
      ("HALKB", "2021-10-25", "2. Daire: dokunulmazlık yok (22.10.2021 Cuma)"),
      ("HALKB", "2023-04-20", "ABD Yüksek Mahkemesi FSIA kararı (19.04.2023)"),
      ("HALKB", "2024-10-23", "2. Daire: örf-adet dokunulmazlığı reddi (22.10.2024)"),
      ("HALKB", "2025-10-07", "Yüksek Mahkeme başvuruyu reddetti (06.10.2025 Pzt)"),
      ("HALKB", "2026-03-09", "DOJ-Halkbank ertelenmiş kovuşturma anlaşması (09.03.2026)"),
      ("HALKB", "2026-06-17", "Dava düşürüldü (haber 17.06.2026)"),
      ("GARAN", "2021-11-15", "BBVA gönüllü pay alım teklifi duyurusu (TL12,20)"),
      ("GARAN", "2022-04-25", "BBVA teklif fiyatını TL15'e yükseltti"),
      ("XBANK", "2018-08-10", "Kur krizi (Brunson/Trump tarifeleri)"),
      ("XBANK", "2021-12-21", "KKM duyurusu (20.12.2021 akşamı)"),
      ("XBANK", "2023-05-29", "Seçim 2. tur sonrası"),
      ("XBANK", "2023-06-22", "TCMB ortodoks dönüş faiz artışı"),
      ("XBANK", "2025-03-19", "İmamoğlu gözaltısı"),
      ]
X = bk.R("XBANK"); M = bk.xu()
rows = []
for st, dt, desc in EV:
    t0 = pd.Timestamp(dt); y = bk.R(st)
    bench = M if st == "XBANK" else X
    df = pd.concat([y.rename("y"), bench.rename("b")], axis=1)
    if t0 not in df.index:
        t0 = df.index[df.index.searchsorted(t0)]
    i0 = df.index.get_loc(t0)
    est = df.iloc[max(0, i0 - 260): i0 - 20].dropna()
    b = est.cov().iloc[0, 1] / est["b"].var(); a = est["y"].mean() - b * est["b"].mean()
    sres = (est["y"] - a - b * est["b"]).std()
    ar = (df["y"] - a - b * df["b"])
    raw0 = df["y"].iloc[i0]
    o = {"stock": st, "date": str(t0.date()), "event": desc, "raw0_pct": 100 * raw0, "bench0_pct": 100 * df["b"].iloc[i0]}
    for L, lab in [(1, "0"), (3, "0_2"), (6, "0_5")]:
        car = ar.iloc[i0:i0 + L].sum(); o[f"CAR{lab}_pct"] = 100 * car; o[f"t{lab}"] = car / (sres * np.sqrt(L))
    o["pre_m5_m1_pct"] = 100 * ar.iloc[i0 - 5:i0].sum()
    rows.append(o)
E = pd.DataFrame(rows).round(2); E.to_csv(bk.RES + "/events.csv", index=False)
pd.set_option("display.width", 220); print(E[["stock", "date", "raw0_pct", "bench0_pct", "CAR0_pct", "t0", "CAR0_2_pct", "t0_2", "CAR0_5_pct", "event"]].to_string(index=False))
h = E[E.stock == "HALKB"]
print("HALKB olumsuz olaylar (2016-2019, 6 olay) ort CAR0:", round(h.iloc[:6]["CAR0_pct"].mean(), 2), " olumlu/çözüm (2025-10 hariç son 2):", h.iloc[-2:]["CAR0_pct"].round(2).tolist())
