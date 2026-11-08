"""Hakem: NFP 12->15 momentum (h1, h3) çürütme denemesi. python3 -W ignore adv2_nfp.py"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/a3_takvim_olay"
sys.path.insert(0, f"{S}/code")
from lib_altin import *
from scipy import stats as sst
rng = np.random.default_rng(11)
d = load_viop(); s = load_spot(); V = d.index; r = d.v_ret; SPA = s.index
nfp = pd.read_csv(f"{O}/events_us_nfp.csv", parse_dates=["date"])
bay = pd.read_csv(f"{O}/events_tr_bayram.csv", parse_dates=["arife"])
half = set(bay.arife) | set(pd.Timestamp(y, 10, 28) for y in range(2009, 2027))
isnfp = V.isin(nfp.date) & ~V.isin(list(half))
print("VİOP'ta NFP günü (yarım gün hariç):", isnfp.sum(), " yarım güne denk gelen NFP:", (V.isin(nfp.date) & V.isin(list(half))).sum())
x = np.log(d.xau_p15 / d.xau_p12)
sig = np.sign(x).where(isnfp)
ev = pd.DataFrame({"sig": sig, "x": x, "f1": d.fwd1, "f3": d.fwd3, "f5": d.fwd5}).dropna(subset=["sig"])
print("olay sayısı", len(ev), " sig=0:", (ev.sig == 0).sum(), " xau_p12 NaN:", d.xau_p12[isnfp].isna().sum())

def tsimple(z): z = pd.Series(z).dropna(); return z.mean() / z.std() * np.sqrt(len(z))
for h in ("f1", "f3"):
    p = ev.sig * ev[h]
    print(f"\n===== {h}: ort {p.mean()*1e4:.1f} bps t_basit {tsimple(p):.2f} n={p.notna().sum()} isabet {(p>0).mean():.2f}")
    for lo, hi in [(2017, 2019), (2020, 2021), (2022, 2023), (2024, 2026)]:
        m = (ev.index.year >= lo) & (ev.index.year <= hi); z = p[m]
        print(f"  {lo}-{hi}: n={m.sum()} ort={z.mean()*1e4:6.1f} t={tsimple(z):5.2f} isabet={(z>0).mean():.2f}")
    for lo, hi in [(2017, 2021), (2022, 2026)]:
        m = (ev.index.year >= lo) & (ev.index.year <= hi); z = p[m]; print(f"  {lo}-{hi}: n={m.sum()} ort={z.mean()*1e4:6.1f} t={tsimple(z):5.2f} isabet={(z>0).mean():.2f} medyan={z.median()*1e4:.1f}")
    srt = p.sort_values(ascending=False)
    for kk in (1, 3, 5):
        print(f"  en iyi {kk} hariç: ort={srt.iloc[kk:].mean()*1e4:.1f} t={tsimple(srt.iloc[kk:]):.2f}")
    po = p[ev.index > IS_END].sort_values(ascending=False)
    for kk in (1, 3, 5):
        print(f"  OOS en iyi {kk} hariç: ort={po.iloc[kk:].mean()*1e4:.1f} t={tsimple(po.iloc[kk:]):.2f}")
    print("  Wilcoxon p tam=%.3f OOS=%.3f; işaret testi OOS isabet %d/%d p=%.3f" % (sst.wilcoxon(p.dropna()).pvalue, sst.wilcoxon(p[ev.index > IS_END].dropna()).pvalue,
          int((p[ev.index > IS_END] > 0).sum()), int(p[ev.index > IS_END].notna().sum()), 1 - sst.binom.cdf(int((p[ev.index > IS_END] > 0).sum()) - 1, int(p[ev.index > IS_END].notna().sum()), 0.5)))
    # demeaned: drift çıkarıldı
    dm = ev.sig * (ev[h] - d[h.replace("f", "fwd")].mean())
    print(f"  demeaned ort {dm.mean()*1e4:.1f} t {tsimple(dm):.2f}; uzun bacak n={(ev.sig>0).sum()} ort {ev[h][ev.sig>0].mean()*1e4:.1f}; kısa bacak n={(ev.sig<0).sum()} ort(-y) {-ev[h][ev.sig<0].mean()*1e4:.1f}")
    for lo, hi in [(2017, 2021), (2022, 2026)]:
        m = (ev.index.year >= lo) & (ev.index.year <= hi)
        print(f"     {lo}-{hi}: uzun {ev[h][(ev.sig>0)&m].mean()*1e4:.1f} (n={((ev.sig>0)&m).sum()}), kısa {-ev[h][(ev.sig<0)&m].mean()*1e4:.1f} (n={((ev.sig<0)&m).sum()})")

print("\n===== h3'ün ek katkısı: gün 2-3 (fwd3 - fwd1) =====")
p23 = ev.sig * (ev.f3 - ev.f1)
for lo, hi in [(2017, 2021), (2022, 2026), (2017, 2026)]:
    m = (ev.index.year >= lo) & (ev.index.year <= hi); print(f"  {lo}-{hi}: ort {p23[m].mean()*1e4:.1f} t {tsimple(p23[m]):.2f}")

print("\n===== OOS'ta NFP etkisi diğer günlerden farklı mı? (12->15 sinyali tüm günler, etkileşim) =====")
allx = np.sign(x).where(~V.isin(list(half)))
df = pd.DataFrame({"s": allx, "y": d.fwd1, "nfp": isnfp.astype(float)}).dropna()
df["sy"] = df.s * df.y
for lo, hi in [(2017, 2021), (2022, 2026)]:
    m = (df.index.year >= lo) & (df.index.year <= hi); a = df[m]
    o = nw_ols(a.sy, a.nfp, lags=5)
    print(f"  {lo}-{hi}: NFP günleri ort {a.sy[a.nfp==1].mean()*1e4:.1f}, diğer {a.sy[a.nfp==0].mean()*1e4:.1f}, fark t(NW)={o['t']:.2f}")
# OOS'ta rastgele Cumalar: NFP olmayan Cuma kümelerinden 54'lük örneklem -> sign*fwd1 ortalaması dağılımı
fr = df[(df.index.dayofweek == 4) & (df.nfp == 0) & (df.index > IS_END)]
nn = int(((ev.index > IS_END)).sum()); obs = (ev.sig * ev.f1)[ev.index > IS_END].mean()
sims = np.array([fr.sy.sample(nn, replace=False, random_state=int(rng.integers(1e9))).mean() for _ in range(5000)])
print(f"  OOS NFP-dışı Cuma bootstrap: gözlenen {obs*1e4:.1f} bps; p(sim>=obs)={(sims>=obs).mean():.4f}; sim ort {sims.mean()*1e4:.1f} sd {sims.std()*1e4:.1f}")
alld = df[(df.nfp == 0) & (df.index > IS_END)]
sims = np.array([alld.sy.sample(nn, replace=False, random_state=int(rng.integers(1e9))).mean() for _ in range(5000)])
print(f"  OOS NFP-dışı tüm günler bootstrap: p(sim>=obs)={(sims>=obs).mean():.4f}")

print("\n===== yaz saati / yayım saati ayrımı (12:30 vs 13:30 UTC yayım) =====")
# ABD yaz saati: Mart 2. Pazar - Kasım 1. Pazar
def us_dst(t):
    y = t.year; m2 = pd.Timestamp(y, 3, 8); dst0 = m2 + pd.Timedelta(days=(6 - m2.dayofweek) % 7)
    n1 = pd.Timestamp(y, 11, 1); dst1 = n1 + pd.Timedelta(days=(6 - n1.dayofweek) % 7)
    return dst0 <= t < dst1
ev["dst"] = [us_dst(t) for t in ev.index]
for k, g in ev.groupby("dst"):
    p = g.sig * g.f1; m = g.index > IS_END
    print(f"  ABD yaz saati={k}: n={len(g)} ort={p.mean()*1e4:.1f} t={tsimple(p):.2f} | OOS n={m.sum()} ort={p[m].mean()*1e4:.1f} t={tsimple(p[m]):.2f}")

print("\n===== Good Friday / ABD tatili NFP günleri ve bayat fiyat kontrolü =====")
import holidays as _h
gf = [pd.Timestamp(k) for k, v in _h.financial_holidays("NYSE", years=range(2017, 2027)).items() if "Good Friday" in v]
gfe = ev[ev.index.isin(gf)]
print("  Good Friday'e denk gelen NFP olayları:", list(gfe.index.strftime("%Y-%m-%d")), (gfe.sig * gfe.f1 * 1e4).round(0).tolist())
p = ev.sig * ev.f1; p2 = p[~ev.index.isin(gf)]; print(f"  GF hariç ort {p2.mean()*1e4:.1f} t {tsimple(p2):.2f}")
# |x| çok küçük (bayat) olaylar
print("  |x|<2 bps olay sayısı:", (ev.x.abs() < 2e-4).sum())

print("\n===== pencere ve eşik duyarlılığı (h1, işaret) =====")
for a_, b_ in [("12", "15"), ("13", "15"), ("14", "15"), ("12", "14"), ("12", "13"), ("13", "14"), ("07", "15"), ("00", "15")]:
    xx = np.sign(np.log(d[f"xau_p{b_}"] / d[f"xau_p{a_}"])).where(isnfp)
    pp = (xx * d.fwd1).dropna(); m = pp.index > IS_END
    print(f"  {a_}->{b_}: tam ort {pp.mean()*1e4:5.1f} t {tsimple(pp):5.2f} | IS {pp[~m].mean()*1e4:5.1f} t {tsimple(pp[~m]):5.2f} | OOS {pp[m].mean()*1e4:5.1f} t {tsimple(pp[m]):5.2f}")
# eşikli: |x| > q
for qq in (0.0, 0.002, 0.004, 0.006):
    m_ = ev.x.abs() > qq; p = (ev.sig * ev.f1)[m_]; mo = p.index > IS_END
    print(f"  |x|>{qq*1e4:.0f}bps: n={m_.sum()} ort {p.mean()*1e4:.1f} t {tsimple(p):.2f} IS t {tsimple(p[~mo]):.2f} OOS t {tsimple(p[mo]):.2f}")

print("\n===== spot uzun örneklem (15:00->15:00 spot hedef) yıl blokları =====")
isn_s = SPA.isin(nfp.date)
xs = np.sign(np.log(s.xau_p15 / s.xau_p12)).where(isn_s)
for h in (1, 3):
    ps = (xs * s[f"sfwd{h}"]).dropna()
    for lo, hi in [(2010, 2013), (2014, 2016), (2017, 2019), (2020, 2021), (2022, 2023), (2024, 2026)]:
        m = (ps.index.year >= lo) & (ps.index.year <= hi); z = ps[m]
        print(f"  h{h} spot {lo}-{hi}: n={m.sum()} ort={z.mean()*1e4:6.1f} t={tsimple(z):5.2f} isabet={(z>0).mean():.2f}")
    m = ps.index.year <= 2016; print(f"  h{h} spot 2010-2016 toplam: n={m.sum()} ort={ps[m].mean()*1e4:.1f} t={tsimple(ps[m]):.2f}")
    m = ps.index.year <= 2021; print(f"  h{h} spot 2010-2021 toplam: n={m.sum()} ort={ps[m].mean()*1e4:.1f} t={tsimple(ps[m]):.2f}")
    print(f"  h{h} spot 2010-2026 toplam: n={len(ps)} ort={ps.mean()*1e4:.1f} t={tsimple(ps):.2f}")

print("\n===== uzlaşma bayatlığı/yakalama kontrolü: NFP günü log(v_settle/xau_p15) baz sapması sinyalle ilişkili mi =====")
basis = np.log(d.v_settle / d.xau_p15); bdev = basis - basis.rolling(20).median().shift(1)
bb = pd.DataFrame({"sig": ev.sig, "bdev": bdev.reindex(ev.index)}).dropna()
print("  sig*bdev ort %.1f bps t %.2f (pozitif = uzlaşma 15:00 spotun sinyal yönünde ÖTESİNDE, negatif = geride/bayat)" % ((bb.sig * bb.bdev).mean() * 1e4, tsimple(bb.sig * bb.bdev)))
print("  NFP günleri v_volume medyanı %.0f, diğer günler %.0f" % (d.v_volume[isnfp].median(), d.v_volume[~isnfp].median()))

print("\n===== maliyet =====")
pos1 = sig.fillna(0)
oos = V > IS_END
for c in (5, 10, 20):
    for h in (1, 3):
        b = backtest(pos1[oos], r[oos], h, c); bf = backtest(pos1, r, h, c); bi = backtest(pos1[~oos], r[~oos], h, c)
        print(f"  maliyet {c} bps h{h}: IS sh={bi['sharpe']:.2f} OOS sh={b['sharpe']:.2f} tam sh={bf['sharpe']:.2f}")

print("\n===== CPI karşı-kontrol (aynı sinyal) =====")
cpi = pd.read_csv(f"{O}/events_us_cpi.csv", parse_dates=["date"])
isc = V.isin(cpi.date) & ~V.isin(list(half))
pc = (np.sign(x).where(isc) * d.fwd1).dropna(); m = pc.index > IS_END
print(f"  CPI h1: tam {pc.mean()*1e4:.1f} t {tsimple(pc):.2f} | OOS {pc[m].mean()*1e4:.1f} t {tsimple(pc[m]):.2f}")
