"""XME -> COPX pozitif gecikme (a4'te FDR, IS/OOS aynı işaret) işlem kuralına çevrildi: XME z1>+1 -> COPX al;
kontroller: COPX kendi z1>+1, XME z1<-1 (beklenen negatif). Çıktı: sonuclar/aile_sektor_tematik/xme_copx_kural.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *
def z1(s): r = np.log(D(s)["c"]).diff(); return r / r.rolling(60).std().shift(1)
zx = z1("XME").reindex(D("COPX").index); zc = z1("COPX")
rows = []
for nm, sg in (("XME z>+1 -> COPX al", zx > 1), ("XME z>+1 & COPX z<=+1 -> COPX al", (zx > 1) & (zc <= 1)),
               ("kontrol: COPX z>+1 -> COPX al", zc > 1), ("XME z<-1 -> COPX al (beklenen negatif)", zx < -1)):
    for mode in ("C0", "O1", "C1"):
        for h in (1, 3):
            s = summarize(run_sym("COPX", sg, h, mode), nm, per_sym=False); s.update({"mode": mode, "h": h}); rows.append(s)
r = pd.DataFrame(rows); r.to_csv(os.path.join(OUT, "xme_copx_kural.csv"), index=False)
pd.set_option("display.width", 250)
print(r[["label", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t_naive", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string())
