"""Ortak panel kurucu. İki gün endeksi:
  panel_viop.parquet : VİOP işlem günleri (2017-03-06 ..), hedef = VİOP XAUUSD aktif kontrat uzlaşma getirisi
  panel_spot.parquet : Dukascopy XAUUSD'nin 15:00 UTC fiyatı olan iş günleri (2010 ..), hedef = spot 15:00 UTC getirisi
KARAR ANI (cutoff): gün t'nin 15:00 UTC'si. Bir öngörücü yalnızca yayın/kapanış zamanı cutoff'tan ÖNCE ise gün t'de kullanılabilir.
Her öngörücü sütunu için 'x_t' = karar anı t'de bilinen son değer; '_d1' = karar anı t-1'den t'ye bilinen son değerdeki değişim.
"""
import os, sys, glob, json, zipfile, io, re
import numpy as np, pandas as pd
S = sys.argv[1]
P = f"{S}/panel"
UTC = "UTC"

# ------------------------------------------------------------------ hedefler
v = pd.read_parquet(f"{P}/viop_XAUUSD.parquet")
v.index = pd.to_datetime(v.index)
viop_days = v.index

xh = pd.read_parquet(f"{P}/duka/XAUUSD.parquet")
# dakika yaması (Ekim-Kasım 2026) varsa saatliğe çevirip ekle
def minute_patch(sym):
    import lzma, datetime as dt
    out = []
    for f in sorted(glob.glob(f"{S}/data/duka_m/{sym}/2026*.bi5")):
        b = open(f, "rb").read()
        if not b: continue
        day = pd.Timestamp(os.path.basename(f)[:8], tz=UTC)
        raw = lzma.decompress(b)
        a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6)
        vol = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5]
        t = day + pd.to_timedelta(a[:, 0], unit="s")
        out.append(pd.DataFrame({"t": t, "o": a[:, 1], "c": a[:, 2], "l": a[:, 3], "h": a[:, 4], "v": vol}))
    if not out: return None
    m = pd.concat(out); m = m[m.v > 0].set_index("t").sort_index()
    pt = 1e3
    for k in "oclh": m[k] = m[k] / pt
    hr = m.resample("1h").agg({"o": "first", "c": "last", "l": "min", "h": "max", "v": "sum"}).dropna()
    hr.index.name = "bar_start_utc"
    return hr

def hourly(sym):
    fn = f"{P}/duka/{sym}.parquet"
    if not os.path.exists(fn): return None
    d = pd.read_parquet(fn)
    if sym in ("XAUUSD", "USDJPY"):
        pm = minute_patch(sym)
        if pm is not None:
            if sym == "USDJPY": pm[["o", "c", "l", "h"]] = pm[["o", "c", "l", "h"]]  # nokta 1e3 aynı
            d = pd.concat([d, pm[~pm.index.isin(d.index)]]).sort_index()
    # fiyat anı = bar kapanışı = bar_start + 1 saat
    s = d["c"].copy(); s.index = d.index + pd.Timedelta(hours=1)
    return s

def snap(series, days, hour_utc, max_stale_h=2):
    """Her gün için hour_utc:00'daki (veya en fazla max_stale_h saat önceki) son fiyat."""
    if series is None: return pd.Series(np.nan, index=days)
    targ = pd.DatetimeIndex([pd.Timestamp(d).tz_localize(UTC) + pd.Timedelta(hours=hour_utc) for d in days])
    s = series.sort_index()
    idx = s.index.searchsorted(targ, side="right") - 1
    vals = np.where(idx >= 0, s.values[np.clip(idx, 0, None)], np.nan)
    ts = np.where(idx >= 0, s.index.values[np.clip(idx, 0, None)], np.datetime64("NaT"))
    stale = (targ.values - ts) / np.timedelta64(1, "h")
    vals = np.where(stale <= max_stale_h, vals, np.nan)
    return pd.Series(vals, index=days)

