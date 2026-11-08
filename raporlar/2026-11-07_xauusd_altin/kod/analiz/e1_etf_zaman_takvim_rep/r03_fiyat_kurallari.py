"""3) Fiyat kuralları: C3 GDX >=5 gün üst üste düşüş (t-1'e kadar) -> t kapanışında al, h=1; C5 GLD Bollinger(20,2) z_{t-1}<-2 -> 5 gün tut.
Sinyal yalnız t-1 kapanışına kadarki adjclose ile (t-1 16:00 ET < t 15:00 ET). Giriş t kapanışı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
pd.set_option("display.width", 250)

TK = ["GLD", "GDX", "GDXJ", "SLV", "NUGT", "DUST", "GLL", "UGL", "JDST", "JNUG"]
R = {t: logret(t) for t in TK}; RS = {t: np.expm1(r) for t, r in R.items()}
SW = pd.Timestamp("2020-04-01")
def inv_w(t):  # ters ETF beta eşleştirme ağırlığı
    if t == "GLL": return pd.Series(0.5, index=SESS)
    return pd.Series(np.where(SESS < SW, 1 / 3, 0.5), index=SESS)

def run_streak(r):
    """gün t kapanışına kadarki ardışık seri (+ yükseliş, - düşüş). r=0 seriyi sıfırlar."""
    s = np.sign(r).fillna(0).values; out = np.zeros(len(s))
    for i in range(len(s)):
        if s[i] == 0: out[i] = 0
        elif i > 0 and np.sign(out[i - 1]) == s[i]: out[i] = out[i - 1] + s[i]
        else: out[i] = s[i]
    return pd.Series(out, index=r.index)

def report(name, pos, t, h, cost, inv=None, neg=None, lev=None):
    y = fwd_log(R[t], h)
    st = dummy_test(pos.where(y.notna()), y, max(h, 5))
    out = dict(claim=name, etf=t, h=h, **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in st.items()})
    n_sig = int(pos.where(y.notna()).sum()); out["n_sig"] = n_sig
    out["sig_mean_bps"] = round(y[pos == 1].mean() * 1e4, 1); out["uncond_mean_bps"] = round(y.mean() * 1e4, 1)
    # backtest
    for stress in (False, True):
        c = cost[1 if stress else 0]
        net, tr = bt(pos, RS[t], h, c)
        for k in PERIODS:
            o = perf(per(net, k), tr); sfx = f"{k}{'_stres' if stress else ''}"
            out[f"sh_{sfx}"] = round(o["sh"], 2)
            if k == "oos": out[f"ann_oos{'_stres' if stress else ''}"] = round(o["ann"], 2); out["rt_yr_oos"] = round(o["rt_yr"], 2); out["mdd_oos"] = round(o["mdd"], 1)
        if not stress:
            for k in PERIODS: out[f"bh_{k}"] = round(perf(per(RS[t].dropna(), k))["sh"], 2)
            for k in PERIODS: out[f"dm_{k}"] = round(demeaned_sharpe(pos, R[t], h, c, k, "period_log"), 2)
            for k in PERIODS: out[f"dm_alt_{k}"] = round(demeaned_sharpe(pos, R[t], h, c, k, "full_simple"), 2)
            yy = net.groupby(net.index.year).sum(); out["pos_years"] = f"{int((yy > 0).sum())}/{len(yy)}"
            ext = ((net.index.year == 2008) | ((net.index >= "2013-04-01") & (net.index <= "2013-04-30")))
            out["pnl_2008"] = round(net[net.index.year == 2008].sum() * 100, 1)
            out["pnl_2013_04"] = round(net[(net.index >= "2013-04-01") & (net.index <= "2013-04-30")].sum() * 100, 1)
            out["sh_full_ex2008_2013apr"] = round(perf(net[~ext])["sh"], 2)
    # ters ETF'li sürüm (kısa sinyal varsa)
    if inv is not None and neg is not None:
        w = inv_w(inv)
        pl, _ = bt(pos, RS[t], h, cost[0])
        ps, _ = bt(neg * w, RS[inv], h, 20.0)
        comb = (pl.reindex(SESS).fillna(0) + ps.reindex(SESS).fillna(0))[RS[t].notna()]
        for k in PERIODS: out[f"inv_{inv}_{k}"] = round(perf(per(comb, k))["sh"], 2)
        for k in PERIODS: out[f"invleg_only_{k}"] = round(perf(per(ps, k))["sh"], 2)
    if lev is not None:
        netl, trl = bt(pos, RS[lev], h, 20.0)
        for k in PERIODS: out[f"lev_{lev}_{k}"] = round(perf(per(netl, k), trl)["sh"], 2)
    return out

rows = []
# ---- C3: GDX ardışık düşüş
for t in ["GDX", "GDXJ", "GLD", "SLV"]:
    stk = run_streak(R[t])
    for n_ in [3, 4, 5, 6]:
        for h in [1, 3]:
            pos = (stk.shift(1) <= -n_).astype(float)
            # kısa sinyal (simetrik): >= n gün yükseliş -> ters ETF
            neg = (stk.shift(1) >= n_).astype(float)
            inv = {"GDX": "DUST", "GDXJ": "JDST", "GLD": "GLL"}.get(t)
            lev = {"GDX": "NUGT", "GDXJ": "JNUG", "GLD": "UGL"}.get(t)
            rows.append(report(f"C3_seri_dusus>={n_}", pos, t, h, (10, 20), inv=inv, neg=neg, lev=lev))
# ---- C5: GLD Bollinger
for t in ["GLD", "GDX", "GDXJ"]:
    c = adj_on_sessions(t)
    for ddof in [1, 0]:
        z = (c - c.rolling(20).mean()) / c.rolling(20).std(ddof=ddof)
        for h in [1, 3, 5]:
            pos = (z.shift(1) < -2).astype(float); neg = (z.shift(1) > 2).astype(float)
            inv = {"GDX": "DUST", "GDXJ": "JDST", "GLD": "GLL"}[t]; lev = {"GDX": "NUGT", "GDXJ": "JNUG", "GLD": "UGL"}[t]
            o = report(f"C5_BollZ<-2_ddof{ddof}", pos, t, h, (10, 20), inv=inv, neg=neg, lev=lev); rows.append(o)
T = pd.DataFrame(rows); T.to_csv(f"{OUT}/r03_fiyat_kurallari.csv", index=False)
cols = ["claim", "etf", "h", "n_sig", "sig_mean_bps", "ic", "t", "t_is", "t_oos", "t_22", "yrs", "sh_full", "sh_is", "sh_oos", "sh_p22", "sh_oos_stres", "dm_full", "dm_oos", "dm_alt_oos", "bh_oos", "rt_yr_oos", "pos_years"]
print(T[cols].to_string())
cols2 = ["claim", "etf", "h", "pnl_2008", "pnl_2013_04", "sh_full_ex2008_2013apr", "ann_oos", "mdd_oos"] + [c for c in T.columns if c.startswith(("inv_", "invleg", "lev_"))]
print(T[(T.h.isin([1, 3, 5]))][cols2].to_string())
