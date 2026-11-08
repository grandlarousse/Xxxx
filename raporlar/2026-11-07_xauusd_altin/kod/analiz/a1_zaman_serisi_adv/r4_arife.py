import sys; sys.path.insert(0, ".")
from adv_common import *
ARIFE = ["2017-06-23","2017-08-31","2017-10-27","2018-06-14","2018-08-20","2018-10-29","2019-06-03","2019-08-09","2019-10-28","2020-05-22","2020-07-30","2020-10-28",
         "2021-05-12","2021-07-19","2021-10-28","2022-04-29","2022-07-08","2022-10-28","2023-04-20","2023-06-27","2023-10-27","2024-04-09","2024-06-14","2024-10-28",
         "2025-03-28","2025-06-05","2025-10-28","2026-03-19","2026-05-26","2026-10-28"]
A = pd.DatetimeIndex([a for a in ARIFE if pd.Timestamp(a) in d.index])
ls = np.log(d.v_settle.astype(float)); base = (ls - np.log(d.xau_p15)).rolling(21, center=True, min_periods=5).median()
T = pd.DataFrame({H: ((ls - np.log(d[f"xau_p{H}"].astype(float)) - base) * 1e4).reindex(A).round(0) for H in ["07", "12", "13", "15"]})
T["vol"] = d.v_volume.reindex(A); T["vol_med"] = d.v_volume.rolling(20).median().reindex(A)
pc, q = lowmom_spot(5); pv = asof_to_viop(pc)
T["pos"] = pv.reindex(A); T["fwd1_bps"] = (d.fwd1.reindex(A) * 1e4).round(0)
T["p07->p15 bps"] = (np.log(d.xau_p15 / d.xau_p07).reindex(A) * 1e4).round(0)
print(T.to_string())
print("arife sayısı (VİOP günü):", len(A), " LOWMOM aktif:", int((T.pos != 0).sum()))
act = T[T.pos != 0]
print("aktif arife günlerinde pos*fwd1 bps:", (act.pos * act.fwd1_bps).tolist(), " toplam", (act.pos * act.fwd1_bps).sum())
# arife hariç backtest
m = ~d.index.isin(A)
for h in [1, 5]:
    for per in ["IS", "OOS", "FULL"]:
        a, b = PER[per]; mm = (r_v.index >= a) & (r_v.index <= b)
        n0 = bt(pv[mm], r_v[mm], h, 5, demean=True); n1 = bt(pv.where(m, 0)[mm], r_v[mm], h, 5, demean=True)
        print(h, per, "base", round(sh(n0), 3), "arife pozisyonu sıfır", round(sh(n1), 3))
