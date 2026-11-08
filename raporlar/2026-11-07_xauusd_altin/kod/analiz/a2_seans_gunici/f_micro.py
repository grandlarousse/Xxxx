"""(f) VİOP mikro yapısı: hacim ve açık pozisyon şokları (t-1 bülteni; t-1 akşamı yayımlanır -> t 15:00'ten önce).
Ayrıca VİOP-yerel gece/gündüz ayrışımı: v_open (~06:30 UTC normal seans açılışı; spot 07:00 ile MAD 15 bps, en yakın eşleşme)."""
from a2_common import *
reset_families(["f_micro", "f_viop_native"])
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
v = load_viop()
lv = np.log(v.v_tot_volume.replace(0, np.nan))
volz = (lv - lv.shift(1).rolling(20).mean()) / lv.shift(1).rolling(20).std()     # t'nin hacim şoku; t-1 sürümü kullanılacak
doi = np.log(v.v_tot_oi / v.v_tot_oi.shift(1))                                     # toplam OI (tüm vadeler) -> roll-nötr
P_ = {"volz_t-1": volz.shift(1), "ret_x_volz_t-1": (v.v_ret * volz).shift(1), "dOI_t-1": doi.shift(1), "sign_ret_x_dOI_t-1": (np.sign(v.v_ret) * doi).shift(1)}
rows = []
for h in (1, 3, 5):
    for k, x in P_.items():
        rows.append(test("f_micro", f"f_{k}_h{h}", k, x, v[f"fwd{h}"], h, "t-1 bülten"))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/f_micro_ic.csv", index=False); print(R.drop(columns=["family", "test_id", "note"]).to_string())
# VİOP-yerel gece (uzlaşma t-1 -> açılış t) ve gündüz (açılış t -> uzlaşma t) ortalamaları
night = np.log(v.v_open / v.v_prev_settle); dayr = np.log(v.v_settle / v.v_open)
ok = (v.v_open > 0) & v.v_open.notna()
night, dayr = night[ok], dayr[ok]
yr = night.index.year
T = pd.DataFrame({"gece_uzl->acilis": night.groupby(yr).mean() * 1e4, "gunduz_acilis->uzl": dayr.groupby(yr).mean() * 1e4, "n": night.groupby(yr).size()}).round(2)
print("\nVİOP-yerel gece/gündüz ortalama (bps/gün):\n", T.to_string()); T.to_csv(f"{OUT}/f_viop_native_night_day.csv")
for nm, x in [("night", night), ("day", dayr), ("night_minus_day", night - dayr)]:
    fm = mean_test(x); ism = mean_test(x[x.index <= IS_END]); oom = mean_test(x[x.index > IS_END]); ys = x.groupby(x.index.year).mean()
    register(AGENT, "f_viop_native", f"f_native_{nm}", nm, 0, dict(ic=fm["mean"], t=fm["t"], n=fm["n"], t_is=ism["t"], t_oos=oom["t"], ic_oos=oom["mean"],
             yrs_same_sign=int((np.sign(ys) == np.sign(fm["mean"])).sum()), yrs=len(ys)), "VİOP işlem fiyatları; açılış fiyatı ilk işlem (gürültülü)")
    print(nm, "ort bps", round(fm["mean"] * 1e4, 2), "t", round(fm["t"], 2), "IS t", round(ism["t"], 2), "OOS t", round(oom["t"], 2), "yıl", int((np.sign(ys) == np.sign(fm["mean"])).sum()), "/", len(ys))
# Gece-uzun (uzlaşmada al -> ertesi sabah açılışta sat) VİOP-yerel, maliyetli
for c in (0, 5, 10):
    x = night - c / 1e4
    for p, m in [("IS", x.index <= IS_END), ("OOS", x.index > IS_END), ("aksam20.09+", x.index >= "2020-09-18")]:
        xx = x[m]; print(f"VİOP gece-uzun maliyet {c}bps {p}: yıllık %{xx.mean()*252*100:.1f} Sharpe {xx.mean()/xx.std()*np.sqrt(252):.2f}")
