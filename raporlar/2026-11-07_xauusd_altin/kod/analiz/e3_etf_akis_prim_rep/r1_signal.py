"""m_t'yi ham Dukascopy saatliğinden kur; zaman damgalarını doğrula; panel_etf ile karşılaştır."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
days = nyse_days("2008-01-01")
xs = xau_hourly()
print("xau son fiyat anı:", xs.index.max(), "| ilk:", xs.index.min())
cut = et_times(days, 15); cut14 = et_times(days, 14); clo = et_times(days, 16)
xc, tsc = snap(xs, cut); x14, ts14 = snap(xs, cut14); xcl, tscl = snap(xs, clo)
xc.index = days; x14.index = days; xcl.index = days; tsc.index = days; tscl.index = days
# zaman doğrulama: kullanılan fiyat anı <= 15:00 ET
lag_min = (cut.values - tsc.values) / np.timedelta64(1, "m")
print("cut fiyat anı 15:00 ET'den önce/eşit mi:", bool((lag_min >= 0).all()), "| bayatlık dakika dağılımı:", pd.Series(lag_min).value_counts().head(4).to_dict())
print("cut UTC saat dağılımı:", pd.Series(cut.hour).value_counts().to_dict())
# yerel ET saatinde fiyat anı
loc = pd.DatetimeIndex(tsc.values).tz_localize("UTC").tz_convert(NY)
print("fiyat anı ET saati dağılımı:", pd.Series(loc.hour).value_counts().to_dict())
# DST geçiş günlerinde örnek
for dd in ["2024-03-08", "2024-03-11", "2024-11-01", "2024-11-04", "2025-03-10", "2025-11-03"]:
    t = pd.Timestamp(dd)
    if t in days:
        i = days.get_loc(t); print(dd, "cut UTC", cut[i], "fiyat anı", pd.Timestamp(tsc.iloc[i]), "close UTC", clo[i])
m = np.log(xc / xcl.shift(1)); m14 = np.log(x14 / xcl.shift(1))
pe = pd.read_parquet(f"{P}/panel_etf.parquet"); pe.index = pd.to_datetime(pe.index)
mp = np.log(pe.xau_cut / pe.xau_close.shift(1))
cmp = pd.concat([m.rename("mine"), mp.rename("panel")], axis=1).dropna()
print("m: benim n", m.notna().sum(), "panel n", mp.notna().sum(), "| ortak", len(cmp), "| max |fark|", float((cmp.mine - cmp.panel).abs().max()), "| corr", round(cmp.mine.corr(cmp.panel), 6))
print("panel cut_utc ile benim cut eşit mi:", bool((pd.to_datetime(pe.cut_utc).reindex(days).dt.tz_convert("UTC").values == cut.values).all()) if "cut_utc" in pe else "yok")
sig = pd.DataFrame({"xau_cut": xc, "xau_14": x14, "xau_close": xcl, "m": m, "m14": m14, "cut_utc": cut, "price_ts_utc": pd.DatetimeIndex(tsc.values).tz_localize("UTC")})
sig["sd60"] = sig.m.rolling(60, min_periods=40).std().shift(1); sig["zm"] = sig.m / sig.sd60
sig["sd60_14"] = sig.m14.rolling(60, min_periods=40).std().shift(1); sig["zm14"] = sig.m14 / sig.sd60_14
sig.to_parquet(f"{OUT}/sig_m.parquet")
print(sig[["m", "zm", "m14"]].describe().round(4))
