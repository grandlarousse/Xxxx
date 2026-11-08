"""a2_seans_gunici ortak yardımcılar: yamalı saatlik XAUUSD fiyat serisi, segment getirileri, test+kayıt sarmalayıcıları.
Zaman kuralı: Dukascopy saatlik bar index = bar başlangıcı (UTC); fiyat anı = index + 1 saat (bar kapanışı).
Segmentler (gün t satırı; t-1 = endeksteki önceki gün):
  S1 eve  : t-1 15:00 -> t-1 20:00  (VİOP akşam seansı / NY öğleden sonra)  -> t 15:00'ten önce biter
  S2 late : t-1 20:00 -> t 00:00
  S3 asia : t 00:00 -> t 07:00
  S4 lon  : t 07:00 -> t 12:00
  S5 nyam : t 12:00 -> t 15:00   (ABD veri saatleri 12:30/13:30 UTC)
  S1+..+S5 = log(p15_t / p15_{t-1}) = 15:00->15:00 spot getirisi. Hepsi gün t 15:00 UTC'de bilinir (cutoff'ta kapanır).
"""
import os, sys, glob, lzma, numpy as np, pandas as pd
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
sys.path.insert(0, f"{S}/code")
from lib_altin import *  # noqa
OUT = f"{S}/out/a2_seans_gunici"
AGENT = "a2_seans_gunici"
SEGS = ["S1_eve", "S2_late", "S3_asia", "S4_lon", "S5_nyam"]

def minute_patch(sym="XAUUSD"):
    out = []
    for f in sorted(glob.glob(f"{S}/data/duka_m/{sym}/2026*.bi5")):
        b = open(f, "rb").read()
        if not b: continue
        day = pd.Timestamp(os.path.basename(f)[:8], tz="UTC")
        raw = lzma.decompress(b)
        a = np.frombuffer(raw, dtype=">i4").reshape(-1, 6)
        vol = np.frombuffer(raw, dtype=">f4").reshape(-1, 6)[:, 5]
        t = day + pd.to_timedelta(a[:, 0], unit="s")
        out.append(pd.DataFrame({"t": t, "o": a[:, 1] / 1e3, "c": a[:, 2] / 1e3, "l": a[:, 3] / 1e3, "h": a[:, 4] / 1e3, "v": vol}))
    if not out: return None
    m = pd.concat(out); m = m[m.v > 0].set_index("t").sort_index()
    hr = m.resample("1h").agg({"o": "first", "c": "last", "l": "min", "h": "max", "v": "sum"}).dropna()
    hr.index.name = "bar_start_utc"
    return hr

_HB = None
def hourly_bars(sym="XAUUSD"):
    """Yamalı saatlik bar (index = bar başlangıcı UTC)."""
    global _HB
    if _HB is not None: return _HB
    d = hourly(sym)
    pm = minute_patch(sym)
    if pm is not None:
        d = pd.concat([d, pm[~pm.index.isin(d.index)]]).sort_index()
    _HB = d
    return d

def price_series(sym="XAUUSD"):
    """Fiyat anı = bar_start + 1h (bar kapanışı)."""
    d = hourly_bars(sym)
    s = d["c"].copy(); s.index = d.index + pd.Timedelta(hours=1)
    return s

def segments(df):
    """df: panel (xau_p00,p07,p12,p15,xau_p15_prev,xau_p20_prev). Gün t'de 15:00 UTC'de bilinen segment getirileri."""
    o = pd.DataFrame(index=df.index)
    o["S1_eve"] = np.log(df.xau_p20_prev / df.xau_p15_prev)
    o["S2_late"] = np.log(df.xau_p00 / df.xau_p20_prev)
    o["S3_asia"] = np.log(df.xau_p07 / df.xau_p00)
    o["S4_lon"] = np.log(df.xau_p12 / df.xau_p07)
    o["S5_nyam"] = np.log(df.xau_p15 / df.xau_p12)
    o["C_full"] = np.log(df.xau_p15 / df.xau_p15_prev)
    o["C_post"] = o.S1_eve + o.S2_late           # t-1 15:00 -> t 00:00
    o["C_night"] = o.S2_late + o.S3_asia          # t-1 20:00 -> t 07:00
    o["C_on"] = o.S1_eve + o.S2_late + o.S3_asia  # t-1 15:00 -> t 07:00 (VİOP uzlaşmasından Londra açılışına)
    o["C_day"] = o.S4_lon + o.S5_nyam             # t 07:00 -> t 15:00
    o["C_pre"] = o.S3_asia + o.S4_lon + o.S5_nyam # t 00:00 -> t 15:00
    o["D_asia_ny"] = o.S3_asia - o.S5_nyam        # Asya - NY sabahı ayrışması
    return o

