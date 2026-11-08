from adv_lib import *
from scipy import stats as ss
R=pd.read_csv(f"{S}/out/registry/a5_esz_artik.csv"); print("rows",len(R), R.family.value_counts().to_dict())
R["p"]=2*(1-ss.norm.cdf(R.t.abs()))
ok=R.p.notna(); R.loc[ok,"q_bh"]=bh_fdr(R.p[ok]); R["p_bonf"]=(R.p*ok.sum()).clip(upper=1)
print("n valid",ok.sum()," min q",R.q_bh.min().round(4), " n q<0.05",(R.q_bh<0.05).sum(), " n q<0.10",(R.q_bh<0.10).sum(), " Bonf<0.05",(R.p_bonf<0.05).sum())
print("expected |t|>2 frac", round((R.t.abs()>1.96).mean(),3))
keys=["C_I12c_MACRO3_W60_h3","C_I07_MACRO3_W60_h1","B_GSRD_k5_h1","C_I12_MACRO3_W60_h1","A_EURUSD_W60_k1_h1","B_GSRZ_L120_h5","X_C1_q90_h3","X_C1_q70_h3"]
print(R[R.test_id.isin(keys)][["test_id","family","t","p","q_bh","p_bonf","t_is","t_oos"]].round(4).to_string())
print(R.sort_values("p").head(15)[["test_id","family","t","p","q_bh","t_is","t_oos"]].round(4).to_string())
# BH within VIOP-only primary grid families (A_resid,A_fitted,A_own,B_ratio,C_intraday,E)
prim=R[R.family.isin(["A_resid","A_fitted","A_own","B_ratio","C_intraday","E_viop_close"])].copy()
prim["q"]=bh_fdr(prim.p.values); print("primary VIOP grid n",len(prim)," min q",prim.q.min().round(3)); print(prim.sort_values("p").head(5)[["test_id","t","p","q"]].round(4).to_string())
C=R[R.family=="C_intraday"].copy(); C["q"]=bh_fdr(C.p.values); print("C family n",len(C)); print(C.sort_values("p").head(6)[["test_id","t","p","q"]].round(4).to_string())
# OOS-only test of IS selections: 18 selections -> max OOS t
sel=pd.read_csv(f"{S}/out/a5_esz_artik/is_selection.csv"); print(sel.to_string())
