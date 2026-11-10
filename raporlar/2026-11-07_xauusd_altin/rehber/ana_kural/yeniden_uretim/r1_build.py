"""r1: sinyali ham Yahoo'dan, hedefi ham VIOP bulteninden kur; zamanlama denetimi."""
import json
from rep_lib import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 400)

# ---------- 1) ABD tarafi
R = us_returns("adjclose")
print("ABD getirileri:", R.index[0].date(), "->", R.index[-1].date(), len(R))
# takvim butunlugu
for k in ("GDX", "GLD", "SPY"):
    s = load_yahoo(k)
    miss = R.index.difference(s.index)
    print(f"  {k}: ilk {s.index[0].date()} son {s.index[-1].date()} n {len(s)}; ortak takvimde eksik {len(miss)}")
g = load_yahoo("GDX"); l = load_yahoo("GLD"); sp = load_yahoo("SPY")
print("  GDX takviminde olup GLD/SPY'de olmayan:", len(g.index.difference(l.index)), len(g.index.difference(sp.index)),
      "| 2006-05-22 sonrasi GLD'de olup GDX'te olmayan:", len(l.index[l.index >= g.index[0]].difference(g.index)))
print("  sifir getiri gunleri (bayat fiyat suphe): GDX", int((R.GDX == 0).sum()), "GLD", int((R.GLD == 0).sum()), "SPY", int((R.SPY == 0).sum()))
print("  |r|>%15 GDX gunleri:", R.GDX[R.GDX.abs() > 0.15].round(3).to_dict())

e250, B250 = rolling_resid(R, 250, 250)          # kuralin harfi: tam 250 gun
e60, B60 = rolling_resid(R, 250, 60)             # ana ajanin baslangici (min 60 gozlem)
X250 = e250.rolling(10, min_periods=10).sum()
X60 = e60.rolling(10, min_periods=10).sum()
print("\nartik e: ilk gecerli (250)", e250.first_valid_index().date(), "| (min60)", e60.first_valid_index().date())
print("beta ozet (250):"); print(B250.dropna().describe().loc[["mean", "min", "50%", "max"]].round(3).to_string())
print("beta yil sonu degerleri:"); print(B250.dropna().groupby(B250.dropna().index.year).last().round(3).T.to_string())

thr = {}
thr["A_2008_2017_w250"] = float(X250["2008-01-01":"2017-12-31"].dropna().quantile(0.8))
thr["B_tum_<=2017_w250"] = float(X250[:"2017-12-31"].dropna().quantile(0.8))
thr["C_tum_<=2017_min60 (ana ajan)"] = float(X60[:"2017-12-31"].dropna().quantile(0.8))
thr["D_2008_2017_min60"] = float(X60["2008-01-01":"2017-12-31"].dropna().quantile(0.8))
thr["E_2008_2016 (VIOP oncesi)"] = float(X250["2008-01-01":"2016-12-31"].dropna().quantile(0.8))
thr["F_2008_2017-03-03 (VIOP ilk gunu oncesi)"] = float(X250["2008-01-01":"2017-03-03"].dropna().quantile(0.8))
print("\nESIKLER (%80 kantil), %:")
for k, v in thr.items():
    print(f"  {k:45s} {v*100:.3f}")
print("  x'in 2008-2017 dagilimi (%):", (X250["2008-01-01":"2017-12-31"].describe() * 100).round(2).to_dict())
print("  2018+ doneminde x > esikA orani: %", round(float((X250["2018-01-01":] > thr["A_2008_2017_w250"]).mean() * 100), 1))

# ---------- 2) VIOP tarafi (ham bulten)
V, raw = viop_active_from_raw("XAUUSD")
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index).astype("datetime64[ns]")
print("\nVIOP gunleri (ham):", len(V), V.index[0].date(), "->", V.index[-1].date(), "| panel:", len(pv))
cmp = pd.DataFrame({"mine": V.ret, "panel": pv.v_ret, "code_m": V.code, "code_p": pv.v_code})
dif = cmp[(cmp.mine - cmp.panel).abs() > 1e-9]
print("  aktif kontrat kodu farkli gun:", int((cmp.code_m != cmp.code_p).sum()), "| getiri farki >1e-9 gun:", len(dif),
      "| korelasyon:", round(cmp[["mine", "panel"]].corr().iloc[0, 1], 6))
