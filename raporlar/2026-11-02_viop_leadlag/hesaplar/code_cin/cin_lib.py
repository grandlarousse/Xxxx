"""cin ajanı ortak yardımcıları (ll.py'yi DEĞİŞTİRMEZ, üstüne kurar).
Sembol önekleri:
  'SIDX:sh000300'  -> Sina A-pay endeksi (Yahoo 000300.SS bozuk: n=1)
  'SIDX:USDCNH'    -> Sina USD/CNH
  'FUT:I'          -> Çin vadelisi, ROLL-DÜZELTİLMİŞ hibrit seri (tekil kontratlar ~2018+; öncesi sürekli seri + roll-günü filtresi)
  'FUT0:I'         -> Sina sürekli ana kontrat (ham, roll sıçramalı)
  diğerleri        -> Yahoo (ll.raw / data/daily)
Zamanlama: Çin borsaları (A-pay, vadeli gün seansı) kapanışı 15:00 Pekin = 07:00 UTC (BIST sürekli işlem açılışı ile aynı an).
Çin vadeli gece seansı (21:00-23:00/01:00/02:30 Pekin = 13:00-15:00/17:00/18:30 UTC) ERTESİ işlem gününün barına yazılır.
=> Çin vadeli r(t) penceresi = (07:00 UTC t-1, 07:00 UTC t]: BIST t-1 seansının tamamını + t gap'ini kapsar.
"""
import os, sys, json, re, glob, numpy as np, pandas as pd
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code"); import ll
SINA = SCR + "/data_cin/sina"; SIDX = SCR + "/data_cin/sina_idx"
_c = {}

def _load_json(sym):
    p = os.path.join(SINA, sym + ".json")
    if not os.path.exists(p): return None
    d = json.load(open(p))
    if not d: return None
    df = pd.DataFrame(d)
    df["ldate"] = pd.to_datetime(df["d"]); df = df.set_index("ldate").sort_index()
    for k in ["o", "h", "l", "c", "v", "p", "s"]:
        if k in df: df[k] = pd.to_numeric(df[k], errors="coerce")
    df = df[~df.index.duplicated(keep="last")]
    return df

def _exp_key(code, name):
    yymm = name[len(code):]; return int(yymm)

def roll_adjusted(code, oi_share=0.6):
    """Tekil kontratlardan max-açık-pozisyon (bir önceki gün) kuralıyla roll-düzeltilmiş log getiri.
    Ana kontrat yalnızca ileri vadeye geçebilir (cummax). Dönüş: (r_adj Series, info dict)."""
    files = sorted(glob.glob(os.path.join(SINA, f"{code}[0-9][0-9][0-9][0-9].json")))
    C, P = {}, {}
    for f in files:
        nm = os.path.basename(f)[:-5]
        if not re.fullmatch(code + r"\d{4}", nm): continue
        df = _load_json(nm)
        if df is None or len(df) < 5: continue
        C[nm] = df["c"]; P[nm] = df["p"]
    if not C: return None, {}
    cols = sorted(C, key=lambda x: _exp_key(code, x))
    C = pd.DataFrame(C)[cols]; P = pd.DataFrame(P)[cols].fillna(0)
    C = C.where(C > 0)
    main = P.values.argmax(axis=1); main = np.maximum.accumulate(main)
    main = pd.Series(main, index=P.index)
    lc = np.log(C); dr = lc.diff()
    prev = main.shift(1)
    r = pd.Series(np.nan, index=P.index)
    ok = prev.notna()
    idx = np.where(ok)[0]
    r.iloc[idx] = dr.values[idx, prev.values[idx].astype(int)]
    # başlangıç: seçilen kontratın OI'si sürekli serinin OI'sinin >= oi_share katı olduğu ilk gün
    c0 = _load_json(code + "0")
    oi_main = pd.Series(P.values[np.arange(len(P)), main.values], index=P.index)
    start = None
    if c0 is not None:
        ratio = (oi_main / c0["p"].reindex(P.index)).rolling(5).min()
        good = ratio[ratio >= oi_share]
        start = good.index[0] if len(good) else None
    if start is None: start = P.index[0]
    r = r[r.index > start]
    info = {"n_contracts": len(cols), "start": str(start.date()), "n_switch": int((main.diff() > 0).sum())}
    return r, info

def fut_ret(code, hybrid=True, roll_sd=4.0):
    """Hibrit: roll-düzeltilmiş (varsa) + öncesinde sürekli seri. Sürekli seride roll günleri:
    sürekli serinin açık pozisyonunda |dlog OI|>0.35 VE |r|>roll_sd*sd olan günler NaN (sezgisel)."""
    k = ("fut", code, hybrid)
    if k in _c: return _c[k]
    c0 = _load_json(code + "0")
    r0 = np.log(c0["c"].where(c0["c"] > 0)).diff()
    doi = np.log(c0["p"].where(c0["p"] > 0)).diff().abs()
    sd = r0.rolling(120, min_periods=40).std().shift(1)
    suspect = (doi > 0.35) & (r0.abs() > roll_sd * sd)
    r0f = r0.copy(); r0f[suspect] = np.nan
    if not hybrid: _c[k] = r0f; return r0f
    ra, info = roll_adjusted(code)
    if ra is None: _c[k] = r0f; return r0f
    # KARAR (c04_roll_check): sürekli serinin roll gürültüsü büyük (ör. I: corr(ham,düzeltilmiş)=0,93; SA: 0,87) ve
    # sezgisel filtre roll günlerinin çoğunu yakalamıyor -> 'FUT:' = YALNIZCA roll-düzeltilmiş dönem (~2018-12+).
    out = ra.sort_index(); _c[k] = out; return out

