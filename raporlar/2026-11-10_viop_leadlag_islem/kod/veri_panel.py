"""Paneller. python3 -I veri_panel.py <VERI_DIR>   (once veri_viop_oku.py ve veri_yahoo.py calismis olmali)
Uretir (panel/): fut_long, fut_ret(wide), fut_limit(wide), spot_gunluk, dis_gunluk, saatlik, dk5, bolunme_gunleri.csv, eksik_semboller.csv"""
import sys, os, glob, json
import pandas as pd, numpy as np
V = sys.argv[1]; P = f"{V}/panel"; R = f"{V}/raw/yahoo"
meta = json.load(open(f"{R}/meta.json"))
und47 = meta["und47"]
x = pd.read_parquet(f"{P}/viop_gunluk.parquet")
# --- bolunme/bedelsiz gunleri (Yahoo)
spl = []
for f in glob.glob(f"{R}/events/*.json"):
    s = os.path.basename(f)[:-5]; e = json.load(open(f))
    for d, v in (e.get("splits") or {}).items():
        spl.append({"sym": s, "date": d, "num": v.get("numerator"), "den": v.get("denominator"), "ratio": v.get("splitRatio")})
spl = pd.DataFrame(spl).sort_values(["sym", "date"]); spl.to_csv(f"{P}/bolunme_gunleri.csv", index=False)
splset = {(r.sym.replace(".IS", ""), pd.Timestamp(r.date)) for r in spl.itertuples() if r.sym.endswith(".IS")}
# --- fut_ret
UNI = und47 + ["XU030", "XLBNK", "USDTRY", "XAUUSD", "XAGUSD", "XAUTRY"]
def pat(u):
    return rf"^F_{u}M?\d{{4}}(N\d)?$" if u == "XAUTRY" else rf"^F_{u}\d{{4}}(N\d)?$"
rows = []
for u in UNI:
    nm = [u] + {"TRALT": ["KOZAL"], "TRMET": ["KOZAA"]}.get(u, [])  # eski kodlar (KOZAL->TRALT, KOZAA->TRMET) birlestirilir
    y = x[x["und"].isin(nm) & x["code"].str.match("|".join(pat(n) for n in nm))].copy()
    y = y[(y["settle"] > 0) & (y["prev_settle"] > 0)]
    y["bd"] = np.busday_count(y["date"].values.astype("datetime64[D]"), y["expiry"].values.astype("datetime64[D]"))
    y = y[y["bd"] >= 2].sort_values(["date", "expiry", "oi"], ascending=[True, True, False])
    f = y.groupby("date").head(1).copy()
    f["ret"] = np.log(f["settle"] / f["prev_settle"])
    # prev_settle sureklilik: ayni kontratin onceki gun uzlasmasi ile karsilastir
    z = x[x["code"].isin(f["code"].unique())][["date", "code", "settle"]].sort_values(["code", "date"])
    z["lag"] = z.groupby("code")["settle"].shift(1)
    f = f.merge(z[["date", "code", "lag"]], on=["date", "code"], how="left")
    f["ps_mismatch"] = ((f["prev_settle"] / f["lag"] - 1).abs() > 0.003) & f["lag"].notna()
    f["n1"] = f["code"].str.contains(r"N\d$")
    f["split_day"] = [(u, d) in splset for d in f["date"]]
    f["und"] = u
    rows.append(f)
