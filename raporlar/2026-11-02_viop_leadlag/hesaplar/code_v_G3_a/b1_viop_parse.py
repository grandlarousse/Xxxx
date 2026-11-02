"""B1: VİOP günlük bülteni ayrıştırma (ortak dizin data/viop, salt okunur). Tüm vadeli (F_) satırları -> res/viop_fut.parquet.
Dosya biçimi: windows-1254, ';', 1. satır TR başlık, 2. satır EN başlık."""
import os, glob, csv, sys, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
R = S + "/out/code_v_G3_a/res"; OUT = R + "/viop_fut.parquet"
old = pd.read_parquet(OUT) if os.path.exists(OUT) else None
done = set(old["TARIH"].dt.strftime("%Y%m%d")) if old is not None else set()
keep = ["TARIH", "SOZLESME KODU", "PAZAR SEGMENTI", "DAYANAK VARLIK", "VADE TARIHI", "UZLASMA FIYATI", "ONCEKI UZLASMA FIYATI", "ACILIS FIYATI",
        "EN DUSUK FIYAT", "EN YUKSEK FIYAT", "KAPANIS FIYATI", "AGIRLIKLI ORTALAMA FIYAT", "ISLEM HACMI", "ISLEM MIKTARI", "ISLEM SAYISI", "ACIK POZISYON",
        "ACILIS SEANSI FIYATI", "ACILIS SEANSI ISLEM MIKTARI", "ACILIS SEANSI ISLEM SAYISI"]
rows = []; nf = 0
for fn in sorted(glob.glob(S + "/data/viop/viop_*.csv")):
    k = os.path.basename(fn)[5:13]
    if k in done: continue
    try:
        with open(fn, encoding="windows-1254", errors="replace") as f:
            rd = csv.reader(f, delimiter=";"); hdr = [h.strip() for h in next(rd)]; next(rd)
            idx = {h: i for i, h in enumerate(hdr)}
            for r in rd:
                if len(r) < 10: continue
                code = r[idx["SOZLESME KODU"]]
                if not code.startswith("F_"): continue
                rows.append({c: (r[idx[c]] if c in idx and idx[c] < len(r) else "") for c in keep})
        nf += 1
    except Exception as e:
        print("hata", fn, e)
df = pd.DataFrame(rows)
if len(df):
    df["TARIH"] = pd.to_datetime(df["TARIH"]); df["VADE TARIHI"] = pd.to_datetime(df["VADE TARIHI"], errors="coerce")
    for c in keep[5:]:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "."), errors="coerce")
    if old is not None: df = pd.concat([old, df], ignore_index=True)
    df = df.drop_duplicates(["TARIH", "SOZLESME KODU"]).sort_values(["TARIH", "SOZLESME KODU"])
    df.to_parquet(OUT)
else:
    df = old
print("yeni dosya", nf, "toplam gün", df.TARIH.nunique(), df.TARIH.min(), df.TARIH.max(), "satır", len(df))
