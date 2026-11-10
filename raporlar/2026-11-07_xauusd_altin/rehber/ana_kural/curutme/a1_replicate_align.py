"""(1) Bağımsız yeniden üretim + ileriye bakma / takvim hizası denetimi + sağlam çıkarım."""
import numpy as np, pandas as pd
from adv_lib import *
np.random.seed(7)
R = us_returns()
e, B = rolling_resid(R)
E10 = e.rolling(10).sum()
print("ABD getirileri:", R.index[0].date(), "→", R.index[-1].date(), len(R))
print("beta özet (2017+):"); print(B["2017":].describe().loc[["mean", "std", "min", "50%", "max"]].round(2).to_string())
print("beta yıl ortalaması:"); print(B.groupby(B.index.year).mean().round(2).T.to_string())
thr_a = E10[:"2017-12-31"].dropna().quantile(.8); thr_b = E10["2008-01-01":"2017-12-31"].dropna().quantile(.8)
thr_c = E10[:"2017-03-03"].dropna().quantile(.8)
print(f"eşik q80: 2006-08..2017 (ana ajan) %{thr_a*100:.3f} | 2008..2017 %{thr_b*100:.3f} | yalnız VİOP öncesi (..2017-03-03) %{thr_c*100:.3f}")
thr = thr_a
pv = viop(); r = pv.v_ret
x, used = map_us_to_viop(E10, pv.index)
sig = (x > thr).astype(float)
# --- takvim hizası denetimi
gap = (pv.index.values - used.values).astype("timedelta64[D]").astype(int)
print("\nHİZA: VİOP günü − kullanılan ABD kapanış günü (takvim günü) dağılımı:", pd.Series(gap).value_counts().sort_index().to_dict())
print("  ABD kapanışı ≥ VİOP günü olan satır (ihlal):", int((used.values >= pv.index.values).sum()))
# panelin kendi y_GDX_avail sütunuyla çapraz kontrol: kullandığım ABD günü kapanışı = panelin 'karar anında bilinen' kapanışı mı?
gdx = yahoo("GDX")
chk = pd.DataFrame({"mine": gdx.reindex(used.values).values, "panel": pv.y_GDX.values}, index=pv.index).dropna()
print("  panel y_GDX ile aynı kapanış:", int((np.abs(chk.mine / chk.panel - 1) < 1e-6).sum()), "/", len(chk), "| farklı:", int((np.abs(chk.mine / chk.panel - 1) >= 1e-6).sum()))
av = pd.to_datetime(pv.y_GDX_avail).dt.tz_localize(None) if hasattr(pv.y_GDX_avail.dtype, "tz") and pv.y_GDX_avail.dtype.tz is not None else pd.to_datetime(pv.y_GDX_avail)
cut = pv.index + pd.Timedelta(hours=15)
print("  panel y_GDX_avail ≥ gün t 15:00 UTC olan satır:", int((av.values >= cut.values).sum()), "| en geç bilgi saati − cutoff (saat) min:", round(((cut.values - av.values).astype("timedelta64[m]").astype(int) / 60).min(), 1))
# --- temel sonuç
print(f"\nsinyal günü: {int(sig.sum())}/{len(sig)}  (2018+: {int(sig['2018':].sum())}/{len(sig['2018':])})")
rows = []
for h in (1, 3, 5, 10):
    for nm, a, b in [("2017-03..2026", None, None), ("2018..2026", "2018", None), ("2017-03..2021", None, "2021"), ("2022..2026", "2022", None), ("2022..2024", "2022", "2024"), ("2025..2026", "2025", None), ("2018..2024", "2018", "2024"), ("2026 hariç", None, "2025")]:
        y = fwd(r, h)[a:b]; s = sig[a:b]
        for L in (5, 10, 20):
            q = nw_diff(y, s, max(L, h)); rows.append(dict(h=h, donem=nm, L=max(L, h), **q))
T = pd.DataFrame(rows)
print("\nFARK (sinyal günleri − diğer günler) %, NW t (lag 5/10/20):")
pt = T.pivot_table(index=["h", "donem"], columns="L", values="t", sort=False).round(2)
base = T[T.L == T.groupby(["h", "donem"]).L.transform("min")].set_index(["h", "donem"])[["m1", "mall", "diff", "n1", "N"]].round(3)
print(base.join(pt).to_string())
# --- ileriye bakma plasebo: sinyali kaydır
print("\nKAYDIRMA (h3 / h5 fark, NW10 t). +: sinyal gecikir (eski bilgi), −: GELECEK bilgi")
for sh in (-10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10, 20):
    a3 = nw_diff(fwd(r, 3), sig.shift(sh), 10); a5 = nw_diff(fwd(r, 5), sig.shift(sh), 10)
    print(f"  {sh:+3d}: h3 {a3['diff']:+.3f}% t {a3['t']:.2f} | h5 {a5['diff']:+.3f}% t {a5['t']:.2f}")
