"""r2: olay istatistikleri (sinyal sonrasi 1/3/5 gun), donemler, yil yil, saglamlik."""
import json
from rep_lib import *
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60); pd.set_option("display.max_rows", 400)
D = pd.read_parquet(f"{OUT}/rep_signal_viop.parquet")
thr = json.load(open(f"{OUT}/rep_esik.json"))
TH = {"A(2008-17)=%.3f%%" % (thr["A_2008_2017_w250"] * 100): thr["A_2008_2017_w250"],
      "C(ana ajan,2006-17)=%.3f%%" % (thr["C_tum_<=2017_min60 (ana ajan)"] * 100): thr["C_tum_<=2017_min60 (ana ajan)"]}
r = D.ret
PER = [("2017-03..2026-11", None, None), ("2017-21", None, "2021-12-31"), ("2022-26", "2022-01-01", None), ("2018-26", "2018-01-01", None),
       ("2022-24", "2022-01-01", "2024-12-31"), ("2025-26", "2025-01-01", None), ("2017-24 (25-26 haric)", None, "2024-12-31")]
ALL = []
for nm, th in TH.items():
    sig = (D.x > th).astype(float)
    print(f"\n================ ESIK {nm} | sinyal gunu {int(sig.sum())}/{len(sig)} (%{sig.mean()*100:.1f})")
    rows = []
    for h in (1, 3, 5):
        for pn, a, b in PER:
            st = event_stats(r, sig, h, a, b); st["donem"] = pn; st["esik"] = nm; rows.append(st)
    T = pd.DataFrame(rows)[["h", "donem", "N", "n_sig", "mean_sig", "mean_all", "mean_off", "diff_vs_all", "diff", "t_nw", "hit_sig", "hit_all"]]
    print(T.round(3).to_string(index=False)); ALL.append(T.assign(esik=nm))
    # NW lag duyarliligi
    print("  NW gecikme duyarliligi (tam donem) t:", {f"h{h}_L{L}": round(event_stats(r, sig, h, L=L)["t_nw"], 2) for h in (3, 5) for L in (3, 5, 10, 20)})
    # yil yil
    yy = []
    for y in range(2017, 2027):
        a, b = f"{y}-01-01", f"{y}-12-31"
        row = dict(yil=y)
        for h in (1, 3, 5):
            st = event_stats(r, sig, h, a, b)
            row.update({f"n": st["n_sig"], f"h{h}_sin": st["mean_sig"], f"h{h}_tum": st["mean_all"], f"h{h}_fark": st["diff"], f"h{h}_isb": st["hit_sig"]})
        yy.append(row)
    Y = pd.DataFrame(yy).set_index("yil")
    print("  yil yil (ort %, fark = sinyal - diger gunler, isb = isabet %):"); print(Y.round(2).to_string())
    print("  fark>0 olan yil sayisi: h1 %d/10, h3 %d/10, h5 %d/10 | sinyal ort>tum ort: h3 %d/10, h5 %d/10" % (
        (Y.h1_fark > 0).sum(), (Y.h3_fark > 0).sum(), (Y.h5_fark > 0).sum(), (Y.h3_sin > Y.h3_tum).sum(), (Y.h5_sin > Y.h5_tum).sum()))
    Y.to_csv(f"{OUT}/rep_yillik_{nm[0]}.csv")
pd.concat(ALL).to_csv(f"{OUT}/rep_olay.csv", index=False)

# ---------------- saglamlik: esik A
sig = (D.x > thr["A_2008_2017_w250"]).astype(float)
print("\n================ SAGLAMLIK (esik A)")
# 1) plasebo: sinyali dairesel kaydir (otokorelasyon yapisi korunur) -> fark dagilimi
rng = np.random.default_rng(7)
for h in (3, 5):
    f = fwd_sum(r, h); obs = f[sig > 0].mean() - f[sig == 0].mean()
    sv = sig.values; fv = f.values; out = []
    for k in range(2000):
        s2 = np.roll(sv, rng.integers(30, len(sv) - 30))
        m = ~np.isnan(fv)
        out.append(fv[m & (s2 > 0)].mean() - fv[m & (s2 == 0)].mean())
    out = np.array(out)
    print(f"  dairesel kaydirma plasebosu h{h}: gozlenen fark {obs*100:+.3f}%, plasebo ort {out.mean()*100:+.3f}% ss {out.std()*100:.3f}%, tek yanli p = {(out >= obs).mean():.3f}, z = {(obs-out.mean())/out.std():.2f}")
