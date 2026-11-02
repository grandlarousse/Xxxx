"""(c)(d) sağlamlık: plasebo gecikmeler, dairesel kaydırma null, blok bootstrap, aykırı değerler, yıllar,
alternatif sepetler/pencereler, kesitsel plasebo (aynı sinyal diğer VİOP hisselerinde), bayat açılış günleri."""
import numpy as np, pandas as pd, os
import vlib as V

out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
rng = np.random.default_rng(20261102)
X = pd.read_parquet(V.RES + "/panel_E3.parquet")
cal = V.bist_cal()
sig = X.US
tu = V.bist_decomp("TUPRS.IS").reindex(X.index)

# ---- plasebo gecikmeler ----
P("== Plasebo/gecikme profili: corr(US_REF_{t-k}, hedef_t), k=0 aynı gün (ABD t kapanışı BIST t kapanışından SONRA -> işlem dışı)")
usA = pd.concat({s: V.map_A(s, cal) for s in ["VLO", "MPC", "PSX", "PBF"]}, axis=1).mean(axis=1).reindex(X.index)
for k in range(0, 8):
    s = usA.shift(k) if k > 0 else usA
    r1, _, t1, n = V.corr_t(X.y_h, s); r2, _, t2, _ = V.corr_t(X.y, s); r3, _, t3, _ = V.corr_t(X.gap, s)
    P(f"  k={k}: y_h corr={r1:.3f} (t {t1:.2f}) | y corr={r2:.3f} (t {t2:.2f}) | gap corr={r3:.3f} (t {t3:.2f})")
# lag2..5 toplu (çok günlük sürüklenme)
for k in [2, 3]:
    m = V.hac(X.y_h, pd.concat([usA.shift(j).rename(f"l{j}") for j in range(1, k + 1)], axis=1))
    P(f"  y_h ~ lag1..{k}: t=", {c: round(m.tvalues[c], 2) for c in m.tvalues.index if c != 'const'})

# ---- ana strateji ----
res, pnl, pos, df = V.backtest(sig, X.y, cost_bps=0)
g = (pos * df.y)[pos != 0]
P(f"\n== Ana Z1 brüt: ALL n={len(g)} ort={1e4*g.mean():.1f} bps")

# dairesel kaydırma null: sinyal serisini (z-skorlu pozisyonları) rastgele >=60 gün kaydır
posv = pos.values; yv = df.y.values; n = len(yv); idx_oos = df.index >= "2021-01-01"
def stat(pv):
    a = pv != 0; return (pv[a] * yv[a]).mean(), (pv[a & idx_oos] * yv[a & idx_oos]).mean(), (pv[a & ~idx_oos] * yv[a & ~idx_oos]).mean()
obs = stat(posv)
null = np.array([stat(np.roll(posv, rng.integers(60, n - 60))) for _ in range(2000)])
P(f"Dairesel kaydırma null (2000): ALL gözlenen={1e4*obs[0]:.1f} bps, null ort={1e4*null[:,0].mean():.1f}, sd={1e4*null[:,0].std():.1f}, p(tek yön)={(null[:,0]>=obs[0]).mean():.4f}"
  f" | OOS p={(null[:,1]>=obs[1]).mean():.4f} | IS p={(null[:,2]>=obs[2]).mean():.4f}")

# durağan blok bootstrap (ort. blok 10 gün) işlem pnl'i için ALL/OOS ortalama GA
def block_boot(x, B=3000, L=10):
    x = np.asarray(x); n = len(x); out_ = np.empty(B)
    for b in range(B):
        idx = [];
        while len(idx) < n:
            st = rng.integers(0, n); ln = rng.geometric(1 / L); idx.extend(range(st, st + ln))
        idx = np.array(idx[:n]) % n; out_[b] = x[idx].mean()
    return np.percentile(out_, [2.5, 50, 97.5])
for lab, m in [("IS", g.index < "2021"), ("OOS", g.index >= "2021"), ("ALL", np.ones(len(g), bool))]:
    ci = block_boot(g[m].values)
    P(f"Blok bootstrap brüt ort. %95 GA {lab}: [{1e4*ci[0]:.1f}, {1e4*ci[2]:.1f}] bps | 8 bps eşiği aşma? {1e4*ci[0]>8} | 15? {1e4*ci[0]>15}")

