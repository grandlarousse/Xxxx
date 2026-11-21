"""Asama 2: ham Yahoo JSON -> genis panel (pickle) + evren.csv + veri_kalite.csv
Kullanim: python3 -I panel_kur.py <ham_dizin> <panel_dizin> <veri_dizin>
"""
import sys, os, json, urllib.parse, datetime as dt
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evren_tanim import KODLAR, KALDIRAC, sinif, tur, YENI_KOD

ham, pdir, vdir = sys.argv[1:4]
os.makedirs(pdir, exist_ok=True); os.makedirs(vdir, exist_ok=True)
BAS, SON = pd.Timestamp("2005-01-03"), pd.Timestamp("2026-11-20")
ALAN = ["open", "high", "low", "close", "adjclose", "volume"]

def oku(k):
    f = os.path.join(ham, urllib.parse.quote(k, safe="") + ".json")
    if not os.path.exists(f): return None, None
    r = json.load(open(f))["chart"]["result"][0]
    if not r.get("timestamp"): return None, None
    tz = r["meta"].get("exchangeTimezoneName", "UTC")
    q = r["indicators"]["quote"][0]
    d = pd.DataFrame({a: q.get(a) for a in ["open", "high", "low", "close", "volume"]})
    d["adjclose"] = r["indicators"].get("adjclose", [{}])[0].get("adjclose", d["close"])
    # tarih = borsanin yerel takvim tarihi
    d.index = pd.to_datetime(r["timestamp"], unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
    d = d.apply(pd.to_numeric, errors="coerce")
    d = d[d["close"].notna()]                      # null gunleri at
    d = d[~d.index.duplicated(keep="last")].sort_index()
    ev = r.get("events", {})
    bol = {pd.Timestamp(dt.datetime.fromtimestamp(int(t), dt.timezone.utc).astimezone(__import__("zoneinfo").ZoneInfo(tz)).date()):
           f"{v['numerator']:g}:{v['denominator']:g}" for t, v in ev.get("splits", {}).items()}
    tem = {pd.Timestamp(dt.datetime.fromtimestamp(int(t), dt.timezone.utc).astimezone(__import__("zoneinfo").ZoneInfo(tz)).date()):
           v["amount"] for t, v in ev.get("dividends", {}).items()}
    return d, {"bol": bol, "tem": tem, "tz": tz, "meta": r["meta"]}

spy, _ = oku("SPY")
takvim = spy.index[(spy.index >= BAS) & (spy.index <= SON)]
seri, olay, yok = {}, {}, []
kodlar = []
for k, g in KODLAR:
    kk = YENI_KOD.get(k, k)
    d, e = oku(kk)
    if d is None: yok.append(k); continue
    seri[kk], olay[kk] = d, e; kodlar.append((kk, g, k))

P = {a: pd.DataFrame({k: seri[k][a].reindex(takvim) for k, _, _ in kodlar}, index=takvim) for a in ALAN}
for a in ALAN:
    P[a].index.name = "tarih"
    P[a].to_pickle(os.path.join(pdir, f"{a}.pkl"))

# ---- evren.csv
sat = []
for k, g, eski in kodlar:
    d = seri[k]; c = P["close"][k]; v = P["volume"][k]
    t = tur(k, g)
    son60 = (c * v).dropna().iloc[-60:]
    adv = float(son60.mean()) if len(son60) else np.nan
    lev, day = KALDIRAC.get(k, (1, ""))
    notlar = []
    if eski != k: notlar.append(f"eski kod {eski}")
    if t in ("endeks", "doviz"):
        mal = np.nan; notlar.append("dogrudan islem gormez/hacim anlamsiz; maliyet yok")
        adv = np.nan if t == "doviz" or (v.fillna(0) == 0).all() else adv
    else:
        mal = 1.5 if adv > 1e9 else 3 if adv > 2e8 else 7 if adv > 5e7 else 15
        if lev != 1: mal += 1
        if t == "vadeli": notlar.append("adv = fiyat x kontrat (carpan yok), yaklasik")
        if t == "kripto": notlar.append("Yahoo kripto hacmi USD, 7/24 piyasa; panelde yalniz NYSE gunleri")
    sat.append(dict(kod=k, grup=g, tur=t, kapanis_sinifi=sinif(k), ilk_tarih=d.index[0].date(), son_tarih=d.index[-1].date(),
                    gun_sayisi=int(c.notna().sum()), adv60_usd=round(adv) if adv == adv else np.nan, maliyet_bps=mal,
                    kaldirac=lev, dayanak=day, borsa_tz=olay[k]["tz"], **{"not": "; ".join(notlar)}))
ev = pd.DataFrame(sat)
ev.to_csv(os.path.join(vdir, "evren.csv"), index=False)

# ---- veri_kalite.csv
kal = []
for k, g, _ in kodlar:
    d = seri[k]; e = olay[k]; c = P["close"][k]
    ilk = c.first_valid_index()
    eksik = int(c.loc[ilk:].isna().sum()) if ilk is not None else -1
    eksik_tarih = c.loc[ilk:][c.loc[ilk:].isna()].index
    r = d["close"].pct_change()                     # kendi takviminde ardisik gozlem
    buy = r[r.abs() > 0.40]
    buyl = []
    for t_, x in buy.items():
        b = [s for s, o in e["bol"].items() if abs((s - t_).days) <= 3]
        buyl.append(f"{t_.date()}({x:+.0%}{',BOLUNME ' + e['bol'][b[0]] if b else ''})")
    # adjclose/close orani: temettu disi sicrama
    oran = (d["adjclose"] / d["close"])
    dor = oran / oran.shift(1) - 1
    bek = pd.Series(0.0, index=d.index)
    for t_, amt in e["tem"].items():
        if t_ in d.index:
            i = d.index.get_loc(t_)
            if i > 0: bek.iloc[i] = amt / d["close"].iloc[i - 1]
    sap = (dor - bek).abs()
    sic = sap[sap > 0.005].index
    sicl = [f"{t_.date()}({dor[t_]:+.2%})" for t_ in sic[:8]]
    sifir = int((d.loc[d.index >= BAS, "volume"].fillna(0) == 0).sum())
    ohlc = int(((d["high"] < d[["open", "close"]].max(axis=1) * 0.999) | (d["low"] > d[["open", "close"]].min(axis=1) * 1.001)).sum())
    kal.append(dict(kod=k, ilk_tarih=d.index[0].date(), son_tarih=d.index[-1].date(), son_tarih_tamam=d.index[-1] >= SON,
                    eksik_gun_spy_takvimi=eksik,
                    eksik_ornek=",".join(str(x.date()) for x in eksik_tarih[-5:]),
                    buyuk_getiri_n=len(buy), buyuk_getiri_gunleri=" ".join(buyl[:12]),
                    bolunmeler=" ".join(f"{s.date()}:{v}" for s, v in sorted(e["bol"].items())),
                    adj_oran_sicrama_n=len(sic), adj_oran_sicrama_ornek=" ".join(sicl),
                    sifir_hacim_gun=sifir, ohlc_tutarsiz_gun=ohlc))
kq = pd.DataFrame(kal)
kq.to_csv(os.path.join(vdir, "veri_kalite.csv"), index=False)
json.dump({"gelmeyen": yok}, open(os.path.join(pdir, "_gelmeyen.json"), "w"))
print("kod:", len(kodlar), "gelmeyen:", yok, "takvim:", takvim[0].date(), takvim[-1].date(), len(takvim))