def price_local(sym):
    """Yerel tarih indeksli fiyat (seviye) serisi."""
    if sym in _c: return _c[sym]
    if sym.startswith("SIDX:"):
        d = pd.read_parquet(os.path.join(SIDX, sym[5:] + ".parquet")); s = pd.Series(d["c"].values, index=pd.DatetimeIndex(d["ldate"]))
    elif sym.startswith("FUT:"):
        r = fut_ret(sym[4:]).fillna(0); s = np.exp(r.cumsum())
    elif sym.startswith("FUT0:"):
        d = _load_json(sym[5:] + "0"); s = d["c"]
    else:
        s = ll.daily(sym, on_bist_cal=False)
    s = s[~s.index.duplicated(keep="last")].dropna(); s = s[s > 0].sort_index()
    _c[sym] = s; return s

def ret_local(sym):
    """Kendi işlem günlerinde log getiri (FUT: için roll NaN'ları korunur)."""
    if sym.startswith("FUT:"):
        r = fut_ret(sym[4:]); return r
    s = price_local(sym); r = np.log(s).diff()
    sd = r.rolling(250, min_periods=60).std().shift(1); r[(r.abs() > 12 * sd) & sd.notna()] = np.nan
    return r

def ret_bist(sym):
    """BIST takvimine oturtulmuş getiri (ll konvansiyonu: sürücü fiyatı = yerel tarihi <= t olan son kapanış)."""
    k = ("rb", sym)
    if k in _c: return _c[k]
    if not (sym.startswith("SIDX:") or sym.startswith("FUT")):
        try:
            r = ll.ret(sym); _c[k] = r; return r
        except Exception:
            pass
    rl = ret_local(sym)
    cal = ll.bist_cal(); cal = cal[cal >= rl.index[0]]
    # getirileri BIST günlerine topla: BIST günü t için (önceki BIST günü, t] aralığındaki yerel getiriler
    grp = pd.Series(cal.searchsorted(rl.index, side="left"), index=rl.index)
    grp = grp[grp < len(cal)]
    agg = rl.loc[grp.index].groupby(grp.values).apply(lambda x: x.sum() if x.notna().all() else np.nan)
    # sürücünün işlem görmediği BIST günleri: 0 (ffill eşdeğeri); roll/veri NaN'ı korunur
    r = pd.Series(0.0, index=cal); r.iloc[agg.index.values.astype(int)] = agg.values
    r.iloc[0] = np.nan
    _c[k] = r; return r

def pair_orig_alt(orig, alt, start="2010-01-01"):
    """Orijinal (Çin) vs alternatif: ortak işlem günlerinde senkron, alt->orig(t+1) öncülük, 2g, haftalık korelasyon."""
    po, pa = price_local(orig), price_local(alt)
    po = po[po.index >= start]; pa = pa[pa.index >= start]
    if orig.startswith("FUT:") or alt.startswith("FUT:"):
        ro = ret_local(orig) if orig.startswith("FUT:") else None
    P = pd.concat([po.rename("o"), pa.rename("a")], axis=1, join="inner").dropna()
    if len(P) < 60: return None
    R = np.log(P).diff()
    if orig.startswith("FUT:"):  # roll NaN günlerini koru
        rr = ret_local(orig); R.loc[R.index.isin(rr[rr.isna()].index), "o"] = np.nan
    if alt.startswith("FUT:"):
        rr = ret_local(alt); R.loc[R.index.isin(rr[rr.isna()].index), "a"] = np.nan
    # 12-sigma temizliği
    for c in R:
        sd = R[c].rolling(250, min_periods=60).std().shift(1); R.loc[(R[c].abs() > 12 * sd) & sd.notna(), c] = np.nan
    R = R.iloc[1:]
    out = {"n": int(R.dropna().shape[0]), "start": str(R.index[0].date()), "end": str(R.index[-1].date())}
    out["corr_sync"] = R["o"].corr(R["a"])
    out["corr_altlead"] = R["o"].shift(-1).corr(R["a"])   # alt_t -> orig_{t+1}
    out["corr_origlead"] = R["o"].corr(R["a"].shift(-1))  # orig_t -> alt_{t+1}
    # 2 günlük örtüşmeyen
    R2 = R.fillna(0).groupby(np.arange(len(R)) // 2).sum(); out["corr_2d"] = R2["o"].corr(R2["a"]); out["n_2d"] = len(R2)
    # haftalık (Cuma-Cuma son fiyat)
    W = np.log(pd.concat([po.resample("W-FRI").last().rename("o"), pa.resample("W-FRI").last().rename("a")], axis=1).dropna()).diff().dropna()
    out["corr_weekly"] = W["o"].corr(W["a"]); out["n_w"] = len(W)
    # son 3 yıl haftalık
    W3 = W[W.index >= W.index[-1] - pd.DateOffset(years=3)]; out["corr_weekly_3y"] = W3["o"].corr(W3["a"])
    R3 = R[R.index >= R.index[-1] - pd.DateOffset(years=3)]; out["corr_sync_3y"] = R3["o"].corr(R3["a"])
    out["beta_w"] = np.cov(W["a"], W["o"])[0, 1] / W["o"].var()
    return out
