"""Açılış verisi kalitesi (2014+): hisse gap'i ile XU100 gap'i korelasyonu yıllara göre; |gap|>%1 gün oranı. Açılış 'bozuksa' korelasyon düşer."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
X = decomp("XU100", start="2010-01-01")
rows = []
for s in ["GARAN", "AKBNK", "THYAO", "CIMSA", "OYAKC", "EREGL"]:
    d = decomp(s, start="2010-01-01")
    # 2014 öncesi de hesapla (decomp start 2010)
    j = d[["gap", "intra"]].join(X[["gap", "intra"]].add_prefix("x_"), how="inner").dropna()
    g = j.groupby(j.index.year)
    r = pd.DataFrame({"corr_gap_xgap": g.apply(lambda z: z.gap.corr(z.x_gap)), "corr_intra_xintra": g.apply(lambda z: z.intra.corr(z.x_intra)),
                      "corr_gap_intra": g.apply(lambda z: z.gap.corr(z.intra)), "sd_gap_bps": g.gap.std() * 1e4, "sd_xgap_bps": g.x_gap.std() * 1e4})
    print(s); print(r.round(2).T.to_string())
