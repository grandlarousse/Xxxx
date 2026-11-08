"""s9: şeffaflık — IS seçim ızgarasındaki TÜM konfigürasyonların OOS sonucu (seçim için kullanılmadı; komşu konfigürasyonların sağlamlığını gösterir)."""
from e2_common import *
d = load()
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); SIGA = pd.read_pickle(f"{OUT}/s7_signals.pkl")
rows = []
for cn, und, sign, src, grid in [("C1", "GLD", 1, SIG1, [(("GDX~GLD+SPY", k), h, q) for k in (5, 10) for h in (3, 5) for q in (0.7, 0.8)]),
                                  ("C2", "GDX", 1, SIG1, [(("GDX~GLD+SPY", k), h, q) for k in (1, 3) for h in (1, 3) for q in (0.7, 0.8)]),
                                  ("C2j", "GDXJ", 1, SIG1, [(("GDXJ~GLD+SPY", k), h, q) for k in (1, 3) for h in (1, 3) for q in (0.7, 0.8)]),
                                  ("C5", "GLD", 1, SIGA, [(k, h, q) for k in (1, 5) for h in (3, 5) for q in (0.7, 0.8)])]:
    for key, h, q in grid:
        pos = pos_from_signal(src[key], sign, q)
        oi = strat(d, pos, und, h, "base", None, "2017-12-31"); oo = strat(d, pos, und, h, "base", "2018-01-01", None)
        rows.append(dict(cand=cn, key=str(key), h=h, q=q, is_ideal=round(oi["ideal"]["sharpe"], 2), oos_ideal=round(oo["ideal"]["sharpe"], 2), oos_ideal_dm=round(oo["ideal_dm"]["sharpe"], 2),
                         oos_long=round(oo["long"]["sharpe"], 2), oos_long_dm=round(oo["long_dm"]["sharpe"], 2), oos_bh=round(oo["bh"]["sharpe"], 2)))
g = pd.DataFrame(rows); g.to_csv(f"{OUT}/s9_grid_oos.csv", index=False); pd.set_option("display.width", 250); print(g.to_string())
print(g.groupby("cand")[["is_ideal", "oos_ideal", "oos_ideal_dm", "oos_long", "oos_long_dm"]].median())
