"""e1_etf_zaman_takvim — ortak yardımcılar (ETF/Midas cephesi, kendi zaman serisi + takvim).
Zaman: giriş = gün t ABD kapanışı 16:00 ET; çıkış = t+h kapanışı. Karar anı = gün t 15:00 ET (cut_utc).
Sinyalde ETF kapanışı yalnız t-1 ve öncesi; gün t bilgisi yalnız 15:00 ET spot (xau_cut) / Dukascopy *_cut ile.
IS = 2008..2017, OOS = 2018..2026-11; ayrıca 2022+.
"""
import os, sys, json, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/e1_etf_zaman_takvim"
sys.path.insert(0, f"{S}/code")
import lib_altin
lib_altin.IS_END = pd.Timestamp("2017-12-31")
from lib_altin import fwd, ic, split_stats, nw_ols, backtest, register, placebo_lead, bh_fdr
AGENT = "e1_etf_zaman_takvim"
IS_END = pd.Timestamp("2017-12-31"); P22 = pd.Timestamp("2022-01-01")

D = pd.read_parquet(f"{S}/panel/panel_etf.parquet"); D.index = pd.to_datetime(D.index)
IDX = D.index
UNLEV = ["GLD", "IAU", "GLDM", "SGOL", "BAR", "AAAU", "GDX", "GDXJ", "SLV"]
LEV = ["UGL", "GLL", "NUGT", "DUST", "JNUG", "JDST", "ZSL", "AGQ", "GDXU"]
COST = {t: (10.0, 20.0) for t in UNLEV}; COST.update({t: (20.0, 40.0) for t in LEV})
R = pd.DataFrame({t: np.log(D[f"c_{t}"]).diff() for t in UNLEV + LEV})          # log getiri, gün t-1 kapanış -> t kapanış
RS = np.expm1(R)                                                                   # basit getiri (portföy P&L için)
SW = pd.Timestamp("2020-04-01")   # Direxion NUGT/DUST/JNUG/JDST 3x -> 2x (veride 2020-03-24..04-01 arası geçiş)
def lev_sched(t):
    if t in ("UGL", "AGQ"): return pd.Series(2.0, index=IDX)
    if t in ("GLL", "ZSL"): return pd.Series(-2.0, index=IDX)
    if t in ("NUGT", "JNUG"): return pd.Series(np.where(IDX < SW, 3.0, 2.0), index=IDX)
    if t in ("DUST", "JDST"): return pd.Series(np.where(IDX < SW, -3.0, -2.0), index=IDX)
    if t == "GDXU": return pd.Series(3.0, index=IDX)
    return pd.Series(1.0, index=IDX)
INV = {"GLD": "GLL", "IAU": "GLL", "GLDM": "GLL", "SGOL": "GLL", "GDX": "DUST", "GDXJ": "JDST", "SLV": "ZSL"}
LONGLEV = {"GLD": "UGL", "IAU": "UGL", "GLDM": "UGL", "GDX": "NUGT", "GDXJ": "JNUG", "SLV": "AGQ"}

# --- GLD'nin 15:00 ET tahmini fiyatı (spot oranıyla): bilinir (t 15:00 ET). Altın ETF'leri için "kapanışa yakın" sinyal.
def p15(t):
    """t ETF'inin gün t 15:00 ET yaklaşık log fiyatı = log c_{t-1} + log(xau_cut_t / xau_close_{t-1}). Yalnız altın ETF'leri; gümüş için XAG cut-cut."""
    c = np.log(D[f"c_{t}"])
    if t in ("SLV",):
        g = np.log(D["dk_XAGUSD_cut"]).diff()
    else:
        g = np.log(D["xau_cut"]) - np.log(D["xau_close"]).shift(1)
    return c.shift(1) + g

def yahoo(t):
    d = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); d.index = pd.to_datetime(d.index); return d

def night_day(t):
    """Gece (kapanış t-1 -> açılış t, temettü dahil) ve gün içi (açılış t -> kapanış t) log getiri."""
    y = yahoo(t).reindex(IDX)
    tot = np.log(y.adjclose).diff()
    intra = np.log(y.close / y.open)
    night = tot - intra
    return night, intra, tot

