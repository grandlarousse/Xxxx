"""Türkiye gün öncesi piyasası PTF (Piyasa Takas Fiyatı) saatlik -> günlük.
Kaynak: EPİAŞ Şeffaflık Platformu dışa aktarımı; GitHub üzerinden kamuya açık kopyalar (EPİAŞ API'si 2024'ten beri kimlik doğrulama istiyor):
  2013-2018: github.com/monteburns/ems  DataGen/PTFs/Piyasa_Takas_Fiyati-0101YYYY-3112YYYY.csv
  2019-2025: github.com/onatuzkan/vep-forward-tvtp-option-pricing inputs/historical/ptf_raw/ptf_YYYY.csv
  2026 (31.12.2025-27.09.2026): aynı repo inputs/market/realized_ptf_2025-12-31_2026-09-27.csv
Doğrulama: EPİAŞ 2018 yıllık bülteni 2018 aritmetik ortalama PTF = 231,64 TL/MWh.
ZAMANLAMA: D günü PTF'si D-1 günü ~13:00-14:00 TSİ (10:00-11:00 UTC) ilan edilir -> BIST seansı SIRASINDA bilinir.
"""
import glob, os, pandas as pd, numpy as np
import elib
DL = elib.SCR + "/dl/ptf"
fs = sorted(glob.glob(DL + "/mb_201[3-8].csv")) + sorted(glob.glob(DL + "/ptf_20*.csv")) + [DL + "/realized_2026.csv"]
parts = []
for f in fs:
    d = pd.read_csv(f, sep=";", dtype=str)
    d.columns = ["date", "hour", "tl", "usd", "eur"][: len(d.columns)]
    for c in ["tl", "usd", "eur"]:
        d[c] = pd.to_numeric(d[c].str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")
    d["ts"] = pd.to_datetime(d["date"] + " " + d["hour"], format="%d.%m.%Y %H:%M")
    parts.append(d[["ts", "tl", "usd", "eur"]])
h = pd.concat(parts).drop_duplicates("ts", keep="last").set_index("ts").sort_index()
h.to_parquet(elib.OUT + "/ptf_hourly.parquet")
day = h.index.normalize()
D = h.groupby(day).mean()
pk = h[(h.index.hour >= 8) & (h.index.hour < 20)]
D["tl_peak"] = pk.groupby(pk.index.normalize())["tl"].mean()
D["nh"] = h.groupby(day).size()
D.to_parquet(elib.OUT + "/ptf_daily.parquet")
print(D.index.min(), D.index.max(), len(D))
print("2018 ort TL (EPİAŞ: 231,64):", round(h.loc["2018", "tl"].mean(), 2))
print(D.resample("YE").mean()[["tl", "usd", "eur"]].round(1))
print("eksik saatli gün:", (D.nh < 23).sum())
