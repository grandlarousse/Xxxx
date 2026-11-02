"""s5a: VIOP gunluk bulteninden (2017-03..2026-10) pay vadelisi ve XU030 vadelisi gunluk satirlari -> parquet.
Her gun, her dayanak icin islem hacmi (TL) en buyuk kontrat secilir (ayni kontrat icinde acilis->kapanis; roll etkisi yok)."""
import os, glob, csv, numpy as np, pandas as pd
D = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/viop"
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_M4_b"
UND = ["EREGL", "KRDMD", "BRSAN", "XU030", "ISDMR"]
rows = []
for f in sorted(glob.glob(os.path.join(D, "viop_*.csv"))):
    with open(f, encoding="windows-1254", errors="replace") as fh:
        rd = csv.reader(fh, delimiter=";"); hdr = [h.strip() for h in next(rd)]; next(rd)
        ix = {h: i for i, h in enumerate(hdr)}
        for r in rd:
            if len(r) < 22: continue
            code = r[ix["SOZLESME KODU"]]
            if not code.startswith("F_"): continue
            u = code[2:-4]
            if u not in UND: continue
            if r[ix["PAZAR SEGMENTI"]] not in ("SSF", "IF", "EQIF", "INDEX", "") and u != "XU030":
                pass
            def g(k):
                try: return float(r[ix[k]].replace(",", "."))
                except Exception: return np.nan
            rows.append(dict(date=r[ix["TARIH"]], code=code, und=u, seg=r[ix["PAZAR SEGMENTI"]], exp=r[ix["VADE TARIHI"]],
                             settle=g("UZLASMA FIYATI"), psettle=g("ONCEKI UZLASMA FIYATI"), open=g("ACILIS FIYATI"), low=g("EN DUSUK FIYAT"),
                             high=g("EN YUKSEK FIYAT"), close=g("KAPANIS FIYATI"), vwap=g("AGIRLIKLI ORTALAMA FIYAT"), value=g("ISLEM HACMI"),
                             qty=g("ISLEM MIKTARI"), ntr=g("ISLEM SAYISI"), oi=g("ACIK POZISYON"),
                             osp=g("ACILIS SEANSI FIYATI") if "ACILIS SEANSI FIYATI" in ix and len(r) > ix["ACILIS SEANSI FIYATI"] else np.nan))
A = pd.DataFrame(rows); A["date"] = pd.to_datetime(A["date"])
A.to_parquet(os.path.join(OUT, "viop_rows.parquet"))
print(A.groupby(["und", A.date.dt.year]).size().unstack().fillna(0).astype(int))
print(A[A.und == "XU030"].code.str[:9].value_counts().head())
