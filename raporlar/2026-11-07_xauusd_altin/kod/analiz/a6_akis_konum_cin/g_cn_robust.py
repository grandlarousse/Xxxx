"""(g) Çin altın hisseleri artık getirisi sinyali için ek sağlamlık:
 - beta tanımı (yalnız altın; 120/500g pencere), birikimli artık (3g/5g toplam), artık oto-korelasyonu
 - beşli dilim (quintile) ortalamaları, 2026 hariç OOS, spot hedefle (15:00->15:00 UTC) aynı test
 - "Çin talebi" bileşik endeksi: z(artık bileşik) + z(518880 prim Δ) + z(SHFE prim Δ)  (ön-tanımlı eşit ağırlık)
Bilgi zamanı: 600547.SS 07:00 UTC, 1818/2899.HK 08:10 UTC, 518880.SS ve SHFE 07:00 UTC — hepsi gün t, 15:00 UTC'den ≥6,8 saat önce.
"""
from common import *
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

rd = lambda f: pd.read_csv(f"{OUT}/{f}", index_col=0, parse_dates=True)
A = rd("c_asia_features.csv"); B = rd("b_shfe_features.csv")

# c_asia.py'deki yardımcıları yeniden kullan (kayıt yapmadan): ret_known, gold_window_ret
src = open(f"{OUT}/c_asia.py").read().split("av = pd.DataFrame(")[0]
ns = {}; exec(src, ns)
ret_known, gold_window_ret, STK = ns["ret_known"], ns["gold_window_ret"], ns["STK"]

def resid(P, tk, mk, win=250, use_mkt=True):
    rs = ret_known(P, tk); rm = ret_known(P, mk); g = gold_window_ret(P, tk)
    cols = ["g", "m"] if use_mkt else ["g"]
    dd = pd.concat([rs.rename("y"), g.rename("g"), rm.rename("m")], axis=1)
    ok = dd[["y"] + cols].notna().all(axis=1)
    m = RollingOLS(dd.y[ok], sm.add_constant(dd[cols][ok]), window=win, min_nobs=int(win * 0.6)).fit()
    b = m.params.shift(1)
    res = dd.y[ok] - b["const"] - sum(b[c] * dd[c][ok] for c in cols)
    return res.reindex(P.index)

def comp(P, **kw):
    R_ = pd.concat([resid(P, tk, mk, **kw) for tk, (mk, hh) in STK.items()], axis=1)
    return R_.mean(axis=1, skipna=True).where(R_.notna().sum(axis=1) >= 2)

rows = []
base = A["cn_gold_res_comp"].reindex(D.index)
print("artık bileşik oto-korelasyon lag1..5:", [round(base.autocorr(k), 3) for k in range(1, 6)])
variants = {
    "comp_goldonly_beta": comp(D, use_mkt=False),
    "comp_win120": comp(D, win=120),
    "comp_win500": comp(D, win=500),
    "comp_sum3": base.rolling(3, min_periods=2).sum(),
    "comp_sum5": base.rolling(5, min_periods=3).sum(),
}
for k, v in variants.items():
    rows += T(v, "asia_robust", f"cn_{k}", f"Çin altın hisse artığı varyantı: {k}", hs=(1, 3, 5), note="robust varyant")

# Çin talebi bileşik (ön-tanımlı): z-skorlar 250g geçmiş std ile
def zpast(x): return x / x.rolling(250, min_periods=120).std().shift(1)
cdi = pd.concat([zpast(base), zpast(B["etf_dprem1"].reindex(D.index)), zpast(B["au_dprem1"].reindex(D.index))], axis=1)
cdi = cdi.mean(axis=1, skipna=True).where(cdi.notna().sum(axis=1) >= 2)
rows += T(cdi, "asia", "cn_demand_composite", "Çin talebi bileşik: z(hisse artığı)+z(518880 prim Δ)+z(SHFE prim Δ)", note="ön-tanımlı eşit ağırlık")
df = save(rows, "g_cn_variants"); show(df)

# beşli dilim ortalamaları (fwd5, bps) — IS ve OOS ayrı
q = []
for per, m in [("IS", D.index <= IS_END), ("OOS", D.index > IS_END)]:
    x = base[m]; y = D["fwd5"][m]
    d = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    d["q"] = pd.qcut(d.x, 5, labels=False) + 1
    g = d.groupby("q").y.agg(["mean", "count"]); g["mean"] *= 1e4
    for qq, r in g.iterrows(): q.append(dict(period=per, quintile=int(qq), fwd5_bps=round(r["mean"], 1), n=int(r["count"])))
