"""Adım 1: tek değişkenli tarama (her öznitelik × h ∈ {1,3,5}), VİOP fwd_h hedefi; kayıt 'a8_univariate'.
Ayrıca en güçlü 12 öznitelik için spot panelde 2011–2016 erken dönem tekrarı ('a8_univariate_early') ve placebo_lead."""
from common import *
from features import build

clear_family(["a8_univariate", "a8_univariate_early"])
Xs, XV, info, s, d = build()
rows = []
for f in info.feature:
    for h in (1, 3, 5):
        st = split_stats(XV[f], d[f"fwd{h}"], h)
        register(AGENT, "a8_univariate", f"uni_{f}_h{h}", f, h, st, note=f"VİOP 2017-03..; grup={info.set_index('feature').group[f]}")
        rows.append(dict(feature=f, h=h, **{k: st[k] for k in ["ic", "t", "n", "ic_is", "t_is", "ic_oos", "t_oos", "yrs_same_sign", "yrs"]}))
U = pd.DataFrame(rows)
U["abs_t"] = U.t.abs()
U.sort_values("abs_t", ascending=False).to_csv(f"{OUT}/univariate_viop.csv", index=False)
print("tek değişkenli test sayısı:", len(U))
print("|t|>=2:", (U.abs_t >= 2).sum(), " |t|>=3:", (U.abs_t >= 3).sum(), " (şans beklentisi |t|>=2 ≈", round(0.0455 * len(U), 1), ")")
print("IS-OOS aynı işaret ve |t_oos|>=2:", ((np.sign(U.t_is) == np.sign(U.t_oos)) & (U.t_oos.abs() >= 2)).sum())
print(U.sort_values("abs_t", ascending=False).head(25).round(3).to_string())

# erken dönem tekrarı (spot 2011-2016, hedef sfwd_h), yalnızca set A öznitelikleri arasında en güçlü 12
A = set(info.loc[info.set == "A", "feature"])
top = U[U.feature.isin(A)].sort_values("abs_t", ascending=False).drop_duplicates("feature").head(12)
er = []
for _, r in top.iterrows():
    f, h = r.feature, int(r.h)
    x = Xs[f].loc["2011":"2016"]; y = s[f"sfwd{h}"].loc["2011":"2016"]
    st = ic(x, y, max(h, 5))
    reg = register(AGENT, "a8_univariate_early", f"uni_early_{f}_h{h}", f, h, dict(ic=st["ic"], t=st["t"], n=st["n"]), note="spot 2011-2016 sfwd")
    pl = placebo_lead(XV[f], d.v_ret, h)
    er.append(dict(feature=f, h=h, ic_viop=r.ic, t_viop=r.t, ic_early=st["ic"], t_early=st["t"], same_sign=np.sign(st["ic"]) == np.sign(r.ic), placebo=pl))
E = pd.DataFrame(er); E.to_csv(f"{OUT}/univariate_early_placebo.csv", index=False)
print(E.round(3).to_string())
