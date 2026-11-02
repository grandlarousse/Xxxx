"""gunici ajanı ortak yardımcıları (ll.py'yi değiştirmez, sadece okur).
BAR YAPISI (doğrulandı, 0_verify_bars çıktısı):
- BIST h1: bar etiketi = bar başlangıcı UTC. 06:30 barı = 06:55 açılış müzayedesi + 07:00-07:30 sürekli işlem; 07:30..13:30 tam saat;
  14:30 barı = 14:30-15:00 (30 dk); 15:00 barı = kapanış müzayedesi (sadece son gün mevcut).
- KIŞ AYLARINDA (AB yaz saati dışı, Kas-Mar) h1 verisinde 14:30 barı YOK -> son bar 13:30 (14:30'da biter); 14:30-15:10 eksik.
  Kanıt: kış son bar kapanışı vs günlük kapanış medyan |fark| %0,30 ≈ yaz 14:30 fiyatı vs kapanış %0,27 (yaz 15:00 fiyatı vs kapanış %0,09).
- Endekslerde (XU030/XU100) h1 ilk bar 'o' = ÖNCEKİ KAPANIŞ (açılış değil); açılış = günlük 'o' (= m5 06:55 barının 'c').
  Hisselerde h1 ilk bar 'o' = günlük 'o'. Bu yüzden açılış her zaman GÜNLÜK veriden alınır.
- Sürücüler: ES/NQ/BZ/GC/TRY/EURTRY/BTC h1 :00 hizalı; TUR/TKC/EEM :30 hizalı (13:30..19:30 yaz); DAX/STOXX :00 (07..15 yaz, 08..16 kış).
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
SCR = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
sys.path.insert(0, SCR + "/code"); import ll  # noqa
OUT = SCR + "/out"; CODE = OUT + "/code_gunici"; RES = CODE + "/results"; os.makedirs(RES, exist_ok=True)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
IDX = ["XU030","XU100","XBANK","XLBNK"]
TV = {"ES=F":"CME_MINI:ES1!","NQ=F":"CME_MINI:NQ1!","BZ=F":"ICEEUR:BRN1! / TVC:UKOIL","GC=F":"COMEX:GC1! / TVC:GOLD","TRY=X":"FX:USDTRY",
      "EURTRY=X":"FX:EURTRY","TUR":"AMEX:TUR (BATS:TUR?)","TKC":"NYSE:TKC","EEM":"AMEX:EEM","^GDAXI":"XETR:DAX","^STOXX":"TVC:SXXP?","^STOXX50E":"TVC:SX5E",
      "BTC-USD":"BITSTAMP:BTCUSD / COINBASE:BTCUSD","^N225":"TVC:NI225","^KS11":"KRX:KOSPI?","^HSI":"TVC:HSI? (HKEX açılmayabilir)","CNH=X":"FX:USDCNH",
      "000001.SS":"(Çin-VERİLMEZ) alt: FX:USDCNH / AMEX:ASHR / SGX:CN1!?","FXI":"AMEX:FXI","MCHI":"NASDAQ:MCHI","ASHR":"AMEX:ASHR","XU030":"BIST:XU030 / VİOP:XU0301!","XU100":"BIST:XU100"}
def tvb(s): return f"BIST:{s}" if s in VIOP or s in IDX else TV.get(s, "?")

def load(sym, kind="h1"):
    return ll.raw(ll.T(sym), kind)

def bar_end(d, sym, kind="h1"):
    """Bar bitiş zamanı = başlangıç + adım; bir sonraki bar daha erken başlıyorsa onunla sınırlı. BIST: 14:30 barı 15:00'te, 15:00 barı 15:10'da biter."""
    step = pd.Timedelta(minutes=60 if kind == "h1" else 5)
    st = d.index.tz_convert("UTC")
    e = (st + step).tz_convert(None).values
    nxt = np.append(st[1:].tz_convert(None).values, (st[-1] + step).tz_convert(None).to_datetime64())
    e = np.minimum(e, nxt)
    if ll.is_bist(ll.T(sym)) and kind == "h1":
        hm = st.hour * 100 + st.minute
        e = np.where(hm == 1430, (st + pd.Timedelta(minutes=30)).tz_convert(None).values, e)
        e = np.where(hm == 1500, (st + pd.Timedelta(minutes=10)).tz_convert(None).values, e)
    return pd.DatetimeIndex(e).tz_localize("UTC")

_px = {}
def px_series(sym, kind="h1"):
    k = (sym, kind)
    if k not in _px:
        d = load(sym, kind).copy(); d = d[~d.index.duplicated(keep="last")].sort_index(); d = d[d["c"] > 0]
        s = pd.Series(d["c"].values, index=bar_end(d, sym, kind)); s = s[~s.index.duplicated(keep="last")].sort_index()
        _px[k] = s
    return _px[k]

def snap_at(sym, times, kind="h1", max_age_h=6.0):
    """times: DatetimeIndex UTC tz-aware. Her an için o ana kadar kapanmış son barın kapanışı. max_age_h'den eskiyse NaN."""
    s = px_series(sym, kind); times = pd.DatetimeIndex(times)
    pos = s.index.searchsorted(times, side="right") - 1
    v = np.where(pos >= 0, s.values[np.clip(pos, 0, None)], np.nan)
    tt = s.index.values[np.clip(pos, 0, None)]
    age = (times.tz_convert(None).values - np.asarray(tt, dtype="datetime64[ns]")) / np.timedelta64(1, "h")
    v = np.where((pos >= 0) & (age <= max_age_h), v, np.nan)
    return pd.Series(v, index=times)

