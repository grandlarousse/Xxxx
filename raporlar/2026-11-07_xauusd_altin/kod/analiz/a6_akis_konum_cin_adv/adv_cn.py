"""Hakem (adversarial) yeniden üretim: Çin altın hisseleri artık getirisi -> VİOP XAUUSD fwd{h}.
Bağımsız kurulum: Yahoo ham dosyaları + Dukascopy saatlik; sıfır hacimli (askıya alınmış) günler NaN; beta yalnız t-1'e kadar.
"""
import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import load_viop, load_spot, hourly, fwd, nw_ols, ic, split_stats, backtest, IS_END, bh_fdr
OUT = f"{S}/out/a6_akis_konum_cin_adv"
D = load_viop(); SP = load_spot(); R = D["v_ret"]

# --- spot altın saatlik bar kapanışı (UTC, bar_start+1h)
hx = hourly("XAUUSD"); GX = hx["c"].copy(); GX.index = GX.index.tz_convert("UTC").tz_localize(None) + pd.Timedelta(hours=1)
pv = D["xau_p07"].dropna(); pv.index = pv.index + pd.Timedelta(hours=7)
GX = pd.concat([GX, pv[~pv.index.isin(GX.index)]]).sort_index()
pv8 = D["xau_p07"].dropna()  # (yama yalnız 07; 08 için de 07 yaması kullanılmaz)

def gold_at(ts, stale=3):
    ts = pd.DatetimeIndex(ts)
    i = GX.index.searchsorted(ts, side="right") - 1
    v = GX.values[np.clip(i, 0, None)]; t0 = GX.index[np.clip(i, 0, None)]
    ok = (i >= 0) & ((ts - t0) / pd.Timedelta(hours=1) <= stale)
    return pd.Series(np.where(ok, v, np.nan), index=ts)

CLOSE_UTC = {"600547.SS": 7, "000001.SS": 7, "1818.HK": 8, "2899.HK": 8, "_HSI": 8}

def ystock(tk, drop_zero_vol=True):
    y = pd.read_parquet(f"{S}/panel/yahoo/{tk}.parquet")
    y.index = pd.to_datetime(y.index).normalize()
    y = y[~y.index.duplicated(keep="last")]
    px = y["adjclose"] if tk not in ("_HSI", "000001.SS") else y["close"]
    if drop_zero_vol and tk not in ("_HSI", "000001.SS"):
        px = px.where(y["volume"] > 0)
    return px.dropna()

def on_days(px, days, hh):
    """gün t için: t tarihli kapanış varsa (hh UTC < 15 UTC) onu, getiri = önceki mevcut kapanışa göre; t'de kapanış yoksa NaN."""
    days = pd.DatetimeIndex(days)
    # as-of: her gün t için <= t olan son kapanış
    s = px.reindex(px.index.union(days)).ffill().reindex(days)
    has = pd.Series(days.isin(px.index), index=days)
    last_date = pd.Series(px.index, index=px.index).reindex(px.index.union(days)).ffill().reindex(days)
    r = np.log(s).diff()
    r[~has.values] = np.nan
    # pencere: önceki gün t-1'in as-of kapanış tarihi -> t
    prev_date = last_date.shift(1)
    t1 = pd.DatetimeIndex(last_date.values) + pd.Timedelta(hours=hh)
    t0 = pd.DatetimeIndex(prev_date.values) + pd.Timedelta(hours=hh)
    g = np.log(gold_at(t1).values / gold_at(t0).values)
    g = pd.Series(g, index=days); g[~has.values] = np.nan
    return r, g

def resid(days, tk, mk, win=250, minobs=150, use_mkt=True, drop0=True):
    rs, g = on_days(ystock(tk, drop0), days, CLOSE_UTC[tk])
    rm, _ = on_days(ystock(mk), days, CLOSE_UTC[mk])
    X = pd.concat([rs.rename("y"), g.rename("g"), rm.rename("m")], axis=1)
    cols = ["g", "m"] if use_mkt else ["g"]
    ok = X[["y"] + cols].notna().all(axis=1)
    Z = X[ok]
    yv = Z["y"].values; Xv = np.column_stack([np.ones(len(Z))] + [Z[c].values for c in cols])
    out = np.full(len(Z), np.nan)
    for i in range(len(Z)):
        lo = max(0, i - win)
        if i - lo < minobs: continue
        b = np.linalg.lstsq(Xv[lo:i], yv[lo:i], rcond=None)[0]     # yalnız i-1'e kadar
        out[i] = yv[i] - Xv[i] @ b
    return pd.Series(out, index=Z.index).reindex(days), g

STK = {"600547.SS": "000001.SS", "1818.HK": "_HSI", "2899.HK": "_HSI"}

def composite(days, minn=2, tks=None, **kw):
    tks = tks or list(STK)
    E = pd.concat([resid(days, tk, STK[tk], **kw)[0].rename(tk) for tk in tks], axis=1)
    return E.mean(axis=1).where(E.notna().sum(axis=1) >= minn), E

if __name__ == "__main__":
    comp, E = composite(D.index)
    A = pd.read_csv(f"{S}/out/a6_akis_konum_cin/c_asia_features.csv", index_col=0, parse_dates=True)
    print("analist bileşik ile korelasyon:", round(comp.corr(A["cn_gold_res_comp"].reindex(D.index)), 3),
          "| 600547:", round(E["600547.SS"].corr(A["res600547_SS"].reindex(D.index)), 3))
    comp_z, E_z = composite(D.index, drop0=False)
    print("sıfır hacim düşürmeden korelasyon:", round(comp_z.corr(A["cn_gold_res_comp"].reindex(D.index)), 3))
    pd.concat([comp.rename("comp"), E], axis=1).to_csv(f"{OUT}/adv_cn_features.csv")
    # spot panel 2010+
    compS, ES = composite(SP.index)
    compS0, ES0 = composite(SP.index, drop0=False)
    pd.concat([compS.rename("comp"), ES, compS0.rename("comp_keep0"), ES0.add_suffix("_keep0")], axis=1).to_csv(f"{OUT}/adv_cn_features_spot.csv")
    print("done")
