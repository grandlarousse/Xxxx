import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
rows = []
for s in ["CIMSA", "OYAKC"]:
    d = daily(s)
    x = fade(d.gap, d.intra, 0.01, 10)
    IS = x[x.index <= IS_END]; OOS = x[x.index > IS_END]
    for lab, z in [("IS14-20", IS), ("IS16-20", IS[IS.index >= "2016"]), ("OOS21-26", OOS), ("ALL", x)]:
        r = summ(z, f"{s} {lab}"); rows.append(r)
    # yıllar
    yr = x.groupby(x.index.year).agg(["mean", "count"]).round(1)
    print(s, "yıllar:", dict(zip(yr.index, yr["mean"])), "pozitif:", (yr["mean"] > 0).sum(), "/", len(yr))
    # simetrik kırpma OOS
    for k in [5, 10, 20]:
        z = OOS.sort_values(); zz = z.iloc[k:-k].sort_index()
        rows.append(summ(zz, f"{s} OOS sym-trim {k}+{k}"))
        zz2 = z.iloc[:-k].sort_index()
        rows.append(summ(zz2, f"{s} OOS drop top{k} only"))
    # winsor 1/99 yüzdelik (getiri dağılımı tüm gün-içi üzerinden)
    q1, q99 = (d.intra * 1e4).quantile([0.01, 0.99])
    xw = fade(d.gap, d.intra.clip(q1 / 1e4, q99 / 1e4), 0.01, 10)
    rows.append(summ(xw[xw.index > IS_END], f"{s} OOS intra winsor1/99"))
    rows.append(summ(xw[xw.index <= IS_END], f"{s} IS intra winsor1/99"))
    # aylık toplam katkı yoğunlaşması
    mo = OOS.groupby(OOS.index.to_period("M")).sum().sort_values(ascending=False)
    print(s, "OOS toplam", round(OOS.sum()), "en iyi 3 ay:", mo.head(3).round(0).to_dict(), "en kötü 3:", mo.tail(3).round(0).to_dict())
    print(s, "OOS en iyi 10 işlem:", OOS.sort_values(ascending=False).head(10).round(0).to_dict())
R = pd.DataFrame(rows); print(R.to_string()); R.to_csv(OUT + "/res_b1.csv", index=False)
