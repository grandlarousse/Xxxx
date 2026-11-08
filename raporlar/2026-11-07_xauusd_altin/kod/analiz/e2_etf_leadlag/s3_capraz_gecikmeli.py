"""s3 (aile c): gecikmeli çapraz varlıklar -> GLD / GDX fwd1/3/5.
Bilgi zamanları (gün t sinyali, cutoff t 15:00 ET = yaz 19:00 / kış 20:00 UTC):
  ABD kapanışları (y_*; ETF/hisse 16:00 ET, VIX/GVZ/OVX 16:15 ET, vadeli/DXY 17:00 ET): değer = t-1 kapanışı; d1 = (t-2 -> t-1).
  BTC (Yahoo, 24:00 UTC bar + 1 saat pay): t-1 UTC günü kapanışı (t 01:00 UTC).
  ust_* : t-1 (D 22:00 UTC).
  Avrupa (y_; DAX/STOXX 17:30 CET = 11:30 ET, FTSE/LSE 16:30 Londra = 11:30 ET, Xetra 4GLD): gün t kapanışı (cutoff'tan önce).
  Asya (y_; Nikkei/1328.T 06:30 UTC, Şanghay/518880 07:00 UTC, HK 08:10 UTC, KOSPI 06:30, ASX ~05-06 UTC): gün t kapanışı.
  SHFE AU0 gündüz kapanışı 07:00 UTC t, xau_p07 ve dk_USDCNH_p07 07:00 UTC t.
Senkronsuzluk: Avrupa/Asya gün-t bilgisi gün t 16:00 ET GLD kapanışına zaten girer; yalnız t kapanışı SONRASI getiriyi öngörmesi değerlidir.
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX"]}
LOGP = {"DXY": "y_DX_Y_NYB", "UUP": "y_UUP", "TLT": "y_TLT", "TIP": "y_TIP", "SPY": "y_SPY", "NDX": "y__NDX", "HYG": "y_HYG", "EEM": "y_EEM", "FXI": "y_FXI",
        "VIX": "y__VIX", "GVZ": "y__GVZ", "OVX": "y__OVX", "MOVE": "y__MOVE", "WTI": "y_CL_F", "BAKIR": "y_HG_F", "PLATIN": "y_PL_F", "BTC": "y_BTC_USD",
        "DAX": "y__GDAXI", "STOXX50": "y__STOXX50E", "FTSE": "y__FTSE", "XETRA_GOLD_EUR": "y_4GLD_DE", "SGLN_L": "y_SGLN_L", "PHAU_L": "y_PHAU_L",
        "NIKKEI": "y__N225", "HSI": "y__HSI", "KOSPI": "y__KS11", "ASX200": "y__AXJO", "SSE": "y_000001_SS", "CN_GOLD_ETF_518880": "y_518880_SS",
        "HK_GOLD_ETF_2840": "y_2840_HK", "ZHAOJIN_1818": "y_1818_HK", "ZIJIN_2899": "y_2899_HK", "SHANDONG_600547": "y_600547_SS", "JP_GOLD_ETF_1328": "y_1328_T"}
LEVEL = {"UST10": "ust_nom10", "REAL10": "ust_real10", "UST2": "ust_nom2", "BE10": "ust_be10"}
FEAT = {}
for nm, c in LOGP.items():
    lp = np.log(d[c].astype(float))
    FEAT[(nm, "d1")] = lp.diff(); FEAT[(nm, "d5")] = lp.diff(5)
for nm, c in LEVEL.items():
    FEAT[(nm, "d1")] = d[c].diff(); FEAT[(nm, "d5")] = d[c].diff(5)
cv = d["ust_nom10"] - d["ust_nom2"]; FEAT[("EGRI_10_2", "d1")] = cv.diff(); FEAT[("EGRI_10_2", "d5")] = cv.diff(5)
for nm in ("VIX", "GVZ"):
    FEAT[(nm, "lvlz")] = zpast(np.log(d[LOGP[nm]]), 250)
# Şanghay primi (07:00 UTC t): vadeli carry içerir -> değişim ve 20 gün sapması
prem = np.log(d["shfe_AU0_c"] * 31.1035 / d["dk_USDCNH_p07"]) - np.log(d["xau_p07"])
prem[(prem - prem.rolling(60, min_periods=20).median()).abs() > 0.05] = np.nan   # açık veri hatalarını at (yalnız geçmiş medyanı değil: ±%5 kaba filtre)
FEAT[("SHFE_PREM", "d1")] = prem.diff(); FEAT[("SHFE_PREM", "dev20")] = prem - prem.shift(1).rolling(20, min_periods=10).mean()
# Çin altın ETF'i 518880 primi (07:00 UTC; xau 07 UTC × USDCNH 07 UTC'ye göre): seviye keyfi -> d1 ve 20 gün sapma
cn = np.log(d["y_518880_SS"]) - np.log(d["xau_p07"] * d["dk_USDCNH_p07"])
cn[d["y_518880_SS_avail"].dt.normalize().dt.tz_localize(None) != d.index] = np.nan   # yalnız gün t'de gerçekten işlem gördüyse
FEAT[("CN_ETF_PREM", "d1")] = cn.diff(); FEAT[("CN_ETF_PREM", "dev20")] = cn - cn.shift(1).rolling(20, min_periods=10).mean()
rows = []
for (nm, tr), x in FEAT.items():
    for T in ["GLD", "GDX"]:
        for h in HS:
            rows.append(test("c_capraz_gecikmeli", f"c_{nm}_{tr}_{T}_h{h}", x, R[T], h, f"{nm} {tr} -> {T}"))
res = pd.DataFrame(rows)
cols = ["test_id", "h", "ic", "t", "t_is", "t_oos", "ic_oos", "t_22", "yrs_same_sign", "yrs", "n"]
res[cols].to_csv(f"{OUT}/s3_capraz.csv", index=False); pd.to_pickle(FEAT, f"{OUT}/s3_signals.pkl")
pd.set_option("display.width", 250)
print(res[cols].round(3).sort_values("t", key=abs, ascending=False).head(45).to_string()); print("n", len(res))
# IS-OOS aynı işaret ve OOS |t|>=2 olanlar
f = res[(np.sign(res.t_is) == np.sign(res.t_oos)) & (res.t_oos.abs() >= 2) & (res.t_is.abs() >= 1.5)]
print(f[cols].round(3).to_string())
