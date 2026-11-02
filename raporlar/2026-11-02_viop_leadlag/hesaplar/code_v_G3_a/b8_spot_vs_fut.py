"""B8: Spot (Yahoo) ve VİOP vadeli gün-içi farkının kaynağı.  disc = f_intra - s_intra (aynı gün). Kapanışlar aynı saatte (18:10),
açılışlar farklı: vadeli 09:30 (2023+ açılış seansı 09:20-09:30), spot endeks ~10:00 (09:40-09:55 açılış müzayedesi).
disc > 0 => spot açılış fiyatı, vadeli açılışına göre 'yüksek' (veya 09:30->10:00 arasında yükseliş). Yıllara göre + gap büyüklüğüne göre."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
import warnings; warnings.filterwarnings("ignore")
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)
Z = pd.read_parquet(R + "/b5_XU030_panel.parquet").dropna(subset=["f_intra", "intra", "f_gap", "gap"])
Z["disc"] = Z.f_intra - Z.intra
Y = Z.groupby(Z.index.year).agg(n=("disc", "size"), disc=("disc", lambda s: 1e4 * s.mean()), t=("disc", tstat), disc_med=("disc", lambda s: 1e4 * s.median()),
                                s_short=("intra", lambda s: -1e4 * s.mean()), f_short=("f_intra", lambda s: -1e4 * s.mean()), f_gap=("f_gap", lambda s: 1e4 * s.mean()))
print(Y.round(2).to_string())
print("Tüm: disc ort", round(1e4 * Z.disc.mean(), 2), "t", round(tstat(Z.disc), 2), "| 2017-2023:", round(1e4 * Z.disc.loc[:"2023"].mean(), 2), "t", round(tstat(Z.disc.loc[:"2023"]), 2),
      "| 2024-2026:", round(1e4 * Z.disc.loc["2024":].mean(), 2), "t", round(tstat(Z.disc.loc["2024":]), 2))
q = pd.qcut(Z.gap, 5, labels=False)
print("spot gap kantiline göre disc (bps):", (1e4 * Z.groupby(q).disc.mean()).round(1).to_dict())
print("hafta günü disc:", (1e4 * Z.groupby(Z.index.dayofweek).disc.mean()).round(1).to_dict())
# Aynı günlerde spot ve vadeli aç-sat stratejisi: yıllık işaret uyumu
both = Y[Y.n >= 100]
print("spot aç-sat >0 yıl:", int((both.s_short > 0).sum()), "/", len(both), " vadeli aç-sat >0 yıl:", int((both.f_short > 0).sum()), "/", len(both))
Y.to_csv(R + "/b8_disc_years.csv")
