"""Pratik kural kütüphanesi (rehber/altin). Araştırma kütüphanesi cl/ev'i KULLANIR (aynı tanımlar), panele 02-03.11.2026 bültenlerini ekler.
Ortak veri dosyalarına yazmaz; kendi indirmeleri rehber/altin/veri altında."""
import sys, os, glob
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
R = S + "/out/rehber/altin"
sys.path.insert(0, S + "/out/code_k_dis-suruculer_curut")
import numpy as np, pandas as pd, importlib.util
import cl, ev

def _parse_new():
    spec = importlib.util.spec_from_file_location("vp", S + "/out/code_y_viop/02_parse.py"); vp = importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)
    fs = sorted(glob.glob(R + "/veri/viop/viop_????????.csv"))
    F = pd.concat([vp.parse(f)[0] for f in fs], ignore_index=True)
    F["date"] = pd.to_datetime(F["date"]).dt.normalize(); F["expiry"] = pd.to_datetime(F["expiry"], errors="coerce").dt.normalize()
    F["und"] = F["und_raw"].map(vp.und_std)
    return F

def install_panel(extend=True):
    """cl.panel()'i 02-03.11 bültenleriyle genişletilmiş panelle değiştirir (cl önbelleklerini sıfırlar)."""
    cols = ["date", "code", "und", "expiry", "settle", "prev_settle", "close", "vwap", "value_tl", "trades", "oi", "high", "low", "qty"]
    p = pd.read_parquet(S + "/data/viop_panel.parquet", columns=cols)
    p["code"] = p["code"].astype(str); p["und"] = p["und"].astype(str)
    p["date"] = pd.DatetimeIndex(p["date"]).normalize(); p["expiry"] = pd.DatetimeIndex(p["expiry"]).normalize()
    if extend:
        F = _parse_new(); F = F[F["code"].str.startswith("F_")]
        F = F[[c for c in cols if c in F.columns]]
        F = F[F["date"] > p["date"].max()]
        p = pd.concat([p, F], ignore_index=True)
    cl._P = p; cl._CAL = None; cl._FR.clear(); ev._R.clear()
    return p

def ydaily(sym):
    d = pd.read_parquet(f"{R}/veri/daily/{sym}.parquet")
    d.index = pd.DatetimeIndex(pd.to_datetime(d["ldate"])).normalize(); d = d[~d.index.duplicated(keep="last")].sort_index()
    return d

def intraday(sym, kind):
    """kendi indirmemiz + ortak veri (eski kısmı doldurmak için) birleşik; index = bar başlangıcı UTC."""
    fs = [f"{R}/veri/{kind}/{sym}.parquet", f"{S}/data/{kind}/{sym}.parquet"]
    ds = [pd.read_parquet(f) for f in fs if os.path.exists(f)]
    d = pd.concat(ds[::-1]); d = d[~d.index.duplicated(keep="last")].sort_index()
    step = pd.Timedelta(minutes=60 if kind == "h1" else 5)
    d = d[(d.index.second == 0) & (d.index.minute % (60 if kind == "h1" else 5) == 0)]   # Yahoo'nun eklediği canlı (düzensiz) satırı at
    return d, step

def snap(sym, kind, hh, mm, max_age_min=90):
    """BIST günü t için hh:mm UTC'de BİLİNEN son fiyat = bitişi (başlangıç+adım) <= hh:mm olan son barın kapanışı."""
    d, step = intraday(sym, kind)
    s = pd.Series(d["c"].values, index=(d.index + step).tz_convert(None)); s = s[s > 0]
    c = cl.cal(); tg = c + pd.Timedelta(hours=hh, minutes=mm)
    pos = np.searchsorted(s.index.values, tg.values, side="right") - 1
    ok = pos >= 0
    v = np.where(ok, s.values[np.clip(pos, 0, None)], np.nan)
    age = (tg.values - s.index.values[np.clip(pos, 0, None)]) / np.timedelta64(1, "m")
    v = np.where(ok & (age <= max_age_min), v, np.nan)
    out = pd.Series(v, index=c)
    out[out.index < s.index[0].normalize() + pd.Timedelta(days=1)] = np.nan
    return out

def snap_ret(px, allow_gap=False):
    """BIST takviminde: ln(P_t / P_{t-1}) (t-1 = önceki BIST günü; VİOP uzlaşma/önceki uzlaşma mantığı). Biri yoksa NaN.
    allow_gap=True: önceki BIST günü yoksa son geçerli güne göre."""
    last = px.ffill().shift(1) if allow_gap else px.shift(1)
    return np.log(px / last)

