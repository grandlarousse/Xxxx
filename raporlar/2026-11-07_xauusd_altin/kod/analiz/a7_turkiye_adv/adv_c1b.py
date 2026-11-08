"""Hakem: C1/C2 için kalıcı-rejim kaynaklı t şişmesi (NW gecikme duyarlılığı, blok bootstrap), etkin bağımsız gözlem."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
import numpy as np, pandas as pd
import lib_altin as L
p = L.load_viop()
isx = p.index <= L.IS_END
lfx = np.log(p.dk_USDTRY_p15); ur = p.vo_usdtry_ret; dte = p.vo_usdtry_dte
bpd = np.log(p.vo_usdtry_settle / p.dk_USDTRY_p15) / dte.clip(lower=3)
sig = (lfx.diff().rolling(20).mean() - bpd * 1.4).shift(1)
pos = np.sign(sig).fillna(0)
rng = np.random.default_rng(0)

def ic_nw(x, y, lags):
    return L.ic(x, y, lags)["t"]

def block_boot_ic(x, y, block, B=2000):
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna().rank()
    xv = d.x.values; yv = d.y.values; n = len(d)
    ic0 = np.corrcoef(xv, yv)[0, 1]
    # null: y'yi dairesel blok kaydırmayla x'ten ayır (bağımlılık yapısı korunur) -> kaydırma testi
    stats = []
    for b in range(B):
        k = rng.integers(block, n - block)
        stats.append(np.corrcoef(xv, np.roll(yv, k))[0, 1])
    stats = np.array(stats)
    return ic0, (np.abs(stats) >= abs(ic0)).mean(), stats.std()

print("=== C1: NW gecikme duyarlılığı (IC t) ===")
for h in (1, 5):
    y = L.fwd(ur, h)
    print(f"h={h}: " + " | ".join(f"lag {lg}: t {ic_nw(sig, y, lg):+.2f}" for lg in (5, 20, 60, 120, 250)))
    for seg, m in [("IS", isx), ("OOS", ~isx)]:
        print(f"    {seg}: " + " | ".join(f"lag {lg}: t {ic_nw(sig[m], y[m], lg):+.2f}" for lg in (5, 20, 60, 120)))
print("\n=== C1: dairesel kaydırma (rotation) testi — x ve y'nin kendi kalıcılığını korur ===")
for h in (1, 5):
    y = L.fwd(ur, h)
    ic0, pv, sd = block_boot_ic(sig, y, 60)
    print(f"h={h}: IC {ic0:+.3f}, kaydırma null sd {sd:.3f} (z≈{ic0/sd:+.2f}), p={pv:.4f}")
    for seg, m in [("IS", isx), ("OOS", ~isx)]:
        ic0, pv, sd = block_boot_ic(sig[m], y[m], 60)
        print(f"     {seg}: IC {ic0:+.3f}, z≈{ic0/sd:+.2f}, p={pv:.4f}")

print("\n=== C1 strateji PnL: NW t ve blok bootstrap ===")
a = L.backtest(pos, ur, 1, 5); pnl = a["pnl"]
import statsmodels.api as sm
for seg, m in [("tam", slice(None)), ("IS", pnl.index <= L.IS_END), ("OOS", pnl.index > L.IS_END)]:
    x = pnl if isinstance(m, slice) else pnl[m]
    out = []
    for lg in (0, 5, 20, 60):
        mm = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lg}) if lg else sm.OLS(x.values, np.ones(len(x))).fit()
        out.append(f"lag{lg} t {mm.tvalues[0]:+.2f}")
    print(f"  {seg}: " + " | ".join(out))
# pozisyon kaydırma testi: pozisyon serisini dairesel kaydır, getiriyi sabit tut (pozisyon kalıcılığı korunur)
pv = pos.reindex(ur.index).fillna(0).values; rv = ur.fillna(0).values
s0 = (np.roll(pv, 1) * rv)[1:].mean()
null = []
n = len(pv)
for b in range(3000):
    k = rng.integers(60, n - 60)
    pp = np.roll(pv, k)
    null.append((np.roll(pp, 1) * rv)[1:].mean())
null = np.array(null)
print(f"  pozisyon kaydırma testi (brüt ort günlük getiri): gerçek {s0*1e4:.2f} bps, null ort {null.mean()*1e4:.2f}, sd {null.std()*1e4:.2f}, p(>=)={(null >= s0).mean():.4f}")
# OOS
mo = (ur.index > L.IS_END)
pv2 = pv[mo]; rv2 = rv[mo]; s0 = (np.roll(pv2, 1) * rv2)[1:].mean(); null = []
for b in range(3000):
    k = rng.integers(60, len(pv2) - 60); pp = np.roll(pv2, k); null.append((np.roll(pp, 1) * rv2)[1:].mean())
null = np.array(null)
print(f"  OOS pozisyon kaydırma testi: gerçek {s0*1e4:.2f} bps, null ort {null.mean()*1e4:.2f}, sd {null.std()*1e4:.2f}, p(>=)={(null >= s0).mean():.4f}")
mo = (ur.index <= L.IS_END)
pv2 = pv[mo]; rv2 = rv[mo]; s0 = (np.roll(pv2, 1) * rv2)[1:].mean(); null = []
for b in range(3000):
    k = rng.integers(60, len(pv2) - 60); pp = np.roll(pv2, k); null.append((np.roll(pp, 1) * rv2)[1:].mean())
null = np.array(null)
print(f"  IS pozisyon kaydırma testi: gerçek {s0*1e4:.2f} bps, null ort {null.mean()*1e4:.2f}, sd {null.std()*1e4:.2f}, p(>=)={(null >= s0).mean():.4f}")

# Rejim sayısı: pozisyon epizotları
chg = (pos != pos.shift(1)).cumsum()
ep = pd.DataFrame({"pos": pos, "r": pos.shift(1) * ur, "g": chg}).groupby("g").agg(pos=("pos", "first"), n=("pos", "size"), pnl=("r", "sum"),
                                                                               start=("pos", lambda s: s.index[0]))
ep = ep[ep.pos != 0]
print(f"\n  pozisyon epizotu sayısı {len(ep)}, ortanca uzunluk {ep.n.median():.0f} gün; en kârlı 5 epizot PnL payı: {ep.pnl.nlargest(5).sum()/ep.pnl.sum()*100:.0f}%")
print(ep.sort_values("pnl", ascending=False).head(6).assign(pnl=lambda d: (d.pnl * 100).round(1)).to_string())
print(ep.sort_values("pnl").head(4).assign(pnl=lambda d: (d.pnl * 100).round(1)).to_string())

print("\n=== C2: NW gecikme ve kaydırma testi (2023-06+, hedef h-gün spot) ===")
MAN = pd.Timestamp("2023-06-01"); m = p.index >= MAN
tr20 = lfx.diff().rolling(20).mean()
for h in (1, 3, 5):
    y = lfx.shift(-h) - lfx
    print(f"h={h}: " + " | ".join(f"lag {lg}: t {ic_nw(tr20[m], y[m], lg):+.2f}" for lg in (5, 20, 60)), end="")
    ic0, pv_, sd = block_boot_ic(tr20[m], y[m], 40)
    print(f" | kaydırma z≈{ic0/sd:+.2f} p={pv_:.3f}")
    m2 = m & (p.index < "2026-01-01")
    q = L.ic(tr20[m2], y[m2], max(h, 5)); print(f"    2026 hariç: IC {q['ic']:+.3f} t {q['t']:+.2f}")
    # günlük değişimin aşırı yüksek olduğu birkaç günü (2023 Haz-Ağu, 2025-03) hariç
    m3 = m & ~((p.index >= "2023-06-01") & (p.index <= "2023-08-31")) & ~((p.index >= "2025-03-15") & (p.index <= "2025-04-15"))
    q = L.ic(tr20[m3], y[m3], max(h, 5)); print(f"    2023-06..08 ve 2025-03/04 hariç: IC {q['ic']:+.3f} t {q['t']:+.2f}")
# 2026'da ne oldu: günlük ortalama kayma ay ay
dd = lfx.diff()[m]
print("\n  aylık ort günlük USDTRY değişimi (bps):"); print((dd.groupby(dd.index.to_period("M")).mean() * 1e4).round(1).tail(20).to_string())
