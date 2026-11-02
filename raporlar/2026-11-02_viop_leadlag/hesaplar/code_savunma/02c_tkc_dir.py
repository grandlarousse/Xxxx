"""02c: Yön kontrolü: TKC post-close hareketi TCELL'in o günkü hareketini mi takip ediyor (TKC takipçi), yoksa bilgi mi?
TKC_post_t ~ TCELL cc_t / son saat_t ; TKC_post_t -> TKC ertesi gün (15:30_{t+1}/kapanış_t) geri dönüş."""
from sv import *
X = pd.read_parquet(RES + "/02b_h1.parquet")
d = ll.decomp("TCELL"); cal = X.index
tc = ll.raw("TCELL.IS"); cl = pd.Series(tc["c"].values, index=pd.DatetimeIndex(tc["ldate"].values)); cl = cl[~cl.index.duplicated(keep="last")]
s1430 = ll.snap_daily("TCELL.IS", "14:30")
X["tc_cc"] = d["cc"].reindex(cal); X["tc_last"] = np.log(cl / s1430.reindex(cl.index)).reindex(cal)
tkd = ll.raw("TKC"); tkc = pd.Series(tkd["c"].values, index=pd.DatetimeIndex(tkd["ldate"].values)); tkc = tkc[~tkc.index.duplicated(keep="last")]
tk1530 = ll.snap_daily("TKC", "15:30")
X["tk_on1"] = (np.log(tk1530.reindex(cal).shift(-1) / tkc.reindex(cal)))  # TKC kapanış_t -> 15:30_{t+1}
X["tk_full"] = np.log(tkc.reindex(cal) / tkc.reindex(cal).shift(1))
for y, xv in [("tk_post", "tc_cc"), ("tk_post", "tc_last"), ("tk_on1", "tk_post"), ("TCELL_gap1", "tk_on1")]:
    z = X[[y, xv]].dropna(); z = z[(z.abs() < 0.12).all(axis=1)]
    b, t, n = ll.nw_t(z[y], z[xv]); print(f"{y} ~ {xv}: corr {z.corr().iloc[0,1]:.3f} beta {b:.3f} t {t:.2f} n {n}")
# TKC kapanışı -> ertesi gün TKC 15:30 dönüşü ile TCELL gap+ilk saat eşzamanlı (ikisi de ertesi sabah) — ortak fiyatlama
z = X[["tk_on1", "TCELL_gap1", "TCELL_fh1"]].dropna(); print("corr tk_on1 vs TCELL gap1:", round(z.tk_on1.corr(z.TCELL_gap1), 3), " vs gap1+fh1:", round(z.tk_on1.corr(z.TCELL_gap1 + z.TCELL_fh1), 3))
