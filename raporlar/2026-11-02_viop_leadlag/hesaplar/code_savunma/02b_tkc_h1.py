"""02b: Saatlik TKC post-BIST-kapanış hareketi -> TCELL/TTKOM ertesi gün gap / ilk saat / gün-içi.
Zaman: TKC snap 15:30 UTC (BIST kapanışından 20-30 dk sonra; kışın ABD 14:30'da açıldığı için 15:00 snap yok).
TKC kapanışı = günlük 'c' (20:00/21:00 UTC). Kur post-close = TRY=X snap(21:00)/snap(15:00).
"""
from sv import *
cal = ll.bist_cal()
def snap(sym, hh): return ll.snap_daily(sym, hh)
tk_post_start = snap("TKC", "15:30")
tkd = ll.raw("TKC"); tk_close = pd.Series(tkd["c"].values, index=pd.DatetimeIndex(tkd["ldate"].values))
tk_close = tk_close[~tk_close.index.duplicated(keep="last")]
es15 = snap("ES=F", "15:00"); es_end = snap("ES=F", "21:00")
fx15 = snap("TRY=X", "15:00"); fx21 = snap("TRY=X", "21:00")
tur15 = snap("TUR", "15:30"); turd = ll.raw("TUR"); tur_close = pd.Series(turd["c"].values, index=pd.DatetimeIndex(turd["ldate"].values)); tur_close = tur_close[~tur_close.index.duplicated(keep="last")]
X = pd.DataFrame({"tk_post": np.log(tk_close / tk_post_start), "es_post": np.log(es_end / es15), "fx_post": np.log(fx21 / fx15),
                  "tur_post": np.log(tur_close / tur15)})
X = X.reindex(cal); X = X[X.index >= "2023-12-05"]
for st in ["TCELL", "TTKOM", "ASELS"]:
    d = ll.decomp(st)
    o1 = ll.snap_daily(st + ".IS", "07:30")  # ilk saat barı (06:30-07:30) kapanışı
    dr = ll.raw(st + ".IS"); op = pd.Series(dr["o"].values, index=pd.DatetimeIndex(dr["ldate"].values)); cl = pd.Series(dr["c"].values, index=pd.DatetimeIndex(dr["ldate"].values))
    op = op[~op.index.duplicated(keep="last")]; cl = cl[~cl.index.duplicated(keep="last")]
    fh = np.log(o1.reindex(op.index) / op); rest = np.log(cl / o1.reindex(cl.index))
    X[st + "_gap1"] = d["gap"].shift(-1).reindex(X.index)
    X[st + "_intra1"] = d["intra"].shift(-1).reindex(X.index)
    X[st + "_fh1"] = fh.reindex(cal).shift(-1).reindex(X.index)
    X[st + "_rest1"] = rest.reindex(cal).shift(-1).reindex(X.index)
X["tl_post"] = X.tk_post + X.fx_post.fillna(0)
X.to_parquet(RES + "/02b_h1.parquet")
rows = []
for st in ["TCELL", "TTKOM", "ASELS"]:
    for y in ["gap1", "fh1", "rest1", "intra1"]:
        for xv in ["tk_post", "tl_post", "es_post", "tur_post"]:
            z = X[[st + "_" + y, xv]].dropna(); z = z[z[xv].abs() < 0.1]
            b, t, n = ll.nw_t(z.iloc[:, 0], z[xv]); rows.append((st, y, xv, round(z.corr().iloc[0, 1], 3), round(b, 3), round(t, 2), n))
A = pd.DataFrame(rows, columns=["stock", "y", "x", "corr", "beta", "t", "n"]); A.to_csv(RES + "/02b_h1_uni.csv", index=False)
print(A[A.x.isin(["tk_post", "tl_post", "es_post"])].to_string(index=False))
# çoklu: gap1 ~ tk_post + es_post (TKC ABD piyasasının ötesinde bilgi taşıyor mu)
import statsmodels.api as sm
for st in ["TCELL", "TTKOM"]:
    z = X[[st + "_gap1", "tk_post", "es_post", "fx_post"]].dropna(); z = z[z.tk_post.abs() < 0.1]
    m = sm.OLS(z.iloc[:, 0], sm.add_constant(z[["tk_post", "es_post", "fx_post"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(st, "gap1 ~ tk_post+es_post+fx_post: b", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict(), "R2", round(m.rsquared, 3), "n", len(z))
    z = X[[st + "_intra1", st + "_gap1", "tk_post"]].dropna(); z = z[z.tk_post.abs() < 0.1]
    z["U"] = z.tk_post - z[st + "_gap1"]
    m = sm.OLS(z[st + "_intra1"], sm.add_constant(z[["tk_post", st + "_gap1"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(st, "intra1 ~ tk_post + gap1: b", m.params.round(3).to_dict(), "t", m.tvalues.round(2).to_dict())
print("sd tk_post bps", round(1e4 * X.tk_post.std(), 1), " sd TCELL gap bps", round(1e4 * X.TCELL_gap1.std(), 1), "n", X.tk_post.notna().sum())
