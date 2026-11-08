"""s4: Aday sinyallerin derin kontrolü (IS'te seçilmiş kurallar; OOS tek sefer):
 C1 madenci artığı: e = r_GDXJ − β60 r_GLD (t-1 ABD kapanışları), z(e) → fwd3 (IS'te madenci-artık ailesinde h=3, GDXJ en yüksek t_is).
    + seçim yanlılığını azaltmak için kompozit: ort z(e) {GDX, GDXJ, RING, sepet7}.
 C2 eğri: Δ5(nom10 − nom2) (t-1 22:00 UTC) → fwd1 (tam dönemde bulundu; IS t<2 → seçim yanlılığı var).
 C3 dolar sapması C penceresi: gap = β·r_DXY − r_XAU, [t-1 20:00, t 15:00] → fwd1 (IS t=-2,2).
 C4 reel faiz+dolar seviye modeli artığı (15:00 UTC, W120) → fwd1.
Her aday: kısmi regresyon (altın öz getirileri, S&P, VIX, A penceresi altın), placebo_lead, yıllık IC, roll/uç değer/winsor sağlamlık,
spot panel 2010–2016 erken dönem, emilim tanısı, backtest (IS'te seçilen eşleme; 5 ve 10 bps; demeaned; uzun/kısa bacak; buy&hold)."""
import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *

reg_reset("s4_")
d = load_viop(); sp = load_spot()
idx = d.index

def miner_resid(df, m, beta_win=60):
    rm = np.log(df[m]).diff(); rg = np.log(df["y_GLD"]).diff()
    b = rm.rolling(beta_win, min_periods=40).cov(rg).shift(1) / rg.rolling(beta_win, min_periods=40).var().shift(1)
    return zscale(rm - b * rg)

def miner_comp(df):
    zs = []
    for m in ["y_GDX", "y_GDXJ", "y_RING"]:
        zs.append(miner_resid(df, m))
    bn = ["y_NEM", "y_AEM", "y_B", "y_KGC", "y_FNV", "y_WPM", "y_RGLD"]
    rb = np.log(df[[c for c in bn if c in df]]).diff().mean(axis=1); rg = np.log(df["y_GLD"]).diff()
    b = rb.rolling(60, min_periods=40).cov(rg).shift(1) / rg.rolling(60, min_periods=40).var().shift(1)
    zs.append(zscale(rb - b * rg))
    return pd.concat(zs, axis=1).mean(axis=1)

def curve5(df):
    c = df["ust_nom10"] - df["ust_nom2"]; return zscale(c.diff(5))

def dxy_gapC():
    prev = pd.Series(idx, index=idx).shift(1)
    out = {}
    for s in ("DOLLARIDXUSD", "XAUUSD"):
        p15 = px_at(s, 15); p20 = px_at(s, 20)
        out[s] = pd.Series(np.log(p15.reindex(idx).values / p20.reindex(prev.values).values), index=idx)
    x, g = out["DOLLARIDXUSD"], out["XAUUSD"]
    b = (x.rolling(250, min_periods=150).cov(g) / x.rolling(250, min_periods=150).var()).shift(1)
    return zscale(b * x - g), g

def lvl_p15():
    r = pd.read_parquet(f"{OUT}/s2_model_artik_p15_W120.parquet")
    return r["rz"].reindex(idx)

