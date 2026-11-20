"""snap.parquet: gün x sembol, gün içi belirli saatlerde BİLİNEN son fiyat (uzun biçim).
Sütunlar: date, sym, p_open, p_1630, p_1700, p_1730, p_1750, p_son, p_close, kaynak, bar_1700, bar_1750, bar_son, yahoo_carpan
  FİYAT BAZI: hisselerde bütün p_* sütunları HAM (o gün tahtada görülen) fiyattır. p_close/p_open = D1'in px.parquet c_raw/o_raw sütunları.
  Yahoo gün içi barları geçmişe dönük kısmen bölünme düzeltmeli olduğundan gün içi fiyatlar yahoo_carpan'a bölünerek ham baza çevrildi
  (h1/ ve m5/ dosyaları Yahoo'nun verdiği gibidir: ham = bar fiyatı / yahoo_carpan). Gün içi oranlar (p_1750/p_close vb.) bu yüzden tutarlıdır.
  p_close = günün resmi kapanışı (kapanış seansı fiyatı). Endeks: İş Yatırım'ın günün son (18:00 damgalı) değeri.
  p_open  = hisse: D1 o_raw; endeks: Yahoo günlük 'open' (XU030, XU100; XELKT için yok -> NaN).
  p_1630 / p_1730 = 16:30 / 17:30 TSİ'de bilinen son fiyat. Hisse: Yahoo saatlik barlar :30'da başlar; 15:30 barının kapanışı = 16:30 fiyatı,
            16:30 barının kapanışı = 17:30 fiyatı (bar yoksa en yakın önceki bar). Endeks: İş Yatırım 5 dk (16:25 ve 17:25 barları).
  p_1700 / p_1750 = 17:00 / 17:50 TSİ'de bilinen son fiyat.
            kaynak='m5'  : Yahoo 5 dk (son ~60 gün): 16:55 ve 17:45 barlarının kapanışı (tam).
            kaynak='h1'  : 5 dk yok -> saatlik veride en yakın ÖNCEKİ tamamlanmış bar: p_1700 = p_1630, p_1750 = p_1730 (30 ve 20 dk bayat).
            kaynak='isy_m5': endeks, İş Yatırım 5 dk: 16:55 ve 17:45 barları (tam; 2017'den beri).
            kaynak='isy_h1': endeks, o gün 5 dk verisi eksik -> İş Yatırım saatlik: p_1700 = 16:00 barı (tam), p_1750 = yine 16:00 barı (50 dk bayat).
  bar_1700 / bar_1750 / bar_son = kullanılan barın BAŞLANGIÇ saati (TSİ, HH:MM).
  p_son   = sürekli işlemin son fiyatı (hisse: 17:30 saatlik barının ya da 17:55 5 dk barının kapanışı; yoksa NaN. Endeks: 17:55 barı).
Kullanım: python3 -I 05_snap.py"""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, FULL, STOCKS, ISY_IDX

def ydaily(sym):
    fn = f"{RAW}/yahoo/d/{sym}.json"
    if not os.path.exists(fn): return pd.DataFrame(columns=["p_open", "p_close"])
    res = json.load(open(fn))["chart"]["result"][0]; q = res["indicators"]["quote"][0]
    d = pd.DataFrame({"date": (pd.to_datetime(res["timestamp"], unit="s") + pd.Timedelta(hours=3)).normalize(), "p_open": q["open"], "p_close": q["close"]})
    return d.dropna(subset=["p_close"]).drop_duplicates("date", keep="last").set_index("date").astype(float)

def last_le(df, hm_max, exact=False):
    """Her gün için başlangıcı <= hm_max olan son barın kapanışı ve başlangıç saati."""
    x = df[df["hm"] == hm_max] if exact else df[df["hm"] <= hm_max]
    g = x.groupby("date").tail(1).set_index("date")
    return g["c"], g["ts_tr"].dt.strftime("%H:%M")