xs, _ = map_us_to_viop(E10, pv.index, same_day=True); ss = (xs > thr).astype(float)
print("  [bilerek İLERİYE BAKAN sürüm: aynı gün ABD kapanışı] h3:", {k: round(v, 3) for k, v in nw_diff(fwd(r, 3), ss, 10).items() if k in ("diff", "t")})
x2, _ = map_us_to_viop(E10, pv.index, extra_lag=1); s2 = (x2 > thr).astype(float)
print("  [bir ABD günü ek gecikme: t-2 kapanışı] h3:", {k: round(v, 3) for k, v in nw_diff(fwd(r, 3), s2, 10).items() if k in ("diff", "t")}, "h5:", {k: round(v, 3) for k, v in nw_diff(fwd(r, 5), s2, 10).items() if k in ("diff", "t")})
# giriş anında (aynı gün) getiri ve giriş öncesi sızıntı
print("  sinyal günü t'nin KENDİ getirisi (t-1→t uzlaşma; girişten önce, kaçırılan):", {k: round(v, 3) for k, v in nw_diff(r, sig, 5).items() if k in ("m1", "m0", "diff", "t")})
# --- düz kapanış (temettüsüz) ile sinyal: elle hesap gerçekçiliği
Rc = us_returns(col="close"); ec, _ = rolling_resid(Rc); E10c = ec.rolling(10).sum(); xc, _ = map_us_to_viop(E10c, pv.index); sc = (xc > thr).astype(float)
print("\nTemettü düzeltmesiz 'close' ile sinyal: uyuşma oranı", round((sc == sig).mean(), 4), "| h3", {k: round(v, 3) for k, v in nw_diff(fwd(r, 3), sc, 10).items() if k in ("diff", "t")})
# --- permütasyon: dairesel kaydırma (sinyalin kümelenmesini korur) — tam örneklem ve 2018+
def circ_p(y, s, nrep=2000, minshift=30):
    d = pd.concat([y.rename("y"), s.rename("s")], axis=1).dropna(); yv = d.y.values; sv = d.s.values; n = len(d)
    obs = yv[sv > 0].mean() - yv[sv == 0].mean()
    ks = np.random.randint(minshift, n - minshift, nrep)
    sim = np.array([yv[np.roll(sv, k) > 0].mean() - yv[np.roll(sv, k) == 0].mean() for k in ks])
    return obs * 100, (sim >= obs).mean(), sim.std() * 100
print("\nDAİRESEL KAYDIRMA permütasyonu (tek yönlü p; sinyal kümelenmesi korunur):")
for h in (3, 5):
    for nm, a, b in [("2017-03..2026", None, None), ("2018..2026", "2018", None), ("2018..2024", "2018", "2024"), ("2026 hariç", None, "2025")]:
        o, p, sd = circ_p(fwd(r, h)[a:b], sig[a:b]); print(f"  h{h} {nm:15s} fark {o:+.3f}%  perm-sd {sd:.3f}  z {o/sd:.2f}  p {p:.3f}")
# --- örtüşmesiz: işlem bazında (H=3) t
pos = position(sig, 3); tr = trades(pos, r)
tc = tr[~tr.open_]
print(f"\nİŞLEM (H=3, maliyetsiz): {len(tc)} kapalı işlem (+{int(tr.open_.sum())} açık), ort süre {tc.days.mean():.1f} gün, ort %{tc.ret.mean()*100:.2f}, medyan %{tc.ret.median()*100:.2f}, kazanan %{(tc.ret>0).mean()*100:.0f}, en kötü %{tc.ret.min()*100:.1f}, en iyi %{tc.ret.max()*100:.1f}, t(ort=0) {tc.ret.mean()/tc.ret.std()*np.sqrt(len(tc)):.2f}")
pd.DataFrame({"x": x, "sig": sig, "us_date": used}).to_parquet(OUT + "/sig_adv.parquet")
main = pd.read_parquet(S + "/out/net/c1_viop_sig.parquet")
print("ana ajanın sinyaliyle uyuşma:", round((main.sig.values == sig.values).mean(), 5), "| x maks fark:", float(np.nanmax(np.abs(main.x.values - x.values))))