# 2) ortusmeyen: sinyal kumelerinin (ardisik sinyal gunleri) ILK gunu -> h gun sonrasi
first = (sig > 0) & (sig.shift(1).fillna(0) == 0)
print("  sinyal kumesi (ardisik blok) sayisi:", int(first.sum()), "| ort blok uzunlugu:", round(sig.sum() / first.sum(), 2))
for h in (1, 3, 5):
    f = fwd_sum(r, h)
    a = f[first].dropna(); base = f.dropna()
    from scipy import stats as ss
    t1 = ss.ttest_1samp(a - base.mean(), 0)
    print(f"  blok ILK gunu h{h}: n {len(a)}, ort {a.mean()*100:+.3f}% (tum {base.mean()*100:+.3f}%), isabet %{(a>0).mean()*100:.0f}, (ort - tum ort) t = {t1.statistic:.2f}")
# 3) sinyal gecikme/kaydirma (ileri bakma testi): sig.shift(k)
print("  sinyal kaydirma -> h3 / h5 fark (t):")
for k in (-5, -3, -2, -1, 0, 1, 2, 3, 5, 10):
    s2 = sig.shift(k)
    a3 = nw_diff(fwd_sum(r, 3), s2, 5); a5 = nw_diff(fwd_sum(r, 5), s2, 5)
    print(f"    kaydirma {k:+d}: h3 {a3['b']*100:+.3f}% (t {a3['t']:.2f}) | h5 {a5['b']*100:+.3f}% (t {a5['t']:.2f})")
