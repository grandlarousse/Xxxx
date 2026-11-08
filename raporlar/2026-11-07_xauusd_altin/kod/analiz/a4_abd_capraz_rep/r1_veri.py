"""r1_veri: Bağımsız yeniden üretim — ham tablolardan veri kurulumu (lib_altin / analist kodu KULLANILMAZ).
Çıktı: r1_viop.parquet (VİOP günleri), r1_spot.parquet (spot iş günleri), r1_kontrol.txt
Kurallar:
  - Hedef: viop_long XAUUSD; aktif kontrat = ÖNCEKİ gün açık pozisyonu en büyük kontrat; v_ret = log(settle/prev_settle) aynı kontrat içinde.
  - Yahoo: ham yahoo/<T>.parquet adjclose; kapanış anı = gün D 16:00 America/New_York (hisse/ETF), 17:00 ET (DXY, vadeli).
    Gün t için son kapanış = kapanış_anı < t 15:00 UTC olan son D (merge_asof, kesin küçük).
  - Hazine: data/treasury ham CSV; gün D değeri D 22:00 UTC'de mevcut → t 15:00'ten önce olan son D.
  - Dukascopy saatlik: index = bar başlangıcı; H:00 fiyatı = (H-1):00 başlayan barın kapanışı.
"""
import glob, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
P = f"{S}/panel"; OUT = f"{S}/out/a4_abd_capraz_rep"
log = open(f"{OUT}/r1_kontrol.txt", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n")

# ---------------- VİOP hedef ----------------
v = pd.read_parquet(f"{P}/viop_long.parquet")
x = v[v.root == "XAUUSD"].copy(); x["date"] = pd.to_datetime(x["date"])
x = x.sort_values(["date", "code"])
days = np.array(sorted(x.date.unique()))
# her gün en büyük OI kontratı
oi_max = x.loc[x.groupby("date")["oi"].idxmax(), ["date", "code"]].set_index("date")["code"]
active = oi_max.shift(1)                       # önceki günün en büyük OI kontratı
active.iloc[0] = oi_max.iloc[0]                # ilk gün: aynı gün (yalnız ilk satır)
xi = x.set_index(["date", "code"])
rows = []
for dt, c in active.items():
    r = xi.loc[(dt, c)]
    rows.append(dict(date=dt, code=c, settle=r.settle, prev_settle=r.prev_settle, volume=r.volume, oi=r.oi, expiry=r.expiry))
V = pd.DataFrame(rows).set_index("date")
V["v_ret"] = np.log(V.settle / V.prev_settle)
# prev_settle tutarlılığı: aynı kontratın önceki gün settle'ı ile karşılaştır
prev_same = []
for i, (dt, c) in enumerate(active.items()):
    if i == 0: prev_same.append(np.nan); continue
    pdt = days[i - 1]
    prev_same.append(xi.loc[(pdt, c)].settle if (pdt, c) in xi.index else np.nan)
V["settle_prevday_same"] = prev_same
dif = (V.prev_settle - V.settle_prevday_same).abs()
say("VIOP gün:", len(V), V.index[0].date(), V.index[-1].date())
say("prev_settle != önceki gün aynı kontrat settle (>0.001) sayısı:", int((dif > 1e-3).sum()), "/", int(dif.notna().sum()))
if (dif > 1e-3).any(): say(V[dif > 1e-3][["code", "prev_settle", "settle_prevday_same"]].head(10).to_string())
for h in (1, 3, 5):
    V[f"fwd{h}"] = sum(V.v_ret.shift(-k) for k in range(1, h + 1))
# panel ile karşılaştır
pv = pd.read_parquet(f"{P}/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
say("v_ret panel ile max fark:", float((V.v_ret - pv.v_ret).abs().max()), " kod farklı gün:", int((V.code != pv.v_code).sum()))
for h in (1, 3, 5):
    say(f"fwd{h} panel ile max fark:", float((V[f'fwd{h}'] - pv[f'fwd{h}']).abs().max()))
say("v_ret uç değerler (|r|>4%):", V.v_ret[V.v_ret.abs() > 0.04].round(4).to_dict())
roll = (V.code != V.code.shift(1)).sum(); say("roll sayısı:", int(roll))

# ---------------- Dukascopy saatlik ----------------
def duka_px(sym, hour):
    h = pd.read_parquet(f"{P}/duka/{sym}.parquet")
    idx = h.index.tz_convert("UTC").tz_localize(None) + pd.Timedelta(hours=1)
    c = pd.Series(h["c"].values, index=idx)
    c = c[(c.index.hour == hour) & (c.index.minute == 0)]
    c.index = c.index.normalize()
    return c[~c.index.duplicated(keep="last")]

# ---------------- Yahoo as-of ----------------
def yahoo_asof(tk, target_days, close_hour_et=16, close_min=0):
    y = pd.read_parquet(f"{P}/yahoo/{tk}.parquet"); y.index = pd.to_datetime(y.index)
    y = y[y.adjclose.notna() & (y.adjclose > 0)]
    # kapanış anı: D close_hour ET → UTC
    loc = (y.index + pd.Timedelta(hours=close_hour_et, minutes=close_min)).tz_localize("America/New_York", ambiguous="NaT", nonexistent="shift_forward")
    cl = loc.tz_convert("UTC").tz_localize(None)
    # ham ts_utc (bar açılışı) kapanıştan önce olmalı
    ts = pd.to_datetime(y.ts_utc).dt.tz_convert("UTC").dt.tz_localize(None)
    assert (ts.values < cl.values).all(), tk
    src = pd.DataFrame({"close_utc": cl, "px": y.adjclose.values, "D": y.index}).sort_values("close_utc")
    tgt = pd.DataFrame({"t": target_days, "cut": target_days + pd.Timedelta(hours=15)}).sort_values("cut")
    m = pd.merge_asof(tgt, src, left_on="cut", right_on="close_utc", allow_exact_matches=False, direction="backward")
    m = m.set_index("t")
    return m

TICK = {"GDXJ": 16, "GLD": 16, "GDX": 16, "RING": 16, "NEM": 16, "AEM": 16, "B": 16, "KGC": 16, "FNV": 16, "WPM": 16, "RGLD": 16,
        "DX-Y.NYB": 17}

def build(target_days, name):
    D = pd.DataFrame(index=target_days)
    for tk, hh in TICK.items():
        m = yahoo_asof(tk, target_days, hh)
        col = "y_" + tk.replace("-", "_").replace(".", "_")
        D[col] = m["px"]; D[col + "_D"] = m["D"]; D[col + "_cl"] = m["close_utc"]
        viol = int((m["close_utc"] >= m.index + pd.Timedelta(hours=15)).sum())
        lag = ((m.index + pd.Timedelta(hours=15) - m["close_utc"]).dt.total_seconds() / 3600)
        say(f"[{name}] {tk}: ihlal={viol}, medyan gecikme={lag.median():.1f} saat, min={lag.min():.1f}, D>=t gün sayısı={int((m['D'] >= m.index).sum())}")
    # Hazine
    def treas(typ, cols):
        fs = sorted(glob.glob(f"{S}/data/treasury/{typ}_*.csv")); L = []
        for f in fs:
            t = pd.read_csv(f); t["Date"] = pd.to_datetime(t["Date"], format="%m/%d/%Y"); L.append(t.set_index("Date")[cols])
        t = pd.concat(L).sort_index(); return t[~t.index.duplicated(keep="last")]
    tn = treas("daily_treasury_yield_curve", ["2 Yr", "10 Yr"]).rename(columns={"2 Yr": "nom2", "10 Yr": "nom10"})
    tr = treas("daily_treasury_real_yield_curve", ["10 YR"]).rename(columns={"10 YR": "real10"})
    for tt in (tn, tr):
        tt = tt.apply(pd.to_numeric, errors="coerce")
        src = tt.copy(); src["avail"] = src.index + pd.Timedelta(hours=22); src = src.reset_index().sort_values("avail")
        tgt = pd.DataFrame({"t": target_days, "cut": target_days + pd.Timedelta(hours=15)})
        m = pd.merge_asof(tgt, src, left_on="cut", right_on="avail", allow_exact_matches=False).set_index("t")
        for c in tt.columns:
            D["ust_" + c] = m[c]
        D["ust_D_" + "_".join(tt.columns)] = m["Date"]
    # Dukascopy 15:00 ve 20:00
    for s in ("XAUUSD", "DOLLARIDXUSD"):
        p15 = duka_px(s, 15); p20 = duka_px(s, 20); p00 = duka_px(s, 0)
        D[f"{s}_p15"] = p15.reindex(target_days).values
        D[f"{s}_p20"] = p20.reindex(target_days).values
        D[f"{s}_p00"] = p00.reindex(target_days).values
        for hh in (21, 22, 23):
            D[f"{s}_p{hh}"] = duka_px(s, hh).reindex(target_days).values
    return D

Vd = build(V.index, "viop")
Vd = V.join(Vd)
# panel ile Yahoo karşılaştırma
for c in ["y_GDXJ", "y_GLD", "y_DX_Y_NYB", "y_B"]:
    if c in pv:
        say(f"{c} panel ile max göreli fark: {float((Vd[c] / pv[c] - 1).abs().max()):.2e}")
say("ust_nom10 panel ile max fark:", float((Vd.ust_nom10 - pv.ust_nom10).abs().max()), " real10:", float((Vd.ust_real10 - pv.ust_real10).abs().max()))
say("xau_p15 panel ile max fark:", float((Vd.XAUUSD_p15 - pv.xau_p15).abs().max()), " NaN (ham saatlik eksik):", int(Vd.XAUUSD_p15.isna().sum()), " panelde NaN:", int(pv.xau_p15.isna().sum()))
say("DXY p15 panel ile max fark:", float((Vd.DOLLARIDXUSD_p15 - pv.dk_DOLLARIDXUSD_p15).abs().max()))
Vd.to_parquet(f"{OUT}/r1_viop.parquet")

# ---------------- spot paneli (2010+) ----------------
p15 = duka_px("XAUUSD", 15)
sdays = p15.index[(p15.index >= "2010-01-01") & (p15.index.dayofweek < 5)]
Sp = pd.DataFrame({"p15": p15.reindex(sdays)}, index=sdays)
Sp["s_ret"] = np.log(Sp.p15).diff()
for h in (1, 3, 5):
    Sp[f"sfwd{h}"] = sum(Sp.s_ret.shift(-k) for k in range(1, h + 1))
Sd = build(sdays, "spot")
Sp = Sp.join(Sd.drop(columns=[c for c in Sd.columns if c.startswith("XAUUSD_p15")]))
ps = pd.read_parquet(f"{P}/panel_spot.parquet"); ps.index = pd.to_datetime(ps.index)
cm = Sp.index.intersection(ps.index)
say("spot gün:", len(Sp), "panel_spot gün:", len(ps), "ortak:", len(cm))
say("s_ret panel_spot ile max fark (ortak gün):", float((Sp.s_ret.reindex(cm) - ps.s_ret.reindex(cm)).abs().max()))
say("sfwd3 panel_spot ile max fark:", float((Sp.sfwd3.reindex(cm) - ps.sfwd3.reindex(cm)).abs().max()))
Sp.to_parquet(f"{OUT}/r1_spot.parquet")
log.close()
