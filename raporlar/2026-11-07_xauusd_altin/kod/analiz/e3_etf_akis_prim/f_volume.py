"""(f) Hacim şokları: y_<ETF>_vol = son bilinen (t-1) ABD kapanış gününün hacmi (bilgi anı t-1 16:00 ET; Yahoo günlük, t'de bilinir).
vz_t = ln(vol_{t-1}) − ortalama(ln vol, t-61..t-2)  [standartlaştırılmış: / std aynı pencere]
vzs_t = vz_t × sign(r_{t-1})  (yüksek hacimli yükseliş/düşüş günü)
Hedef: aynı ETF'nin t kapanışından t+h'ye getirisi.
"""
from common import *
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
raw = pd.read_parquet(f"{P}/yahoo/GLD.parquet"); raw.index = pd.to_datetime(raw.index)
chk = (d.y_GLD_vol == raw.volume.shift(1).reindex(d.index)).mean()
print("y_GLD_vol = ham hacim(t-1) uyumu:", round(chk, 4))
rows = []
for t in ["GLD", "GDX", "GDXJ", "SLV", "IAU"]:
    v = np.log(d[f"y_{t}_vol"].where(d[f"y_{t}_vol"] > 0))
    v = v.where(v.diff() != 0)   # tekrar eden (bayat) değerleri çıkar
    mu = v.shift(1).rolling(60, min_periods=40).mean(); sd = v.shift(1).rolling(60, min_periods=40).std()
    vz = (v - mu) / sd
    r = lr(d[f"c_{t}"])
    rl1 = r.shift(1)   # t-1 getirisi (y_* ile aynı gün)
    vzs = vz * np.sign(rl1)
    hi = (vz > 2).astype(float).where(vz.notna())
    for h in HS:
        y = fwd(r, h)
        rows.append(test("f_volume", f"f_vz_{t}_h{h}", f"{t} hacim şoku z (t-1) -> {t}", vz, y, h))
        rows.append(test("f_volume", f"f_vzs_{t}_h{h}", f"{t} hacim z × işaret(r_t-1) -> {t}", vzs, y, h))
        if t in ("GLD", "GDX"):
            rows.append(mean_diff_test("f_volume_big", f"f_hi_dn_{t}_h{h}", f"{t} hacim z>2 ve r_t-1<0 -> {t}", (hi * (rl1 < 0)).where(hi.notna()), y, h))
            rows.append(mean_diff_test("f_volume_big", f"f_hi_up_{t}_h{h}", f"{t} hacim z>2 ve r_t-1>0 -> {t}", (hi * (rl1 > 0)).where(hi.notna()), y, h))
    if t == "GLD":
        print("placebo vzs GLD:", placebo_lead(vzs, r, 1))
res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/f_volume_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]].round(3).to_string())
# IS seçimi -> strateji
c = res[res.family == "f_volume"].copy(); c["a"] = c.t_is.abs()
b = c.sort_values("a", ascending=False).iloc[0]
print("IS seçimi:", b.test_id, round(b.t_is, 2), "OOS t:", round(b.t_oos, 2))
t = b.test_id.split("_")[2]; h = int(b.test_id.split("_h")[-1]); kind = b.test_id.split("_")[1]
v = np.log(d[f"y_{t}_vol"].where(d[f"y_{t}_vol"] > 0)); v = v.where(v.diff() != 0)
vz = (v - v.shift(1).rolling(60, min_periods=40).mean()) / v.shift(1).rolling(60, min_periods=40).std()
x = vz if kind == "vz" else vz * np.sign(lr(d[f"c_{t}"]).shift(1))
pos = (np.sign(b.t_is) * np.sign(x) * (x.abs() > 1)).fillna(0)
sr = pd.DataFrame(strat_eval(f"hacim_{b.test_id}", pos, t, h, d))
sr.to_csv(f"{OUT}/f_volume_strategies.csv", index=False)
print(sr[["strategy", "mode", "cost", "sh_is", "sh_oos", "sh_22", "shdm_is", "shdm_oos", "bh_oos", "exposure_long", "exposure_short"]].to_string())