xs = hourly("XAUUSD")
# spot gün endeksi: 15:00 UTC'de taze (<=1 saat) fiyatı olan hafta içi günler, 2010+
cand = pd.bdate_range("2010-01-04", "2026-11-06")
p15 = snap(xs, cand, 15, 1)
spot_days = p15.dropna().index

DUKA = ["XAGUSD", "XPTUSD", "DOLLARIDXUSD", "USTBONDTRUSD", "USA500IDXUSD", "USDJPY", "EURUSD", "USDCNH", "USDTRY", "BRENTCMDUSD", "COPPERCMDUSD", "VOLIDXUSD", "BTCUSD"]
HSER = {s: hourly(s) for s in ["XAUUSD"] + DUKA}

# ------------------------------------------------------------------ Yahoo: kapanış saatleri
CLOSE = {  # exchangeName -> (yerel saat, tz)
    "NYQ": ("16:00", "America/New_York"), "NMS": ("16:00", "America/New_York"), "NGM": ("16:00", "America/New_York"),
    "PCX": ("16:00", "America/New_York"), "ASE": ("16:00", "America/New_York"), "SNP": ("16:00", "America/New_York"),
    "NIM": ("16:00", "America/New_York"), "CXI": ("16:15", "America/New_York"), "WCB": ("16:15", "America/New_York"),
    "NYS": ("17:00", "America/New_York"), "CGI": ("16:00", "America/New_York"), "NYB": ("17:00", "America/New_York"),
    "CMX": ("17:00", "America/New_York"), "NYM": ("17:00", "America/New_York"), "CME": ("17:00", "America/New_York"), "CBT": ("17:00", "America/New_York"),
    "CCY": ("23:59", "UTC"), "CCC": ("23:59", "UTC"),
    "IST": ("18:10", "Europe/Istanbul"), "OSA": ("15:30", "Asia/Tokyo"), "HKG": ("16:10", "Asia/Hong_Kong"), "SHH": ("15:00", "Asia/Shanghai"),
    "KSC": ("15:30", "Asia/Seoul"), "ASX": ("16:10", "Australia/Sydney"), "NSI": ("15:30", "Asia/Kolkata"),
    "GER": ("17:30", "Europe/Berlin"), "ZRH": ("17:30", "Europe/Berlin"), "FGI": ("16:30", "Europe/London"),
}
LEVEL_DIFF = {"_TNX", "_FVX", "_IRX", "_TYX"}  # faiz: fark (yüzde puan)
meta = json.load(open(f"{P}/yahoo/_meta.json"))

def asof_series(vals, avail_utc, days, cutoff_hour=15):
    """vals, avail_utc aynı sıralı; her gün t için avail < t 15:00 UTC olan son değer ve onun avail zamanı."""
    o = np.argsort(avail_utc.values)
    av = avail_utc.values[o]; vv = np.asarray(vals)[o]
    cut = pd.DatetimeIndex([pd.Timestamp(d).tz_localize(UTC) + pd.Timedelta(hours=cutoff_hour) for d in days]).values
    idx = np.searchsorted(av, cut, side="left") - 1  # strictly before cutoff
    x = np.where(idx >= 0, vv[np.clip(idx, 0, None)], np.nan)
    a = np.where(idx >= 0, av[np.clip(idx, 0, None)], np.datetime64("NaT"))
    return pd.Series(x, index=days), pd.Series(a, index=days)