gC_dxy, gold_C = dxy_gapC()
CANDS = {
    "C1_GDXJ_artik": dict(x=miner_resid(d, "y_GDXJ"), h=3, info="t-1 ABD kapanışı (GDXJ, GLD; ≤21:00 UTC t-1), β geçmiş 60 gün", early=lambda s: miner_resid(s, "y_GDXJ")),
    "C1b_madenci_kompozit": dict(x=miner_comp(d), h=3, info="t-1 ABD kapanışı", early=lambda s: miner_comp(s)),
    "C2_egri_d5": dict(x=curve5(d), h=1, info="ust_nom10, ust_nom2 gün t-1 (22:00 UTC t-1)", early=lambda s: curve5(s)),
    "C3_dxy_gapC": dict(x=gC_dxy, h=1, info="Dukascopy DXY ve XAU t-1 20:00 → t 15:00 UTC", early=None),
    "C4_reelmodel_p15": dict(x=lvl_p15(), h=1, info="xau_p15, dk_DOLLARIDXUSD_p15 (t 15:00), reel10 t-1", early=None),
}
# kontroller (hepsi gün t 15:00 UTC'den önce bilinir)
ctrl = gold_controls(d)
ctrl["spx"] = zscale(np.log(d["y__GSPC"]).diff()); ctrl["vix"] = zscale(np.log(d["y__VIX"]).diff())
ctrl["gC"] = zscale(gold_C)
roll_ok = {h: (d["v_code"] == d["v_code"].shift(-h)) for h in (1, 3, 5)}
ext = ((idx >= "2020-03-01") & (idx <= "2020-04-30")) | ((idx >= "2026-01-01") & (idx <= "2026-02-28"))

def mappings(x):
    return {"isaret": np.sign(x), "z_kirp": (x / 2).clip(-1, 1), "uc_tercile": np.sign(x).where(x.abs() > 0.43, 0.0)}  # |z|>0.43 ≈ normalde üst/alt üçte bir

summary = {}
for name, C in CANDS.items():
    x = C["x"]; H = C["h"]; out = {"bilgi_zamani": C["info"], "h_secili": H}
    for h in (1, 3, 5):
        y = d[f"fwd{h}"]
        s = split_stats(x, y, h); out[f"ic_h{h}"] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items()}
    y = d[f"fwd{H}"]
    # kısmi
    pk = partial_stats(x, y, ctrl, H); out["kismi_t"] = {k: round(v, 2) for k, v in pk.items() if k in ("t", "t_is", "t_oos")}
    reg("s4_kismi", f"s4_{name}_kismi", name + " | g1,g5,spx,vix,gC", H, pk)
    # placebo
    out["placebo"] = placebo_lead(x, d["v_ret"], H)
    # sağlamlık
    rb = {}
    rb["roll_haric"] = split_stats(x.where(roll_ok[H]), y, H)
    rb["uc_haric(Mar20,OcaSub26)"] = split_stats(x.where(~ext), y.where(~ext), H)
    lo, hi = y.quantile([0.01, 0.99]); rb["winsor_y"] = split_stats(x, y.clip(lo, hi), H)
    # sıfır hacimli gün yok (v_volume>0 her gün); düşük hacim: önceki 250 günün %10'luk diliminin altı (gün t-1 hacmi → bilinen)
    lowv = d["v_volume"].shift(1) < d["v_volume"].shift(1).rolling(250, min_periods=60).quantile(0.10)
    rb["dusuk_hacim_haric"] = split_stats(x.where(~lowv), y, H)
    rb["pearson"] = split_stats(x, y, H, method="pearson")
    out["saglamlik"] = {k: dict(ic=round(v["ic"], 4), t=round(v["t"], 2), t_is=round(v["t_is"], 2), t_oos=round(v["t_oos"], 2)) for k, v in rb.items()}
    for k, v in rb.items(): reg("s4_saglam", f"s4_{name}_{k}", name + " " + k, H, v)
    # emilim tanısı: x → altın [t-1 20:00, t 15:00] (C3 için anlamsız: x zaten bu pencereden)
    if not name.startswith("C3"):
        e = split_stats(x, gold_C, 1); out["emilim_altinC"] = dict(ic=round(e["ic"], 4), t=round(e["t"], 2))
    # erken dönem spot paneli
    if C["early"] is not None:
        xs = C["early"](sp)
        for per, a, b in (("2010-2016", "2010-01-01", "2016-12-31"), ("2017-2026_spot", "2017-03-01", "2026-12-31")):
            m = (sp.index >= a) & (sp.index <= b)
            st = ic(xs[m], sp[f"sfwd{H}"][m], max(H, 5))
            out[f"spot_{per}"] = dict(ic=round(st["ic"], 4), t=round(st["t"], 2), n=st["n"])
            if per == "2010-2016": reg("s4_erken", f"s4_{name}_erken", name + " spot 2010-2016", H, dict(ic=st["ic"], t=st["t"], n=st["n"]))
        ye = yearly_sign_table(xs[(sp.index <= "2016-12-31")], sp[f"sfwd{H}"][(sp.index <= "2016-12-31")])
        out["spot_erken_yillik"] = ye.round(3).to_dict()
    # backtest: eşleme IS'te seçilir
    yo = split_stats(x[idx <= IS_END], d[f"fwd{H}"][idx <= IS_END], H)
    yon = float(np.sign(yo["ic"]))  # yön yalnız IS IC işaretinden
    out["yon_IS"] = yon
    maps = mappings(yon * x); bt = {}
    best, bestS = None, -9
    for mn, pos in maps.items():
        r_is = backtest(pos[idx <= IS_END], d["v_ret"][idx <= IS_END], H)
        bt[mn] = dict(is_sharpe=round(r_is["sharpe"], 2))
        if r_is["sharpe"] > bestS: best, bestS = mn, r_is["sharpe"]
    pos = maps[best]
    full = legs_bt(pos, d["v_ret"], H, COST_BPS); stress = bt_summary(pos, d["v_ret"], H, 10.0)
    oos_bt = backtest(pos[idx > IS_END], d["v_ret"][idx > IS_END], H)
    oos_dm = backtest(pos[idx > IS_END], d["v_ret"][idx > IS_END], H, demean=True)
    reg("s4_bt", f"s4_{name}_bt_oos", name + f" backtest OOS ({best})", H, dict(ic=oos_bt["sharpe"], t=oos_bt["t_daily"], n=oos_bt["n_days"]), note="ic=OOS net Sharpe")
    # yıl yıl net getiri
    pnl = backtest(pos, d["v_ret"], H)["pnl"]; bh = d["v_ret"]
    yr = pd.DataFrame({"strateji_%": pnl.groupby(pnl.index.year).sum() * 100, "buyhold_%": bh.groupby(bh.index.year).sum() * 100}).round(2)
    out["backtest"] = dict(eslemeler_IS=bt, secilen=best, ls=full["ls"], long=full["long"], short=full["short"], stres_10bps=stress,
                           oos_t_gunluk=round(oos_bt["t_daily"], 2), oos_sharpe_dm=round(oos_dm["sharpe"], 2), yillik=yr.to_dict())
    pnl.to_frame("pnl").to_parquet(f"{OUT}/s4_pnl_{name}.parquet")
    summary[name] = out

