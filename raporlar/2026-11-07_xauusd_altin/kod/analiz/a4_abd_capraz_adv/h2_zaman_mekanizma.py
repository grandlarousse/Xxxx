"""h2: (1) Yahoo GLD / GDXJ / DXY kapanış saatinin Dukascopy ile doğrulanması (tarih kayması = ileriye bakma riski),
(2) C1 sinyalinin hedef penceresini saat dilimlerine ayırma (mekanizma), (3) D1 emilim tanısının pencere başlangıç saatine duyarlılığı,
(4) DST ayrımı."""
import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
pd.set_option("display.width", 250)
d = load_viop(); idx = d.index

def hourly_px(sym):
    h = hourly(sym).copy(); i = pd.to_datetime(h.index)
    if i.tz is not None: i = i.tz_convert("UTC").tz_localize(None)
    return pd.Series(h["c"].values, index=i + pd.Timedelta(hours=1))  # fiyat anı
XAU = hourly_px("XAUUSD"); DXY = hourly_px("DOLLARIDXUSD")

def raw(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); y.index = pd.to_datetime(y.index); return y

# ---------- (1) Yahoo günlük getiri ile Dukascopy [D-1 H → D H] getirisi korelasyonu, H taraması; kayma k=-1,0,+1 gün
def scan(ytk, hsym, col="adjclose", years=("2018-01-01", "2026-10-29")):
    y = raw(ytk)[col]; y = y[(y.index >= years[0]) & (y.index <= years[1])]
    ry = np.log(y).diff().dropna()
    out = {}
    for k in (-1, 0, 1):
        for H in range(12, 24):
            dates = ry.index + pd.Timedelta(days=k)
            p1 = hsym.reindex(dates + pd.Timedelta(hours=H))
            # önceki işlem günü
            prevd = pd.Series(ry.index).shift(1).values + pd.Timedelta(days=k)
            p0 = hsym.reindex(pd.DatetimeIndex(prevd) + pd.Timedelta(hours=H))
            rr = pd.Series(np.log(p1.values / p0.values), index=ry.index)
            c = pd.concat([ry, rr], axis=1).dropna().corr().iloc[0, 1]
            out[(k, H)] = round(c, 3)
    s = pd.Series(out); s.index = pd.MultiIndex.from_tuples(s.index, names=["kayma_gun", "saat_UTC"])
    return s.unstack(1)
for tk, hs in (("GLD", XAU), ("GDXJ", XAU), ("DX-Y.NYB", DXY)):
    print(f"(1) {tk}: corr(Yahoo günlük, Duka [D-1 H, D H])\n", scan(tk, hs, "close" if tk == "DX-Y.NYB" else "adjclose").to_string())

# ---------- (2) C1 mekanizma: sinyal → altın getirisi saat dilimleri (gün t+k, k=0..3)
x = miner_resid(d, "y_GDXJ")
segs = {}
def seg_ret(day_off, h0, h1, day_off1=None):
    day_off1 = day_off if day_off1 is None else day_off1
    days = pd.Series(idx, index=idx)
    d0 = days.shift(-day_off) if day_off else days
    d1 = days.shift(-day_off1) if day_off1 else days
    p0 = XAU.reindex(pd.DatetimeIndex(d0.values) + pd.Timedelta(hours=h0)).values
    p1 = XAU.reindex(pd.DatetimeIndex(d1.values) + pd.Timedelta(hours=h1)).values
    return pd.Series(np.log(p1 / p0), index=idx)
rows = []
spec = [("t-1 20:00→t 07:00 (Asya)", -1, 20, 0, 7), ("t 07:00→t 13:00 (Avrupa)", 0, 7, 0, 13), ("t 13:00→t 15:00 (ABD açılış)", 0, 13, 0, 15)]
for k in (0, 1, 2):
    spec += [(f"t+{k} 15:00→t+{k} 20:00 (ABD öğleden sonra)", k, 15, k, 20), (f"t+{k} 20:00→t+{k+1} 07:00 (Asya)", k, 20, k + 1, 7),
             (f"t+{k+1} 07:00→t+{k+1} 13:00 (Avrupa)", k + 1, 7, k + 1, 13), (f"t+{k+1} 13:00→t+{k+1} 15:00 (ABD sabah)", k + 1, 13, k + 1, 15)]
for nm, a, h0, b, h1 in spec:
    if a < 0:
        days = pd.Series(idx, index=idx); d0 = days.shift(1)
        p0 = XAU.reindex(pd.DatetimeIndex(d0.values) + pd.Timedelta(hours=h0)).values
        p1 = XAU.reindex(pd.DatetimeIndex(idx) + pd.Timedelta(hours=h1)).values
        r = pd.Series(np.log(p1 / p0), index=idx)
    else:
        r = seg_ret(a, h0, h1, b)
    s = split_stats(x, r, 1)
    rows.append(dict(pencere=nm, ic=round(s["ic"], 3), t=round(s["t"], 2), t_is=round(s["t_is"], 2), t_oos=round(s["t_oos"], 2), n=s["n"]))
