"""BT5 (5 dk): XU030 5 dk şoku (|z|>2, z geçmiş 500 bar) -> hisseye bir SONRAKİ bardan gir, h=3 bar (15 dk) tut. Yahoo m5 (~60 gün).
Maliyet: 8 / 15 bps VE tik-farkındalıklı maliyet (1 fiyat adımı spread + 4 bps komisyon; pay vadelisinde spread genellikle daha geniş).
IS = ilk yarı, OOS = ikinci yarı (gün bazında)."""
from ye_common import *
import s4_intraday as S4
S4.SRC, S4.KIND = "yh", "m5"
T = pd.read_csv(RES + "/tickinfo_yh_m5.csv", index_col=0)
x = S4.bar_ret(S4.px("XU030"))
mu = x["r"].rolling(500, min_periods=200).mean().shift(1); sd = x["r"].rolling(500, min_periods=200).std().shift(1)
z = (x["r"] - mu) / sd
days = pd.DatetimeIndex(sorted(x["date"].unique())); mid = days[len(days) // 2]
H = 3; rows = []
for s in VIOP:
    p = S4.px(s)
    if p is None: continue
    S_ = S4.bar_ret(p)
    df = pd.concat([S_["r"].rename("y"), S_["date"], z.rename("z")], axis=1, join="inner")
    fwd = sum(df["y"].shift(-k) for k in range(1, H + 1))  # t+1..t+H (giriş: şok barının KAPANIŞINDAN sonra)
    same = df["date"].shift(-H) == df["date"]; fwd[~same] = np.nan
    sig = np.sign(df["z"]).where(df["z"].abs() > 2, 0)
    pnl_g = (sig * fwd)[sig != 0].dropna()
    tick_cost = T.loc[s, "rel_tick_bps"] + 4 if s in T.index else np.nan
    for cn, c in [("8", 8), ("15", 15), ("tik+4", tick_cost)]:
        pn = pnl_g - c / 1e4
        r = {"stock": s, "cost": cn, "cost_bps": c, "n": len(pn)}
        for k, msk in [("IS", pn.index.map(lambda t: (t + pd.Timedelta(hours=3)).normalize() < mid)), ("OOS", pn.index.map(lambda t: (t + pd.Timedelta(hours=3)).normalize() >= mid))]:
            q = pn[np.asarray(msk, bool)]
            r[f"{k}_n"] = len(q); r[f"{k}_mean_bps"] = 1e4 * q.mean() if len(q) else np.nan; r[f"{k}_t"] = q.mean() / q.std() * np.sqrt(len(q)) if len(q) > 5 else np.nan
        r["gross_bps"] = 1e4 * pnl_g.mean(); rows.append(r)
R = pd.DataFrame(rows); R.to_csv(RES + "/bt_m5_shock.csv", index=False)
pd.set_option("display.width", 200)
print(R.groupby("cost")[["gross_bps", "IS_mean_bps", "OOS_mean_bps", "OOS_t"]].median().round(2))
print(R[R.cost == "tik+4"].sort_values("gross_bps", ascending=False).head(12).round(2).to_string())
print("OOS>0 hisse sayısı (8bps):", (R[R.cost == "8"].OOS_mean_bps > 0).sum(), "/", (R.cost == "8").sum(), " (tik+4):", (R[R.cost == "tik+4"].OOS_mean_bps > 0).sum())
