"""İddia 1 işlem kuralı: VİOP akşam kapanışı (20:00 UTC) al -> ertesi normal seans açılışı (06:30 UTC) sat.
(a) Spot vekil 2020-09-18+: giriş 20:00, çıkış 06:00 / 07:00 (06:30 ara değer yok), yalnız ertesi gün VİOP işlem günü olan geceler.
(b) VİOP yerel 2026 (akşam bülteni kapanışı -> v_os_price), spot pencereyle izleme hatası.
(c) Maliyet 5/10 bps; drift düzeltmesi üç biçimde; buy&hold karşılaştırma; alt dönem."""
from adv_common import *
import glob
v = load_viop(); s = load_spot(); px = A2.price_series()
vd = v.index[v.index >= "2020-09-21"]
prev_cal = pd.DatetimeIndex([pd.Timestamp(d.date()) for d in v.index.to_series().shift(1).reindex(vd)])
# akşam seansı t-1 takvim gününde (önceki VİOP günü) 16-20 UTC; çıkış t 06:30
b0 = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") for d in vd]); bp = prev_cal.tz_localize("UTC")
e20 = snap(px, bp + pd.Timedelta(hours=20)); x06 = snap(px, b0 + pd.Timedelta(hours=6)); x07 = snap(px, b0 + pd.Timedelta(hours=7))
x0630 = np.sqrt(x06 * x07)
night = pd.DataFrame({"r06": np.log(x06 / e20), "r07": np.log(x07 / e20), "r0630": np.log(x0630 / e20)}, index=vd)
# aynı günlerin 15:00->15:00 spot getirisi (buy&hold), ve VİOP v_ret
night["bh"] = np.log(v.xau_p15 / v.xau_p15_prev).reindex(vd)
night["vret"] = v.v_ret.reindex(vd)
night = night.dropna(subset=["r0630", "bh"])
print("n gece:", len(night))
def sh(x): x = x.dropna(); return round(x.mean() / x.std() * np.sqrt(252), 2)
rows = []
for nm in ("r0630", "r07"):
    for c in (0, 5, 7.5, 10):
        net = night[nm] - c / 1e4
        r = dict(kural=nm, cost=c, bps=round(net.mean() * 1e4, 2), t=round(mean_t(net)[1], 2), sharpe=sh(net))
        for k, (a, b) in {"2020-21": ("2020-01-01", "2021-12-31"), "2022-23": ("2022-01-01", "2023-12-31"), "2024-26": ("2024-01-01", "2026-12-31"), "OOS22+": ("2022-01-01", "2026-12-31")}.items():
            m = (net.index >= a) & (net.index <= b); r[f"sh_{k}"] = sh(net[m])
        # drift düzeltme: (i) zaman payı 10.5/24 x yıllık ort günlük getiri; (ii) varyans payı; (iii) bütün günlük drift
        yr = night.index.year; dm = night.bh.groupby(yr).transform("mean")
        vs = night[nm].groupby(yr).transform("var") / night.bh.groupby(yr).transform("var")
        r["sh_dm_time"] = sh(net - dm * 10.5 / 24); r["sh_dm_var"] = sh(net - vs * dm); r["sh_dm_full"] = sh(net - dm)
        oo = night.index >= "2022-01-01"
        r["oos_dm_var"] = sh((net - vs * dm)[oo]); r["oos_dm_time"] = sh((net - dm * 10.5 / 24)[oo])
        rows.append(r)
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(f"{OUT}/adv1b_trade.csv", index=False)
print("buy&hold 15->15 spot Sharpe (aynı günler):", sh(night.bh), " OOS:", sh(night.bh[night.index >= "2022-01-01"]), "| VİOP v_ret B&H:", sh(night.vret), "OOS", sh(night.vret[night.index >= "2022-01-01"]))
print("gece getirisi std bps:", round(night.r0630.std() * 1e4, 1), " başabaş maliyet (bps) tam:", round(night.r0630.mean() * 1e4, 2), " OOS:", round(night.r0630[night.index >= "2022-01-01"].mean() * 1e4, 2))
# 50/50 karışım: B&H'yi gece dışı saatlerde de tutmanın marjinal değeri (gece dışı = bh - gece)
offn = night.bh - night.r0630
print("gece-dışı (06:30->ertesi 20:00 yaklaşık) ort bps:", round(offn.mean() * 1e4, 2), " t", round(mean_t(offn)[1], 2), " Sharpe", sh(offn))

# (b) VİOP yerel 2026
ev = []
for f in sorted(glob.glob(f"{S}/dl4/as_*.csv")):
    t = pd.read_csv(f, sep=";", skiprows=[1]); t = t[t["SOZLESME KODU"].astype(str).str.startswith("F_XAUUSD")]
    t = t[pd.to_numeric(t["ISLEM MIKTARI"], errors="coerce") > 0]
    if t.empty: continue
    for _, r in t.iterrows():
        ev.append(dict(cal=pd.Timestamp(os.path.basename(f)[3:11]), code=r["SOZLESME KODU"], ev_close=float(r["KAPANIS FIYATI"]), ev_open=float(r["ACILIS FIYATI"]), qty=float(r["ISLEM MIKTARI"])))
E = pd.DataFrame(ev)
# ertesi VİOP günü ve o günün aktif kontratı / açılış seansı fiyatı
vi = v.index
E["next"] = [vi[vi > d][0] if (vi > d).any() else pd.NaT for d in E.cal]
E = E.dropna(subset=["next"])
E = E.merge(v[["v_code", "v_os_price", "v_open", "v_settle", "v_prev_settle"]], left_on="next", right_index=True)
E = E[E.code == E.v_code]
E["viop_night"] = np.log(E.v_os_price / E.ev_close)
bc = pd.DatetimeIndex(E.cal).tz_localize("UTC"); bn = pd.DatetimeIndex(E.next).tz_localize("UTC")
p20 = snap(px, bc + pd.Timedelta(hours=20)); q06 = snap(px, bn + pd.Timedelta(hours=6)); q07 = snap(px, bn + pd.Timedelta(hours=7))
E["spot_night"] = np.log(np.sqrt(q06 * q07) / p20)
E["diff"] = E.viop_night - E.spot_night
E = E.dropna(subset=["viop_night", "spot_night"])
print(f"\nVİOP yerel 2026 (n={len(E)}): VİOP gece ort {E.viop_night.mean()*1e4:.2f} bps (medyan {E.viop_night.median()*1e4:.2f}), spot aynı gece {E.spot_night.mean()*1e4:.2f} bps; fark ort {E['diff'].mean()*1e4:.2f}, medyan {E['diff'].median()*1e4:.2f}, std {E['diff'].std()*1e4:.1f} bps; corr {E.viop_night.corr(E.spot_night):.3f}")
print("   gün t açılış=v_open eşit mi (os_price):", float((E.v_open == E.v_os_price).mean()))
E.to_csv(f"{OUT}/adv1b_viop_native_2026.csv", index=False)
