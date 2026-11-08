"""Aile havuzu değerlendirmesi: birden fazla ETF'deki işlemleri birleştirip hafta-kümeli t verir;
her işlem için SPY beta-hedge'li (sektöre özgü) getiriyi de hesaplar (yalnız teşhis amaçlı; Midas'ta açığa satış yok)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import *

_D = {}


def D(sym):
    if sym not in _D:
        if os.path.exists(os.path.join(lib.DATA, "etf", sym + ".parquet")):
            _D[sym] = lib.load(sym)
        else:  # hisse (temettüsüz ham)
            df = pd.read_parquet(os.path.join(lib.DATA, "stock", sym + ".parquet"))
            df = df[df["c"] > 0].copy(); df["raw_c"] = df["c"]; df["dv"] = df["c"] * df["v"]
            _D[sym] = df
    return _D[sym]


def beta60(sym, ref="SPY", n=60):
    a = np.log(D(sym)["c"]).diff(); b = np.log(D(ref)["c"]).diff().reindex(a.index)
    return (a.rolling(n).cov(b) / b.rolling(n).var())


def add_hedge(tr, sym, mode, ref="SPY"):
    """tr'ye ref getirisini (aynı giriş/çıkış) ve beta60 hedge'li getiriyi ekler."""
    if len(tr) == 0:
        tr["ref"] = []; tr["hedged"] = []; return tr
    R = D(ref); b = beta60(sym, ref)
    ep = (R["o"] if mode == "O1" else R["c"]).reindex(pd.to_datetime(tr["entry_date"])).values
    xp = R["c"].reindex(pd.to_datetime(tr["exit_date"])).values
    tr = tr.copy()
    tr["ref"] = xp / ep - 1
    tr["beta"] = b.reindex(pd.to_datetime(tr["sig_date"])).values
    tr["hedged"] = tr["gross"] - tr["beta"].fillna(1.0) * tr["ref"]
    return tr


def run_sym(sym, sig, h, mode, pos=2500.0, exit_sig=None, hedge=True, warm=200):
    df = D(sym)
    sig = sig.reindex(df.index).fillna(False).astype(bool).copy()
    if warm: sig.iloc[:warm] = False
    cost = cost_for(df, pos)
    tr = lib.trades(df, sig, h, mode, exit_sig, cost)
    tr["sym"] = sym; tr["cost_bp"] = cost
    if hedge: tr = add_hedge(tr, sym, mode)
    return tr


def summarize(tr, label="", per_sym=True):
    """Havuz özeti: işlem düzeyi + hafta-kümeli t, IS/OOS, yıllar, ETF başına pozitif oranı."""
    r = {"label": label, "n": len(tr)}
    if len(tr) < 3:
        return r
    ne = tr["net"].values; g = tr["gross"].values
    r["mean_gross_bp"] = g.mean() * 1e4; r["mean_net_bp"] = ne.mean() * 1e4
    r["win"] = float((ne > 0).mean())
    w = ne[ne > 0].sum(); l = -ne[ne < 0].sum(); r["pf"] = float(w / l) if l > 0 else np.inf
    r["t_naive"] = tstat(ne)
    tc, nw, mw = clustered_t(tr); r["t_cl"] = tc; r["n_weeks"] = nw
    r["t_cl_ay"] = clustered_t(tr, "M")[0]
    r["p_cl"] = lib.t_to_p(tc, nw) if np.isfinite(tc) else np.nan
    tw, _, mwk = week_mean_t(tr); r["t_wk_eq"] = tw; r["wk_eq_net_bp"] = mwk
    r["worst_bp"] = float(ne.min() * 1e4)
    d = pd.to_datetime(tr["sig_date"])
    for nm, m in (("is", d <= lib.IS_END), ("oos", d > lib.IS_END)):
        p = tr[m.values]
        r[f"{nm}_n"] = len(p)
        r[f"{nm}_net_bp"] = p["net"].mean() * 1e4 if len(p) else np.nan
        r[f"{nm}_t_cl"] = clustered_t(p)[0] if len(p) > 3 else np.nan
    wk = tr.groupby(d.dt.to_period("W-FRI").values)["net"].mean()
    yrs = wk.groupby(wk.index.year).sum()
    r["years_pos_frac"] = float((yrs > 0).mean()); r["n_years"] = len(yrs)
    # hafta-ortalaması serisinden eşit ağırlıklı "portföy" maxDD (her hafta bir birim)
    eq = np.cumprod(1 + wk.sort_index().values); r["maxdd_wk"] = float((eq / np.maximum.accumulate(eq) - 1).min())
    if "hedged" in tr:
        hd = tr["hedged"].dropna()
        r["mean_hedged_bp"] = hd.mean() * 1e4
        r["t_hedged_cl"] = clustered_t(tr.dropna(subset=["hedged"]), col="hedged")[0]
        r["mean_ref_bp"] = tr["ref"].mean() * 1e4
    if per_sym and "sym" in tr:
        ps = tr.groupby("sym")["net"].mean()
        r["n_sym"] = len(ps); r["pos_sym_frac"] = float((ps > 0).mean())
        if "cl" not in tr:
            cl = tr["sym"].map(CL_OF)
            pc = tr.groupby(cl)["net"].mean(); r["n_cl"] = len(pc); r["pos_cl_frac"] = float((pc > 0).mean())
    return r


def neff_from_corr(syms, start="2017-01-01"):
    """Günlük getiri korelasyon matrisinin özdeğerlerinden etkin bağımsız seri sayısı: (Σλ)²/Σλ²."""
    R = pd.DataFrame({s: np.log(D(s)["c"]).diff() for s in syms})
    R = R[R.index >= start].dropna(how="any")
    lam = np.linalg.eigvalsh(R.corr().values)
    return float(lam.sum() ** 2 / (lam ** 2).sum()), len(R)
