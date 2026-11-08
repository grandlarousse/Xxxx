"""r2: İddiaların bağımsız yeniden hesabı (C1, C1b, C2, C3, D1, C4). Girdi r1_viop.parquet, r1_spot.parquet (ham tablolardan r1_veri.py)."""
import sys, json, numpy as np, pandas as pd
OUT = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_rep"
sys.path.insert(0, OUT)
from rep_util import *

d = pd.read_parquet(f"{OUT}/r1_viop.parquet"); sp = pd.read_parquet(f"{OUT}/r1_spot.parquet")
idx = d.index; ISM = idx <= IS_END; OOSM = idx > IS_END
YRS = (idx[-1] - idx[0]).days / 365.25
res = {}
lg = open(f"{OUT}/r2_log.txt", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s); lg.write(s + "\n")

def zsc(r, win=120, minp=60):
    return r / r.rolling(win, min_periods=minp).std().shift(1)

def beta(a, b, win, minp):
    return (a.rolling(win, min_periods=minp).cov(b) / b.rolling(win, min_periods=minp).var()).shift(1)

def resid_z(df, col, bw=60):
    rm = np.log(df[col]).diff(); rg = np.log(df["y_GLD"]).diff()
    return zsc(rm - beta(rm, rg, bw, 40) * rg)

def maps(x):
    return {"isaret": np.sign(x).fillna(0), "z_kirp": (x / 2).clip(-1, 1).fillna(0), "uc_tercile": np.sign(x).where(x.abs() > 0.43, 0.0).fillna(0)}

def full_eval(name, x, H, fixed_map=None, early_fn=None):
    y = d[f"fwd{H}"]
    s = split(x, y, H); sp_p = split(x, y, H, method="pearson")
    o = dict(ic=round(s["ic"], 4), t=round(s["t"], 2), ic_is=round(s["ic_is"], 4), t_is=round(s["t_is"], 2), ic_oos=round(s["ic_oos"], 4), t_oos=round(s["t_oos"], 2),
             yrs=s["yrs"], n=s["n"], pearson_t=round(sp_p["t"], 2), pearson_t_is=round(sp_p["t_is"], 2), pearson_t_oos=round(sp_p["t_oos"], 2), by_year=s["by_year"])
    other_h = {}
    for h in (1, 3, 5):
        ss = split(x, d[f"fwd{h}"], h); other_h[h] = (round(ss["t"], 2), round(ss["t_is"], 2), round(ss["t_oos"], 2))
    o["t_by_h(full,is,oos)"] = other_h
    # yön ve eşleme yalnız IS'ten
    yon = float(np.sign(s["ic_is"]))
    M = maps(yon * x)
    is_sh = {k: round(bt(p[ISM], d.v_ret[ISM], H)["sharpe"], 3) for k, p in M.items()}
    best = max(is_sh, key=is_sh.get)
    o["yon_IS"] = yon; o["IS_sharpe_eslemeler"] = is_sh; o["IS_secilen"] = best
    use = fixed_map or best
    pos = M[use]; o["kullanilan_esleme"] = use
    for per, m in (("full", slice(None)), ("is", ISM), ("oos", OOSM)):
        pp, rr = (pos, d.v_ret) if isinstance(m, slice) else (pos[m], d.v_ret[m])
        a = bt(pp, rr, H); b = bt(pp, rr, H, demean=True); c = bt(pp, rr, H, cost_bps=10); g = bt(pp, rr, H, netting=False)
        bh = bt(pd.Series(1.0, index=rr.index), rr, 1, cost_bps=0)
        o[f"bt_{per}"] = dict(sharpe5=round(a["sharpe"], 2), sharpe5_t=round(a["t_sharpe"], 2), sharpe5_dm=round(b["sharpe"], 2), sharpe10=round(c["sharpe"], 2),
                              sharpe5_netlesmesiz=round(g["sharpe"], 2), ann5_pct=round(a["ann_ret"] * 100, 2), bh_sharpe=round(bh["sharpe"], 2), bh_ann_pct=round(bh["ann_ret"] * 100, 2),
                              exposure=round(a["exposure"], 2), turnover=round(a["turnover"], 1),
                              long_sh=round(bt(pp.clip(lower=0), rr, H)["sharpe"], 2), short_sh=round(bt(pp.clip(upper=0), rr, H)["sharpe"], 2),
                              long_sh_dm=round(bt(pp.clip(lower=0), rr, H, demean=True)["sharpe"], 2), short_sh_dm=round(bt(pp.clip(upper=0), rr, H, demean=True)["sharpe"], 2))
    o["sinyal_gunu_yil"] = round(float((pos != 0).sum() / YRS), 1)
    o["acik_simulasyon_full_sharpe5_netlesmesiz"] = round(bt_explicit(pos, d.v_ret, H), 2)
    pnl = bt(pos, d.v_ret, H)["pnl"]
    o["yillik_strateji_%"] = (pnl.groupby(pnl.index.year).sum() * 100).round(1).to_dict()
    o["yillik_bh_%"] = (d.v_ret.groupby(idx.year).sum() * 100).round(1).to_dict()
    if early_fn is not None:
        xs = early_fn(sp)
        for per, a_, b_ in (("2010_2016", "2010-01-01", "2016-12-31"), ("2017_2026", "2017-03-01", "2026-12-31")):
            m = (sp.index >= a_) & (sp.index <= b_)
            st = ic_t(xs[m], sp[f"sfwd{H}"][m], max(H, 5))
            o[f"spot_{per}"] = dict(ic=round(st["ic"], 4), t=round(st["t"], 2), n=st["n"])
        m = sp.index <= "2016-12-31"
        ps = maps(yon * xs)[use]
        a = bt(ps[m], sp.s_ret[m], H); b = bt(ps[m], sp.s_ret[m], H, demean=True)
        o["spot_2010_2016_bt"] = dict(sharpe5=round(a["sharpe"], 2), t=round(a["t_sharpe"], 2), sharpe5_dm=round(b["sharpe"], 2))
        dd = pd.concat([xs[m].rename("x"), sp[f"sfwd{H}"][m].rename("y")], axis=1).dropna()
        o["spot_erken_yillik_ic"] = dd.groupby(dd.index.year).apply(lambda g: g.x.corr(g.y, method="spearman")).round(3).to_dict()
    res[name] = o
    say("=" * 25, name)
    for k, v in o.items(): say(f"  {k}: {v}")
    return pos

