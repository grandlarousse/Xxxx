"""Ek saldırılar: dönem içi plasebo, uzun trend kontrolü, SPY terimi, taze sinyal dönem dönem, oran biçimi ızgarası, beklenti aralığı, roll maliyeti."""
import numpy as np, pandas as pd, statsmodels.api as sm
from adv_lib import *
rng = np.random.default_rng(23)
R = us_returns(); e, B = rolling_resid(R); pv = viop(); r = pv.v_ret; bh = (np.exp(r) - 1).iloc[1:]
E10 = e.rolling(10).sum(); thr = E10[:"2017-12-31"].dropna().quantile(.8)
x, _ = map_us_to_viop(E10, pv.index); sig = (x > thr).astype(float)
def M(ser): return map_us_to_viop(ser, pv.index)[0]
# 1) dönem içi plasebo (yıl içi kaydırma) — 2025–26 ve 2017–2024 ayrı
sv = sig.values; yrs = pv.index.year.values
def within_year():
    out = sv.copy()
    for y in np.unique(yrs):
        m = np.where(yrs == y)[0]; out[m] = np.roll(sv[m], rng.integers(0, len(m)))
    return out
def st(s, a, b, H=3, c=5):
    pos = position(pd.Series(s, index=pv.index), H); p = pnl(pos, r, c)[a:b]; t = trades(pos[a:b], r[a:b], c); tc = t[~t.open_]
    return sharpe(p), tc.ret.mean() * 100, p.mean() * 252 * 100
print("=== YIL İÇİ plasebo (1000 sim), dönem dönem ===")
sims = [within_year() for _ in range(1000)]
for per, a, b in [("2017-03..2024", None, "2024"), ("2018..2024", "2018", "2024"), ("2022..2024", "2022", "2024"), ("2025..2026", "2025", None), ("2025", "2025", "2025"), ("2026", "2026", None), ("2017-03..2021", None, "2021")]:
    o = st(sv, a, b); S_ = np.array([st(s, a, b) for s in sims])
    print(f"  {per:14s} kural: Sharpe {o[0]:.2f} ort işlem %{o[1]:.2f} yıllık %{o[2]:.1f} | plasebo medyan Sharpe {np.median(S_[:,0]):.2f}, ort işlem %{np.nanmedian(S_[:,1]):.2f} | yüzdelik: Sharpe %{(S_[:,0]<o[0]).mean()*100:.1f}, ort işlem %{(S_[:,1]<o[1]).mean()*100:.1f}")
# 2) uzun trend kontrolü
C = pd.DataFrame(index=pv.index)
C["V60"] = r.rolling(60).sum(); C["V120"] = r.rolling(120).sum(); C["ma50"] = (np.log(pv.v_settle) - np.log(pv.v_settle).rolling(50).mean())
C["GDX60"] = M(R.GDX.rolling(60).sum()); C["vol20"] = r.rolling(20).std(); C["x60"] = M(e.rolling(60).sum())
print("\n=== uzun trend / rejim kontrolleri ile (h3, h5; tam ve 2018+) ===")
for cols in (["V60"], ["V60", "V120", "ma50"], ["GDX60"], ["x60"], ["V60", "ma50", "GDX60", "vol20"]):
    o = []
    for a in (None, "2018"):
        for h in (3, 5):
            d = pd.concat([fwd(r, h).rename("y"), sig.rename("sig"), C[cols]], axis=1)[a:].dropna(); Z = (d[cols] - d[cols].mean()) / d[cols].std()
            m = sm.OLS(d.y, sm.add_constant(pd.concat([d[["sig"]], Z], axis=1))).fit(cov_type="HAC", cov_kwds={"maxlags": 10}); o.append(f"{'tam' if a is None else '18+'} h{h} b {m.params['sig']*100:+.3f} t {m.tvalues['sig']:.2f}")
    print(f"  {'+'.join(cols):24s} " + " | ".join(o))
