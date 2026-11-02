"""Dayanak bazında günlük VİOP serileri: ön vade (c1), ikinci vade (c2), AP-seçimli 'likit' sözleşme (t-1 AP'ye göre, look-ahead yok),
toplam hacim/AP; spot ile birleştirme. Çıktı: results/daily_<und>.parquet ve results/daily_all.parquet"""
import numpy as np, pandas as pd
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
F = load_panel()
F = F[F["und"].isin(ALL) & (F["expiry"] >= F["date"])].copy()
# XU030 2020-07-27 öncesi endeks/1000 fiyatlı (sözleşme çarpanı 100 TL); fiyatları yeni ölçeğe çevir (x100) -> sadece seviye karşılaştırması için
# (getiriler etkilenmez). Kontrol: mult sütunu.
F["scale"] = 1.0
for u in IDX:
    m = (F["und"] == u) & (F["settle"] < 1000)  # eski ölçek (ör. 142.925)
    F.loc[m, "scale"] = 100.0
px = ["settle", "prev_settle", "open", "low", "high", "close", "vwap", "os_price"]
for c in px: F[c] = (F[c] * F["scale"]).where(F[c] > 0)  # 0 = işlem yok -> NaN
F["notional_px"] = F["settle"]
F["oi_tl"] = F["oi"] * F["mult"].where(F["mult"].notna()).groupby(F["und"]).transform("median") * F["settle"]
F = F.sort_values(["und", "date", "expiry"])
F["rank"] = F.groupby(["und", "date"]).cumcount() + 1
# önceki günün kapanışı (aynı sözleşme)
F["prev_close"] = F.groupby("code")["close"].shift(1)
F["prev_date"] = F.groupby("code")["date"].shift(1)
F["prev_oi"] = F.groupby("code")["oi"].shift(1)
F["prev_value"] = F.groupby("code")["value_tl"].shift(1)
agg = F.groupby(["und", "date"]).agg(value_tl=("value_tl", "sum"), qty=("qty", "sum"), trades=("trades", "sum"), oi=("oi", "sum"),
                                     oi_tl=("oi_tl", "sum"), n_ser=("code", "count"), os_value=("os_value", "sum"), os_trades=("os_trades", "sum"))
def pick(df, name):
    keep = ["code", "expiry", "settle", "prev_settle", "open", "high", "low", "close", "vwap", "value_tl", "qty", "trades", "oi", "oi_chg",
            "os_price", "os_value", "os_trades", "prev_close", "prev_date", "prev_oi", "mult"]
    d = df.set_index(["und", "date"])[keep]; d.columns = [f"{name}_{c}" for c in d.columns]; return d
c1 = pick(F[F["rank"] == 1], "c1"); c2 = pick(F[F["rank"] == 2], "c2")
# likit sözleşme: t-1'de AP'si en büyük olan (aynı kod t'de hâlâ listeleniyorsa); yoksa c1
F["prev_oi_f"] = F["prev_oi"].fillna(-1)
liq_idx = F.sort_values(["und", "date", "prev_oi_f", "expiry"], ascending=[True, True, False, True]).groupby(["und", "date"]).head(1)
cl = pick(liq_idx, "L")
# hacimce en likit (t günü; sadece tanımlayıcı istatistik için, sinyalde kullanılmaz)
vmax = F.sort_values(["und", "date", "value_tl"], ascending=[True, True, False]).groupby(["und", "date"]).head(1).set_index(["und", "date"])[["rank", "code"]]
vmax.columns = ["vmax_rank", "vmax_code"]
D = agg.join(c1).join(c2).join(cl).join(vmax).reset_index()
D["c1_dte"] = (D["c1_expiry"] - D["date"]).dt.days; D["c2_dte"] = (D["c2_expiry"] - D["date"]).dt.days; D["L_dte"] = (D["L_expiry"] - D["date"]).dt.days
# getiriler (aynı sözleşme)
for p in ["c1", "L"]:
    D[f"{p}_r_set"] = np.log(D[f"{p}_settle"] / D[f"{p}_prev_settle"])
    D[f"{p}_r_cls"] = np.log(D[f"{p}_close"] / D[f"{p}_prev_close"])
    D[f"{p}_r_intra"] = np.log(D[f"{p}_close"] / D[f"{p}_open"])
    D[f"{p}_r_on"] = np.log(D[f"{p}_open"] / D[f"{p}_prev_close"])
    D[f"{p}_r_on_set"] = np.log(D[f"{p}_open"] / D[f"{p}_prev_settle"])
    for c in [f"{p}_r_set", f"{p}_r_cls", f"{p}_r_intra", f"{p}_r_on", f"{p}_r_on_set"]:
        D.loc[(D[c].abs() > 0.2) | (D[f"{p}_trades"] <= 0), c] = np.nan  # düzeltme/bayat
# spot birleştir
out = []
for u, g in D.groupby("und"):
    g = g.set_index("date").sort_index()
    sp = spot_daily(u)
    if sp is not None:
        sp = sp[["o", "h", "l", "c", "adj", "v"]].add_prefix("s_")
        g = g.join(sp, how="left")
        g["s_value_tl"] = g["s_v"] * g["s_c"]
    g["und"] = u; out.append(g)
D = pd.concat(out).reset_index().rename(columns={"index": "date"})
D.to_parquet(RES + "/daily_all.parquet", index=False)
print(D.shape, D["date"].min(), D["date"].max())
print(D.groupby("und")["date"].agg(["min", "max", "count"]).to_string())
