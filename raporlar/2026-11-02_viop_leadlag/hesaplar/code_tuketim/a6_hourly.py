"""A6: Saatlik (60m, ~2023-11+) testler. Bar zaman damgası = bar başlangıcı (UTC).
(a) AEFES <-> CCOLA: aynı saat, CCOLA_{h-1}->AEFES_h, AEFES_{h-1}->CCOLA_h (gün içi; gece hariç)
(b) ULKER <-> CC=F (kakao) aynı saat (örtüşen seans ~12:45/13:45-15:00 UTC), kakao_{h-1}->ULKER_h
(c) defansif sepet vs ES=F saatlik senkron beta (XU100 kontrollü)
Çıktı: a6_hourly.csv"""
from common import *
def hr(sym):
    d = ll.raw(ll.T(sym), "h1").copy(); d = d[d["c"] > 0]
    r = np.log(d["c"]).diff()
    day = d.index.tz_convert(None).normalize()
    r[pd.Series(day, index=d.index).diff().dt.days.fillna(1).values != 0] = np.nan  # gece/ilk bar
    return r
rows = []
def add(lab, a, b, k):
    df = pd.concat([a.rename("a"), b.shift(k).rename("b")], axis=1).dropna()
    df = df[(df["a"] != 0) & (df["b"] != 0)]
    if len(df) < 200: rows.append({"test": lab, "lag": k, "n": len(df)}); return
    c, t, n = nwcorr(df["a"], df["b"])
    rows.append({"test": lab, "lag": k, "corr": c, "t": t, "n": n})
A, C, U, X = hr("AEFES"), hr("CCOLA"), hr("ULKER"), hr("XU100")
xa, _ = resid(A, X); xc, _ = resid(C, X)
for k in (0, 1, 2): add("AEFES~CCOLA (ham)", A, C, k)
for k in (1, 2): add("CCOLA~AEFES (ham, ters)", C, A, k)
for k in (0, 1): add("AEFES~CCOLA (XU100 artık)", xa, xc, k)
add("CCOLA~AEFES (XU100 artık, ters)", xc, xa, 1)
try:
    K = ll.raw("CC=F", "h1").copy(); kr = np.log(K["c"]).diff()
    kr = kr.reindex(U.index)  # sadece BIST bar başlangıçlarıyla eşleşen kakao barları (zaman damgası aynıysa)
    print("kakao-BIST ortak bar sayısı:", int(kr.notna().sum()))
    # BIST barı [t, t+60) ; kakao barı farklı dakikalarda başlayabilir -> BIST bitişine en yakın kakao fiyatı ile hizala
    Kc = K["c"].sort_index(); ends = U.index + pd.Timedelta(minutes=60)
    pos = Kc.index.searchsorted(ends, side="right") - 1; pos0 = Kc.index.searchsorted(U.index, side="right") - 1
    ok = (pos >= 0) & (pos0 >= 0)
    kk = pd.Series(np.where(ok, np.log(Kc.values[np.clip(pos, 0, None)]) - np.log(Kc.values[np.clip(pos0, 0, None)]), np.nan), index=U.index)
    kk[kk == 0] = np.nan
    xu_, _ = resid(U, X)
    add("ULKER~kakao aynı saat (ham)", U, kk, 0); add("ULKER~kakao aynı saat (XU100 artık)", xu_, kk, 0); add("ULKER~kakao_{h-1}", U, kk, 1)
except Exception as e:
    print("kakao h1 hata", e)
E = ll.raw("ES=F", "h1").copy(); Ec = E["c"].sort_index(); ends = A.index + pd.Timedelta(minutes=60)
pos = Ec.index.searchsorted(ends, side="right") - 1; pos0 = Ec.index.searchsorted(A.index, side="right") - 1
es = pd.Series(np.log(Ec.values[np.clip(pos, 0, None)]) - np.log(Ec.values[np.clip(pos0, 0, None)]), index=A.index)
for s in ["BIMAS", "MGROS", "SOKM", "ULKER", "AEFES", "CCOLA", "XU100"]:
    h = hr(s) if s != "XU100" else X
    add(f"{s}~ES=F aynı saat (ham)", h, es.reindex(h.index), 0)
    if s != "XU100":
        add(f"{s}~ES=F aynı saat (XU100 artık)", resid(h, X)[0], es.reindex(h.index), 0)
H = pd.DataFrame(rows); H.to_csv(CODE + "/a6_hourly.csv", index=False)
print(H.round(3).to_string(index=False))