# 4) ayni gun (t-1 uzlasma -> t uzlasma) getirisi: sinyalin bilindigi ama alinamayan aralik
a0 = nw_diff(r, sig, 5)
print(f"  sinyal gunu t'nin kendi getirisi (t-1->t uzlasma; ABD kapanisindan ONCE baslar, yakalanamaz): fark {a0['b']*100:+.3f}% t {a0['t']:.2f}")
# 5) altin momentumu kontrolu: GLD 10 gunluk getiri (t-1 ABD kapanisi) ve VIOP'un kendi 10 gunluk getirisi (t-1 uzlasma)
R = us_returns("adjclose")
gld10 = R.GLD.rolling(10).sum(); gdx10 = R.GDX.rolling(10).sum(); spy10 = R.SPY.rolling(10).sum()
g10, _ = map_last_us_before(D.index, gld10); m10, _ = map_last_us_before(D.index, gdx10); s10, _ = map_last_us_before(D.index, spy10)
v10 = r.rolling(10).sum().shift(1)
print("  cok degiskenli (HAC L=5): fwd_h ~ sig + GLD10 + VIOP10(t-1)")
for h in (3, 5):
    for pn, a, b in [("tam", None, None), ("2018-26", "2018-01-01", None)]:
        d = pd.concat([fwd_sum(r, h).rename("y"), sig.rename("sig"), g10.rename("gld10"), v10.rename("v10")], axis=1).dropna().loc[a:b]
        m = sm.OLS(d.y, sm.add_constant(d[["sig", "gld10", "v10"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        print(f"    h{h} {pn}: sig {m.params['sig']*100:+.3f}% (t {m.tvalues['sig']:.2f}) | gld10 t {m.tvalues['gld10']:.2f} | v10 t {m.tvalues['v10']:.2f}")
print("  sinyal ile GLD10 korelasyonu:", round(sig.corr(g10), 3), "| sinyal gunlerinde GLD10 ort %", round(g10[sig > 0].mean() * 100, 2), "tum gunler %", round(g10.mean() * 100, 2))
# 6) alternatif 'basit' sinyaller: ham GDX 10 gun > %80 kantil ; GLD 10 gun > %80 kantil (2008-2017)
for nm2, ser in [("ham GDX 10g", gdx10), ("GLD 10g", gld10), ("GDX10 - 2*GLD10 (sabit beta)", gdx10 - 2 * gld10)]:
    th2 = float(ser["2008-01-01":"2017-12-31"].quantile(0.8)); xx, _ = map_last_us_before(D.index, ser); s2 = (xx > th2).astype(float)
    a3 = nw_diff(fwd_sum(r, 3), s2, 5); a5 = nw_diff(fwd_sum(r, 5), s2, 5)
    print(f"  alternatif {nm2:30s} esik %{th2*100:.2f} n {int(s2.sum())}: h3 {a3['b']*100:+.3f}% (t {a3['t']:.2f}) | h5 {a5['b']*100:+.3f}% (t {a5['t']:.2f})")
# 7) esik / pencere / beta penceresi duyarliligi
US = pd.read_parquet(f"{OUT}/rep_us_resid.parquet")
print("  esik kantili duyarliligi (2008-2017 dagilimi):")
for q in (0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95):
    th2 = float(US.X250["2008-01-01":"2017-12-31"].quantile(q)); s2 = (D.x > th2).astype(float)
    a1 = nw_diff(fwd_sum(r, 1), s2, 5); a3 = nw_diff(fwd_sum(r, 3), s2, 5); a5 = nw_diff(fwd_sum(r, 5), s2, 5)
    print(f"    q{q}: esik %{th2*100:.2f} n {int(s2.sum())}: h1 t {a1['t']:.2f} | h3 {a3['b']*100:+.3f}% t {a3['t']:.2f} | h5 {a5['b']*100:+.3f}% t {a5['t']:.2f}")
print("  pencere k duyarliligi (q80, 2008-2017):")
for k in (3, 5, 8, 10, 12, 15, 20):
    Xk = US.e250.rolling(k, min_periods=k).sum(); th2 = float(Xk["2008-01-01":"2017-12-31"].quantile(0.8)); xx, _ = map_last_us_before(D.index, Xk); s2 = (xx > th2).astype(float)
    a3 = nw_diff(fwd_sum(r, 3), s2, 5); a5 = nw_diff(fwd_sum(r, 5), s2, 5)
    print(f"    k{k}: n {int(s2.sum())}: h3 {a3['b']*100:+.3f}% t {a3['t']:.2f} | h5 {a5['b']*100:+.3f}% t {a5['t']:.2f}")
print("  beta penceresi / veri sutunu duyarliligi (k10, q80 2008-2017):")
for lab, col, win in [("adjclose w120", "adjclose", 120), ("adjclose w500", "adjclose", 500), ("close(temettu duzeltmesiz) w250", "close", 250)]:
    R2 = us_returns(col); e2, _ = rolling_resid(R2, win, win); X2 = e2.rolling(10, min_periods=10).sum()
    th2 = float(X2["2008-01-01":"2017-12-31"].quantile(0.8)); xx, _ = map_last_us_before(D.index, X2); s2 = (xx > th2).astype(float)
    a3 = nw_diff(fwd_sum(r, 3), s2, 5); a5 = nw_diff(fwd_sum(r, 5), s2, 5)
    print(f"    {lab:34s} esik %{th2*100:.2f} n {int(s2.sum())} (esik A ile farkli gun {int((s2 != sig).sum())}): h3 {a3['b']*100:+.3f}% t {a3['t']:.2f} | h5 {a5['b']*100:+.3f}% t {a5['t']:.2f}")
# 8) yarim gunler ve NYSE-tatili sonrasi gunler haric
half = D.half
bd = pd.Series([np.busday_count(u.date(), t.date()) for u, t in zip(D.us_date, D.index)], index=D.index)
for lab, mask in [("yarim gun girisleri haric", ~half), ("NYSE tatili sonrasi (bayat sinyal) haric", bd == 1), ("vade gunu aktif gunler haric", D.index.to_series().ne(pd.read_parquet(f"{OUT}/rep_viop_active.parquet").expiry))]:
    s2 = sig.where(mask)
    a3 = nw_diff(fwd_sum(r, 3), s2, 5); a5 = nw_diff(fwd_sum(r, 5), s2, 5)
    print(f"  {lab:42s}: h3 {a3['b']*100:+.3f}% t {a3['t']:.2f} (n {a3['n1']}) | h5 {a5['b']*100:+.3f}% t {a5['t']:.2f}")
# 9) en buyuk gunlerin etkisi: 2026-01-28..02-02 ve fwd'nin %1 kirpilmasi
for h in (3, 5):
    f = fwd_sum(r, h); lo, hi = f.quantile(0.01), f.quantile(0.99); fw = f.clip(lo, hi)
    a = nw_diff(fw, sig, 5); print(f"  %1-%99 kirpilmis fwd h{h}: fark {a['b']*100:+.3f}% t {a['t']:.2f}")
    # medyan farki
    print(f"    medyan: sinyal {f[sig>0].median()*100:+.3f}% | tum {f.median()*100:+.3f}%")
