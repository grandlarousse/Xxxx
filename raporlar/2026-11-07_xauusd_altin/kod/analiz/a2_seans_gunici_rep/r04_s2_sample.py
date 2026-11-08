"""C1: analist rakamı (2010-16: 2,15 bps) ile benimki (2,34) arasındaki farkın kaynağı: örneklem (p20 eksik günler)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a2_seans_gunici_rep")
from rep_common import *
sp = pd.read_parquet(f"{P}/panel_spot.parquet"); sp.index = pd.to_datetime(sp.index)
d = sp.index
p20a = pd.Series(price_asof(day_times(d, 20), 3).values, index=d).shift(1)
p00 = pd.Series(price_at(day_times(d, 0)).values, index=d)
S2_mine = np.log(p00 / p20a)
S2_pan = np.log(sp.xau_p00 / sp.xau_p20_prev)
segs_ok = pd.concat([np.log(sp.xau_p20_prev / sp.xau_p15_prev), S2_pan, np.log(sp.xau_p07 / sp.xau_p00), np.log(sp.xau_p12 / sp.xau_p07), np.log(sp.xau_p15 / sp.xau_p12)], axis=1).notna().all(axis=1)
for nm, x in [("benim (as-of p20)", S2_mine), ("panel sütunları, tüm segment dolu", S2_pan[segs_ok]), ("benim, analist örneklemi", S2_mine[segs_ok])]:
    for per, m in [("2010-16", x.index < "2017-01-01"), ("tam", x.index > "2000")]:
        mu, t, n = nw_t_mean(x[m], 5); print(f"{nm} {per}: {mu*1e4:.2f} bps t {t:.2f} n {n}")
extra = S2_mine.dropna().index.difference(S2_pan[segs_ok].dropna().index)
print("benim örneklemde olup analistte olmayan gün:", len(extra), "bu günlerde S2 ort", round(S2_mine[extra].mean()*1e4, 1), "bps; günler (ilk 10):", [str(x.date()) for x in extra[:10]])
print("bu günlerin haftanın günü:", pd.Series(extra.dayofweek).value_counts().to_dict())
diff = (S2_mine - S2_pan)[segs_ok].abs().dropna(); print("ortak günlerde |fark|>0:", (diff > 1e-12).sum())
