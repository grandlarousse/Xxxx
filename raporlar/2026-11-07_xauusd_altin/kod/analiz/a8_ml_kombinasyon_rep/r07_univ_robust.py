"""Adım 7: tek değişkenli adayların (A8-2/3/4) ek sağlamlık kontrolleri.
 - yıl yıl net Sharpe; 2026 hariç OOS; Sharpe'ın kaba anlamlılığı (günlük net pnl ortalamasının NW t'si)
 - A8-2 ile A8-4 sinyallerinin bağımlılığı (korelasyon, pozisyon uyumu)
 - Δ5 tanımına duyarlılık: spot iş günü satırı (rapor) vs VİOP satırı vs Treasury gözlem günü
 - drift nötr kıyas: aynı uzun oranına sahip rastgele pozisyonların OOS Sharpe dağılımı (500 permütasyon; blok=20 gün)"""
import numpy as np, pandas as pd, json
from rep_stats import split_ic, ic_test, bt_full, bt, nw_t_mean
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
v = pd.read_parquet(f"{OUT}/base_viop.parquet"); sp = pd.read_parquet(f"{OUT}/base_spot.parquet")
XV = pd.read_parquet(f"{OUT}/feat_viop.parquet")
SIG = {"A8-2": ("rt_nom2_d5", -1, 1), "A8-3": ("seg_last1h", +1, 5), "A8-4": ("rt_curve_2s10s_d5", +1, 1)}
rng = np.random.default_rng(7)
out = {}
for cid, (f, sg, h) in SIG.items():
    x = XV[f] * sg; pos = np.sign(x).fillna(0)
    z = bt(pos, v.ret, h); p = z["pnl"]
    yr = p.groupby(p.index.year).apply(lambda g: round(float(g.mean() / g.std() * np.sqrt(252)), 2))
    oos = bt(pos.loc["2022":], v.ret.loc["2022":], h)["pnl"]
    o26 = bt(pos.loc["2022":"2025"], v.ret.loc["2022":"2025"], h)
    o26dm = bt(pos.loc["2022":"2025"], v.ret.loc["2022":"2025"], h, demean=True)
    bh26 = bt(pd.Series(1.0, index=v.loc["2022":"2025"].index), v.ret.loc["2022":"2025"], 1, 0.0)
    # rastgele blok-pozisyon kıyası: OOS'ta aynı uzun oranı, 20 günlük bloklarla karıştırılmış pozisyon
    po = pos.loc["2022":].values; nb = int(np.ceil(len(po) / 20)); blocks = [po[i * 20:(i + 1) * 20] for i in range(nb)]
    sims = []
    for _ in range(500):
        perm = np.concatenate([blocks[i] for i in rng.permutation(nb)])[:len(po)]
        sims.append(bt(pd.Series(perm, index=pos.loc["2022":].index), v.ret.loc["2022":], h)["sharpe"])
    sims = np.array(sims); real = bt(pos.loc["2022":], v.ret.loc["2022":], h)["sharpe"]
    out[cid] = dict(yearly_sharpe=yr.to_dict(), oos_pnl_nw_t=round(nw_t_mean(oos, max(h, 5)), 3),
                    oos_ex2026=dict(sh=round(o26["sharpe"], 3), sh_dm=round(o26dm["sharpe"], 3), bh=round(bh26["sharpe"], 3)),
                    frac_long_oos=round(float((pos.loc["2022":] > 0).mean()), 3),
                    blockperm_oos=dict(real=round(real, 3), p_ge=round(float((sims >= real).mean()), 3), sim_mean=round(float(sims.mean()), 3), sim_p95=round(float(np.quantile(sims, 0.95)), 3)))
# A8-2 ile A8-4 bağımlılığı
a, b = -XV.rt_nom2_d5, XV.rt_curve_2s10s_d5
out["A8-2_vs_A8-4"] = dict(corr=round(float(a.corr(b)), 3), spearman=round(float(a.rank().corr(b.rank())), 3),
                           pos_agree=round(float((np.sign(a) == np.sign(b)).mean()), 3),
                           pos_agree_oos=round(float((np.sign(a) == np.sign(b)).loc["2022":].mean()), 3),
                           corr_d_nom10_d_nom2=round(float(XV.rt_nom10_d5.corr(XV.rt_nom2_d5)), 3))
# 2s10s'i Δnom10 ve Δnom2 bileşenlerine ayır (h=1 IC)
for nm, x in {"+d5_nom10": XV.rt_nom10_d5, "-d5_nom2": -XV.rt_nom2_d5, "+curve": XV.rt_curve_2s10s_d5}.items():
    st = split_ic(x, v.fwd1, 1); out[f"decomp_{nm}"] = {k: round(st[k], 3) for k in ("ic", "t", "t_is", "t_oos")}
# Δ5 tanımı duyarlılığı: Treasury gözlem günü (yayımlanan 5 gözlem geriye)
import glob
fs = sorted(glob.glob(f"{S}/data/treasury/daily_treasury_yield_curve_*.csv"))
tn = pd.concat([pd.read_csv(q) for q in fs]); tn["Date"] = pd.to_datetime(tn.Date, format="%m/%d/%Y"); tn = tn.drop_duplicates("Date").set_index("Date").sort_index()
d5_obs_nom2 = tn["2 Yr"].diff(5); d5_obs_curve = (tn["10 Yr"] - tn["2 Yr"]).diff(5)
# gün t'de bilinen son gözlem: tarih < t (D 22:00 UTC < t 15:00 ⇔ D ≤ t−1)
def asof_prev(s, idx):
    s = s.dropna(); i = s.index.searchsorted(pd.DatetimeIndex(idx), side="left") - 1
    return pd.Series(np.where(i >= 0, s.values[np.clip(i, 0, None)], np.nan), index=idx)
for nm, s_, sgn, cid in (("nom2", d5_obs_nom2, -1, "A8-2"), ("curve", d5_obs_curve, 1, "A8-4")):
    x = asof_prev(s_, v.index) * sgn
    st = split_ic(x, v.fwd1, 1)
    out[f"{cid}_treasury_obs_d5"] = dict(**{k: round(st[k], 3) for k in ("ic", "t", "t_is", "t_oos")}, oos_bt=bt_full(np.sign(x).fillna(0).loc["2022":], v.ret.loc["2022":], 1))
json.dump(out, open(f"{OUT}/univ_robust.json", "w"), indent=1, default=str)
for k, val in out.items(): print(k, val)
