"""r6: x'in dilimlerine gore sonraki getiri (monotonluk) — VIOP 2017-2026 ve spot 2008-2026; guncel asiri okuma (x ~ %9,7) icin."""
from rep_lib import *
pd.set_option("display.width", 250)
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet"); r = D.ret
US = pd.read_parquet(f"{OUT}/rep_us_resid.parquet")
ref = US.X250["2008-01-01":"2017-12-31"].dropna()
qs = [0, .2, .4, .5, .6, .8, .9, .95, 1.0]; edges = [ref.quantile(q) for q in qs]; edges[0] = -np.inf; edges[-1] = np.inf
print("dilim sinirlari (2008-2017 kantilleri) %:", [round(e * 100, 2) for e in edges[1:-1]])
def tab(x, ret, lab, a=None, b=None):
    rows = []
    for i in range(len(edges) - 1):
        m = (x > edges[i]) & (x <= edges[i + 1])
        row = dict(dilim=f"q{qs[i]:.2f}-{qs[i+1]:.2f}")
        for h in (1, 3, 5):
            f = fwd_sum(ret, h).loc[a:b]; mm = m.reindex(f.index).fillna(False)
            row.update({"n": int((mm & f.notna()).sum()), f"h{h}": f[mm].mean() * 100, f"h{h}_isb": (f[mm] > 0).mean() * 100})
        rows.append(row)
    allr = dict(dilim="TUM")
    for h in (1, 3, 5):
        f = fwd_sum(ret, h).loc[a:b]; allr.update({"n": int(f.notna().sum()), f"h{h}": f.mean() * 100, f"h{h}_isb": (f > 0).mean() * 100})
    rows.append(allr)
    print(f"\n{lab}"); print(pd.DataFrame(rows).round(3).to_string(index=False))
tab(D.x, r, "VIOP 2017-03..2026-11")
tab(D.x, r, "VIOP 2018-2026", "2018-01-01")
dk = pd.read_parquet(f"{S}/panel/duka/XAUUSD.parquet"); dk.index = pd.DatetimeIndex(dk.index).tz_convert("UTC").tz_localize(None)
b14 = dk[dk.index.hour == 14]; p15 = pd.Series(b14.c.values, index=pd.DatetimeIndex(b14.index.normalize()).astype("datetime64[ns]")); p15 = p15[p15.index.dayofweek < 5]
sr = np.log(p15).diff(); xs, _ = map_last_us_before(p15.index, US.X250)
tab(xs, sr, "SPOT 15:00 UTC 2008-2026"); tab(xs, sr, "SPOT 2010-2016", "2010-01-01", "2016-12-31"); tab(xs, sr, "SPOT 2018-2026", "2018-01-01")
# asiri okuma: x > %6,3 ve x > %8
for lab, x, ret in (("VIOP", D.x, r), ("SPOT 2008-26", xs, sr)):
    for cut in (0.063, 0.08):
        s = (x > cut).astype(float)
        for h in (3, 5):
            st = event_stats(ret, s, h); print(f"{lab} x>%{cut*100:.1f}: h{h} n {st['n_sig']} sinyal ort {st['mean_sig']:+.3f}% tum {st['mean_all']:+.3f}% fark t {st['t_nw']:.2f} isabet %{st['hit_sig']:.0f}")
# rank IC (surekli)
from scipy import stats as ss
for lab, x, ret, a in (("VIOP tam", D.x, r, None), ("VIOP 2018+", D.x, r, "2018-01-01"), ("SPOT 2008-26", xs, sr, None)):
    for h in (1, 3, 5):
        d = pd.concat([fwd_sum(ret, h).rename("f"), x.rename("x")], axis=1).dropna().loc[a:]
        print(f"rank IC {lab} h{h}: {ss.spearmanr(d.x, d.f).statistic:.3f} (n {len(d)})")
