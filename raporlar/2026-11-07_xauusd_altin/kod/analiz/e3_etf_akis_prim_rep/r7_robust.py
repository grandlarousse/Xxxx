"""E3-1/E3-2 sağlamlık: zamanlama alfası, demean kuralı, 2008, veri sıçramaları, kapanış öncesi giriş (saatlik), yarım günler."""
from rc import *
import warnings; warnings.filterwarnings("ignore")
sig = pd.read_parquet(f"{OUT}/sig_m.parquet"); days = sig.index
pos = ((sig.m < 0) & sig.m.notna()).astype(float)
for tgt in ["GDXJ", "GDX"]:
    lr_ = np.log(yh(tgt).reindex(days)).diff(); R = np.expm1(lr_)
    print(tgt, "günlük |log getiri|>20% gün:", lr_[lr_.abs() > 0.2].round(3).to_dict())
    y = R.shift(-1)
    for seg, msk in [("IS", days <= IS_END), ("OOS", days > IS_END), ("22+", days >= "2022-01-01")]:
        d = pd.concat([pos[msk].rename("p"), y[msk].rename("y")], axis=1).dropna()
        b, t = nw_t(d.y.values, d.p.values, 5)
        print(f"  {tgt} {seg}: uzun-gün − nakit-gün ortalama fark {b*1e4:+.1f} bps/gün, NW t {t:.2f}; uzun-gün ort {d.y[d.p==1].mean()*1e4:+.1f}, nakit-gün ort {d.y[d.p==0].mean()*1e4:+.1f}")
    # 2008 (yalnız GDX)
    if tgt == "GDX":
        net, wl, _ = run_bt(pos, R.dropna(), 1, 10)
        print("  GDX 2008: strateji toplam basit getiri %", round(net["2008"].sum() * 100, 1), "| B&H toplam basit getiri %", round(R["2008"].sum() * 100, 1),
              "| 2008 IC", round(ic(sig.zm["2008"], fwd(lr_, 1)["2008"], 5)["ic"], 3), "| 2008 uzun-gün ort bps", round(R.shift(-1)["2008"][pos["2008"] == 1].mean() * 1e4, 1), "nakit-gün", round(R.shift(-1)["2008"][pos["2008"] == 0].mean() * 1e4, 1))
        # 2008 Eylül-Kasım
        print("  GDX 2008-09..11 strateji %", round(net["2008-09":"2008-11"].sum() * 100, 1), "B&H %", round(R["2008-09":"2008-11"].sum() * 100, 1))
# --- kapanış öncesi giriş: saatlik GDXJ (son ~2 yıl, düzeltmesiz) — 15:30 ET fiyatından giriş/çıkış vs 16:00
g = pd.read_parquet(f"{P}/yahoo_h/GDXJ.parquet"); g.index = g.index.tz_convert(NY)
print("saatlik GDXJ:", g.index.min(), g.index.max(), "| bar başlangıçları:", sorted(set(g.index.strftime("%H:%M")))[:12])
reg = g.between_time("09:30", "15:59")
o1530 = reg[reg.index.strftime("%H:%M") == "15:30"]["open"]; o1530.index = pd.to_datetime(o1530.index.date)
c1530 = reg[reg.index.strftime("%H:%M") == "14:30"]["close"]; c1530.index = pd.to_datetime(c1530.index.date)  # 14:30 barının kapanışı = 15:30
cl = yh("GDXJ", "close").reindex(days)
e = pd.concat([o1530.rename("p1530"), c1530.rename("c1530"), cl.rename("close"), pos.rename("p")], axis=1).dropna()
e["r_close"] = np.log(e.close.shift(-1) / e.close); e["r_1530"] = np.log(e.p1530.shift(-1) / e.p1530)
e["last30"] = np.log(e.close / e.p1530)
e = e.dropna()
print("saatlik örneklem n", len(e), e.index.min().date(), e.index.max().date())
for col in ["r_close", "r_1530"]:
    b, t = nw_t(e[col].values, e.p.values, 5)
    print(f"  {col}: uzun-gün − nakit-gün {b*1e4:+.1f} bps (t {t:.2f}); strateji gün başı ort {e[col][e.p==1].sum()/len(e)*1e4:+.2f} bps")
print("  son 30 dk GDXJ getirisi (15:30->16:00) m<0 günlerinde ort bps", round(e.last30[e.p == 1].mean() * 1e4, 1), "m>=0:", round(e.last30[e.p == 0].mean() * 1e4, 1))
# --- demean kuralı ve tam/segment ortalamaları
R = np.expm1(np.log(yh("GDXJ").reindex(days)).diff()).dropna()
print("GDXJ ortalama günlük getiri bps: tam", round(R.mean() * 1e4, 2), "IS", round(R[:"2017"].mean() * 1e4, 2), "OOS", round(R["2018":].mean() * 1e4, 2))
# --- maliyet duyarlılığı OOS
for c in (0, 5, 10, 15, 20, 30, 40):
    net, _, _ = run_bt(pos, R, 1, c); print(f"  maliyet {c} bps: OOS Sharpe {seg_sh(net)['OOS']}, IS {seg_sh(net)['IS']}, 22+ {seg_sh(net)['s22']}")
# --- yıl yıl net (10 bps) ve B&H
net, wl, _ = run_bt(pos, R, 1, 10)
yy = pd.DataFrame({"strat_%": net.groupby(net.index.year).sum() * 100, "bh_%": R.groupby(R.index.year).sum() * 100}).round(1)
print(yy.T.to_string())