# aykırı değer duyarlılığı
P("\n== Aykırı değer duyarlılığı (brüt bps/işlem)")
for lab, gg in [("tümü", g), ("en iyi 5 işlem hariç", g.drop(g.nlargest(5).index)), ("en iyi 10 hariç", g.drop(g.nlargest(10).index)),
                ("|y| %1/%99 winsor", None), ("2023 hariç", g[g.index.year != 2023]), ("2020 hariç", g[g.index.year != 2020])]:
    if gg is None:
        lo, hi = df.y.quantile([.01, .99]); yy = df.y.clip(lo, hi); gg = (pos * yy)[pos != 0]
    for per, m in [("IS", gg.index < "2021"), ("OOS", gg.index >= "2021")]:
        mm, t, nn = V.nw_mean(gg[m]); P(f"  {lab:22s} {per}: n={nn} ort={1e4*mm:.1f} t={t:.2f}")
P(f"  medyan işlem pnl IS={1e4*g[g.index<'2021'].median():.1f} OOS={1e4*g[g.index>='2021'].median():.1f} bps")

# bayat açılış günleri (o == önceki kapanış)
st = tu.stale_open.reindex(g.index).fillna(False).astype(bool)
P(f"\n== Açılış fiyatı == önceki kapanış olan günler: işlem payı={st.mean():.3f} | bu günlerde ort={1e4*g[st].mean():.1f} bps (n={int(st.sum())}) | diğer={1e4*g[~st].mean():.1f} bps")

# yıllara göre korelasyon
P("\n== Yıllara göre corr(US_REF_t-1, y_h) ve corr(US_REF_t-1, y)")
yr = []
for yv_, d in X.groupby(X.index.year):
    a = d[["y_h", "y", "US"]].dropna()
    yr.append({"yıl": yv_, "n": len(a), "c_yh": a.y_h.corr(a.US), "c_y": a.y.corr(a.US)})
YR = pd.DataFrame(yr); P(YR.round(3).to_string(index=False))
P(f"pozitif yıl oranı: y_h {float((YR.c_yh>0).mean()):.2f}, y {float((YR.c_y>0).mean()):.2f}")
YR.to_csv(V.RES + "/by_year_corr.csv", index=False)
rc = pd.concat([X.y_h, X.US], axis=1).dropna(); roll = rc.y_h.rolling(250).corr(rc.US)
P(f"250g kayan corr(y_h): min={roll.min():.3f} medyan={roll.median():.3f} maks={roll.max():.3f} | >0 oranı={float((roll.dropna()>0).mean()):.2f}")

# alternatif sepetler / tanımlar
P("\n== Alternatif sepet/tanımlar: corr(y_h) NW t ve Z1 tek bacak brüt IS/OOS bps")
alt = {}
for s in ["VLO", "MPC", "PSX", "PBF", "DK", "DINO", "CRAK", "XLE", "XOM", "CVX", "COP"]:
    try: alt[s] = V.map_A(s, cal).shift(1).reindex(X.index)
    except Exception as e: P("  yok:", s, e)
A4 = pd.concat({k: alt[k] for k in ["VLO", "MPC", "PSX", "PBF"]}, axis=1)
defs = {"US_REF (VLO,MPC,PSX,PBF)": A4.mean(axis=1),
        "VLO hariç": A4.drop(columns="VLO").mean(axis=1),
        "+DK,+DINO (6 rafineri)": pd.concat([A4, alt["DK"], alt["DINO"]], axis=1).mean(axis=1),
        "medyan(4)": A4.median(axis=1),
        "vol-ölçekli ort(4)": (A4 / A4.rolling(250, min_periods=60).std().shift(1)).mean(axis=1),
        "US_REF - XLE (rafineri spread)": A4.mean(axis=1) - alt["XLE"]}
for k in ["VLO", "MPC", "PSX", "PBF", "DK", "DINO", "CRAK", "XLE", "XOM", "CVX", "COP"]:
    if k in alt: defs[k] = alt[k]
