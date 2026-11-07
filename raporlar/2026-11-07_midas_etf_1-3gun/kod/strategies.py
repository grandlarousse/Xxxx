"""Genel strateji kütüphanesi (parametreler literatür varsayılanı, veriye göre AYARLANMADI).
Her fonksiyon: (df, ctx) -> bool Seri (t kapanışında bilinir). ctx: ortak seriler (VIX vb.)."""
import numpy as np, pandas as pd
from lib import rsi, ibs, sma, zret, atr

def _c(df): return df["c"]

def month_last_day(idx):
    s = pd.Series(idx, index=idx)
    return s.groupby([idx.year, idx.month]).transform("max") == s

def month_nth_from_end(idx, k):
    """Ayın sondan k. işlem günü (k=1 son gün)."""
    s = pd.Series(np.arange(len(idx)), index=idx)
    g = s.groupby([idx.year, idx.month])
    return (g.transform("max") - s) == (k - 1)

def pre_holiday(idx):
    """Bir sonraki işlem günü, bir sonraki iş günü (Pzt-Cum) değilse True (tatil öncesi)."""
    nxt = pd.Series(idx[1:].append(pd.DatetimeIndex([idx[-1] + pd.Timedelta(days=1)])), index=idx)
    bnext = pd.Series(idx + pd.offsets.BDay(1), index=idx)
    return pd.Series(nxt.values > bnext.values, index=idx)

def _vix_ratio(ctx):
    return ctx["VIX"] / ctx["VIX3M"]

LIB = {
    # --- ortalamaya dönüş (long) ---
    "MR_rsi2_lt10_ust200": lambda d, x: (rsi(_c(d), 2) < 10) & (_c(d) > sma(_c(d), 200)),
    "MR_rsi2_lt10": lambda d, x: rsi(_c(d), 2) < 10,
    "MR_rsi2_lt5": lambda d, x: rsi(_c(d), 2) < 5,
    "MR_ibs_lt02": lambda d, x: ibs(d) < 0.2,
    "MR_ibs_lt02_ust200": lambda d, x: (ibs(d) < 0.2) & (_c(d) > sma(_c(d), 200)),
    "MR_ibs_lt01_dusus": lambda d, x: (ibs(d) < 0.1) & (_c(d) < _c(d).shift(1)),
    "MR_3gun_dusus": lambda d, x: (_c(d).diff() < 0) & (_c(d).diff().shift(1) < 0) & (_c(d).diff().shift(2) < 0),
    "MR_5gun_dip_ust200": lambda d, x: (_c(d) <= _c(d).rolling(5).min()) & (_c(d) > sma(_c(d), 200)),
    "MR_z1_lt_m2": lambda d, x: zret(_c(d), 1) < -2,
    "MR_z3_lt_m2": lambda d, x: zret(_c(d), 3) < -2,
    "MR_bb20_alt": lambda d, x: _c(d) < sma(_c(d), 20) - 2 * _c(d).rolling(20).std(),
    "MR_dusus_gap_ibs": lambda d, x: (d["o"] < d["c"].shift(1) * 0.99) & (ibs(d) < 0.3),
    # --- momentum / devam (long) ---
    "MO_20g_zirve": lambda d, x: _c(d) >= _c(d).rolling(20).max(),
    "MO_z1_gt_2": lambda d, x: zret(_c(d), 1) > 2,
    "MO_3gun_yukselis": lambda d, x: (_c(d).diff() > 0) & (_c(d).diff().shift(1) > 0) & (_c(d).diff().shift(2) > 0),
    "MO_ibs_gt08": lambda d, x: ibs(d) > 0.8,
    "MO_trend_10_50": lambda d, x: (_c(d) > sma(_c(d), 10)) & (sma(_c(d), 10) > sma(_c(d), 50)),
    "MO_rsi2_gt90": lambda d, x: rsi(_c(d), 2) > 90,
    # --- takvim ---
    "CA_ay_sonu": lambda d, x: month_last_day(d.index),
    "CA_ay_sonu_3": lambda d, x: month_nth_from_end(d.index, 3),
    "CA_tatil_oncesi": lambda d, x: pre_holiday(d.index),
    "CA_pzt": lambda d, x: pd.Series(d.index.dayofweek == 0, index=d.index),
    "CA_sal": lambda d, x: pd.Series(d.index.dayofweek == 1, index=d.index),
    "CA_car": lambda d, x: pd.Series(d.index.dayofweek == 2, index=d.index),
    "CA_per": lambda d, x: pd.Series(d.index.dayofweek == 3, index=d.index),
    "CA_cum": lambda d, x: pd.Series(d.index.dayofweek == 4, index=d.index),
    # --- volatilite rejimi (VIX kapanışı 16:15 ET: C0'da hafif iyimser) ---
    "VX_vix_sicrama15": lambda d, x: (x["VIX"].pct_change() > 0.15).reindex(d.index),
    "VX_vix_gerilme": lambda d, x: (x["VIX"] > 1.10 * x["VIX"].rolling(10).mean()).reindex(d.index),
    "VX_kontango_09": lambda d, x: (_vix_ratio(x) < 0.90).reindex(d.index),
    "VX_backwardation": lambda d, x: (_vix_ratio(x) > 1.0).reindex(d.index),
    "VX_backw_donus": lambda d, x: ((_vix_ratio(x) < 1.0) & (_vix_ratio(x).shift(1) >= 1.0)).reindex(d.index),
}

# Erken çıkış kuralları (en fazla h gün tutulur)
EXITS = {
    "MR_rsi2_lt10_ust200": lambda d: _c(d) > sma(_c(d), 5),
    "MR_rsi2_lt10": lambda d: _c(d) > sma(_c(d), 5),
    "MR_rsi2_lt5": lambda d: _c(d) > sma(_c(d), 5),
    "MR_ibs_lt02": lambda d: ibs(d) > 0.8,
    "MR_ibs_lt02_ust200": lambda d: ibs(d) > 0.8,
    "MR_3gun_dusus": lambda d: _c(d) > _c(d).shift(1),
}
