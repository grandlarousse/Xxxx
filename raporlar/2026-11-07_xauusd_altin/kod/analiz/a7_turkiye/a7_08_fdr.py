"""Ajan kaydı üzerinde BH-FDR (tüm testler ve yalnız XAUUSD hedefli testler)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
r = pd.read_csv(REGF)
r["q_all"] = np.nan; m = r.p.notna(); r.loc[m, "q_all"] = L.bh_fdr(r.loc[m, "p"])
nonx = r.family.eq("b_trgold") | r.test_id.str.startswith(("usdtry_component", "diag", "C1", "C3"))
x = r[~nonx & r.p.notna()].copy(); r["q_xau"] = np.nan; r.loc[x.index, "q_xau"] = L.bh_fdr(x.p)
r.to_csv(f"{OUT}/registry_with_fdr.csv", index=False)
print("toplam test:", len(r), "| aile:", r.family.value_counts().to_dict())
print("XAUUSD hedefli:", len(x), " p<0.05:", int((x.p < 0.05).sum()), " şans beklentisi:", round(0.05 * len(x), 1), " en küçük q_xau:", round(r.q_xau.min(), 3))
print("q_all<0.05 testler:"); print(r[r.q_all < 0.05][["family", "test_id", "h", "ic", "t", "t_is", "t_oos", "q_all"]].round(4).to_string())
