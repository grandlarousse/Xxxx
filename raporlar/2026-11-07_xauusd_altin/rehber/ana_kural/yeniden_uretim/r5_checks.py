"""r5: ek denetimler — Yahoo tarih hizasi (bir gunluk kayma var mi), elle HAC, ortusmeyen ornekleme, 2018-2024, likidite, guncel durum."""
import json, zoneinfo
from rep_lib import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
thr = json.load(open(f"{OUT}/rep_esik.json")); thA = thr["A_2008_2017_w250"]; thC = thr["C_tum_<=2017_min60 (ana ajan)"]
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet"); r = D.ret
US = pd.read_parquet(f"{OUT}/rep_us_resid.parquet")
R = us_returns("adjclose")

# ---- 1) Yahoo tarih hizasi: GLD gunluk getirisi ile Dukascopy spotun 16:00 ET -> 16:00 ET getirisi
dk = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet"); dk.index = pd.DatetimeIndex(dk.index).tz_convert("UTC").tz_localize(None)
pc = pd.Series(dk.c.values, index=dk.index + pd.Timedelta("1h"))
ny = zoneinfo.ZoneInfo("America/New_York")
ts = pd.DatetimeIndex([pd.Timestamp(d.date().isoformat() + " 16:00", tz=ny).tz_convert("UTC").tz_localize(None) for d in R.index])
sp = pd.Series(pc.reindex(ts).values, index=R.index)
sret = np.log(sp).diff()
print("YAHOO TARIH HIZASI (GLD getirisi vs spot altin 16:00 ET->16:00 ET):")
for a, b, lab in [("2008-01-01", "2016-12-31", "2008-16"), ("2017-01-01", None, "2017-26")]:
    g = R.GLD.loc[a:b]; s = sret.loc[a:b]
    print(f"  {lab}: es zamanli korelasyon {g.corr(s):.3f} | GLD(d) ~ spot(d-1) {g.corr(s.shift(1)):.3f} | GLD(d) ~ spot(d+1) {g.corr(s.shift(-1)):.3f} | n {int((g.notna() & s.notna()).sum())}")
print("  GDX(d) ~ GLD(d) %.3f | GDX(d) ~ GLD(d-1) %.3f | GDX(d) ~ GLD(d+1) %.3f" % (R.GDX.corr(R.GLD), R.GDX.corr(R.GLD.shift(1)), R.GDX.corr(R.GLD.shift(-1))))
try:
    d5 = pd.read_parquet(f"{S}/panel/duka/USA500IDXUSD.parquet"); d5.index = pd.DatetimeIndex(d5.index).tz_convert("UTC").tz_localize(None)
    p5 = pd.Series(d5.c.values, index=d5.index + pd.Timedelta("1h")); s5 = np.log(pd.Series(p5.reindex(ts).values, index=R.index)).diff()
    print("  SPY(d) ~ S&P500 CFD(d) %.3f | (d-1) %.3f | (d+1) %.3f" % (R.SPY.corr(s5), R.SPY.corr(s5.shift(1)), R.SPY.corr(s5.shift(-1))))
except Exception as ex:
    print("  S&P CFD kontrolu yapilamadi:", ex)
# panel y_GDX ile benim eslestirmem ayni kapanisi mi kullaniyor
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index).astype("datetime64[ns]")
gd = load_yahoo("GDX"); mine_px, mine_dt = map_last_us_before(D.index, gd)
print("  panel y_GDX == benim (tarih<t son kapanis) GDX fiyatim: maks |fark|", float((pv.y_GDX - mine_px).abs().max()))
av = pd.to_datetime(pv.y_GDX_avail)
print("  panel y_GDX_avail her zaman < gun t 15:00 UTC:", bool((av < (pv.index + pd.Timedelta("15h"))).all()), "| yarim gunlerde < 09:30 UTC:", bool((av[D.half] < (pv.index[D.half] + pd.Timedelta("9h30m"))).all()))

# ---- 2) elle Newey-West (Bartlett) — statsmodels'ten bagimsiz
def manual_nw(y, s, L):
    d = pd.concat([y.rename("y"), s.rename("s")], axis=1).dropna()
    X = np.column_stack([np.ones(len(d)), d.s.values]); yv = d.y.values
    b = np.linalg.solve(X.T @ X, X.T @ yv); u = yv - X @ b; Z = X * u[:, None]
    Sg = Z.T @ Z
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = Z[l:].T @ Z[:-l]; Sg += w * (G + G.T)
    XtXi = np.linalg.inv(X.T @ X); V = XtXi @ Sg @ XtXi
    return b[1], b[1] / np.sqrt(V[1, 1])