F = pd.concat(rows, ignore_index=True)
is_stock = F["und"].isin(und47)
# NOT: PLAN |ret|>ln(1,105) yazar; ama -%10 limit-asagi gunu ln(0,9)=-0,1054 gercek bir gundur. Yukari ln(1+m+0,005), asagi ln(1-m-0,005) siniri kullanilir.
pre = (F["date"] < "2020-03-13").values; mg = np.where(pre, 0.20, 0.10)
over = (F["ret"] > np.log(1 + mg + 0.005)) | (F["ret"] < np.log(1 - mg - 0.005))
F["nan_neden"] = ""
F.loc[is_stock & over, "nan_neden"] = "marj"
F.loc[is_stock & (F["split_day"] | F["ps_mismatch"]), "nan_neden"] = F["nan_neden"].where(F["nan_neden"] != "", "bolunme_ya_da_ps_uyumsuz")
F["fut_ret"] = F["ret"].where(F["nan_neden"] == "")
sm = np.where(F["date"] < "2020-03-13", 0.20, 0.10)
F["fut_limit"] = is_stock & ((np.exp(F["ret"]) - 1).abs() >= 0.93 * sm) & F["fut_ret"].notna() | (is_stock & (F["nan_neden"] == "marj") & False)
F = F.rename(columns={"settle": "fut_settle", "value_tl": "fut_value_tl", "trades": "fut_trades", "code": "fut_code"})
keep = ["date", "und", "fut_ret", "ret", "fut_settle", "prev_settle", "fut_value_tl", "fut_trades", "fut_code", "expiry", "bd", "oi", "fut_limit", "nan_neden", "ps_mismatch", "n1", "split_day"]
F[keep].to_parquet(f"{P}/fut_long.parquet")
F.pivot(index="date", columns="und", values="fut_ret").to_parquet(f"{P}/fut_ret.parquet")
F.pivot(index="date", columns="und", values="fut_limit").astype(float).to_parquet(f"{P}/fut_limit.parquet")
for c, n in [("fut_settle", "fut_settle"), ("fut_value_tl", "fut_value_tl"), ("fut_trades", "fut_trades")]:
    F.pivot(index="date", columns="und", values=c).to_parquet(f"{P}/{n}.parquet")
F.pivot(index="date", columns="und", values="fut_code").to_parquet(f"{P}/fut_code.parquet")
print("fut_long", len(F), F["date"].min().date(), F["date"].max().date())
print("NaN nedenleri:", F[F["nan_neden"] != ""].groupby(["nan_neden"]).size().to_dict(), "fut_limit:", int(F["fut_limit"].sum()), "N1 satir:", int(F["n1"].sum()), "ps_mismatch:", int(F["ps_mismatch"].sum()))
# --- yahoo panelleri
def load(kind, syms):
    out = []; miss = []
    for s in syms:
        p = f"{R}/{kind}/{s}.parquet"
        if not os.path.exists(p): miss.append((s, kind)); continue
        d = pd.read_parquet(p); d.insert(0, "sym", s); out.append(d)
    return pd.concat(out), miss
miss = []
sp, m = load("daily", [s for s in meta["spot"]]); miss += m
sp = sp.rename_axis("ts_utc").reset_index()
sp = sp[["sym", "ldate", "ts_utc", "o", "h", "l", "c", "adj", "v"]].rename(columns={"ldate": "date"})
sp.to_parquet(f"{P}/spot_gunluk.parquet")
dis, m = load("daily", meta["dis"]); miss += m
dis = dis.rename_axis("ts_utc").reset_index()[["sym", "ldate", "ts_utc", "o", "h", "l", "c", "adj", "v"]].rename(columns={"ldate": "date"})
dis.to_parquet(f"{P}/dis_gunluk.parquet")
h, m = load("h1", meta["saatlik"]); miss += m
h.rename_axis("ts_utc").reset_index().drop(columns="adj").to_parquet(f"{P}/saatlik.parquet")
k, m = load("m5", meta["dk5"]); miss += m
k.rename_axis("ts_utc").reset_index().drop(columns="adj").to_parquet(f"{P}/dk5.parquet")
pd.DataFrame(miss, columns=["sym", "kind"]).to_csv(f"{P}/eksik_semboller.csv", index=False)
for n, d in [("spot_gunluk", sp), ("dis_gunluk", dis), ("saatlik", h), ("dk5", k)]:
    print(n, len(d), d["sym"].nunique())
print("eksik:", miss)
