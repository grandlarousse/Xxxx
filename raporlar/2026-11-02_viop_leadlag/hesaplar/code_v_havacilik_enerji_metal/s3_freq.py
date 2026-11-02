"""S3: aylık/haftalık iddialar: E2 aylık USD (TUPRS~Brent), M5 aylık (EREGL~SLX/MT.AS), E5 AKSEN~aylık ort. PTF, M2/M3 rejim kırılımları."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal")
import vlib as V
RES = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_havacilik_enerji_metal/res"
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
r = {s: V.ret(s) for s in ["TUPRS.IS", "BZ=F", "XU100.IS", "TRY=X", "EEM", "ES=F", "EREGL.IS", "SLX", "MT.AS", "AKSEN.IS", "ODAS.IS", "ENJSA.IS", "TRALT.IS", "GC=F", "^STOXX"]}
M = {k: V.mo(v) for k, v in r.items()}
def mlev(sym):  # ay sonu seviye bazlı (alternatif)
    p = V.px(sym); return np.log(p.resample("ME").last()).diff()
def per3(a, b, ctrl, start):
    o = {}
    for k, (s, e) in [("tam", (start, None)), ("IS", ("2014-01-01", "2020-12-31")), ("OOS", ("2021-01-01", None))]:
        o[k] = V.pcorr(a, b, ctrl, s, e, minn=24)
    return o
def fmt(o): return " ".join(f"{k}={v[0]:.3f}(n{v[1]})" for k, v in o.items())
# ---- E2 aylık USD
tu_usd = M["TUPRS.IS"] - M["TRY=X"]; xu_usd = M["XU100.IS"] - M["TRY=X"]
P("== E2 TUPRS(USD) ~ Brent aylık (2008+). iddia pc 0,35")
P("  corr:", fmt(per3(tu_usd, M["BZ=F"], None, "2008-01-01")))
P("  pc|XU100usd:", fmt(per3(tu_usd, M["BZ=F"], [xu_usd], "2008-01-01")))
P("  pc|XU100usd+EEM+ES:", fmt(per3(tu_usd, M["BZ=F"], [xu_usd, M["EEM"], M["ES=F"]], "2008-01-01")))
P("  pc|XU100 TL + USDTRY (TL hisse):", fmt(per3(M["TUPRS.IS"], M["BZ=F"], [M["XU100.IS"], M["TRY=X"]], "2008-01-01")))
lv = (mlev("TUPRS.IS") - mlev("TRY=X")); P("  seviye bazlı (ay sonu) pc|XU100usd:", fmt(per3(lv, mlev("BZ=F"), [mlev("XU100.IS") - mlev("TRY=X")], "2008-01-01")))
x = pd.concat([tu_usd.rename("a"), M["BZ=F"].rename("b"), xu_usd.rename("c")], axis=1).dropna(); x = x[x.index >= "2008"]
P(f"  Spearman ham={x.a.corr(x.b, method='spearman'):.3f}; 2026 hariç pc={V.pcorr(x.a[x.index<'2026'], x.b[x.index<'2026'], [x.c[x.index<'2026']])[0]:.3f}")
# ---- M5 aylık EREGL ~ SLX / MT.AS (TL, 2008+, XU100 TL kontrol)
for d in ["SLX", "MT.AS"]:
    P(f"== M5 EREGL ~ {d} aylık (TL, 2008+). iddia pc 0,41")
    P("  corr:", fmt(per3(M["EREGL.IS"], M[d], None, "2008-01-01")))
    P("  pc|XU100:", fmt(per3(M["EREGL.IS"], M[d], [M["XU100.IS"]], "2008-01-01")))
    P("  pc|XU100+USDTRY+EEM:", fmt(per3(M["EREGL.IS"], M[d], [M["XU100.IS"], M["TRY=X"], M["EEM"]], "2008-01-01")))
    reg = M["^STOXX"] if d == "MT.AS" else M["ES=F"]
    P("  pc|XU100+USDTRY+EEM+bölge:", fmt(per3(M["EREGL.IS"], M[d], [M["XU100.IS"], M["TRY=X"], M["EEM"], reg], "2008-01-01")))
    x = pd.concat([M["EREGL.IS"].rename("a"), M[d].rename("b"), M["XU100.IS"].rename("c")], axis=1).dropna(); x = x[x.index >= "2008"]
    yy = x.groupby(x.index.year).apply(lambda g: V.pcorr(g.a, g.b, [g.c], minn=10)[0]).dropna()
    P(f"  yıllık aylık pc>0: {(yy>0).sum()}/{len(yy)}; 2008-09 hariç pc={V.pcorr(x.a[x.index>='2010'], x.b[x.index>='2010'], [x.c[x.index>='2010']])[0]:.3f}; son 36 ay pc={V.pcorr(x.a[-36:], x.b[-36:], [x.c[-36:]], minn=24)[0]:.3f}")
# ---- E5 AKSEN ~ PTF
ptf = pd.read_parquet("/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_enerji/ptf_daily.parquet")
ptf.index = pd.DatetimeIndex(ptf.index).tz_localize(None).normalize() if getattr(ptf.index, "tz", None) else pd.DatetimeIndex(ptf.index).normalize()
P(f"== E5 PTF verisi: {ptf.index[0].date()}..{ptf.index[-1].date()}, 2018 TL ort={ptf.tl[ptf.index.year==2018].mean():.2f} (EPİAŞ yıllık bülten 231,64)")
fx = V.px("TRY=X", on_cal=False)  # UTC günü sonu kur
fxd = fx.reindex(ptf.index, method="ffill")
ptf_usd_d = ptf.tl / fxd
cnt = ptf.tl.resample("ME").count()
pm_tl = np.log(ptf.tl.resample("ME").mean()).diff(); pm_usd = np.log(ptf_usd_d.resample("ME").mean()).diff()
pm_tl[cnt < 25] = np.nan; pm_usd[cnt < 25] = np.nan
P(f"  benim USD serim ile ajanın 'usd' sütunu aylık değişim corr={pm_usd.corr(np.log(ptf.usd.resample('ME').mean()).diff()):.4f}")
# mevsimsellikten arındırılmış (takvim ayı ortalaması çıkarılmış; IS ortalaması ile)
def deseason(s):
    isp = s[(s.index >= "2014") & (s.index < "2021")]; mu = isp.groupby(isp.index.month).mean()
    return s - mu.reindex(s.index.month).values
for stk in ["AKSEN.IS", "ODAS.IS", "ENJSA.IS"]:
    a_usd = M[stk] - M["TRY=X"]
    P(f"-- {stk} (2014+) iddia AKSEN USD pc 0,26 (IS 0,28/OOS 0,24); TL+USDTRY 0,24")
    P("  USD corr:", fmt(per3(a_usd, pm_usd, None, "2014-01-01")))
    P("  USD pc|XU100usd:", fmt(per3(a_usd, pm_usd, [xu_usd], "2014-01-01")))
    P("  USD pc|XU100usd+EEM:", fmt(per3(a_usd, pm_usd, [xu_usd, M["EEM"]], "2014-01-01")))
    P("  TL pc|XU100+USDTRY:", fmt(per3(M[stk], pm_tl, [M["XU100.IS"], M["TRY=X"]], "2014-01-01")))
    P("  TL pc|XU100+USDTRY+EEM:", fmt(per3(M[stk], pm_tl, [M["XU100.IS"], M["TRY=X"], M["EEM"]], "2014-01-01")))
    P("  USD pc|XU100usd, PTF mevsimsellikten arındırılmış:", fmt(per3(a_usd, deseason(pm_usd), [xu_usd], "2014-01-01")))
    P("  PTF(m-1) -> hisse(m) pc|XU100usd:", fmt(per3(a_usd, pm_usd.shift(1), [xu_usd], "2014-01-01")))
    P("  hisse(m-1) -> PTF(m) pc|XU100usd:", fmt(per3(a_usd.shift(1), pm_usd, [xu_usd.shift(1)], "2014-01-01")))
    x = pd.concat([a_usd.rename("a"), pm_usd.rename("b"), xu_usd.rename("c")], axis=1).dropna(); x = x[x.index >= "2014"]
    yy = x.groupby(x.index.year).apply(lambda g: V.pcorr(g.a, g.b, [g.c], minn=9)[0]).dropna()
    ex = x[(x.index < "2021-07") | (x.index >= "2023-01")]
    P(f"  yıllık pc>0: {(yy>0).sum()}/{len(yy)} {yy.round(2).to_dict()}")
    P(f"  Spearman kısmi (rank)={V.pcorr(x.a.rank(), x.b.rank(), [x.c.rank()])[0]:.3f}; 2021H2-2022 hariç pc={V.pcorr(ex.a, ex.b, [ex.c])[0]:.3f}; |b| en büyük 5 ay hariç pc={V.pcorr(x.a.drop(x.b.abs().nlargest(5).index), x.b.drop(x.b.abs().nlargest(5).index), [x.c.drop(x.b.abs().nlargest(5).index)])[0]:.3f}")
    if stk == "AKSEN.IS":
        # rastgele kaydırma null'ı: PTF serisini dairesel kaydır
        rng = np.random.default_rng(0); vals = []
        b = x.b.values
        for k in range(1, len(b) - 1):
            bb = np.roll(b, k); vals.append(V.pcorr(x.a, pd.Series(bb, index=x.index), [x.c])[0])
        vals = np.array(vals); obs = V.pcorr(x.a, x.b, [x.c])[0]
        P(f"  dairesel kaydırma null (n={len(vals)}): obs={obs:.3f}, null 95%={np.quantile(np.abs(vals), .95):.3f}, p={np.mean(np.abs(vals) >= abs(obs)):.3f}")
# ---- M2 / M3 rejim: TRALT~GC=F günlük kısmi yarıyıllık
P("== M2 TRALT~GC=F günlük pc|XU100 ve pc|XU100+USDTRY, yarıyıl")
x = pd.concat([r["TRALT.IS"].rename("a"), r["GC=F"].rename("b"), r["XU100.IS"].rename("c"), r["TRY=X"].rename("f")], axis=1).dropna(); x = x[x.index >= "2019"]
g = x.groupby([x.index.year, (x.index.month - 1) // 6])
P(g.apply(lambda d: pd.Series({"pc": V.pcorr(d.a, d.b, [d.c])[0], "pc_fx": V.pcorr(d.a, d.b, [d.c, d.f])[0], "n": len(d)})).round(3).to_string())
# Haftalık USD bazlı TRALT~GC=F yıllık (iddia 2023 −0,11 / 2026 0,49)
W = {k: V.wk(v) for k, v in {"a": r["TRALT.IS"], "au": r["TRALT.IS"] - r["TRY=X"], "b": r["GC=F"], "c": r["XU100.IS"], "cu": r["XU100.IS"] - r["TRY=X"]}.items()}
for lab, a, c in [("TL", W["a"], W["c"]), ("USD", W["au"], W["cu"])]:
    yy = V.byyear(a, W["b"], [c], minn=30, start="2019-01-01"); P(f"  haftalık {lab} pc yıllık: {yy.round(2).to_dict()}")
open(f"{RES}/s3_freq.txt", "w").write("\n".join(out))