print("  sinyal ile korelasyon:", C.corrwith(sig).round(2).to_dict())
tr_up = (C.ma50 > 0)
for nm, m in [("fiyat > 50g ort.", tr_up), ("fiyat <= 50g ort.", ~tr_up & C.ma50.notna())]:
    q3 = nw_diff(fwd(r, 3)[m], sig[m], 10); q5 = nw_diff(fwd(r, 5)[m], sig[m], 10)
    print(f"  {nm:18s} sinyal n {q3['n1']}/{q3['N']}: h3 sinyal ort {q3['m1']:+.3f} diğer {q3['m0']:+.3f} (t {q3['t']:.2f}) | h5 {q5['m1']:+.3f} / {q5['m0']:+.3f} (t {q5['t']:.2f})")
# 3) SPY terimi: sinyal yalnız SPY terimi yüzünden mi?
e_ns, _ = rolling_resid(R, xs=("GLD",)); xn, _ = map_us_to_viop(e_ns.rolling(10).sum(), pv.index); thn = e_ns.rolling(10).sum()[:"2017-12-31"].dropna().quantile(.8); sn = (xn > thn).astype(float)
spy_part = M((-(B.SPY * R.SPY)).rolling(10).sum())
f3 = fwd(r, 3) * 100; f5 = fwd(r, 5) * 100
print("\n=== SPY terimi ===")
for nm, m in [("V0=1 & SPY'siz=1", (sig > 0) & (sn > 0)), ("V0=1 & SPY'siz=0 (yalnız SPY terimi sayesinde)", (sig > 0) & (sn == 0)), ("V0=0 & SPY'siz=1", (sig == 0) & (sn > 0)), ("ikisi de 0", (sig == 0) & (sn == 0))]:
    print(f"  {nm:48s} n {int(m.sum()):4d} h3 {f3[m].mean():+.3f} h5 {f5[m].mean():+.3f}")
d = pd.DataFrame({"s": sig, "sp": spy_part, "f3": f3, "f5": f5}).dropna()
print("  sinyal günlerinde SPY teriminin (−b·SPY10) x içindeki payı: medyan %", round((d.sp[d.s > 0] * 100).median(), 2), "| sinyal & SPY10 düşmüş (terim>0):", int(((d.s > 0) & (d.sp > 0)).sum()), "h3", round(d.f3[(d.s > 0) & (d.sp > 0)].mean(), 3), "| sinyal & SPY10 yükselmiş:", int(((d.s > 0) & (d.sp <= 0)).sum()), "h3", round(d.f3[(d.s > 0) & (d.sp <= 0)].mean(), 3))
# 4) taze sinyal, tam 3 gün (uzatmasız) — dönem dönem
age = sig.groupby((sig == 0).cumsum()).cumsum(); fresh = (age == 1).astype(float)
print("\n=== yalnız TAZE sinyal (ilk gün), tam 3/5 gün tut — dönem dönem ===")
for per, a, b in [("tam", None, None), ("2017-21", None, "2021"), ("2018-24", "2018", "2024"), ("2022-24", "2022", "2024"), ("2025-26", "2025", None)]:
    q3 = nw_diff(fwd(r, 3)[a:b], fresh[a:b], 5); q5 = nw_diff(fwd(r, 5)[a:b], fresh[a:b], 5)
    print(f"  {per:8s} n {q3['n1']:3d}: h3 ort {q3['m1']:+.3f} (diğer {q3['m0']:+.3f}, t {q3['t']:.2f}) | h5 ort {q5['m1']:+.3f} (diğer {q5['m0']:+.3f}, t {q5['t']:.2f})")
# 5) oran biçimi (ln GDX/GLD 10g) ızgarası
print("\n=== ORAN BİÇİMİ ln(GDX/GLD) k-gün değişimi: fark NW t, 2018–2026 (h3 | h5) ve sade işlem alfa t (H=3,5bps; tam) ===")
rows = {}
for k in (5, 8, 10, 12, 15, 20):
    ser = (R.GDX - R.GLD).rolling(k).sum(); xv, _ = map_us_to_viop(ser, pv.index); d = {}
    for q in (.6, .7, .8, .9):
        th = ser[:"2017-12-31"].dropna().quantile(q); s = (xv > th).astype(float)
        p = pnl(position(s, 3), r, 5)
        d[f"q{int(q*100)}"] = f"{nw_diff(fwd(r,3)['2018':], s['2018':], 10)['t']:.1f}|{nw_diff(fwd(r,5)['2018':], s['2018':], 10)['t']:.1f}|a{alpha(p, bh)[1]:.1f}|18-24:{nw_diff(fwd(r,5)['2018':'2024'], s['2018':'2024'], 10)['t']:.1f}"
    rows[f"k{k}"] = d
