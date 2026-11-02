"""Görev 2: likidite / işlenebilirlik tablosu -> out/y_viop_likidite.csv
Pencere: son 252 VİOP günü (W12) + 2023-01+ (W23). Hacim tüm vadeler toplamı (bülten; akşam seansı hacmi T+1 bültenine dahil olabilir, fiyatlar değil).
Spread tahmincileri 'L' (t-1 AP'ye göre seçilen) sözleşmenin günlük OHLC'sinden:
  Roll (1984): s = 2*sqrt(-cov(dp_t, dp_{t-1})) (cov>0 -> tanımsız)
  Corwin-Schultz (2012) 2-gün H/L, aylık ortalama, negatif -> 0
  Abdi-Ranaldo (2017) CHL: s^2 = 4*E[(c_t-eta_t)(c_t-eta_{t+1})], aylık, negatif -> 0
Gidiş-dönüş maliyet = tahmini tam spread (giriş+çıkışta yarım spread) + 2 x komisyon (kurumsal ~onbinde 2 + %5 BSMV = 2,1 bps/yön; borsa payı dahil varsayımı)
  + piyasa etkisi (karekök: 2 x 0,5 x sigma_gün x sqrt(Q/ADV), Q=1 mn TL).
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
D = pd.read_parquet(RES + "/daily_all.parquet")
F = load_panel()
COMM_SIDE = 2.1  # bps/yön (onbinde 2 + BSMV); bireysel tarife onbinde 5-10 olabilir -> hassasiyet sütunu
usd = D[D["und"] == "USDTRY"].set_index("date")["c1_settle"]
dates = pd.DatetimeIndex(sorted(D["date"].unique())); W12 = dates[-252]; LAST = dates[-1]
def cs_spread(h, l):
    # Corwin-Schultz 2-day
    lh = np.log(h / l) ** 2
    beta = lh + lh.shift(-1)
    h2 = pd.concat([h, h.shift(-1)], axis=1).max(axis=1); l2 = pd.concat([l, l.shift(-1)], axis=1).min(axis=1)
    gamma = np.log(h2 / l2) ** 2
    k = 3 - 2 * np.sqrt(2)
    alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
    s = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
    return s
def ar_terms(h, l, c):
    lc, eta = np.log(c), (np.log(h) + np.log(l)) / 2
    return 4 * (lc - eta) * (lc - eta.shift(-1))
def spreads(g):
    """g: tek dayanak, L sözleşmesi; aynı sözleşmenin ardışık günleri kullanılır."""
    g = g[(g["L_trades"] > 0) & (g["L_high"] > 0) & (g["L_low"] > 0)].copy()
    out = {}
    cs_all, ar_all, rr = [], [], []
    for code, x in g.groupby("L_code"):
        x = x.sort_index()
        if len(x) < 3: continue
        cs = cs_spread(x["L_high"], x["L_low"]); ar = ar_terms(x["L_high"], x["L_low"], x["L_close"])
        cs_all.append(cs); ar_all.append(ar)
        dp = np.log(x["L_close"]).diff()
        rr.append(pd.DataFrame({"a": dp, "b": dp.shift(1)}))
    if not cs_all: return dict(sp_cs=np.nan, sp_ar=np.nan, sp_roll=np.nan)
    cs = pd.concat(cs_all).sort_index(); ar = pd.concat(ar_all).sort_index(); R = pd.concat(rr).dropna()
    csm = cs.clip(lower=0).groupby(cs.index.to_period("M")).mean()
    arm = ar.groupby(ar.index.to_period("M")).mean().clip(lower=0) ** 0.5
    cov = np.cov(R["a"], R["b"])[0, 1] if len(R) > 30 else np.nan
    out["sp_cs"] = 1e4 * csm.median(); out["sp_ar"] = 1e4 * arm.median()
    out["sp_roll"] = 1e4 * 2 * np.sqrt(-cov) if (cov == cov and cov < 0) else np.nan
    out["roll_cov_pos"] = bool(cov == cov and cov >= 0)
    return out
def roll_days(u):
    """Her vade döngüsünde, ikinci vadenin hacmi ön vadeyi ilk kez geçtiği gün -> ön vadenin bitişine kalan iş günü."""
    x = F[(F["und"] == u) & (F["expiry"] >= F["date"])]
    res = []
    for exp, gg in x.groupby("expiry"):
        # bu vade ön vade iken (rank1) günler
        days = dates[(dates <= exp)]
        sub = x[x["date"].isin(days[-30:])]
        piv = sub.pivot_table(index="date", columns="expiry", values="value_tl", aggfunc="sum")
        if exp not in piv.columns: continue
        nxt = [c for c in piv.columns if c > exp]
        if not nxt: continue
        n1 = min(nxt)
        cross = piv.index[(piv[n1] > piv[exp])]
        if len(cross) == 0: res.append(0); continue
        first = cross.min(); res.append(int(((dates > first) & (dates <= exp)).sum()))
    return np.median(res) if res else np.nan, len(res)
rows = []
for u in ALL:
    g = D[D["und"] == u].set_index("date").sort_index()
    if g.empty: continue
    w = g[g.index >= W12]; w23 = g[g.index >= "2023-01-01"]
    px = g["c1_settle"].iloc[-1]
    mult = F.loc[(F["und"] == u) & (F["date"] >= W12), "mult"].median()
    tk = tick(u, px, LAST)
    us = usd.reindex(w.index)
    sig = w["L_r_set"].std()
    adv_med = w["value_tl"].median()
    sp = spreads(w)
    rd, nroll = roll_days(u)
    first = g.index[g["value_tl"] > 0].min()
    tick_bps_last = 1e4 * tk / px
    # 12 aylık medyan: her gün o günün fiyatına göre tik (bantlı kural 02.12.2024+)
    tb = [1e4 * tick(u, p_, d_) / p_ for d_, p_ in w["c1_settle"].dropna().items()]
    tick_bps = float(np.median(tb)) if tb else tick_bps_last
    # Wyart vd. (2008) 'spread ~ sigma_gün/sqrt(N_işlem)' yasası (c=1); alt sınır 1 tik. Muhafazakâr: max(1,5 tik, 2*sigma/sqrt(N)).
    ntr = w["trades"].median()
    sp_wy = 1e4 * sig / np.sqrt(ntr) if ntr and ntr > 0 else np.nan
    sp_est = max(tick_bps, sp_wy) if sp_wy == sp_wy else np.nan
    sp_cons = max(1.5 * tick_bps, 2 * sp_wy) if sp_wy == sp_wy else np.nan
    # aktif gün oranı (en az 1 işlem)
    act = (w["trades"] > 0).mean()
    impact_1m = 2 * 0.5 * sig * np.sqrt(1e6 / adv_med) * 1e4 if adv_med > 0 else np.nan
    impact_10m = 2 * 0.5 * sig * np.sqrt(1e7 / adv_med) * 1e4 if adv_med > 0 else np.nan
    rows.append(dict(und=u, tv_ticker=TV[u], first_trade=first.date(), n_days_12m=len(w), active_day_frac=round(act, 3),
                     contract_size=round(mult, 3) if mult == mult else np.nan, last_settle=px, tick=tk, tick_bps_last=tick_bps_last, tick_bps=tick_bps,
                     contract_value_tl=px * (mult if mult == mult else np.nan),
                     adv_tl_mean_12m=w["value_tl"].mean(), adv_tl_median_12m=adv_med, adv_usd_median_12m=(w["value_tl"] / us).median(),
                     adv_tl_median_2023p=w23["value_tl"].median(), adv_usd_median_2023p=(w23["value_tl"] / usd.reindex(w23.index)).median(),
                     trades_median_12m=w["trades"].median(), trades_mean_12m=w["trades"].mean(),
                     avg_trade_tl=(w["value_tl"].sum() / max(w["trades"].sum(), 1)),
                     oi_contracts_median_12m=w["oi"].median(), oi_tl_median_12m=w["oi_tl"].median(),
                     front_vol_share_12m=(w["c1_value_tl"].fillna(0).sum() / w["value_tl"].sum()) if w["value_tl"].sum() > 0 else np.nan,
                     vmax_is_front_frac=(w["vmax_rank"] == 1).mean(), roll_bdays_before_expiry=rd, n_roll_cycles=nroll,
                     os_value_share=(w["os_value"].sum() / w["value_tl"].sum()) if w["value_tl"].sum() > 0 else np.nan,
                     spot_adv_tl_median_12m=w["s_value_tl"].median() if "s_value_tl" in w else np.nan,
                     fut_spot_vol_ratio=(w["value_tl"].median() / w["s_value_tl"].median()) if ("s_value_tl" in w and w["s_value_tl"].median() > 0) else np.nan,
                     sigma_daily_bps=1e4 * sig, sp_roll_bps=sp.get("sp_roll"), sp_cs_bps=sp.get("sp_cs"), sp_ar_bps=sp.get("sp_ar"), sp_wyart_bps=sp_wy,
                     spread_est_bps=sp_est, spread_cons_bps=sp_cons, comm_rt_bps=2 * COMM_SIDE, impact_1m_bps=impact_1m, impact_10m_bps=impact_10m))
L = pd.DataFrame(rows)
# Gerçekçi gidiş-dönüş: küçük emir (<=~0,1% ADV): spread + komisyon; 1 mn TL: + etki. Spread için 'tik tabanı' ile tahminci medyanı arasında
# muhafazakâr seçim; çok likit sözleşmelerde H-L tahmincileri volatiliteden şişer -> alt sınır (1 tik + komisyon) de verilir.
L["rt_cost_floor_bps"] = L["tick_bps"] + L["comm_rt_bps"]
L["rt_cost_small_bps"] = L["spread_est_bps"] + L["comm_rt_bps"]
L["rt_cost_cons_bps"] = L["spread_cons_bps"] + L["comm_rt_bps"]
L["rt_cost_now_bps"] = np.maximum(L["tick_bps_last"], L["sp_wyart_bps"]) + L["comm_rt_bps"]  # son fiyatın tik bandıyla (ileriye dönük)
# vade geçişi: vadeye k iş günü kala ön vadenin hacim payı (medyan, son 3 yıl)
F2 = F[(F["expiry"] >= F["date"]) & (F["date"] >= dates[-756])].copy()
F2["bd_left"] = [int(((dates > d) & (dates <= e)).sum()) for d, e in zip(F2["date"], F2["expiry"])]
F2["rank"] = F2.groupby(["und", "date"])["expiry"].rank(method="first")
tot = F2.groupby(["und", "date"])["value_tl"].transform("sum")
F2["sh"] = F2["value_tl"] / tot
fr = F2[F2["rank"] == 1]
for k in [0, 1, 2, 5]:
    L[f"front_share_bd{k}"] = L["und"].map(fr[fr["bd_left"] == k].groupby("und")["sh"].median())
L["rt_cost_1m_bps"] = L["rt_cost_small_bps"] + L["impact_1m_bps"]
L["rt_cost_retail_bps"] = L["spread_est_bps"] + 2 * 10.5  # bireysel onbinde 10 + BSMV
def cls(r):
    a = r["adv_tl_median_12m"]; c = r["rt_cost_small_bps"]
    k = "A" if a >= 1e9 else "B" if a >= 2.5e8 else "C" if a >= 5e7 else "D"
    if c == c and c > 25 and k in ("A", "B"): k = "C"  # tik maliyeti yüksek (düşük fiyatlı pay) -> düşür
    return k
L["liq_class"] = L.apply(cls, axis=1)
L.to_csv(RES + "/liquidity_raw.csv", index=False)
show = ["und", "first_trade", "contract_size", "tick_bps", "adv_tl_median_12m", "adv_usd_median_12m", "trades_median_12m", "avg_trade_tl", "oi_tl_median_12m",
        "front_vol_share_12m", "roll_bdays_before_expiry", "fut_spot_vol_ratio", "sigma_daily_bps", "sp_roll_bps", "sp_cs_bps", "sp_ar_bps", "sp_wyart_bps", "spread_est_bps",
        "rt_cost_floor_bps", "rt_cost_small_bps", "rt_cost_cons_bps", "rt_cost_1m_bps", "liq_class"]
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
T = L[show].copy()
for c in ["adv_tl_median_12m", "oi_tl_median_12m", "avg_trade_tl"]: T[c] = (T[c] / 1e6).round(2)
T["adv_usd_median_12m"] = (T["adv_usd_median_12m"] / 1e6).round(2)
print(T.sort_values("adv_tl_median_12m", ascending=False).round(2).to_string(index=False))
