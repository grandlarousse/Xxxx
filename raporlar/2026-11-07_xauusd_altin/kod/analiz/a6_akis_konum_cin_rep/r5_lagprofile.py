import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
T = viop_target(); r = T.ret; F = pd.read_parquet(f"{OUT}/r1_features_viop.parquet")
for k in ("comp", "res_600547.SS", "r_HSI"):
    x = F[k]
    rows = {}
    for j in range(1, 9):
        y = r.shift(-j)
        f = ic_t(x, y, 5); o = ic_t(x[x.index > IS_END], y[y.index > IS_END], 5); i = ic_t(x[x.index <= IS_END], y[y.index <= IS_END], 5)
        rows[j] = (round(f["ic"], 3), round(f["t"], 2), round(i["t"], 2), round(o["t"], 2))
    print(k, "IC(x_t, r_{t+j}) -> (ic, t, t_IS, t_OOS):"); [print("   j=", j, v) for j, v in rows.items()]
# uç dönem / roll hariç, 2026 hariç
roll = T.code != T.code.shift(1); rn = roll | roll.shift(-1, fill_value=False) | roll.shift(1, fill_value=False)
ext = ((T.index >= "2020-03-01") & (T.index <= "2020-04-30")) | ((T.index >= "2026-01-01") & (T.index <= "2026-02-28"))
x = F["comp"]
st = split(x.where(~(rn | ext)), T.fwd5, 5); print("comp h5 roll±1 & uç hariç: t", round(st["t"], 2), "OOS", round(st["t_oos"], 2))
m = T.index < "2026-01-01"; st = split(x[m], T.fwd5[m], 5); print("comp h5 2026 hariç: t", round(st["t"], 2), "OOS", round(st["t_oos"], 2), "IC_OOS", round(st["ic_oos"], 3))
pos = np.sign(x).fillna(0)
rr = r[(r.index > IS_END) & ~ext]; print("comp h5 OOS uç hariç Sharpe", round(stagger(pos, rr, 5)["sharpe"], 2))
rr = r[(r.index > IS_END) & (r.index < "2026-01-01")]; print("comp h5 OOS 2022-2025 Sharpe", round(stagger(pos, rr, 5)["sharpe"], 2), "dm", round(stagger(pos, rr, 5, demean=True)["sharpe"], 2))
# yıllık Sharpe
pn = stagger(pos, r, 5)["pnl"]; print("yıllık net Sharpe:", (pn.groupby(pn.index.year).apply(lambda s: s.mean() / s.std() * np.sqrt(252))).round(2).to_dict())
# OOS PnL'in kaç günde yoğunlaştığı
po = stagger(pos, r[r.index > IS_END], 5)["pnl"]; srt = po.sort_values(ascending=False)
print("OOS toplam net log getiri %", round(po.sum() * 100, 1), "| en iyi 10 gün katkısı %", round(srt.head(10).sum() * 100, 1), "| en iyi 10 gün hariç Sharpe", round(srt.iloc[10:].mean() / srt.iloc[10:].std() * np.sqrt(252), 2))
