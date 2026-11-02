"""s08: (c) TRALT ~ SHFE AU vs COMEX GC: haftalık kısmi korelasyon (XU100 kontrollü), farklı hafta çapaları, ortak örneklem,
at yarışı regresyonu (AU ve GC birlikte), Çin primi (AU - GC - USDCNH) katkısı, blok bootstrap farkı, alt dönemler. Kendi AU roll serim."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
tr = bist_dec("TRALT.IS").cc; xu = bist_dec("XU100.IS").cc
AU = to_bist(sina_roll("AU")["cc"], "nan")
GC = to_bist(loc_ret("GC=F", "c"), "nan")
# USDCNH: Sina (UTC gün sonu kapanışı varsayımı) — haftalık düzeyde küçük kayma
cnh = pd.read_parquet(S + "/data_cin/sina_idx/USDCNH.parquet")
cnh_r = pd.Series(np.log(cnh["c"].values), index=pd.DatetimeIndex(cnh["ldate"].values)).diff()
CNH = to_bist(cnh_r, "nan")
tryx = daily_local("TRY=X")["c"]; tr_r = np.log(tryx).diff(); tr_r.index = tr_r.index + pd.Timedelta(days=1)  # FX_FIX: ldate 00:00 UTC kapanış -> önceki UTC gününe ait; 1 gün ileri kaydır = o günün kapanışı
TRYr = to_bist(tr_r, "nan")
D = pd.DataFrame({"tr": tr, "xu": xu, "AU": AU, "GC": GC, "CNH": CNH, "TRY": TRYr})
D = D[D.index >= "2018-11-09"]
def pcorr(df, a, b, ctrl):
    X = np.column_stack([np.ones(len(df))] + [df[c].values for c in ctrl])
    ra = df[a].values - X @ np.linalg.lstsq(X, df[a].values, rcond=None)[0]
    rb = df[b].values - X @ np.linalg.lstsq(X, df[b].values, rcond=None)[0]
    return np.corrcoef(ra, rb)[0, 1]
def weekly(df, anchor):
    return df.resample(f"W-{anchor}").sum(min_count=3)
rng = np.random.default_rng(3)
print("Ortak örneklem 2018-11+, haftalık (hafta içi tüm sütunlar ≥3 gün) — kısmi korelasyon | XU100")
print("çapa |  n  | r_AU  r_GC | pc_AU  pc_GC | fark [%95 blok-bootstrap] | at yarışı (TRALT ~ XU + AU + GC) t_AU t_GC | prim pc")
rows = []
for anc in ["MON", "TUE", "WED", "THU", "FRI"]:
    W = weekly(D, anc).dropna()
    W["prem"] = W.AU - W.GC - W.CNH
    pa, pg = pcorr(W, "tr", "AU", ["xu"]), pcorr(W, "tr", "GC", ["xu"])
    # blok bootstrap (8 haftalık bloklar)
    n = len(W); B = 8; diffs = []
    for _ in range(1000):
        st = rng.integers(0, n - B, n // B + 1); ii = np.concatenate([np.arange(s, s + B) for s in st])[:n]
        Wb = W.iloc[ii].reset_index(drop=True); diffs.append(pcorr(Wb, "tr", "AU", ["xu"]) - pcorr(Wb, "tr", "GC", ["xu"]))
    lo, hi = np.quantile(diffs, [.025, .975])
    r, _ = ols_nw(W.tr, W[["xu", "AU", "GC"]], lags=2)
    pp = pcorr(W, "tr", "prem", ["xu", "GC"])
    print(f"{anc}  | {n} | {W.tr.corr(W.AU):.3f} {W.tr.corr(W.GC):.3f} | {pa:.3f} {pg:.3f} | {pa-pg:+.3f} [{lo:+.3f};{hi:+.3f}] | t_AU {r.loc['AU','t']:+.2f} t_GC {r.loc['GC','t']:+.2f} | prem|xu,GC {pp:+.3f}")
    rows.append(dict(anchor=anc, n=n, pc_AU=pa, pc_GC=pg, diff=pa - pg, lo=lo, hi=hi, t_AU=r.loc['AU', 't'], t_GC=r.loc['GC', 't'], prem_pc=pp))
pd.DataFrame(rows).to_csv(sys.path[0] + "/s08_weekly_anchor.csv", index=False)
# USD bazlı TRALT ve XU+TRY kontrolü (Cuma)
W = weekly(D, "FRI").dropna()
W["tr_usd"] = W.tr - W.TRY
print(f"\nCuma, USD bazlı TRALT: pc_AU={pcorr(W,'tr_usd','AU',['xu','TRY']):.3f} pc_GC={pcorr(W,'tr_usd','GC',['xu','TRY']):.3f}")
# alt dönemler (Cuma ve Çarşamba)
for anc in ["FRI", "WED"]:
    W = weekly(D, anc).dropna()
    for a, b in [("2018-11", "2021-01"), ("2021-01", "2024-01"), ("2024-01", "2027-01")]:
        w = W[(W.index >= a) & (W.index < b)]
        print(f"{anc} {a}..{b}: n={len(w)} pc_AU={pcorr(w,'tr','AU',['xu']):.3f} pc_GC={pcorr(w,'tr','GC',['xu']):.3f}")
# günlük senkron ve 2 günlük
Dd = D.dropna(subset=["tr", "xu", "AU", "GC"])
print(f"\nGünlük: pc_AU={pcorr(Dd,'tr','AU',['xu']):.3f} pc_GC={pcorr(Dd,'tr','GC',['xu']):.3f}  (AU_t penceresi 07:00 t-1->07:00 t; GC_t ~18:00 t-1->18:00 t)")
Dd2 = D.copy(); Dd2["AUn"] = Dd2.AU.shift(-1)  # AU_{t+1}: 07:00 t -> 07:00 t+1, BIST t seansını kapsar
x = Dd2.dropna(subset=["tr", "xu", "AUn", "GC"])
print(f"Günlük, AU_(t+1) (BIST t seansını kapsayan pencere): pc_AU={pcorr(x,'tr','AUn',['xu']):.3f}  vs GC_t {pcorr(x,'tr','GC',['xu']):.3f}; ikisi birlikte:", ols_nw(x.tr, x[["xu", "AUn", "GC"]])[0].round(3).to_dict())
