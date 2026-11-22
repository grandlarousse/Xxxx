"""Kripto 16:00 ET fiyati (15:00-16:00 ET saatlik mumunun kapanisi), her NYSE islem gunu.
Kaynak: Coinbase Exchange saatlik mum; Coinbase saatlik BTC 2015-07-20 basladigi icin oncesi (2015-01-02..2015-07-22) Bitstamp.
Kullanim: python3 -I kripto_1600.py <ham_dizin> <panel_dizin>"""
import sys, os, time, json, requests
import pandas as pd, numpy as np
ham, pdz = sys.argv[1], sys.argv[2]; os.makedirs(ham, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
def coinbase(urun, bas, son):
    yol = os.path.join(ham, f"cb_{urun}.pkl")
    if os.path.exists(yol): return pd.read_pickle(yol)
    parca, t = [], pd.Timestamp(bas, tz="UTC")
    son = pd.Timestamp(son, tz="UTC")
    while t < son:
        e = min(t + pd.Timedelta(hours=300), son)
        for i in range(5):
            try:
                r = requests.get(f"https://api.exchange.coinbase.com/products/{urun}/candles",
                                 params=dict(granularity=3600, start=t.isoformat(), end=e.isoformat()), headers=H, timeout=30)
                if r.status_code == 200: break
            except Exception: pass
            time.sleep(2 * (i + 1))
        else:
            raise RuntimeError(f"coinbase {urun} {t}")
        if r.json(): parca.append(np.array(r.json(), dtype=float))
        t = e; time.sleep(0.12)
    a = np.vstack(parca)
    df = pd.DataFrame(a[:, 1:], index=pd.to_datetime(a[:, 0], unit="s", utc=True), columns=["low", "high", "open", "close", "volume"])
    df = df[~df.index.duplicated()].sort_index(); df.to_pickle(yol); return df
def bitstamp(cift, bas, son):
    yol = os.path.join(ham, f"bs_{cift}.pkl")
    if os.path.exists(yol): return pd.read_pickle(yol)
    parca, t, son = int(pd.Timestamp(bas, tz="UTC").timestamp()), [], int(pd.Timestamp(son, tz="UTC").timestamp())
    parca, t = [], int(pd.Timestamp(bas, tz="UTC").timestamp())
    while t < son:
        r = requests.get(f"https://www.bitstamp.net/api/v2/ohlc/{cift}/", params=dict(step=3600, limit=1000, start=t), headers=H, timeout=30)
        v = r.json()["data"]["ohlc"]
        if not v: break
        parca += v; t = int(v[-1]["timestamp"]) + 3600; time.sleep(0.3)
    df = pd.DataFrame(parca).astype(float); df.index = pd.to_datetime(df.timestamp.astype(int), unit="s", utc=True)
    df = df[["low", "high", "open", "close", "volume"]]; df = df[df.index < pd.Timestamp(son, unit="s", tz="UTC")]
    df = df[~df.index.duplicated()].sort_index(); df.to_pickle(yol); return df
def fiyat_1600(mum, gunler):
    """gunler: NYSE gunleri. 16:00 ET hedefi; hedef-1s baslangicli mumun kapanisi, yoksa hedeften onceki son mum (<=3s)."""
    hedef = pd.DatetimeIndex([pd.Timestamp(d).tz_localize("America/New_York") + pd.Timedelta(hours=16) for d in gunler]).tz_convert("UTC")
    bas = hedef - pd.Timedelta(hours=1)
    c = mum.close
    tam = c.reindex(bas).to_numpy()
    pos = c.index.searchsorted(bas, side="right") - 1        # bas dahil, oncesindeki son mum (bas'tan once baslayan)
    ok = pos >= 0
    yedek = np.where(ok, c.to_numpy()[np.clip(pos, 0, None)], np.nan)
    yas = np.where(ok, (bas - c.index[np.clip(pos, 0, None)]).total_seconds() / 3600, np.nan)
    yedek = np.where(yas <= 3, yedek, np.nan)
    deger = np.where(np.isnan(tam), yedek, tam)
    return pd.Series(deger, index=pd.DatetimeIndex(gunler)), pd.Series(np.isnan(tam) & ~np.isnan(deger), index=pd.DatetimeIndex(gunler))
if __name__ == "__main__":
    gun = pd.read_pickle(os.path.join(pdz, "close.pkl")).index
    son = (pd.Timestamp(gun[-1]) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    cb = {"BTC-USD": coinbase("BTC-USD", "2015-01-20", son), "ETH-USD": coinbase("ETH-USD", "2016-05-15", son),
          "SOL-USD": coinbase("SOL-USD", "2021-05-20", son)}
    bs = bitstamp("btcusd", "2014-12-31", "2015-08-01")   # Coinbase saatlik BTC 2015-07-20 basliyor
    fiy, kay, yd = {}, {}, {}
    for k, m in cb.items():
        ilk = m.index[0]
        if k == "BTC-USD":       # Coinbase'in ilk gunleri ince; ilk 3 gun sonrasindan itibaren Coinbase, oncesi Bitstamp
            esik = ilk + pd.Timedelta(days=3)
            m2 = pd.concat([bs[bs.index < esik], m[m.index >= esik]])
        else:
            m2 = m
        s, y = fiyat_1600(m2, gun)
        g0 = {"BTC-USD": "2015-01-02", "ETH-USD": None, "SOL-USD": None}[k]
        g0 = pd.Timestamp(g0) if g0 else (ilk + pd.Timedelta(days=1)).normalize().tz_localize(None)
        s[s.index < g0] = np.nan; y[s.isna()] = False
        fiy[k], yd[k] = s, y
        kay[k] = pd.Series(np.where(s.index < (esik.tz_localize(None) if k == "BTC-USD" else g0), "bitstamp", "coinbase"), index=s.index).where(s.notna())
    F = pd.DataFrame(fiy); F.to_pickle(os.path.join(pdz, "kripto_1600.pkl"))
    pd.DataFrame(yd).to_pickle(os.path.join(pdz, "kripto_1600_yedek.pkl")); pd.DataFrame(kay).to_pickle(os.path.join(pdz, "kripto_1600_kaynak.pkl"))
    print(F.describe().T[["count"]].join(F.apply(lambda s: s.first_valid_index()).rename("ilk")).join(pd.DataFrame(yd).sum().rename("yedek_mum")))