print(pd.DataFrame(rows).T.to_string())
ser = (R.GDX - R.GLD).rolling(10).sum(); print("  oran biçimi eşikleri (2018 öncesi kantiller) %:", {q: round(ser[:'2017-12-31'].dropna().quantile(q) * 100, 2) for q in (.6, .7, .8, .9)})
# 6) işlem ortalaması için bootstrap aralığı ve dönemsel beklenti
pos = position(sig, 3); t = trades(pos, r, 5); tc = t[~t.open_].copy(); tc["y"] = tc.entry.dt.year
def boot(v, n=5000): 
    v = np.asarray(v); m = np.array([rng.choice(v, len(v)).mean() for _ in range(n)]); return np.percentile(m, [5, 50, 95])
print("\n=== işlem başına net getiri (5 bps) bootstrap %5/%50/%95 ===")
for nm, m in [("tüm 85", tc.y > 0), ("2017–2024 (65)", tc.y <= 2024), ("2018–2024 (59)", (tc.y >= 2018) & (tc.y <= 2024)), ("2025–2026 (20)", tc.y >= 2025)]:
    print(f"  {nm:16s} ort %{tc.ret[m].mean()*100:.2f}  aralık {np.round(boot(tc.ret[m].values)*100, 2).tolist()}  kazanan %{(tc.ret[m]>0).mean()*100:.0f}  std %{tc.ret[m].std()*100:.2f}")
# rastgele giriş kıyası aynı süre dağılımıyla: işlem ort beklenen (drift) = piyasada geçen gün × günlük ort
print("  kıyas: aynı sürelerle rastgele girişin beklenen ort getirisi ≈ %", round(tc.days.mean() * r.mean() * 100, 2), "(tam dönem drift) | 2018–24 drift ile ≈ %", round(tc.days[(tc.y >= 2018) & (tc.y <= 2024)].mean() * r['2018':'2024'].mean() * 100, 2))
# 7) roll ek maliyeti
tr_roll = 0
for _, q in tc.iterrows():
    i = pv.index.get_loc(q.entry); j = pv.index.get_loc(q.exit); tr_roll += int((pv.v_code.iloc[i + 1:j + 1].values != pv.v_code.iloc[i:j].values).sum())
print(f"\nroll: 85 işlemde {tr_roll} roll → gidiş-dönüş sayısı fiilen {85 + tr_roll} (maliyet ×{(85 + tr_roll)/85:.2f})")
for c in (5, 10, 22):
    eff = c * (85 + tr_roll) / 85; p = pnl(pos, r, eff); al = alpha(p, bh)
    print(f"  {c} bps (+roll → {eff:.1f}): Sharpe {sharpe(p):.2f}, alfa %{al[0]:.1f} (t {al[1]:.2f}), 2018+ Sharpe {sharpe(p['2018':]):.2f}, 2018–24 Sharpe {sharpe(p['2018':'2024']):.2f}")
# 8) H=1..10 tam örneklem kısa özet + 1 günlük ufuk
print("\n=== H duyarlılığı (tam, 5 bps): Sharpe | alfa t | ort işlem | işlem sayısı | ort süre ===")
for H in (1, 2, 3, 4, 5, 7, 10):
    ps = position(sig, H); p = pnl(ps, r, 5); tt = trades(ps, r, 5); tt = tt[~tt.open_]
    print(f"  H={H:2d}: {sharpe(p):.2f} | {alpha(p, bh)[1]:.2f} | %{tt.ret.mean()*100:.2f} | {len(tt)} | {tt.days.mean():.1f} gün | 2018–24 Sharpe {sharpe(p['2018':'2024']):.2f}")
