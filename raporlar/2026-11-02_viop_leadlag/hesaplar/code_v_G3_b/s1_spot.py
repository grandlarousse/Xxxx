"""s1: Spot (Yahoo) XU030/XU100 gece & gün-içi yeniden üretim + uç değer bağımlılığı + alt dönem istikrarı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)

for sym in ["XU030.IS", "XU100.IS"]:
    d = bc.decomp(sym, start="2005-01-01")
    P(f"\n===== {sym}  bad gün (temizlenen) 2014+: {int(d.loc['2014':, 'bad'].sum())}; stale open (o==c_prev) yıl payı:")
    P((d.stale_open.groupby(d.index.year).mean().round(3)).to_dict())
    # o==h ve o==l sıklığı (açılış aşırılığı göstergesi)
    oh = (d.o >= d.h * (1 - 1e-7)).groupby(d.index.year).mean().round(3)
    ol = (d.o <= d.l * (1 + 1e-7)).groupby(d.index.year).mean().round(3)
    P("o==h payı:", oh.to_dict()); P("o==l payı:", ol.to_dict())
    x = d.loc["2014":]
    yt = bc.by_year(x, ["gap", "intra"])
    P(yt.round(2).to_string())
    P("gap>0 yıl:", int((yt.gap > 0).sum()), "/", len(yt), " intra<0 yıl:", int((yt.intra < 0).sum()), "/", len(yt))
    s = -x.intra  # aç-sat
    for nm, a, b in [("2014-2026", "2014", "2026"), ("IS 2014-2020", "2014", "2020"), ("OOS 2021-2026", "2021", "2026"),
                     ("2017-03..2026", "2017-03-06", "2026"), ("2023-12..2026-10", "2023-12-01", "2026"),
                     ("2005-2013", "2005", "2013"), ("2014-2016", "2014", "2016"), ("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026")]:
        xx = s.loc[a:b] if nm != "2005-2013" else -d.intra.loc[a:b]
        P(f"aç-sat {nm:18s}", bc.fmt(bc.st(xx)))
    lo, hi, p0 = bc.block_boot(s.loc["2014":], "Y")
    P(f"yıl-blok bootstrap 2014-2026: GA [{lo:.1f},{hi:.1f}] P<=0 {p0:.3f}")
    lo, hi, p0 = bc.block_boot(s.loc["2014":], "M")
    P(f"ay-blok bootstrap 2014-2026: GA [{lo:.1f},{hi:.1f}] P<=0 {p0:.3f}")
    # uç değer bağımlılığı
    ss = s.loc["2014":].dropna()
    srt = ss.sort_values(ascending=False)
    for k in [5, 10, 20, 50, 100]:
        P(f"en iyi {k} gün çıkarılınca: {bc.fmt(bc.st(ss.drop(srt.index[:k])))}")
    for k in [10, 50]:
        sym2 = ss.drop(srt.index[:k]).drop(srt.index[-k:])
        P(f"en iyi ve en kötü {k} gün çıkarılınca: {bc.fmt(bc.st(sym2))}")
    for q in [0.01, 0.025, 0.05]:
        w = ss.clip(ss.quantile(q), ss.quantile(1 - q))
        P(f"winsor %{q*100:.1f}: {bc.fmt(bc.st(w))}")
    # toplam katkı payları
    tot = ss.sum()
    P(f"toplam {tot*1e4:.0f} bps; en iyi 1% gün payı {srt.iloc[:int(len(ss)*0.01)].sum()/tot:.2f}; en iyi 5% {srt.iloc[:int(len(ss)*0.05)].sum()/tot:.2f}")
    # yarım yıl ve çeyrek istikrarı
    hy = ss.groupby([ss.index.year, (ss.index.month > 6)]).mean() * 1e4
    q = ss.groupby(ss.index.to_period("Q")).mean() * 1e4
    P(f"yarıyıl pozitif {int((hy>0).sum())}/{len(hy)}; çeyrek pozitif {int((q>0).sum())}/{len(q)}; ay pozitif {(ss.groupby(ss.index.to_period('M')).mean()>0).mean():.2f}")
    # yıl bırakarak (leave-one-year-out)
    loo = {y: bc.st(ss[ss.index.year != y])["mean"] for y in sorted(set(ss.index.year))}
    P("LOYO ort (bps):", {k: round(v, 1) for k, v in loo.items()})
    # kriz pencereleri
    crisis = [("2018-08-01", "2018-09-30"), ("2020-03-01", "2020-04-30"), ("2021-11-15", "2022-01-15"), ("2023-05-15", "2023-07-15"),
              ("2025-03-15", "2025-04-30"), ("2026-09-01", "2026-10-31")]
    m = pd.Series(True, index=ss.index)
    for a, b in crisis:
        m[(ss.index >= a) & (ss.index <= b)] = False
    P(f"kriz pencereleri hariç: {bc.fmt(bc.st(ss[m]))};  sadece krizler: {bc.fmt(bc.st(ss[~m]))}")
    # haftanın günü
    P("haftanın günü (aç-sat bps):", {k: round(v * 1e4, 1) for k, v in ss.groupby(ss.index.dayofweek).mean().items()})
    # ay sonu / vade günleri (VİOP vadesi: çift ayların son iş günü) etkisi
    me = ss.index.to_series().groupby(ss.index.to_period("M")).transform("max") == ss.index.to_series()
    P(f"ay son iş günü: {bc.fmt(bc.st(ss[me.values]))}; diğer: {bc.fmt(bc.st(ss[~me.values]))}")
    # gap koşullu
    g = x.gap.loc[ss.index]
    for a, b in [(-1, -0.005), (-0.005, 0), (0, 0.005), (0.005, 1)]:
        mm = (g > a) & (g <= b)
        P(f"gap ({a},{b}] n={mm.sum()}: aç-sat {bc.fmt(bc.st(ss[mm]))}")
    import statsmodels.api as sm
    X = sm.add_constant(g.values); r = sm.OLS(ss.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    P(f"aç-sat = a + b*gap: a={r.params[0]*1e4:.2f} bps (t {r.tvalues[0]:.2f}), b={r.params[1]:.3f} (t {r.tvalues[1]:.2f})")
    for a, b in [("2014", "2020"), ("2021", "2026"), ("2023", "2026")]:
        mm = (ss.index >= a) & (ss.index <= b + "-12-31")
        r = sm.OLS(ss.values[mm], sm.add_constant(g.values[mm])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        P(f"   {a}-{b}: a={r.params[0]*1e4:.2f} (t {r.tvalues[0]:.2f}) b={r.params[1]:.3f} (t {r.tvalues[1]:.2f})")
    # gap = 0 (bayat açılış) günleri
    so = x.stale_open.loc[ss.index]
    P(f"o==c_prev günleri n={int(so.sum())}: aç-sat {bc.fmt(bc.st(ss[so]))}")
    yt.to_csv(f"{bc.RES}/s1_years_{sym}.csv")
open(f"{bc.RES}/s1_spot.log", "w").write("\n".join(L))
