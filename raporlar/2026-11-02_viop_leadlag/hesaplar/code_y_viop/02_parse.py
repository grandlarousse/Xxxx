"""VİOP bültenlerini tek parquet'e ayrıştırır.
Çıktılar:
  $S/data/viop_panel.parquet   : tüm VADELİ (F_*) satırlar (esnek TM_ hariç), her gün x sözleşme
  $S/data/viop_opt_agg.parquet : opsiyonların dayanak x gün x (call/put) toplamları (AP, adet, hacim, prim, işlem#)
Sütunlar (panel): date, code, root, und (dayanak, standart ad), und_raw, market, segment, ctype, expiry,
  settle, prev_settle, open, low, high, close, vwap, value_tl, qty, trades, oi, oi_chg,
  os_price, os_value, os_qty, os_trades (açılış seansı alanları; eski bültenlerde yok -> NaN), mult (= value_tl/(qty*vwap)).
Not: KOZAL->TRALT, KOZAA->TRMET yeniden adlandırması uygulanır (und). XU030 vadelisi 27.07.2020 öncesi endeks/1000 fiyatlı.
Kullanım: python3 -I 02_parse.py
"""
import os, re, glob, csv, sys
import numpy as np, pandas as pd
from multiprocessing import Pool
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = f"{S}/data/viop"
REN = {"KOZAL": "TRALT", "KOZAA": "TRMET"}
COLS = {"TARIH": "date", "SOZLESME KODU": "code", "PAZAR": "market", "PAZAR SEGMENTI": "segment", "SOZLESME TIPI": "ctype",
        "DAYANAK VARLIK": "und_raw", "VADE TARIHI": "expiry", "UZLASMA FIYATI": "settle", "ONCEKI UZLASMA FIYATI": "prev_settle",
        "ACILIS FIYATI": "open", "EN DUSUK FIYAT": "low", "EN YUKSEK FIYAT": "high", "KAPANIS FIYATI": "close",
        "AGIRLIKLI ORTALAMA FIYAT": "vwap", "ISLEM HACMI": "value_tl", "PRIM HACMI": "prem_tl", "ISLEM MIKTARI": "qty",
        "ISLEM SAYISI": "trades", "ACIK POZISYON": "oi", "ACIK POZISYON DEGISIMI": "oi_chg", "ACILIS SEANSI FIYATI": "os_price",
        "ACILIS SEANSI ISLEM HACMI": "os_value", "ACILIS SEANSI ISLEM MIKTARI": "os_qty", "ACILIS SEANSI ISLEM SAYISI": "os_trades"}
NUM = ["settle", "prev_settle", "open", "low", "high", "close", "vwap", "value_tl", "prem_tl", "qty", "trades", "oi", "oi_chg",
       "os_price", "os_value", "os_qty", "os_trades"]
def und_std(u):
    u = u.strip()
    if u.endswith(".E"): u = u[:-2]
    elif u.startswith("D_"):
        u = u[2:]
        if u in ("XU030D", "XLBNKD", "X10XBD", "XSD25D"): u = u[:-1]
    return REN.get(u, u)
def fnum(x):
    x = x.strip()
    if x == "": return np.nan
    try: return float(x)
    except ValueError: return float(x.replace(",", "."))
def parse(fn):
    fut, opt = [], []
    with open(fn, encoding="windows-1254", errors="replace") as f:
        rd = csv.reader(f, delimiter=";")
        hdr = [h.strip() for h in next(rd)]; next(rd)
        idx = {COLS[h]: i for i, h in enumerate(hdr) if h in COLS}
        for r in rd:
            if len(r) < 20: continue
            code = r[idx["code"]].strip()
            if code.startswith("F_"):
                rec = {k: r[i] for k, i in idx.items() if i < len(r)}
                fut.append(rec)
            elif code.startswith("O_"):
                rec = {k: r[i] for k, i in idx.items() if i < len(r) and k in ("date", "code", "ctype", "und_raw", "expiry", "value_tl", "prem_tl", "qty", "trades", "oi")}
                opt.append(rec)
    F = pd.DataFrame(fut); O = pd.DataFrame(opt)
    for c in NUM:
        if c in F: F[c] = F[c].map(fnum)
        if c in O: O[c] = O[c].map(fnum)
    return F, O
def main():
    files = sorted(glob.glob(f"{D}/viop_????????.csv"))
    print("files", len(files), flush=True)
    with Pool(2) as p: res = p.map(parse, files, chunksize=20)
    F = pd.concat([r[0] for r in res], ignore_index=True); O = pd.concat([r[1] for r in res if len(r[1])], ignore_index=True)
    F["date"] = pd.to_datetime(F["date"]); F["expiry"] = pd.to_datetime(F["expiry"], errors="coerce")
    F["und"] = F["und_raw"].map(und_std)
    m = F["code"].str.extract(r"^F_(.*?)(\d{4})$")
    F["root"] = m[0].map(lambda x: REN.get(x, x) if isinstance(x, str) else x)
    for c in NUM:
        if c not in F: F[c] = np.nan
    F["mult"] = F["value_tl"] / (F["qty"] * F["vwap"])
    F = F[["date", "code", "root", "und", "und_raw", "market", "segment", "ctype", "expiry"] + [c for c in NUM if c != "prem_tl"] + ["mult"]]
    F = F.sort_values(["date", "und", "expiry", "code"]).reset_index(drop=True)
    for c in ["code", "root", "und", "und_raw", "market", "segment", "ctype"]: F[c] = F[c].astype("category")
    F.to_parquet(f"{S}/data/viop_panel.parquet", index=False)
    print("futures rows", len(F), F["date"].min(), F["date"].max(), F["date"].nunique(), flush=True)
    # opsiyon özetleri
    O["date"] = pd.to_datetime(O["date"]); O["und"] = O["und_raw"].map(und_std)
    O["cp"] = np.where(O["ctype"].str.contains(r"_EC|_AC"), "C", np.where(O["ctype"].str.contains(r"_EP|_AP"), "P", "?"))
    G = O.groupby(["date", "und", "cp"])[["oi", "qty", "value_tl", "prem_tl", "trades"]].sum().reset_index()
    G.to_parquet(f"{S}/data/viop_opt_agg.parquet", index=False)
    print("option agg rows", len(G), flush=True)
if __name__ == "__main__": main()
