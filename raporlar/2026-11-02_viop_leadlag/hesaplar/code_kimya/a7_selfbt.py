"""A7: sürücüsüz kontrol backtestleri (dış sürücü öncülüğünün 'gap'te bitip gün-içinde tersine dönüp dönmediğini anlamak için).
(1) Gap-fade: pozisyon = -sign(gap_t) (açılışta bilinir) -> intra_t.
(2) Kendi momentumu: sign(cc_{t-1}) -> intra_t (açılışta gir) ve sign(cc_{t-1}) -> cc_t (kapanış seansında gir; yaklaşık).
(3) Koşullu: ABD gübre sepeti_{t-1} ile GUBRF gap_t uyumsuzluğu (gap'in sürücüye göre aşırı/eksik tepkisi) -> intra_t.
Çıktı: res_selfbt.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
from a4_bt import basket, US_FERT, EU_CEM
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []


def rec(name, sig, tgt, mode="sign", thr=0.0):
    for cost in [0, 10, 15]:
        res, pnl, pos = run_bt(sig, tgt, cost, thr=thr, mode=mode)
        rows.append({"spec": name, "cost": cost, **{f"{k}_{p}": res[p].get(k, np.nan) for p in ["IS", "OOS"] for k in ["n", "mean_bps", "t", "sharpe"]},
                     "years_bps": res["by_year_bps"]})
    r = rows[-2]
    print(f"{name:55s} 10bps IS {r['mean_bps_IS']:+6.1f} (t{r['t_IS']:+.1f}) OOS {r['mean_bps_OOS']:+6.1f} (t{r['t_OOS']:+.1f}) SR_OOS {r['sharpe_OOS']:+.2f} | brüt OOS {rows[-3]['mean_bps_OOS']:+.1f}", flush=True)


for s in STOCKS + ["XU100"]:
    dd = DEC(s)
    rec(f"gap-fade {s}", -dd["gap"], dd["intra"])
    rec(f"gap-fade |gap|>1% {s}", -dd["gap"], dd["intra"], thr=0.01)
    rec(f"momentum cc_t-1 -> intra_t {s}", dd["cc"].shift(1), dd["intra"])
    rec(f"momentum cc_t-1 -> cc_t {s}", dd["cc"].shift(1), dd["cc"])
# (3) GUBRF: gap - beta*sepet farkı
fb = basket(US_FERT).shift(1); g = DEC("GUBRF")
df = pd.concat([g["gap"].rename("gap"), fb.rename("f")], axis=1).dropna()
beta = df.gap.rolling(500, min_periods=200).cov(df.f).shift(1) / df.f.rolling(500, min_periods=200).var().shift(1)
mis = df.gap - beta * df.f  # sürücü dışı gap
rec("GUBRF: sürücü-dışı gap fade", -mis, g["intra"])
rec("GUBRF: sürücüyle açıklanan gap devam", beta * df.f, g["intra"])
eb = basket(EU_CEM).shift(1); c = DEC("CIMSA")
df = pd.concat([c["gap"].rename("gap"), eb.rename("f")], axis=1).dropna()
beta = df.gap.rolling(500, min_periods=200).cov(df.f).shift(1) / df.f.rolling(500, min_periods=200).var().shift(1)
rec("CIMSA: sürücü-dışı gap fade (AB çimento)", -(df.gap - beta * df.f), c["intra"])
rec("CIMSA: sürücüyle açıklanan gap devam", beta * df.f, c["intra"])
pd.DataFrame(rows).to_csv(os.path.join(HERE, "res_selfbt.csv"), index=False)
