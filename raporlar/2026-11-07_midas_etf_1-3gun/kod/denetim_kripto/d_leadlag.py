"""Denetim kripto lead-lag: sweep özeti + bağımsız regresyonlar (kendi gecikmesi kontrollü, Newey-West) +
IBIT kapanış 'yetişme' (BTC 16:00 ET'ye göre kapanış sapması) + gerçek zamanlı boşluk R².
Çalıştır: python3 -I kod/denetim_kripto/d_leadlag.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import dk, lib
from scipy import stats as st

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
ROOT = dk.ROOT; OUT = dk.OUT

def nw(y, X, lags):
    n, k = X.shape
    xtx = np.linalg.inv(X.T @ X); b = xtx @ X.T @ y; e = y - X @ b
    u = X * e[:, None]; S = u.T @ u
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx
    return b, b / np.sqrt(np.diag(V))

FAMT = ["IBIT", "FBTC", "GBTC", "ETHA", "ETHE", "BITX", "BITI", "SBIT", "ETHU", "BITB", "ARKB", "BITO", "BITU", "BLOK", "MSTU", "CONL"]
print("=== 1) leadlag_sweep aile satırları ===")
L = pd.read_csv(os.path.join(ROOT, "sonuclar", "leadlag_sweep.csv")); x = L[L.target.isin(FAMT)].copy()
fl = ["fdr10_lag_t_h1", "fdr10_lag_t_h3", "fdr10_catch_t_h1", "fdr10_catch_t_h3"]
print(f"  satır {len(x)}, test {len(x)*4}, global FDR bayrağı olan satır: {int(x[fl].any(axis=1).sum())}")
pp = np.concatenate([x["p_" + c].values for c in ["lag_t_h1", "lag_t_h3", "catch_t_h1", "catch_t_h3"]])
print(f"  aile içi BH (q=0.10) yeniden: geçen {int(dk.bh(pp).sum())}; en küçük p={np.nanmin(pp):.2e}")
cost = pd.read_csv(os.path.join(ROOT, "sonuclar", "tarama.csv")).set_index("sym").cost_rt_bp
rows = []
for c in ("h1", "h3"):
    m = (x[f"lag_t_{c}_is"] * x[f"lag_t_{c}_oos"] > 0) & (x[f"lag_t_{c}"].abs() >= 2)
    for _, r in x[m].iterrows():
        rows.append({"hedef": r.target, "oncu": r.leader, "h": c, "t": r[f"lag_t_{c}"], "t_is": r[f"lag_t_{c}_is"], "t_oos": r[f"lag_t_{c}_oos"],
                     "bp_per_sd": r[f"lag_bp_per_sd_{c}"], "maliyet": cost.get(r.target, np.nan), "p": r[f"p_lag_t_{c}"]})
    m = (x[f"catch_t_{c}_is"] * x[f"catch_t_{c}_oos"] > 0) & (x[f"catch_t_{c}"].abs() >= 2)
    for _, r in x[m].iterrows():
        rows.append({"hedef": r.target, "oncu": r.leader + " (yetişme)", "h": c, "t": r[f"catch_t_{c}"], "t_is": r[f"catch_t_{c}_is"], "t_oos": r[f"catch_t_{c}_oos"],
                     "bp_per_sd": r[f"catch_bp_per_sd_{c}"], "maliyet": cost.get(r.target, np.nan), "p": r[f"p_catch_t_{c}"]})
C = pd.DataFrame(rows)
print("  IS/OOS aynı işaret ve |t|>=2 satırlar (IS'i olan hedefler; kripto ETF'lerinin çoğunda IS yok):")
print(C.round(3).to_string(index=False) if len(C) else "  yok")
# hedef başına en güçlü gecikmeli satır (accepted/backup)
for T in ["IBIT", "ETHA", "SBIT", "BITI", "BITX", "ETHU", "GBTC", "FBTC", "ETHE"]:
    s = x[x.target == T]
    if not len(s): continue
    k = s.lag_t_h1.abs().idxmax()
    print(f"  {T}: en büyük |lag_t_h1| {s.loc[k,'leader']} t={s.loc[k,'lag_t_h1']:.2f} ({s.loc[k,'lag_bp_per_sd_h1']:.1f} bp/sd, p={s.loc[k,'p_lag_t_h1']:.4f}); "
          f"en büyük |catch_t_h1| {s.loc[s.catch_t_h1.abs().idxmax(),'leader']} t={s.catch_t_h1.abs().max():.2f}")

print("\n=== 2) Bağımsız regresyon: r_T(t+1..t+h) = a + b r_L(t) + c r_T(t)  (NW, 2024+ ETF dönemi; BTC/ETH 16:00 ET) ===")
BS = dk.btc_session("BTC-USD"); ES = dk.btc_session("ETH-USD")
lead = {"BTC_16ET": np.log(BS.c).diff(), "ETH_16ET": np.log(ES.c).diff(), "QQQ": np.log(lib.load("QQQ").c).diff(),
        "VIX_log": np.log(lib.vol_index("VIX")).diff()}
dg = lib.fred("DGS10")
if dg is not None:
    dg.index = pd.to_datetime(dg.index); lead["DGS10_fark"] = dg.astype(float).diff()
out = []
for T in ["IBIT", "ETHA", "SBIT", "BITI", "BITX", "ETHU", "GBTC", "FBTC", "ETHE"]:
    df = lib.load(T); ry = np.log(df.c).diff()
    for Ln, rl in lead.items():
        for h in (1, 3):
            fy = ry[::-1].rolling(h).sum()[::-1].shift(-1)
            d = pd.DataFrame({"fy": fy, "y": ry, "x": rl.reindex(ry.index)}).dropna()
            d = d[d.index >= "2024-01-11"]
            if len(d) < 150: continue
            b, t = nw(d.fy.values, np.column_stack([np.ones(len(d)), d.x.values, d.y.values]), h)
            half = len(d) // 2; ts = []
            for part in (d.iloc[:half], d.iloc[half:]):
                bb, tt_ = nw(part.fy.values, np.column_stack([np.ones(len(part)), part.x.values, part.y.values]), h); ts.append(tt_[1])
            out.append({"hedef": T, "oncu": Ln, "h": h, "n": len(d), "t_oncu": t[1], "bp_per_sd": b[1] * d.x.std() * 1e4, "t_kendi": t[2],
                        "t_1yari": ts[0], "t_2yari": ts[1], "p": 2 * st.norm.sf(abs(t[1])), "maliyet": cost.get(T, np.nan)})
O = pd.DataFrame(out); O["fdr"] = dk.bh(O.p.values)
O.to_csv(os.path.join(OUT, "leadlag_bagimsiz.csv"), index=False)
print(O[(O.p < 0.10)].round(3).to_string(index=False))
print(f"  toplam {len(O)} test; |t|>=2: {(O.t_oncu.abs()>=2).sum()}; BH-FDR geçen: {int(O.fdr.sum())}; iki yarıda aynı işaret ve |t|>=2: "
      f"{int(((O.t_1yari*O.t_2yari>0)&(O.t_oncu.abs()>=2)).sum())}; |bp/sd| > maliyet: {int((O.bp_per_sd.abs()>O.maliyet).sum())}")

print("\n=== 3) IBIT kapanış sapması (BTC 16:00 ET'ye göre) -> ertesi gün (yetişme; bayat kapanış kontrolü) ===")
IB = lib.load("IBIT")
d = pd.DataFrame({"rb": np.log(BS.c).diff(), "ri": np.log(IB.c).diff(), "on": np.log(IB.o.shift(-1) / IB.c), "cc": np.log(IB.c.shift(-1) / IB.c),
                  "id": np.log(IB.c.shift(-1) / IB.o.shift(-1))}).dropna()
d = d[d.index >= "2024-01-12"]
d["u"] = d.rb - d.ri   # >0: IBIT BTC'nin gerisinde kapandı
print(f"  sd(u)={d.u.std()*1e4:.1f} bp; n={len(d)}")
for yv in ("on", "id", "cc"):
    b, t = nw(d[yv].values, np.column_stack([np.ones(len(d)), d.u.values, d.ri.values]), 1)
    b0, t0 = nw(d[yv].values, np.column_stack([np.ones(len(d)), d.ri.values]), 1)
    print(f"  {yv}: u katsayısı {b[1]:.3f} (t={t[1]:.2f}), {b[1]*d.u.std()*1e4:.1f} bp/sd; kendi getirisi t={t[2]:.2f}")
q = d.u.quantile([0.1, 0.9])
hi = d[d.u >= q.iloc[1]]; lo = d[d.u <= q.iloc[0]]
print(f"  u üst %10 (IBIT geride): ertesi C->C ort {hi.cc.mean()*1e4:.1f} bp (n={len(hi)}, t={dk.tt(hi.cc):.2f}), gece {hi.on.mean()*1e4:.1f}; "
      f"alt %10: C->C {lo.cc.mean()*1e4:.1f} bp, gece {lo.on.mean()*1e4:.1f}; maliyet {cost['IBIT']:.1f} bp")

print("\n=== 4) Gerçek zamanlı: IBIT açılış boşluğu ~ BTC 16:00 -> 09:30 ET; BTC gece -> IBIT gün içi ===")
g = pd.DataFrame({"gap": np.log(IB.o / IB.c.shift(1)), "bon": np.log(BS.o / BS.c.shift(1)).reindex(IB.index), "idr": np.log(IB.c / IB.o),
                  "bon10": np.log(BS.o10 / BS.c.shift(1)).reindex(IB.index)}).dropna()
b, t = nw(g.gap.values, np.column_stack([np.ones(len(g)), g.bon.values]), 1)
print(f"  boşluk ~ BTC gece (09:30 tahmini): R²={g.gap.corr(g.bon)**2:.3f}, eğim {b[1]:.3f}; 10:00 fiyatıyla R²={g.gap.corr(g.bon10)**2:.3f}")
b, t = nw(g.idr.values, np.column_stack([np.ones(len(g)), g.bon.values]), 1)
print(f"  IBIT gün içi ~ BTC gece: eğim {b[1]:.3f} (t={t[1]:.2f})")
