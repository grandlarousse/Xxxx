"""ETF (Midas cephesi) paneli. Gün endeksi = NYSE işlem günleri (GLD'nin işlem gördüğü günler) 2008+.
KARAR ANI (cutoff) = gün t 15:00 America/New_York (ABD kapanışından 1 saat önce; saatlik veri nedeniyle muhafazakâr). UTC karşılığı yazın 19:00, kışın 20:00.
Giriş = gün t ABD kapanışı (16:00 ET), çıkış = t+h ABD kapanışı. Hedef: ETF adjclose log getirileri.
Bir öngörücü yalnızca yayın/kapanış zamanı cutoff'tan ÖNCE ise gün t'de kullanılabilir.
"""
import os, sys, glob, json, zipfile, lzma
import numpy as np, pandas as pd
S = sys.argv[1]; P = f"{S}/panel"; UTC = "UTC"
sys.path.insert(0, f"{S}/code")

gld = pd.read_parquet(f"{P}/yahoo/GLD.parquet")
days = pd.DatetimeIndex(gld.index[gld.index >= "2008-01-01"])
cut = pd.DatetimeIndex([pd.Timestamp(d) + pd.Timedelta(hours=15) for d in days]).tz_localize("America/New_York").tz_convert(UTC)
close_utc = cut + pd.Timedelta(hours=1)

def asof(vals, avail_utc, cutoffs):
    o = np.argsort(avail_utc.values); av = avail_utc.values[o]; vv = np.asarray(vals)[o]
    idx = np.searchsorted(av, cutoffs.values, side="left") - 1
    x = np.where(idx >= 0, vv[np.clip(idx, 0, None)], np.nan)
    a = np.where(idx >= 0, av[np.clip(idx, 0, None)], np.datetime64("NaT", "ns"))
    return pd.Series(x, index=days), pd.Series(pd.to_datetime(a), index=days)

def hourly_series(sym):
    fn = f"{P}/duka/{sym}.parquet"
    if not os.path.exists(fn): return None
    d = pd.read_parquet(fn)
    if sym in ("XAUUSD", "USDJPY"):
        out = []
        for f in sorted(glob.glob(f"{S}/data/duka_m/{sym}/2026*.bi5")):
            b = open(f, "rb").read()
            if not b: continue
            day = pd.Timestamp(os.path.basename(f)[:8], tz=UTC); raw = lzma.decompress(b)
            a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6); vol = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5]
            out.append(pd.DataFrame({"t": day + pd.to_timedelta(a[:, 0], unit="s"), "c": a[:, 2] / 1e3, "v": vol}))
        if out:
            m = pd.concat(out); m = m[m.v > 0].set_index("t").sort_index()
            hr = m.resample("1h").agg({"c": "last", "v": "sum"}).dropna(); hr.index.name = "bar_start_utc"
            d = pd.concat([d, hr[~hr.index.isin(d.index)]]).sort_index()
    s = d["c"].copy(); s.index = d.index + pd.Timedelta(hours=1)
    return s.sort_index()

def snap_at(series, targ, max_stale_h=1.0):
    if series is None: return pd.Series(np.nan, index=days)
    idx = series.index.searchsorted(targ, side="right") - 1
    vals = np.where(idx >= 0, series.values[np.clip(idx, 0, None)], np.nan)
    ts = series.index.values[np.clip(idx, 0, None)]
    stale = (targ.values - ts) / np.timedelta64(1, "h")
    return pd.Series(np.where((idx >= 0) & (stale <= max_stale_h), vals, np.nan), index=days)

out = {}
# --- hedef ETF'ler ve diğer ABD kapanışları (gün t kapanışı = giriş fiyatı; sinyalde kullanmak YASAK, yalnız t-1)
meta = json.load(open(f"{P}/yahoo/_meta.json"))
for k in sorted(os.listdir(f"{P}/yahoo")):
    if not k.endswith(".parquet"): continue
    key = k[:-8]; m = meta.get(key, {})
    d = pd.read_parquet(f"{P}/yahoo/{k}")
    col = "adjclose" if "adjclose" in d else "close"
    out[f"c_{key.replace('-', '_').replace('.', '_')}"] = d[col].reindex(days)  # gün t kapanışı (o borsanın yerel takvim günü)
