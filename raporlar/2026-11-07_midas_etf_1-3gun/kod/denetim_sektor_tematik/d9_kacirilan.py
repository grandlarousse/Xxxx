"""Denetim — kaçırılan: S1 kenarı oynaklıkla ölçekleniyor; sabit 3 $ komisyon düşük oynaklıkta kenarı yiyor.
Eşik YALNIZ IS'te seçilir (IS medyanı, komşular %40/%60 yüzdelikleri), OOS raporlanır. Giriş: AH (+6 bp ceza).
python3 -I kod/denetim_sektor_tematik/d9_kacirilan.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d_ortak import *
pd.set_option("display.width", 250)
smh = D("SMH"); ib = my_ibs(smh)
vol20 = np.log(smh["c"]).diff().rolling(20).std() * np.sqrt(252)   # t kapanışı dahil, t'de bilinir
isv = vol20[vol20.index <= IS_END].dropna()
rows = []
for q in (0.4, 0.5, 0.6):
    thr = float(isv.quantile(q))
    for pos in (1000, 2500):
        for nm, sg in (("S1", ib < 0.2), (f"S1 & vol20>IS q{int(q*100)} ({thr:.2f})", (ib < 0.2) & (vol20 > thr))):
            tr = sim(smh, sg, 1, "C0", cost("SMH", pos) + 6.0); s = st(tr)
            rows.append({"kural": nm, "poz": pos, "n": s["n"], "net_bp": s["net_bp"], "t": s["t"], "is": s["is_net_bp"], "oos": s["oos_net_bp"],
                         "oos_t": s["oos_t"], "yil_poz": s["yil_poz"], "pazarda_gun_payi": s["n"] / len(smh)})
R = pd.DataFrame(rows).drop_duplicates(["kural", "poz"]); print(R.round(2).to_string())
R.to_csv(os.path.join(OUT, "d9_kacirilan.csv"), index=False)
