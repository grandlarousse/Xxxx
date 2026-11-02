"""Yoğunlaşma (en iyi işlemler hangi günler) + seçim yanlılığı: 47 hissede rastgele işaret permütasyonuyla max-t dağılımı (OOS, net 10)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_a")
from vk import *
for s in ["CIMSA", "OYAKC"]:
    d = decomp(s).dropna(subset=["gap", "intra"]); b = d[d.gap.abs() > 0.01].copy()
    b["pnl_bps"] = 1e4 * (-np.sign(b.gap) * b.intra - 0.001); b["gap_%"] = 100 * b.gap; b["intra_%"] = 100 * b.intra
    print(s, "en iyi 15 işlem:"); print(b.nlargest(15, "pnl_bps")[["gap_%", "intra_%", "pnl_bps"]].round(2).to_string())
    print(s, "en kötü 8 işlem:"); print(b.nsmallest(8, "pnl_bps")[["gap_%", "intra_%", "pnl_bps"]].round(2).to_string())
    o = b[b.index >= SPLIT].pnl_bps; srt = o.sort_values(ascending=False)
    print(s, f"OOS toplam pnl {o.sum():.0f} bps; en iyi 10 işlemin payı {srt.iloc[:10].sum()/o.sum():.0%}; en iyi %5 ({int(len(o)*0.05)}) işlem payı {srt.iloc[:int(len(o)*0.05)].sum()/o.sum():.0%}")
# permütasyon: OOS, her hissede |gap|>1% günlerinde pozisyon işaretini rastgele çevir
rng = np.random.default_rng(7)
data = {}
for s in VIOP:
    d = decomp(s).dropna(subset=["gap", "intra"]); b = d[(d.gap.abs() > 0.01) & (d.index >= SPLIT)]
    data[s] = b.intra.values
def tstat(x): return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
obs = {s: tstat(-np.sign(decomp(s).dropna(subset=["gap","intra"]).query("abs(gap)>0.01 and index>=@SPLIT").gap.values) * v - 0.001) for s, v in data.items()}
mx = []
for _ in range(2000):
    mx.append(max(tstat(rng.choice([-1, 1], len(v)) * v - 0.001) for v in data.values()))
mx = np.array(mx)
print("gözlenen OOS t (iid): CIMSA %.2f OYAKC %.2f; null max-t %%95=%.2f %%99=%.2f; P(max>=CIMSA)=%.3f P(max>=OYAKC)=%.3f" % (obs["CIMSA"], obs["OYAKC"], np.quantile(mx, .95), np.quantile(mx, .99), (mx >= obs["CIMSA"]).mean(), (mx >= obs["OYAKC"]).mean()))