# ===================== C1 =====================
zC1 = resid_z(d, "y_GDXJ")
posC1 = full_eval("C1_GDXJ_artik_h3", zC1, 3, early_fn=lambda s: resid_z(s, "y_GDXJ"))

# ===================== C1b =====================
BASK = ["y_NEM", "y_AEM", "y_B", "y_KGC", "y_FNV", "y_WPM", "y_RGLD"]
def comp(df):
    zs = [resid_z(df, c) for c in ("y_GDX", "y_GDXJ", "y_RING")]
    rb = np.log(df[BASK]).diff().mean(axis=1); rg = np.log(df["y_GLD"]).diff()
    zs.append(zsc(rb - beta(rb, rg, 60, 40) * rg))
    return pd.concat(zs, axis=1).mean(axis=1)
full_eval("C1b_madenci_kompozit_h3", comp(d), 3, early_fn=comp)

# ===================== C2 =====================
def curve(df): return zsc((df.ust_nom10 - df.ust_nom2).diff(5))
full_eval("C2_egri_d5_h1", curve(d), 1, early_fn=curve)

# ===================== C3 =====================
prev = pd.Series(idx, index=idx).shift(1)
def win_ret(sym, h_end, h_start, dfx=d):
    p_end = dfx[f"{sym}_p{h_end}"]; p_st = dfx[f"{sym}_p{h_start}"].shift(1)  # önceki endeks günü
    return np.log(p_end / p_st)