if len(dif):
    print(dif.head(20).to_string())
# prev_settle tutarliligi: ayni kontratin dunku uzlasmasi == bugunku prev_settle ?
raw = raw.sort_values(["code", "date"])
raw["settle_lag"] = raw.groupby("code").settle.shift(1)
raw["date_lag"] = raw.groupby("code").date.shift(1)
chk = raw.dropna(subset=["settle_lag"])
bad = chk[(chk.prev_settle - chk.settle_lag).abs() > 1e-6]
print("  prev_settle != dunku settle (ayni kontrat) satir:", len(bad), "/", len(chk))
if len(bad):
    print(bad[["date", "code", "settle", "prev_settle", "settle_lag", "date_lag", "oi", "volume"]].head(30).to_string())
    act_bad = bad.merge(V.reset_index()[["date", "code"]], on=["date", "code"])
    print("  bunlardan aktif kontrata denk gelen:", len(act_bad))
    if len(act_bad): print(act_bad[["date", "code", "settle", "prev_settle", "settle_lag", "date_lag"]].to_string())
# roll gunleri
roll = V.code != V.code.shift(1)
print("  roll (kod degisimi) gunu:", int(roll.sum()) - 1, "| vade gununde hala aktif olan gun:", int((V.expiry == V.index).sum()))
print("  vade gunu aktif:", [d.date().isoformat() for d in V.index[V.expiry == V.index]])
print("  |ret|>%4 gunler:", (V.ret[V.ret.abs() > 0.04] * 100).round(2).to_dict())
print("  hacimsiz (volume=0) aktif kontrat gunu:", int((V.volume == 0).sum()), "| settle==prev_settle gun:", int((V.ret == 0).sum()))

# ---------- 3) eslestirme ve zamanlama denetimi
xA, uA = map_last_us_before(V.index, X250)
D = pd.DataFrame({"x": xA, "us_date": uA, "ret": V.ret, "code": V.code, "settle": V.settle})
D["sig"] = (D.x > thr["A_2008_2017_w250"]).astype(float)
D.loc[D.x.isna(), "sig"] = np.nan
print("\nZAMANLAMA DENETIMI")
print("  us_date < t hepsinde:", bool((D.us_date < D.index).all()), "| min (t - us_date) gun:", int((D.index - D.us_date).dt.days.min()),
      "| maks:", int((D.index - D.us_date).dt.days.max()))
gap = (D.index - D.us_date).dt.days
print("  takvim gunu farki dagilimi:", gap.value_counts().sort_index().to_dict())
# is gunu farki: t ile us_date arasinda atlanan hafta ici gun
bd = pd.Series([np.busday_count(u.date(), t.date()) for u, t in zip(D.us_date, D.index)], index=D.index)
print("  is gunu farki dagilimi (1 = bir onceki is gunu ABD kapanisi):", bd.value_counts().sort_index().to_dict())
late = D[bd > 1]
print(f"  NYSE tatili yuzunden daha eski ABD kapanisi kullanilan VIOP gunu: {len(late)} (sinyalli: {int(late.sig.sum())})")
print("   ornek:", [(t.date().isoformat(), u.date().isoformat()) for t, u in zip(late.index[:12], late.us_date[:12])])
# ABD kapanisinin UTC ani ile VIOP uzlasma ani
import zoneinfo
ny = zoneinfo.ZoneInfo("America/New_York")
us_close_utc = pd.DatetimeIndex([pd.Timestamp(u.date().isoformat() + " 16:00", tz=ny).tz_convert("UTC").tz_localize(None) for u in D.us_date])
HALF = ["2017-08-31", "2018-06-14", "2018-08-20", "2019-06-03", "2019-10-28", "2020-07-30", "2020-10-28", "2021-05-12", "2021-07-19",
        "2021-10-28", "2022-07-08", "2022-10-28", "2023-04-20", "2023-06-27", "2024-04-09", "2024-10-28", "2025-06-05", "2025-10-28",
        "2026-03-19", "2026-05-26", "2026-10-28"]
