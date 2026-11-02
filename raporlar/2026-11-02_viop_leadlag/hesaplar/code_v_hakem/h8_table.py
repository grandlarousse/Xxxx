"""H8: hisse bazında birleşik tablo (birincil test + VİOP + backtest + yurt içi)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, vh
from peers import PEERS, SECTOR
A = pd.read_csv(vh.RES + "/h2_per_stock_all_defs.csv"); P = A[A["def"].str.contains("BİRİNCİL")].set_index("stock")
L1 = A[A["def"].str.startswith("L1")].set_index("stock")
V = pd.read_csv(vh.RES + "/h6_viop_stock.csv").set_index("stock")
B = pd.read_csv(vh.RES + "/h3_backtest_stock.csv")
b1 = B[(B.thr == 1.0) & (B.cost == 16) & (B.hedef == "hedge'li")].set_index("stock")
b2 = B[(B.thr == 1.0) & (B.cost == 8) & (B.hedef == "ham")].set_index("stock")
D = pd.read_csv(vh.RES + "/h3_dom_stock.csv").set_index("stock")
T = pd.DataFrame({"sektör": P.sector, "n_emsal": pd.Series({s: len(PEERS[s]) for s in P.index}),
    "L1_ham_t": L1.t_ALL, "b_bps": P.b_ALL, "t": P.t_ALL, "q_BH47": P.q_ALL, "t_IS": P.t_IS, "t_OOS": P.t_OOS, "q_OOS": P.q_OOS,
    "VIOP_b": V.b_viop_h, "VIOP_t": V.t, "z1_hedge_brut_OOS": b1.gross_OOS, "z1_hedge_net16_OOS": b1.bps_OOS, "z1_ham_net8_OOS": b2.bps_OOS, "z1_ham_net8_IS": b2.bps_IS,
    "DOM_t": D.t_ALL})
T = T.sort_values("t", ascending=False); T.to_csv(vh.RES + "/h8_stock_table.csv")
pd.set_option("display.width", 250); print(T.round(2).to_string())
print("VİOP b>0:", int((T.VIOP_b > 0).sum()), "/47 ; VİOP t>2:", int((T.VIOP_t > 2).sum()), "; VİOP BH:", int((vh.bh(vh.p2(T.VIOP_t.values)) < 0.05).sum()))
print("IS t>1.96 olanlar ve OOS:", T[T.t_IS > 1.96][["t_IS", "t_OOS"]].round(2).to_dict("index"))
print("ham z1 net8 OOS>0 & IS>0:", T[(T.z1_ham_net8_OOS > 0) & (T.z1_ham_net8_IS > 0)].index.tolist())
