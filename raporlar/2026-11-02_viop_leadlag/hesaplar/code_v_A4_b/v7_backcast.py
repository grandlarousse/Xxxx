"""v7: geriye dönük holdout (2008-2013): Yahoo açılışı bozuk olduğundan gün-içi yok; ama 2014+ AIR->gap≈0 olduğu için
AIR_{t-1} -> cc_t gün-içi etkisinin vekili. Kaynak ajan bu dönemi AIR sepetiyle test etmedi (hipotez 2014+ veride kuruldu)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
SG = pd.read_parquet(RES + "/signals.parquet"); AIR = SG.AIR_C
print("AIR ilk geçerli tarih:", AIR.dropna().index[0].date())
for st in ["THYAO", "PGSUS", "TAVHL", "XU100", "DOCO"]:
    d = bist_day(st + ".IS")
    for lab, a, b, col in [("2008-13 cc", "2008-01-01", "2014-01-01", "cc"), ("2014-26 cc", "2014-01-01", "2027", "cc"), ("2014-26 gap", "2014-01-01", "2027", "gap"), ("2014-26 intra", "2014-01-01", "2027", "intra")]:
        y = d[col][(d.index >= a) & (d.index < b)]
        if y.notna().sum() < 200: continue
        df = pd.concat([AIR.rename("s"), y.rename("y")], axis=1).dropna()
        r, n = ols_nw(df.y, df[["s"]])
        b8 = bt(AIR, y, 8, 1.0); b0 = bt(AIR, y, 0, 1.0)
        print(f"{st:6s} {lab:14s} sürekli: coef {r.loc['s','coef']:.3f} NW t {r.loc['s','t']:.2f} (n {n}) | eşik bt brüt {b0['gross']:.1f} bps (t {b0['t_g']:.2f}), 8bps net {b8['bps']:.1f} (t {b8['t']:.2f}), n işlem {b8['n']}")
    d = bist_day(st + ".IS"); y = d.cc[(d.index >= "2008-01-01") & (d.index < "2014-01-01")]
    g, _ = pnl_series(AIR, y)
    if len(g): print("      yıllar brüt:", (1e4 * g.groupby(g.index.year).mean()).round(1).to_dict())
