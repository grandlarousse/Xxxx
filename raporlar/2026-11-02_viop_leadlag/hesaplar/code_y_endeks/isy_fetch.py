"""İş Yatırım ChartData IndexHistoricalAll indirici (endeks VE hisse; sadece kapanış/son fiyat).
period: 1440=günlük, 60=saatlik, 5=5dk. Zaman damgası = UTC epoch, BAR BAŞLANGICI (Yahoo m5 ile birebir doğrulandı: 07:00 barı = 07:00-07:05 son fiyat;
15:00 barı = kapanış müzayedesi). Günlük: ts 21:00/22:00 UTC = ertesi TSİ günü 00:00 -> ldate = (ts+3h).normalize().
Hisse fiyatları temettü/bölünme düzeltmeli (gün-içi getiriyi etkilemez).
Kayıt: data/isy/{d,h1,m5}/<KOD>.parquet (sütun px, index UTC naive). Var olan dosyayı atlar (force=False).
Kullanım: python3 -I isy_fetch.py d|h1|m5 KOD1 KOD2 ...  [START=2015 END=2026-10-30]"""
import os, sys, time, requests, pandas as pd
BASE = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/isy"
U = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll"
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64)"
PER = {"d": 1440, "h1": 60, "m5": 5}
def _req(code, period, f, t):
    try:
        r = S.get(U, params={"period": period, "from": f, "to": t, "endeks": code}, timeout=90)
        if r.status_code == 200 and r.text.strip():
            d = r.json().get("data") or []
            return pd.Series([x[1] for x in d], index=pd.to_datetime([x[0] for x in d], unit="ms"), dtype=float)
    except Exception:
        pass
    return pd.Series(dtype=float)
def _get(code, period, f, t, tries=2, depth=0):
    """Sunucu bazı (from,to) pencereleri için deterministik olarak BOŞ dönüyor (yarıları dolu). Strateji: 2 deneme
    ('from' 1 gün geri çekilerek), olmazsa pencereyi ikiye bölüp özyineleme (en kısa 3 gün)."""
    a, b = pd.Timestamp(f), pd.Timestamp(t)
    for k in range(tries):
        a2 = a - pd.Timedelta(days=k)
        x = _req(code, period, a2.strftime("%Y%m%d%H%M%S"), b.strftime("%Y%m%d%H%M%S"))
        if len(x): return x[x.index >= a]
        time.sleep(0.4)
    if (b - a) <= pd.Timedelta(days=3) or depth >= 6: return pd.Series(dtype=float)
    mid = (a + (b - a) / 2).normalize()
    l = _get(code, period, a.strftime("%Y%m%d%H%M%S"), (mid - pd.Timedelta(seconds=1)).strftime("%Y%m%d%H%M%S"), tries, depth + 1)
    r = _get(code, period, mid.strftime("%Y%m%d%H%M%S"), b.strftime("%Y%m%d%H%M%S"), tries, depth + 1)
    parts = [z for z in (l, r) if len(z)]
    return pd.concat(parts) if parts else pd.Series(dtype=float)
def chunks(kind, start, end):
    s = pd.Timestamp(start); e = pd.Timestamp(end)
    if kind == "d": return [(s, e)]
    step = pd.DateOffset(years=1) if kind == "h1" else pd.DateOffset(months=3)
    out = []; c = s
    while c <= e:
        n = min(c + step - pd.Timedelta(seconds=1), e + pd.Timedelta(hours=23, minutes=59)); out.append((c, n)); c = c + step
    return out
def fetch(code, kind="d", start="2000-01-01", end="2026-10-30", force=False, sleep=0.6):
    p = os.path.join(BASE, kind, code + ".parquet"); os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p) and not force: return "cached"
    parts = []; miss = []
    for a, b in chunks(kind, start, end):
        s = _get(code, PER[kind], a.strftime("%Y%m%d%H%M%S"), b.strftime("%Y%m%d%H%M%S"), tries=(2 if kind != "d" else 6))
        if s is None or len(s) == 0: miss.append(str(a.date())); s = pd.Series(dtype=float)
        parts.append(s); time.sleep(sleep)
    parts = [x for x in parts if len(x)]
    if not parts: return "empty"
    s = pd.concat(parts).sort_index(); s = s[~s.index.duplicated(keep="last")]
    s = s[s.index < pd.Timestamp(end) + pd.Timedelta(days=1) - pd.Timedelta(hours=3)] if kind == "d" else s[s.index < pd.Timestamp(end) + pd.Timedelta(days=1)]
    if len(s) == 0: return "empty"
    df = s.rename("px").to_frame()
    if kind == "d": df["ldate"] = (df.index + pd.Timedelta(hours=3)).normalize()
    df.to_parquet(p); return f"ok n={len(df)} {df.index[0]}..{df.index[-1]} empty_chunks={miss}"
if __name__ == "__main__":
    kind = sys.argv[1]; args = [a for a in sys.argv[2:] if "=" not in a]
    kw = dict(a.split("=") for a in sys.argv[2:] if "=" in a)
    st = kw.get("START", "2000-01-01" if kind == "d" else "2015-01-01"); en = kw.get("END", "2026-10-30")
    for c in args: print(c, kind, fetch(c, kind, st, en), flush=True)
