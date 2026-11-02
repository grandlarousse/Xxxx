"""A3: Uzun örneklem (Yahoo günlük 2014-2026) sağlamlık: medyan/winsor, hafta günü, gap işaretine koşullu gün-içi,
2021/2023 temizlik farkı (hangi gün?), yıl-blok bootstrap, uç gün çıkarma, açılış=önceki kapanış günleri."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a")
from vcommon import *
R = S + "/out/code_v_G3_a/res"; pd.set_option("display.width", 250)
x = decomp("XU030.IS"); x0 = decomp("XU030.IS", lim=9.9)  # neredeyse temizliksiz
s = -x.intra.dropna()
print("XU030 aç-sat 2014-2026: ort", round(1e4*s.mean(), 2), "medyan", round(1e4*s.median(), 2), "winsor1%",
      round(1e4*s.clip(s.quantile(.01), s.quantile(.99)).mean(), 2), "trim1%", round(1e4*s[(s > s.quantile(.01)) & (s < s.quantile(.99))].mean(), 2))
print("temizliksiz n", x0.intra.notna().sum(), "ort", round(-1e4*x0.intra.mean(), 2), " temizlikle düşen günler:")
dd = x0.index[x0.intra.notna() & x.intra.reindex(x0.index).isna()]
print(x0.loc[dd, ["gap", "intra", "cc_p"]].mul(1e4).round(0).to_string())
for y in [2021, 2023]:
    print(y, "temizliksiz intra", round(1e4*x0.intra.loc[str(y)].mean(), 2), "temizlikli", round(1e4*x.intra.loc[str(y)].mean(), 2),
          "| en büyük 3 |intra| günü:", x.intra.loc[str(y)].abs().nlargest(3).mul(1e4).round(0).to_dict())
# en uç 10 günü çıkar
for k in [5, 10, 20]:
    s2 = s.drop(s.abs().nlargest(k).index); print(f"en uç {k} gün çıkarıldı: ort {1e4*s2.mean():.2f} t {tstat(s2):.2f}")
# yıl-blok bootstrap (yılları yerine koyarak çek)
rng = np.random.default_rng(0); yrs = sorted(set(s.index.year)); by = {y: s[s.index.year == y].values for y in yrs}
bs = [np.concatenate([by[y] for y in rng.choice(yrs, len(yrs))]).mean() for _ in range(5000)]
print("yıl-blok bootstrap ort CI95:", np.round(1e4*np.percentile(bs, [2.5, 50, 97.5]), 2), " P(<=0)=", np.mean(np.array(bs) <= 0))
# hafta günü
x["dow"] = x.index.dayofweek
print("\nHafta günü (bps): "); print(x.groupby("dow")[["gap", "intra"]].agg(["mean", "count"]).mul([1e4, 1, 1e4, 1]).round(1).to_string())
print("gap t by dow:", x.groupby("dow")["gap"].apply(tstat).round(2).to_dict(), " intra t:", x.groupby("dow")["intra"].apply(tstat).round(2).to_dict())
# gap işaretine koşullu
x["gs"] = np.sign(x.gap)
print("\nGap işaretine koşullu gün-içi:"); print(x.groupby("gs")["intra"].agg(["mean", "count", tstat]).assign(mean=lambda d: 1e4*d["mean"]).round(2).to_string())
q = pd.qcut(x.gap, 5, labels=False)
print("gap kantil -> intra bps:", (1e4*x.groupby(q)["intra"].mean()).round(1).to_dict(), " gap kantil ort:", (1e4*x.groupby(q)["gap"].mean()).round(0).to_dict())
# gap etkisini çıkar: intra = a + b*gap ; a anlamlı mı?
import numpy.linalg as la
z = x[["gap", "intra"]].dropna(); Xm = np.c_[np.ones(len(z)), z.gap]; b = la.lstsq(Xm, z.intra, rcond=None)[0]; e = z.intra - Xm @ b
se = np.sqrt(np.diag(la.inv(Xm.T @ Xm)) * e.var()); print("intra = a + b gap: a", round(1e4*b[0], 2), "bps t", round(b[0]/se[0], 2), " b", round(b[1], 3), "t", round(b[1]/se[1], 2))
# açılış = önceki kapanış (bayat açılış) günleri
eq = (x.gap.abs() < 1e-9); print("\nXU030 gap==0 gün sayısı by yıl:", eq.groupby(x.index.year).sum().to_dict())
s3 = -x.intra[~eq].dropna(); print("gap==0 günleri hariç aç-sat ort", round(1e4*s3.mean(), 2), "t", round(tstat(s3), 2))
# Hisse: gap==0 oranı yıl bazında (açılış bayatlığı göstergesi)
P = pd.read_pickle(R + "/a1_P.pkl")
G0 = pd.DataFrame({k: (v.gap.abs() < 1e-9).groupby(v.index.year).mean() for k, v in P.items()})
print("47 hisse gap==0 oranı medyanı by yıl:", G0.median(axis=1).round(3).to_dict())
