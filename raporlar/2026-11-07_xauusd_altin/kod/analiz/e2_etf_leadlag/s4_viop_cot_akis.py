"""s4: aile d (VİOP), e (COT), f (GLD pay akışı — ek).
d: VİOP aktif kontrat uzlaşması gün t ~15:05-15:15 UTC VWAP (< 15:00 ET cutoff = 19:00/20:00 UTC). Spot xau_p15 = 15:00 UTC.
   baz_t = log(v_settle) - log(xau_p15); yıllık örtük carry = baz/(dte/365); fazla carry = örtük - nom3m/100 (ust t-1). Sapma = x - geçmiş 20 gün ort.
   Hacim/OI: log(toplam hacim) z (geçmiş 60g), Δlog(toplam OI). Gram altın primi tr_prem_matched (15:10 UTC): seviye z (250g), d1, d5.
   Bu ailede veri 2017-03+ -> IS 2017-03..2017-12 çok kısa; split_stats IS sütunu anlamsız. Burada sözde-IS 2017-03..2021-12, OOS 2022+.
e: COT yönetilen para net/OI (Salı pozisyonu, Cuma 21:00 UTC yayın -> Pazartesi'den itibaren gün t'de bilinir). z (geçmiş 750 gün), haftalık değişim, uç (IS %10/%90).
f: GLD dolaşımdaki pay Δlog (as-of t-1; SSGA D değerini D 23:00 UTC'de yayınlar varsayımı) ve bir gün daha gecikmeli (t-2).
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "SLV"]}
pv = pd.read_parquet(f"{P}/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
pv = pv.reindex(d.index)   # Türkiye tatilinde NaN
rows = []
# ---------- d: VİOP
lib_altin.IS_END = pd.Timestamp("2021-12-31")
basis = np.log(pv["v_settle"]) - np.log(pv["xau_p15"])
dte = pv["v_dte"].astype(float)
impl = basis / (dte.clip(lower=5) / 365.0)
xc = impl - d["ust_nom3m"] / 100.0
xc[(xc - xc.rolling(60, min_periods=20).median()).abs() > 0.15] = np.nan
F = {}
F["VIOP_fazla_carry_dev20"] = xc - xc.shift(1).rolling(20, min_periods=10).mean()
F["VIOP_baz_d1"] = basis.where(pv["v_code"] == pv["v_code"].shift(1)).diff().where(pv["v_code"] == pv["v_code"].shift(1))
lv = np.log(pv["v_tot_volume"].astype(float).replace(0, np.nan))
F["VIOP_hacim_z60"] = (lv - lv.shift(1).rolling(60, min_periods=30).mean()) / lv.shift(1).rolling(60, min_periods=30).std()
F["VIOP_toplamOI_d1"] = np.log(pv["v_tot_oi"].astype(float).replace(0, np.nan)).diff()
F["VIOP_toplamOI_d5"] = np.log(pv["v_tot_oi"].astype(float).replace(0, np.nan)).diff(5)
tp = d["viop_tr_prem_matched"]
F["TR_prem_z250"] = zpast(tp, 250, 60)
F["TR_prem_d1"] = tp.diff(); F["TR_prem_d5"] = tp.diff(5)
for nm, x in F.items():
    for T in ["GLD", "GDX"]:
        for h in HS:
            rows.append(test("d_viop", f"d_{nm}_{T}_h{h}", x, R[T], h, f"{nm} (gün t 15:10 UTC) -> {T}", note="IS=2017-03..2021 OOS=2022+"))
lib_altin.IS_END = pd.Timestamp("2017-12-31")
# ---------- e: COT
s = d["cot_gold_mm_net_oi"]
new = s.ne(s.shift(1)) & s.notna()
vals = s[new]; chg = vals.diff(); chg_d = chg.reindex(d.index).ffill()
z = zpast(s, 750, 250)
G = {"COT_mmnetOI_z750": z, "COT_mmnetOI_haftalik_deg": chg_d}
zi = z[z.index <= IS_END].dropna(); hi, lo = zi.quantile(0.9), zi.quantile(0.1)
G["COT_uc_q10_90"] = pd.Series(np.where(z > hi, 1.0, np.where(z < lo, -1.0, 0.0)), index=d.index).where(z.notna())
SH = ((d.index >= "2018-12-22") & (d.index <= "2019-03-15")) | ((d.index >= "2025-10-01") & (d.index <= "2025-12-31"))
for nm, x in G.items():
    for T in ["GLD", "GDX"]:
        for h in (1, 3, 5, 10):
            rows.append(test("e_cot", f"e_{nm}_{T}_h{h}", x, R[T], h, f"{nm} -> {T}"))
            rows.append(test("e_cot", f"e_{nm}_{T}_h{h}_kapanma_haric", x.where(~SH), R[T], h, f"{nm} (hükümet kapanması dışlanmış) -> {T}", note="robust"))
# ---------- f: GLD pay akışı
sh = np.log(d["flow_gld_shares"].astype(float))
dsh = sh.diff(); dsh[dsh.abs() > 0.1] = np.nan
H = {"GLD_pay_d1_lag1": dsh, "GLD_pay_d1_lag2": dsh.shift(1), "GLD_pay_d5": dsh.rolling(5, min_periods=4).sum()}
for nm, x in H.items():
    for T in ["GLD", "GDX"]:
        for h in HS:
            rows.append(test("f_akis", f"f_{nm}_{T}_h{h}", x, R[T], h, f"{nm} -> {T}"))
res = pd.DataFrame(rows)
cols = ["test_id", "h", "ic", "t", "t_is", "t_oos", "ic_oos", "t_22", "yrs_same_sign", "yrs", "n"]
res[cols].to_csv(f"{OUT}/s4_viop_cot_akis.csv", index=False)
pd.to_pickle({**F, **G, **H}, f"{OUT}/s4_signals.pkl")
pd.set_option("display.width", 250)
print(res[cols].round(3).to_string()); print("n", len(res))
