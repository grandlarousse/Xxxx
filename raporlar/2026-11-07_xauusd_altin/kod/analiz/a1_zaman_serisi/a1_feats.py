"""a1_zaman_serisi — altının kendi fiyat dinamiğinden öznitelikler.
Bilgi zamanları (UTC):
  * spot kaynaklı ('spot'): Dukascopy XAUUSD gün t 15:00 UTC (s_p15 = 14:00 barının kapanışı) ve öncesi → cutoff'ta biliniyor (temiz).
  * VİOP uzlaşma kaynaklı, gün t ('vt'): v_ret/v_settle gün t 15:05-15:15 UTC VWAP → 'kapanışta hesaplanan' (cutoff SONRASI, giriş fiyatıyla eş zamanlı).
  * VİOP uzlaşma kaynaklı, t-1 ('vt1'): gün t-1 15:15 UTC → temiz (1 gün bayat).
  * GVZ (y__GVZ): t-1 ABD kapanışı 16:15 ET (≈20:15/21:15 UTC t-1) → temiz.
  * VİOP hacim / AP / yüksek-düşük / kapanış / VWAP gün t: seans sonu 15:15 UTC (kapanış ≈15:15-15:20) → cutoff SONRASI; yalnız t-1 temiz.
"""
import numpy as np, pandas as pd

K = [1, 2, 3, 5, 10, 20, 60, 120, 250]


def rsi(P, n):
    r = P.diff()
    up = r.clip(lower=0); dn = (-r).clip(lower=0)
    au = up.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    ad = dn.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    out = 100 - 100 / (1 + au / ad)
    return out.where(ad > 0, 100.0).where(au.notna())


def dummy(cond, valid):
    return cond.astype(float).where(valid.notna())


def price_feats(P):
    """P: fiyat düzeyi serisi (gün t değeri gün t'nin fiyatı). Döndür: DataFrame, gün t satırı = P_t'ye kadar bilgi."""
    P = P.astype(float)
    lp = np.log(P); r = lp.diff()
    F = {}
    sig20 = r.rolling(20, min_periods=15).std()
    for k in K:
        rk = lp - lp.shift(k)
        F[f"ret{k}"] = rk
        F[f"vsr{k}"] = rk / (sig20 * np.sqrt(k))
    for n in [20, 50, 100, 200]:
        ma = P.rolling(n).mean(); F[f"pma{n}"] = np.sign(P - ma).where(ma.notna())
    for f, s_ in [(5, 20), (10, 50), (20, 100), (50, 200)]:
        a = P.rolling(f).mean(); b = P.rolling(s_).mean(); F[f"x{f}_{s_}"] = np.sign(a - b).where(b.notna())
    for N in [20, 55]:
        hi = P.shift(1).rolling(N).max(); lo = P.shift(1).rolling(N).min()
        ev = pd.Series(np.where(P > hi, 1.0, np.where(P < lo, -1.0, 0.0)), index=P.index).where(hi.notna())
        F[f"dbrk{N}"] = ev                                   # kırılım olayı (+1 yeni N-gün zirvesi, -1 yeni dip)
        F[f"dst{N}"] = ev.replace(0, np.nan).ffill()          # dur-ve-dön (turtle) durum: son kırılım yönü
    F["d52"] = lp - lp.rolling(250, min_periods=200).max()    # 52 hafta zirvesine log uzaklık (<=0)
    r2 = rsi(P, 2); r14 = rsi(P, 14)
    F["rsi2"] = r2; F["rsi14"] = r14
    F["rsi2_lo"] = dummy(r2 < 10, r2); F["rsi2_hi"] = dummy(r2 > 90, r2)
    F["rsi14_lo"] = dummy(r14 < 30, r14); F["rsi14_hi"] = dummy(r14 > 70, r14)
    ma20 = P.rolling(20).mean(); sd20 = P.rolling(20).std()
    bbz = (P - ma20) / sd20
    F["bbz"] = bbz; F["bb_lo"] = dummy(bbz < -2, bbz); F["bb_hi"] = dummy(bbz > 2, bbz)
    sg = np.sign(r).fillna(0)
    grp = (sg != sg.shift()).cumsum()
    st = sg.groupby(grp).cumsum().where(r.notna())
    F["streak"] = st; F["up3"] = dummy(st >= 3, st); F["dn3"] = dummy(st <= -3, st)
    z1 = r / sig20.shift(1)
    F["z1"] = z1; F["up2s"] = dummy(z1 > 2, z1); F["dn2s"] = dummy(z1 < -2, z1)
    rv5 = r.rolling(5).std() * np.sqrt(252); rv20 = r.rolling(20).std() * np.sqrt(252); rv60 = r.rolling(60).std() * np.sqrt(252)
    F["rv5"] = rv5; F["rv20"] = rv20; F["rv60"] = rv60; F["dlrv"] = np.log(rv5 / rv60)
    F["_sig20"] = sig20; F["_ma200"] = P.rolling(200).mean(); F["_P"] = P
    return pd.DataFrame(F)


def expanding_pct(x, minp=250):
    v = x.values; out = np.full(len(v), np.nan); hist = []
    for i, xi in enumerate(v):
        if np.isfinite(xi):
            hist.append(xi)
            if len(hist) >= minp:
                a = np.asarray(hist); out[i] = (a <= xi).mean()
    return pd.Series(out, index=x.index)


def spot_range_loc(spot_index, p15, hourly_df):
    """Gün t için (15:00 UTC t-1, 15:00 UTC t] penceresindeki spot saatlik yüksek/düşük; p15'in bu aralıktaki yeri (0..1). Temiz (15:00 UTC)."""
    cut = pd.DatetimeIndex(spot_index).tz_localize("UTC") + pd.Timedelta(hours=15)
    end = hourly_df.index + pd.Timedelta(hours=1)
    pos = cut.searchsorted(end, side="left")
    ok = pos < len(cut)
    g = pd.DataFrame({"h": hourly_df.h.values[ok], "l": hourly_df.l.values[ok], "k": pos[ok]})
    agg = g.groupby("k").agg(h=("h", "max"), l=("l", "min"))
    agg.index = pd.DatetimeIndex(spot_index)[agg.index]
    agg = agg.iloc[1:]  # ilk pencere tüm geçmişi kapsar
    hi = agg.h.reindex(spot_index); lo = agg.l.reindex(spot_index)
    loc = ((p15 - lo) / (hi - lo)).where((hi - lo) > 0)
    return loc.clip(0, 1), np.log(hi / lo)


def to_viop(F, vidx):
    """Spot takvimli öznitelikleri VİOP günlerine as-of taşı. Spot takviminde OLAN günlerde aynı günün değeri (NaN ise NaN kalır);
    spot takviminde OLMAYAN VİOP günlerinde (ör. 25 Aralık) son spot gününün satırı (en fazla 4 takvim günü geriye) kullanılır."""
    out = F.reindex(vidx)
    miss = ~vidx.isin(F.index)
    if miss.any():
        md = vidx[miss]
        pos = F.index.searchsorted(md, side="right") - 1
        ok = (pos >= 0)
        ok &= np.asarray((md - F.index[np.clip(pos, 0, None)]).days <= 4)
        out.loc[md[ok]] = F.iloc[pos[ok]].values
    return out
