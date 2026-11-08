"""Hakem: C4 (USDTRY t-1 -> ons), C5 (TR şoku -> kısa ons), C6 (XAUTRYM OI değişimi -> ons)."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
import numpy as np, pandas as pd
import lib_altin as L
from a7_common import build, half_days  # yalnız özellik üretimi; register çağrılmıyor
pd.set_option("display.width", 250)
p, f = build()
r = p.v_ret; isx = p.index <= L.IS_END
sp = L.load_spot()
PER = [("2017", "2019"), ("2020", "2021"), ("2022", "2023"), ("2024", "2026")]

def per_ic(x, y, h):
    out = []
    for a, b in PER:
        m = (x.index.year >= int(a)) & (x.index.year <= int(b))
        q = L.ic(x[m], y[m], max(h, 5)); out.append(f"{a[2:]}-{b[2:]}: {q['ic']:+.3f}({q['t']:+.1f})")
    return " ".join(out)

def bt_line(pos, ret, h, lab):
    o = []
    for c in (5, 10):
        a = L.backtest(pos, ret, h, c); ao = L.backtest(pos[~isx], ret[~isx], h, c); ad = L.backtest(pos[~isx], ret[~isx], h, c, demean=True)
        o.append(f"{c}bps tam {a['sharpe']:+.2f} OOS {ao['sharpe']:+.2f} OOSdm {ad['sharpe']:+.2f}")
    print(f"  {lab}: " + " | ".join(o))

# ---------------- C4 ----------------
print("=== C4: usd_fut_l1 -> XAUUSD ===")
x = f.usd_fut_l1
for h in (1, 3, 5):
    st = L.split_stats(x, f[f"fwd{h}"], h)
    print(f"h={h}: IC {st['ic']:+.3f} t {st['t']:+.2f} IS {st['t_is']:+.2f} OOS {st['t_oos']:+.2f} | alt dönemler {per_ic(x, f[f'fwd{h}'], h)}")
# komşu öngörücüler: spot USDTRY 15:00 değişimi t-1, 2g, 5g; demeaned hedef
for nm, xx in [("usd_spot_1 (t)", f.usd_spot_1), ("usd_spot_1 t-1", f.usd_spot_1.shift(1)), ("usd_fut 2g", p.vo_usdtry_ret.rolling(2).sum().shift(1)),
               ("usd_fut_5_l1", f.usd_fut_5_l1)]:
    q = L.ic(xx, f.fwd3, 5); print(f"  komşu {nm:16s} h=3: IC {q['ic']:+.3f} t {q['t']:+.2f}")
# USDTRY'den küresel dolar bileşenini ayır: DXY değişimi ile ortogonalize
dxy = np.log(p.dk_DOLLARIDXUSD_p15) if "dk_DOLLARIDXUSD_p15" in p else None
if dxy is not None:
    d = pd.concat([p.vo_usdtry_ret.rename("u"), dxy.diff().rename("d")], axis=1).dropna()
    b = np.polyfit(d.d, d.u, 1)[0]
    u_orth = (p.vo_usdtry_ret - b * dxy.diff()).shift(1)
    q = L.ic(u_orth, f.fwd3, 5); q2 = L.ic(dxy.diff().shift(1), f.fwd3, 5)
    print(f"  USDTRY (DXY'den arındırılmış, t-1) h=3: IC {q['ic']:+.3f} t {q['t']:+.2f}  | DXY Δ(t-1) h=3: IC {q2['ic']:+.3f} t {q2['t']:+.2f}")
# spot hedef (15:00->15:00) ile aynı öngörücü (2017+)
xs = x.reindex(sp.index)
q = L.ic(xs, sp.sfwd3, 5); print(f"  spot hedef sfwd3 (2017+): IC {q['ic']:+.3f} t {q['t']:+.2f}")
pos = -np.sign(x).fillna(0)
bt_line(pos, r, 3, "C4 kural")
# yalnız kısa bacak / yalnız uzun bacak
for nm, pp in [("yalnız kısa (USDTRY↑)", pos.clip(upper=0)), ("yalnız uzun (USDTRY↓)", pos.clip(lower=0))]:
    a = L.backtest(pp, r, 3, 5, demean=True); print(f"  {nm} demeaned tam Sharpe {a['sharpe']:+.2f}")

# ---------------- C5 ----------------
print("\n=== C5: TR şoku -> kısa ons ===")
def shock(fx_th=0.025, xu_th=-0.05):
    return ((f.usd_spot_1.abs() > fx_th) | (f.xu_l1 < xu_th)).astype(float)
for fx_th in (0.015, 0.02, 0.025, 0.03, 0.04):
    for xu_th in (-0.03, -0.04, -0.05, -0.06):
        s = shock(fx_th, xu_th)
        y = f.fwd3; e = (y[s > 0] - y.mean()).dropna()
        idx = np.where(s.values > 0)[0]; ep = np.r_[0, np.cumsum(np.diff(idx) > 10)]
        em = pd.Series((y.iloc[idx] - y.mean()).values).groupby(ep).mean().dropna()
        tcl = em.mean() / (em.std() / np.sqrt(len(em)))
        a = L.backtest(-s, r, 3, 5); ao = L.backtest(-s[~isx], r[~isx], 3, 5)
        print(f"  |FX|>{fx_th:.3f} veya XU<{xu_th:+.2f}: n={int(s.sum()):3d} epizot {len(em):2d} fazla {e.mean()*1e4:+6.1f} bps, epizot t {tcl:+.2f} | Sharpe tam {a['sharpe']:+.2f} OOS {ao['sharpe']:+.2f}")
# Ayrı bileşenler ve yön (yalnız TL değer kaybı, yalnız TL değer kazancı)
for nm, s in [("TL değer kaybı >2.5%", (f.usd_spot_1 > 0.025)), ("TL değer kazancı >2.5%", (f.usd_spot_1 < -0.025)), ("yalnız XU<-5%", (f.xu_l1 < -0.05))]:
    y = f.fwd3; e = (y[s] - y.mean()).dropna(); print(f"  {nm:24s}: n={len(e)} fazla {e.mean()*1e4:+.1f} bps t(naif) {e.mean()/(e.std()/np.sqrt(len(e))):+.2f}")
# 2018-08 ve 2021-11/12 hariç
s = shock()
ex = ~(((p.index >= "2018-08-01") & (p.index <= "2018-09-30")) | ((p.index >= "2021-11-01") & (p.index <= "2022-01-31")))
y = f.fwd3; e = (y[(s > 0) & ex] - y.mean()).dropna()
print(f"  2018-08/09 ve 2021-11..2022-01 hariç: n={len(e)} fazla {e.mean()*1e4:+.1f} bps t(naif) {e.mean()/(e.std()/np.sqrt(len(e))):+.2f}")
# küresel dolar: şok günlerinde DXY (t 15:00, 1g) değişimi
if dxy is not None:
    dd = dxy.diff()
    print(f"  şok günlerinde DXY 1g ort {dd[s>0].mean()*1e4:+.1f} bps (koşulsuz {dd.mean()*1e4:+.1f}); sonraki 3g DXY {(dxy.shift(-3)-dxy)[s>0].mean()*1e4:+.1f} bps")

# ---------------- C6 ----------------
print("\n=== C6: XAUTRYM OI 1g değişimi -> ons ===")
x = f.goi_d1_l1
gcode = p.vo_xautry_code
groll = (gcode != gcode.shift(1))
print(f"  XAUTRYM aktif kontrat değişim günü sayısı: {int(groll.sum())}; bu günlerde |Δln OI| ort {np.log(p.vo_xautry_oi).diff()[groll].abs().mean():.3f} vs diğer {np.log(p.vo_xautry_oi).diff()[~groll].abs().mean():.3f}")
# aynı kontrat içi OI değişimi (roll sıçraması yok): viop_long'dan
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
Lg = pd.read_parquet(f"{S}/panel/viop_long.parquet")
g = Lg[Lg.root == "XAUTRYM"][["date", "code", "oi"]].copy(); g["date"] = pd.to_datetime(g["date"])
tot = g.groupby("date").oi.sum().reindex(p.index)
pv = g.pivot_table(index="date", columns="code", values="oi").reindex(p.index)
same_c = pd.Series([pv.loc[d, c] if (isinstance(c, str) and c in pv.columns) else np.nan for d, c in zip(p.index, gcode)], index=p.index)
prev_c = pd.Series([pv[c].shift(1).loc[d] if (isinstance(c, str) and c in pv.columns) else np.nan for d, c in zip(p.index, gcode)], index=p.index)
oi_within = np.log(same_c / prev_c)
cands = {"goi_d1_l1 (analist)": x, "toplam XAUTRYM OI Δln (t-1)": np.log(tot).diff().shift(1), "aynı kontrat içi OI Δln (t-1)": oi_within.shift(1),
         "goi_d1_l1, XAUTRYM roll günleri NaN": x.where(~groll.shift(1, fill_value=False))}
for nm, xx in cands.items():
    for h in (1, 3, 5):
        st = L.split_stats(xx, f[f"fwd{h}"], h)
        print(f"  {nm:38s} h={h}: IC {st['ic']:+.3f} t {st['t']:+.2f} IS {st['t_is']:+.2f} OOS {st['t_oos']:+.2f} yrs {st['yrs_same_sign']}/{st['yrs']}")
print("  alt dönemler goi_d1_l1 h=3:", per_ic(x, f.fwd3, 3))
for nm, xx in list(cands.items())[:3]:
    pos = np.sign(xx).fillna(0); bt_line(pos, r, 3, f"kural {nm}")

# ---------------- çoklu test ----------------
print("\n=== çoklu test (162 test; Bonferroni eşiği p<0.05/162) ===")
from scipy import stats as st_
for nm, t in [("C1 IC h1", 4.35), ("C1 strateji", 2.79), ("C2 IC h5 (2023-06+)", 2.71), ("C3 IC h3", -6.10), ("C4 IC h3", -2.08), ("C5 naif", -2.73), ("C5 kümeli", -1.55), ("C6 IC h3", 2.11)]:
    pval = 2 * (1 - st_.norm.cdf(abs(t))); print(f"  {nm:22s} t {t:+.2f} p {pval:.2e} Bonferroni p×162 {min(1, pval*162):.3f}")