def bist_days():
    """BIST işlem günleri tablosu (XU100 h1 + günlük). Kolonlar: date, prev, nbars, half, prev_half, weekend(prev Cuma)."""
    h = load("XU100", "h1"); dts = pd.DatetimeIndex(h.index.tz_convert(None).normalize())
    nb = pd.Series(1, index=dts).groupby(level=0).sum()
    df = pd.DataFrame({"nbars": nb}); df.index.name = "date"
    df["prev"] = pd.Series(df.index, index=df.index).shift(1)
    df["half"] = df["nbars"] <= 5
    df["prev_half"] = df["half"].shift(1).fillna(False).astype(bool)
    df["gapdays"] = (pd.Series(df.index, index=df.index) - df["prev"]).dt.days
    df["monday_after_fri"] = (df.index.dayofweek == 0) & (df["gapdays"] == 3)
    return df.iloc[1:]

def utc(dates, hhmm):
    h, m = map(int, hhmm.split(":"))
    return pd.DatetimeIndex(pd.DatetimeIndex(dates) + pd.Timedelta(hours=h, minutes=m)).tz_localize("UTC")

def bist_intraday(sym, days):
    """Hisse/endeks için gün parçaları (log): gap, r30 (open->07:30), r1 (open->08:30), rest (08:30->kapanış), intra (open->close), cc.
    Açılış/kapanış günlük veriden; ara noktalar h1'den. Temettü/bölünme: ll.decomp gap kuralı (cc_adj - intra)."""
    dd = ll.decomp(sym)  # cc, gap, intra (temizlenmiş)
    d = ll.raw(ll.T(sym)).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    o = d["o"].reindex(days); c = d["c"].reindex(days)
    p0730 = snap_at(sym, utc(days, "07:30"), max_age_h=0.6).values
    p0830 = snap_at(sym, utc(days, "08:30"), max_age_h=0.6).values
    out = pd.DataFrame(index=days)
    out["cc"] = dd["cc"].reindex(days); out["gap"] = dd["gap"].reindex(days); out["intra"] = dd["intra"].reindex(days)
    out["r30"] = np.log(p0730 / o.values); out["r1"] = np.log(p0830 / o.values); out["rest"] = np.log(c.values / p0830)
    out["r_0730_close"] = np.log(c.values / p0730)
    bad = out["intra"].isna() | (out[["r30","r1","rest"]].abs() > 0.12).any(axis=1)
    out.loc[bad, ["r30","r1","rest","r_0730_close"]] = np.nan
    return out

def ols(y, X, hac=5):
    import statsmodels.api as sm
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(df) < 40: return None
    m = sm.OLS(df["y"].values, sm.add_constant(df.drop(columns="y").values)).fit(cov_type="HAC", cov_kwds={"maxlags": hac})
    return {"b": m.params[1:], "t": m.tvalues[1:], "r2": m.rsquared, "n": len(df), "names": list(df.columns[1:])}

def corr_t(a, b):
    df = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(df) < 40: return np.nan, np.nan, len(df)
    c = df["a"].corr(df["b"]); r = ols((df["a"]-df["a"].mean())/df["a"].std(), ((df["b"]-df["b"].mean())/df["b"].std()).rename("x"))
    return c, r["t"][0], len(df)

def bt_stats(pnl, pos):
    act = pos != 0; n = int(act.sum())
    if n < 15: return {"n": n, "mean_bps": np.nan, "t": np.nan, "hit": np.nan, "sharpe": np.nan}
    pa = pnl[act]; m, t, _ = ll.nw_t(pa)
    ann = pa.mean() * 252 * act.mean(); vol = pnl.std() * np.sqrt(252)
    return {"n": n, "mean_bps": 1e4 * pa.mean(), "t": t, "hit": float((pa > 0).mean()), "sharpe": ann / vol if vol > 0 else np.nan}