M = pd.DataFrame(rows); print("(2) C1 sinyal → altın saat dilimleri\n", M.to_string(index=False))
# ABD saatleri (15→20 t..t+2 ve 13→15 t+1..t+3) toplamı vs ABD dışı
us = seg_ret(0, 15, 20) + seg_ret(1, 13, 20) + seg_ret(2, 13, 20) + seg_ret(3, 13, 15)
non = sum(seg_ret(k, 20, 13, k + 1) for k in (0, 1, 2))
for nm, r in (("ABD saatleri toplam (t 15→t+3 15 içinde)", us), ("ABD dışı (20→13)", non)):
    s = split_stats(x, r, 3); print("(2)", nm, {k: round(v, 3) if isinstance(v, float) else v for k, v in s.items() if k != "by_year"})

# ---------- (3) D1: z(Δ1 log DXY) → altın [t-1 H0 → t 15:00], H0 tarama; ayrıca tek saatlik dilimler; DST ayrımı
dx = zscale(np.log(d["y_DX_Y_NYB"]).diff())
avail = pd.to_datetime(d["y_DX_Y_NYB_avail"])
print("(3) DXY avail saat dağılımı:", avail.dt.hour.value_counts().to_dict())
prev = pd.Series(idx, index=idx).shift(1)
res = []
for H0 in (14, 16, 18, 19, 20, 21, 22, 23, 24, 26, 28, 31):
    p0 = XAU.reindex(pd.DatetimeIndex(prev.values) + pd.Timedelta(hours=H0)).values
    p1 = XAU.reindex(pd.DatetimeIndex(idx) + pd.Timedelta(hours=15)).values
    r = pd.Series(np.log(p1 / p0), index=idx)
    s = split_stats(dx, r, 1)
    res.append(dict(baslangic=f"t-1 {H0}:00" if H0 < 24 else f"t {H0-24:02d}:00", ic=round(s["ic"], 3), t=round(s["t"], 2), t_is=round(s["t_is"], 2), t_oos=round(s["t_oos"], 2)))
print("(3) D1 pencere başlangıcı taraması\n", pd.DataFrame(res).to_string(index=False))
hr = []
for H in range(14, 39):
    p0 = XAU.reindex(pd.DatetimeIndex(prev.values) + pd.Timedelta(hours=H)).values
    p1 = XAU.reindex(pd.DatetimeIndex(prev.values) + pd.Timedelta(hours=H + 1)).values
    r = pd.Series(np.log(p1 / p0), index=idx)
    s = ic(dx, r, 5)
    summer = avail.dt.hour == 21  # yaz saati: 17:00 ET = 21:00 UTC
    s1 = ic(dx[summer], r[summer], 5); s2 = ic(dx[~summer], r[~summer], 5)
    hr.append(dict(saat=f"t-1 {H}:00→{H+1}:00" if H < 24 else f"t {H-24:02d}:00→{H-23:02d}:00", ic=round(s["ic"], 3), t=round(s["t"], 2), t_yaz=round(s1["t"], 2), t_kis=round(s2["t"], 2)))
print("(3) D1 tek saatlik dilimler (Δ1 DXY t-1 kapanışı → altın)\n", pd.DataFrame(hr).to_string(index=False))
# D1 asıl pencere, DST ayrı
p0 = XAU.reindex(pd.DatetimeIndex(prev.values) + pd.Timedelta(hours=20)).values; p1 = XAU.reindex(pd.DatetimeIndex(idx) + pd.Timedelta(hours=15)).values
rC = pd.Series(np.log(p1 / p0), index=idx)
summer = avail.dt.hour == 21
print("(3) D1 asıl pencere yaz:", ic(dx[summer], rC[summer], 5), " kış:", ic(dx[~summer], rC[~summer], 5))
# DXY kapanışından SONRA başlayan pencere: yazın 21:00, kışın 22:00
H0 = np.where(summer, 21, 22)
p0b = np.array([XAU.get(pd.Timestamp(pv) + pd.Timedelta(hours=int(h)), np.nan) if pd.notna(pv) else np.nan for pv, h in zip(prev.values, H0)])
rC2 = pd.Series(np.log(p1 / p0b), index=idx)
print("(3) D1 DXY kapanışından sonra başlayan pencere (yaz 21, kış 22 → t 15):", split_stats(dx, rC2, 1))
