"""6) S3 komşuları (2/3/4 ardışık düşüş; erken çıkışlı/sabit) ve C0'da eşik yakınlığı duyarlılığı (kapanıştan 10 dk önce karar
verilemeyen sınır günleri çıkarılınca). S1 için de aynı: IBS 0,08-0,12 ve |r|<%0,1 sınır günleri çıkarılınca."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dt, lib
D = {s: lib.load(s) for s in ("SPY", "QQQ", "IWM", "DIA", "RSP", "MDY")}
print("S3 komşuları (C0/C1, net bp / t, 2.500$):")
for s in ("SPY", "QQQ", "IWM"):
    d = D[s]; cost = dt.cost_bp(s, 2500)
    for k in (2, 3, 4):
        for exn in ("ilk_yukselis", "sabit"):
            ex = dt.up_close(d) if exn == "ilk_yukselis" else None
            line = []
            for m in ("C0", "O1", "C1"):
                st = dt.summarize(d, dt.sim(d, dt.s3_signal(d, k), 3, m, ex), cost)
                line.append(f"{m}: n={st['n']} {st['net_bp']:.0f}/{st['t']:.2f} (IS {st['is_net_bp']:.0f}, OOS {st['oos_net_bp']:.0f})")
            print(f"  {s} {k} düşüş {exn:12s} | " + " | ".join(line))
print("C0 eşik yakınlığı: sınır günleri çıkarılınca")
for s in ("SPY", "QQQ"):
    d = D[s]; cost = dt.cost_bp(s, 2500); c = d["c"].values; r = np.r_[np.nan, c[1:] / c[:-1] - 1]
    ib = np.nan_to_num(dt.my_ibs(d), nan=0.5)
    s1 = dt.s1_signal(d); s1_m = s1 & ~((ib > 0.08) & (ib < 0.12)) & ~(np.abs(np.nan_to_num(r)) < 0.001)
    s3 = dt.s3_signal(d); s3_m = s3 & ~(np.abs(np.nan_to_num(r)) < 0.001)
    for lab, a, b, ex in (("S1", s1, s1_m, None), ("S3", s3, s3_m, dt.up_close(d))):
        st_a = dt.summarize(d, dt.sim(d, a, 3, "C0", ex), cost); st_b = dt.summarize(d, dt.sim(d, b, 3, "C0", ex), cost)
        print(f"  {s} {lab} C0: tüm n={st_a['n']} {st_a['net_bp']:.1f}/{st_a['t']:.2f} | sınır günleri hariç n={st_b['n']} {st_b['net_bp']:.1f}/{st_b['t']:.2f}"
              f" | sınır gün sayısı {int(a.sum() - b.sum())}")
# S1 SPY ve QQQ sinyal günlerinin örtüşmesi ve 'birleşik' kullanım (sermayeyi böl)
a = pd.Series(dt.s1_signal(D["SPY"]), index=D["SPY"].index); b = pd.Series(dt.s1_signal(D["QQQ"]), index=D["QQQ"].index)
print(f"SPY ve QQQ S1 sinyal günleri: SPY {int(a.sum())}, QQQ {int(b.sum())}, ortak {int((a & b).sum())} ({(a & b).sum() / a.sum():.2f} SPY'a göre)")
# Son sinyaller
for s in ("SPY", "QQQ", "IWM"):
    d = D[s]; z = pd.Series(dt.s1_signal(d), index=d.index); print(s, "son S1 sinyalleri:", list(z[z].index[-4:].date),
          "| son gün IBS", round(float(dt.my_ibs(d)[-1]), 3), "r", round(float(d['c'].iloc[-1] / d['c'].iloc[-2] - 1) * 100, 2), "%")
