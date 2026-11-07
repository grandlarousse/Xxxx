"""Ortak araştırma kütüphanesi — VİOP XAUUSD lead-lag.
Kullanım:  import sys; sys.path.insert(0, '<S>/code'); from lib_altin import *
Kurallar özet (ayrıntı DATA_README.md):
  - Hedef: fwd{h} = VİOP aktif kontrat uzlaşma getirilerinin t+1..t+h toplamı (log). Giriş t uzlaşması (~15:10 UTC).
  - Öngörücü x_t, t günü 15:00 UTC'den ÖNCE tamamen bilinmeli. Panel sütunları buna göre hizalı (as-of).
  - Örtüşen h>1 getirilerde Newey-West (lag >= h) zorunlu.
  - IS = 2017-03..2021-12, OOS = 2022-01..son. Her test 'register()' ile kayda geçer (çoklu test düzeltmesi için).
"""
import os, json, numpy as np, pandas as pd
S = os.environ.get("ALTIN_S", "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad")
P = f"{S}/panel"
IS_END = pd.Timestamp("2021-12-31")
COST_BPS = 5.0   # gidiş-dönüş temel maliyet (spread + komisyon), VİOP XAUUSD
REG_DIR = f"{S}/out/registry"  # ajan başına bir CSV: {REG_DIR}/<agent>.csv

def load_viop():
    d = pd.read_parquet(f"{P}/panel_viop.parquet"); d.index = pd.to_datetime(d.index); return d

def load_spot():
    d = pd.read_parquet(f"{P}/panel_spot.parquet"); d.index = pd.to_datetime(d.index); return d

def hourly(sym):
    """Dukascopy BID saatlik: index = bar başlangıcı UTC; fiyat anı için index+1h kullan."""
    return pd.read_parquet(f"{P}/duka/{sym}.parquet")

def fwd(ret, h):
    return sum(ret.shift(-k) for k in range(1, h + 1))

def nw_ols(y, x, lags=None, add_const=True):
    """y ~ a + b x. Newey-West HAC t. Döndür: dict(b, t, n, r2). x DataFrame olabilir (çoklu)."""
    import statsmodels.api as sm
    X = pd.DataFrame(x).copy()
    d = pd.concat([pd.Series(y, name="y"), X], axis=1).dropna()
    if len(d) < 30: return dict(b=np.nan, t=np.nan, n=len(d), r2=np.nan)
    Xm = sm.add_constant(d.iloc[:, 1:]) if add_const else d.iloc[:, 1:]
    L = lags if lags is not None else 5
    m = sm.OLS(d["y"], Xm).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    k = d.columns[1]
    return dict(b=float(m.params[k]), t=float(m.tvalues[k]), n=int(len(d)), r2=float(m.rsquared), model=m)

def ic(x, y, lags=5, method="spearman"):
    """Bilgi katsayısı (korelasyon) + NW t (rank dönüşümü sonrası OLS)."""
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    if len(d) < 30: return dict(ic=np.nan, t=np.nan, n=len(d))
    if method == "spearman":
        d = d.rank()
    c = d.corr().iloc[0, 1]
    zx = (d.x - d.x.mean()) / d.x.std(); zy = (d.y - d.y.mean()) / d.y.std()
    r = nw_ols(zy, zx, lags=lags)
    return dict(ic=float(c), t=r["t"], n=len(d))

