"""(b) GLD prim/iskontosu.
NAV_D: LBMA Gold Price PM (15:00 Londra) ile hesaplanır, SSGA D akşamı yayımlar.
ons/pay_D = NAV_D / spot(LBMA PM_D); kestirim gürültüsünü azaltmak için D-19..D yuvarlanan medyanı (oz_med) kullanılır (gerçek ons/pay yalnız
gider oranıyla yavaşça azalır).
prem_D = ln(c_GLD_D) − ln(oz_med_D × spot(16:00 ET, D))   -> D kapanışından ve NAV yayınından SONRA hesaplanabilir; sinyalde prem_{t-1}.
Yaklaşık gün-içi prim (son ~2 yıl): GLD 14:30 ET (saatlik bar 13:30 kapanışı) / [oz_med_{t-1} × spot(14:30 ET, 14:00 ve 15:00 ET Dukascopy doğrusal ara değer)].
5 dk (son 60 gün): GLD 15:00 ET (14:55 barı kapanışı) / [oz_med_{t-1} × xau_cut (15:00 ET)].
"""
from common import *
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
nh = pd.read_parquet(f"{P}/etf_gld_navhist.parquet"); nh.index = pd.to_datetime(nh.index)
sp, hh = lbma_pm_spot()
oz = (nh.nav / sp.reindex(nh.index)).replace([np.inf, -np.inf], np.nan)
oz_med = oz.rolling(20, min_periods=10).median()
print("ons/pay günlük log değişim std (ham, medyan):", np.log(oz).diff().std(), np.log(oz_med).diff().std())
ozm = oz_med.reindex(d.index).ffill(limit=3)        # aynı gün D
navd = nh.nav.reindex(d.index)
prem = np.log(d.c_GLD) - np.log(ozm * d.xau_close)
prem_raw = np.log(d.c_GLD) - np.log(navd * d.xau_close / sp.reindex(d.index))
prem_nav = np.log(d.c_GLD / navd)   # klasik (NAV LBMA PM anında, fiyat 16:00 ET) -> spot hareketi içerir
desc = pd.DataFrame({"prem_bps": prem * 1e4, "prem_raw_bps": prem_raw * 1e4})
yr = desc.groupby(desc.index.year).agg(["mean", "std"]).round(1)
print(yr)
ac = {k: round(prem.autocorr(k), 3) for k in (1, 2, 3, 5, 10)}
print("prim otokorelasyon:", ac)
acs = {y: round(prem[str(y)].autocorr(1), 2) for y in range(2008, 2027)}
print("yıllık AC(1):", acs)
rows = []
rG = lr(d.c_GLD); rI = lr(d.c_IAU); rS = lr(d.xau_close)   # spot 16:00 ET -> 16:00 ET
rel = rG - rS
# tanı (ULAŞILAMAZ: prim gün t kapanışında, NAV akşam) -> ertesi gün
for h in HS:
    rows.append(test("b_prem_diag", f"b_prem_t_relGLDspot_h{h}", "prem_t (kapanış; işlem dışı tanı) -> GLD−spot", prem, fwd(rel, h), h, note="tanı; ulaşılamaz bilgi"))
    rows.append(test("b_prem_diag", f"b_prem_t_GLD_h{h}", "prem_t (kapanış; işlem dışı tanı) -> GLD", prem, fwd(rG, h), h, note="tanı; ulaşılamaz bilgi"))
# uygulanabilir: prem_{t-1}
p1 = prem.shift(1)
z1 = (p1 - p1.rolling(250, min_periods=120).mean().shift(1)) / p1.rolling(250, min_periods=120).std().shift(1)
for nm, x in [("prem_l1", p1), ("zprem_l1", z1), ("dprem_l1", prem.shift(1) - prem.shift(2))]:
    for h in HS:
        rows.append(test("b_prem", f"b_{nm}_GLD_h{h}", f"{nm} (t-1 kapanış, NAV t-1 akşamı) -> GLD", x, fwd(rG, h), h))
        rows.append(test("b_prem", f"b_{nm}_relGLDspot_h{h}", f"{nm} -> GLD−spot", x, fwd(rel, h), h))
    rows.append(test("b_prem", f"b_{nm}_IAU_h1", f"{nm} -> IAU", x, fwd(rI, 1), 1))
print("placebo prem_l1 -> GLD:", placebo_lead(p1, rG, 1))

# akış zamanlaması: pay sayısı değişimi primle aynı gün mü ilişkili?
f1 = np.log(nh.shares).diff()
pr_nh = prem.reindex(nh.index)
tim = {f"corr(f1_D, prem_D{k:+d})": round(f1.corr(pr_nh.shift(-k)), 3) for k in (-2, -1, 0, 1)}
print("akış–prim zamanlaması:", tim)

