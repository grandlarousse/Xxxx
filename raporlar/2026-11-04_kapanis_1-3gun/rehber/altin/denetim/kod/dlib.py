"""Denetim (rehber_altin_denetim): BAĞIMSIZ kütüphane. cl/ev/pl/sinyal_altin İÇE AKTARILMAZ.
Veri: ortak VİOP paneli (salt okunur) + kendi indirdiğimiz 02-03.11.2026 bültenleri; Yahoo verisi denetim/veri altında.
Zaman: Türkiye UTC+3 (yaz saati yok). 17:55 TSİ = 14:55 UTC, 18:00 TSİ = 15:00 UTC.
"""
import glob, re
import numpy as np, pandas as pd

S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
D = S + "/out/rehber/altin/denetim"
REG = pd.Timestamp("2020-03-13")      # BIST fiyat marjı ±%20 -> ±%10
CODE_RE = re.compile(r"^F_([A-Z]+(?:030)?)(\d{2})(\d{2})$")


ALIAS = {"KOZAL": "TRALT"}          # Koza Altın -> Türk Altın (24.11.2025 kod değişimi)
def _std_code(code):
    m = CODE_RE.match(code)
    return ALIAS.get(m.group(1), m.group(1)) if m else None


_PAN = None
def panel():
    """Ortak panel + kendi bültenlerimiz (panelden sonraki günler). Yalnız standart aylık vadeli kodlar (F_<UND>MMYY)."""
    global _PAN
    if _PAN is not None:
        return _PAN
    cols = ["date", "code", "expiry", "settle", "prev_settle", "close", "high", "low", "qty", "value_tl"]
    p = pd.read_parquet(S + "/data/viop_panel.parquet", columns=cols)
    p["code"] = p["code"].astype(str)
    p["date"] = pd.DatetimeIndex(p["date"]).normalize(); p["expiry"] = pd.DatetimeIndex(p["expiry"]).normalize()
    last = p["date"].max(); add = []
    for f in sorted(glob.glob(D + "/veri/viop/viop_????????.csv")):
        b = pd.read_csv(f, sep=";", skiprows=[1], dtype=str)
        b.columns = [c.strip() for c in b.columns]
        o = pd.DataFrame({"date": pd.to_datetime(b["TARIH"]), "code": b["SOZLESME KODU"].str.strip(),
                          "expiry": pd.to_datetime(b["VADE TARIHI"], errors="coerce")})
        for k, c in (("settle", "UZLASMA FIYATI"), ("prev_settle", "ONCEKI UZLASMA FIYATI"), ("close", "KAPANIS FIYATI"),
                     ("high", "EN YUKSEK FIYAT"), ("low", "EN DUSUK FIYAT"), ("qty", "ISLEM MIKTARI"), ("value_tl", "ISLEM HACMI")):
            o[k] = pd.to_numeric(b[c], errors="coerce")
        add.append(o[o["date"] > last])
    if add:
        p = pd.concat([p] + add, ignore_index=True)
    p["und"] = p["code"].map(_std_code)
    p = p[p["und"].notna() & (p["settle"] > 0) & (p["prev_settle"] > 0)].copy()
    p = p.drop_duplicates(["date", "code"], keep="last")
    _PAN = p
    return p


_CAL = None
def cal():
    global _CAL
    if _CAL is None:
        p = panel(); _CAL = pd.DatetimeIndex(sorted(p.loc[p["und"] == "XU030", "date"].unique()))
    return _CAL


def td_left(dates, expiry):
    """tarih (dahil değil) -> vade (dahil) arası VİOP işlem günü sayısı; takvim dışı kısım iş günüyle uzatılır."""
    c = cal(); cv = c.values
    pos = np.searchsorted(cv, dates.values, side="left")
    ep = np.searchsorted(cv, expiry.values, side="right") - 1
    n = ep - pos
    beyond = expiry.values > cv[-1]
    if beyond.any():
        n = n.astype(float)
        n[beyond] = (len(cv) - 1 - pos[beyond]) + np.busday_count(np.datetime64(c[-1].date()), expiry.values[beyond].astype("datetime64[D]"))
    return n


_FRONT = {}
def front(und, min_td=3):
    """Her gün: vadeye >= min_td işlem günü kalan en yakın standart kontrat (kod, uzlaşma, günlük getiri, kilit bilgisi)."""
    if (und, min_td) in _FRONT:
        return _FRONT[(und, min_td)]
    p = panel(); x = p[p["und"] == und].copy()
    x["tdl"] = td_left(pd.DatetimeIndex(x["date"]), pd.DatetimeIndex(x["expiry"]))
    x = x[x["tdl"] >= min_td].sort_values(["date", "expiry"])
    f = x.groupby("date").head(1).set_index("date")
    f["r"] = np.log(f["settle"] / f["prev_settle"])
    f = f.reindex(cal())
    _FRONT[(und, min_td)] = f
    return f


