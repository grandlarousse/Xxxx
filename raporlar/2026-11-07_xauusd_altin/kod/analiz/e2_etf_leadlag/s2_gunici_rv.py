"""s2 (aile b): gün içi senkron göreli değer, cutoff 15:00 ET.
b1 (uzun dönem, Dukascopy): pencere [t-1 15:00 ET -> t 15:00 ET]. g_t = log(xau_cut_t/xau_cut_{t-1}); X_t = dk_*_cut log değişimleri (aynı pencere).
    Yuvarlanan 250 gün OLS (beta_{t-1}, yalnız geçmiş) -> artık e_t (gün t 15:00 ET'de bilinir) -> GLD/GDX/SLV fwd (gün t 16:00 ET giriş).
    Veri 2016+ (DXY 2017-12+, T-bond 2018-01+) -> bu aile için sözde-IS 2018-2021, OOS 2022+ (2008-2017 IS'i veri yok).
b2 (son 730 gün, Yahoo saatlik ETF): pencere [t-1 16:00 ET kapanış -> t 14:30 ET] (13:30 ET barının kapanışı; 14:30 < 15:00 cutoff).
    GDX/GDXJ artığı (GLD+SPY'ye göre, beta = geçmiş 250 günlük günlük getiri betası), SLV-GLD, SIL-SLV. Yalnız keşif amaçlı (N≈700).
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SLV", "SIL", "SPY"]}
rows = []
# ---------------- b1
lib_altin.IS_END = pd.Timestamp("2021-12-31")
g = np.log(d["xau_cut"]).diff()
X = pd.DataFrame({s: np.log(d[f"dk_{s}_cut"]).diff() for s in ["XAGUSD", "DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "USDJPY", "EURUSD", "BTCUSD", "COPPERCMDUSD", "BRENTCMDUSD"]})
# boşluk kontrolü: dk_*_cut ardışık iki gün mevcut değilse NaN kalır (diff zaten NaN)
MODELS = {"M1_makro": ["DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "USDJPY"],
          "M2_makro_gumus": ["DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "USDJPY", "XAGUSD"],
          "M3_genis": ["DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "USDJPY", "XAGUSD", "BTCUSD", "COPPERCMDUSD", "BRENTCMDUSD"],
          "M4_gumus": ["XAGUSD"]}
SIG = {}
for mn, cols in MODELS.items():
    B = roll_beta2(g, X[cols], 250, 120).shift(1)
    yhat = sum(B[c] * X[c] for c in cols)
    e = g - yhat
    for k in (1, 3):
        x = e.rolling(k, min_periods=k).sum()       # gün t 15:00 ET'de biter -> gün t'de bilinir (shift yok)
        SIG[(mn, k)] = x
        for T in ["GLD", "GDX", "SLV"]:
            for h in HS:
                st = test("b_gunici_rv", f"b1_{mn}_k{k}_{T}_h{h}", x, R[T], h, f"altın artığı [{mn}] 15:00ET penceresi k={k} -> {T}", note="IS=2018-2021 OOS=2022+")
                rows.append(st)
# ham altın gün içi hareketi (t-1 16:00 ET kapanış -> t 15:00 ET) — kıyas (öz momentum/dönüş; zaman serisi ajanıyla örtüşür)
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1))
for T in ["GLD", "GDX"]:
    for h in HS:
        rows.append(test("b_gunici_rv", f"b1_xau_intraday_{T}_h{h}", gi, R[T], h, "xau [t-1 16:00ET -> t 15:00ET] -> " + T, note="IS=2018-2021 OOS=2022+"))
lib_altin.IS_END = pd.Timestamp("2017-12-31")
# ---------------- b2
def px1430(tk):
    fn = f"{P}/yahoo_h/{tk}.parquet"
    h = pd.read_parquet(fn); et = h.index.tz_convert("America/New_York")
    m = (et.hour == 13) & (et.minute == 30)
    s = pd.Series(h["close"].values[m], index=pd.DatetimeIndex(et[m].date))
    return s[~s.index.duplicated()]
P14 = {t: px1430(t) for t in ["GLD", "GDX", "GDXJ", "SLV", "SIL", "SPY"]}
lib_altin.IS_END = pd.Timestamp("2025-05-31")   # yalnız keşif: ilk yarı / ikinci yarı
# temettü düzeltmesi: c_ adjclose; saatlik ham fiyat. Önceki kapanış için ham kapanış (yahoo close) kullan.
RAWC = {t: pd.read_parquet(f"{P}/yahoo/{t}.parquet")["close"] for t in P14}
I = {}
for t in P14:
    pc = RAWC[t].reindex(d.index).shift(1)
    I[t] = np.log(P14[t].reindex(d.index)) - np.log(pc)      # [t-1 16:00 -> t 14:30 ET]
I = pd.DataFrame(I)
cov = I.notna().all(axis=1); print("b2 gün sayısı", int(cov.sum()), I[cov].index.min(), I[cov].index.max())
# betalar günlük getirilerden (geçmiş 250 gün, t-1'e kadar)
Bg = roll_beta2(R["GDX"], pd.concat([R["GLD"], R["SPY"]], axis=1).set_axis(["GLD", "SPY"], axis=1), 250, 120).shift(1)
Bj = roll_beta2(R["GDXJ"], pd.concat([R["GLD"], R["SPY"]], axis=1).set_axis(["GLD", "SPY"], axis=1), 250, 120).shift(1)
bs = roll_beta(R["SLV"], R["GLD"], 250, 120).shift(1); bsi = roll_beta(R["SIL"], R["SLV"], 250, 120).shift(1)
INTR = {"GDX~GLD+SPY": I.GDX - Bg.GLD * I.GLD - Bg.SPY * I.SPY, "GDXJ~GLD+SPY": I.GDXJ - Bj.GLD * I.GLD - Bj.SPY * I.SPY,
        "SLV~GLD": I.SLV - bs * I.GLD, "SIL~SLV": I.SIL - bsi * I.SLV, "GLD_raw": I.GLD}
for nm, x in INTR.items():
    SIG[("b2", nm)] = x
    tg = {"GDX~GLD+SPY": ["GDX", "GLD"], "GDXJ~GLD+SPY": ["GDXJ", "GLD"], "SLV~GLD": ["SLV", "GLD"], "SIL~SLV": ["SIL", "SLV"], "GLD_raw": ["GLD", "GDX"]}[nm]
    for T in tg:
        for h in HS:
            rows.append(test("b_gunici_rv", f"b2_{nm}_{T}_h{h}", x, R[T], h, f"gün içi artık [{nm}] t-1 16:00->t 14:30 ET -> {T}", note="hourly 730d; IS=ilk yarı (≤2025-05) OOS=ikinci yarı"))
lib_altin.IS_END = pd.Timestamp("2017-12-31")
res = pd.DataFrame(rows)
cols = ["test_id", "h", "ic", "t", "t_is", "t_oos", "ic_oos", "t_22", "yrs_same_sign", "yrs", "n"]
res[cols].to_csv(f"{OUT}/s2_gunici_rv.csv", index=False); pd.to_pickle(SIG, f"{OUT}/s2_signals.pkl")
pd.set_option("display.width", 250)
print(res[cols].round(3).to_string())
