"""İş Yatırım endeks gün içi indirici (2026-11-02 çalışmasındaki isy_fetch.py uyarlaması; yalnız endeks: XELKT, XU030, XU100).
Kaynak: https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll?period=P&from=...&to=...&endeks=KOD
Yanıt: {"data": [[epoch_ms, değer], ...]} -> yalnız son değer (kapanış), OHLC/hacim yok. period: 60, 30, 15, 5 (dk).
Sunucu bazı (from,to) pencerelerinde boş döner -> pencere ikiye bölünerek yeniden denenir.
Çıktı (ham): RAW/isy/<kind>/<KOD>.parquet (ts_utc, c).  Kullanım: python3 -I 04_isy_endeks.py h1|m30|m15|m5 [KOD...] [START=2017-01-01]"""
import os, sys, time, requests, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d2common import RAW, ISY_IDX, UA
U = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
S = requests.Session(); S.headers["User-Agent"] = UA
PER = {"h1": 60, "m30": 30, "m15": 15, "m5": 5}
STEP = {"h1": pd.DateOffset(years=1), "m30": pd.DateOffset(months=6), "m15": pd.DateOffset(months=6), "m5": pd.DateOffset(months=2)}
NREQ = [0]
def _req(code, period, a, b):
    NREQ[0] += 1
    try:
        r = S.get(U, params={"period": period, "from": a.strftime("%Y%m%d%H%M%S"), "to": b.strftime("%Y%m%d%H%M%S"), "endeks": code}, timeout=90)
        if r.status_code == 200 and r.text.strip():
            d = r.json().get("data") or []
            return pd.Series([x[1] for x in d], index=pd.to_datetime([x[0] for x in d], unit="ms"), dtype=float)
    except Exception:
        pass
    return pd.Series(dtype=float)
def _get(code, period, a, b, depth=0):
    """[a, b] penceresini indirir. Sunucu bazı pencerelerde BOŞ ya da KESİK (yalnız bir bölümü) döner:
    - boşsa: 'from' 1-2 gün geri çekilerek yeniden denenir, olmazsa pencere ikiye bölünür;
    - kesikse (ilk/son damga pencere ucundan > 5 gün uzakta): eksik baş/son parçası ayrıca istenir."""
    x = pd.Series(dtype=float)
    for k in range(3):
        x = _req(code, period, a - pd.Timedelta(days=k), b)
        if len(x): break
        time.sleep(0.3)
    gap = pd.Timedelta(days=5)
    if len(x) == 0:
        if (b - a) <= pd.Timedelta(days=4) or depth >= 5: return x
        mid = (a + (b - a) / 2).normalize()
        parts = [z for z in (_get(code, period, a, mid - pd.Timedelta(seconds=1), depth + 1), _get(code, period, mid, b, depth + 1)) if len(z)]
        return pd.concat(parts) if parts else x
    x = x[x.index >= a - pd.Timedelta(hours=3)]
    parts = [x]
    if depth < 5 and len(x) and (b - x.index.max()) > gap:
        parts.append(_get(code, period, (x.index.max() + pd.Timedelta(days=1)).normalize(), b, depth + 1))
    if depth < 5 and len(x) and (x.index.min() - a) > gap:
        parts.append(_get(code, period, a, x.index.min().normalize() - pd.Timedelta(seconds=1), depth + 1))
    parts = [z for z in parts if len(z)]
    return pd.concat(parts) if parts else x
def fetch(code, kind, start, end="2026-11-20"):
    p = f"{RAW}/isy/{kind}/{code}.parquet"; os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p): return "var"
    parts, miss = [], []; c = pd.Timestamp(start); e = pd.Timestamp(end) + pd.Timedelta(hours=23, minutes=59, seconds=59)
    while c <= e:
        n = min(c + STEP[kind] - pd.Timedelta(seconds=1), e)
        s = _get(code, PER[kind], c, n)
        if len(s): parts.append(s)
        else: miss.append(str(c.date()))
        c = c + STEP[kind]; time.sleep(0.5)
    if not parts: return "bos"
    s = pd.concat(parts).sort_index(); s = s[~s.index.duplicated(keep="last")]
    df = pd.DataFrame({"ts_utc": s.index, "c": s.values})
    df.to_parquet(p, index=False)
    return f"ok n={len(df)} {df.ts_utc.iloc[0]}..{df.ts_utc.iloc[-1]} bos_pencere={miss} istek={NREQ[0]}"
if __name__ == "__main__":
    kind = sys.argv[1]; args = [a for a in sys.argv[2:] if "=" not in a] or ISY_IDX
    kw = dict(a.split("=") for a in sys.argv[2:] if "=" in a)
    for c in args: print(c, kind, fetch(c, kind, kw.get("START", "2017-01-01")), flush=True)
