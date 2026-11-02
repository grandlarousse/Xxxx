"""07: Uyarlamalı eşik (z), başabaş maliyet, doğrusal boyutlama, blok bootstrap GA (OOS |U|>50)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
df = pd.read_parquet(OUT + "/02_daily.parquet")
q = df[(df.index >= "2014-01-01")].copy(); q = q[q.D.abs() < 0.15]; q["U"] = q.D - q.gap1
sdD = q.D.rolling(250, min_periods=60).std().shift(1)  # geçmiş bilgi
q["zD"] = q.D / sdD; q["zU"] = q.U / sdD; q["zDk0"] = q.D_k0 / q.D_k0.rolling(250, min_periods=60).std().shift(1)
q["zUk0"] = (q.D_k0 - q.gap1) / q.D_k0.rolling(250, min_periods=60).std().shift(1)
print("=== Uyarlamalı eşik |z|>1 (z = sinyal / geçmiş 250g sd(D)) — brüt bps/işlem (= başabaş maliyet) ve net 8/15 ===")
for nm in ["zD", "zU", "zDk0", "zUk0"]:
    for thr in [0.5, 1.0, 1.5]:
        o = []
        for lab, s, e in [("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]:
            g = bt(q[nm], q.intra1, 0, thr, s, e); n8 = bt(q[nm], q.intra1, 8, thr, s, e); n15 = bt(q[nm], q.intra1, 15, thr, s, e)
            o.append(f"{lab} n {g['n']} brüt {g['mean_bps']:5.1f} t {g['t']:4.2f} | Sh8 {n8['sharpe']:5.2f} Sh15 {n15['sharpe']:5.2f}")
        print(f"  {nm:5s} |z|>{thr}: " + " || ".join(o))
print("\n=== Doğrusal boyutlama w = clip(zD, -2, 2) (maliyet 8 bps × |w|) ===")
w = q.zD.clip(-2, 2)
for lab, s, e in [("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]:
    z = pd.concat([w.rename("w"), q.intra1.rename("y")], axis=1).dropna(); z = z[(z.index >= s) & (z.index <= e)]
    p = z.w * z.y - 8e-4 * z.w.abs(); p0 = z.w * z.y
    print(f"  {lab}: brüt Sh {p0.mean()/p0.std()*np.sqrt(252):.2f} net Sh {p.mean()/p.std()*np.sqrt(252):.2f} n {len(z)}")
print("\n=== Blok bootstrap (blok 20 gün, 5000) OOS |U|>50 net 8 bps ort ve IS ===")
rng = np.random.default_rng(7)
for lab, s, e in [("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]:
    z = q[(q.index >= s) & (q.index <= e)].dropna(subset=["U", "intra1"])
    pos = np.sign(z.U).where(z.U.abs() > 0.005, 0); pnl = (pos * z.intra1 - 8e-4 * pos.abs()).values; act = (pos != 0).values
    N = len(pnl); B = 20; nb = N // B + 1; ms = []
    for _ in range(5000):
        st = rng.integers(0, N - B, nb); idx = (st[:, None] + np.arange(B)).ravel()[:N]
        a = act[idx]; ms.append(pnl[idx][a].mean() * 1e4)
    ms = np.array(ms); print(f"  {lab}: ort {pnl[act].mean()*1e4:.1f} bps, %95 GA [{np.percentile(ms,2.5):.1f}, {np.percentile(ms,97.5):.1f}], P(<=0) {(ms<=0).mean():.3f}")