xD = win_ret("DOLLARIDXUSD", 15, 20); gC = win_ret("XAUUSD", 15, 20)
bC = (xD.rolling(250, min_periods=150).cov(gC) / xD.rolling(250, min_periods=150).var()).shift(1)
zC3 = zsc(bC * xD - gC)
full_eval("C3_dxy_sapma_C_h1", zC3, 1)
# kısmi: altının kendi C getirisi kontrol
def partial(y, x, ctrls, L):
    import statsmodels.api as sm
    D = pd.concat([y.rename("y"), x.rename("x")] + [c.rename(f"c{i}") for i, c in enumerate(ctrls)], axis=1).dropna()
    Z = (D - D.mean()) / D.std()
    m = sm.OLS(Z.y, sm.add_constant(Z.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return round(float(m.tvalues["x"]), 2)
res["C3_dxy_sapma_C_h1"]["kismi_t_altinC"] = partial(d.fwd1, zC3, [zsc(gC)], 5)
res["C3_dxy_sapma_C_h1"]["altin_C_kendi_ic"] = {k: round(v, 3) if isinstance(v, float) else v for k, v in split(zsc(gC), d.fwd1, 1).items() if k != "by_year"}
say("C3 kısmi t (altın C kontrol):", res["C3_dxy_sapma_C_h1"]["kismi_t_altinC"], "altın C kendi:", res["C3_dxy_sapma_C_h1"]["altin_C_kendi_ic"])

# ===================== D1 (emilim tanısı) =====================
zD1 = zsc(np.log(d["y_DX_Y_NYB"]).diff())
absorb = win_ret("XAUUSD", 15, 20)   # t-1 20:00 → t 15:00
s = split(zD1, absorb, 0); s1 = split(zD1, d.fwd1, 1)
res["D1_dolar_emilim_tani"] = dict(ic=round(s["ic"], 4), t=round(s["t"], 2), t_is=round(s["t_is"], 2), t_oos=round(s["t_oos"], 2), yrs=s["yrs"], n=s["n"],
                                   fwd1_ic=round(s1["ic"], 4), fwd1_t=round(s1["t"], 2))
# Zaman çakışması kontrolü: DXY Yahoo kapanışı 17:00 ET (21/22 UTC) → pencere t-1 20:00'de başlıyor; 1–2 saat çakışma. Pencere t 00:00 / t-1 22:00 / 23:00'ten başlatılınca:
for hs in (22, 23):
    w = win_ret("XAUUSD", 15, hs); ss = split(zD1, w, 0)
    res["D1_dolar_emilim_tani"][f"pencere_t-1_{hs}:00"] = (round(ss["ic"], 4), round(ss["t"], 2), round(ss["t_is"], 2), round(ss["t_oos"], 2))
w = np.log(d["XAUUSD_p15"] / d["XAUUSD_p00"]); ss = split(zD1, w, 0)
res["D1_dolar_emilim_tani"]["pencere_t_00:00"] = (round(ss["ic"], 4), round(ss["t"], 2), round(ss["t_is"], 2), round(ss["t_oos"], 2))
w = np.log(d["XAUUSD_p21"].shift(1) / d["XAUUSD_p20"].shift(1)); ss = split(zD1, w, 0)
res["D1_dolar_emilim_tani"]["yalniz_t-1_20-21"] = (round(ss["ic"], 4), round(ss["t"], 2))
say("D1:", res["D1_dolar_emilim_tani"])

# ===================== C4 =====================
def roll_resid(yv, X, W):
    dd = pd.concat([yv.rename("y"), X], axis=1).dropna()
    Y = dd["y"].values; XX = np.column_stack([np.ones(len(dd)), dd.drop(columns="y").values])
    rz = np.full(len(dd), np.nan)
    for i in range(W, len(dd)):
        b, *_ = np.linalg.lstsq(XX[i - W:i], Y[i - W:i], rcond=None)
        e = Y[i - W:i] - XX[i - W:i] @ b
        rz[i] = (Y[i] - XX[i] @ b) / e.std()
    return pd.Series(rz, index=dd.index).reindex(idx)
zC4 = roll_resid(np.log(d.XAUUSD_p15), pd.DataFrame({"r10": d.ust_real10, "ldx": np.log(d.DOLLARIDXUSD_p15)}), 120)
full_eval("C4_reel_dolar_model_artigi_h1", zC4, 1, fixed_map="z_kirp")
g1 = np.log(d.XAUUSD_p15).diff(); g5 = np.log(d.XAUUSD_p15).diff(5)
res["C4_reel_dolar_model_artigi_h1"]["kismi_t_g1g5"] = partial(d.fwd1, zC4, [g1, g5], 5)
say("C4 kısmi:", res["C4_reel_dolar_model_artigi_h1"]["kismi_t_g1g5"])

json.dump(res, open(f"{OUT}/r2_sonuc.json", "w"), indent=1, default=str, ensure_ascii=False)
lg.close()
