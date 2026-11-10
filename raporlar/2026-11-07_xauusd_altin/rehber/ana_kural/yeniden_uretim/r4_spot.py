"""r4: spot altin (Dukascopy saatlik, 15:00 UTC fiyati = 14:00 barinin kapanisi) ile tekrar; 2010-2016 ve diger donemler.
Ayrica: ABD kapanisi (sinyal ani) -> ertesi gun 15:00 UTC (giris ani) arasinda kacan getiri."""
import json, zoneinfo
from rep_lib import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
thr = json.load(open(f"{OUT}/rep_esik.json"))
US = pd.read_parquet(f"{OUT}/rep_us_resid.parquet")
dk = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet")
dk.index = pd.DatetimeIndex(dk.index).tz_convert("UTC").tz_localize(None)
b14 = dk[dk.index.hour == 14]
p15 = pd.Series(b14.c.values, index=pd.DatetimeIndex(b14.index.normalize()).astype("datetime64[ns]"))
p15 = p15[p15.index.dayofweek < 5]
print("spot 15:00 UTC gun sayisi:", len(p15), p15.index[0].date(), "->", p15.index[-1].date())
print("  yillara gore:", p15.groupby(p15.index.year).size().to_dict())
# panel_spot ile karsilastir (yalniz dogrulama)
ps = pd.read_parquet(f"{S}/panel/panel_spot.parquet"); ps.index = pd.to_datetime(ps.index).astype("datetime64[ns]")
c = pd.concat([p15.rename("mine"), ps.xau_p15.rename("panel")], axis=1).dropna()
print("  panel_spot.xau_p15 ile maks |fark|:", float((c.mine - c.panel).abs().max()), "| ortak gun", len(c), "| panelde olup bende olmayan:", len(ps.index.difference(p15.index)), "| bende olup panelde olmayan:", len(p15.index[p15.index >= ps.index[0]].difference(ps.index)))
sr = np.log(p15).diff()
x, ud = map_last_us_before(p15.index, US.X250)
print("  us_date < t hepsinde:", bool((ud.dropna() < ud.dropna().index).all()))
PER = [("2010-2016", "2010-01-01", "2016-12-31"), ("2008-2009", "2008-01-01", "2009-12-31"), ("2010-2012", "2010-01-01", "2012-12-31"), ("2013-2016", "2013-01-01", "2016-12-31"),
       ("2017-03..2026-10 (VIOP donemi)", "2017-03-06", None), ("2018-2026", "2018-01-01", None), ("2008-2026 tum", None, None)]
for tn, th in [("A 2.541%", thr["A_2008_2017_w250"]), ("C 2.307% (ana ajan)", thr["C_tum_<=2017_min60 (ana ajan)"])]:
    sig = (x > th).astype(float); sig[x.isna()] = np.nan
    rows = []
    for h in (1, 3, 5):
        for pn, a, b in PER:
            st = event_stats(sr, sig, h, a, b); st["donem"] = pn; rows.append(st)
    T = pd.DataFrame(rows)[["h", "donem", "N", "n_sig", "mean_sig", "mean_all", "mean_off", "diff", "t_nw", "hit_sig", "hit_all"]]
    print(f"\n=== SPOT, esik {tn}"); print(T.round(3).to_string(index=False))
    yy = []
    for y in range(2008, 2027):
        row = dict(yil=y)
        for h in (3, 5):
            st = event_stats(sr, sig, h, f"{y}-01-01", f"{y}-12-31"); row.update({"n": st["n_sig"], f"h{h}_fark": st["diff"]})
        yy.append(row)
    Y = pd.DataFrame(yy).set_index("yil"); print("  yil yil fark (%):"); print(Y.round(2).T.to_string())
    print("  fark>0 yil: h3 %d/%d, h5 %d/%d" % ((Y.h3_fark > 0).sum(), len(Y), (Y.h5_fark > 0).sum(), len(Y)))

