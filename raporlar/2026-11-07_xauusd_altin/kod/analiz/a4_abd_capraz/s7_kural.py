"""s7: Nihai kurallar (C1 madenci artığı h=3 tercile eşleme; C2 eğri Δ5 h=1 z_kırp) — işlem sayısı/yıl, yıl yıl, OOS buy&hold kıyası,
spot panelde 2010–2016 erken dönem backtest (s_ret, 15:00→15:00 UTC), 5/10 bps. Kayıt: s7_ öneki."""
import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *
reg_reset("s7_")
d = load_viop(); sp = load_spot()

def c1_signal(df):
    rm = np.log(df.y_GDXJ).diff(); rg = np.log(df.y_GLD).diff()
    b = rm.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
    z = zscale(rm - b * rg)
    return z, np.sign(z).where(z.abs() > 0.43, 0.0).where(z.notna(), 0.0)

def c2_signal(df):
    z = zscale((df.ust_nom10 - df.ust_nom2).diff(5))
    return z, (z / 2).clip(-1, 1).fillna(0.0)

RULES = {"C1_GDXJ_artik_h3": (c1_signal, 3), "C2_egri_d5_h1": (c2_signal, 1)}
out = {}
for nm, (fn, H) in RULES.items():
    z, pos = fn(d)
    o = {}
    for per, m in (("full", d.index == d.index), ("is", d.index <= IS_END), ("oos", d.index > IS_END)):
        a = backtest(pos[m], d.v_ret[m], H); b = backtest(pos[m], d.v_ret[m], H, demean=True); c = backtest(pos[m], d.v_ret[m], H, cost_bps=10)
        bh = backtest(pd.Series(1.0, index=d.index[m]), d.v_ret[m], 1, 0)
        o[per] = dict(sharpe5=round(a["sharpe"], 2), sharpe5_dm=round(b["sharpe"], 2), sharpe10=round(c["sharpe"], 2), ann5_pct=round(a["ann_ret"] * 100, 2),
                      t_gunluk=round(a["t_daily"], 2), bh_sharpe=round(bh["sharpe"], 2), bh_ann_pct=round(bh["ann_ret"] * 100, 2), hit=round(a["hit"], 3))
    yrs = (d.index[-1] - d.index[0]).days / 365.25
    o["sinyal_gunu_yil"] = round(float((pos != 0).sum() / yrs), 1)
    o["ort_mutlak_poz"] = round(float(pos.abs().mean()), 2)
    o["uzun_gun_orani"] = round(float((pos > 0).mean()), 2); o["kisa_gun_orani"] = round(float((pos < 0).mean()), 2)
    # erken dönem spot
    zs, ps = fn(sp)
    m = sp.index <= "2016-12-31"
    a = backtest(ps[m], sp.s_ret[m], H); b = backtest(ps[m], sp.s_ret[m], H, demean=True)
    bh = backtest(pd.Series(1.0, index=sp.index[m]), sp.s_ret[m], 1, 0)
    o["spot_2010_2016"] = dict(sharpe5=round(a["sharpe"], 2), sharpe5_dm=round(b["sharpe"], 2), t_gunluk=round(a["t_daily"], 2), bh_sharpe=round(bh["sharpe"], 2))
    reg("s7_bt", f"s7_{nm}_spot_erken_bt", nm + " spot 2010-2016 backtest", H, dict(ic=a["sharpe"], t=a["t_daily"], n=a["n_days"]), note="ic=Sharpe")
    pnl = backtest(pos, d.v_ret, H)["pnl"]
    yr = pd.DataFrame({"strateji_%": pnl.groupby(pnl.index.year).sum() * 100, "buyhold_%": d.v_ret.groupby(d.index.year).sum() * 100}).round(1)
    o["yillik"] = yr.T.to_dict()
    out[nm] = o
    print("=" * 20, nm); print(json.dumps({k: v for k, v in o.items() if k != "yillik"}, indent=1)); print(yr.T.to_string())
json.dump(out, open(f"{OUT}/s7_kural.json", "w"), indent=1, default=float)