def build(days, name):
    days = pd.DatetimeIndex(days)
    out = {}
    # --- spot XAU anlık görüntüleri (UTC saat) — gün t için
    for H in [0, 7, 12, 13, 14, 15, 16, 20]:
        out[f"xau_p{H:02d}"] = snap(HSER["XAUUSD"], days, H, 1)
    # bir önceki gün (t-1 bu endeksteki önceki gün) 20:00 UTC: akşam seansı sonu yaklaşık
    prev = pd.Series(days, index=days).shift(1)
    p20prev = snap(HSER["XAUUSD"], pd.DatetimeIndex(prev.fillna(days[0])), 20, 1); p20prev.index = days
    p15prev = snap(HSER["XAUUSD"], pd.DatetimeIndex(prev.fillna(days[0])), 15, 1); p15prev.index = days
    out["xau_p20_prev"] = p20prev; out["xau_p15_prev"] = p15prev
    # --- Dukascopy çapraz varlıklar: 15:00 UTC (t) ve 07:00 UTC (t)
    for sym in DUKA:
        out[f"dk_{sym}_p15"] = snap(HSER[sym], days, 15, 1)
        out[f"dk_{sym}_p07"] = snap(HSER[sym], days, 7, 1)
    # --- Yahoo
    for k, m in meta.items():
        fn = f"{P}/yahoo/{k}.parquet"
        if not os.path.exists(fn): continue
        d = pd.read_parquet(fn)
        if d.empty: continue
        hhmm, tz = CLOSE.get(m["exchangeName"], ("23:59", "UTC"))
        hh, mm = map(int, hhmm.split(":"))
        loc = pd.DatetimeIndex(d.index) + pd.Timedelta(hours=hh, minutes=mm)
        avail = loc.tz_localize(tz, nonexistent="shift_forward", ambiguous="NaT").tz_convert(UTC)
        if m["exchangeName"] in ("CCY", "CCC"): avail = avail + pd.Timedelta(hours=1)  # bar sonu + pay
        col = "adjclose" if ("adjclose" in d and m.get("instrumentType") in ("EQUITY", "ETF")) else "close"
        ok = ~pd.isna(avail)
        x, a = asof_series(d[col].values[ok], pd.Series(avail[ok]), days)
        key = "y_" + k.replace("-", "_").replace(".", "_")
        out[key] = x
        out[key + "_avail"] = pd.to_datetime(a)
    # --- ABD Hazinesi (gün sonu; ~15:30 ET kotasyonları; yayın akşam) -> D 22:00 UTC'de mevcut say
    def treas(typ, cols):
        fs = sorted(glob.glob(f"{S}/data/treasury/{typ}_*.csv"))
        t = pd.concat([pd.read_csv(f) for f in fs]); t["Date"] = pd.to_datetime(t["Date"], format="%m/%d/%Y")
        t = t.drop_duplicates("Date").set_index("Date").sort_index()
        return t[cols]
    tr = treas("daily_treasury_real_yield_curve", ["5 YR", "10 YR"]).rename(columns={"5 YR": "real5", "10 YR": "real10"})
    tn = treas("daily_treasury_yield_curve", ["3 Mo", "2 Yr", "5 Yr", "10 Yr", "30 Yr"]).rename(columns={"3 Mo": "nom3m", "2 Yr": "nom2", "5 Yr": "nom5", "10 Yr": "nom10", "30 Yr": "nom30"})
    tt = tr.join(tn, how="outer")
    tt["be10"] = tt.nom10 - tt.real10; tt["be5"] = tt.nom5 - tt.real5
    av = pd.Series(pd.DatetimeIndex(tt.index).tz_localize(UTC) + pd.Timedelta(hours=22))
    for c in tt.columns:
        x, a = asof_series(tt[c].values, av, days); out[f"ust_{c}"] = x
    # --- CFTC COT (COMEX altın 088691, gümüş 084691): Salı pozisyonu, Cuma 15:30 ET yayın -> Cuma 21:00 UTC mevcut
    cot = []
    for f in sorted(glob.glob(f"{S}/data/cftc/*.zip")):
        z = zipfile.ZipFile(f)
        for nm in z.namelist():
            t = pd.read_csv(z.open(nm), low_memory=False)
            cot.append(t)
    cot = pd.concat(cot)
    cot["code"] = cot["CFTC_Contract_Market_Code"].astype(str).str.strip().str.zfill(6)
    dcol = [c for c in cot.columns if c.startswith("Report_Date_as_YYYY")][0]
    cot["rd"] = pd.to_datetime(cot[dcol])
    for code, nm in [("088691", "gold"), ("084691", "silver")]:
        g = cot[cot.code == code].drop_duplicates("rd").set_index("rd").sort_index()
        mm = (g["M_Money_Positions_Long_All"] - g["M_Money_Positions_Short_All"])
        oi = g["Open_Interest_All"]
        sw = (g["Swap_Positions_Long_All"] - g["Swap__Positions_Short_All"]) if "Swap__Positions_Short_All" in g else (g["Swap_Positions_Long_All"] - g["Swap_Positions_Short_All"])
        pm = (g["Prod_Merc_Positions_Long_All"] - g["Prod_Merc_Positions_Short_All"])
        df = pd.DataFrame({"mm_net": mm, "mm_net_oi": mm / oi, "oi": oi, "swap_net": sw, "pm_net": pm, "mm_long": g["M_Money_Positions_Long_All"], "mm_short": g["M_Money_Positions_Short_All"]})
        av = pd.Series(pd.DatetimeIndex(df.index).tz_localize(UTC) + pd.Timedelta(days=3, hours=21))
        for c in df.columns:
            x, a = asof_series(df[c].values, av, days); out[f"cot_{nm}_{c}"] = x
        x, a = asof_series(np.array(df.index.values, dtype="datetime64[ns]").astype("int64"), av, days)
        out[f"cot_{nm}_reportdate"] = pd.to_datetime(x)
    # --- SHFE (Sina AU0/AG0): Çin işlem günü D, gündüz kapanışı 15:00 CST = 07:00 UTC
    for nm in ["AU0", "AG0"]:
        txt = open(f"{S}/data/misc/sina_{nm}.txt").read()
        js = json.loads(txt[txt.index("(") + 1: txt.rindex(")")])
        d = pd.DataFrame(js); d["d"] = pd.to_datetime(d["d"]); d = d.set_index("d").sort_index()
        for c in "ohlcv": d[c] = pd.to_numeric(d[c])
        av = pd.Series(pd.DatetimeIndex(d.index).tz_localize(UTC) + pd.Timedelta(hours=7, minutes=5))
        x, a = asof_series(d["c"].values, av, days); out[f"shfe_{nm}_c"] = x
        x, a = asof_series(np.array(d.index.values, dtype="datetime64[ns]").astype("int64"), av, days); out[f"shfe_{nm}_date"] = pd.to_datetime(x)
    # --- GPR günlük (Caldara-Iacoviello): D değeri D+1 23:00 UTC'de mevcut varsay (gerçek zamanlı yayın haftalık; dikkat)
    try:
        g = pd.read_excel(f"{S}/data/misc/gpr_daily.xls")
        dc = [c for c in g.columns if str(c).lower() in ("date", "day")][0]
        g[dc] = pd.to_datetime(g[dc]); g = g.set_index(dc).sort_index()
        av = pd.Series(pd.DatetimeIndex(g.index).tz_localize(UTC) + pd.Timedelta(days=1, hours=23))
        for c in [c for c in g.columns if str(c).upper() in ("GPRD", "GPRD_ACT", "GPRD_THREAT", "GPRD_MA7", "GPRD_MA30")]:
            x, a = asof_series(pd.to_numeric(g[c], errors="coerce").values, av, days); out[f"gpr_{c}"] = x
    except Exception as e:
        print("GPR ERR", e)
    # --- FRED (indirildiyse): günlük seriler D 22:00 UTC + 1 gün mevcut (yayın gecikmesi)
    for f in sorted(glob.glob(f"{S}/data/fred/*.csv")):
        sid = os.path.basename(f)[:-4]
        try:
            t = pd.read_csv(f); t.columns = ["date", "val"]; t["date"] = pd.to_datetime(t["date"]); t["val"] = pd.to_numeric(t["val"], errors="coerce")
            t = t.dropna().set_index("date")
            av = pd.Series(pd.DatetimeIndex(t.index).tz_localize(UTC) + pd.Timedelta(days=1, hours=22))
            x, a = asof_series(t["val"].values, av, days); out[f"fred_{sid}"] = x
        except Exception as e:
            print("FRED ERR", sid, e)
    df = pd.DataFrame(out, index=days)
    return df