def reset_families(fams):
    fn = f"{REG_DIR}/{AGENT}.csv"
    if not os.path.exists(fn): return
    r = pd.read_csv(fn)
    r = r[~r.family.isin(fams)]
    r.to_csv(fn, index=False)

def test(family, test_id, predictor, x, y, h, note=""):
    st = split_stats(x, y, h)
    register(AGENT, family, test_id, predictor, h, st, note)
    return dict(family=family, test_id=test_id, predictor=predictor, h=h, n=st["n"], ic=round(st["ic"], 4), t=round(st["t"], 2),
                ic_is=round(st["ic_is"], 4), t_is=round(st["t_is"], 2), ic_oos=round(st["ic_oos"], 4), t_oos=round(st["t_oos"], 2),
                yrs=f'{st["yrs_same_sign"]}/{st["yrs"]}', note=note)

def mean_test(x, lags=5):
    """Ortalama getiri ve NW t (sabit üzerine regresyon)."""
    import statsmodels.api as sm
    x = pd.Series(x).dropna()
    if len(x) < 30: return dict(mean=np.nan, t=np.nan, n=len(x))
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return dict(mean=float(x.mean()), t=float(m.tvalues[0]), n=len(x))

def legs(pos, ret, h, cost=COST_BPS):
    """Uzun/kısa bacak ve buy&hold kıyası; tam/IS/OOS; ham ve demeaned Sharpe."""
    res = {}
    for nm, p in [("both", pos), ("long", pos.clip(lower=0)), ("short", pos.clip(upper=0))]:
        b = bt_summary(p, ret, h, cost)
        res[nm] = b
    return res

def fmt_legs(res):
    rows = []
    for leg, b in res.items():
        for per in ("full", "is", "oos"):
            d = b[per]
            rows.append(dict(leg=leg, per=per, sharpe=d["sharpe"], sharpe_dm=d["sharpe_demeaned"], ann_pct=d["ann"], hit=d["hit"], turn=d["turnover"], expo=d["exposure"]))
    df = pd.DataFrame(rows)
    df["bh_full"] = list(res.values())[0]["buyhold_sharpe_full"]
    return df

def bh_stats(ret):
    out = {}
    for nm, msk in [("full", slice(None)), ("is", ret.index <= IS_END), ("oos", ret.index > IS_END)]:
        rr = ret[msk] if not isinstance(msk, slice) else ret
        b = backtest(pd.Series(1.0, index=rr.index), rr, 1, 0)
        out[nm] = round(b["sharpe"], 2)
    return out

def roll_window_mask(v, h):
    """True: t+1..t+h penceresinde aktif kontrat değişimi (roll) YOK."""
    ch = v.v_code.ne(v.v_code.shift()).astype(int)
    ch.iloc[0] = 0
    f = sum(ch.shift(-k).fillna(0) for k in range(1, h + 1))
    return f == 0

def extreme_mask(idx):
    """True: uç dönemler (Mart 2020, Ocak-Şubat 2026) DIŞINDA."""
    idx = pd.DatetimeIndex(idx)
    bad = ((idx >= "2020-03-01") & (idx <= "2020-03-31")) | ((idx >= "2026-01-01") & (idx <= "2026-02-28"))
    return pd.Series(~bad, index=idx)