def front_codes(und, min_td=3):
    f = cl.front(und, min_td)
    return f["code"].reindex(cl.cal())

def settle_of(code_series, und):
    """her gün için verilen kontrat kodunun uzlaşma fiyatı tablosu (date x code -> settle) ile erişim fonksiyonu."""
    p = cl.panel(); x = p[p["und"] == und][["date", "code", "settle"]]
    return x.set_index(["date", "code"])["settle"]

def sigma_hedged(und="TRALT"):
    L = ev.legs(und); return L["hedged"]

# ---------------------------------------------------------------- pratik backtest yardımcıları
def yahoo_roll_fix(r, g0, months=(1, 3, 5, 7, 11), tail=6, head=2, thr=0.0025):
    """Yahoo GC=F sürekli kontratı ay sonlarında (FND'den 1-3 iş günü önce) yeni kontrata geçer -> +%0,3..2 sıçrama.
    Pencere: ilgili ayların son `tail` + sonraki ayın ilk `head` BIST günü; pencerede (r - g0) en büyük gün > thr ise
    o günün değişimi VİOP uzlaşma değişimiyle değiştirilir (zamanlama farkı o gün 0 varsayılır). Dönüş: (düzeltilmiş r, bayrak günleri)."""
    r = r.copy(); c = r.index; flags = []
    ym = pd.Series(c.year * 100 + c.month, index=c)
    for key in sorted(ym.unique()):
        if key % 100 not in months: continue
        days = ym.index[ym == key]
        nxt = ym.index[ym > key][:head]
        win = days[-tail:].append(nxt)
        d = (r.reindex(win) - g0.reindex(win)).dropna()
        if len(d) and d.max() > thr:
            k = d.idxmax(); flags.append((k, round(d.max() * 1e4, 1))); r.loc[k] = g0.loc[k]
    return r, flags

_CR = {}
def code_ret(und):
    """(tarih x kontrat) günlük ln(uzlaşma/önceki uzlaşma) — aynı kontrat, bedelsiz/temettü düzeltmeli önceki uzlaşma."""
    if und in _CR: return _CR[und]
    P = cl.panel(); x = P[(P["und"] == und) & (P["settle"] > 0) & (P["prev_settle"] > 0)].copy()
    x["r"] = np.log(x["settle"] / x["prev_settle"])
    t = x.pivot_table(index="date", columns="code", values="r", aggfunc="last").reindex(cl.cal())
    s = x.pivot_table(index="date", columns="code", values="settle", aggfunc="last").reindex(cl.cal())
    _CR[und] = (t, s); return t, s

def same_contract_fwd(und, h, min_td=3):
    """t'de seçilen ön vade kontratı (vadeye >= min_td iş günü) ile t uzlaşması -> t+h uzlaşması getirisi (aynı kontrat)."""
    t, s = code_ret(und); c = cl.cal(); codes = cl.front(und, min_td)["code"].reindex(c)
    tv = t.values; cols = {k: i for i, k in enumerate(t.columns)}
    out = np.full(len(c), np.nan); px = np.full(len(c), np.nan)
    for i in range(len(c) - h):
        cd = codes.iloc[i]
        if not isinstance(cd, str) or cd not in cols: continue
        j = cols[cd]; seg = tv[i + 1:i + h + 1, j]
        if np.all(np.isfinite(seg)): out[i] = seg.sum()
        px[i] = s.values[i, j]
    return pd.Series(out, index=c), codes, pd.Series(px, index=c)

def spot_beta(sym="TRALT.IS", mkt="XU030.IS"):
    a = ydaily(sym); b = ydaily(mkt)
    def lr(d):
        st = (d["v"].fillna(0) <= 0) & (d["h"] == d["l"]); d = d[~st]; return np.log(d["adj"].where(d["adj"] > 0)).diff()
    c = cl.cal(); ra = lr(a).reindex(c); rb = lr(b).reindex(c)
    return cl.roll_beta(ra, rb, 250, 100)

def limit_flags(sym="TRALT.IS"):
    """Spot tavan/taban kapanışı: |getiri| >= limit-%0,5 ve kapanış = gün yükseği/düşüğü."""
    d = ydaily(sym); r = np.log(d["c"] / d["c"].shift(1))
    lim = np.where(d.index < cl.REGIME, np.log(1.195), np.log(1.095))
    up = (r >= lim) & (d["c"] >= d["h"] - 1e-9); dn = (r <= -lim) & (d["c"] <= d["l"] + 1e-9)
    f = pd.Series(np.where(up, 1, np.where(dn, -1, 0)), index=d.index).reindex(cl.cal()).fillna(0)
    return f