def conv(o):
    if isinstance(o, dict): return {str(k): conv(v) for k, v in o.items()}
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    return o
json.dump(conv(summary), open(f"{OUT}/s4_adaylar.json", "w"), indent=1, ensure_ascii=False, default=str)
for k, v in summary.items():
    print("=" * 30, k)
    for kk in ["bilgi_zamani", "h_secili", "kismi_t", "placebo", "saglamlik", "emilim_altinC", "spot_2010-2016", "spot_2017-2026_spot", "spot_erken_yillik"]:
        if kk in v: print(kk, ":", v[kk])
    for h in (1, 3, 5):
        s = v[f"ic_h{h}"]; print(f"h{h}: ic={s['ic']} t={s['t']:.2f} t_is={s['t_is']:.2f} t_oos={s['t_oos']:.2f} yrs={s['yrs_same_sign']}/{s['yrs']} by_year={s['by_year']}")
    b = v["backtest"]; print("BT eşleme IS:", b["eslemeler_IS"], "seçilen:", b["secilen"])
    for leg in ("ls", "long", "short"): print(leg, b[leg])
    print("stres10", b["stres_10bps"]); print("OOS t günlük", b["oos_t_gunluk"], "OOS dm sharpe", b["oos_sharpe_dm"])
    print(pd.DataFrame(b["yillik"]).T.to_string())
