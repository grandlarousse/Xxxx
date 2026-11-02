"""(c)+(e) Sağlamlık: CIMSA/OYAKC günlük fade. Yön (long/short), gap kovaları, olay dışlama, en iyi N işlemi atma, z-eşik, hisseye özgü gap,
ham gap (temettü düzeltmesiz), küçük gap (<%1) plasebo, maliyet duyarlılığı/başabaş, 2016+ temiz-veri IS."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
X = decomp("XU100")
out = []
def rep(s, lab, p, note=""):
    i = p[p.index < SPLIT]; o = p[p.index >= SPLIT]; i16 = i[i.index >= "2016"]
    a = nw_mean_t(p.values); b = nw_mean_t(i.values); b16 = nw_mean_t(i16.values); c = nw_mean_t(o.values)
    yr = p.groupby(p.index.year).mean()
    out.append(dict(sym=s, spec=lab, n=a[2], all_bps=1e4 * a[0], all_t=a[1], IS_bps=1e4 * b[0], IS_t=b[1], IS16_bps=1e4 * b16[0], IS16_t=b16[1], OOS_bps=1e4 * c[0], OOS_t=c[1], OOS_n=c[2],
                    yrs_pos=f"{int((yr>0).sum())}/{len(yr)}", hit=float((p > 0).mean())))
for s in ["CIMSA", "OYAKC"]:
    d = decomp(s).join(X[["gap", "intra"]].add_prefix("x_"), how="left").dropna(subset=["gap", "intra"])
    C = 0.0010
    base = d[d.gap.abs() > 0.01]; pb = -np.sign(base.gap) * base.intra - C
    rep(s, "temel |gap|>1% net10", pb)
    rep(s, "sadece gap<-1% (long)", (base.intra - C)[base.gap < 0])
    rep(s, "sadece gap>+1% (short)", (-base.intra - C)[base.gap > 0])
    for lo, hi in [(0.01, 0.02), (0.02, 0.04), (0.04, 0.09), (0.09, 0.2)]:
        m = (d.gap.abs() > lo) & (d.gap.abs() <= hi); y = d[m]; rep(s, f"kova {lo:.0%}-{hi:.0%}", -np.sign(y.gap) * y.intra - C)
    m = (d.gap.abs() > 0.0) & (d.gap.abs() <= 0.01); y = d[m]; rep(s, "plasebo 0<|gap|<=1% net10", -np.sign(y.gap) * y.intra - C)
    rep(s, "plasebo 0<|gap|<=1% brüt", -np.sign(y.gap) * y.intra)
    ex = pb[~((pb.index >= "2023-02-06") & (pb.index <= "2023-03-31"))]; rep(s, "deprem (06.02-31.03.2023) hariç", ex)
    ex = pb[base.gap.abs() < 0.09]; rep(s, "tavan/taban açılış (|gap|>=9%) hariç", ex)
    for k in [5, 10, 20]:
        q = pb.drop(pb.abs().nlargest(k).index); rep(s, f"en büyük |pnl| {k} işlem atıldı", q)
        q = pb.drop(pb.nlargest(k).index); rep(s, f"en iyi {k} işlem atıldı", q)
    # z-eşik: gap / kayan 60g gap std (t-1'e kadar)
    sd = d.gap.rolling(60, min_periods=40).std().shift(1); z = d.gap / sd
    for zt in [1.0, 1.5, 2.0]:
        y = d[z.abs() > zt]; rep(s, f"z>{zt} (60g gap sd) net10", -np.sign(y.gap) * y.intra - C)
    # hisseye özgü gap: gap - beta*XU100 gap; beta kayan 250g (t-1'e kadar)
    dd = d.dropna(subset=["x_gap"])
    beta = (dd.gap.rolling(250, min_periods=120).cov(dd.x_gap) / dd.x_gap.rolling(250, min_periods=120).var()).shift(1)
    idio = dd.gap - beta * dd.x_gap
    y = dd[idio.abs() > 0.01]; rep(s, "hisseye özgü gap |idio|>1% fade", -np.sign(idio[idio.abs() > 0.01]) * y.intra - C)
    y = dd[(dd.x_gap.abs() > 0.01)]; rep(s, "piyasa gap |XU100 gap|>1% fade (hisse intra)", -np.sign(y.x_gap) * y.intra - C)
    # piyasa-nötr: hisse fade - XU100 intra hedge (pay vadelisi + F_XU030 hedge yaklaşığı)
    y = dd[dd.gap.abs() > 0.01]; rep(s, "fade, XU100 gün-içi hedge'li", -np.sign(y.gap) * (y.intra - y.x_intra) - C - 0.0003)
    # ham gap (temettü düzeltmesiz, trader'ın ekranda gördüğü)
    y = d[d.raw_gap.abs() > 0.01]; rep(s, "ham gap (log o/c_önceki) |>1%", -np.sign(y.raw_gap) * y.intra - C)
    # maliyet duyarlılığı
    gross = -np.sign(base.gap) * base.intra
    for cost in [0, 5, 8, 10, 15, 20, 30, 40, 50, 60]:
        rep(s, f"maliyet {cost} bps", gross - cost / 1e4)
R = pd.DataFrame(out); R.to_csv(OUT + "/res_e7_robust.csv", index=False)
pd.set_option("display.width", 300); print(R.round(2).to_string(index=False))
