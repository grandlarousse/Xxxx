"""Aile (a): Türkiye'ye özgü bilgiyle VİOP XAUUSD fwd{1,3,5} öngörüsü. Her öngörücü x h için split_stats + register."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
import json
FAM = "a_xau_tr"
reset_family(FAM)
p, f = build()
# Kapanışta (K) sürümler ve XU030 gün içi (Yahoo saatlik, 2023-12+; 13:30 UTC barının kapanışı = 14:30 UTC, karar anından önce)
f["usd_fut_K"] = p["vo_usdtry_ret"]; f["xu_K"] = p["vo_xu030_ret"]
xh = pd.read_parquet(f"{S}/panel/yahoo_h/XU030.IS.parquet")
xh.index = xh.index.tz_convert(None)
b1330 = xh[(xh.index.hour == 13) & (xh.index.minute == 30)]["close"]; b1330.index = b1330.index.normalize()
f["xu_intra_1430"] = np.log(b1330.reindex(f.index) / p["y_XU030_IS"])   # t-1 BIST kapanışı -> t 14:30 UTC
# (ad, bilgi zamanı UTC, K=kapanışta hesaplanan mı)
PRED = [
    ("usd_fut_l1", "t-1 15:10 (VİOP USDTRY uzlaşma getirisi)", False),
    ("usd_fut_5_l1", "t-5..t-1 15:10", False),
    ("usd_spot_1", "t 15:00 (Dukascopy USDTRY t-1 15:00 -> t 15:00)", False),
    ("usd_spot_5", "t 15:00 (5 gün)", False),
    ("usd_intra", "t 07:00 -> t 15:00", False),
    ("itl_l1", "t-1 15:10 (VİOP USDTRY bazından ima TL faizi, seviye)", False),
    ("ditl_5_l1", "t-1 15:10 (ima TL faizi 5 gün değişim)", False),
    ("xu_l1", "t-1 15:10 (VİOP XU030 getirisi)", False),
    ("xu_5_l1", "t-5..t-1 15:10", False),
    ("xuusd_l1", "t-1 15:10 (XU030 USD bazlı)", False),
    ("prem_l1", "t-1 15:10 (gram altın primi seviye)", False),
    ("dprem_l1", "t-1 15:10 (prim 1 gün değişim)", False),
    ("dprem5_l1", "t-1 15:10 (prim 5 gün değişim)", False),
    ("premz_l1", "t-1 15:10 (prim 60g z)", False),
    ("prem", "t 15:10 KAPANIŞTA (prim seviye)", True),
    ("dprem_K", "t 15:10 KAPANIŞTA (prim değişim)", True),
    ("premz_K", "t 15:10 KAPANIŞTA (prim z)", True),
    ("gvolz_l1", "t-1 15:10 (XAUTRY hacim 20g z)", False),
    ("goi_d1_l1", "t-1 (XAUTRY OI 1g log değişim)", False),
    ("goi_d5_l1", "t-1 (XAUTRY OI 5g log değişim)", False),
    ("gvol_ratio_z_l1", "t-1 (XAUTRY/XAUUSD hacim oranı 60g z)", False),
    ("xbasis_dev_l1", "t-1 (VİOP XAUUSD uzlaşma - spot 15:00 - taşıma)", False),
    ("xbasis_dev_K", "t 15:10 KAPANIŞTA (VİOP XAUUSD baz sapması)", True),
    ("usd_fut_K", "t 15:10 KAPANIŞTA (VİOP USDTRY getirisi)", True),
    ("xu_K", "t 15:10 KAPANIŞTA (VİOP XU030 getirisi)", True),
    ("xu_intra_1430", "t 14:30 UTC (Yahoo saatlik XU030, t-1 kapanış->t 14:30; yalnız 2023-12+)", False),
]
rows = []
for nm, when, K in PRED:
    for h in (1, 3, 5):
        st = test(FAM, nm, f[nm], f[f"fwd{h}"], h, note=("K " if K else "") + when)
        rows.append(dict(pred=nm, info=when, K=K, h=h, ic=st["ic"], t=st["t"], n=st["n"], ic_is=st["ic_is"], t_is=st["t_is"], ic_oos=st["ic_oos"], t_oos=st["t_oos"],
                         yrs=f"{st['yrs_same_sign']}/{st['yrs']}"))
R = pd.DataFrame(rows)
R.to_csv(f"{OUT}/a_ic_table.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
print(R.drop(columns=["info"]).round(3).to_string())
# Placebo (ileriye bakma) — aynı gün 15:00 bilgileri ve en iyi 5
print("\n=== placebo_lead (shift<0 = gelecek bilgisi, yasak) ===")
best = R.reindex(R.t.abs().sort_values(ascending=False).index).drop_duplicates("pred").head(6).pred.tolist()
for nm in sorted(set(best + ["usd_spot_1", "usd_intra"])):
    for h in (1, 5):
        print(nm, h, placebo_lead(f[nm], f["v_ret"], h))
