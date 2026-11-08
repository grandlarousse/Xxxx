"""(g) Takvim sepeti ve madenci 5 gün düşüş kuralı için: komşu gün placebo, yıl-içi rastgele gün permütasyonu, global BH-FDR."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("g_")
MK = pd.read_pickle(f"{O}/c_masks.pkl"); F = pd.read_pickle(f"{O}/a_feats.pkl")
ix = pd.Series(IDX, index=IDX); ym = ix.dt.to_period("M"); pos_in_m = ix.groupby(ym).cumcount() + 1; pos_end = ix.groupby(ym).cumcount(ascending=False) + 1
rng = np.random.default_rng(7)
out = []
basket = MK["pre_hol"] | MK["first"]
neigh = {"sepet": basket, "ayin_2._gunu": pos_in_m == 2, "ayin_3._gunu": pos_in_m == 3, "ayin_son_gunu": pos_end == 1, "ayin_sondan_2.": pos_end == 2,
         "tatil_oncesi_-1_gun": MK["pre_hol"].shift(-1).fillna(False).astype(bool), "tatil_sonrasi": MK["pre_hol"].shift(1).fillna(False).astype(bool)}
for t in ["GDXJ", "GDX", "GLD", "SLV"]:
    r = R[t]
    for nm, m in neigh.items():
        q = r[m.reindex(r.index).fillna(False) & r.notna()]
        out.append(dict(etf=t, gun=nm, n=len(q), ort_bps=round(q.mean() * 1e4, 1), ort_oos_bps=round(q[q.index > IS_END].mean() * 1e4, 1), tum_gun_ort_bps=round(r.mean() * 1e4, 1)))
P = pd.DataFrame(out); P.to_csv(f"{O}/g_komsu_gun_placebo.csv", index=False); print(P.to_string())
# Permütasyon: her yıl içinde aynı sayıda rastgele gün -> ortalama getiri dağılımı
pr = []
for t, nm, m in [("GDXJ", "sepet", basket), ("GDX", "sepet", basket), ("GDXJ", "ilk_gun", MK["first"]), ("GDX", "tatil_oncesi", MK["pre_hol"]), ("GDXJ", "tatil_oncesi", MK["pre_hol"])]:
    r = R[t].dropna(); mm = m.reindex(r.index).fillna(False)
    obs = r[mm].mean(); yrs = r.index.year; cnt = mm.groupby(yrs).sum()
    pos_by_y = {y: np.where(yrs == y)[0] for y in cnt.index}
    sims = np.empty(5000)
    for i in range(5000):
        idx = np.concatenate([rng.choice(pos_by_y[y], int(c), replace=False) for y, c in cnt.items() if c > 0])
        sims[i] = r.values[idx].mean()
    p = (np.sum(sims >= obs) + 1) / (len(sims) + 1)
    pr.append(dict(etf=t, kural=nm, gozlenen_bps=round(obs * 1e4, 1), perm_ort_bps=round(sims.mean() * 1e4, 1), perm_95_bps=round(np.quantile(sims, 0.95) * 1e4, 1), p_tek_yonlu=round(p, 4)))
PR = pd.DataFrame(pr); PR.to_csv(f"{O}/g_permutasyon.csv", index=False); print(PR.to_string())
# Global BH-FDR (bu ajanın tüm kayıtları)
reg_ = pd.read_csv(f"{lib_altin.REG_DIR}/{AGENT}.csv")
reg_["q_bh"] = bh_fdr(reg_.p.fillna(1).values)
reg_.to_csv(f"{O}/kayit_fdr.csv", index=False)
print("toplam kayıtlı test:", len(reg_), " aile sayısı:", reg_.family.nunique())
print(reg_.sort_values("p").head(25)[["family", "test_id", "t", "t_is", "t_oos", "p", "q_bh"]].to_string())
# Öngörücü/kural testleri üzerinde FDR (betimsel aşınma/ortalama testleri ve f_final yinelemeleri hariç)
pred = reg_[~reg_.family.isin(["d_drag", "d_volregime", "b_mean", "f_final"])].copy()
pred["q_pred"] = bh_fdr(pred.p.fillna(1).values); pred.to_csv(f"{O}/kayit_fdr_ongorucu.csv", index=False)
print("öngörücü test:", len(pred), "|t|>=2:", int((pred.t.abs() >= 2).sum()), "beklenen~", round(0.0455 * pred.t.notna().sum()), "|t|>=3:", int((pred.t.abs() >= 3).sum()),
      "beklenen~", round(0.0027 * pred.t.notna().sum(), 1), "min q:", round(pred.q_pred.min(), 3))
