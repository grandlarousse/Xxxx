"""İddia tablosu için kural backtest'leri (5/10 bps, buy&hold, demeaned, bacaklar). Her kural register edilir."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
import json
FAM = "f_claims"
reset_family(FAM)
p, f = build()
r = p.v_ret; isx = p.index <= L.IS_END
out = {}

def run(name, pos, ret, h, note):
    res = {}
    for cost in (5, 10):
        bs = L.bt_summary(pos, ret, h, cost); lg = legs(pos, ret, h, cost)
        res[cost] = dict(full=bs["full"], IS=bs["is"], OOS=bs["oos"], bh=bs["buyhold_sharpe_full"], legs=lg)
    a = L.backtest(pos, ret, h, 5); ai = L.backtest(pos[isx], ret[isx], h, 5); ao = L.backtest(pos[~isx], ret[~isx], h, 5)
    yr = a["pnl"].groupby(a["pnl"].index.year).sum()
    tpy = float((pos.fillna(0).diff().abs() > 0).sum() / (len(pos) / 252))
    res["t_full"] = a["t_daily"]; res["t_is"] = ai["t_daily"]; res["t_oos"] = ao["t_daily"]; res["yrs_pos"] = f"{int((yr > 0).sum())}/{len(yr)}"; res["pos_changes_per_yr"] = round(tpy, 1)
    L.register(AG, FAM, name, name, h, dict(ic=np.nan, t=a["t_daily"], n=a["n_days"], t_is=ai["t_daily"], t_oos=ao["t_daily"], yrs_same_sign=int((yr > 0).sum()), yrs=len(yr)), note)
    out[name] = res
    print(f"\n== {name} (h={h}) ==  t_full {a['t_daily']:+.2f}  t_IS {ai['t_daily']:+.2f}  t_OOS {ao['t_daily']:+.2f}  yıllar(+) {res['yrs_pos']}  poz.değişim/yıl {tpy:.1f}")
    for cost in (5, 10):
        q = res[cost]
        print(f"  {cost}bps: tam {q['full']['sharpe']} (dm {q['full']['sharpe_demeaned']}) | IS {q['IS']['sharpe']} (dm {q['IS']['sharpe_demeaned']}) | OOS {q['OOS']['sharpe']} (dm {q['OOS']['sharpe_demeaned']}) | B&H {q['bh']} | bacaklar {q['legs']} | maruz {q['full']['exposure']}")

# 1) USDTRY carry zamanlaması (USDTRY vadeli hedef)
lfx = np.log(p.dk_USDTRY_p15); bpd = np.log(p.vo_usdtry_settle / p.dk_USDTRY_p15) / p.vo_usdtry_dte.clip(lower=3)
sig1 = (lfx.diff().rolling(20).mean() - bpd * 1.4).shift(1)
run("C1_usdtry_carry_timing", np.sign(sig1).fillna(0), p.vo_usdtry_ret, 1, "USDTRY vadeli; t-1")
run("C1b_usdtry_always_short", pd.Series(-1.0, index=p.index), p.vo_usdtry_ret, 1, "kıyas: hep kısa USDTRY")
# 4) usd_fut_l1 -> XAUUSD h=3 (tam dönemde en tutarlı işaret; IS'te seçilmedi)
run("C4_xau_short_after_usdtry_up", -np.sign(f.usd_fut_l1).fillna(0), r, 3, "XAUUSD; t-1 VİOP USDTRY")
# 4b) XAUTRY OI 1g değişimi (t-1) yönünde 3 gün
run("C4b_xau_follow_xautry_oi", np.sign(f.goi_d1_l1).fillna(0), r, 3, "XAUUSD; t-1 XAUTRYM OI değişimi")
# 5) TL/XU030 şoku sonrası 3 gün kısa
sh = ((f.usd_spot_1.abs() > 0.025) | (f.xu_l1 < -0.05)).astype(float)
run("C5_xau_short_after_TR_shock", -sh, r, 3, "XAUUSD; şok günü uzlaşmasında kısa, 3 gün")
# 6) tatil sonrası: tatil boyunca spot hareketinin tersine 5 gün
spot_gap = np.log(p.xau_p15 / p.xau_p15_prev)
run("C6_xau_fade_holiday_move", -np.sign(spot_gap.where(f.gap > 0)).fillna(0), r, 5, "XAUUSD; tatil sonrası ilk gün uzlaşmasında gir")
# 3) prim RV (K ve t-1), 3 bacak 15 bps
res_leg = (p.vo_xautry_ret - p.v_ret - p.vo_usdtry_ret).fillna(0)
z = zs(p.tr_prem_matched, 60)
for nm, zz in [("C3_premRV_K", z), ("C3_premRV_l1", z.shift(1))]:
    pos = -(zz > 1).astype(float) + (zz < -1).astype(float)
    for h in (3,):
        a = L.backtest(pos, res_leg, h, 15); ao = L.backtest(pos[~isx], res_leg[~isx], h, 15); ad = L.backtest(pos[~isx], res_leg[~isx], h, 15, demean=True)
        g0 = L.backtest(pos, res_leg, h, 0)
        print(f"\n== {nm} h={h}: brüt Sharpe {g0['sharpe']:+.2f}, net15 tam {a['sharpe']:+.2f} (t {a['t_daily']:+.2f}), OOS net15 {ao['sharpe']:+.2f} (dm {ad['sharpe']:+.2f}), maruz {a['exposure']:.2f}, poz.değişim/yıl {(pos.diff().abs()>0).sum()/(len(pos)/252):.0f}")
        L.register(AG, FAM, nm, nm, h, dict(ic=np.nan, t=a["t_daily"], n=a["n_days"], t_oos=ao["t_daily"]), "3 bacak 15 bps")
json.dump({k: {str(kk): vv for kk, vv in v.items()} for k, v in out.items()}, open(f"{OUT}/claims_bt.json", "w"), default=str, indent=1)
