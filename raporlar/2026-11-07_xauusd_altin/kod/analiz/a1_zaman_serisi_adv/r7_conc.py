import sys; sys.path.insert(0, ".")
from adv_common import *
pc, q = lowmom_spot(5); pv = asof_to_viop(pc)
for h in [1, 5]:
    net = bt(pv, r_v, h, 5, demean=True)
    srt = net.sort_values(ascending=False)
    tot = net.sum()
    print(f"h{h} toplam demeaned pnl {tot*1e4:.0f} bps; en iyi 10 gün payı {srt.head(10).sum()/tot:.2f}; en iyi 20 gün {srt.head(20).sum()/tot:.2f}; en iyi 20 gün çıkınca Sharpe {sh(net.drop(srt.head(20).index)):.2f}")
    # aylık katkı
    mo = net.groupby(net.index.to_period("M")).sum() * 1e4
    print("  en iyi 8 ay (bps):", mo.sort_values(ascending=False).head(8).round(0).to_dict())
    print("  en kötü 5 ay (bps):", mo.sort_values().head(5).round(0).to_dict())
    print("  pozitif ay payı (aktif aylar):", (mo[mo != 0] > 0).mean().round(2), " aktif ay sayısı", int((mo != 0).sum()))
    # en iyi 3 ay çıkarılınca
    top3 = mo.sort_values(ascending=False).head(3).index
    m = ~net.index.to_period("M").isin(top3)
    print("  en iyi 3 ay hariç Sharpe:", round(sh(net[m]), 2), " t", round(tstat(net[m]), 2))
# veri sorunları
print("\nv_ret==0 günleri:", d.index[d.v_ret == 0].strftime("%Y-%m-%d").tolist())
print("pos on v_ret==0 previous day:", pv.shift(1)[d.v_ret == 0].tolist())
print("|v_ret|>4%:", d.index[d.v_ret.abs() > 0.04].strftime("%Y-%m-%d").tolist())
print("v_volume<1000 gün sayısı:", int((d.v_volume < 1000).sum()), " aktif pozisyon:", int(((d.v_volume < 1000) & (pv != 0)).sum()))
# roll günleri ve hedef
roll = d.v_code != d.v_code.shift(1)
print("roll gün sayısı", int(roll.sum()), " roll günü (t+1 roll) pos*fwd1 katkı bps:", round(float((pv * d.fwd1)[roll.shift(-1, fill_value=False)].sum() * 1e4), 0))
# Erken spot alt dönemler
for a, b in [("2010-01-01", "2016-12-31"), ("2010-01-01", "2013-12-31"), ("2014-01-01", "2016-12-31"), ("2017-03-01", "2021-12-31"), ("2022-01-01", "2026-12-31"), ("2010-01-01", "2026-12-31")]:
    m = (s.index >= a) & (s.index <= b)
    for h in [1, 5]:
        n1 = bt(pc[m], r_s[m], h, 5, demean=True); n2 = bt(pc[m], r_s[m], h, 5, demean=True, demean_mode="year")
        print(f"spot {a[:4]}-{b[:4]} h{h}: dm {sh(n1):.2f} (t {tstat(n1):.2f}), yıl-dm {sh(n2):.2f}; aktif {float((pc[m]!=0).mean()):.2f}")
# Spot yıl yıl 2010-2016
n = bt(pc, r_s, 1, 5, demean=True)
print("spot yıllık h1:", n.groupby(n.index.year).apply(sh).round(2).to_dict())
print("aktif payı spot yıllık:", (pc != 0).groupby(pc.index.year).mean().round(2).to_dict())
