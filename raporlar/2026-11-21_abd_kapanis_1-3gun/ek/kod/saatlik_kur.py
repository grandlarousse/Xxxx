"""Yahoo 60m ham JSON -> gunluk tablolar (tarih x kod). Kullanim: python3 -I saatlik_kur.py <ham60_dizin> <panel_dizin>
saatlik_1530.pkl   : son tam saatlik cubugun acilisi = normal gunde 15:30 ET cubugunun open'i (kapanistan 30 dk once),
                     yarim gunde (13:00 kapanis) 12:30 cubugunun open'i. yarim_gun.pkl ile ayirt edin.
saatlik_kapanis.pkl: ayni gunun son cubugunun close'u (15:30-16:00 ya da 12:30-13:00 cubugu; resmi kapanis acik artirmasi degil, son islem).
saatlik_yarim_gun.pkl: tarih -> bool. Zaman damgalari UTC'den America/New_York'a cevrilir (yaz/kis saati zoneinfo ile).
Yarim gunde Yahoo 12:30 cubugunu bos, 12:30-13:00 verisini 13:00 etiketli hacimsiz cubukta veriyor: 12:30'a tasinir.
Son gunde 16:00 ET etiketli tek fiyatli (hacim 0) cubuk atilir."""
import sys, os, json, glob, urllib.parse
import pandas as pd, numpy as np
ham, pdz = sys.argv[1], sys.argv[2]
ac, kp, saat_say = {}, {}, {}
for p in sorted(glob.glob(os.path.join(ham, "*.json"))):
    if os.path.basename(p).startswith("_"): continue
    k = urllib.parse.unquote(os.path.basename(p)[:-5])
    r = json.load(open(p))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    df = pd.DataFrame({"open": q["open"], "close": q["close"], "volume": q["volume"]}, index=ts, dtype=float)
    df = df.dropna(subset=["open", "close"])
    # Yarim gunlerde Yahoo 12:30 cubugunu bos birakip 12:30-13:00 verisini 13:00 etiketli (hacim 0) cubuga koyuyor -> 12:30'a tasi
    yeni = df.index.where(~((df.index.hour == 13) & (df.index.minute == 0)), df.index - pd.Timedelta(minutes=30))
    df.index = yeni
    df = df[(df.index.minute == 30) & (df.index.hour >= 9) & (df.index.hour <= 15)]
    df = df[~df.index.duplicated(keep="first")]
    gun = df.index.tz_localize(None).normalize()
    g = df.groupby(gun)
    son = g.tail(1)
    son.index = son.index.tz_localize(None).normalize()
    ac[k], kp[k] = son.open, son.close
    saat_say[k] = pd.Series(g.apply(lambda x: x.index[-1].hour * 100 + x.index[-1].minute).values, index=son.index)
A, K, SS = pd.DataFrame(ac).sort_index(), pd.DataFrame(kp).sort_index(), pd.DataFrame(saat_say).sort_index()
# yarim gun: kodlarin cogunda son cubuk 12:30
yarim = (SS.eq(1230).sum(axis=1) > 0.5 * SS.notna().sum(axis=1))
# Son cubugu 15:30/12:30 olmayan (eksik son saat) hucreleri NaN yap: kapanistan 30 dk once tanimi bozulmasin
beklenen = np.where(yarim.to_numpy()[:, None], 1230, 1530)
bozuk = SS.notna() & SS.ne(pd.DataFrame(np.broadcast_to(beklenen, SS.shape), index=SS.index, columns=SS.columns))
A, K = A.mask(bozuk), K.mask(bozuk)
panel_gun = pd.read_pickle(os.path.join(pdz, "close.pkl")).index
fazla = A.index.difference(panel_gun)
A, K = A.reindex(panel_gun[panel_gun >= A.index[0]]), K.reindex(panel_gun[panel_gun >= A.index[0]])
yarim = yarim.reindex(A.index).fillna(False).astype(bool)
# Gunluk panelle uyumsuz donemler (saatlik son kapanis / gunluk close orani kontrolunden):
#  B: 2025-01-24'e kadar saatlik seri eski B'ye (Barnes Group) ait -> NaN.
#  GBTC: 2024-07-31 BTC mini trust dagitimi gunluk seride duzeltilmis, saatlikte degil -> o doneme gunluk/saatlik medyan oranla olcekle.
C = pd.read_pickle(os.path.join(pdz, "close.pkl")).reindex(index=K.index, columns=K.columns)
if "B" in A: A.loc[:"2025-01-24", "B"] = np.nan; K.loc[:"2025-01-24", "B"] = np.nan
if "GBTC" in A:
    f = float((C.loc[:"2024-07-29", "GBTC"] / K.loc[:"2024-07-29", "GBTC"]).median())
    A.loc[:"2024-07-29", "GBTC"] *= f; K.loc[:"2024-07-29", "GBTC"] *= f; print("GBTC olcek", round(f, 5))
bps = 1e4 * (K / C - 1)
print("son cubuk close vs gunluk close |bps| medyan/p95/p99:", [round(float(bps.abs().stack().quantile(q)), 1) for q in (.5, .95, .99)],
      ">100bps hucre:", int((bps.abs() > 100).sum().sum()))
A.to_pickle(os.path.join(pdz, "saatlik_1530.pkl")); K.to_pickle(os.path.join(pdz, "saatlik_kapanis.pkl")); yarim.to_pickle(os.path.join(pdz, "saatlik_yarim_gun.pkl"))
print("kod", A.shape[1], "gun", A.shape[0], A.index[0].date(), "->", A.index[-1].date(), "panel disi gun", list(fazla.date))
print("yarim gunler:", list(yarim[yarim].index.date)); print("son saati bozuk hucre:", int(bozuk.sum().sum()))
print("kod basina gun (min/medyan):", int(A.notna().sum().min()), int(A.notna().sum().median()), "en az:", A.notna().sum().nsmallest(5).to_dict())