qd = pd.DataFrame(q); qd.to_csv(f"{OUT}/g_cn_quintiles.csv", index=False); print(qd.pivot(index="quintile", columns="period", values="fwd5_bps"))

# 2026 hariç OOS (Ocak-Şubat 2026 aşırı dönemi ve 2026 güçlü yıl etkisi)
m = (D.index > IS_END) & (D.index < "2026-01-01")
for h in (3, 5):
    r = ic(base[m], D[f"fwd{h}"][m], max(h, 5)); print(f"OOS 2022-2025 h={h}: IC={r['ic']:.3f} t={r['t']:.2f} n={r['n']}")
    register(AG, "asia_robust", "cn_gold_res_comp_oos_ex2026", "Çin altın hisse artığı, OOS 2022-2025 (2026 hariç)", h, dict(ic=r["ic"], t=r["t"], n=r["n"]), "robust")

# spot hedef (spot 15:00 UTC, VİOP günleri) — VİOP mikro yapısından bağımsız mı?
sp_fwd = {h: fwd(np.log(D.xau_p15).diff(), h) for h in (3, 5)}
for h in (3, 5):
    st = split_stats(base, sp_fwd[h], h); print(f"spot hedef h={h}: IC={st['ic']:.3f} t={st['t']:.2f} IS t={st['t_is']:.2f} OOS t={st['t_oos']:.2f}")
    register(AG, "asia_robust", "cn_gold_res_comp_spot_target", "Çin altın hisse artığı -> spot 15:00 UTC fwd", h, st, "robust: spot hedef")

# Strateji: sign kuralı, h=5, 2026 hariç ve uç dönem hariç OOS Sharpe
pos = np.sign(base).fillna(0)
for lab, msk in [("OOS 2022-2025", (R.index > IS_END) & (R.index < "2026-01-01")), ("OOS uç dönem hariç", (R.index > IS_END) & ~EXTREME.values)]:
    rr = R.copy(); rr[~msk] = np.nan; rr = rr.dropna()
    b = backtest(pos.reindex(rr.index), rr, 5); bd = backtest(pos.reindex(rr.index), rr, 5, demean=True)
    print(lab, "Sharpe net 5bps:", round(b["sharpe"], 2), "demeaned:", round(bd["sharpe"], 2))

# Sonradan (post-hoc) varyant: 5g birikimli artık -> h=1/3 işaret kuralı (forking-path uyarısı: tanım sonuçlara bakıldıktan sonra seçildi)
s5 = variants["comp_sum5"]
tabs = []
for h in (1, 3):
    pos5 = np.sign(s5).fillna(0)
    tb = legs_table(pos5, h, f"cn_comp_sum5|sign"); tabs.append(tb)
    rs = rule_stats(pos5, h); register(AG, "asia_rule", "cn_comp_sum5_sign", "5g birikimli Çin hisse artığı işaret kuralı (post-hoc)", h, rs, "post-hoc varyant")
    yp = yearly_pnl(pos5, h)
    sel = tb[(tb.leg == "LS") & (tb.cost_bps == 5)].set_index("period")
    sel10 = tb[(tb.leg == "LS") & (tb.cost_bps == 10)].set_index("period")
    lg = tb[(tb.leg == "long_leg") & (tb.cost_bps == 5)].set_index("period"); sh = tb[(tb.leg == "short_leg") & (tb.cost_bps == 5)].set_index("period")
    print(f"sum5 sign h={h}: Sharpe full/IS/OOS", sel.sharpe.to_dict(), "OOS dm", sel.sharpe_dm["oos"], "OOS 10bps", sel10.sharpe["oos"],
          "long OOS", lg.sharpe["oos"], lg.sharpe_dm["oos"], "short OOS", sh.sharpe["oos"], sh.sharpe_dm["oos"], "sig chg/yr", round(float((pos5.diff().abs() > 0).sum() / len(pos5) * 252), 1))
    print("  yıllık:", yp.to_dict())
pd.concat(tabs).to_csv(f"{OUT}/g_cn_sum5_backtests.csv", index=False)
# erken dönem (spot 2010-2016) 5g birikimli
Xs = ns["build"](SP)["cn_gold_res_comp"].rolling(5, min_periods=3).sum()
for r_ in T_early(Xs, "asia", "cn_comp_sum5", "5g birikimli Çin hisse artığı", hs=(1, 3, 5)):
    print("erken", r_["h"], round(r_["ic"], 3), round(r_["t"], 2), r_["yrs_same"])