print("\nELLE NEWEY-WEST (kucuk orneklem duzeltmesiz) vs statsmodels:")
for tn, th in (("A", thA), ("C", thC)):
    sig = (D.x > th).astype(float)
    for h in (1, 3, 5):
        f = fwd_sum(r, h); b, t = manual_nw(f, sig, max(h, 5)); st = nw_diff(f, sig, max(h, 5))
        print(f"  esik {tn} h{h}: elle fark {b*100:+.3f}% t {t:.2f} | statsmodels t {st['t']:.2f}")

# ---- 3) ortusmeyen ornekleme: her h gunde bir (h faz), Welch t ; fazlarin ortalamasi
from scipy import stats as ss
print("\nORTUSMEYEN ORNEKLEME (her h. gun; h ayri faz) — sinyal vs diger, Welch t:")
for tn, th in (("A", thA), ("C", thC)):
    sig = (D.x > th).astype(float)
    for h in (3, 5):
        f = fwd_sum(r, h); ts_ = []
        for ph in range(h):
            idx = np.arange(ph, len(f), h); ff = f.iloc[idx]; s2 = sig.iloc[idx]; m = ff.notna()
            ts_.append(ss.ttest_ind(ff[m & (s2 > 0)], ff[m & (s2 == 0)], equal_var=False).statistic)
        print(f"  esik {tn} h{h}: faz t'leri {np.round(ts_, 2).tolist()} | ortalama {np.mean(ts_):.2f}")

# ---- 4) 2018-2024 (ara 7 yil) ve 2017 + 2025-26 payi
print("\nALT DONEMLER:")
for tn, th in (("A", thA), ("C", thC)):
    sig = (D.x > th).astype(float)
    for h in (3, 5):
        a = event_stats(r, sig, h, "2018-01-01", "2024-12-31"); b = event_stats(r, sig, h, "2018-01-01", "2021-12-31"); c = event_stats(r, sig, h, None, "2017-12-31")
        print(f"  esik {tn} h{h}: 2018-2024 fark {a['diff']:+.3f}% t {a['t_nw']:.2f} (n {a['n_sig']}) | 2018-2021 {b['diff']:+.3f}% t {b['t_nw']:.2f} | 2017(03-12) {c['diff']:+.3f}% t {c['t_nw']:.2f} (n {c['n_sig']})")

# ---- 5) likidite: aktif kontrat hacmi
V = pd.read_parquet(f"{OUT}/rep_viop_active.parquet")
vl = pd.read_parquet(f"{S}/panel/viop_long.parquet"); xv = vl[vl.root == "XAUUSD"]
tot = xv.groupby("date").agg(volume=("volume", "sum"), value=("value", "sum"), trades=("trades", "sum"))
print("\nLIKIDITE (F_XAUUSD, tum vadeler toplam; yillik medyan gunluk): kontrat / milyon TL / islem")
print(tot.groupby(pd.to_datetime(tot.index).year).median().assign(value=lambda z: z.value / 1e6).round(0).T.to_string())

# ---- 6) guncel durum (veri sonu)
print("\nGUNCEL: son ABD kapanislari ve x (%):")
print((US[["e250", "X250"]].tail(8) * 100).round(2).to_string())
print("  esik A %.3f%% | esik C %.3f%% | son ABD kapanisi %s x = %.2f%% -> bir sonraki VIOP gunu icin sinyal: %s" % (thA * 100, thC * 100, US.index[-1].date(), US.X250.iloc[-1] * 100, "VAR" if US.X250.iloc[-1] > thA else "YOK"))
print("  son VIOP gunu veri setinde:", D.index[-1].date(), "| o gun sinyal:", int(D.sig.iloc[-1]))

# ---- 7) sinyal yogunlugu ve oynaklik rejimi
vol20 = r.rolling(20).std().shift(1) * np.sqrt(252) * 100
sigA = (D.x > thA).astype(float)
print("\nSINYAL ve OYNAKLIK: sinyal gunlerinde onceki 20 gun VIOP oynakligi ort %.1f | diger %.1f" % (vol20[sigA > 0].mean(), vol20[sigA == 0].mean()))
hi = vol20 > vol20.median()
for lab, m in (("yuksek oynaklik yarisi", hi), ("dusuk oynaklik yarisi", ~hi)):
    for h in (3, 5):
        st = nw_diff(fwd_sum(r, h)[m], sigA[m], 5); print(f"  {lab} h{h}: fark {st['b']*100:+.3f}% t {st['t']:.2f} (n {st['n1']})")