rows = []
for k, s in defs.items():
    r, _, t, nn = V.corr_t(X.y_h, s)
    ri, _, ti, _ = V.corr_t(X.y_h[X.index < "2021"], s); ro, _, to, _ = V.corr_t(X.y_h[X.index >= "2021"], s)
    rr, _, _, _ = V.backtest(s[s.index >= "2014"], X.y, cost_bps=0)
    rows.append({"tanım": k, "c_yh": r, "t": t, "t_IS": ti, "t_OOS": to, "Z1_IS_bps": rr["IS"].get("mean_bps"), "Z1_OOS_bps": rr["OOS"].get("mean_bps"),
                 "Z1_IS_t": rr["IS"].get("t"), "Z1_OOS_t": rr["OOS"].get("t")})
AL = pd.DataFrame(rows); P(AL.round(2).to_string(index=False)); AL.to_csv(V.RES + "/alt_defs.csv", index=False)

# z penceresi / eşik ızgarası (Sharpe 8bps)
P("\n== z penceresi x eşik ızgarası: 8 bps net Sharpe IS/OOS (tek bacak)")
grid = []
for zw in [60, 120, 250, 500]:
    for thr in [0.5, 1.0, 1.5]:
        rr, _, _, _ = V.backtest(sig, X.y, cost_bps=8, thr=thr, zw=zw, minp=min(60, zw))
        grid.append({"zw": zw, "thr": thr, "IS_sh": rr["IS"].get("sharpe"), "OOS_sh": rr["OOS"].get("sharpe"), "IS_bps": rr["IS"].get("mean_bps"), "OOS_bps": rr["OOS"].get("mean_bps"),
                     "n_IS": rr["IS"].get("n"), "n_OOS": rr["OOS"].get("n")})
G = pd.DataFrame(grid); P(G.round(2).to_string(index=False))
P(f"8 bps net Sharpe > 0 oranı: IS {float((G.IS_sh>0).mean()):.2f}, OOS {float((G.OOS_sh>0).mean()):.2f}")

# IS içinde iki yarı ve OOS iki yarı
P("\n== Alt dönemler (Z1 brüt bps, t)")
for a_, b_ in [("2014", "2017"), ("2017", "2021"), ("2021", "2024"), ("2024", "2027")]:
    gg = g[(g.index >= a_) & (g.index < b_)]; m, t, nn = V.nw_mean(gg); P(f"  {a_}-{int(b_)-1}: n={nn} ort={1e4*m:.1f} t={t:.2f}")

# ---- kesitsel plasebo: aynı US_REF sinyali diğer VİOP hisselerinin hedge'li gün-içini öngörüyor mu? ----
P("\n== Kesitsel plasebo: corr(US_REF_t-1, hisse intra - XU100 intra), 47 VİOP + AYGAZ, 2014+")
VIOP = "AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK AYGAZ".split()
xu = V.bist_decomp("XU100.IS").reindex(X.index)
cs = []
for s in VIOP:
    p = f"{V.DATA}/daily/{s}.IS.parquet"
    if not os.path.exists(p): continue
    d = V.bist_decomp(s + ".IS").reindex(X.index)
    yh = d.intra - xu.intra
    r, _, t, nn = V.corr_t(yh, sig)
    ri, _, ti, _ = V.corr_t(yh[yh.index < "2021"], sig); ro, _, to, _ = V.corr_t(yh[yh.index >= "2021"], sig)
    cs.append({"hisse": s, "c": r, "t": t, "t_IS": ti, "t_OOS": to, "n": nn})
CS = pd.DataFrame(cs).sort_values("t", ascending=False)
P(CS.head(8).round(3).to_string(index=False)); P("..."); P(CS.tail(4).round(3).to_string(index=False))
P(f"|t|>2 olan hisse sayısı: {int((CS.t.abs()>2).sum())}/{len(CS)} (yalnızca şansla ~{0.05*len(CS):.1f} beklenir) | TUPRS sırası: {int((CS.t >= CS[CS.hisse=='TUPRS'].t.iloc[0]).sum())}")
CS.to_csv(V.RES + "/cross_section_placebo.csv", index=False)
open(V.RES + "/03_robust.txt", "w").write("\n".join(out))