# --- kacan aralik: ABD kapanisi (t-1, 16:00 ET) -> t 15:00 UTC
ny = zoneinfo.ZoneInfo("America/New_York")
pc = dk.c.copy(); pc.index = pc.index + pd.Timedelta("1h")          # fiyat ani = bar basi + 1 saat
def px_at(ts):
    try:
        return pc.loc[ts]
    except KeyError:
        s = pc.loc[:ts]
        return s.iloc[-1] if len(s) and (ts - s.index[-1]) <= pd.Timedelta("3h") else np.nan
sig = (x > thr["A_2008_2017_w250"]).astype(float)
gap = []
for t, u in ud.dropna().items():
    cu = pd.Timestamp(u.date().isoformat() + " 16:00", tz=ny).tz_convert("UTC").tz_localize(None)
    a = px_at(cu); b = p15.get(t, np.nan)
    gap.append((t, np.log(b / a) if a == a and b == b else np.nan))
gap = pd.Series(dict(gap))
for pn, a, b in [("2010-2016", "2010-01-01", "2016-12-31"), ("2017-03..2026-10", "2017-03-06", None), ("tum", None, None)]:
    g = gap.loc[a:b]; s = sig.reindex(g.index)
    d = nw_diff(g, s, 5)
    print(f"ABD kapanisi(t-1) -> 15:00 UTC(t) spot getirisi {pn}: sinyal gunleri {g[s>0].mean()*100:+.3f}% | diger {g[s==0].mean()*100:+.3f}% | fark {d['b']*100:+.3f}% t {d['t']:.2f} (n {d['n1']})")

# --- VIOP uzlasmasi ile spot 15:00 UTC tutarliligi (2017+) ve yarim gunler
V = pd.read_parquet(f"{OUT}/rep_viop_active.parquet"); D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet")
j = pd.concat([V.ret.rename("v"), sr.rename("s")], axis=1).dropna()
print("\nVIOP uzlasma getirisi ile spot 15:00 UTC getirisi (ayni gunler):", len(j), "gun; korelasyon", round(j.corr().iloc[0, 1], 4), "| fark ss (bps)", round((j.v - j.s).std() * 1e4, 1))
# yarim gunlerde uzlasma hangi saate yakin? baz = log(settle/spot_h) ; normal gunlerde 15:00 bazindan sapma
pall = pd.Series(dk.c.values, index=dk.index + pd.Timedelta("1h"))
def spot_at(day, hh):
    return pall.get(day + pd.Timedelta(hours=hh), np.nan)
norm_b = np.log(V.settle / p15.reindex(V.index)).dropna()
basis_roll = norm_b.rolling(5, min_periods=3).median().shift(1)
rows = []
for d in D.index[D.half]:
    row = dict(gun=d.date().isoformat(), sinyal=int(D.sig[d]))
    for hh in (9, 10, 11, 15):
        sp = spot_at(d, hh)
        row[f"baz{hh:02d}_bps"] = (np.log(V.settle[d] / sp) - basis_roll.get(d, np.nan)) * 1e4 if sp == sp else np.nan
    rows.append(row)
HB = pd.DataFrame(rows)
print("yarim gunler: uzlasma - spot(HH:00 UTC) bazinin, onceki 5 gunun 15:00 bazindan sapmasi (bps). Kucuk olan saat = uzlasma ani:")
print(HB.round(1).to_string(index=False))
print("  ort |sapma| bps: 09:00 %.1f | 10:00 %.1f | 11:00 %.1f | 15:00 %.1f" % tuple(HB[[f"baz{h:02d}_bps" for h in (9, 10, 11, 15)]].abs().mean()))
nb = (norm_b - basis_roll).dropna(); nb = nb[~nb.index.isin(D.index[D.half])]
print("  normal gunlerde 15:00 bazinin kendi 5 gunluk medyanindan sapmasi: MAD %.1f bps, ort|.| %.1f bps" % (nb.abs().median() * 1e4, nb.abs().mean() * 1e4))
