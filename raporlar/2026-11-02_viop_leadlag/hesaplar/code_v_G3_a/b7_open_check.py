"""B7: VİOP ACILIS ve Yahoo spot açılışının tutarlılığı, yıllara göre. ABD (^GSPC) T-1 getirisi BIST kapanışından sonra kapanır ->
gerçek bir açılış fiyatı bu bilgiyi İÇERMELİ: corr(gap, spx_{T-1}) yüksek, corr(intra, spx_{T-1}) ~0.
Ayrıca basis_open - basis_close (= ln(Fo/So) - ln(Fc/Sc)): Yahoo spot açılışı ile vadeli açılışı arasındaki sapma."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
import warnings; warnings.filterwarnings("ignore")
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)
Z = pd.read_parquet(R + "/b5_XU030_panel.parquet")
spx = daily("^GSPC")["c"]; r = np.log(spx / spx.shift(1))
# BIST günü T için 'son ABD kapanışı' = T'den önceki en son ABD işlem günü
us = r.dropna(); idx = us.index.searchsorted(Z.index) - 1
Z["spx_prev"] = [us.iloc[i] if i >= 0 else np.nan for i in idx]
Z["dbo"] = (np.log(np.exp(Z.f_gap)) - Z.gap)  # f_gap - s_gap
rows = []
for y, g in Z.groupby(Z.index.year):
    g = g.dropna(subset=["f_gap", "gap", "f_intra", "intra", "spx_prev"])
    if len(g) < 20: continue
    rows.append(dict(year=y, n=len(g), c_fgap_spx=g.f_gap.corr(g.spx_prev), c_sgap_spx=g.gap.corr(g.spx_prev), c_fintra_spx=g.f_intra.corr(g.spx_prev), c_sintra_spx=g.intra.corr(g.spx_prev),
                     sd_fgap=1e4 * g.f_gap.std(), sd_sgap=1e4 * g.gap.std(), f_minus_s_open_bias=1e4 * ((g.f_intra - g.intra)).mean()))
print(pd.DataFrame(rows).round(3).to_string(index=False))
