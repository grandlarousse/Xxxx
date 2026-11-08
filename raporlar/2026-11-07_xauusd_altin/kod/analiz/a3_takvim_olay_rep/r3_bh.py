"""BH q yeniden hesabı: analistin 178 yön testinin p'leri (kayıttan), kendi BH uygulamam; düzeltilmiş BAYRAM t'si ve NFP işaret-kuralı t'siyle duyarlılık."""
import pandas as pd, numpy as np
from scipy import stats
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
R = pd.read_csv(f"{S}/out/a3_takvim_olay/registry_with_q.csv")
R = R[R.family != "oynaklik"].copy(); print("yön testi:", len(R))
def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]; return np.clip(q, 0, 1)
R["p2"] = 2 * stats.norm.sf(R.t.abs())
R["q_mine"] = bh(R.p2.fillna(1))
ids = ["QEND_TDE1_h3", "NFP_cond_spot12to15_h1", "NFP_cond_spot12to15_h3", "OG_OEday_h1", "BAYRAM_post_h5", "MONTH_Oca_h1"]
print(R[R.test_id.isin(ids)][["test_id", "t", "q", "q_mine"]].round(3).to_string())
# duyarlılık: BAYRAM t=-2.94 (sahte olay çıkarılmış), NFP h1/h3 işaret kuralı t (2.42 / 2.51)
R2 = R.copy()
for tid, t in [("BAYRAM_post_h5", -2.94), ("NFP_cond_spot12to15_h1", 2.42), ("NFP_cond_spot12to15_h3", 2.51)]:
    R2.loc[R2.test_id == tid, "t"] = t
R2["p2"] = 2 * stats.norm.sf(R2.t.abs()); R2["q_adj"] = bh(R2.p2.fillna(1))
print("düzeltilmiş t'lerle:\n", R2[R2.test_id.isin(ids)][["test_id", "t", "q_adj"]].round(3).to_string())
print("|t|>=2:", int((R.t.abs() >= 2).sum()), " |t|>=3:", int((R.t.abs() >= 3).sum()), " beklenen (178×0.0455, ×0.0027):", round(178 * 0.0455, 1), round(178 * 0.0027, 2))
