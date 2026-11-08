"""Hakem: QEND_TDE1_h3 çürütme denemesi. python3 -W ignore adv1_qend.py"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *
rng = np.random.default_rng(7)
d = load_viop(); s = load_spot(); V = d.index; r = d.v_ret
def cal_pos(idx):
    g = pd.Series(np.arange(len(idx)), index=idx).groupby([idx.year, idx.month]); tdm = g.cumcount() + 1; n = g.transform("size"); return tdm.values, (n - tdm).values
tdm, tde = cal_pos(V)
qm = np.isin(V.month, [3, 6, 9, 12])
D = pd.Series((qm & (tde == 1)).astype(float), index=V)
y = d.fwd3
ev = y[D == 1]; ne = y[D == 0]
print("n_ev", len(ev), "ev mean %.1f non %.1f diff %.1f" % (ev.mean()*1e4, ne.mean()*1e4, (ev.mean()-ne.mean())*1e4))
o = ic(D, y, 5, "pearson"); print("NW t", round(o["t"], 2))
# basit olay t (olaylar 3 ay arayla, örtüşme yok): (ev - ne.mean) / sd * sqrt(n)
ex = ev - ne.mean(); print("basit olay t %.2f, medyan %.1f bps, isabet %.2f, binom p(>=k)" % (ex.mean()/ex.std()*np.sqrt(len(ex)), ev.median()*1e4, (ev>0).mean()))
from scipy import stats as sst
k = int((ev > 0).sum()); print("  pozitif olay %d/%d, binom tek yön p=%.3f; (ev>non mean) %d/%d p=%.3f" % (k, len(ev), 1-sst.binom.cdf(k-1, len(ev), 0.5), int((ex>0).sum()), len(ex), 1-sst.binom.cdf(int((ex>0).sum())-1, len(ex), 0.5)))
print("  Wilcoxon (ev - non mean) p=%.3f" % sst.wilcoxon(ex).pvalue)

print("\n--- alt dönemler ---")
for lo, hi in [("2017", "2019"), ("2020", "2021"), ("2022", "2023"), ("2024", "2026")]:
    m = (V.year >= int(lo)) & (V.year <= int(hi)); e = y[(D == 1) & m]; n_ = y[(D == 0) & m]
    xx = e - n_.mean()
    print(f"{lo}-{hi}: n={len(e)} ev={e.mean()*1e4:6.1f} non={n_.mean()*1e4:5.1f} diff={xx.mean()*1e4:6.1f} t_basit={xx.mean()/xx.std()*np.sqrt(len(xx)):.2f} isabet={(e>0).mean():.2f}")

print("\n--- yerel drift düzeltmesi ---")
# (a) geçmiş 63 gün ortalama v_ret * 3 (ex-ante drift), (b) ±63 gün merkezli (olay penceresi hariç) ortalama fwd3
past = r.rolling(63).mean().shift(0) * 3  # gün t'ye kadar (t dahil) bilinen
cen = []
pos = np.where(D.values == 1)[0]
for p in pos:
    w = list(range(max(0, p-63), max(0, p-3))) + list(range(min(len(V), p+4), min(len(V)-3, p+67)))
    cen.append(y.iloc[w].mean())
cen = pd.Series(cen, index=V[pos])
for lab, base in [("geçmiş63", past.iloc[pos].values), ("merkez±63", cen.values)]:
    xx = ev.values - base
    print(f"{lab}: excess ort={xx.mean()*1e4:.1f} bps t_basit={xx.mean()/xx.std()*np.sqrt(len(xx)):.2f} medyan={np.median(xx)*1e4:.1f}")
    for lo, hi in [(2017, 2021), (2022, 2026)]:
        m = (V[pos].year >= lo) & (V[pos].year <= hi); z = xx[m]
        print(f"     {lo}-{hi}: {z.mean()*1e4:.1f} t={z.mean()/z.std()*np.sqrt(len(z)):.2f} n={len(z)}")

print("\n--- spot ile aynı pencere (VİOP olay tarihleri, spot 15:00->15:00, t+3 VİOP günü) ---")
sp = d.xau_p15
spot3 = np.log(sp.shift(-3) / sp)
print("spot fwd3 olay ort %.1f, VİOP fwd3 %.1f, korelasyon %.3f" % (spot3[D==1].mean()*1e4, ev.mean()*1e4, spot3[D==1].corr(ev)))
# kapsanan spot iş günü sayısı (bayram/yılbaşı uzaması)
SPA = s.index
nspan = []
for p in pos:
    if p + 3 < len(V):
        nspan.append(((SPA > V[p]) & (SPA <= V[p+3])).sum())
    else: nspan.append(np.nan)
nspan = pd.Series(nspan, index=V[pos])
print("kapsanan spot gün sayısı dağılımı:", nspan.value_counts().to_dict())
pd_ = ev / nspan * 3
print("spot-gün başına normalize (x3) olay ort %.1f" % (pd_.mean()*1e4))
long = nspan > 3; print("uzun pencere (>3 spot gün) olaylar:", list(zip(V[pos][long.values].strftime('%Y-%m-%d'), (ev[long.values]*1e4).round(0))))
print("yalnız 3 spot günlük pencereler: n=%d ort=%.1f" % ((~long).sum(), ev[(~long).values].mean()*1e4))

print("\n--- ay bazında ---")
for mm in (3, 6, 9, 12):
    e = ev[ev.index.month == mm]; print(mm, "n", len(e), "ort %.1f medyan %.1f pozitif %d/%d" % (e.mean()*1e4, e.median()*1e4, (e>0).sum(), len(e)))
e2 = ev[ev.index.month != 12]; xx = e2 - ne.mean(); print("Aralık hariç: n=%d ort=%.1f t_basit=%.2f; IS ort %.1f OOS ort %.1f" % (len(e2), xx.mean()*1e4, xx.mean()/xx.std()*np.sqrt(len(xx)), e2[e2.index<=IS_END].mean()*1e4, e2[e2.index>IS_END].mean()*1e4))
e3 = ev[ev.index.year < 2025]; xx = e3 - ne[ne.index.year < 2025].mean(); print("2025-26 hariç: n=%d diff=%.1f t_basit=%.2f" % (len(e3), xx.mean()*1e4, xx.mean()/xx.std()*np.sqrt(len(xx))))
e4 = ev[(ev.index.year < 2025) & (ev.index.month != 12)]; xx = e4 - ne[ne.index.year < 2025].mean(); print("2025-26 ve Aralık hariç: n=%d diff=%.1f t_basit=%.2f" % (len(e4), xx.mean()*1e4, xx.mean()/xx.std()*np.sqrt(len(xx))))
srt = (ev - ne.mean()).sort_values(ascending=False)
for kk in (1, 3, 5):
    z = srt.iloc[kk:]; print(f"en iyi {kk} olay hariç: ort={z.mean()*1e4:.1f} t_basit={z.mean()/z.std()*np.sqrt(len(z)):.2f}")
# leave-one-year-out
lo_ = {}
for yy in sorted(set(ev.index.year)):
    z = (ev - ne.mean())[ev.index.year != yy]; lo_[yy] = round(z.mean()/z.std()*np.sqrt(len(z)), 2)
print("yıl-dışla t:", lo_)

print("\n--- çeyrek döngüsünde konum taraması (TDE1 olayını k gün kaydır), h=3 ---")
res = []
for kk in range(-45, 46):
    Dk = D.shift(kk).fillna(0)
    o = ic(Dk, y, 5, "pearson"); e = y[Dk == 1]; res.append((kk, round((e.mean() - y[Dk == 0].mean())*1e4, 1), round(o["t"], 2)))
R = pd.DataFrame(res, columns=["k", "diff", "t"])
print(R.to_string(index=False))
far = R[(R.k.abs() > 5)]
print("|k|>5 için |t|>=2 oranı: %.2f, t>=3.08: %d / %d, t ortalaması %.2f, sd %.2f" % ((far.t.abs() >= 2).mean(), (far.t >= 3.08).sum(), len(far), far.t.mean(), far.t.std()))

print("\n--- Monte Carlo: her çeyrekte rastgele 1 gün (aynı zaman dağılımı, drift rejimi korunur) ---")
q = pd.PeriodIndex(V, freq="Q")
grp = pd.Series(np.arange(len(V)), index=V).groupby(q)
groups = [g.values for _, g in grp if len(g) > 20]
yv = y.values; ok = np.isfinite(yv)
obs = ev.mean() - ne.mean()
sims = np.empty(20000)
for i in range(len(sims)):
    pp = np.array([rng.choice(gg[:-3]) for gg in groups])
    m = np.zeros(len(V), bool); m[pp] = True
    sims[i] = np.nanmean(yv[m & ok]) - np.nanmean(yv[~m & ok])
print("gözlenen fark %.1f bps; MC p(tek yön)=%.4f; MC p(iki yön |.|)=%.4f; sim ort %.1f sd %.1f" % (obs*1e4, (sims >= obs).mean(), (np.abs(sims) >= abs(obs)).mean(), sims.mean()*1e4, sims.std()*1e4))

print("\n--- ay içi tüm konumlar (çeyrek ayları vs diğer), h=1,3,5: kaç kombinasyon t>=3.08 ---")
rows = []
for grpname, mk in [("Q", qm), ("nonQ", ~qm), ("all", np.ones(len(V), bool))]:
    for lab, arr in [("tde", tde), ("tdm", tdm)]:
        for kpos in range(0, 8):
            if lab == "tdm" and kpos == 0: continue
            for h in (1, 3, 5):
                Dk = pd.Series((mk & (arr == kpos)).astype(float), index=V)
                o = ic(Dk, d[f"fwd{h}"], max(h, 5), "pearson"); rows.append((grpname, f"{lab}{kpos}", h, round(o["t"], 2)))
RR = pd.DataFrame(rows, columns=["grp", "pos", "h", "t"])
print(RR.pivot_table(index=["grp", "pos"], columns="h", values="t").to_string())
print("Q grubu kombinasyon sayısı", (RR.grp == "Q").sum(), " |t|>=2:", ((RR.grp == "Q") & (RR.t.abs() >= 2)).sum(), " t>=3:", ((RR.grp == "Q") & (RR.t >= 3)).sum())

print("\n--- spot bağımsız erken dönem 2010-2016 (tam spot takvimi; Mart-2017 kısmi ay hatası yok) ---")
tdm_s, tde_s = cal_pos(SPA); qs = np.isin(SPA.month, [3, 6, 9, 12])
Ds = pd.Series((qs & (tde_s == 1)).astype(float), index=SPA)
for lo, hi in [(2010, 2012), (2013, 2016), (2010, 2016)]:
    m = (SPA.year >= lo) & (SPA.year <= hi); e = s.sfwd3[(Ds == 1) & m]; n_ = s.sfwd3[(Ds == 0) & m]; xx = e - n_.mean()
    o = ic(Ds[m], s.sfwd3[m], 5, "pearson")
    print(f"spot {lo}-{hi}: n={len(e)} diff={xx.mean()*1e4:.1f} t_NW={o['t']:.2f} t_basit={xx.mean()/xx.std()*np.sqrt(len(xx)):.2f} isabet={(e>0).mean():.2f}")
# erken dönem Aralık hariç
m = (SPA.year <= 2016); e = s.sfwd3[(Ds == 1) & m & (SPA.month != 12)]; xx = e - s.sfwd3[(Ds == 0) & m].mean()
print(f"spot 2010-2016 Aralık hariç: n={len(e)} diff={xx.mean()*1e4:.1f} t_basit={xx.mean()/xx.std()*np.sqrt(len(xx)):.2f}")
e = s.sfwd3[(Ds == 1) & m & (SPA.month == 12)]; print("spot 2010-2016 yalnız Aralık:", (e*1e4).round(0).to_dict())
# erken dönem komşu konum taraması
res = []
for kk in range(-45, 46):
    Dk = Ds.shift(kk).fillna(0); mm_ = SPA.year <= 2016
    o = ic(Dk[mm_], s.sfwd3[mm_], 5, "pearson"); res.append((kk, round(o["t"], 2)))
Re = pd.DataFrame(res, columns=["k", "t"]); print("erken spot konum taraması, k=-3..3:", Re[Re.k.abs() <= 3].set_index("k").t.to_dict(), " |k|>5 |t|>=1.5 oranı %.2f" % (Re[Re.k.abs() > 5].t.abs() >= 1.5).mean())

print("\n--- maliyet ve backtest ---")
oos = V > IS_END
for c in (5, 10, 20):
    b = backtest(D[oos], r[oos], 3, c); bf = backtest(D, r, 3, c); bd = backtest(D[oos], r[oos], 3, c, demean=True)
    print(f"maliyet {c} bps: OOS sh={b['sharpe']:.2f} dm={bd['sharpe']:.2f} tam sh={bf['sharpe']:.2f}")
# drift-nötr: olaylarda uzun + aynı gün t'de 'her zaman uzun' karşı pozisyon (excess) -> ev - ortalama
print("olay başına net (10 bps) ort %.1f bps; drift(non mean) sonrası %.1f bps" % ((ev.mean()*1e4 - 10), (ev.mean()-ne.mean())*1e4 - 10))

print("\n--- dolar/diğer varlık penceresi ---")
for c in ["dk_EURUSD_p15", "dk_DOLLARIDXUSD_p15", "dk_USA500IDXUSD_p15", "dk_XAGUSD_p15", "dk_USTBONDTRUSD_p15"]:
    if c in d.columns:
        px = d[c]; f3 = np.log(px.shift(-3) / px); e = f3[D == 1]; n_ = f3[D == 0]
        xx = (e - n_.mean()).dropna(); print(f"{c}: diff={xx.mean()*1e4:.1f} t_basit={xx.mean()/xx.std()*np.sqrt(len(xx)):.2f} n={len(xx)}")
# altın/gümüş oranı ve altın-S&P farkı
print("\n--- VİOP takvim bütünlüğü: çeyrek aylarında işlem günü sayısı ---")
cnt = pd.Series(1, index=V).groupby([V.year, V.month]).size()
qq = cnt[[m in (3, 6, 9, 12) for _, m in cnt.index]]
print(qq.to_dict())