def run_trades(z, y, h=2, thr=1.0, skip=None, ext=None):
    """cl.trades ile aynı örtüşmesiz mantık (+ isteğe bağlı giriş atlama bayrağı). y: t->t+h getiri. Dönüş DataFrame."""
    zz = z.reindex(y.index).values; yy = y.values; n = len(yy)
    sk = skip.reindex(y.index).fillna(False).values if skip is not None else np.zeros(n, bool)
    rows = []; i = 0
    while i < n:
        if np.isfinite(zz[i]) and np.isfinite(yy[i]) and abs(zz[i]) > thr and not sk[i]:
            d = np.sign(zz[i]); rows.append((y.index[i], d, d * yy[i], zz[i])); i += h
        else:
            i += 1
    return pd.DataFrame(rows, columns=["date", "dir", "gross", "z"]).set_index("date")

def stats(tr, cost_bps, split="2022-01-01", per=None):
    """cost_bps: sabit sayı ya da işlem bazında Series (bps)."""
    if len(tr) < 3: return dict(n=len(tr))
    cst = cost_bps.reindex(tr.index).values if isinstance(cost_bps, pd.Series) else cost_bps
    g = tr["gross"].values * 1e4; net = g - cst; idx = tr.index
    yrs = max((idx[-1] - idx[0]).days / 365.25, 0.25)
    isd = idx < pd.Timestamp(split)
    cum = np.cumsum(net); dd = (cum - np.maximum.accumulate(np.r_[0, cum])[1:]).min()
    o = dict(n=len(tr), per_yr=round(len(tr) / yrs, 1), gross=round(g.mean(), 1), net=round(net.mean(), 1), t=round(cl.tstat(net), 2),
             hit=round((net > 0).mean(), 3), IS=round(net[isd].mean(), 1) if isd.sum() >= 3 else np.nan, IS_t=round(cl.tstat(net[isd]), 2) if isd.sum() >= 5 else np.nan, IS_n=int(isd.sum()),
             OOS=round(net[~isd].mean(), 1) if (~isd).sum() >= 3 else np.nan, OOS_t=round(cl.tstat(net[~isd]), 2) if (~isd).sum() >= 5 else np.nan, OOS_n=int((~isd).sum()),
             maxdd_bps=round(dd, 0), worst=round(net.min(), 0), worst_date=str(idx[np.argmin(net)].date()), best=round(net.max(), 0),
             sum_bps=round(net.sum(), 0))
    m24 = idx >= "2024-01-01"
    o["y2024_26"] = (round(net[m24].mean(), 1), round(cl.tstat(net[m24]), 2) if m24.sum() >= 5 else np.nan, int(m24.sum()))
    k = 10; srt = np.sort(net)
    o["drop_top10"] = (round(srt[:-k].mean(), 1), round(cl.tstat(srt[:-k]), 2)) if len(net) > k + 5 else None
    o["by_year"] = pd.Series(net, index=idx).groupby(idx.year).agg(lambda v: f"{v.mean():+.0f}({len(v)})").to_dict()
    return o

def fut_lock_flags(und="TRALT", min_td=3, thr=0.09):
    """Vadeli (ön vade) kilit: uzlaşma değişimi >= +%9 ve kapanış = gün yükseği -> +1 (tavan kilidi); <= -%9 ve kapanış = gün düşüğü -> -1."""
    P = cl.panel(); f = cl.front(und, min_td); c = cl.cal()
    x = P[P["und"] == und].set_index(["date", "code"])[["high", "low", "close", "settle"]]
    k = list(zip(f.index, f["code"]))
    hh = x.reindex(k); hh.index = f.index
    r = f["ret"]
    up = (r >= np.log(1 + thr)) & (hh["close"] >= hh["high"] - 1e-9)
    dn = (r <= np.log(1 - thr)) & (hh["close"] <= hh["low"] + 1e-9)
    return pd.Series(np.where(up, 1, np.where(dn, -1, 0)), index=f.index).reindex(c).fillna(0)

def roll_window_mask(idx, months=(1, 3, 5, 7, 11), tail=6, head=2):
    """Yahoo GC=F'nin vade geçişi yapabileceği günler (ilgili ayların son `tail` + sonraki ayın ilk `head` BIST günü)."""
    s = pd.Series(idx.year * 100 + idx.month, index=idx); m = pd.Series(False, index=idx)
    for key in sorted(s.unique()):
        if key % 100 not in months: continue
        days = s.index[s == key]; nxt = s.index[s > key][:head]
        m.loc[days[-tail:]] = True; m.loc[nxt] = True
    return m
