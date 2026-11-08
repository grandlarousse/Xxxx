"""Hakem: Çin artık sinyalinin zamana yoğunlaşması (yarım yıllık IC), PnL yoğunlaşması, Şanghay primi ile mekanizma testi."""
import sys, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); from lib_altin import load_viop, ic, backtest, IS_END, fwd
D = load_viop(); R = D["v_ret"]
F = pd.read_csv(f"{S}/out/a6_akis_konum_cin_adv/adv_cn_features.csv", index_col=0, parse_dates=True).reindex(D.index); x = F["comp"]
d = pd.concat([x.rename("x"), D.fwd5.rename("y")], axis=1).dropna()
hy = d.groupby([d.index.year, (d.index.month > 6).astype(int) + 1]).apply(lambda g: round(g.x.corr(g.y, method="spearman"), 3))
print("yarım yıllık IC (h5):"); print(hy.to_string())
pos = np.sign(x).fillna(0); b = backtest(pos, R, 5)
p = b["pnl"]; oos = p[p.index > IS_END]
srt = oos.sort_values(ascending=False)
print("\nOOS toplam PnL (log, %):", round(oos.sum() * 100, 2), "| en iyi 10 gün:", round(srt.head(10).sum() * 100, 2), "| en iyi 20:", round(srt.head(20).sum() * 100, 2), "| en kötü 10:", round(srt.tail(10).sum() * 100, 2))
print("en iyi 10 gün:", [d_.strftime("%Y-%m-%d") for d_ in srt.head(10).index])
oo = oos.drop(srt.head(10).index); print("en iyi 10 gün hariç OOS Sharpe:", round(oo.mean() / oo.std() * np.sqrt(252), 2), " orijinal:", round(oos.mean() / oos.std() * np.sqrt(252), 2))
cum = oos.cumsum(); print("OOS kümülatif PnL yıl sonları (%):", (cum.groupby(cum.index.year).last() * 100).round(2).to_dict())
# mekanizma: artık, gelecek Şanghay primi değişimini öngörüyor mu? (Çin talebi -> prim artışı beklenir)
B = pd.read_csv(f"{S}/out/a6_akis_konum_cin/b_shfe_features.csv", index_col=0, parse_dates=True).reindex(D.index)
print("\nb_shfe kolonları:", [c for c in B.columns][:20])
for col in [c for c in ("au_dprem1", "etf_dprem1") if c in B]:
    dp = B[col]
    for k in (0, 1):
        y = sum(dp.shift(-i) for i in range(1 + k, 6 + k)) if k else dp
        r = ic(x, y, 5); ro = ic(x[D.index > IS_END], y[D.index > IS_END], 5)
        print(f"  corr(x_t, {col} {'gelecek 1..5' if k else 'aynı gün'}): ic={r['ic']:+.3f} t={r['t']:+.2f} | OOS ic={ro['ic']:+.3f} t={ro['t']:+.2f}")