# ---------------- istatistik ----------------
def rstats(sig, y, h, method="pearson"):
    """sig (ayrık ya da sürekli) ~ y (h günlük ileri getiri). NW lag>=max(h,5). Tam/IS/OOS/2022+ t, yıllık işaret tutarlılığı."""
    L = max(h, 5)
    d = pd.concat([pd.Series(sig, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 60 or d.x.std() == 0: return dict(ic=np.nan, t=np.nan, n=len(d))
    def tt(q):
        if len(q) < 40 or q.x.std() == 0: return np.nan, np.nan
        r = nw_ols(q.y, q.x, lags=L); return r["t"], r["b"]
    t_f, b_f = tt(d); t_i, _ = tt(d[d.index <= IS_END]); t_o, b_o = tt(d[d.index > IS_END]); t_2, _ = tt(d[d.index >= P22])
    icf = d.x.corr(d.y, method=method)
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method=method) if (len(g) > 20 and g.x.std() > 0) else np.nan)
    sg = np.sign(icf)
    return dict(ic=float(icf), t=float(t_f), b=float(b_f), n=int(len(d)), t_is=t_i, t_oos=t_o, b_oos=b_o, t_22=t_2,
                ic_oos=float(d[d.index > IS_END].x.corr(d[d.index > IS_END].y, method=method)) if (d.index > IS_END).sum() > 40 else np.nan,
                yrs_same_sign=int((np.sign(yr) == sg).sum()), yrs=int(yr.notna().sum()), by_year=yr.round(3).to_dict())

def ev_stats(mask, r1, h=1):
    """Olay günü (mask True = giriş günü) sonrası h günlük getiri vs diğer günler: fark (bps), NW t; IS/OOS/2022+; yıllık işaret."""
    y = fwd(r1, h)
    return rstats(mask.astype(float).where(y.notna()), y, h)

# ---------------- backtest ----------------
def _mdd(p):
    w = (1 + p).cumprod(); return float((w / w.cummax() - 1).min())

def bt2(pos, h, base, inv=None, w_inv=None, cost=(10.0, 20.0), cost_inv=(20.0, 40.0), stress=False, rl=None, ri=None):
    """pos_t ∈ [-1,1] gün t kapanışında alınır, h gün tutulur (1/h kademeli). Pozitif kısım 'base' ETF'te uzun;
    negatif kısım (inv verilirse) ters ETF'te |pos|*w_inv ağırlıkla UZUN (beta eşleştirmeli). inv=None -> negatif kısım nakit.
    Basit getiri, maliyet = |Δağırlık| × tek yön (RT/2). Döndür: günlük net P&L serisi + eff ağırlıklar."""
    rl = RS[base] if rl is None else rl
    pos = pos.reindex(IDX).fillna(0).clip(-1, 1)
    pl = pos.clip(lower=0); ps = (-pos).clip(lower=0)
    eL = sum(pl.shift(k).fillna(0) for k in range(h)) / h
    cL = cost[1] if stress else cost[0]
    g = eL.shift(1) * rl.fillna(0)
    c = (eL - eL.shift(1).fillna(0)).abs().shift(1).fillna(0) * cL / 2e4
    turn = (eL - eL.shift(1).fillna(0)).abs()
    if inv is not None:
        ri = RS[inv] if ri is None else ri
        w = (w_inv if w_inv is not None else 1.0 / lev_sched(inv).abs())
        eS = sum(ps.shift(k).fillna(0) for k in range(h)) / h * w
        cS = cost_inv[1] if stress else cost_inv[0]
        g = g + eS.shift(1) * ri.fillna(0)
        c = c + (eS - eS.shift(1).fillna(0)).abs().shift(1).fillna(0) * cS / 2e4
        turn = turn + (eS - eS.shift(1).fillna(0)).abs()
        valid = rl.notna() & ri.notna()
    else:
        valid = rl.notna()
    net = (g - c)[valid]
    return net, turn[valid]

def perf(p, turn=None, lab=""):
    p = p.dropna()
    if len(p) < 50: return dict(sh=np.nan, ann=np.nan, vol=np.nan, mdd=np.nan, n=len(p))
    ann = p.mean() * 252; vol = p.std() * np.sqrt(252)
    o = dict(sh=round(ann / vol, 2) if vol > 0 else np.nan, ann=round(ann * 100, 2), vol=round(vol * 100, 1), mdd=round(_mdd(p) * 100, 1), n=len(p))
    if turn is not None: o["rt_yr"] = round(float(turn.reindex(p.index).sum() / len(p) * 252 / 2), 1)
    return o

PERIODS = {"full": (None, None), "is": (None, IS_END), "oos": (IS_END + pd.Timedelta(days=1), None), "p22": (P22, None)}
def sl(s, k):
    a, b = PERIODS[k]
    if a is not None: s = s[s.index >= a]
    if b is not None: s = s[s.index <= b]
    return s

def strat_table(pos, h, base, label, lev=True, inv=True, extra=None):
    """Bir pozisyon serisi için uygulanabilir sürümler: ideal (açığa satış serbest, base üzerinde; ham ve drift-çıkarılmış),
    yalnız uzun (değilse nakit), ters ETF'li, kaldıraçlı uzun (aynı sinyal, tam nominal). Dönemler: full/is/oos/p22; maliyet temel+stres."""
    rows = []
    rl = RS[base]
    bh = rl.dropna()
    # ideal: pos (±) × base, maliyet base
    for st in (False, True):
        net, tr = bt2(pos, h, base, cost=COST[base], stress=st)  # yalnız uzun
        rows.append(("long_only", st, net, tr))
        # ideal ± (sentetik açığa satış — Midas'ta YOK, yalnız kıyas)
        pl = pos.reindex(IDX).fillna(0).clip(-1, 1)
        eff = sum(pl.shift(k).fillna(0) for k in range(h)) / h
        cc = COST[base][1] if st else COST[base][0]
        g = (eff.shift(1) * rl).dropna(); cst = (eff - eff.shift(1).fillna(0)).abs().shift(1).fillna(0).reindex(g.index) * cc / 2e4
        rows.append(("ideal_ls", st, g - cst, (eff - eff.shift(1).fillna(0)).abs().reindex(g.index)))
        if inv and base in INV:
            net, tr = bt2(pos, h, base, inv=INV[base], cost=COST[base], cost_inv=COST[INV[base]], stress=st)
            rows.append((f"inv_{INV[base]}", st, net, tr))
        if lev and base in LONGLEV:
            lt = LONGLEV[base]
            net, tr = bt2(pos, h, lt, cost=COST[lt], stress=st)
            rows.append((f"lev_{lt}", st, net, tr))
    out = []
    for ver, st, net, tr in rows:
        for k in PERIODS:
            p = sl(net, k); o = perf(p, tr)
            b = perf(sl(bh, k).reindex(p.index).dropna()) if len(p) > 50 else dict(sh=np.nan)
            out.append(dict(strategy=label, base=base, h=h, version=ver, cost="stres" if st else "temel", period=k, **o, bh_sh=b["sh"]))
    # drift-çıkarılmış ideal (library backtest demean=True, log getiri)
    for k in PERIODS:
        rr = sl(R[base].dropna(), k)
        a = backtest(pos.reindex(rr.index), rr, h, COST[base][0], demean=True)
        a2 = backtest(pos.reindex(rr.index).clip(lower=0), rr, h, COST[base][0], demean=True)
        out.append(dict(strategy=label, base=base, h=h, version="ideal_ls_demeaned", cost="temel", period=k, sh=a and round(a["sharpe"], 2), ann=a and round(a["ann_ret"] * 100, 2), n=a and a["n_days"]))
        out.append(dict(strategy=label, base=base, h=h, version="long_only_demeaned", cost="temel", period=k, sh=a2 and round(a2["sharpe"], 2), ann=a2 and round(a2["ann_ret"] * 100, 2), n=a2 and a2["n_days"]))
    df = pd.DataFrame(out)
    if extra:
        for kk, vv in extra.items(): df[kk] = vv
    return df

def pivot_short(df):
    """Özet: temel maliyet; sürüm × dönem Sharpe."""
    q = df[df.cost == "temel"].pivot_table(index=["strategy", "base", "h", "version"], columns="period", values="sh", aggfunc="first")
    return q[[c for c in ["full", "is", "oos", "p22"] if c in q.columns]]

TESTS = []
def reg(family, test_id, predictor, h, st, note=""):
    st = {k: (float(v) if isinstance(v, (np.floating, np.integer)) else v) for k, v in st.items() if k != "by_year"}
    row = register(AGENT, family, test_id, predictor, h, st, note)
    TESTS.append(row); return row

def save(df, name):
    df.to_csv(f"{O}/{name}", index=isinstance(df.index, pd.MultiIndex) or df.index.name is not None)

def reset(prefix):
    """Bu betiğin ailesine (family ön eki) ait eski kayıtları siler (yeniden çalıştırmada çift kayıt olmasın)."""
    fn = f"{lib_altin.REG_DIR}/{AGENT}.csv"
    if os.path.exists(fn):
        r = pd.read_csv(fn)
        r = r[~r.family.astype(str).str.startswith(prefix)]
        r.to_csv(fn, index=False)

def sel_best(tab, key_cols, tcol="t_is"):
    """IS'te |t| en büyük parametreyi seç (her key grubu için)."""
    t = tab.copy(); t["abs_t_is"] = t[tcol].abs()
    return t.sort_values("abs_t_is", ascending=False).groupby(key_cols, as_index=False).head(1)