def prep(df):
    df = df.sort_values("ts_tr").copy(); df["date"] = df["ts_tr"].dt.normalize(); df["hm"] = df["ts_tr"].dt.hour * 60 + df["ts_tr"].dt.minute
    return df

def yahoo_carpan(last_bar, c_raw, ca_days=()):
    """Yahoo gün içi barları geçmişe dönük KISMEN bölünme/bedelsiz düzeltmeli (günlük ham kapanışla aynı bazda değil).
    k(t) = Yahoo gün içi fiyat bazı / ham (o gün işlem gören) fiyat bazı; parça parça sabittir, düzeltme günlerinde basamak yapar.
    Kestirim: lq = log(günün son saatlik bar kapanışı / ham resmi kapanış); 5 günlük sol/sağ medyan farkı > %4 olan yerel en büyük nokta = kırılma;
    her parçada k = exp(medyan lq); |k-1| < %0,7 ise k = 1. Sonra kırılma çevresindeki ±4 günde komşu parçanın çarpanı daha iyi uyuyorsa o alınır."""
    lq = np.log(last_bar / c_raw).dropna()
    if len(lq) < 3: return pd.Series(1.0, index=lq.index), []
    v = lq.values; n = len(v); d = np.zeros(n)
    for i in range(1, n):
        L = np.median(v[max(0, i - 5):i]); Rr = np.median(v[i:min(n, i + 5)]); d[i] = Rr - L
    brk = [i for i in range(1, n) if abs(d[i]) > 0.04 and abs(d[i]) >= np.abs(d[max(1, i - 5):min(n, i + 6)]).max() - 1e-12]
    # yanlış alarm süzgeci (ör. art arda tavan/taban günleri): kırılma ya büyük olmalı (>%12) ya da D1'in özsermaye hâli günlerine (ca_days) ±4 gün yakın
    near = lambda t: any(abs((t - c).days) <= 4 for c in ca_days)
    brk = [i for i in brk if abs(d[i]) > 0.12 or near(lq.index[i])]
    k = np.ones(n); edges = [0] + brk + [n]
    for a_, b_ in zip(edges[:-1], edges[1:]):
        if b_ > a_:
            m = float(np.exp(np.median(v[a_:b_]))); k[a_:b_] = 1.0 if abs(m - 1) < 0.007 else m
    # sınır inceltme: kırılma çevresindeki günlerde (Yahoo geçişi 1-2 gün kaydırabiliyor) komşu parçanın çarpanı belirgin daha iyi uyuyorsa onu kullan
    segk = sorted(set(np.round(k, 10)))
    if len(segk) > 1:
        for i in range(n):
            if abs(v[i] - np.log(k[i])) > 0.06:
                lo, hi = max(0, i - 4), min(n, i + 5); cand = set(np.round(k[lo:hi], 10))
                best = min(cand, key=lambda c: abs(v[i] - np.log(c)))
                if abs(v[i] - np.log(best)) < 0.06: k[i] = best
    return pd.Series(k, index=lq.index), [lq.index[i] for i in brk]

