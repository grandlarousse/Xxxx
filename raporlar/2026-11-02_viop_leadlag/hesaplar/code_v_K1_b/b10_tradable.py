"""İşlenebilir pencere: yalnız VİOP pay vadelisinin listelendiği günler. 10:30 girişi, maliyet duyarlılığı, yıllar, XU030 hedge; spotta müzayede long-only alternatifi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet"); L = pd.read_csv(OUT + "/res_b9_listing.csv", parse_dates=["ilk"])
P = P.merge(L[["sym", "ilk"]], on="sym"); P["listed"] = P.date >= P.ilk
X = daily("XU030", is_index=True); hx = h1("XU030"); f = hx[hx.hm == 630].set_index("day")
X["m_r2"] = np.log(X.c / f.c.reindex(X.index)); P = P.merge(X[["m_r2"]], left_on="date", right_index=True, how="left")
P["sg"] = -np.sign(P.gap); sel = (P.gap.abs() > 0.01) & P.r2.notna()
out = []
for s in ["CIMSA", "OYAKC", "POOL_dusuk", "POOL_hepsi"]:
    df = P[P.listed & sel] if s.startswith("POOL") else P[(P.sym == s) & P.listed & sel]
    if s == "POOL_dusuk": df = df[df.liqT == "dusuk"]
    for cost in [8, 10, 15]:
        df = df.assign(_v=df.sg * df.r2 * 1e4 - cost)
        z = df.groupby("date")._v.mean(); m, t, n = nwt(z.values); out.append(dict(who=s, var=f"10:30 net{cost}", mean=round(m, 1), t=round(t, 2), n=n))
    df = df.assign(_v=df.sg * df.r2 * 1e4 - 10 - df.reltick)
    z = df.groupby("date")._v.mean(); m, t, n = nwt(z.values); out.append(dict(who=s, var="10:30 net10 + 1 tik", mean=round(m, 1), t=round(t, 2), n=n))
    df = df.assign(_v=df.sg * (df.r2 - df.m_r2) * 1e4 - 13)
    z = df.groupby("date")._v.mean(); m, t, n = nwt(z.values); out.append(dict(who=s, var="10:30 XU030 hedge (beta=1) net13", mean=round(m, 1), t=round(t, 2), n=n))
    df = df.assign(_v=df.sg * df.intra * 1e4 - 10)
    z = df.groupby("date")._v.mean(); m, t, n = nwt(z.values); out.append(dict(who=s, var="açılış (VİOP'ta imkansız) net10", mean=round(m, 1), t=round(t, 2), n=n))
    if not s.startswith("POOL"):
        df = df.assign(_v=df.sg * df.r2 * 1e4 - 10); yy = df.groupby(df.date.dt.year)._v.agg(["mean", "count"]).round(1)
        print(s, "10:30 net10 yıllar:", yy.to_dict("index"))
R = pd.DataFrame(out); print(R.to_string()); R.to_csv(OUT + "/res_b10_tradable.csv", index=False)
# Spot alternatifi: müzayedeye katılarak long-only (gap<-1%) -> kapanış. Tüm dönem, IS/OOS. Maliyet 10.
for s in ["CIMSA", "OYAKC"]:
    d = P[P.sym == s]
    for lab, cond in [("long (gap<-1%)", d.gap < -0.01), ("short (gap>+1%)", d.gap > 0.01)]:
        z = d[cond]
        for per, zz in [("IS", z[z.date <= IS_END]), ("OOS", z[z.date > IS_END])]:
            x = (zz.sg * zz.intra * 1e4 - 10).values; m, t, n = nwt(x); print(f"{s} spot müzayede {lab} {per}: {m:.1f} bps t {t:.2f} n {n}")
