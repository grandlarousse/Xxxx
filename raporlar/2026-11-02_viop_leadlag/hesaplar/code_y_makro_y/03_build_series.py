"""Günlük yurt içi makro değişken paneli -> res/macro_daily.parquet (BIST takvimi; getiri = log, faiz = yüzde puan değişimi).
Önce: 01_parse_viop.py ve 02_parse_bap.py çalışmış olmalı."""
import numpy as np, pandas as pd
import mlib as M, ll
cal = ll.bist_cal(); cal = cal[cal >= "2010-01-01"]
V = {}
# 1) Yahoo günlük (FX_FIX: UTC günü sonu ~24:00)
V["y_usd"] = ll.ret("TRY=X"); V["y_eur"] = ll.ret("EURTRY=X"); V["y_bsk"] = 0.5 * (V["y_usd"] + V["y_eur"])
V["y_xau"] = ll.ret("GC=F") + V["y_usd"]   # gram altın TL ~ ons(USD, ~18 UTC) x USDTRY(24 UTC) — zaman uyumsuz
V["gc"] = ll.ret("GC=F")
# 2) Saatlik 15:00 UTC hizalı + gece/gündüz
for nm, sym in [("usd", "TRY=X"), ("eur", "EURTRY=X"), ("gc", "GC=F")]:
    V["h15_" + nm] = M.h15_ret(sym); V["n_" + nm] = M.night_ret(sym, "15:00", "06:00"); V["d_" + nm] = M.day_ret(sym, "06:00", "15:00")
V["h15_bsk"] = 0.5 * (V["h15_usd"] + V["h15_eur"]); V["n_bsk"] = 0.5 * (V["n_usd"] + V["n_eur"])
V["h15_xau"] = V["h15_gc"] + V["h15_usd"]; V["n_xau"] = V["n_gc"] + V["n_usd"]; V["d_xau"] = V["d_gc"] + V["d_usd"]
# 3) VİOP vadeli (uzlaşma ~15:00-15:15 UTC; aynı kontrat getirisi)
for nm, root in [("usd", "USDTRY"), ("eur", "EURTRY"), ("xau", "XAUTRY"), ("xauusd", "XAUUSD"), ("xu030f", "XU030")]:
    try:
        f = M.viop_front(root); V["v_" + nm] = f["ret"]
        if nm == "usd": V["v_usd_oi"] = f["oi"]; V["v_usd_volm"] = f["vol_tl"]
    except Exception as e: print("viop", root, e)
V["v_bsk"] = 0.5 * (V["v_usd"] + V["v_eur"])
# 4) Zımni TL faizi (USDTRY vadeli takvim yayılımı + ^IRX)
for nm, (a, b) in {"ir12": (0, 1), "ir13": (0, 2)}.items():
    o = M.viop_implied_rate("USDTRY", a, b)
    V[nm + "_lvl"] = o["ir"]; V["d_" + nm] = o["ir"].diff().where(o["c1"] == o["c1"].shift(1))  # aynı kontrat çifti -> roll sıçraması yok
    V[nm + "_diff_lvl"] = o["diff"]
# 5) TLREF
t = M.tlref(); V["tlref_lvl"] = t; V["d_tlref"] = t.reindex(cal).ffill().diff()
# 6) DİBS getirileri
try:
    b = pd.read_parquet(M.RES + "/bap_bonds.parquet"); b = b[(b["isin"] != "") & b["yc"].notna() & (b["yc"] > 0)]
    b["w"] = b["vol"].fillna(0) + 1
    g = b.groupby(["date", "isin"]).apply(lambda x: pd.Series({"y": np.average(x["yc"], weights=x["w"]), "dtm": x["dtm"].max(), "vol": x["vol"].sum()})).reset_index()
    med = g.groupby("date")["y"].median(); g = g[g["y"] > 0.6 * g["date"].map(med)]  # TÜFE'ye endeksli (reel getiri) kağıtları ele
    dates = np.sort(g["date"].unique()); prev = dict(zip(dates[1:], dates[:-1]))
    g["pdate"] = g["date"].map(prev)
    gp = g[["date", "isin", "y"]].rename(columns={"date": "pdate", "y": "py"})
    g = g.merge(gp, on=["pdate", "isin"], how="left"); g["dy"] = g["y"] - g["py"]
    for nm, (lo, hi) in {"dibs2": (450, 1000), "dibs5": (1400, 2200), "dibs10": (2900, 4000), "dibs1": (150, 450)}.items():
        x = g[(g["dtm"] >= lo) & (g["dtm"] <= hi)]
        def wmed(z, col):
            z = z.dropna(subset=[col]).sort_values(col)
            if len(z) == 0: return np.nan
            c = z["vol"].cumsum() / z["vol"].sum(); return float(z[col].values[np.searchsorted(c.values, 0.5)])
        V[nm + "_lvl"] = x.groupby("date").apply(lambda z: wmed(z, "y"))
        dd = x[x["dy"].notna() & (x["dy"].abs() < 8)]
        V["d_" + nm] = dd.groupby("date").apply(lambda z: wmed(z, "dy"))
        V[nm + "_n"] = dd.groupby("date").size()
except Exception as e: print("bap", e)
# 7) Risk primi vekilleri (ABD kapanışı ~20-21 UTC)
V["tur"] = ll.ret("TUR"); V["emb"] = ll.ret("EMB"); V["tur_eem"] = ll.ret("TUR") - ll.ret("EEM")
# 8) BIST bağlam
V["xu100"] = ll.ret("XU100"); V["xbank"] = ll.ret("XBANK"); V["xu030"] = ll.ret("XU030")
df = pd.DataFrame({k: pd.Series(v).reindex(cal) for k, v in V.items()})
df.index.name = "date"; df.to_parquet(M.RES + "/macro_daily.parquet")
desc = df.describe().T[["count", "mean", "std"]]; desc["first"] = df.apply(lambda s: s.first_valid_index()); print(desc.to_string())
