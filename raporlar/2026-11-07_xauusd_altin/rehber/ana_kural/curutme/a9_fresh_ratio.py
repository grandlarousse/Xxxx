"""Kullanıcının tarzına en yakın sürüm: taze sinyalde gir, tam 3 gün sonra çık (uzatma yok) + oran biçimi alt dönemler."""
import numpy as np, pandas as pd
from adv_lib import *
rng = np.random.default_rng(5)
R = us_returns(); e, B = rolling_resid(R); pv = viop(); r = pv.v_ret; bh = (np.exp(r) - 1).iloc[1:]
E10 = e.rolling(10).sum(); thr = E10[:"2017-12-31"].dropna().quantile(.8); x, _ = map_us_to_viop(E10, pv.index); sig = (x > thr).astype(float)
age = sig.groupby((sig == 0).cumsum()).cumsum(); fresh = (age == 1)
f3 = (np.exp(fwd(r, 3)) - 1) * 100
d = pd.DataFrame({"f3": f3[fresh]}).dropna(); d["y"] = d.index.year
print("TAZE-3GÜN: n", len(d), "ort %", round(d.f3.mean(), 2), "medyan %", round(d.f3.median(), 2), "kazanan %", round((d.f3 > 0).mean() * 100), "en kötü %", round(d.f3.min(), 1), "en iyi %", round(d.f3.max(), 1), "std %", round(d.f3.std(), 2))
print("  tüm günlerin 3 günlük ort %", round(f3.mean(), 3), "| kazanan %", round((f3 > 0).mean() * 100))
print("  yıl yıl:", d.groupby("y").f3.agg(["size", "mean"]).round(2).to_dict("index"))
allf = f3.dropna().values; n = len(d)
sim = np.array([rng.choice(allf, n, replace=False).mean() for _ in range(5000)])
print("  rastgele n gün plasebosu: ort yüzdelik %", round((sim < d.f3.mean()).mean() * 100, 1))
for a, b in [(None, "2024"), ("2018", "2024"), ("2025", None)]:
    dd = d[a:b]; al = f3[a:b].dropna().values; sm_ = np.array([rng.choice(al, len(dd), replace=False).mean() for _ in range(5000)])
    print(f"  {a}..{b}: n {len(dd)} ort %{dd.f3.mean():.2f} (tüm günler %{al.mean():.2f}) yüzdelik %{(sm_ < dd.f3.mean()).mean()*100:.1f}")
# oran biçimi alt dönem + işlem
ser = (R.GDX - R.GLD).rolling(10).sum(); th = ser[:"2017-12-31"].dropna().quantile(.8); xr, _ = map_us_to_viop(ser, pv.index); sr = (xr > th).astype(float)
pos = position(sr, 3); p = pnl(pos, r, 5); t = trades(pos, r, 5); tc = t[~t.open_].copy(); tc["y"] = tc.entry.dt.year
print("\nORAN BİÇİMİ (GDX 10g getirisi − GLD 10g getirisi > %", round(th * 100, 2), ") H=3, 5 bps:")
g = tc.groupby("y").ret.agg(["size", "mean", "sum"]); g[["mean", "sum"]] *= 100; print(g.round(2).T.to_string())
for nm, a, b in [("tam", None, None), ("2018-26", "2018", None), ("2018-24", "2018", "2024"), ("2022-24", "2022", "2024"), ("2025-26", "2025", None)]:
    al = alpha(p[a:b], bh[a:b]); print(f"  {nm:8s} Sharpe {sharpe(p[a:b]):.2f} (B&H {sharpe(bh[a:b]):.2f}) alfa %{al[0]:.1f} t {al[1]:.2f} | h3 t {nw_diff(fwd(r,3)[a:b], sr[a:b], 10)['t']:.2f} h5 t {nw_diff(fwd(r,5)[a:b], sr[a:b], 10)['t']:.2f}")
print("  V0 ile aynı gün sinyal veren oran:", round((sr[sig > 0] > 0).mean(), 2), "| oran sinyal günü:", int(sr.sum()), "| işlem:", len(tc), "ort %", round(tc.ret.mean() * 100, 2), "kazanan %", round((tc.ret > 0).mean() * 100), "en kötü %", round(tc.ret.min() * 100, 1))
# her iki biçim birden (kesişim)
both = ((sr > 0) & (sig > 0)).astype(float); pb = pnl(position(both, 3), r, 5); alb = alpha(pb, bh)
print("  KESİŞİM (ikisi de sinyal): gün", int(both.sum()), "Sharpe", round(sharpe(pb), 2), "alfa t", round(alb[1], 2), "| 2018–24 Sharpe", round(sharpe(pb['2018':'2024']), 2))
