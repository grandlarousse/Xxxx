"""Dukascopy zaman damgası doğrulaması: GLD NAV (LBMA PM 15:00 Londra'dan hesaplanır) değişimi hangi saatteki spot değişimiyle en uyumlu?
Ayrıca GLD kapanış (16:00 ET) getirisi hangi saatteki spot getirisiyle en uyumlu?"""
from rc import *
import warnings; warnings.filterwarnings("ignore")
xs = xau_hourly()
nh = pd.read_parquet(f"{P}/etf_gld_navhist.parquet"); nh.index = pd.to_datetime(nh.index).normalize(); nh = nh[~nh.index.duplicated()]
nh = nh["2010":"2026-10"]
dn = np.log(nh.nav).diff()
out = {}
for hh in (13, 14, 15, 16, 17):
    t = pd.DatetimeIndex([pd.Timestamp(f"{d.date()} {hh}:00", tz="Europe/London").tz_convert("UTC") for d in nh.index])
    s, _ = snap(xs, t, 0); s.index = nh.index
    out[f"Londra {hh}:00"] = round(dn.corr(np.log(s).diff()), 4)
print("ΔlnNAV ~ Δln spot (Londra saati):", out)
days = nyse_days("2010-01-01")[:-5]
rg = np.log(yh("GLD", "close").reindex(days)).diff()
o2 = {}
for hh in (14, 15, 16, 17):
    s, _ = snap(xs, et_times(days, hh), 0); s.index = days
    o2[f"ET {hh}:00"] = round(rg.corr(np.log(s).diff()), 4)
print("GLD kapanış getirisi ~ Δln spot (ET saati):", o2)
