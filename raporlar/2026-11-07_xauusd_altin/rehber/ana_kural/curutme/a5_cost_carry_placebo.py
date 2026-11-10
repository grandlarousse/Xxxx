"""(5) maliyet, taşıma (carry), plasebo ; taze/eski sinyal ; süre dağılımı."""
import numpy as np, pandas as pd
from adv_lib import *
rng = np.random.default_rng(11)
R = us_returns(); e, B = rolling_resid(R); pv = viop(); r = pv.v_ret
E10 = e.rolling(10).sum(); thr = E10[:"2017-12-31"].dropna().quantile(.8)
x, _ = map_us_to_viop(E10, pv.index); sig = (x > thr).astype(float)
bh = (np.exp(r) - 1).iloc[1:]
# ---- taşıma: spot 15:00 UTC getirisi − vadeli getirisi
sp = np.log(pv.xau_p15); s_ret = sp.diff()
carry = (s_ret - r)
print("xau_p15 eksik gün:", int(pv.xau_p15.isna().sum()))
print("TAŞIMA (spot getirisi − vadeli getirisi), yıllık %:", round(carry.mean() * 252 * 100, 2), "| yıl yıl:", (carry.groupby(carry.index.year).mean() * 252 * 100).round(1).to_dict())
basis = np.log(pv.v_settle / pv.xau_p15); ann = basis / (pv.v_dte.clip(lower=1) / 365) * 100
print("uzlaşma/spot primi yıllıklandırılmış medyan % (dte>20):", ann[pv.v_dte > 20].groupby(ann[pv.v_dte > 20].index.year).median().round(1).to_dict())
sbh = (np.exp(s_ret) - 1).iloc[1:]
print(f"B&H vadeli: yıllık %{bh.mean()*252*100:.1f} Sharpe {sharpe(bh):.2f} | B&H spot (taşımasız): yıllık %{sbh.mean()*252*100:.1f} Sharpe {sharpe(sbh):.2f}")
print("\n=== MALİYET × H (tam örneklem ve 2018+) ===")
rows = []
for H in (3, 5):
    pos = position(sig, H); n_tr = len(trades(pos, r))
    for c in (0, 5, 10, 22, 40):
        p = pnl(pos, r, c); ps = pnl(pos, s_ret, c)
        a = alpha(p, bh); a18 = alpha(p["2018":], bh["2018":]); a_s = alpha(p, sbh); a_ss = alpha(ps, sbh)
        t = trades(pos, r, c); tc = t[~t.open_]
        rows.append(dict(H=H, bps=c, Sharpe=round(sharpe(p), 2), Sh_18p=round(sharpe(p["2018":]), 2), Sh_18_24=round(sharpe(p["2018":"2024"]), 2), yillik=round(p.mean() * 252 * 100, 1),
                         alfa=round(a[0], 1), alfa_t=round(a[1], 2), alfa18_t=round(a18[1], 2), alfa_vs_spotBH=round(a_s[0], 1), t_vs_spot=round(a_s[1], 2),
                         spotKural_Sh=round(sharpe(ps), 2), spotKural_alfa=round(a_ss[0], 1), spotKural_t=round(a_ss[1], 2), ort_islem=round(tc.ret.mean() * 100, 2), maxDD=round(maxdd(p) * 100, 1)))
print(pd.DataFrame(rows).to_string(index=False))
pos3 = position(sig, 3); p5 = pnl(pos3, r, 5)
paid = (pos3.shift(1) * carry).iloc[1:]
print(f"\nkuralın ödediği taşıma: yılda %{paid.mean()*252*100:.2f} (piyasada %{pos3.mean()*100:.0f}); B&H vadeli yılda %{carry.mean()*252*100:.2f} öder.")
print(f"Sharpe farkı ayrıştırma (5 bps, H=3): vadeli kural {sharpe(p5):.2f} − vadeli B&H {sharpe(bh):.2f} = {sharpe(p5)-sharpe(bh):+.2f} ; aynı kural spot getirisiyle {sharpe(pnl(pos3, s_ret, 5)):.2f} − spot B&H {sharpe(sbh):.2f} = {sharpe(pnl(pos3, s_ret, 5))-sharpe(sbh):+.2f}")
print("  maks düşüş: kural %", round(maxdd(p5) * 100, 1), "| B&H vadeli %", round(maxdd(bh) * 100, 1))
# ---- işlem süresi dağılımı
t3 = trades(pos3, r, 5); tc = t3[~t3.open_]
print("\nİŞLEM SÜRESİ (H=3; VİOP günü):", tc.days.describe().round(1).to_dict(), "| 3 gün olan %", round((tc.days == 3).mean() * 100), "| ≤5 gün %", round((tc.days <= 5).mean() * 100), "| >10 gün %", round((tc.days > 10).mean() * 100))
print("  süreye göre ort getiri %:", tc.groupby(pd.cut(tc.days, [0, 3, 5, 10, 100])).ret.agg(["size", "mean", "sum"]).assign(mean=lambda z: z["mean"] * 100, sum=lambda z: z["sum"] * 100).round(2).to_dict("index"))
# ---- taze / eski sinyal
age = sig.groupby((sig == 0).cumsum()).cumsum()     # kaçıncı ardışık sinyal günü
f3 = fwd(r, 3) * 100; f5 = fwd(r, 5) * 100; f1 = fwd(r, 1) * 100
print("\nSİNYAL YAŞI → sonraki getiriler (ort %):")
for nm, m in [("1. gün (taze)", age == 1), ("2–3. gün", (age >= 2) & (age <= 3)), ("4–7. gün", (age >= 4) & (age <= 7)), ("8+ gün", age >= 8), ("sinyal yok", sig == 0)]:
    print(f"  {nm:14s} n {int(m.sum()):4d}  h1 {f1[m].mean():+.3f}  h3 {f3[m].mean():+.3f}  h5 {f5[m].mean():+.3f}")