# ------------------------------------------------------------------ VİOP paneli
pv = build(viop_days, "viop")
for c in ["code", "expiry", "settle", "prev_settle", "ret", "close", "open", "high", "low", "vwap", "volume", "trades", "oi", "os_price", "tot_volume", "tot_oi", "next_code", "next_settle", "dte", "value"]:
    pv["v_" + c] = v[c]
# diğer VİOP kontratları (aynı 15:10 UTC damgası)
for root, nm in [("XAUTRYM", "xautry"), ("XAGUSD", "xag"), ("USDTRY", "usdtry"), ("XU030", "xu030"), ("EURUSD", "eurusd")]:
    fn = f"{P}/viop_{root}.parquet"
    if os.path.exists(fn):
        c = pd.read_parquet(fn); c.index = pd.to_datetime(c.index)
        for col in ["settle", "ret", "expiry", "code", "volume", "oi", "dte"]:
            pv[f"vo_{nm}_{col}"] = c[col].reindex(pv.index)
# gram altın sentetik prim: aynı vade ayında XAUTRYM / (XAUUSD × USDTRY / 31.1035)
L = pd.read_parquet(f"{P}/viop_long.parquet")
L["ym"] = L["expiry"].dt.to_period("M")
g1 = L[L.root == "XAUTRYM"][["date", "ym", "settle", "volume"]].rename(columns={"settle": "xt", "volume": "xt_vol"})
g2 = L[L.root == "XAUUSD"][["date", "ym", "settle", "volume"]].rename(columns={"settle": "xu", "volume": "xu_vol"})
g3 = L[L.root == "USDTRY"][["date", "ym", "settle"]].rename(columns={"settle": "fx"})
m = g1.merge(g2, on=["date", "ym"]).merge(g3, on=["date", "ym"])
m = m[(m.xt > 0) & (m.xu > 0) & (m.fx > 0)]
m["prem"] = np.log(m.xt) - np.log(m.xu * m.fx / 31.1035)
m = m.sort_values(["date", "xt_vol"], ascending=[True, False]).drop_duplicates("date").set_index("date")
pv["tr_prem_matched"] = m["prem"].reindex(pv.index)
pv["tr_prem_ym"] = m["ym"].astype(str).reindex(pv.index)
# ileri getiriler (aynı kontrat zincirinden günlük getiri toplamı)
for h in (1, 3, 5, 10):
    pv[f"fwd{h}"] = sum(pv["v_ret"].shift(-k) for k in range(1, h + 1))
pv.index.name = "date"
pv.to_parquet(f"{P}/panel_viop.parquet")
print("panel_viop", pv.shape, pv.index.min().date(), pv.index.max().date())

# ------------------------------------------------------------------ Spot paneli (2010+)
ps = build(spot_days, "spot")
ps["s_p15"] = p15.reindex(spot_days)
ps["s_ret"] = np.log(ps["s_p15"]).diff()
for h in (1, 3, 5, 10):
    ps[f"sfwd{h}"] = sum(ps["s_ret"].shift(-k) for k in range(1, h + 1))
# VİOP sütunlarını (varsa) aynı güne ekle
for c in ["v_ret", "v_settle", "v_code", "v_volume", "v_oi"]:
    ps[c] = pv[c].reindex(ps.index)
ps.index.name = "date"
ps.to_parquet(f"{P}/panel_spot.parquet")
print("panel_spot", ps.shape, ps.index.min().date(), ps.index.max().date())
