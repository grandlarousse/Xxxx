"""(a) CFTC COT konumlanma -> VİOP fwd1/3/5/10.
Bilgi zamanı: Salı pozisyonu, Cuma 15:30 ET (20:30/19:30 UTC) yayın; panelde Cuma 21:00 UTC mevcut -> ilk kullanım Pazartesi (t) 15:00 UTC öncesi.
Hükümet kapanması dönemlerinde (2018-12-21..2019-03-08, 2025-10-01..2026-01-23) yayın gecikti -> bu günlerde sinyal NaN (ana sürüm) ve ayrıca dahil sürüm.
Haftalık özellikler ham CFTC dosyasından hesaplanır (52/156 hafta z), gün t'ye panelin cot_gold_reportdate (as-of) anahtarıyla eşlenir.
"""
from common import *
import glob, zipfile

cot = []
for f in sorted(glob.glob(f"{S}/data/cftc/*.zip")):
    z = zipfile.ZipFile(f)
    for nm in z.namelist():
        cot.append(pd.read_csv(z.open(nm), low_memory=False))
cot = pd.concat(cot)
cot["code"] = cot["CFTC_Contract_Market_Code"].astype(str).str.strip().str.zfill(6)
dcol = [c for c in cot.columns if c.startswith("Report_Date_as_YYYY")][0]
cot["rd"] = pd.to_datetime(cot[dcol])

def weekly(code):
    g = cot[cot.code == code].drop_duplicates("rd").set_index("rd").sort_index()
    oi = g["Open_Interest_All"].astype(float)
    swS = "Swap__Positions_Short_All" if "Swap__Positions_Short_All" in g else "Swap_Positions_Short_All"
    w = pd.DataFrame(index=g.index)
    w["mm_net_oi"] = (g["M_Money_Positions_Long_All"] - g["M_Money_Positions_Short_All"]) / oi
    w["swap_net_oi"] = (g["Swap_Positions_Long_All"] - g[swS]) / oi
    w["pm_net_oi"] = (g["Prod_Merc_Positions_Long_All"] - g["Prod_Merc_Positions_Short_All"]) / oi
    w["d_mm"] = (g["M_Money_Positions_Long_All"] - g["M_Money_Positions_Short_All"]).diff() / oi.shift(1)
    w["d_mml"] = g["M_Money_Positions_Long_All"].diff() / oi.shift(1)
    w["d_mms"] = g["M_Money_Positions_Short_All"].diff() / oi.shift(1)
    w["d_oi"] = np.log(oi).diff()
    return w

wg = weekly("088691"); ws = weekly("084691")
F = pd.DataFrame(index=wg.index)
F["g_mm_z52"] = zroll(wg.mm_net_oi, 52)
F["g_mm_z156"] = zroll(wg.mm_net_oi, 156)
F["g_dmm_z52"] = zroll(wg.d_mm, 52)                  # haftalık akış (z)
F["g_dmm_4w"] = zroll(wg.d_mm.rolling(4).sum(), 52)  # 4 haftalık akış
F["g_swap_z52"] = zroll(wg.swap_net_oi, 52)
F["g_pm_z52"] = zroll(wg.pm_net_oi, 52)
F["g_dmml_z52"] = zroll(wg.d_mml, 52)
F["g_dmms_z52"] = zroll(wg.d_mms, 52)                # kısa kapama (negatif) = short covering
F["g_doi_x_dmm"] = zroll(wg.d_oi, 52) * np.sign(wg.d_mm)  # OI artışı + MM yönü
F["s_mm_z52"] = zroll(ws.mm_net_oi.reindex(wg.index), 52)
F["s_dmm_z52"] = zroll(ws.d_mm.reindex(wg.index), 52)
F.to_csv(f"{OUT}/cot_weekly_features.csv")

def to_daily(panel, Fw):
    rd = pd.to_datetime(panel["cot_gold_reportdate"])
    X = Fw.reindex(rd.values); X.index = panel.index
    return X