# --- spot altın ve çapraz varlıklar: cutoff (15:00 ET) ve kapanış (16:00 ET) anında; ayrıca VİOP uzlaşma anı 15:10 UTC
XS = hourly_series("XAUUSD")
out["xau_cut"] = snap_at(XS, cut); out["xau_close"] = snap_at(XS, close_utc)
v15 = pd.DatetimeIndex([pd.Timestamp(d).tz_localize(UTC) + pd.Timedelta(hours=15) for d in days])
out["xau_1500utc"] = snap_at(XS, v15)
for H in (0, 7, 12):
    out[f"xau_{H:02d}utc"] = snap_at(XS, pd.DatetimeIndex([pd.Timestamp(d).tz_localize(UTC) + pd.Timedelta(hours=H) for d in days]))
for sym in ["XAGUSD", "XPTUSD", "DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "USDJPY", "EURUSD", "USDCNH", "USDTRY", "BRENTCMDUSD", "COPPERCMDUSD", "VOLIDXUSD", "BTCUSD"]:
    hs = hourly_series(sym)
    out[f"dk_{sym}_cut"] = snap_at(hs, cut)
# --- VİOP (gün t uzlaşması 15:10 UTC < cutoff): bilinen
pv = pd.read_parquet(f"{P}/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
for c in ["v_settle", "v_ret", "v_volume", "v_oi", "v_code", "vo_xautry_settle", "vo_usdtry_settle", "tr_prem_matched", "shfe_AU0_c", "shfe_AU0_date", "dk_USDCNH_p07", "xau_p07"]:
    if c in pv: out["viop_" + c if not c.startswith(("shfe", "dk_", "xau")) else c] = pv[c].reindex(days)
# --- Yahoo as-of (cutoff'tan önce kapanmış son değer): diğer piyasaların kapanışları
CLOSE = {"NYQ": ("16:00", "America/New_York"), "NMS": ("16:00", "America/New_York"), "NGM": ("16:00", "America/New_York"), "PCX": ("16:00", "America/New_York"),
         "ASE": ("16:00", "America/New_York"), "BTS": ("16:00", "America/New_York"), "SNP": ("16:00", "America/New_York"), "NIM": ("16:00", "America/New_York"), "CXI": ("16:15", "America/New_York"),
         "WCB": ("16:15", "America/New_York"), "NYS": ("17:00", "America/New_York"), "CGI": ("16:00", "America/New_York"), "NYB": ("17:00", "America/New_York"),
         "CMX": ("17:00", "America/New_York"), "NYM": ("17:00", "America/New_York"), "CME": ("17:00", "America/New_York"), "CBT": ("17:00", "America/New_York"),
         "CCY": ("23:59", "UTC"), "CCC": ("23:59", "UTC"), "IST": ("18:10", "Europe/Istanbul"), "OSA": ("15:30", "Asia/Tokyo"), "JPX": ("15:30", "Asia/Tokyo"), "HKG": ("16:10", "Asia/Hong_Kong"),
         "SHH": ("15:00", "Asia/Shanghai"), "KSC": ("15:30", "Asia/Seoul"), "ASX": ("16:10", "Australia/Sydney"), "NSI": ("15:30", "Asia/Kolkata"),
         "GER": ("17:30", "Europe/Berlin"), "ZRH": ("17:30", "Europe/Berlin"), "FGI": ("16:30", "Europe/London"), "LSE": ("16:30", "Europe/London"),
         "MIL": ("17:30", "Europe/Rome"), "TOR": ("16:00", "America/Toronto")}
for k, m in meta.items():
    fn = f"{P}/yahoo/{k}.parquet"
    if not os.path.exists(fn): continue
    d = pd.read_parquet(fn)
    if d.empty: continue
    hhmm, tz = CLOSE.get(m.get("exchangeName"), ("23:59", "UTC")); hh, mm = map(int, hhmm.split(":"))
    loc = pd.DatetimeIndex(d.index) + pd.Timedelta(hours=hh, minutes=mm)
    avail = loc.tz_localize(tz, nonexistent="shift_forward", ambiguous="NaT").tz_convert(UTC)
    if m.get("exchangeName") in ("CCY", "CCC"): avail = avail + pd.Timedelta(hours=1)
    col = "adjclose" if ("adjclose" in d and m.get("instrumentType") in ("EQUITY", "ETF")) else "close"
    ok = ~pd.isna(avail)
    x, a = asof(d[col].values[ok], pd.Series(avail[ok]), cut)
    key = "y_" + k.replace("-", "_").replace(".", "_")
    out[key] = x; out[key + "_avail"] = a
    if "volume" in d:
        xv, _ = asof(d["volume"].values[ok], pd.Series(avail[ok]), cut); out[key + "_vol"] = xv
# --- Hazine (D 22:00 UTC), COT (Salı + 3 gün 21:00 UTC), GPR (D+1 23:00 UTC)
def treas(typ, cols):
    t = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(f"{S}/data/treasury/{typ}_*.csv"))]); t["Date"] = pd.to_datetime(t["Date"], format="%m/%d/%Y")
    return t.drop_duplicates("Date").set_index("Date").sort_index()[cols]