HALF = pd.DatetimeIndex(HALF)
D["half"] = D.index.isin(HALF)
settle_utc = pd.DatetimeIndex([t + (pd.Timedelta("9h30m") if hf else pd.Timedelta("15h00m")) for t, hf in zip(D.index, D.half)])
lead_h = (settle_utc - us_close_utc) / pd.Timedelta("1h")
print("  (VIOP giris ani - kullanilan ABD kapanis ani) saat: min %.1f, medyan %.1f, maks %.1f ; negatif/sifir sayisi %d" % (lead_h.min(), np.median(lead_h), lead_h.max(), int((lead_h <= 0).sum())))
print("  yarim gun listesinden veri setinde islem gunu olan:", int(D.half.sum()), "/", len(HALF), "| eksik:", [d.date().isoformat() for d in HALF.difference(D.index)])
print("  yarim gunlerde sinyal:", int(D.sig[D.half].sum()), "gun;", D[D.half & (D.sig > 0)].index.strftime("%Y-%m-%d").tolist())
print("  yarim gunlerde (giris - ABD kapanis) saat min:", round(float(pd.Series(lead_h, index=D.index)[D.half].min()), 1))
# VIOP'un kapali, ABD'nin acik oldugu gunler (sinyal uretilir ama islem yapilamaz) ve tersi
us_days = X250.dropna().index
us_in = us_days[(us_days >= D.index[0]) & (us_days <= D.index[-1])]
print("  ABD acik/VIOP kapali gun:", len(us_in.difference(D.index)), "| VIOP acik/ABD kapali gun:", len(D.index.difference(us_in)))
# ayni ABD kapanisi iki VIOP gununde kullaniliyor mu (ABD tatili) / bir ABD kapanisi hic kullanilmiyor mu (TR tatili)
dup = D.us_date.duplicated().sum(); unused = len(us_in[:-1].difference(pd.DatetimeIndex(D.us_date)))
print("  ayni ABD kapanisinin tekrar kullanildigi VIOP gunu:", int(dup), "| hic kullanilmayan ABD kapanisi (TR tatili):", unused)

# ana ajanin sinyal dosyasi ile karsilastirma (yalniz okuma)
try:
    ms = pd.read_parquet(f"{S}/out/net/c1_viop_sig.parquet"); ms.index = pd.to_datetime(ms.index).astype("datetime64[ns]")
    xC, _ = map_last_us_before(V.index, X60)
    c = pd.DataFrame({"x_mine250": D.x, "x_mine60": xC, "x_main": ms.x, "sig_mine": D.sig, "sig_main": ms.sig})
    print("\nANA AJAN SINYALI ILE KARSILASTIRMA")
    print("  x korelasyonu (250 vs ana):", round(c.x_mine250.corr(c.x_main), 6), "| (min60 vs ana):", round(c.x_mine60.corr(c.x_main), 6),
          "| maks |fark| min60:", float((c.x_mine60 - c.x_main).abs().max()), "| maks |fark| w250:", float((c.x_mine250 - c.x_main).abs().max()))
    print("  sinyal gunu: benim (esik A)", int(c.sig_mine.sum()), "| ana ajan", int(c.sig_main.sum()), "| farkli gun:", int((c.sig_mine != c.sig_main).sum()))
    dd = c[c.sig_mine != c.sig_main]
    if len(dd): print(dd.assign(x_mine250=lambda z: z.x_mine250 * 100, x_main=lambda z: z.x_main * 100).round(3).head(30).to_string())
except Exception as ex:
    print("ana ajan sinyal dosyasi okunamadi:", ex)

D["us_close_utc"] = us_close_utc
D.to_parquet(f"{OUT}/rep_signal_viop.parquet")
pd.DataFrame({"e250": e250, "X250": X250, "e60": e60, "X60": X60}).to_parquet(f"{OUT}/rep_us_resid.parquet")
V.to_parquet(f"{OUT}/rep_viop_active.parquet")
json.dump({k: v for k, v in thr.items()}, open(f"{OUT}/rep_esik.json", "w"), indent=1)
print("\nsinyal gunu (esik A, 2008-2017, w250):", int(D.sig.sum()), "/", len(D), " = %", round(D.sig.mean() * 100, 1))
print("yillara gore sinyal gunu:", D.sig.groupby(D.index.year).sum().astype(int).to_dict())
print("son 12 VIOP gunu:"); print(D[["us_date", "x", "sig", "ret", "code"]].tail(12).assign(x=lambda z: (z.x * 100).round(2), ret=lambda z: (z.ret * 100).round(2)).to_string())
