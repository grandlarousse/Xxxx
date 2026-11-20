"""snap.parquet: gün x sembol, gün içi belirli saatlerde BİLİNEN son fiyat (uzun biçim).
Sütunlar: date, sym, p_open, p_1630, p_1700, p_1730, p_1750, p_son, p_close, kaynak, bar_1700, bar_1750, bar_son
  p_close = günün resmi kapanışı (kapanış seansı fiyatı). Hisse: Yahoo günlük 'close'. Endeks (İş Yatırım): 18:00 damgalı 5 dk değeri.
  p_open  = Yahoo günlük 'open' (XELKT dahil; yoksa NaN).
  p_1630 / p_1730 = 16:30 / 17:30 TSİ'de bilinen son fiyat. Hisse: Yahoo saatlik barlar :30'da başlar; 15:30 barının kapanışı = 16:30 fiyatı,
            16:30 barının kapanışı = 17:30 fiyatı (bar yoksa en yakın önceki bar). Endeks: İş Yatırım 5 dk (16:25 ve 17:25 barları).
  p_1700 / p_1750 = 17:00 / 17:50 TSİ'de bilinen son fiyat.
            kaynak='m5'  : Yahoo 5 dk (son ~60 gün): 16:55 ve 17:45 barlarının kapanışı (tam).
            kaynak='h1'  : 5 dk yok -> saatlik veride en yakın ÖNCEKİ tamamlanmış bar: p_1700 = p_1630, p_1750 = p_1730 (30 ve 20 dk bayat).
            kaynak='isy_m5': endeks, İş Yatırım 5 dk: 16:55 ve 17:45 barları (tam; 2017'den beri).
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

def stock(sym):
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
    out = out.join(ydaily(sym), how="left")
    return out

def index_isy(code):
    m = pd.read_parquet(f"{RAW}/isy/m5/{code}.parquet"); m["ts_tr"] = m["ts_utc"] + pd.Timedelta(hours=3); m = prep(m)
    m = m[m["hm"] <= 18 * 60 + 15]
    out = pd.DataFrame(index=pd.DatetimeIndex(sorted(m["date"].unique()), name="date"))
    out["p_1630"], _ = last_le(m, 16 * 60 + 25); out["p_1730"], _ = last_le(m, 17 * 60 + 25)
    out["p_1700"], out["bar_1700"] = last_le(m, 16 * 60 + 55); out["p_1750"], out["bar_1750"] = last_le(m, 17 * 60 + 45)
    out["p_son"], out["bar_son"] = last_le(m, 17 * 60 + 55, exact=True)
    cl = m.groupby("date").tail(1).set_index("date")   # günün son 5 dk değeri = kapanış seansı (normal gün 18:00; yarım gün 12:35/12:40)
    out["p_close_isy"] = cl["c"]; out["kaynak"] = "isy_m5"
    yd = ydaily(code); out = out.join(yd.rename(columns={"p_close": "p_close_yahoo"}), how="left")
    out["p_close"] = out["p_close_isy"]
    return out

if __name__ == "__main__":
    parts = []
    for s in STOCKS: parts.append(stock(s).assign(sym=s))
    for c in ISY_IDX: parts.append(index_isy(c).assign(sym=c))
    S = pd.concat(parts).reset_index()
    cols = ["date", "sym", "p_open", "p_1630", "p_1700", "p_1730", "p_1750", "p_son", "p_close", "kaynak", "bar_1700", "bar_1750", "bar_son"]
    aux = S[["date", "sym", "p_close_isy", "p_close_yahoo"]].dropna(subset=["p_close_isy"])
    aux.to_parquet(f"{RAW}/snap_endeks_kapanis_kontrol.parquet", index=False)
    S = S[cols].sort_values(["date", "sym"]).reset_index(drop=True)
    S.to_parquet(f"{FULL}/snap.parquet", index=False)
    print(S.groupby("kaynak").agg(n=("sym", "size"), sym=("sym", "nunique"), ilk=("date", "min"), son=("date", "max")).to_string())
    print(S[cols[2:9]].isna().mean().round(4).to_string())
