from ye_common import *
A = pd.read_csv(RES + "/lead_idx_to_stock.csv"); B = pd.read_csv(RES + "/lead_stock_to_idx.csv"); C = pd.read_csv(RES + "/lead_idx_to_idx.csv"); N = pd.read_csv(RES + "/lead_null.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
def fdr_df(df, col="t_full"):
    p = ll.t_to_p(df[col].values); rej, padj = ll.fdr(p); df = df.copy(); df["p"] = p; df["q"] = padj; df["fdr"] = rej
    df["rep"] = (np.sign(df.t_IS) == np.sign(df.t_OOS)) & (df.t_IS.abs() > 2) & (df.t_OOS.abs() > 2); return df
print("NULL |t|>3 oranı:", (N.t.abs() > 3).mean().round(4), "|t|>2:", (N.t.abs() > 2).mean().round(4), "n=", len(N))
for tgt in ["cc", "gap", "intra"]:
    a = fdr_df(A[(A["var"] == "raw") & (A.target == tgt)])
    print(f"\n=== A {tgt}: testler {len(a)}, |t|>3 oranı {(a.t_full.abs()>3).mean():.3f}, FDR geçen {a.fdr.sum()}, IS&OOS replikasyon {a.rep.sum()}, FDR&rep {(a.fdr & a.rep).sum()}")
    g = a.groupby("idx").agg(med_b=("b_full", "median"), frac_pos=("b_full", lambda x: (x > 0).mean()), n_fdr=("fdr", "sum"), n_rep=("rep", "sum"), med_bOOS=("b_OOS", "median"))
    print(g.sort_values("n_fdr", ascending=False).head(15).round(3).to_string())
    a.to_csv(RES + f"/A_{tgt}_fdr.csv", index=False)
    print(a[a.fdr & a.rep].sort_values("t_full", key=abs, ascending=False).head(25)[["stock", "idx", "w", "b_full", "t_full", "b_IS", "t_IS", "b_OOS", "t_OOS"]].round(3).to_string())
# ex vs raw karşılaştırması
for tgt in ["cc", "gap", "intra"]:
    x = A[A.target == tgt].pivot_table(index=["stock", "idx"], columns="var", values="b_full").dropna()
    print(tgt, "raw vs ex (hisse-hariç) ortalama b:", x.mean().round(4).to_dict(), "fark medyan", (x.raw - x.ex).median().round(4))
b = fdr_df(B); print(f"\n=== B hisse->endeks: {len(b)} test, FDR {b.fdr.sum()}, rep {b.rep.sum()}")
print(b[b.fdr].sort_values("t_full", key=abs, ascending=False).head(25)[["stock", "idx", "b_full", "t_full", "t_IS", "t_OOS"]].round(3).to_string())
b.to_csv(RES + "/B_fdr.csv", index=False)
c = fdr_df(C); print(f"\n=== C endeks->endeks: {len(c)} test, FDR {c.fdr.sum()}, rep {c.rep.sum()}, FDR&rep {(c.fdr & c.rep).sum()}")
print(c[c.fdr & c.rep].sort_values("t_full", key=abs, ascending=False).head(40)[["leader", "follower", "b_full", "t_full", "b_IS", "t_IS", "b_OOS", "t_OOS"]].round(3).to_string())
c.to_csv(RES + "/C_fdr.csv", index=False)
