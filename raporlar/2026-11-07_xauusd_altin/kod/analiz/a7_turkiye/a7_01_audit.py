"""Veri denetimi: yarım günler, yurt içi tatiller, roll günleri, sıfır hacim, zaman damgası kontrolleri."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
pd.set_option("display.width", 220); pd.set_option("display.max_rows", 300)

p, f = build()
f.to_parquet(f"{OUT}/features.parquet")
hd, d10, d15 = half_days(p)
print("=== Yarım günler (uzlaşma ~09:40 UTC) ===")
H = pd.DataFrame({"code": p.v_code, "settle": p.v_settle, "dev10_bps": d10 * 1e4, "dev15_bps": d15 * 1e4, "dow": p.index.day_name()})[hd]
print(H.round(1).to_string())
print("adet:", int(hd.sum()))

gap, missing = tr_holiday_gaps(p)
print("\n=== VİOP kapalı hafta içi günler (yıl başına) ===")
ms = pd.Series(1, index=missing)
print(ms.groupby(ms.index.year).sum().to_string())
post = gap[gap > 0]
print("tatil sonrası ilk gün sayısı:", len(post), " gap dağılımı:", post.value_counts().sort_index().to_dict())

print("\n=== Roll günleri (v_code değişimi) ===")
rt = f["roll_t"] & (f.index > f.index[0])
print("adet:", int(rt.sum()))
print(pd.DataFrame({"code": p.v_code, "prev": p.v_code.shift(1), "dte": p.v_dte, "v_ret": p.v_ret})[rt].tail(12).to_string())
print("roll günü v_ret std vs diğer:", round(p.v_ret[rt].std() * 1e4, 1), round(p.v_ret[~rt].std() * 1e4, 1), "bps")

print("\n=== Sıfır hacim / eksik ===")
print("v_volume==0:", int((p.v_volume.fillna(0) == 0).sum()), " vo_xautry_volume==0:", int((p.vo_xautry_volume.fillna(0) == 0).sum()),
      " vo_usdtry_volume==0:", int((p.vo_usdtry_volume.fillna(0) == 0).sum()))
print("v_ret==0:", int((p.v_ret == 0).sum()))
print("dk_USDTRY_p15 eksik:", int(p.dk_USDTRY_p15.isna().sum()), " son:", p.dk_USDTRY_p15.last_valid_index())

print("\n=== USDTRY zaman damgası kontrolü: VİOP USDTRY getirisi (15:10) ile Dukascopy 15:00 değişimi korelasyonu, kaydırmalı ===")
for s in (-1, 0, 1):
    print(s, round(p.vo_usdtry_ret.corr(np.log(p.dk_USDTRY_p15).diff().shift(s)), 3))
print("Yahoo USDTRY=X diff ile Dukascopy 15:00 diff, kaydırmalı:")
for s in (-2, -1, 0, 1):
    print(s, round(np.log(p.y_USDTRY_X).diff().corr(np.log(p.dk_USDTRY_p15).diff().shift(s)), 3))
print("\n=== XAUUSD VİOP getirisi ile spot 15:00 getirisi ===")
sr = np.log(p.xau_p15).diff()
for s in (-1, 0, 1):
    print(s, round(p.v_ret.corr(sr.shift(s)), 3))
print("tr_prem_matched özet (%):"); print((p.tr_prem_matched * 100).describe().round(3).to_string())
print("|prem|>2% gün:", (p.tr_prem_matched.abs() > 0.02).sum())
print(p.loc[p.tr_prem_matched.abs() > 0.02, ["tr_prem_matched", "vo_xautry_code", "v_code", "vo_usdtry_code", "vo_xautry_volume"]].to_string())
