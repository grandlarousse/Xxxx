"""Ortak faktör kontrolü: gap = beta*gap_XU030 + idio; fade idio işaretiyle; getiri XU030 ile hedge'li. 10:30 versiyonu XU030 hedge + 3 bps."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet")
X = daily("XU030", is_index=True)
hx = h1("XU030"); f = hx[hx.hm == 630].set_index("day")
X["p1030"] = f.c.reindex(X.index); X["r2"] = np.log(X.c / X.p1030)
# endeks h1 ilk bar açılışı önceki kapanış olabilir -> kullanılmıyor; sadece 10:30 kapanışı.
M = X[["gap", "intra", "r2"]].add_prefix("m_")
P = P.merge(M, left_on="date", right_index=True, how="left")
out = []
for s in ["CIMSA", "OYAKC"] + ["POOL_dusuk", "POOL_hepsi"]:
    if s.startswith("POOL"):
        df = P if s == "POOL_hepsi" else P[P.liqT == "dusuk"]
    else:
        df = P[P.sym == s]
    df = df.copy()
    # rolling beta (250g, t-1'e kadar) her hisse için
    parts = []
    for sym, z in df.groupby("sym"):
        z = z.sort_values("date").copy()
        cov = (z.cc * z.m_gap.add(z.m_intra)).rolling(250, min_periods=120).mean() - z.cc.rolling(250, min_periods=120).mean() * (z.m_gap + z.m_intra).rolling(250, min_periods=120).mean()
        var = (z.m_gap + z.m_intra).rolling(250, min_periods=120).var()
        z["beta"] = (cov / var).shift(1).clip(0, 2)
        parts.append(z)
    df = pd.concat(parts)
    df["idio_gap"] = df.gap - df.beta * df.m_gap
    df["h_intra"] = df.intra - df.beta * df.m_intra
    df["h_r2"] = df.r2 - df.beta * df.m_r2
    variants = {
        "ham: gap işareti, ham intra, 10bps": (-np.sign(df.gap) * df.intra * 1e4 - 10).where(df.gap.abs() > 0.01),
        "idio gap işareti (|idio|>1%), ham intra": (-np.sign(df.idio_gap) * df.intra * 1e4 - 10).where(df.idio_gap.abs() > 0.01),
        "idio gap işareti, XU030 hedge'li intra, 13bps": (-np.sign(df.idio_gap) * df.h_intra * 1e4 - 13).where(df.idio_gap.abs() > 0.01),
        "piyasa gap işareti (|beta*m_gap|>1%), ham intra": (-np.sign(df.m_gap) * df.intra * 1e4 - 10).where((df.beta * df.m_gap).abs() > 0.01),
        "10:30: ham": (-np.sign(df.gap) * df.r2 * 1e4 - 10).where((df.gap.abs() > 0.01) & df.r2.notna()),
        "10:30: ham gap, XU030 hedge'li, 13bps": (-np.sign(df.gap) * df.h_r2 * 1e4 - 13).where((df.gap.abs() > 0.01) & df.h_r2.notna()),
        "acilis: ham gap, XU030 hedge'li, 13bps": (-np.sign(df.gap) * df.h_intra * 1e4 - 13).where((df.gap.abs() > 0.01) & df.h_intra.notna()),
        "acilis h1-donemi: idio gap, hedge'li, 13bps": (-np.sign(df.idio_gap) * df.h_intra * 1e4 - 13).where((df.idio_gap.abs() > 0.01) & df.h_r2.notna()),
        "10:30: idio gap, XU030 hedge'li, 13bps": (-np.sign(df.idio_gap) * df.h_r2 * 1e4 - 13).where((df.idio_gap.abs() > 0.01) & df.h_r2.notna()),
    }
    for name, v in variants.items():
        df["_v"] = v
        for per, z in [("IS", df[df.date <= IS_END]), ("OOS", df[df.date > IS_END])]:
            if "10:30" in name and per == "IS": continue
            ser = z.groupby("date")._v.mean().dropna()
            m, t, n = nwt(ser.values); out.append(dict(who=s, var=name, per=per, mean=round(m, 1), t=round(t, 2), ndays=n))
R = pd.DataFrame(out); print(R.to_string()); R.to_csv(OUT + "/res_b6_factor.csv", index=False)
