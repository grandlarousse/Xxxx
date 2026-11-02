"""v6: (i) 3 hisse ortalama IS t ile varyant seçimi -> OOS; (ii) Abdi-Ranaldo (2017) kapanış-yüksek-düşük spread tahmini (vadeli ve spot)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
SC = pd.read_csv(RES + "/v5_speccurve.csv")
k = ["resid", "wb", "wz", "legs", "thr"]
A = SC.groupby(k).agg(IS_t=("IS_t", "mean"), OOS_t=("OOS_t", "mean"), OOS_bps=("OOS_bps", "mean")).reset_index().sort_values("IS_t", ascending=False)
print("== (i) Ortalama IS t ile sıralı ilk 8 varyant (3 hisse ort.) ==\n", A.head(8).round(2).to_string(index=False))
best = A.iloc[0]
x = SC.merge(pd.DataFrame([best[k]]), on=k)
print("seçilen varyantın hisse bazında OOS:\n", x[["tgt", "IS_bps", "IS_t", "OOS_bps", "OOS_t"]].round(2).to_string(index=False))
print("Başlık varyantı (resid, 250, 250, EU+US, 1.0) ortalama IS t sırası:", int(np.where((A.resid == True) & (A.wb == 250) & (A.wz == 250) & (A.legs == "EU+US") & (A.thr == 1.0))[0][0]) + 1, "/", len(A))
print("Tüm varyantlarda OOS ort. t dağılımı: medyan %.2f, %%75 %.2f, %%90 %.2f" % (A.OOS_t.median(), A.OOS_t.quantile(.75), A.OOS_t.quantile(.9)))
print("IS ort. t ile OOS ort. t sıra korelasyonu (Spearman): %.2f" % A[["IS_t", "OOS_t"]].corr(method="spearman").iloc[0, 1])

# (ii) Abdi-Ranaldo spread: s^2 = 4 E[(c_t - eta_t)(c_t - eta_{t+1})], eta = (log h + log l)/2
def ar_spread(c, h, l):
    lc, eta = np.log(c), (np.log(h) + np.log(l)) / 2
    x = 4 * (lc - eta) * (lc - eta.shift(-1))
    return x
F = pd.read_parquet(RES + "/v4b_viop_front.parquet")
print("\n== (ii) Abdi-Ranaldo efektif spread tahmini (bps, yıllık ort. -> sqrt(max(E,0))) ==")
for st in ["THYAO", "PGSUS", "TAVHL"]:
    f = F.loc[st]
    f = f[(f.high > 0) & (f.low > 0)]
    xf = ar_spread(f.close, f.high, f.low)
    d = bist_day(st + ".IS"); xs = ar_spread(d.c, d.h, d.l)
    outf = {y: round(1e4 * np.sqrt(max(v, 0)), 1) for y, v in xf.groupby(xf.index.year).mean().items()}
    outs = {y: round(1e4 * np.sqrt(max(v, 0)), 1) for y, v in xs[xs.index >= "2017-01-01"].groupby(xs[xs.index >= "2017-01-01"].index.year).mean().items()}
    print(st, "vadeli:", outf); print(st, "spot  :", outs)
    # fiyat adımı / fiyat (2024-26)
    ff = f[f.index >= "2024-01-01"]
    px = ff.close.median()
    print(f"   2024+ medyan vadeli fiyat {px:.2f} TL")
