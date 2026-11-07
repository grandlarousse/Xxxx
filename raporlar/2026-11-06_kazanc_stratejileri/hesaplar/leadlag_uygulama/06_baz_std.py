#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_baz_std.py - XU030 vadelisi kapanis bazi sicramasi kuralinin GUNCEL esigi: std120(Db).
b_t = ln(F_XU030 on vade KAPANIS FIYATI_t / XU030 spot kapanis_t); Db_t = b_t - b_{t-1} (ayni sozlesme; devir gunu bos).
Bulten: Borsa Istanbul VIOP gunluk CSV (varsayilan basliklar, istekler arasi 0,8 sn). Spot: leadlag2/isy/XU030.csv.
Not: kural [PL #1] 18:10 son fiyatini kullanir; bultenin KAPANIS FIYATI endeks vadelisinin seans kapanisidir (18:15) -> yaklasik.
"""
import os, sys, time
import numpy as np, pandas as pd, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as o

URL = "https://www.borsaistanbul.com/data/vadeli/viop_{:%Y%m%d}.csv"
S = requests.Session()


def bulten(g):
    f = os.path.join(o.V, "viop", f"viop_{g:%Y%m%d}.csv")
    if not os.path.exists(f):
        try:
            r = S.get(URL.format(g), timeout=60); time.sleep(0.8)
            if r.status_code == 200 and r.text.lstrip().startswith("TARIH;"):
                open(f, "w", encoding="utf-8").write(r.text)
        except requests.RequestException:
            return None
    if not os.path.exists(f):
        return None
    t = open(f, encoding="utf-8", errors="replace").read().splitlines()
    bas = [x.strip() for x in t[0].split(";")]
    rows = [x.split(";") for x in t[2:] if x.startswith(f"{g:%Y-%m-%d};F_XU030")]
    if not rows:
        return None
    d = pd.DataFrame([r[:len(bas)] for r in rows], columns=bas)
    d["VADE TARIHI"] = pd.to_datetime(d["VADE TARIHI"])
    d["KAPANIS FIYATI"] = pd.to_numeric(d["KAPANIS FIYATI"].str.replace(",", "."), errors="coerce")
    d = d[(d["VADE TARIHI"] - g).dt.days > 1].sort_values("VADE TARIHI")
    return d.iloc[0] if len(d) else None


def main():
    spot = pd.read_csv(os.path.join(o.V, "isy", "XU030.csv"), index_col=0, parse_dates=True)["px"]
    gun = spot.index[spot.index >= pd.Timestamp("2026-04-01")]
    rec = []
    for g in gun:
        x = bulten(g)
        if x is None or not np.isfinite(x["KAPANIS FIYATI"]):
            continue
        rec.append(dict(tarih=g, kod=x["SOZLESME KODU"], F=x["KAPANIS FIYATI"], S=spot.loc[g]))
    D = pd.DataFrame(rec).set_index("tarih")
    D["b"] = np.log(D.F / D.S)
    D["db"] = D.b.diff().where(D.kod == D.kod.shift(1))
    D["std120"] = D.db.rolling(120, min_periods=60).std()
    D.to_csv(os.path.join(o.V, "sonuc", "xu030_baz.csv"), float_format="%.6f")
    son = D.iloc[-1]
    txt = (f"Bulten gunu {len(D)} ({D.index[0].date()}..{D.index[-1].date()}); son {D.index[-1].date()} {son.kod}: "
           f"b {son.b*1e4:+.0f} bps, Db {son.db*1e4:+.0f} bps, std120(Db) {son.std120*1e4:.0f} bps, z {son.db/son.std120:+.2f}\n"
           + D.tail(6)[["kod", "F", "S", "b", "db", "std120"]].assign(b=lambda x: (x.b*1e4).round(0), db=lambda x: (x.db*1e4).round(0),
                                                                     std120=lambda x: (x.std120*1e4).round(0)).to_string())
    open(os.path.join(o.V, "sonuc", "xu030_baz.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
