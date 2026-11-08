"""Adım 9: tek değişkenli taramanın öne çıkan 6 sinyali için spot panelde 2011–2026 uzun örneklem testi (hedef sfwd_h, 15:00→15:00 spot).
VİOP örneklemiyle örtüşür (bağımsız değil); 2011–2016 kısmı bağımsız erken dönemdir. Kayıt 'a8_univariate_longspot'."""
from common import *
from features import build
clear_family(["a8_univariate_longspot"])
Xs, XV, info, s, d = build()
rows = []
for f in ["rt_nom2_d5", "rt_curve_2s10s_d5", "xa_gdx_rel1", "seg_last1h", "xa_aud_d5", "cot_mm_z52"]:
    for h in (1, 3, 5):
        x = Xs[f].loc["2011":]; y = s[f"sfwd{h}"].loc["2011":]
        st = ic(x, y, max(h, 5)); e = ic(x.loc[:"2016"], y.loc[:"2016"], max(h, 5)); l = ic(x.loc["2017":], y.loc["2017":], max(h, 5))
        dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna(); yr = dd.groupby(dd.index.year).apply(lambda g: g.x.corr(g.y, method="spearman"))
        same = int((np.sign(yr) == np.sign(st["ic"])).sum())
        register(AGENT, "a8_univariate_longspot", f"long_{f}_h{h}", f, h, dict(ic=st["ic"], t=st["t"], n=st["n"], t_is=e["t"], t_oos=l["t"], yrs_same_sign=same, yrs=int(yr.notna().sum())), note="spot 2011-2026; t_is=2011-16, t_oos=2017-26")
        rows.append(dict(feature=f, h=h, ic=st["ic"], t=st["t"], ic_2011_16=e["ic"], t_2011_16=e["t"], ic_2017_26=l["ic"], t_2017_26=l["t"], yrs=f"{same}/{int(yr.notna().sum())}"))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/longspot.csv", index=False); print(R.round(3).to_string(index=False))