def stock(sym, PX, CA=None):
    h = prep(pd.read_parquet(f"{FULL}/h1/{sym}.parquet"))
    out = pd.DataFrame(index=pd.DatetimeIndex(sorted(h["date"].unique()), name="date"))
    out["p_1630"], b1630 = last_le(h, 15 * 60 + 30)
    out["p_1730"], b1730 = last_le(h, 16 * 60 + 30)
    out["p_son"], bson = last_le(h, 17 * 60 + 30, exact=True)
    out["p_1700"], out["p_1750"], out["kaynak"], out["bar_1700"], out["bar_1750"], out["bar_son"] = out["p_1630"], out["p_1730"], "h1", b1630, b1730, bson
    p5 = f"{FULL}/m5/{sym}.parquet"
    if os.path.exists(p5):
        m = prep(pd.read_parquet(p5))
        a, ba = last_le(m, 16 * 60 + 55); b, bb = last_le(m, 17 * 60 + 45); s, bs = last_le(m, 17 * 60 + 55, exact=True)
        idx = out.index.intersection(a.index)
        out.loc[idx, "p_1700"] = a[idx]; out.loc[idx, "bar_1700"] = ba[idx]; out.loc[idx, "kaynak"] = "m5"
        idx2 = idx.intersection(b.index); out.loc[idx2, "p_1750"] = b[idx2]; out.loc[idx2, "bar_1750"] = bb[idx2]
        idx3 = idx.intersection(s.index); out.loc[idx3, "p_son"] = s[idx3]; out.loc[idx3, "bar_son"] = bs[idx3]
    lastbar = h.groupby("date").tail(1).set_index("date")["c"]
    if PX is not None and sym in PX.index.get_level_values(0):
        d = PX.loc[sym]; out["p_close"] = d["c_raw"].reindex(out.index); out["p_open"] = d["o_raw"].reindex(out.index)
        ca_days = list(CA.index[CA[sym].fillna(0).astype(float) != 0]) if CA is not None and sym in CA else []
        k, brk = yahoo_carpan(lastbar.reindex(out.index), out["p_close"], ca_days)
        out["yahoo_carpan"] = k.reindex(out.index).ffill().bfill().fillna(1.0)
        for c in ("p_1630", "p_1700", "p_1730", "p_1750", "p_son"): out[c] = out[c] / out["yahoo_carpan"]
    else:   # D1 paneli yoksa: Yahoo günlük (bölünme düzeltmeli) kapanış; çarpan kestirilemez
        out = out.join(ydaily(sym), how="left"); out["yahoo_carpan"] = np.nan; brk = []
    return out, brk

def _isy(kind, code):
    fn = f"{RAW}/isy/{kind}/{code}.parquet"
    if not os.path.exists(fn): return None
    m = pd.read_parquet(fn); m["ts_tr"] = m["ts_utc"] + pd.Timedelta(hours=3); m = prep(m)
    return m[m["hm"] <= 18 * 60 + 15]

def index_isy(code):
    """Endeks: önce İş Yatırım 5 dk (kaynak='isy_m5'). O gün 5 dk verisi yok/eksikse (bar sayısı < XELKT'nin o günkü 5 dk bar sayısının %80'i)
    İş Yatırım saatlik (kaynak='isy_h1'): p_1700 = 16:00 barı (16:00-17:00'nin son değeri, tam); p_1750 = yine 16:00 barı (50 dk bayat);
    p_son = 17:00 barı; p_close = 18:00 barı. p_1630/p_1730 bu durumda Yahoo saatlik XU030/XU100 barlarından (varsa) alınır."""
    h = _isy("h1", code); m = _isy("m5", code); ref = _isy("m5", "XELKT")
    out = pd.DataFrame(index=pd.DatetimeIndex(sorted(h["date"].unique()), name="date"))
    out["p_1700"], out["bar_1700"] = last_le(h, 16 * 60); out["p_1750"], out["bar_1750"] = out["p_1700"], out["bar_1700"]
    out["p_son"], out["bar_son"] = last_le(h, 17 * 60, exact=True)
    out["p_close_isy"] = h.groupby("date").tail(1).set_index("date")["c"]; out["kaynak"] = "isy_h1"; out["p_1630"] = np.nan; out["p_1730"] = np.nan
    yh = f"{FULL}/h1/{code}.parquet"
    if os.path.exists(yh):
        y = prep(pd.read_parquet(yh)); a, _ = last_le(y, 15 * 60 + 30); b, _ = last_le(y, 16 * 60 + 30)
        out["p_1630"] = a.reindex(out.index); out["p_1730"] = b.reindex(out.index)
    if m is not None:
        n = m.groupby("date").size(); nref = ref.groupby("date").size().reindex(n.index)
        ok = n.index[(n >= 0.8 * nref.fillna(n.median())) & (m.groupby("date")["hm"].max().reindex(n.index) >= h.groupby("date")["hm"].max().reindex(n.index).fillna(0))]
        ok = ok.intersection(out.index); m = m[m["date"].isin(ok)]
        for col, hm, bar in (("p_1630", 16 * 60 + 25, None), ("p_1730", 17 * 60 + 25, None), ("p_1700", 16 * 60 + 55, "bar_1700"), ("p_1750", 17 * 60 + 45, "bar_1750")):
            v, bb = last_le(m, hm); out.loc[v.index, col] = v
            if bar: out.loc[v.index, bar] = bb
        v, bb = last_le(m, 17 * 60 + 55, exact=True); out.loc[ok, "p_son"] = v.reindex(ok); out.loc[ok, "bar_son"] = bb.reindex(ok)
        out.loc[ok, "p_close_isy"] = m.groupby("date").tail(1).set_index("date")["c"].reindex(ok); out.loc[ok, "kaynak"] = "isy_m5"
    yd = ydaily(code); out = out.join(yd.rename(columns={"p_close": "p_close_yahoo"}), how="left")
    out["p_close"] = out["p_close_isy"]
    return out

