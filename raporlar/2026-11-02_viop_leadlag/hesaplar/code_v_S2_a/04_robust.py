"""04: Sağlamlık: FX zamanlaması (k0), alternatif tanımlar, kontroller, piyasa-nötr hedef, plasebo, aykırı değer, long/short ayrımı, kaydırma null'u."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
pd.set_option("display.width", 250)
df = pd.read_parquet(OUT + "/02_daily.parquet")
q = df[(df.index >= "2014-01-01")].copy()
q = q[q.D.abs() < 0.15]
q["U"] = q.D - q.gap1
PER = [("ALL", "2014-01-01", "2026-12-31"), ("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]
def regline(y, xs, z, name):
    out = []
    for lab, s, e in PER:
        zz = z[(z.index >= s) & (z.index <= e)]
        m, n = nw(zz[y], zz[xs])
        out.append(f"{lab}: b {m.params[xs[0]]:.3f} t {m.tvalues[xs[0]]:.2f} n {n}")
    print(f"{name:55s} | " + " | ".join(out))
print("=== A) Zamanlama: FX k0 (t sabahı kuru, kesinlikle ileriye bakmaz) ===")
q["U_k0"] = q.D_k0 - q.gap1
regline("intra1", ["D_k0", "gap1"], q, "intra1 ~ D_k0 + gap1")
regline("intra1", ["D", "gap1"], q, "intra1 ~ D(k1) + gap1 [referans]")
q["dfx_dev"] = q.D - q.D_k0
regline("intra1", ["dfx_dev", "D_k0", "gap1"], q, "intra1 ~ (D-D_k0: gün içi kur bileşeni) + D_k0 + gap1")
regline("gap1", ["D_k0"], q, "gap1 ~ D_k0")
for lab, s, e in PER[1:]:
    r = bt(q.U_k0, q.intra1, 8, 0.005, s, e); print(f"  BT U_k0 |>50| {lab}: n {r['n']} {r['mean_bps']:.1f} bps t {r['t']:.2f} Sh {r['sharpe']:.2f}")
print("\n=== B) Alternatif sapma tanımları (intra1 ~ X + gap1; BT |X-gap1|>50 bps 8 bps) ===")
for nm in ["D", "Dc", "D10", "D60", "D_med"]:
    z = q.dropna(subset=[nm]); z = z[z[nm].abs() < 0.15]
    regline("intra1", [nm, "gap1"], z, f"intra1 ~ {nm} + gap1")
    u = z[nm] - z.gap1
    print("   BT:", " | ".join(f"{lab} {bt(u, z.intra1, 8, 0.005, s, e)['mean_bps']:.1f} bps Sh {bt(u, z.intra1, 8, 0.005, s, e)['sharpe']:.2f}" for lab, s, e in PER[1:]))
print("\n=== C) Kontroller ===")
regline("intra1", ["D", "gap1", "xu_gap1", "intra0", "cc0", "xu_intra0"], q, "intra1 ~ D + gap1 + XU100gap1 + kendi lag + XU lag")
regline("intra1", ["D", "gap1", "xu_gap1", "xu_intra1"], q, "intra1 ~ D + gap1 + XU100gap1 + XU100intra1 (senkron)")
regline("intra1", ["D", "gap1", "es_cc"], q, "intra1 ~ D + gap1 + ES(t)")
# piyasa-nötr hedef: beta geçmiş 250g
b = (q.intra1.rolling(250, min_periods=100).cov(q.xu_intra1) / q.xu_intra1.rolling(250, min_periods=100).var()).shift(1)
q["ab_intra1"] = q.intra1 - b * q.xu_intra1
regline("ab_intra1", ["D", "gap1"], q, "TCELL-βXU100 gün-içi ~ D + gap1")
print("\n=== D) Plasebo hedefler ===")
regline("xu_intra1", ["D", "xu_gap1"], q, "XU100 intra1 ~ D + XU gap1")
regline("x30_intra1", ["D", "x30_gap1"], q, "XU030 intra1 ~ D + XU030 gap1")
regline("tt_intra1", ["D", "tt_gap1"], q, "TTKOM intra1 ~ D + TTKOM gap1")
print("\n=== E) Plasebo zaman: D_{t-1} -> intra_{t+1}  (bir gün eski sinyal) ===")
q["Dlag"] = q.D.shift(1)
regline("intra1", ["Dlag", "gap1"], q, "intra1 ~ D_{t-1} + gap1")
regline("intra1", ["D", "Dlag", "gap1"], q, "intra1 ~ D + D_{t-1} + gap1")
print("\n=== F) Aykırı değerler / rejim ===")
lo, hi = q.D.quantile([0.01, 0.99]); qw = q.copy(); qw["D"] = qw.D.clip(lo, hi); qw["gap1"] = qw.gap1.clip(*qw.gap1.quantile([0.01, 0.99]))
qw["intra1"] = qw.intra1.clip(*qw.intra1.quantile([0.01, 0.99]))
regline("intra1", ["D", "gap1"], qw, "winsorize %1 (D, gap1, intra1)")
ex = q[~((q.index >= "2021-11-15") & (q.index <= "2022-01-31"))]
regline("intra1", ["D", "gap1"], ex, "KKM dönemi (15.11.21-31.01.22) hariç")
ex2 = ex[~((ex.index >= "2018-08-01") & (ex.index <= "2018-09-30")) & ~((ex.index >= "2025-03-18") & (ex.index <= "2025-04-10"))]
regline("intra1", ["D", "gap1"], ex2, "+ Ağu-Eyl 2018 ve Mar-Nis 2025 hariç")
for lab, s, e in PER[1:]:
    u = ex.U; r = bt(u, ex.intra1, 8, 0.005, s, e); print(f"  BT |U|>50 KKM hariç {lab}: n {r['n']} {r['mean_bps']:.1f} bps Sh {r['sharpe']:.2f}")
# en büyük 10 işlem katkısı (OOS)
z = q[q.index >= "2021"]; pos = np.sign(z.U).where(z.U.abs() > 0.005, 0); pnl = (pos * z.intra1 - 8e-4 * pos.abs())[pos != 0]
srt = pnl.sort_values()
print(f"  OOS toplam pnl {1e4*pnl.sum():.0f} bps; en iyi 10 işlem {1e4*srt.iloc[-10:].sum():.0f} bps, en kötü 10 {1e4*srt.iloc[:10].sum():.0f}; en iyi 10 hariç ort {1e4*srt.iloc[:-10].mean():.1f} bps")
print("  en iyi 10 işlem tarihleri:", [d.strftime('%Y-%m-%d') for d in srt.index[-10:]])
print("\n=== G) Long/short ayrımı ve yön yanlılığı ===")
for lab, s, e in PER:
    z = q[(q.index >= s) & (q.index <= e)]
    pos = np.sign(z.U).where(z.U.abs() > 0.005, 0)
    L = z.intra1[pos > 0]; S = -z.intra1[pos < 0]
    print(f"{lab}: long n {len(L)} brüt {1e4*L.mean():.1f} bps | short n {len(S)} brüt {1e4*S.mean():.1f} bps | TCELL ort gün-içi {1e4*z.intra1.mean():.1f} bps | ort U {1e4*z.U.mean():.1f} bps | ort gap1 {1e4*z.gap1.mean():.1f}")
# demeaned U: geçmiş 250g gap ortalaması çıkarılmış
gm = q.gap1.shift(1).rolling(250, min_periods=100).mean()  # gap1(t) = gap at t+1; shift(1) -> son bilinen
q["U_dm"] = q.D - (q.gap1 - gm)
for lab, s, e in PER[1:]:
    r = bt(q.U_dm, q.intra1, 8, 0.005, s, e); print(f"  BT U_demeaned(gap ort. çıkarılmış) |>50| {lab}: n {r['n']} {r['mean_bps']:.1f} bps Sh {r['sharpe']:.2f} long% {r['long_frac']:.2f}")
# sabit pozisyon kıyas: hep short gün-içi
for lab, s, e in PER[1:]:
    r = bt(pd.Series(-1.0, index=q.index), q.intra1, 8, 0, s, e); print(f"  KIYAS her gün short TCELL gün-içi {lab}: {r['mean_bps']:.1f} bps Sh {r['sharpe']:.2f}")
print("\n=== H) Dairesel kaydırma null'u (sinyal 21..N-21 gün kaydırılır), OOS |U|>50 ===")
z = q[q.index >= "2021"].dropna(subset=["D", "gap1", "intra1"])
obs = bt(z.D - z.gap1, z.intra1, 8, 0.005)["sharpe"]
Dv = z.D.values; N = len(z); sh = []
for k in range(21, N - 21, 3):
    Ds = pd.Series(np.roll(Dv, k), index=z.index)
    sh.append(bt(Ds - z.gap1, z.intra1, 8, 0.005)["sharpe"])
sh = np.array(sh)
print(f"  gözlenen Sharpe {obs:.2f}; null ort {sh.mean():.2f} sd {sh.std():.2f}; p(null>=obs) {(sh >= obs).mean():.3f} (n={len(sh)})")
# aynı null D sinyali için (gap kullanılmaz)
obsD = bt(z.D, z.intra1, 8, 0.005)["sharpe"]; shD = np.array([bt(pd.Series(np.roll(Dv, k), index=z.index), z.intra1, 8, 0.005)["sharpe"] for k in range(21, N - 21, 3)])
print(f"  D-only: gözlenen {obsD:.2f}; null ort {shD.mean():.2f} sd {shD.std():.2f}; p {(shD >= obsD).mean():.3f}")
print("  NOT: U null'unun ortalaması > 0 ise kazancın bir kısmı gap-fade/kısa yanlılıktan, D'den değil.")
