"""06a: VİOP günlük bültenlerinden F_TUPRS ve F_XU030 satırlarını ayrıştır (ham CSV'ler veri; kod ayrı dizinde). Çıktı: res/viop_rows.parquet"""
import os, glob, re, csv, pandas as pd, numpy as np
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
files = sorted(glob.glob(S + "/data/viop/viop_2*.csv"))
pat = re.compile(r"^F_(TUPRS|XU030)\d{4}$")
rows = []
for fn in files:
    with open(fn, encoding="windows-1254", errors="replace") as f:
        lines = f.read().splitlines()
    if len(lines) < 3: continue
    hdr = [h.strip() for h in lines[1].split(";")]  # İngilizce başlık
    for ln in lines[2:]:
        if ";F_TUPRS" not in ln and ";F_XU030" not in ln: continue
        r = ln.split(";")
        if len(r) < 23 or not pat.match(r[1]): continue
        d = dict(zip(hdr, r)); rows.append(d)
D = pd.DataFrame(rows)
num = ["SETTLEMENT PRICE", "PREVIOUS SETTLEMENT PRICE", "OPENING PRICE", "LOWEST PRICE", "HIGHEST PRICE", "CLOSING PRICE", "VWAP", "TRADED VALUE", "TRADE VOLUME", "TRADE COUNT", "OPEN POSITION",
       "OPENING SESSION PRICE", "TRADED VALUE AT OPENING SESSION", "TRADED VOLUME AT OPENING SESSION", "TRADE COUNT AT OPENING SESSION"]
for c in num:
    if c in D: D[c] = pd.to_numeric(D[c].str.replace(",", "."), errors="coerce")
D["date"] = pd.to_datetime(D["TRADE DATE"]); D["exp"] = pd.to_datetime(D["EXPIRATION DATE"], errors="coerce")
D["und"] = D["INSTRUMENT SERIES"].str[2:7].where(D["INSTRUMENT SERIES"].str.startswith("F_TUPRS"), "XU030")
D.to_parquet(S + "/out/code_v_E3_b/res/viop_rows.parquet")
print(len(files), "dosya;", D.shape, D.groupby([D.date.dt.year, "und"]).size().unstack().to_string())