tt = treas("daily_treasury_real_yield_curve", ["5 YR", "10 YR"]).rename(columns={"5 YR": "real5", "10 YR": "real10"}).join(
     treas("daily_treasury_yield_curve", ["3 Mo", "2 Yr", "10 Yr"]).rename(columns={"3 Mo": "nom3m", "2 Yr": "nom2", "10 Yr": "nom10"}), how="outer")
tt["be10"] = tt.nom10 - tt.real10
av = pd.Series(pd.DatetimeIndex(tt.index).tz_localize(UTC) + pd.Timedelta(hours=22))
for c in tt.columns: out[f"ust_{c}"] = asof(tt[c].values, av, cut)[0]
cot = []
for f in sorted(glob.glob(f"{S}/data/cftc/*.zip")):
    z = zipfile.ZipFile(f)
    for nm in z.namelist(): cot.append(pd.read_csv(z.open(nm), low_memory=False))
cot = pd.concat(cot); cot["code"] = cot["CFTC_Contract_Market_Code"].astype(str).str.strip().str.zfill(6)
dcol = [c for c in cot.columns if c.startswith("Report_Date_as_YYYY")][0]; cot["rd"] = pd.to_datetime(cot[dcol])
g = cot[cot.code == "088691"].drop_duplicates("rd").set_index("rd").sort_index()
cg = pd.DataFrame({"mm_net": g["M_Money_Positions_Long_All"] - g["M_Money_Positions_Short_All"], "oi": g["Open_Interest_All"]}); cg["mm_net_oi"] = cg.mm_net / cg.oi
av = pd.Series(pd.DatetimeIndex(cg.index).tz_localize(UTC) + pd.Timedelta(days=3, hours=21))
for c in cg.columns: out[f"cot_gold_{c}"] = asof(cg[c].values, av, cut)[0]
# --- GLD/GLDM NAV ve dolaşımdaki pay (akış). D değeri D 23:00 UTC'de (kapanıştan sonra) yayınlanmış varsayıldı -> gün t'de en son D = t-1.
for t in ["gld", "gldm"]:
    fn = f"{S}/data/etf_flows/navhist-{t}.xlsx"
    if not os.path.exists(fn): continue
    x = pd.read_excel(fn, header=3).iloc[:, :4]; x.columns = ["date", "nav", "shares", "tna"]
    x["date"] = pd.to_datetime(x["date"], format="%d-%b-%Y", errors="coerce"); x = x.dropna(subset=["date"]).set_index("date").sort_index()
    for c in ["nav", "shares", "tna"]: x[c] = pd.to_numeric(x[c], errors="coerce")
    x.to_parquet(f"{P}/etf_{t}_navhist.parquet")
    av = pd.Series(pd.DatetimeIndex(x.index).tz_localize(UTC) + pd.Timedelta(hours=23))
    for c in ["nav", "shares"]: out[f"flow_{t}_{c}"] = asof(x[c].values, av, cut)[0]
    out[f"flow_{t}_nav_t"] = x["nav"].reindex(days)   # gün t NAV (LBMA PM'den) — gün t kapanışından sonra yayınlanır; sinyalde t-1 kullan
df = pd.DataFrame(out, index=days); df.index.name = "date"
df["cut_utc"] = cut; df["close_utc"] = close_utc
df.to_parquet(f"{P}/panel_etf.parquet")
print("panel_etf", df.shape, df.index.min().date(), df.index.max().date())
print([c for c in df.columns if c.startswith("c_")][:200])
