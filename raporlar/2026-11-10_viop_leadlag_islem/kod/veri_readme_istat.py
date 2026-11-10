"""README icin sayilar. python3 -I veri_readme_istat.py <VERI_DIR>"""
import sys, os, pandas as pd, numpy as np
V = sys.argv[1]; P = f"{V}/panel"
def sz(n): return round(os.path.getsize(f"{P}/{n}") / 1e6, 1)
for n in ["viop_gunluk", "fut_long", "fut_ret", "fut_limit", "fut_settle", "fut_value_tl", "fut_trades", "fut_code", "spot_gunluk", "dis_gunluk", "saatlik", "dk5"]:
    d = pd.read_parquet(f"{P}/{n}.parquet")
    dc = "date" if "date" in d.columns else ("ts_utc" if "ts_utc" in d.columns else None)
    rng = (str(d[dc].min())[:16], str(d[dc].max())[:16]) if dc else (str(d.index.min().date()), str(d.index.max().date()))
    print(n, len(d), d.shape[1], rng, sz(n + ".parquet"), "MB")
F = pd.read_parquet(f"{P}/fut_long.parquet")
print("fut_ret dolu/NaN:", F.fut_ret.notna().sum(), F.fut_ret.isna().sum())
st = F[F.und.isin(pd.read_parquet(f"{P}/fut_ret.parquet").columns)]
print("fut_limit yil:", F[F.fut_limit].groupby(F.date.dt.year).size().to_dict())
print("fut_limit und top8:", F[F.fut_limit].und.value_counts().head(8).to_dict())
print("fut_limit toplam", int(F.fut_limit.sum()), " NaN nedeni:", F.nan_neden.value_counts().to_dict())
print("fut_ret NaN gunleri:\n", F[F.nan_neden != ""][["date", "und", "fut_code", "ret", "nan_neden"]].to_string(index=False, max_rows=30))
print("gun sayisi/und min:", F.groupby("und").size().min(), "max", F.groupby("und").size().max())
print("kisa und:", F.groupby("und").date.min()[lambda s: s > "2017-04-01"].dt.date.astype(str).to_dict())
print("fut_trades==0 oran:", round((F.fut_trades == 0).mean(), 4))
S = pd.read_parquet(f"{P}/spot_gunluk.parquet"); g = S.groupby("sym").date.agg(["min", "max", "size"])
print("kisa spot (ilk>2017-03):", g[g["min"] > "2017-03-01"]["min"].dt.date.astype(str).to_dict())
print("spot son tarih !=2026-11-10:", g[g["max"] < "2026-11-09"]["max"].dt.date.astype(str).to_dict())
print("TRALT/TRMET/TRENJ ilk c:", {s: (str(S[S.sym==s].date.min().date()), round(float(S[S.sym==s].c.iloc[0]),2)) for s in ["TRALT.IS","TRMET.IS","TRENJ.IS"]})
sp = pd.read_csv(f"{P}/bolunme_gunleri.csv"); sp = sp[sp.date >= "2017-03-01"]
u = pd.read_parquet(f"{P}/fut_ret.parquet").columns
sp47 = sp[sp.sym.str.replace(".IS", "", regex=False).isin(u)]
print("bolunme 2017+ toplam", len(sp), "47-dayanak", len(sp47))
print("; ".join(f"{r.sym.replace('.IS','')} {r.date} {r.ratio}" for r in sp47.itertuples()))
H = pd.read_parquet(f"{P}/saatlik.parquet"); K = pd.read_parquet(f"{P}/dk5.parquet")
print("saatlik gun:", H.ts_utc.dt.date.nunique(), "5dk gun:", K.ts_utc.dt.date.nunique())