def export_isy():
    """İş Yatırım endeks serilerini panele yazar: panel_full/h1_isy/<KOD>.parquet ve m5_isy/<KOD>.parquet (ts_utc, ts_tr, c).
    Damga = bar BAŞLANGICI; c = o aralıktaki son endeks değeri; 18:00 TSİ damgalı değer = kapanış seansı sonrası resmi kapanış."""
    for kind in ("h1", "m5"):
        os.makedirs(f"{FULL}/{kind}_isy", exist_ok=True)
        for code in ISY_IDX:
            fn = f"{RAW}/isy/{kind}/{code}.parquet"
            if not os.path.exists(fn): print("YOK", fn); continue
            x = pd.read_parquet(fn).sort_values("ts_utc"); x.insert(1, "ts_tr", x["ts_utc"] + pd.Timedelta(hours=3))
            x.reset_index(drop=True).to_parquet(f"{FULL}/{kind}_isy/{code}.parquet", index=False)

if __name__ == "__main__":
    export_isy()
    parts = []; kir = []
    pxf = f"{FULL}/px.parquet"   # D1 çıktısı: ham (o gün işlem gören) açılış/kapanış
    PX = pd.read_parquet(pxf, columns=["date", "sym", "c_raw", "o_raw"]).set_index(["sym", "date"]).sort_index() if os.path.exists(pxf) else None
    CA = pd.read_parquet(f"{FULL}/ca_day.parquet") if os.path.exists(f"{FULL}/ca_day.parquet") else None   # D1: özsermaye hâli günleri
    if PX is None: print("UYARI: px.parquet yok -> p_close Yahoo günlük, ham baza çevirme yapılmadı")
    for s in STOCKS:
        o, brk = stock(s, PX, CA); parts.append(o.assign(sym=s)); kir += [(s, str(b.date()), round(float(o.loc[b, "yahoo_carpan"]), 4)) for b in brk]
    pd.DataFrame(kir, columns=["sym", "date", "yeni_carpan"]).to_csv(f"{RAW}/yahoo_carpan_kirilmalar.csv", index=False)
    print("yahoo_carpan kırılma sayısı", len(kir), kir[:12])
    for c in ISY_IDX: parts.append(index_isy(c).assign(sym=c))
    S = pd.concat(parts).reset_index()
    cols = ["date", "sym", "p_open", "p_1630", "p_1700", "p_1730", "p_1750", "p_son", "p_close", "kaynak", "bar_1700", "bar_1750", "bar_son", "yahoo_carpan"]
    aux = S[["date", "sym", "p_close_isy", "p_close_yahoo"]].dropna(subset=["p_close_isy"])
    aux.to_parquet(f"{RAW}/snap_endeks_kapanis_kontrol.parquet", index=False)
    S = S[cols].sort_values(["date", "sym"]).reset_index(drop=True)
    S.to_parquet(f"{FULL}/snap.parquet", index=False)
    print(S.groupby("kaynak").agg(n=("sym", "size"), sym=("sym", "nunique"), ilk=("date", "min"), son=("date", "max")).to_string())
    print(S[cols[2:9]].isna().mean().round(4).to_string())