_CR = {}
def contract_logret(und):
    """(gün x kontrat) ln(uzlaşma/önceki uzlaşma): aynı kontrat zinciri (bülten önceki uzlaşması bedelsiz/temettüye göre düzeltilmiş)."""
    if und not in _CR:
        p = panel(); x = p[p["und"] == und].copy(); x["r"] = np.log(x["settle"] / x["prev_settle"])
        _CR[und] = (x.pivot_table(index="date", columns="code", values="r", aggfunc="last").reindex(cal()),
                    x.pivot_table(index="date", columns="code", values="settle", aggfunc="last").reindex(cal()))
    return _CR[und]


def viop_gold_z(w=250, minp=100):
    """Araştırma sinyali (bağımsız yeniden yazım): ön vade XAUUSD uzlaşma log değişimi; 10σ üstü -> NaN; z = g / std250(önceki)."""
    g = front("XAUUSD")["r"].copy()
    sd60 = g.rolling(250, min_periods=60).std().shift(1)
    g[(g.abs() > 10 * sd60) & sd60.notna()] = np.nan
    sd = g.rolling(w, min_periods=minp).std().shift(1)
    return g, sd, g / sd


def ydaily(sym):
    d = pd.read_parquet(f"{D}/veri/daily/{sym}.parquet")
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"])).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    stale = (d["v"].fillna(0) <= 0) & (d["h"] == d["l"])
    return d[~stale]


def spot_beta(a="TRALT.IS", b="XU030.IS", w=250, minp=100, upto=None):
    c = cal()
    ra = np.log(ydaily(a)["adj"]).diff(); rb = np.log(ydaily(b)["adj"]).diff()
    if upto is not None:
        ra = ra[ra.index <= upto]; rb = rb[rb.index <= upto]
    ra = ra.reindex(c); rb = rb.reindex(c)
    m = ra.notna() & rb.notna(); ra = ra.where(m); rb = rb.where(m)
    cov = ra.rolling(w, min_periods=minp).cov(rb); var = rb.rolling(w, min_periods=minp).var()
    return (cov / var).shift(1)


def intraday(sym, kind):
    """Kendi indirmemiz; ortak veri dizininde aynı sembolün daha eski barları varsa (salt okunur) başa eklenir."""
    d = pd.read_parquet(f"{D}/veri/{kind}/{sym}.parquet")
    import os
    old = f"{S}/data/{kind}/{sym}.parquet"
    if os.path.exists(old):
        o = pd.read_parquet(old); o = o[o.index < d.index[0]]
        d = pd.concat([o, d]).sort_index()
    step = 60 if kind == "h1" else 5
    d = d[(d.index.second == 0) & (d.index.minute % step == 0)]
    return d, step


def snap(sym, kind, hh, mm, max_age_min=90, days=None, live=False):
    """BIST günü t için hh:mm UTC'de bilinen fiyat: bitişi (başlangıç+adım) <= hedef olan son barın kapanışı.
    Bar bitişi hedeften max_age_min dakikadan eskiyse NaN. live=True: bitişi gelecekte olan son (açık) bar da kabul (canlı kullanım)."""
    d, step = intraday(sym, kind)
    end = (d.index + pd.Timedelta(minutes=step)).tz_convert(None)
    s = pd.Series(d["c"].values, index=end); s = s[s > 0]
    days = cal() if days is None else days
    tg = pd.DatetimeIndex(days) + pd.Timedelta(hours=hh, minutes=mm)
    pos = np.searchsorted(s.index.values, tg.values, side="right") - 1
    ok = pos >= 0; pc = np.clip(pos, 0, None)
    age = (tg.values - s.index.values[pc]) / np.timedelta64(1, "m")
    v = np.where(ok & (age <= max_age_min), s.values[pc], np.nan)
    out = pd.Series(v, index=pd.DatetimeIndex(days))
    out[out.index < s.index[0].normalize() + pd.Timedelta(days=1)] = np.nan
    return out


def chg(px):
    """BIST takviminde ln(P_t / P_{t-1}); t-1 = önceki BIST günü (VİOP uzlaşma/önceki uzlaşma mantığı)."""
    return np.log(px / px.shift(1))


def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return np.nan if len(x) < 5 else x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))


