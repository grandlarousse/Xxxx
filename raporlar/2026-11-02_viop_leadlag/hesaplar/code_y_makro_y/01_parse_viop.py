"""VİOP bültenlerinden döviz/altın/faiz vadelilerini çıkarır -> res/viop_fx.parquet.
Satırlar: F_USDTRY*, F_EURTRY*, F_XAUTRY*, F_XAUUSD*, F_TLREF*, D_FI segmenti, F_XU030*, F_XLBNK* (bağlam)."""
import os, glob, re, csv, sys
import pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUT = S + "/out/code_y_makro_y/res/viop_fx.parquet"
pat = re.compile(r"^F_(USDTRY|EURTRY|XAUTRY|XAUUSD|TLREF|XU030|XLBNK|EURUSD)")
keep = ["TARIH", "SOZLESME KODU", "PAZAR", "PAZAR SEGMENTI", "DAYANAK VARLIK", "VADE TARIHI", "UZLASMA FIYATI", "ONCEKI UZLASMA FIYATI",
        "ACILIS FIYATI", "EN DUSUK FIYAT", "EN YUKSEK FIYAT", "KAPANIS FIYATI", "AGIRLIKLI ORTALAMA FIYAT", "ISLEM HACMI", "ISLEM MIKTARI", "ISLEM SAYISI", "ACIK POZISYON"]
old = pd.read_parquet(OUT) if os.path.exists(OUT) else None
done = set(old["file"].unique()) if old is not None else set()
rows = []
for fn in sorted(glob.glob(S + "/data/viop/viop_*.csv")):
    b = os.path.basename(fn)
    if b in done: continue
    with open(fn, encoding="windows-1254", errors="replace") as f:
        rd = csv.reader(f, delimiter=";"); hdr = [h.strip() for h in next(rd)]; next(rd)
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rd:
            if len(r) < 20: continue
            code = r[ix["SOZLESME KODU"]]
            if pat.match(code) or r[ix["PAZAR"]] == "D_FI":
                d = {k: (r[ix[k]] if k in ix and ix[k] < len(r) else "") for k in keep}; d["file"] = b; rows.append(d)
new = pd.DataFrame(rows)
if len(new):
    for c in keep[6:]: new[c] = pd.to_numeric(new[c], errors="coerce")
    new["TARIH"] = pd.to_datetime(new["TARIH"]); new["VADE TARIHI"] = pd.to_datetime(new["VADE TARIHI"], errors="coerce")
df = pd.concat([old, new]) if old is not None else new
df = df.drop_duplicates(["TARIH", "SOZLESME KODU"]).sort_values(["TARIH", "SOZLESME KODU"])
df.to_parquet(OUT); print(df.shape, df["TARIH"].min(), df["TARIH"].max(), df["file"].nunique())
