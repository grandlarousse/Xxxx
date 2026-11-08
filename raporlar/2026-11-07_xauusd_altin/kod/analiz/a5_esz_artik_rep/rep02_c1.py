"""Adım 2: C1 (büyük makro günlerinde 12-15 UTC artık sürmesi) bağımsız yeniden hesap."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/spot_snaps.parquet")
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
D = D[D.index >= "2010-01-01"]
g12 = np.log(D.XAU_p15 / D.XAU_p12)
X12 = pd.DataFrame({k: np.log(D[f"{k}_p15"] / D[f"{k}_p12"]) for k in ("DXY", "TBOND", "SPX")})
print("x12 kapsama:", X12.notna().all(1).sum(), "ilk tam gün:", X12.dropna().index[0].date())
print("en büyük |x12|:", X12.abs().max().round(4).to_dict(), X12.abs().idxmax().astype(str).to_dict())
rr = rolling_ols(g12, X12, 60)
e12 = rr.e / rr.sig; f12 = rr.fit / rr.sig
print("e12 ilk:", e12.dropna().index[0].date(), "n:", e12.notna().sum())
V = lambda s: s.reindex(va.index)
E, F = V(e12), V(f12)
thr = F.abs()[F.index <= IS_END].dropna().quantile(0.8)
print("eşik q80 |fit/σ| (IS VİOP günleri):", round(thr, 4), " IS gözlem:", F[F.index <= IS_END].notna().sum())
cond = F.abs() > thr
x = E.where(cond)
print("koşul günleri:", int(x.notna().sum()), "ilk:", x.dropna().index[0].date(), " yıllık:", x.dropna().groupby(x.dropna().index.year).size().to_dict())
for h in (1, 3, 5):
    st = stats(x, va[f"fwd{h}"], h)
    print(f"C1 h{h}: ic {st['ic']:.3f} t {st['t']:.2f} n {st['n']} | IS ic {st['ic_is']:.3f} t {st['t_is']:.2f} n {st['n_is']} | OOS ic {st['ic_oos']:.3f} t {st['t_oos']:.2f} n {st['n_oos']} | yıl {st['yrs']}")
st = stats(x, va.fwd3, 3); print("yıllık IC h3:", st["by_year"])
# NW lag duyarlılığı ve düzeltme
for L in (3, 5, 10):
    print(f"  h3 NW L={L}: t={stats(x, va.fwd3, 3, L=L)['t']:.2f}")
# Pearson
for clip in (None, 3):
    xx = x if clip is None else x.clip(-clip, clip)
    st = stats(xx, va.fwd3, 3, method="pearson"); print(f"Pearson h3 clip={clip}: ic {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f}")
# Spot ve atlamalı hedef (2016+ spot takvimi)
xs = e12.where(f12.abs() > thr)
for h in (3,):
    sf = sum(np.log(D.XAU_p15).diff().shift(-k) for k in range(1, h + 1))
    sk = np.log(D.XAU_p15.shift(-h) / D.XAU_p16)
    for nm, yy in [("spot", sf), ("skip1h", sk)]:
        st = stats(xs, yy, h); print(f"C1 {nm} h{h}: t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} n {st['n']}")
# eşik duyarlılığı
for q in (0.7, 0.9):
    th = F.abs()[F.index <= IS_END].dropna().quantile(q)
    st = stats(E.where(F.abs() > th), va.fwd3, 3); print(f"q{int(q*100)} h3: thr {th:.3f} t {st['t']:.2f} OOS {st['t_oos']:.2f} n {st['n']}")
# kontroller
st = stats(V(g12).where(cond), va.fwd3, 3); print("kendi g12 | koşul h3: t", round(st["t"], 2))
st = stats(E.where(~cond & F.notna()), va.fwd3, 3); print("sakin makro günleri h3: t", round(st["t"], 2))
st = stats(x.where(x.index.year != 2020), va.fwd3, 3); print("2020 hariç: t", round(st["t"], 2), "IS", round(st["t_is"], 2), "OOS", round(st["t_oos"], 2))

# --- Backtest: sign(e12) koşul günlerinde, 3 alt portföy, 5 bps ---
pos = np.sign(x).fillna(0.0)
res = bt_split(pos, va.ret, 3, 5.0)
for k, d in res.items():
    print(k, {a: round(b, 3) for a, b in d.items()})
print("sinyal/yıl:", round(pos.ne(0).sum() / ((va.index[-1] - x.dropna().index[0]).days / 365.25), 1), " (tüm dönem yıl başına:", round(pos.ne(0).sum()/ ((va.index[-1]-va.index[0]).days/365.25),1), ")")
# OOS-only: sinyal döneminin içinde Sharpe (pozisyonsuz günler dahil) zaten öyle; ayrıca sinyal varlığı döneminde
# işlem düzeyi
tr = (pos * va.fwd3)[pos != 0].dropna()
print("işlem başı brüt bps: tüm", round(tr.mean() * 1e4, 1), "IS", round(tr[tr.index <= IS_END].mean() * 1e4, 1), "OOS", round(tr[tr.index > IS_END].mean() * 1e4, 1), "n", len(tr),
      " t(işlem, örtüşme yok sayılmış):", round(tr.mean() / tr.std() * np.sqrt(len(tr)), 2))
print("uzun işlem ort bps", round(va.fwd3[pos > 0].mean() * 1e4, 1), " kısa işlem (kısa getirisi) bps", round((-va.fwd3[pos < 0]).mean() * 1e4, 1), " koşulsuz 3g bps", round(va.fwd3.mean() * 1e4, 1))
pnl = bt(pos, va.ret, 3, 5.0)["pnl"]
print("yıllık net %:", (pnl.groupby(pnl.index.year).sum() * 100).round(2).to_dict())
pd.DataFrame(dict(e12=e12, f12=f12, g12=g12)).to_parquet(f"{OUT}/c1_signal_rep.parquet")
