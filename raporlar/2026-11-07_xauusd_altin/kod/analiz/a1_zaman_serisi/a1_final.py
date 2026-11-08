#!/usr/bin/env python3
"""a1_zaman_serisi — son aşama: 'sakin piyasa momentumu' (LOWVOL_MOM) bacağının ayrıntılı sağlamlığı, placebo, yıllık tablolar,
kayıt üzerinde BH-FDR özeti. Önce a1_main.py, a1_deep.py, a1_volreg.py çalışmış olmalı. Çalıştır: python3 -W ignore a1_final.py
KURAL (LOWVOL_MOM_k5): gün t 15:00 UTC'de spot XAUUSD ile
   x  = ln(P15_t / P15_{t-5})                     (5 iş günü getirisi)
   rv = std(ln P15 günlük farkı, son 20 gün);  q = rv'nin 2010'dan bu yana genişleyen yüzdeliği (bugün dahil)
   q < 1/3 ise pozisyon = sign(x), aksi halde 0.  Giriş gün t VİOP uzlaşması, çıkış t+h uzlaşması (kademeli, h=1/3/5).
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, f"{S}/out/a1_zaman_serisi")
from lib_altin import *
from a1_feats import *

AG = "a1_zaman_serisi"; OUT = f"{S}/out/{AG}"
H = [1, 3, 5]
d = load_viop(); s = load_spot(); r_v = d.v_ret
lp = np.log(s.s_p15); r_s = lp.diff()
q_cal = expanding_pct(r_s.rolling(20).std())
q = to_viop(pd.DataFrame({"q": q_cal}), d.index).q
Fv = price_feats(np.exp(d.v_ret.cumsum()))


def lowmom_cal(k=5):
    return np.sign(lp - lp.shift(k)).where(q_cal < 1 / 3, 0.0).where(q_cal.notna())


def V(x): return to_viop(pd.DataFrame({"x": x}), d.index).x


roll = (d.v_code != d.v_code.shift(1)); roll_near = roll.rolling(3, center=True, min_periods=1).max().astype(bool)
EXT = ((d.index >= "2020-03-01") & (d.index <= "2020-04-30")) | ((d.index >= "2026-01-01") & (d.index <= "2026-03-31"))
ism = r_v.index <= IS_END
R = []


def bt_line(nm, pos, h, ret=r_v, reg=True):
    f = backtest(pos, ret, h, 5, demean=True); a = backtest(pos[ism], ret[ism], h, 5, demean=True); b = backtest(pos[~ism], ret[~ism], h, 5, demean=True)
    bn = backtest(pos[~ism], ret[~ism], h, 5); b10 = backtest(pos[~ism], ret[~ism], h, 10, demean=True); raw = backtest(pos, ret, h, 5)
    g = f["pnl"].groupby(f["pnl"].index.year); act = pos.reindex(ret.index).fillna(0).abs().groupby(ret.index.year).mean()
    ys = (g.mean() / g.std() * np.sqrt(252))
    yrs_active = [y for y in ys.index if act.get(y, 0) > 0.05]
    pos_yrs = int(sum(ys[y] > 0 for y in yrs_active))
    row = dict(sig=nm, h=h, sh_full=round(raw["sharpe"], 2), shdm_full=round(f["sharpe"], 2), t_full=round(f["t_daily"], 2), shdm_is=round(a["sharpe"], 2), t_is=round(a["t_daily"], 2),
               shdm_oos=round(b["sharpe"], 2), t_oos=round(b["t_daily"], 2), sh_oos_net=round(bn["sharpe"], 2), shdm_oos_10=round(b10["sharpe"], 2), ann_oos=round(bn["ann_ret"] * 100, 2),
               expo=round(f["exposure"], 2), turnover=round(f["turnover_per_yr"], 1), yrs=f"{pos_yrs}/{len(yrs_active)}", by_year=json.dumps({int(y): round(ys[y], 2) for y in yrs_active}))
    if reg:
        register(AG, "robust_lowmom", f"{nm}|h{h}", nm, h, dict(ic=row["shdm_full"], t=row["t_full"], n=f["n_days"], t_is=row["t_is"], t_oos=row["t_oos"], ic_oos=row["shdm_oos"],
                 yrs_same_sign=pos_yrs, yrs=len(yrs_active)), "LOWVOL_MOM sağlamlık; ic=demeaned Sharpe")
    R.append(row); return row


for h in H:
    base = V(lowmom_cal(5))
    bt_line("LOWMOM_k5(base)", base, h, reg=False)
    for k in [1, 3, 10, 20]: bt_line(f"LOWMOM_k{k}", V(lowmom_cal(k)), h)
    # VİOP uzlaşma getirisiyle (spot q ile): t (kapanışta hesaplanan) ve t-1 (temiz)
    bt_line("LOWMOM_k5_viop_t", np.sign(Fv.ret5).where(q < 1 / 3, 0.0).where(q.notna()), h)
    bt_line("LOWMOM_k5_viop_t1", np.sign(Fv.ret5.shift(1)).where(q.shift(1) < 1 / 3, 0.0).where(q.notna()), h)
    bt_line("LOWMOM_k5_excl_rollnear", base, h, ret=r_v.where(~roll_near))
    bt_line("LOWMOM_k5_excl_extreme", base, h, ret=r_v.where(~EXT))
    lo_, hi_ = r_v.quantile([0.01, 0.99]); bt_line("LOWMOM_k5_winsor", base, h, ret=r_v.clip(lo_, hi_))
    bt_line("LOWMOM_k5_continuous", (V(lp - lp.shift(5)) / V(r_s.rolling(20).std() * np.sqrt(5))).clip(-1, 1).where(q < 1 / 3, 0.0), h)
pd.DataFrame(R).to_csv(f"{OUT}/lowmom_robust.csv", index=False)

# placebo: sinyali ileri/geri kaydır
x = V((lp - lp.shift(5)).where(q_cal < 1 / 3))
PL = [dict(sig="ret5_loV|spot", h=h, **{f"s{k}": v for k, v in placebo_lead(x, r_v, h).items()}) for h in H]
pd.DataFrame(PL).to_csv(f"{OUT}/placebo_lowmom.csv", index=False)

# erken spot yıllık (2010-2016) + tam spot dönem yıl yıl
p_cal = lowmom_cal(5)
ER = []
for h in H:
    bt = backtest(p_cal, r_s, h, 5, demean=True); g = bt["pnl"].groupby(bt["pnl"].index.year)
    act = p_cal.abs().groupby(p_cal.index.year).mean()
    ER.append(dict(h=h, **{str(int(y)): round(v, 2) for y, v in (g.mean() / g.std() * np.sqrt(252)).items() if act.get(y, 0) > 0.05}))
pd.DataFrame(ER).to_csv(f"{OUT}/lowmom_spot_by_year.csv", index=False)

# güncel durum
last = dict(date=str(s.index[-1].date()), q_last=round(float(q_cal.iloc[-1]), 3), rv20_ann=round(float(r_s.rolling(20).std().iloc[-1] * np.sqrt(252)), 3),
            low_vol_threshold_rv20_ann=round(float(np.nanquantile(r_s.rolling(20).std().dropna().values, 1 / 3) * np.sqrt(252)), 3),
            share_lowvol_2026=round(float((q_cal[q_cal.index.year == 2026] < 1 / 3).mean()), 3))
json.dump(last, open(f"{OUT}/lowmom_current.json", "w"), indent=1)

# BH-FDR özeti (bu ajanın kaydı)
G = pd.read_csv(f"{REG_DIR}/{AG}.csv")
G["q"] = bh_fdr(G.p.fillna(1).values)
prim = G[~G.family.str.startswith("robust")].copy(); prim["q_prim"] = bh_fdr(prim.p.fillna(1).values)
summ = dict(n_total=len(G), n_primary=len(prim), n_robust=int(G.family.str.startswith("robust").sum()), n_p05=int((G.p < 0.05).sum()), n_abs_t3=int((G.t.abs() >= 3).sum()),
            min_q_all=float(G.q.min()), min_q_primary=float(prim.q_prim.min()), n_q10_primary=int((prim.q_prim < 0.10).sum()),
            by_family=G.groupby("family").size().to_dict(),
            top=prim.sort_values("p").head(12)[["family", "test_id", "t", "t_is", "t_oos", "p", "q_prim"]].round(4).to_dict("records"))
json.dump(summ, open(f"{OUT}/registry_summary.json", "w"), indent=1, default=str)
print(pd.DataFrame(R).drop(columns="by_year").to_string()); print(pd.DataFrame(PL).to_string()); print(pd.DataFrame(ER).to_string()); print(last)
print(json.dumps({k: v for k, v in summ.items() if k != "top"}, indent=1, default=str)); print(pd.DataFrame(summ["top"]).to_string())
