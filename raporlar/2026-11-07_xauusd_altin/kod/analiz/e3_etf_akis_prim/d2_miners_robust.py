"""(d2) 'Altının 15:00 ET'ye kadarki hareketi -> madenci ETF'lerinde ertesi gün dönüş' bulgusunun sağlamlık testleri.
m_t = ln(xau_cut_t / xau_close_{t-1}) [Dukascopy spot; 16:00 ET t-1 -> 15:00 ET t; bilgi anı 15:00 ET = 19:00/20:00 UTC].
Kontroller: (i) diğer madenci/kaldıraçlı ETF'ler, (ii) göreli getiri (madenci − β·GLD, β geçmiş 250 gün),
(iii) daha erken kesim (14:00 ET) ve daha eski bilgi (m_{t-1}) placebo, (iv) uç dönemler hariç, (v) yıl yıl, (vi) VİOP günleriyle çakışma yok (ABD hedefi).
"""
from common import *
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
rows = []
m = np.log(d.xau_cut / d.xau_close.shift(1))
zm = m / m.rolling(60, min_periods=40).std().shift(1)
# 14:00 ET spot (Dukascopy saatlik; fiyat anı = index+1h)
x = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")["c"]; x.index = (x.index + pd.Timedelta(hours=1)).tz_convert("America/New_York")
x14 = x[x.index.hour == 14]; x14.index = pd.to_datetime(x14.index.date); x14 = x14[~x14.index.duplicated()].reindex(d.index)
m14 = np.log(x14 / d.xau_close.shift(1)); zm14 = m14 / m14.rolling(60, min_periods=40).std().shift(1)
# Avrupa+Asya kısmı (16:00 ET t-1 -> 07:00 UTC t) ve ABD sabahı (07:00 UTC -> 15:00 ET) ayrımı
mA = np.log(d.xau_07utc / d.xau_close.shift(1)); mB = np.log(d.xau_cut / d.xau_07utc)
zA = mA / mA.rolling(60, min_periods=40).std().shift(1); zB = mB / mB.rolling(60, min_periods=40).std().shift(1)

tick = ["GDXJ", "GDX", "SIL", "SILJ", "RING", "SGDM", "GOEX", "GDXU", "NUGT", "JNUG", "NEM", "AEM", "GOLD", "KGC", "SLV", "GLD"]
for t in tick:
    if f"c_{t}" not in d or d[f"c_{t}"].notna().sum() < 500: continue
    r = lr(d[f"c_{t}"])
    for h in (1, 5):
        rows.append(test("d2_miners", f"d2_zm_{t}_h{h}", f"z(m_t) 15:00 ET -> {t}", zm, fwd(r, h), h, reg=t not in ("GDXJ", "GDX", "SLV", "GLD")))  # d_letf'te kayıtlı olanları tekrar sayma
# göreli getiri madenci − β GLD
rG = lr(d.c_GLD)
for t in ["GDXJ", "GDX", "SIL", "RING"]:
    r = lr(d[f"c_{t}"])
    beta = (r.rolling(250, min_periods=120).cov(rG) / rG.rolling(250, min_periods=120).var()).shift(1)
    rel = r - beta * rG
    for h in (1, 5):
        rows.append(test("d2_miners_rel", f"d2_zm_rel_{t}_h{h}", f"z(m_t) -> {t} − β·GLD", zm, fwd(rel, h), h))
    rows.append(test("d2_miners_rel", f"d2_zm_GLDonly_for_{t}_h1", f"z(m_t) -> β·GLD bileşeni ({t})", zm, fwd(beta.shift(-1) * rG, 1), 1, reg=False))
# zaman varyantları
for t in ["GDXJ", "GDX"]:
    r = lr(d[f"c_{t}"])
    for nm, z_ in [("zm14", zm14), ("zm_l1", zm.shift(1)), ("zA_asya_avrupa", zA), ("zB_abd_sabah", zB)]:
        for h in (1, 5):
            rows.append(test("d2_timing", f"d2_{nm}_{t}_h{h}", f"{nm} -> {t}", z_, fwd(r, h), h))
    print(t, "placebo zm:", placebo_lead(zm, r, 1))
res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/d2_miners_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]].round(3).to_string())
b = res[res.test_id == "d2_zm_GDXJ_h1"].iloc[0]
print("GDXJ yıl yıl IC:", b.by_year)
b = res[res.test_id == "d2_zm_GDX_h1"].iloc[0]
print("GDX yıl yıl IC:", b.by_year)

# uç dönemler hariç IC
r = lr(d.c_GDXJ); y = fwd(r, 1)
msk = pd.Series(True, index=d.index)
for a_, b_ in EXTREMES.values(): msk[a_:b_] = False
print("GDXJ h1 IC uç dönemler hariç:", ic(zm[msk], y[msk], 5))
# büyüklük: zm dilimlerine göre GDXJ ertesi gün ortalama (bps)
dd = pd.concat([zm.rename("z"), y.rename("y")], axis=1).dropna()
for seg, mm in [("is", dd.index <= IS_END), ("oos", dd.index > IS_END), ("22+", dd.index >= SUB_START)]:
    g = dd[mm]; bkt = pd.cut(g.z, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    print(seg, (g.groupby(bkt).y.agg(["mean", "count"]).assign(mean=lambda q: (q["mean"] * 1e4).round(1))).T.to_string())
