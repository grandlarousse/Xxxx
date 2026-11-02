"""THYAO_{t-1} -> XU030 gün-içi_t sağlamlık: makro/uluslararası kontroller (ES, BZ, USDTRY, XU030 gap_t), 2014+ örneklem, yarıyıllar, placebo (diğer 46 hisse)."""
from ye_common import *
x30 = idx_ret("XU030")
y = ll.raw("XU030.IS"); y.index = pd.DatetimeIndex(y["ldate"]); y = y[~y.index.duplicated(keep="last")]
o = y["o"].reindex(x30.index); c_ = idx_px("XU030"); intra30 = np.log(c_ / o); bad = (o <= 0) | (np.abs(np.log(o / c_.shift(1))) < 1e-7); intra30[bad] = np.nan; gap30 = x30 - intra30
th = stk_ret("THYAO"); es = ll.ret("ES=F"); bz = ll.ret("BZ=F"); fx = ll.ret("TRY=X")
def run(ctrls, lab, a=START, b=END, lead=th):
    df = pd.concat([intra30.rename("y"), lead.shift(1).rename("x")] + [c.rename(f"c{i}") for i, c in enumerate(ctrls)], axis=1)
    df = df[(df.index >= a) & (df.index <= b)].dropna(); Z = (df - df.mean()) / df.std()
    bb, tt, n, _ = ols_nw(Z.y.values, Z.drop(columns="y").values); return {"model": lab, "b": bb[1], "t": tt[1], "n": n}
R = [run([x30.shift(1)], "XU030_{t-1}"), run([x30.shift(1), es.shift(1), bz.shift(1), fx.shift(1)], "+ES,BZ,USDTRY_{t-1}"),
     run([x30.shift(1), es.shift(1), bz.shift(1), fx.shift(1), gap30], "+ XU030 gap_t (açılışta bilinen)"),
     run([x30.shift(1), es, bz, fx], "+ES,BZ,USDTRY_t (senkron, look-ahead; sadece teşhis)")]
for a, b in [("2014-01-01", "2017-06-30"), ("2017-07-01", "2020-12-31"), ("2021-01-01", "2023-06-30"), ("2023-07-01", "2026-10-30")]:
    R.append(run([x30.shift(1)], f"alt dönem {a[:7]}..{b[:7]}", pd.Timestamp(a), pd.Timestamp(b)))
pl = []
for s in VIOP:
    r = run([x30.shift(1)], s, lead=stk_ret(s)); pl.append(r)
P = pd.DataFrame(pl).sort_values("t"); R = pd.DataFrame(R)
pd.set_option("display.width", 200); print(R.round(3).to_string()); print("PLACEBO/kesit: 47 hissenin hisse_{t-1} -> XU030 gün-içi_t (XU030_{t-1} kontrollü):"); print(P.round(2).to_string(index=False))
print("|t|>3:", (P.t.abs() > 3).sum(), " BH-FDR geçen:", ll.fdr(ll.t_to_p(P.t.values))[0].sum())
R.to_csv(RES + "/thyao_robust.csv", index=False); P.to_csv(RES + "/stock_lead_xu030_intra.csv", index=False)
