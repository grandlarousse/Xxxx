"""a8 ortak yardımcılar: kayıt temizleme, değerlendirme ölçütleri (CT R², Clark-West, isabet, backtest özetleri)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_altin import *  # noqa

AGENT = "a8_ml_kombinasyon"
OUT = f"{S}/out/{AGENT}"
REG = f"{REG_DIR}/{AGENT}.csv"


def clear_family(fams):
    """Betik yeniden çalıştırıldığında kendi ailesinin eski kayıtlarını sil (çift sayımı önler)."""
    if not os.path.exists(REG): return
    r = pd.read_csv(REG)
    r = r[~r.family.isin(fams)]
    r.to_csv(REG, index=False)


def nw_mean_t(x, lags):
    import statsmodels.api as sm
    x = pd.Series(x).dropna()
    if len(x) < 30: return np.nan
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(m.tvalues[0])


def forecast_metrics(y, yhat, ybar, h):
    """y: gerçekleşen fwd_h; yhat: model tahmini; ybar: eğitim penceresinin tarihsel ortalaması (o anki).
    Döndür: R2_hm (CT, tarihsel ortalama kıyası), R2_0 (sıfır = rastgele yürüyüş kıyası), CW t (hm ve 0), isabet, temel isabet."""
    dd = pd.concat([y.rename("y"), yhat.rename("f"), ybar.rename("b")], axis=1).dropna()
    if len(dd) < 50: return {}
    e_m = (dd.y - dd.f) ** 2; e_b = (dd.y - dd.b) ** 2; e_0 = dd.y ** 2
    L = max(h, 5)
    cw_hm = e_b - (e_m - (dd.b - dd.f) ** 2)
    cw_0 = e_0 - (e_m - (0 - dd.f) ** 2)
    return dict(n=len(dd), r2_hm=float(1 - e_m.sum() / e_b.sum()), r2_0=float(1 - e_m.sum() / e_0.sum()),
                cw_t_hm=nw_mean_t(cw_hm, L), cw_t_0=nw_mean_t(cw_0, L),
                hit=float((np.sign(dd.f) == np.sign(dd.y)).mean()), hit_base_long=float((dd.y > 0).mean()),
                hit_timing=float((np.sign(dd.f - dd.b) == np.sign(dd.y - dd.b)).mean()),
                frac_long=float((dd.f > 0).mean()))


def bt_block(pos, ret, h, cost=COST_BPS):
    """Tek dönem: ham ve demeaned net Sharpe, yıllık getiri, uzun ve kısa bacak, B&H."""
    a = backtest(pos, ret, h, cost); b = backtest(pos, ret, h, cost, demean=True)
    L = backtest(pos.clip(lower=0), ret, h, cost); Sh = backtest(pos.clip(upper=0), ret, h, cost)
    bh = backtest(pd.Series(1.0, index=ret.index), ret, 1, 0); bhd = backtest(pd.Series(1.0, index=ret.index), ret, 1, 0, demean=True)
    f = lambda z, k: (round(z[k], 3) if z is not None else np.nan)
    return dict(sharpe=f(a, "sharpe"), sharpe_dm=f(b, "sharpe"), ann=f(a, "ann_ret"), turnover=f(a, "turnover_per_yr"), exposure=f(a, "exposure"),
                long_sharpe=f(L, "sharpe"), long_ann=f(L, "ann_ret"), short_sharpe=f(Sh, "sharpe"), short_ann=f(Sh, "ann_ret"),
                bh_sharpe=f(bh, "sharpe"), bh_ann=f(bh, "ann_ret"), t_daily=f(a, "t_daily"))


def yearly_sharpe(pos, ret, h, cost=COST_BPS):
    a = backtest(pos, ret, h, cost)
    if a is None: return {}
    p = a["pnl"]; g = p.groupby(p.index.year)
    return {int(k): round(float(v.mean() / v.std() * np.sqrt(252)), 2) if v.std() > 0 else np.nan for k, v in g}
