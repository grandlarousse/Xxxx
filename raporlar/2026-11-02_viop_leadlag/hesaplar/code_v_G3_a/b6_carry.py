"""B6: Spot gece getirisinin ne kadarı TL faiz taşıma (carry) ? Vadeli = fazla getiri (excess return) enstrümanı.
carry_gün = ln(UZL_{T-1}/SPOT_{T-1}) / kalan gün (takvim). Beklenti: s_gap - f_gap ≈ carry_gün × gece takvim günü (1 / Pazartesi 3).
Ayrıca s_intra - f_intra (gün-içi baz değişimi)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
import warnings; warnings.filterwarnings("ignore")
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)
Z = pd.read_parquet(R + "/b5_XU030_panel.parquet")
Z = Z[Z.index >= "2020-08-01"]  # 2020 temmuz endeks/vadeli birim değişimi sonrası baz seviyesi anlamlı
Z["carry_d"] = (Z.basis_c / Z.days_to_exp.clip(lower=1)).shift(1)
Z["cal"] = pd.Series(Z.index, index=Z.index).diff().dt.days
Z["exp_carry"] = Z.carry_d * Z.cal
Z["d_gap"] = Z.gap - Z.f_gap; Z["d_intra"] = Z.intra - Z.f_intra
q = Z.dropna(subset=["d_gap", "exp_carry", "d_intra"])
q = q[(q.basis_c.abs() < 0.2)]
print("n", len(q))
print("ort (bps): s_gap", round(1e4*q.gap.mean(), 1), " f_gap", round(1e4*q.f_gap.mean(), 1), " fark", round(1e4*q.d_gap.mean(), 1), " beklenen carry", round(1e4*q.exp_carry.mean(), 1))
print("ort (bps): s_intra", round(1e4*q.intra.mean(), 1), " f_intra", round(1e4*q.f_intra.mean(), 1), " fark", round(1e4*q.d_intra.mean(), 1))
print("yıllık:"); print((1e4*q.groupby(q.index.year)[["gap", "f_gap", "d_gap", "exp_carry", "intra", "f_intra", "d_intra"]].mean()).round(1).to_string())
print("takvim günü (1=hafta içi, 3=Pzt):"); print((1e4*q.groupby(q.cal.clip(upper=4))[["gap", "f_gap", "d_gap", "exp_carry"]].mean()).round(1).assign(n=q.groupby(q.cal.clip(upper=4)).size()).to_string())
# regresyon d_gap ~ exp_carry
import numpy.linalg as la
A = np.c_[np.ones(len(q)), q.exp_carry]; b = la.lstsq(A, q.d_gap, rcond=None)[0]; e = q.d_gap - A @ b; se = np.sqrt(np.diag(la.inv(A.T @ A)) * e.var())
print("d_gap = a + b*exp_carry: a", round(1e4*b[0], 2), "bps (t", round(b[0]/se[0], 2), ") b", round(b[1], 2), "(t", round(b[1]/se[1], 1), ")")
print("f_gap (fazla gece getirisi) yıllık pozitif mi:", (q.groupby(q.index.year).f_gap.mean() > 0).to_dict())