BAD = lambda idx: pd.Series(((idx >= "2018-12-21") & (idx <= "2019-03-08")) | ((idx >= "2025-10-01") & (idx <= "2026-01-23")), index=idx)
X = to_daily(D, F)
bad = BAD(D.index)
Xc = X.copy(); Xc[bad.values] = np.nan
Xc.to_csv(f"{OUT}/a_cot_features_daily.csv")
fresh = pd.Series(pd.to_datetime(D.cot_gold_reportdate) != pd.to_datetime(D.cot_gold_reportdate).shift(1), index=D.index)  # rapordan sonraki ilk VİOP günü

DESC = {"g_mm_z52": "COT altın MM net/OI 52h z (seviye)", "g_mm_z156": "COT altın MM net/OI 156h z", "g_dmm_z52": "COT altın MM net haftalık değişim/OI z52",
        "g_dmm_4w": "COT altın MM net 4h değişim z52", "g_swap_z52": "COT altın swap net/OI z52", "g_pm_z52": "COT altın üretici net/OI z52",
        "g_dmml_z52": "COT altın MM long değişim z52", "g_dmms_z52": "COT altın MM short değişim z52", "g_doi_x_dmm": "COT altın OI değişim z × sign(ΔMM)",
        "s_mm_z52": "COT gümüş MM net/OI z52", "s_dmm_z52": "COT gümüş MM net değişim z52"}

rows = []
for k, desc in DESC.items():
    rows += T(Xc[k], "cot", f"cot_{k}", desc, note="kapanma dönemleri dışlandı; bilgi: Cuma 21:00 UTC -> Pzt")
df = save(rows, "a_cot_ic"); show(df)

# --- sağlamlık: kapanma dahil, yalnız rapor sonrası ilk gün (h=5, örtüşmesiz yakın)
rows2 = []
for k in DESC:
    rows2 += T(X[k], "cot_robust", f"cot_{k}_incl_shutdown", DESC[k] + " (kapanma dahil)", hs=(5,), note="robust")
    xf = Xc[k].where(fresh)
    rows2 += T(xf, "cot_robust", f"cot_{k}_fresh", DESC[k] + " (yalnız rapor sonrası ilk gün)", hs=(5,), note="robust")
df2 = save(rows2, "a_cot_robust"); show(df2)

# --- erken dönem (spot 2010-2016)
Xs = to_daily(SP, F)
rows3 = []
for k in DESC:
    rows3 += T_early(Xs[k], "cot", f"cot_{k}", DESC[k])
df3 = save(rows3, "a_cot_early"); show(df3, ("test_id", "h", "n", "ic", "t", "yrs_same"))

# --- kural testi (literatür: r2 §3.9): 156h z>+2 kısa, z<-2 uzun; ayrıca 52h z ±1.5. Monday-fresh değil, her gün tutulan pozisyon.
bt = []
for k, thr in [("g_mm_z156", 2.0), ("g_mm_z52", 1.5)]:
    pos = pd.Series(np.where(Xc[k] > thr, -1.0, np.where(Xc[k] < -thr, 1.0, 0.0)), index=D.index)
    for h in (5,):
        t = legs_table(pos, h, f"contrarian {k} ±{thr}"); bt.append(t)
        print(k, thr, "aktif gün oranı", round((pos != 0).mean(), 3), "uzun", int((pos > 0).sum()), "kısa", int((pos < 0).sum()))
bt = pd.concat(bt); bt.to_csv(f"{OUT}/a_cot_rules.csv", index=False)
print(bt[(bt.cost_bps == 5) | (bt.leg == "buyhold")].to_string(index=False))
for k, thr in [("g_mm_z156", 2.0), ("g_mm_z52", 1.5)]:
    for h in (5,):
        st = dict(n=int((Xc[k].abs() > thr).sum()))
        pos = pd.Series(np.where(Xc[k] > thr, -1.0, np.where(Xc[k] < -thr, 1.0, 0.0)), index=D.index)
        s = rule_stats(pos, 5)
        register(AG, "cot_rule", f"cot_rule_{k}_{thr}", f"COT kontraryen kural {k} ±{thr}", 5, s, "kural; aktif günlerde pos×fwd5 ortalaması (bps), NW t")
        print("rule", k, thr, {a: (round(s[a], 3) if isinstance(s[a], float) else s[a]) for a in ("ic", "t", "n", "t_is", "t_oos")})
