"""Çoklu test, IS->OOS replikasyon ve kaydırılmış/karıştırılmış sürücü ile null dağılımı.
Çıktı: cache/fdr_summary.csv, cache/null_summary.csv, cache/replication.csv
"""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
import matrix as MX

FAMS = ["sync", "sync_usd", "pc_xu", "pc_xt", "pc_glob", "gap_l1", "intra_l1", "intra_l0", "cum25", "rev"]
nV = len(VIOP)
dm = pd.read_parquet(os.path.join(CACHE, "driver_meta.parquet"))
clean = (~dm["sparse"] & ~dm["mirror"]).values

def summarize(res, label, subset=None):
    out = []
    for f in FAMS:
        if (f, "full") not in res: continue
        c, n, t, b = res[(f, "full")]
        t = t[:nV]; c = c[:nV]
        if subset is not None: t = t[:, subset]; c = c[:, subset]
        p = p_from_t(t).ravel(); ok = ~np.isnan(p)
        r05, _ = bh(p, 0.05); r01, _ = bh(p, 0.01)
        row = {"label": label, "fam": f, "n_tests": int(ok.sum()), "p<0.05": int((p[ok] < 0.05).sum()), "p<0.001": int((p[ok] < 0.001).sum()),
               "bh05": int(r05.sum()), "bh01": int(r01.sum()), "exp_p05": round(0.05 * ok.sum(), 1)}
        # replikasyon: IS BH05 -> OOS aynı işaret & p<0.05
        if (f, "is") in res and (f, "oos") in res:
            ci, _, ti, _ = res[(f, "is")]; co, _, to, _ = res[(f, "oos")]
            ti = ti[:nV]; to = to[:nV]
            if subset is not None: ti = ti[:, subset]; to = to[:, subset]
            pi = p_from_t(ti).ravel(); po = p_from_t(to).ravel()
            disc, _ = bh(pi, 0.05)
            rep = disc & (np.sign(ti.ravel()) == np.sign(to.ravel())) & (po < 0.05)
            same = disc & (np.sign(ti.ravel()) == np.sign(to.ravel()))
            row.update({"is_bh05": int(disc.sum()), "oos_rep": int(rep.sum()), "rep_rate": round(rep.sum() / disc.sum(), 3) if disc.sum() else np.nan,
                        "same_sign_rate": round(same.sum() / disc.sum(), 3) if disc.sum() else np.nan})
            # top-200 IS |t| (BH'den bağımsız) replikasyon
            ok2 = ~np.isnan(pi) & ~np.isnan(po); order = np.argsort(pi[ok2])[:200]
            tis = ti.ravel()[ok2][order]; tos = to.ravel()[ok2][order]; pos_ = po[ok2][order]
            row["top200_rep_rate"] = round(float(((np.sign(tis) == np.sign(tos)) & (pos_ < 0.05)).mean()), 3)
        out.append(row)
    return out

if __name__ == "__main__":
    Xv = MX.X.values
    real = MX.run(Xv, wins=["full", "is", "oos"])
    rows = summarize(real, "GERCEK") + summarize(real, "GERCEK_temiz", clean)
    pd.DataFrame(rows).to_csv(os.path.join(CACHE, "fdr_summary.csv"), index=False)
    nul = []
    rng = np.random.default_rng(7)
    for S in [37, 71, 113, 173, 251, 409]:
        r = MX.run(MX.shifted(Xv, S), wins=["full", "is", "oos"]); nul += summarize(r, f"shift{S}")
    for k in range(3):
        perm = rng.permutation(len(Xv)); r = MX.run(Xv[perm], wins=["full", "is", "oos"]); nul += summarize(r, f"perm{k}")
    N = pd.DataFrame(nul); N.to_csv(os.path.join(CACHE, "null_summary.csv"), index=False)
    R = pd.DataFrame(rows)
    print(R[["label", "fam", "n_tests", "p<0.05", "bh05", "bh01", "is_bh05", "rep_rate", "top200_rep_rate"]].to_string(index=False))
    g = N.assign(kind=N.label.str.extract(r"^(shift|perm)")[0]).groupby(["kind", "fam"])[["p<0.05", "p<0.001", "bh05", "bh01", "is_bh05", "top200_rep_rate"]].mean().round(2)
    print(g.to_string())
