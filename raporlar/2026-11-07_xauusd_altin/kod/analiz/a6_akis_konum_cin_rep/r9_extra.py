import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
from r1_cn import stock_resid, daily_ret, STK
T = viop_target(); days = T.index; r = T.ret; F = pd.read_parquet(f"{OUT}/r1_features_viop.parquet")
G15 = pd.Series(gold_at(days + pd.Timedelta(hours=15)), index=days); G07 = pd.Series(gold_at(days + pd.Timedelta(hours=7)), index=days)
C = pd.DataFrame({"s_r1": np.log(G15 / G15.shift(1)), "s_r5": np.log(G15 / G15.shift(5)), "s_0715": np.log(G15 / G07), "v_r1": r.shift(1)})
for k, h in [("r_HSI", 3), ("r_HSI", 1), ("comp_sum5", 1)]:
    xz = (F[k] - F[k].mean()) / F[k].std()
    for lab, m in [("tam", days == days), ("OOS", days > IS_END)]:
        d = pd.concat([T[f"fwd{h}"].rename("y"), xz.rename("x"), C], axis=1)[m].dropna()
        b, t, n = nw_t(d.y.values, np.column_stack([np.ones(len(d)), d.drop(columns="y").values]), max(h, 5)); print(f"{k} h{h} kontrollü {lab}: t={t[1]:.2f}")
# erken dönem lag profili (spot 15:00 takvimi)
bd = pd.bdate_range("2009-06-01", "2017-01-31"); p15 = pd.Series(gold_at(bd + pd.Timedelta(hours=15), 1.0), index=bd).dropna(); sr = np.log(p15).diff()
E = pd.DataFrame({f"res_{tk}": stock_resid(tk)[0].reindex(p15.index) for tk in STK}); comp = E.mean(axis=1).where(E.notna().sum(axis=1) >= 2)
m = (p15.index >= "2010-01-01") & (p15.index <= "2016-12-31")
print("erken 2010-2016 comp lag profili IC(x_t, s_r_{t+j}):", {j: (round(ic_t(comp[m], sr.shift(-j)[m], 5)["ic"], 3), round(ic_t(comp[m], sr.shift(-j)[m], 5)["t"], 2)) for j in range(1, 6)})
# VİOP döneminde spot takvimiyle j=2
print("2017+ VİOP takvimi comp j=2 yıllık IC:", pd.concat([F.comp.rename("x"), r.shift(-2).rename("y")], axis=1).dropna().groupby(lambda d: d.year).apply(lambda g: round(g.x.corr(g.y, method="spearman"), 3)).to_dict())
# rastgele işaret kuralı karşılaştırması: aynı ciroda rastgele işaretlerin OOS Sharpe dağılımı (h=5)
rng = np.random.default_rng(0); ro = r[r.index > IS_END]; sims = []
for _ in range(300):
    pr = pd.Series(rng.choice([-1.0, 1.0], len(days)), index=days); sims.append(stagger(pr, ro, 5)["sharpe"])
sims = np.array(sims); print("rastgele ±1 işaret, h=5 OOS Sharpe: ort", round(sims.mean(), 2), "sd", round(sims.std(), 2), "%95", round(np.quantile(sims, 0.95), 2), "| P(>=1.26)", round((sims >= 1.26).mean(), 3))