fresh = ((age == 1)).astype(float)
print("  yalnız TAZE sinyalde gir, tam 3 gün tut (uzatma yok): fark", {k: round(v, 3) for k, v in nw_diff(fwd(r, 3), fresh, 5).items() if k in ("m1", "m0", "diff", "t", "n1")})
print("  yalnız TAZE sinyalde gir, tam 5 gün tut:", {k: round(v, 3) for k, v in nw_diff(fwd(r, 5), fresh, 5).items() if k in ("m1", "m0", "diff", "t", "n1")})
# sinyal bittikten sonraki günler (çıkış kuralı gerekçesi)
off = ((sig == 0) & (sig.shift(1) == 1)).astype(float)
print("  sinyalin söndüğü ilk gün sonrası h3:", round(f3[off > 0].mean(), 3), "n", int(off.sum()))
# ---- PLASEBO
def stats(s, cost=5, H=3, a=None, b=None):
    pos = position(pd.Series(s, index=pv.index), H); p = pnl(pos, r, cost)[a:b]; t = trades(pos[a:b], r[a:b], cost); tc = t[~t.open_]
    al = alpha(p, bh[a:b])
    return sharpe(p), tc.ret.mean() * 100, al[0], al[1], p.mean() * 252 * 100, len(tc), pos[a:b].mean(), tc.ret.median() * 100, (tc.ret > 0).mean()
obs = stats(sig.values)
sv = sig.values; n = len(sv); yrs = pv.index.year.values
def circ(): return np.roll(sv, rng.integers(40, n - 40))
def within_year():
    out = sv.copy()
    for y in np.unique(yrs):
        m = np.where(yrs == y)[0]; out[m] = np.roll(sv[m], rng.integers(0, len(m)))
    return out
def run_shuffle():
    # 1 ve 0 koşularını ayrı ayrı karıştır, dönüşümlü diz
    ch = np.flatnonzero(np.diff(sv) != 0) + 1; runs = np.split(sv, ch)
    ones = [q for q in runs if q[0] > 0]; zeros = [q for q in runs if q[0] == 0]
    rng.shuffle(ones); rng.shuffle(zeros); out = []
    for i in range(max(len(ones), len(zeros))):
        if i < len(zeros): out.append(zeros[i])
        if i < len(ones): out.append(ones[i])
    return np.concatenate(out)
def iid(): return rng.permutation(sv)
names = ["Sharpe", "ort_islem%", "alfa%", "alfa_t", "yillik%", "islem", "piyasada", "medyan_islem%", "kazanan"]
print(f"\n=== PLASEBO (1000 simülasyon; H=3, 5 bps). GERÇEK KURAL: " + ", ".join(f"{k} {v:.2f}" for k, v in zip(names, obs)))
for nm, gen in [("A dairesel kaydırma (kümelenme aynı, zaman rastgele)", circ), ("B koşu karıştırma (aynı işlem süreleri, rastgele sıra)", run_shuffle), ("C YIL İÇİ kaydırma (her yıl aynı sayıda sinyal günü)", within_year), ("D tamamen rastgele günler (kümelenmesiz)", iid)]:
    sims = np.array([stats(gen()) for _ in range(1000)])
    pct = [(sims[:, i] < obs[i]).mean() * 100 for i in range(5)]
    print(f"[{nm}]")
    print("   plasebo medyan: " + ", ".join(f"{k} {np.median(sims[:, i]):.2f}" for i, k in enumerate(names)))
    print("   plasebo %5–%95: " + ", ".join(f"{k} [{np.percentile(sims[:, i],5):.2f}, {np.percentile(sims[:, i],95):.2f}]" for i, k in enumerate(names[:5])))
    print("   kuralın yüzdeliği: " + ", ".join(f"{k} %{pct[i]:.1f}" for i, k in enumerate(names[:5])))
# 2018+ ve 2018–2024 için C tipi
for per, a, b in [("2018–2026", "2018", None), ("2018–2024", "2018", "2024"), ("2026 hariç", None, "2025")]:
    o = stats(sig.values, a=a, b=b)
    for nm, gen in [("A", circ), ("C", within_year)]:
        sims = np.array([stats(gen(), a=a, b=b) for _ in range(500)])
        print(f"[{per} / plasebo {nm}] kural Sharpe {o[0]:.2f} (yüzdelik %{(sims[:,0]<o[0]).mean()*100:.1f}; plasebo medyan {np.median(sims[:,0]):.2f}) | ort işlem %{o[1]:.2f} (yüzdelik %{(sims[:,1]<o[1]).mean()*100:.1f}; medyan {np.median(sims[:,1]):.2f}) | alfa %{o[2]:.1f} (yüzdelik %{(sims[:,2]<o[2]).mean()*100:.1f})")
