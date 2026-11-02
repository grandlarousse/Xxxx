"""s04: (a) TRALT gün-içi ~ Çin/HK altın sinyalleri — derin çürütme testleri (günlük veri, 2014+).
 1) Sinyali günlük bileşenlere ayır: Asya gap (önceki kapanış -> yerel açılış 01:30 UTC; BIST t-1 seansı + ABD gecesini içerir)
    ve Asya gün-içi (01:30 -> 07:00/08:10 UTC t; BIST t-1 kapanışından SONRA, BIST t açılışından ÖNCE (SSE) / örtüşmeli (HK)).
 2) Bayat açılış testi: TRALT açılışı == önceki kapanış olan günler vs diğerleri.
 3) Kontroller: TRALT gap_t (açılış bilgiyi fiyatladı mı), kendi gecikmesi, XU100 gap/gün-içi gecikmesi, ABD GC/GDX t-1.
 4) At yarışı: 600547 vs 1787 vs 518880 (SSE altın ETF) vs 601899.
 5) Uç değer: winsorize %1, Spearman, en iyi 10 günü at, |sinyal| eşikleri.
 6) Yıllar, tatil sonrası günler hariç, dairesel kaydırma null'u."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
from scipy.stats import spearmanr
tr = bist_dec("TRALT.IS"); xu = bist_dec("XU100.IS")
y = tr.intra
def comp(sym):
    d = daily_local(sym); af = d["adj"] / d["c"]
    cc = np.log(d["adj"]).diff(); intra = np.log(d["c"] / d["o"]); gap = cc - intra
    return {k: to_bist(v, "zero").reindex(y.index) for k, v in dict(cc=cc, gap=gap, intra=intra).items()}
SIG = {s: comp(s) for s in ["600547.SS", "1787.HK", "518880.SS", "601899.SS", "2899.HK"]}
print("== 1) Bileşenler -> TRALT gün-içi (r, NW t, n) ==")
for s, c in SIG.items():
    out = []
    for k in ["cc", "gap", "intra"]:
        b, t, n = nw_t(y, c[k]); out.append(f"{k}: r={b:+.3f} t={t:+.2f}")
    print(f"{s:10s} " + " | ".join(out) + f" n={n}")
s6 = SIG["600547.SS"]; h7 = SIG["1787.HK"]; g8 = SIG["518880.SS"]
print("\n== 1b) Bileşenlerin TRALT GAP_t ile ilişkisi (açılışta fiyatlanma) ==")
for s, c in SIG.items():
    print(f"{s:10s} " + " | ".join(f"{k}: r={nw_t(tr.gap, c[k])[0]:+.3f} t={nw_t(tr.gap, c[k])[1]:+.2f}" for k in ["cc", "gap", "intra"]))
print("\n== 2) Bayat açılış ayrımı (TRALT o == önceki c) ==")
d = daily_local("TRALT.IS"); stale = (np.abs(np.log(d.o / d.c.shift(1))) < 1e-6).reindex(y.index).fillna(False)
for s in ["600547.SS", "1787.HK", "518880.SS"]:
    for lab, m in [("bayat", stale), ("normal", ~stale)]:
        b, t, n = nw_t(y[m], SIG[s]["cc"][m]); print(f"{s:10s} {lab:6s} r={b:+.3f} t={t:+.2f} n={n}")
print("\n== 3) Kontrollü regresyon (standartlaştırılmış, NW t) hedef TRALT intra_t ==")
gc = to_bist(loc_ret("GC=F", "c"), "zero"); gdx = to_bist(loc_ret("GDX", "adj"), "zero")
X = pd.DataFrame({"s600547": s6["cc"], "tr_gap": tr.gap, "tr_intra_l1": y.shift(1), "tr_cc_l1": tr.cc.shift(1), "xu_gap": xu.gap, "xu_intra_l1": xu.intra.shift(1), "GC_l1": gc.shift(1), "GDX_l1": gdx.shift(1)})
X = X[X.index >= "2014-01-01"]
for cols in [["s600547"], ["s600547", "tr_gap"], ["s600547", "tr_gap", "tr_intra_l1", "xu_gap", "xu_intra_l1"], ["s600547", "tr_gap", "tr_intra_l1", "xu_gap", "xu_intra_l1", "GC_l1", "GDX_l1"]]:
    res, n = ols_nw(y, X[cols]); print(f"n={n} " + " | ".join(f"{i}: {r.b:+.3f} (t {r.t:+.2f})" for i, r in res.iterrows()))
print("\n== 4) At yarışı ==")
H = pd.DataFrame({"s600547": s6["cc"], "h1787": h7["cc"], "etf518880": g8["cc"], "s601899": SIG["601899.SS"]["cc"], "tr_gap": tr.gap})
for cols in [["s600547", "etf518880"], ["s600547", "h1787"], ["s600547", "etf518880", "tr_gap"], ["s600547", "s601899", "etf518880"]]:
    res, n = ols_nw(y, H[cols]); print(f"n={n} " + " | ".join(f"{i}: {r.b:+.3f} (t {r.t:+.2f})" for i, r in res.iterrows()))
print("\n== 5) Uç değer duyarlılığı (600547 cc -> TRALT intra) ==")
df = pd.concat([s6["cc"].rename("s"), y.rename("y")], axis=1).dropna(); df = df[df.s != 0]
print("Pearson", round(df.s.corr(df.y), 4), "Spearman", round(spearmanr(df.s, df.y)[0], 4), "n", len(df))
w = df.clip(df.quantile(.01), df.quantile(.99), axis=1); print("winsor %1 r", round(w.s.corr(w.y), 4), "t", round(nw_t(w.y, w.s)[1], 2))
w = df.clip(df.quantile(.05), df.quantile(.95), axis=1); print("winsor %5 r", round(w.s.corr(w.y), 4), "t", round(nw_t(w.y, w.s)[1], 2))
r, pnl, pos = bt(s6["cc"], y, 10); a = pnl[pos != 0]
print("BT tam:", fmt(r))
srt = a.sort_values(ascending=False)
for k in [5, 10, 20]:
    rest = a.drop(srt.index[:k]); print(f"en iyi {k} işlem atılınca: ort {1e4*rest.mean():+.2f} bps, t {nw_t(rest.values)[1]:+.2f}")
print("en iyi 10 işlem:", [(str(i.date()), round(1e4*v)) for i, v in srt.head(10).items()])
for thr in [0.0, 0.005, 0.01, 0.02]:
    sig = s6["cc"].where(s6["cc"].abs() > thr, 0)
    r, _, _ = bt(sig, y, 10); print(f"|s|>{thr:.3f}: {fmt(r)}")
print("\n== 6) Yıllar (600547 cc -> TRALT intra): r, t, net10 bps ==")
r, pnl, pos = bt(s6["cc"], y, 10)
dd = pd.concat([s6["cc"].rename("s"), y.rename("y")], axis=1).dropna()
for yr, g in dd.groupby(dd.index.year):
    a = pnl[(pnl.index.year == yr) & (pos != 0)]
    print(yr, f"r={g.s.corr(g.y):+.3f} t={nw_t(g.y, g.s)[1]:+.2f} n={len(g)} net10={1e4*a.mean():+.1f}")
# tatil sonrası: 600547'nin önceki işlem günü ile arası > 4 takvim günü
d6 = daily_local("600547.SS"); gapdays = pd.Series(d6.index, index=d6.index).diff().dt.days
post = (to_bist((gapdays > 4).astype(float), "zero").reindex(y.index).fillna(0) > 0)
m = ~post.astype(bool)
b, t, n = nw_t(y[m], s6["cc"][m]); print(f"\nÇin uzun tatil sonrası günler HARİÇ: r={b:+.3f} t={t:+.2f} n={n} (atılan {int(post.sum())})")
# Dairesel kaydırma null'u
rng = np.random.default_rng(7); base = nw_t(y, s6["cc"])[1]
sv = s6["cc"].reindex(y.index).values; yv = y.values; ok = ~np.isnan(yv)
null = []
for k in rng.integers(60, len(sv) - 60, 500):
    ss = pd.Series(np.roll(sv, k), index=y.index); null.append(nw_t(y, ss)[1])
null = np.array(null); print(f"dairesel kaydırma null (500): gerçek t={base:.2f}; null |t| %95={np.nanquantile(np.abs(null), .95):.2f}, %99={np.nanquantile(np.abs(null), .99):.2f}; p={np.mean(np.abs(null) >= abs(base)):.3f}")
