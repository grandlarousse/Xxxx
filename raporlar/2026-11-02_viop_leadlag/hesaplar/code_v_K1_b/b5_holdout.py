"""Seçim hattının dürüst holdout testi: hisseleri 2016-01..2023-11 açılış-girişli fade sonucuna göre seç, 2023-12+ 10:30 girişte değerlendir."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
from scipy import stats
P = pd.read_parquet(OUT + "/panel_b.parquet")
P["sg"] = -np.sign(P.gap); sel = P.gap.abs() > 0.01
P["pnl_open"] = (P.sg * P.intra * 1e4 - 10).where(sel)
P["pnl_1030"] = (P.sg * P.r2 * 1e4 - 10).where(sel & P.r2.notna())
P["pnl_open_h1"] = P.pnl_open.where(P.r2.notna())
pre = P[(P.date >= "2016-01-01") & (P.date < "2023-11-30")]; post = P[P.date >= "2023-11-30"]
rows = []
for s in VIOP:
    a = pre[pre.sym == s].sort_values("date").pnl_open.dropna(); b = post[post.sym == s].sort_values("date").pnl_1030.dropna(); c = post[post.sym == s].sort_values("date").pnl_open_h1.dropna()
    ma, ta, na = nwt(a.values); mb, tb, nb = nwt(b.values); mc, tc, nc = nwt(c.values)
    rows.append(dict(sym=s, pre_open=ma, pre_t=ta, pre_n=na, post_1030=mb, post_t=tb, post_n=nb, post_open=mc, post_open_t=tc))
R = pd.DataFrame(rows).round(2)
print("pre t sırası (ilk 10):"); print(R.sort_values("pre_t", ascending=False).head(10).to_string())
print("Spearman(pre_t, post_1030):", round(stats.spearmanr(R.pre_t, R.post_1030, nan_policy='omit')[0], 3), " p", round(stats.spearmanr(R.pre_t, R.post_1030, nan_policy='omit')[1], 3))
print("Spearman(pre_t, post_open):", round(stats.spearmanr(R.pre_t, R.post_open, nan_policy='omit')[0], 3), " p", round(stats.spearmanr(R.pre_t, R.post_open, nan_policy='omit')[1], 3))
print("CIMSA pre sırası:", int(R.pre_t.rank(ascending=False)[R.sym == "CIMSA"].iloc[0]), " OYAKC:", int(R.pre_t.rank(ascending=False)[R.sym == "OYAKC"].iloc[0]))
for k in [3, 5, 10, 15]:
    top = R.sort_values("pre_t", ascending=False).head(k).sym.tolist()
    z = post[post.sym.isin(top)].groupby("date").pnl_1030.mean().dropna(); m, t, n = nwt(z.values)
    z2 = post[post.sym.isin(top)].groupby("date").pnl_open_h1.mean().dropna(); m2, t2, n2 = nwt(z2.values)
    print(f"üst {k} (pre'ye göre) -> post 10:30 portföy: {m:.1f} bps (t {t:.2f}, {n} gün) | post açılış: {m2:.1f} (t {t2:.2f})  {top}")
# ex-ante likidite kuralı: pre dönemde düşük tercil işe yaradı mı, post'ta 10:30'da?
for lab, df, col in [("pre düşük tercil açılış", pre, "pnl_open"), ("post düşük tercil 10:30", post, "pnl_1030"), ("post düşük tercil açılış", post, "pnl_open_h1")]:
    z = df[df.liqT == "dusuk"].groupby("date")[col].mean().dropna(); m, t, n = nwt(z.values); print(lab, round(m, 1), round(t, 2), n)
R.to_csv(OUT + "/res_b5_holdout.csv", index=False)