# gün-içi yaklaşık prim (saatlik, ~2 yıl)
gh = pd.read_parquet(f"{P}/yahoo_h/GLD.parquet")
gh.index = gh.index.tz_convert("America/New_York")
b1330 = gh[(gh.index.hour == 13) & (gh.index.minute == 30)]["close"]; b1330.index = pd.to_datetime(b1330.index.date)
x = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")["c"]; x.index = (x.index + pd.Timedelta(hours=1)).tz_convert("America/New_York")
x14 = x[x.index.hour == 14]; x14.index = pd.to_datetime(x14.index.date)
x15 = x[x.index.hour == 15]; x15.index = pd.to_datetime(x15.index.date)
x15 = x15.reindex(d.index).fillna(d.xau_cut); x14 = x14.reindex(d.index)
s1430 = np.exp((np.log(x14) + np.log(x15)) / 2)
oz_l1 = oz_med.reindex(d.index).ffill(limit=3).shift(1)
pin = np.log(b1330.reindex(d.index)) - np.log(oz_l1 * s1430)
pin = pin - pin.rolling(60, min_periods=20).median().shift(1)   # yavaş seviye farkını (bid/mid, oz kestirimi) çıkar
print("gün-içi prim (14:30 ET) gözlem:", pin.notna().sum(), "std bps", round(pin.std() * 1e4, 1), "corr(pin, prem_t)", round(pin.corr(prem), 3), "corr(pin, prem_t-1)", round(pin.corr(prem.shift(1)), 3))
for h in HS:
    rows.append(test("b_prem_intraday", f"b_pin1430_GLD_h{h}", "GLD gün-içi prim 14:30 ET (saatlik) -> GLD", pin, fwd(rG, h), h, note="2024-12+; tamamı OOS"))
    rows.append(test("b_prem_intraday", f"b_pin1430_relGLDspot_h{h}", "GLD gün-içi prim 14:30 ET -> GLD−spot", pin, fwd(rel, h), h, note="2024-12+; tamamı OOS"))
# 5 dk 15:00 ET (60 gün)
g5 = pd.read_parquet(f"{P}/yahoo_5m/GLD.parquet"); g5.index = g5.index.tz_convert("America/New_York")
b1455 = g5[(g5.index.hour == 14) & (g5.index.minute == 55)]["close"]; b1455.index = pd.to_datetime(b1455.index.date)
p5 = np.log(b1455.reindex(d.index)) - np.log(oz_l1 * d.xau_cut)
p5 = p5 - p5.mean()
dd5 = pd.DataFrame({"p5": p5, "r1": fwd(rG, 1), "rel1": fwd(rel, 1), "prem_t": prem}).dropna()
print("5dk 15:00 ET prim: n", len(dd5), "std bps", round(dd5.p5.std() * 1e4, 1), "corr(p5, prem_t)", round(dd5.p5.corr(dd5.prem_t), 2),
      "corr(p5, GLD t+1)", round(dd5.p5.corr(dd5.r1), 3), "corr(p5, GLD−spot t+1)", round(dd5.rel1.corr(dd5.p5), 3))
rows.append(test("b_prem_intraday", "b_p5_1500_GLD_h1", "GLD 15:00 ET prim (5dk) -> GLD", p5, fwd(rG, 1), 1, note="son 60 gün"))

res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/b_premium_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]].round(3).to_string())
pd.DataFrame({"prem": prem, "prem_raw": prem_raw, "pin1430": pin}).to_parquet(f"{OUT}/b_premium_series.parquet")

# Strateji (IS seçimi): prem_l1 işaretine göre karşıt; |z|>1 eşiği IS'te seçilir
srows = []
best = None
for thr in (0.0, 0.5, 1.0, 1.5):
    for h in HS:
        pos = (-np.sign(z1) * (z1.abs() > thr)).fillna(0)
        r = strat_eval(f"prim_kontra_z{thr}", pos, "GLD", h, d)
        for rr_ in r: rr_["thr"] = thr
        srows += r
sr = pd.DataFrame(srows)
isb = sr[(sr["mode"] == "long_only") & (sr.cost == "base")].sort_values("shdm_is", ascending=False).iloc[0]
print("IS seçimi (yalnız uzun, demeaned IS Sharpe):", isb.strategy, isb.h, isb.shdm_is, "-> OOS", isb.sh_oos, isb.shdm_oos)
sr.to_csv(f"{OUT}/b_premium_strategies.csv", index=False)
print(sr[["strategy", "h", "mode", "cost", "sh_is", "sh_oos", "sh_22", "shdm_is", "shdm_oos", "bh_oos", "exposure_long", "turnover_yr"]].to_string())