def split_stats(x, y, h, method="spearman"):
    """Tam dönem, IS, OOS ve yıllık IC; yılların kaçında aynı işaret."""
    L = max(h, 5)
    full = ic(x, y, L, method); is_ = ic(x[x.index <= IS_END], y[y.index <= IS_END], L, method); oos = ic(x[x.index > IS_END], y[y.index > IS_END], L, method)
    d = pd.concat([pd.Series(x, name="x"), pd.Series(y, name="y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method=method) if len(g) > 20 else np.nan)
    sgn = np.sign(full["ic"])
    return dict(ic=full["ic"], t=full["t"], n=full["n"], ic_is=is_["ic"], t_is=is_["t"], ic_oos=oos["ic"], t_oos=oos["t"],
                yrs_same_sign=int((np.sign(yr) == sgn).sum()), yrs=int(yr.notna().sum()), by_year=yr.round(3).to_dict())

def backtest(pos, ret, h, cost_bps=COST_BPS, demean=False):
    """pos_t ∈ [-1,1], t kapanışında alınır, h gün tutulur. 'Kademeli' uygulama: her gün sermayenin 1/h'i ile yeni pozisyon açılır,
    h gün sonra kapanır (örtüşen h alt portföyün ortalaması). Günlük portföy getirisi = mean_{k=0..h-1} pos_{t-k} * ret_{t+1}... .
    Maliyet: her alt portföyde pozisyon değişimi |Δpos| × cost/2 (tek yön) — açılış+kapanış = cost. demean=True: getiriden örneklem ortalaması çıkarılır (drift etkisini ayıklar).
    Döndür: dict(ann_ret, ann_vol, sharpe, hit, n_days, exposure, turnover_per_yr, t_daily, pnl Series)."""
    r = ret.copy()
    if demean: r = r - r.mean()
    pos = pos.reindex(r.index).fillna(0).clip(-1, 1)
    # gün t+1 getirisi için etkin (netleştirilmiş) pozisyon: t, t-1, ..., t-h+1 günlerinde açılmış alt portföylerin ortalaması
    eff = sum(pos.shift(k).fillna(0) for k in range(h)) / h
    gross = eff.shift(1) * r
    # maliyet: toplam pozisyondaki değişim |eff_t - eff_{t-1}| × tek yön maliyet (cost_bps/2), t kapanışında ödenir -> t+1 getirisinden düşülür
    turn = (eff - eff.shift(1).fillna(0)).abs()
    cost = turn.shift(1).fillna(0) * cost_bps / 2 / 1e4
    net = (gross - cost).dropna()
    if len(net) < 50: return None
    ann = net.mean() * 252; vol = net.std() * np.sqrt(252)
    t = net.mean() / (net.std() / np.sqrt(len(net))) if net.std() > 0 else np.nan
    return dict(ann_ret=float(ann), ann_vol=float(vol), sharpe=float(ann / vol) if vol > 0 else np.nan, hit=float((net[eff.shift(1).reindex(net.index) != 0] > 0).mean()),
                n_days=int(len(net)), exposure=float(eff.abs().mean()), turnover_per_yr=float(turn.sum() / len(net) * 252), t_daily=float(t), pnl=net)

def bt_summary(pos, ret, h, cost_bps=COST_BPS):
    """IS/OOS ayrı: ham ve demean edilmiş getirilerle net Sharpe; ayrıca her zaman uzun (buy&hold) karşılaştırması."""
    out = {}
    for nm, msk in [("full", slice(None)), ("is", ret.index <= IS_END), ("oos", ret.index > IS_END)]:
        rr = ret[msk] if not isinstance(msk, slice) else ret
        pp = pos.reindex(rr.index)
        a = backtest(pp, rr, h, cost_bps); b = backtest(pp, rr, h, cost_bps, demean=True)
        out[nm] = dict(sharpe=a and round(a["sharpe"], 2), ann=a and round(a["ann_ret"] * 100, 2), hit=a and round(a["hit"], 3), turnover=a and round(a["turnover_per_yr"], 1),
                       sharpe_demeaned=b and round(b["sharpe"], 2), exposure=a and round(a["exposure"], 2))
    bh = backtest(pd.Series(1.0, index=ret.index), ret, 1, 0)
    out["buyhold_sharpe_full"] = round(bh["sharpe"], 2)
    return out

def bh_fdr(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.clip(q, 0, 1)

def register(agent, family, test_id, predictor, h, stats, note=""):
    """Her bir hipotez testini kayda geçir (sonuç ne olursa olsun). stats: split_stats() çıktısı veya dict(ic,t,n,...)."""
    os.makedirs(REG_DIR, exist_ok=True); REG = f"{REG_DIR}/{agent}.csv"
    from scipy import stats as st
    row = dict(agent=agent, family=family, test_id=test_id, predictor=predictor, h=h, n=stats.get("n"), ic=stats.get("ic"), t=stats.get("t"),
               p=float(2 * (1 - st.norm.cdf(abs(stats.get("t")))) if stats.get("t") is not None and np.isfinite(stats.get("t")) else np.nan),
               t_is=stats.get("t_is"), t_oos=stats.get("t_oos"), ic_oos=stats.get("ic_oos"), yrs_same_sign=stats.get("yrs_same_sign"), yrs=stats.get("yrs"), note=note)
    pd.DataFrame([row]).to_csv(REG, mode="a", header=not os.path.exists(REG), index=False)
    return row

def placebo_lead(x, ret, h):
    """İleriye bakma kontrolü: x'i 1..3 gün GERİ kaydırınca (yani daha eski bilgi) sonuç benzer olmalı; x'i İLERİ kaydırınca (gelecek bilgisi) patlıyorsa dikkat.
    Döndür: {shift: IC} — shift<0 = geleceğe bakan (yasak), shift>0 = daha eski bilgi."""
    y = fwd(ret, h)
    return {s: round(ic(x.shift(s), y, max(h, 5))["ic"], 4) for s in (-2, -1, 0, 1, 2, 3)}
