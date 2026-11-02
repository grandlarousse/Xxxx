"""s09a: VİOP günlük bülteninden (data/viop/*.csv; ortak indirilmiş) TRALT/KOZAL, KRDMD, EREGL, TRMET/KOZAA pay vadelisi satırlarını çıkar."""
import glob, io, os, pandas as pd, numpy as np
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
OUT = S + "/out/code_v_C4C5_b/viop_ssf_sel.parquet"
U = {"KOZAL.E", "TRALT.E", "KRDMD.E", "EREGL.E", "KOZAA.E", "TRMET.E"}
rows = []
for f in sorted(glob.glob(S + "/data/viop/viop_*.csv")):
    try:
        raw = open(f, "rb").read().decode("windows-1254", errors="replace")
    except Exception:
        continue
    lines = raw.splitlines()
    if len(lines) < 3: continue
    hdr = lines[1].split(";")
    keep = [l for l in lines[2:] if any(u in l for u in U)]
    if not keep: continue
    df = pd.read_csv(io.StringIO("\n".join([";".join(hdr)] + keep)), sep=";", header=0, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    rows.append(df)
D = pd.concat(rows, ignore_index=True)
D = D[D["MARKET SEGMENT"].str.strip().isin(["SSF"]) | D["INSTRUMENT SERIES"].str.startswith("F_")]
for c in ["SETTLEMENT PRICE", "OPENING PRICE", "LOWEST PRICE", "HIGHEST PRICE", "CLOSING PRICE", "VWAP", "TRADED VALUE", "TRADE VOLUME", "TRADE COUNT", "OPEN POSITION", "OPENING SESSION PRICE", "TRADED VALUE AT OPENING SESSION", "TRADED VOLUME AT OPENING SESSION"]:
    if c in D: D[c] = pd.to_numeric(D[c].str.replace(",", "."), errors="coerce")
D["TRADE DATE"] = pd.to_datetime(D["TRADE DATE"]); D["EXPIRATION DATE"] = pd.to_datetime(D["EXPIRATION DATE"], errors="coerce")
D.to_parquet(OUT)
print(D.shape, D["TRADE DATE"].min(), D["TRADE DATE"].max())
print(D.groupby("UNDERLYING")["TRADE DATE"].agg(["min", "max", "count"]))