def simulate(z, thr=1.0, h=2, start="2018-12-17", end=None, beta=None, lock=True, maxext=3, integer=True, simple=True):
    """Örtüşmesiz pratik kural. t'de |z|>thr ve pozisyon yoksa yön(z) ile F_TRALT (t'de seçilen kontrat) ve
    -b·F_XU030 aç (t uzlaşması), t+h uzlaşmasında kapat; çıkış günü yeniden sinyal bakılır (aynı yön = devam, ters = çevir).
    lock: girişte kendi yönüne kilit (alışta tavan, satışta taban) -> giriş yok; çıkışta size karşı kilit -> en fazla maxext gün uzat.
    Getiri: TRALT tutarına göre (bps). simple=True: basit getiri (TL ile birebir); False: log toplam (araştırma gibi)."""
    c = cal(); n = len(c)
    fT = front("TRALT"); fX = front("XU030")
    lrT, sT = contract_logret("TRALT"); lrX, sX = contract_logret("XU030")
    zz = z.reindex(c).values
    b = beta.reindex(c).values
    # vadeli kilit bayrağı (seçili ön vade): kapanış = gün yükseği & değişim >= limit-1 puan (tavan); tersi taban
    lim = np.where(c < REG, np.log(1.19), np.log(1.09))
    upL = ((fT["r"] >= lim) & (fT["close"] >= fT["high"] - 1e-9)).values
    dnL = ((fT["r"] <= -lim) & (fT["close"] <= fT["low"] + 1e-9)).values
    multX = np.where(c < pd.Timestamp("2020-07-27"), 100.0, 10.0)
    i = int(np.searchsorted(c.values, np.datetime64(pd.Timestamp(start))))
    iend = n if end is None else int(np.searchsorted(c.values, np.datetime64(pd.Timestamp(end)), side="right"))
    rows = []; prev = None; skipped = 0
    while i < iend - 1:
        zi = zz[i]
        if not (np.isfinite(zi) and abs(zi) > thr and isinstance(fT["code"].iloc[i], str) and isinstance(fX["code"].iloc[i], str) and np.isfinite(b[i])):
            i += 1; continue
        d = 1.0 if zi > 0 else -1.0
        if lock and ((d > 0 and upL[i]) or (d < 0 and dnL[i])):
            skipped += 1; i += 1; continue
        H = h
        if lock:
            while i + H < n - 1 and H < h + maxext and ((d > 0 and dnL[i + H]) or (d < 0 and upL[i + H])):
                H += 1
        if i + H >= n:
            break
        cT, cX = fT["code"].iloc[i], fX["code"].iloc[i]
        segT = lrT[cT].values[i + 1:i + H + 1]; segX = lrX[cX].values[i + 1:i + H + 1]
        if not (np.all(np.isfinite(segT)) and np.all(np.isfinite(segX))):
            i += 1; continue
        pT = fT["settle"].iloc[i]; pX = fX["settle"].iloc[i]
        if integer:
            N = max(1, int(round(multX[i] * pX / (b[i] * 100 * pT)))); be = multX[i] * pX / (N * 100 * pT)
        else:
            N = np.nan; be = b[i]
        RT = np.expm1(segT.sum()) if simple else segT.sum(); RX = np.expm1(segX.sum()) if simple else segX.sum()
        gross = d * (RT - be * RX)
        cont = prev is not None and prev[0] == i and prev[1] == d
        same_c = cont and prev[2] == cT and prev[3] == cX
        tkX = 0.025 if c[i] < pd.Timestamp('2020-07-27') else (0.25 if c[i] < pd.Timestamp('2025-01-01') else 1.0)   # bültenden: 2025'ten beri XU030 fiyat adımı 1 puan
        tick = (2 * 0.01 / pT * 1e4 + 4.2) + be * (2 * tkX / pX * 1e4 + 4.2)
        rows.append(dict(date=c[i], exit=c[i + H], dir=d, z=zi, hold=H, gross_bps=gross * 1e4, code_T=cT, code_X=cX, pT=pT, pX=pX,
                         beta=b[i], N=N, b_eff=be, devam=cont, devam_ayni_kontrat=same_c, tick_bps=tick,
                         notional_T=(N if integer else 1) * 100 * pT, notional_X=multX[i] * pX))
        prev = (i + H, d, cT, cX); i += H
    T = pd.DataFrame(rows)
    if len(T):
        T = T.set_index("date")
    T.attrs["skipped"] = skipped
    return T


def stats(T, cost="8+3", split="2022-01-01"):
    if len(T) < 5:
        return dict(n=len(T))
    g = T["gross_bps"].values
    if cost == "8+3": cst = 11.0
    elif cost == "15+3": cst = 18.0
    elif cost == "tik": cst = T["tick_bps"].values
    elif cost == "8+3 devam0": cst = np.where(T["devam_ayni_kontrat"].values, 0.0, 11.0)
    else: cst = float(cost)
    net = g - cst; idx = T.index
    yrs = max((idx[-1] - idx[0]).days / 365.25, 0.25)
    isd = idx < pd.Timestamp(split); m24 = idx >= pd.Timestamp("2024-01-01")
    cum = np.cumsum(net); dd = (cum - np.maximum.accumulate(np.r_[0.0, cum])[1:]).min()
    srt = np.sort(net)
    return dict(n=len(T), per_yr=len(T) / yrs, hold=T["hold"].mean(), gross=g.mean(), net=net.mean(), t=tstat(net), hit=(net > 0).mean(),
                IS=net[isd].mean(), IS_t=tstat(net[isd]), OOS=net[~isd].mean(), OOS_t=tstat(net[~isd]),
                y24=net[m24].mean(), y24_t=tstat(net[m24]), y24_n=int(m24.sum()),
                drop10=srt[:-10].mean(), drop10_t=tstat(srt[:-10]), maxdd=dd, worst=net.min(), worst_date=str(idx[np.argmin(net)].date()),
                long=net[T["dir"].values > 0].mean(), short=net[T["dir"].values < 0].mean(), n_long=int((T["dir"] > 0).sum()),
                p5=np.percentile(net, 5), sd=net.std(ddof=1),
                by_year={int(k): round(v, 0) for k, v in pd.Series(net, index=idx).groupby(idx.year).mean().items()})
